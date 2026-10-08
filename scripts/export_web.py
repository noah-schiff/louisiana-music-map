"""Export LouisianaMusic.gdb to a single self-contained web/index.html."""
import datetime, json, re, sys, tempfile
from functools import reduce
from pathlib import Path
import schema, geo

TOLERANCE = "300 Meters"
TX = "WGS_1984_(ITRF00)_To_NAD_1983"
BS = chr(92)  # backslash, spelled out so no tool can collapse the escape

def round_coords(obj, places=4):
    if isinstance(obj, (list, tuple)):
        return [round_coords(o, places) for o in obj]
    return round(obj, places) if isinstance(obj, float) else obj

def embed_json(data) -> str:
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return text.replace("</", "<" + BS + "/").replace("<!--", "<" + BS + "u0021--")

def render(template: str, parts: dict) -> str:
    return re.sub(r"\{\{(\w+)\}\}", lambda m: parts[m.group(1)], template)

def split_template(template: str):
    """One template, two pages. <!--S-->...<!--/S--> blocks are the standalone-only document
    wrapper: kept (markers removed) for index.html, dropped for the Claude artifact fragment."""
    standalone = re.sub(r"<!--/?S-->", "", template)
    fragment = re.sub(r"<!--S-->.*?<!--/S-->", "", template, flags=re.S)
    return standalone, fragment

def _geojson(fc, keep):
    """Feature class -> WGS 84 GeoJSON FeatureCollection with only the `keep` properties."""
    import arcpy
    with tempfile.TemporaryDirectory() as d:
        out = str(Path(d) / "x.geojson")
        arcpy.conversion.FeaturesToJSON(str(fc), out, geoJSON="GEOJSON", outputToWGS84="WGS84")
        fcoll = json.loads(Path(out).read_text(encoding="utf-8"))
    feats = [{"type": "Feature",
              "properties": {k: f["properties"].get(k) for k in keep},
              "geometry": {"type": f["geometry"]["type"], "coordinates": round_coords(f["geometry"]["coordinates"])}}
             for f in fcoll["features"] if f.get("geometry")]
    return {"type": "FeatureCollection", "features": feats}

def _rows(table, fields):
    import arcpy
    with arcpy.da.SearchCursor(str(table), fields) as c:
        return [dict(zip(fields, r)) for r in c]

def collect(gdb_path) -> dict:
    import arcpy
    gdb = Path(gdb_path); P = lambda n: str(gdb / n)
    arcpy.env.overwriteOutput = True
    arcpy.env.geographicTransformations = TX
    wgs = arcpy.SpatialReference(4326)

    # Simplify parishes once; build web regions from the SAME simplified shapes so edges coincide.
    arcpy.cartography.SimplifyPolygon(P("Base_Parishes"), P("tmp_par"), "POINT_REMOVE", TOLERANCE,
                                      collapsed_point_option="NO_KEEP")
    arcpy.management.Dissolve(P("tmp_par"), P("tmp_state"))
    with arcpy.da.SearchCursor(P("tmp_par"), ["NAME", "SHAPE@"]) as c:
        shapes = {geo.norm_parish(n): s for n, s in c}
    reg_fields = ["region_id", "genre_id", "label", "year_start", "year_end", "note", "sources", "parishes"]
    arcpy.management.CreateFeatureclass(str(gdb), "tmp_reg", "POLYGON", template=P("Regions"),
                                        spatial_reference=arcpy.Describe(P("Regions")).spatialReference)
    with arcpy.da.InsertCursor(P("tmp_reg"), ["SHAPE@"] + reg_fields) as ic:
        for row in _rows(P("Regions"), reg_fields):
            got, missing = geo.match_parishes(row["parishes"].split(";"), shapes)
            if missing:
                raise schema.SchemaError([f"{row['region_id']}: no parish named '{m.strip()}'" for m in missing])
            ic.insertRow([reduce(lambda a, b: a.union(b), got)] + [row[f] for f in reg_fields])

    regions = _geojson(P("tmp_reg"), reg_fields[:-1])
    for f in regions["features"]:
        f["properties"]["sources"] = schema.parse_sources(f["properties"]["sources"] or "")
    base = {"state": _geojson(P("tmp_state"), []),
            "parishes": _geojson(P("tmp_par"), ["NAME"]),
            "rivers": _geojson(P("Base_Rivers"), ["name"]),
            "lakes": _geojson(P("Base_Lakes"), ["name"]),
            "cities": []}
    for f in base["parishes"]["features"]:
        f["properties"] = {"name": f["properties"]["NAME"]}
    base["ecoregions"] = {"type": "FeatureCollection", "features": []}
    if arcpy.Exists(P("Base_Ecoregions")):
        arcpy.cartography.SimplifyPolygon(P("Base_Ecoregions"), P("tmp_eco"), "POINT_REMOVE", TOLERANCE,
                                          collapsed_point_option="NO_KEEP")
        base["ecoregions"] = _geojson(P("tmp_eco"), ["eco_id", "name", "description", "sources"])
        for f in base["ecoregions"]["features"]:
            f["properties"]["sources"] = schema.parse_sources(f["properties"]["sources"] or "")
    nature = {}
    if arcpy.Exists(P("Nature")):
        for n in _rows(P("Nature"), ["tbl", "row_id", "nature_note", "sources"]):
            nature[(n["tbl"], n["row_id"])] = {"note": n["nature_note"],
                                               "sources": schema.parse_sources(n["sources"] or "")}
    for f in regions["features"]:
        f["properties"]["nature"] = nature.get(("regions", f["properties"]["region_id"]))
    with arcpy.da.SearchCursor(P("Base_Cities"), ["name", "SHAPE@"]) as c:
        for name, shp in c:
            pt = shp.projectAs(wgs, TX).firstPoint
            base["cities"].append({"name": name, "lat": round(pt.Y, 4), "lon": round(pt.X, 4)})

    genres = _rows(P("Genres"), ["genre_id", "name", "color", "year_start", "year_end", "summary", "sources"])
    for g in genres:
        g["sources"] = schema.parse_sources(g["sources"] or "")
        g["nature"] = nature.get(("genres", g["genre_id"]))
    eras = sorted(_rows(P("Eras"), ["era_id", "name", "year_start", "year_end", "summary"]),
                  key=lambda e: e["year_start"])
    pf = ["place_id", "name", "type", "genre_id", "other_genres", "year_start", "year_end", "town", "parish",
          "writeup", "listen_1_label", "listen_1_url", "listen_2_label", "listen_2_url", "sources"]
    places = []
    with arcpy.da.SearchCursor(P("Places"), ["SHAPE@"] + pf) as c:
        for row in c:
            p = dict(zip(pf, row[1:]))
            pt = row[0].projectAs(wgs, TX).firstPoint
            p["lat"], p["lon"] = round(pt.Y, 4), round(pt.X, 4)
            p["other_genres"] = [g.strip() for g in (p["other_genres"] or "").split(";") if g.strip()]
            p["sources"] = schema.parse_sources(p["sources"] or "")
            p["nature"] = nature.get(("places", p["place_id"]))
            p["listen"] = [{"label": p[f"listen_{n}_label"], "url": p[f"listen_{n}_url"]}
                           for n in ("1", "2") if p[f"listen_{n}_url"]]
            for n in ("1", "2"):
                del p[f"listen_{n}_label"], p[f"listen_{n}_url"]
            places.append(p)
    places.sort(key=lambda p: (p["year_start"], p["place_id"]))

    for t in ("tmp_par", "tmp_par_Pnt", "tmp_state", "tmp_reg", "tmp_eco", "tmp_eco_Pnt"):
        if arcpy.Exists(P(t)):
            arcpy.management.Delete(P(t))
    # Nothing may drop out between the geodatabase and the page (e.g. a feature with empty geometry).
    for fc, got in (("Regions", len(regions["features"])), ("Places", len(places)), ("Genres", len(genres))):
        n = int(arcpy.management.GetCount(P(fc))[0])
        if got != n:
            raise ValueError(f"{fc}: {n} in the geodatabase but {got} exported")
    counts = {"genres": len(genres), "eras": len(eras), "regions": len(regions["features"]), "places": len(places)}
    return {"meta": {"built": datetime.date.today().isoformat(), "counts": counts},
            "eras": eras, "genres": genres, "regions": regions, "places": places, "base": base}

def export(gdb_path, web_dir) -> dict:
    web = Path(web_dir)
    read = lambda rel: (web / rel).read_text(encoding="utf-8")
    data = collect(gdb_path)
    parts = {"LEAFLET_CSS": read("vendor/leaflet.css"), "APP_CSS": read("src/app.css"),
             "LEAFLET_JS": read("vendor/leaflet.js"), "CORE_JS": read("src/core.js"),
             "APP_JS": read("src/app.js"), "DATA": embed_json(data)}
    for k in ("LEAFLET_JS", "CORE_JS", "APP_JS"):
        if "</script" in parts[k].lower():
            raise ValueError(f"{k} contains a closing script tag and cannot be inlined")
    standalone, fragment = split_template(read("src/template.html"))
    html = render(standalone, parts)
    (web / "index.html").write_text(html, encoding="utf-8", newline="\n")
    (web / "artifact.html").write_text(render(fragment, parts).strip() + "\n", encoding="utf-8", newline="\n")
    print("Exported:", data["meta"]["counts"], f"| index.html {len(html.encode('utf-8')) / 1024:.0f} KB")
    return data["meta"]["counts"]

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    export(root / "LouisianaMusic.gdb", root / "web")

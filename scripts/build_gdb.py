"""Build LouisianaMusic.gdb from the research CSVs and data_raw. Rebuilds from scratch."""
import sys
from functools import reduce
from pathlib import Path
import arcpy
import schema, geo

SR = arcpy.SpatialReference(26915)
WGS = arcpy.SpatialReference(4326)
TX = "WGS_1984_(ITRF00)_To_NAD_1983"

def _count(fc):
    return int(arcpy.management.GetCount(str(fc))[0])

def _table(gdb, name, fields, rows):
    t = arcpy.management.CreateTable(str(gdb), name)[0]
    arcpy.management.AddFields(t, [[f, ty, f, ln] for f, ty, ln in fields])
    with arcpy.da.InsertCursor(t, [f for f, _, _ in fields]) as c:
        for r in rows:
            c.insertRow(r)

def _src(sources):
    return " | ".join(f"{s['label']} <{s['url']}>" if s["url"] else s["label"] for s in sources)

def build(research_dir, raw_dir, gdb_path) -> dict:
    research_dir, raw_dir, gdb = Path(research_dir), Path(raw_dir), Path(gdb_path)
    R = schema.load_research(research_dir)
    arcpy.env.overwriteOutput = True
    arcpy.env.geographicTransformations = TX
    if arcpy.Exists(str(gdb)):
        arcpy.management.Delete(str(gdb))
    arcpy.management.CreateFileGDB(str(gdb.parent), gdb.name)
    P = lambda n: str(gdb / n)

    # Parishes: shoreline-clipped Census cartographic boundaries, Louisiana only.
    cb = str(raw_dir / "cb_2023_us_county_500k" / "cb_2023_us_county_500k.shp")
    arcpy.conversion.ExportFeatures(cb, P("tmp_la"), where_clause="STATEFP = '22'")
    arcpy.management.Project(P("tmp_la"), P("Base_Parishes"), SR)
    arcpy.management.RepairGeometry(P("Base_Parishes"))
    arcpy.management.Dissolve(P("Base_Parishes"), P("Base_State"))
    n_par = _count(P("Base_Parishes"))
    if n_par != 64:
        raise schema.SchemaError([f"expected 64 parishes, found {n_par}"])

    # Water: clip Natural Earth to a box around the state (in WGS 84), then project.
    ext = arcpy.Describe(P("tmp_la")).extent
    box = arcpy.Polygon(arcpy.Array([arcpy.Point(x, y) for x, y in [
        (ext.XMin - 0.6, ext.YMin - 0.4), (ext.XMin - 0.6, ext.YMax + 0.4),
        (ext.XMax + 0.6, ext.YMax + 0.4), (ext.XMax + 0.6, ext.YMin - 0.4)]]), WGS)
    rivers = []
    for name in ("ne_10m_rivers_lake_centerlines", "ne_10m_rivers_north_america"):
        arcpy.analysis.Clip(str(raw_dir / name / f"{name}.shp"), box, P(f"tmp_{name}"))
        rivers.append(P(f"tmp_{name}"))
    arcpy.management.Merge(rivers, P("tmp_rivers"))
    arcpy.management.Project(P("tmp_rivers"), P("Base_Rivers"), SR)
    arcpy.analysis.Clip(str(raw_dir / "ne_10m_lakes" / "ne_10m_lakes.shp"), box, P("tmp_lakes"))
    arcpy.management.Project(P("tmp_lakes"), P("Base_Lakes"), SR)
    # Natural regions: EPA Level III ecoregions, trimmed to the same coastline as the parishes.
    eco_shp = raw_dir / "la_eco_l3" / "la_eco_l3.shp"
    n_eco = 0
    if eco_shp.exists():
        arcpy.management.Project(str(eco_shp), P("tmp_eco"), SR)
        arcpy.analysis.Clip(P("tmp_eco"), P("Base_State"), P("tmp_eco_clip"))
        arcpy.management.Dissolve(P("tmp_eco_clip"), P("Base_Ecoregions"), ["US_L3CODE", "US_L3NAME"])
        arcpy.management.AddFields(P("Base_Ecoregions"), [["eco_id", "TEXT", "eco_id", 8], ["name", "TEXT", "name", 100],
                                                          ["description", "TEXT", "description", 1500],
                                                          ["sources", "TEXT", "sources", 2000]])
        info = {e["eco_id"]: e for e in R["ecoregions"]}
        with arcpy.da.UpdateCursor(P("Base_Ecoregions"),
                                   ["US_L3CODE", "US_L3NAME", "eco_id", "name", "description", "sources"]) as c:
            for code, epa_name, *_ in c:
                e = info.get(code, {})
                c.updateRow([code, epa_name, code, e.get("name") or epa_name, e.get("description", ""),
                             _src(e.get("sources", []))])
        del c                                   # an open edit cursor keeps the whole workspace locked
        n_eco = _count(P("Base_Ecoregions"))
    arcpy.management.ClearWorkspaceCache()

    arcpy.env.workspace = str(gdb)          # cleanup stays after the water steps: `ext` came from tmp_la
    for t in arcpy.ListFeatureClasses("tmp_*"):
        arcpy.management.Delete(t)

    def points(name, fields, rows):
        fc = arcpy.management.CreateFeatureclass(str(gdb), name, "POINT", spatial_reference=SR)[0]
        arcpy.management.AddFields(fc, [[f, ty, f, ln] for f, ty, ln in fields])
        with arcpy.da.InsertCursor(fc, ["SHAPE@"] + [f for f, _, _ in fields]) as c:
            for lon, lat, vals in rows:
                c.insertRow([arcpy.PointGeometry(arcpy.Point(lon, lat), WGS).projectAs(SR, TX)] + vals)

    points("Base_Cities", [("name", "TEXT", 60)], [(c["lon"], c["lat"], [c["name"]]) for c in R["cities"]])

    _table(gdb, "Genres", [("genre_id", "TEXT", 40), ("name", "TEXT", 100), ("color", "TEXT", 7),
                           ("year_start", "LONG", None), ("year_end", "LONG", None),
                           ("summary", "TEXT", 2000), ("sources", "TEXT", 2000)],
           [[g["genre_id"], g["name"], g["color"], g["year_start"], g["year_end"], g["summary"], _src(g["sources"])]
            for g in R["genres"]])
    _table(gdb, "Eras", [("era_id", "TEXT", 40), ("name", "TEXT", 100), ("year_start", "LONG", None),
                         ("year_end", "LONG", None), ("summary", "TEXT", 2000)],
           [[e["era_id"], e["name"], e["year_start"], e["year_end"], e["summary"]] for e in R["eras"]])

    # Regions: union of the named parishes. Report the match rate; any miss is an error.
    with arcpy.da.SearchCursor(P("Base_Parishes"), ["NAME", "SHAPE@"]) as c:
        shapes = {geo.norm_parish(n): s for n, s in c}
    reg_fields = [("region_id", "TEXT", 60), ("genre_id", "TEXT", 40), ("label", "TEXT", 120),
                  ("year_start", "LONG", None), ("year_end", "LONG", None), ("parishes", "TEXT", 1500),
                  ("note", "TEXT", 1000), ("sources", "TEXT", 2000)]
    fc = arcpy.management.CreateFeatureclass(str(gdb), "Regions", "POLYGON", spatial_reference=SR)[0]
    arcpy.management.AddFields(fc, [[f, ty, f, ln] for f, ty, ln in reg_fields])
    probs, listed, matched = [], 0, 0
    with arcpy.da.InsertCursor(fc, ["SHAPE@"] + [f for f, _, _ in reg_fields]) as c:
        for r in R["regions"]:
            got, missing = geo.match_parishes(r["parishes"], shapes)
            listed += len(r["parishes"]); matched += len(got)
            probs += [f"{r['region_id']}: no parish named '{m}'" for m in missing]
            if got and not missing:
                c.insertRow([reduce(lambda a, b: a.union(b), got), r["region_id"], r["genre_id"], r["label"],
                             r["year_start"], r["year_end"], "; ".join(r["parishes"]), r["note"], _src(r["sources"])])
    print(f"Regions: {matched} of {listed} listed parishes matched")
    if probs:
        raise schema.SchemaError(probs)

    points("Places", [("place_id", "TEXT", 60), ("name", "TEXT", 150), ("type", "TEXT", 30),
                      ("genre_id", "TEXT", 40), ("other_genres", "TEXT", 200), ("year_start", "LONG", None),
                      ("year_end", "LONG", None), ("town", "TEXT", 80), ("parish", "TEXT", 60),
                      ("out_of_state", "SHORT", None), ("writeup", "TEXT", 3000),
                      ("listen_1_label", "TEXT", 150), ("listen_1_url", "TEXT", 500),
                      ("listen_2_label", "TEXT", 150), ("listen_2_url", "TEXT", 500), ("sources", "TEXT", 2000)],
           [(p["lon"], p["lat"], [p["place_id"], p["name"], p["type"], p["genre_id"], "; ".join(p["other_genres"]),
                                  p["year_start"], p["year_end"], p["town"], p["parish"], int(p["out_of_state"]),
                                  p["writeup"], p["listen_1_label"], p["listen_1_url"], p["listen_2_label"],
                                  p["listen_2_url"], _src(p["sources"])]) for p in R["places"]])

    _table(gdb, "Nature", [("tbl", "TEXT", 10), ("row_id", "TEXT", 60), ("nature_note", "TEXT", 1500),
                           ("sources", "TEXT", 2000)],
           [[n["table"], n["row_id"], n["nature_note"], _src(n["sources"])] for n in R["nature"]])

    counts = {"genres": _count(P("Genres")), "eras": _count(P("Eras")), "regions": _count(P("Regions")),
              "places": _count(P("Places")), "cities": _count(P("Base_Cities")), "parishes": n_par,
              "ecoregions": n_eco, "nature": _count(P("Nature"))}
    print("Built:", counts, "| read:", {k: len(v) for k, v in R.items()})
    return counts

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    try:
        build(root / "research", root / "data_raw", root / "LouisianaMusic.gdb")
    except schema.SchemaError as e:
        print(f"{len(e.problems)} problem(s):"); print("\n".join("  " + p for p in e.problems)); sys.exit(1)

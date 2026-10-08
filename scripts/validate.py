"""Checks run after every build. Prints numbers; exits 1 if anything is wrong."""
import sys
from pathlib import Path
from urllib.parse import quote
import requests
import schema

OEMBED = "https://www.youtube.com/oembed?format=json&url="
UA = {"User-Agent": "Mozilla/5.0 (Louisiana Music Map link check)"}

def check_gdb(research_dir, gdb_path) -> list:
    import arcpy
    R, gdb, probs = schema.load_research(research_dir), Path(gdb_path), []
    for table, fc in (("genres", "Genres"), ("eras", "Eras"), ("regions", "Regions"), ("places", "Places"),
                      ("nature", "Nature")):
        if not arcpy.Exists(str(gdb / fc)):
            probs.append(f"{fc}: missing from the geodatabase"); continue
        n = int(arcpy.management.GetCount(str(gdb / fc))[0])
        if n != len(R[table]):
            probs.append(f"{fc}: {n} built but {len(R[table])} in research")
    with arcpy.da.SearchCursor(str(gdb / "Base_State"), ["SHAPE@"]) as c:
        state = next(c)[0]
    by_id = {p["place_id"]: p for p in R["places"]}
    with arcpy.da.SearchCursor(str(gdb / "Places"), ["place_id", "SHAPE@", "out_of_state"]) as c:
        for pid, shp, oos in c:
            # 2 km tolerance: barrier islands and river-edge sites sit on a generalized coastline.
            if not oos and state.distanceTo(shp) > 2000:
                p = by_id[pid]
                probs.append(f"{pid}: point is outside Louisiana ({p['lat']}, {p['lon']})")
    with arcpy.da.SearchCursor(str(gdb / "Regions"), ["region_id", "SHAPE@AREA"]) as c:
        probs += [f"{rid}: empty geometry" for rid, area in c if not area]
    return probs

def check_links(urls) -> list:
    bad = []
    for u in urls:
        # A removed YouTube video still serves a normal watch page; oEmbed says whether it exists.
        youtube = "youtube.com/watch" in u or "youtu.be/" in u
        target = OEMBED + quote(u, safe="") if youtube else u
        try:
            code = requests.get(target, headers=UA, timeout=20, stream=True).status_code
        except requests.RequestException as e:
            bad.append((u, f"broken ({type(e).__name__})")); continue
        if youtube and code in (400, 404):
            bad.append((u, "broken (video unavailable)"))
        elif code in (401, 403, 429):
            bad.append((u, f"check by hand ({code})"))
        elif code >= 400:
            bad.append((u, f"broken ({code})"))
    return bad

def all_urls(R) -> list:
    urls = {s["url"] for t in ("genres", "regions", "places") for row in R[t] for s in row["sources"] if s["url"]}
    urls |= {l["url"] for p in R["places"] for l in p["listen"]}
    urls |= {s["url"] for t in ("nature", "ecoregions") for row in R.get(t, []) for s in row["sources"] if s["url"]}
    return sorted(urls)

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    probs = check_gdb(root / "research", root / "LouisianaMusic.gdb")
    print(f"Geodatabase checks: {len(probs)} problem(s)")
    R = schema.load_research(root / "research")
    print(f"Places with a listen link: {sum(1 for p in R['places'] if p['listen'])} of {len(R['places'])}")
    if "--links" in sys.argv:
        urls = all_urls(schema.load_research(root / "research"))
        bad = check_links(urls)
        print(f"Links: {len(urls) - len(bad)} of {len(urls)} responded OK")
        probs += [f"{u}: {why}" for u, why in bad]
    print("\n".join("  " + p for p in probs))
    sys.exit(1 if probs else 0)

"""Mechanical checks on newly researched place batches before they are built into the map.

Usage:  python verify_new_places.py places_E.csv places_F.csv places_G.csv

For every row: all 18 columns, a unique new id, valid type and genre ids, year_start not before
the genre's, a 60-120 word write-up, a point inside the Louisiana outline (from the geodatabase),
no existing place within 60 m (a likely duplicate), and a listen link that YouTube confirms.
Prints one line per row plus any problems. Facts are checked separately by a human or a fact-checker.
"""
import csv, sys
from pathlib import Path
from urllib.parse import quote
import requests

here = Path(__file__).resolve().parent
root = here.parents[1]
sys.path.insert(0, str(root / "scripts"))
import schema

sys.stdout.reconfigure(encoding="utf-8")
OEMBED = "https://www.youtube.com/oembed?format=json&url="
UA = {"User-Agent": "Mozilla/5.0 (Louisiana Music Map link check)"}
new_files = [here / a for a in sys.argv[1:]]

def read(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))

genres = {g["genre_id"]: int(g["year_start"]) for g in read(here.parent / "genres.csv")}
existing = [r for f in sorted(here.glob("places_*.csv")) if f not in new_files for r in read(f)]
existing += [r for r in read(here.parent / "places.csv")]          # includes fact-checker additions
seen = {r["place_id"] for r in existing}

import arcpy
gdb = root / "LouisianaMusic.gdb"
with arcpy.da.SearchCursor(str(gdb / "Base_State"), ["SHAPE@"]) as c:
    state = next(c)[0]
sr, wgs = state.spatialReference, arcpy.SpatialReference(4326)
def pt(lat, lon):
    return arcpy.PointGeometry(arcpy.Point(float(lon), float(lat)), wgs).projectAs(sr, "WGS_1984_(ITRF00)_To_NAD_1983")
old_pts = {r["place_id"]: pt(r["lat"], r["lon"]) for r in existing}

total = bad = 0
for f in new_files:
    rows = read(f)
    print(f"\n== {f.name}: {len(rows)} rows")
    for r in rows:
        total += 1
        probs = [f"missing column {c}" for c in schema.COLUMNS["places"] if c not in r]
        pid = r.get("place_id", "?")
        if probs:
            print(f"FAIL {pid}: {probs}"); bad += 1; continue
        if pid in seen: probs.append("id already used")
        seen.add(pid)
        if r["type"] not in schema.PLACE_TYPES: probs.append(f"type '{r['type']}'")
        gs = [r["genre_id"]] + [g.strip() for g in r["other_genres"].split(";") if g.strip()]
        probs += [f"unknown genre '{g}'" for g in gs if g not in genres]
        try:
            ys = int(r["year_start"]); ye = int(r["year_end"]) if r["year_end"].strip() else None
            if r["genre_id"] in genres and ys < genres[r["genre_id"]]:
                probs.append(f"starts {ys}, before its genre ({genres[r['genre_id']]})")
            if ye is not None and ye < ys: probs.append("ends before it starts")
        except ValueError:
            probs.append("year is not a whole number")
        words = len(r["writeup"].split())
        if not 60 <= words <= 120: probs.append(f"write-up is {words} words")
        if not schema.parse_sources(r["sources"]): probs.append("no sources")
        elif all("wikipedia.org" in s["url"] for s in schema.parse_sources(r["sources"])): probs.append("Wikipedia is the only source")
        try:
            g = pt(r["lat"], r["lon"])
            d = state.distanceTo(g)
            if d > 2000: probs.append(f"point is {d/1000:.1f} km outside Louisiana")
            near = sorted((g.distanceTo(o), k) for k, o in old_pts.items())[:1]
            if near and near[0][0] < 60: probs.append(f"within {near[0][0]:.0f} m of existing place '{near[0][1]}'")
            old_pts[pid] = g
        except Exception as e:
            probs.append(f"bad coordinates ({e})")
        yt = ""
        u, label = r["listen_1_url"].strip(), r["listen_1_label"].strip()
        if bool(u) != bool(label): probs.append("listen link needs both label and url")
        elif u:
            try:
                if "youtube.com/watch" in u or "youtu.be/" in u:
                    resp = requests.get(OEMBED + quote(u, safe=""), headers=UA, timeout=20)
                    if resp.status_code != 200: probs.append(f"YouTube oEmbed returned {resp.status_code}")
                    else:
                        j = resp.json(); yt = f"{j.get('title','')} // {j.get('author_name','')}"
                else:
                    code = requests.get(u, headers=UA, timeout=20, stream=True).status_code
                    yt = f"(not YouTube) HTTP {code}"
                    if code >= 400 and code not in (401, 403, 429): probs.append(f"listen link returned {code}")
            except requests.RequestException as e:
                probs.append(f"listen link failed ({type(e).__name__})")
        if r["listen_2_url"].strip() or r["listen_2_label"].strip(): probs.append("listen_2 should be blank")
        bad += bool(probs)
        print(f"{'FAIL' if probs else 'ok  '} {pid} | {r['name']} | {r['year_start']}-{r['year_end'] or 'today'} | {r['town']}, {r['parish']} | {r['genre_id']} | {words}w")
        if label: print(f"       listen: {label}\n       actual: {yt}")
        for p in probs: print(f"       PROBLEM: {p}")
print(f"\nrows: {total} | with problems: {bad}")

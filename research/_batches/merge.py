"""Merge research\\_batches\\places_*.csv into research\\places.csv (sorted by year, ids unique)."""
import csv, sys
from pathlib import Path

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here.parents[1] / "scripts"))
import schema

cols = schema.COLUMNS["places"]
rows, seen = [], {}
for f in sorted(here.glob("places_*.csv")):
    with open(f, newline="", encoding="utf-8-sig") as fh:
        batch = list(csv.DictReader(fh))
    print(f.name, len(batch))
    for r in batch:
        r = {c: (r.get(c) or "").strip() for c in cols}
        if r["place_id"] in seen:
            print("  DUPLICATE id", r["place_id"], "in", f.name, "and", seen[r["place_id"]]); continue
        seen[r["place_id"]] = f.name
        rows.append(r)
rows.sort(key=lambda r: (int(r["year_start"]), r["place_id"]))
with open(here.parent / "places.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(rows)
print("places.csv", len(rows))

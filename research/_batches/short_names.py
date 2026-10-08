"""Shorten genre display names so the legend reads on one line. Re-runnable."""
import csv
from pathlib import Path

NAMES = {"ancient": "Ancient mound builders", "native": "Native nations", "colonial": "Colonial French and Spanish",
         "congo": "Congo Square traditions", "creole": "Creole and la-la", "cajun": "Cajun",
         "mardigras_indian": "Mardi Gras Indians", "blues": "Blues", "gospel": "Gospel and spirituals",
         "country": "Country and the Hayride", "rnb": "R&B and early rock", "funk": "Funk", "hiphop": "Hip-hop"}
f = Path(__file__).resolve().parents[1] / "genres.csv"
with open(f, newline="", encoding="utf-8-sig") as fh:
    rd = csv.DictReader(fh); cols = rd.fieldnames; rows = list(rd)
for r in rows:
    r["name"] = NAMES.get(r["genre_id"], r["name"])
with open(f, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_ALL); w.writeheader(); w.writerows(rows)
print([r["name"] for r in rows])

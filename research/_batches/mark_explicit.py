"""Add editorial lines to fix_zz_editorial.csv that mark recordings with explicit lyrics in their
listen label. The current label is read from places.csv, so run this after rebuild_research.py;
it is safe to run again."""
import csv
from pathlib import Path

here = Path(__file__).resolve().parent
EXPLICIT = ["magnolia_projects_cash_money", "calliope_projects_no_limit", "ghost_town_lounge",
            "odyssey_records_carrollton"]
NOTE = "explicit lyrics"

places = {r["place_id"]: r for r in csv.DictReader(open(here.parent / "places.csv", encoding="utf-8-sig", newline=""))}
f = here / "fix_zz_editorial.csv"
rows = list(csv.DictReader(open(f, encoding="utf-8-sig", newline="")))
cols = list(rows[0].keys())
rows = [r for r in rows if not (r["field"] == "listen_1_label" and r["row_id"] in EXPLICIT)]
for pid in EXPLICIT:
    label = places[pid]["listen_1_label"]
    assert label, pid + " has no listen label"
    if NOTE not in label:
        label = label[:-1] + "; " + NOTE + ")" if label.endswith(")") else label + " (" + NOTE + ")"
    rows.append({"table": "places", "row_id": pid, "field": "listen_1_label", "new_value": label, "evidence_url": "",
                 "reason": "Editorial: the recording contains explicit lyrics and the label says so, so a reader can "
                           "choose. It stays because it is the record the place is known for."})
    print(pid, "->", label)
with open(f, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_ALL)
    w.writeheader()
    w.writerows(rows)

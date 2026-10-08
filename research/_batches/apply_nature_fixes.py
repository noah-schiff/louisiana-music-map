"""Rebuild research\\nature.csv and ecoregions.csv from the researcher's files plus the fact-check
corrections in fix_nature.csv (columns: file,table,row_id,field,new_value,evidence_url,reason)."""
import csv
from pathlib import Path

here = Path(__file__).resolve().parent
research = here.parent

def read(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh)
        return rd.fieldnames, list(rd)

ncols, nature = read(here / "nature_notes.csv")
ecols, eco = read(here / "ecoregions.csv")
_, fixes = read(here / "fix_nature.csv")
log, changed, deleted, skipped = [], 0, 0, []
for x in fixes:
    f, t, rid, field, val = (x[k].strip() for k in ("file", "table", "row_id", "field", "new_value"))
    if f == "nature":
        rows, row = nature, next((r for r in nature if r["table"] == t and r["row_id"] == rid), None)
    else:
        rows, row = eco, next((r for r in eco if r["eco_id"] == rid), None)
    if row is None:
        skipped.append(f"{f} {t} {rid}: no such row"); continue
    if field == "DELETE_ROW":
        rows.remove(row); deleted += 1
        log.append(f"- land-and-sound `{rid}` ({t or 'ecoregion'}): removed. {x['reason']}"); continue
    if field not in row:
        skipped.append(f"{f} {rid}: unknown field {field}"); continue
    if row[field] != val:
        row[field] = val; changed += 1
        log.append(f"- land-and-sound `{rid}` ({t or 'ecoregion'}) {field}: revised. {x['reason']} ({x['evidence_url']})")

for name, cols, rows in (("nature.csv", ncols, nature), ("ecoregions.csv", ecols, eco)):
    with open(research / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_ALL); w.writeheader(); w.writerows(rows)

notes = research / "NOTES.md"
text = notes.read_text(encoding="utf-8")
marker = "\n## Land-and-sound fact-check corrections\n"
notes.write_text(text.split(marker)[0].rstrip() + "\n" + marker + "\n" + "\n".join(log) + "\n",
                 encoding="utf-8", newline="\n")
print(f"nature rows: {len(nature)} | ecoregions: {len(eco)} | fields changed: {changed} | deleted: {deleted} | skipped: {skipped}")

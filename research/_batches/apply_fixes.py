"""Apply fact-check corrections (fix_*.csv) to the research CSVs and log them in NOTES.md.

Each correction line: table,row_id,field,new_value,evidence_url,reason
field == DELETE_ROW removes the row. A row_id that does not exist yet is created (places only).
Run AFTER merge.py; merge.py rebuilds places.csv from the raw batches and would undo these.
"""
import csv, sys
from pathlib import Path

here = Path(__file__).resolve().parent
research = here.parent
sys.path.insert(0, str(research.parent / "scripts"))
import schema

tables = {}
for t in ("places", "genres", "regions", "eras"):
    with open(research / f"{t}.csv", newline="", encoding="utf-8-sig") as fh:
        tables[t] = list(csv.DictReader(fh))

log, changed, deleted, added, skipped = [], 0, 0, 0, []
for f in sorted(here.glob("fix_*.csv")):
    with open(f, newline="", encoding="utf-8-sig") as fh:
        fixes = list(csv.DictReader(fh))
    if fixes and "file" in fixes[0]:
        continue                      # land-and-sound corrections: handled by apply_nature_fixes.py
    print(f.name, len(fixes), "lines")
    for x in fixes:
        t, rid, field, val = x["table"].strip(), x["row_id"].strip(), x["field"].strip(), x["new_value"].strip()
        idf, cols = schema.ID_FIELD[t], schema.COLUMNS[t]
        row = next((r for r in tables[t] if r[idf] == rid), None)
        if field == "DELETE_ROW":
            if row:
                tables[t].remove(row); deleted += 1
                log.append(f"- `{rid}` ({t}): row removed. {x['reason']} ({x['evidence_url']})")
            continue
        if field not in cols:
            skipped.append(f"{f.name}: {rid}: unknown field '{field}'"); continue
        if row is None:
            if t not in ("places", "regions", "genres"):
                skipped.append(f"{f.name}: {rid}: no such row in {t}"); continue
            row = {c: "" for c in cols}; row[idf] = rid; tables[t].append(row); added += 1
            log.append(f"- `{rid}` ({t}): new row added by the fact-checker. {x['reason']} ({x['evidence_url']})")
        if row.get(field, "") != val:
            old = row.get(field, "")
            row[field] = val; changed += 1
            if len(old) < 60 and len(val) < 60:
                log.append(f"- `{rid}` ({t}) {field}: \"{old}\" -> \"{val}\". {x['reason']} ({x['evidence_url']})")
            else:
                log.append(f"- `{rid}` ({t}) {field}: text revised. {x['reason']} ({x['evidence_url']})")

tables["places"].sort(key=lambda r: (int(r["year_start"] or 0), r["place_id"]))
for t, rows in tables.items():
    with open(research / f"{t}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=schema.COLUMNS[t], quoting=csv.QUOTE_ALL, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

notes = research / "NOTES.md"
text = notes.read_text(encoding="utf-8") if notes.exists() else ""
marker = "\n## Fact-check corrections\n"
text = text.split(marker)[0].rstrip() + "\n" + marker + "\n" + "\n".join(log) + "\n"
notes.write_text(text, encoding="utf-8", newline="\n")
print(f"fields changed: {changed} | rows deleted: {deleted} | rows added: {added} | skipped: {len(skipped)}")
print("\n".join("  SKIPPED " + s for s in skipped))

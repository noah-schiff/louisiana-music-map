"""Rebuild the research CSVs from the raw batches and every correction file, in the one right order.

    python rebuild_research.py

1. merge.py               places.csv from places_*.csv
2. short_names.py         short genre names for the legend
3. apply_fixes.py         every fact-check correction (fix_*.csv), logged in NOTES.md
4. apply_nature_fixes.py  land-and-sound notes and natural regions
5. palette.py apply       genre colors from palette.json (must run last: fix files also set colors)
6. schema.py              validate the result
"""
import subprocess, sys
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[1]
steps = [[here / "merge.py"], [here / "short_names.py"], [here / "apply_fixes.py"], [here / "apply_nature_fixes.py"],
         [here / "palette.py", "apply"], [root / "scripts" / "schema.py", root / "research"]]
for step in steps:
    r = subprocess.run([sys.executable] + [str(s) for s in step], capture_output=True, text=True, encoding="utf-8")
    tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
    print(f"{Path(step[0]).name:24s} {tail[0][:150]}")
    if r.returncode:
        print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(r.returncode)

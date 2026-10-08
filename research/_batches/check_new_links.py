"""Check only the links that are new since the last commit (fast path for content-only updates).

Run from anywhere:  python check_new_links.py
The full check remains  python scripts\\validate.py --links
"""
import subprocess, sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "scripts"))
import schema, validate

sys.stdout.reconfigure(encoding="utf-8")
urls = validate.all_urls(schema.load_research(root / "research"))
old = ""
for f in ("places", "genres", "regions", "nature", "ecoregions"):
    r = subprocess.run(["git", "-C", str(root), "show", f"HEAD:research/{f}.csv"],
                       capture_output=True, text=True, encoding="utf-8")
    old += r.stdout or ""
new = [u for u in urls if u not in old]
bad = validate.check_links(new)
print(f"new links: {len(new)} | responded OK: {len(new) - len(bad)}")
for u, why in bad:
    print(f"  {why}: {u}")

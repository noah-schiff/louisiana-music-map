"""Independently verify the proposed YouTube listen links (listen_*.csv) and write the ones that
pass to fix_listen.csv, which apply_fixes.py then applies.

A link passes when YouTube's oEmbed endpoint confirms the video exists and is public, the URL is
in canonical watch form, the place exists and still has no listen link, and the label fits.
Prints every link with the title and channel YouTube reports, for a human read-through.
"""
import csv, re, sys
from pathlib import Path
from urllib.parse import quote
import requests

here = Path(__file__).resolve().parent
OEMBED = "https://www.youtube.com/oembed?format=json&url="
# Editorial holds: links that exist but do not meet the brief.
HOLD = {"adai_caddo_robeline": "held: the channel is a month old and could not be confirmed as the "
                               "nation's own; tribal entries take official channels only"}
UA = {"User-Agent": "Mozilla/5.0 (Louisiana Music Map link check)"}

with open(here.parent / "places.csv", newline="", encoding="utf-8-sig") as fh:
    places = {r["place_id"]: r for r in csv.DictReader(fh)}

proposals = {}
for f in sorted(here.glob("listen_*.csv")):
    with open(f, newline="", encoding="utf-8-sig") as fh:
        for x in csv.DictReader(fh):
            proposals.setdefault(x["row_id"].strip(), {})[x["field"].strip()] = x
passed, failed = [], []
for pid, fields in sorted(proposals.items()):
    lab, url = fields.get("listen_1_label"), fields.get("listen_1_url")
    why = HOLD.get(pid)
    if why:
        pass
    elif pid not in places:
        why = "no such place"
    elif not lab or not url:
        why = "label or url line missing"
    else:
        u, label = url["new_value"].strip(), lab["new_value"].strip()
        if not re.fullmatch(r"https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}", u):
            why = f"not a canonical YouTube watch URL: {u}"
        elif len(label) > 150:
            why = f"label is {len(label)} characters"
        elif not re.match(r"^(Listen|Watch): ", label):
            why = "label must start with 'Listen: ' or 'Watch: '"
        else:
            try:
                r = requests.get(OEMBED + quote(u, safe=""), headers=UA, timeout=20)
                if r.status_code != 200:
                    why = f"YouTube oEmbed returned {r.status_code}"
                else:
                    j = r.json()
                    passed.append((pid, label, u, j.get("title", ""), j.get("author_name", ""), lab, url))
            except requests.RequestException as e:
                why = f"request failed ({type(e).__name__})"
    if why:
        failed.append((pid, why))

cols = ["table", "row_id", "field", "new_value", "evidence_url", "reason"]
with open(here / "fix_listen.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_ALL, extrasaction="ignore")
    w.writeheader()
    for pid, label, u, title, channel, lab, url in passed:
        w.writerow({**lab, "new_value": label}); w.writerow({**url, "new_value": u})

out = sys.stdout
out.reconfigure(encoding="utf-8")
for pid, label, u, title, channel, *_ in passed:
    print(f"OK   {pid}\n       name:    {places[pid]['name']}\n       label:   {label}\n       youtube: {title}  //  {channel}\n       {u}")
for pid, why in failed:
    print(f"FAIL {pid}: {why}")
print(f"\nproposed: {len(proposals)} | passed: {len(passed)} | failed: {len(failed)}")

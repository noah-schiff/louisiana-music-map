"""Audit every YouTube listen link beyond "does it exist": length, title, channel and description,
checked against the label shown on the map. Nobody has listened to these; this is the next best thing.

Flags, for a human to look at:
  LONG      a "Listen:" link over 20 minutes (probably a concert, lecture or full album, not a track)
  SHORT     under 45 seconds
  TALK      a "Listen:" label whose title or description reads like an interview, lecture, news or tour
  MISMATCH  no distinctive word from the label appears in the video's title, channel or description
"""
import csv, json, re, sys, time
from pathlib import Path
import requests

here = Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}
STOP = set("listen watch the and of at in on a to for from with youtube topic channel live official video audio "
           "music louisiana new orleans la by is his her their its museum".split())
TALKY = re.compile(r"\b(interview|lecture|talk|presentation|panel|news|report|tour of|documentary|segment|"
                   r"discusses|speaks|conversation|webinar|tribute video)\b", re.I)

with open(here.parent / "places.csv", newline="", encoding="utf-8-sig") as fh:
    places = list(csv.DictReader(fh))
rows, flagged = [], 0
for p in places:
    for n in ("1", "2"):
        url, label = p[f"listen_{n}_url"].strip(), p[f"listen_{n}_label"].strip()
        if "youtube.com/watch" not in url:
            continue
        info = {"secs": None, "title": "", "channel": "", "desc": ""}
        try:
            html = requests.get(url, headers=UA, timeout=25).text
            m = re.search(r'"lengthSeconds":"(\d+)"', html); info["secs"] = int(m.group(1)) if m else None
            m = re.search(r'"shortDescription":"(.*?)","isCrawlable"', html, re.S)
            info["desc"] = json.loads('"' + m.group(1) + '"') if m else ""
            m = re.search(r'"videoDetails":\{"videoId":"[^"]+","title":"(.*?)","lengthSeconds"', html)
            info["title"] = json.loads('"' + m.group(1) + '"') if m else ""
            m = re.search(r'"ownerChannelName":"(.*?)"', html); info["channel"] = json.loads('"' + m.group(1) + '"') if m else ""
        except Exception as e:
            info["desc"] = f"(fetch failed: {type(e).__name__})"
        flags = []
        listen = label.lower().startswith("listen")
        if info["secs"] is None: flags.append("NO-METADATA")
        else:
            if listen and info["secs"] > 20 * 60: flags.append(f"LONG {info['secs'] // 60} min")
            if info["secs"] < 45: flags.append(f"SHORT {info['secs']} s")
        hay = " ".join([info["title"], info["channel"], info["desc"]]).lower()
        if listen and TALKY.search(info["title"] + " " + info["desc"][:300]): flags.append("TALK?")
        words = [w for w in re.findall(r"[a-zà-ÿ']{4,}", label.lower()) if w not in STOP]
        if words and info["title"] and not any(w in hay for w in words): flags.append("MISMATCH")
        flagged += bool(flags)
        rows.append((p["place_id"], label, info, flags))
        time.sleep(0.4)

for pid, label, info, flags in rows:
    if flags:
        mins = f"{info['secs'] // 60}:{info['secs'] % 60:02d}" if info["secs"] is not None else "?"
        print(f"{pid}\n   label:   {label}\n   actual:  {info['title']} // {info['channel']} // {mins}\n   flags:   {', '.join(flags)}"
              f"\n   desc:    {info['desc'][:160].replace(chr(10), ' ')}")
secs = [r[2]["secs"] for r in rows if r[2]["secs"] is not None]
print(f"\nYouTube links audited: {len(rows)} | with metadata: {len(secs)} | flagged: {flagged}")

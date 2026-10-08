"""Give the entries that draw on Warren Kimball's dissertation their page citations.

Checked on 2026-10-08 against the PDF itself (Warren Keith Kimball, "Northern Music Culture in
Antebellum New Orleans," PhD diss., Louisiana State University, 2017), printed page numbers:

  st_charles_theatre                    p. 1 (Caldwell's English St. Charles Theater); p. 4 (Jenny Lind's
                                        thirteen concerts; Mayo's "Swedish Nightingale Mazurka", 1851)
  first_presbyterian_lafayette_square   pp. 28-29 (1 July 1842 public school exhibition; the choir "one of
                                        the best in the city"); p. 32 (singing school advertised 3 Nov 1842,
                                        in the basement); pp. 55-56 (1841 temperance concert); p. 113 (Erben
                                        organ, Daily Picayune 2 Dec 1857)
  clapp_church_sacred_music_society     p. 16 (Mueller: "a society similar to the Handel & Haydn Society");
                                        p. 52 (The Bee, 13 Feb 1836: "A GRAND ORATORIO ... in St. Charles
                                        church", identified as the First Congregational Church); pp. 59-63
                                        (society formed 1842; first public concert 18 May 1842 in "the Rev.
                                        Mr. Clapp's church"; The Creation in full); p. 75 (1850 meeting notice)
  mayo_werlein_5_camp_street            p. 92 (Mayo bought Johns's store "late in 1841"; note 16 cites John
                                        Baron's research on Johns; note 18: Werlein bought Mayo's business
                                        in 1853); p. 94 (move from 89 Chartres Street to 5 Camp Street);
                                        pp. 95-96 (joint imprints with Northern firms); p. 105 (concert
                                        tickets sold at Mayo's); p. 108 (advertisements "almost daily")

Runs after apply_fixes.py (see rebuild_research.py). Re-runnable.
"""
import csv, re, sys
from pathlib import Path

research = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(research.parent / "scripts"))
import schema

CITE = "Warren Keith Kimball, Northern Music Culture in Antebellum New Orleans (PhD diss., Louisiana State University, 2017), "
URL = " <https://repository.lsu.edu/gradschool_dissertations/4119>"
PAGES = {
    ("places", "st_charles_theatre"): "pp. 1, 4",
    ("places", "first_presbyterian_lafayette_square"): "pp. 28-29, 32, 55-56, 113",
    ("places", "clapp_church_sacred_music_society"): "pp. 16, 52-53, 59-63, 75",
    ("places", "mayo_werlein_5_camp_street"): "pp. 92-96, 105, 108",
    ("genres", "classical"): "abstract (p. iv) and chs. 1-4 (pp. 1-114)",
    ("regions", "classical_new_orleans"): "abstract (p. iv) and chs. 1-4 (pp. 1-114)",
}
WRITEUPS = {
    "mayo_werlein_5_camp_street": (
        "Sheet music tied antebellum New Orleans to the Northern trade, and its busiest counter was 5 Camp Street. "
        "William T. Mayo bought Emile Johns's music business and moved it from Chartres Street into the American "
        "sector. Warren Kimball dates the purchase to late 1841, most others to 1846; the 1846 city register "
        "already lists Mayo here. He issued pieces jointly with New York's William Hall & Son and sold "
        "instruments and concert tickets. Philip Werlein bought the business in 1853, by Kimball's account, "
        "issued the first Southern edition of Dixie in 1860, at first without crediting Dan Emmett, and closed "
        "the store in 1862 under Union occupation. The point marks the Canal Street end of Camp Street; the "
        "exact lot is unconfirmed."),
}
changed = 0
for table in ("places", "genres", "regions"):
    path = research / f"{table}.csv"
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    idf = schema.ID_FIELD[table]
    for r in rows:
        pages = PAGES.get((table, r[idf]))
        if pages:
            new = re.sub(re.escape(CITE) + r"[^<|]*?" + re.escape(URL), CITE + pages + URL, r["sources"])
            if CITE + pages + URL not in new:
                sys.exit(f"{table} {r[idf]}: Kimball citation not found in sources")
            changed += new != r["sources"]; r["sources"] = new
        if table == "places" and r[idf] in WRITEUPS:
            changed += r["writeup"] != WRITEUPS[r[idf]]; r["writeup"] = WRITEUPS[r[idf]]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=schema.COLUMNS[table], quoting=csv.QUOTE_ALL, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
print(f"Kimball page citations: {len(PAGES)} entries, {changed} fields changed this run; "
      f"Mayo write-up is {len(WRITEUPS['mayo_werlein_5_camp_street'].split())} words")

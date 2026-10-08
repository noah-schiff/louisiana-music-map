"""Batch K: St. Patrick's Church and its 1843 Erben organ, from Kimball's dissertation (read from the PDF, with pages)."""
import csv, sys
from pathlib import Path

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here.parents[1] / "scripts"))
import schema

row = {
    "place_id": "st_patricks_church_camp_street",
    "name": "St. Patrick's Church",
    "type": "institution",
    "genre_id": "classical",
    "other_genres": "",
    "year_start": "1841",
    "year_end": "",
    "town": "New Orleans",
    "parish": "Orleans",
    "lat": "29.9466",
    "lon": "-90.0697",
    "out_of_state": "",
    "writeup": (
        "St. Patrick's, finished in 1840 for an English-speaking, largely Irish parish, stood apart from "
        "French-speaking Catholic churches. By 1841 it was holding sacred concerts to pay for an organ, "
        "which it ordered from Henry Erben of New York. The instrument arrived by steamboat in March 1843, called "
        "\"the largest probably in America\", and was seized at the port over the church's building debts; the "
        "church appealed to the legislature, and by April it was being installed. With nearly 2,000 pipes in a "
        "Gothic case 37 feet high, it was shown in a public recital. In 1850 Rossini's Stabat Mater was sung "
        "here to benefit the Orphan Boys' Asylum. The church still stands on Camp Street, a block from Lafayette Square."),
    "listen_1_label": "", "listen_1_url": "", "listen_2_label": "", "listen_2_url": "",
    "sources": (
        "Warren Keith Kimball, Northern Music Culture in Antebellum New Orleans (PhD diss., Louisiana State "
        "University, 2017), pp. 55, 111-113 <https://repository.lsu.edu/gradschool_dissertations/4119> | "
        "Old St. Patrick's Church, History <https://oldstpatricks.org/history/> | "
        "Wikipedia, St. Patrick's Church (New Orleans, Louisiana) (National Historic Landmark, 1974) "
        "<https://en.wikipedia.org/wiki/St._Patrick%27s_Church_(New_Orleans,_Louisiana)>"),
}
with open(here / "places_K.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=schema.COLUMNS["places"], quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerow(row)
print("places_K.csv written |", len(row["writeup"].split()), "words")

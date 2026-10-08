"""Batch J: Christ Church on Canal Street, drawn from Kimball's dissertation (read from the PDF, with pages)."""
import csv, sys
from pathlib import Path

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here.parents[1] / "scripts"))
import schema

row = {
    "place_id": "christ_church_canal_street",
    "name": "Christ Church (Canal Street sites)",
    "type": "institution",
    "genre_id": "classical",
    "other_genres": "",
    "year_start": "1842",
    "year_end": "1886",
    "town": "New Orleans",
    "parish": "Orleans",
    "lat": "29.9546",
    "lon": "-90.0708",
    "out_of_state": "",
    "writeup": (
        "Christ Church, the city's first Protestant congregation, formed in 1805 and built on Canal Street. "
        "Early in 1842 it hired Frederick Müller of Boston as organist and choir director at $900 a year; from "
        "this post he also led the Sacred Music Society and taught singing in the public schools. He found a choir of six and set about training more singers. The "
        "congregation then worshipped at Canal and Bourbon streets. By 1847 it had moved a block toward the lake to "
        "a Gothic church at Canal and Dauphine, and Müller directed Neukomm's oratorio David to help pay for a new "
        "organ from George Jardine of New York. The point marks that corner. The congregation moved uptown in 1886."),
    "listen_1_label": "", "listen_1_url": "", "listen_2_label": "", "listen_2_url": "",
    "sources": (
        "Warren Keith Kimball, Northern Music Culture in Antebellum New Orleans (PhD diss., Louisiana State "
        "University, 2017), pp. 32, 34-36, 52, 110, 113 <https://repository.lsu.edu/gradschool_dissertations/4119> | "
        "Christ Church Cathedral, History (the four church buildings and their sites) <https://cccnola.org/?p=560> | "
        "Wikipedia, Christ Church Cathedral (New Orleans) (lakeside corner of Canal and Dauphine) "
        "<https://en.wikipedia.org/wiki/Christ_Church_Cathedral_(New_Orleans)>"),
}
with open(here / "places_J.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=schema.COLUMNS["places"], quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerow(row)
print("places_J.csv written |", len(row["writeup"].split()), "words")

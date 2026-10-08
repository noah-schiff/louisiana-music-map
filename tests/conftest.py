import csv, sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

GOOD = {
    "genres": [
        {"genre_id": "ancient", "name": "Ancient mound-builder cultures", "color": "#8c6d46",
         "year_start": "-1700", "year_end": "1500", "summary": "S.", "sources": "A source <https://example.org/a>"},
        {"genre_id": "jazz", "name": "Jazz", "color": "#3d6fd6",
         "year_start": "1895", "year_end": "", "summary": "S.", "sources": "A book"},
    ],
    "eras": [
        {"era_id": "e1", "name": "Ancient Louisiana", "year_start": "-1700", "year_end": "1500", "summary": "S."},
        {"era_id": "e2", "name": "Later", "year_start": "1500", "year_end": "2026", "summary": "S."},
    ],
    "regions": [
        {"region_id": "r1", "genre_id": "jazz", "label": "New Orleans", "year_start": "1895", "year_end": "",
         "parishes": "Orleans; Jefferson", "note": "", "sources": "A book"},
    ],
    "places": [
        {"place_id": "p1", "name": "Poverty Point", "type": "archaeological site", "genre_id": "ancient",
         "other_genres": "", "year_start": "-1700", "year_end": "-1100", "town": "Epps", "parish": "West Carroll",
         "lat": "32.6367", "lon": "-91.4069", "out_of_state": "", "writeup": "Text.",
         "listen_1_label": "", "listen_1_url": "", "listen_2_label": "", "listen_2_url": "",
         "sources": "Site <https://example.org/pp> | A book"},
    ],
    "cities": [{"name": "New Orleans", "lat": "29.9511", "lon": "-90.0715"}],
}

def write_research(folder, data=None, encoding="utf-8", **overrides):
    """Write a CSV set. overrides: table name -> list of rows (replaces that table)."""
    data = {**(data or GOOD), **overrides}
    folder.mkdir(parents=True, exist_ok=True)
    for name, rows in data.items():
        with open(folder / f"{name}.csv", "w", newline="", encoding=encoding) as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
    return folder

def edited(table, index=0, **changes):
    rows = [dict(r) for r in GOOD[table]]
    rows[index].update(changes)
    return {table: rows}

@pytest.fixture
def research(tmp_path):
    return write_research(tmp_path / "research")

"""Load and validate the research CSVs. Pure Python: no arcpy."""
import csv, re
from pathlib import Path

PLACE_TYPES = {"venue", "studio", "birthplace", "festival", "archaeological site",
               "tribal community", "institution", "landmark"}
COLUMNS = {
    "genres": ["genre_id", "name", "color", "year_start", "year_end", "summary", "sources"],
    "eras": ["era_id", "name", "year_start", "year_end", "summary"],
    "regions": ["region_id", "genre_id", "label", "year_start", "year_end", "parishes", "note", "sources"],
    "places": ["place_id", "name", "type", "genre_id", "other_genres", "year_start", "year_end", "town",
               "parish", "lat", "lon", "out_of_state", "writeup", "listen_1_label", "listen_1_url",
               "listen_2_label", "listen_2_url", "sources"],
    "cities": ["name", "lat", "lon"],
}
# Longest text each geodatabase field holds (see build_gdb.py). Checked here so an overrun is
# reported by name instead of failing inside arcpy.
LIMITS = {"writeup": 3000, "summary": 2000, "sources": 2000, "note": 1000, "parishes": 1500,
          "name": 100, "label": 120, "town": 80, "parish": 60, "other_genres": 200,
          "listen_1_label": 150, "listen_2_label": 150, "listen_1_url": 500, "listen_2_url": 500,
          "place_id": 60, "region_id": 60, "genre_id": 40, "era_id": 40}
OPTIONAL_TABLES = {
    "nature": ["table", "row_id", "nature_note", "sources"],
    "ecoregions": ["eco_id", "name", "description", "sources"],
}
OPTIONAL = {"year_end", "note", "other_genres", "out_of_state", "town", "parish",
            "listen_1_label", "listen_1_url", "listen_2_label", "listen_2_url"}
ID_FIELD = {"genres": "genre_id", "eras": "era_id", "regions": "region_id", "places": "place_id", "cities": "name"}
LA_BOX = (28.5, 33.5, -94.5, -88.5)  # lat min, lat max, lon min, lon max

class SchemaError(Exception):
    def __init__(self, problems):
        self.problems = problems
        super().__init__("\n".join(problems))

def read_rows(path: Path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            header = [h.strip() for h in (reader.fieldnames or [])]
            rows = [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in reader]
    except UnicodeDecodeError:
        raise SchemaError([f"{path.name}: not UTF-8. In Excel use Save As > "
                           f"'CSV UTF-8 (Comma delimited)'."])
    return header, [r for r in rows if any(r.values())]

def parse_sources(text):
    out = []
    for part in filter(None, (p.strip() for p in text.split("|"))):
        m = re.match(r"^(.*?)\s*<(https?://[^>\s]+)>$", part)
        out.append({"label": m.group(1) or m.group(2), "url": m.group(2)} if m else {"label": part, "url": ""})
    return out

def _split(text):
    return [p.strip() for p in text.split(";") if p.strip()]

def load_research(folder) -> dict:
    folder, probs, data = Path(folder), [], {}
    for table, cols in COLUMNS.items():
        path = folder / f"{table}.csv"
        if not path.exists():
            probs.append(f"{table}.csv: file not found"); data[table] = []; continue
        header, rows = read_rows(path)
        missing = [c for c in cols if c not in header]
        if missing:
            probs += [f"{table}.csv: missing column {c}" for c in missing]; data[table] = []; continue
        data[table] = rows
    if probs:
        raise SchemaError(probs)

    def year(row, rid, field, blank_ok):
        v = row[field]
        if v == "" and blank_ok:
            return None
        try:
            y = int(v)
        except ValueError:
            probs.append(f"{rid}: {field} '{v}' is not a whole number"); return None
        if y == 0:
            probs.append(f"{rid}: {field}: year 0 does not exist (use -1 or 1)"); return None
        return y

    genre_ids = {g["genre_id"] for g in data["genres"]}
    for table, rows in data.items():
        idf, seen = ID_FIELD[table], set()
        for row in rows:
            rid = row[idf] or f"{table}.csv row"
            if row[idf] in seen:
                probs.append(f"{table}.csv: duplicate {idf} '{row[idf]}'")
            seen.add(row[idf])
            for c in COLUMNS[table]:
                if c not in OPTIONAL and row[c] == "":
                    probs.append(f"{rid}: {c} is blank")
                if len(row[c]) > LIMITS.get(c, 10**9):
                    probs.append(f"{rid}: {c} is {len(row[c])} characters; the limit is {LIMITS[c]}")
            if "year_start" in row:
                row["year_start"] = year(row, rid, "year_start", False)
                row["year_end"] = year(row, rid, "year_end", table != "eras")
                if None not in (row["year_start"], row["year_end"]) and row["year_start"] > row["year_end"]:
                    probs.append(f"{rid}: year_start is after year_end")
            if "sources" in row:
                row["sources"] = parse_sources(row["sources"])
            if table in ("regions", "places") and row["genre_id"] not in genre_ids:
                probs.append(f"{rid}: unknown genre_id '{row['genre_id']}'")
            if "lat" in row:
                try:
                    row["lat"], row["lon"] = float(row["lat"]), float(row["lon"])
                except ValueError:
                    probs.append(f"{rid}: lat/lon are not numbers"); continue
                row["out_of_state"] = row.get("out_of_state", "").lower() in ("yes", "y", "true", "1")
                a, b, c, d = LA_BOX
                if not row["out_of_state"] and not (a <= row["lat"] <= b and c <= row["lon"] <= d):
                    probs.append(f"{rid}: lat/lon outside Louisiana (set out_of_state to yes if intended)")
    for g in data["genres"]:
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", g["color"]):
            probs.append(f"{g['genre_id']}: color '{g['color']}' must look like #a1b2c3")
    for r in data["regions"]:
        r["parishes"] = _split(r["parishes"])
    for p in data["places"]:
        if p["type"] not in PLACE_TYPES:
            probs.append(f"{p['place_id']}: type '{p['type']}' is not one of {sorted(PLACE_TYPES)}")
        p["other_genres"] = _split(p["other_genres"])
        for g in p["other_genres"]:
            if g not in genre_ids:
                probs.append(f"{p['place_id']}: unknown genre_id '{g}'")
        p["listen"] = []
        for n in ("1", "2"):
            label, url = p[f"listen_{n}_label"], p[f"listen_{n}_url"]
            if bool(label) != bool(url):
                probs.append(f"{p['place_id']}: listen_{n} needs both label and url")
            elif url and not re.match(r"^https?://", url):
                probs.append(f"{p['place_id']}: listen_{n}_url must start with http")
            elif url:
                p["listen"].append({"label": label, "url": url})
    # Optional landscape content: notes tying an entry to its environment, and the natural regions.
    for table, cols in OPTIONAL_TABLES.items():
        data[table] = []
        path = folder / f"{table}.csv"
        if not path.exists():
            continue
        header, rows = read_rows(path)
        missing = [c for c in cols if c not in header]
        if missing:
            probs += [f"{table}.csv: missing column {c}" for c in missing]; continue
        for row in rows:
            row["sources"] = parse_sources(row["sources"])
        data[table] = rows
    seen_notes = set()
    for e in data["ecoregions"]:
        probs += [f"ecoregions.csv: {e['eco_id'] or 'row'}: {c} is blank"
                  for c in ("eco_id", "name", "description") if not e[c]]
    for n in data["nature"]:
        key = (n["table"], n["row_id"])
        if key in seen_notes:
            probs.append(f"nature.csv: duplicate note for {n['table']} '{n['row_id']}'")
        seen_notes.add(key)
        if n["table"] not in ("genres", "regions", "places"):
            probs.append(f"nature.csv: table '{n['table']}' must be genres, regions or places"); continue
        if n["row_id"] not in {r[ID_FIELD[n["table"]]] for r in data[n["table"]]}:
            probs.append(f"nature.csv: no {n['table']} row '{n['row_id']}'")
        if not n["nature_note"]:
            probs.append(f"nature.csv: {n['row_id']}: nature_note is blank")

    eras = data["eras"]
    if any(a["year_end"] != b["year_start"] for a, b in zip(eras, eras[1:])):
        probs.append("eras.csv: eras must be contiguous and in order (each year_end equals the next year_start)")
    if probs:
        raise SchemaError(probs)
    return data

if __name__ == "__main__":
    import sys
    try:
        d = load_research(sys.argv[1])
    except SchemaError as e:
        print(f"{len(e.problems)} problem(s):"); print("\n".join("  " + p for p in e.problems)); sys.exit(1)
    print({k: len(v) for k, v in d.items()})

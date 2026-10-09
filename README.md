# Louisiana Music Through Time

An interactive map of Louisiana's musical history, from about 1700 BCE to today. Drag the
timeline to watch each tradition's heartland and landmark places appear across the state:
20 genres, 35 heartland regions and 133 places, each with its sources.

**Live map: https://noah-schiff.github.io/louisiana-music-map/**

## Opening and sharing the map

- **`web\index.html`** is the whole map in one file. Double-click it to open it in a browser.
  It works offline on its built-in basemap; the Streets and Satellite buttons need internet.
- To share it, send that one file, or put it on any static web host (GitHub Pages, Netlify,
  a university web folder).
- **`web\artifact.html`** is the same map packaged for publishing as a Claude artifact. Online
  basemaps are not available there, so the buttons hide themselves.

## What is in this folder

| Path | What it is |
|---|---|
| `research\` | The content. `genres.csv`, `eras.csv`, `regions.csv`, `places.csv`, `cities.csv`, plus `NOTES.md` (judgment calls and fact-check corrections) |
| `research\_batches\` | Raw research batches and fact-check corrections, kept as a record |
| `data_raw\` | Downloaded base data (Census parishes, Natural Earth rivers and lakes). Never edited |
| `LouisianaMusic.gdb` | Geodatabase built from the research files. NAD 1983 UTM Zone 15N |
| `LouisianaMusic.aprx` | ArcGIS Pro project with every layer, colored by genre |
| `scripts\` | The build pipeline |
| `web\src\` | The page's source: layout, styles and behaviour |
| `web\vendor\` | Leaflet 1.9.4 |
| `tests\` | Automated tests |
| `docs\` | Design spec and implementation plan |

## Changing the content

The CSV files in `research\` are the single source of truth. Everything else is rebuilt from them.

1. Open the CSV in Excel and edit it. To add a place, add a row to `places.csv`.
2. Save with **Save As > CSV UTF-8 (Comma delimited)**.
3. Rebuild (below). The first step checks your edits and tells you exactly what is wrong if
   something is: a misspelled parish, an unknown genre id, a year that is not a whole number.

Field notes:

- Years are whole numbers. BCE years are negative (1700 BCE is `-1700`). Leave `year_end` blank
  for anything still active.
- `genre_id` must be one of the ids in `genres.csv`. `other_genres` is a semicolon-separated list.
- `type` is one of: venue, studio, birthplace, festival, archaeological site, tribal community,
  institution, landmark.
- `sources` looks like `Label <https://url> | Second label <https://url>`.
- In `regions.csv`, `parishes` is a semicolon-separated list of parish names without "Parish".

## How the research files are assembled

The CSVs in `research\` are themselves built from the raw research and every fact-check
correction, kept in `research\_batches\`:

- `places_A.csv` … `places_I.csv` are the places as first researched.
- `fix_*.csv` are corrections from independent fact-checkers, one line per field changed, each
  with its evidence. `fix_zz_editorial.csv` holds a few deliberate editorial overrides.
- `palette.json` holds the genre colors.

One command reapplies all of it in the right order and validates the result:

```powershell
& $PY research\_batches\rebuild_research.py
```

Editing `research\places.csv` directly works, but that command will overwrite it. To make a
change that lasts, add a line to a `fix_*.csv` file (or a row to a `places_*.csv` batch) and run
the command. Every applied correction is logged in `research\NOTES.md`.

Useful checks in the same folder: `verify_new_places.py` (mechanical checks on a new batch),
`check_new_links.py` (only links added since the last commit), `audit_listen.py` (length, title
and description of every YouTube link) and `palette.py measure` (how distinguishable the genre
colors are, including for color-blind viewers).

## Colors and marker shapes

Twenty genres are more than color can separate, so each family of genres also has a marker shape.
The families are listed twice and must match: `SHAPES` in `web\src\app.js` and `FAMILIES` in
`research\_batches\palette.py`. When adding a genre, add it to both, then run
`& $PY research\_batches\palette.py spread 12` to choose colors that stay distinct within each
shape, and rebuild.

## Rebuilding

Run these from this folder in PowerShell. `$PY` is ArcGIS Pro's Python.

```powershell
$PY = "C:\GIS\bin\Python\envs\arcgispro-py3\python.exe"
& $PY scripts\build_gdb.py          # research CSVs + base data -> LouisianaMusic.gdb
& $PY scripts\validate.py --links   # every point inside Louisiana, counts agree, links respond
& $PY scripts\export_web.py         # geodatabase -> web\index.html and web\artifact.html
& $PY scripts\make_aprx.py          # refresh the ArcGIS Pro project (close Pro first)
& $PY -m pytest tests -q            # the test suite (takes a few minutes)
```

The timeline logic has its own browser tests in `web\src\tests.html`; serve the `web` folder
(`& $PY -m http.server 8765 --directory web`) and open `http://localhost:8765/src/tests.html`.

## Base data (not in this repository)

`data_raw\` and the built geodatabase are left out of version control. To rebuild from scratch,
download and unzip each of these into `data_raw\<name>\`:

| Folder name | Source |
|---|---|
| `cb_2023_us_county_500k` | https://www2.census.gov/geo/tiger/GENZ2023/shp/cb_2023_us_county_500k.zip |
| `ne_10m_rivers_lake_centerlines` | https://naciscdn.org/naturalearth/10m/physical/ne_10m_rivers_lake_centerlines.zip |
| `ne_10m_rivers_north_america` | https://naciscdn.org/naturalearth/10m/physical/ne_10m_rivers_north_america.zip |
| `ne_10m_lakes` | https://naciscdn.org/naturalearth/10m/physical/ne_10m_lakes.zip |
| `la_eco_l3` | https://dmap-prod-oms-edc.s3.us-east-1.amazonaws.com/ORD/Ecoregions/la/la_eco_l3.zip |

`make_aprx.py` also needs any blank ArcGIS Pro project to copy from; set `SEED` at the top of the
script to one of yours.

## About the content

- Heartland regions are approximations made from groups of whole parishes. They show where a
  tradition was centered, not where it stopped.
- For the ancient period there is little direct evidence of music. Those entries state what
  archaeology and the tribal nations' own accounts support, and mark inference as inference.
- Every entry cites its sources, shown in the map's detail panel.
- Recordings with explicit lyrics say so in their link label
  (`research/_batches/mark_explicit.py`).

## If an organization wants to use this

This is a personal project by a student. It is not an official guide, and nobody listed on it has
endorsed it. Someone weighing it for public or promotional use should know:

- **How the research was done.** The entries were gathered with an AI research assistant (Claude)
  working from a written brief (`research/RESEARCH_BRIEF.md`), then checked by a separate
  fact-checking pass against each cited source (`research/FACTCHECK_BRIEF.md`). Every correction
  is a line in a `research/_batches/fix_*.csv` file giving the old claim, the new value, the
  evidence and the reason. No subject expert has reviewed the whole map.
- **Status of venues.** Each place shown as active was checked for whether it still operates
  (`research/STATUS_BRIEF.md`; the record is `research/_batches/fix_status_*.txt`). That check has
  a date, shown in the About panel, and goes stale. The map tells visitors to confirm before going.
- **Private and vanished places.** Birthplaces, markers and former venues are often private
  property or empty lots. Each place's panel says what a visitor should expect.
- **Tribal nations.** Entries on Native nations are written from the nations' own published
  accounts. No nation has reviewed them. An organization publishing this should ask them first.
- **Basemaps.** The Streets and Satellite views use free OpenStreetMap, CARTO and Esri services,
  which suits a personal project. An organization should supply its own licensed basemap; the
  Designed and Landscape views are drawn from public-domain data and need none.
- **Listen links** go to YouTube and other outside sites. They are checked when the map is built
  (`scripts/validate.py`), and they can disappear.
- **Accessibility.** Audited against WCAG 2.1 AA with scripted checks: text and marker contrast in
  both themes, keyboard operation, target sizes, landmarks, and a Places list that gives everything
  on the map as text. It has not been tested with users of assistive technology.
- **Coverage is uneven.** About 135 places cannot represent the state; many parishes have none.

## Credits

Parish boundaries: U.S. Census Bureau cartographic boundary files (2023). Rivers and lakes:
Natural Earth. Online basemaps: OpenStreetMap contributors, CARTO, Esri. Mapping library: Leaflet.

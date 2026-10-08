# Brief: more places for the Louisiana Music History Map

Live map: https://noahmschiff.com/louisiana-music-map/ . It has 74 places. The owner wants more.

Read `RESEARCH_BRIEF.md` (rules for facts, sources, prose and CSV writing) and `LISTEN_BRIEF.md`
(what counts as a good listen link, and the YouTube oEmbed verification step) in this folder first.
Both bind this task. Python is `C:\GIS\bin\Python\envs\arcgispro-py3\python.exe`.

Then read `places.csv`, `genres.csv` and `regions.csv` here with the csv module so you know what
the map already has. Do not edit them. Do not add a place that is already on the map under any
name, and do not add a second point for the same building.

## What to add

10 to 12 new places in the area and themes given in your task. Each must be:

- A specific, mappable location: a building, an address, a marked site, a festival ground.
- Musically significant for a reason a source states, not just "a musician lived nearby".
- Verified to the research brief's standard: every name, date and location confirmed in a source
  you opened this session; coordinates to four decimals for the actual site, checked against a
  second independent reference (a geocoder, OpenStreetMap, a National Register listing, a marker
  database).

Prefer places that fill a gap: a genre with few places, a parish with none, a decade that is thin.

## Columns (exact header, all 18)

`place_id,name,type,genre_id,other_genres,year_start,year_end,town,parish,lat,lon,out_of_state,writeup,listen_1_label,listen_1_url,listen_2_label,listen_2_url,sources`

- `place_id`: unique lowercase slug with underscores, not already used in `places.csv`.
- `type`: one of venue, studio, birthplace, festival, archaeological site, tribal community,
  institution, landmark.
- `genre_id`: one of the 19 ids in `genres.csv`. `other_genres`: semicolon-separated ids or blank.
- `year_start`: the year the place became significant FOR THAT MUSIC (not the year an older
  building was put up, if the music came later). It must not be earlier than the `year_start` of
  its `genre_id` in `genres.csv`; if the place is older than the genre, either choose the genre
  that fits its early history or use the year the music began there, and say so in the write-up.
- `year_end`: blank if still active or still standing as a landmark; otherwise the year it closed
  or was demolished.
- `town`, `parish` (parish name without the word "Parish"), `lat`, `lon` (inside Louisiana;
  longitude negative), `out_of_state` blank.
- `writeup`: 60 to 120 words, original prose, plain and specific.
- `listen_1_label`, `listen_1_url`: one link per the listen brief (official channels first;
  YouTube allowed; verified with oEmbed if YouTube). Label form
  `Listen: <artist>, "<title>" (<channel>, YouTube)` or `Watch: <what it is> (<channel>, YouTube)`
  or, for a non-YouTube page, `Listen: <what it is> (<host>)`. Leave both blank if nothing fits.
  Leave `listen_2_*` blank.
- `sources`: `Label <https://url> | Label <https://url>`, at least one that is not Wikipedia.

Write the file with `csv.DictWriter` (`quoting=csv.QUOTE_ALL`, UTF-8, `newline=""`) to the path in
your task, then read it back and confirm: every row has all 18 columns; ids are unique and not in
`places.csv`; `type` and genre ids are valid; `year_start` is not before the genre's start;
coordinates fall between 28.9 and 33.1 north and -94.1 and -88.8 west; write-ups are 60 to 120
words.

## Final report (short)

Rows written; for each, one line with the place, years, parish and genre; anything you looked at
and left out, with the reason; source disagreements and what you chose; coordinates that rest on
a single reference.

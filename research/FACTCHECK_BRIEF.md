# Fact-check brief: Louisiana Music History Map

You are an independent fact-checker. Another researcher wrote the rows you are about to check; you
did not. Your job is to try to prove each row wrong. Assume nothing is right until you have
confirmed it in a source you opened in this session. The content will be shown publicly with its
sources.

Read `RESEARCH_BRIEF.md` in this folder first: its rules bind the rows you are checking and any
replacement text you propose.

## What to check, for every row you are assigned

1. **Name** spelled correctly.
2. **Dates**: `year_start` and `year_end` supported by a reliable source. Where sources disagree,
   the chosen year should be defensible and the prose should not claim more precision than exists.
3. **Location** (place rows): town and parish correct; `lat`/`lon` on the actual site, confirmed
   against a reference independent of the one the original researcher is likely to have used
   (for example a geocoder, OpenStreetMap, a National Register listing, a marker database). Flag
   anything more than about 300 m off for a building, or 1 km for a district or large site.
4. **Every factual claim in the write-up or summary** supported by a source. Flag anything that is
   unsupported, overstated, or presented as fact when it is inference. Be especially strict with
   the ancient and Native rows.
5. **Every URL** in `sources` and the listen fields loads and is about the thing it is cited for.
   Some sites (Smithsonian Folkways, hmdb.org, loc.gov) block simple fetch tools; try the browser
   tools before calling a link broken.
6. **Parish lists** (region rows): every parish belongs; no obviously central parish is missing,
   judged against sources, not against your own impression.

Do not rewrite rows for style. Do not edit the research CSV files. Only report corrections.

## Listen links (place rows only)

Where a place row has blank listen fields, try to find ONE legitimate, stable listen link that is
clearly relevant to that place: a Library of Congress item, a Smithsonian Folkways album or track
page, or an official artist/label/tribe/archive/museum/festival page or channel with audio or
video. Confirm it loads. If you cannot find one that meets the rule, leave it blank; do not link
unofficial uploads. Report these as corrections to `listen_1_label` and `listen_1_url`.

## Output

Write a CSV (Python `csv.DictWriter`, `quoting=csv.QUOTE_ALL`, UTF-8, `newline=""`; Python is at
`C:\GIS\bin\Python\envs\arcgispro-py3\python.exe`) to the path given in your task, with exactly
these columns:

`table,row_id,field,new_value,evidence_url,reason`

- `table`: `places`, `genres`, `regions` or `eras`.
- `row_id`: the row's `place_id`, `genre_id`, `region_id` or `era_id`.
- `field`: the column to change. Use the special value `DELETE_ROW` when a row cannot be
  confirmed and should be removed (leave `new_value` blank).
- `new_value`: the complete replacement value for that field (for `writeup`, `summary` and
  `sources`, the whole new text, following the research brief's rules and length limits).
- `evidence_url`: a URL you opened that supports the change.
- `reason`: one sentence.

One line per field changed. Rows that check out get no line. Read the file back to confirm it
parses.

## Final report (short)

How many rows you checked, how many were fully confirmed, how many corrections of each kind, any
row you recommend deleting, and anything you could not verify either way.

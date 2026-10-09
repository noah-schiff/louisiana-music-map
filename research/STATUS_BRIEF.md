# Status-check brief: is each place still what the map says it is?

The map (https://noahmschiff.com/louisiana-music-map/) is about to be shown to the Louisiana Office
of Tourism. A tourism office will notice at once if the map implies a visitor can go somewhere that
has closed, moved, burned, or is not open to the public. Each place on your list is currently shown
as active today (its `year_end` is blank). Your job is to find out, for each one, its real status
as of 2026.

Read `RESEARCH_BRIEF.md` in this folder first; its rules on sources bind you (open the page, cite
only URLs you opened, no guessing). Python is `C:\GIS\bin\Python\envs\arcgispro-py3\python.exe`.
Read `places.csv` here with the csv module to see each row. Do not edit it.

## For each place, establish

1. Does it still exist and operate in the role the write-up describes (venue still presenting
   music; festival still held, and where; museum, church or school still open; studio still working)?
   Use the most recent evidence you can find: the place's own site or social page, a 2025-2026 news
   story, a current events listing, an official tourism or government listing. Note the date of the
   evidence.
2. If it has closed, moved, burned, been sold, or changed its name or use: the year, with a source.
3. Whether the public can actually visit (open to the public; by appointment; private; a marker or
   an empty site).

## What to write

A CSV (Python `csv.DictWriter`, `quoting=csv.QUOTE_ALL`, UTF-8, `newline=""`) at the path in your
task, with exactly these columns:

`table,row_id,field,new_value,evidence_url,reason`

`table` is always `places`. Write lines ONLY where the map is wrong or misleading:

- `year_end`: the year it ended, if it has ended (the map then shows it as historic).
- `writeup`: the complete replacement write-up (60 to 120 words, original prose) when a sentence
  says or implies something that is no longer true (for example "still hosts", "today", "every
  Saturday"), or when a closure, move or change of use should be stated. Change as little as
  possible; keep the history.
- `name`: only if the place's name has changed and the map uses a wrong one.
- `sources`: the complete replacement value only if you add the page that documents a change.

Do not write a line for a place that checks out. Do not change coordinates, genres or listen links.

Also write, next to it, a plain text file with the same name but ending `.txt`: one line per place
on your list, in the form

`place_id | STATUS | as of <date of evidence> | <how the public can visit, in a few words> | <evidence URL>`

where STATUS is one of: OPEN (operating as described), CHANGED (still there but the write-up
needed a fix), CLOSED (ended; year given), UNCONFIRMED (no evidence from 2024 or later either way).
This file is the record for every place, including those with no corrections.

## Final report (short)

Counts of OPEN / CHANGED / CLOSED / UNCONFIRMED, each correction in one line, and the places you
could not confirm.

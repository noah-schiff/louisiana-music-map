# Listen-link brief: Louisiana Music History Map

The map (https://noah-schiff.github.io/louisiana-music-map/) shows about 74 places in Louisiana's
musical history. Each place's panel can carry a "Listen" link. 52 places have none. The owner has
now approved YouTube as a source. Your job is to find ONE good YouTube link for each place on your
list.

## Your list

Run this (Python is `C:\GIS\bin\Python\envs\arcgispro-py3\python.exe`), replacing OFFSET with the
number given in your task:

```python
import csv
rows = list(csv.DictReader(open(r"research\places.csv", encoding="utf-8-sig", newline="")))  # run from the project folder
blank = sorted((r for r in rows if not r["listen_1_url"].strip()), key=lambda r: r["place_id"])
mine = blank[OFFSET::3]
for r in mine:
    print(r["place_id"], "|", r["name"], "|", r["type"], "|", r["genre_id"], "|", r["year_start"], "-", r["year_end"])
    print("   ", r["writeup"])
```

Read each write-up: it tells you which artists, recordings or events the place is known for, and
the link must match that. Do not edit `places.csv`.

## What counts as a good link

The link should let someone hear the music this place is known for, as specifically as possible:
a recording made at that studio, a performance at that venue or festival, the artist born there
playing the style the write-up describes, a tradition bearer from that community.

Channel preference, best first:
1. An official channel: the artist's own, the record label's, Smithsonian Folkways, Library of
   Congress, the American Folklife Center, the Alan Lomax Archive / Association for Cultural Equity,
   the festival's or venue's own channel, a museum, a university archive, public television or
   radio (PBS, LPB Louisiana Public Broadcasting, WWOZ, NPR, KRVS), the National Park Service, or
   the tribal nation's own channel.
2. A YouTube auto-generated "Topic" channel track (description begins "Provided to YouTube by ..."),
   which is label-licensed.
3. Only if neither exists: a long-standing upload from a reputable archive-style channel. Avoid
   random personal re-uploads of commercial recordings, lyric videos, playlists, "full album"
   uploads, compilations with unclear rights, reaction or commentary videos, and anything likely to
   be taken down.

Special cases:
- **Tribal communities and Native traditions:** use only the nation's own channel, a public
  broadcaster, a museum, the Library of Congress, or another institution working with the nation.
  Never a third party's recording of ceremony. If nothing appropriate exists, leave it blank.
- **Archaeological sites, churches, museums and other places with no recording of their own:** an
  official video about the place (park service, state museum, public television) is acceptable.
  Label it "Watch:" instead of "Listen:".
- If you cannot find a link that is clearly relevant and from an acceptable channel, leave the
  place out. A blank is better than a weak or wrong link.

## Verify every link

For each candidate, fetch `https://www.youtube.com/oembed?url=<VIDEO_URL>&format=json` (plain
HTTP GET; it returns JSON with `title` and `author_name` for a public, embeddable video and an
error otherwise). Record the title and channel it returns. Do not propose a link whose oEmbed check
fails or whose title or channel does not match what you expected. Use the canonical form
`https://www.youtube.com/watch?v=VIDEOID` with no extra parameters. Never guess or construct a
video ID.

## Output

Write a CSV with Python's `csv` module (`csv.DictWriter`, `quoting=csv.QUOTE_ALL`, UTF-8,
`newline=""`) to the path given in your task, with exactly these columns:

`table,row_id,field,new_value,evidence_url,reason`

Two lines per place:
- `table` = `places`, `row_id` = the place_id, `field` = `listen_1_label`, `new_value` = the label
  shown on the map, at most 110 characters, in the form
  `Listen: <artist>, "<title>" (<channel>, YouTube)` or
  `Watch: <what it is> (<channel>, YouTube)`.
- `table` = `places`, `row_id` = the place_id, `field` = `listen_1_url`, `new_value` = the URL.

For both lines, `evidence_url` = the video URL and `reason` = one sentence saying why this video
fits this place, plus the oEmbed title and channel in the form `[oEmbed: <title> / <channel>]`.

Read the file back to confirm it parses.

## Final report (short)

How many places were on your list, how many got a link, which were left blank and why, and any
link you are less than sure about.

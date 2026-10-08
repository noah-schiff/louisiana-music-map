# Research brief: Louisiana Music History Map

You are researching content for an interactive map of Louisiana's musical history, from about
1700 BCE to 2026. A viewer drags a timeline and sees which music belonged to which part of the
state. Your rows are shown to the public with their sources, so accuracy matters more than volume.

## Rules (all binding)

1. **Verify on the web. Do not write from memory.** Every fact (names, dates, locations) must be
   confirmed in a source you actually opened in this session. Every URL you cite must be one you
   fetched and saw load with relevant content. Never guess or construct a URL.
2. **Preferred sources:** 64 Parishes (64parishes.org), Louisiana Folklife Program
   (louisianafolklife.org), Library of Congress, Smithsonian Folkways, National Park Service,
   Louisiana Division of Archaeology, tribal nations' own websites, university presses,
   peer-reviewed work, official museum/venue/festival sites. Wikipedia may help you find leads and
   coordinates but should not be the only source for a row.
3. **Ancient and early Native material:** state only what archaeology and the nations' own accounts
   support. Mark inference as inference in the prose ("Archaeologists infer..."). If there is no
   real evidence connecting a site or people to music, sound-making, dance or ceremony, leave it
   out. Fewer rows are better than speculative ones. Describe living tribal traditions in the
   present tense, using the nation's own framing where available.
4. **Write-ups are original prose**, 60 to 120 words, plain and specific, written for a curious
   general reader. No copied sentences. Say why the place matters to the music.
5. **Listen links** only to: Library of Congress, Smithsonian Folkways, or an official
   artist/label/tribe/archive/museum channel or page. Leave blank if you cannot find a legitimate,
   stable one. Do not link to unofficial uploads.
6. **Years are whole numbers.** BCE years are negative (1700 BCE is -1700). There is no year 0.
   Leave `year_end` blank if the thing is still active, still standing as a landmark, or a living
   tradition.
7. If you cannot confirm something, leave the row out and list it in your final report.

## Genre ids (use exactly these)

ancient (ancient mound-builder cultures), native (Native nations' music), colonial (colonial
French and Spanish music), congo (African and Caribbean traditions, Congo Square), creole (Creole
music and la-la), cajun, zydeco, jazz, brass (brass band and second line), mardigras_indian
(Mardi Gras Indian / Black Masking Indian music), blues (including swamp blues), gospel (gospel
and spirituals), country (country and the Louisiana Hayride), rnb (rhythm and blues and early rock
and roll), swamp_pop, funk, bounce, hiphop (Louisiana hip-hop).

## Eras

ancient -1700 to 1500; nations 1500 to 1700; colonial 1700 to 1803; c19 1803 to 1890;
jazzbirth 1890 to 1920; recording 1920 to 1945; postwar 1945 to 1970; modern 1970 to 2026.

## CSV format

UTF-8, comma-separated, a header row, every text field wrapped in double quotes, embedded double
quotes doubled (""). Write the file with Python's `csv` module (`csv.DictWriter`,
`quoting=csv.QUOTE_ALL`, `encoding="utf-8"`, `newline=""`) so quoting is correct; do not hand-type
the CSV. Python is at `C:\GIS\bin\Python\envs\arcgispro-py3\python.exe`. After writing, read the
file back with `csv.DictReader` and confirm the row count and that every row has every column.

`sources` format: `Label <https://url> | Second label <https://url>`. A print source with no URL
is just its citation as the label. Labels must not contain `|`, `<` or `>`.

## Final report (keep it short)

Rows written, the output path, anything you could not confirm and left out, and any place where
sources disagree (with what you chose and why).

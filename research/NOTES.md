# Statewide framework: research notes

Covers `eras.csv` (8 rows), `genres.csv` (18 rows) and `regions.csv` (30 rows). Every URL cited
in those files was opened during research. This file records what is solid, what is disputed,
what is unknown, and where a date or boundary is a judgment call.

## Ancient period (1700 BCE to 1500 CE)

**Established**
- Poverty Point (West Carroll Parish) was built about 1700 to 1100 BCE: five mounds, six
  C-shaped ridges and a 43-acre plaza that was artificially filled and levelled. UNESCO describes
  it as "created and used for residential and ceremonial purposes" (3700 to 3100 BP).
- Marksville culture, 1 to 400 CE; Troyville, 400 to 700 CE; Coles Creek, 700 to 1200 CE;
  Plaquemine, 1200 to 1700 CE; Caddo culture, 900 to 1700 CE (64 Parishes dates).
- At the Crooks site (LaSalle Parish), Marksville-era burials included "clusters of pebbles that
  were probably the inorganic remains of rattles" (64 Parishes, Marksville Culture).
- An effigy pipe from the Gahagan site (Red River Parish) "depicts a frog holding a ceremonial
  rattle" (64 Parishes, Caddo Culture).
- Troyville sites have large pits that appear to have been used to cook for feasts, and platform
  mounds that "may have been used as stages for public ceremonies".

**Inference, and marked as such in the prose**
- That any of these places had music. Ceremony and feasting are inferred from architecture and
  food remains; rattles are inferred from pebble clusters and one carved image. Nothing tells us
  what anything sounded like.
- The purpose of Poverty Point. Village, trade fair and pilgrimage center are all live
  hypotheses. Large post rings found under the plaza are of unknown significance.

**Unknown**
- No musical instrument is reported from Poverty Point in the sources consulted.
- No source consulted reports a flute, whistle, drum or panpipe from a Louisiana site of this
  period, so none is claimed.
- Who the builders' descendants are. The name of the people who built Poverty Point is unknown.

**Left out on purpose**
- Coles Creek and Plaquemine cultures have no region row. They built ceremonial mound centers
  across much of the state, but I found no source tying a specific Louisiana site of theirs to
  sound-making, and a region covering "most of Louisiana" would not be conservative.
- Tortoise-shell rattles are reported for the Meso-Indian period (5000 to 2000 BCE) in
  *Louisiana Prehistory*, which is before the map's start date, and with no site named.
- Watson Brake and the LSU mounds predate 1700 BCE.
- The gaps in the ancient regions (1100 BCE to 1 CE, and 700 to 900 CE) are real gaps in the
  evidence I could tie to sound or ceremony, not claims that nobody lived here.

## Native nations (1500 onward)

**Established**
- Caddo: homeland on the Red River in northwest Louisiana; ceded lands east of the Sabine in
  1835; settled in present Oklahoma in 1859. The Turkey Dance (more than fifty songs, one
  recalling the creation of Caddo Lake) and the Drum Dance are living traditions.
- Chitimacha: the tribe states it has "always been here", with a homeland covering the
  Atchafalaya Basin, west toward Lafayette, south to the Gulf and east to the New Orleans area.
  Frances Densmore collected Chitimacha songs; no sacred songs were included.
- Tunica-Biloxi: at Marksville since about 1779 (tribe) or the 1770s; federally recognized 1981.
  Songs in Tunica and Biloxi were recorded from elders in the 1960s to 1980s and are sung again.
- Coushatta: permanent community at Bayou Blue near Elton from the 1880s. Songs and dances were
  set aside in the early twentieth century and revived from the 1970s.
- Jena Band of Choctaw: documented at Jena in the 1880 census; federally recognized 1995.
- Houma: near present West Feliciana Parish in 1682; moved downriver after 1706; gradually moved
  to the Terrebonne and Lafourche bayous in the nineteenth century.

**Contested or uncertain**
- The year 1500 is a convention marking the approach of the documented period. It is not a start
  date for any tradition. The genre summary says so.
- Chitimacha reservation date: the tribe's site gives 1916; the Louisiana Folklife Program
  gives 1919. I used 1916, the tribe's own date, as the end of the `native_chitimacha` region.
- Tunica-Biloxi arrival at Marksville: "approximately 1779" or "the 1770s".
- H.F. Gregory's essay says the Caddo "seem to have disappeared from Louisiana". The Caddo Nation
  is a living sovereign nation in Oklahoma, and I followed that framing.

**Unknown**
- What any nation's music sounded like before the twentieth-century recordings. The 1500 to 1700
  era summary says this directly.

**Boundary judgment calls**
- `native_chitimacha` uses five parishes (St. Mary, St. Martin, Iberia, Iberville, Assumption),
  a deliberately small subset of the homeland the tribe describes. Widening it east to the
  New Orleans area would be defensible on the tribe's account.
- `native_today` starts in 1880 because that is when the last of the five communities
  (Coushatta, Jena Choctaw) is documented in place. The Tunica-Biloxi and Chitimacha were on
  their land earlier. It lists LaSalle only for the Jena Band, though Jena was in Catahoula
  Parish in 1880 and the tribe also has members in Catahoula and Grant.
- No region is drawn for the Houma and Tunica homelands on the Mississippi before 1800, or for
  the state-recognized Choctaw-Apache, Clifton Choctaw and other communities. Three rows per
  genre was the limit, and I had music evidence for the nations chosen.

## Start years that are judgment calls

| Genre | Year used | Why, and the alternative |
|---|---|---|
| colonial | 1725 | First dated musical event (parish musician hired, Capuchin school). Music surely arrived with the French earlier; nothing dated was found. |
| congo | 1724 | Code Noir makes Sunday a non-work day. The first enslaved Africans arrived in 1719 (not verified in a fetched source). The 1817 ordinance is when Congo Square itself becomes the site. |
| congo (end) | 1856 | Sources disagree: dances diminished through the 1840s (Johnson); shut down 1835, resumed, shut down 1851, drums and horns banned 1856 (New Orleans Historical); "1817 to 1856" (Raeburn). I used 1856. The tradition's influence continues, and drumming at the square resumed in modern times. |
| creole | 1867 | First publication of Louisiana Creole songs in *Slave Songs of the United States*. The songs are older. La-la house dances are dated only to the "early twentieth century" (64 Parishes) or "the 1920s" (Handbook of Texas). The one region row starts in 1900, so the map shows no Creole region from 1867 to 1900. |
| cajun | 1765 | Arrival of the Broussard party in the Attakapas. Twenty Acadians arrived in 1764. Ancelet dates recognizable "Cajun music" to the early twentieth century, which is why the prairie region starts in 1900; that 1900 split is a round number. |
| zydeco | 1949 | Clarence Garlow's "Bon Ton Roula". Lightnin' Hopkins's "Zolo Go" is about 1947 but is a Houston record. The word's spelling was fixed in the early 1960s. |
| brass | 1880 | NPS dates the Excelsior and Onward to the 1880s; Sakakeeny says Black brass bands appeared "in the decades after Emancipation in 1865". Brass bands in general are older. |
| mardigras_indian | 1880 | Montana family account of the Creole Wild West. 64 Parishes says origins are "not known and remain hotly contested"; one theory ties them to Buffalo Bill's 1884 to 1885 visit. |
| blues | 1890 | Sandmel: "late nineteenth century", with guitars widely available from the mid-1890s. Approximate. |
| gospel | 1850 | Approximate. Sources say only "ante-bellum" spirituals and that Easter Rock predates the Civil War. No firm first date exists. |
| country | 1925 | First Louisiana country record (John W. Daniel). The fiddle and ballad tradition behind it is much older and undated. |
| funk | 1967 | The Meters form (64 Parishes). Their first chart singles are 1969. Wikipedia gives 1965 for the band. |
| hiphop | 1986 | Ninja Crew single. "Late 1980s" is the safer phrase. |

## Region boundaries that are judgment calls

- **Single-parish regions.** Colonial, Congo Square, jazz core, brass, Mardi Gras Indian, R&B,
  funk, bounce and New Orleans hip-hop are Orleans Parish only, because that is where every
  source places them. Jefferson Parish (West Bank) could be argued for several.
- **`jazz_lake_river`** rests on two documented cases only: the Dew Drop hall in Mandeville and
  Kid Ory's Woodland Band near LaPlace. Other river and bayou towns had early bands, but I did
  not verify them.
- **`cajun_prairie`** leaves out Vermilion, Iberia and the Lafourche country, which are Cajun by
  any cultural definition (Acadiana is officially 22 parishes). They are missing because the
  music sources I read did not name towns there.
- **`creole_prairie`** and **`zydeco_core`** are small for the same reason.
- **`blues_baton_rouge`**: St. Francisville is in West Feliciana and Clinton and Slaughter are in
  East Feliciana; the source lists the towns, and I assigned the parishes. Crowley (Acadia),
  where swamp blues was recorded, is not in the region.
- **`blues_delta`** and **`blues_shreveport`** start in 1900 as an approximation. The Delta
  fieldwork cited dates from the 1980s.
- **`gospel_north`** (1900) and **`gospel_cities`** (1910): start years are approximate. Gospel is
  sung statewide; these rows mark where the sources name performers.
- **`country_north`** omits Richland Parish (Delhi), which the source names only as a modern
  star's hometown.
- **`hiphop_baton_rouge`** starts in 1997; the source says only "late 1990s".
- Parish assignment of towns (for example Oak Grove to West Carroll, Pineville to Rapides,
  Dubach to Lincoln, Vinton to Calcasieu) is mine where the source named only the town.

## Fact-check corrections

- `poverty_point` (places) writeup: text revised. The flat statement that no instruments have been reported was an unsourced negative; reworded to what the Louisiana Division of Archaeology and the cited sources actually say, with the plaza gathering kept as inference. (https://www.crt.state.la.us/dataprojects/archaeology/povertypoint/ceremonial-life.html)
- `poverty_point` (places) sources: text revised. Adds the state archaeology page that supports the statements about ceremony and the plaza post circles. (https://www.crt.state.la.us/dataprojects/archaeology/povertypoint/ceremonial-life.html)
- `chitimacha_charenton` (places) writeup: text revised. Densmore describes no alligator-skin rattle: the drum and the alligator skin (scraped with a stick) come from Swanton 1911 as quoted by her, not from the 1933 informants, and her remark that the songs were lost is now framed as her own judgment. (https://archive.org/stream/bulletin1331943smit/bulletin1331943smit_djvu.txt)
- `tunica_biloxi_marksville` (places) writeup: text revised. 64 Parishes dates the move to the Red River confluence to several years after French contact; 1706 is the year the Tunica attacked their Houma hosts, not the year of the move. (https://64parishes.org/entry/tunica-biloxi-tribe)
- `united_houma_nation` (places) writeup: text revised. The source identifies Lanor Curole only as a tribal member from Golden Meadow, and the tribe's site lists 400 Monarch Drive as the main office with a temporary address elsewhere in Houma since January 2026. (https://gardevoirci.nicholls.edu/2021/music/)
- `adai_caddo_robeline` (places) writeup: text revised. States plainly that the Adai Caddo are a separate, state-recognized tribe distinct from the Caddo Nation in Oklahoma, and dates the chief's remarks to the 2014 feature. (https://gov.louisiana.gov/federal-and-state-recognized-tribes)
- `adai_caddo_robeline` (places) sources: text revised. The row rested on a TV feature and a tourism page; the tribe's own site (name, address, annual powwow) and the state list of recognized tribes now support it. (https://www.adaicaddo.com/)
- `theatre_st_pierre` (places) writeup: text revised. Makes the two accounts of the closing consistent with the more detailed chronology (closed 1803 for disrepair, reopened 1804, auctioned 1810). (https://en.wikipedia.org/wiki/Theatre_de_la_Rue_Saint_Pierre)
- `theatre_st_pierre` (places) year_end: "1803" -> "1810". The 1803 closure was for the bad condition of the building and the theatre reopened in 1804; the building was auctioned in 1810, so 1810 is the defensible end year. (https://en.wikipedia.org/wiki/Theatre_de_la_Rue_Saint_Pierre)
- `union_sons_hall_funky_butt` (places) writeup: text revised. No source says Bolden owned the hall; the sources say his band was the most popular of several that played there. (https://veritenews.org/2024/07/01/bitd-funky-butt-hall-louis-armstrong-buddy-bolden/)
- `union_sons_hall_funky_butt` (places) listen_1_label: text revised. Smithsonian Folkways album on the Bolden era with audio samples; loads in a browser. (https://folkways.si.edu/music-of-new-orleans-vol-4-the-birth-of-jazz/ragtime/album/smithsonian)
- `union_sons_hall_funky_butt` (places) listen_1_url: text revised. Smithsonian Folkways album on the Bolden era with audio samples; loads in a browser. (https://folkways.si.edu/music-of-new-orleans-vol-4-the-birth-of-jazz/ragtime/album/smithsonian)
- `storyville` (places) listen_1_label: text revised. Smithsonian Folkways album whose tracks include pieces titled Storyville and Tom Anderson's; loads in a browser. (https://folkways.si.edu/music-of-new-orleans-vol-4-the-birth-of-jazz/ragtime/album/smithsonian)
- `storyville` (places) listen_1_url: text revised. Smithsonian Folkways album whose tracks include pieces titled Storyville and Tom Anderson's; loads in a browser. (https://folkways.si.edu/music-of-new-orleans-vol-4-the-birth-of-jazz/ragtime/album/smithsonian)
- `colored_waifs_home` (places) year_start: "1913" -> "1906". The Home opened in 1906, and the other rows date a place from its founding rather than from a famous arrival; the write-up already gives Armstrong's 1913 arrival. (https://veritenews.org/2024/06/12/bitd-colored-waifs-home-parish-prison/)
- `jelly_roll_morton_house` (places) year_start: "1885" -> "1890". Britannica gives October 20, 1890 and Wikipedia about 1890, while 1885 rests on A Closer Walk's circa date; the write-up already tells readers both years are given. (https://www.britannica.com/biography/Jelly-Roll-Morton)
- `fats_domino_house` (places) writeup: text revised. PBS American Masters and Slate both date the house to 1960, so "in the 1960s" is tightened and unsourced phrasing from the Substack post is dropped. (https://www.pbs.org/wnet/americanmasters/fats-domino-timeline-of-dominos-life-hits-and-career-highlights/6252/)
- `fats_domino_house` (places) sources: text revised. Replaces the Substack post with two stronger sources that give the 1960 date and the Caffin and Marais location. (https://slate.com/culture/2017/10/fats-domino-new-orleans-rock-legend-is-dead.html)
- `angola_state_penitentiary` (places) listen_1_label: "" -> "Angola Prisoners' Blues (Smithsonian Folkways / Arhoolie)". Folkways album of blues recorded inside Angola by Harry Oster in the 1950s; page loads with playable tracks. (https://folkways.si.edu/angola-prisoners-blues-cd/blues/music/album/smithsonian)
- `angola_state_penitentiary` (places) listen_1_url: text revised. Folkways album of blues recorded inside Angola by Harry Oster in the 1950s; page loads with playable tracks. (https://folkways.si.edu/angola-prisoners-blues-cd/blues/music/album/smithsonian)
- `slim_harpo_marker_mulatto_bend` (places) writeup: text revised. Born February 1924 and died 31 January 1970 makes him 45, not 46; the marker text the row copied is internally inconsistent. (https://en.wikipedia.org/wiki/Slim_Harpo)
- `haneys_big_house` (places) writeup: text revised. The marker at North First and Greathouse was erected by the town of Ferriday; the separate Blues Trail marker is about 0.2 miles away. (https://www.hmdb.org/m.asp?m=119690)
- `jd_miller_studio_crowley` (places) writeup: text revised. The mapped City Hall building is itself a studio site: Miller bought it in 1964 and ran his studio on the second floor; the unsupported "from 1957" Excello date is removed. (https://countryroadsmagazine.com/art-and-culture/history/restoring-the-past/)
- `jd_miller_studio_crowley` (places) sources: text revised. Adds the two sources that give the studio locations (M&S Electric at 218 North Parkerson; the 1964 purchase of the Ford building). (https://www.louisianafolklife.org/lt/articles_essays/miller_and_soileau.html)
- `jd_miller_studio_crowley` (places) listen_1_label: text revised. University archive record with audio of John Broven's 1979 interview with Miller in Crowley; page loads. (https://cls.louisiana.edu/node/23496)
- `jd_miller_studio_crowley` (places) listen_1_url: "" -> "https://cls.louisiana.edu/node/23496". University archive record with audio of John Broven's 1979 interview with Miller in Crowley; page loads. (https://cls.louisiana.edu/node/23496)
- `freds_lounge` (places) writeup: text revised. Tante Sue died on 1 April 2025, and the family history printed by the local paper dates the broadcast to 1968 on KEUN (KVPI from 1987), against 1962 on KVPI in the row. (https://www.evangelinetoday.com/news-local/taunt-sue-de-mamou-dies)
- `freds_lounge` (places) sources: text revised. Adds the local newspaper account that supports the 2025 death and the alternative radio dates. (https://www.evangelinetoday.com/news-local/taunt-sue-de-mamou-dies)
- `richards_club` (places) sources: text revised. The 2006 closing and the 2017 fire are now each supported by a contemporary news report instead of Wikipedia alone. (https://theind.com/articles/2697/)
- `jazz_fest_fair_grounds` (places) year_start: "1972" -> "1970". Judgment call: the festival was founded in April 1970; using the founding year matches the Festivals Acadiens row and keeps Jazz Fest on the timeline for 1970 and 1971, and the write-up already explains the 1972 move to the Fair Grounds. (https://64parishes.org/entry/new-orleans-jazz-heritage-festival)
- `studio_in_the_country` (places) year_start: "1972" -> "1973". The studio's own site gives 1973; 1972 comes from Wikipedia only, and the write-up already notes both dates. (https://studiointhecountry.com/)
- `festivals_acadiens_et_creoles` (places) writeup: text revised. The cited article does not say Dewey Balfa inspired the no-dancing format or that the event became a fall festival in 1976, so both claims are trimmed. (https://64parishes.org/a-major-milestone-for-the-music-of-french-louisiana)
- `southwest_louisiana_zydeco_festival` (places) writeup: text revised. The festival moved to the Yambilee grounds in 2016 and made that its permanent home in 2017; the write-up now gives the year and drops band names not found in the sources. (https://www.theadvertiser.com/story/entertainment/2017/08/28/after-35-years-zydeco-fest-finds-new-home/599843001/)
- `southwest_louisiana_zydeco_festival` (places) sources: text revised. Adds the festival's own history page and a report of the move to Opelousas. (https://www.zydeco.org/history/)
- `backstreet_cultural_museum` (places) lat: "29.9646" -> "29.9658". The point sits on the original Henriette Delille Street building; 1531 St. Philip Street, the home since July 2022, geocodes about 360 m to the west between North Villere and North Robertson streets. (https://en.wikipedia.org/wiki/Backstreet_Cultural_Museum)
- `backstreet_cultural_museum` (places) lon: "-90.0662" -> "-90.0701". The point sits on the original Henriette Delille Street building; 1531 St. Philip Street, the home since July 2022, geocodes about 360 m to the west between North Villere and North Robertson streets. (https://en.wikipedia.org/wiki/Backstreet_Cultural_Museum)
- `magnolia_projects_cash_money` (places): new row added by the fact-checker. NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) name: "" -> "Magnolia Projects (C.J. Peete) and Cash Money Records". NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) type: "" -> "landmark". NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) genre_id: "" -> "hiphop". NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) other_genres: "" -> "bounce". NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) year_start: "" -> "1991". NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) year_end: "" -> "2007". NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) town: "" -> "New Orleans". NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) parish: "" -> "Orleans". NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) lat: "" -> "29.9376". NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) lon: "" -> "-90.0910". NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) writeup: text revised. NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `magnolia_projects_cash_money` (places) sources: text revised. NEW ROW: adds a verified New Orleans hip-hop site for the 1990s. (https://acloserwalknola.com/places/magnolia-c-j-peete-public-housing-development/)
- `louisiana_swamp_pop_museum` (places): new row added by the fact-checker. NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) name: "" -> "Louisiana Swamp Pop Museum". NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) type: "" -> "institution". NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) genre_id: "" -> "swamp_pop". NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) other_genres: "" -> "rnb". NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) year_start: "" -> "2010". NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) town: "" -> "Ville Platte". NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) parish: "" -> "Evangeline". NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) lat: "" -> "30.6893". NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) lon: "" -> "-92.2737". NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) writeup: text revised. NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `louisiana_swamp_pop_museum` (places) sources: text revised. NEW ROW: adds a verified swamp pop site. (https://www.fox8live.com/2019/07/31/heart-louisiana-swamp-pop-museum/)
- `amede_ardoin_statue` (places): new row added by the fact-checker. NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) name: "" -> "Amédé Ardoin Statue (St. Landry Parish Visitor Center)". NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) type: "" -> "landmark". NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) genre_id: "" -> "creole". NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) other_genres: "" -> "cajun;zydeco". NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) year_start: "" -> "1929". NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) town: "" -> "Opelousas". NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) parish: "" -> "St. Landry". NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) lat: "" -> "30.5836". NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) lon: "" -> "-92.0509". NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) writeup: text revised. NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) listen_1_label: text revised. NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) listen_1_url: text revised. NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `amede_ardoin_statue` (places) sources: text revised. NEW ROW: adds a verified site for the first Creole and Cajun recordings of 1929 and after. (https://cajuntravel.com/things/amede-ardoin-statue/)
- `french_opera_house` (places) genre_id: "colonial" -> "classical". Opened December 1, 1859, fifty-six years after the colonial genre ends; it is an opera house and belongs to the new classical genre. (https://64parishes.org/entry/opera-and-ballet)
- `theatre_d_orleans` (places) genre_id: "colonial" -> "classical". Opened 1815, after the colonial period ended in 1803; it was the city's French opera house and belongs to the new classical genre. (https://64parishes.org/entry/opera-and-ballet)
- `theatre_st_pierre` (places) other_genres: "" -> "classical". Opened 1792 under Spanish rule, so colonial stays as the main genre, but its 1796 Sylvain is the starting point of the classical genre and it should appear there too. (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places): new row added by the fact-checker. New place for English-language theatre and concert life: 1824 Camp Street Theatre, 1835 opening, 4,100 seats and March 1842 fire from 64 Parishes; Lind's thirteen concerts from HNOC and Kimball; opening day and later history from Cinema Treasures. Coordinates agree between Wikipedia (29.95005, -90.07017) and OpenStreetMap for 426 St. Charles Ave (29.95004, -90.07029). (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) name: "" -> "St. Charles Theatre (site)". Field of the new place row; see the place_id line for the evidence. (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) type: "" -> "venue". Field of the new place row; see the place_id line for the evidence. (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) genre_id: "" -> "classical". Field of the new place row; see the place_id line for the evidence. (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) year_start: "" -> "1835". New place for English-language theatre and concert life: 1824 Camp Street Theatre, 1835 opening, 4,100 seats and March 1842 fire from 64 Parishes; Lind's thirteen concerts from HNOC and Kimball; opening day and later history from Cinema Treasures. Coordinates agree between Wikipedia (29.95005, -90.07017) and OpenStreetMap for 426 St. Charles Ave (29.95004, -90.07029). (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) year_end: "" -> "1965". New place for English-language theatre and concert life: 1824 Camp Street Theatre, 1835 opening, 4,100 seats and March 1842 fire from 64 Parishes; Lind's thirteen concerts from HNOC and Kimball; opening day and later history from Cinema Treasures. Coordinates agree between Wikipedia (29.95005, -90.07017) and OpenStreetMap for 426 St. Charles Ave (29.95004, -90.07029). (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) town: "" -> "New Orleans". Field of the new place row; see the place_id line for the evidence. (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) parish: "" -> "Orleans". Field of the new place row; see the place_id line for the evidence. (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) lat: "" -> "29.9500". New place for English-language theatre and concert life: 1824 Camp Street Theatre, 1835 opening, 4,100 seats and March 1842 fire from 64 Parishes; Lind's thirteen concerts from HNOC and Kimball; opening day and later history from Cinema Treasures. Coordinates agree between Wikipedia (29.95005, -90.07017) and OpenStreetMap for 426 St. Charles Ave (29.95004, -90.07029). (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) lon: "" -> "-90.0702". New place for English-language theatre and concert life: 1824 Camp Street Theatre, 1835 opening, 4,100 seats and March 1842 fire from 64 Parishes; Lind's thirteen concerts from HNOC and Kimball; opening day and later history from Cinema Treasures. Coordinates agree between Wikipedia (29.95005, -90.07017) and OpenStreetMap for 426 St. Charles Ave (29.95004, -90.07029). (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) writeup: text revised. New place for English-language theatre and concert life: 1824 Camp Street Theatre, 1835 opening, 4,100 seats and March 1842 fire from 64 Parishes; Lind's thirteen concerts from HNOC and Kimball; opening day and later history from Cinema Treasures. Coordinates agree between Wikipedia (29.95005, -90.07017) and OpenStreetMap for 426 St. Charles Ave (29.95004, -90.07029). (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) sources: text revised. New place for English-language theatre and concert life: 1824 Camp Street Theatre, 1835 opening, 4,100 seats and March 1842 fire from 64 Parishes; Lind's thirteen concerts from HNOC and Kimball; opening day and later history from Cinema Treasures. Coordinates agree between Wikipedia (29.95005, -90.07017) and OpenStreetMap for 426 St. Charles Ave (29.95004, -90.07029). (https://64parishes.org/entry/opera-and-ballet)
- `first_presbyterian_lafayette_square` (places): new row added by the fact-checker. New place for Protestant church music and public-school singing: choir, 1841 concert, July 1, 1842 exhibition, November 1842 singing school and 1857 Erben organ from the Kimball dissertation; 1835, 1854, 1857, 1938 and the site (now the F. Edward Hebert Federal Building) from Campanella. Coordinates of the Hebert building agree between OpenStreetMap (29.94741, -90.07047) and the Esri geocoder for 600 S. Maestri Place (29.94741, -90.07047). (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) name: "" -> "First Presbyterian Church, Lafayette Square (site)". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) type: "" -> "institution". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) genre_id: "" -> "classical". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) year_start: "" -> "1835". New place for Protestant church music and public-school singing: choir, 1841 concert, July 1, 1842 exhibition, November 1842 singing school and 1857 Erben organ from the Kimball dissertation; 1835, 1854, 1857, 1938 and the site (now the F. Edward Hebert Federal Building) from Campanella. Coordinates of the Hebert building agree between OpenStreetMap (29.94741, -90.07047) and the Esri geocoder for 600 S. Maestri Place (29.94741, -90.07047). (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) year_end: "" -> "1938". New place for Protestant church music and public-school singing: choir, 1841 concert, July 1, 1842 exhibition, November 1842 singing school and 1857 Erben organ from the Kimball dissertation; 1835, 1854, 1857, 1938 and the site (now the F. Edward Hebert Federal Building) from Campanella. Coordinates of the Hebert building agree between OpenStreetMap (29.94741, -90.07047) and the Esri geocoder for 600 S. Maestri Place (29.94741, -90.07047). (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) town: "" -> "New Orleans". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) parish: "" -> "Orleans". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) lat: "" -> "29.9474". New place for Protestant church music and public-school singing: choir, 1841 concert, July 1, 1842 exhibition, November 1842 singing school and 1857 Erben organ from the Kimball dissertation; 1835, 1854, 1857, 1938 and the site (now the F. Edward Hebert Federal Building) from Campanella. Coordinates of the Hebert building agree between OpenStreetMap (29.94741, -90.07047) and the Esri geocoder for 600 S. Maestri Place (29.94741, -90.07047). (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) lon: "" -> "-90.0705". New place for Protestant church music and public-school singing: choir, 1841 concert, July 1, 1842 exhibition, November 1842 singing school and 1857 Erben organ from the Kimball dissertation; 1835, 1854, 1857, 1938 and the site (now the F. Edward Hebert Federal Building) from Campanella. Coordinates of the Hebert building agree between OpenStreetMap (29.94741, -90.07047) and the Esri geocoder for 600 S. Maestri Place (29.94741, -90.07047). (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) writeup: text revised. New place for Protestant church music and public-school singing: choir, 1841 concert, July 1, 1842 exhibition, November 1842 singing school and 1857 Erben organ from the Kimball dissertation; 1835, 1854, 1857, 1938 and the site (now the F. Edward Hebert Federal Building) from Campanella. Coordinates of the Hebert building agree between OpenStreetMap (29.94741, -90.07047) and the Esri geocoder for 600 S. Maestri Place (29.94741, -90.07047). (https://exa.ai/library/publication/vppbys56qr5)
- `first_presbyterian_lafayette_square` (places) sources: text revised. New place for Protestant church music and public-school singing: choir, 1841 concert, July 1, 1842 exhibition, November 1842 singing school and 1857 Erben organ from the Kimball dissertation; 1835, 1854, 1857, 1938 and the site (now the F. Edward Hebert Federal Building) from Campanella. Coordinates of the Hebert building agree between OpenStreetMap (29.94741, -90.07047) and the Esri geocoder for 600 S. Maestri Place (29.94741, -90.07047). (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places): new row added by the fact-checker. New place for the sacred concert tradition: February 1836 oratorio, 1842 founding, May 18, 1842 concert, complete Creation and 1850 notice from the Kimball dissertation; the St. Charles and Gravier location and the 1851 fire from Campanella. Intersection coordinates agree between the Esri geocoder (29.95147, -90.07003) and the Census geocoder (29.95150, -90.06987). (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) name: text revised. Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) type: "" -> "institution". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) genre_id: "" -> "classical". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) year_start: "" -> "1836". New place for the sacred concert tradition: February 1836 oratorio, 1842 founding, May 18, 1842 concert, complete Creation and 1850 notice from the Kimball dissertation; the St. Charles and Gravier location and the 1851 fire from Campanella. Intersection coordinates agree between the Esri geocoder (29.95147, -90.07003) and the Census geocoder (29.95150, -90.06987). (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) year_end: "" -> "1851". New place for the sacred concert tradition: February 1836 oratorio, 1842 founding, May 18, 1842 concert, complete Creation and 1850 notice from the Kimball dissertation; the St. Charles and Gravier location and the 1851 fire from Campanella. Intersection coordinates agree between the Esri geocoder (29.95147, -90.07003) and the Census geocoder (29.95150, -90.06987). (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) town: "" -> "New Orleans". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) parish: "" -> "Orleans". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) lat: "" -> "29.9515". New place for the sacred concert tradition: February 1836 oratorio, 1842 founding, May 18, 1842 concert, complete Creation and 1850 notice from the Kimball dissertation; the St. Charles and Gravier location and the 1851 fire from Campanella. Intersection coordinates agree between the Esri geocoder (29.95147, -90.07003) and the Census geocoder (29.95150, -90.06987). (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) lon: "" -> "-90.0700". New place for the sacred concert tradition: February 1836 oratorio, 1842 founding, May 18, 1842 concert, complete Creation and 1850 notice from the Kimball dissertation; the St. Charles and Gravier location and the 1851 fire from Campanella. Intersection coordinates agree between the Esri geocoder (29.95147, -90.07003) and the Census geocoder (29.95150, -90.06987). (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) writeup: text revised. New place for the sacred concert tradition: February 1836 oratorio, 1842 founding, May 18, 1842 concert, complete Creation and 1850 notice from the Kimball dissertation; the St. Charles and Gravier location and the 1851 fire from Campanella. Intersection coordinates agree between the Esri geocoder (29.95147, -90.07003) and the Census geocoder (29.95150, -90.06987). (https://exa.ai/library/publication/vppbys56qr5)
- `clapp_church_sacred_music_society` (places) sources: text revised. New place for the sacred concert tradition: February 1836 oratorio, 1842 founding, May 18, 1842 concert, complete Creation and 1850 notice from the Kimball dissertation; the St. Charles and Gravier location and the 1851 fire from Campanella. Intersection coordinates agree between the Esri geocoder (29.95147, -90.07003) and the Census geocoder (29.95150, -90.06987). (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places): new row added by the fact-checker. New place for the American-sector sheet music trade: Mayo at 5 Camp Street, 1841 purchase, 1853 sale, Hall & Son partnership, tickets and advertising from the Kimball dissertation; Werlein and Dixie from HNOC. The point is the Canal Street end of Camp Street (Esri 29.95242, -90.06826 and OpenStreetMap 29.95236, -90.06823 for 100 Camp St); the lot of old No. 5 is approximate and the write-up says so. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) name: "" -> "Mayo and Werlein music store, No. 5 Camp Street (site)". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) type: "" -> "institution". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) genre_id: "" -> "classical". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) year_start: "" -> "1841". New place for the American-sector sheet music trade: Mayo at 5 Camp Street, 1841 purchase, 1853 sale, Hall & Son partnership, tickets and advertising from the Kimball dissertation; Werlein and Dixie from HNOC. The point is the Canal Street end of Camp Street (Esri 29.95242, -90.06826 and OpenStreetMap 29.95236, -90.06823 for 100 Camp St); the lot of old No. 5 is approximate and the write-up says so. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) year_end: "" -> "1867". New place for the American-sector sheet music trade: Mayo at 5 Camp Street, 1841 purchase, 1853 sale, Hall & Son partnership, tickets and advertising from the Kimball dissertation; Werlein and Dixie from HNOC. The point is the Canal Street end of Camp Street (Esri 29.95242, -90.06826 and OpenStreetMap 29.95236, -90.06823 for 100 Camp St); the lot of old No. 5 is approximate and the write-up says so. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) town: "" -> "New Orleans". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) parish: "" -> "Orleans". Field of the new place row; see the place_id line for the evidence. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) lat: "" -> "29.9524". New place for the American-sector sheet music trade: Mayo at 5 Camp Street, 1841 purchase, 1853 sale, Hall & Son partnership, tickets and advertising from the Kimball dissertation; Werlein and Dixie from HNOC. The point is the Canal Street end of Camp Street (Esri 29.95242, -90.06826 and OpenStreetMap 29.95236, -90.06823 for 100 Camp St); the lot of old No. 5 is approximate and the write-up says so. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) lon: "" -> "-90.0683". New place for the American-sector sheet music trade: Mayo at 5 Camp Street, 1841 purchase, 1853 sale, Hall & Son partnership, tickets and advertising from the Kimball dissertation; Werlein and Dixie from HNOC. The point is the Canal Street end of Camp Street (Esri 29.95242, -90.06826 and OpenStreetMap 29.95236, -90.06823 for 100 Camp St); the lot of old No. 5 is approximate and the write-up says so. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) writeup: text revised. New place for the American-sector sheet music trade: Mayo at 5 Camp Street, 1841 purchase, 1853 sale, Hall & Son partnership, tickets and advertising from the Kimball dissertation; Werlein and Dixie from HNOC. The point is the Canal Street end of Camp Street (Esri 29.95242, -90.06826 and OpenStreetMap 29.95236, -90.06823 for 100 Camp St); the lot of old No. 5 is approximate and the write-up says so. (https://exa.ai/library/publication/vppbys56qr5)
- `mayo_werlein_5_camp_street` (places) sources: text revised. New place for the American-sector sheet music trade: Mayo at 5 Camp Street, 1841 purchase, 1853 sale, Hall & Son partnership, tickets and advertising from the Kimball dissertation; Werlein and Dixie from HNOC. The point is the Canal Street end of Camp Street (Esri 29.95242, -90.06826 and OpenStreetMap 29.95236, -90.06823 for 100 Camp St); the lot of old No. 5 is approximate and the write-up says so. (https://exa.ai/library/publication/vppbys56qr5)
- `classical` (genres) sources: text revised. The 2018 American Music article was not read (the repository record carries no text or abstract), so its label must say it is further reading and not a source consulted; no claim in the row depends on it. (https://repository.lsu.edu/music_pubs/102)
- `clapp_church_sacred_music_society` (places) sources: text revised. The 2018 American Music article was not read (the repository record carries no text or abstract), so its label must say it is further reading and not a source consulted; no claim in the row depends on it. (https://repository.lsu.edu/music_pubs/102)
- `classical_new_orleans` (regions) note: text revised. The cited 64 Parishes article names opera and ballet companies outside New Orleans (Opéra Louisiane in Baton Rouge, 2006; Baton Rouge and Lafayette ballet companies), so the statement that every dated event in the sources took place in New Orleans is false as written. (https://64parishes.org/entry/opera-and-ballet)
- `st_charles_theatre` (places) writeup: text revised. Lind's New Orleans run was not confined to February: the Daily Crescent advertised her tenth concert on March 3 and her twelfth at the St. Charles Theatre for Friday, March 7, 1851 (one word trimmed to stay within 120 words). (https://www.loc.gov/collections/chronicling-america/?dl=page&end_date=1851-03-12&ops=PHRASE&qs=Jenny+Lind&searchType=advanced&start_date=1851-03-03&location_state=louisiana)
- `st_charles_theatre` (places) sources: text revised. Adds the period newspaper that supports the February and March dating of the Lind concerts. (https://www.loc.gov/collections/chronicling-america/?dl=page&end_date=1851-03-12&ops=PHRASE&qs=Jenny+Lind&searchType=advanced&start_date=1851-03-03&location_state=louisiana)
- `mayo_werlein_5_camp_street` (places) year_end: "1867" -> "1862". Boudreaux's directory study has Werlein at 3 and 5 Camp Street through 1861, closing the business in 1862 when he refused the Union oath, and not listed again as a music merchant until 1867, at 82 Baronne Street; Jumonville likewise says his stock was confiscated in 1862 and the firm ceased operations until autumn 1865, so 1867 (Wikipedia) is the date of the next known address, not the end of the Camp Street store. (https://repository.lsu.edu/gradschool_disstheses/8225/)
- `mayo_werlein_5_camp_street` (places) writeup: text revised. The claim that Werlein was first to publish Dixie is contested (Firth, Pond & Co. issued Emmett's authorized edition in New York in 1860; Werlein's was the first Southern edition and at first credited J. C. Viereck, not Emmett); 1846 is the date given by most accounts (Boudreaux, Jumonville, Lemmon), not only 64 Parishes; and the store's 1862 closing is added to match the corrected year_end. (https://repository.lsu.edu/gradschool_disstheses/8225/)
- `mayo_werlein_5_camp_street` (places) sources: text revised. Replaces the Wikipedia citation for the store's end with the two scholarly sources that document the 1862 closing, the 1846 date and the Dixie edition. (https://repository.lsu.edu/gradschool_disstheses/8225/)

## Land-and-sound fact-check corrections

- land-and-sound `ancient` (genres) nature_note: revised. The cited 64 Parishes page says nothing about archaeologists inferring gatherings; UNESCO's residential and ceremonial wording is the supportable claim, and the flood sentence was a near-copy. (https://whc.unesco.org/en/list/1435/)
- land-and-sound `ancient` (genres) sources: revised. Adds the source that supports the ceremonial-use statement. (https://whc.unesco.org/en/list/1435/)
- land-and-sound `native` (genres) nature_note: revised. The alligator-skin instrument comes from Swanton 1911 as quoted by Densmore, not from elders in 1933; the claim that instruments come from each nation's own country is unsupported (the Houma chief names elk skins); the Houma clause was a near-copy. (https://archive.org/stream/bulletin1331943smit/bulletin1331943smit_djvu.txt)
- land-and-sound `congo` (genres) nature_note: revised. The source lists the instruments and says they were modeled after African prototypes; it does not say the sound was made from what the country supplied. (https://64parishes.org/entry/congo-square)
- land-and-sound `creole` (genres) nature_note: revised. The original joined the cattle families and the accordion merchants as one story and said the merchants imported the first accordions; the two sources are independent and Ancelet says only that merchants began importing diatonic accordions. (https://www.louisianafolklife.org/lt/articles_essays/cajunzydeco.html)
- land-and-sound `cajun` (genres) nature_note: revised. The opening sentence was a near-copy of Sandmel's sentence; reworded and attributed, claims unchanged. (https://www.louisianafolklife.org/LT/Articles_Essays/treas_trad_la_music.html)
- land-and-sound `zydeco` (genres) nature_note: revised. Ancelet presents the haricots derivation as a folk explanation and notes studies suggesting African origins, so the name cannot be stated as fact; snap beans is not in the cited sources. (https://www.louisianafolklife.org/lt/articles_essays/cajunzydeco.html)
- land-and-sound `mardigras_indian` (genres) nature_note: revised. The source says Indians were once seen only on Mardi Gras day and St. Joseph's night but now appear all year, so the calendar is not fixed. (https://64parishes.org/entry/mardi-gras-indians)
- land-and-sound `blues` (genres) nature_note: revised. Neither source calls the Baton Rouge sound relaxed (Sandmel's phrase is country in the city), and changes with the land implied a causal link the sources do not make. (https://www.louisianafolklife.org/LT/Articles_Essays/blues.html)
- land-and-sound `gospel` (genres) nature_note: revised. Roach quotes one rocker preferring the wooden-floor sound to concrete; she does not report rockers lamenting its loss. (https://www.louisianafolklife.org/LT/Articles_Essays/easterrock.html)
- land-and-sound `country` (genres) nature_note: revised. Opening sentence and the oil-camp clause were near-copies of the sources; reworded and attributed, claims unchanged. (https://64parishes.org/entry/country-music)
- land-and-sound `swamp_pop` (genres) nature_note: revised. Neither source says swamp is shorthand for south Louisiana or that the name points to a homeland, not a sound; Sandmel in fact ties its regional identity to a vocal style. (https://www.louisianafolklife.org/LT/Articles_Essays/treas_trad_la_music.html)
- land-and-sound `hiphop` (genres) nature_note: revised. First sentence was a near-copy of the source, and the clearest-case claim was the researcher's own judgment, not the source's. (https://64parishes.org/entry/rap-hip-hop-and-bounce-music)
- land-and-sound `ancient_poverty_point` (regions) nature_note: revised. The sources place the site, not the whole parish, on Macon Ridge; the flood sentence was a near-copy. (https://64parishes.org/entry/poverty-point)
- land-and-sound `native_caddo` (regions) nature_note: revised. The original merged two different songs: the Redbird riding song about removal, and a separate Across the Ouachita song the source links to a 1787 move. (https://www.louisianafolklife.org/LT/Articles_Essays/creole_art_caddo_homecomin.html)
- land-and-sound `native_chitimacha` (regions) nature_note: revised. Densmore says only cane, in a legend told by Benjamin Paul; equating it with the river cane of the basketry was the researcher's inference. (https://archive.org/stream/bulletin1331943smit/bulletin1331943smit_djvu.txt)
- land-and-sound `cajun_prairie` (regions) nature_note: revised. The EPA table lists cropland of mostly rice, soybeans and hay with some crawfish aquaculture, not mostly rice fields and crawfish ponds. (https://dmap-prod-oms-edc.s3.us-east-1.amazonaws.com/ORD/Ecoregions/la/la_back.pdf)
- land-and-sound `zydeco_core` (regions) nature_note: revised. Plaisance and Cecilia are the home towns of riders quoted in the article; the ride it describes was held in Sulphur. (https://64parishes.org/creole-trail-rides)
- land-and-sound `blues_shreveport` (regions) nature_note: revised. The NPS page says he was exposed to music on Fannin Street, not that he played its saloons; the cotton phrase was a near-copy. (https://www.nps.gov/locations/lowermsdeltaregion/leadbelly.htm)
- land-and-sound `blues_delta` (regions) nature_note: revised. The EPA table still lists forested wetlands and deciduous forest first, so gave way largely to crops overstates it; the blues clause was a near-copy. (https://dmap-prod-oms-edc.s3.us-east-1.amazonaws.com/ORD/Ecoregions/la/la_back.pdf)
- land-and-sound `gospel_delta` (regions) nature_note: revised. Roach places the surviving Easter Rock in Winnsboro, not near it. (https://www.louisianafolklife.org/LT/Articles_Essays/easterrock.html)
- land-and-sound `country_north` (regions) nature_note: revised. Sandmel says the region is populated, not settled, by these groups, and the Colvin clause was a near-copy of the 64 Parishes sentence. (https://64parishes.org/entry/country-music)
- land-and-sound `poverty_point` (places) nature_note: revised. Two clauses were near-copies of the 64 Parishes sentences; reworded, claims unchanged. (https://64parishes.org/entry/poverty-point)
- land-and-sound `marksville_site` (places) nature_note: revised. The article hedges that the site may have served as a ceremonial site; the original stated it as fact and added an inference about siting on the river bank. (https://www.tunicabiloxi.org/this-archaeological-site-drew-pilgrims-2000-years-ago-now-there-are-big-plans-for-its-future/)
- land-and-sound `chitimacha_charenton` (places) nature_note: revised. Densmore attributes the legend to Benjamin Paul and quotes a single earlier account (Swanton 1911), not several older accounts. (https://archive.org/stream/bulletin1331943smit/bulletin1331943smit_djvu.txt)
- land-and-sound `tunica_biloxi_marksville` (places) nature_note: revised. First sentence was a near-copy of the tribe's own sentence and did not make clear this was an earlier village, not Marksville. (https://www.tunicabiloxi.org/history/)
- land-and-sound `united_houma_nation` (places) nature_note: revised. The lands-and-waters clause was verbatim from the source, and the handed-down-by-elders statement is the article's, not Chief Creppel's. (https://gardevoirci.nicholls.edu/2021/music/)
- land-and-sound `congo_square` (places) nature_note: revised. City Commons and turning basin are both in Johnson but belong to different periods (colonial market ground; after 1812), and simple, open, grassy plain was verbatim. (https://64parishes.org/congo-square-la-place-publique)
- land-and-sound `milneburg` (places) nature_note: revised. Raeburn says the seawall and landfill erased the music scene, not the shoreline, and does not say the camps were rented. (https://64parishes.org/jazz-at-the-lakefront)
- land-and-sound `acadian_arrival_st_martinville` (places) nature_note: revised. February 1765 is the arrival at New Orleans; the source does not date the move to the Attakapas to that month. (https://acadianmemorial.org/acadian-immigration-into-south-louisiana-1764-1785/)
- land-and-sound `73` (ecoregion) description: revised. Delta blues as a genre did not arise in Louisiana; Sandmel describes a northeastern-parish style similar to the Mississippi Delta's, and all arose here overstates origin. (https://www.louisianafolklife.org/LT/Articles_Essays/blues.html)
- land-and-sound `75` (ecoregion) description: revised. Spatial overlay of the map's places on the EPA Level III layer puts the Dew Drop hall in ecoregion 75; replaces a sentence about the map's own notes. ()

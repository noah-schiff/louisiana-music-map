import pytest
from conftest import write_research, edited, GOOD
import schema

def problems(tmp_path, **ov):
    with pytest.raises(schema.SchemaError) as e:
        schema.load_research(write_research(tmp_path / "r", **ov))
    return "\n".join(e.value.problems)

def test_good_set_loads_with_types(research):
    r = schema.load_research(research)
    p = r["places"][0]
    assert (p["year_start"], p["year_end"], p["lat"], p["out_of_state"]) == (-1700, -1100, 32.6367, False)
    assert p["sources"] == [{"label": "Site", "url": "https://example.org/pp"}, {"label": "A book", "url": ""}]
    assert r["genres"][1]["year_end"] is None
    assert r["regions"][0]["parishes"] == ["Orleans", "Jefferson"]

def test_excel_bom_and_blank_rows_are_tolerated(tmp_path):
    blank = {k: "" for k in GOOD["cities"][0]}
    f = write_research(tmp_path / "r", encoding="utf-8-sig", cities=GOOD["cities"] + [blank])
    r = schema.load_research(f)
    assert r["genres"][0]["genre_id"] == "ancient" and len(r["cities"]) == 1

def test_non_utf8_file_gives_save_as_instruction(tmp_path):
    f = write_research(tmp_path / "r")
    (f / "cities.csv").write_bytes("name,lat,lon\nThibodaux caf\xe9,29.8,-90.8\n".encode("cp1252"))
    with pytest.raises(schema.SchemaError) as e:
        schema.load_research(f)
    assert "CSV UTF-8" in e.value.problems[0]

def test_missing_required_field(tmp_path):
    assert "p1: writeup is blank" in problems(tmp_path, **edited("places", writeup=""))

def test_missing_column(tmp_path):
    rows = [{k: v for k, v in r.items() if k != "sources"} for r in GOOD["places"]]
    assert "places.csv: missing column sources" in problems(tmp_path, places=rows)

def test_unknown_genre(tmp_path):
    assert "unknown genre_id 'polka'" in problems(tmp_path, **edited("places", genre_id="polka"))
    assert "unknown genre_id 'polka'" in problems(tmp_path, **edited("places", other_genres="jazz; polka"))

def test_bad_and_reversed_years(tmp_path):
    assert "year_start 'c. 1900' is not a whole number" in problems(tmp_path, **edited("places", year_start="c. 1900"))
    assert "year_start is after year_end" in problems(tmp_path, **edited("places", year_start="-1000", year_end="-1100"))
    assert "year 0 does not exist" in problems(tmp_path, **edited("places", year_end="0"))

def test_bad_type_color_coords_url(tmp_path):
    assert "type 'bar' is not one of" in problems(tmp_path, **edited("places", type="bar"))
    assert "color 'blue'" in problems(tmp_path, **edited("genres", color="blue"))
    assert "lat/lon outside Louisiana" in problems(tmp_path, **edited("places", lat="40.7", lon="-74.0"))
    assert "listen_1_url must start with http" in problems(
        tmp_path, **edited("places", listen_1_label="Hear", listen_1_url="javascript:alert(1)"))
    assert "listen_1 needs both label and url" in problems(tmp_path, **edited("places", listen_1_label="Hear"))

def test_out_of_state_flag_allows_far_coordinates(tmp_path):
    f = write_research(tmp_path / "r", **edited("places", lat="40.7", lon="-74.0", out_of_state="yes"))
    assert schema.load_research(f)["places"][0]["out_of_state"] is True

def test_duplicate_ids_and_all_problems_reported_together(tmp_path):
    rows = GOOD["places"] + [dict(GOOD["places"][0], writeup="")]
    text = problems(tmp_path, places=rows)
    assert "duplicate place_id 'p1'" in text and "writeup is blank" in text

def test_eras_must_be_contiguous(tmp_path):
    assert "eras must be contiguous" in problems(tmp_path, **edited("eras", 1, year_start="1600"))

NATURE = [{"table": "places", "row_id": "p1", "nature_note": "Built on Macon Ridge above the floodplain.",
           "sources": "NPS <https://example.org/n>"}]
ECO = [{"eco_id": "73", "name": "Mississippi Alluvial Plain", "description": "Flat river bottomland.",
        "sources": "EPA <https://example.org/e>"}]

def test_nature_and_ecoregions_are_optional(research):
    r = schema.load_research(research)
    assert r["nature"] == [] and r["ecoregions"] == []

def test_nature_and_ecoregions_load(tmp_path):
    r = schema.load_research(write_research(tmp_path / "r", nature=NATURE, ecoregions=ECO))
    assert r["nature"][0]["sources"] == [{"label": "NPS", "url": "https://example.org/n"}]
    assert r["ecoregions"][0]["eco_id"] == "73"

def test_nature_note_must_point_at_a_real_row(tmp_path):
    bad = [dict(NATURE[0], row_id="nowhere"), dict(NATURE[0], table="cities")]
    text = problems(tmp_path, nature=bad)
    assert "nature.csv: no places row 'nowhere'" in text and "nature.csv: table 'cities'" in text

def test_text_longer_than_its_geodatabase_field_is_reported(tmp_path):
    text = problems(tmp_path, **edited("places", writeup="x" * 3001))
    assert "p1: writeup is 3001 characters; the limit is 3000" in text

def test_text_at_the_limit_is_accepted(tmp_path):
    r = schema.load_research(write_research(tmp_path / "r", **edited("places", writeup="x" * 3000)))
    assert len(r["places"][0]["writeup"]) == 3000

def test_optional_tables_reject_blank_and_duplicate_rows(tmp_path):
    text = problems(tmp_path, nature=NATURE + NATURE, ecoregions=[dict(ECO[0], description="")])
    assert "nature.csv: duplicate note for places 'p1'" in text
    assert "ecoregions.csv: 73: description is blank" in text

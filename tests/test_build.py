from pathlib import Path
import pytest
from conftest import write_research, edited
import schema

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data_raw"
pytestmark = pytest.mark.skipif(not (RAW / "cb_2023_us_county_500k").exists(), reason="base data not downloaded")

def test_build_counts_and_crs(tmp_path):
    import arcpy, build_gdb
    gdb = tmp_path / "t.gdb"
    counts = build_gdb.build(write_research(tmp_path / "r"), RAW, gdb)
    assert counts == {"genres": 2, "eras": 2, "regions": 1, "places": 1, "cities": 1, "parishes": 64,
                      "ecoregions": 6, "nature": 0}
    assert arcpy.Describe(str(gdb / "Places")).spatialReference.factoryCode == 26915
    assert int(arcpy.management.GetCount(str(gdb / "Base_Rivers"))[0]) > 0
    assert int(arcpy.management.GetCount(str(gdb / "Base_Lakes"))[0]) > 0
    with arcpy.da.SearchCursor(str(gdb / "Regions"), ["SHAPE@AREA", "parishes"]) as c:
        area, parishes = next(c)
    assert area > 1e8 and parishes == "Orleans; Jefferson"

def test_unmatched_parish_is_an_error_naming_it(tmp_path):
    import build_gdb
    r = write_research(tmp_path / "r", **edited("regions", parishes="Orleans; Atlantis"))
    with pytest.raises(schema.SchemaError) as e:
        build_gdb.build(r, RAW, tmp_path / "t.gdb")
    assert "r1: no parish named 'Atlantis'" in e.value.problems[0]

def test_validate_clean_build_has_no_problems(tmp_path):
    import build_gdb, validate
    r = write_research(tmp_path / "r"); gdb = tmp_path / "t.gdb"
    build_gdb.build(r, RAW, gdb)
    assert validate.check_gdb(r, gdb) == []

def test_validate_flags_point_outside_state(tmp_path):
    import build_gdb, validate
    # In the Gulf: inside the lat/lon sanity box, outside the state polygon.
    r = write_research(tmp_path / "r", **edited("places", lat="28.7", lon="-91.5"))
    gdb = tmp_path / "t.gdb"; build_gdb.build(r, RAW, gdb)
    assert validate.check_gdb(r, gdb) == ["p1: point is outside Louisiana (28.7, -91.5)"]

def test_check_links_classifies(monkeypatch):
    import validate
    class Resp:
        def __init__(self, code): self.status_code = code
    codes = {"https://ok": 200, "https://gone": 404, "https://blocked": 403}
    monkeypatch.setattr(validate.requests, "get", lambda u, **k: Resp(codes[u]))
    assert validate.check_links(list(codes)) == [
        ("https://gone", "broken (404)"), ("https://blocked", "check by hand (403)")]

def test_build_carries_landscape_notes_and_ecoregion_text(tmp_path):
    import arcpy, build_gdb
    nature = [{"table": "places", "row_id": "p1", "nature_note": "On Macon Ridge.", "sources": "NPS <https://example.org/n>"}]
    eco = [{"eco_id": "73", "name": "Mississippi Alluvial Plain", "description": "River bottomland.", "sources": "EPA"}]
    gdb = tmp_path / "t.gdb"
    counts = build_gdb.build(write_research(tmp_path / "r", nature=nature, ecoregions=eco), RAW, gdb)
    assert counts["nature"] == 1 and counts["ecoregions"] == 6
    rows = {c: d for c, d in arcpy.da.SearchCursor(str(gdb / "Base_Ecoregions"), ["eco_id", "description"])}
    assert rows["73"] == "River bottomland." and set(rows) == {"34", "35", "65", "73", "74", "75"}

def test_validate_flags_landscape_tables_out_of_step_with_research(tmp_path):
    import build_gdb, validate
    nature = [{"table": "places", "row_id": "p1", "nature_note": "On Macon Ridge.", "sources": "NPS <https://example.org/n>"}]
    gdb = tmp_path / "t.gdb"
    build_gdb.build(write_research(tmp_path / "r", nature=nature), RAW, gdb)
    assert validate.check_gdb(write_research(tmp_path / "r2"), gdb) == ["Nature: 1 built but 0 in research"]

def test_check_links_asks_youtube_whether_the_video_exists(monkeypatch):
    """A removed YouTube video still serves a normal watch page, so the checker must use oEmbed."""
    import validate
    class Resp:
        def __init__(self, code): self.status_code = code
    asked = []
    def fake_get(u, **k):
        asked.append(u)
        if "oembed" in u:
            return Resp(404 if "GONE" in u else 401 if "NOEMBED" in u else 200)
        return Resp(200)                      # every watch page "works"
    monkeypatch.setattr(validate.requests, "get", fake_get)
    urls = ["https://www.youtube.com/watch?v=LIVE", "https://www.youtube.com/watch?v=GONE",
            "https://youtu.be/NOEMBED", "https://example.org/page"]
    assert validate.check_links(urls) == [
        ("https://www.youtube.com/watch?v=GONE", "broken (video unavailable)"),
        ("https://youtu.be/NOEMBED", "check by hand (401)")]
    assert sum("oembed" in a for a in asked) == 3 and "https://example.org/page" in asked

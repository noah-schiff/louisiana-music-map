import json, re
from pathlib import Path
import pytest
from conftest import write_research, edited

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data_raw"
needs_data = pytest.mark.skipif(not (RAW / "cb_2023_us_county_500k").exists(), reason="base data not downloaded")

def test_round_coords_recurses():
    import export_web
    assert export_web.round_coords([[-91.123456, 30.987654], [[1.00004, 2.00006]]]) == [[-91.1235, 30.9877], [[1.0, 2.0001]]]

def test_embed_json_cannot_close_the_script_tag():
    import export_web
    nasty = {"t": 'He said "hi" </script><script>alert(1)</script> & <b>café</b> <!-- x'}
    text = export_web.embed_json(nasty)
    assert "</script" not in text.lower() and "<!--" not in text
    assert json.loads(text) == nasty

def test_render_single_pass_and_unknown_marker():
    import export_web
    out = export_web.render("a {{X}} b {{Y}}", {"X": "{{Y}}", "Y": "why"})
    assert out == "a {{Y}} b why"   # substituted text is not rescanned
    with pytest.raises(KeyError):
        export_web.render("{{NOPE}}", {})

@needs_data
def test_export_end_to_end(tmp_path):
    import build_gdb, export_web
    nature = [{"table": "places", "row_id": "p1", "nature_note": "On Macon Ridge.", "sources": "NPS <https://example.org/n>"}]
    eco = [{"eco_id": "73", "name": "Mississippi Alluvial Plain", "description": "River bottomland.", "sources": "EPA"}]
    r = write_research(tmp_path / "r", nature=nature, ecoregions=eco,
                       **edited("places", writeup='Quote " and </script> & <i>tag</i>'))
    gdb = tmp_path / "t.gdb"; build_gdb.build(r, RAW, gdb)
    web = tmp_path / "web"; (web / "src").mkdir(parents=True); (web / "vendor").mkdir()
    for rel in ("src/template.html", "src/app.js", "src/app.css", "src/core.js", "vendor/leaflet.js", "vendor/leaflet.css"):
        (web / rel).write_bytes((ROOT / "web" / rel).read_bytes())
    counts = export_web.export(gdb, web)
    assert counts == {"genres": 2, "eras": 2, "regions": 1, "places": 1}
    html = (web / "index.html").read_text(encoding="utf-8")
    assert len(re.findall(r"</script>", html)) == 4          # exactly the template's own four
    data = json.loads(re.search(r'<script id="lmm-data" type="application/json">(.*?)</script>', html, re.S).group(1))
    p = data["places"][0]
    assert p["writeup"] == 'Quote " and </script> & <i>tag</i>'
    assert (p["lat"], p["lon"], p["year_start"]) == (32.6367, -91.4069, -1700)
    assert data["genres"][1]["year_end"] is None
    reg = data["regions"]["features"][0]
    assert reg["geometry"]["type"] in ("Polygon", "MultiPolygon") and reg["properties"]["genre_id"] == "jazz"
    lon, lat = _first_coord(reg["geometry"]["coordinates"])
    assert -91 < lon < -89 and 29 < lat < 31                  # WGS 84 degrees, lon first
    assert len(data["base"]["parishes"]["features"]) == 64
    eco_feats = {f["properties"]["eco_id"]: f["properties"] for f in data["base"]["ecoregions"]["features"]}
    assert len(eco_feats) == 6 and eco_feats["73"]["description"] == "River bottomland."
    assert eco_feats["34"]["name"] == "Western Gulf Coastal Plain"      # name falls back to the EPA layer
    assert p["nature"] == {"note": "On Macon Ridge.", "sources": [{"label": "NPS", "url": "https://example.org/n"}]}
    assert data["genres"][0]["nature"] is None and reg["properties"]["nature"] is None
    assert len(html.encode("utf-8")) < 3_000_000

def _first_coord(c):
    while isinstance(c[0], list):
        c = c[0]
    return c

def test_split_template_makes_standalone_and_fragment():
    import export_web
    t = "<!--S--><!doctype html><head><!--/S--><title>T</title><!--S--></head><body><!--/S--><p>x</p><!--S--></body><!--/S-->"
    standalone, fragment = export_web.split_template(t)
    assert standalone == "<!doctype html><head><title>T</title></head><body><p>x</p></body>"
    assert fragment == "<title>T</title><p>x</p>"

@needs_data
def test_export_writes_artifact_fragment(tmp_path):
    import build_gdb, export_web
    gdb = tmp_path / "t.gdb"; build_gdb.build(write_research(tmp_path / "r"), RAW, gdb)
    web = tmp_path / "web"; (web / "src").mkdir(parents=True); (web / "vendor").mkdir()
    for rel in ("src/template.html", "src/app.js", "src/app.css", "src/core.js", "vendor/leaflet.js", "vendor/leaflet.css"):
        (web / rel).write_bytes((ROOT / "web" / rel).read_bytes())
    export_web.export(gdb, web)
    index = (web / "index.html").read_text(encoding="utf-8")
    frag = (web / "artifact.html").read_text(encoding="utf-8")
    assert index.lstrip().lower().startswith("<!doctype html>") and "</body>" in index
    assert not re.search(r"<!doctype|<html[\s>]|<head[\s>]|<body[\s>]|</body>|</html>", frag, re.I)
    assert frag.lstrip().startswith("<title>") and 'id="lmm-data"' in frag
    assert "<!--S-->" not in index and "<!--/S-->" not in index

def test_built_artifact_needs_nothing_from_outside_but_fonts():
    """Guard on the real output: the Claude artifact blocks outside scripts and images."""
    frag = (ROOT / "web" / "artifact.html")
    if not frag.exists():
        pytest.skip("web/artifact.html not built yet")
    html = re.sub(r'<script id="lmm-data".*?</script>', "", frag.read_text(encoding="utf-8"), flags=re.S)
    refs = re.findall(r'<(?:script|link|img|iframe|source|video|audio)\b[^>]*\b(?:src|href)="([^"]+)"', html)
    assert refs and all(r.startswith("https://fonts.googleapis.com/") for r in refs), refs

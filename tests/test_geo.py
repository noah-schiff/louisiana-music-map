import geo

def test_norm_parish_variants_collapse():
    same = ["St. Landry", "Saint Landry", "St Landry", "st. landry parish", " ST. LANDRY "]
    assert len({geo.norm_parish(n) for n in same}) == 1
    assert geo.norm_parish("La Salle") == geo.norm_parish("LaSalle")
    assert geo.norm_parish("De Soto Parish") == geo.norm_parish("DeSoto")
    assert geo.norm_parish("East Baton Rouge") != geo.norm_parish("West Baton Rouge")

def test_match_parishes_reports_unmatched_by_name():
    avail = {geo.norm_parish(n): n for n in ["St. Landry", "LaSalle", "Orleans"]}
    got, missing = geo.match_parishes(["Saint Landry", "La Salle", "Orlans"], avail)
    assert got == ["St. Landry", "LaSalle"] and missing == ["Orlans"]

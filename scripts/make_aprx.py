"""Create LouisianaMusic.aprx with one map holding every layer. Safe to re-run."""
from pathlib import Path
import arcpy

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT.parent / "Case 1.aprx"          # an existing blank project, opened read-only and copied
OUT = ROOT / "LouisianaMusic.aprx"
GDB = ROOT / "LouisianaMusic.gdb"
LAYERS = ["Base_State", "Base_Ecoregions", "Base_Lakes", "Base_Rivers", "Base_Parishes", "Base_Cities", "Regions", "Places"]  # bottom to top

def main():
    seed = arcpy.mp.ArcGISProject(str(SEED))
    seed.saveACopy(str(OUT)); del seed
    aprx = arcpy.mp.ArcGISProject(str(OUT))
    aprx.homeFolder, aprx.defaultGeodatabase = str(ROOT), str(GDB)
    for m in aprx.listMaps():
        aprx.deleteItem(m)
    m = aprx.createMap("Louisiana Music", "MAP")
    m.spatialReference = arcpy.SpatialReference(26915)
    for lyr in m.listLayers():
        m.removeLayer(lyr)                      # drop the default basemap
    layers = [n for n in LAYERS if arcpy.Exists(str(GDB / n))]     # natural regions are optional
    for name in layers:
        m.addDataFromPath(str(GDB / name))
    # Pro places new layers by geometry type (points over lines over polygons), so set the order explicitly.
    want = layers[::-1]
    for upper, lower in zip(want, want[1:]):
        m.moveLayer(m.listLayers(upper)[0], m.listLayers(lower)[0], "AFTER")
    for t in ("Genres", "Eras", "Nature"):
        if arcpy.Exists(str(GDB / t)):
            m.addDataFromPath(str(GDB / t))

    colors = {g: c for g, c in arcpy.da.SearchCursor(str(GDB / "Genres"), ["genre_id", "color"])}
    for lname in ("Regions", "Places"):
        lyr = m.listLayers(lname)[0]
        sym = lyr.symbology
        sym.updateRenderer("UniqueValueRenderer")
        sym.renderer.fields = ["genre_id"]
        for grp in sym.renderer.groups:
            for item in grp.items:
                h = colors[item.values[0][0]].lstrip("#")
                rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
                item.symbol.color = {"RGB": rgb + [45 if lname == "Regions" else 100]}
        lyr.symbology = sym

    for lyr in m.listLayers("Base_Ecoregions"):
        lyr.visible = False                    # natural regions: switch on in the Contents pane
    aprx.save()
    names = [l.name for l in m.listLayers()]
    broken = [l.name for l in m.listLayers() if l.isBroken]
    print("Layers (top to bottom):", names, "| tables:", [t.name for t in m.listTables()], "| broken:", broken)
    assert names == layers[::-1] and not broken

if __name__ == "__main__":
    main()

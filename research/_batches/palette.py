"""Measure and improve the genre palette.

    python palette.py measure     report how far apart the current genre colors are
    python palette.py choose      pick a better-separated set and save it to palette.json
    python palette.py apply       write the colors in palette.json into research\\genres.csv

Distance is OKLab delta-E x 100 (about 2 is just noticeable; under 8 is hard to tell apart as map
symbols), taken as the worst of normal vision, deuteranopia and protanopia (Machado et al. 2009).
Colors must also stand out from the land color in both themes.
"""
import csv, itertools, json, math, sys
from pathlib import Path

here = Path(__file__).resolve().parent
GENRES = here.parent / "genres.csv"
SAVED = here / "palette.json"
LAND = {"light": "#dfe6dd", "dark": "#1f2d2a"}
CVD = {
    "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
}

def hex_rgb(h):
    h = h.lstrip("#"); return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
def rgb_hex(c):
    return "#" + "".join(f"{round(max(0, min(1, v)) * 255):02x}" for v in c)
def lin(v): return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
def unlin(v): return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055

def oklab(rgb_lin):
    r, g, b = rgb_lin
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)

def oklch_to_rgb(L, C, h):
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s]

def views(hexcolor):
    """OKLab coordinates of a color as seen with normal vision and two kinds of color blindness."""
    rl = [lin(v) for v in hex_rgb(hexcolor)]
    out = [oklab(rl)]
    for m in CVD.values():
        out.append(oklab([max(0, min(1, sum(m[i][j] * rl[j] for j in range(3)))) for i in range(3)]))
    return out

def dist(va, vb):
    return min(100 * math.dist(a, b) for a, b in zip(va, vb))

def contrast(h1, h2):
    def lum(h):
        r, g, b = (lin(v) for v in hex_rgb(h)); return 0.2126 * r + 0.7152 * g + 0.0722 * b
    a, b = sorted((lum(h1), lum(h2)), reverse=True)
    return (a + 0.05) / (b + 0.05)

def read_genres():
    with open(GENRES, newline="", encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh); return rd.fieldnames, list(rd)

def report(colors, title):
    v = {g: views(c) for g, c in colors.items()}
    pairs = sorted((dist(v[a], v[b]), a, b) for a, b in itertools.combinations(colors, 2))
    land = {g: min(contrast(c, l) for l in LAND.values()) for g, c in colors.items()}
    print(f"\n{title}")
    print(f"  closest pair: {pairs[0][0]:.1f}  |  pairs under 8: {sum(1 for p in pairs if p[0] < 8)} of {len(pairs)}"
          f"  |  median: {pairs[len(pairs) // 2][0]:.1f}")
    print("  five closest:", "; ".join(f"{a}/{b} {d:.1f}" for d, a, b in pairs[:5]))
    weak = sorted(land.items(), key=lambda kv: kv[1])[:3]
    print("  weakest contrast with the land (worse theme):", "; ".join(f"{g} {r:.2f}" for g, r in weak))
    return pairs[0][0]

def choose(n, old):
    pool = []
    for L in (0.42, 0.50, 0.58, 0.66, 0.74):
        for C in (0.07, 0.11, 0.15, 0.19, 0.23):
            for h in range(0, 360, 12):
                rl = oklch_to_rgb(L, C, h)
                if all(-1e-6 <= x <= 1 + 1e-6 for x in rl):
                    hx = rgb_hex([unlin(max(0, x)) for x in rl])
                    if min(contrast(hx, l) for l in LAND.values()) >= 1.9:
                        pool.append(hx)
    pool = sorted(set(pool))
    pv = {c: views(c) for c in pool}
    best, best_score = None, -1
    for seed in pool[:: max(1, len(pool) // 40)]:           # farthest-point selection from several seeds
        chosen = [seed]
        near = {c: dist(pv[c], pv[seed]) for c in pool}
        while len(chosen) < n:
            nxt = max(pool, key=lambda c: near[c])
            chosen.append(nxt)
            for c in pool:
                near[c] = min(near[c], dist(pv[c], pv[nxt]))
        score = min(dist(pv[a], pv[b]) for a, b in itertools.combinations(chosen, 2))
        if score > best_score:
            best, best_score = chosen, score
    # Give each genre the new color nearest its old one (normal vision), greedily by closest match first,
    # so familiar associations (green Cajun, blue jazz) survive where they can.
    ov = {g: views(c)[0] for g, c in old.items()}
    cand = sorted((100 * math.dist(ov[g], pv[c][0]), g, c) for g in old for c in best)
    out, used = {}, set()
    for _, g, c in cand:
        if g not in out and c not in used:
            out[g] = c; used.add(c)
    return out, len(pool)

# Twenty hues cannot all be told apart, so each family of genres also gets its own marker shape
# (the same table lives in web/src/app.js as SHAPES). Colors only have to be distinct WITHIN a family.
FAMILIES = {
    "circle":        ["ancient", "native", "colonial", "congo", "creole"],
    "diamond":       ["cajun", "zydeco", "swamp_pop"],
    "square":        ["jazz", "brass", "mardigras_indian", "marching"],
    "triangle":      ["gospel", "classical"],
    "triangle-down": ["blues", "country"],
    "hexagon":       ["rnb", "funk", "bounce", "hiphop"],
}

def family_report(colors, title):
    v = {g: views(c) for g, c in colors.items()}
    worst = []
    for shape, gs in FAMILIES.items():
        gs = [g for g in gs if g in colors]
        d = [(dist(v[a], v[b]), a, b) for a, b in itertools.combinations(gs, 2)]
        if d:
            worst.append((min(d), shape))
    print(f"\n{title}: closest pair that shares a shape")
    for (d, a, b), shape in sorted(worst):
        print(f"  {shape:14s} {a}/{b} {d:.1f}")
    unplaced = [g for g in colors if not any(g in gs for gs in FAMILIES.values())]
    if unplaced:
        print("  genres with no family (drawn as circles):", unplaced)
    return min(w[0][0] for w in worst)

def choose_grouped(old):
    """Within each family pick well-separated colors, each as near its old color as that allows."""
    pool = []
    for L in (0.46, 0.54, 0.62, 0.70):
        for C in (0.09, 0.13, 0.17, 0.21):
            for h in range(0, 360, 10):
                rl = oklch_to_rgb(L, C, h)
                if all(-1e-6 <= x <= 1 + 1e-6 for x in rl):
                    hx = rgb_hex([unlin(max(0, x)) for x in rl])
                    if min(contrast(hx, l) for l in LAND.values()) >= 2.0:
                        pool.append(hx)
    pool = sorted(set(pool))
    pv = {c: views(c) for c in pool}
    out = {}
    for shape, gs in FAMILIES.items():
        gs = [g for g in gs if g in old]
        ov = {g: views(old[g])[0] for g in gs}
        best, best_key = None, None
        # Try every assignment of "nearest few" candidates per genre and keep the best-separated one.
        near = {g: sorted(pool, key=lambda c: math.dist(ov[g], pv[c][0]))[:14] for g in gs}
        for combo in itertools.product(*(near[g] for g in gs)):
            if len(set(combo)) < len(combo):
                continue
            sep = min((dist(pv[a], pv[b]) for a, b in itertools.combinations(combo, 2)), default=99)
            drift = sum(100 * math.dist(ov[g], pv[c][0]) for g, c in zip(gs, combo))
            key = (min(sep, 20), -drift)          # separation up to "clearly different", then stay close to the old color
            if best_key is None or key > best_key:
                best, best_key = combo, key
        out.update(dict(zip(gs, best)))
    for g in old:                                  # a genre outside every family keeps its color
        out.setdefault(g, old[g])
    return out

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "measure"
    cols, rows = read_genres()
    current = {r["genre_id"]: r["color"] for r in rows}
    if mode == "spread":
        # Per family: start from the color nearest the first genre's old color, add the farthest-apart
        # colors (worst case over normal and color-blind vision), then hand them out so each genre
        # lands as near its old color as possible.
        pool = []
        for L in (0.36, 0.44, 0.52, 0.60, 0.68, 0.76, 0.84):
            for C in (0.06, 0.10, 0.14, 0.18, 0.22):
                for h in range(0, 360, 10):
                    rl = oklch_to_rgb(L, C, h)
                    if all(-1e-6 <= x <= 1 + 1e-6 for x in rl):
                        hx = rgb_hex([unlin(max(0, x)) for x in rl])
                        if min(contrast(hx, l) for l in LAND.values()) >= 1.6:
                            pool.append(hx)
        pool = sorted(set(pool)); pv = {c: views(c) for c in pool}
        new = {}
        for shape, gs in FAMILIES.items():
            gs = [g for g in gs if g in current]
            ov = {g: views(current[g])[0] for g in gs}
            best, best_sep = None, -1
            for g0 in gs:                                    # try each genre's old color as the anchor
                seed = min(pool, key=lambda c: math.dist(ov[g0], pv[c][0]))
                chosen, near = [seed], {c: dist(pv[c], pv[seed]) for c in pool}
                while len(chosen) < len(gs):
                    nxt = max(pool, key=lambda c: near[c]); chosen.append(nxt)
                    for c in pool:
                        near[c] = min(near[c], dist(pv[c], pv[nxt]))
                sep = min((dist(pv[a], pv[b]) for a, b in itertools.combinations(chosen, 2)), default=99)
                if sep > best_sep:
                    best, best_sep = chosen, sep
            perm = min(itertools.permutations(best),
                       key=lambda p: sum(math.dist(ov[g], pv[c][0]) for g, c in zip(gs, p)))
            new.update(dict(zip(gs, perm)))
        # Now pull each color back toward its old one as far as possible while every same-shape
        # pair stays at least TARGET apart: clearly different, without scrambling associations.
        TARGET = float(sys.argv[2]) if len(sys.argv) > 2 else 12.0
        for shape, gs in FAMILIES.items():
            gs = [g for g in gs if g in current]
            ov = {g: views(current[g])[0] for g in gs}
            for _ in range(4):
                for g in gs:
                    others = [new[o] for o in gs if o != g]
                    for c in sorted(pool, key=lambda c: math.dist(ov[g], pv[c][0])):
                        if c not in others and all(dist(pv[c], pv[o]) >= TARGET for o in others):
                            new[g] = c; break
        for g in current:
            new.setdefault(g, current[g])
        report(current, f"Current palette ({len(current)} genres)")
        b = family_report(current, "Current")
        a = family_report(new, "Proposed (spread within each shape family)")
        land = sorted(((min(contrast(c, l) for l in LAND.values()), g) for g, c in new.items()))[:3]
        print("  weakest contrast with the land:", "; ".join(f"{g} {r:.2f}" for r, g in land))
        SAVED.write_text(json.dumps(new, indent=1), encoding="utf-8")
        print(f"\nclosest same-shape pair {b:.1f} -> {a:.1f}; saved to {SAVED.name}")
        for shape, gs in FAMILIES.items():
            print(f"  {shape:14s}", "  ".join(f"{g} {new[g]}" for g in gs))
    elif mode == "manual":
        # Hand-assigned from the Okabe-Ito colour-blind-safe set (plus a dark neutral and a wine),
        # so that no two genres sharing a marker shape are close, and familiar associations
        # (green Cajun, blue jazz and blues, rust Native nations) mostly survive.
        new = {
            "ancient": "#5a5246", "native": "#d55e00", "colonial": "#0072b2", "congo": "#e69f00", "creole": "#cc79a7",
            "cajun": "#009e73", "zydeco": "#c2407a", "swamp_pop": "#3fa7dc",
            "jazz": "#0072b2", "brass": "#e69f00", "mardigras_indian": "#cc79a7", "marching": "#009e73",
            "gospel": "#009e73", "classical": "#882255",
            "blues": "#0072b2", "country": "#d55e00",
            "rnb": "#d55e00", "funk": "#0072b2", "bounce": "#cc79a7", "hiphop": "#444b55",
        }
        for g in current:
            new.setdefault(g, current[g])
        report(current, f"Current palette ({len(current)} genres)")
        b = family_report(current, "Current")
        a = family_report(new, "Proposed (manual, by shape family)")
        land = sorted(((min(contrast(c, l) for l in LAND.values()), g) for g, c in new.items()))[:3]
        print("  weakest contrast with the land:", "; ".join(f"{g} {r:.2f}" for r, g in land))
        SAVED.write_text(json.dumps(new, indent=1), encoding="utf-8")
        print(f"\nclosest same-shape pair {b:.1f} -> {a:.1f}; saved to {SAVED.name}")
    elif mode == "grouped":
        report(current, f"Current palette ({len(current)} genres)")
        b = family_report(current, "Current")
        new = choose_grouped(current)
        report(new, "Proposed palette")
        a = family_report(new, "Proposed")
        SAVED.write_text(json.dumps(new, indent=1), encoding="utf-8")
        print(f"\nclosest same-shape pair {b:.1f} -> {a:.1f}; saved to {SAVED.name}")
        print("; ".join(f"{g} {current[g]}->{c}" for g, c in new.items() if current[g] != c))
    elif mode == "measure":
        report(current, f"Current palette ({len(current)} genres)")
        family_report(current, "Current")
    elif mode == "choose":
        before = report(current, f"Current palette ({len(current)} genres)")
        new, pool = choose(len(current), current)
        after = report(new, f"Proposed palette (chosen from {pool} candidates)")
        SAVED.write_text(json.dumps(new, indent=1), encoding="utf-8")
        print(f"\nclosest pair {before:.1f} -> {after:.1f}; saved to {SAVED.name}")
        print("; ".join(f"{g} {current[g]}->{c}" for g, c in new.items()))
    elif mode == "apply":
        new = json.loads(SAVED.read_text(encoding="utf-8"))
        missing = [g for g in current if g not in new]
        if missing:
            print(f"NOTE: palette.json has no color for {missing}; they keep their current color. "
                  f"Add them to FAMILIES here and SHAPES in web/src/app.js, then run 'spread'.")
        for r in rows:
            r["color"] = new.get(r["genre_id"], r["color"])
            new[r["genre_id"]] = r["color"]
        with open(GENRES, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_ALL); w.writeheader(); w.writerows(rows)
        report(new, "Applied palette")

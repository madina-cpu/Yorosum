"""Generate Yorosum logo SVGs with outlined type.

Usage: python3 -I gen.py <fonts_dir> <out_dir>
"""
import math, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

BERRY, GOLD, BONE, ROSE, BLACK = "#8E2149", "#B08A62", "#FBF8F3", "#F0D5DD", "#1A1416"

# ---------------------------------------------------------------- type
def outline(font_path, text, size, tracking_em=0.0, kern=None):
    """Return (path_d, width) for text set at `size` px, baseline y=0."""
    f = TTFont(font_path)
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    s = size / upm
    pen = SVGPathPen(gs)
    x = 0.0
    for i, ch in enumerate(text):
        g = cmap[ord(ch)]
        tp = TransformPen(pen, (s, 0, 0, -s, x, 0))
        gs[g].draw(tp)
        x += gs[g].width * s
        if i < len(text) - 1:
            x += tracking_em * size + (kern or {}).get(text[i:i + 2], 0) * size
    return pen.getCommands(), x


# ---------------------------------------------------------------- mark
def arc_pts(d, r, a):
    """Point on an arc that crosses the axis at x=d, radius r, centre (d - r, 0)."""
    return (d - r + r * math.cos(math.radians(a)), -r * math.sin(math.radians(a)))


def arc(d, r, a0, a1, w, color):
    """Arc from angle a0 to a1 about its own centre (degrees, 0 = right, +ve = up)."""
    p0, p1 = arc_pts(d, r, a0), arc_pts(d, r, a1)
    large = 1 if (a1 - a0) > 180 else 0
    return (f'<path d="M{p0[0]:.2f} {p0[1]:.2f} A{r} {r} 0 {large} 0 {p1[0]:.2f} {p1[1]:.2f}" '
            f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')


# Dot + two arcs with equal optical gaps on the axis:
#   gap = d_inner - w/2 - dot = d_outer - d_inner - w
# Each arc's centre sits behind the dot (radius = d × flat), so the arcs read as
# open parentheses — breath — rather than concentric signal waves.
CUTS = {
    # A — Refined Breath: mirror-symmetric about the horizontal axis.
    "A": dict(dot=9, w=7, gap=11.5, flat=(1.3, 1.15), inner=(-50, 50), outer=(-52, 52)),
    # B — Rising Exhale: the sweep runs longer above the axis — breath lifting out.
    "B": dict(dot=9, w=7, gap=11.5, flat=(1.3, 1.15), inner=(-40, 58), outer=(-42, 62)),
    # B-small — optical cut of B for 16–32 px and sub-8 mm print.
    "Bs": dict(dot=10.5, w=9, gap=10, flat=(1.3, 1.15), inner=(-42, 56), outer=(-42, 58)),
}


def mark_geom(cut):
    c = CUTS[cut]
    di = c["dot"] + c["gap"] + c["w"] / 2
    do = di + c["w"] + c["gap"]
    return c, (di, di * c["flat"][0], c["inner"]), (do, do * c["flat"][1], c["outer"])


def mark(cut, dot_c, inner_c, outer_c):
    c, (di, ri, ai), (do, ro, ao) = mark_geom(cut)
    return (f'<circle cx="0" cy="0" r="{c["dot"]}" fill="{dot_c}"/>'
            + arc(di, ri, *ai, c["w"], inner_c)
            + arc(do, ro, *ao, c["w"], outer_c))


def mark_bbox(cut):
    c, inner, outer = mark_geom(cut)
    hw = c["w"] / 2
    ys = [c["dot"], -c["dot"]]
    xs = [-c["dot"]]
    for d, r, (a0, a1) in (inner, outer):
        for a in (a0, a1):
            x, y = arc_pts(d, r, a)
            xs.append(x - hw)
            ys += [y - hw, y + hw]
        xs.append(d + hw)  # arc crosses 0°
    return min(xs), min(ys), max(xs), max(ys)


PALETTES = {
    "primary":   dict(bg=None,  dot=BERRY, inner=BERRY, outer=GOLD, word=BERRY, sub=BERRY),
    "reversed":  dict(bg=BERRY, dot=BONE,  inner=BONE,  outer=GOLD, word=BONE,  sub=BONE),
    "mono":      dict(bg=None,  dot=BERRY, inner=BERRY, outer=BERRY, word=BERRY, sub=BERRY),
    "black":     dict(bg=None,  dot=BLACK, inner=BLACK, outer=BLACK, word=BLACK, sub=BLACK),
    "white":     dict(bg=BLACK, dot="#FFFFFF", inner="#FFFFFF", outer="#FFFFFF", word="#FFFFFF", sub="#FFFFFF"),
}

# Wordmark: tracking tightened from ~0.19em to 0.12em; manual pair kerning for the
# round/diagonal letters so the rhythm reads even. Reversed drops to weight 700 to
# offset irradiation (light type on dark looks heavier).
KERN = {"YO": -0.015, "RO": -0.01, "OS": 0.005, "UM": -0.005}
CAP = 0.703  # Schibsted cap height / em (1440/2048)


def wordmark(weight, size):
    return outline(os.path.join(FONTS, f"sg{weight}.ttf"), "YOROSUM", size, 0.12, KERN)


def subline(size, tracking_em):
    return outline(os.path.join(FONTS, "Pretendard-Regular.otf"), "여러숨", size, tracking_em)


def svg(w, h, body, bg=None, label=""):
    rect = f'<rect width="{w:.1f}" height="{h:.1f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{label}">{rect}{body}</svg>\n')


def lockup_h(cut, pal, sub=True):
    p = PALETTES[pal]
    weight = 700 if pal in ("reversed", "white") else 800
    size = 56
    cap = CAP * size
    wd, ww = wordmark(weight, size)
    x0, y0, x1, y1 = mark_bbox(cut)
    mh = y1 - y0
    scale = (cap * 1.6) / mh             # mark is 1.6 × cap height
    pad = CUTS[cut]["dot"] * 2 * scale    # clearspace = dot diameter
    gap = cap * 0.62
    mx = pad - x0 * scale
    text_x = pad + (x1 - x0) * scale + gap
    if sub:
        sd, sw = subline(size * 0.34, 0.55)
        block_h = cap + size * 0.30 + size * 0.34 * 0.74
    else:
        block_h = cap
    # The mark centres on the cap height, so the dot sits on the wordmark's optical axis;
    # the sub-line hangs below. Canvas grows to hold whichever reaches further.
    cy = (y0 + y1) / 2 * scale
    above = max(cap / 2, mh * scale / 2)
    below = max(block_h - cap / 2, mh * scale / 2)
    h = above + below + 2 * pad
    base = pad + above + cap / 2
    my = base - cap / 2 - cy
    body = f'<g transform="translate({mx:.2f} {my:.2f}) scale({scale:.4f})">{mark(cut, p["dot"], p["inner"], p["outer"])}</g>'
    body += f'<path transform="translate({text_x:.2f} {base:.2f})" d="{wd}" fill="{p["word"]}"/>'
    if sub:
        sb = base + size * 0.30 + size * 0.34 * 0.74
        body += f'<path transform="translate({text_x + 2:.2f} {sb:.2f})" d="{sd}" fill="{p["sub"]}" opacity="0.85"/>'
    w = text_x + ww + pad
    return svg(w, h, body, p["bg"], "YOROSUM 여러숨")


def lockup_v(cut, pal):
    p = PALETTES[pal]
    weight = 700 if pal in ("reversed", "white") else 800
    size = 48
    cap = CAP * size
    wd, ww = wordmark(weight, size)
    sd, sw = subline(size * 0.36, 0.55)
    x0, y0, x1, y1 = mark_bbox(cut)
    scale = (cap * 2.3) / (y1 - y0)
    pad = CUTS[cut]["dot"] * 2 * scale
    w = ww + 2 * pad
    # centre the mark's visual mass (dot-to-outer-arc span) over the wordmark
    mw = (x1 - x0) * scale
    mx = (w - mw) / 2 - x0 * scale
    my = pad - y0 * scale
    base = pad + (y1 - y0) * scale + cap * 0.85 + cap
    sb = base + size * 0.62
    body = f'<g transform="translate({mx:.2f} {my:.2f}) scale({scale:.4f})">{mark(cut, p["dot"], p["inner"], p["outer"])}</g>'
    body += f'<path transform="translate({pad:.2f} {base:.2f})" d="{wd}" fill="{p["word"]}"/>'
    body += f'<path transform="translate({(w - sw) / 2:.2f} {sb:.2f})" d="{sd}" fill="{p["sub"]}" opacity="0.85"/>'
    h = sb + pad
    return svg(w, h, body, p["bg"], "YOROSUM 여러숨")


def mark_only(cut, pal, box=None):
    p = PALETTES[pal]
    x0, y0, x1, y1 = mark_bbox(cut)
    pad = CUTS[cut]["dot"]
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    side = max(w, h)
    tx = (side - (x1 - x0)) / 2 - x0
    ty = (side - (y1 - y0)) / 2 - y0
    body = f'<g transform="translate({tx:.2f} {ty:.2f})">{mark(cut, p["dot"], p["inner"], p["outer"])}</g>'
    return svg(side, side, body, p["bg"], "YOROSUM mark")


def app_icon(cut):
    x0, y0, x1, y1 = mark_bbox(cut)
    side = 512
    s = side * 0.56 / max(x1 - x0, y1 - y0)
    tx = (side - (x1 - x0) * s) / 2 - x0 * s
    ty = (side - (y1 - y0) * s) / 2 - y0 * s
    body = (f'<rect width="512" height="512" rx="112" fill="{ROSE}"/>'
            f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{mark(cut, BERRY, BERRY, GOLD)}</g>')
    return svg(side, side, body, None, "YOROSUM app icon")


files = {}
for cut in ("A", "B"):
    for pal in ("primary", "reversed", "mono", "black", "white"):
        files[f"concept-{cut}/yorosum-lockup-horizontal-{pal}.svg"] = lockup_h(cut, pal)
    for pal in ("primary", "reversed", "mono"):
        files[f"concept-{cut}/yorosum-lockup-stacked-{pal}.svg"] = lockup_v(cut, pal)
        files[f"concept-{cut}/yorosum-mark-{pal}.svg"] = mark_only(cut, pal)
    files[f"concept-{cut}/yorosum-wordmark-only-primary.svg"] = lockup_h(cut, "primary", sub=False)
for pal in ("primary", "reversed", "mono", "black"):
    files[f"concept-B/small/yorosum-mark-small-{pal}.svg"] = mark_only("Bs", pal)
files["concept-B/yorosum-app-icon.svg"] = app_icon("Bs")

for name, s in files.items():
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(s)
print(len(files), "files")

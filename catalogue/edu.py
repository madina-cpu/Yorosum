"""Five-page educational catalogue for phones: 390 × 844 pages, EN / RU / UZ.

    python3 catalogue/edu.py

Writes catalogue/out/yorosum-guide-<lang>.pdf (en, ru, uz) and yorosum-guide-all-languages.pdf
(opens with a language chooser; clickable flags top-left on every page).
Copy comes from catalogue/edu_i18n.json; fonts, logo and SNS icons are shared with build.py.

Every size and gap comes from the rule set at the top of E_CSS:
type scale (display 32 · title 26 · label 20 · lead/body 15 · small 13 · caption 12 · eyebrow 11),
spacing scale 4 · 8 · 12 · 16 · 24 · 32, side margin 28, content box 84 → 780.
"""
import json
import math
import os
import re
import subprocess

from build import BUILD, CHANNEL_URLS, CSS, FLAG, ICONS, LOGO, MARK, OUT, ROOT

FONTS = CSS.split("/* yorosum.com tokens */")[0]
STORE = "https://yorosum.com/QR_landing_page_links/"
PAGES = 5
NB = " "

E_CSS = r"""
:root { --bone: #FBF8F3; --rose: #F0D5DD; --blush: #F6E6EA; --berry: #8E2149; --wine: #5E1530; --ink: #2B1A20; --mute: #7C6670;
  --gold: #B08A62; --line: rgba(142, 33, 73, .16); --white: #FFFFFF;
  --sans: "Pretendard Variable", "Apple SD Gothic Neo", sans-serif; --serif: YSerif, "Pretendard Variable", serif;
  /* spacing scale */ --s1: 4px; --s2: 8px; --s3: 12px; --s4: 16px; --s5: 24px; --s6: 32px;
  --pad: 28px; --top: 84px; --foot: 64px; }
@page { size: 390px 844px; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #E9E3DE; }
body { font-family: var(--sans); color: var(--ink); -webkit-font-smoothing: antialiased; word-break: keep-all; overflow-wrap: break-word;
  font-synthesis: none; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
img, svg { display: block; }
em { font-style: normal; }
a { color: inherit; text-decoration: none; }
ul { list-style: none; }

.pg { position: relative; width: 390px; height: 844px; overflow: hidden; background: var(--bone); break-before: page; }
body > .pg:first-child { break-before: auto; }
@media screen { .pg { margin: 0 auto var(--s5); } body { padding: var(--s5) 0; } }
.pg .in { position: absolute; left: var(--pad); right: var(--pad); top: var(--top); bottom: var(--foot); display: flex; flex-direction: column; }

/* ---- type scale (always prefixed with .pg so no reset can override it) ---- */
.pg .t-display { font: 500 32px/1.12 var(--sans); letter-spacing: -.03em; color: var(--ink); }
.pg .t-display em { font: italic 400 1.14em/1 var(--serif); letter-spacing: 0; color: var(--berry); }
.pg .t-title { font: 500 26px/1.25 var(--sans); letter-spacing: -.02em; color: var(--ink); text-wrap: balance; }
.pg .t-label { font: italic 500 20px/1.1 var(--serif); color: var(--berry); }
.pg .t-eb { font: 600 11px/1.4 var(--sans); letter-spacing: .2em; text-transform: uppercase; color: var(--gold); }
.pg .t-lead { font: 400 15px/1.6 var(--sans); color: var(--mute); }
.pg .t-body { font: 400 15px/1.6 var(--sans); color: var(--ink); }
.pg .t-body b { font-weight: 600; color: var(--berry); }
.pg .t-small { font: 500 13px/1.45 var(--sans); color: var(--ink); }
.pg .t-cap { font: 400 12px/1.5 var(--sans); color: var(--mute); }
.pg .t-cap b { font-weight: 600; color: var(--ink); }
.pg .t-sub { font: 600 13px/1.3 var(--sans); letter-spacing: .08em; color: var(--berry); }
.pg .t-fig { font: 400 44px/1 var(--serif); color: var(--berry); white-space: nowrap; }
.pg .t-fig small { font: 500 15px/1 var(--sans); color: var(--ink); margin-left: var(--s1); }
.pg .t-val { font: 400 18px/1 var(--serif); color: var(--berry); white-space: nowrap; }
.nw { white-space: nowrap; }
.pg .t-inc { font: 500 12px/1 var(--sans); color: var(--mute); white-space: nowrap; }

/* ---- spacing rules: label →8→ title →12→ lead →24→ figure →24→ points ---- */
.pg .gap-8 { margin-top: var(--s2); }
.pg .gap-12 { margin-top: var(--s3); }
.pg .gap-24 { margin-top: var(--s5); }

/* top bar and folio */
.bar { position: absolute; z-index: 4; top: 26px; left: var(--pad); }
.bar svg { width: 26px; height: 25px; }
.pn { position: absolute; left: var(--pad); right: var(--pad); bottom: 26px; display: flex; justify-content: space-between; align-items: baseline;
  font: 600 9px/1 var(--sans); letter-spacing: .16em; text-transform: uppercase; color: var(--mute); }
.pn i { font: italic 400 14px/1 var(--serif); letter-spacing: 0; color: var(--berry); text-transform: none; }
.switch { position: absolute; z-index: 5; top: 26px; left: var(--pad); display: flex; gap: var(--s3); }
.switch a { display: block; width: 30px; height: 22px; border-radius: 4px; overflow: hidden; box-shadow: 0 1px 5px rgba(43, 26, 32, .22); }
.switch a.on { box-shadow: 0 0 0 2px var(--bone), 0 0 0 3.5px var(--berry); }
.switch img { width: 100%; height: 100%; object-fit: cover; }

/* figure card: one per education page */
.pg .card { background: var(--blush); border-radius: 12px; padding: 20px; flex: 1 1 auto; display: flex; flex-direction: column; justify-content: center; }

/* points */
.pg .pts { display: flex; flex-direction: column; gap: var(--s3); }
.pg .pts li { position: relative; padding-left: 20px; }
.pg .pts li::before { content: ""; position: absolute; left: 2px; top: 9px; width: 6px; height: 6px; border-radius: 50%; background: var(--berry); }

/* 1 cover */
.cover { display: flex; flex-direction: column; }
.cover .photo { position: relative; flex: 1 1 auto; min-height: 220px; overflow: hidden; }
.cover .photo img { width: 100%; height: 100%; object-fit: cover; object-position: 80% 50%; }
.cover .photo::after { content: ""; position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(251, 248, 243, .7) 0%, rgba(251, 248, 243, 0) 34%, rgba(251, 248, 243, 0) 78%, var(--bone) 100%); }
.cover .logo { position: absolute; z-index: 3; top: 26px; left: var(--pad); width: 140px; height: auto; }
.with-switch .cover .logo { top: 72px; }
.cover .body { flex: none; padding: var(--s5) var(--pad) var(--foot); display: flex; flex-direction: column; }
.pg .facts { border-top: 1px solid var(--line); }
.pg .fact { display: grid; grid-template-columns: 132px minmax(0, 1fr); gap: var(--s4); align-items: center; padding: var(--s3) 0; border-bottom: 1px solid var(--line); }
.pg .chips { display: flex; flex-wrap: wrap; gap: var(--s2); }
.pg .chip { font: 500 12px/1 var(--sans); padding: var(--s2) var(--s3); border-radius: 99px; background: var(--blush); color: var(--wine); }

/* 2 body areas */
.pg .areas { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--s4); }
.pg .area { display: flex; flex-direction: column; align-items: center; gap: var(--s2); text-align: center; }
.pg .area .ic { width: 72px; height: 72px; border-radius: 50%; background: var(--white); display: flex; align-items: center; justify-content: center; }
.pg .area .ic svg { width: 44px; height: 44px; }
.pg .area p { font: 600 13px/1.45 var(--sans); color: var(--ink); }

/* 3 absorption */
.pg .zones { display: flex; flex-direction: column; }
.pg .zone { display: grid; grid-template-columns: 76px minmax(0, 1fr); gap: var(--s3); align-items: center; }
.pg .zone p { font: 600 11px/1.3 var(--sans); color: var(--mute); }
.pg .zone svg { width: 100%; height: auto; }
.pg .legend { display: flex; flex-direction: column; gap: var(--s3); margin-top: var(--s4); padding-top: var(--s4); border-top: 1px solid var(--line); }
.pg .legend li { display: grid; grid-template-columns: 76px minmax(0, 1fr); gap: var(--s3); align-items: center; }
.pg .legend svg { width: 76px; height: 14px; }

/* 4 vitamin C */
.pg .eq { display: grid; grid-template-columns: minmax(0, 1fr) 20px minmax(0, 1fr) 20px minmax(0, 1fr); gap: var(--s1); align-items: start; }
.pg .eq > div { display: flex; flex-direction: column; align-items: center; gap: var(--s2); text-align: center; }
.pg .eq svg { width: 80px; height: 80px; }
.pg .eq .op { height: 80px; display: flex; align-items: center; justify-content: center; font: 400 24px/1 var(--serif); color: var(--mute); }
.pg .eq p { font: 600 12px/1.4 var(--sans); color: var(--ink); }
.pg .dv { margin-top: var(--s5); padding-top: var(--s5); border-top: 1px solid var(--line); }
.pg .dv-h { display: flex; justify-content: space-between; align-items: baseline; gap: var(--s3); }
.pg .dv-bar { height: 10px; margin-top: var(--s3); border-radius: 10px; background: linear-gradient(90deg, #C9708E, var(--berry)); }
.pg .dv-s { display: flex; justify-content: space-between; margin-top: var(--s2); }

/* 5 how to take, ingredients, wholesale, store */
.pg .how { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--s3); }
.pg .how > div { display: flex; flex-direction: column; align-items: center; gap: var(--s2); text-align: center; }
.pg .how .ic { width: 40px; height: 40px; border-radius: 50%; background: var(--blush); display: flex; align-items: center; justify-content: center; }
.pg .how .ic svg { width: 24px; height: 24px; }
.pg .how p { font: 600 12px/1.4 var(--sans); color: var(--ink); }
.pg .tbl { border-top: 1px solid var(--line); }
.pg .row { display: flex; justify-content: space-between; align-items: center; gap: var(--s3); min-height: 32px; padding: 6px 0; border-bottom: 1px solid var(--line); }
.pg .row .t-small { min-width: 0; }
.pg .row .t-val { font-size: 16px; }
.pg .end { display: grid; grid-template-columns: 68px minmax(0, 1fr); gap: var(--s4); align-items: center; }
.pg .end .qr img { width: 68px; height: 68px; }
.pg .end-r { display: flex; flex-direction: column; gap: var(--s2); }
.pg .sns { display: flex; gap: var(--s3); }
.pg .sns svg { width: 28px; height: 28px; }

/* chooser (all-languages file) */
.pick .photo { flex: none; height: 440px; }
.pick .body { flex: 1 1 auto; }
.pg .langs { display: flex; flex-direction: column; gap: var(--s3); }
.pg .lang { display: flex; align-items: center; gap: var(--s4); height: 60px; padding: 0 var(--s5) 0 var(--s4); border-radius: 12px; background: var(--white); border: 1px solid var(--line); }
.pg .lang img { width: 36px; height: 27px; border-radius: 4px; object-fit: cover; box-shadow: 0 2px 6px rgba(43, 26, 32, .16); }
.pg .lang b { display: block; font: 600 15px/1.3 var(--sans); color: var(--ink); }
.pg .lang small { display: block; font: 400 12px/1.5 var(--sans); color: var(--mute); }
.pg .lang .go { margin-left: auto; font: 400 20px/1 var(--serif); color: var(--berry); }
"""


def tidy(s):
    """Keep numbers and their units on one line: 2 000 · 300 Da · 10–12."""
    s = re.sub(r"(\d) (?=\d{3}\b)", r"\1" + NB, s)
    s = re.sub(r"(\d) (?=(mg|мг|Da|Да|g|г|kg|кг|cm|см|sm|×)(?![\w]))", r"\1" + NB, s)
    s = re.sub(r"× (?=\d)", "×" + NB, s)
    s = re.sub(r"(\d[\d\u00a0]*–\d[\d\u00a0]*(?:\u00a0(?:Da|Да))?)", r'<span class="nw">\1</span>', s)
    return s


# ---------- illustrations ----------
SV = 'fill="none" stroke="#8E2149" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'

AREA_ICONS = [
    # skin: three layers
    f'<svg viewBox="0 0 48 48" {SV}><path d="M6 15c4-4 8-4 12 0s8 4 12 0 8-4 12 0"/>'
    f'<path d="M6 25c4-3 8-3 12 0s8 3 12 0 8-3 12 0" stroke-opacity=".6"/>'
    f'<path d="M6 35c4-3 8-3 12 0s8 3 12 0 8-3 12 0" stroke-opacity=".32"/></svg>',
    # hair and nails: fingertip with nail, three strands
    f'<svg viewBox="0 0 48 48" {SV}><path d="M7 44V23a6 6 0 0 1 12 0v21"/><path d="M10 23a3 3 0 0 1 6 0v4a3 3 0 0 1-6 0z" stroke="#B08A62"/>'
    f'<path d="M27 5c-4 10 5 16 1 37"/><path d="M33 5c-4 10 5 16 1 37"/><path d="M39 5c-4 10 5 16 1 37"/></svg>',
    # joints: knee, gold cartilage between the bones
    f'<svg viewBox="0 0 48 48" {SV}><path d="M19 4v11c-4 1-6 3-5 7h20c1-4-1-6-5-7V4"/>'
    f'<path d="M14 27c0 4 2 6 5 7v10M34 27c0 4-2 6-5 7v10M14 27h20"/><path d="M17 24.5h14" stroke="#B08A62" stroke-width="2.4"/></svg>',
    # bones
    f'<svg viewBox="0 0 48 48" {SV}><g transform="rotate(-35 24 24)"><path d="M13 20h22M13 28h22"/>'
    f'<path d="M13 20a4.5 4.5 0 1 0-4 4 4.5 4.5 0 1 0 4 4"/><path d="M35 20a4.5 4.5 0 1 1 4 4 4.5 4.5 0 1 1-4 4"/></g></svg>',
]

BERRY, GREY, GREY_D = "#8E2149", "#CDBDBD", "#B9A7A8"


def pair(x, y, ang=0, r=3.2):
    """A tiny collagen piece (two beads)."""
    dx, dy = math.cos(math.radians(ang)) * r * 1.9, math.sin(math.radians(ang)) * r * 1.9
    return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + dx:.1f}" y2="{y + dy:.1f}" stroke="{BERRY}" stroke-width="1.6"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{BERRY}"/><circle cx="{x + dx:.1f}" cy="{y + dy:.1f}" r="{r}" fill="{BERRY}"/>')


def chain(x0, x1, y, n, amp=5, r=3.6):
    """A long collagen piece (many beads)."""
    pts = [(x0 + (x1 - x0) * i / (n - 1), y + amp * math.sin(i * 1.1)) for i in range(n)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    beads = "".join(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{GREY}" stroke="{GREY_D}" stroke-width=".8"/>' for px, py in pts)
    return f'<polyline points="{line}" fill="none" stroke="{GREY_D}" stroke-width="1.4"/>{beads}'


def zone_svgs():
    """Intestine · wall · blood strips, drawn at 202 px wide so they line up when stacked."""
    W = 202
    gut = (f'<svg viewBox="0 0 {W} 60"><path d="M0 8a8 8 0 0 1 8-8h{W - 16}a8 8 0 0 1 8 8v52H0z" fill="#FBF8F3"/>'
           + pair(14, 18, 20) + pair(44, 40, -30) + pair(70, 16, 60) + pair(26, 46, 80) + pair(58, 28, 10)
           + chain(104, 196, 34, 13) + '</svg>')
    cells, x = [], 4
    for i in range(7):
        cells.append(f'<rect x="{x}" y="0" width="18" height="36" rx="5" fill="#E8BFCB"/>')
        x += 28
    gaps = [4 + 18 + 5 + 28 * i for i in range(6)]  # centre of each gap
    through = "".join(pair(g, 8, 90, 3) for g in gaps[:3])
    wall = (f'<svg viewBox="0 0 {W} 36"><rect width="{W}" height="36" fill="#FBF8F3"/>{"".join(cells)}{through}'
            "</svg>")
    blood = (f'<svg viewBox="0 0 {W} 44"><path d="M0 0h{W}v36a8 8 0 0 1-8 8H8a8 8 0 0 1-8-8z" fill="#F2CBD5"/>'
             + pair(18, 18, 0) + pair(48, 28, 30) + pair(80, 16, -20) + pair(112, 30, 10) + pair(146, 18, 40) + pair(176, 28, -10)
             + '<path d="M12 38h178" stroke="#E2A9B8" stroke-width="1" stroke-dasharray="2 6" stroke-linecap="round"/></svg>')
    return gut, wall, blood


LEG_OURS = '<svg viewBox="0 0 76 14">' + pair(6, 7, 0) + pair(30, 7, 0) + pair(54, 7, 0) + '</svg>'
LEG_TYP = '<svg viewBox="0 0 76 14">' + chain(5, 71, 7, 10, amp=2.5, r=3.4) + '</svg>'


def eq_svgs():
    pieces = '<svg viewBox="0 0 80 80"><circle cx="40" cy="40" r="38" fill="#FFFFFF"/>' + "".join(
        pair(x, y, a) for x, y, a in [(22, 26, 20), (44, 20, 70), (54, 40, -20), (30, 46, 40), (42, 58, 0), (20, 58, -60)]) + '</svg>'
    vitc = ('<svg viewBox="0 0 80 80"><circle cx="40" cy="40" r="38" fill="#FFFFFF"/><circle cx="40" cy="40" r="24" fill="#F4E9DC" stroke="#B08A62" stroke-width="2"/>'
            '<path d="M48 31a12 12 0 1 0 0 18" fill="none" stroke="#B08A62" stroke-width="3.2" stroke-linecap="round"/></svg>')
    strands = []
    for k, (col, w) in enumerate([("#8E2149", 3), ("#C9708E", 3), ("#B08A62", 3)]):
        pts = " ".join(f"{14 + t * 52 / 60:.1f},{40 + 11 * math.sin(t / 60 * 3 * math.pi + k * 2 * math.pi / 3):.1f}" for t in range(61))
        strands.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    helix = '<svg viewBox="0 0 80 80"><circle cx="40" cy="40" r="38" fill="#FFFFFF"/>' + "".join(strands) + '</svg>'
    return pieces, vitc, helix


HOW_ICONS = [
    # stick
    f'<svg viewBox="0 0 26 26" {SV} stroke-width="1.7"><rect x="9" y="2" width="8" height="22" rx="1.5"/><path d="M9 6h8M11 6l1.5-2.5L14 6" stroke-opacity=".6"/></svg>',
    # glass of water
    f'<svg viewBox="0 0 26 26" {SV} stroke-width="1.7"><path d="M6 3h14l-2 20H8z"/><path d="M7.5 11c2 1 3.5 1 5.5 0s3.5-1 5.5 0" stroke="#B08A62"/></svg>',
    # calendar
    f'<svg viewBox="0 0 26 26" {SV} stroke-width="1.7"><rect x="3" y="5" width="20" height="18" rx="2.5"/><path d="M3 10h20M8 3v4M18 3v4"/>'
    f'<path d="M8 15.5l2.5 2.5L18 13" stroke="#B08A62"/></svg>',
]


# ---------- pages ----------
def pages(lang, t, switch=""):
    t = {k: tidy(v) if isinstance(v, str) else v for k, v in t.items()}
    L = t["html_lang"]
    top = switch or f'<div class="bar">{MARK.format(cls="")}</div>'

    def pn(i):
        return f'<div class="pn"><span>Yorosum · {t["lang_name"]}</span><i>{i:02d} / {PAGES:02d}</i></div>'

    def head(n):
        return (f'<p class="t-label">{t[f"p{n}_label"]}</p><h2 class="t-title gap-8">{t[f"p{n}_title"]}</h2>')

    def points(n):
        return '<ul class="pts gap-24">' + "".join(f'<li class="t-body">{t[f"p{n}_b{i}"]}</li>' for i in (1, 2, 3)) + '</ul>'

    def fig(v, unit):
        return f'<b class="t-fig">{v}<small>{unit}</small></b>'

    facts = "".join(f'<div class="fact">{fig(v, u)}<p class="t-body">{t[k]}</p></div>' for v, u, k in [
        ("300", t["u_da"], "c_f1"), (t["n2000"], t["u_mg"], "c_f2"), ("100", t["u_mg"], "c_f3")])
    chips = "".join(f'<span class="chip">{t[f"c_chip{i}"]}</span>' for i in (1, 2, 3))
    areas = "".join(f'<div class="area"><div class="ic">{AREA_ICONS[i]}</div><p>{t[f"p2_i{i + 1}"]}</p></div>' for i in range(4))
    gut, wall, blood = zone_svgs()
    pieces, vitc, helix = eq_svgs()
    how = "".join(f'<div><div class="ic">{HOW_ICONS[i]}</div><p>{t[f"p5_h{i + 1}"]}</p></div>' for i in range(3))
    ing = [(t["ing1"], t["ing1_v"]), (t["ing2"], t["ing2_v"]), (t["ing3"], None), (t["ing4"], None), (t["ing5"], None), (t["ing6"], t["ing6_v"])]
    ing_rows = "".join(f'<div class="row"><span class="t-small">{n}</span>'
                       + (f'<span class="t-val">{v}</span>' if v else f'<span class="t-inc">{t["inc"]}</span>') + '</div>' for n, v in ing)
    moq_rows = "".join(f'<div class="row"><span class="t-small">{t[f"m{i}_k"]}</span><span class="t-val">{t[f"m{i}"]}</span></div>' for i in (1, 2, 3))
    sns = "".join(f'<a href="{u}" aria-label="{k}">{ICONS[k]}</a>' for k, u in zip(["instagram", "telegram", "facebook", "kakao"], CHANNEL_URLS))

    return "".join([
        f'''<section class="pg cover" lang="{L}" id="lang-{lang}">{switch}
  <div class="photo"><img src="../assets/img/cover.jpg" alt=""></div>{LOGO.format(cls="logo")}
  <div class="body">
    <p class="t-eb">{t["c_eb"]}</p>
    <h1 class="t-display gap-8">{t["c_title"]}</h1>
    <p class="t-sub gap-8">{t["c_sub"]}</p>
    <p class="t-lead gap-12">{t["c_tag"]}</p>
    <div class="facts gap-24">{facts}</div>
    <div class="chips gap-24">{chips}</div>
  </div>{pn(1)}</section>''',

        f'''<section class="pg" lang="{L}">{top}<div class="in">
  {head(2)}<p class="t-lead gap-12">{t["p2_lead"]}</p>
  <div class="card gap-24"><div class="areas">{areas}</div></div>
  {points(2)}
</div>{pn(2)}</section>''',

        f'''<section class="pg" lang="{L}">{top}<div class="in">
  {head(3)}<p class="t-lead gap-12">{t["p3_lead"]}</p>
  <div class="card gap-24">
    <div class="zones">
      <div class="zone"><p>{t["p3_gut"]}</p>{gut}</div>
      <div class="zone"><p>{t["p3_wall"]}</p>{wall}</div>
      <div class="zone"><p>{t["p3_blood"]}</p>{blood}</div>
    </div>
    <ul class="legend">
      <li>{LEG_OURS}<p class="t-cap"><b>{t["p3_ours"]} · {t["p3_ours_v"]}</b><br>{t["p3_leg1"]}</p></li>
      <li>{LEG_TYP}<p class="t-cap"><b>{t["p3_typ"]} · {t["p3_typ_v"]}</b><br>{t["p3_leg2"]}</p></li>
    </ul>
  </div>
  {points(3)}
</div>{pn(3)}</section>''',

        f'''<section class="pg" lang="{L}">{top}<div class="in">
  {head(4)}<p class="t-lead gap-12">{t["p4_lead"]}</p>
  <div class="card gap-24"><div class="eq">
    <div>{pieces}<p>{t["p4_e1"]}</p></div><span class="op">+</span>
    <div>{vitc}<p>{t["p4_e2"]}</p></div><span class="op">→</span>
    <div>{helix}<p>{t["p4_e3"]}</p></div>
  </div>
  <div class="dv">
    <div class="dv-h"><span class="t-small">{t["p4_bar"]}</span><b class="t-fig">100<small>{t["u_mg"]}</small></b></div>
    <div class="dv-bar"></div>
    <div class="dv-s"><span class="t-cap">0%</span><span class="t-cap"><b>100%</b> {t["p4_bar_v"]}</span></div>
  </div></div>
  {points(4)}
</div>{pn(4)}</section>''',

        f'''<section class="pg" lang="{L}">{top}<div class="in">
  {head(5)}
  <div class="how gap-24">{how}</div>
  <p class="t-eb gap-24">{t["p5_ing"]}</p>
  <div class="tbl gap-8">{ing_rows}</div>
  <p class="t-cap gap-8"><b>{t["p5_alg"]}</b> {t["p5_note"]}</p>
  <p class="t-eb gap-24">{t["p5_moq"]}</p>
  <div class="tbl gap-8">{moq_rows}</div>
  <div class="end gap-24">
    <a class="qr" href="{STORE}"><img src="../assets/img/qr.svg" alt="QR"></a>
    <div class="end-r"><p class="t-cap">{t["p5_qr"]}</p><nav class="sns">{sns}</nav></div>
  </div>
</div>{pn(5)}</section>''',
    ])


def switch_for(active, copy):
    flags = "".join(f'<a href="#lang-{l}" class="{"on" if l == active else ""}" aria-label="{copy[l]["lang_name"]}">'
                    f'<img src="../assets/flags/{FLAG[l]}.svg" alt=""></a>' for l in copy)
    return f'<nav class="switch">{flags}</nav>'


def chooser(copy):
    buttons = "".join(f'<a class="lang" href="#lang-{l}" lang="{l}"><img src="../assets/flags/{FLAG[l]}.svg" alt="">'
                      f'<span><b>{t["lang_name"]}</b><small>{t["pick"]}</small></span><span class="go">→</span></a>' for l, t in copy.items())
    return f'''<section class="pg cover pick" id="home">
  <div class="photo"><img src="../assets/img/cover.jpg" alt=""></div>{LOGO.format(cls="logo")}
  <div class="body">
    <p class="t-eb">Product guide · 2026</p>
    <h1 class="t-display gap-8">Yorosum Glow <em>Peptide</em></h1>
    <nav class="langs gap-24">{buttons}</nav>
  </div>
</section>'''


def doc(lang_attr, title, body):
    return (f'<!doctype html>\n<html lang="{lang_attr}">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=390">\n<title>{title}</title>\n'
            f'<style>{FONTS}{E_CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n')


PDF_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    await p.goto('file://' + j.html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.emulateMedia({ media: 'print' });
    // layout check: content must end inside the 84 → 780 box on every page
    const bad = await p.evaluate(() => [...document.querySelectorAll('.pg')].map((pg, i) => {
      const box = pg.getBoundingClientRect();
      let max = 0;
      pg.querySelectorAll('.in > *, .body > *').forEach(e => { max = Math.max(max, e.getBoundingClientRect().bottom - box.top); });
      const over = [...pg.querySelectorAll('p, b, span, li')].filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).display !== 'inline').map(e => e.className + ':' + e.textContent.slice(0, 20)).join('|');
      return { page: i + 1, bottom: Math.round(max), over };
    }).filter(r => r.bottom > 781 || r.over));
    if (bad.length) console.log('LAYOUT', j.pdf, JSON.stringify(bad));
    await p.pdf({ path: j.pdf, preferCSSPageSize: true, printBackground: true });
    if (j.png) {
      const s = await p.$$('.pg');
      for (let i = 0; i < s.length; i++) await s[i].screenshot({ path: j.png.replace('%d', i + 1) });
    }
    await p.close();
    console.log('pdf', j.pdf);
  }
  await b.close();
})();
"""


def main():
    copy = json.loads((ROOT / "edu_i18n.json").read_text(encoding="utf-8"))
    BUILD.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    jobs = []
    for l, t in copy.items():
        html = BUILD / f"g-{l}.html"
        html.write_text(doc(t["html_lang"], f"Yorosum Glow Peptide — {t['lang_name']}", pages(l, t)), encoding="utf-8")
        jobs.append({"html": str(html), "pdf": str(OUT / f"yorosum-guide-{l}.pdf"), "png": str(BUILD / f"g-{l}-%d.png")})
    body = chooser(copy) + "".join(f'<div class="with-switch">{pages(l, t, switch_for(l, copy))}</div>' for l, t in copy.items())
    html = BUILD / "g-all.html"
    html.write_text(doc("en", "Yorosum Glow Peptide — Product guide", body), encoding="utf-8")
    jobs.append({"html": str(html), "pdf": str(OUT / "yorosum-guide-all-languages.pdf"), "png": str(BUILD / "g-all-%d.png")})
    js = BUILD / "gpdf.js"
    js.write_text(PDF_JS)
    npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", str(js), json.dumps(jobs)], check=True, env={**os.environ, "NODE_PATH": npm_root})

    from pypdf import PdfReader, PdfWriter
    pdf = OUT / "yorosum-guide-all-languages.pdf"
    w = PdfWriter(clone_from=PdfReader(str(pdf)))
    w.add_outline_item("Choose language", 0)
    for i, l in enumerate(copy):
        w.add_outline_item(copy[l]["lang_name"], 1 + i * PAGES)
    w.page_mode = "/UseOutlines"
    with open(pdf, "wb") as f:
        w.write(f)


if __name__ == "__main__":
    main()

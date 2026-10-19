"""Build the Yorosum Glow Peptide catalogue: 4 A4 pages per language, as HTML and print PDFs.

    python3 catalogue/build.py            # all languages
    python3 catalogue/build.py en ko      # some

Writes catalogue/build/<lang>.html and catalogue/out/yorosum-catalogue-<lang>[-bleed].pdf.
Copy lives in catalogue/i18n.json; design tokens follow yorosum.com (.yv system).
"""
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
BUILD = ROOT / "build"
OUT = ROOT / "out"
BLEED_MM = 3

LOGO = """<svg class="{cls}" viewBox="96 120 1690 310" role="img" aria-label="YOROSUM 여러숨">
<circle cx="137" cy="250" r="36" fill="#8E2149"/>
<path d="M222 170A89 89 0 0 1 222 330" fill="none" stroke="#8E2149" stroke-width="26" stroke-linecap="round"/>
<path d="M295 138A131 131 0 0 1 295 362" fill="none" stroke="#B08A62" stroke-width="26" stroke-linecap="round"/>
<text x="485" y="290" textLength="1292" lengthAdjust="spacing" fill="#8E2149" font-family="Pretendard Variable" font-size="198" font-weight="700">YOROSUM</text>
<text x="490" y="422" textLength="310" lengthAdjust="spacing" fill="#A3587A" font-family="Pretendard Variable" font-size="74" font-weight="500">여러숨</text>
</svg>"""

MARK = """<svg class="{cls}" viewBox="96 120 276 260" aria-hidden="true">
<circle cx="137" cy="250" r="36" fill="#8E2149"/>
<path d="M222 170A89 89 0 0 1 222 330" fill="none" stroke="#8E2149" stroke-width="26" stroke-linecap="round"/>
<path d="M295 138A131 131 0 0 1 295 362" fill="none" stroke="#B08A62" stroke-width="26" stroke-linecap="round"/>
</svg>"""


def tile(bg, inner, defs=""):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{defs}<rect width="24" height="24" rx="5.5" fill="{bg}"/>{inner}</svg>'


ICONS = {
    "instagram": tile("url(#ig-g)", '<g fill="none" stroke="#fff" stroke-width="1.7"><rect x="5.8" y="5.8" width="12.4" height="12.4" rx="3.6"/><circle cx="12" cy="12" r="3"/></g><circle cx="15.6" cy="8.4" r=".9" fill="#fff"/>',
                      '<defs><linearGradient id="ig-g" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FEDA75"/><stop offset=".3" stop-color="#FA7E1E"/><stop offset=".55" stop-color="#D62976"/><stop offset=".8" stop-color="#962FBF"/><stop offset="1" stop-color="#4F5BD5"/></linearGradient></defs>'),
    "telegram": tile("#2AABEE", '<path d="M5.6 11.7l11.3-4.4c.5-.2 1 .1.8.9l-1.9 9c-.1.6-.5.8-1.1.5l-3-2.2-1.4 1.4c-.2.2-.3.3-.6.3l.2-3.1 5.6-5.1c.2-.2 0-.3-.4-.1l-6.9 4.4-3-.9c-.6-.2-.7-.6.2-.9z" fill="#fff"/>'),
    "facebook": tile("url(#fb-g)", '<path d="M13.4 19v-5.8h2l.3-2.4h-2.3V9.3c0-.7.2-1.2 1.2-1.2h1.2V6c-.2 0-1-.1-1.8-.1-1.8 0-3 1.1-3 3.1v1.8H9v2.4h2V19z" fill="#fff"/>',
                     '<defs><linearGradient id="fb-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#18ACFE"/><stop offset="1" stop-color="#0163E0"/></linearGradient></defs>'),
    "kakao": tile("#FEE500", '<path d="M12 5.8c-4 0-7.2 2.5-7.2 5.6 0 2 1.3 3.7 3.3 4.7l-.8 2.9c-.1.3.2.5.4.3l3.4-2.3c.3 0 .6.1.9.1 4 0 7.2-2.5 7.2-5.6S16 5.8 12 5.8z" fill="#3A1D1D"/><text x="12" y="12.9" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="3.6" fill="#FEE500">TALK</text>'),
}

CSS = r"""
/* static weights: variable fonts embed as Type3 in Chromium PDFs */
@font-face { font-family: "Pretendard Variable"; src: url(../assets/fonts/Pretendard-Regular.woff2) format("woff2"); font-weight: 400; font-display: block; }
@font-face { font-family: "Pretendard Variable"; src: url(../assets/fonts/Pretendard-Medium.woff2) format("woff2"); font-weight: 500; font-display: block; }
@font-face { font-family: "Pretendard Variable"; src: url(../assets/fonts/Pretendard-SemiBold.woff2) format("woff2"); font-weight: 600; font-display: block; }
@font-face { font-family: "Pretendard Variable"; src: url(../assets/fonts/Pretendard-Bold.woff2) format("woff2"); font-weight: 700; font-display: block; }
@font-face { font-family: YSerif; font-style: normal; font-display: block; src: url(../assets/fonts/instrument-serif-latin-400-normal.woff2) format("woff2");
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
@font-face { font-family: YSerif; font-style: italic; font-display: block; src: url(../assets/fonts/instrument-serif-latin-400-italic.woff2) format("woff2");
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
@font-face { font-family: YSerif; font-style: normal; font-display: block; src: url(../assets/fonts/instrument-serif-latin-ext-400-normal.woff2) format("woff2");
  unicode-range: U+0100-02AF, U+0304, U+0308, U+0329, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }
@font-face { font-family: YSerif; font-style: italic; font-display: block; src: url(../assets/fonts/instrument-serif-latin-ext-400-italic.woff2) format("woff2");
  unicode-range: U+0100-02AF, U+0304, U+0308, U+0329, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }
@font-face { font-family: YSerif; font-style: normal; font-display: block; src: url(../assets/fonts/cormorant-garamond-cyrillic-500-normal.woff2) format("woff2"); unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }
@font-face { font-family: YSerif; font-style: italic; font-display: block; src: url(../assets/fonts/cormorant-garamond-cyrillic-500-italic.woff2) format("woff2"); unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116; }

/* yorosum.com tokens */
:root {
  --bone: #FBF8F3; --rose: #F0D5DD; --blush: #F6E6EA; --berry: #8E2149; --wine: #5E1530;
  --ink: #2B1A20; --mute: #7C6670; --gold: #B08A62; --line: rgba(142, 33, 73, .16); --white: #FFFFFF;
  --sans: "Pretendard Variable", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
  --serif: YSerif, "Pretendard Variable", serif;  /* Hangul in serif slots falls back to Pretendard, upright */
  --b: __BLEED__mm;   /* bleed */
  --m: 15mm;          /* margin inside trim */
}
@page { size: __PAGE_W__mm __PAGE_H__mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #E9E3DE; }
body { font-family: var(--sans); color: var(--ink); -webkit-font-smoothing: antialiased; word-break: keep-all; overflow-wrap: break-word;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; font-feature-settings: "tnum" 0; }
img { display: block; }
em { font-style: normal; }
body { font-synthesis: none; }

.page { position: relative; width: calc(210mm + 2 * var(--b)); height: calc(297mm + 2 * var(--b)); overflow: hidden; background: var(--bone); break-after: page; }
.page:last-child { break-after: auto; }
@media screen { .page { margin: 0 auto 10mm; box-shadow: 0 4mm 12mm rgba(43, 26, 32, .12); } body { padding: 10mm 0; } }
.safe { position: absolute; top: calc(var(--b) + var(--m)); bottom: calc(var(--b) + var(--m)); left: calc(var(--b) + var(--m)); right: calc(var(--b) + var(--m)); }

/* type scale (pt): 7.5 · 8.5 · 9.5 · 11 · 14 · 24 · 34 · 60 */
.eb { font: 600 7.5pt/1.4 var(--sans); letter-spacing: .24em; text-transform: uppercase; color: var(--gold); }
.ch { font: italic 400 14pt/1.1 var(--serif); color: var(--berry); }
.h2 { font: 500 24pt/1.2 var(--sans); letter-spacing: -.025em; color: var(--ink); }
.lead { font: 400 9.5pt/1.7 var(--sans); color: var(--mute); }
.foot { position: absolute; left: calc(var(--b) + var(--m)); right: calc(var(--b) + var(--m)); bottom: calc(var(--b) + 9mm);
  display: flex; justify-content: space-between; align-items: center; font: 500 7pt/1 var(--sans); letter-spacing: .14em; text-transform: uppercase; color: var(--mute); }
.foot .pn { font: italic 400 10pt/1 var(--serif); letter-spacing: 0; color: var(--berry); text-transform: none; }

/* ---------- 1 · Cover ---------- */
.cover-photo { position: absolute; left: 0; right: 0; top: 0; height: calc(var(--b) + 158mm); }
.cover-photo img { width: 100%; height: 100%; object-fit: cover; object-position: 86% 52%; }
.cover-photo::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(251, 248, 243, .55) 0%, rgba(251, 248, 243, 0) 28%); }
.cover-top { position: absolute; z-index: 2; top: calc(var(--b) + 13mm); left: calc(var(--b) + var(--m)); right: calc(var(--b) + var(--m)); display: flex; justify-content: space-between; align-items: flex-start; }
.logo-l { width: 56mm; height: auto; display: block; }
.cover-top .eb { padding-top: 1.5mm; color: var(--wine); }
.cover-body { position: absolute; top: calc(var(--b) + 158mm + 13mm); left: calc(var(--b) + var(--m)); right: calc(var(--b) + var(--m)); display: flex; flex-direction: column; gap: 3mm; }
.cover-body h1 { font: 500 34pt/1.12 var(--sans); letter-spacing: -.03em; color: var(--ink); margin-top: 1mm; }
.cover-body h1 em { font: italic 400 1.14em/1 var(--serif); color: var(--berry); letter-spacing: 0; }
.name-sub { font: 600 9.5pt/1.3 var(--sans); letter-spacing: .08em; color: var(--berry); }
.tagline { font: 400 11pt/1.55 var(--sans); color: var(--mute); }
.figs { position: absolute; top: calc(var(--b) + 228mm); left: calc(var(--b) + var(--m)); right: calc(var(--b) + var(--m)); }
.figs .eb { margin-bottom: 3mm; }
.figs-row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border-top: .3mm solid var(--line); }
.fig { padding: 5mm 4mm 0 5mm; display: flex; flex-direction: column; gap: 2.5mm; }
.fig:first-child { padding-left: 0; }
.fig + .fig { border-left: .3mm solid var(--line); }
.fig b { font: 400 30pt/1 var(--serif); color: var(--ink); white-space: nowrap; font-weight: 400; }
.fig b small { font: 500 9pt/1 var(--sans); margin-left: 1.2mm; color: var(--ink); }
.fig span { font: 400 8pt/1.45 var(--sans); color: var(--mute); }
.strip { position: absolute; left: 0; right: 0; bottom: 0; height: calc(var(--b) + 17mm); background: var(--blush); }
.strip-in { position: absolute; left: calc(var(--b) + var(--m)); right: calc(var(--b) + var(--m)); top: 0; height: 17mm; display: flex; align-items: center; gap: 7mm; font: 500 8.5pt/1 var(--sans); color: var(--ink); }
.strip-in i { display: inline-block; width: 1.4mm; height: 1.4mm; border-radius: 50%; background: var(--berry); margin-right: 2.2mm; vertical-align: .35mm; }
.strip-in .url { margin-left: auto; font: italic 400 11pt/1 var(--serif); color: var(--berry); }

/* ---------- 2 · Formula ---------- */
.p2-head { display: flex; flex-direction: column; gap: 3.5mm; max-width: 132mm; }
.p2-grid { position: absolute; top: 52mm; left: 0; right: 0; display: grid; grid-template-columns: minmax(0, 1fr) 88mm; gap: 10mm; align-items: start; }
.ing .eb, .spec .eb, .alg .eb { margin-bottom: 2.5mm; }
.ing-row { display: flex; justify-content: space-between; align-items: baseline; gap: 4mm; padding: 4.8mm 0; border-top: .3mm solid var(--line); }
.ing-row:last-child { border-bottom: .3mm solid var(--line); }
.ing-row b { display: block; font: 600 10pt/1.35 var(--sans); }
.ing-row small { display: block; font: 400 8pt/1.4 var(--sans); color: var(--mute); margin-top: .8mm; }
.ing-row .v { flex: none; font: 400 15pt/1 var(--serif); color: var(--berry); white-space: nowrap; }
.ing-row .v.t { font: 500 8.5pt/1 var(--sans); color: var(--mute); }
.box-photo { width: 88mm; height: 88mm; border-radius: 1.5mm; overflow: hidden; background: var(--rose); }
.box-photo img { width: 100%; height: 100%; object-fit: cover; }
.src { margin-top: 4mm; background: var(--blush); border-radius: 1.5mm; padding: 5mm; display: flex; flex-direction: column; gap: 2mm; }
.src p { font: 500 10pt/1.45 var(--sans); color: var(--wine); }
.p2-bottom { position: absolute; left: 0; right: 0; bottom: 14mm; display: grid; grid-template-columns: minmax(0, 1fr) 88mm; gap: 10mm; }
.spec-row { display: grid; grid-template-columns: 30mm minmax(0, 1fr); gap: 3mm; padding: 2.4mm 0; border-top: .3mm solid var(--line); font: 400 8.5pt/1.4 var(--sans); }
.spec-row:last-child { border-bottom: .3mm solid var(--line); }
.spec-row span:first-child { color: var(--mute); }
.alg-box { border-top: .3mm solid var(--line); border-bottom: .3mm solid var(--line); padding: 2.4mm 0 3.2mm; }
.alg .main { font: 600 9pt/1.45 var(--sans); color: var(--berry); margin-bottom: 2mm; }
.alg .body { font: 400 7.5pt/1.6 var(--sans); color: var(--mute); }

/* ---------- 3 · Ritual ---------- */
.steps { position: absolute; top: 31mm; left: 0; right: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6mm; }
.step { display: flex; flex-direction: column; gap: 2mm; }
.step-photo { aspect-ratio: 3 / 5; border-radius: 1.5mm; overflow: hidden; background: var(--rose); margin-bottom: 2.5mm; }
.step-photo img { width: 100%; height: 100%; object-fit: cover; }
.step .n { font: italic 400 15pt/1 var(--serif); color: var(--berry); }
.step b { font: 600 11pt/1.3 var(--sans); }
.step p { font: 400 8.5pt/1.55 var(--sans); color: var(--mute); }
.habit { position: absolute; left: 0; right: 0; bottom: 0; height: calc(var(--b) + 92mm); background: var(--blush); }
.habit-in { position: absolute; left: calc(var(--b) + var(--m)); right: calc(var(--b) + var(--m)); top: 0; height: 74mm; display: grid; grid-template-columns: 74mm minmax(0, 1fr); gap: 10mm; align-items: center; }
.habit .big { font: 400 60pt/.9 var(--serif); color: var(--berry); letter-spacing: -.02em; white-space: nowrap; }
.habit .big small { font: 500 12pt/1 var(--sans); color: var(--ink); letter-spacing: 0; margin-left: 2mm; }
.habit h3 { font: 500 14pt/1.35 var(--sans); letter-spacing: -.015em; color: var(--ink); margin-bottom: 3mm; }
.habit p { font: 400 9.5pt/1.7 var(--sans); color: var(--mute); }
.page.p3 .foot { z-index: 2; }

/* ---------- 4 · Back ---------- */
.back-photo { position: absolute; left: 0; right: 0; top: 0; height: calc(var(--b) + 120mm); }
.back-photo img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 38%; }
.back-body { position: absolute; top: calc(var(--b) + 120mm + 13mm); left: calc(var(--b) + var(--m)); right: calc(var(--b) + var(--m)); }
.back-head { display: flex; flex-direction: column; gap: 3.5mm; margin-bottom: 9mm; }
.back-grid { display: grid; grid-template-columns: 62mm minmax(0, 1fr); gap: 10mm; align-items: start; }
.qr { background: var(--white); border: .3mm solid var(--line); border-radius: 1.5mm; padding: 6mm; display: flex; flex-direction: column; gap: 4mm; }
.qr img { width: 100%; height: auto; }
.qr p { font: 400 8pt/1.5 var(--sans); color: var(--mute); }
.qr .url { font: italic 400 12pt/1 var(--serif); color: var(--berry); }
.chans .eb { margin-bottom: 2.5mm; }
.chan { display: flex; align-items: center; gap: 4mm; padding: 3.6mm 0; border-top: .3mm solid var(--line); }
.chan:last-child { border-bottom: .3mm solid var(--line); }
.chan svg { width: 8mm; height: 8mm; flex: none; }
.chan b { display: block; font: 600 10pt/1.3 var(--sans); }
.chan small { display: block; font: 400 8pt/1.4 var(--sans); color: var(--mute); }
.sign { position: absolute; left: calc(var(--b) + var(--m)); right: calc(var(--b) + var(--m)); bottom: calc(var(--b) + 12mm); display: flex; justify-content: space-between; align-items: flex-end; padding-top: 6mm; border-top: .3mm solid var(--line); }
.logo-s { width: 44mm; height: auto; display: block; }
.sign-r { text-align: right; display: flex; flex-direction: column; gap: 1.6mm; }
.sign-r .line { font: italic 400 14pt/1.1 var(--serif); color: var(--berry); }
.sign-r .cs { font: 400 8pt/1.4 var(--sans); color: var(--mute); }
.sign-r .cs b { font-weight: 600; color: var(--ink); }
.sign-r .copy { font: 400 7pt/1.4 var(--sans); color: var(--mute); }
"""

PAGES = """
<!-- 1 · Cover -->
<section class="page p1">
  <div class="cover-photo"><img src="../assets/img/cover.jpg" alt=""></div>
  <div class="cover-top">__LOGO_L__<span class="eb">{doc_label}</span></div>
  <div class="cover-body">
    <p class="eb">{category}</p>
    <h1>{name_line}</h1>
    <p class="name-sub">{name_sub}</p>
    <p class="tagline">{tagline}</p>
  </div>
  <div class="figs">
    <p class="eb">{per_stick}</p>
    <div class="figs-row">
      <div class="fig"><b>{n2000}<small>{u_mg}</small></b><span>{fig1_label}</span></div>
      <div class="fig"><b>300<small>{u_da}</small></b><span>{fig2_label}</span></div>
      <div class="fig"><b>100<small>{u_mg}</small></b><span>{fig3_label}</span></div>
    </div>
  </div>
  <div class="strip"><div class="strip-in"><span><i></i>{strip1}</span><span><i></i>{strip2}</span><span><i></i>{strip3}</span><span class="url">yorosum.com</span></div></div>
</section>

<!-- 2 · Formula -->
<section class="page p2">
  <div class="safe">
    <div class="p2-head">
      <p class="ch">{p2_label}</p>
      <h2 class="h2">{p2_title}</h2>
      <p class="lead">{p2_intro}</p>
    </div>
    <div class="p2-grid">
      <div class="ing">
        <p class="eb">{ing_head}</p>
        <div class="ing-row"><div><b>{ing1}</b><small>{ing1_d}</small></div><span class="v">{ing1_v}</span></div>
        <div class="ing-row"><div><b>{ing2}</b><small>{ing2_d}</small></div><span class="v">{ing2_v}</span></div>
        <div class="ing-row"><div><b>{ing3}</b></div><span class="v">{ing3_v}</span></div>
        <div class="ing-row"><div><b>{ing4}</b></div><span class="v">{ing4_v}</span></div>
        <div class="ing-row"><div><b>{ing6}</b></div><span class="v">{ing6_v}</span></div>
        <div class="ing-row"><div><b>{ing5}</b></div><span class="v t">{ing5_v}</span></div>
      </div>
      <div>
        <div class="box-photo"><img src="../assets/img/box.jpg" alt=""></div>
        <div class="src"><p class="eb">{src_head}</p><p>{src_body}</p></div>
      </div>
    </div>
    <div class="p2-bottom">
      <div class="spec">
        <p class="eb">{spec_head}</p>
        <div class="spec-row"><span>{spec1_k}</span><span>{spec1_v}</span></div>
        <div class="spec-row"><span>{spec2_k}</span><span>{spec2_v}</span></div>
        <div class="spec-row"><span>{spec3_k}</span><span>{spec3_v}</span></div>
        <div class="spec-row"><span>{spec4_k}</span><span>{spec4_v}</span></div>
        <div class="spec-row"><span>{spec5_k}</span><span>{spec5_v}</span></div>
        <div class="spec-row"><span>{spec6_k}</span><span>{spec6_v}</span></div>
      </div>
      <div class="alg">
        <p class="eb">{alg_head}</p>
        <div class="alg-box"><p class="main">{alg_main}</p>
        <p class="body">{alg_body}</p></div>
      </div>
    </div>
  </div>
  <div class="foot"><span>Yorosum · Glow Peptide · {lang_name}</span><span class="pn">02</span></div>
</section>

<!-- 3 · Ritual -->
<section class="page p3">
  <div class="safe">
    <div class="p2-head">
      <p class="ch">{p3_label}</p>
      <h2 class="h2">{p3_title}</h2>
    </div>
    <div class="steps">
      <div class="step"><div class="step-photo"><img src="../assets/img/step1.jpg" alt=""></div><span class="n">01</span><b>{s1_t}</b><p>{s1_d}</p></div>
      <div class="step"><div class="step-photo"><img src="../assets/img/step2.jpg" alt=""></div><span class="n">02</span><b>{s2_t}</b><p>{s2_d}</p></div>
      <div class="step"><div class="step-photo"><img src="../assets/img/step3.jpg" alt=""></div><span class="n">03</span><b>{s3_t}</b><p>{s3_d}</p></div>
    </div>
  </div>
  <div class="habit"><div class="habit-in">
    <p class="big">10–12<small>{c_unit}</small></p>
    <div><h3>{c_title}</h3><p>{c_body}</p></div>
  </div></div>
  <div class="foot"><span>Yorosum · Glow Peptide · {lang_name}</span><span class="pn">03</span></div>
</section>

<!-- 4 · Back -->
<section class="page p4">
  <div class="back-photo"><img src="../assets/img/back.jpg" alt=""></div>
  <div class="back-body">
    <div class="back-head">
      <p class="ch">{p4_label}</p>
      <h2 class="h2">{p4_title}</h2>
    </div>
    <div class="back-grid">
      <div class="qr"><img src="../assets/img/qr.svg" alt="QR"><p>{qr_caption}</p><span class="url">yorosum.com</span></div>
      <div class="chans">
        <p class="eb">{ch_head}</p>
        <div class="chan">__IC_instagram__<div><b>Instagram</b><small>@yorosum_official</small></div></div>
        <div class="chan">__IC_telegram__<div><b>Telegram</b><small>t.me/yorosum</small></div></div>
        <div class="chan">__IC_facebook__<div><b>Facebook</b><small>Yorosum</small></div></div>
        <div class="chan">__IC_kakao__<div><b>{ch_kakao}</b><small>pf.kakao.com/_HwPFX</small></div></div>
      </div>
    </div>
  </div>
  <div class="sign">
    __LOGO_S__
    <div class="sign-r">
      <p class="line">{signoff}</p>
      <p class="cs">{cs_label} <b>{phone}</b> · yorosum.com</p>
      <p class="copy">{copyright}</p>
    </div>
  </div>
</section>
"""


def render(lang, t, bleed):
    t = dict(t)
    t["n2000"] = "2 000" if lang in ("uz", "ru") else "2,000"  # local thousands style, kept on one line
    t["c_body"] = t["c_body"].replace("10–12", '<span style="white-space:nowrap">10–12</span>').replace("10~12주", '<span style="white-space:nowrap">10~12주</span>')
    t["phone"] = "070-8080-5163" if lang == "ko" else "+82 70-8080-5163"
    body = PAGES.format(**t)
    body = body.replace("__LOGO_L__", LOGO.format(cls="logo-l")).replace("__LOGO_S__", LOGO.format(cls="logo-s"))
    for k, v in ICONS.items():
        body = body.replace(f"__IC_{k}__", v)
    css = (CSS.replace("__BLEED__", str(bleed))
              .replace("__PAGE_W__", str(210 + 2 * bleed))
              .replace("__PAGE_H__", str(297 + 2 * bleed)))
    return (f'<!doctype html>\n<html lang="{t["html_lang"]}">\n<head>\n<meta charset="utf-8">\n'
            f'<title>Yorosum Glow Peptide — {t["lang_name"]}</title>\n<style>{css}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n')


PDF_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  for (const j of jobs) {
    const p = await b.newPage();
    await p.goto('file://' + j.html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: j.pdf, preferCSSPageSize: true, printBackground: true });
    if (j.png) {
      await p.setViewportSize({ width: 794, height: 1123 });
      await p.emulateMedia({ media: 'print' });
      const pages = await p.$$('.page');
      for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: j.png.replace('%d', i + 1), scale: 'device' });
    }
    await p.close();
    console.log('pdf', j.pdf);
  }
  await b.close();
})();
"""


def main(langs):
    copy = json.loads((ROOT / "i18n.json").read_text(encoding="utf-8"))
    BUILD.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    jobs = []
    for lang in langs or list(copy):
        for bleed in (0, BLEED_MM):
            name = f"{lang}-bleed" if bleed else lang
            html = BUILD / f"{name}.html"
            html.write_text(render(lang, copy[lang], bleed), encoding="utf-8")
            pdf = OUT / f"yorosum-catalogue-{name}.pdf"
            jobs.append({"html": str(html), "pdf": str(pdf),
                         "png": str(BUILD / f"{lang}-p%d.png") if not bleed else None})
    js = BUILD / "pdf.js"
    js.write_text(PDF_JS)
    npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", str(js), json.dumps(jobs)], check=True, env={**os.environ, "NODE_PATH": npm_root})


if __name__ == "__main__":
    main(sys.argv[1:])

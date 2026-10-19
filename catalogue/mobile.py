"""Phone edition of the catalogue: 390 × 844 screens, one idea per screen, tappable links.

    python3 catalogue/mobile.py

Writes catalogue/out/yorosum-mobile-<lang>.pdf and yorosum-mobile-all-languages.pdf
(the latter opens with a language chooser and has a language switcher on every screen).
Copy comes from catalogue/i18n.json; artwork and fonts are shared with build.py.
"""
import json
import os
import subprocess

from build import BUILD, CHANNEL_URLS, CODE, CSS, FLAG, ICONS, LOGO, MARK, OUT, PICK, ROOT

FONTS = CSS.split("/* yorosum.com tokens */")[0]
STORE = "https://yorosum.com/QR_landing_page_links/"
SCREENS = 5

M_CSS = r"""
:root { --bone: #FBF8F3; --rose: #F0D5DD; --blush: #F6E6EA; --berry: #8E2149; --wine: #5E1530; --ink: #2B1A20; --mute: #7C6670;
  --gold: #B08A62; --line: rgba(142, 33, 73, .16); --white: #FFFFFF;
  --sans: "Pretendard Variable", "Apple SD Gothic Neo", sans-serif; --serif: YSerif, "Pretendard Variable", serif; --pad: 28px; }
@page { size: 390px 844px; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #E9E3DE; }
body { font-family: var(--sans); color: var(--ink); -webkit-font-smoothing: antialiased; word-break: keep-all; overflow-wrap: break-word; font-synthesis: none;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
img { display: block; }
em { font-style: normal; }
a { color: inherit; text-decoration: none; }
.scr { position: relative; width: 390px; height: 844px; overflow: hidden; background: var(--bone); break-after: page; }
.scr:last-child { break-after: auto; }
@media screen { .scr { margin: 0 auto 24px; } body { padding: 24px 0; } }
.in { position: absolute; left: var(--pad); right: var(--pad); top: 84px; bottom: 64px; display: flex; flex-direction: column; }

/* running bar: mark top-left, page number bottom */
.bar { position: absolute; z-index: 4; top: 26px; left: var(--pad); }
.bar svg { width: 26px; height: 25px; display: block; }
.pn { position: absolute; left: var(--pad); right: var(--pad); bottom: 26px; display: flex; justify-content: space-between; align-items: baseline;
  font: 600 9px/1 var(--sans); letter-spacing: .16em; text-transform: uppercase; color: var(--mute); }
.pn i { font: italic 400 14px/1 var(--serif); letter-spacing: 0; color: var(--berry); text-transform: none; }

/* type */
.eb { font: 600 10px/1.4 var(--sans); letter-spacing: .22em; text-transform: uppercase; color: var(--gold); }
.ch { font: italic 400 20px/1.1 var(--serif); color: var(--berry); }
.h2 { font: 500 30px/1.22 var(--sans); letter-spacing: -.025em; text-wrap: balance; }
.lead { font: 400 15.5px/1.7 var(--sans); color: var(--mute); }
.stack { display: flex; flex-direction: column; gap: 12px; }

/* 1 cover */
.c-photo { position: absolute; left: 0; right: 0; top: 0; height: 470px; }
.c-photo img { width: 100%; height: 100%; object-fit: cover; object-position: 80% 50%; }
.c-photo::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(251, 248, 243, .6) 0%, rgba(251, 248, 243, 0) 30%); }
.c-logo { position: absolute; z-index: 3; top: 30px; left: var(--pad); width: 150px; height: auto; }
.c-body { position: absolute; left: var(--pad); right: var(--pad); top: 500px; display: flex; flex-direction: column; gap: 10px; }
.c-body h1 { font: 500 36px/1.12 var(--sans); letter-spacing: -.03em; }
.c-body h1 em { font: italic 400 1.14em/1 var(--serif); color: var(--berry); letter-spacing: 0; }
.c-sub { font: 600 12px/1.3 var(--sans); letter-spacing: .08em; color: var(--berry); }
.c-tag { font: 400 16px/1.6 var(--sans); color: var(--mute); }
.hint { position: absolute; left: var(--pad); bottom: 28px; display: flex; align-items: center; gap: 10px; font: italic 400 15px/1 var(--serif); color: var(--berry); }
.hint span { width: 1px; height: 26px; background: linear-gradient(var(--berry), rgba(142, 33, 73, 0)); }

/* 2 figures */
.figs { display: flex; flex-direction: column; margin-top: 18px; }
.fig { padding: 22px 0; border-top: 1px solid var(--line); display: flex; flex-direction: column; gap: 8px; }
.fig:last-child { border-bottom: 1px solid var(--line); }
.fig b { font: 400 64px/.95 var(--serif); color: var(--ink); white-space: nowrap; font-weight: 400; }
.fig b small { font: 500 17px/1 var(--sans); margin-left: 6px; }
.fig span { font: 400 14px/1.45 var(--sans); color: var(--mute); }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: auto; }
.chip { font: 500 13px/1 var(--sans); padding: 10px 14px; border-radius: 99px; background: var(--blush); color: var(--wine); }

/* 3 formula */
.photo { border-radius: 6px; overflow: hidden; background: var(--rose); }
.photo img { width: 100%; height: 100%; object-fit: cover; }
.f-photo { margin-top: auto; height: 334px; }

/* 4 ingredients */
.rows { display: flex; flex-direction: column; margin-top: 12px; }
.row { display: flex; justify-content: space-between; align-items: baseline; gap: 14px; padding: 15px 0; border-top: 1px solid var(--line); }
.row:last-child { border-bottom: 1px solid var(--line); }
.row b { display: block; font: 600 16px/1.35 var(--sans); }
.row small { display: block; font: 400 13px/1.4 var(--sans); color: var(--mute); margin-top: 3px; }
.row .v { flex: none; font: 400 22px/1 var(--serif); color: var(--berry); white-space: nowrap; }
.row .v.t { font: 500 13px/1 var(--sans); color: var(--mute); }
.card { margin-top: auto; background: var(--blush); border-radius: 6px; padding: 18px 20px; display: flex; flex-direction: column; gap: 8px; }
.card p:last-child { font: 500 16px/1.5 var(--sans); color: var(--wine); }

/* 5 ritual */
.steps { display: flex; flex-direction: column; gap: 14px; margin-top: 22px; }
.step { display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 18px; align-items: center; }
.step .photo { height: 150px; }
.step .n { font: italic 400 20px/1 var(--serif); color: var(--berry); }
.step b { display: block; font: 600 18px/1.3 var(--sans); margin: 8px 0 6px; }
.step p { font: 400 14px/1.55 var(--sans); color: var(--mute); }

/* 6 habit */
.habit { background: var(--blush); }
.habit .in { justify-content: center; gap: 22px; }
.habit .big { font: 400 112px/.85 var(--serif); color: var(--berry); letter-spacing: -.02em; white-space: nowrap; }
.habit .big small { display: block; font: 500 20px/1 var(--sans); color: var(--ink); letter-spacing: 0; margin-top: 14px; }
.habit h3 { font: 500 26px/1.3 var(--sans); letter-spacing: -.02em; text-wrap: balance; }
.habit p { font: 400 16px/1.7 var(--sans); color: var(--mute); }

/* 7 specs */
.spec { display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 12px; padding: 12px 0; border-top: 1px solid var(--line); font: 400 14px/1.45 var(--sans); }
.spec span:first-child { color: var(--mute); }
.specs { margin: 12px 0 30px; border-bottom: 1px solid var(--line); }
.alg-main { font: 600 15px/1.5 var(--sans); color: var(--berry); margin: 12px 0 8px; }
.alg-body { font: 400 12.5px/1.65 var(--sans); color: var(--mute); }

/* 8 store */
.s-photo { position: absolute; left: 0; right: 0; top: 0; height: 250px; }
.s-photo img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 40%; }
.store .in { top: 278px; }
.btn { display: flex; align-items: center; justify-content: space-between; height: 56px; padding: 0 22px; border-radius: 99px; background: var(--berry); color: var(--white);
  font: 600 16px/1 var(--sans); margin: 18px 0 14px; }
.btn i { font: italic 400 20px/1 var(--serif); }
.chan { display: flex; align-items: center; gap: 14px; padding: 11px 0; border-top: 1px solid var(--line); }
.chan:last-child { border-bottom: 1px solid var(--line); }
.chan svg { width: 32px; height: 32px; flex: none; }
.chan b { display: block; font: 600 15px/1.3 var(--sans); }
.chan small { display: block; font: 400 12.5px/1.3 var(--sans); color: var(--mute); }
.chan .go { margin-left: auto; font: italic 400 18px/1 var(--serif); color: var(--berry); }
.sign { margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end; gap: 12px; }
.sign svg { width: 116px; height: auto; display: block; }
.sign div { text-align: right; display: flex; flex-direction: column; gap: 4px; }
.sign .line { font: italic 400 17px/1.15 var(--serif); color: var(--berry); }
.sign .cs { font: 400 11px/1.4 var(--sans); color: var(--mute); }
.sign .cs b { color: var(--ink); font-weight: 600; }
.store .pn { display: none; }

/* 8 wholesale */
.moq { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 26px; border-top: 1px solid var(--line); }
.moq div { padding: 18px 12px 18px 16px; border-bottom: 1px solid var(--line); display: flex; flex-direction: column; gap: 8px; }
.moq div:nth-child(odd) { padding-left: 0; border-right: 1px solid var(--line); }
.moq b { font: 400 30px/1 var(--serif); color: var(--berry); white-space: nowrap; font-weight: 400; }
.moq span { font: 400 13px/1.4 var(--sans); color: var(--mute); }


/* ---- 5-screen edition ---- */
.h2.sm { font-size: 25px; }
.prem { gap: 0; }
.pt { margin-top: 22px; padding-top: 18px; border-top: 1px solid var(--line); }
.pt-h { font: 500 15px/1 var(--sans); color: var(--ink); display: flex; align-items: baseline; gap: 5px; }
.pt-h b { font: 400 50px/.9 var(--serif); color: var(--berry); font-weight: 400; }
.pt-k { font: 600 14.5px/1.35 var(--sans); color: var(--ink); margin-top: 8px; }
.pt-b { font: 400 13px/1.6 var(--sans); color: var(--mute); margin-top: 5px; }
.scale { position: relative; height: 8px; margin: 30px 0 6px; border-radius: 8px; background: linear-gradient(90deg, var(--berry), var(--rose) 45%, #E9E3DE); }
.scale em { position: absolute; top: 50%; width: 16px; height: 16px; margin: -8px 0 0 -8px; border-radius: 50%; background: var(--berry); border: 3px solid var(--bone); box-shadow: 0 0 0 1px var(--berry); }
.scale em span { position: absolute; bottom: 18px; left: 50%; transform: translateX(-20%); white-space: nowrap; font: 600 11px/1 var(--sans); color: var(--berry); }
.scale-l { display: flex; justify-content: space-between; font: 500 11px/1 var(--sans); color: var(--mute); }
.pt.two { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0; }
.pt.two > div + div { border-left: 1px solid var(--line); padding-left: 16px; }
.pt.two > div:first-child { padding-right: 14px; }
.pt.two .pt-h b { font-size: 40px; }
.fish { margin-top: auto; background: var(--blush); border-radius: 6px; padding: 16px 18px; }
.fish .pt-k { margin-top: 0; color: var(--wine); }
.f-top { display: grid; grid-template-columns: 120px minmax(0, 1fr); gap: 18px; align-items: center; }
.f-top .photo { height: 120px; }
.rows .row { padding: 11px 0; align-items: center; }
.rows .row b { font-size: 14.5px; }
.rows .row .v { font-size: 19px; }
.rows .row .v.t { font-size: 13px; }
.how { margin-top: auto; display: grid; grid-template-columns: 80px minmax(0, 1fr); gap: 16px; align-items: center; background: var(--blush); border-radius: 6px; padding: 12px; }
.how .photo { height: 96px; }
.how .pt-k { margin-top: 0; color: var(--wine); }
.store .in { top: 250px; gap: 0; }
.s-photo { height: 226px; }
.qr { display: flex; align-items: center; gap: 16px; margin-top: 18px; padding: 14px; background: var(--white); border: 1px solid var(--line); border-radius: 8px; }
.qr img { width: 112px; height: 112px; flex: none; }
.qr span { font: 400 13px/1.55 var(--sans); color: var(--mute); }
.sns { display: flex; justify-content: space-between; margin-top: 18px; padding: 0 6px; }
.sns a svg { width: 52px; height: 52px; display: block; }
.flagrow { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 18px; }
.flagrow img { width: 100%; aspect-ratio: 4 / 3; border-radius: 5px; object-fit: cover; box-shadow: 0 2px 8px rgba(43, 26, 32, .16); }
.sign { align-items: center; }
.sign .copy { font: 400 10.5px/1 var(--sans); color: var(--mute); letter-spacing: .04em; }

/* language switcher (all-languages edition) */
.switch { position: absolute; z-index: 5; top: 22px; left: var(--pad); display: flex; gap: 10px; }
.switch a { display: block; width: 30px; height: 22.5px; border-radius: 4px; overflow: hidden; box-shadow: 0 1px 5px rgba(43, 26, 32, .22); }
.switch a.on { box-shadow: 0 0 0 2px var(--bone), 0 0 0 3.5px var(--berry); }
.switch img { width: 100%; height: 100%; object-fit: cover; display: block; }
.with-switch .c-logo { top: 72px; }
.with-switch .c-body { top: 510px; }

/* language chooser */
.pick .c-photo { height: 400px; }
.pick-body { position: absolute; left: var(--pad); right: var(--pad); top: 424px; display: flex; flex-direction: column; gap: 8px; }
.pick-body h1 { font: 500 30px/1.15 var(--sans); letter-spacing: -.03em; }
.pick-body h1 em { font: italic 400 1.14em/1 var(--serif); color: var(--berry); }
.langs { display: flex; flex-direction: column; gap: 10px; margin-top: 14px; }
.lang { display: flex; align-items: center; gap: 16px; height: 64px; padding: 0 20px 0 16px; border-radius: 10px; background: var(--white); border: 1px solid var(--line); }
.lang img { width: 40px; height: 30px; border-radius: 4px; object-fit: cover; box-shadow: 0 2px 6px rgba(43, 26, 32, .16); }
.lang b { font: 600 17px/1.2 var(--sans); }
.lang small { display: block; font: italic 400 14px/1.2 var(--serif); color: var(--berry); }
.lang .go { margin-left: auto; font: 400 20px/1 var(--serif); color: var(--berry); }
"""


def esc_nowrap(s):
    return (s.replace("10–12", '<span style="white-space:nowrap">10–12</span>')
             .replace("10~12주", '<span style="white-space:nowrap">10~12주</span>'))


def screens(lang, t, switch=""):
    """Five screens: cover · why premium · formula & how to take · wholesale · store."""
    mark = f'<div class="bar">{MARK.format(cls="")}</div>'
    top = switch or mark
    L = t["html_lang"]

    def pn(i):
        return f'<div class="pn"><span>Yorosum · {t["lang_name"]}</span><i>{i:02d} / {SCREENS:02d}</i></div>'

    ing = [(t["ing1"], t["ing1_v"], False), (t["ing2"], t["ing2_v"], False), (t["ing3"], t["ing3_v"], True),
           (t["ing5"], t["ing5_v"], True), (t["ing4"], t["ing4_v"], True), (t["ing6"], t["ing6_v"], False)]
    rows = "".join(f'<div class="row"><b>{a}</b><span class="v{" t" if txt else ""}">{v}</span></div>' for a, v, txt in ing)
    moq = "".join(f'<div><b>{t[f"moq_v{i}"]}</b><span>{t[f"moq_k{i}"]}</span></div>' for i in range(1, 7))
    sns = "".join(f'<a href="{u}" aria-label="{k}">{ICONS[k]}</a>' for k, u in zip(["instagram", "telegram", "facebook", "kakao"], CHANNEL_URLS))
    n2000 = "2\u00a0000" if lang in ("uz", "ru") else "2,000"
    da_marker = "300 Да" if lang == "ru" else "300 Da"
    return "".join([
        f'''<section class="scr cover" lang="{L}" id="lang-{lang}">{switch}
  <div class="c-photo"><img src="../assets/img/cover.jpg" alt=""></div>{LOGO.format(cls="c-logo")}
  <div class="c-body"><p class="eb">{t["category"]}</p><h1>{t["name_line"]}</h1><p class="c-sub">{t["name_sub"]}</p><p class="c-tag">{t["tagline"]}</p></div>
  <div class="hint"><span></span>01 / {SCREENS:02d}</div></section>''',

        f'''<section class="scr" lang="{L}">{top}<div class="in prem">
  <div class="stack"><p class="ch">{t["prem_label"]}</p><h2 class="h2 sm">{t["prem_title"]}</h2></div>
  <div class="pt">
    <p class="pt-h"><b>300</b>{t["u_da"]}</p><p class="pt-k">{t["da_head"]}</p>
    <div class="scale" aria-hidden="true"><i></i><em style="left:8%"><span>{da_marker}</span></em></div>
    <div class="scale-l"><span>{t["scale_lo"]}</span><span>{t["scale_hi"]}</span></div>
    <p class="pt-b">{t["da_body"]}</p>
  </div>
  <div class="pt two">
    <div><p class="pt-h"><b>{"2 000" if lang in ("uz", "ru") else "2,000"}</b>{t["u_mg"]}</p><p class="pt-k">{t["mg_head"]}</p><p class="pt-b">{t["mg_body"]}</p></div>
    <div><p class="pt-h"><b>100</b>{t["u_mg"]}</p><p class="pt-k">{t["vc_head"]}</p><p class="pt-b">{t["vc_body"]}</p></div>
  </div>
  <div class="fish"><p class="pt-k">{t["fish_head"]}</p><p class="pt-b">{t["fish_body"]}</p></div>
</div>{pn(2)}</section>''',

        f'''<section class="scr" lang="{L}">{top}<div class="in">
  <div class="f-top"><div class="photo"><img src="../assets/img/box.jpg" alt=""></div>
    <div class="stack"><p class="ch">{t["p2_label"]}</p><h2 class="h2 sm">{t["p2_title"]}</h2></div></div>
  <p class="eb" style="margin-top:22px">{t["ing_head"]}</p><div class="rows">{rows}</div>
  <div class="how"><div class="photo"><img src="../assets/img/step2.jpg" alt=""></div>
    <div><p class="pt-k">{t["how_head"]}</p><p class="pt-b">{esc_nowrap(t["how_body"])}</p></div></div>
</div>{pn(3)}</section>''',

        f'''<section class="scr" lang="{L}">{top}<div class="in">
  <div class="stack"><p class="ch">{t["moq_label"]}</p><h2 class="h2 sm">{t["moq_title"]}</h2></div>
  <div class="moq">{moq}</div>
  <p class="eb" style="margin-top:30px">{t["alg_head"]}</p><p class="alg-main">{t["alg_main"]}</p><p class="alg-body">{t["alg_body"]}</p>
</div>{pn(4)}</section>''',

        f'''<section class="scr store" lang="{L}">{switch}
  <div class="s-photo"><img src="../assets/img/back.jpg" alt=""></div>
  <div class="in">
    <div class="stack"><p class="ch">{t["p4_label"]}</p><h2 class="h2 sm">{t["p4_title"]}</h2></div>
    <a class="qr" href="{STORE}"><img src="../assets/img/qr.svg" alt="QR"><span>{t["qr_caption"]}</span></a>
    <nav class="sns">{sns}</nav>
    <div class="sign">{LOGO.format(cls="")}<p class="copy">© 2026 YOROSUM</p></div>
  </div>{pn(5)}</section>''',
    ])


def switch_for(active, copy):
    """Top-left language switcher: clickable flags only; the current language has a berry ring."""
    flags = "".join(f'<a href="#lang-{l}" class="{"on" if l == active else ""}" aria-label="{copy[l]["lang_name"]}">'
                    f'<img src="../assets/flags/{FLAG[l]}.svg" alt=""></a>' for l in copy)
    return f'<nav class="switch">{flags}</nav>'


def chooser(copy):
    buttons = "".join(f'<a class="lang" href="#lang-{l}"><img src="../assets/flags/{FLAG[l]}.svg" alt="">'
                      f'<span><b lang="{l}">{copy[l]["lang_name"]}</b><small lang="{l}">{PICK[l]}</small></span><span class="go">→</span></a>' for l in copy)
    return f'''<section class="scr pick" id="home">
  <div class="c-photo"><img src="../assets/img/cover.jpg" alt=""></div>{LOGO.format(cls="c-logo")}
  <div class="pick-body"><p class="eb">Product Catalogue 2026</p><h1>Yorosum Glow <em>Peptide</em></h1><nav class="langs">{buttons}</nav></div>
</section>'''


def doc(lang_attr, title, body):
    return (f'<!doctype html>\n<html lang="{lang_attr}">\n<head>\n<meta charset="utf-8">\n<title>{title}</title>\n'
            f'<style>{FONTS}{M_CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n')


PDF_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: 390, height: 844 } });
    await p.goto('file://' + j.html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: j.pdf, preferCSSPageSize: true, printBackground: true });
    if (j.png) {
      await p.emulateMedia({ media: 'print' });
      const s = await p.$$('.scr');
      for (let i = 0; i < s.length; i++) await s[i].screenshot({ path: j.png.replace('%d', i + 1) });
    }
    await p.close();
    console.log('pdf', j.pdf);
  }
  await b.close();
})();
"""


def main():
    copy = json.loads((ROOT / "i18n.json").read_text(encoding="utf-8"))
    BUILD.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    jobs = []
    for l, t in copy.items():
        html = BUILD / f"m-{l}.html"
        html.write_text(doc(t["html_lang"], f"Yorosum Glow Peptide — {t['lang_name']}", screens(l, t)), encoding="utf-8")
        jobs.append({"html": str(html), "pdf": str(OUT / f"yorosum-mobile-{l}.pdf"), "png": str(BUILD / f"m-{l}-%d.png")})
    allb = chooser(copy) + "".join(f'<div class="with-switch">{screens(l, t, switch_for(l, copy))}</div>' for l, t in copy.items())
    html = BUILD / "m-all.html"
    html.write_text(doc("en", "Yorosum Glow Peptide — Mobile catalogue", allb), encoding="utf-8")
    jobs.append({"html": str(html), "pdf": str(OUT / "yorosum-mobile-all-languages.pdf"), "png": str(BUILD / "m-all-%d.png")})
    js = BUILD / "mpdf.js"
    js.write_text(PDF_JS)
    npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", str(js), json.dumps(jobs)], check=True, env={**os.environ, "NODE_PATH": npm_root})

    from pypdf import PdfReader, PdfWriter
    pdf = OUT / "yorosum-mobile-all-languages.pdf"
    w = PdfWriter(clone_from=PdfReader(str(pdf)))
    w.add_outline_item("Choose language", 0)
    for i, l in enumerate(copy):
        w.add_outline_item(copy[l]["lang_name"], 1 + i * SCREENS)
    w.page_mode = "/UseOutlines"
    with open(pdf, "wb") as f:
        w.write(f)


if __name__ == "__main__":
    main()

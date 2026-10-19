// Render each language build to an A4 PDF with Playwright's Chromium.
// Usage: python3 build.py && NODE_PATH=$(npm root -g) node pdf.js
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const LANGS = ["en", "ru", "uz"];
const root = __dirname;
fs.mkdirSync(path.join(root, "pdf"), { recursive: true });

(async () => {
  const browser = await chromium.launch();
  for (const lang of LANGS) {
    const src = lang === "en" ? "collagen-comparison.html" : `collagen-comparison.${lang}.html`;
    const strings = JSON.parse(fs.readFileSync(path.join(root, "src/i18n", `${lang}.json`), "utf8"));
    // The artifact host adds the document skeleton; add it here so the PDF renders in standards mode.
    const tmp = path.join(root, `.print-${lang}.html`);
    fs.writeFileSync(tmp, `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"></head><body>` +
      fs.readFileSync(path.join(root, src), "utf8") + "</body></html>");

    const page = await browser.newPage();
    const errors = [];
    page.on("pageerror", e => errors.push(e.message));
    await page.emulateMedia({ media: "print", colorScheme: "light" });
    await page.goto("file://" + tmp, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => document.querySelectorAll("details").forEach(d => (d.open = true)));
    const out = path.join(root, "pdf", `collagen-benchmark-${lang}.pdf`);
    await page.pdf({
      path: out,
      preferCSSPageSize: true,
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: "<span></span>",
      footerTemplate: `<div style="width:100%;font:8px sans-serif;color:#56676f;padding:0 12mm;display:flex;justify-content:space-between">
        <span>${strings.meta.footer}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`
    });
    await page.close();
    fs.unlinkSync(tmp);
    console.log(lang, errors.length ? errors : "ok", out);
  }
  await browser.close();
})();

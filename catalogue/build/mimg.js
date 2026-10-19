const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const l of ['en', 'uz', 'ru', 'ko']) {
    const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
    await p.goto('file:///home/user/Yorosum/catalogue/build/m-' + l + '.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.emulateMedia({ media: 'print' });
    const s = await p.$$('.scr');
    for (let i = 0; i < s.length; i++) await s[i].screenshot({ path: `/home/user/Yorosum/catalogue/build/mi-${l}-${i + 1}.png` });
    await p.close();
  }
  await b.close();
})();

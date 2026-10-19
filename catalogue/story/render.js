// Render story.html frame by frame (animations paused and scrubbed), then encode MP4 + GIF with ffmpeg.
//   NODE_PATH=$(npm root -g) node catalogue/story/render.js
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs'), path = require('path');
const DIR = __dirname, FR = path.join(DIR, '..', 'build', 'story_frames'), OUT = path.join(DIR, '..', 'out');
const FPS = 30, SECONDS = 8;
(async () => {
  fs.rmSync(FR, { recursive: true, force: true }); fs.mkdirSync(FR, { recursive: true });
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(DIR, 'story.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => document.getAnimations().forEach(a => a.pause()));
  for (let i = 0; i < FPS * SECONDS; i++) {
    const t = (i / FPS) * 1000;
    await p.evaluate(t => document.getAnimations().forEach(a => { a.currentTime = t; }), t);
    await p.screenshot({ path: path.join(FR, `f${String(i).padStart(4, '0')}.png`) });
  }
  await b.close();
  const mp4 = path.join(OUT, 'yorosum-catalogue-story.mp4'), gif = path.join(OUT, 'yorosum-catalogue-story.gif');
  execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${FR}/f%04d.png -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 17 -movflags +faststart ${mp4}`);
  execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${FR}/f%04d.png -vf "fps=12,scale=540:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=sierra2_4a" ${gif}`);
  execSync(`cp ${FR}/f${String(FPS * SECONDS - 1).padStart(4, '0')}.png ${path.join(OUT, 'yorosum-catalogue-story.png')}`);
  console.log('done');
})();

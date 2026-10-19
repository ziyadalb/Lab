// Print an HTML file to an A4 PDF with Chromium (Playwright), after fonts and math are ready.
// Usage: NODE_PATH="$(npm root -g)" node tools/export_pdf.mjs <in.html> <out.pdf> [toc.json]
// toc.json (optional) maps anchor id -> page number; it fills the table of contents before printing.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const [, , inFile, outFile, tocFile] = process.argv;
const browser = await chromium.launch();
// Viewport = A4 content width (210mm - 2 x 15mm margins) so the overflow check sees the printed layout.
const page = await browser.newPage({ viewport: { width: Math.round(180 / 25.4 * 96), height: 1100 } });
await page.emulateMedia({ media: 'print' });
await page.goto('file://' + path.resolve(inFile), { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
// Math or table content wider than its box would be cut in the PDF: report every case.
const overflow = await page.evaluate(() => {
  const out = [];
  for (const el of document.querySelectorAll('.md, td, .ch, .rb, .fc > div, .box, .drill')) {
    if (el.scrollWidth > el.clientWidth + 1) {
      const ann = el.querySelector('annotation');
      out.push({ cls: el.className, over: el.scrollWidth - el.clientWidth,
                 tex: ann ? ann.textContent.slice(0, 90) : el.textContent.slice(0, 60) });
    }
  }
  return out;
});
const fontsOk = await page.evaluate(() => {
  const want = ['Plex Arabic', 'KaTeX_Main', 'KaTeX_Math'];
  const loaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, ''));
  return want.map(w => [w, loaded.includes(w)]);
});
if (tocFile && fs.existsSync(tocFile)) {
  const toc = JSON.parse(fs.readFileSync(tocFile, 'utf8'));
  await page.evaluate((toc) => {
    for (const el of document.querySelectorAll('.toc .pg, .pgref')) {
      const n = toc[el.dataset.target];
      el.textContent = n ? String(n) : '';
    }
  }, toc);
}
await page.pdf({ path: outFile, format: 'A4', printBackground: true, preferCSSPageSize: true,
                 outline: true, tagged: true, displayHeaderFooter: false });
await browser.close();
console.log(JSON.stringify({ out: outFile, fonts: fontsOk, overflow }, null, 1));
if (overflow.length) process.exitCode = 3;

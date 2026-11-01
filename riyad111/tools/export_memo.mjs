// Print src/memo.html to an A4 PDF with Chromium (Playwright) after fonts and KaTeX are ready.
// Usage: node tools/export_memo.mjs <in.html> <out.pdf> [toc.json]
// toc.json maps anchor id -> page number; it fills the contents page and the "(ص N)" references.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire('/opt/node-tools/node_modules/');
const { chromium } = require('playwright');

const [, , inFile, outFile, tocFile] = process.argv;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: Math.round(182 / 25.4 * 96), height: 1100 } });
await page.emulateMedia({ media: 'print' });
await page.goto('file://' + path.resolve(inFile), { waitUntil: 'load' });
await page.waitForFunction(() => window.__mathDone === true);
await page.evaluate(() => document.fonts.ready);
const mathErrors = await page.evaluate(() => window.__mathErrors);
const fonts = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '') + ' ' + f.weight));
const overflow = await page.evaluate(() => {
  const out = [];
  for (const el of document.querySelectorAll('.m, .tt, .gi, .step, .box, .ex')) {
    if (el.scrollWidth > el.clientWidth + 1) {
      const ann = el.querySelector('annotation');
      out.push({ cls: el.className, over: el.scrollWidth - el.clientWidth, tex: ann ? ann.textContent.slice(0, 90) : el.textContent.slice(0, 60) });
    }
  }
  return out;
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
await page.pdf({
  path: outFile, format: 'A4', printBackground: true, tagged: true, outline: false,
  margin: { top: '14mm', bottom: '17mm', left: '14mm', right: '14mm' },
  displayHeaderFooter: true, headerTemplate: '<div></div>',
  footerTemplate: '<div style="width:100%;text-align:center;font-size:9pt;color:#666;font-family:sans-serif"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
});
await browser.close();
console.log(JSON.stringify({ out: outFile, mathErrors, overflow, fonts: [...new Set(fonts)].length }, null, 1));
if (mathErrors.length || overflow.length) process.exitCode = 3;

// Replace data-tex placeholders with server-side KaTeX (HTML + MathML with the TeX annotation).
// Usage: node tools/render_math.mjs <in.html> <out.html>
import fs from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const katex = require('katex');

const [, , inFile, outFile] = process.argv;
let html = fs.readFileSync(inFile, 'utf8');
const unescape = (s) => s.replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
// colour meanings, the same everywhere: 🔵 u (the inside), 🟢 du (the derivative of the inside), 🟠 the adjustment number,
// 🔴 a minus sign or a danger
const MACROS = { '\\cU': '\\textcolor{##1565c0}{#1}', '\\cD': '\\textcolor{##1b7a2e}{#1}',
                 '\\cA': '\\textcolor{##d35400}{#1}', '\\cR': '\\textcolor{##c0181f}{#1}' };
let count = 0;
const errors = [];
const render = (tex, display) => {
  count += 1;
  try {
    return katex.renderToString(tex, { displayMode: display, throwOnError: true, output: 'htmlAndMathml', strict: 'ignore', trust: false, macros: { ...MACROS } });
  } catch (e) {
    errors.push({ tex, message: String(e.message || e) });
    return '<span class="katex-error">' + tex + '</span>';
  }
};
html = html.replace(/<div class="md([^"]*)" dir="ltr" data-tex="([^"]*)"><\/div>/g,
  (_, cls, tex) => `<div class="md${cls}" dir="ltr">${render(unescape(tex), true)}</div>`);
html = html.replace(/<bdi class="mi" dir="ltr" data-tex="([^"]*)"><\/bdi>/g,
  (_, tex) => `<bdi class="mi" dir="ltr">${render(unescape(tex), false)}</bdi>`);
fs.writeFileSync(outFile, html);
console.log(JSON.stringify({ rendered: count, errors }, null, 1));
if (errors.length) process.exit(1);

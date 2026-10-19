#!/bin/bash
# Build, export and check the shortcuts booklet (stage 3 sample).
#   HTML (math checked while building) -> KaTeX -> PDF pass 1 -> page map -> PDF pass 2 -> QA + leak check
# Needs: python3 with sympy 1.14 and pymupdf; node with katex (npm install); Playwright + Chromium
# installed globally (NODE_PATH points at the global modules); poppler (pdftotext, pdftoppm).
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
OUT=out/sample
PDF=$OUT/MATH111_Quiz2_Shortcuts_Sample.pdf
mkdir -p $OUT

python3 tools/render_booklet.py
node tools/render_math.mjs src/booklet.html src/booklet.katex.html > $OUT/katex.json
node tools/export_pdf.mjs src/booklet.katex.html $OUT/pass1.pdf > $OUT/export_pass1.json
python3 tools/page_map.py $OUT/pass1.pdf $OUT/toc.json
node tools/export_pdf.mjs src/booklet.katex.html $PDF $OUT/toc.json > $OUT/export_pass2.json
python3 tools/page_map.py $PDF $OUT/toc_check.json
cmp -s $OUT/toc.json $OUT/toc_check.json || { echo "page numbers moved between passes"; exit 1; }

python3 tools/qa_pdf.py $PDF src/booklet.html src/booklet.katex.html $OUT/export_pass2.json --report reports/pdf_qa_sample.json
python3 tools/leak_check.py src/booklet.katex.html $PDF --report reports/leak_check.json
echo "built $PDF"

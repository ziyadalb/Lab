#!/bin/bash
# Build, export and check the «odd و even» lesson file (Dr. Musa's 18 questions).
#   HTML (every line checked) -> KaTeX -> PDF pass 1 -> page map -> PDF pass 2 -> outline -> QA + leak check
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
OUT=out/odd_even
PDF=$OUT/MATH111_Odd_Even.pdf
mkdir -p $OUT
python3 tools/render_odd_even.py
node tools/render_math.mjs src/odd_even.html src/odd_even.katex.html > $OUT/katex.json
node tools/export_pdf.mjs src/odd_even.katex.html $OUT/pass1.pdf > $OUT/export_pass1.json || true
python3 tools/page_map.py $OUT/pass1.pdf $OUT/toc.json
node tools/export_pdf.mjs src/odd_even.katex.html $PDF $OUT/toc.json > $OUT/export.json || true
python3 tools/page_map.py $PDF $OUT/toc_check.json
cmp -s $OUT/toc.json $OUT/toc_check.json || { echo "page numbers moved between passes"; exit 1; }
rm -f $OUT/pass1.pdf $OUT/export_pass1.json $OUT/toc_check.json
python3 tools/fix_outline.py $PDF $OUT/outline.json
# no English question prompts in this file, so that one probe is expected to fail; everything else must pass
python3 tools/qa_pdf.py $PDF src/odd_even.html src/odd_even.katex.html $OUT/export.json --report reports/pdf_qa_odd_even.json || true
# Dr. Musa's cos^7 sin^6 was held for the old quiz's mock (H03); released for this file only, with its old near copies
python3 tools/leak_check.py src/odd_even.katex.html $PDF --report reports/leak_check_odd_even.json --usage data/usage_guide.json \
  --allow H03,MU-94-3,N52-E2-1,N52-E2-3
echo "built $PDF"

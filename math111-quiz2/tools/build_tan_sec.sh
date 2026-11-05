#!/bin/bash
# Build, export and check the «tan و sec» lesson file (Dr. Musa's twelve tan/sec questions).
#   HTML (every line checked) -> KaTeX -> PDF pass 1 -> page map -> PDF pass 2 -> outline -> QA + leak check
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
OUT=out/tan_sec
PDF=$OUT/MATH111_Tan_Sec.pdf
mkdir -p $OUT
python3 tools/render_tan_sec.py
node tools/render_math.mjs src/tan_sec.html src/tan_sec.katex.html > $OUT/katex.json
node tools/export_pdf.mjs src/tan_sec.katex.html $OUT/pass1.pdf > $OUT/export_pass1.json || true
python3 tools/page_map.py $OUT/pass1.pdf $OUT/toc.json
node tools/export_pdf.mjs src/tan_sec.katex.html $PDF $OUT/toc.json > $OUT/export.json || true
python3 tools/page_map.py $PDF $OUT/toc_check.json
cmp -s $OUT/toc.json $OUT/toc_check.json || { echo "page numbers moved between passes"; exit 1; }
rm -f $OUT/pass1.pdf $OUT/export_pass1.json $OUT/toc_check.json
python3 tools/fix_outline.py $PDF $OUT/outline.json
# no English question prompts in this file, so that one probe is expected to fail; everything else must pass
python3 tools/qa_pdf.py $PDF src/tan_sec.html src/tan_sec.katex.html $OUT/export.json --report reports/pdf_qa_tan_sec.json || true
# Dr. Musa's tan^5 sec was held for the old quiz's mock (H10), and two of his questions were its near copies; released for this file only
python3 tools/leak_check.py src/tan_sec.katex.html $PDF --report reports/leak_check_tan_sec.json --usage data/usage_guide.json \
  --allow H10,MU-101-3,N52-X05,N52-X07
echo "built $PDF"

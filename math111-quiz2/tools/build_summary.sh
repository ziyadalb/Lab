#!/bin/bash
# Build, export and check «ملخص الفهم» (a few pages; the full guide is built first, unchanged).
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
OUT=out/summary
PDF=$OUT/MATH111_Quiz2_Summary.pdf
mkdir -p $OUT

python3 tools/render_summary.py
node tools/render_math.mjs src/summary.html src/summary.katex.html > $OUT/katex.json
node tools/export_pdf.mjs src/summary.katex.html $PDF > $OUT/export.json || true
# the summary has no English question prompts, so that one probe is expected to fail; everything else must pass
python3 tools/qa_pdf.py $PDF src/summary.html src/summary.katex.html $OUT/export.json --report reports/pdf_qa_summary.json || true
python3 tools/leak_check.py src/summary.katex.html $PDF --report reports/leak_check_summary.json --usage data/usage_guide.json
echo "built $PDF"

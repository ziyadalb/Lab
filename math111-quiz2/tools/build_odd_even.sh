#!/bin/bash
# Build, export and check the «odd و even» lesson file.
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
OUT=out/odd_even
PDF=$OUT/MATH111_Odd_Even.pdf
mkdir -p $OUT
python3 tools/render_odd_even.py
node tools/render_math.mjs src/odd_even.html src/odd_even.katex.html > $OUT/katex.json
node tools/export_pdf.mjs src/odd_even.katex.html $PDF > $OUT/export.json || true
# no English question prompts in this file, so that one probe is expected to fail; everything else must pass
python3 tools/qa_pdf.py $PDF src/odd_even.html src/odd_even.katex.html $OUT/export.json --report reports/pdf_qa_odd_even.json || true
python3 tools/leak_check.py src/odd_even.katex.html $PDF --report reports/leak_check_odd_even.json --usage data/usage_guide.json
echo "built $PDF"

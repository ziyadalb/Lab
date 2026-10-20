#!/bin/bash
# Build, export and check the mock exams file.
#   HTML (every solution line checked while building) -> KaTeX -> PDF -> QA
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
OUT=out/mocks
PDF=$OUT/MATH111_Quiz2_Mock_Exams.pdf
mkdir -p $OUT

python3 tools/render_mocks.py
node tools/render_math.mjs src/mocks.html src/mocks.katex.html > $OUT/katex.json
node tools/export_pdf.mjs src/mocks.katex.html $PDF > $OUT/export.json || true
python3 tools/qa_pdf.py $PDF src/mocks.html src/mocks.katex.html $OUT/export.json --report reports/pdf_qa_mocks.json
echo "built $PDF"

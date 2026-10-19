#!/bin/bash
# Build, export and check the full study guide.
#   HTML (every line checked while building) -> KaTeX -> PDF pass 1 -> page map -> PDF pass 2 -> QA + leak check
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
OUT=out/guide
PDF=$OUT/MATH111_Quiz2_Guide.pdf
mkdir -p $OUT

python3 tools/render_guide.py
node tools/render_math.mjs src/guide.html src/guide.katex.html > $OUT/katex.json
node tools/export_pdf.mjs src/guide.katex.html $OUT/pass1.pdf > $OUT/export_pass1.json || true
python3 tools/page_map.py $OUT/pass1.pdf $OUT/toc.json
node tools/export_pdf.mjs src/guide.katex.html $PDF $OUT/toc.json > $OUT/export_pass2.json || true
python3 tools/page_map.py $PDF $OUT/toc_check.json
cmp -s $OUT/toc.json $OUT/toc_check.json || { echo "page numbers moved between passes"; exit 1; }

python3 tools/qa_pdf.py $PDF src/guide.html src/guide.katex.html $OUT/export_pass2.json --report reports/pdf_qa_guide.json
python3 tools/leak_check.py src/guide.katex.html $PDF --report reports/leak_check_guide.json --usage data/usage_guide.json
echo "built $PDF"

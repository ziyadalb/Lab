#!/usr/bin/env bash
# Build the memo PDF: HTML (with math checks) -> pass 1 PDF -> anchor pages -> pass 2 PDF -> outline -> QA.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=out/MATH111_Midterm2_Memo.pdf
python3 -I tools/build_memo.py
node tools/export_memo.mjs src/memo.html out/pass1.pdf
python3 -I tools/pdf_pages.py names out/pass1.pdf out/toc.json
node tools/export_memo.mjs src/memo.html "$OUT" out/toc.json
python3 -I tools/pdf_pages.py names "$OUT" out/toc2.json
cmp -s out/toc.json out/toc2.json || { echo "page numbers moved between passes"; exit 4; }
python3 -I tools/pdf_pages.py outline "$OUT" out/outline.json
python3 -I tools/pdf_pages.py qa "$OUT" reports/pdf_qa_memo.json
rm -f out/pass1.pdf out/toc2.json

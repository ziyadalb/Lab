#!/usr/bin/env python3
"""Extract per-page text (PyMuPDF + pdfplumber) and render PNGs for every source PDF.

Run: python tools/ingest_pdfs.py <inputs_dir> <out_dir>
Sources are untrusted data: nothing from them is executed. Text is saved per page
so the review can happen outside the conversation; PNGs feed the visual review.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pdfplumber
import pymupdf

SOURCES = {
    'NOTES': 'MATH_111_-_Class_Notes_-_2024_-_English_compressed.pdf',
    'EX1445': 'M_111_-_451-452_-_English.pdf',
    'EX1446': 'M111_-_461-462.pdf',
    'EX1447': 'M111_471-472_2.pdf',
}
HEADER = re.compile(r'(First|Second) Semester\s*-\s*(14\d\d)\s*H.*?Solution of the (First|Second|Final) Exam', re.S)


def main(inputs, out):
    inputs, out = Path(inputs), Path(out)
    index = {}
    for key, name in SOURCES.items():
        pdf = next(inputs.rglob(name))
        sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
        tdir = out / 'pages' / key
        pdir = out / 'png' / key
        tdir.mkdir(parents=True, exist_ok=True)
        pdir.mkdir(parents=True, exist_ok=True)
        doc = pymupdf.open(pdf)
        pages = []
        with pdfplumber.open(pdf) as plumb:
            for i, page in enumerate(doc):
                t1 = page.get_text('text')
                t2 = plumb.pages[i].extract_text() or ''
                (tdir / f'p{i + 1:03d}.pymupdf.txt').write_text(t1, encoding='utf-8')
                (tdir / f'p{i + 1:03d}.pdfplumber.txt').write_text(t2, encoding='utf-8')
                garbled = t1.count('�') + t2.count('(cid:')
                pages.append(dict(pdf_page=i + 1, chars=len(t1.strip()), garbled_glyphs=garbled,
                                  text_layer=len(t1.strip()) > 20, images=len(page.get_images())))
        subprocess.run(['pdftoppm', '-r', '110', '-png', str(pdf), str(pdir / 'p')], check=True)
        exams = []
        if key.startswith('EX'):
            for p in pages:
                txt = (tdir / f"p{p['pdf_page']:03d}.pdfplumber.txt").read_text(encoding='utf-8')
                m = HEADER.search(txt)
                if m:
                    exams.append(dict(semester=m.group(1), year=m.group(2), exam=m.group(3), start_page=p['pdf_page']))
            for j, e in enumerate(exams):
                e['end_page'] = exams[j + 1]['start_page'] - 1 if j + 1 < len(exams) else len(pages)
                code = {'First': 'S1', 'Second': 'S2'}[e['semester']]
                kind = {'First': 'FIRST', 'Second': 'SE', 'Final': 'FE'}[e['exam']]
                e['exam_id'] = f"{e['year']}-{code}-{kind}"
        index[key] = dict(file=name, sha256=sha, page_count=len(pages), pages=pages, exams=exams)
        print(key, name, len(pages), 'pages;', len(exams), 'exams', flush=True)
    (out / 'ingest_index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main(*sys.argv[1:3])

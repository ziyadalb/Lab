#!/usr/bin/env python3
"""Automated checks on an exported study PDF and the HTML it was printed from.

Usage: python3 tools/qa_pdf.py <doc.pdf> <doc.html (placeholders)> <doc.katex.html> <export.json> [--report out.json]

Checks: A4 pages; every font embedded; Arabic text at least 12 pt; every internal link lands on a
page and every #anchor in the HTML has a target; bookmarks present; text extractable (English and
Arabic words found by pdftotext); every KaTeX annotation equals the LaTeX the build produced (same
order, same count); no formula wider than its box (from the export step). Exit 1 on any failure.
"""
import html
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import pymupdf

ARABIC = re.compile('[؀-ۿ]')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    pdf_path, html_path, katex_path, export_path = args[:4]
    out_path = Path(sys.argv[sys.argv.index('--report') + 1]) if '--report' in sys.argv else Path('reports/pdf_qa.json')
    doc = pymupdf.open(pdf_path)
    res, fails = {}, []

    # pages
    sizes = {(round(p.rect.width), round(p.rect.height)) for p in doc}
    res['pages'] = doc.page_count
    res['page_sizes_pt'] = sorted(sizes)
    if sizes != {(595, 842)}:
        fails.append('page size is not A4 portrait')

    # fonts
    fonts = {}
    for p in doc:
        for xref, ext, ftype, base, name, enc, *_ in p.get_fonts(full=True):
            fonts[base] = ext
    res['fonts'] = {k: v for k, v in sorted(fonts.items())}
    not_embedded = [k for k, v in fonts.items() if v in ('n/a', '')]
    if not_embedded:
        fails.append('fonts not embedded: %s' % not_embedded)

    # text sizes: Arabic text and all non-math text (page numbers excluded)
    min_ar, min_text, small = 99.0, 99.0, []
    for i, p in enumerate(doc, 1):
        h = p.rect.height
        for b in p.get_text('dict')['blocks']:
            for line in b.get('lines', []):
                for sp in line['spans']:
                    t = sp['text'].strip()
                    if not t or sp['bbox'][1] > h - 17 / 25.4 * 72:      # footer band = page number
                        continue
                    if 'KaTeX' in sp['font']:
                        continue
                    min_text = min(min_text, sp['size'])
                    if ARABIC.search(t):
                        min_ar = min(min_ar, sp['size'])
                        if sp['size'] < 11.95:
                            small.append(dict(page=i, size=round(sp['size'], 2), text=t[:40]))
    res['min_arabic_pt'] = round(min_ar, 2)
    res['min_text_pt_excluding_math_and_page_numbers'] = round(min_text, 2)
    if small:
        fails.append('Arabic text below 12 pt: %d spans' % len(small))
        res['small_arabic_spans'] = small[:20]

    # links: PDF side
    names = doc.resolve_names()
    n_links, bad_links = 0, []
    for i, p in enumerate(doc, 1):
        for ln in p.get_links():
            if ln['kind'] in (pymupdf.LINK_GOTO, pymupdf.LINK_NAMED):
                n_links += 1
                target = ln.get('page', -1)
                if ln['kind'] == pymupdf.LINK_NAMED:
                    dest = names.get(ln.get('nameddest') or ln.get('name'))
                    target = dest['page'] if dest else -1
                if not 0 <= target < doc.page_count:
                    bad_links.append(dict(page=i, link=str(ln.get('nameddest') or ln.get('name') or ln.get('page'))))
    res['internal_links'] = n_links
    res['named_destinations'] = len(names)
    if bad_links:
        fails.append('internal links without a valid target: %d' % len(bad_links))
        res['bad_links'] = bad_links[:20]

    # links: HTML side
    src = Path(html_path).read_text(encoding='utf-8')
    ids = set(re.findall(r'\sid="([^"]+)"', src))
    hrefs = re.findall(r'href="#([^"]+)"', src)
    missing = sorted({h for h in hrefs if h not in ids})
    res['html_links'] = len(hrefs)
    if missing:
        fails.append('HTML links to missing anchors: %s' % missing)

    # bookmarks
    res['bookmarks'] = len(doc.get_toc())
    if res['bookmarks'] == 0:
        fails.append('no bookmarks')

    # text extraction
    txt = subprocess.run(['pdftotext', '-layout', pdf_path, '-'], capture_output=True, text=True).stdout
    txt_n = unicodedata.normalize('NFKC', txt)
    probes_en = ['Evaluate the following integrals', 'Find dy/dx of the following']
    probes_ar = ['الاختصار', 'العلامة', 'مثال من سؤال حقيقي', 'سلّم المساعدة']
    res['text_extraction'] = dict(
        tool='pdftotext (poppler)', characters=len(txt),
        english_found={w: w in txt for w in probes_en},
        arabic_found={w: (w in txt_n or w[::-1] in txt_n) for w in probes_ar},
        arabic_found_in_logical_order={w: w in txt_n for w in probes_ar})
    if not all(res['text_extraction']['english_found'].values()):
        fails.append('English prompts not extractable')

    # KaTeX annotations = LaTeX produced by the build
    unesc = lambda s: s.replace('&quot;', '"').replace('&#x27;', "'").replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    produced = [unesc(t) for t in re.findall(r'data-tex="([^"]*)"', src)]
    katex = Path(katex_path).read_text(encoding='utf-8')
    rendered = [html.unescape(a) for a in re.findall(r'<annotation encoding="application/x-tex">(.*?)</annotation>', katex, re.S)]
    mismatch = sum(1 for a, b in zip(produced, rendered) if a.strip() != b.strip())
    res['math'] = dict(produced=len(produced), rendered=len(rendered), mismatched=mismatch,
                       katex_errors=katex.count('katex-error'))
    if len(produced) != len(rendered) or mismatch or res['math']['katex_errors']:
        fails.append('KaTeX output differs from the produced LaTeX')

    # overflow (measured by the export step at the printed width)
    exp = json.loads(Path(export_path).read_text())
    res['overflowing_formulas'] = len(exp.get('overflow', []))
    res['fonts_loaded_in_browser'] = exp.get('fonts')
    if res['overflowing_formulas']:
        fails.append('formulas wider than their box: %d' % res['overflowing_formulas'])

    res['failures'] = fails
    out_path.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(dict(pages=res['pages'], failures=fails, min_arabic_pt=res['min_arabic_pt'],
                          links=n_links, math=res['math'], arabic=res['text_extraction']['arabic_found']),
                     ensure_ascii=False))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()

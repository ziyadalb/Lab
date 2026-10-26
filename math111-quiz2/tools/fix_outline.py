"""Replace the PDF outline Chromium writes (one bookmark per heading, about 380, with the Arabic words in the wrong
order) by a short one in reading order: the sections, the cases under them (⭐ on the core ones), the end pages.

Usage: python3 tools/fix_outline.py <guide.pdf> <outline.json>
outline.json (written by tools/render_guide.py): [[level, title, [anchor, fallback anchor, …]], …]
The page of an anchor is its named destination in the PDF (Chromium writes one per linked id). The contents
page has no link to it: it is page 2, right after the cover.
"""
import json
import os
import sys

import pymupdf


def build(pdf, spec):
    doc = pymupdf.open(pdf)
    pages = {name: dest['page'] + 1 for name, dest in doc.resolve_names().items() if dest.get('page', -1) >= 0}
    toc, missing = [], []
    for level, title, anchors in json.loads(open(spec, encoding='utf-8').read()):
        page = next((pages[a] for a in anchors if a in pages), 2 if anchors == ['toc'] else None)
        if page is None:
            missing.append(anchors[0])
            continue
        toc.append([level, title, page])
    if missing:
        raise SystemExit('outline: no page for ' + ', '.join(missing))
    if any(b[2] < a[2] for a, b in zip(toc, toc[1:])):
        raise SystemExit('outline: pages go backwards')
    doc.set_toc(toc)
    tmp = pdf + '.tmp'
    doc.save(tmp, garbage=1, deflate=True)
    doc.close()
    os.replace(tmp, pdf)
    # read it back: same entries, same order, the named destinations (the links) still there
    back = pymupdf.open(pdf)
    got = [[lvl, title, page] for lvl, title, page in back.get_toc(simple=True)]
    if got != toc:
        raise SystemExit('outline: read back differs from what was written')
    if len(back.resolve_names()) < len(pages):
        raise SystemExit('outline: named destinations lost while saving')
    return dict(entries=len(toc), top=sum(1 for t in toc if t[0] == 1), pages=back.page_count)


if __name__ == '__main__':
    print(json.dumps(build(sys.argv[1], sys.argv[2]), ensure_ascii=False))

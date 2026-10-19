"""Page number of every named destination (HTML id) in a printed PDF, for the second export pass.

Usage: python3 tools/page_map.py <pass1.pdf> <toc.json>
Chromium writes one named destination per linked id, so the table of contents can be filled with
the pages of the first pass; the second pass only changes digits inside the contents page.
"""
import json
import sys

import pymupdf


def page_map(pdf):
    doc = pymupdf.open(pdf)
    return {name: dest['page'] + 1 for name, dest in doc.resolve_names().items() if dest.get('page', -1) >= 0}


if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    m = page_map(src)
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(m, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(json.dumps(dict(destinations=len(m), pages=pymupdf.open(src).page_count)))

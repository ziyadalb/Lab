#!/usr/bin/env python3
"""Build «ملخص الفهم» (src/summary.html): what to memorise, the tree, and the decision table of the cases.

It builds the full guide first (same checks, same case numbers), then the summary from the same parts; the page
numbers of the worked examples come from the last full build (out/guide/toc.json).
Run: python3 tools/render_summary.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'content'))

import render_guide as RG  # noqa: E402
import booklet_engine as E  # noqa: E402
import guide_kit as K  # noqa: E402
import guide_summary as S  # noqa: E402
from bidi import isolate_runs  # noqa: E402


def main():
    RG.main()
    pages = json.loads((ROOT / 'out' / 'guide' / 'toc.json').read_text(encoding='utf-8'))
    body = S.build(pages, [(key, uids) for key, _, uids in RG.SECTIONS if key in K.METHODS])
    body = isolate_runs(K.renum(body))
    tpl = (ROOT / 'src' / 'template.html').read_text(encoding='utf-8')
    (ROOT / 'src' / 'summary.html').write_text(tpl.replace('{{TITLE}}', 'ملخص الفهم').replace('{{BODY}}', body), encoding='utf-8')
    print('summary ok', E.write_log('summary'))


if __name__ == '__main__':
    main()

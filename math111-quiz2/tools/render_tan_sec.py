#!/usr/bin/env python3
"""Build the «tan و sec» lesson file (src/tan_sec.html) on Dr. Musa's twelve tan/sec questions (pp. 98–107); every line
is checked while building. Also writes its PDF outline (out/tan_sec/outline.json) for tools/fix_outline.py.
Run: python3 tools/render_tan_sec.py"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'content'))

import booklet_engine as E  # noqa: E402
import tan_sec  # noqa: E402
from bidi import isolate_runs  # noqa: E402

body = isolate_runs(tan_sec.build())
tpl = (ROOT / 'src' / 'template.html').read_text(encoding='utf-8')
tpl = tpl.replace('<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="style.css">\n<link rel="stylesheet" href="tan_sec.css">')
(ROOT / 'src' / 'tan_sec.html').write_text(tpl.replace('{{TITLE}}', 'tan و sec').replace('{{BODY}}', body), encoding='utf-8')
(ROOT / 'out' / 'tan_sec').mkdir(parents=True, exist_ok=True)
(ROOT / 'out' / 'tan_sec' / 'outline.json').write_text(json.dumps(tan_sec.OUTLINE, ensure_ascii=False), encoding='utf-8')
print('tan_sec ok', E.write_log('tan_sec'), len(E.LOG), 'checks')

#!/usr/bin/env python3
"""Build the «odd و even» lesson file (src/odd_even.html) on Dr. Musa's 18 questions; every line is checked while
building. Also writes its PDF outline (out/odd_even/outline.json) for tools/fix_outline.py.
Run: python3 tools/render_odd_even.py"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'content'))

import booklet_engine as E  # noqa: E402
import odd_even  # noqa: E402
from bidi import isolate_runs  # noqa: E402

body = isolate_runs(odd_even.build())
tpl = (ROOT / 'src' / 'template.html').read_text(encoding='utf-8')
(ROOT / 'src' / 'odd_even.html').write_text(tpl.replace('{{TITLE}}', 'odd و even').replace('{{BODY}}', body), encoding='utf-8')
(ROOT / 'out' / 'odd_even').mkdir(parents=True, exist_ok=True)
(ROOT / 'out' / 'odd_even' / 'outline.json').write_text(json.dumps(odd_even.OUTLINE, ensure_ascii=False), encoding='utf-8')
print('odd_even ok', E.write_log('odd_even'), len(E.LOG), 'checks')

#!/usr/bin/env python3
"""Check that no held-out mock question (or a near copy of one) appears in a study document.

Usage: python3 tools/leak_check.py <document.katex.html> [<document.pdf>] [--report reports/leak_check.json]

Held = data/holdout_ids.json: the 10 held items and their exact copies; 'avoid' = near copies of a
held item (constant multiple / one number changed). Checks, all against the document actually produced:
  1. ids:        no held or avoid item id and no held or avoid source label (year, semester, question,
                 page) in the HTML or the PDF text; no avoid item used;
  2. text:       the LaTeX token sequence of each held or avoid question (functions, powers, numbers,
                 variables) is not contained in any rendered formula (KaTeX annotation), nor is any
                 sum inside it with five or more tokens (a radicand such as 4x^2+8x+20);
  3. symbolic:   every real question used in the document (data/usage.json) is compared with SymPy
                 to every held question: exact, constant multiple or one number changed = leak;
  4. structure:  a rendered formula with the same token sequence as a held question once numbers are
                 masked, or a used question of the same shape with several numbers changed, is listed
                 for manual review (audit/leak_review.md), not a failure: the shortcuts are taught on
                 same-shape questions by design.
Exit code 1 if any check 1-3 fails.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'content'))

from booklet import source_label  # noqa: E402
from booklet_engine import HOLD, ITEMS, q_tex  # noqa: E402
from mathlib import P, plain, tex  # noqa: E402
from similarity import relation  # noqa: E402

import sympy as s  # noqa: E402

SKIP = {r'\left', r'\right', r'\frac', r'\dfrac', r'\tfrac', r'\sqrt', r'\displaystyle', r'\operatorname',
        r'\mathrm', r'\quad', r'\qquad', r'\,', r'\cdot', r'\int', r'\big', r'\Big'}
TOKEN = re.compile(r'\\[A-Za-z]+|\d+|[a-zA-Z]|\^')


def tokens(latex):
    """Functions, powers, numbers and letters of a formula, without layout commands and without dx."""
    raw = [t for t in TOKEN.findall(latex) if t not in SKIP]
    out, i = [], 0
    while i < len(raw):
        if raw[i] == 'd' and raw[i + 1:i + 2] == ['x']:
            i += 2
            continue
        out.append(raw[i])
        i += 1
    return out


def masked(toks):
    return ['#' if t.isdigit() else t for t in toks]


def contains(seq, sub):
    n = len(sub)
    return n > 0 and any(seq[i:i + n] == sub for i in range(len(seq) - n + 1))


def held_set():
    held = dict(HOLD['held_items'])                       # item id -> Hxx
    for pid, copies in HOLD['held_copies'].items():
        for c in copies:
            held[c] = held[pid] + ' (copy)'
    return held


def subexpressions(item):
    """Sums inside a held question (radicands, denominators, arguments) printed as in the documents."""
    q = item['q'][4:] if item['q'].startswith('raw:') else item['q']
    e = plain(P(q, evaluate=False))
    out = []
    for sub in s.preorder_traversal(e):
        if sub is not e and sub.is_Add:
            toks = tokens(tex(sub))
            if len(toks) >= 5:
                out.append((tex(sub), toks))
    return out


def commands(toks):
    return sum(1 for t in toks if t.startswith('\\'))


def main():
    args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and not sys.argv[i - 1].startswith('--')]
    report_path = ROOT / 'reports' / 'leak_check.json'
    if '--report' in sys.argv:
        report_path = Path(sys.argv[sys.argv.index('--report') + 1])
    doc = Path(args[0]).read_text(encoding='utf-8')
    pdf_text = ''
    if len(args) > 1:
        pdf_text = subprocess.run(['pdftotext', '-layout', args[1], '-'], capture_output=True, text=True).stdout
    annotations = [html.unescape(a) for a in re.findall(r'<annotation encoding="application/x-tex">(.*?)</annotation>', doc, re.S)]
    ann_tokens = [tokens(a) for a in annotations]
    plain = html.unescape(re.sub(r'<[^>]+>', ' ', doc))
    usage_file = Path(sys.argv[sys.argv.index('--usage') + 1]) if '--usage' in sys.argv else ROOT / 'data' / 'usage.json'
    usage = json.loads(usage_file.read_text(encoding='utf-8'))
    held = held_set()
    avoid = {a: 'near copy %d' % n for n, a in enumerate(HOLD['avoid'], 1)}
    failures, review, seen = [], [], set()
    for item_id, tag in sorted(held.items()) + sorted(avoid.items()):
        it = ITEMS[item_id]
        # 1. ids and source labels; near copies may not be used at all
        label = source_label(it)
        for where, text in (('html', plain), ('pdf', pdf_text)):
            if item_id in text:
                failures.append(dict(check='id', item=tag, where=where))
            if label in text:
                failures.append(dict(check='source label', item=tag, where=where))
        if item_id in usage:
            failures.append(dict(check='used', item=tag, where=usage[item_id]['location']))
        # 2. a rendered formula contains the question itself
        qt = tokens(q_tex(it))
        for k, at in enumerate(ann_tokens):
            if contains(at, qt):
                failures.append(dict(check='text', item=tag, formula_no=k, formula=annotations[k][:120]))
            elif item_id in held and (masked(at) == masked(qt) or (commands(qt) >= 2 and contains(masked(at), masked(qt)))):
                key = (tag, annotations[k])
                if key not in seen:
                    seen.add(key)
                    review.append(dict(check='same shape in a formula', item=tag, formula=annotations[k][:120]))
        # 2b. a sum inside the question (e.g. its radicand) shown on its own
        for sub_tex, st in subexpressions(it):
            for k, at in enumerate(ann_tokens):
                if contains(at, st):
                    failures.append(dict(check='part of a held question', item=tag, part=sub_tex, formula=annotations[k][:120]))
        if item_id not in held:
            continue
        # 3. symbolic comparison with every real question used in the document
        for used_id in usage:
            rel = relation(it, ITEMS[used_id])
            if rel in ('exact', 'constant_multiple', 'one_number_changed'):
                failures.append(dict(check='symbolic', item=tag, relation=rel, used=used_id))
            elif rel == 'numbers_changed':
                review.append(dict(check='used question of the same shape, several numbers changed', item=tag,
                                   used=used_id, where=usage[used_id]['location']))
    out = dict(document=args[0], pdf=args[1] if len(args) > 1 else None, formulas_scanned=len(annotations),
               held_checked=len(held), avoid_checked=len(avoid), used_items=len(usage), failures=failures, for_manual_review=review)
    report_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(dict(formulas_scanned=len(annotations), held_checked=len(held), avoid_checked=len(avoid), used_items=len(usage),
                          failures=len(failures), for_manual_review=len(review)), ensure_ascii=False))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()

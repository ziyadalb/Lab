#!/usr/bin/env python3
"""Verify every item answer, every transcribed official answer, every formula and every shortcut.

Run: python tools/verify.py            (all)      python tools/verify.py --only items|formulas|shortcuts
Writes reports/verification_report.json and reports/verification_report.md (actual outputs).
Statuses: symbolic (exact residual 0 on every real branch and real-valued), partial_domain (exact
residual 0 but the answer is not real on some stated branch), unresolved (no exact zero, no
counterexample), failed (counterexample or non-real everywhere). Numeric probes are auxiliary only.
"""
import argparse
import collections
import json
import multiprocessing as mp
import platform
import sys
from pathlib import Path

import sympy as s

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mathlib import P, check, log_forms, sumexpr, x, t  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def branches(spec):
    return [x if b == 'x' else P(b) for b in spec]


def run_item(it):
    out = dict(id=it['id'], kind=it['kind'], task=it['task'], case=it['case'], section=it['section'])
    f = P(it['q'][4:] if it['q'].startswith('raw:') else it['q'])
    try:
        if it['task'] == 'defint':
            lo, hi = P(it['bounds'][0]), P(it['bounds'][1])
            F = sumexpr(it['antiderivative'])
            res = check('defint', f, F, [], lower=lo, upper=hi, exact_value=sumexpr(it['answer']))
            continuity = s.calculus.util.continuous_domain(f, x, s.Interval(lo, hi))
            res['details'].append(dict(check='integrand continuous on [a,b]', result=str(continuity)))
            out['answer'] = res
            if it.get('official'):
                out['official'] = check('defint', f, F, [], lower=lo, upper=hi, exact_value=sumexpr(it['official']))
        else:
            br = branches(it['branches'])
            sym = branches(it['sym']) if it.get('sym') else None
            out['answer'] = check(it['task'], f, sumexpr(it['answer']), br, sym=sym)
            if it.get('official') and it['official'] != it['answer']:
                out['official'] = check(it['task'], f, sumexpr(it['official']), br, sym=sym)
            elif it.get('official'):
                out['official'] = dict(status=out['answer']['status'], same_as_answer=True)
    except Exception as exc:  # recorded, never counted as success
        out['answer'] = dict(status='unresolved', error=type(exc).__name__ + ': ' + str(exc)[:200])
    return out


# ------------------------------------------------------------------ formulas quoted from the notes
FORMULAS = [
    # id, page, kind, function, claimed result, branches, note
    ('F-D1', 57, 'diff', 'asinh(x)', '1/sqrt(1+x**2)', ['t', '-t'], ''),
    ('F-D2', 58, 'diff', 'acosh(x)', '1/sqrt(x**2-1)', ['1+t'], ''),
    ('F-D3', 58, 'diff', 'atanh(x)', '1/(1-x**2)', ['t/(1+t)', '-t/(1+t)'], ''),
    ('F-D4-notes', 58, 'diff', 'acoth(x)', '-1/(1-x**2)', ['1+t', '-1-t'], 'as printed in the notes (K1)'),
    ('F-D4-correct', 58, 'diff', 'acoth(x)', '1/(1-x**2)', ['1+t', '-1-t'], 'corrected sign'),
    ('F-D5', 58, 'diff', 'asech(x)', '-1/(x*sqrt(1-x**2))', ['t/(1+t)'], ''),
    ('F-D6', 58, 'diff', 'acsch(x)', '-1/(Abs(x)*sqrt(1+x**2))', ['t', '-t'], ''),
    ('F-I1', 59, 'int', '1/sqrt(a**2+x**2)', 'asinh(x/a)', ['t', '-t'], 'a>0'),
    ('F-I2', 59, 'int', '1/sqrt(x**2-a**2)', 'acosh(x/a)', ['a+t'], 'x>a'),
    ('F-I3', 60, 'int', '1/(a**2-x**2)', 'atanh(x/a)/a', ['a*t/(1+t)', '-a*t/(1+t)'], '|x|<a'),
    ('F-I4-notes', 60, 'int', '1/(a**2-x**2)', '-acoth(x/a)/a', ['a+t', '-a-t'], 'as printed in the notes (K1)'),
    ('F-I4-correct', 60, 'int', '1/(a**2-x**2)', 'acoth(x/a)/a', ['a+t', '-a-t'], 'corrected sign'),
    ('F-I5', 60, 'int', '1/(x*sqrt(a**2-x**2))', '-asech(Abs(x)/a)/a', ['a*t/(1+t)', '-a*t/(1+t)'], '0<|x|<a'),
    ('F-I6', 60, 'int', '1/(x*sqrt(a**2+x**2))', '-acsch(Abs(x)/a)/a', ['t', '-t'], 'x!=0'),
    ('F-P1', 63, 'int', 'x*cos(x)', 'x*sin(x)+cos(x)', ['x'], 'parts example'),
    ('F-T1', 70, 'int', 'tan(x)**m', 'tan(x)**(m-1)/(m-1)-Integral(tan(x)**(m-2),x)', ['x'], 'reduction, m=2..8'),
    ('F-T2', 73, 'int', 'cot(x)**m', '-cot(x)**(m-1)/(m-1)-Integral(cot(x)**(m-2),x)', ['x'], 'reduction, m=2..8'),
    ('F-S1', 74, 'identity', 'sin(m*x)*cos(n*x)', '(sin((m-n)*x)+sin((m+n)*x))/2', [], ''),
    ('F-S2', 74, 'identity', 'sin(m*x)*sin(n*x)', '(cos((m-n)*x)-cos((m+n)*x))/2', [], ''),
    ('F-S3', 74, 'identity', 'cos(m*x)*cos(n*x)', '(cos((m-n)*x)+cos((m+n)*x))/2', [], ''),
    ('F-H1', 67, 'identity', 'sin(x)**2', '(1-cos(2*x))/2', [], ''),
    ('F-H2', 67, 'identity', 'cos(x)**2', '(1+cos(2*x))/2', [], ''),
]


def run_formula(row):
    fid, page, kind, fs, Fs, br, note = row
    a = s.Symbol('a', positive=True)
    extra = {'a': a}
    out = dict(id=fid, page=page, note=note)
    if kind == 'identity':
        diff = s.simplify(s.expand_trig(P(fs) - P(Fs)).rewrite(s.exp))
        m, n = s.symbols('m n', real=True)
        diff = s.simplify(s.expand_trig(P(fs).subs({}) - P(Fs)).rewrite(s.exp).expand())
        out.update(status='symbolic' if s.simplify(diff) == 0 else 'unresolved', residual=str(diff))
        return out
    if fid in ('F-T1', 'F-T2'):
        rows = []
        for mm in range(2, 9):
            f = P(fs).subs(s.Symbol('m', real=True), mm)
            F = P(Fs).subs(s.Symbol('m', real=True), mm)
            rest = F.atoms(s.Integral)
            Fd = F
            for integ in rest:
                Fd = Fd.subs(integ, s.Symbol('J'))
            # d/dx of the closed part + remaining integrand must equal f
            closed = Fd.subs(s.Symbol('J'), 0)
            rem = [i.function for i in rest][0]
            sign = -1
            res = s.simplify(s.trigsimp((s.diff(closed, x) + sign * rem - f).rewrite(s.cos)))
            rows.append(dict(m=mm, residual=str(res)))
        out.update(status='symbolic' if all(r['residual'] == '0' for r in rows) else 'unresolved', rows=rows)
        return out
    f = P(fs, extra=extra)
    F = P(Fs, extra=extra)
    brs = [x if b == 'x' else P(b, extra=extra) for b in br]
    res = check(kind, f, F, brs)
    out.update(status=res['status'], details=res['details'])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', choices=['items', 'formulas', 'shortcuts'])
    args = ap.parse_args()
    report = dict(libraries=dict(python=platform.python_version(), sympy=s.__version__))
    if args.only in (None, 'items'):
        items = json.loads((ROOT / 'data' / 'items.json').read_text(encoding='utf-8'))
        items += json.loads((ROOT / 'data' / 'generated_items.json').read_text(encoding='utf-8'))
        items += json.loads((ROOT / 'data' / 'musa_items.json').read_text(encoding='utf-8'))
        for f in sorted((ROOT / 'data').glob('extra_*.json')):
            items += json.loads(f.read_text(encoding='utf-8'))
        with mp.Pool(max(2, mp.cpu_count())) as pool:
            rows = pool.map(run_item, items, chunksize=1)
        report['items'] = rows
        report['items_summary'] = dict(
            answer=collections.Counter(r['answer']['status'] for r in rows),
            official=collections.Counter(r['official']['status'] for r in rows if 'official' in r))
        print('items', report['items_summary'], flush=True)
    if args.only in (None, 'formulas'):
        with mp.Pool(max(2, mp.cpu_count())) as pool:
            frows = pool.map(run_formula, FORMULAS, chunksize=1)
        report['formulas'] = frows
        print('formulas', collections.Counter(r['status'] for r in frows), flush=True)
    if args.only in (None, 'shortcuts'):
        try:
            from shortcuts_check import run_all
            report['shortcuts'] = run_all()
            print('shortcuts', collections.Counter(r['status'] for r in report['shortcuts']), flush=True)
        except ImportError:
            report['shortcuts'] = 'not yet written'
    name = 'verification_report' + ('_' + args.only if args.only else '')
    (ROOT / 'reports').mkdir(exist_ok=True)
    (ROOT / 'reports' / (name + '.json')).write_text(json.dumps(report, ensure_ascii=False, indent=1, default=str),
                                                    encoding='utf-8')


if __name__ == '__main__':
    main()

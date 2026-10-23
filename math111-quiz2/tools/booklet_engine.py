"""Math rows for the study documents: every displayed formula is printed from SymPy and every
claimed equality is checked before it is rendered. A failed check stops the build.
"""
import json
from pathlib import Path

import sympy as s

from mathlib import P, check, log_forms, rawtex, sumexpr, tex, texsum, x, t

ROOT = Path(__file__).resolve().parent.parent
ITEMS = {i['id']: i for i in json.loads((ROOT / 'data' / 'items.json').read_text(encoding='utf-8'))}
# extra practice written in this project (verified like the real items; labelled in the documents)
ITEMS.update({i['id']: i for i in json.loads((ROOT / 'data' / 'generated_items.json').read_text(encoding='utf-8'))})
# questions from Dr. Musa Ajjal's 1448/1449 notes (cited by page; the notes themselves are not in this repository)
ITEMS.update({i['id']: i for i in json.loads((ROOT / 'data' / 'musa_items.json').read_text(encoding='utf-8'))})
# more questions (generated or from Dr. Musa's notes) kept in separate files, one per batch of work
for _f in sorted((ROOT / 'data').glob('extra_*.json')):
    ITEMS.update({i['id']: i for i in json.loads(_f.read_text(encoding='utf-8'))})
HOLD = json.loads((ROOT / 'data' / 'holdout_ids.json').read_text())
BLOCKED = set(HOLD['held_items']) | set(HOLD['avoid']) | {c for v in HOLD['held_copies'].values() for c in v}
LOG = []          # every check performed while rendering
USED = {}         # item id -> list of places it was used


class BuildError(Exception):
    pass


def _record(kind, ok, **info):
    LOG.append(dict(kind=kind, ok=bool(ok), **info))
    if not ok:
        raise BuildError(f'{kind} failed: {info}')


def use(item_id, where, allow_held=False):
    if item_id in BLOCKED and not allow_held:
        raise BuildError(f'{item_id} is held out (or a near copy) and may not appear in study material')
    USED.setdefault(item_id, []).append(where)
    return ITEMS[item_id]


def _strip(q):
    return q[4:] if q.startswith('raw:') else q


def _integrand(item):
    """Integrand LaTeX, in parentheses when it is a sum (so the dx covers every term)."""
    body = tex(item['q'])
    return r'\left(%s\right)' % body if item['task'] != 'diff' and isinstance(P(item['q'][4:] if item['q'].startswith('raw:') else item['q'], evaluate=False), s.Add) else body


def q_tex(item):
    body = item.get('qtex') or _integrand(item)  # qtex: shown as written in the exam (log base 10)
    if item['task'] == 'diff':
        return r'y = ' + body
    if item['task'] == 'defint':
        lo, hi = tex(item['bounds'][0]), tex(item['bounds'][1])
        return r'\int_{%s}^{%s} %s\,dx' % (lo, hi, body)
    return r'\int %s\,dx' % body


def ans_tex(item, with_lhs=False):
    body = texsum(item['answer'])
    if item['task'] == 'diff':
        return (r'\frac{dy}{dx} = ' if with_lhs else '') + body
    if item['task'] == 'defint':
        return ('= ' if not with_lhs else '') + body
    return (r'\int %s\,dx = ' % _integrand(item) if with_lhs else '= ') + body + ' + C'


def branches_of(item):
    return [x if b == 'x' else P(b) for b in (item.get('sym') or item['branches'])]


def same_antiderivative(terms_or_expr, item, label):
    """Claimed antiderivative equals the item's verified answer up to a constant."""
    F = sumexpr(terms_or_expr) if isinstance(terms_or_expr, list) else terms_or_expr
    res = check('int', P(_strip(item['q'])), F, [x if b == 'x' else P(b) for b in item['branches']],
                sym=[x if b == 'x' else P(b) for b in item['sym']] if item.get('sym') else None)
    _record('antiderivative', res['status'] == 'symbolic', item=item['id'], label=label, status=res['status'])


def same_defint(terms, item, label):
    """Claimed value of a definite integral: F' = f on [a, b] and F(b) - F(a) = value, exactly."""
    f = P(_strip(item['q']))
    lo, hi = P(item['bounds'][0]), P(item['bounds'][1])
    res = check('defint', f, sumexpr(item['antiderivative']), [], lower=lo, upper=hi, exact_value=sumexpr(terms))
    _record('definite integral', res['status'] == 'symbolic', item=item['id'], label=label, status=res['status'])


def step_ok(expr, item, label):
    """A middle line of a solution (it may still contain Integral(...)): its derivative is the integrand
    on every real branch of the item, so the line equals the integral up to a constant."""
    S = P(expr) if isinstance(expr, str) else expr
    f = P(_strip(item['q']))
    brs = item.get('sym') or item['branches'] or ['x']
    ok = all(_zero(s.diff(S, x) - f, None if b == 'x' else b) for b in brs)
    _record('step', ok, item=item['id'], label=label, step=str(expr))


def diff_step_ok(expr, item, label):
    """A middle line of a derivative solution equals the verified derivative on every branch."""
    S = P(expr) if isinstance(expr, str) else expr
    brs = item['branches'] or ['x']
    ok = all(_zero(S - sumexpr(item['answer']), None if b == 'x' else b) for b in brs)
    _record('derivative step', ok, item=item['id'], label=label, step=str(expr))


def same_derivative(terms_or_expr, item, label):
    F = sumexpr(terms_or_expr) if isinstance(terms_or_expr, list) else terms_or_expr
    res = check('diff', P(_strip(item['q'])), F, [x if b == 'x' else P(b) for b in item['branches']])
    _record('derivative', res['status'] == 'symbolic', item=item['id'], label=label, status=res['status'])


def same_value(a_terms, b_terms, label, branch=None):
    """Two expressions are equal (identically, or on a branch x = phi(t))."""
    A = sumexpr(a_terms) if isinstance(a_terms, list) else (P(a_terms) if isinstance(a_terms, str) else a_terms)
    B = sumexpr(b_terms) if isinstance(b_terms, list) else (P(b_terms) if isinstance(b_terms, str) else b_terms)
    d = log_forms(A - B)
    if branch is not None:
        d = d.subs(x, P(branch))
    r = s.simplify(d)
    if r != 0:
        r = s.simplify(s.expand(s.expand_trig(r.rewrite(s.exp))))
    _record('identity', r == 0, label=label, residual=str(r))


def _zero(expr, branch=None):
    e = log_forms(expr)
    if branch is not None:
        e = e.subs(x, P(branch))
    r = s.simplify(e)
    if r != 0:
        r = s.simplify(s.trigsimp(r.rewrite(s.cos)))
    if r != 0:      # products of trig functions with different angles
        r = s.simplify(s.expand(s.expand_trig(r).rewrite(s.exp)))
    return r == 0


def parts_rows(u, dv, du, v, label, branch=None):
    """u, dv chosen; du and v claimed. Checks du = u' dx and v' = dv (on a branch x = phi(t) if given)."""
    U, DV, DU, V = P(u), P(dv), P(du), P(v)
    _record('parts_du', _zero(s.diff(U, x) - DU, branch), label=label, u=u, du=du)
    _record('parts_v', _zero(s.diff(V, x) - DV, branch), label=label, dv=dv, v=v)
    dv_tex = 'dx' if DV == 1 else tex(dv) + r'\,dx'
    return (r'u = %s \qquad dv = %s \\ du = %s\,dx \qquad v = %s'
            % (tex(u), dv_tex, tex(du), tex(v)))


def sub_row(u_of_x, du_claim, label, var='u', branch=None):
    U, DU = P(u_of_x), P(du_claim)
    _record('substitution', _zero(s.diff(U, x) - DU, branch), label=label, u=u_of_x, du=du_claim)
    dx = r'dx' if DU == 1 else r'-dx' if DU == -1 else tex(du_claim) + r'\,dx'
    return r'%s = %s \qquad d%s = %s' % (var, tex(u_of_x), var, dx)


def eq_chain(lhs_latex, rhs_list):
    return lhs_latex + ' ' + ' '.join(rhs_list)


def write_log(name):
    out = ROOT / 'reports' / f'{name}_checks.json'
    out.write_text(json.dumps(dict(checks=LOG, used=USED,
                                   counts=dict(total=len(LOG), ok=sum(c['ok'] for c in LOG))),
                              ensure_ascii=False, indent=1), encoding='utf-8')
    return out


def formula(f, F, kind='int', var='u', branches=('t', '-t'), pos=(), real=(), uprime=False, label=''):
    """A general formula row: printed from SymPy and checked (F' = f, or F = f' for 'diff').

    The display uses `var`; the check substitutes var -> x and uses positive/real parameters.
    Returns (lhs_latex, rhs_latex).
    """

    syms = {n: s.Symbol('lambda' if n == 'lam' else n, positive=True) for n in pos}
    syms.update({n: s.Symbol(n, real=True) for n in real})
    f_c, F_c = P(f, extra=dict(syms, **{var: x})), P(F, extra=dict(syms, **{var: x}))
    brs = [x if b == 'x' else P(b, extra=dict(syms)) for b in branches]
    res = check(kind, f_c, F_c, brs)
    _record('formula', res['status'] == 'symbolic', label=label, f=f, F=F, status=res['status'])
    disp = dict(syms, **{var: s.Symbol(var, real=True)})
    if kind == 'int':
        return r'\int %s\,d%s' % (rawtex(f, disp), var), rawtex(F, disp)
    return r'\frac{d}{dx}\,%s' % rawtex(f, disp), rawtex(F, disp, append="u'" if uprime else None)


def arith(latex, claims, label):
    """Hand-typed parameter/arithmetic line; each (lhs, rhs) claim is checked exactly."""
    for claim in claims:
        lhs, rhs = claim[0], claim[1]
        d = P(lhs) - P(rhs)
        if len(claim) > 2:          # the claim holds on a branch x = phi(t), t > 0 (e.g. x > 1/2)
            d = log_forms(d).subs(x, P(claim[2]))
        d = s.simplify(d)
        if d != 0:
            d = s.simplify(s.trigsimp(d.rewrite(s.cos)))
        if d != 0:
            d = s.simplify(s.expand(d.rewrite(s.exp)))
        _record('arithmetic', d == 0, label=label, claim=f'{lhs} = {rhs}', residual=str(d))
    return latex


def functional(lhs_fn, label):
    """Check a statement about arbitrary functions, given as a zero-valued SymPy builder."""
    r = s.simplify(lhs_fn())
    _record('functional', r == 0, label=label, residual=str(r))

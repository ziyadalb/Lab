"""Shared math layer: parsing authored expressions, real-domain checks, LaTeX in the notes' notation.

Every displayed formula is printed from the same SymPy string that verify.py checks.
Expressions are authored in this project (data/*.json) after visual review of the sources;
nothing from the source files is evaluated.
"""
import re
import signal

import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations
from sympy.printing.latex import LatexPrinter

x = s.Symbol('x', real=True)
t = s.Symbol('t', positive=True)
u = s.Symbol('u', real=True)
C = s.Symbol('C')

# Names the authored strings may use. Inverse hyperbolics are SymPy functions for display
# and are replaced by the notes' logarithmic forms (notes p.57) before any check.
NAMES = {n: getattr(s, n) for n in [
    'sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'sinh', 'cosh', 'tanh', 'coth', 'sech', 'csch',
    'asinh', 'acosh', 'atanh', 'acoth', 'asech', 'acsch', 'asin', 'acos', 'atan', 'asec',
    'log', 'exp', 'sqrt', 'Abs', 'Rational', 'Integer', 'pi', 'E', 'cbrt', 'real_root',
    'Integral', 'Derivative', 'Eq', 'Symbol', 'sign', 'integrate', 'diff']}
NAMES.update(x=x, t=t, u=u, e=s.E, C=C)
for name in 'a b c d k m n p q r w v h A B D'.split():
    NAMES[name] = s.Symbol(name, real=True)


def P(text, evaluate=True, extra=None):
    """Parse an authored expression string."""
    names = dict(NAMES)
    if extra:
        names.update(extra)
    if not evaluate:
        # the unevaluated parser distributes a unary minus over a bracket; -1*( keeps the bracket
        text = re.sub(r'(?<![*/])-\(', '-1*(', text)
    glob = {'__builtins__': {}, 'Mul': s.Mul, 'Add': s.Add, 'Pow': s.Pow, 'Integer': s.Integer,
            'Rational': s.Rational, 'Float': s.Float, 'Symbol': s.Symbol, 'Function': s.Function}
    return parse_expr(text, local_dict=names, global_dict=glob,
                      transformations=standard_transformations, evaluate=evaluate)


def log_forms(e):
    """Replace inverse hyperbolic functions by the notes' logarithmic forms (p.57)."""
    rep = {
        s.asinh: lambda z: s.log(z + s.sqrt(z ** 2 + 1)),
        s.acosh: lambda z: s.log(z + s.sqrt(z ** 2 - 1)),
        # inside each real domain the ratio is positive, so the notes' |.| can be dropped
        s.atanh: lambda z: s.log((1 + z) / (1 - z)) / 2,
        s.acoth: lambda z: s.log((z + 1) / (z - 1)) / 2,
        s.asech: lambda z: s.log((1 + s.sqrt(1 - z ** 2)) / z),
        s.acsch: lambda z: s.log(1 / z + s.sqrt(1 + 1 / z ** 2)),
    }
    for f, g in rep.items():
        e = e.replace(f, g)
    return e


class TimeLimit(Exception):
    pass


def _alarm(*_):
    raise TimeLimit()


signal.signal(signal.SIGALRM, _alarm)


def domain_diff(expr, var):
    """d/dvar with d log|g| = g'/g (valid where g != 0); avoids sign() artefacts."""
    logs = [z for z in s.preorder_traversal(expr) if z.func == s.log and z.args[0].func == s.Abs]
    if not logs:
        return s.diff(expr, var)
    logs = list(dict.fromkeys(logs))
    dummies = {z: s.Dummy(real=True) for z in logs}
    frozen = expr.xreplace(dummies)
    ans = s.diff(frozen, var)
    for z, dz in dummies.items():
        g = z.args[0].args[0]
        ans += s.diff(frozen, dz) * domain_diff(g, var) / g
    return ans.xreplace({v: k for k, v in dummies.items()})


def _simp(v):
    v = s.factor_terms(v)
    for step in (lambda z: s.simplify(z),
                 lambda z: s.simplify(s.powsimp(s.powdenest(z, force=False))),
                 lambda z: s.trigsimp(s.simplify(z.rewrite(s.cos))),
                 lambda z: s.simplify(z.rewrite(s.exp)),
                 lambda z: s.simplify(s.radsimp(s.together(z)))):
        if v == 0:
            return v
        try:
            v = step(v)
        except Exception:
            pass
    return v


def numeric_probe(residual, var, points):
    """Auxiliary only: max |residual| at sample points (None if not evaluable)."""
    residual = residual.subs({z: 2 for z in residual.free_symbols if z != var})
    worst = 0
    for p in points:
        try:
            val = complex(s.N(residual.subs(var, p), 30))
        except Exception:
            return None
        worst = max(worst, abs(val))
    return worst


def is_real_on(expr, var, points):
    # free parameters (like a>0 in a formula) are probed at a=2
    expr = expr.subs({z: 2 for z in expr.free_symbols if z != var})
    for p in points:
        try:
            val = complex(s.N(expr.subs(var, p), 30))
        except Exception:
            return False
        if abs(val.imag) > 1e-20:
            return False
    return True


def check(kind, f, F, branches, lower=None, upper=None, exact_value=None, seconds=25, sym=None):
    """Verify F against f on every real branch.

    kind: 'diff' (F should equal f'), 'int' (F' should equal f), 'defint' (exact value).
    branches: list of SymPy expressions x = phi(t), t > 0 (or [x] for a generic real variable).
    Returns dict(status, details). status in: symbolic, failed, unresolved.
    """
    f_l, F_l = log_forms(f), log_forms(F)
    details = []
    if kind == 'defint':
        signal.alarm(seconds)
        try:
            val = s.simplify(log_forms(exact_value) - (F_l.subs(x, upper) - F_l.subs(x, lower)))
            details.append(dict(check='F(b)-F(a) equals stated value', residual=str(val)))
            deriv = _simp(domain_diff(F_l, x) - f_l)
            details.append(dict(check="F'=f on [a,b]", residual=str(deriv)))
            ok = val == 0 and deriv == 0
        except TimeLimit:
            ok = False
            details.append(dict(check='timeout'))
        finally:
            signal.alarm(0)
        return dict(status='symbolic' if ok else 'unresolved', details=details)
    all_ok = True
    sym = sym or branches
    for b, pb in zip(sym, branches if len(branches) == len(sym) else sym):
        var = x if b == x else t
        fb = f_l if b == x else f_l.subs(x, b)
        Fb = F_l if b == x else F_l.subs(x, b)
        jac = 1 if b == x else s.diff(b, t)
        if kind == 'diff':
            raw = Fb * jac - domain_diff(fb, var)
        else:
            raw = domain_diff(Fb, var) - fb * jac
        signal.alarm(seconds)
        try:
            residual = _simp(raw)
            ok = residual == 0
            entry = dict(branch=str(b), residual=str(residual), symbolic_zero=ok)
        except TimeLimit:
            ok = False
            entry = dict(branch=str(b), residual='timeout', symbolic_zero=False)
        finally:
            signal.alarm(0)
        if b == x:
            probe_pts = [s.Rational(1, 3), s.Rational(7, 10), s.Rational(11, 10), -s.Rational(2, 5)]
        else:
            probe_pts = [s.Rational(1, 3), s.Rational(7, 10), s.Rational(3, 2), 2, s.Rational(13, 4)]
        if not ok:
            entry['numeric_max_abs'] = str(numeric_probe(raw, var, probe_pts))
        Fp = F_l if pb == x else F_l.subs(x, pb)
        entry['real_valued'] = is_real_on(Fp, x if pb == x else t, probe_pts)
        entry['probe_branch'] = str(pb)
        details.append(entry)
        all_ok = all_ok and ok and entry['real_valued']
    if all_ok:
        return dict(status='symbolic', details=details)
    if all(d['symbolic_zero'] for d in details) and any(d['real_valued'] for d in details):
        return dict(status='partial_domain', details=details)
    if any(d['symbolic_zero'] and d['real_valued'] for d in details):
        return dict(status='branch_only', details=details)
    failed = any(d.get('numeric_max_abs') not in (None, 'None') and float(d['numeric_max_abs']) > 1e-12
                 for d in details) or any(not d['real_valued'] for d in details)
    return dict(status='failed' if failed else 'unresolved', details=details)


class NotesPrinter(LatexPrinter):
    """LaTeX in the notation of Dr. Tariq's notes: sinh^{-1}, sech, ln, |x|, no 'atan'."""
    _inv = {'asinh': r'\sinh^{-1}', 'acosh': r'\cosh^{-1}', 'atanh': r'\tanh^{-1}',
            'acoth': r'\coth^{-1}', 'asech': r'\operatorname{sech}^{-1}', 'acsch': r'\operatorname{csch}^{-1}',
            'asin': r'\sin^{-1}', 'acos': r'\cos^{-1}', 'atan': r'\tan^{-1}', 'asec': r'\sec^{-1}'}

    def __init__(self, settings=None):
        base = dict(ln_notation=True, fold_short_frac=False, fold_frac_powers=True, mul_symbol=None,
                    inv_trig_style='power')
        base.update(settings or {})
        super().__init__(base)

    def _print_Function(self, expr, exp=None):
        name = expr.func.__name__
        if name in self._inv:
            arg = self._print(expr.args[0])
            head = self._inv[name]
            if exp is not None:
                return r'\left(%s\left(%s\right)\right)^{%s}' % (head, arg, exp)
            if expr.args[0].is_Symbol:
                return r'%s %s' % (head, arg)
            return r'%s\left(%s\right)' % (head, arg)
        if name in ('sech', 'csch'):
            arg = self._print(expr.args[0])
            head = r'\operatorname{%s}' % name
            if exp is not None:
                head += '^{%s}' % exp
            return r'%s\left(%s\right)' % (head, arg) if not expr.args[0].is_Symbol else r'%s %s' % (head, arg)
        simple = ('sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'sinh', 'cosh', 'tanh', 'coth')
        a0 = expr.args[0]
        if name in simple and (a0.is_Symbol or (a0.is_Mul and all(f.is_Symbol or (f.is_Integer and f > 0)
                                                                  for f in a0.args))):
            head = '\\' + name + ('^{%s}' % exp if exp is not None else '')
            return '%s %s' % (head, self._print(expr.args[0]))
        return super()._print_Function(expr, exp)

    def _print_log(self, expr, exp=None):
        z = expr.args[0]
        if z.is_Symbol or (z.is_Integer and z > 0):
            body = r'\ln %s' % self._print(z)
        elif z.func == s.Abs:
            body = r'\ln\left|%s\right|' % self._print(z.args[0])
        else:
            body = r'\ln\left(%s\right)' % self._print(z)
        return body if exp is None else r'\left(%s\right)^{%s}' % (body, exp)

    def _print_Mul(self, expr):
        if self._settings.get('order') == 'none' and any(
                f.is_Pow and f.exp.is_Integer and f.exp < -1 and f.base.is_Symbol for f in expr.args):
            return ' '.join(self.parenthesize(f, 1000) if f.is_Add else self._print(f) for f in expr.args)
        return super()._print_Mul(expr)

    def _print_Pow(self, expr):
        if (self._settings.get('order') == 'none' and expr.exp.is_Integer and expr.exp < -1
                and expr.base.is_Symbol):
            return '%s^{%s}' % (self._print(expr.base), self._print(expr.exp))
        return super()._print_Pow(expr)

    def _print_Integral(self, expr):
        return super()._print_Integral(expr).replace(r'\, dx', r'\,dx')


def plain(e):
    """Rebuild an unevaluated parse without evaluating, dropping the unit factors the parser
    leaves behind (x - 1 is parsed as x + (-1)*1), so the authored order survives printing."""
    if not e.args:
        return e
    args = [plain(a) for a in e.args]
    if e.is_Mul:
        args = [a for a in args if a != 1]
        if not args:
            return s.S.One
        if len(args) == 2:    # real_root(b, n) parses as |b|^(1/n) sign(b); show it as the n-th root of b
            pw = [a for a in args if a.is_Pow and isinstance(a.base, s.Abs) and a.exp.is_Rational and a.exp.p == 1]
            sg = [a for a in args if isinstance(a, s.sign)]
            if pw and sg and pw[0].base.args[0] == sg[0].args[0]:
                return s.Pow(sg[0].args[0], pw[0].exp, evaluate=False)
        return args[0] if len(args) == 1 else s.Mul(*args, evaluate=False)
    if e.is_Add:
        return s.Add(*args, evaluate=False)
    if e.is_Pow:
        return s.Pow(*args, evaluate=False)
    try:
        return e.func(*args, evaluate=False)
    except TypeError:
        return e.func(*args)


def _factors(e):
    if e.is_Mul:
        return [g for a in e.args for g in _factors(a)]
    return [e]


def _join(pr, fs, wrap=False):
    out = ''
    for f in fs:
        piece = r'\left(%s\right)' % pr._print(f) if f.is_Add and (len(fs) > 1 or wrap) else pr._print(f)
        if out and out[-1].isdigit() and piece[0].isdigit():
            out += r' \cdot '
        elif out:
            out += ' '
        out += piece
    return out


def _term(pr, e):
    """One authored term: numeric coefficient first (-\\frac{2}{5} e^{2x} ...), other factors in
    the authored order, non-numeric denominators as one fraction."""
    if not e.is_Mul and not (e.is_Pow and e.exp.is_Number and e.exp < 0):
        return pr._print(e)
    num, den, c = [], [], s.S.One
    for f in _factors(e):
        if f.is_Number:
            c *= f
        elif f.is_Pow and f.exp.is_Number and f.exp < 0:
            k = -f.exp
            if f.base.is_Number:
                c /= f.base ** k
                continue
            for g in (_factors(f.base) if k == 1 else [s.Pow(f.base, k, evaluate=False)]):
                if g.is_Number:
                    c /= g
                else:
                    den.append(g)
        else:
            num.append(f)
    if not c.is_Rational:
        return pr._print(e)
    sign, c = ('-' if c < 0 else ''), abs(c)
    p_, q_ = int(c.p), int(c.q)
    if not den:
        coef = '' if c == 1 else (str(p_) if q_ == 1 else r'\frac{%d}{%d}' % (p_, q_))
        body = _join(pr, num, wrap=bool(sign or coef))
        if not body:
            return sign + (coef or '1')
        if coef and body[0].isdigit():
            coef += r' \cdot'
        return sign + coef + (' ' if coef else '') + body
    free = lambda f: not ({str(z) for z in f.free_symbols} & {'x', 'u'})
    rest = [f for f in num if not free(f)]
    if (all(free(g) for g in den) and rest and rest[0].is_Function and not isinstance(rest[0], s.exp)):
        # constant denominator before a function: \frac{c}{nk}\sinh^{-1}(...), as the notes write it
        k = _join(pr, ([s.Integer(p_)] if p_ != 1 else []) + [f for f in num if free(f)]) or '1'
        d = _join(pr, ([s.Integer(q_)] if q_ != 1 else []) + den)
        return sign + r'\frac{%s}{%s} ' % (k, d) + _join(pr, rest)
    tail = []      # trailing bracket factors go after the fraction: \frac{e^{ax}}{a^2+b^2}(a sin bx - ...)
    while len(num) > 1 and num[-1].is_Add:
        tail.insert(0, num.pop())
    n = _join(pr, ([s.Integer(p_)] if p_ != 1 else []) + num) or '1'
    d = _join(pr, ([s.Integer(q_)] if q_ != 1 else []) + den)
    return sign + r'\frac{%s}{%s}' % (n, d) + ''.join(r' \left(%s\right)' % pr._print(a) for a in tail)


def rawtex(text, extra=None, append=None):
    """LaTeX of an authored expression in the authored order (for answers and formulas).
    `append` multiplies the printed expression by an extra symbol (u' in derivative tables)."""
    e = plain(P(text, evaluate=False, extra=extra))
    pr = NotesPrinter(dict(order='none'))
    if append is not None:
        if e.is_Add:
            return r'\left(%s\right) %s' % (rawtex(text, extra), append)
        body = _term(pr, e)
        if not body.lstrip('-').startswith(r'\frac'):
            return body + r' \cdot ' + append
        e = s.Mul(e, s.Symbol(append), evaluate=False)
    if e.is_Add:
        return texsum([a for a in e.args], _pr=pr)
    return _term(pr, e)


def tex(text_or_expr, **settings):
    """LaTeX of an authored expression. 'raw:' strings keep the authored order; others are
    evaluated (SymPy normalises signs and fractions)."""
    if isinstance(text_or_expr, str):
        raw = text_or_expr.startswith('raw:')
        e = plain(P(text_or_expr[4:], evaluate=False)) if raw else P(text_or_expr)
        if raw:
            settings = dict(settings, order='none')
    else:
        e = text_or_expr
    return NotesPrinter(settings).doprint(e)


def texsum(terms, _pr=None, **settings):
    """LaTeX of a sum printed in the authored order: terms is a list of expression strings
    (or unevaluated expressions); each term is printed coefficient-first."""
    pr = _pr or NotesPrinter(dict(settings, order='none'))
    out = ''
    for i, term in enumerate(terms):
        if isinstance(term, str):
            term = plain(P(term[4:] if term.startswith('raw:') else term, evaluate=False))
        body = _term(pr, term)
        if i == 0:
            out = body
        elif body.startswith('-'):
            out += ' - ' + body[1:].lstrip()
        else:
            out += ' + ' + body
    return out


def sumexpr(terms):
    """The SymPy value of an ordered term list (what verify.py checks)."""
    return s.Add(*[P(term[4:] if term.startswith('raw:') else term) for term in terms])

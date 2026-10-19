"""Shared math layer: parsing authored expressions, real-domain checks, LaTeX in the notes' notation.

Every displayed formula is printed from the same SymPy string that verify.py checks.
Expressions are authored in this project (data/*.json) after visual review of the sources;
nothing from the source files is evaluated.
"""
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
    'Integral', 'Derivative', 'Eq', 'Symbol', 'sign']}
NAMES.update(x=x, t=t, u=u, e=s.E, C=C)
for name in 'a b c d k m n p q r w v h A B D'.split():
    NAMES[name] = s.Symbol(name, real=True)


def P(text, evaluate=True, extra=None):
    """Parse an authored expression string."""
    names = dict(NAMES)
    if extra:
        names.update(extra)
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
        base = dict(ln_notation=True, fold_short_frac=False, mul_symbol=None,
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
            return r'%s\left(%s\right)' % (head, arg)
        if name in ('sech', 'csch'):
            arg = self._print(expr.args[0])
            head = r'\operatorname{%s}' % name
            if exp is not None:
                head += '^{%s}' % exp
            return r'%s\left(%s\right)' % (head, arg) if not expr.args[0].is_Symbol else r'%s %s' % (head, arg)
        simple = ('sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'sinh', 'cosh', 'tanh', 'coth')
        if name in simple and (expr.args[0].is_Symbol or (expr.args[0].is_Mul and len(expr.args[0].args) == 2
                                                           and expr.args[0].args[0].is_Number
                                                           and expr.args[0].args[1].is_Symbol)):
            head = '\\' + name + ('^{%s}' % exp if exp is not None else '')
            return '%s %s' % (head, self._print(expr.args[0]))
        return super()._print_Function(expr, exp)

    def _print_log(self, expr, exp=None):
        z = expr.args[0]
        if z.is_Symbol:
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


def tex(text_or_expr, **settings):
    """LaTeX of an authored expression (evaluated, so SymPy normalises signs and fractions)."""
    if isinstance(text_or_expr, str):
        raw = text_or_expr.startswith('raw:')
        e = P(text_or_expr[4:], evaluate=False) if raw else P(text_or_expr)
        if raw:
            settings = dict(settings, order='none')
            e = e.replace(lambda z: z.is_Mul and s.S.One in z.args,
                          lambda z: s.Mul(*[a for a in z.args if a != 1], evaluate=False))
    else:
        e = text_or_expr
    return NotesPrinter(settings).doprint(e)


def texsum(terms, **settings):
    """LaTeX of a sum printed in the authored order: terms is a list of expression strings."""
    out = ''
    for i, term in enumerate(terms):
        body = tex(term, **settings)
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

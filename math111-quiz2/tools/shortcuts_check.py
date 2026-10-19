"""The shortcuts kit: each shortcut as data (display + general check + concrete applications).

General checks use symbolic parameters with the stated conditions (proof by differentiation),
or, for recipes whose length depends on a degree (DI table, Pascal row, reduction chains),
an analytic argument recorded in audit/shortcut_study.md plus exact checks over a parameter grid.
Concrete checks apply each shortcut, as a formula, to every real question/exercise of its case and
compare with the verified answer (derivative of the difference must be 0 on the item's branches).
"""
import itertools
import json
from pathlib import Path

import sympy as s

from mathlib import P, check, log_forms, sumexpr, x, t

ROOT = Path(__file__).resolve().parent.parent
a, b, k, c = s.symbols('a b k c', positive=True)
n = s.Symbol('n', real=True)
m = s.Symbol('m', real=True)


def diff_zero(F, f, conds_subs=None, branches=(x,)):
    """d/dx F - f == 0 (symbolic, with log forms), on the given branches."""
    res = []
    for br in branches:
        Fb = log_forms(F).subs(x, br) if br != x else log_forms(F)
        fb = log_forms(f).subs(x, br) if br != x else log_forms(f)
        var = x if br == x else t
        jac = 1 if br == x else s.diff(br, t)
        r = s.simplify(s.diff(Fb, var) - fb * jac)
        if r != 0:
            r = s.simplify(r.rewrite(s.exp))
        res.append(r)
    return all(r == 0 for r in res), [str(r) for r in res]


# ------------------------------------------------------------------ general statements
def g_alqaws():
    # ∫ x^n ln|a x| dx = x^(n+1)/(n+1) * (ln|a x| - 1/(n+1)),  n != -1
    F = x ** (n + 1) / (n + 1) * (s.log(a * x) - 1 / (n + 1))
    ok, r = diff_zero(F, x ** n * s.log(a * x), branches=[t])
    return ok, 'x>0 symbolic n,a; x<0 follows since d/dx ln|ax| = 1/x on both sides', r


def g_dawaran():
    Fs = s.exp(a * x) * (a * s.sin(b * x) - b * s.cos(b * x)) / (a ** 2 + b ** 2)
    Fc = s.exp(a * x) * (a * s.cos(b * x) + b * s.sin(b * x)) / (a ** 2 + b ** 2)
    A, B = s.symbols('A B', real=True, nonzero=True)
    Fs, Fc = Fs.subs({a: A, b: B}), Fc.subs({a: A, b: B})
    ok1, r1 = diff_zero(Fs, s.exp(A * x) * s.sin(B * x))
    ok2, r2 = diff_zero(Fc, s.exp(A * x) * s.cos(B * x))
    return ok1 and ok2, 'a, b real, (a,b) != (0,0)', r1 + r2


def g_nisfayn():
    A, B = s.symbols('A B', real=True)
    Fc = (s.exp((A + B) * x) / (A + B) + s.exp((A - B) * x) / (A - B)) / 2
    Fs = (s.exp((A + B) * x) / (A + B) - s.exp((A - B) * x) / (A - B)) / 2
    ok1, r1 = diff_zero(Fc, s.exp(A * x) * s.cosh(B * x))
    ok2, r2 = diff_zero(Fs, s.exp(A * x) * s.sinh(B * x))
    # special case a = b: e^{ax}cosh(ax) = (e^{2ax}+1)/2 -> e^{2ax}/(4a) + x/2
    ok3, r3 = diff_zero(s.exp(2 * A * x) / (4 * A) + x / 2, s.exp(A * x) * s.cosh(A * x))
    ok4, r4 = diff_zero(s.exp(2 * A * x) / (4 * A) - x / 2, s.exp(A * x) * s.sinh(A * x))
    return ok1 and ok2 and ok3 and ok4, 'A != ±B; separate line when A = ±B', r1 + r2 + r3 + r4


def g_lamda():
    # ∫ dx/sqrt(b^(2kx)+a^2) = -1/(a k ln b) csch^-1(b^(kx)/a);  b>0, b!=1
    F = -s.acsch(b ** (k * x) / a) / (a * k * s.log(b))
    ok1, r1 = diff_zero(F, 1 / s.sqrt(b ** (2 * k * x) + a ** 2), branches=[x])
    # ∫ dx/(x sqrt(x^(2n)+a^2)) = -1/(n a) csch^-1(|x|^n / a)  (n>0)
    N = s.Symbol('N', positive=True)
    F2 = -s.acsch(t ** N / a) / (N * a)
    f2 = 1 / (t * s.sqrt(t ** (2 * N) + a ** 2))
    r2 = s.simplify(s.diff(log_forms(F2), t) - f2)
    # ∫ dx/(x sqrt(a^2 - x^(2n))) = -1/(n a) sech^-1(|x|^n / a)
    F3 = -s.asech(t ** N / a) / (N * a)
    f3 = 1 / (t * s.sqrt(a ** 2 - t ** (2 * N)))
    r3 = s.simplify(s.diff(log_forms(F3), t) - f3)
    return ok1 and r2 == 0 and r3 == 0, 'a>0, k>0, b>0 (b != 1); x>0 shown, x<0 by evenness with |x|', r1 + [str(r2), str(r3)]


def g_six_integrals():
    rows = [('1/sqrt(u**2+a**2)', 'asinh(u/a)', ['t', '-t']),
            ('1/sqrt(u**2-a**2)', 'acosh(u/a)', ['a+t']),
            ('1/(a**2-u**2)', 'atanh(u/a)/a', ['a*t/(1+t)', '-a*t/(1+t)']),
            ('1/(a**2-u**2)', 'acoth(u/a)/a', ['a+t', '-a-t']),
            ('1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', ['a*t/(1+t)', '-a*t/(1+t)']),
            ('1/(u*sqrt(u**2+a**2))', '-acsch(Abs(u)/a)/a', ['t', '-t'])]
    out, ok = [], True
    for f, F, br in rows:
        res = check('int', P(f.replace('u', 'x'), extra={'a': a}), P(F.replace('u', 'x'), extra={'a': a}),
                    [P(z, extra={'a': a}) for z in br])
        out.append(res['status'])
        ok = ok and res['status'] == 'symbolic'
    return ok, 'a>0 symbolic', out


def g_twins_derivatives():
    rows = [('asinh(x)', '1/sqrt(x**2+1)', ['t', '-t']), ('acosh(x)', '1/sqrt(x**2-1)', ['1+t']),
            ('atanh(x)', '1/(1-x**2)', ['t/(1+t)']), ('acoth(x)', '1/(1-x**2)', ['1+t', '-1-t']),
            ('asech(x)', '-1/(x*sqrt(1-x**2))', ['t/(1+t)']), ('acsch(x)', '-1/(Abs(x)*sqrt(1+x**2))', ['t', '-t'])]
    out = [check('diff', P(f), P(F), [P(z) for z in br])['status'] for f, F, br in rows]
    return all(o == 'symbolic' for o in out), 'chain rule multiplies by u\'', out


def g_square():
    A_, D_ = s.symbols('A D', real=True)
    B_ = s.Symbol('B', real=True)
    h = -B_ / (2 * A_)
    d = D_ - B_ ** 2 / (4 * A_)
    Q = A_ * x ** 2 + B_ * x + D_
    ok_identity = s.simplify(Q - (A_ * (x - h) ** 2 + d)) == 0 and s.simplify(Q.subs(x, h) - d) == 0
    Ap, dp = s.symbols('A_p d_p', positive=True)
    # A>0, d>0: (c/√A) sinh^-1(√A (x-h)/√d) ;  x - h = y
    y = x
    f1 = 1 / s.sqrt(Ap * y ** 2 + dp)
    r1 = check('int', f1, s.asinh(s.sqrt(Ap) * y / s.sqrt(dp)) / s.sqrt(Ap), [t, -t])['status']
    # A>0, d<0 (d=-dp): (c/√A) cosh^-1(√A (x-h)/√(-d)), x-h>√(-d/A)
    f2 = 1 / s.sqrt(Ap * y ** 2 - dp)
    r2 = check('int', f2, s.acosh(s.sqrt(Ap) * y / s.sqrt(dp)) / s.sqrt(Ap), [s.sqrt(dp / Ap) + t])['status']
    # linear factor, A>0: -(c/√d) csch^-1(√A|x-h|/√d)
    f3 = 1 / (y * s.sqrt(Ap * y ** 2 + dp))
    r3 = check('int', f3, -s.acsch(s.sqrt(Ap) * s.Abs(y) / s.sqrt(dp)) / s.sqrt(dp), [t, -t])['status']
    # linear factor, A<0 (A=-Ap): -(c/√d) sech^-1(√|A| |x-h|/√d)
    f4 = 1 / (y * s.sqrt(dp - Ap * y ** 2))
    r4 = check('int', f4, -s.asech(s.sqrt(Ap) * s.Abs(y) / s.sqrt(dp)) / s.sqrt(dp),
               [s.sqrt(dp / Ap) * t / (1 + t), -s.sqrt(dp / Ap) * t / (1 + t)])['status']
    ok = ok_identity and all(r == 'symbolic' for r in (r1, r2, r3, r4))
    return ok, 'h=-B/(2A), d=Q(h); A,d symbolic with stated signs', [ok_identity, r1, r2, r3, r4]


def g_rafeeq():
    # ∫ f^-1(x) dx = x f^-1(x) - ∫ x (f^-1)'(x) dx  and the six tabulated results
    rows = [('asin(x)', 'x*asin(x)+sqrt(1-x**2)', ['t/(1+t)', '-t/(1+t)']),
            ('atan(x)', 'x*atan(x)-log(1+x**2)/2', ['x']),
            ('asec(x)', 'x*asec(x)-acosh(x)', ['1+t']),
            ('asinh(x)', 'x*asinh(x)-sqrt(1+x**2)', ['x']),
            ('acosh(x)', 'x*acosh(x)-sqrt(x**2-1)', ['1+t']),
            ('atanh(x)', 'x*atanh(x)+log(1-x**2)/2', ['t/(1+t)', '-t/(1+t)']),
            ('x*atanh(x)', 'x**2*atanh(x)/2+x/2-atanh(x)/2', ['t/(1+t)', '-t/(1+t)']),
            ('x*asech(x)', 'x**2*asech(x)/2-sqrt(1-x**2)/2', ['t/(1+t)']),
            ('x*asec(x)', 'x**2*asec(x)/2-sqrt(x**2-1)/2', ['1+t']),
            ('x*acsch(x)', 'x**2*acsch(x)/2+sqrt(1+x**2)/2', ['t'])]
    out = [check('int', P(f), P(F), [x if z == 'x' else P(z) for z in br])['status'] for f, F, br in rows]
    return all(o == 'symbolic' for o in out), 'table rows each verified', out


def g_pascal():
    """Recipe check over a grid: build the answer by the Pascal rule and compare."""
    results = []
    U = s.Symbol('U')
    for (fam, p_, kk, sign, uf, base) in [
            ('sin^p cos^(2k+1)', None, None, 1, s.sin, lambda kk: (1 - U ** 2) ** kk),
            ('cos^p sin^(2k+1)', None, None, -1, s.cos, lambda kk: (1 - U ** 2) ** kk),
            ('tan^p sec^(2k+2)', None, None, 1, s.tan, lambda kk: (1 + U ** 2) ** kk),
            ('sec^p tan^(2k+1)', None, None, 1, s.sec, lambda kk: (U ** 2 - 1) ** kk),
            ('cot^p csc^(2k+2)', None, None, -1, s.cot, lambda kk: (1 + U ** 2) ** kk),
            ('csc^p cot^(2k+1)', None, None, -1, s.csc, lambda kk: (U ** 2 - 1) ** kk)]:
        for pp, kk in itertools.product([0, 1, 2, 3, 4, s.Rational(1, 2), s.Rational(1, 3)], [0, 1, 2, 3]):
            poly = s.Poly(s.expand(base(kk)), U)
            ans = sum(cf * uf(x) ** (pp + e[0] + 1) / (pp + e[0] + 1) for e, cf in poly.terms()) * sign
            if fam.startswith('sin^p'):
                f = s.sin(x) ** pp * s.cos(x) ** (2 * kk + 1)
            elif fam.startswith('cos^p'):
                f = s.cos(x) ** pp * s.sin(x) ** (2 * kk + 1)
            elif fam.startswith('tan^p'):
                f = s.tan(x) ** pp * s.sec(x) ** (2 * kk + 2)
            elif fam.startswith('sec^p'):
                f = s.sec(x) ** (pp + 1) * s.tan(x) ** (2 * kk + 1)
            elif fam.startswith('cot^p'):
                f = s.cot(x) ** pp * s.csc(x) ** (2 * kk + 2)
            else:
                f = s.csc(x) ** (pp + 1) * s.cot(x) ** (2 * kk + 1)
            br = t / (1 + t)  # 0<x<1: every base positive, fractional powers real
            r = s.simplify(s.trigsimp((s.diff(ans, x) - f).subs(x, br) .rewrite(s.cos)))
            if r != 0:
                r = s.simplify(s.expand_trig(r))
            results.append((fam, str(pp), kk, r == 0))
    ok = all(z[3] for z in results)
    return ok, 'grid p in {0..4,1/2,1/3}, k in {0..3}, six families', sum(1 for z in results if z[3]), len(results)


def g_folded():
    """DI table (الجدول المطوي) as a closed recipe, checked for polynomials up to degree 4."""
    res = []
    kk = s.Symbol('kk', positive=True)
    for deg in range(0, 5):
        cs = s.symbols('p0:%d' % (deg + 1))
        Pp = sum(ci * x ** i for i, ci in enumerate(cs))
        ders = [s.diff(Pp, x, j) for j in range(deg + 1)]
        e_ans = s.exp(kk * x) * sum((-1) ** j * ders[j] / kk ** (j + 1) for j in range(deg + 1))
        cos_ans = s.sin(kk * x) * sum((-1) ** j * ders[2 * j] / kk ** (2 * j + 1) for j in range((deg) // 2 + 1)) \
            + s.cos(kk * x) * sum((-1) ** j * ders[2 * j + 1] / kk ** (2 * j + 2) for j in range((deg + 1) // 2))
        sin_ans = -s.cos(kk * x) * sum((-1) ** j * ders[2 * j] / kk ** (2 * j + 1) for j in range(deg // 2 + 1)) \
            + s.sin(kk * x) * sum((-1) ** j * ders[2 * j + 1] / kk ** (2 * j + 2) for j in range((deg + 1) // 2))
        cosh_ans = s.sinh(kk * x) * sum(ders[2 * j] / kk ** (2 * j + 1) for j in range(deg // 2 + 1)) \
            - s.cosh(kk * x) * sum(ders[2 * j + 1] / kk ** (2 * j + 2) for j in range((deg + 1) // 2))
        sinh_ans = s.cosh(kk * x) * sum(ders[2 * j] / kk ** (2 * j + 1) for j in range(deg // 2 + 1)) \
            - s.sinh(kk * x) * sum(ders[2 * j + 1] / kk ** (2 * j + 2) for j in range((deg + 1) // 2))
        for name, F, g in [('exp', e_ans, s.exp(kk * x)), ('cos', cos_ans, s.cos(kk * x)), ('sin', sin_ans, s.sin(kk * x)),
                           ('cosh', cosh_ans, s.cosh(kk * x)), ('sinh', sinh_ans, s.sinh(kk * x))]:
            r = s.simplify((s.diff(F, x) - Pp * g).rewrite(s.exp))
            res.append((deg, name, r == 0))
    return all(z[2] for z in res), 'symbolic coefficients p0..p4, symbolic k>0', sum(z[2] for z in res), len(res)


def g_reduction():
    res = []
    for mm in range(2, 9):
        # ∫tan^m = tan^(m-1)/(m-1) - ∫tan^(m-2);  chain closed forms
        F = 0
        sign = 1
        j = mm
        while j >= 2:
            F += sign * s.tan(x) ** (j - 1) / (j - 1)
            sign = -sign
            j -= 2
        F += sign * (x if j == 0 else -s.log(s.cos(x)))
        r = s.simplify((s.diff(F, x) - s.tan(x) ** mm).rewrite(s.cos))
        res.append(('tan', mm, r == 0))
        Fc = 0
        sign = 1
        j = mm
        while j >= 2:
            Fc += -sign * s.cot(x) ** (j - 1) / (j - 1)
            sign = -sign
            j -= 2
        Fc += sign * (x if j == 0 else s.log(s.sin(x)))
        r = s.simplify((s.diff(Fc, x) - s.cot(x) ** mm).rewrite(s.cos))
        res.append(('cot', mm, r == 0))
    # sec^n = sec^(n-2) tan/(n-1) + (n-2)/(n-1) ∫ sec^(n-2), n = 3, 5, 7 closed forms
    def sec_int(nn):
        if nn == 1:
            return s.log(s.sec(x) + s.tan(x))
        return s.sec(x) ** (nn - 2) * s.tan(x) / (nn - 1) + s.Rational(nn - 2, nn - 1) * sec_int(nn - 2)

    def csc_int(nn):
        if nn == 1:
            return -s.log(s.csc(x) + s.cot(x))
        return -s.csc(x) ** (nn - 2) * s.cot(x) / (nn - 1) + s.Rational(nn - 2, nn - 1) * csc_int(nn - 2)
    for nn in (3, 5, 7):
        br = t / (1 + t)
        r = s.simplify(s.trigsimp((s.diff(sec_int(nn), x) - s.sec(x) ** nn).subs(x, br).rewrite(s.cos)))
        res.append(('sec', nn, r == 0))
        r = s.simplify(s.trigsimp((s.diff(csc_int(nn), x) - s.csc(x) ** nn).subs(x, br).rewrite(s.cos)))
        res.append(('csc', nn, r == 0))
    return all(z[2] for z in res), 'tan/cot m=2..8; sec/csc n=3,5,7', [z for z in res if not z[2]]


def g_products():
    M, N = s.symbols('M N', positive=True)
    rows = [(s.sin(M * x) * s.cos(N * x), -(s.cos((M - N) * x) / (M - N) + s.cos((M + N) * x) / (M + N)) / 2),
            (s.sin(M * x) * s.sin(N * x), (s.sin((M - N) * x) / (M - N) - s.sin((M + N) * x) / (M + N)) / 2),
            (s.cos(M * x) * s.cos(N * x), (s.sin((M - N) * x) / (M - N) + s.sin((M + N) * x) / (M + N)) / 2)]
    out = [s.simplify(s.expand_trig(s.diff(F, x) - f).rewrite(s.exp).expand()) == 0 for f, F in rows]
    return all(out), 'M != N', out


def g_even():
    K = s.Symbol('K', positive=True)
    rows = [(s.sin(K * x) ** 2, x / 2 - s.sin(2 * K * x) / (4 * K)), (s.cos(K * x) ** 2, x / 2 + s.sin(2 * K * x) / (4 * K)),
            (s.sin(x) ** 2 * s.cos(x) ** 2, x / 8 - s.sin(4 * x) / 32)]
    out = [s.simplify(s.diff(F, x) - f) == 0 for f, F in rows]
    return all(out), 'k>0', out


def g_small():
    rows = [('log(Abs(x))', 'x*log(Abs(x))-x', ['t', '-t']),
            ('log(Abs(x))**2', 'x*log(Abs(x))**2-2*x*log(Abs(x))+2*x', ['t', '-t']),
            ('exp(sqrt(x))', '2*exp(sqrt(x))*(sqrt(x)-1)', ['t']),
            ('log(x**2+a**2)', 'x*log(x**2+a**2)-2*x+2*a*atan(x/a)', ['x']),
            ('x**3*sqrt(x**2+c)', '(x**2+c)**Rational(5,2)/5-c*(x**2+c)**Rational(3,2)/3', ['t'])]
    out = []
    for f, F, br in rows:
        ex = {'a': a, 'c': s.Symbol('c', real=True)}
        out.append(check('int', P(f, extra=ex), P(F, extra=ex), [x if z == 'x' else P(z) for z in br])['status'])
    return all(o == 'symbolic' for o in out), 'listed rows', out


GENERAL = {'S-TWINS': g_twins_derivatives, 'S-SIX': g_six_integrals, 'S-LAMDA': g_lamda, 'S-SQUARE': g_square,
           'S-FOLDED': g_folded, 'S-QAWS': g_alqaws, 'S-RAFEEQ': g_rafeeq, 'S-DAWARAN': g_dawaran,
           'S-NISFAYN': g_nisfayn, 'S-SMALL': g_small, 'S-PASCAL': g_pascal, 'S-EVEN': g_even,
           'S-REDUCE': g_reduction, 'S-PROD': g_products}


def run_all():
    out = []
    for sid, fn in GENERAL.items():
        try:
            res = fn()
            ok, cond, detail = res[0], res[1], res[2:]
            out.append(dict(id=sid, status='symbolic' if ok else 'unresolved', conditions=cond, detail=str(detail)[:600]))
        except Exception as exc:
            out.append(dict(id=sid, status='unresolved', error=type(exc).__name__ + ': ' + str(exc)[:300]))
        print(sid, out[-1]['status'], flush=True)
    return out


if __name__ == '__main__':
    print(json.dumps(run_all(), ensure_ascii=False, indent=1))

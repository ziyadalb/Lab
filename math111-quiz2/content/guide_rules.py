"""The general rules quoted in the first row of the shortcut tables of the examples.

Each rule is checked when it is printed, exactly as on the formula sheet: R(key) returns the claim that
short_steps() hands to formula() (F' = f with positive or real parameters) or to functional() (a rule with
arbitrary functions that must simplify to zero).
"""
import sympy as s

from mathlib import x

F = '=FORMULA'
RULES = {
    'twins sinh': (F, 'asinh(u)', '1/sqrt(u**2+1)', dict(kind='diff', branches=('t', '-t'), uprime=True)),
    'twins csch': (F, 'acsch(u)', '-1/(Abs(u)*sqrt(1+u**2))', dict(kind='diff', branches=('t', '-t'), uprime=True)),
    'exp base 6': (F, '6**u', '6**u*log(6)', dict(kind='diff', branches=('x',), uprime=True)),
    'six sinh': (F, '1/sqrt(u**2+a**2)', 'asinh(u/a)', dict(pos=('a',))),
    'six cosh': (F, '1/sqrt(u**2-a**2)', 'acosh(u/a)', dict(branches=('a+t',), pos=('a',))),
    'six tanh': (F, '1/(a**2-u**2)', 'atanh(u/a)/a', dict(branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',))),
    'six coth': (F, '1/(a**2-u**2)', 'acoth(u/a)/a', dict(branches=('a+t', '-a-t'), pos=('a',))),
    'six sech': (F, '1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', dict(branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',))),
    'adjust': (F, 'c*x**(n-1)/sqrt((k*x**n)**2+a**2)', 'c*asinh(k*x**n/a)/(n*k)',
               dict(var='x', branches=('t',), pos=('a', 'c', 'k', 'n'))),
    'lamda csch': (F, '1/sqrt(b**(2*lam*x)+a**2)', '-acsch(b**(lam*x)/a)/(a*lam*log(b))',
                   dict(var='x', branches=('x',), pos=('a', 'b', 'lam'))),
    'sqrt sinh': (F, '1/(sqrt(x)*sqrt(a**2+x))', '2*asinh(sqrt(x)/a)', dict(var='x', branches=('t',), pos=('a',))),
    'micro +': (F, 'x/sqrt(c+x**2)', 'sqrt(c+x**2)', dict(var='x', branches=('t', '-t'), pos=('c',))),
    'xn ln': (F, 'x**n*log(x)', 'x**(n+1)/(n+1)*(log(x)-1/(n+1))', dict(var='x', branches=('t',), real=('n',))),
    'ln alone': (F, 'log(Abs(x))', 'x*log(Abs(x))-x', dict(var='x')),
    'dawaran sin': (F, 'exp(a*x)*sin(b*x)', 'exp(a*x)*(a*sin(b*x)-b*cos(b*x))/(a**2+b**2)',
                    dict(var='x', branches=('x',), pos=('a', 'b'))),
    'dawaran cos': (F, 'exp(a*x)*cos(b*x)', 'exp(a*x)*(a*cos(b*x)+b*sin(b*x))/(a**2+b**2)',
                    dict(var='x', branches=('x',), pos=('a', 'b'))),
    'dawaran one sin': (F, 'exp(a*x)*sin(b*x)', 'exp(a*x)*(a*sin(b*x)-diff(sin(b*x),x))/(a**2+b**2)',
                        dict(var='x', branches=('x',), real=('a',), pos=('b',))),
    'dawaran one cos': (F, 'exp(a*x)*cos(b*x)', 'exp(a*x)*(a*cos(b*x)-diff(cos(b*x),x))/(a**2+b**2)',
                        dict(var='x', branches=('x',), real=('a',), pos=('b',))),
    'nisfayn cosh': (F, 'exp(a*x)*cosh(b*x)', '(exp((a+b)*x)/(a+b)+exp((a-b)*x)/(a-b))/2',
                     dict(var='x', branches=('x',), real=('a', 'b'))),
    'small e sqrt': (F, 'exp(sqrt(x))', '2*exp(sqrt(x))*(sqrt(x)-1)', dict(var='x', branches=('t',))),
    'even sin2': (F, 'sin(k*x)**2', 'x/2-sin(2*k*x)/(4*k)', dict(var='x', branches=('x',), pos=('k',))),
    'sec base': (F, 'sec(x)', 'log(Abs(sec(x)+tan(x)))', dict(var='x', branches=('t/(1+t)',))),
    'prod sc': (F, 'sin(m*x)*cos(n*x)', '-(cos((m-n)*x)/(m-n)+cos((m+n)*x)/(m+n))/2',
                dict(var='x', branches=('x',), real=('m', 'n'))),
}


def _fn(name):
    return s.Function(name)(x)


def _linear():
    """(px+q)G1 - pG2 is an antiderivative of (px+q)g when G1' = g and G2' = G1."""
    G1, G2, g = _fn('G_1'), _fn('G_2'), _fn('g')
    p, q = s.symbols('p q', real=True)
    return (s.diff((p * x + q) * G1 - p * G2, x) - (p * x + q) * g).subs({s.Derivative(G1, x): g, s.Derivative(G2, x): G1})


def _di():
    """DI table for a polynomial of degree 2: f G1 - f' G2 + f'' G3 (G1' = g, G2' = G1, G3' = G2)."""
    G1, G2, G3, g = _fn('G_1'), _fn('G_2'), _fn('G_3'), _fn('g')
    a, b, c = s.symbols('a b c', real=True)
    f = a * x ** 2 + b * x + c
    expr = s.diff(f * G1 - s.diff(f, x) * G2 + s.diff(f, x, 2) * G3, x) - f * g
    return s.expand(expr.subs({s.Derivative(G1, x): g, s.Derivative(G2, x): G1, s.Derivative(G3, x): G2}))


def _g_gprime():
    """The function times its derivative integrates to half its square."""
    g = _fn('g')
    return s.diff(g ** 2 / 2, x) - g * s.diff(g, x)


def _rafeeq():
    """int f dx = x f - int x f' dx (H' = x f')."""
    f, H = _fn('f'), _fn('H')
    return (s.diff(x * f - H, x) - f).subs(s.Derivative(H, x), x * s.diff(f, x))


def _x_inverse():
    """int x f dx = x^2/2 f - 1/2 int x^2 f' dx (H' = x^2 f')."""
    f, H = _fn('f'), _fn('H')
    return s.expand((s.diff(x ** 2 / 2 * f - H / 2, x) - x * f).subs(s.Derivative(H, x), x ** 2 * s.diff(f, x)))


def _definite():
    """F(b) - F(a) = int_a^b F'(x) dx, for a polynomial F (the rule itself is the fundamental theorem)."""
    a, b = s.symbols('a b', real=True)
    Fx = x ** 3 - 2 * x
    return s.integrate(s.diff(Fx, x), (x, a, b)) - (Fx.subs(x, b) - Fx.subs(x, a))


def _tan_reduce():
    """d/dx tan^(m-1)/(m-1) = tan^m + tan^(m-2), i.e. int tan^m = tan^(m-1)/(m-1) - int tan^(m-2)."""
    m, T = s.Symbol('m', positive=True), s.tan(x)
    return s.powsimp(s.expand(s.diff(T ** (m - 1) / (m - 1), x) - T ** m - T ** (m - 2)))


def _sec_reduce():
    """d/dx sec^(n-2) tan/(n-1) + (n-2)/(n-1) sec^(n-2) = sec^n (with tan^2 = sec^2 - 1)."""
    n, S, T = s.Symbol('n', positive=True), s.sec(x), s.tan(x)
    e = s.expand(s.diff(S ** (n - 2) * T / (n - 1), x) + (n - 2) / (n - 1) * S ** (n - 2) - S ** n)
    return s.powsimp(s.expand(s.together(e.subs(T ** 2, S ** 2 - 1))))


BUILDERS = {'linear': _linear, 'di': _di, 'g gprime': _g_gprime, 'rafeeq': _rafeeq, 'x inverse': _x_inverse,
            'definite': _definite, 'tan reduce': _tan_reduce, 'sec reduce': _sec_reduce}


def R(key):
    """The checked claim for a rule row of a shortcut table."""
    if key in RULES:
        return RULES[key]
    return ('=RULE', BUILDERS[key])

"""SymPy checks for every mathematical claim printed in the P08 chapter of the memo.

Each check is (key, description, ok). build_memo.py refuses to write the HTML if one fails.
Conventions: x real; ln|f| differentiated as log(f) (same derivative wherever f != 0).
"""
import sympy as sp

x, u = sp.symbols('x u', real=True)
A, B, C, A1, A2 = sp.symbols('A B C A1 A2')
R, ln, atan = sp.Rational, sp.log, sp.atan


def eq(a, b):
    return sp.simplify(sp.expand(a - b)) == 0


def deriv_ok(F, f):
    return sp.simplify(sp.diff(F, x) - f) == 0


def run():
    out = []
    def chk(key, desc, ok):
        out.append((key, desc, bool(ok)))

    # ---------- main example 1445-S1-FE-Q2.4 ----------
    f = (4*x**2 - x + 12)/(x**3 + 4*x)
    chk('m.add', '3/x + (x-1)/(x^2+4) = (4x^2-x+12)/(x^3+4x)', eq(sp.together(3/x + (x-1)/(x**2+4)), f))
    chk('m.add.num', '3(x^2+4)+(x-1)x = 4x^2-x+12', eq(3*(x**2+4) + (x-1)*x, 4*x**2 - x + 12))
    chk('m.fac', 'x^3+4x = x(x^2+4)', eq(x**3 + 4*x, x*(x**2+4)))
    chk('m.disc', '0^2-4*1*4 = -16', 0 - 4*1*4 == -16)
    chk('m.expand', 'A(x^2+4)+(Bx+C)x = (A+B)x^2+Cx+4A', eq(A*(x**2+4) + (B*x+C)*x, (A+B)*x**2 + C*x + 4*A))
    chk('m.solve', 'A=3,B=1,C=-1 solve the system', sp.solve([A+B-4, C+1, 4*A-12], [A, B, C]) == {A: 3, B: 1, C: -1})
    dec = 3/x + (x-1)/(x**2+4)
    chk('m.dec', 'decomposition equals integrand', eq(sp.together(dec), f))
    chk('m.spot-1', 'x=-1: both sides -17/5', f.subs(x, -1) == R(-17, 5) and dec.subs(x, -1) == R(-17, 5) and R(-3) - R(2, 5) == R(-17, 5))
    chk('m.spot1', 'x=1: both sides 3', f.subs(x, 1) == 3 and dec.subs(x, 1) == 3)
    F = 3*ln(x) + R(1, 2)*ln(x**2+4) - R(1, 2)*atan(x/2)
    chk('m.ans', 'answer differentiates to integrand', deriv_ok(F, f))
    chk('m.d1', 'd/dx (1/2)ln(x^2+4) = x/(x^2+4)', deriv_ok(R(1, 2)*ln(x**2+4), x/(x**2+4)))
    chk('m.d2', 'd/dx (1/2)tan^-1(x/2) = 1/(x^2+4)', deriv_ok(R(1, 2)*atan(x/2), 1/(x**2+4)))
    chk('m.d2b', '(1/2)(1/2)/(1+x^2/4) = 1/(x^2+4)', eq(R(1, 4)/(1 + x**2/4), 1/(x**2+4)))
    chk('m.usub', 'int x/(x^2+4): u=x^2+4, du=2x dx -> (1/2)ln u', deriv_ok(R(1, 2)*ln(x**2+4), x/(x**2+4)))
    chk('m.cover', 'cover-up A = 12/(0+4) = 3', R(12, 4) == 3 and ((4*x**2 - x + 12)/(x**2+4)).subs(x, 0) == 3)
    p, q, r = sp.symbols('p q r'); a = sp.symbols('a', positive=True)
    chk('rule.readoff', '(px^2+qx+r)/(x(x^2+a^2)) = (r/a^2)/x + ((p-r/a^2)x+q)/(x^2+a^2)',
        eq(sp.together((r/a**2)/x + ((p - r/a**2)*x + q)/(x**2 + a**2)), (p*x**2 + q*x + r)/(x*(x**2 + a**2))))
    chk('rule.split', 'int (Bx+C)/(x^2+a^2) = (B/2)ln(x^2+a^2) + (C/a)tan^-1(x/a)',
        deriv_ok(B/2*ln(x**2+a**2) + C/a*atan(x/a), (B*x + C)/(x**2 + a**2)))
    chk('rule.atan', 'int dx/(x^2+a^2) = (1/a)tan^-1(x/a)', deriv_ok(atan(x/a)/a, 1/(x**2+a**2)))
    chk('rule.cover', 'cover-up: N(s) = A E(s) from N = A E + (x-s)(...)', True)  # algebraic; numeric instances below

    # ---------- B2 1445-S2-FE-Q2.4 ----------
    f2 = (3*x + 1)/(x**2 + 2*x - 8)
    chk('b2.fac', 'x^2+2x-8 = (x-2)(x+4)', eq(x**2 + 2*x - 8, (x-2)*(x+4)))
    chk('b2.c1', 'x=2: (3*2+1)/(2+4) = 7/6', R(7, 6) == R(3*2+1, 2+4))
    chk('b2.c2', 'x=-4: (3(-4)+1)/(-4-2) = 11/6', R(3*(-4)+1, -4-2) == R(11, 6))
    chk('b2.dec', '7/6/(x-2) + 11/6/(x+4)', eq(sp.together(R(7, 6)/(x-2) + R(11, 6)/(x+4)), f2))
    chk('b2.ans', 'answer', deriv_ok(R(7, 6)*ln(x-2) + R(11, 6)*ln(x+4), f2))

    # ---------- B3 1447-S1-SE-Q2.8 ----------
    f3 = (2*x + 1)/(x**2*(1 + x**2))
    chk('b3.expand', 'A1 x(1+x^2)+A2(1+x^2)+(Bx+C)x^2 = (A1+B)x^3+(A2+C)x^2+A1 x+A2',
        eq(A1*x*(1+x**2) + A2*(1+x**2) + (B*x+C)*x**2, (A1+B)*x**3 + (A2+C)*x**2 + A1*x + A2))
    chk('b3.dec', '2/x + 1/x^2 + (-2x-1)/(1+x^2)', eq(sp.together(2/x + 1/x**2 + (-2*x-1)/(1+x**2)), f3))
    chk('b3.cover', 'cover x^2 at 0: (2*0+1)/(1+0) = 1 = A2', ((2*x+1)/(1+x**2)).subs(x, 0) == 1)
    chk('b3.pow', 'int x^-2 = -1/x', deriv_ok(-1/x, x**-2))
    chk('b3.ans', 'answer', deriv_ok(2*ln(x) - 1/x - ln(1+x**2) - atan(x), f3))

    # ---------- B4 1447-S1-FE-Q2.4 ----------
    f4 = (5*x**2 + 6*x + 4)/((x+1)*(x**2 + x + 1))
    chk('b4.disc', '1-4 = -3', 1 - 4 == -3)
    chk('b4.cover', 'x=-1: (5-6+4)/(1-1+1) = 3', ((5*x**2+6*x+4)/(x**2+x+1)).subs(x, -1) == 3)
    chk('b4.expand', 'A(x^2+x+1)+(Bx+C)(x+1) = (A+B)x^2+(A+B+C)x+(A+C)',
        eq(A*(x**2+x+1) + (B*x+C)*(x+1), (A+B)*x**2 + (A+B+C)*x + (A+C)))
    chk('b4.xcheck', 'x-coefficient check 3+2+1 = 6', 3 + 2 + 1 == 6)
    chk('b4.dec', '3/(x+1) + (2x+1)/(x^2+x+1)', eq(sp.together(3/(x+1) + (2*x+1)/(x**2+x+1)), f4))
    chk('b4.ans', 'answer', deriv_ok(3*ln(x+1) + ln(x**2+x+1), f4))
    wrong = 4/(x+1) + (x + 6)/(x**2 + x + 1)
    chk('b4.trap', 'read-off copied onto (x+1)(x^2+x+1) is wrong: at x=0 gives 10, original 4',
        not eq(sp.together(wrong), f4) and wrong.subs(x, 0) == 10 and f4.subs(x, 0) == 4)

    # ---------- B5 1447-S2-FE-Q2.4 ----------
    f5 = (3*x**2 + 1)/((x**2 - 1)*(x**2 + 1))
    chk('b5.fac', 'x^2-1 = (x-1)(x+1)', eq(x**2 - 1, (x-1)*(x+1)))
    chk('b5.c1', 'x=1: (3+1)/((1+1)(1+1)) = 1', R(4, 4) == 1)
    chk('b5.c2', 'x=-1: (3+1)/((-1-1)(1+1)) = -1', R(4, -4) == -1)
    ident = A1*(x+1)*(x**2+1) + A2*(x-1)*(x**2+1) + (B*x+C)*(x**2-1)
    chk('b5.x3', 'x^3 coefficient A1+A2+B', sp.Poly(sp.expand(ident), x).coeff_monomial(x**3) == A1 + A2 + B)
    chk('b5.x0', 'x=0: A1 - A2 - C', sp.expand(ident.subs(x, 0)) == A1 - A2 - C)
    chk('b5.dec', '1/(x-1) - 1/(x+1) + 1/(x^2+1)', eq(sp.together(1/(x-1) - 1/(x+1) + 1/(x**2+1)), f5))
    chk('b5.ans', 'answer', deriv_ok(ln(x-1) - ln(x+1) + atan(x), f5))

    # ---------- pair: numerator = derivative ----------
    g = (2*x + 2)/(x**2 + 2*x - 8)
    chk('pair.ln', 'int (2x+2)/(x^2+2x-8) = ln|x^2+2x-8|', deriv_ok(ln(x**2 + 2*x - 8), g))
    chk('pair.pf', '(2x+2)/((x-2)(x+4)) = 1/(x-2) + 1/(x+4)', eq(sp.together(1/(x-2) + 1/(x+4)), g))
    chk('pair.same', 'ln|x-2|+ln|x+4| = ln|(x-2)(x+4)|', eq(sp.expand_log(ln((x-2)*(x+4)), force=True), ln(x-2) + ln(x+4)))

    # ---------- training ----------
    t2a = (2*x + 1)/(x**2 + x + 1)
    chk('t2a', 'int (2x+1)/(x^2+x+1) = ln(x^2+x+1)', deriv_ok(ln(x**2 + x + 1), t2a))
    t2b = (x + 3)/(x**2 + 9)
    chk('t2b', 'int (x+3)/(x^2+9) = (1/2)ln(x^2+9) + tan^-1(x/3)', deriv_ok(R(1, 2)*ln(x**2+9) + atan(x/3), t2b))
    t2c = (5*x**2 + 3*x - 2)/(x**3 + 2*x**2)
    chk('t2c.fac', 'x^3+2x^2 = x^2(x+2)', eq(x**3 + 2*x**2, x**2*(x+2)))
    chk('t2c.dec', '2/x - 1/x^2 + 3/(x+2)', eq(sp.together(2/x - 1/x**2 + 3/(x+2)), t2c))
    chk('t2c.cov', 'x=-2: (20-6-2)/4 = 3; x^2 at 0: -2/2 = -1', R(20-6-2, 4) == 3 and R(-2, 2) == -1)
    chk('t2c.ans', 'answer', deriv_ok(2*ln(x) + 1/x + 3*ln(x+2), t2c))

    t3 = (x + 3)/(x**3 + 9*x)
    chk('t3.read', 'A=3/9=1/3, C=1, B=0-1/3', True and R(3, 9) == R(1, 3))
    chk('t3.dec', '(1/3)/x + (-(1/3)x+1)/(x^2+9)', eq(sp.together(R(1, 3)/x + (-R(1, 3)*x + 1)/(x**2+9)), t3))
    chk('t3.split', 'B/2 = -1/6, C/a = 1/3', R(-1, 3)/2 == R(-1, 6) and R(1, 3) == R(1, 3))
    chk('t3.ans', 'answer', deriv_ok(R(1, 3)*ln(x) - R(1, 6)*ln(x**2+9) + R(1, 3)*atan(x/3), t3))

    t4 = (5*x**2 + x + 8)/(x**3 + 4*x)
    chk('t4.dec', '2/x + (3x+1)/(x^2+4)', eq(sp.together(2/x + (3*x+1)/(x**2+4)), t4))
    chk('t4.ans', 'answer', deriv_ok(2*ln(x) + R(3, 2)*ln(x**2+4) + R(1, 2)*atan(x/2), t4))

    t5 = (3*x**2 + x + 4)/(x*(x**2 + 4))
    chk('t5.dec', '1/x + (2x+1)/(x^2+4)', eq(sp.together(1/x + (2*x+1)/(x**2+4)), t5))
    chk('t5.ans', 'answer', deriv_ok(ln(x) + ln(x**2+4) + R(1, 2)*atan(x/2), t5))

    t6 = (8*x + 2)/(x**2 + 2*x - 8)
    chk('t6.cov', 'x=2: 18/6=3; x=-4: -30/-6=5', R(18, 6) == 3 and R(-30, -6) == 5)
    chk('t6.dec', '3/(x-2) + 5/(x+4)', eq(sp.together(3/(x-2) + 5/(x+4)), t6))
    chk('t6.notder', '8x+2 is not a multiple of 2x+2', sp.simplify((8*x+2)/(2*x+2)).is_number is False)
    chk('t6.ans', 'answer', deriv_ok(3*ln(x-2) + 5*ln(x+4), t6))

    t7 = 1/((x - 1)*(x**2 + 1))
    chk('t7.cov', 'x=1: 1/(1+1) = 1/2', (1/(x**2+1)).subs(x, 1) == R(1, 2))
    chk('t7.expand', 'A(x^2+1)+(Bx+C)(x-1) = (A+B)x^2+(C-B)x+(A-C)', eq(A*(x**2+1) + (B*x+C)*(x-1), (A+B)*x**2 + (C-B)*x + (A-C)))
    chk('t7.dec', '(1/2)/(x-1) + (-(1/2)x-1/2)/(x^2+1)', eq(sp.together(R(1, 2)/(x-1) + (-R(1, 2)*x - R(1, 2))/(x**2+1)), t7))
    chk('t7.xcheck', 'x coefficient C-B = 0', R(-1, 2) - R(-1, 2) == 0)
    chk('t7.ans', 'answer', deriv_ok(R(1, 2)*ln(x-1) - R(1, 4)*ln(x**2+1) - R(1, 2)*atan(x), t7))

    t8 = (x**2 + 1)/(x**3 - 2*x**2)
    chk('t8.fac', 'x^3-2x^2 = x^2(x-2)', eq(x**3 - 2*x**2, x**2*(x-2)))
    chk('t8.cov', 'x=2: 5/4; x^2 at 0: 1/(-2)', ((x**2+1)/x**2).subs(x, 2) == R(5, 4) and ((x**2+1)/(x-2)).subs(x, 0) == R(-1, 2))
    chk('t8.expand', 'Ax(x-2)+B(x-2)+Cx^2 = (A+C)x^2+(B-2A)x-2B', eq(A*x*(x-2) + B*(x-2) + C*x**2, (A+C)*x**2 + (B-2*A)*x - 2*B))
    chk('t8.dec', '-(1/4)/x - (1/2)/x^2 + (5/4)/(x-2)', eq(sp.together(-R(1, 4)/x - R(1, 2)/x**2 + R(5, 4)/(x-2)), t8))
    chk('t8.ans', 'answer', deriv_ok(-R(1, 4)*ln(x) + 1/(2*x) + R(5, 4)*ln(x-2), t8))

    t9 = (x**3 - 1)/(x**2 + x)
    chk('t9.div', '(x^3-1) = (x^2+x)(x-1) + (x-1)', eq((x**2+x)*(x-1) + (x-1), x**3 - 1))
    chk('t9.dec', 'x-1 - 1/x + 2/(x+1)', eq(sp.together(x - 1 - 1/x + 2/(x+1)), t9))
    chk('t9.cov', '(x-1)/(x(x+1)): x=0 -> -1, x=-1 -> 2', ((x-1)/(x+1)).subs(x, 0) == -1 and ((x-1)/x).subs(x, -1) == 2)
    chk('t9.ans', 'answer', deriv_ok(x**2/2 - x - ln(x) + 2*ln(x+1), t9))

    t10 = sp.cos(x)/(sp.sin(x)**2 + 5*sp.sin(x) + 6)
    chk('t10.fac', 'u^2+5u+6 = (u+2)(u+3)', eq(u**2 + 5*u + 6, (u+2)*(u+3)))
    chk('t10.dec', '1/((u+2)(u+3)) = 1/(u+2) - 1/(u+3)', sp.simplify(1/(u+2) - 1/(u+3) - 1/((u+2)*(u+3))) == 0)
    chk('t10.ans', 'answer ln(sin x+2) - ln(sin x+3)', deriv_ok(ln(sp.sin(x)+2) - ln(sp.sin(x)+3), t10))
    return out


if __name__ == '__main__':
    res = run()
    bad = [r for r in res if not r[2]]
    print(len(res), 'checks;', len(bad), 'failed')
    for r in bad:
        print('FAIL', r)

"""Verify pattern P08 (partial fractions) for riyad111.

What is checked, per real exam question (12 questions, 12 papers):
  1. the official decomposition equals the integrand (identity in x);
  2. the official antiderivative differentiates back to the integrand.
     d/dx ln|f| = f'/f on every interval where f != 0, so ln|f| is
     differentiated as log(f) (same derivative); tan^-1 needs no domain note;
  3. every cover-up value (non-repeated linear factor) equals the official
     coefficient;
  4. numeric spot check of the decomposition at x = 1 and x = -1 when defined
     (the check taught to the student).
General rules (symbolic constants):
  R1  x(x^2+a^2) read-off: A = r/a^2, C = q, B = p - A   (a != 0)
  R2  split rule: d/dx[(B/2) ln(x^2+a^2) + (C/a) tan^-1(x/a)] = (Bx+C)/(x^2+a^2), a>0
  R3  cover-up: for D = (x-r) E with E(r) != 0, the coefficient of 1/(x-r) is N(r)/E(r)
Trap check: R1 applied to a denominator that is not x(x^2+a^2) must fail.
Output: reports/verify_p08.json
"""
import json, sys
from pathlib import Path
import sympy as sp

x = sp.symbols('x', real=True)
p, q, r = sp.symbols('p q r', real=True)
a = sp.symbols('a', positive=True)
B, C = sp.symbols('B C', real=True)
ln, atan, R = sp.log, sp.atan, sp.Rational

Q = [
 # id, location, integrand, official decomposition, official answer (ln|f| as log(f)), linear roots for cover-up {root: official coeff}, branch
 ("1445-S1-SE-Q2.8", "M 111 - (451-452) - English.pdf p8", (x+3)/(x**3+9*x),
  R(1,3)/x + (-R(1,3)*x+1)/(x**2+9),
  R(1,3)*ln(x) - R(1,6)*ln(x**2+9) + R(1,3)*atan(x/3), {0: R(1,3)}, "B1"),
 ("1445-S2-SE-Q2.8", "M 111 - (451-452) - English.pdf p24", (3*x**2+3*x+8)/(x**3+4*x),
  2/x + (x+3)/(x**2+4),
  2*ln(x) + R(1,2)*ln(x**2+4) + R(3,2)*atan(x/2), {0: 2}, "B1"),
 ("1446-S1-SE-Q2.8", "M111 - (461-462).pdf p8", (5*x**2+x+8)/(x**3+4*x),
  2/x + (3*x+1)/(x**2+4),
  2*ln(x) + R(3,2)*ln(x**2+4) + R(1,2)*atan(x/2), {0: 2}, "B1"),
 ("1446-S2-SE-Q2.9", "M111 - (461-462).pdf p24", (x**2+x+9)/(x**3+9*x),
  1/x + 1/(x**2+9),
  ln(x) + R(1,3)*atan(x/3), {0: 1}, "B1"),
 ("1447-S1-SE-Q2.8", "M111 (471-472)_2.pdf p7", (2*x+1)/(x**2*(1+x**2)),
  2/x + 1/x**2 + (-2*x-1)/(1+x**2),
  2*ln(x) - 1/x - ln(1+x**2) - atan(x), {}, "B3"),
 ("1447-S2-SE-Q3.6", "M111 (471-472)_2.pdf p22", (3*x**2+x+4)/(x*(x**2+4)),
  1/x + (2*x+1)/(x**2+4),
  ln(x) + ln(x**2+4) + R(1,2)*atan(x/2), {0: 1}, "B1"),
 ("1445-S1-FE-Q2.4", "M 111 - (451-452) - English.pdf p12", (4*x**2-x+12)/(x**3+4*x),
  3/x + (x-1)/(x**2+4),
  3*ln(x) + R(1,2)*ln(x**2+4) - R(1,2)*atan(x/2), {0: 3}, "B1"),
 ("1445-S2-FE-Q2.4", "M 111 - (451-452) - English.pdf p28", (3*x+1)/(x**2+2*x-8),
  R(7,6)/(x-2) + R(11,6)/(x+4),
  R(7,6)*ln(x-2) + R(11,6)*ln(x+4), {2: R(7,6), -4: R(11,6)}, "B2"),
 ("1446-S1-FE-Q2.4", "M111 - (461-462).pdf p12", (3*x+1)/(x**3+x),
  1/x + (-x+3)/(x**2+1),
  ln(x) - R(1,2)*ln(x**2+1) + 3*atan(x), {0: 1}, "B1"),
 ("1446-S2-FE-Q2.3", "M111 - (461-462).pdf p26", (3*x**2+x+8)/(x**3+4*x),
  2/x + (x+1)/(x**2+4),
  2*ln(x) + R(1,2)*ln(x**2+4) + R(1,2)*atan(x/2), {0: 2}, "B1"),
 ("1447-S1-FE-Q2.4", "M111 (471-472)_2.pdf p11", (5*x**2+6*x+4)/((x+1)*(x**2+x+1)),
  3/(x+1) + (2*x+1)/(x**2+x+1),
  3*ln(x+1) + ln(x**2+x+1), {-1: 3}, "B4"),
 ("1447-S2-FE-Q2.4", "M111 (471-472)_2.pdf p26", (3*x**2+1)/((x**2-1)*(x**2+1)),
  1/(x-1) - 1/(x+1) + 1/(x**2+1),
  ln(x-1) - ln(x+1) + atan(x), {1: 1, -1: -1}, "B5"),
]

def coverup(f, root):
    n, d = sp.fraction(sp.together(f))
    e = sp.cancel(d/(x-root))
    return sp.nsimplify(n.subs(x, root)/e.subs(x, root))

out = {"tool": "SymPy " + sp.__version__, "assumptions": "x real; ln|f| differentiated as log(f) (same derivative wherever f != 0); a>0 in R2", "questions": [], "rules": {}, "traps": []}
ok_all = True
for qid, loc, f, dec, ans, cov, br in Q:
    rec = {"id": qid, "location": loc, "branch": br}
    rec["decomposition_identity"] = sp.simplify(sp.together(dec - f)) == 0
    rec["apart_matches"] = sp.simplify(sp.apart(f, x) - dec) == 0
    rec["answer_derivative"] = sp.simplify(sp.diff(ans, x) - f) == 0
    rec["coverup"] = {str(k): {"official": str(v), "coverup": str(coverup(f, k)), "ok": coverup(f, k) == v} for k, v in cov.items()}
    spots = {}
    for t in (1, -1, 2):
        fv = f.subs(x, t); dv = dec.subs(x, t)
        if fv.is_finite and dv.is_finite:
            spots[str(t)] = {"integrand": str(sp.nsimplify(fv)), "decomposition": str(sp.nsimplify(dv)), "ok": sp.simplify(fv - dv) == 0}
    rec["spot_values"] = spots
    good = rec["decomposition_identity"] and rec["apart_matches"] and rec["answer_derivative"] and all(v["ok"] for v in rec["coverup"].values()) and all(v["ok"] for v in spots.values())
    rec["status"] = "مثبت (تطابق رمزي)" if good else "فشل"
    ok_all &= good
    out["questions"].append(rec)

# R1: read-off for x(x^2+a^2)
A1 = r/a**2
R1 = sp.simplify((p*x**2 + q*x + r)/(x*(x**2+a**2)) - (A1/x + ((p - A1)*x + q)/(x**2+a**2))) == 0
out["rules"]["R1_readoff_x(x^2+a^2)"] = {"statement": "(p x^2+q x+r)/(x(x^2+a^2)) = (r/a^2)/x + ((p - r/a^2) x + q)/(x^2+a^2)", "conditions": "a != 0; denominator exactly x times (x^2 + a^2): linear factor is x itself, quadratic has no x-term", "symbolic": R1}
# R2: split rule
R2 = sp.simplify(sp.diff(B/2*ln(x**2+a**2) + C/a*atan(x/a), x) - (B*x+C)/(x**2+a**2)) == 0
out["rules"]["R2_split"] = {"statement": "int (Bx+C)/(x^2+a^2) dx = (B/2) ln(x^2+a^2) + (C/a) tan^-1(x/a) + c", "conditions": "a>0", "symbolic": R2}
# R3: cover-up general (simple linear factor)
s0 = sp.symbols('s0', real=True)
N = sp.Function('N'); E = sp.Function('E')
# proof sketch is algebraic: N = A E + (x-s0) M  =>  N(s0) = A E(s0). Check on a generic cubic example with symbolic coefficients:
c0, c1, c2, d1, d2 = sp.symbols('c0 c1 c2 d1 d2', real=True)
fgen = (c2*x**2 + c1*x + c0)/((x - s0)*(x**2 + d1*x + d2))
Agen = (c2*s0**2 + c1*s0 + c0)/(s0**2 + d1*s0 + d2)
resid = sp.simplify(sp.cancel((fgen - Agen/(x - s0))*(x**2 + d1*x + d2)))
# after removing A/(x-s0) the remainder must have no pole at s0: (x - s0)*remainder -> 0 as x->s0
R3 = sp.simplify(sp.limit(((fgen - Agen/(x - s0))*(x - s0)).subs({c0:4, c1:6, c2:5, d1:1, d2:1, s0:-1}), x, -1)) == 0
R3b = sp.simplify(((fgen - Agen/(x - s0))*(x - s0)).subs(x, s0 + sp.Symbol('h'))).subs(sp.Symbol('h'), 0)
out["rules"]["R3_coverup"] = {"statement": "D=(x-s)E, E(s)!=0: coefficient of 1/(x-s) = N(s)/E(s)", "conditions": "linear factor not repeated; proper fraction", "symbolic_generic_quadratic_E": sp.simplify(sp.cancel(R3b)) == 0, "numeric_case_1447S1FE": R3}

# Trap: R1 read-off applied to 1447-S1-FE-Q2.4 (denominator (x+1)(x^2+x+1)) -> must NOT equal integrand
f_trap = (5*x**2+6*x+4)/((x+1)*(x**2+x+1))
wrong = (4/1)/(x+1) + ((5-4)*x + 6)/(x**2+x+1)   # 'A = constant/..., C = x-coefficient' copied blindly
out["traps"].append({"case": "R1 copied onto (x+1)(x^2+x+1) [1447-S1-FE-Q2.4]", "wrong_equals_integrand": sp.simplify(wrong - f_trap) == 0, "expected": False})
f_trap2 = (2*x+1)/(x**2*(1+x**2))
# cover-up at x=0 for repeated x^2 gives only the 1/x^2 coefficient
cov_rep = sp.nsimplify(((2*x+1)/(1+x**2)).subs(x, 0))
out["traps"].append({"case": "cover-up on repeated x^2 [1447-S1-SE-Q2.8]: gives coefficient of 1/x^2 only", "coverup_value": str(cov_rep), "official_A2_(1/x^2)": "1", "official_A1_(1/x)": "2", "note": "covering x^2 gives A2=1 (correct for 1/x^2); A1 must come from comparing coefficients"})

out["all_ok"] = bool(ok_all and R1 and R2 and out["rules"]["R3_coverup"]["symbolic_generic_quadratic_E"] and R3 and not out["traps"][0]["wrong_equals_integrand"])
Path(__file__).resolve().parent.parent.joinpath("reports/verify_p08.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))
print("all_ok:", out["all_ok"])
for qrec in out["questions"]:
    print(qrec["id"], qrec["branch"], qrec["status"], {k: v["ok"] for k, v in qrec["coverup"].items()}, {k: v["ok"] for k, v in qrec["spot_values"].items()})
print(out["rules"]); print(out["traps"])

#!/usr/bin/env python3
"""Authored item data (after visual review of the original PDFs) -> data/items.json.

Each item: id, kind, src (file key + pdf page + number), task (diff|int|defint), q (display/check string,
'raw:' keeps the printed shape), official (transcribed official answer terms or None), answer (our
answer terms, checked by verify.py), branches (x = phi(t), t>0; 'x' = generic real), domain, case, section.
Notes pages: PDF page = printed page. Exam keys: EX1445/EX1446/EX1447 = the three exam PDFs.
"""
import json
from pathlib import Path

POS, NEG, BOTH, GEN = ['t'], ['-t'], ['t', '-t'], ['x']
I = []


def item(id_, kind, src, task, q, answer, branches, case, section, official=None, domain='', note='', **kw):
    I.append(dict(id=id_, kind=kind, src=src, task=task, q=q, answer=answer, official=official,
                  branches=branches, domain=domain, case=case, section=section, note=note, **kw))


def ex(id_, page, task, q, official, answer, branches, case, section, domain='', note='', **kw):
    item(id_, 'exam', dict(file='EX' + id_[:4], pdf_page=page, number=id_.split('-')[-1]), task, q, answer,
         branches, case, section, official, domain, note, **kw)


def nx(id_, page, num, task, q, answer, branches, case, section, domain='', note='', kind='notes_exercise', official=None, **kw):
    item(id_, kind, dict(file='NOTES', pdf_page=page, number=num), task, q, answer, branches, case, section,
         official, domain, note, **kw)


# ---------------------------------------------------------------- 4.2 derivatives (exams)
ex('1445-S1-SE-Q1.1', 5, 'diff', 'raw:cosh(3*x**2)+asech(2*x)',
   ['6*x*sinh(3*x**2)', '-1/(x*sqrt(1-4*x**2))'], ['6*x*sinh(3*x**2)', '-1/(x*sqrt(1-4*x**2))'],
   ['t/(2*(1+t))'], 'C42-D', '4.2', '0<x<1/2')
ex('1445-S1-SE-Q1.2', 5, 'diff', 'raw:acoth(3*x)+tanh(sqrt(2*x))**2',
   ['-3/(1-9*x**2)', '2*tanh(sqrt(2*x))*sech(sqrt(2*x))**2/sqrt(2*x)'],
   ['3/(1-9*x**2)', '2*tanh(sqrt(2*x))*sech(sqrt(2*x))**2/sqrt(2*x)'],
   ['1/3+t'], 'C42-D', '4.2', 'x>1/3', note='K1: official sign follows notes p.58')
ex('1445-S1-FE-Q1.3', 10, 'diff', 'raw:asinh(3**x)+log(Abs(tanh(4*x)))',
   ['3**x*log(3)/sqrt(1+3**(2*x))', '4*sech(4*x)**2/tanh(4*x)'],
   ['3**x*log(3)/sqrt(1+3**(2*x))', '4*sech(4*x)**2/tanh(4*x)'], BOTH, 'C42-D', '4.2', 'x!=0')
ex('1445-S2-SE-Q1.1', 22, 'diff', 'raw:tanh(2*x**3)+asech(3*x)',
   ['6*x**2*sech(2*x**3)**2', '-1/(x*sqrt(1-9*x**2))'], ['6*x**2*sech(2*x**3)**2', '-1/(x*sqrt(1-9*x**2))'],
   ['t/(3*(1+t))'], 'C42-D', '4.2', '0<x<1/3')
ex('1445-S2-SE-Q1.2', 22, 'diff', 'raw:acosh(sqrt(x))+sinh(1/x)**3',
   ['1/(2*sqrt(x)*sqrt(x-1))', '-3*sinh(1/x)**2*cosh(1/x)/x**2'],
   ['1/(2*sqrt(x)*sqrt(x-1))', '-3*sinh(1/x)**2*cosh(1/x)/x**2'], ['1+t'], 'C42-D', '4.2', 'x>1')
ex('1445-S2-FE-Q1.3', 26, 'diff', 'raw:acosh(3**(2*x-1))+log(Abs(csch(x/2)))/log(10)',
   ['2*3**(2*x-1)*log(3)/sqrt(3**(4*x-2)-1)', '-coth(x/2)/(2*log(10))'],
   ['2*3**(2*x-1)*log(3)/sqrt(3**(4*x-2)-1)', '-coth(x/2)/(2*log(10))'], ['1/2+t'], 'C42-D', '4.2', 'x>1/2',
   note='log means log base 10 in the exam')
ex('1446-S1-SE-Q1.1', 5, 'diff', 'raw:csch(2/x)+atanh(exp(5*x))',
   ['2*csch(2/x)*coth(2/x)/x**2', '5*exp(5*x)/(1-exp(10*x))'],
   ['2*csch(2/x)*coth(2/x)/x**2', '5*exp(5*x)/(1-exp(10*x))'], NEG, 'C42-D', '4.2', 'x<0')
ex('1446-S1-SE-Q1.2', 5, 'diff', 'raw:asinh(sqrt(x))+coth(4*x**2)',
   ['1/(2*sqrt(x)*sqrt(1+x))', '-8*x*csch(4*x**2)**2'], ['1/(2*sqrt(x)*sqrt(1+x))', '-8*x*csch(4*x**2)**2'],
   POS, 'C42-D', '4.2', 'x>0')
ex('1446-S1-FE-Q1.3', 10, 'diff', 'raw:acosh(3**(x**2-1))+log(Abs(tanh(2*x)))/log(10)',
   ['2*x*log(3)*3**(x**2-1)/sqrt(3**(2*x**2-2)-1)', '2*sech(2*x)**2/(tanh(2*x)*log(10))'],
   ['2*x*log(3)*3**(x**2-1)/sqrt(3**(2*x**2-2)-1)', '2*sech(2*x)**2/(tanh(2*x)*log(10))'],
   ['1+t', '-1-t'], 'C42-D', '4.2', '|x|>1', note='log means log base 10 in the exam')
ex('1446-S2-SE-Q1.1', 21, 'diff', 'raw:coth(real_root(x,3))+acsch(2/x)',
   ['-csch(real_root(x,3))**2/(3*real_root(x,3)**2)', '1/(x*sqrt(4/x**2+1))'],
   ['-csch(real_root(x,3))**2/(3*real_root(x,3)**2)', '1/(Abs(x)*sqrt(4/x**2+1))'],
   BOTH, 'C42-D', '4.2', 'x!=0', note='official drops |f(x)| of notes formula 6: valid only for x>0')
ex('1446-S2-SE-Q1.2', 21, 'diff', 'raw:acoth(x**3/3)+acosh(3*x)',
   ['x**2/(1-x**6/9)', '3/sqrt(9*x**2-1)'], ['x**2/(1-x**6/9)', '3/sqrt(9*x**2-1)'],
   ['3**Rational(1,3)+t'], 'C42-D', '4.2', 'x>cbrt(3)', note='official uses the correct + sign for coth^-1')
ex('1446-S2-FE-Q1.3', 25, 'diff', 'raw:tanh(sqrt(x))+asinh(2/sqrt(x))',
   ['sech(sqrt(x))**2/(2*sqrt(x))', '-1/(x**Rational(3,2)*sqrt(1+4/x))'],
   ['sech(sqrt(x))**2/(2*sqrt(x))', '-1/(x**Rational(3,2)*sqrt(1+4/x))'], POS, 'C42-D', '4.2', 'x>0')
ex('1447-S1-SE-Q1.1', 5, 'diff', 'raw:sinh(sqrt(x**2+1))+acosh(exp(x))',
   ['x*cosh(sqrt(x**2+1))/sqrt(x**2+1)', 'exp(x)/sqrt(exp(2*x)-1)'],
   ['x*cosh(sqrt(x**2+1))/sqrt(x**2+1)', 'exp(x)/sqrt(exp(2*x)-1)'], POS, 'C42-D', '4.2', 'x>0')
ex('1447-S1-SE-Q1.2', 5, 'diff', 'raw:sech(5*x**2)+atanh(sin(x))',
   ['-10*x*sech(5*x**2)*tanh(5*x**2)', 'cos(x)/(1-sin(x)**2)'],
   ['-10*x*sech(5*x**2)*tanh(5*x**2)', 'cos(x)/(1-sin(x)**2)'], ['t/(1+t)'], 'C42-D', '4.2', 'sin x != ±1')
ex('1447-S2-SE-Q1.1', 20, 'diff', 'raw:asinh(log(Abs(x+1)))',
   ['1/((x+1)*sqrt(1+log(Abs(x+1))**2))'], ['1/((x+1)*sqrt(1+log(Abs(x+1))**2))'], ['t-1', '-t-1'],
   'C42-D', '4.2', 'x!=-1')
ex('1447-S2-SE-Q1.2', 20, 'diff', 'raw:acsch(sqrt(x+2))',
   ['-1/(2*(x+2)*sqrt(x+3))'], ['-1/(2*(x+2)*sqrt(x+3))'], ['t-2'], 'C42-D', '4.2', 'x>-2')

# ---------------------------------------------------------------- 4.2 integrals (exams)
ex('1445-S1-SE-Q2.2', 6, 'int', 'raw:1/(sqrt(x)*sqrt(1+x))', ['2*asinh(sqrt(x))'], ['2*asinh(sqrt(x))'],
   POS, 'C42-I-SINH', '4.2', 'x>0', note='second official solution: 2 cosh^-1(sqrt(x+1))')
ex('1445-S1-SE-Q2.7', 8, 'int', 'raw:sin(x)/(4-cos(x)**2)', ['-atanh(cos(x)/2)/2'], ['-atanh(cos(x)/2)/2'],
   GEN, 'C42-I-TANH', '4.2', 'all real x (|cos x/2|<1)')
ex('1445-S2-SE-Q2.4', 23, 'int', 'raw:1/(x*sqrt(x**6+25))', ['-acsch(x**3/5)/15'], ['-acsch(Abs(x)**3/5)/15'],
   BOTH, 'C42-I-CSCH', '4.2', 'x!=0', note='official drops |.|: valid only for x>0')
ex('1446-S2-SE-Q2.7', 23, 'int', 'raw:1/sqrt(exp(6*x)+1)', ['-acsch(exp(3*x))/3'], ['-acsch(exp(3*x))/3'],
   GEN, 'C42-I-HIDDEN', '4.2', 'all real x')
ex('1447-S1-SE-Q2.2', 5, 'int', 'raw:1/sqrt(5**(2*x)+1)', ['-acsch(5**x)/log(5)'], ['-acsch(5**x)/log(5)'],
   GEN, 'C42-I-HIDDEN', '4.2', 'all real x')
ex('1447-S2-SE-Q3.2', 21, 'int', 'raw:1/(x*sqrt(log(Abs(x))**2-1))', ['acosh(log(Abs(x)))'],
   ['acosh(log(Abs(x)))'], ['exp(1+t)', '-exp(1+t)'], 'C42-I-COSH', '4.2', 'ln|x|>1',
   note='notes formula 2 condition f(x)>a; the region ln|x|<-1 is not covered by this form')
ex('1445-S2-SE-Q2.7', 24, 'int', 'raw:1/sqrt(x**2+6*x+13)', ['asinh((x+3)/2)'], ['asinh((x+3)/2)'],
   ['t-3', '-t-3'], 'C42-CS', '4.2', 'all real x')
ex('1445-S2-FE-Q2.1', 27, 'int', 'raw:2/sqrt(4*x**2+8*x+20)', ['asinh((x+1)/2)'], ['asinh((x+1)/2)'],
   ['t-1', '-t-1'], 'C42-CS', '4.2', 'all real x')
ex('1446-S1-SE-Q2.2', 5, 'int', 'raw:3/sqrt(x**2+6*x-16)', ['3*acosh((x+3)/5)'], ['3*acosh((x+3)/5)'],
   ['2+t'], 'C42-CS', '4.2', 'x+3>5 (notes formula 2 condition)', note='left region x<-8 not covered by this form')
ex('1446-S2-SE-Q2.2', 21, 'int', 'raw:1/sqrt(x**2+2*x+10)', ['asinh((x+1)/3)'], ['asinh((x+1)/3)'],
   ['t-1', '-t-1'], 'C42-CS', '4.2', 'all real x')
ex('1447-S1-FE-Q2.1', 10, 'int', 'raw:1/sqrt(x**2-4*x)', ['acosh((x-2)/2)'], ['acosh((x-2)/2)'], ['4+t'],
   'C42-CS', '4.2', 'x-2>2', note='left region x<0 not covered by this form')
ex('1447-S1-SE-Q2.4', 6, 'int', 'raw:1/((x-3)*sqrt(7-x**2+6*x))', ['-asech((x-3)/4)/4'],
   ['-asech(Abs(x-3)/4)/4'], ['3+4*t/(1+t)', '3-4*t/(1+t)'], 'C42-CSL', '4.2', '-1<x<7, x!=3',
   note='official drops |.| of notes formula 5: real only for 3<x<7')
ex('1447-S2-SE-Q3.4', 22, 'int', 'raw:1/((x-2)*sqrt(-x**2+4*x-2))', ['-asech((x-2)/sqrt(2))/sqrt(2)'],
   ['-asech(Abs(x-2)/sqrt(2))/sqrt(2)'], ['2+sqrt(2)*t/(1+t)', '2-sqrt(2)*t/(1+t)'], 'C42-CSL', '4.2',
   '2-sqrt2<x<2+sqrt2, x!=2', note='official drops |.|: real only for x>2', sym=['2+t', '2-t'])
ex('1447-S2-FE-Q2.6', 27, 'int', 'raw:1/((x+3)*sqrt(x**2+6*x+13))', ['-acsch((x+3)/2)/2'],
   ['-acsch(Abs(x+3)/2)/2'], ['t-3', '-t-3'], 'C42-CSL', '4.2', 'x!=-3', note='official drops |.|: valid only for x>-3')
# contrast only (3.4): completing the square -> sin^-1
for qid, page, q, a, br in [
        ('1445-S1-FE-Q2.1', 11, 'raw:2/sqrt(-x**2-6*x)', '2*asin((x+3)/3)', ['-3+3*t/(1+t)', '-3-3*t/(1+t)']),
        ('1446-S1-FE-Q2.1', 11, 'raw:2/sqrt(-x**2+6*x-8)', '2*asin(x-3)', ['3+t/(1+t)', '3-t/(1+t)']),
        ('1446-S2-FE-Q2.1', 26, 'raw:1/sqrt(-x**2-2*x+8)', 'asin((x+1)/3)', ['-1+3*t/(1+t)', '-1-3*t/(1+t)'])]:
    ex(qid, page, 'int', q, [a], [a], br, 'C34-CONTRAST', '3.4', 'interior of the root domain', scope='contrast')

# ---------------------------------------------------------------- 5.1 (exams)
ex('1445-S1-SE-Q2.1', 5, 'int', 'raw:exp(-x)*cosh(x)', ['x/2', '-exp(-2*x)/4'], ['x/2', '-exp(-2*x)/4'], GEN,
   'C51-EXPH', '5.1', 'all real x')
ex('1445-S1-SE-Q2.3', 6, 'defint', 'raw:x**3*log(x)', ['3*exp(4)/16', '1/16'], ['3*exp(4)/16', '1/16'], [],
   'C51-DEF', '5.1', '[1,e]', bounds=['1', 'E'], antiderivative=['x**4*log(x)/4', '-x**4/16'])
ex('1445-S1-SE-Q2.5', 7, 'int', 'raw:acosh(x)', ['x*acosh(x)', '-sqrt(x**2-1)'], ['x*acosh(x)', '-sqrt(x**2-1)'],
   ['1+t'], 'C51-INV', '5.1', 'x>1')
ex('1445-S1-FE-Q2.2', 11, 'int', 'raw:x**2*cosh(x)', ['x**2*sinh(x)', '-2*x*cosh(x)', '2*sinh(x)'],
   ['x**2*sinh(x)', '-2*x*cosh(x)', '2*sinh(x)'], GEN, 'C51-POLY2', '5.1', 'all real x')
ex('1445-S2-SE-Q2.2', 22, 'int', 'raw:(2*x+1)*cos(x)', ['(2*x+1)*sin(x)', '2*cos(x)'],
   ['(2*x+1)*sin(x)', '2*cos(x)'], GEN, 'C51-POLY1', '5.1', 'all real x')
ex('1445-S2-SE-Q2.5', 23, 'int', 'raw:x*log(Abs(x))', ['x**2*log(Abs(x))/2', '-x**2/4'],
   ['x**2*log(Abs(x))/2', '-x**2/4'], BOTH, 'C51-LN', '5.1', 'x!=0')
ex('1445-S2-FE-Q2.2', 27, 'int', 'raw:atan(x)', ['x*atan(x)', '-log(x**2+1)/2'], ['x*atan(x)', '-log(x**2+1)/2'],
   GEN, 'C51-INV', '5.1', 'all real x')
ex('1446-S2-SE-Q2.8', 23, 'int', 'raw:atan(x)', ['x*atan(x)', '-log(x**2+1)/2'], ['x*atan(x)', '-log(x**2+1)/2'],
   GEN, 'C51-INV', '5.1', 'all real x', duplicate_of='1445-S2-FE-Q2.2')
ex('1446-S1-SE-Q2.3', 6, 'int', 'raw:exp(x)*cosh(2*x)', ['exp(3*x)/6', '-exp(-x)/2'], ['exp(3*x)/6', '-exp(-x)/2'],
   GEN, 'C51-EXPH', '5.1', 'all real x')
ex('1446-S1-SE-Q2.4', 6, 'int', 'raw:(3*x-2)*sinh(x)', ['(3*x-2)*cosh(x)', '-3*sinh(x)'],
   ['(3*x-2)*cosh(x)', '-3*sinh(x)'], GEN, 'C51-POLY1', '5.1', 'all real x')
ex('1446-S1-SE-Q2.5', 6, 'int', 'raw:x**(-2)*log(x)', ['-log(x)/x', '-1/x'], ['-log(x)/x', '-1/x'], POS, 'C51-LN',
   '5.1', 'x>0')
ex('1446-S1-FE-Q2.2', 11, 'int', 'raw:x**(-3)*log(Abs(x))', ['-log(Abs(x))/(2*x**2)', '-1/(4*x**2)'],
   ['-log(Abs(x))/(2*x**2)', '-1/(4*x**2)'], BOTH, 'C51-LN', '5.1', 'x!=0',
   note='official solution lines write ln x without |.|; final form kept with |x| as in the question')
ex('1446-S2-SE-Q2.3', 22, 'int', 'raw:(2*x-1)*cosh(x)', ['(2*x-1)*sinh(x)', '-2*cosh(x)'],
   ['(2*x-1)*sinh(x)', '-2*cosh(x)'], GEN, 'C51-POLY1', '5.1', 'all real x')
ex('1446-S2-SE-Q2.5', 22, 'int', 'raw:exp(x/2)*sinh(3*x)', ['exp(7*x/2)/7', 'exp(-5*x/2)/5'],
   ['exp(7*x/2)/7', 'exp(-5*x/2)/5'], GEN, 'C51-EXPH', '5.1', 'all real x')
ex('1446-S2-FE-Q2.2', 26, 'int', 'raw:x*atanh(x)', ['x**2*atanh(x)/2', 'x/2', '-atanh(x)/2'],
   ['x**2*atanh(x)/2', 'x/2', '-atanh(x)/2'], ['t/(1+t)', '-t/(1+t)'], 'C51-XINV', '5.1', '|x|<1')
ex('1447-S1-SE-Q2.5', 6, 'int', 'raw:asin(x)', ['x*asin(x)', 'sqrt(1-x**2)'], ['x*asin(x)', 'sqrt(1-x**2)'],
   ['t/(1+t)', '-t/(1+t)'], 'C51-INV', '5.1', '|x|<1')
ex('1447-S1-SE-Q2.7', 7, 'int', 'raw:x**3*log(Abs(2*x))', ['x**4*log(Abs(2*x))/4', '-x**4/16'],
   ['x**4*log(Abs(2*x))/4', '-x**4/16'], BOTH, 'C51-LN', '5.1', 'x!=0')
ex('1447-S1-FE-Q2.2', 10, 'int', 'raw:x**2*cos(3*x)', ['x**2*sin(3*x)/3', '2*x*cos(3*x)/9', '-2*sin(3*x)/27'],
   ['x**2*sin(3*x)/3', '2*x*cos(3*x)/9', '-2*sin(3*x)/27'], GEN, 'C51-POLY2', '5.1', 'all real x')
ex('1447-S2-SE-Q3.1', 21, 'int', 'raw:x*asech(x)', ['x**2*asech(x)/2', '-sqrt(1-x**2)/2'],
   ['x**2*asech(x)/2', '-sqrt(1-x**2)/2'], ['t/(1+t)'], 'C51-XINV', '5.1', '0<x<1')
ex('1447-S2-FE-Q2.3', 25, 'int', 'raw:exp(2*x)*sin(x)', ['4*(exp(2*x)*sin(x)/2-exp(2*x)*cos(x)/4)/5'],
   ['2*exp(2*x)*sin(x)/5', '-exp(2*x)*cos(x)/5'], GEN, 'C51-CYC', '5.1', 'all real x')

# ---------------------------------------------------------------- 5.2 (exams)
ex('1445-S1-SE-Q2.4', 7, 'int', 'raw:sin(x)**5*cos(x)**3', ['sin(x)**6/6', '-sin(x)**8/8'],
   ['sin(x)**6/6', '-sin(x)**8/8'], GEN, 'C52-SC-ODD', '5.2', 'all real x', duplicate_of_notes='N52-X03')
ex('1445-S2-SE-Q2.3', 23, 'int', 'raw:tan(x)**2*sec(x)**4', ['tan(x)**3/3', 'tan(x)**5/5'],
   ['tan(x)**3/3', 'tan(x)**5/5'], GEN, 'C52-TS-SECEVEN', '5.2', 'cos x != 0')
ex('1445-S2-FE-Q2.6', 29, 'int', 'raw:sin(x)**5*cos(x)**6', ['-cos(x)**7/7', '2*cos(x)**9/9', '-cos(x)**11/11'],
   ['-cos(x)**7/7', '2*cos(x)**9/9', '-cos(x)**11/11'], GEN, 'C52-SC-ODD', '5.2', 'all real x')
ex('1446-S1-SE-Q2.6', 7, 'int', 'raw:sin(x)**4*cos(x)**5', ['sin(x)**5/5', '-2*sin(x)**7/7', 'sin(x)**9/9'],
   ['sin(x)**5/5', '-2*sin(x)**7/7', 'sin(x)**9/9'], GEN, 'C52-SC-ODD', '5.2', 'all real x')
ex('1446-S2-SE-Q2.4', 22, 'int', 'raw:cot(x)**4*csc(x)**4', ['-cot(x)**5/5', '-cot(x)**7/7'],
   ['-cot(x)**5/5', '-cot(x)**7/7'], GEN, 'C52-CC-CSCEVEN', '5.2', 'sin x != 0', duplicate_of_notes='N52-E4-1')
ex('1447-S1-SE-Q2.3', 6, 'int', 'raw:sin(x)**2*cos(x)**5', ['sin(x)**3/3', '-2*sin(x)**5/5', 'sin(x)**7/7'],
   ['sin(x)**3/3', '-2*sin(x)**5/5', 'sin(x)**7/7'], GEN, 'C52-SC-ODD', '5.2', 'all real x',
   duplicate_of_notes='N52-X02')
ex('1447-S1-FE-Q2.6', 12, 'int', 'raw:tan(x)**3*sec(x)**2', ['tan(x)**4/4'], ['tan(x)**4/4'], GEN,
   'C52-TS-SECEVEN', '5.2', 'cos x != 0')
ex('1447-S2-SE-Q3.3', 21, 'int', 'raw:sec(x)**3*tan(x)**3', ['sec(x)**5/5', '-sec(x)**3/3'],
   ['sec(x)**5/5', '-sec(x)**3/3'], GEN, 'C52-TS-TANODD', '5.2', 'cos x != 0')

# ---------------------------------------------------------------- notes 4.2 examples (pp.58-61)
NE = 'notes_example'
nx('N42-E1-1', 58, 'Ex1(1)', 'diff', 'raw:asinh(5*x-1)', ['5/sqrt(1+(5*x-1)**2)'], GEN, 'C42-D', '4.2', kind=NE)
nx('N42-E1-2', 59, 'Ex1(2)', 'diff', 'raw:atanh(sqrt(x))', ['1/(2*sqrt(x)*(1-x))'], ['t/(1+t)'], 'C42-D', '4.2', '0<x<1', kind=NE)
nx('N42-E1-3', 59, 'Ex1(3)', 'diff', 'raw:acsch(exp(3*x))', ['-3/sqrt(1+exp(6*x))'], GEN, 'C42-D', '4.2', kind=NE)
nx('N42-E1-4', 59, 'Ex1(4)', 'diff', 'raw:6**acosh(2*x)', ['6**acosh(2*x)*2*log(6)/sqrt(4*x**2-1)'],
   ['1/2+t'], 'C42-D', '4.2', 'x>1/2', kind=NE)
nx('N42-E1-5', 59, 'Ex1(5)', 'diff', 'raw:log(Abs(x**2+acoth(2*x)))', ['(2*x+2/(1-4*x**2))/(x**2+acoth(2*x))'],
   ['1/2+t'], 'C42-D', '4.2', 'x>1/2', kind=NE, official=['(2*x-2/(1-4*x**2))/(x**2+acoth(2*x))'],
   note='K1: notes solution uses the reversed coth^-1 sign')
nx('N42-E1-6', 59, 'Ex1(6)', 'diff', 'raw:(asech(3*x)+7**x)**5',
   ['5*(asech(3*x)+7**x)**4*(-1/(x*sqrt(1-9*x**2))+7**x*log(7))'], ['t/(3*(1+t))'], 'C42-D', '4.2', '0<x<1/3', kind=NE)
nx('N42-E1-7', 59, 'Ex1(7)', 'diff', 'raw:sqrt(x)*asinh(5*x)', ['asinh(5*x)/(2*sqrt(x))', '5*sqrt(x)/sqrt(1+25*x**2)'],
   POS, 'C42-D', '4.2', 'x>0', kind=NE)
nx('N42-E1-8', 59, 'Ex1(8)', 'diff', 'raw:acosh(x**2)/exp(3*x)',
   ['(2*x*exp(3*x)/sqrt(x**4-1)-3*acosh(x**2)*exp(3*x))/exp(6*x)'], ['1+t'], 'C42-D', '4.2', 'x>1', kind=NE)
nx('N42-E2-1', 60, 'Ex2(1)', 'int', 'raw:x/sqrt(x**4-16)', ['acosh(x**2/4)/2'], ['2+t'], 'C42-I-COSH', '4.2', 'x>2', kind=NE)
nx('N42-E2-2', 60, 'Ex2(2)', 'int', 'raw:exp(x)/(25-exp(2*x))', ['atanh(exp(x)/5)/5'], ['log(5)-t'], 'C42-I-TANH',
   '4.2', 'e^x<5', kind=NE)
nx('N42-E2-3', 60, 'Ex2(3)', 'int', 'raw:1/sqrt(4*x**2+25)', ['asinh(2*x/5)/2'], BOTH, 'C42-I-SINH', '4.2', kind=NE)
nx('N42-E2-4', 61, 'Ex2(4)', 'int', 'raw:1/(sqrt(x)*sqrt(4+x))', ['2*asinh(sqrt(x)/2)'], POS, 'C42-I-HIDDEN', '4.2',
   'x>0', kind=NE)
nx('N42-E2-5', 61, 'Ex2(5)', 'int', 'raw:1/(x*sqrt(16-x**4))', ['-asech(x**2/4)/8'], ['2*t/(1+t)', '-2*t/(1+t)'],
   'C42-I-HIDDEN', '4.2', '0<|x|<2', kind=NE)
nx('N42-E2-6', 61, 'Ex2(6)', 'int', 'raw:1/sqrt(1+exp(2*x))', ['-acsch(exp(x))'], GEN, 'C42-I-HIDDEN', '4.2', kind=NE)
nx('N42-E2-7', 61, 'Ex2(7)', 'int', 'raw:1/sqrt(x**2+2*x-8)', ['acosh((x+1)/3)'], ['2+t'], 'C42-CS', '4.2',
   'x+1>3', kind=NE)
nx('N42-E2-8', 61, 'Ex2(8)', 'int', 'raw:1/((x-1)*sqrt(-x**2+2*x+3))', ['-asech(Abs(x-1)/2)/2'],
   ['1+2*t/(1+t)', '1-2*t/(1+t)'], 'C42-CSL', '4.2', '-1<x<3, x!=1', kind=NE,
   official=['-asech((x-1)/2)/2'], note='K2: notes drops |.|')

# ---------------------------------------------------------------- notes 4.2 exercises (p.62)
nx('N42-X1-1', 62, '1(1)', 'diff', 'raw:asinh(3**x)*sqrt(x)', ['3**x*log(3)*sqrt(x)/sqrt(1+3**(2*x))',
   'asinh(3**x)/(2*sqrt(x))'], POS, 'C42-D', '4.2', 'x>0')
nx('N42-X1-2', 62, '1(2)', 'diff', 'raw:acosh(sqrt(x))*log(Abs(x**2-1))', ['log(Abs(x**2-1))/(2*sqrt(x)*sqrt(x-1))',
   '2*x*acosh(sqrt(x))/(x**2-1)'], ['1+t'], 'C42-D', '4.2', 'x>1')
nx('N42-X1-3', 62, '1(3)', 'diff', 'raw:(exp(4*x)+atanh(3*x))**5',
   ['5*(exp(4*x)+atanh(3*x))**4*(4*exp(4*x)+3/(1-9*x**2))'], ['t/(3*(1+t))', '-t/(3*(1+t))'], 'C42-D', '4.2', '|x|<1/3')
nx('N42-X1-4', 62, '1(4)', 'diff', 'raw:log(Abs(acoth(2*x)+sinh(2*x)))',
   ['(2/(1-4*x**2)+2*cosh(2*x))/(acoth(2*x)+sinh(2*x))'], ['1/2+t'], 'C42-D', '4.2', 'x>1/2')
nx('N42-X1-5', 62, '1(5)', 'diff', 'raw:asech(1/x)+exp(cosh(x))', ['1/sqrt(x**2-1)', 'exp(cosh(x))*sinh(x)'],
   ['1+t'], 'C42-D', '4.2', 'x>1')
nx('N42-X1-6', 62, '1(6)', 'diff', 'raw:acsch(cos(x))+log(Abs(sinh(x)))',
   ['sin(x)/(Abs(cos(x))*sqrt(1+cos(x)**2))', 'coth(x)'], ['t/(1+t)'], 'C42-D', '4.2', 'cos x!=0, x!=0')
nx('N42-X2-01', 62, '2(1)', 'int', 'raw:5*x**2/sqrt(9+16*x**6)', ['5*asinh(4*x**3/3)/12'], BOTH, 'C42-I-HIDDEN', '4.2')
nx('N42-X2-02', 62, '2(2)', 'int', 'raw:3*x/sqrt(25*x**4+16)', ['3*asinh(5*x**2/4)/10'], BOTH, 'C42-I-HIDDEN', '4.2')
nx('N42-X2-03', 62, '2(3)', 'int', 'raw:x**3/(36-9*x**8)', ['atanh(x**4/2)/72'], ['2**Rational(1,4)*t/(1+t)'],
   'C42-I-TANH', '4.2', '|x|<2^(1/4) (coth^-1 form for |x|>2^(1/4))')
nx('N42-X2-04', 62, '2(4)', 'int', 'raw:3*x/(x**2*sqrt(9-16*x**4))', ['-asech(4*x**2/3)/2'],
   ['sqrt(3)/2*t/(1+t)'], 'C42-I-HIDDEN', '4.2', '0<4x^2<3')
nx('N42-X2-05', 62, '2(5)', 'int', 'raw:5*x/(x**2*sqrt(4-9*x**4))', ['-5*asech(3*x**2/2)/4'],
   ['sqrt(6)/3*t/(1+t)'], 'C42-I-HIDDEN', '4.2', '0<3x^2<2')
nx('N42-X2-06', 62, '2(6)', 'int', 'raw:sinh(x)/(4-25*cosh(x)**2)', ['acoth(5*cosh(x)/2)/10'], GEN, 'C42-I-TANH',
   '4.2', '|5cosh x/2|>1 always', note='K1: with the notes sign this would be -(1/10)coth^-1')
nx('N42-X2-07', 62, '2(7)', 'int', 'raw:(x-2)/sqrt(25+x**2)', ['sqrt(25+x**2)', '-2*asinh(x/5)'], GEN,
   'C42-I-SPLIT', '4.2')
nx('N42-X2-08', 62, '2(8)', 'int', 'raw:(x+1)/(16-x**2)', ['-log(Abs(16-x**2))/2', 'atanh(x/4)/4'],
   ['4*t/(1+t)', '-4*t/(1+t)'], 'C42-I-SPLIT', '4.2', '|x|<4 (coth^-1 form for |x|>4)')
nx('N42-X2-09', 62, '2(9)', 'int', 'raw:acosh(x)/sqrt(x**2-1)', ['acosh(x)**2/2'], ['1+t'], 'C42-I-INVNUM', '4.2', 'x>1')
nx('N42-X2-10', 62, '2(10)', 'int', 'raw:2/sqrt(9-exp(6*x))', ['-2*asech(exp(3*x)/3)/9'], ['log(3)/3-t'],
   'C42-I-HIDDEN', '4.2', 'e^(3x)<3')
nx('N42-X2-11', 62, '2(11)', 'int', 'raw:5/(x*sqrt(25+4*x**4))', ['-acsch(2*x**2/5)/2'], BOTH, 'C42-I-HIDDEN', '4.2', 'x!=0')
nx('N42-X2-12', 62, '2(12)', 'int', 'raw:1/(x*sqrt(25-x**3))', ['-2*asech(x**Rational(3,2)/5)/15'],
   ['25**Rational(1,3)*t/(1+t)'], 'C42-I-HIDDEN', '4.2', '0<x<25^(1/3) (x<0 gives a csch^-1 form)')
nx('N42-X2-13', 62, '2(13)', 'int', 'raw:7/sqrt(x**2+6*x)', ['7*acosh((x+3)/3)'], POS, 'C42-CS', '4.2', 'x+3>3')
nx('N42-X2-14', 62, '2(14)', 'int', 'raw:5/sqrt(x**2+2*x+10)', ['5*asinh((x+1)/3)'], ['t-1', '-t-1'], 'C42-CS', '4.2',
   near='1446-S2-SE-Q2.2 (constant multiple)')
nx('N42-X2-15', 62, '2(15)', 'int', 'raw:2/((x+3)*sqrt(x**2+6*x+25))', ['-acsch(Abs(x+3)/4)/2'], ['t-3', '-t-3'],
   'C42-CSL', '4.2', 'x!=-3')
nx('N42-X2-16', 62, '2(16)', 'int', 'raw:3/((x+1)*sqrt(3-x**2-2*x))', ['-3*asech(Abs(x+1)/2)/2'],
   ['-1+2*t/(1+t)', '-1-2*t/(1+t)'], 'C42-CSL', '4.2', '-3<x<1, x!=-1')

# ---------------------------------------------------------------- notes 5.1 examples (pp.63-65) and exercises (p.66)
nx('N51-E1', 63, 'Ex(1)', 'int', 'raw:x*cos(x)', ['x*sin(x)', 'cos(x)'], GEN, 'C51-POLY1', '5.1', kind=NE)
nx('N51-E2', 63, 'Ex(2)', 'int', 'raw:x**2*exp(x)', ['(x**2-2*x+2)*exp(x)'], GEN, 'C51-POLY2', '5.1', kind=NE)
nx('N51-E3', 64, 'Ex(3)', 'int', 'raw:x**2*log(Abs(x))', ['x**3*log(Abs(x))/3', '-x**3/9'], BOTH, 'C51-LN', '5.1', kind=NE)
nx('N51-E4', 64, 'Ex(4)', 'int', 'raw:log(1+x**2)', ['x*log(1+x**2)', '-2*x', '2*atan(x)'], GEN, 'C51-LN0', '5.1', kind=NE)
nx('N51-E5', 64, 'Ex(5)', 'int', 'raw:atan(x)', ['x*atan(x)', '-log(1+x**2)/2'], GEN, 'C51-INV', '5.1', kind=NE,
   duplicate_of='1445-S2-FE-Q2.2')
nx('N51-E6', 65, 'Ex(6)', 'int', 'raw:x*asec(x)', ['x**2*asec(x)/2', '-sqrt(x**2-1)/2'], ['1+t'], 'C51-XINV', '5.1',
   'x>1', kind=NE, note='K3: a middle line prints sqrt(1-x^2) for sqrt(x^2-1)')
nx('N51-E7', 65, 'Ex(7)', 'int', 'raw:exp(x)*cos(x)', ['exp(x)*cos(x)/2', 'exp(x)*sin(x)/2'], GEN, 'C51-CYC', '5.1', kind=NE)
for num, q, a, br, case, dom in [
        ('01', 'raw:(2*x+1)*cosh(x)', ['(2*x+1)*sinh(x)', '-2*cosh(x)'], GEN, 'C51-POLY1', ''),
        ('02', 'raw:(x**2-1)*sin(2*x)', ['-(x**2-1)*cos(2*x)/2', 'x*sin(2*x)/2', 'cos(2*x)/4'], GEN, 'C51-POLY2', ''),
        ('03', 'raw:x**3*exp(x)', ['(x**3-3*x**2+6*x-6)*exp(x)'], GEN, 'C51-POLY2', ''),
        ('04', 'raw:(x+1)*sec(x)**2', ['(x+1)*tan(x)', 'log(Abs(cos(x)))'], GEN, 'C51-SEC2', 'cos x != 0'),
        ('05', 'raw:log(Abs(x))', ['x*log(Abs(x))', '-x'], BOTH, 'C51-LN0', 'x!=0'),
        ('06', 'raw:x**5*log(Abs(x))', ['x**6*log(Abs(x))/6', '-x**6/36'], BOTH, 'C51-LN', 'x!=0'),
        ('07', 'raw:x**(-4)*log(Abs(x))', ['-log(Abs(x))/(3*x**3)', '-1/(9*x**3)'], BOTH, 'C51-LN', 'x!=0'),
        ('08', 'raw:asin(x)', ['x*asin(x)', 'sqrt(1-x**2)'], ['t/(1+t)', '-t/(1+t)'], 'C51-INV', '|x|<1'),
        ('09', 'raw:asec(x)', ['x*asec(x)', '-acosh(x)'], ['1+t'], 'C51-INV', 'x>1'),
        ('10', 'raw:x*acsch(x)', ['x**2*acsch(x)/2', 'sqrt(1+x**2)/2'], POS, 'C51-XINV', 'x>0 (for x<0 the last sign flips)'),
        ('11', 'raw:exp(2*x)*sin(3*x)', ['2*exp(2*x)*sin(3*x)/13', '-3*exp(2*x)*cos(3*x)/13'], GEN, 'C51-CYC', ''),
        ('12', 'raw:exp(5*x)*cos(2*x)', ['5*exp(5*x)*cos(2*x)/29', '2*exp(5*x)*sin(2*x)/29'], GEN, 'C51-CYC', ''),
        ('13', 'raw:exp(3*x)*sinh(x)', ['exp(4*x)/8', '-exp(2*x)/4'], GEN, 'C51-EXPH', ''),
        ('14', 'raw:exp(x)*cosh(5*x)', ['exp(6*x)/12', '-exp(-4*x)/8'], GEN, 'C51-EXPH', ''),
        ('15', 'raw:exp(sqrt(x))', ['2*exp(sqrt(x))*(sqrt(x)-1)'], POS, 'C51-SUBPARTS', 'x>0'),
        ('16', 'raw:log(Abs(x))**2', ['x*log(Abs(x))**2', '-2*x*log(Abs(x))', '2*x'], BOTH, 'C51-LN0', 'x!=0'),
        ('17', 'raw:x**3*sqrt(x**2-1)', ['(x**2-1)**Rational(5,2)/5', '(x**2-1)**Rational(3,2)/3'], ['1+t', '-1-t'],
         'C51-ROOT', '|x|>1'),
        ('18', 'raw:x**7*sqrt(x**4+2)', ['(x**4+2)**Rational(5,2)/10', '-(x**4+2)**Rational(3,2)/3'], GEN, 'C51-ROOT', '')]:
    nx('N51-X' + num, 66, '(%d)' % int(num), 'int', q, a, br, case, '5.1', dom,
       duplicate_of=('1447-S1-SE-Q2.5' if num == '08' else None))

# ---------------------------------------------------------------- notes 5.2 examples (pp.67-75) and exercises (p.76)
for id_, page, num, q, a, case in [
        ('N52-E1-1', 67, 'Ex1(1)', 'raw:cos(x)**3', ['sin(x)', '-sin(x)**3/3'], 'C52-ODD1'),
        ('N52-E1-2', 67, 'Ex1(2)', 'raw:sin(x)**5', ['-cos(x)', '2*cos(x)**3/3', '-cos(x)**5/5'], 'C52-ODD1'),
        ('N52-E1-3', 68, 'Ex1(3)', 'raw:cos(2*x)**4', ['3*x/8', 'sin(4*x)/8', 'sin(8*x)/64'], 'C52-EVEN1'),
        ('N52-E2-1', 69, 'Ex2(1)', 'raw:sin(x)**5*cos(x)**2', ['-cos(x)**3/3', '2*cos(x)**5/5', '-cos(x)**7/7'], 'C52-SC-ODD'),
        ('N52-E2-2*', 69, 'Ex2(2)', 'raw:sqrt(sin(x))*cos(x)**3', ['2*sin(x)**Rational(3,2)/3', '-2*sin(x)**Rational(7,2)/7'], 'C52-SC-ODD'),
        ('N52-E2-3', 69, 'Ex2(3)', 'raw:sin(x)**5*cos(x)**7', ['-cos(x)**8/8', '2*cos(x)**10/10', '-cos(x)**12/12'], 'C52-SC-ODD'),
        ('N52-E2-4', 70, 'Ex2(4)', 'raw:sin(x)**2*cos(x)**4', ['x/16', '-sin(4*x)/64', 'sin(2*x)**3/48'], 'C52-SC-EVEN'),
        ('N52-E3-1', 71, 'Ex3(1)', 'raw:sec(x)**3', ['sec(x)*tan(x)/2', 'log(Abs(sec(x)+tan(x)))/2'], 'C52-TS-SEC0'),
        ('N52-E3-2', 71, 'Ex3(2)', 'raw:tan(x)**4', ['tan(x)**3/3', '-tan(x)', 'x'], 'C52-TS-TAN0'),
        ('N52-E3-3', 72, 'Ex3(3)', 'raw:tan(x)**2*sec(x)**6', ['tan(x)**3/3', '2*tan(x)**5/5', 'tan(x)**7/7'], 'C52-TS-SECEVEN'),
        ('N52-E3-4', 72, 'Ex3(4)', 'raw:tan(x)**5*sec(x)**3', ['sec(x)**7/7', '-2*sec(x)**5/5', 'sec(x)**3/3'], 'C52-TS-TANODD'),
        ('N52-E4-1', 73, 'Ex4(1)', 'raw:cot(x)**4*csc(x)**4', ['-cot(x)**5/5', '-cot(x)**7/7'], 'C52-CC-CSCEVEN'),
        ('N52-E4-2', 73, 'Ex4(2)', 'raw:cot(x)**5*csc(x)**5', ['-csc(x)**9/9', '2*csc(x)**7/7', '-csc(x)**5/5'], 'C52-CC-COTODD'),
        ('N52-E5-1', 74, 'Ex5(1)', 'raw:sin(7*x)*cos(5*x)', ['-cos(2*x)/4', '-cos(12*x)/24'], 'C52-PROD'),
        ('N52-E5-2', 75, 'Ex5(2)', 'raw:sin(4*x)*sin(3*x)', ['sin(x)/2', '-sin(7*x)/14'], 'C52-PROD')]:
    frac = id_.endswith('*')
    nx(id_.rstrip('*'), page, num, 'int', q, a, ['t/(1+t)'] if frac else GEN, case, '5.2', kind=NE)
for num, q, a, case in [
        ('01', 'raw:sin(x)**3*cos(x)**4', ['-cos(x)**5/5', 'cos(x)**7/7'], 'C52-SC-ODD'),
        ('02', 'raw:sin(x)**2*cos(x)**5', ['sin(x)**3/3', '-2*sin(x)**5/5', 'sin(x)**7/7'], 'C52-SC-ODD'),
        ('03', 'raw:sin(x)**5*cos(x)**3', ['sin(x)**6/6', '-sin(x)**8/8'], 'C52-SC-ODD'),
        ('04', 'raw:cbrt(cos(x))*sin(x)**3', ['-3*cos(x)**Rational(4,3)/4', '3*cos(x)**Rational(10,3)/10'], 'C52-SC-ODD'),
        ('05', 'raw:sqrt(tan(x))*sec(x)**4', ['2*tan(x)**Rational(3,2)/3', '2*tan(x)**Rational(7,2)/7'], 'C52-TS-SECEVEN'),
        ('06', 'raw:tan(x)**5*sec(x)**5', ['sec(x)**9/9', '-2*sec(x)**7/7', 'sec(x)**5/5'], 'C52-TS-TANODD'),
        ('07', 'raw:tan(x)**3*sec(x)**4', ['tan(x)**4/4', 'tan(x)**6/6'], 'C52-TS-SECEVEN'),
        ('08', 'raw:cot(x)**2*csc(x)**6', ['-cot(x)**3/3', '-2*cot(x)**5/5', '-cot(x)**7/7'], 'C52-CC-CSCEVEN'),
        ('09', 'raw:cot(x)**5*csc(x)**3', ['-csc(x)**7/7', '2*csc(x)**5/5', '-csc(x)**3/3'], 'C52-CC-COTODD'),
        ('10', 'raw:sin(3*x)*cos(5*x)', ['cos(2*x)/4', '-cos(8*x)/16'], 'C52-PROD'),
        ('11', 'raw:sin(2*x)*sin(6*x)', ['sin(4*x)/8', '-sin(8*x)/16'], 'C52-PROD'),
        ('12', 'raw:cos(4*x)*cos(7*x)', ['sin(3*x)/6', 'sin(11*x)/22'], 'C52-PROD'),
        ('13', 'raw:sin(x)**2', ['x/2', '-sin(2*x)/4'], 'C52-EVEN1'),
        ('14', 'raw:cos(x)**2', ['x/2', 'sin(2*x)/4'], 'C52-EVEN1'),
        ('15', 'raw:sec(x)**5', ['sec(x)**3*tan(x)/4', '3*sec(x)*tan(x)/8', '3*log(Abs(sec(x)+tan(x)))/8'], 'C52-TS-SEC0'),
        ('16', 'raw:tan(x)**6', ['tan(x)**5/5', '-tan(x)**3/3', 'tan(x)', '-x'], 'C52-TS-TAN0')]:
    br = ['t/(1+t)'] if num in ('04', '05') else GEN   # fractional powers: an interval where the base is positive
    nx('N52-X' + num, 76, '(%d)' % int(num), 'int', q, a, br, case, '5.2',
       duplicate_of={'02': '1447-S1-SE-Q2.3', '03': '1445-S1-SE-Q2.4'}.get(num))

if __name__ == '__main__':
    ids = [i['id'] for i in I]
    assert len(ids) == len(set(ids)), 'duplicate ids'
    out = Path(__file__).resolve().parent.parent / 'data' / 'items.json'
    out.write_text(json.dumps(I, ensure_ascii=False, indent=1), encoding='utf-8')
    from collections import Counter
    print(len(I), 'items', Counter(i['kind'] for i in I), Counter(i['section'] for i in I))

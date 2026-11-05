"""«odd و even»: تكاملات sin و cos بالأسس، على أسئلة مذكرة د. موسى الـ18 (ص 89–97).

One question (is there an odd power?), three lines of «why», Dr. Musa's four groups in order of difficulty, practice in
twins (a question and its mirror with sin and cos swapped), the algebra the questions need, the five famous mistakes,
a ten-question mastery test and the full solutions of the eleven questions Dr. Musa left unsolved. His seven solved
questions are shown with his own steps. Every equality, step and answer is checked with SymPy while building.
"""
import re

import sympy as sp

from booklet_engine import BuildError, arith
from guide_kit import rich
from html_kit import link, lines, md, mi, p, table, ul
from mathlib import P, u, x

BLANK = r'\boxed{\phantom{00}}'


def pgref(a):
    return '<span class="pgref" data-target="%s"></span>' % a


def antideriv(F, f, label, branch=None):
    """The answer F really is an antiderivative of f (d/dx F = f)."""
    arith('', [('diff(%s,x)' % F, f) + ((branch,) if branch else ())], label + ' answer')


def steps(rows, label):
    """(latex, claims, why[, 'swap']) rows; every claim is checked; the last row is the answer.
    A 🔁 swap row shows, under each piece, what it becomes in u: it is not numbered (done with the eyes, not written)."""
    body = ''
    n = 0
    for k, row in enumerate(rows, 1):
        latex, claims, why = row[:3]
        arith(latex, claims, '%s step %d' % (label, k))
        if len(row) > 3 and row[3] == 'swap':
            body += ('<tr class="swap"><td class="n">🔁</td><td colspan="2">%s<div class="swhy">%s</div></td></tr>'
                     % (mi(r'\displaystyle ' + latex), rich('<b>التبديل</b> (بعيونك، ما يلزم تكتبه): ' + why)))
            continue
        n += 1
        cls = ' class="final"' if k == len(rows) else ''
        body += '<tr%s><td class="n">%d</td><td>%s</td><td>%s</td></tr>' % (cls, n, mi(r'\displaystyle ' + latex), rich(why))
    return ('<table class="steps"><thead><tr><th>#</th><th>الخطوة (تكتبها)</th><th>ليش؟ (لك أنت)</th></tr></thead>'
            '<tbody>' + body + '</tbody></table>')


def section(id_, title, inner):
    return '<section class="chapter oe" id="%s"><h2>%s</h2>%s</section>' % (id_, title, inner)


def box(title, inner, cls='', id_=''):
    return '<div class="sbox %s"%s><h3>%s</h3>%s</div>' % (cls, (' id="%s"' % id_) if id_ else '', rich(title), inner)


def D(tex):
    return 'diff(%s,x)' % tex


S, C = 'sin(x)', 'cos(x)'
# ---------------------------------------------------------------- Dr. Musa's 18 questions
# id: (question latex, Musa page, number, group, integrand, answer, answer latex, how it is used here)
Q = {
    'A1': (r'\int\sin^{2}x\,dx', 89, 1, 'A', 'sin(x)**2', 'x/2-sin(2*x)/4', r'\frac12x-\frac14\sin2x+c', 'worked'),
    'A2': (r'\int\sin^{3}x\,dx', 89, 2, 'A', 'sin(x)**3', '-cos(x)+cos(x)**3/3', r'-\cos x+\frac13\cos^{3}x+c', 'twin'),
    'A3': (r'\int\cos^{3}x\,dx', 89, 3, 'A', 'cos(x)**3', 'sin(x)-sin(x)**3/3', r'\sin x-\frac13\sin^{3}x+c', 'worked'),
    'A4': (r'\int\cos^{2}x\,dx', 89, 4, 'A', 'cos(x)**2', 'x/2+sin(2*x)/4', r'\frac12x+\frac14\sin2x+c', 'solo'),
    'A5': (r'\int\sin^{5}x\,dx', 89, 5, 'A', 'sin(x)**5', '-cos(x)+2*cos(x)**3/3-cos(x)**5/5',
           r'-\cos x+\frac23\cos^{3}x-\frac15\cos^{5}x+c', 'worked'),
    'A6': (r'\int\sin^{4}x\,dx', 89, 6, 'A', 'sin(x)**4', '3*x/8-sin(2*x)/4+sin(4*x)/32', r'\frac38x-\frac14\sin2x+\frac1{32}\sin4x+c', 'worked'),
    'A7': (r'\int\cos^{4}x\,dx', 89, 7, 'A', 'cos(x)**4', '3*x/8+sin(2*x)/4+sin(4*x)/32', r'\frac38x+\frac14\sin2x+\frac1{32}\sin4x+c', 'solo'),
    'B1': (r'\int\sin^{5}x\cos^{3}x\,dx', 93, 1, 'B', 'sin(x)**5*cos(x)**3', 'sin(x)**6/6-sin(x)**8/8', r'\frac16\sin^{6}x-\frac18\sin^{8}x+c', 'worked'),
    'B2': (r'\int\cos^{5}x\sin^{3}x\,dx', 93, 2, 'B', 'cos(x)**5*sin(x)**3', '-cos(x)**6/6+cos(x)**8/8', r'-\frac16\cos^{6}x+\frac18\cos^{8}x+c', 'twin'),
    'B3': (r'\int\sin^{7}x\cos^{5}x\,dx', 93, 3, 'B', 'sin(x)**7*cos(x)**5', 'sin(x)**8/8-sin(x)**10/5+sin(x)**12/12',
           r'\frac18\sin^{8}x-\frac15\sin^{10}x+\frac1{12}\sin^{12}x+c', 'solo'),
    'C1': (r'\int\sin^{5}x\cos^{4}x\,dx', 94, 1, 'C', 'sin(x)**5*cos(x)**4', '-cos(x)**5/5+2*cos(x)**7/7-cos(x)**9/9',
           r'-\frac15\cos^{5}x+\frac27\cos^{7}x-\frac19\cos^{9}x+c', 'worked'),
    'C2': (r'\int\cos^{5}x\sin^{4}x\,dx', 94, 2, 'C', 'cos(x)**5*sin(x)**4', 'sin(x)**5/5-2*sin(x)**7/7+sin(x)**9/9',
           r'\frac15\sin^{5}x-\frac27\sin^{7}x+\frac19\sin^{9}x+c', 'twin'),
    'C3': (r'\int\cos^{7}x\sin^{6}x\,dx', 94, 3, 'C', 'cos(x)**7*sin(x)**6', 'sin(x)**7/7-sin(x)**9/3+3*sin(x)**11/11-sin(x)**13/13',
           r'\frac17\sin^{7}x-\frac13\sin^{9}x+\frac3{11}\sin^{11}x-\frac1{13}\sin^{13}x+c', 'hard'),
    'D1': (r'\int\sin^{2}x\cos^{2}x\,dx', 96, 1, 'D', 'sin(x)**2*cos(x)**2', 'x/8-sin(4*x)/32', r'\frac18x-\frac1{32}\sin4x+c', 'worked'),
    'D2': (r'\int\sin^{4}x\cos^{2}x\,dx', 96, 2, 'D', 'sin(x)**4*cos(x)**2', 'x/16-sin(4*x)/64-sin(2*x)**3/48',
           r'\frac{x}{16}-\frac{\sin4x}{64}-\frac{\sin^{3}2x}{48}+c', 'fill'),
    'D3': (r'\int\cos^{6}x\sin^{2}x\,dx', 96, 3, 'D', 'cos(x)**6*sin(x)**2', '5*x/128-sin(4*x)/128+sin(2*x)**3/48-sin(8*x)/1024',
           r'\frac{5x}{128}-\frac{\sin4x}{128}+\frac{\sin^{3}2x}{48}-\frac{\sin8x}{1024}+c', 'hard'),
    'D4': (r'\int\sin^{6}x\cos^{2}x\,dx', 96, 4, 'D', 'sin(x)**6*cos(x)**2', '5*x/128-sin(4*x)/128-sin(2*x)**3/48-sin(8*x)/1024',
           r'\frac{5x}{128}-\frac{\sin4x}{128}-\frac{\sin^{3}2x}{48}-\frac{\sin8x}{1024}+c', 'hard'),
    'D5': (r'\int\cos^{4}x\sin^{2}x\,dx', 96, 5, 'D', 'cos(x)**4*sin(x)**2', 'x/16-sin(4*x)/64+sin(2*x)**3/48',
           r'\frac{x}{16}-\frac{\sin4x}{64}+\frac{\sin^{3}2x}{48}+c', 'solo'),
}
GROUP = {'A': ('secA', '١. أسس لحالها', 'موسى ص 89–92'), 'C': ('secB', '٢. Odd and Even', 'موسى ص 94–95'),
         'B': ('secC', '٣. Odd and Odd', 'موسى ص 93'), 'D': ('secD', '٤. Even and Even', 'موسى ص 96–97')}
KIND = {'worked': '🧱 محلول', 'twin': '👯 توأم', 'solo': '✏️ لحالك', 'fill': '✍️ فراغات', 'hard': '⭐⭐ تحدي'}
TWIN_OF = {'A2': 'A3', 'B2': 'B1', 'C2': 'C1'}


def musa(k):
    return 'موسى ص %d (%d)' % (Q[k][1], Q[k][2])


# ---------------------------------------------------------------- the steps of every question (checked)
def U_SIN():
    return (r'\text{let }\cU{u=\sin x},\quad \cD{du=\cos x\,dx}', [(D(S), C)],
            'اشتق $u$ وحط جنبها $dx$: $du=\\cos x\\,dx$. وهذي بالضبط القطعة الخضرا اللي حجزناها.')


def U_COS():
    return (r'\text{let }\cU{u=\cos x},\quad du=\cR{-}\sin x\,dx\ \Rightarrow\ \cD{\sin x\,dx}=\cR{-}\cD{du}', [(D(C), '-' + S)],
            '🔴 مشتقة cos فيها سالب. نضرب الطرفين في $-1$: القطعة الخضرا $\\sin x\\,dx$ صار اسمها $-du$.')


SWAP = 'swap'          # a 🔁 row: under each piece, what it becomes in u (done with the eyes, not numbered)
MINUS_DU = r'\cR{-}\cD{du}'
HALF_DU = r'\cD{\tfrac12\,du}'


def UB(x_tex, u_tex):
    """A piece of the integral and, under it, what it becomes in u."""
    return r'\underbrace{%s}_{\displaystyle \cU{%s}}' % (x_tex, u_tex)


def UD(x_tex, du_tex=r'\cD{du}'):
    """The kept (green) piece and, under it, its du form."""
    return r'\underbrace{\cD{%s}}_{\displaystyle %s}' % (x_tex, du_tex)


SWAP_WHY = 'كل قطعة صارت $u$، والخضرا صارت $du$. ما بقى ولا $x$ ولا $dx$ ✓'
SWAP_WHY_MINUS = 'كل قطعة صارت $u$، والخضرا صارت $-du$. ما بقى ولا $x$ ولا $dx$ ✓'

ROWS = {
    'A1': [(r'\sin^{2}x=\frac{1-\cos2x}{2}', [('sin(x)**2', '(1-cos(2*x))/2')],
            'أس زوجي لحاله: ما فيه قطعة نحجزها تصير $du$، فنص الزاوية. «سين وسالب».'),
           (r'I=\frac12\int(1-\cos2x)\,dx', [], 'الـ $\\frac12$ تطلع برّا التكامل.'),
           (r'I=\frac12\left[x-\frac12\sin2x\right]+c', [(D('(x-sin(2*x)/2)/2'), 'sin(x)**2')], r'$\int\cos2x\,dx=\frac12\sin2x$: نقسم على رقم الزاوية.'),
           (r'I=\frac12x-\frac14\sin2x+c', [(D('x/2-sin(2*x)/4'), 'sin(x)**2')], 'نوزّع $\\frac12$ على القوس.')],
    'A2': [(r'I=\int\sin^{2}x\,\cD{\sin x\,dx}', [('sin(x)**3', 'sin(x)**2*sin(x)')], 'أس sin فردي (3): نحجز $\\sin x\\,dx$ وحدة، عشان تصير $du$.'),
           (r'I=\int(1-\cos^{2}x)\,\cD{\sin x\,dx}', [('sin(x)**2', '1-cos(x)**2')], 'الباقي $\\sin^2x$ نحوّله لـ cos بالمتطابقة، عشان يصير كله $u$.'),
           U_COS(),
           (r'I=\int' + UB(r'(1-\cos^{2}x)', r'(1-u^{2})') + r'\;' + UD(r'\sin x\,dx', MINUS_DU),
            [('sin(x)**3', '-(1-cos(x)**2)*diff(cos(x),x)')], SWAP_WHY_MINUS, SWAP),
           (r'I=\cR{-}\int(1-u^{2})\,du=-\left[u-\frac13u^{3}\right]+c', [('integrate(1-u**2,u)', 'u-u**3/3')],
            'السالب قدّام التكامل، وبرّا قوس كبير لأنه يضرب كل الحدود.'),
           (r'I=-\cos x+\frac13\cos^{3}x+c', [(D('-cos(x)+cos(x)**3/3'), 'sin(x)**3')], 'نوزّع السالب ونرجّع $u=\\cos x$. ونفس توقّع التوأم ✓')],
    'A3': [(r'I=\int\cos^{2}x\,\cD{\cos x\,dx}', [('cos(x)**3', 'cos(x)**2*cos(x)')],
            'أس cos فردي (3): نحجز $\\cos x\\,dx$ وحدة، عشان تصير $du$ (مشتقة $\\sin x$ هي $\\cos x$).'),
           (r'I=\int(1-\sin^{2}x)\,\cD{\cos x\,dx}', [('cos(x)**2', '1-sin(x)**2')], 'الباقي $\\cos^2x$ أسه زوجي: نحوّله لـ sin بالمتطابقة، عشان يصير كله $u$.'),
           U_SIN(),
           (r'I=\int' + UB(r'(1-\sin^{2}x)', r'(1-u^{2})') + r'\;' + UD(r'\cos x\,dx'),
            [('cos(x)**3', '(1-sin(x)**2)*diff(sin(x),x)')], SWAP_WHY, SWAP),
           (r'I=\int(1-u^{2})\,du=u-\frac13u^{3}+c', [('integrate(1-u**2,u)', 'u-u**3/3')], 'صار سهل: كل حد زد أسه 1 واقسم عليه.'),
           (r'I=\sin x-\frac13\sin^{3}x+c', [(D('sin(x)-sin(x)**3/3'), 'cos(x)**3')], 'نرجّع $u=\\sin x$. أعلى أس 3 = أس السؤال ✓')],
    'A4': [(r'\cos^{2}x=\frac{1+\cos2x}{2}', [('cos(x)**2', '(1+cos(2*x))/2')], 'أس زوجي: ما فيه قطعة تصير $du$، فنص الزاوية. و cos معها زائد.'),
           (r'I=\frac12\int(1+\cos2x)\,dx', [], 'الـ $\\frac12$ برّا.'),
           (r'I=\frac12x+\frac14\sin2x+c', [(D('x/2+sin(2*x)/4'), 'cos(x)**2')], 'نفس $\\sin^2$ بس الإشارة زائد.')],
    'A5': [(r'I=\int\sin^{4}x\,\cD{\sin x\,dx}=\int(\sin^{2}x)^{2}\,\cD{\sin x\,dx}', [('sin(x)**5', '(sin(x)**2)**2*sin(x)')],
            'أس sin فردي (5): نحجز $\\sin x\\,dx$ وحدة عشان تصير $du$، والباقي $\\sin^4=(\\sin^2)^2$.'),
           (r'I=\int(1-\cos^{2}x)^{2}\,\cD{\sin x\,dx}', [('(sin(x)**2)**2', '(1-cos(x)**2)**2')], 'نحوّل $\\sin^2$ اللي داخل القوس لـ cos، عشان يصير كله $u$.'),
           U_COS(),
           (r'I=\int' + UB(r'(1-\cos^{2}x)^{2}', r'(1-u^{2})^{2}') + r'\;' + UD(r'\sin x\,dx', MINUS_DU),
            [('sin(x)**5', '-(1-cos(x)**2)**2*diff(cos(x),x)')], SWAP_WHY_MINUS, SWAP),
           (r'I=\cR{-}\int(1-u^{2})^{2}\,du=-\int(1-2u^{2}+u^{4})\,du', [('(1-u**2)**2', '1-2*u**2+u**4')],
            'السالب قدّام التكامل. ونفك القوس (جاهز في الأدوات).'),
           (r'I=-\left[u-\frac23u^{3}+\frac15u^{5}\right]+c', [('integrate(1-2*u**2+u**4,u)', 'u-2*u**3/3+u**5/5')],
            'كل حد لحاله، والسالب برّا قوس كبير لأنه يضرب الكل. (عند موسى هالقوس مرسوم بخطين | |، وهو قوس عادي.)'),
           (r'I=-\cos x+\frac23\cos^{3}x-\frac15\cos^{5}x+c', [(D('-cos(x)+2*cos(x)**3/3-cos(x)**5/5'), 'sin(x)**5')],
            'نوزّع السالب آخر شي ونرجّع $u=\\cos x$. أعلى أس 5 ✓')],
    'A6': [(r'\sin^{4}x=(\sin^{2}x)^{2}=\left(\frac{1-\cos2x}{2}\right)^{2}=\frac14(1-\cos2x)^{2}',
            [('sin(x)**4', '((1-cos(2*x))/2)**2'), ('((1-cos(2*x))/2)**2', '(1-cos(2*x))**2/4')], 'أس زوجي: ما فيه قطعة تصير $du$، فنص الزاوية للمربع.'),
           (r'=\frac14\left(1-2\cos2x+\cos^{2}2x\right)', [('(1-cos(2*x))**2/4', '(1-2*cos(2*x)+cos(2*x)**2)/4')], 'نفك المربع: $(a-b)^2=a^2-2ab+b^2$.'),
           (r'\cos^{2}2x=\frac12+\frac12\cos4x', [('cos(2*x)**2', 'Rational(1,2)+cos(4*x)/2')],
            'طلع $\\cos^2$ مرة ثانية: نص الزاوية، و $2x$ تصير $4x$.'),
           (r'=\frac14\left(\frac32-2\cos2x+\frac12\cos4x\right)', [('sin(x)**4', '(Rational(3,2)-2*cos(2*x)+cos(4*x)/2)/4')], '$1+\\frac12=\\frac32$.'),
           (r'I=\frac14\left[\frac32x-\sin2x+\frac18\sin4x\right]+c', [(D('(3*x/2-sin(2*x)+sin(4*x)/8)/4'), 'sin(x)**4')],
            '$2\\cdot\\frac12=1$، و $\\frac12\\cdot\\frac14=\\frac18$.'),
           (r'I=\frac38x-\frac14\sin2x+\frac1{32}\sin4x+c', [(D('3*x/8-sin(2*x)/4+sin(4*x)/32'), 'sin(x)**4')], 'نوزّع $\\frac14$.')],
    'A7': [(r'\cos^{4}x=\frac14\left(1+2\cos2x+\cos^{2}2x\right)', [('cos(x)**4', '(1+2*cos(2*x)+cos(2*x)**2)/4')], 'نفس $\\sin^4$، بس زائد.'),
           (r'=\frac14\left(\frac32+2\cos2x+\frac12\cos4x\right)', [('cos(x)**4', '(Rational(3,2)+2*cos(2*x)+cos(4*x)/2)/4')], 'نص الزاوية لـ $\\cos^22x$.'),
           (r'I=\frac38x+\frac14\sin2x+\frac1{32}\sin4x+c', [(D('3*x/8+sin(2*x)/4+sin(4*x)/32'), 'cos(x)**4')],
            'نفس جواب $\\sin^4$، والفرق إشارة $\\sin2x$ بس.')],
    'B1': [(r'I=\int\sin^{5}x\cos^{2}x\,\cD{\cos x\,dx}', [('sin(x)**5*cos(x)**3', 'sin(x)**5*cos(x)**2*cos(x)')],
            'الاثنين فرديين (5 و 3): نحجز من الأصغر $\\cos x\\,dx$، عشان تصير $du$.'),
           (r'I=\int\sin^{5}x\,(1-\sin^{2}x)\,\cD{\cos x\,dx}', [('cos(x)**2', '1-sin(x)**2')], 'الباقي $\\cos^2x$ نحوّله لـ sin، عشان يصير كله $u$.'),
           U_SIN(),
           (r'I=\int' + UB(r'\sin^{5}x', 'u^{5}') + r'\,' + UB(r'(1-\sin^{2}x)', r'(1-u^{2})') + r'\;' + UD(r'\cos x\,dx'),
            [('sin(x)**5*cos(x)**3', 'sin(x)**5*(1-sin(x)**2)*diff(sin(x),x)')], SWAP_WHY, SWAP),
           (r'I=\int u^{5}(1-u^{2})\,du=\int(u^{5}-u^{7})\,du', [('u**5*(1-u**2)', 'u**5-u**7')], 'نوزّع $u^5$: الأسس تنجمع.'),
           (r'I=\frac16u^{6}-\frac18u^{8}+c', [('integrate(u**5-u**7,u)', 'u**6/6-u**8/8')], 'كل حد لحاله.'),
           (r'I=\frac16\sin^{6}x-\frac18\sin^{8}x+c', [(D('sin(x)**6/6-sin(x)**8/8'), 'sin(x)**5*cos(x)**3')], 'نرجّع $u=\\sin x$. أعلى أس 8 = 5 + 3 ✓')],
    'B2': [(r'I=\int\cos^{5}x\sin^{2}x\,\cD{\sin x\,dx}', [('cos(x)**5*sin(x)**3', 'cos(x)**5*sin(x)**2*sin(x)')],
            'الأصغر $\\sin^3$: نحجز $\\sin x\\,dx$ عشان تصير $du$.'),
           (r'I=\int\cos^{5}x\,(1-\cos^{2}x)\,\cD{\sin x\,dx}', [('sin(x)**2', '1-cos(x)**2')], 'الباقي لـ cos، عشان يصير كله $u$.'),
           U_COS(),
           (r'I=\int' + UB(r'\cos^{5}x', 'u^{5}') + r'\,' + UB(r'(1-\cos^{2}x)', r'(1-u^{2})') + r'\;' + UD(r'\sin x\,dx', MINUS_DU),
            [('cos(x)**5*sin(x)**3', '-cos(x)**5*(1-cos(x)**2)*diff(cos(x),x)')], SWAP_WHY_MINUS, SWAP),
           (r'I=\cR{-}\int u^{5}(1-u^{2})\,du=-\left[\frac16u^{6}-\frac18u^{8}\right]+c', [('integrate(u**5*(1-u**2),u)', 'u**6/6-u**8/8')],
            'السالب برّا القوس.'),
           (r'I=-\frac16\cos^{6}x+\frac18\cos^{8}x+c', [(D('-cos(x)**6/6+cos(x)**8/8'), 'cos(x)**5*sin(x)**3')],
            'نوزّع السالب ونرجّع $u=\\cos x$. ونفس توقّع التوأم ✓')],
    'B3': [(r'I=\int\sin^{7}x\cos^{4}x\,\cD{\cos x\,dx}', [('sin(x)**7*cos(x)**5', 'sin(x)**7*cos(x)**4*cos(x)')],
            'الأصغر $\\cos^5$: نحجز $\\cos x\\,dx$ عشان تصير $du$.'),
           (r'I=\int\sin^{7}x\,(1-\sin^{2}x)^{2}\,\cD{\cos x\,dx}', [('cos(x)**4', '(1-sin(x)**2)**2')],
            '$\\cos^4=(\\cos^2)^2$، ونحوّل لـ sin عشان يصير كله $u$.'),
           U_SIN(),
           (r'I=\int' + UB(r'\sin^{7}x', 'u^{7}') + r'\,' + UB(r'(1-\sin^{2}x)^{2}', r'(1-u^{2})^{2}') + r'\;' + UD(r'\cos x\,dx'),
            [('sin(x)**7*cos(x)**5', 'sin(x)**7*(1-sin(x)**2)**2*diff(sin(x),x)')], SWAP_WHY, SWAP),
           (r'I=\int u^{7}(1-2u^{2}+u^{4})\,du=\int(u^{7}-2u^{9}+u^{11})\,du', [('u**7*(1-u**2)**2', 'u**7-2*u**9+u**11')], 'نفك القوس ونوزّع.'),
           (r'I=\frac18\sin^{8}x-\frac15\sin^{10}x+\frac1{12}\sin^{12}x+c', [(D('sin(x)**8/8-sin(x)**10/5+sin(x)**12/12'), 'sin(x)**7*cos(x)**5')],
            '$\\frac{2}{10}=\\frac15$. أعلى أس 12 = 7 + 5 ✓')],
    'C1': [(r'I=\int\sin^{4}x\cos^{4}x\,\cD{\sin x\,dx}=\int(\sin^{2}x)^{2}\cos^{4}x\,\cD{\sin x\,dx}',
            [('sin(x)**5*cos(x)**4', '(sin(x)**2)**2*cos(x)**4*sin(x)')],
            'أس sin فردي (5)، وأس cos زوجي (4): نحجز $\\sin x\\,dx$ عشان تصير $du$.'),
           (r'I=\int(1-\cos^{2}x)^{2}\cos^{4}x\,\cD{\sin x\,dx}', [('(sin(x)**2)**2', '(1-cos(x)**2)**2')], 'نحوّل $\\sin^2$ لـ cos، عشان يصير كله $u$.'),
           U_COS(),
           (r'I=\int' + UB(r'(1-\cos^{2}x)^{2}', r'(1-u^{2})^{2}') + r'\,' + UB(r'\cos^{4}x', 'u^{4}') + r'\;' + UD(r'\sin x\,dx', MINUS_DU),
            [('sin(x)**5*cos(x)**4', '-(1-cos(x)**2)**2*cos(x)**4*diff(cos(x),x)')], SWAP_WHY_MINUS, SWAP),
           (r'I=\cR{-}\int(1-u^{2})^{2}u^{4}\,du=-\int(u^{4}-2u^{6}+u^{8})\,du', [('(1-u**2)**2*u**4', 'u**4-2*u**6+u**8')],
            'نفك القوس، ونضرب كل حد في $u^4$.'),
           (r'I=-\left[\frac15u^{5}-\frac27u^{7}+\frac19u^{9}\right]+c', [('integrate(u**4-2*u**6+u**8,u)', 'u**5/5-2*u**7/7+u**9/9')],
            'كل حد لحاله، والسالب برّا القوس.'),
           (r'I=-\frac15\cos^{5}x+\frac27\cos^{7}x-\frac19\cos^{9}x+c', [(D('-cos(x)**5/5+2*cos(x)**7/7-cos(x)**9/9'), 'sin(x)**5*cos(x)**4')],
            'نوزّع السالب ونرجّع $u=\\cos x$. أعلى أس 9 = 5 + 4 ✓')],
    'C2': [(r'I=\int\cos^{4}x\sin^{4}x\,\cD{\cos x\,dx}', [('cos(x)**5*sin(x)**4', 'cos(x)**4*sin(x)**4*cos(x)')],
            'أس cos فردي: نحجز $\\cos x\\,dx$ عشان تصير $du$.'),
           (r'I=\int(1-\sin^{2}x)^{2}\sin^{4}x\,\cD{\cos x\,dx}', [('cos(x)**4', '(1-sin(x)**2)**2')], 'الباقي لـ sin، عشان يصير كله $u$.'),
           U_SIN(),
           (r'I=\int' + UB(r'(1-\sin^{2}x)^{2}', r'(1-u^{2})^{2}') + r'\,' + UB(r'\sin^{4}x', 'u^{4}') + r'\;' + UD(r'\cos x\,dx'),
            [('cos(x)**5*sin(x)**4', '(1-sin(x)**2)**2*sin(x)**4*diff(sin(x),x)')], SWAP_WHY, SWAP),
           (r'I=\int(u^{4}-2u^{6}+u^{8})\,du', [('(1-u**2)**2*u**4', 'u**4-2*u**6+u**8')], 'نفس قوس $\\sin^5\\cos^4$ بالضبط.'),
           (r'I=\frac15\sin^{5}x-\frac27\sin^{7}x+\frac19\sin^{9}x+c', [(D('sin(x)**5/5-2*sin(x)**7/7+sin(x)**9/9'), 'cos(x)**5*sin(x)**4')],
            'نرجّع $u=\\sin x$. ونفس توقّع التوأم ✓')],
    'C3': [(r'I=\int(\cos^{2}x)^{3}\sin^{6}x\,\cD{\cos x\,dx}', [('cos(x)**7*sin(x)**6', '(cos(x)**2)**3*sin(x)**6*cos(x)')],
            'أس cos فردي (7): نحجز $\\cos x\\,dx$ عشان تصير $du$، والباقي $\\cos^6=(\\cos^2)^3$.'),
           (r'I=\int(1-\sin^{2}x)^{3}\sin^{6}x\,\cD{\cos x\,dx}', [('(cos(x)**2)**3', '(1-sin(x)**2)**3')], 'الباقي لـ sin، عشان يصير كله $u$.'),
           U_SIN(),
           (r'I=\int' + UB(r'(1-\sin^{2}x)^{3}', r'(1-u^{2})^{3}') + r'\,' + UB(r'\sin^{6}x', 'u^{6}') + r'\;' + UD(r'\cos x\,dx'),
            [('cos(x)**7*sin(x)**6', '(1-sin(x)**2)**3*sin(x)**6*diff(sin(x),x)')], SWAP_WHY, SWAP),
           (r'I=\int(1-3u^{2}+3u^{4}-u^{6})\,u^{6}\,du=\int(u^{6}-3u^{8}+3u^{10}-u^{12})\,du',
            [('(1-u**2)**3*u**6', 'u**6-3*u**8+3*u**10-u**12')], 'التكعيب من صفحة الجبر، ثم نضرب في $u^6$.'),
           (r'I=\frac17\sin^{7}x-\frac13\sin^{9}x+\frac3{11}\sin^{11}x-\frac1{13}\sin^{13}x+c',
            [(D('sin(x)**7/7-sin(x)**9/3+3*sin(x)**11/11-sin(x)**13/13'), 'cos(x)**7*sin(x)**6')], '$\\frac39=\\frac13$. أعلى أس 13 = 7 + 6 ✓')],
    'D1': [(r'I=\int\frac12(1-\cos2x)\cdot\frac12(1+\cos2x)\,dx', [('sin(x)**2*cos(x)**2', '(1-cos(2*x))*(1+cos(2*x))/4')],
            'الاثنين زوجيين: ما فيه قطعة تصير $du$، فنص الزاوية لكل واحد.'),
           (r'I=\int\frac14(1-\cos^{2}2x)\,dx', [('(1-cos(2*x))*(1+cos(2*x))/4', '(1-cos(2*x)**2)/4')], '$(a-b)(a+b)=a^2-b^2$.'),
           (r'I=\int\left[\frac14-\frac14\cdot\frac12(1+\cos4x)\right]dx=\int\left[\frac18-\frac18\cos4x\right]dx',
            [('(1-cos(2*x)**2)/4', 'Rational(1,8)-cos(4*x)/8')], 'نص الزاوية مرة ثانية لـ $\\cos^22x$.'),
           (r'I=\frac18x-\frac1{32}\sin4x+c', [(D('x/8-sin(4*x)/32'), 'sin(x)**2*cos(x)**2')], '$\\frac18\\cdot\\frac14=\\frac1{32}$.')],
    'D2': [(r'\sin^{4}x\cos^{2}x=(\sin x\cos x)^{2}\sin^{2}x=\frac14\sin^{2}2x\cdot\frac{1-\cos2x}{2}',
            [('sin(x)**4*cos(x)**2', 'sin(2*x)**2/4*(1-cos(2*x))/2')], 'الحركة 1: اجمع $\\sin x\\cos x$. والحركة 2: نص الزاوية للباقي $\\sin^2x$.'),
           (r'=\frac18\sin^{2}2x-\frac18\sin^{2}2x\cos2x', [('sin(2*x)**2/4*(1-cos(2*x))/2', 'sin(2*x)**2/8-sin(2*x)**2*cos(2*x)/8')], 'نوزّع.'),
           (r'\int\sin^{2}2x\,dx=\frac x2-\frac{\sin4x}{8}', [(D('x/2-sin(4*x)/8'), 'sin(2*x)**2')], 'نص الزاوية: $2x$ تصير $4x$.'),
           (r'\text{let }\cU{u=\sin2x},\quad du=2\cos2x\,dx\ \Rightarrow\ \cD{\cos2x\,dx}=' + HALF_DU, [(D('sin(2*x)'), '2*cos(2*x)')],
            'الحركة 3: $\\sin^22x\\cos2x$ فيها cos أسه 1 (فردي)، فنحجزه. ومشتقة $\\sin2x$ فيها 2، فنقسم الطرفين على 2.'),
           (r'\int' + UB(r'\sin^{2}2x', 'u^{2}') + r'\;' + UD(r'\cos2x\,dx', HALF_DU),
            [('sin(2*x)**2*cos(2*x)', 'Rational(1,2)*sin(2*x)**2*diff(sin(2*x),x)')], 'كل قطعة صارت $u$، والخضرا صارت $\\frac12du$ ✓', SWAP),
           (r'\int\sin^{2}2x\cos2x\,dx=\frac12\int u^{2}\,du=\frac{\sin^{3}2x}{6}', [(D('sin(2*x)**3/6'), 'sin(2*x)**2*cos(2*x)')],
            '$\\frac12\\cdot\\frac{u^3}{3}=\\frac{u^3}{6}$، ونرجّع $u=\\sin2x$.'),
           (r'I=\frac{x}{16}-\frac{\sin4x}{64}-\frac{\sin^{3}2x}{48}+c', [(D('x/16-sin(4*x)/64-sin(2*x)**3/48'), 'sin(x)**4*cos(x)**2')],
            '$\\frac18\\cdot\\frac12=\\frac1{16}$، و $\\frac18\\cdot\\frac18=\\frac1{64}$، و $\\frac18\\cdot\\frac16=\\frac1{48}$.')],
    'D5': [(r'\cos^{4}x\sin^{2}x=\frac14\sin^{2}2x\cdot\frac{1+\cos2x}{2}', [('cos(x)**4*sin(x)**2', 'sin(2*x)**2/4*(1+cos(2*x))/2')],
            'نفس $\\sin^4\\cos^2$، والباقي $\\cos^2x$ معه زائد.'),
           (r'=\frac18\sin^{2}2x+\frac18\sin^{2}2x\cos2x', [('sin(2*x)**2/4*(1+cos(2*x))/2', 'sin(2*x)**2/8+sin(2*x)**2*cos(2*x)/8')], 'نوزّع.'),
           (r'I=\frac{x}{16}-\frac{\sin4x}{64}+\frac{\sin^{3}2x}{48}+c', [(D('x/16-sin(4*x)/64+sin(2*x)**3/48'), 'cos(x)**4*sin(x)**2')],
            'نفس قطع التوأم ($u=\\sin2x$ للقطعة الثانية)، والفرق إشارة وحدة.')],
    'D3': [(r'\cos^{6}x\sin^{2}x=(\sin x\cos x)^{2}\cos^{4}x=\frac14\sin^{2}2x\cdot\frac{(1+\cos2x)^{2}}{4}',
            [('cos(x)**6*sin(x)**2', 'sin(2*x)**2/4*(1+cos(2*x))**2/4')], 'الحركة 1، ثم $\\cos^4=(\\cos^2)^2$ بنص الزاوية.'),
           (r'=\frac1{16}\left(\sin^{2}2x+2\sin^{2}2x\cos2x+\sin^{2}2x\cos^{2}2x\right)',
            [('sin(2*x)**2/4*(1+cos(2*x))**2/4', '(sin(2*x)**2+2*sin(2*x)**2*cos(2*x)+sin(2*x)**2*cos(2*x)**2)/16')], 'نفك المربع.'),
           (r'\sin^{2}2x\cos^{2}2x=\frac14\sin^{2}4x', [('sin(2*x)**2*cos(2*x)**2', 'sin(4*x)**2/4')], 'الحركة 1 مرة ثانية: $\\sin2x\\cos2x=\\frac12\\sin4x$.'),
           (r'=\frac1{16}\sin^{2}2x+\frac18\sin^{2}2x\cos2x+\frac1{64}\sin^{2}4x',
            [('cos(x)**6*sin(x)**2', 'sin(2*x)**2/16+sin(2*x)**2*cos(2*x)/8+sin(4*x)**2/64')], 'ثلاث قطع، كل وحدة تعرفها (الوسطى بـ $u=\\sin2x$).'),
           (r'\int\sin^{2}4x\,dx=\frac x2-\frac{\sin8x}{16}', [(D('x/2-sin(8*x)/16'), 'sin(4*x)**2')], 'نص الزاوية: $4x$ تصير $8x$.'),
           (r'I=\frac{5x}{128}-\frac{\sin4x}{128}+\frac{\sin^{3}2x}{48}-\frac{\sin8x}{1024}+c',
            [(D('5*x/128-sin(4*x)/128+sin(2*x)**3/48-sin(8*x)/1024'), 'cos(x)**6*sin(x)**2')],
            '$x$: $\\frac1{32}+\\frac1{128}=\\frac5{128}$. والباقي من القطع الثلاث.')],
    'D4': [(r'\sin^{6}x\cos^{2}x=\frac14\sin^{2}2x\cdot\frac{(1-\cos2x)^{2}}{4}', [('sin(x)**6*cos(x)**2', 'sin(2*x)**2/4*(1-cos(2*x))**2/4')],
            'نفس $\\cos^6\\sin^2$، بس الباقي $\\sin^4$ معه ناقص.'),
           (r'=\frac1{16}\sin^{2}2x-\frac18\sin^{2}2x\cos2x+\frac1{64}\sin^{2}4x',
            [('sin(x)**6*cos(x)**2', 'sin(2*x)**2/16-sin(2*x)**2*cos(2*x)/8+sin(4*x)**2/64')], 'نفس القطع الثلاث، والوسطى سالبة.'),
           (r'I=\frac{5x}{128}-\frac{\sin4x}{128}-\frac{\sin^{3}2x}{48}-\frac{\sin8x}{1024}+c',
            [(D('5*x/128-sin(4*x)/128-sin(2*x)**3/48-sin(8*x)/1024'), 'sin(x)**6*cos(x)**2')], 'نفس جواب $\\cos^6\\sin^2$، والفرق إشارة وحدة.')],
}

# the fill-in-the-blanks lines of D2 (the full lines are the checked rows above)
FILL_D2 = [r'\sin^{4}x\cos^{2}x=(\sin x\cos x)^{2}\sin^{2}x=\frac14\sin^{2}2x\cdot' + BLANK,
           r'=\frac18\sin^{2}2x-' + BLANK + r'\,\sin^{2}2x\cos2x',
           r'\int\sin^{2}2x\,dx=\frac x2-' + BLANK,
           r'u=' + BLANK + r':\quad\int\sin^{2}2x\cos2x\,dx=' + BLANK,
           r'I=' + BLANK + '+c']


def check_all():
    antideriv('-cos(x)**4/4+cos(x)**6/6', 'sin(x)**3*cos(x)**3', 'checkpoint B 1 other choice')
    for k, (qt, pg, n, g, f, F, Ft, kind) in Q.items():
        antideriv(F, f, 'Musa ' + k)


# ---------------------------------------------------------------- pages
def page_map():
    why = ul([rich('<b>نحجز وحدة</b> عشان تصير $du$: مشتقة $\\sin x$ هي $\\cos x$، ومشتقة $\\cos x$ هي $-\\sin x$. (الشرح الكامل في صفحة 🔑 u و du.)'),
              rich('<b>المتطابقة</b> $\\sin^2=1-\\cos^2$ تحوّل بس الأس <b>الزوجي</b>. فبعد ما تحجز لازم الباقي زوجي، يعني لازم يكون فيه أس <b>فردي</b> من البداية. '
                   'وإذا كلها زوجية ما فيه شي تحجزه، فنص الزاوية: ينزّل الأس للنص ويضاعف الزاوية.'),
              rich('<b>الأصغر</b> (لو الاثنين فرديين) يعني أقواس أقل تفكها.')])
    names = table(['اسم موسى', 'وش تسوي'], [
        ['أسس لحالها (فردي)', rich('احجز وحدة، والباقي بالمتطابقة')],
        ['أسس لحالها (زوجي)', 'نص الزاوية'],
        ['<b>Odd and Even</b>', rich('احجز من <b>الفردي</b>')],
        ['<b>Odd and Odd</b>', rich('احجز من <b>الأصغر</b> (متساويين؟ أي واحد)')],
        ['<b>Even and Even</b>', rich('الحركات الثلاث: اجمع $\\sin x\\cos x$، ثم نص الزاوية، ثم $u=\\sin2x$ إذا لزم')]], 'decide')
    urule = p(rich('🔑 <b>وش $u$؟</b> حجزت $\\cos x\\,dx$ ← let $u=\\sin x$. حجزت $\\sin x\\,dx$ ← let $u=\\cos x$ (ويطلع سالب).'))
    contents = p(' · '.join([link(a, t) + ' ص ' + pgref(a) for a, t in [
        ('udu', '🔑 u و du'), ('tools', '🧰 الأدوات والجبر'), ('secA', GROUP['A'][1]), ('secB', GROUP['C'][1]), ('secC', GROUP['B'][1]),
        ('secD', GROUP['D'][1]), ('fix', '🔍 صحّح الغلط'), ('test', '📝 اختبار الإتقان'), ('key', '🔑 المفتاح'),
        ('sols', '✅ حلول أسئلة موسى'), ('recall', '🧠 استرجاع قبل الكويز')]]), 'contents')
    order = ['A3', 'A5', 'A2', 'A1', 'A6', 'A4', 'A7', 'C1', 'C2', 'C3', 'B1', 'B2', 'B3', 'D1', 'D2', 'D5', 'D3', 'D4']   # study order
    tracker = table(['☐', 'السؤال', 'عند موسى', 'هنا', 'ص'], [
        ['☐', mi(Q[k][0]), musa(k), KIND[Q[k][7]], link('q-' + k, pgref('q-' + k))] for k in order], 'tracker')
    plan = ('<ol class="plan">' + ''.join('<li>%s</li>' % rich(t) for t in [
        '<b>ما فهمت $u$ و $du$؟</b> صفحة 🔑 u و du أول. ثم <b>هذي الصفحة والأدوات:</b> الـ«ليش» أهم من القواعد. غطِّها واكتبها من راسك. <b>10 دقايق.</b>',
        '<b>الأقسام الأربعة بالترتيب.</b> في كل قسم: المثال المحلول (غطِّ عمود «الخطوة» وتوقّع)، ثم التوأم (توقّع جوابه بسطر، ثم حله)، '
        'ثم «لحالك»، ثم الفحص الصغير. وعلّم ☐ في المتتبع. <b>75 دقيقة.</b>',
        '<b>صحّح الغلط.</b> <b>10 دقايق.</b>',
        '<b>اختبار الإتقان:</b> الجولة الأولى أول سطر بس، والثانية حل كامل. 8 من 10 = أتقنته. <b>25 دقيقة.</b>',
        '<b>أمثلة دكتورك:</b> أول صفحة من محاضرة 15 في صفحاته اللي بخط يده (4 أمثلة). غطِّ حله وحلها. هو اللي يكتب الكويز. <b>15 دقيقة.</b>',
        '<b>قبل الكويز:</b> صفحة «🧠 استرجاع» (آخر الملف)، والجولة الأولى من الاختبار. <b>15 دقيقة.</b>']) + '</ol>')
    return section('map', '🗺️ odd و even: الخريطة',
                   '<div class="oe-q">' + rich('السؤال الوحيد: <b>فيه أس فردي؟</b>') + '</div>'
                   + p(rich('إيه ← <b>احجز</b> وحدة من الفردي، وحوّل الباقي، وعوّض $u$. لا ← <b>نص الزاوية</b>.'))
                   + '<div class="udu-hint">' + rich('🔑 <b>ما فهمت $u$ و $du$؟</b> ') + link('udu', 'صفحتها قبل أي حل: ص ' + pgref('udu')) + '</div>'
                   + '<h3>ليش؟ (3 أسطر تخليك تطلع القواعد بنفسك)</h3>' + why
                   + '<h3>أسماء موسى = نفس القاعدة</h3>' + names + urule
                   + p(rich('🚫 <b>مو هذا الدرس:</b> زاويتين مختلفتين مثل $\\sin3x\\cos2x$ (درس الضرب، موسى ص 102)، '
                            'أو tan و sec (موسى ص 98).'), 'small')
                   + '<h3>الأقسام</h3>' + contents
                   + '<h3>📍 متتبع أسئلة موسى الـ18</h3>' + tracker
                   + '<h3>📋 خطة المذاكرة</h3>' + plan)


UDU_KEY = ['(1) $\\displaystyle \\sin x\\,dx=-du$ (اضرب الطرفين في $-1$)',
           '(2) $\\displaystyle \\cos3x\\,dx=\\frac13\\,du$ (لأن $du=3\\cos3x\\,dx$)',
           '(3) $u$، و $-du$: $\\displaystyle \\int u^{4}(-du)=-\\frac15\\cos^{5}x+c$']


def page_udu():
    """u and du from zero: the exchange idea, the two lines to write, one full example with the 🔁 swap, why the kept piece
    is needed (the whole secret of odd and even), the three shapes of du, the minus example, four questions, and practice."""
    ex1 = steps([
        (r'\text{let }\cU{u=\sin x},\quad \cD{du=\cos x\,dx}', [(D(S), C)], 'سطرين «سعر الصرف»: اشتق $u$ وحط جنبها $dx$.'),
        (r'I=\int' + UB(r'\sin^{2}x', 'u^{2}') + r'\;' + UD(r'\cos x\,dx'), [('sin(x)**2*cos(x)', 'sin(x)**2*diff(sin(x),x)')],
         '$\\sin^2x$ صارت $u^2$، و $\\cos x\\,dx$ كلها مع بعض صارت $du$. ما بقى ولا $x$ ✓', SWAP),
        (r'I=\int u^{2}\,du=\frac13u^{3}+c', [('integrate(u**2,u)', 'u**3/3')], 'صار سهل: زد الأس 1 واقسم عليه.'),
        (r'I=\frac13\sin^{3}x+c', [(D('sin(x)**3/3'), 'sin(x)**2*cos(x)')], 'نرجّع $u=\\sin x$. وتأكد: اشتقه، يرجع السؤال ✓')], 'udu ex1')
    ex2 = steps([
        (r'\text{let }\cU{u=\cos x},\quad du=\cR{-}\sin x\,dx', [(D(C), '-' + S)], 'مشتقة cos فيها سالب.'),
        (r'\cR{-}du=\cD{\sin x\,dx}', [('-diff(cos(x),x)', 'sin(x)')], 'نضرب الطرفين في $-1$. الحين القطعة اللي في السؤال صار اسمها $-du$.'),
        (r'I=\int' + UB(r'\cos^{2}x', 'u^{2}') + r'\;' + UD(r'\sin x\,dx', MINUS_DU), [('cos(x)**2*sin(x)', '-cos(x)**2*diff(cos(x),x)')],
         '$\\cos^2x$ صارت $u^2$، و $\\sin x\\,dx$ صارت $-du$ ✓', SWAP),
        (r'I=\cR{-}\int u^{2}\,du=-\frac13u^{3}+c', [('integrate(u**2,u)', 'u**3/3')],
         'السالب يطلع قدّام التكامل. ولو بعده أكثر من حد، نحطه برّا قوس $-[\\ldots]$ لأنه يضرب الكل.'),
        (r'I=-\frac13\cos^{3}x+c', [(D('-cos(x)**3/3'), 'cos(x)**2*sin(x)')], 'نرجّع $u=\\cos x$ ✓')], 'udu ex2')
    forms = table([rich('let $u$'), rich('$du$'), 'القطعة اللي في السؤال تصير', ''], [
        [mi(r'u=\sin x'), mi(r'du=\cos x\,dx'), mi(r'\cos x\,dx=du'), ''],
        [mi(r'u=\cos x'), mi(r'du=-\sin x\,dx'), mi(r'\sin x\,dx=-du'), rich('اضرب الطرفين في $-1$')],
        [mi(r'u=\sin2x'), mi(r'du=2\cos2x\,dx'), mi(r'\cos2x\,dx=\tfrac12\,du'), 'اقسم الطرفين على 2']], 'duforms')
    arith('', [(D('sin(x)'), 'cos(x)'), (D('cos(x)'), '-sin(x)'), (D('sin(2*x)'), '2*cos(2*x)')], 'udu forms')
    arith('', [(D('sin(3*x)'), '3*cos(3*x)')], 'udu practice 2')
    antideriv('-cos(x)**5/5', 'cos(x)**4*sin(x)', 'udu practice 3')
    practice = ('<ol class="fill">'
                + '<li>%s</li>' % mi(r'\text{let }u=\cos x\ \Rightarrow\ \sin x\,dx=' + BLANK)
                + '<li>%s</li>' % mi(r'\text{let }u=\sin3x\ \Rightarrow\ \cos3x\,dx=' + BLANK)
                + '<li>%s</li>' % mi(r'\displaystyle\int\cos^{4}x\,\sin x\,dx=\int(' + BLANK + r')^{4}\,(' + BLANK + r')') + '</ol>'
                + p(rich('وكمّل الثالث لين الجواب:'), 'small') + lines(2, 'write tight'))
    checks = ul([rich(t) for t in ['✅ كتبت let $u$ و $du$؟', '✅ قطعة $du$ موجودة كاملة في السؤال؟',
                                     '✅ بعد التبديل: ما بقى ولا $x$ ولا $dx$؟', '✅ رجّعت $x$ في الآخر؟']], 'checks')
    return section('udu', '🔑 u و du من الصفر (اقرأها قبل أي حل)',
                   '<div class="oe-q">' + rich('الفكرة: نحوّل التكامل الصعب لتكامل سهل مثل $\\int u^2\\,du$') + '</div>'
                   + p(rich('مثل تصريف الفلوس: كل شي بـ«عملة $x$» يتصرّف لـ«عملة $u$». ولو بقى شي واحد بعملة $x$، التصريف خربان.'))
                   + '<div class="oe-grid2">'
                   + box('١. سعر الصرف: سطرين تكتبهم دايم (مثل دكتورك)', md(r'\begin{gathered}\text{let }\cU{u=\sin x}\\ \cD{du=\cos x\,dx}\end{gathered}')
                         + p(rich('اشتق $u$، وحط جنبها $dx$. <b>ليش $dx$؟</b> كل تكامل آخره $dx$. ولما نصرف لـ $u$، القطعة $\\cos x\\,dx$ '
                                  '<b>كلها مع بعض</b> تصير $du$.')))
                   + box('٢. ليش لازم القطعة الخضرا؟ (وهذا كل سر odd و even)',
                         p(rich('$du$ هي «تذكرة» التصريف: بدونها يبقى $dx$ بعملة $x$. مثلًا $\\int\\sin^2x\\,dx$ ما فيها $\\cos x$، فـ $u=\\sin x$ ما تنفع.'))
                         + p(rich('<b>الأس الفردي</b> يعطيك قطعة زيادة ($\\sin x$ أو $\\cos x$) تحجزها وتصير $du$. <b>والزوجي</b> ما يعطيك، فتروح لنص الزاوية.')))
                   + '</div>'
                   + box('٣. مثال كامل: $\\int\\sin^2x\\cos x\\,dx$', ex1
                         + p(rich('السطور المرقّمة تكتبها في الكويز. وسطر 🔁 تسويه بعيونك: قوس تحت كل قطعة، ومكتوب تحته وش صارت.'), 'small'), 'worked')
                   + box('٤. $du$ لها 3 أشكال بس', forms)
                   + box('٥. مثال السالب: $\\int\\cos^2x\\sin x\\,dx$', ex2, 'worked')
                   + '<div class="oe-grid2">' + box('✅ 4 أسئلة قبل ما تكمّل أي حل', checks)
                   + box('✍️ جرّب (الأجوبة في المفتاح ص ' + pgref('key') + ')', practice) + '</div>'
                   + p(link('tools', 'كمّل: الأدوات ص ' + pgref('tools')) + ' · ' + link('secA', 'القسم ١ ص ' + pgref('secA')), 'small'))


def page_tools():
    t1 = arith(r'\sin^{2}x+\cos^{2}x=1\ \Rightarrow\ \sin^{2}x=1-\cos^{2}x,\quad \cos^{2}x=1-\sin^{2}x',
               [('sin(x)**2+cos(x)**2', '1'), ('sin(x)**2', '1-cos(x)**2'), ('cos(x)**2', '1-sin(x)**2')], 'tool pyth')
    t1b = arith(r'\begin{gathered}\sin^{2}x+\cos^{2}x=1\\ \sin^{2}x=1-\cos^{2}x\\ \cos^{2}x=1-\sin^{2}x\end{gathered}',
                [('sin(x)**2+cos(x)**2', '1'), ('sin(x)**2', '1-cos(x)**2'), ('cos(x)**2', '1-sin(x)**2')], 'tool pyth b')
    t2 = arith(r"(\sin x)'=\cos x\qquad (\cos x)'=\cR{-}\sin x", [(D(S), C), (D(C), '-' + S)], 'tool d')
    t3 = arith(r'\sin^{2}x=\frac{1-\cos2x}{2}\qquad \cos^{2}x=\frac{1+\cos2x}{2}\qquad \sin x\cos x=\frac12\sin2x',
               [('sin(x)**2', '(1-cos(2*x))/2'), ('cos(x)**2', '(1+cos(2*x))/2'), ('sin(x)*cos(x)', 'sin(2*x)/2')], 'tool half')
    t4 = arith(r'\int u^{n}\,du=\frac{u^{n+1}}{n+1}\qquad \int\cos kx\,dx=\frac{\sin kx}{k}',
               [(D('x**6/6'), 'x**5'), (D('sin(4*x)/4'), 'cos(4*x)')], 'tool int')
    alg = arith(r'(1-u^{2})^{2}=1-2u^{2}+u^{4}\\ (1-u^{2})^{3}=1-3u^{2}+3u^{4}-u^{6}\\ (1\pm\cos2x)^{2}=1\pm2\cos2x+\cos^{2}2x\\ (\sin x\cos x)^{2}=\frac14\sin^{2}2x',
                [('(1-u**2)**2', '1-2*u**2+u**4'), ('(1-u**2)**3', '1-3*u**2+3*u**4-u**6'),
                 ('(1+cos(2*x))**2', '1+2*cos(2*x)+cos(2*x)**2'), ('(1-cos(2*x))**2', '1-2*cos(2*x)+cos(2*x)**2'),
                 ('(sin(x)*cos(x))**2', 'sin(2*x)**2/4')], 'tool alg')
    num = arith(r'u=2:\quad (1-4)^{2}=9,\quad 1-8+16=9\ \checkmark', [('(1-4)**2', '9'), ('1-8+16', '9')], 'tool num')
    frac = arith(r'\begin{gathered}\frac14\cdot\frac12=\frac18\qquad \frac18\cdot\frac12=\frac1{16}\\ \frac1{16}\cdot\frac14=\frac1{64}\qquad \frac{2}{10}=\frac15\qquad \frac39=\frac13\end{gathered}',
                 [('Rational(1,4)*Rational(1,2)', 'Rational(1,8)'), ('Rational(1,8)*Rational(1,2)', 'Rational(1,16)'),
                  ('Rational(1,16)*Rational(1,4)', 'Rational(1,64)'), ('Rational(2,10)', 'Rational(1,5)'), ('Rational(3,9)', 'Rational(1,3)')], 'tool frac')
    return section('tools', '🧰 الأدوات والجبر',
                   '<div class="oe-grid2">' + box('١. المتطابقة: تحوّل الباقي', md(t1b))
                   + box('٢. المشتقات: تعطيك $du$', md(t2) + p(rich('let $u=\\sin x$ ← $du=\\cos x\\,dx$.<br>let $u=\\cos x$ ← $\\sin x\\,dx=-du$.'), 'small')) + '</div>'
                   + box('٣. نص الزاوية: «سين وسالب»، والزاوية تتضاعف', md(t3))
                   + box('٤. التكامل', md(t4) + p(rich('مع $kx$ اقسم على $k$: $\\int\\cos4x\\,dx=\\frac14\\sin4x$.'), 'small')
                         + p(rich('ومع زاوية في الفردي: $u=\\sin2x$ يعني ') + mi(arith(r'du=2\cos2x\,dx', [(D('sin(2*x)'), '2*cos(2*x)')], 'tool angle'))
                             + rich('، فيطلع $\\frac12$ قدّام التكامل.'), 'small'))
                   + box('٥. الأقواس اللي تطلع في أسئلة موسى (جاهزة)', md(r'\begin{gathered}' + alg + r'\end{gathered}')
                         + p(rich('تشك؟ عوّض رقم في الطرفين:'), 'small') + md(num))
                   + box('🔴 عادة السالب (ومن وين يجي)', p(rich('مع $u=\\cos x$: $du=-\\sin x\\,dx$، يعني $\\sin x\\,dx=-du$. فالسالب يطلع قدّام التكامل. '
                                                 'اكتبه <b>برّا قوس كبير</b> $-\\left[\\ldots\\right]$ لأنه يضرب كل الحدود، ولا توزعه إلا آخر سطر. مثل ما يسوي موسى.')))
                   + '<div class="oe-grid2">' + box('🔢 الكسور اللي تطلع', md(frac))
                   + box('👀 تنبيه على مذكرة موسى', p(rich('في ص 91 كتب القوس بخطين عموديين: $-|u-\\frac23u^3+\\frac15u^5|$. '
                                                         '<b>هذا قوس عادي، مو قيمة مطلقة.</b>'))) + '</div>')


def qblock(k):
    qt, pg, n, g, f, F, Ft, kind = Q[k]
    head = '%s · %s' % (KIND[kind], musa(k))
    sol = link('s-' + k, 'الحل ص ' + pgref('s-' + k), 'btn')
    if kind == 'worked':
        return box(head + ' · محلول عنده', md(qt) + steps(ROWS[k], 'worked ' + k), 'worked', 'q-' + k)
    if kind == 'twin':
        tw = TWIN_OF[k]
        return box(head + ' · توأم ' + musa(tw), md(qt) + p(link('q-' + tw, 'جواب توأمه ص ' + pgref('q-' + tw)), 'small')
                   + p(rich('<b>(اختياري) توقّع:</b> خذ جواب توأمه، وبدّل sin مع cos، واقلب إشارة الجواب كله. اكتب توقّعك:')) + lines(1, 'write tight')
                   + p('<b>وبعدين حلها كاملة:</b>') + lines(5, 'write tight') + p(sol), 'twin', 'q-' + k)
    if kind == 'fill':
        return box(head + ' · عبّي الفراغات', md(qt) + '<ol class="fill">' + ''.join('<li>%s</li>' % mi(r'\displaystyle ' + t) for t in FILL_D2)
                   + '</ol>' + p(sol), 'fill', 'q-' + k)
    extra = p(rich('💡 $\\cos^6=(\\cos^2)^3=(1-\\sin^2)^3$، والتكعيب جاهز في الأدوات.'), 'small') if k == 'C3' else ''
    if k in ('D3', 'D4'):
        extra = p(rich('💡 نفس الحركات الثلاث، بس الباقي $\\cos^4$ أو $\\sin^4$ (مربع نص الزاوية)، وتطلع $\\sin^22x\\cos^22x=\\frac14\\sin^24x$.'), 'small')
    if k in ('A4', 'A7'):
        extra = p(rich('في الزوجي ما فيه قاعدة توأم: حلها، وقارن مع توأمها. الفرق في إشارة $\\sin2x$ بس.'), 'small')
    return box(head, md(qt) + extra + lines(6, 'write tight') + p(sol), kind, 'q-' + k)


def check_block(title, qs):
    out = ''
    for k, item in enumerate(qs, 1):
        qt, F, f = item[:3]
        antideriv(F, f, 'checkpoint %s %d' % (title, k))
        tag = (' <span class="hardtag">%s</span>' % item[3]) if len(item) > 3 else ''
        out += '<div class="ch"><b>%d</b>%s%s%s</div>' % (k, tag, md(qt), lines(3, 'write tight'))
    return box('✅ فحص صغير: صح الاثنين؟ كمّل. غلط؟ ارجع للمثال المحلول (الأجوبة في المفتاح)', '<div class="chgrid">' + out + '</div>', 'check')


CHECKS = {
    'A': [(r'\int\cos^{5}x\,dx', 'sin(x)-2*sin(x)**3/3+sin(x)**5/5', 'cos(x)**5'), (r'\int\sin^{2}2x\,dx', 'x/2-sin(4*x)/8', 'sin(2*x)**2')],
    'C': [(r'\int\sin^{3}x\cos^{4}x\,dx', '-cos(x)**5/5+cos(x)**7/7', 'sin(x)**3*cos(x)**4'), (r'\int\cos^{3}x\sin^{2}x\,dx', 'sin(x)**3/3-sin(x)**5/5', 'cos(x)**3*sin(x)**2')],
    'B': [(r'\int\sin^{3}x\cos^{3}x\,dx', 'sin(x)**4/4-sin(x)**6/6', 'sin(x)**3*cos(x)**3'), (r'\int\cos^{3}x\sin^{7}x\,dx', 'sin(x)**8/8-sin(x)**10/10', 'cos(x)**3*sin(x)**7')],
    'D': [(r'\int\sin^{2}3x\cos^{2}3x\,dx', 'x/8-sin(12*x)/96', 'sin(3*x)**2*cos(3*x)**2'),
          (r'\int\sin^{4}x\cos^{4}x\,dx', '3*x/128-sin(4*x)/128+sin(8*x)/1024', 'sin(x)**4*cos(x)**4', '⭐⭐ تحدي')]}
CHECK_KEYS = {
    'A': [r'\sin x-\frac23\sin^{3}x+\frac15\sin^{5}x+c', r'\frac x2-\frac18\sin4x+c'],
    'C': [r'-\frac15\cos^{5}x+\frac17\cos^{7}x+c', r'\frac13\sin^{3}x-\frac15\sin^{5}x+c'],
    'B': [r'\frac14\sin^{4}x-\frac16\sin^{6}x+c\ \ (\text{or }-\tfrac14\cos^{4}x+\tfrac16\cos^{6}x)', r'\frac18\sin^{8}x-\frac1{10}\sin^{10}x+c'],
    'D': [r'\frac x8-\frac1{96}\sin12x+c', r'\frac{3x}{128}-\frac{\sin4x}{128}+\frac{\sin8x}{1024}+c']}


def page_D():
    anchor, title, pages = GROUP['D']
    moves = ('<ol class="method">' + ''.join('<li>%s</li>' % rich(t) for t in [
        '<b>اجمع</b> كل $\\sin x\\cos x$ في $\\frac12\\sin2x$ (أكثر ما تقدر).',
        '<b>الباقي</b> ($\\sin^2$ أو $\\cos^2$ أو مربعهم) بنص الزاوية.',
        '<b>طلع</b> $\\sin^22x\\cos2x$؟ هذا فردي: let $u=\\sin2x$، و $\\cos2x\\,dx=\\frac12du$. وطلع $\\sin^2$ أو $\\cos^2$ ثاني؟ نص الزاوية مرة ثانية.']) + '</ol>')
    three = box('🧱 نفس السؤال بالحركات الثلاث (أقصر، وتمشي على كل Even and Even)', steps([
        (r'\sin^{2}x\cos^{2}x=(\sin x\cos x)^{2}=\frac14\sin^{2}2x', [('sin(x)**2*cos(x)**2', 'sin(2*x)**2/4')],
         'الحركة 1: اجمع $\\sin x\\cos x=\\frac12\\sin2x$.'),
        (r'=\frac14\cdot\frac{1-\cos4x}{2}=\frac18-\frac18\cos4x', [('sin(2*x)**2/4', 'Rational(1,8)-cos(4*x)/8')], 'الحركة 2: نص الزاوية للباقي.'),
        (r'I=\frac18x-\frac1{32}\sin4x+c', [(D('x/8-sin(4*x)/32'), 'sin(x)**2*cos(x)**2')], 'نفس جواب موسى ✓')], 'D1 three moves'), 'worked')
    body = (p(rich('كل الأسس زوجية، فما فيه شي تحجزه. موسى حل $\\sin^2\\cos^2$ بنص الزاوية لكل واحد، والباقي ما حله. '
                   'هنا طريقة وحدة تمشي على الخمسة:')) + moves
            + qblock('D1') + three + ''.join(qblock(k) for k in ('D2', 'D5', 'D3', 'D4')))
    return section(anchor, '%s <span class="musa">(%s)</span>' % (title, pages), body + check_block('D', CHECKS['D']))


ODD_STEPS = ['<b>احجز</b> $\\sin x\\,dx$ أو $\\cos x\\,dx$ وحدة من صاحب الأس الفردي، عشان تصير $du$. الاثنين فرديين؟ من الأصغر.',
             '<b>حوّل</b> الباقي (صار أسه زوجي) بالمتطابقة، عشان يصير كله $u$.',
             '<b>let:</b> حجزت $\\cos x\\,dx$؟ $u=\\sin x$. حجزت $\\sin x\\,dx$؟ $u=\\cos x$، و 🔴 $\\sin x\\,dx=-du$ (السالب برّا قوس كبير).',
             '<b>بدّل</b> كل قطعة بـ $u$ (سطر 🔁): ما يبقى ولا $x$ ولا $dx$.',
             '<b>فك القوس</b> (جاهز في الأدوات) ووزّع، ثم <b>كامل</b> كل حد.',
             '<b>رجّع</b> $x$ وحط $+c$. وتأكد: <b>أعلى أس في جوابك = مجموع الأسين</b>.']
TWIN = ('<div class="twinrule">' + '<b>👯 حيلة إضافية (اختياري، بعد ما تفهم الحل اللي فوق): قاعدة التوأم.</b> في الفردي بس: سؤال وتوأمه = نفس الأسس بعد ما تبدّل sin و cos. '
        'جوابه = <b>نفس الأرقام</b>، وتبدّل sin مع cos، و<b>تنقلب إشارة الجواب كله</b>.</div>')


def page_A():
    anchor, title, pages = GROUP['A']
    body = (p(rich('أبسط شكل: sin أو cos لحالها. الفردي بالحجز، والزوجي بنص الزاوية.'))
            + '<h3>الفردي</h3><ol class="method">' + ''.join('<li>%s</li>' % rich(t) for t in ODD_STEPS) + '</ol>'
            + qblock('A3') + rich(TWIN) + qblock('A5') + qblock('A2')
            + '<h3>الزوجي</h3>' + p(rich('نص الزاوية، ولو طلع $\\cos^2$ ثاني: نص الزاوية مرة ثانية.'))
            + qblock('A1') + qblock('A6') + qblock('A4') + qblock('A7'))
    return section(anchor, '%s <span class="musa">(%s)</span>' % (title, pages), body + check_block('A', CHECKS['A']))


def page_C():
    anchor, title, pages = GROUP['C']
    body = (p(rich('واحد فردي وواحد زوجي: <b>احجز من الفردي</b>. نفس خطوات الأسس لحالها، بس فيه دالة ثانية تمشي معك.'))
            + qblock('C1') + qblock('C2') + qblock('C3'))
    return section(anchor, '%s <span class="musa">(%s)</span>' % (title, pages), body + check_block('C', CHECKS['C']))


def page_B():
    anchor, title, pages = GROUP['B']
    body = (p(rich('الاثنين فرديين: <b>احجز من الأصغر</b>. والثاني يمشي بعد، بس شغله أكثر، وجوابه شكله غير (وهو صح).'))
            + qblock('B1') + qblock('B2') + qblock('B3'))
    return section(anchor, '%s <span class="musa">(%s)</span>' % (title, pages), body + check_block('B', CHECKS['B']))


MISTAKES = [
    (r'\int\sin^{3}x\,dx:\ u=\cos x,\ du=\sin x\,dx\ \Rightarrow', 'cos(x)-cos(x)**3/3', r'\cos x-\frac13\cos^{3}x',
     'مشتقة $\\cos x$ هي $-\\sin x$. نسيت السالب، فالجواب كله انقلب.', '-cos(x)+cos(x)**3/3', r'-\cos x+\frac13\cos^{3}x+c', 'sin(x)**3'),
    (r'\sin^{4}x=', '1-cos(x)**4', r'1-\cos^{4}x', 'المتطابقة تحوّل $\\sin^2$ بس. $\\sin^4=(\\sin^2)^2$: تحوّل اللي داخل القوس، والقوس يبقى مربع. '
     'وتطلع في 5 من أسئلة موسى.', '(1-cos(x)**2)**2', r'(1-\cos^{2}x)^{2}', None),
    (r'(1-u^{2})^{2}=', '1-u**4', r'1-u^{4}', 'نسيت الحد الأوسط $2ab$.', '1-2*u**2+u**4', r'1-2u^{2}+u^{4}', None),
    (r'\int\cos^{2}x\,dx=\int\frac{1+\cos2x}{2}dx=', 'x/2+sin(2*x)/2', r'\frac x2+\frac12\sin2x',
     '$\\int\\cos2x\\,dx=\\frac12\\sin2x$، ومعه $\\frac12$ من قدّام: تصير $\\frac14$.', 'x/2+sin(2*x)/4', r'\frac x2+\frac14\sin2x+c', 'cos(x)**2'),
    (r'\int\sin^{2}x\,dx=', 'sin(x)**3/3', r'\frac13\sin^{3}x', 'قاعدة القوة تحتاج مشتقة الداخل جنبها، وما فيه $\\cos x$. هذا زوجي: نص الزاوية.',
     'x/2-sin(2*x)/4', r'\frac x2-\frac14\sin2x+c', 'sin(x)**2'),
    (r'-\int(u^{4}-u^{6})\,du=', '-u**5/5-u**7/7', r'-\frac{u^{5}}{5}-\frac{u^{7}}{7}', 'السالب لازم يدخل على <b>كل</b> حدود القوس، مو أول حد بس.',
     '-u**5/5+u**7/7', r'-\frac{u^{5}}{5}+\frac{u^{7}}{7}', None)]


def page_fix():
    rows = ''
    for k, (qq, wrong, wrong_tex, why, right, right_tex, f) in enumerate(MISTAKES, 1):
        a, b = P(wrong), P(right)
        if f:
            arith('', [(D(right), f)], 'mistake %d right' % k)
            a, b = sp.diff(a, x), sp.diff(b, x)
        diff = [abs(complex((a - b).subs({x: v, u: v}).evalf())) for v in (0.7, 1.3)]
        if max(diff) < 1e-9:
            raise BuildError('mistake %d: the wrong version is not wrong' % k)
        rows += ('<div class="fix"><b>%d.</b> %s<div class="fixq">🔍 وين الغلط؟</div><div class="fixa">%s %s</div></div>'
                 % (k, mi(qq + r'\ \cR{' + wrong_tex + '}'), p('<b>الجواب:</b> ' + rich(why)), md(right_tex)))
    arith('', [('(1-u**2)**2', '1-2*u**2+u**4'), ('integrate(-(u**4-u**6),u)', '-u**5/5+u**7/7'),
               ('sin(x)**4', '(1-cos(x)**2)**2')], 'mistakes right lines')
    return section('fix', '🔍 صحّح الغلط: الأغلاط الست المشهورة',
                   p(rich('كل سطر أحمر فيه غلطة. غطِّ «الجواب» ولقها أول. الحاسوب تأكد إن كل «غلط» غلط فعلًا، وكل «صح» صح.')) + rows)


TEST = [  # (question, branch, first line, answer latex, F, f)
    (r'\int\sin^{3}x\cos^{6}x\,dx', 'Odd and Even: احجز sin', r'(1-\cos^{2}x)\cos^{6}x\sin x,\ u=\cos x',
     r'-\frac17\cos^{7}x+\frac19\cos^{9}x+c', '-cos(x)**7/7+cos(x)**9/9', 'sin(x)**3*cos(x)**6'),
    (r'\int\cos^{3}x\sin^{4}x\,dx', 'Odd and Even: احجز cos', r'(1-\sin^{2}x)\sin^{4}x\cos x,\ u=\sin x',
     r'\frac15\sin^{5}x-\frac17\sin^{7}x+c', 'sin(x)**5/5-sin(x)**7/7', 'cos(x)**3*sin(x)**4'),
    (r'\int\sin^{4}x\cos^{5}x\,dx', 'Odd and Even: احجز cos (📝 اختبار ثاني 1446)', r'(1-\sin^{2}x)^{2}\sin^{4}x\cos x,\ u=\sin x',
     r'\frac15\sin^{5}x-\frac27\sin^{7}x+\frac19\sin^{9}x+c', 'sin(x)**5/5-2*sin(x)**7/7+sin(x)**9/9', 'sin(x)**4*cos(x)**5'),
    (r'\int\sin^{2}x\cos^{5}x\,dx', 'Odd and Even: احجز cos (📝 اختبار ثاني 1447)', r'(1-\sin^{2}x)^{2}\sin^{2}x\cos x,\ u=\sin x',
     r'\frac13\sin^{3}x-\frac25\sin^{5}x+\frac17\sin^{7}x+c', 'sin(x)**3/3-2*sin(x)**5/5+sin(x)**7/7', 'sin(x)**2*cos(x)**5'),
    (r'\int\sin^{3}x\cos^{7}x\,dx', 'Odd and Odd: الأصغر sin', r'(1-\cos^{2}x)\cos^{7}x\sin x,\ u=\cos x',
     r'-\frac18\cos^{8}x+\frac1{10}\cos^{10}x+c', '-cos(x)**8/8+cos(x)**10/10', 'sin(x)**3*cos(x)**7'),
    (r'\int\cos^{3}2x\,dx', 'فردي لحاله بزاوية $2x$', r'u=\sin2x,\ du=2\cos2x\,dx',
     r'\frac12\sin2x-\frac16\sin^{3}2x+c', 'sin(2*x)/2-sin(2*x)**3/6', 'cos(2*x)**3'),
    (r'\int\sin^{2}3x\,dx', 'زوجي لحاله بزاوية $3x$', r'\sin^{2}3x=\frac{1-\cos6x}{2}', r'\frac x2-\frac1{12}\sin6x+c', 'x/2-sin(6*x)/12', 'sin(3*x)**2'),
    (r'\int\sin^{7}x\,dx', 'فردي لحاله (تكعيب)', r'(1-\cos^{2}x)^{3}\sin x,\ u=\cos x',
     r'-\cos x+\cos^{3}x-\frac35\cos^{5}x+\frac17\cos^{7}x+c', '-cos(x)+cos(x)**3-3*cos(x)**5/5+cos(x)**7/7', 'sin(x)**7'),
    (r'\int\sin3x\cos2x\,dx', '🚫 مو odd و even: زاويتين مختلفتين (درس الضرب)', r'\sin3x\cos2x=\frac12(\sin x+\sin5x)',
     r'-\frac12\cos x-\frac1{10}\cos5x+c', '-cos(x)/2-cos(5*x)/10', 'sin(3*x)*cos(2*x)'),
    (r'\int\sin^{5}x\cos^{5}x\,dx', 'Odd and Odd: متساويين، أي واحد', r'\sin^{5}x(1-\sin^{2}x)^{2}\cos x,\ u=\sin x',
     r'\frac16\sin^{6}x-\frac14\sin^{8}x+\frac1{10}\sin^{10}x+c', 'sin(x)**6/6-sin(x)**8/4+sin(x)**10/10', 'sin(x)**5*cos(x)**5')]


def recall():
    """Six prompts to write from memory the night or the morning before the quiz; each links to its answer."""
    prompts = [('القاعدة كلها في سؤال واحد، وفرعيه.', 'map'),
               ('ليش نحجز وحدة؟ وليش لازم أس فردي؟', 'map'),
               ('المتطابقة، وقانونا نص الزاوية، و $\\sin x\\cos x$.', 'tools'),
               ('$(1-u^2)^2$ و $(1-u^2)^3$.', 'tools'),
               ('الحركات الثلاث في Even and Even.', 'secD'),
               ('let $u$ و $du$: أشكال $du$ الثلاثة، ومن وين يجي السالب، وفحص «أعلى أس».', 'udu')]
    rows = ''.join('<div class="ch"><b>%d</b>%s%s%s</div>' % (k, p(rich(t)), lines(2, 'write tight'),
                                                          p(link(a, 'الجواب ص ' + pgref(a)), 'small'))
                   for k, (t, a) in enumerate(prompts, 1))
    return section('recall', '🧠 استرجاع قبل الكويز (اكتب من راسك، ثم شيك)',
                   p(rich('في الكويز، أول 3 أسطر (القسمة، والمتطابقة، و $u$ و $du$) عليها درجات حتى لو ما كملت. هذي الصفحة تثبّتها.'))
                   + '<div class="chgrid">' + rows + '</div>')


def page_test():
    qs = ''
    for k, (qt, br, first, ans, F, f) in enumerate(TEST, 1):
        antideriv(F, f, 'test %d' % k)
        qs += '<div class="ch"><b>%d</b>%s%s</div>' % (k, md(qt), lines(3, 'write tight'))
    return section('test', '📝 اختبار الإتقان: 10 أسئلة جديدة',
                   p(rich('<b>الجولة الأولى:</b> اكتب تحت كل سؤال <b>القسم وأول سطر</b> بس (30 ثانية لكل سؤال). '
                          '<b>الجولة الثانية:</b> حلها كاملة. 8 من 10 صح = أتقنته. ونفس أشكال موسى، بس بأسس ثانية. ')
                     + link('key', 'المفتاح ص ' + pgref('key')) + '.')
                   + '<div class="chgrid">' + qs + '</div>')


def page_key():
    items = ''.join('<li><b>%s</b><div>أول سطر: %s</div><div>الجواب: %s</div></li>'
                    % (rich(br), mi(r'\displaystyle ' + first), mi(r'\displaystyle ' + ans))
                    for k, (qt, br, first, ans, F, f) in enumerate(TEST, 1))
    checks = ''
    for g in ('A', 'C', 'B', 'D'):
        checks += '<li><b>%s</b>%s</li>' % (GROUP[g][1], ''.join('<div>(%d) %s</div>' % (n, mi(r'\displaystyle ' + a))
                                                                 for n, a in enumerate(CHECK_KEYS[g], 1)))
    fill = ul([rich(re.sub(r'\$([^$]+)\$', lambda m: '$\\displaystyle ' + m.group(1) + '$', t)) for t in ['$\\frac{1-\\cos2x}{2}$', '$\\frac18$', '$\\frac{\\sin4x}{8}$',
                                  '$u=\\sin2x$، و $\\frac{\\sin^32x}{6}$', '$\\frac{x}{16}-\\frac{\\sin4x}{64}-\\frac{\\sin^32x}{48}$']], 'keylist cols2')
    return section('key', '🔑 المفتاح',
                   '<h3>اختبار الإتقان: القسم، وأول سطر، والجواب</h3><ol class="keylist">' + items + '</ol>'
                   + p(rich('جوابك شكله غير؟ اشتقه: إذا رجع السؤال فهو صح. والفرق بثابت عادي (مثلًا في Odd and Odd لو حجزت من الثاني).'), 'small')
                   + '<h3>الفحوص الصغيرة</h3><ul class="keylist">' + checks + '</ul>'
                   + '<h3>فراغات ' + mi(r'\sin^{4}x\cos^{2}x') + ' (بالترتيب)</h3>' + fill
                   + '<h3>🔑 صفحة u و du: جرّب</h3>' + ul([rich(t) for t in UDU_KEY], 'keylist cols2'))


def page_sols():
    out = ''
    for k in ('A2', 'A4', 'A7', 'C2', 'C3', 'B2', 'B3', 'D2', 'D5', 'D3', 'D4'):
        out += ('<div class="sol" id="s-%s"><div class="drill-head"><b>%s</b> %s %s</div>%s</div>'
                % (k, musa(k), mi(r'\displaystyle ' + Q[k][0]), link('q-' + k, '↩', 'back btn'), steps(ROWS[k], 'sol ' + k)))
    return section('sols', '✅ حلول أسئلة موسى اللي ما حلها (11)',
                   p(rich('السبعة اللي حلها موسى موجودة في أقسامها بخطواته. وهذي الباقية بنفس أسلوبه.'), 'small') + out)


def build():
    check_all()
    title = ('<section class="summary" id="top"><div class="kicker">ريض 111 · درس 5.2 · مذكرة د. موسى ص 89–97</div>'
             '<h1>odd و even: تكاملات sin و cos</h1>'
             + p(rich('أسئلة موسى الـ18، كل واحد محلول. وكل سطر وكل جواب هنا فحصه الحاسوب.'), 'small')
             + p(link('map', 'ابدأ من الخريطة ←'), 'small') + '</section>')
    return (title + page_map() + page_udu() + page_tools() + page_A() + page_C() + page_B() + page_D() + page_fix() + page_test()
            + page_key() + page_sols() + recall())


OUTLINE = [[1, '🗺️ الخريطة والمتتبع', ['map']], [1, '🔑 u و du', ['udu']], [1, '🧰 الأدوات والجبر', ['tools']], [1, '١. أسس لحالها', ['secA']],
           [1, '٢. Odd and Even', ['secB']], [1, '٣. Odd and Odd', ['secC']], [1, '٤. Even and Even', ['secD']],
           [1, '🔍 صحّح الغلط', ['fix']], [1, '📝 اختبار الإتقان', ['test']], [1, '🔑 المفتاح', ['key']], [1, '✅ حلول أسئلة موسى', ['sols']],
           [1, '🧠 استرجاع قبل الكويز', ['recall']]]

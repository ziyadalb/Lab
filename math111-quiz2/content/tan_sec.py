"""«tan و sec»: تكاملات tan و sec بالأسس، على أسئلة مذكرة د. موسى (ص 98–107).

The same three moves as the sin/cos file (keep a piece, turn the rest, substitute u), now with tan and sec: four ordered
questions decide the rule (a sec^2 to keep -> u = tan; tan odd with a sec -> u = sec; no sec -> the tan chain; tan even
and sec odd -> parts, I comes back). Dr. Musa's twelve questions on pp. 98–107 (four solved by him, two solved by the
doctor in lecture 15), each section with a worked example, a fill-in or a solo question, and a small check; then the six
famous mistakes, a ten-question mastery test, the key, full solutions and a recall page. Every equality, step and
answer is checked with SymPy while building.
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


def D(tex):
    return 'diff(%s,x)' % tex


def antideriv(F, f, label):
    """The answer F really is an antiderivative of f (d/dx F = f); logs are written without |.| (0 < x < pi/2)."""
    arith('', [(D(F), f)], label + ' answer')


def mathnums(text):
    """Outside $...$: «6 = 3 + 4 − 1» becomes a math island, so the RTL line never reverses it."""
    parts = text.split('$')
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'\d+(?:\s*[=+−]\s*\d+)+', lambda m: '$' + m.group(0).replace('−', '-').replace(' ', '') + '$', parts[i])
    return '$'.join(parts)


def steps(rows, label):
    """(latex, claims, why[, 'swap']) rows; every claim is checked; the last row is the answer.
    A 🔁 swap row shows, under each piece, what it becomes in u: it is not numbered (done with the eyes, not written)."""
    body = ''
    n = 0
    for k, row in enumerate(rows, 1):
        latex, claims, why = row[:3]
        arith(latex, claims, '%s step %d' % (label, k))
        if len(row) > 3 and row[3] == SWAP:
            body += ('<tr class="swap"><td class="n">🔁</td><td colspan="2">%s<div class="swhy">%s</div></td></tr>'
                     % (mi(r'\displaystyle ' + latex), rich('<b>التبديل</b> (بعيونك، ما يلزم تكتبه): ' + why)))
            continue
        n += 1
        cls = ' class="final"' if k == len(rows) else ''
        body += '<tr%s><td class="n">%d</td><td>%s</td><td>%s</td></tr>' % (cls, n, mi(r'\displaystyle ' + latex), rich(mathnums(why)))
    return ('<table class="steps"><thead><tr><th>#</th><th>الخطوة (تكتبها)</th><th>ليش؟ (لك أنت)</th></tr></thead>'
            '<tbody>' + body + '</tbody></table>')


def sbox(head, inner, cls='', id_=''):
    return '<div class="sbox %s"%s><h3>%s</h3>%s</div>' % (cls, (' id="%s"' % id_) if id_ else '', head, inner)


def kind(k):
    return '<span class="kind %s">%s</span>' % (k, KIND[k])


# ---------------------------------------------------------------- the four rules
RULES = {
    'S': ('r1', 'secS', '١', 'أس sec زوجي (2، 4، 6…)', 'لازم يكون فيه $\\sec^2x$ تحجزه (الصفر ما يحسب)',
          'احجز $\\cD{\\sec^2x\\,dx}$، والباقي $\\sec^2=1+\\tan^2$، و $\\cU{u=\\tan x}$', 'موسى ص 98–101 و 107'),
    'T': ('r2', 'secT', '٢', 'أس tan فردي، ومعه sec', 'tan فردي، و sec أسه 1 أو أكثر',
          'احجز $\\cD{\\sec x\\tan x\\,dx}$، والباقي $\\tan^2=\\sec^2-1$، و $\\cU{u=\\sec x}$', 'موسى ص 101 و 105 و 107'),
    'L': ('r3', 'secL', '٣', 'ما فيه sec أبد', 'tan لحاله',
          'قص $\\tan^2=\\sec^2-1$: قطعة فيها $\\sec^2$، وقطعة أسها أقل بـ 2. وكرر', 'موسى ص 98 و 100 و 107'),
    'P': ('r4', 'secP', '٤', 'الباقي: tan زوجي و sec فردي', 'ومنها sec لحاله بأس فردي',
          '$dv=\\sec^2x\\,dx$، و $I$ يرجع لك، فتجمعه وتقسم', 'موسى ص 98 و 101 و 107'),
}
KIND = {'worked': '🧱 محلول', 'fill': '✍️ عبّي الفراغات', 'solo': '✏️ لحالك', 'hard': '⭐⭐⭐ اختياري'}

# ---------------------------------------------------------------- Dr. Musa's twelve questions
# id: (question latex, where in Musa, rule, integrand, answer (logs without |.|), answer latex, kind, who solved it)
Q = {
    'S1': (r'\int\sec^{4}x\,dx', 'ص 98 (4)', 'S', 'sec(x)**4', 'tan(x)+tan(x)**3/3', r'\tan x+\frac13\tan^{3}x+c', 'worked', 'موسى ص 99'),
    'S2': (r'\int\tan^{3}x\sec^{4}x\,dx', 'ص 101 (1)، وكمان ص 107 (7)', 'S', 'tan(x)**3*sec(x)**4', 'tan(x)**4/4+tan(x)**6/6',
           r'\frac14\tan^{4}x+\frac16\tan^{6}x+c', 'worked', 'موسى ص 101'),
    'S3': (r'\int\sqrt{\tan x}\,\sec^{4}x\,dx', 'ص 107 (5)', 'S', 'sqrt(tan(x))*sec(x)**4',
           '2*tan(x)**Rational(3,2)/3+2*tan(x)**Rational(7,2)/7', r'\frac23\tan^{3/2}x+\frac27\tan^{7/2}x+c', 'fill', ''),
    'T1': (r'\int\tan^{5}x\sec^{5}x\,dx', 'ص 107 (6)', 'T', 'tan(x)**5*sec(x)**5', 'sec(x)**9/9-2*sec(x)**7/7+sec(x)**5/5',
           r'\frac19\sec^{9}x-\frac27\sec^{7}x+\frac15\sec^{5}x+c', 'worked', 'موسى ص 105'),
    'T2': (r'\int\tan^{5}x\sec x\,dx', 'ص 101 (3)', 'T', 'tan(x)**5*sec(x)', 'sec(x)**5/5-2*sec(x)**3/3+sec(x)',
           r'\frac15\sec^{5}x-\frac23\sec^{3}x+\sec x+c', 'solo', ''),
    'L1': (r'\int\tan^{2}x\,dx', 'ص 98 (6)', 'L', 'tan(x)**2', 'tan(x)-x', r'\tan x-x+c', 'worked', ''),
    'L2': (r'\int\tan^{3}x\,dx', 'ص 98 (7)', 'L', 'tan(x)**3', 'tan(x)**2/2+log(cos(x))', r'\frac12\tan^{2}x+\ln|\cos x|+c', 'worked',
           'موسى ص 100 (مكتوب عليه (3))'),
    'L3': (r'\int\tan^{4}x\,dx', 'ص 98 (8)', 'L', 'tan(x)**4', 'tan(x)**3/3-tan(x)+x', r'\frac13\tan^{3}x-\tan x+x+c', 'fill',
           'دكتورك، محاضرة 15 ص 2'),
    'L4': (r'\int\tan^{6}x\,dx', 'ص 107 (16)', 'L', 'tan(x)**6', 'tan(x)**5/5-tan(x)**3/3+tan(x)-x',
           r'\frac15\tan^{5}x-\frac13\tan^{3}x+\tan x-x+c', 'solo', ''),
    'P1': (r'\int\sec^{3}x\,dx', 'ص 98 (3)', 'P', 'sec(x)**3', 'sec(x)*tan(x)/2+log(sec(x)+tan(x))/2',
           r'\frac12\sec x\tan x+\frac12\ln|\sec x+\tan x|+c', 'worked', 'دكتورك، محاضرة 15 ص 2'),
    'P2': (r'\int\sec^{5}x\,dx', 'ص 107 (15)', 'P', 'sec(x)**5', 'sec(x)**3*tan(x)/4+3*sec(x)*tan(x)/8+3*log(sec(x)+tan(x))/8',
           r'\frac14\sec^{3}x\tan x+\frac38\sec x\tan x+\frac38\ln|\sec x+\tan x|+c', 'fill', ''),
    'P3': (r'\int\tan^{4}x\sec^{3}x\,dx', 'ص 101 (2)', 'P', 'tan(x)**4*sec(x)**3',
           'sec(x)**5*tan(x)/6-7*sec(x)**3*tan(x)/24+sec(x)*tan(x)/16+log(sec(x)+tan(x))/16',
           r'\frac16\sec^{5}x\tan x-\frac7{24}\sec^{3}x\tan x+\frac1{16}\sec x\tan x+\frac1{16}\ln|\sec x+\tan x|+c', 'hard', ''),
}
ORDER = ['S1', 'S2', 'S3', 'T1', 'T2', 'L1', 'L2', 'L3', 'L4', 'P1', 'P2', 'P3']   # study order = section order


def musa(k):
    return 'موسى ' + Q[k][1]


SEC, TAN = 'sec(x)', 'tan(x)'


def U_TAN():
    return (r'\text{let }\cU{u=\tan x},\quad \cD{du=\sec^{2}x\,dx}', [(D(TAN), 'sec(x)**2')],
            'اشتق $u$ وحط جنبها $dx$: $du=\\sec^2x\\,dx$. وهذي بالضبط القطعة الخضرا.')


def U_SEC():
    return (r'\text{let }\cU{u=\sec x},\quad \cD{du=\sec x\tan x\,dx}', [(D(SEC), 'sec(x)*tan(x)')],
            'مشتقة $\\sec x$ هي $\\sec x\\tan x$: هي بالضبط القطعة الخضرا. (وما فيه سالب هنا.)')


SWAP = 'swap'          # a 🔁 row: under each piece, what it becomes in u (done with the eyes, not numbered)
SWAP_WHY = 'كل قطعة صارت $u$، والخضرا صارت $du$. ما بقى ولا $x$ ولا $dx$ ✓'


def UB(x_tex, u_tex):
    """A piece of the integral and, under it, what it becomes in u."""
    return r'\underbrace{%s}_{\displaystyle \cU{%s}}' % (x_tex, u_tex)


def UD(x_tex, du_tex=r'\cD{du}'):
    """The kept (green) piece and, under it, its du form."""
    return r'\underbrace{\cD{%s}}_{\displaystyle %s}' % (x_tex, du_tex)


# ---------------------------------------------------------------- the steps of every question (checked), in the doctor's style (I = ...)
ROWS = {
    'S1': [(r'I=\int\sec^{2}x\cdot\cD{\sec^{2}x\,dx}', [('sec(x)**4', 'sec(x)**2*sec(x)**2')],
            'أس sec زوجي (4): نحجز $\\sec^2x$ ونكتبها آخر شي، لأنها $du$ حق $u=\\tan x$.'),
           (r'I=\int(1+\tan^{2}x)\,\cD{\sec^{2}x\,dx}', [('sec(x)**2', '1+tan(x)**2')], 'الباقي $\\sec^2x$ نحوّله لـ tan بـ $\\sec^2=1+\\tan^2$، عشان يصير كله $u$.'),
           U_TAN(),
           (r'I=\int' + UB(r'(1+\tan^{2}x)', r'(1+u^{2})') + r'\;' + UD(r'\sec^{2}x\,dx'), [('sec(x)**4', '(1+tan(x)**2)*diff(tan(x),x)')], SWAP_WHY, SWAP),
           (r'I=\int(1+u^{2})\,du=u+\frac13u^{3}+c', [('integrate(1+u**2,u)', 'u+u**3/3')], 'كل حد: زد الأس 1 واقسم عليه.'),
           (r'I=\tan x+\frac13\tan^{3}x+c', [(D('tan(x)+tan(x)**3/3'), 'sec(x)**4')], 'نرجّع $u=\\tan x$. فحص: أكبر أس 3 = 4 − 1 ✓')],
    'S2': [(r'I=\int\tan^{3}x\,\sec^{2}x\cdot\cD{\sec^{2}x\,dx}', [('tan(x)**3*sec(x)**4', 'tan(x)**3*sec(x)**2*sec(x)**2')],
            'أس sec زوجي (4): نحجز $\\sec^2x$. (tan فردي بعد: القسمين ينفعون. نبدأ بـ sec الزوجي مثل موسى، وبالقسم ٢ يطلع جوابك شكله غير وهو صح.)'),
           (r'I=\int\tan^{3}x\,(1+\tan^{2}x)\,\cD{\sec^{2}x\,dx}', [('sec(x)**2', '1+tan(x)**2')], 'الباقي $\\sec^2=1+\\tan^2$، عشان يصير كله $u$.'),
           U_TAN(),
           (r'I=\int' + UB(r'\tan^{3}x', 'u^{3}') + r'\,' + UB(r'(1+\tan^{2}x)', r'(1+u^{2})') + r'\;' + UD(r'\sec^{2}x\,dx'),
            [('tan(x)**3*sec(x)**4', 'tan(x)**3*(1+tan(x)**2)*diff(tan(x),x)')], SWAP_WHY, SWAP),
           (r'I=\int u^{3}(1+u^{2})\,du=\int(u^{3}+u^{5})\,du', [('u**3*(1+u**2)', 'u**3+u**5')], 'نوزّع $u^3$: الأسس تنجمع.'),
           (r'I=\frac14\tan^{4}x+\frac16\tan^{6}x+c', [(D('tan(x)**4/4+tan(x)**6/6'), 'tan(x)**3*sec(x)**4')], 'فحص: 6 = 3 + 4 − 1 ✓')],
    'S3': [(r'I=\int\tan^{1/2}x\,\sec^{2}x\cdot\cD{\sec^{2}x\,dx}', [('sqrt(tan(x))*sec(x)**4', 'tan(x)**Rational(1,2)*sec(x)**2*sec(x)**2')],
            '$\\sqrt{\\tan x}=\\tan^{1/2}x$. وأس sec زوجي: نحجز $\\sec^2x$.'),
           (r'I=\int\tan^{1/2}x\,(1+\tan^{2}x)\,\cD{\sec^{2}x\,dx}', [('sec(x)**2', '1+tan(x)**2')], 'الباقي لـ tan، عشان يصير كله $u$.'),
           U_TAN(),
           (r'I=\int' + UB(r'\tan^{1/2}x', 'u^{1/2}') + r'\,' + UB(r'(1+\tan^{2}x)', r'(1+u^{2})') + r'\;' + UD(r'\sec^{2}x\,dx'),
            [('sqrt(tan(x))*sec(x)**4', 'tan(x)**Rational(1,2)*(1+tan(x)**2)*diff(tan(x),x)')], SWAP_WHY, SWAP),
           (r'I=\int u^{1/2}(1+u^{2})\,du=\int(u^{1/2}+u^{5/2})\,du', [('u**Rational(1,2)*(1+u**2)', 'u**Rational(1,2)+u**Rational(5,2)')],
            '$\\frac12+2=\\frac52$ (لأن $2=\\frac42$).'),
           (r'I=\frac23u^{3/2}+\frac27u^{7/2}+c', [('integrate(u**Rational(1,2)+u**Rational(5,2),u)', '2*u**Rational(3,2)/3+2*u**Rational(7,2)/7')],
            'زد 1 واقلب: $\\frac12+1=\\frac32$ فنضرب في $\\frac23$، و $\\frac52+1=\\frac72$ فنضرب في $\\frac27$.'),
           (r'I=\frac23\tan^{3/2}x+\frac27\tan^{7/2}x+c', [(D('2*tan(x)**Rational(3,2)/3+2*tan(x)**Rational(7,2)/7'), 'sqrt(tan(x))*sec(x)**4')],
            'فحص: $\\frac72=\\frac12+4-1$ ✓')],
    'T1': [(r'I=\int\tan^{4}x\,\sec^{4}x\cdot\cD{\sec x\tan x\,dx}', [('tan(x)**5*sec(x)**5', 'tan(x)**4*sec(x)**4*sec(x)*tan(x)')],
            'أس sec فردي (5)، فالقاعدة ١ ما تنفع. أس tan فردي (5): نحجز $\\sec x\\tan x$.'),
           (r'I=\int(\sec^{2}x-1)^{2}\sec^{4}x\,\cD{\sec x\tan x\,dx}', [('tan(x)**4', '(sec(x)**2-1)**2')],
            'الباقي $\\tan^4=(\\tan^2)^2$، وكل $\\tan^2=\\sec^2-1$، عشان يصير كله $u$.'),
           U_SEC(),
           (r'I=\int' + UB(r'(\sec^{2}x-1)^{2}', r'(u^{2}-1)^{2}') + r'\,' + UB(r'\sec^{4}x', 'u^{4}') + r'\;' + UD(r'\sec x\tan x\,dx'),
            [('tan(x)**5*sec(x)**5', '(sec(x)**2-1)**2*sec(x)**4*diff(sec(x),x)')], SWAP_WHY, SWAP),
           (r'I=\int(u^{2}-1)^{2}u^{4}\,du=\int(u^{8}-2u^{6}+u^{4})\,du', [('(u**2-1)**2*u**4', 'u**8-2*u**6+u**4')],
            'نفك القوس (جاهز في الأدوات)، ونضرب في $u^4$.'),
           (r'I=\frac19\sec^{9}x-\frac27\sec^{7}x+\frac15\sec^{5}x+c', [(D('sec(x)**9/9-2*sec(x)**7/7+sec(x)**5/5'), 'tan(x)**5*sec(x)**5')],
            'نرجّع $u=\\sec x$. فحص: 9 = 5 + 5 − 1 ✓')],
    'T2': [(r'I=\int\tan^{4}x\cdot\cD{\sec x\tan x\,dx}', [('tan(x)**5*sec(x)', 'tan(x)**4*sec(x)*tan(x)')],
            'tan فردي، و sec أسه 1 بس: يروح كله في القطعة المحجوزة.'),
           (r'I=\int(\sec^{2}x-1)^{2}\,\cD{\sec x\tan x\,dx}', [('tan(x)**4', '(sec(x)**2-1)**2')], '$\\tan^4=(\\sec^2-1)^2$، عشان يصير كله $u$.'),
           U_SEC(),
           (r'I=\int' + UB(r'(\sec^{2}x-1)^{2}', r'(u^{2}-1)^{2}') + r'\;' + UD(r'\sec x\tan x\,dx'),
            [('tan(x)**5*sec(x)', '(sec(x)**2-1)**2*diff(sec(x),x)')], SWAP_WHY, SWAP),
           (r'I=\int(u^{4}-2u^{2}+1)\,du', [('(u**2-1)**2', 'u**4-2*u**2+1')], 'نفك القوس.'),
           (r'I=\frac15\sec^{5}x-\frac23\sec^{3}x+\sec x+c', [(D('sec(x)**5/5-2*sec(x)**3/3+sec(x)'), 'tan(x)**5*sec(x)')],
            'فحص: 5 = 5 + 1 − 1 ✓')],
    'L1': [(r'I=\int(\sec^{2}x-1)\,dx', [('tan(x)**2', 'sec(x)**2-1')], 'ما فيه sec تحجزه: نحوّل $\\tan^2$ كلها بالمتطابقة.'),
           (r'I=\tan x-x+c', [(D('tan(x)-x'), 'tan(x)**2')], '$\\int\\sec^2x\\,dx=\\tan x$، و $\\int1\\,dx=x$. هذي أول درجة في السلسلة.')],
    'L2': [(r'I=\int\tan^{2}x\,\tan x\,dx=\int(\sec^{2}x-1)\tan x\,dx', [('tan(x)**3', '(sec(x)**2-1)*tan(x)')], 'نقص $\\tan^2$ ونحوّلها.'),
           (r'I=\int\tan x\,\cD{\sec^{2}x\,dx}-\int\tan x\,dx', [('(sec(x)**2-1)*tan(x)', 'tan(x)*sec(x)**2-tan(x)')], 'نوزّع: صار عندنا قطعتين.'),
           U_TAN(),
           (r'\int' + UB(r'\tan x', 'u') + r'\;' + UD(r'\sec^{2}x\,dx') + r'\ -\int\tan x\,dx', [('tan(x)*sec(x)**2', 'tan(x)*diff(tan(x),x)')],
            'القطعة الأولى صارت $\\int u\\,du$. والثانية من الأربع اللي تحفظها ✓', SWAP),
           (r'I=\int u\,du+\ln|\cos x|+c', [('integrate(u,u)', 'u**2/2'), (D('log(cos(x))'), '-tan(x)')],
            '$\\int\\tan x\\,dx=-\\ln|\\cos x|$، والسالب اللي قدامها يخليها $+$.'),
           (r'I=\frac12\tan^{2}x+\ln|\cos x|+c', [(D('tan(x)**2/2+log(cos(x))'), 'tan(x)**3')],
            'مثل موسى بالضبط. (ونفسها $\\frac12\\tan^2x-\\ln|\\sec x|$.) فحص: 2 = 3 − 1 ✓')],
    'L3': [(r'I=\int\tan^{2}x\,(\sec^{2}x-1)\,dx', [('tan(x)**4', 'tan(x)**2*(sec(x)**2-1)')], 'نقص $\\tan^2$ وحدة بس، ونخلي الثانية.'),
           (r'I=\int\tan^{2}x\,\cD{\sec^{2}x\,dx}-\int\tan^{2}x\,dx', [('tan(x)**2*(sec(x)**2-1)', 'tan(x)**2*sec(x)**2-tan(x)**2')], 'نوزّع.'),
           (r'I=\frac13\tan^{3}x-\int\tan^{2}x\,dx', [(D('tan(x)**3/3'), 'tan(x)**2*sec(x)**2')],
            'القطعة الأولى $u=\\tan x$. والثانية $\\int\\tan^2x$ حليناها في أول درجة.'),
           (r'I=\frac13\tan^{3}x-(\tan x-x)+c', [], 'السالب يدخل على القوس كله.'),
           (r'I=\frac13\tan^{3}x-\tan x+x+c', [(D('tan(x)**3/3-tan(x)+x'), 'tan(x)**4')],
            'نفس جواب دكتورك (محاضرة 15، مثال 5). فحص: 3 = 4 − 1 ✓')],
    'L4': [(r'I=\int\tan^{4}x\,\cD{\sec^{2}x\,dx}-\int\tan^{4}x\,dx', [('tan(x)**6', 'tan(x)**4*sec(x)**2-tan(x)**4')],
            'نقص $\\tan^2=\\sec^2-1$ من $\\tan^6$ ونوزّع.'),
           (r'I=\frac15\tan^{5}x-\int\tan^{4}x\,dx', [(D('tan(x)**5/5'), 'tan(x)**4*sec(x)**2')], 'القطعة الأولى $u=\\tan x$.'),
           (r'I=\frac15\tan^{5}x-\left(\frac13\tan^{3}x-\tan x+x\right)+c', [], '$\\int\\tan^4x$ حليناها في الدرجة اللي قبل.'),
           (r'I=\frac15\tan^{5}x-\frac13\tan^{3}x+\tan x-x+c', [(D('tan(x)**5/5-tan(x)**3/3+tan(x)-x'), 'tan(x)**6')],
            'السالب يدخل على كل القوس. فحص: 5 = 6 − 1 ✓')],
    'P1': [(r'I=\int\sec x\cdot\sec^{2}x\,dx', [('sec(x)**3', 'sec(x)*sec(x)**2')], 'لو حجزنا $\\sec^2$ يبقى $\\sec x$ ما تتحول لـ tan: فتجزئة مثل دكتورك.'),
           (r'\begin{aligned}&\cU{u=\sec x} &&dv=\sec^{2}x\,dx\\ &\cD{du=\sec x\tan x\,dx} &&v=\tan x\end{aligned}', [(D(SEC), 'sec(x)*tan(x)'), (D(TAN), 'sec(x)**2')],
            '$dv=\\sec^2x\\,dx$ لأن تكاملها سهل: $v=\\tan x$.'),
           (r'I=\sec x\tan x-\int\sec x\tan^{2}x\,dx', [('sec(x)**3', 'diff(sec(x)*tan(x),x)-sec(x)*tan(x)**2')], '$I=uv-\\int v\\,du$.'),
           (r'I=\sec x\tan x-\int\sec x(\sec^{2}x-1)\,dx', [('tan(x)**2', 'sec(x)**2-1')], '$\\tan^2=\\sec^2-1$.'),
           (r'I=\sec x\tan x-\int\sec^{3}x\,dx+\int\sec x\,dx', [('sec(x)*(sec(x)**2-1)', 'sec(x)**3-sec(x)')], 'نوزّع. انتبه: رجع لنا $\\int\\sec^3x$ نفسه!'),
           (r'I=\sec x\tan x-\cR{I}+\ln|\sec x+\tan x|', [(D('log(sec(x)+tan(x))'), 'sec(x)')], '↩️ $I$ رجع! ننقله للطرف الثاني.'),
           (r'2I=\sec x\tan x+\ln|\sec x+\tan x|', [(D('sec(x)*tan(x)+log(sec(x)+tan(x))'), '2*sec(x)**3')], '$I+I=2I$.'),
           (r'I=\frac12\sec x\tan x+\frac12\ln|\sec x+\tan x|+c', [(D('sec(x)*tan(x)/2+log(sec(x)+tan(x))/2'), 'sec(x)**3')],
            'نقسم <b>كل</b> الحدود على 2: «نص ونص». فحص: $\\sec x\\tan x$ أسها $1+1=2=3-1$ ✓')],
    'P2': [(r'I=\int\sec^{3}x\cdot\sec^{2}x\,dx', [('sec(x)**5', 'sec(x)**3*sec(x)**2')], 'نفس حركة $\\sec^3$: $\\sec^2x\\,dx$ هي $dv$.'),
           (r'\begin{aligned}&\cU{u=\sec^{3}x} &&dv=\sec^{2}x\,dx\\ &\cD{du=3\sec^{3}x\tan x\,dx} &&v=\tan x\end{aligned}',
            [(D('sec(x)**3'), '3*sec(x)**3*tan(x)'), (D(TAN), 'sec(x)**2')], 'مشتقة $\\sec^3x$: $3\\sec^2x\\cdot\\sec x\\tan x$ (قاعدة السلسلة).'),
           (r'I=\sec^{3}x\tan x-3\int\sec^{3}x\tan^{2}x\,dx', [('sec(x)**5', 'diff(sec(x)**3*tan(x),x)-3*sec(x)**3*tan(x)**2')], '$uv-\\int v\\,du$.'),
           (r'I=\sec^{3}x\tan x-3\int\sec^{5}x\,dx+3\int\sec^{3}x\,dx', [('sec(x)**3*tan(x)**2', 'sec(x)**5-sec(x)**3')],
            '$\\tan^2=\\sec^2-1$ ونوزّع: $I$ رجع، ومعه 3.'),
           (r'4I=\sec^{3}x\tan x+3\int\sec^{3}x\,dx', [], '$I+3I=4I$.'),
           (r'\begin{aligned}I=&\ \frac14\sec^{3}x\tan x\\&+\frac34\left(\frac12\sec x\tan x+\frac12\ln|\sec x+\tan x|\right)+c\end{aligned}',
            [(D('sec(x)**3*tan(x)/4+Rational(3,4)*(sec(x)*tan(x)/2+log(sec(x)+tan(x))/2)'), 'sec(x)**5')],
            'نقسم على 4. و $\\int\\sec^3x$ جاهزة: «نص ونص».'),
           (r'\begin{aligned}I=&\ \frac14\sec^{3}x\tan x+\frac38\sec x\tan x\\&+\frac38\ln|\sec x+\tan x|+c\end{aligned}',
            [(D('sec(x)**3*tan(x)/4+3*sec(x)*tan(x)/8+3*log(sec(x)+tan(x))/8'), 'sec(x)**5')],
            '$\\frac34\\cdot\\frac12=\\frac38$. فحص: $\\sec^3x\\tan x$ أسها $3+1=4=5-1$ ✓')],
    'P3': [(r'\tan^{4}x=(\sec^{2}x-1)^{2}=\sec^{4}x-2\sec^{2}x+1', [('tan(x)**4', '(sec(x)**2-1)**2'), ('(sec(x)**2-1)**2', 'sec(x)**4-2*sec(x)**2+1')],
            'tan زوجي و sec فردي: ما فيه حجز. نحوّل كل tan لـ sec.'),
           (r'I=\int\sec^{7}x\,dx-2\int\sec^{5}x\,dx+\int\sec^{3}x\,dx', [('tan(x)**4*sec(x)**3', 'sec(x)**7-2*sec(x)**5+sec(x)**3')],
            'نضرب في $\\sec^3x$: صارت كلها sec لحاله.'),
           (r'\int\sec^{7}x\,dx=\frac16\sec^{5}x\tan x+\frac56\int\sec^{5}x\,dx', [('sec(x)**7', 'diff(sec(x)**5*tan(x)/6,x)+Rational(5,6)*sec(x)**5')],
            'نفس حركة $\\sec^5$: $u=\\sec^5x$، و $I$ يرجع بـ 5، فـ $6I$.'),
           (r'I=\frac16\sec^{5}x\tan x-\frac76\int\sec^{5}x\,dx+\int\sec^{3}x\,dx',
            [('tan(x)**4*sec(x)**3', 'diff(sec(x)**5*tan(x)/6,x)-Rational(7,6)*sec(x)**5+sec(x)**3')], '$\\frac56-2=-\\frac76$.'),
           (r'I=\frac16\sec^{5}x\tan x-\frac7{24}\sec^{3}x\tan x+\frac18\int\sec^{3}x\,dx',
            [('tan(x)**4*sec(x)**3', 'diff(sec(x)**5*tan(x)/6-7*sec(x)**3*tan(x)/24,x)+sec(x)**3/8')],
            '$\\int\\sec^5$ من القسم: $\\frac14\\sec^3\\tan+\\frac34\\int\\sec^3$. و $-\\frac76\\cdot\\frac34+1=\\frac18$.'),
           (r'\begin{aligned}I=&\ \frac16\sec^{5}x\tan x-\frac7{24}\sec^{3}x\tan x\\&+\frac1{16}\sec x\tan x+\frac1{16}\ln|\sec x+\tan x|+c\end{aligned}',
            [(D('sec(x)**5*tan(x)/6-7*sec(x)**3*tan(x)/24+sec(x)*tan(x)/16+log(sec(x)+tan(x))/16'), 'tan(x)**4*sec(x)**3')],
            '«نص ونص» ضرب $\\frac18$. فحص: $\\sec^5x\\tan x$ أسها $5+1=6=4+3-1$ ✓')],
}

FILL = {
    'S3': [r'I=\int\tan^{1/2}x\,\sec^{2}x\cdot' + BLANK + r'\,dx',
           r'I=\int\tan^{1/2}x\,(' + BLANK + r')\,\sec^{2}x\,dx',
           r'u=' + BLANK + r',\quad du=' + BLANK,
           r'I=\int(u^{1/2}+u^{' + BLANK + r'})\,du',
           r'I=' + BLANK + r'+c'],
    'L3': [r'I=\int\tan^{2}x\,(' + BLANK + r')\,dx',
           r'I=\int\tan^{2}x\sec^{2}x\,dx-\int' + BLANK + r'\,dx',
           r'I=' + BLANK + r'-(\tan x-x)+c',
           r'I=' + BLANK + r'+c'],
    'P2': [r'u=' + BLANK + r',\quad dv=\sec^{2}x\,dx,\quad du=' + BLANK + r',\quad v=\tan x',
           r'I=\sec^{3}x\tan x-3\int\sec^{3}x\,(' + BLANK + r')\,dx',
           BLANK + r'\,I=\sec^{3}x\tan x+3\int\sec^{3}x\,dx',
           r'I=\frac14\sec^{3}x\tan x+\frac34\cdot' + BLANK + r'+c'],
}
FILL_KEY = {
    'S3': [r'\sec^{2}x', r'1+\tan^{2}x', r'\tan x,\ \sec^{2}x\,dx', r'5/2', r'\frac23\tan^{3/2}x+\frac27\tan^{7/2}x'],
    'L3': [r'\sec^{2}x-1', r'\tan^{2}x', r'\frac13\tan^{3}x', r'\frac13\tan^{3}x-\tan x+x'],
    'P2': [r'\sec^{3}x,\ \ 3\sec^{3}x\tan x\,dx', r'\sec^{2}x-1', r'4', r'\left(\frac12\sec x\tan x+\frac12\ln|\sec x+\tan x|\right)'],
}


def check_all():
    for k in ORDER:
        antideriv(Q[k][4], Q[k][3], 'Musa ' + k)
    # the other route of a question both rules fit (tan^3 sec^4 with u = sec) is right too
    antideriv('sec(x)**6/6-sec(x)**4/4', 'tan(x)**3*sec(x)**4', 'S2 other route')
    arith('', [('sec(x)**6/6-sec(x)**4/4-(tan(x)**4/4+tan(x)**6/6)', 'Rational(-1,12)')], 'S2 routes differ by a constant')


# ---------------------------------------------------------------- pages
TITLES = {'S': 'أس sec زوجي: $u=\\tan x$', 'T': 'أس tan فردي ومعه sec: $u=\\sec x$', 'L': 'ما فيه sec: سلسلة tan',
          'P': 'tan زوجي و sec فردي: تجزئة'}


def rule_head(r, title=None, of=True):
    cls, anchor, num, ask, sub, todo, pages = RULES[r]
    title = title or TITLES[r]
    return ('<div class="ts-head %s"><div class="top"><div class="num">%s</div><h2>%s</h2>%s</div>'
            '<div class="rule">%s</div><div class="meta">%s · %s</div></div>'
            % (cls, num, rich(title or ask), '<span class="of">القسم %s من ٤</span>' % num if of else '', rich(todo), rich(sub), pages))


def page_start():
    hero = ('<div class="ts-hero"><div class="kicker">ريض 111 · درس 5.2 · مذكرة د. موسى ص 98–107</div>'
            '<h1>tan و sec</h1><div class="sub">نفس حركات sin و cos اللي تعرفها، بس مع tan و sec.</div>'
            '<div class="ts-chips"><span class="ts-chip">4 قواعد</span><span class="ts-chip">12 سؤال من موسى</span>'
            '<span class="ts-chip">6 محلولة لك</span><span class="ts-chip">كل سطر فحصه الحاسوب</span></div></div>')
    same = table(['', 'sin و cos (تعرفها)', 'tan و sec (هذا الملف)'], [
        [rich('احجز ($du$)'), mi(r'\cos x\,dx') + ' أو ' + mi(r'\sin x\,dx'), mi(r'\sec^{2}x\,dx') + ' أو ' + mi(r'\sec x\tan x\,dx')],
        ['حوّل الباقي بـ', mi(r'\sin^{2}x+\cos^{2}x=1'), mi(r'\sec^{2}x-\tan^{2}x=1')],
        ['عوّض', mi(r'u=\sin x') + ' أو ' + mi(r'\cos x'), mi(r'u=\tan x') + ' أو ' + mi(r'\sec x')],
        ['ما فيه شي تحجزه؟', 'نص الزاوية', 'سلسلة tan، أو تجزئة'],
        ['فحص أكبر أس', 'مجموع الأسين', '<b>مجموع الأسين − 1</b>']], 'same')
    arith('', [('sec(x)**2-tan(x)**2', '1')], 'start identity')
    qs = ''
    for r in ('S', 'T', 'L', 'P'):
        cls, anchor, num, ask, sub, todo, pages = RULES[r]
        qs += ('<div class="ts-q %s"><div class="num">%s</div><div class="txt"><div class="ask">%s؟</div><div>%s</div></div>%s</div>'
               % (cls, num, rich(ask), rich(todo), link(anchor, 'القسم %s ص %s' % (num, pgref(anchor)), 'go')))
    note = ('<div class="ts-note">' + rich('⚠️ <b>الصفر زوجي بس ما يحسب:</b> $\\tan^4x$ ما فيه $\\sec^2$ تحجزه، فهي ثالث سؤال. '
                                           'و $\\sec^3x$ لو حجزت منها $\\sec^2$ يبقى $\\sec x$ ما تتحول، فهي رابع سؤال.') + '</div>')
    return ('<section class="chapter first" id="start">' + hero
            + '<div class="ts-sentence">' + rich('احجز دايم $du$: sec زوجي ← $u=\\tan x$ · tan فردي ← $u=\\sec x$') + '</div>'
            + '<h3>نفس الحركات، والفرق بس في الشريك</h3>' + same
            + '<h3>🧭 أربعة أسئلة، بالترتيب، وأول «إيه» هي قاعدتك</h3>' + qs + note
            + '<div class="ts-go">' + link('udu', 'ابدأ: 🔑 u و du ←') + '</div>'
            + p(' · '.join(link(an, t + ' ص ' + pgref(an)) for an, t in [
                ('udu', '🔑 u و du'), ('map', '🗺️ المتتبع'), ('tools', '🧰 الأدوات'), ('fix', '🔍 صحّح الغلط'), ('test', '📝 الاختبار'),
                ('key', '🔑 المفتاح'), ('sols', '✅ الحلول'), ('recall', '🧠 الاسترجاع')]), 'small center') + '</section>')


UDU_KEY = ['(1) $\\displaystyle \\sec^{2}x\\,dx=du$',
           '(2) $\\displaystyle \\sec2x\\tan2x\\,dx=\\frac12\\,du$ (لأن $du=2\\sec2x\\tan2x\\,dx$)',
           '(3) $u$، و $du$: $\\displaystyle \\int u^{4}\\,du=\\frac15\\tan^{5}x+c$']


def page_udu():
    """u and du from zero, in tan and sec: the exchange idea, the two lines to write, why the kept piece is needed (the
    whole secret of sections 1 and 2), one full example with the 🔁 swap, the shapes of du, a note on the other u of parts,
    four questions and practice."""
    ex = steps([
        (r'\text{let }\cU{u=\tan x},\quad \cD{du=\sec^{2}x\,dx}', [(D(TAN), 'sec(x)**2')], 'سطرين «سعر الصرف»: اشتق $u$ وحط جنبها $dx$.'),
        (r'I=\int' + UB(r'\tan^{2}x', 'u^{2}') + r'\;' + UD(r'\sec^{2}x\,dx'), [('tan(x)**2*sec(x)**2', 'tan(x)**2*diff(tan(x),x)')],
         '$\\tan^2x$ صارت $u^2$، و $\\sec^2x\\,dx$ كلها مع بعض صارت $du$. ما بقى ولا $x$ ✓', SWAP),
        (r'I=\int u^{2}\,du=\frac13u^{3}+c', [('integrate(u**2,u)', 'u**3/3')], 'صار سهل: زد الأس 1 واقسم عليه.'),
        (r'I=\frac13\tan^{3}x+c', [(D('tan(x)**3/3'), 'tan(x)**2*sec(x)**2')], 'نرجّع $u=\\tan x$. وتأكد: اشتقه، يرجع السؤال ✓')], 'udu ex')
    forms = table([rich('let $u$'), rich('$du$'), 'القطعة اللي في السؤال تصير', ''], [
        [mi(r'u=\tan x'), mi(r'du=\sec^{2}x\,dx'), mi(r'\sec^{2}x\,dx=du'), ''],
        [mi(r'u=\sec x'), mi(r'du=\sec x\tan x\,dx'), mi(r'\sec x\tan x\,dx=du'), ''],
        [mi(r'u=\tan3x'), mi(r'du=3\sec^{2}3x\,dx'), mi(r'\sec^{2}3x\,dx=\tfrac13\,du'), 'اقسم الطرفين على 3']], 'duforms')
    arith('', [(D('tan(x)'), 'sec(x)**2'), (D('sec(x)'), 'sec(x)*tan(x)'), (D('tan(3*x)'), '3*sec(3*x)**2')], 'udu forms')
    arith('', [(D('sec(2*x)'), '2*sec(2*x)*tan(2*x)')], 'udu practice 2')
    antideriv('tan(x)**5/5', 'tan(x)**4*sec(x)**2', 'udu practice 3')
    practice = ('<ol class="fill">'
                + '<li>%s</li>' % mi(r'\text{let }u=\tan x\ \Rightarrow\ \sec^{2}x\,dx=' + BLANK)
                + '<li>%s</li>' % mi(r'\text{let }u=\sec2x\ \Rightarrow\ \sec2x\tan2x\,dx=' + BLANK)
                + '<li>%s</li>' % mi(r'\displaystyle\int\tan^{4}x\,\sec^{2}x\,dx=\int(' + BLANK + r')^{4}\,(' + BLANK + r')') + '</ol>'
                + p(rich('وكمّل الثالث لين الجواب:'), 'small') + lines(2, 'write tight'))
    checks = ul([rich(t) for t in ['✅ كتبت let $u$ و $du$؟', '✅ قطعة $du$ موجودة كاملة في السؤال؟',
                                     '✅ بعد التبديل: ما بقى ولا $x$ ولا $dx$؟', '✅ رجّعت $x$ في الآخر؟']], 'checks')
    return ('<section class="chapter" id="udu"><div class="ts-head ts-plain"><div class="top"><h2>🔑 u و du من الصفر (اقرأها قبل أي حل)</h2></div></div>'
            + '<div class="ts-sentence">' + rich('الفكرة: نحوّل التكامل الصعب لتكامل سهل مثل $\\int u^2\\,du$') + '</div>'
            + p(rich('مثل تصريف الفلوس: كل شي بـ«عملة $x$» يتصرّف لـ«عملة $u$». ولو بقى شي واحد بعملة $x$، التصريف خربان.'))
            + '<div class="toolgrid">'
            + sbox(rich('١. سعر الصرف: سطرين تكتبهم دايم (مثل دكتورك)'), md(r'\begin{gathered}\text{let }\cU{u=\tan x}\\ \cD{du=\sec^{2}x\,dx}\end{gathered}')
                   + p(rich('اشتق $u$، وحط جنبها $dx$. <b>ليش $dx$؟</b> كل تكامل آخره $dx$. ولما نصرف لـ $u$، القطعة $\\sec^2x\\,dx$ '
                            '<b>كلها مع بعض</b> تصير $du$.')))
            + sbox(rich('٢. ليش لازم القطعة الخضرا؟'),
                   p(rich('$du$ هي «تذكرة» التصريف. مثلًا $\\int\\tan^2x\\,dx$ ما فيها $\\sec^2x$، فـ $u=\\tan x$ ما تنفع، وعشان كذا لها قاعدة لحالها (القسم ٣).'))
                   + p(rich('<b>وهذا سر القسمين ١ و ٢:</b> sec الزوجي يعطيك $\\sec^2x$ تحجزها، و tan الفردي مع sec يعطيك $\\sec x\\tan x$.')))
            + '</div>'
            + sbox(rich('٣. مثال كامل: $\\int\\tan^2x\\sec^2x\\,dx$'), ex
                   + p(rich('السطور المرقّمة تكتبها في الكويز. وسطر 🔁 تسويه بعيونك: قوس تحت كل قطعة، ومكتوب تحته وش صارت.'), 'small'), 'worked')
            + sbox(rich('٤. أشكال $du$ هنا (وما فيه سالب أبد، أسهل من cos!)'), forms)
            + '<div class="tip">' + rich('⚠️ <b>في القسم ٤ (التجزئة) $u$ معناها شي ثاني:</b> القطعة اللي نشتقها، و $dv$ اللي نكاملها. مو تعويض.') + '</div>'
            + '<div class="toolgrid">' + sbox(rich('✅ 4 أسئلة قبل ما تكمّل أي حل'), checks)
            + sbox(rich('✍️ جرّب (الأجوبة في المفتاح ص ') + pgref('key') + ')', practice) + '</div>'
            + '<div class="ts-go">' + link('secS', 'يلا: القسم ١ ←') + '</div></section>')


def page_map():
    doc = table(['عند دكتورك (محاضرة 16)', 'يعني', 'هنا'], [
        ['m is odd', rich('أس tan فردي: $u=\\sec x$'), link('secT', 'القسم ٢')],
        ['n is even', rich('أس sec زوجي: $u=\\tan x$'), link('secS', 'القسم ١')],
        ['m is even and n is odd', 'تجزئة', link('secP', 'القسم ٤')],
        [mi(r'\int\tan^{4}x\,dx') + ' (lecture 15)', 'tan لحاله', link('secL', 'القسم ٣')]], 'doc')
    rows = []
    for k in ORDER:
        r = Q[k][2]
        who = Q[k][7]
        short = {'موسى ص 99': 'موسى ص 99', 'موسى ص 101': 'موسى ص 101', 'موسى ص 105': 'موسى ص 105',
                 'موسى ص 100 (مكتوب عليه (3))': 'موسى ص 100', 'دكتورك، محاضرة 15 ص 2': 'دكتورك (م 15)'}
        where = Q[k][1].split('،')[0] + ((' <span class="src">· ✔ %s</span>' % short[who]) if who else '')
        rows.append(['☐', '<span class="dot %s"></span>' % RULES[r][0] + mi(Q[k][0]), where, kind(Q[k][6]), link('q-' + k, pgref('q-' + k))])
    tracker = table(['☐', 'السؤال', 'عند موسى (✔ محلول عند)', 'هنا', 'ص'], rows, 'tracker')
    plan = ('<ol class="plan">' + ''.join('<li>%s</li>' % rich(t) for t in [
        '<b>«ابدأ هنا»، و 🔑 u و du، والأدوات:</b> غطِّ واكتب المشتقتين، والمتطابقة، والتكاملات الأربعة.',
        '<b>الأقسام الأربعة بالترتيب:</b> 🧱 غطِّ عمود «الخطوة» وتوقّع السطر الجاي، ✍️ عبّي، ✏️ حل لحالك، ✅ الفحص. وعلّم ☐ هنا.',
        '<b>🔍 صحّح الغلط، ثم 📝 الاختبار:</b> جولة أول سطر بس، وجولة حل كامل. 8 من 10 = أتقنته.',
        '<b>أمثلة دكتورك</b> (محاضرة 15 ص 2، ومحاضرة 16 ص 1): غطِّ حله وحلها. <b>وقبل الكويز:</b> 🧠 الاسترجاع.']) + '</ol>')
    short = ('<div class="tip">' + rich('⏱️ <b>وقتك ضيق؟</b> «ابدأ هنا»، والأدوات، والقسمين ١ و ٢، وأول 4 أسئلة من الاختبار. '
                                         'كل أسئلة tan و sec في الاختبارات القديمة كانت منهم.') + '</div>')
    contents = p(' · '.join([link(a, t) + ' ص ' + pgref(a) for a, t in [
        ('tools', '🧰 الأدوات'), ('secS', '١'), ('secT', '٢'), ('secL', '٣'), ('secP', '٤'), ('fix', '🔍 صحّح الغلط'),
        ('test', '📝 الاختبار'), ('key', '🔑 المفتاح'), ('sols', '✅ الحلول'), ('recall', '🧠 الاسترجاع')]]), 'small')
    return ('<section class="chapter" id="map"><div class="ts-head ts-plain"><div class="top"><h2>🗺️ المتتبع والخطة</h2></div></div>'
            + '<h3>شجرة دكتورك = نفس الأسئلة الأربعة</h3>' + doc
            + '<h3>📍 أسئلة موسى الـ12 (بترتيب المذاكرة)</h3>' + tracker
            + '<h3>📋 الخطة</h3>' + plan + short + '</section>')


def page_tools():
    d = arith(r"(\tan x)'=\sec^{2}x\qquad (\sec x)'=\sec x\tan x", [(D(TAN), 'sec(x)**2'), (D(SEC), 'sec(x)*tan(x)')], 'tool d')
    ident = arith(r'\begin{gathered}\sin^{2}x+\cos^{2}x=1\\ \Big\downarrow\ \div\cos^{2}x\\ \tan^{2}x+1=\sec^{2}x\end{gathered}',
                  [('tan(x)**2+1', 'sec(x)**2'), ('(sin(x)**2+cos(x)**2)/cos(x)**2', 'tan(x)**2+1')], 'tool ident')
    two = arith(r'\begin{gathered}\sec^{2}x=1+\tan^{2}x\\ \tan^{2}x=\sec^{2}x-1\end{gathered}', [('sec(x)**2', '1+tan(x)**2'), ('tan(x)**2', 'sec(x)**2-1')], 'tool two')
    ints = arith(r'\begin{aligned}&\int\sec^{2}x\,dx=\tan x &&\int\sec x\tan x\,dx=\sec x\\'
                 r'&\int\tan x\,dx=-\ln|\cos x|=\ln|\sec x| &&\int\sec x\,dx=\ln|\sec x+\tan x|\end{aligned}',
                 [(D(TAN), 'sec(x)**2'), (D(SEC), 'sec(x)*tan(x)'), (D('-log(cos(x))'), 'tan(x)'), (D('log(sec(x))'), 'tan(x)'),
                  (D('log(sec(x)+tan(x))'), 'sec(x)')], 'tool ints')
    why_tan = arith(r'\int\tan x\,dx=\int\frac{\sin x}{\cos x}dx,\quad u=\cos x,\ du=-\sin x\,dx\ \Rightarrow\ -\ln|\cos x|',
                    [('tan(x)', 'sin(x)/cos(x)'), (D('cos(x)'), '-sin(x)'), (D('-log(cos(x))'), 'tan(x)')], 'tool why tan')
    why_sec = arith(r'\int\sec x\cdot\frac{\sec x+\tan x}{\sec x+\tan x}dx,\quad u=\sec x+\tan x,\ du=(\sec x\tan x+\sec^{2}x)\,dx\ \Rightarrow\ \ln|u|',
                    [(D('sec(x)+tan(x)'), 'sec(x)*tan(x)+sec(x)**2'), ('sec(x)*(sec(x)+tan(x))', 'sec(x)*tan(x)+sec(x)**2')], 'tool why sec')
    howmany = table(['الباقي بعد الحجز', 'يصير', 'أس القوس'], [
        [mi(r'\sec^{2}x'), mi(r'1+\tan^{2}x'), '1'], [mi(r'\sec^{4}x'), mi(r'(1+\tan^{2}x)^{2}'), '2'], [mi(r'\sec^{6}x'), mi(r'(1+\tan^{2}x)^{3}'), '3'],
        [mi(r'\tan^{2}x'), mi(r'\sec^{2}x-1'), '1'], [mi(r'\tan^{4}x'), mi(r'(\sec^{2}x-1)^{2}'), '2']], 'howmany')
    arith('', [('sec(x)**4', '(1+tan(x)**2)**2'), ('sec(x)**6', '(1+tan(x)**2)**3'), ('tan(x)**4', '(sec(x)**2-1)**2')], 'tool howmany')
    alg = arith(r'\begin{gathered}(1+u^{2})^{2}=1+2u^{2}+u^{4}\\ (u^{2}-1)^{2}=u^{4}-2u^{2}+1\\ (1+u^{2})^{3}=1+3u^{2}+3u^{4}+u^{6}\\ u^{a}\cdot u^{b}=u^{a+b}\end{gathered}',
                [('(1+u**2)**2', '1+2*u**2+u**4'), ('(u**2-1)**2', 'u**4-2*u**2+1'), ('(1+u**2)**3', '1+3*u**2+3*u**4+u**6'), ('u**2*u**3', 'u**5')], 'tool alg')
    frac = arith(r'\int u^{1/2}\,du=\frac{u^{3/2}}{3/2}=\frac23u^{3/2}\qquad \frac12+2=\frac52',
                 [('integrate(u**Rational(1,2),u)', '2*u**Rational(3,2)/3'), ('Rational(1,2)+2', 'Rational(5,2)')], 'tool frac')
    ang = arith(r'\begin{gathered}u=\tan3x\ \Rightarrow\ du=3\sec^{2}3x\,dx\\ \Rightarrow\ \sec^{2}3x\,dx=\tfrac13\,du\end{gathered}', [(D('tan(3*x)'), '3*sec(3*x)**2')], 'tool angle')
    return ('<section class="chapter" id="tools"><div class="ts-head ts-plain"><div class="top"><h2>🧰 الأدوات: 3 أشياء تحفظها، والباقي تطلعه منها</h2></div></div>'
            + '<div class="toolgrid">'
            + sbox('١. المشتقتين = القاعدتين', md(d) + p(rich('اللي تحجزه هو $du$: مع $u=\\tan x$ تحجز $\\sec^2x$، ومع $u=\\sec x$ تحجز $\\sec x\\tan x$.')))
            + sbox('٢. متطابقة وحدة (ومن وين جت)', md(ident) + md(two) + p(rich('<b>احفظها كذا:</b> $\\sec^2$ هو الكبير، فهو $1+\\tan^2$.')))
            + '</div>'
            + sbox('٣. أربع تكاملات تحفظها', md(ints)
                   + p(rich('💡 موسى حاط $\\int\\sec x\\,dx$ و $\\int\\tan x\\,dx$ كأسئلة (ص 98 (1) و (5)). لو انسألت عنها، هذي طريقتها:'), 'small')
                   + md(why_tan) + md(why_sec))
            + '<div class="toolgrid">'
            + sbox('٤. كم قوس؟', howmany + p(rich('أس القوس = الباقي ÷ 2.'), 'small'))
            + sbox('٥. جبر تحتاجه', md(alg) + p(rich('<b>الأس الكسري:</b> «زد 1 واقلب»'), 'small') + md(frac)
                   + p(rich('<b>مع زاوية:</b> يطلع رقمها في $du$'), 'small') + md(ang))
            + '</div></section>')


def qblock(k):
    qt, where, r, f, F, Ft, kd, who = Q[k]
    head = kind(kd) + ' <span class="src">%s%s</span>' % (musa(k), (' · محلول عند ' + who) if who and kd == 'worked' else '')
    sol = link('s-' + k, 'الحل الكامل ص ' + pgref('s-' + k), 'btn')
    total = {'S1': '4', 'S2': '3+4', 'S3': r'\tfrac12+4', 'T1': '5+5', 'T2': '5+1', 'L1': '2', 'L2': '3', 'L3': '4', 'L4': '6',
             'P1': '3', 'P2': '5', 'P3': '4+3'}[k]
    head += ' <span class="predict">' + rich('🔮 توقّع: أكبر أس في الجواب $=%s-1$' % total) + '</span>'
    predict = ''
    if kd == 'worked':
        return sbox(head, md(qt) + predict + steps(ROWS[k], 'worked ' + k), 'worked', 'q-' + k)
    if kd == 'fill':
        extra = ''
        if k == 'L3':
            extra = p(rich('بعد ما تعبّيها، قارن مع حل دكتورك (محاضرة 15، مثال 5).'), 'small')
        return sbox(head, md(qt) + predict + '<ol class="fill">' + ''.join('<li>%s</li>' % mi(r'\displaystyle ' + t) for t in FILL[k])
                    + '</ol>' + extra + p(sol), 'fill', 'q-' + k)
    hint = {'T2': rich('💡 sec أسه 1: بعد ما تحجز $\\sec x\\tan x$ ما يبقى sec. يبقى $\\tan^4=(\\sec^2-1)^2$ بس.'),
            'L4': rich('💡 نفس حركة $\\tan^4$ مرة زيادة. وتأكد بالسلسلة (فوق).'),
            'P3': rich('⭐⭐⭐ <b>أطول سؤال في الباب، وما جا في أي اختبار من الـ12.</b> حوّل كل tan لـ sec، ثم حركة $\\sec^5$ ثلاث مرات. '
                       'واجب دكتورك $\\int\\tan^2x\\sec^3x\\,dx$ (محاضرة 16) نفس الفكرة وأقصر. 📄 <b>حلها على ورقة لحالها.</b>')}.get(k, '')
    space = '' if k == 'P3' else lines({'L4': 3}.get(k, 4), 'write tight')
    return sbox(head, md(qt) + p(hint, 'small') + predict + space + p(sol), kd, 'q-' + k)


def check_block(r, qs, done=''):
    out = ''
    for n, (qt, F, f, tag) in enumerate(qs, 1):
        antideriv(F, f, 'check %s %d' % (r, n))
        t = (' <span class="src">%s</span>' % tag) if tag else ''
        out += '<div class="ch"><b>%d</b>%s%s%s</div>' % (n, t, md(qt), lines(CHECK_LINES[r], 'write tight'))
    return sbox('✅ فحص صغير: صح الاثنين؟ كمّل. غلط؟ ارجع للمحلول (الأجوبة في المفتاح ص %s)' % pgref('key'), '<div class="chgrid">' + out + '</div>' + ('<div class="ts-done">%s</div>' % done if done else ''), 'check')


CHECK_LINES = {'S': 2, 'T': 4, 'L': 2, 'P': 2}
CHECKS = {
    'S': [(r'\int\tan^{2}x\sec^{4}x\,dx', 'tan(x)**3/3+tan(x)**5/5', 'tan(x)**2*sec(x)**4', '📝 اختبار ثاني 1445'),
          (r'\int\sec^{6}x\,dx', 'tan(x)+2*tan(x)**3/3+tan(x)**5/5', 'sec(x)**6', '')],
    'T': [(r'\int\sec^{3}x\tan^{3}x\,dx', 'sec(x)**5/5-sec(x)**3/3', 'sec(x)**3*tan(x)**3', '📝 اختبار ثاني 1447'),
          (r'\int\tan^{3}x\sec x\,dx', 'sec(x)**3/3-sec(x)', 'tan(x)**3*sec(x)', '')],
    'L': [(r'\int\tan^{5}x\,dx', 'tan(x)**4/4-tan(x)**2/2+log(sec(x))', 'tan(x)**5', ''),
          (r'\int\tan^{2}2x\,dx', 'tan(2*x)/2-x', 'tan(2*x)**2', '')],
    'P': [(r'\int\tan^{2}x\sec x\,dx', 'sec(x)*tan(x)/2-log(sec(x)+tan(x))/2', 'tan(x)**2*sec(x)', '💡 حوّل tan'),
          (r'\int\sec^{3}2x\,dx', 'sec(2*x)*tan(2*x)/4+log(sec(2*x)+tan(2*x))/4', 'sec(2*x)**3', '')]}
CHECK_KEYS = {
    'S': [r'\frac13\tan^{3}x+\frac15\tan^{5}x+c', r'\tan x+\frac23\tan^{3}x+\frac15\tan^{5}x+c'],
    'T': [r'\frac15\sec^{5}x-\frac13\sec^{3}x+c', r'\frac13\sec^{3}x-\sec x+c'],
    'L': [r'\frac14\tan^{4}x-\frac12\tan^{2}x+\ln|\sec x|+c', r'\frac12\tan2x-x+c'],
    'P': [r'\frac12\sec x\tan x-\frac12\ln|\sec x+\tan x|+c', r'\frac14\sec2x\tan2x+\frac14\ln|\sec2x+\tan2x|+c']}

METHOD = {
    'S': ['<b>احجز</b> $\\cD{\\sec^2x\\,dx}$ واكتبها آخر شي.', '<b>حوّل</b> الباقي من sec بـ $\\sec^2=1+\\tan^2$ (جدول «كم قوس؟»).',
          '<b>let</b> $\\cU{u=\\tan x}$، و $du=\\sec^2x\\,dx$ (هي القطعة الخضرا).', '<b>بدّل</b> كل قطعة بـ $u$ (سطر 🔁).', '<b>فك القوس</b> ووزّع، ثم كامل كل حد.', '<b>رجّع</b> $\\tan x$، وافحص: أكبر أس = المجموع − 1.'],
    'T': ['<b>احجز</b> $\\cD{\\sec x\\tan x\\,dx}$ (وحدة sec ووحدة tan).', '<b>حوّل</b> الباقي من tan (صار زوجي) بـ $\\tan^2=\\sec^2-1$.',
          '<b>let</b> $\\cU{u=\\sec x}$، و $du=\\sec x\\tan x\\,dx$ (هي القطعة الخضرا).', '<b>بدّل</b> كل قطعة بـ $u$ (سطر 🔁).', '<b>فك القوس</b> ووزّع، ثم كامل.', '<b>رجّع</b> $\\sec x$، وافحص.'],
    'L': ['<b>قص</b> $\\tan^2x=\\sec^2x-1$ من السؤال.', '<b>وزّع:</b> قطعة فيها $\\sec^2x$ (تنحل بـ $u=\\tan x$)، وقطعة tan بأس أقل بـ 2.',
          '<b>كرر</b> على القطعة الثانية لين توصل $\\tan^2$ (جوابها $\\tan x-x$) أو $\\tan$ (جوابها $\\ln|\\sec x|$).'],
    'P': ['⚠️ <b>$u$ هنا معناها شي ثاني:</b> القطعة اللي نشتقها، و $dv$ اللي نكاملها (مو تعويض).', '<b>خل</b> $dv=\\sec^2x\\,dx$، و $u$ = باقي الـ sec.', '<b>$uv-\\int v\\,du$</b>، وحوّل $\\tan^2=\\sec^2-1$ ووزّع.',
          '<b>$I$ يرجع لك:</b> انقله للطرف الثاني، واقسم <b>كل</b> الحدود.', 'tan زوجي مع sec فردي؟ حوّل كل tan لـ sec أول.',
          '✍️ <b>في الكويز:</b> اكتب التجزئة كاملة مثل دكتورك. «نص ونص» تحفظها بس عشان تتأكد من جوابك.'],
}
DONE = {'S': 'خلصت القسم ١! هذا أكثر شي جا في الاختبارات. علّم ☐ وكمّل للقسم ٢.',
        'T': 'خلصت القسمين اللي جوا في الاختبارات القديمة 💪 علّم ☐.',
        'L': 'خلصت سلسلة tan. باقي قسم واحد.',
        'P': '🎉 خلصت الأقسام الأربعة! روح لـ «صحّح الغلط»، ثم الاختبار.'}


def page_rule(r):
    cls, anchor = RULES[r][0], RULES[r][1]
    method = '<ol class="ts-steps">' + ''.join('<li>%s</li>' % rich(t) for t in METHOD[r]) + '</ol>'
    extra = ''
    if r == 'L':
        chain = arith(r'\int\tan^{6}x\,dx:\quad 5,\ 3,\ 1\ \Rightarrow\ \frac{\tan^{5}x}{5}-\frac{\tan^{3}x}{3}+\frac{\tan x}{1}-x+c',
                      [(D('tan(x)**5/5-tan(x)**3/3+tan(x)-x'), 'tan(x)**6')], 'chain tan6')
        extra = ('<div class="tip">' + rich('⚡ <b>سلسلة tan (نفس اللي في المذكرة الكبيرة): تأكد فيها من جوابك</b><br>'
                                            'الأسس تبدأ من (أس السؤال − 1) وتنزل 2 2 · كل حد على أسه · الإشارات تتبادل $+\\ -\\ +$ · '
                                            'وآخر حد (بالإشارة اللي عليها الدور): $x$ إذا أس السؤال زوجي، و $\\ln|\\sec x|$ إذا فردي.') + md(chain) + '</div>')
    if r == 'L':
        body = method + extra + ''.join(qblock(k) for k in ORDER if Q[k][2] == r) + check_block(r, CHECKS[r], DONE[r])
    else:
        body = method + ''.join(qblock(k) for k in ORDER if Q[k][2] == r) + extra + check_block(r, CHECKS[r], DONE[r])
    return '<section class="chapter %s" id="%s">' % (cls, anchor) + rule_head(r) + body + '</section>'


MISTAKES = [  # (where, wrong (sympy), wrong latex, why, right (sympy), right latex, integrand or None)
    (r'\sec^{2}x=', '1-tan(x)**2', r'1-\tan^{2}x', 'هذي تشبه $\\sin^2=1-\\cos^2$ بس غلط هنا. $\\sec^2$ هو الكبير.', '1+tan(x)**2', r'1+\tan^{2}x', None),
    (r'\int\sec^{2}x\,dx=', 'sec(x)**3/3', r'\frac13\sec^{3}x', 'قاعدة القوة تحتاج $du$ جنبها، وما فيه. هذي من الأربع اللي تحفظها.', 'tan(x)', r'\tan x+c', 'sec(x)**2'),
    (r'\tan^{4}x=', 'sec(x)**4-1', r'\sec^{4}x-1', 'المتطابقة تحوّل $\\tan^2$ بس. $\\tan^4=(\\tan^2)^2$: تحوّل داخل القوس، والقوس يبقى مربع.',
     '(sec(x)**2-1)**2', r'(\sec^{2}x-1)^{2}', None),
    (r'u=\tan x\ \Rightarrow\ du=', 'sec(x)', r'\sec x\,dx', 'مشتقة $\\tan x$ هي $\\sec^2x$. فلازم تحجز <b>اثنين</b> sec، مو وحدة.', 'sec(x)**2', r'\sec^{2}x\,dx', None),
    (r'\int\tan x\,dx=', 'log(cos(x))', r'\ln|\cos x|', 'نسيت سالب $du=-\\sin x\\,dx$.', '-log(cos(x))', r'-\ln|\cos x|=\ln|\sec x|+c', 'tan(x)'),
    (r'2I=\sec x\tan x+\ln|\sec x+\tan x|\ \Rightarrow\ I=', 'sec(x)*tan(x)/2+log(sec(x)+tan(x))', r'\frac12\sec x\tan x+\ln|\sec x+\tan x|',
     'قسمت أول حد بس. لازم تقسم <b>كل</b> الحدود على 2.', 'sec(x)*tan(x)/2+log(sec(x)+tan(x))/2', r'\frac12\sec x\tan x+\frac12\ln|\sec x+\tan x|+c',
     'sec(x)**3')]


def page_fix():
    rows = ''
    for k, (qq, wrong, wrong_tex, why, right, right_tex, f) in enumerate(MISTAKES, 1):
        a, b = P(wrong), P(right)
        if f:
            arith('', [(D(right), f)], 'mistake %d right' % k)
            a, b = sp.diff(a, x), sp.diff(b, x)
        diff = [abs(complex((a - b).subs({x: v, u: v}).evalf())) for v in (0.3, 0.7)]
        if max(diff) < 1e-9:
            raise BuildError('mistake %d: the wrong version is not wrong' % k)
        rows += ('<div class="fix"><b>%d.</b> %s<div class="fixq">🔍 وين الغلط؟</div><div class="fixa">%s %s</div></div>'
                 % (k, mi(qq + r'\ \cR{' + wrong_tex + '}'), p('<b>الجواب:</b> ' + rich(why)), md(right_tex)))
    arith('', [('sec(x)**2', '1+tan(x)**2'), ('tan(x)**4', '(sec(x)**2-1)**2'), (D('tan(x)'), 'sec(x)**2')], 'mistakes right lines')
    return ('<section class="chapter" id="fix"><div class="ts-head ts-plain"><div class="top"><h2>🔍 صحّح الغلط: الأغلاط الست المشهورة</h2></div></div>'
            + p(rich('كل سطر أحمر فيه غلطة. غطِّ «الجواب» ولقها أول. الحاسوب تأكد إن كل «غلط» غلط فعلًا، وكل «صح» صح.')) + rows + '</section>')


TEST = [  # (question, rule, first line, answer latex, F, f)
    (r'\int\tan^{3}x\sec^{2}x\,dx', 'القسم ١ (أو ٢) · 📝 اختبار نهائي 1447', r'\tan^{3}x\cdot\sec^{2}x\,dx,\ u=\tan x',
     r'\frac14\tan^{4}x+c\quad(\text{or }\tfrac14\sec^{4}x-\tfrac12\sec^{2}x+c)', 'tan(x)**4/4', 'tan(x)**3*sec(x)**2'),
    (r'\int\tan^{5}x\sec^{3}x\,dx', 'القسم ٢: sec فردي، tan فردي', r'(\sec^{2}x-1)^{2}\sec^{2}x\cdot\sec x\tan x\,dx,\ u=\sec x',
     r'\frac17\sec^{7}x-\frac25\sec^{5}x+\frac13\sec^{3}x+c', 'sec(x)**7/7-2*sec(x)**5/5+sec(x)**3/3', 'tan(x)**5*sec(x)**3'),
    (r'\int\tan^{4}x\sec^{6}x\,dx', 'القسم ١', r'\tan^{4}x(1+\tan^{2}x)^{2}\sec^{2}x\,dx,\ u=\tan x',
     r'\frac15\tan^{5}x+\frac27\tan^{7}x+\frac19\tan^{9}x+c', 'tan(x)**5/5+2*tan(x)**7/7+tan(x)**9/9', 'tan(x)**4*sec(x)**6'),
    (r'\int\sec^{4}3x\,dx', 'القسم ١ بزاوية', r'(1+\tan^{2}3x)\sec^{2}3x\,dx,\ u=\tan3x,\ du=3\sec^{2}3x\,dx',
     r'\frac13\tan3x+\frac19\tan^{3}3x+c', 'tan(3*x)/3+tan(3*x)**3/9', 'sec(3*x)**4'),
    (r'\int\tan^{3}x\sqrt{\sec x}\,dx', 'القسم ٢ بأس كسري', r'(\sec^{2}x-1)\sec^{-1/2}x\cdot\sec x\tan x\,dx,\ u=\sec x',
     r'\frac25\sec^{5/2}x-2\sec^{1/2}x+c', '2*sec(x)**Rational(5,2)/5-2*sqrt(sec(x))', 'tan(x)**3*sqrt(sec(x))'),
    (r'\int\tan^{7}x\,dx', 'القسم ٣: سلسلة tan', r'\tan^{5}x(\sec^{2}x-1)\,dx',
     r'\frac16\tan^{6}x-\frac14\tan^{4}x+\frac12\tan^{2}x-\ln|\sec x|+c', 'tan(x)**6/6-tan(x)**4/4+tan(x)**2/2-log(sec(x))', 'tan(x)**7'),
    (r'\int\tan x\sec^{4}x\,dx', 'القسم ١ أو ٢ (الاثنين صح)', r'\sec^{3}x\cdot\sec x\tan x\,dx,\ u=\sec x',
     r'\frac14\sec^{4}x+c\quad(\text{or }\tfrac12\tan^{2}x+\tfrac14\tan^{4}x+c)', 'sec(x)**4/4', 'tan(x)*sec(x)**4'),
    (r'\int\sec^{8}x\,dx', 'القسم ١ (قوس تكعيب)', r'(1+\tan^{2}x)^{3}\sec^{2}x\,dx,\ u=\tan x',
     r'\tan x+\tan^{3}x+\frac35\tan^{5}x+\frac17\tan^{7}x+c', 'tan(x)+tan(x)**3+3*tan(x)**5/5+tan(x)**7/7', 'sec(x)**8'),
    (r'\int\sec^{5}x\tan x\,dx', 'القسم ٢ (أسرع سؤال)', r'\sec^{4}x\cdot\sec x\tan x\,dx,\ u=\sec x', r'\frac15\sec^{5}x+c', 'sec(x)**5/5', 'sec(x)**5*tan(x)'),
    (r'\int(\tan x+\sec x)^{2}\,dx', 'فك المربع، ثم الأربع تكاملات', r'\tan^{2}x+2\sec x\tan x+\sec^{2}x',
     r'2\tan x+2\sec x-x+c', '2*tan(x)+2*sec(x)-x', '(tan(x)+sec(x))**2')]


def page_test():
    qs = ''
    for k, (qt, br, first, ans, F, f) in enumerate(TEST, 1):
        antideriv(F, f, 'test %d' % k)
        qs += '<div class="ch"><b>%d</b>%s%s</div>' % (k, md(qt), lines(3, 'write tight'))
    arith('', [('diff(sec(x)**4/4,x)', 'diff(tan(x)**2/2+tan(x)**4/4,x)'), ('diff(sec(x)**4/4-sec(x)**2/2,x)', 'tan(x)**3*sec(x)**2')], 'test other routes')
    return ('<section class="chapter" id="test"><div class="ts-head ts-plain"><div class="top"><h2>📝 اختبار الإتقان: 10 أسئلة جديدة</h2></div></div>'
            + p(rich('<b>الجولة الأولى:</b> اكتب تحت كل سؤال <b>القسم وأول سطر</b> بس. <b>الجولة الثانية:</b> حلها كاملة. '
                     '8 من 10 صح = أتقنته. ') + link('key', 'المفتاح ص ' + pgref('key')) + '.')
            + '<div class="chgrid">' + qs + '</div></section>')


def page_key():
    items = ''.join('<li><b>%d. %s</b><div>أول سطر: %s</div><div>الجواب: %s</div></li>'
                    % (k, rich(br), mi(r'\displaystyle ' + first), mi(r'\displaystyle ' + ans))
                    for k, (qt, br, first, ans, F, f) in enumerate(TEST, 1))
    checks = ''
    for r in ('S', 'T', 'L', 'P'):
        checks += '<li><b>القسم %s</b>%s</li>' % (RULES[r][2], ''.join('<div>(%d) %s</div>' % (n, mi(r'\displaystyle ' + a))
                                                                     for n, a in enumerate(CHECK_KEYS[r], 1)))
    fills = ''
    for k in ('S3', 'L3', 'P2'):
        fills += '<li><b>%s</b>%s</li>' % (mi(Q[k][0]), ''.join('<div>(%d) %s</div>' % (n, mi(r'\displaystyle ' + a)) for n, a in enumerate(FILL_KEY[k], 1)))
    return ('<section class="chapter" id="key"><div class="ts-head ts-plain"><div class="top"><h2>🔑 المفتاح</h2></div></div>'
            + '<h3>اختبار الإتقان: القسم، وأول سطر، والجواب</h3><ol class="keylist">' + items + '</ol>'
            + p(rich('جوابك شكله غير؟ اشتقه: إذا رجع السؤال فهو صح. والفرق بثابت عادي لما القسمين ينفعون.'), 'small')
            + '<h3>الفحوص الصغيرة</h3><ul class="keylist">' + checks + '</ul>'
            + '<h3>الفراغات (بالترتيب)</h3><ul class="keylist two">' + fills + '</ul>'
            + '<h3>🔑 صفحة u و du: جرّب</h3><ul class="keylist two">' + ''.join('<li>%s</li>' % rich(t) for t in UDU_KEY) + '</ul></section>')


def page_sols():
    out = ''
    for k in ('S3', 'T2', 'L3', 'L4', 'P2', 'P3'):
        out += ('<div class="sol" id="s-%s"><div class="drill-head"><b>%s</b> %s %s</div>%s</div>'
                % (k, musa(k), mi(r'\displaystyle ' + Q[k][0]), link('q-' + k, '↩ رجوع', 'back btn'), steps(ROWS[k], 'sol ' + k)))
    return ('<section class="chapter" id="sols"><div class="ts-head ts-plain"><div class="top"><h2>✅ حلول أسئلة موسى اللي ما انحلت (6)</h2></div></div>'
            + p(rich('المحلولة (عند موسى أو دكتورك أو هنا) في أقسامها. وهذي الباقية بنفس الأسلوب: $I=$ في كل سطر، و«ليش؟» لكل خطوة.'), 'small') + out + '</section>')


def recall():
    prompts = [('الأسئلة الأربعة بالترتيب، ووش تسوي في كل وحدة.', 'start'),
               ('let $u$ و $du$ (الشكلين)، والمتطابقة ومن وين جت.', 'udu'),
               ('التكاملات الأربعة: $\\sec^2$، و $\\sec\\tan$، و $\\tan$، و $\\sec$.', 'tools'),
               ('أول 3 أسطر في $\\int\\sec^3x\\,dx$، وجوابها «نص ونص».', 'q-P1'),
               ('سلسلة tan: الأسس، والإشارات، وآخر حد.', 'secL'),
               ('فحص أكبر أس هنا، وفي sin و cos.', 'start')]
    rows = ''.join('<div class="ch"><b>%d</b>%s%s%s</div>' % (k, p(rich(t)), lines(4, 'write tight'), p(link(a, 'الجواب ص ' + pgref(a)), 'small'))
                   for k, (t, a) in enumerate(prompts, 1))
    return ('<section class="chapter" id="recall"><div class="ts-head ts-plain"><div class="top"><h2>🧠 استرجاع قبل الكويز (اكتب من راسك، ثم شيك)</h2></div></div>'
            + p(rich('في الكويز، أول 3 أسطر (الكسرة، والتحويل، و $u$ و $du$) عليها درجات حتى لو ما كملت. هذي الصفحة تثبّتها.'))
            + '<div class="chgrid">' + rows + '</div></section>')


def build():
    check_all()
    body = (page_start() + page_udu() + page_map() + page_tools() + ''.join(page_rule(r) for r in ('S', 'T', 'L', 'P'))
            + page_fix() + page_test() + page_key() + page_sols() + recall())
    return '<main class="ts">' + body + '</main>'


OUTLINE = [[1, '🚪 ابدأ هنا', ['start']], [1, '🔑 u و du', ['udu']], [1, '🗺️ المتتبع والخطة', ['map']], [1, '🧰 الأدوات', ['tools']],
           [1, '١. أس sec زوجي', ['secS']], [1, '٢. tan فردي ومعه sec', ['secT']], [1, '٣. سلسلة tan', ['secL']],
           [1, '٤. تجزئة', ['secP']], [1, '🔍 صحّح الغلط', ['fix']], [1, '📝 اختبار الإتقان', ['test']], [1, '🔑 المفتاح', ['key']],
           [1, '✅ الحلول', ['sols']], [1, '🧠 الاسترجاع', ['recall']]]

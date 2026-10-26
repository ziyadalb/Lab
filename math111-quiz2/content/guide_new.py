"""المذكرة الكاملة — الحالات الجديدة (من فروق محاضرات الدكتور): الاشتقاق اللوغاريتمي، 3.4 أم 4.2؟،
البسط بدلالة الداخل، خواص ln أول، cosh أو sinh لحالها في المقام.

Each case is short (about 2.5 pages): when, why, the method script with one trick, one worked example, the trap,
what to write, a quick check, the one-line summary, and two or three exercises with full solutions.
Every formula, step and answer is checked while building. Colour macros in the LaTeX: \\cU{} 🔵 u (the inside),
\\cD{} 🟢 du (the derivative of the inside), \\cA{} 🟠 the adjustment number, \\cR{} 🔴 a minus sign or a danger.
"""
import sympy as s

from booklet_engine import ITEMS, arith, formula, functional
from guide_kit import Unit, contrast, final, method, question, rich, steps
from html_kit import md, mi, p, table, ul
from mathlib import x


def _eq(pair):
    return md(pair[0] + ' = ' + pair[1])


# ---------------------------------------------------------------- الاشتقاق اللوغاريتمي
def u_logdiff():
    U = Unit('U-LD', 'الاشتقاق اللوغاريتمي: x في الأساس وفي الأس', '4.2', 'من مذكرة د. موسى', 0)
    U.add('idea', 'ليش تشتغل؟', p(rich(
        'قاعدة القوة تبي الأس رقم، وقانون $a^u$ يبي الأساس رقم، فـ $x^{x}$ ما لها قانون. '
        'لكن ln ينزّل الأس قدّام ($\\ln A^{b}=b\\ln A$)، فيصير ضرب عادي نشتقه.')))
    arith('', [('diff(3**(x**2),x)', '3**(x**2)*log(3)*2*x'), ('diff((x**2+1)**5,x)', '5*(x**2+1)**4*2*x')], 'U-LD contrast')
    U.add('sign', 'متى؟', p(rich('<b>إذا شفت:</b> المطلوب مشتقة، و $x$ في الأساس وفي الأس مع بعض، مثل $x^{3x^2}$ أو $(x^2+1)^{x}$.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> الأس رقم (قاعدة القوة)، أو الأساس رقم مثل $3^{x^2}$ (قانون $a^u$).'))
          + contrast([(r'y=x^{3x^{2}}', 'اشتقاق لوغاريتمي: ln للطرفين', 'الأساس والأس فيهم $x$'),
                      (r'y=3^{x^{2}}', "قانون $a^u$: $3^{x^2}\\ln3\\cdot2x$", 'الأساس رقم'),
                      (r'y=\left(x^{2}+1\right)^{5}', 'قاعدة القوة: $5(x^2+1)^4\\cdot2x$', 'الأس رقم')]))
    au = formula('a**u', 'a**u*log(a)', 'diff', branches=('x',), pos=('a',), uprime=True, label='U-LD a^u')
    functional(lambda: s.diff(s.log(s.Function('f')(x)), x) - s.diff(s.Function('f')(x), x) / s.Function('f')(x), 'U-LD ln y')
    laws = (md(arith(r'\ln A^{b}=b\ln A,\qquad \left(\ln y\right)^{\prime}=\frac{y^{\prime}}{y}', [('log(2**5)', '5*log(2)')], 'U-LD law'))
            + p(rich('وللمقارنة، الأساس رقم: ') + mi(au[0] + ' = ' + au[1]), 'small'))
    U.add('short', '🧭 الخطوات', method([
        'وش الدالة اللي برّا؟ قوة، والأساس والأس فيهم $x$. فلا قاعدة القوة تنفع، ولا قانون $a^u$.',
        'خذ ln للطرفين، ونزّل الأس قدّام: يصير الأس مضروب في ln الأساس.',
        "اشتق الطرفين. اليسار $\\frac{y'}{y}$. واليمين قاعدة الضرب: مشتقة ln من الجدول، والداخل يبقى مثل ما هو، ثم 🟢 × مشتقة الداخل.",
        "بسّط، ثم 🔴 اضرب في $y$، وحط مكان $y$ الدالة الأصلية."],
        tricks_=[("الجواب دايم يبدأ بالدالة الأصلية: $\\left(x^{x}\\right)'=x^{x}\\left(\\ln x+1\\right)$.",
                  [('diff(x**x,x)', 'x**x*(log(x)+1)', 't')])], label='U-LD') + laws)

    it = ITEMS['MC-01']
    ex = question(it, 'U-LD example')
    ex += steps(it, [
        ('tex', r'\ln y=\ln x^{\cA{3x^{2}}}=\cA{3x^{2}}\ln x', [('log(x**(3*x**2))', '3*x**2*log(x)', 't')],
         'قوة، والأساس والأس فيهم $x$. فناخذ ln للطرفين، و 🟠 الأس ينزل قدّام.'),
        ('tex', r"\frac{y^{\prime}}{y}=6x\cdot\ln x+3x^{2}\cdot\frac{1}{x}", [('diff(3*x**2*log(x),x)', '6*x*log(x)+3*x**2/x', 't')],
         "نشتق الطرفين. اليسار $\\frac{y'}{y}$. اليمين ضرب: مشتقة الأولى × الثانية، زائد الأولى × مشتقة الثانية."),
        ('tex', r"\frac{y^{\prime}}{y}=3x+6x\ln x", [('6*x*log(x)+3*x**2/x', '3*x+6*x*log(x)', 't')], 'نبسّط: $3x^2\\cdot\\frac1x=3x$.'),
        ('line', '(3*x+6*x*log(x))*x**(3*x**2)', '🔴 نضرب الطرفين في $y$، ونحط مكان $y$ الدالة الأصلية $x^{3x^2}$.')], 'U-LD ex')
    ex += final(it, 'U-LD example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. موسى)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('أكبر غلطة: تنسى تضرب في $y$ في الآخر. الجواب لازم يبدأ بالدالة الأصلية.'),
                                rich('لا تستعمل قاعدة القوة والأس فيه $x$: $\\left(x^{x}\\right)^{\\prime}$ مو $x\\cdot x^{x-1}$.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r"\ln y=3x^{2}\ln x\ \Rightarrow\ \frac{y^{\prime}}{y}=3x+6x\ln x",
                   [('log(x**(3*x**2))', '3*x**2*log(x)', 't'), ('diff(3*x**2*log(x),x)', '3*x+6*x*log(x)', 't')], 'U-LD paper 1'))
          + md(arith(r"y^{\prime}=\left(3x+6x\ln x\right)x^{3x^{2}}", [('diff(x**(3*x**2),x)', '(3*x+6*x*log(x))*x**(3*x**2)', 't')], 'U-LD paper 2')))
    arith('', [('(3*1+6*1*log(1))*1**(3*1**2)', '3')], 'U-LD check')
    U.add('ok', '✔ تأكد', p(rich("عوّض $x=1$ في جواب المثال: $y'=(3+0)\\cdot1=3$، والدالة الأصلية لازم تكون موجودة في جوابك.")))
    U.gist('مشتقة، و $x$ في الأساس وفي الأس', 'ln للطرفين، والأس ينزل قدّام', "اشتق الطرفين، ثم اضرب في $y$")
    U.drill('1', 'MC-02', 'G', 'ln للطرفين: الأس $x$ ينزل قدّام.',
            first=r'\ln y=x\ln\left(x^{2}+1\right)', claims=[('log((x**2+1)**x)', 'x*log(x**2+1)')],
            sol_rows=[('tex', r"\frac{y^{\prime}}{y}=1\cdot\ln\left(x^{2}+1\right)+x\cdot\frac{\cD{2x}}{x^{2}+1}",
                       [('diff(x*log(x**2+1),x)', 'log(x**2+1)+x*2*x/(x**2+1)')],
                       'نشتق الطرفين. اليمين ضرب: مشتقة $x$ هي 1. ومشتقة $\\ln(x^2+1)$: 🟢 مشتقة الداخل $2x$ على الداخل.'),
                      ('line', '(x**2+1)**x*(log(x**2+1)+2*x**2/(x**2+1))', '🔴 نضرب في $y=(x^2+1)^x$. و $x\\cdot2x=2x^2$.')])
    U.drill('2', 'MC-04', 'I', 'ln للطرفين: $\\ln y=\\sinh x\\,\\ln x$، ثم قاعدة الضرب.',
            sol_rows=[('tex', r'\ln y=\sinh x\,\ln x', [('log(x**sinh(x))', 'sinh(x)*log(x)', 't')],
                       'الأساس والأس فيهم $x$. ناخذ ln للطرفين، والأس $\\sinh x$ ينزل قدّام.'),
                      ('tex', r"\frac{y^{\prime}}{y}=\cosh x\,\ln x+\sinh x\cdot\frac{1}{x}", [('diff(sinh(x)*log(x),x)', 'cosh(x)*log(x)+sinh(x)/x', 't')],
                       'قاعدة الضرب: مشتقة $\\sinh x$ هي $\\cosh x$ (من 4.1)، ومشتقة $\\ln x$ هي $\\frac1x$.'),
                      ('line', 'x**sinh(x)*(cosh(x)*log(x)+sinh(x)/x)', '🔴 نضرب في $y$، ونحط $y=x^{\\sinh x}$.')])
    return U


# ---------------------------------------------------------------- 3.4 أم 4.2؟
def u_34():
    U = Unit('U-34', '3.4 أم 4.2؟ sin⁻¹ و tan⁻¹ و sec⁻¹ ضد الزائدية', '4.2', 'من الاختبارات ومذكرة د. موسى', 0)
    U.add('idea', 'ليش تشتغل؟', p(rich(
        'الجدولين شكلهم متقارب، والفرق إشارة وحدة ومكان $u$. فإذا كتبت المقام بالشكل الكامل ($a^2$ و $u^2$)، '
        'يبان لك القانون الصح من أول نظرة.')))
    U.add('sign', 'متى؟', p(rich('<b>إذا شفت:</b> تكامل فيه جذر أو مقام فيه $x^2$، خصوصًا $-x^2$ تحت الجذر، أو قوس مضروب برّا الجذر.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> فوق مشتقة اللي تحت كاملة، مثل $\\frac{2x}{\\sqrt{x^2+9}}$. هذا تعويض عادي، وجوابه جذر أو ln.'))
          + contrast([(r'\int\frac{dx}{\sqrt{9-\left(x+1\right)^{2}}}', '3.4: $\\sin^{-1}$', '$a^2-u^2$ تحت الجذر، و $u$ مو برّا'),
                      (r'\int\frac{dx}{\sqrt{\left(x+2\right)^{2}+9}}', '4.2: $\\sinh^{-1}$', '$u^2+a^2$ تحت الجذر'),
                      (r'\int\frac{dx}{\left(x-1\right)\sqrt{\left(x-1\right)^{2}-4}}', '3.4: $\\sec^{-1}$', '$u$ برّا الجذر، وتحت $u^2-a^2$')]))
    f = dict(
        asin=formula('1/sqrt(a**2-u**2)', 'asin(u/a)', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-34 asin'),
        atan=formula('1/(a**2+u**2)', 'atan(u/a)/a', branches=('x',), pos=('a',), label='U-34 atan'),
        asec=formula('1/(u*sqrt(u**2-a**2))', 'asec(u/a)/a', branches=('a+t',), pos=('a',), label='U-34 asec'),
        asinh=formula('1/sqrt(u**2+a**2)', 'asinh(u/a)', pos=('a',), label='U-34 asinh'),
        acosh=formula('1/sqrt(u**2-a**2)', 'acosh(u/a)', branches=('a+t',), pos=('a',), label='U-34 acosh'),
        atanh=formula('1/(a**2-u**2)', 'atanh(u/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-34 atanh'),
        asech=formula('1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-34 asech'),
        acsch=formula('1/(u*sqrt(a**2+u**2))', '-acsch(Abs(u)/a)/a', branches=('t', '-t'), pos=('a',), label='U-34 acsch'))
    cell = lambda k: mi(r'\displaystyle ' + f[k][1])
    rows = [[mi(r'\sqrt{a^{2}-u^{2}}'), cell('asin'), '—'],
            [mi(r'a^{2}+u^{2}') + ' بدون جذر', cell('atan'), '—'],
            [mi(r'u\sqrt{u^{2}-a^{2}}'), cell('asec'), '—'],
            [mi(r'\sqrt{u^{2}+a^{2}}'), '—', cell('asinh')],
            [mi(r'\sqrt{u^{2}-a^{2}}'), '—', cell('acosh')],
            [mi(r'a^{2}-u^{2}') + ' بدون جذر', '—', cell('atanh') + ' أو ' + mi(r'\coth^{-1}')],
            [mi(r'u\sqrt{a^{2}-u^{2}}'), '—', cell('asech')],
            [mi(r'u\sqrt{a^{2}+u^{2}}'), '—', cell('acsch')]]
    law = (table(['تحت (في المقام)', '3.4 مثلثية عكسية', '4.2 زائدية عكسية'], rows, 'formula compact')
           + p(rich('في الجدول: كل تكامل $\\int\\frac{du}{\\ldots}$، و $a$ رقم موجب. وقانون $\\sec^{-1}$ لـ $u>a$، مثل مذكرة د. طارق.'), 'small'))
    U.add('short', '🧭 الخطوات', method([
        '🔵 سمّ الداخل $u$: اكتب اللي تحت الجذر بـ $a^2$ و $u^2$. وإذا فيه $x^2$ و $x$، كمّل المربع، و $u$ = اللي داخل المربع.',
        '🟢 اشتقه: $du=\\ldots\\,dx$.',
        '🟠 اقسم اللي برّا على مشتقة الداخل: طلع رقم؟ هذا رقم التعديل، يطلع قدّام التكامل مرة وحدة بس.',
        'اكتب التكامل كله بـ $u$، وطبّق القانون. 3.4 أم 4.2؟ شوف الجدول تحت.',
        'رجّع $x$، وحط $+C$.'],
        tricks_=[('3.4 له ثلاثة أشكال بس: $\\sqrt{a^2-u^2}$، و $a^2+u^2$ بدون جذر، و $u\\sqrt{u^2-a^2}$. أي شكل غيرها؟ 4.2. '
                  'مثال: $\\left(\\sin^{-1}\\frac x3\\right)^{\\prime}=\\frac{1}{\\sqrt{9-x^2}}$، و $\\left(\\sinh^{-1}\\frac x3\\right)^{\\prime}=\\frac{1}{\\sqrt{x^2+9}}$.',
                  [('diff(asin(x/3),x)', '1/sqrt(9-x**2)', '3*t/(1+t)'), ('diff(asinh(x/3),x)', '1/sqrt(x**2+9)')])], label='U-34') + law)

    it = ITEMS['1446-S2-FE-Q2.1']
    ex = question(it, 'U-34 example')
    ex += steps(it, [
        ('tex', r'-x^{2}-2x+8=\cR{-}\left(x^{2}+2x\right)+8', [('-x**2-2*x+8', '-(x**2+2*x)+8')],
         '🔴 $x^2$ معها سالب. نطلّع السالب من حدود $x$ قبل إكمال المربع.'),
        ('tex', r'x^{2}+2x=\left(x+1\right)^{2}-1', [('x**2+2*x', '(x+1)**2-1')], 'نكمّل المربع: نص معامل $x$ هو 1، ومربعه 1. نضيفه ونطرحه.'),
        ('tex', r'-x^{2}-2x+8=-\left(x+1\right)^{2}+1+8=3^{2}-\cU{\left(x+1\right)}^{2}', [('-x**2-2*x+8', '3**2-(x+1)**2')],
         'السالب يدخل على القوس: $-(\\ldots-1)=-(\\ldots)+1$. و $1+8=9=3^2$.'),
        ('sub', 'x+1', '1', '🔵 $u=x+1$. 🟢 مشتقته 1، فما فيه رقم تعديل.'),
        ('tex', r'\int\frac{dx}{\sqrt{3^{2}-\left(x+1\right)^{2}}}=\int\frac{du}{\sqrt{3^{2}-u^{2}}}', [('1/sqrt(-x**2-2*x+8)', '1/sqrt(3**2-(x+1)**2)')],
         '$a^2-u^2$ تحت الجذر، و $u$ مو برّا الجذر: هذا أول شكل في 3.4.'),
        ('line', 'asin((x+1)/3)', 'القانون $\\sin^{-1}\\frac ua$ مع $a=3$. ونرجع $u=x+1$.')], 'U-34 ex')
    ex += final(it, 'U-34 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تختار بالاسم: $\\sqrt{9-u^2}$ تعطي $\\sin^{-1}$، و $\\sqrt{u^2+9}$ تعطي $\\sinh^{-1}$. الإشارة هي اللي تقرر.'),
                                rich('🔴 مع $-x^2$: طلّع السالب قبل إكمال المربع. $-x^2-2x=-(x^2+2x)$، مو $-(x^2-2x)$.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'-x^{2}-2x+8=9-\left(x+1\right)^{2},\qquad u=x+1,\quad du=dx',
                   [('-x**2-2*x+8', '9-(x+1)**2'), ('diff(x+1,x)', '1')], 'U-34 paper 1'))
          + md(arith(r'\int\frac{du}{\sqrt{3^{2}-u^{2}}}=\sin^{-1}\frac{x+1}{3}+C',
                     [('diff(asin((x+1)/3),x)', '1/sqrt(-x**2-2*x+8)', '-1+3*t/(1+t)'), ('diff(asin((x+1)/3),x)', '1/sqrt(-x**2-2*x+8)', '-1-3*t/(1+t)')],
                     'U-34 paper 2')))
    arith('', [('9-(x+1)**2', '-x**2-2*x+8')], 'U-34 check')
    U.add('ok', '✔ تأكد', p(rich('فك القوس اللي كتبته: $9-(x+1)^2=-x^2-2x+8$، لازم يرجع اللي تحت الجذر بالضبط.')))
    U.gist('جذر أو مقام فيه $x^2$، وما تدري 3.4 أو 4.2', 'اكتب المقام بـ $a^2$ و $u^2$ (وكمّل المربع إذا لزم)',
           '3.4 بس لـ $\\sqrt{a^2-u^2}$ و $a^2+u^2$ و $u\\sqrt{u^2-a^2}$، والباقي 4.2')
    U.drill('1', '1445-S1-FE-Q2.1', 'G', 'طلّع السالب، وكمّل المربع: نص 6 هو 3.',
            first=r'-x^{2}-6x=-\left(x^{2}+6x\right)=9-\left(x+3\right)^{2}', claims=[('-x**2-6*x', '-(x**2+6*x)'), ('-x**2-6*x', '9-(x+3)**2')],
            sol_rows=[('sub', 'x+3', '1', '🔵 صار $3^2-u^2$ تحت الجذر، و $u=x+3$. 🟢 مشتقته 1.'),
                      ('tex', r'\int\frac{2\,dx}{\sqrt{3^{2}-\left(x+3\right)^{2}}}=2\int\frac{du}{\sqrt{3^{2}-u^{2}}}',
                       [('2/sqrt(-x**2-6*x)', '2/sqrt(3**2-(x+3)**2)')], 'الرقم 2 يطلع برّا. و $a^2-u^2$ تحت الجذر: 3.4.'),
                      ('tex', r'=2\sin^{-1}\frac{u}{3}', [('diff(2*asin(x/3),x)', '2/sqrt(9-x**2)', '3*t/(1+t)')],
                       'القانون $\\sin^{-1}\\frac ua$ مع $a=3$. ونرجع $u=x+3$.')])
    U.drill('2', '1446-S1-FE-Q2.1', 'P', 'طلّع السالب من حدود $x$، ثم كمّل المربع، ثم شوف الشكل.',
            sol_rows=[('tex', r'-x^{2}+6x-8=-\left(x^{2}-6x\right)-8', [('-x**2+6*x-8', '-(x**2-6*x)-8')], '🔴 نطلّع السالب من حدود $x$.'),
                      ('tex', r'x^{2}-6x=\left(x-3\right)^{2}-9', [('x**2-6*x', '(x-3)**2-9')], 'نكمّل المربع: نص $-6$ هو $-3$، ومربعه 9.'),
                      ('tex', r'-x^{2}+6x-8=-\left(x-3\right)^{2}+9-8=1-\left(x-3\right)^{2}', [('-x**2+6*x-8', '1-(x-3)**2')],
                       'السالب يدخل: $-(\\ldots-9)=-(\\ldots)+9$. و $9-8=1$.'),
                      ('sub', 'x-3', '1', '🔵 $1^2-u^2$ تحت الجذر، و $u=x-3$.'),
                      ('line', '2*asin(x-3)', '3.4: $2\\sin^{-1}\\frac{u}{1}=2\\sin^{-1}(x-3)$.')])
    U.drill('3', 'MC-07', 'I', 'كمّل المربع، ولاحظ إن $x-2$ برّا الجذر.',
            sol_rows=[('tex', r'x^{2}-4x=\left(x-2\right)^{2}-2^{2}', [('x**2-4*x', '(x-2)**2-2**2')], 'نكمّل المربع: نص $-4$ هو $-2$، ومربعه 4.'),
                      ('sub', 'x-2', '1', '🔵 نسمّي $u=x-2$. ونفس $u$ مضروب برّا الجذر.'),
                      ('tex', r'\int\frac{5\,dx}{\left(x-2\right)\sqrt{\left(x-2\right)^{2}-2^{2}}}=5\int\frac{du}{u\sqrt{u^{2}-2^{2}}}',
                       [('5/((x-2)*sqrt(x**2-4*x))', '5/((x-2)*sqrt((x-2)**2-2**2))', '4+t')],
                       '$u$ برّا الجذر، وتحت $u^2-a^2$: هذا $\\sec^{-1}$ من 3.4.'),
                      ('line', '5*asec((x-2)/2)/2', 'القانون $\\frac1a\\sec^{-1}\\frac ua$ مع $a=2$، ونضرب في 5.')])
    return U


# ---------------------------------------------------------------- البسط بدلالة الداخل
def u_x2():
    U = Unit('U-X2', 'بقى x بعد التعويض: x² = u − a', '4.2', 'من مذكرة د. موسى', 0)
    U.add('idea', 'ليش تشتغل؟', p(rich(
        'بعد ما تسمّي $u$، لازم كل $x$ يتحول لـ $u$، وما ينفع تكامل وفيه الاثنين. '
        'فالـ $x$ اللي بقى نطلّعه من $u$ نفسه: من $u=x^2+3$ يطلع $x^2=u-3$.')))
    U.add('sign', 'متى؟', p(rich('<b>إذا شفت:</b> قوة فردية لـ $x$ برّا، مثل $x^3$، وداخل الجذر أو القوس $x^2+$ رقم. أو $x$ مضروب في $(1+x)^{n}$.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> برّا $x$ بس وداخل $x^2+$ رقم: تعويض مباشر، وما يبقى شي.'))
          + contrast([(r'\int\frac{x^{3}}{\left(3+x^{2}\right)^{5/2}}dx', 'تجهيز: $x^2=u-3$', 'بعد $x\\,dx=\\frac{du}{2}$ يبقى $x^2$'),
                      (r'\int\frac{x}{\left(3+x^{2}\right)^{5/2}}dx', 'تعويض مباشر', 'برّا $x$ بس، وهي نص مشتقة $3+x^2$'),
                      (r'\int x\left(1+x\right)^{1/3}dx', 'تجهيز: $x=u-1$', 'بعد $du=dx$ يبقى $x$')]))
    U.add('short', '🧭 الخطوات', method([
        'وش الشكل اللي يدلك؟ بعد ما تسمّي 🔵 $u$ وتعوّض 🟢 $du$، بقى $x$ (أو $x^2$) ما تحوّل.',
        'سوّ الحركة: طلّع اللي بقى من $u$ نفسه. $u=x^2+3$ يعني $x^2=u-3$. و $u=1+x$ يعني $x=u-1$.',
        'تأكد برقم إن الشكل الجديد يساوي القديم.',
        'ارجع للشجرة: الحين وش الطريقة؟ غالبًا توزّع، ثم قاعدة القوة حد حد.'],
        tricks_=[('افصل القوة الفردية: $x^3\\,dx=x^2\\cdot x\\,dx$. الـ $x\\,dx$ تروح لـ $du$، والـ $x^2$ تصير $u-3$. '
                  'تأكد برقم: $x=1$ يعطي $u=4$، و $u-3=1=x^2$.', [('x**3', 'x**2*x'), ('4-3', '1**2')])], label='U-X2'))

    it = ITEMS['MC-08']
    ex = question(it, 'U-X2 example')
    ex += steps(it, [
        ('sub', '3+x**2', '2*x', '🔵 نسمّي اللي تحت القوس $u=3+x^2$. 🟢 مشتقته $2x$.'),
        ('tex', r'x\,dx=\cA{\frac{1}{2}}\,du,\qquad x^{2}=u-3', [('diff(3+x**2,x)/2', 'x'), ('(3+x**2)-3', 'x**2')],
         '🟠 فوق $x\\,dx$ بدون 2، فنقسم على 2. وبقى $x^2$: نطلّعه من $u$ نفسه.'),
        ('tex', r'\int\frac{x^{2}\cdot x\,dx}{\left(3+x^{2}\right)^{5/2}}=\frac12\int\frac{u-3}{u^{5/2}}\,du',
         [('x**3/(3+x**2)**Rational(5,2)', 'Rational(1,2)*((3+x**2)-3)/(3+x**2)**Rational(5,2)*diff(3+x**2,x)')],
         'نفصل $x^3=x^2\\cdot x$، ونعوّض الاثنين. ما بقى ولا $x$.'),
        ('tex', r'=\frac12\int\left(u^{-3/2}-3u^{-5/2}\right)du', [('(x-3)/x**Rational(5,2)', 'x**Rational(-3,2)-3*x**Rational(-5,2)', 't')],
         'ارجع للشجرة: نوزّع. $\\frac{u}{u^{5/2}}=u^{-3/2}$، و $\\frac{3}{u^{5/2}}=3u^{-5/2}$.'),
        ('tex', r'=\frac12\left(\frac{u^{-1/2}}{-1/2}-3\cdot\frac{u^{-3/2}}{-3/2}\right)=-u^{-1/2}+u^{-3/2}',
         [('diff(-x**Rational(-1,2)+x**Rational(-3,2),x)', '(x**Rational(-3,2)-3*x**Rational(-5,2))/2', 't')],
         'قاعدة القوة: نزيد الأس 1 ونقسم عليه، ثم نضرب في $\\frac12$.'),
        ('line', '-1/sqrt(3+x**2)+1/(3+x**2)**Rational(3,2)', 'نرجع $u=3+x^2$.')], 'U-X2 ex')
    ex += final(it, 'U-X2 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. موسى)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تكامل وفيه $x$ و $u$ مع بعض. كل $x$ لازم يتحول قبل ما تكامل.'),
                                rich('🔴 إشارة الحركة: $u=x^2+3$ يعني $x^2=u-3$ (ناقص)، مو $u+3$.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'u=3+x^{2},\quad du=2x\,dx,\quad x^{2}=u-3\ \Rightarrow\ \frac12\int\left(u^{-3/2}-3u^{-5/2}\right)du',
                   [('diff(3+x**2,x)', '2*x'), ('(3+x**2)-3', 'x**2')], 'U-X2 paper 1'))
          + md(arith(r'=-\frac{1}{\sqrt{3+x^{2}}}+\frac{1}{\left(3+x^{2}\right)^{3/2}}+C',
                     [('diff(-1/sqrt(3+x**2)+1/(3+x**2)**Rational(3,2),x)', 'x**3/(3+x**2)**Rational(5,2)')], 'U-X2 paper 2')))
    U.add('ok', '✔ تأكد', p(rich('قبل ما تكامل، شوف السطر: لازم ما يبقى فيه ولا $x$.')))
    U.gist('بعد التعويض بقى $x$ أو $x^2$ زيادة', 'طلّعه من $u$: $x^2=u-3$، أو $x=u-1$', 'وزّع، وكامل حد حد بقاعدة القوة')
    U.drill('1', 'MC-09', 'P', 'نسمّي $u=1+x$، فـ $x=u-1$.',
            sol_rows=[('sub', '1+x', '1', '🔵 نسمّي اللي داخل القوس $u=1+x$. 🟢 مشتقته 1.'),
                      ('tex', r'x=u-1', [('(1+x)-1', 'x')], 'بقى $x$ برّا القوس: نطلّعه من $u$.'),
                      ('tex', r'\int x\left(1+x\right)^{1/3}dx=\int\left(u-1\right)u^{1/3}\,du=\int\left(u^{4/3}-u^{1/3}\right)du',
                       [('x*(1+x)**Rational(1,3)', '((1+x)-1)*(1+x)**Rational(1,3)'), ('(x-1)*x**Rational(1,3)', 'x**Rational(4,3)-x**Rational(1,3)', 't')],
                       'نعوّض، ونوزّع: $u\\cdot u^{1/3}=u^{4/3}$.'),
                      ('tex', r'=\frac{3}{7}u^{7/3}-\frac{3}{4}u^{4/3}',
                       [('diff(3*x**Rational(7,3)/7-3*x**Rational(4,3)/4,x)', 'x**Rational(4,3)-x**Rational(1,3)', 't')],
                       'قاعدة القوة: نزيد الأس 1 ونقسم عليه. والقسمة على $\\frac73$ ضرب في $\\frac37$.'),
                      ('line', '3*(1+x)**Rational(7,3)/7-3*(1+x)**Rational(4,3)/4', 'نرجع $u=1+x$.')])
    U.drill('2', 'MC-10', 'I', '$u=16-x^2$، فـ $x^2=16-u$، و $x\\,dx=-\\frac{du}{2}$.',
            sol_rows=[('sub', '16-x**2', '-2*x', '🔵 نسمّي اللي تحت الجذر $u=16-x^2$. 🟢 مشتقته $-2x$.'),
                      ('tex', r'x\,dx=\cA{-\frac12}\,du,\qquad x^{2}=16-u', [('diff(16-x**2,x)/(-2)', 'x'), ('16-(16-x**2)', 'x**2')],
                       '🟠 فوق $x\\,dx$، فنقسم على $-2$. والـ $x^2$ اللي بقى نطلّعه من $u$.'),
                      ('tex', r'\int x^{2}\sqrt{16-x^{2}}\cdot x\,dx=-\frac12\int\left(16-u\right)u^{1/2}\,du',
                       [('x**3*sqrt(16-x**2)', '-Rational(1,2)*(16-(16-x**2))*sqrt(16-x**2)*diff(16-x**2,x)')],
                       'نفصل $x^3=x^2\\cdot x$، ونعوّض الاثنين.'),
                      ('tex', r'=-\frac12\int\left(16u^{1/2}-u^{3/2}\right)du=-\frac12\left(\frac{32}{3}u^{3/2}-\frac25u^{5/2}\right)',
                       [('diff(-(Rational(32,3)*x**Rational(3,2)-Rational(2,5)*x**Rational(5,2))/2,x)', '-(16*x**Rational(1,2)-x**Rational(3,2))/2', 't')],
                       'نوزّع، ونكامل كل حد: $16\\cdot\\frac{u^{3/2}}{3/2}=\\frac{32}{3}u^{3/2}$.'),
                      ('line', '-16*(16-x**2)**Rational(3,2)/3+(16-x**2)**Rational(5,2)/5', 'نضرب في $-\\frac12$، ونرجع $u=16-x^2$.')])
    return U


# ---------------------------------------------------------------- خواص ln أول
def u_lnrules():
    U = Unit('U-LN', 'خواص ln أول: بسّط قبل ما تشتق أو تكامل', '4.2', 'من مذكرة د. موسى', 0)
    U.add('idea', 'ليش تشتغل؟', p(rich(
        'خواص ln تحوّل الصعب لسهل: الأس ينزل قدّام، والضرب يصير جمع، والقسمة طرح، و $e^{\\ln A}=A$. '
        'فنبسّط أول، والباقي يصير سؤال عادي.')))
    U.add('sign', 'متى؟', p(rich('<b>إذا شفت:</b> $e$ وفي أسها ln، مثل $e^{8\\ln x}$. أو ln داخلها ضرب أو قسمة أو جذر أو أس.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> ln داخلها شي بسيط مثل $\\ln(x^2+1)$ (اشتقها على طول)، أو $\\int\\ln x\\,dx$ (تجزئة).'))
          + contrast([(r'\int\frac{e^{8\ln x}}{x^{4}}dx', 'تجهيز: $e^{8\\ln x}=x^8$', '$e$ و ln يلغون بعض'),
                      (r'y=\ln\left|\frac{\sqrt{x^{2}+1}\,\sin^{5}x}{\left(x^{3}+4\right)^{2}}\right|', 'تجهيز: فكّ ln أول', 'داخل ln ضرب وقسمة وأسس'),
                      (r'\int\ln x\,dx', 'تجزئة', 'ln لحالها في تكامل')]))
    law = md(arith(r'\ln A^{n}=n\ln A,\quad \ln\left(AB\right)=\ln A+\ln B,\quad \ln\frac{A}{B}=\ln A-\ln B,\quad e^{\ln A}=A',
                   [('log(x**5)', '5*log(x)', 't'), ('log(x*(x+1))', 'log(x)+log(x+1)', 't'), ('log(x/(x+1))', 'log(x)-log(x+1)', 't'),
                    ('exp(log(x))', 'x', 't')], 'U-LN laws'))
    U.add('short', '🧭 الخطوات', method([
        'وش الشكل اللي يدلك؟ $e^{\\ldots\\ln\\ldots}$، أو ln داخلها ضرب أو قسمة أو أس أو جذر.',
        'سوّ الحركة: الأس ينزل قدّام (أو يرجع داخل)، والضرب جمع، والقسمة طرح، و $e^{\\ln A}=A$.',
        'تأكد برقم إن الشكل الجديد يساوي القديم.',
        'ارجع للشجرة: الحين وش الطريقة؟ اشتقاق حد حد، أو تكامل بقاعدة القوة.'],
        tricks_=[('الجذر أس: $\\ln\\sqrt[3]{x}=\\ln x^{1/3}=\\frac13\\ln x$. وتأكد برقم: $e^{2\\ln3}=3^{2}=9$.',
                  [('log(x**Rational(1,3))', 'log(x)/3', 't'), ('exp(2*log(3))', '9')])], label='U-LN') + law)

    it = ITEMS['MC-11']
    ex = question(it, 'U-LN example')
    ex += steps(it, [
        ('tex', r'e^{\cA{8}\ln x}=e^{\ln x^{\cA{8}}}=x^{8}', [('exp(8*log(x))', 'x**8', 't')],
         'وش الشكل؟ $e$ وفي أسها ln. الحركة: 🟠 الـ 8 ترجع أس داخل ln، ثم $e$ و ln يلغون بعض.'),
        ('tex', r'\frac{e^{8\ln x}}{x^{4}}=\frac{x^{8}}{x^{4}}=x^{4}', [('exp(8*log(x))/x**4', 'x**4', 't')],
         'القسمة بنفس الأساس: نطرح الأسس، $8-4=4$.'),
        ('line', 'x**5/5', 'ارجع للشجرة: صار قاعدة القوة. نزيد الأس 1 ونقسم عليه.')], 'U-LN ex')
    ex += final(it, 'U-LN example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. موسى)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('🔴 خواص ln للضرب والقسمة بس: $\\ln(A+B)$ ما تنفك.'),
                                rich('الأس اللي ينزل لازم يكون على اللي داخل ln كله: $\\ln\\sin^5x=5\\ln\\sin x$، لكن $(\\ln x)^5$ ما ينزل أسها.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\frac{e^{8\ln x}}{x^{4}}=\frac{x^{8}}{x^{4}}=x^{4}', [('exp(8*log(x))/x**4', 'x**4', 't')], 'U-LN paper 1'))
          + md(arith(r'\int x^{4}\,dx=\frac{x^{5}}{5}+C', [('diff(x**5/5,x)', 'x**4')], 'U-LN paper 2')))
    arith('', [('exp(8*log(2))', '2**8'), ('2**8', '256')], 'U-LN check')
    U.add('ok', '✔ تأكد', p(rich('عوّض رقم في الحركة: $x=2$ في $e^{8\\ln x}$ يعطي $2^8=256$، ونفس الرقم من $x^8$.')))
    U.gist('$e^{n\\ln x}$، أو ln داخلها ضرب أو قسمة أو أس', 'فكّ بخواص ln: الأس قدّام، والضرب جمع، و $e^{\\ln A}=A$',
           'اشتق أو كامل حد حد')
    U.drill('1', 'MC-13', 'G', 'الـ 7 ترجع أس داخل ln، و $e^{\\ln A}=A$.',
            first=r'e^{7\ln\left|x+1\right|}=\left|x+1\right|^{7}=\left(x+1\right)^{7}', claims=[('exp(7*log(Abs(x+1)))', '(x+1)**7', '-1+t')],
            sol_rows=[('sub', 'x+1', '1', '🔵 نسمّي $u=x+1$، و 🟢 مشتقته 1 (لـ $x>-1$ القيمة المطلقة ما تغيّر شي).'),
                      ('line', '(x+1)**8/8', 'قاعدة القوة: نزيد الأس 1 ونقسم عليه.')])
    U.drill('2', 'MC-12', 'I', 'فكّ ln أول: الجذر أس $\\frac12$، والضرب جمع، والقسمة طرح.',
            sol_rows=[('tex', r'y=\frac{1}{2}\ln\left(x^{2}+1\right)+5\ln\left|\sin x\right|-2\ln\left|x^{3}+4\right|',
                       [('exp(log(sqrt(x**2+1)*sin(x)**5/(x**3+4)**2))', 'exp(log(x**2+1)/2+5*log(sin(x))-2*log(x**3+4))', 'pi*t/(1+t)')],
                       'الضرب جمع، والقسمة طرح، وكل أس ينزل قدّام: $\\sqrt{x^2+1}=(x^2+1)^{1/2}$.'),
                      ('tex', r"y^{\prime}=\frac12\cdot\frac{\cD{2x}}{x^{2}+1}+5\cdot\frac{\cD{\cos x}}{\sin x}-2\cdot\frac{\cD{3x^{2}}}{x^{3}+4}",
                       [('diff(log(x**2+1)/2+5*log(sin(x))-2*log(x**3+4),x)', 'Rational(1,2)*2*x/(x**2+1)+5*cos(x)/sin(x)-2*3*x**2/(x**3+4)', 'pi*t/(1+t)')],
                       'ارجع للشجرة: صار اشتقاق ln حد حد. مشتقة ln: 🟢 مشتقة الداخل على الداخل.'),
                      ('line', 'x/(x**2+1)+5*cot(x)-6*x**2/(x**3+4)', 'نبسّط: $\\frac12\\cdot2x=x$، و $\\frac{\\cos x}{\\sin x}=\\cot x$، و $2\\cdot3x^2=6x^2$.')])
    return U


# ---------------------------------------------------------------- cosh أو sinh في المقام
def u_coshden():
    U = Unit('U-CH', 'cosh أو sinh لحالها في المقام: اكتبها بالأسس', '4.2', 'من مذكرة د. موسى وتدريب إضافي', 0)
    U.add('idea', 'ليش تشتغل؟', p(rich(
        'ما فيه قانون جاهز لـ $\\int\\frac{dx}{\\cosh x}$. لكن $\\cosh x=\\frac{e^{x}+e^{-x}}{2}$، '
        'وإذا ضربنا فوق وتحت في $e^x$ يطلع $e^x$ ومشتقتها، فيصير تعويض عادي.')))
    U.add('sign', 'متى؟', p(rich('<b>إذا شفت:</b> $\\cosh x$ أو $\\sinh x$ لحالها في المقام، وفوق ما فيه مشتقتها.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> فوق مشتقة اللي تحت، مثل $\\frac{\\cosh x}{\\sinh x}$: هذا تعويض $u=\\sinh x$ على طول.'))
          + contrast([(r'\int\frac{dx}{\cosh x}', 'تجهيز: بالأسس', 'فوق 1 بس'),
                      (r'\int\frac{e^{x}}{\sinh x}dx', 'تجهيز: بالأسس', 'فوق $e^x$، مو مشتقة $\\sinh x$'),
                      (r'\int\frac{\cosh x}{\sinh x}dx', 'تعويض $u=\\sinh x$', 'مشتقة المقام فوق، فالجواب ln')]))
    law = md(arith(r'\cosh x=\frac{e^{x}+e^{-x}}{2},\qquad \sinh x=\frac{e^{x}-e^{-x}}{2}',
                   [('cosh(x)', '(exp(x)+exp(-x))/2'), ('sinh(x)', '(exp(x)-exp(-x))/2')], 'U-CH laws'))
    U.add('short', '🧭 الخطوات', method([
        'وش الشكل اللي يدلك؟ $\\cosh x$ أو $\\sinh x$ في المقام، وفوق ما فيه مشتقتها.',
        'سوّ الحركة: اكتبها بالأسس، ثم اضرب فوق وتحت في $e^x$ عشان يروح $e^{-x}$.',
        'تأكد برقم إن الشكل الجديد يساوي القديم.',
        'ارجع للشجرة: الحين وش الطريقة؟ تعويض: 🔵 $u=e^{x}$، أو $u$ = المقام إذا مشتقته فوق.'],
        tricks_=[('$e^{x}\\cdot e^{-x}=e^{0}=1$. مثال: $e^{x}\\left(e^{x}+e^{-x}\\right)=e^{2x}+1$.',
                  [('exp(x)*(exp(x)+exp(-x))', 'exp(2*x)+1')])], label='U-CH') + law)

    it = ITEMS['GC-01']
    ex = question(it, 'U-CH example')
    ex += steps(it, [
        ('tex', r'\frac{1}{\cosh x}=\frac{\cA{2}}{e^{x}+e^{-x}}', [('1/cosh(x)', '2/(exp(x)+exp(-x))')],
         'وش الشكل؟ $\\cosh x$ في المقام، وفوق 1 بس. نكتبه بالأسس: 🟠 الـ 2 اللي تحت تطلع فوق.'),
        ('tex', r'=\frac{2\,e^{x}}{e^{x}\left(e^{x}+e^{-x}\right)}=\frac{2\,e^{x}}{e^{2x}+1}', [('2/(exp(x)+exp(-x))', '2*exp(x)/(exp(2*x)+1)')],
         'نضرب فوق وتحت في $e^x$: $e^x\\cdot e^{-x}=1$، و $e^x\\cdot e^x=e^{2x}$.'),
        ('sub', 'exp(x)', 'exp(x)', 'ارجع للشجرة: فوق $e^x$، وتحت $(e^x)^2+1$. 🔵 $u=e^x$، و 🟢 $du=e^x\\,dx$ موجودة فوق.'),
        ('tex', r'\int\frac{2\,e^{x}\,dx}{\left(e^{x}\right)^{2}+1}=2\int\frac{du}{1+u^{2}}', [('2*exp(x)/(exp(2*x)+1)', '2*diff(exp(x),x)/(1+exp(x)**2)')],
         'صار $1+u^2$ بدون جذر: قانون $\\tan^{-1}$ من 3.4.'),
        ('line', '2*atan(exp(x))', '$\\int\\frac{du}{1+u^2}=\\tan^{-1}u$. ونرجع $u=e^x$.')], 'U-CH ex')
    ex += final(it, 'U-CH example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (تدريب إضافي: ما جا هذا الشكل في المصادر)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('🔴 $\\int\\frac{dx}{\\cosh x}$ مو $\\ln|\\cosh x|$. الـ ln بس إذا مشتقة المقام فوق.'),
                                rich('لا تنسى الـ 2: $\\frac{1}{\\cosh x}=\\frac{2}{e^x+e^{-x}}$، مو $\\frac{1}{e^x+e^{-x}}$.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\frac{1}{\cosh x}=\frac{2e^{x}}{e^{2x}+1},\qquad u=e^{x},\quad du=e^{x}\,dx',
                   [('1/cosh(x)', '2*exp(x)/(exp(2*x)+1)'), ('diff(exp(x),x)', 'exp(x)')], 'U-CH paper 1'))
          + md(arith(r'2\int\frac{du}{1+u^{2}}=2\tan^{-1}\left(e^{x}\right)+C', [('diff(2*atan(exp(x)),x)', '1/cosh(x)')], 'U-CH paper 2')))
    arith('', [('1/cosh(0)', '1'), ('2*exp(0)/(exp(0)+1)', '1')], 'U-CH check')
    U.add('ok', '✔ تأكد', p(rich('تأكد برقم من الحركة: $x=0$ يعطي $\\frac{1}{\\cosh0}=1$، و $\\frac{2e^0}{e^0+1}=1$.')))
    U.gist('$\\cosh x$ أو $\\sinh x$ لحالها في المقام', 'اكتبها بالأسس، واضرب فوق وتحت في $e^x$', 'تعويض $u=e^x$ (أو $u$ = المقام)')
    U.drill('1', 'MC-16', 'P', 'قبل الأسس، شوف فوق: $\\cosh x$ هي مشتقة $\\sinh x$.',
            sol_rows=[('sub', 'sinh(x)', 'cosh(x)', 'فوق $\\cosh x$ = مشتقة $\\sinh x$، فهذي مو حالة الأسس. ارجع للشجرة: تعويض 🔵 $u=\\sinh x$.'),
                      ('tex', r'\int\frac{\cosh x\,dx}{1+\sinh^{2}x}=\int\frac{du}{1+u^{2}}', [('cosh(x)/(1+sinh(x)**2)', 'diff(sinh(x),x)/(1+sinh(x)**2)')],
                       'صار $1+u^2$ بدون جذر: قانون $\\tan^{-1}$ من 3.4.'),
                      ('line', 'atan(sinh(x))', 'نرجع $u=\\sinh x$. (في مذكرة د. موسى ص66 الجواب مكتوب $\\sinh x$، وهذا غلط: '
                                                '$\\frac{\\cosh x}{\\cosh^2x}=\\frac{1}{\\cosh x}$ مو $\\cosh x$.)')])
    U.drill('2', 'GC-03', 'I', 'اكتب $\\sinh x$ بالأسس، واضرب فوق وتحت في $e^x$. ثم $u$ = المقام.',
            sol_rows=[('tex', r'\frac{e^{x}}{\sinh x}=\frac{2\,e^{x}}{e^{x}-e^{-x}}=\frac{2\,e^{2x}}{e^{2x}-1}',
                       [('exp(x)/sinh(x)', '2*exp(x)/(exp(x)-exp(-x))'), ('2*exp(x)/(exp(x)-exp(-x))', '2*exp(2*x)/(exp(2*x)-1)')],
                       'نكتب $\\sinh x$ بالأسس والـ 2 تطلع فوق، ثم نضرب فوق وتحت في $e^x$.'),
                      ('sub', 'exp(2*x)-1', '2*exp(2*x)', 'ارجع للشجرة: 🟢 مشتقة المقام $2e^{2x}$ موجودة فوق كاملة. 🔵 نسمّي $u=e^{2x}-1$.'),
                      ('tex', r'\int\frac{2\,e^{2x}\,dx}{e^{2x}-1}=\int\frac{du}{u}=\ln\left|u\right|',
                       [('2*exp(2*x)/(exp(2*x)-1)', 'diff(exp(2*x)-1,x)/(exp(2*x)-1)'), ('diff(log(x),x)', '1/x', 't')],
                       '$\\int\\frac{du}{u}=\\ln|u|$، ونرجع $u=e^{2x}-1$.')])
    return U


UNITS_NEW = [u_logdiff, u_34, u_x2, u_lnrules, u_coshden]

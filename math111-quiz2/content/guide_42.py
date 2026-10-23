"""المذكرة الكاملة — الدرس 4.2: الدوال الزائدية العكسية (الأيام 1–3)."""
from booklet import sc_lamda, sc_six, sc_square, sc_twins
from booklet_engine import ITEMS, arith, formula, functional, q_tex, same_value, use
from guide_kit import Unit, alg, contrast, final, method, pgref, question, rich, short_steps, shortcut, steps, tricks
from guide_rules import R
from html_kit import link, md, mi, p, table, ul
import sympy as s
from mathlib import x


def frow(z, c=None):
    return [mi(r'\displaystyle ' + z[0]), mi(r'\displaystyle ' + z[1])] + ([c] if c is not None else [])


# ---------------------------------------------------------------- 1
def u_deriv():
    U = Unit('U-D1', 'مشتقة الدالة الزائدية العكسية', '4.2', 'ص56–58', 1)
    U.add('idea', 'الفكرة', p(rich(
        'كل دالة زائدية عكسية لها قانون مشتقة جاهز في الجدول. '
        "إذا داخل الدالة شي غير $x$ لحالها، نسمّيه $u$ ونضرب القانون في مشتقته $u'$. "
        'هذي قاعدة السلسلة نفسها اللي استعملتها في 4.1.')))
    U.add('sign', 'العلامة', p(rich(
        'إذا شفت <b>Find dy/dx</b> أو <b>Find the derivative</b>، وفي السؤال $\\sinh^{-1}$ أو $\\cosh^{-1}$ أو $\\tanh^{-1}$ '
        'أو $\\coth^{-1}$ أو $\\operatorname{sech}^{-1}$ أو $\\operatorname{csch}^{-1}$.'))
          + contrast([(r'y=\sinh^{-1}(3x)', "قانون $\\sinh^{-1}$، ثم نضرب في $u'$", 'دالة عكسية: الـ $-1$ اسم، مو أس'),
                      (r'y=\sinh(3x)', 'من 4.1: $\\cosh(3x)\\cdot3$', 'دالة عادية، مو عكسية'),
                      (r'\int\frac{dx}{\sqrt{x^{2}+49}}', 'تكامل (النوع 3)', 'المطلوب تكامل، مو مشتقة')]))
    U.prev('أول نوع في 4.2: في 4.1 اشتقيت الدوال الزائدية العادية، وهنا نشتق الدوال العكسية.')
    law, _ = sc_twins()
    U.add('short', '📐 القانون: جدول مشتقات الدوال العكسية', law + method([
        "نسمّي اللي داخل الدالة العكسية $u$، ونشتقه فيطلع $u'$.",
        'نجيب قانون الدالة من الجدول.',
        "نعوّض $u$ في القانون، ونضرب في $u'$.",
        'نبسّط: مربع الجذر، والكسر فوق كسر.'], tricks_=[
        ('نحفظ الجدول بثلاث جمل. $\\sinh^{-1}$ معها $\\sqrt{u^2+1}$، و $\\cosh^{-1}$ معها $\\sqrt{u^2-1}$. '
         '$\\tanh^{-1}$ و $\\coth^{-1}$ نفس الشكل $\\frac{1}{1-u^2}$. $\\operatorname{sech}^{-1}$ و $\\operatorname{csch}^{-1}$ فيها سالب، و $u$ برّا الجذر.',
         [('diff(asinh(x),x)', '1/sqrt(x**2+1)'), ('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t'),
          ('diff(atanh(x),x)', '1/(1-x**2)'), ('diff(acoth(x),x)', '1/(1-x**2)'), ('diff(asech(x),x)', '-1/(x*sqrt(1-x**2))', 't/(1+t)')]),
        ("ودايم نضرب في مشتقة اللي داخل الدالة: $\\left(\\sinh^{-1}4x\\right)'=\\frac{4}{\\sqrt{16x^2+1}}$.",
         [('diff(asinh(4*x),x)', '4/sqrt(16*x**2+1)')])], label='U-D1')
          + p(rich('مشتقات الدوال الزائدية العادية (sinh و cosh و tanh…) من 4.1، وتحتاجها في التمارين. جدولها في ')
              + link('P-A3', '📚 أ3 ص ' + pgref('P-A3')) + '.', 'small'))
    for f_, F_, br in [('asinh(x)', 'log(x+sqrt(x**2+1))', None), ('acosh(x)', 'log(x+sqrt(x**2-1))', '1+t'),
                       ('atanh(x)', 'log((1+x)/(1-x))/2', 't/(1+t)'), ('acoth(x)', 'log((x+1)/(x-1))/2', '1+t'),
                       ('asech(x)', 'log((1+sqrt(1-x**2))/x)', 't/(1+t)'), ('acsch(x)', 'log(1/x+sqrt(1+x**2)/Abs(x))', 't')]:
        same_value(f_, F_, 'log form ' + f_, branch=br)
    defs = table(['الدالة', 'تُعرَّف عند', 'بـ ln'], [
        [mi(r'\sinh^{-1}x'), 'كل ' + mi('x'), mi(r'\ln\left(x+\sqrt{x^{2}+1}\right)')],
        [mi(r'\cosh^{-1}x'), mi(r'x\ge1'), mi(r'\ln\left(x+\sqrt{x^{2}-1}\right)')],
        [mi(r'\tanh^{-1}x'), mi(r'|x|<1'), mi(r'\frac12\ln\frac{1+x}{1-x}')],
        [mi(r'\coth^{-1}x'), mi(r'|x|>1'), mi(r'\frac12\ln\frac{x+1}{x-1}')],
        [mi(r'\operatorname{sech}^{-1}x'), mi(r'0<x\le1'), mi(r'\ln\frac{1+\sqrt{1-x^{2}}}{x}')],
        [mi(r'\operatorname{csch}^{-1}x'), mi(r'x\ne0'), mi(r'\ln\left(\frac1x+\frac{\sqrt{1+x^{2}}}{|x|}\right)')]], 'formula compact')
    U.add('note', 'للمعرفة بس: كل دالة عكسية تنكتب بـ ln (مذكرة د. طارق ص57)',
          p('ما جات في الاختبارات السابقة، فما تحتاج تحفظها.') + defs)

    it = ITEMS['N42-E1-1']
    ex = question(it, 'U-D1 example 1')
    ex += steps(it, [
        ('tex', r"u=5x-1,\qquad u'=5", [('diff(5*x-1,x)', '5')],
         'داخل $\\sinh^{-1}$ مو $x$ لحالها، فنسمّيه $u$ ونشتقه. مشتقة $5x$ هي 5، والرقم $-1$ مشتقته 0.'),
        ('tex', r"\left(\sinh^{-1}u\right)'=\frac{u'}{\sqrt{u^{2}+1}}", [('diff(asinh(x),x)', '1/sqrt(x**2+1)')],
         "قانون $\\sinh^{-1}$ من الجدول. فيه $u'$ فوق لأن داخل الدالة مو $x$ لحالها."),
        ('line', '5/sqrt(1+(5*x-1)**2)', "نعوّض $u'=5$ فوق، و $u=5x-1$ تحت.")], 'U-D1 ex1')
    ex += final(it, 'U-D1 example 1')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)

    it = ITEMS['1447-S2-SE-Q1.2']
    ex = question(it, 'U-D1 example 2')
    ex += steps(it, [
        ('tex', r"u=\sqrt{x+2},\qquad u'=\frac{1}{2\sqrt{x+2}}", [('diff(sqrt(x+2),x)', '1/(2*sqrt(x+2))')],
         'داخل $\\operatorname{csch}^{-1}$ جذر، فنسمّيه $u$. مشتقة الجذر = 1 على ضعف الجذر، في مشتقة اللي تحته (هنا 1).'),
        ('tex', r"\left(\operatorname{csch}^{-1}u\right)'=-\frac{u'}{|u|\sqrt{1+u^{2}}}",
         [('diff(acsch(x),x)', '-1/(Abs(x)*sqrt(1+x**2))', 't'), ('diff(acsch(x),x)', '-1/(Abs(x)*sqrt(1+x**2))', '-t')],
         'قانون $\\operatorname{csch}^{-1}$ من الجدول: فيه سالب، و $|u|$ برّا الجذر.'),
        ('tex', r'|u|=\sqrt{x+2}', [('Abs(sqrt(x+2))', 'sqrt(x+2)', 't-2')], 'الجذر موجب دايم، فالقيمة المطلقة ما تغيّر شي.'),
        ('tex', r'u^{2}=\left(\sqrt{x+2}\right)^{2}=x+2', [('sqrt(x+2)**2', 'x+2')], 'الجذر تربيعه يرجّع اللي تحته.'),
        ('tex', r'1+u^{2}=1+x+2=x+3', [('1+x+2', 'x+3')], 'نجمع الأرقام: $1+2=3$.'),
        ('tex', r"y'=-\frac{\ \frac{1}{2\sqrt{x+2}}\ }{\sqrt{x+2}\,\sqrt{x+3}}",
         [('diff(acsch(sqrt(x+2)),x)', '-(1/(2*sqrt(x+2)))/(sqrt(x+2)*sqrt(x+3))', 't-2')],
         "نعوّض في القانون: $u'$ فوق، و $|u|$ و $\\sqrt{1+u^2}$ تحت."),
        ('tex', r"y'=-\frac{1}{2\sqrt{x+2}\cdot\sqrt{x+2}\cdot\sqrt{x+3}}",
         [('-(1/(2*sqrt(x+2)))/(sqrt(x+2)*sqrt(x+3))', '-1/(2*sqrt(x+2)*sqrt(x+2)*sqrt(x+3))')],
         'كسر فوق كسر: مقام الكسر الصغير $2\\sqrt{x+2}$ ينزل ويُضرب في المقام الكبير.'),
        ('line', '-1/(2*(x+2)*sqrt(x+3))', 'الجذر في نفسه يعطي اللي تحته: $\\sqrt{x+2}\\cdot\\sqrt{x+2}=x+2$.')], 'U-D1 ex2')
    ex += final(it, 'U-D1 example 2')
    U.add('ex', '🧱 مثال 2 محلول خطوة خطوة (اختبار سابق)', ex)

    it2 = ITEMS['1446-S2-SE-Q1.2']
    U.add('trap', '⚠️ الفخ', ul([
        rich("أكثر غلطة: تنسى تضرب في $u'$."),
        rich("إشارة $\\coth^{-1}$: مشتقتها $\\frac{u'}{1-u^2}$ موجبة، نفس $\\tanh^{-1}$. مذكرة د. طارق ص58 ومفتاح 1445 كتبوها بسالب، "
             'والحساب يقول موجبة. <b>اسأل الدكتور وش يعتمد</b>، واكتب في الكويز اللي يقوله. هذا مثال بالإشارة الصحيحة من مفتاح 1446:')])
          + md(q_tex(use(it2['id'], 'U-D1 trap'))) + final(it2, 'U-D1 trap'))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r"u=\sqrt{x+2}\qquad u'=\frac{1}{2\sqrt{x+2}}", [('diff(sqrt(x+2),x)', '1/(2*sqrt(x+2))')], 'U-D1 paper 1'))
          + md(arith(r"y'=-\frac{u'}{|u|\sqrt{1+u^{2}}}=-\frac{\ \frac{1}{2\sqrt{x+2}}\ }{\sqrt{x+2}\,\sqrt{x+3}}",
                     [('diff(acsch(sqrt(x+2)),x)', '-(1/(2*sqrt(x+2)))/(sqrt(x+2)*sqrt(x+3))', 't-2')], 'U-D1 paper 2'))
          + md(arith(r"y'=-\frac{1}{2(x+2)\sqrt{x+3}}", [('diff(acsch(sqrt(x+2)),x)', '-1/(2*(x+2)*sqrt(x+3))', 't-2')], 'U-D1 paper 3')))
    U.add('ok', '✔ تأكد', p(rich("شوف البسط: لازم يكون فيه $u'$. ومع $\\operatorname{sech}^{-1}$ و $\\operatorname{csch}^{-1}$ الجواب يبدأ بإشارة سالبة.")))
    U.gist('مشتقة، وفي السؤال دالة عكسية مثل $\\sinh^{-1}$ أو $\\operatorname{csch}^{-1}$', "سمّ اللي داخل الدالة $u$، واشتقه",
           "قانون الدالة من الجدول، مضروب في $u'$")
    U.drill('1', '1445-S1-SE-Q1.1', 'G', 'نشتق كل حد لحاله. الثاني قانون $\\operatorname{sech}^{-1}$.',
            first=r"\left(\cosh(3x^{2})\right)'=\sinh(3x^{2})\cdot6x",
            claims=[('diff(cosh(3*x**2),x)', 'sinh(3*x**2)*6*x')],
            sol_rows=[('tex', r"u=2x,\qquad u'=2", [('diff(2*x,x)', '2')],
                       'الحد الثاني: داخل $\\operatorname{sech}^{-1}$ هو $2x$، فنسمّيه $u$. مشتقته 2.'),
                      ('tex', r"\left(\operatorname{sech}^{-1}u\right)'=-\frac{u'}{u\sqrt{1-u^{2}}}",
                       [('diff(asech(x),x)', '-1/(x*sqrt(1-x**2))', 't/(1+t)')],
                       'قانون $\\operatorname{sech}^{-1}$ من الجدول: فيه سالب، و $u$ برّا الجذر.'),
                      ('tex', r"\left(\operatorname{sech}^{-1}2x\right)'=-\frac{2}{2x\sqrt{1-(2x)^{2}}}",
                       [('diff(asech(2*x),x)', '-2/(2*x*sqrt(1-(2*x)**2))', 't/(2*(1+t))')], "نعوّض $u=2x$ و $u'=2$."),
                      ('tex', r'=-\frac{1}{x\sqrt{1-4x^{2}}}', [('-2/(2*x*sqrt(1-(2*x)**2))', '-1/(x*sqrt(1-4*x**2))', 't/(2*(1+t))')],
                       'نختصر 2 فوق مع 2 تحت. و $(2x)^2=4x^2$.'),
                      ('line', '6*x*sinh(3*x**2)-1/(x*sqrt(1-4*x**2))', 'نجمع مشتقة الحدين.')])
    U.drill('2', '1446-S1-SE-Q1.2', 'P', 'الأول قانون $\\sinh^{-1}$ مع $u=\\sqrt x$. الثاني من 4.1.',
            sol_rows=[('tex', r"u=\sqrt{x},\qquad u'=\frac{1}{2\sqrt{x}}", [('diff(sqrt(x),x)', '1/(2*sqrt(x))')],
                       'الحد الأول: داخل $\\sinh^{-1}$ جذر، فنسمّيه $u$. مشتقة الجذر = 1 على ضعف الجذر.'),
                      ('tex', r"\left(\sinh^{-1}u\right)'=\frac{u'}{\sqrt{u^{2}+1}}", [('diff(asinh(x),x)', '1/sqrt(x**2+1)')],
                       'قانون $\\sinh^{-1}$ من الجدول.'),
                      ('tex', r'u^{2}=\left(\sqrt{x}\right)^{2}=x', [('sqrt(x)**2', 'x')], 'الجذر تربيعه يرجّع اللي تحته.'),
                      ('tex', r"\left(\sinh^{-1}\sqrt{x}\right)'=\frac{\ \frac{1}{2\sqrt{x}}\ }{\sqrt{x+1}}",
                       [('diff(asinh(sqrt(x)),x)', '(1/(2*sqrt(x)))/sqrt(x+1)', 't')], "نعوّض $u'$ فوق، و $u^2=x$ تحت."),
                      ('tex', r'=\frac{1}{2\sqrt{x}\,\sqrt{x+1}}', [('(1/(2*sqrt(x)))/sqrt(x+1)', '1/(2*sqrt(x)*sqrt(x+1))')],
                       'كسر فوق كسر: مقام الكسر الصغير $2\\sqrt x$ ينزل تحت.'),
                      ('tex', r"\left(\coth(4x^{2})\right)'=-\operatorname{csch}^{2}(4x^{2})\cdot8x",
                       [('diff(coth(4*x**2),x)', '-csch(4*x**2)**2*8*x')],
                       'الحد الثاني دالة عادية. من 4.1: مشتقة coth هي $-\\operatorname{csch}^2$، في مشتقة اللي داخلها ($8x$).'),
                      ('line', '1/(2*sqrt(x)*sqrt(1+x))-8*x*csch(4*x**2)**2', 'نجمع مشتقة الحدين.')])
    U.drill('3', '1447-S1-SE-Q1.2', 'I', 'الأول من 4.1. الثاني قانون $\\tanh^{-1}$ مع $u=\\sin x$.',
            sol_rows=[('tex', r"\left(\operatorname{sech}(5x^{2})\right)'=-\operatorname{sech}(5x^{2})\tanh(5x^{2})\cdot10x",
                       [('diff(sech(5*x**2),x)', '-sech(5*x**2)*tanh(5*x**2)*10*x')],
                       'الحد الأول دالة عادية، مو عكسية. من 4.1: مشتقة sech هي $-\\operatorname{sech}\\cdot\\tanh$، في مشتقة اللي داخلها ($10x$).'),
                      ('tex', r"u=\sin x,\qquad u'=\cos x", [('diff(sin(x),x)', 'cos(x)')],
                       'الحد الثاني: داخل $\\tanh^{-1}$ هو $\\sin x$، فنسمّيه $u$.'),
                      ('tex', r"\left(\tanh^{-1}u\right)'=\frac{u'}{1-u^{2}}", [('diff(atanh(x),x)', '1/(1-x**2)')],
                       'قانون $\\tanh^{-1}$ من الجدول.'),
                      ('tex', r"\left(\tanh^{-1}(\sin x)\right)'=\frac{\cos x}{1-\sin^{2}x}", [('diff(atanh(sin(x)),x)', 'cos(x)/(1-sin(x)**2)')],
                       "نعوّض $u=\\sin x$ و $u'=\\cos x$."),
                      ('line', '-10*x*sech(5*x**2)*tanh(5*x**2)+cos(x)/(1-sin(x)**2)', 'نجمع مشتقة الحدين.')])
    return U


def box_memo(memo):
    return '<div class="memo-inline"><b>كيف أتذكّره:</b> ' + memo + '</div>'


# ---------------------------------------------------------------- 2
def u_deriv_rules():
    U = Unit('U-D2', 'مشتقات مركبة: أسية، ln، قوة، ضرب', '4.2', 'ص59، تمارين 1–6', 1)
    U.add('idea', 'الفكرة', p(rich(
        'الدالة العكسية تجي داخل قاعدة ثانية: أسية، أو ln، أو قوة، أو ضرب دالتين. '
        'نشتق القاعدة الكبيرة أول، وبعدها نشتق الدالة العكسية اللي داخلها بقانون النوع 1. '
        'كل طبقة نشتقها لحالها، ونضرب النتائج في بعض.')))
    U.add('sign', 'العلامة', p(rich('إذا شفت مشتقة، والدالة العكسية داخل أس مثل $6^{(\\ldots)}$، أو داخل $\\ln$ أو $\\log$، '
                                    'أو مرفوعة لقوة، أو مضروبة في دالة ثانية.')))
    U.prev('في النوع 1 كانت الدالة العكسية لحالها. هنا هي داخل قاعدة ثانية، فنشتق القاعدة الكبيرة أول.')
    r = [formula('a**u', 'a**u*log(a)', 'diff', branches=('x',), pos=('a',), uprime=True, label='rule a^u'),
         formula('exp(u)', 'exp(u)', 'diff', branches=('x',), uprime=True, label='rule e^u'),
         formula('log(Abs(u))', '1/u', 'diff', branches=('t', '-t'), uprime=True, label='rule ln|u|'),
         formula('log(Abs(u))/log(10)', '1/(u*log(10))', 'diff', branches=('t', '-t'), uprime=True, label='rule log10'),
         formula('u**n', 'n*u**(n-1)', 'diff', branches=('t',), real=('n',), uprime=True, label='rule u^n')]
    f, g = s.Function('f')(x), s.Function('g')(x)
    functional(lambda: s.diff(f * g, x) - (s.diff(f, x) * g + f * s.diff(g, x)), 'product rule')
    functional(lambda: s.simplify(s.diff(f / g, x) - (s.diff(f, x) * g - f * s.diff(g, x)) / g ** 2), 'quotient rule')
    law = table(['المشتقة', 'تساوي'], [frow(z) for z in r], 'formula compact')
    law += md(r"(f\,g)'=f'\,g+f\,g',\qquad \left(\frac{f}{g}\right)'=\frac{f'\,g-f\,g'}{g^{2}}")
    law += p(rich('$a$ رقم موجب ثابت (الأساس)، و $n$ رقم ثابت (الأس)، و $f$ و $g$ دالتين. '
                  'وفي الاختبارات $\\log$ بدون أساس يعني أساس 10.'), 'small')
    U.add('short', '📐 القانون: القواعد اللي حول الدالة العكسية', law + method([
        'نحدد القاعدة الكبيرة: أسية، أو ln، أو قوة، أو ضرب.',
        'نكتب مشتقة القاعدة الكبيرة، ونخلي مشتقة اللي داخلها لسطر لحاله.',
        'نشتق الدالة العكسية بقانونها من جدول النوع 1.',
        'نعوّض ونرتّب الجواب.'], tricks_=[
        ('نشتق من برّا لجوّا: كل طبقة مشتقتها، ونضربها في بعض. مثال: $\\left(\\sinh^{-1}2x\\right)^3$ برّا قوة، مشتقتها '
         '$3\\left(\\sinh^{-1}2x\\right)^2$. وجوّا $\\sinh^{-1}2x$، مشتقتها $\\frac{2}{\\sqrt{4x^2+1}}$. ونضربهم.',
         [('diff(asinh(2*x)**3,x)', '3*asinh(2*x)**2*2/sqrt(4*x**2+1)')])], label='U-D2'))
    it = ITEMS['N42-E1-4']
    ex = question(it, 'U-D2 example')
    ex += steps(it, [
        ('tex', r"y'=6^{u}\cdot\ln6\cdot u',\qquad u=\cosh^{-1}(2x)",
         [('diff(6**acosh(2*x),x)', '6**acosh(2*x)*log(6)*diff(acosh(2*x),x)')],
         "هنا التريك: نبدأ من برّا. برّا أسية، والقانون $(a^u)'=a^u\\ln a\\cdot u'$، وهنا $a=6$ و $u$ الأس كله."),
        ('tex', r"u'=\frac{2}{\sqrt{(2x)^{2}-1}}", [('diff(acosh(2*x),x)', '2/sqrt((2*x)**2-1)', '1/2+t')],
         'بعدها جوّا: نشتق الأس بقانون $\\cosh^{-1}$ من النوع 1. اللي داخله $2x$، ومشتقته 2.'),
        ('tex', r"u'=\frac{2}{\sqrt{4x^{2}-1}}", [('2/sqrt((2*x)**2-1)', '2/sqrt(4*x**2-1)')],
         'نفك المربع: $(2x)^2=2^2\\cdot x^2=4x^2$.'),
        ('line', '6**acosh(2*x)*2*log(6)/sqrt(4*x**2-1)', "نعوّض $u'$ في السطر الأول، ونرتّب الأرقام قدّام.")], 'U-D2 ex')
    ex += final(it, 'U-D2 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([
        rich('رتّب: القاعدة الكبيرة أول، ثم اللي داخلها. لا تشتق الدالة العكسية وتنسى الأسية.'),
        rich('مع $a^u$ لا تنسى $\\ln a$. ومع $\\log$ (أساس 10) لا تنسى $\\ln10$ في المقام.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r"y'=6^{u}\cdot\ln6\cdot u'", [('diff(6**acosh(2*x),x)', '6**acosh(2*x)*log(6)*diff(acosh(2*x),x)')], 'U-D2 paper 1'))
          + md(arith(r"u=\cosh^{-1}(2x)\qquad u'=\frac{2}{\sqrt{4x^{2}-1}}", [('diff(acosh(2*x),x)', '2/sqrt(4*x**2-1)', '1/2+t')], 'U-D2 paper 2'))
          + md(arith(r"y'=6^{\cosh^{-1}(2x)}\cdot\ln6\cdot\frac{2}{\sqrt{4x^{2}-1}}",
                     [('diff(6**acosh(2*x),x)', '6**acosh(2*x)*log(6)*2/sqrt(4*x**2-1)', '1/2+t')], 'U-D2 paper 3')))
    U.add('ok', '✔ تأكد', p(rich('عدّ الطبقات: كل طبقة تعطي عامل في الجواب. هنا ثلاثة: $6^{\\cosh^{-1}(2x)}$، و $\\ln6$، ومشتقة الأس.')))
    U.gist('مشتقة، والدالة العكسية داخل أس أو ln أو قوة أو ضرب', 'اشتق القاعدة الكبيرة (برّا) أول',
           'اشتق الدالة العكسية (جوّا) بقانون النوع 1، واضرب')
    U.drill('1', 'N42-E1-6', 'G', 'قاعدة القوة أول، ثم نشتق اللي داخل القوس حد حد.',
            first=r"y'=5\left(\operatorname{sech}^{-1}(3x)+7^{x}\right)^{4}\cdot\left(\operatorname{sech}^{-1}(3x)+7^{x}\right)'",
            claims=[('diff((asech(3*x)+7**x)**5,x)', '5*(asech(3*x)+7**x)**4*diff(asech(3*x)+7**x,x)')],
            sol_rows=[('tex', r"\left(\operatorname{sech}^{-1}3x\right)'=-\frac{3}{3x\sqrt{1-(3x)^{2}}}",
                       [('diff(asech(3*x),x)', '-3/(3*x*sqrt(1-(3*x)**2))', 't/(3*(1+t))')],
                       "داخل القوس: قانون $\\operatorname{sech}^{-1}$ من النوع 1، $-\\frac{u'}{u\\sqrt{1-u^2}}$ مع $u=3x$ و $u'=3$."),
                      ('tex', r'=-\frac{1}{x\sqrt{1-9x^{2}}}', [('-3/(3*x*sqrt(1-(3*x)**2))', '-1/(x*sqrt(1-9*x**2))', 't/(3*(1+t))')],
                       'نختصر 3 فوق مع 3 تحت. و $(3x)^2=9x^2$.'),
                      ('tex', r"\left(7^{x}\right)'=7^{x}\ln7", [('diff(7**x,x)', '7**x*log(7)')],
                       "القانون $(a^u)'=a^u\\ln a\\cdot u'$، وهنا $a=7$ و $u=x$، فـ $u'=1$."),
                      ('line', '5*(asech(3*x)+7**x)**4*(-1/(x*sqrt(1-9*x**2))+7**x*log(7))',
                       'نعوّض مشتقة اللي داخل القوس في السطر الجاهز.')])
    U.drill('2', 'N42-X1-1', 'P', "ضرب دالتين: $(fg)'=f'g+fg'$.",
            sol_rows=[('tex', r"y'=\left(\sinh^{-1}3^{x}\right)'\cdot\sqrt{x}+\sinh^{-1}3^{x}\cdot\left(\sqrt{x}\right)'",
                       [('diff(asinh(3**x)*sqrt(x),x)', 'diff(asinh(3**x),x)*sqrt(x)+asinh(3**x)*diff(sqrt(x),x)')],
                       "ضرب دالتين. القانون: $(fg)'=f'g+fg'$، و $f=\\sinh^{-1}3^x$ و $g=\\sqrt x$."),
                      ('tex', r"u=3^{x},\qquad u'=3^{x}\ln3", [('diff(3**x,x)', '3**x*log(3)')],
                       "داخل $\\sinh^{-1}$ هو $3^x$، فنسمّيه $u$. القانون $(a^x)'=a^x\\ln a$ مع $a=3$."),
                      ('tex', r"\left(\sinh^{-1}3^{x}\right)'=\frac{3^{x}\ln3}{\sqrt{\left(3^{x}\right)^{2}+1}}",
                       [('diff(asinh(3**x),x)', '3**x*log(3)/sqrt((3**x)**2+1)')], "قانون $\\sinh^{-1}$: $\\frac{u'}{\\sqrt{u^2+1}}$."),
                      ('tex', r'\left(3^{x}\right)^{2}=3^{2x}', [('(3**x)**2', '3**(2*x)')], 'أس فوق أس: نضرب الأسين، $x\\cdot2=2x$.'),
                      ('tex', r"\left(\sqrt{x}\right)'=\frac{1}{2\sqrt{x}}", [('diff(sqrt(x),x)', '1/(2*sqrt(x))')], 'مشتقة الجذر = 1 على ضعف الجذر.'),
                      ('line', '3**x*log(3)*sqrt(x)/sqrt(1+3**(2*x))+asinh(3**x)/(2*sqrt(x))', 'نعوّض كل قطعة في قانون الضرب.')])
    U.drill('3', '1446-S1-FE-Q1.3', 'I', 'الأول قانون $\\cosh^{-1}$ مع أسية. الثاني $\\log$ بأساس 10.',
            sol_rows=[('tex', r"u=3^{x^{2}-1},\qquad u'=3^{x^{2}-1}\cdot\ln3\cdot2x", [('diff(3**(x**2-1),x)', '3**(x**2-1)*log(3)*2*x')],
                       'الحد الأول: داخل $\\cosh^{-1}$ أسية، فنسمّيها $u$. مشتقة $3^{(\\ldots)}$ = نفسها × $\\ln3$ × مشتقة الأس ($2x$).'),
                      ('tex', r'u^{2}=\left(3^{x^{2}-1}\right)^{2}=3^{2x^{2}-2}', [('(3**(x**2-1))**2', '3**(2*x**2-2)')],
                       'أس فوق أس: نضرب الأسين، $2(x^2-1)=2x^2-2$.'),
                      ('tex', r"\left(\cosh^{-1}u\right)'=\frac{u'}{\sqrt{u^{2}-1}}", [('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t')],
                       'قانون $\\cosh^{-1}$ من النوع 1.'),
                      ('tex', r"\left(\cosh^{-1}3^{x^{2}-1}\right)'=\frac{2x\ln3\cdot3^{x^{2}-1}}{\sqrt{3^{2x^{2}-2}-1}}",
                       [('diff(acosh(3**(x**2-1)),x)', '2*x*log(3)*3**(x**2-1)/sqrt(3**(2*x**2-2)-1)', '1+t')],
                       "نعوّض $u'$ فوق، و $u^2$ تحت."),
                      ('tex', r'\log\left|\tanh2x\right|=\frac{\ln\left|\tanh2x\right|}{\ln10}', [('log(tanh(2*x),10)', 'log(tanh(2*x))/log(10)')],
                       'الحد الثاني: $\\log$ بدون أساس يعني أساس 10. نحوّله لـ ln: نقسم على $\\ln10$، وهو رقم ثابت.'),
                      ('tex', r"\left(\ln\left|\tanh2x\right|\right)'=\frac{2\operatorname{sech}^{2}2x}{\tanh2x}",
                       [('diff(log(tanh(2*x)),x)', '2*sech(2*x)**2/tanh(2*x)', 't')],
                       'مشتقة $\\ln|\\ldots|$ = مشتقة اللي داخلها ÷ اللي داخلها. ومن 4.1 مشتقة $\\tanh2x$ هي $2\\operatorname{sech}^22x$.'),
                      ('line', '2*x*log(3)*3**(x**2-1)/sqrt(3**(2*x**2-2)-1)+2*sech(2*x)**2/(tanh(2*x)*log(10))',
                       'نجمع الحدين. والحد الثاني مقسوم على $\\ln10$.')])
    return U


# ---------------------------------------------------------------- 3
def u_six():
    U = Unit('U-I1', 'جدول التكاملات الستة', '4.2', 'ص59–60', 1)
    U.add('idea', 'الفكرة', p(rich(
        'التكامل عكس الاشتقاق. كل قانون مشتقة في النوع 1 يعطي قانون تكامل. '
        'شغلك ترتّب السؤال على شكل القانون: حد مربع $u^2$، ورقم مربع $a^2$، و $du$ في البسط.')))
    U.add('sign', 'العلامة', p(rich('إذا شفت تكامل كسر، وفي المقام جذر فيه مربع زائد رقم أو مربع ناقص رقم، '
                                    'والبسط رقم أو مشتقة اللي داخل المربع.'))
          + contrast([(r'\int\frac{dx}{\sqrt{x^{2}+49}}', 'قانون $\\sinh^{-1}$', 'البسط رقم، وتحت الجذر مربع زائد رقم'),
                      (r'\int\frac{x\,dx}{\sqrt{x^{2}+49}}', 'تعويض $w=x^2+49$', 'البسط $x$، يعني مشتقة اللي تحت الجذر كله تقريبًا'),
                      (r'\int\frac{dx}{\sqrt{49-x^{2}}}', '$\\sin^{-1}$ (درس 3.4)', 'رقم ناقص مربع تحت الجذر')]))
    U.prev('في النوعين 1 و 2 كنا نشتق. هنا أول تكامل في 4.2، ونستعمل نفس الجدول بالعكس.')
    r = [formula('1/sqrt(u**2+a**2)', 'asinh(u/a)', pos=('a',), label='U-I1 law sinh'),
         formula('1/sqrt(u**2-a**2)', 'acosh(u/a)', branches=('a+t',), pos=('a',), label='U-I1 law cosh'),
         formula('1/(a**2-u**2)', 'atanh(u/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-I1 law tanh'),
         formula('1/(a**2-u**2)', 'acoth(u/a)/a', branches=('a+t', '-a-t'), pos=('a',), label='U-I1 law coth'),
         formula('1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-I1 law sech'),
         formula('1/(u*sqrt(a**2+u**2))', '-acsch(Abs(u)/a)/a', pos=('a',), label='U-I1 law csch')]
    conds = ['كل ' + mi('u'), mi('u>a'), mi('|u|<a'), mi('|u|>a'), mi('0<|u|<a'), mi(r'u\neq0')]
    law = table(['التكامل', 'الجواب (+C)', 'الشرط'], [frow(z, c) for z, c in zip(r, conds)], 'formula')
    law += p(rich('$a$ رقم موجب: الرقم اللي مربعه في السؤال. أول قانونين (جذر لحاله) بدون $\\frac1a$، والأربعة الباقية فيها $\\frac1a$.'), 'small')
    U.add('short', '📐 القانون: جدول التكاملات الستة', law + method([
        'نكتب كل حد تحت الجذر كمربع: $(\\ldots)^2$ و $a^2$.',
        'نسمّي اللي داخل المربع $u$، ونشتقه عشان نطلع $du$.',
        'نكتب البسط بدلالة $du$. الرقم اللي يطلع من التعويض يروح برّا التكامل.',
        'نختار القانون من الجدول، ونرجع $u$.'], tricks_=[
        ('رقم التعديل: البسط ناقصه رقم عشان يصير $du$؟ نقسم عليه برّا. مثال: $u=3x^2$ يعني $du=6x\\,dx$، '
         'والبسط $x\\,dx$، فالبسط $=\\frac16du$.', [('diff(3*x**2,x)/6', 'x')]),
        ('نكتب اللي تحت الجذر كمربع: $9x^4=(3x^2)^2$، يعني $u=3x^2$.', [('9*x**4', '(3*x**2)**2')])], label='U-I1'))
    it = ITEMS['N42-E2-3']
    ex = question(it, 'U-I1 example 1')
    ex += steps(it, [
        ('tex', r'4x^{2}+25=(2x)^{2}+5^{2}', [('4*x**2+25', '(2*x)**2+5**2')],
         'تحت الجذر مو مكتوب كمربعات. جذر 4 هو 2، فـ $4x^2=(2x)^2$. و $25=5^2$.'),
        ('sub', '2*x', '2', 'نسمّي اللي داخل المربع $u$. مشتقة $2x$ هي 2.'),
        ('tex', r'dx=\frac{du}{2}', [('diff(2*x,x)/2', '1')], 'هنا التريك، رقم التعديل: $du$ فيه 2 والبسط $dx$ ما فيه، فنقسم على 2.'),
        ('tex', r'\int\frac{dx}{\sqrt{4x^{2}+25}}=\frac12\int\frac{du}{\sqrt{u^{2}+5^{2}}}',
         [('1/sqrt(4*x**2+25)', 'Rational(1,2)*diff(2*x,x)/sqrt((2*x)**2+5**2)')],
         'نعوّض. الرقم $\\frac12$ ثابت، فيطلع برّا التكامل.'),
        ('tex', r'=\frac12\sinh^{-1}\frac{u}{5}', [('diff(asinh(x/5),x)', '1/sqrt(x**2+25)')],
         'القانون: $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$، وهنا $a=5$.'),
        ('line', 'asinh(2*x/5)/2', 'نرجع $u=2x$.')], 'U-I1 ex1')
    ex += final(it, 'U-I1 example 1')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    it = ITEMS['N42-X2-01']
    ex = question(it, 'U-I1 example 2')
    ex += steps(it, [
        ('tex', r'9+16x^{6}=3^{2}+\left(4x^{3}\right)^{2}', [('9+16*x**6', '3**2+(4*x**3)**2')],
         'نكتب كل حد كمربع. جذر 16 هو 4، ونص الأس 6 هو 3، فـ $16x^6=(4x^3)^2$. و $9=3^2$.'),
        ('sub', '4*x**3', '12*x**2', 'نسمّي اللي داخل المربع $u$. مشتقة $4x^3$ هي $12x^2$.'),
        ('tex', r'x^{2}\,dx=\frac{du}{12}', [('diff(4*x**3,x)/12', 'x**2')],
         'هنا التريك، رقم التعديل: $du$ فيه 12 والبسط ما فيه، فنقسم على 12.'),
        ('tex', r'\int\frac{5x^{2}\,dx}{\sqrt{9+16x^{6}}}=5\cdot\frac{1}{12}\int\frac{du}{\sqrt{u^{2}+3^{2}}}',
         [('5*x**2/sqrt(9+16*x**6)', '5*Rational(1,12)*diff(4*x**3,x)/sqrt((4*x**3)**2+3**2)')],
         'نعوّض. البسط $5x^2\\,dx$ يصير $5\\cdot\\frac{du}{12}$، والأرقام تطلع برّا التكامل.'),
        ('tex', r'5\cdot\frac{1}{12}=\frac{5}{12}', [('5*Rational(1,12)', 'Rational(5,12)')], 'نضرب الرقمين: $5\\times1=5$ فوق، و 12 تحت.'),
        ('tex', r'=\frac{5}{12}\sinh^{-1}\frac{u}{3}', [('diff(asinh(x/3),x)', '1/sqrt(x**2+9)')],
         'القانون: $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$، وهنا $a=3$.'),
        ('line', '5*asinh(4*x**3/3)/12', 'نرجع $u=4x^3$.')], 'U-I1 ex2')
    ex += final(it, 'U-I1 example 2')
    U.add('ex', '🧱 مثال 2 محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تنسى الرقم اللي يطلع من التعويض، مثل $\\frac12$ أو $\\frac{5}{12}$.'),
                                rich('$\\cosh^{-1}$ يصح بس لما $u>a$، زي ما تشترط مذكرة د. طارق.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'4x^{2}+25=(2x)^{2}+5^{2}', [('4*x**2+25', '(2*x)**2+5**2')], 'U-I1 paper 1'))
          + md(arith(r'u=2x\qquad du=2\,dx', [('diff(2*x,x)', '2')], 'U-I1 paper 2'))
          + md(arith(r'\int\frac{dx}{\sqrt{4x^{2}+25}}=\frac12\int\frac{du}{\sqrt{u^{2}+5^{2}}}=\frac12\sinh^{-1}\frac{2x}{5}+C',
                     [('1/sqrt(4*x**2+25)', 'Rational(1,2)*diff(2*x,x)/sqrt((2*x)**2+5**2)'),
                      ('diff(asinh(2*x/5)/2,x)', '1/sqrt(4*x**2+25)')], 'U-I1 paper 3')))
    U.add('ok', '✔ تأكد', p(rich('اشتق جوابك: لازم يرجع السؤال بنفس الرقم في البسط. إذا طلع الرقم ضعفه أو نصه، راجع رقم التعديل.')))
    U.gist('تكامل، وتحت الجذر مربع زائد رقم أو مربع ناقص رقم', 'اكتب كل حد كمربع، وسمّ اللي داخل المربع $u$',
           'رقم التعديل برّا. ثم زائد يعني $\\sinh^{-1}$، وناقص يعني $\\cosh^{-1}$')
    U.drill('1', 'N42-E2-1', 'G', 'نسمّي $u=x^2$. وتحت الجذر ناقص، فالقانون $\\cosh^{-1}$.',
            first=r'x^{4}-16=\left(x^{2}\right)^{2}-4^{2}',
            claims=[('x**4-16', '(x**2)**2-4**2')],
            sol_rows=[('sub', 'x**2', '2*x', 'نسمّي اللي داخل المربع $u$. مشتقة $x^2$ هي $2x$.'),
                      ('tex', r'x\,dx=\frac{du}{2}', [('diff(x**2,x)/2', 'x')], 'رقم التعديل: $du$ فيه 2 والبسط ما فيه، فنقسم على 2.'),
                      ('tex', r'\int\frac{x\,dx}{\sqrt{x^{4}-16}}=\frac12\int\frac{du}{\sqrt{u^{2}-4^{2}}}',
                       [('x/sqrt(x**4-16)', 'Rational(1,2)*diff(x**2,x)/sqrt((x**2)**2-4**2)')], 'نعوّض، والرقم $\\frac12$ يطلع برّا التكامل.'),
                      ('tex', r'=\frac12\cosh^{-1}\frac{u}{4}', [('diff(acosh(x/4),x)', '1/sqrt(x**2-16)', '4+t')],
                       'القانون: $\\int\\frac{du}{\\sqrt{u^2-a^2}}=\\cosh^{-1}\\frac ua$، وهنا $a=4$.'),
                      ('line', 'acosh(x**2/4)/2', 'نرجع $u=x^2$.')])
    U.drill('2', 'N42-X2-02', 'P', '$u=5x^2$، و $a=4$.',
            sol_rows=[('tex', r'25x^{4}+16=\left(5x^{2}\right)^{2}+4^{2}', [('25*x**4+16', '(5*x**2)**2+4**2')],
                       'نكتب كل حد كمربع. جذر 25 هو 5، ونص الأس 4 هو 2. و $16=4^2$.'),
                      ('sub', '5*x**2', '10*x', 'نسمّي اللي داخل المربع $u$. مشتقة $5x^2$ هي $10x$.'),
                      ('tex', r'x\,dx=\frac{du}{10}', [('diff(5*x**2,x)/10', 'x')], 'رقم التعديل: نقسم على 10.'),
                      ('tex', r'\int\frac{3x\,dx}{\sqrt{25x^{4}+16}}=\frac{3}{10}\int\frac{du}{\sqrt{u^{2}+4^{2}}}',
                       [('3*x/sqrt(25*x**4+16)', 'Rational(3,10)*diff(5*x**2,x)/sqrt((5*x**2)**2+4**2)')],
                       'نعوّض. البسط $3x\\,dx$ يصير $3\\cdot\\frac{du}{10}=\\frac{3}{10}du$.'),
                      ('tex', r'=\frac{3}{10}\sinh^{-1}\frac{u}{4}', [('diff(asinh(x/4),x)', '1/sqrt(x**2+16)')],
                       'القانون: $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$، وهنا $a=4$.'),
                      ('line', '3*asinh(5*x**2/4)/10', 'نرجع $u=5x^2$.')])
    U.drill('3', '1447-S2-SE-Q3.2', 'I', '$u=\\ln|x|$، ومشتقته $\\frac1x$ موجودة.',
            sol_rows=[('sub', 'log(Abs(x))', '1/x', 'تحت الجذر $(\\ln|x|)^2$، ومشتقة $\\ln|x|$ هي $\\frac1x$ وموجودة في السؤال. نسمّيه $u$.', 'u', 't'),
                      ('tex', r'\int\frac{dx}{x\sqrt{\left(\ln|x|\right)^{2}-1}}=\int\frac{du}{\sqrt{u^{2}-1^{2}}}',
                       [('1/(x*sqrt(log(x)**2-1))', 'diff(log(x),x)/sqrt(log(x)**2-1**2)')],
                       'نعوّض: $\\frac{dx}{x}$ هو $du$ تمامًا، فما فيه رقم تعديل.'),
                      ('tex', r'=\cosh^{-1}u', [('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t')],
                       'القانون: $\\int\\frac{du}{\\sqrt{u^2-a^2}}=\\cosh^{-1}\\frac ua$، وهنا $a=1$.'),
                      ('line', 'acosh(log(Abs(x)))', 'نرجع $u=\\ln|x|$.')])
    return U


# ---------------------------------------------------------------- 4
def u_tanh():
    U = Unit('U-I2', 'tanh⁻¹ أم coth⁻¹؟', '4.2', 'ص60، تمارين 3 و6', 2)
    U.add('idea', 'الفكرة', p(rich(
        '$\\int\\frac{du}{a^2-u^2}$ له جوابين بنفس الصيغة: $\\frac1a\\tanh^{-1}\\frac ua$ و $\\frac1a\\coth^{-1}\\frac ua$. '
        '$\\tanh^{-1}$ تقبل بس أرقام بين $-1$ و 1، و $\\coth^{-1}$ تقبل بس اللي برّاها. '
        'فنقارن $|u|$ مع $a$ عشان نعرف أي واحد.')))
    U.add('sign', 'العلامة', p(rich('إذا شفت تكامل كسر <b>بدون جذر</b>، وفي المقام رقم ناقص مربع، والبسط مشتقة اللي داخل المربع.'))
          + contrast([(r'\int\frac{dx}{49-x^{2}}', 'قانون $\\tanh^{-1}$ أو $\\coth^{-1}$', 'رقم ناقص مربع، بدون جذر'),
                      (r'\int\frac{x\,dx}{49-x^{2}}', '$-\\frac12\\ln|49-x^2|$', 'البسط $x$، يعني مشتقة المقام تقريبًا'),
                      (r'\int\frac{dx}{49+x^{2}}', '$\\tan^{-1}$ (مو من هذا الدرس)', 'مجموع، مو فرق')]))
    U.prev('في النوع 3 كان في المقام جذر. هنا ما فيه جذر، فالجواب $\\tanh^{-1}$ أو $\\coth^{-1}$.')
    r = [formula('1/(a**2-u**2)', 'atanh(u/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-I2 law tanh'),
         formula('1/(a**2-u**2)', 'acoth(u/a)/a', branches=('a+t', '-a-t'), pos=('a',), label='U-I2 law coth')]
    law = table(['التكامل', 'الجواب (+C)', 'متى'], [frow(r[0], mi('|u|<a')), frow(r[1], mi('|u|>a'))], 'formula')
    U.add('short', '📐 القانون: tanh⁻¹ و coth⁻¹', law + method([
        'نكتب المقام كمربعين: $a^2-u^2$. وإذا طلع مقلوب ($u^2-a^2$)، نطلّع سالب أول.',
        'نسمّي اللي داخل المربع $u$، ونطلع $du$ ونعوّض.',
        'نقارن $|u|$ مع $a$: أصغر يعني $\\tanh^{-1}$، وأكبر يعني $\\coth^{-1}$.',
        'نطبق القانون مع $\\frac1a$، ونرجع $u$.'], tricks_=[
        ('tanh⁻¹ أم coth⁻¹؟ نقارن $u$ مع $a$: أصغر يعني $\\tanh^{-1}$، وأكبر يعني $\\coth^{-1}$. '
         'مثال: $u=e^x$ و $a=5$ و $x<0$، فـ $u<1<5$، يعني $\\tanh^{-1}$.', [('exp(0)', '1')]),
        ('رقم التعديل: $u=x^4$ يعني $du=4x^3dx$. والبسط $x^3dx$ ناقصه 4، فالبسط $=\\frac14du$.', [('diff(x**4,x)/4', 'x**3')])],
        label='U-I2'))
    it = ITEMS['N42-E2-2']
    ex = question(it, 'U-I2 example 1')
    ex += steps(it, [
        ('tex', r'25-e^{2x}=5^{2}-\left(e^{x}\right)^{2}', [('25-exp(2*x)', '5**2-exp(x)**2')],
         'المقام بدون جذر: رقم ناقص أسية. نكتبه كمربعين: $e^{2x}=(e^x)^2$ لأن $x\\cdot2=2x$، و $25=5^2$.'),
        ('sub', 'exp(x)', 'exp(x)', 'نسمّي اللي داخل المربع $u$. مشتقة $e^x$ هي نفسها.'),
        ('tex', r'\int\frac{e^{x}\,dx}{25-e^{2x}}=\int\frac{du}{5^{2}-u^{2}}', [('exp(x)/(25-exp(2*x))', 'diff(exp(x),x)/(5**2-exp(x)**2)')],
         'نعوّض. البسط $e^x\\,dx$ هو $du$ تمامًا، فما فيه رقم تعديل.'),
        ('tex', r'e^{x}<e^{\ln5}=5', [('exp(log(5))', '5')],
         'هنا التريك: نقارن $u$ مع $a=5$. مذكرة د. طارق تاخذ $x<\\ln5$، يعني $e^x<5$، يعني $|u|<a$.'),
        ('tex', r'=\frac15\tanh^{-1}\frac{u}{5}', [('diff(atanh(x/5)/5,x)', '1/(25-x**2)')],
         '$|u|<a$، فالقانون: $\\int\\frac{du}{a^2-u^2}=\\frac1a\\tanh^{-1}\\frac ua$، وهنا $a=5$.'),
        ('line', 'atanh(exp(x)/5)/5', 'نرجع $u=e^x$.')], 'U-I2 ex1')
    ex += final(it, 'U-I2 example 1')
    ex += p(rich('وإذا كان $e^x>5$، يصير الجواب $' + arith(r'\frac15\coth^{-1}\frac{e^{x}}{5}+C',
                                                          [('diff(acoth(exp(x)/5)/5,x)', 'exp(x)/(25-exp(2*x))', 'log(5)+t')],
                                                          'U-I2 ex1 other side') + '$.'), 'small')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    it = ITEMS['N42-X2-06']
    ex = question(it, 'U-I2 example 2')
    ex += steps(it, [
        ('tex', r'4-25\cosh^{2}x=2^{2}-(5\cosh x)^{2}', [('4-25*cosh(x)**2', '2**2-(5*cosh(x))**2')],
         'المقام رقم ناقص مربع، بدون جذر. نكتبه كمربعين: جذر 25 هو 5، و $4=2^2$.'),
        ('sub', '5*cosh(x)', '5*sinh(x)', 'نسمّي اللي داخل المربع $u$. مشتقة $\\cosh x$ هي $\\sinh x$ (من 4.1).'),
        ('tex', r'\sinh x\,dx=\frac{du}{5}', [('diff(5*cosh(x),x)/5', 'sinh(x)')],
         'رقم التعديل: $du$ فيه 5 والبسط ما فيه، فنقسم على 5.'),
        ('tex', r'\int\frac{\sinh x\,dx}{4-25\cosh^{2}x}=\frac15\int\frac{du}{2^{2}-u^{2}}',
         [('sinh(x)/(4-25*cosh(x)**2)', 'Rational(1,5)*diff(5*cosh(x),x)/(2**2-(5*cosh(x))**2)')],
         'نعوّض، والرقم $\\frac15$ يطلع برّا التكامل.'),
        ('tex', r'u=5\cosh x\ge5\cosh0=5>2', [('5*cosh(0)', '5')],
         'هنا التريك: نقارن $u$ مع $a=2$. أصغر قيمة لـ $\\cosh x$ هي 1، فـ $u$ دايم 5 أو أكبر. يعني $|u|>a$.'),
        ('tex', r'=\frac15\cdot\frac12\coth^{-1}\frac{u}{2}', [('diff(acoth(x/2)/2,x)', '1/(4-x**2)')],
         '$|u|>a$، فالقانون: $\\int\\frac{du}{a^2-u^2}=\\frac1a\\coth^{-1}\\frac ua$، وهنا $a=2$.'),
        ('tex', r'\frac15\cdot\frac12=\frac{1}{10}', [('Rational(1,5)*Rational(1,2)', 'Rational(1,10)')],
         'نضرب الكسرين: فوق في فوق، وتحت في تحت.'),
        ('line', 'acoth(5*cosh(x)/2)/10', 'نرجع $u=5\\cosh x$.')], 'U-I2 ex2')
    ex += final(it, 'U-I2 example 2')
    U.add('ex', '🧱 مثال 2 محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تختار $\\tanh^{-1}$ دايم. قارن $|u|$ مع $a$ أول.'),
                                rich('مذكرة د. طارق ص60 كتبت قانون $\\coth^{-1}$ بإشارة سالبة. الحساب يعطي موجبة، مثل $\\tanh^{-1}$ '
                                     '(شوف تنبيه النوع 1).')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'4-25\cosh^{2}x=2^{2}-(5\cosh x)^{2}', [('4-25*cosh(x)**2', '2**2-(5*cosh(x))**2')], 'U-I2 paper 1'))
          + md(arith(r'u=5\cosh x\qquad du=5\sinh x\,dx\qquad u\ge5>2', [('diff(5*cosh(x),x)', '5*sinh(x)'), ('5*cosh(0)', '5')], 'U-I2 paper 2'))
          + md(arith(r'\int\frac{\sinh x\,dx}{4-25\cosh^{2}x}=\frac15\int\frac{du}{2^{2}-u^{2}}=\frac{1}{10}\coth^{-1}\frac{5\cosh x}{2}+C',
                     [('sinh(x)/(4-25*cosh(x)**2)', 'Rational(1,5)*diff(5*cosh(x),x)/(2**2-(5*cosh(x))**2)'),
                      ('diff(acoth(5*cosh(x)/2)/10,x)', 'sinh(x)/(4-25*cosh(x)**2)')], 'U-I2 paper 3')))
    U.add('ok', '✔ تأكد', p(rich('ارجع لسطر المقارنة قبل ما تكتب الجواب: $|u|$ أصغر من $a$ يعني $\\tanh^{-1}$، وأكبر يعني $\\coth^{-1}$. '
                                 'وتأكد إن $\\frac1a$ قدّام الجواب.')))
    U.gist('تكامل كسر بدون جذر، وفي المقام رقم ناقص مربع', 'اكتب المقام $a^2-u^2$، وسمّ $u$',
           'قارن $|u|$ مع $a$: أصغر $\\tanh^{-1}$، وأكبر $\\coth^{-1}$، ومعهم $\\frac1a$')
    U.drill('1', 'G-83', 'G', 'هنا $u=x$ و $a=3$.',
            first=r'9-x^{2}=3^{2}-x^{2}', claims=[('9-x**2', '3**2-x**2')],
            sol_rows=[('tex', r'u=x,\qquad du=dx,\qquad a=3', [('diff(x,x)', '1'), ('3**2', '9')],
                       'نقارن مع القانون $\\int\\frac{du}{a^2-u^2}$. اللي داخل المربع $x$ لحالها، فما فيه رقم تعديل.'),
                      ('tex', r'|x|>3:\qquad\frac13\coth^{-1}\frac{x}{3}+C', [('diff(acoth(x/3)/3,x)', '1/(9-x**2)')],
                       'لو $|x|>3$، يعني $|u|>a$، فالقانون $\\frac1a\\coth^{-1}\\frac ua$.'),
                      ('line', 'atanh(x/3)/3', 'ولو $|x|<3$، يعني $|u|<a$، فالقانون $\\frac1a\\tanh^{-1}\\frac ua$. هذا الجواب لما $x$ قريب من 0.')])
    U.drill('2', 'N42-X2-03', 'P', '$u=3x^4$ و $a=6$. وقريب من 0 يعني $\\tanh^{-1}$.',
            sol_rows=[('tex', r'36-9x^{8}=6^{2}-\left(3x^{4}\right)^{2}', [('36-9*x**8', '6**2-(3*x**4)**2')],
                       'المقام بدون جذر. نكتبه كمربعين: جذر 9 هو 3، ونص الأس 8 هو 4. و $36=6^2$.'),
                      ('sub', '3*x**4', '12*x**3', 'نسمّي اللي داخل المربع $u$. مشتقة $3x^4$ هي $12x^3$.'),
                      ('tex', r'x^{3}dx=\frac{du}{12}', [('diff(3*x**4,x)/12', 'x**3')], 'رقم التعديل: نقسم على 12.'),
                      ('tex', r'\int\frac{x^{3}dx}{36-9x^{8}}=\frac{1}{12}\int\frac{du}{6^{2}-u^{2}}',
                       [('x**3/(36-9*x**8)', 'Rational(1,12)*diff(3*x**4,x)/(6**2-(3*x**4)**2)')], 'نعوّض، والرقم $\\frac{1}{12}$ يطلع برّا التكامل.'),
                      ('tex', r'=\frac{1}{12}\cdot\frac16\tanh^{-1}\frac{u}{6}', [('diff(atanh(x/6)/6,x)', '1/(36-x**2)')],
                       'لما $x$ قريب من 0، $|u|<6$. فالقانون $\\frac1a\\tanh^{-1}\\frac ua$ مع $a=6$.'),
                      ('tex', r'\frac{1}{12}\cdot\frac16=\frac{1}{72}', [('Rational(1,12)*Rational(1,6)', 'Rational(1,72)')],
                       'نضرب الكسرين: $12\\times6=72$ تحت.'),
                      ('tex', r'\frac{u}{6}=\frac{3x^{4}}{6}=\frac{x^{4}}{2}', [('3*x**4/6', 'x**4/2')], 'نرجع $u=3x^4$، ونختصر 3 مع 6.'),
                      ('line', 'atanh(x**4/2)/72', 'نكتب الجواب كامل بدلالة $x$.')])
    U.drill('3', 'G-15', 'I', '$u=e^{2x}$ و $a=3$. وإذا $e^{2x}<3$ فهو $\\tanh^{-1}$.',
            sol_rows=[('tex', r'9-e^{4x}=3^{2}-\left(e^{2x}\right)^{2}', [('9-exp(4*x)', '3**2-exp(2*x)**2')],
                       'نكتب المقام كمربعين: $e^{4x}=(e^{2x})^2$ لأن $2x\\cdot2=4x$، و $9=3^2$.'),
                      ('sub', 'exp(2*x)', '2*exp(2*x)', 'نسمّي اللي داخل المربع $u$. مشتقة $e^{2x}$ هي $2e^{2x}$.'),
                      ('tex', r'e^{2x}dx=\frac{du}{2}', [('diff(exp(2*x),x)/2', 'exp(2*x)')], 'رقم التعديل: نقسم على 2.'),
                      ('tex', r'\int\frac{e^{2x}dx}{9-e^{4x}}=\frac12\int\frac{du}{3^{2}-u^{2}}',
                       [('exp(2*x)/(9-exp(4*x))', 'Rational(1,2)*diff(exp(2*x),x)/(3**2-exp(2*x)**2)')], 'نعوّض، والرقم $\\frac12$ يطلع برّا.'),
                      ('tex', r'=\frac12\cdot\frac13\tanh^{-1}\frac{u}{3}', [('diff(atanh(x/3)/3,x)', '1/(9-x**2)')],
                       'ناخذ $e^{2x}<3$، يعني $|u|<a$. فالقانون $\\frac1a\\tanh^{-1}\\frac ua$ مع $a=3$. ولو $e^{2x}>3$ يصير $\\coth^{-1}$.'),
                      ('tex', r'\frac12\cdot\frac13=\frac16', [('Rational(1,2)*Rational(1,3)', 'Rational(1,6)')], 'نضرب الكسرين.'),
                      ('line', 'atanh(exp(2*x)/3)/6', 'نرجع $u=e^{2x}$.')])
    U.drill('4', 'M-10', 'I', '$u=x^2$، والمقام مقلوب: نطلّع سالب. و $u$ أكبر من 4.',
            sol_rows=[('tex', r'x^{4}-16=\left(x^{2}\right)^{2}-4^{2}', [('x**4-16', '(x**2)**2-4**2')],
                       'نحسب التكامل أول بدون الحدود. نكتب المقام كمربعين: $x^4=(x^2)^2$، و $16=4^2$.'),
                      ('sub', 'x**2', '2*x', 'نسمّي اللي داخل المربع $u$. مشتقة $x^2$ هي $2x$.'),
                      ('tex', r'x\,dx=\frac{du}{2}', [('diff(x**2,x)/2', 'x')], 'رقم التعديل: نقسم على 2.'),
                      ('tex', r'\int\frac{x\,dx}{x^{4}-16}=\frac12\int\frac{du}{u^{2}-4^{2}}',
                       [('x/(x**4-16)', 'Rational(1,2)*diff(x**2,x)/((x**2)**2-4**2)')], 'نعوّض، والرقم $\\frac12$ يطلع برّا.'),
                      ('tex', r'\frac{1}{u^{2}-4^{2}}=-\frac{1}{4^{2}-u^{2}}', [('1/(x**2-16)', '-1/(16-x**2)')],
                       'المقام مقلوب عن القانون. نطلّع سالب: $u^2-16=-(16-u^2)$.'),
                      ('tex', r'=-\frac12\int\frac{du}{4^{2}-u^{2}}', [('x/(x**4-16)', '-Rational(1,2)*diff(x**2,x)/(4**2-(x**2)**2)')],
                       'السالب يطلع برّا التكامل مع $\\frac12$.'),
                      ('tex', r'4\le x\le8\qquad16\le u\le64', [('4**2', '16'), ('8**2', '64')],
                       'نقارن $u$ مع $a=4$. $x$ بين 4 و 8، فـ $u=x^2$ بين 16 و 64، وأكبر من 4. يعني $\\coth^{-1}$.'),
                      ('tex', r'=-\frac12\cdot\frac14\coth^{-1}\frac{u}{4}', [('diff(acoth(x/4)/4,x)', '1/(16-x**2)')],
                       'القانون: $\\int\\frac{du}{a^2-u^2}=\\frac1a\\coth^{-1}\\frac ua$، وهنا $a=4$.'),
                      ('tex', r'-\frac12\cdot\frac14=-\frac18', [('-Rational(1,2)*Rational(1,4)', '-Rational(1,8)')], 'نضرب الكسرين.'),
                      ('tex', r'F(x)=-\frac18\coth^{-1}\frac{x^{2}}{4}', [('diff(-acoth(x**2/4)/8,x)', 'x/(x**4-16)')],
                       'نرجع $u=x^2$. هذا $F(x)$، التكامل بدون الحدود.'),
                      ('tex', r'F(8)=-\frac18\coth^{-1}\frac{8^{2}}{4}=-\frac18\coth^{-1}16', [('-acoth(Rational(8**2,4))/8', '-acoth(16)/8')],
                       'نعوّض الحد الأعلى: $8^2=64$، و $\\frac{64}{4}=16$.'),
                      ('tex', r'F(4)=-\frac18\coth^{-1}\frac{4^{2}}{4}=-\frac18\coth^{-1}4', [('-acoth(Rational(4**2,4))/8', '-acoth(4)/8')],
                       'نعوّض الحد الأدنى: $4^2=16$، و $\\frac{16}{4}=4$.'),
                      ('tex', r'F(8)-F(4)=\frac18\coth^{-1}4-\frac18\coth^{-1}16', [('-acoth(16)/8-(-acoth(4)/8)', 'acoth(4)/8-acoth(16)/8')],
                       'أعلى ناقص أدنى. سالب في سالب = موجب. وما فيه $+C$ في المحدد.')])
    return U


# ---------------------------------------------------------------- 5
def u_sech():
    U = Unit('U-I3', 'x في المقام: sech⁻¹ و csch⁻¹', '4.2', 'ص60، تمارين 4 و5 و11', 2)
    U.add('idea', 'الفكرة', p(rich(
        'إذا برّا الجذر $x$ وتحت الجذر قوة لـ $x$، نضرب فوق وتحت في قوة $x$. '
        'الهدف إن اللي برّا الجذر يصير $u$ نفسه، ويطلع $du$ في البسط. '
        'بعدها قانون $\\operatorname{sech}^{-1}$ إذا تحت الجذر ناقص، أو $\\operatorname{csch}^{-1}$ إذا زائد.')))
    U.add('sign', 'العلامة', p(rich('إذا شفت $x$ مضروب برّا الجذر في المقام، وتحت الجذر رقم زائد أو ناقص قوة لـ $x$.')))
    U.prev('في النوعين 3 و 4 كان المقام جذر لحاله أو بدون جذر. هنا $x$ مضروب برّا الجذر، فالقانون $\\operatorname{sech}^{-1}$ أو $\\operatorname{csch}^{-1}$.')
    r = [formula('1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-I3 law sech'),
         formula('1/(u*sqrt(a**2+u**2))', '-acsch(Abs(u)/a)/a', pos=('a',), label='U-I3 law csch')]
    law = table(['التكامل', 'الجواب (+C)', 'الشرط'], [frow(r[0], mi('0<|u|<a')), frow(r[1], mi(r'u\neq0'))], 'formula')
    U.add('short', '📐 القانون: sech⁻¹ و csch⁻¹', law + method([
        'نكتب اللي تحت الجذر كمربعين، فنعرف $u$.',
        'نضرب فوق وتحت في قوة $x$ اللي تخلي اللي برّا الجذر يصير $u$.',
        'نسمّي $u$، ونطلع $du$، ونعوّض. الرقم اللي يطلع من التعويض يروح برّا.',
        'تحت الجذر ناقص يعني $\\operatorname{sech}^{-1}$، وزائد يعني $\\operatorname{csch}^{-1}$. ونكتب $|u|$.'], tricks_=[
        ('$u$ برّا الجذر يعني الجواب يبدأ بسالب و $\\frac1a$، ومعه $|u|$. مثال: '
         '$\\int\\frac{du}{u\\sqrt{u^2+4}}=-\\frac12\\operatorname{csch}^{-1}\\frac{|u|}{2}$.',
         [('diff(-acsch(Abs(x)/2)/2,x)', '1/(x*sqrt(x**2+4))', 't'), ('diff(-acsch(Abs(x)/2)/2,x)', '1/(x*sqrt(x**2+4))', '-t')]),
        ('رقم التعديل: بعد الضرب في $x$، البسط $x\\,dx$ و $du=2x\\,dx$ (مع $u=x^2$)، فالبسط $=\\frac12du$.', [('diff(x**2,x)/2', 'x')])],
        label='U-I3'))
    it = ITEMS['N42-E2-5']
    ex = question(it, 'U-I3 example')
    ex += steps(it, [
        ('tex', r'16-x^{4}=4^{2}-\left(x^{2}\right)^{2}', [('16-x**4', '4**2-(x**2)**2')],
         'نكتب اللي تحت الجذر كمربعين: $x^4=(x^2)^2$، و $16=4^2$. فنبي $u=x^2$.'),
        ('tex', r'\frac{1}{x\sqrt{16-x^{4}}}\cdot\frac{x}{x}=\frac{x}{x^{2}\sqrt{16-x^{4}}}', [('1/(x*sqrt(16-x**4))*x/x', 'x/(x**2*sqrt(16-x**4))')],
         'برّا الجذر $x$ بس، ونبيه $x^2$ عشان يصير $u$. نضرب فوق وتحت في $x$، والضرب في $\\frac xx=1$ ما يغيّر القيمة.'),
        ('sub', 'x**2', '2*x', 'نسمّي $u=x^2$. مشتقته $2x$.'),
        ('tex', r'x\,dx=\frac{du}{2}', [('diff(x**2,x)/2', 'x')], 'هنا التريك، رقم التعديل: $du$ فيه 2 والبسط ما فيه، فنقسم على 2.'),
        ('tex', r'\int\frac{x\,dx}{x^{2}\sqrt{16-x^{4}}}=\frac12\int\frac{du}{u\sqrt{4^{2}-u^{2}}}',
         [('x/(x**2*sqrt(16-x**4))', 'Rational(1,2)*diff(x**2,x)/(x**2*sqrt(4**2-(x**2)**2))')],
         'نعوّض: البسط $\\frac{du}{2}$، و $x^2$ برّا الجذر يصير $u$.'),
        ('tex', r'=\frac12\cdot\left(-\frac14\right)\operatorname{sech}^{-1}\frac{|u|}{4}', [('diff(-asech(Abs(x)/4)/4,x)', '1/(x*sqrt(16-x**2))', '4*t/(1+t)')],
         'تحت الجذر رقم ناقص مربع، و $u$ برّا. القانون: $\\int\\frac{du}{u\\sqrt{a^2-u^2}}=-\\frac1a\\operatorname{sech}^{-1}\\frac{|u|}{a}$، وهنا $a=4$.'),
        ('tex', r'\frac12\cdot\left(-\frac14\right)=-\frac18', [('Rational(1,2)*(-Rational(1,4))', '-Rational(1,8)')],
         'نضرب الكسرين: موجب في سالب = سالب.'),
        ('tex', r'|u|=\left|x^{2}\right|=x^{2}', [('Abs(x**2)', 'x**2')], '$x^2$ موجب دايم، فما نحتاج القيمة المطلقة.'),
        ('line', '-asech(x**2/4)/8', 'نرجع $u=x^2$.')], 'U-I3 ex')
    ex += final(it, 'U-I3 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('إذا $u$ ممكن يكون سالب (مثل $x^3$)، اكتب $|u|$. مفتاح 1445 نساها، فصار جوابه صحيح بس لما $x>0$.'),
                                rich('نضرب في القوة اللي تخلي اللي برّا الجذر يصير $u$. مع $x^6$ نبي $u=x^3$، فنضرب في $x^2$.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\frac{1}{x\sqrt{16-x^{4}}}=\frac{x}{x^{2}\sqrt{4^{2}-(x^{2})^{2}}}', [('1/(x*sqrt(16-x**4))', 'x/(x**2*sqrt(4**2-(x**2)**2))')], 'U-I3 paper 1'))
          + md(arith(r'u=x^{2}\qquad du=2x\,dx', [('diff(x**2,x)', '2*x')], 'U-I3 paper 2'))
          + md(arith(r'\int\frac{dx}{x\sqrt{16-x^{4}}}=\frac12\int\frac{du}{u\sqrt{4^{2}-u^{2}}}=-\frac18\operatorname{sech}^{-1}\frac{x^{2}}{4}+C',
                     [('x/(x**2*sqrt(16-x**4))', 'Rational(1,2)*diff(x**2,x)/(x**2*sqrt(4**2-(x**2)**2))'),
                      ('diff(-asech(x**2/4)/8,x)', '1/(x*sqrt(16-x**4))', '2*t/(1+t)')], 'U-I3 paper 3')))
    U.add('ok', '✔ تأكد', p(rich('الجواب يبدأ بإشارة سالبة دايم. والرقم قدّامه = الرقم اللي طلع من التعويض × $\\frac1a$: هنا $\\frac12\\cdot\\frac14=\\frac18$.')))
    U.gist('$x$ مضروب برّا الجذر، وتحت الجذر رقم وقوة لـ $x$', 'اضرب فوق وتحت في قوة $x$، عشان اللي برّا يصير $u$',
           'تحت الجذر ناقص يعني $\\operatorname{sech}^{-1}$، وزائد يعني $\\operatorname{csch}^{-1}$. والجواب سالب')
    U.drill('1', 'G-16', 'G', 'مثل المثال، لكن تحت الجذر زائد، فالقانون $\\operatorname{csch}^{-1}$.',
            first=r'\frac{1}{x\sqrt{x^{4}+9}}=\frac{x}{x^{2}\sqrt{(x^{2})^{2}+3^{2}}}',
            claims=[('1/(x*sqrt(x**4+9))', 'x/(x**2*sqrt((x**2)**2+3**2))')],
            sol_rows=[('sub', 'x**2', '2*x', 'برّا الجذر صار $x^2$. نسمّيه $u$، ومشتقته $2x$.'),
                      ('tex', r'x\,dx=\frac{du}{2}', [('diff(x**2,x)/2', 'x')], 'رقم التعديل: نقسم على 2.'),
                      ('tex', r'\int\frac{x\,dx}{x^{2}\sqrt{x^{4}+9}}=\frac12\int\frac{du}{u\sqrt{u^{2}+3^{2}}}',
                       [('1/(x*sqrt(x**4+9))', 'Rational(1,2)*diff(x**2,x)/(x**2*sqrt((x**2)**2+3**2))')], 'نعوّض، والرقم $\\frac12$ يطلع برّا.'),
                      ('tex', r'=\frac12\cdot\left(-\frac13\right)\operatorname{csch}^{-1}\frac{|u|}{3}',
                       [('diff(-acsch(Abs(x)/3)/3,x)', '1/(x*sqrt(x**2+9))', 't'), ('diff(-acsch(Abs(x)/3)/3,x)', '1/(x*sqrt(x**2+9))', '-t')],
                       'تحت الجذر زائد. القانون: $\\int\\frac{du}{u\\sqrt{u^2+a^2}}=-\\frac1a\\operatorname{csch}^{-1}\\frac{|u|}{a}$، وهنا $a=3$.'),
                      ('tex', r'\frac12\cdot\left(-\frac13\right)=-\frac16', [('Rational(1,2)*(-Rational(1,3))', '-Rational(1,6)')], 'نضرب الكسرين.'),
                      ('line', '-acsch(x**2/3)/6', 'نرجع $u=x^2$. و $x^2$ موجب، فما نحتاج القيمة المطلقة.')])
    U.drill('2', 'N42-X2-11', 'P', '$u=2x^2$ و $a=5$. وبرّا الجذر $x^2=\\frac u2$.',
            sol_rows=[('tex', r'\frac{5}{x\sqrt{25+4x^{4}}}=\frac{5x}{x^{2}\sqrt{25+4x^{4}}}', [('5/(x*sqrt(25+4*x**4))', '5*x/(x**2*sqrt(25+4*x**4))')],
                       'نضرب فوق وتحت في $x$، عشان برّا الجذر يصير $x^2$.'),
                      ('tex', r'25+4x^{4}=5^{2}+\left(2x^{2}\right)^{2}', [('25+4*x**4', '5**2+(2*x**2)**2')],
                       'نكتب تحت الجذر كمربعين: جذر 4 هو 2، ونص الأس 4 هو 2. و $25=5^2$.'),
                      ('sub', '2*x**2', '4*x', 'نسمّي اللي داخل المربع $u$. مشتقة $2x^2$ هي $4x$.'),
                      ('tex', r'x\,dx=\frac{du}{4}', [('diff(2*x**2,x)/4', 'x')], 'رقم التعديل: نقسم على 4.'),
                      ('tex', r'x^{2}=\frac{u}{2}', [('2*x**2/2', 'x**2')], 'برّا الجذر $x^2$ مو $u$. من $u=2x^2$ نقسم على 2.'),
                      ('tex', r'\int\frac{5x\,dx}{x^{2}\sqrt{25+4x^{4}}}=\int\frac{5\cdot\frac{du}{4}}{\frac{u}{2}\sqrt{5^{2}+u^{2}}}',
                       [('5*x/(x**2*sqrt(25+4*x**4))', '(5*Rational(1,4)*diff(2*x**2,x))/((2*x**2/2)*sqrt(5**2+(2*x**2)**2))')],
                       'نعوّض كل قطعة.'),
                      ('tex', r'=5\cdot\frac14\cdot2\int\frac{du}{u\sqrt{5^{2}+u^{2}}}', [('5/(x*sqrt(25+4*x**4))', '5*Rational(1,4)*2*diff(2*x**2,x)/(2*x**2*sqrt(5**2+(2*x**2)**2))')],
                       'كسر فوق كسر: القسمة على $\\frac u2$ = الضرب في $\\frac2u$. والأرقام تطلع برّا.'),
                      ('tex', r'5\cdot\frac14\cdot2=\frac52', [('5*Rational(1,4)*2', 'Rational(5,2)')], 'نضرب الأرقام: $5\\times2=10$ فوق، و 4 تحت، و $\\frac{10}{4}=\\frac52$.'),
                      ('tex', r'=\frac52\cdot\left(-\frac15\right)\operatorname{csch}^{-1}\frac{|u|}{5}',
                       [('diff(-acsch(Abs(x)/5)/5,x)', '1/(x*sqrt(x**2+25))', 't'), ('diff(-acsch(Abs(x)/5)/5,x)', '1/(x*sqrt(x**2+25))', '-t')],
                       'تحت الجذر زائد. القانون: $-\\frac1a\\operatorname{csch}^{-1}\\frac{|u|}{a}$، وهنا $a=5$.'),
                      ('tex', r'\frac52\cdot\left(-\frac15\right)=-\frac12', [('Rational(5,2)*(-Rational(1,5))', '-Rational(1,2)')],
                       'نضرب الكسرين: 5 فوق مع 5 تحت تروح.'),
                      ('line', '-acsch(2*x**2/5)/2', 'نرجع $u=2x^2$. وهو موجب دايم، فما نحتاج القيمة المطلقة.')])
    U.drill('3', '1445-S2-SE-Q2.4', 'I', 'نضرب في $x^2$ فوق وتحت: $u=x^3$، ونكتب $|x^3|$.',
            sol_rows=[('tex', r'\frac{1}{x\sqrt{x^{6}+25}}=\frac{x^{2}}{x^{3}\sqrt{x^{6}+25}}', [('1/(x*sqrt(x**6+25))', 'x**2/(x**3*sqrt(x**6+25))')],
                       'تحت الجذر $x^6=(x^3)^2$، فنبي $u=x^3$ برّا الجذر. نضرب فوق وتحت في $x^2$.'),
                      ('tex', r'x^{6}+25=\left(x^{3}\right)^{2}+5^{2}', [('x**6+25', '(x**3)**2+5**2')], 'نكتب كمربعين: نص الأس 6 هو 3، و $25=5^2$.'),
                      ('sub', 'x**3', '3*x**2', 'نسمّي $u=x^3$. مشتقته $3x^2$.'),
                      ('tex', r'x^{2}dx=\frac{du}{3}', [('diff(x**3,x)/3', 'x**2')], 'رقم التعديل: نقسم على 3.'),
                      ('tex', r'\int\frac{x^{2}dx}{x^{3}\sqrt{x^{6}+25}}=\frac13\int\frac{du}{u\sqrt{u^{2}+5^{2}}}',
                       [('1/(x*sqrt(x**6+25))', 'Rational(1,3)*diff(x**3,x)/(x**3*sqrt((x**3)**2+5**2))')], 'نعوّض، والرقم $\\frac13$ يطلع برّا.'),
                      ('tex', r'=\frac13\cdot\left(-\frac15\right)\operatorname{csch}^{-1}\frac{|u|}{5}',
                       [('diff(-acsch(Abs(x)/5)/5,x)', '1/(x*sqrt(x**2+25))', 't'), ('diff(-acsch(Abs(x)/5)/5,x)', '1/(x*sqrt(x**2+25))', '-t')],
                       'تحت الجذر زائد. القانون: $-\\frac1a\\operatorname{csch}^{-1}\\frac{|u|}{a}$، وهنا $a=5$.'),
                      ('tex', r'\frac13\cdot\left(-\frac15\right)=-\frac{1}{15}', [('Rational(1,3)*(-Rational(1,5))', '-Rational(1,15)')], 'نضرب الكسرين.'),
                      ('tex', r'|u|=\left|x^{3}\right|=|x|^{3}', [('Abs(x**3)', 'Abs(x)**3')], '$x^3$ ممكن يكون سالب، فنخلي القيمة المطلقة.'),
                      ('line', '-acsch(Abs(x)**3/5)/15', 'نرجع $u=x^3$.')])
    return U


# ---------------------------------------------------------------- 6
def u_lamda():
    U = Unit('U-I4', 'أسية تحت الجذر', '4.2', 'ص61، تمارين 10 و12', 2)
    U.add('idea', 'الفكرة', p(rich(
        'تحت الجذر أسية مثل $e^{6x}$، والبسط رقم بس. مشتقة الأسية مو موجودة فوق، فما نقدر نعوّض على طول. '
        'نضرب فوق وتحت في جذر الأسية (هنا $e^{3x}$). كذا تطلع مشتقتها فوق، ويصير $u$ برّا الجذر. '
        'وهذا شكل قانون $\\operatorname{csch}^{-1}$ أو $\\operatorname{sech}^{-1}$ من النوع 5.')))
    U.add('sign', 'العلامة', p(rich('إذا شفت أسية تحت الجذر زائد أو ناقص رقم، مثل $\\sqrt{e^{6x}+1}$، والبسط رقم بس.'))
          + contrast([(r'\int\frac{dx}{\sqrt{e^{6x}+1}}', 'هذا النوع', 'البسط رقم، ومشتقة الأسية مو فوق'),
                      (r'\int\frac{e^{3x}\,dx}{\sqrt{e^{6x}+1}}', 'النوع 3', 'مشتقة الأسية فوق، فنعوّض $u=e^{3x}$ على طول'),
                      (r'\int\frac{dx}{\sqrt{e^{2x}-1}}', '$\\sec^{-1}$ (درس 3.4)', 'أسية ناقص رقم، وقانونها مو من جدول 4.2')]))
    U.prev('في النوع 5 كان $x$ برّا الجذر من البداية. هنا ما فيه شي برّا الجذر، فنصنعه: نضرب فوق وتحت في جذر الأسية.')
    formula('1/(u*sqrt(u**2+a**2))', '-acsch(Abs(u)/a)/a', pos=('a',), label='U-I4 law csch')
    formula('1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-I4 law sech')
    laws = (md(r'\int\frac{du}{u\sqrt{u^{2}+a^{2}}}=-\frac1a\operatorname{csch}^{-1}\frac{|u|}{a}+C')
            + md(r'\int\frac{du}{u\sqrt{a^{2}-u^{2}}}=-\frac1a\operatorname{sech}^{-1}\frac{|u|}{a}+C'))
    U.add('short', '🧭 الطريقة', method([
        'نكتب الأسية كمربع: نص الأس. مثل $e^{6x}=(e^{3x})^2$.',
        'نضرب فوق وتحت في جذر الأسية ($e^{3x}$)، فيطلع برّا الجذر.',
        'نسمّي $u$ = جذر الأسية. مشتقته صارت فوق، ونقسم على الرقم اللي يطلع معها.',
        '$u^2+a^2$ تحت الجذر يعني قانون $\\operatorname{csch}^{-1}$. و $a^2-u^2$ يعني قانون $\\operatorname{sech}^{-1}$. ثم نرجع $u$.'],
        tricks_=[('أسية تحت الجذر: نضرب فوق وتحت في جذرها. $e^{6x}=(e^{3x})^2$، فنضرب في $e^{3x}$.', [('exp(6*x)', 'exp(3*x)**2')]),
                 ('رقم التعديل: $du=3e^{3x}dx$ والبسط $e^{3x}dx$ بس. فالبسط $=\\frac13du$، ونطلّع $\\frac13$ برّا التكامل.',
                  [('diff(exp(3*x),x)/3', 'exp(3*x)')])], label='U-I4') + laws)
    it = ITEMS['1446-S2-SE-Q2.7']
    ex = question(it, 'U-I4 example')
    ex += steps(it, [
        ('tex', r'e^{6x}=\left(e^{3x}\right)^{2}', [('exp(6*x)', 'exp(3*x)**2')],
         'البسط رقم، ومشتقة الأسية مو فوق. فنجهّزها: نكتب الأسية كمربع، ونص 6 هو 3.'),
        ('tex', r'\frac{1}{\sqrt{e^{6x}+1}}=\frac{e^{3x}}{e^{3x}\sqrt{\left(e^{3x}\right)^{2}+1}}',
         [('1/sqrt(exp(6*x)+1)', 'exp(3*x)/(exp(3*x)*sqrt(exp(3*x)**2+1))')],
         'هنا التريك: نضرب فوق وتحت في $e^{3x}$، فما تتغير القيمة. وصار $e^{3x}$ برّا الجذر.'),
        ('sub', 'exp(3*x)', '3*exp(3*x)', 'نسمّي $u=e^{3x}$، لأنه برّا الجذر وداخله. ومشتقته $3e^{3x}$.'),
        ('tex', r'e^{3x}\,dx=\frac{du}{3}', [('diff(exp(3*x),x)/3', 'exp(3*x)')],
         'فوق عندنا $e^{3x}dx$ بدون 3. فنقسم على 3.'),
        ('tex', r'\int\frac{e^{3x}\,dx}{e^{3x}\sqrt{\left(e^{3x}\right)^{2}+1}}=\frac13\int\frac{du}{u\sqrt{u^{2}+1^{2}}}',
         [('exp(3*x)/(exp(3*x)*sqrt(exp(3*x)**2+1))', 'Rational(1,3)*diff(exp(3*x),x)/(exp(3*x)*sqrt(exp(3*x)**2+1**2))')],
         'نعوّض. صار بنفس شكل القانون، و $\\frac13$ برّا التكامل.'),
        ('tex', r'=-\frac13\operatorname{csch}^{-1}u', [('diff(-acsch(x)/3,x)', '1/(3*x*sqrt(x**2+1))', 't')],
         'القانون: $\\int\\frac{du}{u\\sqrt{u^2+a^2}}=-\\frac1a\\operatorname{csch}^{-1}\\frac{|u|}{a}$، وهنا $a=1$. و $u=e^{3x}$ موجب، فـ $|u|=u$.'),
        ('line', '-acsch(exp(3*x))/3', 'نرجع $u=e^{3x}$.')], 'U-I4 ex')
    ex += final(it, 'U-I4 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('إذا مشتقة الأسية موجودة فوق، مثل $\\frac{e^{x}}{\\sqrt{e^{2x}+1}}$، لا تضرب في شي. هذا النوع 3: $u=e^x$ على طول.'),
                                rich('مع أساس غير $e$ مثل $5^x$: مشتقته $5^x\\ln5$. فيطلع $\\ln5$ تحت في الجواب.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\frac{1}{\sqrt{e^{6x}+1}}=\frac{e^{3x}}{e^{3x}\sqrt{\left(e^{3x}\right)^{2}+1}}',
                   [('1/sqrt(exp(6*x)+1)', 'exp(3*x)/(exp(3*x)*sqrt(exp(3*x)**2+1))')], 'U-I4 paper 1'))
          + md(arith(r'u=e^{3x}\qquad du=3e^{3x}\,dx', [('diff(exp(3*x),x)', '3*exp(3*x)')], 'U-I4 paper 2'))
          + md(arith(r'\frac13\int\frac{du}{u\sqrt{u^{2}+1}}=-\frac13\operatorname{csch}^{-1}e^{3x}+C',
                     [('diff(-acsch(exp(3*x))/3,x)', '1/sqrt(exp(6*x)+1)')], 'U-I4 paper 3')))
    U.add('ok', '✔ تأكد', p(rich('الجواب يبدأ بسالب دايم. والرقم قدّامه = البسط ÷ ($a$ × الرقم اللي في أس $u$). '
                                 'هنا $u=e^{3x}$ و $a=1$، فالرقم $\\frac{1}{1\\times3}=\\frac13$ ✓.')))
    U.gist('أسية تحت الجذر، والبسط رقم بس', 'نضرب فوق وتحت في جذر الأسية، ونسمّيه $u$',
           'زائد تحت الجذر يعني $\\operatorname{csch}^{-1}$، وناقص يعني $\\operatorname{sech}^{-1}$')
    U.drill('1', 'N42-E2-6', 'G', 'نص الأس 2 هو 1، فنضرب فوق وتحت في $e^x$.',
            first=r'\frac{1}{\sqrt{1+e^{2x}}}=\frac{e^{x}}{e^{x}\sqrt{1+\left(e^{x}\right)^{2}}}',
            claims=[('1/sqrt(1+exp(2*x))', 'exp(x)/(exp(x)*sqrt(1+exp(x)**2))')],
            sol_rows=[('sub', 'exp(x)', 'exp(x)', 'نسمّي $u=e^x$. مشتقته $e^x$، وهي فوق كاملة.'),
                      ('tex', r'\int\frac{e^{x}\,dx}{e^{x}\sqrt{1+\left(e^{x}\right)^{2}}}=\int\frac{du}{u\sqrt{u^{2}+1^{2}}}',
                       [('exp(x)/(exp(x)*sqrt(1+exp(x)**2))', 'diff(exp(x),x)/(exp(x)*sqrt(exp(x)**2+1**2))')],
                       'نعوّض. صار بنفس شكل القانون.'),
                      ('line', '-acsch(exp(x))', 'القانون: $-\\frac1a\\operatorname{csch}^{-1}\\frac{|u|}{a}$ مع $a=1$. و $e^x$ موجب. ثم نرجع $u=e^x$.')])
    U.drill('2', '1447-S1-SE-Q2.2', 'P', '$5^{2x}=(5^x)^2$، ومشتقة $5^x$ فيها $\\ln5$.',
            sol_rows=[('tex', r'5^{2x}=\left(5^{x}\right)^{2}', [('5**(2*x)', '(5**x)**2')],
                       'البسط رقم، ومشتقة الأسية مو فوق. نكتب الأسية كمربع: نص الأس $2x$ هو $x$.'),
                      ('tex', r'\frac{1}{\sqrt{5^{2x}+1}}=\frac{5^{x}}{5^{x}\sqrt{\left(5^{x}\right)^{2}+1}}',
                       [('1/sqrt(5**(2*x)+1)', '5**x/(5**x*sqrt((5**x)**2+1))')], 'نضرب فوق وتحت في $5^x$، فيطلع برّا الجذر.'),
                      ('sub', '5**x', '5**x*log(5)', 'نسمّي $u=5^x$. مشتقة $5^x$ هي $5^x\\ln5$.'),
                      ('tex', r'5^{x}\,dx=\frac{du}{\ln5}', [('diff(5**x,x)/log(5)', '5**x')], 'فوق عندنا $5^x dx$ بدون $\\ln5$. فنقسم على $\\ln5$.'),
                      ('tex', r'=\frac{1}{\ln5}\int\frac{du}{u\sqrt{u^{2}+1^{2}}}',
                       [('5**x/(5**x*sqrt((5**x)**2+1))', 'diff(5**x,x)/log(5)/(5**x*sqrt((5**x)**2+1**2))')],
                       'نعوّض، و $\\frac{1}{\\ln5}$ برّا التكامل.'),
                      ('line', '-acsch(5**x)/log(5)', 'القانون $\\operatorname{csch}^{-1}$ مع $a=1$، و $5^x$ موجب. ثم نرجع $u=5^x$.')])
    U.drill('3', 'N42-X2-10', 'I', 'تحت الجذر رقم ناقص أسية، يعني قانون $\\operatorname{sech}^{-1}$ مع $a=3$.',
            sol_rows=[('tex', r'9-e^{6x}=3^{2}-\left(e^{3x}\right)^{2}', [('9-exp(6*x)', '3**2-exp(3*x)**2')],
                       'البسط رقم. نكتب 9 والأسية كمربعين: $9=3^2$، ونص الأس 6 هو 3.'),
                      ('tex', r'\frac{2}{\sqrt{9-e^{6x}}}=\frac{2e^{3x}}{e^{3x}\sqrt{3^{2}-\left(e^{3x}\right)^{2}}}',
                       [('2/sqrt(9-exp(6*x))', '2*exp(3*x)/(exp(3*x)*sqrt(3**2-exp(3*x)**2))')], 'نضرب فوق وتحت في $e^{3x}$.'),
                      ('sub', 'exp(3*x)', '3*exp(3*x)', 'نسمّي $u=e^{3x}$، فـ $e^{3x}dx=\\frac{du}{3}$.'),
                      ('tex', r'=\frac23\int\frac{du}{u\sqrt{3^{2}-u^{2}}}',
                       [('2*exp(3*x)/(exp(3*x)*sqrt(3**2-exp(3*x)**2))', 'Rational(2,3)*diff(exp(3*x),x)/(exp(3*x)*sqrt(3**2-exp(3*x)**2))')],
                       'نعوّض. الرقم 2 فوق مع $\\frac13$ يصير $\\frac23$.'),
                      ('tex', r'\frac23\cdot\left(-\frac13\right)=-\frac29', [('Rational(2,3)*(-Rational(1,3))', '-Rational(2,9)')],
                       'القانون: $-\\frac1a\\operatorname{sech}^{-1}\\frac{|u|}{a}$ مع $a=3$. نضرب الرقمين.'),
                      ('line', '-2*asech(exp(3*x)/3)/9', 'نرجع $u=e^{3x}$. وهو موجب، فـ $|u|=u$.')])
    U.drill('4', 'N42-X2-12', 'I', 'نكتب $x^3=(x^{3/2})^2$، ونضرب فوق وتحت في $x^{1/2}$.',
            sol_rows=[('tex', r'x^{3}=\left(x^{3/2}\right)^{2}', [('x**3', '(x**Rational(3,2))**2', 't')],
                       'نفس الفكرة لكن مع قوة. نكتب $x^3$ كمربع: نص الأس 3 هو $\\frac32$.'),
                      ('tex', r'\frac{1}{x\sqrt{25-x^{3}}}=\frac{x^{1/2}}{x^{3/2}\sqrt{5^{2}-\left(x^{3/2}\right)^{2}}}',
                       [('1/(x*sqrt(25-x**3))', 'x**Rational(1,2)/(x**Rational(3,2)*sqrt(5**2-(x**Rational(3,2))**2))', 't')],
                       'نضرب فوق وتحت في $x^{1/2}$. لأن $x\\cdot x^{1/2}=x^{3/2}$، فيصير برّا الجذر $x^{3/2}$.'),
                      ('sub', 'x**Rational(3,2)', '3*x**Rational(1,2)/2', 'نسمّي $u=x^{3/2}$. مشتقته $\\frac32x^{1/2}$، يعني $x^{1/2}dx=\\frac23du$.', 'u', 't'),
                      ('tex', r'=\frac23\int\frac{du}{u\sqrt{5^{2}-u^{2}}}',
                       [('x**Rational(1,2)/(x**Rational(3,2)*sqrt(5**2-(x**Rational(3,2))**2))',
                         'Rational(2,3)*diff(x**Rational(3,2),x)/(x**Rational(3,2)*sqrt(5**2-(x**Rational(3,2))**2))', 't')],
                       'نعوّض، و $\\frac23$ برّا التكامل.'),
                      ('tex', r'\frac23\cdot\left(-\frac15\right)=-\frac{2}{15}', [('Rational(2,3)*(-Rational(1,5))', '-Rational(2,15)')],
                       'القانون $\\operatorname{sech}^{-1}$ مع $a=5$. نضرب $\\frac23$ في $-\\frac15$.'),
                      ('line', '-2*asech(x**Rational(3,2)/5)/15', 'نرجع $u=x^{3/2}$.')])
    return U


# ---------------------------------------------------------------- 7
def u_sqrt():
    U = Unit('U-I5', 'جذر x مخفي', '4.2', 'ص61، تمرين 2(4)', 2)
    U.add('idea', 'الفكرة', p(rich(
        'في المقام $\\sqrt x$، ومعها جذر ثاني فيه $x$ لحالها. نسمّي $u=\\sqrt x$. '
        'مشتقته $\\frac{1}{2\\sqrt x}$، وهي موجودة في السؤال إلا الرقم 2. '
        'و $x=u^2$، فيصير الجذر الثاني بشكل قانون من جدول 4.2.')))
    U.add('sign', 'العلامة', p(rich('إذا شفت $\\sqrt x$ في المقام، ومعها جذر فيه $x$ لحالها (مو $x^2$)، مثل $\\sqrt{x}\\sqrt{4+x}$.'))
          + contrast([(r'\int\frac{dx}{\sqrt{x}\sqrt{4+x}}', 'هذا النوع', 'تحت الجذر الثاني $x$ لحالها'),
                      (r'\int\frac{dx}{\sqrt{4+x^{2}}}', 'النوع 3', 'تحت الجذر $x^2$، فهو مربع جاهز'),
                      (r'\int\frac{dx}{\sqrt{4+x}}', 'قاعدة القوة', 'ما فيه $\\sqrt x$ برّا: الجواب $2\\sqrt{4+x}$')]))
    U.prev('في النوع 6 كانت أسية تحت الجذر، فضربنا فوق وتحت. هنا $\\sqrt x$ موجودة من البداية، فنسمّيها $u$ على طول.')
    formula('1/sqrt(u**2+a**2)', 'asinh(u/a)', pos=('a',), label='U-I5 law sinh')
    formula('1/sqrt(u**2-a**2)', 'acosh(u/a)', branches=('a+t',), pos=('a',), label='U-I5 law cosh')
    laws = (md(r'\int\frac{du}{\sqrt{u^{2}+a^{2}}}=\sinh^{-1}\frac{u}{a}+C') + md(r'\int\frac{du}{\sqrt{u^{2}-a^{2}}}=\cosh^{-1}\frac{u}{a}+C'))
    U.add('short', '🧭 الطريقة', method([
        'نسمّي $u=\\sqrt x$. يعني $du=\\frac{dx}{2\\sqrt x}$.',
        'نضرب في 2: $\\frac{dx}{\\sqrt x}=2\\,du$.',
        'نكتب $x=u^2$ في الجذر الثاني، لأن $\\sqrt x\\cdot\\sqrt x=x$.',
        'زائد يعني قانون $\\sinh^{-1}$، وناقص يعني قانون $\\cosh^{-1}$. ثم نرجع $u=\\sqrt x$.'],
        tricks_=[('$\\sqrt x$ ومعها $\\frac{1}{\\sqrt x}$؟ يعني $u=\\sqrt x$، و $\\frac{dx}{\\sqrt x}=2\\,du$.', [('2*diff(sqrt(x),x)', '1/sqrt(x)')]),
                 ('نكتب الرقم كمربع عشان نعرف $a$: $4+x=2^2+u^2$، يعني $a=2$.', [('2**2+sqrt(x)**2', '4+x')])], label='U-I5') + laws)
    it = ITEMS['N42-E2-4']
    ex = question(it, 'U-I5 example')
    ex += steps(it, [
        ('sub', 'sqrt(x)', '1/(2*sqrt(x))', 'في المقام $\\sqrt x$ وتحت الجذر الثاني $x$ لحالها. فنسمّي $u=\\sqrt x$.'),
        ('tex', r'\frac{dx}{\sqrt{x}}=2\,du', [('2*diff(sqrt(x),x)', '1/sqrt(x)')],
         'هنا التريك: نضرب الطرفين في 2، عشان يطلع $\\frac{dx}{\\sqrt x}$ اللي في السؤال.'),
        ('tex', r'x=\sqrt{x}\cdot\sqrt{x}=u^{2}', [('sqrt(x)*sqrt(x)', 'x')], 'الجذر في نفسه يعطي اللي تحته. فـ $x=u^2$.'),
        ('tex', r'4+x=2^{2}+u^{2}', [('2**2+sqrt(x)**2', '4+x')], 'نعوّض $x=u^2$، ونكتب 4 كمربع: $4=2^2$.'),
        ('tex', r'\int\frac{dx}{\sqrt{x}\sqrt{4+x}}=2\int\frac{du}{\sqrt{u^{2}+2^{2}}}',
         [('1/(sqrt(x)*sqrt(4+x))', '2*diff(sqrt(x),x)/sqrt(sqrt(x)**2+2**2)')], 'نعوّض. صار بنفس شكل القانون، والـ 2 برّا التكامل.'),
        ('line', '2*asinh(sqrt(x)/2)', 'القانون: $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$، وهنا $a=2$. ثم نرجع $u=\\sqrt x$.')], 'U-I5 ex')
    ex += final(it, 'U-I5 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تنسى الـ 2: $\\frac{dx}{\\sqrt x}=2\\,du$، مو $du$.'),
                                rich('داخل الدالة العكسية $\\sqrt x$، مو $x$: الجواب $2\\sinh^{-1}\\frac{\\sqrt x}{2}$.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'u=\sqrt{x}\qquad du=\frac{dx}{2\sqrt{x}}\qquad \frac{dx}{\sqrt{x}}=2\,du', [('2*diff(sqrt(x),x)', '1/sqrt(x)')], 'U-I5 paper 1'))
          + md(arith(r'4+x=2^{2}+u^{2}', [('2**2+sqrt(x)**2', '4+x')], 'U-I5 paper 2'))
          + md(arith(r'2\int\frac{du}{\sqrt{u^{2}+2^{2}}}=2\sinh^{-1}\frac{\sqrt{x}}{2}+C',
                     [('diff(2*asinh(sqrt(x)/2),x)', '1/(sqrt(x)*sqrt(4+x))', 't')], 'U-I5 paper 3')))
    U.add('ok', '✔ تأكد', p(rich('الجواب فيه 2 قدّام، و $\\sqrt x$ داخل الدالة العكسية. '
                                 'لأن مشتقة $\\sqrt x$ فيها $\\frac12$، والـ 2 اللي قدّام تلغيها ✓.')))
    U.gist('$\\sqrt x$ في المقام، ومعها جذر فيه $x$ لحالها', 'نسمّي $u=\\sqrt x$، و $\\frac{dx}{\\sqrt x}=2\\,du$',
           '$x=u^2$. زائد يعني $\\sinh^{-1}$، وناقص يعني $\\cosh^{-1}$')
    U.drill('1', '1445-S1-SE-Q2.2', 'G', 'نفس المثال، و $1=1^2$.',
            first=r'u=\sqrt{x},\qquad \frac{dx}{\sqrt{x}}=2\,du,\qquad 1+x=1+u^{2}',
            claims=[('2*diff(sqrt(x),x)', '1/sqrt(x)'), ('1+sqrt(x)**2', '1+x')],
            sol_rows=[('tex', r'\int\frac{dx}{\sqrt{x}\sqrt{1+x}}=2\int\frac{du}{\sqrt{u^{2}+1^{2}}}',
                       [('1/(sqrt(x)*sqrt(1+x))', '2*diff(sqrt(x),x)/sqrt(sqrt(x)**2+1**2)')], 'نعوّض. صار بنفس شكل القانون، والـ 2 برّا.'),
                      ('tex', r'=2\sinh^{-1}\frac{u}{1}=2\sinh^{-1}u', [('diff(2*asinh(x),x)', '2/sqrt(x**2+1)')],
                       'القانون: $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$، وهنا $a=1$.'),
                      ('line', '2*asinh(sqrt(x))', 'نرجع $u=\\sqrt x$.')])
    U.drill('2', 'G-85', 'P', 'نفس المثال، و $9=3^2$.',
            sol_rows=[('sub', 'sqrt(x)', '1/(2*sqrt(x))', 'في المقام $\\sqrt x$، فنسمّيها $u$.'),
                      ('tex', r'\frac{dx}{\sqrt{x}}=2\,du', [('2*diff(sqrt(x),x)', '1/sqrt(x)')], 'نضرب الطرفين في 2، عشان يطلع اللي في السؤال.'),
                      ('tex', r'9+x=3^{2}+u^{2}', [('3**2+sqrt(x)**2', '9+x')], 'لأن $\\sqrt x\\cdot\\sqrt x=x$، يعني $x=u^2$. و $9=3^2$.'),
                      ('tex', r'\int\frac{dx}{\sqrt{x}\sqrt{9+x}}=2\int\frac{du}{\sqrt{u^{2}+3^{2}}}',
                       [('1/(sqrt(x)*sqrt(9+x))', '2*diff(sqrt(x),x)/sqrt(sqrt(x)**2+3**2)')], 'نعوّض. صار بنفس شكل القانون.'),
                      ('line', '2*asinh(sqrt(x)/3)', 'القانون $\\sinh^{-1}\\frac ua$ مع $a=3$. ثم نرجع $u=\\sqrt x$.')])
    U.drill('3', 'G-39', 'I', 'نفس التعويض، لكن تحت الجذر ناقص، يعني $\\cosh^{-1}$.',
            sol_rows=[('sub', 'sqrt(x)', '1/(2*sqrt(x))', 'في المقام $\\sqrt x$، فنسمّيها $u$.'),
                      ('tex', r'\frac{dx}{\sqrt{x}}=2\,du', [('2*diff(sqrt(x),x)', '1/sqrt(x)')], 'نضرب الطرفين في 2.'),
                      ('tex', r'x-4=u^{2}-2^{2}', [('sqrt(x)**2-2**2', 'x-4')], 'لأن $x=u^2$، و $4=2^2$.'),
                      ('tex', r'\int\frac{dx}{\sqrt{x}\sqrt{x-4}}=2\int\frac{du}{\sqrt{u^{2}-2^{2}}}',
                       [('1/(sqrt(x)*sqrt(x-4))', '2*diff(sqrt(x),x)/sqrt(sqrt(x)**2-2**2)')], 'نعوّض. صار مربع ناقص رقم.'),
                      ('line', '2*acosh(sqrt(x)/2)', 'القانون: $\\int\\frac{du}{\\sqrt{u^2-a^2}}=\\cosh^{-1}\\frac ua$، و $a=2$. ثم نرجع $u=\\sqrt x$.')])
    U.drill('4', 'G-86', 'I', '$x=\\sqrt x\\cdot\\sqrt x$، فتطلع $\\sqrt x$ في المقام.',
            sol_rows=[('tex', r'\frac{1}{x\sqrt{1+x}}=\frac{1}{\sqrt{x}\cdot\sqrt{x}\,\sqrt{1+x}}', [('1/(x*sqrt(1+x))', '1/(sqrt(x)*sqrt(x)*sqrt(1+x))')],
                       'ما فيه $\\sqrt x$ ظاهرة. لكن $x=\\sqrt x\\cdot\\sqrt x$، فتطلع $\\sqrt x$ في المقام.'),
                      ('sub', 'sqrt(x)', '1/(2*sqrt(x))', 'نسمّي $u=\\sqrt x$.'),
                      ('tex', r'\frac{dx}{\sqrt{x}}=2\,du', [('2*diff(sqrt(x),x)', '1/sqrt(x)')],
                       'نضرب في 2. وتبقى $\\sqrt x$ الثانية، وهي $u$ نفسه.'),
                      ('tex', r'\int\frac{dx}{\sqrt{x}\cdot\sqrt{x}\,\sqrt{1+x}}=2\int\frac{du}{u\sqrt{u^{2}+1^{2}}}',
                       [('1/(x*sqrt(1+x))', '2*diff(sqrt(x),x)/(sqrt(x)*sqrt(sqrt(x)**2+1**2))')],
                       'نعوّض: $\\sqrt x=u$، و $1+x=1+u^2$. صار $u$ برّا الجذر مثل النوع 5.'),
                      ('line', '-2*acsch(sqrt(x))',
                       'القانون: $\\int\\frac{du}{u\\sqrt{u^2+a^2}}=-\\frac1a\\operatorname{csch}^{-1}\\frac{|u|}{a}$، و $a=1$. و $u=\\sqrt x$ موجب.')])
    return U


# ---------------------------------------------------------------- 8
def u_split():
    U = Unit('U-I6', 'بسط مركّب: افصل الكسر', '4.2', 'ص62، تمرينا 7 و8', 2)
    U.add('idea', 'الفكرة', p(rich(
        'البسط فيه حدّين: حد فيه $x$، ورقم. كل حد يحتاج طريقة، فنفصل الكسر لكسرين لهم نفس المقام. '
        'كسر $x$ نحلّه بتعويض $w$ = اللي تحت الجذر. وكسر الرقم نحلّه بقانون من جدول 4.2.')))
    U.add('sign', 'العلامة', p(rich('إذا شفت البسط فيه $x$ ورقم مع بعض، مثل $x-2$، والمقام من أشكال جدول 4.2.'))
          + contrast([(r'\int\frac{x-2}{\sqrt{25+x^{2}}}dx', 'هذا النوع: نفصل', 'البسط فيه $x$ ورقم'),
                      (r'\int\frac{x+3}{\sqrt{x^{2}+6x+10}}dx', 'تعويض واحد', 'البسط نص مشتقة اللي تحت الجذر، فما نفصل'),
                      (r'\int\frac{3\,dx}{\sqrt{25+x^{2}}}', 'النوع 3', 'البسط رقم بس، فقانون على طول')]))
    U.prev('في النوع 7 كان البسط رقم، وكفانا تعويض واحد. هنا البسط فيه $x$ ورقم، فنفصل الكسر ونحل كل جزء لحاله.')
    formula('1/sqrt(u)', '2*sqrt(u)', branches=('t',), label='U-I6 law power')
    formula('1/sqrt(u**2+a**2)', 'asinh(u/a)', pos=('a',), label='U-I6 law sinh')
    laws = (md(r'\int w^{-1/2}\,dw=\frac{w^{1/2}}{1/2}=2\sqrt{w}+C') + md(r'\int\frac{du}{\sqrt{u^{2}+a^{2}}}=\sinh^{-1}\frac{u}{a}+C'))
    U.add('short', '🧭 الطريقة', method([
        'نشوف البسط أول: إذا هو مشتقة اللي تحت الجذر (أو نصها)، فهو تعويض واحد وما نفصل.',
        'غير كذا نفصل الكسر: كل حد في البسط على نفس المقام، ومعه إشارته.',
        'كسر $x$: نسمّي $w$ = اللي تحت الجذر. مشتقته فيها $x$، فينحل بقاعدة القوة.',
        'كسر الرقم: نطلّع الرقم برّا، ونستعمل قانون $\\sinh^{-1}$ أو $\\cosh^{-1}$ أو $\\tanh^{-1}$.',
        'نجمع الجوابين بنفس الإشارة اللي في الفصل.'],
        tricks_=[('بسط فيه جمع؟ نفصل لكسرين، وكل واحد نوع لحاله: $\\frac{x-2}{\\sqrt{25+x^2}}=\\frac{x}{\\sqrt{25+x^2}}-\\frac{2}{\\sqrt{25+x^2}}$.',
                  [('(x-2)/sqrt(25+x**2)', 'x/sqrt(25+x**2)-2/sqrt(25+x**2)')])], label='U-I6') + laws)
    it = ITEMS['N42-X2-07']
    ex = question(it, 'U-I6 example')
    ex += steps(it, [
        ('tex', r'\frac{x-2}{\sqrt{25+x^{2}}}=\frac{x}{\sqrt{25+x^{2}}}-\frac{2}{\sqrt{25+x^{2}}}',
         [('(x-2)/sqrt(25+x**2)', 'x/sqrt(25+x**2)-2/sqrt(25+x**2)')],
         'مشتقة $25+x^2$ هي $2x$، والبسط فيه $-2$ زيادة. هنا التريك: نفصل الكسر، وكل حد ومعه إشارته.'),
        ('sub', '25+x**2', '2*x', 'الكسر الأول: نسمّي $w$ = اللي تحت الجذر. مشتقته $2x$، و $x$ موجودة فوق.', 'w'),
        ('tex', r'x\,dx=\frac{dw}{2}', [('diff(25+x**2,x)/2', 'x')], 'فوق عندنا $x\\,dx$ بدون 2. فنقسم على 2.'),
        ('tex', r'\int\frac{x\,dx}{\sqrt{25+x^{2}}}=\frac12\int w^{-1/2}\,dw',
         [('x/sqrt(25+x**2)', 'Rational(1,2)*diff(25+x**2,x)*(25+x**2)**Rational(-1,2)')],
         'نعوّض، ونكتب الجذر تحت كأس سالب: $\\frac{1}{\\sqrt w}=w^{-1/2}$.'),
        ('tex', r'=\frac12\cdot2\sqrt{w}=\sqrt{25+x^{2}}', [('diff(sqrt(25+x**2),x)', 'x/sqrt(25+x**2)')],
         'قاعدة القوة: $\\int w^{-1/2}dw=2\\sqrt w$. ثم نرجع $w=25+x^2$.'),
        ('tex', r'\int\frac{2\,dx}{\sqrt{x^{2}+5^{2}}}=2\sinh^{-1}\frac{x}{5}', [('diff(2*asinh(x/5),x)', '2/sqrt(x**2+25)')],
         'الكسر الثاني: الرقم 2 برّا. والقانون $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$ مع $u=x$ و $a=5$.'),
        ('line', 'sqrt(25+x**2)-2*asinh(x/5)', 'نطرح الجزأين، بنفس الإشارة اللي في الفصل.')], 'U-I6 ex')
    ex += final(it, 'U-I6 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('انتبه للإشارة: $\\frac{x-2}{\\ldots}=\\frac{x}{\\ldots}-\\frac{2}{\\ldots}$. السالب يروح مع الرقم.'),
                                rich('كسر $x$ مو قانون $\\sinh^{-1}$. جوابه جذر، أو $\\ln$ إذا ما فيه جذر.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\int\frac{x-2}{\sqrt{25+x^{2}}}dx=\int\frac{x\,dx}{\sqrt{25+x^{2}}}-\int\frac{2\,dx}{\sqrt{25+x^{2}}}',
                   [('(x-2)/sqrt(25+x**2)', 'x/sqrt(25+x**2)-2/sqrt(25+x**2)')], 'U-I6 paper 1'))
          + md(arith(r'w=25+x^{2}\qquad dw=2x\,dx', [('diff(25+x**2,x)', '2*x')], 'U-I6 paper 2'))
          + md(arith(r'=\sqrt{25+x^{2}}-2\sinh^{-1}\frac{x}{5}+C', [('diff(sqrt(25+x**2)-2*asinh(x/5),x)', '(x-2)/sqrt(25+x**2)')], 'U-I6 paper 3')))
    U.add('ok', '✔ تأكد', p(rich("اشتق الحد الأول: $\\left(\\sqrt{25+x^2}\\right)'=\\frac{2x}{2\\sqrt{25+x^2}}=\\frac{x}{\\sqrt{25+x^2}}$. "
                                 'لازم يرجع الكسر الأول ✓.')))
    U.gist('البسط فيه $x$ ورقم', 'نشوف هل البسط مشتقة اللي تحت الجذر. إذا لا، نفصل الكسر',
           'كسر $x$ بتعويض $w$، وكسر الرقم بقانون من جدول 4.2')
    U.drill('1', 'G-87', 'G', 'مثل المثال، لكن الرقم موجب، و $a=2$.',
            first=r'\frac{x+2}{\sqrt{x^{2}+4}}=\frac{x}{\sqrt{x^{2}+4}}+\frac{2}{\sqrt{x^{2}+4}}',
            claims=[('(x+2)/sqrt(x**2+4)', 'x/sqrt(x**2+4)+2/sqrt(x**2+4)')],
            sol_rows=[('sub', 'x**2+4', '2*x', 'كسر $x$: نسمّي $w$ = اللي تحت الجذر، فـ $x\\,dx=\\frac{dw}{2}$.', 'w'),
                      ('tex', r'\int\frac{x\,dx}{\sqrt{x^{2}+4}}=\frac12\int w^{-1/2}\,dw=\sqrt{x^{2}+4}',
                       [('x/sqrt(x**2+4)', 'Rational(1,2)*diff(x**2+4,x)*(x**2+4)**Rational(-1,2)'), ('diff(sqrt(x**2+4),x)', 'x/sqrt(x**2+4)')],
                       'قاعدة القوة: $\\int w^{-1/2}dw=2\\sqrt w$، و $\\frac12\\cdot2=1$. ثم نرجع $w$.'),
                      ('tex', r'\int\frac{2\,dx}{\sqrt{x^{2}+2^{2}}}=2\sinh^{-1}\frac{x}{2}', [('diff(2*asinh(x/2),x)', '2/sqrt(x**2+4)')],
                       'كسر الرقم: القانون $\\sinh^{-1}\\frac ua$ مع $u=x$ و $a=2$، والـ 2 برّا.'),
                      ('line', 'sqrt(x**2+4)+2*asinh(x/2)', 'نجمع الجزأين.')])
    U.drill('2', 'G-01', 'P', 'افصل الكسر. كسر $2x$ هو مشتقة اللي تحت الجذر كاملة.',
            sol_rows=[('tex', r'\frac{2x+3}{\sqrt{x^{2}+9}}=\frac{2x}{\sqrt{x^{2}+9}}+\frac{3}{\sqrt{x^{2}+9}}',
                       [('(2*x+3)/sqrt(x**2+9)', '2*x/sqrt(x**2+9)+3/sqrt(x**2+9)')], 'مشتقة $x^2+9$ هي $2x$، والبسط فيه 3 زيادة. فنفصل الكسر.'),
                      ('sub', 'x**2+9', '2*x', 'الكسر الأول: نسمّي $w=x^2+9$. ومشتقته $2x$ فوق كاملة.', 'w'),
                      ('tex', r'\int w^{-1/2}\,dw=2\sqrt{w}=2\sqrt{x^{2}+9}', [('diff(2*sqrt(x**2+9),x)', '2*x/sqrt(x**2+9)')],
                       'قاعدة القوة: $\\frac{w^{1/2}}{1/2}=2\\sqrt w$. ثم نرجع $w$.'),
                      ('tex', r'\int\frac{3\,dx}{\sqrt{x^{2}+3^{2}}}=3\sinh^{-1}\frac{x}{3}', [('diff(3*asinh(x/3),x)', '3/sqrt(x**2+9)')],
                       'الكسر الثاني: القانون $\\sinh^{-1}\\frac ua$ مع $a=3$، والـ 3 برّا.'),
                      ('line', '2*sqrt(x**2+9)+3*asinh(x/3)', 'نجمع الجزأين.')])
    U.drill('3', 'N42-X2-08', 'I', 'افصل. كسر $x$ يعطي $\\ln$، وكسر الرقم قانون $\\tanh^{-1}$ مع $a=4$.',
            sol_rows=[('tex', r'\frac{x+1}{16-x^{2}}=\frac{x}{16-x^{2}}+\frac{1}{16-x^{2}}', [('(x+1)/(16-x**2)', 'x/(16-x**2)+1/(16-x**2)')],
                       'البسط فيه $x$ ورقم، والمقام بلا جذر. فنفصل الكسر.'),
                      ('sub', '16-x**2', '-2*x', 'الكسر الأول: نسمّي $w=16-x^2$. مشتقته $-2x$، يعني $x\\,dx=-\\frac{dw}{2}$.', 'w'),
                      ('tex', r'\int\frac{x\,dx}{16-x^{2}}=-\frac12\int\frac{dw}{w}=-\frac12\ln\left|16-x^{2}\right|',
                       [('diff(-log(Abs(16-x**2))/2,x)', 'x/(16-x**2)', '4*t/(1+t)'), ('diff(-log(Abs(16-x**2))/2,x)', 'x/(16-x**2)', '-4*t/(1+t)')],
                       'القانون $\\int\\frac{dw}{w}=\\ln|w|$. ثم نرجع $w$.'),
                      ('tex', r'\int\frac{dx}{4^{2}-x^{2}}=\frac14\tanh^{-1}\frac{x}{4}', [('diff(atanh(x/4)/4,x)', '1/(16-x**2)')],
                       'الكسر الثاني: القانون $\\int\\frac{du}{a^2-u^2}=\\frac1a\\tanh^{-1}\\frac ua$ مع $a=4$، لأن $|x|<4$.'),
                      ('line', '-log(Abs(16-x**2))/2+atanh(x/4)/4', 'نجمع الجزأين.')])
    U.drill('4', 'M-13', 'I', 'قبل ما تفصل، شوف البسط: هل هو نص مشتقة اللي تحت الجذر؟',
            sol_rows=[('tex', r'\left(x^{2}+8x+25\right)^{\prime}=2x+8=2\left(x+4\right)', [('diff(x**2+8*x+25,x)', '2*(x+4)')],
                       'قبل ما نفصل، نشتق اللي تحت الجذر. طلع $2(x+4)$، يعني البسط نص المشتقة.'),
                      ('tex', r'w=x^{2}+8x+25\qquad dw=\left(2x+8\right)dx', [('diff(x**2+8*x+25,x)', '2*x+8')],
                       'فما نحتاج نفصل. نسمّي $w$ = اللي تحت الجذر كله.'),
                      ('tex', r'(x+4)\,dx=\frac{dw}{2}', [('diff(x**2+8*x+25,x)/2', 'x+4')], 'نقسم على 2 عشان يطلع البسط نفسه.'),
                      ('tex', r'\int\frac{(x+4)\,dx}{\sqrt{x^{2}+8x+25}}=\frac12\int w^{-1/2}\,dw',
                       [('(x+4)/sqrt(x**2+8*x+25)', 'Rational(1,2)*diff(x**2+8*x+25,x)*(x**2+8*x+25)**Rational(-1,2)')],
                       'نعوّض، و $\\frac{1}{\\sqrt w}=w^{-1/2}$.'),
                      ('line', 'sqrt(x**2+8*x+25)', 'قاعدة القوة: $\\frac12\\cdot2\\sqrt w=\\sqrt w$. ثم نرجع $w$.')])
    return U


# ---------------------------------------------------------------- 9
def u_invnum():
    U = Unit('U-I7', 'دالة عكسية ومشتقتها في السؤال', '4.2', 'ص62، تمرين 9', 3)
    U.add('idea', 'الفكرة', p(rich(
        'في السؤال دالة عكسية مثل $\\cosh^{-1}x$، ومعها مشتقتها مضروبة فيها. نسمّي $u$ = الدالة العكسية. '
        'فتصير مشتقتها مع $dx$ هي $du$، ويبقى تكامل سهل: $\\int u\\,du$.')))
    U.add('sign', 'العلامة', p(rich('إذا شفت دالة عكسية ومعها مشتقتها، مضروبتين في بعض.'))
          + contrast([(r'\int\frac{\cosh^{-1}x}{\sqrt{x^{2}-1}}dx', 'تعويض $u=\\cosh^{-1}x$', 'مشتقة $\\cosh^{-1}x$ هي $\\frac{1}{\\sqrt{x^2-1}}$، وموجودة في السؤال'),
                      (r'\int\sinh^{-1}(2x)\,dx', 'تجزئة (درس 5.1)', 'الدالة لحالها، بلا مشتقتها')]))
    U.prev('في النوع 8 كان $w$ = اللي تحت الجذر. هنا $u$ = الدالة العكسية نفسها، لأن مشتقتها موجودة في السؤال.')
    laws = (md(arith(r'\frac{d}{dx}\sinh^{-1}x=\frac{1}{\sqrt{x^{2}+1}}\qquad \frac{d}{dx}\cosh^{-1}x=\frac{1}{\sqrt{x^{2}-1}}\qquad \frac{d}{dx}\tanh^{-1}x=\frac{1}{1-x^{2}}',
                     [('diff(asinh(x),x)', '1/sqrt(x**2+1)'), ('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t'), ('diff(atanh(x),x)', '1/(1-x**2)')], 'U-I7 law derivatives'))
            + md(arith(r'\int u\,du=\frac{u^{2}}{2}+C', [('integrate(x,x)', 'x**2/2')], 'U-I7 law power')))
    U.add('short', '🧭 الطريقة', method([
        'نلقى الدالة العكسية في السؤال، مثل $\\cosh^{-1}x$.',
        'نتأكد إن مشتقتها موجودة، من جدول مشتقات الدوال العكسية.',
        'نسمّي $u$ = الدالة العكسية. فمشتقتها مع $dx$ تصير $du$.',
        'نكامل بقاعدة القوة: $\\int u\\,du=\\frac{u^2}{2}$. ثم نرجع $u$.'],
        tricks_=[('الدالة العكسية ومشتقتها مضروبتين؟ $u$ = الدالة، والجواب $\\frac{u^2}{2}$. مع $\\cosh^{-1}x$ يطلع $\\frac{(\\cosh^{-1}x)^2}{2}$.',
                  [('diff(acosh(x)**2/2,x)', 'acosh(x)/sqrt(x**2-1)', '1+t')])], label='U-I7') + laws)
    it = ITEMS['N42-X2-09']
    ex = question(it, 'U-I7 example')
    ex += steps(it, [
        ('tex', r'\frac{\cosh^{-1}x}{\sqrt{x^{2}-1}}=\cosh^{-1}x\cdot\frac{1}{\sqrt{x^{2}-1}}', [('acosh(x)/sqrt(x**2-1)', 'acosh(x)*1/sqrt(x**2-1)')],
         'نكتب الكسر كضرب، عشان نشوف الدالة العكسية ومعها كسر ثاني.'),
        ('tex', r'\frac{d}{dx}\cosh^{-1}x=\frac{1}{\sqrt{x^{2}-1}}', [('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t')],
         'الكسر الثاني هو نفسه مشتقة $\\cosh^{-1}x$، من جدول مشتقات الدوال العكسية.'),
        ('sub', 'acosh(x)', '1/sqrt(x**2-1)', 'هنا التريك: نسمّي $u$ = الدالة العكسية. ومشتقتها مع $dx$ صارت $du$.', 'u', '1+t'),
        ('tex', r'\int\cosh^{-1}x\cdot\frac{dx}{\sqrt{x^{2}-1}}=\int u\,du', [('acosh(x)/sqrt(x**2-1)', 'acosh(x)*diff(acosh(x),x)', '1+t')],
         'نعوّض. بقي تكامل سهل.'),
        ('tex', r'=\frac{u^{2}}{2}', [('integrate(x,x)', 'x**2/2')], 'قاعدة القوة: نزيد الأس واحد، ونقسم على الأس الجديد.'),
        ('line', 'acosh(x)**2/2', 'نرجع $u=\\cosh^{-1}x$.')], 'U-I7 ex')
    ex += final(it, 'U-I7 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('$(\\cosh^{-1}x)^2$ يعني مربع الدالة كلها، مو $\\cosh^{-1}(x^2)$.'),
                                rich('إذا الدالة العكسية في المقام، مثل $\\frac{1}{\\sqrt{x^2-1}\\,\\cosh^{-1}x}$، يصير $\\int\\frac{du}{u}=\\ln|u|$، مو $\\frac{u^2}{2}$.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'u=\cosh^{-1}x\qquad du=\frac{dx}{\sqrt{x^{2}-1}}', [('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t')], 'U-I7 paper 1'))
          + md(arith(r'\int u\,du=\frac{u^{2}}{2}=\frac{\left(\cosh^{-1}x\right)^{2}}{2}+C',
                     [('diff(acosh(x)**2/2,x)', 'acosh(x)/sqrt(x**2-1)', '1+t')], 'U-I7 paper 2')))
    U.add('ok', '✔ تأكد', p(rich("اشتق جوابك: $\\left(\\frac{u^2}{2}\\right)'=u\\cdot u'$، يعني $\\cosh^{-1}x\\cdot\\frac{1}{\\sqrt{x^2-1}}$. "
                                 'لازم يرجع السؤال ✓.')))
    U.gist('دالة عكسية ومعها مشتقتها', 'نسمّي $u$ = الدالة العكسية', '$\\int u\\,du=\\frac{u^2}{2}$، ثم نرجع $u$')
    U.drill('1', 'G-88', 'G', 'مشتقة $\\sinh^{-1}x$ هي $\\frac{1}{\\sqrt{1+x^2}}$، وموجودة في السؤال.',
            first=r'u=\sinh^{-1}x,\qquad du=\frac{dx}{\sqrt{1+x^{2}}}', claims=[('diff(asinh(x),x)', '1/sqrt(1+x**2)')],
            sol_rows=[('tex', r'\int\frac{\sinh^{-1}x}{\sqrt{1+x^{2}}}dx=\int u\,du', [('asinh(x)/sqrt(1+x**2)', 'asinh(x)*diff(asinh(x),x)')],
                       'نعوّض: الدالة العكسية صارت $u$، والكسر مع $dx$ صار $du$.'),
                      ('tex', r'=\frac{u^{2}}{2}', [('integrate(x,x)', 'x**2/2')], 'قاعدة القوة: نزيد الأس واحد، ونقسم على 2.'),
                      ('line', 'asinh(x)**2/2', 'نرجع $u=\\sinh^{-1}x$.')])
    U.drill('2', 'G-02', 'P', 'نفس التمرين 1، لكن $\\int u^2du=\\frac{u^3}{3}$.',
            sol_rows=[('sub', 'asinh(x)', '1/sqrt(1+x**2)', 'مشتقة $\\sinh^{-1}x$ موجودة في السؤال. فنسمّي $u$ = الدالة العكسية.'),
                      ('tex', r'\int\frac{\left(\sinh^{-1}x\right)^{2}}{\sqrt{1+x^{2}}}dx=\int u^{2}\,du',
                       [('asinh(x)**2/sqrt(1+x**2)', 'asinh(x)**2*diff(asinh(x),x)')], 'نعوّض: $(\\sinh^{-1}x)^2$ صارت $u^2$.'),
                      ('tex', r'=\frac{u^{3}}{3}', [('integrate(x**2,x)', 'x**3/3')], 'قاعدة القوة: نزيد الأس واحد، ونقسم على 3.'),
                      ('line', 'asinh(x)**3/3', 'نرجع $u=\\sinh^{-1}x$.')])
    U.drill('3', 'G-03', 'I', 'مشتقة $\\tanh^{-1}x$ هي $\\frac{1}{1-x^2}$.',
            sol_rows=[('tex', r'\frac{d}{dx}\tanh^{-1}x=\frac{1}{1-x^{2}}', [('diff(atanh(x),x)', '1/(1-x**2)')],
                       'المقام $1-x^2$ هو مقام مشتقة $\\tanh^{-1}x$. فمشتقتها موجودة في السؤال.'),
                      ('sub', 'atanh(x)', '1/(1-x**2)', 'نسمّي $u$ = الدالة العكسية.', 'u', 't/(1+t)'),
                      ('tex', r'\int\frac{\tanh^{-1}x}{1-x^{2}}dx=\int u\,du', [('atanh(x)/(1-x**2)', 'atanh(x)*diff(atanh(x),x)')], 'نعوّض.'),
                      ('tex', r'=\frac{u^{2}}{2}', [('integrate(x,x)', 'x**2/2')], 'قاعدة القوة.'),
                      ('line', 'atanh(x)**2/2', 'نرجع $u=\\tanh^{-1}x$.')])
    U.drill('4', 'M-14', 'I', 'افصل الكسر أول مثل النوع 8. والجزء الثاني فيه $\\tan^{-1}x$ ومشتقتها.',
            sol_rows=[('tex', r'\frac{x+\tan^{-1}x}{1+x^{2}}=\frac{x}{1+x^{2}}+\frac{\tan^{-1}x}{1+x^{2}}',
                       [('(x+atan(x))/(1+x**2)', 'x/(1+x**2)+atan(x)/(1+x**2)')], 'البسط فيه حدّين، فنفصل الكسر مثل النوع 8.'),
                      ('sub', '1+x**2', '2*x', 'الكسر الأول: نسمّي $w$ = المقام. مشتقته $2x$، يعني $x\\,dx=\\frac{dw}{2}$.', 'w'),
                      ('tex', r'\int\frac{x\,dx}{1+x^{2}}=\frac12\int\frac{dw}{w}=\frac12\ln\left(1+x^{2}\right)', [('diff(log(1+x**2)/2,x)', 'x/(1+x**2)')],
                       'القانون $\\int\\frac{dw}{w}=\\ln|w|$. و $1+x^2$ موجب، فما نحتاج القيمة المطلقة.'),
                      ('tex', r'\frac{d}{dx}\tan^{-1}x=\frac{1}{1+x^{2}}', [('diff(atan(x),x)', '1/(1+x**2)')],
                       'الكسر الثاني: مشتقة $\\tan^{-1}x$ (درس 3.4) هي $\\frac{1}{1+x^2}$، وموجودة.'),
                      ('sub', 'atan(x)', '1/(1+x**2)', 'نسمّي $u=\\tan^{-1}x$. فالكسر مع $dx$ صار $du$.'),
                      ('tex', r'\int\frac{\tan^{-1}x\,dx}{1+x^{2}}=\int u\,du', [('atan(x)/(1+x**2)', 'atan(x)*diff(atan(x),x)')], 'نعوّض.'),
                      ('tex', r'=\frac{u^{2}}{2}=\frac{\left(\tan^{-1}x\right)^{2}}{2}', [('diff(atan(x)**2/2,x)', 'atan(x)/(1+x**2)')],
                       'قاعدة القوة، ثم نرجع $u=\\tan^{-1}x$.'),
                      ('line', 'log(x**2+1)/2+atan(x)**2/2', 'نجمع الجزأين.')])
    return U


# ---------------------------------------------------------------- 10
def u_square():
    U = Unit('U-I8', 'إكمال المربع', '4.2', 'ص61، تمارين 13 و14', 2)
    U.add('idea', 'الفكرة', p(rich(
        'تحت الجذر ثلاثة حدود فيها حد $x$، مثل $x^2+6x-16$. هذا مو مربع جاهز، فما نقدر نستعمل القانون مباشرة. '
        'نكمّل المربع فيصير: (قوس)² زائد أو ناقص رقم. بعدها نسمّي القوس $u$ ونستعمل قانون من جدول تكاملات 4.2.')))
    U.add('sign', 'العلامة', p(rich('تحت الجذر $x^2$ و $x$ ورقم، وما فيه شي مضروب برّا الجذر.'))
          + contrast([(r'\int\frac{dx}{\sqrt{x^{2}+6x+13}}', 'هذا النوع', 'تحت الجذر فيه حد $x$'),
                      (r'\int\frac{dx}{(x+3)\sqrt{x^{2}+6x+13}}', 'النوع 11', 'فيه قوس مضروب برّا الجذر'),
                      (r'\int\frac{dx}{\sqrt{x^{2}+9}}', 'النوع 3', 'مربع جاهز، ما يحتاج إكمال')]))
    U.prev('في الأنواع 3 إلى 9 كان تحت الجذر مربع جاهز مثل $x^2+9$. هنا فيه حد $x$ زيادة، فلازم نكمّل المربع أول.')
    laws = (md(r'\int\frac{du}{\sqrt{u^{2}+a^{2}}}=\sinh^{-1}\frac{u}{a}+C') + md(r'\int\frac{du}{\sqrt{u^{2}-a^{2}}}=\cosh^{-1}\frac{u}{a}+C'))
    U.add('short', '🧭 الطريقة', method([
        'نكمّل المربع: نص معامل $x$، ومربعه نضيفه ونطرحه.',
        'يصير تحت الجذر: (قوس)² زائد رقم، أو (قوس)² ناقص رقم.',
        'نسمّي القوس $u$. ومشتقته 1، يعني $du=dx$.',
        'زائد يعني قانون $\\sinh^{-1}$. وناقص يعني قانون $\\cosh^{-1}$. ثم نرجع $u$.'],
        tricks_=[('<b>نص معامل $x$:</b> في $x^2+6x$ نص 6 هو 3، ومربعه 9. فـ $x^2+6x+9=(x+3)^2$. والقوس فيه نفس إشارة معامل $x$: '
                  '$x^2-4x+4=(x-2)^2$.', [('x**2+6*x+9', '(x+3)**2'), ('x**2-4*x+4', '(x-2)**2')])], label='U-I8') + laws)
    it = ITEMS['1446-S1-SE-Q2.2']
    ex1_it = it
    ex = question(it, 'U-I8 example 1')
    ex += steps(it, [
        ('tex', r'x^{2}+6x-16=\left(x^{2}+6x+9\right)-9-16', [('x**2+6*x-16', 'x**2+6*x+9-9-16')],
         'تحت الجذر مو مربع جاهز، فنكمّل المربع. نص 6 هو 3، ومربعه 9. نضيف 9 ونطرحها، فما تتغير القيمة.'),
        ('tex', r'=(x+3)^{2}-25', [('x**2+6*x+9-9-16', '(x+3)**2-25')],
         'أول ثلاثة حدود مربع كامل: $(x+3)^2=x^2+6x+9$. والأرقام: $-9-16=-25$.'),
        ('tex', r'=(x+3)^{2}-5^{2}', [('(x+3)**2-25', '(x+3)**2-5**2')], 'نكتب 25 كمربع عشان نعرف $a$: هنا $a=5$.'),
        ('sub', 'x+3', '1', 'نسمّي القوس $u$. مشتقة $x+3$ هي 1، فـ $du=dx$.'),
        ('tex', r'\int\frac{3\,dx}{\sqrt{x^{2}+6x-16}}=3\int\frac{du}{\sqrt{u^{2}-5^{2}}}', [('3/sqrt((x+3)**2-5**2)', '3/sqrt(x**2+6*x-16)')],
         'نعوّض. صار بنفس شكل القانون، والرقم 3 يطلع برّا التكامل.'),
        ('tex', r'=3\cosh^{-1}\frac{u}{5}', [('diff(3*acosh(x/5),x)', '3/sqrt(x**2-25)', '5+t')],
         'مربع ناقص رقم، يعني القانون: $\\int\\frac{du}{\\sqrt{u^2-a^2}}=\\cosh^{-1}\\frac ua$، و $a=5$.'),
        ('line', '3*acosh((x+3)/5)', 'نرجع $u=x+3$.')], 'U-I8 ex1')
    ex += final(it, 'U-I8 example 1')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    it = ITEMS['1445-S2-SE-Q2.7']
    ex = question(it, 'U-I8 example 2')
    ex += steps(it, [
        ('tex', r'x^{2}+6x+13=\left(x^{2}+6x+9\right)-9+13', [('x**2+6*x+13', 'x**2+6*x+9-9+13')],
         'نكمّل المربع. نص 6 هو 3، ومربعه 9. نضيف 9 ونطرحها.'),
        ('tex', r'=(x+3)^{2}+4=(x+3)^{2}+2^{2}', [('x**2+6*x+9-9+13', '(x+3)**2+2**2')],
         'أول ثلاثة حدود $(x+3)^2$. والأرقام: $-9+13=4$، و $4=2^2$.'),
        ('sub', 'x+3', '1', 'نسمّي القوس $u$، و $du=dx$.'),
        ('tex', r'\int\frac{dx}{\sqrt{x^{2}+6x+13}}=\int\frac{du}{\sqrt{u^{2}+2^{2}}}', [('1/sqrt((x+3)**2+2**2)', '1/sqrt(x**2+6*x+13)')],
         'نعوّض. صار بنفس شكل القانون.'),
        ('line', 'asinh((x+3)/2)', 'مربع زائد رقم، يعني القانون: $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$، و $a=2$. ثم نرجع $u=x+3$.')],
        'U-I8 ex2')
    ex += final(it, 'U-I8 example 2')
    U.add('ex', '🧱 مثال 2: الرقم موجب، يعني sinh⁻¹ (اختبار سابق)', ex)
    U.add('short', '⚡ الطريقة السريعة: المركز والباقي', shortcut(
        ex1_it, 'U-I8 ex1',
        saves='بدل ما تضيف وتطرح وتفك أقواس، تعوّض رقم واحد. والجبر هو أكثر شي يغلّط في هذا النوع.',
        origin='القوس ($x$ ناقص المركز) يصير صفر لما نعوّض المركز مكان $x$. فإذا عوّضنا المركز في اللي تحت الجذر، '
               'يختفي المربع ويبقى الرقم الباقي لحاله. وهذا نفس الرقم اللي طلع في 🧱 بعد ما أضفنا وطرحنا ($-25$).',
        steps_=['نحسب <b>المركز</b> = سالب معامل $x$ ÷ (2 × معامل $x^2$).',
                'نحسب <b>الباقي</b>: نعوّض المركز مكان $x$ في اللي تحت الجذر.',
                'نكتب: اللي تحت الجذر = (معامل $x^2$) × ($x$ ناقص المركز)² + الباقي.',
                'الباقي موجب يعني قانون $\\sinh^{-1}$. والباقي سالب يعني قانون $\\cosh^{-1}$.'],
        on='على مثال 1 في 🧱:',
        rows=[('المركز: معامل $x$ هو 6، ومعامل $x^2$ هو 1.', r'-\frac{6}{2\times1}=-3', [('-Rational(6,2*1)', '-3')]),
              ('الباقي: نعوّض $-3$ مكان $x$. انتبه: $(-3)^2=9$ موجب.', r'(-3)^{2}+6(-3)-16=9-18-16=-25', [('(-3)**2+6*(-3)-16', '-25')]),
              ('نكتب ($x$ ناقص المركز)² + الباقي. و $x-(-3)=x+3$. نفس سطر 🧱.', r'x^{2}+6x-16=(x+3)^{2}-25=(x+3)^{2}-5^{2}',
               [('x**2+6*x-16', '(x+3)**2-5**2')]),
              ('الباقي سالب، يعني قانون $\\cosh^{-1}$ مع $a=5$، والرقم 3 برّا. نفس جواب 🧱 ✓', r'3\cosh^{-1}\frac{x+3}{5}+C',
               [('=ANS', '3*acosh((x+3)/5)')])],
        memo='المركز يصفّر القوس، والباقي هو اللي يبقى.',
        never=['المركز سالب يعني القوس فيه زائد: $x-(-3)=x+3$. لا تكتب $x-3$.',
               'إذا ما فيه حد $x$ تحت الجذر (مثل $x^2+9$) ما تحتاجه. هذا النوع 3.'],
        paper='تكتب السطر اللي طلع: $x^2+6x-16=(x+3)^2-5^2$. هو نفس سطر إكمال المربع، فالمصحح يشوف نفس الشي.',
        ask='اكتب كل واحد على شكل (قوس)² + الباقي',
        tries=[('x^{2}+4x+13', r'(x+2)^{2}+9', [('x**2+4*x+13', '(x+2)**2+9')]),
               ('x^{2}-10x+16', r'(x-5)^{2}-9', [('x**2-10*x+16', '(x-5)**2-9')]),
               ('x^{2}+8x+7', r'(x+4)^{2}-9', [('x**2+8*x+7', '(x+4)**2-9')])]))
    U.add('trap', '⚠️ الفخ', ul([rich('انتبه للإشارة: $x^2-4x$ نصه $-2$، فيصير $(x-2)^2$ مو $(x+2)^2$.'),
                                rich('لو معامل $x^2$ مو 1، طلّعه من الجذر أول (التمرين 3).')]))
    U.add('paper', '✍️ في ورقة الكويز', md(r'x^{2}+6x-16=(x+3)^{2}-5^{2}') + md(r'u=x+3\qquad du=dx')
          + md(r'\int\frac{3\,dx}{\sqrt{x^{2}+6x-16}}=3\int\frac{du}{\sqrt{u^{2}-5^{2}}}=3\cosh^{-1}\frac{x+3}{5}+C'))
    U.add('ok', '✔ تأكد', p(rich('افتح القوس اللي كتبته: $(x+3)^2-25=x^2+6x+9-25=x^2+6x-16$. لازم يرجع اللي تحت الجذر.')))
    U.gist('تحت الجذر $x^2$ و $x$ ورقم، وما فيه شي برّا الجذر', 'كمّل المربع، وسمّ القوس $u$',
           '(قوس)² + رقم يعني $\\sinh^{-1}$، و(قوس)² − رقم يعني $\\cosh^{-1}$')
    U.drill('1', '1447-S1-FE-Q2.1', 'G', 'نص $-4$ هو $-2$، ومربعه 4.',
            first=r'x^{2}-4x=\left(x^{2}-4x+4\right)-4=(x-2)^{2}-2^{2}',
            claims=[('x**2-4*x', 'x**2-4*x+4-4'), ('x**2-4*x', '(x-2)**2-2**2')],
            sol_rows=[('tex', r'-\frac{-4}{2\times1}=2,\qquad 2^{2}-4\times2=-4', [('-Rational(-4,2)', '2'), ('2**2-4*2', '-4')],
                       '✔ تأكد بالسريع: المركز 2، والباقي $-4=-2^2$. نفس السطر الجاهز.'),
                      ('sub', 'x-2', '1', 'نسمّي القوس $u$، و $du=dx$.'),
                      ('tex', r'\int\frac{dx}{\sqrt{x^{2}-4x}}=\int\frac{du}{\sqrt{u^{2}-2^{2}}}', [('1/sqrt((x-2)**2-2**2)', '1/sqrt(x**2-4*x)')],
                       'نعوّض. صار مربع ناقص رقم.'),
                      ('line', 'acosh((x-2)/2)', 'القانون: $\\int\\frac{du}{\\sqrt{u^2-a^2}}=\\cosh^{-1}\\frac ua$، و $a=2$. ثم نرجع $u=x-2$.')])
    U.drill('2', 'N42-X2-14', 'P', 'نص 2 هو 1، ومربعه 1.',
            sol_rows=[('tex', r'x^{2}+2x+10=\left(x^{2}+2x+1\right)-1+10', [('x**2+2*x+10', 'x**2+2*x+1-1+10')],
                       'نكمّل المربع. نص 2 هو 1، ومربعه 1. نضيفه ونطرحه.'),
                      ('tex', r'=(x+1)^{2}+3^{2}', [('x**2+2*x+1-1+10', '(x+1)**2+3**2')], 'أول ثلاثة حدود $(x+1)^2$. والأرقام: $-1+10=9=3^2$.'),
                      ('tex', r'-\frac{2}{2\times1}=-1,\qquad (-1)^{2}+2(-1)+10=9', [('-Rational(2,2)', '-1'), ('(-1)**2+2*(-1)+10', '9')],
                       '✔ تأكد بالسريع: المركز $-1$، والباقي 9. نفس اللي طلع.'),
                      ('sub', 'x+1', '1', 'نسمّي القوس $u$، و $du=dx$.'),
                      ('tex', r'\int\frac{5\,dx}{\sqrt{x^{2}+2x+10}}=5\int\frac{du}{\sqrt{u^{2}+3^{2}}}', [('5/sqrt((x+1)**2+3**2)', '5/sqrt(x**2+2*x+10)')],
                       'نعوّض، والرقم 5 يطلع برّا التكامل.'),
                      ('line', '5*asinh((x+1)/3)', 'مربع زائد رقم: القانون $\\sinh^{-1}\\frac ua$ مع $a=3$. ثم نرجع $u=x+1$.')])
    U.drill('3', 'G-04', 'I', 'طلّع 9 من الجذر أول.',
            sol_rows=[('tex', r'9x^{2}+36x+45=9\left(x^{2}+4x+5\right)', [('9*x**2+36*x+45', '9*(x**2+4*x+5)')],
                       'معامل $x^2$ مو 1. نطلّع 9 عامل مشترك من كل الحدود.'),
                      ('tex', r'\sqrt{9\left(x^{2}+4x+5\right)}=3\sqrt{x^{2}+4x+5}', [('sqrt(9*(x**2+4*x+5))', '3*sqrt(x**2+4*x+5)')],
                       'جذر 9 هو 3، ويطلع برّا الجذر.'),
                      ('tex', r'x^{2}+4x+5=\left(x^{2}+4x+4\right)+1=(x+2)^{2}+1^{2}', [('x**2+4*x+5', '(x+2)**2+1**2')],
                       'نكمّل المربع: نص 4 هو 2، ومربعه 4. والباقي $5-4=1$.'),
                      ('tex', r'-\frac{36}{2\times9}=-2,\qquad 9(-2)^{2}+36(-2)+45=9', [('-Rational(36,18)', '-2'), ('9*(-2)**2+36*(-2)+45', '9'),
                                                                                       ('9*x**2+36*x+45', '9*(x+2)**2+9')],
                       '✔ تأكد بالسريع: المركز $-2$، والباقي 9. فـ $9x^2+36x+45=9(x+2)^2+9$، وهذا نفس اللي طلع بعد ما نطلّع 9.'),
                      ('sub', 'x+2', '1', 'نسمّي القوس $u$، و $du=dx$.'),
                      ('tex', r'\int\frac{dx}{3\sqrt{(x+2)^{2}+1}}=\frac13\int\frac{du}{\sqrt{u^{2}+1^{2}}}', [('1/(3*sqrt((x+2)**2+1))', '1/sqrt(9*x**2+36*x+45)')],
                       'نعوّض، والـ 3 اللي تحت تصير $\\frac13$ برّا التكامل.'),
                      ('line', 'asinh(x+2)/3', 'القانون $\\sinh^{-1}\\frac ua$ مع $a=1$، ثم نرجع $u=x+2$.')])
    return U


# ---------------------------------------------------------------- 11
def u_square_lin():
    U = Unit('U-I9', 'إكمال المربع مع قوس برّا الجذر', '4.2', 'ص61، تمارين 15 و16', 3)
    U.add('idea', 'الفكرة', p(rich(
        'مثل النوع 10: نكمّل المربع تحت الجذر. الفرق إن فيه قوس مضروب برّا الجذر، وهذا القوس هو نفسه القوس اللي يطلع '
        'من إكمال المربع. لما نسمّيه $u$ يصير التكامل $\\int\\frac{du}{u\\sqrt{\\ldots}}$، وهذا قانون من جدول 4.2.')))
    U.add('sign', 'العلامة', p(rich('قوس مثل $(x+3)$ مضروب برّا جذر، وتحت الجذر $x^2$ و $x$ ورقم.')))
    U.prev('مثل النوع 10، لكن فيه قوس برّا الجذر. فالقانون يتغير: بدل $\\sinh^{-1}$ و $\\cosh^{-1}$ يطلع $\\operatorname{csch}^{-1}$ أو $\\operatorname{sech}^{-1}$.')
    laws = (md(r'\int\frac{du}{u\sqrt{u^{2}+a^{2}}}=-\frac1a\operatorname{csch}^{-1}\frac{|u|}{a}+C')
            + md(r'\int\frac{du}{u\sqrt{a^{2}-u^{2}}}=-\frac1a\operatorname{sech}^{-1}\frac{|u|}{a}+C'))
    U.add('short', '🧭 الطريقة', method([
        'نكمّل المربع تحت الجذر (مثل النوع 10).',
        'نتأكد إن القوس اللي برّا الجذر هو نفسه القوس اللي طلع.',
        'نسمّيه $u$، و $du=dx$.',
        '(قوس)² + رقم يعني $\\operatorname{csch}^{-1}$. ورقم − (قوس)² يعني $\\operatorname{sech}^{-1}$. ثم نرجع $u$.'],
        tricks_=['<b>$u$ برّا الجذر</b> يعني الجواب يبدأ بسالب و $\\frac1a$، ومعه $|u|$. مثال: $a=2$ يعني $-\\frac12$ قدّام الجواب.',
                 '<b>القوس برّا الجذر لازم يكون نفس القوس</b> اللي يطلع من إكمال المربع. إذا اختلف، هذا مو النوع 11.'], label='U-I9') + laws)
    it = ITEMS['N42-E2-8']
    ex = question(it, 'U-I9 example')
    ex += steps(it, [
        ('tex', r'-x^{2}+2x+3=-\left(x^{2}-2x\right)+3', [('-x**2+2*x+3', '-(x**2-2*x)+3')],
         'معامل $x^2$ سالب. نطلّع السالب من حدّي $x$ عشان نكمّل المربع داخل القوس.'),
        ('tex', r'x^{2}-2x=\left(x^{2}-2x+1\right)-1=(x-1)^{2}-1', [('x**2-2*x', '(x-1)**2-1')],
         'نكمّل المربع داخل القوس: نص $-2$ هو $-1$، ومربعه 1. نضيفه ونطرحه.'),
        ('tex', r'-\left[(x-1)^{2}-1\right]+3=4-(x-1)^{2}=2^{2}-(x-1)^{2}', [('-((x-1)**2-1)+3', '2**2-(x-1)**2')],
         'نرجّع السالب: يقلب الإشارتين. والأرقام: $1+3=4=2^2$.'),
        ('sub', 'x-1', '1', 'القوس برّا الجذر هو $(x-1)$، نفس القوس اللي طلع. نسمّيه $u$، و $du=dx$.'),
        ('tex', r'\int\frac{dx}{(x-1)\sqrt{-x^{2}+2x+3}}=\int\frac{du}{u\sqrt{2^{2}-u^{2}}}',
         [('1/((x-1)*sqrt(-x**2+2*x+3))', 'diff(x-1,x)/((x-1)*sqrt(2**2-(x-1)**2))')], 'نعوّض. صار بنفس شكل القانون.'),
        ('line', '-asech(Abs(x-1)/2)/2',
         'رقم ناقص مربع، و $u$ برّا الجذر. القانون: $-\\frac1a\\operatorname{sech}^{-1}\\frac{|u|}{a}$ مع $a=2$. ثم نرجع $u=x-1$.')], 'U-I9 ex')
    ex += final(it, 'U-I9 example')
    ex += p(rich('مذكرة د. طارق كتبت الجواب بدون $|\\,|$، فصار صحيح بس لما $x>1$.'), 'small')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('short', '⚡ الطريقة السريعة: المركز والباقي', shortcut(
        it, 'U-I9 ex',
        saves='تكمّل المربع بدون ما تطلّع السالب وترجّعه. هنا معامل $x^2$ سالب، وهذا أكثر مكان تضيع فيه الإشارات.',
        origin='نفس طريقة النوع 10: القوس ($x$ ناقص المركز) يصير صفر عند المركز، فاللي يبقى تحت الجذر هو الباقي. '
               'ومعامل $x^2$ يبقى قدّام القوس كما هو، حتى لو سالب.',
        steps_=['نحسب <b>المركز</b> = سالب معامل $x$ ÷ (2 × معامل $x^2$).',
                'نحسب <b>الباقي</b>: نعوّض المركز مكان $x$ في اللي تحت الجذر.',
                'نكتب: اللي تحت الجذر = (معامل $x^2$) × ($x$ ناقص المركز)² + الباقي.',
                'نتأكد إن القوس برّا الجذر هو ($x$ ناقص المركز)، ثم القانون.'],
        rows=[('المركز: معامل $x$ هو 2، ومعامل $x^2$ هو $-1$.', r'-\frac{2}{2\times(-1)}=1', [('-Rational(2,2*(-1))', '1')]),
              ('الباقي: نعوّض 1 مكان $x$ تحت الجذر.', r'-(1)^{2}+2(1)+3=4=2^{2}', [('-1**2+2*1+3', '4')]),
              ('معامل $x^2$ هو $-1$، فنكتب $-1\times(x-1)^2+4$. نفس سطر 🧱، والقوس برّا الجذر $(x-1)$ ✓',
               r'-x^{2}+2x+3=4-(x-1)^{2}=2^{2}-(x-1)^{2}', [('-x**2+2*x+3', '2**2-(x-1)**2')]),
              ('رقم ناقص مربع، و $u$ برّا الجذر: قانون $\\operatorname{sech}^{-1}$ مع $a=2$. نفس جواب 🧱 ✓',
               r'-\frac12\operatorname{sech}^{-1}\frac{|x-1|}{2}+C', [('=ANS', '-asech(Abs(x-1)/2)/2')])],
        memo='المركز يصفّر القوس، والباقي هو اللي يبقى. ومعامل $x^2$ يبقى قدّام القوس بإشارته.',
        never=['إذا القوس برّا الجذر مو ($x$ ناقص المركز)، ما ينفع هذا القانون.',
               'إذا ما فيه قوس برّا الجذر، هذا النوع 10.'],
        paper='تكتب السطر اللي طلع: $-x^2+2x+3=2^2-(x-1)^2$، ثم $u=x-1$.',
        ask='اكتب كل واحد على شكل الباقي ± (قوس)²',
        tries=[('-x^{2}+4x', r'4-(x-2)^{2}', [('-x**2+4*x', '4-(x-2)**2')]),
               ('x^{2}-6x+13', r'(x-3)^{2}+4', [('x**2-6*x+13', '(x-3)**2+4')]),
               ('-x^{2}-6x', r'9-(x+3)^{2}', [('-x**2-6*x', '9-(x+3)**2')])]))
    U.add('trap', '⚠️ الفخ', ul([rich('القوس برّا الجذر لازم يكون نفس القوس داخل المربع، وإلا ما تنفع الطريقة.'),
                                rich('اكتب $|u|$ في الجواب. أغلب المفاتيح الرسمية تنساها.')]))
    U.add('paper', '✍️ في ورقة الكويز', md(r'-x^{2}+2x+3=2^{2}-(x-1)^{2}') + md(r'u=x-1\qquad du=dx')
          + md(r'\int\frac{du}{u\sqrt{2^{2}-u^{2}}}=-\frac12\operatorname{sech}^{-1}\frac{|x-1|}{2}+C'))
    U.add('ok', '✔ تأكد', p(rich('افتح القوس: $4-(x-1)^2=4-x^2+2x-1=-x^2+2x+3$ ✓. والجواب يبدأ بإشارة سالبة دايم.')))
    U.gist('قوس برّا جذر، وتحت الجذر $x^2$ و $x$ ورقم', 'كمّل المربع، وتأكد إن القوس نفسه',
           'سمّ القوس $u$: (قوس)² + رقم يعني $\\operatorname{csch}^{-1}$، ورقم − (قوس)² يعني $\\operatorname{sech}^{-1}$')
    U.drill('1', '1447-S2-FE-Q2.6', 'G', 'معامل $x^2$ موجب، يعني $\\operatorname{csch}^{-1}$.',
            first=r'x^{2}+6x+13=\left(x^{2}+6x+9\right)+4=(x+3)^{2}+2^{2}',
            claims=[('x**2+6*x+13', '(x+3)**2+2**2')],
            sol_rows=[('sub', 'x+3', '1', 'القوس برّا الجذر $(x+3)$ نفس القوس. نسمّيه $u$، و $du=dx$.'),
                      ('tex', r'=\int\frac{du}{u\sqrt{u^{2}+2^{2}}}', [('1/((x+3)*sqrt(x**2+6*x+13))', 'diff(x+3,x)/((x+3)*sqrt((x+3)**2+2**2))')],
                       'نعوّض. صار مربع زائد رقم، و $u$ برّا الجذر.'),
                      ('line', '-acsch(Abs(x+3)/2)/2', 'القانون: $-\\frac1a\\operatorname{csch}^{-1}\\frac{|u|}{a}$ مع $a=2$. ثم نرجع $u=x+3$.')])
    U.drill('2', 'N42-X2-15', 'P', 'نص 6 هو 3، ومربعه 9.',
            sol_rows=[('tex', r'x^{2}+6x+25=\left(x^{2}+6x+9\right)+16=(x+3)^{2}+4^{2}', [('x**2+6*x+25', '(x+3)**2+4**2')],
                       'نكمّل المربع: نص 6 هو 3، ومربعه 9. والباقي $25-9=16=4^2$.'),
                      ('tex', r'-\frac{6}{2\times1}=-3,\qquad (-3)^{2}+6(-3)+25=16', [('-Rational(6,2)', '-3'), ('(-3)**2+6*(-3)+25', '16')],
                       '✔ تأكد بالسريع: المركز $-3$، والباقي 16. نفس اللي طلع.'),
                      ('sub', 'x+3', '1', 'القوس برّا الجذر نفس القوس. نسمّيه $u$.'),
                      ('tex', r'=2\int\frac{du}{u\sqrt{u^{2}+4^{2}}}', [('2/((x+3)*sqrt(x**2+6*x+25))', '2*diff(x+3,x)/((x+3)*sqrt((x+3)**2+4**2))')],
                       'نعوّض، والرقم 2 يطلع برّا التكامل.'),
                      ('line', '-acsch(Abs(x+3)/4)/2', 'القانون مع $a=4$: $2\\cdot\\left(-\\frac14\\right)=-\\frac12$. ثم نرجع $u$.')])
    U.drill('3', 'N42-X2-16', 'I', 'معامل $x^2$ سالب، فنطلّع السالب أول.',
            sol_rows=[('tex', r'3-x^{2}-2x=-\left(x^{2}+2x\right)+3', [('3-x**2-2*x', '-(x**2+2*x)+3')], 'نطلّع السالب من حدّي $x$.'),
                      ('tex', r'=-\left[(x+1)^{2}-1\right]+3=4-(x+1)^{2}', [('-((x+1)**2-1)+3', '4-(x+1)**2')],
                       'نكمّل المربع داخل القوس: نص 2 هو 1. ونرجّع السالب.'),
                      ('tex', r'-\frac{-2}{2\times(-1)}=-1,\qquad 3-(-1)^{2}-2(-1)=4', [('-Rational(-2,-2)', '-1'), ('3-(-1)**2-2*(-1)', '4')],
                       '✔ تأكد بالسريع: معامل $x$ هو $-2$ ومعامل $x^2$ هو $-1$. المركز $-1$، والباقي 4. نفس اللي طلع.'),
                      ('sub', 'x+1', '1', 'القوس برّا الجذر $(x+1)$ نفس القوس. نسمّيه $u$.'),
                      ('tex', r'=3\int\frac{du}{u\sqrt{2^{2}-u^{2}}}', [('3/((x+1)*sqrt(3-x**2-2*x))', '3*diff(x+1,x)/((x+1)*sqrt(2**2-(x+1)**2))')],
                       'نعوّض، والرقم 3 يطلع برّا.'),
                      ('line', '-3*asech(Abs(x+1)/2)/2', 'رقم ناقص مربع: القانون $\\operatorname{sech}^{-1}$ مع $a=2$. $3\\cdot\\left(-\\frac12\\right)=-\\frac32$.')])
    return U


UNITS_42 = [u_deriv, u_deriv_rules, u_six, u_tanh, u_sech, u_lamda, u_sqrt, u_split, u_invnum, u_square, u_square_lin]

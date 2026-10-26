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
        "كل دالة عكسية لها مشتقة جاهزة في الجدول، بس الجدول مكتوب لـ 🔵 $u$. "
        "ولما الداخل مو $x$ لحالها، قاعدة السلسلة (نفسها اللي في 4.1) تضرب في 🟢 مشتقة الداخل $u'$.")))
    U.add('sign', 'العلامة', p(rich(
        '<b>إذا شفت:</b> <b>Find dy/dx</b> أو <b>Find the derivative</b>، وفي السؤال $\\sinh^{-1}$ أو $\\cosh^{-1}$ أو $\\tanh^{-1}$ '
        'أو $\\coth^{-1}$ أو $\\operatorname{sech}^{-1}$ أو $\\operatorname{csch}^{-1}$، لحالها أو مجموعة مع دالة ثانية.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> الدالة العكسية داخل أس أو $\\ln$ أو قوة أو ضرب: نفس الاشتقاق، بس نبدأ بالطبقة اللي برّا '
                   '(مشتقات مركبة). أو المطلوب تكامل، مو مشتقة: هذا تعويض.'))
          + contrast([(r'y=\sinh^{-1}(3x)', "اشتقاق بالجدول: $\\frac{u'}{\\sqrt{u^2+1}}$ مع $u=3x$", 'دالة عكسية: الـ $-1$ اسم، مو أس'),
                      (r'y=\sinh(3x)', 'اشتقاق من 4.1: $\\cosh(3x)\\cdot3$', 'دالة عادية، مو عكسية'),
                      (r'y=\left(\sinh^{-1}3x\right)^{2}', 'اشتقاق: القوة أول، ثم $\\sinh^{-1}$', 'الدالة العكسية داخل قوة'),
                      (r'\int\frac{dx}{\sqrt{x^{2}+49}}', 'تعويض: $u=x$ و $a=7$، قانون $\\sinh^{-1}$', 'المطلوب تكامل، مو مشتقة')]))
    law, _ = sc_twins()
    U.add('short', '📐 القانون: جدول مشتقات الدوال العكسية', law + method([
        '<b>وش الدالة اللي برّا؟</b> الدالة العكسية نفسها، مثل $\\sinh^{-1}$. واللي داخلها نسمّيه 🔵 $u$.',
        '<b>مشتقتها من الجدول، والداخل يبقى مثل ما هو:</b> نكتب قانونها، ونحط $u$ مكانه بدون ما نغيّره.',
        "<b>🟢 × مشتقة الداخل:</b> نشتق $u$، ونحط $u'$ فوق في القانون.",
        '<b>بسّط:</b> مربع الجذر، والكسر فوق كسر.'], tricks_=[
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
        ('tex', r"\cU{u=5x-1},\qquad \cD{u'=5}", [('diff(5*x-1,x)', '5')],
         'داخل $\\sinh^{-1}$ مو $x$ لحالها، فنسمّيه 🔵 $u$ ونشتقه. مشتقة $5x$ هي 5، والرقم $-1$ مشتقته 0.'),
        ('tex', r"\left(\sinh^{-1}\cU{u}\right)'=\frac{\cD{u'}}{\sqrt{\cU{u}^{2}+1}}", [('diff(asinh(x),x)', '1/sqrt(x**2+1)')],
         "قانون $\\sinh^{-1}$ من الجدول. فيه 🟢 $u'$ فوق لأن داخل الدالة مو $x$ لحالها."),
        ('line', '5/sqrt(1+(5*x-1)**2)', "نعوّض 🟢 $u'=5$ فوق، و 🔵 $u=5x-1$ تحت.")], 'U-D1 ex1')
    ex += final(it, 'U-D1 example 1')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)

    it = ITEMS['1447-S2-SE-Q1.2']
    ex = question(it, 'U-D1 example 2')
    ex += steps(it, [
        ('tex', r"\cU{u=\sqrt{x+2}},\qquad \cD{u'=\frac{1}{2\sqrt{x+2}}}", [('diff(sqrt(x+2),x)', '1/(2*sqrt(x+2))')],
         'داخل $\\operatorname{csch}^{-1}$ جذر، فنسمّيه 🔵 $u$. مشتقة الجذر = 1 على ضعف الجذر، في مشتقة اللي تحته (هنا 1).'),
        ('tex', r"\left(\operatorname{csch}^{-1}\cU{u}\right)'=\cR{-}\frac{\cD{u'}}{|\cU{u}|\sqrt{1+\cU{u}^{2}}}",
         [('diff(acsch(x),x)', '-1/(Abs(x)*sqrt(1+x**2))', 't'), ('diff(acsch(x),x)', '-1/(Abs(x)*sqrt(1+x**2))', '-t')],
         'قانون $\\operatorname{csch}^{-1}$ من الجدول: فيه 🔴 سالب، و $|u|$ برّا الجذر.'),
        ('tex', r'|u|=\sqrt{x+2}', [('Abs(sqrt(x+2))', 'sqrt(x+2)', 't-2')], 'الجذر موجب دايم، فالقيمة المطلقة ما تغيّر شي.'),
        ('tex', r'u^{2}=\left(\sqrt{x+2}\right)^{2}=x+2', [('sqrt(x+2)**2', 'x+2')], 'الجذر تربيعه يرجّع اللي تحته.'),
        ('tex', r'1+u^{2}=1+x+2=x+3', [('1+x+2', 'x+3')], 'نجمع الأرقام: $1+2=3$.'),
        ('tex', r"y'=\cR{-}\frac{\ \cD{\frac{1}{2\sqrt{x+2}}}\ }{\cU{\sqrt{x+2}}\,\sqrt{x+3}}",
         [('diff(acsch(sqrt(x+2)),x)', '-(1/(2*sqrt(x+2)))/(sqrt(x+2)*sqrt(x+3))', 't-2')],
         "نعوّض في القانون: 🟢 $u'$ فوق، و $|u|$ و $\\sqrt{1+u^2}$ تحت."),
        ('tex', r"y'=\cR{-}\frac{1}{2\sqrt{x+2}\cdot\sqrt{x+2}\cdot\sqrt{x+3}}",
         [('-(1/(2*sqrt(x+2)))/(sqrt(x+2)*sqrt(x+3))', '-1/(2*sqrt(x+2)*sqrt(x+2)*sqrt(x+3))')],
         'كسر فوق كسر: مقام الكسر الصغير $2\\sqrt{x+2}$ ينزل ويُضرب في المقام الكبير.'),
        ('line', '-1/(2*(x+2)*sqrt(x+3))', 'الجذر في نفسه يعطي اللي تحته: $\\sqrt{x+2}\\cdot\\sqrt{x+2}=x+2$.')], 'U-D1 ex2')
    ex += final(it, 'U-D1 example 2')
    U.add('ex', '🧱 مثال 2 محلول خطوة خطوة (اختبار سابق)', ex)

    it2 = ITEMS['1446-S2-SE-Q1.2']
    U.add('trap', '⚠️ الفخ', ul([
        rich("أكثر غلطة: تنسى تضرب في $u'$."),
        rich("✎ إشارة $\\coth^{-1}$: دكتورك (محاضرة 13) يكتب $(\\coth^{-1}u)'=-\\frac{u'}{1-u^2}$ بسالب، وهو اللي يصحح، "
             '<b>فاكتبها مثله</b>. رياضيًا هي موجبة مثل $\\tanh^{-1}$، ومفتاح 1446 كتبها موجبة. هذا سؤال 1446، وجوابه بالطريقتين:')])
          + md(q_tex(use(it2['id'], 'U-D1 trap'))) + final(it2, 'U-D1 trap'))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r"\cU{u=\sqrt{x+2}}\qquad \cD{u'=\frac{1}{2\sqrt{x+2}}}", [('diff(sqrt(x+2),x)', '1/(2*sqrt(x+2))')], 'U-D1 paper 1'))
          + md(arith(r"y'=\cR{-}\frac{\cD{u'}}{|\cU{u}|\sqrt{1+\cU{u}^{2}}}=\cR{-}\frac{\ \cD{\frac{1}{2\sqrt{x+2}}}\ }{\cU{\sqrt{x+2}}\,\sqrt{x+3}}",
                     [('diff(acsch(sqrt(x+2)),x)', '-(1/(2*sqrt(x+2)))/(sqrt(x+2)*sqrt(x+3))', 't-2')], 'U-D1 paper 2'))
          + md(arith(r"y'=\cR{-}\frac{1}{2(x+2)\sqrt{x+3}}", [('diff(acsch(sqrt(x+2)),x)', '-1/(2*(x+2)*sqrt(x+3))', 't-2')], 'U-D1 paper 3')))
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
    U.drill('3c', '1445-S1-SE-Q1.2', 'I', '✎ الأول $\\coth^{-1}$ مع $u=3x$، واكتبه بإشارة دكتورك. الثاني قوة، ثم tanh، ثم جذر.',
            sol_rows=[('tex', r"\left(\coth^{-1}3x\right)'=\frac{\cD{3}}{1-9x^{2}}", [('diff(acoth(3*x),x)', '3/(1-9*x**2)', '1/3+t')],
                       'قانون $\\coth^{-1}$ مع 🔵 $u=3x$، بالإشارة الرياضية. ✎ دكتورك يكتبه بسالب: $-\\frac{3}{1-9x^2}$.'),
                      ('tex', r"\left(\tanh^{2}\sqrt{2x}\right)'=2\tanh\sqrt{2x}\cdot\operatorname{sech}^{2}\sqrt{2x}\cdot\cD{\frac{1}{\sqrt{2x}}}",
                       [('diff(tanh(sqrt(2*x))**2,x)', '2*tanh(sqrt(2*x))*sech(sqrt(2*x))**2/sqrt(2*x)', 't')],
                       'ثلاث طبقات: القوة، ثم tanh، ثم 🟢 مشتقة $\\sqrt{2x}$ وهي $\\frac{2}{2\\sqrt{2x}}=\\frac{1}{\\sqrt{2x}}$.')])
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
    U.drill('4', '1445-S2-SE-Q1.1', 'I', 'الأول من 4.1. الثاني قانون $\\operatorname{sech}^{-1}$ مع $u=3x$.',
            sol_rows=[('tex', r"\left(\tanh(2x^{3})\right)'=\operatorname{sech}^{2}(2x^{3})\cdot6x^{2}",
                       [('diff(tanh(2*x**3),x)', 'sech(2*x**3)**2*6*x**2')],
                       'الحد الأول دالة عادية من 4.1: مشتقة tanh هي $\\operatorname{sech}^2$، والداخل يبقى، ثم × مشتقة الداخل ($6x^2$).'),
                      ('tex', r"u=3x,\qquad u'=3", [('diff(3*x,x)', '3')],
                       'الحد الثاني: داخل $\\operatorname{sech}^{-1}$ هو $3x$، فنسمّيه $u$. مشتقته 3.'),
                      ('tex', r"\left(\operatorname{sech}^{-1}u\right)'=-\frac{u'}{u\sqrt{1-u^{2}}}",
                       [('diff(asech(x),x)', '-1/(x*sqrt(1-x**2))', 't/(1+t)')],
                       'قانون $\\operatorname{sech}^{-1}$ من الجدول: فيه سالب، و $u$ برّا الجذر.'),
                      ('tex', r"\left(\operatorname{sech}^{-1}3x\right)'=-\frac{3}{3x\sqrt{1-9x^{2}}}",
                       [('diff(asech(3*x),x)', '-3/(3*x*sqrt(1-9*x**2))', 't/(3*(1+t))')],
                       "نعوّض $u=3x$ و $u'=3$. و $(3x)^2=9x^2$."),
                      ('tex', r'=-\frac{1}{x\sqrt{1-9x^{2}}}', [('-3/(3*x*sqrt(1-9*x**2))', '-1/(x*sqrt(1-9*x**2))', 't/(3*(1+t))')],
                       'نختصر 3 فوق مع 3 تحت.'),
                      ('line', '6*x**2*sech(2*x**3)**2-1/(x*sqrt(1-9*x**2))', 'نجمع مشتقة الحدين.')])
    U.drill('5', '1445-S2-SE-Q1.2', 'I', 'الأول قانون $\\cosh^{-1}$ مع $u=\\sqrt x$. الثاني ثلاث طبقات: قوة، ثم sinh، ثم $\\frac1x$.',
            sol_rows=[('tex', r"u=\sqrt{x},\qquad u'=\frac{1}{2\sqrt{x}}", [('diff(sqrt(x),x)', '1/(2*sqrt(x))')],
                       'الحد الأول: داخل $\\cosh^{-1}$ جذر، فنسمّيه $u$. مشتقة الجذر = 1 على ضعف الجذر.'),
                      ('tex', r"\left(\cosh^{-1}u\right)'=\frac{u'}{\sqrt{u^{2}-1}}", [('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t')],
                       'قانون $\\cosh^{-1}$ من الجدول.'),
                      ('tex', r"\left(\cosh^{-1}\sqrt{x}\right)'=\frac{\ \frac{1}{2\sqrt{x}}\ }{\sqrt{x-1}}=\frac{1}{2\sqrt{x}\,\sqrt{x-1}}",
                       [('diff(acosh(sqrt(x)),x)', '(1/(2*sqrt(x)))/sqrt(x-1)', '1+t'),
                        ('(1/(2*sqrt(x)))/sqrt(x-1)', '1/(2*sqrt(x)*sqrt(x-1))', '1+t')],
                       "نعوّض: $u^2=(\\sqrt x)^2=x$. وكسر فوق كسر: مقام الكسر الصغير $2\\sqrt x$ ينزل تحت."),
                      ('tex', r"\left(\frac1x\right)'=\left(x^{-1}\right)'=-\frac{1}{x^{2}}", [('diff(1/x,x)', '-1/x**2', 't')],
                       'الحد الثاني: أعمق طبقة $\\frac1x$. نكتبها $x^{-1}$، ومشتقتها $-x^{-2}$.'),
                      ('tex', r"\left(\sinh^{3}\tfrac1x\right)'=3\sinh^{2}\tfrac1x\cdot\cosh\tfrac1x\cdot\left(-\frac{1}{x^{2}}\right)",
                       [('diff(sinh(1/x)**3,x)', '3*sinh(1/x)**2*cosh(1/x)*(-1/x**2)', 't')],
                       'من برّا لجوّا: القوة مشتقتها $3\\sinh^2$، ثم مشتقة sinh هي cosh، ثم × مشتقة $\\frac1x$.'),
                      ('line', '1/(2*sqrt(x)*sqrt(x-1))-3*sinh(1/x)**2*cosh(1/x)/x**2', 'نجمع مشتقة الحدين. والسالب يطلع قدّام الحد الثاني.')])
    U.drill('6', '1446-S2-FE-Q1.3', 'I', 'الأول من 4.1 مع $\\sqrt x$. الثاني قانون $\\sinh^{-1}$ مع $u=\\frac{2}{\\sqrt x}=2x^{-1/2}$.',
            sol_rows=[('tex', r"\left(\tanh\sqrt{x}\right)'=\operatorname{sech}^{2}\sqrt{x}\cdot\frac{1}{2\sqrt{x}}",
                       [('diff(tanh(sqrt(x)),x)', 'sech(sqrt(x))**2/(2*sqrt(x))', 't')],
                       'الحد الأول دالة عادية من 4.1: مشتقة tanh هي $\\operatorname{sech}^2$، ثم × مشتقة الداخل $\\sqrt x$.'),
                      ('tex', r"u=\frac{2}{\sqrt{x}}=2x^{-1/2},\qquad u'=-x^{-3/2}=-\frac{1}{x^{3/2}}",
                       [('2/sqrt(x)', '2*x**Rational(-1,2)', 't'), ('diff(2/sqrt(x),x)', '-1/x**Rational(3,2)', 't')],
                       'الحد الثاني: داخل $\\sinh^{-1}$ هو $\\frac{2}{\\sqrt x}$. نكتبه بأس سالب عشان نشتقه: $2\\cdot\\left(-\\frac12\\right)=-1$، والأس $-\\frac12-1=-\\frac32$.'),
                      ('tex', r"\left(\sinh^{-1}u\right)'=\frac{u'}{\sqrt{u^{2}+1}}", [('diff(asinh(x),x)', '1/sqrt(x**2+1)')],
                       'قانون $\\sinh^{-1}$ من الجدول.'),
                      ('tex', r'u^{2}=\left(\frac{2}{\sqrt{x}}\right)^{2}=\frac{4}{x}', [('(2/sqrt(x))**2', '4/x', 't')],
                       'نربّع فوق وتحت: $2^2=4$، و $(\\sqrt x)^2=x$.'),
                      ('tex', r"\left(\sinh^{-1}\frac{2}{\sqrt{x}}\right)'=\frac{-\frac{1}{x^{3/2}}}{\sqrt{\frac{4}{x}+1}}",
                       [('diff(asinh(2/sqrt(x)),x)', '-1/(x**Rational(3,2)*sqrt(4/x+1))', 't')],
                       "نعوّض $u'$ فوق، و $u^2$ تحت."),
                      ('line', 'sech(sqrt(x))**2/(2*sqrt(x))-1/(x**Rational(3,2)*sqrt(1+4/x))', 'نجمع مشتقة الحدين.')])
    return U


def box_memo(memo):
    return '<div class="memo-inline"><b>كيف أتذكّره:</b> ' + memo + '</div>'


# ---------------------------------------------------------------- 2
def u_deriv_rules():
    U = Unit('U-D2', 'مشتقات مركبة: أسية، ln، قوة، ضرب', '4.2', 'ص59، تمارين 1–6', 1)
    U.add('idea', 'الفكرة', p(rich(
        'كل طبقة لها قاعدة مشتقة: الأسية، و $\\ln$، والقوة، والضرب. '
        'وقاعدة السلسلة تقول: مشتقة الطبقة اللي برّا، × 🟢 مشتقة اللي داخلها، وهكذا لين نوصل لـ $x$.')))
    U.add('sign', 'العلامة', p(rich('<b>إذا شفت:</b> مشتقة، والدالة العكسية <b>داخل</b> شي ثاني: أس مثل $6^{(\\ldots)}$، '
                                    'أو $\\ln$ أو $\\log$، أو قوس مرفوع لقوة، أو مضروبة في دالة ثانية.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> الدالة العكسية لحالها، أو مجموعة مع دالة ثانية بـ +: اشتقاق بالجدول على طول. '
                   'أو $x$ في الأساس وفي الأس مع بعض، مثل $x^{\\sinh^{-1}x}$: هذا الاشتقاق اللوغاريتمي.'))
          + contrast([(r'y=6^{\cosh^{-1}(2x)}', "اشتقاق: الأسية أول، $6^{u}\\ln6\\cdot u'$", 'الدالة العكسية داخل الأس'),
                      (r'y=\cosh^{-1}\left(6^{x}\right)', "اشتقاق: $\\cosh^{-1}$ أول، ثم $u'=6^x\\ln6$", 'الأسية داخل الدالة العكسية'),
                      (r'y=x^{\sinh^{-1}x}', 'الاشتقاق اللوغاريتمي: $\\ln y$ أول', '$x$ في الأساس وفي الأس')]))
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
        '<b>وش الدالة اللي برّا؟</b> الطبقة الكبيرة: أسية، أو $\\ln$، أو قوة، أو ضرب.',
        "<b>مشتقتها من الجدول، والداخل يبقى مثل ما هو:</b> مثل $\\left(6^{u}\\right)'=6^{u}\\ln6\\cdot u'$، و $u$ يبقى مكتوب كامل.",
        '<b>🟢 × مشتقة الداخل:</b> الداخل دالة عكسية، فنشتقه بجدول مشتقات الدوال العكسية في سطر لحاله.',
        '<b>بسّط:</b> نعوّض في السطر الأول، ونرتّب الأرقام قدّام.'], tricks_=[
        ('نشتق من برّا لجوّا: كل طبقة مشتقتها، ونضربها في بعض. مثال: $\\left(\\sinh^{-1}2x\\right)^3$ برّا قوة، مشتقتها '
         '$3\\left(\\sinh^{-1}2x\\right)^2$. وجوّا $\\sinh^{-1}2x$، مشتقتها $\\frac{2}{\\sqrt{4x^2+1}}$. ونضربهم.',
         [('diff(asinh(2*x)**3,x)', '3*asinh(2*x)**2*2/sqrt(4*x**2+1)')])], label='U-D2'))
    it = ITEMS['N42-E1-4']
    ex = question(it, 'U-D2 example')
    ex += steps(it, [
        ('tex', r"y'=6^{\cU{u}}\cdot\ln6\cdot\cD{u'},\qquad \cU{u=\cosh^{-1}(2x)}",
         [('diff(6**acosh(2*x),x)', '6**acosh(2*x)*log(6)*diff(acosh(2*x),x)')],
         "هنا التريك: نبدأ من برّا. برّا أسية، والقانون $(a^u)'=a^u\\ln a\\cdot u'$، وهنا $a=6$ و 🔵 $u$ الأس كله."),
        ('tex', r"\cD{u'}=\frac{2}{\sqrt{(2x)^{2}-1}}", [('diff(acosh(2*x),x)', '2/sqrt((2*x)**2-1)', '1/2+t')],
         'بعدها جوّا: نشتق الأس بقانون $\\cosh^{-1}$ من جدول مشتقات الدوال العكسية. اللي داخله $2x$، ومشتقته 2.'),
        ('tex', r"\cD{u'}=\frac{2}{\sqrt{4x^{2}-1}}", [('2/sqrt((2*x)**2-1)', '2/sqrt(4*x**2-1)')],
         'نفك المربع: $(2x)^2=2^2\\cdot x^2=4x^2$.'),
        ('line', '6**acosh(2*x)*2*log(6)/sqrt(4*x**2-1)', "نعوّض 🟢 $u'$ في السطر الأول، ونرتّب الأرقام قدّام.")], 'U-D2 ex')
    ex += final(it, 'U-D2 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([
        rich('رتّب: القاعدة الكبيرة أول، ثم اللي داخلها. لا تشتق الدالة العكسية وتنسى الأسية.'),
        rich('مع $a^u$ لا تنسى $\\ln a$. ومع $\\log$ (أساس 10) لا تنسى $\\ln10$ في المقام.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r"y'=6^{\cU{u}}\cdot\ln6\cdot\cD{u'}", [('diff(6**acosh(2*x),x)', '6**acosh(2*x)*log(6)*diff(acosh(2*x),x)')], 'U-D2 paper 1'))
          + md(arith(r"\cU{u=\cosh^{-1}(2x)}\qquad \cD{u'=\frac{2}{\sqrt{4x^{2}-1}}}", [('diff(acosh(2*x),x)', '2/sqrt(4*x**2-1)', '1/2+t')], 'U-D2 paper 2'))
          + md(arith(r"y'=6^{\cosh^{-1}(2x)}\cdot\ln6\cdot\cD{\frac{2}{\sqrt{4x^{2}-1}}}",
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
        'كل قانون مشتقة لدالة عكسية يعطينا قانون تكامل بالعكس. '
        'والتعويض يحوّل السؤال لشكل القانون بالضبط: 🔵 $u^2$ ورقم مربع $a^2$ تحت الجذر، و 🟢 $du$ فوق.')))
    U.add('sign', 'العلامة', p(rich('<b>إذا شفت:</b> تكامل كسر، وتحته جذر فيه مربع زائد رقم أو مربع ناقص رقم (مثل $\\sqrt{4x^2+25}$)، '
                                    'وفوق رقم أو جزء من مشتقة الداخل.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> فوق مشتقة اللي تحت الجذر <b>كله</b> (مثل $\\frac{x}{\\sqrt{x^2+49}}$): تعويض $w$ = اللي تحت الجذر، '
                   'والجواب جذر. أو تحت الجذر رقم ناقص مربع ($\\sqrt{49-x^2}$): هذا $\\sin^{-1}$ من 3.4. '
                   'أو تحت الجذر حد $x$ زيادة ($x^2+6x+13$): تجهيز: كمّل المربع أول.'))
          + contrast([(r'\int\frac{dx}{\sqrt{x^{2}+49}}', 'تعويض: $u=x$ و $a=7$، قانون $\\sinh^{-1}$', 'البسط رقم، وتحت الجذر مربع زائد رقم'),
                      (r'\int\frac{x\,dx}{\sqrt{x^{2}+49}}', 'تعويض: $w=x^2+49$، والجواب $\\sqrt{x^2+49}$', 'البسط $x$، يعني مشتقة اللي تحت الجذر كله تقريبًا'),
                      (r'\int\frac{dx}{\sqrt{49-x^{2}}}', '$\\sin^{-1}\\frac x7$ (درس 3.4)', 'رقم ناقص مربع تحت الجذر'),
                      (r'\int\frac{dx}{\sqrt{x^{2}+6x+13}}', 'تجهيز: كمّل المربع، ثم $u=x+3$', 'فيه حد $x$ تحت الجذر')]))
    r = [formula('1/sqrt(u**2+a**2)', 'asinh(u/a)', pos=('a',), label='U-I1 law sinh'),
         formula('1/sqrt(u**2-a**2)', 'acosh(u/a)', branches=('a+t',), pos=('a',), label='U-I1 law cosh'),
         formula('1/(a**2-u**2)', 'atanh(u/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-I1 law tanh'),
         formula('1/(a**2-u**2)', 'acoth(u/a)/a', branches=('a+t', '-a-t'), pos=('a',), label='U-I1 law coth'),
         formula('1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-I1 law sech'),
         formula('1/(u*sqrt(a**2+u**2))', '-acsch(Abs(u)/a)/a', pos=('a',), label='U-I1 law csch')]
    conds = ['كل ' + mi('u'), mi('u>a'), mi('|u|<a'), mi('|u|>a') + ' ✎ دكتورك', mi('0<|u|<a'), mi(r'u\neq0')]
    from booklet import doctor_coth, doctor_note
    r[3] = (r[3][0], doctor_coth('int'))          # the doctor's sign first; the math sign in the note under the table
    law = table(['التكامل', 'الجواب (+C)', 'الشرط'], [frow(z, c) for z, c in zip(r, conds)], 'formula') + doctor_note('int')
    law += p(rich('$a$ رقم موجب: الرقم اللي مربعه في السؤال. أول قانونين (جذر لحاله) بدون $\\frac1a$، والأربعة الباقية فيها $\\frac1a$.'), 'small')
    U.add('short', '📐 القانون: جدول التكاملات الستة', law + method([
        '<b>🔵 سمّ الداخل $u$:</b> نكتب كل حد تحت الجذر كمربع، مثل $4x^2=(2x)^2$. اللي داخل المربع هو $u$، والرقم $a^2$.',
        '<b>🟢 اشتقه: $du=\\ldots\\,dx$.</b> مثل $u=2x$ يعني $du=2\\,dx$.',
        '<b>🟠 اقسم اللي برّا على مشتقة الداخل: طلع رقم؟ هذا رقم التعديل، يطلع قدّام التكامل مرة وحدة بس.</b> '
        'فوق $dx$ بس (يعني 1)، ومشتقة الداخل 2، فرقم التعديل $\\frac12$.',
        '<b>اكتب التكامل كله بـ $u$، وطبّق القانون:</b> زائد تحت الجذر يعني $\\sinh^{-1}\\frac ua$، وناقص يعني $\\cosh^{-1}\\frac ua$.',
        '<b>رجّع $x$، وحط $+C$.</b>'], tricks_=[
        ('رقم التعديل: البسط ناقصه رقم عشان يصير $du$؟ نقسم عليه برّا. مثال: $u=3x^2$ يعني $du=6x\\,dx$، '
         'والبسط $x\\,dx$، فالبسط $=\\frac16du$.', [('diff(3*x**2,x)/6', 'x')]),
        ('نكتب اللي تحت الجذر كمربع: $9x^4=(3x^2)^2$، يعني $u=3x^2$.', [('9*x**4', '(3*x**2)**2')])], label='U-I1'))
    it = ITEMS['N42-E2-3']
    ex = question(it, 'U-I1 example 1')
    ex += steps(it, [
        ('tex', r'4x^{2}+25=(\cU{2x})^{2}+5^{2}', [('4*x**2+25', '(2*x)**2+5**2')],
         'تحت الجذر مو مكتوب كمربعات. جذر 4 هو 2، فـ $4x^2=(2x)^2$. و $25=5^2$.'),
        ('sub', '2*x', '2', 'نسمّي اللي داخل المربع 🔵 $u$. مشتقة $2x$ هي 2.'),
        ('tex', r'dx=\frac{\cD{du}}{\cA{2}}', [('diff(2*x,x)/2', '1')],
         'هنا التريك، 🟠 رقم التعديل: نقسم اللي برّا ($dx$ بس، يعني 1) على مشتقة الداخل (2)، فيطلع $\\frac12$.'),
        ('tex', r'\int\frac{dx}{\sqrt{4x^{2}+25}}=\cA{\frac12}\int\frac{\cD{du}}{\sqrt{\cU{u}^{2}+5^{2}}}',
         [('1/sqrt(4*x**2+25)', 'Rational(1,2)*diff(2*x,x)/sqrt((2*x)**2+5**2)')],
         'نعوّض. 🟠 الرقم $\\frac12$ ثابت، فيطلع قدّام التكامل مرة وحدة بس.'),
        ('tex', r'=\cA{\frac12}\sinh^{-1}\frac{\cU{u}}{5}', [('diff(asinh(x/5),x)', '1/sqrt(x**2+25)')],
         'القانون: $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$، وهنا $a=5$.'),
        ('line', 'asinh(2*x/5)/2', 'نرجع $u=2x$.')], 'U-I1 ex1')
    ex += final(it, 'U-I1 example 1')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    it = ITEMS['N42-X2-01']
    ex = question(it, 'U-I1 example 2')
    ex += steps(it, [
        ('tex', r'9+16x^{6}=3^{2}+\left(\cU{4x^{3}}\right)^{2}', [('9+16*x**6', '3**2+(4*x**3)**2')],
         'نكتب كل حد كمربع. جذر 16 هو 4، ونص الأس 6 هو 3، فـ $16x^6=(4x^3)^2$. و $9=3^2$.'),
        ('sub', '4*x**3', '12*x**2', 'نسمّي اللي داخل المربع 🔵 $u$. مشتقة $4x^3$ هي $12x^2$.'),
        ('tex', r'x^{2}\,dx=\frac{\cD{du}}{\cA{12}}', [('diff(4*x**3,x)/12', 'x**2')],
         'هنا التريك، 🟠 رقم التعديل: $du$ فيه 12 والبسط ما فيه، فنقسم على 12.'),
        ('tex', r'\int\frac{5x^{2}\,dx}{\sqrt{9+16x^{6}}}=5\cdot\cA{\frac{1}{12}}\int\frac{\cD{du}}{\sqrt{\cU{u}^{2}+3^{2}}}',
         [('5*x**2/sqrt(9+16*x**6)', '5*Rational(1,12)*diff(4*x**3,x)/sqrt((4*x**3)**2+3**2)')],
         'نعوّض. البسط $5x^2\\,dx$ يصير $5\\cdot\\frac{du}{12}$، والأرقام تطلع برّا التكامل.'),
        ('tex', r'5\cdot\frac{1}{12}=\cA{\frac{5}{12}}', [('5*Rational(1,12)', 'Rational(5,12)')], 'نضرب الرقمين: $5\\times1=5$ فوق، و 12 تحت.'),
        ('tex', r'=\cA{\frac{5}{12}}\sinh^{-1}\frac{\cU{u}}{3}', [('diff(asinh(x/3),x)', '1/sqrt(x**2+9)')],
         'القانون: $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$، وهنا $a=3$.'),
        ('line', '5*asinh(4*x**3/3)/12', 'نرجع $u=4x^3$.')], 'U-I1 ex2')
    ex += final(it, 'U-I1 example 2')
    U.add('ex', '🧱 مثال 2 محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تنسى الرقم اللي يطلع من التعويض، مثل $\\frac12$ أو $\\frac{5}{12}$.'),
                                rich('$\\cosh^{-1}$ يصح بس لما $u>a$، زي ما تشترط مذكرة د. طارق.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'4x^{2}+25=(\cU{2x})^{2}+5^{2}', [('4*x**2+25', '(2*x)**2+5**2')], 'U-I1 paper 1'))
          + md(arith(r'\cU{u=2x}\qquad \cD{du=2\,dx}', [('diff(2*x,x)', '2')], 'U-I1 paper 2'))
          + md(arith(r'\int\frac{dx}{\sqrt{4x^{2}+25}}=\cA{\frac12}\int\frac{\cD{du}}{\sqrt{\cU{u}^{2}+5^{2}}}=\cA{\frac12}\sinh^{-1}\frac{2x}{5}+C',
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
        'اللي يحدد واحد منهم هو المجال: $\\tanh^{-1}$ بس لما $|u|<a$، و $\\coth^{-1}$ بس لما $|u|>a$. فنقارن 🔵 $|u|$ مع $a$.')))
    U.add('sign', 'العلامة', p(rich('<b>إذا شفت:</b> تكامل كسر <b>بدون جذر</b>، وتحت رقم ناقص مربع (مثل $25-e^{2x}$)، '
                                    'وفوق مشتقة الداخل أو جزء منها.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> فوق مشتقة المقام كله (مثل $\\frac{x}{49-x^2}$): تعويض $w$ = المقام، والجواب $\\ln$. '
                   'أو المقام مجموع ($49+x^2$): هذا $\\tan^{-1}$ من 3.4. أو فيه جذر: تعويض بقانون $\\sinh^{-1}$ أو $\\cosh^{-1}$.'))
          + contrast([(r'\int\frac{dx}{49-x^{2}}', 'تعويض: $u=x$ و $a=7$، ثم قارن $|x|$ مع 7', 'رقم ناقص مربع، بدون جذر'),
                      (r'\int\frac{x\,dx}{49-x^{2}}', 'تعويض: $w=49-x^2$، والجواب $-\\frac12\\ln|49-x^2|$', 'البسط $x$، يعني مشتقة المقام تقريبًا'),
                      (r'\int\frac{dx}{49+x^{2}}', '$\\frac17\\tan^{-1}\\frac x7$ (درس 3.4)', 'مجموع، مو فرق')]))
    r = [formula('1/(a**2-u**2)', 'atanh(u/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-I2 law tanh'),
         formula('1/(a**2-u**2)', 'acoth(u/a)/a', branches=('a+t', '-a-t'), pos=('a',), label='U-I2 law coth')]
    from booklet import doctor_coth, doctor_note
    r[1] = (r[1][0], doctor_coth('int'))          # the doctor's sign (he marks the quiz); the math sign in the note below
    law = (table(['التكامل', 'الجواب (+C)', 'متى'], [frow(r[0], mi('|u|<a')), frow(r[1], mi('|u|>a') + ' ✎ دكتورك')], 'formula')
           + doctor_note('int'))
    U.add('short', '📐 القانون: tanh⁻¹ و coth⁻¹', law + method([
        '<b>🔵 سمّ الداخل $u$:</b> نكتب المقام كمربعين $a^2-u^2$. وإذا طلع مقلوب ($u^2-a^2$)، نطلّع 🔴 سالب أول.',
        '<b>🟢 اشتقه: $du=\\ldots\\,dx$.</b> مثل $u=e^x$ يعني $du=e^x\\,dx$.',
        '<b>🟠 اقسم اللي برّا على مشتقة الداخل: طلع رقم؟ هذا رقم التعديل، يطلع قدّام التكامل مرة وحدة بس.</b>',
        '<b>اكتب التكامل كله بـ $u$، وطبّق القانون:</b> نقارن $|u|$ مع $a$. أصغر يعني $\\tanh^{-1}$، وأكبر يعني $\\coth^{-1}$. ومعهم $\\frac1a$.',
        '<b>رجّع $x$، وحط $+C$.</b>'], tricks_=[
        ('tanh⁻¹ أم coth⁻¹؟ نقارن $u$ مع $a$: أصغر يعني $\\tanh^{-1}$، وأكبر يعني $\\coth^{-1}$. '
         'مثال: $u=e^x$ و $a=5$ و $x<0$، فـ $u<1<5$، يعني $\\tanh^{-1}$.', [('exp(0)', '1')]),
        ('رقم التعديل: $u=x^4$ يعني $du=4x^3dx$. والبسط $x^3dx$ ناقصه 4، فالبسط $=\\frac14du$.', [('diff(x**4,x)/4', 'x**3')])],
        label='U-I2'))
    it = ITEMS['N42-E2-2']
    ex = question(it, 'U-I2 example 1')
    ex += steps(it, [
        ('tex', r'25-e^{2x}=5^{2}-\left(\cU{e^{x}}\right)^{2}', [('25-exp(2*x)', '5**2-exp(x)**2')],
         'المقام بدون جذر: رقم ناقص أسية. نكتبه كمربعين: $e^{2x}=(e^x)^2$ لأن $x\\cdot2=2x$، و $25=5^2$.'),
        ('sub', 'exp(x)', 'exp(x)', 'نسمّي اللي داخل المربع 🔵 $u$. مشتقة $e^x$ هي نفسها.'),
        ('tex', r'\int\frac{e^{x}\,dx}{25-e^{2x}}=\int\frac{\cD{du}}{5^{2}-\cU{u}^{2}}', [('exp(x)/(25-exp(2*x))', 'diff(exp(x),x)/(5**2-exp(x)**2)')],
         'نعوّض. البسط $e^x\\,dx$ هو 🟢 $du$ تمامًا: اللي برّا ÷ مشتقة الداخل = 1، فما فيه رقم تعديل.'),
        ('tex', r'\cU{e^{x}}<e^{\ln5}=5', [('exp(log(5))', '5')],
         'هنا التريك: نقارن 🔵 $u$ مع $a=5$. مذكرة د. طارق تاخذ $x<\\ln5$، يعني $e^x<5$، يعني $|u|<a$.'),
        ('tex', r'=\frac15\tanh^{-1}\frac{\cU{u}}{5}', [('diff(atanh(x/5)/5,x)', '1/(25-x**2)')],
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
        ('tex', r'4-25\cosh^{2}x=2^{2}-(\cU{5\cosh x})^{2}', [('4-25*cosh(x)**2', '2**2-(5*cosh(x))**2')],
         'المقام رقم ناقص مربع، بدون جذر. نكتبه كمربعين: جذر 25 هو 5، و $4=2^2$.'),
        ('sub', '5*cosh(x)', '5*sinh(x)', 'نسمّي اللي داخل المربع 🔵 $u$. مشتقة $\\cosh x$ هي $\\sinh x$ (من 4.1).'),
        ('tex', r'\sinh x\,dx=\frac{\cD{du}}{\cA{5}}', [('diff(5*cosh(x),x)/5', 'sinh(x)')],
         '🟠 رقم التعديل: $du$ فيه 5 والبسط ما فيه، فنقسم على 5.'),
        ('tex', r'\int\frac{\sinh x\,dx}{4-25\cosh^{2}x}=\cA{\frac15}\int\frac{\cD{du}}{2^{2}-\cU{u}^{2}}',
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
                                rich('✎ مع $\\coth^{-1}$ اكتب جوابك بإشارة دكتورك (سالبة قدّام $\\frac1a$). خطوات الحل هنا بالإشارة الرياضية، '
                                     'وصندوق الجواب يكتب لك الشكلين.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'4-25\cosh^{2}x=2^{2}-(\cU{5\cosh x})^{2}', [('4-25*cosh(x)**2', '2**2-(5*cosh(x))**2')], 'U-I2 paper 1'))
          + md(arith(r'\cU{u=5\cosh x}\qquad \cD{du=5\sinh x\,dx}\qquad u\ge5>2', [('diff(5*cosh(x),x)', '5*sinh(x)'), ('5*cosh(0)', '5')], 'U-I2 paper 2'))
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
        'قانونا $\\operatorname{sech}^{-1}$ و $\\operatorname{csch}^{-1}$ فيهم 🔵 $u$ مرتين: برّا الجذر وداخله. '
        'فنضرب فوق وتحت في قوة $x$، عشان اللي برّا الجذر يصير $u$ نفسه، و 🟢 $du$ يطلع فوق.')))
    U.add('sign', 'العلامة', p(rich('<b>إذا شفت:</b> $x$ (أو قوة لـ $x$) مضروب <b>برّا</b> الجذر في المقام، وتحت الجذر رقم زائد أو ناقص '
                                    'قوة لـ $x$، مثل $x\\sqrt{16-x^4}$ أو $x\\sqrt{x^4+9}$.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> تحت الجذر قوة $x$ ناقص رقم (المربع قبل الرقم)، مثل $x\\sqrt{x^4-16}$: هذا $\\sec^{-1}$ من 3.4، '
                   'مو من جدول 4.2. أو برّا الجذر قوس مثل $(x+3)$ وتحت الجذر حد $x$ زيادة: تجهيز: كمّل المربع أول.'))
          + contrast([(r'\int\frac{dx}{x\sqrt{16-x^{4}}}', 'تعويض: اضرب في $\\frac xx$، ثم $u=x^2$، قانون $\\operatorname{sech}^{-1}$', 'رقم ناقص مربع، و $u$ برّا الجذر'),
                      (r'\int\frac{dx}{x\sqrt{x^{4}+16}}', 'تعويض: اضرب في $\\frac xx$، ثم $u=x^2$، قانون $\\operatorname{csch}^{-1}$', 'مربع زائد رقم، و $u$ برّا الجذر'),
                      (r'\int\frac{dx}{x\sqrt{x^{4}-16}}', '$\\sec^{-1}$ (درس 3.4)، مع $u=x^2$', 'مربع ناقص رقم: مو من جدول 4.2'),
                      (r'\int\frac{x\,dx}{\sqrt{16-x^{4}}}', '$\\sin^{-1}$ (درس 3.4)، مع $u=x^2$', 'ما فيه شي برّا الجذر')]))
    r = [formula('1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-I3 law sech'),
         formula('1/(u*sqrt(a**2+u**2))', '-acsch(Abs(u)/a)/a', pos=('a',), label='U-I3 law csch')]
    law = table(['التكامل', 'الجواب (+C)', 'الشرط'], [frow(r[0], mi('0<|u|<a')), frow(r[1], mi(r'u\neq0'))], 'formula')
    U.add('short', '📐 القانون: sech⁻¹ و csch⁻¹', law + method([
        '<b>🔵 سمّ الداخل $u$:</b> نكتب اللي تحت الجذر كمربعين: $16-x^4=4^2-(x^2)^2$، يعني $u=x^2$.',
        '<b>🟢 اشتقه: $du=\\ldots\\,dx$.</b> $du=2x\\,dx$.',
        '<b>🟠 اقسم اللي برّا على مشتقة الداخل: طلع رقم؟ هذا رقم التعديل، يطلع قدّام التكامل مرة وحدة بس.</b> '
        'برّا الجذر $x$ بس، ونبيه $u=x^2$. فنضرب فوق وتحت في $x$: يصير فوق $x\\,dx$، و $x\\div2x=\\frac12$.',
        '<b>اكتب التكامل كله بـ $u$، وطبّق القانون:</b> ناقص تحت الجذر يعني $\\operatorname{sech}^{-1}$، وزائد يعني $\\operatorname{csch}^{-1}$. '
        'والجواب يبدأ بـ 🔴 سالب و $\\frac1a$، ومعه $|u|$.',
        '<b>رجّع $x$، وحط $+C$.</b>'], tricks_=[
        ('$u$ برّا الجذر يعني الجواب يبدأ بسالب و $\\frac1a$، ومعه $|u|$. مثال: '
         '$\\int\\frac{du}{u\\sqrt{u^2+4}}=-\\frac12\\operatorname{csch}^{-1}\\frac{|u|}{2}$.',
         [('diff(-acsch(Abs(x)/2)/2,x)', '1/(x*sqrt(x**2+4))', 't'), ('diff(-acsch(Abs(x)/2)/2,x)', '1/(x*sqrt(x**2+4))', '-t')]),
        ('رقم التعديل: بعد الضرب في $x$، البسط $x\\,dx$ و $du=2x\\,dx$ (مع $u=x^2$)، فالبسط $=\\frac12du$.', [('diff(x**2,x)/2', 'x')])],
        label='U-I3'))
    it = ITEMS['N42-E2-5']
    ex = question(it, 'U-I3 example')
    ex += steps(it, [
        ('tex', r'16-x^{4}=4^{2}-\left(\cU{x^{2}}\right)^{2}', [('16-x**4', '4**2-(x**2)**2')],
         'نكتب اللي تحت الجذر كمربعين: $x^4=(x^2)^2$، و $16=4^2$. فنبي 🔵 $u=x^2$.'),
        ('tex', r'\frac{1}{x\sqrt{16-x^{4}}}\cdot\frac{x}{x}=\frac{x}{\cU{x^{2}}\sqrt{16-x^{4}}}', [('1/(x*sqrt(16-x**4))*x/x', 'x/(x**2*sqrt(16-x**4))')],
         'برّا الجذر $x$ بس، ونبيه $x^2$ عشان يصير $u$. نضرب فوق وتحت في $x$، والضرب في $\\frac xx=1$ ما يغيّر القيمة.'),
        ('sub', 'x**2', '2*x', 'نسمّي 🔵 $u=x^2$. مشتقته $2x$.'),
        ('tex', r'x\,dx=\frac{\cD{du}}{\cA{2}}', [('diff(x**2,x)/2', 'x')], 'هنا التريك، 🟠 رقم التعديل: $du$ فيه 2 والبسط ما فيه، فنقسم على 2.'),
        ('tex', r'\int\frac{x\,dx}{x^{2}\sqrt{16-x^{4}}}=\cA{\frac12}\int\frac{\cD{du}}{\cU{u}\sqrt{4^{2}-\cU{u}^{2}}}',
         [('x/(x**2*sqrt(16-x**4))', 'Rational(1,2)*diff(x**2,x)/(x**2*sqrt(4**2-(x**2)**2))')],
         'نعوّض: البسط 🟢 $\\frac{du}{2}$، و $x^2$ برّا الجذر يصير 🔵 $u$.'),
        ('tex', r'=\cA{\frac12}\cdot\left(\cR{-}\frac14\right)\operatorname{sech}^{-1}\frac{|\cU{u}|}{4}', [('diff(-asech(Abs(x)/4)/4,x)', '1/(x*sqrt(16-x**2))', '4*t/(1+t)')],
         'تحت الجذر رقم ناقص مربع، و $u$ برّا. القانون: $\\int\\frac{du}{u\\sqrt{a^2-u^2}}=-\\frac1a\\operatorname{sech}^{-1}\\frac{|u|}{a}$، وهنا $a=4$. وفيه 🔴 سالب.'),
        ('tex', r'\frac12\cdot\left(-\frac14\right)=\cR{-}\frac18', [('Rational(1,2)*(-Rational(1,4))', '-Rational(1,8)')],
         'نضرب الكسرين: موجب في سالب = سالب.'),
        ('tex', r'|u|=\left|x^{2}\right|=x^{2}', [('Abs(x**2)', 'x**2')], '$x^2$ موجب دايم، فما نحتاج القيمة المطلقة.'),
        ('line', '-asech(x**2/4)/8', 'نرجع $u=x^2$.')], 'U-I3 ex')
    ex += final(it, 'U-I3 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('إذا $u$ ممكن يكون سالب (مثل $x^3$)، اكتب $|u|$. مفتاح 1445 نساها، فصار جوابه صحيح بس لما $x>0$.'),
                                rich('نضرب في القوة اللي تخلي اللي برّا الجذر يصير $u$. مع $x^6$ نبي $u=x^3$، فنضرب في $x^2$.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\frac{1}{x\sqrt{16-x^{4}}}=\frac{x}{\cU{x^{2}}\sqrt{4^{2}-(\cU{x^{2}})^{2}}}', [('1/(x*sqrt(16-x**4))', 'x/(x**2*sqrt(4**2-(x**2)**2))')], 'U-I3 paper 1'))
          + md(arith(r'\cU{u=x^{2}}\qquad \cD{du=2x\,dx}', [('diff(x**2,x)', '2*x')], 'U-I3 paper 2'))
          + md(arith(r'\int\frac{dx}{x\sqrt{16-x^{4}}}=\cA{\frac12}\int\frac{\cD{du}}{\cU{u}\sqrt{4^{2}-\cU{u}^{2}}}=\cR{-}\frac18\operatorname{sech}^{-1}\frac{x^{2}}{4}+C',
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
        'مشتقة الأسية مو موجودة فوق، فما فيه تعويض مباشر. '
        'والضرب فوق وتحت في نفس الشي ما يغيّر القيمة، بس يطلّع الأسية برّا الجذر، فيصير بشكل قانون $\\operatorname{csch}^{-1}$ أو $\\operatorname{sech}^{-1}$.')))
    U.add('sign', 'العلامة', p(rich('<b>إذا شفت:</b> أسية تحت الجذر زائد أو ناقص رقم، مثل $\\sqrt{e^{6x}+1}$، وفوق رقم بس.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> مشتقة الأسية موجودة فوق (مثل $\\frac{e^{3x}}{\\sqrt{e^{6x}+1}}$): تعويض $u=e^{3x}$ على طول، بدون ضرب. '
                   'أو أسية ناقص رقم ($\\sqrt{e^{2x}-1}$): نفس الضرب، بس الجواب $\\sec^{-1}$ من 3.4.'))
          + contrast([(r'\int\frac{dx}{\sqrt{e^{6x}+1}}', 'تجهيز: اضرب فوق وتحت في $e^{3x}$، ثم $u=e^{3x}$', 'البسط رقم، ومشتقة الأسية مو فوق'),
                      (r'\int\frac{e^{3x}\,dx}{\sqrt{e^{6x}+1}}', 'تعويض على طول: $u=e^{3x}$، قانون $\\sinh^{-1}$', 'مشتقة الأسية فوق'),
                      (r'\int\frac{dx}{\sqrt{e^{2x}-1}}', '$\\sec^{-1}$ (درس 3.4)', 'أسية ناقص رقم، وقانونها مو من جدول 4.2')]))
    formula('1/(u*sqrt(u**2+a**2))', '-acsch(Abs(u)/a)/a', pos=('a',), label='U-I4 law csch')
    formula('1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='U-I4 law sech')
    laws = (md(r'\int\frac{du}{u\sqrt{u^{2}+a^{2}}}=-\frac1a\operatorname{csch}^{-1}\frac{|u|}{a}+C')
            + md(r'\int\frac{du}{u\sqrt{a^{2}-u^{2}}}=-\frac1a\operatorname{sech}^{-1}\frac{|u|}{a}+C'))
    arith('', [('exp(6*0)', 'exp(3*0)**2'), ('exp(6*0)', '1')], 'U-I4 number check')
    U.add('short', '🧭 الطريقة', method([
        '<b>وش الشكل اللي يدلك؟</b> أسية تحت الجذر، وفوق رقم بس.',
        '<b>سوّ الحركة:</b> نكتب الأسية كمربع ($e^{6x}=(e^{3x})^2$)، ونضرب فوق وتحت في جذرها $e^{3x}$. فيطلع برّا الجذر.',
        '<b>تأكد برقم إن الشكل الجديد يساوي القديم:</b> الضرب في $\\frac{e^{3x}}{e^{3x}}=1$ ما يغيّر شي. '
        'وعند $x=0$: $e^{6\\cdot0}=1$، و $(e^{0})^2=1$ ✓.',
        '<b>ارجع للشجرة: الحين وش الطريقة؟</b> صارت تعويض: 🔵 $u=e^{3x}$، و 🟢 $du=3e^{3x}dx$، و 🟠 رقم التعديل $\\frac13$. '
        'زائد تحت الجذر يعني $\\operatorname{csch}^{-1}$، وناقص يعني $\\operatorname{sech}^{-1}$.'],
        tricks_=[('أسية تحت الجذر: نضرب فوق وتحت في جذرها. $e^{6x}=(e^{3x})^2$، فنضرب في $e^{3x}$.', [('exp(6*x)', 'exp(3*x)**2')]),
                 ('رقم التعديل: $du=3e^{3x}dx$ والبسط $e^{3x}dx$ بس. فالبسط $=\\frac13du$، ونطلّع $\\frac13$ برّا التكامل.',
                  [('diff(exp(3*x),x)/3', 'exp(3*x)')])], label='U-I4') + laws)
    it = ITEMS['1446-S2-SE-Q2.7']
    ex = question(it, 'U-I4 example')
    ex += steps(it, [
        ('tex', r'e^{6x}=\left(\cU{e^{3x}}\right)^{2}', [('exp(6*x)', 'exp(3*x)**2')],
         'البسط رقم، ومشتقة الأسية مو فوق. فنجهّزها: نكتب الأسية كمربع، ونص 6 هو 3.'),
        ('tex', r'\frac{1}{\sqrt{e^{6x}+1}}=\frac{e^{3x}}{\cU{e^{3x}}\sqrt{\left(\cU{e^{3x}}\right)^{2}+1}}',
         [('1/sqrt(exp(6*x)+1)', 'exp(3*x)/(exp(3*x)*sqrt(exp(3*x)**2+1))')],
         'هنا التريك: نضرب فوق وتحت في $e^{3x}$، فما تتغير القيمة. وصار $e^{3x}$ برّا الجذر.'),
        ('sub', 'exp(3*x)', '3*exp(3*x)', 'نسمّي 🔵 $u=e^{3x}$، لأنه برّا الجذر وداخله. ومشتقته $3e^{3x}$.'),
        ('tex', r'e^{3x}\,dx=\frac{\cD{du}}{\cA{3}}', [('diff(exp(3*x),x)/3', 'exp(3*x)')],
         'فوق عندنا $e^{3x}dx$ بدون 3. فـ 🟠 رقم التعديل $\\frac13$.'),
        ('tex', r'\int\frac{e^{3x}\,dx}{e^{3x}\sqrt{\left(e^{3x}\right)^{2}+1}}=\cA{\frac13}\int\frac{\cD{du}}{\cU{u}\sqrt{\cU{u}^{2}+1^{2}}}',
         [('exp(3*x)/(exp(3*x)*sqrt(exp(3*x)**2+1))', 'Rational(1,3)*diff(exp(3*x),x)/(exp(3*x)*sqrt(exp(3*x)**2+1**2))')],
         'نعوّض. صار بنفس شكل القانون، و 🟠 $\\frac13$ قدّام التكامل.'),
        ('tex', r'=\cR{-}\cA{\frac13}\operatorname{csch}^{-1}\cU{u}', [('diff(-acsch(x)/3,x)', '1/(3*x*sqrt(x**2+1))', 't')],
         'القانون: $\\int\\frac{du}{u\\sqrt{u^2+a^2}}=-\\frac1a\\operatorname{csch}^{-1}\\frac{|u|}{a}$، وهنا $a=1$. و $u=e^{3x}$ موجب، فـ $|u|=u$.'),
        ('line', '-acsch(exp(3*x))/3', 'نرجع $u=e^{3x}$.')], 'U-I4 ex')
    ex += final(it, 'U-I4 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('إذا مشتقة الأسية موجودة فوق، مثل $\\frac{e^{x}}{\\sqrt{e^{2x}+1}}$، لا تضرب في شي. هذا تعويض على طول: $u=e^x$.'),
                                rich('مع أساس غير $e$ مثل $5^x$: مشتقته $5^x\\ln5$. فيطلع $\\ln5$ تحت في الجواب.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\frac{1}{\sqrt{e^{6x}+1}}=\frac{e^{3x}}{\cU{e^{3x}}\sqrt{\left(\cU{e^{3x}}\right)^{2}+1}}',
                   [('1/sqrt(exp(6*x)+1)', 'exp(3*x)/(exp(3*x)*sqrt(exp(3*x)**2+1))')], 'U-I4 paper 1'))
          + md(arith(r'\cU{u=e^{3x}}\qquad \cD{du=3e^{3x}\,dx}', [('diff(exp(3*x),x)', '3*exp(3*x)')], 'U-I4 paper 2'))
          + md(arith(r'\cA{\frac13}\int\frac{\cD{du}}{\cU{u}\sqrt{\cU{u}^{2}+1}}=\cR{-}\frac13\operatorname{csch}^{-1}e^{3x}+C',
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
        'مشتقة $\\sqrt x$ هي $\\frac{1}{2\\sqrt x}$، وهي موجودة في السؤال إلا الرقم 2. '
        'ولما 🔵 $u=\\sqrt x$ يصير $x=u^2$، فالجذر الثاني يصير مربع زائد أو ناقص رقم، بشكل القانون.')))
    U.add('sign', 'العلامة', p(rich('<b>إذا شفت:</b> $\\sqrt x$ في المقام، ومعها جذر ثاني فيه $x$ لحالها (مو $x^2$)، مثل $\\sqrt{x}\\sqrt{4+x}$.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> تحت الجذر $x^2$ (مثل $\\sqrt{4+x^2}$): تعويض عادي $u=x$ بقانون $\\sinh^{-1}$. '
                   'أو ما فيه $\\sqrt x$ برّا (مثل $\\frac{1}{\\sqrt{4+x}}$): قاعدة القوة، والجواب $2\\sqrt{4+x}$.'))
          + contrast([(r'\int\frac{dx}{\sqrt{x}\sqrt{4+x}}', 'تعويض: $u=\\sqrt x$، و $\\frac{dx}{\\sqrt x}=2\\,du$', 'تحت الجذر الثاني $x$ لحالها'),
                      (r'\int\frac{dx}{\sqrt{4+x^{2}}}', 'تعويض: $u=x$ و $a=2$، قانون $\\sinh^{-1}$', 'تحت الجذر $x^2$، فهو مربع جاهز'),
                      (r'\int\frac{dx}{\sqrt{4+x}}', 'قاعدة القوة: $2\\sqrt{4+x}$', 'ما فيه $\\sqrt x$ برّا')]))
    formula('1/sqrt(u**2+a**2)', 'asinh(u/a)', pos=('a',), label='U-I5 law sinh')
    formula('1/sqrt(u**2-a**2)', 'acosh(u/a)', branches=('a+t',), pos=('a',), label='U-I5 law cosh')
    laws = (md(r'\int\frac{du}{\sqrt{u^{2}+a^{2}}}=\sinh^{-1}\frac{u}{a}+C') + md(r'\int\frac{du}{\sqrt{u^{2}-a^{2}}}=\cosh^{-1}\frac{u}{a}+C'))
    U.add('short', '🧭 الطريقة', method([
        '<b>🔵 سمّ الداخل $u$:</b> هنا $u=\\sqrt x$.',
        '<b>🟢 اشتقه: $du=\\ldots\\,dx$.</b> $du=\\frac{dx}{2\\sqrt x}$.',
        '<b>🟠 اقسم اللي برّا على مشتقة الداخل: طلع رقم؟ هذا رقم التعديل، يطلع قدّام التكامل مرة وحدة بس.</b> '
        'فوق $\\frac{1}{\\sqrt x}$، ومشتقة الداخل $\\frac{1}{2\\sqrt x}$. القسمة تعطي 2، يعني $\\frac{dx}{\\sqrt x}=2\\,du$.',
        '<b>اكتب التكامل كله بـ $u$، وطبّق القانون:</b> $x=u^2$ في الجذر الثاني، لأن $\\sqrt x\\cdot\\sqrt x=x$. '
        'زائد يعني $\\sinh^{-1}$، وناقص يعني $\\cosh^{-1}$.',
        '<b>رجّع $x$، وحط $+C$.</b> $u=\\sqrt x$.'],
        tricks_=[('$\\sqrt x$ ومعها $\\frac{1}{\\sqrt x}$؟ يعني $u=\\sqrt x$، و $\\frac{dx}{\\sqrt x}=2\\,du$.', [('2*diff(sqrt(x),x)', '1/sqrt(x)')]),
                 ('نكتب الرقم كمربع عشان نعرف $a$: $4+x=2^2+u^2$، يعني $a=2$.', [('2**2+sqrt(x)**2', '4+x')])], label='U-I5') + laws)
    it = ITEMS['N42-E2-4']
    ex = question(it, 'U-I5 example')
    ex += steps(it, [
        ('sub', 'sqrt(x)', '1/(2*sqrt(x))', 'في المقام $\\sqrt x$ وتحت الجذر الثاني $x$ لحالها. فنسمّي 🔵 $u=\\sqrt x$.'),
        ('tex', r'\frac{dx}{\sqrt{x}}=\cA{2}\,\cD{du}', [('2*diff(sqrt(x),x)', '1/sqrt(x)')],
         'هنا التريك: نضرب الطرفين في 2، عشان يطلع $\\frac{dx}{\\sqrt x}$ اللي في السؤال. فـ 🟠 رقم التعديل 2.'),
        ('tex', r'x=\sqrt{x}\cdot\sqrt{x}=\cU{u}^{2}', [('sqrt(x)*sqrt(x)', 'x')], 'الجذر في نفسه يعطي اللي تحته. فـ $x=u^2$.'),
        ('tex', r'4+x=2^{2}+\cU{u}^{2}', [('2**2+sqrt(x)**2', '4+x')], 'نعوّض $x=u^2$، ونكتب 4 كمربع: $4=2^2$.'),
        ('tex', r'\int\frac{dx}{\sqrt{x}\sqrt{4+x}}=\cA{2}\int\frac{\cD{du}}{\sqrt{\cU{u}^{2}+2^{2}}}',
         [('1/(sqrt(x)*sqrt(4+x))', '2*diff(sqrt(x),x)/sqrt(sqrt(x)**2+2**2)')], 'نعوّض. صار بنفس شكل القانون، و 🟠 الـ 2 قدّام التكامل.'),
        ('line', '2*asinh(sqrt(x)/2)', 'القانون: $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$، وهنا $a=2$. ثم نرجع $u=\\sqrt x$.')], 'U-I5 ex')
    ex += final(it, 'U-I5 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تنسى الـ 2: $\\frac{dx}{\\sqrt x}=2\\,du$، مو $du$.'),
                                rich('داخل الدالة العكسية $\\sqrt x$، مو $x$: الجواب $2\\sinh^{-1}\\frac{\\sqrt x}{2}$.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\cU{u=\sqrt{x}}\qquad \cD{du=\frac{dx}{2\sqrt{x}}}\qquad \frac{dx}{\sqrt{x}}=\cA{2}\,\cD{du}', [('2*diff(sqrt(x),x)', '1/sqrt(x)')], 'U-I5 paper 1'))
          + md(arith(r'4+x=2^{2}+\cU{u}^{2}', [('2**2+sqrt(x)**2', '4+x')], 'U-I5 paper 2'))
          + md(arith(r'\cA{2}\int\frac{\cD{du}}{\sqrt{\cU{u}^{2}+2^{2}}}=2\sinh^{-1}\frac{\sqrt{x}}{2}+C',
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
                       'نعوّض: $\\sqrt x=u$، و $1+x=1+u^2$. صار $u$ برّا الجذر، بشكل قانون $\\operatorname{csch}^{-1}$.'),
                      ('line', '-2*acsch(sqrt(x))',
                       'القانون: $\\int\\frac{du}{u\\sqrt{u^2+a^2}}=-\\frac1a\\operatorname{csch}^{-1}\\frac{|u|}{a}$، و $a=1$. و $u=\\sqrt x$ موجب.')])
    return U


# ---------------------------------------------------------------- 8
def u_split():
    U = Unit('U-I6', 'بسط مركّب: افصل الكسر', '4.2', 'ص62، تمرينا 7 و8', 2)
    U.add('idea', 'الفكرة', p(rich(
        'كل حد فوق يحتاج طريقة مختلفة: حد $x$ يحتاج تعويض $w$، والرقم يحتاج قانون. '
        'وكسر بحدّين فوق يساوي مجموع كسرين لهم نفس المقام، فنفصل ونحل كل كسر لحاله.')))
    U.add('sign', 'العلامة', p(rich('<b>إذا شفت:</b> فوق $x$ ورقم مع بعض، مثل $x-2$، وتحت من أشكال جدول 4.2 '
                                    '(جذر فيه مربع ± رقم، أو رقم ناقص مربع بدون جذر).'))
          + p(rich('<b>مو هذي الحالة إذا:</b> فوق هو مشتقة اللي تحت الجذر أو نصها (مثل $\\frac{x+1}{\\sqrt{x^2+2x+10}}$): '
                   'تعويض واحد $w$ = اللي تحت الجذر، بدون فصل. أو فوق رقم بس: تعويض بالقانون على طول.'))
          + contrast([(r'\int\frac{x-2}{\sqrt{25+x^{2}}}dx', 'تجهيز: افصل لكسرين، ثم كل كسر لحاله', 'البسط فيه $x$ ورقم'),
                      (r'\int\frac{x+3}{\sqrt{x^{2}+6x+10}}dx', 'تعويض واحد: $w=x^2+6x+10$', 'البسط نص مشتقة اللي تحت الجذر، فما نفصل'),
                      (r'\int\frac{3\,dx}{\sqrt{25+x^{2}}}', 'تعويض: $u=x$ و $a=5$، قانون $\\sinh^{-1}$', 'البسط رقم بس')]))
    formula('1/sqrt(u)', '2*sqrt(u)', branches=('t',), label='U-I6 law power')
    formula('1/sqrt(u**2+a**2)', 'asinh(u/a)', pos=('a',), label='U-I6 law sinh')
    laws = (md(r'\int w^{-1/2}\,dw=\frac{w^{1/2}}{1/2}=2\sqrt{w}+C') + md(r'\int\frac{du}{\sqrt{u^{2}+a^{2}}}=\sinh^{-1}\frac{u}{a}+C'))
    arith('', [('(0-2)/sqrt(25+0**2)', '0/sqrt(25+0**2)-2/sqrt(25+0**2)'), ('(0-2)/sqrt(25)', '-Rational(2,5)')], 'U-I6 number check')
    U.add('short', '🧭 الطريقة', method([
        '<b>وش الشكل اللي يدلك؟</b> فوق حدّين: $x$ ورقم. ونتأكد أول إنه مو مشتقة اللي تحت (أو نصها). إذا هو، تعويض واحد وما نفصل.',
        '<b>سوّ الحركة:</b> نفصل الكسر: كل حد فوق على نفس المقام، ومعه إشارته.',
        '<b>تأكد برقم إن الشكل الجديد يساوي القديم:</b> عند $x=0$: $\\frac{0-2}{5}=-\\frac25$، و $\\frac05-\\frac25=-\\frac25$ ✓.',
        '<b>ارجع للشجرة: الحين وش الطريقة؟</b> كسر $x$: تعويض 🔵 $w$ = اللي تحت الجذر، والجواب جذر (أو $\\ln$ إذا ما فيه جذر). '
        'وكسر الرقم: تعويض بقانون $\\sinh^{-1}$ أو $\\cosh^{-1}$ أو $\\tanh^{-1}$. ونجمع بنفس الإشارة.'],
        tricks_=[('بسط فيه جمع؟ نفصل لكسرين، وكل واحد نوع لحاله: $\\frac{x-2}{\\sqrt{25+x^2}}=\\frac{x}{\\sqrt{25+x^2}}-\\frac{2}{\\sqrt{25+x^2}}$.',
                  [('(x-2)/sqrt(25+x**2)', 'x/sqrt(25+x**2)-2/sqrt(25+x**2)')])], label='U-I6') + laws)
    it = ITEMS['N42-X2-07']
    ex = question(it, 'U-I6 example')
    ex += steps(it, [
        ('tex', r'\frac{x-2}{\sqrt{25+x^{2}}}=\frac{x}{\sqrt{25+x^{2}}}\cR{-}\frac{2}{\sqrt{25+x^{2}}}',
         [('(x-2)/sqrt(25+x**2)', 'x/sqrt(25+x**2)-2/sqrt(25+x**2)')],
         'مشتقة $25+x^2$ هي $2x$، والبسط فيه $-2$ زيادة. هنا التريك: نفصل الكسر، وكل حد ومعه إشارته (🔴 السالب يروح مع 2).'),
        ('sub', '25+x**2', '2*x', 'الكسر الأول: نسمّي 🔵 $w$ = اللي تحت الجذر. مشتقته $2x$، و $x$ موجودة فوق.', 'w'),
        ('tex', r'x\,dx=\frac{\cD{dw}}{\cA{2}}', [('diff(25+x**2,x)/2', 'x')], 'فوق عندنا $x\\,dx$ بدون 2. فـ 🟠 رقم التعديل $\\frac12$.'),
        ('tex', r'\int\frac{x\,dx}{\sqrt{25+x^{2}}}=\cA{\frac12}\int \cU{w}^{-1/2}\,\cD{dw}',
         [('x/sqrt(25+x**2)', 'Rational(1,2)*diff(25+x**2,x)*(25+x**2)**Rational(-1,2)')],
         'نعوّض، ونكتب الجذر تحت كأس سالب: $\\frac{1}{\\sqrt w}=w^{-1/2}$.'),
        ('tex', r'=\cA{\frac12}\cdot2\sqrt{\cU{w}}=\sqrt{25+x^{2}}', [('diff(sqrt(25+x**2),x)', 'x/sqrt(25+x**2)')],
         'قاعدة القوة: $\\int w^{-1/2}dw=2\\sqrt w$. ثم نرجع $w=25+x^2$.'),
        ('tex', r'\int\frac{2\,dx}{\sqrt{x^{2}+5^{2}}}=2\sinh^{-1}\frac{x}{5}', [('diff(2*asinh(x/5),x)', '2/sqrt(x**2+25)')],
         'الكسر الثاني: الرقم 2 برّا. والقانون $\\int\\frac{du}{\\sqrt{u^2+a^2}}=\\sinh^{-1}\\frac ua$ مع $u=x$ و $a=5$.'),
        ('line', 'sqrt(25+x**2)-2*asinh(x/5)', 'نطرح الجزأين، بنفس الإشارة اللي في الفصل.')], 'U-I6 ex')
    ex += final(it, 'U-I6 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('انتبه للإشارة: $\\frac{x-2}{\\ldots}=\\frac{x}{\\ldots}-\\frac{2}{\\ldots}$. السالب يروح مع الرقم.'),
                                rich('كسر $x$ مو قانون $\\sinh^{-1}$. جوابه جذر، أو $\\ln$ إذا ما فيه جذر.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\int\frac{x-2}{\sqrt{25+x^{2}}}dx=\int\frac{x\,dx}{\sqrt{25+x^{2}}}\cR{-}\int\frac{2\,dx}{\sqrt{25+x^{2}}}',
                   [('(x-2)/sqrt(25+x**2)', 'x/sqrt(25+x**2)-2/sqrt(25+x**2)')], 'U-I6 paper 1'))
          + md(arith(r'\cU{w=25+x^{2}}\qquad \cD{dw=2x\,dx}', [('diff(25+x**2,x)', '2*x')], 'U-I6 paper 2'))
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
        'مشتقة الدالة العكسية موجودة جنبها في السؤال. '
        'فلما 🔵 $u$ = الدالة العكسية، يصير الباقي مع $dx$ هو 🟢 $du$ بالضبط، ويبقى تكامل سهل: $\\int u\\,du$.')))
    U.add('sign', 'العلامة', p(rich('<b>إذا شفت:</b> دالة عكسية (مثل $\\cosh^{-1}x$ أو $\\tan^{-1}x$)، ومعها مشتقتها مضروبة فيها، '
                                    'مثل $\\frac{\\cosh^{-1}x}{\\sqrt{x^2-1}}$.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> الدالة العكسية لحالها بدون مشتقتها (مثل $\\int\\sinh^{-1}2x\\,dx$)، '
                   'أو مضروبة في $x$ (مثل $x\\tan^{-1}x$): هذا تجزئة.'))
          + contrast([(r'\int\frac{\cosh^{-1}x}{\sqrt{x^{2}-1}}dx', 'تعويض: $u=\\cosh^{-1}x$، والجواب $\\frac{u^2}{2}$', 'مشتقة $\\cosh^{-1}x$ هي $\\frac{1}{\\sqrt{x^2-1}}$، وموجودة في السؤال'),
                      (r'\int\sinh^{-1}(2x)\,dx', 'تجزئة: $u=\\sinh^{-1}2x$ و $dv=dx$', 'الدالة لحالها، بلا مشتقتها'),
                      (r'\int x\tan^{-1}x\,dx', 'تجزئة: $u=\\tan^{-1}x$ و $dv=x\\,dx$', '$x$ مو مشتقة $\\tan^{-1}x$')]))
    laws = (md(arith(r'\frac{d}{dx}\sinh^{-1}x=\frac{1}{\sqrt{x^{2}+1}}\qquad \frac{d}{dx}\cosh^{-1}x=\frac{1}{\sqrt{x^{2}-1}}\qquad \frac{d}{dx}\tanh^{-1}x=\frac{1}{1-x^{2}}',
                     [('diff(asinh(x),x)', '1/sqrt(x**2+1)'), ('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t'), ('diff(atanh(x),x)', '1/(1-x**2)')], 'U-I7 law derivatives'))
            + md(arith(r'\int u\,du=\frac{u^{2}}{2}+C', [('integrate(x,x)', 'x**2/2')], 'U-I7 law power')))
    U.add('short', '🧭 الطريقة', method([
        '<b>🔵 سمّ الداخل $u$:</b> هنا $u$ = الدالة العكسية نفسها، مثل $u=\\cosh^{-1}x$.',
        '<b>🟢 اشتقه: $du=\\ldots\\,dx$.</b> من جدول مشتقات الدوال العكسية: $du=\\frac{dx}{\\sqrt{x^2-1}}$.',
        '<b>🟠 اقسم اللي برّا على مشتقة الداخل: طلع رقم؟ هذا رقم التعديل، يطلع قدّام التكامل مرة وحدة بس.</b> '
        'اللي برّا $\\frac{1}{\\sqrt{x^2-1}}$ هو المشتقة نفسها، فالرقم 1.',
        '<b>اكتب التكامل كله بـ $u$، وطبّق القانون:</b> $\\int u\\,du=\\frac{u^2}{2}$.',
        '<b>رجّع $x$، وحط $+C$.</b>'],
        tricks_=[('الدالة العكسية ومشتقتها مضروبتين؟ $u$ = الدالة، والجواب $\\frac{u^2}{2}$. مع $\\cosh^{-1}x$ يطلع $\\frac{(\\cosh^{-1}x)^2}{2}$.',
                  [('diff(acosh(x)**2/2,x)', 'acosh(x)/sqrt(x**2-1)', '1+t')])], label='U-I7') + laws)
    it = ITEMS['N42-X2-09']
    ex = question(it, 'U-I7 example')
    ex += steps(it, [
        ('tex', r'\frac{\cosh^{-1}x}{\sqrt{x^{2}-1}}=\cU{\cosh^{-1}x}\cdot\cD{\frac{1}{\sqrt{x^{2}-1}}}', [('acosh(x)/sqrt(x**2-1)', 'acosh(x)*1/sqrt(x**2-1)')],
         'نكتب الكسر كضرب، عشان نشوف الدالة العكسية ومعها كسر ثاني.'),
        ('tex', r'\frac{d}{dx}\cU{\cosh^{-1}x}=\cD{\frac{1}{\sqrt{x^{2}-1}}}', [('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t')],
         'الكسر الثاني هو نفسه مشتقة $\\cosh^{-1}x$، من جدول مشتقات الدوال العكسية.'),
        ('sub', 'acosh(x)', '1/sqrt(x**2-1)', 'هنا التريك: نسمّي 🔵 $u$ = الدالة العكسية. ومشتقتها مع $dx$ صارت 🟢 $du$.', 'u', '1+t'),
        ('tex', r'\int\cU{\cosh^{-1}x}\cdot\cD{\frac{dx}{\sqrt{x^{2}-1}}}=\int\cU{u}\,\cD{du}', [('acosh(x)/sqrt(x**2-1)', 'acosh(x)*diff(acosh(x),x)', '1+t')],
         'نعوّض. اللي برّا هو المشتقة نفسها، فما فيه رقم تعديل. بقي تكامل سهل.'),
        ('tex', r'=\frac{\cU{u}^{2}}{2}', [('integrate(x,x)', 'x**2/2')], 'قاعدة القوة: نزيد الأس واحد، ونقسم على الأس الجديد.'),
        ('line', 'acosh(x)**2/2', 'نرجع $u=\\cosh^{-1}x$.')], 'U-I7 ex')
    ex += final(it, 'U-I7 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('$(\\cosh^{-1}x)^2$ يعني مربع الدالة كلها، مو $\\cosh^{-1}(x^2)$.'),
                                rich('إذا الدالة العكسية في المقام، مثل $\\frac{1}{\\sqrt{x^2-1}\\,\\cosh^{-1}x}$، يصير $\\int\\frac{du}{u}=\\ln|u|$، مو $\\frac{u^2}{2}$.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\cU{u=\cosh^{-1}x}\qquad \cD{du=\frac{dx}{\sqrt{x^{2}-1}}}', [('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t')], 'U-I7 paper 1'))
          + md(arith(r'\int\cU{u}\,\cD{du}=\frac{\cU{u}^{2}}{2}=\frac{\left(\cosh^{-1}x\right)^{2}}{2}+C',
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
    U.drill('4', 'M-14', 'I', 'تجهيز أول: افصل الكسر. والجزء الثاني فيه $\\tan^{-1}x$ ومشتقتها.',
            sol_rows=[('tex', r'\frac{x+\tan^{-1}x}{1+x^{2}}=\frac{x}{1+x^{2}}+\frac{\tan^{-1}x}{1+x^{2}}',
                       [('(x+atan(x))/(1+x**2)', 'x/(1+x**2)+atan(x)/(1+x**2)')], 'البسط فيه حدّين، فنفصل الكسر (تجهيز: افصل الكسر).'),
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
        'القوانين تبي مربع واحد زائد أو ناقص رقم، وتحت الجذر عندنا حد $x$ زيادة. '
        'إكمال المربع يجمع $x^2$ و $x$ في قوس واحد مربع، فيصير بشكل القانون، والقوس هو 🔵 $u$.')))
    U.add('sign', 'العلامة', p(rich('<b>إذا شفت:</b> تحت الجذر $x^2$ و $x$ ورقم (مثل $x^2+6x-16$)، وما فيه شي مضروب برّا الجذر.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> فيه قوس مضروب برّا الجذر (مثل $(x-1)\\sqrt{x^2-2x+10}$): نفس التجهيز، '
                   'بس القانون $\\operatorname{csch}^{-1}$ أو $\\operatorname{sech}^{-1}$. أو ما فيه حد $x$ تحت الجذر ($x^2+9$): تعويض بالقانون على طول. '
                   'أو معامل $x^2$ سالب ($-x^2+4x$): نفس الحركة، بس الجواب $\\sin^{-1}$ من 3.4.'))
          + contrast([(r'\int\frac{dx}{\sqrt{x^{2}+6x+13}}', 'تجهيز: كمّل المربع، ثم $u=x+3$ و $\\sinh^{-1}$', 'تحت الجذر فيه حد $x$'),
                      (r'\int\frac{dx}{(x-1)\sqrt{x^{2}-2x+10}}', 'تجهيز: كمّل المربع، ثم $u=x-1$ و $\\operatorname{csch}^{-1}$', 'فيه قوس مضروب برّا الجذر'),
                      (r'\int\frac{dx}{\sqrt{x^{2}+9}}', 'تعويض على طول: $u=x$ و $a=3$', 'مربع جاهز، ما يحتاج إكمال'),
                      (r'\int\frac{dx}{\sqrt{-x^{2}+4x}}', 'تجهيز: كمّل المربع، ثم $\\sin^{-1}\\frac{x-2}{2}$ (درس 3.4)', 'معامل $x^2$ سالب')]))
    laws = (md(r'\int\frac{du}{\sqrt{u^{2}+a^{2}}}=\sinh^{-1}\frac{u}{a}+C') + md(r'\int\frac{du}{\sqrt{u^{2}-a^{2}}}=\cosh^{-1}\frac{u}{a}+C'))
    arith('', [('0**2+6*0-16', '(0+3)**2-25'), ('0**2+6*0-16', '-16')], 'U-I8 number check')
    U.add('short', '🧭 الطريقة', method([
        '<b>وش الشكل اللي يدلك؟</b> تحت الجذر $x^2$ و $x$ ورقم.',
        '<b>سوّ الحركة:</b> نكمّل المربع: نص معامل $x$، ومربعه نضيفه ونطرحه. فيصير (قوس)² زائد أو ناقص رقم.',
        '<b>تأكد برقم إن الشكل الجديد يساوي القديم:</b> عوّض $x=0$ في الاثنين. $0+0-16=-16$، و $(0+3)^2-25=9-25=-16$ ✓.',
        '<b>ارجع للشجرة: الحين وش الطريقة؟</b> تعويض: 🔵 $u$ = القوس، و 🟢 $du=dx$. '
        '(قوس)² + رقم يعني $\\sinh^{-1}$، و(قوس)² − رقم يعني $\\cosh^{-1}$.'],
        tricks_=[('<b>نص معامل $x$:</b> في $x^2+6x$ نص 6 هو 3، ومربعه 9. فـ $x^2+6x+9=(x+3)^2$. والقوس فيه نفس إشارة معامل $x$: '
                  '$x^2-4x+4=(x-2)^2$.', [('x**2+6*x+9', '(x+3)**2'), ('x**2-4*x+4', '(x-2)**2')])], label='U-I8') + laws)
    it = ITEMS['1446-S1-SE-Q2.2']
    ex1_it = it
    ex = question(it, 'U-I8 example 1')
    ex += steps(it, [
        ('tex', r'x^{2}+6x-16=\left(x^{2}+6x+9\right)-9-16', [('x**2+6*x-16', 'x**2+6*x+9-9-16')],
         'تحت الجذر مو مربع جاهز، فنكمّل المربع. نص 6 هو 3، ومربعه 9. نضيف 9 ونطرحها، فما تتغير القيمة.'),
        ('tex', r'=(\cU{x+3})^{2}-25', [('x**2+6*x+9-9-16', '(x+3)**2-25')],
         'أول ثلاثة حدود مربع كامل: $(x+3)^2=x^2+6x+9$. والأرقام: $-9-16=-25$.'),
        ('tex', r'=(\cU{x+3})^{2}-5^{2}', [('(x+3)**2-25', '(x+3)**2-5**2')], 'نكتب 25 كمربع عشان نعرف $a$: هنا $a=5$.'),
        ('sub', 'x+3', '1', 'نسمّي القوس 🔵 $u$. مشتقة $x+3$ هي 1، فـ 🟢 $du=dx$.'),
        ('tex', r'\int\frac{3\,dx}{\sqrt{x^{2}+6x-16}}=3\int\frac{\cD{du}}{\sqrt{\cU{u}^{2}-5^{2}}}', [('3/sqrt((x+3)**2-5**2)', '3/sqrt(x**2+6*x-16)')],
         'نعوّض. صار بنفس شكل القانون، والرقم 3 يطلع برّا التكامل.'),
        ('tex', r'=3\cosh^{-1}\frac{\cU{u}}{5}', [('diff(3*acosh(x/5),x)', '3/sqrt(x**2-25)', '5+t')],
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
               'إذا ما فيه حد $x$ تحت الجذر (مثل $x^2+9$) ما تحتاجه: تعويض بالقانون على طول.'],
        paper='تكتب السطر اللي طلع: $x^2+6x-16=(x+3)^2-5^2$. هو نفس سطر إكمال المربع، فالمصحح يشوف نفس الشي.',
        ask='اكتب كل واحد على شكل (قوس)² + الباقي',
        tries=[('x^{2}+4x+13', r'(x+2)^{2}+9', [('x**2+4*x+13', '(x+2)**2+9')]),
               ('x^{2}-10x+16', r'(x-5)^{2}-9', [('x**2-10*x+16', '(x-5)**2-9')]),
               ('x^{2}+8x+7', r'(x+4)^{2}-9', [('x**2+8*x+7', '(x+4)**2-9')])]))
    U.add('trap', '⚠️ الفخ', ul([rich('انتبه للإشارة: $x^2-4x$ نصه $-2$، فيصير $(x-2)^2$ مو $(x+2)^2$.'),
                                rich('لو معامل $x^2$ مو 1، طلّعه من الجذر أول (التمرين 3).')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'x^{2}+6x-16=(\cU{x+3})^{2}-5^{2}', [('x**2+6*x-16', '(x+3)**2-5**2')], 'U-I8 paper 1'))
          + md(arith(r'\cU{u=x+3}\qquad \cD{du=dx}', [('diff(x+3,x)', '1')], 'U-I8 paper 2'))
          + md(arith(r'\int\frac{3\,dx}{\sqrt{x^{2}+6x-16}}=3\int\frac{\cD{du}}{\sqrt{\cU{u}^{2}-5^{2}}}=3\cosh^{-1}\frac{x+3}{5}+C',
                     [('3/sqrt((x+3)**2-5**2)', '3/sqrt(x**2+6*x-16)'), ('diff(3*acosh((x+3)/5),x)', '3/sqrt(x**2+6*x-16)', '2+t')], 'U-I8 paper 3')))
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
        'نفس إكمال المربع، بس القوس اللي يطلع هو نفسه القوس اللي برّا الجذر. '
        'فلما نسمّيه 🔵 $u$ يصير التكامل $\\int\\frac{du}{u\\sqrt{\\ldots}}$، وهذا قانون $\\operatorname{csch}^{-1}$ أو $\\operatorname{sech}^{-1}$.')))
    U.add('sign', 'العلامة', p(rich('<b>إذا شفت:</b> قوس مثل $(x+3)$ مضروب برّا جذر، وتحت الجذر $x^2$ و $x$ ورقم.'))
          + p(rich('<b>مو هذي الحالة إذا:</b> ما فيه قوس برّا الجذر: نفس التجهيز (كمّل المربع)، والقانون $\\sinh^{-1}$ أو $\\cosh^{-1}$. '
                   'أو القوس برّا مو نفس قوس المربع: هذا القانون ما ينفع.'))
          + contrast([(r'\int\frac{dx}{(x-1)\sqrt{x^{2}-2x+10}}', 'تجهيز: كمّل المربع، ثم $u=x-1$ و $\\operatorname{csch}^{-1}$', 'القوس برّا نفس قوس المربع'),
                      (r'\int\frac{dx}{\sqrt{x^{2}-2x+10}}', 'تجهيز: كمّل المربع، ثم $u=x-1$ و $\\sinh^{-1}$', 'ما فيه شي برّا الجذر')]))
    laws = (md(r'\int\frac{du}{u\sqrt{u^{2}+a^{2}}}=-\frac1a\operatorname{csch}^{-1}\frac{|u|}{a}+C')
            + md(r'\int\frac{du}{u\sqrt{a^{2}-u^{2}}}=-\frac1a\operatorname{sech}^{-1}\frac{|u|}{a}+C'))
    arith('', [('-0**2+2*0+3', '4-(0-1)**2'), ('-0**2+2*0+3', '3')], 'U-I9 number check')
    U.add('short', '🧭 الطريقة', method([
        '<b>وش الشكل اللي يدلك؟</b> قوس برّا الجذر، وتحت الجذر $x^2$ و $x$ ورقم.',
        '<b>سوّ الحركة:</b> نكمّل المربع تحت الجذر. وإذا معامل $x^2$ سالب، نطلّع 🔴 السالب من حدّي $x$ أول.',
        '<b>تأكد برقم إن الشكل الجديد يساوي القديم:</b> عوّض $x=0$: $-0+0+3=3$، و $4-(0-1)^2=4-1=3$ ✓. '
        'وتأكد إن القوس برّا الجذر هو نفس القوس اللي طلع.',
        '<b>ارجع للشجرة: الحين وش الطريقة؟</b> تعويض: 🔵 $u$ = القوس، و 🟢 $du=dx$. '
        '(قوس)² + رقم يعني $\\operatorname{csch}^{-1}$، ورقم − (قوس)² يعني $\\operatorname{sech}^{-1}$. والجواب يبدأ بـ 🔴 سالب.'],
        tricks_=['<b>$u$ برّا الجذر</b> يعني الجواب يبدأ بسالب و $\\frac1a$، ومعه $|u|$. مثال: $a=2$ يعني $-\\frac12$ قدّام الجواب.',
                 '<b>القوس برّا الجذر لازم يكون نفس القوس</b> اللي يطلع من إكمال المربع. إذا اختلف، هذا القانون ما ينفع.'], label='U-I9') + laws)
    it = ITEMS['N42-E2-8']
    ex = question(it, 'U-I9 example')
    ex += steps(it, [
        ('tex', r'-x^{2}+2x+3=\cR{-}\left(x^{2}-2x\right)+3', [('-x**2+2*x+3', '-(x**2-2*x)+3')],
         'معامل $x^2$ سالب. نطلّع 🔴 السالب من حدّي $x$ عشان نكمّل المربع داخل القوس.'),
        ('tex', r'x^{2}-2x=\left(x^{2}-2x+1\right)-1=(\cU{x-1})^{2}-1', [('x**2-2*x', '(x-1)**2-1')],
         'نكمّل المربع داخل القوس: نص $-2$ هو $-1$، ومربعه 1. نضيفه ونطرحه.'),
        ('tex', r'\cR{-}\left[(x-1)^{2}-1\right]+3=4-(\cU{x-1})^{2}=2^{2}-(\cU{x-1})^{2}', [('-((x-1)**2-1)+3', '2**2-(x-1)**2')],
         'نرجّع 🔴 السالب: يقلب الإشارتين. والأرقام: $1+3=4=2^2$.'),
        ('sub', 'x-1', '1', 'القوس برّا الجذر هو $(x-1)$، نفس القوس اللي طلع. نسمّيه 🔵 $u$، و 🟢 $du=dx$.'),
        ('tex', r'\int\frac{dx}{(x-1)\sqrt{-x^{2}+2x+3}}=\int\frac{\cD{du}}{\cU{u}\sqrt{2^{2}-\cU{u}^{2}}}',
         [('1/((x-1)*sqrt(-x**2+2*x+3))', 'diff(x-1,x)/((x-1)*sqrt(2**2-(x-1)**2))')], 'نعوّض. صار بنفس شكل القانون.'),
        ('line', '-asech(Abs(x-1)/2)/2',
         'رقم ناقص مربع، و $u$ برّا الجذر. القانون: $-\\frac1a\\operatorname{sech}^{-1}\\frac{|u|}{a}$ مع $a=2$. ثم نرجع $u=x-1$.')], 'U-I9 ex')
    ex += final(it, 'U-I9 example')
    ex += p(rich('مذكرة د. طارق كتبت الجواب بدون $|\\,|$، فصار صحيح بس لما $x>1$.'), 'small')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('short', '⚡ الطريقة السريعة: المركز والباقي', shortcut(
        it, 'U-I9 ex',
        saves='تكمّل المربع بدون ما تطلّع السالب وترجّعه. هنا معامل $x^2$ سالب، وهذا أكثر مكان تضيع فيه الإشارات.',
        origin='نفس المركز والباقي في إكمال المربع: القوس ($x$ ناقص المركز) يصير صفر عند المركز، فاللي يبقى تحت الجذر هو الباقي. '
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
               'إذا ما فيه قوس برّا الجذر، القانون $\\sinh^{-1}$ أو $\\cosh^{-1}$ (إكمال المربع بدون قوس برّا).'],
        paper='تكتب السطر اللي طلع: $-x^2+2x+3=2^2-(x-1)^2$، ثم $u=x-1$.',
        ask='اكتب كل واحد على شكل الباقي ± (قوس)²',
        tries=[('-x^{2}+4x', r'4-(x-2)^{2}', [('-x**2+4*x', '4-(x-2)**2')]),
               ('x^{2}-6x+13', r'(x-3)^{2}+4', [('x**2-6*x+13', '(x-3)**2+4')]),
               ('-x^{2}-6x', r'9-(x+3)^{2}', [('-x**2-6*x', '9-(x+3)**2')])]))
    U.add('trap', '⚠️ الفخ', ul([rich('القوس برّا الجذر لازم يكون نفس القوس داخل المربع، وإلا ما تنفع الطريقة.'),
                                rich('اكتب $|u|$ في الجواب. أغلب المفاتيح الرسمية تنساها.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'-x^{2}+2x+3=2^{2}-(\cU{x-1})^{2}', [('-x**2+2*x+3', '2**2-(x-1)**2')], 'U-I9 paper 1'))
          + md(arith(r'\cU{u=x-1}\qquad \cD{du=dx}', [('diff(x-1,x)', '1')], 'U-I9 paper 2'))
          + md(arith(r'\int\frac{\cD{du}}{\cU{u}\sqrt{2^{2}-\cU{u}^{2}}}=\cR{-}\frac12\operatorname{sech}^{-1}\frac{|x-1|}{2}+C',
                     [('diff(-asech(Abs(x-1)/2)/2,x)', '1/((x-1)*sqrt(-x**2+2*x+3))', '1+2*t/(1+t)'),
                      ('diff(-asech(Abs(x-1)/2)/2,x)', '1/((x-1)*sqrt(-x**2+2*x+3))', '1-2*t/(1+t)')], 'U-I9 paper 3')))
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

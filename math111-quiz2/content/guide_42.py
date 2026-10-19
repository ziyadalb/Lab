"""المذكرة الكاملة — الدرس 4.2: الدوال الزائدية العكسية (الأيام 1–3)."""
from booklet import sc_lamda, sc_six, sc_square, sc_twins
from booklet_engine import ITEMS, arith, formula, functional, same_value
from guide_kit import Unit, alg, contrast, final, question, rich, short_steps, steps
from html_kit import md, mi, p, table, ul
import sympy as s
from mathlib import x


def frow(z, c=None):
    return [mi(r'\displaystyle ' + z[0]), mi(r'\displaystyle ' + z[1])] + ([c] if c is not None else [])


# ---------------------------------------------------------------- 1
def u_deriv():
    U = Unit('U-D1', 'مشتقة الدالة الزائدية العكسية', '4.2', 'ص56–58', 1)
    U.add('idea', 'الفكرة', p(rich(
        'كل دالة زائدية عكسية لها مشتقة جاهزة (جدول التوائم). إذا كان داخلها شيء غير $x$ نسمّيه $u$، '
        "ونضرب المشتقة الجاهزة في مشتقة الداخل $u'$. هذه قاعدة السلسلة نفسها التي استعملتها في 4.1.")))
    U.add('sign', 'العلامة: متى أستخدمه؟', p(rich(
        'السؤال يقول <b>Find dy/dx</b> أو <b>Find the derivative</b>، وفي الدالة $\\sinh^{-1}$ أو $\\cosh^{-1}$ '
        'أو $\\tanh^{-1}$ أو $\\coth^{-1}$ أو $\\operatorname{sech}^{-1}$ أو $\\operatorname{csch}^{-1}$.'))
          + contrast([(r'y=\sinh^{-1}(5x-1)', 'جدول التوائم × $u\'$', 'دالة عكسية: الأس $-1$ اسم وليس قوة'),
                      (r'y=\sinh(5x-1)', 'من 4.1: $\\cosh(5x-1)\\cdot5$', 'دالة عادية، ليست عكسية'),
                      (r'\int\frac{dx}{\sqrt{1+x^{2}}}', 'تكامل (النوع 3)', 'المطلوب تكامل، ليس مشتقة')]))
    d41 = [formula('sinh(u)', 'cosh(u)', 'diff', branches=('x',), uprime=True, label='G 4.1 sinh'),
           formula('cosh(u)', 'sinh(u)', 'diff', branches=('x',), uprime=True, label='G 4.1 cosh'),
           formula('tanh(u)', 'sech(u)**2', 'diff', branches=('x',), uprime=True, label='G 4.1 tanh'),
           formula('coth(u)', '-csch(u)**2', 'diff', branches=('t',), uprime=True, label='G 4.1 coth'),
           formula('sech(u)', '-sech(u)*tanh(u)', 'diff', branches=('x',), uprime=True, label='G 4.1 sech'),
           formula('csch(u)', '-csch(u)*coth(u)', 'diff', branches=('t',), uprime=True, label='G 4.1 csch')]
    for f_, F_, br in [('asinh(x)', 'log(x+sqrt(x**2+1))', None), ('acosh(x)', 'log(x+sqrt(x**2-1))', '1+t'),
                       ('atanh(x)', 'log((1+x)/(1-x))/2', 't/(1+t)'), ('acoth(x)', 'log((x+1)/(x-1))/2', '1+t'),
                       ('asech(x)', 'log((1+sqrt(1-x**2))/x)', 't/(1+t)'), ('acsch(x)', 'log(1/x+sqrt(1+x**2)/Abs(x))', 't')]:
        same_value(f_, F_, 'log form ' + f_, branch=br)
    defs = table(['الدالة', 'تُعرَّف عند', 'الصيغة اللوغاريتمية (ص57)'], [
        [mi(r'\sinh^{-1}x'), 'كل ' + mi('x'), mi(r'\ln\left(x+\sqrt{x^{2}+1}\right)')],
        [mi(r'\cosh^{-1}x'), mi(r'x\ge1'), mi(r'\ln\left(x+\sqrt{x^{2}-1}\right)')],
        [mi(r'\tanh^{-1}x'), mi(r'|x|<1'), mi(r'\frac12\ln\frac{1+x}{1-x}')],
        [mi(r'\coth^{-1}x'), mi(r'|x|>1'), mi(r'\frac12\ln\frac{x+1}{x-1}')],
        [mi(r'\operatorname{sech}^{-1}x'), mi(r'0<x\le1'), mi(r'\ln\frac{1+\sqrt{1-x^{2}}}{x}')],
        [mi(r'\operatorname{csch}^{-1}x'), mi(r'x\ne0'), mi(r'\ln\left(\frac1x+\frac{\sqrt{1+x^{2}}}{|x|}\right)')]], 'formula compact')
    U.add('note', 'تذكير: من 4.1 ومن تعريف الدوال (ص56–57)',
          p('مشتقات الدوال الزائدية العادية (تحتاجها مع العكسية في نفس السؤال):')
          + table(['المشتقة', 'تساوي'], [frow(z) for z in d41], 'formula compact')
          + p(rich('الإشارة السالبة مع coth و sech و csch فقط.'), 'small')
          + p('الدوال العكسية الست ومجالها (للمعرفة، لا يُسأل عنها مباشرة في الاختبارات السابقة):') + defs)
    short, memo = sc_twins()
    U.add('short', '⚡ الاختصار: جدول التوائم', short + box_memo(memo))

    it = ITEMS['N42-E1-1']
    ex = question(it, 'U-D1 example 1')
    ex += short_steps(it, [
        ('وش داخل الدالة؟', r"u=5x-1,\quad u'=5", [('diff(5*x-1,x)', '5')]),
        ("صف sinh من جدول التوائم: $\\frac{u'}{\\sqrt{u^2+1}}$. عوّض:", r"y'=\frac{5}{\sqrt{1+(5x-1)^{2}}}",
         [('=ANS', '5/sqrt(1+(5*x-1)**2)')])], 'U-D1 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r"u=5x-1,\qquad u'=5", [('diff(5*x-1,x)', '5')], 'نسمّي ما داخل الدالة $u$. مشتقة $5x-1$: الـ $x$ تعطي 5، والرقم $-1$ يختفي'),
        ('tex', r'\frac{d}{du}\sinh^{-1}u=\frac{1}{\sqrt{u^{2}+1}}', [('diff(asinh(x),x)', '1/sqrt(x**2+1)')], 'من جدول التوائم (صف sinh)'),
        ('line', '5/sqrt(1+(5*x-1)**2)', "نضرب في $u'=5$ ونرجع $u=5x-1$")], 'U-D1 ex1')
    ex += final(it, 'U-D1 example 1')
    U.add('ex', 'مثال 1 (من المذكرة)', ex)

    it = ITEMS['1447-S2-SE-Q1.2']
    ex = question(it, 'U-D1 example 2')
    ex += short_steps(it, [
        ('وش داخل الدالة؟', r"u=\sqrt{x+2},\quad u'=\frac{1}{2\sqrt{x+2}}", [('diff(sqrt(x+2),x)', '1/(2*sqrt(x+2))')]),
        ("صف csch: $-\\frac{u'}{|u|\\sqrt{1+u^2}}$، و $|u|=\\sqrt{x+2}$، و $1+u^2=x+3$:", r"y'=-\frac{1}{2(x+2)\sqrt{x+3}}",
         [('1+sqrt(x+2)**2', 'x+3'), ('=ANS', '-1/(2*(x+2)*sqrt(x+3))')])], 'U-D1 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r"u=\sqrt{x+2},\qquad u'=\frac{1}{2\sqrt{x+2}}", [('diff(sqrt(x+2),x)', '1/(2*sqrt(x+2))')],
         'مشتقة الجذر = 1 على ضعف الجذر، في مشتقة ما تحته (هنا 1)'),
        ('tex', r'|u|=\sqrt{x+2},\qquad 1+u^{2}=1+(x+2)=x+3', [('1+sqrt(x+2)**2', 'x+3')],
         'الجذر موجب دائمًا فلا نحتاج القيمة المطلقة، ومربع الجذر = ما تحته'),
        ('line', '-(1/(2*sqrt(x+2)))/(sqrt(x+2)*sqrt(x+3))', "صف csch: $-\\frac{u'}{|u|\\sqrt{1+u^{2}}}$"),
        ('line', '-1/(2*(x+2)*sqrt(x+3))', 'نبسّط الكسر المركب (🧮 تحت)')], 'U-D1 ex2')
    ex += final(it, 'U-D1 example 2')
    U.add('ex', 'مثال 2 (اختبار سابق)', ex)
    U.raw(alg('root-self', 'الجذر في نفسه', [
        (r'\sqrt{x+2}\cdot\sqrt{x+2}=x+2', [('sqrt(x+2)*sqrt(x+2)', 'x+2')], 'الجذر مضروبًا في نفسه يعطي ما تحته:'),
        (r'\left(\sqrt{x+2}\right)^{2}=x+2', [('sqrt(x+2)**2', 'x+2')], 'وهو نفسه مربع الجذر:')]))
    U.raw(alg('frac-frac', 'كسر صغير فوق كسر كبير', [
        (r'\frac{\ \frac{1}{2\sqrt{x+2}}\ }{\sqrt{x+2}\,\sqrt{x+3}}=\frac{1}{2\sqrt{x+2}\cdot\sqrt{x+2}\cdot\sqrt{x+3}}',
         [('(1/(2*sqrt(x+2)))/(sqrt(x+2)*sqrt(x+3))', '1/(2*sqrt(x+2)*sqrt(x+2)*sqrt(x+3))')],
         'مقام الكسر الصغير ($2\\sqrt{x+2}$) ينزل ويُضرب في المقام الكبير:'),
        (r'=\frac{1}{2(x+2)\sqrt{x+3}}', [('1/(2*sqrt(x+2)*sqrt(x+2)*sqrt(x+3))', '1/(2*(x+2)*sqrt(x+3))')],
         'ثم $\\sqrt{x+2}\\cdot\\sqrt{x+2}=x+2$:')]))
    U.add('ok', '✔ تأكد في 10 ثواني', ul([rich('هل ضربت في $u\'$؟'), rich("صف sech أو csch؟ حدّه فيه إشارة سالبة (إذا كانت $u'$ موجبة).")]))
    U.add('trap', '⚠️ الفخ', ul([
        rich("أكثر غلطة: نسيان الضرب في $u'$."),
        rich('في csch⁻¹ إذا كان $u$ قد يكون سالبًا اكتب $|u|$. أحد المفاتيح الرسمية أسقطها فصار جوابه صحيحًا لـ $x>0$ فقط.'),
        '<b>تنبيه coth⁻¹:</b> المذكرة ص58 ومفتاح 1445 كتبا مشتقة coth⁻¹ بإشارة سالبة، والحساب الصحيح (ومفتاح 1446) موجبة '
        '— مثل tanh⁻¹ تمامًا. <b>اسأل الدكتور أي إشارة يعتمد</b>، واكتب في الكويز ما يقوله.']))
    U.add('paper', '✍️ في ورقة الكويز', p(rich("سطر $u$ و $u'$، ثم سطر الصيغة بالتعويض، ثم سطر التبسيط:"))
          + md(r"u=\sqrt{x+2},\ u'=\frac{1}{2\sqrt{x+2}}\ \Rightarrow\ y'=-\frac{u'}{|u|\sqrt{1+u^{2}}}=-\frac{1}{2(x+2)\sqrt{x+3}}"))
    U.drill('1', '1445-S1-SE-Q1.1', 'G',
            'اشتق كل حد لحاله. الأول من 4.1: cosh يصير sinh. الثاني صف sech مع $u=2x$.',
            first=r"\frac{d}{dx}\cosh(3x^{2})=6x\sinh(3x^{2}),\qquad u=2x,\ u'=2",
            claims=[('diff(cosh(3*x**2),x)', '6*x*sinh(3*x**2)'), ('diff(2*x,x)', '2')])
    U.drill('2', '1446-S1-SE-Q1.2', 'P',
            'صف sinh مع $u=\\sqrt{x}$. والحد الثاني من 4.1: مشتقة coth هي $-\\operatorname{csch}^2$.')
    U.drill('3', '1447-S1-SE-Q1.2', 'I',
            'sech من 4.1: $-\\operatorname{sech}u\\tanh u\\cdot u\'$. و tanh⁻¹ مع $u=\\sin x$.')
    return U


def box_memo(memo):
    return '<div class="memo-inline"><b>كيف أتذكّره:</b> ' + memo + '</div>'


# ---------------------------------------------------------------- 2
def u_deriv_rules():
    U = Unit('U-D2', 'مشتقات مركبة: أسية، ln، قوة، ضرب', '4.2', 'ص59، تمارين 1–6', 1)
    U.add('idea', 'الفكرة', p(rich(
        'الدالة العكسية تجي داخل قاعدة ثانية (أسية أو ln أو قوة أو ضرب). اشتق <b>القاعدة الكبيرة أولًا</b>، '
        'وإذا وصلت للدالة العكسية استخدم جدول التوائم كأنها $u$.')))
    U.add('sign', 'العلامة', p(rich('مشتقة، والدالة العكسية داخل $a^{(\\ldots)}$ أو $\\ln|\\ldots|$ أو $(\\ldots)^{n}$ '
                                    'أو مضروبة في دالة ثانية.')))
    r = [formula('b**u', 'b**u*log(b)', 'diff', branches=('x',), pos=('b',), uprime=True, label='rule a^u'),
         formula('exp(u)', 'exp(u)', 'diff', branches=('x',), uprime=True, label='rule e^u'),
         formula('log(Abs(u))', '1/u', 'diff', branches=('t', '-t'), uprime=True, label='rule ln|u|'),
         formula('log(Abs(u))/log(10)', '1/(u*log(10))', 'diff', branches=('t', '-t'), uprime=True, label='rule log10'),
         formula('u**n', 'n*u**(n-1)', 'diff', branches=('t',), real=('n',), uprime=True, label='rule u^n')]
    f, g = s.Function('f')(x), s.Function('g')(x)
    functional(lambda: s.diff(f * g, x) - (s.diff(f, x) * g + f * s.diff(g, x)), 'product rule')
    functional(lambda: s.simplify(s.diff(f / g, x) - (s.diff(f, x) * g - f * s.diff(g, x)) / g ** 2), 'quotient rule')
    rules = table(['المشتقة', 'تساوي'], [frow(z) for z in r], 'formula compact')
    rules += md(r"(f\,g)'=f'\,g+f\,g',\qquad \left(\frac{f}{g}\right)'=\frac{f'\,g-f\,g'}{g^{2}}")
    rules += p(rich('في الاختبارات $\\log$ بدون أساس = أساس 10 (والمذكرة تكتب $\\ln$ للطبيعي).'), 'small')
    U.add('short', '⚡ القواعد اللي تحيط بالدالة العكسية', rules)
    it = ITEMS['N42-E1-4']
    ex = question(it, 'U-D2 example')
    ex += short_steps(it, [
        ('الخارج أسية بأساس 6، والداخل:', r"u=\cosh^{-1}(2x),\quad u'=\frac{2}{\sqrt{4x^{2}-1}}",
         [('diff(acosh(2*x),x)', '2/sqrt(4*x**2-1)', '1+t')]),
        ("قاعدة الأسية $6^{u}\\cdot\\ln6\\cdot u'$:", r"y'=6^{\cosh^{-1}(2x)}\cdot\ln6\cdot\frac{2}{\sqrt{4x^{2}-1}}",
         [('=ANS', '6**acosh(2*x)*log(6)*2/sqrt(4*x**2-1)')])], 'U-D2 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r"y=6^{u}\ \Rightarrow\ y'=6^{u}\ln6\cdot u'", [('diff(6**acosh(2*x),x)', '6**acosh(2*x)*log(6)*diff(acosh(2*x),x)')],
         'القاعدة الكبيرة: أسية بأساس 6، و $u=\\cosh^{-1}(2x)$'),
        ('tex', r"u'=\frac{2}{\sqrt{(2x)^{2}-1}}=\frac{2}{\sqrt{4x^{2}-1}}", [('diff(acosh(2*x),x)', '2/sqrt(4*x**2-1)', '1+t')],
         'صف cosh من التوائم مع داخل $2x$ (مشتقته 2)'),
        ('line', '6**acosh(2*x)*log(6)*2/sqrt(4*x**2-1)', "قاعدة الأسية: $6^{u}\\cdot\\ln6\\cdot u'$")], 'U-D2 ex')
    ex += final(it, 'U-D2 example')
    U.add('ex', 'مثال (من المذكرة)', ex)
    U.raw(alg('pow-pow', 'أس فوق أس', [
        (r'\left(3^{x^{2}-1}\right)^{2}=3^{2(x^{2}-1)}=3^{2x^{2}-2}', [('(3**(x**2-1))**2', '3**(2*x**2-2)')],
         'عند تربيع أسية نضرب الأسين (تحتاجه في التمرين 3):'),
        (r'\left(e^{3x}\right)^{2}=e^{6x}', [('exp(3*x)**2', 'exp(6*x)')], 'ومثله مع $e$:')]))
    U.raw(alg('log10', 'log بأساس 10', [
        (r'\log u=\frac{\ln u}{\ln10}', [('log(x,10)', 'log(x)/log(10)')], 'نحوّل إلى ln، و$\\ln10$ رقم ثابت:'),
        (r"\frac{d}{dx}\log|u|=\frac{u'}{u\,\ln10}", [('diff(log(x**2+1)/log(10),x)', '2*x/((x**2+1)*log(10))')],
         'فالمشتقة مثل ln مقسومة على $\\ln10$:')]))
    it2 = ITEMS['1446-S2-SE-Q1.2']
    U.add('trap', '⚠️ الفخ', ul([
        rich('رتّب: القاعدة الخارجية أولًا، ثم الداخل. لا تشتق الدالة العكسية وتنسى الأسية.'),
        rich('$\\ln|\\tanh 4x|$: مشتقتها $\\frac{4\\operatorname{sech}^{2}4x}{\\tanh4x}$ — البسط مشتقة الداخل كاملة.'),
        'إشارة coth⁻¹ (تنبيه النوع 1). مثال صحيح الإشارة من مفتاح 1446:'])
          + question(it2, 'U-D2 trap') + final(it2, 'U-D2 trap'))
    U.add('paper', '✍️ في ورقة الكويز', p(rich("اكتب $u$ و $u'$ في سطر، ثم القاعدة الكبيرة، ثم الجواب.")))
    U.drill('1', 'N42-E1-6', 'G', 'قاعدة القوة أولًا، ثم اشتق ما داخل القوس حدًا حدًا.',
            first=r"y'=5\left(\operatorname{sech}^{-1}(3x)+7^{x}\right)^{4}\cdot\left(\operatorname{sech}^{-1}(3x)+7^{x}\right)'",
            claims=[('diff((asech(3*x)+7**x)**5,x)', '5*(asech(3*x)+7**x)**4*diff(asech(3*x)+7**x,x)')])
    U.drill('2', 'N42-X1-1', 'P', 'ضرب دالتين: الأولى × مشتقة الثانية + الثانية × مشتقة الأولى. و $(3^x)\'=3^x\\ln3$.')
    U.drill('3', '1446-S1-FE-Q1.3', 'I',
            'الحد الأول: صف cosh مع $u=3^{x^2-1}$ (🧮 أس فوق أس). الثاني: $\\log$ بأساس 10.')
    return U


# ---------------------------------------------------------------- 3
def u_six():
    U = Unit('U-I1', 'جدول التكاملات الستة وقاعدة الضبط', '4.2', 'ص59–60', 1)
    U.add('idea', 'الفكرة', p(rich(
        'التكامل عكس الاشتقاق: كل صف في جدول التوائم يعطي صف تكامل. شغلك أن ترتّب السؤال على شكل الصف: '
        'حد مربع $u^2$، ورقم مربع $a^2$، ومشتقة $u$ في البسط.')))
    U.add('sign', 'العلامة', p(rich('تكامل كسر، في المقام: جذر $\\sqrt{u^2\\pm a^2}$، أو $u\\sqrt{a^2\\pm u^2}$ ($u$ خارج الجذر)، '
                                    'أو بدون جذر $a^2-u^2$؛ والبسط رقم أو مشتقة $u$.'))
          + contrast([(r'\int\frac{dx}{\sqrt{4x^{2}+25}}', 'صف sinh', 'البسط رقم، والمقام جذر مجموع مربعين'),
                      (r'\int\frac{x\,dx}{\sqrt{4x^{2}+25}}', 'تعويض $w=4x^2+25$', 'البسط مشتقة ما تحت الجذر كله'),
                      (r'\int\frac{dx}{\sqrt{25-4x^{2}}}', '$\\sin^{-1}$ (درس 3.4)', 'رقم ناقص مربع تحت جذر')]))
    short, memo = sc_six()
    U.add('short', '⚡ الاختصار', short + box_memo(memo))
    it = ITEMS['N42-E2-3']
    ex = question(it, 'U-I1 example 1')
    ex += short_steps(it, [
        ('اكتب كمربعات:', r'4x^{2}+25=(2x)^{2}+5^{2}\ \Rightarrow\ u=2x,\ a=5', [('4*x**2+25', '(2*x)**2+5**2')]),
        ('جذر فيه مجموع ⇐ صف sinh. والضبط: مشتقة $u$ هي 2 والبسط 1 ⇐ نضرب في $\\frac12$:', r'\frac12\sinh^{-1}\frac{2x}{5}+C',
         [('=ANS', 'asinh(2*x/5)/2')])], 'U-I1 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'4x^{2}+25=(2x)^{2}+5^{2}', [('4*x**2+25', '(2*x)**2+5**2')], 'نكتب كل حد كمربع (🧮 تحت)'),
        ('sub', '2*x', '2', 'نسمّي $u=2x$'),
        ('tex', r'dx=\frac{du}{2}\ \Rightarrow\ \int\frac{dx}{\sqrt{(2x)^{2}+5^{2}}}=\frac12\int\frac{du}{\sqrt{u^{2}+5^{2}}}',
         [('1/sqrt((2*x)**2+5**2)', 'Rational(1,2)*diff(2*x,x)/sqrt((2*x)**2+5**2)')], 'نعوّض $dx$ فيظهر $\\frac12$'),
        ('line', 'asinh(2*x/5)/2', 'صف sinh: $\\sinh^{-1}\\frac{u}{a}$، ثم نرجع $u=2x$')], 'U-I1 ex1')
    ex += final(it, 'U-I1 example 1')
    U.add('ex', 'مثال 1 (من المذكرة)', ex)
    U.raw(alg('squares', 'كتابة الحد كمربع', [
        (r'4x^{2}=(2x)^{2}', [('4*x**2', '(2*x)**2')], 'جذر المعامل، ونصف الأس:'),
        (r'16x^{6}=(4x^{3})^{2}', [('16*x**6', '(4*x**3)**2')], 'جذر 16 = 4، ونصف 6 = 3:'),
        (r'25=5^{2},\qquad 9=3^{2}', [('5**2', '25'), ('3**2', '9')], 'والأرقام:'),
        (r'e^{6x}=\left(e^{3x}\right)^{2}', [('exp(6*x)', 'exp(3*x)**2')], 'ومع الأسية نصف الأس:')]))
    it = ITEMS['N42-X2-01']
    ex = question(it, 'U-I1 example 2')
    ex += short_steps(it, [
        ('اكتب كمربعات:', r'16x^{6}=(4x^{3})^{2},\ 9=3^{2}\ \Rightarrow\ u=4x^{3},\ a=3', [('16*x**6', '(4*x**3)**2')]),
        ('قاعدة الضبط مع $c=5$ و $n=3$ و $k=4$:', r'\frac{c}{nk}=\frac{5}{3\cdot4}=\frac{5}{12}', [('Rational(5,3*4)', 'Rational(5,12)')]),
        ('صف sinh × المعامل:', r'\frac{5}{12}\sinh^{-1}\frac{4x^{3}}{3}+C', [('=ANS', '5*asinh(4*x**3/3)/12')])], 'U-I1 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('sub', '4*x**3', '12*x**2', 'نسمّي $u=4x^3$'),
        ('tex', r'x^{2}dx=\frac{du}{12}\ \Rightarrow\ 5\int\frac{x^{2}\,dx}{\sqrt{9+16x^{6}}}=\frac{5}{12}\int\frac{du}{\sqrt{u^{2}+3^{2}}}',
         [('5*x**2/sqrt(9+16*x**6)', 'Rational(5,12)*diff(4*x**3,x)/sqrt((4*x**3)**2+3**2)')], 'البسط $5x^2dx=\\frac{5}{12}du$'),
        ('line', '5*asinh(4*x**3/3)/12', 'صف sinh ونرجع $u$')], 'U-I1 ex2')
    ex += final(it, 'U-I1 example 2')
    U.add('ex', 'مثال 2: البسط مضاعف للمشتقة (من المذكرة)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('cosh⁻¹ يصح بشرط $u>a$ فقط، كما تشترط المذكرة.'),
                                rich('لا تنسَ $\\frac{1}{a}$ في صفوف tanh و coth و sech و csch (صفّا الجذر وحده بدونها).'),
                                rich('إذا كان في البسط $x$ وتحت الجذر $x^2$ فقط (لا $x^4$ أو أعلى)، فهو تعويض عادي: $w$ = ما تحت الجذر (الصف الثاني في جدول العلامة).')]))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر: $u=\\ldots,\\ du=\\ldots$. سطر: التكامل بدلالة $u$. سطر: الجواب.')))
    U.drill('1', 'N42-E2-1', 'G', 'البسط $x\\,dx$ هو نصف $du$. صف cosh مع $a=4$.',
            first=r'x^{4}=(x^{2})^{2},\quad 16=4^{2},\quad u=x^{2},\ du=2x\,dx',
            claims=[('x**4', '(x**2)**2'), ('diff(x**2,x)', '2*x')])
    U.drill('2', 'N42-X2-02', 'P', '$25x^4=(5x^2)^2$ و $16=4^2$، و $u=5x^2$ مشتقتها $10x$.')
    U.drill('3', '1447-S2-SE-Q3.2', 'I', '$u=\\ln|x|$ ومشتقتها $\\frac1x$ موجودة. صف cosh مع $a=1$.')
    return U


# ---------------------------------------------------------------- 4
def u_tanh():
    U = Unit('U-I2', 'tanh⁻¹ أم coth⁻¹؟', '4.2', 'ص60، تمارين 3 و6', 2)
    U.add('idea', 'الفكرة', p(rich('الصيغة نفسها: $\\frac1a\\cdot(\\ldots)^{-1}\\frac{u}{a}$. الفرق الوحيد: '
                                   'إذا $|u|<a$ فهي tanh⁻¹، وإذا $|u|>a$ فهي coth⁻¹.')))
    U.add('sign', 'العلامة', p(rich('مقام <b>بدون جذر</b> من الشكل $a^2-u^2$، والبسط مشتقة $u$.'))
          + contrast([(r'\int\frac{dx}{25-x^{2}}', 'tanh⁻¹ أو coth⁻¹', 'رقم ناقص مربع، بلا جذر'),
                      (r'\int\frac{x\,dx}{25-x^{2}}', '$-\\frac12\\ln|25-x^2|$', 'البسط مشتقة المقام تقريبًا'),
                      (r'\int\frac{dx}{25+x^{2}}', '$\\tan^{-1}$ (ليس من هذا الدرس)', 'مجموع، ليس فرقًا')]))
    r = [formula('1/(a**2-u**2)', 'atanh(u/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='G tanh'),
         formula('1/(a**2-u**2)', 'acoth(u/a)/a', branches=('a+t', '-a-t'), pos=('a',), label='G coth')]
    U.add('short', '⚡ الاختصار', table(['التكامل', 'الجواب (+C)', 'متى'], [frow(r[0], mi('|u|<a')), frow(r[1], mi('|u|>a'))], 'formula')
          + box_memo(rich('قارن $|u|$ مع $a$: أصغر ⇐ tanh، أكبر ⇐ coth. والمعامل $\\frac1a$ في الحالتين.')))
    it = ITEMS['N42-E2-2']
    ex = question(it, 'U-I2 example 1')
    ex += short_steps(it, [
        ('اكتب كمربعين:', r'25-e^{2x}=5^{2}-\left(e^{x}\right)^{2}\ \Rightarrow\ u=e^{x},\ a=5', [('25-exp(2*x)', '5**2-exp(x)**2')]),
        ('البسط $e^x$ هو مشتقة $u$ بالضبط. والمذكرة تأخذ $e^x<5$، أي $|u|<a$ ⇐ tanh:', r'\frac15\tanh^{-1}\frac{e^{x}}{5}+C',
         [('=ANS', 'atanh(exp(x)/5)/5')])], 'U-I2 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'25-e^{2x}=5^{2}-\left(e^{x}\right)^{2}', [('25-exp(2*x)', '5**2-exp(x)**2')], 'نكتب كمربعين (🧮 كتابة الحد كمربع)'),
        ('sub', 'exp(x)', 'exp(x)', 'نسمّي $u=e^x$، ومشتقتها في البسط'),
        ('tex', r'=\int\frac{du}{5^{2}-u^{2}}', [('exp(x)/(25-exp(2*x))', 'diff(exp(x),x)/(5**2-exp(x)**2)')], 'التكامل بدلالة $u$'),
        ('line', 'atanh(exp(x)/5)/5', 'المذكرة تأخذ الجهة $e^x<5$ ⇐ tanh⁻¹، و $\\frac1a=\\frac15$')], 'U-I2 ex1')
    ex += final(it, 'U-I2 example 1') + p(rich('إذا كان $e^x>5$ يصير الجواب $\\frac15\\coth^{-1}\\frac{e^x}{5}$.'), 'small')
    U.add('ex', 'مثال 1 (من المذكرة)', ex)
    it = ITEMS['N42-X2-06']
    ex = question(it, 'U-I2 example 2')
    ex += short_steps(it, [
        ('اكتب كمربعين:', r'4-25\cosh^{2}x=2^{2}-(5\cosh x)^{2}\ \Rightarrow\ u=5\cosh x,\ a=2', [('4-25*cosh(x)**2', '2**2-(5*cosh(x))**2')]),
        ("الضبط: $u'=5\\sinh x$ والبسط $\\sinh x$ ⇐ نضرب في $\\frac15$. والمقارنة: $u\\ge5>2$ ⇐ coth:",
         r'\frac15\cdot\frac12\coth^{-1}\frac{5\cosh x}{2}=\frac{1}{10}\coth^{-1}\frac{5\cosh x}{2}+C',
         [('Rational(1,5)*Rational(1,2)', 'Rational(1,10)'), ('=ANS', 'acoth(5*cosh(x)/2)/10')])], 'U-I2 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'4-25\cosh^{2}x=2^{2}-(5\cosh x)^{2}', [('4-25*cosh(x)**2', '2**2-(5*cosh(x))**2')], 'مربعان'),
        ('sub', '5*cosh(x)', '5*sinh(x)', 'نسمّي $u=5\\cosh x$'),
        ('tex', r'\begin{array}{l}\sinh x\,dx=\frac{du}{5}\\ \displaystyle\int\frac{\sinh x\,dx}{4-25\cosh^{2}x}=\frac15\int\frac{du}{2^{2}-u^{2}}\end{array}',
         [('sinh(x)/(4-25*cosh(x)**2)', 'Rational(1,5)*diff(5*cosh(x),x)/(2**2-(5*cosh(x))**2)')], 'البسط $\\sinh x\\,dx$'),
        ('tex', r'u=5\cosh x\ge5>2=a', [], 'لأن $\\cosh x\\ge1$ دائمًا ⇐ $|u|>a$ ⇐ coth⁻¹'),
        ('line', 'acoth(5*cosh(x)/2)/10', '$\\frac15\\cdot\\frac12\\coth^{-1}\\frac{u}{2}$')], 'U-I2 ex2')
    ex += final(it, 'U-I2 example 2')
    U.add('ex', 'مثال 2: لماذا coth هنا؟ (من المذكرة)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تختار tanh تلقائيًا: افحص $|u|$ و $a$.'),
                                'المذكرة ص60 كتبت صيغة coth⁻¹ بإشارة سالبة؛ الحساب يعطي موجبة (تنبيه النوع 1).']))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر $u$ و $du$، وسطر يبيّن المقارنة ($u\\ge5>2$)، ثم الجواب.')))
    U.drill('1', 'N42-X2-03', 'G', 'قرب الصفر $|u|$ صغير ⇐ tanh. المعامل: $\\frac{1}{12}\\cdot\\frac16$.',
            first=r'9x^{8}=(3x^{4})^{2},\quad 36=6^{2},\quad u=3x^{4},\ du=12x^{3}dx',
            claims=[('9*x**8', '(3*x**4)**2'), ('diff(3*x**4,x)', '12*x**3')])
    U.drill('2', 'G-15', 'P', '$u=e^{2x}$ و $a=3$؛ إذا $e^{2x}<3$ فهي tanh.')
    return U


# ---------------------------------------------------------------- 5
def u_sech():
    U = Unit('U-I3', 'x في المقام: sech⁻¹ و csch⁻¹', '4.2', 'ص60، تمارين 4 و5 و11', 2)
    U.add('idea', 'الفكرة', p(rich('إذا خارج الجذر $x$ وداخله قوة لـ $x$، اضرب فوق وتحت في $x$ (أو قوة له) حتى يصير '
                                   'خارج الجذر $u$ نفسه وفي البسط مشتقته. بعدها صف sech (داخل الجذر ناقص) أو csch (زائد).')))
    U.add('sign', 'العلامة', p(rich('$\\int\\frac{dx}{x\\sqrt{a^2\\pm x^{n}}}$: $x$ في المقام خارج الجذر.')))
    r = [formula('1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='G sech'),
         formula('1/(u*sqrt(a**2+u**2))', '-acsch(Abs(u)/a)/a', pos=('a',), label='G csch')]
    U.add('short', '⚡ الاختصار', table(['التكامل', 'الجواب (+C)'], [frow(z) for z in r], 'formula')
          + box_memo(rich('سالب دائمًا، و $\\frac1a$، و $|u|$. داخل الجذر $-$ ⇐ sech، و $+$ ⇐ csch.')))
    it = ITEMS['N42-E2-5']
    ex = question(it, 'U-I3 example')
    ex += short_steps(it, [
        ('اضرب فوق وتحت في $x$ فيصير:', r'u=x^{2},\quad x\,dx=\frac{du}{2},\quad 16=4^{2}\ \Rightarrow\ a=4', [('x**4', '(x**2)**2'), ('4**2', '16')]),
        ('داخل الجذر ناقص ⇐ صف sech (سالب، و $\\frac1a$):', r'\frac12\cdot\left(-\frac14\right)\operatorname{sech}^{-1}\frac{x^{2}}{4}=-\frac18\operatorname{sech}^{-1}\frac{x^{2}}{4}+C',
         [('Rational(1,2)*(-Rational(1,4))', '-Rational(1,8)'), ('=ANS', '-asech(x**2/4)/8')])], 'U-I3 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\frac{1}{x\sqrt{16-x^{4}}}=\frac{x}{x^{2}\sqrt{4^{2}-(x^{2})^{2}}}',
         [('1/(x*sqrt(16-x**4))', 'x/(x**2*sqrt(4**2-(x**2)**2))')], 'نضرب فوق وتحت في $x$ (🧮 تحت)'),
        ('sub', 'x**2', '2*x', 'نسمّي $u=x^2$'),
        ('tex', r'\begin{array}{l}x\,dx=\frac{du}{2}\\ \displaystyle\int\frac{x\,dx}{x^{2}\sqrt{16-x^{4}}}=\frac12\int\frac{du}{u\sqrt{4^{2}-u^{2}}}\end{array}',
         [('x/(x**2*sqrt(4**2-(x**2)**2))', 'Rational(1,2)*diff(x**2,x)/(x**2*sqrt(4**2-(x**2)**2))')], 'التكامل بدلالة $u$'),
        ('line', '-asech(x**2/4)/8', 'صف sech: $\\frac12\\cdot\\left(-\\frac14\\right)\\operatorname{sech}^{-1}\\frac{|u|}{4}$، و $|x^2|=x^2$')],
        'U-I3 ex')
    ex += final(it, 'U-I3 example')
    U.add('ex', 'مثال (من المذكرة)', ex)
    U.raw(alg('times-x', 'الضرب فوق وتحت', [
        (r'\frac{1}{x\sqrt{16-x^{4}}}\cdot\frac{x}{x}=\frac{x}{x^{2}\sqrt{16-x^{4}}}',
         [('1/(x*sqrt(16-x**4))*x/x', 'x/(x**2*sqrt(16-x**4))')], 'نضرب في $\\frac{x}{x}=1$ فلا تتغير القيمة:'),
        (r'x^{4}=\left(x^{2}\right)^{2}', [('x**4', '(x**2)**2')], 'فيظهر $u=x^2$ مرتين: خارج الجذر وداخله:')]))
    U.add('trap', '⚠️ الفخ', ul([rich('إذا كان $u$ قد يكون سالبًا (مثل $x^3$) اكتب $|u|$. مفتاح 1445 أسقطها فصار صحيحًا لـ $x>0$ فقط.'),
                                rich('اضرب في القوة التي تجعل الخارج = $u$: مع $x^6$ اضرب في $x^2$ ($u=x^3$).')]))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر الضرب في $\\frac{x}{x}$، سطر $u$ و $du$، ثم الجواب.')))
    U.drill('1', 'G-16', 'G', 'مثل المثال، لكن داخل الجذر $+$ ⇐ csch. و $x^2\\ge0$ فلا حاجة لـ $|\\,|$.',
            first=r'\frac{x}{x^{2}\sqrt{(x^{2})^{2}+3^{2}}},\qquad u=x^{2},\ du=2x\,dx',
            claims=[('1/(x*sqrt(x**4+9))', 'x/(x**2*sqrt((x**2)**2+3**2))')])
    U.drill('2', 'N42-X2-11', 'P', '$4x^4=(2x^2)^2$، و $u=2x^2$، و $a=5$.')
    U.drill('3', '1445-S2-SE-Q2.4', 'I', 'اضرب في $x^2$ فوق وتحت: $u=x^3$، واكتب $|x^3|$.')
    return U


# ---------------------------------------------------------------- 6
def u_lamda():
    U = Unit('U-I4', 'لامدا: أسية تحت الجذر', '4.2', 'ص61، تمارين 10 و12', 2)
    U.add('idea', 'الفكرة', p(rich('أسية تحت الجذر بدون مشتقتها في البسط. الحل الطويل: اضرب فوق وتحت في الأسية فتصير '
                                   'النوع السابق (sech أو csch). الاختصار يعطيك الجواب مباشرة.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\frac{dx}{\\sqrt{e^{kx}+a^2}}$ أو $\\int\\frac{dx}{\\sqrt{a^2-b^{kx}}}$ أو $\\int\\frac{dx}{x\\sqrt{a^2\\pm x^{n}}}$ و $n$ فردي (مثل $x^3$)، والبسط رقم فقط '
                                    '(مع $\\sqrt{e^{kx}-a^2}$ يطلع $\\sec^{-1}$، وهذا ليس من الدرس).')))
    short, memo = sc_lamda()
    U.add('short', '⚡ الاختصار', short + box_memo(memo))
    it = ITEMS['1446-S2-SE-Q2.7']
    ex = question(it, 'U-I4 example')
    ex += short_steps(it, [
        ('اكتب الأسية كمربع:', r'e^{6x}=\left(e^{3x}\right)^{2}\ \Rightarrow\ b=e,\ \lambda=3,\ a=1', [('exp(6*x)', 'exp(3*x)**2')]),
        ('داخل الجذر $+$ ⇐ csch، والمعامل $-\\frac{1}{a\\lambda\\ln b}$:', r'-\frac{1}{1\cdot3\cdot\ln e}\operatorname{csch}^{-1}e^{3x}=-\frac13\operatorname{csch}^{-1}e^{3x}+C',
         [('1/(1*3*log(E))', 'Rational(1,3)'), ('=ANS', '-acsch(exp(3*x))/3')])], 'U-I4 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\frac{1}{\sqrt{e^{6x}+1}}=\frac{e^{3x}}{e^{3x}\sqrt{(e^{3x})^{2}+1}}',
         [('1/sqrt(exp(6*x)+1)', 'exp(3*x)/(exp(3*x)*sqrt(exp(3*x)**2+1))')], 'نضرب فوق وتحت في $e^{3x}$'),
        ('sub', 'exp(3*x)', '3*exp(3*x)', 'نسمّي $u=e^{3x}$'),
        ('tex', r'\begin{array}{l}e^{3x}dx=\frac{du}{3}\\ \displaystyle\int\frac{e^{3x}dx}{e^{3x}\sqrt{e^{6x}+1}}=\frac13\int\frac{du}{u\sqrt{u^{2}+1}}\end{array}',
         [('exp(3*x)/(exp(3*x)*sqrt(exp(3*x)**2+1))', 'Rational(1,3)*diff(exp(3*x),x)/(exp(3*x)*sqrt(exp(3*x)**2+1))')], 'التكامل بدلالة $u$'),
        ('line', '-acsch(exp(3*x))/3', 'صف csch مع $a=1$، و $u=e^{3x}>0$')], 'U-I4 ex')
    ex += final(it, 'U-I4 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('إذا ظهرت مشتقة الداخل في البسط، مثل $\\frac{e^x}{\\sqrt{e^{2x}+1}}$، فهذا النوع 3 مباشرة.'),
                                rich('مع أساس غير $e$ (مثل $5^x$) يظهر $\\ln5$ في المقام.')]))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('اكتب سطر الضرب في الأسية (يقنع المصحح)، ثم الجواب.')))
    U.drill('1', 'N42-E2-6', 'G', 'لامدا مع $\\lambda=1$ و $a=1$ و $b=e$.', first=r'e^{2x}=\left(e^{x}\right)^{2}:\quad b=e,\ \lambda=1,\ a=1',
            claims=[('exp(2*x)', 'exp(x)**2')])
    U.drill('2', '1447-S1-SE-Q2.2', 'P', 'الأساس 5: $5^{2x}=(5^x)^2$، فيظهر $\\ln5$ في المقام.')
    U.drill('3', 'N42-X2-10', 'I', 'داخل الجذر ناقص ⇐ sech، و $a=3$ و $\\lambda=3$، والبسط 2 يضرب الجواب.')
    U.drill('4', 'N42-X2-12', 'I', 'شكل القوة: $x^3=(x^{3/2})^2$، فـ $\\lambda=\\frac32$ و $a=5$، وداخل الجذر ناقص ⇐ sech.')
    return U


# ---------------------------------------------------------------- 7
def u_sqrt():
    U = Unit('U-I5', 'جذر x مخفي', '4.2', 'ص61، تمرين 2(4)', 2)
    U.add('idea', 'الفكرة', p(rich('$\\frac{1}{\\sqrt x}$ في السؤال هي تقريبًا مشتقة $\\sqrt x$. نسمّي $u=\\sqrt{x}$ فيصير '
                                   '$x=u^2$ ويظهر شكل الجدول.')))
    U.add('sign', 'العلامة', p(rich('$\\sqrt{x}$ في المقام، ومعها جذر فيه $x$ وحدها، مثل $\\sqrt{x}\\sqrt{4+x}$.')))
    f = formula('1/(sqrt(x)*sqrt(a**2+x))', '2*asinh(sqrt(x)/a)', var='x', branches=('t',), pos=('a',), label='G sqrt sinh')
    U.add('short', '⚡ الاختصار', md(f[0] + ' = ' + f[1] + ' + C') + box_memo(rich('ضعف sinh⁻¹ مع $\\sqrt{x}$ داخلها.')))
    it = ITEMS['N42-E2-4']
    ex = question(it, 'U-I5 example')
    ex += short_steps(it, [
        ('الشكل $\\frac{1}{\\sqrt x\\sqrt{a^2+x}}$ مع:', r'a^{2}=4\ \Rightarrow\ a=2', [('2**2', '4')]),
        ('ضعف sinh⁻¹، و $\\sqrt x$ داخلها:', r'2\sinh^{-1}\frac{\sqrt{x}}{2}+C', [('=ANS', '2*asinh(sqrt(x)/2)')])], 'U-I5 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('sub', 'sqrt(x)', '1/(2*sqrt(x))', 'نسمّي $u=\\sqrt x$'),
        ('tex', r'\frac{dx}{\sqrt{x}}=2\,du,\qquad 4+x=2^{2}+u^{2}', [('4+sqrt(x)**2', '4+x')], 'لأن $u^2=x$ (🧮 الجذر في نفسه)'),
        ('tex', r'=2\int\frac{du}{\sqrt{u^{2}+2^{2}}}', [('1/(sqrt(x)*sqrt(4+x))', '2*diff(sqrt(x),x)/sqrt(sqrt(x)**2+2**2)')], 'التكامل بدلالة $u$'),
        ('line', '2*asinh(sqrt(x)/2)', 'صف sinh ونرجع $u=\\sqrt x$')], 'U-I5 ex')
    ex += final(it, 'U-I5 example')
    U.add('ex', 'مثال (من المذكرة)', ex)
    U.raw(alg('root-self'))
    U.add('trap', '⚠️ الفخ', ul([rich('لا تنسَ الـ 2: $\\frac{dx}{\\sqrt x}=2\\,du$.'),
                                rich('المفتاح الرسمي لسؤال 1445 أعطى أيضًا $2\\cosh^{-1}\\sqrt{x+1}$، وهو جواب صحيح آخر.')]))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر $u=\\sqrt x$، $du=\\frac{dx}{2\\sqrt x}$، ثم الجواب.')))
    U.drill('1', '1445-S1-SE-Q2.2', 'G', 'نفس المثال مع $a=1$.', first=r'u=\sqrt{x},\quad \frac{dx}{\sqrt{x}}=2\,du,\quad 1+x=1+u^{2}',
            claims=[('1+sqrt(x)**2', '1+x')])
    U.drill('2', 'G-39', 'I', 'نفس التعويض $u=\\sqrt x$، لكن داخل الجذر $u^2-4$ ⇐ صف cosh مع $a=2$.')
    return U


# ---------------------------------------------------------------- 8
def u_split():
    U = Unit('U-I6', 'بسط مركّب: افصل الكسر', '4.2', 'ص62، تمرينا 7 و8', 2)
    U.add('idea', 'الفكرة', p(rich('إذا البسط فيه $x$ ورقم، افصل الكسر لكسرين: جزء $x$ تعويض مباشر، وجزء الرقم من الجدول.')))
    U.add('sign', 'العلامة', p(rich('البسط مثل $x-2$ أو $2x+3$، والمقام من أشكال الجدول.')))
    m1 = formula('x/sqrt(c+x**2)', 'sqrt(c+x**2)', var='x', branches=('t', '-t'), pos=('c',), label='G micro +')
    m3 = formula('x/(c-x**2)', '-log(Abs(c-x**2))/2', var='x', branches=('sqrt(c)*t/(1+t)', 'sqrt(c)+t'), pos=('c',), label='G micro ln -')
    U.add('short', '⚡ الاختصار', table(['جزء x', 'الجواب (+C)'], [frow(m1), frow(m3)], 'formula compact')
          + box_memo('جزء x: ضد الجدول، ينحل بتعويض. جزء الرقم: الجدول.'))
    it = ITEMS['N42-X2-07']
    ex = question(it, 'U-I6 example')
    ex += short_steps(it, [
        ('افصل البسط:', r'\frac{x}{\sqrt{25+x^{2}}}-\frac{2}{\sqrt{25+x^{2}}}', [('(x-2)/sqrt(25+x**2)', 'x/sqrt(25+x**2)-2/sqrt(25+x**2)')]),
        ('جزء $x$ من جدول الاختصار:', r'\int\frac{x\,dx}{\sqrt{25+x^{2}}}=\sqrt{25+x^{2}}', [('diff(sqrt(25+x**2),x)', 'x/sqrt(25+x**2)')]),
        ('جزء الرقم صف sinh مع $a=5$، ثم اجمع:', r'\sqrt{25+x^{2}}-2\sinh^{-1}\frac{x}{5}+C', [('=ANS', 'sqrt(25+x**2)-2*asinh(x/5)')])], 'U-I6 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\frac{x-2}{\sqrt{25+x^{2}}}=\frac{x}{\sqrt{25+x^{2}}}-\frac{2}{\sqrt{25+x^{2}}}',
         [('(x-2)/sqrt(25+x**2)', 'x/sqrt(25+x**2)-2/sqrt(25+x**2)')], 'نفصل الكسر (البسط على المقام لكل حد)'),
        ('line', 'sqrt(25+x**2)-Integral(2/sqrt(25+x**2),x)', 'الجزء الأول: $\\int\\frac{x}{\\sqrt{c+x^2}}dx=\\sqrt{c+x^2}$'),
        ('line', 'sqrt(25+x**2)-2*asinh(x/5)', 'الجزء الثاني: صف sinh مع $a=5$')], 'U-I6 ex')
    ex += final(it, 'U-I6 example')
    U.add('ex', 'مثال (من المذكرة)', ex)
    U.add('trap', '⚠️ الفخ', p(rich('انتبه للإشارة عند الفصل: $\\frac{x-2}{\\ldots}=\\frac{x}{\\ldots}-\\frac{2}{\\ldots}$.')))
    U.add('paper', '✍️ في ورقة الكويز', p('سطر الفصل، ثم جواب كل جزء، ثم اجمع.'))
    U.drill('1', 'G-01', 'G', 'الجزء الأول تعويض $w=x^2+9$، والثاني صف sinh مع $a=3$.',
            first=r'=\int\frac{2x}{\sqrt{x^{2}+9}}\,dx+\int\frac{3}{\sqrt{x^{2}+9}}\,dx',
            claims=[('(2*x+3)/sqrt(x**2+9)', '2*x/sqrt(x**2+9)+3/sqrt(x**2+9)')])
    U.drill('2', 'N42-X2-08', 'I', 'افصل: $\\frac{x}{16-x^2}$ يعطي ln، و $\\frac{1}{16-x^2}$ يعطي tanh⁻¹ مع $a=4$.')
    return U


# ---------------------------------------------------------------- 9
def u_invnum():
    U = Unit('U-I7', 'دالة عكسية ومشتقتها في السؤال', '4.2', 'ص62، تمرين 9', 3)
    U.add('idea', 'الفكرة', p(rich('إذا شفت دالة عكسية <b>ومشتقتها</b> في نفس التكامل، هذا تعويض بسيط: $u$ = الدالة العكسية.')))
    U.add('sign', 'العلامة', contrast([(r'\int\frac{\cosh^{-1}x}{\sqrt{x^{2}-1}}dx', 'تعويض $u=\\cosh^{-1}x$', 'المقام مشتقة $\\cosh^{-1}x$'),
                                       (r'\int\cosh^{-1}x\,dx', 'تجزئة (اليوم 4)', 'الدالة وحدها بلا مشتقتها')]))
    U.add('short', '⚡ الاختصار', md(r'\int f^{-1}\cdot\left(f^{-1}\right)'"'"r'\,dx=\frac{\left(f^{-1}\right)^{2}}{2}+C')
          + box_memo('الدالة × مشتقتها ⇐ مربع الدالة على 2.'))
    functional(lambda: s.diff(s.Function('g')(x) ** 2 / 2, x) - s.Function('g')(x) * s.diff(s.Function('g')(x), x), 'g g\' rule')
    it = ITEMS['N42-X2-09']
    ex = question(it, 'U-I7 example')
    ex += short_steps(it, [
        ('المقام $\\frac{1}{\\sqrt{x^2-1}}$ هو مشتقة الدالة:', r'f^{-1}=\cosh^{-1}x,\quad \left(\cosh^{-1}x\right)'"'"r'=\frac{1}{\sqrt{x^{2}-1}}',
         [('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t')]),
        ('الدالة × مشتقتها ⇐ مربعها على 2:', r'\frac{\left(\cosh^{-1}x\right)^{2}}{2}+C', [('=ANS', 'acosh(x)**2/2')])], 'U-I7 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('sub', 'acosh(x)', '1/sqrt(x**2-1)', 'مشتقة $\\cosh^{-1}x$ موجودة في المقام', 'u', '1+t'),
        ('tex', r'=\int u\,du=\frac{u^{2}}{2}', [('integrate(x,x)', 'x**2/2')], 'قاعدة القوة')], 'U-I7 ex')
    ex += final(it, 'U-I7 example')
    U.add('ex', 'مثال (من المذكرة)', ex)
    U.add('trap', '⚠️ الفخ', p(rich('$(\\cosh^{-1}x)^2$ تعني مربع الدالة، وليست $\\cosh^{-1}(x^2)$.')))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر $u$ و $du$، ثم $\\int u\\,du$، ثم الجواب.')))
    U.drill('1', 'G-02', 'G', '$\\int u^2du=\\frac{u^3}{3}$.', first=r'u=\sinh^{-1}x,\quad du=\frac{dx}{\sqrt{1+x^{2}}}',
            claims=[('diff(asinh(x),x)', '1/sqrt(1+x**2)')])
    U.drill('2', 'G-03', 'I', 'مشتقة $\\tanh^{-1}x$ هي $\\frac{1}{1-x^2}$.')
    return U


# ---------------------------------------------------------------- 10
def u_square():
    U = Unit('U-I8', 'إكمال المربع', '4.2', 'ص61، تمارين 13 و14', 3)
    U.add('idea', 'الفكرة', p(rich('تحت الجذر ثلاثي فيه حد $x$ (مثل $x^2+6x-16$). نكمّل المربع فيصير $(x-h)^2\\pm d$، '
                                   'ثم $u=x-h$ ونستخدم جدول التكاملات.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\frac{c\\,dx}{\\sqrt{Ax^2+Bx+D}}$ وفيه حد $x$ (أي $B\\ne0$)، ولا عامل خارج الجذر.')))
    short, memo = sc_square()
    U.add('short', '⚡ الاختصار', short + box_memo(memo))
    it = ITEMS['1446-S1-SE-Q2.2']
    ex = question(it, 'U-I8 example 1')
    ex += short_steps(it, [
        ('المركز:', r'h=-\frac{B}{2A}=-\frac{6}{2}=-3', [('-Rational(6,2)', '-3')]),
        ('قيمة الثلاثي عند المركز:', r'd=Q(-3)=9-18-16=-25=-5^{2}', [('9-18-16', '-25')]),
        ('الباقي سالب ⇐ cosh مع $u=x+3$ و $a=5$:', r'3\cosh^{-1}\frac{x+3}{5}+C', [('=ANS', '3*acosh((x+3)/5)')])], 'U-I8 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'x^{2}+6x-16=(x+3)^{2}-5^{2}', [('x**2+6*x-16', '(x+3)**2-5**2')], 'إكمال المربع (🧮 تحت)'),
        ('sub', 'x+3', '1', 'نسمّي $u=x+3$'),
        ('tex', r'=3\int\frac{du}{\sqrt{u^{2}-5^{2}}}', [('3/sqrt((x+3)**2-5**2)', '3/sqrt(x**2+6*x-16)')], 'التكامل بدلالة $u$'),
        ('line', '3*acosh((x+3)/5)', 'صف cosh (بشرط $x+3>5$)')], 'U-I8 ex1')
    ex += final(it, 'U-I8 example 1')
    U.add('ex', 'مثال 1 (اختبار سابق)', ex)
    U.raw(alg('complete-square', 'إكمال المربع', [
        (r'6\div2=3', [('Rational(6,2)', '3')], 'معامل $x$ هو 6، ونصفه:'),
        (r'3^{2}=9', [('3**2', '9')], 'نربّعه:'),
        (r'x^{2}+6x-16=x^{2}+6x+9-9-16', [('x**2+6*x-16', 'x**2+6*x+9-9-16')], 'نضيف 9 ونطرحها، فما تتغير القيمة:'),
        (r'x^{2}+6x+9=(x+3)^{2}', [('x**2+6*x+9', '(x+3)**2')], 'أول ثلاثة حدود مربع كامل:'),
        (r'(x+3)^{2}=x^{2}+3x+3x+9=x^{2}+6x+9\ \checkmark', [('(x+3)**2', 'x**2+6*x+9')], 'تأكد بالفك:'),
        (r'-9-16=-25=-5^{2}', [('-9-16', '-25')], 'الأرقام الباقية:'),
        (r'x^{2}+6x-16=(x+3)^{2}-5^{2}', [('x**2+6*x-16', '(x+3)**2-5**2')], 'النتيجة:')],
        intro='الاختصار ($h$ و $d$) يعطي النتيجة نفسها بسرعة؛ هذه الطريقة الكاملة لو نسيته.'))
    it = ITEMS['1445-S2-SE-Q2.7']
    ex = question(it, 'U-I8 example 2')
    ex += short_steps(it, [
        ('المركز والباقي:', r'h=-\frac{6}{2}=-3,\quad d=Q(-3)=9-18+13=4=2^{2}', [('-Rational(6,2)', '-3'), ('9-18+13', '4')]),
        ('الباقي موجب ⇐ sinh مع $u=x+3$ و $a=2$:', r'\sinh^{-1}\frac{x+3}{2}+C', [('=ANS', 'asinh((x+3)/2)')])], 'U-I8 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'x^{2}+6x+13=(x+3)^{2}+2^{2}', [('x**2+6*x+13', '(x+3)**2+2**2')], 'إكمال المربع: نصف 6 هو 3، و $13-9=4$'),
        ('sub', 'x+3', '1', 'نسمّي $u=x+3$'),
        ('tex', r'=\int\frac{du}{\sqrt{u^{2}+2^{2}}}', [('1/sqrt((x+3)**2+2**2)', '1/sqrt(x**2+6*x+13)')], 'التكامل بدلالة $u$'),
        ('line', 'asinh((x+3)/2)', 'صف sinh مع $a=2$')], 'U-I8 ex2')
    ex += final(it, 'U-I8 example 2')
    U.add('ex', 'مثال 2: الباقي موجب ⇐ sinh (اختبار سابق)', ex)
    U.raw(alg('factor-root', 'إخراج رقم من الجذر', [
        (r'9x^{2}+36x+45=9\left(x^{2}+4x+5\right)', [('9*x**2+36*x+45', '9*(x**2+4*x+5)')], 'نأخذ 9 عاملًا مشتركًا:'),
        (r'\sqrt{9\left(x^{2}+4x+5\right)}=\sqrt9\cdot\sqrt{x^{2}+4x+5}=3\sqrt{x^{2}+4x+5}',
         [('sqrt(9*(x**2+4*x+5))', '3*sqrt(x**2+4*x+5)')], 'جذر الضرب = ضرب الجذور:')],
        intro='تحتاجه إذا كان معامل $x^2$ ليس 1 (التمرين 3).'))
    U.add('trap', '⚠️ الفخ', ul([rich('$h=-\\frac{B}{2A}$: انتبه للإشارة. $x^2-4x$ مركزه $h=+2$.'),
                                rich('الباقي سالب ⇐ cosh، موجب ⇐ sinh. ومعامل $x^2$ سالب بلا عامل خارج الجذر ⇐ ليس من هذا الدرس ($\\sin^{-1}$).')]))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر إكمال المربع (مثل $x^2+6x-16=(x+3)^2-5^2$)، ثم سطر الصيغة.')))
    U.drill('1', '1447-S1-FE-Q2.1', 'G', 'صف cosh مع $a=2$ و $u=x-2$.',
            first=r'h=-\frac{-4}{2}=2,\quad Q(2)=4-8=-4,\quad x^{2}-4x=(x-2)^{2}-2^{2}',
            claims=[('-Rational(-4,2)', '2'), ('4-8', '-4'), ('x**2-4*x', '(x-2)**2-2**2')])
    U.drill('2', 'N42-X2-14', 'P', '$h=-1$ و $Q(-1)=9$، والبسط 5 يضرب الجواب.')
    U.drill('3', 'G-04', 'I', 'أخرج 9 من الجذر أولًا (🧮 إخراج رقم من الجذر)، ثم $h=-2$.')
    return U


# ---------------------------------------------------------------- 11
def u_square_lin():
    U = Unit('U-I9', 'إكمال المربع مع عامل خارج الجذر', '4.2', 'ص61، تمارين 15 و16', 3)
    U.add('idea', 'الفكرة', p(rich('مثل النوع السابق، لكن خارج الجذر عامل $(x-h)$ هو نفسه مركز المربع. بعد $u=x-h$ يصير '
                                   'السؤال من النوع 5 (sech أو csch).')))
    U.add('sign', 'العلامة', p(rich('$\\int\\frac{c\\,dx}{(x-h)\\sqrt{Ax^2+Bx+D}}$ والعامل الخارجي يطابق المركز $h$ تمامًا.')))
    U.add('short', '⚡ الاختصار', p(rich('من جدول إكمال المربع (النوع 10): الصفان الأخيران. المعامل دائمًا $-\\frac{c}{\\sqrt d}$، '
                                        'ومعامل $x^2$ موجب ⇐ csch، سالب ⇐ sech (والباقي $d>0$ في الحالتين).')))
    it = ITEMS['N42-E2-8']
    ex = question(it, 'U-I9 example')
    ex += short_steps(it, [
        ('المركز والباقي:', r'h=-\frac{2}{2\cdot(-1)}=1,\quad d=Q(1)=-1+2+3=4,\quad \sqrt d=2', [('-Rational(2,2*(-1))', '1'), ('-1+2+3', '4')]),
        ('العامل خارج الجذر $(x-1)=(x-h)$ ✓، ومعامل $x^2$ سالب ⇐ sech، والمعامل $-\\frac{c}{\\sqrt d}=-\\frac12$:',
         r'-\frac12\operatorname{sech}^{-1}\frac{|x-1|}{2}+C', [('=ANS', '-asech(Abs(x-1)/2)/2')])], 'U-I9 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'-x^{2}+2x+3=2^{2}-(x-1)^{2}', [('-x**2+2*x+3', '2**2-(x-1)**2')], 'إكمال المربع مع سالب (🧮 تحت)'),
        ('sub', 'x-1', '1', 'نسمّي $u=x-1$، وهو نفسه العامل خارج الجذر'),
        ('tex', r'=\int\frac{du}{u\sqrt{2^{2}-u^{2}}}', [('1/((x-1)*sqrt(-x**2+2*x+3))', 'diff(x-1,x)/((x-1)*sqrt(2**2-(x-1)**2))')],
         'التكامل بدلالة $u$'),
        ('line', '-asech(Abs(x-1)/2)/2', 'صف sech مع $a=2$ و $|u|$')], 'U-I9 ex')
    ex += final(it, 'U-I9 example')
    ex += p(rich('المذكرة كتبت الجواب بدون $|\\,|$ فصار صحيحًا لـ $x>1$ فقط.'), 'small')
    U.add('ex', 'مثال (من المذكرة)', ex)
    U.raw(alg('neg-square', 'إكمال المربع ومعامل x² سالب', [
        (r'-x^{2}+2x+3=-\left(x^{2}-2x\right)+3', [('-x**2+2*x+3', '-(x**2-2*x)+3')], 'نُخرج السالب من حدّي $x$:'),
        (r'x^{2}-2x=(x-1)^{2}-1', [('x**2-2*x', '(x-1)**2-1')], 'نكمّل المربع داخل القوس:'),
        (r'-\left[(x-1)^{2}-1\right]+3=4-(x-1)^{2}', [('-((x-1)**2-1)+3', '4-(x-1)**2')], 'نوزّع السالب ونجمع الأرقام:')]))
    U.add('trap', '⚠️ الفخ', ul([rich('العامل الخارجي يجب أن يكون $(x-h)$ نفسه، وإلا لا تنطبق الصيغة.'),
                                rich('أغلب المفاتيح الرسمية تحذف $|\\,|$؛ اكتبها أنت.')]))
    U.add('paper', '✍️ في ورقة الكويز', p('سطر إكمال المربع، سطر u، ثم الجواب.'))
    U.drill('1', '1447-S2-FE-Q2.6', 'G', 'csch لأن معامل $x^2$ موجب، و $a=2$.',
            first=r'h=-3,\quad d=Q(-3)=9-18+13=4,\quad \sqrt d=2,\quad (x-h)=(x+3)\ \checkmark',
            claims=[('9-18+13', '4'), ('x**2+6*x+13', '(x+3)**2+4')])
    U.drill('2', 'N42-X2-15', 'P', '$h=-3$ و $d=Q(-3)=16$، والبسط 2.')
    U.drill('3', 'N42-X2-16', 'I', 'معامل $x^2$ سالب ⇐ sech، و $h=-1$، و $d=Q(-1)=4$.')
    return U


UNITS_42 = [u_deriv, u_deriv_rules, u_six, u_tanh, u_sech, u_lamda, u_sqrt, u_split, u_invnum, u_square, u_square_lin]

"""المذكرة الكاملة — الدرس 4.2: الدوال الزائدية العكسية (الأيام 1–3)."""
from booklet import sc_lamda, sc_six, sc_square, sc_twins
from booklet_engine import ITEMS, arith, formula, functional, q_tex, same_value, use
from guide_kit import Unit, alg, contrast, final, method, pgref, question, rich, short_steps, steps
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
        'كل دالة زائدية عكسية لها مشتقة جاهزة (جدول التوائم). إذا كان داخلها شيء غير $x$ نسمّيه $u$، '
        "ونضرب المشتقة الجاهزة في مشتقة الداخل $u'$. هذه قاعدة السلسلة نفسها التي استعملتها في 4.1.")))
    U.add('sign', 'العلامة: متى أستخدمه؟', p(rich(
        'السؤال يقول <b>Find dy/dx</b> أو <b>Find the derivative</b>، وفي الدالة $\\sinh^{-1}$ أو $\\cosh^{-1}$ '
        'أو $\\tanh^{-1}$ أو $\\coth^{-1}$ أو $\\operatorname{sech}^{-1}$ أو $\\operatorname{csch}^{-1}$.'))
          + contrast([(r'y=\sinh^{-1}(5x-1)', 'جدول التوائم × $u\'$', 'دالة عكسية: الأس $-1$ اسم وليس قوة'),
                      (r'y=\sinh(5x-1)', 'من 4.1: $\\cosh(5x-1)\\cdot5$', 'دالة عادية، ليست عكسية'),
                      (r'\int\frac{dx}{\sqrt{1+x^{2}}}', 'تكامل (النوع 3)', 'المطلوب تكامل، ليس مشتقة')]))
    for f_, F_, br in [('asinh(x)', 'log(x+sqrt(x**2+1))', None), ('acosh(x)', 'log(x+sqrt(x**2-1))', '1+t'),
                       ('atanh(x)', 'log((1+x)/(1-x))/2', 't/(1+t)'), ('acoth(x)', 'log((x+1)/(x-1))/2', '1+t'),
                       ('asech(x)', 'log((1+sqrt(1-x**2))/x)', 't/(1+t)'), ('acsch(x)', 'log(1/x+sqrt(1+x**2)/Abs(x))', 't')]:
        same_value(f_, F_, 'log form ' + f_, branch=br)
    defs = table(['الدالة', 'تُعرَّف عند', 'الصيغة اللوغاريتمية (مذكرة د. طارق ص57)'], [
        [mi(r'\sinh^{-1}x'), 'كل ' + mi('x'), mi(r'\ln\left(x+\sqrt{x^{2}+1}\right)')],
        [mi(r'\cosh^{-1}x'), mi(r'x\ge1'), mi(r'\ln\left(x+\sqrt{x^{2}-1}\right)')],
        [mi(r'\tanh^{-1}x'), mi(r'|x|<1'), mi(r'\frac12\ln\frac{1+x}{1-x}')],
        [mi(r'\coth^{-1}x'), mi(r'|x|>1'), mi(r'\frac12\ln\frac{x+1}{x-1}')],
        [mi(r'\operatorname{sech}^{-1}x'), mi(r'0<x\le1'), mi(r'\ln\frac{1+\sqrt{1-x^{2}}}{x}')],
        [mi(r'\operatorname{csch}^{-1}x'), mi(r'x\ne0'), mi(r'\ln\left(\frac1x+\frac{\sqrt{1+x^{2}}}{|x|}\right)')]], 'formula compact')
    U.add('note', 'تذكير: من 4.1 ومن تعريف الدوال (مذكرة د. طارق ص56–57)',
          p(rich('مشتقات الدوال الزائدية <b>العادية</b> (sinh و cosh و tanh…) تحتاجها مع العكسية في نفس السؤال. جدولها وشرحها في ')
            + link('P-A3', '📚 أ3 ص ' + pgref('P-A3')) + '.')
          + p('الدوال العكسية الست ومجالها (للمعرفة، لا يُسأل عنها مباشرة في الاختبارات السابقة):') + defs)
    short, memo = sc_twins()
    U.add('short', '⚡ الاختصار: جدول التوائم', short + box_memo(memo))

    it = ITEMS['N42-E1-1']
    ex = question(it, 'U-D1 example 1')
    ex += short_steps(it, [
        ('القانون: صف sinh من جدول التوائم', r"\frac{d}{dx}\sinh^{-1}u=\frac{u'}{\sqrt{u^{2}+1}}", [R('twins sinh')]),
        ("طلّع $u$ من السؤال: هو ما داخل الدالة. ومشتقته: الـ $5x$ تعطي 5، والرقم $-1$ يختفي", r"u=5x-1,\qquad u'=5",
         [('diff(5*x-1,x)', '5')]),
        ("عوّض $u'$ فوق و $u$ تحت في القانون. هذا هو الجواب", r"y'=\frac{5}{\sqrt{(5x-1)^{2}+1}}",
         [('=ANS', '5/sqrt((5*x-1)**2+1)')])], 'U-D1 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r"u=5x-1,\qquad u'=5", [('diff(5*x-1,x)', '5')], 'نسمّي ما داخل الدالة $u$. مشتقة $5x-1$: الـ $x$ تعطي 5، والرقم $-1$ يختفي'),
        ('tex', r'\frac{d}{du}\sinh^{-1}u=\frac{1}{\sqrt{u^{2}+1}}', [('diff(asinh(x),x)', '1/sqrt(x**2+1)')], 'من جدول التوائم (صف sinh)'),
        ('line', '5/sqrt(1+(5*x-1)**2)', "نضرب في $u'=5$ ونرجع $u=5x-1$")], 'U-D1 ex1')
    ex += final(it, 'U-D1 example 1')
    U.add('ex', 'مثال 1 (من مذكرة د. طارق)', ex)

    it = ITEMS['1447-S2-SE-Q1.2']
    ex = question(it, 'U-D1 example 2')
    ex += short_steps(it, [
        ('القانون: صف csch من جدول التوائم (فيه سالب و $|u|$)', r"\frac{d}{dx}\operatorname{csch}^{-1}u=-\frac{u'}{|u|\sqrt{1+u^{2}}}",
         [R('twins csch')]),
        ('طلّع $u$ (ما داخل الدالة) ومشتقته: 1 على ضعف الجذر', r"u=\sqrt{x+2},\qquad u'=\frac{1}{2\sqrt{x+2}}",
         [('diff(sqrt(x+2),x)', '1/(2*sqrt(x+2))')]),
        ('جهّز قطع المقام: الجذر موجب فـ $|u|$ هو نفسه، ومربع الجذر = ما تحته (🧮)', r'|u|=\sqrt{x+2},\qquad 1+u^{2}=1+(x+2)=x+3',
         [('1+sqrt(x+2)**2', 'x+3')]),
        ('عوّض القطع الثلاث في القانون', r"y'=-\frac{\ \frac{1}{2\sqrt{x+2}}\ }{\sqrt{x+2}\,\sqrt{x+3}}",
         [('=ANS', '-(1/(2*sqrt(x+2)))/(sqrt(x+2)*sqrt(x+3))')]),
        ('بسّط: مقام الكسر الصغير ينزل، و $\\sqrt{x+2}\\cdot\\sqrt{x+2}=x+2$ (🧮 تحت)', r"y'=-\frac{1}{2(x+2)\sqrt{x+3}}",
         [('=ANS', '-1/(2*(x+2)*sqrt(x+3))')])], 'U-D1 ex2')
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
        '<b>تنبيه coth⁻¹:</b> مذكرة د. طارق ص58 ومفتاح 1445 كتبا مشتقة coth⁻¹ بإشارة سالبة، والحساب الصحيح (ومفتاح 1446) موجبة '
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
    rules += p(rich('في الاختبارات $\\log$ بدون أساس = أساس 10 (ومذكرة د. طارق تكتب $\\ln$ للطبيعي).'), 'small')
    U.add('short', '⚡ القواعد اللي تحيط بالدالة العكسية', rules)
    it = ITEMS['N42-E1-4']
    ex = question(it, 'U-D2 example')
    ex += short_steps(it, [
        ('القاعدة الكبيرة أولًا: الدالة أسية بأساس 6', r"\frac{d}{dx}6^{u}=6^{u}\cdot\ln6\cdot u'", [R('exp base 6')]),
        ("طلّع $u$: هو الأس كله. ومشتقته من صف cosh في التوائم، وداخله $2x$ مشتقته 2",
         r"u=\cosh^{-1}(2x),\qquad u'=\frac{2}{\sqrt{(2x)^{2}-1}}=\frac{2}{\sqrt{4x^{2}-1}}",
         [('diff(acosh(2*x),x)', '2/sqrt(4*x**2-1)', '1+t')]),
        ("عوّض $u$ و $u'$ في القاعدة", r"y'=6^{\cosh^{-1}(2x)}\cdot\ln6\cdot\frac{2}{\sqrt{4x^{2}-1}}",
         [('=ANS', '6**acosh(2*x)*log(6)*2/sqrt(4*x**2-1)')])], 'U-D2 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r"y=6^{u}\ \Rightarrow\ y'=6^{u}\ln6\cdot u'", [('diff(6**acosh(2*x),x)', '6**acosh(2*x)*log(6)*diff(acosh(2*x),x)')],
         'القاعدة الكبيرة: أسية بأساس 6، و $u=\\cosh^{-1}(2x)$'),
        ('tex', r"u'=\frac{2}{\sqrt{(2x)^{2}-1}}=\frac{2}{\sqrt{4x^{2}-1}}", [('diff(acosh(2*x),x)', '2/sqrt(4*x**2-1)', '1+t')],
         'صف cosh من التوائم مع داخل $2x$ (مشتقته 2)'),
        ('line', '6**acosh(2*x)*log(6)*2/sqrt(4*x**2-1)', "قاعدة الأسية: $6^{u}\\cdot\\ln6\\cdot u'$")], 'U-D2 ex')
    ex += final(it, 'U-D2 example')
    U.add('ex', 'مثال (من مذكرة د. طارق)', ex)
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
          + md(q_tex(use(it2['id'], 'U-D2 trap'))) + final(it2, 'U-D2 trap'))
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
        ('القانون: جذر فيه مجموع مربعين ⇐ صف sinh من الجدول', r'\int\frac{du}{\sqrt{u^{2}+a^{2}}}=\sinh^{-1}\frac{u}{a}+C',
         [R('six sinh')]),
        ('اكتب كل حد كمربع (🧮 تحت)، فتطلع $u$ و $a$؛ = سطر 1 في 🧱', r'4x^{2}+25=(2x)^{2}+5^{2}\ \Rightarrow\ u=2x,\ a=5',
         [('4*x**2+25', '(2*x)**2+5**2')]),
        ('الضبط: مشتقة $u$ هي 2، والبسط $dx$ ما فيه 2 ⇐ نضرب الجواب في $\\frac12$؛ = السطران 2–3 في 🧱',
         r'du=2\,dx\ \Rightarrow\ dx=\frac12\,du', [('diff(2*x,x)', '2')]),
        ('عوّض $u=2x$ و $a=5$ في القانون، واضرب في $\\frac12$', r'\frac12\sinh^{-1}\frac{2x}{5}+C', [('=ANS', 'asinh(2*x/5)/2')])],
        'U-I1 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'4x^{2}+25=(2x)^{2}+5^{2}', [('4*x**2+25', '(2*x)**2+5**2')], 'نكتب كل حد كمربع (🧮 تحت)'),
        ('sub', '2*x', '2', 'نسمّي $u=2x$'),
        ('tex', r'dx=\frac{du}{2}\ \Rightarrow\ \int\frac{dx}{\sqrt{(2x)^{2}+5^{2}}}=\frac12\int\frac{du}{\sqrt{u^{2}+5^{2}}}',
         [('1/sqrt((2*x)**2+5**2)', 'Rational(1,2)*diff(2*x,x)/sqrt((2*x)**2+5**2)')], 'نعوّض $dx$ فيظهر $\\frac12$'),
        ('line', 'asinh(2*x/5)/2', 'صف sinh: $\\sinh^{-1}\\frac{u}{a}$، ثم نرجع $u=2x$')], 'U-I1 ex1')
    ex += final(it, 'U-I1 example 1')
    U.add('ex', 'مثال 1 (من مذكرة د. طارق)', ex)
    U.raw(alg('squares', 'كتابة الحد كمربع', [
        (r'4x^{2}=(2x)^{2}', [('4*x**2', '(2*x)**2')], 'جذر المعامل، ونصف الأس:'),
        (r'16x^{6}=(4x^{3})^{2}', [('16*x**6', '(4*x**3)**2')], 'جذر 16 = 4، ونصف 6 = 3:'),
        (r'25=5^{2},\qquad 9=3^{2}', [('5**2', '25'), ('3**2', '9')], 'والأرقام:'),
        (r'e^{6x}=\left(e^{3x}\right)^{2}', [('exp(6*x)', 'exp(3*x)**2')], 'ومع الأسية نصف الأس:')]))
    it = ITEMS['N42-X2-01']
    ex = question(it, 'U-I1 example 2')
    ex += short_steps(it, [
        ('القانون: قاعدة الضبط مع صف sinh', r'\int\frac{c\,x^{n-1}}{\sqrt{(kx^{n})^{2}+a^{2}}}dx=\frac{c}{nk}\sinh^{-1}\frac{kx^{n}}{a}+C',
         [R('adjust')]),
        ('اكتب ما تحت الجذر كمربعين (🧮 كتابة الحد كمربع)', r'16x^{6}=(4x^{3})^{2},\qquad 9=3^{2}',
         [('16*x**6', '(4*x**3)**2'), ('3**2', '9')]),
        ('طلّع الأرقام: $u=kx^n=4x^3$، والبسط $5x^2=c\\,x^{n-1}$', r'k=4,\quad n=3,\quad a=3,\quad c=5',
         [('5*x**(3-1)', '5*x**2'), ('(4*x**3)**2', '16*x**6')]),
        ('احسب المعامل؛ = $\\frac{5}{12}$ في السطر 2 من 🧱', r'\frac{c}{nk}=\frac{5}{3\cdot4}=\frac{5}{12}', [('Rational(5,3*4)', 'Rational(5,12)')]),
        ('عوّض في القانون', r'\frac{5}{12}\sinh^{-1}\frac{4x^{3}}{3}+C', [('=ANS', '5*asinh(4*x**3/3)/12')])], 'U-I1 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('sub', '4*x**3', '12*x**2', 'نسمّي $u=4x^3$'),
        ('tex', r'x^{2}dx=\frac{du}{12}\ \Rightarrow\ 5\int\frac{x^{2}\,dx}{\sqrt{9+16x^{6}}}=\frac{5}{12}\int\frac{du}{\sqrt{u^{2}+3^{2}}}',
         [('5*x**2/sqrt(9+16*x**6)', 'Rational(5,12)*diff(4*x**3,x)/sqrt((4*x**3)**2+3**2)')], 'البسط $5x^2dx=\\frac{5}{12}du$'),
        ('line', '5*asinh(4*x**3/3)/12', 'صف sinh ونرجع $u$')], 'U-I1 ex2')
    ex += final(it, 'U-I1 example 2')
    U.add('ex', 'مثال 2: البسط مضاعف للمشتقة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('cosh⁻¹ يصح بشرط $u>a$ فقط، كما تشترط مذكرة د. طارق.'),
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
        ('القانون: رقم ناقص مربع بلا جذر، و $|u|<a$ ⇐ صف tanh', r'\int\frac{du}{a^{2}-u^{2}}=\frac1a\tanh^{-1}\frac{u}{a}+C',
         [R('six tanh')]),
        ('اكتب المقام كمربعين، فتطلع $u$ و $a$؛ = سطر 1 في 🧱', r'25-e^{2x}=5^{2}-\left(e^{x}\right)^{2}\ \Rightarrow\ u=e^{x},\ a=5',
         [('25-exp(2*x)', '5**2-exp(x)**2')]),
        ('البسط $e^x\\,dx$ هو $du$ بالضبط، فلا ضبط ولا معامل', r'du=e^{x}dx', [('diff(exp(x),x)', 'exp(x)')]),
        ('قارن $u$ مع $a$: مذكرة د. طارق تأخذ $e^x<5$ (أي $x<\\ln5$) ⇐ $|u|<a$ ⇐ tanh', r'e^{x}<5\iff x<\ln5',
         [('exp(log(5))', '5')]),
        ('عوّض $u=e^x$ و $a=5$ في القانون', r'\frac15\tanh^{-1}\frac{e^{x}}{5}+C', [('=ANS', 'atanh(exp(x)/5)/5')])], 'U-I2 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'25-e^{2x}=5^{2}-\left(e^{x}\right)^{2}', [('25-exp(2*x)', '5**2-exp(x)**2')], 'نكتب كمربعين (🧮 كتابة الحد كمربع)'),
        ('sub', 'exp(x)', 'exp(x)', 'نسمّي $u=e^x$، ومشتقتها في البسط'),
        ('tex', r'=\int\frac{du}{5^{2}-u^{2}}', [('exp(x)/(25-exp(2*x))', 'diff(exp(x),x)/(5**2-exp(x)**2)')], 'التكامل بدلالة $u$'),
        ('line', 'atanh(exp(x)/5)/5', 'مذكرة د. طارق تأخذ الجهة $e^x<5$ ⇐ tanh⁻¹، و $\\frac1a=\\frac15$')], 'U-I2 ex1')
    ex += final(it, 'U-I2 example 1') + p(rich('إذا كان $e^x>5$ يصير الجواب $\\frac15\\coth^{-1}\\frac{e^x}{5}$.'), 'small')
    U.add('ex', 'مثال 1 (من مذكرة د. طارق)', ex)
    it = ITEMS['N42-X2-06']
    ex = question(it, 'U-I2 example 2')
    ex += short_steps(it, [
        ('القانون: نفس الشكل، لكن إذا $|u|>a$ ⇐ صف coth', r'\int\frac{du}{a^{2}-u^{2}}=\frac1a\coth^{-1}\frac{u}{a}+C',
         [R('six coth')]),
        ('اكتب المقام كمربعين، فتطلع $u$ و $a$', r'4-25\cosh^{2}x=2^{2}-(5\cosh x)^{2}\ \Rightarrow\ u=5\cosh x,\ a=2',
         [('4-25*cosh(x)**2', '2**2-(5*cosh(x))**2')]),
        ('الضبط: مشتقة $u$ فيها 5 والبسط $\\sinh x$ بدونها ⇐ نضرب في $\\frac15$', r'du=5\sinh x\,dx\ \Rightarrow\ \sinh x\,dx=\frac{du}{5}',
         [('diff(5*cosh(x),x)', '5*sinh(x)')]),
        ('قارن: أصغر قيمة لـ $\\cosh x$ هي 1 ⇐ $u\\ge5>2$ دائمًا ⇐ coth (= سطر 4 في 🧱)', r'u=5\cosh x\ge5\cosh0=5>2=a',
         [('5*cosh(0)', '5')]),
        ('عوّض في القانون واضرب في $\\frac15$: $\\frac15\\cdot\\frac12=\\frac{1}{10}$',
         r'\frac15\cdot\frac12\coth^{-1}\frac{5\cosh x}{2}=\frac{1}{10}\coth^{-1}\frac{5\cosh x}{2}+C',
         [('Rational(1,5)*Rational(1,2)', 'Rational(1,10)'), ('=ANS', 'acoth(5*cosh(x)/2)/10')])], 'U-I2 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'4-25\cosh^{2}x=2^{2}-(5\cosh x)^{2}', [('4-25*cosh(x)**2', '2**2-(5*cosh(x))**2')], 'مربعان'),
        ('sub', '5*cosh(x)', '5*sinh(x)', 'نسمّي $u=5\\cosh x$'),
        ('tex', r'\begin{array}{l}\sinh x\,dx=\frac{du}{5}\\[7pt] \displaystyle\int\frac{\sinh x\,dx}{4-25\cosh^{2}x}=\frac15\int\frac{du}{2^{2}-u^{2}}\end{array}',
         [('sinh(x)/(4-25*cosh(x)**2)', 'Rational(1,5)*diff(5*cosh(x),x)/(2**2-(5*cosh(x))**2)')], 'البسط $\\sinh x\\,dx$'),
        ('tex', r'u=5\cosh x\ge5>2=a', [], 'لأن $\\cosh x\\ge1$ دائمًا ⇐ $|u|>a$ ⇐ coth⁻¹'),
        ('line', 'acoth(5*cosh(x)/2)/10', '$\\frac15\\cdot\\frac12\\coth^{-1}\\frac{u}{2}$')], 'U-I2 ex2')
    ex += final(it, 'U-I2 example 2')
    U.add('ex', 'مثال 2: لماذا coth هنا؟ (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تختار tanh تلقائيًا: افحص $|u|$ و $a$.'),
                                'مذكرة د. طارق ص60 كتبت صيغة coth⁻¹ بإشارة سالبة؛ الحساب يعطي موجبة (تنبيه النوع 1).']))
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
        ('القانون: $u$ خارج الجذر، وداخل الجذر ناقص ⇐ صف sech', r'\int\frac{du}{u\sqrt{a^{2}-u^{2}}}=-\frac1a\operatorname{sech}^{-1}\frac{|u|}{a}+C',
         [R('six sech')]),
        ('اضرب فوق وتحت في $x$ حتى يصير خارج الجذر $x^2$ (🧮 تحت)؛ = سطر 1 في 🧱',
         r'\frac{1}{x\sqrt{16-x^{4}}}=\frac{x}{x^{2}\sqrt{4^{2}-(x^{2})^{2}}}', [('1/(x*sqrt(16-x**4))', 'x/(x**2*sqrt(4**2-(x**2)**2))')]),
        ('طلّع $u$ و $a$. والبسط $x\\,dx$ نصف $du$ ⇐ نضرب في $\\frac12$', r'u=x^{2},\quad du=2x\,dx\ \Rightarrow\ x\,dx=\frac{du}{2},\quad a=4',
         [('diff(x**2,x)', '2*x'), ('4**2', '16')]),
        ('عوّض في القانون، و $|x^2|=x^2$', r'\frac12\cdot\left(-\frac14\right)\operatorname{sech}^{-1}\frac{x^{2}}{4}',
         [('=ANS', 'Rational(1,2)*(-Rational(1,4))*asech(x**2/4)')]),
        ('اضرب الكسرين: $\\frac12\\cdot\\left(-\\frac14\\right)=-\\frac18$', r'=-\frac18\operatorname{sech}^{-1}\frac{x^{2}}{4}+C',
         [('Rational(1,2)*(-Rational(1,4))', '-Rational(1,8)'), ('=ANS', '-asech(x**2/4)/8')])], 'U-I3 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\frac{1}{x\sqrt{16-x^{4}}}=\frac{x}{x^{2}\sqrt{4^{2}-(x^{2})^{2}}}',
         [('1/(x*sqrt(16-x**4))', 'x/(x**2*sqrt(4**2-(x**2)**2))')], 'نضرب فوق وتحت في $x$ (🧮 تحت)'),
        ('sub', 'x**2', '2*x', 'نسمّي $u=x^2$'),
        ('tex', r'\begin{array}{l}x\,dx=\frac{du}{2}\\[7pt] \displaystyle\int\frac{x\,dx}{x^{2}\sqrt{16-x^{4}}}=\frac12\int\frac{du}{u\sqrt{4^{2}-u^{2}}}\end{array}',
         [('x/(x**2*sqrt(4**2-(x**2)**2))', 'Rational(1,2)*diff(x**2,x)/(x**2*sqrt(4**2-(x**2)**2))')], 'التكامل بدلالة $u$'),
        ('line', '-asech(x**2/4)/8', 'صف sech: $\\frac12\\cdot\\left(-\\frac14\\right)\\operatorname{sech}^{-1}\\frac{|u|}{4}$، و $|x^2|=x^2$')],
        'U-I3 ex')
    ex += final(it, 'U-I3 example')
    U.add('ex', 'مثال (من مذكرة د. طارق)', ex)
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
        ('القانون: أسية تحت الجذر مع $+$ ⇐ صف csch في جدول لامدا',
         r'\int\frac{dx}{\sqrt{b^{2\lambda x}+a^{2}}}=-\frac{1}{a\lambda\ln b}\operatorname{csch}^{-1}\frac{b^{\lambda x}}{a}+C', [R('lamda csch')]),
        ('اكتب الأسية كمربع: نصف الأس (🧮 كتابة الحد كمربع)', r'e^{6x}=\left(e^{3x}\right)^{2}', [('exp(6*x)', 'exp(3*x)**2')]),
        ('طلّع الأرقام: الأساس $e$، و $b^{\\lambda x}=e^{3x}$، و $1=1^2$', r'b=e,\qquad \lambda=3,\qquad a=1', [('exp(2*3*x)', 'exp(6*x)')]),
        ('احسب المعامل؛ تذكّر $\\ln e=1$', r'-\frac{1}{a\lambda\ln b}=-\frac{1}{1\cdot3\cdot\ln e}=-\frac13', [('-1/(1*3*log(E))', '-Rational(1,3)')]),
        ('عوّض في القانون، و $\\frac{e^{3x}}{1}=e^{3x}$؛ نفس جواب 🧱 (الضرب في $e^{3x}$)', r'-\frac13\operatorname{csch}^{-1}e^{3x}+C',
         [('=ANS', '-acsch(exp(3*x))/3')])], 'U-I4 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\frac{1}{\sqrt{e^{6x}+1}}=\frac{e^{3x}}{e^{3x}\sqrt{(e^{3x})^{2}+1}}',
         [('1/sqrt(exp(6*x)+1)', 'exp(3*x)/(exp(3*x)*sqrt(exp(3*x)**2+1))')], 'نضرب فوق وتحت في $e^{3x}$'),
        ('sub', 'exp(3*x)', '3*exp(3*x)', 'نسمّي $u=e^{3x}$'),
        ('tex', r'\begin{array}{l}e^{3x}dx=\frac{du}{3}\\[7pt] \displaystyle\int\frac{e^{3x}dx}{e^{3x}\sqrt{e^{6x}+1}}=\frac13\int\frac{du}{u\sqrt{u^{2}+1}}\end{array}',
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
        ('القانون: $\\sqrt x$ في المقام × جذر فيه $x$ وحدها', r'\int\frac{dx}{\sqrt{x}\sqrt{a^{2}+x}}=2\sinh^{-1}\frac{\sqrt{x}}{a}+C',
         [R('sqrt sinh')]),
        ('طلّع $a$: الرقم تحت الجذر هو $a^2$', r'a^{2}=4\ \Rightarrow\ a=2', [('2**2', '4')]),
        ('عوّض $a=2$. الـ 2 قدّام جات من $\\frac{dx}{\\sqrt x}=2\\,du$ (السطر 2 في 🧱)', r'2\sinh^{-1}\frac{\sqrt{x}}{2}+C',
         [('=ANS', '2*asinh(sqrt(x)/2)')])], 'U-I5 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('sub', 'sqrt(x)', '1/(2*sqrt(x))', 'نسمّي $u=\\sqrt x$'),
        ('tex', r'\frac{dx}{\sqrt{x}}=2\,du,\qquad 4+x=2^{2}+u^{2}', [('4+sqrt(x)**2', '4+x')], 'لأن $u^2=x$ (🧮 الجذر في نفسه)'),
        ('tex', r'=2\int\frac{du}{\sqrt{u^{2}+2^{2}}}', [('1/(sqrt(x)*sqrt(4+x))', '2*diff(sqrt(x),x)/sqrt(sqrt(x)**2+2**2)')], 'التكامل بدلالة $u$'),
        ('line', '2*asinh(sqrt(x)/2)', 'صف sinh ونرجع $u=\\sqrt x$')], 'U-I5 ex')
    ex += final(it, 'U-I5 example')
    U.add('ex', 'مثال (من مذكرة د. طارق)', ex)
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
        ('افصل الكسر: كل حد من البسط على المقام نفسه (انتبه للإشارة)',
         r'\frac{x-2}{\sqrt{25+x^{2}}}=\frac{x}{\sqrt{25+x^{2}}}-\frac{2}{\sqrt{25+x^{2}}}', [('(x-2)/sqrt(25+x**2)', 'x/sqrt(25+x**2)-2/sqrt(25+x**2)')]),
        ('قانون جزء $x$ من جدول الاختصار (يطلع من تعويض $w=c+x^2$)', r'\int\frac{x\,dx}{\sqrt{c+x^{2}}}=\sqrt{c+x^{2}}', [R('micro +')]),
        ('جزء $x$ مع $c=25$', r'\int\frac{x\,dx}{\sqrt{25+x^{2}}}=\sqrt{25+x^{2}}', [('diff(sqrt(25+x**2),x)', 'x/sqrt(25+x**2)')]),
        ('جزء الرقم: صف sinh مع $a=5$، والـ 2 تطلع قدّام', r'\int\frac{2\,dx}{\sqrt{x^{2}+5^{2}}}=2\sinh^{-1}\frac{x}{5}',
         [('diff(2*asinh(x/5),x)', '2/sqrt(x**2+25)')]),
        ('اطرح الجزأين كما في سطر الفصل', r'\sqrt{25+x^{2}}-2\sinh^{-1}\frac{x}{5}+C', [('=ANS', 'sqrt(25+x**2)-2*asinh(x/5)')])], 'U-I6 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\frac{x-2}{\sqrt{25+x^{2}}}=\frac{x}{\sqrt{25+x^{2}}}-\frac{2}{\sqrt{25+x^{2}}}',
         [('(x-2)/sqrt(25+x**2)', 'x/sqrt(25+x**2)-2/sqrt(25+x**2)')], 'نفصل الكسر (البسط على المقام لكل حد)'),
        ('line', 'sqrt(25+x**2)-Integral(2/sqrt(25+x**2),x)', 'الجزء الأول: $\\int\\frac{x}{\\sqrt{c+x^2}}dx=\\sqrt{c+x^2}$'),
        ('line', 'sqrt(25+x**2)-2*asinh(x/5)', 'الجزء الثاني: صف sinh مع $a=5$')], 'U-I6 ex')
    ex += final(it, 'U-I6 example')
    U.add('ex', 'مثال (من مذكرة د. طارق)', ex)
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
    U.add('sign', 'العلامة', contrast([(r'\int\frac{\cosh^{-1}x}{\sqrt{x^{2}-1}}dx', 'تعويض $u=\\cosh^{-1}x$', 'مشتقة $\\cosh^{-1}x$ (وهي $\\frac{1}{\\sqrt{x^2-1}}$) موجودة في السؤال'),
                                       (r'\int\cosh^{-1}x\,dx', 'تجزئة (اليوم 4)', 'الدالة وحدها بلا مشتقتها')]))
    U.add('short', '⚡ الاختصار', md(r'\int f^{-1}\cdot\left(f^{-1}\right)'"'"r'\,dx=\frac{\left(f^{-1}\right)^{2}}{2}+C')
          + box_memo('الدالة × مشتقتها ⇐ مربع الدالة على 2.'))
    functional(lambda: s.diff(s.Function('g')(x) ** 2 / 2, x) - s.Function('g')(x) * s.diff(s.Function('g')(x), x), 'g g\' rule')
    it = ITEMS['N42-X2-09']
    ex = question(it, 'U-I7 example')
    ex += short_steps(it, [
        ('القانون: الدالة × مشتقتها ⇐ مربعها على 2', r'\int f^{-1}\cdot\left(f^{-1}\right)'"'"r'\,dx=\frac{\left(f^{-1}\right)^{2}}{2}+C',
         [R('g gprime')]),
        ('تأكد أن العامل $\\frac{1}{\\sqrt{x^2-1}}$ هو مشتقة الدالة (صف cosh في التوائم)',
         r'f^{-1}=\cosh^{-1}x,\qquad \left(\cosh^{-1}x\right)'"'"r'=\frac{1}{\sqrt{x^{2}-1}}', [('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t')]),
        ('عوّض في القانون؛ = $\\int u\\,du=\\frac{u^2}{2}$ في 🧱', r'\frac{\left(\cosh^{-1}x\right)^{2}}{2}+C', [('=ANS', 'acosh(x)**2/2')])], 'U-I7 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('sub', 'acosh(x)', '1/sqrt(x**2-1)', 'مشتقة $\\cosh^{-1}x$ موجودة في المقام', 'u', '1+t'),
        ('tex', r'=\int u\,du=\frac{u^{2}}{2}', [('integrate(x,x)', 'x**2/2')], 'قاعدة القوة')], 'U-I7 ex')
    ex += final(it, 'U-I7 example')
    U.add('ex', 'مثال (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', p(rich('$(\\cosh^{-1}x)^2$ تعني مربع الدالة، وليست $\\cosh^{-1}(x^2)$.')))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر $u$ و $du$، ثم $\\int u\\,du$، ثم الجواب.')))
    U.drill('1', 'G-02', 'G', '$\\int u^2du=\\frac{u^3}{3}$.', first=r'u=\sinh^{-1}x,\quad du=\frac{dx}{\sqrt{1+x^{2}}}',
            claims=[('diff(asinh(x),x)', '1/sqrt(1+x**2)')])
    U.drill('2', 'G-03', 'I', 'مشتقة $\\tanh^{-1}x$ هي $\\frac{1}{1-x^2}$.')
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
        'زائد يعني قانون $\\sinh^{-1}$. وناقص يعني قانون $\\cosh^{-1}$. ثم نرجع $u$.']) + laws)
    it = ITEMS['1446-S1-SE-Q2.2']
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
    sh = (p('بدل ما تكمّل المربع بالخطوات، فيه طريقة أسرع توصلك لنفس الشكل:')
          + method(['<b>المركز</b> = سالب معامل $x$ ÷ (2 × معامل $x^2$).',
                    '<b>الباقي</b> = عوّض المركز مكان $x$ في اللي تحت الجذر.',
                    'اللي تحت الجذر = ($x$ ناقص المركز)² + الباقي.',
                    'الباقي موجب يعني $\\sinh^{-1}$، والباقي سالب يعني $\\cosh^{-1}$.']))
    sh += short_steps(it, [
        ('المركز: معامل $x$ هو 6، ومعامل $x^2$ هو 1.', r'-\frac{6}{2\cdot1}=-3', [('-Rational(6,2*1)', '-3')]),
        ('الباقي: نعوّض $-3$ مكان $x$ تحت الجذر.', r'(-3)^{2}+6(-3)-16=9-18-16=-25', [('(-3)**2+6*(-3)-16', '-25')]),
        ('نكتب ($x$ ناقص المركز)² + الباقي. نفس اللي طلع في 🧱.', r'x^{2}+6x-16=(x+3)^{2}-5^{2}', [('x**2+6*x-16', '(x+3)**2-5**2')]),
        ('الباقي سالب، يعني القانون $\\cosh^{-1}$ مع $a=5$.', r'3\cosh^{-1}\frac{x+3}{5}+C', [('=ANS', '3*acosh((x+3)/5)')])], 'U-I8 ex1')
    U.add('short', '⚡ الطريقة السريعة: المركز والباقي', sh)
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
            sol_rows=[('sub', 'x-2', '1', 'نسمّي القوس $u$، و $du=dx$.'),
                      ('tex', r'\int\frac{dx}{\sqrt{x^{2}-4x}}=\int\frac{du}{\sqrt{u^{2}-2^{2}}}', [('1/sqrt((x-2)**2-2**2)', '1/sqrt(x**2-4*x)')],
                       'نعوّض. صار مربع ناقص رقم.'),
                      ('line', 'acosh((x-2)/2)', 'القانون: $\\int\\frac{du}{\\sqrt{u^2-a^2}}=\\cosh^{-1}\\frac ua$، و $a=2$. ثم نرجع $u=x-2$.')])
    U.drill('2', 'N42-X2-14', 'P', 'نص 2 هو 1، ومربعه 1.',
            sol_rows=[('tex', r'x^{2}+2x+10=\left(x^{2}+2x+1\right)-1+10', [('x**2+2*x+10', 'x**2+2*x+1-1+10')],
                       'نكمّل المربع. نص 2 هو 1، ومربعه 1. نضيفه ونطرحه.'),
                      ('tex', r'=(x+1)^{2}+3^{2}', [('x**2+2*x+1-1+10', '(x+1)**2+3**2')], 'أول ثلاثة حدود $(x+1)^2$. والأرقام: $-1+10=9=3^2$.'),
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
        '(قوس)² + رقم يعني $\\operatorname{csch}^{-1}$. ورقم − (قوس)² يعني $\\operatorname{sech}^{-1}$. ثم نرجع $u$.']) + laws)
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
    sh = (p('نفس المركز والباقي من النوع 10. وفيه قاعدة زيادة: <b>الرقم قدّام الجواب</b> = سالب رقم البسط ÷ جذر الباقي.')
          + short_steps(it, [
              ('المركز: معامل $x$ هو 2، ومعامل $x^2$ هو $-1$.', r'-\frac{2}{2\cdot(-1)}=1', [('-Rational(2,2*(-1))', '1')]),
              ('الباقي: نعوّض 1 مكان $x$ تحت الجذر.', r'-1+2+3=4=2^{2}', [('-1**2+2*1+3', '4')]),
              ('نكتب الباقي ناقص ($x$ ناقص المركز)². والقوس برّا الجذر $(x-1)$ ✓', r'-x^{2}+2x+3=2^{2}-(x-1)^{2}',
               [('-x**2+2*x+3', '2**2-(x-1)**2')]),
              ('الرقم قدّام الجواب: سالب 1 ÷ جذر 4. ومعامل $x^2$ سالب يعني $\\operatorname{sech}^{-1}$.',
               r'-\frac{1}{\sqrt4}\operatorname{sech}^{-1}\frac{|x-1|}{2}+C=-\frac12\operatorname{sech}^{-1}\frac{|x-1|}{2}+C',
               [('-1/sqrt(4)', '-Rational(1,2)'), ('=ANS', '-asech(Abs(x-1)/2)/2')])], 'U-I9 ex'))
    U.add('short', '⚡ الطريقة السريعة: المركز والباقي', sh)
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
                      ('sub', 'x+3', '1', 'القوس برّا الجذر نفس القوس. نسمّيه $u$.'),
                      ('tex', r'=2\int\frac{du}{u\sqrt{u^{2}+4^{2}}}', [('2/((x+3)*sqrt(x**2+6*x+25))', '2*diff(x+3,x)/((x+3)*sqrt((x+3)**2+4**2))')],
                       'نعوّض، والرقم 2 يطلع برّا التكامل.'),
                      ('line', '-acsch(Abs(x+3)/4)/2', 'القانون مع $a=4$: $2\\cdot\\left(-\\frac14\\right)=-\\frac12$. ثم نرجع $u$.')])
    U.drill('3', 'N42-X2-16', 'I', 'معامل $x^2$ سالب، فنطلّع السالب أول.',
            sol_rows=[('tex', r'3-x^{2}-2x=-\left(x^{2}+2x\right)+3', [('3-x**2-2*x', '-(x**2+2*x)+3')], 'نطلّع السالب من حدّي $x$.'),
                      ('tex', r'=-\left[(x+1)^{2}-1\right]+3=4-(x+1)^{2}', [('-((x+1)**2-1)+3', '4-(x+1)**2')],
                       'نكمّل المربع داخل القوس: نص 2 هو 1. ونرجّع السالب.'),
                      ('sub', 'x+1', '1', 'القوس برّا الجذر $(x+1)$ نفس القوس. نسمّيه $u$.'),
                      ('tex', r'=3\int\frac{du}{u\sqrt{2^{2}-u^{2}}}', [('3/((x+1)*sqrt(3-x**2-2*x))', '3*diff(x+1,x)/((x+1)*sqrt(2**2-(x+1)**2))')],
                       'نعوّض، والرقم 3 يطلع برّا.'),
                      ('line', '-3*asech(Abs(x+1)/2)/2', 'رقم ناقص مربع: القانون $\\operatorname{sech}^{-1}$ مع $a=2$. $3\\cdot\\left(-\\frac12\\right)=-\\frac32$.')])
    return U


UNITS_42 = [u_deriv, u_deriv_rules, u_six, u_tanh, u_sech, u_lamda, u_sqrt, u_split, u_invnum, u_square, u_square_lin]

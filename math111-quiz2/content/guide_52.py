"""المذكرة الكاملة — الدرس 5.2: التكاملات المثلثية (اليومان 5–6)."""
from booklet import sc_even, sc_prod, sc_reduce
from booklet_engine import ITEMS, arith, same_value
from guide_kit import Unit, alg, contrast, final, question, rich, short_steps, steps
from guide_rules import R
from guide_42 import box_memo
from html_kit import md, mi, p, table, ul

# the normal method of types 22, 23, 25, 26 and 28: which piece is kept for du, which u, how the rest is converted
METHOD_ROWS = {
    'cos': [mi(r'\cos^{\text{odd}}x'), mi(r'\cos x\,dx'), mi(r'u=\sin x'), mi(r'\cos^{2}x=1-\sin^{2}x')],
    'sin': [mi(r'\sin^{\text{odd}}x'), mi(r'\sin x\,dx=-du'), mi(r'u=\cos x'), mi(r'\sin^{2}x=1-\cos^{2}x')],
    'sec': [mi(r'\sec^{\text{even}}x'), mi(r'\sec^{2}x\,dx'), mi(r'u=\tan x'), mi(r'\sec^{2}x=1+\tan^{2}x')],
    'tan': [mi(r'\tan^{\text{odd}}x') + ' ومعه sec', mi(r'\sec x\tan x\,dx'), mi(r'u=\sec x'), mi(r'\tan^{2}x=\sec^{2}x-1')],
    'csc': [mi(r'\csc^{\text{even}}x'), mi(r'\csc^{2}x\,dx=-du'), mi(r'u=\cot x'), mi(r'\csc^{2}x=1+\cot^{2}x')],
    'cot': [mi(r'\cot^{\text{odd}}x') + ' ومعه csc', mi(r'\csc x\cot x\,dx=-du'), mi(r'u=\csc x'), mi(r'\cot^{2}x=\csc^{2}x-1')]}
METHOD_STEPS = ['<b>احجز</b> قطعة المشتقة (العمود الثاني): هي اللي تصير $du$.',
                '<b>حوّل</b> الباقي (قوته زوجية) بالمتطابقة في العمود الأخير.',
                '<b>عوّض</b> $u$ و $du$، وانتبه للسالب إذا كان $du$ بالسالب.',
                '<b>فك القوس</b> ووزّع (🧮)، ثم <b>كامل</b> كل حد (زِد الأس 1 واقسم عليه)، و<b>ارجع</b> لـ $x$.']


def method_table(keys):
    """The rows of the method table, every identity and derivative in it checked."""
    arith('', [('cos(x)**2', '1-sin(x)**2'), ('sin(x)**2', '1-cos(x)**2'), ('sec(x)**2', '1+tan(x)**2'),
               ('tan(x)**2', 'sec(x)**2-1'), ('csc(x)**2', '1+cot(x)**2'), ('cot(x)**2', 'csc(x)**2-1'),
               ('diff(sin(x),x)', 'cos(x)'), ('diff(cos(x),x)', '-sin(x)'), ('diff(tan(x),x)', 'sec(x)**2'),
               ('diff(sec(x),x)', 'sec(x)*tan(x)'), ('diff(cot(x),x)', '-csc(x)**2'), ('diff(csc(x),x)', '-csc(x)*cot(x)')], 'method table')
    return table(['إذا وجدت', 'احجز (تصير du)', 'خذ', 'والباقي يتحوّل بـ'], [METHOD_ROWS[k] for k in keys], 'formula')


def method_box(keys, memo):
    return ('<ol class="method">' + ''.join('<li>%s</li>' % rich(t) for t in METHOD_STEPS) + '</ol>'
            + method_table(keys) + box_memo(rich(memo)))


def sc_method():
    """For the formula sheet: the four steps and the whole table."""
    return '<ol class="method">' + ''.join('<li>%s</li>' % rich(t) for t in METHOD_STEPS) + '</ol>' + method_table(list(METHOD_ROWS)), ''


# ---------------------------------------------------------------- 22
def u_odd_alone():
    U = Unit('U-T1', 'قوة فردية لـ sin أو cos وحدها', '5.2', 'ص67–68، مثال 1', 5)
    U.add('idea', 'الفكرة', p(rich('احجز واحدًا من القوة الفردية (هو مشتقة الدالة الأخرى)، وحوّل الباقي (قوة زوجية) بالمتطابقة '
                                   '$\\sin^2x+\\cos^2x=1$. فيصير التكامل كثيرة حدود في $u$.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\cos^3x\\,dx$ أو $\\int\\sin^5x\\,dx$: قوة <b>فردية</b> لدالة واحدة.'))
          + contrast([(r'\int\cos^{3}x\,dx', 'احجز $\\cos x$، $u=\\sin x$', 'الأس فردي'),
                      (r'\int\cos^{2}x\,dx', 'نصف الزاوية (النوع 24)', 'الأس زوجي')]))
    U.add('short', '🧭 الطريقة: 4 خطوات ثابتة', method_box(['cos', 'sin'], 'احجز، حوّل، عوّض، فك وكامل. نفس الخطوات في الأنواع 23 و25 و26 و28.'))
    it = ITEMS['N52-E1-1']
    ex = question(it, 'U-T1 example')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\cos^{3}x=\cos^{2}x\cdot\cos x', [('cos(x)**3', 'cos(x)**2*cos(x)')],
         '<b>احجز</b> $\\cos x$: أس cos فردي، و $\\cos x\\,dx$ هي $du$ لما $u=\\sin x$'),
        ('tex', r'\cos^{2}x=1-\sin^{2}x\ \Rightarrow\ \cos^{3}x=(1-\sin^{2}x)\cos x', [('cos(x)**3', '(1-sin(x)**2)*cos(x)')],
         '<b>حوّل</b> الباقي $\\cos^2x$ (🧮 متطابقات فيثاغورس تحت)'),
        ('sub', 'sin(x)', 'cos(x)', '<b>عوّض</b>: $u=\\sin x$، و $du=\\cos x\\,dx$'),
        ('tex', r'\int\cos^{3}x\,dx=\int(1-u^{2})\,du', [('cos(x)**3', '(1-sin(x)**2)*diff(sin(x),x)')], 'التكامل كله بدلالة $u$'),
        ('tex', r'=u-\frac{u^{3}}{3}', [('integrate(1-u**2,u)', 'u-u**3/3')], '<b>كامل</b> كل حد: $\\int1\\,du=u$ و $\\int u^2du=\\frac{u^3}{3}$'),
        ('line', 'sin(x)-sin(x)**3/3', '<b>ارجع</b> $u=\\sin x$')], 'U-T1 ex')
    ex += final(it, 'U-T1 example')
    U.add('ex', 'مثال (من مذكرة د. طارق)', ex)
    U.raw(alg('trig-pyth', 'متطابقات فيثاغورس', [
        (r'\sin^{2}x+\cos^{2}x=1', [('sin(x)**2+cos(x)**2', '1')], 'الأساس:'),
        (r'\cos^{2}x=1-\sin^{2}x,\qquad \sin^{2}x=1-\cos^{2}x', [('cos(x)**2', '1-sin(x)**2')], 'ننقل حدًا للطرف الثاني:'),
        (r'\sec^{2}x=1+\tan^{2}x,\qquad \csc^{2}x=1+\cot^{2}x', [('sec(x)**2', '1+tan(x)**2'), ('csc(x)**2', '1+cot(x)**2')],
         'ونظيرتاها (تحتاجهما مع tan و cot):')]))
    U.raw(alg('expand-sq', 'فك مربع قوس', [
        (r'(1-u^{2})^{2}=1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')], '$(a-b)^2=a^2-2ab+b^2$ (تحتاجه في التمرين 2):'),
        (r'(1+u^{2})^{2}=1+2u^{2}+u^{4}', [('(1+u**2)**2', '1+2*u**2+u**4')], '$(a+b)^2=a^2+2ab+b^2$:'),
        (r'(u^{2}-1)^{2}=u^{4}-2u^{2}+1', [('(u**2-1)**2', 'u**4-2*u**2+1')], 'والترتيب لا يغيّر شيئًا:')]))
    U.add('trap', '⚠️ الفخ', p(rich('مع $\\sin$: $du=-\\sin x\\,dx$، فتظهر إشارة سالبة أمام التكامل كله.')))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر الحجز والتحويل، سطر $u$ و $du$، ثم الجواب.')))
    U.drill('1', 'G-09', 'G', 'انتبه: $\\sin x\\,dx=-du$.',
            first=r'\sin^{3}x=(1-\cos^{2}x)\sin x,\quad u=\cos x,\ du=-\sin x\,dx', claims=[('sin(x)**3', '(1-cos(x)**2)*sin(x)')])
    U.drill('2', 'N52-E1-2', 'P', '$\\sin^4x=(1-\\cos^2x)^2=1-2u^2+u^4$ (🧮 فك مربع قوس).')
    U.drill('3', 'G-10', 'I', 'مثل التمرين 2 لكن $u=\\sin x$ بدون سالب.')
    return U


# ---------------------------------------------------------------- 23
def u_pascal():
    U = Unit('U-T2', 'sin و cos معًا وأحدهما فردي', '5.2', 'ص68–69، مثال 2', 5)
    U.add('idea', 'الفكرة', p(rich('نفس النوع السابق: احجز من الدالة صاحبة الأس الفردي، وحوّل الباقي. الدالة الثانية تبقى كما هي '
                                   'وتصير قوة لـ $u$. بعدها فك القوس ووزّع.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\sin^m x\\cos^n x\\,dx$ وأحد الأسين فردي.')))
    U.add('short', '🧭 الطريقة: نفس الخطوات الأربع (النوع 22)', method_box(['cos', 'sin'], 'احجز من صاحب الأس الفردي، والثانية تصير $u$.'))
    it = ITEMS['1446-S1-SE-Q2.6']
    ex = question(it, 'U-T2 example')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\sin^{4}x\cos^{5}x=\sin^{4}x\cos^{4}x\cdot\cos x', [('sin(x)**4*cos(x)**5', 'sin(x)**4*cos(x)**4*cos(x)')],
         '<b>احجز</b> $\\cos x$: أس cos فردي (5)، وأس sin زوجي (4)'),
        ('tex', r'\cos^{4}x=\left(\cos^{2}x\right)^{2}=(1-\sin^{2}x)^{2}', [('cos(x)**4', '(1-sin(x)**2)**2')],
         '<b>حوّل</b> الباقي: $\\cos^4x$ مربع $\\cos^2x$ (🧮 متطابقات فيثاغورس)'),
        ('sub', 'sin(x)', 'cos(x)', '<b>عوّض</b>: $u=\\sin x$، و $du=\\cos x\\,dx$'),
        ('tex', r'\int\sin^{4}x\cos^{5}x\,dx=\int u^{4}(1-u^{2})^{2}\,du',
         [('sin(x)**4*cos(x)**5', 'sin(x)**4*(1-sin(x)**2)**2*diff(sin(x),x)')], 'التكامل كله بدلالة $u$'),
        ('tex', r'(1-u^{2})^{2}=1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')], '<b>فك القوس</b> وحده أولًا (🧮 فك مربع قوس)'),
        ('tex', r'u^{4}(1-2u^{2}+u^{4})=u^{4}-2u^{6}+u^{8}', [('u**4*(1-2*u**2+u**4)', 'u**4-2*u**6+u**8')],
         'وزّع $u^4$ على كل حد: الأسس تنجمع'),
        ('tex', r'\int\left(u^{4}-2u^{6}+u^{8}\right)du=\frac{u^{5}}{5}-\frac{2u^{7}}{7}+\frac{u^{9}}{9}',
         [('integrate(u**4-2*u**6+u**8,u)', 'u**5/5-2*u**7/7+u**9/9')], '<b>كامل</b> كل حد: زِد الأس 1 واقسم عليه'),
        ('line', 'sin(x)**5/5-2*sin(x)**7/7+sin(x)**9/9', '<b>ارجع</b> $u=\\sin x$')], 'U-T2 ex')
    ex += final(it, 'U-T2 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.raw(alg('frac-exp', 'تكامل أس كسري', [
        (r'\int u^{1/2}du=\frac{u^{3/2}}{3/2}=\frac23u^{3/2}', [('integrate(u**Rational(1,2),u)', '2*u**Rational(3,2)/3')],
         'نزيد الأس 1 ونقسم عليه؛ والقسمة على كسر = ضرب في مقلوبه (تحتاجه في التمرين 3):')]))
    U.add('trap', '⚠️ الفخ', ul([rich('الأسان زوجيان معًا ⇐ ما يصلح؛ نصف الزاوية (النوع 24).'),
                                'إذا الأسان فرديان معًا فاحجز من الأصغر (حدود أقل).']))
    U.add('paper', '✍️ في ورقة الكويز', md(r'\sin^{4}x\cos^{5}x=\sin^{4}x\,(1-\sin^{2}x)^{2}\cos x,\quad u=\sin x,\ du=\cos x\,dx')
          + p('ثم سطر التوزيع وسطر الجواب.'))
    U.drill('1', '1447-S1-SE-Q2.3', 'G', 'احجز $\\cos x$، والباقي $\\cos^4x=(1-\\sin^2x)^2$؛ فك القوس (🧮) ثم وزّع $u^2$.',
            first=r'\sin^{2}x\cos^{5}x=\sin^{2}x\,(1-\sin^{2}x)^{2}\cos x,\quad u=\sin x,\ du=\cos x\,dx',
            claims=[('sin(x)**2*cos(x)**5', 'sin(x)**2*(1-sin(x)**2)**2*cos(x)')])
    U.drill('2', 'N52-X01', 'P', 'الفردي sin ⇐ $u=\\cos x$ وإشارة سالبة أمام الكل.')
    U.drill('3', 'N52-E2-2', 'I', 'نفس الطريقة: احجز $\\cos x$، و $\\sqrt{\\sin x}=u^{1/2}$، والأسس كسرية (🧮).')
    return U


# ---------------------------------------------------------------- 24
def u_even():
    U = Unit('U-T3', 'أسس زوجية: نصف الزاوية', '5.2', 'ص67–70، أمثلة 1(3) و2(4)', 5)
    U.add('idea', 'الفكرة', p(rich('ما فيه أس فردي نحجز منه، فنخفّض الأس بمتطابقة نصف الزاوية: الأس 2 يصير أس 1 بزاوية مضاعفة.')))
    U.add('sign', 'العلامة', p(rich('$\\sin^2$ أو $\\cos^2$ أو $\\cos^4$ أو $\\sin^2\\cos^4$: كل الأسس زوجية.')))
    short, memo = sc_even()
    U.add('short', '⚡ الاختصار', short + box_memo(memo))
    it = ITEMS['N52-X13']
    ex = question(it, 'U-T3 example 1')
    ex += short_steps(it, [
        ('القانون: صف $\\sin^2$ في جدول نصف الزاوية', r'\int\sin^{2}kx\,dx=\frac{x}{2}-\frac{\sin2kx}{4k}+C', [R('even sin2')]),
        ('طلّع $k$: معامل $x$ داخل sin، ثم $2k$ و $4k$', r'k=1,\qquad 2k=2,\qquad 4k=4', [('2*1', '2'), ('4*1', '4')]),
        ('عوّض؛ = جواب 🧱 (من $\\sin^2x=\\frac{1-\\cos2x}{2}$)', r'\frac{x}{2}-\frac{\sin2x}{4}+C', [('=ANS', 'x/2-sin(2*x)/4')])], 'U-T3 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\sin^{2}x=\frac{1-\cos2x}{2}', [('sin(x)**2', '(1-cos(2*x))/2')], 'نصف الزاوية (مذكرة د. طارق ص67)'),
        ('line', 'x/2-sin(2*x)/4', '$\\int\\cos2x\\,dx=\\frac12\\sin2x$')], 'U-T3 ex1')
    ex += final(it, 'U-T3 example 1')
    U.add('ex', 'مثال 1 (تمرين من مذكرة د. طارق)', ex)
    it = ITEMS['N52-E1-3']
    ex = question(it, 'U-T3 example 2')
    ex += short_steps(it, [
        ('القانون: صيغة أس 4 جاهزة (تطلع من نصف الزاوية مرتين؛ = السطور 1–3 في 🧱)',
         r'\cos^{4}\theta=\frac38+\frac12\cos2\theta+\frac18\cos4\theta', [('cos(x)**4', 'Rational(3,8)+cos(2*x)/2+cos(4*x)/8')]),
        ('عوّض $\\theta=2x$: كل زاوية تتضاعف', r'\cos^{4}2x=\frac38+\frac12\cos4x+\frac18\cos8x',
         [('cos(2*x)**4', 'Rational(3,8)+cos(4*x)/2+cos(8*x)/8')]),
        ('كامل حدًا حدًا: الرقم يعطي $x$، و $\\int\\cos kx\\,dx=\\frac{\\sin kx}{k}$', r'\frac38x+\frac12\cdot\frac{\sin4x}{4}+\frac18\cdot\frac{\sin8x}{8}',
         [('=ANS', '3*x/8+sin(4*x)/8+sin(8*x)/64')]),
        ('اضرب الكسور: $\\frac12\\cdot\\frac14=\\frac18$، و $\\frac18\\cdot\\frac18=\\frac{1}{64}$', r'=\frac{3x}{8}+\frac{\sin4x}{8}+\frac{\sin8x}{64}+C',
         [('Rational(1,2)*Rational(1,4)', 'Rational(1,8)'), ('Rational(1,8)*Rational(1,8)', 'Rational(1,64)'),
          ('=ANS', '3*x/8+sin(4*x)/8+sin(8*x)/64')])], 'U-T3 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\cos^{4}2x=\left(\frac{1+\cos4x}{2}\right)^{2}=\frac14\left(1+2\cos4x+\cos^{2}4x\right)',
         [('cos(2*x)**4', '(1+2*cos(4*x)+cos(4*x)**2)/4')], 'نصف الزاوية مرة، ثم فك المربع'),
        ('tex', r'\cos^{2}4x=\frac{1+\cos8x}{2}', [('cos(4*x)**2', '(1+cos(8*x))/2')], 'نصف الزاوية مرة ثانية'),
        ('tex', r'\cos^{4}2x=\frac38+\frac12\cos4x+\frac18\cos8x', [('cos(2*x)**4', 'Rational(3,8)+cos(4*x)/2+cos(8*x)/8')],
         'نجمع: $\\frac14+\\frac18=\\frac38$'),
        ('line', '3*x/8+sin(4*x)/8+sin(8*x)/64', 'نكامل كل حد')], 'U-T3 ex2')
    ex += final(it, 'U-T3 example 2')
    U.add('ex', 'مثال 2: أس 4 (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', p(rich('$\\int\\sin^2x\\,dx\\ne\\frac{\\sin^3x}{3}$ لأن مشتقة $\\sin x$ غير موجودة بجانبه.')))
    U.add('paper', '✍️ في ورقة الكويز', md(r'\sin^{2}x=\frac{1-\cos2x}{2}') + p('ثم كامل حدًا حدًا.'))
    U.drill('1', 'N52-X14', 'G', 'زائد مع cos.', first=r'\cos^{2}x=\frac{1+\cos2x}{2}', claims=[('cos(x)**2', '(1+cos(2*x))/2')])
    U.drill('2', 'N52-E2-4', 'I', '$\\sin^2x\\cos^4x=(\\sin x\\cos x)^2\\cos^2x=\\frac14\\sin^22x\\cdot\\frac{1+\\cos2x}{2}$.')
    return U


# ---------------------------------------------------------------- 25
def u_sec_even():
    U = Unit('U-T4', 'tan و sec: الـ sec زوجي', '5.2', 'ص70–71، الحالة 1', 5)
    U.add('idea', 'الفكرة', p(rich('احجز $\\sec^2x$ (مشتقة $\\tan x$)، والباقي من sec يتحول إلى tan بـ $\\sec^2x=1+\\tan^2x$. '
                                   'ثم $u=\\tan x$.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\tan^m x\\sec^n x\\,dx$ و $n$ زوجي (أو sec زوجي وحده).')))
    U.add('short', '🧭 الطريقة: نفس الخطوات الأربع (النوع 22)', method_box(['sec'], 'sec زوجي ⇐ احجز $\\sec^2x$، و $u=\\tan x$.'))
    it = ITEMS['1447-S1-FE-Q2.6']
    ex = question(it, 'U-T4 example')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('sub', 'tan(x)', 'sec(x)**2', '<b>احجز</b> $\\sec^2x$ (أس sec زوجي) و<b>عوّض</b> $u=\\tan x$. هنا ما فيه باقي يتحوّل'),
        ('tex', r'\int\tan^{3}x\sec^{2}x\,dx=\int u^{3}\,du', [('tan(x)**3*sec(x)**2', 'tan(x)**3*diff(tan(x),x)')],
         'التكامل كله بدلالة $u$'),
        ('tex', r'=\frac{u^{4}}{4}', [('integrate(u**3,u)', 'u**4/4')], '<b>كامل</b>: زِد الأس 1 واقسم عليه'),
        ('line', 'tan(x)**4/4', '<b>ارجع</b> $u=\\tan x$')], 'U-T4 ex')
    ex += final(it, 'U-T4 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', p(rich('هذا السؤال ينحل أيضًا بـ $u=\\sec x$ (لأن tan فردي)، ويعطي $\\frac{\\sec^4x}{4}-\\frac{\\sec^2x}{2}$. '
                                    'الجوابان صحيحان ويختلفان بثابت.')))
    same_value('sec(x)**4/4-sec(x)**2/2', 'tan(x)**4/4-Rational(1,4)', 'U-T4 two answers')
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر $u=\\tan x$، $du=\\sec^2x\\,dx$، ثم الجواب.')))
    U.drill('1', 'G-11', 'G', '$u=\\tan x$.', first=r'\sec^{4}x=\sec^{2}x\cdot\sec^{2}x=(1+\tan^{2}x)\sec^{2}x',
            claims=[('sec(x)**4', '(1+tan(x)**2)*sec(x)**2')])
    U.drill('2', 'G-12', 'I', 'احجز $\\sec^2x$؛ الباقي $\\sec^4x=(1+u^2)^2$.')
    return U


# ---------------------------------------------------------------- 26
def u_tan_odd():
    U = Unit('U-T5', 'tan و sec: الـ tan فردي', '5.2', 'ص71–72، الحالة 2', 6)
    U.add('idea', 'الفكرة', p(rich('احجز $\\sec x\\tan x$ (مشتقة $\\sec x$)، والباقي من tan (زوجي) يتحول بـ $\\tan^2x=\\sec^2x-1$. ثم $u=\\sec x$.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\tan^m x\\sec^n x\\,dx$ و $m$ فردي، ومعه sec واحد على الأقل.')))
    U.add('short', '🧭 الطريقة: نفس الخطوات الأربع (النوع 22)', method_box(['tan'], 'tan فردي ⇐ احجز $\\sec x\\tan x$، و $u=\\sec x$.'))
    it = ITEMS['1447-S2-SE-Q3.3']
    ex = question(it, 'U-T5 example')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\sec^{3}x\tan^{3}x=\sec^{2}x\tan^{2}x\cdot\sec x\tan x', [('sec(x)**3*tan(x)**3', 'sec(x)**2*tan(x)**2*sec(x)*tan(x)')],
         '<b>احجز</b> $\\sec x\\tan x$: أس tan فردي، ومعه sec'),
        ('tex', r'\tan^{2}x=\sec^{2}x-1\ \Rightarrow\ \sec^{2}x\,(\sec^{2}x-1)\cdot\sec x\tan x',
         [('sec(x)**3*tan(x)**3', 'sec(x)**2*(sec(x)**2-1)*sec(x)*tan(x)')], '<b>حوّل</b> الباقي $\\tan^2x$ إلى sec (🧮 متطابقات فيثاغورس)'),
        ('sub', 'sec(x)', 'sec(x)*tan(x)', '<b>عوّض</b>: $u=\\sec x$، و $du=\\sec x\\tan x\\,dx$'),
        ('tex', r'\int\sec^{3}x\tan^{3}x\,dx=\int u^{2}(u^{2}-1)\,du',
         [('sec(x)**3*tan(x)**3', 'sec(x)**2*(sec(x)**2-1)*diff(sec(x),x)')], 'التكامل كله بدلالة $u$'),
        ('tex', r'u^{2}(u^{2}-1)=u^{4}-u^{2}', [('u**2*(u**2-1)', 'u**4-u**2')], '<b>وزّع</b> $u^2$ على القوس'),
        ('tex', r'\int\left(u^{4}-u^{2}\right)du=\frac{u^{5}}{5}-\frac{u^{3}}{3}', [('integrate(u**4-u**2,u)', 'u**5/5-u**3/3')],
         '<b>كامل</b> كل حد'),
        ('line', 'sec(x)**5/5-sec(x)**3/3', '<b>ارجع</b> $u=\\sec x$')], 'U-T5 ex')
    ex += final(it, 'U-T5 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', p(rich('tan زوجي و sec فردي ⇐ لا هذا ولا ذاك: حوّل كل tan إلى sec ثم سلسلة sec (النوع 27).')))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر الحجز والتحويل، سطر $u=\\sec x$، ثم الجواب.')))
    U.drill('1', 'G-13', 'G', '$\\int(u^2-1)\\,du$.', first=r'\tan^{3}x\sec x=\tan^{2}x\cdot\sec x\tan x=(\sec^{2}x-1)\sec x\tan x',
            claims=[('tan(x)**3*sec(x)', '(sec(x)**2-1)*sec(x)*tan(x)')])
    U.drill('2', 'N52-E3-4', 'P', 'احجز $\\sec x\\tan x$؛ الباقي $\\tan^4x\\sec^2x=(\\sec^2x-1)^2\\sec^2x$.')
    U.drill('3', 'N52-X06', 'I', 'احجز $\\sec x\\tan x$؛ الباقي $\\tan^4x\\sec^4x=(u^2-1)^2u^4$.')
    return U


# ---------------------------------------------------------------- 27
def u_reduce():
    U = Unit('U-T6', 'tan وحدها و sec فردي وحده (سلسلة التخفيض)', '5.2', 'ص70–73، الحالتان 3 و4', 6)
    U.add('idea', 'الفكرة', p(rich('ما فيه شيء نحجزه. نكسر القوة: $\\tan^mx=\\tan^{m-2}x\\,(\\sec^2x-1)$ فينزل الأس 2 كل مرة. '
                                   'ومع sec الفردي تجزئة يرجع فيها التكامل نفسه.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\tan^4x\\,dx$ أو $\\int\\tan^6x\\,dx$ أو $\\int\\sec^3x\\,dx$ أو $\\int\\sec^5x\\,dx$.')))
    short, memo = sc_reduce()
    U.add('short', '⚡ الاختصار', short + box_memo(memo))
    it = ITEMS['N52-E3-2']
    ex = question(it, 'U-T6 example 1')
    ex += short_steps(it, [
        ('القانون: سلسلة tan (الأس ينزل 2 كل مرة)', r'\int\tan^{m}x\,dx=\frac{\tan^{m-1}x}{m-1}-\int\tan^{m-2}x\,dx', [R('tan reduce')]),
        ('مع $m=4$: $m-1=3$، والأس الباقي 2', r'\int\tan^{4}x\,dx=\frac{\tan^{3}x}{3}-\int\tan^{2}x\,dx',
         [('diff(tan(x)**3/3,x)-tan(x)**2', 'tan(x)**4')]),
        ('مع $m=2$: $m-1=1$، والأس الباقي 0، و $\\int\\tan^0x\\,dx=\\int1\\,dx=x$', r'\int\tan^{2}x\,dx=\tan x-x',
         [('diff(tan(x)-x,x)', 'tan(x)**2')]),
        ('عوّض الثاني في الأول، ووزّع السالب (🧮)؛ = جواب 🧱', r'\frac{\tan^{3}x}{3}-\left(\tan x-x\right)=\frac{\tan^{3}x}{3}-\tan x+x+C',
         [('=ANS', 'tan(x)**3/3-tan(x)+x')])], 'U-T6 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\tan^{4}x=\tan^{2}x\,(\sec^{2}x-1)=\tan^{2}x\sec^{2}x-\tan^{2}x', [('tan(x)**4', 'tan(x)**2*sec(x)**2-tan(x)**2')],
         'نكسر القوة'),
        ('line', 'tan(x)**3/3-Integral(tan(x)**2,x)', 'الحد الأول $u=\\tan x$'),
        ('tex', r'\tan^{2}x=\sec^{2}x-1', [('tan(x)**2', 'sec(x)**2-1')], 'مرة ثانية'),
        ('line', 'tan(x)**3/3-tan(x)+x', '$\\int(\\sec^2x-1)dx=\\tan x-x$')], 'U-T6 ex1')
    ex += final(it, 'U-T6 example 1')
    U.add('ex', 'مثال 1 (من مذكرة د. طارق)', ex)
    it = ITEMS['N52-E3-1']
    A = '(sec(x)*tan(x)/2+log(Abs(sec(x)+tan(x)))/2)'
    ex = question(it, 'U-T6 example 2')
    ex += short_steps(it, [
        ('القانون: سلسلة sec', r'\int\sec^{n}x\,dx=\frac{\sec^{n-2}x\,\tan x}{n-1}+\frac{n-2}{n-1}\int\sec^{n-2}x\,dx', [R('sec reduce')]),
        ('مع $n=3$: $n-1=2$ و $n-2=1$', r'\int\sec^{3}x\,dx=\frac{\sec x\tan x}{2}+\frac12\int\sec x\,dx',
         [('diff(sec(x)*tan(x)/2,x)+sec(x)/2', 'sec(x)**3')]),
        ('التكامل الباقي من الجدول', r'\int\sec x\,dx=\ln\left|\sec x+\tan x\right|', [R('sec base')]),
        ('عوّض؛ = جواب 🧱 (التجزئة ثم حل المعادلة)', r'\frac{\sec x\tan x}{2}+\frac12\ln\left|\sec x+\tan x\right|+C', [('=ANS', A)])],
        'U-T6 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('parts', 'sec(x)', 'sec(x)**2', 'sec(x)*tan(x)', 'tan(x)', '$u=\\sec x$ و $dv=\\sec^2x\\,dx$'),
        ('line', 'sec(x)*tan(x)-Integral(sec(x)*tan(x)**2,x)', 'القانون'),
        ('tex', r'I=\sec x\tan x-I+\int\sec x\,dx', [('sec(x)*tan(x)-%s+log(Abs(sec(x)+tan(x)))' % A, A)],
         '$\\tan^2x=\\sec^2x-1$ فيرجع $I=\\int\\sec^3x\\,dx$ (🧮 حل معادلة فيها التكامل نفسه)'),
        ('tex', r'2I=\sec x\tan x+\ln|\sec x+\tan x|', [('2*%s' % A, 'sec(x)*tan(x)+log(Abs(sec(x)+tan(x)))')], 'نجمع $I$ ونقسم على 2')],
        'U-T6 ex2')
    ex += final(it, 'U-T6 example 2')
    U.add('ex', 'مثال 2: sec³ (من مذكرة د. طارق)', ex)
    U.raw(alg('cyclic-eq'))
    U.add('trap', '⚠️ الفخ', p(rich('لا تنسَ الحد الأخير: $+x$ أو $-x$ مع الأس الزوجي، و $\\ln|\\sec x|$ مع الفردي.')))
    U.add('paper', '✍️ في ورقة الكويز', md(r'\int\tan^{4}x\,dx=\int\tan^{2}x\,(\sec^{2}x-1)\,dx=\frac{\tan^{3}x}{3}-\int\tan^{2}x\,dx'))
    U.drill('1', 'N52-X16', 'G', '$\\int\\tan^4x\\,dx$ هو المثال 1.', first=r'\int\tan^{6}x\,dx=\frac{\tan^{5}x}{5}-\int\tan^{4}x\,dx',
            claims=[('diff(tan(x)**5/5,x)-tan(x)**4', 'tan(x)**6')])
    U.drill('2', 'N52-X15', 'I', '$\\int\\sec^5x\\,dx=\\frac{\\sec^3x\\tan x}{4}+\\frac34\\int\\sec^3x\\,dx$، و $\\int\\sec^3x$ هو المثال 2.')
    return U


# ---------------------------------------------------------------- 28
def u_cotcsc():
    U = Unit('U-T7', 'cot و csc', '5.2', 'ص73، الحالات المشابهة', 6)
    U.add('idea', 'الفكرة', p(rich('نفس tan و sec بالضبط، مع فرق واحد: مشتقات cot و csc سالبة، فتظهر إشارة $-$ أمام الكل.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\cot^m x\\csc^n x\\,dx$.'))
          + contrast([(r'\int\cot^{4}x\csc^{4}x\,dx', '$u=\\cot x$', 'csc زوجي'),
                      (r'\int\cot^{5}x\csc^{3}x\,dx', '$u=\\csc x$', 'cot فردي')]))
    U.add('short', '🧭 الطريقة: نفس الخطوات الأربع (النوع 22)', method_box(['csc', 'cot'], 'مثل tan و sec، وزد سالب أمام الكل.'))
    it = ITEMS['1446-S2-SE-Q2.4']
    ex = question(it, 'U-T7 example')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\cot^{4}x\csc^{4}x=\cot^{4}x\csc^{2}x\cdot\csc^{2}x', [('cot(x)**4*csc(x)**4', 'cot(x)**4*csc(x)**2*csc(x)**2')],
         '<b>احجز</b> $\\csc^2x$: أس csc زوجي'),
        ('tex', r'\csc^{2}x=1+\cot^{2}x\ \Rightarrow\ \cot^{4}x\,(1+\cot^{2}x)\csc^{2}x',
         [('cot(x)**4*csc(x)**4', 'cot(x)**4*(1+cot(x)**2)*csc(x)**2')], '<b>حوّل</b> الباقي $\\csc^2x$ إلى cot (🧮 متطابقات فيثاغورس)'),
        ('sub', 'cot(x)', '-csc(x)**2', '<b>عوّض</b>: $u=\\cot x$، و $du=-\\csc^2x\\,dx$ ⇐ $\\csc^2x\\,dx=-du$'),
        ('tex', r'\int\cot^{4}x\csc^{4}x\,dx=-\int u^{4}(1+u^{2})\,du',
         [('cot(x)**4*csc(x)**4', '-cot(x)**4*(1+cot(x)**2)*diff(cot(x),x)')], 'التكامل بدلالة $u$، والسالب قدّام الكل'),
        ('tex', r'u^{4}(1+u^{2})=u^{4}+u^{6}', [('u**4*(1+u**2)', 'u**4+u**6')], '<b>وزّع</b> $u^4$'),
        ('tex', r'-\int\left(u^{4}+u^{6}\right)du=-\frac{u^{5}}{5}-\frac{u^{7}}{7}', [('-integrate(u**4+u**6,u)', '-u**5/5-u**7/7')],
         '<b>كامل</b> كل حد، والسالب يدخل على الاثنين'),
        ('line', '-cot(x)**5/5-cot(x)**7/7', '<b>ارجع</b> $u=\\cot x$')], 'U-T7 ex')
    ex += final(it, 'U-T7 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', p(rich('$\\frac{d}{dx}\\cot x=-\\csc^2x$ و $\\frac{d}{dx}\\csc x=-\\csc x\\cot x$: السالب في الاثنين.')))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر الحجز، سطر $u$ و $du$ (بالسالب)، ثم الجواب.')))
    U.drill('1', 'N52-X08', 'G', 'إشارة سالبة أمام الكل، والقوس $(1+u^2)^2$.',
            first=r'\csc^{6}x=(1+\cot^{2}x)^{2}\csc^{2}x,\quad u=\cot x,\ du=-\csc^{2}x\,dx',
            claims=[('csc(x)**6', '(1+cot(x)**2)**2*csc(x)**2')])
    U.drill('2', 'N52-X09', 'P', 'cot فردي ⇐ $u=\\csc x$، و $du=-\\csc x\\cot x\\,dx$.')
    U.drill('3', 'N52-E4-2', 'I', 'مثل التمرين 2: احجز $\\csc x\\cot x$، والباقي $(u^2-1)^2u^4$، وسالب قدّام الكل.')
    return U


# ---------------------------------------------------------------- 29
def u_prod():
    U = Unit('U-T8', 'ضرب sin و cos بزاويتين مختلفتين', '5.2', 'ص74–75، مثال 5', 6)
    U.add('idea', 'الفكرة', p(rich('متطابقات الضرب تحوّل حاصل الضرب إلى مجموع، والمجموع سهل التكامل.')))
    U.add('sign', 'العلامة', p(rich('$\\sin mx\\cos nx$ أو $\\sin mx\\sin nx$ أو $\\cos mx\\cos nx$ و $m\\ne n$.')))
    short, memo = sc_prod()
    U.add('short', '⚡ الاختصار', short + box_memo(memo))
    it = ITEMS['N52-E5-1']
    ex = question(it, 'U-T8 example')
    ex += short_steps(it, [
        ('القانون: صف sin·cos (بشرط $m\\ne\\pm n$)',
         r'\int\sin mx\cos nx\,dx=-\frac12\left(\frac{\cos(m-n)x}{m-n}+\frac{\cos(m+n)x}{m+n}\right)+C', [R('prod sc')]),
        ('طلّع الزاويتين: $m$ مع sin و $n$ مع cos، ثم الفرق والمجموع', r'm=7,\ n=5:\qquad m-n=2,\qquad m+n=12', [('7-5', '2'), ('7+5', '12')]),
        ('عوّض في القانون', r'-\frac12\left(\frac{\cos2x}{2}+\frac{\cos12x}{12}\right)', [('=ANS', '-(cos(2*x)/2+cos(12*x)/12)/2')]),
        ('وزّع $-\\frac12$: $\\frac12\\cdot\\frac12=\\frac14$ و $\\frac12\\cdot\\frac{1}{12}=\\frac{1}{24}$؛ = جواب 🧱',
         r'=-\frac{\cos2x}{4}-\frac{\cos12x}{24}+C', [('-(cos(2*x)/2+cos(12*x)/12)/2', '-cos(2*x)/4-cos(12*x)/24'),
                                                     ('=ANS', '-cos(2*x)/4-cos(12*x)/24')])], 'U-T8 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\sin7x\cos5x=\frac12\left[\sin2x+\sin12x\right]', [('sin(7*x)*cos(5*x)', '(sin(2*x)+sin(12*x))/2')],
         'متطابقة الضرب (🧮)'),
        ('line', '-cos(2*x)/4-cos(12*x)/24', '$\\int\\sin kx\\,dx=-\\frac1k\\cos kx$')], 'U-T8 ex')
    ex += final(it, 'U-T8 example')
    U.add('ex', 'مثال (من مذكرة د. طارق)', ex)
    U.raw(alg('product-ids', 'متطابقات الضرب (مذكرة د. طارق ص74)', [
        (r'\sin A\cos B=\frac12\left[\sin(A-B)+\sin(A+B)\right]', [('sin(7*x)*cos(5*x)', '(sin(2*x)+sin(12*x))/2')], 'sin × cos:'),
        (r'\sin A\sin B=\frac12\left[\cos(A-B)-\cos(A+B)\right]', [('sin(4*x)*sin(3*x)', '(cos(x)-cos(7*x))/2')], 'sin × sin:'),
        (r'\cos A\cos B=\frac12\left[\cos(A-B)+\cos(A+B)\right]', [('cos(3*x)*cos(x)', '(cos(2*x)+cos(4*x))/2')], 'cos × cos:'),
        (r'\sin(-\theta)=-\sin\theta,\qquad \cos(-\theta)=\cos\theta', [('sin(-2*x)', '-sin(2*x)'), ('cos(-2*x)', 'cos(2*x)')],
         'إذا طلع $A-B$ سالبًا:')]))
    U.add('trap', '⚠️ الفخ', p(rich('إذا كان $m-n$ سالبًا: $\\cos(-\\theta)=\\cos\\theta$ لكن $\\sin(-\\theta)=-\\sin\\theta$؛ انتبه للإشارة.')))
    U.add('paper', '✍️ في ورقة الكويز', md(r'\sin7x\cos5x=\frac12\left[\sin2x+\sin12x\right]') + p('ثم كامل كل حد.'))
    U.drill('1', 'N52-X10', 'G', '$\\sin(-2x)=-\\sin2x$.',
            first=r'\sin3x\cos5x=\frac12\left[\sin(-2x)+\sin8x\right]=\frac12\left[-\sin2x+\sin8x\right]',
            claims=[('sin(3*x)*cos(5*x)', '(-sin(2*x)+sin(8*x))/2')])
    U.drill('2', 'N52-E5-2', 'P', 'sin·sin: $\\frac12[\\cos(m-n)x-\\cos(m+n)x]$.')
    U.drill('3', 'G-14', 'I', 'cos·cos: $\\frac12[\\cos2x+\\cos4x]$.')
    return U


UNITS_52 = [u_odd_alone, u_pascal, u_even, u_sec_even, u_tan_odd, u_reduce, u_cotcsc, u_prod]

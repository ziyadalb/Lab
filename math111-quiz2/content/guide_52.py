"""المذكرة الكاملة — الدرس 5.2: التكاملات المثلثية (اليومان 5–6)."""
from booklet import sc_even, sc_pascal, sc_prod, sc_reduce
from booklet_engine import ITEMS, arith, same_value
from guide_kit import Unit, alg, contrast, final, question, rich, short_steps, steps
from guide_42 import box_memo
from html_kit import md, mi, p, table, ul


# ---------------------------------------------------------------- 22
def u_odd_alone():
    U = Unit('U-T1', 'قوة فردية لـ sin أو cos وحدها', '5.2', 'ص67–68، مثال 1', 5)
    U.add('idea', 'الفكرة', p(rich('احجز واحدًا من القوة الفردية (هو مشتقة الدالة الأخرى)، وحوّل الباقي (قوة زوجية) بالمتطابقة '
                                   '$\\sin^2x+\\cos^2x=1$. فيصير التكامل كثيرة حدود في $u$.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\cos^3x\\,dx$ أو $\\int\\sin^5x\\,dx$: قوة <b>فردية</b> لدالة واحدة.'))
          + contrast([(r'\int\cos^{3}x\,dx', 'احجز $\\cos x$، $u=\\sin x$', 'الأس فردي'),
                      (r'\int\cos^{2}x\,dx', 'نصف الزاوية (النوع 24)', 'الأس زوجي')]))
    U.add('short', '⚡ الاختصار', ul([
        rich('$\\cos^{2k+1}x$: $u=\\sin x$، والباقي $(1-u^2)^k$، وإشارة $+$.'),
        rich('$\\sin^{2k+1}x$: $u=\\cos x$، والباقي $(1-u^2)^k$، وإشارة $-$ أمام الكل.')])
          + box_memo(rich('احجز واحدًا، والباقي زوجي يصير $(1-u^2)$.')))
    it = ITEMS['N52-E1-1']
    ex = question(it, 'U-T1 example')
    ex += short_steps(it, [
        ('cos أسه فردي ($3=2\\cdot1+1$) ⇐ $u=\\sin x$ وإشارة $+$، والقوس:', r'k=1:\quad (1-u^{2})^{1}', [('2*1+1', '3')]),
        ('كامل القوس ونرجع $u$:', r'u-\frac{u^{3}}{3}=\sin x-\frac{\sin^{3}x}{3}+C',
         [('integrate(1-x**2,x)', 'x-x**3/3'), ('=ANS', 'sin(x)-sin(x)**3/3')])], 'U-T1 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\cos^{3}x=\cos^{2}x\cdot\cos x=(1-\sin^{2}x)\cos x', [('cos(x)**3', '(1-sin(x)**2)*cos(x)')],
         'نحجز $\\cos x$ (مشتقة $\\sin x$) ونحوّل $\\cos^2x$ (🧮)'),
        ('sub', 'sin(x)', 'cos(x)', 'نسمّي $u=\\sin x$'),
        ('tex', r'=\int(1-u^{2})\,du=u-\frac{u^{3}}{3}', [('integrate(1-x**2,x)', 'x-x**3/3')], 'تكامل كثيرة حدود'),
        ('line', 'sin(x)-sin(x)**3/3', 'نرجع $u=\\sin x$')], 'U-T1 ex')
    ex += final(it, 'U-T1 example')
    U.add('ex', 'مثال (من المذكرة)', ex)
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
    U = Unit('U-T2', 'sin و cos معًا وأحدهما فردي (صف باسكال)', '5.2', 'ص68–69، مثال 2', 5)
    U.add('idea', 'الفكرة', p(rich('نفس النوع السابق: احجز من الدالة صاحبة الأس الفردي، والباقي قوس يُفك. صف باسكال يعطيك '
                                   'معاملات القوس بسرعة بدون فك.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\sin^m x\\cos^n x\\,dx$ وأحد الأسين فردي.')))
    short, memo = sc_pascal()
    U.add('short', '⚡ الاختصار (يشمل tan/sec و cot/csc في الأنواع القادمة)', short + box_memo(memo))
    it = ITEMS['1446-S1-SE-Q2.6']
    ex = question(it, 'U-T2 example')
    ex += short_steps(it, [
        ('cos أسه فردي ($5=2\\cdot2+1$) ⇐ $u=\\sin x$، وأس البداية $p$ = أس sin:', r'k=2,\quad p=4', [('2*2+1', '5')]),
        ('صف باسكال رقم 2 هو $1\\ \\ 2\\ \\ 1$ بإشارات $+\\ -\\ +$، والأسس تبدأ من $p+1=5$ وتزيد 2:',
         r'\frac{u^{5}}{5}-\frac{2u^{7}}{7}+\frac{u^{9}}{9}', [('integrate(u**4*(1-u**2)**2,u)', 'u**5/5-2*u**7/7+u**9/9')]),
        ('نرجع $u=\\sin x$:', r'\frac{\sin^{5}x}{5}-\frac{2\sin^{7}x}{7}+\frac{\sin^{9}x}{9}+C',
         [('=ANS', 'sin(x)**5/5-2*sin(x)**7/7+sin(x)**9/9')])], 'U-T2 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\sin^{4}x\cos^{5}x=\sin^{4}x\,(1-\sin^{2}x)^{2}\cos x', [('sin(x)**4*cos(x)**5', 'sin(x)**4*(1-sin(x)**2)**2*cos(x)')],
         'نحجز $\\cos x$ والباقي $\\cos^4x=(1-\\sin^2x)^2$'),
        ('sub', 'sin(x)', 'cos(x)', 'نسمّي $u=\\sin x$'),
        ('tex', r'=\int u^{4}(1-2u^{2}+u^{4})\,du=\int\left(u^{4}-2u^{6}+u^{8}\right)du', [('u**4*(1-2*u**2+u**4)', 'u**4-2*u**6+u**8')],
         'نفك القوس (🧮 فك مربع قوس) ونوزّع $u^4$'),
        ('line', 'sin(x)**5/5-2*sin(x)**7/7+sin(x)**9/9', 'نكامل كل حد ونرجع $u$')], 'U-T2 ex')
    ex += final(it, 'U-T2 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.raw(alg('frac-exp', 'تكامل أس كسري', [
        (r'\int u^{1/2}du=\frac{u^{3/2}}{3/2}=\frac23u^{3/2}', [('integrate(u**Rational(1,2),u)', '2*u**Rational(3,2)/3')],
         'نزيد الأس 1 ونقسم عليه؛ والقسمة على كسر = ضرب في مقلوبه (تحتاجه في التمرين 3):')]))
    U.add('trap', '⚠️ الفخ', ul([rich('الأسان زوجيان معًا ⇐ ما يصلح؛ نصف الزاوية (النوع 24).'),
                                'إذا الأسان فرديان معًا فاحجز من الأصغر (حدود أقل).']))
    U.add('paper', '✍️ في ورقة الكويز', md(r'\sin^{4}x\cos^{5}x=\sin^{4}x\,(1-\sin^{2}x)^{2}\cos x,\quad u=\sin x,\ du=\cos x\,dx')
          + p('ثم سطر التوزيع وسطر الجواب.'))
    U.drill('1', '1447-S1-SE-Q2.3', 'G', 'الأسس في الجواب: 3، 5، 7 ومعاملات القوس 1، −2، 1.',
            first=r'\cos^{5}x=\cos^{2\cdot2+1}x:\quad k=2,\ u=\sin x,\ p=2',
            claims=[('sin(x)**2*cos(x)**5', 'sin(x)**2*(1-sin(x)**2)**2*cos(x)')])
    U.drill('2', 'N52-X01', 'P', 'الفردي sin ⇐ $u=\\cos x$ وإشارة سالبة أمام الكل.')
    U.drill('3', 'N52-E2-2', 'I', '$\\sqrt{\\sin x}=u^{1/2}$؛ القاعدة نفسها والأسس كسرية (🧮).')
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
        ('الأس زوجي ⇐ نصف الزاوية، والزاوية $kx$ مع:', r'k=1,\quad 4k=4', [('4*1', '4')]),
        ('نصف $x$، ناقص (مع sin) $\\sin$ ضعف الزاوية على $4k$:', r'\frac{x}{2}-\frac{\sin2x}{4}+C', [('=ANS', 'x/2-sin(2*x)/4')])], 'U-T3 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\sin^{2}x=\frac{1-\cos2x}{2}', [('sin(x)**2', '(1-cos(2*x))/2')], 'نصف الزاوية (ص67)'),
        ('line', 'x/2-sin(2*x)/4', '$\\int\\cos2x\\,dx=\\frac12\\sin2x$')], 'U-T3 ex1')
    ex += final(it, 'U-T3 example 1')
    U.add('ex', 'مثال 1 (تمرين المذكرة)', ex)
    it = ITEMS['N52-E1-3']
    ex = question(it, 'U-T3 example 2')
    ex += short_steps(it, [
        ('صيغة جاهزة لأس 4 (تطلع من نصف الزاوية مرتين):', r'\cos^{4}\theta=\frac38+\frac12\cos2\theta+\frac18\cos4\theta',
         [('cos(x)**4', 'Rational(3,8)+cos(2*x)/2+cos(4*x)/8')]),
        ('مع $\\theta=2x$ كامل حدًا حدًا (كل sin يُقسم على زاويته):', r'\frac{3x}{8}+\frac{\sin4x}{8}+\frac{\sin8x}{64}+C',
         [('=ANS', '3*x/8+sin(4*x)/8+sin(8*x)/64')])], 'U-T3 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\cos^{4}2x=\left(\frac{1+\cos4x}{2}\right)^{2}=\frac14\left(1+2\cos4x+\cos^{2}4x\right)',
         [('cos(2*x)**4', '(1+2*cos(4*x)+cos(4*x)**2)/4')], 'نصف الزاوية مرة، ثم فك المربع'),
        ('tex', r'\cos^{2}4x=\frac{1+\cos8x}{2}', [('cos(4*x)**2', '(1+cos(8*x))/2')], 'نصف الزاوية مرة ثانية'),
        ('tex', r'\cos^{4}2x=\frac38+\frac12\cos4x+\frac18\cos8x', [('cos(2*x)**4', 'Rational(3,8)+cos(4*x)/2+cos(8*x)/8')],
         'نجمع: $\\frac14+\\frac18=\\frac38$'),
        ('line', '3*x/8+sin(4*x)/8+sin(8*x)/64', 'نكامل كل حد')], 'U-T3 ex2')
    ex += final(it, 'U-T3 example 2')
    U.add('ex', 'مثال 2: أس 4 (من المذكرة)', ex)
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
    U.add('short', '⚡ الاختصار', p(rich('صف $\\sec^{2k+2}x$ في جدول باسكال (النوع 23): $u=\\tan x$، وإشارة $+$، والقوس $(1+u^2)^k$.'))
          + box_memo('sec زوجي ⇐ u = tan.'))
    it = ITEMS['1447-S1-FE-Q2.6']
    ex = question(it, 'U-T4 example')
    ex += short_steps(it, [
        ('sec زوجي ($\\sec^2=\\sec^{2\\cdot0+2}$) ⇐ $u=\\tan x$، وإشارة $+$، و $p$ = أس tan:', r'k=0,\quad p=3', [('2*0+2', '2')]),
        ('ما في قوس، فالأس يزيد 1 ونقسم عليه:', r'\frac{u^{4}}{4}=\frac{\tan^{4}x}{4}+C', [('integrate(x**3,x)', 'x**4/4'), ('=ANS', 'tan(x)**4/4')])],
        'U-T4 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('sub', 'tan(x)', 'sec(x)**2', '$u=\\tan x$، و $\\sec^2x\\,dx=du$ موجودة كما هي'),
        ('tex', r'=\int u^{3}\,du=\frac{u^{4}}{4}', [('integrate(x**3,x)', 'x**4/4')], 'قاعدة القوة'),
        ('line', 'tan(x)**4/4', 'نرجع $u$')], 'U-T4 ex')
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
    U.add('short', '⚡ الاختصار', p(rich('صف $\\tan^{2k+1}x$ في جدول باسكال (النوع 23): $u=\\sec x$، و $p$ = أس sec ناقص 1، والقوس $(u^2-1)^k$.'))
          + box_memo('tan فردي ⇐ u = sec، وأس البداية ينقص 1.'))
    it = ITEMS['1447-S2-SE-Q3.3']
    ex = question(it, 'U-T5 example')
    ex += short_steps(it, [
        ('tan أسه فردي ($3=2\\cdot1+1$) ⇐ $u=\\sec x$، و $p$ = أس sec ناقص 1:', r'k=1,\quad p=3-1=2', [('2*1+1', '3'), ('3-1', '2')]),
        ('القوس $(u^2-1)^1$ بإشارات تتناوب والأعلى موجب، والأسس تبدأ من $p+1=3$:',
         r'\frac{u^{5}}{5}-\frac{u^{3}}{3}=\frac{\sec^{5}x}{5}-\frac{\sec^{3}x}{3}+C',
         [('integrate(x**2*(x**2-1),x)', 'x**5/5-x**3/3'), ('=ANS', 'sec(x)**5/5-sec(x)**3/3')])], 'U-T5 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\sec^{3}x\tan^{3}x=\sec^{2}x\,(\sec^{2}x-1)\cdot\sec x\tan x',
         [('sec(x)**3*tan(x)**3', 'sec(x)**2*(sec(x)**2-1)*sec(x)*tan(x)')], 'نحجز $\\sec x\\tan x$ ونحوّل $\\tan^2x$'),
        ('sub', 'sec(x)', 'sec(x)*tan(x)', 'نسمّي $u=\\sec x$'),
        ('tex', r'=\int u^{2}(u^{2}-1)\,du=\int\left(u^{4}-u^{2}\right)du', [('u**2*(u**2-1)', 'u**4-u**2')], 'نوزّع'),
        ('line', 'sec(x)**5/5-sec(x)**3/3', 'نكامل ونرجع $u$')], 'U-T5 ex')
    ex += final(it, 'U-T5 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', p(rich('tan زوجي و sec فردي ⇐ لا هذا ولا ذاك: حوّل كل tan إلى sec ثم سلسلة sec (النوع 27).')))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر الحجز والتحويل، سطر $u=\\sec x$، ثم الجواب.')))
    U.drill('1', 'G-13', 'G', '$\\int(u^2-1)\\,du$.', first=r'\tan^{3}x\sec x=\tan^{2}x\cdot\sec x\tan x=(\sec^{2}x-1)\sec x\tan x',
            claims=[('tan(x)**3*sec(x)', '(sec(x)**2-1)*sec(x)*tan(x)')])
    U.drill('2', 'N52-E3-4', 'P', '$\\tan^4x=(\\sec^2x-1)^2$، و $p=3-1=2$.')
    U.drill('3', 'N52-X06', 'I', '$p=5-1=4$، والقوس $(u^2-1)^2$.')
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
        ('سلسلة tan مرتين (الأس ينزل 2 كل مرة):', r'\int\tan^{4}x\,dx=\frac{\tan^{3}x}{3}-\int\tan^{2}x\,dx,\qquad \int\tan^{2}x\,dx=\tan x-x',
         [('diff(tan(x)**3/3,x)-tan(x)**2', 'tan(x)**4'), ('diff(tan(x)-x,x)', 'tan(x)**2')]),
        ('الأس زوجي ⇐ النهاية $\\pm x$:', r'\frac{\tan^{3}x}{3}-\tan x+x+C', [('=ANS', 'tan(x)**3/3-tan(x)+x')])], 'U-T6 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\tan^{4}x=\tan^{2}x\,(\sec^{2}x-1)=\tan^{2}x\sec^{2}x-\tan^{2}x', [('tan(x)**4', 'tan(x)**2*sec(x)**2-tan(x)**2')],
         'نكسر القوة'),
        ('line', 'tan(x)**3/3-Integral(tan(x)**2,x)', 'الحد الأول $u=\\tan x$'),
        ('tex', r'\tan^{2}x=\sec^{2}x-1', [('tan(x)**2', 'sec(x)**2-1')], 'مرة ثانية'),
        ('line', 'tan(x)**3/3-tan(x)+x', '$\\int(\\sec^2x-1)dx=\\tan x-x$')], 'U-T6 ex1')
    ex += final(it, 'U-T6 example 1')
    U.add('ex', 'مثال 1 (من المذكرة)', ex)
    it = ITEMS['N52-E3-1']
    A = '(sec(x)*tan(x)/2+log(Abs(sec(x)+tan(x)))/2)'
    ex = question(it, 'U-T6 example 2')
    ex += short_steps(it, [
        ('سلسلة sec مع $n=3$:', r'\int\sec^{3}x\,dx=\frac{\sec x\tan x}{2}+\frac12\int\sec x\,dx',
         [('diff(sec(x)*tan(x)/2,x)+sec(x)/2', 'sec(x)**3')]),
        ('و $\\int\\sec x\\,dx=\\ln|\\sec x+\\tan x|$ من الجدول:', r'\frac{\sec x\tan x}{2}+\frac12\ln\left|\sec x+\tan x\right|+C',
         [('=ANS', A)])], 'U-T6 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('parts', 'sec(x)', 'sec(x)**2', 'sec(x)*tan(x)', 'tan(x)', '$u=\\sec x$ و $dv=\\sec^2x\\,dx$'),
        ('line', 'sec(x)*tan(x)-Integral(sec(x)*tan(x)**2,x)', 'القانون'),
        ('tex', r'I=\sec x\tan x-I+\int\sec x\,dx', [('sec(x)*tan(x)-%s+log(Abs(sec(x)+tan(x)))' % A, A)],
         '$\\tan^2x=\\sec^2x-1$ فيرجع $I=\\int\\sec^3x\\,dx$ (🧮 حل معادلة فيها التكامل نفسه)'),
        ('tex', r'2I=\sec x\tan x+\ln|\sec x+\tan x|', [('2*%s' % A, 'sec(x)*tan(x)+log(Abs(sec(x)+tan(x)))')], 'نجمع $I$ ونقسم على 2')],
        'U-T6 ex2')
    ex += final(it, 'U-T6 example 2')
    U.add('ex', 'مثال 2: sec³ (من المذكرة)', ex)
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
    U.add('short', '⚡ الاختصار', p(rich('الصفان الأخيران في جدول باسكال (النوع 23)، والإشارة $-$ أمام الكل في الحالتين.'))
          + box_memo('مثل tan و sec، وزد سالب.'))
    it = ITEMS['1446-S2-SE-Q2.4']
    ex = question(it, 'U-T7 example')
    ex += short_steps(it, [
        ('csc زوجي ($4=2\\cdot1+2$) ⇐ $u=\\cot x$، وإشارة $-$ أمام الكل، و $p$ = أس cot:', r'k=1,\quad p=4', [('2*1+2', '4')]),
        ('القوس $(1+u^2)^1$ كله $+$، والأسس تبدأ من $p+1=5$:', r'-\left(\frac{u^{5}}{5}+\frac{u^{7}}{7}\right)=-\frac{\cot^{5}x}{5}-\frac{\cot^{7}x}{7}+C',
         [('integrate(x**4*(1+x**2),x)', 'x**5/5+x**7/7'), ('=ANS', '-cot(x)**5/5-cot(x)**7/7')])], 'U-T7 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\cot^{4}x\csc^{4}x=\cot^{4}x\,(1+\cot^{2}x)\csc^{2}x', [('cot(x)**4*csc(x)**4', 'cot(x)**4*(1+cot(x)**2)*csc(x)**2')],
         'نحجز $\\csc^2x$ ونحوّل الباقي (🧮 متطابقات فيثاغورس)'),
        ('sub', 'cot(x)', '-csc(x)**2', '$u=\\cot x$، و $\\csc^2x\\,dx=-du$'),
        ('tex', r'=-\int u^{4}(1+u^{2})\,du=-\int\left(u^{4}+u^{6}\right)du', [('u**4*(1+u**2)', 'u**4+u**6')], 'نوزّع'),
        ('line', '-cot(x)**5/5-cot(x)**7/7', 'نكامل ونرجع $u$')], 'U-T7 ex')
    ex += final(it, 'U-T7 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', p(rich('$\\frac{d}{dx}\\cot x=-\\csc^2x$ و $\\frac{d}{dx}\\csc x=-\\csc x\\cot x$: السالب في الاثنين.')))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر الحجز، سطر $u$ و $du$ (بالسالب)، ثم الجواب.')))
    U.drill('1', 'N52-X08', 'G', 'إشارة سالبة أمام الكل، والقوس $(1+u^2)^2$.',
            first=r'\csc^{6}x=(1+\cot^{2}x)^{2}\csc^{2}x,\quad u=\cot x,\ du=-\csc^{2}x\,dx',
            claims=[('csc(x)**6', '(1+cot(x)**2)**2*csc(x)**2')])
    U.drill('2', 'N52-X09', 'P', 'cot فردي ⇐ $u=\\csc x$، و $du=-\\csc x\\cot x\\,dx$.')
    U.drill('3', 'N52-E4-2', 'I', 'مثل التمرين 2 مع $p=5-1=4$.')
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
        ('اقرأ الزاويتين:', r'm=7,\ n=5:\quad m-n=2,\quad m+n=12', [('7-5', '2'), ('7+5', '12')]),
        ('صف sin·cos: سالب نصف، وكل cos يُقسم على زاويته:', r'-\frac12\left[\frac{\cos2x}{2}+\frac{\cos12x}{12}\right]=-\frac{\cos2x}{4}-\frac{\cos12x}{24}+C',
         [('-(cos(2*x)/2+cos(12*x)/12)/2', '-cos(2*x)/4-cos(12*x)/24'), ('=ANS', '-cos(2*x)/4-cos(12*x)/24')])], 'U-T8 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'\sin7x\cos5x=\frac12\left[\sin2x+\sin12x\right]', [('sin(7*x)*cos(5*x)', '(sin(2*x)+sin(12*x))/2')],
         'متطابقة الضرب (🧮)'),
        ('line', '-cos(2*x)/4-cos(12*x)/24', '$\\int\\sin kx\\,dx=-\\frac1k\\cos kx$')], 'U-T8 ex')
    ex += final(it, 'U-T8 example')
    U.add('ex', 'مثال (من المذكرة)', ex)
    U.raw(alg('product-ids', 'متطابقات الضرب (المذكرة ص74)', [
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

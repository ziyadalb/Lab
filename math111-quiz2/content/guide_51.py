"""المذكرة الكاملة — الدرس 5.1: التكامل بالتجزئة.

Every type: the card (idea, sign, how it differs from the type before), the law or the fixed steps, an example solved
step by step with one operation per row (🧱), then the quick way only where it saves lines (types 12-14 and 19),
the box «before you hand in», the one-line summary, and the exercises.
"""
from booklet import di_table
from booklet_engine import ITEMS, arith, same_value
from guide_kit import Unit, contrast, final, method, pgref, question, rich, short_steps, shortcut, steps, tricks
from guide_rules import R
from guide_42 import box_memo
from html_kit import link, md, mi, p, ul


DI_RULES = ul([rich('عمود <b>D</b>: اشتق كثيرة الحدود (أو القوس) لين توصل صفر.'),
               rich('عمود <b>I</b>: كامل الدالة الثانية في كل صف.'),
               rich('اضرب كل خانة في D في الخانة اللي <b>تحتها قطريًا</b> في I. الإشارات بالترتيب: $+$ ثم $-$ ثم $+$ ثم $-$.'),
               'الصف اللي فيه صفر ما تضربه.'])


# ---------------------------------------------------------------- 12
def u_parts_linear():
    U = Unit('U-P1', 'فكرة التجزئة: كثيرة حدود خطية × دالة', '5.1', 'ص63', 3)
    U.add('idea', 'الفكرة', p(rich(
        'قاعدة الضرب في الاشتقاق $(uv)\'=u\'v+uv\'$ إذا قلبناها تكاملًا تطلع قاعدة التجزئة: '
        '$\\int u\\,dv=uv-\\int v\\,du$. عندك شيئان مضروبان: خلّ واحدًا <b>يصغر لما تشتقه</b> ($3x-2$ يصير 3)، '
        'والثاني <b>سهل تكامله</b> ($\\sinh x$ يصير $\\cosh x$).')))
    U.add('sign', 'العلامة', p(rich('قوس فيه $x$ بدون أس، مثل $(3x-2)$، مضروب في $e^{kx}$ أو $\\sin kx$ أو $\\cos kx$ أو $\\sinh kx$ أو $\\cosh kx$ أو $\\sec^2x$.'))
          + contrast([(r'\int x\cosh x\,dx', 'تجزئة', '$x$ ليست مشتقة شيء داخل cosh'),
                      (r'\int x\cosh(x^{2})\,dx', 'تعويض $u=x^2$', '$x$ موجودة كمشتقة لـ $x^2$ (تقريبًا)')]))
    U.prev('أول نوع في 5.1. في 4.2 كان كل تكامل تعويض. هنا شيئان مضروبان والتعويض ما يمشي، فنستعمل قانون التجزئة.')
    U.add('note', 'تذكير: تكاملات تحتاجها', p(rich('التجزئة تنتهي دائمًا بتكاملات من الجدول الأساسي ($e^{kx}$ و $\\sin kx$ و $\\cos kx$ '
                                                 'و $\\sinh kx$ و $\\cosh kx$ و $\\sec^2x$). الجدول وأمثلته وتمارينه في ')
                                            + link('P-B2', '📚 ب2 ص ' + pgref('P-B2')) + '.')
          + p(rich('مع sin الإشارة سالبة: $\\int\\sin x\\,dx=-\\cos x$. مع sinh موجبة: $\\int\\sinh x\\,dx=\\cosh x$.'), 'small'))
    U.add('short', '📐 القانون: التجزئة', md(r'\int u\,dv=uv-\int v\,du') + method([
        'اختر $u$: الشي اللي <b>يصغر لما تشتقه</b> (هنا القوس). والباقي مع $dx$ هو $dv$.',
        'اشتق $u$ تطلع $du$، وكامل $dv$ تطلع $v$. اكتب الأربعة في مربع.',
        'عوّض في القانون: $uv-\\int v\\,du$.',
        'كامل التكامل الباقي (صار أسهل)، ولا تنسَ $+C$.'], '$u$ اللي يصغر بالاشتقاق، و $dv$ اللي تعرف تكامله.',
        tricks_=['<b>LIATE يختار لك $u$:</b> L = ln، ثم I = Inverse (دالة عكسية)، ثم A = Algebraic ($x$ وقواه)، '
                 'ثم T = Trig (sin و cos)، ثم E = Exponential ($e^x$، ومعها sinh و cosh). اللي يجي أول في الترتيب هو $u$. '
                 'مثال: $(3x-2)\\sinh x$ فيها A و E، و A أول، فـ $u=3x-2$.'], label='U-P1'))
    it = ITEMS['1446-S1-SE-Q2.4']
    ex = question(it, 'U-P1 example')
    ex += steps(it, [
        ('parts', '3*x-2', 'sinh(x)', '3', 'cosh(x)', 'شيئان مضروبان، فنستعمل التجزئة. نختار $u$ القوس لأنه يصغر لما نشتقه، والباقي $dv=\\sinh x\\,dx$.'),
        ('line', '(3*x-2)*cosh(x)-Integral(3*cosh(x),x)', 'نعوّض في القانون $uv-\\int v\\,du$: $u\\cdot v=(3x-2)\\cosh x$، و $v\\,du=3\\cosh x\\,dx$.'),
        ('line', '(3*x-2)*cosh(x)-3*Integral(cosh(x),x)', 'الرقم 3 مضروب، فيطلع قدّام التكامل ومعه إشارته.'),
        ('line', '(3*x-2)*cosh(x)-3*sinh(x)', 'تكامل $\\cosh x$ هو $\\sinh x$.')], 'U-P1 ex')
    ex += final(it, 'U-P1 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('short', '⚡ الطريقة السريعة: جدول DI', shortcut(
        it, 'U-P1 ex',
        saves='هنا يوفر سطر بس. لكن تتعلمه على مثال سهل، عشان في النوع 13 يوفر عليك تجزئتين كاملتين.',
        origin='كل سطر في الجدول = تجزئة وحدة من 🧱. عمود D هو $u$ ومشتقاته، وعمود I هو $dv$ وتكاملاته. '
               'والإشارة تتبادل لأن القانون $uv-\\int v\\,du$ فيه ناقص.',
        steps_=['نرسم ثلاث أعمدة: الإشارة، و D، و I.',
                'في D: نكتب القوس، ونشتقه لين يصير صفر.',
                'في I: نكتب الدالة الثانية، ونكاملها في كل سطر.',
                'نضرب كل خانة في D في خانة I اللي <b>تحتها بسطر</b> (مايل ↘). الإشارات بالترتيب: $+$ ثم $-$ ثم $+$.'],
        example_html=di_table([('+', '3*x-2', 'sinh(x)'), ('-', '3', 'cosh(x)'), (r'\cdot', '0', 'sinh(x)')]),
        rows=[('عمود D: نشتق القوس لين يصير صفر.', r'3x-2\ \to\ 3\ \to\ 0', [('diff(3*x-2,x)', '3'), ('diff(3,x)', '0')]),
              ('عمود I: نكامل $\\sinh x$ في كل سطر.', r'\sinh x\ \to\ \cosh x\ \to\ \sinh x',
               [('integrate(sinh(x),x)', 'cosh(x)'), ('integrate(cosh(x),x)', 'sinh(x)')]),
              ('نضرب مايل: $(3x-2)$ في $\\cosh x$ بإشارة $+$، و 3 في $\\sinh x$ بإشارة $-$.', r'(+)\,(3x-2)\cosh x\qquad(-)\,3\sinh x',
               [('(3*x-2)*cosh(x)-3*sinh(x)', '(3*x-2)*cosh(x)+(-1)*3*sinh(x)')]),
              ('نجمع الحدين. نفس جواب 🧱 ✓', r'(3x-2)\cosh x-3\sinh x+C', [('=ANS', '(3*x-2)*cosh(x)-3*sinh(x)')])],
        memo='D تنزل للصفر، I تتكامل، واضرب مايل $+\\ -\\ +$.',
        never=['إذا الدالة الثانية ln أو دالة عكسية: ما نعرف نكاملها في عمود I. هذي النوعين 14 و17.',
               'مع $e^{ax}\\sin bx$: عمود D ما يوصل صفر أبد. هذا النوع 19.'],
        paper='في هذا النوع اكتب التجزئة العادية، لأنها قصيرة. والجدول تتأكد فيه من جوابك.',
        tries=[(r'\int x\,e^{x}\,dx', r'x\,e^{x}-e^{x}', [('diff(x*exp(x)-exp(x),x)', 'x*exp(x)')]),
               (r'\int(3x+1)\cos x\,dx', r'(3x+1)\sin x+3\cos x', [('diff((3*x+1)*sin(x)+3*cos(x),x)', '(3*x+1)*cos(x)')])]))
    same_value('diff((3*x-2)*cosh(x)-3*sinh(x),x)', '(3*x-2)*sinh(x)', 'U-P1 check')
    U.add('ok', '✔ تأكد', p(rich('اشتق جوابك: $3\\cosh x+(3x-2)\\sinh x-3\\cosh x=(3x-2)\\sinh x$. رجع السؤال ✓')))
    U.add('trap', '⚠️ الفخ', ul([rich('لا تنسَ الرقم اللي يطلع من مشتقة القوس (هنا 3)، ولا $+C$.'),
                                rich('مع sin و cos: $\\int\\sin x\\,dx=-\\cos x$، فانتبه للإشارات.')]))
    U.add('paper', '✍️ في ورقة الكويز', md(r'\begin{array}{l}u=3x-2\qquad dv=\sinh x\,dx\\du=3\,dx\qquad v=\cosh x\end{array}')
          + md(r'\int(3x-2)\sinh x\,dx=(3x-2)\cosh x-3\int\cosh x\,dx \\ \qquad=(3x-2)\cosh x-3\sinh x+C'))
    U.gist('قوس مثل $(3x-2)$ مضروب في $e^{kx}$ أو sin أو cos أو sinh أو cosh', '$u=$ القوس، و $dv=$ الباقي',
           'القانون $uv-\\int v\\,du$، والتكامل الباقي سهل')
    U.drill('1', 'N51-E1', 'G', '$u=x$ و $dv=\\cos x\\,dx$.',
            first=r'u=x,\quad dv=\cos x\,dx,\quad du=dx,\quad v=\sin x',
            claims=[('diff(x,x)', '1'), ('integrate(cos(x),x)', 'sin(x)')],
            sol_rows=[('line', 'x*sin(x)-Integral(sin(x),x)', 'نعوّض في القانون $uv-\\int v\\,du$: $uv=x\\sin x$، و $v\\,du=\\sin x\\,dx$.'),
                      ('tex', r'=x\sin x-\left(-\cos x\right)', [('diff(x*sin(x)-(-cos(x)),x)', 'x*cos(x)')],
                       'تكامل $\\sin x$ هو $-\\cos x$. نحطه بين قوسين عشان ما نضيع السالب.'),
                      ('line', 'x*sin(x)+cos(x)', 'سالب في سالب = موجب.')])
    U.drill('2', '1446-S2-SE-Q2.3', 'P', '$u=2x-1$ و $dv=\\cosh x\\,dx$.',
            sol_rows=[('parts', '2*x-1', 'cosh(x)', '2', 'sinh(x)', 'نختار $u$ القوس لأنه يصغر لما نشتقه، و $dv=\\cosh x\\,dx$.'),
                      ('line', '(2*x-1)*sinh(x)-Integral(2*sinh(x),x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
                      ('line', '(2*x-1)*sinh(x)-2*Integral(sinh(x),x)', 'الرقم 2 مضروب، فيطلع قدّام التكامل.'),
                      ('line', '(2*x-1)*sinh(x)-2*cosh(x)', 'تكامل $\\sinh x$ هو $\\cosh x$، بدون سالب.')])
    U.drill('3', 'N51-X04', 'I', '$u=x+1$ و $dv=\\sec^2x\\,dx$.',
            sol_rows=[('parts', 'x+1', 'sec(x)**2', '1', 'tan(x)', '$u$ القوس. و $dv=\\sec^2x\\,dx$، وتكامله $v=\\tan x$.'),
                      ('line', '(x+1)*tan(x)-Integral(tan(x),x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
                      ('tex', r'-\int\tan x\,dx=-\left(-\ln|\cos x|\right)=+\ln|\cos x|', [('diff(-log(cos(x)),x)', 'tan(x)')],
                       'تكامل $\\tan x$ هو $-\\ln|\\cos x|$. وسالب في سالب = موجب، فيصير الجواب $(x+1)\\tan x+\\ln|\\cos x|+C$.')])
    return U


# ---------------------------------------------------------------- 13
def u_parts_di():
    U = Unit('U-P2', 'كثيرة حدود درجة 2 أو 3: جدول DI', '5.1', 'ص63–64، تمارين 2 و3', 3)
    U.add('idea', 'الفكرة', p(rich('مع $x^2$ أو $x^3$ نحتاج التجزئة مرتين أو ثلاثًا. جدول DI يرتّب كل التجزئات في جدول واحد: '
                                   'عمود نشتق فيه كثيرة الحدود حتى الصفر، وعمود نكامل فيه الدالة الثانية.')))
    U.add('sign', 'العلامة', p(rich('$x^2$ أو $x^3$ (أو كثيرة حدود من درجتهما) × $e^{kx}$ أو sin أو cos أو sinh أو cosh.')))
    U.prev('مثل النوع 12، لكن القوس فيه $x^2$ أو $x^3$. فالتجزئة تتكرر مرتين أو ثلاث، وجدول DI يسويها كلها مرة وحدة.')
    U.add('short', '🧭 الطريقة: التجزئة تتكرر', method([
        'أول تجزئة: $u=$ كثيرة الحدود، و $dv=$ الباقي.',
        'التكامل الباقي فيه $x$ بقوة أقل: سوّ تجزئة ثانية بنفس الاختيار.',
        'كرّر لين تختفي $x$.',
        'وزّع السالب على القوس: يقلب إشارة كل حد داخله.'],
        tricks_=[('<b>دورة sin و cos في عمود I:</b> $\\sin\\to-\\cos\\to-\\sin\\to\\cos\\to\\sin$. ومع $kx$ نقسم على $k$ في كل سطر: '
                  '$\\sin2x\\to-\\frac12\\cos2x\\to-\\frac14\\sin2x\\to\\frac18\\cos2x$.',
                  [('integrate(sin(x),x)', '-cos(x)'), ('integrate(-cos(x),x)', '-sin(x)'), ('integrate(-sin(x),x)', 'cos(x)'),
                   ('integrate(sin(2*x),x)', '-cos(2*x)/2'), ('integrate(-cos(2*x)/2,x)', '-sin(2*x)/4'), ('integrate(-sin(2*x)/4,x)', 'cos(2*x)/8')])],
        label='U-P2'))
    it = ITEMS['1445-S1-FE-Q2.2']
    ex = question(it, 'U-P2 example')
    ex += steps(it, [
        ('parts', 'x**2', 'cosh(x)', '2*x', 'sinh(x)', 'أول تجزئة: $u=x^2$ لأنه يصغر لما نشتقه، و $dv=\\cosh x\\,dx$.'),
        ('line', 'x**2*sinh(x)-Integral(2*x*sinh(x),x)', 'نعوّض في القانون. التكامل الباقي فيه $x$ بس، فنعيد التجزئة.'),
        ('parts', '2*x', 'sinh(x)', '2', 'cosh(x)', 'ثاني تجزئة على التكامل الباقي: $u=2x$، و $dv=\\sinh x\\,dx$.'),
        ('line', 'x**2*sinh(x)-(2*x*cosh(x)-Integral(2*cosh(x),x))', 'نحط ناتج التجزئة الثانية داخل قوس، لأن قدّامه سالب.'),
        ('line', 'x**2*sinh(x)-2*x*cosh(x)+Integral(2*cosh(x),x)', 'نوزّع السالب على القوس: $-(2x\\cosh x)$ تصير $-2x\\cosh x$، و $-(-\\int)$ تصير $+\\int$.'),
        ('line', 'x**2*sinh(x)-2*x*cosh(x)+2*sinh(x)', 'آخر تكامل سهل: $\\int2\\cosh x\\,dx=2\\sinh x$.')], 'U-P2 ex')
    ex += final(it, 'U-P2 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('short', '⚡ الطريقة السريعة: جدول DI', shortcut(
        it, 'U-P2 ex',
        saves='بدل تجزئتين، وقوس، وسالب في سالب (6 أسطر في 🧱)، تكتب جدول وسطر جواب.',
        origin='نفس جدول النوع 12. كل سطر = تجزئة من 🧱: سطر $x^2$ هو التجزئة الأولى، وسطر $2x$ هو الثانية. '
               'والإشارات تتبادل لأن كل تجزئة فيها ناقص. وهذا بالضبط اللي سويناه في 🧱 لما وزّعنا السالب على القوس.',
        steps_=['نرسم ثلاث أعمدة: الإشارة، و D، و I.',
                'في D: نكتب كثيرة الحدود، ونشتقها لين توصل صفر.',
                'في I: نكتب الدالة الثانية، ونكاملها في كل سطر (نفس عدد سطور D).',
                'نضرب كل خانة في D في خانة I اللي <b>تحتها بسطر</b> (مايل ↘). الإشارات بالترتيب: $+\\ -\\ +\\ -$. وصف الصفر ما نضربه.'],
        example_html=di_table([('+', 'x**2', 'cosh(x)'), ('-', '2*x', 'sinh(x)'), ('+', '2', 'cosh(x)'), (r'\cdot', '0', 'sinh(x)')]),
        rows=[('عمود D: نشتق $x^2$ لين يصير صفر.', r'x^{2}\ \to\ 2x\ \to\ 2\ \to\ 0', [('diff(x**2,x)', '2*x'), ('diff(2*x,x)', '2'), ('diff(2,x)', '0')]),
              ('عمود I: نكامل $\\cosh x$ في كل سطر. تكامل cosh هو sinh، وتكامل sinh هو cosh.', r'\cosh x\ \to\ \sinh x\ \to\ \cosh x\ \to\ \sinh x',
               [('integrate(cosh(x),x)', 'sinh(x)'), ('integrate(sinh(x),x)', 'cosh(x)')]),
              ('نضرب مايل: كل خانة في D في اللي تحتها بسطر في I، بإشارات $+$ ثم $-$ ثم $+$.',
               r'(+)\,x^{2}\sinh x\quad(-)\,2x\cosh x\quad(+)\,2\sinh x',
               [('x**2*sinh(x)-2*x*cosh(x)+2*sinh(x)', 'x**2*sinh(x)+(-1)*(2*x)*cosh(x)+2*sinh(x)')]),
              ('نجمع الحدود. نفس جواب 🧱 ✓', r'x^{2}\sinh x-2x\cosh x+2\sinh x+C', [('=ANS', 'x**2*sinh(x)-2*x*cosh(x)+2*sinh(x)')])],
        memo='D تنزل للصفر، I تتكامل، واضرب مايل $+\\ -\\ +$.',
        never=['إذا الدالة الثانية ln أو دالة عكسية: ما نعرف نكاملها في عمود I. هذي النوعين 14 و17.',
               'مع $e^{ax}\\sin bx$: عمود D ما يوصل صفر أبد. هذا النوع 19.'],
        paper='اكتب الجدول نفسه، ثم سطر الجواب. الجدول هو التجزئة المتكررة مرتبة.',
        ask='اكتب العمود أو الجواب',
        tries=[(r'\text{D: }x^{3}', r'x^{3}\to3x^{2}\to6x\to6\to0', [('diff(x**3,x)', '3*x**2'), ('diff(3*x**2,x)', '6*x'), ('diff(6*x,x)', '6')]),
               (r'\text{I: }\cos3x', r'\cos3x\to\tfrac13\sin3x\to-\tfrac19\cos3x\to-\tfrac{1}{27}\sin3x',
                [('integrate(cos(3*x),x)', 'sin(3*x)/3'), ('integrate(sin(3*x)/3,x)', '-cos(3*x)/9'), ('integrate(-cos(3*x)/9,x)', '-sin(3*x)/27')]),
               (r'\int x^{2}e^{-x}\,dx', r'-x^{2}e^{-x}-2x\,e^{-x}-2e^{-x}', [('diff(-x**2*exp(-x)-2*x*exp(-x)-2*exp(-x),x)', 'x**2*exp(-x)')])]))
    U.add('trap', '⚠️ الفخ', ul([rich('أكثر غلط في عمود I: إشارة تكامل sin. $\\int\\sin x\\,dx=-\\cos x$، وهذي الإشارة تنضرب مع إشارة الجدول.'),
                                'الجدول يوقف لما يوصل عمود D صفر. صف الصفر ما تضربه.']))
    U.add('paper', '✍️ في ورقة الكويز', p('اكتب جدول DI نفسه، ثم سطر الجواب. الجدول هو التجزئة المتكررة نفسها، بس مرتبة.'))
    U.gist('$x^2$ أو $x^3$ مضروبة في $e^{kx}$ أو sin أو cos أو sinh أو cosh', 'جدول DI: D تشتق، و I تكامل',
           'اضرب قطريًا بإشارات $+\\,-\\,+$')
    U.drill('1', 'N51-E2', 'G', 'كل تكاملات $e^x$ هي $e^x$؛ الإشارات $+\\,-\\,+$.',
            first=r'D:\ x^{2},\ 2x,\ 2,\ 0\qquad I:\ e^{x},\ e^{x},\ e^{x},\ e^{x}',
            claims=[('diff(x**2,x)', '2*x'), ('integrate(exp(x),x)', 'exp(x)')],
            sol_rows=[('tex', r'(+)\,x^{2}e^{x}\quad(-)\,2x\,e^{x}\quad(+)\,2e^{x}',
                       [('x**2*exp(x)-2*x*exp(x)+2*exp(x)', 'x**2*exp(x)+(-1)*2*x*exp(x)+2*exp(x)')],
                       'نضرب مايل: كل خانة في D في اللي تحتها بسطر في I، بإشارات $+$ ثم $-$ ثم $+$.'),
                      ('line', 'x**2*exp(x)-2*x*exp(x)+2*exp(x)', 'نجمع الحدود الثلاثة.'),
                      ('line', '(x**2-2*x+2)*exp(x)', 'نطلّع $e^x$ عامل مشترك من كل الحدود.')])
    U.drill('2', 'N51-X03', 'P', 'أربعة صفوف قبل الصفر: $x^3,\\ 3x^2,\\ 6x,\\ 6$.',
            sol_rows=[('tex', r'D:\ x^{3},\ 3x^{2},\ 6x,\ 6,\ 0\qquad I:\ e^{x},\ e^{x},\ e^{x},\ e^{x},\ e^{x}',
                       [('diff(x**3,x)', '3*x**2'), ('diff(3*x**2,x)', '6*x'), ('diff(6*x,x)', '6')], 'جدول DI: نشتق $x^3$ لين الصفر، وتكامل $e^x$ هو $e^x$ دايم.'),
                      ('tex', r'+x^{3}e^{x}-3x^{2}e^{x}+6x\,e^{x}-6e^{x}',
                       [('diff(x**3*exp(x)-3*x**2*exp(x)+6*x*exp(x)-6*exp(x),x)', 'x**3*exp(x)')], 'نضرب قطريًا بإشارات $+$ ثم $-$ ثم $+$ ثم $-$.'),
                      ('line', '(x**3-3*x**2+6*x-6)*exp(x)', 'نطلّع $e^x$ عامل مشترك من كل الحدود.')])
    U.drill('3', 'N51-X02', 'I', 'تكاملات $\\sin2x$: $-\\frac12\\cos2x$، ثم $-\\frac14\\sin2x$، ثم $\\frac18\\cos2x$.',
            sol_rows=[('tex', r'D:\ x^{2}-1,\ 2x,\ 2,\ 0', [('diff(x**2-1,x)', '2*x'), ('diff(2*x,x)', '2')],
                       'عمود D: نشتق $x^2-1$ لين يصير صفر.'),
                      ('tex', r'I:\ \sin2x,\ -\tfrac12\cos2x,\ -\tfrac14\sin2x,\ \tfrac18\cos2x',
                       [('integrate(sin(2*x),x)', '-cos(2*x)/2'), ('integrate(-cos(2*x)/2,x)', '-sin(2*x)/4'),
                        ('integrate(-sin(2*x)/4,x)', 'cos(2*x)/8')],
                       'عمود I: هنا التريك: دورة sin و cos، ونقسم على 2 في كل سطر.'),
                      ('tex', r'(x^{2}-1)\left(-\frac{\cos2x}{2}\right)-2x\left(-\frac{\sin2x}{4}\right)+2\cdot\frac{\cos2x}{8}',
                       [('(x**2-1)*(-cos(2*x)/2)-2*x*(-sin(2*x)/4)+2*cos(2*x)/8', '-(x**2-1)*cos(2*x)/2+x*sin(2*x)/2+cos(2*x)/4')],
                       'نضرب مايل بإشارات $+$ ثم $-$ ثم $+$.'),
                      ('line', '-(x**2-1)*cos(2*x)/2+x*sin(2*x)/2+cos(2*x)/4', 'نبسّط: سالب في سالب = موجب، و $\\frac28=\\frac14$.')])
    return U


# ---------------------------------------------------------------- 14
def u_qaws():
    U = Unit('U-P3', 'قوة × ln', '5.1', 'ص64، تمارين 5–7', 3)
    U.add('idea', 'الفكرة', p(rich('$\\ln$ تكاملها صعب لكن مشتقتها سهلة ($\\frac1x$). فدائمًا $u=\\ln$، و $dv$ = القوة. '
                                   'بعد التجزئة يصير التكامل الباقي قوة بسيطة.')))
    U.add('sign', 'العلامة', p(rich('$x^n$ (حتى لو $n$ سالب) مضروبة في $\\ln|ax|$.')))
    U.prev('مثل النوعين 12 و13 (قوة × دالة)، لكن الدالة هنا ln. والاختيار ينقلب: ln هي $u$ لأن تكاملها صعب.')
    U.add('short', '🧭 الطريقة', method([
        '$u=\\ln|x|$، فـ $du=\\frac{dx}{x}$.',
        '$dv=x^n\\,dx$، فـ $v=\\frac{x^{n+1}}{n+1}$ (قاعدة القوة).',
        'عوّض في القانون $uv-\\int v\\,du$.',
        '$v\\,du$ يصير قوة بسيطة: كاملها.'],
        tricks_=['<b>LIATE:</b> L = ln تجي قبل A = $x$، فـ $u=\\ln$ دايم في هذا النوع. وحتى لو الكسر $\\frac{\\ln x}{x^2}$، اكتبه $x^{-2}\\ln x$ أول.'],
        label='U-P3'))
    it = ITEMS['N51-E3']
    ex = question(it, 'U-P3 example 1')
    ex += steps(it, [
        ('parts', 'log(Abs(x))', 'x**2', '1/x', 'x**3/3', 'ln تكاملها صعب ومشتقتها سهلة، فنختارها $u$. والباقي $dv=x^2dx$، وتكامله $\\frac{x^3}{3}$.', 't'),
        ('line', 'x**3*log(Abs(x))/3-Integral(x**2/3,x)', 'نعوّض في القانون. و $v\\,du=\\frac{x^3}{3}\\cdot\\frac1x=\\frac{x^2}{3}$: القسمة على $x$ تنقص الأس 1.'),
        ('line', 'x**3*log(Abs(x))/3-x**3/9', 'نكامل: $\\int\\frac{x^2}{3}dx=\\frac13\\cdot\\frac{x^3}{3}=\\frac{x^3}{9}$.')], 'U-P3 ex1')
    ex += final(it, 'U-P3 example 1')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    ex1_it = it
    it = ITEMS['1446-S1-SE-Q2.5']
    ex = question(it, 'U-P3 example 2')
    ex += steps(it, [
        ('parts', 'log(x)', 'x**(-2)', '1/x', '-1/x', 'نكتب الكسر كضرب: $\\frac{\\ln x}{x^2}=x^{-2}\\ln x$. نختار $u=\\ln x$، و $dv=x^{-2}dx$، وتكامله $\\frac{x^{-1}}{-1}=-\\frac1x$.', 't'),
        ('line', '-log(x)/x-Integral(-1/x**2,x)', 'نعوّض في القانون. و $v\\,du=-\\frac1x\\cdot\\frac1x=-\\frac{1}{x^2}$.'),
        ('line', '-log(x)/x+Integral(1/x**2,x)', 'سالب في سالب = موجب.'),
        ('line', '-log(x)/x-1/x', 'نكامل: $\\int x^{-2}dx=\\frac{x^{-1}}{-1}=-\\frac1x$. نزيد الأس 1 ونقسم عليه.')], 'U-P3 ex2')
    ex += final(it, 'U-P3 example 2')
    U.add('ex', '🧱 مثال 2: أس سالب (اختبار سابق)', ex)
    U.add('short', '⚡ الطريقة السريعة: قوة × ln في سطر', shortcut(
        ex1_it, 'U-P3 ex1',
        saves='بدل 3 أسطر، الجواب في سطر. وتتأكد فيه من جوابك في الكويز.',
        origin='في مثال 1 طلع الجواب $\\frac{x^3}{3}\\ln|x|-\\frac{x^3}{9}$. نطلّع $\\frac{x^3}{3}$ عامل مشترك، فيصير '
               '$\\frac{x^3}{3}\\left(\\ln|x|-\\frac13\\right)$. ونفس الشكل يطلع مع أي أس: $v$ ضرب ($\\ln$ ناقص 1 على مقام $v$).',
        steps_=['نكامل القوة لحالها: نزيد الأس 1 ونقسم عليه. هذا $v$.',
                'نكتب الجواب: $v$ × ($\\ln|x|$ ناقص 1 على نفس الرقم اللي قسمنا عليه).'],
        on='على مثال 1 في 🧱:',
        rows=[('نكامل القوة لحالها: الأس 2 يصير 3، ونقسم على 3.', r'v=\frac{x^{3}}{3}', [('integrate(x**2,x)', 'x**3/3')]),
              ('نضرب $v$ في ($\\ln|x|$ ناقص 1 على 3). نفس جواب 🧱 ✓', r'\frac{x^{3}}{3}\left(\ln|x|-\frac13\right)+C',
               [('=ANS', 'x**3/3*(log(Abs(x))-Rational(1,3))'), R('xn ln')])],
        after_rows=p(rich('وعلى مثال 2: $v=\\frac{x^{-1}}{-1}=-\\frac1x$، والرقم اللي قسمنا عليه $-1$. فالجواب '
                          '$-\\frac1x\\left(\\ln x-\\frac{1}{-1}\\right)=-\\frac1x\\left(\\ln x+1\\right)$، نفس جواب 🧱 ✓'
                          + arith('', [('-1/x*(log(x)+1)', '-log(x)/x-1/x')], 'U-P3 ex2 quick')), 'small'),
        memo='كامل القوة، واضرب في ($\\ln$ ناقص واحد على نفس المقام).',
        never=['مع $\\frac{\\ln x}{x}$: الأس $-1$، والمقام يصير صفر. هذا تعويض $u=\\ln x$، والجواب $\\frac{(\\ln x)^2}{2}$.',
               'مع $\\ln|2x|$ نفس الطريقة، بس تكتب $\\ln|2x|$ داخل القوس.'],
        paper='اكتب سطر التجزئة ($u$ و $dv$ و $du$ و $v$) ثم الجواب. والسريع تتأكد فيه.',
        tries=[(r'\int x^{4}\ln x\,dx', r'\frac{x^{5}}{5}\left(\ln x-\frac15\right)', [('diff(x**5/5*(log(x)-Rational(1,5)),x)', 'x**4*log(x)', 't')]),
               (r'\int\frac{\ln x}{x^{3}}\,dx', r'-\frac{1}{2x^{2}}\left(\ln x+\frac12\right)',
                [('diff(-1/(2*x**2)*(log(x)+Rational(1,2)),x)', 'log(x)/x**3', 't')]),
               (r'\int\ln x\,dx', r'x\left(\ln x-1\right)', [('diff(x*(log(x)-1),x)', 'log(x)', 't')])]))
    U.add('trap', '⚠️ الفخ', ul([rich('$n=-1$، أي $\\int\\frac{\\ln|x|}{x}dx$، ليست تجزئة: عوّض $u=\\ln|x|$ فالجواب $\\frac{(\\ln|x|)^2}{2}$.'),
                                rich('مع $\\ln|2x|$ المشتقة $\\frac1x$ (الـ 2 تختفي)، والطريقة كما هي.')]))
    U.add('paper', '✍️ في ورقة الكويز', md(r'\begin{array}{l}u=\ln|x|\qquad dv=x^{2}dx\\du=\frac1x\,dx\qquad v=\frac{x^{3}}{3}\end{array}')
          + p('ثم سطر القانون والجواب.'))
    U.gist('$x^n$ (حتى لو سالب) مضروبة في $\\ln|ax|$', '$u=\\ln$، و $dv=x^n\\,dx$', 'القانون، و $v\\,du$ قوة بسيطة')
    U.drill('1', '1445-S2-SE-Q2.5', 'G', '$u=\\ln|x|$ و $dv=x\\,dx$.',
            first=r'u=\ln|x|,\quad dv=x\,dx,\quad du=\frac{dx}{x},\quad v=\frac{x^{2}}{2}',
            claims=[('diff(log(x),x)', '1/x', 't'), ('integrate(x,x)', 'x**2/2')],
            sol_rows=[('line', 'x**2*log(Abs(x))/2-Integral(x/2,x)', 'نعوّض في القانون. و $v\\,du=\\frac{x^2}{2}\\cdot\\frac1x=\\frac x2$.'),
                      ('line', 'x**2*log(Abs(x))/2-x**2/4', 'نكامل: $\\int\\frac x2\\,dx=\\frac12\\cdot\\frac{x^2}{2}=\\frac{x^2}{4}$.'),
                      ('tex', r'\frac{x^{2}}{2}\left(\ln|x|-\frac12\right)=\frac{x^{2}}{2}\ln|x|-\frac{x^{2}}{4}',
                       [('x**2/2*(log(x)-Rational(1,2))', 'x**2*log(x)/2-x**2/4')], '✔ تأكد بالسريع: القانون الجاهز مع $n=1$')])
    U.drill('2', 'N51-X07', 'P', '$u=\\ln|x|$ و $dv=x^{-4}dx$.',
            sol_rows=[('parts', 'log(Abs(x))', 'x**(-4)', '1/x', '-1/(3*x**3)', '$u=\\ln|x|$. و $dv=x^{-4}dx$، وتكامله $\\frac{x^{-3}}{-3}=-\\frac{1}{3x^3}$.', 't'),
                      ('line', '-log(Abs(x))/(3*x**3)-Integral(-1/(3*x**4),x)', 'نعوّض في القانون. و $v\\,du=-\\frac{1}{3x^3}\\cdot\\frac1x=-\\frac{1}{3x^4}$.'),
                      ('line', '-log(Abs(x))/(3*x**3)+Integral(1/(3*x**4),x)', 'سالب في سالب = موجب.'),
                      ('line', '-log(Abs(x))/(3*x**3)-1/(9*x**3)', 'نكامل: $\\frac13\\cdot\\frac{x^{-3}}{-3}=-\\frac{1}{9x^3}$.'),
                      ('tex', r'\frac{x^{-3}}{-3}\left(\ln|x|-\frac{1}{-3}\right)=-\frac{\ln|x|}{3x^{3}}-\frac{1}{9x^{3}}',
                       [('x**(-3)/(-3)*(log(x)-1/(-3))', '-log(x)/(3*x**3)-1/(9*x**3)')], '✔ تأكد بالسريع: $n=-4$')])
    U.drill('3', '1447-S1-SE-Q2.7', 'I', '$u=\\ln|2x|$ ومشتقتها $\\frac1x$.',
            sol_rows=[('parts', 'log(Abs(2*x))', 'x**3', '1/x', 'x**4/4', '$u=\\ln|2x|$، ومشتقتها $\\frac{2}{2x}=\\frac1x$. و $dv=x^3dx$، وتكامله $\\frac{x^4}{4}$.', 't'),
                      ('line', 'x**4*log(Abs(2*x))/4-Integral(x**3/4,x)', 'نعوّض في القانون. و $v\\,du=\\frac{x^4}{4}\\cdot\\frac1x=\\frac{x^3}{4}$.'),
                      ('line', 'x**4*log(Abs(2*x))/4-x**4/16', 'نكامل: $\\frac14\\cdot\\frac{x^4}{4}=\\frac{x^4}{16}$.')])
    return U


# ---------------------------------------------------------------- 15
def u_ln_alone():
    U = Unit('U-P4', 'ln وحدها، و (ln x)²، و ln(1+x²)', '5.1', 'ص64، تمارين 5 و16 ومثال 4', 4)
    U.add('idea', 'الفكرة', p(rich('ما فيه ضرب ظاهر؟ اكتب $dv=dx$ (واحد مخفي): $u=\\ln$ و $v=x$.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\ln|x|\\,dx$ أو $\\int(\\ln|x|)^2dx$ أو $\\int\\ln(1+x^2)dx$: ln وحدها.')))
    U.prev('مثل النوع 14، لكن ما فيه قوة مضروبة: ln وحدها. فنخترع الضرب: $dv=dx$.')
    U.add('short', '🧭 الطريقة', method([
        'ما فيه ضرب؟ اكتب $dv=dx$ (كأنك ضربت في 1).',
        '$u=$ ln، و $du=$ مشتقتها. و $v=x$.',
        'عوّض في القانون $uv-\\int v\\,du$.',
        '$x\\cdot du$ يصير بسيطًا. ومع $\\ln(x^2+c)$ تحتاج قسمة بسيطة.'], '$\\int\\ln|x|\\,dx=x\\ln|x|-x$. احفظ هذا السطر.',
        tricks_=['<b>LIATE:</b> ما فيه غير ln، فهي $u$. واللي يبقى $dx$ لحاله، فـ $dv=dx$ و $v=x$.',
                 ('<b>⚡ النوع 14 يشتغل هنا:</b> $\\ln x=x^0\\ln x$، فـ $v=\\frac{x^1}{1}=x$، والجواب $x(\\ln x-1)$.',
                  [('diff(x*(log(x)-1),x)', 'log(x)', 't')])], label='U-P4'))
    it = ITEMS['N51-X05']
    ex = question(it, 'U-P4 example')
    ex += steps(it, [
        ('parts', 'log(Abs(x))', '1', '1/x', 'x', 'ما فيه ضرب ظاهر، فنعتبرها $\\ln|x|\\cdot1$. نختار $u=\\ln|x|$، و $dv=dx$، فـ $v=x$.', 't'),
        ('line', 'x*log(Abs(x))-Integral(1,x)', 'نعوّض في القانون. و $v\\,du=x\\cdot\\frac1x=1$، فالتكامل الباقي سهل.'),
        ('line', 'x*log(Abs(x))-x', 'تكامل 1 هو $x$.')], 'U-P4 ex')
    ex += final(it, 'U-P4 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', p(rich('$\\int\\ln|x|\\,dx\\ne\\frac1x$. هذه مشتقتها، ليست تكاملها.')))
    U.add('paper', '✍️ في ورقة الكويز', md(r'u=\ln|x|,\ dv=dx,\ du=\frac1x\,dx,\ v=x'))
    U.gist('ln وحدها: $\\ln|x|$ أو $(\\ln|x|)^2$ أو $\\ln(x^2+c)$', '$u=\\ln$، و $dv=dx$ (واحد مخفي)', 'القانون، ثم بسّط $x\\cdot du$')
    U.drill('1', 'G-79', 'G', '$u=\\ln|3x|$ و $dv=dx$.',
            first=r'u=\ln|3x|,\quad dv=dx,\quad du=\frac{dx}{x},\quad v=x', claims=[('diff(log(3*x),x)', '1/x', 't')],
            sol_rows=[('line', 'x*log(Abs(3*x))-Integral(1,x)', 'نعوّض في القانون. و $x\\cdot\\frac1x=1$.'),
                      ('line', 'x*log(Abs(3*x))-x', 'تكامل 1 هو $x$.')])
    U.drill('2', 'N51-X16', 'P', 'التكامل الباقي $2\\int\\ln|x|\\,dx$ هو المثال.',
            sol_rows=[('parts', 'log(Abs(x))**2', '1', '2*log(Abs(x))/x', 'x', '$u=(\\ln|x|)^2$. مشتقتها بقاعدة السلسلة: 2 × $\\ln|x|$ × $\\frac1x$. و $dv=dx$.', 't'),
                      ('line', 'x*log(Abs(x))**2-Integral(2*log(Abs(x)),x)', 'نعوّض في القانون. و $x\\cdot\\frac{2\\ln|x|}{x}=2\\ln|x|$: الـ $x$ تروح مع الـ $x$.'),
                      ('line', 'x*log(Abs(x))**2-2*(x*log(Abs(x))-x)', 'التكامل الباقي هو المثال: $\\int\\ln|x|\\,dx=x\\ln|x|-x$. نحطه بين قوسين.'),
                      ('line', 'x*log(Abs(x))**2-2*x*log(Abs(x))+2*x', 'نوزّع $-2$ على القوس: يضرب كل حد، وسالب في سالب = موجب.')])
    U.drill('3', 'N51-E4', 'I', '$v\\,du=\\frac{2x^2}{1+x^2}$ ثم قسمة.',
            sol_rows=[('parts', 'log(1+x**2)', '1', '2*x/(1+x**2)', 'x', '$u=\\ln(1+x^2)$، ومشتقتها $\\frac{2x}{1+x^2}$. و $dv=dx$، فـ $v=x$.'),
                      ('line', 'x*log(1+x**2)-Integral(2*x**2/(1+x**2),x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
                      ('line', 'x*log(1+x**2)-Integral(2-2/(1+x**2),x)', 'البسط والمقام نفس الدرجة، فنقسم: $2x^2=2(1+x^2)-2$، يعني $\\frac{2x^2}{1+x^2}=2-\\frac{2}{1+x^2}$.'),
                      ('line', 'x*log(1+x**2)-2*x+2*atan(x)', 'نكامل حدًا حدًا: $\\int2\\,dx=2x$، و $\\int\\frac{2}{1+x^2}dx=2\\tan^{-1}x$.')])
    U.drill('4', 'G-80', 'I', 'مثل التمرين 3 مع 4 بدل 1.',
            sol_rows=[('parts', 'log(x**2+4)', '1', '2*x/(x**2+4)', 'x', '$u=\\ln(x^2+4)$، ومشتقتها $\\frac{2x}{x^2+4}$. و $dv=dx$، فـ $v=x$.'),
                      ('line', 'x*log(x**2+4)-Integral(2*x**2/(x**2+4),x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
                      ('line', 'x*log(x**2+4)-Integral(2-8/(x**2+4),x)', 'نقسم: $2x^2=2(x^2+4)-8$، يعني $\\frac{2x^2}{x^2+4}=2-\\frac{8}{x^2+4}$.'),
                      ('line', 'x*log(x**2+4)-2*x+4*atan(x/2)', 'نكامل حدًا حدًا. والثاني من قانون 3.4: $\\int\\frac{dx}{x^2+a^2}=\\frac1a\\tan^{-1}\\frac xa$ مع $a=2$، و $8\\cdot\\frac12=4$.')])
    return U


# ---------------------------------------------------------------- 16
def u_definite():
    U = Unit('U-P5', 'تكامل محدد بالتجزئة', '5.1', 'من الاختبارات', 4)
    U.add('idea', 'الفكرة', p(rich('أوجد التكامل كأنه غير محدد ($F$)، ثم عوّض الحد الأعلى ناقص الحد الأدنى: $F(b)-F(a)$. لا $+C$.')))
    U.add('sign', 'العلامة', p(rich('$\\int_a^b$ بأرقام فوق وتحت، والدالة من أنواع التجزئة.')))
    U.prev('أي نوع من 12 إلى 15، بس فيه حدود فوق وتحت. تحل كالعادة، ثم تعوّض الأرقام.')
    U.add('short', '📐 القانون', md(r'\int_{a}^{b}f(x)\,dx=F(b)-F(a)') + box_memo('أعلى ناقص أدنى، وانتبه لسالب في سالب.')
          + tricks(['احسب الجواب كامل أول ($F$)، ثم عوّض الحدّين مرة وحدة: (الأعلى) ناقص (الأدنى). لا تعوّض في نص الحل.',
                    ('أرقام تختصر عليك: $\\ln1=0$، و $\\ln e=1$، و $e^0=1$، و $\\sinh0=0$، و $\\cosh0=1$.',
                     [('log(1)', '0'), ('log(E)', '1'), ('exp(0)', '1'), ('sinh(0)', '0'), ('cosh(0)', '1')])], 'U-P5'))
    it = ITEMS['1445-S1-SE-Q2.3']
    ex = question(it, 'U-P5 example')
    ex += steps(it, [
        ('tex', r'F(x)=\frac{x^{4}}{4}\left(\ln x-\frac14\right)', [('diff(x**4/4*(log(x)-Rational(1,4)),x)', 'x**3*log(x)')],
         'نوجد $F$ بالتجزئة: $u=\\ln x$ و $dv=x^3dx$ (النوع 14)'),
        ('tex', r'F(e)=\frac{e^{4}}{4}\left(1-\frac14\right)=\frac{3e^{4}}{16}', [('E**4/4*(log(E)-Rational(1,4))', '3*E**4/16')],
         'نعوّض الحد الأعلى، و $\\ln e=1$'),
        ('tex', r'F(1)=\frac14\left(0-\frac14\right)=-\frac{1}{16}', [('Rational(1,4)*(log(1)-Rational(1,4))', '-Rational(1,16)')],
         'نعوّض الحد الأدنى، و $\\ln1=0$'),
        ('tex', r'F(e)-F(1)=\frac{3e^{4}}{16}-\left(-\frac{1}{16}\right)=\frac{3e^{4}}{16}+\frac{1}{16}',
         [('3*E**4/16-(-Rational(1,16))', '3*E**4/16+Rational(1,16)')], 'نطرح: سالب في سالب = موجب')], 'U-P5 ex')
    ex += final(it, 'U-P5 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', ul(['لا تكتب +C في المحدد.', rich('$F(b)-F(a)$ وليس العكس، وضع $F(a)$ داخل قوس قبل الطرح.')]))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر $F(x)$، ثم سطر $F(b)-F(a)$ بالأرقام، ثم الجواب.')))
    U.gist('$\\int_a^b$ بأرقام فوق وتحت', 'أوجد $F(x)$ كأنه بدون حدود', '$F(b)-F(a)$، بدون $+C$')
    U.drill('1', 'G-05', 'G', '$F(1)=0$ و $F(0)=-1$.', first=r'F(x)=(x-1)e^{x}', claims=[('diff((x-1)*exp(x),x)', 'x*exp(x)')],
            sol_rows=[('tex', r'F(1)=(1-1)e^{1}=0', [('(1-1)*E', '0')], 'نعوّض الحد الأعلى $x=1$ في $F$.'),
                      ('tex', r'F(0)=(0-1)e^{0}=-1', [('(0-1)*exp(0)', '-1')], 'نعوّض الحد الأدنى $x=0$. و $e^0=1$.'),
                      ('tex', r'F(1)-F(0)=0-(-1)=1', [('0-(-1)', '1')], 'سالب في سالب = موجب.')])
    U.drill('2', 'G-81', 'P', '$u=x$ و $dv=\\cos x\\,dx$، و $\\sin\\frac\\pi2=1$.',
            sol_rows=[('tex', r'F(x)=x\sin x+\cos x', [('diff(x*sin(x)+cos(x),x)', 'x*cos(x)')], 'نوجد $F$ بالتجزئة: $u=x$ و $dv=\\cos x\\,dx$ (مثل النوع 12).'),
                      ('tex', r'F\left(\frac{\pi}{2}\right)=\frac{\pi}{2}\cdot1+0=\frac{\pi}{2}', [('pi/2*sin(pi/2)+cos(pi/2)', 'pi/2')],
                       'الحد الأعلى: $\\sin\\frac\\pi2=1$ و $\\cos\\frac\\pi2=0$'),
                      ('tex', r'F(0)=0+1=1', [('0*sin(0)+cos(0)', '1')], 'الحد الأدنى: $\\cos0=1$'),
                      ('tex', r'F\left(\frac{\pi}{2}\right)-F(0)=\frac{\pi}{2}-1', [('pi/2-1', 'pi/2-1')], 'الأعلى ناقص الأدنى. وهذا الجواب.')])
    U.drill('3', 'G-06', 'I', '$F=x\\ln x-x$ (النوع 15).',
            sol_rows=[('tex', r'F(x)=x\ln x-x', [('diff(x*log(x)-x,x)', 'log(x)')], 'نوجد $F$: ln وحدها، مثل النوع 15.'),
                      ('tex', r'F(e)=e\cdot1-e=0', [('E*log(E)-E', '0')], 'الحد الأعلى، و $\\ln e=1$'),
                      ('tex', r'F(1)=1\cdot0-1=-1', [('1*log(1)-1', '-1')], 'الحد الأدنى، و $\\ln1=0$'),
                      ('tex', r'F(e)-F(1)=0-(-1)=1', [('0-(-1)', '1')], 'سالب في سالب = موجب.')])
    U.drill('4', 'G-82', 'I', '$u=\\ln x$ و $dv=x^2dx$.',
            sol_rows=[('tex', r'F(x)=\frac{x^{3}}{3}\ln x-\frac{x^{3}}{9}', [('diff(x**3*log(x)/3-x**3/9,x)', 'x**2*log(x)')], 'نوجد $F$: قوة × ln، مثل النوع 14.'),
                      ('tex', r'F(e)=\frac{e^{3}}{3}-\frac{e^{3}}{9}=\frac{2e^{3}}{9}', [('E**3*log(E)/3-E**3/9', '2*E**3/9')], 'الحد الأعلى، و $\\ln e=1$'),
                      ('tex', r'F(1)=0-\frac19=-\frac19', [('log(1)/3-Rational(1,9)', '-Rational(1,9)')], 'الحد الأدنى، و $\\ln1=0$'),
                      ('tex', r'F(e)-F(1)=\frac{2e^{3}}{9}+\frac19=\frac{2e^{3}+1}{9}', [('2*E**3/9+Rational(1,9)', '(2*E**3+1)/9')],
                       'سالب في سالب = موجب.')])
    return U


# ---------------------------------------------------------------- 17
def u_rafeeq():
    U = Unit('U-P6', 'دالة عكسية وحدها', '5.1', 'ص64–65، تمارين 8–10', 4)
    U.add('idea', 'الفكرة', p(rich('الدالة العكسية تكاملها غير معروف لكن مشتقتها معروفة. فهي $u$، و $dv=dx$ (واحد مخفي). '
                                   'يبقى تكامل $x$ × مشتقتها، وهذا تعويض بسيط.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\tan^{-1}x\\,dx$ أو $\\int\\sin^{-1}x\\,dx$ أو $\\int\\cosh^{-1}x\\,dx$… الدالة وحدها.'))
          + contrast([(r'\int\cosh^{-1}x\,dx', 'تجزئة (هنا)', 'الدالة وحدها'),
                      (r'\int\frac{\cosh^{-1}x}{\sqrt{x^{2}-1}}dx', 'تعويض (النوع 9)', 'مشتقتها موجودة')]))
    U.prev('نفس فكرة النوع 15 ($dv=dx$)، لكن بدل ln عندك دالة عكسية.')
    U.add('short', '🧭 الطريقة', method([
        'الدالة العكسية وحدها، فنختارها $u$، و $dv=dx$.',
        '$du=$ مشتقتها (من جدول 3.4 أو 4.2)، و $v=x$.',
        'عوّض في القانون: $x\\cdot$ الدالة $-\\int x\\cdot$ مشتقتها.',
        'التكامل الباقي تعويض: $w=$ ما تحت الجذر أو المقام (ب2).'],
        tricks_=['<b>LIATE:</b> I = الدالة العكسية تجي قبل كل شي، فهي $u$. وما فيه غيرها، فـ $dv=dx$.',
                 ('<b>التكامل الباقي دايم تعويض:</b> $w$ = اللي تحت الجذر أو المقام. مثال: $\\int\\frac{x\\,dx}{\\sqrt{x^2-1}}$ مع $w=x^2-1$ '
                  'يطلع $\\sqrt{x^2-1}$.', [('diff(sqrt(x**2-1),x)', 'x/sqrt(x**2-1)', '1+t')])], label='U-P6'))
    it = ITEMS['1445-S1-SE-Q2.5']
    ex = question(it, 'U-P6 example')
    ex += steps(it, [
        ('parts', 'acosh(x)', '1', '1/sqrt(x**2-1)', 'x', 'الدالة العكسية تكاملها مو معروف ومشتقتها معروفة، فنختارها $u$. و $dv=dx$، فـ $v=x$.', '1+t'),
        ('line', 'x*acosh(x)-Integral(x/sqrt(x**2-1),x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
        ('tex', r'w=x^{2}-1,\ dw=2x\,dx:\quad\int\frac{x\,dx}{\sqrt{x^{2}-1}}=\frac12\int w^{-1/2}dw=\sqrt{w}',
         [('diff(sqrt(x**2-1),x)', 'x/sqrt(x**2-1)', '1+t')], 'التكامل الباقي بتعويض $w$ = ما تحت الجذر'),
        ('line', 'x*acosh(x)-sqrt(x**2-1)', 'نرجع $w=x^2-1$، ونحط الناتج مكان التكامل الباقي.')], 'U-P6 ex')
    ex += final(it, 'U-P6 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('مع sec⁻¹ يبقى $\\int\\frac{dx}{\\sqrt{x^2-1}}=\\cosh^{-1}x$ (ربط مع 4.2).'),
                                rich('انتبه للإشارة: $\\int\\frac{x}{\\sqrt{1-x^2}}dx=-\\sqrt{1-x^2}$ (سالب).')]))
    U.add('paper', '✍️ في ورقة الكويز', md(r'u=\cosh^{-1}x,\ dv=dx,\ du=\frac{dx}{\sqrt{x^{2}-1}},\ v=x') + p('ثم القانون والجواب.'))
    U.gist('دالة عكسية وحدها: $\\tan^{-1}x$ أو $\\sin^{-1}x$ أو $\\cosh^{-1}x$…', '$u=$ الدالة، و $dv=dx$', 'القانون، ثم تعويض $w$')
    U.drill('1', '1446-S2-SE-Q2.8', 'G', '$\\int\\frac{x}{1+x^2}dx=\\frac12\\ln(1+x^2)$.',
            first=r'u=\tan^{-1}x,\ dv=dx,\ du=\frac{dx}{1+x^{2}},\ v=x', claims=[('diff(atan(x),x)', '1/(1+x**2)')],
            sol_rows=[('line', 'x*atan(x)-Integral(x/(1+x**2),x)', 'نعوّض في القانون $uv-\\int v\\,du$'),
                      ('tex', r'w=1+x^{2},\ dw=2x\,dx:\quad\int\frac{x\,dx}{1+x^{2}}=\frac12\int\frac{dw}{w}=\frac12\ln(1+x^{2})',
                       [('diff(log(1+x**2)/2,x)', 'x/(1+x**2)')], 'التكامل الباقي بتعويض $w$ = المقام'),
                      ('line', 'x*atan(x)-log(1+x**2)/2', 'نجمع الحدين، وهذا الجواب.')])
    U.drill('2', '1447-S1-SE-Q2.5', 'P', '$\\int\\frac{x}{\\sqrt{1-x^2}}dx=-\\sqrt{1-x^2}$.',
            sol_rows=[('parts', 'asin(x)', '1', '1/sqrt(1-x**2)', 'x', '$u=\\sin^{-1}x$، ومشتقتها $\\frac{1}{\\sqrt{1-x^2}}$. و $dv=dx$، فـ $v=x$.', 't/(1+t)'),
                      ('line', 'x*asin(x)-Integral(x/sqrt(1-x**2),x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
                      ('tex', r'\int\frac{x\,dx}{\sqrt{1-x^{2}}}=-\sqrt{1-x^{2}}', [('diff(-sqrt(1-x**2),x)', 'x/sqrt(1-x**2)', 't/(1+t)')],
                       '$w=1-x^2$ و $dw=-2x\\,dx$: السالب يطلع (ب2)'),
                      ('line', 'x*asin(x)+sqrt(1-x**2)', 'سالب في سالب = موجب.')])
    U.drill('3', 'N51-X09', 'I', 'مشتقة $\\sec^{-1}x$ هي $\\frac{1}{x\\sqrt{x^2-1}}$ (لـ $x>1$).',
            sol_rows=[('parts', 'asec(x)', '1', '1/(x*sqrt(x**2-1))', 'x', '$u=\\sec^{-1}x$، ومشتقتها $\\frac{1}{x\\sqrt{x^2-1}}$ (لما $x>1$). و $dv=dx$.', '1+t'),
                      ('line', 'x*asec(x)-Integral(1/sqrt(x**2-1),x)', 'نعوّض في القانون. و $v\\,du=x\\cdot\\frac{1}{x\\sqrt{x^2-1}}=\\frac{1}{\\sqrt{x^2-1}}$: الـ $x$ تروح.'),
                      ('line', 'x*asec(x)-acosh(x)', 'قانون 4.2: $\\int\\frac{dx}{\\sqrt{x^2-a^2}}=\\cosh^{-1}\\frac xa$، وهنا $a=1$.')])
    return U


# ---------------------------------------------------------------- 18
def u_xinv():
    U = Unit('U-P7', 'x × دالة عكسية', '5.1', 'ص65، مثال 6 وتمرين 10', 4)
    U.add('idea', 'الفكرة', p(rich('مثل النوع السابق لكن $dv=x\\,dx$ فـ $v=\\frac{x^2}{2}$. التكامل الباقي غالبًا يحتاج قسمة بسيطة.')))
    U.add('sign', 'العلامة', p(rich('$\\int x\\tanh^{-1}x\\,dx$ أو $\\int x\\sec^{-1}x\\,dx$… $x$ مضروبة في دالة عكسية.')))
    U.prev('مثل النوع 17، لكن مع $x$ مضروبة: $dv=x\\,dx$ بدل $dx$.')
    U.add('short', '🧭 الطريقة', method([
        '$u=$ الدالة العكسية، و $dv=x\\,dx$.',
        '$du=$ مشتقتها، و $v=\\frac{x^2}{2}$.',
        'عوّض في القانون، وطلّع $\\frac12$ برّا التكامل الباقي.',
        'التكامل الباقي: قسمة بسيطة أو تعويض $w$.'],
        tricks_=['<b>LIATE:</b> I = الدالة العكسية قبل A = $x$، فـ $u$ = الدالة العكسية، و $dv=x\\,dx$.',
                 ('<b>أضف واطرح في البسط:</b> $\\frac{x^2}{1+x^2}=\\frac{x^2+1-1}{1+x^2}=1-\\frac{1}{1+x^2}$. وكل حد له قانون.',
                  [('x**2/(1+x**2)', '1-1/(1+x**2)')])], label='U-P7'))
    it = ITEMS['1446-S2-FE-Q2.2']
    ex = question(it, 'U-P7 example')
    ex += steps(it, [
        ('parts', 'atanh(x)', 'x', '1/(1-x**2)', 'x**2/2', 'نختار الدالة العكسية $u$، ومشتقتها $\\frac{1}{1-x^2}$. و $dv=x\\,dx$، فـ $v=\\frac{x^2}{2}$.', 't/(1+t)'),
        ('line', 'x**2*atanh(x)/2-Integral(x**2/(2*(1-x**2)),x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
        ('line', 'x**2*atanh(x)/2-Integral(-Rational(1,2)+1/(2*(1-x**2)),x)', 'البسط والمقام نفس الدرجة، فنقسم: $x^2=-(1-x^2)+1$، يعني $\\frac{x^2}{1-x^2}=-1+\\frac{1}{1-x^2}$.'),
        ('line', 'x**2*atanh(x)/2-(-x/2+atanh(x)/2)', 'نكامل كل حد: $\\int-\\frac12dx=-\\frac x2$، و $\\int\\frac{dx}{1-x^2}=\\tanh^{-1}x$ (قانون 4.2 مع $a=1$).'),
        ('line', 'x**2*atanh(x)/2+x/2-atanh(x)/2', 'نوزّع السالب على القوس: يقلب إشارة الحدين.')], 'U-P7 ex')
    ex += final(it, 'U-P7 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', ul(['لا تنسَ $\\frac12$ قدّام التكامل الباقي.',
                                rich('في مذكرة د. طارق ص65 خطأ مطبعي: $\\sqrt{1-x^2}$ بدل $\\sqrt{x^2-1}$ في مثال $x\\sec^{-1}x$؛ الجواب النهائي صحيح.')]))
    U.add('paper', '✍️ في ورقة الكويز', md(r'u=\tanh^{-1}x,\ dv=x\,dx,\ du=\frac{dx}{1-x^{2}},\ v=\frac{x^{2}}{2}'))
    U.gist('$x$ مضروبة في دالة عكسية', '$u=$ الدالة، و $dv=x\\,dx$', 'القانون مع $\\frac12$، ثم قسمة أو تعويض')
    U.drill('1', 'G-07', 'G', '$\\frac{x^2}{1+x^2}=1-\\frac{1}{1+x^2}$.',
            first=r'u=\tan^{-1}x,\ dv=x\,dx,\ du=\frac{dx}{1+x^{2}},\ v=\frac{x^{2}}{2}', claims=[('diff(atan(x),x)', '1/(1+x**2)')],
            sol_rows=[('line', 'x**2*atan(x)/2-Integral(x**2/(2*(1+x**2)),x)',
                       'نعوّض في القانون $uv-\\int v\\,du$. و $v\\,du=\\frac{x^2}{2}\\cdot\\frac{1}{1+x^2}$.'),
                      ('tex', r'\frac{x^{2}}{1+x^{2}}=\frac{x^{2}+1-1}{1+x^{2}}=1-\frac{1}{1+x^{2}}', [('x**2/(1+x**2)', '1-1/(1+x**2)')],
                       'هنا التريك: نضيف 1 ونطرحه في البسط، فينفصل الكسر.'),
                      ('line', 'x**2*atan(x)/2-Integral(Rational(1,2)-1/(2*(1+x**2)),x)', 'نحط الكسر الجديد في التكامل.'),
                      ('line', 'x**2*atan(x)/2-x/2+atan(x)/2',
                       'نكامل: $\\int1\\,dx=x$، و $\\int\\frac{dx}{1+x^2}=\\tan^{-1}x$. وسالب في سالب = موجب.')])
    U.drill('2', 'N51-X10', 'P', 'لـ $x>0$: $v\\,du=-\\frac{x}{2\\sqrt{1+x^2}}$.',
            sol_rows=[('parts', 'acsch(x)', 'x', '-1/(x*sqrt(1+x**2))', 'x**2/2', '$u=\\operatorname{csch}^{-1}x$، ومشتقتها $-\\frac{1}{x\\sqrt{1+x^2}}$ (لما $x>0$). و $dv=x\\,dx$.', 't'),
                      ('line', 'x**2*acsch(x)/2+Integral(x/(2*sqrt(1+x**2)),x)', 'نعوّض في القانون. المشتقة فيها سالب، وسالب في سالب = موجب.'),
                      ('tex', r'\int\frac{x\,dx}{2\sqrt{1+x^{2}}}=\frac12\sqrt{1+x^{2}}', [('diff(sqrt(1+x**2)/2,x)', 'x/(2*sqrt(1+x**2))')],
                       'تعويض $w=1+x^2$ (ب2)'),
                      ('line', 'x**2*acsch(x)/2+sqrt(1+x**2)/2', 'نجمع الحدين، وهذا الجواب.')])
    U.drill('3', 'N51-E6', 'I', '$v\\,du=\\frac{x}{2\\sqrt{x^2-1}}$.',
            sol_rows=[('parts', 'asec(x)', 'x', '1/(x*sqrt(x**2-1))', 'x**2/2', '$u=\\sec^{-1}x$، ومشتقتها $\\frac{1}{x\\sqrt{x^2-1}}$ (لما $x>1$). و $dv=x\\,dx$.', '1+t'),
                      ('line', 'x**2*asec(x)/2-Integral(x/(2*sqrt(x**2-1)),x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
                      ('tex', r'\int\frac{x\,dx}{2\sqrt{x^{2}-1}}=\frac12\sqrt{x^{2}-1}', [('diff(sqrt(x**2-1)/2,x)', 'x/(2*sqrt(x**2-1))', '1+t')],
                       'تعويض $w=x^2-1$ (ب2)'),
                      ('line', 'x**2*asec(x)/2-sqrt(x**2-1)/2', 'نجمع الحدين، وهذا الجواب.')])
    return U


# ---------------------------------------------------------------- 19
def u_dawaran():
    U = Unit('U-P8', 'أسية × sin أو cos (التكامل يرجع لنفسه)', '5.1', 'ص65، تمارين 11 و12', 4)
    U.add('idea', 'الفكرة', p(rich('بالتجزئة مرتين يرجع التكامل الأصلي $I$ نفسه، فنحل معادلة. الطريقة السريعة هي نتيجة هذه المعادلة جاهزة.')))
    U.add('sign', 'العلامة', p(rich('$e^{ax}$ مضروبة في $\\sin bx$ أو $\\cos bx$.')))
    U.prev('مثل النوع 12 (شيئان مضروبان)، لكن ما فيه قوس يصغر. التجزئة مرتين ترجعك للتكامل نفسه.')
    U.add('short', '🧭 الطريقة', method([
        'أول تجزئة: $u=$ sin أو cos، و $dv=e^{ax}dx$.',
        'ثاني تجزئة على التكامل الباقي، <b>بنفس الاختيار</b> (المثلثية $u$).',
        'يرجع التكامل الأصلي: سمّه $I$.',
        'اجمع $I$ في طرف واحد، ثم اقسم.'],
        tricks_=['<b>نفس الاختيار في التجزئتين:</b> إذا اخترت المثلثية $u$ في الأولى، اخترها $u$ في الثانية بعد. لو بدّلت، ترجع لنفس السؤال.'],
        label='U-P8'))
    it = ITEMS['1447-S2-FE-Q2.3']
    I_ = '(2*exp(2*x)*sin(x)/5-exp(2*x)*cos(x)/5)'
    ex = question(it, 'U-P8 example')
    ex += steps(it, [
        ('parts', 'sin(x)', 'exp(2*x)', 'cos(x)', 'exp(2*x)/2', 'أول تجزئة: $u=\\sin x$، و $dv=e^{2x}dx$، فـ $v=\\frac{e^{2x}}{2}$.'),
        ('line', 'exp(2*x)*sin(x)/2-Integral(exp(2*x)*cos(x)/2,x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
        ('parts', 'cos(x)', 'exp(2*x)', '-sin(x)', 'exp(2*x)/2', 'التكامل الباقي نفس الشكل. نسوي تجزئة ثانية بنفس الاختيار: المثلثية هي $u$.'),
        ('tex', r'I=\frac{e^{2x}\sin x}{2}-\frac{e^{2x}\cos x}{4}-\frac14I',
         [('exp(2*x)*sin(x)/2-exp(2*x)*cos(x)/4-%s/4' % I_, I_)], 'نعوّض. رجع التكامل الأصلي نفسه، فنسمّيه $I$.'),
        ('tex', r'\frac54I=\frac{e^{2x}\sin x}{2}-\frac{e^{2x}\cos x}{4}', [('Rational(5,4)*%s' % I_, 'exp(2*x)*sin(x)/2-exp(2*x)*cos(x)/4')],
         'ننقل $\\frac14I$ للطرف الأول: $I+\\frac14I=\\frac54I$.'),
        ('tex', r'I=\frac45\left(\frac{e^{2x}\sin x}{2}-\frac{e^{2x}\cos x}{4}\right)', [('Rational(4,5)*(exp(2*x)*sin(x)/2-exp(2*x)*cos(x)/4)', I_)],
         'نضرب الطرفين في $\\frac45$ عشان يبقى $I$ لحاله.')], 'U-P8 ex')
    ex += final(it, 'U-P8 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    rule = md(r"\int e^{ax}f\,dx=\frac{e^{ax}\left(a\,f-f'\right)}{a^{2}+b^{2}}+C")
    rule += p(rich('$f$ = الدالة ($\\sin bx$ أو $\\cos bx$)، و $f\'$ = مشتقتها. مع cos ما تحتاج تحفظ إشارة: مشتقة $\\cos bx$ فيها سالب، '
                   'فـ «ناقص مشتقتها» يصير زائد. مثال: $\\int e^{x}\\cos2x\\,dx$ قوسها $\\cos2x+2\\sin2x$.'
                   + arith('', [('1*cos(2*x)-diff(cos(2*x),x)', 'cos(2*x)+2*sin(2*x)')], 'U-P8 cos sign')), 'small')
    U.add('short', '⚡ الطريقة السريعة: قاعدة وحدة لـ sin و cos', shortcut(
        it, 'U-P8 ex',
        saves='بدل تجزئتين وحل معادلة (6 أسطر في 🧱)، الجواب في سطر.',
        origin='في 🧱 حلّينا المعادلة بالأرقام: $\\frac54I=\\ldots$ ثم ضربنا في $\\frac45$. لو حلّيناها مرة وحدة بحروف، '
               'يطلع قانون واحد يشتغل مع sin ومع cos:',
        origin_html=rule,
        steps_=['نقرأ $a$ = الرقم مع $x$ في الأسية، و $b$ = الرقم مع $x$ داخل sin أو cos.',
                'نحسب المقام: $a^2+b^2$.',
                'نكتب القوس: ($a$ × الدالة) ناقص (مشتقة الدالة).',
                'الجواب = $e^{ax}$ × القوس ÷ المقام.'],
        rows=[('نقرأ الرقمين ونحسب المقام: الأسية $e^{2x}$ فيها 2، و $\\sin x$ فيها 1.', r'a=2,\quad b=1,\quad a^{2}+b^{2}=4+1=5',
               [('2**2+1**2', '5')]),
              ('القوس: $2\\times\\sin x$ ناقص مشتقة $\\sin x$، ومشتقتها $\\cos x$.', r'2\sin x-\cos x',
               [('2*sin(x)-diff(sin(x),x)', '2*sin(x)-cos(x)')]),
              ('الجواب = $e^{2x}$ × القوس ÷ 5. نفس جواب 🧱 ✓', r'\frac{e^{2x}}{5}\left(2\sin x-\cos x\right)+C',
               [('=ANS', 'exp(2*x)*(2*sin(x)-cos(x))/5'), R('dawaran one sin'), R('dawaran one cos')])],
        memo='المقام $a^2+b^2$، والقوس: $a$ × الدالة ناقص مشتقتها.',
        never=['مع sinh أو cosh ما ينفع. هذا النوع 20: اكتبها بالأسس.',
               'مع $e^{-x}$: $a=-1$، و $a^2=1$. لا تنسى السالب في «$a$ × الدالة».'],
        paper='إذا السؤال يقول by parts: اكتب التجزئتين والمعادلة، والسريع يعطيك الجواب الصح قبل. وإذا ما حدد: سطر القانون بالأرقام.',
        tries=[(r'\int e^{3x}\cos x\,dx', r'\frac{e^{3x}}{10}\left(3\cos x+\sin x\right)',
                [('diff(exp(3*x)*(3*cos(x)+sin(x))/10,x)', 'exp(3*x)*cos(x)')]),
               (r'\int e^{-x}\sin x\,dx', r'-\frac{e^{-x}}{2}\left(\sin x+\cos x\right)',
                [('diff(-exp(-x)*(sin(x)+cos(x))/2,x)', 'exp(-x)*sin(x)')])]))
    U.add('trap', '⚠️ الفخ', ul(['في التجزئة الثانية لازم تختار نفس النوع لـ u (المثلثية)، وإلا ترجع للبداية.',
                                rich('لا تخلط مع $e^{ax}\\sinh bx$: هذا النوع 20.')]))
    U.add('paper', '✍️ في ورقة الكويز', p('اكتب التجزئتين ثم سطر المعادلة. وبعدها تأكد بالطريقة السريعة.'))
    U.gist('$e^{ax}$ مضروبة في $\\sin bx$ أو $\\cos bx$', 'تجزئة مرتين، و $u=$ المثلثية في المرتين',
           'يرجع $I$: اجمعه في طرف واحد واقسم')
    J1 = '(exp(x)*(cos(x)+sin(x))/2)'
    U.drill('1', 'N51-E7', 'G', '$u=\\cos x$ ثم $u=\\sin x$.',
            first=r'u=\cos x,\quad dv=e^{x}dx,\quad du=-\sin x\,dx,\quad v=e^{x}',
            claims=[('diff(cos(x),x)', '-sin(x)'), ('integrate(exp(x),x)', 'exp(x)')],
            sol_rows=[('line', 'exp(x)*cos(x)+Integral(exp(x)*sin(x),x)', 'نعوّض في القانون. المشتقة فيها سالب، وسالب في سالب = موجب.'),
                      ('parts', 'sin(x)', 'exp(x)', 'cos(x)', 'exp(x)', 'التكامل الباقي نفس الشكل. تجزئة ثانية بنفس الاختيار: $u=\\sin x$، و $dv=e^xdx$.'),
                      ('tex', r'I=e^{x}\cos x+e^{x}\sin x-I', [('exp(x)*cos(x)+exp(x)*sin(x)-%s' % J1, J1)], 'نعوّض. رجع التكامل الأصلي نفسه، فنسمّيه $I$.'),
                      ('tex', r'2I=e^{x}\cos x+e^{x}\sin x', [('2*%s' % J1, 'exp(x)*cos(x)+exp(x)*sin(x)')], 'نجمع $I$ في طرف واحد: $I+I=2I$.'),
                      ('line', 'exp(x)*(cos(x)+sin(x))/2', 'نقسم الطرفين على 2 عشان يبقى $I$ لحاله.'),
                      ('tex', r'\frac{e^{x}}{1^{2}+1^{2}}\left(1\cdot\cos x+1\cdot\sin x\right)', [('exp(x)/2*(cos(x)+sin(x))', J1)],
                       '✔ تأكد بالسريع: $a=1$ و $b=1$، والمقام 2. القوس: $\\cos x$ ناقص مشتقته ($-\\sin x$)، يعني $\\cos x+\\sin x$.')])
    J2 = '(exp(2*x)*(2*sin(3*x)-3*cos(3*x))/13)'
    U.drill('2', 'N51-X11', 'P', '$u=\\sin3x$ ثم $u=\\cos3x$.',
            sol_rows=[('parts', 'sin(3*x)', 'exp(2*x)', '3*cos(3*x)', 'exp(2*x)/2', 'أول تجزئة: $u=\\sin3x$، و $dv=e^{2x}dx$، فـ $v=\\frac{e^{2x}}{2}$.'),
                      ('line', 'exp(2*x)*sin(3*x)/2-Integral(3*exp(2*x)*cos(3*x)/2,x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
                      ('parts', 'cos(3*x)', 'exp(2*x)', '-3*sin(3*x)', 'exp(2*x)/2', 'تجزئة ثانية بنفس الاختيار: المثلثية $u=\\cos3x$.'),
                      ('tex', r'I=\frac{e^{2x}\sin3x}{2}-\frac34e^{2x}\cos3x-\frac94I',
                       [('exp(2*x)*sin(3*x)/2-Rational(3,4)*exp(2*x)*cos(3*x)-Rational(9,4)*%s' % J2, J2)], 'نعوّض. رجع التكامل الأصلي نفسه، فنسمّيه $I$.'),
                      ('tex', r'\frac{13}{4}I=\frac{e^{2x}\sin3x}{2}-\frac34e^{2x}\cos3x',
                       [('Rational(13,4)*%s' % J2, 'exp(2*x)*sin(3*x)/2-Rational(3,4)*exp(2*x)*cos(3*x)')], 'نجمع $I$ في طرف واحد: $I+\\frac94I=\\frac{13}{4}I$.'),
                      ('line', 'exp(2*x)*(2*sin(3*x)-3*cos(3*x))/13', 'نضرب الطرفين في $\\frac{4}{13}$ عشان يبقى $I$ لحاله.'),
                      ('tex', r'\frac{e^{2x}}{2^{2}+3^{2}}\left(2\sin3x-3\cos3x\right)', [('exp(2*x)/(2**2+3**2)*(2*sin(3*x)-3*cos(3*x))', J2)],
                       '✔ تأكد بالسريع: $a=2$ و $b=3$، والمقام 13. القوس: $2\\sin3x$ ناقص مشتقته ($3\\cos3x$).')])
    J3 = '(exp(5*x)*(5*cos(2*x)+2*sin(2*x))/29)'
    U.drill('3', 'N51-X12', 'I', '$u=\\cos2x$ ثم $u=\\sin2x$.',
            sol_rows=[('parts', 'cos(2*x)', 'exp(5*x)', '-2*sin(2*x)', 'exp(5*x)/5', 'أول تجزئة: $u=\\cos2x$، و $dv=e^{5x}dx$، فـ $v=\\frac{e^{5x}}{5}$.'),
                      ('line', 'exp(5*x)*cos(2*x)/5+Integral(2*exp(5*x)*sin(2*x)/5,x)', 'نعوّض في القانون. مشتقة cos فيها سالب، وسالب في سالب = موجب.'),
                      ('parts', 'sin(2*x)', 'exp(5*x)', '2*cos(2*x)', 'exp(5*x)/5', 'تجزئة ثانية بنفس الاختيار: المثلثية $u=\\sin2x$.'),
                      ('tex', r'I=\frac{e^{5x}\cos2x}{5}+\frac{2}{25}e^{5x}\sin2x-\frac{4}{25}I',
                       [('exp(5*x)*cos(2*x)/5+Rational(2,25)*exp(5*x)*sin(2*x)-Rational(4,25)*%s' % J3, J3)], 'نعوّض. رجع التكامل الأصلي نفسه، فنسمّيه $I$.'),
                      ('tex', r'\frac{29}{25}I=\frac{e^{5x}\cos2x}{5}+\frac{2}{25}e^{5x}\sin2x',
                       [('Rational(29,25)*%s' % J3, 'exp(5*x)*cos(2*x)/5+Rational(2,25)*exp(5*x)*sin(2*x)')], 'نجمع $I$ في طرف واحد: $I+\\frac{4}{25}I=\\frac{29}{25}I$.'),
                      ('line', 'exp(5*x)*(5*cos(2*x)+2*sin(2*x))/29', 'نضرب الطرفين في $\\frac{25}{29}$ عشان يبقى $I$ لحاله.'),
                      ('tex', r'\frac{e^{5x}}{5^{2}+2^{2}}\left(5\cos2x+2\sin2x\right)', [('exp(5*x)/(5**2+2**2)*(5*cos(2*x)+2*sin(2*x))', J3)],
                       '✔ تأكد بالسريع: $a=5$ و $b=2$، والمقام 29. القوس: $5\\cos2x$ ناقص مشتقته ($-2\\sin2x$)، يعني $5\\cos2x+2\\sin2x$.')])
    return U


# ---------------------------------------------------------------- 20
def u_nisfayn():
    U = Unit('U-P9', 'أسية × sinh أو cosh (اكتبها بالأسس)', '5.1', 'ص66، تمرينا 13 و14', 4)
    U.add('idea', 'الفكرة', p(rich('sinh و cosh أصلًا أسيات (تعريف 4.1). نكتبها بالتعريف، نضرب، فيصير مجموع أسيات سهل التكامل.')))
    U.add('sign', 'العلامة', p(rich('$e^{ax}$ مضروبة في $\\sinh bx$ أو $\\cosh bx$.')))
    U.prev('شكله مثل النوع 19، لكن sinh و cosh أصلًا أسيات. فما نحتاج تجزئة: نكتبها بالتعريف.')
    U.add('short', '🧭 الطريقة', method([
        'اكتب sinh أو cosh بالتعريف (أ3): $\\cosh u=\\frac{e^u+e^{-u}}{2}$، و $\\sinh u=\\frac{e^u-e^{-u}}{2}$.',
        'اضرب في الأسية: لما نضرب أسيات الأسس تنجمع.',
        'كامل كل حد: $\\int e^{kx}dx=\\frac{e^{kx}}{k}$.',
        'إذا طلع أس صفر، فالحد ثابت وتكامله $x$ × الثابت.'],
        tricks_=[('<b>لما نضرب أسيات الأسس تنجمع:</b> $e^{x}\\cdot e^{2x}=e^{3x}$، و $e^{x}\\cdot e^{-2x}=e^{-x}$.',
                  [('exp(x)*exp(2*x)', 'exp(3*x)'), ('exp(x)*exp(-2*x)', 'exp(-x)')]),
                 '<b>لا تخلط مع النوع 19:</b> sinh و cosh نكتبها بالأسس. أما sin و cos فلها الطريقة السريعة في النوع 19.'], label='U-P9'))
    it = ITEMS['1446-S1-SE-Q2.3']
    ex = question(it, 'U-P9 example')
    ex += steps(it, [
        ('tex', r'\cosh2x=\frac{e^{2x}+e^{-2x}}{2}', [('cosh(2*x)', '(exp(2*x)+exp(-2*x))/2')], 'cosh أصلًا أسيات. نكتبه بالتعريف من 4.1.'),
        ('tex', r'e^{x}\cosh2x=\frac{e^{3x}+e^{-x}}{2}', [('exp(x)*cosh(2*x)', '(exp(3*x)+exp(-x))/2')], 'نضرب في $e^x$. لما نضرب أسيات الأسس تنجمع: $x+2x=3x$ و $x-2x=-x$.'),
        ('tex', r'=\frac12e^{3x}+\frac12e^{-x}', [('(exp(3*x)+exp(-x))/2', 'exp(3*x)/2+exp(-x)/2')], 'نفصل الكسر حدين عشان نكامل كل واحد لحاله.'),
        ('tex', r'\int\frac12e^{3x}dx=\frac{e^{3x}}{6},\qquad \int\frac12e^{-x}dx=-\frac{e^{-x}}{2}',
         [('integrate(exp(3*x)/2,x)', 'exp(3*x)/6'), ('integrate(exp(-x)/2,x)', '-exp(-x)/2')], 'نكامل كل حد: نقسم على رقم $x$'),
        ('line', 'exp(3*x)/6-exp(-x)/2', 'نجمع الحدين، وهذا الجواب.')], 'U-P9 ex')
    ex += final(it, 'U-P9 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('إذا طلع أس صفر ($e^{0}=1$) فالحد ثابت ($\\frac12$ أو $-\\frac12$) وتكامله $\\pm\\frac{x}{2}$ (التمرين 3).'),
                                rich('مع sinh بين الحدين سالب.')]))
    U.add('paper', '✍️ في ورقة الكويز', p('سطر التعريف، ثم سطر الضرب، ثم الجواب. هكذا حلّ المفتاح الرسمي.'))
    U.gist('$e^{ax}$ مضروبة في $\\sinh bx$ أو $\\cosh bx$', 'اكتب sinh أو cosh بالتعريف', 'اضرب واجمع الأسس، ثم كامل كل حد')
    U.drill('1', 'N51-X13', 'G', 'مع sinh يكون بين الحدين سالب.',
            first=r'e^{3x}\sinh x=e^{3x}\cdot\frac{e^{x}-e^{-x}}{2}=\frac{e^{4x}-e^{2x}}{2}',
            claims=[('exp(3*x)*sinh(x)', '(exp(4*x)-exp(2*x))/2')],
            sol_rows=[('tex', r'\frac12\int e^{4x}dx=\frac{e^{4x}}{8}', [('integrate(exp(4*x)/2,x)', 'exp(4*x)/8')], 'الحد الأول: تكامل $e^{4x}$ هو $\\frac{e^{4x}}{4}$، والنص يخليه $\\frac{e^{4x}}{8}$.'),
                      ('tex', r'\frac12\int e^{2x}dx=\frac{e^{2x}}{4}', [('integrate(exp(2*x)/2,x)', 'exp(2*x)/4')], 'الحد الثاني: تكامل $e^{2x}$ هو $\\frac{e^{2x}}{2}$، والنص يخليه $\\frac{e^{2x}}{4}$.'),
                      ('line', 'exp(4*x)/8-exp(2*x)/4', 'وبين الحدين سالب، لأن تعريف sinh فيه سالب.')])
    U.drill('2', 'N51-X14', 'P', 'الأسان $6x$ و $-4x$.',
            sol_rows=[('tex', r'e^{x}\cosh5x=\frac{e^{6x}+e^{-4x}}{2}', [('exp(x)*cosh(5*x)', '(exp(6*x)+exp(-4*x))/2')], 'نكتب cosh بالتعريف ونضرب في $e^x$. الأسس تنجمع: $x+5x=6x$ و $x-5x=-4x$.'),
                      ('tex', r'\frac12\int e^{6x}dx=\frac{e^{6x}}{12},\qquad \frac12\int e^{-4x}dx=\frac{e^{-4x}}{-8}',
                       [('integrate(exp(6*x)/2,x)', 'exp(6*x)/12'), ('integrate(exp(-4*x)/2,x)', '-exp(-4*x)/8')], 'نكامل كل حد'),
                      ('line', 'exp(6*x)/12-exp(-4*x)/8', 'نجمع الحدين، وهذا الجواب.')])
    U.drill('3', '1445-S1-SE-Q2.1', 'I', 'أحد الأسين صفر.',
            sol_rows=[('tex', r'e^{-x}\cosh x=e^{-x}\cdot\frac{e^{x}+e^{-x}}{2}=\frac{1+e^{-2x}}{2}', [('exp(-x)*cosh(x)', '(1+exp(-2*x))/2')],
                       'التعريف، و $e^{-x}\\cdot e^{x}=e^0=1$'),
                      ('tex', r'\int\frac12dx=\frac{x}{2},\qquad \int\frac12e^{-2x}dx=-\frac{e^{-2x}}{4}',
                       [('integrate(Rational(1,2),x)', 'x/2'), ('integrate(exp(-2*x)/2,x)', '-exp(-2*x)/4')], 'نكامل كل حد'),
                      ('line', 'x/2-exp(-2*x)/4', 'نجمع الحدين، وهذا الجواب.')])
    return U


# ---------------------------------------------------------------- 21
def u_subparts():
    U = Unit('U-P10', 'تعويض أولًا: جذر داخل الدالة، وقوة × جذر', '5.1', 'ص66، تمارين 15 و17 و18', 4)
    U.add('idea', 'الفكرة', p(rich('بعض الأسئلة تحتاج تعويضًا قبل أي شيء: $e^{\\sqrt x}$ نتخلص من الجذر بـ $t=\\sqrt x$ فيصير تجزئة عادية. '
                                   'و $x^3\\sqrt{x^2+c}$ تنحل بتعويض $w=x^2+c$ فقط.')))
    U.add('sign', 'العلامة', p(rich('$e^{\\sqrt x}$ أو $\\cos\\sqrt x$؛ أو قوة فردية لـ $x$ × جذر فيه $x^2$ (أو $x^4$).')))
    U.prev('آخر نوع في 5.1: قبل التجزئة (أو بدلها) تعويض.')
    U.add('short', '🧭 الطريقة', method([
        '<b>جذر داخل الدالة</b> ($e^{\\sqrt x}$ أو $\\cos\\sqrt x$): $t=\\sqrt x$، فـ $x=t^2$ و $dx=2t\\,dt$. يصير تجزئة (النوع 12).',
        '<b>قوة × جذر</b> ($x^3\\sqrt{x^2+c}$): $w=$ ما تحت الجذر. اكتب الباقي بدلالة $w$، وكامل حدًا حدًا.',
        'في الآخر ارجع لـ $x$.'],
        tricks_=[('<b>$\\sqrt x$ داخل دالة:</b> $t=\\sqrt x$، و $x=t^2$، و $dx=2t\\,dt$. مثال: $\\int e^{\\sqrt x}dx=\\int2t\\,e^{t}dt$، وهذا النوع 12.',
                  [('diff(2*exp(sqrt(x))*(sqrt(x)-1),x)', 'exp(sqrt(x))', 't')])], label='U-P10'))
    it = ITEMS['N51-X15']
    ex = question(it, 'U-P10 example')
    ex += steps(it, [
        ('tex', r't=\sqrt{x},\quad x=t^{2},\quad dx=2t\,dt', [('diff(x**2,x)', '2*x')], 'الجذر داخل الدالة يصعّبها. نسمّي $t=\\sqrt x$، فـ $x=t^2$ و $dx=2t\\,dt$.'),
        ('tex', r'\int e^{\sqrt x}dx=\int2t\,e^{t}\,dt', [('exp(sqrt(x))', '2*sqrt(x)*exp(sqrt(x))*diff(sqrt(x),x)')], 'نعوّض: $e^{\\sqrt x}$ تصير $e^t$، و $dx$ تصير $2t\\,dt$. صار تجزئة عادية.'),
        ('tex', r'u=2t,\quad dv=e^{t}dt,\quad du=2\,dt,\quad v=e^{t}', [('diff(2*x,x)', '2'), ('integrate(exp(x),x)', 'exp(x)')],
         'تجزئة (النوع 12): $u=2t$'),
        ('tex', r'=2t\,e^{t}-\int2e^{t}\,dt=2t\,e^{t}-2e^{t}', [('diff(2*x*exp(x)-2*exp(x),x)', '2*x*exp(x)')], 'نعوّض في القانون $uv-\\int v\\,du$، وتكامل $e^t$ هو $e^t$.'),
        ('line', '2*exp(sqrt(x))*(sqrt(x)-1)', 'نرجع $t=\\sqrt x$، ونطلّع $2e^{\\sqrt x}$ عامل مشترك.')], 'U-P10 ex')
    ex += final(it, 'U-P10 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تنسَ $dx=2t\\,dt$؛ هي اللي تعطي حد $t$ للتجزئة.'),
                                rich('$x^3dx=x^2\\cdot x\\,dx$: نكتب $x^2=w-c$ و $x\\,dx=\\frac{dw}{2}$.')]))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر التعويض ($t$ و $dx$)، ثم التجزئة، ثم الرجوع لـ $x$.')))
    U.gist('$e^{\\sqrt x}$ أو $\\cos\\sqrt x$، أو قوة × جذر فيه $x^2$', '$t=\\sqrt x$، أو $w=$ ما تحت الجذر', 'تجزئة أو تكامل حدًا حدًا، ثم ارجع لـ $x$')
    U.drill('1', 'G-08', 'G', '$u=2t$ و $dv=\\cos t\\,dt$.',
            first=r't=\sqrt{x},\ dx=2t\,dt:\quad\int\cos\sqrt{x}\,dx=\int2t\cos t\,dt',
            claims=[('cos(sqrt(x))', '2*sqrt(x)*cos(sqrt(x))*diff(sqrt(x),x)')],
            sol_rows=[('tex', r'u=2t,\quad dv=\cos t\,dt,\quad du=2\,dt,\quad v=\sin t', [('integrate(cos(x),x)', 'sin(x)')], 'صار تجزئة مثل النوع 12: $u=2t$ و $dv=\\cos t\\,dt$.'),
                      ('tex', r'=2t\sin t-\int2\sin t\,dt=2t\sin t+2\cos t', [('diff(2*x*sin(x)+2*cos(x),x)', '2*x*cos(x)')],
                       '$\\int\\sin t\\,dt=-\\cos t$، وسالب في سالب = موجب'),
                      ('line', '2*sqrt(x)*sin(sqrt(x))+2*cos(sqrt(x))', 'نرجع $t=\\sqrt x$ في كل مكان.')])
    U.drill('2', 'N51-X17', 'P', '$w=x^2-1$، $x^2=w+1$، $x\\,dx=\\frac{dw}{2}$.',
            sol_rows=[('sub', 'x**2-1', '2*x', 'نسمّي اللي تحت الجذر $w=x^2-1$، ومشتقته $2x$.', 'w'),
                      ('tex', r'x^{3}\sqrt{x^{2}-1}\,dx=x^{2}\sqrt{x^{2}-1}\cdot x\,dx=(w+1)\sqrt{w}\,\frac{dw}{2}',
                       [('x**3*sqrt(x**2-1)', '((x**2-1)+1)*sqrt(x**2-1)*diff(x**2-1,x)/2')], 'نفصل $x^3=x^2\\cdot x$. ومن $w=x^2-1$: $x^2=w+1$، و $x\\,dx=\\frac{dw}{2}$.'),
                      ('tex', r'=\frac12\int\left(w^{3/2}+w^{1/2}\right)dw=\frac15w^{5/2}+\frac13w^{3/2}',
                       [('integrate((w**Rational(3,2)+w**Rational(1,2))/2,w)', 'w**Rational(5,2)/5+w**Rational(3,2)/3', 't')], 'نوزّع $\\sqrt w=w^{1/2}$ على القوس، ونكامل كل حد: نزيد الأس 1 ونقسم عليه.'),
                      ('line', '(x**2-1)**Rational(5,2)/5+(x**2-1)**Rational(3,2)/3', 'نرجع $w=x^2-1$.')])
    U.drill('3', 'N51-X18', 'I', '$w=x^4+2$، $x^4=w-2$، $x^3dx=\\frac{dw}{4}$.',
            sol_rows=[('sub', 'x**4+2', '4*x**3', 'نسمّي اللي تحت الجذر $w=x^4+2$، ومشتقته $4x^3$.', 'w'),
                      ('tex', r'x^{7}\sqrt{x^{4}+2}\,dx=x^{4}\sqrt{x^{4}+2}\cdot x^{3}dx=(w-2)\sqrt{w}\,\frac{dw}{4}',
                       [('x**7*sqrt(x**4+2)', '((x**4+2)-2)*sqrt(x**4+2)*diff(x**4+2,x)/4')], 'نفصل $x^7=x^4\\cdot x^3$. ومن $w=x^4+2$: $x^4=w-2$، و $x^3dx=\\frac{dw}{4}$.'),
                      ('tex', r'=\frac14\int\left(w^{3/2}-2w^{1/2}\right)dw=\frac{1}{10}w^{5/2}-\frac13w^{3/2}',
                       [('integrate((w**Rational(3,2)-2*w**Rational(1,2))/4,w)', 'w**Rational(5,2)/10-w**Rational(3,2)/3', 't')],
                       'نوزّع $\\sqrt w=w^{1/2}$ على القوس، ونكامل كل حد: نزيد الأس 1 ونقسم عليه.'),
                      ('line', '(x**4+2)**Rational(5,2)/10-(x**4+2)**Rational(3,2)/3', 'نرجع $w=x^4+2$.')])
    return U


UNITS_51 = [u_parts_linear, u_parts_di, u_qaws, u_ln_alone, u_definite, u_rafeeq, u_xinv, u_dawaran, u_nisfayn, u_subparts]

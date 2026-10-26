"""المذكرة الكاملة — الدرس 5.2: التكاملات المثلثية.

Every case, printed in this order: when (what you see, and what it is not), why it works, the steps (the doctor's
branches, then the fixed script of the method in the same words every time), the examples solved step by step with one
operation per row (🧱), before you hand in, the one-line summary, and the exercises with full solutions. Only the
tan chain keeps a quick way (⚡), written after its examples.
"""
from booklet_engine import ITEMS, arith, same_value
from guide_kit import Unit, contrast, final, method, question, rich, shortcut, steps, tricks
from guide_51 import PREP_SCRIPT, SUB_SCRIPT, script, when
from html_kit import md, mi, p, table, ul

# the reserve step comes first in every 5.2 substitution, then the substitution script word for word
RESERVE = 'احجز وحدة: القطعة اللي تصير 🟢 $du$'
TRIG_SCRIPT = [RESERVE] + SUB_SCRIPT
# the doctor's branches, in his words and order
SC_TREE = (p('<b>🌳 فروع دكتورك:</b>')
           + table([rich('$\\int\\sin^m x\\cos^n x\\,dx$'), 'وش تسوي'],
                   [[rich('$m$ فردي'), rich('$u=\\cos x$ (احجز $\\sin x$)')],
                    [rich('$n$ فردي'), rich('$u=\\sin x$ (احجز $\\cos x$)')],
                    ['الاثنين زوجي', 'نص الزاوية']], 'compact'))
TS_TREE = (p('<b>🌳 فروع دكتورك:</b>')
           + table([rich('$\\int\\tan^m x\\sec^n x\\,dx$'), 'وش تسوي'],
                   [[rich('$m$ فردي'), rich('$u=\\sec x$ (احجز $\\sec x\\tan x$)')],
                    [rich('$n$ زوجي'), rich('$u=\\tan x$ (احجز $\\sec^2x$)')],
                    [rich('$m$ زوجي و $n$ فردي'), 'تجزئة']], 'compact')
           + p(rich('$m$ فردي و $n$ زوجي مع بعض (مثل $\\tan^3x\\sec^2x$)؟ الفرعين صح، والجوابين يختلفون برقم ثابت بس.'), 'small'))


def laws(label, rows):
    """The identities or laws of a type, each one printed and checked."""
    return ''.join(md(arith(latex, claims, '%s law %d' % (label, k))) for k, (latex, claims) in enumerate(rows, 1))


def checked(label, text, claims):
    """A line of text whose math is checked (quick checks and traps)."""
    arith('', claims, label)
    return rich(text)


SIN_COS = [(r'\cos^{2}x=1-\sin^{2}x,\qquad \sin^{2}x=1-\cos^{2}x', [('cos(x)**2', '1-sin(x)**2'), ('sin(x)**2', '1-cos(x)**2')]),
           (r'\frac{d}{dx}\sin x=\cos x,\qquad \frac{d}{dx}\cos x=-\sin x', [('diff(sin(x),x)', 'cos(x)'), ('diff(cos(x),x)', '-sin(x)')])]
ODD_TRICK = [('احجز وحدة من صاحب الأس الفردي، والثانية تبقى زي ما هي: $\\sin^6x\\cos^3x=\\sin^6x\\cos^2x\\cdot\\cos x$.',
              [('sin(x)**6*cos(x)**3', 'sin(x)**6*cos(x)**2*cos(x)')]),
             ('الاثنين فرديين؟ احجز من الأصغر: في $\\sin^3x\\cos^7x$ نحجز $\\sin x$. ومع sin يطلع سالب، لأن $du=-\\sin x\\,dx$.',
              [('sin(x)**3*cos(x)**7', '(1-cos(x)**2)*cos(x)**7*sin(x)'), ('diff(cos(x),x)', '-sin(x)')])]
TAN_SEC_TRICK = [('sec زوجي: احجز $\\sec^2x$، و $u=\\tan x$، لأن $\\frac{d}{dx}\\tan x=\\sec^2x$.', [('diff(tan(x),x)', 'sec(x)**2')]),
                 ('tan فردي: احجز $\\sec x\\tan x$، و $u=\\sec x$، لأن $\\frac{d}{dx}\\sec x=\\sec x\\tan x$.',
                  [('diff(sec(x),x)', 'sec(x)*tan(x)')])]

# the formula sheet: what to keep for du in types 22, 23, 25, 26 and 28, and how the rest is turned
SHEET_ROWS = [('أس cos فردي', r'\cos x\,dx', r'u=\sin x', r'\cos^{2}x=1-\sin^{2}x'),
              ('أس sin فردي', r'\sin x\,dx=-du', r'u=\cos x', r'\sin^{2}x=1-\cos^{2}x'),
              ('أس sec زوجي', r'\sec^{2}x\,dx', r'u=\tan x', r'\sec^{2}x=1+\tan^{2}x'),
              ('أس tan فردي ومعه sec', r'\sec x\tan x\,dx', r'u=\sec x', r'\tan^{2}x=\sec^{2}x-1'),
              ('أس csc زوجي', r'\csc^{2}x\,dx=-du', r'u=\cot x', r'\csc^{2}x=1+\cot^{2}x'),
              ('أس cot فردي ومعه csc', r'\csc x\cot x\,dx=-du', r'u=\csc x', r'\cot^{2}x=\csc^{2}x-1')]
SHEET_STEPS = ['نحجز القطعة اللي تصير $du$ (العمود الثاني).',
               'نحوّل الباقي بالمتطابقة (العمود الأخير).',
               'نعوّض $u$ و $du$. وإذا $du$ فيها سالب، يطلع سالب قدّام التكامل.',
               'نفك القوس ونوزّع، ثم نكامل كل حد ونرجع لـ $x$.']


def sc_method():
    """For the formula sheet: the steps in words and the table of what to keep, every identity and derivative checked."""
    arith('', [('cos(x)**2', '1-sin(x)**2'), ('sin(x)**2', '1-cos(x)**2'), ('sec(x)**2', '1+tan(x)**2'),
               ('tan(x)**2', 'sec(x)**2-1'), ('csc(x)**2', '1+cot(x)**2'), ('cot(x)**2', 'csc(x)**2-1'),
               ('diff(sin(x),x)', 'cos(x)'), ('diff(cos(x),x)', '-sin(x)'), ('diff(tan(x),x)', 'sec(x)**2'),
               ('diff(sec(x),x)', 'sec(x)*tan(x)'), ('diff(cot(x),x)', '-csc(x)**2'), ('diff(csc(x),x)', '-csc(x)*cot(x)')], 'method sheet')
    rows = [[see, mi(keep), mi(u), mi(rest)] for see, keep, u, rest in SHEET_ROWS]
    return (method(SHEET_STEPS) + table(['إذا شفت', 'احجز (تصير du)', 'نسمّي', 'والباقي يتحوّل بـ'], rows, 'formula'), '')


# ---------------------------------------------------------------- 22
def u_odd_alone():
    U = Unit('U-T1', 'قوة فردية لـ sin أو cos وحدها', '5.2', 'ص67–68، مثال 1', 5)
    U.add('idea', 'الفكرة', p(rich(
        'مشتقة $\\sin x$ هي $\\cos x$. فإذا حجزنا $\\cos x$ وحدة صارت 🟢 $du$، '
        'والباقي أسه زوجي نحوّله كله لـ 🔵 $\\sin x$ بـ $\\cos^2x=1-\\sin^2x$.')))
    U.add('sign', 'العلامة', when(
        'sin أو cos لحالها بأس فردي: $\\int\\cos^3x\\,dx$ أو $\\int\\sin^5x\\,dx$.',
        'الأس زوجي، مثل $\\int\\cos^2x\\,dx$: ما فيه شي تحجزه، فهذا تجهيز (نص الزاوية).',
        [(r'\int\cos^{3}x\,dx', 'تعويض: احجز $\\cos x$، و $u=\\sin x$', 'الأس فردي'),
         (r'\int\cos^{2}x\,dx', 'تجهيز: نص الزاوية', 'الأس زوجي، ما فيه شي نحجزه')]))
    U.add('short', '🧭 الطريقة', SC_TREE + method(script(TRIG_SCRIPT, [
        'من صاحب الأس الفردي: $\\cos^3x=\\cos^2x\\cdot\\cos x$',
        'الدالة الثانية: حجزت $\\cos x$؟ $u=\\sin x$. حجزت $\\sin x$؟ $u=\\cos x$. والباقي حوّله لـ $u$ بالمتطابقة',
        '$u=\\sin x$ يعطي $du=\\cos x\\,dx$، و $u=\\cos x$ يعطي $du=-\\sin x\\,dx$',
        'القطعة المحجوزة ÷ $du$: مع $\\cos x$ الرقم 1، ومع $\\sin x$ الرقم $-1$، يعني 🔴 سالب قدّام التكامل',
        'فك القوس، وكامل كل حد: زد الأس 1 واقسم عليه',
        None])) + laws('U-T1', SIN_COS)
        + tricks([('احجز وحدة من صاحب الأس الفردي: $\\cos^7x=\\cos^6x\\cdot\\cos x$.', [('cos(x)**7', 'cos(x)**6*cos(x)')]),
                  ('ومع sin يطلع سالب: $u=\\cos x$ يعني $du=-\\sin x\\,dx$، فـ $\\sin x\\,dx=-du$.', [('diff(cos(x),x)', '-sin(x)')])], 'U-T1'))
    it = ITEMS['N52-E1-1']
    ex = question(it, 'U-T1 example')
    ex += steps(it, [
        ('tex', r'\cos^{3}x=\cos^{2}x\cdot\cD{\cos x}', [('cos(x)**3', 'cos(x)**2*cos(x)')],
         'أس cos فردي. نحجز $\\cos x$ وحدة عشان تصير 🟢 $du$ لما $u=\\sin x$.'),
        ('tex', r'\cos^{2}x=1-\cU{\sin^{2}x}', [('cos(x)**2', '1-sin(x)**2')],
         'الباقي $\\cos^2x$ نحوّله لـ sin، عشان كل شي يصير بدلالة 🔵 $\\sin x$.'),
        ('tex', r'\cos^{3}x=(1-\cU{\sin^{2}x})\,\cD{\cos x}', [('cos(x)**3', '(1-sin(x)**2)*cos(x)')], 'نحط المتطابقة مكان $\\cos^2x$.'),
        ('sub', 'sin(x)', 'cos(x)', 'نسمّي $u=\\sin x$. مشتقته $\\cos x$، وهي القطعة اللي حجزناها.'),
        ('tex', r'\int\cos^{3}x\,dx=\int(1-\cU{u^{2}})\,\cD{du}', [('cos(x)**3', '(1-sin(x)**2)*diff(sin(x),x)')],
         'نعوّض: 🔵 $\\sin x$ تصير $u$، و 🟢 $\\cos x\\,dx$ تصير $du$.'),
        ('tex', r'=u-\frac{u^{3}}{3}', [('integrate(1-u**2,u)', 'u-u**3/3')], 'نكامل كل حد: نزيد الأس 1 ونقسم عليه.'),
        ('line', 'sin(x)-sin(x)**3/3', 'نرجع $u=\\sin x$.')], 'U-T1 ex')
    ex += final(it, 'U-T1 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('ok', '✔ تأكد', p(checked('U-T1 ok', 'أعلى أس في جوابك لازم يساوي أس السؤال: هنا $\\sin^3x$، وأس السؤال 3 ✓. ومع sin يكون أول حد في الجواب سالب.',
                                    [('diff(sin(x)-sin(x)**3/3,x)', 'cos(x)**3')])))
    U.add('trap', '⚠️ الفخ', ul([rich('مع sin: $du=-\\sin x\\,dx$، فيطلع سالب قدّام التكامل كله. لا تنساه.'),
                                rich('القطعة اللي حجزتها هي $du$. لا تحوّلها بالمتطابقة.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\cos^{3}x=(1-\sin^{2}x)\cos x,\qquad \cU{u=\sin x},\quad \cD{du=\cos x\,dx}',
                   [('cos(x)**3', '(1-sin(x)**2)*cos(x)'), ('diff(sin(x),x)', 'cos(x)')], 'U-T1 paper'))
          + md(arith(r'\int(1-u^{2})\,du=\sin x-\frac{\sin^{3}x}{3}+C', [('diff(sin(x)-sin(x)**3/3,x)', 'cos(x)**3')], 'U-T1 paper 2')))
    U.gist('قوة فردية لـ sin أو cos وحدها', 'احجز وحدة: $\\cos x$ أو $\\sin x$', 'حوّل الباقي بالمتطابقة، و $u$ = الدالة الثانية')
    U.drill('1', 'G-09', 'G', 'احجز $\\sin x$، و $\\sin x\\,dx=-du$.',
            first=r'\sin^{3}x=(1-\cos^{2}x)\sin x,\quad u=\cos x,\ du=\cR{-}\sin x\,dx',
            claims=[('sin(x)**3', '(1-cos(x)**2)*sin(x)'), ('diff(cos(x),x)', '-sin(x)')],
            sol_rows=[('tex', r'\int\sin^{3}x\,dx=\cR{-}\int(1-u^{2})\,du', [('sin(x)**3', '-(1-cos(x)**2)*diff(cos(x),x)')],
                       'نعوّض: $\\cos x$ تصير $u$، و $\\sin x\\,dx=-du$. فيطلع سالب قدّام التكامل.'),
                      ('tex', r'=-\left(u-\frac{u^{3}}{3}\right)', [('-integrate(1-u**2,u)', '-(u-u**3/3)')], 'نكامل كل حد داخل القوس.'),
                      ('tex', r'=-u+\frac{u^{3}}{3}', [('-(u-u**3/3)', '-u+u**3/3')], 'نوزّع السالب: يقلب إشارة كل حد.'),
                      ('line', '-cos(x)+cos(x)**3/3', 'نرجع $u=\\cos x$.')])
    U.drill('2', 'N52-E1-2', 'P', 'احجز $\\sin x$، والباقي $\\sin^4x=(1-\\cos^2x)^2$.',
            sol_rows=[('tex', r'\sin^{5}x=\sin^{4}x\cdot\sin x', [('sin(x)**5', 'sin(x)**4*sin(x)')],
                       'أس sin فردي. نحجز $\\sin x$ وحدة عشان تصير $du$ مع $u=\\cos x$.'),
                      ('tex', r'\sin^{4}x=\left(\sin^{2}x\right)^{2}=(1-\cos^{2}x)^{2}', [('sin(x)**4', '(1-cos(x)**2)**2')],
                       'الباقي أسه 4، يعني مربع $\\sin^2x$. نحوّل $\\sin^2x=1-\\cos^2x$.'),
                      ('sub', 'cos(x)', '-sin(x)', 'نسمّي $u=\\cos x$. مشتقته $-\\sin x$، فـ $\\sin x\\,dx=-du$.'),
                      ('tex', r'\int\sin^{5}x\,dx=-\int(1-u^{2})^{2}\,du', [('sin(x)**5', '-(1-cos(x)**2)**2*diff(cos(x),x)')],
                       'نعوّض، والسالب يطلع قدّام التكامل.'),
                      ('tex', r'(1-u^{2})^{2}=1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')],
                       'نفك القوس: الأول تربيع، ناقص ضعف الضرب، زائد الثاني تربيع.'),
                      ('tex', r'-\int\left(1-2u^{2}+u^{4}\right)du=-\left(u-\frac{2u^{3}}{3}+\frac{u^{5}}{5}\right)',
                       [('-integrate(1-2*u**2+u**4,u)', '-(u-2*u**3/3+u**5/5)')], 'نكامل كل حد: نزيد الأس 1 ونقسم عليه.'),
                      ('tex', r'=-u+\frac{2u^{3}}{3}-\frac{u^{5}}{5}', [('-(u-2*u**3/3+u**5/5)', '-u+2*u**3/3-u**5/5')],
                       'نوزّع السالب: يقلب إشارة كل حد.'),
                      ('line', '-cos(x)+2*cos(x)**3/3-cos(x)**5/5', 'نرجع $u=\\cos x$.')])
    U.drill('3', 'G-10', 'I', 'احجز $\\cos x$، و $u=\\sin x$ بدون سالب.',
            sol_rows=[('tex', r'\cos^{5}x=\cos^{4}x\cdot\cos x', [('cos(x)**5', 'cos(x)**4*cos(x)')],
                       'أس cos فردي. نحجز $\\cos x$ وحدة عشان تصير $du$.'),
                      ('tex', r'\cos^{4}x=\left(\cos^{2}x\right)^{2}=(1-\sin^{2}x)^{2}', [('cos(x)**4', '(1-sin(x)**2)**2')],
                       'الباقي مربع $\\cos^2x$. نحوّل $\\cos^2x=1-\\sin^2x$.'),
                      ('sub', 'sin(x)', 'cos(x)', 'نسمّي $u=\\sin x$، و $du=\\cos x\\,dx$. هنا ما فيه سالب.'),
                      ('tex', r'\int\cos^{5}x\,dx=\int(1-u^{2})^{2}\,du', [('cos(x)**5', '(1-sin(x)**2)**2*diff(sin(x),x)')],
                       'نعوّض: كل شي صار بدلالة $u$.'),
                      ('tex', r'(1-u^{2})^{2}=1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')], 'نفك القوس.'),
                      ('tex', r'\int\left(1-2u^{2}+u^{4}\right)du=u-\frac{2u^{3}}{3}+\frac{u^{5}}{5}',
                       [('integrate(1-2*u**2+u**4,u)', 'u-2*u**3/3+u**5/5')], 'نكامل كل حد.'),
                      ('line', 'sin(x)-2*sin(x)**3/3+sin(x)**5/5', 'نرجع $u=\\sin x$.')])
    return U


# ---------------------------------------------------------------- 23
def u_sc_odd():
    U = Unit('U-T2', 'sin و cos معًا وأحدهما فردي', '5.2', 'ص68–69، مثال 2', 5)
    U.add('idea', 'الفكرة', p(rich(
        'نحجز وحدة من صاحب الأس الفردي تصير 🟢 $du$، ونحوّل باقيه بالمتطابقة. '
        'والدالة الثانية ما نلمسها، لأنها هي 🔵 $u$ نفسه بقوته.')))
    U.add('sign', 'العلامة', when(
        'sin و cos مضروبتين بنفس الزاوية، وواحد من الأسين على الأقل فردي: $\\int\\sin^4x\\cos^5x\\,dx$.',
        'الأسين زوجيين ($\\sin^2x\\cos^4x$): تجهيز، نص الزاوية. والزاويتين مختلفتين ($\\sin7x\\cos5x$): تجهيز، الضرب إلى جمع.',
        [(r'\int\sin^{4}x\cos^{5}x\,dx', 'تعويض: احجز $\\cos x$، و $u=\\sin x$', '$n=5$ فردي'),
         (r'\int\sin^{3}x\cos^{8}x\,dx', 'تعويض: احجز $\\sin x$، و $u=\\cos x$', '$m=3$ فردي'),
         (r'\int\sin^{2}x\cos^{4}x\,dx', 'تجهيز: نص الزاوية', 'الأسين زوجيين')]))
    U.add('short', '🧭 الطريقة', SC_TREE + method(script(TRIG_SCRIPT, [
        'من صاحب الأس الفردي: $\\sin^4x\\cos^5x=\\sin^4x\\cos^4x\\cdot\\cos x$. والاثنين فرديين؟ احجز من الأصغر',
        'الدالة الثانية ($\\sin x$ هنا). باقي الدالة المحجوزة حوّله بالمتطابقة، والدالة الثانية تبقى مثل ما هي',
        '$u=\\sin x$ يعطي $du=\\cos x\\,dx$',
        'مع $\\cos x$ محجوزة الرقم 1. ومع $\\sin x$ محجوزة يطلع 🔴 $-1$ قدّام التكامل',
        'فك القوس، ووزّع قوة $u$ على كل حد (الأسس تنجمع)، ثم كامل',
        None])) + laws('U-T2', SIN_COS) + tricks(ODD_TRICK, 'U-T2'))
    it = ITEMS['1446-S1-SE-Q2.6']
    ex = question(it, 'U-T2 example')
    ex += steps(it, [
        ('tex', r'\sin^{4}x\cos^{5}x=\sin^{4}x\cos^{4}x\cdot\cD{\cos x}', [('sin(x)**4*cos(x)**5', 'sin(x)**4*cos(x)**4*cos(x)')],
         'أس cos فردي (5)، وأس sin زوجي (4). نحجز $\\cos x$ وحدة عشان تصير 🟢 $du$.'),
        ('tex', r'\cos^{4}x=\left(\cos^{2}x\right)^{2}=(1-\cU{\sin^{2}x})^{2}', [('cos(x)**4', '(1-sin(x)**2)**2')],
         'الباقي $\\cos^4x$ مربع $\\cos^2x$. نحوّل $\\cos^2x=1-\\sin^2x$ عشان يصير كله 🔵 sin.'),
        ('sub', 'sin(x)', 'cos(x)', 'نسمّي $u=\\sin x$، لأن مشتقته $\\cos x$ هي القطعة المحجوزة.'),
        ('tex', r'\int\sin^{4}x\cos^{5}x\,dx=\int \cU{u^{4}}(1-\cU{u^{2}})^{2}\,\cD{du}',
         [('sin(x)**4*cos(x)**5', 'sin(x)**4*(1-sin(x)**2)**2*diff(sin(x),x)')],
         'نعوّض: $\\sin^4x$ تصير 🔵 $u^4$، والقوس بدلالة $u$، و 🟢 $\\cos x\\,dx=du$.'),
        ('tex', r'(1-u^{2})^{2}=1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')],
         'نفك القوس: الأول تربيع، ناقص ضعف الضرب، زائد الثاني تربيع.'),
        ('tex', r'u^{4}(1-2u^{2}+u^{4})=u^{4}-2u^{6}+u^{8}', [('u**4*(1-2*u**2+u**4)', 'u**4-2*u**6+u**8')],
         'نوزّع $u^4$ على كل حد. لما نضرب قوى $u$ الأسس تنجمع.'),
        ('tex', r'\int\left(u^{4}-2u^{6}+u^{8}\right)du=\frac{u^{5}}{5}-\frac{2u^{7}}{7}+\frac{u^{9}}{9}',
         [('integrate(u**4-2*u**6+u**8,u)', 'u**5/5-2*u**7/7+u**9/9')], 'نكامل كل حد: نزيد الأس 1 ونقسم عليه.'),
        ('line', 'sin(x)**5/5-2*sin(x)**7/7+sin(x)**9/9', 'نرجع $u=\\sin x$.')], 'U-T2 ex')
    ex += final(it, 'U-T2 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('ok', '✔ تأكد', p(checked('U-T2 ok', 'أعلى أس في جوابك = مجموع أسين السؤال: $4+5=9$ ✓. '
                                    'وأقل أس = أس الدالة اللي صارت $u$ زائد 1: $4+1=5$ ✓.', [('4+5', '9'), ('4+1', '5')])))
    U.add('trap', '⚠️ الفخ', ul(['الأسين زوجيين؟ ما فيه شي نحجزه، فهذا تجهيز: نص الزاوية.',
                                'الاثنين فرديين؟ احجز من الأصغر، عشان القوس اللي تفكه يصير أصغر.']))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\sin^{4}x\cos^{5}x=\sin^{4}x\,(1-\sin^{2}x)^{2}\cos x,\qquad \cU{u=\sin x},\quad \cD{du=\cos x\,dx}',
                   [('sin(x)**4*cos(x)**5', 'sin(x)**4*(1-sin(x)**2)**2*cos(x)'), ('diff(sin(x),x)', 'cos(x)')], 'U-T2 paper'))
          + p('ثم سطر فك القوس، وسطر التوزيع، وسطر الجواب.'))
    U.gist('sin و cos مضروبتين، وأحد الأسين فردي', 'احجز وحدة من صاحب الأس الفردي', 'حوّل باقيه، ووزّع قوة $u$، وكامل')
    U.drill('1', '1447-S1-SE-Q2.3', 'G', 'احجز $\\cos x$، والباقي $\\cos^4x=(1-\\sin^2x)^2$.',
            first=r'\sin^{2}x\cos^{5}x=\sin^{2}x\,(1-\sin^{2}x)^{2}\cos x,\quad u=\sin x,\ du=\cos x\,dx',
            claims=[('sin(x)**2*cos(x)**5', 'sin(x)**2*(1-sin(x)**2)**2*cos(x)')],
            sol_rows=[('tex', r'\int\sin^{2}x\cos^{5}x\,dx=\int u^{2}(1-u^{2})^{2}\,du',
                       [('sin(x)**2*cos(x)**5', 'sin(x)**2*(1-sin(x)**2)**2*diff(sin(x),x)')],
                       'نعوّض: $\\sin^2x$ تصير $u^2$، و $\\cos x\\,dx=du$.'),
                      ('tex', r'(1-u^{2})^{2}=1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')], 'نفك القوس.'),
                      ('tex', r'u^{2}(1-2u^{2}+u^{4})=u^{2}-2u^{4}+u^{6}', [('u**2*(1-2*u**2+u**4)', 'u**2-2*u**4+u**6')],
                       'نوزّع $u^2$ على كل حد: الأسس تنجمع.'),
                      ('tex', r'\int\left(u^{2}-2u^{4}+u^{6}\right)du=\frac{u^{3}}{3}-\frac{2u^{5}}{5}+\frac{u^{7}}{7}',
                       [('integrate(u**2-2*u**4+u**6,u)', 'u**3/3-2*u**5/5+u**7/7')], 'نكامل كل حد.'),
                      ('line', 'sin(x)**3/3-2*sin(x)**5/5+sin(x)**7/7', 'نرجع $u=\\sin x$.')])
    U.drill('2', 'N52-X01', 'P', 'أس sin فردي، فـ $u=\\cos x$ وسالب قدّام التكامل.',
            sol_rows=[('tex', r'\sin^{3}x\cos^{4}x=\sin^{2}x\cos^{4}x\cdot\sin x', [('sin(x)**3*cos(x)**4', 'sin(x)**2*cos(x)**4*sin(x)')],
                       'أس sin فردي (3). نحجز $\\sin x$ وحدة.'),
                      ('tex', r'=(1-\cos^{2}x)\cos^{4}x\cdot\sin x', [('sin(x)**3*cos(x)**4', '(1-cos(x)**2)*cos(x)**4*sin(x)')],
                       'نحوّل الباقي $\\sin^2x=1-\\cos^2x$، عشان كل شي يصير cos.'),
                      ('sub', 'cos(x)', '-sin(x)', 'نسمّي $u=\\cos x$، فـ $\\sin x\\,dx=-du$.'),
                      ('tex', r'\int\sin^{3}x\cos^{4}x\,dx=-\int(1-u^{2})\,u^{4}\,du',
                       [('sin(x)**3*cos(x)**4', '-(1-cos(x)**2)*cos(x)**4*diff(cos(x),x)')], 'نعوّض، والسالب يطلع قدّام التكامل.'),
                      ('tex', r'(1-u^{2})\,u^{4}=u^{4}-u^{6}', [('(1-u**2)*u**4', 'u**4-u**6')], 'نوزّع $u^4$ على القوس.'),
                      ('tex', r'-\int\left(u^{4}-u^{6}\right)du=-\left(\frac{u^{5}}{5}-\frac{u^{7}}{7}\right)',
                       [('-integrate(u**4-u**6,u)', '-(u**5/5-u**7/7)')], 'نكامل كل حد.'),
                      ('tex', r'=-\frac{u^{5}}{5}+\frac{u^{7}}{7}', [('-(u**5/5-u**7/7)', '-u**5/5+u**7/7')], 'نوزّع السالب على القوس.'),
                      ('line', '-cos(x)**5/5+cos(x)**7/7', 'نرجع $u=\\cos x$.')])
    U.drill('3', 'N52-E2-2', 'I', 'احجز $\\cos x$، و $\\sqrt{\\sin x}=u^{1/2}$.',
            sol_rows=[('tex', r'\sqrt{\sin x}\,\cos^{3}x=\sqrt{\sin x}\,\cos^{2}x\cdot\cos x',
                       [('sqrt(sin(x))*cos(x)**3', 'sqrt(sin(x))*cos(x)**2*cos(x)')], 'أس cos فردي (3). نحجز $\\cos x$ وحدة.'),
                      ('tex', r'=\sqrt{\sin x}\,(1-\sin^{2}x)\cos x', [('sqrt(sin(x))*cos(x)**3', 'sqrt(sin(x))*(1-sin(x)**2)*cos(x)')],
                       'نحوّل الباقي $\\cos^2x=1-\\sin^2x$.'),
                      ('sub', 'sin(x)', 'cos(x)', 'نسمّي $u=\\sin x$، و $du=\\cos x\\,dx$.'),
                      ('tex', r'\int\sqrt{\sin x}\,\cos^{3}x\,dx=\int u^{1/2}(1-u^{2})\,du',
                       [('sqrt(sin(x))*cos(x)**3', 'sqrt(sin(x))*(1-sin(x)**2)*diff(sin(x),x)')], 'نعوّض. والجذر يصير أس: $\\sqrt u=u^{1/2}$.'),
                      ('tex', r'u^{1/2}(1-u^{2})=u^{1/2}-u^{5/2}', [('u**Rational(1,2)*(1-u**2)', 'u**Rational(1,2)-u**Rational(5,2)')],
                       'نوزّع $u^{1/2}$: الأسس تنجمع، و $\\frac12+2=\\frac52$.'),
                      ('tex', r'\int\left(u^{1/2}-u^{5/2}\right)du=\frac23u^{3/2}-\frac27u^{7/2}',
                       [('integrate(u**Rational(1,2)-u**Rational(5,2),u)', '2*u**Rational(3,2)/3-2*u**Rational(7,2)/7')],
                       'نزيد الأس 1 ونقسم عليه. والقسمة على $\\frac32$ يعني ضرب في $\\frac23$.'),
                      ('line', '2*sin(x)**Rational(3,2)/3-2*sin(x)**Rational(7,2)/7', 'نرجع $u=\\sin x$.')])
    return U


# ---------------------------------------------------------------- 24
def u_even():
    U = Unit('U-T3', 'أسس زوجية: نص الزاوية', '5.2', 'ص67–70، أمثلة 1(3) و2(4)', 5)
    U.add('idea', 'الفكرة', p(rich(
        'لما كل الأسس زوجية ما فيه شي نحجزه: لو حجزنا $\\cos x$ يبقى أس فردي ما يتحوّل. '
        'فننزّل الأس بنص الزاوية: $\\cos^2x=\\frac{1+\\cos2x}{2}$، فالأس 2 يصير 1، و $\\cos2x$ تكامله سطر.')))
    U.add('sign', 'العلامة', when(
        'sin أو cos (أو الاثنين بنفس الزاوية) وكل الأسس زوجية: $\\int\\sin^2x\\,dx$ أو $\\int\\cos^4x\\,dx$ أو $\\int\\sin^2x\\cos^4x\\,dx$.',
        'فيه أس فردي ($\\cos^3x$ أو $\\sin^2x\\cos^5x$): هذا تعويض، احجز من صاحب الأس الفردي.',
        [(r'\int\cos^{2}x\,dx', 'تجهيز: نص الزاوية، $\\cos^2x=\\frac{1+\\cos2x}{2}$', 'الأس زوجي'),
         (r'\int\cos^{3}x\,dx', 'تعويض: احجز $\\cos x$، و $u=\\sin x$', 'الأس فردي')]))
    U.add('short', '🧭 الطريقة', SC_TREE + method(script(PREP_SCRIPT, [
        'كل أسس sin و cos زوجية (عند دكتورك: الاثنين زوجي ← نص الزاوية)',
        'كل $\\sin^2$ أو $\\cos^2$ بنص الزاوية. والأس 4 اكتبه مربع ($\\cos^4x=(\\cos^2x)^2$)، وفك القوس، وكرّر نص الزاوية. '
        'و sin و cos مضروبتين؟ $\\sin x\\cos x=\\frac{\\sin2x}{2}$',
        checked('U-T3 check', 'عوّض $x=0$: $\\cos^20=1$، و $\\frac{1+\\cos0}{2}=1$ ✓', [('cos(0)**2', '1'), ('(1+cos(0))/2', '1')]),
        'صار رقم و $\\cos2x$: كل حد من الجدول. الرقم يصير مضروب في $x$، و 🟠 $\\int\\cos2x\\,dx=\\frac{\\sin2x}{2}$: اقسم على رقم $x$']))
        + laws('U-T3', [(r'\sin^{2}x=\frac{1-\cos2x}{2},\qquad \cos^{2}x=\frac{1+\cos2x}{2}',
                         [('sin(x)**2', '(1-cos(2*x))/2'), ('cos(x)**2', '(1+cos(2*x))/2')]),
                        (r'\sin x\cos x=\frac{\sin2x}{2}', [('sin(x)*cos(x)', 'sin(2*x)/2')])])
        + tricks([('سين وسالب: $\\sin^2$ معها ناقص، و $\\cos^2$ معها زائد. والزاوية تتضاعف: $\\sin^23x=\\frac{1-\\cos6x}{2}$.',
                   [('sin(3*x)**2', '(1-cos(6*x))/2')])], 'U-T3'))
    it = ITEMS['N52-X13']
    ex = question(it, 'U-T3 example 1')
    ex += steps(it, [
        ('tex', r'\sin^{2}x=\frac{1\cR{-}\cos2x}{2}', [('sin(x)**2', '(1-cos(2*x))/2')],
         'الأس زوجي، فما فيه شي نحجزه. ننزّل الأس بنص الزاوية، و sin معها 🔴 ناقص.'),
        ('tex', r'=\frac12-\frac{\cos2x}{2}', [('(1-cos(2*x))/2', 'Rational(1,2)-cos(2*x)/2')], 'نفصل الكسر حدين عشان نكامل كل واحد لحاله.'),
        ('tex', r'\int\frac12\,dx=\frac{x}{2},\qquad \int\frac{\cos2x}{2}\,dx=\frac{\sin2x}{2\cdot\cA{2}}=\frac{\sin2x}{4}',
         [('integrate(Rational(1,2),x)', 'x/2'), ('integrate(cos(2*x)/2,x)', 'sin(2*x)/4'), ('sin(2*x)/(2*2)', 'sin(2*x)/4')],
         'نكامل كل حد. تكامل $\\cos2x$ هو $\\frac{\\sin2x}{2}$، لأننا 🟠 نقسم على 2 رقم $x$.'),
        ('line', 'x/2-sin(2*x)/4', 'نجمع الحدين، والسالب يبقى قدّام الثاني.')], 'U-T3 ex1')
    ex += final(it, 'U-T3 example 1')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (تمرين من مذكرة د. طارق)', ex)
    it = ITEMS['N52-E1-3']
    ex = question(it, 'U-T3 example 2')
    ex += steps(it, [
        ('tex', r'\cos^{4}2x=\left(\cos^{2}2x\right)^{2}', [('cos(2*x)**4', '(cos(2*x)**2)**2')],
         'الأس 4 زوجي. نكتبه مربع $\\cos^22x$ عشان نستعمل نص الزاوية.'),
        ('tex', r'\cos^{2}2x=\frac{1+\cos4x}{2}', [('cos(2*x)**2', '(1+cos(4*x))/2')],
         'نص الزاوية: cos معها زائد، والزاوية تتضاعف من $2x$ لـ $4x$.'),
        ('tex', r'\cos^{4}2x=\left(\frac{1+\cos4x}{2}\right)^{2}=\frac{1+2\cos4x+\cos^{2}4x}{4}',
         [('cos(2*x)**4', '(1+2*cos(4*x)+cos(4*x)**2)/4')], 'نربّع: نفك القوس اللي في البسط، والمقام $2^2=4$.'),
        ('tex', r'\cos^{2}4x=\frac{1+\cos8x}{2}', [('cos(4*x)**2', '(1+cos(8*x))/2')],
         'بقي $\\cos^24x$ وأسه 2. نستعمل نص الزاوية مرة ثانية.'),
        ('tex', r'\cos^{4}2x=\frac14+\frac{\cos4x}{2}+\frac18+\frac{\cos8x}{8}',
         [('cos(2*x)**4', 'Rational(1,4)+cos(4*x)/2+Rational(1,8)+cos(8*x)/8')],
         'نعوّض، ونوزّع $\\frac14$ على كل حد: $\\frac14\\cdot\\frac12=\\frac18$.'),
        ('tex', r'=\frac38+\frac{\cos4x}{2}+\frac{\cos8x}{8}', [('Rational(1,4)+Rational(1,8)', 'Rational(3,8)')],
         'نجمع الرقمين: $\\frac14+\\frac18=\\frac38$.'),
        ('line', '3*x/8+sin(4*x)/8+sin(8*x)/64',
         'نكامل كل حد ونقسم على رقم $x$: $\\frac12\\cdot\\frac14=\\frac18$، و $\\frac18\\cdot\\frac18=\\frac{1}{64}$.')], 'U-T3 ex2')
    ex += final(it, 'U-T3 example 2')
    U.add('ex', '🧱 مثال 2 محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('ok', '✔ تأكد', p(checked('U-T3 ok', 'في المثال 2، عوّض $x=0$ في السطر اللي قبل التكامل: $\\frac38+\\frac12+\\frac18=1$، '
                                    'و $\\cos^4(0)=1$ ✓. يعني فك المربع صح.',
                                    [('Rational(3,8)+Rational(1,2)+Rational(1,8)', '1'), ('cos(0)**4', '1')])))
    U.add('trap', '⚠️ الفخ', ul([rich('$\\int\\sin^2x\\,dx\\ne\\frac{\\sin^3x}{3}$، لأن مشتقة $\\sin x$ مو موجودة جنبه.'),
                                checked('U-T3 trap', 'لما تكامل $\\cos4x$ اقسم على 4: $\\int\\cos4x\\,dx=\\frac{\\sin4x}{4}$.',
                                        [('diff(sin(4*x)/4,x)', 'cos(4*x)')])]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\cos^{4}2x=\left(\frac{1+\cos4x}{2}\right)^{2}=\frac{1+2\cos4x+\cos^{2}4x}{4}',
                   [('cos(2*x)**4', '(1+2*cos(4*x)+cos(4*x)**2)/4')], 'U-T3 paper'))
          + p(rich('ثم نص الزاوية مرة ثانية لـ $\\cos^24x$، ثم كامل كل حد.')))
    U.gist('كل الأسس زوجية: $\\sin^2$ أو $\\cos^2$ أو $\\cos^4$', 'نص الزاوية: $\\sin^2$ ناقص، و $\\cos^2$ زائد',
           'الأس 4 مربع: فك القوس، وكرّر نص الزاوية، ثم كامل')
    U.drill('1', 'N52-X14', 'G', 'cos معها زائد.', first=r'\cos^{2}x=\frac{1+\cos2x}{2}', claims=[('cos(x)**2', '(1+cos(2*x))/2')],
            sol_rows=[('tex', r'=\frac12+\frac{\cos2x}{2}', [('(1+cos(2*x))/2', 'Rational(1,2)+cos(2*x)/2')], 'نفصل الكسر حدين.'),
                      ('tex', r'\int\frac12\,dx=\frac{x}{2},\qquad \int\frac{\cos2x}{2}\,dx=\frac{\sin2x}{4}',
                       [('integrate(Rational(1,2),x)', 'x/2'), ('integrate(cos(2*x)/2,x)', 'sin(2*x)/4')],
                       'نكامل كل حد، ونقسم على 2 رقم $x$.'),
                      ('line', 'x/2+sin(2*x)/4', 'نجمع الحدين. مع cos الإشارة زائد.')])
    U.drill('2', 'M-19', 'P', 'اجمعهم في مربع: $(\\sin x\\cos x)^2$.',
            sol_rows=[('tex', r'\sin^{2}x\cos^{2}x=\left(\sin x\cos x\right)^{2}', [('sin(x)**2*cos(x)**2', '(sin(x)*cos(x))**2')],
                       'الأسين زوجيين ومتساويين. نجمعهم في مربع واحد عشان نستعمل $\\sin x\\cos x=\\frac{\\sin2x}{2}$.'),
                      ('tex', r'=\left(\frac{\sin2x}{2}\right)^{2}=\frac{\sin^{2}2x}{4}', [('(sin(x)*cos(x))**2', 'sin(2*x)**2/4')],
                       'نعوّض المتطابقة، ونربّع: المقام $2^2=4$.'),
                      ('tex', r'\sin^{2}2x=\frac{1-\cos4x}{2}', [('sin(2*x)**2', '(1-cos(4*x))/2')],
                       'نص الزاوية: sin معها ناقص، والزاوية تتضاعف لـ $4x$.'),
                      ('tex', r'\sin^{2}x\cos^{2}x=\frac18-\frac{\cos4x}{8}', [('sin(x)**2*cos(x)**2', 'Rational(1,8)-cos(4*x)/8')],
                       'نضرب في $\\frac14$: $\\frac14\\cdot\\frac12=\\frac18$.'),
                      ('line', 'x/8-sin(4*x)/32', 'نكامل كل حد. تكامل $\\cos4x$ هو $\\frac{\\sin4x}{4}$، و $\\frac18\\cdot\\frac14=\\frac{1}{32}$.')])
    U.drill('3', 'M-20', 'I', 'اكتبها مربع $\\sin^2x$، ونص الزاوية مرتين.',
            sol_rows=[('tex', r'\sin^{4}x=\left(\sin^{2}x\right)^{2}', [('sin(x)**4', '(sin(x)**2)**2')],
                       'الأس 4 زوجي. نكتبه مربع $\\sin^2x$.'),
                      ('tex', r'\sin^{2}x=\frac{1-\cos2x}{2}', [('sin(x)**2', '(1-cos(2*x))/2')], 'نص الزاوية: sin معها ناقص.'),
                      ('tex', r'\sin^{4}x=\frac{1-2\cos2x+\cos^{2}2x}{4}', [('sin(x)**4', '(1-2*cos(2*x)+cos(2*x)**2)/4')],
                       'نربّع: نفك القوس اللي في البسط، والمقام 4.'),
                      ('tex', r'\cos^{2}2x=\frac{1+\cos4x}{2}', [('cos(2*x)**2', '(1+cos(4*x))/2')],
                       'بقي $\\cos^22x$ وأسه 2. نص الزاوية مرة ثانية.'),
                      ('tex', r'\sin^{4}x=\frac14-\frac{\cos2x}{2}+\frac18+\frac{\cos4x}{8}',
                       [('sin(x)**4', 'Rational(1,4)-cos(2*x)/2+Rational(1,8)+cos(4*x)/8')], 'نعوّض، ونوزّع $\\frac14$ على كل حد.'),
                      ('tex', r'=\frac38-\frac{\cos2x}{2}+\frac{\cos4x}{8}', [('Rational(1,4)+Rational(1,8)', 'Rational(3,8)')],
                       'نجمع الرقمين: $\\frac14+\\frac18=\\frac38$.'),
                      ('line', '3*x/8-sin(2*x)/4+sin(4*x)/32',
                       'نكامل كل حد ونقسم على رقم $x$: $\\frac12\\cdot\\frac12=\\frac14$، و $\\frac18\\cdot\\frac14=\\frac{1}{32}$.')])
    U.drill('4', 'N52-E2-4', 'I', 'طلّع $(\\sin x\\cos x)^2$، ويبقى $\\cos^2x$.',
            sol_rows=[('tex', r'\sin^{2}x\cos^{4}x=\left(\sin x\cos x\right)^{2}\cos^{2}x',
                       [('sin(x)**2*cos(x)**4', '(sin(x)*cos(x))**2*cos(x)**2')],
                       'كل الأسس زوجية. نطلّع مربع $\\sin x\\cos x$، ويبقى $\\cos^2x$.'),
                      ('tex', r'\left(\sin x\cos x\right)^{2}=\frac{\sin^{2}2x}{4}', [('(sin(x)*cos(x))**2', 'sin(2*x)**2/4')],
                       'المتطابقة $\\sin x\\cos x=\\frac{\\sin2x}{2}$، ثم نربّع.'),
                      ('tex', r'\cos^{2}x=\frac{1+\cos2x}{2}', [('cos(x)**2', '(1+cos(2*x))/2')], 'نص الزاوية للباقي $\\cos^2x$.'),
                      ('tex', r'\sin^{2}x\cos^{4}x=\frac{\sin^{2}2x}{8}+\frac{\sin^{2}2x\cos2x}{8}',
                       [('sin(x)**2*cos(x)**4', 'sin(2*x)**2/8+sin(2*x)**2*cos(2*x)/8')],
                       'نضرب: $\\frac14\\cdot\\frac12=\\frac18$، ونوزّع على القوس.'),
                      ('tex', r'\frac{\sin^{2}2x}{8}=\frac{1}{16}-\frac{\cos4x}{16}', [('sin(2*x)**2/8', 'Rational(1,16)-cos(4*x)/16')],
                       'الحد الأول: نص الزاوية $\\sin^22x=\\frac{1-\\cos4x}{2}$، ونضرب في $\\frac18$.'),
                      ('tex', r'\int\left(\frac{1}{16}-\frac{\cos4x}{16}\right)dx=\frac{x}{16}-\frac{\sin4x}{64}',
                       [('integrate(Rational(1,16)-cos(4*x)/16,x)', 'x/16-sin(4*x)/64')], 'نكامل. تكامل $\\cos4x$ هو $\\frac{\\sin4x}{4}$.'),
                      ('sub', 'sin(2*x)', '2*cos(2*x)', 'الحد الثاني فيه $\\cos2x$، وهي مشتقة $\\sin2x$ (تقريبًا). نسمّي $w=\\sin2x$.', 'w'),
                      ('tex', r'\int\frac{\sin^{2}2x\cos2x}{8}\,dx=\frac{1}{16}\int w^{2}\,dw=\frac{\sin^{3}2x}{48}',
                       [('diff(sin(2*x)**3/48,x)', 'sin(2*x)**2*cos(2*x)/8')],
                       '$\\cos2x\\,dx=\\frac{dw}{2}$، فـ $\\frac18\\cdot\\frac12=\\frac1{16}$. و $\\int w^2dw=\\frac{w^3}{3}$.'),
                      ('line', 'x/16-sin(4*x)/64+sin(2*x)**3/48', 'نجمع ناتج الحدين، ونرجع $w=\\sin2x$.')], extra_lines=2)
    return U


# ---------------------------------------------------------------- 25
def u_sec_even():
    U = Unit('U-T4', 'tan و sec: الـ sec زوجي', '5.2', 'ص70–71، الحالة 1', 5)
    U.add('idea', 'الفكرة', p(rich(
        'مشتقة $\\tan x$ هي $\\sec^2x$. فإذا أس sec زوجي نحجز $\\sec^2x$ تصير 🟢 $du$، '
        'والباقي نحوّله لـ 🔵 tan بـ $\\sec^2x=1+\\tan^2x$.')))
    U.add('sign', 'العلامة', when(
        'tan و sec مضروبتين وأس sec زوجي: $\\int\\tan^3x\\sec^2x\\,dx$. أو sec بأس زوجي لحاله: $\\int\\sec^4x\\,dx$.',
        'أس tan فردي وأس sec فردي ($\\tan^3x\\sec x$): تعويض بس احجز $\\sec x\\tan x$ و $u=\\sec x$. '
        'وأس tan زوجي وأس sec فردي (مثل $\\sec^3x$ لحاله): تجزئة.',
        [(r'\int\tan^{3}x\sec^{2}x\,dx', 'تعويض: احجز $\\sec^2x$، و $u=\\tan x$', '$n=2$ زوجي'),
         (r'\int\tan^{3}x\sec x\,dx', 'تعويض: احجز $\\sec x\\tan x$، و $u=\\sec x$', '$m=3$ فردي، و $n=1$ فردي'),
         (r'\int\sec^{3}x\,dx', 'تجزئة: $u=\\sec x$، و $dv=\\sec^2x\\,dx$', '$m=0$ زوجي، و $n=3$ فردي')]))
    U.add('short', '🧭 الطريقة', TS_TREE + method(script(TRIG_SCRIPT, [
        'أس sec زوجي: احجز $\\sec^2x$ ($\\sec^4x=\\sec^2x\\cdot\\sec^2x$)',
        '$u=\\tan x$. وباقي sec حوّله بـ $\\sec^2x=1+\\tan^2x$',
        '$du=\\sec^2x\\,dx$',
        'القطعة المحجوزة هي $du$ بالضبط، فالرقم 1',
        'فك القوس ووزّع، ثم كامل كل حد',
        None]))
        + laws('U-T4', [(r'\sec^{2}x=1+\tan^{2}x,\qquad \frac{d}{dx}\tan x=\sec^{2}x',
                         [('sec(x)**2', '1+tan(x)**2'), ('diff(tan(x),x)', 'sec(x)**2')])])
        + tricks(TAN_SEC_TRICK, 'U-T4'))
    it = ITEMS['1447-S1-FE-Q2.6']
    ex = question(it, 'U-T4 example')
    ex += steps(it, [
        ('sub', 'tan(x)', 'sec(x)**2', 'أس sec زوجي (2). نحجز $\\sec^2x$ لأنها مشتقة $\\tan x$، فنسمّي $u=\\tan x$.'),
        ('tex', r'\int\cU{\tan^{3}x}\,\cD{\sec^{2}x\,dx}=\int\cU{u^{3}}\,\cD{du}', [('tan(x)**3*sec(x)**2', 'tan(x)**3*diff(tan(x),x)')],
         'ما بقي شي من sec نحوّله. 🔵 $\\tan^3x$ تصير $u^3$، و 🟢 $\\sec^2x\\,dx=du$.'),
        ('tex', r'=\frac{u^{4}}{4}', [('integrate(u**3,u)', 'u**4/4')], 'نكامل: نزيد الأس 1 ونقسم عليه.'),
        ('line', 'tan(x)**4/4', 'نرجع $u=\\tan x$.')], 'U-T4 ex')
    ex += final(it, 'U-T4 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('ok', '✔ تأكد', p(checked('U-T4 ok', 'اشتق جوابك: $\\left(\\frac{\\tan^4x}{4}\\right)\'=\\tan^3x\\cdot\\sec^2x$ ✓. رجع السؤال.',
                                    [('diff(tan(x)**4/4,x)', 'tan(x)**3*sec(x)**2')])))
    same_value('sec(x)**4/4-sec(x)**2/2', 'tan(x)**4/4-Rational(1,4)', 'U-T4 two answers')
    U.add('trap', '⚠️ الفخ', ul([rich('حليته بـ $u=\\sec x$ لأن tan فردي؟ يطلع $\\frac{\\sec^4x}{4}-\\frac{\\sec^2x}{2}$. '
                                     'هذا صح بعد، ويختلف عن $\\frac{\\tan^4x}{4}$ برقم ثابت بس.'),
                                checked('U-T4 trap', 'بعد ما تحجز $\\sec^2x$، انقص 2 من أس sec: $\\sec^8x=\\sec^6x\\cdot\\sec^2x$.',
                                        [('sec(x)**8', 'sec(x)**6*sec(x)**2')])]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\cU{u=\tan x},\quad \cD{du=\sec^{2}x\,dx},\qquad \int\tan^{3}x\sec^{2}x\,dx=\int u^{3}\,du=\frac{\tan^{4}x}{4}+C',
                   [('diff(tan(x),x)', 'sec(x)**2'), ('diff(tan(x)**4/4,x)', 'tan(x)**3*sec(x)**2')], 'U-T4 paper')))
    U.gist('tan و sec مضروبتين، وأس sec زوجي', 'احجز $\\sec^2x$، و $u=\\tan x$', 'حوّل باقي sec بـ $1+\\tan^2x$، ثم وزّع وكامل')
    U.drill('1', 'G-91', 'G', '$\\sec^2x$ موجودة، فـ $u=\\tan x$.',
            first=r'u=\tan x,\quad du=\sec^{2}x\,dx', claims=[('diff(tan(x),x)', 'sec(x)**2')],
            sol_rows=[('tex', r'\int\tan^{6}x\sec^{2}x\,dx=\int u^{6}\,du', [('tan(x)**6*sec(x)**2', 'tan(x)**6*diff(tan(x),x)')],
                       'نعوّض: $\\tan^6x$ تصير $u^6$، و $\\sec^2x\\,dx=du$.'),
                      ('tex', r'=\frac{u^{7}}{7}', [('integrate(u**6,u)', 'u**7/7')], 'نكامل: نزيد الأس 1 ونقسم عليه.'),
                      ('line', 'tan(x)**7/7', 'نرجع $u=\\tan x$.')])
    U.drill('2', 'M-21', 'G', 'احجز $\\sec^2x$، والباقي $\\sec^2x=1+\\tan^2x$.',
            first=r'\sec^{4}x=\sec^{2}x\cdot\sec^{2}x=(1+\tan^{2}x)\sec^{2}x', claims=[('sec(x)**4', '(1+tan(x)**2)*sec(x)**2')],
            sol_rows=[('sub', 'tan(x)', 'sec(x)**2', 'نسمّي $u=\\tan x$، لأن مشتقته $\\sec^2x$ هي القطعة المحجوزة.'),
                      ('tex', r'\int\sec^{4}x\,dx=\int(1+u^{2})\,du', [('sec(x)**4', '(1+tan(x)**2)*diff(tan(x),x)')],
                       'نعوّض: القوس بدلالة $u$، و $\\sec^2x\\,dx=du$.'),
                      ('tex', r'=u+\frac{u^{3}}{3}', [('integrate(1+u**2,u)', 'u+u**3/3')], 'نكامل كل حد.'),
                      ('line', 'tan(x)+tan(x)**3/3', 'نرجع $u=\\tan x$.')])
    U.drill('3', 'G-92', 'P', 'احجز $\\sec^2x$، والباقي $\\sec^4x=(1+\\tan^2x)^2$.',
            sol_rows=[('tex', r'\sec^{6}x=\sec^{4}x\cdot\sec^{2}x', [('sec(x)**6', 'sec(x)**4*sec(x)**2')],
                       'أس sec زوجي. نحجز $\\sec^2x$، ويبقى $\\sec^4x$.'),
                      ('tex', r'\sec^{4}x=\left(\sec^{2}x\right)^{2}=(1+\tan^{2}x)^{2}', [('sec(x)**4', '(1+tan(x)**2)**2')],
                       'الباقي مربع $\\sec^2x$. نحوّل $\\sec^2x=1+\\tan^2x$.'),
                      ('sub', 'tan(x)', 'sec(x)**2', 'نسمّي $u=\\tan x$، و $du=\\sec^2x\\,dx$.'),
                      ('tex', r'\int\sec^{6}x\,dx=\int(1+u^{2})^{2}\,du', [('sec(x)**6', '(1+tan(x)**2)**2*diff(tan(x),x)')],
                       'نعوّض: كل شي صار بدلالة $u$.'),
                      ('tex', r'(1+u^{2})^{2}=1+2u^{2}+u^{4}', [('(1+u**2)**2', '1+2*u**2+u**4')],
                       'نفك القوس: الأول تربيع، زائد ضعف الضرب، زائد الثاني تربيع.'),
                      ('tex', r'\int\left(1+2u^{2}+u^{4}\right)du=u+\frac{2u^{3}}{3}+\frac{u^{5}}{5}',
                       [('integrate(1+2*u**2+u**4,u)', 'u+2*u**3/3+u**5/5')], 'نكامل كل حد.'),
                      ('line', 'tan(x)+2*tan(x)**3/3+tan(x)**5/5', 'نرجع $u=\\tan x$.')])
    U.drill('4', 'G-12', 'I', 'احجز $\\sec^2x$، والباقي $\\sec^4x=(1+u^2)^2$.',
            sol_rows=[('tex', r'\sec^{6}x=\sec^{4}x\cdot\sec^{2}x', [('sec(x)**6', 'sec(x)**4*sec(x)**2')],
                       'أس sec زوجي (6). نحجز $\\sec^2x$ من $\\sec^6x$، ويبقى $\\sec^4x$. و $\\tan^3x$ يبقى مثل ما هو.'),
                      ('tex', r'\sec^{4}x=(1+\tan^{2}x)^{2}', [('sec(x)**4', '(1+tan(x)**2)**2')], 'نحوّل الباقي لـ tan.'),
                      ('sub', 'tan(x)', 'sec(x)**2', 'نسمّي $u=\\tan x$، و $du=\\sec^2x\\,dx$.'),
                      ('tex', r'\int\tan^{3}x\sec^{6}x\,dx=\int u^{3}(1+u^{2})^{2}\,du',
                       [('tan(x)**3*sec(x)**6', 'tan(x)**3*(1+tan(x)**2)**2*diff(tan(x),x)')], 'نعوّض.'),
                      ('tex', r'(1+u^{2})^{2}=1+2u^{2}+u^{4}', [('(1+u**2)**2', '1+2*u**2+u**4')], 'نفك القوس.'),
                      ('tex', r'u^{3}(1+2u^{2}+u^{4})=u^{3}+2u^{5}+u^{7}', [('u**3*(1+2*u**2+u**4)', 'u**3+2*u**5+u**7')],
                       'نوزّع $u^3$: الأسس تنجمع.'),
                      ('tex', r'\int\left(u^{3}+2u^{5}+u^{7}\right)du=\frac{u^{4}}{4}+\frac{u^{6}}{3}+\frac{u^{8}}{8}',
                       [('integrate(u**3+2*u**5+u**7,u)', 'u**4/4+u**6/3+u**8/8')], 'نكامل كل حد. و $\\frac{2u^6}{6}=\\frac{u^6}{3}$.'),
                      ('line', 'tan(x)**4/4+tan(x)**6/3+tan(x)**8/8', 'نرجع $u=\\tan x$.')])
    return U


# ---------------------------------------------------------------- 26
def u_tan_odd():
    U = Unit('U-T5', 'tan و sec: الـ tan فردي', '5.2', 'ص71–72، الحالة 2', 6)
    U.add('idea', 'الفكرة', p(rich(
        'مشتقة $\\sec x$ هي $\\sec x\\tan x$. فإذا أس tan فردي ومعه sec، نحجز $\\sec x\\tan x$ تصير 🟢 $du$، '
        'وباقي tan أسه زوجي نحوّله لـ 🔵 sec بـ $\\tan^2x=\\sec^2x-1$.')))
    U.add('sign', 'العلامة', when(
        'tan و sec مضروبتين، وأس tan فردي، ومعه sec واحد على الأقل: $\\int\\sec^3x\\tan^3x\\,dx$.',
        'أس tan زوجي وأس sec فردي ($\\tan^4x\\sec^3x$): تجزئة (حوّل كل tan لـ sec، ثم سلسلة sec). '
        'وأس sec زوجي: تعويض بس احجز $\\sec^2x$ و $u=\\tan x$.',
        [(r'\int\tan^{3}x\sec^{3}x\,dx', 'تعويض: احجز $\\sec x\\tan x$، و $u=\\sec x$', '$m=3$ فردي'),
         (r'\int\tan^{4}x\sec^{3}x\,dx', 'تجزئة: حوّل كل tan لـ sec، ثم سلسلة sec', '$m$ زوجي و $n$ فردي')]))
    U.add('short', '🧭 الطريقة', TS_TREE + method(script(TRIG_SCRIPT, [
        'أس tan فردي: احجز $\\sec x\\tan x$',
        '$u=\\sec x$. وباقي tan حوّله بـ $\\tan^2x=\\sec^2x-1$',
        '$du=\\sec x\\tan x\\,dx$',
        'القطعة المحجوزة هي $du$ بالضبط، فالرقم 1',
        'فك القوس ووزّع، ثم كامل كل حد',
        None]))
        + laws('U-T5', [(r'\tan^{2}x=\sec^{2}x-1,\qquad \frac{d}{dx}\sec x=\sec x\tan x',
                         [('tan(x)**2', 'sec(x)**2-1'), ('diff(sec(x),x)', 'sec(x)*tan(x)')])])
        + tricks(TAN_SEC_TRICK, 'U-T5'))
    it = ITEMS['1447-S2-SE-Q3.3']
    ex = question(it, 'U-T5 example')
    ex += steps(it, [
        ('tex', r'\sec^{3}x\tan^{3}x=\sec^{2}x\tan^{2}x\cdot\cD{\sec x\tan x}', [('sec(x)**3*tan(x)**3', 'sec(x)**2*tan(x)**2*sec(x)*tan(x)')],
         'أس tan فردي (3) ومعه sec. نحجز $\\sec x\\tan x$ لأنها مشتقة $\\sec x$، فتصير 🟢 $du$.'),
        ('tex', r'\tan^{2}x=\cU{\sec^{2}x}-1', [('tan(x)**2', 'sec(x)**2-1')],
         'الباقي $\\tan^2x$ نحوّله لـ sec، عشان كل شي يصير بدلالة 🔵 $\\sec x$.'),
        ('sub', 'sec(x)', 'sec(x)*tan(x)', 'نسمّي $u=\\sec x$. مشتقته هي القطعة اللي حجزناها.'),
        ('tex', r'\int\sec^{3}x\tan^{3}x\,dx=\int\cU{u^{2}}(\cU{u^{2}}-1)\,\cD{du}',
         [('sec(x)**3*tan(x)**3', 'sec(x)**2*(sec(x)**2-1)*diff(sec(x),x)')],
         'نعوّض: $\\sec^2x$ تصير 🔵 $u^2$، و $\\tan^2x$ تصير $u^2-1$، و 🟢 $\\sec x\\tan x\\,dx=du$.'),
        ('tex', r'u^{2}(u^{2}-1)=u^{4}-u^{2}', [('u**2*(u**2-1)', 'u**4-u**2')], 'نوزّع $u^2$ على القوس: الأسس تنجمع.'),
        ('tex', r'\int\left(u^{4}-u^{2}\right)du=\frac{u^{5}}{5}-\frac{u^{3}}{3}', [('integrate(u**4-u**2,u)', 'u**5/5-u**3/3')],
         'نكامل كل حد.'),
        ('line', 'sec(x)**5/5-sec(x)**3/3', 'نرجع $u=\\sec x$.')], 'U-T5 ex')
    ex += final(it, 'U-T5 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('ok', '✔ تأكد', p(checked('U-T5 ok', 'الجواب كله بدلالة $\\sec x$. وأعلى أس = أس tan + أس sec − 1: $3+3-1=5$ ✓.', [('3+3-1', '5')])))
    U.add('trap', '⚠️ الفخ', ul([rich('أس tan زوجي وأس sec فردي؟ ما ينفع الحجز. حوّل كل $\\tan^2x$ لـ $\\sec^2x-1$، ثم سلسلة sec (النوع 27).'),
                                rich('إذا بقي $\\tan x$ في التكامل بعد ما كتبت $u=\\sec x$، فالتحويل ما خلص.')]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\sec^{3}x\tan^{3}x=\sec^{2}x\,(\sec^{2}x-1)\sec x\tan x,\qquad \cU{u=\sec x},\quad \cD{du=\sec x\tan x\,dx}',
                   [('sec(x)**3*tan(x)**3', 'sec(x)**2*(sec(x)**2-1)*sec(x)*tan(x)'), ('diff(sec(x),x)', 'sec(x)*tan(x)')], 'U-T5 paper'))
          + p('ثم سطر التوزيع، وسطر الجواب.'))
    U.gist('tan و sec مضروبتين، وأس tan فردي', 'احجز $\\sec x\\tan x$، و $u=\\sec x$', 'حوّل باقي tan بـ $\\sec^2x-1$، ثم وزّع وكامل')
    U.drill('1', 'G-13', 'G', 'الباقي $\\tan^2x=\\sec^2x-1$.',
            first=r'\tan^{3}x\sec x=\tan^{2}x\cdot\sec x\tan x=(\sec^{2}x-1)\sec x\tan x',
            claims=[('tan(x)**3*sec(x)', '(sec(x)**2-1)*sec(x)*tan(x)')],
            sol_rows=[('sub', 'sec(x)', 'sec(x)*tan(x)', 'نسمّي $u=\\sec x$، و $du=\\sec x\\tan x\\,dx$.'),
                      ('tex', r'\int\tan^{3}x\sec x\,dx=\int(u^{2}-1)\,du', [('tan(x)**3*sec(x)', '(sec(x)**2-1)*diff(sec(x),x)')],
                       'نعوّض: القوس بدلالة $u$، والقطعة المحجوزة $du$.'),
                      ('tex', r'=\frac{u^{3}}{3}-u', [('integrate(u**2-1,u)', 'u**3/3-u')], 'نكامل كل حد.'),
                      ('line', 'sec(x)**3/3-sec(x)', 'نرجع $u=\\sec x$.')])
    U.drill('2', 'N52-E3-4', 'P', 'احجز $\\sec x\\tan x$، والباقي $\\tan^4x=(\\sec^2x-1)^2$.',
            sol_rows=[('tex', r'\tan^{5}x\sec^{3}x=\tan^{4}x\sec^{2}x\cdot\sec x\tan x',
                       [('tan(x)**5*sec(x)**3', 'tan(x)**4*sec(x)**2*sec(x)*tan(x)')], 'أس tan فردي (5). نحجز $\\sec x\\tan x$.'),
                      ('tex', r'\tan^{4}x=\left(\tan^{2}x\right)^{2}=(\sec^{2}x-1)^{2}', [('tan(x)**4', '(sec(x)**2-1)**2')],
                       'الباقي مربع $\\tan^2x$. نحوّل $\\tan^2x=\\sec^2x-1$.'),
                      ('sub', 'sec(x)', 'sec(x)*tan(x)', 'نسمّي $u=\\sec x$.'),
                      ('tex', r'\int\tan^{5}x\sec^{3}x\,dx=\int(u^{2}-1)^{2}u^{2}\,du',
                       [('tan(x)**5*sec(x)**3', '(sec(x)**2-1)**2*sec(x)**2*diff(sec(x),x)')], 'نعوّض.'),
                      ('tex', r'(u^{2}-1)^{2}=u^{4}-2u^{2}+1', [('(u**2-1)**2', 'u**4-2*u**2+1')], 'نفك القوس.'),
                      ('tex', r'(u^{4}-2u^{2}+1)\,u^{2}=u^{6}-2u^{4}+u^{2}', [('(u**4-2*u**2+1)*u**2', 'u**6-2*u**4+u**2')],
                       'نوزّع $u^2$: الأسس تنجمع.'),
                      ('tex', r'\int\left(u^{6}-2u^{4}+u^{2}\right)du=\frac{u^{7}}{7}-\frac{2u^{5}}{5}+\frac{u^{3}}{3}',
                       [('integrate(u**6-2*u**4+u**2,u)', 'u**7/7-2*u**5/5+u**3/3')], 'نكامل كل حد.'),
                      ('line', 'sec(x)**7/7-2*sec(x)**5/5+sec(x)**3/3', 'نرجع $u=\\sec x$.')])
    U.drill('3', 'N52-X06', 'I', 'احجز $\\sec x\\tan x$، والباقي $(u^2-1)^2u^4$.',
            sol_rows=[('tex', r'\tan^{5}x\sec^{5}x=\tan^{4}x\sec^{4}x\cdot\sec x\tan x',
                       [('tan(x)**5*sec(x)**5', 'tan(x)**4*sec(x)**4*sec(x)*tan(x)')], 'أس tan فردي (5). نحجز $\\sec x\\tan x$.'),
                      ('tex', r'\tan^{4}x=(\sec^{2}x-1)^{2}', [('tan(x)**4', '(sec(x)**2-1)**2')], 'نحوّل الباقي من tan لـ sec.'),
                      ('sub', 'sec(x)', 'sec(x)*tan(x)', 'نسمّي $u=\\sec x$.'),
                      ('tex', r'\int\tan^{5}x\sec^{5}x\,dx=\int(u^{2}-1)^{2}u^{4}\,du',
                       [('tan(x)**5*sec(x)**5', '(sec(x)**2-1)**2*sec(x)**4*diff(sec(x),x)')], 'نعوّض.'),
                      ('tex', r'(u^{2}-1)^{2}=u^{4}-2u^{2}+1', [('(u**2-1)**2', 'u**4-2*u**2+1')], 'نفك القوس.'),
                      ('tex', r'(u^{4}-2u^{2}+1)\,u^{4}=u^{8}-2u^{6}+u^{4}', [('(u**4-2*u**2+1)*u**4', 'u**8-2*u**6+u**4')],
                       'نوزّع $u^4$: الأسس تنجمع.'),
                      ('tex', r'\int\left(u^{8}-2u^{6}+u^{4}\right)du=\frac{u^{9}}{9}-\frac{2u^{7}}{7}+\frac{u^{5}}{5}',
                       [('integrate(u**8-2*u**6+u**4,u)', 'u**9/9-2*u**7/7+u**5/5')], 'نكامل كل حد.'),
                      ('line', 'sec(x)**9/9-2*sec(x)**7/7+sec(x)**5/5', 'نرجع $u=\\sec x$.')])
    return U


# ---------------------------------------------------------------- 27
def u_reduce():
    U = Unit('U-T6', 'tan وحدها و sec فردي وحده (سلسلة التخفيض)', '5.2', 'ص70–73، الحالتان 3 و4', 6)
    U.add('idea', 'الفكرة', p(rich(
        'ما فيه دالة ثانية نحجز منها، فنكسر $\\tan^2x=\\sec^2x-1$: يطلع حد فيه 🟢 $\\sec^2x$ (تعويض) وحد tan بأس أقل باثنين. '
        'و sec الفردي لحاله تجزئة، يرجع فيها التكامل نفسه فنحله كمعادلة.')))
    U.add('sign', 'العلامة', when(
        'tan لحالها بأي أس: $\\int\\tan^4x\\,dx$. أو sec لحالها بأس فردي: $\\int\\sec^3x\\,dx$.',
        'sec لحالها بأس زوجي ($\\sec^4x$): تعويض، احجز $\\sec^2x$. و tan ومعها sec ($\\tan^3x\\sec^2x$): تعويض، احجز.',
        [(r'\int\tan^{4}x\,dx', 'تجهيز: اكسر $\\tan^2x=\\sec^2x-1$', 'tan لحالها'),
         (r'\int\sec^{3}x\,dx', 'تجزئة: $u=\\sec x$، و $dv=\\sec^2x\\,dx$', '$m=0$ زوجي، و $n=3$ فردي'),
         (r'\int\sec^{4}x\,dx', 'تعويض: احجز $\\sec^2x$، و $u=\\tan x$', '$n=4$ زوجي')]))
    U.add('short', '🧭 الطريقة', TS_TREE + method(script(PREP_SCRIPT, [
        'tan لحالها: $n=0$ زوجي، بس ما فيه $\\sec^2x$ تحجزه',
        'اكسر مربع واحد: $\\tan^4x=\\tan^2x\\,(\\sec^2x-1)$، ووزّع',
        checked('U-T6 check', 'عوّض $x=\\frac\\pi4$: $\\tan^4\\frac\\pi4=1$، و $1\\cdot(2-1)=1$ ✓',
                [('tan(pi/4)**4', '1'), ('tan(pi/4)**2*(sec(pi/4)**2-1)', '1')]),
        'الحد اللي فيه $\\sec^2x$ تعويض $u=\\tan x$. والحد الثاني tan بأس أقل باثنين: اكسره مرة ثانية لين يصير الأس 1 أو يختفي'],
        ['<b>و sec فردي لحاله</b> (عند دكتورك: $m$ زوجي و $n$ فردي ← تجزئة): $u=\\sec x$، و $dv=\\sec^2x\\,dx$. '
         'يرجع التكامل نفسه، فاجمعه في طرف واحد واقسم.']))
        + laws('U-T6', [(r'\tan^{2}x=\sec^{2}x-1', [('tan(x)**2', 'sec(x)**2-1')]),
                        (r'\int\tan x\,dx=\ln|\sec x|,\qquad \int\sec x\,dx=\ln|\sec x+\tan x|',
                         [('diff(log(sec(x)),x)', 'tan(x)'), ('diff(log(sec(x)+tan(x)),x)', 'sec(x)')])]))
    it = ITEMS['N52-E3-2']
    ex = question(it, 'U-T6 example 1')
    ex += steps(it, [
        ('tex', r'\tan^{4}x=\tan^{2}x\,(\sec^{2}x-1)', [('tan(x)**4', 'tan(x)**2*(sec(x)**2-1)')],
         'tan وحدها، فما فيه شي نحجزه. نكسر مربع واحد من tan بـ $\\tan^2x=\\sec^2x-1$.'),
        ('tex', r'=\cU{\tan^{2}x}\,\cD{\sec^{2}x}\cR{-}\tan^{2}x', [('tan(x)**2*(sec(x)**2-1)', 'tan(x)**2*sec(x)**2-tan(x)**2')],
         'نوزّع $\\tan^2x$ على القوس. الحد الأول فيه 🔵 tan ومشتقته 🟢 $\\sec^2x$. وانتبه للحد الثاني: قدّامه 🔴 سالب.'),
        ('sub', 'tan(x)', 'sec(x)**2', 'الحد الأول فيه $\\sec^2x$، يعني تعويض: نسمّي $u=\\tan x$، و $du=\\sec^2x\\,dx$. فيصير $\\int u^2\\,du$.'),
        ('tex', r'\int u^{2}\,du=\frac{u^{3}}{3}=\frac{\tan^{3}x}{3}', [('integrate(u**2,u)', 'u**3/3')],
         'نكامل: نزيد الأس 1 ونقسم عليه، ثم نرجع $u=\\tan x$.'),
        ('line', 'tan(x)**3/3-Integral(tan(x)**2,x)', 'هذا الحد الأول. والتكامل الثاني فيه $\\tan^2x$، فنكسره مرة ثانية.'),
        ('tex', r'\int\tan^{2}x\,dx=\int\left(\sec^{2}x-1\right)dx=\tan x-x',
         [('tan(x)**2', 'sec(x)**2-1'), ('diff(tan(x)-x,x)', 'sec(x)**2-1')],
         'نفس المتطابقة. تكامل $\\sec^2x$ هو $\\tan x$، وتكامل 1 هو $x$.'),
        ('line', 'tan(x)**3/3-(tan(x)-x)', 'نحط الناتج بين قوسين، لأن قدّامه 🔴 سالب.'),
        ('line', 'tan(x)**3/3-tan(x)+x', 'نوزّع السالب: يقلب إشارة الحدين.')], 'U-T6 ex1')
    ex += final(it, 'U-T6 example 1')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    it = ITEMS['N52-E3-1']
    A = '(sec(x)*tan(x)/2+log(Abs(sec(x)+tan(x)))/2)'
    ex = question(it, 'U-T6 example 2')
    ex += steps(it, [
        ('parts', 'sec(x)', 'sec(x)**2', 'sec(x)*tan(x)', 'tan(x)',
         'sec فردي وحده، فما ينفع الحجز. نستعمل التجزئة: $u=\\sec x$، و $dv=\\sec^2x\\,dx$ لأن تكامله $\\tan x$.'),
        ('line', 'sec(x)*tan(x)-Integral(sec(x)*tan(x)**2,x)', 'نعوّض في القانون $uv-\\int v\\,du$. و $v\\,du=\\tan x\\cdot\\sec x\\tan x$.'),
        ('tex', r'\sec x\tan^{2}x=\sec x\,(\sec^{2}x-1)', [('sec(x)*tan(x)**2', 'sec(x)*(sec(x)**2-1)')],
         'نحوّل $\\tan^2x=\\sec^2x-1$ عشان يصير كله sec.'),
        ('tex', r'=\sec^{3}x-\sec x', [('sec(x)*(sec(x)**2-1)', 'sec(x)**3-sec(x)')], 'نوزّع $\\sec x$ على القوس.'),
        ('line', 'sec(x)*tan(x)-Integral(sec(x)**3,x)+Integral(sec(x),x)',
         'نفصل التكامل ونوزّع السالب. رجع $\\int\\sec^3x\\,dx$ نفسه!'),
        ('tex', r'I=\sec x\tan x-I+\ln|\sec x+\tan x|', [('sec(x)*tan(x)-%s+log(Abs(sec(x)+tan(x)))' % A, A)],
         'نسمّي $I=\\int\\sec^3x\\,dx$. و $\\int\\sec x\\,dx=\\ln|\\sec x+\\tan x|$ من القانون فوق.'),
        ('tex', r'2I=\sec x\tan x+\ln|\sec x+\tan x|', [('2*%s' % A, 'sec(x)*tan(x)+log(Abs(sec(x)+tan(x)))')],
         'ننقل $I$ للطرف الأول: $I+I=2I$.'),
        ('tex', r'I=\frac{\sec x\tan x}{2}+\frac12\ln|\sec x+\tan x|', [('diff(sec(x)*tan(x)/2+log(sec(x)+tan(x))/2,x)', 'sec(x)**3')],
         'نقسم الطرفين على 2 عشان يبقى $I$ لحاله.')], 'U-T6 ex2')
    ex += final(it, 'U-T6 example 2')
    U.add('ex', '🧱 مثال 2 محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('short', '⚡ الطريقة السريعة: سلسلة tan، و sec³ «نص ونص»', shortcut(
        ITEMS['N52-E3-2'], 'U-T6 ex1',
        saves='بدل ما تكسر القوة كل مرة وتوزّع السالب (9 أسطر في مثال 1)، تكتب الجواب حد حد. وكل ما كبر الأس، وفّرت أكثر.',
        origin='في مثال 1 كل كسرة $\\tan^2x=\\sec^2x-1$ عطتنا حد ($\\frac{\\tan^3x}{3}$) وسالب تكامل بأس أقل باثنين ($-\\int\\tan^2x$). '
               'والكسرة الثانية عطت $\\tan x$ وسالب $\\int1$. فالحدود تمشي بنمط ثابت.',
        steps_=['نكتب الأسس: تبدأ من (الأس ناقص 1) وتنزل 2، 2، لين قبل الصفر.',
                'كل حد = tan بهذا الأس ÷ نفس الأس.',
                'الإشارات تتبادل: $+$ ثم $-$ ثم $+$.',
                'آخر حد بالإشارة اللي عليها الدور: $x$ إذا أس السؤال زوجي، و $\\ln|\\sec x|$ إذا فردي.'],
        on='على مثال 1 في 🧱:',
        rows=[('الأسس تبدأ من $4-1=3$ وتنزل 2، فتصير 3 ثم 1.', r'3,\ 1', [('4-1', '3'), ('3-2', '1')]),
              ('كل حد tan بالأس ÷ الأس، والإشارات $+$ ثم $-$.', r'\frac{\tan^{3}x}{3}-\frac{\tan^{1}x}{1}', [('tan(x)**3/3-tan(x)**1/1', 'tan(x)**3/3-tan(x)')]),
              ('الأس 4 زوجي، فآخر حد $x$، والدور على $+$. نفس جواب 🧱 ✓', r'\frac{\tan^{3}x}{3}-\tan x+x+C', [('=ANS', 'tan(x)**3/3-tan(x)+x')])],
        after_rows=p(rich('<b>و sec الفردي:</b> $\\int\\sec^3x\\,dx$ جوابه جاهز «نص ونص»: $\\frac12\\sec x\\tan x+\\frac12\\ln|\\sec x+\\tan x|$، نفس مثال 2 ✓. '
                          'ومع $\\sec^5$ ننزل مرة وحدة: $\\int\\sec^5x\\,dx=\\frac14\\sec^3x\\tan x+\\frac34\\int\\sec^3x\\,dx$، ثم «نص ونص».'
                          + arith('', [('diff(sec(x)*tan(x)/2+log(sec(x)+tan(x))/2,x)', 'sec(x)**3', 't/(1+t)'),
                                       ('diff(sec(x)**3*tan(x)/4,x)+Rational(3,4)*sec(x)**3', 'sec(x)**5')], 'U-T6 sec quick'))),
        memo='الأسس تنزل 2 2، كل حد على أسه، الإشارات تتبادل، والآخر $x$ أو $\\ln|\\sec x|$.',
        never=['إذا مع tan دالة sec (مثل $\\tan^3x\\sec^2x$): هذي الأنواع 25 و26، احجز.',
               'sec بأس زوجي وحده (مثل $\\sec^4x$): احجز $\\sec^2x$، هذا النوع 25.'],
        paper='اكتب أول كسرة ($\\tan^4x=\\tan^2x(\\sec^2x-1)$)، ثم السلسلة كاملة.',
        tries=[(r'\int\tan^{7}x\,dx', r'\frac{\tan^{6}x}{6}-\frac{\tan^{4}x}{4}+\frac{\tan^{2}x}{2}-\ln|\sec x|',
                [('diff(tan(x)**6/6-tan(x)**4/4+tan(x)**2/2-log(sec(x)),x)', 'tan(x)**7')]),
               (r'\int\tan^{8}x\,dx', r'\frac{\tan^{7}x}{7}-\frac{\tan^{5}x}{5}+\frac{\tan^{3}x}{3}-\tan x+x',
                [('diff(tan(x)**7/7-tan(x)**5/5+tan(x)**3/3-tan(x)+x,x)', 'tan(x)**8')])]))
    U.add('ok', '✔ تأكد', p(rich('آخر حد في جوابك: أس tan زوجي يعطي $x$ أو $-x$، وأس tan فردي يعطي $\\ln|\\sec x|$ بإشارة. '
                                 'في المثال 1 الأس 4 والجواب ينتهي بـ $+x$ ✓.')))
    U.add('trap', '⚠️ الفخ', ul([rich('لا تنسَ آخر حد: $x$ مع الأس الزوجي، و $\\ln|\\sec x|$ مع الأس الفردي.'),
                                'لما تحط ناتج التكامل الثاني، حطه بين قوسين. السالب اللي قدّامه يقلب كل إشاراته.']))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\int\tan^{4}x\,dx=\int\tan^{2}x\,(\sec^{2}x-1)\,dx=\frac{\tan^{3}x}{3}-\int\tan^{2}x\,dx',
                   [('tan(x)**4', 'tan(x)**2*(sec(x)**2-1)'), ('diff(tan(x)**3/3,x)-tan(x)**2', 'tan(x)**4')], 'U-T6 paper'))
          + p(rich('ثم $\\int\\tan^2x\\,dx=\\tan x-x$، ووزّع السالب.')))
    U.gist('tan وحدها، أو sec فردي وحده', 'tan: اكسر $\\tan^2x=\\sec^2x-1$. sec: تجزئة مع $dv=\\sec^2x\\,dx$',
           'كرّر لين يخلص الأس. ومع sec يرجع التكامل: اجمعه في طرف واقسم')
    U.drill('1', 'G-93', 'G', 'نفس المتطابقة بزاوية $2x$.',
            first=r'\tan^{2}2x=\sec^{2}2x-1', claims=[('tan(2*x)**2', 'sec(2*x)**2-1')],
            sol_rows=[('line', 'Integral(sec(2*x)**2,x)-Integral(1,x)', 'نفصل لتكاملين.'),
                      ('tex', r'\int\sec^{2}2x\,dx=\frac{\tan2x}{2}', [('diff(tan(2*x)/2,x)', 'sec(2*x)**2')],
                       'تكامل $\\sec^2$ هو tan، ونقسم على 2 رقم $x$.'),
                      ('line', 'tan(2*x)/2-x', 'وتكامل 1 هو $x$.'),
                      ('tex', r'\frac{\tan2x}{1\cdot2}-x', [('diff(tan(2*x)/(1*2)-x,x)', 'tan(2*x)**2')],
                       '✔ تأكد بالسريع: سلسلة tan مع أس 2 تعطي $\\frac{\\tan}{1}$ ثم $-x$. ومع $2x$ نقسم على 2 بعد.')])
    U.drill('2', 'N52-X16', 'G', 'الحد الأول تعويض، والثاني $\\int\\tan^4x\\,dx$ هو المثال 1.',
            first=r'\tan^{6}x=\tan^{4}x\,(\sec^{2}x-1)=\tan^{4}x\sec^{2}x-\tan^{4}x',
            claims=[('tan(x)**6', 'tan(x)**4*sec(x)**2-tan(x)**4')],
            sol_rows=[('line', 'tan(x)**5/5-Integral(tan(x)**4,x)', 'الحد الأول تعويض $u=\\tan x$: $\\int u^4du=\\frac{u^5}{5}$.'),
                      ('line', 'tan(x)**5/5-(tan(x)**3/3-tan(x)+x)', '$\\int\\tan^4x\\,dx$ هو المثال 1. نحطه بين قوسين، لأن قدّامه سالب.'),
                      ('line', 'tan(x)**5/5-tan(x)**3/3+tan(x)-x', 'نوزّع السالب: يقلب إشارة كل حد داخل القوس.'),
                      ('tex', r'\frac{\tan^{5}x}{5}-\frac{\tan^{3}x}{3}+\frac{\tan x}{1}-x',
                       [('diff(tan(x)**5/5-tan(x)**3/3+tan(x)/1-x,x)', 'tan(x)**6')],
                       '✔ تأكد بالسريع: سلسلة tan. الأسس 5 ثم 3 ثم 1، والإشارات تتناوب، والأس زوجي فآخر حد $x$.')])
    U.drill('3', 'G-94', 'P', 'اكسر مرتين. والأس فردي، فآخر حد فيه $\\ln|\\sec x|$.',
            sol_rows=[('tex', r'\tan^{5}x=\tan^{3}x\,(\sec^{2}x-1)', [('tan(x)**5', 'tan(x)**3*(sec(x)**2-1)')],
                       'tan وحدها. نكسر مربع واحد بـ $\\tan^2x=\\sec^2x-1$.'),
                      ('tex', r'=\tan^{3}x\sec^{2}x-\tan^{3}x', [('tan(x)**3*(sec(x)**2-1)', 'tan(x)**3*sec(x)**2-tan(x)**3')],
                       'نوزّع $\\tan^3x$ على القوس.'),
                      ('line', 'tan(x)**4/4-Integral(tan(x)**3,x)', 'الحد الأول تعويض $u=\\tan x$: $\\int u^3du=\\frac{u^4}{4}$.'),
                      ('tex', r'\tan^{3}x=\tan x\sec^{2}x-\tan x', [('tan(x)**3', 'tan(x)*sec(x)**2-tan(x)')],
                       'نكسر $\\tan^3x$ بنفس المتطابقة، ونوزّع $\\tan x$.'),
                      ('tex', r'\int\tan^{3}x\,dx=\frac{\tan^{2}x}{2}-\ln|\sec x|', [('diff(tan(x)**2/2-log(sec(x)),x)', 'tan(x)**3')],
                       'الأول تعويض يعطي $\\frac{u^2}{2}$. و $\\int\\tan x\\,dx=\\ln|\\sec x|$.'),
                      ('line', 'tan(x)**4/4-(tan(x)**2/2-log(Abs(sec(x))))', 'نحطه بين قوسين، لأن قدّامه سالب.'),
                      ('line', 'tan(x)**4/4-tan(x)**2/2+log(Abs(sec(x)))', 'نوزّع السالب على القوس.'),
                      ('tex', r'\frac{\tan^{4}x}{4}-\frac{\tan^{2}x}{2}+\ln|\sec x|',
                       [('diff(tan(x)**4/4-tan(x)**2/2+log(sec(x)),x)', 'tan(x)**5')],
                       '✔ تأكد بالسريع: سلسلة tan. الأسس 4 ثم 2، والإشارات تتناوب، والأس فردي فآخر حد $\\ln|\\sec x|$.')])
    A3 = '(sec(x)*tan(x)/2+log(Abs(sec(x)+tan(x)))/2)'
    B = '(sec(x)**3*tan(x)/4+3*sec(x)*tan(x)/8+3*log(Abs(sec(x)+tan(x)))/8)'
    U.drill('4', 'N52-X15', 'I', 'تجزئة مع $u=\\sec^3x$ و $dv=\\sec^2x\\,dx$، و $\\int\\sec^3x\\,dx$ هو المثال 2.',
            sol_rows=[('parts', 'sec(x)**3', 'sec(x)**2', '3*sec(x)**3*tan(x)', 'tan(x)',
                       '$u=\\sec^3x$ و $dv=\\sec^2x\\,dx$. مشتقة $\\sec^3x$ بقاعدة السلسلة: $3\\sec^2x\\cdot\\sec x\\tan x$.'),
                      ('line', 'sec(x)**3*tan(x)-Integral(3*sec(x)**3*tan(x)**2,x)', 'نعوّض في القانون $uv-\\int v\\,du$.'),
                      ('tex', r'3\sec^{3}x\tan^{2}x=3\sec^{3}x\,(\sec^{2}x-1)', [('3*sec(x)**3*tan(x)**2', '3*sec(x)**3*(sec(x)**2-1)')],
                       'نحوّل $\\tan^2x=\\sec^2x-1$.'),
                      ('tex', r'=3\sec^{5}x-3\sec^{3}x', [('3*sec(x)**3*(sec(x)**2-1)', '3*sec(x)**5-3*sec(x)**3')], 'نوزّع على القوس.'),
                      ('tex', r'J=\sec^{3}x\tan x-3J+3\int\sec^{3}x\,dx', [('sec(x)**3*tan(x)-3*%s+3*%s' % (B, A3), B)],
                       'نسمّي $J=\\int\\sec^5x\\,dx$. رجع $J$ نفسه، ومعه $\\int\\sec^3x\\,dx$.'),
                      ('tex', r'4J=\sec^{3}x\tan x+3\int\sec^{3}x\,dx', [('4*%s' % B, 'sec(x)**3*tan(x)+3*%s' % A3)],
                       'ننقل $3J$ للطرف الأول: $J+3J=4J$.'),
                      ('tex', r'\int\sec^{3}x\,dx=\frac{\sec x\tan x}{2}+\frac12\ln|\sec x+\tan x|',
                       [('diff(sec(x)*tan(x)/2+log(sec(x)+tan(x))/2,x)', 'sec(x)**3')], 'هذا جواب المثال 2.'),
                      ('tex', r'J=\frac{\sec^{3}x\tan x}{4}+\frac{3\sec x\tan x}{8}+\frac38\ln|\sec x+\tan x|',
                       [('diff(sec(x)**3*tan(x)/4+3*sec(x)*tan(x)/8+3*log(sec(x)+tan(x))/8,x)', 'sec(x)**5')],
                       'نعوّض ونقسم على 4: $\\frac34\\cdot\\frac12=\\frac38$.'),
                      ('tex', r'\frac{\sec^{3}x\tan x}{4}+\frac34\int\sec^{3}x\,dx',
                       [('diff(sec(x)**3*tan(x)/4,x)+Rational(3,4)*sec(x)**3', 'sec(x)**5')],
                       '✔ تأكد بالسريع: نقسم على 4 (أس sec ناقص 1)، والرقم $\\frac34$ هو (أس sec ناقص 2) على (أس sec ناقص 1).')],
            extra_lines=2)
    return U


# ---------------------------------------------------------------- 28
def u_cotcsc():
    U = Unit('U-T7', 'cot و csc', '5.2', 'ص73، الحالات المشابهة', 6)
    U.add('idea', 'الفكرة', p(rich(
        'نفس tan و sec بالضبط، لأن مشتقة cot هي $-\\csc^2x$ ومشتقة csc هي $-\\csc x\\cot x$. '
        'الفرق الوحيد هذا 🔴 السالب، فيطلع سالب قدّام التكامل كله.')))
    U.add('sign', 'العلامة', when(
        'cot و csc مضروبتين: $\\int\\cot^4x\\csc^4x\\,dx$ أو $\\int\\cot^5x\\csc^3x\\,dx$.',
        'tan و sec: نفس الطريقة بدون السالب.',
        [(r'\int\cot^{4}x\csc^{4}x\,dx', 'تعويض: احجز $\\csc^2x$، و $u=\\cot x$', 'أس csc زوجي'),
         (r'\int\cot^{5}x\csc^{3}x\,dx', 'تعويض: احجز $\\csc x\\cot x$، و $u=\\csc x$', 'أس cot فردي')]))
    U.add('short', '🧭 الطريقة', method(script(TRIG_SCRIPT, [
        'csc زوجي: احجز $\\csc^2x$. cot فردي ومعه csc: احجز $\\csc x\\cot x$',
        '$u=\\cot x$ أو $u=\\csc x$. والباقي حوّله بالمتطابقة',
        '$du=-\\csc^2x\\,dx$ أو $du=-\\csc x\\cot x\\,dx$',
        'القطعة المحجوزة ÷ $du$ = $-1$، يعني 🔴 سالب قدّام التكامل كله',
        'فك القوس ووزّع، ثم كامل كل حد',
        None]))
        + laws('U-T7', [(r'\csc^{2}x=1+\cot^{2}x,\qquad \cot^{2}x=\csc^{2}x-1', [('csc(x)**2', '1+cot(x)**2'), ('cot(x)**2', 'csc(x)**2-1')]),
                        (r'\frac{d}{dx}\cot x=-\csc^{2}x,\qquad \frac{d}{dx}\csc x=-\csc x\cot x',
                         [('diff(cot(x),x)', '-csc(x)**2'), ('diff(csc(x),x)', '-csc(x)*cot(x)')])])
        + tricks([('نفس tan و sec بالضبط، وكل شي بسالب: $\\frac{d}{dx}\\cot x=-\\csc^2x$، و $\\frac{d}{dx}\\csc x=-\\csc x\\cot x$.',
                   [('diff(cot(x),x)', '-csc(x)**2'), ('diff(csc(x),x)', '-csc(x)*cot(x)')])], 'U-T7'))
    it = ITEMS['1446-S2-SE-Q2.4']
    ex = question(it, 'U-T7 example')
    ex += steps(it, [
        ('tex', r'\cot^{4}x\csc^{4}x=\cot^{4}x\csc^{2}x\cdot\cD{\csc^{2}x}', [('cot(x)**4*csc(x)**4', 'cot(x)**4*csc(x)**2*csc(x)**2')],
         'أس csc زوجي (4). نحجز $\\csc^2x$ لأنها مشتقة $\\cot x$ بسالب، فتصير 🟢 $du$.'),
        ('tex', r'\csc^{2}x=1+\cU{\cot^{2}x}', [('csc(x)**2', '1+cot(x)**2')],
         'نحوّل الباقي $\\csc^2x$ لـ cot، عشان كل شي يصير بدلالة 🔵 $\\cot x$.'),
        ('sub', 'cot(x)', '-csc(x)**2', 'نسمّي $u=\\cot x$. مشتقته $-\\csc^2x$، فـ $\\csc^2x\\,dx=-du$.'),
        ('tex', r'\int\cot^{4}x\csc^{4}x\,dx=\cR{-}\int\cU{u^{4}}(1+\cU{u^{2}})\,\cD{du}',
         [('cot(x)**4*csc(x)**4', '-cot(x)**4*(1+cot(x)**2)*diff(cot(x),x)')], 'نعوّض. 🔴 السالب اللي في $du$ يطلع قدّام التكامل.'),
        ('tex', r'u^{4}(1+u^{2})=u^{4}+u^{6}', [('u**4*(1+u**2)', 'u**4+u**6')], 'نوزّع $u^4$: الأسس تنجمع.'),
        ('tex', r'-\int\left(u^{4}+u^{6}\right)du=-\left(\frac{u^{5}}{5}+\frac{u^{7}}{7}\right)',
         [('-integrate(u**4+u**6,u)', '-(u**5/5+u**7/7)')], 'نكامل كل حد.'),
        ('tex', r'=-\frac{u^{5}}{5}-\frac{u^{7}}{7}', [('-(u**5/5+u**7/7)', '-u**5/5-u**7/7')], 'السالب يدخل على الحدين.'),
        ('line', '-cot(x)**5/5-cot(x)**7/7', 'نرجع $u=\\cot x$.')], 'U-T7 ex')
    ex += final(it, 'U-T7 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (اختبار سابق)', ex)
    U.add('ok', '✔ تأكد', p(rich('أعلى أس في جوابك إشارته سالبة دايم: هنا $-\\frac{\\cot^7x}{7}$ ✓. لأن مشتقة cot ومشتقة csc فيهم سالب.')))
    U.add('trap', '⚠️ الفخ', ul([rich('$\\frac{d}{dx}\\cot x=-\\csc^2x$ و $\\frac{d}{dx}\\csc x=-\\csc x\\cot x$: السالب في الاثنين.'),
                                'السالب اللي قدّام التكامل يدخل على كل الحدود، مو على أول حد بس.']))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\cot^{4}x\csc^{4}x=\cot^{4}x\,(1+\cot^{2}x)\csc^{2}x,\qquad \cU{u=\cot x},\quad \cD{\csc^{2}x\,dx=\cR{-}du}',
                   [('cot(x)**4*csc(x)**4', 'cot(x)**4*(1+cot(x)**2)*csc(x)**2'), ('diff(cot(x),x)', '-csc(x)**2')], 'U-T7 paper'))
          + p('ثم سطر التوزيع، وسطر الجواب.'))
    U.gist('cot و csc مضروبتين', 'csc زوجي: $u=\\cot x$. cot فردي: $u=\\csc x$', 'مثل tan و sec، والسالب قدّام التكامل كله')
    U.drill('1', 'N52-X08', 'G', 'سالب قدّام الكل، والقوس $(1+u^2)^2$.',
            first=r'\csc^{6}x=(1+\cot^{2}x)^{2}\csc^{2}x,\quad u=\cot x,\ du=-\csc^{2}x\,dx',
            claims=[('csc(x)**6', '(1+cot(x)**2)**2*csc(x)**2')],
            sol_rows=[('tex', r'\int\cot^{2}x\csc^{6}x\,dx=-\int u^{2}(1+u^{2})^{2}\,du',
                       [('cot(x)**2*csc(x)**6', '-cot(x)**2*(1+cot(x)**2)**2*diff(cot(x),x)')],
                       'نعوّض: $\\cot^2x$ تصير $u^2$، و $\\csc^2x\\,dx=-du$.'),
                      ('tex', r'(1+u^{2})^{2}=1+2u^{2}+u^{4}', [('(1+u**2)**2', '1+2*u**2+u**4')], 'نفك القوس.'),
                      ('tex', r'u^{2}(1+2u^{2}+u^{4})=u^{2}+2u^{4}+u^{6}', [('u**2*(1+2*u**2+u**4)', 'u**2+2*u**4+u**6')],
                       'نوزّع $u^2$: الأسس تنجمع.'),
                      ('tex', r'-\int\left(u^{2}+2u^{4}+u^{6}\right)du=-\left(\frac{u^{3}}{3}+\frac{2u^{5}}{5}+\frac{u^{7}}{7}\right)',
                       [('-integrate(u**2+2*u**4+u**6,u)', '-(u**3/3+2*u**5/5+u**7/7)')], 'نكامل كل حد.'),
                      ('line', '-cot(x)**3/3-2*cot(x)**5/5-cot(x)**7/7', 'السالب يدخل على كل الحدود، ونرجع $u=\\cot x$.')])
    U.drill('2', 'N52-X09', 'P', 'أس cot فردي، فـ $u=\\csc x$ و $du=-\\csc x\\cot x\\,dx$.',
            sol_rows=[('tex', r'\cot^{5}x\csc^{3}x=\cot^{4}x\csc^{2}x\cdot\csc x\cot x',
                       [('cot(x)**5*csc(x)**3', 'cot(x)**4*csc(x)**2*csc(x)*cot(x)')], 'أس cot فردي (5). نحجز $\\csc x\\cot x$.'),
                      ('tex', r'\cot^{4}x=(\csc^{2}x-1)^{2}', [('cot(x)**4', '(csc(x)**2-1)**2')], 'نحوّل الباقي $\\cot^2x=\\csc^2x-1$.'),
                      ('sub', 'csc(x)', '-csc(x)*cot(x)', 'نسمّي $u=\\csc x$، فـ $\\csc x\\cot x\\,dx=-du$.'),
                      ('tex', r'\int\cot^{5}x\csc^{3}x\,dx=-\int(u^{2}-1)^{2}u^{2}\,du',
                       [('cot(x)**5*csc(x)**3', '-(csc(x)**2-1)**2*csc(x)**2*diff(csc(x),x)')], 'نعوّض، والسالب يطلع قدّام التكامل.'),
                      ('tex', r'(u^{2}-1)^{2}u^{2}=u^{6}-2u^{4}+u^{2}', [('(u**2-1)**2*u**2', 'u**6-2*u**4+u**2')],
                       'نفك القوس ونوزّع $u^2$.'),
                      ('tex', r'-\int\left(u^{6}-2u^{4}+u^{2}\right)du=-\left(\frac{u^{7}}{7}-\frac{2u^{5}}{5}+\frac{u^{3}}{3}\right)',
                       [('-integrate(u**6-2*u**4+u**2,u)', '-(u**7/7-2*u**5/5+u**3/3)')], 'نكامل كل حد.'),
                      ('tex', r'=-\frac{u^{7}}{7}+\frac{2u^{5}}{5}-\frac{u^{3}}{3}', [('-(u**7/7-2*u**5/5+u**3/3)', '-u**7/7+2*u**5/5-u**3/3')],
                       'نوزّع السالب: يقلب إشارة كل حد.'),
                      ('line', '-csc(x)**7/7+2*csc(x)**5/5-csc(x)**3/3', 'نرجع $u=\\csc x$.')])
    U.drill('3', 'N52-E4-2', 'I', 'مثل التمرين 2، والباقي $(u^2-1)^2u^4$.',
            sol_rows=[('tex', r'\cot^{5}x\csc^{5}x=\cot^{4}x\csc^{4}x\cdot\csc x\cot x',
                       [('cot(x)**5*csc(x)**5', 'cot(x)**4*csc(x)**4*csc(x)*cot(x)')], 'أس cot فردي (5). نحجز $\\csc x\\cot x$.'),
                      ('tex', r'\cot^{4}x=(\csc^{2}x-1)^{2}', [('cot(x)**4', '(csc(x)**2-1)**2')], 'نحوّل الباقي من cot لـ csc.'),
                      ('sub', 'csc(x)', '-csc(x)*cot(x)', 'نسمّي $u=\\csc x$، فـ $\\csc x\\cot x\\,dx=-du$.'),
                      ('tex', r'\int\cot^{5}x\csc^{5}x\,dx=-\int(u^{2}-1)^{2}u^{4}\,du',
                       [('cot(x)**5*csc(x)**5', '-(csc(x)**2-1)**2*csc(x)**4*diff(csc(x),x)')], 'نعوّض، والسالب قدّام التكامل.'),
                      ('tex', r'(u^{2}-1)^{2}u^{4}=u^{8}-2u^{6}+u^{4}', [('(u**2-1)**2*u**4', 'u**8-2*u**6+u**4')],
                       'نفك القوس ونوزّع $u^4$.'),
                      ('tex', r'-\int\left(u^{8}-2u^{6}+u^{4}\right)du=-\left(\frac{u^{9}}{9}-\frac{2u^{7}}{7}+\frac{u^{5}}{5}\right)',
                       [('-integrate(u**8-2*u**6+u**4,u)', '-(u**9/9-2*u**7/7+u**5/5)')], 'نكامل كل حد.'),
                      ('tex', r'=-\frac{u^{9}}{9}+\frac{2u^{7}}{7}-\frac{u^{5}}{5}', [('-(u**9/9-2*u**7/7+u**5/5)', '-u**9/9+2*u**7/7-u**5/5')],
                       'نوزّع السالب.'),
                      ('line', '-csc(x)**9/9+2*csc(x)**7/7-csc(x)**5/5', 'نرجع $u=\\csc x$.')])
    return U


# ---------------------------------------------------------------- 29
def u_prod():
    U = Unit('U-T8', 'ضرب sin و cos بزاويتين مختلفتين', '5.2', 'ص74–75، مثال 5', 6)
    U.add('idea', 'الفكرة', p(rich(
        'دالتين بزاويتين مختلفتين ما فيهم دالة ومشتقتها، فالحجز ما ينفع. '
        'لكن متطابقة الضرب تحوّل الضرب لجمع، والجمع نكامله حد حد.')))
    U.add('sign', 'العلامة', when(
        'sin أو cos مضروبة في sin أو cos، والزاويتين مختلفتين: $\\int\\sin7x\\cos5x\\,dx$.',
        'نفس الزاوية ($\\sin^4x\\cos^5x$): تعويض بالحجز، أو نص الزاوية إذا الأسين زوجيين.',
        [(r'\int\sin7x\cos5x\,dx', 'تجهيز: الضرب إلى جمع', 'زاويتين مختلفتين'),
         (r'\int\sin^{4}x\cos^{5}x\,dx', 'تعويض: احجز $\\cos x$، و $u=\\sin x$', 'نفس الزاوية $x$، وأس فردي')]))
    U.add('short', '📐 القانون',
          p(rich('نسمّي الزاوية الأولى $A$ والثانية $B$. مثلًا في $\\sin7x\\cos5x$: $A=7x$ و $B=5x$.'))
          + laws('U-T8', [(r'\sin A\cos B=\frac12\left[\sin(A-B)+\sin(A+B)\right]', [('sin(a)*cos(b)', '(sin(a-b)+sin(a+b))/2')]),
                          (r'\sin A\sin B=\frac12\left[\cos(A-B)-\cos(A+B)\right]', [('sin(a)*sin(b)', '(cos(a-b)-cos(a+b))/2')]),
                          (r'\cos A\cos B=\frac12\left[\cos(A-B)+\cos(A+B)\right]', [('cos(a)*cos(b)', '(cos(a-b)+cos(a+b))/2')])])
          + p(rich('وإذا طلع الفرق سالب:'))
          + laws('U-T8 sign', [(r'\sin(-2x)=-\sin2x,\qquad \cos(-2x)=\cos2x', [('sin(-2*x)', '-sin(2*x)'), ('cos(-2*x)', 'cos(2*x)')])])
          + method(script(PREP_SCRIPT, [
              'زاويتين مختلفتين. سمّ الأولى $A$ والثانية $B$، واحسب الفرق والمجموع',
              'اختر المتطابقة حسب الدالتين: sin·cos أو sin·sin أو cos·cos',
              checked('U-T8 check', 'عوّض $x=\\frac\\pi4$ في المثال: $\\sin\\frac{7\\pi}{4}\\cos\\frac{5\\pi}{4}=\\frac12$، '
                      'و $\\frac12\\left[\\sin\\frac\\pi2+\\sin3\\pi\\right]=\\frac12$ ✓',
                      [('sin(7*pi/4)*cos(5*pi/4)', 'Rational(1,2)'), ('(sin(pi/2)+sin(3*pi))/2', 'Rational(1,2)')]),
              'صار جمع: كل حد من الجدول، و 🟠 اقسم على رقم $x$، ثم اضرب في $\\frac12$']))
          + tricks([('الضرب يصير جمع بزاويتين: الفرق والمجموع ($7x$ و $5x$ تعطي $2x$ و $12x$). و sin·sin الوحيدة اللي فيها ناقص.',
                     [('7-5', '2'), ('7+5', '12'), ('sin(7*x)*cos(5*x)', '(sin(2*x)+sin(12*x))/2')])], 'U-T8'))
    it = ITEMS['N52-E5-1']
    ex = question(it, 'U-T8 example')
    ex += steps(it, [
        ('tex', r'7x-5x=2x,\qquad 7x+5x=12x', [('7*x-5*x', '2*x'), ('7*x+5*x', '12*x')],
         'الزاويتين مختلفتين، فنستعمل متطابقة الضرب. نحسب الفرق والمجموع أول.'),
        ('tex', r'\sin7x\cos5x=\frac12\left[\sin2x+\sin12x\right]', [('sin(7*x)*cos(5*x)', '(sin(2*x)+sin(12*x))/2')],
         'متطابقة sin·cos: $\\frac12$ × (sin الفرق + sin المجموع).'),
        ('tex', r'\int\sin2x\,dx=\cR{-}\frac{\cos2x}{\cA{2}},\qquad \int\sin12x\,dx=\cR{-}\frac{\cos12x}{\cA{12}}',
         [('diff(-cos(2*x)/2,x)', 'sin(2*x)'), ('diff(-cos(12*x)/12,x)', 'sin(12*x)')],
         'نكامل كل حد لحاله: تكامل sin هو 🔴 سالب cos، و 🟠 نقسم على رقم $x$.'),
        ('tex', r'=\frac12\left(-\frac{\cos2x}{2}-\frac{\cos12x}{12}\right)',
         [('diff((-cos(2*x)/2-cos(12*x)/12)/2,x)', 'sin(7*x)*cos(5*x)')], 'نضرب في $\\frac12$ اللي من المتطابقة.'),
        ('line', '-cos(2*x)/4-cos(12*x)/24', 'نوزّع $\\frac12$: $\\frac12\\cdot\\frac12=\\frac14$، و $\\frac12\\cdot\\frac1{12}=\\frac1{24}$.')], 'U-T8 ex')
    ex += final(it, 'U-T8 example')
    U.add('ex', '🧱 مثال محلول خطوة خطوة (من مذكرة د. طارق)', ex)
    U.add('ok', '✔ تأكد', p(checked('U-T8 ok', 'في جوابك لازم تطلع زاويتين: الفرق والمجموع، هنا $2x$ و $12x$ ✓. '
                                    'وكل حد مقسوم على رقم زاويته وعلى 2: $2\\cdot2=4$ و $12\\cdot2=24$.',
                                    [('7-5', '2'), ('7+5', '12'), ('2*2', '4'), ('12*2', '24')])))
    U.add('trap', '⚠️ الفخ', ul([checked('U-T8 trap 1', 'إذا طلع الفرق سالب: $\\cos(-2x)=\\cos2x$، لكن $\\sin(-2x)=-\\sin2x$. انتبه للإشارة.',
                                        [('cos(-2*x)', 'cos(2*x)'), ('sin(-2*x)', '-sin(2*x)')]),
                                checked('U-T8 trap 2', 'sin·sin الوحيدة اللي فيها ناقص: $\\sin5x\\sin x=\\frac12\\left[\\cos4x-\\cos6x\\right]$.',
                                        [('sin(5*x)*sin(x)', '(cos(4*x)-cos(6*x))/2')])]))
    U.add('paper', '✍️ في ورقة الكويز',
          md(arith(r'\sin7x\cos5x=\frac12\left[\sin2x+\sin12x\right]', [('sin(7*x)*cos(5*x)', '(sin(2*x)+sin(12*x))/2')], 'U-T8 paper'))
          + p(rich('ثم كامل كل حد، ووزّع $\\frac12$.')))
    U.gist('sin أو cos مضروبة في sin أو cos، والزاويتين مختلفتين', 'متطابقة الضرب: الفرق والمجموع',
           'كامل كل حد واقسم على رقم $x$، ثم وزّع $\\frac12$')
    U.drill('1', 'N52-X10', 'G', 'الفرق سالب: $\\sin(-2x)=-\\sin2x$.',
            first=r'\sin3x\cos5x=\frac12\left[\sin(-2x)+\sin8x\right]=\frac12\left[-\sin2x+\sin8x\right]',
            claims=[('sin(3*x)*cos(5*x)', '(-sin(2*x)+sin(8*x))/2')],
            sol_rows=[('tex', r'\int\sin2x\,dx=-\frac{\cos2x}{2},\qquad \int\sin8x\,dx=-\frac{\cos8x}{8}',
                       [('diff(-cos(2*x)/2,x)', 'sin(2*x)'), ('diff(-cos(8*x)/8,x)', 'sin(8*x)')],
                       'نكامل كل حد لحاله: تكامل sin هو سالب cos، ونقسم على رقم $x$.'),
                      ('tex', r'=\frac12\left(\frac{\cos2x}{2}-\frac{\cos8x}{8}\right)',
                       [('diff((cos(2*x)/2-cos(8*x)/8)/2,x)', 'sin(3*x)*cos(5*x)')],
                       'الحد الأول قدّامه سالب، وسالب في سالب = موجب. ونضرب في $\\frac12$.'),
                      ('line', 'cos(2*x)/4-cos(8*x)/16', 'نوزّع $\\frac12$ على الحدين.')])
    U.drill('2', 'N52-E5-2', 'P', 'sin·sin فيها ناقص بين الحدين.',
            sol_rows=[('tex', r'4x-3x=x,\qquad 4x+3x=7x', [('4*x-3*x', 'x'), ('4*x+3*x', '7*x')],
                       'الزاويتين مختلفتين. نحسب الفرق والمجموع.'),
                      ('tex', r'\sin4x\sin3x=\frac12\left[\cos x-\cos7x\right]', [('sin(4*x)*sin(3*x)', '(cos(x)-cos(7*x))/2')],
                       'متطابقة sin·sin: cos الفرق ناقص cos المجموع.'),
                      ('tex', r'\int\cos x\,dx=\sin x,\qquad \int\cos7x\,dx=\frac{\sin7x}{7}',
                       [('diff(sin(x),x)', 'cos(x)'), ('diff(sin(7*x)/7,x)', 'cos(7*x)')], 'نكامل كل حد: تكامل cos هو sin، ونقسم على رقم $x$.'),
                      ('line', 'sin(x)/2-sin(7*x)/14', 'نضرب في $\\frac12$: $\\frac12\\cdot\\frac17=\\frac1{14}$.')])
    U.drill('3', 'G-14', 'I', 'cos·cos فيها زائد بين الحدين.',
            sol_rows=[('tex', r'3x-x=2x,\qquad 3x+x=4x', [('3*x-x', '2*x'), ('3*x+x', '4*x')], 'نحسب الفرق والمجموع.'),
                      ('tex', r'\cos3x\cos x=\frac12\left[\cos2x+\cos4x\right]', [('cos(3*x)*cos(x)', '(cos(2*x)+cos(4*x))/2')],
                       'متطابقة cos·cos: زائد بين الحدين.'),
                      ('tex', r'\int\cos2x\,dx=\frac{\sin2x}{2},\qquad \int\cos4x\,dx=\frac{\sin4x}{4}',
                       [('diff(sin(2*x)/2,x)', 'cos(2*x)'), ('diff(sin(4*x)/4,x)', 'cos(4*x)')], 'نكامل كل حد ونقسم على رقم $x$.'),
                      ('line', 'sin(2*x)/4+sin(4*x)/8', 'نضرب في $\\frac12$.')])
    return U


UNITS_52 = [u_odd_alone, u_sc_odd, u_even, u_sec_even, u_tan_odd, u_reduce, u_cotcsc, u_prod]

"""المذكرة الكاملة — الدرس 5.1: التكامل بالتجزئة (الأيام 3–5)."""
from booklet import di_table, sc_dawaran, sc_nisfayn, sc_qaws, sc_rafeeq
from booklet_engine import ITEMS, arith, formula, functional, same_value
from guide_kit import Unit, alg, contrast, final, question, rich, short_steps, steps
from guide_rules import R
from guide_42 import box_memo, frow
from html_kit import md, mi, p, table, ul
import sympy as s
from mathlib import x


def int_table(label):
    rows = [formula('exp(k*x)', 'exp(k*x)/k', var='x', branches=('x',), pos=('k',), label=label + ' e'),
            formula('sin(k*x)', '-cos(k*x)/k', var='x', branches=('x',), pos=('k',), label=label + ' sin'),
            formula('cos(k*x)', 'sin(k*x)/k', var='x', branches=('x',), pos=('k',), label=label + ' cos'),
            formula('sinh(k*x)', 'cosh(k*x)/k', var='x', branches=('x',), pos=('k',), label=label + ' sinh'),
            formula('cosh(k*x)', 'sinh(k*x)/k', var='x', branches=('x',), pos=('k',), label=label + ' cosh'),
            formula('sec(x)**2', 'tan(x)', var='x', branches=('t/(1+t)',), label=label + ' sec2')]
    return table(['التكامل', 'الجواب (+C)'], [frow(z) for z in rows], 'formula compact')


# ---------------------------------------------------------------- 12
def u_parts_linear():
    U = Unit('U-P1', 'فكرة التجزئة: كثيرة حدود خطية × دالة', '5.1', 'ص63', 3)
    U.add('idea', 'الفكرة', p(rich(
        'قاعدة الضرب في الاشتقاق $(uv)\'=u\'v+uv\'$ إذا قلبناها تكاملًا تطلع قاعدة التجزئة: '
        '$\\int u\\,dv=uv-\\int v\\,du$. عندك شيئان مضروبان: خلّ واحدًا <b>يصغر لما تشتقه</b> ($3x-2$ يصير 3)، '
        'والثاني <b>سهل تكامله</b> ($\\sinh x$ يصير $\\cosh x$).')))
    U.add('sign', 'العلامة', p(rich('حد مثل $(px+q)$ مضروب في $e^{kx}$ أو $\\sin kx$ أو $\\cos kx$ أو $\\sinh kx$ أو $\\cosh kx$ أو $\\sec^2x$.'))
          + contrast([(r'\int x\cosh x\,dx', 'تجزئة', '$x$ ليست مشتقة شيء داخل cosh'),
                      (r'\int x\cosh(x^{2})\,dx', 'تعويض $u=x^2$', '$x$ موجودة كمشتقة لـ $x^2$ (تقريبًا)')]))
    U.add('note', 'تذكير: تكاملات تحتاجها', int_table('G parts table')
          + p(rich('مع sin الإشارة سالبة: $\\int\\sin x\\,dx=-\\cos x$. مع sinh موجبة: $\\int\\sinh x\\,dx=\\cosh x$.'), 'small'))
    G1, G2, g = s.Function('G_1')(x), s.Function('G_2')(x), s.Function('g')(x)
    pp, qq = s.symbols('p q', real=True)
    functional(lambda: (s.diff((pp * x + qq) * G1 - pp * G2, x) - (pp * x + qq) * g)
               .subs({s.Derivative(G1, x): g, s.Derivative(G2, x): G1}), 'G linear rule')
    U.add('short', '⚡ الاختصار', md(r'\int(px+q)\,g\,dx=(px+q)\,G_{1}-p\,G_{2}+C')
          + p(rich('$G_1$ تكامل $g$، و $G_2$ تكامل $G_1$، و $p$ معامل $x$.'), 'small')
          + box_memo('القوس كما هو × التكامل الأول، ناقص معامل x × التكامل الثاني.'))
    it = ITEMS['1446-S1-SE-Q2.4']
    ex = question(it, 'U-P1 example')
    ex += short_steps(it, [
        ('القانون: قوس خطي × دالة', r'\int(px+q)\,g\,dx=(px+q)\,G_{1}-p\,G_{2}+C', [R('linear')]),
        ('طلّع $p$: معامل $x$ في القوس $3x-2$', r'p=3', [('diff(3*x-2,x)', '3')]),
        ('$G_1$: كامل الدالة الثانية $g=\\sinh x$ مرة', r'G_{1}=\int\sinh x\,dx=\cosh x', [('integrate(sinh(x),x)', 'cosh(x)')]),
        ('$G_2$: كامل $G_1$ مرة ثانية', r'G_{2}=\int\cosh x\,dx=\sinh x', [('integrate(cosh(x),x)', 'sinh(x)')]),
        ('عوّض: القوس كما هو × $G_1$، ناقص $p$ × $G_2$؛ = السطران 2–3 في 🧱', r'(3x-2)\cosh x-3\sinh x+C',
         [('=ANS', '(3*x-2)*cosh(x)-3*sinh(x)')])], 'U-P1 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('parts', '3*x-2', 'sinh(x)', '3', 'cosh(x)', 'نختار $u$ كثيرة الحدود لأنها تصغر بالاشتقاق'),
        ('line', '(3*x-2)*cosh(x)-Integral(3*cosh(x),x)', 'القانون: $uv-\\int v\\,du$'),
        ('line', '(3*x-2)*cosh(x)-3*sinh(x)', 'الثابت 3 يطلع من التكامل (🧮)، وتكامل cosh هو sinh')], 'U-P1 ex')
    ex += final(it, 'U-P1 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.raw(alg('const-out', 'الثابت يطلع من التكامل', [
        (r'\int3\cosh x\,dx=3\int\cosh x\,dx=3\sinh x', [('integrate(3*cosh(x),x)', '3*sinh(x)')], 'الرقم المضروب يخرج قدّام التكامل:'),
        (r'-\int3\cosh x\,dx=-3\sinh x', [('-integrate(3*cosh(x),x)', '-3*sinh(x)')], 'ومعه إشارته:')]))
    same_value('diff((3*x-2)*cosh(x)-3*sinh(x),x)', '(3*x-2)*sinh(x)', 'U-P1 check')
    U.add('ok', '✔ تأكد في 10 ثواني', p(rich('اشتق جوابك: $3\\cosh x+(3x-2)\\sinh x-3\\cosh x=(3x-2)\\sinh x$ ✓ رجع السؤال.')))
    U.add('trap', '⚠️ الفخ', ul([rich('لا تنسَ ضرب $p$ في الحد الثاني، ولا $+C$.'),
                                rich('مع sin و cos: $\\int\\sin x\\,dx=-\\cos x$، فانتبه للإشارات.')]))
    U.add('paper', '✍️ في ورقة الكويز', md(r'\begin{array}{l}u=3x-2\qquad dv=\sinh x\,dx\\du=3\,dx\qquad v=\cosh x\end{array}')
          + md(r'\int(3x-2)\sinh x\,dx=(3x-2)\cosh x-3\int\cosh x\,dx \\ \qquad=(3x-2)\cosh x-3\sinh x+C'))
    U.drill('1', 'N51-E1', 'G', 'مع cos: $G_1=\\sin x$، و $G_2=\\int\\sin x\\,dx=-\\cos x$.',
            first=r'p=1,\quad G_{1}=\sin x,\quad G_{2}=-\cos x',
            claims=[('integrate(cos(x),x)', 'sin(x)'), ('integrate(sin(x),x)', '-cos(x)')])
    U.drill('2', '1446-S2-SE-Q2.3', 'P', '$p=2$، $G_1=\\sinh x$، $G_2=\\cosh x$.')
    U.drill('3', 'N51-X04', 'I', '$G_1=\\tan x$، و $G_2=\\int\\tan x\\,dx=-\\ln|\\cos x|$.',
            sol_rows=[('parts', 'x+1', 'sec(x)**2', '1', 'tan(x)', 'كثيرة الحدود $u$'),
                      ('line', '(x+1)*tan(x)-Integral(tan(x),x)', 'القانون'),
                      ('tex', r'-\int\tan x\,dx=-\left(-\ln|\cos x|\right)=+\ln|\cos x|', [('diff(-log(cos(x)),x)', 'tan(x)')],
                       '$\\int\\tan x\\,dx=-\\ln|\\cos x|$، وسالب في سالب = موجب')])
    return U


# ---------------------------------------------------------------- 13
def u_parts_di():
    U = Unit('U-P2', 'كثيرة حدود درجة 2 أو 3: جدول DI', '5.1', 'ص63–64، تمارين 2 و3', 3)
    U.add('idea', 'الفكرة', p(rich('مع $x^2$ أو $x^3$ نحتاج التجزئة مرتين أو ثلاثًا. جدول DI يرتّب كل التجزئات في جدول واحد: '
                                   'عمود نشتق فيه كثيرة الحدود حتى الصفر، وعمود نكامل فيه الدالة الثانية.')))
    U.add('sign', 'العلامة', p(rich('$x^2$ أو $x^3$ (أو كثيرة حدود من درجتهما) × $e^{kx}$ أو sin أو cos أو sinh أو cosh.')))
    U.add('short', '⚡ الاختصار: جدول DI', ul([
        rich('عمود <b>D</b>: اشتق كثيرة الحدود حتى تصل صفر.'),
        rich('عمود <b>I</b>: كامل الدالة الثانية في كل صف.'),
        rich('اضرب كل خانة في D بالخانة <b>تحتها قطريًا</b> في I، والإشارات تتناوب $+\\ -\\ +\\ -$.'),
        'لا تضرب صف الصفر.']) + box_memo('كثيرة الحدود تنزل للصفر، والدالة الثانية تُكامل، والإشارات تتناوب.'))
    it = ITEMS['1445-S1-FE-Q2.2']
    ex = question(it, 'U-P2 example')
    ex += short_steps(it, [
        ('القانون (جدول DI): كثيرة الحدود $f$ تُشتق، والدالة $g$ تُكامل، والإشارات $+\\ -\\ +$',
         r"\int f\,g\,dx=f\,G_{1}-f'\,G_{2}+f''\,G_{3}+C", [R('di')]),
        ('عمود D: اشتق $f=x^2$ حتى توصل صفر', r'x^{2}\ \to\ 2x\ \to\ 2\ \to\ 0', [('diff(x**2,x)', '2*x'), ('diff(2*x,x)', '2'), ('diff(2,x)', '0')]),
        ('عمود I: كامل $g=\\cosh x$ في كل صف', r'\cosh x\ \to\ \sinh x\ \to\ \cosh x\ \to\ \sinh x',
         [('integrate(cosh(x),x)', 'sinh(x)'), ('integrate(sinh(x),x)', 'cosh(x)')]),
        ('اضرب كل خانة في D بالخانة تحتها قطريًا في I مع إشارتها (الجدول تحت)',
         r'(+)\,x^{2}\cdot\sinh x\quad(-)\,2x\cdot\cosh x\quad(+)\,2\cdot\sinh x', [('x**2*sinh(x)-2*x*cosh(x)+2*sinh(x)', 'x**2*sinh(x)+(-1)*(2*x)*cosh(x)+2*sinh(x)')]),
        ('اجمع الحدود الثلاثة؛ = التجزئتان في 🧱 مرة واحدة', r'x^{2}\sinh x-2x\cosh x+2\sinh x+C',
         [('=ANS', 'x**2*sinh(x)-2*x*cosh(x)+2*sinh(x)')])], 'U-P2 ex')
    ex += di_table([('+', 'x**2', 'cosh(x)'), ('-', '2*x', 'sinh(x)'), ('+', '2', 'cosh(x)'), (r'\cdot', '0', 'sinh(x)')])
    ex += p('<b>🧱 خطوة خطوة (نفس الشي بالتجزئة مرتين):</b>') + steps(it, [
        ('parts', 'x**2', 'cosh(x)', '2*x', 'sinh(x)', 'أول تجزئة: $u=x^2$'),
        ('line', 'x**2*sinh(x)-Integral(2*x*sinh(x),x)', 'القانون'),
        ('parts', '2*x', 'sinh(x)', '2', 'cosh(x)', 'ثاني تجزئة على التكامل الباقي'),
        ('line', 'x**2*sinh(x)-(2*x*cosh(x)-Integral(2*cosh(x),x))', 'نعوّض الناتج داخل قوس'),
        ('line', 'x**2*sinh(x)-2*x*cosh(x)+2*sinh(x)', 'نوزّع السالب على القوس (🧮)')], 'U-P2 ex')
    ex += final(it, 'U-P2 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.raw(alg('neg-bracket', 'توزيع السالب على قوس', [
        (r'-\left(2x\cosh x-2\sinh x\right)=-2x\cosh x+2\sinh x', [('-(2*x*cosh(x)-2*sinh(x))', '-2*x*cosh(x)+2*sinh(x)')],
         'السالب يقلب إشارة كل حد داخل القوس:'),
        (r'-(-a)=+a', [], 'سالب في سالب = موجب.')]))
    U.add('trap', '⚠️ الفخ', ul([rich('مع $\\sin kx$ أو $\\cos kx$: كل تكامل يقسم على $k$ ويغيّر الإشارة حسب النوع. اكتب عمود I بهدوء.'),
                                'يتوقف الجدول عندما يصل عمود D إلى صفر.']))
    U.add('paper', '✍️ في ورقة الكويز', p('اكتب الجدول نفسه، ثم سطر الجواب. الجدول تنظيم للتجزئة المتكررة ويقبله المصحح عادة.'))
    U.drill('1', 'N51-E2', 'G', 'كل تكاملات $e^x$ هي $e^x$؛ الإشارات $+\\,-\\,+$.',
            first=r'D:\ x^{2},\ 2x,\ 2,\ 0\qquad I:\ e^{x},\ e^{x},\ e^{x},\ e^{x}',
            claims=[('diff(x**2,x)', '2*x'), ('integrate(exp(x),x)', 'exp(x)')])
    U.drill('2', 'N51-X03', 'P', 'أربعة صفوف قبل الصفر: $x^3,\\ 3x^2,\\ 6x,\\ 6$.')
    U.drill('3', 'N51-X02', 'I', 'تكاملات $\\sin2x$: $-\\frac12\\cos2x$، ثم $-\\frac14\\sin2x$، ثم $\\frac18\\cos2x$.')
    return U


# ---------------------------------------------------------------- 14
def u_qaws():
    U = Unit('U-P3', 'قوة × ln (القوس)', '5.1', 'ص64، تمارين 5–7', 4)
    U.add('idea', 'الفكرة', p(rich('$\\ln$ تكاملها صعب لكن مشتقتها سهلة ($\\frac1x$). فدائمًا $u=\\ln$، و $dv$ = القوة. '
                                   'بعد التجزئة يصير التكامل الباقي قوة بسيطة.')))
    U.add('sign', 'العلامة', p(rich('$x^n$ (حتى لو $n$ سالب) مضروبة في $\\ln|ax|$.')))
    short, memo = sc_qaws()
    U.add('short', '⚡ الاختصار', short + box_memo(memo))
    it = ITEMS['N51-E3']
    ex = question(it, 'U-P3 example 1')
    ex += short_steps(it, [
        ('القانون: قوة × ln (القوس)', r'\int x^{n}\ln|x|\,dx=\frac{x^{n+1}}{n+1}\left(\ln|x|-\frac{1}{n+1}\right)+C', [R('xn ln')]),
        ('طلّع $n$: أس $x$، وزِد عليه 1', r'n=2,\qquad n+1=3', [('2+1', '3')]),
        ('عوّض $n+1=3$ في المكانين', r'\frac{x^{3}}{3}\left(\ln|x|-\frac13\right)', [('=ANS', 'x**3/3*(log(Abs(x))-Rational(1,3))')]),
        ('وزّع $\\frac{x^3}{3}$ على القوس: $\\frac{x^3}{3}\\cdot\\frac13=\\frac{x^3}{9}$؛ = جواب 🧱', r'=\frac{x^{3}}{3}\ln|x|-\frac{x^{3}}{9}+C',
         [('x**3/3*Rational(1,3)', 'x**3/9'), ('=ANS', 'x**3*log(Abs(x))/3-x**3/9')])], 'U-P3 ex1')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('parts', 'log(Abs(x))', 'x**2', '1/x', 'x**3/3', 'ln دائمًا $u$', 't'),
        ('line', 'x**3*log(Abs(x))/3-Integral(x**2/3,x)', '$v\\,du=\\frac{x^3}{3}\\cdot\\frac1x=\\frac{x^2}{3}$ (🧮)'),
        ('line', 'x**3*log(Abs(x))/3-x**3/9', '$\\int\\frac{x^2}{3}dx=\\frac{x^3}{9}$')], 'U-P3 ex1')
    ex += final(it, 'U-P3 example 1')
    U.add('ex', 'مثال 1 (من مذكرة د. طارق)', ex)
    U.raw(alg('pow-rules', 'قواعد الأسس', [
        (r'\frac{x^{3}}{3}\cdot\frac{1}{x}=\frac{x^{3-1}}{3}=\frac{x^{2}}{3}', [('x**3/3*(1/x)', 'x**2/3')], 'القسمة على $x$ تنقص الأس 1:'),
        (r'x^{-2}=\frac{1}{x^{2}}', [('x**(-2)', '1/x**2')], 'الأس السالب = مقلوب:'),
        (r'\int x^{-2}dx=\frac{x^{-1}}{-1}=-\frac1x', [('integrate(x**(-2),x)', '-1/x')], 'قاعدة القوة مع أس سالب: نزيد 1 ونقسم عليه:'),
        (r'\frac{x^{-3}}{-3}=-\frac{1}{3x^{3}}', [('x**(-3)/(-3)', '-1/(3*x**3)')], 'والسالب يطلع قدّام الكسر:')]))
    it = ITEMS['1446-S1-SE-Q2.5']
    ex = question(it, 'U-P3 example 2')
    ex += short_steps(it, [
        ('القانون نفسه (هنا $\\ln x$ لأن $x>0$)', r'\int x^{n}\ln x\,dx=\frac{x^{n+1}}{n+1}\left(\ln x-\frac{1}{n+1}\right)+C', [R('xn ln')]),
        ('اكتب الكسر كقوة سالبة (🧮 قواعد الأسس)، وطلّع $n$', r'\frac{\ln x}{x^{2}}=x^{-2}\ln x\ \Rightarrow\ n=-2,\quad n+1=-1',
         [('log(x)/x**2', 'x**(-2)*log(x)'), ('-2+1', '-1')]),
        ('عوّض $n+1=-1$ في المكانين', r'\frac{x^{-1}}{-1}\left(\ln x-\frac{1}{-1}\right)', [('=ANS', 'x**(-1)/(-1)*(log(x)-1/(-1))')]),
        ('بسّط: $\\frac{x^{-1}}{-1}=-\\frac1x$، و $-\\frac{1}{-1}=+1$ (سالب في سالب)؛ = جواب 🧱',
         r'=-\frac{1}{x}\left(\ln x+1\right)=-\frac{\ln x+1}{x}+C', [('x**(-1)/(-1)', '-1/x'), ('=ANS', '-(log(x)+1)/x')])], 'U-P3 ex2')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('parts', 'log(x)', 'x**(-2)', '1/x', '-1/x', 'ln دائمًا $u$', 't'),
        ('line', '-log(x)/x-Integral(-1/x**2,x)', '$v\\,du=-\\frac1x\\cdot\\frac1x=-\\frac{1}{x^2}$'),
        ('line', '-log(x)/x-1/x', '$\\int\\frac{dx}{x^2}=-\\frac1x$، وسالب في سالب (🧮 قواعد الأسس)')], 'U-P3 ex2')
    ex += final(it, 'U-P3 example 2')
    U.add('ex', 'مثال 2: أس سالب (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('$n=-1$، أي $\\int\\frac{\\ln|x|}{x}dx$، ليست تجزئة: عوّض $u=\\ln|x|$ فالجواب $\\frac{(\\ln|x|)^2}{2}$.'),
                                rich('مع $\\ln|2x|$ المشتقة $\\frac1x$ (الـ 2 تختفي)، والقاعدة كما هي.')]))
    U.add('paper', '✍️ في ورقة الكويز', md(r'\begin{array}{l}u=\ln|x|\qquad dv=x^{2}dx\\du=\frac1x\,dx\qquad v=\frac{x^{3}}{3}\end{array}')
          + p('ثم سطر القانون والجواب.'))
    U.drill('1', '1445-S2-SE-Q2.5', 'G', 'وزّع القوس: $\\frac{x^2}{2}\\ln|x|-\\frac{x^2}{4}$.',
            first=r'n=1,\quad n+1=2:\quad \frac{x^{2}}{2}\left(\ln|x|-\frac12\right)',
            claims=[('diff(x**2/2*(log(x)-Rational(1,2)),x)', 'x*log(x)')])
    U.drill('2', 'N51-X07', 'P', '$n=-4$ فـ $n+1=-3$ (🧮 قواعد الأسس).')
    U.drill('3', '1447-S1-SE-Q2.7', 'I', 'مشتقة $\\ln|2x|$ هي $\\frac1x$؛ القاعدة نفسها مع $n=3$.')
    return U


# ---------------------------------------------------------------- 15
def u_ln_alone():
    U = Unit('U-P4', 'ln وحدها، و (ln x)²، و ln(1+x²)', '5.1', 'ص64، تمارين 5 و16 ومثال 4', 4)
    U.add('idea', 'الفكرة', p(rich('ما فيه ضرب ظاهر؟ اكتب $dv=dx$ (واحد مخفي): $u=\\ln$ و $v=x$.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\ln|x|\\,dx$ أو $\\int(\\ln|x|)^2dx$ أو $\\int\\ln(1+x^2)dx$: ln وحدها.')))
    r = [formula('log(Abs(x))', 'x*log(Abs(x))-x', var='x', label='G small ln'),
         formula('log(Abs(x))**2', 'x*log(Abs(x))**2-2*x*log(Abs(x))+2*x', var='x', label='G small ln2'),
         formula('log(x**2+a**2)', 'x*log(x**2+a**2)-2*x+2*a*atan(x/a)', var='x', branches=('x',), pos=('a',), label='G small ln quad')]
    U.add('short', '⚡ الاختصار', table(['التكامل', 'الجواب (+C)'], [frow(z) for z in r], 'formula compact')
          + box_memo(rich('$\\ln$ وحدها: $x\\ln|x|-x$. والمربع: نفس الفكرة مرتين.')))
    it = ITEMS['N51-X05']
    ex = question(it, 'U-P4 example')
    ex += short_steps(it, [
        ('القانون: سطر من جدول الاختصار (احفظه)', r'\int\ln|x|\,dx=x\ln|x|-x+C', [R('ln alone')]),
        ('من وين جا؟ ما فيه ضرب ⇐ الواحد المخفي $dv=dx$، و ln هي $u$', r'u=\ln|x|,\quad du=\frac{dx}{x},\quad dv=dx,\quad v=x',
         [('diff(log(x),x)', '1/x'), ('integrate(1,x)', 'x')]),
        ('القانون $uv-\\int v\\,du$، و $x\\cdot\\frac1x=1$', r'x\ln|x|-\int x\cdot\frac{1}{x}\,dx=x\ln|x|-\int1\,dx', [('x*(1/x)', '1')]),
        ('$\\int1\\,dx=x$، فيطلع سطر الجدول', r'x\ln|x|-x+C', [('=ANS', 'x*log(Abs(x))-x')])], 'U-P4 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('parts', 'log(Abs(x))', '1', '1/x', 'x', '$dv=dx$: الواحد المخفي', 't'),
        ('line', 'x*log(Abs(x))-Integral(1,x)', '$v\\,du=x\\cdot\\frac1x=1$'),
        ('line', 'x*log(Abs(x))-x', '$\\int1\\,dx=x$')], 'U-P4 ex')
    ex += final(it, 'U-P4 example')
    U.add('ex', 'مثال (من مذكرة د. طارق)', ex)
    U.raw(alg('poly-div', 'قسمة بسيطة: درجة البسط = درجة المقام', [
        (r'\frac{2x^{2}}{1+x^{2}}=\frac{2(1+x^{2})-2}{1+x^{2}}=2-\frac{2}{1+x^{2}}', [('2*x**2/(1+x**2)', '2-2/(1+x**2)')],
         'نكتب البسط بدلالة المقام ونطرح الفرق (تحتاجه في التمرين 2):'),
        (r'\frac{x^{2}}{1-x^{2}}=\frac{-(1-x^{2})+1}{1-x^{2}}=-1+\frac{1}{1-x^{2}}', [('x**2/(1-x**2)', '-1+1/(1-x**2)')],
         'ومثله (تحتاجه في النوع 18):')]))
    U.add('trap', '⚠️ الفخ', p(rich('$\\int\\ln|x|\\,dx\\ne\\frac1x$. هذه مشتقتها، ليست تكاملها.')))
    U.add('paper', '✍️ في ورقة الكويز', md(r'u=\ln|x|,\ dv=dx,\ du=\frac1x\,dx,\ v=x'))
    U.drill('1', 'N51-X16', 'G', 'التكامل الباقي $2\\int\\ln|x|\\,dx$ هو المثال.',
            first=r'u=(\ln|x|)^{2},\ dv=dx,\ du=\frac{2\ln|x|}{x}\,dx,\ v=x', claims=[('diff(log(x)**2,x)', '2*log(x)/x')])
    U.drill('2', 'N51-E4', 'I', '$v\\,du=\\frac{2x^2}{1+x^2}$ ثم قسمة (🧮): $2-\\frac{2}{1+x^2}$.')
    return U


# ---------------------------------------------------------------- 16
def u_definite():
    U = Unit('U-P5', 'تكامل محدد بالتجزئة', '5.1', 'من الاختبارات', 4)
    U.add('idea', 'الفكرة', p(rich('أوجد التكامل كأنه غير محدد ($F$)، ثم عوّض الحد الأعلى ناقص الحد الأدنى: $F(b)-F(a)$. لا $+C$.')))
    U.add('sign', 'العلامة', p(rich('$\\int_a^b$ بأرقام فوق وتحت، والدالة من أنواع التجزئة.')))
    U.add('short', '⚡ الاختصار', md(r'\int_{a}^{b}f(x)\,dx=F(b)-F(a)') + box_memo('أعلى ناقص أدنى، وانتبه لسالب في سالب.'))
    it = ITEMS['1445-S1-SE-Q2.3']
    ex = question(it, 'U-P5 example')
    ex += short_steps(it, [
        ('القانون: $F$ عند الحد الأعلى ناقص $F$ عند الحد الأدنى', r'\int_{a}^{b}f(x)\,dx=F(b)-F(a)', [R('definite')]),
        ('$F$ من القوس (النوع 14) مع $n=3$ و $n+1=4$', r'F(x)=\frac{x^{4}}{4}\left(\ln x-\frac14\right)',
         [('diff(x**4/4*(log(x)-Rational(1,4)),x)', 'x**3*log(x)')]),
        ('عوّض الحد الأعلى $x=e$، و $\\ln e=1$', r'F(e)=\frac{e^{4}}{4}\left(1-\frac14\right)=\frac{e^{4}}{4}\cdot\frac34=\frac{3e^{4}}{16}',
         [('E**4/4*(log(E)-Rational(1,4))', '3*E**4/16')]),
        ('عوّض الحد الأدنى $x=1$، و $\\ln1=0$', r'F(1)=\frac{1}{4}\left(0-\frac14\right)=-\frac{1}{16}',
         [('Rational(1,4)*(log(1)-Rational(1,4))', '-Rational(1,16)')]),
        ('اطرح: سالب في سالب = موجب', r'F(e)-F(1)=\frac{3e^{4}}{16}-\left(-\frac{1}{16}\right)=\frac{3e^{4}+1}{16}',
         [('3*E**4/16-(-Rational(1,16))', '(3*E**4+1)/16'), ('=ANS', '(3*E**4+1)/16')])], 'U-P5 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r'F(x)=\frac{x^{4}}{4}\left(\ln x-\frac14\right)', [('diff(x**4/4*(log(x)-Rational(1,4)),x)', 'x**3*log(x)')],
         'القوس مع $n=3$ (النوع 14)'),
        ('tex', r'F(e)=\frac{e^{4}}{4}\left(1-\frac14\right)=\frac{3e^{4}}{16}', [('E**4/4*(log(E)-Rational(1,4))', '3*E**4/16')],
         '$\\ln e=1$ (🧮)'),
        ('tex', r'F(1)=\frac14\left(0-\frac14\right)=-\frac{1}{16}', [('Rational(1,4)*(log(1)-Rational(1,4))', '-Rational(1,16)')],
         '$\\ln1=0$'),
        ('tex', r'F(e)-F(1)=\frac{3e^{4}}{16}-\left(-\frac{1}{16}\right)=\frac{3e^{4}}{16}+\frac{1}{16}',
         [('3*E**4/16-(-Rational(1,16))', '3*E**4/16+Rational(1,16)')], 'سالب في سالب = موجب')], 'U-P5 ex')
    ex += final(it, 'U-P5 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.raw(alg('ln-values', 'قيم مهمة', [
        (r'\ln e=1,\qquad \ln1=0', [('log(E)', '1'), ('log(1)', '0')], 'قيم ln:'),
        (r'e^{0}=1,\qquad e^{\ln a}=a', [('exp(0)', '1'), ('exp(log(5))', '5')], 'قيم e:')]))
    U.add('trap', '⚠️ الفخ', ul(['لا تكتب +C في المحدد.', rich('$F(b)-F(a)$ وليس العكس، وضع $F(a)$ داخل قوس قبل الطرح.')]))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر $F(x)$، ثم سطر $F(b)-F(a)$ بالأرقام، ثم الجواب.')))
    U.drill('1', 'G-05', 'G', '$F(1)=0$ و $F(0)=-1$.', first=r'F(x)=(x-1)e^{x}', claims=[('diff((x-1)*exp(x),x)', 'x*exp(x)')])
    U.drill('2', 'G-06', 'I', '$F=x\\ln x-x$ (النوع 15).')
    return U


# ---------------------------------------------------------------- 17
def u_rafeeq():
    U = Unit('U-P6', 'دالة عكسية وحدها (الرفيق)', '5.1', 'ص64–65، تمارين 8–10', 4)
    U.add('idea', 'الفكرة', p(rich('الدالة العكسية تكاملها غير معروف لكن مشتقتها معروفة. فهي $u$، و $dv=dx$ (واحد مخفي). '
                                   'يبقى تكامل $x$ × مشتقتها، وهذا تعويض بسيط.')))
    U.add('sign', 'العلامة', p(rich('$\\int\\tan^{-1}x\\,dx$ أو $\\int\\sin^{-1}x\\,dx$ أو $\\int\\cosh^{-1}x\\,dx$… الدالة وحدها.'))
          + contrast([(r'\int\cosh^{-1}x\,dx', 'تجزئة (هنا)', 'الدالة وحدها'),
                      (r'\int\frac{\cosh^{-1}x}{\sqrt{x^{2}-1}}dx', 'تعويض (النوع 9)', 'مشتقتها موجودة')]))
    short, memo = sc_rafeeq()
    U.add('short', '⚡ الاختصار', short + box_memo(memo))
    it = ITEMS['1445-S1-SE-Q2.5']
    ex = question(it, 'U-P6 example')
    ex += short_steps(it, [
        ('القانون (الرفيق): $x$ × الدالة، ناقص تكامل $x$ × مشتقتها', r"\int f(x)\,dx=x\,f(x)-\int x\,f'(x)\,dx", [R('rafeeq')]),
        ('مشتقة الدالة من صف cosh في التوائم', r"f=\cosh^{-1}x,\qquad f'=\frac{1}{\sqrt{x^{2}-1}}", [('diff(acosh(x),x)', '1/sqrt(x**2-1)', '1+t')]),
        ('عوّض في القانون؛ = السطران 1–2 في 🧱', r'x\cosh^{-1}x-\int\frac{x}{\sqrt{x^{2}-1}}\,dx',
         [('diff(x*acosh(x),x)-x/sqrt(x**2-1)', 'acosh(x)', '1+t')]),
        ('التكامل الباقي: تعويض $w=x^2-1$ (سطر في جدول الاختصار)', r'\int\frac{x\,dx}{\sqrt{x^{2}-1}}=\sqrt{x^{2}-1}',
         [('diff(sqrt(x**2-1),x)', 'x/sqrt(x**2-1)', '1+t')]),
        ('اكتب الجواب', r'x\cosh^{-1}x-\sqrt{x^{2}-1}+C', [('=ANS', 'x*acosh(x)-sqrt(x**2-1)')])], 'U-P6 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('parts', 'acosh(x)', '1', '1/sqrt(x**2-1)', 'x', 'الدالة العكسية $u$، و $dv=dx$', '1+t'),
        ('line', 'x*acosh(x)-Integral(x/sqrt(x**2-1),x)', 'القانون'),
        ('line', 'x*acosh(x)-sqrt(x**2-1)', '$\\int\\frac{x}{\\sqrt{x^2-1}}dx=\\sqrt{x^2-1}$ (من جدول الاختصار)')], 'U-P6 ex')
    ex += final(it, 'U-P6 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('مع sec⁻¹ يبقى $\\int\\frac{dx}{\\sqrt{x^2-1}}=\\cosh^{-1}x$ (ربط مع 4.2).'),
                                rich('انتبه للإشارة: $\\int\\frac{x}{\\sqrt{1-x^2}}dx=-\\sqrt{1-x^2}$ (سالب).')]))
    U.add('paper', '✍️ في ورقة الكويز', md(r'u=\cosh^{-1}x,\ dv=dx,\ du=\frac{dx}{\sqrt{x^{2}-1}},\ v=x') + p('ثم القانون والجواب.'))
    U.drill('1', '1446-S2-SE-Q2.8', 'G', '$\\int\\frac{x}{1+x^2}dx=\\frac12\\ln(1+x^2)$.',
            first=r'u=\tan^{-1}x,\ dv=dx,\ du=\frac{dx}{1+x^{2}},\ v=x', claims=[('diff(atan(x),x)', '1/(1+x**2)')])
    U.drill('2', '1447-S1-SE-Q2.5', 'P', '$\\int\\frac{x}{\\sqrt{1-x^2}}dx=-\\sqrt{1-x^2}$.')
    U.drill('3', 'N51-X09', 'I', 'مشتقة $\\sec^{-1}x$ هي $\\frac{1}{x\\sqrt{x^2-1}}$ (لـ $x>1$)، فيبقى $\\int\\frac{dx}{\\sqrt{x^2-1}}$.')
    return U


# ---------------------------------------------------------------- 18
def u_xinv():
    U = Unit('U-P7', 'x × دالة عكسية', '5.1', 'ص65، مثال 6 وتمرين 10', 4)
    U.add('idea', 'الفكرة', p(rich('مثل النوع السابق لكن $dv=x\\,dx$ فـ $v=\\frac{x^2}{2}$. التكامل الباقي غالبًا يحتاج قسمة بسيطة.')))
    U.add('sign', 'العلامة', p(rich('$\\int x\\tanh^{-1}x\\,dx$ أو $\\int x\\sec^{-1}x\\,dx$… $x$ مضروبة في دالة عكسية.')))
    U.add('short', '⚡ الاختصار', md(r'\int x\,f^{-1}(x)\,dx=\frac{x^{2}}{2}f^{-1}(x)-\frac12\int x^{2}\big(f^{-1}\big)'"'"r'(x)\,dx')
          + box_memo(rich('$\\frac{x^2}{2}$ × الدالة، ناقص نصف تكامل $x^2$ × مشتقتها.')))
    it = ITEMS['1446-S2-FE-Q2.2']
    ex = question(it, 'U-P7 example')
    ex += short_steps(it, [
        ('القانون: $\\frac{x^2}{2}$ × الدالة، ناقص نصف تكامل $x^2$ × مشتقتها', r"\int x\,f(x)\,dx=\frac{x^{2}}{2}f(x)-\frac12\int x^{2}f'(x)\,dx",
         [R('x inverse')]),
        ('مشتقة الدالة من صف tanh في التوائم', r"f=\tanh^{-1}x,\qquad f'=\frac{1}{1-x^{2}}", [('diff(atanh(x),x)', '1/(1-x**2)')]),
        ('عوّض في القانون؛ = السطران 1–2 في 🧱', r'\frac{x^{2}}{2}\tanh^{-1}x-\frac12\int\frac{x^{2}}{1-x^{2}}\,dx',
         [('diff(x**2*atanh(x)/2,x)-x**2/(2*(1-x**2))', 'x*atanh(x)')]),
        ('القسمة (🧮): اكتب البسط بدلالة المقام', r'\frac{x^{2}}{1-x^{2}}=-1+\frac{1}{1-x^{2}}', [('x**2/(1-x**2)', '-1+1/(1-x**2)')]),
        ('كامل: $\\int(-1)\\,dx=-x$ و $\\int\\frac{dx}{1-x^2}=\\tanh^{-1}x$، ثم وزّع $-\\frac12$',
         r'\frac{x^{2}}{2}\tanh^{-1}x+\frac{x}{2}-\frac12\tanh^{-1}x+C', [('=ANS', 'x**2*atanh(x)/2+x/2-atanh(x)/2')])], 'U-P7 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('parts', 'atanh(x)', 'x', '1/(1-x**2)', 'x**2/2', '$u$ الدالة العكسية، و $dv=x\\,dx$', 't/(1+t)'),
        ('line', 'x**2*atanh(x)/2-Integral(x**2/(2*(1-x**2)),x)', 'القانون'),
        ('line', 'x**2*atanh(x)/2-Integral(-Rational(1,2)+1/(2*(1-x**2)),x)', 'القسمة: $\\frac{x^2}{1-x^2}=-1+\\frac{1}{1-x^2}$ (🧮)'),
        ('line', 'x**2*atanh(x)/2+x/2-atanh(x)/2', 'نكامل: $\\int\\frac{dx}{1-x^2}=\\tanh^{-1}x$')], 'U-P7 ex')
    ex += final(it, 'U-P7 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.raw(alg('poly-div'))
    U.add('trap', '⚠️ الفخ', ul(['لا تنسَ نصف (½) قبل التكامل الباقي.',
                                rich('في مذكرة د. طارق ص65 خطأ مطبعي: $\\sqrt{1-x^2}$ بدل $\\sqrt{x^2-1}$ في مثال $x\\sec^{-1}x$؛ الجواب النهائي صحيح.')]))
    U.add('paper', '✍️ في ورقة الكويز', md(r'u=\tanh^{-1}x,\ dv=x\,dx,\ du=\frac{dx}{1-x^{2}},\ v=\frac{x^{2}}{2}'))
    U.drill('1', 'G-07', 'G', '$\\frac{x^2}{1+x^2}=1-\\frac{1}{1+x^2}$.',
            first=r'u=\tan^{-1}x,\ dv=x\,dx,\ du=\frac{dx}{1+x^{2}},\ v=\frac{x^{2}}{2}', claims=[('diff(atan(x),x)', '1/(1+x**2)')])
    U.drill('2', 'N51-X10', 'P', 'لـ $x>0$: $v\\,du=\\frac{x^2}{2}\\cdot\\frac{-1}{x\\sqrt{1+x^2}}=-\\frac{x}{2\\sqrt{1+x^2}}$.')
    U.drill('3', 'N51-E6', 'I', '$v\\,du=\\frac{x^2}{2}\\cdot\\frac{1}{x\\sqrt{x^2-1}}=\\frac{x}{2\\sqrt{x^2-1}}$.')
    return U


# ---------------------------------------------------------------- 19
def u_dawaran():
    U = Unit('U-P8', 'أسية × sin أو cos (الدوران)', '5.1', 'ص65، تمارين 11 و12', 4)
    U.add('idea', 'الفكرة', p(rich('بالتجزئة مرتين يرجع التكامل الأصلي $I$ نفسه، فنحل معادلة. الاختصار هو نتيجة هذه المعادلة جاهزة.')))
    U.add('sign', 'العلامة', p(rich('$e^{ax}$ مضروبة في $\\sin bx$ أو $\\cos bx$.')))
    short, memo = sc_dawaran()
    U.add('short', '⚡ الاختصار', short + box_memo(memo))
    it = ITEMS['1447-S2-FE-Q2.3']
    ex = question(it, 'U-P8 example')
    ex += short_steps(it, [
        ('القانون: صف sin في جدول الدوران', r'\int e^{ax}\sin bx\,dx=\frac{e^{ax}}{a^{2}+b^{2}}\left(a\sin bx-b\cos bx\right)+C',
         [R('dawaran sin')]),
        ('طلّع الأرقام: $a$ معامل $x$ في الأسية، و $b$ معامل $x$ في sin، ثم المقام', r'a=2,\qquad b=1,\qquad a^{2}+b^{2}=4+1=5',
         [('2**2+1**2', '5')]),
        ('عوّض في القانون', r'\frac{e^{2x}}{5}\left(2\sin x-1\cdot\cos x\right)+C', [('=ANS', 'exp(2*x)*(2*sin(x)-1*cos(x))/5')]),
        ('بسّط $1\\cdot\\cos x=\\cos x$؛ = جواب 🧱 بعد التجزئة مرتين', r'=\frac{e^{2x}}{5}\left(2\sin x-\cos x\right)+C',
         [('=ANS', 'exp(2*x)*(2*sin(x)-cos(x))/5')])], 'U-P8 ex')
    I_ = '(2*exp(2*x)*sin(x)/5-exp(2*x)*cos(x)/5)'
    ex += p('<b>🧱 خطوة خطوة (التجزئة مرتين):</b>') + steps(it, [
        ('parts', 'sin(x)', 'exp(2*x)', 'cos(x)', 'exp(2*x)/2', 'أول تجزئة: $u=\\sin x$'),
        ('line', 'exp(2*x)*sin(x)/2-Integral(exp(2*x)*cos(x)/2,x)', 'القانون'),
        ('parts', 'cos(x)', 'exp(2*x)', '-sin(x)', 'exp(2*x)/2', 'ثاني تجزئة بنفس الاختيار (المثلثية $u$)'),
        ('tex', r'I=\frac{e^{2x}\sin x}{2}-\frac{e^{2x}\cos x}{4}-\frac14I',
         [('exp(2*x)*sin(x)/2-exp(2*x)*cos(x)/4-%s/4' % I_, I_)], 'رجع التكامل الأصلي $I$ (السطر يتحقق مع الجواب)'),
        ('tex', r'\frac54I=\frac{e^{2x}\sin x}{2}-\frac{e^{2x}\cos x}{4}', [('Rational(5,4)*%s' % I_, 'exp(2*x)*sin(x)/2-exp(2*x)*cos(x)/4')],
         'ننقل $\\frac14I$ للطرف الأول (🧮)'),
        ('tex', r'I=\frac45\left(\frac{e^{2x}\sin x}{2}-\frac{e^{2x}\cos x}{4}\right)', [('Rational(4,5)*(exp(2*x)*sin(x)/2-exp(2*x)*cos(x)/4)', I_)],
         'نضرب في $\\frac45$')], 'U-P8 ex')
    ex += final(it, 'U-P8 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.raw(alg('cyclic-eq', 'حل معادلة فيها التكامل نفسه', [
        (r'I=A-\frac14I\ \Rightarrow\ I+\frac14I=A', [], 'نجمع $I$ في طرف واحد (نضيف $\\frac14I$ للطرفين):'),
        (r'I+\frac14I=\frac44I+\frac14I=\frac54I', [('1+Rational(1,4)', 'Rational(5,4)')], 'نجمع الكسور:'),
        (r'\frac54I=A\ \Rightarrow\ I=\frac45A', [('Rational(5,4)*Rational(4,5)', '1')], 'نقسم على $\\frac54$ = نضرب في $\\frac45$:')]))
    U.add('trap', '⚠️ الفخ', ul(['في التجزئة الثانية لازم تختار نفس النوع لـ u (المثلثية)، وإلا ترجع للبداية.',
                                rich('لا تخلط مع $e^{ax}\\sinh bx$: هذا النوع 20.')]))
    U.add('paper', '✍️ في ورقة الكويز', p('إذا الوقت ضيق: سطر الصيغة بالأرقام ثم الجواب. وإذا تبي خطوات كاملة: التجزئتان ثم سطر المعادلة.'))
    U.drill('1', 'N51-E7', 'G', 'صف cos: $a\\cos+b\\sin$.', first=r'a=1,\quad b=1,\quad a^{2}+b^{2}=2', claims=[('1**2+1**2', '2')])
    U.drill('2', 'N51-X11', 'P', '$a=2$، $b=3$، والمقام $13$.')
    U.drill('3', 'N51-X12', 'I', '$a=5$، $b=2$، والمقام $29$.')
    return U


# ---------------------------------------------------------------- 20
def u_nisfayn():
    U = Unit('U-P9', 'أسية × sinh أو cosh (النصفين)', '5.1', 'ص66، تمرينا 13 و14', 5)
    U.add('idea', 'الفكرة', p(rich('sinh و cosh أصلًا أسيات (تعريف 4.1). نكتبها بالتعريف، نضرب، فيصير مجموع أسيات سهل التكامل.')))
    U.add('sign', 'العلامة', p(rich('$e^{ax}$ مضروبة في $\\sinh bx$ أو $\\cosh bx$.')))
    short, memo = sc_nisfayn()
    U.add('short', '⚡ الاختصار', short + box_memo(memo))
    it = ITEMS['1446-S1-SE-Q2.3']
    ex = question(it, 'U-P9 example')
    ex += short_steps(it, [
        ('القانون: صف cosh في جدول النصفين (بشرط $a\\ne\\pm b$)',
         r'\int e^{ax}\cosh bx\,dx=\frac12\left(\frac{e^{(a+b)x}}{a+b}+\frac{e^{(a-b)x}}{a-b}\right)+C', [R('nisfayn cosh')]),
        ('طلّع الأرقام، واحسب المجموع والفرق', r'a=1,\quad b=2:\qquad a+b=3,\qquad a-b=-1', [('1+2', '3'), ('1-2', '-1')]),
        ('عوّض في القانون (مع cosh بين الحدين $+$)', r'\frac12\left(\frac{e^{3x}}{3}+\frac{e^{-x}}{-1}\right)', [('=ANS', '(exp(3*x)/3+exp(-x)/(-1))/2')]),
        ('وزّع $\\frac12$: $\\frac12\\cdot\\frac13=\\frac16$، و $\\frac{1}{-1}=-1$؛ = جواب 🧱', r'=\frac{e^{3x}}{6}-\frac{e^{-x}}{2}+C',
         [('(exp(3*x)/3+exp(-x)/(-1))/2', 'exp(3*x)/6-exp(-x)/2'), ('=ANS', 'exp(3*x)/6-exp(-x)/2')])], 'U-P9 ex')
    ex += p('<b>🧱 خطوة خطوة (بالتعريف):</b>') + steps(it, [
        ('tex', r'\cosh2x=\frac{e^{2x}+e^{-2x}}{2}', [('cosh(2*x)', '(exp(2*x)+exp(-2*x))/2')], 'تعريف cosh (4.1)'),
        ('tex', r'e^{x}\cosh2x=\frac{e^{3x}+e^{-x}}{2}', [('exp(x)*cosh(2*x)', '(exp(3*x)+exp(-x))/2')], 'نضرب ونجمع الأسس (🧮)'),
        ('line', 'exp(3*x)/6-exp(-x)/2', 'نكامل كل حد: $\\int e^{kx}dx=\\frac{e^{kx}}{k}$')], 'U-P9 ex')
    ex += final(it, 'U-P9 example')
    U.add('ex', 'مثال (اختبار سابق)', ex)
    U.raw(alg('exp-mult', 'ضرب الأسيات وتعريف sinh و cosh', [
        (r'e^{x}\cdot e^{2x}=e^{x+2x}=e^{3x}', [('exp(x)*exp(2*x)', 'exp(3*x)')], 'نجمع الأسس:'),
        (r'e^{x}\cdot e^{-2x}=e^{x-2x}=e^{-x}', [('exp(x)*exp(-2*x)', 'exp(-x)')], 'ومع أس سالب:'),
        (r'\cosh u=\frac{e^{u}+e^{-u}}{2},\qquad \sinh u=\frac{e^{u}-e^{-u}}{2}', [('cosh(x)', '(exp(x)+exp(-x))/2'), ('sinh(x)', '(exp(x)-exp(-x))/2')],
         'التعريف من 4.1:')]))
    U.add('trap', '⚠️ الفخ', ul([rich('إذا $a=b$ أو $a=-b$ يصير أحد الأسين صفرًا: حدّه ثابت ($\\frac12$ أو $-\\frac12$) وتكامله $\\pm\\frac{x}{2}$ (التمرين 3).'),
                                rich('مع sinh بين الحدين سالب.')]))
    U.add('paper', '✍️ في ورقة الكويز', p('سطر التعريف، ثم سطر الضرب، ثم الجواب. هكذا حلّ المفتاح الرسمي.'))
    U.drill('1', 'N51-X13', 'G', 'sinh ⇐ بين الحدين سالب.', first=r'a=3,\ b=1:\quad \frac12\left[\frac{e^{4x}}{4}-\frac{e^{2x}}{2}\right]',
            claims=[('(exp(4*x)/4-exp(2*x)/2)/2', 'exp(4*x)/8-exp(2*x)/4')])
    U.drill('2', 'N51-X14', 'P', '$a=1$، $b=5$: الأسان $6x$ و $-4x$.')
    U.drill('3', '1445-S1-SE-Q2.1', 'I', '$a=-1$، $b=1$: أحد الأسين صفر.')
    return U


# ---------------------------------------------------------------- 21
def u_subparts():
    U = Unit('U-P10', 'تعويض أولًا: جذر داخل الدالة، وقوة × جذر', '5.1', 'ص66، تمارين 15 و17 و18', 5)
    U.add('idea', 'الفكرة', p(rich('بعض الأسئلة تحتاج تعويضًا قبل أي شيء: $e^{\\sqrt x}$ نتخلص من الجذر بـ $t=\\sqrt x$ فيصير تجزئة عادية. '
                                   'و $x^3\\sqrt{x^2+c}$ تنحل بتعويض $w=x^2+c$ فقط.')))
    U.add('sign', 'العلامة', p(rich('$e^{\\sqrt x}$ أو $\\cos\\sqrt x$؛ أو قوة فردية لـ $x$ × جذر فيه $x^2$ (أو $x^4$).')))
    r = [formula('exp(sqrt(x))', '2*exp(sqrt(x))*(sqrt(x)-1)', var='x', branches=('t',), label='G small e sqrt'),
         formula('x**3*sqrt(x**2+c)', '(x**2+c)**Rational(5,2)/5-c*(x**2+c)**Rational(3,2)/3', var='x', branches=('t',), real=('c',), label='G small root')]
    U.add('short', '⚡ الاختصار', table(['التكامل', 'الجواب (+C)'], [frow(z) for z in r], 'formula compact')
          + box_memo(rich('الجذر داخل الدالة ⇐ $t=\\sqrt x$. قوة × جذر ⇐ $w$ = ما تحت الجذر.')))
    it = ITEMS['N51-X15']
    ex = question(it, 'U-P10 example')
    ex += short_steps(it, [
        ('القانون: سطر من جدول الاختصار (مذكرة د. طارق، تمرين 15)', r'\int e^{\sqrt{x}}dx=2e^{\sqrt{x}}\left(\sqrt{x}-1\right)+C',
         [R('small e sqrt')]),
        ('من وين جا؟ الجذر داخل الدالة ⇐ $t=\\sqrt x$، فـ $x=t^2$ و $dx=2t\\,dt$', r'\int e^{\sqrt{x}}dx=\int2t\,e^{t}\,dt',
         [('exp(sqrt(x))', '2*sqrt(x)*exp(sqrt(x))*diff(sqrt(x),x)')]),
        ('النوع 12 مع $p=2$ (من $2t$)، و $G_1=G_2=e^t$', r'2t\,e^{t}-2e^{t}=2(t-1)e^{t}', [('diff(2*(x-1)*exp(x),x)', '2*x*exp(x)')]),
        ('ارجع $t=\\sqrt x$؛ فيطلع سطر الجدول', r'2e^{\sqrt{x}}\left(\sqrt{x}-1\right)+C', [('=ANS', '2*exp(sqrt(x))*(sqrt(x)-1)')])], 'U-P10 ex')
    ex += p('<b>🧱 خطوة خطوة:</b>') + steps(it, [
        ('tex', r't=\sqrt{x},\quad x=t^{2},\quad dx=2t\,dt', [('diff(x**2,x)', '2*x')], 'نتخلص من الجذر'),
        ('tex', r'\int e^{\sqrt x}dx=\int2t\,e^{t}\,dt', [('exp(sqrt(x))', '2*sqrt(x)*exp(sqrt(x))*diff(sqrt(x),x)')], 'التكامل بدلالة $t$'),
        ('tex', r'=2\left(t\,e^{t}-e^{t}\right)=2(t-1)e^{t}', [('diff(2*(x-1)*exp(x),x)', '2*x*exp(x)')], 'النوع 12 مع $p=2$: $G_1=G_2=e^t$'),
        ('line', '2*exp(sqrt(x))*(sqrt(x)-1)', 'نرجع $t=\\sqrt x$')], 'U-P10 ex')
    ex += final(it, 'U-P10 example')
    U.add('ex', 'مثال (من مذكرة د. طارق)', ex)
    U.add('trap', '⚠️ الفخ', ul([rich('لا تنسَ $dx=2t\\,dt$؛ هي اللي تعطي حد $t$ للتجزئة.'),
                                rich('$x^3dx=x^2\\cdot x\\,dx$: نكتب $x^2=w-c$ و $x\\,dx=\\frac{dw}{2}$.')]))
    U.add('paper', '✍️ في ورقة الكويز', p(rich('سطر التعويض ($t$ و $dx$)، ثم التجزئة، ثم الرجوع لـ $x$.')))
    U.drill('1', 'G-08', 'G', '$p=2$ (من $2t$)، $G_1=\\sin t$، $G_2=-\\cos t$.',
            first=r't=\sqrt{x},\ dx=2t\,dt:\quad\int\cos\sqrt{x}\,dx=\int2t\cos t\,dt',
            claims=[('cos(sqrt(x))', '2*sqrt(x)*cos(sqrt(x))*diff(sqrt(x),x)')])
    U.drill('2', 'N51-X17', 'P', '$w=x^2-1$، $x^2=w+1$، $x\\,dx=\\frac{dw}{2}$.')
    U.drill('3', 'N51-X18', 'I', '$w=x^4+2$، $x^4=w-2$، $x^3dx=\\frac{dw}{4}$.')
    return U


UNITS_51 = [u_parts_linear, u_parts_di, u_qaws, u_ln_alone, u_definite, u_rafeeq, u_xinv, u_dawaran, u_nisfayn, u_subparts]

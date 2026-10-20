"""المذكرة الكاملة — صفحات «📚 من الدروس السابقة»: ما تحتاجه أسئلة 4.2 و5.1 و5.2 من الدروس التي قبلها.

Five short pages, each placed just before the first type that needs it (guide_end.BEFORE_UNIT):
ق1 hyperbolic functions (4.1), ق2 derivative rules, ق3 basic integrals and substitution (2.3, 2.4, 3.1, 3.2),
ق4 inverse trigonometric functions (3.4), ق5 trigonometric identities. Every rule, example row and try-it answer
is checked while building, like the rest of the guide.
"""
from booklet_engine import arith, formula
from guide_kit import alg, pgref, rich, steps_table
from html_kit import box, chip, link, md, mi, p, table, ul

TITLES = {'pq1': 'ق1: الدوال الزائدية (درس 4.1)', 'pq2': 'ق2: قواعد الاشتقاق وقاعدة السلسلة',
          'pq3': 'ق3: التكامل الأساسي والتعويض بـ u', 'pq4': 'ق4: الدوال المثلثية العكسية (درس 3.4)',
          'pq5': 'ق5: متطابقات المثلثات'}
SHORT = {'pq1': 'ق1', 'pq2': 'ق2', 'pq3': 'ق3', 'pq4': 'ق4', 'pq5': 'ق5'}
SOURCE = {'pq1': 'مذكرة د. طارق: درس 4.1، ص49–56', 'pq2': 'التفاضل، ومذكرة د. طارق: دروس 3.1–3.3، ص27–42',
          'pq3': 'مذكرة د. طارق: دروس 2.3 و2.4 (ص20–26) و3.1 و3.2 (ص27–37)', 'pq4': 'مذكرة د. طارق: درس 3.4، ص43–48',
          'pq5': 'من مقررات قبل ريض 111؛ مذكرة د. طارق تستعملها في 5.2 (ص67)'}
MINUTES = {'pq1': 10, 'pq2': 10, 'pq3': 15, 'pq4': 10, 'pq5': 10}
HTML = {}     # anchor -> finished section (built in document order, see build())
KEYS = []     # (anchor, [answer latex, ...]) for the keys section
SHEET = {}    # anchor -> compact tables for the formula sheet


def _row(z, cond=None):
    return [mi(r'\displaystyle ' + z[0]), mi(r'\displaystyle ' + z[1])] + ([cond] if cond is not None else [])


def _cells(rows, label):
    """Example rows (latex, claims, why): every claim checked; the last row is the answer."""
    return [(arith(latex, claims, '%s step %d' % (label, k)), why, k == len(rows))
            for k, (latex, claims, why) in enumerate(rows, 1)]


def _example(title, q_latex, rows, label, check=None):
    out = p('<b>%s</b>' % title) + md(q_latex) + steps_table(_cells(rows, label))
    if check:
        out += p('<b>✔ تأكد:</b> ' + rich(check), 'small')
    return out


def _try(anchor, items):
    """Two try-it questions; the answers are checked and printed in the keys section."""
    answers = [arith(ans, claims, '%s try %d' % (anchor, k)) for k, (_, ans, claims) in enumerate(items, 1)]
    KEYS.append((anchor, answers))
    qs = ' '.join('(%d) %s' % (k, rich(q)) for k, (q, _, _) in enumerate(items, 1))
    return p('✏️ <b>جرّب:</b> ' + qs + ' — ' + link('k-' + anchor, 'الأجوبة ص ' + pgref('k-' + anchor)), 'try')


def _uses(units):
    return '، '.join(link(uid, 'النوع %s' % num) for uid, num in units)


def _section(anchor, why, body):
    head = ('<div class="pq-head">%s%s</div>' % (chip('📚 من الدروس السابقة', 'pq'), chip(SOURCE[anchor], 'src')))
    return ('<section class="chapter flow prereq" id="%s"><h2>📚 %s</h2>%s' % (anchor, TITLES[anchor], head)
            + box('note', 'ليش تحتاجه هنا', why) + body + '</section>')


# ---------------------------------------------------------------- ق1
def pq1():
    defs = [(r'\sinh x=\frac{e^{x}-e^{-x}}{2}', ('sinh(x)', '(exp(x)-exp(-x))/2')),
            (r'\cosh x=\frac{e^{x}+e^{-x}}{2}', ('cosh(x)', '(exp(x)+exp(-x))/2')),
            (r'\tanh x=\frac{\sinh x}{\cosh x}', ('tanh(x)', 'sinh(x)/cosh(x)')),
            (r'\coth x=\frac{\cosh x}{\sinh x}', ('coth(x)', 'cosh(x)/sinh(x)')),
            (r'\operatorname{sech}x=\frac{1}{\cosh x}', ('sech(x)', '1/cosh(x)')),
            (r'\operatorname{csch}x=\frac{1}{\sinh x}', ('csch(x)', '1/sinh(x)'))]
    def_rows = [[mi(r'\displaystyle ' + arith(lt, [c], 'pq1 definition'))] for lt, c in defs]
    ids = arith(r'\cosh^{2}x-\sinh^{2}x=1,\qquad 1-\tanh^{2}x=\operatorname{sech}^{2}x,\qquad \coth^{2}x-1=\operatorname{csch}^{2}x',
                [('cosh(x)**2-sinh(x)**2', '1'), ('1-tanh(x)**2', 'sech(x)**2'), ('coth(x)**2-1', 'csch(x)**2')], 'pq1 identities')
    vals = arith(r'\sinh0=0,\qquad \cosh0=1,\qquad \cosh x\ge1', [('sinh(0)', '0'), ('cosh(0)', '1')], 'pq1 values')
    d = [formula('sinh(u)', 'cosh(u)', 'diff', branches=('x',), uprime=True, label='pq1 d sinh'),
         formula('cosh(u)', 'sinh(u)', 'diff', branches=('x',), uprime=True, label='pq1 d cosh'),
         formula('tanh(u)', 'sech(u)**2', 'diff', branches=('x',), uprime=True, label='pq1 d tanh'),
         formula('coth(u)', '-csch(u)**2', 'diff', branches=('t',), uprime=True, label='pq1 d coth'),
         formula('sech(u)', '-sech(u)*tanh(u)', 'diff', branches=('x',), uprime=True, label='pq1 d sech'),
         formula('csch(u)', '-csch(u)*coth(u)', 'diff', branches=('t',), uprime=True, label='pq1 d csch')]
    i = [formula('sinh(u)', 'cosh(u)', label='pq1 int sinh'), formula('cosh(u)', 'sinh(u)', label='pq1 int cosh'),
         formula('sech(u)**2', 'tanh(u)', label='pq1 int sech2'), formula('sech(u)*tanh(u)', '-sech(u)', label='pq1 int sech tanh')]
    why = p(rich('الكويز على 4.2 و5.1 و5.2، لكن أسئلته مليانة بالدوال الزائدية <b>العادية</b> من 4.1:')) + ul([
        rich('سؤال المشتقة (النوعان 1 و2) يجمع دالة عادية مثل $\\cosh(3x^2)$ مع دالة عكسية.'),
        rich('في النوع 4 نحتاج $\\cosh x\\ge1$، وفي النوعين 12 و13 نكامل $\\sinh$ و $\\cosh$.'),
        rich('في النوع 20 نكتب $\\sinh$ و $\\cosh$ بالأسيات (التعريف تحت).')])
    body = box('short', 'التعريف: كلها من eˣ و e⁻ˣ', table(['الدالة'], def_rows, 'formula compact')
               + p(rich('يعني $\\cosh$ «نصف المجموع» و $\\sinh$ «نصف الفرق»، والباقي قسمة مثل المثلثات.'), 'small'))
    body += box('short', 'المتطابقات والقيم', md(ids) + md(vals)
                + p(rich('$\\cosh x$ أصغر قيمة له 1 (عند $x=0$)، فهو ما يصير صفرًا ولا سالبًا أبدًا.'), 'small'))
    body += box('short', 'المشتقات (u′ = مشتقة ما داخل الدالة)', table(['المشتقة', 'تساوي'], [_row(z) for z in d], 'formula compact')
                + p(rich('الإشارة السالبة مع coth و sech و csch فقط. و $(\\cosh u)\'=+\\sinh u\\cdot u\'$ بدون سالب، عكس cos.'), 'small'))
    body += box('short', 'التكاملات', table(['التكامل', 'الجواب (+C)'], [_row(z) for z in i], 'formula compact'))
    ex = _example('مثال 1: أوجد مشتقة', r'y=\cosh\left(4x^{2}\right)', [
        (r"u=4x^{2},\qquad u'=8x", [('diff(4*x**2,x)', '8*x')], 'نسمّي ما داخل الدالة $u$، ونشتقه'),
        (r"\left(\cosh u\right)'=\sinh u\cdot u'", [('diff(cosh(4*x**2),x)', 'sinh(4*x**2)*diff(4*x**2,x)')], 'من جدول المشتقات: cosh يصير sinh بدون سالب'),
        (r"y'=\sinh\left(4x^{2}\right)\cdot8x=8x\sinh\left(4x^{2}\right)", [('diff(cosh(4*x**2),x)', '8*x*sinh(4*x**2)')],
         "نعوّض $u$ و $u'$، ونقدّم الرقم")], 'pq1 ex1')
    ex += _example('مثال 2: اكتب بالأسيات (تحتاجه في النوع 20)', r'e^{x}\sinh x', [
        (r'\sinh x=\frac{e^{x}-e^{-x}}{2}', [('sinh(x)', '(exp(x)-exp(-x))/2')], 'التعريف'),
        (r'e^{x}\sinh x=\frac{e^{x}\cdot e^{x}-e^{x}\cdot e^{-x}}{2}', [('exp(x)*sinh(x)', '(exp(x)*exp(x)-exp(x)*exp(-x))/2')], 'نضرب $e^x$ في كل حد'),
        (r'=\frac{e^{2x}-1}{2}', [('exp(x)*sinh(x)', '(exp(2*x)-1)/2')], 'الأسس تنجمع: $x+x=2x$ و $x-x=0$، و $e^0=1$')], 'pq1 ex2')
    body += box('ex', 'أمثلة محلولة', ex)
    body += box('trap', '⚠️ الفخ', ul([rich('$\\cosh^2x-\\sinh^2x=1$ بإشارة <b>سالب</b>، عكس $\\cos^2x+\\sin^2x=1$.'),
                                       rich('$\\frac{d}{dx}\\cosh x=+\\sinh x$ (بدون سالب)، و $\\int\\sinh x\\,dx=+\\cosh x$.'),
                                       rich('$\\sinh^{-1}x$ (العكسية، درس 4.2) ليست $\\frac{1}{\\sinh x}$؛ هذي $\\operatorname{csch}x$.')]))
    body += _try('pq1', [('أوجد $\\frac{d}{dx}\\sinh(5x)$.', r"5\cosh5x", [('diff(sinh(5*x),x)', '5*cosh(5*x)')]),
                         ('اكتب $\\cosh2x$ بالأسيات.', r'\cosh2x=\frac{e^{2x}+e^{-2x}}{2}', [('cosh(2*x)', '(exp(2*x)+exp(-2*x))/2')])])
    SHEET['pq1'] = (table(['المشتقة', 'تساوي'], [_row(z) for z in d], 'formula compact') + md(ids))
    return _section('pq1', why, body)


# ---------------------------------------------------------------- ق2
def pq2():
    r = [formula('u**n', 'n*u**(n-1)', 'diff', branches=('t',), real=('n',), uprime=True, label='pq2 power'),
         formula('sqrt(u)', '1/(2*sqrt(u))', 'diff', branches=('t',), uprime=True, label='pq2 sqrt'),
         formula('exp(u)', 'exp(u)', 'diff', branches=('x',), uprime=True, label='pq2 exp'),
         formula('a**u', 'a**u*log(a)', 'diff', branches=('x',), pos=('a',), uprime=True, label='pq2 a^u'),
         formula('log(Abs(u))', '1/u', 'diff', branches=('t', '-t'), uprime=True, label='pq2 ln'),
         formula('sin(u)', 'cos(u)', 'diff', branches=('x',), uprime=True, label='pq2 sin'),
         formula('cos(u)', '-sin(u)', 'diff', branches=('x',), uprime=True, label='pq2 cos'),
         formula('tan(u)', 'sec(u)**2', 'diff', branches=('t/(1+t)',), uprime=True, label='pq2 tan'),
         formula('sec(u)', 'sec(u)*tan(u)', 'diff', branches=('t/(1+t)',), uprime=True, label='pq2 sec'),
         formula('cot(u)', '-csc(u)**2', 'diff', branches=('t/(1+t)',), uprime=True, label='pq2 cot'),
         formula('csc(u)', '-csc(u)*cot(u)', 'diff', branches=('t/(1+t)',), uprime=True, label='pq2 csc')]
    why = p(rich('السؤال الأول في الكويز غالبًا «Find dy/dx»: دالة عكسية (4.2) داخل قاعدة ثانية. وكل سطر «✔ تأكد» في المذكرة '
                 'يطلب منك تشتق جوابك. فلازم القواعد هذي تكون جاهزة.'))
    chain = box('short', 'قاعدة السلسلة (أهم قاعدة)', p(rich('إذا الدالة فيها شيء غير $x$ داخلها، نسمّيه $u$:'))
                + ul([rich('<b>1.</b> اشتق الدالة الخارجية واترك $u$ كما هو.'), rich("<b>2.</b> اضرب في $u'$ (مشتقة الداخل).")])
                + p(rich("لهذا كل صف في الجدول تحت فيه $u'$. إذا الداخل $x$ وحده فـ $u'=1$ ولا يتغير شيء.")))
    rules = box('short', 'جدول المشتقات', table(['المشتقة', 'تساوي'], [_row(z) for z in r], 'formula compact')
                + md(r"(f\,g)'=f'\,g+f\,g',\qquad \left(\frac{f}{g}\right)'=\frac{f'\,g-f\,g'}{g^{2}}")
                + p(rich('مع sin الأشياء موجبة، ومع cos و cot و csc سالبة (كل دالة تبدأ بـ «co» مشتقتها سالبة).'), 'small'))
    ex = _example('مثال 1', r'y=\ln\left|\cos3x\right|', [
        (r'u=\cos3x', [('cos(3*x)', 'cos(3*x)')], 'الخارج ln، والداخل $u$'),
        (r"u'=-\sin3x\cdot3=-3\sin3x", [('diff(cos(3*x),x)', '-3*sin(3*x)')], 'cos يصير −sin، ونضرب في مشتقة $3x$ (وهي 3): سلسلة داخل سلسلة'),
        (r"y'=\frac{u'}{u}=\frac{-3\sin3x}{\cos3x}", [('diff(log(cos(3*x)),x)', '-3*sin(3*x)/cos(3*x)')], "صف ln: $\\frac{u'}{u}$"),
        (r"y'=-3\tan3x", [('-3*sin(3*x)/cos(3*x)', '-3*tan(3*x)')], '$\\frac{\\sin}{\\cos}=\\tan$')], 'pq2 ex1')
    ex += _example('مثال 2', r'y=2^{x^{2}}', [
        (r"u=x^{2},\qquad u'=2x", [('diff(x**2,x)', '2*x')], 'الأس كله $u$'),
        (r"y'=2^{u}\cdot\ln2\cdot u'=2^{x^{2}}\cdot\ln2\cdot2x", [('diff(2**(x**2),x)', '2**(x**2)*log(2)*2*x')],
         'صف $a^u$: نفسها × $\\ln a$ × $u\'$')], 'pq2 ex2')
    body = chain + rules + box('ex', 'أمثلة محلولة', ex)
    body += box('trap', '⚠️ الفخ', ul([rich("أكثر غلطة في الكويز: نسيان $u'$."),
                                       rich("$(\\ln|u|)'=\\frac{u'}{u}$، وليست $\\frac{1}{u}$ فقط."),
                                       rich('$(\\cos x)\'=-\\sin x$ بالسالب، لكن $(\\cosh x)\'=+\\sinh x$.')]))
    body += _try('pq2', [('أوجد $\\frac{d}{dx}e^{\\sin x}$.', r"\cos x\,e^{\sin x}", [('diff(exp(sin(x)),x)', 'cos(x)*exp(sin(x))')]),
                         ('أوجد $\\frac{d}{dx}\\sqrt{x^{2}+1}$.', r"\frac{x}{\sqrt{x^{2}+1}}", [('diff(sqrt(x**2+1),x)', 'x/sqrt(x**2+1)')])])
    return _section('pq2', why, body)


# ---------------------------------------------------------------- ق3
def pq3():
    t = [formula('x**n', 'x**(n+1)/(n+1)', var='x', branches=('t',), real=('n',), label='pq3 power'),
         formula('1/x', 'log(Abs(x))', var='x', branches=('t', '-t'), label='pq3 1/x'),
         formula('exp(k*x)', 'exp(k*x)/k', var='x', branches=('x',), pos=('k',), label='pq3 e'),
         formula('sin(k*x)', '-cos(k*x)/k', var='x', branches=('x',), pos=('k',), label='pq3 sin'),
         formula('cos(k*x)', 'sin(k*x)/k', var='x', branches=('x',), pos=('k',), label='pq3 cos'),
         formula('sinh(k*x)', 'cosh(k*x)/k', var='x', branches=('x',), pos=('k',), label='pq3 sinh'),
         formula('cosh(k*x)', 'sinh(k*x)/k', var='x', branches=('x',), pos=('k',), label='pq3 cosh'),
         formula('sec(x)**2', 'tan(x)', var='x', branches=('t/(1+t)',), label='pq3 sec2'),
         formula('csc(x)**2', '-cot(x)', var='x', branches=('t/(1+t)',), label='pq3 csc2'),
         formula('sec(x)*tan(x)', 'sec(x)', var='x', branches=('t/(1+t)',), label='pq3 sec tan'),
         formula('tan(x)', 'log(Abs(sec(x)))', var='x', branches=('t/(1+t)',), label='pq3 tan'),
         formula('sec(x)', 'log(Abs(sec(x)+tan(x)))', var='x', branches=('t/(1+t)',), label='pq3 sec')]
    why = p(rich('كل جداول 4.2 مكتوبة بـ $u$ و $du$، وكل أنواع 5.2 تبدأ بتعويض، والتجزئة في 5.1 تنتهي بتكامل من الجدول هذا. '
                 'التعويض هو <b>الطريقة العادية</b> نفسها، مو اختصار.'))
    basic = box('short', 'جدول التكاملات الأساسية', table(['التكامل', 'الجواب (+C)'], [_row(z) for z in t], 'formula compact')
                + p(rich('الشرط مع $x^n$: $n\\ne-1$ (لأن $n=-1$ هو $\\int\\frac1x dx=\\ln|x|$). والرقم المضروب يطلع برّا: '
                         '$\\int c\\,f\\,dx=c\\int f\\,dx$، والجمع يتوزع.'), 'small'))
    steps5 = box('short', 'التعويض بـ u: خمس خطوات ثابتة', '<ol class="method">' + ''.join('<li>%s</li>' % rich(s) for s in [
        '<b>اختر $u$</b>: الجزء اللي <b>مشتقته موجودة جنبه</b> (أو الشيء اللي داخل دالة أو تحت جذر أو قوة).',
        '<b>اشتق</b>: اكتب $du=(\\ldots)\\,dx$، وطلّع منه اللي موجود في السؤال (مثل $x\\,dx=\\frac{du}{2}$).',
        '<b>عوّض</b>: اكتب التكامل كله بدلالة $u$. لازم <b>كل</b> $x$ تختفي.',
        '<b>كامل</b> بالجدول.',
        '<b>ارجع</b> لـ $x$، وزد $+C$.']) + '</ol>')
    picks = [(r'\int\cos3x\,dx', 'u=3x', 'du=3\\,dx', r'\frac13\sin3x', ('diff(sin(3*x)/3,x)', 'cos(3*x)'), 'داخل الدالة'),
             (r'\int x\left(x^{2}+1\right)^{5}dx', 'u=x^{2}+1', 'du=2x\\,dx', r'\frac{\left(x^{2}+1\right)^{6}}{12}',
              ('diff((x**2+1)**6/12,x)', 'x*(x**2+1)**5'), 'تحت القوة، ومشتقته $2x$ موجودة'),
             (r'\int\cos x\left(1+\sin x\right)^{3}dx', 'u=1+\\sin x', 'du=\\cos x\\,dx', r'\frac{\left(1+\sin x\right)^{4}}{4}',
              ('diff((1+sin(x))**4/4,x)', 'cos(x)*(1+sin(x))**3'), 'مشتقته $\\cos x$ موجودة'),
             (r'\int\frac{e^{x}}{1+e^{x}}dx', 'u=1+e^{x}', 'du=e^{x}dx', r'\ln\left(1+e^{x}\right)',
              ('diff(log(1+exp(x)),x)', 'exp(x)/(1+exp(x))'), 'المقام، ومشتقته في البسط'),
             (r'\int\frac{\ln x}{x}dx', 'u=\\ln x', 'du=\\frac{dx}{x}', r'\frac{\left(\ln x\right)^{2}}{2}',
              ('diff(log(x)**2/2,x)', 'log(x)/x'), '$\\frac1x$ هي مشتقته')]
    pick_rows = [[mi(r'\displaystyle ' + q), mi(u), mi(r'\displaystyle ' + du), mi(r'\displaystyle ' + arith(a, [c], 'pq3 pick')), rich(w)]
                 for q, u, du, a, c, w in picks]
    choose = box('short', 'كيف أختار u؟', table(['السؤال', 'u', 'du', 'الجواب (+C)', 'ليش هذا u'], pick_rows, 'formula compact pick')
                 + p(rich('وفي 4.2 نفس الشي: $\\int\\frac{dx}{\\sqrt{4x^2+25}}$ فيه $u=2x$، و $\\int\\frac{x\\,dx}{\\sqrt{16-x^4}}$ فيه $u=x^2$.'), 'small'))
    ex = _example('مثال 1: البسط جزء من du', r'\int x\left(x^{2}+1\right)^{5}dx', [
        (r'u=x^{2}+1', [('x**2+1', 'x**2+1')], '<b>اختر</b>: تحت القوة، ومشتقته $2x$ وعندنا $x$'),
        (r'du=2x\,dx\ \Rightarrow\ x\,dx=\frac{du}{2}', [('diff(x**2+1,x)/2', 'x')], '<b>اشتق</b>، ونقسم على 2 لأن السؤال فيه $x\\,dx$ بس'),
        (r'\int x\left(x^{2}+1\right)^{5}dx=\int u^{5}\cdot\frac{du}{2}=\frac12\int u^{5}\,du',
         [('x*(x**2+1)**5', 'Rational(1,2)*(x**2+1)**5*diff(x**2+1,x)')], '<b>عوّض</b>: ما بقي ولا $x$'),
        (r'=\frac12\cdot\frac{u^{6}}{6}=\frac{u^{6}}{12}', [('integrate(u**5,u)/2', 'u**6/12')], '<b>كامل</b>: زِد الأس 1 واقسم عليه'),
        (r'=\frac{\left(x^{2}+1\right)^{6}}{12}+C', [('diff((x**2+1)**6/12,x)', 'x*(x**2+1)**5')], '<b>ارجع</b> $u=x^2+1$')],
        'pq3 ex1', check='اشتق الجواب: $\\frac{6(x^2+1)^5\\cdot2x}{12}=x(x^2+1)^5$ ✓ رجع السؤال.')
    ex += _example('مثال 2: ليش نقسم على k؟', r'\int\cos3x\,dx', [
        (r'u=3x,\qquad du=3\,dx\ \Rightarrow\ dx=\frac{du}{3}', [('diff(3*x,x)', '3')], '<b>اختر</b> ما داخل cos، و<b>اشتق</b>'),
        (r'\int\cos3x\,dx=\int\cos u\cdot\frac{du}{3}=\frac13\int\cos u\,du', [('cos(3*x)', 'Rational(1,3)*cos(3*x)*diff(3*x,x)')], '<b>عوّض</b>'),
        (r'=\frac13\sin u=\frac13\sin3x+C', [('diff(sin(3*x)/3,x)', 'cos(3*x)')], '<b>كامل</b> و<b>ارجع</b>. هذا سبب $\\frac1k$ في الجدول')],
        'pq3 ex2')
    body = basic + steps5 + choose + box('ex', 'أمثلة محلولة', ex)
    body += box('trap', '⚠️ الفخ', ul([rich('لا تكامل وفيه $x$ و $u$ مع بعض: لازم كل $x$ تختفي أولًا.'),
                                       rich('لا تنسَ الرقم اللي يطلع من $du$ (مثل $\\frac12$ أو $\\frac13$).'),
                                       rich('لا تنسَ ترجع لـ $x$ في الآخر، وتزيد $+C$.')]))
    body += _try('pq3', [('$\\int x^{2}\\left(x^{3}+2\\right)^{4}dx$', r'\frac{\left(x^{3}+2\right)^{5}}{15}+C',
                          [('diff((x**3+2)**5/15,x)', 'x**2*(x**3+2)**4')]),
                         ('$\\int e^{5x}dx$', r'\frac{e^{5x}}{5}+C', [('diff(exp(5*x)/5,x)', 'exp(5*x)')])])
    return _section('pq3', why, body)


# ---------------------------------------------------------------- ق4
def pq4():
    d = [formula('asin(u)', '1/sqrt(1-u**2)', 'diff', branches=('t/(1+t)', '-t/(1+t)'), uprime=True, label='pq4 d asin'),
         formula('acos(u)', '-1/sqrt(1-u**2)', 'diff', branches=('t/(1+t)', '-t/(1+t)'), uprime=True, label='pq4 d acos'),
         formula('atan(u)', '1/(1+u**2)', 'diff', branches=('x',), uprime=True, label='pq4 d atan'),
         formula('asec(u)', '1/(u*sqrt(u**2-1))', 'diff', branches=('1+t',), uprime=True, label='pq4 d asec (u > 1)')]
    i = [formula('1/sqrt(a**2-u**2)', 'asin(u/a)', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='pq4 int asin'),
         formula('1/(a**2+u**2)', 'atan(u/a)/a', branches=('x',), pos=('a',), label='pq4 int atan'),
         formula('1/(u*sqrt(u**2-a**2))', 'asec(u/a)/a', branches=('a+t',), pos=('a',), label='pq4 int asec (u > a)')]
    why = p(rich('في 5.1 نكامل الدوال العكسية بالتجزئة (النوعان 17 و18: $\\int\\tan^{-1}x$ و $\\int\\sin^{-1}x$ و $\\int x\\sec^{-1}x$)، '
                 'فنحتاج مشتقاتها. وفي النوع 15 يطلع $\\tan^{-1}$ من $\\int\\ln(1+x^2)$. وفي 4.2 لازم تفرّق بين '
                 'جداول 3.4 (المثلثية العكسية) وجداول 4.2 (الزائدية العكسية).'))
    body = box('short', 'المشتقات', table(['المشتقة', 'تساوي'], [_row(z) for z in d], 'formula compact')
               + p(rich('صف $\\sec^{-1}$ مكتوب لـ $u>1$ مثل مذكرة د. طارق.'), 'small'))
    body += box('short', 'التكاملات الثلاثة', table(['التكامل', 'الجواب (+C)', 'الشرط'],
                                                   [_row(i[0], mi('|u|<a')), _row(i[1], 'كل ' + mi('u')), _row(i[2], mi('u>a'))], 'formula compact'))
    cmp_rows = [[mi(r'\sqrt{a^{2}-u^{2}}'), mi(r'\sin^{-1}\frac{u}{a}'), '—'],
                [mi(r'\sqrt{u^{2}+a^{2}}'), '—', mi(r'\sinh^{-1}\frac{u}{a}')],
                [mi(r'\sqrt{u^{2}-a^{2}}'), '—', mi(r'\cosh^{-1}\frac{u}{a}')],
                [mi(r'a^{2}+u^{2}') + ' (بلا جذر)', mi(r'\frac1a\tan^{-1}\frac{u}{a}'), '—'],
                [mi(r'a^{2}-u^{2}') + ' (بلا جذر)', '—', mi(r'\frac1a\tanh^{-1}') + ' أو ' + mi(r'\coth^{-1}')],
                [mi(r'u\sqrt{u^{2}-a^{2}}'), mi(r'\frac1a\sec^{-1}\frac{u}{a}'), '—'],
                [mi(r'u\sqrt{a^{2}\pm u^{2}}'), '—', mi(r'\operatorname{sech}^{-1}') + ' أو ' + mi(r'\operatorname{csch}^{-1}')]]
    body += box('short', 'لا تخلط: 3.4 أم 4.2؟ (شكل المقام يقرر)', table(['في المقام', '3.4 مثلثية عكسية', '4.2 زائدية عكسية (الكويز)'], cmp_rows, 'formula compact')
                + p(rich('الكويز على عمود 4.2. أسئلة عمود 3.4 تجي في الكويز داخل التجزئة (5.1) أو للمقارنة فقط.'), 'small'))
    ex = _example('مثال 1: مشتقة', r'y=\tan^{-1}\left(x^{2}\right)', [
        (r"u=x^{2},\qquad u'=2x", [('diff(x**2,x)', '2*x')], 'ما داخل الدالة'),
        (r"y'=\frac{u'}{1+u^{2}}=\frac{2x}{1+x^{4}}", [('diff(atan(x**2),x)', '2*x/(1+x**4)')], 'صف $\\tan^{-1}$، و $(x^2)^2=x^4$')], 'pq4 ex1')
    ex += _example('مثال 2: تكامل', r'\int\frac{dx}{9+x^{2}}', [
        (r'9+x^{2}=3^{2}+x^{2}\ \Rightarrow\ a=3,\ u=x', [('9+x**2', '3**2+x**2')], 'رقم زائد مربع بلا جذر ⇐ $\\tan^{-1}$'),
        (r'\frac13\tan^{-1}\frac{x}{3}+C', [('diff(atan(x/3)/3,x)', '1/(9+x**2)')], 'صف $\\tan^{-1}$ مع $\\frac1a=\\frac13$')], 'pq4 ex2')
    ex += p(rich('<b>انتبه:</b> لو البسط $x$ فهو تعويض وليس $\\tan^{-1}$: $\\int\\frac{x\\,dx}{1+x^2}=\\frac12\\ln(1+x^2)$ (تحتاجه في النوع 17).'), 'small')
    arith('', [('diff(log(1+x**2)/2,x)', 'x/(1+x**2)')], 'pq4 x/(1+x^2)')
    body += box('ex', 'أمثلة محلولة', ex)
    body += box('trap', '⚠️ الفخ', ul([rich('$\\sin^{-1}x$ معكوس، وليست $\\frac{1}{\\sin x}$.'),
                                       rich('$a^2+u^2$ بلا جذر ⇐ $\\tan^{-1}$ (3.4). و $a^2-u^2$ بلا جذر ⇐ $\\tanh^{-1}$ (4.2). حرف واحد يفرق.')]))
    body += _try('pq4', [('أوجد $\\frac{d}{dx}\\sin^{-1}(3x)$.', r'\frac{3}{\sqrt{1-9x^{2}}}', [('diff(asin(3*x),x)', '3/sqrt(1-9*x**2)')]),
                         ('$\\int\\frac{dx}{\\sqrt{16-x^{2}}}$', r'\sin^{-1}\frac{x}{4}+C', [('diff(asin(x/4),x)', '1/sqrt(16-x**2)')])])
    SHEET['pq4'] = (table(['المشتقة', 'تساوي'], [_row(z) for z in d], 'formula compact')
                    + table(['التكامل', 'الجواب (+C)'], [_row(z) for z in i], 'formula compact'))
    return _section('pq4', why, body)


# ---------------------------------------------------------------- ق5
def pq5():
    why = p(rich('كل أنواع 5.2 تبدأ بتحويل بمتطابقة: نحوّل الباقي بعد الحجز (الأنواع 22–28)، أو نخفّض الأس بنصف الزاوية (النوع 24)، '
                 'أو نحوّل الضرب لجمع (النوع 29). والمشتقات في ' + link('pq2', 'ق2') + '، والتكاملات في ' + link('pq3', 'ق3') + '.'))
    pyth = alg('trig-pyth', 'متطابقات فيثاغورس', [
        (r'\sin^{2}x+\cos^{2}x=1', [('sin(x)**2+cos(x)**2', '1')], 'الأساس:'),
        (r'\cos^{2}x=1-\sin^{2}x,\qquad \sin^{2}x=1-\cos^{2}x', [('cos(x)**2', '1-sin(x)**2')], 'ننقل حدًا للطرف الثاني:'),
        (r'\sec^{2}x=1+\tan^{2}x,\qquad \csc^{2}x=1+\cot^{2}x', [('sec(x)**2', '1+tan(x)**2'), ('csc(x)**2', '1+cot(x)**2')],
         'نقسم الأساس على $\\cos^2x$ أو $\\sin^2x$ (تحتاجهما مع tan و cot):')])
    dbl = [(r'\sin2x=2\sin x\cos x', ('sin(2*x)', '2*sin(x)*cos(x)')),
           (r'\cos2x=\cos^{2}x-\sin^{2}x=2\cos^{2}x-1=1-2\sin^{2}x', ('cos(2*x)', '1-2*sin(x)**2')),
           (r'\cos^{2}x=\frac{1+\cos2x}{2},\qquad \sin^{2}x=\frac{1-\cos2x}{2}', ('sin(x)**2', '(1-cos(2*x))/2')),
           (r'\sin(-\theta)=-\sin\theta,\qquad \cos(-\theta)=\cos\theta', ('sin(-x)+sin(x)', '0')),
           (r'\sin0=0,\quad \cos0=1,\quad \sin\pi=0,\quad \cos\pi=-1', ('cos(pi)', '-1'))]
    extra = arith('', [('cos(2*x)', '2*cos(x)**2-1'), ('cos(x)**2', '(1+cos(2*x))/2'), ('cos(-x)', 'cos(x)'), ('sin(pi)', '0')], 'pq5 extra')
    body = pyth + box('short', 'ضعف الزاوية ونصفها، والإشارات', table(['المتطابقة'], [[mi(r'\displaystyle ' + arith(lt, [c], 'pq5 identity'))]
                                                                              for lt, c in dbl], 'formula compact') + extra
                      + p(rich('نصف الزاوية: مع $\\cos^2$ زائد، ومع $\\sin^2$ ناقص. والزاوية تتضاعف: $\\cos^2 3x=\\frac{1+\\cos6x}{2}$.'), 'small'))
    ex = _example('مثال 1: خفّض الأس (النوع 24)', r'\sin^{2}x\cos^{2}x', [
        (r'\sin x\cos x=\frac12\sin2x', [('sin(x)*cos(x)', 'sin(2*x)/2')], 'من $\\sin2x=2\\sin x\\cos x$'),
        (r'\sin^{2}x\cos^{2}x=\left(\frac12\sin2x\right)^{2}=\frac14\sin^{2}2x', [('sin(x)**2*cos(x)**2', 'sin(2*x)**2/4')], 'نربّع الطرفين'),
        (r'=\frac14\cdot\frac{1-\cos4x}{2}=\frac{1-\cos4x}{8}', [('sin(x)**2*cos(x)**2', '(1-cos(4*x))/8')], 'نصف الزاوية مع $2x$: الزاوية تصير $4x$')],
        'pq5 ex1')
    ex += _example('مثال 2: حوّل للحجز (الأنواع 22–28)', r'\tan^{3}x', [
        (r'\tan^{3}x=\tan x\cdot\tan^{2}x', [('tan(x)**3', 'tan(x)*tan(x)**2')], 'نفصل مربعًا'),
        (r'=\tan x\left(\sec^{2}x-1\right)', [('tan(x)**3', 'tan(x)*(sec(x)**2-1)')], 'من $\\sec^2x=1+\\tan^2x$')], 'pq5 ex2')
    body += box('ex', 'أمثلة محلولة', ex)
    body += box('trap', '⚠️ الفخ', ul([rich('$\\sin2x\\ne2\\sin x$. الصح $2\\sin x\\cos x$.'),
                                       rich('$\\sin^2x$ تعني $(\\sin x)^2$، وليست $\\sin(x^2)$.')]))
    body += _try('pq5', [('اكتب $\\sin^{2}4x$ بنصف الزاوية.', r'\sin^{2}4x=\frac{1-\cos8x}{2}', [('sin(4*x)**2', '(1-cos(8*x))/2')]),
                         ('اكتب $\\cot^{2}x$ بدلالة $\\csc x$.', r'\cot^{2}x=\csc^{2}x-1', [('cot(x)**2', 'csc(x)**2-1')])])
    SHEET['pq5'] = table(['المتطابقة'], [[mi(r'\displaystyle ' + r'\sin^{2}x+\cos^{2}x=1,\quad \sec^{2}x=1+\tan^{2}x,\quad \csc^{2}x=1+\cot^{2}x')]]
                         + [[mi(r'\displaystyle ' + lt)] for lt, _ in dbl[:3]], 'formula compact')
    return _section('pq5', why, body)


BUILDERS = {'pq1': pq1, 'pq2': pq2, 'pq3': pq3, 'pq4': pq4, 'pq5': pq5}


def build(anchors):
    """Build the given pages now (call in document order, so that algebra boxes and keys follow the page order)."""
    for a in anchors:
        HTML[a] = BUILDERS[a]()


def sheet():
    """Formula-sheet block: 4.1 derivatives and identities, 3.4, trigonometric identities."""
    return ('<h3>من الدروس السابقة</h3>' + p('<b>4.1 الزائدية:</b>') + '<div class="fsheet">' + SHEET['pq1'] + '</div>'
            + p('<b>3.4 المثلثية العكسية:</b>') + '<div class="fsheet">' + SHEET['pq4'] + '</div>'
            + p('<b>المثلثات:</b>') + '<div class="fsheet">' + SHEET['pq5'] + '</div>')

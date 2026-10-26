"""المذكرة الكاملة v7 — صفحات الطرق: كيف تذاكر منها، القسم 0 (قبل أي حل)، الشجرة، أول صفحة في كل طريقة (السكربت،
كيف تفرّق، خريطتها)، القسم د (التمييز والتذكر)، ورقة الدرجة الكاملة، «جوابك يختلف عن المفتاح؟».

Every math line on these pages is checked while building (arith / formula); a failed check stops the build.
"""
import guide_kit as K
from booklet_engine import arith, formula
from guide_kit import part, pgref, rich
from html_kit import box, en, lines, link, md, mi, p, table, ul


def chapter(id_, title, inner, cls=''):
    """A page of its own; any $…$ left in its text (table cells) becomes inline math."""
    return '<section class="chapter %s" id="%s"><h2>%s</h2>%s</section>' % (cls, id_, title, rich(inner))


def M(latex, claims, label):
    """Inline math whose claims are checked."""
    return mi(r'\displaystyle ' + arith(latex, claims, label))


def D(latex, claims, label):
    """Display math whose claims are checked."""
    return md(arith(latex, claims, label))


def F(f, F_, kind='int', label='', **kw):
    """A general rule printed from SymPy and checked: 'lhs = rhs'."""
    lhs, rhs = formula(f, F_, kind, label=label, **kw)
    return mi(r'\displaystyle ' + lhs + ' = ' + rhs)


# ---------------------------------------------------------------- the fixed words of each method
SCRIPTS = {
    'A': ['وش الدالة اللي برّا؟', 'مشتقتها من الجدول، والداخل يبقى مثل ما هو', '🟢 × مشتقة الداخل', 'بسّط',
          '🔴 <b>لا تنسى:</b> كل حد له مشتقته، و $y\'=$ قبل الجواب'],
    'B': ['🔵 سمّ الداخل $u$', '🟢 اشتقه: $du=\\ldots\\,dx$',
          '🟠 اقسم اللي برّا على مشتقة الداخل: طلع رقم؟ هذا رقم التعديل، يطلع قدّام التكامل مرة وحدة بس',
          'اكتب التكامل كله بـ $u$، وطبّق القانون', 'رجّع $x$، وحط $+C$',
          '🔴 <b>لا تنسى:</b> $|u|$ داخل ln، ورقم التعديل مرة وحدة، و $+C$'],
    'P': ['وش الشكل اللي يدلك؟', 'سوّ الحركة', 'تأكد برقم إن الشكل الجديد يساوي القديم', 'ارجع للشجرة: الحين وش الطريقة؟',
          '🔴 <b>لا تنسى:</b> التجهيز ما يغيّر القيمة؛ لو الرقم ما طابق، الحركة غلط'],
    'C': ['رتّب بـ LIATE: اللي أول هو 🔵 $u$، والباقي $dv$', 'المربع: $u$ و $dv$ فوق، و 🟢 $du$ و $v$ تحت',
          'القانون: $uv-\\int v\\,du$', 'كمّل $\\int v\\,du$؛ وإذا تكررت التجزئة: جدول DI، وعمود الإشارات 🔴 $+\\,-\\,+$ تكتبه أول',
          '$+C$؛ وفي المحدد: احسب كامل، ثم عوّض',
          '🔴 <b>لا تنسى:</b> السالب قدّام $\\int v\\,du$ يدخل على كل حدوده'],
}
SEC_ID = {'A': 'sA', 'B': 'sB', 'P': 'sP', 'C': 'sC'}
# the four questions of the tree: (label, question, where it sends you)
TREE_Q = [
    ('س1', 'المطلوب <b>مشتقة</b>؟ (Find dy/dx، أو Find the derivative)', 'أ. الاشتقاق', 'sA'),
    ('س2', 'تكامل. فيه <b>دالة ومشتقتها</b>؟ اقسم اللي برّا على مشتقة الداخل: طلع رقم؟ أو شكله <b>قانون جاهز</b>؟ '
           'ومع sin و cos و tan و sec: تقدر <b>تحجز</b> وحدة فتصير دالة ومشتقتها؟', 'ب. التعويض', 'sB'),
    ('س3', 'لا؟ دوّر <b>علامة تجهيز</b>: $x^2$ و $x$ تحت الجذر، بسط فيه جمع، $\\sin^2$ لحالها، زاويتين مختلفتين، '
           '$\\tan^n$ لحالها، sinh أو cosh مع $e^x$ أو في المقام، $x^3$ فوق $x^2+a$، ln لقوة أو جذر', 'سوّ الحركة، ثم ارجع لـ س2', 'sP'),
    ('س4', 'ولا علامة؟ <b>ضرب نوعين مختلفين</b> (مثل $x\\,e^{3x}$، $x^2\\ln x$)، أو $\\ln$ أو دالة عكسية لحالها', 'ج. التجزئة', 'sC'),
]


def script_html(m, ex_rows=None):
    """The fixed steps of a method, numbered, in the same words everywhere."""
    return '<ol class="script %s">%s</ol>' % (K.METHODS[m][2], ''.join('<li>%s</li>' % rich(t) for t in SCRIPTS[m]))


# ================================================================ how to study (first pages)
def legend():
    colours = table(['اللون', 'معناه', 'مثال'], [
        ['🔵 أزرق', 'الداخل، أو $u$ اللي تسمّيه', M(r'\cU{u=x^{2}}', [], 'legend u')],
        ['🟢 أخضر', 'مشتقة الداخل، أو $du$', M(r'\cD{du=2x\,dx}', [('diff(x**2,x)', '2*x')], 'legend du')],
        ['🟠 برتقالي', 'رقم التعديل (يطلع قدّام التكامل مرة وحدة)', M(r'\cA{\tfrac12}\int\cosh u\,du', [], 'legend adj')],
        ['🔴 أحمر', 'السالب أو الخطر: إشارة تضيع، أو غلطة مشهورة', M(r'\int\sin x\,dx=\cR{-}\cos x+C', [('diff(-cos(x),x)', 'sin(x)')], 'legend minus')]],
        'legend')
    marks = table(['الرمز', 'معناه'], [
        ['📍 الشجرة', 'أي سؤال في الشجرة يوديك لهذي الحالة'], ['🔥', 'كم مرة جات الحالة في الاختبارات الـ12 السابقة'],
        ['📝 · 📗 · 📘 · ✏️', 'مصدر السؤال: اختبار سابق، مذكرة د. موسى، مذكرة د. طارق، تدريب إضافي كتبناه'],
        ['🔑', 'تريك صغير يمنع غلطة مشهورة'], ['⚡', 'طريقة أسرع لنفس الحل، تتأكد فيها من جوابك'],
        ['✎', 'إشارة $\\coth^{-1}$ مثل ما يكتبها دكتورك'],
        ['☐ ✓ / ؟ / ✗', 'ثقتك بالحالة بعد ما تحل تمارينها: ✓ أحلها لحالي، ؟ أحتاج المثال، ✗ ارجع لها بكرة']], 'legend')
    colours, marks = rich(colours), rich(marks)
    return colours, marks


def howto(plan_rows, old_rows):
    order = ul([
        '<b>المذكرة مرتبة بطريقة الحل، مو بالدرس.</b> في الكويز ما أحد يقول لك «هذا من 5.1». أنت تشوف السؤال وتقرّر الطريقة. '
        'فالمذكرة تعلّمك القرار: ' + link('tree', 'الشجرة') + ' أربعة أسئلة، وكل سؤال يوديك لطريقة.',
        '<b>الأقسام:</b> 0. قبل أي حل ← أ. الاشتقاق ← 🌳 الشجرة ← ب. التعويض ← 🔧 التجهيزات ← ج. التجزئة ← د. التمييز والتذكر.',
        '<b>كل حالة بنفس الترتيب:</b> 🔎 متى؟ ← 💡 ليش تشتغل؟ ← 🪜 الخطوات ← 🧱 مثال محلول ← ⚡ (إذا فيه) ← ✔ قبل ما تسلّم ← التمارين.',
        '<b>الخطوات</b> في كل طريقة بنفس الكلمات (السكربت). احفظ السكربت، وكل حالة تزيد عليه تفصيلة.',
        '<b>جدول الحل</b> فيه عمودان: «الخطوة» تكتبها في الكويز، و«ليش؟» لك أنت عشان تفهم.',
        '<b>التمارين</b> متدرجة: موجّه (أول سطر جاهز)، ثم ناقص الخطوات، ثم لحالك. حاول بالقلم، وبعدين اضغط «✅ الحل».'])
    colours, marks = legend()
    links = ul([rich('<b>4.1 ← 4.2:</b> 4.2 هو 4.1 بالعكس. $\\sinh$ تعطي $\\cosh$، والمعكوس $\\sinh^{-1}$ له مشتقة جديدة في الجدول.'),
                rich('<b>المشتقة ← التكامل:</b> كل صف في جدول المشتقات، اقلبه يصير قانون تكامل: '
                     '$(\\sinh^{-1}u)\'=\\frac{u\'}{\\sqrt{u^2+1}}$، فـ $\\int\\frac{du}{\\sqrt{u^2+1}}=\\sinh^{-1}u$.'),
                rich('<b>التعويض = قاعدة السلسلة بالعكس:</b> في المشتقة تضرب في 🟢 مشتقة الداخل. في التكامل تلقاها جاهزة، وتشيلها بـ $du$.'),
                rich('<b>التجزئة = قاعدة الضرب بالعكس:</b> $(uv)\'=u\'v+uv\'$، فـ $\\int u\\,dv=uv-\\int v\\,du$.'),
                rich('<b>5.2 = تجهيز + تعويض:</b> تحجز $\\sin x$ أو $\\sec^2x$، فيصير السؤال تعويض عادي. وأحيانًا تجزئة ($\\sec^3x$).'),
                rich('<b>فالكويز كله أربع أدوات:</b> جدول مشتقات، وجدول تكاملات، وتعويض، وتجزئة. والتجهيزات بس تصلّح الشكل.')])
    old = table(['الرقم القديم', 'الحالة الجديدة', 'العنوان', 'ص'], old_rows, 'answers oldnew')
    gloss = table(['في ورقة الكويز', 'معناها'], [
        [en('Evaluate the following integrals'), 'احسب التكاملات التالية'],
        [en('Find dy/dx  /  Find the derivative'), 'أوجد المشتقة'],
        [mi(r'\sinh^{-1}x') + ' أو ' + en('arcsinh x'), 'معكوس sinh (مو ' + mi(r'\frac{1}{\sinh x}') + ')'],
        [mi(r'\log x'), 'لوغاريتم بأساس 10؛ و ' + mi(r'\ln x') + ' الطبيعي']], 'glossary')
    return chapter('howto', 'كيف تذاكر منها', order
                   + '<h3>🔗 هل الدروس مترابطة؟ إيه، وهذي الروابط</h3>' + links
                   + '<h3>📋 الترتيب</h3>' + '<ol class="plan">' + ''.join('<li>%s</li>' % r[1] for r in plan_rows) + '</ol>'
                   + '<h3>🎨 الألوان: نفس المعنى في كل المذكرة</h3>' + colours
                   + p('كل لون معه رمز، فلو طبعت المذكرة أبيض وأسود تعرف المعنى من الرمز.', 'small')
                   + '<h3>الرموز</h3>' + marks
                   + '<h3 id="oldnew">🔁 الرقم القديم ← الحالة الجديدة</h3>'
                   + p('إذا ذاكرت من النسخة القديمة: كل رقم قديم صار له رقم حالة جديد. دوّر رقمك القديم هنا.', 'small') + old
                   + '<h3>كلمات الأسئلة الإنجليزية</h3>' + gloss)


# ================================================================ 0. before any solution
def sec0():
    mode = p(rich('<b>أول شي تكتبه جنب كل سؤال: «مشتقة» أو «تكامل».</b> اقرأ أول كلمة: <b>Find dy/dx</b> أو '
                  '<b>Find the derivative</b> = مشتقة. <b>Evaluate</b> و $\\int$ = تكامل. '
                  'نص الأغلاط تبدأ من هنا: تكامل الثابت صفر، أو تشتق وأنت المفروض تكامل.'))
    pairs = table(['الدالة', 'مشتقتها', 'تكاملها (+C)'], [
        [mi('5'), M('0', [('diff(5,x)', '0')], 'pair const d'), M(r'\cR{5x}\ \ (\text{not }0)', [('diff(5*x,x)', '5')], 'pair const i')],
        [mi('x^{n}'), M('n\\,x^{n-1}', [('diff(x**3,x)', '3*x**2')], 'pair pow d'), M(r'\frac{x^{n+1}}{n+1}', [('diff(x**4/4,x)', 'x**3')], 'pair pow i')],
        [mi(r'\frac1x'), M(r'-\frac{1}{x^{2}}', [('diff(1/x,x)', '-1/x**2')], 'pair inv d'), M(r'\ln|x|', [('diff(log(x),x)', '1/x', 't')], 'pair inv i')],
        [mi(r'\ln x'), M(r'\frac1x', [('diff(log(x),x)', '1/x', 't')], 'pair ln d'), M(r'x\ln x-x', [('diff(x*log(x)-x,x)', 'log(x)', 't')], 'pair ln i')],
        [mi('e^{3x}'), M(r'3e^{3x}', [('diff(exp(3*x),x)', '3*exp(3*x)')], 'pair exp d'), M(r'\frac{e^{3x}}{3}', [('diff(exp(3*x)/3,x)', 'exp(3*x)')], 'pair exp i')],
        [mi('2^{x}'), M(r'2^{x}\ln2', [('diff(2**x,x)', '2**x*log(2)')], 'pair a d'), M(r'\frac{2^{x}}{\ln2}', [('diff(2**x/log(2),x)', '2**x')], 'pair a i')],
        [mi(r'\sin x'), M(r'\cos x', [('diff(sin(x),x)', 'cos(x)')], 'pair sin d'), M(r'\cR{-}\cos x', [('diff(-cos(x),x)', 'sin(x)')], 'pair sin i')],
        [mi(r'\cos x'), M(r'\cR{-}\sin x', [('diff(cos(x),x)', '-sin(x)')], 'pair cos d'), M(r'\sin x', [('diff(sin(x),x)', 'cos(x)')], 'pair cos i')],
        [mi(r'\sinh x'), M(r'\cosh x', [('diff(sinh(x),x)', 'cosh(x)')], 'pair sinh d'), M(r'\cosh x', [('diff(cosh(x),x)', 'sinh(x)')], 'pair sinh i')],
        [mi(r'\cosh x'), M(r'\sinh x', [('diff(cosh(x),x)', 'sinh(x)')], 'pair cosh d'), M(r'\sinh x', [('diff(sinh(x),x)', 'cosh(x)')], 'pair cosh i')],
        [mi(r'\tan x'), M(r'\sec^{2}x', [('diff(tan(x),x)', 'sec(x)**2')], 'pair tan d'), M(r'\ln|\sec x|', [('diff(log(sec(x)),x)', 'tan(x)', 't/(1+t)')], 'pair tan i')],
        [mi(r'\sec x'), M(r'\sec x\tan x', [('diff(sec(x),x)', 'sec(x)*tan(x)')], 'pair sec d'),
         M(r'\ln|\sec x+\tan x|', [('diff(log(sec(x)+tan(x)),x)', 'sec(x)', 't/(1+t)')], 'pair sec i')]], 'pairs')
    four = table(['تكتبها كذا', 'معناها', 'مشتقتها'], [
        [mi(r'\sinh x'), 'الدالة نفسها (4.1)', M(r'\cosh x', [('diff(sinh(x),x)', 'cosh(x)')], 'four 1')],
        [mi(r'\sinh^{-1}x'), 'المعكوس (4.2). الـ $-1$ <b>اسم</b>، مو أس', M(r'\frac{1}{\sqrt{x^{2}+1}}', [('diff(asinh(x),x)', '1/sqrt(x**2+1)')], 'four 2')],
        [mi(r'\frac{1}{\sinh x}=\operatorname{csch}x'), 'المقلوب: واحد على الدالة', M(r'\cR{-}\operatorname{csch}x\coth x', [('diff(1/sinh(x),x)', '-csch(x)*coth(x)')], 'four 3')],
        [mi(r'\sinh^{2}x=(\sinh x)^{2}'), 'التربيع: الأس 2 على الدالة كلها', M(r'2\sinh x\cosh x', [('diff(sinh(x)**2,x)', '2*sinh(x)*cosh(x)')], 'four 4')],
        [mi(r'\sin^{-1}x'), 'المعكوس (3.4)', M(r'\frac{1}{\sqrt{1-x^{2}}}', [('diff(asin(x),x)', '1/sqrt(1-x**2)', 't/(1+t)')], 'four 5')],
        [mi(r'\frac{1}{\sin x}=\csc x'), 'المقلوب', M(r'\cR{-}\csc x\cot x', [('diff(1/sin(x),x)', '-csc(x)*cot(x)')], 'four 6')]], 'four')
    moves = [
        ('الأسس', r'x^{a}\cdot x^{b}=x^{a+b},\qquad \frac{1}{x^{n}}=x^{-n},\qquad \sqrt[n]{x^{m}}=x^{m/n}',
         [('x**2*x**3', 'x**5'), ('1/x**3', 'x**(-3)'), ('sqrt(x**3)', 'x**Rational(3,2)', 't')],
         r'\sqrt{4^{3}}=\sqrt{64}=8=4^{3/2}', [('sqrt(4**3)', '8'), ('4**Rational(3,2)', '8')]),
        ('اكتبها كمربع', r'9x^{4}=(3x^{2})^{2},\qquad e^{6x}=(e^{3x})^{2},\qquad x=(\sqrt x)^{2}',
         [('9*x**4', '(3*x**2)**2'), ('exp(6*x)', 'exp(3*x)**2'), ('x', 'sqrt(x)**2', 't')],
         r'x=2:\ 9\cdot16=144=6^{2}', [('9*2**4', '(3*2**2)**2')]),
        ('السالب قدّام القوس', r'-(a-b)=-a+b', [('-(x-3)', '-x+3')], r'-(5-2)=-3=-5+2', [('-(5-2)', '-5+2')]),
        ('مربع القوس', r'(a+b)^{2}=a^{2}+2ab+b^{2}', [('(x+3)**2', 'x**2+6*x+9')], r'(3+1)^{2}=16=9+6+1', [('(3+1)**2', '9+6+1')]),
        ('افصل الكسر (البسط بس)', r'\frac{a+b}{c}=\frac{a}{c}+\frac{b}{c}', [('(x+2)/(x**2+4)', 'x/(x**2+4)+2/(x**2+4)')],
         r'\frac{2+4}{3}=2=\frac23+\frac43', [('Rational(6,3)', 'Rational(2,3)+Rational(4,3)')]),
        ('كسر فوق كسر', r'\frac{\ a/b\ }{c}=\frac{a}{b\,c}', [('(1/(2*x))/(x+1)', '1/(2*x*(x+1))')],
         r'\frac{\ 1/2\ }{3}=\frac16', [('Rational(1,2)/3', 'Rational(1,6)')]),
        ('العامل المشترك (ومن الجذر)', r'\sqrt{9x^{2}+36}=\sqrt{9(x^{2}+4)}=3\sqrt{x^{2}+4}', [('sqrt(9*x**2+36)', '3*sqrt(x**2+4)')],
         r'x=0:\ \sqrt{36}=6=3\cdot2', [('sqrt(36)', '3*2')]),
        ('خواص ln (تفك الضرب والقوة، ما تفك الجمع)', r'\ln(ab)=\ln a+\ln b,\qquad \ln x^{n}=n\ln x,\qquad \ln\sqrt[3]{x}=\tfrac13\ln x',
         [('log(2*x)', 'log(2)+log(x)', 't'), ('log(x**5)', '5*log(x)', 't'), ('log(x**Rational(1,3))', 'log(x)/3', 't')],
         r'x=8:\ \ln2=\tfrac13\ln8', [('log(2)', 'log(8)/3')]),
        ('أضف واطرح', r'\frac{x^{2}}{x^{2}+1}=\frac{x^{2}+1-1}{x^{2}+1}=1-\frac{1}{x^{2}+1}', [('x**2/(x**2+1)', '1-1/(x**2+1)')],
         r'x=1:\ \tfrac12=1-\tfrac12', [('Rational(1,2)', '1-Rational(1,2)')])]
    mv = ''.join('<li><b>%s:</b> %s<div class="numcheck">🔢 فحص برقم: %s</div></li>'
                 % (name, M(rule, rc, 'move %d' % k), M(num, nc, 'move %d check' % k))
                 for k, (name, rule, rc, num, nc) in enumerate(moves, 1))
    import sympy as sp
    angles = [('0', '0'), (r'\frac{\pi}{6}', 'pi/6'), (r'\frac{\pi}{4}', 'pi/4'), (r'\frac{\pi}{3}', 'pi/3'), (r'\frac{\pi}{2}', 'pi/2')]
    vals = {'sin': ['0', r'\frac12', r'\frac{\sqrt2}{2}', r'\frac{\sqrt3}{2}', '1'],
            'cos': ['1', r'\frac{\sqrt3}{2}', r'\frac{\sqrt2}{2}', r'\frac12', '0'],
            'tan': ['0', r'\frac{1}{\sqrt3}', '1', r'\sqrt3', r'\text{—}'],
            'sec': ['1', r'\frac{2}{\sqrt3}', r'\sqrt2', '2', r'\text{—}']}
    exact = {'sin': ['0', '1/2', 'sqrt(2)/2', 'sqrt(3)/2', '1'], 'cos': ['1', 'sqrt(3)/2', 'sqrt(2)/2', '1/2', '0'],
             'tan': ['0', '1/sqrt(3)', '1', 'sqrt(3)', None], 'sec': ['1', '2/sqrt(3)', 'sqrt(2)', '2', None]}
    trig_rows = []
    for fn in ('sin', 'cos', 'tan', 'sec'):
        row = [mi('\\' + fn + ' x')]
        for k, (lab, a) in enumerate(angles):
            claims = [('%s(%s)' % (fn, a), exact[fn][k])] if exact[fn][k] else []
            row.append(M(vals[fn][k], claims, 'trig value %s %s' % (fn, a)))
        trig_rows.append(row)
    trig = table(['', '0'] + [mi(a) for a, _ in angles[1:]], trig_rows, 'trigvals')
    other = M(r'\ln1=0,\quad e^{0}=1,\quad \sinh0=0,\quad \cosh0=1,\quad \tanh0=0',
              [('log(1)', '0'), ('exp(0)', '1'), ('sinh(0)', '0'), ('cosh(0)', '1'), ('tanh(0)', '0')], 'zero values')
    body = (part('✍️ سطر الوضع', mode)
            + part('🔁 نفس الدالة: مشتقتها جنب تكاملها', p(rich('أكثر غلطتين: تكامل الثابت صفر 🔴، وتخلط بين مشتقة ln وتكاملها. '
                                                                  'غطِّ عمودين، واكتبهم من ذاكرتك.')) + pairs, 'p-steps')
            + part('🔀 الأربعة اللي تتلخبط', p(rich('نفس الحروف، وأربعة معاني. الـ $-1$ على <b>اسم</b> الدالة معناه معكوس. '
                                                     'أما المقلوب فيصير الدالة تحت واحد، وله اسم ثاني (csch و csc).')) + four)
            + part('🧮 حركات الجبر التسع، وكل حركة معها فحص برقم',
                   p(rich('قبل ما تكمّل حل، أي حركة شكّيت فيها: عوّض رقم صغير في الطرفين. لو طلعوا نفس الرقم فالحركة صح.'))
                   + '<ol class="moves">' + mv + '</ol>')
            + part('📐 جدول قيم المثلثات (للتكامل المحدد)', p('وقيم لازم تعرفها: ' + other) + trig, 'p-steps'))
    return chapter('s0', '0. قبل أي حل', body, 'method m0')


# ================================================================ the tree
def tree():
    qs = ''.join('<div class="tq"><span class="tl">%s</span><div class="tb">%s</div><div class="tg">← %s</div></div>'
                 % (lab, rich(q), link(sec, rich(go))) for lab, q, go, sec in TREE_Q)
    basic = table(['التكامل', 'الجواب (+C)', 'انتبه'], [
        [mi(r'\int 5\,dx'), M(r'\cR{5x}', [('diff(5*x,x)', '5')], 'basic const'), '🔴 تكامل الثابت <b>مو صفر</b>: الثابت ومعه $x$'],
        [mi(r'\int x^{n}\,dx'), M(r'\frac{x^{n+1}}{n+1}', [('diff(x**6/6,x)', 'x**5')], 'basic pow'), '$n\\ne-1$'],
        [mi(r'\int\frac{dx}{x}'), M(r'\ln|x|', [('diff(log(x),x)', '1/x', 't')], 'basic ln'), 'مع $\\frac1x$ بس؛ غيره قاعدة القوة'],
        [mi(r'\int e^{kx}\,dx'), M(r'\frac{e^{kx}}{k}', [('diff(exp(5*x)/5,x)', 'exp(5*x)')], 'basic exp'), 'اقسم على رقم $x$'],
        [mi(r'\int a^{u}\,du'), M(r'\frac{a^{u}}{\ln a}', [('diff(2**x/log(2),x)', '2**x'), ('diff(pi**x/log(pi),x)', 'pi**x')], 'basic a^u'),
         'الأساس رقم (مثل $2$ أو $\\pi$)، والأس فيه $x$'],
        [mi(r'\int\sin x\,dx'), M(r'\cR{-}\cos x', [('diff(-cos(x),x)', 'sin(x)')], 'basic sin'), '🔴 السالب مع sin'],
        [mi(r'\int\cos x\,dx'), M(r'\sin x', [('diff(sin(x),x)', 'cos(x)')], 'basic cos'), ''],
        [mi(r'\int\sec^{2}x\,dx'), M(r'\tan x', [('diff(tan(x),x)', 'sec(x)**2')], 'basic sec2'), ''],
        [mi(r'\int\sec x\tan x\,dx'), M(r'\sec x', [('diff(sec(x),x)', 'sec(x)*tan(x)')], 'basic sectan'), ''],
        [mi(r'\int\csc^{2}x\,dx'), M(r'\cR{-}\cot x', [('diff(-cot(x),x)', 'csc(x)**2')], 'basic csc2'), '🔴 السالب مع co'],
        [mi(r'\int\tan x\,dx'), M(r'\ln|\sec x|', [('diff(log(sec(x)),x)', 'tan(x)', 't/(1+t)')], 'basic tan'), ''],
        [mi(r'\int\sec x\,dx'), M(r'\ln|\sec x+\tan x|', [('diff(log(sec(x)+tan(x)),x)', 'sec(x)', 't/(1+t)')], 'basic sec'), ''],
        [mi(r'\int\sinh x\,dx'), M(r'\cosh x', [('diff(cosh(x),x)', 'sinh(x)')], 'basic sinh'), 'بدون سالب'],
        [mi(r'\int\cosh x\,dx'), M(r'\sinh x', [('diff(sinh(x),x)', 'cosh(x)')], 'basic cosh'), 'بدون سالب'],
        [mi(r'\int\operatorname{sech}^{2}x\,dx'), M(r'\tanh x', [('diff(tanh(x),x)', 'sech(x)**2')], 'basic sech2'), '']], 'basic')
    pairs = [
        (r'\int x\cosh(x^{2})\,dx', 'تعويض: $\\cU{u=x^2}$', r'\int x\cosh x\,dx', 'تجزئة: $u=x$، $dv=\\cosh x\\,dx$',
         'اقسم اللي برّا على مشتقة الداخل: $\\frac{x}{2x}=\\frac12$ رقم ← تعويض. $\\frac{x}{1}=x$ مو رقم ← تجزئة.'),
        (r'\int x\,e^{x^{2}}\,dx', 'تعويض: $\\cU{u=x^2}$', r'\int x\,e^{3x}\,dx', 'تجزئة: $u=x$، $dv=e^{3x}dx$', 'نفس السؤال: اقسم على مشتقة الداخل.'),
        (r'\int\frac{\ln x}{x}\,dx', 'تعويض: $\\cU{u=\\ln x}$', r'\int\ln x\,dx', 'تجزئة: $u=\\ln x$، $dv=dx$',
         '$\\frac1x$ هي مشتقة $\\ln x$ ← تعويض. ln لحالها ← تجزئة.'),
        (r'\int\frac{dx}{\sqrt{x^{2}+9}}', 'قانون: $\\sinh^{-1}\\frac x3$', r'\int\frac{x\,dx}{\sqrt{x^{2}+9}}', 'تعويض: $\\cU{u=x^2+9}$',
         'فوق $x$ = نص مشتقة اللي تحت ← تعويض عادي. فوق رقم ← قانون 4.2.'),
        (r'\int\frac{dx}{9-x^{2}}', '4.2: $\\tanh^{-1}$ أو $\\coth^{-1}$', r'\int\frac{dx}{9+x^{2}}', '3.4: $\\frac13\\tan^{-1}\\frac x3$',
         'ناقص بين الرقم و $x^2$ ← 4.2. زائد ← 3.4 ($\\tan^{-1}$).'),
        (r'\int\frac{dx}{\sqrt{9-x^{2}}}', '3.4: $\\sin^{-1}\\frac x3$', r'\int\frac{dx}{\sqrt{x^{2}-9}}', '4.2: $\\cosh^{-1}\\frac x3$',
         'الرقم أول (الرقم ناقص $x^2$) ← $\\sin^{-1}$. $x^2$ أول ← $\\cosh^{-1}$.'),
        (r'\int\frac{dx}{x\sqrt{9-x^{2}}}', '4.2: $\\operatorname{sech}^{-1}$', r'\int\frac{dx}{x\sqrt{x^{2}-9}}', '3.4: $\\sec^{-1}$',
         '$u$ برّا الجذر: الرقم أول ← sech⁻¹، $x^2$ أول ← sec⁻¹، والزائد ← csch⁻¹.'),
        (r'\int\sin^{3}x\,dx', 'احجز $\\sin x$: $\\cU{u=\\cos x}$', r'\int\sin^{2}x\,dx', 'تجهيز: نص الزاوية',
         'أس فردي ← احجز وحدة. أس زوجي لحاله ← نص الزاوية.'),
        (r'\int\tan x\sec^{2}x\,dx', 'تعويض: $\\cU{u=\\tan x}$', r'\int\tan^{2}x\,dx', 'تجهيز: $\\tan^2x=\\sec^2x-1$',
         'معها $\\sec^2x$ (مشتقة tan) ← تعويض. tan لحالها ← اكسرها.'),
        (r'\int\frac{2x}{x^{2}+9}\,dx', 'تعويض: $\\cU{u=x^2+9}$ ← ln', r'\int\frac{x+3}{x^{2}+9}\,dx', 'تجهيز: افصل الكسر',
         'البسط كله مشتقة المقام ← تعويض. البسط فيه جمع ← افصل، وكل كسر لحاله.'),
        (r'\int\frac{x}{x^{2}+4}\,dx', 'تعويض: $\\cU{u=x^2+4}$', r'\int\frac{x^{3}}{x^{2}+4}\,dx', 'تجهيز: $x^2=u-4$',
         '$\\frac{x}{2x}$ رقم ← تعويض. $\\frac{x^3}{2x}=\\frac{x^2}{2}$ فيه $x$ ← اكتب $x^2$ بـ $u$.'),
        (r'\int e^{x}\sinh x\,dx', 'تجهيز: sinh بالأسس', r'\int e^{x}\sin x\,dx', 'تجزئة مرتين (يرجع لنفسه)',
         'sinh و cosh مع $e^x$ ← بالأسس، أسرع. sin و cos ← تجزئة.')]
    prow = [[mi(r'\displaystyle ' + a), rich(ma), mi(r'\displaystyle ' + b), rich(mb), rich(why)] for a, ma, b, mb, why in pairs]
    # the first lines quoted in the pairs, checked
    arith('', [('diff(x**2,x)', '2*x'), ('diff(log(x),x)', '1/x', 't'), ('diff(x**2+9,x)', '2*x'), ('diff(cos(x),x)', '-sin(x)'),
               ('diff(tan(x),x)', 'sec(x)**2'), ('tan(x)**2', 'sec(x)**2-1'), ('diff(asinh(x/3),x)', '1/sqrt(x**2+9)'),
               ('diff(atan(x/3)/3,x)', '1/(9+x**2)'), ('diff(asin(x/3),x)', '1/sqrt(9-x**2)', '3*t/(1+t)'),
               ('diff(acosh(x/3),x)', '1/sqrt(x**2-9)', '3+t'), ('(x+3)/(x**2+9)', 'x/(x**2+9)+3/(x**2+9)'),
               ('exp(x)*sinh(x)', '(exp(2*x)-1)/2')], 'tree pairs')
    rule = p(rich('<b>🔒 قاعدة الشجرة:</b> قرّر مرة وحدة بسبب واضح، واكتب السبب بكلمة جنب السؤال. <b>لا تغيّر الطريقة إلا إذا فشلت</b> '
                  '(طلع لك $x$ بعد ما قسمت، أو التكامل صار أصعب). ساعتها ارجع للسؤال اللي بعده في الشجرة.'))
    body = (p(rich('كل سؤال تكامل أو مشتقة: امشِ على الأسئلة الأربعة بالترتيب، ووقّف عند أول «إيه». هذي أهم صفحة في المذكرة.'))
            + '<div class="tree">' + qs + '</div>' + rule
            + part('📐 الجدول الأساسي (تحفظه)', basic, 'p-steps')
            + part('👯 12 زوج يتشابهون: والسؤال اللي يفرّقهم', p(rich('غطِّ عمود الطريقة، وقرّر أنت أول.'))
                   + table(['السؤال', 'الطريقة', 'شبيهه', 'الطريقة', 'اللي يفرّق'], prow, 'twins'), 'p-pairs'))
    return chapter('tree', '🌳 الشجرة: أي طريقة؟', body, 'method mT')


# ================================================================ first page of each method
def method_map(m):
    rows = [[link(uid, '%d. %s' % (num, title)),
             rich(K.GIST[uid][2]) if uid in K.GIST else '', rich(K.GIST[uid][3]) if uid in K.GIST else '',
             str(K.FIRE.get(uid, 0) or '—'), pgref(uid)]
            for uid, num, title in K.CASES if K.METHOD_OF.get(uid) == m]
    return table(['الحالة', 'إذا شفت', 'أول خطوة', '🔥', 'ص'], rows, 'map')


MANUAL = {'acot(u)': (r"\frac{d}{dx}\,\cot^{-1}u = -\frac{u'}{1+u^{2}}",
                      [('diff(atan(1/x),x)', '-1/(1+x**2)', 't')]),
          'acsc(u)': (r"\frac{d}{dx}\,\csc^{-1}u = -\frac{u'}{u\sqrt{u^{2}-1}}",
                      [('diff(asin(1/x),x)', '-1/(x*sqrt(x**2-1))', '1+t')])}


def intro_A():
    ex = ('<ol class="script-ex">'
          + '<li>' + rich('الدالة اللي برّا: $\\sinh^{-1}$، وداخلها 🔵 $3x$.') + '</li>'
          + '<li>' + rich('مشتقتها من الجدول، والداخل يبقى: ') + M(r'\frac{1}{\sqrt{\cU{(3x)}^{2}+1}}', [('1/sqrt((3*x)**2+1)', '1/sqrt(9*x**2+1)')], 'A ex 2') + '</li>'
          + '<li>' + rich('🟢 × مشتقة الداخل ($3$): ') + M(r'\frac{1}{\sqrt{(3x)^{2}+1}}\cdot\cD{3}', [('diff(asinh(3*x),x)', '3/sqrt((3*x)**2+1)')], 'A ex 3') + '</li>'
          + '<li>' + rich('بسّط: ') + M(r"y'=\frac{3}{\sqrt{9x^{2}+1}}", [('diff(asinh(3*x),x)', '3/sqrt(9*x**2+1)')], 'A ex 4') + '</li></ol>')
    fam = [('sinh', 'cosh(u)', 'asinh(u)', '1/sqrt(u**2+1)', 'asin(u)', '1/sqrt(1-u**2)', ('t', '-t'), ('t/(1+t)',)),
           ('cosh', 'sinh(u)', 'acosh(u)', '1/sqrt(u**2-1)', 'acos(u)', '-1/sqrt(1-u**2)', ('1+t',), ('t/(1+t)',)),
           ('tanh', 'sech(u)**2', 'atanh(u)', '1/(1-u**2)', 'atan(u)', '1/(1+u**2)', ('t/(1+t)',), ('t',)),
           ('coth', '-csch(u)**2', 'acoth(u)', None, 'acot(u)', '-1/(1+u**2)', ('1+t',), ('t',)),
           ('sech', '-sech(u)*tanh(u)', 'asech(u)', '-1/(u*sqrt(1-u**2))', 'asec(u)', '1/(u*sqrt(u**2-1))', ('t/(1+t)',), ('1+t',)),
           ('csch', '-csch(u)*coth(u)', 'acsch(u)', '-1/(Abs(u)*sqrt(1+u**2))', 'acsc(u)', '-1/(u*sqrt(u**2-1))', ('t',), ('1+t',))]
    rows = []
    from booklet import doctor_coth
    for name, d1, f2, d2, f3, d3, b2, b3 in fam:
        c1 = F(name + '(u)', d1, 'diff', uprime=True, branches=('t',), label='A fam ' + name)
        c2 = (mi(r'\displaystyle \frac{d}{dx}\,\coth^{-1}u = ' + doctor_coth('diff')) + ' ✎' if d2 is None
              else F(f2, d2, 'diff', uprime=True, branches=b2, label='A fam inv ' + name))
        if f3 in MANUAL:                # SymPy's checker cannot differentiate acot/acsc after a branch substitution
            lat, claims = MANUAL[f3]
            c3 = M(lat, claims, 'A fam trig ' + name)
        else:
            c3 = F(f3, d3, 'diff', uprime=True, branches=b3, label='A fam trig ' + name)
        rows.append([c1, c2, c3])
    table3 = table(['4.1 الدالة نفسها', '4.2 المعكوس الزائدي', '3.4 المعكوس المثلثي'], rows, 'fam3')
    how = table(['تشوف', 'وش هو', 'أول سطر'], [
        [mi(r'y=\sinh(3x)'), 'دالة عادية (4.1)', M(r"y'=\cosh(3x)\cdot\cD{3}", [('diff(sinh(3*x),x)', '3*cosh(3*x)')], 'A how 1')],
        [mi(r'y=\sinh^{-1}(3x)'), 'معكوس (4.2): جدول العمود الثاني', M(r"y'=\frac{\cD{3}}{\sqrt{9x^{2}+1}}", [('diff(asinh(3*x),x)', '3/sqrt(9*x**2+1)')], 'A how 2')],
        [mi(r'y=2^{x^{2}}'), 'الأساس رقم، والأس فيه $x$: $a^u$', M(r"y'=2^{x^{2}}\ln2\cdot\cD{2x}", [('diff(2**(x**2),x)', '2**(x**2)*log(2)*2*x')], 'A how 3')],
        [mi(r'y=(x^{2}+1)^{5}'), 'الأس رقم: قاعدة القوة', M(r"y'=5(x^{2}+1)^{4}\cdot\cD{2x}", [('diff((x**2+1)**5,x)', '5*(x**2+1)**4*2*x')], 'A how 4')],
        [mi(r'y=x^{\sin x}'), 'الأساس <b>والأس</b> فيهم $x$ ← الاشتقاق اللوغاريتمي', M(r'\ln y=\sin x\,\ln x', [('log(x**sin(x))', 'sin(x)*log(x)', 't')], 'A how 5')]], 'contrast')
    body = (p(rich('السؤال يقول <b>Find dy/dx</b>. هنا ما فيه قرار صعب: كل المشتقات بنفس السكربت. '
                   'الغلطة الأشهر نسيان 🟢 مشتقة الداخل، فلها سطر لحالها.'))
            + part('🪜 السكربت (نفس الكلمات في كل مشتقة)', script_html('A')
                   + p(rich('<b>مثال:</b> $y=\\sinh^{-1}(3x)$')) + ex, 'p-steps')
            + part('📐 جدول واحد بثلاثة أعمدة: نفس الاسم في ثلاث دروس', table3
                   + p(rich("كل صف فيه 🟢 $u'$. والعمود الثاني والثالث يتشابهون: لاحظ الجذر وإشارته. "
                            "صف $\\coth^{-1}$ ✎ بإشارة دكتورك."), 'small'), 'p-steps')
            + part('🔀 كيف تفرّق', how)
            + part('🗺️ حالات الطريقة أ', method_map('A')))
    return chapter('sA', 'أ. الاشتقاق', body, 'method mA')


def intro_B():
    ex = ('<ol class="script-ex">'
          + '<li>' + rich('🔵 الداخل $x^2$: ') + M(r'\cU{u=x^{2}}', [], 'B ex 1') + '</li>'
          + '<li>' + rich('🟢 اشتقه: ') + M(r'\cD{du=2x\,dx}', [('diff(x**2,x)', '2*x')], 'B ex 2') + '</li>'
          + '<li>' + rich('🟠 اللي برّا $x$، مقسوم على مشتقة الداخل $2x$: ') + M(r'\frac{x}{2x}=\cA{\frac12}', [('x/(2*x)', 'Rational(1,2)')], 'B ex 3')
          + rich(' رقم، يعني تعويض. ويطلع قدّام التكامل <b>مرة وحدة</b>.') + '</li>'
          + '<li>' + rich('كله بـ $u$: ') + M(r'\int x\cosh(x^{2})\,dx=\cA{\frac12}\int\cosh u\,du=\frac12\sinh u',
                                               [('diff(sinh(x**2)/2,x)', 'x*cosh(x**2)')], 'B ex 4') + '</li>'
          + '<li>' + rich('رجّع $x$: ') + M(r'=\frac12\sinh(x^{2})+C', [('diff(sinh(x**2)/2,x)', 'x*cosh(x**2)')], 'B ex 5') + '</li></ol>')
    test = table(['السؤال', 'اللي برّا ÷ مشتقة الداخل', 'النتيجة'], [
        [mi(r'\int x\cosh(x^{2})\,dx'), M(r'\frac{x}{2x}=\cA{\frac12}', [('x/(2*x)', 'Rational(1,2)')], 'B t1'), 'رقم ← تعويض'],
        [mi(r'\int x^{2}e^{x^{3}}\,dx'), M(r'\frac{x^{2}}{3x^{2}}=\cA{\frac13}', [('x**2/(3*x**2)', 'Rational(1,3)')], 'B t2'), 'رقم ← تعويض'],
        [mi(r'\int\frac{e^{x}}{\sqrt{e^{2x}-16}}\,dx'), M(r'\frac{e^{x}}{e^{x}}=\cA{1}', [('exp(x)/exp(x)', '1')], 'B t3'), 'رقم ← تعويض (قانون 4.2)'],
        [mi(r'\int x\cosh x\,dx'), M(r'\frac{x}{1}=\cR{x}', [], 'B t4'), 'فيه $x$ ← مو تعويض (ج. التجزئة)'],
        [mi(r'\int x^{3}\cosh(x^{2})\,dx'), M(r'\frac{x^{3}}{2x}=\cR{\frac{x^{2}}{2}}', [('x**3/(2*x)', 'x**2/2')], 'B t5'),
         'فيه $x$ ← تعويض ثم تجزئة (أو $x^2=u$)']], 'contrast')
    wrong = (D(r'\int\frac{x\,dx}{x^{2}+1}:\quad \cU{u=x^{2}+1},\ \ \cD{du=2x\,dx}', [('diff(x**2+1,x)', '2*x')], 'B wrong 1')
             + p(rich('🔴 <b>غلط:</b> $\\frac12\\int\\frac{du}{2u}=\\frac14\\ln|u|$. قسمنا على 2 <b>مرتين</b>: مرة برّا، ومرة داخل.'))
             + p(rich('✓ <b>صح:</b> ') + M(r'\cA{\frac12}\int\frac{du}{u}=\frac12\ln(x^{2}+1)+C', [('diff(log(x**2+1)/2,x)', 'x/(x**2+1)')], 'B wrong 2')))
    body = (p(rich('السؤال تكامل، وفيه <b>دالة ومشتقتها</b>، أو شكله قانون جاهز بعد ما تسمّي الداخل. '
                   'هذي أكثر طريقة في الكويز: تكاملات 4.2 كلها، وتكاملات 5.2 بعد ما تحجز.'))
            + part('🪜 السكربت (نفس الكلمات في كل تعويض)', script_html('B') + p(rich('<b>مثال:</b> $\\int x\\cosh(x^{2})\\,dx$')) + ex, 'p-steps')
            + part('🧪 اختبار اللي برّا (يحسم الشك)', p(rich('اللي برّا الدالة (مثل $x$ قدّام cosh) لا تخاف منه. <b>اقسمه على مشتقة الداخل</b>:'))
                   + test)
            + part('🔴 رقم التعديل مرة وحدة بس', wrong)
            + part('🔀 كيف تفرّق: تعويض أم تجزئة؟', p(rich('السؤال اللي يحسم: «اقسم اللي برّا على مشتقة الداخل. طلع رقم؟ تعويض. '
                                                           'طلع فيه $x$؟ تجزئة». والأزواج كاملة في ') + link('tree', 'الشجرة') + '.'))
            + part('🗺️ حالات الطريقة ب', method_map('B')))
    return chapter('sB', 'ب. التعويض', body, 'method mB')


PREPS = [
    ('كمّل المربع', '$x^2$ و $x$ تحت الجذر (أو تحت الكسر)', '$x^2+6x+5=(x+3)^2-4$', 'س2: قانون 4.2 أو 3.4', ['U-I8', 'U-I9']),
    ('افصل الكسر', 'البسط فيه جمع: $\\frac{x+3}{\\ldots}$', 'كسرين، وكل كسر طريقته', 'س2 لكل كسر', ['U-I6']),
    ('اضرب فوق وتحت', 'أسية أو قوة $x$ تحت الجذر، وما فيه شي برّا يكمّلها', 'اضرب في جذرها، فتطلع مشتقتها فوق', 'س2: قانون 4.2', ['U-I4', 'U-I3']),
    ('نص الزاوية', '$\\sin^2x$ أو $\\cos^2x$ لحالها، أو الاثنين زوجي', '$\\sin^2x=\\frac{1-\\cos2x}{2}$', 'س2: جدول', ['U-T3']),
    ('الضرب إلى جمع', 'زاويتين مختلفتين: $\\sin5x\\cos2x$', 'المجموع والفرق', 'س2: جدول', ['U-T8']),
    ('اكسر tan', '$\\tan^nx$ لحالها', '$\\tan^2x=\\sec^2x-1$', 'س2: تعويض $u=\\tan x$', ['U-T6']),
    ('sinh أو cosh بالأسس', 'sinh أو cosh مضروبة في $e^{x}$', '$\\sinh x=\\frac{e^x-e^{-x}}{2}$، ثم وزّع', 'س2: جدول الأسية', ['U-P9']),
    ('$x^2=u-a$', '$x^3$ (أو $x^5$) فوق $x^2+a$', 'سمّ $u=x^2+a$، واكتب الباقي $x^2=u-a$', 'س2: تعويض', ['U-X2']),
    ('خواص ln أول', 'ln لقوة أو جذر: $\\ln x^2$، $\\ln\\sqrt[3]x$', '$\\ln\\sqrt[3]x=\\frac13\\ln x$', 'س2: تعويض $u=\\ln x$', ['U-LN']),
    ('cosh في المقام بالأسس', 'cosh أو sinh تحت الكسر', 'اكتبها بالأسس، واضرب فوق وتحت في $e^x$', 'س2: $u=e^x$', ['U-CH'])]


def intro_P():
    arith('', [('x**2+6*x+5', '(x+3)**2-4'), ('sin(x)**2', '(1-cos(2*x))/2'), ('tan(x)**2', 'sec(x)**2-1'),
               ('sinh(x)', '(exp(x)-exp(-x))/2'), ('log(x**Rational(1,3))', 'log(x)/3', 't')], 'preps table')
    rows = [[rich('<b>%s</b>' % name), rich(sign), rich(move), rich(back),
             '، '.join(link(u, str(K.NUM[u])) + ' (ص ' + pgref(u) + ')' for u in uids if u in K.NUM) or '—']
            for name, sign, move, back, uids in PREPS]
    body = (p(rich('التكامل ما يطابق قانون، وما فيه دالة ومشتقتها، بس فيه <b>علامة</b>. التجهيز حركة جبر تغيّر الشكل '
                   'بدون ما تغيّر القيمة. بعدها ترجع لـ س2 في الشجرة، وغالبًا يصير قانون أو تعويض.'))
            + part('🪜 السكربت (نفس الكلمات في كل تجهيز)', script_html('P'), 'p-steps')
            + part('🔧 التجهيزات العشر: العلامة ← الحركة ← وين ترجع', table(['التجهيز', 'العلامة', 'الحركة', 'بعدها', 'الحالة'], rows, 'preps')
                   + p(rich('🔢 «تأكد برقم» يعني: عوّض $x=1$ في الشكل القديم والجديد. لازم يطلعون نفس الرقم.'), 'small'))
            + part('🗺️ حالات التجهيزات', method_map('P')))
    return chapter('sP', '🔧 التجهيزات: غيّر الشكل، ثم ارجع للشجرة', body, 'method mP')


def intro_C():
    ex = ('<ol class="script-ex">'
          + '<li>' + rich('LIATE: $x$ (A) قبل $e^{3x}$ (E)، فـ 🔵 $u=x$.') + '</li>'
          + '<li>' + rich('المربع:') + D(r'\cU{u=x}\qquad dv=e^{3x}dx\\ \cD{du=dx}\qquad v=\frac{e^{3x}}{3}',
                                           [('diff(x,x)', '1'), ('diff(exp(3*x)/3,x)', 'exp(3*x)')], 'C ex box') + '</li>'
          + '<li>' + rich('القانون: ') + M(r'I=\frac{x\,e^{3x}}{3}-\int\frac{e^{3x}}{3}\,dx', [], 'C ex law') + '</li>'
          + '<li>' + rich('كمّل: ') + M(r'I=\frac{x\,e^{3x}}{3}-\frac{e^{3x}}{9}+C', [('diff(x*exp(3*x)/3-exp(3*x)/9,x)', 'x*exp(3*x)')], 'C ex end') + '</li></ol>')
    dv = table(['$dv$', '$v$ (تكامله)', 'انتبه'], [
        [mi(r'e^{kx}\,dx'), M(r'\frac{e^{kx}}{k}', [('diff(exp(-2*x)/(-2),x)', 'exp(-2*x)')], 'dv exp'), 'مع $e^{-2x}$: اقسم على $\\cR{-2}$'],
        [mi(r'\sin kx\,dx'), M(r'\cR{-}\frac{\cos kx}{k}', [('diff(-cos(3*x)/3,x)', 'sin(3*x)')], 'dv sin'), '🔴 السالب'],
        [mi(r'\cos kx\,dx'), M(r'\frac{\sin kx}{k}', [('diff(sin(3*x)/3,x)', 'cos(3*x)')], 'dv cos'), ''],
        [mi(r'\sinh kx\,dx'), M(r'\frac{\cosh kx}{k}', [('diff(cosh(3*x)/3,x)', 'sinh(3*x)')], 'dv sinh'), 'بدون سالب'],
        [mi(r'\cosh kx\,dx'), M(r'\frac{\sinh kx}{k}', [('diff(sinh(3*x)/3,x)', 'cosh(3*x)')], 'dv cosh'), ''],
        [mi(r'\sec^{2}x\,dx'), M(r'\tan x', [('diff(tan(x),x)', 'sec(x)**2')], 'dv sec2'), ''],
        [mi(r'\sec x\tan x\,dx'), M(r'\sec x', [('diff(sec(x),x)', 'sec(x)*tan(x)')], 'dv sectan'), ''],
        [mi(r'\csc^{2}x\,dx'), M(r'\cR{-}\cot x', [('diff(-cot(x),x)', 'csc(x)**2')], 'dv csc2'), '🔴 السالب'],
        [mi(r'\csc x\cot x\,dx'), M(r'\cR{-}\csc x', [('diff(-csc(x),x)', 'csc(x)*cot(x)')], 'dv csccot'), '🔴 السالب'],
        [mi(r'x^{n}\,dx'), M(r'\frac{x^{n+1}}{n+1}', [('diff(x**4/4,x)', 'x**3')], 'dv pow'), 'مع ln: $x^n$ هي $dv$ دايم'],
        [mi(r'dx'), M('x', [('diff(x,x)', '1')], 'dv one'), 'ln لحالها أو دالة عكسية لحالها']], 'dvtab')
    definite = (p(rich('<b>المحدد:</b> احسب التكامل <b>كامل</b> بدون حدود، ثم عوّض الحدّين <b>مرة وحدة</b> في الآخر: '
                       '(فوق) ناقص (تحت). كذا ما تضيع حدود في نص الحل. والقيم في ') + link('s0', 'جدول قيم المثلثات') + '.')
                + D(r'\int_{0}^{1}x\,e^{3x}dx=\left[\frac{x\,e^{3x}}{3}-\frac{e^{3x}}{9}\right]_{0}^{1}=\left(\frac{e^{3}}{3}-\frac{e^{3}}{9}\right)-\left(0-\frac19\right)=\frac{2e^{3}+1}{9}',
                    [('integrate(x*exp(3*x),(x,0,1))', '(2*exp(3)+1)/9'), ('(exp(3)/3-exp(3)/9)-(0-Rational(1,9))', '(2*exp(3)+1)/9')], 'C definite'))
    di = p(rich('<b>جدول DI</b> (إذا $u$ قوة 2 أو 3): اكتب عمود الإشارات 🔴 $+\\ -\\ +\\ -$ <b>أول</b>، بعدين D تنزل للصفر، و I تتكامل، '
                'واضرب مايل. الشرح كامل في حالته.'))
    body = (p(rich('ضرب نوعين مختلفين، أو $\\ln$ أو دالة عكسية لحالها. ما فيه دالة ومشتقتها (اختبار اللي برّا طلع فيه $x$). '
                   'الفكرة: نشتق واحد يسهل (🔵 $u$)، ونكامل الثاني ($dv$).'))
            + part('🪜 السكربت (نفس الكلمات في كل تجزئة)', script_html('C') + p(rich('<b>مثال:</b> $\\int x\\,e^{3x}\\,dx$')) + ex, 'p-steps')
            + part('🧭 LIATE: مين يصير $u$؟', p(rich('اللي يجي أول في الكلمة هو 🔵 $u$: <b>L</b> ln، ثم <b>I</b> دالة عكسية، ثم <b>A</b> $x$ وقواها، '
                                                     'ثم <b>T</b> sin و cos، ثم <b>E</b> $e^x$. والباقي كله $dv$.')))
            + part('📐 جدول $dv$ ← $v$', dv, 'p-steps') + part('🔁 لما تتكرر', di) + part('📏 التكامل المحدد', definite)
            + part('🗺️ حالات الطريقة ج', method_map('C')))
    return chapter('sC', 'ج. التجزئة', body, 'method mC')


def intro_D():
    blanks = lambda n: lines(n, 'write tight')
    memory = (p(rich('آخر خطوة: <b>من ذاكرتك</b>، بدون ما تقلب. اكتب، وبعدين صحّح من الصفحات. اللي نسيته ارجع له.'))
              + '<h3>الشجرة: الأسئلة الأربعة</h3>' + blanks(4)
              + '<h3>السكربتات الأربعة</h3>' + ''.join('<p><b>%s %s:</b></p>%s' % (K.METHODS[m][0], K.METHODS[m][1], blanks(2)) for m in 'ABPC')
              + '<h3>صف $\\coth^{-1}$ عند دكتورك، و $\\int a^u\\,du$</h3>' + blanks(2))
    body = (p(rich('في الكويز الأسئلة مخلوطة وبدون عناوين. هنا تتدرب على <b>القرار</b>: وش الطريقة؟ ووش أول سطر؟ '
                   'ثلاث صفحات «وش الحالة؟» (بدون حل)، ثم مراجعة مخلوطة تحلها كاملة، ثم صفحة من ذاكرتك.'))
            + part('🧠 من ذاكرتك', memory))
    return chapter('sD', 'د. التمييز والتذكر', body, 'method mD')


# ================================================================ full mark, and «your answer differs from the key»
def fullmark():
    must = ul([rich('سطر 🔵 $u=\\ldots$ و 🟢 $du=\\ldots$ (أو مربع التجزئة كامل: $u$ و $dv$ و $du$ و $v$). هذا عليه درجة لحاله.'),
               rich('التكامل بعد التعويض مكتوب كله بـ $u$، قبل الجواب.'),
               rich('الجواب بـ $x$ (رجّع $u$)، و <b>$+C$</b> في كل تكامل غير محدد.'),
               rich('$\\ln|u|$ بالقيمة المطلقة، و $|u|$ في $\\operatorname{csch}^{-1}$ و $\\operatorname{sech}^{-1}$ مثل الجدول.'),
               rich("في المشتقة: $y'=$، والمشتقة كاملة بكل حد. حد نسيته = درجة ناقصة."),
               rich('في المحدد: الحدود مكتوبة، والتعويض (فوق ناقص تحت) ظاهر.'),
               rich('$\\coth^{-1}$: بإشارة دكتورك ✎ (سالبة).')])
    not_needed = ul([rich('<b>التبسيط الأخير ما يلزم.</b> المفاتيح الرسمية تقبل مثلًا $\\frac{\\cos x}{1-\\sin^{2}x}$ بدون ما تكتبها $\\sec x$.'),
                     rich('ترتيب الحدود، وشكل الثابت ($\\frac12x^2+C$ أو $\\frac12(x^2+1)+C$ نفس الشي).'),
                     rich('الكلام والشرح بالعربي: يكفي السطور الرياضية.'),
                     rich('تكتب $\\tanh^{-1}$ أو صيغة ln: الاثنين صح إذا الحساب صح.')])
    arith('', [('cos(x)/(1-sin(x)**2)', 'sec(x)')], 'fullmark unsimplified')
    plan = table(['قبل ما تسلّم', 'شيّك'], [
        ['$+C$', 'في كل تكامل غير محدد'], ['الإشارات', '🔴 sin و csc و cot و sech و csch، والسالب قدّام القوس'],
        ['رقم التعديل', '🟠 مرة وحدة بس'], ['المشتقة', '🟢 مضروبة في مشتقة الداخل؟'], ['تكامل جواب واحد على الأقل', 'اشتقه: يرجع السؤال؟']], 'compact')
    body = (part('✅ لازم ينكتب (عليه درجات)', must) + part('➖ ما يلزم (لا تضيّع وقتك فيه)', not_needed)
            + part('✔ قبل التسليم', rich(plan)))
    return chapter('fullmark', '💯 ورقة الدرجة الكاملة', body, 'flow')


def differs():
    rows = [
        ('ثابت يختفي', r'\tfrac12(x^{2}+1)+C', r'\tfrac12x^{2}+C', 'الفرق $\\frac12$ رقم، ويدخل في $C$',
         [('diff((x**2+1)/2,x)', 'diff(x**2/2,x)')]),
        ('ln أو المعكوس الزائدي', r'\tanh^{-1}x', r'\tfrac12\ln\frac{1+x}{1-x}', 'نفس الدالة (صيغتها بـ ln)',
         [('diff(atanh(x),x)', 'diff(log((1+x)/(1-x))/2,x)', 't/(1+t)')]),
        ('sinh⁻¹ أو ln', r'\sinh^{-1}\frac{x}{3}', r'\ln\left(x+\sqrt{x^{2}+9}\right)', 'يختلفون بـ $\\ln3$ (ثابت)',
         [('diff(asinh(x/3),x)', 'diff(log(x+sqrt(x**2+9)),x)')]),
        ('sin² أو cos²', r'\tfrac12\sin^{2}x', r'-\tfrac12\cos^{2}x', 'الفرق $\\frac12$ (لأن $\\sin^2+\\cos^2=1$)',
         [('diff(sin(x)**2/2,x)', 'diff(-cos(x)**2/2,x)')]),
        ('tan² أو sec²', r'\tfrac12\tan^{2}x', r'\tfrac12\sec^{2}x', 'الفرق $\\frac12$', [('diff(tan(x)**2/2,x)', 'diff(sec(x)**2/2,x)')]),
        ('ln|sec| أو −ln|cos|', r'\ln|\sec x|', r'-\ln|\cos x|', 'نفس الشي بالضبط', [('diff(log(sec(x)),x)', 'diff(-log(cos(x)),x)', 't/(1+t)')]),
        ('نص الزاوية', r'\tfrac{x}{2}-\tfrac{\sin2x}{4}', r'\tfrac12(x-\sin x\cos x)', 'نفس الشي ($\\sin2x=2\\sin x\\cos x$)',
         [('x/2-sin(2*x)/4', '(x-sin(x)*cos(x))/2')]),
        ('بدون تبسيط', r'\frac{\cos x}{1-\sin^{2}x}', r'\sec x', 'نفس الشي، والمفتاح يقبل الاثنين', [('cos(x)/(1-sin(x)**2)', 'sec(x)')])]
    trs = [[rich(n), M(a, [], 'differs a %d' % k), M(b, c, 'differs %d' % k), rich(w)] for k, (n, a, b, w, c) in enumerate(rows, 1)]
    how = ul([rich('<b>اشتق جوابك.</b> إذا رجع السؤال، فجوابك صح حتى لو شكله غير (قد يختلف بثابت).'),
              rich('<b>أو عوّض رقمين</b> (مثل $x=1$ و $x=2$) في جوابك وجواب المفتاح: إذا الفرق نفسه في الاثنين، فالفرق ثابت وجوابك صح.'),
              rich('✎ <b>$\\coth^{-1}$:</b> لو المفتاح موجب وأنت سالب (أو بالعكس)، هذا اختلاف الإشارة بين دكتورك والرياضيات. اكتب مثل دكتورك.'),
              rich('<b>$|u|$:</b> بعض المفاتيح تحذف القيمة المطلقة. اكتبها أنت، ما تضرك.')])
    body = (p(rich('جوابك غير شكل عن المفتاح؟ <b>مو شرط إنه غلط.</b> هذي أشهر الأشكال اللي تختلف وهي نفس الجواب. '
                   'كل صف فحصه الحاسوب: مشتقة الشكلين واحدة.'))
            + table(['الحالة', 'شكل', 'شكل ثاني', 'ليش نفس الجواب'], trs, 'differs') + part('🔍 كيف تتأكد بنفسك', how))
    return chapter('differs', '🤔 جوابك يختلف عن المفتاح؟', body, 'flow')


# ================================================================ section د: fix the mistake, mastery checks
FIXES = [  # (question, the wrong work, where it went wrong, the right line, wrong claim that must fail, right claims)
    (r'\int5\,dx', r'=0', 'تكامل الثابت مو صفر. الصفر هو <b>مشتقة</b> الثابت 🔴.', r'\int5\,dx=5x+C',
     ('diff(0,x)', '5'), [('diff(5*x,x)', '5')]),
    (r'\int\frac{x}{x^{2}+1}\,dx', r'\cU{u=x^{2}+1},\ \cD{du=2x\,dx}:\quad \frac12\int\frac{du}{2u}=\frac14\ln|u|',
     'قسمنا على 2 <b>مرتين</b>: مرة برّا ومرة داخل 🟠. رقم التعديل مرة وحدة.', r'\frac12\int\frac{du}{u}=\frac12\ln(x^{2}+1)+C',
     ('diff(log(x**2+1)/4,x)', 'x/(x**2+1)'), [('diff(log(x**2+1)/2,x)', 'x/(x**2+1)')]),
    (r"y=\sinh^{-1}(3x)", r"y'=\frac{1}{\sqrt{9x^{2}+1}}", 'نسينا 🟢 مشتقة الداخل (3).', r"y'=\frac{3}{\sqrt{9x^{2}+1}}",
     ('diff(asinh(3*x),x)', '1/sqrt(9*x**2+1)'), [('diff(asinh(3*x),x)', '3/sqrt(9*x**2+1)')]),
    (r'\int x^{2}e^{x}\,dx', r'=x^{2}e^{x}+2xe^{x}+2e^{x}', 'إشارات DI لازم تتبادل 🔴 $+\\ -\\ +$: الحد الثاني سالب.',
     r'=x^{2}e^{x}-2xe^{x}+2e^{x}+C', ('diff(x**2*exp(x)+2*x*exp(x)+2*exp(x),x)', 'x**2*exp(x)'),
     [('diff(x**2*exp(x)-2*x*exp(x)+2*exp(x),x)', 'x**2*exp(x)')]),
    (r"y=\sinh^{-1}x", r"y'=-\operatorname{csch}x\coth x", 'هذي مشتقة <b>المقلوب</b> $\\frac1{\\sinh x}$، مو المعكوس.',
     r"y'=\frac{1}{\sqrt{x^{2}+1}}", ('diff(asinh(x),x)', '-csch(x)*coth(x)'), [('diff(asinh(x),x)', '1/sqrt(x**2+1)')]),
    (r'\int\ln x\,dx', r'=\frac1x', '$\\frac1x$ <b>مشتقة</b> ln، مو تكاملها. ln لحالها: تجزئة.', r'=x\ln x-x+C',
     ('diff(1/x,x)', 'log(x)'), [('diff(x*log(x)-x,x)', 'log(x)', 't')]),
    (r'\int_{0}^{1}x\,e^{x}\,dx', r'=\left[xe^{x}-e^{x}\right]_{0}^{1}=(e-e)-(0-0)=0', '$e^0=1$ مو صفر. الحد التحتي $(0-1)$.',
     r'=(e-e)-(0-1)=1', ('0', '1'), [('integrate(x*exp(x),(x,0,1))', '1'), ('(E-E)-(0-1)', '1')]),
    (r'\int\frac{dx}{x^{2}+4}', r'=\int\frac{dx}{x^{2}}+\int\frac{dx}{4}', 'المقام <b>ما ينفصل</b>. نفصل البسط بس.',
     r'=\frac12\tan^{-1}\frac{x}{2}+C', ('1/(x**2+4)', '1/x**2+Rational(1,4)'), [('diff(atan(x/2)/2,x)', '1/(x**2+4)')]),
    (r'\int\sin3x\,dx', r'=\frac{\cos3x}{3}', 'تكامل sin فيه سالب 🔴.', r'=-\frac{\cos3x}{3}+C',
     ('diff(cos(3*x)/3,x)', 'sin(3*x)'), [('diff(-cos(3*x)/3,x)', 'sin(3*x)')]),
    (r'\int e^{2x}\,dx', r'=2e^{2x}', 'ضربنا في 2 بدل ما نقسم. في التكامل نقسم على رقم $x$.', r'=\frac{e^{2x}}{2}+C',
     ('diff(2*exp(2*x),x)', 'exp(2*x)'), [('diff(exp(2*x)/2,x)', 'exp(2*x)')])]


def fix_mistakes():
    from guide_end import differs
    rows = ''
    for k, (q, wrong, why, right, (wl, wr), claims) in enumerate(FIXES, 1):
        differs(wl, wr, 'fix %d' % k)
        rows += ('<div class="fix"><b>%d.</b> %s %s<div class="fixq">🔍 وين الغلط؟</div>%s</div>'
                 % (k, M(q, [], 'fix q %d' % k), M(r'\cR{' + wrong + '}', [], 'fix w %d' % k),
                    '<div class="fixa">' + p('<b>الجواب:</b> ' + rich(why)) + M(right, claims, 'fix r %d' % k) + '</div>'))
    return chapter('fixit', '🔍 صحّح الغلط', p(rich('هذي غلطاتك أنت (من جلساتك). غطِّ «الجواب» وحاول تلقى الغلط أول. '
                                                   'كل «غلط» تأكد الحاسوب إنه غلط فعلًا، وكل «صح» إنه صح.')) + rows, 'flow')


MASTERY_KEYS = []


# checked questions from Dr. Tariq's and Dr. Musa's notes that the guide does not use elsewhere: (case, item), by method
MASTERY_FILL = {
    'A': [('U-D1', 'N42-X1-5'), ('U-D2', 'M-06'), ('U-D1', 'N42-E1-3'), ('U-D2', 'M-28')],
    'B': [('U-I3', 'N42-X2-04'), ('U-T2', 'N52-X03'), ('U-T7', 'N52-E4-1'), ('U-I1', 'N42-X2-01'), ('U-T2', 'N52-X02')],
    'P': [('U-T3', 'N52-E1-3'), ('U-T8', 'N52-E5-2')],
    'C': [('U-P3', 'N51-X06'), ('U-P6', 'N51-X08'), ('U-T6', 'N52-E3-1')]}


def mastery():
    """Five unlabelled questions per method from past exams that did not fit in their case; answers in the keys."""
    from booklet import final as _fin, source_label
    from booklet_engine import BLOCKED, ITEMS, USED, ans_tex, q_tex, use
    out = p(rich('<b>فحص الإتقان:</b> بدون عناوين، مثل الكويز. حل الخمسة لحالك. <b>4 من 5 صح</b>؟ كمّل. '
                 'أقل؟ ارجع لحالة اللي غلطت فيه (رقمها في المفاتيح) وحل تمرينها الأخير.'))
    for m in 'ABPC':
        order = {'exam': 0, 'musa': 1, 'generated': 3}
        pool = sorted([(uid, i) for uid, i in K.EXTRA if K.METHOD_OF.get(uid) == m],
                      key=lambda c: order.get(ITEMS[c[1]]['kind'], 2))
        picks, seen = [], set()
        for uid, i in pool:              # one question per case first, so the check covers the method
            if uid not in seen and len(picks) < 5:
                picks.append((uid, i)); seen.add(uid)
        for c in pool:
            if c not in picks and len(picks) < 5:
                picks.append(c)
        for uid, i in MASTERY_FILL.get(m, []):     # still short: questions from the notes not used anywhere in the guide
            if len(picks) < 5 and uid in K.NUM and i not in USED and i not in BLOCKED:
                picks.append((uid, i))
        if not picks:
            continue
        qs, keys = '', []
        for k, (uid, item_id) in enumerate(picks, 1):
            it = use(item_id, 'mastery %s' % m)
            qs += '<div class="ch"><b>%d</b>%s%s</div>' % (k, md(q_tex(it)), lines(1, 'write tight'))
            _fin(it, 'mastery %s' % m)
            keys.append([str(k), link(uid, 'الحالة %d' % K.NUM[uid]), mi(r'\displaystyle ' + ans_tex(it).lstrip('= ')),
                         source_label(it)])
        MASTERY_KEYS.append((m, keys))
        out += ('<h3 id="mastery-%s">✅ %s (%d أسئلة)</h3>' % (m, K.mname(m), len(picks))
                + '<div class="chgrid">' + qs + '</div>' + p('المفتاح: ' + link('k-mastery', 'ص ' + pgref('k-mastery')), 'small'))
    return chapter('mastery', '✅ فحوص الإتقان', out, 'flow')


def mastery_keys():
    out = ''
    for m, rows in MASTERY_KEYS:
        out += ('<h4>%s</h4>' % K.mname(m)
                + table(['#', 'الحالة', 'الجواب', 'المصدر'], rows, 'answers'))
    return '<h3 id="k-mastery">مفتاح فحوص الإتقان</h3>' + out if out else ''

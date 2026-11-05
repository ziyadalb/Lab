"""«odd و even»: تكاملات sin و cos بالأسس — ملف شرح كامل لدرس واحد (مذكرة د. موسى ص 93–97، ود. طارق ص 67–69).

The whole lesson is one question (is there an odd power?) and two branches. Worked examples with a «ليش؟» column,
then completion problems with blanks, then problems on your own, the five famous mistakes, ten mixed questions and
a key. Every equality, every step and every answer is checked with SymPy while building; a failed check stops it.
Questions come from Dr. Musa's and Dr. Tariq's notes and past exams; none from the doctor's lecture photos and none of
the mock exams' held questions (the leak check runs on the result).
"""
import sympy as sp

from booklet_engine import BuildError, arith
from guide_kit import rich
from html_kit import md, mi, p, table, ul
from mathlib import P, u, x

BLANK = r'\boxed{\phantom{00}}'


def chk(latex, claims, label):
    return arith(latex, claims, label)


def antideriv(F, f, label, branch=None):
    """The final answer F really is an antiderivative of f (checked as d/dx F = f)."""
    claim = ('diff(%s,x)' % F, f) + ((branch,) if branch else ())
    arith('', [claim], label + ' answer')


def steps(rows, label):
    """A worked example: (latex, claims, why); the last row is the answer."""
    body = ''
    for k, (latex, claims, why) in enumerate(rows, 1):
        chk(latex, claims, '%s step %d' % (label, k))
        cls = ' class="final"' if k == len(rows) else ''
        body += '<tr%s><td class="n">%d</td><td>%s</td><td>%s</td></tr>' % (cls, k, mi(r'\displaystyle ' + latex), rich(why))
    return ('<table class="steps"><thead><tr><th>#</th><th>الخطوة (تكتبها)</th><th>ليش؟ (لك أنت)</th></tr></thead>'
            '<tbody>' + body + '</tbody></table>')


def q(latex):
    return md(latex)


def section(id_, title, inner):
    return '<section class="chapter oe" id="%s"><h2>%s</h2>%s</section>' % (id_, title, inner)


def box(title, inner, cls=''):
    return '<div class="sbox %s"><h3>%s</h3>%s</div>' % (cls, rich(title), inner)


# ---------------------------------------------------------------- 1. the map, the plan, the tools
def page_map():
    rows = [['أس <b>sin</b> فردي (والثاني أي شي)', rich('احجز $\\sin x$، وحوّل الباقي لـ cos'), mi(r'u=\cos x,\ \ \sin x\,dx=\cR{-}du')],
            ['أس <b>cos</b> فردي', rich('احجز $\\cos x$، وحوّل الباقي لـ sin'), mi(r'u=\sin x,\ \ \cos x\,dx=du')],
            ['<b>الاثنين فرديين</b>', rich('احجز من <b>الأصغر</b> (أقل شغل). والثاني يمشي بعد'), '—'],
            ['<b>كلها زوجية</b> (والصفر زوجي)', rich('ما فيه شي تحجزه ← <b>نص الزاوية</b>'), 'ما فيه ' + mi('u')]]
    arith('', [('diff(cos(x),x)', '-sin(x)'), ('diff(sin(x),x)', 'cos(x)')], 'map du')
    tree = ('<div class="oe-q">' + rich('السؤال الوحيد: <b>فيه أس فردي؟</b>') + '</div>'
            + table(['تشوف', 'وش تسوي', 'التعويض'], rows, 'decide')
            + ul([rich('أنواع موسى الثلاثة (Odd و Odd، و Odd و Even، و Even و Even) هي هذا الجدول: الفردي يمشي بالحجز، والزوجي بنص الزاوية.'),
                  rich('$\\int\\sin^4x\\,dx$ هي $\\sin^4x\\cos^0x$: الصفر زوجي، فهي «كلها زوجية».'),
                  rich('أس كسري مثل $\\sqrt{\\sin x}$ ما يعتبر فردي ولا زوجي: احجز من الثاني (الفردي).')]))
    plan = ('<ol class="plan">' + ''.join('<li>%s</li>' % rich(t) for t in [
        '<b>الخريطة والأدوات</b> (هذي الصفحة واللي بعدها): غطِّها واكتبها من راسك. <b>10 دقايق.</b>',
        '<b>الأمثلة المحلولة</b>: غطِّ عمود «الخطوة»، واقرأ «ليش؟»، وتوقّع السطر قبل ما تكشفه. <b>25 دقيقة.</b>',
        '<b>الناقص ثم «لحالك»</b> في كل فرع، وصحّح من المفتاح. <b>30 دقيقة.</b>',
        '<b>صحّح الغلط</b>: لا تقرأ الجواب قبل ما تلقى الغلطة. <b>10 دقايق.</b>',
        '<b>المخلوطة</b>: أول سطر لكل الأسئلة العشرة أول (تدريب القرار)، ثم حلها كاملة. <b>40 دقيقة.</b>',
        '<b>يوم ثاني أو قبل الكويز</b>: المخلوطة مرة ثانية بدون ما تقلب. 8 من 10 صح = أتقنتها. أقل؟ ارجع للفرع اللي غلطت فيه.'])
            + '</ol>')
    return section('map', '🗺️ odd و even: الخريطة', p(rich('كل أسئلة الدرس شكلها $\\int\\sin^m x\\cos^n x\\,dx$. '
                                                         'وكلها تنحل بقرار واحد:')) + tree
                   + '<h3>📋 خطة الإتقان</h3>' + plan)


def page_tools():
    ident = chk(r'\sin^{2}x+\cos^{2}x=1\ \Rightarrow\ \sin^{2}x=1-\cos^{2}x,\quad \cos^{2}x=1-\sin^{2}x',
                [('sin(x)**2+cos(x)**2', '1'), ('sin(x)**2', '1-cos(x)**2'), ('cos(x)**2', '1-sin(x)**2')], 'tool pyth')
    half = chk(r'\sin^{2}x=\frac{1-\cos2x}{2}\qquad \cos^{2}x=\frac{1+\cos2x}{2}\qquad \sin x\cos x=\frac12\sin2x',
               [('sin(x)**2', '(1-cos(2*x))/2'), ('cos(x)**2', '(1+cos(2*x))/2'), ('sin(x)*cos(x)', 'sin(2*x)/2')], 'tool half')
    integ = chk(r'\int u^{n}\,du=\frac{u^{n+1}}{n+1}\qquad \int\cos kx\,dx=\frac{\sin kx}{k}\qquad \int\sin kx\,dx=-\frac{\cos kx}{k}',
                [('diff(x**6/6,x)', 'x**5'), ('diff(sin(4*x)/4,x)', 'cos(4*x)'), ('diff(-cos(4*x)/4,x)', 'sin(4*x)')], 'tool int')
    alg = chk(r'(1-u^{2})^{2}=1-2u^{2}+u^{4}\qquad (1-u^{2})^{3}=1-3u^{2}+3u^{4}-u^{6}\qquad u^{4}(1-u^{2})=u^{4}-u^{6}',
              [('(1-u**2)**2', '1-2*u**2+u**4'), ('(1-u**2)**3', '1-3*u**2+3*u**4-u**6'), ('u**4*(1-u**2)', 'u**4-u**6')], 'tool alg')
    numcheck = chk(r'u=2:\quad (1-4)^{2}=9,\qquad 1-8+16=9\ \checkmark', [('(1-4)**2', '9'), ('1-8+16', '9')], 'tool alg num')
    return section('tools', '🧰 الأدوات: 5 أسطر بس تحفظها',
                   box('١. المتطابقة (تحوّل الباقي)', md(ident))
                   + box('٢. المشتقات (تعطيك du)', md(chk(r"(\sin x)'=\cos x\qquad (\cos x)'=\cR{-}\sin x",
                                                         [('diff(sin(x),x)', 'cos(x)'), ('diff(cos(x),x)', '-sin(x)')], 'tool d'))
                         + p(rich('🔴 السالب مع cos هو أشهر غلطة في الدرس كله.'), 'small'))
                   + box('٣. نص الزاوية (للزوجي): «سين وسالب»، والزاوية تتضاعف', md(half))
                   + box('٤. التكامل', md(integ) + p(rich('مع $kx$ اقسم على $k$: $\\int\\cos2x\\,dx=\\frac{\\sin2x}{2}$.'), 'small'))
                   + box('٥. فك الأقواس (أكثر شي يغلّط)', md(alg)
                         + p(rich('تشك؟ عوّض رقم في الطرفين:'), 'small') + md(numcheck)))


# ---------------------------------------------------------------- 2. odd branch
ODD_STEPS = ['<b>احجز</b> وحدة من صاحب الأس الفردي ($\\sin x$ أو $\\cos x$). الاثنين فرديين؟ من الأصغر.',
             '<b>حوّل</b> الباقي (صار أسه زوجي) بالمتطابقة للدالة الثانية.',
             '<b>عوّض</b>: $u$ = الدالة الثانية، و $du$ = القطعة المحجوزة. 🔴 مع $u=\\cos x$: $\\sin x\\,dx=-du$.',
             '<b>فك القوس</b> ووزّع، ثم <b>كامل</b> كل حد: زد الأس 1 واقسم عليه.',
             '<b>رجّع</b> $x$، وحط $+C$. وتأكد: <b>أعلى أس في جوابك = مجموع الأسين</b>.']


def page_odd():
    e1 = steps([
        (r'\cos^{3}x=\cos^{2}x\cdot\cD{\cos x}', [('cos(x)**3', 'cos(x)**2*cos(x)')], 'أس cos فردي (3): نحجز $\\cos x$ وحدة، لأنها مشتقة $\\sin x$.'),
        (r'\cos^{2}x=1-\sin^{2}x', [('cos(x)**2', '1-sin(x)**2')], 'الباقي أسه زوجي: نحوّله لـ sin.'),
        (r'\cU{u=\sin x}\qquad \cD{du=\cos x\,dx}', [('diff(sin(x),x)', 'cos(x)')], 'الدالة الثانية هي $u$، ومشتقتها هي القطعة اللي حجزناها.'),
        (r'I=\int(1-\cU{u}^{2})\,\cD{du}=u-\frac{u^{3}}{3}', [('integrate(1-u**2,u)', 'u-u**3/3')], 'كل حد لحاله: زد الأس 1 واقسم عليه.'),
        (r'I=\sin x-\frac{\sin^{3}x}{3}+C', [('diff(sin(x)-sin(x)**3/3,x)', 'cos(x)**3')], 'نرجّع $u=\\sin x$. أعلى أس 3 = أس السؤال ✓')], 'odd e1')
    e2 = steps([
        (r'\sin^{3}x\cos^{4}x=\sin^{2}x\cos^{4}x\cdot\cD{\sin x}', [('sin(x)**3*cos(x)**4', 'sin(x)**2*cos(x)**4*sin(x)')],
         'أس sin فردي (3)، وأس cos زوجي (4): نحجز $\\sin x$.'),
        (r'\sin^{2}x=1-\cos^{2}x', [('sin(x)**2', '1-cos(x)**2')], 'الباقي يتحوّل لـ cos.'),
        (r'\cU{u=\cos x}\qquad \cD{du=-\sin x\,dx}\ \Rightarrow\ \sin x\,dx=\cR{-}du', [('diff(cos(x),x)', '-sin(x)')],
         '🔴 مشتقة cos فيها سالب، فالقطعة المحجوزة $=-du$.'),
        (r'I=\cR{-}\int(1-u^{2})\,u^{4}\,du=-\int\left(u^{4}-u^{6}\right)du', [('(1-u**2)*u**4', 'u**4-u**6')], 'السالب يطلع قدّام التكامل، ونوزّع $u^4$.'),
        (r'=-\frac{u^{5}}{5}+\frac{u^{7}}{7}', [('integrate(-(u**4-u**6),u)', '-u**5/5+u**7/7')], 'نكامل، والسالب يدخل على الحدين.'),
        (r'I=-\frac{\cos^{5}x}{5}+\frac{\cos^{7}x}{7}+C', [('diff(-cos(x)**5/5+cos(x)**7/7,x)', 'sin(x)**3*cos(x)**4')],
         'نرجّع $u=\\cos x$. أعلى أس 7 = 3 + 4 ✓')], 'odd e2')
    e3 = steps([
        (r'\sin^{5}x\cos^{3}x=\sin^{5}x\cos^{2}x\cdot\cD{\cos x}', [('sin(x)**5*cos(x)**3', 'sin(x)**5*cos(x)**2*cos(x)')],
         'الاثنين فرديين: الأصغر 3 (cos)، فنحجز $\\cos x$. أقل فك أقواس.'),
        (r'\cos^{2}x=1-\sin^{2}x', [('cos(x)**2', '1-sin(x)**2')], 'الباقي لـ sin.'),
        (r'\cU{u=\sin x}\qquad \cD{du=\cos x\,dx}', [('diff(sin(x),x)', 'cos(x)')], 'بدون سالب هنا.'),
        (r'I=\int u^{5}(1-u^{2})\,du=\int\left(u^{5}-u^{7}\right)du', [('u**5*(1-u**2)', 'u**5-u**7')], 'نوزّع $u^5$.'),
        (r'I=\frac{\sin^{6}x}{6}-\frac{\sin^{8}x}{8}+C', [('diff(sin(x)**6/6-sin(x)**8/8,x)', 'sin(x)**5*cos(x)**3')],
         'نكامل ونرجّع. أعلى أس 8 = 5 + 3 ✓')], 'odd e3')
    # completion problem (blanks); the full lines are checked
    chk('', [('cos(x)**5*sin(x)**4', 'cos(x)**4*sin(x)**4*cos(x)'), ('cos(x)**4', '(1-sin(x)**2)**2'),
             ('u**4*(1-u**2)**2', 'u**4-2*u**6+u**8')], 'odd c1')
    antideriv('sin(x)**5/5-2*sin(x)**7/7+sin(x)**9/9', 'cos(x)**5*sin(x)**4', 'odd c1')
    c1 = ('<ol class="fill">'
          + ''.join('<li>%s</li>' % t for t in [
              mi(r'\cos^{5}x\sin^{4}x=\cos^{4}x\sin^{4}x\cdot\cos x') + rich(' (أس cos فردي: حجزنا $\\cos x$)'),
              mi(r'\cos^{4}x=(1-\sin^{2}x)^{' + BLANK + '}'),
              mi(r'u=' + BLANK + r',\qquad du=' + BLANK),
              mi(r'I=\int u^{4}(1-u^{2})^{2}\,du=\int\left(u^{4}-' + BLANK + r'+u^{8}\right)du'),
              mi(r'I=' + BLANK + r'+C')]) + '</ol>')
    for F, f, lab in [('-cos(x)**5/5+2*cos(x)**7/7-cos(x)**9/9', 'sin(x)**5*cos(x)**4', 'odd s1'),
                      ('sin(x)**3/3-2*sin(x)**5/5+sin(x)**7/7', 'sin(x)**2*cos(x)**5', 'odd s2')]:
        antideriv(F, f, lab)
    solo = ('<div class="chgrid">'
            + '<div class="ch"><b>1</b>' + q(r'\int\sin^{5}x\cos^{4}x\,dx') + '<div class="src">📗 د. موسى ص 94</div></div>'
            + '<div class="ch"><b>2</b>' + q(r'\int\sin^{2}x\cos^{5}x\,dx') + '<div class="src">📝 اختبار ثاني 1447</div></div>'
            + '</div>')
    return section('odd', '١. فيه أس فردي: احجز وحوّل',
                   '<ol class="method">' + ''.join('<li>%s</li>' % rich(t) for t in ODD_STEPS) + '</ol>'
                   + box('🧱 مثال 1: أس فردي لحاله · 📘 د. طارق ص 67', q(r'\int\cos^{3}x\,dx') + e1)
                   + box('🧱 مثال 2: sin فردي (مع السالب) · 📘 د. طارق ص 76', q(r'\int\sin^{3}x\cos^{4}x\,dx') + e2)
                   + box('🧱 مثال 3: الاثنين فرديين · 📗 د. موسى ص 93', q(r'\int\sin^{5}x\cos^{3}x\,dx') + e3
                         + p(rich('لو حجزت من $\\sin^5$ يمشي بعد، بس تفك $(1-\\cos^2x)^2$، وهذا شغل أكثر.'), 'small'))
                   + box('✍️ عبّي الفراغات · 📗 د. موسى ص 94', q(r'\int\cos^{5}x\sin^{4}x\,dx') + c1)
                   + box('✏️ لحالك (الحل في المفتاح)', solo))


# ---------------------------------------------------------------- 3. even branch
EVEN_STEPS = ['حوّل كل $\\sin^2$ و $\\cos^2$ بنص الزاوية. ولو $\\sin x\\cos x$ مع بعض: $\\frac12\\sin2x$.',
              'فك القوس أو المربع.',
              'طلع $\\cos^2$ مرة ثانية (بزاوية مضاعفة)؟ نص الزاوية مرة ثانية: $2x$ تصير $4x$.',
              'كامل كل حد: $\\int\\cos kx\\,dx=\\frac{\\sin kx}{k}$. وتأكد: فيه حد $x$ لحاله.']


def page_even():
    e4 = steps([
        (r'\sin^{2}x=\frac{1-\cos2x}{2}=\frac12-\frac12\cos2x', [('sin(x)**2', 'Rational(1,2)-cos(2*x)/2')],
         'أس sin زوجي وما فيه cos: ما فيه شي نحجزه، فنص الزاوية. «سين وسالب».'),
        (r'I=\int\left(\frac12-\frac12\cos2x\right)dx', [], 'نكامل حد حد.'),
        (r'I=\frac{x}{2}-\frac{\sin2x}{4}+C', [('diff(x/2-sin(2*x)/4,x)', 'sin(x)**2')],
         '$\\int\\cos2x\\,dx=\\frac{\\sin2x}{2}$، ومعه $\\frac12$ قدّام: $\\frac14$.')], 'even e4')
    e5 = steps([
        (r'\sin^{4}x=\left(\sin^{2}x\right)^{2}=\left(\frac{1-\cos2x}{2}\right)^{2}', [('sin(x)**4', '((1-cos(2*x))/2)**2')],
         'الأس 4 زوجي: نكتبه مربع $\\sin^2$، ونحط نص الزاوية.'),
        (r'=\frac{1-2\cos2x+\cos^{2}2x}{4}', [('((1-cos(2*x))/2)**2', '(1-2*cos(2*x)+cos(2*x)**2)/4')], 'نفك المربع: $(a-b)^2=a^2-2ab+b^2$.'),
        (r'\cos^{2}2x=\frac{1+\cos4x}{2}', [('cos(2*x)**2', '(1+cos(4*x))/2')], 'طلع $\\cos^2$ مرة ثانية: نص الزاوية مرة ثانية، والزاوية تتضاعف.'),
        (r'\sin^{4}x=\frac38-\frac12\cos2x+\frac18\cos4x', [('sin(x)**4', 'Rational(3,8)-cos(2*x)/2+cos(4*x)/8')],
         'نجمع الأرقام: $\\frac14+\\frac18=\\frac38$.'),
        (r'I=\frac{3x}{8}-\frac{\sin2x}{4}+\frac{\sin4x}{32}+C', [('diff(3*x/8-sin(2*x)/4+sin(4*x)/32,x)', 'sin(x)**4')],
         'كل cos نقسمه على رقم زاويته.')], 'even e5')
    chk('', [('sin(x)**2*cos(x)**2', 'sin(2*x)**2/4'), ('sin(2*x)**2', '(1-cos(4*x))/2'),
             ('sin(x)**2*cos(x)**2', 'Rational(1,8)-cos(4*x)/8')], 'even c2')
    antideriv('x/8-sin(4*x)/32', 'sin(x)**2*cos(x)**2', 'even c2')
    c2 = ('<ol class="fill">' + ''.join('<li>%s</li>' % t for t in [
        mi(r'\sin x\cos x=\frac12\sin2x\ \Rightarrow\ \sin^{2}x\cos^{2}x=\frac14\sin^{2}2x') + rich(' (التريك: مع بعض بنفس الأس)'),
        mi(r'\sin^{2}2x=\frac{1-\cos' + BLANK + r'}{2}'),
        mi(r'\sin^{2}x\cos^{2}x=' + BLANK + '-' + BLANK + r'\cos4x'),
        mi(r'I=' + BLANK + r'+C')]) + '</ol>')
    for F, f, lab in [('3*x/8+sin(2*x)/4+sin(4*x)/32', 'cos(x)**4', 'even s3'), ('x/2+sin(6*x)/12', 'cos(3*x)**2', 'even s4')]:
        antideriv(F, f, lab)
    solo = ('<div class="chgrid">'
            + '<div class="ch"><b>3</b>' + q(r'\int\cos^{4}x\,dx') + '</div>'
            + '<div class="ch"><b>4</b>' + q(r'\int\cos^{2}3x\,dx') + rich('<div class="src">انتبه: $2\\cdot3x=6x$</div>') + '</div>'
            + '</div>')
    return section('even', '٢. كلها زوجية: نص الزاوية',
                   '<ol class="method">' + ''.join('<li>%s</li>' % rich(t) for t in EVEN_STEPS) + '</ol>'
                   + box('🧱 مثال 4: أس زوجي لحاله', q(r'\int\sin^{2}x\,dx') + e4)
                   + box('🧱 مثال 5: نص الزاوية مرتين', q(r'\int\sin^{4}x\,dx') + e5)
                   + box('✍️ عبّي الفراغات · 📗 د. موسى ص 96', q(r'\int\sin^{2}x\cos^{2}x\,dx') + c2)
                   + box('✏️ لحالك (الحل في المفتاح)', solo))


# ---------------------------------------------------------------- 4. the five famous mistakes
MISTAKES = [
    (r'\int\sin^{3}x\,dx:\quad u=\cos x,\ du=\sin x\,dx', 'cos(x)-cos(x)**3/3', r'\cos x-\frac{\cos^{3}x}{3}',
     'مشتقة $\\cos x$ هي $-\\sin x$. نسيت السالب، فطلع الجواب كله بالعكس.', '-cos(x)+cos(x)**3/3', r'-\cos x+\frac{\cos^{3}x}{3}+C', 'sin(x)**3'),
    (r'(1-u^{2})^{2}', '1-u**4', r'1-u^{4}', 'نسيت الحد الأوسط $2ab$.', '1-2*u**2+u**4', r'1-2u^{2}+u^{4}', None),
    (r'\int\cos^{2}x\,dx=\int\frac{1+\cos2x}{2}dx', 'x/2+sin(2*x)/2', r'\frac x2+\frac{\sin2x}{2}',
     '$\\int\\cos2x\\,dx=\\frac{\\sin2x}{2}$، ومعه $\\frac12$ من قدّام: صارت $\\frac14$.', 'x/2+sin(2*x)/4', r'\frac x2+\frac{\sin2x}{4}+C', 'cos(x)**2'),
    (r'\int\sin^{2}x\,dx', 'sin(x)**3/3', r'\frac{\sin^{3}x}{3}', 'قاعدة القوة تحتاج مشتقة الداخل جنبها، وما فيه $\\cos x$. هذا زوجي: نص الزاوية.',
     'x/2-sin(2*x)/4', r'\frac x2-\frac{\sin2x}{4}+C', 'sin(x)**2'),
    (r'\sin^{2}x', '(1+cos(2*x))/2', r'\frac{1+\cos2x}{2}', '«سين وسالب»: $\\sin^2$ معها ناقص، و $\\cos^2$ معها زائد.',
     '(1-cos(2*x))/2', r'\frac{1-\cos2x}{2}', None)]


def page_mistakes():
    rows = ''
    for k, (qq, wrong, wrong_tex, why, right, right_tex, f) in enumerate(MISTAKES, 1):
        a, b = P(wrong), P(right)
        if f:                                          # compare derivatives with the integrand
            a, b, ff = sp.diff(a, x), sp.diff(b, x), P(f)
            if sp.simplify(b - ff) != 0:
                raise BuildError('mistake %d: the right answer is wrong' % k)
            arith('', [('diff(%s,x)' % right, f)], 'mistake %d right' % k)
        diff = [abs(complex((a - b).subs({x: v, u: v}).evalf())) for v in (0.7, 1.3)]
        if max(diff) < 1e-9:
            raise BuildError('mistake %d: the wrong version is not wrong' % k)
        rows += ('<div class="fix"><b>%d.</b> %s = %s<div class="fixq">🔍 وين الغلط؟</div><div class="fixa">%s %s</div></div>'
                 % (k, mi(qq), mi(r'\cR{' + wrong_tex + '}'), p('<b>الجواب:</b> ' + rich(why)), md(right_tex)))
    arith('', [('(1-u**2)**2', '1-2*u**2+u**4'), ('sin(x)**2', '(1-cos(2*x))/2')], 'mistakes right lines')
    return section('fix', '🔍 صحّح الغلط: الأغلاط الخمس المشهورة',
                   p(rich('كل سطر أحمر فيه غلطة. غطِّ «الجواب» ولقها أول. الحاسوب تأكد إن كل «غلط» غلط فعلًا، وكل «صح» صح.')) + rows)


# ---------------------------------------------------------------- 5. mixed questions and the key
MIXED = [  # (question latex, source, branch, first line latex, answer latex, F, f, branch for the check)
    (r'\int\sin^{5}x\,dx', '', 'فردي (sin)', r'\sin^{5}x=(1-\cos^{2}x)^{2}\sin x,\ u=\cos x',
     r'-\cos x+\frac{2\cos^{3}x}{3}-\frac{\cos^{5}x}{5}+C', '-cos(x)+2*cos(x)**3/3-cos(x)**5/5', 'sin(x)**5', None),
    (r'\int\cos^{2}2x\,dx', '', 'زوجي', r'\cos^{2}2x=\frac{1+\cos4x}{2}', r'\frac x2+\frac{\sin4x}{8}+C', 'x/2+sin(4*x)/8', 'cos(2*x)**2', None),
    (r'\int\cos^{5}x\sin^{3}x\,dx', '📗 موسى ص 93', 'الاثنين فرديين: الأصغر sin', r'\sin^{3}x=(1-\cos^{2}x)\sin x,\ u=\cos x',
     r'-\frac{\cos^{6}x}{6}+\frac{\cos^{8}x}{8}+C', '-cos(x)**6/6+cos(x)**8/8', 'cos(x)**5*sin(x)**3', None),
    (r'\int\sin^{3}x\cos^{2}x\,dx', '', 'فردي (sin)', r'(1-\cos^{2}x)\cos^{2}x\sin x,\ u=\cos x',
     r'-\frac{\cos^{3}x}{3}+\frac{\cos^{5}x}{5}+C', '-cos(x)**3/3+cos(x)**5/5', 'sin(x)**3*cos(x)**2', None),
    (r'\int\cos^{3}2x\,dx', '', 'فردي (cos) بزاوية $2x$', r'u=\sin2x,\ du=2\cos2x\,dx',
     r'\frac{\sin2x}{2}-\frac{\sin^{3}2x}{6}+C', 'sin(2*x)/2-sin(2*x)**3/6', 'cos(2*x)**3', None),
    (r'\int\sqrt{\sin x}\,\cos^{3}x\,dx', '📘 طارق ص 69', 'فردي (cos)، وأس sin كسري', r'u=\sin x,\ \cos^{2}x=1-u^{2}',
     r'\frac23\sin^{3/2}x-\frac27\sin^{7/2}x+C', '2*sin(x)**Rational(3,2)/3-2*sin(x)**Rational(7,2)/7', 'sqrt(sin(x))*cos(x)**3', 't/(1+t)'),
    (r'\int\sin^{4}x\cos^{5}x\,dx', '📝 اختبار ثاني 1446', 'فردي (cos)', r'\cos^{4}x=(1-\sin^{2}x)^{2},\ u=\sin x',
     r'\frac{\sin^{5}x}{5}-\frac{2\sin^{7}x}{7}+\frac{\sin^{9}x}{9}+C', 'sin(x)**5/5-2*sin(x)**7/7+sin(x)**9/9', 'sin(x)**4*cos(x)**5', None),
    (r'\int\sin^{7}x\cos^{5}x\,dx', '📗 موسى ص 93', 'الاثنين فرديين: الأصغر cos', r'\cos^{4}x=(1-\sin^{2}x)^{2},\ u=\sin x',
     r'\frac{\sin^{8}x}{8}-\frac{\sin^{10}x}{5}+\frac{\sin^{12}x}{12}+C', 'sin(x)**8/8-sin(x)**10/5+sin(x)**12/12', 'sin(x)**7*cos(x)**5', None),
    (r'\int\sqrt[3]{\cos x}\,\sin^{3}x\,dx', '📘 طارق ص 76', 'فردي (sin)، وأس cos كسري', r'u=\cos x,\ \sin^{2}x=1-u^{2}',
     r'-\frac34\cos^{4/3}x+\frac{3}{10}\cos^{10/3}x+C', '-3*cos(x)**Rational(4,3)/4+3*cos(x)**Rational(10,3)/10', 'cos(x)**Rational(1,3)*sin(x)**3', 't/(1+t)'),
    (r'\int\sin^{5}x\cos^{6}x\,dx', '📝 نهائي 1445', 'فردي (sin)', r'\sin^{4}x=(1-\cos^{2}x)^{2},\ u=\cos x',
     r'-\frac{\cos^{7}x}{7}+\frac{2\cos^{9}x}{9}-\frac{\cos^{11}x}{11}+C', '-cos(x)**7/7+2*cos(x)**9/9-cos(x)**11/11', 'sin(x)**5*cos(x)**6', None)]


def page_mixed():
    qs = ''
    for k, (qq, src, *_rest) in enumerate(MIXED, 1):
        F, f, br = _rest[3], _rest[4], _rest[5]
        antideriv(F, f, 'mixed %d' % k, br)
        qs += '<div class="ch"><b>%d</b>%s%s</div>' % (k, q(qq), ('<div class="src">%s</div>' % src) if src else '')
    return section('mixed', '🔀 10 أسئلة مخلوطة (مثل الاختبار)',
                   p(rich('<b>الجولة الأولى:</b> اكتب تحت كل سؤال <b>الفرع وأول سطر</b> بس. <b>الجولة الثانية:</b> حلها كاملة. '
                          'المفتاح في الصفحة اللي بعدها.')) + '<div class="chgrid">' + qs + '</div>')


def page_key():
    rows = [[str(k), rich(br), mi(r'\displaystyle ' + first), mi(r'\displaystyle ' + ans)]
            for k, (qq, src, br, first, ans, F, f, b) in enumerate(MIXED, 1)]
    blanks = ul([rich('<b>عبّي الفراغات (فردي):</b> $2$ · $u=\\sin x$، $du=\\cos x\\,dx$ · $2u^6$ · '
                      '$\\frac{\\sin^5x}{5}-\\frac{2\\sin^7x}{7}+\\frac{\\sin^9x}{9}$'),
                 rich('<b>عبّي الفراغات (زوجي):</b> $4x$ · $\\frac18$ و $\\frac18$ · $\\frac x8-\\frac{\\sin4x}{32}$')])
    solo = table(['#', 'الجواب'], [
        ['1', mi(r'\displaystyle -\frac{\cos^{5}x}{5}+\frac{2\cos^{7}x}{7}-\frac{\cos^{9}x}{9}+C')],
        ['2', mi(r'\displaystyle \frac{\sin^{3}x}{3}-\frac{2\sin^{5}x}{5}+\frac{\sin^{7}x}{7}+C')],
        ['3', mi(r'\displaystyle \frac{3x}{8}+\frac{\sin2x}{4}+\frac{\sin4x}{32}+C')],
        ['4', mi(r'\displaystyle \frac{x}{2}+\frac{\sin6x}{12}+C')]], 'answers')
    return section('key', '🔑 المفتاح',
                   '<h3>الفراغات</h3>' + blanks + '<h3>«لحالك»</h3>' + solo
                   + '<h3>المخلوطة: الفرع، وأول سطر، والجواب</h3>'
                   + table(['#', 'الفرع', 'أول سطر', 'الجواب'], rows, 'answers')
                   + p(rich('جوابك شكله غير؟ اشتقه: إذا رجع السؤال فهو صح. والفرق بثابت عادي.'), 'small'))


def build():
    title = ('<section class="summary" id="top"><div class="kicker">ريض 111 · درس 5.2 · odd و even</div>'
             '<h1>odd و even: تكاملات sin و cos</h1>'
             + p(rich('درس واحد، شرح كامل: قرار واحد، وفرعين، وأمثلة محلولة، وتدريب يقل فيه الدعم، وأسئلة مخلوطة بمفتاحها. '
                      'كل سطر وكل جواب هنا فحصه الحاسوب.'), 'small') + '</section>')
    return title + page_map() + page_tools() + page_odd() + page_even() + page_mistakes() + page_mixed() + page_key()

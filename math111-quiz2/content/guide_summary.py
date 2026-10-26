"""«ملخص الفهم»: the whole quiz in a few pages, built from the same checked parts as the full guide.

What to memorise is the few things that generate the rules (one derivative table read both ways, one «keep the
derivative of u» rule for the trig powers, the parts formula), not the 34 cases. Then the tree, then one decision
table: for every case what you see, the first step, the rule, and the page of its worked example in the full guide.
Every formula line is checked while building (arith / formula), like the guide.
"""
import re

import guide_kit as K
import guide_paths as GP
from booklet import doctor_coth, frow, sc_six, sc_twins
from booklet_engine import arith, formula
from guide_52 import SHEET_ROWS
from guide_kit import rich
from html_kit import mi, md, p, table, ul

SKIP = {'U-I7', 'U-T7', 'U-P8', 'U-P10'}      # cases 8, 13, 32, 33: rare in the exams, Dr. Musa's notes and the lectures


def box(title, inner):
    return '<div class="sbox"><h3>%s</h3>%s</div>' % (rich(title), inner)


def memory():
    """Everything to memorise, in the fewest rules; every line checked."""
    d41 = arith(r"(\sinh x)'=\cosh x,\quad (\cosh x)'=\sinh x,\quad (\tanh x)'=\operatorname{sech}^{2}x\\ "
                r"(\coth x)'=-\operatorname{csch}^{2}x,\quad (\operatorname{sech}x)'=-\operatorname{sech}x\tanh x,\quad "
                r"(\operatorname{csch}x)'=-\operatorname{csch}x\coth x",
                [('diff(sinh(x),x)', 'cosh(x)'), ('diff(cosh(x),x)', 'sinh(x)'), ('diff(tanh(x),x)', 'sech(x)**2'),
                 ('diff(coth(x),x)', '-csch(x)**2'), ('diff(sech(x),x)', '-sech(x)*tanh(x)'),
                 ('diff(csch(x),x)', '-csch(x)*coth(x)')], 'summary 4.1')
    one = box('١. مشتقات 4.1: قاعدة وحدة',
              p(rich('زي مشتقات المثلثات بالضبط، إلا <b>اثنين إشارتهم عكس</b>: $\\cosh$ مشتقتها موجبة، و $\\operatorname{sech}$ مشتقتها سالبة. '
                     'ودايم × مشتقة الداخل.')) + md(r'\begin{gathered}' + d41 + r'\end{gathered}'))
    twins = box('٢. مشتقات الدوال العكسية (4.2)',
                sc_twins()[0]
                + p(rich('تحفظها كذا: $\\sinh^{-1}$ معها $\\sqrt{u^2+1}$، و $\\cosh^{-1}$ معها $\\sqrt{u^2-1}$. '
                         '$\\tanh^{-1}$ و $\\coth^{-1}$ نفس الشكل $\\frac{1}{1-u^2}$. '
                         '$\\operatorname{sech}^{-1}$ و $\\operatorname{csch}^{-1}$ فيهم سالب و $u$ برّا الجذر.'), 'small'))
    six = box('٣. التكاملات: نفس الجدول، بس تقراه بالعكس ومعه $a$',
              sc_six(adjust=False)[0]
              + p(rich('الجذر لحاله ($\\sinh^{-1}$ و $\\cosh^{-1}$) <b>بدون</b> $\\frac1a$، والباقي <b>معه</b> $\\frac1a$. '
                       'و tanh⁻¹ أم coth⁻¹؟ قارن $|u|$ مع $a$، وإذا السؤال ما حدّد $x$: $\\tanh^{-1}$ وجنبه $|u|<a$.'), 'small'))
    r34 = [formula('1/sqrt(a**2-u**2)', 'asin(u/a)', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='summary asin'),
           formula('1/(a**2+u**2)', 'atan(u/a)/a', branches=('x',), pos=('a',), label='summary atan'),
           formula('1/(u*sqrt(u**2-a**2))', 'asec(u/a)/a', branches=('a+t',), pos=('a',), label='summary asec')]
    three4 = box('٤. من درس 3.4 (عشان ما تخلطها مع 4.2)',
                 table(['التكامل', 'الجواب (+C)', 'متى'], [frow(r34[0], 'الرقم أول تحت الجذر'), frow(r34[1], 'زائد، بدون جذر'),
                                                          frow(r34[2], mi('u') + ' برّا، و ' + mi('u^2') + ' أول')], 'formula'))
    sub = box('٥. التعويض في سطر',
              p(rich('اقسم اللي برّا على مشتقة الداخل: طلع <b>رقم</b>؟ تعويض، والرقم يطلع قدّام التكامل <b>مرة وحدة</b>. '
                     'طلع فيه $x$؟ شوف التجهيزات، وإلا تجزئة.')))
    parts = box('٦. التجزئة',
                md(arith(r'\int u\,dv=uv-\int v\,du', [], 'summary parts'))
                + ul([rich('<b>LIATE</b> يختار $u$: ln، ثم دالة عكسية، ثم $x$ وقواها، ثم sin و cos، ثم $e^x$. والباقي $dv$.'),
                      rich('$u$ قوة 2 أو 3 ← <b>جدول DI</b>: D تنزل للصفر، I تتكامل، والإشارات $+\\ -\\ +$.'),
                      rich('ln لحالها أو دالة عكسية لحالها ← $dv=dx$.'),
                      rich('$e^{ax}$ مع sin أو cos ← جزّئ مرتين بنفس الاختيار. التكامل يرجع لنفسه، فانقله لليسار.')]))
    half = arith(r'\sin^{2}x=\frac{1-\cos2x}{2}\qquad\cos^{2}x=\frac{1+\cos2x}{2}',
                 [('sin(x)**2', '(1-cos(2*x))/2'), ('cos(x)**2', '(1+cos(2*x))/2')], 'summary half')
    prod = arith(r'\sin A\cos B=\tfrac12\left[\sin(A-B)+\sin(A+B)\right]\\ \cos A\cos B=\tfrac12\left[\cos(A-B)+\cos(A+B)\right]'
                 r'\\ \sin A\sin B=\tfrac12\left[\cos(A-B)-\cos(A+B)\right]',
                 [('sin(7*x)*cos(5*x)', '(sin(2*x)+sin(12*x))/2'), ('sin(4*x)*sin(3*x)', '(cos(x)-cos(7*x))/2'),
                  ('cos(3*x)*cos(x)', '(cos(2*x)+cos(4*x))/2')], 'summary product')
    rows = [[see, mi(keep), mi(u), mi(rest)] for see, keep, u, rest in SHEET_ROWS]
    arith('', [('cos(x)**2', '1-sin(x)**2'), ('sec(x)**2', '1+tan(x)**2'), ('csc(x)**2', '1+cot(x)**2'),
               ('diff(sin(x),x)', 'cos(x)'), ('diff(cos(x),x)', '-sin(x)'), ('diff(tan(x),x)', 'sec(x)**2'),
               ('diff(sec(x),x)', 'sec(x)*tan(x)'), ('diff(cot(x),x)', '-csc(x)**2'), ('diff(csc(x),x)', '-csc(x)*cot(x)')],
          'summary keep table')
    trig = box('٧. المثلثات (5.2): قاعدة وحدة بدل 8 حالات',
               p(rich('<b>احجز مشتقة الـ $u$، وحوّل الباقي بالمتطابقة</b> ($\\sin^2+\\cos^2=1$، أو $1+\\tan^2=\\sec^2$، أو $1+\\cot^2=\\csc^2$).'))
               + table(['إذا شفت', 'احجز (تصير du)', 'نسمّي', 'والباقي يتحوّل بـ'], rows, 'formula')
               + ul([rich('الاثنين فرديين؟ احجز من الأصغر.'),
                     rich('<b>الأسس كلها زوجية</b> (ما فيه شي تحجزه) ← نص الزاوية:') + md(half),
                     rich('<b>زاويتين مختلفتين</b> ← حوّل الضرب لجمع (sin·sin الوحيدة اللي فيها ناقص):') + md(r'\begin{gathered}' + prod + r'\end{gathered}'),
                     rich('$\\tan^n$ لحالها ← $\\tan^2x=\\sec^2x-1$. و $\\sec^3x$ لحالها ← تجزئة: $u=\\sec x$، $dv=\\sec^2x\\,dx$.')]))
    sq = arith(r'x^{2}+6x+5=(x+3)^{2}-4', [('x**2+6*x+5', '(x+3)**2-4')], 'summary square')
    expo = arith(r'\sinh x=\frac{e^{x}-e^{-x}}{2}\qquad\cosh x=\frac{e^{x}+e^{-x}}{2}\qquad \ln\sqrt[3]{x}=\frac13\ln x',
                 [('sinh(x)', '(exp(x)-exp(-x))/2'), ('cosh(x)', '(exp(x)+exp(-x))/2'), ('log(x**Rational(1,3))', 'log(x)/3', 't')],
                 'summary exp')
    prep = box('٨. التجهيزات (جبر يغيّر الشكل بس)',
               ul([rich('<b>إكمال المربع:</b> نص معامل $x$، ربّعه، أضفه واطرحه:') + md(sq),
                   rich('<b>sinh و cosh مع $e^x$ أو في المقام</b> ← اكتبها بالأسس:') + md(expo),
                   rich('<b>بسط فيه جمع</b> ← افصل لكسرين. <b>$x^3$ فوق $x^2+a$</b> ← $u=x^2+a$ و $x^2=u-a$. '
                        '<b>أسية تحت الجذر</b> ← اضرب فوق وتحت في اللي يخلي اللي برّا $u$.')]))
    doc = box('٩. عند دكتورك (درجات سهلة لا تضيعها)',
              ul([rich('كل سطر تكامل يبدأ بـ $I=$، وفي الآخر $+C$.'),
                  rich('$|u|$ داخل ln، ومع $\\operatorname{sech}^{-1}$ و $\\operatorname{csch}^{-1}$.'),
                  rich('$\\coth^{-1}$ بإشارته هو ✎: ') + mi(r'\frac{d}{dx}\coth^{-1}u=' + doctor_coth('diff'))
                  + rich(' و $\\int\\frac{du}{a^2-u^2}=') + mi(doctor_coth('int')) + '.',
                  rich('ما عرفت تكمّل؟ اكتب أول سطر ($u$ و $du$، أو $u$ و $dv$): عليه درجة.')]))
    return ('<section class="chapter summary" id="memory"><h2>🧠 كل اللي تحفظه</h2>'
            + p(rich('هذي كل القوانين. الحالات الـ34 كلها تطبيق لها، فما تحفظ الحالات: تحفظ هذي، والشجرة تقول لك أي وحدة.'))
            + one + twins + six + three4 + sub + parts + trig + prep + doc + '</section>')


def decision(pages, sections):
    """One row per case: what you see → first step → rule → page of its worked example in the full guide."""
    out = ''
    for key, uids in sections:
        rows = []
        for uid in uids:
            if uid.startswith('P-') or uid in SKIP or uid not in K.GIST:
                continue
            num, title, see, first, rule = K.GIST[uid]
            rows.append(['<b>%s%d</b>' % ('⭐' if uid in K.CORE else '', num), rich(see), rich(first), rich(rule),
                         str(pages.get(uid, ''))])
        if not rows:
            continue
        script = ' ← '.join(re.sub(r'🔴 <b>لا تنسى:</b> ', '', s) for s in GP.SCRIPTS[key][:-1])
        out += ('<h3>%s</h3>' % K.mname(key) + p(rich('<b>الخطوات:</b> ' + script), 'small')
                + table(['#', 'إذا شفت', 'أول خطوة', 'القاعدة', 'ص 🧱'], rows, 'decide'))
    return ('<section class="chapter summary" id="decide"><h2>🗂️ جدول القرار: 30 حالة في سطر سطر</h2>'
            + p(rich('غطِّ الأعمدة الثلاثة الأخيرة، واقرأ «إذا شفت»، وقل أول خطوة من راسك. ما عرفت؟ افتح المثال المحلول 🧱 '
                     'في المذكرة الكاملة (رقم الصفحة في آخر عمود). الحالات 8 و13 و32 و33 سحبنا عليها.'))
            + out + '</section>')


def howto():
    return ('<section class="summary" id="top"><div class="kicker">ريض 111 · الكويز الثاني · ملخص الفهم</div>'
            '<h1>ملخص الفهم</h1>'
            + ul([rich('<b>١. احفظ صفحة «كل اللي تحفظه»</b>: 9 صناديق، وهي كل القوانين.'),
                  rich('<b>٢. الشجرة</b>: أربعة أسئلة تختار لك الطريقة.'),
                  rich('<b>٣. جدول القرار</b>: كل حالة في سطر. غطِّ وقل أول خطوة.'),
                  rich('<b>٤.</b> الحالة اللي ما عرفت تبدأها بس: افتح مثالها 🧱 في المذكرة الكاملة (الصفحة مكتوبة)، وحل تمرين «تعرفها؟».')])
            + p('ما فيه طرق سريعة ولا تريكات هنا: الطريقة العادية تحل كل شي، وكذا تحفظ أقل.', 'small')
            + '</section>')


def build(pages, sections):
    tree = re.sub(r'<a [^>]*>(.*?)</a>', r'\1', GP.tree(), flags=re.S)     # its links point into the full guide
    return howto() + memory() + tree + decision(pages, sections)

"""المذكرة الكاملة — القسم د (وش الحالة؟ والمراجعة المخلوطة)، يوم الكويز، الاختباران، ليلة الكويز، ورقة القوانين،
إذا علقت، أخطاء الجبر، سجل الأخطاء، المفاتيح، الملحق."""
import json
from pathlib import Path

import booklet as B
from booklet import sc_six, sc_twins
from booklet_engine import HOLD, ITEMS, LOG, ans_tex, q_tex
from guide_52 import sc_method
import guide_prereq as PQ
import guide_kit as K
from guide_kit import HELP, TRY_KEYS, final, pgref, rich
from html_kit import box, chip, lines, link, md, mi, p, table, ul

ROOT = Path(__file__).resolve().parent.parent

TITLES = {'mockA': 'الاختبار التجريبي A', 'mixed': 'المراجعة المخلوطة', 'mockB': 'الاختبار التجريبي B',
          'quizday': 'يوم الكويز: الليلة، والصباح، وفي القاعة', 'night': '🌙 مراجعة ليلة الكويز'}
# after the four methods: what to write for a full mark, the quiz day, the mocks; then the appendix
END_TOC = [('fullmark', '💯 ورقة الدرجة الكاملة'), ('differs', '🤔 جوابك يختلف عن المفتاح؟'), ('quizday', '🎯 ' + TITLES['quizday']),
           ('mockA', '📝 الاختبار التجريبي A'), ('night', TITLES['night']), ('mockB', '📝 الاختبار التجريبي B (إذا بقي وقت)'),
           ('stuck', 'ملحق: إذا علقت'), ('mistakes', 'ملحق: أخطاء الجبر الشائعة'),
           ('errlog', 'ملحق: سجل الأخطاء'), ('keys', 'ملحق: المفاتيح'), ('appendix', 'ملحق: المصادر والتحقق')]

SPEED = {
    'speed42': ('4.2', [('N42-X2-13', 'النوع 10: المركز $-3$، والباقي $-9$ سالب، يعني cosh، و $a=3$'),
                        ('1446-S2-SE-Q2.2', 'النوع 10: المركز $-1$، والباقي $9$ موجب، يعني sinh، و $a=3$'),
                        ('N42-E2-7', 'النوع 10: المركز $-1$، والباقي $-9$ سالب، يعني cosh، و $a=3$'),
                        ('1447-S1-SE-Q2.4', 'النوع 11: المركز $3$، والباقي $16$، ومعامل $x^2$ سالب، يعني sech'),
                        ('N42-X2-05', 'النوع 5: $u=3x^2$، $a=2$، داخل الجذر ناقص، يعني sech'),
                        ('N42-E1-7', 'النوع 2: ضرب دالتين، و $u=5x$'),
                        ('N42-X1-3', 'النوع 2: قوة، ثم tanh⁻¹ مع $u=3x$'),
                        ('1445-S1-FE-Q1.3', 'النوعان 1 و 2: sinh⁻¹ مع $u=3^x$، ثم ln'),
                        ('1447-S2-SE-Q1.1', 'النوع 1: $u=\\ln|x+1|$'),
                        ('1447-S2-SE-Q3.4', 'النوع 11: المركز $2$، والباقي $2$، ومعامل $x^2$ سالب، يعني sech، و $a=\\sqrt2$')]),
    'speed51': ('5.1', [('N51-X01', 'النوع 12: $u=$ القوس، و $dv=\\cosh x\\,dx$ (أو جدول DI)'),
                        ('G-22', 'النوع 14: $u=\\ln|x|$، و $dv=x^4dx$'),
                        ('G-40', 'النوع 17: دالة عكسية وحدها، يعني $u=$ الدالة، و $dv=dx$'),
                        ('G-41', 'النوع 17: دالة عكسية وحدها، يعني $u=$ الدالة، و $dv=dx$'),
                        ('G-17', 'النوع 12: $u=x$، و $dv=e^{-x}dx$'),
                        ('G-18', 'النوع 13: جدول DI'),
                        ('G-19', 'النوع 19: التكامل يرجع لنفسه، رقم الأسية 3 ورقم sin 1'),
                        ('G-20', 'النوع 20: اكتب sinh بالأسس'),
                        ('G-21', 'النوع 17: دالة عكسية وحدها، يعني $u=$ الدالة، و $dv=dx$')]),
    'speed52': ('5.2', [('N52-X11', 'النوع 29: sin·sin، $m=2$، $n=6$'),
                        ('N52-X04', 'النوع 23: $u=\\cos x$، و $\\sqrt[3]{\\cos x}=u^{1/3}$'),
                        ('G-23', 'النوع 23: sin فردي، يعني $u=\\cos x$'),
                        ('G-24', 'النوع 27: $\\tan^2x=\\sec^2x-1$'),
                        ('G-25', 'النوع 28: csc زوجي، يعني $u=\\cot x$'),
                        ('G-26', 'النوع 29: $m=5$، $n=2$'),
                        ('G-27', 'النوع 24: نص الزاوية'),
                        ('G-28', 'النوع 28: cot فردي، يعني $u=\\csc x$')])}

# derivatives first, as in the quiz; the integrals interleaved so that their order does not give away the lesson
MIXED = [('1445-S2-FE-Q1.3', 'النوعان 1 و 2'), ('1446-S2-SE-Q1.1', 'النوع 1 + 4.1'), ('N42-E1-8', 'النوع 2: قسمة'),
         ('N42-X1-2', 'النوع 2: ضرب'), ('G-33', 'النوع 23'), ('G-29', 'النوع 10'), ('G-32', 'النوع 19'), ('G-35', 'النوع 29'),
         ('G-30', 'النوع 5'), ('G-37', 'النوع 16'), ('G-34', 'النوع 27'), ('G-31', 'النوع 12'),
         ('1445-S2-SE-Q2.2', 'النوع 12'), ('1446-S1-FE-Q2.2', 'النوع 14')]

SPEED_KEYS = {}    # speed page -> rows of its key (printed in the keys section)
MIXED_KEY = []     # rows of the mixed-review key


def section(id_, title, inner, cls=''):
    return '<section class="chapter %s" id="%s"><h2>%s</h2>%s</section>' % (cls, id_, title, inner)


def question_used(it, where):
    from booklet_engine import use
    use(it['id'], where)
    return it


def speed_page(anchor):
    lesson, rows = SPEED[anchor]
    qs, key = '', []
    for k, (item_id, hint) in enumerate(rows, 1):
        it = ITEMS[item_id]
        qs += '<div class="ch"><b>%d</b>%s%s</div>' % (k, md(q_tex(question_used(it, anchor))), lines(1, 'write short'))
        key.append([str(k), rich(hint), mi(r'\displaystyle ' + ans_tex(it, with_lhs=False).lstrip('= '))])
        final(it, anchor)
    SPEED_KEYS[anchor] = (lesson, key)
    hint = {'4.2': '$u$ و $a$، أو المركز والباقي', '5.1': '$u$ و $dv$', '5.2': 'القطعة اللي تحجزها و $u$'}[lesson]
    page = (p(rich('لا تحل. اكتب تحت كل سؤال <b>الطريقة ورقم الحالة</b> و<b>أول سطر</b> فقط (مثل ' + hint + '). '
                   'الهدف إنك تقرّر في ثواني. المفتاح في ') + link('k-' + anchor, 'المفاتيح ص ' + pgref('k-' + anchor)) + '.')
            + '<div class="chgrid">' + qs + '</div>')
    return section(anchor, '🔎 وش الحالة؟ أسئلة من درس %s' % lesson, page, 'flow')


def mock_box(which):
    anchor = 'mock' + which
    if which == 'A':
        items = ['افتح ملف <b>الاختبارين التجريبيين</b>، الاختبار A.',
                 '60 دقيقة بالضبط (اضبط منبهًا)، بدون مذكرة وبدون ورقة قوانين وبدون آلة حاسبة.',
                 'بعد الوقت صحّح <b>A فقط</b> من صفحة حلوله، وسجّل كل غلطة في ' + link('errlog', 'سجل الأخطاء')
                 + '. حلول B بعد فاصل ثاني: لا تفتحها قبل ما تحل B بكرة.',
                 'أي سؤال غلطت فيه: ارجع لحالته (رقمها في صفحة الحلول)، واقرأ 🧱، وحل تمرينها الأخير مرة ثانية.']
    else:
        items = ['افتح الملف نفسه، الاختبار B. نفس الشروط: 60 دقيقة، بدون مذكرة وبدون ورقة قوانين وبدون آلة حاسبة.',
                 'بعد الوقت صحّح B من صفحة حلوله، وسجّل أخطاءك في ' + link('errlog', 'سجل الأخطاء') + '.',
                 'أي سؤال غلطت فيه: ارجع لحالته، واقرأ 🧱، وحل تمرينها الأخير مرة ثانية.']
    return section(anchor, '📝 الاختبار التجريبي %s' % which, box('warn', 'التعليمات', ul(items)), 'flow')


def mixed_page():
    qs, key = '', []
    for k, (item_id, kind) in enumerate(MIXED, 1):
        it = ITEMS[item_id]
        qs += '<div class="ch"><b>%d</b>%s%s</div>' % (k, md(q_tex(question_used(it, 'mixed review'))), lines(4, 'write tight'))
        key.append([str(k), rich(kind), mi(r'\displaystyle ' + ans_tex(it, with_lhs=False).lstrip('= '))])
        final(it, 'mixed review')
    MIXED_KEY[:] = key
    page = (p('%d سؤال من الدروس الثلاثة بدون عناوين، مثل الكويز. لكل سؤال: امشِ على الشجرة، واكتب أول سطر، ثم حل. '
              % len(MIXED) + 
              'الأجوبة في ' + link('k-mixed', 'المفاتيح ص ' + pgref('k-mixed')) + '.')
            + '<div class="chgrid">' + qs + '</div>')
    return section('mixed', '🔀 المراجعة المخلوطة', page)


def section_d():
    """Section د: the three «which case?» pages, then the mixed review."""
    import guide_paths as GP
    return GP.mastery() + GP.fix_mistakes() + ''.join(speed_page(a) for a in ('speed42', 'speed51', 'speed52')) + mixed_page()


def after_methods():
    """After the four methods: the full-mark sheet, «your answer differs from the key», the quiz day, the mocks."""
    import guide_paths as GP
    return GP.fullmark() + GP.differs() + quiz_day() + mock_box('A') + night() + mock_box('B')


def formulas():
    """The laws to know, and the five quick ways with their memory lines (every math line checked)."""
    from booklet_engine import arith
    sheet = lambda html: '<div class="fsheet">' + html + '</div>'
    quick = lambda name, text: p('<b>⚡ ' + name + ':</b> ' + rich(text))
    law42 = sheet(sc_twins()[0]) + sheet(sc_six(adjust=False)[0])
    law42 += quick('المركز والباقي (النوعان 10 و11)', 'المركز = سالب معامل $x$ ÷ (2 × معامل $x^2$). والباقي = اللي تحت الجذر لما نعوّض المركز. '
                   'فيصير: (معامل $x^2$) × ($x$ ناقص المركز)² + الباقي. «المركز يصفّر القوس، والباقي هو اللي يبقى».')
    law42 += p(rich('🔑 رقم التعديل: البسط ناقصه رقم عشان يصير $du$؟ اقسم عليه برّا. و tanh⁻¹ أم coth⁻¹؟ $u$ أصغر من $a$ يعني tanh⁻¹.'))
    law51 = p('<b>📐 التجزئة:</b> ' + rich('$\\int u\\,dv=uv-\\int v\\,du$. واختيار $u$ بالترتيب LIATE: ln، ثم دالة عكسية، ثم $x$، ثم sin و cos، ثم $e^x$.'))
    law51 += quick('جدول DI (النوعان 12 و13)', 'D تنزل للصفر، I تتكامل، واضرب مايل بإشارات $+\\ -\\ +$.')
    law51 += quick('قوة × ln (النوعان 14 و15)', 'كامل القوة ($v$)، واضرب في ($\\ln x$ ناقص 1 على نفس المقام). '
                   'مثال: $\\int x^2\\ln x\\,dx=\\frac{x^3}{3}\\left(\\ln x-\\frac13\\right)$، و $\\int\\ln x\\,dx=x(\\ln x-1)$.'
                   + arith('', [('diff(x**3/3*(log(x)-Rational(1,3)),x)', 'x**2*log(x)', 't'), ('diff(x*(log(x)-1),x)', 'log(x)', 't')], 'sheet ln'))
    law51 += quick('أسية × sin أو cos (النوع 19)', 'المقام $a^2+b^2$، والقوس: $a$ × الدالة ناقص مشتقتها.')
    law51 += md(r"\int e^{ax}f\,dx=\frac{e^{ax}\left(a\,f-f'\right)}{a^{2}+b^{2}}+C\qquad f=\sin bx\ \text{or}\ \cos bx")
    law52 = sheet(sc_method()[0])
    law52 += sheet(md(arith(r'\sin^{2}x=\frac{1-\cos2x}{2}\qquad \cos^{2}x=\frac{1+\cos2x}{2}',
                            [('sin(x)**2', '(1-cos(2*x))/2'), ('cos(x)**2', '(1+cos(2*x))/2')], 'sheet half'))
                   + p(rich('🔑 سين وسالب: $\\sin^2$ معها ناقص.')))
    prods = [(r'\sin A\cos B=\tfrac12\left[\sin(A-B)+\sin(A+B)\right]', ('sin(7*x)*cos(5*x)', '(sin(2*x)+sin(12*x))/2')),
             (r'\sin A\sin B=\tfrac12\left[\cos(A-B)-\cos(A+B)\right]', ('sin(4*x)*sin(3*x)', '(cos(x)-cos(7*x))/2')),
             (r'\cos A\cos B=\tfrac12\left[\cos(A-B)+\cos(A+B)\right]', ('cos(3*x)*cos(x)', '(cos(2*x)+cos(4*x))/2'))]
    law52 += sheet(''.join(md(arith(t, [c], 'sheet product')) for t, c in prods))
    law52 += quick('سلسلة tan و sec³ (النوع 27)', 'الأسس تنزل 2 2، كل حد على أسه، الإشارات تتبادل، والآخر $x$ (أس زوجي) أو $\\ln|\\sec x|$ (أس فردي). '
                   'مثال: $\\int\\tan^4x\\,dx=\\frac{\\tan^3x}{3}-\\tan x+x$. و $\\int\\sec^3x\\,dx$ «نص ونص»: '
                   '$\\frac12\\sec x\\tan x+\\frac12\\ln|\\sec x+\\tan x|$.'
                   + arith('', [('diff(tan(x)**3/3-tan(x)+x,x)', 'tan(x)**4'),
                                ('diff(sec(x)*tan(x)/2+log(sec(x)+tan(x))/2,x)', 'sec(x)**3', 't/(1+t)')], 'sheet tan'))
    parts = ['<h3>4.2</h3>' + law42, '<h3>5.1</h3>' + law51, '<h3>5.2</h3>' + law52]
    return section('formulas', '📋 ورقة القوانين والطرق السريعة',
                   p('اقرأها يوم 26 ومرة صباح الكويز. لا تُدخلها معك القاعة.', 'small') + ''.join(parts) + PQ.sheet(), 'fsheets')


def stuck():
    body = ul(['<b>ما عرفت الطريقة؟</b> ' + link('tree', 'الشجرة') + ': أربعة أسئلة بالترتيب، ووقّف عند أول «إيه».',
               '<b>عرفت الطريقة وما عرفت تبدأ؟</b> اكتب أول سطر في سكربتها: غالبًا $u$ و $du$، أو $u$ و $dv$.',
               '<b>نسيت الطريقة السريعة؟</b> استخدم خطوات 🧱 في صفحة الحالة، أو أول صفحة في طريقتها.',
               '<b>الجبر وقفك؟</b> ' + link('s0', 'حركات الجبر التسع في القسم 0') + '، وكل حركة معها فحص برقم. وشوف ' + link('mistakes', 'أخطاء الجبر الشائعة') + '.',
               '<b>جوابك يختلف عن الحل؟</b> ' + link('differs', 'جوابك يختلف عن المفتاح؟') + ': اشتق جوابك، أو عوّض رقمين.',
               '<b>tanh⁻¹ أم coth⁻¹؟</b> قارن $|u|$ مع $a$.',
               '<b>نسيت الإشارة في sin و cos؟</b> $\\int\\sin=-\\cos$ و $\\int\\cos=\\sin$. و sinh و cosh بدون سالب.',
               '<b>في الكويز:</b> ابدأ بالسؤال الأسهل (المشتقات عادة أسرع). لا تترك سؤالًا فاضيًا: الخطوة الأولى الصحيحة '
               '(مثل $u$ و $du$، أو $u$ و $dv$) أفضل من ورقة فاضية.'])
    return section('stuck', '🆘 إذا علقت', rich(body))


def errlog():
    rows = [['', '', '', ''] for _ in range(14)]
    intro = p('كل غلطة تكتبها هنا مرة واحدة. نوع الغلطة: <b>فهم</b> (ما فهمت الفكرة)، <b>اختيار</b> (اخترت الطريقة الغلط)، '
              '<b>استرجاع</b> (نسيت القانون أو البداية)، <b>جبر</b> (حساب أو إشارة). راجع هذه الصفحة كل صباح ويوم 26. '
              'وأغلاط الجبر المعروفة تجدها في ' + link('mistakes', 'أخطاء الجبر الشائعة') + '.')
    return section('errlog', '📒 سجل الأخطاء', intro + table(['التمرين (والصفحة)', 'وش صار', 'نوع الغلطة', 'الصح'], rows, 'errlog'))


def help_ladder():
    intro = (p('لكل تمرين ثلاث درجات مساعدة. <b>افتح درجة وحدة بس</b>، ثم ارجع للتمرين واكتب خطوتك التالية بنفسك. '
               'إذا علقت مرة ثانية، افتح الدرجة اللي بعدها.')
             + p('الرقم في أول عمود: <b>12.3</b> = الحالة 12، التمرين 3. اضغطه يرجعك للتمرين.', 'small')
             + ul(['<b>💡 الدرجة 1: تلميح العلامة</b> — الجدول الأول هنا.',
                   '<b>✍️ الدرجة 2: أول خطوة</b> — الجدول الثاني هنا. في التمرين الموجّه هي الخطوة اللي بعد البداية الجاهزة.',
                   '<b>✅ الدرجة 3: الحل الكامل</b> — في الصفحة اللي بعد تمارين النوع.']))
    h_rows = [['<span id="h-%s"></span>%s' % (e['dtag'], link('d-' + e['dtag'], '%s.%s ↩' % (e['num'], e['tag']))), rich(e['hint'])]
              for e in HELP]
    f_rows = [['<span id="f-%s"></span>%s' % (e['dtag'], link('d-' + e['dtag'], '%s.%s ↩' % (e['num'], e['tag']))),
               mi(e['step'][0]), rich(e['step'][1])] for e in HELP]
    return section('help', '🪜 سلّم المساعدة', intro
                   + '<h3>💡 الدرجة 1: تلميح العلامة</h3>' + table(['رقم', 'التلميح'], h_rows, 'help1')
                   + '<h3>✍️ الدرجة 2: أول خطوة</h3>' + table(['رقم', 'أول خطوة', 'ليش؟'], f_rows, 'help2'))


def keys():
    t_rows = [['<span id="k-%s"></span>%s' % (skill, link('alg-' + skill, title + ' ↩')), mi(r'\displaystyle ' + ans)]
              for skill, title, ans in TRY_KEYS]
    out = ''
    for anchor in ('speed42', 'speed51', 'speed52'):
        lesson, key = SPEED_KEYS[anchor]
        out += ('<h3 id="k-%s">مفتاح «وش الحالة؟»: أسئلة %s %s</h3>' % (anchor, lesson, link(anchor, '↩'))
                + table(['#', 'الحالة وأول سطر', 'الجواب (للتأكد فقط)'], key, 'answers'))
    out += ('<h3 id="k-mixed">أجوبة المراجعة المخلوطة %s</h3>' % link('mixed', '↩')
            + p('للتكاملات: اشتق جوابك؛ إذا رجع السؤال فهو صحيح (قد يختلف بثابت). للمشتقات: قارن حدًا حدًا. '
                'وإذا ما ضبط، افتح صفحة الحالة.', 'small')
            + table(['#', 'الحالة', 'الجواب'], MIXED_KEY, 'answers'))
    import guide_paths as GP
    out += GP.mastery_keys()
    out += '<h3>أجوبة «جرّب» في صناديق الجبر</h3>' + table(['المهارة', 'الجواب'], t_rows, 'answers')
    for ch, k_rows in PQ.KEYS:
        out += ('<h3 id="k-%s">أجوبة الاختبار السريع: قبل درس %s %s</h3>' % (ch, PQ.LESSON[ch], link(ch, '↩'))
                + table(['#', 'الجواب', 'الجزء'], k_rows, 'answers'))
    return section('keys', '🔑 المفاتيح', out)


def appendix():
    summ = json.loads((ROOT / 'reports' / 'registry_summary.json').read_text(encoding='utf-8'))
    gen = json.loads((ROOT / 'data' / 'generated_items.json').read_text(encoding='utf-8'))
    rows = [['الاختبارات المفهرسة', '18 (6 أولى، 6 ثانية، 6 نهائية) من ثلاثة ملفات 1445–1447'],
            ['أجزاء داخل النطاق في الاختبارات', '%d جزءًا، منها %d فريدًا' % (summ['in_scope_exam_parts'], summ['in_scope_exam_unique'])],
            ['أمثلة وتمارين مذكرة د. طارق في الأقسام الثلاثة', '%d مثالًا و %d تمرينًا' % (summ['notes_items']['notes_example'], summ['notes_items']['notes_exercise'])],
            ['في هذه المذكرة', '%d حالة في 4 طرق، و %d تمرينًا بحلول كاملة، و10 أجزاء «📚 أساس»' % (len(K.CASES), len(HELP))],
            ['تدريبات إضافية من إعداد هذه المذكرة', '%d، مكتوب عليها «تدريب إضافي»، وكل جواب متحقق بالطريقة نفسها' % len(gen)],
            ['الأسئلة المحجوزة للاختبارين التجريبيين', '%d، بالمعرفات <bdi dir="ltr">%s</bdi>؛ لا تظهر هنا'
             % (len(HOLD['hids']), ', '.join(HOLD['hids']))],
            ['فحوص الحاسوب', '%d فحصًا ناجحًا: كل جواب، وكل قانون، وكل مساواة في الخطوات' % len(LOG)]]
    notes = ul(['<b>K1 ✎:</b> دكتورك (محاضرة 13) ومذكرة د. طارق (ص58 وص60) يكتبون إشارة مشتقة coth⁻¹ وتكاملها سالبة؛ '
                'الصيغة اللوغاريتمية نفسها (محاضرة 13، ومذكرة د. طارق ص57) تعطي الموجبة، ومفتاح 1446 استخدم الموجبة. '
                'المذكرة تكتب إشارة دكتورك أول لأنه هو اللي يصحح، وتحتها الإشارة الرياضية.',
                '<b>K2:</b> بعض الحلول الرسمية تحذف القيمة المطلقة في sech⁻¹ و csch⁻¹ و ln، فتصح على جهة واحدة من المجال.',
                '<b>K3:</b> خطأ مطبعي في مذكرة د. طارق ص65 (سطر في مثال x sec⁻¹x) لا يغير الجواب.',
                'سطور «ليش؟» والكلام العربي كتبناها نحن؛ الحاسوب يفحص الرياضيات فقط. وفي صفحة أخطاء الجبر يفحص أيضًا أن كل «غلط» غلط فعلًا.'])
    return section('appendix', 'ملحق: المصادر والتحقق', table(['البند', 'القيمة'], rows, 'answers') + notes)


# common algebra mistakes: (wrong latex, right latex, why, (wrong lhs, wrong rhs) that must differ, right claims)
MISTAKES = [
    (r'\sqrt{x^{2}+9}=x+3', r'\sqrt{9x^{2}}=3|x|', 'الجذر يتوزع على الضرب فقط، ما يتوزع على الجمع',
     ('sqrt(x**2+9)', 'x+3'), [('sqrt(9*x**2)', '3*Abs(x)')]),
    (r'(1-u^{2})^{2}=1-u^{4}', r'(1-u^{2})^{2}=1-2u^{2}+u^{4}', 'لا تنسَ الحد الأوسط $2ab$',
     ('(1-u**2)**2', '1-u**4'), [('(1-u**2)**2', '1-2*u**2+u**4')]),
    (r'-(2x-3)=-2x-3', r'-(2x-3)=-2x+3', 'السالب يقلب إشارة <b>كل</b> حد داخل القوس',
     ('-(2*x-3)', '-2*x-3'), [('-(2*x-3)', '-2*x+3')]),
    (r'x^{-2}=-x^{2}', r'x^{-2}=\frac{1}{x^{2}}', 'الأس السالب مقلوب، مو إشارة سالبة',
     ('x**(-2)', '-x**2'), [('x**(-2)', '1/x**2')]),
    (r'e^{x}\cdot e^{2x}=e^{2x^{2}}', r'e^{x}\cdot e^{2x}=e^{3x}', 'في الضرب الأسس <b>تنجمع</b>',
     ('exp(x)*exp(2*x)', 'exp(2*x**2)'), [('exp(x)*exp(2*x)', 'exp(3*x)')]),
    (r'\frac{1}{x^{2}+4}=\frac{1}{x^{2}}+\frac14', r'\frac{x+2}{x^{2}}=\frac{1}{x}+\frac{2}{x^{2}}', 'نفصل البسط فقط؛ المقام ما ينفصل (النوع 8)',
     ('1/(x**2+4)', '1/x**2+Rational(1,4)'), [('(x+2)/x**2', '1/x+2/x**2')]),
    (r'\frac{2/3}{4/5}=\frac{8}{15}', r'\frac{2/3}{4/5}=\frac23\cdot\frac54=\frac56', 'القسمة على كسر = ضرب في مقلوبه',
     ('Rational(2,3)/Rational(4,5)', 'Rational(8,15)'), [('Rational(2,3)/Rational(4,5)', 'Rational(5,6)')]),
    (r'\ln(x^{2}+1)=\ln x^{2}+\ln1', r'\ln\left(x^{2}\right)=2\ln|x|', 'ln يفك الضرب والقوة، ما يفك الجمع',
     ('log(x**2+1)', 'log(x**2)+log(1)'), [('log(x**2)', '2*log(x)', 't')]),
    (r'\sinh^{-1}x=\frac{1}{\sinh x}', r'\frac{1}{\sinh x}=\operatorname{csch}x', 'الأس $-1$ على اسم الدالة معناه معكوس، مو مقلوب',
     ('asinh(x)', '1/sinh(x)'), [('1/sinh(x)', 'csch(x)')]),
    (r"\frac{d}{dx}\sinh^{-1}(3x)=\frac{1}{\sqrt{9x^{2}+1}}", r"\frac{d}{dx}\sinh^{-1}(3x)=\frac{3}{\sqrt{9x^{2}+1}}", "لا تنسَ $u'$ (قاعدة السلسلة)",
     ('diff(asinh(3*x),x)', '1/sqrt(9*x**2+1)'), [('diff(asinh(3*x),x)', '3/sqrt(9*x**2+1)')]),
    (r'\int\sin^{2}x\,dx=\frac{\sin^{3}x}{3}', r'\int\sin^{2}x\,dx=\frac{x}{2}-\frac{\sin2x}{4}', 'قاعدة القوة تحتاج مشتقة الداخل بجانبها (النوع 24)',
     ('diff(sin(x)**3/3,x)', 'sin(x)**2'), [('diff(x/2-sin(2*x)/4,x)', 'sin(x)**2')]),
    (r'\int x\cosh x\,dx=\frac{x^{2}}{2}\sinh x', r'\int x\cosh x\,dx=x\sinh x-\cosh x', 'التكامل ما يتوزع على الضرب: تجزئة (النوع 12)',
     ('diff(x**2/2*sinh(x),x)', 'x*cosh(x)'), [('diff(x*sinh(x)-cosh(x),x)', 'x*cosh(x)')]),
    (r'\int\frac{dx}{x^{2}}=\ln x^{2}', r'\int x^{-2}dx=\frac{x^{-1}}{-1}=-\frac1x', 'ln فقط مع $\\frac1x$؛ غيره قاعدة القوة',
     ('diff(log(x**2),x)', 'x**(-2)'), [('diff(-1/x,x)', 'x**(-2)')]),
    (r'\int3\cosh x\,dx=3x\sinh x', r'\int3\cosh x\,dx=3\sinh x', 'الثابت يطلع برّا كما هو، ما يصير $3x$',
     ('diff(3*x*sinh(x),x)', '3*cosh(x)'), [('diff(3*sinh(x),x)', '3*cosh(x)')]),
]


def differs(lhs, rhs, label):
    """A printed mistake must really be wrong: the two sides differ at sample points."""
    from booklet_engine import _record
    from mathlib import P, u, x
    d = P(lhs) - P(rhs)
    vals = [abs(complex(d.subs({x: v, u: v}).evalf())) for v in (0.7, 1.9)]
    _record('mistake', max(vals) > 1e-6, label=label, claim='%s != %s' % (lhs, rhs))


def mistakes():
    from booklet_engine import arith
    rows = []
    for k, (wrong, right, why, (wl, wr), claims) in enumerate(MISTAKES, 1):
        differs(wl, wr, 'mistake %d' % k)
        rows.append([mi(r'\displaystyle ' + wrong), mi(r'\displaystyle ' + arith(right, claims, 'mistake %d right' % k)), rich(why)])
    return section('mistakes', '❌ أخطاء الجبر الشائعة',
                   p('هذي الأغلاط تتكرر في الكويز. اقرأ الصف كاملًا: الغلط، ثم الصح، ثم ليش. كل «صح» فحصه الحاسوب، وكل «غلط» تأكد أنه غلط فعلًا.')
                   + table(['✗ غلط', '✓ صح', 'ليش؟'], rows, 'mistakes'))


def quiz_day():
    plan = '<ol>' + ''.join('<li>%s</li>' % t for t in [
        'اقرأ كل الأسئلة، واكتب جنب كل سؤال: مشتقة أو تكامل، والطريقة من ' + link('tree', 'الشجرة') + ' (في راسك).',
        'سؤال المشتقة: سطر $u$ و $u\'$، ثم القانون، ثم الجواب.',
        'التكاملات: ابدأ بالأسهل عليك.',
        'راجع: $+C$، والإشارات، و $|u|$. واشتق جواب تكامل واحد على الأقل وتأكد أنه يرجع السؤال.']) + '</ol>'
    body = (box('note', '🌙 الليلة قبل الكويز (الاثنين 26 أكتوبر)', ul([
                'اقرأ ' + link('night', 'صفحة مراجعة الليلة') + ' (الشجرة، والسكربتات، والتريكات)، ثم ' + link('errlog', 'سجل أخطائك') + '.',
                'لا تبدأ أسئلة جديدة.',
                'جهّز: قلمين، وممحاة، وبطاقتك الجامعية.']))
            + box('note', '☀️ صباح الكويز', ul([
                'اقرأ ' + link('tree', 'الشجرة') + ' وأول صفحة في كل طريقة مرة وحدة.',
                'اكتب من ذاكرتك على ورقة: الشجرة، والسكربتات الأربعة، وجدول مشتقات الدوال العكسية (و $\\coth^{-1}$ ✎ بإشارة دكتورك)، '
                'وجدول التكاملات الستة. ثم قارن.']))
            + box('short', '📝 في القاعة', plan)
            + box('warn', '🆘 إذا علقت داخل القاعة', ul([
                'اكتب أول سطر على الأقل ($u$ و $du$، أو $u$ و $dv$): قد يعطيك جزءًا من الدرجة، وغالبًا يفتح لك الباقي.',
                'اترك مكانًا وانتقل للسؤال اللي بعده، وارجع له في الآخر.',
                'لا تمسح شغلك: إذا غلطت اشطب بخط واحد واكتب الصح جنبه.'])))
    return section('quizday', '🎯 ' + TITLES['quizday'], rich(body), 'flow')

# 🔑 every type's trick in one line (the same tricks as in the 🧭 or 📐 box of each type)
# the cases added in v7 (no old number)
NEW_TRICKS = [
    ('U-LD', 'الأساس والأس فيهم $x$؟ خذ ln للطرفين، اشتق، واضرب في $y$ آخر شي.'),
    ('U-34', 'الرقم أول تحت الجذر ← $\\sin^{-1}$ (3.4). $x^2$ أول ← $\\cosh^{-1}$. و $u$ برّا الجذر: الرقم أول ← sech⁻¹، $x^2$ أول ← sec⁻¹.'),
    ('U-X2', 'بقى $x$ بعد التعويض؟ اكتبه بـ $u$: إذا $u=x^2+a$ فـ $x^2=u-a$.'),
    ('U-LN', 'ln لقوة أو جذر؟ نزّل الأس قدّام أول: $\\ln\\sqrt[3]x=\\frac13\\ln x$.'),
    ('U-CH', 'cosh أو sinh لحالها في المقام؟ اكتبها بالأسس، واضرب فوق وتحت في $e^x$، ثم $u=e^x$.')]

TRICKS = [
    ('1', 'sinh⁻¹ معها $\\sqrt{u^2+1}$، و cosh⁻¹ معها $\\sqrt{u^2-1}$. tanh⁻¹ و coth⁻¹ نفس الشكل $\\frac{1}{1-u^2}$. sech⁻¹ و csch⁻¹ فيها سالب و $u$ برّا الجذر. ودايم × مشتقة الداخل.'),
    ('2', 'اشتق من برّا لجوّا: كل طبقة مشتقتها، واضربها في بعض.'),
    ('3 إلى 7', 'رقم التعديل: البسط ناقصه رقم عشان يصير $du$؟ اقسم عليه برّا. واكتب اللي تحت الجذر كمربع: $9x^4=(3x^2)^2$.'),
    ('4', 'tanh⁻¹ أم coth⁻¹؟ $u$ أصغر من $a$ يعني tanh⁻¹، وأكبر يعني coth⁻¹.'),
    ('5', '$u$ برّا الجذر: الجواب يبدأ بسالب و $\\frac1a$، ومعه $|u|$.'),
    ('6', 'أسية تحت الجذر: اضرب فوق وتحت في جذرها ($e^{6x}=(e^{3x})^2$، فاضرب في $e^{3x}$).'),
    ('7', '$\\sqrt x$ ومعها $\\frac{1}{\\sqrt x}$: $u=\\sqrt x$، و $\\frac{dx}{\\sqrt x}=2\\,du$.'),
    ('8', 'بسط فيه جمع؟ افصل لكسرين، وكل واحد نوع لحاله.'),
    ('9', 'الدالة العكسية ومشتقتها مضروبتين: $u$ = الدالة، والجواب $\\frac{u^2}{2}$.'),
    ('10 و11', '⚡ المركز والباقي، أو «نص معامل $x$» للطريقة العادية.'),
    ('12', 'LIATE يختار $u$: ln، ثم دالة عكسية، ثم $x$، ثم sin و cos، ثم $e^x$.'),
    ('13', 'عمود I: $\\sin\\to-\\cos\\to-\\sin\\to\\cos$، ومع $kx$ اقسم على $k$ كل سطر.'),
    ('14 و15', 'LIATE: ln هي $u$. ومع ln وحدها $dv=dx$.'),
    ('16', 'احسب الجواب كامل، ثم عوّض الحدّين مرة وحدة. $\\ln1=0$، $e^0=1$، $\\sinh0=0$، $\\cosh0=1$.'),
    ('17', '$dv=dx$، والتكامل الباقي تعويض: $w$ = اللي تحت الجذر.'),
    ('18', 'أضف واطرح 1: $\\frac{x^2}{1+x^2}=1-\\frac{1}{1+x^2}$.'),
    ('19', 'نفس الاختيار في التجزئتين (المثلثية $u$).'),
    ('20', 'اكتب sinh أو cosh بالأسس، ووزّع: الأسس تنجمع.'),
    ('21', '$\\sqrt x$ داخل دالة: $t=\\sqrt x$، و $dx=2t\\,dt$.'),
    ('22 و23', 'احجز وحدة من صاحب الأس الفردي. الاثنين فرديين؟ من الأصغر. ومع sin يطلع سالب.'),
    ('24', 'سين وسالب: $\\sin^2$ معها ناقص، و $\\cos^2$ معها زائد، والزاوية تتضاعف.'),
    ('25 و26', 'sec زوجي: احجز $\\sec^2$ و $u=\\tan$. tan فردي: احجز $\\sec\\tan$ و $u=\\sec$.'),
    ('27', '⚡ سلسلة tan، و $\\sec^3$ «نص ونص».'),
    ('28', 'نفس tan و sec، بس مشتقة cot و csc فيها سالب.'),
    ('29', 'الضرب يصير جمع بزاويتين: الفرق والمجموع. و sin·sin الوحيدة اللي فيها ناقص.')]


def newnums(old):
    """«10 و11» or «3 إلى 7» (old type numbers) -> the new case numbers, smallest first."""
    out = K.renum(('الأنواع ' if (' و' in old or 'إلى' in old) else 'النوع ') + old)
    return out.split(' ', 1)[1]


def night():
    """The night before the quiz: the five quick ways with their memory lines, every trick, and the lesson maps."""
    from booklet_engine import arith
    quick = [['المركز والباقي', '10 و11', 'المركز يصفّر القوس، والباقي هو اللي يبقى.',
              arith(r'x^{2}+6x-16=(x+3)^{2}-25', [('x**2+6*x-16', '(x+3)**2-25')], 'night square')],
             ['جدول DI', '12 و13', 'D تنزل للصفر، I تتكامل، واضرب مايل $+\\ -\\ +$.',
              arith(r'\int x^{2}\cosh x=x^{2}\sinh x-2x\cosh x+2\sinh x', [('diff(x**2*sinh(x)-2*x*cosh(x)+2*sinh(x),x)', 'x**2*cosh(x)')], 'night di')],
             ['قوة × ln', '14 و15', 'كامل القوة، واضرب في ($\\ln$ ناقص واحد على نفس المقام).',
              arith(r'\int x^{2}\ln x=\frac{x^{3}}{3}\left(\ln x-\frac13\right)', [('diff(x**3/3*(log(x)-Rational(1,3)),x)', 'x**2*log(x)', 't')], 'night ln')],
             ['أسية × sin أو cos', '19', 'المقام $a^2+b^2$، والقوس: $a$ × الدالة ناقص مشتقتها.',
              arith(r'\int e^{2x}\sin x=\frac{e^{2x}}{5}\left(2\sin x-\cos x\right)', [('diff(exp(2*x)*(2*sin(x)-cos(x))/5,x)', 'exp(2*x)*sin(x)')], 'night exp')],
             ['سلسلة tan و sec³', '27', 'الأسس تنزل 2 2، كل حد على أسه، الإشارات تتبادل، والآخر $x$ أو $\\ln|\\sec x|$.',
              arith(r'\int\tan^{4}x=\frac{\tan^{3}x}{3}-\tan x+x', [('diff(tan(x)**3/3-tan(x)+x,x)', 'tan(x)**4')], 'night tan')]]
    rows = [[rich('<b>' + n + '</b>'), newnums(t), rich(m), mi(r'\displaystyle ' + ex)] for n, t, m, ex in quick]
    page = (p('بالليل: ' + link('tree', 'الشجرة') + '، ثم السكربتات الأربعة (أول صفحة في كل طريقة)، ثم '
              + link('fullmark', 'ورقة الدرجة الكاملة') + '، ثم سجل أخطائك. لا تبدأ أسئلة جديدة.')
            + '<h3>⚡ الطرق السريعة الخمس</h3>' + table(['الطريقة', 'الحالات', '🧠 جملة الحفظ', 'مثال'], rows, 'answers')
            + '<h3>🔑 كل التريكات</h3>' + table(['الحالة', 'التريك'], sorted([[newnums(n), rich(t)] for n, t in TRICKS]
                                                   + [[str(K.NUM[u]), rich(t)] for u, t in NEW_TRICKS if u in K.NUM],
                                                   key=lambda r: int(r[0].split()[0].strip('،'))), 'answers'))
    return section('night', '🌙 مراجعة ليلة الكويز', page, 'flow')


def end_sections():
    return stuck() + mistakes() + errlog() + keys() + appendix()     # v7: the laws sheet is the tree and the method pages

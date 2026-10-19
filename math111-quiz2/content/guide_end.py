"""المذكرة الكاملة — صفحات الأيام، سرعة الاختصار، المراجعة المخلوطة، ورقة القوانين، بطاقة القرار، إذا علقت، سجل الأخطاء، الملحق."""
import json
from pathlib import Path

import booklet as B
from booklet import final, sc_dawaran, sc_even, sc_lamda, sc_nisfayn, sc_pascal, sc_prod, sc_qaws, sc_rafeeq, sc_reduce, \
    sc_six, sc_small, sc_square, sc_twins
from booklet_engine import HOLD, ITEMS, LOG, ans_tex, q_tex
from guide_kit import ALG_SEEN, DAYS as UNIT_DAYS, pgref, question, rich
from html_kit import box, chip, en, lines, link, md, mi, p, table, ul

ROOT = Path(__file__).resolve().parent.parent

EXTRA_TOC = {3: [('speed42', 'سرعة الاختصار: 4.2')], 5: [('speed51', 'سرعة الاختصار: 5.1')],
             6: [('speed52', 'سرعة الاختصار: 5.2'), ('mockA', 'الاختبار التجريبي A')],
             7: [('mixed', 'المراجعة المخلوطة'), ('mockB', 'الاختبار التجريبي B')]}
END_TOC = [('formulas', 'ورقة القوانين والاختصارات'), ('decide', 'بطاقة القرار: أي نوع؟'), ('stuck', 'إذا علقت'),
           ('errlog', 'سجل الأخطاء'), ('appendix', 'ملحق: المصادر والتحقق')]

WARM = {2: ['1445-S2-SE-Q1.1', 'N42-E1-3'], 3: ['N42-E1-2', 'N42-X2-04'], 4: ['N42-X1-5', '1445-S2-SE-Q2.2'],
        5: ['N51-X06', '1445-S2-SE-Q1.2'], 6: ['1446-S1-FE-Q2.2', 'N42-X1-6']}

SPEED = {
    'speed42': ('4.2', [('N42-X2-13', 'النوع 10: $h=-3$، $d=-9$ ⇐ cosh، $a=3$'),
                        ('1446-S2-SE-Q2.2', 'النوع 10: $h=-1$، $d=9$ ⇐ sinh، $a=3$'),
                        ('N42-E2-7', 'النوع 10: $h=-1$، $d=-9$ ⇐ cosh، $a=3$'),
                        ('1447-S1-SE-Q2.4', 'النوع 11: $h=3$، $d=16$، معامل $x^2$ سالب ⇐ sech'),
                        ('N42-X2-05', 'النوع 5: $u=3x^2$، $a=2$، داخل الجذر ناقص ⇐ sech'),
                        ('N42-E1-7', 'النوع 2: ضرب دالتين، و $u=5x$'),
                        ('N42-X1-3', 'النوع 2: قوة، ثم tanh⁻¹ مع $u=3x$'),
                        ('1445-S1-FE-Q1.3', 'النوعان 1 و 2: sinh⁻¹ مع $u=3^x$، ثم ln'),
                        ('1447-S2-SE-Q1.1', 'النوع 1: $u=\\ln|x+1|$'),
                        ('1447-S2-SE-Q3.4', 'النوع 11: $h=2$، $d=2$ ⇐ sech، $a=\\sqrt2$')]),
    'speed51': ('5.1', [('N51-X01', 'النوع 12: $p=2$، $G_1=\\sinh x$'),
                        ('G-22', 'النوع 14: $n=4$'),
                        ('N51-E5', 'النوع 17: الرفيق'),
                        ('N51-X08', 'النوع 17: الرفيق'),
                        ('G-17', 'النوع 12: $p=1$، $G_1=-e^{-x}$'),
                        ('G-18', 'النوع 13: جدول DI'),
                        ('G-19', 'النوع 19: $a=3$، $b=1$'),
                        ('G-20', 'النوع 20: $a=2$، $b=1$'),
                        ('G-21', 'النوع 17: الرفيق')]),
    'speed52': ('5.2', [('N52-X11', 'النوع 29: sin·sin، $m=2$، $n=6$'),
                        ('N52-X04', 'النوع 23: $u=\\cos x$، و $\\sqrt[3]{\\cos x}=u^{1/3}$'),
                        ('G-23', 'النوع 23: sin فردي ⇐ $u=\\cos x$'),
                        ('G-24', 'النوع 27: $\\tan^2x=\\sec^2x-1$'),
                        ('G-25', 'النوع 28: csc زوجي ⇐ $u=\\cot x$'),
                        ('G-26', 'النوع 29: $m=5$، $n=2$'),
                        ('G-27', 'النوع 24: نصف الزاوية'),
                        ('G-28', 'النوع 28: cot فردي ⇐ $u=\\csc x$')])}

MIXED = [('1445-S2-FE-Q1.3', 'النوعان 1 و 2'), ('1446-S2-SE-Q1.1', 'النوع 1 + 4.1'), ('N42-E1-8', 'النوع 2: قسمة'),
         ('N42-X1-2', 'النوع 2: ضرب'), ('G-29', 'النوع 10'), ('G-30', 'النوع 5'), ('G-31', 'النوع 12'), ('G-32', 'النوع 19'),
         ('G-37', 'النوع 16'), ('G-33', 'النوع 23'), ('G-34', 'النوع 27'), ('G-35', 'النوع 29')]


def section(id_, title, inner, cls=''):
    return '<section class="chapter %s" id="%s"><h2>%s</h2>%s</section>' % (cls, id_, title, inner)


def day_schedule(d, n_units):
    rows = [['5 دقائق', 'اقرأ صفحة "كيف تستخدم المذكرة"' if d == 1 else '🔁 الإحماء تحت: اكتب الاختصارات من ذاكرتك وحل سؤالي المراجعة']]
    for _, num, title in UNIT_DAYS.get(d, []):
        rows.append(['25 دقيقة', 'النوع %d (%s): الفكرة ← المثال ← التمارين ← الحلول' % (num, title)])
        rows.append(['5 دقائق', 'راحة: قم من مكانك واشرب ماء'])
    for anchor, title in EXTRA_TOC.get(d, []):
        if anchor.startswith('speed'):
            rows.append(['10 دقائق', title])
        elif anchor.startswith('mock'):
            rows.append(['60 + 15 دقيقة', title + ' في الملف المنفصل، ثم التصحيح'])
        elif anchor == 'mixed':
            rows.append(['45 دقيقة', title])
    if d == 7:
        rows.append(['20 دقيقة', 'اقرأ ورقة القوانين وسجل أخطائك'])
    rows.append(['5 دقائق', 'سجّل أخطاء اليوم في سجل الأخطاء'])
    return rows


def warmup(d):
    learned = [t for dd in sorted(UNIT_DAYS) if dd < d for _, _, t in UNIT_DAYS[dd]]
    body = p('اكتب على ورقة جانبية، بدون ما تفتح المذكرة: اسم كل نوع درسته واختصاره في سطر.')
    if learned:
        body += p('<b>الأنواع اللي درستها:</b> ' + '، '.join(learned) + '.', 'small')
    if d in WARM:
        qs, keys = '', []
        for k, item_id in enumerate(WARM[d], 1):
            it = ITEMS[item_id]
            qs += '<div class="ch"><b>مراجعة %d</b>%s%s%s</div>' % (k, chip(B.source_label(it), 'src'), md(q_tex(question_used(it, 'day %d warm-up' % d))),
                                                                 lines(2, 'write tight'))
            final(it, 'day %d warm-up' % d)
            keys.append(mi(ans_tex(it, with_lhs=False).lstrip('= ')))
        body += '<div class="chgrid">' + qs + '</div>'
        body += '<div class="hint"><span class="flip">✅ الأجوبة: ' + ' &nbsp;|&nbsp; '.join(keys) + '</span></div>'
    return box('memo', '🔁 الإحماء (5 دقائق)', body)


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
    page = (p(rich('لا تحل. اكتب تحت كل سؤال <b>رقم النوع</b> و<b>الأرقام المهمة</b> فقط (مثل $u$ و $a$ و $p$). '
                   'الهدف أن تعرف النوع في ثوانٍ. المفتاح في الصفحة التالية.'))
            + '<div class="chgrid">' + qs + '</div>'
            + '<section class="sols"><h4>مفتاح سرعة الاختصار: %s</h4>' % lesson
            + table(['#', 'النوع والأرقام', 'الجواب (للتأكد فقط)'], key, 'answers') + '</section>')
    return section(anchor, '⚡ سرعة الاختصار: %s' % lesson, page, 'flow')


def after_lesson(lesson):
    return speed_page({'4.2': 'speed42', '5.1': 'speed51', '5.2': 'speed52'}[lesson])


def mock_box(which):
    anchor = 'mock' + which
    body = ul(['افتح ملف <b>الاختبارين التجريبيين</b>، الاختبار %s.' % which,
               '60 دقيقة بالضبط (اضبط منبهًا)، بدون مذكرة وبدون ورقة قوانين وبدون آلة حاسبة.',
               'بعد الوقت: صحّح من صفحة الحلول في نفس الملف، وسجّل كل غلطة في ' + link('errlog', 'سجل الأخطاء') + '.',
               'أي نوع غلطت فيه: ارجع لصفحته في المذكرة وحل تمرينه الثالث مرة ثانية.'])
    return section(anchor, '📝 الاختبار التجريبي %s' % which, box('warn', 'التعليمات', body), 'flow')


def mixed_page():
    qs, key = '', []
    for k, (item_id, kind) in enumerate(MIXED, 1):
        it = ITEMS[item_id]
        qs += '<div class="ch"><b>%d</b>%s%s</div>' % (k, md(q_tex(question_used(it, 'mixed review'))), lines(4, 'write tight'))
        key.append([str(k), rich(kind), mi(r'\displaystyle ' + ans_tex(it, with_lhs=False).lstrip('= '))])
        final(it, 'mixed review')
    page = (p('12 سؤالًا من الدروس الثلاثة بدون عناوين، مثل الكويز. لكل سؤال: حدّد النوع، ثم حل. الوقت المقترح 45 دقيقة.')
            + '<div class="chgrid">' + qs + '</div>'
            + '<section class="sols"><h4>أجوبة المراجعة المخلوطة</h4>'
            + p('إذا اختلف جوابك: اشتقه؛ إذا رجع السؤال فهو صحيح (قد يختلف بثابت). وإلا افتح صفحة النوع.', 'small')
            + table(['#', 'النوع', 'الجواب'], key, 'answers') + '</section>')
    return section('mixed', '🔀 المراجعة المخلوطة', page)


def after_day(d):
    out = ''
    if d == 6:
        out += mock_box('A')
    if d == 7:
        out += mixed_page() + mock_box('B')
    return out


def formulas():
    parts = []
    for title, fns in [('4.2', [sc_twins, sc_six, sc_lamda, sc_square]),
                       ('5.1', [sc_qaws, sc_rafeeq, sc_dawaran, sc_nisfayn, sc_small]),
                       ('5.2', [sc_pascal, sc_even, sc_reduce, sc_prod])]:
        inner = p('<b>الخطي و DI:</b> ' + rich('$\\int(px+q)\\,g\\,dx=(px+q)G_1-pG_2$؛ ومع $x^2$ أو $x^3$ جدول DI.')) if title == '5.1' else ''
        for fn in fns:
            short, _ = fn()
            inner += '<div class="fsheet">' + short + '</div>'
        parts.append('<h3>%s</h3>' % title + inner)
    return section('formulas', '📋 ورقة القوانين والاختصارات',
                   p('اقرأها يوم 26 ومرة صباح الكويز. لا تُدخل معك القاعة.', 'small') + ''.join(parts))


DECIDE = [
    (r"y=\ldots\sinh^{-1}(u)\ldots", 1), (r"y=a^{(\ldots)},\ \ln|\ldots|,\ (\ldots)^{n},\ f\cdot g", 2),
    (r'\int\frac{c}{\sqrt{u^{2}\pm a^{2}}}', 3), (r'\int\frac{du}{a^{2}-u^{2}}', 4), (r'\int\frac{dx}{x\sqrt{a^{2}\pm x^{n}}}', 5),
    (r'\int\frac{dx}{\sqrt{e^{kx}\pm a^{2}}}', 6), (r'\int\frac{dx}{\sqrt{x}\sqrt{a^{2}+x}}', 7), (r'\int\frac{px+q}{\sqrt{\ldots}}', 8),
    (r'\int f^{-1}\cdot\left(f^{-1}\right)' "'", 9), (r'\int\frac{c}{\sqrt{Ax^{2}+Bx+D}}', 10), (r'\int\frac{c}{(x-h)\sqrt{Ax^{2}+Bx+D}}', 11),
    (r'\int(px+q)\cdot e^{kx},\ \sin,\ \cosh\ldots', 12), (r'\int x^{2}\cdot\ldots,\ \int x^{3}\cdot\ldots', 13),
    (r'\int x^{n}\ln|ax|', 14), (r'\int\ln|x|,\ (\ln|x|)^{2},\ \ln(1+x^{2})', 15), (r'\int_{a}^{b}\ldots', 16),
    (r'\int f^{-1}(x)\,dx', 17), (r'\int x\,f^{-1}(x)\,dx', 18), (r'\int e^{ax}\sin bx,\ e^{ax}\cos bx', 19),
    (r'\int e^{ax}\sinh bx,\ e^{ax}\cosh bx', 20), (r'\int e^{\sqrt x},\ \int x^{3}\sqrt{x^{2}+c}', 21),
    (r'\int\sin^{\text{odd}}x,\ \int\cos^{\text{odd}}x', 22), (r'\int\sin^{m}x\cos^{n}x\ (\text{one odd})', 23),
    (r'\int\sin^{2}x,\ \cos^{4}x,\ \sin^{2}x\cos^{2}x', 24), (r'\int\tan^{m}x\sec^{\text{even}}x', 25),
    (r'\int\tan^{\text{odd}}x\sec^{n}x', 26), (r'\int\tan^{n}x,\ \int\sec^{\text{odd}}x', 27), (r'\int\cot^{m}x\csc^{n}x', 28),
    (r'\int\sin mx\cos nx\ \ldots', 29)]


def decide():
    num_to = {num: (uid, title) for d in UNIT_DAYS.values() for uid, num, title in d}
    rows = [[mi(r'\displaystyle ' + shape), link(num_to[n][0], '%d. %s' % (n, num_to[n][1])), pgref(num_to[n][0])] for shape, n in DECIDE]
    return section('decide', '🧭 بطاقة القرار: أي نوع؟', p('شوف شكل السؤال، وروح للنوع.') + table(['شكل السؤال', 'النوع', 'ص'], rows, 'answers'))


def stuck():
    skills = '، '.join(link('alg-' + k, t) for k, t in ALG_SEEN.items())
    body = ul(['<b>ما عرفت النوع؟</b> ' + link('decide', 'بطاقة القرار') + '.',
               '<b>عرفت النوع ونسيت الاختصار؟</b> استخدم 🧱 الطريقة الأساسية في صفحة النوع، أو ' + link('formulas', 'ورقة القوانين') + '.',
               '<b>الجبر وقفك؟</b> صناديق 🧮: ' + skills + '.',
               '<b>جوابك يختلف عن الحل؟</b> اشتق جوابك. إذا رجع السؤال فهو صحيح (قد يختلف بثابت). وإلا ابحث عن الإشارة أو المعامل.',
               rich('<b>tanh⁻¹ أم coth⁻¹؟</b> قارن $|u|$ مع $a$.'),
               rich('<b>نسيت الإشارة في sin و cos؟</b> $\\int\\sin=-\\cos$ و $\\int\\cos=\\sin$؛ و sinh و cosh بدون سالب.'),
               rich('<b>في الكويز:</b> ابدأ بالسؤال الأسهل (المشتقات عادة أسرع). لا تترك سؤالًا فاضيًا: الخطوة الأولى الصحيحة '
                    '(مثل $u$ و $du$، أو $u$ و $dv$) أفضل من ورقة فاضية.')])
    return section('stuck', '🆘 إذا علقت', body)


def errlog():
    rows = [['', '', '', ''] for _ in range(14)]
    intro = p('كل غلطة تكتبها هنا مرة واحدة. نوع الغلطة: <b>فهم</b> (ما فهمت الفكرة)، <b>اختيار</b> (اخترت النوع الغلط)، '
              '<b>استرجاع</b> (نسيت القانون)، <b>جبر</b> (حساب أو إشارة). راجع هذه الصفحة يوم 26.')
    return section('errlog', '📒 سجل الأخطاء', intro + table(['التمرين (والصفحة)', 'وش صار', 'نوع الغلطة', 'الصح'], rows, 'errlog'))


def appendix():
    summ = json.loads((ROOT / 'reports' / 'registry_summary.json').read_text(encoding='utf-8'))
    gen = json.loads((ROOT / 'data' / 'generated_items.json').read_text(encoding='utf-8'))
    rows = [['الاختبارات المفهرسة', '18 (6 أولى، 6 ثانية، 6 نهائية) من ثلاثة ملفات 1445–1447'],
            ['أجزاء داخل النطاق في الاختبارات', '%d جزءًا، منها %d فريدًا' % (summ['in_scope_exam_parts'], summ['in_scope_exam_unique'])],
            ['عناصر المذكرة', '%d مثالًا و %d تمرينًا في 4.2 و 5.1 و 5.2' % (summ['notes_items']['notes_example'], summ['notes_items']['notes_exercise'])],
            ['تدريبات إضافية من إعداد هذه المذكرة', '%d، كل جواب متحقق بالطريقة نفسها' % len(gen)],
            ['الأسئلة المحجوزة للاختبارين التجريبيين', '%d، بالمعرفات <bdi dir="ltr">%s</bdi>؛ لا تظهر هنا'
             % (len(HOLD['hids']), ', '.join(HOLD['hids']))],
            ['فحوص البناء', '%d فحصًا ناجحًا لكل صيغة وخطوة وجواب في هذه المذكرة' % len(LOG)]]
    notes = ul(['<b>K1:</b> المذكرة ص58 وص60 تكتب إشارة مشتقة coth⁻¹ وتكاملها بالعكس؛ الصيغة اللوغاريتمية في المذكرة نفسها (ص57) '
                'تعطي الموجبة. مفتاح 1445 تبع المذكرة ومفتاح 1446 استخدم الموجبة. اسأل الدكتور.',
                '<b>K2:</b> بعض الحلول الرسمية تحذف القيمة المطلقة في sech⁻¹ و csch⁻¹ و ln، فتصح على جهة واحدة من المجال.',
                '<b>K3:</b> خطأ مطبعي في المذكرة ص65 (سطر في مثال x sec⁻¹x) لا يغير الجواب.'])
    return section('appendix', 'ملحق: المصادر والتحقق', table(['البند', 'القيمة'], rows, 'answers') + notes)


def end_sections():
    return formulas() + decide() + stuck() + errlog() + appendix()

#!/usr/bin/env python3
"""Assemble the shortcuts booklet (sample stage) as HTML with math placeholders.

Run: python tools/render_booklet.py  ->  src/booklet.html (math as data-tex placeholders)
Then: node tools/render_math.mjs src/booklet.html out/booklet.katex.html ; node tools/export_pdf.mjs ...
Every formula/answer is checked while building; a failed check aborts (reports/booklet_checks.json).
"""
import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'content'))

import booklet as B  # noqa: E402
from booklet_engine import HOLD, ITEMS, arith, formula, write_log  # noqa: E402
from html_kit import box, chip, en, lines, link, md, mi, p, table, ul  # noqa: E402

TODAY = datetime.date(2026, 10, 19)


def section(id_, title, inner, cls=''):
    return '<section class="chapter %s" id="%s"><h2>%s</h2>%s</section>' % (cls, id_, title, inner)


def cover():
    return ('<section class="cover" id="top"><div class="kicker">ريض 111 · الكويز الثاني · الثلاثاء 27 أكتوبر 2026</div>'
            '<h1>كرّاسة الاختصارات</h1>'
            '<div class="sub">4.2 الدوال الزائدية العكسية · 5.1 التكامل بالتجزئة · 5.2 التكاملات المثلثية</div>'
            + box('note', 'لمن هذه الكرّاسة', p('لزياد. كل حالة في الدروس الثلاثة لها اختصار يعطي الجواب مباشرة، ومعه علامة تعرف بها '
                                                'متى تستخدمه، ومثال من سؤال حقيقي، وطريقة كتابته في ورقة الكويز.'))
            + box('note', 'هل الاختصارات صحيحة؟', p('نعم. كل اختصار هنا تحققنا منه رياضيًا بالحاسوب، ثم جربناه على أسئلة الاختبارات السابقة '
                                                     'وتمارين المذكرة. لا تحتاج أن تحفظ البرهان؛ احفظ العلامة والاختصار.'))
            + box('warn', 'عينة للموافقة', p('هذه النسخة الأولى (العينة). بعد موافقتك تُبنى المذكرة الكاملة حول هذه الاختصارات، '
                                             'ومعها الاختباران التجريبيان وخطة المذاكرة.'))
            + '<div class="meta">المصادر: مذكرة د. طارق الفضل (2024) واختبارات المقرر 1445–1447. تاريخ الإصدار: %s</div></section>'
            % TODAY.isoformat())


def how_to_use():
    steps = ul(['ابدأ كل جلسة بصفحة ' + link('recall', 'اكتب من الذاكرة') + ' (5 دقائق) قبل أن تفتح البطاقات.',
                'اقرأ البطاقة: <b>العلامة</b> أولًا، ثم <b>الاختصار</b>، ثم غطِّ المثال وحاول حله.',
                'حل تدريب ' + link('choose', 'اختر الاختصار') + ' دون حساب: اكتب اسم الاختصار والأرقام فقط.',
                'ثم التدريب ' + link('apply', 'الموجّه فالناقص فالمستقل') + '. إذا تعطلت: '
                + link('help', 'سلّم المساعدة') + ' بثلاث درجات (تلميح، أول خطوة، حل كامل)، وارجع بعد كل درجة وحاول وحدك.'])
    legend = table(['المربع', 'معناه'], [
        [chip('العلامة: متى أستخدمه؟', 'k-sign'), 'شكل السؤال الذي يناسب الاختصار.'],
        [chip('الاختصار', 'k-short'), 'القاعدة التي تعطي الجواب.'],
        [chip('كيف أتذكّره', 'k-memo'), 'جملة قصيرة تساعد الذاكرة.'],
        [chip('مثال من سؤال حقيقي', 'k-ex'), 'سؤال من اختبار سابق أو من المذكرة، بالأرقام.'],
        [chip('الفخ', 'k-trap'), 'متى يخطئ الاختصار أو أين يخطئ الطلاب.'],
        [chip('في ورقة الكويز', 'k-paper'), 'ما تكتبه حتى يرى المصحح خطواتك.'],
        [chip('لو نسيت الاختصار', 'k-fallback'), 'الطريقة الأساسية من المذكرة.']], 'legend')
    note = box('warn', 'عن الكتابة في الكويز', p('لا نعرف سياسة المصحح في قبول الجواب وحده، لذلك في كل بطاقة سطران أو ثلاثة '
                                                  'تكتبها قبل الجواب. استخدم الاختصار لتعرف الجواب بسرعة وتتحقق منه.'))
    return section('howto', 'كيف تستخدم الكرّاسة', steps + legend + note)


def toc(entries):
    rows = ''.join('<li class="lvl%d"><a href="#%s"><span class="t">%s</span><span class="pg" data-target="%s"></span></a></li>'
                   % (lvl, a, t, a) for lvl, a, t in entries)
    return '<section class="toc" id="toc"><h2>المحتويات</h2><ol>%s</ol></section>' % rows


def foundations():
    reading = table(['في الورقة', 'معناه'], [
        [en('Find dy/dx of the following'), 'أوجد المشتقة'],
        [en("Find f'(x)  /  Find y'"), 'أوجد المشتقة'],
        [en('Find the derivative of the following functions'), 'أوجد مشتقة كل دالة'],
        [en('Evaluate the following integrals'), 'احسب التكاملات (غير المحدد: أضف C)'],
        [en('integral with limits a and b'), 'تكامل محدد: الجواب عدد'],
    ], 'glossary')
    symbols = ul([mi(r'\sinh^{-1}x') + ' دالة عكسية، وليست ' + mi(r'\frac{1}{\sinh x}') + ' (هذه ' + mi(r'\operatorname{csch}x') + ').',
                  mi(r'\operatorname{sech}x=\frac{1}{\cosh x}') + '، ' + mi(r'\operatorname{csch}x=\frac{1}{\sinh x}') + '، '
                  + mi(r'\coth x=\frac{\cosh x}{\sinh x}') + '.',
                  mi('|u|') + ' القيمة المطلقة: تُكتب عندما يمكن أن يكون ' + mi('u') + ' سالبًا.'])
    d41 = [formula('sinh(u)', 'cosh(u)', 'diff', branches=('x',), uprime=True, label='4.1 sinh'),
           formula('cosh(u)', 'sinh(u)', 'diff', branches=('x',), uprime=True, label='4.1 cosh'),
           formula('tanh(u)', 'sech(u)**2', 'diff', branches=('x',), uprime=True, label='4.1 tanh'),
           formula('coth(u)', '-csch(u)**2', 'diff', branches=('t',), uprime=True, label='4.1 coth'),
           formula('sech(u)', '-sech(u)*tanh(u)', 'diff', branches=('x',), uprime=True, label='4.1 sech'),
           formula('csch(u)', '-csch(u)*coth(u)', 'diff', branches=('t',), uprime=True, label='4.1 csch')]
    prereq = table(['المشتقة', 'تساوي'], [[mi(r'\displaystyle ' + a), mi(r'\displaystyle ' + b)] for a, b in d41], 'formula compact')
    prereq += p('الإشارة السالبة مع coth و sech و csch فقط. و ' + mi(r'\int\sinh x\,dx=\cosh x') + '، ' + mi(r'\int\cosh x\,dx=\sinh x') + '.', 'small')
    alg = table(['المهارة', 'مثال', 'تحقق بنفسك'], [
        ['القسمة على كسر', mi(arith(r'\frac{5}{3\cdot4}=\frac{5}{12}', [('Rational(5,3*4)', 'Rational(5,12)')], 'alg1')),
         'F1: ' + mi(r'\frac{1}{1/4}=?') + ' ' + link('fa-F1', 'الجواب', 'help')],
        ['الأس السالب', mi(arith(r'x^{-2}=\frac{1}{x^{2}},\quad \int x^{-2}dx=-x^{-1}', [('x**(-2)', '1/x**2'), ('integrate(x**(-2),x)', '-1/x')], 'alg2')),
         'F2: ' + mi(r'\int x^{-3}dx=?') + ' ' + link('fa-F2', 'الجواب', 'help')],
        ['الجذر أس', mi(arith(r'\sqrt{x}=x^{1/2},\quad \frac{1}{\sqrt x}=x^{-1/2}', [('sqrt(x)', 'x**Rational(1,2)')], 'alg3')),
         'F3: ' + mi(r'(1-u^{2})^{2}=?') + ' ' + link('fa-F3', 'الجواب', 'help')],
        ['قاعدة السلسلة', mi(arith(r'\frac{d}{dx}\cosh(3x^{2})=6x\sinh(3x^{2})', [('diff(cosh(3*x**2),x)', '6*x*sinh(3*x**2)')], 'alg4')),
         'F4: ' + mi(r'\frac{d}{dx}\tanh(x^{3})=?') + ' ' + link('fa-F4', 'الجواب', 'help')],
        ['الإشارات', mi(r'-(-a)=+a,\quad -(a-b)=-a+b'), 'F5: ' + mi(r'-\frac{1}{-3}=?') + ' ' + link('fa-F5', 'الجواب', 'help')]], 'skills')
    inner = (box('short', 'قراءة السؤال الإنجليزي', reading) + box('memo', 'رموز', symbols)
             + box('ex', 'من درس 4.1 (متطلب سابق)', prereq) + box('paper', 'جبر تحتاجه الاختصارات', alg))
    return section('basics', 'أساسيات مصغرة', inner)


def cards_part():
    groups = [('g42', '4.2 الدوال الزائدية العكسية', range(0, 4)), ('g51', '5.1 التكامل بالتجزئة', range(4, 10)),
              ('g52', '5.2 التكاملات المثلثية', range(10, 14))]
    out = []
    for gid, title, idx in groups:
        out.append(section(gid, title, ''.join(B.CARDS[i]() for i in idx), 'group'))
    return ''.join(out)


def drills_part():
    choose = ''.join('<div class="ch" id="c-C%d"><b>C%d</b>%s%s</div>' % (i, i, B.md(B.q_tex(ITEMS[k])), lines(1, 'write short'))
                     for i, k in enumerate(B.CHOOSE, 1))
    for k in B.CHOOSE:
        B.use(k, 'choose drill')
    ch = section('choose', 'اختر الاختصار (دون حساب)', p('اكتب بجانب كل سؤال: اسم الاختصار والأرقام المهمة فقط. لا تحل. الأسئلة مختلطة عمدًا، '
                                                          'وبعضها لا يحتاج اختصارًا. ' + link('ch-ans', 'الإجابات في قسم المساعدة', 'help'))
                 + '<div class="chgrid">' + choose + '</div>')
    groups = {'موجّه': [], 'ناقص الخطوات': [], 'مستقل': []}
    for tag, k, level in B.tagged_drills():
        groups[level].append(B.drill_block(tag, k, level))
    ap = section('apply', 'طبّق', box('note', 'الترتيب', p('موجّه (البداية مكتوبة) ← ناقص الخطوات ← مستقل. الحلول في آخر الكرّاسة، '
                                                          'ولا تفتح الحل الكامل قبل التلميح والخطوة الأولى.'))
                 + '<h3>موجّه</h3>' + ''.join(groups['موجّه']) + '<h3>ناقص الخطوات</h3>' + ''.join(groups['ناقص الخطوات'])
                 + '<h3>مستقل</h3>' + ''.join(groups['مستقل']))
    return ch + ap


def recall_part():
    cards = ''.join('<div class="fc"><div class="front"><b>%d</b> %s</div><div class="back">%s</div></div>'
                    % (i, B.SIGNS[i - 1], link('S%d' % i, B.NAMES[i - 1], 'card')) for i in range(1, 15))
    flash = section('flash', 'بطاقات الاسترجاع', p('غطِّ العمود الأيسر واقرأ العلامة، ثم قل اسم الاختصار واكتب صيغته على ورقة جانبية. '
                                                    'افتح البطاقة للتأكد.') + '<div class="fcgrid">' + cards + '</div>')
    boxes = ''.join('<div class="rb"><div class="rn">%d. %s</div>%s</div>' % (i, B.NAMES[i - 1], lines(2, 'write tight'))
                    for i in range(1, 15))
    recall = section('recall', 'اكتب من الذاكرة', p('في بداية كل جلسة: اكتب الاختصار تحت كل اسم دون النظر. ما نسيته عُد إلى بطاقته، '
                                                    'ثم اكتبه مرة أخرى في نهاية الجلسة. اطبع نسخًا من هذه الصفحة أو اكتب على نسخة مكررة.')
                     + '<div class="rgrid">' + boxes + '</div>')
    return flash + recall


def help_part():
    hints, firsts, fulls = B.help_sections()
    fa = table(['', 'الجواب'], [
        ['<span id="fa-F1">F1</span>', mi(arith('4', [('1/(Rational(1,4))', '4')], 'F1'))],
        ['<span id="fa-F2">F2</span>', mi(arith(r'-\frac{1}{2x^{2}}+C', [('integrate(x**(-3),x)', '-1/(2*x**2)')], 'F2'))],
        ['<span id="fa-F3">F3</span>', mi(arith(r'1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')], 'F3'))],
        ['<span id="fa-F4">F4</span>', mi(arith(r'3x^{2}\operatorname{sech}^{2}(x^{3})', [('diff(tanh(x**3),x)', '3*x**2*sech(x**3)**2')], 'F4'))],
        ['<span id="fa-F5">F5</span>', mi(arith(r'\frac13', [('-1/(-3)', 'Rational(1,3)')], 'F5'))]], 'answers')
    inner = (box('note', 'كيف تستخدم المساعدة', p('خذ درجة واحدة فقط، ثم ارجع للتمرين واكتب خطوتك التالية بنفسك. '
                                                  'الحل الكامل للمقارنة بعد أن تحاول.'))
             + '<h3 id="ch-ans">إجابات «اختر الاختصار»</h3>' + B.choose_answers()
             + '<h3>إجابات الأساسيات</h3>' + fa
             + '<h3 id="ladder1">الدرجة 1: تلميح</h3>' + ''.join(hints)
             + '<h3 id="ladder2">الدرجة 2: أول خطوة مكتوبة</h3>' + ''.join(firsts)
             + '<h3 id="ladder3">الدرجة 3: الحل الكامل</h3>' + ''.join(fulls))
    return section('help', 'سلّم المساعدة', inner)


def appendix():
    summ = json.loads((ROOT / 'reports' / 'registry_summary.json').read_text(encoding='utf-8'))
    ver = json.loads((ROOT / 'reports' / 'verification_report_items.json').read_text())['items_summary']
    rows = [['الاختبارات المفهرسة', '18 (6 أولى، 6 ثانية، 6 نهائية) من ثلاثة ملفات 1445–1447'],
            ['أجزاء داخل النطاق في الاختبارات', '%d جزءًا، منها %d فريدًا' % (summ['in_scope_exam_parts'], summ['in_scope_exam_unique'])],
            ['عناصر المذكرة', '%d مثالًا و %d تمرينًا في 4.2 و 5.1 و 5.2' % (summ['notes_items']['notes_example'], summ['notes_items']['notes_exercise'])],
            ['الأسئلة المحجوزة للاختبارين التجريبيين', '%d، بالمعرفات <bdi dir="ltr">%s</bdi>؛ لا تظهر هنا ولا يُكتب حلها'
             % (len(HOLD['hids']), ', '.join(HOLD['hids']))],
            ['التحقق من إجاباتنا', '%d من %d تحقق رمزي على كل جزء من المجال الحقيقي' % (ver['answer'].get('symbolic', 0), sum(ver['answer'].values()))],
            ['الحلول الرسمية وحلول المذكرة', '%d صحيحة كاملًا؛ %d صحيحة على جهة واحدة فقط؛ %d خاطئة بسبب إشارة coth⁻¹'
             % (ver['official'].get('symbolic', 0), ver['official'].get('branch_only', 0) + ver['official'].get('partial_domain', 0),
                ver['official'].get('failed', 0))]]
    notes = ul(['<b>K1:</b> المذكرة ص58 وص60 تكتب إشارة مشتقة coth⁻¹ وتكاملها بالعكس؛ الصيغة اللوغاريتمية في المذكرة نفسها (ص57) تعطي الموجبة. '
                'مفتاح 1445 تبع المذكرة ومفتاح 1446 استخدم الموجبة.',
                '<b>K2:</b> بعض الحلول الرسمية تحذف القيمة المطلقة في sech⁻¹ و csch⁻¹ و ln، فتصح على جهة واحدة من المجال.',
                'خطأ مطبعي في المذكرة ص65 (سطر في مثال x sec⁻¹x) لا يغير الجواب.'])
    return section('appendix', 'ملحق: المصادر والتحقق', table(['البند', 'القيمة'], rows, 'answers') + notes
                   + p('السجل الكامل وملفات التحقق مرفقة مع حزمة المصادر، وليست للمذاكرة.', 'small'))


def main():
    entries = [(1, 'howto', 'كيف تستخدم الكرّاسة'), (1, 'basics', 'أساسيات مصغرة'),
               (1, 'g42', '4.2 الدوال الزائدية العكسية')] + [(2, 'S%d' % i, '%d. %s' % (i, B.NAMES[i - 1])) for i in range(1, 5)] + \
              [(1, 'g51', '5.1 التكامل بالتجزئة')] + [(2, 'S%d' % i, '%d. %s' % (i, B.NAMES[i - 1])) for i in range(5, 11)] + \
              [(1, 'g52', '5.2 التكاملات المثلثية')] + [(2, 'S%d' % i, '%d. %s' % (i, B.NAMES[i - 1])) for i in range(11, 15)] + \
              [(1, 'choose', 'اختر الاختصار'), (1, 'apply', 'طبّق'), (1, 'flash', 'بطاقات الاسترجاع'), (1, 'recall', 'اكتب من الذاكرة'),
               (1, 'help', 'سلّم المساعدة'), (1, 'appendix', 'ملحق: المصادر والتحقق')]
    body = cover() + toc(entries) + how_to_use() + foundations() + cards_part() + drills_part() + recall_part() + help_part() + appendix()
    tpl = (ROOT / 'src' / 'template.html').read_text(encoding='utf-8')
    html_out = tpl.replace('{{TITLE}}', 'كرّاسة الاختصارات').replace('{{BODY}}', body)
    (ROOT / 'src' / 'booklet.html').write_text(html_out, encoding='utf-8')
    log = write_log('booklet')
    usage = {k: dict(usage='مستخدم في كرّاسة الاختصارات', location='; '.join(sorted(set(v)))) for k, v in __import__('booklet_engine').USED.items()}
    (ROOT / 'data' / 'usage.json').write_text(json.dumps(usage, ensure_ascii=False, indent=1), encoding='utf-8')
    print('ok', log, len(usage), 'items used')


if __name__ == '__main__':
    main()

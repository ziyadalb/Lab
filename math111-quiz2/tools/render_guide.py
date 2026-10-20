#!/usr/bin/env python3
"""Assemble the full study guide (one PDF): 7 study days, one unit per question type, end sections.

Run: python3 tools/render_guide.py  ->  src/guide.html (math as data-tex placeholders)
Every formula, step and answer is checked while building; a failed check aborts (reports/guide_checks.json).
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
import booklet_engine as E  # noqa: E402
import guide_kit as K  # noqa: E402
from html_kit import box, chip, en, lines, link, md, mi, p, table, ul  # noqa: E402
import guide_42  # noqa: E402

UNIT_MODULES = [guide_42]
for name in ('guide_51', 'guide_52'):
    UNIT_MODULES.append(__import__(name))
import guide_end as END  # noqa: E402
import guide_prereq as PQ  # noqa: E402
from bidi import isolate_runs  # noqa: E402

TODAY = datetime.date(2026, 10, 19)
DAYS = {1: ('الثلاثاء', 20), 2: ('الأربعاء', 21), 3: ('الخميس', 22), 4: ('الجمعة', 23), 5: ('السبت', 24),
        6: ('الأحد', 25), 7: ('الاثنين', 26)}
LESSON_OF_DAY = {1: 'أساسيات من الدروس السابقة + 4.2: المشتقات وأول التكاملات', 2: '4.2: باقي التكاملات وإكمال المربع',
                 3: 'آخر نوع في 4.2 + بداية 5.1: التكامل بالتجزئة', 4: '5.1: المحدد، والدوال العكسية، والدوران، والتعويض',
                 5: '5.2: sin و cos، و tan و sec', 6: '5.2: آخر الأنواع + الاختبار التجريبي A',
                 7: 'مراجعة مخلوطة + الاختبار التجريبي B'}

def section(id_, title, inner, cls=''):
    return '<section class="chapter %s" id="%s"><h2>%s</h2>%s</section>' % (cls, id_, title, inner)


def cover():
    return ('<section class="cover" id="top"><div class="kicker">ريض 111 · الكويز الثاني · الثلاثاء 27 أكتوبر 2026</div>'
            '<h1>مذكرة الكويز الثاني</h1>'
            '<div class="sub">4.2 الدوال الزائدية العكسية · 5.1 التكامل بالتجزئة · 5.2 التكاملات المثلثية</div>'
            + box('note', 'لمن هذه المذكرة', p('لزياد. كل نوع سؤال في الدروس الثلاثة مكتمل في مكانه: الاختصار والطريقة الأساسية على '
                                               'نفس المثال، والجبر مشروح خطوة خطوة، وبعدها تمارين متدرجة وحلولها الكاملة في الصفحة التالية.'))
            + box('note', 'هل الحلول صحيحة؟', p('كل جواب، وكل قانون، وكل مساواة في الخطوات، فحصها الحاسوب رياضيًا قبل الطباعة '
                                                '(العدد في الملحق). الأمثلة والتمارين من اختبارات المقرر السابقة ومن مذكرة د. طارق؛ '
                                                'والقليل المكتوب عليه «تدريب إضافي» كتبناه نحن لأنواع لها أسئلة قليلة.'))
            + box('warn', 'الاختباران التجريبيان', p('في ملف منفصل. أسئلتهما من اختبارات حقيقية حُجزت ولم تظهر في هذه المذكرة. '
                                                     'حل A في اليوم 6 و B في اليوم 7 كما في الخطة.'))
            + '<div class="meta">المصادر: مذكرة د. طارق الفضل (2024) واختبارات المقرر 1445–1447. تاريخ الإصدار: %s</div></section>'
            % TODAY.isoformat())


def toc():
    rows = ''

    def entry(anchor, text, lvl=2):
        return ('<li class="lvl%d"><a href="#%s"><span class="t">%s</span><span class="pg" data-target="%s"></span></a></li>'
                % (lvl, anchor, text, anchor))
    for d in sorted(DAYS):
        day, date = DAYS[d]
        rows += entry('day%d' % d, 'اليوم %d — %s %d أكتوبر: %s' % (d, day, date, LESSON_OF_DAY[d]), 1)
        for a in END.DAY_START.get(d, []):
            rows += entry(a, '⚡ ' + END.TITLES[a])
        for uid, num, title in K.DAYS.get(d, []):
            for a in END.BEFORE_UNIT.get(uid, []):
                rows += entry(a, END.TITLES[a] if a in PQ.TITLES else '⚡ ' + END.TITLES[a])
            rows += entry(uid, '%d. %s' % (num, title))
        for a in END.DAY_END.get(d, []):
            rows += entry(a, END.TITLES[a])
    for anchor, title in END.END_TOC:
        rows += entry(anchor, title, 1)
    return '<section class="toc" id="toc"><h2>المحتويات</h2><ol>%s</ol></section>' % rows


def how_to_use():
    order = ul(['<b>كل يوم</b> يبدأ بصفحة اليوم: الهدف، وجدول الوقت، والإحماء (تكتب فيه الاختصارات من ذاكرتك وتبدأ سؤالي مراجعة).',
                '<b>كل نوع سؤال</b> مكتمل في مكانه بنفس الترتيب دائمًا (الجدول تحت)، وتمارينه بعد شرحه مباشرة.',
                '<b>المثال</b> محلول مرتين: ⚡ بالاختصار خطوة خطوة، ثم 🧱 بالطريقة الأساسية، وجنب كل خطوة سببها '
                '(أنواع الحجز في 5.2: 🧱 فقط).',
                '<b>التمارين</b> متدرجة: موجّه (أول سطر جاهز)، ثم ناقص الخطوات، ثم لحالك. اكتب في المساحة تحت كل تمرين.',
                '<b>إذا علقت في تمرين</b>: افتح رابطًا واحدًا فوقه ثم ارجع حاول: 💡 تلميح ← ✍️ أول خطوة ← ✅ الحل الكامل '
                '(الأولان في ' + link('help', 'سلّم المساعدة') + ').',
                '<b>الجبر</b>: كل مهارة مشروحة أول مرة في صندوق 🧮 مع «جرّب»، وبعدها رابط لها.',
                '<b>أرقام الدروس</b>: 4.2 و5.1 و5.2 دروس الكويز. والأقدم (مثل 4.1 و3.4) دروس قبلها، مشروحة في صفحات '
                '«📚 ق1–ق5»، وفي رأس كل نوع رابط لها.',
                '<b>أخطاؤك</b>: سجّل كل غلطة في ' + link('errlog', 'سجل الأخطاء') + ' آخر المذكرة، وراجعه كل صباح.',
                '<b>في الكويز</b>: اكتب دائمًا سطور «في ورقة الكويز»، والاختصار لتتأكد من الجواب بسرعة.'])
    legend = table(['المربع', 'معناه'], [
        [chip('الفكرة والعلامة', 'k-idea'), 'ليش الطريقة تشتغل، وكيف تعرف النوع، ومع أي نوع يختلط.'],
        [chip('⚡ الاختصار', 'k-short'), 'القاعدة التي تعطي الجواب مباشرة، وشروطها.'],
        [chip('🧭 الطريقة', 'k-short'), 'في أنواع 5.2 بلا اختصار: خطوات ثابتة للطريقة العادية.'],
        [chip('📚 ق1…ق5', 'pq'), 'شرح من الدروس السابقة (مثل 4.1 و3.4) تحتاجه في هذا النوع.'],
        [chip('🧮 جبر', 'k-alg'), 'مهارة جبر مشروحة بالتفصيل، ومعها «جرّب».'],
        [chip('⚠️ الفخ', 'k-trap'), 'الغلطة التي يقع فيها الطلاب.'],
        [chip('✍️ في ورقة الكويز و ✔ تأكد', 'k-paper'), 'ما تكتبه حتى يرى المصحح خطواتك، وفحص سريع لجوابك.']], 'legend')
    gloss = table(['في ورقة الكويز', 'معناها'], [
        [en('Evaluate the following integrals'), 'احسب التكاملات التالية'],
        [en('Find dy/dx  /  Find the derivative'), 'أوجد المشتقة'],
        [mi(r'\sinh^{-1}x') + ' أو ' + en('arcsinh x'), 'معكوس sinh (وليس ' + mi(r'\frac{1}{\sinh x}') + ')'],
        [mi(r'\log x'), 'لوغاريتم بأساس 10؛ و ' + mi(r'\ln x') + ' الطبيعي']], 'glossary')
    return section('howto', 'كيف تستخدم المذكرة', order + legend + '<h3>كلمات الأسئلة الإنجليزية</h3>' + gloss)


def day_page(d):
    day, date = DAYS[d]
    units = K.DAYS.get(d, [])
    goal = ul(['☐ %d. %s' % (num, title) for _, num, title in units] + ['☐ ' + t for _, t in END.day_extras(d)], 'checks')
    rows, total = END.day_schedule(d)
    plan = table(['الوقت', 'وش تسوي'], rows, 'compact')
    warm = END.warmup(d) if d > 1 else box('memo', '🔁 الإحماء (5 دقائق)', p(
        'اكتب على ورقة، بدون ما تفتح المذكرة: مشتقة ' + mi(r'\sinh x') + ' و ' + mi(r'\cosh x') + ' و ' + mi(r'\tanh x')
        + '. هذي من درس 4.1، الدرس اللي قبل الكويز. بعدها افتح ' + link('pq1', '📚 ق1 ص ' + K.pgref('pq1'))
        + ' وقارن بجدول المشتقات. إذا ما تذكرت شيئًا، عادي: ق1 تشرحه من البداية.'))
    return ('<section class="chapter day-page" id="day%d"><h2>اليوم %d — %s %d أكتوبر</h2>' % (d, d, day, date)
            + box('short', '🎯 هدف اليوم: ' + LESSON_OF_DAY[d], goal)
            + box('note', '⏱️ الوقت: %s تقريبًا (عدّل الفواصل على راحتك)' % END.duration(total), plan) + warm + '</section>')


def main():
    ordered = []
    PQ.build(['pq1', 'pq2', 'pq3', 'pq4'])       # built in document order, before the types that link to them
    for mod in UNIT_MODULES:
        if mod.__name__ == 'guide_52':
            PQ.build(['pq5'])                      # its algebra box comes before type 22's link to it
        for fn in getattr(mod, [n for n in dir(mod) if n.startswith('UNITS_')][0]):
            ordered.append(fn())
    body = cover() + toc() + how_to_use()
    for d in sorted(DAYS):
        body += day_page(d) + END.day_start(d)
        for U in [u for u in ordered if u.day == d]:
            body += END.before_unit(U.uid) + U.html()
        body += END.after_day(d)
    body += END.end_sections()
    body = isolate_runs(body)
    tpl = (ROOT / 'src' / 'template.html').read_text(encoding='utf-8')
    html_out = tpl.replace('{{TITLE}}', 'مذكرة الكويز الثاني').replace('{{BODY}}', body)
    (ROOT / 'src' / 'guide.html').write_text(html_out, encoding='utf-8')
    log = E.write_log('guide')
    usage = {k: dict(usage='مستخدم في المذكرة الكاملة', location='; '.join(sorted(set(v)))) for k, v in E.USED.items()}
    (ROOT / 'data' / 'usage_guide.json').write_text(json.dumps(usage, ensure_ascii=False, indent=1), encoding='utf-8')
    print('ok', log, len(usage), 'items used,', sum(len(v) for v in K.DAYS.values()), 'units,', len(K.HELP), 'exercises')


if __name__ == '__main__':
    main()

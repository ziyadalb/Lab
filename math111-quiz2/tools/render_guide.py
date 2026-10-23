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

TODAY = datetime.date(2026, 10, 23)
DAYS = K.DAY_NAME                 # day number -> date label (days 1-2 done, 3-6 left, 7 = extras for spare time)
DONE_DAYS = (1, 2)
LESSON_OF_DAY = {1: 'قبل درس 4.2 + 4.2: المشتقات وأول تكامل', 2: '4.2: باقي التكاملات',
                 3: 'آخر نوع في 4.2 + قبل درس 5.1 + بداية 5.1', 4: '5.1: باقي الأنواع',
                 5: 'قبل درس 5.2 + 5.2: sin و cos', 6: '5.2: tan و sec + الاختبار التجريبي A + ليلة الكويز',
                 7: 'المراجعة المخلوطة والاختبار التجريبي B'}


def day_title(d):
    return '⭐ إضافي: إذا بقي وقت' if d == 7 else 'اليوم %d — %s' % (d, DAYS[d])

def section(id_, title, inner, cls=''):
    return '<section class="chapter %s" id="%s"><h2>%s</h2>%s</section>' % (cls, id_, title, inner)


def cover():
    return ('<section class="cover" id="top"><div class="kicker">ريض 111 · الكويز الثاني · الثلاثاء 27 أكتوبر 2026</div>'
            '<h1>مذكرة الكويز الثاني</h1>'
            '<div class="sub">4.2 الدوال الزائدية العكسية · 5.1 التكامل بالتجزئة · 5.2 التكاملات المثلثية</div>'
            + box('note', 'لمن هذه المذكرة', p('لزياد. كل نوع سؤال في الدروس الثلاثة مكتمل في مكانه: وش هذا النوع، ثم مثال محلول '
                                               'خطوة خطوة، والجبر مشروح، وبعدها تمارين متدرجة وحلولها الكاملة في الصفحة التالية.'))
            + box('note', 'هل الحلول صحيحة؟', p('كل جواب، وكل قانون، وكل مساواة في الخطوات، فحصها الحاسوب رياضيًا قبل الطباعة '
                                                '(العدد في الملحق). الأمثلة والتمارين من اختبارات المقرر السابقة ومن مذكرة د. طارق؛ '
                                                'والقليل المكتوب عليه «تدريب إضافي» كتبناه نحن لأنواع لها أسئلة قليلة.'))
            + box('warn', 'الاختباران التجريبيان', p('في ملف منفصل. أسئلتهما من اختبارات حقيقية حُجزت ولم تظهر في هذه المذكرة. '
                                                     'حل A يوم الاثنين 26 كما في الخطة، و B إذا بقي وقت.'))
            + '<div class="meta">المصادر: مذكرة د. طارق الفضل (2024) واختبارات المقرر 1445–1447. تاريخ الإصدار: %s</div></section>'
            % TODAY.isoformat())


def toc():
    rows = ''

    def entry(anchor, text, lvl=2):
        return ('<li class="lvl%d"><a href="#%s"><span class="t">%s</span><span class="pg" data-target="%s"></span></a></li>'
                % (lvl, anchor, text, anchor))
    for d in sorted(DAYS):
        rows += entry('day%d' % d, '%s: %s' % (day_title(d), LESSON_OF_DAY[d]), 1)
        for a in END.DAY_START.get(d, []):
            rows += entry(a, '🔎 ' + END.TITLES[a])
        for uid, num, title in K.DAYS.get(d, []):
            for a in END.BEFORE_UNIT.get(uid, []):
                if a not in PQ.TITLES:
                    rows += entry(a, '🔎 ' + END.TITLES[a])
                    continue
                rows += entry(a, END.TITLES[a])
                for puid, label, ptitle in PQ.PARTS[a]:
                    rows += entry(puid, '%s. %s' % (label, ptitle), 3)
            sec = MAP_BEFORE.get(uid)
            if sec:
                rows += entry('map-' + sec, '🗺️ خريطة درس %s' % sec)
            rows += entry(uid, '%d. %s' % (num, title))
        for a in END.DAY_END.get(d, []):
            rows += entry(a, END.TITLES[a])
    for anchor, title in END.END_TOC:
        rows += entry(anchor, title, 1)
    return '<section class="toc" id="toc"><h2>المحتويات</h2><ol>%s</ol></section>' % rows


def how_to_use():
    order = ul(['<b>كل يوم</b> يبدأ بصفحة اليوم: الهدف، وجدول الوقت، والإحماء.',
                '<b>كل نوع سؤال</b> بنفس الترتيب: 🎯 وش هذا النوع، ثم 📐 القانون أو 🧭 الطريقة، ثم 🧱 مثال محلول خطوة خطوة '
                '(وبعده ⚡ الطريقة السريعة، بس في الأنواع اللي توفر فيها وقت)، ثم ✔ قبل ما تسلّم، ثم 📌 الخلاصة، ثم التمارين.',
                '<b>جدول الحل</b> فيه عمودان: «الخطوة» هي اللي تكتبها في الكويز، و«ليش؟» لك أنت عشان تفهم.',
                '<b>التمارين</b> متدرجة: موجّه (أول سطر جاهز)، ثم ناقص الخطوات، ثم لحالك. حاول في المساحة، وبعدين اضغط «✅ الحل».',
                '<b>🗺️ خريطة الدرس</b> قبل أول نوع في الدرس: كل أنواعه، ووش تشوف في السؤال، وأول خطوة. ارجع لها كل ما احترت.',
                '<b>قبل كل درس</b> فصل «📚 قبل الدرس» فيه الأساسيات من الفصول السابقة، وفي رأس كل نوع رابط للجزء اللي يحتاجه.',
                '<b>أخطاؤك</b>: سجّل كل غلطة في ' + link('errlog', 'سجل الأخطاء') + ' آخر المذكرة، وراجعه كل صباح.'])
    legend = table(['المربع', 'معناه'], [
        [chip('🎯 وش هذا النوع', 'k-idea'), 'الفكرة، وكيف تعرف النوع من شكله، والفرق عن النوع اللي قبله.'],
        [chip('📐 القانون · 🧭 الطريقة', 'k-short'), 'القانون اللي تحتاجه، أو خطوات ثابتة تمشي عليها.'],
        [chip('⚡ الطريقة السريعة', 'k-short'), 'نفس الخطوات مختصرة. موجودة بس لما توفر وقت، وتستعملها لتتأكد من جوابك.'],
        [chip('🧮 جبر', 'k-alg'), 'مهارة جبر مشروحة بالتفصيل، ومعها «جرّب».'],
        [chip('✔ قبل ما تسلّم', 'k-paper'), 'الغلطة المشهورة، ووش تكتب في الورقة، وفحص سريع لجوابك.'],
        [chip('📌 الخلاصة', 'k-gist'), 'النوع في سطر: وش تشوف، وأول خطوة، وبعدها وش تسوي.']], 'legend')
    gloss = table(['في ورقة الكويز', 'معناها'], [
        [en('Evaluate the following integrals'), 'احسب التكاملات التالية'],
        [en('Find dy/dx  /  Find the derivative'), 'أوجد المشتقة'],
        [mi(r'\sinh^{-1}x') + ' أو ' + en('arcsinh x'), 'معكوس sinh (وليس ' + mi(r'\frac{1}{\sinh x}') + ')'],
        [mi(r'\log x'), 'لوغاريتم بأساس 10؛ و ' + mi(r'\ln x') + ' الطبيعي']], 'glossary')
    return section('howto', 'كيف تستخدم المذكرة', order + legend + '<h3>كلمات الأسئلة الإنجليزية</h3>' + gloss)


# the lesson map goes just before the first type of its lesson
MAP_BEFORE = {'U-D1': '4.2', 'U-P1': '5.1'}


def lesson_map(sec):
    rows = [[link(uid, "%d. %s" % (num, title)), K.rich(see), K.rich(first), K.pgref(uid)]
            for uid, (num, title, see, first, rule) in sorted(K.GIST.items(), key=lambda kv: kv[1][0])
            if K.LESSON_OF_UID.get(uid) == sec]
    intro = p('هذي كل أنواع الدرس في صفحة. شوف شكل السؤال، واعرف نوعه وأول خطوة فيه، ثم روح لصفحته. '
              'ارجع لهذي الصفحة كل ما احترت، وراجعها ليلة الكويز.')
    return ('<section class="chapter lesson-map %s" id="map-%s"><h2>🗺️ خريطة درس %s: اعرف النوع من شكله</h2>%s%s</section>'
            % (K.LESSON_CLS[sec], sec, sec, intro, table(['النوع', 'إذا شفت', 'أول خطوة', 'ص'], rows, 'map')))


def day_page(d):
    units = K.DAYS.get(d, [])
    goal = ul(['☐ %d. %s' % (num, title) for _, num, title in units] + ['☐ ' + t for _, t in END.day_extras(d)], 'checks')
    head = '<section class="chapter day-page" id="day%d"><h2>%s</h2>' % (d, day_title(d))
    if d in DONE_DAYS:
        return (head + box('short', '🎯 هدف اليوم: ' + LESSON_OF_DAY[d], goal)
                + box('note', '✓ خلصت هذا اليوم', p('هذا اليوم خلصته. أنواعه تبقى هنا للرجوع لها، ومراجعتها يوم الاثنين 26.'))
                + '</section>')
    if d == 7:
        return (head + box('note', 'ما يدخل في الخطة', p('هذي إضافات لو خلصت يومك وبقي عندك وقت ونشاط: صفحة «اعرف النوع 5.2»، '
                                                          'والمراجعة المخلوطة، والاختبار التجريبي B. ما عليك منها إذا ما بقي وقت.'))
                + box('short', 'الإضافات', goal) + '</section>')
    rows, total = END.day_schedule(d)
    plan = table(['الوقت', 'وش تسوي'], rows, 'compact')
    note = ''
    if d == 3:
        note = box('warn', 'الخطة الجديدة', p('باقي 4 أيام: الجمعة 23، والسبت 24، والأحد 25، والاثنين 26. والكويز الثلاثاء 27. '
                                              'كل يوم قرابة 3 ساعات ونص. إذا بدأت اليوم بالنسخة القديمة، كمّل من وين وصلت: أرقام الأنواع ما تغيرت.'))
    tired = ''
    if total > 180:
        tired = p('اليوم أطول من 3 ساعات. إذا تعبت، خلّ تمرين «لحالك» في آخر نوعين وحلّه يوم الاثنين 26.' if d < 6 else
                  'إذا تعبت، أهم شي اليوم الاختبار التجريبي A وصفحة «يوم الكويز»، ونوم بدري.', 'small')
    return (head + box('short', '🎯 هدف اليوم: ' + LESSON_OF_DAY[d], goal) + note
            + box('note', '⏱️ الوقت: %s تقريبًا (عدّل الفواصل على راحتك)' % END.duration(total), plan + tired)
            + END.warmup(d) + '</section>')


def main():
    ordered = []
    PQ.build(['pre42'])                            # built in document order: each chapter before its lesson's types
    for mod in UNIT_MODULES:
        if mod.__name__ == 'guide_51':
            PQ.build(['pre51'])
        if mod.__name__ == 'guide_52':
            PQ.build(['pre52'])                    # its algebra box comes before type 22's link to it
        for fn in getattr(mod, [n for n in dir(mod) if n.startswith('UNITS_')][0]):
            ordered.append(fn())
    body = cover() + toc() + how_to_use()
    for d in sorted(DAYS):
        body += day_page(d) + END.day_start(d)
        for U in [u for u in ordered if u.day == d]:
            body += END.before_unit(U.uid)
            if U.uid in MAP_BEFORE:
                body += lesson_map(MAP_BEFORE[U.uid])
            body += U.html()
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

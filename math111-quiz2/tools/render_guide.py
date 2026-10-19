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
    try:
        UNIT_MODULES.append(__import__(name))
    except ModuleNotFoundError:
        pass
import guide_end as END  # noqa: E402

TODAY = datetime.date(2026, 10, 19)
DAYS = {1: ('الثلاثاء', 20), 2: ('الأربعاء', 21), 3: ('الخميس', 22), 4: ('الجمعة', 23), 5: ('السبت', 24),
        6: ('الأحد', 25), 7: ('الاثنين', 26)}
LESSON_OF_DAY = {1: '4.2 المشتقات + أول التكاملات', 2: '4.2 التكاملات', 3: '4.2 إكمال المربع + بداية 5.1',
                 4: '5.1 التكامل بالتجزئة', 5: '5.1 (تكملة) + بداية 5.2', 6: '5.2 + الاختبار التجريبي A',
                 7: 'مراجعة مخلوطة + الاختبار التجريبي B'}


def section(id_, title, inner, cls=''):
    return '<section class="chapter %s" id="%s"><h2>%s</h2>%s</section>' % (cls, id_, title, inner)


def cover():
    return ('<section class="cover" id="top"><div class="kicker">ريض 111 · الكويز الثاني · الثلاثاء 27 أكتوبر 2026</div>'
            '<h1>مذكرة الكويز الثاني</h1>'
            '<div class="sub">4.2 الدوال الزائدية العكسية · 5.1 التكامل بالتجزئة · 5.2 التكاملات المثلثية</div>'
            + box('note', 'لمن هذه المذكرة', p('لزياد. كل نوع سؤال في الدروس الثلاثة له صفحتان: الاختصار والطريقة الأساسية على نفس '
                                               'المثال، والجبر مشروح خطوة خطوة، وبعدها تمارين وحلولها في الصفحة التالية.'))
            + box('note', 'هل الحلول صحيحة؟', p('كل جواب وكل خطوة في هذه المذكرة تحقق منها الحاسوب رياضيًا قبل الطباعة. '
                                                'الأمثلة والتمارين من اختبارات المقرر السابقة ومن مذكرة د. طارق؛ والقليل المكتوب عليه '
                                                '"تدريب إضافي" كتبناه نحن لأنواع لها أسئلة قليلة.'))
            + box('warn', 'الاختباران التجريبيان', p('في ملف منفصل. أسئلتهما من اختبارات حقيقية حُجزت ولم تظهر في هذه المذكرة. '
                                                     'حلّهما في اليومين 6 و7 كما في الخطة.'))
            + '<div class="meta">المصادر: مذكرة د. طارق الفضل (2024) واختبارات المقرر 1445–1447. تاريخ الإصدار: %s</div></section>'
            % TODAY.isoformat())


def toc():
    rows = ''
    for d in sorted(K.DAYS):
        day, date = DAYS[d]
        rows += ('<li class="lvl1"><a href="#day%d"><span class="t">اليوم %d — %s %d أكتوبر: %s</span>'
                 '<span class="pg" data-target="day%d"></span></a></li>' % (d, d, day, date, LESSON_OF_DAY[d], d))
        speed_after = {'U-I9': 'speed42', 'U-P10': 'speed51', 'U-T8': 'speed52'}
        extras = dict(END.EXTRA_TOC.get(d, []))
        for uid, num, title in K.DAYS[d]:
            rows += ('<li class="lvl2"><a href="#%s"><span class="t">%d. %s</span><span class="pg" data-target="%s"></span></a></li>'
                     % (uid, num, title, uid))
            if uid in speed_after and speed_after[uid] in extras:
                a = speed_after[uid]
                rows += ('<li class="lvl2"><a href="#%s"><span class="t">%s</span><span class="pg" data-target="%s"></span></a></li>'
                         % (a, extras[a], a))
        for anchor, title in END.EXTRA_TOC.get(d, []):
            if anchor.startswith('speed'):
                continue
            rows += ('<li class="lvl2"><a href="#%s"><span class="t">%s</span><span class="pg" data-target="%s"></span></a></li>'
                     % (anchor, title, anchor))
    for anchor, title in END.END_TOC:
        rows += ('<li class="lvl1"><a href="#%s"><span class="t">%s</span><span class="pg" data-target="%s"></span></a></li>'
                 % (anchor, title, anchor))
    return '<section class="toc" id="toc"><h2>المحتويات</h2><ol>%s</ol></section>' % rows


def how_to_use():
    order = ul(['<b>كل يوم</b> يبدأ بصفحة "ابدأ هنا": هدف اليوم، والوقت، و 5 دقائق تكتب فيها الاختصارات من ذاكرتك.',
                '<b>كل نوع سؤال</b> مكتمل في مكانه بنفس الترتيب دائمًا (الجدول تحت).',
                '<b>التلميح</b> تحت كل تمرين مقلوب عمدًا: اقلب الورقة أو الشاشة إذا احتجته فقط.',
                '<b>الحلول</b> في الصفحة التي بعد التمارين مباشرة. حاول أولًا، ثم قارن سطرًا سطرًا.',
                '<b>الجبر</b>: أول مرة تحتاج مهارة تجدها مشروحة بالتفصيل في صندوق 🧮، وبعدها رابط يرجعك لها.',
                '<b>أخطاؤك</b>: سجّل كل غلطة في ' + link('errlog', 'سجل الأخطاء') + ' آخر المذكرة، وراجعه في اليوم 7.'])
    legend = table(['المربع', 'معناه'], [
        [chip('الفكرة', 'k-idea'), 'ليش الطريقة تشتغل، في سطرين.'],
        [chip('العلامة', 'k-sign'), 'كيف تعرف النوع، ومع أي نوع يختلط.'],
        [chip('تذكير', 'k-note'), 'معلومة قديمة تحتاجها هنا.'],
        [chip('⚡ الاختصار', 'k-short'), 'القاعدة التي تعطي الجواب مباشرة.'],
        [chip('مثال', 'k-ex'), 'سؤال حقيقي محلول بالاختصار، ثم 🧱 خطوة خطوة وجنب كل خطوة سببها.'],
        [chip('🧮 جبر', 'k-alg'), 'مهارة جبر مشروحة بالتفصيل.'],
        [chip('✔ تأكد', 'k-ok'), 'فحص سريع لجوابك.'],
        [chip('⚠️ الفخ', 'k-trap'), 'الغلطة التي يقع فيها الطلاب.'],
        [chip('✍️ في ورقة الكويز', 'k-paper'), 'ما تكتبه حتى يرى المصحح خطواتك.']], 'legend')
    note = box('warn', 'عن الكتابة في الكويز', p('لا نعرف هل يقبل المصحح الجواب وحده، لذلك اكتب دائمًا السطرين أو الثلاثة '
                                                  'الموجودة في صندوق "في ورقة الكويز"، واستخدم الاختصار لتعرف الجواب بسرعة وتتأكد منه.'))
    return section('howto', 'كيف تستخدم المذكرة', order + legend + note)


def day_page(d):
    day, date = DAYS[d]
    units = K.DAYS.get(d, [])
    goal = ul(['%d. %s' % (num, title) for _, num, title in units] + [t for _, t in END.EXTRA_TOC.get(d, [])])
    plan = table(['الوقت', 'وش تسوي'], END.day_schedule(d, len(units)), 'compact')
    warm = END.warmup(d)
    return ('<section class="chapter day-page" id="day%d"><h2>اليوم %d — %s %d أكتوبر</h2>' % (d, d, day, date)
            + box('short', '🎯 هدف اليوم: ' + LESSON_OF_DAY[d], goal)
            + box('note', '⏱️ الوقت (حوالي ساعتين ونصف)', plan) + warm + '</section>')


def main():
    ordered = []
    for mod in UNIT_MODULES:
        for fn in getattr(mod, [n for n in dir(mod) if n.startswith('UNITS_')][0]):
            ordered.append(fn())
    last_of_lesson = {U.uid for U, nxt in zip(ordered, ordered[1:] + [None]) if nxt is None or nxt.section != U.section}
    body = cover() + toc() + how_to_use()
    for d in sorted(DAYS):
        body += day_page(d)
        for U in [u for u in ordered if u.day == d]:
            body += U.html()
            if U.uid in last_of_lesson:
                body += END.after_lesson(U.section)
        body += END.after_day(d)
    body += END.end_sections()
    tpl = (ROOT / 'src' / 'template.html').read_text(encoding='utf-8')
    html_out = tpl.replace('{{TITLE}}', 'مذكرة الكويز الثاني').replace('{{BODY}}', body)
    (ROOT / 'src' / 'guide.html').write_text(html_out, encoding='utf-8')
    log = E.write_log('guide')
    usage = {k: dict(usage='مستخدم في المذكرة الكاملة', location='; '.join(sorted(set(v)))) for k, v in E.USED.items()}
    (ROOT / 'data' / 'usage_guide.json').write_text(json.dumps(usage, ensure_ascii=False, indent=1), encoding='utf-8')
    print('ok', log, len(usage), 'items used,', sum(len(v) for v in K.DAYS.values()), 'units')


if __name__ == '__main__':
    main()

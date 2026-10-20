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
from bidi import isolate_runs  # noqa: E402

TODAY = datetime.date(2026, 10, 19)
DAYS = {1: ('الثلاثاء', 20), 2: ('الأربعاء', 21), 3: ('الخميس', 22), 4: ('الجمعة', 23), 5: ('السبت', 24),
        6: ('الأحد', 25), 7: ('الاثنين', 26)}
LESSON_OF_DAY = {1: '4.2: المشتقات وأول التكاملات', 2: '4.2: باقي التكاملات وإكمال المربع',
                 3: '5.1: بداية التكامل بالتجزئة', 4: '5.1: الدوال العكسية والدوران والتعويض',
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
            rows += entry(uid, '%d. %s' % (num, title))
        for a in END.DAY_END.get(d, []):
            rows += entry(a, END.TITLES[a])
    for anchor, title in END.END_TOC:
        rows += entry(anchor, title, 1)
    return '<section class="toc" id="toc"><h2>المحتويات</h2><ol>%s</ol></section>' % rows


def how_to_use():
    order = ul(['<b>كل يوم</b> يبدأ بصفحة اليوم: الهدف، وجدول الوقت، والإحماء (تكتب فيه الاختصارات من ذاكرتك وتبدأ سؤالي مراجعة).',
                '<b>كل نوع سؤال</b> مكتمل في مكانه بنفس الترتيب دائمًا (الجدول تحت)، وتمارينه بعد شرحه مباشرة.',
                '<b>المثال</b> محلول مرتين: ⚡ بالاختصار في خطوات قصيرة مرقمة، ثم 🧱 بالطريقة الأساسية خطوة خطوة وجنب كل خطوة سببها.',
                '<b>التمارين</b> متدرجة: موجّه (أول سطر جاهز)، ثم ناقص الخطوات، ثم لحالك. اكتب في المساحة تحت كل تمرين.',
                '<b>إذا علقت في تمرين</b>: فوقه ثلاثة روابط بالترتيب، وافتح واحدًا فقط ثم ارجع حاول: '
                '💡 تلميح ← ✍️ أول خطوة ← ✅ الحل الكامل. التلميح وأول خطوة في ' + link('help', 'سلّم المساعدة') + ' آخر المذكرة، '
                'والحل الكامل في الصفحة اللي بعد التمارين.',
                '<b>الجبر</b>: أول مرة تحتاج مهارة تجدها مشروحة بالتفصيل في صندوق 🧮 ومعها سؤال «جرّب»، وبعدها رابط يرجعك لها.',
                '<b>أخطاؤك</b>: سجّل كل غلطة في ' + link('errlog', 'سجل الأخطاء') + ' آخر المذكرة، وراجعه كل صباح.',
                '<b>في الكويز</b>: لا نعرف هل يقبل المصحح الجواب وحده، فاكتب دائمًا سطور «في ورقة الكويز»، '
                'واستخدم الاختصار لتعرف الجواب بسرعة وتتأكد منه.'])
    legend = table(['المربع', 'معناه'], [
        [chip('الفكرة والعلامة', 'k-idea'), 'ليش الطريقة تشتغل، وكيف تعرف النوع، ومع أي نوع يختلط.'],
        [chip('تذكير', 'k-note'), 'معلومة قديمة تحتاجها هنا.'],
        [chip('⚡ الاختصار', 'k-short'), 'القاعدة التي تعطي الجواب مباشرة، وشروطها.'],
        [chip('مثال', 'k-ex'), 'سؤال حقيقي: ⚡ بالاختصار، ثم 🧱 خطوة خطوة.'],
        [chip('🧮 جبر', 'k-alg'), 'مهارة جبر مشروحة بالتفصيل، ومعها «جرّب».'],
        [chip('⚠️ الفخ', 'k-trap'), 'الغلطة التي يقع فيها الطلاب.'],
        [chip('✍️ في ورقة الكويز و ✔ تأكد', 'k-paper'), 'ما تكتبه حتى يرى المصحح خطواتك، وفحص سريع لجوابك.']], 'legend')
    gloss = table(['في ورقة الكويز', 'معناها'], [
        [en('Evaluate the following integrals'), 'احسب التكاملات التالية'],
        [en('Find dy/dx  /  Find the derivative'), 'أوجد المشتقة'],
        [en('the following'), 'التالية (الأسئلة تحت)'],
        [mi(r'\sinh^{-1}x') + ' أو ' + en('arcsinh x'), 'معكوس sinh (وليس ' + mi(r'\frac{1}{\sinh x}') + ')'],
        [mi(r'\log x'), 'لوغاريتم بأساس 10؛ و ' + mi(r'\ln x') + ' الطبيعي']], 'glossary')
    return section('howto', 'كيف تستخدم المذكرة', order + legend + '<h3>كلمات الأسئلة الإنجليزية</h3>' + gloss)


def day_page(d):
    day, date = DAYS[d]
    units = K.DAYS.get(d, [])
    goal = ul(['%d. %s' % (num, title) for _, num, title in units] + [t for _, t in END.day_extras(d)])
    rows, total = END.day_schedule(d)
    plan = table(['الوقت', 'وش تسوي'], rows, 'compact')
    warm = END.warmup(d) if d > 1 else box('memo', '🔁 الإحماء (5 دقائق)', p(
        'قبل ما تبدأ: اكتب من ذاكرتك مشتقات sinh و cosh و tanh من درس 4.1، ثم قارنها بصندوق «تذكير» في النوع 1.'))
    return ('<section class="chapter day-page" id="day%d"><h2>اليوم %d — %s %d أكتوبر</h2>' % (d, d, day, date)
            + box('short', '🎯 هدف اليوم: ' + LESSON_OF_DAY[d], goal)
            + box('note', '⏱️ الوقت: %s تقريبًا (عدّل الفواصل على راحتك)' % END.duration(total), plan) + warm + '</section>')


def main():
    ordered = []
    for mod in UNIT_MODULES:
        for fn in getattr(mod, [n for n in dir(mod) if n.startswith('UNITS_')][0]):
            ordered.append(fn())
    body = cover() + toc() + how_to_use()
    for d in sorted(DAYS):
        body += day_page(d) + END.day_start(d)
        for U in [u for u in ordered if u.day == d]:
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

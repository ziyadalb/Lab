#!/usr/bin/env python3
"""The mock exams file: neutral instructions, mock A, mock B, then (each behind its own stop page) the worked
solutions with sources, and at the end the blueprint of the two mocks.

Run: python3 tools/render_mocks.py  ->  src/mocks.html (math as data-tex placeholders)
The ten questions are the held-out ones; every solution row and answer is checked like the guide.
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'content'))

import booklet_engine as E  # noqa: E402
from booklet import final as _final, prompt, source_label  # noqa: E402
from guide_kit import answer_box, rich, step_cells, steps_table  # noqa: E402
from html_kit import box, en, lines, md, p, table, ul  # noqa: E402
from mock_sols import MINUTES, MOCKS, SOLS, TYPE_OF, TYPES  # noqa: E402
from bidi import isolate_runs  # noqa: E402

HOLD = E.HOLD['held_items']
# v7: the guide numbers cases by method; old type numbers (mock_sols.TYPE_OF) are mapped to the new case numbers
_CASES = json.loads((ROOT / 'data' / 'case_numbers.json').read_text(encoding='utf-8'))
NEW_NUM = {c['old']: (c['num'], c['title']) for c in _CASES.values() if c.get('old')}


def case_ref(old):
    num, title = NEW_NUM[old]
    return 'الحالة %d (%s)' % (num, title)


def order(which):
    """The derivative stays first, as in the quiz; the four integrals are shuffled once (fixed seed)."""
    ids = list(MOCKS[which])
    rest = ids[1:]
    random.Random(27 if which == 'A' else 26).shuffle(rest)
    return [ids[0]] + rest


def chapter(id_, title, inner, cls=''):
    return '<section class="chapter %s" id="%s"><h2>%s</h2>%s</section>' % (cls, id_, title, inner)


def instructions():
    return ('<section class="cover" id="top"><div class="kicker">ريض 111 · الكويز الثاني · الثلاثاء 27 أكتوبر 2026</div>'
            '<h1>الاختباران التجريبيان</h1><div class="sub">اختبار A واختبار B، كل واحد 5 أسئلة و 60 دقيقة</div>'
            + box('note', 'التعليمات', ul([
                'اضبط منبهًا على 60 دقيقة لكل اختبار.',
                'بدون مذكرة، وبدون ورقة قوانين، وبدون آلة حاسبة، مثل الكويز.',
                'اكتب خطواتك كاملة كما تكتبها في الكويز؛ الجواب وحده قد لا يكفي.',]))
            + box('short', 'متى أحل؟', ul([
                '<b>الاختبار A</b> يوم الاثنين 26 أكتوبر بعد ما تخلص الطرق الأربع، ثم صحّح A فقط من صفحة حلوله.',
                '<b>الاختبار B</b> إذا بقي وقت (الاثنين بالليل، أو قبلها لو خلصت بدري)، ثم صحّح B.',
                'حلول كل اختبار بعد صفحة «قف» خاصة به. لا تفتح حلول B قبل ما تحل B.']))
            + box('warn', 'عن الأسئلة', ul([
                'الأسئلة العشرة حقيقية: 7 من اختبارات المقرر السابقة (1445–1447)، وواحد من تمارين مذكرة د. طارق، '
                'واثنين من مذكرة د. موسى (بدل سؤالين كانوا قريبين جدًا من أمثلة محاضرات دكتورك). كلها محجوزة وما تظهر في المذكرة.',
                'لكن ما نقدر نضمن إنك ما شفتها قبل (مثلًا لو حليت الاختبارات السابقة). إذا عرفت سؤالًا، اكتب «شفته قبل» جنبه.',
                'كل سؤال هنا جزء واحد من سؤال أصلي في الاختبار.']))
            + '</section>')


def exam(which):
    qs = ''
    for k, item_id in enumerate(order(which), 1):
        it = E.use(item_id, 'mock %s' % which, allow_held=True)
        n = 9 if it['task'] == 'diff' else 12
        qs += ('<div class="mq"><div class="mq-head">السؤال %d</div>' % k + en(prompt(it)) + md(E.q_tex(it))
               + lines(n, 'write tight') + '</div>')
    return chapter('mock' + which, 'الاختبار التجريبي ' + which, p('60 دقيقة · 5 أسئلة · ابدأ المنبه الآن.', 'small') + qs, 'exam')


def stop(which):
    other = 'B' if which == 'A' else None
    text = p('الصفحات التالية فيها <b>حلول الاختبار %s</b>. افتحها بعد ما تخلص الاختبار %s كاملًا.' % (which, which))
    if other:
        text += p('بعد حلول A تجي صفحة «قف» ثانية، وبعدها حلول B: لا تتجاوزها قبل ما تحل B.')
    return chapter('stop' + which, '🛑 قف', box('warn', 'قبل ما تقلب الصفحة', text), 'stop')


def solutions(which):
    out = p('صحّح سؤالًا سؤالًا. إذا اختلف جوابك: اشتقه (للتكاملات)؛ إذا رجع السؤال فهو صحيح (قد يختلف بثابت). '
            'وكل غلطة سجّلها في سجل الأخطاء آخر المذكرة.', 'small')
    for k, item_id in enumerate(order(which), 1):
        it = E.ITEMS[item_id]
        cells = step_cells(it, SOLS[item_id], 'mock %s q%d' % (which, k))
        answer = answer_box(it, 'mock %s q%d' % (which, k))
        body = md(E.q_tex(it)) + steps_table(cells) + ('' if cells[-1][2] else answer)
        types = '، '.join(case_ref(t) for t in TYPE_OF[item_id])
        extra = ' والمشتقات من 4.1' if item_id in ('1447-S1-SE-Q1.1', '1446-S1-SE-Q1.1') else ''
        body += p('<b>المصدر:</b> %s · معرّف الحجز %s' % (source_label(it), HOLD[item_id]), 'small')
        body += p('<b>إذا غلطت:</b> ارجع في المذكرة إلى %s%s، واقرأ ⚡ و🧱، وحل تمرينه الأخير.' % (types, extra), 'small')
        out += '<div class="sol"><div class="drill-head"><b>السؤال %d</b></div>%s</div>' % (k, body)
    return chapter('sol' + which, 'حلول الاختبار التجريبي ' + which, out)


def blueprint():
    rows = []
    for which in ('A', 'B'):
        for k, item_id in enumerate(order(which), 1):
            it = E.ITEMS[item_id]
            rows.append(['%s%d' % (which, k), it['section'], '، '.join('الحالة %d' % NEW_NUM[t][0] for t in TYPE_OF[item_id]),
                         'مشتقة' if it['task'] == 'diff' else 'تكامل', HOLD[item_id]])
    score = table(['الاختبار', 'صحيح كامل', 'بداية صحيحة فقط', 'خطأ أو فاضي'], [['A', '', '', ''], ['B', '', '', '']], 'errlog')
    return chapter('plan', 'مخطط الاختبارين ونتيجتك',
                   p('هذا اختيار تعليمي يوازن الدروس الثلاثة (مشتقة من 4.2 أولًا، ثم تكاملات من 4.2 و 5.1 و 5.2)، '
                     'وليس توزيعًا رسميًا للكويز؛ لا نعرف توزيعه الرسمي.')
                   + table(['السؤال', 'الدرس', 'الحالة في المذكرة', 'المطلوب', 'معرّف الحجز'], rows, 'answers')
                   + '<h3>سجّل نتيجتك (عدد الأسئلة)</h3>' + score
                   + p(rich('«بداية صحيحة» يعني أول سطر صحيح (مثل $u$ و $du$، أو $u$ و $dv$) ثم تعطلت. هذه تعني أن المشكلة في التنفيذ أو الجبر، '
                            'لا في اختيار الطريقة.'), 'small'))


def main():
    body = (instructions() + exam('A') + exam('B') + stop('A') + solutions('A') + stop('B') + solutions('B') + blueprint())
    body = isolate_runs(body)
    tpl = (ROOT / 'src' / 'template.html').read_text(encoding='utf-8')
    (ROOT / 'src' / 'mocks.html').write_text(tpl.replace('{{TITLE}}', 'الاختباران التجريبيان').replace('{{BODY}}', body), encoding='utf-8')
    held = sorted(i for i in E.USED if i in HOLD)
    assert len(held) == 10 and len(E.USED) == 10, E.USED      # exactly the ten held questions, nothing else
    log = E.write_log('mocks')
    print('ok', log, len(held), 'held questions')


if __name__ == '__main__':
    main()

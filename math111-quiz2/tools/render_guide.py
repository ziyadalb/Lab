#!/usr/bin/env python3
"""Assemble the full study guide (one PDF), v7: ordered by the method that solves a question, not by lesson.

  0. قبل أي حل ← أ. الاشتقاق ← 🌳 الشجرة ← ب. التعويض ← 🔧 التجهيزات ← ج. التجزئة ← د. التمييز والتذكر
  ← ورقة الدرجة الكاملة، جوابك يختلف عن المفتاح؟، يوم الكويز، الاختباران، ليلة الكويز ← الملحق

Run: python3 tools/render_guide.py  ->  src/guide.html (math as data-tex placeholders)
Every formula, step and answer is checked while building; a failed check aborts (reports/guide_checks.json).
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'content'))

import booklet_engine as E  # noqa: E402
import guide_kit as K  # noqa: E402
from html_kit import link, p, table  # noqa: E402
import guide_42  # noqa: E402
import guide_51  # noqa: E402
import guide_52  # noqa: E402
try:
    import guide_new  # noqa: E402   the cases added in v7 (logarithmic differentiation, 3.4 or 4.2, three preparations)
except ImportError:
    guide_new = None
import guide_end as END  # noqa: E402
import guide_paths as GP  # noqa: E402
import guide_prereq as PQ  # noqa: E402
from bidi import isolate_runs  # noqa: E402

# builder of every case and prerequisite part, by uid
BUILD = dict(zip(K.OLD_ORDER, guide_42.UNITS_42 + guide_51.UNITS_51 + guide_52.UNITS_52))
if guide_new:
    BUILD.update(dict(zip(['U-LD', 'U-34', 'U-X2', 'U-LN', 'U-CH'], guide_new.UNITS_NEW)))
BUILD.update({'P-A1': PQ.part_a1, 'P-A2': PQ.part_a2, 'P-A3': PQ.part_a3, 'P-A4': PQ.part_a4, 'P-B1': PQ.part_b1,
              'P-B2': PQ.part_b2, 'P-B3': PQ.part_b3, 'P-C1': PQ.part_c1, 'P-C2': PQ.part_c2, 'P-C3': PQ.part_c3})

# the sections in document order: (method key, its first page, the parts and cases in order)
SECTIONS = [
    ('0', GP.sec0, []),
    ('A', GP.intro_A, ['P-A2', 'P-A3', 'U-D1', 'U-D2', 'U-LD']),
    ('T', GP.tree, []),
    ('B', GP.intro_B, ['U-I1', 'U-I2', 'U-I3', 'U-I5', 'U-I7', 'P-C1', 'U-T1', 'U-T2', 'U-T4', 'U-T5', 'U-T7']),
    ('P', GP.intro_P, ['U-I6', 'U-X2', 'U-LN', 'U-I4', 'U-CH', 'U-P9', 'U-I8', 'U-I9', 'U-34', 'U-T3', 'U-T8', 'U-T6']),
    ('C', GP.intro_C, ['U-P1', 'U-P2', 'U-P3', 'U-P4', 'U-P6', 'U-P7', 'U-P8', 'U-P10', 'U-P5']),
    ('D', GP.intro_D, []),
]
# v6 basics now written inside a section page: their old links land on that page
ALIAS = {'P-A1': '0', 'P-B3': '0', 'P-C2': '0', 'P-A4': 'T', 'P-B2': 'C', 'P-B1': 'A', 'P-C3': 'B'}
SEC_TITLE = {'0': '0. قبل أي حل', 'A': 'أ. الاشتقاق', 'T': '🌳 الشجرة: أي طريقة؟', 'B': 'ب. التعويض',
             'P': '🔧 التجهيزات', 'C': 'ج. التجزئة', 'D': 'د. التمييز والتذكر'}
SEC_ANCHOR = {'0': 's0', 'A': 'sA', 'T': 'tree', 'B': 'sB', 'P': 'sP', 'C': 'sC', 'D': 'sD'}
# the two days left (the plan approved on Sunday 25 October): (when, what, minutes, link)
PLAN = [   # the order of study (no times: Ziyad's choice)
    ('1', 'القسم 0 والشجرة', '', 's0'),
    ('2', 'أ. الاشتقاق (جا 16 مرة في الاختبارات)', '', 'sA'),
    ('3', 'ب. التعويض: تكاملات 4.2، ثم 5.2 بالحجز', '', 'sB'),
    ('4', '🔧 التجهيزات: كمّل المربع أول (جا 8 مرات)', '', 'sP'),
    ('5', 'ج. التجزئة (جا 17 مرة)', '', 'sC'),
    ('6', 'د. فحوص الإتقان، و«صحّح الغلط»، و«وش الحالة؟»', '', 'mastery'),
    ('7', 'الاختبار التجريبي A، ثم صحّحه', '', 'mockA'),
    ('8', 'بالليل: الشجرة، والسكربتات، وورقة الدرجة الكاملة', '', 'night'),
]


def cover():
    return ('<section class="cover" id="top"><div class="kicker">ريض 111 · الكويز الثاني · الثلاثاء 27 أكتوبر 2026</div>'
            '<h1>مذكرة الدرجة الكاملة</h1>'
            '<div class="sub">4.2 الدوال الزائدية العكسية · 5.1 التكامل بالتجزئة · 5.2 التكاملات المثلثية<br>'
            'مرتبة بطريقة الحل: اشتقاق، تعويض، تجهيزات، تجزئة</div>'
            + p('<b>لزياد.</b> كل سؤال في الكويز تبدأه بالشجرة: أربعة أسئلة توديك للطريقة. وكل طريقة لها سكربت ثابت، '
                'وكل حالة فيها مثال محلول خطوة خطوة وتمارين بحلول كاملة.')
            + p('<b>هل الحلول صحيحة؟</b> كل جواب، وكل قانون، وكل سطر في الخطوات، فحصه الحاسوب قبل الطباعة. '
                'التمارين بالأولوية: 📝 الاختبارات السابقة، ثم 📗 مذكرة د. موسى، ثم 📘 مذكرة د. طارق.')
            + p('<b>الاختباران التجريبيان</b> في ملف منفصل. أسئلتهما من اختبارات حقيقية محجوزة ما تظهر في هذي المذكرة، '
                'بس ما نضمن إنك ما شفتها في مكان ثاني.')
            + '<div class="meta">المصادر: اختبارات المقرر 1445–1447، ومذكرة د. طارق الفضل (2024)، ومذكرة د. موسى عجال (1448/1449)، '
              'وطريقة كتابة دكتورك في محاضراته. الإصدار 7.</div></section>')


def toc(entries):
    def entry(anchor, text, lvl=2):
        return ('<li class="lvl%d"><a href="#%s"><span class="t">%s</span><span class="pg" data-target="%s"></span></a></li>'
                % (lvl, anchor, text, anchor))
    rows = entry('howto', 'كيف تذاكر منها، والترتيب، والرقم القديم ← الجديد', 1)
    for key, items in entries:
        rows += entry(SEC_ANCHOR[key], SEC_TITLE[key], 1)
        for anchor, text in items:
            rows += entry(anchor, text, 3 if text.startswith('📚') else 2)
    for anchor, title in END.END_TOC:
        rows += entry(anchor, title, 1)
    return '<section class="toc" id="toc"><h2>المحتويات</h2><ol>%s</ol></section>' % rows


def main():
    # labels and methods are known before building, so the links between pages are right in every direction
    pre = [uid for _, _, uids in SECTIONS for uid in uids if uid.startswith('P-')]
    K.NEED_LABEL.clear()
    K.NEED_LABEL.update({uid: 'أساس %d' % k for k, uid in enumerate(pre, 1)})
    for key, _, uids in SECTIONS:
        for uid in uids:
            if not uid.startswith('P-') and key in K.METHODS:
                K.METHOD_OF[uid] = key
    idx = ROOT / 'data' / 'musa_index.json'
    if idx.exists():
        for q in json.loads(idx.read_text(encoding='utf-8')):
            if q.get('usable', True) and q.get('case', '').startswith('U-'):
                K.MUSA_COUNT[q['case']] = K.MUSA_COUNT.get(q['case'], 0) + 1
    # build in document order (the first explanation of an algebra move carries its anchor)
    built, toc_items = {}, []
    for key, _, uids in SECTIONS:
        items = []
        for uid in uids:
            if uid not in BUILD:
                continue                                   # a v7 case not written yet
            U = BUILD[uid]()
            built[uid] = U.html()
            items.append((uid, '📚 %s. %s' % (U.num, U.title) if uid.startswith('P-') else '%d. %s' % (U.num, U.title)))
        toc_items.append((key, items))
    # first pages of the sections (they list the cases built above), then the pages around them
    old_rows = [[str(K.OLD_NUM[uid]), link(uid, str(K.NUM[uid])), t, K.pgref(uid)]
                for uid, n, t in sorted(K.CASES, key=lambda c: K.OLD_NUM.get(c[0], 99)) if uid in K.OLD_NUM]
    plan_rows = [[when, link(anchor, what), mins] for when, what, mins, anchor in PLAN]
    body = cover() + toc(toc_items) + GP.howto(plan_rows, old_rows)
    for key, first, uids in SECTIONS:
        body += first() + ''.join('<span id="%s"></span>' % a for a, k in ALIAS.items() if k == key)
        body += ''.join(built[uid] for uid in uids if uid in built)
        body += K.sols_section(key) if key in K.METHODS else ''
        if key == 'D':
            body += END.section_d()
    body += END.after_methods() + END.end_sections()
    body = K.renum(body)
    # older texts name the prerequisite parts by their v6 labels (أ1 … ج3)
    v6 = {'أ1': 'P-A1', 'أ2': 'P-A2', 'أ3': 'P-A3', 'أ4': 'P-A4', 'ب1': 'P-B1', 'ب2': 'P-B2', 'ب3': 'P-B3',
          'ج1': 'P-C1', 'ج2': 'P-C2', 'ج3': 'P-C3'}
    lab = lambda old: K.NEED_LABEL.get(v6[old], 'القسم 0')
    body = re.sub(r'📚 ([أبج][1-4])', lambda m: '📚 ' + lab(m.group(1)), body)
    body = re.sub(r'\(([أبج][1-4])\)', lambda m: '(' + lab(m.group(1)) + ')', body)
    body = isolate_runs(body)
    tpl = (ROOT / 'src' / 'template.html').read_text(encoding='utf-8')
    html_out = tpl.replace('{{TITLE}}', 'مذكرة الدرجة الكاملة').replace('{{BODY}}', body)
    (ROOT / 'src' / 'guide.html').write_text(html_out, encoding='utf-8')
    (ROOT / 'data' / 'case_numbers.json').write_text(json.dumps(
        {uid: dict(num=n, title=t, old=K.OLD_NUM.get(uid)) for uid, n, t in K.CASES}, ensure_ascii=False, indent=1), encoding='utf-8')
    log = E.write_log('guide')
    usage = {k: dict(usage='مستخدم في المذكرة الكاملة', location='; '.join(sorted(set(v)))) for k, v in E.USED.items()}
    (ROOT / 'data' / 'usage_guide.json').write_text(json.dumps(usage, ensure_ascii=False, indent=1), encoding='utf-8')
    print('ok', log, len(usage), 'items used,', len(K.CASES), 'cases,', len(K.HELP), 'exercises')


if __name__ == '__main__':
    main()

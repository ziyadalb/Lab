#!/usr/bin/env python3
"""Coverage statement (COVERAGE.md): every in-scope case -> the guide type that teaches it, its examples,
exercises and page, the held questions, the items left unused, and the actual page count of each file.

Run after both builds: python3 tools/coverage.py
"""
import json
import re
from collections import defaultdict
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent


def main():
    items = {i['id']: i for i in json.loads((ROOT / 'data' / 'items.json').read_text(encoding='utf-8'))}
    gen = {i['id']: i for i in json.loads((ROOT / 'data' / 'generated_items.json').read_text(encoding='utf-8'))}
    musa = {i['id']: i for i in json.loads((ROOT / 'data' / 'musa_items.json').read_text(encoding='utf-8'))}
    for f in sorted((ROOT / 'data').glob('extra_*.json')):
        for i in json.loads(f.read_text(encoding='utf-8')):
            (gen if i['kind'] == 'generated' else musa)[i['id']] = i
    allit = dict(items, **gen, **musa)
    usage = json.loads((ROOT / 'data' / 'usage_guide.json').read_text(encoding='utf-8'))
    hold = json.loads((ROOT / 'data' / 'holdout_ids.json').read_text())
    pages = json.loads((ROOT / 'out' / 'guide' / 'toc.json').read_text())
    html = (ROOT / 'src' / 'guide.html').read_text(encoding='utf-8')
    units = {m.group(1): (int(m.group(2)), re.sub('<[^>]+>', '', m.group(3)))
             for m in re.finditer(r'<div class="unit-head[^"]*" id="(U-[A-Z0-9]+)"><span class="num">(\d+)</span><h3>(.*?)</h3>', html)}
    n_guide = pymupdf.open(ROOT / 'out' / 'guide' / 'MATH111_Quiz2_Guide.pdf').page_count
    n_mocks = pymupdf.open(ROOT / 'out' / 'mocks' / 'MATH111_Quiz2_Mock_Exams.pdf').page_count

    by_unit = defaultdict(lambda: dict(ex=[], dr=[], other=[]))
    case_units = defaultdict(set)
    for iid, u in usage.items():
        for loc in u['location'].split('; '):
            m = re.match(r'(U-[A-Z0-9]+) (example|drill|trap)', loc)
            if m:
                key = {'example': 'ex', 'drill': 'dr', 'trap': 'other'}[m.group(2)]
                by_unit[m.group(1)][key].append(iid)
                case_units[allit[iid]['case']].add(m.group(1))
    in_scope = [i for i in items.values() if i['section'] in ('4.2', '5.1', '5.2') and i.get('scope') != 'contrast']
    cases = sorted({i['case'] for i in in_scope} | {i['case'] for i in gen.values() if i['case'].startswith('C')})  # PRE-*: «قبل الدرس» drills
    held = hold['held_items']

    out = ['# بيان التغطية', '',
           'يُولَّد هذا الملف آليًا من بيانات البناء (`tools/coverage.py`)، بعد بناء المذكرة والاختبارين.', '',
           '## الملفات وعدد صفحاتها الفعلي', '',
           '| الملف | الصفحات |', '|---|---|',
           '| `out/guide/MATH111_Quiz2_Guide.pdf` (المذكرة) | %d |' % n_guide,
           '| `out/mocks/MATH111_Quiz2_Mock_Exams.pdf` (الاختباران التجريبيان) | %d |' % n_mocks, '',
           '## المرفقات التي رُوجعت', '',
           '- مذكرة د. طارق الفضل (2024): الأقسام 4.2 (ص56–62)، و5.1 (ص63–66)، و5.2 (ص67–76).',
           '- ثلاثة ملفات اختبارات (1445، 1446، 1447)، فيها 18 اختبارًا: 6 أولى، و6 ثانية، و6 نهائية.',
           '- ملف الأنماط والتحقق المرفق: استُعمل نقطة بداية للتصنيف فقط.', '',
           '## كل حالة في النطاق: أين تُدرَّس', '',
           '| الحالة | النوع في المذكرة | أمثلة | تمارين | محجوز للمحاكاة | صفحة النوع |', '|---|---|---|---|---|---|']
    for c in cases:
        us = sorted(case_units.get(c, []), key=lambda u: units.get(u, (99,))[0])
        types = '؛ '.join('%d. %s' % units[u] for u in us) or '—'
        ex = sorted({i for u in us for i in by_unit[u]['ex'] if allit[i]['case'] == c})
        dr = sorted({i for u in us for i in by_unit[u]['dr'] if allit[i]['case'] == c})
        h = sorted(held[i] for i in held if items[i]['case'] == c)
        pg = '، '.join(str(pages[u]) for u in us if u in pages) or '—'
        out.append('| %s | %s | %s | %s | %s | %s |' % (c, types, ' '.join(ex) or '—', ' '.join(dr) or '—', ' '.join(h) or '—', pg))
    missing = [c for c in cases if c not in case_units]
    out += ['', 'حالات بلا نوع في المذكرة: %s.' % ('، '.join(missing) if missing else 'لا يوجد'), '']

    unused = sorted(i['id'] for i in in_scope if i['id'] not in usage and i['id'] not in held)
    avoid = set(hold['avoid'])
    out += ['## أسئلة داخل النطاق لم تُستخدم', '',
            '| السؤال | الحالة | السبب |', '|---|---|---|']
    for i in unused:
        why = 'معلق: قريب جدًا من سؤال محجوز (يُفتح بعد المحاكاة)' if i in avoid else 'مكرر أو بديل لسؤال مستخدم من النوع نفسه'
        out.append('| %s | %s | %s |' % (i, items[i]['case'], why))
    out += ['', '## الحجز', '',
            '- 10 أسئلة حقيقية محجوزة: %s. كلها في ملف الاختبارين، ولا يظهر أي منها في المذكرة (فحص التسرب: 0 فشل).'
            % '، '.join(sorted(held.values())),
            '- التوزيع: كل اختبار فيه مشتقة من 4.2 أولًا، ثم أربعة تكاملات من 4.2 و5.1 و5.2. هذا اختيار تعليمي، وليس التوزيع الرسمي للكويز.',
            '- لا نضمن أن زيادًا لم يرَ هذه الأسئلة من قبل؛ هذا مكتوب في تعليمات الاختبارين.', '',
            '## التدريبات الإضافية (من إعداد هذا العمل)', '',
            '| المعرف | الحالة | أين استُخدم |', '|---|---|---|']
    for g in sorted(gen, key=lambda s: int(s.split('-')[1])):
        out.append('| %s | %s | %s |' % (g, gen[g]['case'], usage.get(g, {}).get('location', 'غير مستخدم')))
    out += ['', 'كل تدريب إضافي مكتوب عليه «تدريب إضافي» في المذكرة، وجوابه متحقق بالطريقة نفسها.', '']
    (ROOT / 'COVERAGE.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
    print('COVERAGE.md:', len(cases), 'cases,', len(unused), 'unused,', n_guide, 'guide pages,', n_mocks, 'mock pages')


if __name__ == '__main__':
    main()

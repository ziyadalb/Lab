#!/usr/bin/env python3
"""Build the question registry (audit CSV/JSON + a study-safe CSV) and descriptive counts.

Inputs: data/exam_review.jsonl (visual review of the 18 original exams), data/items.json,
reports/verification_report_items.json, data/holdout_ids.json, data/usage.json (optional),
and the secondary transcription (path given as argument) for rows not reviewed visually.
Run: python tools/build_registry.py <transcribed_source.json>
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from similarity import relation  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FILES = {'EX1445': 'M 111 - 451-452 - English.pdf', 'EX1446': 'M111 - 461-462.pdf',
         'EX1447': 'M111 471-472_2.pdf', 'NOTES': 'MATH 111 - Class Notes - 2024 - English (compressed).pdf'}
SEM = {'S1': 'الأول', 'S2': 'الثاني'}
EXAM = {'SE': 'الاختبار الثاني', 'FE': 'النهائي', 'FIRST': 'الاختبار الأول'}
SKILLS = {
    'C42-D': 'قاعدة السلسلة؛ مشتقات 4.1؛ مشتقة a^x وln وlog؛ الأسس والجذور',
    'C42-I-SINH': 'تعويض؛ ضبط الثابت', 'C42-I-COSH': 'تعويض؛ شرط f(x)>a', 'C42-I-TANH': 'تعويض؛ مقارنة |u| بـa',
    'C42-I-CSCH': 'تعويض؛ قيمة مطلقة', 'C42-I-HIDDEN': 'ضرب وقسمة لإظهار المشتقة؛ أسس',
    'C42-I-SPLIT': 'فصل البسط؛ ln', 'C42-I-INVNUM': 'قاعدة القوة مع دالة عكسية',
    'C42-CS': 'إكمال المربع؛ كسور', 'C42-CSL': 'إكمال المربع؛ عامل خطي هو المركز؛ قيمة مطلقة',
    'C34-CONTRAST': 'إكمال المربع؛ صيغة sin^-1 (3.4)',
    'C51-POLY1': 'تجزئة مرة واحدة؛ إشارات', 'C51-POLY2': 'تجزئة متكررة/جدول DI؛ كسور',
    'C51-LN': 'تجزئة؛ أسس سالبة؛ ln', 'C51-LN0': 'تجزئة مع dv=dx؛ قسمة', 'C51-INV': 'تجزئة مع dv=dx؛ تعويض',
    'C51-XINV': 'تجزئة؛ قسمة كثيرات حدود', 'C51-CYC': 'تجزئة مرتين؛ حل معادلة التكامل',
    'C51-EXPH': 'تعريف cosh/sinh الأسّي؛ أسس', 'C51-SEC2': 'تجزئة؛ ∫tan x', 'C51-SUBPARTS': 'تعويض ثم تجزئة',
    'C51-ROOT': 'تعويض w=داخل الجذر أو تجزئة', 'C51-DEF': 'تجزئة؛ تعويض الحدود',
    'C52-ODD1': 'حجز عامل؛ متطابقة فيثاغورس', 'C52-EVEN1': 'نصف الزاوية', 'C52-SC-ODD': 'حجز عامل؛ صف باسكال',
    'C52-SC-EVEN': 'نصف الزاوية مكررًا', 'C52-TS-SEC0': 'تجزئة؛ تكرار', 'C52-TS-TAN0': 'صيغة التخفيض',
    'C52-TS-SECEVEN': 'u=tan؛ صف باسكال', 'C52-TS-TANODD': 'u=sec؛ صف باسكال', 'C52-CC-CSCEVEN': 'u=cot؛ إشارة سالبة',
    'C52-CC-COTODD': 'u=csc؛ إشارة سالبة', 'C52-PROD': 'متطابقات الضرب'}


def main(transcription):
    review = [json.loads(l) for l in (ROOT / 'data' / 'exam_review.jsonl').read_text(encoding='utf-8').splitlines()]
    items = {i['id']: i for i in json.loads((ROOT / 'data' / 'items.json').read_text(encoding='utf-8'))}
    ver = {r['id']: r for r in json.loads((ROOT / 'reports' / 'verification_report_items.json').read_text())['items']}
    hold = json.loads((ROOT / 'data' / 'holdout_ids.json').read_text())
    usage = {}
    for name in ('usage.json', 'usage_guide.json'):      # the full guide's usage replaces the sample's
        f = ROOT / 'data' / name
        if f.exists():
            usage.update(json.loads(f.read_text(encoding='utf-8')))
    sys.path.insert(0, str(ROOT / 'content'))
    from mock_sols import MOCKS                           # where each held question sits in the mocks file
    mock_at = {i: 'الاختبار التجريبي %s، السؤال %d' % (w, k) for w, ids in MOCKS.items() for k, i in enumerate(ids, 1)}
    T = json.loads(Path(transcription).read_text(encoding='utf-8'))
    trans = {r['A']: r for r in T['الأسئلة المدرجة'][1:]}
    trans_ex = {r['A']: r for r in T['المستبعدة'][1:]}

    # duplicate groups over every in-scope item (exam + notes)
    ins = [i for i in items.values() if i['section'] in ('4.2', '5.1', '5.2')]
    groups, near = {}, defaultdict(list)
    gid = 0
    for a_i, a in enumerate(ins):
        for b in ins[a_i + 1:]:
            if a['task'] != b['task'] or a['case'] != b['case']:
                continue
            rel = relation(a, b)
            if rel == 'exact':
                g = groups.get(a['id']) or groups.get(b['id'])
                if not g:
                    gid += 1
                    g = f'DG{gid:02d}'
                groups[a['id']] = groups[b['id']] = g
            elif rel in ('constant_multiple', 'one_number_changed'):
                near[a['id']].append(f"{b['id']} ({rel})")
                near[b['id']].append(f"{a['id']} ({rel})")

    rows = []
    reviewed = set()
    for r in review:
        reviewed.add(r['id'])
        it = items.get(r['id'])
        exam_id, q = r['id'].rsplit('-Q', 1)
        year, sem, kind = exam_id.split('-')
        rows.append(dict(
            id=r['id'], parent_id=exam_id + '-Q' + q.split('.')[0], kind='exam',
            file=FILES[r['src']], pdf_page=r.get('page_span', r['pdf_page']), printed_page=r['pdf_page'],
            year=year, semester=SEM[sem], exam=EXAM[kind], question=q.split('.')[0], part=(q.split('.') + [''])[1],
            marks_official=r.get('marks', ''), english_text=r.get('instr', ''), math=r['expr'],
            task=(it or {}).get('task', ''), section=r['section'], case=(it or {}).get('case', r.get('pattern', '')),
            skills=SKILLS.get((it or {}).get('case', ''), ''),
            solution_source=('حل رسمي في الملف الأصلي (مراجعة بصرية) + حل محقق في هذا العمل' if it else
                             'خارج النطاق: لم يُحل'),
            extraction='استخراج آلي + مراجعة بصرية', note=r.get('note', '')))
    for qid, tr in list(trans.items()) + list(trans_ex.items()):
        if qid in reviewed:
            continue
        exam_id, q = qid.rsplit('-Q', 1)
        year, sem, kind = exam_id.split('-')
        rows.append(dict(id=qid, parent_id=exam_id + '-Q' + q.split('.')[0], kind='exam',
                         file=tr.get('E') or {'1445': FILES['EX1445'], '1446': FILES['EX1446'], '1447': FILES['EX1447']}[year],
                         pdf_page=tr.get('F') or tr.get('B'), printed_page=tr.get('F') or tr.get('B'), year=year,
                         semester=SEM[sem], exam=EXAM[kind], question=q.split('.')[0], part=(q.split('.') + [''])[1],
                         marks_official='', english_text='', math=tr.get('J') or tr.get('C'), task='',
                         section='خارج (6.x/7.x/8.x/2.2/3.x)', case=tr.get('H', ''), skills='',
                         solution_source='لم يُحل (خارج النطاق)',
                         extraction='نقل ثانوي + مراجعة نصية لطبقة نص الأصل (لا رموز داخل النطاق)', note=tr.get('D', '')))
    for year, key in (('1445', 'EX1445'), ('1446', 'EX1446'), ('1447', 'EX1447')):
        for sem in ('S1', 'S2'):
            rows.append(dict(id=f'{year}-{sem}-FIRST', parent_id=f'{year}-{sem}-FIRST', kind='exam_unit',
                             file=FILES[key], pdf_page='1-4' if sem == 'S1' else '16-21', printed_page='',
                             year=year, semester=SEM[sem], exam=EXAM['FIRST'], question='كامل الاختبار', part='',
                             marks_official='', english_text='', math='', task='',
                             section='خارج (1.x–3.x' + ('، و4.1 في 1447-S2' if (year, sem) == ('1447', 'S2') else '') + ')',
                             case='', skills='', solution_source='لم يُحل (خارج النطاق)',
                             extraction='استخراج آلي + مراجعة نصية؛ مراجعة بصرية لـ1445-S1 و1447-S2',
                             note='وحدة العد هنا الاختبار كاملًا لأنه خارج النطاق'))
    for it in items.values():
        if it['kind'] == 'exam':
            continue
        rows.append(dict(id=it['id'], parent_id=it['id'].rsplit('-', 1)[0], kind=it['kind'], file=FILES['NOTES'],
                         pdf_page=it['src']['pdf_page'], printed_page=it['src']['pdf_page'], year='غير معلوم',
                         semester='', exam='مذكرة د. طارق', question=it['src']['number'], part='', marks_official='',
                         english_text=('Find the derivatives of the following:' if it['task'] == 'diff'
                                       else 'Evaluate the following integrals:'),
                         math=it['q'][4:] if it['q'].startswith('raw:') else it['q'], task=it['task'],
                         section=it['section'], case=it['case'], skills=SKILLS.get(it['case'], ''),
                         solution_source=('حل في المذكرة + حل محقق في هذا العمل' if it['kind'] == 'notes_example'
                                          else 'حل محقق في هذا العمل (لا حل في المذكرة)'),
                         extraction='مراجعة بصرية', note=it.get('note', '')))
    held = hold['held_items']
    for r in rows:
        it = items.get(r['id'])
        r['duplicate_group'] = groups.get(r['id'], '')
        r['near_copies'] = '; '.join(near.get(r['id'], []))
        v = ver.get(r['id'])
        r['verification'] = '' if not v else v['answer']['status']
        r['official_check'] = '' if not v or 'official' not in v else v['official']['status']
        in_scope = it is not None and it['section'] in ('4.2', '5.1', '5.2')
        if r['id'] in held:
            r['usage'], r['holdout_id'] = 'محجوز', held[r['id']]
            usage[r['id']] = dict(usage='محجوز', location=mock_at.get(r['id'], ''))
        elif r['id'] in hold['avoid']:
            r['usage'], r['holdout_id'] = 'معلق مؤقتًا: قريب جدًا من سؤال محجوز (لا يستخدم قبل المحاكاة)', ''
        elif it is not None and it.get('scope') == 'contrast':
            r['usage'], r['holdout_id'] = 'مرجع إضافي (صف مقارنة فقط؛ 3.4 خارج النطاق)', ''
        elif in_scope:
            r['usage'], r['holdout_id'] = usage.get(r['id'], {}).get('usage', 'مرجع إضافي (غير مستخدم في المذكرة)'), ''
        else:
            r['usage'], r['holdout_id'] = 'مستبعد (خارج النطاق المثبت)', ''
        r['location'] = usage.get(r['id'], {}).get('location', '')
        r['exclusion_reason'] = '' if in_scope else ('القسم ' + r['section'])
    rows.sort(key=lambda r: (r['kind'] != 'exam', r['id']))
    fields = list(rows[0].keys())
    with (ROOT / 'data' / 'registry_full.csv').open('w', encoding='utf-8-sig', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    (ROOT / 'data' / 'registry_full.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    # study-safe: held items appear only as opaque ids; near copies keep only id + usage
    safe_fields = ['id', 'kind', 'file', 'pdf_page', 'year', 'exam', 'question', 'part', 'section', 'case', 'usage', 'location']
    with (ROOT / 'data' / 'registry_study_safe.csv').open('w', encoding='utf-8-sig', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=safe_fields)
        w.writeheader()
        for r in rows:
            if r['usage'] == 'محجوز':
                w.writerow(dict({k: '' for k in safe_fields}, id=r['holdout_id'], usage='محجوز للمحاكاة'))
            elif r['usage'].startswith('معلق مؤقتًا'):
                w.writerow(dict({k: '' for k in safe_fields}, id=r['id'], usage='معلق مؤقتًا حتى بعد المحاكاة'))
            else:
                w.writerow({k: r[k] for k in safe_fields})
    # counts
    exam_in = [r for r in rows if r['kind'] == 'exam' and items.get(r['id']) and items[r['id']]['section'] in ('4.2', '5.1', '5.2')]
    unique = {r['duplicate_group'] or r['id'] for r in exam_in}
    per_case = defaultdict(set)
    for r in exam_in:
        per_case[r['case']].add(r['id'].rsplit('-Q', 1)[0])
    summary = dict(
        registry_rows=len(rows), kinds=Counter(r['kind'] for r in rows),
        exams_indexed=18, exams_with_in_scope_parts=len({r['id'].rsplit('-Q', 1)[0] for r in exam_in}),
        in_scope_exam_parts=len(exam_in), in_scope_exam_unique=len(unique),
        notes_items=Counter(r['kind'] for r in rows if r['kind'].startswith('notes')),
        usage=Counter(r['usage'] for r in rows),
        appearances_in_independent_exams={k: len(v) for k, v in sorted(per_case.items())},
        duplicate_groups={g: sorted(i for i, gg in groups.items() if gg == g) for g in sorted(set(groups.values()))},
        verification=Counter(r['verification'] for r in rows if r['verification']),
        official=Counter(r['official_check'] for r in rows if r['official_check']))
    (ROOT / 'reports' / 'registry_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])

"""Build riyad111/data/questions.csv (batch 1: six finals + six second exams).
Scope (student, 2026-11-01): Midterm 2, same as 1447-S2 second exam -> 4.2, 5.1-5.5, 6.1.

IDs are reused from math111-quiz2/data/registry_full.csv (stable since Oct 2026).
Q1/Q2 math text comes from that registry (automatic extraction + visual review there);
Q3 rows of the finals were re-read here from the raw text layer (short form, branch
details marked pending until each pattern is opened). Pattern ids: patterns/pattern_map.md.
"""
import csv, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
old = list(csv.DictReader(open(ROOT/'math111-quiz2/data/registry_full.csv', encoding='utf-8-sig')))
FILES = {'1445': 'M 111 - (451-452) - English.pdf', '1446': 'M111 - (461-462).pdf', '1447': 'M111 (471-472)_2.pdf'}

SEC2P = {'2.2': 'P01', '4.2': 'P05', '3.4': 'P05', '5.1': 'P06', '5.2': 'P10', '5.3': 'P07', '5.4': 'P08',
         '5.5': 'P09', '4.1': 'P11', '3.1': 'P11', '3': 'P11', '6.1': 'P12'}
OVR = {  # id: (pattern, branch/note)
 '1445-S1-FE-Q1.2': ('P02', ''), '1445-S2-FE-Q1.2': ('P02', ''), '1446-S1-FE-Q1.2': ('P02', ''),
 '1446-S2-FE-Q1.2': ('P02', ''), '1447-S1-FE-Q1.2': ('P02', ''), '1447-S2-FE-Q1.2': ('P02', ''),
 '1445-S1-FE-Q1.3': ('P03', ''), '1445-S2-FE-Q1.3': ('P03', ''), '1446-S1-FE-Q1.3': ('P03', ''), '1446-S2-FE-Q1.3': ('P03', ''),
 '1447-S1-FE-Q1.3': ('P04', 'f(x)^g(x): اشتقاق لوغاريتمي'), '1447-S2-FE-Q1.3': ('P04', 'خواص ln قبل الاشتقاق'),
 '1445-S1-FE-Q2.5': ('P09', 'x^(1/2)+x^(1/3): u=x^(1/6) ثم قسمة'),
 '1446-S2-FE-Q2.5': ('P05', 'تهيئة أسس: 4^(2-x)=16/2^(2x) ثم u=2^x و tan^-1'),
 '1447-S1-FE-Q2.3': ('P11', 'تعويض مباشر u = داخل sec'),
 '1447-S2-FE-Q2.1': ('P11', '1/(x(1+ln x)): u=1+ln x'),
 '1447-S2-FE-Q2.2': ('P05', 'u=sec x ثم tan^-1'),
}
for k in [r['id'] for r in old if r['kind'] == 'exam' and r['section'].startswith('2.2') and r['id'].endswith('Q1.1')]:
    OVR.setdefault(k, ('P01', ''))
# second-exam rows that are derivatives (Q1) -> P03
Q3 = [  # finals, part 3 (re-read from raw text layer; page = pdf page from old registry)
 ('1445-S1-FE-Q3.1', 'lim_{x->inf} (e^x+5x)/(e^(2x)+...)  [L Hopital]', 'P12', 'inf/inf'),
 ('1445-S1-FE-Q3.2', 'int_1^inf dx/(2x-1)^3', 'P13', 'حد لانهائي واحد'),
 ('1445-S1-FE-Q3.3', 'area: y=-x^2, y=x^2+1, x=-1, x=2', 'P14', 'حدود مُعطاة بخطوط رأسية'),
 ('1445-S1-FE-Q3.4', 'volume about x-axis: y=x^2, y=x', 'P15', 'حلقات (washer)'),
 ('1445-S1-FE-Q3.5', 'arc length y=2+cosh x, 0..ln2', 'P16', 'مربع كامل: 1+sinh^2=cosh^2'),
 ('1445-S1-FE-Q3.6', 'polar->Cartesian r=8cos t+6sin t', 'P17', 'ضرب في r'),
 ('1445-S1-FE-Q3.7', 'polar area inside r=3+3cos t outside a circle', 'P18', 'داخل منحنى وخارج آخر'),
 ('1445-S2-FE-Q3.1', 'int_0^inf x e^(1-x^2) dx', 'P13', 'حد لانهائي واحد'),
 ('1445-S2-FE-Q3.2', 'area: y=4-x^2, y=x+2', 'P14', 'حدود من التقاطع'),
 ('1445-S2-FE-Q3.3', 'volume about x-axis: y=4-x^2, y=x+4, x=2', 'P15', 'حلقات'),
 ('1445-S2-FE-Q3.4', 'arc length y=sqrt(1-x^2), -1..1', 'P16', 'نصف دائرة'),
 ('1445-S2-FE-Q3.5', 'polar->Cartesian r=8sin t+6cos t', 'P17', 'ضرب في r'),
 ('1445-S2-FE-Q3.6', 'polar area inside r=2+2cos t outside r=3', 'P18', 'داخل منحنى وخارج آخر'),
 ('1446-S1-FE-Q3.1', 'lim_{x->inf} e^(-x^3)(x^4+1)', 'P12', '0·inf تُعاد كتابته كسرًا'),
 ('1446-S1-FE-Q3.2', 'int_2^inf dx/(x (ln x)^2)', 'P13', 'حد لانهائي واحد + تعويض u=ln x'),
 ('1446-S1-FE-Q3.3', 'area: y=4-x^2, y=x-2', 'P14', 'حدود من التقاطع'),
 ('1446-S1-FE-Q3.4', 'volume about x-axis: y=sqrt(x-1), y=0, x=5', 'P15', 'أقراص (disc)'),
 ('1446-S1-FE-Q3.5', 'arc length y=ln|sec x| (حسب السجل السابق؛ يراجع بصريًا)', 'P16', 'مربع كامل: 1+tan^2=sec^2'),
 ('1446-S1-FE-Q3.6', 'polar->Cartesian r=1/(sin t-2cos t)', 'P17', 'ضرب المقام'),
 ('1446-S1-FE-Q3.7', 'polar area inside r=2-2cos t outside r=2+2cos t', 'P18', 'داخل منحنى وخارج آخر'),
 ('1446-S2-FE-Q3.1', 'lim_{x->inf} (x-x e^x)/(x+2x e^x)', 'P12', 'inf/inf'),
 ('1446-S2-FE-Q3.2', 'int_{-inf}^{inf} dx/(x^2+4)', 'P13', 'حدان لانهائيان: تقسيم'),
 ('1446-S2-FE-Q3.3', 'area: y=5x^2, y=4+x^2', 'P14', 'حدود من التقاطع'),
 ('1446-S2-FE-Q3.4', 'volume about x-axis: y=x^2, y=-x+2', 'P15', 'حلقات'),
 ('1446-S2-FE-Q3.5', 'arc length y=(e^x+e^-x)/2 on [0,ln3]', 'P16', 'مربع كامل: cosh'),
 ('1446-S2-FE-Q3.6', 'polar->Cartesian 1/r = (sin t+5cos t)/2', 'P17', 'ضرب المقام'),
 ('1446-S2-FE-Q3.7', 'polar area r=1+cos t in 2nd quadrant', 'P18', 'منحنى واحد بحدود زاوية'),
 ('1447-S1-FE-Q3.1', 'lim_{x->inf} x^(1/x)', 'P12', 'inf^0 عبر e^(ln)'),
 ('1447-S1-FE-Q3.2', 'int_0^inf x/(1+x^2)^2 dx', 'P13', 'حد لانهائي واحد + تعويض'),
 ('1447-S1-FE-Q3.3', 'area: y=x^2, y=sqrt x', 'P14', 'حدود من التقاطع'),
 ('1447-S1-FE-Q3.4', 'volume about x-axis: y=x^2, y=x+2', 'P15', 'حلقات'),
 ('1447-S1-FE-Q3.5', 'arc length y=(2/3)x sqrt x, 0..1', 'P16', '1+(y\')^2 = 1+x'),
 ('1447-S1-FE-Q3.6', 'polar->Cartesian r=cos t+sec t', 'P17', 'ضرب في r'),
 ('1447-S1-FE-Q3.7', 'common region r=2 and r=2+2cos t', 'P18', 'منطقة مشتركة'),
 ('1447-S2-FE-Q3.1', 'lim_{x->inf} (1+4/x)^(2x)', 'P12', '1^inf عبر e^(ln)'),
 ('1447-S2-FE-Q3.2', 'int_0^2 dx/sqrt(2-x)', 'P13', 'انقطاع عند طرف'),
 ('1447-S2-FE-Q3.3', 'area: y=2-x^2, y=x', 'P14', 'حدود من التقاطع'),
 ('1447-S2-FE-Q3.4', 'volume about x-axis: y=x^2/2, y=2', 'P15', 'حلقات'),
 ('1447-S2-FE-Q3.5', 'arc length y=ln|sec x|, 0..pi/4', 'P16', 'مربع كامل: 1+tan^2=sec^2'),
 ('1447-S2-FE-Q3.6', 'polar->Cartesian 3/r = sin t - sec t', 'P17', 'ضرب في r'),
 ('1447-S2-FE-Q3.7', 'polar area 1st quadrant inside r=1+sin t outside r=1', 'P18', 'داخل منحنى وخارج آخر'),
]
P08_BRANCH = {'1445-S1-SE-Q2.8': 'B1', '1445-S2-SE-Q2.8': 'B1', '1446-S1-SE-Q2.8': 'B1', '1446-S2-SE-Q2.9': 'B1',
              '1447-S1-SE-Q2.8': 'B3', '1447-S2-SE-Q3.6': 'B1', '1445-S1-FE-Q2.4': 'B1', '1445-S2-FE-Q2.4': 'B2',
              '1446-S1-FE-Q2.4': 'B1', '1446-S2-FE-Q2.3': 'B1', '1447-S1-FE-Q2.4': 'B4', '1447-S2-FE-Q2.4': 'B5'}
rows = []
oldq3 = {r['id']: r for r in old}
def paper(i): return i.split('-Q')[0]
for r in old:
    if r['kind'] != 'exam' or r['exam'] not in ('النهائي', 'الاختبار الثاني'): continue
    i = r['id']
    if '-FE-Q3' in i: continue
    pat, br = OVR.get(i, (None, ''))
    if pat is None:
        if '-SE-Q1.' in i: pat = 'P03'
        else: pat = SEC2P.get(r['section'].split()[0], '؟')
    if pat == 'P08': br = P08_BRANCH[i]
    ver = 'مثبت رمزيًا (reports/verify_p08.json)' if pat == 'P08' else ('مثبت رمزيًا في math111-quiz2' if r['verification'] == 'symbolic' else 'لم يُحقق بعد (يفتح مع نمطه)')
    rows.append(dict(id=i, paper=paper(i), paper_type='نهائي' if '-FE-' in i else 'ثاني', file=FILES[i[:4]], pdf_page=r['pdf_page'],
                     marks=r['marks_official'], task=r['english_text'] or r['task'], math=r['math'], pattern=pat, branch=br,
                     solution='حل رسمي في الملف', verification=ver, note=r['note']))
for i, m, pat, br in Q3:
    o = oldq3.get(i, {})
    rows.append(dict(id=i, paper=paper(i), paper_type='نهائي', file=FILES[i[:4]], pdf_page=o.get('pdf_page', ''), marks='',
                     task='', math=m, pattern=pat, branch=br + ' (مبدئي)', solution='حل رسمي في الملف',
                     verification='لم يُحقق بعد (يفتح مع نمطه)', note='استخراج من طبقة النص الخام؛ مراجعة بصرية عند فتح النمط'))
# --- scope (2026-11-01, student): Midterm 2 = same scope as 1447-S2 second exam -> 4.2, 5.1-5.5, 6.1
SEC_BY_PAT = {'P01': '2.2', 'P02': '2.2', 'P03': '4.2', 'P04': '3.x', 'P06': '5.1', 'P07': '5.3', 'P08': '5.4',
              'P09': '5.5', 'P10': '5.2', 'P12': '6.1', 'P13': '6.2', 'P14': '7.1', 'P15': '7.2', 'P16': '7.3',
              'P17': '8.2', 'P18': '8.4'}
SEC_FIX = {'1446-S2-FE-Q2.5': '3.4', '1447-S2-FE-Q2.2': '3.4', '1447-S1-FE-Q2.3': '2.4/3.x', '1447-S2-FE-Q2.1': '3.1',
           '1447-S1-FE-Q1.3': '3.3', '1447-S2-FE-Q1.3': '3.1'}
IN = {'4.2', '5.1', '5.2', '5.3', '5.4', '5.5', '6.1'}
oldsec = {r['id']: r['section'] for r in old}
for d in rows:
    sec = SEC_FIX.get(d['id']) or SEC_BY_PAT.get(d['pattern'])
    if d['pattern'] in ('P05', 'P11') and d['id'] not in SEC_FIX:
        sec = oldsec.get(d['id'], '').split()[0]
    d['section'] = sec
    if sec in IN: d['in_scope'] = 'داخل'
    elif sec in ('3.4', '4.1'): d['in_scope'] = 'أساس (خارج كسؤال مستقل)'
    else: d['in_scope'] = 'خارج'
rows.sort(key=lambda d: d['id'])
out = ROOT/'riyad111/data/questions.csv'
with open(out, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=['id','paper','paper_type','file','pdf_page','marks','section','in_scope','task','math','pattern','branch','solution','verification','note']); w.writeheader(); w.writerows(rows)
# counts per pattern: questions and independent papers (union of ids)
cnt = collections.defaultdict(lambda: {'q': set(), 'p': set(), 'pf': set()})
for d in rows:
    if d['in_scope'] != 'داخل': continue
    c = cnt[d['pattern']]; c['q'].add(d['id']); c['p'].add(d['paper'])
    if d['paper_type'] == 'نهائي': c['pf'].add(d['paper'])
print(len(rows), 'rows')
for k in sorted(cnt):
    print(k, 'questions', len(cnt[k]['q']), 'papers', len(cnt[k]['p']), 'finals', len(cnt[k]['pf']))

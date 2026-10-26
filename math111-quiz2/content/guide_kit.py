"""Building blocks of the full guide: one unit per question type.

A unit is: card (idea, sign and what it is confused with) -> reminder -> shortcut -> examples, each solved
first with the shortcut in short numbered steps and then line by line with the basic method -> algebra boxes
where an algebra move is needed -> trap -> what to write on the quiz paper and a quick check -> exercises
(guided, partial, on your own) -> their full solutions on the next page. The two lighter help levels of every
exercise (a hint about the sign, then the first written step) are collected at the end of the guide and
linked both ways, so nothing is printed upside down or hidden.

Every math line goes through a check (tools/booklet_engine.py); a failed check stops the build.
"""
import re

from booklet import final as _final, prompt, source_label
from booklet_engine import BLOCKED
from booklet_engine import (ITEMS, BuildError, ans_tex, arith, diff_step_ok, formula, functional, parts_rows, q_tex,
                            same_antiderivative, same_defint, same_derivative, step_ok, sub_row, use)
from html_kit import box, chip, en, lines, link, md, mi, p, table, ul
from mathlib import rawtex, tex, texsum

DAYS = {}          # day number -> list of (uid, number, title)
GIST = {}          # uid -> (number, title, what you see, first step, rule): the one-line summary, reused by the lesson maps
LESSON_OF_UID = {} # uid -> lesson (4.2, 5.1, 5.2)
DRILLS_N = {}      # uid -> number of exercises (for the time plan of the day)
ALG_SEEN = {}      # algebra skill -> title (first, detailed explanation carries the anchor)
HELP = []          # one entry per exercise: the two lighter help levels, printed at the end of the guide
TRY_KEYS = []      # algebra try-its: (skill, title, answer latex)
FINAL_ROW = set()  # items whose last step row already shows the final answer
COUNTER = [0]

# study day of every unit (days 1-2 are done; days 3-6 are the four days left before the quiz)
DAY_OF = {'U-D1': 1, 'U-D2': 1, 'U-I1': 1, 'U-I2': 2, 'U-I3': 2,
          'U-I4': 2, 'U-I5': 2, 'U-I6': 2, 'U-I7': 2, 'U-I8': 2, 'U-I9': 3,
          'U-P1': 3, 'U-P2': 3, 'U-P3': 3, 'U-P4': 4, 'U-P5': 4,
          'U-P6': 4, 'U-P7': 4, 'U-P8': 4, 'U-P9': 4, 'U-P10': 4,
          'U-T1': 5, 'U-T2': 5, 'U-T3': 5, 'U-T4': 5, 'U-T5': 6,
          'U-T6': 6, 'U-T7': 6, 'U-T8': 6}
# where to read in Dr. Tariq's notes: the explanation pages, then the page of the exercises used here
PAGES = {'U-D2': 'ص59، تمارين ص62', 'U-I1': 'ص59–60، تمارين ص62', 'U-I2': 'ص60، تمارين ص62', 'U-I3': 'ص60–61، تمارين ص62',
         'U-I4': 'ص61، تمارين ص62', 'U-I5': 'ص61', 'U-I6': 'تمارين ص62', 'U-I7': 'تمارين ص62', 'U-I8': 'ص61، تمارين ص62',
         'U-I9': 'ص61، تمارين ص62', 'U-P1': 'ص63، تمارين ص66', 'U-P2': 'ص63، تمارين ص66', 'U-P3': 'ص64، تمارين ص66',
         'U-P4': 'ص64، تمارين ص66', 'U-P5': 'من الاختبارات السابقة', 'U-P6': 'ص64–65، تمارين ص66', 'U-P7': 'ص65، تمارين ص66',
         'U-P8': 'ص65، تمارين ص66', 'U-P9': 'تمارين ص66', 'U-P10': 'تمارين ص66', 'U-T1': 'ص67', 'U-T2': 'ص68–69، تمارين ص76',
         'U-T3': 'ص67–70، تمارين ص76', 'U-T4': 'ص70–71', 'U-T5': 'ص71–72، تمارين ص76', 'U-T6': 'ص70–73، تمارين ص76',
         'U-T7': 'ص73، تمارين ص76', 'U-T8': 'ص74–75، تمارين ص76'}
# the prerequisite pages (guide_prereq.py) each type relies on, shown as links in the type's header
NEEDS = {'U-D1': ['P-A2', 'P-A3'], 'U-D2': ['P-A2', 'P-A1'], 'U-I1': ['P-A4', 'P-A1'], 'U-I2': ['P-A4', 'P-A1'],
         'U-I3': ['P-A4', 'P-A1'], 'U-I4': ['P-A4', 'P-A1'], 'U-I5': ['P-A4', 'P-A1'], 'U-I6': ['P-A4'], 'U-I7': ['P-A4', 'P-A2'],
         'U-I8': ['P-A4', 'P-A1'], 'U-I9': ['P-A4', 'P-A1'],
         'U-P1': ['P-B2'], 'U-P2': ['P-B2', 'P-B3'], 'U-P3': ['P-B1', 'P-A1'], 'U-P4': ['P-B1', 'P-B3'], 'U-P5': ['P-B3'],
         'U-P6': ['P-B1', 'P-B2'], 'U-P7': ['P-B1', 'P-B3'], 'U-P8': ['P-B2', 'P-B3'], 'U-P9': ['P-A3', 'P-B3'], 'U-P10': ['P-A4', 'P-B2'],
         'U-T1': ['P-C3', 'P-C2'], 'U-T2': ['P-C3', 'P-C2'], 'U-T3': ['P-C1'], 'U-T4': ['P-C3', 'P-C1'], 'U-T5': ['P-C3', 'P-C1'],
         'U-T6': ['P-C1'], 'U-T7': ['P-C3', 'P-C1'], 'U-T8': ['P-C1']}
NEED_LABEL = {'P-A1': 'أ1', 'P-A2': 'أ2', 'P-A3': 'أ3', 'P-A4': 'أ4', 'P-B1': 'ب1', 'P-B2': 'ب2', 'P-B3': 'ب3',
              'P-C1': 'ج1', 'P-C2': 'ج2', 'P-C3': 'ج3'}
# writing space in lines of 7.5 mm: a start needs a few lines, a full solution more (5.1 solutions are longest)
WRITE = {'G': {'4.2': 2, '5.1': 2, '5.2': 2}, 'P': {'4.2': 3, '5.1': 3, '5.2': 3}, 'I': {'4.2': 4, '5.1': 5, '5.2': 4}}
ASK = {'diff': 'المطلوب: المشتقة', 'int': 'المطلوب: احسب التكامل', 'defint': 'المطلوب: احسب التكامل المحدد'}
# the date shown for each study day (days 1 and 2 are already done)
DAY_NAME = {1: '20 أكتوبر ✓', 2: '21–22 أكتوبر ✓', 3: 'الجمعة 23', 4: 'السبت 24', 5: 'الأحد 25', 6: 'الاثنين 26', 7: 'إذا بقي وقت'}
# lesson colour class of each section (unit header band and the lesson map)
LESSON_CLS = {'4.2': 'l42', '5.1': 'l51', '5.2': 'l52'}
MAPS_READY = {'4.2', '5.1', '5.2'}   # lessons whose map page is built (every type of the lesson has its one-line summary)

# ---------------------------------------------------------------- v7: cases ordered by the method that solves them
# old type numbers (guide v1–v6): for the old → new table, and to rewrite «النوع N» in texts written before v7
OLD_ORDER = ['U-D1', 'U-D2', 'U-I1', 'U-I2', 'U-I3', 'U-I4', 'U-I5', 'U-I6', 'U-I7', 'U-I8', 'U-I9',
             'U-P1', 'U-P2', 'U-P3', 'U-P4', 'U-P5', 'U-P6', 'U-P7', 'U-P8', 'U-P9', 'U-P10',
             'U-T1', 'U-T2', 'U-T3', 'U-T4', 'U-T5', 'U-T6', 'U-T7', 'U-T8']
OLD_NUM = {uid: k for k, uid in enumerate(OLD_ORDER, 1)}
# how many times each case came in the 12 past second and final exams 1445–1447 (in-scope parts, held ones included)
FIRE = {'U-D1': 15, 'U-D2': 1, 'U-I1': 1, 'U-I2': 1, 'U-I3': 1, 'U-I4': 2, 'U-I5': 1, 'U-I6': 0, 'U-I7': 0, 'U-I8': 5,
        'U-I9': 3, 'U-P1': 3, 'U-P2': 2, 'U-P3': 4, 'U-P4': 0, 'U-P5': 1, 'U-P6': 4, 'U-P7': 2, 'U-P8': 1, 'U-P9': 3,
        'U-P10': 0, 'U-T1': 0, 'U-T2': 4, 'U-T3': 0, 'U-T4': 2, 'U-T5': 1, 'U-T6': 0, 'U-T7': 1, 'U-T8': 0,
        'U-LD': 0, 'U-34': 3, 'U-X2': 0, 'U-LN': 0, 'U-CH': 0}
# the four methods: letter, name, colour class
METHODS = {'A': ('أ', 'الاشتقاق', 'mA'), 'B': ('ب', 'التعويض', 'mB'), 'P': ('🔧', 'التجهيزات', 'mP'), 'C': ('ج', 'التجزئة', 'mC')}
METHOD_OF = {}     # uid -> method key, set by the renderer from the section a case sits in
# where each case sits in the decision tree (the four questions, page «الشجرة»)
TREE_DEFAULT = {'A': 'س1: مشتقة ← أ. الاشتقاق', 'B': 'س2: دالة ومشتقتها، أو قانون جاهز ← ب. التعويض',
                'P': 'س3: علامة تجهيز ← سوّ الحركة، ثم ارجع لـ س2', 'C': 'س4: ضرب نوعين، أو ln أو دالة عكسية لحالها ← ج. التجزئة'}
TREE = {'U-T1': 'س2 بعد ما تحجز ← ب. التعويض', 'U-T2': 'س2 بعد ما تحجز ← ب. التعويض', 'U-T4': 'س2 بعد ما تحجز ← ب. التعويض',
        'U-T5': 'س2 بعد ما تحجز ← ب. التعويض', 'U-T7': 'س2 بعد ما تحجز ← ب. التعويض',
        'U-34': 'س2: قانون جاهز، بس من أي درس؟ ← 3.4 أم 4.2 (وقبله س3: كمّل المربع إذا لزم)',
        'U-T6': 'س3: tan لحالها ← اكسر tan، ثم س2 (و $\\sec^3x$ لحالها: س4 تجزئة)',
        'U-P10': 'س2 أول: تعويض يشيل الجذر ← ثم س4: تجزئة', 'U-P5': 'س4 ← ج. التجزئة، ثم عوّض الحدّين مرة وحدة'}
NUM = {}           # uid -> case number (document order)
CASES = []         # (uid, number, title) in document order
MUSA_COUNT = {}    # uid -> usable questions in Dr. Musa's notes (data/musa_index.json, filled by the renderer)


try:                # v7: Dr. Musa's questions that replace our written (✏️) drills, by case
    from musa_drills import MUSA_DRILLS
except ImportError:
    MUSA_DRILLS = {}
MUSA_OVER_NOTES = {'U-T8'}   # no written drill to replace there: Dr. Musa comes before Dr. Tariq
BAN = {'G-13'}       # one number away from a mock question (H10): never printed
# past-exam questions freed in v7 (they left the mocks): (uid, item, level, hint, solution rows)
EXAM_ADD = [
    ('U-T2', '1445-S1-SE-Q2.4', 'I', 'الاثنين فرديين: احجز من الأصغر ($\\cos x$)، و $u=\\sin x$.', [
        ('tex', r'\sin^{5}x\cos^{3}x=\sin^{5}x\,(1-\sin^{2}x)\cos x', [('sin(x)**5*cos(x)**3', 'sin(x)**5*(1-sin(x)**2)*cos(x)')],
         'الاثنين فرديين: نحجز من الأصغر، $\\cos x$'),
        ('sub', 'sin(x)', 'cos(x)', '$u=\\sin x$'),
        ('tex', r'I=\int u^{5}(1-u^{2})\,du=\int\left(u^{5}-u^{7}\right)du', [('x**5*(1-x**2)', 'x**5-x**7')], 'نوزّع'),
        ('line', 'sin(x)**6/6-sin(x)**8/8', 'نكامل ونرجع $u$')]),
    ('U-T2', '1445-S2-FE-Q2.6', 'I', 'sin فردي: احجز $\\sin x$، و $u=\\cos x$.', [
        ('tex', r'\sin^{5}x\cos^{6}x=(1-\cos^{2}x)^{2}\cos^{6}x\,\sin x', [('sin(x)**5*cos(x)**6', '(1-cos(x)**2)**2*cos(x)**6*sin(x)')],
         'sin فردي: نحجز $\\sin x$'),
        ('sub', 'cos(x)', '-sin(x)', '$u=\\cos x$، و $\\sin x\\,dx=-du$'),
        ('tex', r'I=-\int u^{6}(1-u^{2})^{2}\,du=-\int\left(u^{6}-2u^{8}+u^{10}\right)du', [('x**6*(1-x**2)**2', 'x**6-2*x**8+x**10')],
         'نفك القوس ونوزّع، و🔴 السالب قدّام'),
        ('line', '-cos(x)**7/7+2*cos(x)**9/9-cos(x)**11/11', 'نكامل ونرجع $u$')]),
    ('U-T4', '1445-S2-SE-Q2.3', 'I', 'sec زوجي: احجز $\\sec^2x$، و $u=\\tan x$.', [
        ('tex', r'\tan^{2}x\sec^{4}x=\tan^{2}x\,(1+\tan^{2}x)\sec^{2}x', [('tan(x)**2*sec(x)**4', 'tan(x)**2*(1+tan(x)**2)*sec(x)**2')],
         'sec زوجي: نحجز $\\sec^2x$'),
        ('sub', 'tan(x)', 'sec(x)**2', '$u=\\tan x$'),
        ('tex', r'I=\int\left(u^{2}+u^{4}\right)du', [('x**2*(1+x**2)', 'x**2+x**4')], 'نوزّع'),
        ('line', 'tan(x)**3/3+tan(x)**5/5', 'نكامل ونرجع $u$')])]
RANK = {'exam': 0, 'musa': 1, 'generated': 3}     # which exercises a case prints first: past exams, Dr. Musa, Dr. Tariq, ours
LAST_Q = [None]      # the item of the last question() call (to know which item a 🧱 example shows)
SC_ITEM = [None]     # the item of the last shortcut() call (its 🧱 example is the one kept)
EXTRA = []         # (uid, item id): exercises over a case's cap; the mastery checks take them, past exams first
SOLS_BY_METHOD = {}  # method key -> solution blocks of its cases (printed at the end of the method)


def cap(uid):
    """Exercises printed per case, by how often it came in the past exams (the prerequisite parts have none)."""
    if uid.startswith('P-'):
        return 0
    n = FIRE.get(uid, 0)
    return 4 if n >= 4 else 3 if n else 2


def lean_steps(cells):
    """A drill solution: the steps only; the reason is written once, for the first (deciding) row."""
    why = cells[0][1]
    body = ''.join('<tr class="%s"><td class="n">%d</td><td>%s</td></tr>' % ('final' if fin else '', k, mi(r'\displaystyle ' + latex))
                   for k, (latex, _, fin) in enumerate(cells, 1))
    return ((p(rich(why), 'leanwhy') if why else '')
            + '<table class="steps lean"><tbody>' + body + '</tbody></table>')


def mname(m):
    """«ب. التعويض», «🔧 التجهيزات»."""
    letter, name = METHODS[m][0], METHODS[m][1]
    return ('%s %s' if letter == '🔧' else '%s. %s') % (letter, name)


def times(n):
    """«مرة / مرتين / 3 مرات» in the guide's dialect."""
    return {1: 'مرة', 2: 'مرتين'}.get(n, '%d مرات' % n if 3 <= n <= 10 else '%d مرة' % n)


def fire(uid):
    n = FIRE.get(uid, 0)
    return 'جا في الاختبارات %s' % times(n) if n else 'ما جا في الاختبارات'


def src_icon(it):
    """📝 past exam, 📗 Dr. Musa, 📘 Dr. Tariq, ✏️ written for this guide."""
    return {'exam': '📝', 'musa': '📗', 'generated': '✏️'}.get(it['kind'], '📘')


def renum(text):
    """Rewrite old type numbers («النوع 12», «النوعين 14 و17», «الأنواع 22 إلى 25») as the new case numbers."""
    new = lambda n: NUM.get(OLD_ORDER[int(n) - 1]) if 1 <= int(n) <= len(OLD_ORDER) else None
    text = text.replace('هذا النوع', 'هذي الحالة')

    def many(nums):
        got = sorted({new(n) for n in nums if new(n)})
        return ' و'.join(str(g) for g in got) if len(got) < 3 else '، '.join(str(g) for g in got[:-1]) + ' و' + str(got[-1])

    def rng(m):
        a, b = int(m.group(2)), int(m.group(3))
        return m.group(1) + many(range(a, b + 1))

    text = re.sub(r'(الأنواع )(\d+) ?(?:إلى|–|-) ?(\d+)', lambda m: rng(m).replace('الأنواع ', 'الحالات '), text)
    text = re.sub(r'(النوعين|النوعان|الأنواع) (\d+) ?و ?(\d+)',
                  lambda m: {'النوعين': 'الحالتين', 'النوعان': 'الحالتان', 'الأنواع': 'الحالات'}[m.group(1)] + ' '
                  + many([m.group(2), m.group(3)]), text)
    return re.sub(r'النوع (\d+)', lambda m: 'الحالة %s' % (new(m.group(1)) or m.group(1)), text)


def part(heading, inner, cls=''):
    """A section of a case page: a heading and its content in one column (no box)."""
    return '<div class="part %s"><h4 class="ph">%s</h4>%s</div>' % (cls, heading, inner)


def ex_label(label):
    """«🧱 مثال محلول خطوة خطوة (اختبار سابق)» -> «🧱 مثال · 📝 من اختبار سابق»."""
    out = re.sub(r'مثال ?\d+ ?', 'مثال ', label.replace('محلول خطوة خطوة ', '').replace(' محلول', ''))
    for old, new in (('(اختبار سابق)', '· 📝 من اختبار سابق'), ('(من مذكرة د. طارق)', '· 📘 من مذكرة د. طارق'),
                     ('(تمرين من مذكرة د. طارق)', '· 📘 تمرين من مذكرة د. طارق'), ('(من مذكرة د. موسى)', '· 📗 من مذكرة د. موسى')):
        out = out.replace(old, new)
    return out


def unit_minutes(uid):
    """Study time of one type: 10 minutes for the explanation and 5 per exercise (plus a 5-minute break)."""
    return 10 + 5 * DRILLS_N.get(uid, 3)


def rich(text):
    """Arabic text with $...$ math islands."""
    parts = text.split('$')
    return ''.join(mi(seg) if i % 2 else seg for i, seg in enumerate(parts))


def pgref(anchor):
    return '<span class="pgref" data-target="%s"></span>' % anchor


def question(it, where, allow_held=False):
    use(it['id'], where, allow_held=allow_held)
    LAST_Q[0] = (it['id'], where)
    return '<div class="q">' + chip(src_icon(it) + ' ' + source_label(it), 'src') + en(prompt(it)) + md(q_tex(it)) + '</div>'


def drill_question(it, where):
    """An exercise: just the question (its English instruction is printed once above the list, its source with the
    solution)."""
    use(it['id'], where)
    return '<div class="q">' + md(q_tex(it)) + '</div>'


def _flat(latex):
    return re.sub(r'\s+', '', latex)


def step_cells(it, rows, label):
    """Check every row of a basic-method solution and return (latex, why, is_final) per row. Row kinds:
    ('parts', u, dv, du, v, why[, branch])   integration by parts: du and v are checked
    ('sub', u, du, why[, var[, branch]])      substitution line: du is checked (on a branch x = phi(t) if given)
    ('line', expr, why)                      a line equal to the integral (may contain Integral) or derivative
    ('tex', latex, claims, why)              typed line; every claim is checked exactly
    The last row is marked final when it prints exactly the verified answer, so the answer is not repeated.
    """
    out = []
    for k, row in enumerate(rows):
        kind, tag = row[0], '%s step %d' % (label, k + 1)
        is_final = False
        if kind == 'parts':
            _, u, dv, du, v, why = row[:6]
            latex = parts_rows(u, dv, du, v, tag, branch=row[6] if len(row) > 6 else None)
            latex = r'\begin{array}{l}\displaystyle ' + latex.replace('\\\\', '\\\\[6pt] \\displaystyle ') + r'\end{array}'
        elif kind == 'sub':
            _, u, du, why = row[:4]
            latex = sub_row(u, du, tag, var=row[4] if len(row) > 4 else 'u', branch=row[5] if len(row) > 5 else None)
        elif kind == 'line':
            _, expr, why = row
            body = rawtex(expr)
            if it['task'] == 'diff':
                diff_step_ok(expr, it, tag)
                latex = "y' = " + body
            else:
                step_ok(expr, it, tag)
                latex = 'I = ' + body + ('' if 'Integral' in expr else ' + C')     # the doctor's paper: I = …
            is_final = (k == len(rows) - 1 and 'Integral' not in expr and it['task'] != 'defint'
                        and _flat(body) == _flat(texsum(it['answer'])))
        elif kind == 'tex':
            _, latex, claims, why = row
            latex = arith(latex, claims, tag)
        else:
            raise BuildError('unknown step kind ' + kind)
        out.append((latex, why, is_final))
    return out


def steps_table(cells, cls=''):
    body = ''.join('<tr class="%s"><td class="n">%d</td><td>%s</td><td>%s</td></tr>'
                   % ('final' if fin else '', k, mi(r'\displaystyle ' + latex), rich(why))
                   for k, (latex, why, fin) in enumerate(cells, 1))
    return ('<table class="steps%s"><thead><tr><th>#</th><th>الخطوة</th><th>ليش؟</th></tr></thead><tbody>'
            % (' ' + cls if cls else '') + body + '</tbody></table>')


def steps(it, rows, label):
    """Basic method, numbered, one line per step, each with its reason (see step_cells)."""
    cells = step_cells(it, rows, label)
    if cells and cells[-1][2]:
        FINAL_ROW.add(it['id'])
    return steps_table(cells)


def doctor_terms(it):
    """The answer terms in the course doctor's coth⁻¹ sign (lecture 13: d/dx coth⁻¹u = −u'/(1−u²) and
    ∫du/(a²−u²) = −(1/a)coth⁻¹(u/a)), or None when the question has no coth⁻¹. Checked: they are exactly the true
    answer of the same question with coth⁻¹ replaced by −coth⁻¹."""
    import itertools
    import sympy as sp
    from booklet_engine import _record, _strip
    from mathlib import P, x
    if 'acoth' not in it['q'] + ' '.join(it['answer']):
        return None
    flip = lambda e: e.replace(sp.acoth, lambda z: -sp.acoth(z))
    terms = [P(t) for t in it['answer']]
    if it['task'] != 'diff':
        out = [flip(t) for t in terms]
        _record('doctor coth', any(sp.simplify(a - b) != 0 for a, b in zip(out, terms)), item=it['id'])
        return out
    target = sp.diff(flip(P(_strip(it['q']))), x)
    br = P(it['branches'][0]) if it.get('branches') else x
    for signs in sorted(itertools.product((1, -1), repeat=len(terms)), key=lambda v: v.count(-1)):
        cand = [sg * t for sg, t in zip(signs, terms)]
        if sp.simplify((sum(cand) - target).subs(x, br)) == 0:
            _record('doctor coth', -1 in signs, item=it['id'])
            return cand
    raise BuildError('no doctor form for %s' % it['id'])


def _two_lines(lhs, terms, tail, at=2):
    """A long answer on two lines (after `at` terms), so it fits a solution column."""
    from mathlib import texsum as _ts
    if len(terms) <= at:
        return lhs + _ts(terms) + tail
    rest = _ts(terms[at:])
    rest = rest if rest.lstrip().startswith('-') else '+ ' + rest
    return r'\begin{aligned}%s%s\\ &\quad %s%s\end{aligned}' % (lhs.replace('=', '&=', 1), _ts(terms[:at]), rest, tail)


def answer_box(it, where, narrow=False):
    """Check the answer and print it in the green box (derivatives start with y' =). With coth⁻¹ the doctor's sign
    comes first (he marks the quiz) and the true sign in a small line under it. narrow: a solution column."""
    import sympy as _sp
    from mathlib import P as _P, texsum as _ts
    html = _final(it, where)
    lhs0 = "y' = " if it['task'] == 'diff' else '= '
    tail0 = ' + C' if it['task'] == 'int' else ''
    if it['task'] == 'diff':
        html = md("y' = " + ans_tex(it), 'ans')
    if narrow and len(it['answer']) >= 3:
        html = md(_two_lines(lhs0, list(it['answer']), tail0), 'ans')
    doc = doctor_terms(it)
    if doc is None:
        return html
    if it['task'] == 'diff':             # keep the authored form of each term; only its sign changes
        doc = [a if _sp.simplify(d - _P(a)) == 0 else '-1*(%s)' % a for d, a in zip(doc, it['answer'])]
    body = _ts([str(t) for t in doc])
    if narrow and len(doc) >= 2:
        return (md(_two_lines("y' = " if it['task'] == 'diff' else '= ', [str(t) for t in doc], ' + C' if it['task'] == 'int' else '', at=1), 'ans')
                + p('✍️ هذا بإشارة دكتورك في ' + mi(r'\coth^{-1}') + ' (اكتبه كذا). رياضيًا الإشارة بالعكس:', 'small doctor')
                + md(_two_lines(lhs0, list(it['answer']), tail0, at=1), 'truesign'))
    lhs = "y' = " if it['task'] == 'diff' else '= '
    tail = ' + C' if it['task'] == 'int' else ''
    return (md(lhs + body + tail, 'ans') + p('✍️ هذا بإشارة دكتورك في ' + mi(r'\coth^{-1}') + ' (اكتبه كذا في الكويز). '
                                             'رياضيًا الإشارة بالعكس:', 'small doctor') + html.replace("md ans", "md truesign"))


def final(it, where):
    """Check the answer; print it in the answer box unless the last step row already shows it."""
    html = answer_box(it, where)
    if it['id'] in FINAL_ROW:
        FINAL_ROW.discard(it['id'])
        if doctor_terms(it) is None:     # with coth⁻¹ the box stays: it shows the doctor's sign first
            return ''
    return html


def short_steps(it, rows, label, lead=True):
    """The shortcut applied to the same example, as explained numbered steps in the same table as the basic
    method: the rule, the numbers read from the question, the substitution, the simplification, the answer.
    rows: (why, latex, claims); every row needs at least one claim:
      ('=ANS', expr)            expr is the item's verified answer (antiderivative up to a constant, derivative, value)
      ('=FORMULA', f, F, opts)  a general rule with parameters, checked like the formula sheet (formula(), F' = f)
      ('=RULE', builder)        a rule with arbitrary functions: builder() must simplify to zero
      (lhs, rhs[, branch])      an exact equality
    """
    cells = []
    for k, (why, latex, claims) in enumerate(rows, 1):
        tag = '%s short %d' % (label, k)
        if not claims:
            raise BuildError('shortcut step %s has no check' % tag)
        plain = []
        for c in claims:
            if c[0] == '=ANS':
                if it['task'] == 'diff':
                    same_derivative([c[1]], it, tag)
                elif it['task'] == 'defint':
                    same_defint([c[1]], it, tag)
                else:
                    same_antiderivative([c[1]], it, tag)
            elif c[0] == '=FORMULA':
                formula(c[1], c[2], label=tag, **(c[3] if len(c) > 3 else {}))
            elif c[0] == '=RULE':
                functional(c[1], tag)
            else:
                plain.append(c)
        cells.append((arith(latex, plain, tag), why, k == len(rows)))
    return ((p('<b>⚡ الطريقة السريعة:</b> نفس خطوات 🧱 فوق، مختصرة. استعملها لتتأكد من جوابك.', 'sslbl') if lead else '')
            + steps_table(cells, 'short'))


def alg(skill, title=None, rows=None, intro='', try_=None):
    """Algebra box: detailed the first time a skill is needed (with a one-line try-it whose answer is in the
    keys at the end), a link back to it afterwards."""
    anchor = 'alg-' + skill
    if skill in ALG_SEEN:
        return p('🧮 ' + ALG_SEEN[skill] + ' — ' + link(anchor, 'الشرح المفصّل في ص ' + pgref(anchor)), 'algref')
    if rows is None:            # the skill's box was dropped (the algebra now sits inside the solution tables)
        return ''
    ALG_SEEN[skill] = title
    if try_ is None:
        from guide_checks import TRY
        try_ = TRY.get(skill)
    body = (p(rich(intro)) if intro else '') + '<ol class="algsteps">' + ''.join(
        '<li>%s%s</li>' % (rich(text) + ' ' if text else '', mi(r'\displaystyle ' + arith(latex, claims, 'algebra ' + skill)) if latex else '')
        for latex, claims, text in rows) + '</ol>'
    if try_:
        text, ans, claims = try_
        TRY_KEYS.append((skill, title, arith(ans, claims, 'try ' + skill)))
        body += p('✏️ <b>جرّب:</b> ' + rich(text) + ' — ' + link('k-' + skill, 'الجواب ص ' + pgref('k-' + skill)), 'try')
    return box('alg', '🧮 جبر: ' + title, body, anchor=anchor)


def _lead(label, html):
    """Put a bold label at the start of the first paragraph of a box body."""
    m = re.match(r'\s*<p class="[^"]*">', html)
    if m:
        return html[:m.end()] + label + ' ' + html[m.end():]
    return p(label) + html


class Unit:
    def __init__(self, uid, title, section, pages, day):
        COUNTER[0] += 1
        day, pages = DAY_OF.get(uid, day), PAGES.get(uid, pages)
        self.uid, self.num, self.title, self.section, self.pages, self.day = uid, COUNTER[0], title, section, pages, day
        self.ref = 'الحالة %d' % self.num
        self.parts, self.drills, self.sols = [], [], []
        self.pending, self.ex_items = [], []
        self.gist_html = ''
        LESSON_OF_UID[uid] = section
        DAYS.setdefault(day, []).append((uid, self.num, title))
        NUM[uid] = self.num
        CASES.append((uid, self.num, title))

    def add(self, kind, label, inner):
        if kind == 'ex':                 # remember which question the example shows (one example is kept, see _one_example)
            self.ex_items.append(LAST_Q[0])
        if kind == 'short' and label.startswith('⚡'):
            self.sc_item = SC_ITEM[0]
        self.parts.append((kind, label, inner))

    def _one_example(self):
        """v7: one 🧱 example per case — the one the ⚡ quick way uses, else a past-exam one, else the first.
        The others are not printed, and their question no longer counts as used."""
        exs = [k for k, (kind, _, _) in enumerate(self.parts) if kind == 'ex']
        if len(exs) < 2:
            return
        items = self.ex_items
        keep = 0
        if getattr(self, 'sc_item', None) and self.sc_item in [i[0] for i in items if i]:
            keep = [i[0] if i else None for i in items].index(self.sc_item)
        else:
            keep = next((k for k, i in enumerate(items) if i and ITEMS[i[0]]['kind'] == 'exam'), 0)
        from booklet_engine import USED
        for k, idx in enumerate(exs):
            if k != keep:
                self.parts[idx] = ('dropped', None, '')
                if items[k]:
                    item, where = items[k]
                    if where in USED.get(item, []):
                        USED[item].remove(where)
                        if not USED[item]:
                            del USED[item]
                    if ITEMS[item]['kind'] == 'exam':      # a past-exam example is not lost: it goes to the mastery checks
                        EXTRA.insert(0, (self.uid, item))

    def raw(self, html):
        self.parts.append(('raw', None, html))

    def prev(self, text):
        """One line in the type card: how this type differs from the one before it."""
        self.parts.append(('prev', None, text))

    def gist(self, see, first, rule):
        """The one-line summary at the end of the type (also a row of the lesson map)."""
        GIST[self.uid] = (self.num, self.title, see, first, rule)
        self.gist_html = p(rich('<b>الخلاصة:</b> إذا شفت ' + see + ' ← ' + first + ' ← ' + rule), 'gist')

    def drill(self, tag, item_id, level, hint, first=None, claims=(), mids=(), sol_rows=None, extra_lines=0):
        """v7: exercises are collected, and the case prints the best ones (see _pick_drills)."""
        self.pending.append((tag, item_id, level, hint, first, claims, mids, sol_rows, extra_lines))

    def _pick_drills(self):
        """Print cap(uid) exercises: past exams first, then Dr. Musa (also replacing ours), Dr. Tariq, ours; then in
        guided → partial → own order. The rest go to the mastery checks."""
        if getattr(self, 'picked', False):
            return
        self.picked = True
        cands = list(self.pending) + [(str(90 + k), i, lv, h, None, (), (), rows, 0)
                                      for k, (u, i, lv, h, rows) in enumerate(EXAM_ADD) if u == self.uid]
        musa_left = len(MUSA_DRILLS.get(self.uid, []))
        ranked = []
        for n, c in enumerate(cands):
            it = ITEMS[c[1]]
            if c[1] in BAN or c[1] in BLOCKED:
                continue
            r = RANK.get(it['kind'], 2)
            if (it['kind'] == 'generated' or (self.uid in MUSA_OVER_NOTES and it['kind'].startswith('notes'))) and musa_left:
                r, musa_left = 1, musa_left - 1
            ranked.append((r, n, c))
        ranked.sort()
        n_cap = cap(self.uid)
        chosen = sorted(ranked[:n_cap], key=lambda z: ('GPI'.index(z[2][2]), z[1]))
        for _, _, c in ranked[n_cap:]:
            if not self.uid.startswith('P-') and ITEMS[c[1]]['kind'] != 'generated':
                EXTRA.append((self.uid, c[1]))
        for k, (_, _, c) in enumerate(chosen, 1):
            self._drill_now(str(k), *c[1:])

    def _drill_now(self, tag, item_id, level, hint, first=None, claims=(), mids=(), sol_rows=None, extra_lines=0):
        from guide_sols import SOLS
        it = ITEMS[item_id]
        if (it['kind'] == 'generated' or (self.uid in MUSA_OVER_NOTES and it['kind'].startswith('notes'))) and MUSA_DRILLS.get(self.uid):   # Dr. Musa's question takes the place of one we wrote
            m = MUSA_DRILLS[self.uid].pop(0)
            item_id, it, hint, sol_rows, mids = m['item'], ITEMS[m['item']], m['hint'], m['sol_rows'], ()
            first, claims = (m.get('first'), m.get('claims', ())) if level == 'G' and m.get('first') else (None, ())
            if level == 'G' and not first:
                level = 'P'
        sol_rows = sol_rows if sol_rows is not None else SOLS.get(item_id, {}).get('rows')
        mids = list(mids) or SOLS.get(item_id, {}).get('mids', [])
        where = '%s drill %s' % (self.uid, tag)
        lvl = {'G': 'موجّه', 'P': 'ناقص الخطوات', 'I': 'لحالك'}[level]
        dtag = '%s-%s' % (self.uid, tag)
        DRILLS_N[self.uid] = DRILLS_N.get(self.uid, 0) + 1
        head = ('<div class="drill-head" id="d-%s"><b>%s تمرين %s</b> %s<span class="help">%s</span></div>'
                % (dtag, src_icon(it), tag, chip(lvl, 'lvl'), link('s-' + dtag, 'الحل ص ' + pgref('s-' + dtag), 'btn')))
        body = drill_question(it, where)
        first_tex = arith(first, claims, where + ' first') if first else None
        n = WRITE[level][self.section] + extra_lines
        if level == 'G':
            body += p('أول سطر جاهز. كمّل الحل:') + md(first_tex) + lines(n, 'write tight')
        elif level == 'P':
            body += p('اكتب أول سطر، ثم كمّل الحل:') + lines(n, 'write tight')
        else:
            body += lines(n, 'write tight')
        self.drills.append((prompt(it), '<div class="drill">' + head + body + '</div>'))
        # level 3: the full explained solution, on the page after the exercises
        sol = ''                         # the given first line of a guided exercise is printed with the exercise only
        cells = step_cells(it, sol_rows, where) if sol_rows else []
        if cells:
            sol += lean_steps(cells)
        mid_tex = []
        for m in mids:
            if it['task'] == 'diff':
                diff_step_ok(m, it, where + ' middle')
                mid_tex.append("y' = " + rawtex(m))
            else:
                step_ok(m, it, where + ' middle')
                mid_tex.append('I = ' + rawtex(m) + ('' if 'Integral' in m else ' + C'))
            sol += md(mid_tex[-1])
        answer = answer_box(it, where, narrow=True)
        if not (cells and cells[-1][2] and not mids) or doctor_terms(it) is not None:
            sol += answer
        self.sols.append('<div class="sol" id="s-%s"><div class="drill-head"><b>تمرين %s</b> %s %s</div>%s%s</div>'
                         % (dtag, tag, mi(r'\displaystyle ' + q_tex(it)), link('d-' + dtag, '↩', 'back btn'),
                            p(source_label(it), 'srcline'), sol))
        # levels 1 and 2 go to the help ladder at the end of the guide
        if cells:
            step = (cells[0][0], cells[0][1])
        elif mid_tex:
            step = (mid_tex[0], '')
        else:
            raise BuildError('exercise %s has no first step for the help ladder' % dtag)
        HELP.append(dict(dtag=dtag, num=self.num, tag=tag, hint=hint, step=step, guided=level == 'G'))

    def head_html(self):
        m = METHOD_OF.get(self.uid, 'B')
        needs = '، '.join(link(a, '📚 %s (ص ' % NEED_LABEL[a] + pgref(a) + ')') for a in NEEDS.get(self.uid, []) if a in NEED_LABEL)
        musa = MUSA_COUNT.get(self.uid)
        meta = ['الشجرة: ' + rich(TREE.get(self.uid, TREE_DEFAULT[m])), fire(self.uid)]
        if musa:
            meta.append('📗 في مذكرة د. موسى: %d' % musa)
        if needs:
            meta.append('تحتاج: ' + needs)
        if self.uid in OLD_NUM:
            pass                             # the old number is in the old → new table (how-to page)
        return ('<div class="unit-head %s" id="%s"><span class="num">%d</span><h3>%s</h3><span class="mtag">%s %s</span></div>'
                '<p class="unit-meta">%s</p>'
                % (METHODS[m][2], self.uid, self.num, self.title, METHODS[m][0], METHODS[m][1], ' · '.join(meta)))

    def body_parts(self):
        """The case page in one column: متى؟ ← ليش تشتغل؟ ← الخطوات ← 🧱 ← ⚡ ← قبل ما تسلّم (no boxes)."""
        from guide_checks import CHECKS
        by = lambda k: [inner for kind, _, inner in self.parts if kind == k]
        oks, traps = by('ok'), by('trap')
        out = []
        if by('sign'):
            out.append(part('🔎 متى؟', ''.join(by('sign')), 'p-when'))
        if by('idea'):
            out.append(part('ليش تشتغل؟', ''.join(by('idea')), 'p-why'))
        for kind, label, inner in self.parts:
            if kind in ('idea', 'sign', 'ok', 'trap', 'prev', 'dropped'):
                continue
            if kind == 'raw':
                out.append(inner)
                continue
            if kind == 'paper':             # before you hand in: the trap, what to write, a quick check
                check = _lead('<b>✔ تأكد:</b>', ''.join(oks)) if oks else ''
                if self.uid in CHECKS:
                    check += p('<b>✔ تأكد:</b> ' + rich(CHECKS[self.uid]))
                elif not oks:
                    raise BuildError('unit %s has no quick check' % self.uid)
                trap = ''.join('<div class="danger">' + t + '</div>' for t in traps)
                out.append(part('🔴 لا تنسى، قبل ما تسلّم', trap + _lead('<b>✍️ في ورقة الكويز:</b>', inner) + check, 'p-paper'))
                continue
            if kind == 'short':
                heading = label.replace('🧭 الطريقة', '🪜 الخطوات').replace('🧭 الخطوات', '🪜 الخطوات')
                out.append(part(heading, inner, 'p-quick' if label.startswith('⚡') else 'p-steps'))
            elif kind == 'ex':
                out.append(part(ex_label(label), inner, 'p-ex'))
            elif kind != 'note':
                out.append(part('📎 ' + label, inner, 'p-' + kind))
        return out

    def html(self):
        self._pick_drills()
        self._one_example()
        first_prompt = self.drills[0][0] if self.drills else ''
        drills = ('<h4 class="drills-title">تمارين %s</h4>' % self.ref
                  + (en(first_prompt) if first_prompt else '')
                  + ''.join(html.replace('<div class="q">', '<div class="q">' + en(pr), 1) if pr != first_prompt else html
                            for pr, html in self.drills)
                  + '<div class="confidence"><b>ثقتك بهذي الحالة؟</b> <span>☐ ✓ أحلها لحالي</span>'
                    '<span>☐ ؟ أحتاج المثال</span><span>☐ ✗ ارجع لها بكرة</span></div>')
        if self.sols:                    # solutions are printed together at the end of the method (no page break per case)
            SOLS_BY_METHOD.setdefault(METHOD_OF.get(self.uid, 'B'), []).append(
                '<div class="solcase"><h4>%s: %s %s</h4>%s</div>' % (self.ref, self.title, link(self.uid, '↩'), ''.join(self.sols)))
        return ('<article class="unit">' + self.head_html() + ''.join(self.body_parts()) + self.gist_html
                + drills + '</article>')


def sols_section(m):
    """«✅ حلول تمارين الطريقة»: every solution of the method's cases, one after the other."""
    blocks = SOLS_BY_METHOD.get(m, [])
    if not blocks:
        return ''
    return ('<section class="sols" id="sols-%s"><h3>✅ حلول تمارين %s</h3>' % (m, mname(m))
            + p('حاولت؟ قارن حلك سطر سطر. الشرح الكامل في 🧱 حالته. جوابك شكله غير؟ شوف '
                + link('differs', 'جوابك يختلف عن المفتاح؟') + '.', 'small') + ''.join(blocks) + '</section>')


def tricks(items, label='trick'):
    """🔑 lines: a small rule that stops a typical mistake, each with numbers. An item is a text, or
    (text, claims) when its math must be checked."""
    out = ''
    for k, item in enumerate(items, 1):
        text, claims = (item, []) if isinstance(item, str) else item
        if claims:
            arith('', claims, '%s trick %d' % (label, k))
        out += '<div class="trick"><b>🔑 تريك:</b> ' + rich(text) + '</div>'
    return out


def method(steps_, memo=None, tricks_=(), label='method'):
    """A fixed list of steps in words (the way to solve a type), with an optional memory line and 🔑 lines."""
    def li(t):
        t = rich(t)
        if '<b>هنا:</b>' in t:              # v7: the script words stay one line; the detail of this case goes under them
            head, detail = t.split('<b>هنا:</b>', 1)
            return '<li>%s<span class="here">%s</span></li>' % (head, detail)
        return '<li>%s</li>' % t
    for t in tricks_[1:]:                   # v7: one trick per case (the others are still checked)
        if not isinstance(t, str):
            arith('', t[1], label + ' extra trick')
    return ('<ol class="method">' + ''.join(li(t) for t in steps_) + '</ol>'
            + ('<div class="memo-inline"><b>كيف أتذكّره:</b> ' + rich(memo) + '</div>' if memo else '')
            + tricks(tricks_[:1], label))


def shortcut(it, label, saves, origin, steps_, rows, memo, never, tries, paper=None, origin_html='',
             on='على نفس مثال 🧱:', ask='بالطريقة السريعة', example_html='', after_rows=''):
    """The quick way of a type, always in the same seven parts:
    what it saves, where it comes from (tied to the 🧱 solution), the steps in words, the same example
    (short_steps rows, checked), the memory line, when it does not work, and a few half-minute tries whose answers
    sit at the end of the box. tries: (question latex, answer latex, claims); every answer is checked."""
    SC_ITEM[0] = it['id']
    part = lambda title, body: '<div class="sc-part"><b>%s</b> %s</div>' % (title, body)
    html = part('وش يوفر لك:', rich(saves))
    html += '<div class="sc-part"><b>الخطوات:</b></div><ol class="method">' + ''.join('<li>%s</li>' % rich(t) for t in steps_) + '</ol>'
    html += '<div class="sc-part"><b>%s</b></div>' % on + example_html + short_steps(it, rows, label, lead=False) + after_rows
    html += '<div class="memo-inline"><b>🧠 جملة الحفظ:</b> ' + rich(memo) + '</div>'
    html += '<div class="sc-part never"><b>⚠️ متى ما ينفع:</b> ' + '، و'.join(rich(t).rstrip('.') for t in never) + '.</div>'
    for k, (q, a, claims) in enumerate(tries, 1):   # v7: still checked, no longer printed (one explanation per case)
        arith(a, claims, '%s try %d' % (label, k))
    return html


def contrast(rows):
    """'What it is confused with' table: (question latex, method, why); three rows at most (v7)."""
    rows = rows[:3]
    return table(['السؤال', 'الطريقة', 'ليش؟'], [[mi(r'\displaystyle ' + q), rich(m), rich(w)] for q, m, w in rows], 'contrast')

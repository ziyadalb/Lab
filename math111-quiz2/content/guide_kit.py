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
WRITE = {'G': {'4.2': 3, '5.1': 3, '5.2': 3}, 'P': {'4.2': 4, '5.1': 4, '5.2': 4}, 'I': {'4.2': 5, '5.1': 7, '5.2': 6}}
ASK = {'diff': 'المطلوب: المشتقة', 'int': 'المطلوب: احسب التكامل', 'defint': 'المطلوب: احسب التكامل المحدد'}
# the date shown for each study day (days 1 and 2 are already done)
DAY_NAME = {1: '20 أكتوبر ✓', 2: '21–22 أكتوبر ✓', 3: 'الجمعة 23', 4: 'السبت 24', 5: 'الأحد 25', 6: 'الاثنين 26', 7: 'إذا بقي وقت'}
# lesson colour class of each section (unit header band and the lesson map)
LESSON_CLS = {'4.2': 'l42', '5.1': 'l51', '5.2': 'l52'}
MAPS_READY = {'4.2', '5.1', '5.2'}   # lessons whose map page is built (every type of the lesson has its one-line summary)


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
    return '<div class="q">' + chip(source_label(it), 'src') + en(prompt(it)) + md(q_tex(it)) + '</div>'


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
                latex = '= ' + body + ('' if 'Integral' in expr else ' + C')
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


def answer_box(it, where):
    """Check the answer and print it in the green box (derivatives start with y' =)."""
    html = _final(it, where)
    return md("y' = " + ans_tex(it), 'ans') if it['task'] == 'diff' else html


def final(it, where):
    """Check the answer; print it in the answer box unless the last step row already shows it."""
    html = answer_box(it, where)
    if it['id'] in FINAL_ROW:
        FINAL_ROW.discard(it['id'])
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
        self.ref = 'النوع %d' % self.num
        self.parts, self.drills, self.sols = [], [], []
        self.gist_html = ''
        LESSON_OF_UID[uid] = section
        DAYS.setdefault(day, []).append((uid, self.num, title))

    def add(self, kind, label, inner):
        self.parts.append((kind, label, inner))

    def raw(self, html):
        self.parts.append(('raw', None, html))

    def prev(self, text):
        """One line in the type card: how this type differs from the one before it."""
        self.parts.append(('prev', None, text))

    def gist(self, see, first, rule):
        """The one-line summary at the end of the type (also a row of the lesson map)."""
        GIST[self.uid] = (self.num, self.title, see, first, rule)
        self.gist_html = box('gist', '📌 الخلاصة', '<div class="gist-row"><span>' + rich('<b>إذا شفت:</b> ' + see) + '</span><span>'
                             + rich('<b>أول خطوة:</b> ' + first) + '</span><span>' + rich('<b>ثم:</b> ' + rule) + '</span></div>')

    def drill(self, tag, item_id, level, hint, first=None, claims=(), mids=(), sol_rows=None, extra_lines=0):
        from guide_sols import SOLS
        it = ITEMS[item_id]
        sol_rows = sol_rows if sol_rows is not None else SOLS.get(item_id, {}).get('rows')
        mids = list(mids) or SOLS.get(item_id, {}).get('mids', [])
        where = '%s drill %s' % (self.uid, tag)
        lvl = {'G': 'موجّه', 'P': 'ناقص الخطوات', 'I': 'لحالك'}[level]
        dtag = '%s-%s' % (self.uid, tag)
        DRILLS_N[self.uid] = DRILLS_N.get(self.uid, 0) + 1
        head = ('<div class="drill-head" id="d-%s"><b>تمرين %s</b> %s<span class="help">%s</span></div>'
                % (dtag, tag, chip(lvl, 'lvl'), link('s-' + dtag, '✅ الحل ص ' + pgref('s-' + dtag), 'btn')))
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
        sol = ''
        if first_tex:
            sol += md(first_tex)
        cells = step_cells(it, sol_rows, where) if sol_rows else []
        if cells:
            sol += steps_table(cells)
        mid_tex = []
        for m in mids:
            if it['task'] == 'diff':
                diff_step_ok(m, it, where + ' middle')
                mid_tex.append("y' = " + rawtex(m))
            else:
                step_ok(m, it, where + ' middle')
                mid_tex.append('= ' + rawtex(m) + ('' if 'Integral' in m else ' + C'))
            sol += md(mid_tex[-1])
        answer = answer_box(it, where)
        if not (cells and cells[-1][2] and not mids):
            sol += answer
        self.sols.append('<div class="sol" id="s-%s"><div class="drill-head"><b>تمرين %s</b> %s %s</div>%s%s</div>'
                         % (dtag, tag, mi(r'\displaystyle ' + q_tex(it)), link('d-' + dtag, '↩ ارجع للتمرين', 'back btn'),
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
        needs = '، '.join(link(a, '📚 %s (ص ' % NEED_LABEL.get(a, a) + pgref(a) + ')') for a in NEEDS.get(self.uid, []))
        meta = ' · '.join(x for x in ['درس ' + self.section, DAY_NAME.get(self.day, ''), '⏱️ %d دقيقة' % unit_minutes(self.uid),
                                      ('تحتاج: ' + needs) if needs else ''] if x)
        if self.section in MAPS_READY:
            meta += ' · ' + link('map-' + self.section, '🗺️ خريطة الدرس')
        return ('<div class="unit-head %s" id="%s"><span class="num">%d</span><h3>%s</h3></div><p class="unit-meta">%s</p>'
                % (LESSON_CLS.get(self.section, ''), self.uid, self.num, self.title, meta))

    def html(self):
        from guide_checks import CHECKS
        head = self.head_html()
        idea = [inner for kind, _, inner in self.parts if kind == 'idea']
        oks = [inner for kind, _, inner in self.parts if kind == 'ok']
        traps = [inner for kind, _, inner in self.parts if kind == 'trap']
        prev = [inner for kind, _, inner in self.parts if kind == 'prev']
        out = []
        for kind, label, inner in self.parts:
            if kind in ('idea', 'ok', 'trap', 'prev'):
                continue
            if kind == 'raw':
                out.append(inner)
                continue
            if kind == 'sign':              # one card: why it works, how to recognise it, how it differs from the type before
                inner = ((_lead('<b>💡 الفكرة:</b>', idea[0]) if idea else '') + _lead('<b>🔎 العلامة:</b>', inner)
                         + ''.join(p('<b>🔗 الفرق عن النوع اللي قبله:</b> ' + rich(t), 'prevline') for t in prev))
                kind, label = 'idea', '🎯 وش هذا النوع'
            if kind == 'paper':             # before you hand in: the trap, what to write, a quick check
                check = _lead('<b>✔ تأكد:</b>', ''.join(oks)) if oks else ''
                if self.uid in CHECKS:
                    check += p('<b>✔ تأكد:</b> ' + rich(CHECKS[self.uid]))
                elif not oks:
                    raise BuildError('unit %s has no quick check' % self.uid)
                trap = ''.join(_lead('<b>⚠️ انتبه:</b>', t) for t in traps)
                inner = trap + _lead('<b>✍️ في ورقة الكويز:</b>', inner) + check
                label = '✔ قبل ما تسلّم'
            out.append(box(kind, label, inner))
        first_prompt = self.drills[0][0] if self.drills else ''
        drills = ('<h4 class="drills-title">تمارين %s</h4>' % self.ref + (en(first_prompt) if first_prompt else '')
                  + ''.join(html.replace('<div class="q">', '<div class="q">' + en(pr), 1) if pr != first_prompt else html
                            for pr, html in self.drills))
        src = p('المصدر: ' + (self.pages if self.pages.startswith('من') else 'مذكرة د. طارق، ' + self.pages), 'srcline')
        sols = ('<section class="sols"><h4>حلول تمارين %s: %s</h4>' % (self.ref, self.title)
                + p('حاولت؟ قارن حلك سطرًا سطرًا. إذا اختلف جوابك، سجّل الغلطة في سجل الأخطاء آخر المذكرة.', 'small')
                + ''.join(self.sols) + '</section>')
        return '<article class="unit">' + head + ''.join(out) + self.gist_html + src + drills + sols + '</article>'


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
    return ('<ol class="method">' + ''.join('<li>%s</li>' % rich(t) for t in steps_) + '</ol>'
            + ('<div class="memo-inline"><b>كيف أتذكّره:</b> ' + rich(memo) + '</div>' if memo else '')
            + tricks(tricks_, label))


def shortcut(it, label, saves, origin, steps_, rows, memo, never, tries, paper=None, origin_html='',
             on='على نفس مثال 🧱:', ask='بالطريقة السريعة', example_html='', after_rows=''):
    """The quick way of a type, always in the same seven parts:
    what it saves, where it comes from (tied to the 🧱 solution), the steps in words, the same example
    (short_steps rows, checked), the memory line, when it does not work, and a few half-minute tries whose answers
    sit at the end of the box. tries: (question latex, answer latex, claims); every answer is checked."""
    part = lambda title, body: '<div class="sc-part"><b>%s</b> %s</div>' % (title, body)
    html = part('وش يوفر لك:', rich(saves)) + part('من وين جا:', rich(origin)) + origin_html
    html += '<div class="sc-part"><b>الخطوات:</b></div><ol class="method">' + ''.join('<li>%s</li>' % rich(t) for t in steps_) + '</ol>'
    html += '<div class="sc-part"><b>%s</b></div>' % on + example_html + short_steps(it, rows, label, lead=False) + after_rows
    html += '<div class="memo-inline"><b>🧠 جملة الحفظ:</b> ' + rich(memo) + '</div>'
    html += '<div class="sc-part never"><b>⚠️ متى ما ينفع:</b></div>' + ul([rich(t) for t in never])
    if paper:
        html += part('✍️ في الكويز:', rich(paper))
    qs, ans = [], []
    for k, (q, a, claims) in enumerate(tries, 1):
        qs.append('<li>%s</li>' % mi(r'\displaystyle ' + q))
        ans.append(mi(r'\displaystyle ' + arith(a, claims, '%s try %d' % (label, k))))
    html += ('<div class="tries"><b>🏃 جرّب بسرعة</b> (نص دقيقة لكل واحد، %s):<ol>' % rich(ask) + ''.join(qs) + '</ol>'
             + '<div class="tries-ans"><b>الأجوبة:</b><ol>' + ''.join('<li>%s</li>' % a for a in ans) + '</ol></div></div>')
    return html


def contrast(rows):
    """'What it is confused with' table: (question latex, method, why)."""
    return table(['السؤال', 'الطريقة', 'ليش؟'], [[mi(r'\displaystyle ' + q), rich(m), rich(w)] for q, m, w in rows], 'contrast')

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
DRILLS_N = {}      # uid -> number of exercises (for the time plan of the day)
ALG_SEEN = {}      # algebra skill -> title (first, detailed explanation carries the anchor)
HELP = []          # one entry per exercise: the two lighter help levels, printed at the end of the guide
TRY_KEYS = []      # algebra try-its: (skill, title, answer latex)
FINAL_ROW = set()  # items whose last step row already shows the final answer
COUNTER = [0]

# study day of every unit, balanced so that every day stays within two to three hours
DAY_OF = {'U-D1': 1, 'U-D2': 1, 'U-I1': 1, 'U-I2': 1, 'U-I3': 1,
          'U-I4': 2, 'U-I5': 2, 'U-I6': 2, 'U-I7': 2, 'U-I8': 2, 'U-I9': 2,
          'U-P1': 3, 'U-P2': 3, 'U-P3': 3, 'U-P4': 3, 'U-P5': 3,
          'U-P6': 4, 'U-P7': 4, 'U-P8': 4, 'U-P9': 4, 'U-P10': 4,
          'U-T1': 5, 'U-T2': 5, 'U-T3': 5, 'U-T4': 5, 'U-T5': 5,
          'U-T6': 6, 'U-T7': 6, 'U-T8': 6}
# where to read in Dr. Tariq's notes: the explanation pages, then the page of the exercises used here
PAGES = {'U-D2': 'ص59، تمارين ص62', 'U-I1': 'ص59–60، تمارين ص62', 'U-I2': 'ص60، تمارين ص62', 'U-I3': 'ص60–61، تمارين ص62',
         'U-I4': 'ص61، تمارين ص62', 'U-I5': 'ص61', 'U-I6': 'تمارين ص62', 'U-I7': 'تمارين ص62', 'U-I8': 'ص61، تمارين ص62',
         'U-I9': 'ص61، تمارين ص62', 'U-P1': 'ص63، تمارين ص66', 'U-P2': 'ص63، تمارين ص66', 'U-P3': 'ص64، تمارين ص66',
         'U-P4': 'ص64، تمارين ص66', 'U-P5': 'من الاختبارات السابقة', 'U-P6': 'ص64–65، تمارين ص66', 'U-P7': 'ص65، تمارين ص66',
         'U-P8': 'ص65، تمارين ص66', 'U-P9': 'تمارين ص66', 'U-P10': 'تمارين ص66', 'U-T1': 'ص67', 'U-T2': 'ص68–69، تمارين ص76',
         'U-T3': 'ص67–70، تمارين ص76', 'U-T4': 'ص70–71', 'U-T5': 'ص71–72، تمارين ص76', 'U-T6': 'ص70–73، تمارين ص76',
         'U-T7': 'ص73، تمارين ص76', 'U-T8': 'ص74–75، تمارين ص76'}
# writing space in lines of 7.5 mm: a start needs a few lines, a full solution more (5.1 solutions are longest)
WRITE = {'G': {'4.2': 3, '5.1': 3, '5.2': 3}, 'P': {'4.2': 4, '5.1': 4, '5.2': 4}, 'I': {'4.2': 5, '5.1': 7, '5.2': 6}}
ASK = {'diff': 'المطلوب: المشتقة', 'int': 'المطلوب: احسب التكامل', 'defint': 'المطلوب: احسب التكامل المحدد'}


def rich(text):
    """Arabic text with $...$ math islands."""
    parts = text.split('$')
    return ''.join(mi(seg) if i % 2 else seg for i, seg in enumerate(parts))


def pgref(anchor):
    return '<span class="pgref" data-target="%s"></span>' % anchor


def question(it, where, allow_held=False):
    use(it['id'], where, allow_held=allow_held)
    return ('<div class="q">' + chip(source_label(it), 'src') + chip(ASK[it['task']], 'ask') + en(prompt(it))
            + md(q_tex(it)) + '</div>')


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


def short_steps(it, rows, label):
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
    return p('<b>⚡ بالاختصار، خطوة خطوة:</b>', 'sslbl') + steps_table(cells, 'short')


def alg(skill, title=None, rows=None, intro='', try_=None):
    """Algebra box: detailed the first time a skill is needed (with a one-line try-it whose answer is in the
    keys at the end), a link back to it afterwards."""
    anchor = 'alg-' + skill
    if skill in ALG_SEEN:
        return p('🧮 ' + ALG_SEEN[skill] + ' — ' + link(anchor, 'الشرح المفصّل في ص ' + pgref(anchor)), 'algref')
    if rows is None:
        raise BuildError('first use of algebra skill %s needs its explanation' % skill)
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
        self.parts, self.drills, self.sols = [], [], []
        DAYS.setdefault(day, []).append((uid, self.num, title))

    def add(self, kind, label, inner):
        self.parts.append((kind, label, inner))

    def raw(self, html):
        self.parts.append(('raw', None, html))

    def drill(self, tag, item_id, level, hint, first=None, claims=(), mids=(), sol_rows=None, extra_lines=0):
        from guide_sols import SOLS
        it = ITEMS[item_id]
        sol_rows = sol_rows if sol_rows is not None else SOLS.get(item_id, {}).get('rows')
        mids = list(mids) or SOLS.get(item_id, {}).get('mids', [])
        where = '%s drill %s' % (self.uid, tag)
        lvl = {'G': 'موجّه', 'P': 'ناقص الخطوات', 'I': 'لحالك'}[level]
        dtag = '%s-%s' % (self.uid, tag)
        DRILLS_N[self.uid] = DRILLS_N.get(self.uid, 0) + 1
        help_links = ' · '.join([link('h-' + dtag, '💡 تلميح ص ' + pgref('h-' + dtag)),
                                 link('f-' + dtag, '✍️ أول خطوة ص ' + pgref('f-' + dtag)),
                                 link('s-' + dtag, '✅ الحل ص ' + pgref('s-' + dtag))])
        head = ('<div class="drill-head" id="d-%s"><b>تمرين %s</b> %s<span class="help">%s</span></div>'
                % (dtag, tag, chip(lvl, 'lvl'), help_links))
        body = question(it, where)
        first_tex = arith(first, claims, where + ' first') if first else None
        n = WRITE[level][self.section] + extra_lines
        if level == 'G':
            body += p('البداية جاهزة؛ أكمل:') + md(first_tex) + lines(n, 'write tight')
        elif level == 'P':
            body += p('اكتب سطر المعطيات ثم الجواب:') + lines(n, 'write tight')
        else:
            body += lines(n, 'write tight')
        self.drills.append('<div class="drill">' + head + body + '</div>')
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
        self.sols.append('<div class="sol" id="s-%s"><div class="drill-head"><b>تمرين %s</b> %s %s</div>%s</div>'
                         % (dtag, tag, mi(r'\displaystyle ' + q_tex(it)), link('d-' + dtag, 'ارجع للتمرين', 'back'), sol))
        # levels 1 and 2 go to the help ladder at the end of the guide
        if cells:
            step = (cells[0][0], cells[0][1])
        elif mid_tex:
            step = (mid_tex[0], '')
        else:
            raise BuildError('exercise %s has no first step for the help ladder' % dtag)
        HELP.append(dict(dtag=dtag, num=self.num, tag=tag, hint=hint, step=step, guided=level == 'G'))

    def html(self):
        from guide_checks import CHECKS
        head = ('<div class="unit-head" id="%s"><span class="num">%d</span><h3>%s</h3>%s%s%s</div>'
                % (self.uid, self.num, self.title, chip(self.section, 'sec'),
                   chip(self.pages if self.pages.startswith('من') else 'مذكرة د. طارق: ' + self.pages, 'pg'),
                   chip('اليوم %d' % self.day, 'day')))
        idea = [inner for kind, _, inner in self.parts if kind == 'idea']
        oks = [inner for kind, _, inner in self.parts if kind == 'ok']
        out = []
        for kind, label, inner in self.parts:
            if kind in ('idea', 'ok'):
                continue
            if kind == 'raw':
                out.append(inner)
                continue
            if kind == 'sign' and idea:     # one card: why it works, then how to recognise it
                inner = _lead('<b>💡 الفكرة:</b>', idea[0]) + _lead('<b>🔎 العلامة:</b>', inner)
                label = 'الفكرة والعلامة'
            if kind == 'paper':             # what to write, then a quick check of the answer
                check = _lead('<b>✔ تأكد:</b>', ''.join(oks)) if oks else ''
                if self.uid in CHECKS:
                    check += p('<b>✔ تأكد:</b> ' + rich(CHECKS[self.uid]))
                elif not oks:
                    raise BuildError('unit %s has no quick check' % self.uid)
                inner += check
                label = '✍️ في ورقة الكويز و ✔ تأكد'
            out.append(box(kind, label, inner))
        drills = '<h4 class="drills-title">تمارين النوع %d</h4>' % self.num + ''.join(self.drills)
        sols = ('<section class="sols"><h4>حلول تمارين النوع %d: %s</h4>' % (self.num, self.title)
                + p('حاولت؟ قارن حلك سطرًا سطرًا. إذا اختلف جوابك، سجّل الغلطة في سجل الأخطاء آخر المذكرة.', 'small')
                + ''.join(self.sols) + '</section>')
        return '<article class="unit">' + head + ''.join(out) + drills + sols + '</article>'


def contrast(rows):
    """'What it is confused with' table: (question latex, method, why)."""
    return table(['السؤال', 'الطريقة', 'ليش؟'], [[mi(r'\displaystyle ' + q), rich(m), rich(w)] for q, m, w in rows], 'contrast')

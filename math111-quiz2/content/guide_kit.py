"""Building blocks of the full guide: one unit per question type.

A unit is: idea -> sign (and what it is confused with) -> reminder -> shortcut -> one real example solved
by the shortcut and, line by line, by the basic method -> algebra boxes where an algebra move is
needed -> 10-second check -> trap -> what to write on the quiz paper -> three exercises (guided,
partial, on your own) with an upside-down hint -> the solutions of those exercises on the next page.

Every math line goes through a check (tools/booklet_engine.py); a failed check stops the build.
"""
from booklet import final, prompt, source_label
from booklet_engine import (ITEMS, BuildError, arith, diff_step_ok, parts_rows, q_tex, same_derivative, step_ok,
                            sub_row, use)
from html_kit import box, chip, en, lines, link, md, mi, p, table, ul
from mathlib import rawtex, tex

DAYS = {}          # day number -> list of (uid, number, title)
ALG_SEEN = {}      # algebra skill -> title (first, detailed explanation carries the anchor)
COUNTER = [0]


def rich(text):
    """Arabic text with $...$ math islands."""
    parts = text.split('$')
    return ''.join(mi(seg) if i % 2 else seg for i, seg in enumerate(parts))


def pgref(anchor):
    return '<span class="pgref" data-target="%s"></span>' % anchor


def question(it, where, allow_held=False):
    use(it['id'], where, allow_held=allow_held)
    return '<div class="q">' + chip(source_label(it), 'src') + en(prompt(it)) + md(q_tex(it)) + '</div>'


def steps(it, rows, label):
    """Basic method, one line per step, each with its reason. Row kinds:
    ('parts', u, dv, du, v, why[, branch])   integration by parts: du and v are checked
    ('sub', u, du, why[, var[, branch]])      substitution line: du is checked (on a branch x = phi(t) if given)
    ('line', expr, why)                      a line equal to the integral (may contain Integral) or derivative
    ('tex', latex, claims, why)              typed line; every claim is checked exactly
    """
    out = []
    for k, row in enumerate(rows):
        kind, tag = row[0], '%s step %d' % (label, k + 1)
        if kind == 'parts':
            _, u, dv, du, v, why = row[:6]
            latex = parts_rows(u, dv, du, v, tag, branch=row[6] if len(row) > 6 else None)
            latex = r'\begin{array}{l}' + latex + r'\end{array}'
        elif kind == 'sub':
            _, u, du, why = row[:4]
            latex = sub_row(u, du, tag, var=row[4] if len(row) > 4 else 'u', branch=row[5] if len(row) > 5 else None)
        elif kind == 'line':
            _, expr, why = row
            if it['task'] == 'diff':
                diff_step_ok(expr, it, tag)
                latex = "y' = " + rawtex(expr)
            else:
                step_ok(expr, it, tag)
                latex = '= ' + rawtex(expr) + ('' if 'Integral' in expr else ' + C')
        elif kind == 'tex':
            _, latex, claims, why = row
            latex = arith(latex, claims, tag)
        else:
            raise BuildError('unknown step kind ' + kind)
        out.append([mi(r'\displaystyle ' + latex), rich(why)])
    return table(['الخطوة', 'ليش؟'], out, 'steps')


def alg(skill, title=None, rows=None, intro=''):
    """Algebra box: detailed the first time a skill is needed, a link back to it afterwards."""
    anchor = 'alg-' + skill
    if skill in ALG_SEEN:
        return p('🧮 ' + ALG_SEEN[skill] + ' — ' + link(anchor, 'الشرح المفصّل في ص ' + pgref(anchor)), 'algref')
    if rows is None:
        raise BuildError('first use of algebra skill %s needs its explanation' % skill)
    ALG_SEEN[skill] = title
    body = (p(rich(intro)) if intro else '') + '<ol class="algsteps">' + ''.join(
        '<li>%s%s</li>' % (rich(text) + ' ' if text else '', mi(r'\displaystyle ' + arith(latex, claims, 'algebra ' + skill)) if latex else '')
        for latex, claims, text in rows) + '</ol>'
    return box('alg', '🧮 جبر: ' + title, body, anchor=anchor)


class Unit:
    def __init__(self, uid, title, section, pages, day):
        COUNTER[0] += 1
        self.uid, self.num, self.title, self.section, self.pages, self.day = uid, COUNTER[0], title, section, pages, day
        self.parts, self.drills, self.sols = [], [], []
        DAYS.setdefault(day, []).append((uid, self.num, title))

    def add(self, kind, label, inner):
        self.parts.append(box(kind, label, inner))

    def raw(self, html):
        self.parts.append(html)

    def drill(self, tag, item_id, level, hint, first=None, claims=(), mids=(), sol_rows=None, extra_lines=0):
        from guide_sols import SOLS
        it = ITEMS[item_id]
        sol_rows = sol_rows if sol_rows is not None else SOLS.get(item_id, {}).get('rows')
        mids = list(mids) or SOLS.get(item_id, {}).get('mids', [])
        where = '%s drill %s' % (self.uid, tag)
        lvl = {'G': 'موجّه', 'P': 'ناقص الخطوات', 'I': 'لحالك'}[level]
        dtag = '%s-%s' % (self.uid, tag)
        head = ('<div class="drill-head" id="d-%s"><b>تمرين %s</b> %s %s</div>'
                % (dtag, tag, chip(lvl, 'lvl'), link('s-' + dtag, 'الحل في ص ' + pgref('s-' + dtag), 'help')))
        body = question(it, where)
        first_tex = arith(first, claims, where + ' first') if first else None
        if level == 'G':
            body += p('البداية جاهزة؛ أكمل:') + md(first_tex) + lines(2 + extra_lines, 'write tight')
        elif level == 'P':
            body += p('اكتب سطر المعطيات ثم الجواب:') + lines(2 + extra_lines, 'write tight')
        else:
            body += lines(4 + extra_lines, 'write tight')
        body += '<div class="hint"><span class="flip">💡 تلميح: %s</span></div>' % rich(hint)
        self.drills.append('<div class="drill">' + head + body + '</div>')
        sol = md(q_tex(it))
        if first_tex:
            sol += md(first_tex)
        if sol_rows:
            sol += steps(it, sol_rows, where)
        for m in mids:
            if it['task'] == 'diff':
                diff_step_ok(m, it, where + ' middle')
                sol += md("y' = " + rawtex(m))
            else:
                step_ok(m, it, where + ' middle')
                sol += md('= ' + rawtex(m) + ('' if 'Integral' in m else ' + C'))
        sol += final(it, where)
        self.sols.append('<div class="sol" id="s-%s"><div class="drill-head"><b>تمرين %s</b> %s</div>%s</div>'
                         % (dtag, tag, link('d-' + dtag, 'ارجع للتمرين', 'back'), sol))

    def html(self):
        head = ('<div class="unit-head" id="%s"><span class="num">%d</span><h3>%s</h3>%s%s%s</div>'
                % (self.uid, self.num, self.title, chip(self.section, 'sec'), chip('المذكرة ' + self.pages, 'pg'),
                   chip('اليوم %d' % self.day, 'day')))
        drills = '<h4 class="drills-title">تمارين النوع %d</h4>' % self.num + ''.join(self.drills)
        sols = ('<section class="sols"><h4>حلول تمارين النوع %d: %s</h4>' % (self.num, self.title)
                + p('حاولت؟ قارن حلك سطرًا سطرًا. إذا اختلف جوابك، سجّل الغلطة في سجل الأخطاء آخر المذكرة.', 'small')
                + ''.join(self.sols) + '</section>')
        return '<article class="unit">' + head + ''.join(self.parts) + drills + sols + '</article>'


def contrast(rows):
    """'What it is confused with' table: (question latex, method, why)."""
    return table(['السؤال', 'الطريقة', 'ليش؟'], [[mi(q), rich(m), rich(w)] for q, m, w in rows], 'contrast')

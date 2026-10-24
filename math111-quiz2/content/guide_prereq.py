"""المذكرة الكاملة — «📚 قبل الدرس»: أساسيات التفاضل والتكامل والتبسيط من الفصول السابقة، قبل كل درس من دروس الكويز.

Three chapters, each printed just before the first type of its lesson (guide_end.BEFORE_UNIT):
  pre42  أ1 الأسس والجذور، أ2 الاشتقاق وقاعدة السلسلة، أ3 الدوال الزائدية (4.1)، أ4 التكامل والتعويض بـ u
  pre51  ب1 مشتقات تحتاجها التجزئة (ln و3.4)، ب2 تكاملات تحتاجها التجزئة، ب3 تبسيط 5.1
  pre52  ج1 المثلثات، ج2 تبسيط 5.2، ج3 التعويض في المثلثات
Every part is built like a question type: why you need it, the explanation step by step, the rules, worked
examples, the trap, a quick check, and exercises with writing space whose full solutions follow on the next page.
Every rule, example row, exercise answer and quick-check answer is checked while building.
"""
from booklet_engine import ITEMS, arith, formula
from guide_kit import DRILLS_N, HELP, WRITE, Unit, alg, method, pgref, rich, steps_table, tricks
from html_kit import box, chip, en, lines, link, md, mi, p, table, ul

LESSON = {'pre42': '4.2', 'pre51': '5.1', 'pre52': '5.2'}
TITLES = {'pre42': 'قبل درس 4.2: الأساسيات اللي تحتاجها', 'pre51': 'قبل درس 5.1: الأساسيات اللي تحتاجها',
          'pre52': 'قبل درس 5.2: الأساسيات اللي تحتاجها'}
PARTS = {}        # chapter -> [(uid, label, title)]
PART_MINUTES = 20
HTML = {}         # chapter -> finished html
KEYS = []         # (chapter, rows) answers of the quick checks, printed in the keys section
SHEET = {}        # formula-sheet tables


def _row(z, cond=None):
    return [mi(r'\displaystyle ' + z[0]), mi(r'\displaystyle ' + z[1])] + ([cond] if cond is not None else [])


def _cells(rows, label):
    """Rows (latex, claims, why): every claim checked; the last row is the answer."""
    out = []
    for k, (latex, claims, why) in enumerate(rows, 1):
        if not claims:
            raise ValueError('row without a check: %s %d' % (label, k))
        out.append((arith(latex, claims, '%s step %d' % (label, k)), why, k == len(rows)))
    return out


class PreUnit(Unit):
    """A prerequisite part: same boxes, exercises and solutions as a question type, with its own label (أ1…ج3)."""

    def __init__(self, uid, label, title, chapter, source):
        self.uid, self.num, self.ref, self.title = uid, label, label, title
        self.section, self.pages, self.chapter, self.day = LESSON[chapter], source, chapter, 0
        self.parts, self.drills, self.sols = [], [], []
        self.n_ex = 0
        PARTS.setdefault(chapter, []).append((uid, label, title))

    def head_html(self):
        return ('<div class="unit-head pre" id="%s"><span class="num">%s</span><h3>%s</h3>%s%s</div>'
                % (self.uid, self.num, self.title, chip('📚 قبل درس %s' % self.section, 'pq'), chip(self.source_text(), 'src')))

    def source_text(self):
        return self.pages

    def why(self, text, uses):
        links = '، '.join(link(uid, 'النوع %s' % n) for uid, n in uses)
        self.add('idea', '💡 ليش تحتاجه في درس %s' % self.section, p(rich(text)) + (p('تحتاجه في: ' + links, 'small') if uses else ''))

    def explain(self, steps):
        """Numbered explanation: (text, latex or None, claims)."""
        items = ''
        for k, (text, latex, claims) in enumerate(steps, 1):
            m = md(arith(latex, claims, '%s explain %d' % (self.uid, k))) if latex else ''
            items += '<li>%s%s</li>' % (rich(text), m)
        self.add('note', '📖 الشرح خطوة خطوة', '<ol class="explain">' + items + '</ol>')

    def example(self, title, q_latex, rows, check=None):
        self.n_ex += 1
        out = p('<b>مثال %d: %s</b>' % (self.n_ex, rich(title))) + md(q_latex) + steps_table(_cells(rows, '%s ex%d' % (self.uid, self.n_ex)))
        if check:
            out += p('<b>✔ تأكد:</b> ' + rich(check), 'small')
        self.add('ex', 'مثال محلول %d' % self.n_ex, out)

    def task(self, tag, level, ask, instruction, q_latex, rows, hint):
        """An exercise that is not a derivative or an integral (simplify, rewrite, evaluate)."""
        where = '%s drill %s' % (self.uid, tag)
        dtag = '%s-%s' % (self.uid, tag)
        lvl = {'G': 'موجّه', 'P': 'ناقص الخطوات', 'I': 'لحالك'}[level]
        DRILLS_N[self.uid] = DRILLS_N.get(self.uid, 0) + 1
        cells = _cells(rows, where)
        head = ('<div class="drill-head" id="d-%s"><b>تمرين %s</b> %s<span class="help">%s</span></div>'
                % (dtag, tag, chip(lvl, 'lvl'), link('s-' + dtag, '✅ الحل ص ' + pgref('s-' + dtag), 'btn')))
        body = '<div class="q">' + p(rich(instruction)) + md(q_latex) + '</div>'
        n = max(2, WRITE[level][self.section] - 1)
        if level == 'G':
            body += p('أول سطر جاهز. كمّل الحل:') + md(cells[0][0]) + lines(n, 'write tight')
        else:
            body += lines(n, 'write tight')
        self.drills.append(('', '<div class="drill">' + head + body + '</div>'))
        self.sols.append('<div class="sol" id="s-%s"><div class="drill-head"><b>تمرين %s</b> %s %s</div>%s%s</div>'
                         % (dtag, tag, mi(r'\displaystyle ' + q_latex), link('d-' + dtag, '↩ ارجع للتمرين', 'back btn'),
                            p('تدريب إضافي (من إعداد هذه المذكرة، جوابه متحقق)', 'srcline'), steps_table(cells)))
        step = cells[1] if level == 'G' and len(cells) > 1 else cells[0]
        HELP.append(dict(dtag=dtag, num=self.num, tag=tag, hint=hint, step=(step[0], step[1]), guided=level == 'G'))

    def html(self):
        out = [self.head_html()]
        for kind, label, inner in self.parts:
            out.append(inner if kind == 'raw' else box(kind, label, inner))
        first = next((pr for pr, _ in self.drills if pr), '')
        drills = ('<h4 class="drills-title">تمارين %s: اكتب الحل بنفسك</h4>' % self.ref + (en(first) if first else '')
                  + ''.join(html.replace('<div class="q">', '<div class="q">' + en(pr), 1) if pr and pr != first else html
                            for pr, html in self.drills))
        sols = ('<section class="sols"><h4>حلول تمارين %s: %s</h4>' % (self.ref, self.title)
                + p('حاولت؟ قارن حلك سطرًا سطرًا. إذا اختلف جوابك، سجّل الغلطة في سجل الأخطاء آخر المذكرة.', 'small')
                + ''.join(self.sols) + '</section>')
        return '<article class="unit prereq-unit">' + ''.join(out) + drills + sols + '</article>'


# ================================================================ before 4.2
def part_a1():
    U = PreUnit('P-A1', 'أ1', 'الأسس والجذور، والكتابة كمربع', 'pre42', 'جبر من قبل المقرر')
    U.why(r'في 4.2 لازم تكتب اللي تحت الجذر كمربع، مثل $16x^6=(4x^3)^2$. وقبل ما تكامل، تكتب الجذر والكسر على شكل أس.',
          [('U-I1', 3), ('U-I3', 5), ('U-I4', 6), ('U-I8', 10)])
    U.explain([
        (r'الأس يعني نضرب الشي في نفسه: $x^3$ يعني $x\cdot x\cdot x$. و $x^1=x$، و $x^0=1$.',
         r'x^{3}=x\cdot x\cdot x,\qquad x^{0}=1', [('x**3', 'x*x*x'), ('x**0', '1')]),
        (r'<b>ضرب</b> نفس الأساس: نجمع الأسس.', r'x^{2}\cdot x^{3}=x^{2+3}=x^{5}', [('x**2*x**3', 'x**5')]),
        (r'<b>قسمة</b> نفس الأساس: نطرح أس اللي تحت من أس اللي فوق.', r'\frac{x^{5}}{x^{2}}=x^{5-2}=x^{3}', [('x**5/x**2', 'x**3')]),
        (r'<b>قوة فوق قوة</b>: نضرب الأسس.', r'\left(x^{2}\right)^{3}=x^{2\cdot3}=x^{6}', [('(x**2)**3', 'x**6')]),
        (r'<b>الأس السالب</b> يعني مقلوب. ما يعني إن الجواب سالب.', r'x^{-2}=\frac{1}{x^{2}},\qquad \frac{1}{x^{3}}=x^{-3}',
         [('x**(-2)', '1/x**2'), ('1/x**3', 'x**(-3)')]),
        (r'<b>الجذر</b> أس كسر. الجذر التربيعي أس $\frac12$، والجذر التكعيبي أس $\frac13$.',
         r'\sqrt{x}=x^{1/2},\qquad \frac{1}{\sqrt{x}}=x^{-1/2},\qquad \sqrt[3]{x}=x^{1/3}',
         [('sqrt(x)', 'x**Rational(1,2)', 't'), ('1/sqrt(x)', 'x**Rational(-1,2)', 't')]),
        (r'<b>قوس فيه ضرب</b>: كل شي داخل القوس ياخذ الأس، حتى الرقم.', r'\left(3x^{2}\right)^{2}=3^{2}\cdot\left(x^{2}\right)^{2}=9x^{4}',
         [('(3*x**2)**2', '9*x**4')]),
        (r'<b>الكتابة كمربع</b> أهم مهارة في 4.2. نطلّع جذر الرقم، وناخذ نص الأس.',
         r'16x^{6}=\left(4x^{3}\right)^{2},\qquad 25=5^{2},\qquad e^{6x}=\left(e^{3x}\right)^{2}',
         [('16*x**6', '(4*x**3)**2'), ('5**2', '25'), ('exp(6*x)', 'exp(3*x)**2')]),
        (r'<b>الجذر يتوزع على الضرب</b>. لكن ما يتوزع على الجمع.', r'\sqrt{9x}=3\sqrt{x},\qquad \sqrt{x^{2}+9}\ne x+3',
         [('sqrt(9*x)', '3*sqrt(x)', 't')])])
    rules = [(r'x^{a}\cdot x^{b}=x^{a+b}', ('x**a*x**b', 'x**(a+b)')), (r'\frac{x^{a}}{x^{b}}=x^{a-b}', ('x**a/x**b', 'x**(a-b)')),
             (r'\left(x^{a}\right)^{b}=x^{ab}', ('(x**a)**b', 'x**(a*b)', 't')), (r'x^{-a}=\frac{1}{x^{a}}', ('x**(-a)', '1/x**a')),
             (r'\sqrt{x}=x^{1/2}', ('sqrt(x)', 'x**Rational(1,2)', 't')), (r'(xy)^{a}=x^{a}y^{a}', ('(x*y)**2', 'x**2*y**2'))]
    U.add('short', '📐 القانون: قواعد الأسس',
          table(['القاعدة'], [[mi(r'\displaystyle ' + arith(lt, [c], 'P-A1 rule'))] for lt, c in rules], 'formula compact')
          + p(rich('في الجدول: $a$ و $b$ أي أسين، و $y$ أي شي ثاني مضروب في $x$.'), 'small')
          + tricks([(r'تبي تكتب شي كمربع؟ خذ جذر الرقم، ونص الأس: $9x^4=(3x^2)^2$. وتأكد بالعكس: $(3x^2)^2=3^2x^4=9x^4$.',
                     [('9*x**4', '(3*x**2)**2'), ('(3*x**2)**2', '3**2*x**4')])], 'P-A1'))
    U.example('بسّط', r'x^{3}\cdot x^{-5}\cdot x^{4}', [
        (r'x^{3}\cdot x^{-5}\cdot x^{4}=x^{3+(-5)+4}', [('x**3*x**(-5)*x**4', 'x**(3-5+4)')], 'نفس الأساس مضروب في بعض، فنجمع الأسس.'),
        (r'=x^{2}', [('x**(3-5+4)', 'x**2')], 'نحسب الأس: $3-5+4=2$.')],
        check=r'عوّض $x=2$ في السؤال: $8\cdot\frac{1}{32}\cdot16=4$. وفي الجواب: $2^2=4$ ✓')
    arith('', [('2**3*2**(-5)*2**4', '2**2')], 'P-A1 check')
    U.example('اكتب كأس واحد (تحتاجه قبل التكامل)', r'\frac{1}{x^{2}\sqrt{x}}', [
        (r'\sqrt{x}=x^{1/2}', [('sqrt(x)', 'x**Rational(1,2)', 't')],
         r'نكتب الجذر كأس، عشان نقدر نجمعه مع أس $x^2$. الجذر التربيعي أس $\frac12$.'),
        (r'x^{2}\sqrt{x}=x^{2}\cdot x^{1/2}', [('x**2*sqrt(x)', 'x**2*x**Rational(1,2)', 't')], 'نعوّض الجذر بالأس في المقام.'),
        (r'=x^{2+\frac12}=x^{5/2}', [('x**2*x**Rational(1,2)', 'x**Rational(5,2)', 't')],
         r'ضرب نفس الأساس، فنجمع الأسس: $2+\frac12=\frac52$.'),
        (r'\frac{1}{x^{5/2}}=x^{-5/2}', [('1/(x**2*sqrt(x))', 'x**Rational(-5,2)', 't')],
         'اللي في المقام يطلع فوق بأس سالب، لأن الأس السالب يعني مقلوب.')])
    U.example('اكتب اللي تحت الجذر كمربعين (شكل 4.2)', r'\sqrt{25x^{6}+16}', [
        (r'25x^{6}=\left(5x^{3}\right)^{2}', [('25*x**6', '(5*x**3)**2')], 'هنا التريك: جذر 25 هو 5، ونص الأس 6 هو 3.'),
        (r'16=4^{2}', [('4**2', '16')], 'جذر 16 هو 4.'),
        (r'\sqrt{25x^{6}+16}=\sqrt{\left(5x^{3}\right)^{2}+4^{2}}', [('25*x**6+16', '(5*x**3)**2+4**2')], 'نعوّض المربعين تحت الجذر.'),
        (r'u=5x^{3},\qquad a=4', [('(5*x**3)**2+4**2', '25*x**6+16')],
         r'صار بشكل $\sqrt{u^2+a^2}$ اللي في جدول 4.2. اللي داخل المربع الأول هو $u$، والرقم هو $a$.')])
    U.example('ومع الأسية', r'\sqrt{e^{8x}-9}', [
        (r'e^{8x}=\left(e^{4x}\right)^{2}', [('exp(8*x)', 'exp(4*x)**2')], 'نص الأس $8x$ هو $4x$.'),
        (r'9=3^{2}', [('3**2', '9')], 'جذر 9 هو 3.'),
        (r'\sqrt{e^{8x}-9}=\sqrt{\left(e^{4x}\right)^{2}-3^{2}}', [('exp(8*x)-9', 'exp(4*x)**2-3**2')], 'نعوّض المربعين تحت الجذر.'),
        (r'u=e^{4x},\qquad a=3', [('exp(4*x)**2-3**2', 'exp(8*x)-9')],
         r'صار بشكل $\sqrt{u^2-a^2}$. اللي داخل المربع الأول هو $u$، والرقم هو $a$.')])
    U.add('trap', '⚠️ الفخ', ul([rich(r'$(x+3)^2$ مو $x^2+9$. الصح $x^2+6x+9$، لا تنسى الحد اللي في النص.'),
                                rich(r'$x^{-2}$ مو $-x^2$. الأس السالب يعني مقلوب: $\frac{1}{x^2}$.'),
                                rich(r'$(2x)^2=4x^2$، مو $2x^2$. الرقم بعد يتربّع.'),
                                rich(r'$\sqrt{x^2+9}$ مو $x+3$. الجذر ما يتوزع على الجمع.')]))
    arith('', [('(x+3)**2', 'x**2+6*x+9'), ('(2*x)**2', '4*x**2')], 'P-A1 trap')
    U.add('ok', '✔ تأكد', p(rich('عوّض رقم سهل مثل $x=2$ في السؤال وفي جوابك. إذا طلع نفس الرقم، فتبسيطك صح.')))
    U.task('1', 'G', 'بسّط', 'اكتب كأس واحد:', r'x^{4}\cdot x^{-7}\cdot x', [
        (r'x^{4}\cdot x^{-7}\cdot x^{1}=x^{4-7+1}', [('x**4*x**(-7)*x', 'x**(4-7+1)')],
         'نفس الأساس مضروب، فنجمع الأسس. و $x$ لحالها أسها 1.'),
        (r'=x^{-2}', [('x**(4-7+1)', 'x**(-2)')], 'نحسب الأس: $4-7+1=-2$.'),
        (r'=\frac{1}{x^{2}}', [('x**4*x**(-7)*x', '1/x**2')], 'الأس السالب يعني مقلوب.')],
           'اجمع الأسس، و $x$ لحالها أسها 1.')
    U.task('2', 'P', 'بسّط', 'اكتب كأس واحد:', r'\frac{\sqrt{x}}{x^{3}}', [
        (r'\frac{\sqrt{x}}{x^{3}}=\frac{x^{1/2}}{x^{3}}', [('sqrt(x)/x**3', 'x**Rational(1,2)/x**3', 't')],
         r'نكتب الجذر كأس $\frac12$، عشان نقدر نطرح الأسس.'),
        (r'=x^{\frac12-3}', [('x**Rational(1,2)/x**3', 'x**(Rational(1,2)-3)', 't')],
         'قسمة نفس الأساس: نطرح أس اللي تحت من أس اللي فوق.'),
        (r'=x^{-5/2}', [('sqrt(x)/x**3', 'x**Rational(-5,2)', 't')],
         r'نحسب الأس. نكتب 3 كـ $\frac62$ عشان نطرح: $\frac12-\frac62=-\frac52$.')],
           r'اكتب الجذر كأس $\frac12$ أول.')
    U.task('3', 'P', 'فك القوس', 'فك القوس:', r'\left(2x^{3}\right)^{4}', [
        (r'\left(2x^{3}\right)^{4}=2^{4}\cdot\left(x^{3}\right)^{4}', [('(2*x**3)**4', '2**4*(x**3)**4')],
         'كل شي داخل القوس ياخذ الأس، حتى الرقم 2.'),
        (r'=16\left(x^{3}\right)^{4}', [('2**4*(x**3)**4', '16*(x**3)**4')], r'$2^4=2\cdot2\cdot2\cdot2=16$.'),
        (r'=16x^{12}', [('(2*x**3)**4', '16*x**12')], r'قوة فوق قوة، فنضرب الأسس: $3\cdot4=12$.')],
           'الرقم 2 بعد ياخذ الأس 4.')
    U.task('4', 'I', 'اكتب كمربعين', 'اكتب كمربع ناقص مربع، وطلّع $u$ و $a$:', r'49x^{4}-36', [
        (r'49x^{4}=\left(7x^{2}\right)^{2}', [('49*x**4', '(7*x**2)**2')], 'جذر 49 هو 7، ونص الأس 4 هو 2.'),
        (r'36=6^{2}', [('6**2', '36')], 'جذر 36 هو 6.'),
        (r'49x^{4}-36=\left(7x^{2}\right)^{2}-6^{2}', [('49*x**4-36', '(7*x**2)**2-6**2')], 'نعوّض المربعين.'),
        (r'u=7x^{2},\qquad a=6', [('(7*x**2)**2-6**2', '49*x**4-36')],
         'صار بشكل $u^2-a^2$. اللي داخل المربع الأول هو $u$، والرقم هو $a$.')],
           'جذر الرقم، ونص الأس.')
    U.task('5', 'I', 'اكتب كمربعين', 'اكتب كمربع زائد مربع، وطلّع $u$ و $a$:', r'e^{10x}+4', [
        (r'e^{10x}=\left(e^{5x}\right)^{2}', [('exp(10*x)', 'exp(5*x)**2')], 'نص الأس $10x$ هو $5x$.'),
        (r'4=2^{2}', [('2**2', '4')], 'جذر 4 هو 2.'),
        (r'e^{10x}+4=\left(e^{5x}\right)^{2}+2^{2}', [('exp(10*x)+4', 'exp(5*x)**2+2**2')], 'نعوّض المربعين.'),
        (r'u=e^{5x},\qquad a=2', [('exp(5*x)**2+2**2', 'exp(10*x)+4')],
         'صار بشكل $u^2+a^2$. اللي داخل المربع الأول هو $u$، والرقم هو $a$.')],
           'مع $e$ خذ نص الأس.')
    return U


def part_a2():
    U = PreUnit('P-A2', 'أ2', 'قواعد الاشتقاق وقاعدة السلسلة', 'pre42', 'التفاضل، ومذكرة د. طارق: دروس 3.1–3.3، ص27–42')
    U.why('أول سؤال في الكويز غالبًا «Find dy/dx»، وتحتاج فيه قاعدة السلسلة. وكل «✔ تأكد: اشتق جوابك» في المذكرة يحتاج هذي القواعد.',
          [('U-D1', 1), ('U-D2', 2)])
    U.explain([
        ('في الكويز ما تحتاج تعريف المشتقة، تحتاج القواعد. أهمها ثلاث: القوة، والسلسلة، والضرب.', None, []),
        (r'<b>قاعدة القوة</b>: ننزّل الأس قدّام، وننقص منه 1.', r'\frac{d}{dx}x^{5}=5x^{4},\qquad \frac{d}{dx}x^{-3}=-3x^{-4}',
         [('diff(x**5,x)', '5*x**4'), ('diff(x**(-3),x)', '-3*x**(-4)')]),
        (r'<b>الجذر</b>: نكتبه أس $\frac12$ أول، ثم نستعمل قاعدة القوة.', r'\frac{d}{dx}\sqrt{x}=\frac12x^{-1/2}=\frac{1}{2\sqrt{x}}',
         [('diff(sqrt(x),x)', '1/(2*sqrt(x))', 't')]),
        ('الرقم لحاله مشتقته صفر. والرقم المضروب يبقى مثل ما هو. والجمع نشتقه حد حد.',
         r'\frac{d}{dx}\left(4x^{3}-7x+2\right)=12x^{2}-7', [('diff(4*x**3-7*x+2,x)', '12*x**2-7')]),
        (r"<b>قاعدة السلسلة</b> للدالة اللي داخلها دالة. <b>1.</b> نسمّي اللي داخل $u$. "
         r"<b>2.</b> نشتق الدالة اللي برّا، ونخلي $u$ مثل ما هو. <b>3.</b> نضرب في $u'$، يعني مشتقة اللي داخل.",
         r'\frac{d}{dx}(3x+1)^{5}=5(3x+1)^{4}\cdot3=15(3x+1)^{4}', [('diff((3*x+1)**5,x)', '15*(3*x+1)**4')]),
        (r"نفس الفكرة مع أي دالة: مشتقة اللي برّا من الجدول، ثم نضرب في $u'$.",
         r'\frac{d}{dx}e^{x^{2}}=e^{x^{2}}\cdot2x,\qquad \frac{d}{dx}\sin4x=4\cos4x',
         [('diff(exp(x**2),x)', '2*x*exp(x**2)'), ('diff(sin(4*x),x)', '4*cos(4*x)')]),
        ('<b>ln</b>: مشتقة اللي داخل، مقسومة على اللي داخل.', r'\frac{d}{dx}\ln\left|x^{2}+1\right|=\frac{2x}{x^{2}+1}',
         [('diff(log(x**2+1),x)', '2*x/(x**2+1)')]),
        ('<b>الضرب</b>: مشتقة الأولى × الثانية، زائد الأولى × مشتقة الثانية.', r'\frac{d}{dx}\left(x^{2}\sin x\right)=2x\sin x+x^{2}\cos x',
         [('diff(x**2*sin(x),x)', '2*x*sin(x)+x**2*cos(x)')]),
        ('<b>القسمة</b>: مشتقة اللي فوق × اللي تحت، ناقص اللي فوق × مشتقة اللي تحت. ثم نقسم الكل على اللي تحت تربيع.',
         r'\frac{d}{dx}\frac{x}{x+1}=\frac{1\cdot(x+1)-x\cdot1}{(x+1)^{2}}=\frac{1}{(x+1)^{2}}', [('diff(x/(x+1),x)', '1/(x+1)**2')])])
    r = [formula('u**n', 'n*u**(n-1)', 'diff', branches=('t',), real=('n',), uprime=True, label='P-A2 power'),
         formula('sqrt(u)', '1/(2*sqrt(u))', 'diff', branches=('t',), uprime=True, label='P-A2 sqrt'),
         formula('exp(u)', 'exp(u)', 'diff', branches=('x',), uprime=True, label='P-A2 exp'),
         formula('a**u', 'a**u*log(a)', 'diff', branches=('x',), pos=('a',), uprime=True, label='P-A2 a^u'),
         formula('log(Abs(u))', '1/u', 'diff', branches=('t', '-t'), uprime=True, label='P-A2 ln'),
         formula('sin(u)', 'cos(u)', 'diff', branches=('x',), uprime=True, label='P-A2 sin'),
         formula('cos(u)', '-sin(u)', 'diff', branches=('x',), uprime=True, label='P-A2 cos'),
         formula('tan(u)', 'sec(u)**2', 'diff', branches=('t/(1+t)',), uprime=True, label='P-A2 tan'),
         formula('sec(u)', 'sec(u)*tan(u)', 'diff', branches=('t/(1+t)',), uprime=True, label='P-A2 sec')]
    U.add('short', '📐 القانون: جدول المشتقات (u′ = مشتقة اللي داخل الدالة)',
          table(['المشتقة', 'تساوي'], [_row(z) for z in r], 'formula compact')
          + p(rich('في الجدول: $n$ أي أس، و $a$ أي رقم موجب. و $\\log$ بدون أساس يعني أساس 10، ومشتقته مثل ln مقسومة على $\\ln10$.'), 'small')
          + tricks([(r"اشتق من برّا لجوّا: كل طبقة نشتقها، ونضرب كل المشتقات في بعض. مثال: $\left(e^{\sin3x}\right)'=e^{\sin3x}\cdot\cos3x\cdot3$.",
                     [('diff(exp(sin(3*x)),x)', 'exp(sin(3*x))*cos(3*x)*3')])], 'P-A2'))
    U.example('أوجد المشتقة (قوة على قوس)', r'y=\left(x^{2}+1\right)^{4}', [
        (r"u=x^{2}+1,\qquad u'=2x", [('diff(x**2+1,x)', '2*x')],
         'قوس عليه أس، وداخله دالة، فنستعمل السلسلة. نسمّي اللي داخل القوس $u$، ونشتقه.'),
        (r"y'=4u^{3}\cdot u'", [('diff((x**2+1)**4,x)', '4*(x**2+1)**3*diff(x**2+1,x)')],
         "قاعدة القوة على القوس: ننزّل 4 وننقص 1. ثم نضرب في $u'$."),
        (r"y'=4\left(x^{2}+1\right)^{3}\cdot2x", [('diff((x**2+1)**4,x)', '4*(x**2+1)**3*2*x')], "نرجّع $u$ و $u'$."),
        (r"y'=8x\left(x^{2}+1\right)^{3}", [('diff((x**2+1)**4,x)', '8*x*(x**2+1)**3')], r'نضرب الأرقام: $4\cdot2=8$.')])
    U.example('أوجد المشتقة (أسية مع سلسلة)', r'y=e^{3x^{2}}', [
        (r"u=3x^{2},\qquad u'=6x", [('diff(3*x**2,x)', '6*x')], 'الأس كله دالة، فنسمّيه $u$ ونشتقه.'),
        (r"y'=e^{u}\cdot u'", [('diff(exp(3*x**2),x)', 'exp(3*x**2)*diff(3*x**2,x)')],
         "قانون الأسية: مشتقة $e^u$ هي $e^u$ نفسها، مضروبة في $u'$."),
        (r"y'=6x\,e^{3x^{2}}", [('diff(exp(3*x**2),x)', '6*x*exp(3*x**2)')], "نرجّع $u$ و $u'$، ونكتب $6x$ قدّام.")])
    U.example('أوجد المشتقة (ln، وداخلها سلسلة)', r'y=\ln\left|\cos3x\right|', [
        (r'u=\cos3x', [('cos(3*x)', 'cos(3*x)')], 'برّا ln، وداخلها $\\cos3x$. نسمّي اللي داخل $u$.'),
        (r"u'=-\sin3x\cdot3=-3\sin3x", [('diff(cos(3*x),x)', '-3*sin(3*x)')], 'مشتقة cos هي سالب sin. ونضرب في 3، لأن مشتقة $3x$ هي 3.'),
        (r"y'=\frac{u'}{u}=\frac{-3\sin3x}{\cos3x}", [('diff(log(cos(3*x)),x)', '-3*sin(3*x)/cos(3*x)')],
         'قانون ln: مشتقة اللي داخل، مقسومة على اللي داخل.'),
        (r'=-3\tan3x', [('-3*sin(3*x)/cos(3*x)', '-3*tan(3*x)')], r'لأن $\frac{\sin3x}{\cos3x}=\tan3x$.')])
    U.example('أوجد المشتقة (ضرب)', r'y=x^{2}e^{-x}', [
        (r"f=x^{2},\qquad f'=2x", [('diff(x**2,x)', '2*x')], 'دالتين مضروبتين، فنستعمل قاعدة الضرب. نسمّي الأولى $f$، ونشتقها.'),
        (r"g=e^{-x},\qquad g'=-e^{-x}", [('diff(exp(-x),x)', '-exp(-x)')],
         'نسمّي الثانية $g$. مشتقتها فيها سلسلة: نضرب في $-1$، لأن مشتقة $-x$ هي $-1$.'),
        (r"y'=f'g+fg'=2x\,e^{-x}-x^{2}e^{-x}", [('diff(x**2*exp(-x),x)', '2*x*exp(-x)-x**2*exp(-x)')],
         'قاعدة الضرب: مشتقة الأولى × الثانية، زائد الأولى × مشتقة الثانية.')])
    U.add('trap', '⚠️ الفخ', ul([rich("أكثر غلطة في الكويز: تنسى مشتقة اللي داخل. مثلًا $(e^{3x})'=3e^{3x}$، مو $e^{3x}$."),
                                rich("$(\\ln|u|)'=\\frac{u'}{u}$، مو $\\frac1u$ بس."),
                                rich("$(\\cos x)'=-\\sin x$، بالسالب.")]))
    arith('', [('diff(exp(3*x),x)', '3*exp(3*x)')], 'P-A2 trap')
    U.add('ok', '✔ تأكد', p(rich('كل دالة داخلها دالة، لازم تطلع مشتقتها مضروبة في مشتقة اللي داخل. إذا ما لقيتها، ارجع لقاعدة السلسلة.')))
    U.drill('1', 'G-46', 'G', 'ننزّل الأس 4، وننقص 1، ثم نضرب في مشتقة القوس.',
            first=r"u=2x^{3}-5,\quad u'=6x^{2}", claims=[('diff(2*x**3-5,x)', '6*x**2')],
            sol_rows=[('tex', r"y'=4u^{3}\cdot u'", [('diff((2*x**3-5)**4,x)', '4*(2*x**3-5)**3*diff(2*x**3-5,x)')],
                       "قاعدة القوة على القوس: ننزّل 4 وننقص 1. ثم نضرب في $u'$."),
                      ('tex', r"y'=4\left(2x^{3}-5\right)^{3}\cdot6x^{2}", [('diff((2*x**3-5)**4,x)', '4*(2*x**3-5)**3*6*x**2')],
                       "نرجّع $u$ و $u'$."),
                      ('line', '24*x**2*(2*x**3-5)**3', r'نضرب الأرقام: $4\cdot6=24$.')])
    U.drill('2', 'M-05', 'P', 'الأس كله $u$، ومشتقة $e^u$ هي $e^u$ مضروبة في مشتقة الأس.',
            sol_rows=[('tex', r"u=2x^{5}+3x,\quad u'=10x^{4}+3", [('diff(2*x**5+3*x,x)', '10*x**4+3')],
                       'الأس كله دالة، فنسمّيه $u$ ونشتقه. مشتقة $2x^5$ هي $10x^4$، ومشتقة $3x$ هي 3.'),
                      ('tex', r"y'=e^{u}\cdot u'", [('diff(exp(2*x**5+3*x),x)', 'exp(2*x**5+3*x)*diff(2*x**5+3*x,x)')],
                       "قانون الأسية: مشتقة $e^u$ هي $e^u$ نفسها، مضروبة في $u'$."),
                      ('line', '(10*x**4+3)*exp(2*x**5+3*x)', "نرجّع $u$ و $u'$. والأس يبقى مثل ما هو.")])
    U.drill('3', 'G-48', 'I', 'ln: مشتقة اللي داخل على اللي داخل.',
            sol_rows=[('tex', r"u=x^{2}+3x,\quad u'=2x+3", [('diff(x**2+3*x,x)', '2*x+3')], 'برّا ln. نسمّي اللي داخل $u$، ونشتقه.'),
                      ('tex', r"y'=\frac{u'}{u}", [('diff(log(x**2+3*x),x)', 'diff(x**2+3*x,x)/(x**2+3*x)', 't')],
                       'قانون ln: مشتقة اللي داخل، مقسومة على اللي داخل.'),
                      ('line', '(2*x+3)/(x**2+3*x)', "نعوّض $u$ و $u'$.")])
    U.drill('4', 'G-49', 'I', 'دالتين مضروبتين: قاعدة الضرب.',
            sol_rows=[('tex', r"f=x^{3},\quad f'=3x^{2}", [('diff(x**3,x)', '3*x**2')], 'دالتين مضروبتين. نسمّي الأولى $f$، ونشتقها بقاعدة القوة.'),
                      ('tex', r"g=e^{2x},\quad g'=2e^{2x}", [('diff(exp(2*x),x)', '2*exp(2*x)')],
                       'نسمّي الثانية $g$. مشتقتها فيها سلسلة: نضرب في 2، لأن مشتقة $2x$ هي 2.'),
                      ('line', '3*x**2*exp(2*x)+2*x**3*exp(2*x)', 'قاعدة الضرب: مشتقة الأولى × الثانية، زائد الأولى × مشتقة الثانية.')])
    U.drill('5', 'G-50', 'I', 'حدّين: نشتق كل واحد لحاله.',
            sol_rows=[('tex', r"\frac{d}{dx}\tan5x=\sec^{2}5x\cdot5", [('diff(tan(5*x),x)', '5*sec(5*x)**2')],
                       r'حدّين مجموعين، فنشتق كل حد لحاله. مشتقة tan هي $\sec^2$، ونضرب في 5، لأن مشتقة $5x$ هي 5.'),
                      ('tex', r"\frac{d}{dx}\sqrt{x^{2}+1}=\frac{2x}{2\sqrt{x^{2}+1}}", [('diff(sqrt(x**2+1),x)', '2*x/(2*sqrt(x**2+1))')],
                       'مشتقة الجذر: 1 على ضعف الجذر، مضروبة في مشتقة اللي تحته.'),
                      ('tex', r"=\frac{x}{\sqrt{x^{2}+1}}", [('2*x/(2*sqrt(x**2+1))', 'x/sqrt(x**2+1)')], 'نختصر 2 فوق مع 2 تحت.'),
                      ('line', '5*sec(5*x)**2+x/sqrt(x**2+1)', 'نجمع مشتقتي الحدّين.')])
    return U


def part_a3():
    U = PreUnit('P-A3', 'أ3', 'الدوال الزائدية (درس 4.1)', 'pre42', 'مذكرة د. طارق: درس 4.1، ص49–56')
    U.why(r'درس 4.2 عن الدوال الزائدية <b>العكسية</b>، فلازم تعرف الدوال الزائدية العادية أول. '
          r'وسؤال المشتقة يجمع دالة عادية مثل $\cosh(3x^2)$ مع دالة عكسية.',
          [('U-D1', 1), ('U-I2', 4), ('U-P1', 12), ('U-P9', 20)])
    U.explain([
        (r'الدوال الزائدية مبنية من $e^x$ و $e^{-x}$ بس. $\cosh$ هو متوسطهم، و $\sinh$ نص الفرق بينهم.',
         r'\sinh x=\frac{e^{x}-e^{-x}}{2},\qquad \cosh x=\frac{e^{x}+e^{-x}}{2}', [('sinh(x)', '(exp(x)-exp(-x))/2'), ('cosh(x)', '(exp(x)+exp(-x))/2')]),
        (r'نحسب قيمتها بالتعويض في التعريف. و $e$ و $\ln$ يلغون بعض: $e^{\ln3}=3$.',
         r'\cosh(\ln3)=\frac{e^{\ln3}+e^{-\ln3}}{2}=\frac{3+\frac13}{2}=\frac53', [('cosh(log(3))', 'Rational(5,3)')]),
        ('الأربع الباقية قسمة، مثل المثلثات بالضبط.', r'\tanh x=\frac{\sinh x}{\cosh x},\quad \coth x=\frac{\cosh x}{\sinh x},\quad '
         r'\operatorname{sech}x=\frac{1}{\cosh x},\quad \operatorname{csch}x=\frac{1}{\sinh x}',
         [('tanh(x)', 'sinh(x)/cosh(x)'), ('coth(x)', 'cosh(x)/sinh(x)'), ('sech(x)', '1/cosh(x)'), ('csch(x)', '1/sinh(x)')]),
        (r'المتطابقة الأساسية فيها <b>سالب</b>، عكس المثلثات. و $\cosh x$ دايم 1 أو أكبر، فما يصير صفر ولا سالب.',
         r'\cosh^{2}x-\sinh^{2}x=1,\qquad \cosh0=1,\qquad \sinh0=0', [('cosh(x)**2-sinh(x)**2', '1'), ('cosh(0)', '1'), ('sinh(0)', '0')]),
        (r'المشتقات مثل sin و cos، بس <b>بدون سالب</b>: مشتقة $\cosh$ هي $+\sinh$.',
         r'\frac{d}{dx}\sinh x=\cosh x,\qquad \frac{d}{dx}\cosh x=\sinh x', [('diff(sinh(x),x)', 'cosh(x)'), ('diff(cosh(x),x)', 'sinh(x)')]),
        ('ومع دالة داخلها: نفس قاعدة السلسلة. نضرب في مشتقة اللي داخل.', r'\frac{d}{dx}\cosh\left(3x^{2}\right)=\sinh\left(3x^{2}\right)\cdot6x',
         [('diff(cosh(3*x**2),x)', '6*x*sinh(3*x**2)')]),
        ('والتكامل عكس المشتقة.', r'\int\cosh x\,dx=\sinh x+C,\qquad \int\sinh x\,dx=\cosh x+C',
         [('diff(sinh(x),x)', 'cosh(x)'), ('diff(cosh(x),x)', 'sinh(x)')])])
    d = [formula('sinh(u)', 'cosh(u)', 'diff', branches=('x',), uprime=True, label='P-A3 d sinh'),
         formula('cosh(u)', 'sinh(u)', 'diff', branches=('x',), uprime=True, label='P-A3 d cosh'),
         formula('tanh(u)', 'sech(u)**2', 'diff', branches=('x',), uprime=True, label='P-A3 d tanh'),
         formula('coth(u)', '-csch(u)**2', 'diff', branches=('t',), uprime=True, label='P-A3 d coth'),
         formula('sech(u)', '-sech(u)*tanh(u)', 'diff', branches=('x',), uprime=True, label='P-A3 d sech'),
         formula('csch(u)', '-csch(u)*coth(u)', 'diff', branches=('t',), uprime=True, label='P-A3 d csch')]
    i = [formula('sinh(u)', 'cosh(u)', label='P-A3 int sinh'), formula('cosh(u)', 'sinh(u)', label='P-A3 int cosh'),
         formula('sech(u)**2', 'tanh(u)', label='P-A3 int sech2'), formula('sech(u)*tanh(u)', '-sech(u)', label='P-A3 int sech tanh')]
    ids = arith(r'\cosh^{2}x-\sinh^{2}x=1,\qquad 1-\tanh^{2}x=\operatorname{sech}^{2}x,\qquad \coth^{2}x-1=\operatorname{csch}^{2}x',
                [('cosh(x)**2-sinh(x)**2', '1'), ('1-tanh(x)**2', 'sech(x)**2'), ('coth(x)**2-1', 'csch(x)**2')], 'P-A3 identities')
    U.add('short', '📐 القانون: المشتقات والتكاملات والمتطابقات',
          table(['المشتقة', 'تساوي'], [_row(z) for z in d], 'formula compact')
          + tricks([(r"الإشارة السالبة بس مع الثلاث اللي هي مقلوب: coth و sech و csch. أما sinh و cosh و tanh فبدون سالب. "
                     r"مثال: $\left(\operatorname{sech}x\right)'=-\operatorname{sech}x\tanh x$، و $\left(\tanh x\right)'=\operatorname{sech}^2x$.",
                     [('diff(sech(x),x)', '-sech(x)*tanh(x)'), ('diff(tanh(x),x)', 'sech(x)**2')])], 'P-A3')
          + table(['التكامل', 'الجواب (+C)'], [_row(z) for z in i], 'formula compact') + md(ids))
    SHEET['hyp'] = table(['المشتقة', 'تساوي'], [_row(z) for z in d], 'formula compact') + md(ids)
    U.example('أوجد المشتقة', r'y=\cosh\left(4x^{2}\right)', [
        (r"u=4x^{2},\qquad u'=8x", [('diff(4*x**2,x)', '8*x')], 'cosh داخلها دالة، فنستعمل السلسلة. نسمّي اللي داخل $u$، ونشتقه.'),
        (r"\left(\cosh u\right)'=\sinh u\cdot u'", [('diff(cosh(4*x**2),x)', 'sinh(4*x**2)*diff(4*x**2,x)')],
         "مشتقة cosh هي sinh، بدون سالب. ثم نضرب في $u'$."),
        (r"y'=8x\sinh\left(4x^{2}\right)", [('diff(cosh(4*x**2),x)', '8*x*sinh(4*x**2)')], "نعوّض $u$ و $u'$، ونكتب $8x$ قدّام.")])
    U.example('اكتب بالأسس (تحتاجه في النوع 20)', r'e^{x}\sinh x', [
        (r'\sinh x=\frac{e^{x}-e^{-x}}{2}', [('sinh(x)', '(exp(x)-exp(-x))/2')], 'نكتب sinh بتعريفه، عشان يصير كل شي أسس.'),
        (r'e^{x}\sinh x=\frac{e^{x}e^{x}-e^{x}e^{-x}}{2}', [('exp(x)*sinh(x)', '(exp(x)*exp(x)-exp(x)*exp(-x))/2')],
         'نضرب $e^x$ في كل حد فوق.'),
        (r'=\frac{e^{2x}-e^{0}}{2}', [('(exp(x)*exp(x)-exp(x)*exp(-x))/2', '(exp(2*x)-exp(0))/2')],
         'ضرب نفس الأساس، فنجمع الأسس: $x+x=2x$، و $x-x=0$.'),
        (r'=\frac{e^{2x}-1}{2}', [('exp(x)*sinh(x)', '(exp(2*x)-1)/2')], 'أي شي أسه 0 يساوي 1، فـ $e^0=1$.')])
    U.example('كامل بتعويض بسيط', r'\int\sinh3x\,dx', [
        (r'u=3x,\qquad du=3\,dx', [('diff(3*x,x)', '3')], 'sinh داخلها $3x$. نسمّيه $u$، ونشتقه.'),
        (r'dx=\frac{du}{3}', [('1/diff(3*x,x)', 'Rational(1,3)')], 'نقسم على 3، عشان نعوّض مكان $dx$.'),
        (r'\int\sinh3x\,dx=\frac13\int\sinh u\,du', [('sinh(3*x)', 'Rational(1,3)*sinh(3*x)*diff(3*x,x)')],
         r'نعوّض. والـ $\frac13$ تطلع برّا التكامل.'),
        (r'=\frac13\cosh u', [('integrate(sinh(u),u)/3', 'cosh(u)/3')], 'تكامل sinh هو cosh، بدون سالب.'),
        (r'=\frac13\cosh3x+C', [('diff(cosh(3*x)/3,x)', 'sinh(3*x)')], 'نرجع $u=3x$.')])
    U.add('trap', '⚠️ الفخ', ul([rich(r'$\cosh^2x-\sinh^2x=1$ بالسالب، عكس $\cos^2x+\sin^2x=1$.'),
                                rich(r'مشتقة $\cosh x$ هي $+\sinh x$ بدون سالب. وتكامل $\sinh x$ هو $+\cosh x$.'),
                                rich(r'$\sinh^{-1}x$ هي الدالة العكسية من درس 4.2. مو $\frac{1}{\sinh x}$، هذي اسمها $\operatorname{csch}x$.')]))
    U.add('ok', '✔ تأكد', p(rich(r'عوّض $x=0$: $\sinh0=0$ و $\cosh0=1$. إذا جوابك يعطي غير كذا عند الصفر، راجع الإشارة.')))
    U.drill('1', 'G-51', 'G', 'cosh يصير sinh، ثم نضرب في مشتقة اللي داخل.', first=r"u=5x^{2},\quad u'=10x", claims=[('diff(5*x**2,x)', '10*x')],
            sol_rows=[('tex', r"\left(\cosh u\right)'=\sinh u\cdot u'", [('diff(cosh(5*x**2),x)', 'sinh(5*x**2)*diff(5*x**2,x)')],
                       "مشتقة cosh هي sinh، بدون سالب. ثم نضرب في $u'$."),
                      ('tex', r"y'=\sinh\left(5x^{2}\right)\cdot10x", [('diff(cosh(5*x**2),x)', 'sinh(5*x**2)*10*x')], "نعوّض $u$ و $u'$."),
                      ('line', '10*x*sinh(5*x**2)', 'نكتب $10x$ قدّام.')])
    U.drill('2', 'M-06', 'P', 'من برّا لجوّا: $e$، ثم sinh، ثم $3x^5$.',
            sol_rows=[('tex', r"y'=e^{\sinh\left(3x^{5}\right)}\cdot\left(\sinh\left(3x^{5}\right)\right)'",
                       [('diff(exp(sinh(3*x**5)),x)', 'exp(sinh(3*x**5))*diff(sinh(3*x**5),x)')],
                       r'هنا التريك: من برّا لجوّا. أول طبقة $e^{\ldots}$: مشتقتها نفسها، ونضرب في مشتقة الأس.'),
                      ('tex', r"=e^{\sinh\left(3x^{5}\right)}\cdot\cosh\left(3x^{5}\right)\cdot\left(3x^{5}\right)'",
                       [('diff(exp(sinh(3*x**5)),x)', 'exp(sinh(3*x**5))*cosh(3*x**5)*diff(3*x**5,x)')],
                       'الطبقة الثانية sinh: مشتقتها cosh بدون سالب، ونضرب في مشتقة اللي داخلها.'),
                      ('tex', r"=e^{\sinh\left(3x^{5}\right)}\cdot\cosh\left(3x^{5}\right)\cdot15x^{4}",
                       [('diff(exp(sinh(3*x**5)),x)', 'exp(sinh(3*x**5))*cosh(3*x**5)*15*x**4')],
                       r'آخر طبقة $3x^5$: ننزّل 5 ونضربها في 3، وننقص الأس 1. $3\cdot5=15$.'),
                      ('line', '15*x**4*cosh(3*x**5)*exp(sinh(3*x**5))', 'نكتب $15x^4$ قدّام.')])
    U.drill('3', 'G-53', 'I', 'مشتقة sech فيها سالب.',
            sol_rows=[('tex', r"u=3x,\quad u'=3", [('diff(3*x,x)', '3')], 'sech داخلها $3x$. نسمّيه $u$، ونشتقه.'),
                      ('tex', r"\left(\operatorname{sech}u\right)'=-\operatorname{sech}u\tanh u\cdot u'",
                       [('diff(sech(3*x),x)', '-sech(3*x)*tanh(3*x)*diff(3*x,x)')],
                       "قانون sech: مشتقتها فيها سالب، لأن sech مقلوب cosh. ثم نضرب في $u'$."),
                      ('line', '-3*sech(3*x)*tanh(3*x)', "نعوّض $u=3x$ و $u'=3$.")])
    U.drill('4', 'G-54', 'P', 'نسمّي $4x$ هو $u$، ونقسم على 4.',
            sol_rows=[('sub', '4*x', '4', 'cosh داخلها $4x$. نسمّيه $u$، ونشتقه.'),
                      ('tex', r'dx=\frac{du}{4}', [('1/diff(4*x,x)', 'Rational(1,4)')], 'نقسم على 4، عشان نعوّض مكان $dx$.'),
                      ('tex', r'\int\cosh4x\,dx=\frac14\int\cosh u\,du', [('cosh(4*x)', 'Rational(1,4)*cosh(4*x)*diff(4*x,x)')],
                       r'نعوّض. والـ $\frac14$ تطلع برّا التكامل.'),
                      ('tex', r'=\frac14\sinh u', [('integrate(cosh(u),u)/4', 'sinh(u)/4')], 'تكامل cosh هو sinh.'),
                      ('line', 'sinh(4*x)/4', 'نرجع $u=4x$.')])
    U.drill('5', 'M-07', 'I', 'نسمّي $x^3$ هو $u$، ومشتقته $3x^2$.',
            sol_rows=[('sub', 'x**3', '3*x**2', 'داخل cosh فيه $x^3$، ومشتقته $3x^2$. وبرّا عندنا $x^2$، فنسمّي $x^3$ هو $u$.'),
                      ('tex', r'x^{2}\,dx=\frac{du}{3}', [('diff(x**3,x)/3', 'x**2')],
                       r'السؤال فيه $x^2\,dx$ بس، مو $3x^2\,dx$. فنقسم الطرفين على 3.'),
                      ('tex', r'\int x^{2}\cosh\left(x^{3}\right)dx=\frac13\int\cosh u\,du', [('x**2*cosh(x**3)', 'Rational(1,3)*cosh(x**3)*diff(x**3,x)')],
                       r'نعوّض. ما بقي ولا $x$، والـ $\frac13$ تطلع برّا.'),
                      ('tex', r'=\frac13\sinh u', [('integrate(cosh(u),u)/3', 'sinh(u)/3')], 'تكامل cosh هو sinh، بدون سالب.'),
                      ('line', 'sinh(x**3)/3', 'نرجع $u=x^3$.')])
    U.task('6', 'I', 'احسب', 'احسب القيمة بالتعريف:', r'\sinh\left(\ln2\right)', [
        (r'\sinh(\ln2)=\frac{e^{\ln2}-e^{-\ln2}}{2}', [('sinh(log(2))', '(exp(log(2))-exp(-log(2)))/2')],
         r'نعوّض $\ln2$ مكان $x$ في التعريف $\frac{e^x-e^{-x}}{2}$.'),
        (r'=\frac{2-\frac12}{2}', [('(exp(log(2))-exp(-log(2)))/2', '(2-Rational(1,2))/2')],
         r'$e$ و $\ln$ يلغون بعض: $e^{\ln2}=2$. والأس السالب مقلوب: $e^{-\ln2}=\frac12$.'),
        (r'=\frac{3/2}{2}', [('(2-Rational(1,2))/2', 'Rational(3,2)/2')], r'نطرح فوق: $2-\frac12=\frac42-\frac12=\frac32$.'),
        (r'=\frac34', [('sinh(log(2))', 'Rational(3,4)')], r'القسمة على 2 تضرب المقام في 2: $\frac{3}{2\cdot2}=\frac34$.')],
           'عوّض في التعريف، و $e^{\\ln2}=2$.')
    return U


def part_a4():
    U = PreUnit('P-A4', 'أ4', 'التكامل الأساسي والتعويض بـ u', 'pre42', 'مذكرة د. طارق: دروس 2.3 و2.4 (ص20–26) و3.1 و3.2')
    U.why('كل قوانين 4.2 مكتوبة بـ $u$ و $du$، يعني كل تكامل في 4.2 تعويض. وفي 5.1 و5.2 تحتاج نفس التعويض ونفس التكاملات الأساسية.',
          [('U-I1', 3), ('U-I3', 5), ('U-I8', 10), ('U-P10', 21)])
    U.explain([
        (r'التكامل عكس الاشتقاق. نبي دالة مشتقتها تساوي اللي داخل التكامل. ونزيد $+C$، لأن مشتقة أي رقم صفر.',
         r'\frac{d}{dx}\left(x^{3}+5\right)=3x^{2}\ \Rightarrow\ \int3x^{2}\,dx=x^{3}+C', [('diff(x**3+5,x)', '3*x**2')]),
        (r'<b>قاعدة القوة</b>: نزيد الأس 1، ونقسم على الأس الجديد.',
         r'\int x^{4}dx=\frac{x^{5}}{5}+C,\qquad \int\frac{dx}{x^{2}}=\int x^{-2}dx=\frac{x^{-1}}{-1}=-\frac1x+C',
         [('diff(x**5/5,x)', 'x**4'), ('diff(-1/x,x)', 'x**(-2)')]),
        (r'<b>الجذر</b>: نكتبه أس أول. والقسمة على كسر يعني نضرب في مقلوبه.',
         r'\int\sqrt{x}\,dx=\int x^{1/2}dx=\frac{x^{3/2}}{3/2}=\frac23x^{3/2}+C', [('diff(2*x**Rational(3,2)/3,x)', 'sqrt(x)', 't')]),
        (r'إذا الأس $-1$، قاعدة القوة ما تنفع، لأن الأس الجديد يصير صفر. فتكامل $\frac1x$ هو $\ln|x|$.',
         r'\int\frac{dx}{x}=\ln|x|+C', [('diff(log(x),x)', '1/x', 't')]),
        ('الرقم المضروب يطلع برّا التكامل. والجمع والطرح نكاملهم حد حد.',
         r'\int\left(6x^{2}+\frac{4}{x}\right)dx=2x^{3}+4\ln|x|+C', [('diff(2*x**3+4*log(x),x)', '6*x**2+4/x', 't')]),
        (r'<b>التعويض</b>: دالة داخل دالة، ومشتقة اللي داخل موجودة جنبها. نسمّي اللي داخل $u$. '
         r'ولو المشتقة ناقصها رقم بس، عادي. هذا عكس قاعدة السلسلة.',
         r'\int2x\cos\left(x^{2}\right)dx:\quad u=x^{2},\ du=2x\,dx\ \Rightarrow\ \int\cos u\,du=\sin\left(x^{2}\right)+C',
         [('diff(sin(x**2),x)', '2*x*cos(x**2)')]),
        (r'لهذا نقسم على 3 مع $e^{3x}$، لأن مشتقة $3x$ هي 3. والمثال 2 تحت يشرح ليش.', r'\int e^{3x}dx=\frac{e^{3x}}{3}+C',
         [('diff(exp(3*x)/3,x)', 'exp(3*x)')]),
        ('<b>تأكد دايم</b>: اشتق جوابك. لازم يرجع اللي داخل التكامل.', None, [])])
    t = [formula('x**n', 'x**(n+1)/(n+1)', var='x', branches=('t',), real=('n',), label='P-A4 power'),
         formula('1/x', 'log(Abs(x))', var='x', branches=('t', '-t'), label='P-A4 1/x'),
         formula('exp(k*x)', 'exp(k*x)/k', var='x', branches=('x',), pos=('k',), label='P-A4 e'),
         formula('sin(k*x)', '-cos(k*x)/k', var='x', branches=('x',), pos=('k',), label='P-A4 sin'),
         formula('cos(k*x)', 'sin(k*x)/k', var='x', branches=('x',), pos=('k',), label='P-A4 cos'),
         formula('sinh(k*x)', 'cosh(k*x)/k', var='x', branches=('x',), pos=('k',), label='P-A4 sinh'),
         formula('cosh(k*x)', 'sinh(k*x)/k', var='x', branches=('x',), pos=('k',), label='P-A4 cosh'),
         formula('sec(x)**2', 'tan(x)', var='x', branches=('t/(1+t)',), label='P-A4 sec2')]
    U.add('short', '📐 القانون: جدول التكاملات الأساسية', table(['التكامل', 'الجواب (+C)'], [_row(z) for z in t], 'formula compact')
          + p(rich('في الجدول: $n$ هو الأس، ولازم $n\\ne-1$. و $k$ هو الرقم اللي قدام $x$.'), 'small'))
    U.add('short', '🧭 الطريقة: التعويض بـ u في خمس خطوات', method([
        '<b>نختار $u$</b>: اللي داخل دالة، أو تحت جذر، أو تحت أس. ولازم مشتقته تكون موجودة جنبه.',
        '<b>نشتق</b>: نكتب $du=(\\ldots)\\,dx$. ثم نطلّع اللي موجود في السؤال، مثل $x\\,dx=\\frac{du}{2}$.',
        '<b>نعوّض</b>: نكتب التكامل كله بـ $u$. لازم كل $x$ تختفي.',
        '<b>نكامل</b> من الجدول.',
        '<b>نرجع</b> لـ $x$، ونزيد $+C$.'],
        tricks_=[(r'رقم التعديل: لو $du$ فيها رقم زيادة عن السؤال، نقسم عليه برّا التكامل. '
                  r'مثلًا $u=x^2+1$ يعطي $du=2x\,dx$، والسؤال فيه $x\,dx$ بس، فـ $x\,dx=\frac12du$.',
                  [('diff(x**2+1,x)/2', 'x')])], label='P-A4'))
    picks = [(r'\int\cos3x\,dx', 'u=3x', 'du=3\\,dx', r'\frac13\sin3x', ('diff(sin(3*x)/3,x)', 'cos(3*x)'), 'اللي داخل cos.'),
             (r'\int x\left(x^{2}+1\right)^{5}dx', 'u=x^{2}+1', 'du=2x\\,dx', r'\frac{\left(x^{2}+1\right)^{6}}{12}',
              ('diff((x**2+1)**6/12,x)', 'x*(x**2+1)**5'), 'اللي تحت الأس. مشتقته $2x$، وعندنا $x$.'),
             (r'\int\frac{e^{x}}{1+e^{x}}dx', 'u=1+e^{x}', 'du=e^{x}dx', r'\ln\left(1+e^{x}\right)',
              ('diff(log(1+exp(x)),x)', 'exp(x)/(1+exp(x))'), 'المقام. مشتقته $e^x$، وموجودة فوق.'),
             (r'\int\frac{\ln x}{x}dx', 'u=\\ln x', 'du=\\frac{dx}{x}', r'\frac{\left(\ln x\right)^{2}}{2}',
              ('diff(log(x)**2/2,x)', 'log(x)/x'), 'مشتقة $\\ln x$ هي $\\frac1x$، وموجودة.'),
             (r'\int\frac{dx}{\sqrt{4x^{2}+25}}', 'u=2x', 'du=2\\,dx', r'\frac12\sinh^{-1}\frac{2x}{5}',
              ('diff(asinh(2*x/5)/2,x)', '1/sqrt(4*x**2+25)'), 'تحت الجذر $(2x)^2+5^2$، فـ $u=2x$. هذا من درس 4.2.')]
    U.add('short', '🧭 كيف تختار u؟', table(['السؤال', 'u', 'du', 'الجواب (+C)', 'ليش هذا u'],
                                         [[mi(r'\displaystyle ' + q), mi(u), mi(r'\displaystyle ' + du), mi(r'\displaystyle ' + arith(a, [c], 'P-A4 pick')), rich(w)]
                                          for q, u, du, a, c, w in picks], 'formula compact pick'))
    U.example('مشتقة القوس موجودة، ناقصها رقم', r'\int x\left(x^{2}+1\right)^{5}dx', [
        (r'u=x^{2}+1,\qquad du=2x\,dx', [('diff(x**2+1,x)', '2*x')], 'نختار $u$: اللي تحت الأس. ونشتقه.'),
        (r'x\,dx=\frac{du}{2}', [('diff(x**2+1,x)/2', 'x')], r'هنا التريك: رقم التعديل. السؤال فيه $x\,dx$ بس، مو $2x\,dx$. فنقسم على 2.'),
        (r'\int x\left(x^{2}+1\right)^{5}dx=\frac12\int u^{5}\,du', [('x*(x**2+1)**5', 'Rational(1,2)*(x**2+1)**5*diff(x**2+1,x)')],
         r'نعوّض: القوس يصير $u^5$، و $x\,dx$ تصير $\frac{du}{2}$. ما بقي ولا $x$.'),
        (r'=\frac12\cdot\frac{u^{6}}{6}', [('integrate(u**5,u)/2', 'Rational(1,2)*u**6/6')], 'نكامل بقاعدة القوة: نزيد الأس 1، ونقسم على 6.'),
        (r'=\frac{u^{6}}{12}', [('Rational(1,2)*u**6/6', 'u**6/12')], r'نضرب المقامين: $2\cdot6=12$.'),
        (r'=\frac{\left(x^{2}+1\right)^{6}}{12}+C', [('diff((x**2+1)**6/12,x)', 'x*(x**2+1)**5')], 'نرجع $u=x^2+1$، ونزيد $+C$.')],
        check=r'اشتق الجواب: $\frac{6(x^2+1)^5\cdot2x}{12}=x(x^2+1)^5$ ✓ رجع السؤال.')
    U.example('ليش نقسم على الرقم اللي قدام $x$؟', r'\int\cos3x\,dx', [
        (r'u=3x,\qquad du=3\,dx', [('diff(3*x,x)', '3')], 'نختار اللي داخل cos، ونشتقه.'),
        (r'dx=\frac{du}{3}', [('1/diff(3*x,x)', 'Rational(1,3)')], 'نقسم على 3، عشان نعوّض مكان $dx$.'),
        (r'\int\cos3x\,dx=\frac13\int\cos u\,du', [('cos(3*x)', 'Rational(1,3)*cos(3*x)*diff(3*x,x)')], r'نعوّض. والـ $\frac13$ تطلع برّا.'),
        (r'=\frac13\sin u', [('integrate(cos(u),u)/3', 'sin(u)/3')], 'تكامل cos هو sin.'),
        (r'=\frac13\sin3x+C', [('diff(sin(3*x)/3,x)', 'cos(3*x)')], r'نرجع $u=3x$. ومن هنا جا «نقسم على الرقم اللي قدام $x$» في الجدول.')])
    U.example('$x$ فوق، و $x^2$ تحت الجذر (يتكرر في 4.2 و5.1)', r'\int\frac{x\,dx}{\sqrt{x^{2}+9}}', [
        (r'w=x^{2}+9,\qquad dw=2x\,dx', [('diff(x**2+9,x)', '2*x')], 'نسمّي اللي تحت الجذر $w$، ونشتقه. مشتقته $2x$، وعندنا $x$ فوق.'),
        (r'x\,dx=\frac{dw}{2}', [('diff(x**2+9,x)/2', 'x')], 'رقم التعديل: فوق $x$ بس، فنقسم على 2.'),
        (r'=\frac12\int w^{-1/2}dw', [('x/sqrt(x**2+9)', 'Rational(1,2)*(x**2+9)**Rational(-1,2)*diff(x**2+9,x)')],
         r'نعوّض. والجذر في المقام يصير أس $-\frac12$.'),
        (r'=\frac12\cdot\frac{w^{1/2}}{1/2}', [('integrate(w**Rational(-1,2),w)/2', 'Rational(1,2)*w**Rational(1,2)/Rational(1,2)')],
         r'قاعدة القوة: $-\frac12+1=\frac12$، ونقسم على $\frac12$.'),
        (r'=w^{1/2}', [('Rational(1,2)*w**Rational(1,2)/Rational(1,2)', 'w**Rational(1,2)')], r'$\frac12$ تقسيم $\frac12$ يساوي 1.'),
        (r'=\sqrt{x^{2}+9}+C', [('diff(sqrt(x**2+9),x)', 'x/sqrt(x**2+9)')], 'نرجع $w=x^2+9$، والأس $\\frac12$ هو الجذر.')])
    U.example('ln يطلع لما المقام $x$ ورقم، مثل $2x+5$', r'\int\frac{dx}{2x+5}', [
        (r'u=2x+5,\qquad du=2\,dx', [('diff(2*x+5,x)', '2')], 'نسمّي المقام $u$، ونشتقه.'),
        (r'dx=\frac{du}{2}', [('1/diff(2*x+5,x)', 'Rational(1,2)')], 'نقسم على 2، عشان نعوّض مكان $dx$.'),
        (r'=\frac12\int\frac{du}{u}', [('1/(2*x+5)', 'Rational(1,2)*diff(2*x+5,x)/(2*x+5)')], r'نعوّض. والـ $\frac12$ تطلع برّا.'),
        (r'=\frac12\ln|u|', [('diff(log(u)/2,u)', '1/(2*u)')], r'تكامل $\frac1u$ هو $\ln|u|$.'),
        (r'=\frac12\ln|2x+5|+C', [('diff(log(2*x+5)/2,x)', '1/(2*x+5)', 't')], 'نرجع $u=2x+5$.')])
    U.add('trap', '⚠️ الفخ', ul([rich('لا تكامل وفيه $x$ و $u$ مع بعض. لازم كل $x$ تختفي أول.'),
                                rich('لا تنسى الرقم اللي يطلع من $du$، مثل $\\frac12$ أو $\\frac13$.'),
                                rich('$\\int x^2dx$ مو $\\frac{x^2}{2}$. الأس يزيد 1، فيصير $\\frac{x^3}{3}$.'),
                                rich('لا تنسى ترجع لـ $x$، وتزيد $+C$.')]))
    U.add('ok', '✔ تأكد', p(rich('اشتق جوابك. إذا رجع اللي داخل التكامل، فجوابك صح.')))
    U.drill('1', 'G-56', 'G', 'كامل كل حد لحاله بقاعدة القوة.',
            first=r'\int3x^{2}dx-\int4x\,dx+\int x^{-2}dx', claims=[('3*x**2-4*x+x**(-2)', '3*x**2-4*x+1/x**2')],
            sol_rows=[('tex', r'\int3x^{2}dx=3\cdot\frac{x^{3}}{3}=x^{3}', [('integrate(3*x**2,x)', 'x**3')],
                       'قاعدة القوة: الأس يصير 3، ونقسم على 3. والـ 3 اللي قدام تروح مع الـ 3 اللي تحت.'),
                      ('tex', r'\int4x\,dx=4\cdot\frac{x^{2}}{2}=2x^{2}', [('integrate(4*x,x)', '2*x**2')],
                       r'الأس يصير 2، ونقسم على 2. و $\frac42=2$.'),
                      ('tex', r'\int x^{-2}dx=\frac{x^{-1}}{-1}=-\frac1x', [('integrate(x**(-2),x)', '-1/x')],
                       'الأس يصير $-1$، ونقسم على $-1$. والأس السالب يعني مقلوب.'),
                      ('line', 'x**3-2*x**2-1/x', 'نجمع الحدود الثلاثة بإشاراتها، ونزيد $+C$.')])
    U.drill('2', 'G-57', 'P', 'نسمّي الأس $u$، ونقسم على $-2$.',
            sol_rows=[('sub', '-2*x', '-2', 'الأس $-2x$. نسمّيه $u$، ونشتقه.'),
                      ('tex', r'dx=-\frac{du}{2}', [('1/diff(-2*x,x)', '-Rational(1,2)')], 'نقسم على $-2$، عشان نعوّض مكان $dx$.'),
                      ('tex', r'\int e^{-2x}dx=-\frac12\int e^{u}du', [('exp(-2*x)', '-Rational(1,2)*exp(-2*x)*diff(-2*x,x)')],
                       r'نعوّض. والـ $-\frac12$ تطلع برّا التكامل.'),
                      ('tex', r'=-\frac12e^{u}', [('-integrate(exp(u),u)/2', '-exp(u)/2')], 'تكامل $e^u$ هو $e^u$ نفسها.'),
                      ('line', '-exp(-2*x)/2', 'نرجع $u=-2x$.')])
    U.drill('3', 'M-08', 'P', 'نسمّي اللي داخل القوس $u$، ونقسم على 4.',
            sol_rows=[('sub', 'exp(4*x)+3', '4*exp(4*x)',
                       'داخل القوس $e^{4x}+3$، ومشتقته $4e^{4x}$. وفوق عندنا $e^{4x}$، فنسمّي اللي داخل القوس $u$.'),
                      ('tex', r'e^{4x}dx=\frac{du}{4}', [('diff(exp(4*x)+3,x)/4', 'exp(4*x)')],
                       'هنا التريك: رقم التعديل. فوق $e^{4x}$ بس، مو $4e^{4x}$. فنقسم على 4.'),
                      ('tex', r'\int\frac{e^{4x}}{\left(e^{4x}+3\right)^{3}}dx=\frac14\int\frac{du}{u^{3}}',
                       [('exp(4*x)/(exp(4*x)+3)**3', 'Rational(1,4)*diff(exp(4*x)+3,x)/(exp(4*x)+3)**3')], 'نعوّض. ما بقي ولا $x$.'),
                      ('tex', r'=\frac14\int u^{-3}du', [('1/u**3', 'u**(-3)')], 'نكتب الكسر بأس سالب، عشان نستعمل قاعدة القوة.'),
                      ('tex', r'=\frac14\cdot\frac{u^{-2}}{-2}', [('integrate(u**(-3),u)/4', 'Rational(1,4)*u**(-2)/(-2)')],
                       'قاعدة القوة: الأس يصير $-2$، ونقسم على $-2$.'),
                      ('tex', r'=-\frac{1}{8u^{2}}', [('Rational(1,4)*u**(-2)/(-2)', '-1/(8*u**2)')],
                       r'نضرب: $\frac14\cdot\frac{1}{-2}=-\frac18$. والأس السالب يرجع مقام.'),
                      ('line', '-1/(8*(exp(4*x)+3)**2)', 'نرجع $u=e^{4x}+3$.')])
    U.drill('4', 'M-09', 'I', 'مشتقة المقام 3 مرات البسط.',
            sol_rows=[('sub', 'x**3+3*x+7', '3*x**2+3', 'المقام $x^3+3x+7$، ومشتقته $3x^2+3$. وهذي قريبة من البسط، فنسمّي المقام $u$.'),
                      ('tex', r'3x^{2}+3=3\left(x^{2}+1\right)', [('3*x**2+3', '3*(x**2+1)')], 'نطلّع 3 عامل مشترك. يطلع البسط $x^2+1$ بالضبط.'),
                      ('tex', r'\left(x^{2}+1\right)dx=\frac{du}{3}', [('diff(x**3+3*x+7,x)/3', 'x**2+1')],
                       'هنا التريك: رقم التعديل. البسط ناقصه 3، فنقسم على 3.'),
                      ('tex', r'\int\frac{x^{2}+1}{x^{3}+3x+7}dx=\frac13\int\frac{du}{u}',
                       [('(x**2+1)/(x**3+3*x+7)', 'Rational(1,3)*diff(x**3+3*x+7,x)/(x**3+3*x+7)')], r'نعوّض. والـ $\frac13$ تطلع برّا.'),
                      ('tex', r'=\frac13\ln|u|', [('diff(log(u)/3,u)', '1/(3*u)')], r'تكامل $\frac1u$ هو $\ln|u|$.'),
                      ('line', 'log(Abs(x**3+3*x+7))/3', r'نرجع $u=x^3+3x+7$. ونخلي $|\,|$، لأن المقام ممكن يصير سالب.')])
    U.drill('5', 'G-60', 'I', 'نسمّي المقام $u$، ونقسم على 3.',
            sol_rows=[('sub', '3*x+2', '3', 'نسمّي المقام $u$، ونشتقه.'),
                      ('tex', r'dx=\frac{du}{3}', [('1/diff(3*x+2,x)', 'Rational(1,3)')], 'نقسم على 3، عشان نعوّض مكان $dx$.'),
                      ('tex', r'\int\frac{dx}{3x+2}=\frac13\int\frac{du}{u}', [('1/(3*x+2)', 'Rational(1,3)*diff(3*x+2,x)/(3*x+2)')],
                       r'نعوّض. والـ $\frac13$ تطلع برّا.'),
                      ('tex', r'=\frac13\ln|u|', [('diff(log(u)/3,u)', '1/(3*u)')], r'تكامل $\frac1u$ هو $\ln|u|$.'),
                      ('line', 'log(Abs(3*x+2))/3', 'نرجع $u=3x+2$.')])
    return U


# ================================================================ before 5.1
def part_b1():
    U = PreUnit('P-B1', 'ب1', 'مشتقات تحتاجها التجزئة: ln والمثلثية العكسية (درس 3.4)', 'pre51', 'مذكرة د. طارق: درس 3.4، ص43–48، ودرس 3.1')
    U.why('في التجزئة نشتق $u$، وغالبًا $u$ هي ln أو دالة عكسية. فلازم تعرف مشتقاتها من درس 3.4، وتعرف تكاملاتها اللي تطلع في آخر الحل.',
          [('U-P3', 14), ('U-P4', 15), ('U-P6', 17), ('U-P7', 18)])
    U.explain([
        ('<b>ln</b>: مشتقتها مشتقة اللي داخل، مقسومة على اللي داخل.',
         r'\frac{d}{dx}\ln|x|=\frac1x,\qquad \frac{d}{dx}\ln\left|x^{2}+1\right|=\frac{2x}{x^{2}+1}',
         [('diff(log(x),x)', '1/x', 't'), ('diff(log(x**2+1),x)', '2*x/(x**2+1)')]),
        ('الرقم المضروب داخل ln يختفي من المشتقة، لأنه ينختصر فوق وتحت.', r'\frac{d}{dx}\ln|2x|=\frac{2}{2x}=\frac1x',
         [('diff(log(2*x),x)', '1/x', 't'), ('2/(2*x)', '1/x')]),
        (r'<b>$\sin^{-1}x$</b> هي الزاوية اللي sin حقها يساوي $x$. مشتقتها كسر تحته جذر.',
         r'\frac{d}{dx}\sin^{-1}x=\frac{1}{\sqrt{1-x^{2}}}', [('diff(asin(x),x)', '1/sqrt(1-x**2)')]),
        (r'<b>$\tan^{-1}x$</b> مشتقتها كسر بدون جذر.', r'\frac{d}{dx}\tan^{-1}x=\frac{1}{1+x^{2}}', [('diff(atan(x),x)', '1/(1+x**2)')]),
        ('لا تخلط مع درس 4.2. الشكل نفسه تقريبًا، لكن الإشارة تحت الجذر تختلف.',
         r'\frac{d}{dx}\sin^{-1}x=\frac{1}{\sqrt{1-x^{2}}},\qquad \frac{d}{dx}\sinh^{-1}x=\frac{1}{\sqrt{x^{2}+1}}',
         [('diff(asin(x),x)', '1/sqrt(1-x**2)'), ('diff(asinh(x),x)', '1/sqrt(x**2+1)')]),
        ('ومع دالة داخلها: نفس قاعدة السلسلة. نضرب في مشتقة اللي داخل.',
         r'\frac{d}{dx}\tan^{-1}(3x)=\frac{1}{1+(3x)^{2}}\cdot3=\frac{3}{1+9x^{2}}',
         [('diff(atan(3*x),x)', '3/(1+(3*x)**2)'), ('3/(1+(3*x)**2)', '3/(1+9*x**2)')]),
        (r'وفي آخر التجزئة يطلع لك تكامل من 3.4. رقم زائد $x^2$ بدون جذر يعطي $\tan^{-1}$. تحتاجه في النوع 17.',
         r'\int\frac{dx}{1+x^{2}}=\tan^{-1}x+C', [('diff(atan(x),x)', '1/(1+x**2)')]),
        (r'لكن إذا فوق $x$، فهو تعويض عادي ويطلع ln. لأن مشتقة $1+x^2$ هي $2x$.',
         r'\int\frac{x\,dx}{1+x^{2}}=\frac12\ln\left(1+x^{2}\right)+C', [('diff(log(1+x**2)/2,x)', 'x/(1+x**2)')])])
    d = [formula('log(Abs(u))', '1/u', 'diff', branches=('t', '-t'), uprime=True, label='P-B1 ln'),
         formula('asin(u)', '1/sqrt(1-u**2)', 'diff', branches=('t/(1+t)', '-t/(1+t)'), uprime=True, label='P-B1 asin'),
         formula('acos(u)', '-1/sqrt(1-u**2)', 'diff', branches=('t/(1+t)', '-t/(1+t)'), uprime=True, label='P-B1 acos'),
         formula('atan(u)', '1/(1+u**2)', 'diff', branches=('x',), uprime=True, label='P-B1 atan'),
         formula('asec(u)', '1/(u*sqrt(u**2-1))', 'diff', branches=('1+t',), uprime=True, label='P-B1 asec (u > 1)')]
    i = [formula('1/sqrt(a**2-u**2)', 'asin(u/a)', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='P-B1 int asin'),
         formula('1/(a**2+u**2)', 'atan(u/a)/a', branches=('x',), pos=('a',), label='P-B1 int atan'),
         formula('1/(u*sqrt(u**2-a**2))', 'asec(u/a)/a', branches=('a+t',), pos=('a',), label='P-B1 int asec (u > a)')]
    U.add('short', '📐 القانون: مشتقات الدوال العكسية وتكاملاتها', table(['المشتقة', 'تساوي'], [_row(z) for z in d], 'formula compact')
          + p(rich(r"في الجدول: $u'$ مشتقة اللي داخل الدالة. وقانون $\sec^{-1}$ مكتوب لـ $u>1$، مثل مذكرة د. طارق."), 'small')
          + table(['التكامل', 'الجواب (+C)', 'الشرط'], [_row(i[0], mi('|u|<a')), _row(i[1], 'كل ' + mi('u')), _row(i[2], mi('u>a'))], 'formula compact')
          + p(rich('في جدول التكامل: $a$ رقم موجب، و $u$ اللي داخل.'), 'small')
          + tricks([(r'مشتقة أي دالة عكسية كسر، وفوقه مشتقة اللي داخل. مثال: $\left(\tan^{-1}4x\right)^{\prime}=\frac{4}{1+16x^2}$.',
                     [('diff(atan(4*x),x)', '4/(1+16*x**2)')])], 'P-B1'))
    SHEET['inv'] = (table(['المشتقة', 'تساوي'], [_row(z) for z in d[1:]], 'formula compact')
                    + table(['التكامل', 'الجواب (+C)'], [_row(z) for z in i], 'formula compact'))
    cmp_rows = [[mi(r'\sqrt{a^{2}-u^{2}}'), mi(r'\sin^{-1}\frac{u}{a}'), '—'],
                [mi(r'\sqrt{u^{2}+a^{2}}'), '—', mi(r'\sinh^{-1}\frac{u}{a}')],
                [mi(r'\sqrt{u^{2}-a^{2}}'), '—', mi(r'\cosh^{-1}\frac{u}{a}')],
                [mi(r'a^{2}+u^{2}') + ' (بدون جذر)', mi(r'\frac1a\tan^{-1}\frac{u}{a}'), '—'],
                [mi(r'a^{2}-u^{2}') + ' (بدون جذر)', '—', mi(r'\frac1a\tanh^{-1}') + ' أو ' + mi(r'\coth^{-1}')]]
    U.add('short', '📐 لا تخلط: 3.4 أم 4.2؟ شكل المقام يقرر',
          table(['في المقام', '3.4 مثلثية عكسية', '4.2 زائدية عكسية'], cmp_rows, 'formula compact')
          + p(rich('مع الجذر: رقم ناقص $u^2$ يعني 3.4، وغيره يعني 4.2. وبدون جذر: زائد يعني 3.4، وناقص يعني 4.2.'), 'small'))
    U.example('أوجد المشتقة', r'y=\tan^{-1}\left(x^{2}\right)', [
        (r"u=x^{2},\qquad u'=2x", [('diff(x**2,x)', '2*x')], r'داخل $\tan^{-1}$ فيه $x^2$، مو $x$ بس. نسمّيه $u$، ونشتقه.'),
        (r"y'=\frac{u'}{1+u^{2}}", [('diff(atan(x**2),x)', 'diff(x**2,x)/(1+(x**2)**2)')],
         r"قانون $\tan^{-1}$: مشتقة اللي داخل، على 1 زائد اللي داخل تربيع."),
        (r"y'=\frac{2x}{1+\left(x^{2}\right)^{2}}", [('diff(atan(x**2),x)', '2*x/(1+(x**2)**2)')], "نعوّض $u=x^2$ و $u'=2x$."),
        (r"y'=\frac{2x}{1+x^{4}}", [('diff(atan(x**2),x)', '2*x/(1+x**4)')], r'قوة فوق قوة، فنضرب الأسس: $(x^2)^2=x^4$.')])
    U.example('أوجد المشتقة (sec⁻¹، لـ x > ⅓)', r'y=\sec^{-1}(3x)', [
        (r"u=3x,\qquad u'=3", [('diff(3*x,x)', '3')], r'داخل $\sec^{-1}$ فيه $3x$. نسمّيه $u$، ونشتقه.'),
        (r"y'=\frac{u'}{u\sqrt{u^{2}-1}}", [('diff(asec(3*x),x)', 'diff(3*x,x)/(3*x*sqrt((3*x)**2-1))', '1/3+t')],
         r"قانون $\sec^{-1}$: مشتقة اللي داخل، على اللي داخل ضرب جذر (اللي داخل تربيع ناقص 1)."),
        (r"y'=\frac{3}{3x\sqrt{9x^{2}-1}}", [('diff(asec(3*x),x)', '3/(3*x*sqrt(9*x**2-1))', '1/3+t')],
         r"نعوّض $u=3x$ و $u'=3$. والرقم بعد يتربّع: $(3x)^2=9x^2$."),
        (r"y'=\frac{1}{x\sqrt{9x^{2}-1}}", [('diff(asec(3*x),x)', '1/(x*sqrt(9*x**2-1))', '1/3+t')], 'نختصر 3 فوق مع 3 تحت.')])
    U.example('أوجد المشتقة (ضرب، مثل اللي يطلع في النوع 18)', r'y=x^{2}\tan^{-1}x', [
        (r"f=x^{2},\qquad f'=2x", [('diff(x**2,x)', '2*x')], 'دالتين مضروبتين، فنستعمل قاعدة الضرب. نسمّي الأولى $f$، ونشتقها.'),
        (r"g=\tan^{-1}x,\qquad g'=\frac{1}{1+x^{2}}", [('diff(atan(x),x)', '1/(1+x**2)')], r'نسمّي الثانية $g$. مشتقتها من قانون $\tan^{-1}$.'),
        (r"y'=f'g+fg'=2x\tan^{-1}x+x^{2}\cdot\frac{1}{1+x^{2}}", [('diff(x**2*atan(x),x)', '2*x*atan(x)+x**2*(1/(1+x**2))')],
         'قاعدة الضرب: مشتقة الأولى × الثانية، زائد الأولى × مشتقة الثانية.'),
        (r"y'=2x\tan^{-1}x+\frac{x^{2}}{1+x^{2}}", [('diff(x**2*atan(x),x)', '2*x*atan(x)+x**2/(1+x**2)')], r'نضرب $x^2$ في الكسر، فتصير فوق.')])
    U.example('كامل (من درس 3.4)', r'\int\frac{dx}{9+x^{2}}', [
        (r'9+x^{2}=3^{2}+x^{2}', [('9+x**2', '3**2+x**2')],
         r'تحت رقم زائد $x^2$، وما فيه جذر. نكتب 9 كمربع عشان نعرف $a$: هنا $a=3$.'),
        (r'\int\frac{dx}{3^{2}+x^{2}}=\frac13\tan^{-1}\frac{x}{3}+C', [('diff(atan(x/3)/3,x)', '1/(9+x**2)')],
         r'القانون: $\int\frac{du}{a^2+u^2}=\frac1a\tan^{-1}\frac ua$، وهنا $u=x$ و $a=3$.')],
        check=r'اشتق الجواب: $\frac13\cdot\frac{1/3}{1+x^2/9}=\frac{1}{9+x^2}$ ✓ رجع السؤال.')
    arith('', [('Rational(1,3)*Rational(1,3)/(1+x**2/9)', '1/(9+x**2)')], 'P-B1 check')
    U.add('trap', '⚠️ الفخ', ul([rich(r'$\sin^{-1}x$ دالة عكسية، مو $\frac{1}{\sin x}$. هذي اسمها $\csc x$.'),
                                rich(r'$a^2+u^2$ بدون جذر يعطي $\tan^{-1}$ من 3.4. و $a^2-u^2$ بدون جذر يعطي $\tanh^{-1}$ من 4.2. إشارة وحدة تفرق.'),
                                rich('لا تنسى مشتقة اللي داخل فوق الكسر.')]))
    U.add('ok', '✔ تأكد', p(rich('مشتقات الدوال العكسية كلها كسور، وفوقها مشتقة اللي داخل. إذا جوابك ما فيه كسر، ارجع للجدول.')))
    U.drill('1', 'G-61', 'G', r'قانون $\sin^{-1}$، واللي داخل $2x$.', first=r"u=2x,\quad u'=2", claims=[('diff(2*x,x)', '2')],
            sol_rows=[('tex', r"y'=\frac{u'}{\sqrt{1-u^{2}}}", [('diff(asin(2*x),x)', 'diff(2*x,x)/sqrt(1-(2*x)**2)', 't/(2*(1+t))')],
                       r'قانون $\sin^{-1}$: مشتقة اللي داخل، على جذر (1 ناقص اللي داخل تربيع).'),
                      ('tex', r"y'=\frac{2}{\sqrt{1-(2x)^{2}}}", [('diff(asin(2*x),x)', '2/sqrt(1-(2*x)**2)', 't/(2*(1+t))')],
                       "نعوّض $u=2x$ و $u'=2$."),
                      ('line', '2/sqrt(1-4*x**2)', r'الرقم بعد يتربّع: $(2x)^2=4x^2$.')])
    U.drill('2', 'M-02', 'P', r'برّا ln، واللي داخلها فيه $\tan^{-1}2x$.',
            sol_rows=[('tex', r'u=x^{3}+\tan^{-1}2x', [('x**3+atan(2*x)', 'x**3+atan(2*x)')],
                       r'برّا ln، وداخلها $x^3+\tan^{-1}2x$. نسمّي اللي داخل $u$.'),
                      ('tex', r"\left(\tan^{-1}2x\right)'=\frac{2}{1+4x^{2}}", [('diff(atan(2*x),x)', '2/(1+4*x**2)')],
                       r'قانون $\tan^{-1}$ مع $2x$: فوق مشتقة $2x$ وهي 2، وتحت $(2x)^2=4x^2$.'),
                      ('tex', r"u'=3x^{2}+\frac{2}{1+4x^{2}}", [('diff(x**3+atan(2*x),x)', '3*x**2+2/(1+4*x**2)')],
                       r'نشتق $u$ حد حد. مشتقة $x^3$ هي $3x^2$.'),
                      ('tex', r"y'=\frac{u'}{u}", [('diff(log(x**3+atan(2*x)),x)', 'diff(x**3+atan(2*x),x)/(x**3+atan(2*x))', 't')],
                       'قانون ln: مشتقة اللي داخل، مقسومة على اللي داخل.'),
                      ('line', '(3*x**2+2/(1+4*x**2))/(x**3+atan(2*x))', "نعوّض $u$ و $u'$.")])
    U.drill('3', 'M-01', 'P', r'دالتين مضروبتين: $\sqrt x$ في $\ln|x|$.',
            sol_rows=[('tex', r"f=\sqrt{x},\quad f'=\frac{1}{2\sqrt{x}}", [('diff(sqrt(x),x)', '1/(2*sqrt(x))')],
                       'دالتين مضروبتين، فنستعمل قاعدة الضرب. نسمّي الأولى $f$. مشتقة الجذر: 1 على ضعف الجذر.'),
                      ('tex', r"g=\ln|x|,\quad g'=\frac1x", [('diff(log(x),x)', '1/x', 't')], r'نسمّي الثانية $g$. مشتقة $\ln|x|$ هي $\frac1x$.'),
                      ('tex', r"y'=f'g+fg'=\frac{\ln|x|}{2\sqrt{x}}+\sqrt{x}\cdot\frac1x",
                       [('diff(sqrt(x)*log(x),x)', 'log(x)/(2*sqrt(x))+sqrt(x)/x', 't')],
                       'قاعدة الضرب: مشتقة الأولى × الثانية، زائد الأولى × مشتقة الثانية.'),
                      ('tex', r'\frac{\sqrt{x}}{x}=\frac{1}{\sqrt{x}}', [('sqrt(x)/x', '1/sqrt(x)', 't')],
                       r'نبسّط الحد الثاني: $x=\sqrt x\cdot\sqrt x$، فنختصر جذر فوق مع جذر تحت.'),
                      ('line', 'log(Abs(x))/(2*sqrt(x))+1/sqrt(x)', 'نكتب الجواب بعد التبسيط.')])
    U.drill('4', 'M-27', 'I', r'$x^6=(x^3)^2$، فنسمّي $x^3$ هو $u$، ثم قانون $\tan^{-1}$.',
            sol_rows=[('tex', r'9+x^{6}=3^{2}+\left(x^{3}\right)^{2}', [('9+x**6', '3**2+(x**3)**2')],
                       r'تحت رقم زائد $x^6$، وما فيه جذر. نكتب الاثنين كمربعات: $9=3^2$ و $x^6=(x^3)^2$.'),
                      ('sub', 'x**3', '3*x**2', r'اللي داخل المربع $x^3$، ومشتقته $3x^2$. وفوق عندنا $x^2$، فنسمّي $x^3$ هو $u$.'),
                      ('tex', r'x^{2}\,dx=\frac{du}{3}', [('diff(x**3,x)/3', 'x**2')], r'فوق $x^2\,dx$ بس، مو $3x^2\,dx$. فنقسم على 3.'),
                      ('tex', r'\int\frac{x^{2}\,dx}{9+x^{6}}=\frac13\int\frac{du}{3^{2}+u^{2}}',
                       [('x**2/(9+x**6)', 'Rational(1,3)*diff(x**3,x)/(3**2+(x**3)**2)')], r'نعوّض. والـ $\frac13$ تطلع برّا التكامل.'),
                      ('tex', r'=\frac13\cdot\frac13\tan^{-1}\frac{u}{3}', [('diff(atan(u/3)/3,u)', '1/(9+u**2)')],
                       r'القانون: $\int\frac{du}{a^2+u^2}=\frac1a\tan^{-1}\frac ua$، وهنا $a=3$.'),
                      ('tex', r'=\frac19\tan^{-1}\frac{u}{3}', [('Rational(1,3)*Rational(1,3)', 'Rational(1,9)')], r'نضرب الرقمين: $\frac13\cdot\frac13=\frac19$.'),
                      ('line', 'atan(x**3/3)/9', 'نرجع $u=x^3$.')])
    U.drill('5', 'M-28', 'I', r'دالتين مضروبتين: قاعدة الضرب. ومع $\sin^{-1}5x$ نضرب في 5.',
            sol_rows=[('tex', r"f=\sqrt{x},\quad f'=\frac{1}{2\sqrt{x}}", [('diff(sqrt(x),x)', '1/(2*sqrt(x))')],
                       'دالتين مضروبتين، فنستعمل قاعدة الضرب. نسمّي الأولى $f$. مشتقة الجذر: 1 على ضعف الجذر.'),
                      ('tex', r"g=\sin^{-1}5x,\quad g'=\frac{5}{\sqrt{1-(5x)^{2}}}", [('diff(asin(5*x),x)', '5/sqrt(1-(5*x)**2)', 't/(5*(1+t))')],
                       r'نسمّي الثانية $g$. قانون $\sin^{-1}$ مع $5x$، وفوق مشتقة $5x$ وهي 5.'),
                      ('tex', r"g'=\frac{5}{\sqrt{1-25x^{2}}}", [('5/sqrt(1-(5*x)**2)', '5/sqrt(1-25*x**2)')], r'الرقم بعد يتربّع: $(5x)^2=25x^2$.'),
                      ('tex', r"y'=f'g+fg'=\frac{\sin^{-1}5x}{2\sqrt{x}}+\sqrt{x}\cdot\frac{5}{\sqrt{1-25x^{2}}}",
                       [('diff(sqrt(x)*asin(5*x),x)', 'asin(5*x)/(2*sqrt(x))+sqrt(x)*5/sqrt(1-25*x**2)', 't/(5*(1+t))')],
                       'قاعدة الضرب: مشتقة الأولى × الثانية، زائد الأولى × مشتقة الثانية.'),
                      ('line', 'asin(5*x)/(2*sqrt(x))+5*sqrt(x)/sqrt(1-25*x**2)', r'نكتب $5\sqrt x$ فوق في الكسر الثاني.')])
    return U


def part_b2():
    U = PreUnit('P-B2', 'ب2', 'تكاملات تحتاجها التجزئة', 'pre51', 'مذكرة د. طارق: دروس 2.3 و2.4 و3.1 و3.2، وص52–53')
    U.why('في التجزئة نكامل $dv$ عشان نطلّع $v$، وفي الآخر يبقى تكامل ثاني. هذي التكاملات لازم تطلع صح وبإشارتها، وإلا يخرب الحل كله.',
          [('U-P1', 12), ('U-P2', 13), ('U-P6', 17), ('U-P10', 21)])
    U.explain([
        (r'<b>$e$ مع رقم قدام $x$</b>: الجواب نفسها، مقسومة على الرقم اللي قدام $x$. لأن مشتقة $4x$ هي 4.',
         r'\int e^{4x}dx=\frac{e^{4x}}{4}+C', [('diff(exp(4*x)/4,x)', 'exp(4*x)')]),
        (r'ومع سالب قدام $x$: نقسم على $-1$، فيطلع سالب.', r'\int e^{-x}dx=-e^{-x}+C', [('diff(-exp(-x),x)', 'exp(-x)')]),
        ('<b>sin و cos</b>: تكامل sin فيه سالب، وتكامل cos بدون سالب. ونقسم على الرقم اللي قدام $x$.',
         r'\int\sin3x\,dx=-\frac{\cos3x}{3}+C,\qquad \int\cos3x\,dx=\frac{\sin3x}{3}+C',
         [('diff(-cos(3*x)/3,x)', 'sin(3*x)'), ('diff(sin(3*x)/3,x)', 'cos(3*x)')]),
        ('<b>sinh و cosh</b>: بدون سالب أبد.', r'\int\sinh2x\,dx=\frac{\cosh2x}{2}+C,\qquad \int\cosh x\,dx=\sinh x+C',
         [('diff(cosh(2*x)/2,x)', 'sinh(2*x)'), ('diff(sinh(x),x)', 'cosh(x)')]),
        ('<b>القوة السالبة أو الكسرية</b>: نزيد الأس 1، ونقسم على الأس الجديد. تجي مع ln في النوع 14.',
         r'\int x^{-3}dx=\frac{x^{-2}}{-2}=-\frac{1}{2x^{2}}+C', [('diff(-1/(2*x**2),x)', 'x**(-3)')]),
        (r'<b>$x$ فوق، وتحت $x^2$ ورقم</b>: نسمّي اللي تحت $w$. مشتقته فيها $x$، فيصير تعويض عادي. تحتاجه في النوع 17.',
         r'\int\frac{x\,dx}{\sqrt{1-x^{2}}}=-\sqrt{1-x^{2}}+C,\qquad \int\frac{x\,dx}{1+x^{2}}=\frac12\ln\left(1+x^{2}\right)+C',
         [('diff(-sqrt(1-x**2),x)', 'x/sqrt(1-x**2)', 't/(1+t)'), ('diff(log(1+x**2)/2,x)', 'x/(1+x**2)')])])
    m = [formula('x/sqrt(a**2+x**2)', 'sqrt(a**2+x**2)', var='x', branches=('t', '-t'), pos=('a',), label='P-B2 micro +'),
         formula('x/sqrt(a**2-x**2)', '-sqrt(a**2-x**2)', var='x', branches=('a*t/(1+t)',), pos=('a',), label='P-B2 micro -'),
         formula('x/(a**2+x**2)', 'log(a**2+x**2)/2', var='x', branches=('t',), pos=('a',), label='P-B2 micro ln +'),
         formula('x/(a**2-x**2)', '-log(Abs(a**2-x**2))/2', var='x', branches=('a*t/(1+t)', 'a+t'), pos=('a',), label='P-B2 micro ln -')]
    U.add('short', '📐 القانون: أربعة تكاملات تنحل بتعويض', table(['التكامل', 'الجواب (+C)'], [_row(z) for z in m], 'formula compact')
          + p(rich('في الجدول: $a$ أي رقم موجب. والسالب يطلع مع $a^2-x^2$، لأن مشتقتها $-2x$.'), 'small')
          + tricks([(r'رقم التعديل: $w=1-x^2$ يعطي $dw=-2x\,dx$، والسؤال فيه $x\,dx$ بس. فـ $x\,dx=-\frac12\,dw$، ومن هنا يجي السالب.',
                     [('diff(1-x**2,x)/(-2)', 'x')])], 'P-B2'))
    U.example('كامل (بالتعويض، عشان تشوف من وين يجي السالب)', r'\int\sin3x\,dx', [
        (r'u=3x,\qquad du=3\,dx', [('diff(3*x,x)', '3')], 'sin داخلها $3x$. نسمّيه $u$، ونشتقه.'),
        (r'dx=\frac{du}{3}', [('1/diff(3*x,x)', 'Rational(1,3)')], 'نقسم على 3، عشان نعوّض مكان $dx$.'),
        (r'\int\sin3x\,dx=\frac13\int\sin u\,du', [('sin(3*x)', 'Rational(1,3)*sin(3*x)*diff(3*x,x)')], r'نعوّض. والـ $\frac13$ تطلع برّا التكامل.'),
        (r'=\frac13\left(-\cos u\right)', [('integrate(sin(u),u)/3', '-cos(u)/3')], 'تكامل sin هو سالب cos، لأن مشتقة cos فيها سالب.'),
        (r'=-\frac13\cos u', [('Rational(1,3)*(-cos(u))', '-cos(u)/3')], 'السالب يطلع قدّام.'),
        (r'=-\frac13\cos3x+C', [('diff(-cos(3*x)/3,x)', 'sin(3*x)')], 'نرجع $u=3x$.')])
    U.example('قوة سالبة', r'\int\frac{dx}{x^{3}}', [
        (r'\frac{1}{x^{3}}=x^{-3}', [('1/x**3', 'x**(-3)')], 'نكتب الكسر كأس سالب، عشان نستعمل قاعدة القوة.'),
        (r'\int x^{-3}dx=\frac{x^{-3+1}}{-3+1}', [('diff(x**(-2)/(-2),x)', 'x**(-3)')], 'قاعدة القوة: نزيد الأس 1، ونقسم على الأس الجديد.'),
        (r'=\frac{x^{-2}}{-2}', [('x**(-3+1)/(-3+1)', 'x**(-2)/(-2)')], 'نحسب الأس: $-3+1=-2$.'),
        (r'=-\frac{1}{2x^{2}}+C', [('x**(-2)/(-2)', '-1/(2*x**2)')], 'الأس السالب يعني مقلوب، والسالب يطلع قدّام.')])
    U.example('$x$ فوق جذر $1-x^2$ (يطلع في النوع 17 مع sin⁻¹)', r'\int\frac{x\,dx}{\sqrt{1-x^{2}}}', [
        (r'w=1-x^{2},\qquad dw=-2x\,dx', [('diff(1-x**2,x)', '-2*x')],
         r'اللي تحت الجذر مشتقته فيها $x$، و $x$ موجودة فوق. نسمّيه $w$، ونشتقه.'),
        (r'x\,dx=-\frac{dw}{2}', [('diff(1-x**2,x)/(-2)', 'x')], r'هنا التريك: فوق $x\,dx$ بس. فنقسم على $-2$، ومن هنا يجي السالب.'),
        (r'=-\frac12\int w^{-1/2}dw', [('x/sqrt(1-x**2)', '-Rational(1,2)*(1-x**2)**Rational(-1,2)*diff(1-x**2,x)', 't/(1+t)')],
         r'نعوّض. والجذر في المقام يصير أس $-\frac12$.'),
        (r'=-\frac12\cdot\frac{w^{1/2}}{1/2}', [('-integrate(w**Rational(-1,2),w)/2', '-Rational(1,2)*w**Rational(1,2)/Rational(1,2)')],
         r'قاعدة القوة: $-\frac12+1=\frac12$، ونقسم على $\frac12$.'),
        (r'=-w^{1/2}', [('-Rational(1,2)*w**Rational(1,2)/Rational(1,2)', '-w**Rational(1,2)')], r'$\frac12$ تقسيم $\frac12$ يساوي 1.'),
        (r'=-\sqrt{1-x^{2}}+C', [('diff(-sqrt(1-x**2),x)', 'x/sqrt(1-x**2)', 't/(1+t)')], r'نرجع $w=1-x^2$، والأس $\frac12$ هو الجذر.')])
    U.add('trap', '⚠️ الفخ', ul([rich(r'$\int\sin x\,dx=-\cos x$ بالسالب. لكن $\int\sinh x\,dx=+\cosh x$ بدون سالب.'),
                                rich(r'$\int e^{-x}dx=-e^{-x}$. نقسم على $-1$، فيطلع سالب.'),
                                rich(r'$\int x^{-1}dx$ ما تنفع معه قاعدة القوة، لأن الأس الجديد يصير صفر. جوابه $\ln|x|$.')]))
    U.add('ok', '✔ تأكد', p(rich('اشتق جوابك. أكثر غلط هنا في الإشارة، والاشتقاق يكشفه.')))
    U.drill('1', 'M-03', 'G', r'نسمّي الأس $u$، ونقسم على 8.', first=r'u=8x+1,\quad dx=\frac{du}{8}', claims=[('1/diff(8*x+1,x)', 'Rational(1,8)')],
            sol_rows=[('tex', r'\int e^{8x+1}dx=\frac18\int e^{u}\,du', [('exp(8*x+1)', 'Rational(1,8)*exp(8*x+1)*diff(8*x+1,x)')],
                       r'نعوّض. والـ $\frac18$ تطلع برّا التكامل.'),
                      ('tex', r'=\frac18e^{u}', [('integrate(exp(u),u)/8', 'exp(u)/8')], 'تكامل $e^u$ هو $e^u$ نفسها.'),
                      ('line', 'exp(8*x+1)/8', 'نرجع $u=8x+1$.')])
    U.drill('2', 'G-67', 'P', 'تكامل sinh هو cosh بدون سالب، ونقسم على 2.',
            sol_rows=[('sub', '2*x', '2', 'sinh داخلها $2x$. نسمّيه $u$، ونشتقه.'),
                      ('tex', r'dx=\frac{du}{2}', [('1/diff(2*x,x)', 'Rational(1,2)')], 'نقسم على 2، عشان نعوّض مكان $dx$.'),
                      ('tex', r'\int\sinh2x\,dx=\frac12\int\sinh u\,du', [('sinh(2*x)', 'Rational(1,2)*sinh(2*x)*diff(2*x,x)')],
                       r'نعوّض. والـ $\frac12$ تطلع برّا التكامل.'),
                      ('tex', r'=\frac12\cosh u', [('integrate(sinh(u),u)/2', 'cosh(u)/2')], 'تكامل sinh هو cosh، بدون سالب.'),
                      ('line', 'cosh(2*x)/2', 'نرجع $u=2x$.')])
    U.drill('3', 'G-68', 'P', r'نزيد الأس 1: $-4+1=-3$، ونقسم عليه.',
            sol_rows=[('tex', r'\int x^{-4}dx=\frac{x^{-4+1}}{-4+1}', [('diff(x**(-3)/(-3),x)', 'x**(-4)', 't')],
                       'قاعدة القوة: نزيد الأس 1، ونقسم على الأس الجديد.'),
                      ('tex', r'=\frac{x^{-3}}{-3}', [('x**(-4+1)/(-4+1)', 'x**(-3)/(-3)')], 'نحسب الأس: $-4+1=-3$.'),
                      ('line', '-1/(3*x**3)', 'الأس السالب يعني مقلوب، والسالب يطلع قدّام.')])
    U.drill('4', 'G-69', 'I', r'نسمّي اللي تحت الجذر $w$، ونقسم على 2.',
            sol_rows=[('sub', 'x**2-1', '2*x', r'اللي تحت الجذر مشتقته $2x$، و $x$ موجودة فوق. نسمّيه $w$.', 'w', '1+t'),
                      ('tex', r'x\,dx=\frac{dw}{2}', [('diff(x**2-1,x)/2', 'x')], r'فوق $x\,dx$ بس، مو $2x\,dx$. فنقسم على 2.'),
                      ('tex', r'\int\frac{x\,dx}{\sqrt{x^{2}-1}}=\frac12\int w^{-1/2}dw',
                       [('x/sqrt(x**2-1)', 'Rational(1,2)*(x**2-1)**Rational(-1,2)*diff(x**2-1,x)', '1+t')],
                       r'نعوّض. والجذر في المقام يصير أس $-\frac12$.'),
                      ('tex', r'=\frac12\cdot\frac{w^{1/2}}{1/2}', [('integrate(w**Rational(-1,2),w)/2', 'Rational(1,2)*w**Rational(1,2)/Rational(1,2)')],
                       r'قاعدة القوة: $-\frac12+1=\frac12$، ونقسم على $\frac12$.'),
                      ('tex', r'=w^{1/2}', [('Rational(1,2)*w**Rational(1,2)/Rational(1,2)', 'w**Rational(1,2)')], r'$\frac12$ تقسيم $\frac12$ يساوي 1.'),
                      ('line', 'sqrt(x**2-1)', r'نرجع $w=x^2-1$، والأس $\frac12$ هو الجذر.')])
    U.drill('5', 'M-04', 'I', 'مشتقة المقام ضعف البسط، فنقسم على 2.',
            sol_rows=[('sub', 'x**2+2*sin(x)', '2*x+2*cos(x)', r'المقام مشتقته $2x+2\cos x$، وهذي قريبة من البسط. نسمّي المقام $w$.', 'w', 't'),
                      ('tex', r'2x+2\cos x=2\left(x+\cos x\right)', [('2*x+2*cos(x)', '2*(x+cos(x))')],
                       r'نطلّع 2 عامل مشترك. يطلع البسط $x+\cos x$ بالضبط.'),
                      ('tex', r'\left(x+\cos x\right)dx=\frac{dw}{2}', [('diff(x**2+2*sin(x),x)/2', 'x+cos(x)')], 'البسط ناقصه 2، فنقسم على 2.'),
                      ('tex', r'\int\frac{x+\cos x}{x^{2}+2\sin x}dx=\frac12\int\frac{dw}{w}',
                       [('(x+cos(x))/(x**2+2*sin(x))', 'Rational(1,2)*diff(x**2+2*sin(x),x)/(x**2+2*sin(x))')], r'نعوّض. والـ $\frac12$ تطلع برّا.'),
                      ('tex', r'=\frac12\ln|w|', [('diff(log(w)/2,w)', '1/(2*w)')], r'تكامل $\frac1w$ هو $\ln|w|$.'),
                      ('tex', r'=\frac12\ln\left|x^{2}+2\sin x\right|+C', [('diff(log(x**2+2*sin(x))/2,x)', '(x+cos(x))/(x**2+2*sin(x))')],
                       r'نرجع $w=x^2+2\sin x$.')])
    return U


def part_b3():
    U = PreUnit('P-B3', 'ب3', 'تبسيط درس 5.1', 'pre51', 'جبر، ومذكرة د. طارق: دروس 3.1 و3.2')
    U.why('أغلب أخطاء التجزئة تجي في التبسيط، مو في الطريقة. هنا تتدرّب على السالب قدّام القوس، والكسر، والتكامل المحدد، والتكامل اللي يرجع لنفسه.',
          [('U-P2', 13), ('U-P5', 16), ('U-P7', 18), ('U-P8', 19), ('U-P9', 20)])
    I0 = 'exp(x)*(sin(x)-cos(x))/2'
    U.explain([
        ('<b>السالب قدّام القوس</b> يقلب إشارة كل حد داخله، مو أول حد بس.', r'-\left(2x\cos x-2\sin x\right)=-2x\cos x+2\sin x',
         [('-(2*x*cos(x)-2*sin(x))', '-2*x*cos(x)+2*sin(x)')]),
        ('<b>ضرب كسرين</b>: فوق في فوق، وتحت في تحت. ثم نختصر.', r'\frac{x^{3}}{3}\cdot\frac1x=\frac{x^{3}}{3x}=\frac{x^{2}}{3}',
         [('x**3/3*(1/x)', 'x**3/(3*x)'), ('x**3/(3*x)', 'x**2/3')]),
        (r'<b>إذا فوق وتحت فيهم $x^2$</b>: نكتب اللي فوق بدلالة اللي تحت، ثم نفصل لكسرين.',
         r'\frac{x^{2}}{1+x^{2}}=\frac{\left(1+x^{2}\right)-1}{1+x^{2}}=1-\frac{1}{1+x^{2}}',
         [('x**2/(1+x**2)', '((1+x**2)-1)/(1+x**2)'), ('x**2/(1+x**2)', '1-1/(1+x**2)')]),
        ('<b>قيم تحفظها</b> للتكامل المحدد في النوع 16.', r'\ln1=0,\quad \ln e=1,\quad e^{0}=1,\quad e^{\ln7}=7,\quad \cos0=1',
         [('log(1)', '0'), ('log(E)', '1'), ('exp(0)', '1'), ('exp(log(7))', '7'), ('cos(0)', '1')]),
        ('<b>التكامل المحدد</b>: نعوّض الحد اللي فوق، ونطرح منه تعويض الحد اللي تحت. ونحط الثاني بين قوسين.',
         r'\left[x^{2}\right]_{1}^{3}=3^{2}-\left(1^{2}\right)=9-1=8', [('3**2-(1**2)', '8')]),
        (r'<b>التكامل اللي يرجع لنفسه</b> (النوع 19): نسمّيه $I$. يطلع في الطرفين، فننقله لطرف واحد ونجمعه.',
         r'I=e^{x}\sin x-e^{x}\cos x-I,\qquad 2I=e^{x}\sin x-e^{x}\cos x',
         [(I0, 'exp(x)*sin(x)-exp(x)*cos(x)-' + I0), ('2*' + I0, 'exp(x)*sin(x)-exp(x)*cos(x)')]),
        ('ثم نقسم على الرقم اللي قدام $I$.', r'I=\frac{e^{x}\sin x-e^{x}\cos x}{2}', [(I0, '(exp(x)*sin(x)-exp(x)*cos(x))/2')]),
        ('<b>ضرب الأسيات</b>: الأسس تنجمع. تحتاجه في النوع 20.', r'e^{x}\cdot e^{2x}=e^{3x},\qquad e^{x}\cdot\frac{e^{2x}+e^{-2x}}{2}=\frac{e^{3x}+e^{-x}}{2}',
         [('exp(x)*exp(2*x)', 'exp(3*x)'), ('exp(x)*(exp(2*x)+exp(-2*x))/2', '(exp(3*x)+exp(-x))/2')])])
    U.add('short', '📐 القانون: التكامل المحدد',
          md(arith(r'\int_{1}^{3}2x\,dx=\left[x^{2}\right]_{1}^{3}=3^{2}-\left(1^{2}\right)=8', [('diff(x**2,x)', '2*x'), ('3**2-(1**2)', '8')], 'P-B3 law'))
          + p(rich('نكامل أول بدون $+C$. ثم نعوّض الحد اللي فوق، ونطرح منه تعويض الحد اللي تحت.'), 'small')
          + tricks([(r'احسب الجواب كامل أول، ثم عوّض الحدين مرة وحدة. واحفظ: $\ln1=0$، و $\ln e=1$، و $e^0=1$، و $\cos0=1$.',
                     [('log(1)', '0'), ('log(E)', '1'), ('exp(0)', '1'), ('cos(0)', '1')])], 'P-B3'))
    U.example('وزّع وبسّط (يطلع في النوع 13)', r'x^{2}\sin x-2\left(x\cos x-\sin x\right)', [
        (r'-2\left(x\cos x-\sin x\right)=-2x\cos x-2\left(-\sin x\right)', [('-2*(x*cos(x)-sin(x))', '-2*x*cos(x)-2*(-sin(x))')],
         'الـ $-2$ تدخل على كل حد داخل القوس.'),
        (r'=-2x\cos x+2\sin x', [('-2*x*cos(x)-2*(-sin(x))', '-2*x*cos(x)+2*sin(x)')], r'سالب في سالب = موجب: $-2\cdot(-\sin x)=+2\sin x$.'),
        (r'x^{2}\sin x-2x\cos x+2\sin x', [('x**2*sin(x)-2*(x*cos(x)-sin(x))', 'x**2*sin(x)-2*x*cos(x)+2*sin(x)')],
         'نكتب الحد الأول مع الحدين الجديدين.')])
    U.example('قسمة بسيطة (يطلع في النوعين 15 و18)', r'\frac{2x^{2}}{1+x^{2}}', [
        (r'2x^{2}=2\left(1+x^{2}\right)-2', [('2*x**2', '2*(1+x**2)-2')],
         r'نكتب اللي فوق بدلالة اللي تحت: $2(1+x^2)=2+2x^2$، فنطرح 2 عشان يرجع $2x^2$.'),
        (r'\frac{2x^{2}}{1+x^{2}}=\frac{2\left(1+x^{2}\right)}{1+x^{2}}-\frac{2}{1+x^{2}}', [('2*x**2/(1+x**2)', '2*(1+x**2)/(1+x**2)-2/(1+x**2)')],
         'فوق صار طرح، فنفصل لكسرين.'),
        (r'=2-\frac{2}{1+x^{2}}', [('2*x**2/(1+x**2)', '2-2/(1+x**2)')], r'نختصر $1+x^2$ فوق مع تحت.')])
    U.example('احسب (محدد)', r'\left[x\ln x-x\right]_{1}^{e}', [
        (r'e\ln e-e=e\cdot1-e', [('E*log(E)-E', 'E*1-E')], r'نعوّض الحد اللي فوق $e$ مكان $x$. و $\ln e=1$.'),
        (r'=0', [('E*1-E', '0')], '$e-e=0$.'),
        (r'1\cdot\ln1-1=1\cdot0-1=-1', [('1*log(1)-1', '-1')], r'نعوّض الحد اللي تحت 1. و $\ln1=0$.'),
        (r'0-\left(-1\right)=1', [('0-(-1)', '1')], 'اللي فوق ناقص اللي تحت. وسالب في سالب = موجب.')])
    U.example('حل للتكامل $I$ (النوع 19)', r'I=e^{x}\sin x-e^{x}\cos x-I', [
        (r'I+I=e^{x}\sin x-e^{x}\cos x', [(I0 + '+' + I0, 'exp(x)*sin(x)-exp(x)*cos(x)')],
         r'$I$ في الطرفين. ننقل $-I$ للطرف الأول، فتصير $+I$.'),
        (r'2I=e^{x}\sin x-e^{x}\cos x', [(I0 + '+' + I0, '2*' + I0)], r'نجمع: $I+I=2I$.'),
        (r'I=\frac{e^{x}\sin x-e^{x}\cos x}{2}', [(I0, '(exp(x)*sin(x)-exp(x)*cos(x))/2')], 'نقسم الطرفين على 2.')],
        check=r'هذا $\int e^x\sin x\,dx$. اشتق الجواب: يطلع $e^x\sin x$ ✓')
    arith('', [('diff(' + I0 + ',x)', 'exp(x)*sin(x)')], 'P-B3 check')
    U.add('trap', '⚠️ الفخ', ul([rich(r'$-(x-\sin x)=-x+\sin x$: الحد الثاني بعد تنقلب إشارته.'),
                                rich(r'$\frac{1}{1+x^2}\ne1+\frac{1}{x^2}$: المقام ما ينفصل.'),
                                rich('في المحدد: اللي فوق ناقص اللي تحت، مو العكس. وحط اللي تحت بين قوسين.')]))
    arith('', [('-(x-sin(x))', '-x+sin(x)')], 'P-B3 trap')
    U.add('ok', '✔ تأكد', p(rich('بعد التبسيط، عوّض رقم سهل مثل $x=1$ في السطر قبل وبعد. لازم يطلع نفس الرقم.')))
    U.task('1', 'G', 'وزّع', 'وزّع السالب:', r'-\left(2xe^{x}-2e^{x}\right)', [
        (r'-\left(2xe^{x}\right)=-2xe^{x}', [('-(2*x*exp(x))', '-2*x*exp(x)')], 'السالب يدخل على الحد الأول.'),
        (r'-\left(-2e^{x}\right)=+2e^{x}', [('-(-2*exp(x))', '2*exp(x)')], 'ويدخل على الحد الثاني. سالب في سالب = موجب.'),
        (r'-\left(2xe^{x}-2e^{x}\right)=-2xe^{x}+2e^{x}', [('-(2*x*exp(x)-2*exp(x))', '-2*x*exp(x)+2*exp(x)')], 'نكتب الحدين مع بعض.')],
           'السالب يقلب إشارة الحدين.')
    U.task('2', 'P', 'قسّم', 'اكتب كرقم ناقص كسر:', r'\frac{x^{2}}{x^{2}+4}', [
        (r'x^{2}=\left(x^{2}+4\right)-4', [('x**2', '(x**2+4)-4')], r'فوق وتحت فيهم $x^2$. نكتب اللي فوق بدلالة اللي تحت: نزيد 4 وننقص 4.'),
        (r'\frac{x^{2}}{x^{2}+4}=\frac{x^{2}+4}{x^{2}+4}-\frac{4}{x^{2}+4}', [('x**2/(x**2+4)', '(x**2+4)/(x**2+4)-4/(x**2+4)')],
         'فوق صار طرح، فنفصل لكسرين.'),
        (r'=1-\frac{4}{x^{2}+4}', [('x**2/(x**2+4)', '1-4/(x**2+4)')], 'أي شي على نفسه يساوي 1.')],
           r'نزيد 4 وننقص 4 فوق: $x^2=(x^2+4)-4$.')
    U.task('3', 'P', 'احسب', 'احسب:', r'\left[x^{2}\ln x-\frac{x^{2}}{2}\right]_{1}^{e}', [
        (r'e^{2}\ln e-\frac{e^{2}}{2}=e^{2}-\frac{e^{2}}{2}', [('E**2*log(E)-E**2/2', 'E**2-E**2/2')], r'نعوّض الحد اللي فوق $e$. و $\ln e=1$.'),
        (r'=\frac{e^{2}}{2}', [('E**2-E**2/2', 'E**2/2')], r'نص $e^2$ ناقص من $e^2$ يبقى نص $e^2$.'),
        (r'1^{2}\ln1-\frac{1^{2}}{2}=0-\frac12=-\frac12', [('1**2*log(1)-Rational(1,2)', '-Rational(1,2)')], r'نعوّض الحد اللي تحت 1. و $\ln1=0$.'),
        (r'\frac{e^{2}}{2}-\left(-\frac12\right)=\frac{e^{2}+1}{2}', [('E**2/2-(-Rational(1,2))', '(E**2+1)/2')],
         'اللي فوق ناقص اللي تحت. وسالب في سالب = موجب.')],
           r'عوّض $e$ ثم 1. و $\ln e=1$، و $\ln1=0$.')
    J0 = 'exp(x)*(sin(4*x)-4*cos(4*x))/17'
    U.task('4', 'I', 'حل', r'هذا $I=\int e^x\sin4x\,dx$ بعد تجزئتين. حل للتكامل $I$:',
           r'I=\frac{1}{16}e^{x}\sin4x-\frac14e^{x}\cos4x-\frac{1}{16}I', [
        (r'I+\frac{1}{16}I=\frac{1}{16}e^{x}\sin4x-\frac14e^{x}\cos4x', [(J0 + '+' + J0 + '/16', 'exp(x)*sin(4*x)/16-exp(x)*cos(4*x)/4')],
         r'ننقل $-\frac{1}{16}I$ للطرف الأول، فتصير $+\frac{1}{16}I$.'),
        (r'\frac{17}{16}I=\frac{1}{16}e^{x}\sin4x-\frac14e^{x}\cos4x', [('1+Rational(1,16)', 'Rational(17,16)')],
         r'نجمع: $1+\frac{1}{16}=\frac{16}{16}+\frac{1}{16}=\frac{17}{16}$.'),
        (r'I=\frac{16}{17}\left(\frac{1}{16}e^{x}\sin4x-\frac14e^{x}\cos4x\right)', [(J0, 'Rational(16,17)*(exp(x)*sin(4*x)/16-exp(x)*cos(4*x)/4)')],
         r'نضرب الطرفين في المقلوب $\frac{16}{17}$.'),
        (r'I=\frac{1}{17}e^{x}\sin4x-\frac{4}{17}e^{x}\cos4x', [(J0, 'exp(x)*sin(4*x)/17-4*exp(x)*cos(4*x)/17')],
         r'نوزّع: $\frac{16}{17}\cdot\frac{1}{16}=\frac{1}{17}$، و $\frac{16}{17}\cdot\frac14=\frac{4}{17}$.')],
           r'انقل $\frac{1}{16}I$ للطرف الأول، ثم اقسم على $\frac{17}{16}$.')
    arith('', [('diff(' + J0 + ',x)', 'exp(x)*sin(4*x)')], 'P-B3 task 4 check')
    U.task('5', 'I', 'بسّط', 'اكتب بالأسس وبسّط:', r'e^{x}\cosh x', [
        (r'\cosh x=\frac{e^{x}+e^{-x}}{2}', [('cosh(x)', '(exp(x)+exp(-x))/2')], 'نكتب cosh بتعريفه، عشان يصير كل شي أسس.'),
        (r'e^{x}\cosh x=\frac{e^{x}e^{x}+e^{x}e^{-x}}{2}', [('exp(x)*cosh(x)', '(exp(x)*exp(x)+exp(x)*exp(-x))/2')], 'نضرب $e^x$ في كل حد فوق.'),
        (r'=\frac{e^{2x}+e^{0}}{2}', [('(exp(x)*exp(x)+exp(x)*exp(-x))/2', '(exp(2*x)+exp(0))/2')],
         'ضرب نفس الأساس، فنجمع الأسس: $x+x=2x$، و $x-x=0$.'),
        (r'=\frac{e^{2x}+1}{2}', [('exp(x)*cosh(x)', '(exp(2*x)+1)/2')], 'أي شي أسه 0 يساوي 1، فـ $e^0=1$.')],
           r'اكتب cosh بتعريفه، واضرب $e^x$ في كل حد.')
    return U


# ================================================================ before 5.2
def part_c1():
    U = PreUnit('P-C1', 'ج1', 'المثلثات: المتطابقات، وضعف الزاوية ونصها، والمشتقات', 'pre52',
                'من مقررات قبل ريض 111، ومذكرة د. طارق تستعملها في 5.2 (ص67)')
    U.why('كل أنواع 5.2 تبدأ بمتطابقة تحوّل السؤال لشكل نعرف نكامله. وتحتاج مشتقات الدوال الست عشان تعرف وش تحجز.',
          [('U-T1', 22), ('U-T3', 24), ('U-T4', 25), ('U-T6', 27), ('U-T8', 29)])
    U.explain([
        (r'<b>المتطابقة الأساسية</b>: $\sin^2x+\cos^2x=1$ لأي زاوية.', r'\sin^{2}x+\cos^{2}x=1', [('sin(x)**2+cos(x)**2', '1')]),
        (r'نقسم الطرفين على $\cos^2x$، فتطلع متطابقة tan و sec.',
         r'\frac{\sin^{2}x}{\cos^{2}x}+\frac{\cos^{2}x}{\cos^{2}x}=\frac{1}{\cos^{2}x},\qquad \tan^{2}x+1=\sec^{2}x',
         [('sin(x)**2/cos(x)**2+cos(x)**2/cos(x)**2', '1/cos(x)**2'), ('tan(x)**2+1', 'sec(x)**2')]),
        (r'ونقسم على $\sin^2x$، فتطلع متطابقة cot و csc.', r'1+\cot^{2}x=\csc^{2}x', [('1+cot(x)**2', 'csc(x)**2')]),
        ('في 5.2 نستعملها عشان نحوّل الباقي بعد الحجز.', r'\cos^{2}x=1-\sin^{2}x,\qquad \tan^{2}x=\sec^{2}x-1',
         [('cos(x)**2', '1-sin(x)**2'), ('tan(x)**2', 'sec(x)**2-1')]),
        (r'<b>ضعف الزاوية</b>: نكتب $\sin2x$ كضرب sin في cos، ومعه 2.',r'\sin2x=2\sin x\cos x', [('sin(2*x)', '2*sin(x)*cos(x)')]),
        ('<b>نص الزاوية</b> ينزّل الأس من 2 إلى 1. مع $\\cos^2$ زائد، ومع $\\sin^2$ ناقص، والزاوية تتضاعف.',
         r'\cos^{2}x=\frac{1+\cos2x}{2},\qquad \sin^{2}4x=\frac{1-\cos8x}{2}', [('cos(x)**2', '(1+cos(2*x))/2'), ('sin(4*x)**2', '(1-cos(8*x))/2')]),
        ('<b>مشتقات الدوال الست</b>: اللي اسمها يبدأ بـ co مشتقتها فيها سالب.',
         r'\frac{d}{dx}\tan x=\sec^{2}x,\qquad \frac{d}{dx}\sec x=\sec x\tan x,\qquad \frac{d}{dx}\cot x=-\csc^{2}x',
         [('diff(tan(x),x)', 'sec(x)**2'), ('diff(sec(x),x)', 'sec(x)*tan(x)'), ('diff(cot(x),x)', '-csc(x)**2')]),
        ('<b>والتكاملات</b> عكس المشتقات. واثنين لازم تحفظهم، لأنهم ما يطلعون من جدول المشتقات.',
         r'\int\tan x\,dx=\ln|\sec x|+C,\qquad \int\sec x\,dx=\ln|\sec x+\tan x|+C',
         [('diff(log(sec(x)),x)', 'tan(x)', 't/(1+t)'), ('diff(log(sec(x)+tan(x)),x)', 'sec(x)', 't/(1+t)')])])
    U.raw(alg('trig-pyth', 'متطابقات فيثاغورس', [
        (r'\sin^{2}x+\cos^{2}x=1', [('sin(x)**2+cos(x)**2', '1')], 'المتطابقة الأساسية:'),
        (r'\cos^{2}x=1-\sin^{2}x,\qquad \sin^{2}x=1-\cos^{2}x', [('cos(x)**2', '1-sin(x)**2'), ('sin(x)**2', '1-cos(x)**2')],
         'ننقل حد للطرف الثاني، فتطلع صورتين. تحتاجهم مع sin و cos:'),
        (r'\sec^{2}x=1+\tan^{2}x', [('sec(x)**2', '1+tan(x)**2')], r'نقسم الأساسية على $\cos^2x$. تحتاجها مع tan و sec:'),
        (r'\csc^{2}x=1+\cot^{2}x', [('csc(x)**2', '1+cot(x)**2')], r'ونقسمها على $\sin^2x$. تحتاجها مع cot و csc:')]))
    d6 = [formula('sin(u)', 'cos(u)', 'diff', branches=('x',), uprime=True, label='P-C1 sin'),
          formula('cos(u)', '-sin(u)', 'diff', branches=('x',), uprime=True, label='P-C1 cos'),
          formula('tan(u)', 'sec(u)**2', 'diff', branches=('t/(1+t)',), uprime=True, label='P-C1 tan'),
          formula('cot(u)', '-csc(u)**2', 'diff', branches=('t/(1+t)',), uprime=True, label='P-C1 cot'),
          formula('sec(u)', 'sec(u)*tan(u)', 'diff', branches=('t/(1+t)',), uprime=True, label='P-C1 sec'),
          formula('csc(u)', '-csc(u)*cot(u)', 'diff', branches=('t/(1+t)',), uprime=True, label='P-C1 csc')]
    i6 = [formula('sec(x)**2', 'tan(x)', var='x', branches=('t/(1+t)',), label='P-C1 int sec2'),
          formula('csc(x)**2', '-cot(x)', var='x', branches=('t/(1+t)',), label='P-C1 int csc2'),
          formula('sec(x)*tan(x)', 'sec(x)', var='x', branches=('t/(1+t)',), label='P-C1 int sec tan'),
          formula('csc(x)*cot(x)', '-csc(x)', var='x', branches=('t/(1+t)',), label='P-C1 int csc cot'),
          formula('tan(x)', 'log(Abs(sec(x)))', var='x', branches=('t/(1+t)',), label='P-C1 int tan'),
          formula('sec(x)', 'log(Abs(sec(x)+tan(x)))', var='x', branches=('t/(1+t)',), label='P-C1 int sec')]
    dbl = [(r'\sin2x=2\sin x\cos x', [('sin(2*x)', '2*sin(x)*cos(x)')]),
           (r'\cos^{2}x=\frac{1+\cos2x}{2},\qquad \sin^{2}x=\frac{1-\cos2x}{2}', [('cos(x)**2', '(1+cos(2*x))/2'), ('sin(x)**2', '(1-cos(2*x))/2')]),
           (r'\sin(-x)=-\sin x,\qquad \cos(-x)=\cos x', [('sin(-x)', '-sin(x)'), ('cos(-x)', 'cos(x)')])]
    dbl_t = table(['المتطابقة'], [[mi(r'\displaystyle ' + arith(lt, c, 'P-C1 identity'))] for lt, c in dbl], 'formula compact')
    U.add('short', '📐 القانون: مشتقات الدوال الست وتكاملاتها', table(['المشتقة', 'تساوي'], [_row(z) for z in d6], 'formula compact')
          + p(rich("في الجدول: $u'$ مشتقة اللي داخل الدالة."), 'small')
          + table(['التكامل', 'الجواب (+C)'], [_row(z) for z in i6], 'formula compact'))
    U.add('short', '📐 القانون: ضعف الزاوية ونصها', dbl_t
          + tricks([(r'سين وسالب: $\sin^2$ معها ناقص، و $\cos^2$ معها زائد. والزاوية تتضاعف: $\sin^23x=\frac{1-\cos6x}{2}$.',
                     [('sin(3*x)**2', '(1-cos(6*x))/2')])], 'P-C1'))
    SHEET['trig'] = (table(['المتطابقة'], [[mi(r'\displaystyle \sin^{2}x+\cos^{2}x=1,\quad \sec^{2}x=1+\tan^{2}x,\quad \csc^{2}x=1+\cot^{2}x')]], 'formula compact')
                     + dbl_t)
    U.example('أوجد المشتقة', r'y=\sec3x', [
        (r"u=3x,\qquad u'=3", [('diff(3*x,x)', '3')], 'sec داخلها $3x$. نسمّيه $u$، ونشتقه.'),
        (r"y'=\sec u\tan u\cdot u'", [('diff(sec(3*x),x)', 'sec(3*x)*tan(3*x)*diff(3*x,x)')], "قانون sec: مشتقته $\\sec u\\tan u$، ثم نضرب في $u'$."),
        (r"y'=3\sec3x\tan3x", [('diff(sec(3*x),x)', '3*sec(3*x)*tan(3*x)')], "نعوّض $u=3x$ و $u'=3$، ونكتب 3 قدّام.")])
    U.example('نزّل الأس (النوع 24)', r'\sin^{2}x\cos^{2}x', [
        (r'\sin x\cos x=\frac12\sin2x', [('sin(x)*cos(x)', 'sin(2*x)/2')], r'من ضعف الزاوية $\sin2x=2\sin x\cos x$. نقسم الطرفين على 2.'),
        (r'\sin^{2}x\cos^{2}x=\left(\sin x\cos x\right)^{2}', [('sin(x)**2*cos(x)**2', '(sin(x)*cos(x))**2')], 'الأسين نفس الرقم، فنكتبهم مربع واحد.'),
        (r'=\left(\frac12\sin2x\right)^{2}=\frac14\sin^{2}2x', [('(sin(2*x)/2)**2', 'sin(2*x)**2/4')],
         r'نعوّض السطر الأول، ونربّع: $\left(\frac12\right)^2=\frac14$.'),
        (r'\sin^{2}2x=\frac{1-\cos4x}{2}', [('sin(2*x)**2', '(1-cos(4*x))/2')], r'هنا التريك: سين وسالب. والزاوية تتضاعف: $2\cdot2x=4x$.'),
        (r'\frac14\cdot\frac{1-\cos4x}{2}=\frac{1-\cos4x}{8}', [('sin(x)**2*cos(x)**2', '(1-cos(4*x))/8')], r'نضرب المقامين: $4\cdot2=8$.')])
    U.example('حوّل للحجز (الأنواع 22–28)', r'\tan^{3}x', [
        (r'\tan^{3}x=\tan x\cdot\tan^{2}x', [('tan(x)**3', 'tan(x)*tan(x)**2')], 'نفصل مربع، عشان نستعمل المتطابقة عليه.'),
        (r'=\tan x\left(\sec^{2}x-1\right)', [('tan(x)**3', 'tan(x)*(sec(x)**2-1)')], r'من $\tan^2x+1=\sec^2x$: ننقل 1 للطرف الثاني.'),
        (r'=\tan x\sec^{2}x-\tan x', [('tan(x)**3', 'tan(x)*sec(x)**2-tan(x)')], r'نوزّع $\tan x$ على القوس.')])
    U.add('trap', '⚠️ الفخ', ul([rich(r'$\sin2x\ne2\sin x$. الصح $2\sin x\cos x$.'),
                                rich(r'$\sin^2x$ يعني $(\sin x)^2$، مو $\sin(x^2)$.'),
                                rich(r'مشتقة cos و cot و csc فيها سالب. و $\int\sin x\,dx=-\cos x$.')]))
    U.add('ok', '✔ تأكد', p(rich(r'عوّض $x=0$ في متطابقتك: $\sin0=0$ و $\cos0=1$. لازم الطرفين يتساوون.')))
    U.task('1', 'G', 'اكتب بنص الزاوية', 'اكتب بنص الزاوية:', r'\cos^{2}5x', [
        (r'\cos^{2}x=\frac{1+\cos2x}{2}', [('cos(x)**2', '(1+cos(2*x))/2')], r'القانون: مع $\cos^2$ زائد، والزاوية تتضاعف.'),
        (r'2\cdot5x=10x', [('2*5*x', '10*x')], r'الزاوية هنا $5x$، وضعفها $10x$.'),
        (r'\cos^{2}5x=\frac{1+\cos10x}{2}', [('cos(5*x)**2', '(1+cos(10*x))/2')], r'نعوّض $5x$ مكان $x$ في القانون.')],
           r'مع $\cos^2$ زائد، والزاوية تتضاعف.')
    U.drill('2', 'G-71', 'P', r"قانون sec، ونضرب في مشتقة $x^2$.",
            sol_rows=[('tex', r"u=x^{2},\quad u'=2x", [('diff(x**2,x)', '2*x')], 'sec داخلها $x^2$. نسمّيه $u$، ونشتقه.'),
                      ('tex', r"y'=\sec u\tan u\cdot u'", [('diff(sec(x**2),x)', 'sec(x**2)*tan(x**2)*diff(x**2,x)')],
                       "قانون sec: مشتقته $\\sec u\\tan u$، ثم نضرب في $u'$."),
                      ('line', '2*x*sec(x**2)*tan(x**2)', "نعوّض $u=x^2$ و $u'=2x$، ونكتب $2x$ قدّام.")])
    U.drill('3', 'M-29', 'P', r'نسمّي $2+e^{7x}$ هو $u$، و $\int\csc^2u\,du=-\cot u$.',
            sol_rows=[('sub', '2+exp(7*x)', '7*exp(7*x)',
                       r'داخل $\csc^2$ فيه $2+e^{7x}$، ومشتقته $7e^{7x}$. وبرّا عندنا $e^{7x}$، فنسمّي $2+e^{7x}$ هو $u$.'),
                      ('tex', r'e^{7x}dx=\frac{du}{7}', [('diff(2+exp(7*x),x)/7', 'exp(7*x)')], r'برّا $e^{7x}\,dx$ بس، مو $7e^{7x}\,dx$. فنقسم على 7.'),
                      ('tex', r'\int e^{7x}\csc^{2}\left(2+e^{7x}\right)dx=\frac17\int\csc^{2}u\,du',
                       [('exp(7*x)*csc(2+exp(7*x))**2', 'Rational(1,7)*csc(2+exp(7*x))**2*diff(2+exp(7*x),x)')], r'نعوّض. والـ $\frac17$ تطلع برّا التكامل.'),
                      ('tex', r'=-\frac17\cot u', [('diff(-cot(u)/7,u)', 'csc(u)**2/7')],
                       r'من الجدول: $\int\csc^2u\,du=-\cot u$. فيه سالب، لأن cot يبدأ بـ co.'),
                      ('line', '-cot(2+exp(7*x))/7', r'نرجع $u=2+e^{7x}$.')])
    U.drill('4', 'G-73', 'I', r'وش الدالة اللي مشتقتها $\csc x\cot x$؟ انتبه للسالب.',
            sol_rows=[('tex', r'\frac{d}{dx}\csc x=-\csc x\cot x', [('diff(csc(x),x)', '-csc(x)*cot(x)')],
                       r'نبي دالة مشتقتها $\csc x\cot x$. من الجدول: مشتقة csc هي $-\csc x\cot x$.'),
                      ('tex', r'\frac{d}{dx}\left(-\csc x\right)=\csc x\cot x', [('diff(-csc(x),x)', 'csc(x)*cot(x)')],
                       'مشتقة csc فيها سالب. فنحط سالب قدّام csc، عشان تصير المشتقة موجبة.'),
                      ('line', '-csc(x)', r'إذن تكامل $\csc x\cot x$ هو $-\csc x$.')])
    U.task('5', 'I', 'حوّل', r'اكتب كـ $\cos x$ مضروب في شي فيه $\sin x$ بس:', r'\cos^{5}x', [
        (r'\cos^{5}x=\cos^{4}x\cdot\cos x', [('cos(x)**5', 'cos(x)**4*cos(x)')], r'نفصل $\cos x$ وحدة. الباقي أسه 4، وهو زوجي.'),
        (r'=\left(\cos^{2}x\right)^{2}\cos x', [('cos(x)**4*cos(x)', '(cos(x)**2)**2*cos(x)')], r'قوة فوق قوة: $\cos^4x=(\cos^2x)^2$.'),
        (r'=\left(1-\sin^{2}x\right)^{2}\cos x', [('cos(x)**5', '(1-sin(x)**2)**2*cos(x)')], r'من المتطابقة الأساسية: $\cos^2x=1-\sin^2x$.')],
           r'افصل $\cos x$ وحدة، والباقي $\cos^4x=(\cos^2x)^2$.')
    return U


def part_c2():
    U = PreUnit('P-C2', 'ج2', 'تبسيط درس 5.2: فك القوس، والتوزيع، والتكامل حد حد', 'pre52', 'جبر، ومذكرة د. طارق: درس 2.3')
    U.why('بعد التعويض في 5.2 يطلع لك قوس فيه $u$ وعليه أس، فتفكه وتوزّع وتكامل حد حد. وهذي أكثر خطوات 5.2 فيها أخطاء جبر.',
          [('U-T1', 22), ('U-T2', 23), ('U-T5', 26), ('U-T7', 28)])
    U.explain([
        ('<b>مربع القوس</b>: الأول تربيع، ثم ضعف ضرب الحدين، ثم الثاني تربيع. لا تنسى الحد اللي في النص.',
         r'(1-u^{2})^{2}=1-2u^{2}+u^{4},\qquad (u^{2}-1)^{2}=u^{4}-2u^{2}+1', [('(1-u**2)**2', '1-2*u**2+u**4'), ('(u**2-1)**2', 'u**4-2*u**2+1')]),
        ('<b>تكعيب القوس</b>: الأرقام 1 و3 و3 و1. ومع زائد كلها موجبة.', r'(1+u^{2})^{3}=1+3u^{2}+3u^{4}+u^{6}', [('(1+u**2)**3', '1+3*u**2+3*u**4+u**6')]),
        (r'<b>نضرب $u^3$ في القوس</b>: نضربها في كل حد، والأسس تنجمع.', r'u^{3}\left(1-2u^{2}+u^{4}\right)=u^{3}-2u^{5}+u^{7}',
         [('u**3*(1-2*u**2+u**4)', 'u**3-2*u**5+u**7')]),
        ('<b>تكامل كثيرة الحدود</b>: كل حد لحاله. نزيد الأس 1، ونقسم على الأس الجديد، والرقم اللي قدّام يبقى.',
         r'\int\left(u^{3}-2u^{5}+u^{7}\right)du=\frac{u^{4}}{4}-\frac{2u^{6}}{6}+\frac{u^{8}}{8}=\frac{u^{4}}{4}-\frac{u^{6}}{3}+\frac{u^{8}}{8}+C',
         [('integrate(u**3-2*u**5+u**7,u)', 'u**4/4-2*u**6/6+u**8/8'), ('2*u**6/6', 'u**6/3')]),
        (r'<b>الأس الكسري</b>، مثل $\sqrt u=u^{1/2}$: نفس القاعدة. والقسمة على كسر يعني نضرب في مقلوبه.',
         r'\int u^{5/2}du=\frac{u^{7/2}}{7/2}=\frac27u^{7/2}+C', [('integrate(u**Rational(5,2),u)', '2*u**Rational(7,2)/7')]),
        (r'<b>إذا $du$ فيها سالب</b>، مثل $u=\cos x$: السالب يطلع قدّام التكامل كله.',
         r'\int\cos^{2}x\sin x\,dx=-\int u^{2}du=-\frac{u^{3}}{3}=-\frac{\cos^{3}x}{3}+C', [('diff(-cos(x)**3/3,x)', 'cos(x)**2*sin(x)')])])
    sq = [(r'\left(1+u^{2}\right)^{2}=1+2u^{2}+u^{4}', [('(1+u**2)**2', '1+2*u**2+u**4')]),
          (r'\left(1-u^{2}\right)^{2}=1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')]),
          (r'\left(1+u^{2}\right)^{3}=1+3u^{2}+3u^{4}+u^{6}', [('(1+u**2)**3', '1+3*u**2+3*u**4+u**6')])]
    U.add('short', '📐 القانون: فك القوس', table(['القوس'], [[mi(r'\displaystyle ' + arith(lt, c, 'P-C2 rule'))] for lt, c in sq], 'formula compact')
          + p(rich('في المربع: الحد اللي في النص ضعف ضرب الحدين، وإشارته نفس الإشارة اللي في القوس.'), 'small')
          + tricks([(r'تأكد من الفك: عوّض $u=1$ قبل وبعد. $(1+1^2)^2=4$، و $1+2+1=4$ ✓',
                     [('(1+1**2)**2', '4'), ('1+2+1', '4')])], 'P-C2'))
    U.example('فك ثم وزّع ثم كامل', r'\int u^{2}\left(1-u^{2}\right)^{2}du', [
        (r'(1-u^{2})^{2}=1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')],
         r'نفك القوس أول. الحد اللي في النص: $2\cdot1\cdot u^2=2u^2$، وإشارته سالبة.'),
        (r'u^{2}\left(1-2u^{2}+u^{4}\right)=u^{2}-2u^{4}+u^{6}', [('u**2*(1-2*u**2+u**4)', 'u**2-2*u**4+u**6')],
         r'نضرب $u^2$ في كل حد، والأسس تنجمع.'),
        (r'\int\left(u^{2}-2u^{4}+u^{6}\right)du=\frac{u^{3}}{3}-\frac{2u^{5}}{5}+\frac{u^{7}}{7}+C',
         [('integrate(u**2-2*u**4+u**6,u)', 'u**3/3-2*u**5/5+u**7/7')], 'نكامل حد حد: نزيد الأس 1، ونقسم على الأس الجديد.')])
    U.example('أس كسري', r'\int u^{1/2}\left(1-u^{2}\right)du', [
        (r'u^{1/2}\left(1-u^{2}\right)=u^{1/2}-u^{5/2}', [('u**Rational(1,2)*(1-u**2)', 'u**Rational(1,2)-u**Rational(5,2)', 't')],
         r'نوزّع، والأسس تنجمع: $\frac12+2=\frac52$.'),
        (r'\int\left(u^{1/2}-u^{5/2}\right)du=\frac{u^{3/2}}{3/2}-\frac{u^{7/2}}{7/2}',
         [('diff(u**Rational(3,2)/Rational(3,2)-u**Rational(7,2)/Rational(7,2),u)', 'u**Rational(1,2)-u**Rational(5,2)', 't')],
         r'نزيد الأس 1: $\frac12+1=\frac32$، و $\frac52+1=\frac72$.'),
        (r'=\frac23u^{3/2}-\frac27u^{7/2}+C', [('u**Rational(3,2)/Rational(3,2)-u**Rational(7,2)/Rational(7,2)', '2*u**Rational(3,2)/3-2*u**Rational(7,2)/7', 't')],
         'القسمة على كسر يعني نضرب في مقلوبه.')])
    U.example('السالب قدّام التكامل', r'-\int\left(u^{4}-u^{6}\right)du', [
        (r'\int\left(u^{4}-u^{6}\right)du=\frac{u^{5}}{5}-\frac{u^{7}}{7}', [('integrate(u**4-u**6,u)', 'u**5/5-u**7/7')],
         'نكامل داخل القوس أول، والسالب نخليه برّا.'),
        (r'-\int\left(u^{4}-u^{6}\right)du=-\left(\frac{u^{5}}{5}-\frac{u^{7}}{7}\right)', [('-integrate(u**4-u**6,u)', '-(u**5/5-u**7/7)')],
         'نرجّع السالب قدّام الجواب كله.'),
        (r'=-\frac{u^{5}}{5}+\frac{u^{7}}{7}+C', [('-(u**5/5-u**7/7)', '-u**5/5+u**7/7')], 'نوزّع السالب: يقلب إشارة كل حد.')])
    U.add('trap', '⚠️ الفخ', ul([rich(r'$(1-u^2)^2\ne1-u^4$. نسيت الحد اللي في النص $-2u^2$.'),
                                rich(r'$u^3\cdot u^2=u^5$، مو $u^6$. في الضرب الأسس تنجمع.'),
                                rich('السالب قدّام التكامل يدخل على كل الحدود.')]))
    U.add('ok', '✔ تأكد', p(rich(r'عوّض $u=1$ في القوس قبل الفك وبعده. لازم يطلع نفس الرقم: $(1-1)^2=0$، و $1-2+1=0$ ✓')))
    arith('', [('(1-1)**2', '0'), ('1-2+1', '0')], 'P-C2 check')
    U.task('1', 'G', 'فك القوس', 'فك القوس:', r'\left(1+u^{2}\right)^{2}', [
        (r'1^{2}=1', [('1**2', '1')], 'الحد الأول تربيع.'),
        (r'2\cdot1\cdot u^{2}=2u^{2}', [('2*1*u**2', '2*u**2')], 'الحد اللي في النص: ضعف ضرب الحدين.'),
        (r'\left(u^{2}\right)^{2}=u^{4}', [('(u**2)**2', 'u**4')], 'الحد الثاني تربيع: قوة فوق قوة، فنضرب الأسس.'),
        (r'\left(1+u^{2}\right)^{2}=1+2u^{2}+u^{4}', [('(1+u**2)**2', '1+2*u**2+u**4')], 'نجمع الثلاثة.')],
           r'لا تنسى الحد اللي في النص $2u^2$.')
    U.task('2', 'P', 'وزّع', 'فك القوس، ثم وزّع:', r'u^{3}\left(1+u^{2}\right)^{2}', [
        (r'(1+u^{2})^{2}=1+2u^{2}+u^{4}', [('(1+u**2)**2', '1+2*u**2+u**4')], r'نفك القوس أول. لا تنسى الحد اللي في النص $2u^2$.'),
        (r'u^{3}\cdot1+u^{3}\cdot2u^{2}+u^{3}\cdot u^{4}', [('u**3*(1+2*u**2+u**4)', 'u**3*1+u**3*2*u**2+u**3*u**4')], r'نضرب $u^3$ في كل حد.'),
        (r'=u^{3}+2u^{5}+u^{7}', [('u**3*(1+u**2)**2', 'u**3+2*u**5+u**7')], r'الأسس تنجمع: $3+2=5$، و $3+4=7$.')],
           r'فك القوس أول، ثم اضرب $u^3$ في كل حد.')
    U.task('3', 'P', 'كامل', 'كامل حد حد:', r'\int\left(u^{4}+2u^{6}+u^{8}\right)du', [
        (r'\int u^{4}du=\frac{u^{5}}{5}', [('integrate(u**4,u)', 'u**5/5')], 'الحد الأول: نزيد الأس 1، ونقسم على 5.'),
        (r'\int2u^{6}du=\frac{2u^{7}}{7}', [('integrate(2*u**6,u)', '2*u**7/7')], 'الحد الثاني: الرقم 2 يبقى، والأس يصير 7.'),
        (r'\int u^{8}du=\frac{u^{9}}{9}', [('integrate(u**8,u)', 'u**9/9')], 'الحد الثالث: الأس يصير 9.'),
        (r'=\frac{u^{5}}{5}+\frac{2u^{7}}{7}+\frac{u^{9}}{9}+C', [('integrate(u**4+2*u**6+u**8,u)', 'u**5/5+2*u**7/7+u**9/9')],
         'نجمع الحدود، ونزيد $+C$.')],
           'كل حد: نزيد الأس 1، ونقسم على الأس الجديد.')
    U.task('4', 'I', 'كامل', 'وزّع، ثم كامل:', r'\int u^{2/3}\left(1-u^{2}\right)du', [
        (r'u^{2/3}\left(1-u^{2}\right)=u^{2/3}-u^{8/3}', [('u**Rational(2,3)*(1-u**2)', 'u**Rational(2,3)-u**Rational(8,3)', 't')],
         r'نوزّع، والأسس تنجمع: $\frac23+2=\frac23+\frac63=\frac83$.'),
        (r'\int\left(u^{2/3}-u^{8/3}\right)du=\frac{u^{5/3}}{5/3}-\frac{u^{11/3}}{11/3}',
         [('diff(u**Rational(5,3)/Rational(5,3)-u**Rational(11,3)/Rational(11,3),u)', 'u**Rational(2,3)-u**Rational(8,3)', 't')],
         r'نزيد الأس 1: $\frac23+1=\frac53$، و $\frac83+1=\frac{11}{3}$.'),
        (r'=\frac35u^{5/3}-\frac{3}{11}u^{11/3}+C',
         [('u**Rational(5,3)/Rational(5,3)-u**Rational(11,3)/Rational(11,3)', '3*u**Rational(5,3)/5-3*u**Rational(11,3)/11', 't')],
         'القسمة على كسر يعني نضرب في مقلوبه.')],
           r'الأسس الكسرية: $\frac23+1=\frac53$.')
    U.task('5', 'I', 'كامل', 'كامل، وانتبه للسالب:', r'-\int\left(u^{4}-2u^{2}\right)du', [
        (r'\int\left(u^{4}-2u^{2}\right)du=\frac{u^{5}}{5}-\frac{2u^{3}}{3}', [('integrate(u**4-2*u**2,u)', 'u**5/5-2*u**3/3')],
         'نكامل داخل القوس أول، والسالب نخليه برّا.'),
        (r'-\int\left(u^{4}-2u^{2}\right)du=-\left(\frac{u^{5}}{5}-\frac{2u^{3}}{3}\right)', [('-integrate(u**4-2*u**2,u)', '-(u**5/5-2*u**3/3)')],
         'نرجّع السالب قدّام الجواب كله.'),
        (r'=-\frac{u^{5}}{5}+\frac{2u^{3}}{3}+C', [('-(u**5/5-2*u**3/3)', '-u**5/5+2*u**3/3')], 'نوزّع السالب على الحدين.')],
           'كامل أول، ثم وزّع السالب على الحدين.')
    return U


def part_c3():
    U = PreUnit('P-C3', 'ج3', 'التعويض في المثلثات: u = sin أو cos أو tan أو sec', 'pre52', 'مذكرة د. طارق: درس 2.4، ودرس 5.2 ص67')
    U.why('كل أنواع الحجز في 5.2 تنتهي بتعويض $u$ = دالة مثلثية. هنا تتعلمه وهو سهل، لأن المشتقة موجودة كاملة في السؤال.',
          [('U-T1', 22), ('U-T2', 23), ('U-T4', 25), ('U-T5', 26), ('U-T7', 28)])
    U.explain([
        (r'الفكرة: إذا السؤال فيه دالة مثلثية، ومشتقتها مضروبة فيها، نسمّي الدالة $u$. والمشتقة تصير $du$.', None, []),
        (r'مع $u=\sin x$: لازم $\cos x\,dx$ تكون موجودة.', r'\int\sin^{4}x\cos x\,dx=\int u^{4}du=\frac{u^{5}}{5}=\frac{\sin^{5}x}{5}+C',
         [('diff(sin(x)**5/5,x)', 'sin(x)**4*cos(x)')]),
        (r'مع $u=\cos x$: مشتقته $-\sin x$، فيطلع سالب قدّام التكامل.', r'\int\cos^{3}x\sin x\,dx=-\int u^{3}du=-\frac{\cos^{4}x}{4}+C',
         [('diff(-cos(x)**4/4,x)', 'cos(x)**3*sin(x)')]),
        (r'مع $u=\tan x$: لازم $\sec^2x\,dx$ تكون موجودة.', r'\int\tan^{3}x\sec^{2}x\,dx=\int u^{3}du=\frac{\tan^{4}x}{4}+C',
         [('diff(tan(x)**4/4,x)', 'tan(x)**3*sec(x)**2')]),
        (r'مع $u=\sec x$: مشتقته $\sec x\tan x$. فنفصل $\sec x\tan x$ عن الباقي.',
         r'\int\sec^{3}x\tan x\,dx=\int\sec^{2}x\cdot\sec x\tan x\,dx=\frac{\sec^{3}x}{3}+C',
         [('sec(x)**3*tan(x)', 'sec(x)**2*sec(x)*tan(x)'), ('diff(sec(x)**3/3,x)', 'sec(x)**3*tan(x)')]),
        ('وإذا المشتقة ناقصة؟ نحجز قطعة، ونحوّل الباقي بمتطابقة من ج1. هذا اللي تتعلمه في الأنواع 22 إلى 28.', None, [])])
    subs = [('sin(x)', 'cos(x)', r'u=\sin x', r'du=\cos x\,dx', r'\cos x\,dx'),
            ('cos(x)', '-sin(x)', r'u=\cos x', r'du=-\sin x\,dx', r'\sin x\,dx=-du'),
            ('tan(x)', 'sec(x)**2', r'u=\tan x', r'du=\sec^{2}x\,dx', r'\sec^{2}x\,dx'),
            ('sec(x)', 'sec(x)*tan(x)', r'u=\sec x', r'du=\sec x\tan x\,dx', r'\sec x\tan x\,dx'),
            ('cot(x)', '-csc(x)**2', r'u=\cot x', r'du=-\csc^{2}x\,dx', r'\csc^{2}x\,dx=-du'),
            ('csc(x)', '-csc(x)*cot(x)', r'u=\csc x', r'du=-\csc x\cot x\,dx', r'\csc x\cot x\,dx=-du')]
    rows = [[mi(u_), mi(arith(du_, [('diff(%s,x)' % f, g)], 'P-C3 table')), mi(need)] for f, g, u_, du_, need in subs]
    U.add('short', '📐 القانون: جدول التعويض المثلثي', table(['إذا أخذت', 'فإن', 'لازم يكون في السؤال'], rows, 'formula compact')
          + p(rich('بعد التعويض نكامل بقاعدة القوة، ثم نرجع لـ $x$.'), 'small')
          + tricks([(r'cos و cot و csc مشتقاتها سالبة، فيطلع سالب قدّام التكامل. مثال: $u=\cos x$ يعطي $\sin x\,dx=-du$.',
                     [('-diff(cos(x),x)', 'sin(x)')])], 'P-C3'))
    U.example('u = sin x', r'\int\sin^{4}x\cos x\,dx', [
        (r'u=\sin x,\qquad du=\cos x\,dx', [('diff(sin(x),x)', 'cos(x)')], r'فيه sin، ومشتقته $\cos x$ موجودة كاملة. نسمّي $\sin x$ هو $u$.'),
        (r'\int\sin^{4}x\cos x\,dx=\int u^{4}du', [('sin(x)**4*cos(x)', 'sin(x)**4*diff(sin(x),x)')], r'نعوّض: $\sin^4x=u^4$، و $\cos x\,dx=du$.'),
        (r'=\frac{u^{5}}{5}', [('integrate(u**4,u)', 'u**5/5')], 'قاعدة القوة: نزيد الأس 1، ونقسم على 5.'),
        (r'=\frac{\sin^{5}x}{5}+C', [('diff(sin(x)**5/5,x)', 'sin(x)**4*cos(x)')], r'نرجع $u=\sin x$.')])
    U.example('u = cos x (يطلع سالب)', r'\int\cos^{3}x\sin x\,dx', [
        (r'u=\cos x,\qquad du=-\sin x\,dx', [('diff(cos(x),x)', '-sin(x)')], r'فيه cos، ومشتقته فيها $\sin x$ الموجودة. نسمّي $\cos x$ هو $u$.'),
        (r'\sin x\,dx=-du', [('-diff(cos(x),x)', 'sin(x)')], r'نضرب الطرفين في $-1$، عشان نعوّض مكان $\sin x\,dx$.'),
        (r'\int\cos^{3}x\sin x\,dx=-\int u^{3}du', [('cos(x)**3*sin(x)', '-cos(x)**3*diff(cos(x),x)')], 'نعوّض. والسالب يطلع قدّام التكامل.'),
        (r'=-\frac{u^{4}}{4}', [('-integrate(u**3,u)', '-u**4/4')], 'قاعدة القوة: نزيد الأس 1، ونقسم على 4.'),
        (r'=-\frac{\cos^{4}x}{4}+C', [('diff(-cos(x)**4/4,x)', 'cos(x)**3*sin(x)')], r'نرجع $u=\cos x$.')])
    U.example('u = sec x (نفصل sec tan)', r'\int\sec^{3}x\tan x\,dx', [
        (r'\sec^{3}x\tan x=\sec^{2}x\cdot\sec x\tan x', [('sec(x)**3*tan(x)', 'sec(x)**2*sec(x)*tan(x)')],
         r'مشتقة sec هي $\sec x\tan x$. فنفصلها عن الباقي.'),
        (r'u=\sec x,\qquad du=\sec x\tan x\,dx', [('diff(sec(x),x)', 'sec(x)*tan(x)')], r'نسمّي $\sec x$ هو $u$.'),
        (r'\int\sec^{2}x\cdot\sec x\tan x\,dx=\int u^{2}du', [('sec(x)**2*sec(x)*tan(x)', 'sec(x)**2*diff(sec(x),x)')],
         r'نعوّض: $\sec^2x=u^2$، و $\sec x\tan x\,dx=du$.'),
        (r'=\frac{u^{3}}{3}', [('integrate(u**2,u)', 'u**3/3')], 'قاعدة القوة.'),
        (r'=\frac{\sec^{3}x}{3}+C', [('diff(sec(x)**3/3,x)', 'sec(x)**3*tan(x)')], r'نرجع $u=\sec x$.')])
    U.add('trap', '⚠️ الفخ', ul([rich(r'مع $u=\cos x$ و $u=\cot x$ و $u=\csc x$ يطلع سالب قدّام التكامل.'),
                                rich(r'لا تعوّض إذا المشتقة مو موجودة. $\int\sin^4x\,dx$ ما فيه $\cos x$، فهذا نوع ثاني: نص الزاوية.')]))
    U.add('ok', '✔ تأكد', p(rich(r"اشتق جوابك بقاعدة السلسلة: $\left(\frac{\sin^5x}{5}\right)'=\sin^4x\cos x$ ✓. لازم يرجع السؤال.")))
    arith('', [('diff(sin(x)**5/5,x)', 'sin(x)**4*cos(x)')], 'P-C3 check')
    U.drill('1', 'G-74', 'G', r'نسمّي $\sin x$ هو $u$، والمشتقة $\cos x\,dx$ موجودة.', first=r'u=\sin x,\quad du=\cos x\,dx',
            claims=[('diff(sin(x),x)', 'cos(x)')],
            sol_rows=[('tex', r'\int\sin^{6}x\cos x\,dx=\int u^{6}du', [('sin(x)**6*cos(x)', 'sin(x)**6*diff(sin(x),x)')],
                       r'نعوّض: $\sin^6x=u^6$، و $\cos x\,dx=du$.'),
                      ('tex', r'=\frac{u^{7}}{7}', [('integrate(u**6,u)', 'u**7/7')], 'قاعدة القوة: نزيد الأس 1، ونقسم على 7.'),
                      ('line', 'sin(x)**7/7', r'نرجع $u=\sin x$.')])
    U.drill('2', 'M-30', 'P', r'$\frac{1}{\csc3x}=\sin3x$، ثم نسمّي $\cos3x$ هو $u$.',
            sol_rows=[('tex', r'\frac{e^{\cos3x}}{\csc3x}=\sin3x\,e^{\cos3x}', [('exp(cos(3*x))/csc(3*x)', 'sin(3*x)*exp(cos(3*x))')],
                       r'csc مقلوب sin. فالقسمة على $\csc3x$ تعني الضرب في $\sin3x$.'),
                      ('sub', 'cos(3*x)', '-3*sin(3*x)', r'الأس $\cos3x$، ومشتقته فيها $\sin3x$ الموجودة. نسمّي $\cos3x$ هو $u$.'),
                      ('tex', r'\sin3x\,dx=-\frac{du}{3}', [('diff(cos(3*x),x)/(-3)', 'sin(3*x)')], r'نقسم على $-3$، عشان نعوّض مكان $\sin3x\,dx$.'),
                      ('tex', r'\int\sin3x\,e^{\cos3x}dx=-\frac13\int e^{u}du', [('sin(3*x)*exp(cos(3*x))', '-Rational(1,3)*exp(cos(3*x))*diff(cos(3*x),x)')],
                       r'نعوّض. والـ $-\frac13$ تطلع برّا التكامل.'),
                      ('tex', r'=-\frac13e^{u}', [('-integrate(exp(u),u)/3', '-exp(u)/3')], 'تكامل $e^u$ هو $e^u$ نفسها.'),
                      ('line', '-exp(cos(3*x))/3', r'نرجع $u=\cos3x$.')])
    U.drill('3', 'G-76', 'P', r'نسمّي $\tan x$ هو $u$، والمشتقة $\sec^2x\,dx$ موجودة.',
            sol_rows=[('sub', 'tan(x)', 'sec(x)**2', r'فيه tan، ومشتقته $\sec^2x$ موجودة كاملة. نسمّي $\tan x$ هو $u$.'),
                      ('tex', r'\int\tan^{4}x\sec^{2}x\,dx=\int u^{4}du', [('tan(x)**4*sec(x)**2', 'tan(x)**4*diff(tan(x),x)')],
                       r'نعوّض: $\tan^4x=u^4$، و $\sec^2x\,dx=du$.'),
                      ('tex', r'=\frac{u^{5}}{5}', [('integrate(u**4,u)', 'u**5/5')], 'قاعدة القوة: نزيد الأس 1، ونقسم على 5.'),
                      ('line', 'tan(x)**5/5', r'نرجع $u=\tan x$.')])
    U.drill('4', 'G-77', 'I', r'نفصل $\sec x\tan x$، والباقي $\sec^3x$.',
            sol_rows=[('tex', r'\sec^{4}x\tan x=\sec^{3}x\cdot\sec x\tan x', [('sec(x)**4*tan(x)', 'sec(x)**3*sec(x)*tan(x)')],
                       r'مشتقة sec هي $\sec x\tan x$. فنفصلها عن الباقي.'),
                      ('sub', 'sec(x)', 'sec(x)*tan(x)', r'نسمّي $\sec x$ هو $u$.'),
                      ('tex', r'\int\sec^{3}x\cdot\sec x\tan x\,dx=\int u^{3}du', [('sec(x)**3*sec(x)*tan(x)', 'sec(x)**3*diff(sec(x),x)')],
                       r'نعوّض: $\sec^3x=u^3$، و $\sec x\tan x\,dx=du$.'),
                      ('tex', r'=\frac{u^{4}}{4}', [('integrate(u**3,u)', 'u**4/4')], 'قاعدة القوة: نزيد الأس 1، ونقسم على 4.'),
                      ('line', 'sec(x)**4/4', r'نرجع $u=\sec x$.')])
    U.drill('5', 'G-78', 'I', r'نسمّي $\sin x$ هو $u$، والجذر أس $\frac12$.',
            sol_rows=[('sub', 'sin(x)', 'cos(x)', r'داخل الجذر $\sin x$، ومشتقته $\cos x$ موجودة. نسمّي $\sin x$ هو $u$.'),
                      ('tex', r'\int\sqrt{\sin x}\cos x\,dx=\int u^{1/2}du', [('sqrt(sin(x))*cos(x)', 'sin(x)**Rational(1,2)*diff(sin(x),x)', 't/(1+t)')],
                       r'نعوّض. والجذر يصير أس $\frac12$.'),
                      ('tex', r'=\frac{u^{3/2}}{3/2}', [('integrate(u**Rational(1,2),u)', 'u**Rational(3,2)/Rational(3,2)')],
                       r'قاعدة القوة: $\frac12+1=\frac32$، ونقسم على $\frac32$.'),
                      ('tex', r'=\frac23u^{3/2}', [('u**Rational(3,2)/Rational(3,2)', '2*u**Rational(3,2)/3')], 'القسمة على كسر يعني نضرب في مقلوبه.'),
                      ('line', '2*sin(x)**Rational(3,2)/3', r'نرجع $u=\sin x$.')])
    return U


BUILDERS = {'pre42': [part_a1, part_a2, part_a3, part_a4], 'pre51': [part_b1, part_b2, part_b3],
            'pre52': [part_c1, part_c2, part_c3]}

# quick check at the start of each chapter: (question, answer latex, claims, part uid)
QUICK = {
    'pre42': [(r'اكتب $\frac{1}{x^{3}}$ بأس سالب.', r'x^{-3}', [('1/x**3', 'x**(-3)')], 'P-A1'),
              (r'اكتب $16x^{4}$ كمربع.', r'\left(4x^{2}\right)^{2}', [('16*x**4', '(4*x**2)**2')], 'P-A1'),
              (r'اشتق $(x^{2}+1)^{3}$.', r'6x\left(x^{2}+1\right)^{2}', [('diff((x**2+1)**3,x)', '6*x*(x**2+1)**2')], 'P-A2'),
              (r'$\frac{d}{dx}\cosh x=$ ؟', r'\sinh x', [('diff(cosh(x),x)', 'sinh(x)')], 'P-A3'),
              (r'$\int\frac{2x}{x^{2}+1}dx=$ ؟', r'\ln\left(x^{2}+1\right)+C', [('diff(log(x**2+1),x)', '2*x/(x**2+1)')], 'P-A4')],
    'pre51': [(r'$\frac{d}{dx}\tan^{-1}x=$ ؟', r'\frac{1}{1+x^{2}}', [('diff(atan(x),x)', '1/(1+x**2)')], 'P-B1'),
              (r'$\frac{d}{dx}\ln|5x|=$ ؟', r'\frac{1}{x}', [('diff(log(5*x),x)', '1/x', 't')], 'P-B1'),
              (r'$\int\sin2x\,dx=$ ؟', r'-\frac{\cos2x}{2}+C', [('diff(-cos(2*x)/2,x)', 'sin(2*x)')], 'P-B2'),
              (r'$\int x^{-2}dx=$ ؟', r'-\frac1x+C', [('diff(-1/x,x)', 'x**(-2)')], 'P-B2'),
              (r'$-(x-\sin x)=$ ؟ و $\ln e=$ ؟', r'-x+\sin x,\qquad 1', [('-(x-sin(x))', '-x+sin(x)'), ('log(E)', '1')], 'P-B3')],
    'pre52': [(r'$\sin^{2}x+\cos^{2}x=$ ؟ واكتب $\tan^{2}x$ بدلالة sec.', r'1,\qquad \sec^{2}x-1', [('sin(x)**2+cos(x)**2', '1'), ('tan(x)**2', 'sec(x)**2-1')], 'P-C1'),
              (r'$\frac{d}{dx}\tan x=$ ؟', r'\sec^{2}x', [('diff(tan(x),x)', 'sec(x)**2')], 'P-C1'),
              (r'فك $(1-u^{2})^{2}$.', r'1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')], 'P-C2'),
              (r'$\int u^{5}du=$ ؟', r'\frac{u^{6}}{6}+C', [('integrate(u**5,u)', 'u**6/6')], 'P-C2'),
              (r'إذا $u=\cos x$ فإن $du=$ ؟', r'-\sin x\,dx', [('diff(cos(x),x)', '-sin(x)')], 'P-C3')]}
INTRO = {
    'pre42': 'درس 4.2 عن الدوال الزائدية العكسية، ويستعمل أربعة أشياء تعلمتها قبل. الأول: الأسس والجذور، عشان تكتب اللي تحت الجذر كمربع. '
             'الثاني: قواعد الاشتقاق، عشان سؤال المشتقة. الثالث: الدوال الزائدية العادية من درس 4.1. '
             'الرابع: التكامل بالتعويض، لأن كل قوانين 4.2 مكتوبة بـ $u$.',
    'pre51': 'في درس 5.1 (التكامل بالتجزئة) تشتق $u$ وتكامل $dv$، ويستعمل ثلاثة أشياء تعلمتها قبل. '
             'الأول: مشتقات ln والدوال العكسية من درس 3.4. الثاني: التكاملات الأساسية بإشارتها الصحيحة. '
             'الثالث: التبسيط بعد القانون.',
    'pre52': 'في درس 5.2 (التكاملات المثلثية) كل سؤال بنفس الترتيب: متطابقة، ثم تعويض $u$، ثم فك قوس وتكامل حد حد. '
             'فتحتاج ثلاثة أشياء. الأول: المتطابقات ومشتقات الدوال الست. الثاني: جبر فك الأقواس. '
             'الثالث: التعويض بدالة مثلثية لما المشتقة موجودة كاملة.'}


def chapter_intro(ch):
    rows = [[link(uid, label + ' ↩'), title, '%d دقيقة' % PART_MINUTES, pgref(uid)] for uid, label, title in PARTS[ch]]
    q_rows, k_rows = [], []
    for k, (q, ans, claims, uid) in enumerate(QUICK[ch], 1):
        label = dict((u, l) for u, l, _ in PARTS[ch])[uid]
        q_rows.append([str(k), rich(q), link(uid, label)])
        k_rows.append([str(k), mi(r'\displaystyle ' + arith(ans, claims, '%s quick %d' % (ch, k))), link(uid, label)])
    KEYS.append((ch, k_rows))
    body = (p(rich(INTRO[ch]))
            + box('short', 'أجزاء هذا الفصل', table(['الجزء', 'وش فيه', 'الوقت', 'ص'], rows, 'compact'))
            + box('memo', '⏱️ اختبار سريع (3 دقائق، بدون ما تفتح شي)',
                  p('جاوب على ورقة، ثم صحّح من ' + link('k-' + ch, 'المفاتيح ص ' + pgref('k-' + ch))
                    + '. أي سؤال غلطت فيه أو ما عرفته: اقرأ جزءه بتركيز وحل كل تمارينه. وإذا جاوبت كل أسئلة الجزء صح، '
                      'يكفيك تمر على أمثلته وتحل تمرين «لحالك».')
                  + table(['#', 'السؤال', 'الجزء'], q_rows, 'compact'))
            + p(rich('<b>كيف تذاكر كل جزء:</b> اقرأ الشرح خطوة خطوة، ثم الأمثلة (غطِّ عمود «الخطوة» وحاول قبل ما تشوف)، '
                     'ثم حل التمارين في المساحة، وصحّح من الصفحة اللي بعدها.'), 'small'))
    return ('<section class="chapter prereq" id="%s"><h2>📚 %s</h2>%s</section>' % (ch, TITLES[ch], body))


def build(chapters):
    """Build chapters now (call in document order, so that algebra boxes and keys follow the page order)."""
    for ch in chapters:
        units = [fn() for fn in BUILDERS[ch]]
        HTML[ch] = chapter_intro(ch) + ''.join(U.html() for U in units)


def schedule_rows(ch):
    """(minutes, what) rows for the day plan."""
    rows = [(5, '📚 الاختبار السريع قبل درس %s' % LESSON[ch])]
    rows += [(PART_MINUTES, '📚 %s: %s، اقرأ وحل التمارين' % (label, title)) for _, label, title in PARTS[ch]]
    return rows


def sheet():
    """Formula-sheet block: 4.1 derivatives and identities, 3.4, trigonometric identities."""
    return ('<h3>من الدروس السابقة</h3>' + p('<b>4.1 الزائدية:</b>') + '<div class="fsheet">' + SHEET['hyp'] + '</div>'
            + p('<b>3.4 المثلثية العكسية:</b>') + '<div class="fsheet">' + SHEET['inv'] + '</div>'
            + p('<b>المثلثات:</b>') + '<div class="fsheet">' + SHEET['trig'] + '</div>')

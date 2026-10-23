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
from guide_kit import DRILLS_N, HELP, WRITE, Unit, alg, pgref, rich, steps_table
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
            body += p('البداية جاهزة؛ أكمل:') + md(cells[0][0]) + lines(n, 'write tight')
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
    U.why('كل تكامل في 4.2 يبدأ بكتابة ما تحت الجذر كمربعين ($16x^6=(4x^3)^2$)، وكل جواب فيه أسس وجذور تحتاج تبسيط. '
          'والتكامل بقاعدة القوة يحتاج تكتب الجذر والكسر كأس.', [('U-I1', 3), ('U-I3', 5), ('U-I4', 6), ('U-I8', 10)])
    U.explain([
        (r'الأس يعني تضرب الشيء في نفسه: $x^3$ تعني $x\cdot x\cdot x$. و $x^1=x$، و $x^0=1$.',
         r'x^{3}=x\cdot x\cdot x,\qquad x^{0}=1', [('x**3', 'x*x*x'), ('x**0', '1')]),
        (r'<b>ضرب</b> نفس الأساس: الأسس <b>تنجمع</b>.', r'x^{2}\cdot x^{3}=x^{2+3}=x^{5}', [('x**2*x**3', 'x**5')]),
        (r'<b>قسمة</b> نفس الأساس: الأسس <b>تنطرح</b> (أس الفوق ناقص أس التحت).', r'\frac{x^{5}}{x^{2}}=x^{5-2}=x^{3}', [('x**5/x**2', 'x**3')]),
        (r'<b>قوة فوق قوة</b>: الأسس <b>تنضرب</b>.', r'\left(x^{2}\right)^{3}=x^{2\cdot3}=x^{6}', [('(x**2)**3', 'x**6')]),
        (r'<b>الأس السالب</b> معناه <b>مقلوب</b>، وليس رقمًا سالبًا.', r'x^{-2}=\frac{1}{x^{2}},\qquad \frac{1}{x^{3}}=x^{-3}',
         [('x**(-2)', '1/x**2'), ('1/x**3', 'x**(-3)')]),
        (r'<b>الجذر</b> = أس كسري: الجذر التربيعي أس $\frac12$، والتكعيبي أس $\frac13$.',
         r'\sqrt{x}=x^{1/2},\qquad \frac{1}{\sqrt{x}}=x^{-1/2},\qquad \sqrt[3]{x}=x^{1/3}',
         [('sqrt(x)', 'x**Rational(1,2)', 't'), ('1/sqrt(x)', 'x**Rational(-1,2)', 't')]),
        (r'<b>قوة لحاصل ضرب</b>: كل عامل يأخذ الأس، حتى الرقم.', r'\left(3x^{2}\right)^{2}=3^{2}\cdot\left(x^{2}\right)^{2}=9x^{4}',
         [('(3*x**2)**2', '9*x**4')]),
        (r'<b>الكتابة كمربع</b> (أهم مهارة في 4.2): خذ <b>جذر الرقم</b> و<b>نصف الأس</b>.',
         r'16x^{6}=\left(4x^{3}\right)^{2},\qquad 25=5^{2},\qquad e^{6x}=\left(e^{3x}\right)^{2}',
         [('16*x**6', '(4*x**3)**2'), ('5**2', '25'), ('exp(6*x)', 'exp(3*x)**2')]),
        (r'<b>الجذر يتوزع على الضرب</b>، لكن <b>ما يتوزع على الجمع</b>.', r'\sqrt{9u}=3\sqrt{u},\qquad \sqrt{x^{2}+9}\ne x+3',
         [('sqrt(9*x)', '3*sqrt(x)', 't')])])
    rules = [(r'x^{a}\cdot x^{b}=x^{a+b}', ('x**a*x**b', 'x**(a+b)')), (r'\frac{x^{a}}{x^{b}}=x^{a-b}', ('x**a/x**b', 'x**(a-b)')),
             (r'\left(x^{a}\right)^{b}=x^{ab}', ('(x**a)**b', 'x**(a*b)', 't')), (r'x^{-a}=\frac{1}{x^{a}}', ('x**(-a)', '1/x**a')),
             (r'\sqrt{x}=x^{1/2}', ('sqrt(x)', 'x**Rational(1,2)', 't')), (r'(xy)^{a}=x^{a}y^{a}', ('(x*y)**2', 'x**2*y**2'))]
    U.add('short', 'القواعد في جدول', table(['القاعدة'], [[mi(r'\displaystyle ' + arith(lt, [c], 'P-A1 rule'))] for lt, c in rules], 'formula compact'))
    U.example('بسّط', r'x^{3}\cdot x^{-5}\cdot x^{4}', [
        (r'x^{3}\cdot x^{-5}\cdot x^{4}=x^{3+(-5)+4}', [('x**3*x**(-5)*x**4', 'x**(3-5+4)')], 'ضرب نفس الأساس ⇐ الأسس تنجمع'),
        (r'=x^{2}', [('x**(3-5+4)', 'x**2')], '$3-5+4=2$')], check='عوّض $x=2$: $8\\cdot\\frac{1}{32}\\cdot16=4=2^2$ ✓')
    arith('', [('2**3*2**(-5)*2**4', '2**2')], 'P-A1 check')
    U.example('اكتب كأس واحد (تحتاجه قبل التكامل)', r'\frac{1}{x^{2}\sqrt{x}}', [
        (r'\sqrt{x}=x^{1/2}', [('sqrt(x)', 'x**Rational(1,2)', 't')], 'الجذر أس نص'),
        (r'x^{2}\sqrt{x}=x^{2}\cdot x^{1/2}=x^{5/2}', [('x**2*sqrt(x)', 'x**Rational(5,2)', 't')], 'الأسس تنجمع: $2+\\frac12=\\frac52$'),
        (r'\frac{1}{x^{5/2}}=x^{-5/2}', [('1/(x**2*sqrt(x))', 'x**Rational(-5,2)', 't')], 'المقلوب = أس سالب')])
    U.example('اكتب ما تحت الجذر كمربعين (شكل 4.2)', r'\sqrt{25x^{6}+16}', [
        (r'25x^{6}=\left(5x^{3}\right)^{2}', [('25*x**6', '(5*x**3)**2')], 'جذر 25 هو 5، ونصف الأس 6 هو 3'),
        (r'16=4^{2}', [('4**2', '16')], 'الرقم'),
        (r'\sqrt{25x^{6}+16}=\sqrt{\left(5x^{3}\right)^{2}+4^{2}}\ \Rightarrow\ u=5x^{3},\ a=4', [('25*x**6+16', '(5*x**3)**2+4**2')],
         'هذا شكل $\\sqrt{u^2+a^2}$ في جدول 4.2')])
    U.example('ومع الأسية', r'\sqrt{e^{8x}-9}', [
        (r'e^{8x}=\left(e^{4x}\right)^{2},\qquad 9=3^{2}', [('exp(8*x)', 'exp(4*x)**2'), ('3**2', '9')], 'نصف الأس، وجذر الرقم'),
        (r'\sqrt{e^{8x}-9}=\sqrt{\left(e^{4x}\right)^{2}-3^{2}}\ \Rightarrow\ u=e^{4x},\ a=3', [('exp(8*x)-9', 'exp(4*x)**2-3**2')],
         'شكل $\\sqrt{u^2-a^2}$')])
    U.add('trap', '⚠️ الفخ', ul([rich(r'$(x+3)^2\ne x^2+9$. الصح $x^2+6x+9$ (لا تنسَ الحد الأوسط).'),
                                rich(r'$x^{-2}\ne-x^2$. الأس السالب مقلوب: $\frac{1}{x^2}$.'),
                                rich(r'$(2x)^2=4x^2$ وليس $2x^2$: الرقم يتربع أيضًا.'),
                                rich(r'$\sqrt{x^2+9}\ne x+3$: الجذر ما يتوزع على الجمع.')]))
    arith('', [('(x+3)**2', 'x**2+6*x+9'), ('(2*x)**2', '4*x**2')], 'P-A1 trap')
    U.add('ok', '✔ تأكد', p(rich('عوّض رقمًا سهلًا (مثل $x=2$) في السؤال وفي جوابك. إذا طلعوا نفس الرقم فتبسيطك صحيح.')))
    U.task('1', 'G', 'بسّط', 'اكتب كأس واحد:', r'x^{4}\cdot x^{-7}\cdot x', [
        (r'x^{4}\cdot x^{-7}\cdot x^{1}=x^{4-7+1}', [('x**4*x**(-7)*x', 'x**(4-7+1)')], 'ضرب ⇐ الأسس تنجمع، و $x=x^1$'),
        (r'4-7+1=-2', [('4-7+1', '-2')], 'نحسب الأس'),
        (r'x^{-2}=\frac{1}{x^{2}}', [('x**4*x**(-7)*x', '1/x**2')], 'الأس السالب مقلوب')], 'لا تنسَ أن $x$ وحدها أسها 1.')
    U.task('2', 'P', 'بسّط', 'اكتب كأس واحد:', r'\frac{\sqrt{x}}{x^{3}}', [
        (r'\frac{x^{1/2}}{x^{3}}=x^{\frac12-3}', [('sqrt(x)/x**3', 'x**(Rational(1,2)-3)', 't')], 'الجذر أس نص، والقسمة تطرح الأسس'),
        (r'=x^{-5/2}', [('sqrt(x)/x**3', 'x**Rational(-5,2)', 't')], '$\\frac12-3=\\frac12-\\frac62=-\\frac52$')],
           'اكتب الجذر كأس $\\frac12$ أولًا.')
    U.task('3', 'P', 'فك القوس', 'فك القوس:', r'\left(2x^{3}\right)^{4}', [
        (r'\left(2x^{3}\right)^{4}=2^{4}\cdot\left(x^{3}\right)^{4}', [('(2*x**3)**4', '2**4*(x**3)**4')], 'كل عامل يأخذ الأس'),
        (r'=16x^{12}', [('(2*x**3)**4', '16*x**12')], '$2^4=16$، والأسس تنضرب: $3\\cdot4=12$')], 'الرقم 2 أيضًا يأخذ الأس 4.')
    U.task('4', 'I', 'اكتب كمربعين', 'اكتب كمربع ناقص مربع، وطلّع $u$ و $a$:', r'49x^{4}-36', [
        (r'49x^{4}=\left(7x^{2}\right)^{2},\qquad 36=6^{2}', [('49*x**4', '(7*x**2)**2'), ('6**2', '36')], 'جذر الرقم ونصف الأس'),
        (r'49x^{4}-36=\left(7x^{2}\right)^{2}-6^{2}\ \Rightarrow\ u=7x^{2},\ a=6', [('49*x**4-36', '(7*x**2)**2-6**2')], 'شكل $u^2-a^2$')],
           'جذر 49 هو 7، ونصف الأس 4 هو 2.')
    U.task('5', 'I', 'اكتب كمربعين', 'اكتب كمربع زائد مربع، وطلّع $u$ و $a$:', r'e^{10x}+4', [
        (r'e^{10x}=\left(e^{5x}\right)^{2},\qquad 4=2^{2}', [('exp(10*x)', 'exp(5*x)**2'), ('2**2', '4')], 'نصف الأس'),
        (r'e^{10x}+4=\left(e^{5x}\right)^{2}+2^{2}\ \Rightarrow\ u=e^{5x},\ a=2', [('exp(10*x)+4', 'exp(5*x)**2+2**2')], 'شكل $u^2+a^2$')],
           'مع $e$ خذ نصف الأس، مثل $e^{6x}=(e^{3x})^2$.')
    return U


def part_a2():
    U = PreUnit('P-A2', 'أ2', 'قواعد الاشتقاق وقاعدة السلسلة', 'pre42', 'التفاضل، ومذكرة د. طارق: دروس 3.1–3.3، ص27–42')
    U.why('السؤال الأول في الكويز غالبًا «Find dy/dx»: دالة عكسية (4.2) داخل قاعدة ثانية (قوة، أو أسية، أو ln، أو ضرب). '
          'وكل سطر «✔ تأكد: اشتق جوابك» في المذكرة يحتاج هذه القواعد.', [('U-D1', 1), ('U-D2', 2)])
    U.explain([
        (r'المشتقة تعطيك سرعة تغيّر الدالة. في الكويز ما تحتاج التعريف، تحتاج <b>القواعد</b>. أهمها ثلاث: القوة، والسلسلة، والضرب.', None, []),
        (r'<b>قاعدة القوة</b>: نزّل الأس قدّام، وانقص منه 1.', r'\frac{d}{dx}x^{5}=5x^{4},\qquad \frac{d}{dx}x^{-3}=-3x^{-4}',
         [('diff(x**5,x)', '5*x**4'), ('diff(x**(-3),x)', '-3*x**(-4)')]),
        (r'الجذر: اكتبه أس $\frac12$ أولًا (أ1)، ثم القاعدة نفسها.', r'\frac{d}{dx}\sqrt{x}=\frac12x^{-1/2}=\frac{1}{2\sqrt{x}}',
         [('diff(sqrt(x),x)', '1/(2*sqrt(x))', 't')]),
        (r'الرقم وحده مشتقته صفر، والرقم المضروب يبقى، والجمع حدًا حدًا.', r'\frac{d}{dx}\left(4x^{3}-7x+2\right)=12x^{2}-7',
         [('diff(4*x**3-7*x+2,x)', '12*x**2-7')]),
        (r"<b>قاعدة السلسلة</b> (دالة داخل دالة): <b>1.</b> سمّ الداخل $u$. <b>2.</b> اشتق الخارج واترك $u$ كما هو. "
         r"<b>3.</b> اضرب في $u'$ (مشتقة الداخل).", r'\frac{d}{dx}(3x+1)^{5}=5(3x+1)^{4}\cdot3=15(3x+1)^{4}',
         [('diff((3*x+1)**5,x)', '15*(3*x+1)**4')]),
        (r"نفس الفكرة مع كل دالة: الدالة الخارجية من الجدول، ثم × $u'$.", r'\frac{d}{dx}e^{x^{2}}=e^{x^{2}}\cdot2x,\qquad \frac{d}{dx}\sin4x=4\cos4x',
         [('diff(exp(x**2),x)', '2*x*exp(x**2)'), ('diff(sin(4*x),x)', '4*cos(4*x)')]),
        (r"<b>ln</b>: مشتقة الداخل <b>على</b> الداخل.", r'\frac{d}{dx}\ln\left|x^{2}+1\right|=\frac{2x}{x^{2}+1}', [('diff(log(x**2+1),x)', '2*x/(x**2+1)')]),
        (r'<b>الضرب</b>: (مشتقة الأول × الثاني) + (الأول × مشتقة الثاني).', r'\frac{d}{dx}\left(x^{2}\sin x\right)=2x\sin x+x^{2}\cos x',
         [('diff(x**2*sin(x),x)', '2*x*sin(x)+x**2*cos(x)')]),
        (r'<b>القسمة</b>: (مشتقة الفوق × التحت − الفوق × مشتقة التحت) ÷ التحت تربيع.',
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
    U.add('short', 'جدول المشتقات (u′ = مشتقة ما داخل الدالة)', table(['المشتقة', 'تساوي'], [_row(z) for z in r], 'formula compact')
          + p(rich('$\\log$ بدون أساس = أساس 10: مشتقته مثل ln مقسومة على $\\ln10$.'), 'small'))
    U.example('أوجد المشتقة (قوة مع سلسلة)', r'y=\left(x^{2}+1\right)^{4}', [
        (r"u=x^{2}+1,\qquad u'=2x", [('diff(x**2+1,x)', '2*x')], 'نسمّي ما داخل القوس $u$ ونشتقه'),
        (r"y'=4u^{3}\cdot u'", [('diff((x**2+1)**4,x)', '4*(x**2+1)**3*diff(x**2+1,x)')], 'قاعدة القوة على الخارج، ثم × $u\'$'),
        (r"y'=4\left(x^{2}+1\right)^{3}\cdot2x=8x\left(x^{2}+1\right)^{3}", [('diff((x**2+1)**4,x)', '8*x*(x**2+1)**3')], 'نرجع $u$ ونضرب الأرقام')])
    U.example('أوجد المشتقة (أسية مع سلسلة)', r'y=e^{3x^{2}}', [
        (r"u=3x^{2},\qquad u'=6x", [('diff(3*x**2,x)', '6*x')], 'الأس كله $u$'),
        (r"y'=e^{u}\cdot u'=6x\,e^{3x^{2}}", [('diff(exp(3*x**2),x)', '6*x*exp(3*x**2)')], '$e^u$ تبقى كما هي، × $u\'$')])
    U.example('أوجد المشتقة (ln مع سلسلة داخل سلسلة)', r'y=\ln\left|\cos3x\right|', [
        (r'u=\cos3x', [('cos(3*x)', 'cos(3*x)')], 'الخارج ln، والداخل $u$'),
        (r"u'=-\sin3x\cdot3=-3\sin3x", [('diff(cos(3*x),x)', '-3*sin(3*x)')], 'cos يصير −sin، × مشتقة $3x$'),
        (r"y'=\frac{u'}{u}=\frac{-3\sin3x}{\cos3x}=-3\tan3x", [('diff(log(cos(3*x)),x)', '-3*tan(3*x)')], 'صف ln، و $\\frac{\\sin}{\\cos}=\\tan$')])
    U.example('أوجد المشتقة (ضرب)', r'y=x^{2}e^{-x}', [
        (r"f=x^{2},\ f'=2x;\qquad g=e^{-x},\ g'=-e^{-x}", [('diff(x**2,x)', '2*x'), ('diff(exp(-x),x)', '-exp(-x)')], 'جهّز القطع الأربع'),
        (r"y'=f'g+fg'=2x\,e^{-x}-x^{2}e^{-x}", [('diff(x**2*exp(-x),x)', '2*x*exp(-x)-x**2*exp(-x)')], 'قاعدة الضرب')])
    U.add('trap', '⚠️ الفخ', ul([rich("أكثر غلطة في الكويز: نسيان $u'$. مثلًا $(e^{3x})'=3e^{3x}$ وليس $e^{3x}$."),
                                rich("$(\\ln|u|)'=\\frac{u'}{u}$، وليست $\\frac1u$ فقط."),
                                rich("$(\\cos x)'=-\\sin x$ بالسالب.")]))
    arith('', [('diff(exp(3*x),x)', '3*exp(3*x)')], 'P-A2 trap')
    U.add('ok', '✔ تأكد', p(rich("كل حد فيه دالة داخل دالة لازم يطلع في مشتقته مضروب في مشتقة الداخل. إذا ما شفته، ارجع للخطوة 3.")))
    U.drill('1', 'G-46', 'G', "قوة على قوس: نزّل الأس 4، وانقص 1، ثم × $u'$.",
            first=r"u=2x^{3}-5,\quad u'=6x^{2}", claims=[('diff(2*x**3-5,x)', '6*x**2')],
            sol_rows=[('tex', r"y'=4u^{3}\cdot u'=4\left(2x^{3}-5\right)^{3}\cdot6x^{2}", [('diff((2*x**3-5)**4,x)', '4*(2*x**3-5)**3*6*x**2')],
                       'قاعدة القوة مع السلسلة'),
                      ('line', '24*x**2*(2*x**3-5)**3', 'نضرب $4\\cdot6=24$')])
    U.drill('2', 'G-47', 'P', "الأس كله $u$، و $e^u$ مشتقتها $e^u\\cdot u'$.",
            sol_rows=[('tex', r"u=x^{2}+1,\quad u'=2x", [('diff(x**2+1,x)', '2*x')], 'الأس كله $u$'),
                      ('line', '2*x*exp(x**2+1)', "$e^u\\cdot u'$")])
    U.drill('3', 'G-48', 'I', "ln: مشتقة الداخل على الداخل.",
            sol_rows=[('tex', r"u=x^{2}+3x,\quad u'=2x+3", [('diff(x**2+3*x,x)', '2*x+3')], 'الداخل ومشتقته'),
                      ('line', '(2*x+3)/(x**2+3*x)', "$\\frac{u'}{u}$")])
    U.drill('4', 'G-49', 'I', 'ضرب دالتين: جهّز $f$ و $f\'$ و $g$ و $g\'$.',
            sol_rows=[('tex', r"f=x^{3},\ f'=3x^{2};\qquad g=e^{2x},\ g'=2e^{2x}", [('diff(x**3,x)', '3*x**2'), ('diff(exp(2*x),x)', '2*exp(2*x)')],
                       'القطع الأربع (و $g\'$ فيها سلسلة)'),
                      ('line', '3*x**2*exp(2*x)+2*x**3*exp(2*x)', "$f'g+fg'$")])
    U.drill('5', 'G-50', 'I', 'حدّان: اشتق كل واحد لحاله. tan يصير $\\sec^2$، والجذر 1 على ضعفه.',
            sol_rows=[('tex', r"\frac{d}{dx}\tan5x=\sec^{2}5x\cdot5", [('diff(tan(5*x),x)', '5*sec(5*x)**2')], 'tan يصير sec² × مشتقة الداخل'),
                      ('tex', r"\frac{d}{dx}\sqrt{x^{2}+1}=\frac{2x}{2\sqrt{x^{2}+1}}=\frac{x}{\sqrt{x^{2}+1}}", [('diff(sqrt(x**2+1),x)', 'x/sqrt(x**2+1)')],
                       'الجذر: 1 على ضعف الجذر × مشتقة ما تحته'),
                      ('line', '5*sec(5*x)**2+x/sqrt(x**2+1)', 'نجمع الحدين')])
    return U


def part_a3():
    U = PreUnit('P-A3', 'أ3', 'الدوال الزائدية (درس 4.1)', 'pre42', 'مذكرة د. طارق: درس 4.1، ص49–56')
    U.why('درس 4.2 اسمه «الدوال الزائدية <b>العكسية</b>»، فلازم تعرف الدوال الزائدية العادية أولًا. سؤال المشتقة يجمع دالة عادية '
          'مثل $\\cosh(3x^2)$ مع عكسية، والتكامل بالتجزئة في 5.1 يكامل $\\sinh$ و $\\cosh$، والنوع 20 يكتبها بالأسيات.',
          [('U-D1', 1), ('U-I2', 4), ('U-P1', 12), ('U-P9', 20)])
    U.explain([
        (r'الدوال الزائدية مبنية من $e^x$ و $e^{-x}$ فقط: $\cosh$ هو <b>متوسطهما</b>، و $\sinh$ <b>نصف الفرق</b>.',
         r'\sinh x=\frac{e^{x}-e^{-x}}{2},\qquad \cosh x=\frac{e^{x}+e^{-x}}{2}', [('sinh(x)', '(exp(x)-exp(-x))/2'), ('cosh(x)', '(exp(x)+exp(-x))/2')]),
        (r'تحسب قيمتها بالتعويض في التعريف. تذكّر $e^{\ln a}=a$.', r'\cosh(\ln3)=\frac{e^{\ln3}+e^{-\ln3}}{2}=\frac{3+\frac13}{2}=\frac53',
         [('cosh(log(3))', 'Rational(5,3)')]),
        (r'الأربع الباقية قسمة، بالضبط مثل المثلثات.', r'\tanh x=\frac{\sinh x}{\cosh x},\quad \coth x=\frac{\cosh x}{\sinh x},\quad '
         r'\operatorname{sech}x=\frac{1}{\cosh x},\quad \operatorname{csch}x=\frac{1}{\sinh x}',
         [('tanh(x)', 'sinh(x)/cosh(x)'), ('coth(x)', 'cosh(x)/sinh(x)'), ('sech(x)', '1/cosh(x)'), ('csch(x)', '1/sinh(x)')]),
        (r'المتطابقة الأساسية فيها <b>سالب</b> (عكس المثلثات). ومنها $\cosh x\ge1$ دائمًا، فهو ما يصير صفرًا ولا سالبًا.',
         r'\cosh^{2}x-\sinh^{2}x=1,\qquad \cosh0=1,\qquad \sinh0=0', [('cosh(x)**2-sinh(x)**2', '1'), ('cosh(0)', '1'), ('sinh(0)', '0')]),
        (r'المشتقات مثل sin و cos، لكن <b>بدون سالب</b>: $\cosh$ مشتقته $+\sinh$.', r'\frac{d}{dx}\sinh x=\cosh x,\qquad \frac{d}{dx}\cosh x=\sinh x',
         [('diff(sinh(x),x)', 'cosh(x)'), ('diff(cosh(x),x)', 'sinh(x)')]),
        (r'ومع شيء داخلها: نفس قاعدة السلسلة (أ2).', r'\frac{d}{dx}\cosh\left(3x^{2}\right)=\sinh\left(3x^{2}\right)\cdot6x',
         [('diff(cosh(3*x**2),x)', '6*x*sinh(3*x**2)')]),
        (r'والتكامل عكس المشتقة.', r'\int\cosh x\,dx=\sinh x+C,\qquad \int\sinh x\,dx=\cosh x+C',
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
    U.add('short', 'المشتقات والتكاملات والمتطابقات', table(['المشتقة', 'تساوي'], [_row(z) for z in d], 'formula compact')
          + p(rich('الإشارة السالبة مع coth و sech و csch فقط.'), 'small')
          + table(['التكامل', 'الجواب (+C)'], [_row(z) for z in i], 'formula compact') + md(ids))
    SHEET['hyp'] = table(['المشتقة', 'تساوي'], [_row(z) for z in d], 'formula compact') + md(ids)
    U.example('أوجد المشتقة', r'y=\cosh\left(4x^{2}\right)', [
        (r"u=4x^{2},\qquad u'=8x", [('diff(4*x**2,x)', '8*x')], 'نسمّي ما داخل الدالة $u$'),
        (r"\left(\cosh u\right)'=\sinh u\cdot u'", [('diff(cosh(4*x**2),x)', 'sinh(4*x**2)*diff(4*x**2,x)')], 'cosh يصير sinh بدون سالب'),
        (r"y'=8x\sinh\left(4x^{2}\right)", [('diff(cosh(4*x**2),x)', '8*x*sinh(4*x**2)')], "نعوّض $u$ و $u'$")])
    U.example('اكتب بالأسيات (تحتاجه في النوع 20)', r'e^{x}\sinh x', [
        (r'\sinh x=\frac{e^{x}-e^{-x}}{2}', [('sinh(x)', '(exp(x)-exp(-x))/2')], 'التعريف'),
        (r'e^{x}\sinh x=\frac{e^{x}e^{x}-e^{x}e^{-x}}{2}', [('exp(x)*sinh(x)', '(exp(x)*exp(x)-exp(x)*exp(-x))/2')], 'نضرب $e^x$ في كل حد'),
        (r'=\frac{e^{2x}-1}{2}', [('exp(x)*sinh(x)', '(exp(2*x)-1)/2')], 'الأسس تنجمع: $x+x=2x$ و $x-x=0$، و $e^0=1$')])
    U.example('كامل بتعويض بسيط', r'\int\sinh3x\,dx', [
        (r'u=3x,\qquad du=3\,dx\ \Rightarrow\ dx=\frac{du}{3}', [('diff(3*x,x)', '3')], 'ما داخل الدالة'),
        (r'\int\sinh3x\,dx=\frac13\int\sinh u\,du=\frac13\cosh u', [('diff(cosh(3*x)/3,x)', 'sinh(3*x)')], 'التكامل عكس المشتقة'),
        (r'=\frac13\cosh3x+C', [('diff(cosh(3*x)/3,x)', 'sinh(3*x)')], 'نرجع $u=3x$')])
    U.add('trap', '⚠️ الفخ', ul([rich('$\\cosh^2x-\\sinh^2x=1$ بإشارة <b>سالب</b>، عكس $\\cos^2x+\\sin^2x=1$.'),
                                rich('$\\frac{d}{dx}\\cosh x=+\\sinh x$ (بدون سالب)، و $\\int\\sinh x\\,dx=+\\cosh x$.'),
                                rich('$\\sinh^{-1}x$ (العكسية، درس 4.2) ليست $\\frac{1}{\\sinh x}$؛ هذي $\\operatorname{csch}x$.')]))
    U.add('ok', '✔ تأكد', p(rich('عوّض $x=0$: $\\sinh0=0$ و $\\cosh0=1$. إذا جوابك يعطي غير هذا عند الصفر، راجع الإشارة.')))
    U.drill('1', 'G-51', 'G', "cosh يصير sinh، × $u'$.", first=r"u=5x^{2},\quad u'=10x", claims=[('diff(5*x**2,x)', '10*x')],
            sol_rows=[('line', '10*x*sinh(5*x**2)', "cosh يصير sinh بدون سالب، × $u'=10x$")])
    U.drill('2', 'G-52', 'P', "tanh يصير $\\operatorname{sech}^2$، × $u'$ و $u=e^x$.",
            sol_rows=[('tex', r"u=e^{x},\quad u'=e^{x}", [('diff(exp(x),x)', 'exp(x)')], 'الداخل'),
                      ('line', 'exp(x)*sech(exp(x))**2', "$\\operatorname{sech}^2u\\cdot u'$")])
    U.drill('3', 'G-53', 'I', "sech: مشتقتها $-\\operatorname{sech}u\\tanh u\\cdot u'$.",
            sol_rows=[('tex', r"u=3x,\quad u'=3", [('diff(3*x,x)', '3')], 'الداخل'),
                      ('line', '-3*sech(3*x)*tanh(3*x)', "صف sech بالسالب، × $u'=3$")])
    U.drill('4', 'G-54', 'P', '$u=4x$ و $dx=\\frac{du}{4}$.',
            sol_rows=[('sub', '4*x', '4', '$u=4x$'),
                      ('tex', r'\int\cosh4x\,dx=\frac14\int\cosh u\,du', [('cosh(4*x)', 'Rational(1,4)*cosh(4*x)*diff(4*x,x)')], '$dx=\\frac{du}{4}$'),
                      ('line', 'sinh(4*x)/4', 'نكامل ونرجع $u$')])
    U.drill('5', 'G-55', 'I', '$u=x^2$، ومشتقته $2x$ وعندك $x$.',
            sol_rows=[('sub', 'x**2', '2*x', '$u=x^2$'),
                      ('tex', r'\int x\sinh\left(x^{2}\right)dx=\frac12\int\sinh u\,du', [('x*sinh(x**2)', 'Rational(1,2)*sinh(x**2)*diff(x**2,x)')],
                       '$x\\,dx=\\frac{du}{2}$'),
                      ('line', 'cosh(x**2)/2', '$\\int\\sinh u\\,du=\\cosh u$')])
    U.task('6', 'I', 'احسب', 'احسب القيمة بالتعريف:', r'\sinh\left(\ln2\right)', [
        (r'\sinh(\ln2)=\frac{e^{\ln2}-e^{-\ln2}}{2}', [('sinh(log(2))', '(exp(log(2))-exp(-log(2)))/2')], 'التعريف'),
        (r'=\frac{2-\frac12}{2}=\frac{3/2}{2}=\frac34', [('sinh(log(2))', 'Rational(3,4)')], '$e^{\\ln2}=2$ و $e^{-\\ln2}=\\frac12$')],
           'عوّض في $\\frac{e^x-e^{-x}}{2}$، و $e^{\\ln a}=a$.')
    return U


def part_a4():
    U = PreUnit('P-A4', 'أ4', 'التكامل الأساسي والتعويض بـ u', 'pre42', 'مذكرة د. طارق: دروس 2.3 و2.4 (ص20–26) و3.1 و3.2')
    U.why('كل جداول 4.2 مكتوبة بـ $u$ و $du$: يعني كل تكامل في 4.2 هو تعويض. والتجزئة في 5.1 تنتهي بتكامل من الجدول الأساسي، '
          'وكل أنواع 5.2 تعويض.', [('U-I1', 3), ('U-I3', 5), ('U-I8', 10), ('U-P10', 21)])
    U.explain([
        (r"التكامل <b>عكس</b> الاشتقاق: إذا $F'=f$ فإن $\int f\,dx=F+C$. و $+C$ لأن مشتقة أي رقم صفر.",
         r'\frac{d}{dx}\left(x^{3}+5\right)=3x^{2}\ \Rightarrow\ \int3x^{2}\,dx=x^{3}+C', [('diff(x**3+5,x)', '3*x**2')]),
        (r'<b>قاعدة القوة</b>: زِد الأس 1، واقسم على الأس الجديد.', r'\int x^{4}dx=\frac{x^{5}}{5}+C,\qquad \int\frac{dx}{x^{2}}=\int x^{-2}dx=\frac{x^{-1}}{-1}=-\frac1x+C',
         [('diff(x**5/5,x)', 'x**4'), ('diff(-1/x,x)', 'x**(-2)')]),
        (r'الجذر: اكتبه أسًا أولًا (أ1). والقسمة على كسر = ضرب في مقلوبه.', r'\int\sqrt{x}\,dx=\int x^{1/2}dx=\frac{x^{3/2}}{3/2}=\frac23x^{3/2}+C',
         [('diff(2*x**Rational(3,2)/3,x)', 'sqrt(x)', 't')]),
        (r'الاستثناء الوحيد: $n=-1$ ما ينفع معه زِد الأس (يصير صفرًا).', r'\int\frac{dx}{x}=\ln|x|+C', [('diff(log(x),x)', '1/x', 't')]),
        (r'الرقم المضروب يطلع برّا، والجمع والطرح حدًا حدًا.', r'\int\left(6x^{2}+\frac{4}{x}\right)dx=2x^{3}+4\ln|x|+C',
         [('diff(2*x**3+4*log(x),x)', '6*x**2+4/x', 't')]),
        (r'<b>التعويض</b>: إذا فيه دالة داخل دالة، و<b>مشتقة الداخل موجودة جنبها</b> (أو موجودة إلا رقم)، سمّ الداخل $u$. '
         r'كأنك تعكس قاعدة السلسلة.', r'\int2x\cos\left(x^{2}\right)dx:\quad u=x^{2},\ du=2x\,dx\ \Rightarrow\ \int\cos u\,du=\sin\left(x^{2}\right)+C',
         [('diff(sin(x**2),x)', '2*x*cos(x**2)')]),
        (r'لهذا مع $e^{kx}$ و $\sin kx$… نقسم على $k$: مشتقة الداخل $kx$ هي $k$ (المثال 2 تحت).', r'\int e^{3x}dx=\frac{e^{3x}}{3}+C',
         [('diff(exp(3*x)/3,x)', 'exp(3*x)')]),
        (r'<b>تأكد دائمًا</b>: اشتق جوابك، لازم يرجع السؤال.', None, [])])
    t = [formula('x**n', 'x**(n+1)/(n+1)', var='x', branches=('t',), real=('n',), label='P-A4 power'),
         formula('1/x', 'log(Abs(x))', var='x', branches=('t', '-t'), label='P-A4 1/x'),
         formula('exp(k*x)', 'exp(k*x)/k', var='x', branches=('x',), pos=('k',), label='P-A4 e'),
         formula('sin(k*x)', '-cos(k*x)/k', var='x', branches=('x',), pos=('k',), label='P-A4 sin'),
         formula('cos(k*x)', 'sin(k*x)/k', var='x', branches=('x',), pos=('k',), label='P-A4 cos'),
         formula('sinh(k*x)', 'cosh(k*x)/k', var='x', branches=('x',), pos=('k',), label='P-A4 sinh'),
         formula('cosh(k*x)', 'sinh(k*x)/k', var='x', branches=('x',), pos=('k',), label='P-A4 cosh'),
         formula('sec(x)**2', 'tan(x)', var='x', branches=('t/(1+t)',), label='P-A4 sec2')]
    U.add('short', 'جدول التكاملات الأساسية', table(['التكامل', 'الجواب (+C)'], [_row(z) for z in t], 'formula compact')
          + p(rich('الشرط مع $x^n$: $n\\ne-1$.'), 'small'))
    U.add('short', 'التعويض بـ u: خمس خطوات ثابتة', '<ol class="method">' + ''.join('<li>%s</li>' % rich(s) for s in [
        '<b>اختر $u$</b>: الشيء اللي داخل دالة أو تحت جذر أو قوة، و<b>مشتقته موجودة جنبه</b>.',
        '<b>اشتق</b>: اكتب $du=(\\ldots)\\,dx$، وطلّع منه اللي موجود في السؤال (مثل $x\\,dx=\\frac{du}{2}$).',
        '<b>عوّض</b>: اكتب التكامل كله بدلالة $u$. لازم <b>كل</b> $x$ تختفي.',
        '<b>كامل</b> بالجدول.',
        '<b>ارجع</b> لـ $x$، وزد $+C$.']) + '</ol>')
    picks = [(r'\int\cos3x\,dx', 'u=3x', 'du=3\\,dx', r'\frac13\sin3x', ('diff(sin(3*x)/3,x)', 'cos(3*x)'), 'داخل الدالة'),
             (r'\int x\left(x^{2}+1\right)^{5}dx', 'u=x^{2}+1', 'du=2x\\,dx', r'\frac{\left(x^{2}+1\right)^{6}}{12}',
              ('diff((x**2+1)**6/12,x)', 'x*(x**2+1)**5'), 'تحت القوة، ومشتقته $2x$ موجودة'),
             (r'\int\frac{e^{x}}{1+e^{x}}dx', 'u=1+e^{x}', 'du=e^{x}dx', r'\ln\left(1+e^{x}\right)',
              ('diff(log(1+exp(x)),x)', 'exp(x)/(1+exp(x))'), 'المقام، ومشتقته في البسط'),
             (r'\int\frac{\ln x}{x}dx', 'u=\\ln x', 'du=\\frac{dx}{x}', r'\frac{\left(\ln x\right)^{2}}{2}',
              ('diff(log(x)**2/2,x)', 'log(x)/x'), '$\\frac1x$ هي مشتقته'),
             (r'\int\frac{dx}{\sqrt{4x^{2}+25}}', 'u=2x', 'du=2\\,dx', r'\frac12\sinh^{-1}\frac{2x}{5}',
              ('diff(asinh(2*x/5)/2,x)', '1/sqrt(4*x**2+25)'), 'درس 4.2: ما تحت الجذر $(2x)^2+5^2$')]
    U.add('short', 'كيف أختار u؟', table(['السؤال', 'u', 'du', 'الجواب (+C)', 'ليش هذا u'],
                                        [[mi(r'\displaystyle ' + q), mi(u), mi(r'\displaystyle ' + du), mi(r'\displaystyle ' + arith(a, [c], 'P-A4 pick')), rich(w)]
                                         for q, u, du, a, c, w in picks], 'formula compact pick'))
    U.example('البسط جزء من du', r'\int x\left(x^{2}+1\right)^{5}dx', [
        (r'u=x^{2}+1', [('x**2+1', 'x**2+1')], '<b>اختر</b>: تحت القوة، ومشتقته $2x$ وعندنا $x$'),
        (r'du=2x\,dx\ \Rightarrow\ x\,dx=\frac{du}{2}', [('diff(x**2+1,x)/2', 'x')], '<b>اشتق</b>، ونقسم على 2 لأن السؤال فيه $x\\,dx$ بس'),
        (r'\int x\left(x^{2}+1\right)^{5}dx=\frac12\int u^{5}\,du', [('x*(x**2+1)**5', 'Rational(1,2)*(x**2+1)**5*diff(x**2+1,x)')], '<b>عوّض</b>: ما بقي ولا $x$'),
        (r'=\frac12\cdot\frac{u^{6}}{6}=\frac{u^{6}}{12}', [('integrate(u**5,u)/2', 'u**6/12')], '<b>كامل</b>: زِد الأس 1 واقسم عليه'),
        (r'=\frac{\left(x^{2}+1\right)^{6}}{12}+C', [('diff((x**2+1)**6/12,x)', 'x*(x**2+1)**5')], '<b>ارجع</b> $u=x^2+1$')],
        check='اشتق الجواب: $\\frac{6(x^2+1)^5\\cdot2x}{12}=x(x^2+1)^5$ ✓ رجع السؤال.')
    U.example('ليش نقسم على k؟', r'\int\cos3x\,dx', [
        (r'u=3x,\qquad du=3\,dx\ \Rightarrow\ dx=\frac{du}{3}', [('diff(3*x,x)', '3')], '<b>اختر</b> ما داخل cos، و<b>اشتق</b>'),
        (r'\int\cos3x\,dx=\frac13\int\cos u\,du', [('cos(3*x)', 'Rational(1,3)*cos(3*x)*diff(3*x,x)')], '<b>عوّض</b>'),
        (r'=\frac13\sin u=\frac13\sin3x+C', [('diff(sin(3*x)/3,x)', 'cos(3*x)')], '<b>كامل</b> و<b>ارجع</b>. هذا سبب $\\frac1k$ في الجدول')])
    U.example('x فوق وتحت الجذر $x^2$ (يتكرر في 4.2 و5.1)', r'\int\frac{x\,dx}{\sqrt{x^{2}+9}}', [
        (r'w=x^{2}+9,\qquad dw=2x\,dx\ \Rightarrow\ x\,dx=\frac{dw}{2}', [('diff(x**2+9,x)', '2*x')], 'ما تحت الجذر كله، ومشتقته $2x$'),
        (r'=\frac12\int w^{-1/2}dw=\frac12\cdot\frac{w^{1/2}}{1/2}=w^{1/2}', [('integrate(w**Rational(-1,2),w)/2', 'w**Rational(1,2)')], 'الجذر في المقام = أس $-\\frac12$'),
        (r'=\sqrt{x^{2}+9}+C', [('diff(sqrt(x**2+9),x)', 'x/sqrt(x**2+9)')], 'نرجع $w$')])
    U.example('ln يطلع لما المقام خطي', r'\int\frac{dx}{2x+5}', [
        (r'u=2x+5,\qquad dx=\frac{du}{2}', [('diff(2*x+5,x)', '2')], 'المقام $u$'),
        (r'=\frac12\int\frac{du}{u}=\frac12\ln|u|', [('diff(log(x)/2,x)', '1/(2*x)', 't')], '$\\int\\frac{du}{u}=\\ln|u|$'),
        (r'=\frac12\ln|2x+5|+C', [('diff(log(2*x+5)/2,x)', '1/(2*x+5)', 't')], 'نرجع $u$')])
    U.add('trap', '⚠️ الفخ', ul([rich('لا تكامل وفيه $x$ و $u$ مع بعض: لازم كل $x$ تختفي أولًا.'),
                                rich('لا تنسَ الرقم اللي يطلع من $du$ (مثل $\\frac12$ أو $\\frac13$).'),
                                rich('$\\int x^2dx\\ne\\frac{x^2}{2}$: الأس يزيد 1 ($\\frac{x^3}{3}$). ولا تنسَ ترجع لـ $x$ وتزيد $+C$.')]))
    U.add('ok', '✔ تأكد', p(rich('اشتق جوابك. إذا رجع السؤال فهو صحيح.')))
    U.drill('1', 'G-56', 'G', 'حدًا حدًا بقاعدة القوة، و $\\frac{1}{x^2}=x^{-2}$.',
            first=r'\int3x^{2}dx-\int4x\,dx+\int x^{-2}dx', claims=[('3*x**2-4*x+x**(-2)', '3*x**2-4*x+1/x**2')],
            sol_rows=[('tex', r'\int3x^{2}dx=x^{3},\qquad \int4x\,dx=2x^{2},\qquad \int x^{-2}dx=-\frac1x',
                       [('diff(x**3,x)', '3*x**2'), ('diff(2*x**2,x)', '4*x'), ('diff(-1/x,x)', 'x**(-2)')], 'كل حد بقاعدة القوة'),
                      ('line', 'x**3-2*x**2-1/x', 'نجمع الحدود')])
    U.drill('2', 'G-57', 'P', '$u=-2x$، فـ $dx=-\\frac{du}{2}$.',
            sol_rows=[('sub', '-2*x', '-2', '$u=-2x$'),
                      ('tex', r'\int e^{-2x}dx=-\frac12\int e^{u}du', [('exp(-2*x)', '-Rational(1,2)*exp(-2*x)*diff(-2*x,x)')], '$dx=-\\frac{du}{2}$'),
                      ('line', '-exp(-2*x)/2', 'نكامل ونرجع $u$')])
    U.drill('3', 'G-58', 'P', '$u=x^2+4$، وعندك $x\\,dx=\\frac{du}{2}$، والجذر أس $\\frac12$.',
            sol_rows=[('sub', 'x**2+4', '2*x', '$u=x^2+4$، ومشتقته $2x$ وعندنا $x$'),
                      ('tex', r'\int x\sqrt{x^{2}+4}\,dx=\frac12\int u^{1/2}du', [('x*sqrt(x**2+4)', 'Rational(1,2)*sqrt(x**2+4)*diff(x**2+4,x)')],
                       '$x\\,dx=\\frac{du}{2}$، والجذر أس نص'),
                      ('tex', r'=\frac12\cdot\frac{u^{3/2}}{3/2}=\frac13u^{3/2}', [('integrate(u**Rational(1,2),u)/2', 'u**Rational(3,2)/3')],
                       'قاعدة القوة: $\\frac12\\cdot\\frac23=\\frac13$'),
                      ('line', '(x**2+4)**Rational(3,2)/3', 'نرجع $u$')])
    U.drill('4', 'G-59', 'I', 'المقام $u$، ومشتقته في البسط.',
            sol_rows=[('sub', '2+sin(x)', 'cos(x)', '$u=2+\\sin x$، ومشتقته $\\cos x$ في البسط'),
                      ('tex', r'=\int\frac{du}{u}=\ln|u|', [('cos(x)/(2+sin(x))', 'diff(2+sin(x),x)/(2+sin(x))')], 'التكامل بدلالة $u$'),
                      ('line', 'log(2+sin(x))', '$2+\\sin x>0$ دائمًا فلا نحتاج $|\\,|$')])
    U.drill('5', 'G-60', 'I', 'المقام خطي ⇐ $\\ln$، والـ 3 تطلع $\\frac13$.',
            sol_rows=[('sub', '3*x+2', '3', '$u=3x+2$'),
                      ('tex', r'\int\frac{dx}{3x+2}=\frac13\int\frac{du}{u}', [('1/(3*x+2)', 'Rational(1,3)*diff(3*x+2,x)/(3*x+2)')], '$dx=\\frac{du}{3}$'),
                      ('line', 'log(Abs(3*x+2))/3', '$\\int\\frac{du}{u}=\\ln|u|$')])
    return U


# ================================================================ before 5.1
def part_b1():
    U = PreUnit('P-B1', 'ب1', 'مشتقات تحتاجها التجزئة: ln والمثلثية العكسية (درس 3.4)', 'pre51', 'مذكرة د. طارق: درس 3.4، ص43–48، ودرس 3.1')
    U.why('في التجزئة تختار $u$ الشيء اللي <b>مشتقته أسهل منه</b>: ln، والدوال العكسية. فلازم تعرف مشتقاتها بدون تفكير. '
          'والنوعان 17 و18 فيهما $\\tan^{-1}$ و $\\sin^{-1}$ و $\\sec^{-1}$ من درس 3.4.', [('U-P3', 14), ('U-P4', 15), ('U-P6', 17), ('U-P7', 18)])
    U.explain([
        (r"<b>ln</b>: $\frac{d}{dx}\ln x=\frac1x$. ومع شيء داخلها: $\frac{u'}{u}$. والرقم المضروب داخل ln يختفي.",
         r'\frac{d}{dx}\ln|2x|=\frac{2}{2x}=\frac1x,\qquad \frac{d}{dx}(\ln x)^{2}=\frac{2\ln x}{x}',
         [('diff(log(2*x),x)', '1/x', 't'), ('diff(log(x)**2,x)', '2*log(x)/x', 't')]),
        (r'<b>المثلثية العكسية</b> (درس 3.4): $\sin^{-1}x$ هي الزاوية اللي $\sin$ها $x$. مشتقاتها تطلع كسور (جدول تحت).',
         r'\frac{d}{dx}\sin^{-1}x=\frac{1}{\sqrt{1-x^{2}}},\qquad \frac{d}{dx}\tan^{-1}x=\frac{1}{1+x^{2}}',
         [('diff(asin(x),x)', '1/sqrt(1-x**2)'), ('diff(atan(x),x)', '1/(1+x**2)')]),
        (r'لا تخلط مع الزائدية العكسية (4.2): نفس الشكل تقريبًا، والإشارة تحت الجذر تختلف.',
         r'\frac{d}{dx}\sinh^{-1}x=\frac{1}{\sqrt{x^{2}+1}},\qquad \frac{d}{dx}\sin^{-1}x=\frac{1}{\sqrt{1-x^{2}}}',
         [('diff(asinh(x),x)', '1/sqrt(x**2+1)')]),
        (r"ومع داخل غير $x$: نفس قاعدة السلسلة، × $u'$ (أ2).", r'\frac{d}{dx}\tan^{-1}(3x)=\frac{3}{1+9x^{2}}',
         [('diff(atan(3*x),x)', '3/(1+9*x**2)')]),
        (r'وتكاملات 3.4 تطلع لك في آخر التجزئة، مثل $\int\frac{dx}{1+x^2}=\tan^{-1}x$ (النوع 15). لكن لو البسط $x$ فهو تعويض: '
         r'$\int\frac{x\,dx}{1+x^2}=\frac12\ln(1+x^2)$ (النوع 17).', r'\int\frac{x\,dx}{1+x^{2}}=\frac12\ln\left(1+x^{2}\right)+C',
         [('diff(log(1+x**2)/2,x)', 'x/(1+x**2)')])])
    d = [formula('log(Abs(u))', '1/u', 'diff', branches=('t', '-t'), uprime=True, label='P-B1 ln'),
         formula('asin(u)', '1/sqrt(1-u**2)', 'diff', branches=('t/(1+t)', '-t/(1+t)'), uprime=True, label='P-B1 asin'),
         formula('acos(u)', '-1/sqrt(1-u**2)', 'diff', branches=('t/(1+t)', '-t/(1+t)'), uprime=True, label='P-B1 acos'),
         formula('atan(u)', '1/(1+u**2)', 'diff', branches=('x',), uprime=True, label='P-B1 atan'),
         formula('asec(u)', '1/(u*sqrt(u**2-1))', 'diff', branches=('1+t',), uprime=True, label='P-B1 asec (u > 1)')]
    i = [formula('1/sqrt(a**2-u**2)', 'asin(u/a)', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='P-B1 int asin'),
         formula('1/(a**2+u**2)', 'atan(u/a)/a', branches=('x',), pos=('a',), label='P-B1 int atan'),
         formula('1/(u*sqrt(u**2-a**2))', 'asec(u/a)/a', branches=('a+t',), pos=('a',), label='P-B1 int asec (u > a)')]
    U.add('short', 'المشتقات والتكاملات', table(['المشتقة', 'تساوي'], [_row(z) for z in d], 'formula compact')
          + p(rich('صف $\\sec^{-1}$ مكتوب لـ $u>1$ مثل مذكرة د. طارق.'), 'small')
          + table(['التكامل', 'الجواب (+C)', 'الشرط'], [_row(i[0], mi('|u|<a')), _row(i[1], 'كل ' + mi('u')), _row(i[2], mi('u>a'))], 'formula compact'))
    SHEET['inv'] = (table(['المشتقة', 'تساوي'], [_row(z) for z in d[1:]], 'formula compact')
                    + table(['التكامل', 'الجواب (+C)'], [_row(z) for z in i], 'formula compact'))
    cmp_rows = [[mi(r'\sqrt{a^{2}-u^{2}}'), mi(r'\sin^{-1}\frac{u}{a}'), '—'],
                [mi(r'\sqrt{u^{2}+a^{2}}'), '—', mi(r'\sinh^{-1}\frac{u}{a}')],
                [mi(r'\sqrt{u^{2}-a^{2}}'), '—', mi(r'\cosh^{-1}\frac{u}{a}')],
                [mi(r'a^{2}+u^{2}') + ' (بلا جذر)', mi(r'\frac1a\tan^{-1}\frac{u}{a}'), '—'],
                [mi(r'a^{2}-u^{2}') + ' (بلا جذر)', '—', mi(r'\frac1a\tanh^{-1}') + ' أو ' + mi(r'\coth^{-1}')]]
    U.add('short', 'لا تخلط: 3.4 أم 4.2؟ (شكل المقام يقرر)', table(['في المقام', '3.4 مثلثية عكسية', '4.2 زائدية عكسية'], cmp_rows, 'formula compact'))
    U.example('أوجد المشتقة', r'y=\tan^{-1}\left(x^{2}\right)', [
        (r"u=x^{2},\qquad u'=2x", [('diff(x**2,x)', '2*x')], 'ما داخل الدالة'),
        (r"y'=\frac{u'}{1+u^{2}}=\frac{2x}{1+x^{4}}", [('diff(atan(x**2),x)', '2*x/(1+x**4)')], 'صف $\\tan^{-1}$، و $(x^2)^2=x^4$')])
    U.example('أوجد المشتقة (sec⁻¹، لـ x > ⅓)', r'y=\sec^{-1}(3x)', [
        (r"u=3x,\qquad u'=3", [('diff(3*x,x)', '3')], 'ما داخل الدالة'),
        (r"y'=\frac{u'}{u\sqrt{u^{2}-1}}=\frac{3}{3x\sqrt{9x^{2}-1}}=\frac{1}{x\sqrt{9x^{2}-1}}", [('diff(asec(3*x),x)', '1/(x*sqrt(9*x**2-1))', '1/3+t')],
         'صف $\\sec^{-1}$، والـ 3 تختصر')])
    U.example('أوجد المشتقة (ضرب، مثل اللي يطلع في النوع 18)', r'y=x^{2}\tan^{-1}x', [
        (r"f=x^{2},\ f'=2x;\qquad g=\tan^{-1}x,\ g'=\frac{1}{1+x^{2}}", [('diff(atan(x),x)', '1/(1+x**2)')], 'القطع الأربع'),
        (r"y'=2x\tan^{-1}x+\frac{x^{2}}{1+x^{2}}", [('diff(x**2*atan(x),x)', '2*x*atan(x)+x**2/(1+x**2)')], "$f'g+fg'$")])
    U.example('كامل (3.4)', r'\int\frac{dx}{9+x^{2}}', [
        (r'9+x^{2}=3^{2}+x^{2}\ \Rightarrow\ a=3,\ u=x', [('9+x**2', '3**2+x**2')], 'رقم زائد مربع بلا جذر ⇐ $\\tan^{-1}$'),
        (r'\frac13\tan^{-1}\frac{x}{3}+C', [('diff(atan(x/3)/3,x)', '1/(9+x**2)')], 'صف $\\tan^{-1}$ مع $\\frac1a=\\frac13$')])
    U.add('trap', '⚠️ الفخ', ul([rich('$\\sin^{-1}x$ معكوس، وليست $\\frac{1}{\\sin x}$.'),
                                rich('$a^2+u^2$ بلا جذر ⇐ $\\tan^{-1}$ (3.4). و $a^2-u^2$ بلا جذر ⇐ $\\tanh^{-1}$ (4.2). حرف واحد يفرق.')]))
    U.add('ok', '✔ تأكد', p(rich('مشتقات الدوال العكسية كلها كسور فيها $u\'$ فوق. إذا جوابك ما فيه كسر، راجع الجدول.')))
    U.drill('1', 'G-61', 'G', "صف $\\sin^{-1}$ مع $u=2x$.", first=r"u=2x,\quad u'=2", claims=[('diff(2*x,x)', '2')],
            sol_rows=[('line', '2/sqrt(1-4*x**2)', "$\\frac{u'}{\\sqrt{1-u^2}}$، و $u^2=4x^2$")])
    U.drill('2', 'M-02', 'P', "ln والداخل فيه $\\tan^{-1}2x$.",
            sol_rows=[('tex', r"u=x^{3}+\tan^{-1}2x,\quad u'=3x^{2}+\frac{2}{1+4x^{2}}", [('diff(x**3+atan(2*x),x)', '3*x**2+2/(1+4*x**2)')],
                       'الداخل ومشتقته: صف $\\tan^{-1}$ مع $u=2x$'),
                      ('line', '(3*x**2+2/(1+4*x**2))/(x**3+atan(2*x))', "$(\\ln|u|)'=\\frac{u'}{u}$")])
    U.drill('3', 'M-01', 'P', 'ضرب: $\\sqrt x$ في $\\ln|x|$.',
            sol_rows=[('tex', r"f=\sqrt{x},\ f'=\frac{1}{2\sqrt{x}};\qquad g=\ln|x|,\ g'=\frac1x",
                       [('diff(sqrt(x),x)', '1/(2*sqrt(x))'), ('diff(log(x),x)', '1/x', 't')], 'القطع الأربع'),
                      ('tex', r"y'=\frac{\ln|x|}{2\sqrt{x}}+\sqrt{x}\cdot\frac1x", [('diff(sqrt(x)*log(x),x)', 'log(x)/(2*sqrt(x))+sqrt(x)/x', 't')],
                       "قاعدة الضرب $f'g+fg'$"),
                      ('line', 'log(Abs(x))/(2*sqrt(x))+1/sqrt(x)', '$\\frac{\\sqrt x}{x}=\\frac{1}{\\sqrt x}$ (أ1)')])
    U.drill('4', 'G-64', 'I', 'رقم زائد مربع بلا جذر ⇐ $\\tan^{-1}$، و $a=4$.',
            sol_rows=[('tex', r'16+x^{2}=4^{2}+x^{2}\ \Rightarrow\ a=4', [('16+x**2', '4**2+x**2')], 'رقم زائد مربع بلا جذر'),
                      ('line', 'atan(x/4)/4', '$\\frac1a\\tan^{-1}\\frac{x}{a}$')])
    U.drill('5', 'G-65', 'I', 'ضرب: $x$ في $\\tan^{-1}x$.',
            sol_rows=[('tex', r"f=x,\ f'=1;\qquad g=\tan^{-1}x,\ g'=\frac{1}{1+x^{2}}", [('diff(atan(x),x)', '1/(1+x**2)')], 'القطع الأربع'),
                      ('line', 'atan(x)+x/(1+x**2)', "$f'g+fg'$")])
    return U


def part_b2():
    U = PreUnit('P-B2', 'ب2', 'تكاملات تحتاجها التجزئة', 'pre51', 'مذكرة د. طارق: دروس 2.3 و2.4 و3.1 و3.2، وص52–53')
    U.why('في التجزئة تكامل $dv$ وتطلع $v$، وفي الآخر يبقى $\\int v\\,du$. هذه التكاملات لازم تطلع سريعة وبإشارتها الصحيحة، '
          'وإلا يخرب الحل كله.', [('U-P1', 12), ('U-P2', 13), ('U-P6', 17), ('U-P10', 21)])
    U.explain([
        (r'$e^{kx}$: نفسها مقسومة على $k$ (لأن مشتقة $kx$ هي $k$، أ4).', r'\int e^{4x}dx=\frac{e^{4x}}{4}+C,\qquad \int e^{-x}dx=-e^{-x}+C',
         [('diff(exp(4*x)/4,x)', 'exp(4*x)'), ('diff(-exp(-x),x)', 'exp(-x)')]),
        (r'sin و cos: <b>انتبه للإشارة</b>. $\int\sin=-\cos$ و $\int\cos=+\sin$، ونقسم على $k$.',
         r'\int\sin3x\,dx=-\frac{\cos3x}{3}+C,\qquad \int\cos3x\,dx=\frac{\sin3x}{3}+C',
         [('diff(-cos(3*x)/3,x)', 'sin(3*x)'), ('diff(sin(3*x)/3,x)', 'cos(3*x)')]),
        (r'sinh و cosh: <b>بدون سالب</b> (أ3).', r'\int\sinh2x\,dx=\frac{\cosh2x}{2}+C,\qquad \int\cosh x\,dx=\sinh x+C',
         [('diff(cosh(2*x)/2,x)', 'sinh(2*x)')]),
        (r'قوة سالبة أو كسرية (تجي مع ln في النوع 14): زِد الأس 1 واقسم عليه.', r'\int x^{-3}dx=\frac{x^{-2}}{-2}=-\frac{1}{2x^{2}}+C,\qquad \int x^{3/2}dx=\frac25x^{5/2}+C',
         [('diff(-1/(2*x**2),x)', 'x**(-3)'), ('diff(2*x**Rational(5,2)/5,x)', 'x**Rational(3,2)', 't')]),
        (r'$x$ فوق، وتحت $x^2$ مع رقم: تعويض $w$ = ما تحت الجذر أو المقام (أ4، المثال 3). تحتاجه مع الرفيق (النوع 17).',
         r'\int\frac{x\,dx}{\sqrt{1-x^{2}}}=-\sqrt{1-x^{2}}+C,\qquad \int\frac{x\,dx}{1+x^{2}}=\frac12\ln\left(1+x^{2}\right)+C',
         [('diff(-sqrt(1-x**2),x)', 'x/sqrt(1-x**2)', 't/(1+t)'), ('diff(log(1+x**2)/2,x)', 'x/(1+x**2)')])])
    m = [formula('x/sqrt(c+x**2)', 'sqrt(c+x**2)', var='x', branches=('t', '-t'), pos=('c',), label='P-B2 micro +'),
         formula('x/sqrt(c-x**2)', '-sqrt(c-x**2)', var='x', branches=('sqrt(c)*t/(1+t)',), pos=('c',), label='P-B2 micro -'),
         formula('x/(c+x**2)', 'log(c+x**2)/2', var='x', branches=('t',), pos=('c',), label='P-B2 micro ln +'),
         formula('x/(c-x**2)', '-log(Abs(c-x**2))/2', var='x', branches=('sqrt(c)*t/(1+t)', 'sqrt(c)+t'), pos=('c',), label='P-B2 micro ln -')]
    U.add('short', 'أربعة سطور تنحل بتعويض (احفظها)', table(['التكامل', 'الجواب (+C)'], [_row(z) for z in m], 'formula compact')
          + p(rich('السالب مع $c-x^2$ لأن مشتقة $c-x^2$ هي $-2x$.'), 'small'))
    U.example('كامل (بالتعويض، عشان تشوف من وين يجي السالب)', r'\int\sin3x\,dx', [
        (r'u=3x,\qquad dx=\frac{du}{3}', [('diff(3*x,x)', '3')], 'ما داخل الدالة'),
        (r'\int\sin3x\,dx=\frac13\int\sin u\,du=\frac13\left(-\cos u\right)', [('diff(-cos(x),x)', 'sin(x)')], '$\\int\\sin u\\,du=-\\cos u$'),
        (r'=-\frac13\cos3x+C', [('diff(-cos(3*x)/3,x)', 'sin(3*x)')], 'نرجع $u$')])
    U.example('قوة سالبة', r'\int\frac{dx}{x^{3}}', [
        (r'\frac{1}{x^{3}}=x^{-3}', [('1/x**3', 'x**(-3)')], 'نكتبه كأس (أ1)'),
        (r'\int x^{-3}dx=\frac{x^{-3+1}}{-3+1}=\frac{x^{-2}}{-2}', [('diff(x**(-2)/(-2),x)', 'x**(-3)')], 'زِد الأس 1: $-3+1=-2$'),
        (r'=-\frac{1}{2x^{2}}+C', [('x**(-2)/(-2)', '-1/(2*x**2)')], 'الأس السالب مقلوب، والسالب قدّام')])
    U.example('x فوق جذر $1-x^2$ (الرفيق مع sin⁻¹)', r'\int\frac{x\,dx}{\sqrt{1-x^{2}}}', [
        (r'w=1-x^{2},\qquad dw=-2x\,dx\ \Rightarrow\ x\,dx=-\frac{dw}{2}', [('diff(1-x**2,x)', '-2*x')], 'ما تحت الجذر، ومشتقته $-2x$'),
        (r'=-\frac12\int w^{-1/2}dw=-\frac12\cdot2w^{1/2}=-w^{1/2}', [('-integrate(w**Rational(-1,2),w)/2', '-w**Rational(1,2)')], 'قاعدة القوة'),
        (r'=-\sqrt{1-x^{2}}+C', [('diff(-sqrt(1-x**2),x)', 'x/sqrt(1-x**2)', 't/(1+t)')], 'نرجع $w$. السالب جا من $dw$')])
    U.add('trap', '⚠️ الفخ', ul([rich('$\\int\\sin x\\,dx=-\\cos x$ (بالسالب)، لكن $\\int\\sinh x\\,dx=+\\cosh x$.'),
                                rich('$\\int e^{-x}dx=-e^{-x}$: القسمة على $k=-1$ تعطي سالب.'),
                                rich('$\\int x^{-1}dx$ ما ينفع معه قاعدة القوة: هو $\\ln|x|$.')]))
    U.add('ok', '✔ تأكد', p(rich('اشتق جوابك. هنا السهل تغلط في الإشارة، والاشتقاق يكشفها فورًا.')))
    U.drill('1', 'M-03', 'G', '$u=8x+1$، و $\\int e^u du=e^u$.', first=r'u=8x+1,\quad dx=\frac{du}{8}', claims=[('diff(8*x+1,x)', '8')],
            sol_rows=[('tex', r'\int e^{8x+1}dx=\frac18\int e^{u}\,du', [('exp(8*x+1)', 'Rational(1,8)*exp(8*x+1)*diff(8*x+1,x)')], 'نعوّض'),
                      ('line', 'exp(8*x+1)/8', '$\\int e^u\\,du=e^u$، ونرجع $u$')])
    U.drill('2', 'G-67', 'P', 'sinh تكامله cosh بدون سالب، ونقسم على 2.',
            sol_rows=[('sub', '2*x', '2', '$u=2x$'),
                      ('tex', r'\int\sinh2x\,dx=\frac12\int\sinh u\,du', [('sinh(2*x)', 'Rational(1,2)*sinh(2*x)*diff(2*x,x)')], '$dx=\\frac{du}{2}$'),
                      ('line', 'cosh(2*x)/2', '$\\int\\sinh u\\,du=\\cosh u$')])
    U.drill('3', 'G-68', 'P', 'زِد الأس 1: $-4+1=-3$، واقسم عليه.',
            sol_rows=[('tex', r'\int x^{-4}dx=\frac{x^{-3}}{-3}', [('diff(x**(-3)/(-3),x)', 'x**(-4)', 't')], 'قاعدة القوة'),
                      ('line', '-1/(3*x**3)', 'الأس السالب مقلوب')])
    U.drill('4', 'G-69', 'I', 'تعويض $w=x^2-1$ (ما تحت الجذر).',
            sol_rows=[('sub', 'x**2-1', '2*x', '$w=x^2-1$', 'w', '1+t'),
                      ('tex', r'=\frac12\int w^{-1/2}dw=w^{1/2}', [('integrate(w**Rational(-1,2),w)/2', 'w**Rational(1,2)')], '$x\\,dx=\\frac{dw}{2}$'),
                      ('line', 'sqrt(x**2-1)', 'نرجع $w$')])
    U.drill('5', 'M-04', 'I', 'البسط نص مشتقة المقام.',
            sol_rows=[('sub', 'x**2+2*sin(x)', '2*x+2*cos(x)', '$w=$ المقام، ومشتقته $2x+2\\cos x=2(x+\\cos x)$', 'w', 't'),
                      ('tex', r'=\frac12\int\frac{dw}{w}', [('(x+cos(x))/(x**2+2*sin(x))', 'Rational(1,2)*diff(x**2+2*sin(x),x)/(x**2+2*sin(x))')],
                       'البسط $=\\frac12\\,dw$، و $\\int\\frac{dw}{w}=\\ln|w|$، ثم نرجع $w$')])
    return U


def part_b3():
    U = PreUnit('P-B3', 'ب3', 'تبسيط درس 5.1', 'pre51', 'جبر، ومذكرة د. طارق: دروس 3.1 و3.2')
    U.why('أغلب أخطاء التجزئة مو في الطريقة، في التبسيط: سالب قدّام قوس، وكسر في كسر، وقسمة بسيطة، وقيم ln و e في المحدد، '
          'ومعادلة فيها $I$ في الدوران.', [('U-P2', 13), ('U-P5', 16), ('U-P7', 18), ('U-P8', 19), ('U-P9', 20)])
    U.explain([
        (r'<b>سالب قدّام قوس</b> يقلب إشارة <b>كل</b> حد داخله.', r'-\left(2x\cos x-2\sin x\right)=-2x\cos x+2\sin x',
         [('-(2*x*cos(x)-2*sin(x))', '-2*x*cos(x)+2*sin(x)')]),
        (r'<b>ضرب كسرين</b>: فوق × فوق، وتحت × تحت، ثم اختصر.', r'\frac{x^{3}}{3}\cdot\frac1x=\frac{x^{3}}{3x}=\frac{x^{2}}{3}', [('x**3/3*(1/x)', 'x**2/3')]),
        (r'<b>قسمة بسيطة</b> لما درجة الفوق = درجة التحت: اكتب الفوق بدلالة التحت، ثم افصل.',
         r'\frac{x^{2}}{1+x^{2}}=\frac{(1+x^{2})-1}{1+x^{2}}=1-\frac{1}{1+x^{2}}', [('x**2/(1+x**2)', '1-1/(1+x**2)')]),
        (r'<b>قيم لازم تحفظها</b> (للتكامل المحدد، النوع 16).', r'\ln1=0,\quad \ln e=1,\quad e^{0}=1,\quad e^{\ln a}=a,\quad \sin0=0,\quad \cos0=1',
         [('log(1)', '0'), ('log(E)', '1'), ('exp(0)', '1'), ('exp(log(7))', '7'), ('cos(0)', '1')]),
        (r'<b>المحدد</b>: عوّض الحد الأعلى ثم اطرح تعويض الحد الأدنى، وضع الثاني بين قوسين.', r'\left[x^{2}\right]_{1}^{3}=3^{2}-1^{2}=8', [('3**2-1**2', '8')]),
        (r'<b>إذا رجع التكامل نفسه</b> ($I$) في الطرف الثاني (النوع 19): اجمعه في طرف وحده، ثم اقسم.',
         r'I=A-\frac14I\ \Rightarrow\ \frac54I=A\ \Rightarrow\ I=\frac45A', [('Rational(4,5)*A+Rational(1,4)*Rational(4,5)*A', 'A')]),
        (r'<b>ضرب الأسيات</b>: الأسس تنجمع (النوع 20).', r'e^{x}\cdot e^{2x}=e^{3x},\qquad e^{x}\cdot\frac{e^{2x}+e^{-2x}}{2}=\frac{e^{3x}+e^{-x}}{2}',
         [('exp(x)*exp(2*x)', 'exp(3*x)'), ('exp(x)*(exp(2*x)+exp(-2*x))/2', '(exp(3*x)+exp(-x))/2')])])
    U.example('وزّع وبسّط (يطلع في النوع 13)', r'x^{2}\sin x-2\left(x\cos x-\sin x\right)', [
        (r'-2\left(x\cos x-\sin x\right)=-2x\cos x+2\sin x', [('-2*(x*cos(x)-sin(x))', '-2*x*cos(x)+2*sin(x)')], '−2 يدخل على كل حد'),
        (r'=x^{2}\sin x-2x\cos x+2\sin x', [('x**2*sin(x)-2*(x*cos(x)-sin(x))', 'x**2*sin(x)-2*x*cos(x)+2*sin(x)')], 'نكتب الكل')])
    U.example('قسمة بسيطة (يطلع في النوعين 15 و18)', r'\frac{2x^{2}}{1+x^{2}}', [
        (r'2x^{2}=2\left(1+x^{2}\right)-2', [('2*x**2', '2*(1+x**2)-2')], 'نكتب البسط بدلالة المقام'),
        (r'\frac{2x^{2}}{1+x^{2}}=\frac{2(1+x^{2})}{1+x^{2}}-\frac{2}{1+x^{2}}=2-\frac{2}{1+x^{2}}', [('2*x**2/(1+x**2)', '2-2/(1+x**2)')], 'نفصل، ونختصر')])
    U.example('احسب (محدد)', r'\left[x\ln x-x\right]_{1}^{e}', [
        (r'F(e)=e\cdot\ln e-e=e-e=0', [('E*log(E)-E', '0')], '$\\ln e=1$'),
        (r'F(1)=1\cdot\ln1-1=0-1=-1', [('1*log(1)-1', '-1')], '$\\ln1=0$'),
        (r'F(e)-F(1)=0-(-1)=1', [('0-(-1)', '1')], 'سالب في سالب = موجب')])
    U.example('حل للتكامل I (الدوران)', r'I=e^{x}\sin x-I', [
        (r'I+I=e^{x}\sin x\ \Rightarrow\ 2I=e^{x}\sin x', [('exp(x)*sin(x)/2+exp(x)*sin(x)/2', 'exp(x)*sin(x)')], 'ننقل $I$ للطرف الأول'),
        (r'I=\frac{e^{x}\sin x}{2}', [('exp(x)*sin(x)/2', 'exp(x)*sin(x)-exp(x)*sin(x)/2')], 'نقسم على 2، ونتأكد بالتعويض')])
    U.add('trap', '⚠️ الفخ', ul([rich('$-(a-b)=-a+b$: الحد الثاني إشارته تنقلب.'),
                                rich('$\\frac{1}{a+b}\\ne\\frac1a+\\frac1b$: المقام ما ينفصل.'),
                                rich('في المحدد: $F(b)-F(a)$ وليس العكس، والقوس حول $F(a)$.')]))
    U.add('ok', '✔ تأكد', p(rich('بعد التبسيط عوّض رقمًا (مثل $x=1$) في السطر قبل وبعد. لازم نفس الرقم.')))
    U.task('1', 'G', 'وزّع', 'وزّع السالب:', r'-\left(2xe^{x}-2e^{x}\right)', [
        (r'-\left(2xe^{x}\right)-\left(-2e^{x}\right)', [('-(2*x*exp(x)-2*exp(x))', '-(2*x*exp(x))-(-2*exp(x))')], 'السالب يدخل على كل حد'),
        (r'=-2xe^{x}+2e^{x}', [('-(2*x*exp(x)-2*exp(x))', '-2*x*exp(x)+2*exp(x)')], 'سالب في سالب = موجب')], 'السالب يقلب إشارة الحدين.')
    U.task('2', 'P', 'قسّم', 'اكتب كعدد ناقص كسر:', r'\frac{x^{2}}{x^{2}+4}', [
        (r'\frac{x^{2}}{x^{2}+4}=\frac{(x^{2}+4)-4}{x^{2}+4}', [('x**2/(x**2+4)', '((x**2+4)-4)/(x**2+4)')], 'نزيد 4 وننقص 4 في البسط'),
        (r'=1-\frac{4}{x^{2}+4}', [('x**2/(x**2+4)', '1-4/(x**2+4)')], 'نفصل')], 'اكتب البسط $x^2=(x^2+4)-4$.')
    U.task('3', 'P', 'احسب', 'احسب:', r'\left[x^{2}\ln x-\frac{x^{2}}{2}\right]_{1}^{e}', [
        (r'F(e)=e^{2}\cdot1-\frac{e^{2}}{2}=\frac{e^{2}}{2}', [('E**2*log(E)-E**2/2', 'E**2/2')], '$\\ln e=1$'),
        (r'F(1)=1\cdot0-\frac12=-\frac12', [('1*log(1)-Rational(1,2)', '-Rational(1,2)')], '$\\ln1=0$'),
        (r'F(e)-F(1)=\frac{e^{2}}{2}-\left(-\frac12\right)=\frac{e^{2}+1}{2}', [('E**2/2-(-Rational(1,2))', '(E**2+1)/2')], 'سالب في سالب')],
           'عوّض $e$ ثم 1، و $\\ln e=1$ و $\\ln1=0$.')
    U.task('4', 'I', 'حل', 'حل للتكامل $I$:', r'I=A-\frac{1}{16}I', [
        (r'I+\frac{1}{16}I=\frac{17}{16}I=A', [('1+Rational(1,16)', 'Rational(17,16)')], 'نجمع $I$ في طرف'),
        (r'I=\frac{16}{17}A', [('Rational(16,17)*A+Rational(1,16)*Rational(16,17)*A', 'A')], 'نضرب في المقلوب، ونتأكد بالتعويض')],
           'انقل $\\frac{1}{16}I$ للطرف الأول.')
    U.task('5', 'I', 'بسّط', 'اكتب بالأسيات وبسّط:', r'e^{x}\cosh x', [
        (r'\cosh x=\frac{e^{x}+e^{-x}}{2}', [('cosh(x)', '(exp(x)+exp(-x))/2')], 'التعريف (أ3)'),
        (r'e^{x}\cosh x=\frac{e^{2x}+e^{0}}{2}=\frac{e^{2x}+1}{2}', [('exp(x)*cosh(x)', '(exp(2*x)+1)/2')], 'الأسس تنجمع، و $e^0=1$')],
           'عوّض التعريف واضرب $e^x$ في كل حد.')
    return U


# ================================================================ before 5.2
def part_c1():
    U = PreUnit('P-C1', 'ج1', 'المثلثات: المتطابقات، وضعف الزاوية ونصفها، والمشتقات', 'pre52',
                'من مقررات قبل ريض 111؛ مذكرة د. طارق تستعملها في 5.2 (ص67)')
    U.why('كل أنواع 5.2 تبدأ بمتطابقة: نحوّل الباقي بعد الحجز ($\\cos^2x=1-\\sin^2x$)، أو نخفّض الأس بنصف الزاوية، أو نحوّل الضرب لجمع. '
          'ولازم تعرف مشتقات الست عشان تعرف وش تحجز.', [('U-T1', 22), ('U-T3', 24), ('U-T4', 25), ('U-T6', 27), ('U-T8', 29)])
    U.explain([
        (r'الأساس: $\sin^2x+\cos^2x=1$. اقسم الطرفين على $\cos^2x$ تطلع الثانية، وعلى $\sin^2x$ الثالثة.',
         r'\frac{\sin^{2}x}{\cos^{2}x}+\frac{\cos^{2}x}{\cos^{2}x}=\frac{1}{\cos^{2}x}\ \Rightarrow\ \tan^{2}x+1=\sec^{2}x', [('tan(x)**2+1', 'sec(x)**2')]),
        (r'وكل وحدة تنكتب بثلاث صور. أهمها اللي تحوّل الباقي في 5.2.', r'\cos^{2}x=1-\sin^{2}x,\qquad \tan^{2}x=\sec^{2}x-1,\qquad \cot^{2}x=\csc^{2}x-1',
         [('cos(x)**2', '1-sin(x)**2'), ('tan(x)**2', 'sec(x)**2-1'), ('cot(x)**2', 'csc(x)**2-1')]),
        (r'<b>ضعف الزاوية</b>: $\sin2x=2\sin x\cos x$. و $\cos2x$ له ثلاث صور.', r'\cos2x=\cos^{2}x-\sin^{2}x=2\cos^{2}x-1=1-2\sin^{2}x',
         [('cos(2*x)', '2*cos(x)**2-1'), ('cos(2*x)', '1-2*sin(x)**2')]),
        (r'<b>نصف الزاوية</b> (من صور $\cos2x$): تخفّض الأس 2 إلى 1. مع $\cos^2$ زائد، ومع $\sin^2$ ناقص، والزاوية تتضاعف.',
         r'\cos^{2}x=\frac{1+\cos2x}{2},\qquad \sin^{2}4x=\frac{1-\cos8x}{2}', [('cos(x)**2', '(1+cos(2*x))/2'), ('sin(4*x)**2', '(1-cos(8*x))/2')]),
        (r'<b>المشتقات الست</b>: كل دالة تبدأ بـ «co» مشتقتها سالبة.', r'\frac{d}{dx}\tan x=\sec^{2}x,\qquad \frac{d}{dx}\sec x=\sec x\tan x,\qquad \frac{d}{dx}\cot x=-\csc^{2}x',
         [('diff(tan(x),x)', 'sec(x)**2'), ('diff(sec(x),x)', 'sec(x)*tan(x)'), ('diff(cot(x),x)', '-csc(x)**2')]),
        (r'<b>والتكاملات عكسها</b>، واثنين تحفظهم: $\int\tan x=\ln|\sec x|$ و $\int\sec x=\ln|\sec x+\tan x|$.',
         r'\int\sec^{2}x\,dx=\tan x+C,\qquad \int\sec x\tan x\,dx=\sec x+C', [('diff(tan(x),x)', 'sec(x)**2'), ('diff(sec(x),x)', 'sec(x)*tan(x)')])])
    U.raw(alg('trig-pyth', 'متطابقات فيثاغورس', [
        (r'\sin^{2}x+\cos^{2}x=1', [('sin(x)**2+cos(x)**2', '1')], 'الأساس:'),
        (r'\cos^{2}x=1-\sin^{2}x,\qquad \sin^{2}x=1-\cos^{2}x', [('cos(x)**2', '1-sin(x)**2')], 'ننقل حدًا للطرف الثاني:'),
        (r'\sec^{2}x=1+\tan^{2}x,\qquad \csc^{2}x=1+\cot^{2}x', [('sec(x)**2', '1+tan(x)**2'), ('csc(x)**2', '1+cot(x)**2')],
         'نقسم الأساس على $\\cos^2x$ أو $\\sin^2x$ (تحتاجهما مع tan و cot):')]))
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
    dbl = [(r'\sin2x=2\sin x\cos x', ('sin(2*x)', '2*sin(x)*cos(x)')),
           (r'\cos^{2}x=\frac{1+\cos2x}{2},\qquad \sin^{2}x=\frac{1-\cos2x}{2}', ('sin(x)**2', '(1-cos(2*x))/2')),
           (r'\sin(-\theta)=-\sin\theta,\qquad \cos(-\theta)=\cos\theta', ('sin(-x)+sin(x)', '0'))]
    dbl_t = table(['المتطابقة'], [[mi(r'\displaystyle ' + arith(lt, [c], 'P-C1 identity'))] for lt, c in dbl], 'formula compact')
    U.add('short', 'الجداول', table(['المشتقة', 'تساوي'], [_row(z) for z in d6], 'formula compact')
          + table(['التكامل', 'الجواب (+C)'], [_row(z) for z in i6], 'formula compact') + dbl_t)
    SHEET['trig'] = (table(['المتطابقة'], [[mi(r'\displaystyle \sin^{2}x+\cos^{2}x=1,\quad \sec^{2}x=1+\tan^{2}x,\quad \csc^{2}x=1+\cot^{2}x')]], 'formula compact')
                     + dbl_t)
    U.example('أوجد المشتقة', r'y=\sec3x', [
        (r"u=3x,\qquad u'=3", [('diff(3*x,x)', '3')], 'ما داخل الدالة'),
        (r"y'=\sec u\tan u\cdot u'=3\sec3x\tan3x", [('diff(sec(3*x),x)', '3*sec(3*x)*tan(3*x)')], 'صف sec، × $u\'$')])
    U.example('خفّض الأس (النوع 24)', r'\sin^{2}x\cos^{2}x', [
        (r'\sin x\cos x=\frac12\sin2x', [('sin(x)*cos(x)', 'sin(2*x)/2')], 'من $\\sin2x=2\\sin x\\cos x$'),
        (r'\sin^{2}x\cos^{2}x=\frac14\sin^{2}2x', [('sin(x)**2*cos(x)**2', 'sin(2*x)**2/4')], 'نربّع الطرفين'),
        (r'=\frac14\cdot\frac{1-\cos4x}{2}=\frac{1-\cos4x}{8}', [('sin(x)**2*cos(x)**2', '(1-cos(4*x))/8')], 'نصف الزاوية مع $2x$: الزاوية تصير $4x$')])
    U.example('حوّل للحجز (الأنواع 22–28)', r'\tan^{3}x', [
        (r'\tan^{3}x=\tan x\cdot\tan^{2}x', [('tan(x)**3', 'tan(x)*tan(x)**2')], 'نفصل مربعًا'),
        (r'=\tan x\left(\sec^{2}x-1\right)', [('tan(x)**3', 'tan(x)*(sec(x)**2-1)')], 'من $\\sec^2x=1+\\tan^2x$')])
    U.add('trap', '⚠️ الفخ', ul([rich('$\\sin2x\\ne2\\sin x$. الصح $2\\sin x\\cos x$.'),
                                rich('$\\sin^2x$ تعني $(\\sin x)^2$، وليست $\\sin(x^2)$.'),
                                rich('مشتقة $\\cos$ و $\\cot$ و $\\csc$ سالبة؛ و $\\int\\sin=-\\cos$.')]))
    U.add('ok', '✔ تأكد', p(rich('عوّض $x=0$ في متطابقتك: $\\sin0=0$ و $\\cos0=1$. لازم الطرفين يتساوون.')))
    U.task('1', 'G', 'اكتب بنصف الزاوية', 'اكتب بنصف الزاوية:', r'\cos^{2}5x', [
        (r'\cos^{2}\theta=\frac{1+\cos2\theta}{2}', [('cos(x)**2', '(1+cos(2*x))/2')], 'مع $\\cos^2$ زائد'),
        (r'\theta=5x:\qquad \cos^{2}5x=\frac{1+\cos10x}{2}', [('cos(5*x)**2', '(1+cos(10*x))/2')], 'الزاوية تتضاعف: $2\\cdot5x=10x$')],
           'الزاوية داخل cos تتضاعف.')
    U.drill('2', 'G-71', 'P', "sec يصير $\\sec u\\tan u$، × $u'$ و $u=x^2$.",
            sol_rows=[('tex', r"u=x^{2},\quad u'=2x", [('diff(x**2,x)', '2*x')], 'الداخل'),
                      ('line', '2*x*sec(x**2)*tan(x**2)', "$\\sec u\\tan u\\cdot u'$")])
    U.drill('3', 'G-72', 'P', '$\\int\\sec^2u\\,du=\\tan u$، و $u=3x$.',
            sol_rows=[('sub', '3*x', '3', '$u=3x$'),
                      ('tex', r'\int\sec^{2}3x\,dx=\frac13\int\sec^{2}u\,du', [('sec(3*x)**2', 'Rational(1,3)*sec(3*x)**2*diff(3*x,x)')], '$dx=\\frac{du}{3}$'),
                      ('line', 'tan(3*x)/3', '$\\int\\sec^2u\\,du=\\tan u$')])
    U.drill('4', 'G-73', 'I', 'وش الدالة اللي مشتقتها $-\\csc x\\cot x$؟',
            sol_rows=[('tex', r'\frac{d}{dx}\csc x=-\csc x\cot x', [('diff(csc(x),x)', '-csc(x)*cot(x)')], 'نبحث عن دالة مشتقتها $\\csc x\\cot x$'),
                      ('line', '-csc(x)', 'نضرب في سالب حتى تطلع موجبة')])
    U.task('5', 'I', 'حوّل', 'اكتب كـ $\\cos x$ مضروب في شيء بدلالة $\\sin x$ فقط:', r'\cos^{5}x', [
        (r'\cos^{5}x=\cos^{4}x\cdot\cos x=\left(\cos^{2}x\right)^{2}\cos x', [('cos(x)**5', '(cos(x)**2)**2*cos(x)')], 'نفصل $\\cos x$، والباقي مربع'),
        (r'=\left(1-\sin^{2}x\right)^{2}\cos x', [('cos(x)**5', '(1-sin(x)**2)**2*cos(x)')], '$\\cos^2x=1-\\sin^2x$')],
           'افصل $\\cos x$ واحدة، والباقي $\\cos^4x=(\\cos^2x)^2$.')
    return U


def part_c2():
    U = PreUnit('P-C2', 'ج2', 'تبسيط درس 5.2: فك القوس، والتوزيع، والتكامل حدًا حدًا', 'pre52', 'جبر، ومذكرة د. طارق: درس 2.3')
    U.why('بعد التعويض في 5.2 يصير عندك كثيرة حدود في $u$ داخل أقواس. الحل كله: فك القوس، ثم وزّع، ثم كامل كل حد. '
          'هذي الخطوات هي أكثر مكان تجي فيه أخطاء الجبر.', [('U-T1', 22), ('U-T2', 23), ('U-T5', 26), ('U-T7', 28)])
    U.explain([
        (r'<b>مربع قوس</b>: $(a-b)^2=a^2-2ab+b^2$. لا تنسَ <b>الحد الأوسط</b>.', r'(1-u^{2})^{2}=1-2u^{2}+u^{4},\qquad (u^{2}-1)^{2}=u^{4}-2u^{2}+1',
         [('(1-u**2)**2', '1-2*u**2+u**4'), ('(u**2-1)**2', 'u**4-2*u**2+1')]),
        (r'<b>تكعيب قوس</b>: المعاملات 1، 3، 3، 1. مع زائد كلها موجبة، ومع ناقص الإشارات تتناوب.',
         r'(1+u^{2})^{3}=1+3u^{2}+3u^{4}+u^{6}', [('(1+u**2)**3', '1+3*u**2+3*u**4+u**6')]),
        (r'<b>توزيع $u^k$ على القوس</b>: اضرب في كل حد، والأسس تنجمع (أ1).', r'u^{3}\left(1-2u^{2}+u^{4}\right)=u^{3}-2u^{5}+u^{7}',
         [('u**3*(1-2*u**2+u**4)', 'u**3-2*u**5+u**7')]),
        (r'<b>تكامل كثيرة الحدود</b>: حدًا حدًا، كل حد يزيد أسه 1 ويُقسم عليه، والمعامل يبقى.',
         r'\int\left(u^{3}-2u^{5}+u^{7}\right)du=\frac{u^{4}}{4}-\frac{2u^{6}}{6}+\frac{u^{8}}{8}=\frac{u^{4}}{4}-\frac{u^{6}}{3}+\frac{u^{8}}{8}+C',
         [('integrate(u**3-2*u**5+u**7,u)', 'u**4/4-u**6/3+u**8/8')]),
        (r'<b>أسس كسرية</b> (مثل $\sqrt{\sin x}=u^{1/2}$): نفس القاعدة، والقسمة على كسر = ضرب في مقلوبه.',
         r'\int u^{5/2}du=\frac{u^{7/2}}{7/2}=\frac27u^{7/2}+C', [('integrate(u**Rational(5,2),u)', '2*u**Rational(7,2)/7')]),
        (r'<b>إذا $du$ فيه سالب</b> (مثل $u=\cos x$، $du=-\sin x\,dx$): السالب يطلع قدّام التكامل <b>كله</b>.',
         r'\int\cos^{2}x\sin x\,dx=-\int u^{2}du=-\frac{u^{3}}{3}=-\frac{\cos^{3}x}{3}+C', [('diff(-cos(x)**3/3,x)', 'cos(x)**2*sin(x)')])])
    U.example('فك ثم وزّع ثم كامل', r'\int u^{2}\left(1-u^{2}\right)^{2}du', [
        (r'(1-u^{2})^{2}=1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')], 'فك القوس وحده أولًا'),
        (r'u^{2}\left(1-2u^{2}+u^{4}\right)=u^{2}-2u^{4}+u^{6}', [('u**2*(1-2*u**2+u**4)', 'u**2-2*u**4+u**6')], 'وزّع $u^2$: الأسس تنجمع'),
        (r'\int\left(u^{2}-2u^{4}+u^{6}\right)du=\frac{u^{3}}{3}-\frac{2u^{5}}{5}+\frac{u^{7}}{7}+C',
         [('integrate(u**2-2*u**4+u**6,u)', 'u**3/3-2*u**5/5+u**7/7')], 'كل حد: زِد الأس 1 واقسم عليه')])
    U.example('أس كسري', r'\int u^{1/2}\left(1-u^{2}\right)du', [
        (r'u^{1/2}\left(1-u^{2}\right)=u^{1/2}-u^{5/2}', [('u**Rational(1,2)*(1-u**2)', 'u**Rational(1,2)-u**Rational(5,2)', 't')], 'وزّع: $\\frac12+2=\\frac52$'),
        (r'\int\left(u^{1/2}-u^{5/2}\right)du=\frac{u^{3/2}}{3/2}-\frac{u^{7/2}}{7/2}', [('diff(u**Rational(3,2)/Rational(3,2)-u**Rational(7,2)/Rational(7,2),u)', 'u**Rational(1,2)-u**Rational(5,2)', 't')],
         'زِد الأس 1'),
        (r'=\frac23u^{3/2}-\frac27u^{7/2}+C', [('u**Rational(3,2)/Rational(3,2)', '2*u**Rational(3,2)/3', 't')], 'القسمة على كسر = ضرب في مقلوبه')])
    U.example('السالب قدّام الكل', r'-\int\left(u^{4}-u^{6}\right)du', [
        (r'\int\left(u^{4}-u^{6}\right)du=\frac{u^{5}}{5}-\frac{u^{7}}{7}', [('integrate(u**4-u**6,u)', 'u**5/5-u**7/7')], 'كامل داخل القوس أولًا'),
        (r'-\left(\frac{u^{5}}{5}-\frac{u^{7}}{7}\right)=-\frac{u^{5}}{5}+\frac{u^{7}}{7}+C', [('-(u**5/5-u**7/7)', '-u**5/5+u**7/7')], 'وزّع السالب (ب3)')])
    U.add('trap', '⚠️ الفخ', ul([rich('$(1-u^2)^2\\ne1-u^4$: نسيت $-2u^2$.'),
                                rich('$u^3\\cdot u^2=u^5$ وليس $u^6$: في الضرب الأسس تنجمع.'),
                                rich('مع السالب قدّام التكامل: يدخل على <b>كل</b> الحدود.')]))
    U.add('ok', '✔ تأكد', p(rich('عوّض $u=1$ في القوس قبل الفك وبعده: لازم نفس الرقم. مثلًا $(1-1)^2=0$ و $1-2+1=0$ ✓')))
    U.task('1', 'G', 'فك القوس', 'فك القوس:', r'\left(1+u^{2}\right)^{2}', [
        (r'(a+b)^{2}=a^{2}+2ab+b^{2},\qquad a=1,\ b=u^{2}', [('(1+x)**2', '1+2*x+x**2')], 'القانون'),
        (r'(1+u^{2})^{2}=1+2u^{2}+u^{4}', [('(1+u**2)**2', '1+2*u**2+u**4')], '$b^2=(u^2)^2=u^4$')], 'لا تنسَ الحد الأوسط $2ab$.')
    U.task('2', 'P', 'وزّع', 'فك القوس ثم وزّع:', r'u^{3}\left(1+u^{2}\right)^{2}', [
        (r'(1+u^{2})^{2}=1+2u^{2}+u^{4}', [('(1+u**2)**2', '1+2*u**2+u**4')], 'فك القوس'),
        (r'u^{3}\left(1+2u^{2}+u^{4}\right)=u^{3}+2u^{5}+u^{7}', [('u**3*(1+u**2)**2', 'u**3+2*u**5+u**7')], 'وزّع، والأسس تنجمع')],
           'فك القوس أولًا، ثم اضرب $u^3$ في كل حد.')
    U.task('3', 'P', 'كامل', 'كامل حدًا حدًا:', r'\int\left(u^{4}+2u^{6}+u^{8}\right)du', [
        (r'\int u^{4}du=\frac{u^{5}}{5},\quad \int2u^{6}du=\frac{2u^{7}}{7},\quad \int u^{8}du=\frac{u^{9}}{9}',
         [('integrate(u**4,u)', 'u**5/5'), ('integrate(2*u**6,u)', '2*u**7/7'), ('integrate(u**8,u)', 'u**9/9')], 'كل حد لحاله'),
        (r'=\frac{u^{5}}{5}+\frac{2u^{7}}{7}+\frac{u^{9}}{9}+C', [('integrate(u**4+2*u**6+u**8,u)', 'u**5/5+2*u**7/7+u**9/9')], 'نجمع')],
           'كل حد: زِد الأس 1 واقسم عليه.')
    U.task('4', 'I', 'كامل', 'وزّع ثم كامل:', r'\int u^{2/3}\left(1-u^{2}\right)du', [
        (r'u^{2/3}-u^{8/3}', [('u**Rational(2,3)*(1-u**2)', 'u**Rational(2,3)-u**Rational(8,3)', 't')], 'وزّع: $\\frac23+2=\\frac83$'),
        (r'\int\left(u^{2/3}-u^{8/3}\right)du=\frac{u^{5/3}}{5/3}-\frac{u^{11/3}}{11/3}', [('diff(u**Rational(5,3)/Rational(5,3)-u**Rational(11,3)/Rational(11,3),u)', 'u**Rational(2,3)-u**Rational(8,3)', 't')],
         'زِد الأس 1'),
        (r'=\frac35u^{5/3}-\frac{3}{11}u^{11/3}+C', [('u**Rational(11,3)/Rational(11,3)', '3*u**Rational(11,3)/11', 't')], 'ضرب في المقلوب')],
           'الأسس الكسرية: $\\frac23+1=\\frac53$.')
    U.task('5', 'I', 'كامل', 'كامل (انتبه للسالب):', r'-\int\left(u^{4}-2u^{2}\right)du', [
        (r'\int\left(u^{4}-2u^{2}\right)du=\frac{u^{5}}{5}-\frac{2u^{3}}{3}', [('integrate(u**4-2*u**2,u)', 'u**5/5-2*u**3/3')], 'كامل داخل القوس'),
        (r'=-\frac{u^{5}}{5}+\frac{2u^{3}}{3}+C', [('-(u**5/5-2*u**3/3)', '-u**5/5+2*u**3/3')], 'وزّع السالب')],
           'كامل أولًا، ثم وزّع السالب على الحدين.')
    return U


def part_c3():
    U = PreUnit('P-C3', 'ج3', 'التعويض في المثلثات: u = sin أو cos أو tan أو sec', 'pre52', 'مذكرة د. طارق: درس 2.4، ودرس 5.2 ص67')
    U.why('كل أنواع الحجز في 5.2 (22 و23 و25 و26 و28) تنتهي بتعويض مثلثي. هنا تتعلمه وهو سهل (المشتقة موجودة كاملة)، '
          'وبعدها في الأنواع تتعلم كيف «تحجز» المشتقة لما تكون مخفية.', [('U-T1', 22), ('U-T2', 23), ('U-T4', 25), ('U-T5', 26), ('U-T7', 28)])
    U.explain([
        (r'الفكرة: إذا السؤال فيه دالة مثلثية <b>و</b>مشتقتها مضروبة فيها، سمّ الدالة $u$. المشتقة تصير $du$.', None, []),
        (r'مع $u=\sin x$: المشتقة $\cos x\,dx$ لازم تكون موجودة.', r'\int\sin^{4}x\cos x\,dx=\int u^{4}du=\frac{u^{5}}{5}=\frac{\sin^{5}x}{5}+C',
         [('diff(sin(x)**5/5,x)', 'sin(x)**4*cos(x)')]),
        (r'مع $u=\cos x$: $du=-\sin x\,dx$، فيطلع <b>سالب</b> قدّام التكامل.', r'\int\cos^{3}x\sin x\,dx=-\int u^{3}du=-\frac{\cos^{4}x}{4}+C',
         [('diff(-cos(x)**4/4,x)', 'cos(x)**3*sin(x)')]),
        (r'مع $u=\tan x$: المشتقة $\sec^2x\,dx$ لازم تكون موجودة.',
         r'\int\tan^{2}x\sec^{2}x\,dx=\int u^{2}du=\frac{\tan^{3}x}{3}+C',
         [('diff(tan(x)**3/3,x)', 'tan(x)**2*sec(x)**2')]),
        (r'مع $u=\sec x$: المشتقة $\sec x\tan x\,dx$، فتفصل $\sec x\tan x$ عن الباقي.',
         r'\int\sec^{3}x\tan x\,dx=\int\sec^{2}x\cdot\sec x\tan x\,dx=\frac{\sec^{3}x}{3}+C',
         [('diff(sec(x)**3/3,x)', 'sec(x)**3*tan(x)')]),
        (r'وإذا المشتقة <b>ناقصة</b> أو قوتها أكبر؟ تحجز قطعة وتحوّل الباقي بمتطابقة (ج1). هذا اللي تتعلمه في الأنواع 22–28 بعد هذا الفصل.', None, [])])
    subs = [('sin(x)', 'cos(x)', r'u=\sin x', r'du=\cos x\,dx', r'\cos x\,dx'),
            ('cos(x)', '-sin(x)', r'u=\cos x', r'du=-\sin x\,dx', r'\sin x\,dx=-du'),
            ('tan(x)', 'sec(x)**2', r'u=\tan x', r'du=\sec^{2}x\,dx', r'\sec^{2}x\,dx'),
            ('sec(x)', 'sec(x)*tan(x)', r'u=\sec x', r'du=\sec x\tan x\,dx', r'\sec x\tan x\,dx'),
            ('cot(x)', '-csc(x)**2', r'u=\cot x', r'du=-\csc^{2}x\,dx', r'\csc^{2}x\,dx=-du'),
            ('csc(x)', '-csc(x)*cot(x)', r'u=\csc x', r'du=-\csc x\cot x\,dx', r'\csc x\cot x\,dx=-du')]
    rows = [[mi(u_), mi(arith(du_, [('diff(%s,x)' % f, g)], 'P-C3 table')), mi(need)] for f, g, u_, du_, need in subs]
    U.add('short', 'جدول التعويض المثلثي', table(['إذا أخذت', 'فإن', 'لازم يكون في السؤال'], rows, 'formula compact')
          + p(rich('بعد التعويض: $\\int u^n\\,du=\\frac{u^{n+1}}{n+1}$، وارجع لـ $x$.'), 'small'))
    U.example('u = sin x', r'\int\sin^{4}x\cos x\,dx', [
        (r'u=\sin x,\qquad du=\cos x\,dx', [('diff(sin(x),x)', 'cos(x)')], 'المشتقة $\\cos x\\,dx$ موجودة كاملة'),
        (r'\int u^{4}du=\frac{u^{5}}{5}', [('integrate(u**4,u)', 'u**5/5')], 'قاعدة القوة'),
        (r'=\frac{\sin^{5}x}{5}+C', [('diff(sin(x)**5/5,x)', 'sin(x)**4*cos(x)')], 'نرجع $u$')])
    U.example('u = cos x (يطلع سالب)', r'\int\cos^{3}x\sin x\,dx', [
        (r'u=\cos x,\qquad du=-\sin x\,dx\ \Rightarrow\ \sin x\,dx=-du', [('diff(cos(x),x)', '-sin(x)')], 'مشتقة cos سالبة'),
        (r'-\int u^{3}du=-\frac{u^{4}}{4}', [('-integrate(u**3,u)', '-u**4/4')], 'السالب قدّام'),
        (r'=-\frac{\cos^{4}x}{4}+C', [('diff(-cos(x)**4/4,x)', 'cos(x)**3*sin(x)')], 'نرجع $u$')])
    U.example('u = sec x (نفصل sec tan)', r'\int\sec^{3}x\tan x\,dx', [
        (r'\sec^{3}x\tan x=\sec^{2}x\cdot\sec x\tan x', [('sec(x)**3*tan(x)', 'sec(x)**2*sec(x)*tan(x)')], 'نفصل المشتقة $\\sec x\\tan x$'),
        (r'u=\sec x,\ du=\sec x\tan x\,dx:\qquad \int u^{2}du=\frac{u^{3}}{3}', [('diff(sec(x),x)', 'sec(x)*tan(x)'), ('integrate(u**2,u)', 'u**3/3')], 'نعوّض ونكامل'),
        (r'=\frac{\sec^{3}x}{3}+C', [('diff(sec(x)**3/3,x)', 'sec(x)**3*tan(x)')], 'نرجع $u$')])
    U.add('trap', '⚠️ الفخ', ul([rich('مع $u=\\cos x$ و $u=\\cot x$ و $u=\\csc x$: سالب قدّام التكامل.'),
                                rich('لا تعوّض إذا المشتقة غير موجودة: $\\int\\sin^4x\\,dx$ ما فيه $\\cos x$، فهذا نوع ثاني (نصف الزاوية).')]))
    U.add('ok', '✔ تأكد', p(rich('اشتق جوابك: $\\left(\\frac{\\sin^5x}{5}\\right)\'=\\sin^4x\\cos x$ ✓ (سلسلة: أ2).')))
    U.drill('1', 'G-74', 'G', '$u=\\sin x$، والمشتقة $\\cos x\\,dx$ موجودة.', first=r'u=\sin x,\quad du=\cos x\,dx',
            claims=[('diff(sin(x),x)', 'cos(x)')],
            sol_rows=[('tex', r'\int u^{6}du=\frac{u^{7}}{7}', [('integrate(u**6,u)', 'u**7/7')], 'قاعدة القوة'),
                      ('line', 'sin(x)**7/7', 'نرجع $u$')])
    U.drill('2', 'G-75', 'P', '$u=\\cos x$، وانتبه للسالب.',
            sol_rows=[('sub', 'cos(x)', '-sin(x)', '$u=\\cos x$، و $\\sin x\\,dx=-du$'),
                      ('tex', r'-\int u^{5}du=-\frac{u^{6}}{6}', [('-integrate(u**5,u)', '-u**6/6')], 'السالب قدّام'),
                      ('line', '-cos(x)**6/6', 'نرجع $u$')])
    U.drill('3', 'G-76', 'P', '$u=\\tan x$، والمشتقة $\\sec^2x\\,dx$ موجودة.',
            sol_rows=[('sub', 'tan(x)', 'sec(x)**2', '$u=\\tan x$'),
                      ('tex', r'\int u^{4}du=\frac{u^{5}}{5}', [('integrate(u**4,u)', 'u**5/5')], 'قاعدة القوة'),
                      ('line', 'tan(x)**5/5', 'نرجع $u$')])
    U.drill('4', 'G-77', 'I', 'افصل $\\sec x\\tan x$، والباقي $\\sec^3x$.',
            sol_rows=[('tex', r'\sec^{4}x\tan x=\sec^{3}x\cdot\sec x\tan x', [('sec(x)**4*tan(x)', 'sec(x)**3*sec(x)*tan(x)')], 'نفصل المشتقة'),
                      ('sub', 'sec(x)', 'sec(x)*tan(x)', '$u=\\sec x$'),
                      ('line', 'sec(x)**4/4', '$\\int u^3du=\\frac{u^4}{4}$، ونرجع $u$')])
    U.drill('5', 'G-78', 'I', '$u=\\sin x$، و $\\sqrt{u}=u^{1/2}$.',
            sol_rows=[('sub', 'sin(x)', 'cos(x)', '$u=\\sin x$'),
                      ('tex', r'\int u^{1/2}du=\frac{u^{3/2}}{3/2}=\frac23u^{3/2}', [('integrate(u**Rational(1,2),u)', '2*u**Rational(3,2)/3')], 'أس كسري (ج2)'),
                      ('line', '2*sin(x)**Rational(3,2)/3', 'نرجع $u$')])
    return U


BUILDERS = {'pre42': [part_a1, part_a2, part_a3, part_a4], 'pre51': [part_b1, part_b2, part_b3],
            'pre52': [part_c1, part_c2, part_c3]}

# quick check at the start of each chapter: (question, answer latex, claims, part uid)
QUICK = {
    'pre42': [(r'اكتب $\frac{1}{x^{3}}$ كأس.', r'x^{-3}', [('1/x**3', 'x**(-3)')], 'P-A1'),
              (r'اكتب $16x^{4}$ كمربع.', r'\left(4x^{2}\right)^{2}', [('16*x**4', '(4*x**2)**2')], 'P-A1'),
              (r'اشتق $(x^{2}+1)^{3}$.', r'6x\left(x^{2}+1\right)^{2}', [('diff((x**2+1)**3,x)', '6*x*(x**2+1)**2')], 'P-A2'),
              (r'$\frac{d}{dx}\cosh x=$ ؟', r'\sinh x', [('diff(cosh(x),x)', 'sinh(x)')], 'P-A3'),
              (r'$\int\frac{2x}{x^{2}+1}dx=$ ؟', r'\ln\left(x^{2}+1\right)+C', [('diff(log(x**2+1),x)', '2*x/(x**2+1)')], 'P-A4')],
    'pre51': [(r'$\frac{d}{dx}\tan^{-1}x=$ ؟', r'\frac{1}{1+x^{2}}', [('diff(atan(x),x)', '1/(1+x**2)')], 'P-B1'),
              (r'$\frac{d}{dx}\ln|5x|=$ ؟', r'\frac{1}{x}', [('diff(log(5*x),x)', '1/x', 't')], 'P-B1'),
              (r'$\int\sin2x\,dx=$ ؟', r'-\frac{\cos2x}{2}+C', [('diff(-cos(2*x)/2,x)', 'sin(2*x)')], 'P-B2'),
              (r'$\int x^{-2}dx=$ ؟', r'-\frac1x+C', [('diff(-1/x,x)', 'x**(-2)')], 'P-B2'),
              (r'$-(a-b)=$ ؟ و $\ln e=$ ؟', r'-a+b,\qquad 1', [('-(a-b)', '-a+b'), ('log(E)', '1')], 'P-B3')],
    'pre52': [(r'$\sin^{2}x+\cos^{2}x=$ ؟ و $\tan^{2}x=$ ؟ بدلالة sec', r'1,\qquad \sec^{2}x-1', [('sin(x)**2+cos(x)**2', '1'), ('tan(x)**2', 'sec(x)**2-1')], 'P-C1'),
              (r'$\frac{d}{dx}\tan x=$ ؟', r'\sec^{2}x', [('diff(tan(x),x)', 'sec(x)**2')], 'P-C1'),
              (r'فك $(1-u^{2})^{2}$.', r'1-2u^{2}+u^{4}', [('(1-u**2)**2', '1-2*u**2+u**4')], 'P-C2'),
              (r'$\int u^{5}du=$ ؟', r'\frac{u^{6}}{6}+C', [('integrate(u**5,u)', 'u**6/6')], 'P-C2'),
              (r'إذا $u=\cos x$ فإن $du=$ ؟', r'-\sin x\,dx', [('diff(cos(x),x)', '-sin(x)')], 'P-C3')]}
INTRO = {
    'pre42': 'درس 4.2 (الدوال الزائدية العكسية) يستعمل أربعة أشياء من قبله: الأسس والجذور (عشان تكتب ما تحت الجذر كمربع)، '
             'وقواعد الاشتقاق (سؤال المشتقة)، والدوال الزائدية العادية من 4.1، والتكامل بالتعويض (كل جداول 4.2 مكتوبة بـ $u$).',
    'pre51': 'درس 5.1 (التكامل بالتجزئة) تشتق فيه $u$ وتكامل $dv$. فتحتاج مشتقات ln والدوال العكسية (3.4)، وتكاملات سريعة بإشارتها '
             'الصحيحة، وتبسيط بعد القانون.',
    'pre52': 'درس 5.2 (التكاملات المثلثية) كله: متطابقة، ثم تعويض $u$ مثلثي، ثم فك قوس وكامل حدًا حدًا. فتحتاج المتطابقات والمشتقات '
             'الست، وجبر فك الأقواس، والتعويض المثلثي في صورته السهلة.'}


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

"""كرّاسة الاختصارات — the authored content (Arabic prose + SymPy math strings).

Formulas and answers are printed from SymPy (tools/mathlib.py) and checked while the page is built
(tools/booklet_engine.py). Parameter lines such as "a = 2, b = 1" are typed, and every value they
state is checked by arith().
"""
import sympy as s

from booklet_engine import (ITEMS, ans_tex, arith, formula, functional, parts_rows, q_tex, same_antiderivative,
                            same_defint, same_derivative, same_value, sub_row, use)
from html_kit import box, chip, en, lines, link, md, mi, p, table, ul
from mathlib import rawtex, tex, texsum, x

SEM = {'S1': 'الفصل الأول', 'S2': 'الفصل الثاني'}
EXAM = {'SE': 'الاختبار الثاني', 'FE': 'النهائي'}


def source_label(it):
    if it['kind'] == 'generated':
        return 'تدريب إضافي (من إعداد هذه المذكرة، جوابه متحقق)'
    if it['kind'] == 'exam':
        y, s_, e, q = it['id'].split('-')
        return 'اختبار سابق %s، %s، %s، س%s، ص%d' % (y, SEM[s_], EXAM[e], q[1:].replace('.', ' جزء '),
                                                   it['src']['pdf_page'])
    kind = 'مثال' if it['kind'] == 'notes_example' else 'تمرين'
    return '%s المذكرة %s، ص%d' % (kind, it['src']['number'], it['src']['pdf_page'])


def prompt(it):
    if it['kind'] == 'exam':
        if it['id'] in ('1447-S2-SE-Q1.1', '1447-S2-SE-Q1.2'):
            return 'Find the derivative of the following functions :'
        return 'Find dy/dx of the following :' if it['task'] == 'diff' else 'Evaluate the following integrals :'
    return 'Find the derivatives of the following:' if it['task'] == 'diff' else 'Evaluate the following integrals:'


def question(it, where):
    use(it['id'], where)
    return '<div class="q">' + chip(source_label(it), 'src') + en(prompt(it)) + md(q_tex(it)) + '</div>'


def final(it, where):
    if it['task'] == 'diff':
        same_derivative(it['answer'], it, where)
    elif it['task'] == 'defint':
        same_defint(it['answer'], it, where)
    else:
        same_antiderivative(it['answer'], it, where)
    return md(ans_tex(it), 'ans')


def frow(lhs_rhs, cond=''):
    lhs, rhs = lhs_rhs
    return [mi(r'\displaystyle ' + lhs), mi(r'\displaystyle ' + rhs)] + ([cond] if cond is not None else [])


def card(sid, num, title, section, pages, sign, short, memo, example, trap, paper, fallback):
    head = ('<div class="card-head" id="%s"><span class="num">%d</span><h3>%s</h3>%s%s%s</div>'
            % (sid, num, title, chip(section, 'sec'), chip('المذكرة ' + pages, 'pg'), chip('متحقق', 'ok')))
    parts = [head, box('sign', 'العلامة: متى أستخدمه؟', sign), box('short', 'الاختصار', short)]
    if memo:
        parts.append(box('memo', 'كيف أتذكّره', memo))
    parts += [box('ex', 'مثال من سؤال حقيقي', example), box('trap', 'الفخ', trap),
              box('paper', 'في ورقة الكويز', paper), box('fallback', 'لو نسيت الاختصار', fallback)]
    return '<article class="card">' + ''.join(parts) + '</article>'


# ================================================================== 4.2
def sc_twins():
    """Shortcut box and memory line of card twins (shared by the booklet and the full guide)."""
    rows = [formula('asinh(u)', '1/sqrt(u**2+1)', 'diff', branches=('t', '-t'), uprime=True, label='twins sinh'),
            formula('acosh(u)', '1/sqrt(u**2-1)', 'diff', branches=('1+t',), uprime=True, label='twins cosh'),
            formula('atanh(u)', '1/(1-u**2)', 'diff', branches=('t/(1+t)', '-t/(1+t)'), uprime=True, label='twins tanh'),
            formula('acoth(u)', '1/(1-u**2)', 'diff', branches=('1+t', '-1-t'), uprime=True, label='twins coth'),
            formula('asech(u)', '-1/(u*sqrt(1-u**2))', 'diff', branches=('t/(1+t)',), uprime=True, label='twins sech'),
            formula('acsch(u)', '-1/(Abs(u)*sqrt(1+u**2))', 'diff', branches=('t', '-t'), uprime=True, label='twins csch')]
    conds = ['كل ' + mi('u'), mi('u>1'), mi('|u|<1'), mi('|u|>1'), mi('0<u<1'), mi(r'u\neq0')]
    short = table(['المشتقة', 'تساوي', 'المجال'], [frow(r, c) for r, c in zip(rows, conds)], 'formula')
    short += p(mi("u'") + ' مشتقة ما داخل الدالة (قاعدة السلسلة).', 'small')
    memo = ul(['<b>sinh و cosh</b>: جذر؛ داخل الجذر ' + mi('+1') + ' مع sinh و ' + mi('-1') + ' مع cosh.',
               '<b>tanh و coth</b>: الصيغة نفسها تمامًا؛ الفرق في المجال فقط.',
               '<b>sech و csch</b>: إشارة سالبة و ' + mi('u') + ' خارج الجذر؛ sech معها ' + mi('1-u^{2}') + ' و csch معها '
               + mi('1+u^{2}') + ' و ' + mi('|u|') + '.'])
    return short, memo


def card_twins():
    short, memo = sc_twins()
    it = ITEMS['1447-S2-SE-Q1.2']
    ex_ = question(it, 'card S1')
    ex_ += md(arith(r"u=\sqrt{x+2},\qquad u'=\frac{1}{2\sqrt{x+2}},\qquad 1+u^{2}=x+3",
                    [('diff(sqrt(x+2),x)', '1/(2*sqrt(x+2))'), ('1+(sqrt(x+2))**2', 'x+3')], 'S1 parts'))
    ex_ += p('نعوض في صف csch، ولأن ' + mi(r'\sqrt{x+2}>0') + ' فإن ' + mi('|u|=u') + ':')
    ex_ += final(it, 'card S1')
    trap = ul(['لا تنسَ الضرب في ' + mi("u'") + '.',
               'في csch⁻¹ إذا كان ' + mi('u') + ' قد يكون سالبًا فاكتب ' + mi('|u|')
               + '. أحد المفاتيح الرسمية أسقطها فصار جوابه صحيحًا لـ ' + mi('x>0') + ' فقط.',
               '<b>تنبيه coth⁻¹:</b> اشتقاق الصيغة اللوغاريتمية في المذكرة نفسها (ص57) يعطي الإشارة الموجبة كما في الجدول. '
               'المذكرة ص58 ومفتاح 1445 كتبا الإشارة سالبة، ومفتاح 1446 استخدم الموجبة. اسأل الدكتور أي صيغة يعتمد قبل الكويز.'])
    paper = p('سطر واحد: (مشتقة الدالة الخارجية عند ' + mi('u') + ') × ' + mi("u'") + '، ثم سطر تبسيط.')
    fallback = p('اكتب ' + mi(r'y=\sinh^{-1}u\iff\sinh y=u') + ' واشتق ضمنيًا كما في برهان المذكرة ص58.')
    return card('S1', 1, 'توائم المشتقات', '4.2', 'ص57–58',
                p('المطلوب مشتقة، وفي الدالة دالة زائدية عكسية مثل ' + mi(r'\sinh^{-1}') + ' أو ' + mi(r'\operatorname{sech}^{-1}') + '.'),
                short, memo, ex_, trap, paper, fallback)


def sc_six():
    """Shortcut box and memory line of card six (shared by the booklet and the full guide)."""
    rows = [formula('1/sqrt(u**2+a**2)', 'asinh(u/a)', pos=('a',), label='six sinh'),
            formula('1/sqrt(u**2-a**2)', 'acosh(u/a)', branches=('a+t',), pos=('a',), label='six cosh'),
            formula('1/(a**2-u**2)', 'atanh(u/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='six tanh'),
            formula('1/(a**2-u**2)', 'acoth(u/a)/a', branches=('a+t', '-a-t'), pos=('a',), label='six coth'),
            formula('1/(u*sqrt(a**2-u**2))', '-asech(Abs(u)/a)/a', branches=('a*t/(1+t)', '-a*t/(1+t)'), pos=('a',), label='six sech'),
            formula('1/(u*sqrt(a**2+u**2))', '-acsch(Abs(u)/a)/a', pos=('a',), label='six csch')]
    conds = ['كل ' + mi('u'), mi('u>a'), mi('|u|<a'), mi('|u|>a'), mi('0<|u|<a'), mi(r'u\neq0')]
    short = table(['التكامل', 'الجواب (+C)', 'الشرط'], [frow(r, c) for r, c in zip(rows, conds)], 'formula')
    adj = formula('c*x**(n-1)/sqrt((k*x**n)**2+a**2)', 'c*asinh(k*x**n/a)/(n*k)', var='x', branches=('t',),
                  pos=('a', 'c', 'k', 'n'), label='adjust rule (sinh row)')
    short += p('<b>قاعدة الضبط:</b> إذا كان ' + mi('u=k\\,x^{n}') + ' والبسط ' + mi('c\\,x^{n-1}') + ' فاضرب الصيغة في '
               + mi(r'\frac{c}{n\,k}') + '. مثلًا:') + md(adj[0] + ' = ' + adj[1] + ' + C')
    memo = ul(['صيغتا الجذر وحده (sinh و cosh) <b>بلا</b> ' + mi(r'\frac1a') + '؛ الأربع الباقية فيها ' + mi(r'\frac1a') + '.',
               'tanh أم coth؟ قارن ' + mi('|u|') + ' مع ' + mi('a') + ': أصغر ⇐ tanh، أكبر ⇐ coth.',
               'وجود ' + mi('u') + ' خارج الجذر ⇐ sech أو csch، والإشارة سالبة.'])
    return short, memo


def card_six():
    short, memo = sc_six()
    it = ITEMS['N42-X2-01']
    ex_ = question(it, 'card S2')
    ex_ += md(arith(r'16x^{6}=(4x^{3})^{2}:\quad u=4x^{3},\ a=3,\ c=5,\ n=3,\ k=4,\quad \frac{c}{nk}=\frac{5}{12}',
                    [('16*x**6', '(4*x**3)**2'), ('Rational(5,3*4)', 'Rational(5,12)')], 'S2 params'))
    ex_ += final(it, 'card S2')
    trap = ul(['cosh⁻¹ يصح بشرط ' + mi('u>a') + ' فقط، وهكذا تشترط المذكرة.',
               'tanh⁻¹ أم coth⁻¹ في تمرين المذكرة ' + mi(q_tex(use('N42-X2-06', 'card S2 trap'))) + ': هنا '
               + mi(r'u=5\cosh x\ge5>2') + ' فالجواب بـ coth⁻¹.',
               'المذكرة ص60 كتبت صيغة coth⁻¹ بإشارة سالبة؛ الحساب يعطي موجبة (تنبيه البطاقة 1).'])
    paper = p('سطر ' + mi('u') + ' و ' + mi('du') + '، ثم سطر الصيغة مضروبة في ' + mi(r'\frac{c}{nk}') + '.')
    fallback = p('ارجع إلى التعويض: اكتب ' + mi('u') + ' و ' + mi('du') + ' وأعد كتابة التكامل بدلالة ' + mi('u') + '.')
    return card('S2', 2, 'جدول التكاملات الستة وقاعدة الضبط', '4.2', 'ص59–60',
                p('تكامل كسر فيه جذر أو مقام من الأشكال ' + mi(r'u^{2}\pm a^{2}') + ' أو ' + mi(r'a^{2}-u^{2}')
                  + '، والبسط مشتقة ' + mi('u') + ' أو مضاعف لها.'), short, memo, ex_, trap, paper, fallback)


def sc_lamda():
    """Shortcut box and memory line of card lamda (shared by the booklet and the full guide)."""
    r = [formula('1/sqrt(b**(2*lam*x)+a**2)', '-acsch(b**(lam*x)/a)/(a*lam*log(b))', var='x', branches=('x',),
                 pos=('a', 'b', 'lam'), label='lamda exp csch'),
         formula('1/sqrt(a**2-b**(2*lam*x))', '-asech(b**(lam*x)/a)/(a*lam*log(b))', var='x', branches=('-t',),
                 pos=('a', 'b', 'lam'), label='lamda exp sech'),
         formula('1/(x*sqrt((m*x**lam)**2+a**2))', '-acsch(Abs(m*x**lam)/a)/(a*lam)', var='x', branches=('t',),
                 pos=('a', 'm', 'lam'), label='lamda power csch'),
         formula('1/(x*sqrt(a**2-(m*x**lam)**2))', '-asech(Abs(m*x**lam)/a)/(a*lam)', var='x',
                 branches=('(a/m)**(1/lam)*t/(1+t)',), pos=('a', 'm', 'lam'), label='lamda power sech')]
    short = table(['الشكل', 'الجواب (+C)'], [frow(z, None) for z in r], 'formula')
    short += p(mi(r'\lambda') + ' (لامدا): اكتب ما تحت الجذر كمربع، مثل ' + mi(r'e^{6x}=\left(e^{3x}\right)^{2}') + ' ⇐ '
               + mi(r'\lambda=3') + '، و ' + mi(r'x^{3}=\left(x^{3/2}\right)^{2}') + ' ⇐ ' + mi(r'\lambda=\frac32')
               + '. ومع الأساس ' + mi('e') + ' يكون ' + mi(r'\ln e=1') + '.')
    memo = ul(['المقام دائمًا ' + mi(r'a\times\lambda') + '، ومعه ' + mi(r'\ln b') + ' إذا لم يكن الأساس ' + mi('e') + '.',
               'الإشارة سالبة دائمًا. داخل الجذر ' + mi('+') + ' ⇐ csch⁻¹، وداخل الجذر ' + mi('-') + ' ⇐ sech⁻¹.'])
    return short, memo


def card_lamda():
    short, memo = sc_lamda()
    it = ITEMS['1446-S2-SE-Q2.7']
    ex_ = question(it, 'card S3')
    ex_ += md(arith(r'e^{6x}=(e^{3x})^{2}:\quad b=e,\ \lambda=3,\ a=1', [('exp(6*x)', 'exp(3*x)**2')], 'S3 params'))
    ex_ += final(it, 'card S3')
    it2 = ITEMS['1447-S1-SE-Q2.2']
    use(it2['id'], 'card S3 variation')
    same_antiderivative(it2['answer'], it2, 'card S3 variation')
    ex_ += p('تنويعة (' + source_label(it2) + '): الأساس 5 فيظهر ' + mi(r'\ln5') + ' في المقام.')
    ex_ += md(q_tex(it2) + ' ' + ans_tex(it2))
    trap = ul(['إذا ظهرت مشتقة الداخل في البسط، مثل ' + mi(r'\frac{e^{x}}{\sqrt{e^{2x}+1}}') + '، فهذه البطاقة 2 مباشرة لا لامدا.',
               'في شكل القوة اكتب ' + mi('|m x^{\\lambda}|') + ' إذا كان ' + mi('x') + ' قد يكون سالبًا (أحد المفاتيح أسقطها).'])
    same_value('1/sqrt(exp(6*x)+1)', 'exp(3*x)/(exp(3*x)*sqrt(exp(3*x)**2+1))', 'S3 paper line')
    paper = md(r'\int\frac{dx}{\sqrt{e^{6x}+1}}=\int\frac{e^{3x}\,dx}{e^{3x}\sqrt{(e^{3x})^{2}+1}}')
    paper += p('هذا السطر (الضرب في ' + mi('e^{3x}') + ' بسطًا ومقامًا) يُظهر للمصحح أصل الصيغة، ثم الجواب.', 'small')
    fallback = p('اضرب البسط والمقام في الأسية (أو ' + mi('x^{\\lambda}') + ') ثم استخدم صف csch أو sech في البطاقة 2.')
    return card('S3', 3, 'لامدا', '4.2', 'ص61',
                p('أسية أو قوة تحت الجذر، مثل ' + mi(r'\frac{1}{\sqrt{e^{6x}+1}}') + ' أو ' + mi(r'\frac{1}{x\sqrt{x^{6}+25}}')
                  + '، ولا تظهر مشتقة الداخل.'), short, memo, ex_, trap, paper, fallback)


def sc_square():
    """Shortcut box and memory line of card square (shared by the booklet and the full guide)."""
    r = [formula('c/sqrt(A*(x-h)**2+d)', 'c*asinh(sqrt(A)*(x-h)/sqrt(d))/sqrt(A)', var='x', branches=('h+t', 'h-t'),
                 pos=('A', 'c', 'd'), real=('h',), label='square sinh'),
         formula('c/sqrt(A*(x-h)**2-d)', 'c*acosh(sqrt(A)*(x-h)/sqrt(d))/sqrt(A)', var='x', branches=('h+sqrt(d/A)+t',),
                 pos=('A', 'c', 'd'), real=('h',), label='square cosh (d stands for -d)'),
         formula('c/((x-h)*sqrt(A*(x-h)**2+d))', '-c*acsch(sqrt(A)*Abs(x-h)/sqrt(d))/sqrt(d)', var='x',
                 branches=('h+t', 'h-t'), pos=('A', 'c', 'd'), real=('h',), label='square csch'),
         formula('c/((x-h)*sqrt(d-A*(x-h)**2))', '-c*asech(sqrt(A)*Abs(x-h)/sqrt(d))/sqrt(d)', var='x',
                 branches=('h+sqrt(d/A)*t/(1+t)', 'h-sqrt(d/A)*t/(1+t)'), pos=('A', 'c', 'd'), real=('h',), label='square sech')]
    short = p('<b>خطوتان:</b> المركز ' + mi(r'h=-\frac{B}{2A}') + '، ثم ' + mi('d') + ' = قيمة الثلاثي عند ' + mi('x=h')
              + '. فيصير ما تحت الجذر ' + mi(r'A(x-h)^{2}+d') + '.')
    labels = ['معامل ' + mi('x^2') + ' موجب، ' + mi('d>0'),
              'معامل ' + mi('x^2') + ' موجب، والباقي سالب (اكتبه ' + mi('-d') + ')، بشرط ' + mi(r'x-h>\sqrt{d/A}'),
              'عامل ' + mi('(x-h)') + ' خارج الجذر، معامل ' + mi('x^2') + ' موجب، ' + mi('d>0'),
              'عامل ' + mi('(x-h)') + ' خارج الجذر، معامل ' + mi('x^2') + ' سالب، ' + mi('d>0')]
    short += table(['الشكل', 'الجواب (+C)', 'متى'], [frow(z, l) for z, l in zip(r, labels)], 'formula')
    short += p('للمقارنة فقط (درس 3.4): معامل ' + mi('x^2') + ' سالب ولا عامل خارج الجذر ⇐ ' + mi(r'\sin^{-1}') + '.', 'small')
    memo = ul([mi('d') + ' هو قيمة الثلاثي عند المركز؛ لا تحفظ له قانونًا.',
               'العامل الخطي خارج الجذر ⇐ المعامل ' + mi(r'-\frac{c}{\sqrt d}') + ' دائمًا.',
               'معامل ' + mi('x^2') + ': موجب ⇐ sinh أو cosh أو csch؛ سالب ⇐ sech.'])
    return short, memo


def card_square():
    short, memo = sc_square()
    it = ITEMS['1446-S1-SE-Q2.2']
    ex_ = question(it, 'card S4')
    ex_ += md(arith(r'A=1,\quad h=-\frac{6}{2}=-3,\quad Q(-3)=9-18-16=-25 \\ x^{2}+6x-16=(x+3)^{2}-5^{2}',
                    [('-Rational(6,2)', '-3'), ('9-18-16', '-25'), ('x**2+6*x-16', '(x+3)**2-5**2')], 'S4 a'))
    ex_ += final(it, 'card S4') + p('بشرط ' + mi('x+3>5') + ' كما تشترط المذكرة (الجهة الأخرى لا تغطيها هذه الصيغة).', 'small')
    it2 = ITEMS['1447-S2-FE-Q2.6']
    ex_ += question(it2, 'card S4 b')
    ex_ += md(arith(r'h=-3,\quad d=Q(-3)=9-18+13=4,\quad \sqrt d=2,\quad (x-h)=(x+3)\ \checkmark',
                    [('9-18+13', '4'), ('x**2+6*x+13', '(x+3)**2+4')], 'S4 b'))
    ex_ += final(it2, 'card S4 b') + p('المفتاح الرسمي كتبه بلا قيمة مطلقة، فصار صحيحًا لـ ' + mi('x>-3') + ' فقط.', 'small')
    trap = ul(['العامل الخطي يجب أن يكون ' + mi('(x-h)') + ' نفسه، وإلا لا تنطبق صفوف csch و sech.',
               'معامل أمام ' + mi('x^2') + ' مثل ' + mi(arith(r'\sqrt{9x^{2}+36x+45}=3\sqrt{x^{2}+4x+5}',
                                                  [('sqrt(9*x**2+36*x+45)', '3*sqrt(x**2+4*x+5)')], 'S4 trap'))
               + ': أخرج 9 من الجذر أولًا (يخرج 3) ثم طبّق الجدول.'])
    paper = p('سطر إكمال المربع (مثل ' + mi(r'x^{2}+6x-16=(x+3)^{2}-5^{2}') + ') ثم سطر الصيغة.')
    fallback = p('أكمل المربع بالطريقة العادية (أضف واطرح مربع نصف معامل ' + mi('x') + ') ثم البطاقة 2 مع ' + mi('u=x-h') + '.')
    return card('S4', 4, 'جدول إكمال المربع', '4.2', 'ص61، تمارين 13–16',
                p('تحت الجذر ثلاثي فيه حد ' + mi('x') + ' مثل ' + mi(r'x^{2}+6x+13') + '، وقد يوجد عامل ' + mi('(x-h)') + ' خارج الجذر.'),
                short, memo, ex_, trap, paper, fallback)


# ================================================================== 5.1
def di_table(rows):
    return table(['الإشارة', 'D: اشتق', 'I: كامل'], [[mi(sg), mi(tex(d)), mi(tex(i))] for sg, d, i in rows], 'di')


def sc_folded():
    """Shortcut box and memory line of card folded (shared by the booklet and the full guide)."""
    G1, G2, g = s.Function('G_1')(x), s.Function('G_2')(x), s.Function('g')(x)
    pp, qq = s.symbols('p q', real=True)
    functional(lambda: (s.diff((pp * x + qq) * G1 - pp * G2, x) - (pp * x + qq) * g)
               .subs({s.Derivative(G1, x): g, s.Derivative(G2, x): G1}), 'linear folded rule')
    short = p('<b>أ) الخطي:</b>') + md(r'\int(px+q)\,g\,dx=(px+q)\,G_{1}-p\,G_{2}+C')
    short += p(mi('G_1') + ' تكامل ' + mi('g') + '، و ' + mi('G_2') + ' تكامل ' + mi('G_1') + '.', 'small')
    short += p('<b>ب) جدول DI:</b> عمود D: اشتق كثيرة الحدود حتى الصفر. عمود I: كامل الدالة الأخرى. اضرب قطريًا بالإشارات ' + mi('+\\ -\\ +\\ -\\ \\cdots') + '.')
    memo = ul(['كثيرة الحدود تنزل للصفر، والدالة الأخرى تُكامل.',
               'مع ' + mi('kx') + ' تقسم على ' + mi('k') + ' في كل خطوة تكامل.'])
    return short, memo


def card_folded():
    short, memo = sc_folded()
    it = ITEMS['1446-S1-SE-Q2.4']
    ex_ = question(it, 'card S5 a')
    ex_ += md(arith(r'p=3,\quad G_{1}=\cosh x,\quad G_{2}=\sinh x',
                    [('integrate(sinh(x),x)', 'cosh(x)'), ('integrate(cosh(x),x)', 'sinh(x)')], 'S5a'))
    ex_ += final(it, 'card S5 a')
    it2 = ITEMS['1445-S1-FE-Q2.2']
    ex_ += question(it2, 'card S5 b')
    ex_ += di_table([('+', 'x**2', 'cosh(x)'), ('-', '2*x', 'sinh(x)'), ('+', '2', 'cosh(x)'), (r'\cdot', '0', 'sinh(x)')])
    ex_ += final(it2, 'card S5 b')
    trap = ul(['مع sin: ' + mi(r'\int\sin kx\,dx=-\frac{1}{k}\cos kx') + '؛ هذه الإشارة تجتمع مع إشارة الجدول.',
               'يتوقف الجدول عندما يصل عمود D إلى صفر؛ لا تضرب صف الصفر.'])
    paper = p('اكتب الجدول نفسه ثم سطر الجواب؛ الجدول تنظيم للتجزئة المتكررة.')
    fallback = md(parts_rows('x**2', 'cosh(x)', '2*x', 'sinh(x)', 'S5 fallback')) + p('ثم كرّر التجزئة على التكامل الباقي.')
    return card('S5', 5, 'الجدول المطوي', '5.1', 'ص63–64',
                p('كثيرة حدود × (' + mi(r'e^{kx}') + ' أو ' + mi(r'\sin kx') + ' أو ' + mi(r'\cos kx') + ' أو '
                  + mi(r'\sinh kx') + ' أو ' + mi(r'\cosh kx') + ').'), short, memo, ex_, trap, paper, fallback)


def sc_qaws():
    """Shortcut box and memory line of card qaws (shared by the booklet and the full guide)."""
    f = formula('x**n*log(a*x)', 'x**(n+1)/(n+1)*(log(a*x)-1/(n+1))', var='x', branches=('t',), pos=('a',), real=('n',),
                label='qaws (symbolic real n)')
    short = md(f[0] + ' = ' + f[1] + ' + C') + p('لكل ' + mi(r'n\neq-1') + '، والصيغة نفسها مع ' + mi(r'\ln|ax|') + ' عندما ' + mi('x<0') + '.', 'small')
    memo = p('قاعدة القوة على ' + mi('x^{n}') + '، ثم قوس: ' + mi(r'\ln') + ' ناقص واحد على نفس المقام.')
    return short, memo


def card_qaws():
    short, memo = sc_qaws()
    it = ITEMS['1446-S1-SE-Q2.5']
    ex_ = question(it, 'card S6')
    ex_ += md(arith(r'n=-2,\quad n+1=-1:\quad \frac{x^{-1}}{-1}\left(\ln x-\frac{1}{-1}\right)=-\frac{\ln x+1}{x}',
                    [('x**(-1)/(-1)*(log(x)-1/(-1))', '-(log(x)+1)/x')], 'S6'))
    ex_ += final(it, 'card S6')
    it2 = ITEMS['N51-X05']
    use(it2['id'], 'card S6 variation')
    same_antiderivative(it2['answer'], it2, 'card S6 variation')
    ex_ += p('تنويعة: ' + mi(r'\ln|x|') + ' وحدها هي ' + mi('n=0') + ' (' + source_label(it2) + '):') + md(q_tex(it2) + ' ' + ans_tex(it2))
    trap = ul([mi('n=-1') + '، أي ' + mi(r'\int\frac{\ln|x|}{x}dx') + '، ليست تجزئة: عوّض ' + mi(r'u=\ln|x|') + ' فالجواب '
               + mi(r'\frac{(\ln|x|)^{2}}{2}') + '.',
               'مع ' + mi(r'\ln|2x|') + ' المشتقة ' + mi(r'\frac1x') + ' (الـ 2 تختفي)، والقاعدة كما هي.'])
    paper = md(parts_rows('log(x)', 'x**(-2)', '1/x', '-1/x', 'S6 paper', branch='t')) + p('ثم سطر القوس والجواب.')
    fallback = p('التجزئة: ' + mi(r'u=\ln|ax|') + ' و ' + mi(r'dv=x^{n}dx') + '.')
    return card('S6', 6, 'القوس', '5.1', 'ص64، تمارين 5–7',
                p(mi('x^{n}') + ' مضروبة في ' + mi(r'\ln|ax|') + '، أو ' + mi(r'\ln|x|') + ' وحدها.'), short, memo, ex_, trap, paper, fallback)


def sc_rafeeq(sheet=False):
    """Shortcut box and memory line of card rafeeq (shared by the booklet and the full guide);
    sheet=True leaves out the optional results table (formula sheet)."""
    gf = s.Function('g')(x)
    functional(lambda: s.diff(x * gf - s.Integral(x * s.diff(gf, x), x), x) - gf, 'rafeeq identity')
    short = md(r'\int f^{-1}(x)\,dx=x\,f^{-1}(x)-\int x\,\big(f^{-1}\big)'"'"r'(x)\,dx')
    short += md(r'\int x\,f^{-1}(x)\,dx=\frac{x^{2}}{2}f^{-1}(x)-\frac12\int x^{2}\big(f^{-1}\big)'"'"r'(x)\,dx')
    m1 = formula('x/sqrt(c+x**2)', 'sqrt(c+x**2)', var='x', branches=('t', '-t'), pos=('c',), label='micro +')
    m2 = formula('x/sqrt(c-x**2)', '-sqrt(c-x**2)', var='x', branches=('sqrt(c)*t/(1+t)',), pos=('c',), label='micro -')
    m3 = formula('x/(c+x**2)', 'log(c+x**2)/2', var='x', branches=('t',), pos=('c',), label='micro ln +')
    m4 = formula('x/(c-x**2)', '-log(Abs(c-x**2))/2', var='x', branches=('sqrt(c)*t/(1+t)', 'sqrt(c)+t'), pos=('c',), label='micro ln -')
    short += p('التكامل الباقي يُحسم غالبًا بأحد هذه السطور:') + table(['التكامل', 'الجواب (+C)'], [frow(z, None) for z in (m1, m2, m3, m4)], 'formula compact')
    rows = [formula('asin(x)', 'x*asin(x)+sqrt(1-x**2)', var='x', branches=('t/(1+t)', '-t/(1+t)'), label='r asin'),
            formula('atan(x)', 'x*atan(x)-log(1+x**2)/2', var='x', branches=('x',), label='r atan'),
            formula('asec(x)', 'x*asec(x)-acosh(x)', var='x', branches=('1+t',), label='r asec'),
            formula('acosh(x)', 'x*acosh(x)-sqrt(x**2-1)', var='x', branches=('1+t',), label='r acosh'),
            formula('atanh(x)', 'x*atanh(x)+log(1-x**2)/2', var='x', branches=('t/(1+t)', '-t/(1+t)'), label='r atanh')]
    if not sheet:
        short += p('نتائج للتحقق السريع (لا يلزم حفظها):', 'small') + table(['التكامل', 'الجواب (+C)'], [frow(z, None) for z in rows], 'formula compact')
    memo = p('الرفيق دائمًا ' + mi('x') + ': نضرب ' + mi('x') + ' في الدالة، ثم نطرح تكامل ' + mi('x') + ' في مشتقتها.')
    return short, memo


def card_rafeeq():
    short, memo = sc_rafeeq()
    it = ITEMS['1445-S1-SE-Q2.5']
    ex_ = question(it, 'card S7')
    ex_ += md(r'= x\cosh^{-1}x-\int\frac{x}{\sqrt{x^{2}-1}}\,dx')
    ex_ += final(it, 'card S7')
    it2 = ITEMS['1446-S2-FE-Q2.2']
    ex_ += question(it2, 'card S7 b')
    ex_ += md(arith(r'= \frac{x^{2}}{2}\tanh^{-1}x-\frac12\int\frac{x^{2}}{1-x^{2}}\,dx,\qquad \frac{x^{2}}{1-x^{2}}=-1+\frac{1}{1-x^{2}}',
                    [('x**2/(1-x**2)', '-1+1/(1-x**2)')], 'S7 division'))
    ex_ += final(it2, 'card S7 b')
    trap = ul(['مع ' + mi(r'x\,f^{-1}') + ' قد تحتاج قسمة مثل ' + mi(r'\frac{x^{2}}{1-x^{2}}=-1+\frac{1}{1-x^{2}}') + '.',
               'sec⁻¹: يبقى ' + mi(r'\int\frac{dx}{\sqrt{x^{2}-1}}=\cosh^{-1}x') + ' (ربط مع 4.2).'])
    paper = md(parts_rows('acosh(x)', '1', '1/sqrt(x**2-1)', 'x', 'S7 paper', branch='1+t')) + p('ثم السطر الأول في المثال والجواب.')
    fallback = p('التجزئة: ' + mi(r'u=f^{-1}(x)') + ' و ' + mi('dv=dx') + ' (أو ' + mi('dv=x\\,dx') + ').')
    return card('S7', 7, 'الرفيق', '5.1', 'ص64–65، تمارين 8–10',
                p('دالة عكسية وحدها (مثل ' + mi(r'\tan^{-1}x') + ' أو ' + mi(r'\cosh^{-1}x') + ') أو مضروبة في ' + mi('x') + '.'),
                short, memo, ex_, trap, paper, fallback)


def sc_dawaran():
    """Shortcut box and memory line of card dawaran (shared by the booklet and the full guide)."""
    f1 = formula('exp(a*x)*sin(b*x)', 'exp(a*x)*(a*sin(b*x)-b*cos(b*x))/(a**2+b**2)', var='x', branches=('x',), pos=('a', 'b'), label='dawaran sin')
    f2 = formula('exp(a*x)*cos(b*x)', 'exp(a*x)*(a*cos(b*x)+b*sin(b*x))/(a**2+b**2)', var='x', branches=('x',), pos=('a', 'b'), label='dawaran cos')
    short = md(f1[0] + ' = ' + f1[1] + ' + C') + md(f2[0] + ' = ' + f2[1] + ' + C')
    short += p('فُحصت أيضًا مع ' + mi('a') + ' سالب (مثل ' + mi('e^{-x}') + ').', 'small')
    memo = p('المقام ' + mi('a^{2}+b^{2}') + '. البسط: ' + mi('a') + ' × نفس الدالة، ثم ' + mi('b') + ' × الأخرى؛ مع sin الإشارة ' + mi('-') + '، ومع cos ' + mi('+') + '.')
    return short, memo


def card_dawaran():
    short, memo = sc_dawaran()
    it = ITEMS['1447-S2-FE-Q2.3']
    ex_ = question(it, 'card S8')
    ex_ += md(arith(r'a=2,\quad b=1,\quad a^{2}+b^{2}=5', [('2**2+1**2', '5')], 'S8'))
    ex_ += final(it, 'card S8')
    ex_ += p('المفتاح الرسمي كتبه بالصورة ' + mi(texsum(it['official'])) + '، وهي الجواب نفسه.', 'small')
    same_value(it['official'], it['answer'], 'S8 official equals')
    trap = ul(['إذا حللت بالتجزئة: توقّف عندما يعود التكامل الأصلي، وانقله للطرف الآخر ثم اقسم (مثال المذكرة ص65).',
               'لا تخلط مع ' + mi(r'e^{ax}\sinh bx') + ': هذا البطاقة 9.'])
    paper = p('إذا احتجت خطوات: تجزئتان ثم سطر المعادلة؛ وإلا سطر الصيغة بالأرقام ثم الجواب.')
    fallback = md(parts_rows('sin(x)', 'exp(2*x)', 'cos(x)', 'exp(2*x)/2', 'S8 fallback')) + p('كرّر التجزئة مرة ثانية ثم حل المعادلة.')
    return card('S8', 8, 'الدوران', '5.1', 'ص65، تمارين 11–12',
                p(mi('e^{ax}') + ' مضروبة في ' + mi(r'\sin bx') + ' أو ' + mi(r'\cos bx') + '.'), short, memo, ex_, trap, paper, fallback)


def sc_nisfayn():
    """Shortcut box and memory line of card nisfayn (shared by the booklet and the full guide)."""
    f1 = formula('exp(a*x)*cosh(b*x)', '(exp((a+b)*x)/(a+b)+exp((a-b)*x)/(a-b))/2', var='x', branches=('x',), real=('a', 'b'), label='nisfayn cosh')
    f2 = formula('exp(a*x)*sinh(b*x)', '(exp((a+b)*x)/(a+b)-exp((a-b)*x)/(a-b))/2', var='x', branches=('x',), real=('a', 'b'), label='nisfayn sinh')
    short = md(f1[0] + ' = ' + f1[1] + ' + C') + md(f2[0] + ' = ' + f2[1] + ' + C')
    short += p('بشرط ' + mi(r'a\neq\pm b') + '.', 'small')
    memo = p('نصفان: نصف بأس مجموع ' + mi('(a+b)') + '، ونصف بأس فرق ' + mi('(a-b)') + '. مع sinh يصير بينهما ' + mi('-') + '.')
    return short, memo


def card_nisfayn():
    short, memo = sc_nisfayn()
    it = ITEMS['1446-S1-SE-Q2.3']
    ex_ = question(it, 'card S9')
    ex_ += md(arith(r'a=1,\ b=2:\quad \frac12\left[\frac{e^{3x}}{3}+\frac{e^{-x}}{-1}\right]',
                    [('(exp(3*x)/3+exp(-x)/(-1))/2', 'exp(3*x)/6-exp(-x)/2')], 'S9'))
    ex_ += final(it, 'card S9')
    it2 = ITEMS['1445-S1-SE-Q2.1']
    trap = p('إذا كان ' + mi('a=b') + ' أو ' + mi('a=-b') + ' يصير أحد الأسين صفرًا: حدّه ' + mi(r'\frac12') + ' وتكامله '
             + mi(r'\frac{x}{2}') + '.') + question(it2, 'card S9 trap') + final(it2, 'card S9 trap')
    same_value('exp(-x)*cosh(x)', '(1+exp(-2*x))/2', 'S9 trap line')
    paper = md(r'e^{-x}\cosh x=e^{-x}\cdot\frac{e^{x}+e^{-x}}{2}=\frac{1+e^{-2x}}{2}') + p('ثم تكامل كل حد، وهكذا حلّ المفتاح الرسمي.')
    fallback = p('اكتب cosh أو sinh بالتعريف الأسّي (درس 4.1)، ثم وزّع وكامل.')
    return card('S9', 9, 'النصفين', '5.1', 'تمارين 13–14 ص66',
                p(mi('e^{ax}') + ' مضروبة في ' + mi(r'\sinh bx') + ' أو ' + mi(r'\cosh bx') + '.'), short, memo, ex_, trap, paper, fallback)


def sc_small():
    """Shortcut box and memory line of card small (shared by the booklet and the full guide)."""
    rows = [formula('log(Abs(x))', 'x*log(Abs(x))-x', var='x', label='small ln'),
            formula('log(Abs(x))**2', 'x*log(Abs(x))**2-2*x*log(Abs(x))+2*x', var='x', label='small ln2'),
            formula('exp(sqrt(x))', '2*exp(sqrt(x))*(sqrt(x)-1)', var='x', branches=('t',), label='small e sqrt'),
            formula('log(x**2+a**2)', 'x*log(x**2+a**2)-2*x+2*a*atan(x/a)', var='x', branches=('x',), pos=('a',), label='small ln quad'),
            formula('x**3*sqrt(x**2+c)', '(x**2+c)**Rational(5,2)/5-c*(x**2+c)**Rational(3,2)/3', var='x', branches=('t',), real=('c',), label='small root')]
    notes = ['تمرين (5)', 'تمرين (16)', 'تمرين (15)', 'مثال 4', 'تمرين (17)']
    short = table(['التكامل', 'الجواب (+C)', 'في المذكرة ص64–66'], [frow(z, n) for z, n in zip(rows, notes)], 'formula')
    memo = p('خمس حالات قصيرة: يكفي أن تتعرف شكلها وتعرف أن لها جوابًا جاهزًا.')
    return short, memo


def card_small():
    short, memo = sc_small()
    it = ITEMS['N51-X17']
    ex_ = question(it, 'card S10') + md(arith(r'c=-1', [], 'S10')) + final(it, 'card S10')
    trap = ul([mi(r'e^{\sqrt x}') + ': ابدأ بـ ' + mi(r't=\sqrt x,\ x=t^{2},\ dx=2t\,dt') + ' ثم الجدول المطوي.',
               mi(r'x^{3}\sqrt{x^{2}+c}') + ': الأسهل ' + mi(r'w=x^{2}+c') + '، أي ' + mi(r'x^{2}=w-c') + '.'])
    paper = md(sub_row('x**2-1', '2*x', 'S10 paper', var='w')) + p('ثم ' + mi(r'\frac12\int(w+1)\sqrt{w}\,dw') + ' والجواب.')
    fallback = p('ln أو ' + mi(r'(\ln)^{2}') + ': تجزئة مع ' + mi('dv=dx') + '. الجذر: عوّض ' + mi('w') + ' = ما تحت الجذر.')
    return card('S10', 10, 'اختصارات صغيرة', '5.1', 'ص64، تمارين 5 و15–18', p('أحد الأشكال الخمسة في الجدول.'),
                short, memo, ex_, trap, paper, fallback)


# ================================================================== 5.2
def sc_pascal():
    """Shortcut box and memory line of card pascal (shared by the booklet and the full guide)."""
    routes = [[mi(r'\cos^{2k+1}x'), mi(r'u=\sin x'), '+', 'أس sin', mi(r'(1-u^{2})^{k}')],
              [mi(r'\sin^{2k+1}x'), mi(r'u=\cos x'), '−', 'أس cos', mi(r'(1-u^{2})^{k}')],
              [mi(r'\sec^{2k+2}x'), mi(r'u=\tan x'), '+', 'أس tan', mi(r'(1+u^{2})^{k}')],
              [mi(r'\tan^{2k+1}x') + ' ومعه sec', mi(r'u=\sec x'), '+', 'أس sec ناقص 1', mi(r'(u^{2}-1)^{k}')],
              [mi(r'\csc^{2k+2}x'), mi(r'u=\cot x'), '−', 'أس cot', mi(r'(1+u^{2})^{k}')],
              [mi(r'\cot^{2k+1}x') + ' ومعه csc', mi(r'u=\csc x'), '−', 'أس csc ناقص 1', mi(r'(u^{2}-1)^{k}')]]
    short = table(['إذا وجدت', 'خذ', 'إشارة أمام الكل', 'أس البداية p', 'القوس'], routes, 'formula')
    short += ul(['معاملات القوس من صف باسكال رقم ' + mi('k') + ': ' + mi(r'1\ \big|\ 1\ 1\ \big|\ 1\ 2\ 1\ \big|\ 1\ 3\ 3\ 1') + '.',
                 'الإشارات: ' + mi(r'(1+u^{2})') + ' كلها ' + mi('+') + '، و ' + mi(r'(1-u^{2})') + ' و ' + mi(r'(u^{2}-1)')
                 + ' تتناوب، والحد الأعلى أسًّا في ' + mi(r'(u^{2}-1)') + ' موجب.',
                 'الأسس في الجواب تبدأ من ' + mi('p+1') + ' وتزيد 2، وكل حد يُقسم على أسه.'])
    memo = p('احجز قطعة المشتقة، والباقي قوس من صف باسكال، ثم ارفع كل أس واحدًا واقسم عليه.')
    return short, memo


def card_pascal():
    short, memo = sc_pascal()
    it = ITEMS['1446-S1-SE-Q2.6']
    ex_ = question(it, 'card S11')
    ex_ += md(arith(r'\cos^{5}x=\cos^{2\cdot2+1}x:\ k=2,\ u=\sin x,\ p=4;\quad (1-u^{2})^{2}=1-2u^{2}+u^{4}',
                    [('sin(x)**4*cos(x)**5', 'sin(x)**4*(1-sin(x)**2)**2*cos(x)'), ('(1-u**2)**2', '1-2*u**2+u**4')], 'S11'))
    ex_ += final(it, 'card S11')
    it2 = ITEMS['1447-S2-SE-Q3.3']
    ex_ += question(it2, 'card S11 b')
    ex_ += md(arith(r'\tan^{3}x=\tan^{2\cdot1+1}x:\ k=1,\ u=\sec x,\ p=3-1=2;\quad u^{2}(u^{2}-1)=u^{4}-u^{2}',
                    [('sec(x)**3*tan(x)**3', 'sec(x)**2*(sec(x)**2-1)*sec(x)*tan(x)'), ('u**2*(u**2-1)', 'u**4-u**2')], 'S11b'))
    ex_ += final(it2, 'card S11 b')
    trap = ul(['sin و cos زوجيان معًا ⇐ لا يصلح؛ نصف الزاوية (البطاقة 12).',
               'tan زوجي و sec فردي ⇐ حوّل ' + mi(r'\tan^{2}x=\sec^{2}x-1') + ' ثم سلسلة sec (البطاقة 13).',
               'إذا كان الأسان فرديين معًا فاحجز من الأصغر (حدود أقل).',
               'الأس الكسري للدالة الأخرى لا يضر: ' + mi(q_tex(use('N52-X04', 'card S11 trap'))) + ' بالقاعدة نفسها.'])
    paper = md(r'\sin^{4}x\cos^{5}x=\sin^{4}x\,(1-\sin^{2}x)^{2}\cos x,\qquad ' + sub_row('sin(x)', 'cos(x)', 'S11 paper'))
    paper += p('ثم سطر التوزيع وسطر الجواب.')
    fallback = p('القاعدة العامة في المذكرة ص68 و71 و73: احجز عامل المشتقة واستخدم ' + mi(r'\sin^{2}x+\cos^{2}x=1')
                 + ' أو ' + mi(r'\sec^{2}x=1+\tan^{2}x') + '.')
    return card('S11', 11, 'صف باسكال', '5.2', 'ص67–74',
                p('حاصل ضرب قوتين لزوج: sin/cos أو tan/sec أو cot/csc، ويوجد أس فردي مناسب أو sec/csc زوجي.'),
                short, memo, ex_, trap, paper, fallback)


def sc_even():
    """Shortcut box and memory line of card even (shared by the booklet and the full guide)."""
    f1 = formula('sin(k*x)**2', 'x/2-sin(2*k*x)/(4*k)', var='x', branches=('x',), pos=('k',), label='even sin2')
    f2 = formula('cos(k*x)**2', 'x/2+sin(2*k*x)/(4*k)', var='x', branches=('x',), pos=('k',), label='even cos2')
    f3 = formula('sin(x)**2*cos(x)**2', 'x/8-sin(4*x)/32', var='x', branches=('x',), label='even sin2cos2')
    short = table(['التكامل', 'الجواب (+C)'], [frow(z, None) for z in (f1, f2, f3)], 'formula')
    memo = p('نصف ' + mi('x') + '، ثم ' + mi(r'\sin') + ' ضعف الزاوية على ' + mi('4k') + ': ناقص مع sin، زائد مع cos.')
    return short, memo


def card_even():
    short, memo = sc_even()
    it = ITEMS['N52-X13']
    ex_ = question(it, 'card S12') + final(it, 'card S12')
    it2 = ITEMS['N52-E1-3']
    ex_ += p('أس أعلى: طبّق ' + mi(r'\cos^{2}\theta=\frac{1+\cos2\theta}{2}') + ' مرتين (مثال المذكرة):')
    ex_ += question(it2, 'card S12 b') + final(it2, 'card S12 b')
    trap = p(mi(r'\int\sin^{2}x\,dx\neq\frac{\sin^{3}x}{3}') + ' لأن مشتقة ' + mi(r'\sin x') + ' غير موجودة بجانبه.')
    paper = md(r'\sin^{2}x=\frac{1-\cos2x}{2}') + p('ثم كامل حدًا حدًا.')
    fallback = p('متطابقتا المذكرة ص67: ' + mi(r'\sin^{2}x=\frac{1-\cos2x}{2}') + ' و ' + mi(r'\cos^{2}x=\frac{1+\cos2x}{2}') + '.')
    return card('S12', 12, 'الزوجيات', '5.2', 'ص67–70', p('أس زوجي لـ sin أو cos، أو كلاهما زوجي.'),
                short, memo, ex_, trap, paper, fallback)


def sc_reduce():
    """Shortcut box and memory line of card reduce (shared by the booklet and the full guide)."""
    n_ = s.Symbol('n', positive=True)
    functional(lambda: s.simplify((s.diff(s.sec(x) ** (n_ - 2) * s.tan(x) / (n_ - 1), x)
                                   + (n_ - 2) / (n_ - 1) * s.sec(x) ** (n_ - 2) - s.sec(x) ** n_).rewrite(s.cos)), 'sec reduction (symbolic n)')
    m_ = s.Symbol('m', positive=True)
    T, Ct = s.Symbol('T', positive=True), s.Symbol('Ct', positive=True)
    # d/dx tan^(m-1) = (m-1) tan^(m-2) sec^2 with sec^2 = 1 + tan^2 (written with T = tan x)
    functional(lambda: s.simplify(s.expand((m_ - 1) * T ** (m_ - 2) * (1 + T ** 2) / (m_ - 1) - T ** (m_ - 2) - T ** m_)),
               'tan reduction (symbolic m)')
    functional(lambda: s.simplify(s.expand(s.diff(s.tan(x), x) - (1 + s.tan(x) ** 2))), 'tan derivative identity')
    functional(lambda: s.simplify(s.expand(-(m_ - 1) * Ct ** (m_ - 2) * (-(1 + Ct ** 2)) / (m_ - 1) - Ct ** (m_ - 2) - Ct ** m_)),
               'cot reduction (symbolic m)')
    functional(lambda: s.simplify(s.expand(s.diff(s.cot(x), x) + (1 + s.cot(x) ** 2))), 'cot derivative identity')
    short = md(r'\int\tan^{m}x\,dx=\frac{\tan^{m-1}x}{m-1}-\int\tan^{m-2}x\,dx')
    short += md(r'\int\cot^{m}x\,dx=-\frac{\cot^{m-1}x}{m-1}-\int\cot^{m-2}x\,dx')
    short += md(r'\int\sec^{n}x\,dx=\frac{\sec^{n-2}x\,\tan x}{n-1}+\frac{n-2}{n-1}\int\sec^{n-2}x\,dx')
    b1 = formula('sec(x)', 'log(Abs(sec(x)+tan(x)))', var='x', branches=('t/(1+t)',), label='sec base')
    b2 = formula('tan(x)', 'log(Abs(sec(x)))', var='x', branches=('t/(1+t)',), label='tan base')
    short += table(['التكامل', 'الجواب (+C)'], [frow(z, None) for z in (b1, b2)], 'formula compact')
    memo = p('tan: الأسس تنزل 2 كل مرة (' + mi(r'm-1,\ m-3,\ \ldots') + ') بإشارات متناوبة، والنهاية ' + mi(r'\pm x') + ' إذا كان الأس زوجيًا، أو '
             + mi(r'\pm\ln\left|\sec x\right|') + ' إذا كان فرديًا.')
    return short, memo


def card_reduce():
    short, memo = sc_reduce()
    it = ITEMS['N52-E3-2']
    ex_ = question(it, 'card S13') + final(it, 'card S13')
    it2 = ITEMS['N52-E3-1']
    ex_ += question(it2, 'card S13 b') + final(it2, 'card S13 b')
    trap = p('tan زوجي مع sec فردي: حوّل ' + mi(r'\tan^{2}x=\sec^{2}x-1') + ' فتصير قوى sec، ثم هذه السلسلة (الحالة 5 في المذكرة ص71).')
    same_value('tan(x)**4', 'tan(x)**2*(sec(x)**2-1)', 'S13 paper')
    paper = md(r'\int\tan^{4}x\,dx=\int\tan^{2}x\,(\sec^{2}x-1)\,dx=\frac{\tan^{3}x}{3}-\int\tan^{2}x\,dx')
    fallback = p('اكتب ' + mi(r'\tan^{m}x=\tan^{m-2}x\,(\sec^{2}x-1)') + ' ووزّع، كما في المذكرة ص70–71.')
    return card('S13', 13, 'سلسلة التخفيض', '5.2', 'ص70–73', p('قوة tan أو cot وحدها، أو قوة فردية لـ sec أو csc وحدها.'),
                short, memo, ex_, trap, paper, fallback)


def sc_prod():
    """Shortcut box and memory line of card prod (shared by the booklet and the full guide)."""
    r = [formula('sin(m*x)*cos(n*x)', '-(cos((m-n)*x)/(m-n)+cos((m+n)*x)/(m+n))/2', var='x', branches=('x',), real=('m', 'n'), label='prod sc'),
         formula('sin(m*x)*sin(n*x)', '(sin((m-n)*x)/(m-n)-sin((m+n)*x)/(m+n))/2', var='x', branches=('x',), real=('m', 'n'), label='prod ss'),
         formula('cos(m*x)*cos(n*x)', '(sin((m-n)*x)/(m-n)+sin((m+n)*x)/(m+n))/2', var='x', branches=('x',), real=('m', 'n'), label='prod cc')]
    short = ''.join(md(z[0] + ' = ' + z[1] + ' + C') for z in r) + p('بشرط ' + mi(r'm\neq\pm n') + '.', 'small')
    memo = p('الضرب يصير جمعًا: زاويتان ' + mi('(m-n)') + ' و ' + mi('(m+n)') + '، وكل حد يقسم على زاويته.')
    return short, memo


def card_prod():
    short, memo = sc_prod()
    it = ITEMS['N52-E5-1']
    ex_ = question(it, 'card S14')
    ex_ += md(arith(r'm=7,\ n=5:\quad -\frac12\left[\frac{\cos2x}{2}+\frac{\cos12x}{12}\right]',
                    [('-(cos(2*x)/2+cos(12*x)/12)/2', '-cos(2*x)/4-cos(12*x)/24')], 'S14'))
    ex_ += final(it, 'card S14')
    trap = p('إذا كان ' + mi('m-n') + ' سالبًا: ' + mi(r'\cos(-\theta)=\cos\theta') + ' لكن ' + mi(r'\sin(-\theta)=-\sin\theta') + '؛ انتبه للإشارة.')
    same_value('sin(7*x)*cos(5*x)', '(sin(2*x)+sin(12*x))/2', 'S14 paper')
    paper = md(r'\sin7x\cos5x=\frac12\left[\sin2x+\sin12x\right]') + p('ثم كامل كل حد، كما في المذكرة ص74.')
    fallback = p('متطابقات المذكرة ص74 ثم التكامل المباشر.')
    return card('S14', 14, 'الضرب بزاويتين', '5.2', 'ص74–75',
                p(mi(r'\sin mx\cos nx') + ' أو ' + mi(r'\sin mx\sin nx') + ' أو ' + mi(r'\cos mx\cos nx') + ' بزاويتين مختلفتين.'),
                short, memo, ex_, trap, paper, fallback)


CARDS = [card_twins, card_six, card_lamda, card_square, card_folded, card_qaws, card_rafeeq, card_dawaran,
         card_nisfayn, card_small, card_pascal, card_even, card_reduce, card_prod]
NAMES = ['توائم المشتقات', 'جدول التكاملات الستة وقاعدة الضبط', 'لامدا', 'جدول إكمال المربع', 'الجدول المطوي',
         'القوس', 'الرفيق', 'الدوران', 'النصفين', 'اختصارات صغيرة', 'صف باسكال', 'الزوجيات', 'سلسلة التخفيض',
         'الضرب بزاويتين']
SIGNS = ['مشتقة فيها دالة زائدية عكسية',
         'كسر بجذر أو مقام من الشكل ' + mi(r'u^{2}\pm a^{2}') + '، والبسط مشتقة ' + mi('u'),
         'أسية أو قوة تحت الجذر، ولا مشتقة ظاهرة', 'ثلاثي فيه حد ' + mi('x') + ' تحت الجذر',
         'كثيرة حدود × ' + mi('e^{kx}') + ' أو sin/cos أو sinh/cosh',
         'قوة × ln', 'دالة عكسية وحدها أو × ' + mi('x'), mi('e^{ax}') + ' × sin أو cos', mi('e^{ax}') + ' × sinh أو cosh',
         mi(r'\ln|x|') + '، ' + mi(r'(\ln|x|)^{2}') + '، ' + mi(r'e^{\sqrt{x}}') + '، ' + mi(r'\ln(x^{2}+a^{2})') + '، '
         + mi(r'x^{3}\sqrt{x^{2}+c}'),
         'قوتان لزوج مثلثي وأس فردي مناسب', 'أس زوجي لـ sin/cos',
         'tan أو cot وحدها؛ sec فردي وحده', 'sin/cos بزاويتين مختلفتين']


# ================================================================== drills
CHOOSE = ['1446-S2-SE-Q2.3', 'N42-X2-11', 'N51-X06', 'N52-X01', 'N51-X12', '1447-S1-FE-Q2.1', 'N52-X11',
          'N51-X09', 'N42-X2-03', 'N51-X14', 'N52-X16', '1446-S2-FE-Q1.3', 'N42-X2-09', 'N52-X14']
CHOOSE_ANS = {'1446-S2-SE-Q2.3': (5, r'خطي: $p=2$'), 'N42-X2-11': (3, r'$\lambda=2,\ a=5,\ m=2$ (صف csch)'),
              'N51-X06': (6, r'$n=5$'), 'N52-X01': (11, r'sin فردي: $u=\cos x,\ k=1,\ p=4$'), 'N51-X12': (8, r'$a=5,\ b=2$'),
              '1447-S1-FE-Q2.1': (4, r'$h=2$، والقيمة عند المركز $-4$'), 'N52-X11': (14, r'sin·sin مع $m=2,\ n=6$'),
              'N51-X09': (7, r'الدالة $\sec^{-1}x$'), 'N42-X2-03': (2, r'$u=3x^{4},\ a=6$؛ $\tanh^{-1}$ أو $\coth^{-1}$ حسب $|u|$'),
              'N51-X14': (9, r'$a=1,\ b=5$'), 'N52-X16': (13, r'$\tan^{6}x$'), '1446-S2-FE-Q1.3': (1, r'$\sinh^{-1}$ مع $u=\frac{2}{\sqrt{x}}$'),
              'N42-X2-09': (0, r'لا اختصار: تعويض مباشر $u=\cosh^{-1}x$'), 'N52-X14': (12, r'$\cos^{2}x$')}
GUIDED = ['N51-X01', 'N51-X07', '1445-S2-SE-Q2.7', '1447-S1-SE-Q2.3']
PARTIAL = ['1445-S1-FE-Q1.3', 'N42-X2-10', 'N51-X11', 'N52-X09']
INDEP = ['1445-S2-SE-Q1.1', 'N42-X2-15', '1447-S1-SE-Q2.7', 'N51-X03', '1445-S1-SE-Q2.2', 'N52-X10', 'N51-X04']

# id: (card, hint, first-step latex, arithmetic claims for that line, middle expressions checked against the answer)
SOL = {
    'N51-X01': (5, 'كثيرة حدود من الدرجة الأولى × cosh: القاعدة الخطية في البطاقة 5.',
                r'p=2,\quad G_{1}=\sinh x,\quad G_{2}=\cosh x', [('integrate(cosh(x),x)', 'sinh(x)')], []),
    'N51-X07': (6, r'قوة × $\ln|x|$ بأس سالب: القوس مع $n=-4$.',
                r'n=-4,\quad n+1=-3:\quad\frac{x^{-3}}{-3}\left(\ln|x|-\frac{1}{-3}\right)',
                [('-4+1', '-3')], []),
    '1445-S2-SE-Q2.7': (4, r'ثلاثي فيه حد $x$ تحت الجذر ولا عامل خارجه: جدول إكمال المربع.',
                        r'h=-3,\quad Q(-3)=9-18+13=4,\quad x^{2}+6x+13=(x+3)^{2}+2^{2}',
                        [('9-18+13', '4'), ('x**2+6*x+13', '(x+3)**2+2**2')], []),
    '1447-S1-SE-Q2.3': (11, r'cos أسه فردي (5): صف باسكال مع $u=\sin x$.',
                        r'\cos^{5}x=\cos^{2\cdot2+1}x:\quad k=2,\ u=\sin x,\ p=2',
                        [('sin(x)**2*cos(x)**5', 'sin(x)**2*(1-sin(x)**2)**2*cos(x)')], []),
    '1445-S1-FE-Q1.3': (1, r'مشتقة $\sinh^{-1}$ لدالة أسية، ثم مشتقة $\ln|\tanh 4x|$.', r"u=3^{x},\quad u'=3^{x}\ln3",
                        [('diff(3**x,x)', '3**x*log(3)')], []),
    'N42-X2-10': (3, 'أسية تحت الجذر بإشارة سالبة ولا مشتقة ظاهرة: لامدا (صف sech).',
                  r'9-e^{6x}=3^{2}-(e^{3x})^{2}:\quad a=3,\ \lambda=3,\ b=e,\ c=2',
                  [('9-exp(6*x)', '3**2-exp(3*x)**2')], ['2*(-asech(exp(3*x)/3)/(3*3))']),
    'N51-X11': (8, r'$e^{2x}\sin 3x$: الدوران.', r'a=2,\quad b=3,\quad a^{2}+b^{2}=13', [('2**2+3**2', '13')],
                ['exp(2*x)*(2*sin(3*x)-3*cos(3*x))/13']),
    'N52-X09': (11, r'cot أسه فردي ومعه csc: صف باسكال مع $u=\csc x$.',
                r'\cot^{5}x=\cot^{2\cdot2+1}x:\quad k=2,\ u=\csc x,\ p=3-1=2',
                [('cot(x)**5*csc(x)**3', '(csc(x)**2-1)**2*csc(x)**2*csc(x)*cot(x)')],
                ['-(csc(x)**7/7-2*csc(x)**5/5+csc(x)**3/3)']),
    '1445-S2-SE-Q1.1': (1, r'tanh (من 4.1) و $\operatorname{sech}^{-1}$: توائم المشتقات.', r"u=3x,\quad u'=3", [], []),
    'N42-X2-15': (4, 'ثلاثي تحت الجذر وعامل خطي خارجه: صف csch في جدول إكمال المربع.',
                  r'h=-3,\quad Q(-3)=9-18+25=16,\quad\sqrt d=4,\quad c=2',
                  [('9-18+25', '16'), ('x**2+6*x+25', '(x+3)**2+16')], []),
    '1447-S1-SE-Q2.7': (6, r'قوة × $\ln|2x|$: القوس مع $n=3$.', r'n=3:\quad\frac{x^{4}}{4}\left(\ln|2x|-\frac14\right)', [],
                        ['x**4*(log(Abs(2*x))-Rational(1,4))/4']),
    'N51-X03': (5, r'كثيرة حدود من الدرجة 3 × $e^{x}$: جدول DI.', r'D:\ x^{3},\ 3x^{2},\ 6x,\ 6,\ 0\qquad I:\ e^{x},\ e^{x},\ e^{x},\ \dots',
                [], []),
    '1445-S1-SE-Q2.2': (2, r'اكتب $\sqrt{x}\sqrt{1+x}=\sqrt{x}\sqrt{1+(\sqrt{x})^{2}}$: بطاقة الستة مع $u=\sqrt{x}$.',
                        r'\frac{1}{\sqrt x\sqrt{1+x}}=2\cdot\frac{\frac{1}{2\sqrt x}}{\sqrt{1+(\sqrt x)^{2}}}:\quad u=\sqrt x,\ a=1',
                        [('1/(sqrt(x)*sqrt(1+x))', '2*(1/(2*sqrt(x)))/sqrt(1+sqrt(x)**2)'), ('diff(sqrt(x),x)', '1/(2*sqrt(x))')], []),
    'N52-X10': (14, r'sin × cos بزاويتين: الضرب بزاويتين مع $m=3$ و $n=5$.',
                r'm=3,\ n=5:\quad -\frac12\left[\frac{\cos(-2x)}{-2}+\frac{\cos8x}{8}\right]', [],
                ['-(cos(-2*x)/(-2)+cos(8*x)/8)/2']),
    'N51-X04': (5, r'كثيرة حدود خطية × $\sec^{2}x$: القاعدة الخطية مع $G_{1}=\tan x$.',
                r'p=1,\quad G_{1}=\tan x,\quad G_{2}=\int\tan x\,dx=-\ln\left|\cos x\right|',
                [('integrate(sec(x)**2,x)', 'tan(x)')], ['(x+1)*tan(x)-(-log(Abs(cos(x))))']),
}


def rich(text):
    """Arabic text with $...$ math segments; each segment becomes an isolated LTR math island."""
    parts = text.split('$')
    return ''.join(mi(seg) if i % 2 else seg for i, seg in enumerate(parts))


def tagged_drills():
    return ([('G%d' % i, k, 'موجّه') for i, k in enumerate(GUIDED, 1)]
            + [('P%d' % i, k, 'ناقص الخطوات') for i, k in enumerate(PARTIAL, 1)]
            + [('I%d' % i, k, 'مستقل') for i, k in enumerate(INDEP, 1)])


def drill_block(tag, item_id, level):
    it = ITEMS[item_id]
    use(item_id, 'drill ' + tag)
    head = '<div class="drill-head" id="d-%s"><b>%s</b> %s %s</div>' % (tag, tag, chip(level, 'lvl'), link('h-' + tag, 'مساعدة', 'help'))
    body = chip(source_label(it), 'src') + en(prompt(it)) + md(q_tex(it))
    card_no, hint, first, claims, _ = SOL[item_id]
    if level == 'موجّه':
        body += p('البطاقة ' + str(card_no) + '. بداية الحل جاهزة؛ أكمل:') + md(arith(first, claims, 'first ' + tag)) + lines(3, 'write tight')
    elif level == 'ناقص الخطوات':
        body += p('اكتب سطر المعاملات ثم الجواب:') + lines(3, 'write tight')
    else:
        body += lines(5, 'write tight')
    return '<div class="drill">' + head + body + '</div>'


def help_sections():
    """Three separate ladders so a hint never shows the solution next to it."""
    hints, firsts, fulls = [], [], []
    for tag, k, level in tagged_drills():
        it = ITEMS[k]
        card_no, hint, first, claims, mids = SOL[k]
        first_tex = arith(first, claims, 'first ' + tag)
        hints.append('<div class="hrow" id="h-%s"><b>%s</b> %s %s %s %s</div>' % (
            tag, tag, rich(hint), link('S%d' % card_no, 'البطاقة %d' % card_no, 'card'), link('f-' + tag, 'الخطوة الأولى', 'next'),
            link('d-' + tag, 'العودة للتمرين', 'back')))
        firsts.append('<div class="hrow" id="f-%s"><b>%s</b>%s %s %s</div>' % (
            tag, tag, md(first_tex), link('s-' + tag, 'الحل الكامل', 'next'), link('d-' + tag, 'العودة للتمرين', 'back')))
        body = md(q_tex(it)) + md(first_tex)
        for m_ in mids:
            if it['task'] == 'diff':
                same_derivative([m_], it, 'solution ' + tag)
            else:
                same_antiderivative([m_], it, 'solution ' + tag)
            if rawtex(m_) != texsum(it['answer']):     # a middle line identical to the answer adds nothing
                body += md('= ' + rawtex(m_) + ('' if it['task'] == 'diff' else ' + C'))
        if k == 'N51-X03':
            body += di_table([('+', 'x**3', 'exp(x)'), ('-', '3*x**2', 'exp(x)'), ('+', '6*x', 'exp(x)'), ('-', '6', 'exp(x)'),
                              (r'\cdot', '0', 'exp(x)')])
        body += final(it, 'solution ' + tag)
        fulls.append('<div class="sol" id="s-%s"><div class="drill-head"><b>%s</b> %s</div>%s</div>' % (
            tag, tag, link('d-' + tag, 'العودة للتمرين', 'back'), body))
    return hints, firsts, fulls


def choose_answers():
    rows = []
    for i, k in enumerate(CHOOSE, 1):
        n, key = CHOOSE_ANS[k]
        rows.append(['C%d' % i, (link('S%d' % n, NAMES[n - 1], 'card') if n else 'لا يوجد اختصار'), rich(key)])
    return table(['التمرين', 'الاختصار', 'المفتاح'], rows, 'answers')

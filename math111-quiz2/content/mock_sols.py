"""Mock exams: which held-out question goes where, and the worked solution of each (every row is checked).

The ten questions are real past-exam or notes questions that were held out before the guide was written
(data/holdout_ids.json). Each one is one part of an original question; a mock counts five such parts.
"""
MOCKS = {'A': ['1447-S1-SE-Q1.1', '1445-S2-FE-Q2.1', '1447-S1-FE-Q2.2', '1446-S2-SE-Q2.5', 'MU-94-3'],
         'B': ['1446-S1-SE-Q1.1', '1445-S1-SE-Q2.7', '1447-S2-SE-Q3.1', 'MU-101-3', 'N52-X12']}

# where to study each question again in the guide (type number and title)
TYPES = {1: 'مشتقة الدالة الزائدية العكسية', 4: 'tanh⁻¹ أم coth⁻¹؟', 10: 'إكمال المربع', 13: 'كثيرة حدود درجة 2 أو 3: جدول DI',
         18: 'x × دالة عكسية', 20: 'أسية × sinh أو cosh (اكتبها بالأسس)', 23: 'sin و cos معًا وأحدهما فردي',
         26: 'tan و sec: الـ tan فردي', 29: 'ضرب sin و cos بزاويتين مختلفتين'}
TYPE_OF = {'1447-S1-SE-Q1.1': [1], '1445-S2-FE-Q2.1': [10], '1447-S1-FE-Q2.2': [13], '1446-S2-SE-Q2.5': [20], 'MU-94-3': [23],
           '1446-S1-SE-Q1.1': [1], '1445-S1-SE-Q2.7': [4], '1447-S2-SE-Q3.1': [18], 'MU-101-3': [26], 'N52-X12': [29]}

MINUTES = {'diff': 8, 'int': 11}   # rough working time per question, before the student has tried it

SOLS = {
    '1447-S1-SE-Q1.1': [
        ('tex', r"\frac{d}{dx}\sinh\left(\sqrt{x^{2}+1}\right)=\cosh\left(\sqrt{x^{2}+1}\right)\cdot\frac{2x}{2\sqrt{x^{2}+1}}",
         [('diff(sinh(sqrt(x**2+1)),x)', 'cosh(sqrt(x**2+1))*2*x/(2*sqrt(x**2+1))')], 'من 4.1: sinh يصير cosh، × مشتقة الجذر'),
        ('tex', r"u=e^{x},\ u'=e^{x}:\quad \frac{d}{dx}\cosh^{-1}e^{x}=\frac{u'}{\sqrt{u^{2}-1}}=\frac{e^{x}}{\sqrt{e^{2x}-1}}",
         [('diff(acosh(exp(x)),x)', 'exp(x)/sqrt(exp(2*x)-1)', 't')], 'قانون مشتقة $\\cosh^{-1}u$: $\\frac{u\'}{\\sqrt{u^2-1}}$، و $u=e^x$'),
        ('line', 'x*cosh(sqrt(x**2+1))/sqrt(x**2+1)+exp(x)/sqrt(exp(2*x)-1)', 'نختصر 2، ونجمع الحدين')],
    '1445-S2-FE-Q2.1': [
        ('tex', r'\sqrt{4x^{2}+8x+20}=2\sqrt{x^{2}+2x+5}', [('sqrt(4*x**2+8*x+20)', '2*sqrt(x**2+2*x+5)')], 'نخرج 4 من الجذر'),
        ('tex', r'x^{2}+2x+5=(x+1)^{2}+2^{2}', [('x**2+2*x+5', '(x+1)**2+2**2')], 'نكمّل المربع: المركز $-1$، والباقي $1-2+5=4=2^2$'),
        ('tex', r'\int\frac{2\,dx}{2\sqrt{(x+1)^{2}+2^{2}}}=\int\frac{du}{\sqrt{u^{2}+2^{2}}},\quad u=x+1',
         [('2/sqrt(4*x**2+8*x+20)', '1/sqrt((x+1)**2+2**2)')], 'الـ 2 تختصر'),
        ('line', 'asinh((x+1)/2)', 'مربع زائد رقم: قانون $\\sinh^{-1}\\frac ua$ مع $a=2$، ونرجع $u=x+1$')],
    '1447-S1-FE-Q2.2': [
        ('tex', r'D:\ x^{2},\ 2x,\ 2,\ 0\qquad I:\ \cos3x,\ \tfrac13\sin3x,\ -\tfrac19\cos3x,\ -\tfrac{1}{27}\sin3x',
         [('integrate(cos(3*x),x)', 'sin(3*x)/3'), ('integrate(sin(3*x)/3,x)', '-cos(3*x)/9'), ('integrate(-cos(3*x)/9,x)', '-sin(3*x)/27')],
         'جدول DI: كل تكامل يقسم على 3'),
        ('tex', r'=x^{2}\cdot\frac{\sin3x}{3}-2x\cdot\left(-\frac{\cos3x}{9}\right)+2\cdot\left(-\frac{\sin3x}{27}\right)',
         [('x**2*sin(3*x)/3-2*x*(-cos(3*x)/9)+2*(-sin(3*x)/27)', 'x**2*sin(3*x)/3+2*x*cos(3*x)/9-2*sin(3*x)/27')], 'قطريًا بإشارات $+\\ -\\ +$'),
        ('line', 'x**2*sin(3*x)/3+2*x*cos(3*x)/9-2*sin(3*x)/27', 'نبسّط الإشارات')],
    '1446-S2-SE-Q2.5': [
        ('tex', r'\sinh3x=\frac{e^{3x}-e^{-3x}}{2}\ \Rightarrow\ e^{x/2}\sinh3x=\frac{e^{7x/2}-e^{-5x/2}}{2}',
         [('exp(x/2)*sinh(3*x)', '(exp(7*x/2)-exp(-5*x/2))/2')], 'التعريف، ونجمع الأسس: $\\frac12+3=\\frac72$ و $\\frac12-3=-\\frac52$'),
        ('line', 'exp(7*x/2)/7+exp(-5*x/2)/5', '$\\int e^{kx}dx=\\frac{e^{kx}}{k}$: $\\frac12\\cdot\\frac27=\\frac17$ و $\\frac12\\cdot\\frac{2}{5}=\\frac15$')],
    'MU-94-3': [
        ('tex', r'\cos^{7}x\sin^{6}x=\sin^{6}x\,(1-\sin^{2}x)^{3}\cos x', [('cos(x)**7*sin(x)**6', 'sin(x)**6*(1-sin(x)**2)**3*cos(x)')],
         'cos فردي: نحجز $\\cos x$، والباقي $\\cos^6x=(1-\\sin^2x)^3$'),
        ('sub', 'sin(x)', 'cos(x)', '$u=\\sin x$'),
        ('tex', r'=\int u^{6}(1-3u^{2}+3u^{4}-u^{6})\,du=\int\left(u^{6}-3u^{8}+3u^{10}-u^{12}\right)du',
         [('u**6*(1-u**2)**3', 'u**6-3*u**8+3*u**10-u**12')], 'نفك $(1-u^2)^3$ (مكعب القوس) ونوزّع'),
        ('line', 'sin(x)**7/7-sin(x)**9/3+3*sin(x)**11/11-sin(x)**13/13', 'نكامل ونرجع $u$')],
    '1446-S1-SE-Q1.1': [
        ('tex', r"\frac{d}{dx}\operatorname{csch}\frac2x=-\operatorname{csch}\frac2x\coth\frac2x\cdot\left(-\frac{2}{x^{2}}\right)",
         [('diff(csch(2/x),x)', '-csch(2/x)*coth(2/x)*(-2/x**2)')], 'من 4.1، × مشتقة $\\frac2x$'),
        ('tex', r"\frac{d}{dx}\tanh^{-1}e^{5x}=\frac{5e^{5x}}{1-e^{10x}}", [('diff(atanh(exp(5*x)),x)', '5*exp(5*x)/(1-exp(10*x))')],
         'قانون مشتقة $\\tanh^{-1}u$: $\\frac{u\'}{1-u^2}$، و $u=e^{5x}$ ومشتقتها $5e^{5x}$'),
        ('line', '2*csch(2/x)*coth(2/x)/x**2+5*exp(5*x)/(1-exp(10*x))', 'سالب في سالب = موجب، ونجمع')],
    '1445-S1-SE-Q2.7': [
        ('sub', 'cos(x)', '-sin(x)', '$u=\\cos x$، و $\\sin x\\,dx=-du$'),
        ('tex', r'=-\int\frac{du}{2^{2}-u^{2}}', [('sin(x)/(4-cos(x)**2)', '-diff(cos(x),x)/(2**2-cos(x)**2)')], 'التكامل بدلالة $u$'),
        ('line', '-atanh(cos(x)/2)/2', '$|u|=|\\cos x|\\le1$ أصغر من $a=2$، يعني قانون $\\tanh^{-1}$ مع $\\frac1a=\\frac12$')],
    '1447-S2-SE-Q3.1': [
        ('parts', 'asech(x)', 'x', '-1/(x*sqrt(1-x**2))', 'x**2/2', '$u$ الدالة العكسية، و $dv=x\\,dx$', 't/(1+t)'),
        ('line', 'x**2*asech(x)/2+Integral(x/(2*sqrt(1-x**2)),x)', 'القانون؛ $v\\,du=-\\frac{x}{2\\sqrt{1-x^2}}$ وسالب في سالب'),
        ('line', 'x**2*asech(x)/2-sqrt(1-x**2)/2', '$\\int\\frac{x}{\\sqrt{1-x^2}}dx=-\\sqrt{1-x^2}$')],
    'MU-101-3': [
        ('tex', r'\tan^{5}x\sec x=(\sec^{2}x-1)^{2}\sec x\tan x', [('tan(x)**5*sec(x)', '(sec(x)**2-1)**2*sec(x)*tan(x)')],
         'tan فردي: نحجز $\\sec x\\tan x$، والباقي $\\tan^4x=(\\sec^2x-1)^2$'),
        ('sub', 'sec(x)', 'sec(x)*tan(x)', '$u=\\sec x$'),
        ('tex', r'=\int(u^{2}-1)^{2}\,du=\int\left(u^{4}-2u^{2}+1\right)du', [('(u**2-1)**2', 'u**4-2*u**2+1')], 'نفك القوس'),
        ('line', 'sec(x)**5/5-2*sec(x)**3/3+sec(x)', 'نكامل ونرجع $u$')],
    'N52-X12': [
        ('tex', r'\cos4x\cos7x=\frac12\left[\cos(-3x)+\cos11x\right]=\frac12\left[\cos3x+\cos11x\right]',
         [('cos(4*x)*cos(7*x)', '(cos(3*x)+cos(11*x))/2')], 'متطابقة الضرب، و $\\cos(-\\theta)=\\cos\\theta$'),
        ('line', 'sin(3*x)/6+sin(11*x)/22', 'كل sin يُقسم على زاويته، × $\\frac12$')],
}

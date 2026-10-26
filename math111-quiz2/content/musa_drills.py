"""Exercises from Dr. Musa Ajjal's 1448/1449 notes, to take the place of the ✏️ exercises written for this guide.

MUSA_DRILLS = {case uid: [exercise, ...]}; each exercise has the item id (data/extra_mu.json), the hint, the first
written line with its checks (used when the slot is a guided one) and the solution rows (guide_kit.step_cells kinds).
Every row is checked when the guide is built.
"""
MUSA_DRILLS = {
    'U-T8': [
        dict(item='MU2-102-1', hint='زاويتين مختلفتين، و sin·sin: الوحيدة اللي فيها ناقص.',
             first=r'\sin5x\sin3x=\frac12\left[\cos2x-\cos8x\right]',
             claims=[('sin(5*x)*sin(3*x)', '(cos(2*x)-cos(8*x))/2')],
             sol_rows=[('tex', r'\sin5x\sin3x=\frac12\left[\cos(5x-3x)-\cos(5x+3x)\right]=\frac12\left[\cos2x-\cos8x\right]',
                        [('sin(5*x)*sin(3*x)', '(cos(2*x)-cos(8*x))/2')],
                        'sin·sin = نص (cos الفرق 🔴 ناقص cos المجموع). الفرق $2x$ والمجموع $8x$.'),
                       ('line', 'sin(2*x)/4-sin(8*x)/16', 'كل cos يصير sin مقسوم على زاويته: $\\frac12\\cdot\\frac12=\\frac14$ و $\\frac12\\cdot\\frac18=\\frac1{16}$.')]),
        dict(item='MU2-102-2', hint='sin·cos: نص (sin المجموع + sin الفرق).',
             first=r'\sin4x\cos3x=\frac12\left[\sin7x+\sin x\right]',
             claims=[('sin(4*x)*cos(3*x)', '(sin(7*x)+sin(x))/2')],
             sol_rows=[('tex', r'\sin4x\cos3x=\frac12\left[\sin(4x+3x)+\sin(4x-3x)\right]=\frac12\left[\sin7x+\sin x\right]',
                        [('sin(4*x)*cos(3*x)', '(sin(7*x)+sin(x))/2')],
                        'sin·cos = نص (sin المجموع + sin الفرق). الفرق موجب لأن $4>3$.'),
                       ('line', '-cos(7*x)/14-cos(x)/2', 'تكامل sin فيه 🔴 سالب، ونقسم على الزاوية: $\\frac12\\cdot\\frac17=\\frac1{14}$.')])],
    'U-I3': [
        dict(item='MU2-115-1', hint='$x$ برّا الجذر، وتحت الجذر زائد: csch⁻¹. الداخل $5x$ والرقم 4.',
             first=r'\cU{u=5x},\quad \cD{du=5\,dx},\quad 25x^{2}+16=u^{2}+4^{2}',
             claims=[('diff(5*x,x)', '5'), ('25*x**2+16', '(5*x)**2+4**2')],
             sol_rows=[('sub', '5*x', '5', 'تحت الجذر $25x^2=(5x)^2$، فالداخل 🔵 $u=5x$.'),
                       ('tex', r'\frac{dx}{x}=\frac{du/5}{u/5}=\frac{du}{u}', [('(1/5)/(x/5)', '1/x')],
                        'الـ 5 فوق والـ 5 تحت يختصرون، فما فيه 🟠 رقم تعديل.'),
                       ('tex', r'I=\int\frac{du}{u\sqrt{u^{2}+4^{2}}}=-\frac14\operatorname{csch}^{-1}\frac{|u|}{4}',
                        [('diff(-acsch(Abs(x)/4)/4,x)', '1/(x*sqrt(x**2+16))', 't'), ('diff(-acsch(Abs(x)/4)/4,x)', '1/(x*sqrt(x**2+16))', '-t')],
                        '$u$ برّا الجذر وتحت الجذر زائد: قانون csch⁻¹، فيه 🔴 سالب و $\\frac1a=\\frac14$.'),
                       ('line', '-acsch(5*Abs(x)/4)/4', 'نرجّع $u=5x$، ونخلي $|5x|$ لأن $x$ ممكن يكون سالب.')])],
    'U-I6': [
        dict(item='MU2-121-1', hint='البسط فيه جمع: اكتب $2x-1=(2x-6)+5$. الأول مشتقة المقام، والثاني رقم.',
             first=r'\frac{2x-1}{x^{2}-6x+13}=\frac{2x-6}{x^{2}-6x+13}+\frac{5}{x^{2}-6x+13}',
             claims=[('(2*x-1)/(x**2-6*x+13)', '(2*x-6)/(x**2-6*x+13)+5/(x**2-6*x+13)')],
             sol_rows=[('tex', r'\frac{2x-1}{x^{2}-6x+13}=\frac{2x-6}{x^{2}-6x+13}+\frac{5}{x^{2}-6x+13}',
                        [('(2*x-1)/(x**2-6*x+13)', '(2*x-6)/(x**2-6*x+13)+5/(x**2-6*x+13)')],
                        'مشتقة المقام $2x-6$، فنكتب البسط $(2x-6)+5$ ونفصل.'),
                       ('tex', r'\int\frac{2x-6}{x^{2}-6x+13}\,dx=\ln\left(x^{2}-6x+13\right)',
                        [('diff(log(x**2-6*x+13),x)', '(2*x-6)/(x**2-6*x+13)')],
                        'الكسر الأول: البسط مشتقة المقام، فالجواب ln المقام (موجب دايم، ما نحتاج $|\\,|$).'),
                       ('tex', r'x^{2}-6x+13=(x-3)^{2}+2^{2}', [('x**2-6*x+13', '(x-3)**2+2**2')],
                        'الكسر الثاني: نكمّل المربع. المركز 3، والباقي $9-18+13=4=2^2$.'),
                       ('tex', r'\int\frac{5\,dx}{(x-3)^{2}+2^{2}}=\frac52\tan^{-1}\frac{x-3}{2}',
                        [('diff(5*atan((x-3)/2)/2,x)', '5/((x-3)**2+4)')],
                        'مربع زائد رقم، بدون جذر: قانون $\\tan^{-1}$ من 3.4، و $\\frac1a=\\frac12$.'),
                       ('line', 'log(x**2-6*x+13)+5*atan((x-3)/2)/2', 'نجمع الكسرين.')])],
    'U-I8': [
        dict(item='MU2-123-2', hint='كمّل المربع: المركز $-4$، والباقي 9. وبدون جذر وزائد: $\\tan^{-1}$.',
             first=r'x^{2}+8x+25=(x+4)^{2}+3^{2}', claims=[('x**2+8*x+25', '(x+4)**2+3**2')],
             sol_rows=[('tex', r'x^{2}+8x+25=(x+4)^{2}+3^{2}', [('x**2+8*x+25', '(x+4)**2+3**2')],
                        'نص معامل $x$ هو 4. المركز $-4$، والباقي $16-32+25=9=3^2$.'),
                       ('sub', 'x+4', '1', '🔵 $u=x+4$، ومشتقته 1، فما فيه رقم تعديل.'),
                       ('line', 'atan((x+4)/3)/3', 'مربع زائد رقم بدون جذر: $\\frac1a\\tan^{-1}\\frac ua$ من 3.4، و $a=3$.')])],
    'U-I5': [
        dict(item='MU2-52-4', hint='$\\sqrt x$ داخل الدالة، و $\\frac1{\\sqrt x}$ برّا: $u=\\sqrt x$.',
             first=r'\cU{u=\sqrt{x}},\quad \cD{du=\frac{dx}{2\sqrt{x}}}\ \Rightarrow\ \frac{dx}{\sqrt{x}}=2\,du',
             claims=[('diff(sqrt(x),x)', '1/(2*sqrt(x))')],
             sol_rows=[('sub', 'sqrt(x)', '1/(2*sqrt(x))', 'داخل sech و tanh فيه $\\sqrt x$، فهو 🔵 $u$.'),
                       ('tex', r'I=\cA{2}\int\operatorname{sech}u\tanh u\,du', [('2*sech(x)*tanh(x)', '2*sech(x)*tanh(x)')],
                        '$\\frac{dx}{\\sqrt x}=2\\,du$، فـ 🟠 2 تطلع قدّام التكامل مرة وحدة.'),
                       ('tex', r'\int\operatorname{sech}u\tanh u\,du=-\operatorname{sech}u', [('diff(-sech(x),x)', 'sech(x)*tanh(x)')],
                        'مشتقة sech هي 🔴 سالب sech·tanh، فتكاملها بسالب.'),
                       ('line', '-2*sech(sqrt(x))', 'نرجّع $u=\\sqrt x$.')])],
    'U-I7': [
        dict(item='MU2-52-2', hint='$\\ln x$ داخل cosh، ومشتقتها $\\frac1x$ برّا: $u=\\ln x$.',
             first=r'\cU{u=\ln x},\quad \cD{du=\frac{dx}{x}}', claims=[('diff(log(x),x)', '1/x', 't')],
             sol_rows=[('sub', 'log(x)', '1/x', '$\\ln x$ هي المعكوس لـ $e^x$، ومشتقتها $\\frac1x$ موجودة برّا: دالة ومشتقتها.', 'u', 't'),
                       ('tex', r'I=\cA{\frac15}\int\cosh u\,du', [('Rational(1,5)', 'Rational(1,5)')],
                        'الـ 5 في المقام رقم، فـ 🟠 $\\frac15$ تطلع قدّام التكامل.'),
                       ('line', 'sinh(log(x))/5', 'تكامل cosh هو sinh بدون سالب، ونرجّع $u=\\ln x$.')])],
}

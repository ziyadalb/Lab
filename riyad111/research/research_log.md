# سجل البحث الخارجي

## P08 — الكسور الجزئية (2026-11-01)
الاستعلامات المستعملة: 2 من 3 للنمط كله.

| # | الاستعلام | المصادر المفيدة | الفكرة المستفادة | الحالة |
|---|---|---|---|---|
| 1 | Heaviside cover-up method partial fractions distinct linear factors … repeated factors limitation | [MIT 18.01 – Heaviside cover-up](https://www.ocw.mit.edu/courses/18-01-single-variable-calculus-fall-2006/dda2e5c7522ac8cd77fba8ba9f8524ac_f_hscvr_up_methd.pdf)، [Orloff (MIT) – pf coverup](https://math.mit.edu/~stoopn/18.031/pf-coverup.pdf)، [Gordon College handout](https://www.cs.gordon.edu/courses/mat225/handouts/heavyside.pdf)، [Toronto MAT136 week 4](https://www.math.toronto.edu/jko/MAT136_week_4.pdf) | الإخفاء صحيح للعوامل الخطية غير المكررة. في المكرر يعطي ثابت أعلى قوة فقط. لا يعطي ثوابت التربيعية، والباقي بالمقارنة | مطابق لإثباتنا الرمزي R3، ومقيد بشروطه |
| 2 | partial fractions linear times irreducible quadratic … compare coefficients x^2 and constant term | [UT Austin M408S – LM 7.4](https://web.ma.utexas.edu/users/m408s/CurrentWeb/LM7-4-9.php)، [USC Math 142 – 8.5](https://people.math.sc.edu/josephcf/Teaching/142/Files/Lecture%20Notes/Chapter8/8.5.pdf) | عوّض بجذور العوامل الخطية أولًا، ثم قارن المعاملات للباقي. الحد الثابت وأعلى قوة أسرع معادلتين | مطابق للطريقة الأساسية المرشحة |

- لم تُفتح الصفحات نفسها. الاعتماد على ملخصات نتائج البحث، والإثبات الفعلي رمزي في `reports/verify_p08.json`.
- الأدوات كلها من النطاق: تعويض أعداد، ومقارنة معاملات، وتكاملات 3.1 و3.4. لا تحتاج آلة حاسبة.
- القراءة المباشرة لـ `x(x^2+a^2)` (ب2) استنتاج من بنية الأسئلة، وليست من مصدر خارجي. أُثبتت رمزيًا (R1).

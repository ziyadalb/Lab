# ريض 111 — الكويز الثاني (4.2، 5.1، 5.2)

مواد مذاكرة عربية لطالب واحد لكويز الثلاثاء 27 أكتوبر 2026، مبنية من مذكرة د. طارق الفضل (2024) واختبارات المقرر السابقة 1445–1447.

**الحالة: المرحلة 3 (العينة = كرّاسة الاختصارات) جاهزة وتنتظر الموافقة.** المذكرة الكاملة والاختباران التجريبيان بعد الموافقة.

## المخرجات الحالية
| الملف | ما هو |
|---|---|
| `out/sample/MATH111_Quiz2_Shortcuts_Sample.pdf` | العينة: كرّاسة الاختصارات، 44 صفحة A4 |
| `data/registry_full.csv` | السجل الكامل (257 صفًا) — **يكشف الأسئلة المحجوزة؛ للتدقيق فقط** |
| `data/registry_study_safe.csv` | السجل الآمن للطالب (المحجوز يظهر بمعرفه المعتم فقط) |
| `reports/verification_report.json` | تحقق SymPy: 155 جوابًا، 63 حلًا رسميًا، 22 قانونًا من المذكرة، 14 اختصارًا |
| `reports/booklet_checks.json` | 171 فحصًا أُجري أثناء بناء الكرّاسة (كل صيغة وكل سطر أرقام) |
| `reports/pdf_qa_sample.json`، `reports/leak_check.json` | فحوص PDF والتسرب |
| `reports/visual_qa_log.md`، `reports/page_budget.md` | المراجعة البصرية لكل الصفحات وميزانية الصفحات |
| `audit/` | مراجعة المصادر، دراسة الاختصارات، مراجعة التسرب، الحجز (`holdout_audit.json` فيه نصوص المحجوز — لا يُفتح قبل المحاكاة) |
| `progress.md` | السجل المرحلي والقرارات |

## البناء من جديد
المتطلبات: Python 3.13 مع `sympy==1.14.0` و `pymupdf` و `pdfplumber`؛ Node مع `npm install` (KaTeX 0.16.22 والخط)؛
Playwright 1.56 مع Chromium مثبت عامًا؛ poppler (`pdftotext`, `pdftoppm`).

```bash
# 1) من نسخك من الأصول (لا تُرفع إلى المستودع لحقوق النشر):
python3 tools/ingest_pdfs.py <مجلد الأصول> <مجلد الإخراج>   # نصوص وصور كل الصفحات للمراجعة (أسماء الملفات في SOURCES)
python3 tools/build_items.py                     # data/items.json من التعابير المراجعة يدويًا
python3 tools/verify.py                          # كل الأجوبة والحلول الرسمية والقوانين والاختصارات
python3 tools/select_holdout.py                  # الحجز (ثابت بالبذرة؛ لا يُعاد بعد التأليف)
python3 tools/build_registry.py <transcribed_source.json>
# 2) العينة: بناء + KaTeX + PDF بتمريرتين + فحوص
./tools/build_sample.sh
```

كل صيغة في الكرّاسة تُطبع من تعبير SymPy نفسه الذي يُفحص؛ فشل أي فحص يوقف البناء. الأسئلة المحجوزة ونسخها القريبة ممنوعة في `tools/booklet_engine.py` (`use()` يرفضها).

## المصادر والحقوق
- المذكرة والاختبارات ملك أصحابها؛ لا تُنسخ ملفاتها هنا. تُذكر الصفحة والرقم لكل سؤال.
- الخط: IBM Plex Sans Arabic (رخصة OFL، `src/fonts/`). KaTeX (رخصة MIT، `src/katex/`).

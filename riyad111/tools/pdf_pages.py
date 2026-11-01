"""Helpers: named-destination pages -> toc.json; set a clean outline; QA report.
Usage: python3 -I tools/pdf_pages.py names <pdf> <toc.json>
       python3 -I tools/pdf_pages.py outline <pdf> <outline.json>
       python3 -I tools/pdf_pages.py qa <pdf> <report.json>
"""
import json, os, sys
import pymupdf

def names(pdf, out):
    d = pymupdf.open(pdf)
    pages = {n: dest['page'] + 1 for n, dest in d.resolve_names().items() if dest.get('page', -1) >= 0}
    open(out, 'w').write(json.dumps(pages, ensure_ascii=False, indent=0))
    print('anchors with pages:', len(pages))

def outline(pdf, spec):
    d = pymupdf.open(pdf)
    pages = {n: dest['page'] + 1 for n, dest in d.resolve_names().items() if dest.get('page', -1) >= 0}
    toc = []
    for level, title, anchors in json.load(open(spec, encoding='utf-8')):
        pg = next((pages[a] for a in anchors if a in pages), None)
        if pg is None:
            raise SystemExit('outline: no page for ' + anchors[0])
        toc.append([level, title, pg])
    d.set_toc(toc)
    tmp = pdf + '.tmp'; d.save(tmp, garbage=1, deflate=True); d.close(); os.replace(tmp, pdf)
    print('outline entries:', len(toc))

def qa(pdf, out):
    d = pymupdf.open(pdf)
    fonts = sorted({f[3] for p in d for f in p.get_fonts(full=True)})
    links = sum(1 for p in d for l in p.get_links() if l.get('kind') in (pymupdf.LINK_GOTO, pymupdf.LINK_NAMED))
    import subprocess
    text = [subprocess.run(['pdftotext', '-f', str(i+1), '-l', str(i+1), pdf, '-'], capture_output=True, text=True).stdout for i in range(d.page_count)]
    probes = ['الكسور الجزئية', 'تحليل المقام', 'في', 'حتى', 'الأول', 'محاولاتك', 'النهائي', 'الترشيح', 'Evaluate the following integral', '1445-S1-FE-Q2.4']
    found = {k: [i + 1 for i, t in enumerate(text) if k in t][:6] for k in probes}
    rep = dict(pages=d.page_count, fonts=fonts, internal_links=links, toc=d.get_toc(), text_probes=found,
               sample_page_chars={i + 1: len(t) for i, t in enumerate(text)})
    open(out, 'w').write(json.dumps(rep, ensure_ascii=False, indent=1))
    print(json.dumps({k: rep[k] for k in ('pages', 'internal_links', 'text_probes')}, ensure_ascii=False))
    print('fonts:', fonts)

if __name__ == '__main__':
    {'names': names, 'outline': outline, 'qa': qa}[sys.argv[1]](*sys.argv[2:])

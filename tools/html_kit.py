"""Small HTML vocabulary for the study documents (RTL Arabic page, isolated LTR math/English)."""
import html


def esc(s):
    return html.escape(s, quote=True)


def mi(latex):
    """Inline math, isolated so it never mixes with the Arabic text direction."""
    return '<bdi class="mi" dir="ltr" data-tex="%s"></bdi>' % esc(latex)


def md(latex, cls=''):
    return '<div class="md %s" dir="ltr" data-tex="%s"></div>' % (cls, esc(latex))


def en(text, cls=''):
    return '<div class="en %s" dir="ltr" lang="en">%s</div>' % (cls, esc(text))


def p(text, cls=''):
    return '<p class="%s">%s</p>' % (cls, text)


def ul(items, cls=''):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s</li>' % i for i in items))


def box(kind, label, inner, anchor=None):
    a = ' id="%s"' % anchor if anchor else ''
    return ('<section class="box %s"%s><div class="lbl">%s</div><div class="body">%s</div></section>'
            % (kind, a, label, inner))


def table(head, rows, cls=''):
    h = ''.join('<th>%s</th>' % c for c in head)
    r = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in row) for row in rows)
    return '<table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (cls, h, r)


def link(href, text, cls=''):
    return '<a class="%s" href="#%s">%s</a>' % (cls, href, text)


def lines(n, cls='write'):
    return '<div class="%s" style="--n:%d"></div>' % (cls, n)


def chip(text, cls=''):
    return '<span class="chip %s">%s</span>' % (cls, text)

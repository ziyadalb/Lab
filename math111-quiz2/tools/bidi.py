"""Bidi safety for the study documents.

Latin math typed as plain text inside an Arabic sentence is reordered by the Unicode bidi algorithm
(for example "(+C)" shows as "(C+)"). isolate_runs() wraps every such run in a left-to-right <bdi>.
"""
import re

# Latin math typed as plain text inside Arabic (like "(+C)", "(ln x)²", "√(1−x²)", "−2") is reordered by the
# bidi algorithm; every such run is isolated as a left-to-right island.
MATHCH = r"A-Za-z0-9+\-−=()\[\]√²³⁻¹⁰⁴⁵⁶⁷⁸⁹·×/|'^_<>≤≥≠±∞πθλ∫ "
RUN = re.compile('[%s]+' % MATHCH)
TRIGGER = re.compile(r"[A-Za-z√²³⁻¹∫πθλ]|^[\-−]\d")


OPS = '+-−=·×/'
NEEDS = re.compile(r"[+\-−=()√²³⁻¹|/·×^∫]")


GLUE = re.compile(r'(النوعان|النوع|الأنواع|التمرين|تمرين|اليوم|مثال|مراجعة) (\d)')


def _isolate_text(text):
    text = GLUE.sub('\\1\u00a0\\2', text).replace('⇐ ', '⇐\u00a0')

    def fix(m):
        run = m.group(0)
        i, j = 0, len(run)          # the island is run[i:j]; what is cut off stays in the Arabic sentence
        while True:
            while i < j and run[i] == ' ':
                i += 1
            while j > i and run[j - 1] == ' ':
                j -= 1
            core = run[i:j]
            if not core:
                return run
            if core[-1] == '(' or (core[-1] == ')' and core.count('(') < core.count(')')):
                j -= 1
            elif core[0] == ')' or (core[0] == '(' and core.count('(') > core.count(')')):
                i += 1
            elif len(core) > 1 and core[0] in OPS and core[1] == ' ':      # "× ln": the × joins the Arabic words
                i += 1
            elif len(core) > 1 and core[-1] in OPS and core[-2] == ' ':
                j -= 1
            else:
                break
        if core.count('(') != core.count(')') or not TRIGGER.search(core) or not NEEDS.search(core):
            return run
        return run[:i] + '<bdi dir="ltr" class="tx">%s</bdi>' % core + run[j:]
    return RUN.sub(fix, text)


def isolate_runs(html):
    """Apply _isolate_text to text nodes only (not tags, attributes, math placeholders or English blocks)."""
    out, depth_skip = [], 0
    for tok in re.split(r'(<[^>]+>)', html):
        if tok.startswith('<'):
            name = re.match(r'</?\s*([a-zA-Z0-9]+)', tok)
            if re.match(r'<(bdi|div class="en|div class="md|a class="[^"]*" href)', tok) and not tok.endswith('/>'):
                depth_skip += 1 if not tok.startswith('<a') else 0
            elif re.match(r'</(bdi)>', tok) and depth_skip:
                depth_skip -= 1
            elif re.match(r'</div>', tok) and depth_skip and out and _open_skip_div(out):
                depth_skip -= 1
            out.append(tok)
        else:
            out.append(tok if depth_skip or not tok.strip() else _isolate_text(tok))
    return ''.join(out)


def _open_skip_div(out):
    """True when the innermost open div is an English or math block (they hold no Arabic to fix)."""
    depth = 0
    for tok in reversed(out):
        if tok.startswith('</div'):
            depth += 1
        elif tok.startswith('<div'):
            if depth == 0:
                return tok.startswith('<div class="en') or tok.startswith('<div class="md')
            depth -= 1
    return False

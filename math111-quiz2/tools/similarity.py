"""Structural comparison of tasks: exact copy, constant multiple, same shape with changed numbers."""
import re

import sympy as s

from mathlib import P

_NUM = re.compile(r"Integer\(-?\d+\)|Rational\(-?\d+, \d+\)|Float\('[^']*', precision=\d+\)")


def expr_of(item):
    q = item['q']
    return P(q[4:] if q.startswith('raw:') else q)


def shape(e):
    """srepr with every number replaced: same shape = same structure, numbers may differ."""
    return _NUM.sub('#', s.srepr(e))


def relation(a, b):
    """Return 'exact', 'constant_multiple', 'numbers_changed' or None for two task expressions."""
    if a['task'] != b['task']:
        return None
    ea, eb = expr_of(a), expr_of(b)
    if s.simplify(ea - eb) == 0:
        return 'exact'
    ratio = s.simplify(ea / eb)
    if ratio.is_number:
        return 'constant_multiple'
    if shape(ea) == shape(eb):
        na, nb = _NUM.findall(s.srepr(ea)), _NUM.findall(s.srepr(eb))
        changed = sum(1 for p, q in zip(na, nb) if p != q)
        return 'one_number_changed' if changed <= 1 else 'numbers_changed'
    return None


def numbers_of(e):
    return sorted(str(n) for n in e.atoms(s.Number))

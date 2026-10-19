#!/usr/bin/env python3
"""Choose and freeze the 10 held-out questions BEFORE any teaching material is written.

The blueprint is a declared educational choice (not 'the usual quiz distribution'): each mock has
5 independent parts covering the three sections; together 4.2 x4 (2 derivatives, 2 integrals),
5.1 x3, 5.2 x3. Candidates are checked programmatically against the criteria below; the final pick
among valid candidates is a documented manual decision. Opaque ids H01..H10 are shuffled with a
fixed seed so their order reveals nothing.

Run: python tools/select_holdout.py   (needs data/items.json and reports/verification_report_items.json)
Writes audit/holdout_audit.json (full texts, NOT for the student before the mocks) and data/holdout_ids.json.
"""
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from similarity import relation  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SEED = 1112027

# slot -> (item id, reason). Order of slots inside each mock is decided later at random.
PICK = {
    'A': [('1447-S1-SE-Q1.1', '4.2 derivative: cosh^-1 of an exponential + a 4.1 chain term'),
          ('1445-S2-FE-Q2.1', '4.2 integral: completing the square with a leading coefficient'),
          ('1447-S1-FE-Q2.2', '5.1: quadratic times trig with an inner coefficient (fractions)'),
          ('1446-S2-SE-Q2.5', '5.1: exponential times hyperbolic with fractional exponents'),
          ('1445-S2-FE-Q2.6', '5.2: odd sine power, u = cos, three-term expansion')],
    'B': [('1446-S1-SE-Q1.1', '4.2 derivative: tanh^-1 of an exponential + csch of 2/x'),
          ('1445-S1-SE-Q2.7', '4.2 integral: visible derivative, tanh^-1 vs coth^-1 decision'),
          ('1447-S2-SE-Q3.1', '5.1: x times an inverse hyperbolic function'),
          ('1445-S2-SE-Q2.3', '5.2: even secant power, u = tan'),
          ('N52-X12', '5.2: product of cosines with different angles (notes exercise; no exam question of this case)')],
}
PRIOR_EXPOSED = {'1447-S2-SE-Q1.1', '1447-S2-SE-Q1.2', '1447-S2-SE-Q3.3', '1447-S2-SE-Q3.4', '1447-S2-SE-Q3.5',
                 '1447-S2-SE-Q3.6', '1445-S2-SE-Q2.9'}  # solutions present in heldout_reference_answers.json


def main():
    items = {i['id']: i for i in json.loads((ROOT / 'data' / 'items.json').read_text(encoding='utf-8'))}
    ver = {r['id']: r for r in json.loads((ROOT / 'reports' / 'verification_report_items.json').read_text())['items']}
    picked = [pid for mock in PICK.values() for pid, _ in mock]
    assert len(picked) == 10 and len(set(picked)) == 10
    problems, checks = [], {}
    for pid in picked:
        it = items[pid]
        c = dict(in_scope=it['section'] in ('4.2', '5.1', '5.2') and it.get('scope') != 'contrast',
                 real_source=it['kind'] in ('exam', 'notes_exercise'),
                 answer_symbolic=ver[pid]['answer']['status'] == 'symbolic',
                 official_full_domain=(it['kind'] != 'exam') or ver[pid].get('official', {}).get('status') == 'symbolic',
                 not_prior_exposed=pid not in PRIOR_EXPOSED)
        others = [i for i in items.values() if i['case'] == it['case'] and i['id'] not in picked
                  and i['kind'] in ('exam', 'notes_example', 'notes_exercise')]
        c['case_still_taught'] = len(others) >= 1
        checks[pid] = c
        problems += [f'{pid}: {k}' for k, v in c.items() if not v]
    # every copy of a held item is held too; near items are listed for manual review
    linked, near = {}, {}
    for pid in picked:
        for other in items.values():
            if other['id'] in picked:
                continue
            rel = relation(items[pid], other) if other['case'] == items[pid]['case'] or other['task'] == items[pid]['task'] else None
            if rel == 'exact':
                linked.setdefault(pid, []).append(other['id'])
            elif rel in ('constant_multiple', 'one_number_changed', 'numbers_changed'):
                near.setdefault(pid, []).append(dict(id=other['id'], relation=rel, kind=other['kind']))
    rng = random.Random(SEED)
    order = picked[:]
    rng.shuffle(order)
    hid = {pid: f'H{n:02d}' for n, pid in enumerate(order, 1)}
    audit = dict(seed=SEED, unit='independent part (one derivative or one integral)',
                 blueprint='declared educational choice: 4.2 x4 (2 derivatives + 2 integrals), 5.1 x3, 5.2 x3; '
                           'each mock covers all three sections',
                 section_counts=Counter(items[p]['section'] for p in picked),
                 mocks={m: [dict(hid=hid[p], item=p, reason=r, q=items[p]['q'], answer=items[p]['answer'],
                                 source=items[p]['src']) for p, r in v] for m, v in PICK.items()},
                 criteria=checks, criteria_failures=problems, held_copies=linked, near_items=near,
                 novelty='not guaranteed: every past question and key is in the student\'s patterns workbook; '
                         'exposure is unknown (user answer)')
    (ROOT / 'audit').mkdir(exist_ok=True)
    (ROOT / 'audit' / 'holdout_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=1), encoding='utf-8')
    (ROOT / 'data' / 'holdout_ids.json').write_text(json.dumps(
        dict(hids=sorted(hid.values()), held_items=hid, held_copies=linked,
             # not used as worked examples or drills in study material (near copies of a held item)
             avoid=sorted({n['id'] for v in near.values() for n in v
                           if n['relation'] in ('constant_multiple', 'one_number_changed')}),
             same_pattern_allowed=sorted({n['id'] for v in near.values() for n in v
                                          if n['relation'] == 'numbers_changed'})), ensure_ascii=False, indent=1),
        encoding='utf-8')
    print('criteria failures:', problems or 'none')
    print('held copies:', linked)
    print('near items:', {k: [(n['id'], n['relation']) for n in v] for k, v in near.items()})
    print('sections:', audit['section_counts'])


if __name__ == '__main__':
    main()

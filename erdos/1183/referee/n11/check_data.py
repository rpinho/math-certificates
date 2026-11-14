"""Original-set checks of colouring, lower-bound data, and optional SAT model.
This file neither imports the encoder nor reads producer programs.
"""
import itertools
import json
import sys
from pathlib import Path

def decode(mask):
    assert type(mask) is int and 0 <= mask < 2048
    return frozenset(i + 1 for i in range(11) if mask // (2 ** i) % 2)

def closed(masks, minimum):
    assert len(masks) == len(set(masks)) >= minimum
    family = {decode(x) for x in masks}
    for a in family:
        for b in family:
            assert a.union(b) in family and a.intersection(b) in family
    return family

data = json.loads(Path('certificates/1183_n11_coloring.json').read_text())
assert data['n'] == 11 and len(data['color_by_mask']) == 2048
assert data['rank_colors'] == [1,0,0,0,1,0,0,1,1,1,0,1]
colours = data['color_by_mask']
assert all(type(c) is int and c in (0,1) for c in colours)
assert all(colours[m] == data['rank_colors'][len(decode(m))] for m in range(2048))
print('COLOURING VALID', [colours.count(c) for c in (0,1)])
explicit = [1,3,5,7,31,63,1023]
closed(explicit, 7)
assert {colours[m] for m in explicit} == {0}
print('EXPLICIT SEVEN', explicit, [sorted(decode(m)) for m in explicit])

lower = json.loads(Path('certificates/1183_lower7_families.json').read_text())
assert lower['n'] == 11 and lower['target'] == 7
rank_patterns = []
for family in lower['families']:
    sets = closed(family, 7)
    rank_patterns.append({len(s) for s in sets})
coverage = []
for word in itertools.product((0,1), repeat=12):
    hits = [i for i, ranks in enumerate(rank_patterns) if len({word[r] for r in ranks}) == 1]
    assert hits, word
    coverage.append(hits[0])
Path('certificates/lower_coverage.json').write_text(json.dumps(coverage) + '\n')
print('LOWER DATA VALID', len(rank_patterns), 'closed families; all', len(coverage), 'rank words covered')
print('LOWER FAMILY SIZE RANGE', min(map(len,lower['families'])), max(map(len,lower['families'])))

if len(sys.argv) > 1:
    cnf, solver_log = map(Path, sys.argv[1:])
    model = {}
    for line in solver_log.read_text().splitlines():
        if line.startswith('v '):
            for literal in map(int, line.split()[1:]):
                if literal:
                    assert abs(literal) not in model or model[abs(literal)] == (literal > 0)
                    model[abs(literal)] = literal > 0
    meta = json.loads(cnf.with_suffix('.json').read_text())
    assert model and len(model) == meta['variables']
    count = 0
    with cnf.open() as stream:
        for line in stream:
            if line[0] in 'cp': continue
            clause = list(map(int,line.split()))
            assert clause[-1] == 0
            assert any(model[abs(x)] == (x>0) for x in clause[:-1])
            count += 1
    assert count == meta['clauses']
    masks = [m for i,m in enumerate(meta['masks'],1) if model[i]]
    closed(masks, meta['minimum'])
    assert {colours[m] for m in masks} == {meta['colour']}
    dest = Path('certificates') / (cnf.stem + '_witness.json')
    dest.write_text(json.dumps(masks) + '\n')
    print('SAT MODEL VALID', len(masks), 'members, colour', meta['colour'], masks)

#!/usr/bin/env python3
"""Separately written (same agent), definition-level finite lower-bound check."""
import json,pathlib,itertools,collections
p=json.loads(pathlib.Path('certificates/1183_lower7_families.json').read_text());n=p['n'];families=p['families'];patterns=[]
for fam in families:
 sets=[frozenset(i for i in range(n) if (z>>i)&1) for z in fam];S=set(sets)
 assert len(S)==len(sets)>=7
 assert all((x|y) in S and (x&y) in S for x in S for y in S)
 patterns.append({len(s) for s in S})
# Directly exhaust every two-colouring of the ranks, without a SAT solver.
for code in range(1<<(n+1)):
 assert any(len({(code>>r)&1 for r in ranks})==1 for ranks in patterns),code
# Check the exact rank-CNF against the listed families and colour-swap unit.
actual=[]
for line in pathlib.Path('data/1183_lower7_rank.cnf').read_text().splitlines():
 if line.startswith('p '):assert line=='p cnf 12 '+str(2*len(families)+1)
 else:actual.append(tuple(sorted(map(int,line.split()[:-1]))))
expected=[(1,)]
for rs in patterns:
 expected.extend([tuple(sorted(r+1 for r in rs)),tuple(sorted(-r-1 for r in rs))])
assert collections.Counter(actual)==collections.Counter(expected)
# Johnson graphs are connected: the chain-swap argument can connect all r-sets.
for r in range(1,n):
 level={frozenset(c) for c in itertools.combinations(range(n),r)};seen={next(iter(level))};todo=list(seen)
 while todo:
  s=todo.pop()
  for x in s:
   for y in set(range(n))-s:
    t=(s-{x})|{y}
    if t not in seen:seen.add(t);todo.append(t)
 assert seen==level
print(json.dumps({'result':'VALID LOWER BOUND 7','n':n,'closed_families_checked':len(families),'rank_colourings_covered':2**(n+1),'chain_swap_connectivity':'all ranks connected','scope':'all colourings by the written balanced-chain reduction'}))

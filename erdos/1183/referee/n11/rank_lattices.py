"""Second upper bound: enumerate weighted ideal lattices, independent of SAT.

A monochromatic chain has at most six members, hence a monochromatic
distributive lattice has at most five join-irreducibles. A lattice of
subsets has a base of b always-present coordinates; each remaining active
coordinate corresponds to one poset element and has a positive multiplicity.
Unused coordinates do not affect ranks. Enumerate every natural labeling of
each poset on <=5 elements and every feasible positive weight vector.
"""
import itertools
import json
from pathlib import Path

rank_colour = [1,0,0,0,1,0,0,1,1,1,0,1]

def posets(m):
    pairs = list(itertools.combinations(range(m), 2))
    for code in range(1 << len(pairs)):
        predecessors = [set() for _ in range(m)]
        for k, (a,b) in enumerate(pairs):
            if code & (1 << k):
                predecessors[b].add(a)
        if any(not predecessors[a] <= predecessors[b]
               for b in range(m) for a in predecessors[b]):
            continue
        ideals = []
        for bits in itertools.product((False,True), repeat=m):
            subset = {i for i in range(m) if bits[i]}
            if all(predecessors[i] <= subset for i in subset):
                ideals.append(sorted(subset))
        yield [sorted(p) for p in predecessors], ideals

def weights(m, budget):
    if m == 0:
        yield ()
    else:
        for first in range(1, budget - m + 2):
            for tail in weights(m - 1, budget - first):
                yield (first,) + tail

counts, assignments, valid = [], 0, [0,0]
maximum, examples = [0,0], [None,None]
for m in range(6):
    orders = list(posets(m))
    counts.append(len(orders))
    for b in range(12):
        for w in weights(m, 11-b):
            for predecessors, ideals in orders:
                assignments += 1
                c = rank_colour[b]
                ranks = [b + sum(w[i] for i in ideal) for ideal in ideals]
                if all(rank_colour[r] == c for r in ranks):
                    valid[c] += 1
                    if len(ideals) > maximum[c]:
                        maximum[c] = len(ideals)
                        examples[c] = dict(base=b, weights=w, predecessors=predecessors,
                                           ideals=ideals, ranks=ranks)
    print('poset_size',m,'natural_posets',len(orders),'cumulative_assignments',assignments,
          'maxima',maximum,flush=True)
result = dict(n=11, max_join_irreducibles=5, poset_counts=counts,
              assignments=assignments, monochromatic_assignments=valid,
              colour_maxima=maximum, examples=examples)
Path('certificates/rank_lattices.json').write_text(json.dumps(result,indent=2)+'\n')
assert maximum == [7,7], result
print('INDEPENDENT WEIGHTED-POSET UPPER BOUND VERIFIED', maximum)

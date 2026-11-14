"""Separately written (same agent) complete-colouring and elementary lower-bound check.

The upper-bound proof still needs both exact-CNF checks and backward drat-trim.
No encoder imports and no third-party research code.
"""
import collections, itertools, json, pathlib
d=json.loads(pathlib.Path('certificates/n12_coloring.json').read_text())
assert d['n']==12 and d['candidate_value']==7
colors=d['color_by_mask'];assert len(colors)==4096 and set(colors)=={0,1}
sets=[frozenset(j for j in range(12) if (s//2**j)%2) for s in range(4096)]
for s,c in zip(sets,colors):assert c==d['rank_colors'][len(s)]
for color in [0,1]:
    m=json.loads(pathlib.Path(f'data/n12_1100101100011_c{color}.cnf.json').read_text())
    assert m['n']==12 and m['target']==8 and m['color']==color and not m['union_only']
    assert m['members']==[mask for mask,c in enumerate(colors) if c==color]
    assert m['ranks']==''.join(map(str,d['rank_colors']))
F={sets[s] for s in d['seven_member_witness']}
assert len(F)==7 and all(colors[sum(2**j for j in s)]==1 for s in F)
assert all(s|t in F and s&t in F for s,t in itertools.product(F,repeat=2))
# Every colouring restricts to a colouring of the canonical 13-member maximal chain.
# The majority colour on any chain is a lattice, regardless of its endpoints.
chain=[frozenset(range(r)) for r in range(13)]
for bits in itertools.product([0,1],repeat=13):
    majority=collections.Counter(bits).most_common(1)[0][0]
    G={s for s,b in zip(chain,bits) if b==majority}
    assert len(G)>=7 and all(s|t in G and s&t in G for s,t in itertools.product(G,repeat=2))
print('VALID COMPLETE COLOURING: all 4096 subsets, matching both no-at-least-eight CNF memberships')
print('VALID SEVEN-MEMBER WITNESS:',d['seven_member_witness'])
print('VALID LOWER BOUND 7: every colouring of a 13-set maximal chain has a closed majority family of at least seven')

"""Separately written (same agent): compare base, reconstruct all lex clauses.
No encoder imports. Ground-coordinate swaps are reconstructed using actual sets.
"""
import argparse,collections,itertools,json,pathlib
p=argparse.ArgumentParser();p.add_argument('base');p.add_argument('extended');a=p.parse_args()
b=json.loads(pathlib.Path(a.base+'.json').read_text());n=b['n']
subsets=[frozenset(j for j in range(n) if (s//2**j)%2) for s in b['members']]
number={s:i+1 for i,s in enumerate(subsets)};counter=b['variables'];expected=collections.Counter()
for u in range(n):
    for v in range(u+1,n):
        def swap(s):return frozenset(v if x==u else u if x==v else x for x in s)
        pairs=[(number[s],number[swap(s)]) for s in subsets if number[s]<number[swap(s)]]
        previous=None
        for left,right in pairs:
            counter+=1;leading=[] if previous is None else [-previous]
            for cl in [leading+[-left,right],leading+[-left,-right,counter],leading+[left,right,counter]]:
                expected[tuple(sorted(cl))]+=1
            previous=counter
with open(a.base) as base,open(a.extended) as ext:
    bh=base.readline().split();eh=ext.readline().split()
    assert int(eh[2])==counter and int(eh[3])==int(bh[3])+sum(expected.values())
    for l in base:assert ext.readline()==l
    have=collections.Counter(tuple(sorted(map(int,l.split()[:-1]))) for l in ext)
assert have==expected
# Verify the comparator recurrence exhaustively for lengths 1..4, including
# all auxiliary assignments. Induction extends the same recurrence to any length.
for length in range(1,5):
    for bits in itertools.product([False,True],repeat=2*length):
        left=bits[:length];right=bits[length:];sat=False
        for aux in itertools.product([False,True],repeat=length):
            prev=True;ok=True
            for x,y,q in zip(left,right,aux):
                ok &= ((not prev) or (not x) or y)
                ok &= ((not prev) or (not x) or (not y) or q)
                ok &= ((not prev) or x or y or q)
                prev=q
            sat |= ok
        assert sat==(left<=right)
print(json.dumps({'result':'LEX EXTENSION EXACT','base_variables':b['variables'],'variables':counter,'added_clauses':sum(expected.values()),'transpositions':n*(n-1)//2,'soundness':'The colouring and closure property are invariant under all ground permutations. A global lex-minimum member vector in each orbit satisfies all comparisons. Base counter auxiliaries can be recomputed for its selected members.'}))

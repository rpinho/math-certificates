"""Independent finite structural-case checker. Enumerates block multiplicities,
not the partition recursion used to generate the artifact. Standard library.
"""
import itertools,json
from fractions import Fraction as Q
from pathlib import Path
R=Path(__file__).resolve().parent
spec=json.loads((R/'candidate.json').read_text());caps={int(k):Q(v) for k,v in spec['caps'].items()}
packet=json.loads((R/'structure_cases.json').read_text())
assert packet['schema']=='c44-minimum-structure-cases-v1'
assert packet['scope']=='all-local-degrees-d count maximizer'
assert packet['degrees']==[4,5,6,7,8]
seen={};rows=[]
for c in packet['cases']:
    d=c['d'];k=d-1;r=c['fixed'];sizes=c['block_sizes']
    assert d in packet['degrees'] and type(r)==int and 0<=r<=k
    assert sizes==sorted(sizes) and all(type(m)==int and m>=2 for m in sizes)
    assert r+sum(m-1 for m in sizes)==k
    h=r+sum(sizes)
    assert h==k+len(sizes)==c['controls']
    assert 2*k-h==r+sum(m-2 for m in sizes)==c['deficit_from_2k']
    budget=Q(h+1)+(2**d-2)*caps[d-1]
    assert Q(c['minimum_R_budget'])==budget
    assert c['minimum_R_floor']<=budget<c['minimum_R_floor']+1
    key=(d,r,tuple(sizes));assert key not in seen;seen[key]=c
for d in packet['degrees']:
    k=d-1;expected=set()
    for counts in itertools.product(*(range(k//a+1) for a in range(1,k+1))):
        used=sum(a*c for a,c in enumerate(counts,1))
        if used>k:continue
        sizes=tuple(m for m,c in enumerate(counts,2) for _ in range(c))
        expected.add((d,k-used,sizes))
    actual={key for key in seen if key[0]==d};assert actual==expected
    here=[seen[key] for key in actual]
    worst=max(c['minimum_R_floor'] for c in here)
    extremal=[c for c in here if c['minimum_R_floor']==worst]
    assert len(extremal)==1
    assert extremal[0]['fixed']==0 and extremal[0]['block_sizes']==[2]*k
    rows.append({'d':d,'types':len(here),'worst_minimum_R':worst,
       'all_other_minimum_R_at_most':worst-1,'worst_type':'phi_2^'+str(k)})
assert sum(r['types'] for r in rows)==len(seen)==113
out={'status':'PASS','case_count':len(seen),'rows':rows}
(R/'verification_structure_cases.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

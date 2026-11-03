"""Exact finite controls for the new coefficientwise profile-envelope lemma."""
from collections import Counter
import json
from pathlib import Path


def partitions(n,low=1):
    if n==0:
        yield ()
    for a in range(low,n+1):
        for tail in partitions(n-a,a):yield (a,)+tail


checked=0
for leaves in range(31):
    for positive in partitions(leaves):
        for r in range(max(len(positive),1),13):
            y=(0,)*(r-len(positive))+positive
            cnt=Counter(y)
            for B in range(cnt[0]+1):
                for U in range(cnt[2],r+1):
                    e2=U-((leaves-r+B-U)%2)
                    e1=(3*(r-B)-leaves-e2)//2
                    e3=(leaves-r+B-e2)//2
                    if min(e1,e2,e3)<0:continue
                    x=(0,)*B+(1,)*e1+(2,)*e2+(3,)*e3
                    assert len(x)==r and sum(x)==leaves
                    for t in range(max(3,max(y,default=0))+1):
                        assert sum(max(a-t,0) for a in x)<=sum(max(a-t,0) for a in y), (x,y,B,U,t)
                    checked+=1
# A deliberately invalid envelope is rejected by the same exact criterion.
bad=(0,4);good=(1,3)
assert any(sum(max(a-t,0) for a in bad)>sum(max(a-t,0) for a in good) for t in range(5))
out={'status':'PASS','scope':'finite integer controls, not a substitute for the written majorization proof','cases':checked,'leaf_sum_max':30,'strip_count_max':12,'invalid_envelope_rejected':True}
Path('artifacts/profile_envelope_controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

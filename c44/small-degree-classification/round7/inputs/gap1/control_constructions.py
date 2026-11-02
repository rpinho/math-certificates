"""Exact small address and PR284 checks; no imports from public construction code."""
from pathlib import Path
import json,sys,hashlib
from collections import Counter
R=Path(__file__).resolve().parent
def transform(a):
    a=a.copy();step=1
    while step<len(a):
        for b in range(0,len(a),2*step):
            for j in range(b,b+step):u,v=a[j],a[j+step];a[j]=u+v;a[j+step]=u-v
        step*=2
    return a
def convolution_boolean(p,M):
    z={}
    for s,c in p.items():
        for t,d in p.items():z[s^t]=z.get(s^t,0)+c*d
    assert {s:c for s,c in z.items() if c}=={0:M*M}
addresses=[]
for m in range(6):
    p={}
    for a in range(1<<m):
        for subset in range(1<<m):p[subset|(1<<(m+a))]=(-1)**((a&subset).bit_count())
    n=(1<<m)+m;union=0
    for s in p:union|=s
    assert union==(1<<n)-1 and max(s.bit_count() for s in p)==m+1
    convolution_boolean(p,1<<m)
    addresses.append({'degree':m+1,'variables':n,'CHS_variables':3*(1<<m)-2})
family=[]
for d in (2,3,4):
    path=R/'sources/pr284_instances'/f'd{d}_n{3*d-1}.json'
    z=json.loads(path.read_text());n=z['n'];M=1<<d
    coeff=[0]*(1<<n)
    for support,c in z['terms']:
        mask=sum(1<<i for i in support);assert coeff[mask]==0;coeff[mask]=int(c);assert abs(int(c))==1
    assert sum(c!=0 for c in coeff)==(M-1)*M
    assert max(s.bit_count() for s,c in enumerate(coeff) if c)==d
    values=transform(coeff);hist=Counter(values)
    assert set(hist)=={-M,0,M} and hist[0]*(1<<d)==1<<n
    completed=[]
    # New selector is the high bit, so the two sign branches are concatenated.
    for selector in (1,-1):completed.extend(v//M if v else selector for v in values)
    assert set(completed)<=set((-1,1))
    spectrum=transform(completed)
    degree=max(s.bit_count() for s,c in enumerate(spectrum) if c)
    local=[any(c and (s>>j&1) for s,c in enumerate(spectrum)) for j in range(n+1)]
    assert degree<=2*d+1
    family.append({'degree':d,'variables':n,'zero_count':hist[0],
                   'completion_degree':degree,'completion_variables':sum(local),
                   'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
out={'status':'PASS','ordinary_addresses':addresses,'PR284_ternary_family':family}
(R/'control_constructions.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

"""Exact sparse-Fourier checks of CHS witnesses and minimum-derivative types.
No generator or verifier imports. Integer convolution and Walsh evaluation.
"""
import json
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parent

def xi(d,start):
    if d==1:return {1<<start:1},start+1
    a,end=xi(d-1,start+2);b,end=xi(d-1,end)
    out={}
    for p,c in a.items():out[p|(1<<start)]=c;out[p|(1<<(start+1))]=c
    for p,c in b.items():out[p|(1<<start)]=c;out[p|(1<<(start+1))]=-c
    assert len(out)==len(a)*4
    return out,end

def walsh(a):
    a=a.copy();h=1
    while h<len(a):
        for i in range(0,len(a),2*h):
            for j in range(i,i+h):a[j],a[j+h]=a[j]+a[j+h],a[j]-a[j+h]
        h*=2
    return a

def classify(values,k):
    # Independently recover equality blocks directly from the support columns.
    h=(len(values)-1).bit_length();active=[x for x,v in enumerate(values) if v]
    assert len(active)==1<<(h-k)
    anchor=active[0]
    columns={};fixed=[]
    for j in range(h):
        col=tuple(((x^anchor)>>j)&1 for x in active)
        if not any(col):fixed.append(j)
        else:columns.setdefault(col,[]).append(j)
    groups=list(columns.values())
    assert all(len(g)>=2 for g in groups)
    assert len(fixed)+sum(len(g)-1 for g in groups)==k
    assert h==k+len(groups)<=2*k
    for x in range(1<<h):
        y=x^anchor
        on=not any(y>>j&1 for j in fixed) and all(len({y>>j&1 for j in g})==1 for g in groups)
        sign=values[anchor]*(-1)**sum((y>>g[0])&1 for g in groups if len(g)%2==0)
        assert values[x]==(sign if on else 0)
    return {'fixed':len(fixed),'block_sizes':sorted(map(len,groups)),'controls':h,
            'deficit_from_2k':2*k-h}

def potential(p):
    local={}
    for mask,c in p.items():
        if c:
            w=mask.bit_count()
            for i in range(mask.bit_length()):
                if mask>>i&1:local[i]=max(local.get(i,0),w)
    return sum((F(1,2**v) for v in local.values()),F(0))

spec=json.loads((R/'candidate.json').read_text());caps={int(d):F(c) for d,c in spec['caps'].items()}
rows=[]
for d in range(1,7):
    poly,n=xi(d,0);M=1<<(d-1)
    assert n==3*M-2
    assert all(mask.bit_count()==d and abs(c)==1 for mask,c in poly.items())
    union=0
    for mask in poly:union|=mask
    assert union==(1<<n)-1 and potential(poly)==F(n,2**d)
    conv={}
    entries=list(poly.items())
    for j,(s,c) in enumerate(entries):
        for t,e in entries[j+1:]:conv[s^t]=conv.get(s^t,0)+2*c*e
    assert all(c==0 for c in conv.values()) and sum(c*c for c in poly.values())==M*M
    types=[];minimum=0;representative=None
    for i in range(n):
        deriv={s^(1<<i):c for s,c in poly.items() if s>>i&1}
        energy=sum(c*c for c in deriv.values())
        assert energy>=M and (energy==M or 2*energy>=3*M)
        if energy!=M:continue
        minimum+=1
        H=0
        for mask in deriv:H|=mask
        controls=[j for j in range(n) if H>>j&1];h=len(controls)
        assert h<=2*d-2
        coeff=[0]*(1<<h)
        for mask,c in deriv.items():
            compressed=sum(((mask>>j)&1)<<q for q,j in enumerate(controls))
            coeff[compressed]=c
        vals=walsh(coeff)
        assert all(v in (-M,0,M) for v in vals)
        types.append(classify([v//M for v in vals],d-1))
        if d>=2:assert all(s&H for s in poly)
        if representative is None:representative=(i,controls,H,vals)
    rec={'d':d,'variables':n,'terms':len(poly),'minimum_coordinates':minimum,
         'normalized_weight':str(F(n,2**d)),'upper_cap':str(caps[d]),
         'count_headroom':int(caps[d]*2**d)-n,'types':types}
    assert F(n,2**d)<=caps[d]
    if d>=2:
        i,controls,H,vals=representative;avg=F(0);active=0
        for assignment in range(1<<len(controls)):
            branch={}
            for s,c in poly.items():
                exponent=sum(((s>>j)&1)*((assignment>>q)&1) for q,j in enumerate(controls))
                t=s&~H
                branch[t]=branch.get(t,0)+((-c) if exponent%2 else c)
            branch={s:c for s,c in branch.items() if c}
            assert max((s.bit_count() for s in branch),default=0)<=d-1
            if vals[assignment]:
                assert branch=={1<<i:vals[assignment]};active+=1
            avg+=potential(branch)
        avg/=1<<len(controls)
        assert F(active,1<<len(controls))==F(1,M)
        assert potential(poly)<=F(len(controls),2**d)+avg
        minimum_cap=F(2*d-2,2**d)+F(1,2*M)+F(M-1,M)*caps[d-1]
        assert F(len(controls),2**d)+avg<=minimum_cap
        rec['expected_branch_D']=str(avg);rec['minimum_budget']=str(minimum_cap)
    rows.append(rec)
def add(a,b):
    c=a.copy()
    for s,v in b.items():c[s]=c.get(s,F(0))+v
    return {s:v for s,v in c.items() if v}
def mul(a,b):
    c={}
    for s,v in a.items():
        for t,w in b.items():c[s^t]=c.get(s^t,F(0))+v*w
    return {s:v for s,v in c.items() if v}
def scaled(a,t):return {s:v*t for s,v in a.items()}
def var(i):return {1<<i:F(1)}
def mux(s,t,x,y):
    return add(scaled(mul(add(var(s),var(t)),var(x)),F(1,2)),
               scaled(mul(add(var(s),scaled(var(t),-1)),var(y)),F(1,2)))
# Two quadratic CHS functions sharing precisely one Fourier mask.
g=mux(0,1,3,4);h=mux(0,2,3,5);z=6
f=add(mul({0:F(1,2),1<<z:F(1,2)},g),mul({0:F(1,2),1<<z:F(-1,2)},h))
sharp=[]
for d in range(3,9):
    assert max(s.bit_count() for s in f)==d
    assert mul(f,f)=={0:F(1)}
    inf=sum((v*v for s,v in f.items() if s>>z&1),F(0))
    assert inf==F(3,2**d)
    sharp.append({'degree':d,'selector_influence':str(inf),'ratio_to_minimum':'3/2'})
    w=d+4
    f=add(mul({0:F(1,2),1<<w:F(1,2)},f),{0:F(1,2),1<<w:F(-1,2)})
result={'status':'PASS','witnesses':rows,'sharp_gap_witnesses':sharp}
(R/'control_witnesses.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','witnesses':[{k:v for k,v in row.items() if k!='types'} for row in rows],
                  'sharp_gap_witnesses':sharp},indent=2))

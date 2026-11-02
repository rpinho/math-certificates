"""Independent finite controls of the analytic lemmas; not a universal proof.
Uses integer Walsh transforms and literal truth values, without search imports.
"""
import json, math, os
from pathlib import Path
from fractions import Fraction as Q
R=Path(__file__).resolve().parent
def walsh(v):
    v=list(v);h=1
    while h<len(v):
        for p in range(0,len(v),2*h):
            for j in range(p,p+h):v[j],v[j+h]=v[j]+v[j+h],v[j]-v[j+h]
        h*=2
    return v
def degrees(coeff,n):
    return [max((s.bit_count() for s,a in enumerate(coeff) if a and s>>i&1),default=0) for i in range(n)]
def affine_test(masks,k):
    assert len(masks)==1<<k
    base=masks[0];diff={s^base for s in masks}
    span={0}
    for s in sorted(diff):
        if s not in span:span|={t^s for t in list(span)}
    assert span==diff
    union=0
    for s in masks:union|=s
    assert union.bit_count()<=2*k
def finite():
    rows=[]
    for n in range(1,5):
        N=1<<n;minimum=0;parity=0;count=0
        for table in range(1<<N):
            vals=[1 if table>>x&1 else -1 for x in range(N)];c=walsh(vals)
            d=max((s.bit_count() for s,a in enumerate(c) if a),default=0)
            if not d:continue
            M=1<<(d-1)
            assert all((a*M)%N==0 for a in c)
            z=[a*M//N for a in c]
            for i in range(n):
                masks=[s^(1<<i) for s,a in enumerate(z) if a and s>>i&1]
                if not masks:continue
                energy=sum(a*a for s,a in enumerate(z) if s>>i&1)
                flips=sum(vals[x]!=vals[x^(1<<i)] for x in range(N))
                assert Q(energy,M*M)==Q(flips,N)>=Q(1,M)
                if d>=2:
                    assert energy%2==0;parity+=1
                    if energy!=M:assert energy>=M+2
                if energy==M:
                    assert all(abs(z[s|(1<<i)])==1 for s in masks)
                    affine_test(masks,d-1);minimum+=1
            count+=1
        rows.append({'n':n,'nonconstant_tables':count,'minimum_derivatives':minimum,'parity_checks':parity})
        print(rows[-1],flush=True)
    return rows

def plus(a,b):
    out=a.copy()
    for s,c in b.items():
        out[s]=out.get(s,Q(0))+c
        if not out[s]:del out[s]
    return out
def product(a,b):
    out={}
    for s,c in a.items():
        for t,e in b.items():out[s^t]=out.get(s^t,Q(0))+c*e
    return {s:c for s,c in out.items() if c}
def sc(a,c):return {s:v*c for s,v in a.items() if v*c}
def var(i):return {1<<i:Q(1)}
def D(p):
    union=0
    for s in p:union|=s
    return sum((Q(1,2**max(s.bit_count() for s in p if s>>i&1)) for i in range(union.bit_length()) if union>>i&1),Q(0))
def xi(d,offset=0):
    if d==1:return var(offset),offset+1
    left,end=xi(d-1,offset+2);right,end=xi(d-1,end)
    s=var(offset);t=var(offset+1)
    return plus(product(sc(plus(s,t),Q(1,2)),left),product(sc(plus(s,sc(t,-1)),Q(1,2)),right)),end
def symbolic():
    out=[]
    for d in range(2,7):
        p,n=xi(d);M=2**(d-1)
        assert n==3*2**(d-1)-2 and D(p)==Q(n,2**d)
        assert all(s.bit_count()==d and abs(c)==Q(1,M) for s,c in p.items())
        # Independently check Booleanity by the Fourier convolution identity.
        z={s:int(c*M) for s,c in p.items()};conv={}
        for s,a in z.items():
            for t,b in z.items():conv[s^t]=conv.get(s^t,0)+a*b
        assert conv[0]==M*M and not any(v for s,v in conv.items() if s)
        mincount=0
        for i in range(n):
            masks=[s^(1<<i) for s in z if s>>i&1]
            if len(masks)==M:affine_test(masks,d-1);mincount+=1
        out.append({'CHS_degree':d,'relevant_variables':n,'Fourier_terms':len(p),'minimum_derivatives':mincount})
    # A concrete mixed-degree function tests the corrected duplication argument.
    # Outer selector chooses a quadratic multiplexer or a cubic parity.
    multiplexer=sc(plus(plus(var(1),var(2)),product(var(3),plus(var(1),sc(var(2),-1)))),Q(1,2))
    f=plus(product(sc(plus({0:Q(1)},var(0)),Q(1,2)),multiplexer),product(sc(plus({0:Q(1)},sc(var(0),-1)),Q(1,2)),{(1<<4)|(1<<5)|(1<<6):Q(1)}))
    low=[1,2,3];mapping={1:7,2:8,3:9};copy={}
    for s,c in f.items():
        t=s
        for a,b in mapping.items():
            if s>>a&1:t^=(1<<a)|(1<<b)
        copy[t]=c
    selector=var(10)
    h=plus(product(sc(plus({0:Q(1)},selector),Q(1,2)),f),product(sc(plus({0:Q(1)},sc(selector,-1)),Q(1,2)),copy))
    assert max(s.bit_count() for s in h)==4 and D(h)==D(f)+Q(1,16)>D(f)
    assert product(f,f)=={0:Q(1)} and product(h,h)=={0:Q(1)}
    out.append({'corrected_CHS_duplication':'PASS','old_D':str(D(f)),'new_D':str(D(h))})
    return out
if __name__=='__main__':
    print('PID',os.getpid(),flush=True)
    result={'status':'PASS finite exact controls, not formal verification','truth_tables':finite(),'symbolic_witnesses':symbolic()}
    (R/'sources/structure_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result,flush=True)

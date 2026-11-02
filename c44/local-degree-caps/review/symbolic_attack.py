"""Sparse exact constructions and mixed-degree CHS attacks; reviewer code."""
from fractions import Fraction as Q
from collections import defaultdict
from pathlib import Path
import json,time
start=time.time();root=Path(__file__).resolve().parent
def add(*ps):
    c=defaultdict(Q)
    for p in ps:
        for s,a in p.items():c[s]+=a
    return {s:a for s,a in c.items() if a}
def scale(p,a):return {s:a*v for s,v in p.items() if a*v}
def mul(p,q):
    c=defaultdict(Q)
    for s,a in p.items():
        for t,b in q.items():c[s^t]+=a*b
    return {s:a for s,a in c.items() if a}
def var(i):return {1<<i:Q(1)}
one={0:Q(1)}
def shift(p,k):return {s<<k:a for s,a in p.items()}
def info(p):
    local={}
    for s,a in p.items():
        for i in range(s.bit_length()):
            if s>>i&1:local[i]=max(local.get(i,0),s.bit_count())
    return max(s.bit_count() for s in p),local,sum((Q(1,2**d) for d in local.values()),Q(0))
def xi(d):
    if d==1:return var(0),1
    p,n=xi(d-1)
    return add(scale(mul(add(var(0),var(1)),shift(p,2)),Q(1,2)),
               scale(mul(add(var(0),scale(var(1),-1)),shift(p,n+2)),Q(1,2))),2*n+2
def restrict(p,H,alpha):
    return add(*[{s&~H:a*(-1)**((s&H&alpha).bit_count())} for s,a in p.items()])
def gf2rank(xs):
    piv={}
    for x in xs:
        while x:
            j=x.bit_length()-1
            if j not in piv:piv[j]=x;break
            x^=piv[j]
    return len(piv)
def test(p):
    d,local,D=info(p);M=2**(d-1)
    assert sum(a*a for a in p.values())==1
    # Integer Boolean convolution independent of formula evaluation.
    coeff={s:int(a*M) for s,a in p.items()}
    assert all(Q(coeff[s],M)==p[s] for s in p)
    conv=defaultdict(int)
    for s,a in coeff.items():
        for t,b in coeff.items():conv[s^t]+=a*b
    assert conv[0]==M*M and all(not a for s,a in conv.items() if s)
    mins=[]
    for i in local:
        A={s^(1<<i):a for s,a in p.items() if s>>i&1}
        E=sum((a*M)**2 for a in A.values())
        assert E.denominator==1 and E%2==0 if d>=2 else E==1
        assert E>=M and (E==M or E>=M+2)
        if E==M:
            T=list(A);H=0
            for s in T:H|=s
            assert len(T)==M and all(abs(a)==Q(1,M) for a in A.values())
            assert gf2rank([s^T[0] for s in T])==d-1
            assert H.bit_count()<=2*(d-1)
            assert all(s&H for s in p if s.bit_count()==d)
            mins.append((i,H))
    # Direct multi-coordinate restriction inequality on first minimum control set.
    restricted=None
    if mins:
        i,H=mins[0];bits=[j for j in range(H.bit_length()) if H>>j&1]
        total=Q(0);dictators=0;maxdeg=0
        for a in range(2**len(bits)):
            mask=sum(1<<j for k,j in enumerate(bits) if a>>k&1)
            q=restrict(p,H,mask)
            dd,ll,ww=info(q);maxdeg=max(maxdeg,dd);total+=ww
            if set(q)=={1<<i} and abs(q[1<<i])==1:dictators+=1
        mean=total/2**len(bits)
        control=sum(Q(1,2**local[j]) for j in local if H>>j&1)
        assert D<=control+mean
        assert dictators*M==2**len(bits) and maxdeg<=d-1
        restricted={'controls':len(bits),'branches':2**len(bits),'dictators':dictators,
                    'mean_D':str(mean),'control_cost':str(control),'max_degree':maxdeg}
    return {'degree':d,'variables':len(local),'D':str(D),'terms':len(p),
            'minimum_coordinates':len(mins),'restriction':restricted}

out={'CHS':[test(xi(d)[0]) for d in range(2,7)]}
# Nonhomogeneous minimum derivative: a fresh selector chooses Xi_3 or a
# dictator. A minimum derivative has masks of sizes 2 and 3, both present.
small,_=xi(3)
nonhom=add(scale(mul(add(one,var(10)),small),Q(1,2)),
           scale(mul(add(one,scale(var(10),-1)),var(11)),Q(1,2)))
out['nonhomogeneous_minimum']=test(nonhom)
# Ordinary disjoint composition: Xi_2 o Xi_2 and Xi_2 o Xi_3, Xi_3 o Xi_2.
def substitute(p,i,q):
    a={s^(1<<i):v for s,v in p.items() if s>>i&1}
    b={s:v for s,v in p.items() if not(s>>i&1)}
    return add(b,mul(a,q))
out['compositions']=[]
for outer,inner in [(2,2),(2,3),(3,2)]:
    p,n=xi(outer);q,m=xi(inner)
    for i in range(n):p=substitute(p,i,shift(q,n+i*m))
    out['compositions'].append(test(p))
# A degree-4 mixed-degree example: switch between a two-variable parity and
# a three-variable parity. The low-local-degree block is {x1,x2}.
f=add(scale(mul(add(one,var(0)),{(1<<1)|(1<<2):Q(1)}),Q(1,2)),
      scale(mul(add(one,scale(var(0),-1)),{(1<<3)|(1<<4)|(1<<5):Q(1)}),Q(1,2)))
out['mixed_before']=test(f)
and_sign=scale(add(var(6),var(7),mul(var(6),var(7)),scale(one,-1)),Q(1,2))
old=substitute(f,1,and_sign)
out['old_single_AND']=test(old)
assert info(old)[2]<info(f)[2]
# Correct simultaneous duplication, a fresh selector w at bit8.
copy={((s&~6)|((s&6)<<5)):a for s,a in f.items()}
h=add(scale(mul(add(one,var(8)),f),Q(1,2)),
      scale(mul(add(one,scale(var(8),-1)),copy),Q(1,2)))
out['correct_simultaneous_duplication']=test(h)
assert info(h)[0]<=4 and info(h)[2]>info(f)[2]
out['status']='PASS';out['seconds']=time.time()-start
(root/'receipts'/'symbolic_attack.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

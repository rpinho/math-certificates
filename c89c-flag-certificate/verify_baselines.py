"""Independent exact arithmetic replay of the classical baseline calculations.

Conlon's recurrence is enclosed using integer root isolation, without Decimal
powers or floating point. This checks arithmetic; the general theorems are
proved/cited in ELEMENTARY.md and PRIOR_ART.md.
"""
from fractions import Fraction as Q
from math import factorial
from decimal import Decimal, localcontext
import json

def binom(a,b):
    if a<b: return 0
    return factorial(a)//factorial(b)//factorial(a-b)

def dec(q):
    with localcontext() as ctx:
        ctx.prec=40
        return str(Decimal(q.numerator)/Decimal(q.denominator))

rows=[]
for r,R,m in [(6,252,301),(6,165,196),(6,166,197),(5,46,56)]:
    # Check the ratio's change of sign immediately on either side; it decreases
    # linearly in m, so these inequalities prove the global maximum.
    delta_before=r*(R-2)+1-(r-1)*(m-1)
    delta_after=r*(R-2)+1-(r-1)*m
    assert delta_before>=0 and delta_after<=0
    deletion=Q(m-R+1,binom(m,r))
    average=Q(1,binom(R,r))
    decaen=Q(1,binom(R-1,r-1))
    assert decaen>deletion>average
    row=dict(r=r,R=R,m=m,average=str(average),deletion=str(deletion),decaen=str(decaen),decaen_decimal=dec(decaen))
    rows.append(row);print(row)

S=10**70
def root_bounds(x,p):
    """Return exact floor/ceil bounds with denominator S for x**(1/p)."""
    target=x.numerator*S**p//x.denominator
    lo,hi=0,1 << ((target.bit_length()+p-1)//p)
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**p<=target: lo=mid
        else: hi=mid
    assert lo**p*x.denominator<=x.numerator*S**p
    assert hi**p*x.denominator>x.numerator*S**p
    return Q(lo,S),Q(hi,S)

def snap(lo,hi):
    a=lo.numerator*S//lo.denominator
    b=-((-hi.numerator*S)//hi.denominator)
    assert Q(a,S)<=lo<=hi<=Q(b,S)
    return Q(a,S),Q(b,S)

M={}
for a in range(1,7):
    for b in range(1,7):
        if min(a,b)==1: M[a,b]=(Q(1),Q(1));continue
        p=max(a,b)
        xlo,xhi=M[a-1,b];ylo,yhi=M[a,b-1]
        alo,_=root_bounds(1/xhi,p);_,ahi=root_bounds(1/xlo,p)
        blo,_=root_bounds(1/yhi,p);_,bhi=root_bounds(1/ylo,p)
        M[a,b]=snap(1/(ahi+bhi)**p,1/(alo+blo)**p)
for k in (5,6):
    lo,hi=M[k,k]
    assert hi-lo<Q(1,10**60)
    print('Conlon2012 exact enclosure',k,dec(lo),dec(hi))
assert M[6,6][0]>Q(6185496869639,10**24)
assert M[6,6][1]<Q(6185496869640,10**24)
assert M[6,6][1]<Q(rows[0]['deletion'])
with open('baseline_verified.json','w') as f:
    json.dump(dict(baselines=rows,conlon={str(k):[str(x) for x in M[k,k]] for k in (5,6)}),f,indent=2)
print('PASS: exact baseline arithmetic, global deletion maxima, rational Conlon enclosures.')

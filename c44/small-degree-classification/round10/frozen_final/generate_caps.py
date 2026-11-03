"""Candidate scalar artifact generation; no acceptance role."""
from fractions import Fraction as F
import decimal, functools, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
H=96
counts={1:1,2:4,3:10,4:22}
caps={d:F(n,1<<d) for d,n in counts.items()}

def grid(d,limit):
    k=d-1;m=1<<k
    points={2-F(1,1<<j) for j in range(k)}
    points.add(F(2))
    # New ceiling changes at half-integer 2k*lambda and at integer lambda.
    for a in range(4*k,int(2*k*limit)+2):
        z=((2*a+1)*m+8*k-1)//(8*k)
        points.add(F(2*z,m))
    for a in range(2,int(limit)+1):points.add(F(a))
    for a in range(4*k,int(2*k*limit)+2):
        q=(a*m+4*k-1)//(4*k)
        points.update(F(2*z,m) for z in (q,q+1))
    for a in range(int(F(4*k,3)*limit)+2):
        q=(3*a*m+8*k-1)//(8*k)
        points.update(F(2*z,m) for z in (q,q+1) if 2*z>=2*m)
    return sorted(x for x in points if 1<=x<=limit and (x<2 or (x*m/2).denominator==1))

def hcap(d,x):
    value=2*(d-1)*x;h=int(value)
    if x.denominator>1 and value.denominator==1:h-=1
    if d==5 and x==F(3,2):h=min(h,10)
    if d==6 and x==F(3,2):h=min(h,12)
    if d==6 and x==F(7,4):h=min(h,13)
    if d>=4 and x>1 and 2*(d-1)*x-h<F(1,2):h-=1
    return h

@functools.lru_cache(None)
def selector(d):
    return max([F(1,2)]+[F(1,4)+F(1,1<<(t+1))+caps[t]/2 for t in range(1,d-1)])

def budget(d,x):
    k=d-1;c=caps[k];b=selector(d);hi=hcap(d,x);cut=min(hi,int(F(4*k,3)*x))
    outcomes=[]
    for h in {hi,cut}:
        bound=(1<<d)*c+h+1-2*c*x
        retained=False
        if x>1 and 3*h>4*k*x:
            other=(1<<d)*c+h-2*c*x+4*(b-(c+F(1,2))/2)
            retained=other<bound;bound=min(bound,other)
        outcomes.append((bound,h,retained))
    return max(outcomes)

rows=[]
for d in range(5,H+1):
    m=1<<(d-1);lower=3*m-2
    candidates=grid(d,F(d*m,lower))
    value,x=max((min(int(budget(d,x)[0]),int(F(d*m)/x)),x) for x in candidates)
    counts[d]=value
    excluded=grid(d,F(d*m,value+1))
    peak,x=max((budget(d,y)[0],y) for y in excluded)
    assert peak<value+1
    witnesses=[(y,budget(d,y)) for y in grid(d,F(d*m,value)) if budget(d,y)[0]>=value]
    assert witnesses
    y,w=min(witnesses)
    rows.append(dict(d=d,R=value,previous=str(caps[d-1]),b=str(selector(d)),representatives=len(excluded),
                     first_excluded=value+1,worst=dict(normalized_weight=str(x),budget=str(peak)),
                     feasible=dict(normalized_weight=str(y),budget=str(w[0]),h=w[1],retained=w[2])))
    caps[d]=F(value,1<<d)
    assert caps[d]>=caps[d-1] and caps[d]-caps[d-1]<=F(d*(d-1),1<<d)
    if d<=10:print(d,value,caps[d],rows[-1]['worst'],flush=True)
tail=F(H*H+3*H+4,1<<H)
bound=caps[H]+tail
previous=F('159363009872336981657958180965/79228162514264337593543950336')
decimal.getcontext().prec=60
number=decimal.Decimal(bound.numerator)/decimal.Decimal(bound.denominator)
strict=(number*10**10).to_integral_value(rounding=decimal.ROUND_CEILING)/10**10
artifact=dict(schema='c44-round10-signcaps-v1',status='candidate, unrefereed',horizon=H,
              base_counts={str(d):counts[d] for d in range(1,5)},
              third_weight_artifact='baseline/frozen/certificates/third_weight.json',near_equality_artifact='near_equality.json',previous_bound=str(previous),
              strict_claim=str(strict),improvement_bar='1/10000',rows=rows,
              caps={str(d):str(c) for d,c in caps.items()},tail=str(tail),bound=str(bound))
assert previous-bound>F(1,10000) and bound<F(str(strict))
(ROOT/'certificates/caps.json').write_text(json.dumps(artifact,indent=2)+'\n')
print('BOUND',bound,number,'STRICT',strict,'IMPROVEMENT',float(previous-bound),flush=True)

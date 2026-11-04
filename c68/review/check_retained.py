"""Independent exact rational products and interval arc integration."""
import json, pathlib
from fractions import Fraction as F
from intervals import I,PI,sincos,RN,DN,UP,D
OUT=pathlib.Path('results')

def acos_enclosure(x):
    x=I(x);assert -1<x.lo<=x.hi<1
    lo=D(0);hi=PI.hi
    while UP.subtract(hi,lo)>D('1e-45'):
        mid=RN.divide(RN.add(lo,hi),D(2));co=sincos(I(mid))[1]
        if co.lo>x.hi:lo=mid
        elif co.hi<x.lo:hi=mid
        else:raise AssertionError(('acos unresolved',x,co,lo,hi))
    return I(lo,hi)

def energy(coeff,a,cap):
    # T(theta)=.24+a cos(theta)-.24 cos(2theta).
    a=F(a);cap=F(cap);disc=I(a*a-4*F('12/25')*(cap-F('12/25'))).sqrt()
    rminus=(I(a)-disc)/I('24/25');rplus=(I(a)+disc)/I('24/25')
    # If T(0)>=cap the active interval starts at zero; T(pi)<cap here.
    assert -a<cap
    alpha=I(0) if a>=cap else acos_enclosure(rplus)
    beta=acos_enclosure(rminus)
    n=len(coeff)-1
    def integrals(angle):
        s,c=sincos(angle);sk,ck=I(0),I(1);vals=[angle]
        for k in range(1,n+3):
            sk,ck=sk*c+ck*s,ck*c-sk*s
            vals.append(sk/k)
        return vals
    aa=integrals(alpha);bb=integrals(beta)
    ints=[b-a for a,b in zip(aa,bb)]
    moments=[]
    for k in range(n+1):
        b=(I(cap)*PI if k==0 else I(0))+(I('6/25')-I(cap))*ints[k]+I(a)/2*(ints[abs(k-1)]+ints[k+1])-I('3/25')*(ints[abs(k-2)]+ints[k+2])
        moments.append(b/PI)
    corr=[sum(coeff[j]*coeff[j+k] for j in range(n+1-k)) for k in range(n+1)]
    en=I(corr[0])*moments[0]+2*sum(I(corr[k])*moments[k] for k in range(1,n+1))
    return en,alpha,beta

raw=json.load(open('../review_c68r2/receipts/nearby-candidate.json'));coeff=list(map(F,raw['coefficients']))
assert coeff[1]==1 and F(raw['m1'])==F('1/50') and F(raw['m2'])==1
old,_,oldend=energy(coeff,F('1/50'),F('1/2500'))
new,_,newend=energy(coeff,F('1/50'),F('1/50'))
assert old.hi<I('21/200').lo and new.lo>I('23/200').hi
# The endpoint moments are an explicit PSD measure with masses .51,.49 at +-1.
assert F('51/100')-F('49/100')==F('1/50')
third=json.load(open('../c68r2/counterexample.json'));v=list(map(F,third['V_coefficients']));prod=[F(0)]*(len(v)+2)
for j,c in enumerate(v):prod[j]+=c;prod[j+2]-=c
lhs=F('3/25')*sum(c*c for c in prod);rhs=F('7/100')*sum(v[j]**2 for j in range(3))
assert lhs-rhs==F('-1/100')
# Counterexample to naive J=a uses genuine equal masses with m1=i*40/401.
y=F(40,401);x=F(399,401);b=x*x-y*y;S=y*y+F('6/25')*(1-b*b);J=y*y
assert J<=S<y
# Exact supplied balanced contact configurations, independently using complex pairs.
def cmul(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def dot(z,w):return z[0]*w[0]+z[1]*w[1]
def moment(weights,points,power):
    pp=[(F(1),F(0)) for _ in points]
    for _ in range(power):pp=[cmul(x,z) for x,z in zip(pp,points)]
    return tuple(sum(w*p[k] for w,p in zip(weights,pp)) for k in (0,1))
configs=[]
for case in json.load(open('../c68r3/certificates/contact-configurations.json'))['cases']:
    weights=list(map(F,case['weights']));points=[tuple(map(F,z)) for z in case['domain']];images=[tuple(map(F,z)) for z in case['image_directions']]
    assert sum(weights)==1 and all(dot(z,z)==1 for z in points+images)
    assert moment(weights,images,1)==(0,0)
    m1=moment(weights,points,1);m2=moment(weights,points,2)
    S=dot(m1,m1)+F('6/25')*(1-dot(m2,m2))
    T=[dot(z,m1)+F('6/25')*(1-dot(cmul(z,z),m2)) for z in points]
    u=min(((1-dot(points[i],points[j]))-F('6/25')*(1-dot(cmul(points[i],points[i]),cmul(points[j],points[j]))))/(1-dot(images[i],images[j])) for i in range(len(points)) for j in range(i))
    for i in range(len(points)):
        assert sum(weights[j]*(1-dot(images[i],images[j])) for j in range(len(points)))==1
        assert u<=1-T[i]
    aa=I(dot(m1,m1)).sqrt()
    if dot(m1,m1)==0:J=I(0)
    else:
        q=F(1,2)*(1+dot(m2,cmul(m1,m1))/dot(m1,m1));J=aa*(I(q)+aa)/(1+aa)
    assert I(max(T)).lo>=J.hi or dot(m1,m1)==0
    assert I(1-u).lo>=J.hi or dot(m1,m1)==0
    if case['expect_row_improvement']:assert J.lo>I(S).hi
    configs.append({'name':case['name'],'u':str(u),'S':str(S),'J':J.pair(),'maxT':str(max(T)),'row_slack':str(1-u-max(T))})
result={'arithmetic':'independent rational products + custom 65-digit decimal interval arcs','old_0105_energy':old.pair(),'old_gap':(old-I('21/200')).pair(),'new_row_energy':new.pair(),'new_0115_gap':(new-I('23/200')).pair(),'old_arc_endpoint':oldend.pair(),'new_arc_endpoint':newend.pair(),'third_coefficient':{'lhs':str(lhs),'rhs':str(rhs),'gap':str(lhs-rhs)},'false_floor_J_equals_a':{'a':str(y),'J':str(y*y),'S':str(y*y+F('6/25')*(1-b*b))},'exact_geometric_cases':configs,'all_pass':True}
(OUT/'retained.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

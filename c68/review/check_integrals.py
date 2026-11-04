"""Independent interval enclosure of actual continuous weighted moments.
Uses local bounds on g(t)/(1-t); does not use the submitted cubic envelope.
"""
import json,math
from fractions import Fraction as F
from intervals import I,PI,sincos
c=I('447/1000');R=F('99/100');w=-c.log();p=PI/(2*w);q=(-PI**2/w).exp();Psi=(1+q)**2/(8*q);B=(2/Psi).sqrt()
data=json.load(open('../c68r3/certificates/certificate-0447.json'));nodes=list(map(I,data['nodes']));weights=list(map(I,data['weights']))
ks=[1,2,172,647,648,649,1799];integs={k:I(0) for k in ks}
for j in range(1000):
    a=R+(1-R)*F(j,1000);b=R+(1-R)*F(j+1,1000)
    tt=I(I(a).lo,I(b).hi);d=1-tt;u=-p*tt.log()
    # -log(t)/(1-t)=sum delta^n/(n+1), including its continuous value at t=1.
    ratio=sum(d**n/(n+1) for n in range(11))
    rem=d**11/(12*(1-d));ratio+=I(0,rem.hi)
    # sin(u)/u, Taylor polynomial through u^16; Lagrange remainder.
    sinc=sum((-1)**n*u**(2*n)/math.factorial(2*n+1) for n in range(9))
    er=u**18/math.factorial(19);sinc+=I(er.hi.copy_negate(),er.hi)
    ss=u*sinc;xx=B*ss
    slope=2*B*p*ratio*sinc/((1+xx**2).sqrt()+xx)
    assert slope.lo>0
    for k in ks:
        integ=(I(b)**(k+1)-I(a)**(k+1))/(k+1)-(I(b)**(k+2)-I(a)**(k+2))/(k+2)
        assert integ.lo>0
        integs[k]+=slope*integ
G=[];Q=[]
for j,t in enumerate(nodes):
    if j==0:G.append(I(0));Q.append(I(0));continue
    ss=sincos(-p*t.log())[0];D=Psi/(2*ss**2);H=(1+D).sqrt();g=2/(1+H)
    G.append(g);Q.append(D/(H*(1+H)**2))
rows=[]
for k in ks:
    base=I(R)**(k+1)/(k+1)+integs[k]-sum(wt*(1-g)*t**k for wt,g,t in zip(weights,G,nodes))
    corr=sum(wt*qq*t for wt,qq,t in zip(weights,Q,nodes)) if k==1 else I(0)
    new=base+I('23/200')*corr;assert new.lo>0
    row={'k':k,'actual_continuous_integral':integs[k].pair(),'weighted_margin':new.pair()}
    if k==1:
        old=base+I('19/200')*corr
        # Include the formerly discarded continuous .095 Q(t)t correction in upper bound.
        # Q=g(1-1/H)/2 <=g/2, hence integral <= .095/2 * integral g*t.
        old+=I(0,(I('19/400')*integs[1]).hi)
        assert old.hi<0;row['old_0095_margin_including_continuous_upper']=old.pair()
    rows.append(row)
result={'method':'1000-cell interval enclosure of g/(1-t) using log and sinc series','c':'447/1000','samples':rows,'all_pass':True}
json.dump(result,open('results/direct-integrals.json','w'),indent=2);print(json.dumps(result,indent=2))

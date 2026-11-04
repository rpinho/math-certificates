"""Fresh quantitative check; data-only reads from candidate and predecessor."""
import json, pathlib, sys, math, hashlib
from fractions import Fraction as F
from intervals import I,PI,sincos,sinh,cosh,tanh
OUT=pathlib.Path('results');OUT.mkdir(exist_ok=True)
def run(path,name):
    data=json.load(open(path)); c=I(data['c']); R=I(data['R']); kap=I(data['kappa']); z=I(data['zeta'])
    qnodes=list(map(F,data['nodes']));qweights=list(map(F,data['weights']))
    assert len(qnodes)==len(qweights)==8 and all(w>0 for w in qweights)
    assert all(qnodes[i]<qnodes[i+1] for i in range(7))
    assert qnodes[0]==F(data['c'])**2 and qnodes[-1]==F(data['R']) and sum(qweights)==F(data['R'])
    nodes=list(map(I,qnodes));weights=list(map(I,qweights))
    w=-c.log();A=PI**2/w;q=(-A).exp();Psi=(1+q)**2/(8*q);p=PI/(2*w)
    hypotheses=[I(1)/3-1/cosh(A/2)**2,2*(1-8*kap)*Psi-16*sinh(A/4)**2,tanh(A/8)**2-(1+8*kap)*PI**2/64,(1-4*kap)/2-1/cosh(A/8)**2,Psi-6,PI+p*R.log()]
    assert all(x.lo>0 for x in hypotheses)
    gg=[];ee=[]
    for j,t in enumerate(nodes):
        if j==0:gg.append(I(0));ee.append(I(0));continue
        s=sincos(-p*t.log())[0]
        # Rationalized formula has no small-sine division.
        xx=(2/Psi).sqrt()*s
        g=2*xx/((1+xx**2).sqrt()+xx)
        invH=xx/(1+xx**2).sqrt()
        gg.append(g);ee.append(z*g*(1-invH)/2)
    K=2*(2/Psi).sqrt()*p
    poly=[K,K/2-4*p*p/(Psi*R*R),-K*p*p/(6*R**3)]
    def integral_monomial(j,k):
        return sum(((-1)**l)*math.comb(j,l)*(1-R**(k+l+1))/(k+l+1) for l in range(j+1))
    ordinary=[];weighted=[]
    selected={1,2,3,10,50,100,171,172,173,300,500,647,648,649,1000,1798,1799,1800,3000,5999,6000}
    allA=[];allB=[]
    for k in range(1,6000):
        atom=sum(weight*t**k for weight,t in zip(weights,nodes))
        aa=atom-R**(k+1)/(k+1)
        assert aa.lo>0,(name,'ordinary',k,aa)
        rel=aa*(k+1)/R**(k+1);allA.append((rel.lo,k))
        if k in selected:ordinary.append({'k':k,'margin':aa.pair(),'relative':rel.pair()})
        if k>=1800:continue
        integ=sum(poly[j-1]*integral_monomial(j,k) for j in range(1,4))
        bb=R**(k+1)/(k+1)+integ-sum(wt*(1-g)*t**k for wt,g,t in zip(weights,gg,nodes))
        if k==1:bb+=sum(wt*e*t for wt,e,t in zip(weights,ee,nodes))
        assert bb.lo>0,(name,'weighted',k,bb)
        rel=bb*(k+1)/R**(k+1);allB.append((rel.lo,k))
        if k in selected:weighted.append({'k':k,'margin':bb.pair(),'relative':rel.pair(),'tail_integral_lower_bound':integ.pair()})
    tailA=qweights[-1]*6001-F(data['R']);assert tailA>0
    a0=I('999/1000');b0=I('1249/1250');u0=-p*a0.log()
    slope=p*(1+(1-b0)/2)*(1-u0**2/6)
    smax=I(2).sqrt()*slope*(1-a0)
    ell=2*I(2).sqrt()*slope/(smax+(smax**2+Psi).sqrt())
    assert u0.lo>0 and (6-u0**2).lo>0 and ell.lo>0
    tailB=ell*(1-b0)*(b0-a0)*a0**1800-sum(wt*t**1800 for wt,t in zip(weights,nodes))
    assert tailB.lo>0 and max(qnodes)<F('999/1000')
    rec={'input':path,'sha256':hashlib.sha256(open(path,'rb').read()).hexdigest(),'arithmetic':'independent directed Decimal interval, 65 digits','c':data['c'],'pi':PI.pair(),'hypothesis_positive_margins':[h.pair() for h in hypotheses],'ordinary_range':[1,5999],'weighted_range':[1,1799],'min_ordinary_relative':[str(min(allA)[0]),min(allA)[1]],'min_weighted_relative':[str(min(allB)[0]),min(allB)[1]],'ordinary_samples':ordinary,'weighted_samples':weighted,'ordinary_tail_exact_gap':str(tailA),'weighted_tail_slope':ell.pair(),'weighted_tail_gap':tailB.pair(),'all_pass':True}
    (OUT/(name+'.json')).write_text(json.dumps(rec,indent=2))
    print(name,rec['min_ordinary_relative'],rec['min_weighted_relative'],tailB,flush=True)
# Baseline first, with our independently derived cubic envelope and 1800 tail.
run('../c68r2/certificate-44685.json','baseline-moments')
run('../c68r3/certificates/certificate-0447.json','candidate-moments')

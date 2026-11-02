"""Outward-interval audit of the useful coefficient correction. No search code."""
import argparse,json
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,fmpq,ctx
ctx.prec=320
def I(x):
    x=Q(x);return arb(fmpq(x.numerator,x.denominator))
p=argparse.ArgumentParser();p.add_argument('certificate');p.add_argument('--out',default='inequality-audit.json');a=p.parse_args();d=json.loads(Path(a.certificate).read_text())
c=I(d['c']);R=I(d['R']);zeta=I(d['zeta']);w=-c.log();A=arb.pi()**2/w;q=(-A).exp();Psi=(1+q)**2/(8*q)
def ge(t):
    if Q(t)==Q(d['c'])**2:return arb(0),arb(0)
    sigma=(arb.pi()*I(t).log()/(2*w)).sin()**2
    H=(1+Psi/(2*sigma)).sqrt();g=2/(1+H)
    e=(zeta/2)*g*(1-1/H)
    return g,e
rows=[];old_atomic=arb(0);correction=arb(0)
for t,v in zip(d['nodes'],d['weights']):
    g,e=ge(t);old_atomic+=I(v)*(1-g)*I(t);correction+=I(v)*e*I(t)
    rows.append(dict(t=str(Q(t)),g=str(g),epsilon=str(e),relative_epsilon=str(e/g) if g>0 else 'endpoint'))
gR,_=ge(d['R'])
# On [R,1], g decreases because R>=c and sin^2 decreases toward 1.
old_B1_upper=R**2/2+gR*(1-R**2)/2-old_atomic
assert old_B1_upper<0,'this measure did not demonstrate a failure of the old coefficient criterion'
out=dict(c=d['c'],status='PASS interval audit',old_B1_upper_bound=str(old_B1_upper),old_B1_relative_upper=str(2*old_B1_upper/R**2),atomic_B1_improvement=str(correction),relative_B1_improvement=str(2*correction/R**2),atoms=rows)
Path(a.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

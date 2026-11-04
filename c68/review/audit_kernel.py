"""Independent cross-checks for the custom interval engine, not proof by sampling."""
import random,json
from fractions import Fraction as F
from decimal import Decimal as D
from intervals import I,PI,sincos
from flint import arb,ctx
ctx.prec=384
rng=random.Random(681104)
def contains(v,x):return F(v.lo)<=x<=F(v.hi)
count=0
for _ in range(500):
    a,b,c,d=[F(rng.randint(-100000,100000),rng.randint(1,10000)) for _ in range(4)]
    a,b=sorted((a,b));c,d=sorted((c,d));aa=I(I(a).lo,I(b).hi);bb=I(I(c).lo,I(d).hi)
    for x in (a,b,(a+b)/2):
        for y in (c,d,(c+d)/2):
            assert contains(aa+bb,x+y) and contains(aa-bb,x-y) and contains(aa*bb,x*y)
            if not c<=0<=d:assert contains(aa/bb,x/y)
            for n in (0,1,2,3,8,17,172):assert contains(aa**n,x**n)
            count+=1
# Confirm our intervals enclose independently computed high-precision Arb balls.
def ar(q):
    q=F(q);return arb(q.numerator)/q.denominator
def enclosed(ours,reference):
    assert ar(ours.lo)<reference.lower() and ar(ours.hi)>reference.upper(),(ours,reference)
enclosed(PI,arb.pi())
for _ in range(100):
    x=F(rng.randint(1,1000000),100000);y=I(x);ref=ar(x)
    enclosed(y.log(),ref.log());enclosed(y.exp(),ref.exp());enclosed(y.sqrt(),ref.sqrt())
    sin,cos=sincos(y);enclosed(sin,ref.sin());enclosed(cos,ref.cos())
json.dump({'basic_exact_rational_cases':count,'transcendental_cross_checks':500,'independent_reference':'python-flint Arb 384 bits','all_pass':True},open('results/kernel-audit.json','w'),indent=2)
print('kernel cross-check PASS',count)

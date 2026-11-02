"""Compare independently implemented elementary enclosures to Arb, locally."""
import sys,json,hashlib
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from verify_jung_rational import I,Q,minus_log,pi_interval,exp_positive,sin_interval
ctx.dps=100
def ab(x):return arb(str(x))
def contains(i,a):
 lo=ab(F(i.lo,Q));hi=ab(F(i.hi,Q));assert a>lo and a<hi,(i.bounds(),str(a))
checks=0
contains(pi_interval(),arb.pi());checks+=1
for f in [F(1,5),F(54,125),F(99,100),F(999,1000),1-F(1,10**12)]:contains(minus_log(f),-ab(f).log());checks+=1
for f in [F(1,10**12),F(1,1000),F(1,3),F(1),F(3),F(399,100)]:contains(sin_interval(f),ab(f).sin());checks+=1
for f in [F(1,10**12),F(1,10),F(1),F(6),F(15)]:contains(exp_positive(f),ab(f).exp());checks+=1
# Published and new G have different analytic inputs. Their exact checkers
# intentionally reject each other's formats rather than treating them alike.
out={'status':'PASS','checks':checks,'oracle':'Arb 100 decimal digits','candidate_checker_sha256':hashlib.sha256(Path(__file__).with_name('verify_jung_rational.py').read_bytes()).hexdigest()};Path(__file__).with_name('jung-arithmetic-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out)

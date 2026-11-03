"""Exact six-degree density formula, reconstructed by two native counters.

Fractional edges cross the character x -> parity(73 & x), so a five-tuple
has at most six such edges, including repeated part assignments. Seven exact
evaluations therefore determine its polynomial. This adds an explanatory
formula; the frozen full-matrix replays remain the normative bound checks.
"""
import pathlib,json,subprocess,fcntl,math,time
from fractions import Fraction as F
lock=open('receipts/snapshot_compute.lock','a');fcntl.flock(lock,fcntl.LOCK_EX);start=time.time();definition=json.load(open('certificates/c5_cayley256_definition.json'));H=int(definition['hard_red_mask_hex'],16);S=int(definition['fractional_mask_hex'],16);assert H&S==0;fractional=[x for x in range(256) if S>>x&1];assert len(fractional)==16 and all(bin(73&x).count('1')%2==1 for x in fractional);points=[]
for j in range(7):
 q=[6 if H>>x&1 else j if S>>x&1 else 0 for x in range(256)];matrix='256 6\n'+' '.join(['1']*256)+'\n'+'\n'.join(' '.join(str(q[x^y]) for y in range(256)) for x in range(256))+'\n';kernel='256 6\n'+' '.join(map(str,q))+'\n';answers=[]
 for binary,data in [('./check_wide',matrix),('./check_cayley_exact_r4',kernel)]:
  proc=subprocess.run([binary],input=data,text=True,capture_output=True,check=True);num,den,red,blue=map(int,proc.stdout.split());answers.append((F(num,den),red,blue))
 a,b=answers;assert a[0]==b[0] and a[1]==256*b[1] and a[2]==256*b[2];points.append((F(j,6),a[0]));print('EXACT_POINT',j,str(a[0]),flush=True)
# Lagrange interpolation in ordinary monomial coordinates.
coeff=[F(0)]*7
for i,(x,y) in enumerate(points):
 poly=[F(1)];den=F(1)
 for j,(xx,_) in enumerate(points):
  if i==j:continue
  nxt=[F(0)]*(len(poly)+1)
  for k,v in enumerate(poly):nxt[k]-=xx*v;nxt[k+1]+=v
  poly=nxt;den*=x-xx
 for k,v in enumerate(poly):coeff[k]+=y*v/den
def evaluate(x):return sum(v*x**k for k,v in enumerate(coeff))
for x,y in points:assert evaluate(x)==y
accepted=json.load(open('receipts/cayley256_fine_accepted.json'));chosen=F(2648,4041);assert evaluate(chosen)==F(accepted['density']);simple=json.load(open('receipts/cayley256_simple_accepted.json'));assert evaluate(F(19,29))==F(simple['density']);common=1
for c in coeff:common=common*c.denominator//math.gcd(common,c.denominator)
integers=[int(c*common) for c in coeff];report=dict(PASS=True,status='candidate and unrefereed',degree_bound=6,bipartite_character=73,coefficient_numerators=list(map(str,integers)),coefficient_denominator=str(common),points=[dict(p=str(x),density=str(y)) for x,y in points],two_exact_counters_agree_separately_red_blue=True,selected_density=accepted['density'],elapsed=time.time()-start);pathlib.Path('receipts/cayley_probability_polynomial.json').write_text(json.dumps(report,indent=2));print('EXACT_POLYNOMIAL',integers,'/',common,flush=True)

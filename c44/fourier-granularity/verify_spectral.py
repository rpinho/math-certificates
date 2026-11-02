"""Independent exact certificate verifier; standard library only.
No imports of any search program or numerical optimization library.
Checks normalized Krawtchouk duals against the elementary Fourier L1 lemma.
The universal lemma and compression argument are written in PROOF.md.
"""
import hashlib,json,math,os,pathlib,sys
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parent
def verify_one(c):
 d=c['degree'];n=c['variables']
 assert type(d)==int and 1<=d<=48 and type(n)==int and n>=d
 assert c['schema'] in ('c44-spectral-l1-dual-v1','c44-spectral-level-dual-v2','c44-spectral-lattice-dual-v3')
 lattice=c['schema']=='c44-spectral-lattice-dual-v3'
 free=None if lattice else [0] if c['schema']=='c44-spectral-l1-dual-v1' else c['free_levels']
 if not lattice:
  assert type(free)==list and free==sorted(set(free)) and free[0]==0
  assert all(type(j)==int and 0<=j<d for j in free)
 # Only two prescribed values are accepted; all other Boolean values are
 # bounded in [-1,1]. Endpoint assumptions are unnecessary in these duals.
 a={int(k):F(v) for k,v in c['alpha'].items()}
 assert len(a)==len(c['alpha']) and all(0<=k<=n for k in a)
 moments=[]
 for degree in range(d+1):
  val=F(0)
  for x,w in a.items():
   # Coefficient of t^degree in (1-t)^x (1+t)^(n-x), computed
   # by polynomial multiplication independently of the discovery evaluator.
   left=[(-1)**j*math.comb(x,j) for j in range(min(x,degree)+1)]
   right=[math.comb(n-x,j) for j in range(min(n-x,degree)+1)]
   kl=sum(v*right[degree-j] for j,v in enumerate(left) if 0<=degree-j<len(right))
   val+=w*F(kl,math.comb(n,degree))
  if not lattice and degree not in free:assert abs(val)<=1,(d,n,degree,val)
  moments.append(str(val))
 # L(p)=sum a_x g(x) >= a_0-a_1-sum_{x>=2}|a_x|.
 lower=a.get(0,F(0))-a.get(1,F(0))-sum(abs(w) for x,w in a.items() if x not in (0,1))
 # Granularity gives sum_{S!=empty}|fhat(S)| <= 2^(d-1)(1-a^2),
 # where a=fhat(empty). Complete the square for c_0*a-M*a^2.
 if lattice:
  penalty=F(0)
  for j,value in enumerate(moments):
   value=F(value);z=value//2
   penalty+=math.comb(n,j)*max(z*value-z*z,(z+1)*value-(z+1)**2)
  allowed=F(2**(d-1))+penalty/F(2**(d-1))
 else:
  allowed=F(2**(d-1))+sum(math.comb(n,j)*F(moments[j])**2 for j in free)/F(2**(d+1))
 assert lower>allowed,(d,n,lower,allowed)
 assert c['block_bound']==n-1
 return {'degree':d,'excluded_blocks':n,'B':n-1,'exact_L1_lower':str(lower),
         'allowed_functional_upper':str(allowed),'margin':str(lower-allowed),
         'dual_coefficients':moments,'parseval_levels':free}
def main():
 print('PID',os.getpid(),flush=True)
 p=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'spectral_certificate.json')
 data=p.read_bytes();spec=json.loads(data)
 assert spec['schema']=='c44-spectral-bounds-v1'
 results=[verify_one(c) for c in spec['certificates']]
 assert len({r['degree'] for r in results})==len(results)
 out={'status':'PASS rational dual checks; universal proof is prose, not formalized',
      'certificate_sha256':hashlib.sha256(data).hexdigest(),'results':results}
 (ROOT/'verification_spectral.json').write_text(json.dumps(out,indent=2)+'\n')
 print('PASS',[(r['degree'],r['B']) for r in results],flush=True)
if __name__=='__main__':main()

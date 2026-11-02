"""Exact controls for normalization, granularity, and certificate rejection.
Separate finite checks; not a formalization of the universal proof.
"""
import copy,itertools,json,math,os,pathlib
from fractions import Fraction as F
from verify_spectral import verify_one
R=pathlib.Path(__file__).resolve().parent
def run():
 counts=[]
 # Exhaust all sign truth tables up to four variables. The Walsh transform is
 # computed directly by finite sums, without either Krawtchouk implementation.
 for n in range(1,5):
  size=1<<n;total=0
  for truth in range(1<<size):
   vals=[1 if truth>>x&1 else -1 for x in range(size)]
   coeff=[F(sum(vals[x]*(-1 if (x&s).bit_count()%2 else 1) for x in range(size)),size) for s in range(size)]
   d=max((s.bit_count() for s,a in enumerate(coeff) if a),default=0)
   if d==0:continue
   delta=F(1,2**(d-1));a0=coeff[0];M=2**(d-1)
   assert all((a/delta).denominator==1 for a in coeff)
   assert sum(a*a for a in coeff)==1
   levels=[sum(a for s,a in enumerate(coeff) if s.bit_count()==j) for j in range(d+1)]
   assert sum(abs(a) for a in levels[1:])<=M*(1-a0*a0)
   # Direct slice values agree with the claimed normalized-character average.
   for k in range(n+1):
    direct=F(sum(vals[x] for x in range(size) if x.bit_count()==k),math.comb(n,k))
    reconstruction=F(0)
    for j,a in enumerate(levels):
     average=F(sum((-1 if (x&s).bit_count()%2 else 1) for s in range(size) if s.bit_count()==j for x in [((1<<k)-1)]),math.comb(n,j))
     reconstruction+=a*average
    assert direct==reconstruction
   total+=1
  counts.append({'variables':n,'nonconstant_sign_functions_checked':total})
 # A degree-two fully-sensitive three-variable example saturates (1).
 vals=[1 if x.bit_count() in (0,3) else -1 for x in range(8)]
 assert vals[0]==1 and all(vals[1<<i]==-1 for i in range(3))
 coeff=[F(sum(vals[x]*(-1 if (x&s).bit_count()%2 else 1) for x in range(8)),8) for s in range(8)]
 assert coeff[0]==-F(1,2) and sum(abs(a) for a in coeff[1:])==F(3,2)
 # Hand-checkable small dual from PROOF.md.
 small={'schema':'c44-spectral-l1-dual-v1','degree':4,'variables':10,'block_bound':9,
        'alpha':{'0':'265/32','1':'-55/2','2':'795/32','8':'15/32','10':'-3/32'}}
 c=verify_one(small)
 assert c['dual_coefficients']==['6','1','-1','-1','1'] and F(c['margin'])==F(5,4)
 # A lower degree gives a stronger granularity premise, and the shorter dual
 # can still be valid. This is a positive control, not a corruption to reject.
 lower_degree=copy.deepcopy(small);lower_degree['degree']=3
 assert F(verify_one(lower_degree)['margin'])>0
 # Exact lattice functional inequality from LATTICE_PROOF.md, including
 # negative c, breakpoints, and coefficients of both signs.
 for M in (1,2,4,8,16):
  for cvalue in ('-6','-11/4','-3/2','-1','0','1','5/2','4'):
   cvalue=F(cvalue);z=cvalue//2
   lattice_max=max(cvalue*z-z*z,cvalue*(z+1)-(z+1)**2)
   assert lattice_max>=0 and lattice_max<=cvalue*cvalue/4
   for integer in range(-M,M+1):
    coefficient=F(integer,M)
    assert cvalue*coefficient-M*coefficient**2<=lattice_max/M
 rejects=[]
 for name,change in [('zero_dual',lambda z:z.update(alpha={})),
                     ('wrong_block_claim',lambda z:z.update(block_bound=8)),
                     ('out_of_range_slice',lambda z:z['alpha'].update({'11':'1'})),
                     ('unsupported_degree',lambda z:z.update(degree=49)),
                     ('excessive_norm',lambda z:z['alpha'].update({'0':'1000'}))]:
  z=copy.deepcopy(small);change(z)
  try:verify_one(z)
  except (AssertionError,ValueError,KeyError,ZeroDivisionError):rejects.append(name)
  else:raise AssertionError('Corrupt certificate accepted: '+name)
 return {'status':'PASS exhaustive finite controls and five rejection controls',
         'exhaustive':counts,'small_dual':c,'rejected':rejects}
if __name__=='__main__':
 print('PID',os.getpid(),flush=True);out=run()
 (R/'verification_controls.json').write_text(json.dumps(out,indent=2)+'\n')
 print(out['status'],flush=True)

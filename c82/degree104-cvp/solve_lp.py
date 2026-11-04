"""Re-solve the public factor LP, save duals for subsequent structural search."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import sys,json,time
import numpy as np
from fractions import Fraction
from core import Lib,grid
from wlp import WLP
from flint import ctx
ctx.threads=1

def solve(state,N,out,thr=.004):
 start=time.time();st=json.load(open(state));den=st['denominator'];num=st['numerator'];t=grid(N)
 lib=Lib(den,num,t);lp=WLP(t,lib.LR,lib.LM,lib.dR,lib.LS,lib.dS,thr=thr)
 if 'mu' in st:mu=np.array(st['mu']);w=np.array(st['w'])
 else:
  D=sum((len(r['coeffs'])-1)*r['multiplicity'] for r in den)
  mu=np.array([r['multiplicity']/D for r in den]);w=np.array([float(Fraction(r['q_rational']))/D for r in num])
 value=lp.init(mu,w);mu,w=lp.weights();nu,price,lam=lp.duals()
 g=lp.g(mu,w);have=np.zeros(N,bool);have[lp.rows]=True
 missing_max=float(np.max(g[~have])) if np.any(~have) else None
 assert missing_max is None or missing_max<=1e-10,('unresolved omitted epigraph row',missing_max)
 rd=lib.LM-nu@lib.LR.T-lam*lib.dR
 rn=nu@lib.LS.T+price*lib.dS
 audit=dict(candidate_unrefereed=True,threshold=thr,epigraph_rows=len(lp.rows),
            max_omitted_g=missing_max,normalization_residual=float(lib.dR@mu-1),
            degree_ratio=float(lib.dS@w),dual_mass=float(nu.sum()),
            min_denominator_reduced_cost=float(min(rd)),
            max_active_denominator_abs_rc=float(max(abs(rd[mu>1e-12]))),
            min_numerator_reduced_cost=float(min(rn)),
            max_active_numerator_abs_rc=float(max(abs(rn[w>1e-12]))),
            min_nu=float(min(nu)),max_nu=float(max(nu)),uniform_mass=1/N)
 assert min(rd)>-1e-7 and min(rn)>-1e-7,audit
 json.dump(audit,open(out+'-lp-audit.json','w'),indent=2)
 outstate=dict(denominator=den,numerator=num,mu=list(mu),w=list(w),lp=value,N=N)
 json.dump(outstate,open(out+'.json','w'),indent=1)
 np.savez_compressed(out+'-dual.npz',t=t,nu=nu,price=price,lam=lam)
 print(json.dumps(dict(value=value,lambda_=lam,price=price,denominators=len(den),numerators=len(num),N=N,seconds=time.time()-start)),flush=True)
 return outstate

if __name__=='__main__':solve(sys.argv[1],int(sys.argv[2]),sys.argv[3])

"""Fresh joint LP with HiGHS basis reuse and full-grid row generation.

x_j = deg(R_j)*mu_j and y_i=deg(S_i)*w_i. Nonnegative epigraph
variables carry cost 1/N. Normalization sum x=1, numerator sum y<=1.
For each active grid atom: -log|R|/deg(R) x + log|S|/deg(S) y - u<=0.
Rows omitted initially are added whenever they could change the objective.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time
import highspy
import numpy as np
from scipy import sparse
from numerics import register,grid,transformed_points,roots,root_logs,mahler_T,certificate_weights,write_json

class JointLP:
    def __init__(self, cert, n=None):
        self.start=time.monotonic()
        self.den=list(cert['denominator']); self.num=list(cert['numerator'])
        self.n=n or cert.get('N',524288)
        self.t=grid(self.n); self.z=transformed_points(self.t)
        self.h=np.array([mahler_T(r['coeffs']) for r in self.den])
        # Stream complete-grid sums; all columns stay in the same master LP.
        self.deg=np.array([len(r['coeffs'])-1 for r in self.den+self.num],float)
        self.nd=len(self.den); self.nf=len(self.deg)
        if 'mu' in cert:
            self.weights=np.r_[cert['mu'],cert['w']]
        else:
            _,mu,w=certificate_weights(cert); self.weights=np.r_[mu,w]
        g=self.full_integrand(self.weights)
        # Positive atoms have u>0; retain a band around their boundaries as well.
        self.active=np.zeros(self.n,bool)
        self.idx=np.array([],dtype=np.int64)
        self.model=highspy.Highs()
        for k,v in [('threads',1),('output_flag',False),('solver','simplex'),
                    ('primal_feasibility_tolerance',1e-10),('dual_feasibility_tolerance',1e-10)]:
            self.model.setOptionValue(k,v)
        costs=np.r_[self.h/self.deg[:self.nd],np.zeros(len(self.num))]
        self.model.addCols(self.nf,costs,np.zeros(self.nf),np.full(self.nf,highspy.kHighsInf),0,
                           np.zeros(self.nf+1,dtype=np.int32),np.array([],np.int32),np.array([],float))
        norm=np.zeros((2,self.nf)); norm[0,:self.nd]=1; norm[1,self.nd:]=1
        self.add_matrix_rows(norm,np.array([1.,-highspy.kHighsInf]),np.array([1.,1.-1e-9]))
        first=np.flatnonzero(g>-1e-7)
        first=np.union1d(first,np.arange(0,self.n,max(1,self.n//2048)))
        self.add_atoms(first)

    def full_integrand(self,weights):
        g=np.zeros(self.n)
        for j,(r,w) in enumerate(zip(self.den+self.num,weights)):
            if w!=0:g+=(-w if j<self.nd else w)*root_logs(r['coeffs'],self.z)
        return g

    def add_matrix_rows(self,a,lo,hi):
        a=sparse.csr_matrix(a)
        self.model.addRows(len(lo),lo,hi,a.nnz,a.indptr.astype(np.int32),a.indices.astype(np.int32),a.data)

    def add_atoms(self,indices):
        indices=np.asarray(indices,dtype=np.int64)
        indices=indices[~self.active[indices]]
        if not len(indices):return
        prev=self.model.getNumCol(); m=len(indices)
        self.model.addCols(m,np.full(m,1/self.n),np.zeros(m),np.full(m,highspy.kHighsInf),0,
                           np.zeros(m+1,np.int32),np.array([],np.int32),np.array([],float))
        points=self.z[indices]
        rows=np.column_stack([root_logs(r['coeffs'],points) for r in self.den+self.num])/self.deg
        rows[:,:self.nd]*=-1
        data=sparse.hstack([sparse.csr_matrix(rows),
                            sparse.csr_matrix((m,prev-self.nf)), -sparse.eye(m)],format='csr')
        self.add_matrix_rows(data,np.full(m,-highspy.kHighsInf),np.zeros(m))
        self.active[indices]=True; self.idx=np.r_[self.idx,indices]

    def solve(self,prefix):
        history=[]
        for step in range(50):
            stamp=time.monotonic(); self.model.run()
            status=self.model.getModelStatus()
            if status!=highspy.HighsModelStatus.kOptimal:
                print(json.dumps({'event':'simplex_failure','status':str(status),'action':'clear basis and retry IPM'}),flush=True)
                self.model.clearSolver()
                self.model.setOptionValue('solver','ipm')
                self.model.run()
                status=self.model.getModelStatus()
                if status!=highspy.HighsModelStatus.kOptimal:
                    raise RuntimeError(str(status))
            sol=self.model.getSolution(); x=np.array(sol.col_value[:self.nf])
            weights=x/self.deg
            g=self.full_integrand(weights)
            missing=np.flatnonzero((~self.active)&(g>1e-11))
            history.append({'step':step,'active':len(self.idx),'missing':len(missing),
                            'lp':self.model.getObjectiveValue(),'seconds':time.monotonic()-stamp})
            print(json.dumps(history[-1]),flush=True)
            if not len(missing):break
            self.add_atoms(missing)
        else:raise RuntimeError('row generation did not converge')
        nu=np.zeros(self.n);nu[self.idx]=-np.array(sol.row_dual[2:])
        lam=float(sol.row_dual[0]); eta=-float(sol.row_dual[1])
        H=float(self.h@weights[:self.nd]); J=float(np.maximum(g,0).mean())
        support=nu!=0; points=self.z[support];mass=nu[support]
        den_rc=self.h-np.array([root_logs(r['coeffs'],points)@mass for r in self.den])-lam*self.deg[:self.nd]
        num_rc=np.array([root_logs(r['coeffs'],points)@mass for r in self.num])+eta*self.deg[self.nd:]
        audit={'H':H,'J':J,'objective':H+J,'highs_objective':self.model.getObjectiveValue(),
               'lambda':lam,'eta':eta,'dual_objective':lam-eta*(1-1e-9),
               'gap':H+J-(lam-eta*(1-1e-9)),'denominator_reduced_costs':den_rc.tolist(),
               'numerator_reduced_costs':num_rc.tolist(),'nu_min':float(nu.min()),
               'nu_max':float(nu.max()),'dual_support':int((nu>1e-18).sum()),
               'normalization':float(x[:self.nd].sum()),'numerator_degree':float(x[self.nd:].sum()),
               'history':history,'seconds':time.monotonic()-self.start}
        state={'denominator':self.den,'numerator':self.num,'mu':weights[:self.nd].tolist(),
               'w':weights[self.nd:].tolist(),'N':self.n,'lp':H+J}
        write_json(prefix+'.json',state);write_json(prefix+'-lp.json',audit)
        np.savez_compressed(prefix+'-dual.npz',t=self.t,nu=nu,lam=lam,eta=eta)
        assert abs(audit['gap'])<1e-8 and abs(audit['normalization']-1)<1e-8
        self.weights=weights
        return state,audit


def freeze(state,path):
    # Multiplicities at scale 10^12; numerator powers at dyadic scale 2^20.
    den=[]
    for r,mu in zip(state['denominator'],state['mu']):
        m=int(round(mu*10**12))
        if m>0:den.append({'name':r['name'],'coeffs':r['coeffs'],'multiplicity':m})
    D=sum((len(r['coeffs'])-1)*r['multiplicity'] for r in den)
    num=[]
    for r,w in zip(state['numerator'],state['w']):
        q=Fraction(int(round(w*D*2**20)),2**20)
        if q>0:
            text=str(q)
            if len(str(abs(q.numerator))) in [15,16]:
                text=f'{q.numerator*2}/{q.denominator*2}'
                with open('CERTIFICATE_ENCODING.md','a') as f:
                    f.write(f'\n{path}: {r["name"]}: {q} encoded as {text} (equal rational).\n')
            num.append({'name':r['name'],'coeffs':r['coeffs'],'q_rational':text})
    assert sum((len(r['coeffs'])-1)*Fraction(r['q_rational']) for r in num)<D
    cert={'description':'Candidate, unrefereed. Doche construction; Patankar PR280 weighted CVP method, Pinho PR301 residue/pricing method; our own c82r5/c82r6 search and helpers reused through c82r8 in c82r9. Separately written (same agent) interval verification required.',
          'numeric_unverified':state['lp'],'N':state['N'],'denominator':den,'numerator':num}
    write_json(path,cert)
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',default='candidate.json');p.add_argument('--prefix',default='runs/baseline')
    a=p.parse_args();register('joint_lp')
    state,audit=JointLP(json.loads(Path(a.input).read_text())).solve(a.prefix)
    print(json.dumps(audit),flush=True)
    freeze(state,a.prefix+'-certificate.json')

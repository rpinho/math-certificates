"""Exploratory color-symmetric SDP; exports expanded matrices for exact checking."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:
    os.environ[key]='1'
import sys,math,json,itertools
import numpy as np
from scipy import sparse
import cvxpy as cp
prefix=sys.argv[1];solver=sys.argv[2] if len(sys.argv)>2 else 'SCS_INDIRECT'
meta=[]
with open(prefix+'.meta') as f:
    hdr=list(map(int,next(f).split()));n=hdr[0];assert len(hdr)==1 or hdr[1]==0
    for line in f:
        t,m,typ,d,*keys=map(int,line.split());meta.append((t,m,typ,d,keys))
lookup={(t,m,key):(b,i) for b,(t,m,typ,d,keys) in enumerate(meta) for i,key in enumerate(keys)}
perms={}
def canon(code,t,m):
    s=t+m;rootmask=(1<<(t*(t-1)//2))-1
    if (t,m) not in perms:
        bits={(i,j):j*(j-1)//2+i for j in range(1,s) for i in range(j)}
        pp=[]
        for a in itertools.permutations(range(t)):
            for b in itertools.permutations(range(t,s)):
                p=a+b;pp.append([bits[tuple(sorted((p[i],p[j])))] for j in range(1,s) for i in range(j)])
        perms[t,m]=pp
    best=(code&rootmask,code)
    for p in perms[t,m]:
        h=sum(((code>>old)&1)<<new for new,old in enumerate(p))
        best=min(best,(h&rootmask,h))
    return best[1]
complement=[]
for b,(t,m,typ,d,keys) in enumerate(meta):
    top=(1<<((t+m)*(t+m-1)//2))-1
    images=[lookup[t,m,canon(top^key,t,m)] for key in keys]
    assert len(set(z for z,i in images))==1
    complement.append((images[0][0],np.array([i for z,i in images],dtype=int)))
for b,(c,p) in enumerate(complement):
    assert complement[c][0]==b
    assert np.array_equal(complement[c][1][p],np.arange(len(p)))

reps=[b for b,(c,p) in enumerate(complement) if b<=c]
rep_for={b:min(b,c) for b,(c,p) in enumerate(complement)}
starts={};nc=0;Q={};expr=[];constraints=[]
for b in reps:
    t,m,typ,d,keys=meta[b];starts[b]=nc;nc+=d*(d+1)//2
    q=cp.Variable((d,d),symmetric=True);Q[b]=q;constraints.append(q>>0)
    expr.append(q[np.triu_indices(d)]/(math.comb(n,t)*math.comb(n-t,m)))
def col(b,i,j):
    if i>j:i,j=j,i
    d=meta[b][3];return starts[b]+i*d-i*(i-1)//2+j-i
rows=[];cols=[];vals=[];oldcol=0
for b,(t,m,typ,d,keys) in enumerate(meta):
    c,p=complement[b];r=rep_for[b]
    for i in range(d):
        for j in range(i,d):
            if c==b:
                rows.extend([oldcol,oldcol]);cols.extend([col(r,i,j),col(r,int(p[i]),int(p[j]))]);vals.extend([.5,.5])
            else:
                rows.append(oldcol);cols.append(col(r,i,j) if b==r else col(r,int(p[i]),int(p[j])));vals.append(1.)
            oldcol+=1
P=sparse.coo_matrix((vals,(rows,cols)),shape=(oldcol,nc)).tocsr()
with open(prefix+'.coo') as f:
    nr,ncold=map(int,next(f).split());data=np.loadtxt(f,dtype=np.int32).T
assert ncold==oldcol
A=sparse.coo_matrix((data[2],(data[0],data[1])),shape=(nr,ncold)).tocsr()
C=(A@P).tocsr();C.sort_indices()
obj=np.loadtxt(prefix+'.objective');target=obj[:,0]/obj[:,1]
seen={};keep=[]
for i in range(nr):
    lo,hi=C.indptr[i:i+2];key=(C.indices[lo:hi].tobytes(),C.data[lo:hi].tobytes())
    if key not in seen:seen[key]=i;keep.append(i)
    else:assert target[seen[key]]==target[i]
C=C[keep];target=target[keep]
print('color reduction',nr,'->',len(keep),'rows',ncold,'->',nc,'variables','blocks',[meta[b][3] for b in reps],flush=True)
bound=cp.Variable();constraints.append(C@cp.hstack(expr)+bound<=target)
prob=cp.Problem(cp.Maximize(bound),constraints)
kwargs=dict(verbose=True)
if solver=='SCS_INDIRECT':kwargs.update(eps=1e-8,max_iters=30000,time_limit_secs=1200,use_indirect=True)
elif solver=='SCS':kwargs.update(eps=1e-8,max_iters=30000,time_limit_secs=1200)
else:kwargs.update(max_threads=1,tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9,time_limit=900,max_iter=150)
prob.solve(solver='SCS' if solver=='SCS_INDIRECT' else solver,**kwargs)
result=dict(status=prob.status,bound=float(bound.value) if bound.value is not None else None)
if all(q.value is not None for q in Q.values()):
    expanded=[]
    for b,(c,p) in enumerate(complement):
        r=rep_for[b];q=Q[r].value
        if c==b:q=(q+q[np.ix_(p,p)])/2
        elif b!=r:q=q[np.ix_(p,p)]
        expanded.append(q)
    np.savez_compressed(prefix+'_color_'+solver+'_Q.npz',**{f'q{i}':q for i,q in enumerate(expanded)})
    coeff=np.concatenate([[q[i,j]/(math.comb(n,t)*math.comb(n-t,m)) for i in range(d) for j in range(i,d)] for q,(t,m,typ,d,keys) in zip(expanded,meta)])
    result['min_residual']=float(np.min(obj[:,0]/obj[:,1]-A@coeff))
    result['min_eigenvalue']=min(float(np.linalg.eigvalsh(q)[0]) for q in expanded)
with open(prefix+'_color_'+solver+'_result.json','w') as f:json.dump(result,f,indent=2)
print('RESULT',result,flush=True)

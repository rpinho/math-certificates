"""Independent J011 audit. No claimant code is loaded.

Interpolation is derived using h=f-mu*||x||^2/2 and its (L-mu)-smooth
convex inequality. Positive definiteness is checked by exact LDL pivots.
Only the rational coefficient arrays are input from the claimant.
"""
import json, hashlib, sys, time
from flint import fmpq as Q, fmpq_mat as Mat

ROOT='.'

def zeros(n,m=None):
    return Mat(n, n if m is None else m)

def eye(n):
    a=zeros(n)
    for i in range(n): a[i,i]=1
    return a

def col(n,k):
    a=zeros(n,1)
    a[k,0]=1
    return a

def edgesum(n_oracles, weights, beta, mu, smooth):
    """Sum weighted interpolation quadratics, with optimizer last.

    Coordinates: two initial x's followed by queried gradients.
    From convex smooth h, 0 <= (L-mu)(fi-fj-gj*dy-mu/2*dy^2)
                                   -1/2*(dg-mu*dy)^2.
    """
    d=n_oracles+2
    xprev,x=col(d,0),col(d,1)
    ys=[]; gs=[]
    for k in range(n_oracles):
        y=(1+beta)*x-beta*xprev
        g=col(d,k+2)
        ys.append(y); gs.append(g)
        xprev,x=x,y-g
    ys.append(zeros(d,1)); gs.append(zeros(d,1))
    assert len(weights)==n_oracles*(n_oracles+1)
    A=zeros(d); a=[Q(0) for _ in range(n_oracles)]
    idx=0
    for i in range(n_oracles+1):
        for j in range(n_oracles+1):
            if i==j: continue
            w=weights[idx]; idx+=1
            assert w>=0, ('negative_multiplier',idx-1)
            if not w: continue
            dy=ys[i]-ys[j]; dg=gs[i]-gs[j]
            dh=dg-mu*dy
            sym=(gs[j]*dy.transpose()+dy*gs[j].transpose())/2
            A-=w*((smooth-mu)*(sym+mu*dy*dy.transpose()/2)+dh*dh.transpose()/2)
            if i<n_oracles:a[i]+=w*(smooth-mu)
            if j<n_oracles:a[j]-=w*(smooth-mu)
    return A,a

def ldlt(M,label):
    assert M==M.transpose(),label+' symmetry'
    A=Mat(M); pivots=[]
    for k in range(M.nrows()):
        pivot=A[k,k]
        assert pivot>0,(label,'nonpositive_LDL_pivot',k,str(pivot))
        pivots.append(pivot)
        for i in range(k+1,M.nrows()):
            for j in range(i,M.nrows()):
                a=A[i,j]-A[i,k]*A[j,k]/pivot
                A[i,j]=a; A[j,i]=a
    return {'dimension':M.nrows(),'positive_pivots':len(pivots),
            'min_pivot_approx':float(min(pivots)),
            'pivot_sha256':hashlib.sha256('\n'.join(map(str,pivots)).encode()).hexdigest()}

def check(path):
    data=json.load(open(path))
    assert (data['memory'],data['mu'],data['L'],data['alpha'],data['beta'],data['q'])==(32,'1/25','1','1','21/32','3599/5000')
    P=Mat([[Q(v) for v in row] for row in data['P']])
    p=[Q(v) for v in data['p']]
    lam=[Q(v) for v in data['lam']]
    eta=[Q(v) for v in data['eta']]
    b=Q(data['beta']); mu=Q(data['mu']); L=Q(data['L']); q=Q(data['q'])
    n=len(p); d=n+2
    assert (P.nrows(),P.ncols(),n)==(35,35,33)
    assert P==P.transpose()
    M,a=edgesum(n,lam,b,mu,L)
    V=P-M
    v=[p[i]-a[i] for i in range(n)]
    assert min(v)>0, 'potential_function_coefficients'
    print('positivity reconstructed',flush=True)
    M1,a1=edgesum(n+1,eta,b,mu,L)
    T=zeros(d,d+1)
    T[0,1]=1
    T[1,0]=-b; T[1,1]=1+b; T[1,2]=-1
    for i in range(2,d):T[i,i+1]=1
    U=zeros(d,d+1)
    for i in range(d):U[i,i]=1
    H=q*U.transpose()*P*U-T.transpose()*P*T-M1
    feq=[q*val for val in p]+[Q(0)]
    for i,val in enumerate(p):feq[i+1]-=val
    feq=[feq[i]-a1[i] for i in range(n+1)]
    assert all(val==0 for val in feq),'function_cancellation'
    print('decrease reconstructed and exact function cancellation passed',flush=True)
    res={'certificate_sha256':hashlib.sha256(open(path,'rb').read()).hexdigest(),
         'q':str(q),'q_old':str(Q(18,25)),'improvement':str(Q(18,25)-q),
         'V':ldlt(V,'V'),'H':ldlt(H,'H'),
         'function_coefficients_strictly_positive':True,'function_equalities_exact':True,
         'multipliers_nonnegative':True,'min_function_coefficient_approx':float(min(v))}
    c=Q(1,1000000)
    while True:
        try: res['V_minus_cI']=ldlt(V-c*eye(d),'V-cI'); break
        except AssertionError:c/=10
    res['coercivity_c']=str(c)
    # An independently chosen initial growth bound: ||x_{k+1}|| <= ||y_k||
    # since gradient step at 1/L is nonexpansive and fixes the optimizer.
    # Using the weaker triangle bound 2||y_k|| requires no extra theorem.
    aprev=acur=Q(1); bounds=[]
    for i in range(n):
        yi=(1+b)*acur+b*aprev
        bounds.append(yi)
        aprev,acur=acur,2*yi
    B=[Q(1),Q(1)]+bounds
    C=sum(abs(P[i,j])*B[i]*B[j] for i in range(d) for j in range(d))
    C+=sum(max(Q(0),p[i])*bounds[i]**2/2 for i in range(n))
    res.update(initial_C=str(C),uniform_K=str(C/c),uniform_K_approx=float(C/c))
    assert q<Q(18,25)
    # Scalar quadratic endpoint, derived directly from the recurrence.
    r1,r2=Q(21,25),Q(3,4)
    assert r1+r2==(1-mu)*(1+b) and r1*r2==(1-mu)*b
    res['quadratic_endpoint_roots']=[str(r1),str(r2)]
    res['quadratic_necessary_q']=str(r1*r1)
    res['verified']=True
    return res

if __name__=='__main__':
    start=time.monotonic()
    out=check(sys.argv[1] if len(sys.argv)>1 else 'certificate.json')
    out['elapsed_seconds']=time.monotonic()-start
    json.dump(out,open('independent_result.json','w'),indent=2)
    print(json.dumps(out,indent=2),flush=True)

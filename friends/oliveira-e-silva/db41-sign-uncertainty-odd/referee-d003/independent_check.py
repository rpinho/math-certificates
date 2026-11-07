#!/usr/bin/env python3
"""Independent finite cyclic sign-uncertainty referee, from paper (3.1)/Problem 3.1.

No search/claimant verifier imports; only JSON seed DATA is shared.
All mathematical work is to be run on the shared pod, never locally.
Cosines are direct arb cos_pi evaluations at rational arguments, not an FFT.
"""
import argparse, hashlib, json, math, os, time
from fractions import Fraction
from pathlib import Path
from flint import arb, arb_mat, ctx, fmpq

def rat(v):
    f = Fraction(v)
    return arb(fmpq(f.numerator, f.denominator))

def write_receipt(path, result):
    result['utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    result['precision_bits'] = ctx.prec
    result['verifier_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(path).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)

def cosine_table(N):
    # Even cosines reduce every residue to 0..q, no floating point indices.
    return [arb(fmpq(2*r, N)).cos_pi() for r in range(N//2+1)]

def lower(seed_path, out, k_override=None, zero=False, negate=False):
    started=time.monotonic()
    raw=Path(seed_path).read_bytes(); d=json.loads(raw)
    q=d['q']; N=2*q+1; K=d['k'] if k_override is None else k_override
    assert d['N']==N and d['s']==-1 and 1<=K<=q
    assert len(d['seed'])==q+1
    h=[rat(s) for s in d['seed']]
    if zero: h=[arb(0) for _ in h]
    if negate: h=[-v for v in h]
    cosine=cosine_table(N); root=arb(N).sqrt()
    def cosij(i,j):
        r=(i*j)%N
        return cosine[min(r,N-r)]
    support=[j for j in range(1,q+1) if not h[j].is_zero()]
    def Dh(n):
        return (h[0]+sum((2*h[j]*cosij(n,j) for j in support),arb(0)))/root
    # B is restriction of I+D to inner positive coordinates. All h are exact rationals.
    # The exact x=B^{-1}(h+Dh)_inner defines r=h-E*x and g=r+D*r.
    # Thus g_inner=0 exactly, Dg=g exactly by D^2=I. Floating residuals do not establish zeros.
    ids=list(range(1,K))
    B=arb_mat([[arb(int(i==j))+2*cosij(i,j)/root for j in ids] for i in ids])
    rhs=arb_mat([[h[i]+Dh(i)] for i in ids])
    determinant=B.det()
    if determinant.contains(0):
        raise RuntimeError('Could not certify unique exact correction')
    x=B.solve(rhs, algorithm='lu')
    r=list(h)
    for i in ids: r[i]=r[i]-x[i-1,0]
    rsupport=[j for j in range(1,q+1) if not r[j].is_zero()]
    def g(n):
        return r[n]+(r[0]+sum((2*r[j]*cosij(n,j) for j in rsupport),arb(0)))/root
    g0=g(0); gq=g(q)
    minimum=None; min_index=None; bad=[]
    # For signs, interval comparisons are strict: no tolerance and no clipping to zero.
    # Equality is only used at coordinates eliminated by the exact linear system.
    for n in range(K,q+1):
        value=g(n)
        if not value>=0: bad.append({'n':n,'enclosure':str(value)})
        low=value.lower()
        if minimum is None or low<minimum: minimum=low; min_index=n
    ok=(g0>=0 and gq>0 and not bad)
    # A separate direct consistency check is diagnostic only.
    inner_contain_zero=all(g(i).contains(0) for i in ids)
    assert inner_contain_zero, 'DFT correction algebra is inconsistent'
    result={'mode':'lower','passed':bool(ok),'q':q,'N':N,'excluded_k':K,
            'seed_sha256':hashlib.sha256(raw).hexdigest(),'seed_support':len(support),
            'zero_control':zero,'negative_control':negate,
            'g_scaling':'g = r + D r (twice claimant projection)',
            'determinant':str(determinant),'g0':str(g0),'gq':str(gq),
            'tail_min_lower':str(minimum),'tail_min_index':min_index,
            'bad_tail_count':len(bad),'bad_tail_first':bad[:4],
            'inner_consistency':inner_contain_zero,'seconds':time.monotonic()-started}
    write_receipt(out,result)
    return ok

def upper(q,L,out):
    started=time.monotonic(); N=2*q+1
    assert 3<=L<=q and N<=L*L
    # Construct w_j=sin(2*pi*j/L), 1<=j<L; w_0=w_L=0, otherwise zero.
    # Pair j,L-j proves sum w=0 exactly, so v=w-Dw has v0=0, Dv=-v.
    # Direct cosine sum checks every tail n>=L; there v=-Dw.
    cosine=cosine_table(N); root=arb(N).sqrt()
    w=[arb(fmpq(2*j,L)).sin_pi() for j in range(1,L)]
    def Dw(n):
        terms=[]
        for j,wj in enumerate(w,1):
            rr=(n*j)%N
            terms.append(wj*cosine[min(rr,N-rr)])
        return 2*sum(terms,arb(0))/root
    zeros=[]; bad=[]; tail_min=None; min_index=None; endpoint=None
    for n in range(L,q+1):
        value=-Dw(n)
        if (L*n)%N==0:
            # n/N=m/L with integer m. Product-to-sum reduces the DFT to
            # sums of integer-frequency sines over a complete L-cycle, exactly zero.
            assert value.contains(0)
            zeros.append(n)
            if n==q: endpoint=arb(0)
        else:
            if not value>0: bad.append({'n':n,'enclosure':str(value)})
            if tail_min is None or value.lower()<tail_min:
                tail_min=value.lower(); min_index=n
            if n==q: endpoint=value
    ok=(not bad and endpoint is not None and endpoint>0)
    # v/v(q) is an exact scaling to both required endpoints = 1;
    # use factor 2/v(q) to leave a strict margin after normalization.
    factor=2/endpoint if endpoint is not None and endpoint>0 else None
    result={'mode':'upper','passed':bool(ok),'q':q,'N':N,'feasible_k':L,
            'origin':'exact zero by sine pairing','endpoint':str(endpoint),
            'normalizing_factor':str(factor),'normalized_both_endpoints':'exactly 2',
            'tail_min_positive_lower':str(tail_min),'tail_min_index':min_index,
            'exact_tail_zeros':zeros,'bad_tail_count':len(bad),'bad_tail_first':bad[:4],
            'evaluated_tail_coordinates':q-L+1,'seconds':time.monotonic()-started}
    write_receipt(out,result)
    return ok

def small_lp(out):
    # Direct unreduced Problem 3.1 constraints; f and Df treated separately,
    # rather than assuming an eigenvector or setting f(0)=0.
    import numpy as np
    from scipy.optimize import linprog
    q=5; N=11
    D=np.cos(2*np.pi*np.arange(q+1)[:,None]*np.arange(q+1)[None,:]/N)
    D[:,0]/=math.sqrt(N);D[:,1:]*=2/math.sqrt(N)
    E=np.eye(q+1); rows=[]
    for k in [2,3,4,5]:
        A=np.vstack([-E[0], D[0], -E[q], D[q], -E[k:],D[k:]])
        b=np.r_[0,0,-1,-1,np.zeros(2*(q-k+1))]
        res=linprog(np.zeros(q+1), A_ub=A,b_ub=b,bounds=[(None,None)]*(q+1),method='highs')
        rows.append({'k':k,'status':res.status,'success':res.success,
                     'message':res.message,'f':res.x.tolist() if res.success else None})
    assert [r['success'] for r in rows]==[False,False,True,True]
    # Verify D^2=I and weighted self-adjointness at this diagnostic precision.
    weights=np.diag([1]+[2]*q)
    result={'mode':'small_lp','q':5,'rows':rows,
            'D2_error':float(np.max(np.abs(D@D-E))),
            'weighted_adjoint_error':float(np.max(np.abs(weights@D-D.T@weights))),
            'status':'floating diagnostic; exact lower/upper checks are separate'}
    write_receipt(out,result)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bits',type=int,default=320)
    s=p.add_subparsers(dest='mode',required=True)
    a=s.add_parser('lower');a.add_argument('seed');a.add_argument('out');a.add_argument('--k',type=int)
    a.add_argument('--zero',action='store_true');a.add_argument('--negate',action='store_true')
    a=s.add_parser('upper');a.add_argument('q',type=int);a.add_argument('L',type=int);a.add_argument('out')
    a=s.add_parser('lp');a.add_argument('out')
    args=p.parse_args();ctx.prec=args.bits;ctx.threads=1
    if args.mode=='lower': good=lower(args.seed,args.out,args.k,args.zero,args.negate)
    elif args.mode=='upper': good=upper(args.q,args.L,args.out)
    else: small_lp(args.out);good=True
    if not good: raise SystemExit(2)

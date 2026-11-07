"""Exact rational-polynomial DFT in Q[z]/Phi_(ell^2). Pod only."""
import json,time
from flint import fmpq_poly
from sympy import symbols, cyclotomic_poly, Poly


def one(ell):
    N=ell*ell
    x=symbols('x')
    p=Poly(cyclotomic_poly(N,x),x)
    mod=fmpq_poly([int(p.nth(j)) for j in range(p.degree()+1)])
    E=[]
    for j in range(N):
        E.append(fmpq_poly([0]*j+[1]) % mod)
    z=E[1]
    def cos2(k): return E[k%N]+E[-k%N]
    G,H,seed=[],[],[]
    a=ell*(ell+1)//2
    q=(N-1)//2
    for n in range(N):
        r,m=n%ell,n//ell
        R=int(r==1)-int(r==ell-1)
        # Scale G by 2(z+1); tan(theta/2)*sin(n theta) is rational in z.
        g=(4+2*cos2(n))*(z+1)*int(r==0)
        g+=(2-cos2(n))*(z+1)*int(r in (1,ell-1))
        g+=(z-1)*(E[n]-E[-n%N])*R
        G.append(g%mod)
        # Scale H by 2. Since ell is odd, exp(pi*i/ell)=-z^a.
        H.append((-cos2(a)+cos2(a*(2*m+1)))%mod if r else fmpq_poly())
        j=min(n,N-n)
        seed.append((E[ell*j%N]-E[-ell*j%N]) if j<=ell else fmpq_poly())
    def D(v):
        nz=[(j,y) for j,y in enumerate(v) if not y.is_zero()]
        return [(sum((y*E[-k*j%N] for j,y in nz),fmpq_poly())/ell)%mod
                for k in range(N)]
    DG,DH=D(G),D(H)
    for n in range(N):
        assert DG[n]==G[n]
        if n%ell not in (0,1,ell-1): assert DH[n].is_zero()
        assert G[n].is_zero()==(n%ell not in (0,1,ell-1) or n in (1,N-1))
        assert H[n].is_zero()==(n%ell==0 or n//ell in (0,ell-1))
    ds=D(seed)
    f=[(u-v)%mod for u,v in zip(seed,ds)]
    df=D(f)
    assert f[0].is_zero() and not f[q].is_zero()
    assert all((u+v).is_zero() for u,v in zip(f,df))
    assert all(f[n].is_zero() for n in range(ell,N,ell))
    # A non-periodically-even input is also checked: D^2 reverses it.
    v=[fmpq_poly([int(n==1)]) for n in range(N)]
    ddv=D(D(v))
    assert all(ddv[n]==v[-n%N] for n in range(N))
    return dict(ell=ell,N=N,field_degree=mod.degree(),
                G_self_dual=True,H_Fourier_support=True,zero_masks_exact=True,
                sine_minus_eigen=True,DFT_square_is_reversal=True)


if __name__=='__main__':
    start=time.monotonic();out=[]
    for ell in (3,5,7,9,11,15):
        row=one(ell);out.append(row);print(json.dumps(row),flush=True)
        json.dump(dict(rows=out,seconds=time.monotonic()-start),open('cyclotomic.json','w'),indent=2)
    print('ALL EXACT PASS',time.monotonic()-start,flush=True)

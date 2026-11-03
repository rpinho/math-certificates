"""Exact candidate GF arithmetic verifier, separately written (same agent).

Reads frozen rational data. The combinatorial proof is FIRST_MOMENT_PROOF.md.
No floating-point search result is trusted by this verifier.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from flint import ctx
from verify_mean_two_leaf import verify as verify_mean
from verify_baseline import ball, functions, Dual


def verify(path):
    c=json.loads(Path(path).read_text())
    assert c['bar_sha256']==hashlib.sha256(Path('BAR.json').read_bytes()).hexdigest()
    mc=json.loads(Path('artifacts/mean_two_leaf_certificate.json').read_text())
    assert c['mean_certificate_sha256']==hashlib.sha256(Path('artifacts/mean_two_leaf_certificate.json').read_bytes()).hexdigest()
    mr=verify_mean(mc)
    alpha,beta,cap,aup,ain,binp=map(F,[c[k] for k in ['alpha','beta','two_leaf_cap','leaf_upper_input','leaf_lower_input','empty_lower_input']])
    assert 0<alpha<ain<F(5,9)<aup<1
    assert 0<beta<binp<F(5,27)
    assert F(mc['markov_threshold'])+2*(aup-alpha)<cap
    f={0:beta,1:(3-4*alpha-3*beta-cap)/2,2:cap,3:(2*alpha+beta-1-cap)/2}
    assert all(x>0 for x in f.values())
    assert c['profile']=={str(j):str(x) for j,x in f.items()}
    assert sum(f.values())==1-alpha
    assert sum(j*x for j,x in f.items())==alpha
    z,k,q0,q1,q2,lam=map(F,[c[t] for t in ['z','kappa','q0','q1','q2','lambda']])
    assert lam>=F(521,50) and z*lam<=1
    assert 0<z<F(1,4) and k>0 and 0<q1<q0<q2
    Z,K=ball(z),ball(k)
    s=(1-4*Z).sqrt();Q=(1-s)/2
    assert ball(q2)*Q<1
    def B(q):
        h=functions(Z,q)
        h[1]=h[0]+Dual(Z)*Dual(q,1)*h[0]**2/s
        assert all(x.x>0 for x in h.values())
        val=-K*q.log()+sum(ball(f[j])*h[j].x.log() for j in f)
        slope=-K+sum(ball(f[j])*q*h[j].d/h[j].x for j in f)
        return val,slope
    b1,d1=B(ball(q1));b2,d2=B(ball(q2))
    assert d1<0 and d2>0
    b,d=B(ball(q0))
    rad=abs((ball(q1)/ball(q0)).log())+abs((ball(q2)/ball(q0)).log())
    lower=b-abs(d)*rad
    phi=2*(27*Z/4).log()+2*lower-K*Q.log()
    assert phi>0, 'nonpositive target exponent'
    return {'status':'PASS','claim':'candidate and unrefereed: C30 >= 521/50','verifier':'separately written (same agent)','lambda':str(lam),'z':str(z),'Phi_lower_ball':str(phi),'tangent_slope_ball':str(d),'bracket_slopes_w':[str(d1),str(d2)],'two_leaf_first_moment_ball':mr['two_leaf_density'],'root_and_rouche_verified':True,'profile':{str(j):str(x) for j,x in f.items()},'precision_bits':ctx.prec,'proof_dependency':'FIRST_MOMENT_PROOF.md, plus published BBEP inputs and v3 Harris argument'}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('certificate');args=p.parse_args()
    out=verify(args.certificate)
    Path('artifacts/candidate_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

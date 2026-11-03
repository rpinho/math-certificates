"""Arb dual upper bound on the established-profile exponent at the target.

This is a rejection certificate for one reduced proof method, not an upper
bound on C30. No claim about other profiles or other methods is made.
"""
from fractions import Fraction as F
import copy
import hashlib
import json
from pathlib import Path
from flint import arb,ctx


def rational(q):
    x=F(q)
    return arb(x.numerator)/x.denominator


def verify(c):
    assert c['bar_sha256']==hashlib.sha256(Path('BAR.json').read_bytes()).hexdigest()
    assert F(c['lambda'])==F(521,50) and F(c['z'])*F(c['lambda'])==1
    assert c['profile']=={'0':'5/27','2':'2/9','3':'1/27'}
    ctx.prec=256
    z=rational(c['z'])
    Q=(1-(1-4*z).sqrt())/2
    q=1/Q.sqrt()
    # Truncated Taylor series in z, reconstructed from the definition Omega_j.
    # This avoids the verifier's displayed-polynomial implementation.
    N=3
    s0=(1-4*z).sqrt()
    s=[s0]
    for k in range(1,N+1):s.append(s[-1]*(arb(1)/2-(k-1))/k*(-4)/(1-4*z))
    d=[q*x for x in s];d[0]+=2-q
    r=[1/d[0]]
    for k in range(1,N+1):r.append(-sum(d[i]*r[k-i] for i in range(1,k+1))/d[0])
    from math import comb
    H={j:sum(2*comb(j,i)*z**i*r[i] for i in range(j+1)) for j in [0,2,3]}
    score=2*((27*z/4).log()+sum(rational(c['profile'][str(j)])*H[j].log() for j in H))
    assert score<0, 'the proposed obstruction is not negative'
    return {'status':'PASS','kind':'reduced-model obstruction only; no C30 upper bound','upper_bound_on_exponent_for_every_kappa_at_target':str(score),'q_dual_ball':str(q),'verifier':'separately written (same agent)'}


if __name__=='__main__':
    c=json.loads(Path('artifacts/reduced_obstruction.json').read_text())
    out=verify(c)
    bad=copy.deepcopy(c);bad['profile']['2']='0'
    try:verify(bad)
    except AssertionError:out['corrupted_profile_rejected']=True
    else:raise RuntimeError('corruption accepted')
    Path('artifacts/reduced_obstruction_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

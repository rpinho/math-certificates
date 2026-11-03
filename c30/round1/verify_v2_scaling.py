"""Integer/rational verifier of a printed v2 inequality failure.

The source's appendix code uses a repaired normalization. This counterexample
does NOT disprove its headline bound or identify the author's withdrawal cause.
"""
from fractions import Fraction as F
import copy
import hashlib
import json
from pathlib import Path


def verify(c):
    # Source snapshots are omitted; this checks provenance linkage, not source bytes.
    bar=json.loads(Path('BAR.json').read_text())
    assert c['source_sha256']==bar['source_sha256']['sources/norton-v2.html']
    z=F(c['z']);u=F(c['u']);v=F(c['v']);lam=F(c['rouche_lambda'])
    assert (z,u,v,lam)==(F(4,27),F(1,2),F(0),F(16))
    vmax=z*(1+lam*z)
    assert vmax<F(1,2)
    assert abs(v-z)<=lam*z*z
    A=F(27,16)
    # F0(u)=v1/[z(1+v1)], v1=1/4 solves the smaller kernel root.
    root=F(1,4)
    B=1-z-z*(1+u)
    assert z*root*root-B*root+z==0
    assert root*root<1  # product of the two roots is 1
    FF=root/(z*(1+root))
    assert FF==F(27,20)
    actual=z*z*(A+FF-z*A*FF)/((1-z*A)*(1-z*FF))
    assert actual==F(c['actual_R'])
    # At u=1 and v=1/2, F=108/(23+3 sqrt(161)) < 2.
    # Squaring the positive sides verifies the necessary sqrt inequality.
    assert F(161)>F(31,3)**2
    # Nonnegative coefficients: C_A <= A(rho,omega0)=9/4 and C_F < 2.
    CA,CF=F(9,4),F(2)
    cr_upper=z*z*(CA+CF-z*CA*CF)/((1-z*CA)*(1-z*CF))
    assert cr_upper==F(c['printed_CR_upper']) and cr_upper<1
    assert (1+lam*z)*(3+z*(1+lam*z)+cr_upper*z)<lam
    purported_upper=cr_upper*z*z
    assert actual>purported_upper
    return {'status':'PASS','verifier':'separately written (same agent)','actual_R':str(actual),'upper_on_printed_CR':str(cr_upper),'upper_on_printed_CR_times_z_squared':str(purported_upper),'strict_violation':str(actual-purported_upper),'scope':'printed Lemma 5.11 normalization only; appendix code removes the extra rho^2'}


if __name__=='__main__':
    path=Path('artifacts/v2_scaling_counterexample.json')
    c=json.loads(path.read_text())
    out=verify(c)
    bad=copy.deepcopy(c);bad['actual_R']='1/100'
    try:verify(bad)
    except AssertionError:out['corrupted_certificate_rejected']=True
    else:raise RuntimeError('corruption accepted')
    Path('artifacts/v2_scaling_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

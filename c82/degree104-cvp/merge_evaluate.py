"""Reprice candidate denominator columns jointly, and freeze exact weights.

Search/LP output remains UNVERIFIED until the separate interval checker passes.
"""
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import time

from solve_lp import solve


def freeze(state, path):
    scale=10**12
    den=[]
    for rec,mu in zip(state['denominator'],state['mu']):
        m=int(round(mu*scale))
        if m>0:
            den.append(dict(name=rec['name'],coeffs=rec['coeffs'],multiplicity=m))
    D=sum((len(r['coeffs'])-1)*r['multiplicity'] for r in den)
    num=[]
    for rec,w in zip(state['numerator'],state['w']):
        q=Fraction(round(w*scale*2**20),2**20)
        if q>0:
            num.append(dict(name=rec['name'],coeffs=rec['coeffs'],q_rational=str(q)))
    A=sum((len(r['coeffs'])-1)*Fraction(r['q_rational']) for r in num)
    assert A<D
    cert=dict(description='Candidate, unrefereed. Doche construction; public warm start '
              'and weighted-evaluation Schnorr--Euchner CVP method credited to '
              'vidigoat PR280 at 3a7a84f; reduced-cost/residue method and LP inherited '
              'from Pinho PR301. Search values UNVERIFIED without separate replay.',
              numeric_unverified=state['lp'],N=state['N'],denominator=den,numerator=num)
    raw=(json.dumps(cert,indent=1)+'\n').encode()
    Path(path).write_bytes(raw)
    return dict(certificate_sha256=hashlib.sha256(raw).hexdigest(),D=D,
                degree_A=str(A),degree_ratio=float(A/D),denominators=len(den),
                numerators=len(num))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('files',nargs='+')
    ap.add_argument('--baseline',default='runs/baseline.json')
    ap.add_argument('--prefix',default='runs/round1')
    ap.add_argument('--grid',type=int,default=524288)
    ap.add_argument('--threshold',type=float,default=1e-5)
    a=ap.parse_args()
    start=time.monotonic()
    baseline=json.loads(Path(a.baseline).read_text())
    st=json.loads(Path(a.baseline).read_text())
    known={tuple(r['coeffs']) for r in st['denominator']}
    added=[]
    for path in a.files:
        result=json.loads(Path(path).read_text())
        for rec in result['negative_candidates']:
            for factor in rec['factors']:
                cs=tuple(factor['coeffs'])
                if cs in known or cs[0]!=1:
                    continue
                known.add(cs)
                name='C82r3_'+hashlib.sha256(json.dumps(list(cs)).encode()).hexdigest()[:12]
                st['denominator'].append(dict(name=name,coeffs=list(cs)))
                st['mu'].append(0.)
                added.append(dict(name=name,degree=len(cs)-1,parent_rc=rec['rc'],
                                  public_bank=rec.get('public_bank',False),source=path))
    Path(a.prefix+'-input.json').write_text(json.dumps(st,indent=1)+'\n')
    out=solve(a.prefix+'-input.json',a.grid,a.prefix,thr=a.threshold)
    audit=freeze(out,a.prefix+'-certificate.json')
    audit.update(candidate_unrefereed=True,pid=os.getpid(),added=added,
                 numeric_unverified=out['lp'],baseline_grid_value=baseline['lp'],
                 numeric_gain=baseline['lp']-out['lp'],seconds=time.monotonic()-start)
    Path(a.prefix+'-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps(audit,indent=2),flush=True)


if __name__=='__main__':
    main()

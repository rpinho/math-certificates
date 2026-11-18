"""Derive explicit finite truncation/smearing parameters from a verified packet.
This is a constructive corollary of PROOF.md, not another geometry verifier.
"""
import argparse,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('artifact');ap.add_argument('verification');ap.add_argument('out');ap.add_argument('--claim',default='1703/1000');a=ap.parse_args()
raw=Path(a.artifact).read_bytes();cert=json.loads(raw);v=json.load(open(a.verification));target=F(a.claim)
assert v['result']=='PASS' and hashlib.sha256(raw).hexdigest()==v['artifact_sha256']
q=F(v['ratio']);assert q>target
px,py,lam=map(F,[cert['measure']['Px'],cert['measure']['Py'],cert['measure']['lam']]);R=max(F(w['radius']) for w in cert['witnesses']);s=F(v['min_strict_mass_slack']);assert s>0
k=1+R//min(px,py);N=max(2*k+1,1+math.ceil(4*k*q/(q-target)))
eps=min(F(1,2),s/(16*lam*(2*R+1)));finite=q*F((N-2*k)**2,N*N)
assert k*min(px,py)>R and eps>0 and 4*lam*(2*R+1)*eps<s and finite>target
result={'status':'candidate, unrefereed','artifact_sha256':v['artifact_sha256'],'claim':str(target),'boundary_cells':k,'block_side_cells':N,'smear_radius':str(eps),'maximum_witness_radius':str(R),'finite_function_L1_norm':str(N*N*F(v['mass'])),'finite_atom_count':N*N*len(cert['measure']['pts']),'finite_ratio_lower_bound':str(finite),'finite_ratio_float':float(finite),'proof':'For each witness, smearing adds at most 4*lambda*(2*Rmax+1)*eps < minimum strict mass slack to its required mass. Inner cells are retained. The finite ratio is q*((N-2k)/N)^2 > claim.'}
Path(a.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

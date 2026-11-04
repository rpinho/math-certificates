"""Exact margin-to-ropelength corollary; separately written (same agent).

This arithmetic component requires the geometry/margin checks in verify_all.
It imports no discovery code.
"""
import pathlib,json,hashlib,sys
from fractions import Fraction as F
from verify import Reject,need,frac
def check(folder,certificate=None):
 P=pathlib.Path(folder);raw=(P/'CONSTRUCTION.json').read_bytes();D=json.loads(raw);m=json.loads((P/'margin.json').read_text());f=json.loads((P/'finite_witness.json').read_text());d=certificate if certificate is not None else json.loads((P/'ROP_BOUND.json').read_text())
 need(set(d)=={'kind','status','artifact_sha256','physical_coefficient','thickness_lower','exact_limit_upper','exact_additive_upper','claimed_upper','finite_ratio_upper','bar'},'E_ROP_SCHEMA')
 need(d['kind']=='ropelength_margin_corollary_v1','E_ROP_KIND');need(d['status']=='candidate and unrefereed','E_ROP_STATUS');need(d['artifact_sha256']==hashlib.sha256(raw).hexdigest(),'E_ROP_HASH')
 need(frac(d['bar'])==F(36,5),'E_ROP_BAR');need(m['artifact_sha256']==d['artifact_sha256'] and f['artifact_sha256']==d['artifact_sha256'],'E_ROP_PREREQUISITE_BINDING')
 c=frac(D['claim']['coefficient']);A=frac(D['claim']['additive']);t=frac(m['original_thickness_lower'])
 need(t>0 and t*frac(m['scale_down'])==1,'E_ROP_MARGIN_BINDING');need(frac(d['physical_coefficient'])==c,'E_ROP_PHYSICAL_BINDING');need(frac(d['thickness_lower'])==t,'E_ROP_THICKNESS_BINDING')
 limit=c/t;add=A/t;finite=frac(f['ratio_upper_exact'])/t
 need(frac(d['exact_limit_upper'])==limit,'E_ROP_LIMIT');need(frac(d['exact_additive_upper'])==add,'E_ROP_ADDITIVE');claim=frac(d['claimed_upper']);need(claim<=F(36,5),'E_ROP_BAR');need(limit<claim,'E_ROP_CLAIM')
 need(frac(d['finite_ratio_upper'])==finite and finite<F(36,5),'E_ROP_FINITE')
 return {'verdict':'EXACT_ROPELENGTH_MARGIN_COROLLARY_PASS_CANDIDATE_UNREFEREED','verifier':'separately written (same agent)','upper_exact':str(claim),'upper_display_only':float(claim),'exact_limit_upper':str(limit),'exact_ropelength_additive_upper':str(add),'finite_ratio_upper_exact':str(finite),'qualification':'arithmetic corollary; verify_all also verifies the complete closed-family geometry, topology, speed, margin and finite inputs'}
if __name__=='__main__':
 try:print(json.dumps(check(sys.argv[1]),indent=2))
 except Reject as e:print(str(e));sys.exit(1)

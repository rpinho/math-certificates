"""Same-agent scaling audit using the separately written geometry verifier."""
import pathlib,json,gzip,hashlib,copy,sys
from fractions import Fraction as F
from verify import check_bundle,Reject,need

def check(folder,certificate=None):
 P=pathlib.Path(folder);raw=(P/'CONSTRUCTION.json').read_bytes();d=certificate if certificate is not None else json.loads((P/'margin.json').read_text())
 need(set(d)=={'kind','artifact_sha256','scale_down','original_thickness_lower','scaled_artifact_sha256'},'E_MARGIN_SCHEMA');need(d['kind']=='uniform_scaling_margin_v1','E_MARGIN_KIND');need(d['artifact_sha256']==hashlib.sha256(raw).hexdigest(),'E_MARGIN_HASH')
 rho=F(d['scale_down']);need(0<rho<1,'E_MARGIN_FACTOR');need(F(d['original_thickness_lower'])==1/rho,'E_MARGIN_RECIPROCAL')
 D=json.loads(raw)
 for key in ['scale','cap_radius','inner_cap_radius']:D['parameters'][key]=str(F(D['parameters'][key])*rho)
 D['closure']['vertical_clearance']=str(F(D['closure']['vertical_clearance'])*rho)
 changed=(json.dumps(D,indent=2)+'\n').encode();H=hashlib.sha256(changed).hexdigest();need(d['scaled_artifact_sha256']==H,'E_MARGIN_TRANSFORM_HASH')
 covers=[]
 for p in sorted((P/'covers').glob('*.json.gz')):
  c=json.loads(gzip.decompress(p.read_bytes()));c['artifact_sha256']=H;covers.append(c)
 result=check_bundle(changed,covers)
 return {'verdict':'UNIFORM_SCALING_MARGIN_PASS_CANDIDATE_UNREFEREED','verifier':'separately written (same agent) geometry checker, same-agent scaling driver','scale_down':str(rho),'original_thickness_lower':str(1/rho),'covers_recomputed':result['covers'],'leaves_recomputed':result['leaves'],'scaled_artifact_sha256':H,'qualification':'lambda,Q_outer,Q_inner,and upper vertical clearance scale every physical point uniformly; see PROOF.md'}
if __name__=='__main__':
 try:print(json.dumps(check(sys.argv[1]),indent=2))
 except Reject as e:print(str(e));sys.exit(1)

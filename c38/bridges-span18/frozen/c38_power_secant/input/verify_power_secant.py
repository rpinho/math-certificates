"""Separately written (same agent) exact degree-power/secant checker."""
import pathlib,json,hashlib,datetime,importlib.util,argparse,sys
from fractions import Fraction as Q
sys.set_int_max_str_digits(200000)
PARENT='112b2ccffab251aaf9bad964086338f08beabac1a727b4eec346a4707c5a4f97'
class Rejection(Exception):pass
def need(t,c):
 if not t:raise Rejection(c)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p,c):
 try:d=json.loads(p.read_text())
 except (OSError,ValueError):raise Rejection(c)
 need(type(d)is dict,c);return d
def check(root,parent_override=None):
 root=pathlib.Path(root).resolve();fr=root/'input';mf=fr/'MANIFEST.json';m=read(mf,'MANIFEST_JSON')
 need(m.get('schema')=='c38-power-input-v1','SCHEMA');names={'seed.json','build_power_secant.py','verify_power_secant.py','test_power_controls.py','PROOF_POWER_SECANT.md'};need(set(m.get('sha256',{}))==names,'INPUT_COVERAGE')
 for n,pin in m['sha256'].items():need((fr/n).is_file() and sha(fr/n)==pin,'INPUT_SHA256')
 need(sha(pathlib.Path(__file__))==m['sha256']['verify_power_secant.py'],'RUNNING_SOURCE')
 try:
  t=datetime.datetime.fromisoformat(m['frozen_utc']);need(t.tzinfo and t<=datetime.datetime.now(datetime.timezone.utc),'FREEZE_TIME')
 except (KeyError,TypeError,ValueError):raise Rejection('FREEZE_TIME')
 d=read(fr/'seed.json','SEED_JSON');need(d.get('schema')=='c38-power-seed-v1','SEED_SCHEMA');need(d.get('candidate_unrefereed') is True,'STATUS');need(d.get('family')=='unchanged exact disjoint parent finite family; expanded full coefficient vector unmaterialized','FAMILY_SCOPE');need(d.get('parent_manifest_sha256')==PARENT,'PARENT_BINDING')
 base=pathlib.Path(parent_override).resolve() if parent_override else (root/d['parent_relative']).resolve();pm=base/'input/MANIFEST.json';need(pm.is_file() and sha(pm)==PARENT,'PARENT_MANIFEST_SHA256');pmeta=read(pm,'PARENT_JSON');source=base/'input/verify_disjoint_extension.py';need(source.is_file() and sha(source)==pmeta['sha256']['verify_disjoint_extension.py'],'PARENT_SOURCE_SHA256')
 spec=importlib.util.spec_from_file_location('power_parent_checker',source);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 try:v=mod.check(base)
 except mod.Rejection as error:raise Rejection('PARENT_'+str(error))
 need(read(base/'VERIFIED.json','PARENT_VERIFIED_JSON')==v,'PARENT_VERIFIED_MISMATCH');cp=base/'REJECTION_CONTROLS.json';need(cp.is_file() and sha(cp)==d.get('parent_controls_sha256'),'PARENT_CONTROLS_SHA256');c=read(cp,'PARENT_CONTROLS_JSON');need(c.get('status')=='PASS' and c.get('input_manifest_sha256')==PARENT and len(c.get('controls',[]))==27 and all(x.get('pass') is True and x.get('actual')==x.get('expected') and x['expected'].startswith('REJECT:') for x in c['controls']),'PARENT_CONTROLS_INCOMPLETE')
 b=read(base/'input/seed.json','PARENT_SEED_JSON');sp=(base/b['secant_relative'])/'input/seed.json';need(sha(sp)==b['secant_seed_sha256'],'SECANT_SEED_SHA256');s=read(sp,'SECANT_JSON')
 need(type(d.get('M'))is int and d['M']==b['M']==51081913,'BASE_POINT');M=d['M'];need(all(d.get(k)==s[k] for k in ['L17','L18','U']) and d.get('e')==b['extra_lower'],'BASE_VALUES');need(type(d.get('degree18'))is int and d['degree18']==s['degree18']==1296 and type(d.get('degree_extra'))is int and d['degree_extra']==b['extra_degree']==690,'DEGREES')
 k=d.get('k');need(type(k)is int and 0<k<M,'STEP');need(type(d.get('new_M'))is int and d['new_M']==M-k,'NEW_POINT')
 L17,L18,U,e=map(Q,[s['L17'],s['L18'],s['U'],b['extra_lower']]);need(U>=L17 and min(L17,L18,e)>=0,'BRACKETS')
 def value(step):
  ratio=Q(M-step,M);scaled=e*ratio**690+L18*ratio**1296
  return scaled+(1+Q(step,314))*L17-Q(step,314)*U
 result=value(k);need(result>=1,'BELOW_ONE');need(d.get('S')==str(result),'CLAIMED_VALUE');need(value(k+1)<1,'GRID_STEP_NOT_MAXIMAL');mu=Q(1<<27,M-k);need(d.get('mu')==str(mu),'CLAIMED_MU');need(mu>Q(1051,400),'TARGET')
 return {'status':'VERIFIED_CANDIDATE_UNREFEREED_POWER_SECANT','verification':'separately written (same agent) exact degree-power extension of the complete frozen disjoint certificate','input_manifest_sha256':sha(mf),'parent_manifest_sha256':PARENT,'mu':str(mu),'steps':k,'S':str(result),'S_decimal_diagnostic':float(result),'expanded_full_integer_coefficient_vector_materialized':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('receipt');a=p.parse_args()
 try:
  v=check(a.artifact);pathlib.Path(a.receipt).write_text(json.dumps(v,indent=2)+'\n');print(v['status'],v['mu'],v['S_decimal_diagnostic'])
 except Rejection as e:print('REJECT:'+str(e));raise SystemExit(2)

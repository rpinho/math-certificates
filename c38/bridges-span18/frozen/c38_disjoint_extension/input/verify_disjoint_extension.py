"""Separately written (same agent), four-term exact disjoint-family verifier."""
import pathlib,json,hashlib,datetime,importlib.util,argparse
from fractions import Fraction as F
SECANT='61a2f2064a58dfae8568bf13e60350ffdddbe6cc94746d9d001a7c64370244e9'
class Rejection(Exception):pass
def need(t,c):
 if not t:raise Rejection(c)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p,c):
 try:d=json.loads(p.read_text())
 except (OSError,ValueError):raise Rejection(c)
 need(type(d)is dict,c);return d
def load(p,name):
 spec=importlib.util.spec_from_file_location(name,p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def check(root,overrides=None):
 root=pathlib.Path(root).resolve();fr=root/'input';mf=fr/'MANIFEST.json';m=read(mf,'MANIFEST_JSON')
 need(m.get('schema')=='c38-disjoint-input-v1','SCHEMA')
 names={'seed.json','build_disjoint_extension.py','verify_disjoint_extension.py','test_disjoint_controls.py','PROOF_DISJOINT_EXTENSION.md','verify_rectangle_point_packet.py'}
 need(set(m.get('sha256',{}))==names,'INPUT_COVERAGE')
 for name,pin in m['sha256'].items():need((fr/name).is_file() and sha(fr/name)==pin,'INPUT_SHA256')
 need(sha(pathlib.Path(__file__))==m['sha256']['verify_disjoint_extension.py'],'RUNNING_SOURCE')
 try:
  t=datetime.datetime.fromisoformat(m['frozen_utc']);need(t.tzinfo and t<=datetime.datetime.now(datetime.timezone.utc),'FREEZE_TIME')
 except (KeyError,TypeError,ValueError):raise Rejection('FREEZE_TIME')
 d=read(fr/'seed.json','SEED_JSON');need(d.get('schema')=='c38-disjoint-seed-v1','SEED_SCHEMA');need(d.get('candidate_unrefereed') is True,'STATUS')
 need(d.get('family')=='main spans1-18 union normalized span19-30 range22 cap5 irreducibles; expanded full coefficient vector unmaterialized','FAMILY_SCOPE')
 need(d.get('secant_manifest_sha256')==SECANT,'SECANT_BINDING')
 locations={n:(pathlib.Path(overrides[n]).resolve() if overrides else (root/d[n+'_relative']).resolve()) for n in ['secant','point22','point23']};base=locations['secant']
 sm=base/'input/MANIFEST.json';need(sm.is_file() and sha(sm)==SECANT,'SECANT_MANIFEST_SHA256');smeta=read(sm,'SECANT_JSON');source=base/'input/verify_secant_rescale.py';need(source.is_file() and sha(source)==smeta['sha256']['verify_secant_rescale.py'],'SECANT_SOURCE_SHA256')
 checker=load(source,'disjoint_secant_checker')
 try:checker.check(base)
 except checker.Rejection as e:raise Rejection('SECANT_'+str(e))
 sp=base/'input/seed.json';need(sha(sp)==d.get('secant_seed_sha256'),'SECANT_SEED_SHA256');s=read(sp,'SECANT_SEED_JSON')
 pc=load(fr/'verify_rectangle_point_packet.py','disjoint_point_checker');points={}
 for key in ['point22','point23']:
  r=locations[key];pm=r/'input/MANIFEST.json';need(pm.is_file() and sha(pm)==d.get(key+'_manifest_sha256'),'POINT_INPUT_SHA256')
  try:v=pc.check(r)
  except pc.Reject as e:raise Rejection('POINT_'+str(e))
  expected=dict(W=22 if key=='point22' else 23,span_min=18,span_max=30 if key=='point22' else 18,crossing_cap=5,M=51081913,S=96)
  need(v['parameters']==expected,'POINT_FAMILY_PARAMETERS')
  verified=read(r/'VERIFIED.json','POINT_VERIFIED_JSON');need(verified==v,'POINT_VERIFIED_MISMATCH')
  controls=r/'REJECTION_CONTROLS.json';need(controls.is_file() and sha(controls)==d.get(key+'_controls_sha256'),'POINT_CONTROLS_SHA256');c=read(controls,'POINT_CONTROLS_JSON')
  need(c.get('status')=='PASS' and c.get('input_manifest_sha256')==sha(pm) and len(c.get('controls',[]))==12 and all(x.get('pass_') is True and x.get('actual')==x.get('expected') and x['expected'].startswith('REJECT:') for x in c['controls']),'POINT_CONTROLS_INCOMPLETE')
  points[key]=read(r/'replay.json','POINT_REPLAY_JSON')
 need(type(d.get('M'))is int and d['M']==s['M']==51081913,'BASE_POINT');M=d['M']
 lower=F(int(points['point22']['num_lo']),1<<96);upper=F(int(points['point23']['num_hi']),1<<96);extra=max(F(0),lower-upper)
 need(d.get('lower22')==str(lower) and d.get('upper23')==str(upper),'POINT_VALUES');need(extra>0 and d.get('extra_lower')==str(extra),'EXTRA_LOWER')
 need(all(type(d.get(key))is int for key in ['extra_span_min','extra_span_max','extra_range','extra_crossing_cap']) and [d['extra_span_min'],d['extra_span_max'],d['extra_range'],d['extra_crossing_cap']]==[19,30,22,5],'EXTRA_FAMILY')
 degree=30*(22+1);need(type(d.get('extra_degree'))is int and d['extra_degree']==degree,'EXTRA_DEGREE')
 k=d.get('k');need(type(k)is int and 0<k<M,'STEP');need(type(d.get('new_M'))is int and d['new_M']==M-k,'NEW_POINT');need(min(M-k*s['degree18'],M-k*degree)>=0,'NEGATIVE_MULTIPLIER')
 L17,L18,U=map(F,[s['L17'],s['L18'],s['U']]);t=F(k,314)
 value=(1+t)*L17-t*U+F(M-k*s['degree18'],M)*L18+F(M-k*degree,M)*extra
 need(value>=1,'BELOW_ONE');need(d.get('S')==str(value),'CLAIMED_VALUE');slope=F(s['slope'])+F(degree,M)*extra;need(L17+L18+extra-(k+1)*slope<1,'GRID_STEP_NOT_MAXIMAL')
 mu=F(1<<27,M-k);need(d.get('mu')==str(mu),'CLAIMED_MU');need(mu>F(1051,400),'TARGET')
 return {'status':'VERIFIED_CANDIDATE_UNREFEREED_DISJOINT_EXTENSION','verification':'separately written (same agent) exact disjoint higher-span extension of fully replayed frozen artifacts','input_manifest_sha256':sha(mf),'secant_input_sha256':SECANT,'point_input_sha256':{key:d[key+'_manifest_sha256'] for key in ['point22','point23']},'mu':str(mu),'steps':k,'extra_lower':str(extra),'extra_lower_decimal_diagnostic':float(extra),'S':str(value),'S_decimal_diagnostic':float(value),'expanded_full_integer_coefficient_vector_materialized':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('receipt');a=p.parse_args()
 try:
  v=check(a.artifact);pathlib.Path(a.receipt).write_text(json.dumps(v,indent=2)+'\n');print(v['status'],v['mu'],v['S_decimal_diagnostic'])
 except Rejection as e:print('REJECT:'+str(e));raise SystemExit(2)

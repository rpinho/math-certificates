"""Separately written (same agent), three-term secant certificate checker."""
import pathlib,json,hashlib,datetime,importlib.util,argparse
from fractions import Fraction as Q
MAIN='865241e4447884bb5354ba1799ab94baf4923bb4870e927a151cf14415d6faad'
SPAN='00007825552d00027007f4011d19b1b814d9c81ecf9e670ddb897331a46e052b'
STOP='66ab647c05dbf591a880e361abc8aa88f4abb4a2bf5a5a729f3807f6690e2887'
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
def controls(d,count,code):
 need(d.get('status')=='PASS' and len(d.get('controls',[]))==count and all(c.get('pass') is True and c.get('actual')==c.get('expected') and c['expected'].startswith('REJECT:') for c in d['controls']) and any(c.get('fresh_native_replay') for c in d['controls']),code)
def check(root,overrides=None):
 root=pathlib.Path(root).resolve();fr=root/'input';mf=fr/'MANIFEST.json';m=read(mf,'MANIFEST_JSON')
 need(m.get('schema')=='c38-secant-input-v1','SCHEMA')
 names={'seed.json','build_secant_rescale.py','verify_secant_rescale.py','test_secant_controls.py','PROOF_SECANT_RESCALE.md'}
 need(set(m.get('sha256',{}))==names,'INPUT_COVERAGE')
 for name,pin in m['sha256'].items():need((fr/name).is_file() and sha(fr/name)==pin,'INPUT_SHA256')
 need(sha(pathlib.Path(__file__))==m['sha256']['verify_secant_rescale.py'],'RUNNING_SOURCE')
 try:
  t=datetime.datetime.fromisoformat(m['frozen_utc']);need(t.tzinfo and t<=datetime.datetime.now(datetime.timezone.utc),'FREEZE_TIME')
 except (KeyError,TypeError,ValueError):raise Rejection('FREEZE_TIME')
 d=read(fr/'seed.json','SEED_JSON');need(d.get('schema')=='c38-secant-seed-v1','SEED_SCHEMA');need(d.get('candidate_unrefereed') is True,'STATUS')
 need(d.get('family')=='unchanged exact finite main bridge family; expanded full coefficient vector unmaterialized','FAMILY_SCOPE')
 need(d.get('main_packet_sha256')==MAIN and d.get('span_manifest_sha256')==SPAN and d.get('stop_manifest_sha256')==STOP,'BASE_BINDING')
 locations={n:(pathlib.Path(overrides[n]).resolve() if overrides else (root/d[n+'_relative']).resolve()) for n in ['main','span','stop']};base=locations['main'];span=locations['span'];stop=locations['stop']
 sm=span/'input/MANIFEST.json';need(sm.is_file() and sha(sm)==SPAN,'SPAN_MANIFEST_SHA256');sp=read(sm,'SPAN_JSON');source=span/'input/verify_span_degree.py';need(source.is_file() and sha(source)==sp['sha256']['verify_span_degree.py'],'SPAN_SOURCE_SHA256')
 sc=load(source,'secant_span_checker')
 try:sc.check(span,base)
 except sc.Rejection as e:raise Rejection('BASE_'+str(e))
 v=read(base/'FULL_ACCEPTANCE.json','MAIN_FULL_JSON');packet=read(base/'packet.json','MAIN_PACKET_JSON');mc=read(base/'REJECTION_CONTROLS.json','MAIN_CONTROLS_JSON');need(mc.get('packet_sha256')==MAIN,'MAIN_CONTROLS_BINDING');controls(mc,35,'MAIN_CONTROLS_INCOMPLETE')
 im=stop/'input/INPUT_MANIFEST.json';need(im.is_file() and sha(im)==STOP,'STOP_INPUT_SHA256');source=stop/'verify_span17_stop.py';need(source.is_file() and sha(source)==packet['source_sha256']['verify_span17_stop.py'],'STOP_SOURCE_SHA256')
 checker=load(source,'secant_stop_checker')
 try:sv=checker.check(stop)
 except checker.Reject as e:raise Rejection('STOP_'+str(e))
 fullpath=stop/'FULL_ACCEPTANCE.json';need(fullpath.is_file() and sha(fullpath)==d.get('stop_full_sha256'),'STOP_FULL_SHA256');full=read(fullpath,'STOP_FULL_JSON');need(full==dict(sv,fresh_full_replay=True),'STOP_FULL_INCOMPLETE')
 for h in range(1,18):
  for name,folder in [('span','replay'),('public','replay_public')]:
   actual=read(stop/'complete_union_replay'/('%s_%d.json'%(name,h)),'STOP_FRESH_JSON');old=read(stop/folder/('span_%d.json'%h),'STOP_REFERENCE_JSON');need(actual==old,'STOP_FRESH_MISMATCH')
 cp=stop/'REJECTION_CONTROLS.json';need(cp.is_file() and sha(cp)==d.get('stop_controls_sha256'),'STOP_CONTROLS_SHA256');c=read(cp,'STOP_CONTROLS_JSON');need(c.get('input_manifest_sha256')==STOP,'STOP_CONTROLS_BINDING');controls(c,11,'STOP_CONTROLS_INCOMPLETE')
 need(type(d.get('M'))is int and d['M']==v['M']==51081913,'BASE_POINT');M=d['M'];need(type(d.get('upper_point_M'))is int and d['upper_point_M']==sv['endpoint_M'][1]==51082227,'SECOND_POINT')
 L17=sum((Q(e['finite_irreducible_lower']) for e in v['spans'][:17]),Q(0));L18=Q(v['spans'][17]['finite_irreducible_lower']);U=Q(sv['endpoint_upper_sums'][1]);need(d.get('L17')==str(L17) and d.get('L18')==str(L18),'LOWER_VALUES');need(d.get('U')==str(U) and U>=L17,'UPPER_VALUE')
 degree=v['spans'][17]['l']*v['spans'][17]['w'];need(type(d.get('degree18'))is int and d['degree18']==degree,'DEGREE18');slope=(U-L17)/314+Q(degree,M)*L18;need(slope>0 and d.get('slope')==str(slope),'SLOPE')
 k=d.get('k');need(type(k)is int and 0<k<M,'STEP');new=M-k;need(type(d.get('new_M'))is int and d['new_M']==new,'NEW_POINT');need(M-k*degree>=0,'NEGATIVE_MULTIPLIER')
 t=Q(k,314);value=(1+t)*L17-t*U+Q(M-k*degree,M)*L18
 need(value>=1,'BELOW_ONE');need(d.get('S')==str(value),'CLAIMED_VALUE');need(L17+L18-(k+1)*slope<1,'GRID_STEP_NOT_MAXIMAL')
 mu=Q(1<<27,new);need(d.get('mu')==str(mu),'CLAIMED_MU');need(mu>Q(1051,400),'TARGET')
 return {'status':'VERIFIED_CANDIDATE_UNREFEREED_SECANT_RESCALE','verification':'separately written (same agent) exact secant extension of fully replayed frozen native artifacts','input_manifest_sha256':sha(mf),'main_packet_sha256':MAIN,'stop_input_sha256':STOP,'mu':str(mu),'steps':k,'S':str(value),'S_decimal_diagnostic':float(value),'expanded_full_integer_coefficient_vector_materialized':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('receipt');a=p.parse_args()
 try:
  v=check(a.artifact);pathlib.Path(a.receipt).write_text(json.dumps(v,indent=2)+'\n');print(v['status'],v['mu'],v['S_decimal_diagnostic'])
 except Rejection as e:print('REJECT:'+str(e));raise SystemExit(2)

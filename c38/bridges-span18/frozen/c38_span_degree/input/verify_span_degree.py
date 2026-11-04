"""Separately written (same agent) exact span-degree checker."""
import pathlib,json,hashlib,datetime,importlib.util,argparse,sys
from fractions import Fraction
BASE_PIN='865241e4447884bb5354ba1799ab94baf4923bb4870e927a151cf14415d6faad'
class Rejection(Exception):pass
def require(t,c):
 if not t:raise Rejection(c)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p,c):
 try:d=json.loads(p.read_text())
 except (OSError,ValueError):raise Rejection(c)
 require(type(d)is dict,c);return d
def check(root,base_override=None):
 root=pathlib.Path(root).resolve();fr=root/'input';mf=fr/'MANIFEST.json';m=read(mf,'MANIFEST_JSON')
 require(m.get('schema')=='c38-span-degree-input-v1','SCHEMA')
 names={'seed.json','build_span_degree.py','verify_span_degree.py','test_span_degree_controls.py','PROOF_SPAN_DEGREE.md'}
 require(set(m.get('sha256',{}))==names,'INPUT_COVERAGE')
 for n,pin in m['sha256'].items():require((fr/n).is_file() and digest(fr/n)==pin,'INPUT_SHA256')
 require(digest(pathlib.Path(__file__))==m['sha256']['verify_span_degree.py'],'RUNNING_SOURCE')
 try:
  stamp=datetime.datetime.fromisoformat(m['frozen_utc']);require(stamp.tzinfo is not None and stamp<=datetime.datetime.now(datetime.timezone.utc),'FREEZE_TIME')
 except (KeyError,TypeError,ValueError):raise Rejection('FREEZE_TIME')
 d=read(fr/'seed.json','SEED_JSON');require(d.get('schema')=='c38-span-degree-seed-v1','SEED_SCHEMA')
 require(d.get('candidate_unrefereed') is True,'STATUS')
 require(d.get('family')=='same finite exact family; expanded integer coefficient vector unmaterialized','FAMILY_SCOPE')
 require(d.get('main_packet_sha256')==BASE_PIN,'BASE_BINDING')
 base=pathlib.Path(base_override).resolve() if base_override else (root/d['main_relative_path']).resolve()
 require((base/'packet.json').is_file() and digest(base/'packet.json')==BASE_PIN,'BASE_PACKET_SHA256')
 p=read(base/'packet.json','BASE_JSON');require(digest(base/'verify_packet.py')==p['source_sha256']['verify_packet.py'],'BASE_CHECKER_SHA256')
 spec=importlib.util.spec_from_file_location('span_degree_main',base/'verify_packet.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 try:v=mod.check(base/'packet.json')
 except mod.Rejection as e:raise Rejection('BASE_'+str(e))
 fullpath=base/'FULL_ACCEPTANCE.json';require(fullpath.is_file() and digest(fullpath)==d.get('main_full_sha256'),'BASE_FULL_SHA256');full=read(fullpath,'BASE_FULL_JSON')
 require(full.get('packet_sha256')==BASE_PIN and 'fresh full replay' in full.get('verification','') and full==dict(v,verification=full.get('verification')),'BASE_FULL_INCOMPLETE')
 for e in p['spans']:
  fresh=read(base/'complete_union_replay'/('span_%d.json'%e['l']),'BASE_FRESH_JSON');old=read(base/e['separate']['path'],'BASE_REFERENCE_JSON');require(fresh==old,'BASE_FRESH_MISMATCH')
 require(type(d.get('M'))is int and d['M']==v['M'],'BASE_POINT')
 rows=d.get('spans');require(type(rows)is list and len(rows)==18,'SPAN_COVERAGE')
 lower=Fraction(0);weighted=Fraction(0);degrees=[]
 for row,e in zip(rows,v['spans']):
  require(type(row)is dict and type(row.get('h'))is int and row['h']==e['l'],'SPAN_ORDER')
  require(type(row.get('w'))is int and row['w']==e['w'],'WIDTH')
  degree=e['l']*e['w'];require(type(row.get('degree'))is int and row['degree']==degree,'DEGREE')
  require(row.get('alpha')==e['finite_irreducible_lower'],'ALPHA')
  a=Fraction(e['finite_irreducible_lower']);require(a>=0,'NEGATIVE_ALPHA');lower+=a;weighted+=degree*a;degrees.append(degree)
 require(d.get('L')==str(lower) and d.get('T')==str(weighted),'WEIGHTED_SUM')
 k=d.get('k');require(type(k)is int and 0<k<d['M'],'STEP')
 new=d['M']-k;require(type(d.get('new_M'))is int and d['new_M']==new,'NEW_POINT')
 delta=Fraction(k,d['M']);require(all(1-n*delta>=0 for n in degrees),'NEGATIVE_MULTIPLIER')
 # Accumulate per-span factors, rather than producer's L - k*T/M formula.
 result=sum((Fraction(e['finite_irreducible_lower'])*(1-e['l']*e['w']*delta) for e in reversed(v['spans'])),Fraction(0))
 require(result>=1,'BELOW_ONE');require(d.get('S')==str(result),'CLAIMED_VALUE')
 require(lower-Fraction(k+1,d['M'])*weighted<1,'GRID_STEP_NOT_MAXIMAL')
 mu=Fraction(1<<27,new);require(d.get('mu')==str(mu),'CLAIMED_MU');require(mu>Fraction(1051,400),'TARGET')
 return {'status':'VERIFIED_CANDIDATE_UNREFEREED_SPAN_DEGREE','verification':'separately written (same agent) exact arithmetic on the fully replayed frozen finite bridge family','input_manifest_sha256':digest(mf),'main_packet_sha256':BASE_PIN,'mu':str(mu),'M':new,'steps':k,'S':str(result),'S_decimal_diagnostic':float(result),'expanded_integer_coefficient_vector_materialized':False}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('artifact');parser.add_argument('receipt');parser.add_argument('--base');args=parser.parse_args()
 try:
  result=check(args.artifact,args.base);pathlib.Path(args.receipt).write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['mu'],result['S_decimal_diagnostic'])
 except Rejection as e:print('REJECT:'+str(e));sys.exit(2)

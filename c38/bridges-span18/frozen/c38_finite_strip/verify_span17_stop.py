"""Separately written (same agent) exact upper certificate for span<=17 sums."""
import json,pathlib,hashlib,sys,datetime,argparse,subprocess,os,signal
from fractions import Fraction as Q
class Reject(Exception):pass
ACTIVE_CHILD=None
def stop_own_child(signum,frame):
 if ACTIVE_CHILD is not None and ACTIVE_CHILD.poll() is None:
  os.killpg(ACTIVE_CHILD.pid,signal.SIGTERM);ACTIVE_CHILD.wait()
 raise SystemExit(128+signum)
def need(x,c):
 if not x:raise Reject(c)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def point(root,fr,manifest,corehash,M,folder,coverage,public=False):
 receipt=root/folder/'RECEIPTS.json';need(receipt.is_file(),'RECEIPTS_MISSING');rr=json.loads(receipt.read_text())
 need(rr.get('input_manifest_sha256')==sha(manifest),'RECEIPT_INPUT_BINDING')
 need(rr.get('schema')=='c38-per-span-frozen-replay-v1' and rr.get('core_manifest_sha256')==corehash,'RECEIPT_CORE_BINDING')
 records=rr.get('spans',[]);count=17 if public else coverage
 need(len(records)==count and [r.get('l') for r in records]==list(range(1,count+1)),'COVERAGE');need(rr.get('M')==M,'FUGACITY')
 Blo,Bhi,Alo,Ahi={},{},{},{}
 for h,r in enumerate(records[:17],1):
  prod=fr/('production/span_%d.json'%h);separate=root/folder/('span_%d.json'%h)
  need(r.get('status')=='COMPLETE_FROZEN_REPLAY_MATCH','REPLAY_INCOMPLETE')
  need(prod.is_file() and separate.is_file(),'REPLAY_FILE_MISSING')
  need(sha(prod)==r.get('input_sha256') and sha(separate)==r.get('output_sha256'),'RECEIPT_SHA256')
  need(r.get('core_manifest_sha256')==corehash and r.get('span_manifest_path')=='span_manifests/span_%d.json'%h,'SPAN_BINDING')
  smpath=fr/r['span_manifest_path'];need(smpath.is_file() and sha(smpath)==r.get('span_manifest_sha256'),'SPAN_MANIFEST_SHA256');sm=json.loads(smpath.read_text())
  need(sm.get('schema')=='c38-frozen-span-input-v1' and sm.get('l')==h and sm.get('M')==51081913 and sm.get('production_sha256')==sha(prod) and sm.get('core_manifest_sha256')==corehash,'SPAN_FROZEN_BINDING')
  try:
   f,b,e=[datetime.datetime.fromisoformat(x) for x in [sm['frozen_utc'],r['replay_started_utc'],r['replay_completed_utc']]];need(f.tzinfo is not None and f<=b<=e,'FREEZE_REPLAY_ORDER')
  except (KeyError,TypeError,ValueError):raise Reject('FREEZE_REPLAY_TIME_FORMAT')
  d=json.loads(prod.read_text());v=json.loads(separate.read_text());p=[e for e in d['x'] if e.get('Mnum')==M];need(len(p)==1,'POINT_COVERAGE');p=p[0]
  need(d.get('l')==h and d.get('S')==96 and v.get('l')==h and v.get('M')==M and v.get('w')==d['w'] and v.get('S')==96 and v.get('F')==12,'PARAMETERS')
  need(v.get('status')=='COMPLETE_SEPARATE_SAME_AGENT_RECOMPUTATION','NATIVE_REPLAY_INCOMPLETE')
  need(all(v[k]==p[k] for k in ['num_lo','num_hi']),'FINITE_NUMERATOR_MISMATCH')
  need(all(v[k]==d[k] for k in ['total_states','edges']),'GRAPH_COUNT_MISMATCH')
  sizes=v.get('stage_sizes',[]);need(len(sizes)==h+1 and all(type(x)is int and x>0 for x in sizes) and sum(sizes)==v['total_states'],'STAGE_SIZES')
  values=[v[k] for k in ['num_lo','num_hi','num_tail']];need(all(type(x)in(str,int) and str(x).lstrip('-').isdigit() for x in values),'NUMERATOR_FORMAT')
  a,b,t=map(int,values);need(0<=a<=b and t>=0,'BRACKET')
  Blo[h]=Q(a,1<<96);Bhi[h]=Q(b+t,1<<96)
  Ahi[h]=Bhi[h]-sum((Blo[h-j]*Alo[j] for j in range(1,h)),Q(0))
  Alo[h]=max(Q(0),Blo[h]-sum((Bhi[h-j]*Ahi[j] for j in range(1,h)),Q(0)))
  need(0<=Alo[h]<=Ahi[h],'RENEWAL_BRACKET')
 return sum(Ahi.values(),Q(0))
def check(root,full=False,binary=None,work=None):
 global ACTIVE_CHILD
 root=pathlib.Path(root);fr=root/'input';manifest=fr/'INPUT_MANIFEST.json';need(manifest.is_file(),'INPUT_MANIFEST_MISSING')
 m=json.loads(manifest.read_text());need(m.get('schema')=='c38-frozen-producer-input-v1' and m.get('L')in(17,18) and m.get('M')==51081913,'INPUT_SCHEMA')
 corefile=fr/'CORE_MANIFEST.json';need(corefile.is_file(),'CORE_MANIFEST_MISSING');core=json.loads(corefile.read_text());corehash=sha(corefile)
 need(core.get('schema')=='c38-frozen-verifier-core-v1','CORE_SCHEMA')
 need(set(core.get('sha256',{}))=={'BAR_PUBLIC.json','verify_strip.cpp','verify_strip_f44.cpp','tmx_parallel.c','PROOF_FINITE_STRIP.md','PRIOR_ART_PUBLIC.md'},'CORE_COVERAGE')
 expected=set(core['sha256'])|{'CORE_MANIFEST.json'}|{'production/span_%d.json'%h for h in range(1,m['L']+1)}|{'span_manifests/span_%d.json'%h for h in range(1,m['L']+1)}
 if m.get('terminal_span_mode')=='FINITE_LAST_SPAN_LOWER_ONLY':
  fcp=fr/'finite/MANIFEST.json';need(fcp.is_file(),'FINITE_CORE_MISSING');fc=json.loads(fcp.read_text());need(fc.get('schema')=='c38-finite-last-core-v1','FINITE_CORE_SCHEMA')
  expected|={'finite/MANIFEST.json'}|{'finite/'+name for name in fc['sha256']}
 need(set(m.get('sha256',{}))==expected,'INPUT_COVERAGE')
 for rel,pin in m['sha256'].items():need((fr/rel).is_file() and sha(fr/rel)==pin,'FROZEN_INPUT_SHA256')
 for rel,pin in core['sha256'].items():need(sha(fr/rel)==pin,'CORE_INPUT_SHA256')
 x0,x1,target=Q(51081913,1<<27),Q(51082227,1<<27),Q(400,1051)
 need(x0<target<x1,'FUGACITY_BRACKET');lam=(target-x0)/(x1-x0)
 u0=point(root,fr,manifest,corehash,51081913,'replay',m['L']);u1=point(root,fr,manifest,corehash,51082227,'replay_public',m['L'],True)
 upper=(1-lam)*u0+lam*u1;need(upper<1,'UPPER_NOT_BELOW_ONE')
 result={'status':'CANDIDATE_UNREFEREED_SPAN17_METHOD_STOP_CERTIFICATE','verification':'complete frozen separately written (same agent) two-point native replay plus exact rational upper assembly','endpoint_M':[51081913,51082227],'target_fugacity':'400/1051','convex_interpolation_weight':str(lam),'endpoint_upper_sums':[str(u0),str(u1)],'upper_sum':str(upper),'gap_below_one':str(1-upper),'upper_sum_decimal_diagnostic':float(upper),'scope':'all irreducible bridges of spans<=17, all lengths and transverse widths; their renewal sum at target is below1; this is not an upper bound on mu','input_manifest_sha256':sha(manifest)}
 if full:
  need(binary is not None and work is not None,'FULL_REPLAY_ARGUMENTS');work=pathlib.Path(work);need(not work.exists(),'REPLAY_WORK_EXISTS');work.mkdir(parents=True)
  for h in range(1,18):
   d=json.loads((fr/('production/span_%d.json'%h)).read_text());out=work/('span_%d.json'%h);pub=work/('public_%d.json'%h)
   args=[str(pathlib.Path(binary).resolve()),str(h),'51081913',str(d['w']),str(out),'12','--also','51082227',str(pub)]
   with (work/('span_%d.log'%h)).open('w') as log:
    child=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);ACTIVE_CHILD=child
    with (work/'CHILD_PIDS.jsonl').open('a') as f:f.write(json.dumps({'pid':child.pid,'span':h})+'\n')
    registry=os.environ.get('C38_REGISTER_PIDS_PATH')
    if registry:
     with pathlib.Path(registry).open('a') as f:f.write(json.dumps({'pid':child.pid,'args':args,'log':str(work/('span_%d.log'%h)),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
    code=child.wait();ACTIVE_CHILD=None
   need(code==0,'FULL_REPLAY_REJECTED')
   need(json.loads(out.read_text())==json.loads((root/'replay'/('span_%d.json'%h)).read_text()) and json.loads(pub.read_text())==json.loads((root/'replay_public'/('span_%d.json'%h)).read_text()),'FULL_REPLAY_MISMATCH')
  result['fresh_full_replay']=True
 return result
if __name__=='__main__':
 signal.signal(signal.SIGTERM,stop_own_child);signal.signal(signal.SIGINT,stop_own_child)
 p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('output');p.add_argument('--full',action='store_true');p.add_argument('--binary');p.add_argument('--work');a=p.parse_args()
 try:r=check(a.artifact,a.full,a.binary,a.work);pathlib.Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(r['status'],r['upper_sum_decimal_diagnostic'])
 except Reject as e:print('REJECT:'+str(e));sys.exit(2)

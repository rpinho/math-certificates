"""Separately written (same agent) frozen finite-strip certificate verifier.
No search-side Python module is imported. Full mode recomputes every state/value.
"""
import argparse,hashlib,json,math,pathlib,subprocess,sys,datetime,os,signal
from fractions import Fraction
sys.set_int_max_str_digits(200000)
class Rejection(Exception):pass
ACTIVE_CHILD=None
def stop_own_child(signum,frame):
 if ACTIVE_CHILD is not None and ACTIVE_CHILD.poll() is None:
  os.killpg(ACTIVE_CHILD.pid,signal.SIGTERM);ACTIVE_CHILD.wait()
 raise SystemExit(128+signum)
def need(test,code):
 if not test:raise Rejection(code)
def integer(x,code):
 need(type(x) in (str,int) and str(x).lstrip('-').isdigit(),code);return int(x)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read_json(p,code):
 try:d=json.loads(p.read_text())
 except (OSError,ValueError,UnicodeError):raise Rejection(code)
 need(isinstance(d,dict),code);return d
def check(path,full=False,binary=None,work=None,finite_binary=None):
 global ACTIVE_CHILD
 path=pathlib.Path(path).resolve();root=path.parent
 d=read_json(path,'MANIFEST_JSON')
 need(d.get('schema')=='c38-finite-strip-v1','SCHEMA')
 L=integer(d.get('L'),'SPAN_LIMIT');M=integer(d.get('M'),'FUGACITY')
 need(1<=L<=20,'SPAN_LIMIT');need(0<M<(1<<26),'FUGACITY')
 need(M*1051<=400*(1<<27),'TARGET_TOO_WEAK')
 need(d.get('target')=={'p':1051,'q':400} and all(type(x)is int for x in d['target'].values()),'TARGET_CHANGED')
 need(d.get('coefficient_class')=='all irreducible bridges with span-specific transverse caps','COEFFICIENT_CLASS')
 need(d.get('coefficient_encoding')=='exact finite combinatorial specification; expanded integer vector not materialized','COEFFICIENT_ENCODING')
 entries=d.get('spans');need(isinstance(entries,list) and len(entries)==L,'SPAN_COVERAGE')
 need(all(isinstance(e,dict) for e in entries) and [e.get('l') for e in entries]==list(range(1,L+1)),'SPAN_ORDER_OR_DUPLICATE')
 need(isinstance(d.get('source_sha256'),dict),'SOURCE_REFERENCES')
 for rel,sha in d['source_sha256'].items():
  p=root/rel;need(p.is_file(),'SOURCE_MISSING');need(digest(p)==sha,'SOURCE_SHA256')
 need('verify_strip.cpp' in d.get('source_sha256',{}),'VERIFIER_SOURCE_UNPINNED')
 need('verify_packet.py' in d.get('source_sha256',{}),'ASSEMBLER_SOURCE_UNPINNED')
 need(digest(pathlib.Path(__file__))==d['source_sha256']['verify_packet.py'],'RUNNING_VERIFIER_SOURCE')
 frozen=d.get('frozen_input_manifest');need(isinstance(frozen,dict),'FROZEN_MANIFEST_MISSING')
 fp=root/frozen.get('path','');need(fp.is_file(),'FROZEN_MANIFEST_MISSING');need(digest(fp)==frozen.get('sha256'),'FROZEN_MANIFEST_SHA256')
 fm=read_json(fp,'FROZEN_MANIFEST_JSON');need(fm.get('schema')=='c38-frozen-producer-input-v1' and fm.get('L')==L and fm.get('M')==M,'FROZEN_MANIFEST_PARAMETERS')
 corepath=fp.parent/'CORE_MANIFEST.json';need(corepath.is_file(),'CORE_MANIFEST_MISSING')
 cm=read_json(corepath,'CORE_MANIFEST_JSON');need(cm.get('schema')=='c38-frozen-verifier-core-v1','CORE_SCHEMA')
 corefiles={'BAR_PUBLIC.json','verify_strip.cpp','verify_strip_f44.cpp','tmx_parallel.c','PROOF_FINITE_STRIP.md','PRIOR_ART_PUBLIC.md'}
 need(set(cm.get('sha256',{}))==corefiles,'CORE_COVERAGE')
 expected=corefiles|{'CORE_MANIFEST.json'}|{'production/span_%d.json'%i for i in range(1,L+1)}|{'span_manifests/span_%d.json'%i for i in range(1,L+1)}
 terminal=fm.get('terminal_span_mode','FULL_WIDTH_CERTIFIED');need(terminal in ('FULL_WIDTH_CERTIFIED','FINITE_LAST_SPAN_LOWER_ONLY') and d.get('terminal_span_mode','FULL_WIDTH_CERTIFIED')==terminal,'TERMINAL_MODE')
 finite_terminal=terminal=='FINITE_LAST_SPAN_LOWER_ONLY';fc=None;finitehash=None
 if finite_terminal:
  need(L==18,'FINITE_LAST_SPAN_LIMIT');fcp=fp.parent/'finite/MANIFEST.json';need(fcp.is_file(),'FINITE_CORE_MISSING');fc=read_json(fcp,'FINITE_CORE_JSON');finitehash=digest(fcp)
  need(fc.get('schema')=='c38-finite-last-core-v1' and set(fc.get('sha256',{}))=={'tmx_finite.c','verify_finite_strip.cpp','PROOF_LAST_FINITE.md'},'FINITE_CORE_SCHEMA')
  need(fm.get('finite_core_sha256')==finitehash,'FINITE_CORE_BINDING')
  need('verify_finite_strip.cpp' in d['source_sha256'],'FINITE_VERIFIER_SOURCE_UNPINNED')
  for name,pin in fc['sha256'].items():
   q=fcp.parent/name;need(q.is_file() and digest(q)==pin,'FINITE_CORE_INPUT_SHA256');need(d['source_sha256'].get(name)==pin,'FINITE_SOURCE_BINDING')
  expected|={'finite/MANIFEST.json'}|{'finite/'+name for name in fc['sha256']}

 need(set(fm.get('sha256',{}))==expected,'FROZEN_INPUT_COVERAGE')
 for rel,pin in cm['sha256'].items():
  need((fp.parent/rel).is_file(),'CORE_INPUT_MISSING');need(digest(fp.parent/rel)==pin,'CORE_INPUT_SHA256')
  if rel in d['source_sha256']:need(d['source_sha256'][rel]==pin,'SOURCE_CORE_BINDING')
 for rel,sha in fm.get('sha256',{}).items():
  p=fp.parent/rel;need(p.is_file(),'FROZEN_INPUT_MISSING');need(digest(p)==sha,'FROZEN_INPUT_SHA256')
 replaymeta=d.get('frozen_replay_receipts');need(isinstance(replaymeta,dict),'RECEIPTS_MISSING')
 rp=root/replaymeta.get('path','');need(rp.is_file(),'RECEIPTS_MISSING');need(digest(rp)==replaymeta.get('sha256'),'RECEIPTS_SHA256')
 rr=read_json(rp,'RECEIPTS_JSON');need(rr.get('input_manifest_sha256')==frozen['sha256'],'RECEIPTS_INPUT_BINDING')
 need(rr.get('schema')=='c38-per-span-frozen-replay-v1' and rr.get('M')==M,'RECEIPTS_SCHEMA_OR_POINT')
 need(rr.get('core_manifest_sha256')==digest(corepath),'RECEIPTS_CORE_BINDING')
 if finite_terminal:need(rr.get('finite_core_sha256')==finitehash,'FINITE_RECEIPTS_BINDING')
 records=rr.get('spans',[]);need(isinstance(records,list) and len(records)==L and all(isinstance(x,dict) for x in records) and [x.get('l') for x in records]==list(range(1,L+1)),'RECEIPTS_COVERAGE')
 for e,rec in zip(entries,records):
  need(rec.get('status')=='COMPLETE_FROZEN_REPLAY_MATCH','RECEIPTS_INCOMPLETE')
  need(rec.get('input_sha256')==e['production'].get('sha256') and rec.get('output_sha256')==e['separate'].get('sha256'),'RECEIPTS_HASH_BINDING')
  need(rec.get('core_manifest_sha256')==digest(corepath),'SPAN_CORE_BINDING')
  expected_path='span_manifests/span_%d.json'%e['l'];need(rec.get('span_manifest_path')==expected_path,'SPAN_MANIFEST_PATH')
  sp=fp.parent/expected_path;need(sp.is_file(),'SPAN_MANIFEST_MISSING');need(digest(sp)==rec.get('span_manifest_sha256'),'SPAN_MANIFEST_SHA256')
  sm=read_json(sp,'SPAN_MANIFEST_JSON');need(sm.get('schema')=='c38-frozen-span-input-v1' and sm.get('l')==e['l'] and sm.get('M')==M,'SPAN_MANIFEST_PARAMETERS')
  need(sm.get('production_path')=='production/span_%d.json'%e['l'] and sm.get('production_sha256')==rec['input_sha256'] and sm.get('core_manifest_sha256')==digest(corepath),'SPAN_FROZEN_BINDING')
  last_finite=finite_terminal and e['l']==L
  if last_finite:need(sm.get('mode')==rec.get('mode')=='FINITE_LAST_SPAN_LOWER_ONLY' and sm.get('finite_core_sha256')==rec.get('finite_core_sha256')==finitehash,'FINITE_SPAN_BINDING')
  try:
   stamps=[cm['frozen_utc']]+([fc['frozen_utc']] if last_finite else [])+[sm['frozen_utc'],rec['replay_started_utc'],rec['replay_completed_utc']]
   times=[datetime.datetime.fromisoformat(x) for x in stamps]
   need(all(x.tzinfo is not None for x in times) and times==sorted(times),'FREEZE_REPLAY_ORDER')
  except (KeyError,TypeError,ValueError):raise Rejection('FREEZE_REPLAY_TIME_FORMAT')

 if full:
  need(binary is not None and work is not None,'FULL_REPLAY_ARGUMENTS')
  work=pathlib.Path(work);need(not work.exists(),'REPLAY_WORK_EXISTS');work.mkdir(parents=True)
 lows=[Fraction(0)]*(L+1);uppers=lows.copy();A0=lows.copy();A1=lows.copy();maxdeg=0;details=[]
 for e in entries:
  l=e['l'];finite=finite_terminal and l==L;w=integer(e.get('w'),'WIDTH');need(1<=w<=10000,'WIDTH')
  for key in ['production','separate']:
   item=e.get(key);need(isinstance(item,dict),'DATA_REFERENCE')
   p=root/item.get('path','');need(p.is_file(),'DATA_MISSING');need(digest(p)==item.get('sha256'),'DATA_SHA256')
  prod=read_json(root/e['production']['path'],'DATA_JSON');sep=read_json(root/e['separate']['path'],'DATA_JSON')
  need(prod.get('l')==l and sep.get('l')==l,'SPAN_METADATA')
  need(prod.get('w')==w and sep.get('w')==w,'WIDTH_METADATA')
  need(prod.get('S')==96 and sep.get('S')==96,'SCALE')
  need(sep.get('M')==M,'FUGACITY_METADATA')
  need(sep.get('F') in (12,44),'TAIL_SCALE')
  need(sep.get('status')=='COMPLETE_SEPARATE_SAME_AGENT_RECOMPUTATION','REPLAY_INCOMPLETE')
  if finite:
   need(prod.get('mode')==sep.get('mode')=='FINITE_LAST_SPAN_LOWER_ONLY' and prod.get('infinite_tail_certified') is False and sep.get('infinite_tail_certified') is False,'FINITE_MODE')
  else:need(prod.get('mode','FULL_WIDTH_CERTIFIED')==sep.get('mode','FULL_WIDTH_CERTIFIED')=='FULL_WIDTH_CERTIFIED','SPAN_MODE')
  need(isinstance(prod.get('x'),list),'POINT_COVERAGE');points=[x for x in prod['x'] if isinstance(x,dict) and x.get('Mnum')==M];need(len(points)==1,'POINT_COVERAGE');p=points[0]
  vals={}
  for field in ['num_lo','num_hi','num_tail']:
   pv=integer(p.get(field),'NUMERATOR_FORMAT');sv=integer(sep.get(field),'NUMERATOR_FORMAT')
   need(pv>=0 and sv>=0,'NEGATIVE_NUMERATOR');vals[field]=sv
   if field!='num_tail':need(pv==sv,'FINITE_NUMERATOR_MISMATCH')
  need(vals['num_lo']<=vals['num_hi'],'INVERTED_FINITE_BRACKET')
  if finite:need(vals['num_tail']==0 and integer(p.get('num_tail'),'NUMERATOR_FORMAT')==0,'FINITE_TAIL_MARKER')
  for field in ['total_states','edges']:
   need(type(prod.get(field)) is int and prod[field]>0,'GRAPH_COUNT')
   need(prod[field]==sep.get(field),'GRAPH_COUNT_MISMATCH')
  sizes=sep.get('stage_sizes');need(isinstance(sizes,list) and len(sizes)==l+1 and all(type(x)is int and x>0 for x in sizes),'STAGE_SIZES')
  need(sum(sizes)==sep['total_states'],'STAGE_COUNT_SUM')
  if full:
   log=work/('span_%d.log'%l);out=work/('span_%d.json'%l);exe=finite_binary if finite else binary;need(exe is not None,'FULL_FINITE_ARGUMENTS')
   with log.open('w') as f:
    command=[str(pathlib.Path(exe).resolve()),str(l),str(M),str(w),str(out),str(sep['F'])]
    child=subprocess.Popen(command,stdout=f,stderr=subprocess.STDOUT,start_new_session=True);ACTIVE_CHILD=child
    with (work/'CHILD_PIDS.jsonl').open('a') as record:record.write(json.dumps({'pid':child.pid,'span':l})+'\n')
    registry=os.environ.get('C38_REGISTER_PIDS_PATH')
    if registry:
     with pathlib.Path(registry).open('a') as record:record.write(json.dumps({'pid':child.pid,'args':command,'log':str(log),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
    code=child.wait();ACTIVE_CHILD=None
   need(code==0,'FULL_REPLAY_REJECTED')
   fresh=json.loads(out.read_text());need(fresh==sep,'FULL_REPLAY_MISMATCH')
  # Opposite order to search assembler: accumulate the upper/lower renewal
  # products first, then form the two final interval endpoints.
  D=1<<96; lows[l]=Fraction(vals['num_lo'],D);uppers[l]=Fraction(vals['num_hi']+vals['num_tail'],D)
  sum_upper=Fraction(0);sum_lower=Fraction(0)
  for k in reversed(range(1,l)):
   sum_upper+=uppers[k]*A1[l-k]
   sum_lower+=lows[k]*A0[l-k]
  A0[l]=max(Fraction(0),lows[l]-sum_upper)
  if finite:
   A1[l]=None;need(A0[l]<=uppers[l],'FINITE_RENEWAL_BRACKET')
  else:
   A1[l]=uppers[l]-sum_lower;need(0<=A0[l]<=A1[l],'RENEWAL_BRACKET')
  maxdeg=max(maxdeg,l*w);details.append({'l':l,'w':w,'mode':'FINITE_LAST_SPAN_LOWER_ONLY' if finite else 'FULL_WIDTH_CERTIFIED','finite_irreducible_lower':str(A0[l]),'full_irreducible_upper':str(A1[l]) if A1[l] is not None else None,'finite_irreducible_upper':str(uppers[l]) if finite else str(A1[l])})
 need(d.get('max_degree')==maxdeg,'DEGREE_BOUND')
 total=sum(A0,Fraction(0));need(total>=1,'RENEWAL_BELOW_ONE')
 mu=Fraction(1<<27,M);need(mu>Fraction(2**128,129513673858566230428673965530967449326) and mu>Fraction(1<<27,51082227),'PUBLIC_COMPARISON')
 need(d.get('P_lower')==str(total),'CLAIMED_SUM_MISMATCH')
 need(d.get('candidate_unrefereed') is True,'STATUS_LABEL')
 return {'status':'VERIFIED_CANDIDATE_UNREFEREED','packet_sha256':digest(path),'input_manifest_sha256':frozen['sha256'],'verification':'complete separately written (same agent) recomputation receipts; fresh full replay' if full else 'frozen complete separately written (same agent) recomputation receipts and exact assembly','L':L,'M':M,'terminal_span_mode':terminal,'mu':str(mu),'strictly_above_requested_Numaro_and_located_Planocka_fractions':True,'P_lower':str(total),'margin':str(total-1),'max_degree':maxdeg,'coefficients':'exact finite-class specification; expanded vector not materialized','spans':details}
if __name__=='__main__':
 signal.signal(signal.SIGTERM,stop_own_child);signal.signal(signal.SIGINT,stop_own_child)
 p=argparse.ArgumentParser();p.add_argument('packet');p.add_argument('--full',action='store_true');p.add_argument('--binary');p.add_argument('--finite-binary');p.add_argument('--work');p.add_argument('--receipt');a=p.parse_args()
 try:
  result=check(a.packet,a.full,a.binary,a.work,a.finite_binary)
  if a.receipt:pathlib.Path(a.receipt).write_text(json.dumps(result,indent=2)+'\n')
  print(result['status'])
 except Rejection as e:print('REJECT:'+str(e));sys.exit(2)

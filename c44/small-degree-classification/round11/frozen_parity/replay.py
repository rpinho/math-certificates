"""Replay the round-eleven frozen extension after unchanged inherited replay."""
import concurrent.futures,datetime,hashlib,json,os,pathlib,signal,subprocess,sys,threading,time
F=pathlib.Path(__file__).resolve().parent;R=F.parent
assert F.name=='frozen_parity' and os.getpriority(os.PRIO_PROCESS,0)>=10
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
O=R/'receipts/parity';O.mkdir(parents=True,exist_ok=True)
(R/'build').mkdir(exist_ok=True)
M=json.loads((F/'MANIFEST.json').read_text());BASE=json.loads((F/'BASELINE.json').read_text())
def hashes():
 assert {str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}==set(M['sha256'])|{'MANIFEST.json'}
 for name,digest in M['sha256'].items():assert hashlib.sha256((F/name).read_bytes()).hexdigest()==digest,name
def baseline():
 for name,digest in BASE['manifests'].items():
  path=R/name;assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
  m=json.loads(path.read_text());directory=path.parent
  assert {str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file()}==set(m['sha256'])|{'MANIFEST.json'}
  for rel,want in m['sha256'].items():assert hashlib.sha256((directory/rel).read_bytes()).hexdigest()==want,rel
 receipt=json.loads((R/'inherited/receipts/FINAL_RECEIPT.json').read_text());final=json.loads((R/'inherited/receipts/final/FINAL_RECEIPT.json').read_text())
 assert receipt['status']==final['status']=='PASS'
 assert final['bound']==BASE['bound']==json.loads((F/'caps.json').read_text())['previous_bound']
 assert receipt['manifest_sha256']==BASE['manifests']['inherited/frozen/MANIFEST.json']
 assert final['manifest_sha256']==BASE['manifests']['inherited/frozen_final/MANIFEST.json']
 accepted=json.loads((R/'receipts/accepted/FINAL_RECEIPT.json').read_text());assert accepted['status']=='PASS' and accepted['bound']==BASE['accepted_bound'] and accepted['manifest_sha256']==BASE['manifests']['frozen_accepted/MANIFEST.json']
hashes();baseline();ledger=dict(pid=os.getpid(),started=datetime.datetime.now(datetime.timezone.utc).isoformat(),steps=[]);active={};lock=threading.Lock()
def save():(O/'ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
def run(label,command,timeout):
 with (O/(label+'.log')).open('w') as output:
  child=subprocess.Popen(command,stdout=output,stderr=subprocess.STDOUT,start_new_session=True)
  row=dict(label=label,pid=child.pid,command=command,started=time.time())
  with lock:active[label]=child;ledger['steps'].append(row);save()
  try:code=child.wait(timeout=timeout)
  finally:
   if child.poll() is None:os.killpg(child.pid,signal.SIGTERM);child.wait(timeout=10)
  with lock:active.pop(label);row.update(code=code,seconds=time.time()-row['started']);save()
  assert code==0,(label,code)
def cleanup(signum=None,frame=None):
 for child in list(active.values()):
  if child.poll() is None:
   os.killpg(child.pid,signal.SIGTERM)
   try:child.wait(timeout=10)
   except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
 if signum is not None:raise KeyboardInterrupt
for signum in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):signal.signal(signum,cleanup)
try:
 run('compile_allmin',['g++','-O3','-std=c++17',str(F/'verify_allmin_a.cpp'),'-o',str(R/'build/verify_allmin_a')],120)
 run('compile_partial',['g++','-O3','-std=c++17',str(F/'verify_partial_a.cpp'),'-o',str(R/'build/verify_partial_a')],120)
 tasks=[]
 for index in range(15):
  for v in ('a','b'):
   cmd=[sys.executable,str(F/f'verify_partial_{v}.py'),str(F/'partial.json'),'--case',str(index)]
   if v=='a':cmd+=['--binary',str(R/'build/verify_partial_a')]
   tasks.append((f'partial_{v}_{index}',cmd,1800))
 for v in ('a','b'):
  cmd=[sys.executable,str(F/f'verify_partial_{v}.py'),str(F/'partial.json'),'--positive']
  if v=='a':cmd+=['--binary',str(R/'build/verify_partial_a')]
  tasks.append(('partial_positive_'+v,cmd,300))
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  futures=[pool.submit(run,*task) for task in tasks]
  for future in futures:future.result()
 run('partial_rejections',[sys.executable,str(F/'reject_partial.py'),str(F),str(O/'partial_rejections')],300)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  futures=[pool.submit(run,'verify_'+impl,[sys.executable,str(F/f'verify_{impl}.py'),str(F),'--out',str(O/f'verify_{impl}.json')],900) for impl in ('a','b')]
  for future in futures:future.result()
 run('rejections',[sys.executable,str(F/'reject_controls.py'),str(F),str(O/'rejections')],1800)
 hashes();baseline()
 a=json.loads((O/'verify_a.json').read_text());b=json.loads((O/'verify_b.json').read_text());reject=json.loads((O/'rejections/REJECTIONS.json').read_text())
 assert a['status']==b['status']==reject['status']=='PASS' and a['bound']==b['bound'] and reject['rejections']==96 and reject['positive_controls']==2
 partial_reject=json.loads((O/'partial_rejections/REJECTIONS.json').read_text());assert partial_reject['status']=='PASS' and partial_reject['rejections']==24
 packet=json.loads((F/'caps.json').read_text())
 receipt=dict(status='PASS',qualification='candidate, unrefereed; explicit published and inherited premises',bound=a['bound'],strict_claim=packet['strict_claim'],
  R5_upper=50,R6_upper=107,R7_upper=227,R8_upper=474,lower='3/2',artifact_rejections=120,manifest_sha256=hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),
  partial_cases=15,partial_positive_controls=2,scalar_positive_controls=2,artifact_sha256=a['artifact_sha256'],ended=datetime.datetime.now(datetime.timezone.utc).isoformat())
 receipt['partial_results']={f'{v}_{i}':json.loads((O/f'partial_{v}_{i}.log').read_text()) for i in range(15) for v in ('a','b')}
 receipt['partial_positives']={v:json.loads((O/f'partial_positive_{v}.log').read_text()) for v in ('a','b')}
 assert all(row['unsigned_leaves']==0 for row in receipt['partial_results'].values())
 assert all(row['unsigned_leaves']>0 for row in receipt['partial_positives'].values())
 assert a['artifact_sha256']==b['artifact_sha256']
 (O/'FINAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');ledger['status']='PASS';print(json.dumps(receipt),flush=True)
except BaseException:ledger['status']='FAILED';raise
finally:cleanup();ledger['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()

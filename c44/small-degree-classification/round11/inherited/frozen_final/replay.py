"""Replay the small immutable sign extension against the accepted baseline."""
import concurrent.futures,datetime,hashlib,json,os,pathlib,signal,subprocess,sys,time
F=pathlib.Path(__file__).resolve().parent;R=F.parent
assert F.name=='frozen_final' and os.getpriority(os.PRIO_PROCESS,0)>=10
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
O=R/'receipts/final';O.mkdir(parents=True,exist_ok=True)
M=json.loads((F/'MANIFEST.json').read_text());B=json.loads((F/'BASELINE.json').read_text())
def hashes(directory,manifest):
 actual={str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file()}
 assert actual==set(manifest['sha256'])|{'MANIFEST.json'}
 for name,want in manifest['sha256'].items():assert hashlib.sha256((directory/name).read_bytes()).hexdigest()==want,name
def baseline():
 directory=R/'frozen'
 assert hashlib.sha256((directory/'MANIFEST.json').read_bytes()).hexdigest()==B['manifest_sha256']
 hashes(directory,json.loads((directory/'MANIFEST.json').read_text()))
 receipt=R/'receipts/FINAL_RECEIPT.json'
 historical=F/'BASELINE_RECEIPT.json'
 assert hashlib.sha256(historical.read_bytes()).hexdigest()==B['receipt_sha256']
 live=json.loads(receipt.read_text());old=json.loads(historical.read_text())
 for key in ('status','manifest_sha256','bound','R5_upper','R6_upper','R7_upper'):
  assert live[key]==old[key],key
 assert json.loads(receipt.read_text())['status']=='PASS'
 assert json.loads((F/'certificates/caps.json').read_text())['previous_bound']==json.loads(receipt.read_text())['bound']
hashes(F,M);baseline();children={};ledger=dict(pid=os.getpid(),started=datetime.datetime.now(datetime.timezone.utc).isoformat(),steps=[])
def save():
 (O/'ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
def cleanup(signum=None,frame=None):
 for child in list(children.values()):
  if child.poll() is None:
   os.killpg(child.pid,signal.SIGTERM)
   try:child.wait(timeout=5)
   except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
 if signum is not None:raise KeyboardInterrupt
for signum in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):signal.signal(signum,cleanup)
def run(label,script,*arguments):
 with (O/(label+'.log')).open('w') as log:
  child=subprocess.Popen([sys.executable,str(F/script),*map(str,arguments)],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  children[label]=child;row=dict(label=label,pid=child.pid,started=time.time());ledger['steps'].append(row)
  try:code=child.wait(timeout=900)
  except subprocess.TimeoutExpired:
   os.killpg(child.pid,signal.SIGTERM);child.wait(timeout=10);code=child.returncode
  row.update(code=code,seconds=time.time()-row['started']);children.pop(label);assert code==0,(label,code)
try:
 run('sign_controls','control_signs.py')
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  tasks=[pool.submit(run,'verify_'+impl,'verify_'+impl+'.py',F) for impl in ('a','b')]
  for task in tasks:task.result()
 run('corruptions','reject_controls.py',F,O)
 hashes(F,M);baseline()
 a=json.loads((O/'verify_a.json').read_text());b=json.loads((O/'verify_b.json').read_text());c=json.loads((O/'rejection_controls.json').read_text())
 assert a['status']==b['status']==c['status']=='PASS' and a['bound']==b['bound'] and c['rejections']==40
 caps=json.loads((F/'certificates/caps.json').read_text())
 receipt=dict(status='PASS',qualification='candidate, unrefereed; explicit external premises',bound=a['bound'],strict_claim=caps['strict_claim'],R5_upper=50,R6_upper=107,R7_upper=229,lower='3/2',artifact_rejections=c['rejections'],manifest_sha256=hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),baseline_manifest=B['manifest_sha256'],ended=datetime.datetime.now(datetime.timezone.utc).isoformat())
 (O/'FINAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');ledger['status']='PASS';print(json.dumps(receipt),flush=True)
except BaseException:ledger['status']='FAILED';raise
finally:cleanup();ledger['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()

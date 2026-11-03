"""Frozen round-ten replay. All mutable output stays outside frozen/."""
import argparse,concurrent.futures,datetime,hashlib,json,os,pathlib,shutil,signal,subprocess,sys,time,threading
p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=4);p.add_argument('--replay',action='store_true');a=p.parse_args()
F=pathlib.Path(__file__).resolve().parent;R=F.parent
assert F.name=='frozen' and 1<=a.workers<=4 and os.getpriority(os.PRIO_PROCESS,0)>=10
os.chdir(R)
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
O=R/'receipts';O.mkdir(exist_ok=True);build=R/'build';build.mkdir(exist_ok=True)
manifest=json.loads((F/'MANIFEST.json').read_text())
def hashes():
 actual={str(x.relative_to(F)) for x in F.rglob('*') if x.is_file()}
 assert actual==set(manifest['sha256'])|{'MANIFEST.json'}
 for name,want in manifest['sha256'].items():assert hashlib.sha256((F/name).read_bytes()).hexdigest()==want,name
hashes();ledger=dict(pid=os.getpid(),started=datetime.datetime.now(datetime.timezone.utc).isoformat(),steps=[]);children={}
lock=threading.RLock()
def save():
 with lock:
  temporary=O/'round10_replay_ledger.tmp'
  temporary.write_text(json.dumps(ledger,indent=2)+'\n')
  temporary.replace(O/'round10_replay_ledger.json')
def run(label,command,timeout):
 with (O/(label+'.log')).open('w') as log:
  child=subprocess.Popen(list(map(str,command)),stdout=log,stderr=subprocess.STDOUT,start_new_session=True);children[label]=child
  row=dict(label=label,pid=child.pid,command=list(map(str,command)),started=time.time());ledger['steps'].append(row);save()
  try:code=child.wait(timeout=timeout)
  except subprocess.TimeoutExpired:
   os.killpg(child.pid,signal.SIGTERM)
   try:child.wait(timeout=5)
   except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
   code=child.returncode
  row.update(code=code,seconds=time.time()-row['started']);children.pop(label);save();assert code==0,(label,code)
def cleanup(signum=None,frame=None):
 for child in list(children.values()):
  if child.poll() is None:
   os.killpg(child.pid,signal.SIGTERM)
   try:child.wait(timeout=15)
   except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
 if signum is not None:raise KeyboardInterrupt
for s in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):signal.signal(s,cleanup)
try:
 # Replay inherited math only on a mutable hash-matched copy.
 B=R/'baseline_replay_copy';target=B/'frozen'
 if not target.exists():shutil.copytree(F/'baseline/frozen',target)
 for src in (F/'baseline/frozen').rglob('*'):
  if src.is_file():assert src.read_bytes()==(target/src.relative_to(F/'baseline/frozen')).read_bytes()
 run('baseline_replay',[sys.executable,target/'replay.py','--workers',a.workers,'--replay'],3600)
 assert json.loads((B/'receipts/FINAL_RECEIPT.json').read_text())['status']=='PASS'
 run('compile_near',['g++','-O3','-std=c++17',F/'control_near.cpp','-o',build/'control_near'],120)
 run('near_controls',[build/'control_near'],120)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  futures=[pool.submit(run,'round10_'+impl,[sys.executable,F/f'verify_{impl}.py',F],900) for impl in ('a','b')]
  for f in futures:f.result()
 run('corruptions',[sys.executable,F/'reject_controls.py',F,O],900)
 hashes()
 checks=[json.loads((O/f'verify_{impl}.json').read_text()) for impl in ('a','b')]
 assert all(c['status']=='PASS' for c in checks) and checks[0]['bound']==checks[1]['bound']
 negative=json.loads((O/'rejection_controls.json').read_text());assert negative['status']=='PASS' and negative['rejections']==30
 result=dict(status='PASS',qualification='candidate, unrefereed; explicit external premises',bound=checks[0]['bound'],strict_claim='2.0114439717',R5_upper=50,R6_upper=107,R7_upper=229,lower='3/2',artifact_rejections=30,manifest_sha256=hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),ended=datetime.datetime.now(datetime.timezone.utc).isoformat())
 (O/'FINAL_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
 ledger['status']='PASS';print(json.dumps(result),flush=True)
except BaseException:
 ledger['status']='FAILED';raise
finally:
 cleanup();ledger['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()

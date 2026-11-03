"""Frozen sampled lower seeds and exact rejection controls. No search imports."""
import copy,datetime,hashlib,json,os,pathlib,signal,subprocess,sys,tempfile,time
R=pathlib.Path(__file__).resolve().parent.parent;F=R/'frozen_lower';O=R/'receipts/lower';O.mkdir(exist_ok=True,parents=True)
assert os.getpriority(os.PRIO_PROCESS,0)>=10
M=json.loads((F/'MANIFEST.json').read_text());ledger=dict(pid=os.getpid(),started=datetime.datetime.now(datetime.timezone.utc).isoformat(),steps=[]);child=None
def hashes():
 assert {str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}==set(M['sha256'])|{'MANIFEST.json'}
 for name,want in M['sha256'].items():assert hashlib.sha256((F/name).read_bytes()).hexdigest()==want,name
def cleanup(signum=None,frame=None):
 if child is not None and child.poll() is None:
  os.killpg(child.pid,signal.SIGTERM);child.wait(timeout=10)
 if signum is not None:raise KeyboardInterrupt
for s in (signal.SIGTERM,signal.SIGHUP,signal.SIGINT):signal.signal(s,cleanup)
def run(impl,seed,output,want):
 global child
 with (O/'checks.log').open('a') as log:
  child=subprocess.Popen([sys.executable,str(F/f'verify_{impl}.py'),str(seed),str(output)],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  code=child.wait(timeout=120);ledger['steps'].append(dict(verifier=impl,input=str(seed),pid=child.pid,code=code,expected_success=want));child=None
  assert (code==0)==want
try:
 hashes();results=[]
 for seed in sorted((F/'seeds').glob('*.json')):
  for impl in ('a','b'):
   output=O/(seed.stem+'_'+impl+'.json');run(impl,seed,output,True);results.append(json.loads(output.read_text()))
 assert len(results)==8 and all(r['status']=='PASS' and r['lift']=='3/2' for r in results)
 original=json.loads(next((F/'seeds').glob('*.json')).read_text())
 mutations=[('count',lambda p:p.update(count=p['count']+1)),('degree',lambda p:p.update(target_degree=4)),('coefficient',lambda p:p['gates'][0]['terms'][0].__setitem__(1,65)),('denominator',lambda p:p['gates'][0].update(denominator=128)),('missing_gate',lambda p:p['gates'].pop()),('overlap',lambda p:p['gates'].append(copy.deepcopy(p['gates'][0]))),('used_mask',lambda p:p['gates'][0].update(used=0)),('false_lift',lambda p:p.update(asymptotic_lift='49/32'))]
 with tempfile.TemporaryDirectory(prefix='lower-controls-',dir=O) as tmp:
  temp=pathlib.Path(tmp)
  for label,mutate in mutations:
   obj=copy.deepcopy(original);mutate(obj);path=temp/(label+'.json');path.write_text(json.dumps(obj))
   for impl in ('a','b'):run(impl,path,temp/'unused.json',False)
 hashes();receipt=dict(status='PASS',qualification='candidate, unrefereed; known seeds only',seeds=4,verifications=8,rejections=16,best_lift='3/2',manifest_sha256=hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),ended=datetime.datetime.now(datetime.timezone.utc).isoformat())
 (O/'FINAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');ledger['status']='PASS';print(json.dumps(receipt),flush=True)
except BaseException:ledger['status']='FAILED';raise
finally:cleanup();(O/'ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')

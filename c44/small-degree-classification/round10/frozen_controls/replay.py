"""Auxiliary frozen controls. No accepted upper-bound arithmetic changes."""
import copy,datetime,hashlib,json,os,pathlib,signal,subprocess,sys,tempfile,time
F=pathlib.Path(__file__).resolve().parent;R=F.parent;O=R/'receipts/aux_controls';O.mkdir(parents=True,exist_ok=True);build=R/'build';build.mkdir(exist_ok=True)
assert F.name=='frozen_controls' and os.getpriority(os.PRIO_PROCESS,0)>=10
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
M=json.loads((F/'MANIFEST.json').read_text());binding=json.loads((F/'CATALOGUE.json').read_text());source=R/binding['path'];child=None
ledger=dict(pid=os.getpid(),started=datetime.datetime.now(datetime.timezone.utc).isoformat(),steps=[])
def hashes():
 assert {str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}==set(M['sha256'])|{'MANIFEST.json'}
 for name,want in M['sha256'].items():assert hashlib.sha256((F/name).read_bytes()).hexdigest()==want,name
 assert hashlib.sha256(source.read_bytes()).hexdigest()==binding['sha256']
def cleanup(signum=None,frame=None):
 if child is not None and child.poll() is None:
  os.killpg(child.pid,signal.SIGTERM)
  try:child.wait(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
 if signum is not None:raise KeyboardInterrupt
for signum in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):signal.signal(signum,cleanup)
def run(label,command,success=True):
 global child
 child=subprocess.Popen(list(map(str,command)),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True);row=dict(label=label,pid=child.pid,command=list(map(str,command)),started=time.time())
 try:out,error=child.communicate(timeout=300)
 except subprocess.TimeoutExpired:cleanup();raise
 code=child.returncode;row.update(code=code,seconds=time.time()-row['started']);ledger['steps'].append(row);child=None
 (O/(label+'.log')).write_text(out+error)
 assert (code==0)==success,(label,code)
 if not success:assert 'AssertionError' in error or 'Assertion' in error
try:
 hashes()
 for label,src in [('count','search_gate_cliques.cpp'),('potential','search_potential_cliques.cpp'),('cubic','cubic_stats_b.cpp')]:
  run('compile_'+label,['g++','-O3','-std=c++17',F/src,'-o',build/('aux_'+label)])
 for impl in ('a','b'):run('seed_'+impl,[sys.executable,F/f'verify_seed_{impl}.py',F/'seed36.json',O/('seed_'+impl+'.json')])
 for variant in ('count','potential'):
  for threshold in (36,37):
   result=O/(variant+'_'+str(threshold)+'.json');run(variant+'_'+str(threshold),[build/('aux_'+variant),F/('bank_'+variant+'.txt'),result,'60',str(threshold)])
   data=json.loads(result.read_text());assert data['status']==('PARTITION_FOUND' if threshold==36 else 'FINITE_BANK_NO_MATCH')
   if threshold==36:assert data['best_'+('count' if variant=='count' else 'potential_units')]==36
 run('cubic_a',[sys.executable,F/'cubic_stats_a.py',source,O/'cubic_a.json'])
 run('cubic_b',[build/'aux_cubic',source,O/'cubic_b.json'])
 assert json.loads((O/'cubic_a.json').read_text())==json.loads((O/'cubic_b.json').read_text())
 with tempfile.TemporaryDirectory(prefix='aux-controls-',dir=O) as directory:
  T=pathlib.Path(directory);original=json.loads((F/'seed36.json').read_text())
  for label in ('count','coefficient'):
   obj=copy.deepcopy(original)
   if label=='count':obj['count']+=1
   else:obj['gates'][0]['terms'][0][1]+=1
   artifact=T/(label+'.json');artifact.write_text(json.dumps(obj))
   for impl in ('a','b'):run('reject_seed_'+label+'_'+impl,[sys.executable,F/f'verify_seed_{impl}.py',artifact,T/'unused.json'],False)
  raw=source.read_text();lines=raw.splitlines()
  for label,text in [('flip',('1' if raw[0]=='0' else '0')+raw[1:]),('omit','\n'.join(lines[1:])+'\n')]:
   artifact=T/(label+'.txt');artifact.write_text(text)
   run('reject_cubic_'+label+'_a',[sys.executable,F/'cubic_stats_a.py',artifact,T/'unused_a.json'],False)
   run('reject_cubic_'+label+'_b',[build/'aux_cubic',artifact,T/'unused_b.json'],False)
 hashes();result=dict(status='PASS',qualification='candidate, unrefereed auxiliary controls, no new R5 or lower bound',seed_checks=2,graph_controls=4,catalogue_checks=2,rejection_outcomes=8,manifest_sha256=hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),ended=datetime.datetime.now(datetime.timezone.utc).isoformat())
 (O/'FINAL_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');ledger['status']='PASS';print(json.dumps(result),flush=True)
except BaseException:ledger['status']='FAILED';raise
finally:cleanup();ledger['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(O/'ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')

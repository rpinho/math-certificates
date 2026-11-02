"""Sequential exact replay on the frozen artifact; resource and PID audit."""
import datetime,hashlib,json,os,pathlib,resource,subprocess,sys,time
R=pathlib.Path(__file__).resolve().parent.parent;F=R/'frozen';O=R/'receipts'
os.chdir(R);O.mkdir(exist_ok=True)
resource.setrlimit(resource.RLIMIT_AS,(40_000_000_000,40_000_000_000));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[key]='1'
assert os.getpriority(os.PRIO_PROCESS,0)>=10
manifest=json.loads((F/'MANIFEST.json').read_text())
def hashes():
 for name,digest in manifest['sha256'].items():assert hashlib.sha256((F/name).read_bytes()).hexdigest()==digest,name
hashes()
ledger={'runner_pid':os.getpid(),'nice':os.getpriority(os.PRIO_PROCESS,0),'memory_limit_bytes':40_000_000_000,'workers':1,'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'steps':[]}
def save():(O/'frozen_replay_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
steps=[('quartic_a',[sys.executable,str(F/'verify_quartic_a.py'),str(F)]),
 ('quartic_b',[sys.executable,str(F/'verify_quartic_b.py'),str(F)]),
 ('quintic_a',[sys.executable,str(F/'verify_quintic_a.py'),str(F)]),
 ('quintic_b',[sys.executable,str(F/'verify_quintic_b.py'),str(F)]),
 ('quintic13_a',[sys.executable,str(F/'verify_quintic13_a.py'),str(F)]),
 ('quintic13_b',[sys.executable,str(F/'verify_quintic13_b.py'),str(F)]),
 ('scalar_a',[sys.executable,str(F/'verify_scalar_a.py'),str(F)]),
 ('scalar_b',[sys.executable,str(F/'verify_scalar_b.py'),str(F)]),
 ('sparse_controls',[sys.executable,str(F/'verify_controls.py'),str(F)]),
 ('integer_gap_compile',['g++','-O3','-std=c++17',str(F/'control_integer_gap.cpp'),'-o',str(R/'control_integer_gap_frozen')]),
 ('integer_gap_control',[str(R/'control_integer_gap_frozen')]),
 ('corruptions',[sys.executable,str(F/'corruption_checks.py')])]
try:
 for label,args in steps:
  assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime(2026,11,2,3,3,tzinfo=datetime.timezone.utc)
  with (O/('frozen_'+label+'.log')).open('w') as f:
   p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT);row={'label':label,'pid':p.pid,'command':args,'started':datetime.datetime.now(datetime.timezone.utc).isoformat()};ledger['steps'].append(row);save();start=time.monotonic()
   try:code=p.wait(timeout=1200)
   finally:
    if p.poll() is None:p.terminate();p.wait()
  row.update(code=code,seconds=time.monotonic()-start);save();print(label,code,row['seconds'],flush=True);assert code==0,label
 hashes();ledger['status']='PASS'
finally:
 ledger['utc_end']=datetime.datetime.now(datetime.timezone.utc).isoformat();ledger['peak_child_rss_KiB']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss;save()

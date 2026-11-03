"""Sequential, bounded replay. Run under nice 10 on the authorized compute pod."""
from pathlib import Path
import datetime,hashlib,json,os,resource,subprocess,sys,time
R=Path(__file__).resolve().parent
os.chdir(R)
resource.setrlimit(resource.RLIMIT_AS,(40*1024**3,40*1024**3))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
    os.environ[name]='1'
assert os.getpriority(os.PRIO_PROCESS,0)>=10
manifest=json.loads((R/'MANIFEST.json').read_text())
def check_hashes():
    for path,sha in manifest.items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==sha,path
check_hashes()
commands=[['g++','-O3','-std=c++17','verify_catalogue.cpp','-o','verify_catalogue'],
          ['g++','-O3','-std=c++17','control_pair_lemma.cpp','-o','control_pair_lemma'],
          ['python3','explore_catalogue.py'],
          ['python3','baseline/c44r5/control_witnesses.py'],
          ['./control_pair_lemma'],['python3','control_constructions.py'],
          ['python3','control_rejections.py'],['python3','derive_bound.py','--check'],
          ['python3','verify_packet.py','72'],['python3','verify_packet.py','96']]
ledger={'supervisor_pid':os.getpid(),'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'max_concurrent_direct_workers':1,'memory_limit_bytes':40*1024**3,'nice':os.getpriority(os.PRIO_PROCESS,0),'processes':[]}
def save():
    (R/'PROCESS_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
save()
for index,cmd in enumerate(commands):
    log=R/f'replay_{index:02d}.log';start=time.monotonic()
    with log.open('w') as f:
        p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
        rec={'pid':p.pid,'command':cmd,'log':log.name,'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        ledger['processes'].append(rec);save()
        try:code=p.wait(timeout=1200)
        except BaseException:
            p.terminate();p.wait();raise
    rec.update(exit_code=code,seconds=time.monotonic()-start);save()
    print(json.dumps({'command':cmd,'pid':p.pid,'exit_code':code,'seconds':rec['seconds']}),flush=True)
    assert code==0,log.name
check_hashes()
ledger['utc_end']=datetime.datetime.now(datetime.timezone.utc).isoformat()
ledger['max_child_RSS_KiB']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
ledger['status']='PASS';save()
(R/'FINAL_RECEIPT.json').write_text(json.dumps({'status':'PASS','utc':ledger['utc_end'],
    'manifest_sha256':hashlib.sha256((R/'MANIFEST.json').read_bytes()).hexdigest(),
    'static_files':len(manifest),'R4':22,'R5_upper':53,'C44_upper':'3.1498761303',
    'verification':'independent character sums, structure arithmetic, polynomial convolution, rational columns',
    'external_completeness':'Rasoolzadeh published cubic classification',
    'status_qualification':'candidate, unrefereed; written proof is not mechanized'},indent=2)+'\n')
print('ALL CHECKS PASS',flush=True)

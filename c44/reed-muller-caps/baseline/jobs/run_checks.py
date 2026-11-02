"""Sequential pod replay; bounded memory, tracked children, no detached workers."""
import datetime,json,os,resource,signal,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent.parent
os.chdir(R)
assert os.getpriority(os.PRIO_PROCESS,0)>=10
resource.setrlimit(resource.RLIMIT_AS,(40*1024**3,40*1024**3))
steps=[
 ('rows',['python3','verify_rows.py','candidate.json']),
 ('independent72',['python3','verify_exact.py','candidate.json','72']),
 ('independent96',['python3','verify_exact.py','candidate.json','96']),
 ('structure_cases',['python3','verify_structure_cases.py']),
 ('templates',['python3','make_structure_templates.py']),
 ('compile',['g++','-std=c++17','-O3','control_gap.cpp','-o','control_gap']),
 ('gap',['./control_gap']),
 ('witnesses',['python3','control_witnesses.py']),
 ('rejections',['python3','control_rejections.py']),
 ('receipt',['python3','make_receipt.py'])]
ledger={'runner_pid':os.getpid(),'nice':os.getpriority(os.PRIO_PROCESS,0),
 'memory_limit_bytes':40*1024**3,'concurrent_workers':1,
 'threads':{k:os.environ[k] for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']},
 'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'steps':[]}
for label,cmd in steps:
    start=time.monotonic()
    with (R/(label+'.log')).open('w') as log:
        child=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        step={'label':label,'pid':child.pid,'command':cmd,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        ledger['steps'].append(step)
        (R/'PROCESS_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
        try:rc=child.wait(timeout=600)
        except BaseException:
            os.killpg(child.pid,signal.SIGTERM)
            try:child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid,signal.SIGKILL);child.wait()
            raise
    step.update(returncode=rc,elapsed_seconds=time.monotonic()-start,
                cumulative_max_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    if label=='gap' and rc==0:
        (R/'control_gap.json').write_bytes((R/'gap.log').read_bytes())
    (R/'PROCESS_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
    assert rc==0,(label,rc)
    print(label,'PASS',round(step['elapsed_seconds'],3),flush=True)
ledger['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
ledger['status']='PASS'
(R/'PROCESS_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')

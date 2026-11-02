"""One sequential worker; inherited nice 10 and a 40 GB address-space cap."""
import datetime,os,pathlib,json,subprocess,resource,time
R=pathlib.Path(__file__).resolve().parent.parent
os.chdir(R)
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
    os.environ[key]='1'
resource.setrlimit(resource.RLIMIT_AS,(40_000_000_000,40_000_000_000))
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def manifest_check():
    name=R/'MANIFEST.json'
    if name.exists():
        import hashlib
        for file,digest in json.loads(name.read_text())['sha256'].items():
            assert hashlib.sha256((R/file).read_bytes()).hexdigest()==digest,file
manifest_check()
ledger={'runner_pid':os.getpid(),'nice':os.getpriority(os.PRIO_PROCESS,0),'workers':1,
        'memory_limit_bytes':40_000_000_000,'started':utc(),'steps':[]}
assert ledger['nice']>=10
steps=[('check_a',['python3','verify_caps_a.py']),('check_b',['python3','verify_caps_b.py']),
       ('compile',['g++','-O3','-std=c++17','control_ternary.cpp','-o','control_ternary']),
       ('ternary',['./control_ternary']),
       ('compile_boolean',['g++','-O3','-std=c++17','control_boolean.cpp','-o','control_boolean']),
       ('boolean',['./control_boolean']),('analysis',['python3','analyze.py']),
       ('corruption',['python3','control_corruption.py'])]
try:
    for label,args in steps:
        start=time.monotonic()
        with open(label+'.log','w') as out:
            child=subprocess.Popen(args,stdout=out,stderr=subprocess.STDOUT)
            row={'label':label,'pid':child.pid,'command':args,'started':utc()}
            ledger['steps'].append(row)
            (R/'PROCESS_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
            try:rc=child.wait()
            finally:
                if child.poll() is None:child.terminate();child.wait()
        row.update(returncode=rc,elapsed_seconds=time.monotonic()-start,
                   peak_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        (R/'PROCESS_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
        print(label,rc,round(row['elapsed_seconds'],3),flush=True)
        assert rc==0,label
    manifest_check()
    ledger['status']='PASS'
finally:
    ledger['ended']=utc()
    (R/'PROCESS_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')

"""Bounded job-owned process supervisor. No mathematical acceptance role."""
import concurrent.futures, datetime, json, os, pathlib, resource, signal, subprocess, sys, threading, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)
assert os.getpriority(os.PRIO_PROCESS, 0) >= 10
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
plan = json.loads(pathlib.Path(sys.argv[1]).read_text())
workers = int(plan.get('workers', 1))
assert 1 <= workers <= 14
deadline = datetime.datetime(2026, 11, 3, 11, 35, tzinfo=datetime.timezone.utc).timestamp()
if '--replay' in sys.argv:
    deadline = time.time() + 10 * 3600
ledger = {'supervisor_pid': os.getpid(), 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'workers': workers, 'steps': []}
record = ROOT / 'receipts' / (plan['label'] + '_ledger.json')
record.parent.mkdir(exist_ok=True)
lock = threading.Lock()
active = {}
stopping = threading.Event()
def save():
    temporary = record.with_suffix('.tmp')
    temporary.write_text(json.dumps(ledger, indent=2) + '\n')
    temporary.replace(record)
def cleanup(signum=None, frame=None):
    stopping.set()
    with lock:
        children = list(active.values())
    for child in children:
        if child.poll() is None:
            try: os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError: pass
    if signum is not None:
        raise KeyboardInterrupt
for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(sig, cleanup)
def run(task):
    if stopping.is_set() or time.time() >= deadline:
        return {'label': task['label'], 'status': 'SKIPPED_DEADLINE'}
    command = task['command']
    row = {'label': task['label'], 'command': command, 'started': time.time(), 'timeout': task.get('timeout', 3600)}
    logpath = ROOT / 'receipts' / (plan['label'] + '_' + task['label'] + '.log')
    # A shell wrapper sets per-child address-space limits without preexec_fn
    # (which is unsafe in this threaded supervisor). Only own commands run.
    limit = int(task.get('memory_mb', 6000)) * 1024
    args = ['bash', '-c', 'ulimit -v "$1"; shift; exec "$@"', 'c44-limit', str(limit), *command]
    with logpath.open('w') as log:
        child = subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        with lock:
            active[task['label']] = child
            row['pid'] = child.pid
            ledger['steps'].append(row)
            save()
        try:
            row['code'] = child.wait(timeout=max(1, min(row['timeout'], deadline-time.time())))
            row['status'] = 'PASS' if row['code'] == 0 else 'FAILED'
        except subprocess.TimeoutExpired:
            row['status'] = 'TIMEOUT'
        finally:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGTERM)
                try: child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
            with lock:
                active.pop(task['label'], None)
                row['code'] = child.returncode
                row['seconds'] = time.time()-row['started']
                save()
        print(json.dumps(row), flush=True)
        return row
save()
try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(run, plan['tasks']))
    ledger['status'] = 'PASS' if all(r['status']=='PASS' for r in results) else 'INCOMPLETE'
finally:
    cleanup()
    ledger['ended_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save()

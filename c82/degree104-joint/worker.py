"""Run single-threaded job workers, track descendant memory, process groups and CPU."""
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
LOG = ROOT / 'logs'
START = (ROOT / 'STATUS.md').stat().st_birthtime
LIMIT = START + 36000
running = {}
def launch(label, args):
    out = (LOG / (label + '.log')).open('w')
    proc = subprocess.Popen(['/usr/bin/time','-l','./run_local.sh',*map(str,args)], stdout=out, stderr=out, start_new_session=True)
    out.close()
    running[proc.pid] = (proc, label)
    with open('evidence/pids.jsonl','a') as f:
        print(json.dumps(dict(pid=proc.pid,kind=label,time=time.time())),file=f)
    return proc

def stop(proc):
    try: os.killpg(proc.pid,signal.SIGTERM)
    except ProcessLookupError: pass

def run(jobs):
    procs = [launch(label,args) for label,args in jobs]
    maximum = 0
    try:
        while any(p.poll() is None for p in procs):
            if time.time() > LIMIT-60: raise TimeoutError('10 hour limit')
            rows=subprocess.check_output(['ps','-axo','pgid=,rss='],text=True)
            total=sum(int(r[1])*1024 for line in rows.splitlines() if len(r:=line.split())==2 and int(r[0]) in running)
            maximum=max(maximum,total)
            if total >= 2_800_000_000:
                stop(next(p for p in reversed(procs) if p.poll() is None))
                raise MemoryError(str(total))
            time.sleep(1)
        for p in procs:
            if p.returncode: raise RuntimeError(f'{running[p.pid][1]} exit {p.returncode}')
    finally:
        for p in procs:
            if p.poll() is None: stop(p)
            p.wait()
            running.pop(p.pid)
        with open('evidence/resources.jsonl','a') as f:
            print(json.dumps(dict(labels=[k for k,a in jobs],peak_group_bytes=maximum,time=time.time())),file=f)
if __name__=='__main__':
    run([(k,['verify.py','--certificate','inputs/'+k+'.json','--sha',sha,'--target',target,'--tol','1e-13','--out','evidence/'+k+'.json']) for k,sha,target in [('v6','29dcbf21a10ddb600a9866fe8ee7e7b43e4357926d74f374a8b6fbf41ada71b5','0.2519694883'),('round11','250c5b56566d93f82a476d370df53af6aadf5affad2f96b0a7728e7afc298c83','0.2519695579')]])

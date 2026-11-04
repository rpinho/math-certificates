"""Run only the referee's independent executable; six workers, explicit PID log."""
import concurrent.futures as cf
import datetime
import json
import os
import pathlib
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parent
WIDTHS = [0,41,62,82,103,125,146,168,189,212,234]
TASKS = [(h, WIDTHS[h], m, 'exact', f'{name}{h}')
         for h in range(10,0,-1) for name,m in [('b',51081913),('c',51082227)]]
TASKS += [(h,40,51081913,'coeff',f'count{h}') for h in range(10,0,-1)]

def run(task):
    h,w,m,mode,name = task
    start=time.time()
    command=['nice','-n','10',str(ROOT/'independent_tm'),str(h),str(w),str(m),mode,
             str(ROOT/'results'/f'{name}.json')]
    with (ROOT/'results'/f'{name}.log').open('w') as log:
        p=subprocess.Popen(command,stdout=log,stderr=log)
        with (ROOT/'results'/'PIDS.jsonl').open('a') as f:
            f.write(json.dumps({'pid':p.pid,'command':command,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
        try:
            rc=p.wait(timeout=10800)
        except subprocess.TimeoutExpired:
            p.terminate()
            try: p.wait(timeout=10)
            except subprocess.TimeoutExpired: p.kill();p.wait()
            rc='TIMEOUT'
    receipt={'name':name,'returncode':rc,'seconds':time.time()-start}
    print(json.dumps(receipt),flush=True)
    return receipt

if __name__=='__main__':
    with cf.ThreadPoolExecutor(max_workers=min(6,int(os.environ.get('REFEREE_WORKERS','6')))) as pool:
        receipts=list(pool.map(run,TASKS))
    (ROOT/'results'/'BATCH.json').write_text(json.dumps(receipts,indent=2)+'\n')

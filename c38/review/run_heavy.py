"""Independent extension and rectangle jobs, at most six single-core workers."""
import concurrent.futures as cf
import json
import os
import pathlib
import subprocess
import time
ROOT=pathlib.Path(__file__).resolve().parent
tasks=[]
for w,hi in [(22,30),(23,18)]:
    tasks.append((f'rectangle{w}',['./independent_rectangle',str(w),'18',str(hi),'5']))
for h,w in [(12,280),(11,257)]:
    for name,m in [('b',51081913),('c',51082227)]:
        tasks.append((f'{name}{h}',['./independent_tm',str(h),str(w),str(m),'exact']))
for h in [11,12]: tasks.append((f'count{h}',['./independent_tm',str(h),'40','51081913','coeff']))
def run(task):
    name,cmd=task;start=time.time();cmd+=['results/'+name+'.json']
    with (ROOT/'results'/f'{name}.log').open('w') as log:
        p=subprocess.Popen(cmd,cwd=ROOT,stdout=log,stderr=log)
        with (ROOT/'results'/'HEAVY_PIDS.jsonl').open('a') as f:f.write(json.dumps({'pid':p.pid,'cmd':cmd,'started':start})+'\n')
        try:rc=p.wait(timeout=10200)
        except subprocess.TimeoutExpired:
            p.terminate()
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:p.kill();p.wait()
            rc='TIMEOUT'
    r={'name':name,'returncode':rc,'seconds':time.time()-start}
    print(json.dumps(r),flush=True);return r
with cf.ThreadPoolExecutor(max_workers=min(6,int(os.environ.get('REFEREE_WORKERS','6')))) as executor:
    receipts=list(executor.map(run,tasks))
(ROOT/'results'/'HEAVY_BATCH.json').write_text(json.dumps(receipts,indent=2)+'\n')

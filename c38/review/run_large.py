"""Use two worker slots for spans 14 and 15, with a bounded common deadline."""
import concurrent.futures as cf
import datetime
import json
import pathlib
import os
import subprocess
import time
root=pathlib.Path(__file__).resolve().parent
deadline=time.time()+float(os.environ.get('REFEREE_LARGE_TIMEOUT_SECONDS','10000'))
tasks=[(h,w,name,m) for h,w in [(14,327),(15,351)] for name,m in [('b',51081913),('c',51082227)]]
def run(task):
    h,w,name,m=task;start=time.time();remaining=deadline-start
    if remaining<60:return {'name':name,'span':h,'returncode':'NOT_STARTED_DEADLINE'}
    command=['./independent_interval_large',str(h),str(w),str(m),f'results/{name}{h}_interval.json']
    with open(root/f'results/{name}{h}_interval.log','w') as log:
        p=subprocess.Popen(command,cwd=root,stdout=log,stderr=log)
        with open(root/'results/LARGE_PIDS.jsonl','a') as f:f.write(json.dumps({'pid':p.pid,'command':command})+'\n')
        try:rc=p.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            p.terminate()
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:p.kill();p.wait()
            rc='TIMEOUT'
    result={'name':name,'span':h,'returncode':rc,'seconds':time.time()-start}
    print(json.dumps(result),flush=True);return result
if __name__=='__main__':
    with cf.ThreadPoolExecutor(max_workers=2) as pool:receipts=list(pool.map(run,tasks))
    (root/'results/LARGE_BATCH.json').write_text(json.dumps(receipts,indent=2)+'\n')

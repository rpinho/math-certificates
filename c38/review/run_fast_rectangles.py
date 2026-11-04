import concurrent.futures as cf
import json
import pathlib
import subprocess
import time
root=pathlib.Path(__file__).resolve().parent
def run(W):
    start=time.time();command=['./independent_rectangle_fast',str(W),'18',str(30 if W==22 else 18),'5',f'results/rectangle{W}_fast.json']
    with open(root/f'results/rectangle{W}_fast.log','w') as log:
        p=subprocess.Popen(command,cwd=root,stdout=log,stderr=log)
        with open(root/'results/FAST_RECT_PIDS.jsonl','a') as f:f.write(json.dumps({'pid':p.pid,'command':command})+'\n')
        try:rc=p.wait(timeout=8400)
        except subprocess.TimeoutExpired:
            p.terminate()
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:p.kill();p.wait()
            rc='TIMEOUT'
    result={'W':W,'returncode':rc,'seconds':time.time()-start}
    print(json.dumps(result),flush=True);return result
with cf.ThreadPoolExecutor(max_workers=2) as pool:receipts=list(pool.map(run,[22,23]))
(root/'results/FAST_RECT_BATCH.json').write_text(json.dumps(receipts,indent=2)+'\n')

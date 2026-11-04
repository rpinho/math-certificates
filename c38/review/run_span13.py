import concurrent.futures as cf
import json
import pathlib
import subprocess
import time
root=pathlib.Path(__file__).resolve().parent
def run(pair):
    name,m=pair;start=time.time()
    command=['./independent_interval','13','303',str(m),f'results/{name}13_interval.json']
    with open(root/f'results/{name}13_interval.log','w') as log:
        p=subprocess.Popen(command,cwd=root,stdout=log,stderr=log)
        with open(root/'results/SPAN13_PIDS.jsonl','a') as f:f.write(json.dumps({'pid':p.pid,'command':command})+'\n')
        try:rc=p.wait(timeout=10000)
        except subprocess.TimeoutExpired:
            p.terminate()
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:p.kill();p.wait()
            rc='TIMEOUT'
    result={'name':name,'returncode':rc,'seconds':time.time()-start}
    print(json.dumps(result),flush=True);return result
with cf.ThreadPoolExecutor(max_workers=2) as pool:receipts=list(pool.map(run,[('b',51081913),('c',51082227)]))
(root/'results/SPAN13_BATCH.json').write_text(json.dumps(receipts,indent=2)+'\n')

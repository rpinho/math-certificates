"""Required resource supervision: <=3 GB together, tracked children and timing."""
import json,os,resource,subprocess,sys,time
from pathlib import Path
CAP=3_000_000_000

def snapshot():
    rows={}
    for line in subprocess.check_output(['ps','-axo','pid=,ppid=,rss='],text=True).splitlines():
        pid,ppid,rss=map(int,line.split());rows[pid]=(ppid,rss*1024)
    included={os.getpid()}
    while True:
        more={pid for pid,(parent,rss) in rows.items() if parent in included}
        if more<=included:break
        included|=more
    return {pid:rows[pid][1] for pid in included if pid in rows}

def run(args,log):
    start=time.monotonic();before=resource.getrusage(resource.RUSAGE_CHILDREN)
    with open(log,'w') as out,open(log+'.time','w') as timing:
        p=subprocess.Popen(['/usr/bin/time','-l',sys.executable,*args],stdout=out,stderr=timing)
        with open('evidence/pids.jsonl','a') as f:f.write(json.dumps({'pid':p.pid,'args':args,'kind':'supervised_time'})+'\n')
        peak=0;cut=False
        while p.poll() is None:
            rss=snapshot();total=sum(rss.values());peak=max(peak,total)
            if total>CAP-150_000_000:
                cut=True
                # Stop newest computational child before aggregate reaches 3 GB.
                for pid in sorted(rss,reverse=True):
                    if pid not in [os.getpid(),p.pid]:
                        try:os.kill(pid,15)
                        except ProcessLookupError:pass
                with open('STATUS.md','a') as f:f.write(f'\nResource failure: {args}, aggregate RSS {total} bytes reached safety stop below 3 GB. Log {log}; previous certified packet unchanged.\n')
                break
            time.sleep(.15)
        code=p.wait()
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    rec={'args':args,'pid':p.pid,'exit_code':code,'resource_stop':cut,'wall_seconds':time.monotonic()-start,'cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,'sampled_aggregate_peak_bytes':peak}
    with open('evidence/compute.jsonl','a') as f:f.write(json.dumps(rec)+'\n')
    print(json.dumps(rec),flush=True)
    if code:raise RuntimeError(f'{args} failed ({code}); see {log}')
    return rec
if __name__=='__main__':run(sys.argv[2:],sys.argv[1])

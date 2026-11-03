"""Bound each child run to <= 29 minutes and retain process receipts."""
import argparse, datetime, json, os, pathlib, signal, subprocess, time

p=argparse.ArgumentParser()
p.add_argument('--seconds', type=int, default=1740)
p.add_argument('--log', required=True)
p.add_argument('command', nargs=argparse.REMAINDER)
a=p.parse_args()
if not 0 < a.seconds <= 1740: raise SystemExit('run limit must be <= 1740 seconds')
cmd=a.command
if cmd and cmd[0]=='--': cmd=cmd[1:]
if not cmd: raise SystemExit('missing command')
root=pathlib.Path(__file__).resolve().parent
log=root/a.log
log.parent.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',
         VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
start=time.monotonic()
with log.open('w') as stream:
    child=subprocess.Popen(['nice','-n',str(max(0,10-os.getpriority(os.PRIO_PROCESS,0))),*cmd],cwd=root,env=env,
                            stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
    receipt={'pid':child.pid,'command':cmd,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'limit_seconds':a.seconds,'log':str(log.relative_to(root))}
    with (root/'processes.jsonl').open('a') as f: f.write(json.dumps(receipt)+'\n')
    try:
        rc=child.wait(timeout=a.seconds)
    except subprocess.TimeoutExpired:
        os.killpg(child.pid,signal.SIGTERM)
        try: child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGKILL); child.wait()
        rc=124
    except BaseException:
        os.killpg(child.pid,signal.SIGTERM)
        child.wait(timeout=5)
        raise
receipt.update(exit=rc,elapsed_seconds=time.monotonic()-start)
with (root/'processes.jsonl').open('a') as f: f.write(json.dumps(receipt)+'\n')
print(json.dumps(receipt))
raise SystemExit(rc)

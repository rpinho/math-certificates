"""One sequential checker worker, <=1600 seconds per controller epoch."""
import argparse,datetime,fcntl,json,os,pathlib,signal,subprocess,time
from verify_c57c_forest import code_hashes
p=argparse.ArgumentParser();p.add_argument('--queue',default='ARITH_QUEUE.json');p.add_argument('--seconds',type=int,default=1600);a=p.parse_args();assert 0<a.seconds<=1600
ROOT=pathlib.Path(__file__).resolve().parent;os.chdir(ROOT);queue=ROOT/a.queue;lock=queue.with_suffix('.lock');begun=time.monotonic();STOP=False;child=None;codes=code_hashes()
def stop(signum,frame):
 global STOP;STOP=True
 if child is not None and child.poll()is None:
  try:os.killpg(child.pid,signal.SIGTERM)
  except ProcessLookupError:pass
signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
def ready(job):
 try:
  r=json.loads((ROOT/job['receipt']).read_text());return r['status']in['VERIFIED_ARITHMETIC_PART_NOT_FULL_PROOF','VERIFIED_ARITHMETIC_RANGE_NOT_FULL_PROOF']and r['artifact_sha256']==job['artifact_sha256']and r['checker_files']==codes and r['precision']==192 and r['leaf_range']==[job['lo'],job['hi']]and r['verified_leaves']==job['hi']-job['lo']and r['leaves']==job['leaves']
 except (OSError,ValueError,KeyError,TypeError):return False
def mutate(callback):
 with lock.open('a')as f:
  fcntl.flock(f,fcntl.LOCK_EX);data=json.loads(queue.read_text());value=callback(data);temp=queue.with_name(queue.name+f'.tmp.{os.getpid()}');temp.write_text(json.dumps(data,indent=2)+'\n');temp.replace(queue);return value
while not STOP and time.monotonic()-begun<a.seconds-180:
 def choose(data):
  for job in data['jobs']:
   if ready(job):job['status']='done'
  for job in data['jobs']:
   if job['status']=='pending':job['status']='running';job['runner_pid']=os.getpid();return dict(job)
  return None
 job=mutate(choose)
 if job is None:break
 cmd=[os.sys.executable,'verify_c57c_forest.py','--part',job['part'],'--leaf-start',str(job['lo']),'--leaf-stop',str(job['hi']),'--receipt',job['receipt']]
 started=time.monotonic();limit=min(1500,max(1,int(a.seconds-(started-begun))));rc=124
 with (ROOT/job['log']).open('w')as stream:
  child=subprocess.Popen(cmd,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True,env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1'))
  entry={'pid':child.pid,'command':cmd,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'limit_seconds':limit,'log':job['log'],'queue_job':job['id']}
  with (ROOT/'processes.jsonl').open('a')as f:f.write(json.dumps(entry)+'\n')
  try:rc=child.wait(timeout=limit)
  except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGTERM)
  finally:
   if child.poll()is None:
    try:child.wait(timeout=5)
    except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
   entry.update(exit=rc,elapsed_seconds=time.monotonic()-started)
   with (ROOT/'processes.jsonl').open('a')as f:f.write(json.dumps(entry)+'\n')
 def finish(data):
  found=next(v for v in data['jobs']if v['id']==job['id']);found['status']='done'if rc==0 and ready(job)else('pending'if rc==124 or STOP else 'failed');found['last_exit']=rc;found['elapsed_seconds']=time.monotonic()-started
 mutate(finish);print(json.dumps({'job':job['id'],'exit':rc,'seconds':time.monotonic()-started}),flush=True);child=None
print('ARITHMETIC_QUEUE_EPOCH_FINISHED',flush=True)

"""Finish this job's authorized CSDP run; every accepted artifact gets exact replay."""
import os,sys,time,subprocess,json,hashlib,shutil,signal,datetime
from fractions import Fraction
from pathlib import Path
pid=int(sys.argv[1]);pfx=sys.argv[2] if len(sys.argv)>2 else 'artifacts/original8';tag=sys.argv[3] if len(sys.argv)>3 else 'csdp';root=Path.cwd();receipt=root/('receipts/'+tag+'_pipeline.json')
stop_at=datetime.datetime(2026,11,2,3,0,tzinfo=datetime.timezone.utc).timestamp();sent=False
while Path(f'/proc/{pid}').exists():
 try:
  if os.readlink(f'/proc/{pid}/cwd')!=str(root):break
 except OSError:break
 if time.time()>=stop_at and not sent:
  os.kill(pid,signal.SIGTERM);sent=True
 if time.time()>=stop_at+900:os.kill(pid,signal.SIGKILL)
 time.sleep(30)
result={'utc':time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()),'verified':False}
def run(args,log):
 with open('receipts/'+log,'w') as f:
  p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT)
  with open('receipts/launched_pids.log','a') as record:record.write(str(p.pid)+' '+' '.join(args)+'\n')
  code=p.wait()
 if code:raise RuntimeError('failed '+log+' code '+str(code))
def bound(p):
 v=Path(p).read_text().splitlines()[0].split();return Fraction(int(v[4]),int(v[5]))
try:
 assert Path(pfx+'_color.sol').exists(),'CSDP wrote no solution'
 run([sys.executable,'scripts/read_csdp.py',pfx],tag+'_read.log')
 run([sys.executable,'scripts/export_squares_high.py',pfx,pfx+'_CSDP_Q.npz','artifacts/'+tag+'_provisional.cert','1000000000000','6'],tag+'_export_factors.log')
 candidates=['artifacts/'+tag+'_provisional.cert']
 try:
  run([sys.executable,'scripts/polish_weights_high.py',pfx,candidates[0],'artifacts/'+tag+'_polished.cert'],tag+'_polish.log');candidates.append('artifacts/'+tag+'_polished.cert')
 except Exception as e:result['polish_error']=str(e)
 best=max(candidates,key=bound);frozen='artifacts/frozen_'+tag+'8.cert';shutil.copyfile(best,frozen)
 result['bound']=str(bound(frozen));result['value']=float(bound(frozen));result['sha256']=hashlib.sha256(Path(frozen).read_bytes()).hexdigest();result['chosen']=best
 run(['./verify_frozen_fast',frozen,'sources/graph8.g6'],tag+'_exact.log')
 run(['./verify_legacy_gmp',frozen,'sources/graph8.g6'],tag+'_legacy.log')
 result['verified']=True
 run(['gzip','-c',frozen],'csdp_gzip_placeholder.log') if False else None
 import gzip
 with open(frozen+'.gz','wb') as f:f.write(gzip.compress(Path(frozen).read_bytes(),mtime=0))
except Exception as e:result['error']=str(e)
receipt.write_text(json.dumps(result,indent=2));Path('receipts/'+tag+'_pipeline.done').write_text(json.dumps(result));print(json.dumps(result),flush=True)

"""Lift a verified CSDP result to nine vertices and replay both exact proof paths."""
import os,sys,time,subprocess,json,shutil,gzip,hashlib
from pathlib import Path
receipt=Path('receipts/csdp_pipeline.done')
while not receipt.exists():time.sleep(30)
res=json.loads(receipt.read_text());out={'verified':False}
def run(args,log):
 with open('receipts/'+log,'w') as f:
  p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT)
  with open('receipts/launched_pids.log','a') as r:r.write(str(p.pid)+' '+' '.join(args)+'\n')
  rc=p.wait()
 if rc:raise RuntimeError(log+' code '+str(rc))
try:
 assert res.get('verified'), 'CSDP predecessor did not verify'
 run([sys.executable,'scripts/lift_rows9_cut.py','artifacts/frozen_csdp8.cert','csdp_lift9'],'csdp_lift9_search.log')
 frozen='artifacts/frozen_csdp_lift9.cert';shutil.copyfile('artifacts/csdp_lift9.cert',frozen)
 h=Path(frozen).read_text().splitlines()[0].split();out['bound']=h[4]+'/'+h[5];out['value']=int(h[4])/int(h[5]);out['sha256']=hashlib.sha256(Path(frozen).read_bytes()).hexdigest()
 run(['./verify_frozen_fast',frozen,'sources/graph9.g6'],'csdp_lift9_exact.log')
 run(['./verify_lift9',frozen,'sources/graph8.g6','sources/graph9.g6'],'csdp_lift9_independent.log')
 out['verified']=True;Path(frozen+'.gz').write_bytes(gzip.compress(Path(frozen).read_bytes(),mtime=0))
except Exception as e:out['error']=str(e)
Path('receipts/csdp_lift9_pipeline.json').write_text(json.dumps(out,indent=2));Path('receipts/csdp_lift9_pipeline.done').write_text(json.dumps(out));print(json.dumps(out),flush=True)

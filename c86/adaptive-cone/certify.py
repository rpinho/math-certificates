"""Freeze a finished search artifact and run both independent implementations.
Run only on the authorized pod through run_remote.sh. No search imports.
"""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('tag');p.add_argument('--workers',type=int,default=2);p.add_argument('--beat',default='1.80579911');a=p.parse_args()
source=Path(a.tag+'.json');raw=source.read_bytes();digest=hashlib.sha256(raw).hexdigest()
Path('frozen').mkdir(exist_ok=True)
frozen=Path('frozen')/(a.tag+'-'+digest[:16]+'.json')
if frozen.exists():assert frozen.read_bytes()==raw
else:frozen.write_bytes(raw)
frozen.chmod(0o444)
independent_command=([sys.executable,'-u','parallel_verify.py',str(frozen),'--output',a.tag+'-independent.json','--workers',str(a.workers)] if a.workers>1 else [sys.executable,'-u','independent_verify.py',str(frozen),'--output',a.tag+'-independent.json'])
commands=[('linear',[sys.executable,'-u','verify_linear.py',str(frozen),'--beat',a.beat,'--output',a.tag+'-verification.json']),('independent',independent_command)]
workers=[]
for name,cmd in commands:
 log=open('logs/'+a.tag+'-'+name+'.log','w')
 worker=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL)
 Path('logs/'+a.tag+'-'+name+'.pid').write_text(str(worker.pid)+'\n')
 workers.append((name,worker,log))
manifest=dict(tag=a.tag,frozen=str(frozen),sha256=digest,search_bar=a.beat,started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),verifiers={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in ['verify_linear.py','independent_verify.py']},pids={name:w.pid for name,w,_ in workers})
Path(a.tag+'-frozen-manifest.json').write_text(json.dumps(manifest,indent=2))
result={}
for name,worker,log in workers:result[name]=worker.wait();log.close()
if all(v==0 for v in result.values()):
    cmd=[sys.executable,'-u','audit_artifact.py',str(frozen),a.tag+'-independent.json','--output',a.tag+'-coverage-audit.json']
    result['coverage_audit']=subprocess.run(cmd).returncode
assert hashlib.sha256(frozen.read_bytes()).hexdigest()==digest
manifest.update(exit_codes=result,finished_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
Path(a.tag+'-certification.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2),flush=True)
sys.exit(0 if all(v==0 for v in result.values()) else 1)

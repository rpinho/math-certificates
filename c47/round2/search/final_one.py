"""Produce and exactly check one final candidate at the requested dyadic precision."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
import argparse,json,time,resource,subprocess,sys
from pathlib import Path
from certify import generate
ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('output');ap.add_argument('--bits',type=int,default=64);a=ap.parse_args()
start=time.process_time();wall=time.time();generate(a.source,a.output,D=2**a.bits)
for p in (Path(a.output+'.boxes.tsv'),Path(a.output.replace('.json','-measure.json'))):
 if p.exists():subprocess.run(['/usr/bin/trash',str(p)],check=True)
result=subprocess.run([sys.executable,'verify_exact.py',a.output,'--claim','0','--out',a.output+'.exact.json'],capture_output=True,text=True)
Path(a.output+'.verify.log').write_text(result.stdout+result.stderr)
u=resource.getrusage(resource.RUSAGE_CHILDREN)
Path(a.output+'.run.json').write_text(json.dumps(dict(pid=os.getpid(),source=a.source,bits=a.bits,seconds=time.time()-wall,cpu_seconds=time.process_time()-start+u.ru_utime+u.ru_stime,verifier_returncode=result.returncode),indent=2)+'\n')
print(result.stdout,flush=True)
if result.returncode:raise SystemExit(result.returncode)

"""Save exact improvements during the search, using the inherited verifier."""
import fcntl,json,time,subprocess,sys,os
from pathlib import Path
from fractions import Fraction as F

def checkpoint(source):
 source=Path(source)
 if not source.exists():return
 d=json.loads(source.read_text());fp=float(d['ratio'])
 with open('logs/certify.lock','a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  b=json.loads(Path('certificates/best.json').read_text());old=F(b['ratio'])
  if fp<=float(old)+2e-13:return
  # Freeze the exact producer input before any other chain can change its file.
  Path('chains/certifying.json').write_text(json.dumps(d,indent=1)+'\n')
  from certify import generate
  t=time.time()
  with open('logs/checkpoints.log','a',buffering=1) as out:
   try:
    generate('chains/certifying.json','certificates/pending.json')
    # The verifier's public CLI is used to preserve the existing exact path.
    p=subprocess.run([sys.executable,'verify_exact.py','certificates/pending.json','--claim','0','--out','logs/pending-exact.json'],stdout=out,stderr=out)
    if p.returncode:raise RuntimeError('verify_exact.py rejected checkpoint')
    v=json.loads(Path('logs/pending-exact.json').read_text());q=F(v['ratio'])
    if q>old:
     digits=q.numerator*10**16//q.denominator;tag=f'{digits//10**16}.{digits%10**16:016d}'
     dest=Path(f'certificates/best_{tag}.json');dest.write_bytes(Path('certificates/pending.json').read_bytes())
     Path('chains/best-snapshot.json').write_text(json.dumps(d,indent=1)+'\n')
     meta=dict(ratio=str(q),decimal=tag,certificate=str(dest),exact=v,source=str(source),time=time.time(),search_seconds=time.time()-1794139705.0,atoms=len(d['pts']))
     Path('certificates/best.json').write_text(json.dumps(meta,indent=2)+'\n')
     with open('logs/improvements.jsonl','a') as f:f.write(json.dumps(meta)+'\n')
     print('EXACT IMPROVEMENT',tag,'atoms',len(d['pts']),flush=True)
   except Exception as e:
    out.write('CHECKPOINT FAILURE '+repr(e)+'\n');raise
  for p in (Path('certificates/pending.json.boxes.tsv'),Path('certificates/pending-measure.json')):
   if p.exists():subprocess.run(['/usr/bin/trash',str(p)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

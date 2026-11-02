"""Copy selected frozen artifacts and record exact claims and provenance."""
import json,hashlib,gzip,shutil,time
from pathlib import Path
from fractions import Fraction
out=Path('certificates');out.mkdir(exist_ok=True)
items=[('c6_9.cert','artifacts/frozen_csdp_lift9.cert','primary'),('c6_8.cert.gz','artifacts/frozen_csdp8.cert.gz','eight-vertex support'),('c5_8.cert.gz','artifacts/frozen_k5_column.cert.gz','primary'),('c6_seed8.cert','artifacts/frozen_rows8.cert','search seed'),('public_c6_8.cert','artifacts/baseline.cert','public baseline')]
public5=Fraction('20421620024978222587630220763104861267/13398618197511951998870375167625873326080');public6=Fraction(21083,10**9);facts={}
for name,source,role in items:
 p=out/name;shutil.copyfile(source,p);data=p.read_bytes();raw=gzip.decompress(data) if name.endswith('.gz') else data
 v=iter(map(int,raw.split()));n,k,D,B,bn,bd,mode=[next(v) for _ in range(7)];blocks=[]
 for _ in range(B):
  t,m,typ,d,r=[next(v) for _ in range(5)]
  for _ in range(d+r*d):next(v)
  blocks.append({'t':t,'m':m,'type':typ,'dimension':d,'factor_rows':r})
 assert next(v,None) is None
 b=Fraction(bn,bd);old=public6 if k==6 else public5
 facts[name]={'role':role,'n':n,'k':k,'D':D,'root_mode':mode,'block_count':B,'factor_rows':sum(z['factor_rows'] for z in blocks),'bound':str(b),'value':float(b),'public_comparison':str(old),'absolute_gain':str(b-old),'absolute_gain_decimal':float(b-old),'relative_gain_percent':float((b/old-1)*100),'random_ratio':float(b*2**(k*(k-1)//2-1)),'sha256_file':hashlib.sha256(data).hexdigest(),'sha256_certificate':hashlib.sha256(raw).hexdigest(),'bytes':len(data),'blocks':blocks}
Path('CERTIFICATES.json').write_text(json.dumps(facts,indent=2));print(json.dumps({k:{a:v[a] for a in ['bound','relative_gain_percent','factor_rows','sha256_certificate']} for k,v in facts.items()},indent=2))
provenance={}
for file in ['sources/published_certificates.zip','sources/published_c5.json','sources/Csdp-source.tar.gz','sources/csdp.deb','sources/libsdp.deb','sources/gmpdev.deb']:
 p=Path(file)
 if p.exists():provenance[file]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
Path('receipts/public_input_hashes.json').write_text(json.dumps(provenance,indent=2))
resources=[json.loads(line) for line in Path('receipts/resources.jsonl').read_text().splitlines()];peak=max(resources,key=lambda z:z['rss_kb']);Path('receipts/resource_summary.json').write_text(json.dumps({'recorded_peak_rss_kb':peak['rss_kb'],'peak_utc':peak['utc'],'samples':len(resources),'sample_interval_seconds':30,'compute_rule':'nice 10; BLAS one thread; dedicated CSDP OpenMP at most six workers; at most ten active compute workers including concurrent checks','deadline_utc':'2026-11-02 03:50:00'},indent=2))

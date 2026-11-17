"""Lossless low-memory packing of the already checked explicit witnesses."""
import pathlib,lzma,hashlib,json,time
summary=[]
for n in (21,23):
 source=pathlib.Path(f'certificates/n{n}_balanced.txt');target=source.with_suffix('.txt.xz')
 begin=time.time();digest=hashlib.sha256()
 with source.open('rb') as inp,lzma.open(target,'wb',filters=[{'id':lzma.FILTER_LZMA2,'preset':1,'dict_size':33554432}]) as out:
  while data:=inp.read(1<<20):digest.update(data);out.write(data)
 check=hashlib.sha256()
 with lzma.open(target,'rb') as inp:
  while data:=inp.read(1<<20):check.update(data)
 assert digest.digest()==check.digest()
 row=dict(n=n,source_bytes=source.stat().st_size,packed_bytes=target.stat().st_size,sha256=digest.hexdigest(),seconds=time.time()-begin,dict_size=33554432)
 summary.append(row);print(row,flush=True)
pathlib.Path('logs/balanced_packing.json').write_text(json.dumps(summary,indent=2)+'\n')

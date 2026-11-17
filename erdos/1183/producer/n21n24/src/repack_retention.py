"""Lossless recompression of reference captures and balanced witness text."""
import lzma,hashlib,pathlib,time,json
rows=[]
for name in ['certificates/n21_balanced.txt.xz','certificates/n23_balanced.txt.xz','sources/captures.tar.xz']:
 p=pathlib.Path(name); q=p.with_name(p.name+'.repacked'); h=hashlib.sha256(); start=time.time()
 with lzma.open(p,'rb') as a,lzma.open(q,'wb',filters=[{'id':lzma.FILTER_LZMA2,'preset':3,'dict_size':33554432}]) as b:
  while data:=a.read(1<<20):h.update(data);b.write(data)
 g=hashlib.sha256()
 with lzma.open(q,'rb') as a:
  while data:=a.read(1<<20):g.update(data)
 assert h.digest()==g.digest()
 row=dict(file=name,old=p.stat().st_size,new=q.stat().st_size,sha256=h.hexdigest(),seconds=time.time()-start)
 rows.append(row);print(row,flush=True)
pathlib.Path('logs/retention_repacking.json').write_text(json.dumps(rows,indent=2)+'\n')

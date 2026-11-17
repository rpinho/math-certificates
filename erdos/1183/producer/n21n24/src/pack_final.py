"""Prepare a small, replayable packet without modifying the working data."""
import pathlib,json,gzip,lzma,tarfile,io,shutil,os,time,hashlib
from final_replay import inputs

start=time.time();rows,refs,screens=inputs();root=pathlib.Path('delivery');dest=root/'certificates'
dest.mkdir(parents=True,exist_ok=True)
for name in ('src','logs'):
 p=root/name
 if not p.exists():p.symlink_to('../'+name,target_is_directory=True)
for p in pathlib.Path('certificates').glob('*.json'):shutil.copyfile(p,dest/p.name)
for n,T in screens+[(3,2),(4,2),(4,3)]:
 base=pathlib.Path(f'certificates/n{n}_T{T}');out=dest/base.name
 if not base.exists():continue
 cp=json.loads((base/'checkpoint.json').read_text());assert not cp['stack']
 out.mkdir(exist_ok=True);shutil.copyfile(base/'checkpoint.json',out/'checkpoint.json')
 for i in range(cp['segment']):shutil.copyfile(base/f'{i:06d}.jsonl.gz',out/f'{i:06d}.jsonl.gz')
 for p in base.glob('G_L*.txt.gz'):shutil.copyfile(p,out/p.name)
for n in (21,23):shutil.copyfile(f'certificates/n{n}_balanced.txt.xz',dest/f'n{n}_balanced.txt.xz')

# Keep headline trees directly available; other trees needed for the
# reported classification and restriction claims go in the archive.
direct={c['proof'] for row in rows for c in row['colours']}
for row in json.load(open('certificates/best_n21.json')):
 direct.update(c['proof'] for c in row['colours'])
for p in direct:shutil.copyfile(p,dest/pathlib.Path(p).name)
archived=sorted(set(refs)-direct);raw=0
with lzma.open(dest/'no_trees.tar.xz','wb',filters=[{'id':lzma.FILTER_LZMA2,'preset':1,'dict_size':33554432}]) as compressed,tarfile.open(fileobj=compressed,mode='w|') as archive:
 for name in archived:
  p=pathlib.Path(name)
  size=0
  with gzip.open(p,'rb') as inp:
   while chunk:=inp.read(1<<20):size+=len(chunk)
  raw+=size
  entry=tarfile.TarInfo(p.name[:-3]);entry.size=size;entry.mtime=0
  with gzip.open(p,'rb') as inp:archive.addfile(entry,inp)
paths=list(dest.rglob('*'));logical=sum(p.stat().st_size for p in paths if p.is_file())
# Completed inherited chunks are immutable byte-for-byte duplicates.
bank={};links=0
for p in sorted(dest.glob('n*_T*/*.jsonl.gz')):
 digest=hashlib.sha256(p.read_bytes()).digest()
 if digest in bank:
  # This is a temporary staged copy created above in this session.
  p.unlink();os.link(bank[digest],p);links+=1
 else:bank[digest]=p
seen=set();size=0
for p in dest.rglob('*'):
 if p.is_file():
  st=p.stat();key=(st.st_dev,st.st_ino)
  if key not in seen:size+=st.st_size;seen.add(key)
result=dict(required_no_trees=len(refs),direct_no_trees=len(direct),archived_no_trees=len(archived),
            raw_archived_bytes=raw,archive_bytes=(dest/'no_trees.tar.xz').stat().st_size,
            certificate_data_bytes=size,logical_file_bytes=logical,deduplicated_chunk_links=links,seconds=time.time()-start,preset=1)
pathlib.Path('logs/final_packing.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)

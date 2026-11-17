"""Partition an existing exact DFS stack; merge unchanged proof records."""
import sys,pathlib,json,subprocess,time,os,shutil,resource
from prefix_resume import search
n,T,workers=map(int,sys.argv[1:4]);base=pathlib.Path(f'certificates/n{n}_T{T}')
cp=base/'checkpoint.json';start=time.time();manifest=base/'parallel.json'
initial_seconds=json.loads(cp.read_text())['seconds'] if cp.exists() else 0
if cp.exists() and not json.loads(cp.read_text())['stack']:
 print('ALREADY COMPLETE',n,T);sys.exit(0)
if not manifest.exists():
 # Run the ordinary search on the short pending prefixes first. Every
 # unprocessed root then has length >=14, giving many small disjoint tasks.
 # Short good prefixes and rejection witnesses are retained normally.
 old=search(n,T,frontier_depth=min(14,n+1))
 if not old['stack']:print('ALREADY COMPLETE',n,T);sys.exit(0)
 stacks=[[] for _ in range(min(workers,len(old['stack'])))];workers=len(stacks)
 for i,w in enumerate(old['stack']):stacks[i%workers].append(w)
 for i,stack in enumerate(stacks):
  part=base/f'part{i}';part.mkdir(exist_ok=True)
  (part/'checkpoint.json').write_text(json.dumps(dict(n=n,T=T,stack=stack,segment=0,visited=0,rejected=0,good=0,survivors=[],seconds=0)))
 manifest.write_text(json.dumps(dict(workers=workers,base=old,started_epoch=start,prior_seconds=initial_seconds),indent=2)+'\n')
else:
 m=json.loads(manifest.read_text());workers=m['workers'];old=m['base']
jobs=[]
for i in range(workers):
 out=open(f'logs/part_n{n}_T{T}_{i}.log','a')
 p=subprocess.Popen([sys.executable,'src/prefix_resume.py',str(n),str(T),str(i)],stdout=out,stderr=subprocess.STDOUT)
 pathlib.Path('logs/worker_pids.txt').open('a').write(str(p.pid)+'\n');jobs.append((p,out))
for p,out in jobs:rc=p.wait();out.close();assert rc==0,('worker failed',p.pid,rc)
total=dict(old);total['stack']=[];total['survivors']=list(old['survivors']);idx=old['segment']
for i in range(workers):
 part=base/f'part{i}';s=json.loads((part/'checkpoint.json').read_text());assert not s['stack']
 for k in range(s['segment']):shutil.copyfile(part/f'{k:06d}.jsonl.gz',base/f'{idx:06d}.jsonl.gz');idx+=1
 for k in ('visited','rejected','good'):total[k]+=s[k]
 total['survivors']+=s['survivors']
total['survivors'].sort();assert len(total['survivors'])==len(set(total['survivors']))
m=json.loads(manifest.read_text())
total['segment']=idx;total['seconds']=m['prior_seconds']+time.time()-m['started_epoch']
usage=resource.getrusage(resource.RUSAGE_CHILDREN)
total['parallel_child_core_seconds']=usage.ru_utime+usage.ru_stime
total['parallel_workers']=workers
tmp=cp.with_suffix('.tmp');tmp.write_text(json.dumps(total,indent=2)+'\n');os.replace(tmp,cp)
pathlib.Path(f'logs/n{n}_T{T}_prefix.json').write_text(json.dumps(total,indent=2)+'\n')
print('PARALLEL COMPLETE',json.dumps(total),flush=True)

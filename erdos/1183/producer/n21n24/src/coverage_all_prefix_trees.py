"""Separately implemented replay of segmented prefix/factor certificates.

Checks every recorded family directly, every good prefix's two no-trees,
and walks every word at every length with checker-owned symmetry logic.
"""
import sys,pathlib,json,gzip,subprocess,time
from check import witness,tree

def rejection(row,T):
 assert len(row)==6 and row[0]=='reject'
 _,w,c,f,offset,v=row
 assert type(offset) is int and 0<=offset and offset+len(v)<=len(w)
 assert w[offset:offset+len(v)]==v
 witness(len(v)-1,v,c,T+1,f)
 # The fixed initial coordinate block is disjoint from the shifted family.
 lift=[((x<<offset)|((1<<offset)-1)) for x in f]
 witness(len(w)-1,w,c,T+1,lift)
 return w

def check(n,T,verify_trees=True):
 start=time.time();base=pathlib.Path(f'certificates/n{n}_T{T}')
 cp=json.loads((base/'checkpoint.json').read_text());assert cp['stack']==[],'incomplete run'
 labels=pathlib.Path(f'logs/n{n}_T{T}_coverage.labels');counts={'reject':0,'good':0,'lifted':0};checked=set()
 outs={L:gzip.open(base/f'G_L{L}_T{T}.txt.gz','wt',compresslevel=1) for L in range(1,n+2)}
 try:
  with labels.open('w') as out:
   for i in range(cp['segment']):
    with gzip.open(base/f'{i:06d}.jsonl.gz','rt') as inp:
     for line in inp:
      row=json.loads(line);w=row[1];assert 1<=len(w)<=n+1 and w[0]=='0'
      if row[0]=='reject':
       rejection(row,T);out.write('R '+w+'\n');counts['reject']+=1;counts['lifted']+=row[4]>0
      else:
       assert row[0]=='good' and len(row)==3 and len(row[2])==2
       if verify_trees:
        for c,p in enumerate(row[2]):
         key=(w,c,T+1)
         if key not in checked:tree(p,w,c,T+1);checked.add(key)
       out.write('G '+w+'\n');outs[len(w)].write(w+'\n');counts['good']+=1
 finally:
  for out in outs.values():out.close()
 assert counts['reject']==cp['rejected'] and counts['good']==cp['good']
 got=subprocess.run(['src/coverage',str(n),str(labels)],capture_output=True,text=True)
 assert got.returncode==0,got.stderr
 rows=[json.loads(s) for s in got.stdout.splitlines()];assert len(rows)==n+1
 assert rows[-1]['good_orbits']==len(cp['survivors'])
 result=dict(n=n,T=T,counts=counts,trees_checked=len(checked),coverage=rows,seconds=time.time()-start)
 pathlib.Path(f'logs/n{n}_T{T}_coverage.json').write_text(json.dumps(result,indent=2)+'\n')
 print('COVERAGE PASS',json.dumps(result),flush=True)
 return result
if __name__=='__main__':check(int(sys.argv[1]),int(sys.argv[2]))

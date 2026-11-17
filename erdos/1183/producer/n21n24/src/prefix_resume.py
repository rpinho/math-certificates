"""Round-4 prefix search with explicit factor lifts and segment checkpoints.

No symmetry is applied at intermediate prefixes. Initial colour swap fixes
the first letter to zero. Every good prefix is saved, for future G_m(T).
"""
import sys,json,pathlib,gzip,time,os,shutil
from run import Runner,canonical
from screen import Catalogue
from check import witness

def search(n,T,part=None,frontier_depth=None):
 label=f'n{n}_T{T}';parent=pathlib.Path('certificates')/label
 base=parent if part is None else parent/f'part{part}'
 base.mkdir(exist_ok=True)
 cp=base/'checkpoint.json';began=time.time();cats={};badwords={}
 # A completed preceding dimension supplies exactly the prefixes that can
 # extend. Reuse its checked records, extending only its terminal good words.
 previous=pathlib.Path(f'certificates/n{n-1}_T{T}')
 if part is None and not cp.exists() and (previous/'checkpoint.json').exists():
  old=json.loads((previous/'checkpoint.json').read_text())
  if not old['stack']:
   terminal=[]
   for i in range(old['segment']):
    src=previous/f'{i:06d}.jsonl.gz';shutil.copyfile(src,base/src.name)
    with gzip.open(src,'rt') as inp:
     for line in inp:
      row=json.loads(line)
      if row[0]=='good' and len(row[1])==n:terminal.append(row[1])
   old.update(n=n,stack=[v+b for v in reversed(terminal) for b in ('1','0')],survivors=[],seconds=0)
   cp.write_text(json.dumps(old,indent=2)+'\n')
 state=json.loads(cp.read_text()) if cp.exists() else dict(n=n,T=T,stack=['0'],segment=0,visited=0,rejected=0,good=0,survivors=[],seconds=0)
 if not state['stack']:
  if part is None:pathlib.Path(f'logs/{label}_prefix.json').write_text(json.dumps(state,indent=2)+'\n')
  print('ALREADY COMPLETE',label,flush=True);return state
 # Rebuild only concrete positive factor witnesses; no negative cache is needed.
 seeds=[(base,state['segment'])]
 if part is not None:seeds.insert(0,(parent,json.loads((parent/'checkpoint.json').read_text())['segment']))
 for seed_base,segments in seeds:
  for i in range(segments):
   with gzip.open(seed_base/f'{i:06d}.jsonl.gz','rt') as inp:
    for line in inp:
     row=json.loads(line)
     if row[0]=='reject':
      _,w,c,f,offset,v=row
      badwords[w]=(c,[(x<<offset)|((1<<offset)-1) for x in f])
 frontier_ready=False
 with Runner() as r:
  while state['stack'] and not frontier_ready:
   idx=state['segment'];tmp=base/f'{idx:06d}.part';count=0
   with gzip.open(tmp,'wt',compresslevel=1) as out:
    while state['stack'] and count<256:
     if frontier_depth is not None:
      position=next((i for i in range(len(state['stack'])-1,-1,-1) if len(state['stack'][i])<frontier_depth),None)
      if position is None:frontier_ready=True;break
      w=state['stack'].pop(position)
     else:w=state['stack'].pop()
     count+=1;state['visited']+=1;L=len(w)
     bad=None
     # A suffix is a contiguous factor; records carry its exact lift offset.
     for offset in range(1,L):
      v=w[offset:]
      if v in badwords:
       c,f=badwords[v];bad=(c,f,offset,v);break
     if bad is None:
      if L not in cats:cats[L]=Catalogue(L-1,T+1,r)
      hit=cats[L].reject(w)
      if hit:bad=(hit[0],hit[1]['family'],0,w)
     if bad:
      c,f,offset,v=bad;lift=[(x<<offset)|((1<<offset)-1) for x in f]
      witness(L-1,w,c,T+1,lift);badwords[w]=(c,lift)
      out.write(json.dumps(['reject',w,c,f,offset,v],separators=(',',':'))+'\n');state['rejected']+=1
     else:
      ps=[r.decide(w,c,T+1)['proof'] for c in (0,1)]
      out.write(json.dumps(['good',w,ps],separators=(',',':'))+'\n');state['good']+=1
      if L==n+1:
       if canonical(w)==w:state['survivors'].append(w)
      else:state['stack'].extend([w+'1',w+'0'])
   os.replace(tmp,base/f'{idx:06d}.jsonl.gz');state['segment']+=1
   state['seconds']+=time.time()-began;began=time.time()
   tmp=cp.with_suffix('.tmp');tmp.write_text(json.dumps(state,indent=2)+'\n');os.replace(tmp,cp)
   print('CHECKPOINT',label,state['visited'],state['rejected'],len(state['survivors']),round(state['seconds'],2),flush=True)
 if part is None:pathlib.Path(f'logs/{label}_prefix.json').write_text(json.dumps(state,indent=2)+'\n')
 return state

if __name__=='__main__':search(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]) if len(sys.argv)>3 else None)

"""Replay the delivered mathematical claims, using only certificates and check.py."""
import json,gzip,pathlib,time,math,itertools
from check import witness,tree,read_open
start=time.time();total=0
for row in json.load(open('certificates/results.json')):
 n=row['n'];w=row['word']
 for c in row['colours']:
  witness(n,w,c['colour'],c['maximum'],c['witness'])
  tree(c['proof'],w,c['colour'],c['maximum']+1)
 assert max(c['maximum'] for c in row['colours'])==row['upper']
 print('UPPER',n,row['upper'],flush=True)

def rep(w):
 # Different ordering of the same four proved orbit operations.
 other=''.join(str(1-int(b)) for b in w)
 return min(w,other,w[::-1],other[::-1])

def inputs(kind):
 byname={}
 for p in sorted(pathlib.Path('certificates').glob('*_'+kind+'.jsonl.*')):byname.setdefault(p.name[:-3],p)
 return sorted(byname.values())

survivors={}
for path in inputs('screen'):
 with read_open(path) as inp:
  h=json.loads(next(inp));n=h['n'];T=h['T'];rejected=0;kept=[];orbits=0
  # Enumerate all words, then choose representatives; no producer enumeration imported.
  rows=iter(inp)
  for chars in itertools.product('01',repeat=n+1):
   w=''.join(chars)
   if w!=rep(w):continue
   try:row=json.loads(next(rows))
   except StopIteration:raise AssertionError(('missing orbit',path,w))
   assert row[0]==w,('word order',path,w,row[0]);orbits+=1
   if row[1]=='survives':
    assert len(row[2])==2
    for c,p in enumerate(row[2]):tree(p,w,c,T+1)
    kept.append(w)
    if h.get('stop_first'):break
   else:witness(n,w,row[1],T+1,row[2]);rejected+=1
  assert next(rows,None) is None,'extra orbit'
  survivors[n,T]=kept;total+=rejected
  print('FULL',n,T,orbits,rejected,len(kept),flush=True)
for path in inputs('prefix'):
 with read_open(path) as inp:
  h=json.loads(next(inp));n=h['n'];T=h['T'];it=iter(inp);line=next(it,None);row=json.loads(line) if line else None
  # All prefix files here are nonempty.
  leaves=[];count=0
  def visit(w):
   global row,count
   if row is not None and row[0]==w:
    witness(len(w)-1,w,row[1],T+1,row[2]);count+=1
    line=next(it,None);row=json.loads(line) if line else None;return
   if len(w)==n+1:
    if w==rep(w):leaves.append(w)
    return
   visit(w+'0');visit(w+'1')
  visit('0');assert row is None
  assert sorted(leaves)==sorted(survivors[n,T])
  print('PREFIX',n,T,count,len(leaves),flush=True)
for n in (15,17,19):
 with read_open(f'certificates/n{n}_balanced.jsonl.gz') as inp:
  h=json.loads(next(inp));seen=set()
  for line in inp:
   w,c,f=json.loads(line);assert w.count('1')==(n+1)//2 and w not in seen
   seen.add(w);witness(n,w,c,h['threshold'],f)
  assert len(seen)==math.comb(n+1,(n+1)//2)
  print('BALANCED',n,len(seen),flush=True)
print('REPLAY PASSED',total,'full-screen rejection witnesses; seconds',round(time.time()-start,3),flush=True)

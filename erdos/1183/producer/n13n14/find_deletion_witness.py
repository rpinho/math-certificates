"""Search an actual almost-closed family with precisely one missing implication."""
import json,itertools,pathlib,argparse
p=argparse.ArgumentParser();p.add_argument('word');p.add_argument('target',type=int);a=p.parse_args();n=len(a.word)-1
seeds=[]
screen=pathlib.Path(f'data/screen_n{n}_t{a.target-1}_witnesses.jsonl')
for color in '01':
 chain=[(1<<r)-1 for r in range(n+1) if a.word[r]==color]
 if len(chain)==a.target-1:seeds.append(chain)
for line in (screen.read_text().splitlines() if screen.exists() else []):
 d=json.loads(line)
 if d['word']==a.word:seeds.append(d['family'])
# Additional checked seeds are transformed into this rank colouring.
for fn in ['sources/round1_n11_families.jsonl','sources/round2_search_n12.jsonl']:
 for line in pathlib.Path(fn).read_text().splitlines():
  d=json.loads(line)
  if 'family' not in d:continue
  f=[sum(1<<i for i in s) for s in d['family']]
  if not f:continue
  inter=__import__('functools').reduce(int.__and__,f);union=__import__('functools').reduce(int.__or__,f);coords=[i for i in range(n) if ((union^inter)>>i)&1];w=len(coords)
  if w>n:continue
  f=[sum(1<<j for j,i in enumerate(coords) if s>>i&1) for s in f]
  for shift in range(n-w+1):
   for g in [f,[((1<<w)-1)^s for s in f]]:
    h={((1<<shift)-1)|(s<<shift) for s in g}
    c=a.word[next(iter(h)).bit_count()]
    if len({a.word[s.bit_count()] for s in h})!=1:continue
    h|={(1<<r)-1 for r in list(range(shift))+list(range(shift+w+1,n+1)) if a.word[r]==c}
    if len(h)==a.target-1:seeds.append(sorted(h))
seen=set();tried=0
for f in seeds:
 f=frozenset(f)
 if f in seen:continue
 seen.add(f);c=a.word[next(iter(f)).bit_count()]
 for s in range(1<<n):
  if s in f or a.word[s.bit_count()]!=c:continue
  g=f|{s};bad=[]
  for x,y in itertools.combinations(g,2):
   for z in [x|y,x&y]:
    if z not in g:bad.append((min(x,y),max(x,y),z))
  tried+=1
  if len(bad)!=1:continue
  # Reach a vector lex <= each transposition. The sorted member-mask tuple
  # increases precisely when its full Boolean membership vector decreases.
  g=tuple(sorted(g));changed=True
  while changed:
   changed=False
   for i,j in itertools.combinations(range(n),2):
    h=tuple(sorted(x^((1<<i)|(1<<j)) if ((x>>i)^(x>>j))&1 else x for x in g))
    if h>g:g=h;changed=True;break
  bad=[(min(x,y),max(x,y),z) for x,y in itertools.combinations(g,2) for z in [x|y,x&y] if z not in g]
  assert len(bad)==1
  out={'word':a.word,'n':n,'target':a.target,'color':int(c),'family':g,'missing_implication':bad[0],'seeds_tried':len(seen),'extensions_tried':tried}
  pathlib.Path(f'data/n{n}_deletion_witness.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit
print(json.dumps({'result':'no one-implication witness found; this is not an impossibility proof','seeds':len(seen),'extensions_tried':tried}))

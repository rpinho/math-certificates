"""Cheap rank screening using checked small sublattices plus comparable prefixes.
All rejection witnesses are actual bit-mask families. No SAT verdicts are used.
"""
import itertools,json,pathlib,argparse,collections
p=argparse.ArgumentParser();p.add_argument('n',type=int);p.add_argument('target',type=int);a=p.parse_args();n=a.n
seeds=set()
def add(f):
 f=frozenset(f)
 if not f:return
 assert all(s|t in f and s&t in f for s in f for t in f)
 common=set.intersection(*({i for i in range(n+1) if s>>i&1} for s in f))
 union=set.union(*({i for i in range(n+1) if s>>i&1} for s in f));coords=sorted(union-common)
 g=tuple(sorted(sum(1<<j for j,i in enumerate(coords) if s>>i&1) for s in f))
 seeds.add(g)
for fn in ['sources/round1_n11_families.jsonl','sources/round2_search_n12.jsonl']:
 for line in pathlib.Path(fn).read_text().splitlines():
  d=json.loads(line)
  if 'family' in d:add([sum(1<<i for i in s) for s in d['family']])
for f in json.loads(pathlib.Path('sources/round2_extra_seeds.json').read_text()):add([sum(1<<i for i in s) for s in f])
# Products of chains with positive block sizes, the usual small lattice screen.
for dims in range(1,5):
 for lengths in itertools.product(range(1,4),repeat=dims):
  if __import__('math').prod(x+1 for x in lengths)>24:continue
  for weights in itertools.product(range(1,5),repeat=sum(lengths)):
   if sum(weights)>n:continue
   chains=[];coord=0;ix=0
   for length in lengths:
    ch=[0];mask=0
    for j in range(length):
     w=weights[ix];ix+=1;mask|=((1<<w)-1)<<coord;coord+=w;ch.append(mask)
    chains.append(ch)
   add([__import__('functools').reduce(int.__or__,z,0) for z in itertools.product(*chains)])
# The diamond (lengths 1,1) and its unequal-rank variants are included above.
patterns={}
for f in seeds:
 w=max(f).bit_length()
 if w>n:continue
 for reflected in [f,tuple(sorted(((1<<w)-1)^s for s in f))]:
  for shift in range(n-w+1):
   translated=tuple(((1<<shift)-1)|(s<<shift) for s in reflected)
   rs=frozenset(s.bit_count() for s in translated)
   outside=tuple(range(shift))+tuple(range(shift+w+1,n+1))
   key=(rs,outside,len(f))
   patterns.setdefault(key,translated)
patterns=sorted(patterns.items(),key=lambda x:(-x[0][2],len(x[0][0])))
remaining=[];rejected=[];counts=collections.Counter()
for bits in itertools.product('01',repeat=n):
 word='1'+''.join(bits) # colour swap representative
 majority=max(word.count('0'),word.count('1'))
 if majority>=a.target:
  c=max('01',key=word.count);family=[(1<<r)-1 for r in range(n+1) if word[r]==c];reason='chain'
 else:
  family=None
  for (rs,outside,size),f in patterns:
   c=word[next(iter(rs))]
   if any(word[r]!=c for r in rs):continue
   exterior=[(1<<r)-1 for r in outside if word[r]==c]
   if size+len(exterior)>=a.target:family=list(f)+exterior;reason='checked seed + comparable prefixes';break
 if family is None:remaining.append(word);continue
 fs=set(family)
 assert len(fs)>=a.target and len({word[s.bit_count()] for s in fs})==1
 assert all(s|t in fs and s&t in fs for s in fs for t in fs)
 counts[reason]+=1;rejected.append({'word':word,'reason':reason,'family':sorted(fs)})
out={'n':n,'target':a.target,'representatives':1<<n,'total_words':1<<(n+1),'seeds':len(seeds),'patterns':len(patterns),'rejected_representatives':len(rejected),'counts':dict(counts),'remaining':remaining}
pathlib.Path(f'data/screen_n{n}_t{a.target}.json').write_text(json.dumps(out,indent=2)+'\n')
pathlib.Path(f'data/screen_n{n}_t{a.target}_witnesses.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rejected))
print(json.dumps({k:v for k,v in out.items() if k!='remaining'}));print('Remaining:',remaining[:60])

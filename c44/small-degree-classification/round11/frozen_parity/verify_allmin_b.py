"""Separately written (same agent) exact B: set closures of minimum-partial affine flats.
No proposer or checker A imports. Integer sets only, no numerical solver.
"""
import argparse, itertools, json, math, pathlib, time
cli=argparse.ArgumentParser();cli.add_argument('case');cli.add_argument('output');args=cli.parse_args()
case=json.loads(pathlib.Path(args.case).read_text());assert case['schema']=='c44-allminimum-v1'
assert case['status']=='candidate, unrefereed' and case['degree']==6
assert case['target']=={'controls':22,'norm':124,'expected_unsigned_leaves':0}
assert case['positive']=={'controls':12,'norm':64,'expected_unsigned_leaves_at_least':1}
assert case['seed']==dict(distinguished=0,pairs=[[2*j+1,2*j+2] for j in range(5)],terms=sorted(1|sum(1<<(2*j+1+((choice>>j)&1)) for j in range(5)) for choice in range(32)))
assert case['component_variance_numerator']==63 and case['two_component_norm_threshold']==126
def check(n,N,stop):
 started=time.time();nodes=0;leaves=0;domains=0
 seed=frozenset(case['seed']['terms'])
 def visit(forced,finished):
  nonlocal nodes,leaves,domains
  if stop and leaves:return
  nodes+=1;counts=[sum((s>>j)&1 for s in forced) for j in range(n)]
  if max(counts)>32:return
  deficit=sum(6-s.bit_count() for s in forced)
  if deficit>6*N-32*n:return
  if sum(32-c for c in counts)>6*(N-len(forced)):return
  active=set(j for j,c in enumerate(counts) if c)
  assert all(counts[j]==32 for j in finished)
  if len(finished)==n:
   remainder=N-len(forced)
   if remainder>=0 and math.isqrt(remainder)**2==remainder:leaves+=1
   return
  if active<=finished:
   assert N<2*63
   return
  coordinate=max(active-finished,key=lambda j:(counts[j],j))
  local={s for s in forced if s>>coordinate&1};assert len(local)>=16
  anchor=max(local);directions={0}
  for s in sorted(local,reverse=True):
   delta=s^anchor
   if delta not in directions:directions|={v^delta for v in tuple(directions)}
   if len(directions)>32:return
  assert len(directions) in (16,32)
  original=frozenset(anchor^v for v in directions);assert local<=original
  domains+=1
  candidates=set()
  if len(directions)==32:candidates.add(original)
  else:
   old=sorted(active-{coordinate},reverse=True);unused=sorted(set(range(n))-active,reverse=True)
   # Fresh columns are identical on any newly added coset: quotient by
   # permutations fixing all already-used coordinates, in reverse order.
   for count in range(6):
    for subset in itertools.combinations(old,count):
     base=(1<<coordinate)|sum(1<<v for v in subset)
     for take in range(min(5-count,len(unused))+1):
      extra=base|sum(1<<v for v in unused[:take])
      if extra in original:continue
      extension=original|{extra^v for v in directions}
      if any(s.bit_count()>6 for s in extension):continue
      if any((s not in forced) and any(s>>j&1 for j in finished) for s in extension):continue
      candidates.add(frozenset(extension))
  for extension in sorted(candidates,key=lambda x:tuple(sorted(x,reverse=True))):
   if any(s.bit_count()>6 for s in extension):continue
   if any(s not in forced and any(s>>j&1 for j in finished) for s in extension):continue
   combined=forced|extension
   if len(combined)<=N:visit(combined,finished|{coordinate})
 visit(seed,set([0]))
 return dict(controls=n,norm=N,nodes=nodes,domains=domains,unsigned_leaves=leaves,seconds=time.time()-started)
positive=check(12,64,True);assert positive['unsigned_leaves']>=1
target=check(22,124,False);assert target['unsigned_leaves']==0
result=dict(status='PASS',implementation='B set affine closures',positive=positive,target=target)
pathlib.Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

"""Separately written (same agent): stream every clause from the finite statement.
No imports from encoder or lex generator. Explicit frozenset operations and
sequential exact comparisons avoid storing millions of redundant clauses.
"""
import argparse,itertools,json,pathlib
p=argparse.ArgumentParser();p.add_argument('cnf');p.add_argument('--base');a=p.parse_args()
m=json.loads(pathlib.Path(a.cnf+'.json').read_text());n=m['n'];k=m['target'];word=m['ranks'];color=m['color']
sets=[frozenset(i for i in range(n) if mask//(2**i)%2) for mask in range(2**n)]
allowed=[s for s in sets if int(word[len(s)])==color];ids={s:i+1 for i,s in enumerate(allowed)}
assert m['members']==[sum(2**i for i in s) for s in allowed]
f=open(a.cnf);head=f.readline().split();assert head[:2]==['p','cnf'];nv,nc=map(int,head[2:]);count=0

def take(expected):
 global count
 line=f.readline();assert line,('unexpected EOF',count)
 actual=list(map(int,line.split()));assert actual[-1:]==[0]
 assert actual[:-1]==expected,('clause mismatch',count+1,actual,expected)
 count+=1

closure=0
for i,s in enumerate(allowed):
 for t in allowed[i+1:]:
  if s.issubset(t) or t.issubset(s):continue
  for result in [s.union(t),s.intersection(t)]:
   take([-ids[s],-ids[t]]+([ids[result]] if result in ids else []));closure+=1
assert closure==m['closure_clauses']
N=len(allowed);node={};v=N
for prefix in range(1,N+1):
 for j in range(1,min(prefix,k)+1):v+=1;node[prefix,j]=v
for (i,j),q in node.items():
 prev=node.get((i-1,j));less=node.get((i-1,j-1))
 take([-q]+([prev] if prev else [])+[i])
 if j>1:take([-q]+([prev] if prev else [])+([less] if less else []))
take([node[N,k]] if N>=k else [])
base_count=count;base_nv=v
if 'symmetry' in m:
 for first in range(n):
  for second in range(first+1,n):
   previous=None
   for s in allowed:
    t=frozenset(second if x==first else first if x==second else x for x in s)
    assert t in ids,'not a colour-preserving swap'
    if ids[s]>=ids[t]:continue
    v+=1;lead=[] if previous is None else [-previous];x,y=ids[s],ids[t]
    for cl in [lead+[-x,y],lead+[-x,-y,v],lead+[x,y,v]]:take(cl)
    previous=v
 assert m['base_variables']==base_nv and m['base_clauses']==base_count
assert count==nc and v==nv and not f.read().strip();f.close()
# Counter's backwards recurrence follows by distributivity. Every real >=k
# selection extends using true prefix counts; induction forces >=k members.
for b,x,c,q in itertools.product([False,True],repeat=4):
 assert ((not q) or b or (x and c))==(((not q) or b or x) and ((not q) or b or c))
# Lex comparator local recurrence, all assignments through length 4.
for length in range(1,5):
 for bits in itertools.product([False,True],repeat=2*length):
  left,right=bits[:length],bits[length:];possible=False
  for aux in itertools.product([False,True],repeat=length):
   prev=True;ok=True
   for x,y,q in zip(left,right,aux):
    ok &= ((not prev) or (not x) or y) and ((not prev) or (not x) or (not y) or q) and ((not prev) or x or y or q);prev=q
   possible |= ok
  assert possible==(left<=right)
print(json.dumps({'result':'EVERY CLAUSE REBUILT FROM STATEMENT','n':n,'rank_word':word,'color':color,'target':k,'variables':nv,'clauses':nc,'closure_clauses':closure,'base_clauses':base_count,'lex_clauses':nc-base_count,'transpositions':n*(n-1)//2 if 'symmetry' in m else 0,'soundness':'All coordinate permutations preserve rank colours, size, union and intersection. Choose a global lex-minimum member vector in a counterexample orbit. It satisfies each swap comparison; prefix-count auxiliaries can be recomputed. Equal pairs force equality prefixes until the first difference; 1>0 is forbidden, 0<1 permits subsequent prefixes false. Fixed positions and later endpoints do not affect the first differing position.'}))

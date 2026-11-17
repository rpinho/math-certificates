"""Separately written certificate checker. Does not import search code."""
import gzip,json,sys,pathlib,tarfile,io,lzma
from contextlib import contextmanager

@contextmanager
def read_open(path):
 if hasattr(path,'read'):
  yield path
 elif str(path).endswith('.gz') and pathlib.Path(str(path)[:-3]+'.xz').exists():
  with lzma.open(str(path)[:-3]+'.xz','rt') as f:yield f
 elif str(path).endswith('.xz') and pathlib.Path(path).exists():
  with lzma.open(path,'rt') as f:yield f
 elif str(path).endswith('.gz') and pathlib.Path(str(path)[:-3]).exists():
  with open(str(path)[:-3]) as f:yield f
 elif pathlib.Path(path).exists():
  with (gzip.open(path,'rt') if str(path).endswith('.gz') else open(path)) as f:yield f
 else:
  # All exhaustive trees are retained losslessly in one standard tar.xz archive.
  name=pathlib.Path(path).name
  if name.endswith('.gz'):name=name[:-3]
  with tarfile.open('certificates/no_trees.tar.xz','r:xz') as archive:
   with io.TextIOWrapper(archive.extractfile(name)) as f:yield f


def witness(n,word,c,target,family):
 assert len(word)==n+1 and set(word)<=set('01')
 assert len(family)==len(set(family)) and len(family)>=target
 assert all(type(x) is int and 0<=x<2**n and int(word[x.bit_count()])==c for x in family)
 F=set(family)
 for x in F:
  for y in F:
   assert x&y in F and x|y in F, ('closure',x,y)
 return True

def tree(path,expected_word,expected_colour,expected_threshold):
 with read_open(path) as inp:
  def take():
   line=inp.readline();assert line, 'missing subtree';return json.loads(line)
  h=take();n=len(expected_word)-1
  assert h['n']==n and h['word']==expected_word and h['colour']==expected_colour and h['threshold']==expected_threshold, 'binding'
  allowed={i for i,c in enumerate(expected_word) if int(c)==expected_colour}
  count=0
  def visit(a,preds,weights):
   nonlocal count
   count+=1
   k=len(weights);down={}
   # Enumerate all masks from the order relation, not the producer's extension recurrence.
   for mask in range(2**k):
    if all(not(mask>>i&1) or preds[i]&mask==preds[i] for i in range(k)):
     down[mask]=sum(weights[i] for i in range(k) if mask>>i&1)
   assert len(down)<expected_threshold,'threshold reached in no tree'
   assert all(a+s in allowed for s in down.values()),'invalid state'
   edges=take();assert type(edges) is list
   expected=[(I,w) for I in sorted(down) for w in range(1,n-a-sum(weights)+1)]
   assert len(edges)==len(expected),'missing branches'
   for e,pair in zip(edges,expected):
    assert len(e)==3 and tuple(e[:2])==pair,'branch label'
    I,w=pair;bad=e[2]
    if bad!=-1:
     assert bad in down and bad&I==I and a+down[bad]+w not in allowed,'bad prune'
    else:
     assert all(a+s+w in allowed for D,s in down.items() if D&I==I),'invalid child'
   for I,w,bad in edges:
    if bad==-1:visit(a,preds+[I],weights+[w])
  for a in sorted(allowed):
   assert take()=={'root':a},'missing root'
   visit(a,[],[])
  assert not inp.read().strip(),'trailing data'
  assert h['nodes']==count and count>=2**len(allowed)-1, 'node count'
 return count

if __name__=='__main__':
 print('CHECKED',tree(sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])))

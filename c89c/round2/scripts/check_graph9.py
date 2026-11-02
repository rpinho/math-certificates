"""Independent order-nine list completeness by exhaustive vertex augmentation.
The eight-vertex input list must also pass verify_frozen's labelled orbit cover.
"""
import itertools,hashlib,json,time,sys
from pathlib import Path
import pynauty

def decode(line):
 n=ord(line[0])-63;adj={i:[] for i in range(n)};b=0
 for j in range(1,n):
  for i in range(j):
   if (ord(line[1+b//6])-63)>>(5-b%6)&1:adj[i].append(j);adj[j].append(i)
   b+=1
 return n,adj
small=Path(sys.argv[1] if len(sys.argv)>1 else 'sources/graph8.g6');large=Path(sys.argv[2] if len(sys.argv)>2 else 'sources/graph9.g6');expected=set()
for row,line in enumerate(small.read_text().splitlines()):
 n,adj=decode(line);assert n==8
 for mask in range(256):
  a={i:adj[i]+([8] if mask>>i&1 else []) for i in range(8)};a[8]=[i for i in range(8) if mask>>i&1]
  expected.add(pynauty.certificate(pynauty.Graph(9,adjacency_dict=a)))
 if row%1000==0:print('augmentation',row,len(expected),time.time(),flush=True)
actual=set();count=0
for line in large.read_text().splitlines():
 n,adj=decode(line);assert n==9;key=pynauty.certificate(pynauty.Graph(9,adjacency_dict=adj));assert key not in actual;actual.add(key);count+=1
assert actual==expected
result={'PASS':True,'classes9':count,'augmentation_attempts':12346*256,'sha256_8':hashlib.sha256(small.read_bytes()).hexdigest(),'sha256_9':hashlib.sha256(large.read_bytes()).hexdigest(),'pynauty_version':pynauty.__version__}
Path('receipts/graph9_completeness.json').write_text(json.dumps(result,indent=2));print('PASS',result,flush=True)

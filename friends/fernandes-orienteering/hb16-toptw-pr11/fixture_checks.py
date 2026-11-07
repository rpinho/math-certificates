"""Exhaustive small independent oracles for the closure checker."""
from pathlib import Path
from itertools import permutations
import subprocess,random,json,tempfile
rng=random.Random(1103);exe=str(Path('closure').resolve())
receipts=[]
def run(root):
 r=subprocess.run([exe,'proof'],cwd=root,capture_output=True,text=True)
 return r.returncode==0
for case in range(40):
 n=rng.randint(3,8)
 d=[[0 if i==j else rng.randint(1,12) for j in range(n)]for i in range(n)]
 s=[0]+[rng.randint(0,4)for _ in range(n-1)]
 a=[0]+[rng.randint(0,8)for _ in range(n-1)]
 b=[50]+[rng.randint(12,35)for _ in range(n-1)]
 w=[0]+[rng.randint(0,9)for _ in range(n-1)]
 states={(0,0,0,1)};paths=[]
 def visit(seq,t,z,mem):
  i=seq[-1]
  if t+d[i][0]<=b[0]:paths.append((mem&~1,z))
  for j in range(1,n):
   if mem>>j&1:continue
   tt=max(a[j],t+d[i][j])+s[j]
   if tt>b[j]+s[j]:continue
   states.add((j,tt,z+w[j],mem|1<<j));visit(seq+[j],tt,z+w[j],mem|1<<j)
 visit([0],0,0,1)
 # Prefix maximum is safe even when a prefix cannot return.
 B=max(z for _,_,z,_ in states)
 with tempfile.TemporaryDirectory(dir='.') as root:
  root=Path(root)
  model=[str(n)]+[f'{s[i]} {a[i]} {b[i]} {w[i]}'for i in range(n)]+[' '.join(map(str,row))for row in d]
  (root/'model.txt').write_text('\n'.join(model)+'\n')
  def proof(bound,keep):
   rows=['NGBOUND2',f'{n} {bound} {bound}']+[f'{n} '+' '.join(map(str,range(n)))for _ in range(n)]+[str(len(keep))]
   rows+=[' '.join(map(str,l))for l in sorted(keep)]
   (root/'proof').write_text('\n'.join(rows)+'\n')
  proof(B,states);assert run(root),(case,'valid rejected')
  proof(max(0,B-1),states)
  if B:assert not run(root),(case,'false upper accepted')
  proof(B,states-{(0,0,0,1)});assert not run(root),(case,'missing root accepted')
  # Full enumeration oracle includes directed non-metric travel, waiting,
  # service-start vs departure conventions, and zero reduced rewards.
  receipts.append({'case':case,'vertices':n,'states':len(states),'max_prefix':B,'max_route':max(z for _,z in paths)})
result={'exhaustive_fixtures':len(receipts),'all_passed':True,'details':receipts}
Path('fixture_receipt.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

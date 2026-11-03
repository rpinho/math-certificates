"""Exact ordered-tuple controls for the separately written support/occupancy checker."""
import itertools,random,subprocess,pathlib,json
from fractions import Fraction
rng=random.Random(89);cases=[]
for n in [1,2,3,4]:
 for trial in range(5):
  D=5;R=[[0]*n for _ in range(n)];w=[rng.randrange(1,4) for _ in range(n)]
  for i in range(n):
   for j in range(i+1):R[i][j]=R[j][i]=rng.randrange(D+1)
  exact=0
  for vs in itertools.product(range(n),repeat=5):
   mass=1;red=blue=1
   for v in vs:mass*=w[v]
   for j in range(1,5):
    for i in range(j):red*=R[vs[i]][vs[j]];blue*=D-R[vs[i]][vs[j]]
   exact+=mass*(red+blue)
  exact=Fraction(exact,D**10*sum(w)**5);s=f'{n} {D}\n'+' '.join(map(str,w))+'\n'+'\n'.join(' '.join(map(str,r)) for r in R)+'\n';r=subprocess.run(['./check_graphon'],input=s,capture_output=True,text=True,check=True);a,b,*_=map(int,r.stdout.splitlines());assert Fraction(a,b)==exact;cases.append(dict(n=n,trial=trial,value=str(exact)))
# The generic counter itself rejects asymmetric inputs and invalid masses/ranges.
bad=['2 5\n1 1\n0 1\n2 0\n','1 5\n0\n3\n','1 5\n1\n6\n']
for s in bad:assert subprocess.run(['./check_graphon'],input=s,capture_output=True,text=True).returncode!=0
pathlib.Path('receipts/graphon_controls.json').write_text(json.dumps(dict(PASS=True,exact_small_cases=cases,malformed_rejections=len(bad)),indent=2));print('PASS',len(cases),'exact ordered-tuple comparisons;',len(bad),'malformed cases rejected',flush=True)

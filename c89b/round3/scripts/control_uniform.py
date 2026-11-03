"""Test the bounded-integer generic checker against literal ordered five-tuples."""
import itertools,json,pathlib,random,subprocess
from fractions import Fraction
rng=random.Random(891103);results=[]
for trial in range(30):
 n=1+trial%5;D=rng.randrange(1,13);A=[[0]*n for _ in range(n)]
 for i in range(n):
  for j in range(i+1):A[i][j]=A[j][i]=rng.randrange(D+1)
 total=0
 for v in itertools.product(range(n),repeat=5):
  red=blue=1
  for j in range(1,5):
   for i in range(j):p=A[v[i]][v[j]];red*=p;blue*=D-p
  total+=red+blue
 text=f'{n} {D}\n'+' '.join(['1']*n)+'\n'+'\n'.join(' '.join(map(str,row)) for row in A)+'\n'
 r=subprocess.run(['./check_uniform'],input=text,text=True,capture_output=True,check=True);a,b,red,blue=map(int,r.stdout.split());value=Fraction(a,b);literal=Fraction(total,n**5*D**10);assert value==literal and red+blue==total
 results.append(dict(trial=trial,n=n,D=D,literal_match=True))
bad=[]
for text in ['1 65\n1\n0\n','1 2\n2\n1\n','2 2\n1 1\n0 1\n2 0\n','1 2\n1\n3\n','1 2\n1\n1\nextra\n']:
 r=subprocess.run(['./check_uniform'],input=text,text=True,capture_output=True);assert r.returncode!=0;bad.append(dict(input=text.strip(),rejected=True,diagnostic=r.stderr.strip()))
pathlib.Path('receipts/uniform_controls.json').write_text(json.dumps(dict(PASS=True,literal_controls=results,rejections=bad),indent=2));print('PASS 30 literal ordered-tuple comparisons and5 rejections',flush=True)

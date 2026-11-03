import pathlib,subprocess,json,itertools,random,gzip
from fractions import Fraction
rng=random.Random(1103)
def call(name,n,D,q=None,R=None):
 if name=='check_cayley_exact_r4':s=f'{n} {D}\n'+' '.join(map(str,q))+'\n'
 else:s=f'{n} {D}\n'+' '.join(['1']*n)+'\n'+'\n'.join(' '.join(map(str,r)) for r in R)+'\n'
 r=subprocess.run(['./'+name],input=s,text=True,capture_output=True,check=True);a,b,red,blue=map(int,r.stdout.split());assert Fraction(a,b)==Fraction(red+blue,D**10*n**(4 if q is not None else 5));return Fraction(a,b),red,blue
rows=[]
for trial in range(24):
 n=rng.choice([2,4,8]);D=rng.choice([1,7,36,1000,4096]);q=[rng.randrange(D+1) for _ in range(n)];R=[[q[a^b] for b in range(n)] for a in range(n)]
 a,ar,ab=call('check_wide',n,D,R=R);b,br,bb=call('check_cayley_exact_r4',n,D,q=q);assert a==b and ar==br*n and ab==bb*n
 literal=[0,0]
 for vertices in itertools.product(range(n),repeat=5):
  for color in range(2):
   term=1
   for j in range(1,5):
    for i in range(j):term*=D-R[vertices[i]][vertices[j]] if color else R[vertices[i]][vertices[j]]
   literal[color]+=term
 assert literal==[ar,ab];rows.append(dict(trial=trial,n=n,D=D,density=str(a)))
# Generic matrices that have no Cayley symmetry, including arbitrary loops.
for trial in range(12):
 n=rng.choice([2,3,5]);D=rng.choice([7,1000,4096]);R=[[0]*n for _ in range(n)]
 for j in range(n):
  for i in range(j+1):R[i][j]=R[j][i]=rng.randrange(D+1)
 a,ar,ab=call('check_wide',n,D,R=R);lit=[0,0]
 for vertices in itertools.product(range(n),repeat=5):
  for color in range(2):
   term=1
   for j in range(1,5):
    for i in range(j):term*=D-R[vertices[i]][vertices[j]] if color else R[vertices[i]][vertices[j]]
   lit[color]+=term
 assert lit==[ar,ab];rows.append(dict(generic_trial=trial,n=n,D=D,density=str(a)))
rejects=[]
for binary,inputs in [('check_wide',['2 0\n','2 4097\n','2 10\n1 2\n','2 10\n1 1\n0 2 3 0\n','2 10\n1 1\n0 2 2\n']),('check_cayley_exact_r4',['3 10\n0 2 5\n','2 1000000001\n0 1\n','2 10\n0 11\n','2 10\n0\n','2 10\n0 1\nEXTRA\n'])]:
 for s in inputs:
  r=subprocess.run(['./'+binary],input=s,text=True,capture_output=True);assert r.returncode!=0;rejects.append(dict(binary=binary,input=s,error=r.stderr.strip()))
result=dict(PASS=True,comparisons=rows,rejections=rejects,status='candidate and unrefereed');pathlib.Path('receipts/wide_cayley_controls.json').write_text(json.dumps(result,indent=2));print('PASS',len(rows),'literal comparisons;',len(rejects),'rejections')

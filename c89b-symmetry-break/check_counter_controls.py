"""Exact small controls for the independent support/occupancy counter."""
import itertools,pathlib,random,subprocess
counter=pathlib.Path(__file__).with_name('independent_count').resolve()
rng=random.Random(1101)
for trial in range(25):
 n=1+trial%5;D=5;p=2
 R=[[0]*n for _ in range(n)]
 for i in range(n):
  for j in range(i,n):R[i][j]=R[j][i]=rng.choice([0,p,D])
 inp=f'{n} {D} {p}\n'+'\n'.join(' '.join(map(str,row)) for row in R)+'\n'
 result=subprocess.run([str(counter)],input=inp,text=True,capture_output=True,check=True)
 counts=[list(map(int,line.split())) for line in result.stdout.strip().splitlines()]
 counted=sum(counts[0][e]*p**e*D**(10-e)+counts[1][e]*(D-p)**e*D**(10-e) for e in range(11))
 brute=0
 for v in itertools.product(range(n),repeat=5):
  r=b=1
  for i in range(5):
   for j in range(i):a=R[v[i]][v[j]];r*=a;b*=D-a
  brute+=r+b
 assert counted==brute,(trial,R,counted,brute)
 print('EXACT CONTROL',trial,'n',n,'PASS')
bad='2 5 2\n0 2\n5 0\n'
assert subprocess.run([str(counter)],input=bad,text=True,capture_output=True).returncode!=0
print('ASYMMETRY REJECTION PASS; 25 exact ordered-tuple controls passed')

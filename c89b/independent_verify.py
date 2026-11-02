"""Exact rational arithmetic on the frozen graphon, using an independent C++ recount.

Run from the job root: python frozen/independent_verify.py frozen/candidate.json.gz
The counter is independently implemented with distinct supports and occupancies,
not the search's nondecreasing repeated-label enumeration.
"""
import gzip,hashlib,json,pathlib,subprocess,sys
from fractions import Fraction

path=pathlib.Path(sys.argv[1]); blob=path.read_bytes()
d=json.loads(gzip.decompress(blob) if path.suffix=='.gz' else blob)
assert d['schema']=='rational-step-graphon-v1'
D=d['edge_probability_denominator']; R=d['red_probability_numerators'];n=len(R)
assert type(D) is int and D>0 and 0<n<=1024
assert len(d['block_weights'])==n and all(Fraction(w)==1 for w in d['block_weights'])
assert all(len(row)==n for row in R)
assert all(type(x) is int and 0<=x<=D for row in R for x in row)
assert all(R[i][j]==R[j][i] for i in range(n) for j in range(n))
values=set(x for row in R for x in row)-{0,D};assert len(values)==1
p=values.pop()
counter=pathlib.Path(__file__).with_name('independent_count')
inp=f'{n} {D} {p}\n'+'\n'.join(' '.join(map(str,row)) for row in R)+'\n'
out=subprocess.run([str(counter.resolve())],input=inp,text=True,capture_output=True,check=True).stdout
rows=[list(map(int,s.split())) for s in out.strip().splitlines()]
assert len(rows)==2 and all(len(s)==11 for s in rows)
assert all(0<=a<=n**5 for row in rows for a in row)
q=Fraction(p,D)
density=sum(rows[0][e]*q**e+rows[1][e]*(1-q)**e for e in range(11))/n**5
baseline=Fraction(107218716425177032911811117405568916263805081691166740697,63555655070790142733837367909977622463036348875198349443072)
target=Fraction(168523,100000000)
assert density<target<baseline
print('FROZEN SHA256',hashlib.sha256(blob).hexdigest())
print('RED COUNTS',rows[0]);print('BLUE COUNTS',rows[1])
print('DENSITY EXACT',density)
print('DENSITY APPROX',format(float(density),'.17g'))
print('BASELINE EXACT',baseline)
print('IMPROVEMENT EXACT',baseline-density)
print('IMPROVEMENT RELATIVE APPROX',float((baseline-density)/baseline))
print('PASS: candidate C89b < 0.00168523 < public baseline; unrefereed')

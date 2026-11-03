"""Independent baseline, small full-matrix comparison and rejection controls."""
import pathlib,subprocess,json,gzip,sys
from fractions import Fraction
def exact(d,L,D,p,q):
 r=subprocess.run(['./check_radial_exact'],input=f'{d} {L} {D} {p} {q}\n',text=True,capture_output=True,check=True)
 a,b,red,blue=map(int,r.stdout.split());return Fraction(a,b)
baseline=exact(6,3,7,5,7);assert baseline==Fraction(2405659597,1427496763392),baseline
tests=[]
for d,L,D,p,q in [(2,2,3,1,2),(2,3,5,4,3),(4,2,7,5,6),(2,4,2,0,1)]:
 f=pathlib.Path(f'artifacts/radial_control_{d}_{L}_{D}.json')
 subprocess.run([sys.executable,'scripts/freeze_radial.py',str(d),str(L),str(D),str(p),str(q),str(f)],check=True)
 r=subprocess.run([sys.executable,'scripts/check_graphon.py',str(f)],capture_output=True,text=True,check=True)
 ordinary=Fraction(json.loads(r.stdout)['density']);special=exact(d,L,D,p,q);assert ordinary==special,(d,L,ordinary,special)
 tests.append(dict(parameters=[d,L,D,p,q],density=str(special),match=True));print(tests[-1],flush=True)
bad=[]
for text in ['6 4 0 0 0\n','6 4 36 37 35\n','6 4 36 24 -1\n','6 4 36 24 35 extra\n']:
 r=subprocess.run(['./check_radial_exact'],input=text,capture_output=True,text=True);assert r.returncode!=0;bad.append(dict(input=text.strip(),rejected=True,diagnostic=r.stderr.strip()))
selected=exact(6,4,36,24,35)
try:
 assert selected<Fraction(1,1000)
 raise RuntimeError('false stronger threshold was accepted')
except AssertionError:bad.append(dict(control='false claimed density <0.001',rejected=True))
pathlib.Path('receipts/radial_controls.json').write_text(json.dumps(dict(PASS=True,baseline=str(baseline),small_instances=tests,rejections=bad,selected=str(selected)),indent=2));print('PASS radial controls',flush=True)

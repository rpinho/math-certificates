import json,math,time,hashlib
from pathlib import Path
from fractions import Fraction
names=[p.name for p in sorted(Path('artifacts').glob('frozen*.cert'))]
public5=Fraction('20421620024978222587630220763104861267/13398618197511951998870375167625873326080');public6=Fraction(21083,10**9);out={}
for name in names:
 p=Path('artifacts')/name;v=iter(map(int,p.read_text().split()));n,k,D,B,bn,bd,mode=[next(v) for _ in range(7)];bound=Fraction(bn,bd);blocks=[]
 for _ in range(B):
  t,m,typ,d,r=[next(v) for _ in range(5)];flags=[next(v) for _ in range(d)];L=[[next(v) for _ in range(d)] for _ in range(r)];blocks.append({'t':t,'m':m,'type':typ,'dimension':d,'rows':r})
 old=public5 if k==5 else public6
 out[name]={'n':n,'k':k,'D':D,'blocks':B,'root_mode':mode,'rows':sum(b['rows'] for b in blocks),'value':float(bound),'bound':str(bound),'public_baseline':str(old),'improvement':float(bound-old),'relative_improvement':float(bound/old-1),'random_ratio':float(bound*2**(k*(k-1)//2-1)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'block_parameters':blocks}
Path('receipts/certificate_summary.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:{a:v[a] for a in ['bound','value','improvement','relative_improvement','rows']} for k,v in out.items()},indent=2))

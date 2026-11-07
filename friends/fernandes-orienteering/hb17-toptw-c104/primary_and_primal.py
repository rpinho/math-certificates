import json, pathlib, hashlib, math, re
from fractions import Fraction as F
import fitz
root=pathlib.Path('.')
rows=[]
for ln in pathlib.Path('sources/official_c104.txt').read_text().splitlines()[2:]:
 z=ln.split()
 if not z: continue
 i=int(z[0]); assert i==len(rows)
 rows.append(dict(x=F(z[1]),y=F(z[2]),s=F(z[3]),p=F(z[4]),o=F(z[-2]),c=F(z[-1])))
def dist(i,j,convention='floor'):
 r,s=rows[i],rows[j];sq=(r['x']-s['x'])**2+(r['y']-s['y'])**2
 # floor(sqrt(sq)*10) computed entirely in integers.
 v=math.isqrt(sq.numerator*100//sq.denominator)
 if convention=='ceil' and F(v*v,100)!=sq: v+=1
 return F(v,10)
routes=json.load(open('input/primal.json'))['routes']
def replay(routes,conv='floor'):
 seen=set();score=F(0);out=[]
 assert len(routes)<=4
 for rr in routes:
  assert rr[0]==rr[-1]==0 and 0 not in rr[1:-1]
  t=rows[0]['o'];trace=[];rs=0
  for i,j in zip(rr,rr[1:]):
   arrival=t+dist(i,j,conv);start=max(arrival,rows[j]['o'])
   assert start<=rows[j]['c'],(j,start,rows[j]['c'])
   if j:
    assert j not in seen;seen.add(j);score+=rows[j]['p'];rs+=rows[j]['p']
   t=start+rows[j]['s'];trace.append(dict(node=j,start=str(start),departure=str(t)))
  assert t<=rows[0]['c'];out.append(dict(route=rr,score=int(rs),finish=str(t),trace=trace))
 return dict(score=int(score),customers=len(seen),routes=out)
receipt={'raw_sha256':hashlib.sha256(pathlib.Path('sources/official_c104.txt').read_bytes()).hexdigest(),'primal':replay(routes)}
try: receipt['ceil_rounding_control']=replay(routes,'ceil')
except AssertionError as e: receipt['ceil_rounding_control']={'rejected':str(e)}
# Deliberately simple control: repeatedly choose the best profit/insertion-time
# among all unused nodes and positions, accepting only a full route replay.
greedy=[[0,0] for _ in range(4)];unused=set(range(1,len(rows)))
def finish(rr):
 t=rows[0]['o']
 for i,j in zip(rr,rr[1:]):
  start=max(t+dist(i,j),rows[j]['o'])
  if start>rows[j]['c']: return None
  t=start+rows[j]['s']
 return t if t<=rows[0]['c'] else None
while True:
 best=None
 for j in sorted(unused):
  for v,rr in enumerate(greedy):
   old=finish(rr)
   for pos in range(1,len(rr)):
    trial=rr[:pos]+[j]+rr[pos:];new=finish(trial)
    if new is None: continue
    key=(rows[j]['p']/max(F(1,10),new-old),rows[j]['p'],-j,-v,-pos)
    if best is None or key>best[0]:best=(key,j,v,trial)
 if best is None:break
 _,j,v,rr=best;greedy[v]=rr;unused.remove(j)
receipt['greedy_control']=replay(greedy)
# Independently extract authentic PDF text and font objects (not supplied text).
primary={}
for filename in ['peng.pdf','retained_sevecek2026_actual.pdf','retained_amarouche_supp.pdf']:
 doc=fitz.open('sources/'+filename);hits=[]
 pathlib.Path('sources/'+filename+'.txt').write_text('\n'.join(p.get_text(sort=True) for p in doc))
 for p in doc:
  txt=p.get_text(sort=True)
  if 'c104' in txt and (filename!='retained_sevecek2026_actual.pdf' or '1260' in txt):
   hits.append(dict(pdf_page=p.number+1,text=txt))
   p.get_pixmap(matrix=fitz.Matrix(1.1,1.1)).save('sources/'+filename+f'.p{p.number+1}.png')
 primary[filename]={'sha256':hashlib.sha256(pathlib.Path('sources/'+filename).read_bytes()).hexdigest(),'pages':len(doc),'hits':hits}
 if filename=='peng.pdf':
  p=doc[28];ss=[]
  for b in p.get_text('dict')['blocks']:
   for ln in b.get('lines',[]):
    for s in ln['spans']:
     if s['text'].strip() in ['1260','c104','c103','1210','popt','760','1030']:
      ss.append(dict(text=s['text'],font=s['font'],bbox=s['bbox']))
  primary[filename]['table6_spans']=ss
pathlib.Path('primary_receipt.json').write_text(json.dumps(primary,indent=2))
pathlib.Path('primal_receipt.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps({k:({x:v for x,v in z.items() if x!='routes'} if isinstance(z,dict) else z) for k,z in receipt.items()},indent=2))
print('PDF hits',[(k,[h['pdf_page'] for h in v['hits']]) for k,v in primary.items()])

"""Separately written (same agent) exact verifier of frozen explicit witnesses.
No import from the search or certificate producer. Standard library only.
Completeness of box enumeration is unnecessary: every retained witness is checked.
Usage: python verify_exact.py ARTIFACT --claim RATIONAL [--out RESULT]
"""
import argparse,hashlib,json,sys,time
from fractions import Fraction
from pathlib import Path

def rational(x):
 if not isinstance(x,str):raise ValueError('rational must be a string')
 return Fraction(x)
def check(path,claim):
 raw=Path(path).read_bytes();c=json.loads(raw);d=c['measure']
 if c['format']!='c47-witness-rectangles-v1':raise ValueError('format')
 px,py,lam=[rational(d[k]) for k in ('Px','Py','lam')]
 if min(px,py,lam)<=0:raise ValueError('positive periods/level required')
 pts=[tuple(rational(x) for x in p) for p in d['pts']]
 if not pts or any(len(p)!=3 for p in pts):raise ValueError('atoms')
 if any(not (0<=x<px and 0<=y<py and m>0) for x,y,m in pts):raise ValueError('invalid atom')
 if len(set((x,y) for x,y,m in pts))!=len(pts):raise ValueError('duplicate atom')
 mass=sum(p[2] for p in pts);rectangles=[];min_slack=None
 for w in c['witnesses']:
  a,b,e,f=map(rational,w['box']);r=rational(w['radius']);u,v,s,t=map(rational,w['rectangle'])
  if not (a<=b and e<=f and r>0 and 0<=u<v<=px and 0<=s<t<=py):raise ValueError('invalid box/rectangle')
  # Enumerate each periodic atom actually inside this box; exact floor/ceil.
  total=Fraction(0)
  for x,y,m in pts:
   ilo=-((x-a)//px);ihi=(b-x)//px;jlo=-((y-e)//py);jhi=(f-y)//py
   count=max(0,ihi-ilo+1)*max(0,jhi-jlo+1)
   total+=count*m
  slack=total-4*lam*r*r
  if slack<=0:raise ValueError('witness lacks strict mass margin')
  if not (u>=b-r and v<=a+r and s>=f-r and t<=e+r):raise ValueError('rectangle not inside witness')
  min_slack=slack if min_slack is None else min(min_slack,slack)
  rectangles.append((u,v,s,t))
 if not rectangles:raise ValueError('empty certificate')
 # Exact union: vertical slabs and merged active y intervals. No segment tree.
 events={}
 for i,(u,v,s,t) in enumerate(rectangles):events.setdefault(u,[]).append((1,i));events.setdefault(v,[]).append((-1,i))
 active=set();last=None;area=Fraction(0)
 for x,changes in sorted(events.items()):
  if last is not None and active:
   length=Fraction(0);start=end=None
   for a,b in sorted((rectangles[i][2],rectangles[i][3]) for i in active):
    if end is None:start,end=a,b
    elif a>end:length+=end-start;start,end=a,b
    else:end=max(end,b)
   if end is not None:length+=end-start
   area+=(x-last)*length
  for sign,i in changes:
   if sign==1:active.add(i)
   else:active.remove(i)
  last=x
 if active:raise ValueError('unbalanced events')
 ratio=lam*area/mass
 if ratio<claim:raise ValueError('ratio '+str(ratio)+' is below claim '+str(claim))
 return {'result':'PASS','artifact_sha256':hashlib.sha256(raw).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'ratio':str(ratio),'ratio_float':float(ratio),'claim':str(claim),'area':str(area),'mass':str(mass),'rectangles':len(rectangles),'min_strict_mass_slack':str(min_slack),'verification':'separately written (same agent), exact rational arithmetic','status':'candidate, unrefereed'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('artifact');ap.add_argument('--claim',required=True);ap.add_argument('--out');a=ap.parse_args();t=time.time()
 try:out=check(a.artifact,Fraction(a.claim));out['seconds']=time.time()-t
 except Exception as e:out={'result':'FAIL','error':str(e),'seconds':time.time()-t}
 if a.out:Path(a.out).write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));sys.exit(0 if out['result']=='PASS' else 1)

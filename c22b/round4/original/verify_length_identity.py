"""Separately written (same agent), exact speed-polynomial checker.

Uses quadratic-field arithmetic from velocity components, no geometry or
producer imports. eta=1/s and eta²=1/(R²+h²).
"""
import json,pathlib,hashlib,sys
from fractions import Fraction as F
from flint import arb,ctx,fmpq
ctx.prec=220
class Reject(Exception):pass
def need(c,e):
 if not c:raise Reject(e)
def rational(s):
 need(type(s) is str,'E_SPEED_RATIONAL')
 try:return F(s)
 except Exception:raise Reject('E_SPEED_RATIONAL')
def ball(x):return arb(fmpq(x.numerator,x.denominator))
def check(folder,certificate=None):
 P=pathlib.Path(folder);raw=(P/'CONSTRUCTION.json').read_bytes();D=json.loads(raw);d=certificate if certificate is not None else json.loads((P/'length_identity.json').read_text())
 need(set(d)=={'kind','artifact_sha256','quadratic_relation','rows'},'E_SPEED_SCHEMA');need(d['kind']=='exact_speed_identity_v1','E_SPEED_KIND');need(d['artifact_sha256']==hashlib.sha256(raw).hexdigest(),'E_SPEED_HASH')
 p=D['parameters'];N=rational(p['N']);R=rational(p['R']);h=(N-1)*rational(p['reference_pitch']);S=R*R+h*h;need(S>0,'E_SPEED_FIELD');relation=1/S
 need(rational(d['quadratic_relation'])==relation,'E_SPEED_RELATION')
 def add(x,y):return (x[0]+y[0],x[1]+y[1])
 def mul(x,y):return (x[0]*y[0]+relation*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
 def scale(x,c):return (c*x[0],c*x[1])
 def sq(x):return mul(x,x)
 def pair(x):
  need(isinstance(x,list) and len(x)==2,'E_SPEED_PAIR');return tuple(map(rational,x))
 need(isinstance(d['rows'],list) and len(d['rows'])==2,'E_SPEED_ROWS');radii=[rational(p['outer_radius']),-rational(p['inner_radius'])];means=[]
 for r,row in zip(radii,d['rows']):
  need(set(row)=={'signed_radius','coefficients','mean'},'E_SPEED_ROW_SCHEMA');need(rational(row['signed_radius'])==r,'E_SPEED_RADII')
  vx=(r,-r*h/N);vy=(-r/F(N),r*h);vz=(F(0),-r*R);y0=(R/N,F(0));z0=(h/N,F(0))
  c0=add(add(sq(vx),sq(y0)),sq(z0));c1=scale(add(mul(y0,vy),mul(z0,vz)),2);c2=add(add(sq(vy),sq(vz)),scale(sq(vx),-1));expected=[c0,c1,c2]
  need(isinstance(row['coefficients'],list) and len(row['coefficients'])==3,'E_SPEED_COEFFICIENTS')
  need([pair(x) for x in row['coefficients']]==expected,'E_SPEED_COEFFICIENT')
  mean=add(c0,scale(c2,F(1,2)));need(pair(row['mean'])==mean,'E_SPEED_MEAN');means.append(mean)
 eta=1/ball(S).sqrt();real_means=[ball(x)+ball(y)*eta for x,y in means];need(all(x>0 for x in real_means),'E_SPEED_MEAN_POSITIVE')
 coefficient=ball(rational(p['scale']))*arb.pi()*sum(x.sqrt() for x in real_means);need(coefficient<ball(rational(D['claim']['coefficient'])),'E_SPEED_BOUND')
 return {'verdict':'EXACT_SPEED_POLYNOMIAL_PASS_CANDIDATE_UNREFEREED','verifier':'separately written (same agent)','field':'Q(eta), eta^2=1/(R^2+h^2), eta>0','rows':2,'coefficient_interval':coefficient.str(35),'qualification':'speed identity and Jensen scalar only; full bound also needs body/caps and topology'}
if __name__=='__main__':
 try:print(json.dumps(check(sys.argv[1]),indent=2))
 except Reject as e:print(str(e));sys.exit(1)

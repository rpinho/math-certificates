"""Separately written (same agent) checker for the direct superhelix artifact.

Imports no discovery, cover-builder, or search modules. Arb geometry is
implemented using Frenet vectors and circle-center coordinates. Topology
is exact integer coloring algebra; its geometric justification is in PROOF.md.
"""
import sys,json,pathlib,hashlib,copy,gzip
from fractions import Fraction
from flint import arb,fmpq,ctx
ctx.prec=220
class Reject(Exception):pass
def need(x,code):
 if not x:raise Reject(code)
def frac(s):
 need(type(s) is str,'E_RATIONAL_STRING')
 try:return Fraction(s)
 except Exception:raise Reject('E_RATIONAL')
def B(x):
 if not isinstance(x,Fraction):x=Fraction(x)
 return arb(fmpq(x.numerator,x.denominator))
def box(lo,hi):
 need(lo<=hi,'E_INTERVAL_ORDER');c=(lo+hi)/2;r=(hi-lo)/2
 return arb(fmpq(c.numerator,c.denominator),fmpq(r.numerator,r.denominator))
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def plus(x,y):return [a+b for a,b in zip(x,y)]
def minus(x,y):return [a-b for a,b in zip(x,y)]
def times(x,v):return [v*a for a in x]
def mm(A,Bb):return [[sum(A[i][k]*Bb[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mp(A,n):
 out=[[1,0],[0,1]]
 while n:
  if n%2:out=mm(out,A)
  A=mm(A,A);n//=2
 return out
class Checker:
 def __init__(self,artifact):
  self.d=artifact
  need(set(artifact)=={'kind','status','parameters','claim','certificate_domains','credits','closure'},'E_ARTIFACT_SCHEMA')
  need(artifact['kind']=='c22b_rational_superhelix_knot_splitcaps_v1','E_KIND')
  need(artifact['status']=='candidate and unrefereed','E_STATUS')
  p=artifact['parameters'];c=artifact['claim']
  need(set(p)=={'N','R','outer_radius','inner_radius','reference_pitch','scale','cap_radius','inner_cap_radius','core_periods'},'E_PARAMETER_SCHEMA')
  need(type(p['N']) is str,'E_N')
  nf=frac(p['N']);need(2<=nf<=1000000,'E_N')
  need(type(p['core_periods']) is int and p['core_periods']==nf.denominator,'E_PERIODS')
  self.turns=nf.numerator;self.periods=nf.denominator;self.N=B(nf);self.R=B(frac(p['R']));self.a=B(frac(p['outer_radius']));self.i=B(frac(p['inner_radius']));self.b=B(frac(p['reference_pitch']));self.lam=B(frac(p['scale']));self.Q=B(frac(p['cap_radius']));self.Qinner=B(frac(p['inner_cap_radius']))
  need(self.R>0 and self.a>self.i and self.i>0 and self.b>0 and self.lam>=1 and self.Q>2 and self.Qinner>2,'E_PARAMETER_RANGE')
  need(set(c)=={'coefficient','bar','additive','crossings_slope','crossings_intercept','n_min','components'},'E_CLAIM_SCHEMA')
  need(c['components']==1,'E_COMPONENT_COUNT')
  need(isinstance(artifact['closure'],dict) and set(artifact['closure'])=={'lower','upper','vertical_clearance'} and artifact['closure']['lower']=='nested_semicircles' and artifact['closure']['upper']=='swapped_parallel_semicircles','E_CLOSURE_MODE')
  self.claim=B(frac(c['coefficient']));self.additive=B(frac(c['additive']))
  need(frac(c['bar'])==Fraction(36,5),'E_BAR')
  need(self.claim<=B(Fraction(36,5)) and self.claim>0,'E_CLAIM_BAR')
  need(c['crossings_slope']==4*self.turns and c['crossings_intercept']==3 and c['n_min']==1,'E_CROSSING_FORMULA')
  need(artifact['certificate_domains']=={'body_phase':['0','44/7'],'outer_difference':['3/2','9'],'cross_difference':['-9','9'],'body_interface_phase':['-8','0'],'connector_length':['0','16']},'E_DOMAINS')
  self.h=(self.N-1)*self.b;self.s=(self.R**2+self.h**2).sqrt();self.omega=self.N-self.h/self.s;self.pitch=self.s/self.omega
  self.k=self.R/self.s**2;self.tau=self.h/self.s**2
  self.upper=1+self.k*self.a;self.lower=1-self.k*self.a
  self.hessian=3*self.k+self.a*self.k*self.tau+self.a*self.k**2
  self.rs=[-self.i,self.a,self.a,-self.i];self.cs=[-1,-1,1,1];self.qs=[self.Qinner,self.Q,self.Q,self.Qinner]
  self.speeds=[self.lam*((self.s/self.N)**2*(1+self.k*abs(r))**2+(r*self.omega/self.N)**2).sqrt() for r in self.rs]
  self.ends=[]
  for j in range(4):
   r=self.rs[j];c=self.cs[j];v=[B(0),c*(self.R-r+r*self.h/self.s*self.N),self.h-r*self.R/self.s*self.N]
   norm=dot(v,v).sqrt();T=times(v,1/norm);e=1 if T[1]*c>0 else -1
   W=[B(0),-c*e*T[2],e*T[1]*c]
   origin=[self.lam*c*(self.R-r),B(0),B(0)]
   self.ends.append((origin,T,W,e))

 def scalar(self):
  a,i,R=self.a,self.i,self.R;lam=self.lam;N=self.N;s=self.s;h=self.h
  need(h**2>R**2 and a+1<R,'E_CORE_TUBE')
  need(2*R-2*a>2,'E_CROSS_BUNDLE')
  need(a*h/s-i>(a+i)*R**2/(s*h),'E_FLATTEN_WITHIN_BUNDLE')
  need(2*R-2*a-2*a*R**2/(s*h)>0,'E_FLATTEN_CROSS_BUNDLE')
  need(B(Fraction(44,7))>2*arb.pi(),'E_PHASE_COVER')
  need(lam*(h/N-a*R/s)>0,'E_Z_MONOTONE')
  need(B(Fraction(3,2))*self.speeds[1]<arb.pi(),'E_OUTER_SHORT_ARC')
  need(9*self.speeds[0]<arb.pi(),'E_INNER_SHORT_ARC')
  need(lam*(9*h/N-2*a*R/s)>2,'E_BODY_TAIL')
  need(lam*(8*h/N-a*R/s)>2,'E_BODY_END_ZONE')
  need(lam*2*arb.pi()*h>2,'E_END_SEPARATION')
  means=[(s/N)**2*(1+(self.k*r)**2/2)+(r*self.omega/N)**2 for r in [a,-i]]
  length=lam*arb.pi()*sum(x.sqrt() for x in means)
  need(length<self.claim,'E_LENGTH_COEFFICIENT')
  caps=[]
  for j in [2,3]:
   origin,T,W,e=self.ends[j];c=T[2];p=T[1];Qj=self.qs[j]
   need(c>0 and c<1 and ((j==2 and p>0) or (j==3 and p<0)),'E_CAP_TANGENT_SIGN')
   connector_length=Qj*c.acos();need(connector_length>0,'E_CAP_CONNECTOR_LENGTH')
   if connector_length>16:need(16*c>2 or abs(self.cap(j,B(16))[1])>lam*(R+a)+2,'E_CAP_END_ZONE')
   else:need(connector_length<=16,'E_CAP_CONNECTOR_LENGTH')
   X=origin[0];Y=e*Qj*(1-c);Z=Qj*abs(p);D=(X*X+Y*Y).sqrt();theta=c.acos()
   if j==2:need(X>1 and D>4 and abs(Y)*B(3).sqrt()/2>2,'E_CAP_SIZE')
   else:need(X>2 and D>1,'E_CAP_SIZE')
   caps.append((X,Y,Z,D,theta,c,abs(p)))
  po,mi=caps;Xp,Yp,Zp,Dp,tp,cp,sp=po;Xm,Ym,Zm,Dm,tm,cm,sm=mi
  need(Xm-Xp>2,'E_CONNECTOR_PLANES')
  need(Zp-Zm-Dm>2 and Zm>2,'E_CAP_VERTICAL_SEPARATION')
  clearance=B(frac(self.d['closure']['vertical_clearance']))
  need(clearance>2,'E_UPPER_CLEARANCE')
  ym=abs(Ym);need(Yp>ym,'E_UPPER_CHORD_DIRECTION')
  norm=((Xm+Xp)**2+(Yp-ym)**2).sqrt();D=norm/2;Zstar=Zp+clearance
  plane_distance=2*(Xm*Yp+Xp*ym)/norm
  need(D>4 and plane_distance>2,'E_UPPER_PARALLEL_PLANES')
  top_length=2*(self.Q*tp+self.Qinner*tm)+4*Zstar-2*(Zp+Zm)+arb.pi()*norm
  bottom_length=2*(self.Q*tp+self.Qinner*tm)+arb.pi()*(Dp+Dm)
  E=top_length+bottom_length
  need(E<self.additive,'E_ADDITIVE_LENGTH')
  self.body_coefficient=length;self.cap_length=E
  return {'length_coefficient_upper':length.str(35),'cap_total_length':E.str(35),'upper_plane_distance':plane_distance.str(35),'upper_semicircle_radius':D.str(35),'phase_cover_margin':(B(Fraction(44,7))-2*arb.pi()).str(25),'end_zone_clearance':(lam*(8*h/N-a*R/s)).str(25),'outer_short_arc_upper':(B(Fraction(3,2))*self.speeds[1]).str(25),'inner_short_arc_upper':(9*self.speeds[0]).str(25)}

 def point(self,j,u,velocity=False,acceleration=False):
  # Frenet frame, rather than the builder's cylindrical coefficients.
  r=self.rs[j];c=self.cs[j];t=u/self.N;phase=-u;co=t.cos();si=t.sin();C=phase.cos();S=phase.sin()
  core=[c*self.R*co,c*self.R*si,self.h*t]
  normal=[-c*co,-c*si,B(0)]
  binormal=[c*self.h/self.s*si,-c*self.h/self.s*co,self.R/self.s]
  if not velocity and not acceleration:return times(plus(core,times(plus(times(normal,C),times(binormal,S)),r)),self.lam)
  dc=[-c*self.R*si/self.N,c*self.R*co/self.N,self.h/self.N]
  dn=[c*si/self.N,-c*co/self.N,B(0)]
  db=[c*self.h/self.s*co/self.N,c*self.h/self.s*si/self.N,B(0)]
  if acceleration:
   ddc=[-c*self.R*co/self.N**2,-c*self.R*si/self.N**2,B(0)]
   ddn=[c*co/self.N**2,c*si/self.N**2,B(0)]
   ddb=[-c*self.h/self.s*si/self.N**2,c*self.h/self.s*co/self.N**2,B(0)]
   normal_term=plus(plus(times(normal,-C),times(dn,2*S)),times(ddn,C))
   binormal_term=plus(plus(times(binormal,-S),times(db,-2*C)),times(ddb,S))
   return times(plus(ddc,times(plus(normal_term,binormal_term),r)),self.lam)
  dv=plus(plus(times(normal,S),times(dn,C)),plus(times(binormal,-C),times(db,S)))
  return times(plus(dc,times(dv,r)),self.lam)
 def cap(self,j,l,velocity=False):
  origin,T,W,e=self.ends[j];Qj=self.qs[j];angle=l/Qj
  if velocity:return plus(times(T,angle.cos()),times(W,angle.sin()))
  center=plus(origin,times(W,Qj))
  return plus(center,times(plus(times(T,angle.sin()),times(W,-angle.cos())),Qj))

 def lower_inner_semicircle(self,x,velocity=False):
  origin,T,W,e=self.ends[3];Qj=self.qs[3];X=origin[0];Y=e*Qj*(1-T[2]);Z=Qj*abs(T[1]);D=(X*X+Y*Y).sqrt();theta=arb.pi()*x
  if velocity:return [-arb.pi()*X*theta.sin(),-arb.pi()*Y*theta.sin(),arb.pi()*D*theta.cos()]
  return [X*theta.cos(),Y*theta.cos(),Z+D*theta.sin()]
 def leaf(self,kind,j,k,bounds,reason):
  if kind.startswith('curvature'):
   need(reason=='curvature','E_LEAF_REASON');u=box(*bounds);idx=1 if kind=='curvature_outer' else 0
   v=self.point(idx,u,True);acc=self.point(idx,u,acceleration=True)
   cross=[v[1]*acc[2]-v[2]*acc[1],v[2]*acc[0]-v[0]*acc[2],v[0]*acc[1]-v[1]*acc[0]]
   V=dot(v,v);need(V>0 and V**3-dot(cross,cross)>0,'E_CURVATURE_LEAF');return
  u0,u1,l0,l1=bounds
  if kind=='lower_cap_pair':
   need(j in [1,2] and k==3 and reason in ['natural','mean'],'E_CAP_PAIR_METADATA')
   X=box(u0,u1);Y=box(l0,l1);xm=(u0+u1)/2;ym=(l0+l1)/2
   L=self.qs[j]*self.ends[j][1][2].acos()
   D=minus(self.cap(j,L*X),self.lower_inner_semicircle(Y));mid=minus(self.cap(j,L*B(xm)),self.lower_inner_semicircle(B(ym)))
   if reason=='natural':need(dot(D,D)>4,'E_CAP_PAIR_DISTANCE');return
   dx=times(self.cap(j,L*X,True),L);dy=times(self.lower_inner_semicircle(Y,True),-1)
   bound=dot(mid,mid)+2*dot(D,dx)*box(u0-xm,u1-xm)+2*dot(D,dy)*box(l0-ym,l1-ym)
   need(bound>4,'E_CAP_PAIR_DISTANCE');return
  if kind=='interface' and reason=='short_arc':
   need(j==k and B(-u0)*self.speeds[j]+B(l1)<arb.pi(),'E_SHORT_ARC_LEAF');return
  need(reason in ['natural','mean'],'E_LEAF_REASON')
  U=box(u0,u1);L=box(l0,l1);um=(u0+u1)/2;lm=(l0+l1)/2
  if kind=='interface':
   D=minus(self.point(j,U),self.cap(k,L));mid=minus(self.point(j,B(um)),self.cap(k,B(lm)))
   vx=self.point(j,U,True);vy=times(self.cap(k,L,True),-1)
  else:
   jj=1;kk=1 if kind=='body_outer' else 0
   D=minus(self.point(jj,U),self.point(kk,U+L));mid=minus(self.point(jj,B(um)),self.point(kk,B(um+lm)))
   vx=minus(self.point(jj,U,True),self.point(kk,U+L,True));vy=times(self.point(kk,U+L,True),-1)
  if reason=='natural':need(dot(D,D)>4,'E_DISTANCE_LEAF');return
  bound=dot(mid,mid)+2*dot(D,vx)*box(u0-um,u1-um)+2*dot(D,vy)*box(l0-lm,l1-lm)
  need(bound>4,'E_DISTANCE_LEAF')
 def cover(self,d,artifact_bytes):
  need(set(d)=={'kind','j','k','artifact_sha256','leaves'},'E_COVER_SCHEMA')
  need(d['artifact_sha256']==hashlib.sha256(artifact_bytes).hexdigest(),'E_ARTIFACT_HASH')
  kind=d['kind'];j=d['j'];k=d['k'];need(kind in ['body_outer','body_cross','curvature_outer','curvature_inner','interface','lower_cap_pair'],'E_COVER_KIND')
  need(type(j) is int and type(k) is int and 0<=j<4 and 0<=k<4,'E_COVER_INDEX')
  if kind not in ['interface','lower_cap_pair']:need(j==k==0,'E_BODY_INDEX')
  if kind=='lower_cap_pair':need(j in [1,2] and k==3,'E_CAP_PAIR_INDEX')
  need(isinstance(d['leaves'],list) and 0<len(d['leaves'])<=3000000,'E_LEAVES')
  tree={}
  for row in d['leaves']:
   need(isinstance(row,list) and len(row)==2,'E_LEAF_SCHEMA');path,reason=row
   need(type(path) is str and len(path)<=60 and all(x in '01' for x in path),'E_PATH')
   node=tree
   for char in path:
    need('leaf' not in node,'E_PREFIX_OVERLAP');node=node.setdefault(char,{})
   need(not node,'E_DUPLICATE_OR_PREFIX');node['leaf']=reason
  if kind.startswith('curvature'):bounds=tuple(map(Fraction,['0','44/7']))
  elif kind=='interface':bounds=tuple(map(Fraction,['-8','0','0','16']))
  elif kind=='lower_cap_pair':bounds=tuple(map(Fraction,['0','1','0','1']))
  elif kind=='body_outer':bounds=tuple(map(Fraction,['0','44/7','3/2','9']))
  else:bounds=tuple(map(Fraction,['0','44/7','-9','9']))
  def visit(node,Bb,depth):
   if 'leaf' in node:
    need(set(node)=={'leaf'},'E_PREFIX_OVERLAP')
    try:self.leaf(kind,j,k,Bb,node['leaf'])
    except Reject:
     print(json.dumps({'kind':kind,'j':j,'k':k,'bounds':list(map(str,Bb)),'reason':node['leaf']}),file=sys.stderr);raise
    return
   need(set(node)=={'0','1'},'E_COVER_GAP')
   axis=depth%2 if len(Bb)==4 else 0;ix=2*axis;mid=(Bb[ix]+Bb[ix+1])/2;left=list(Bb);right=list(Bb);left[ix+1]=mid;right[ix]=mid
   visit(node['0'],tuple(left),depth+1);visit(node['1'],tuple(right),depth+1)
  visit(tree,bounds,0);return (kind,j,k,len(d['leaves']))

 def topology(self):
  matrices=[]
  for index in range(3):
   cols=[]
   for p,q in [(1,0),(0,1)]:
    C=[p+q,q,0,p];x,y=C[index:index+2];C[index:index+2]=[2*x-y,x]
    need(C[0]-C[1]+C[2]-C[3]==0,'E_COLOR_DIAGONAL');cols.append([C[0]-C[1],C[1]-C[2]])
   matrices.append([[cols[j][i] for j in range(2)] for i in range(2)])
  U=matrices[0];V=matrices[1]
  need(U==matrices[2] and U==[[1,0],[1,1]] and V==[[1,-1],[0,1]],'E_COLOR_GENERATORS')
  need(mm(U,[[1,0],[-1,1]])==[[1,0],[0,1]] and mm(V,[[1,1],[0,1]])==[[1,0],[0,1]],'E_NEGATIVE_ACTIONS')
  need(mm(U,mm(V,U))==mm(V,mm(U,V)),'E_BRAID_RELATION')
  beta=mm(V,mm(U,mm(U,V)));beta_inv=[[-1,0],[-2,-1]]
  need(mm(beta,beta_inv)==[[1,0],[0,1]],'E_CABLE_INVERSE')
  body=mm(mp(beta_inv,2*self.periods),mp(U,4*(self.turns-self.periods)))
  need(body==[[1,0],[4*self.turns,1]],'E_BODY_MATRIX')
  J=[[body[i][j]-int(i==j) for j in range(2)] for i in range(2)]
  need(mm(J,J)==[[0,0],[0,0]],'E_ALL_N_NILPOTENT')
  for c0,c1 in [(0,1),(1,0),(1,1)]:
   # Single upper crossing: arc0--2 over arc1--3.
   c2=c0;c3=2*c0-c1;p=c0-c1;q=c1-c2
   need(q==-p and c0-c1+c2-c3==0,'E_UPPER_CAP_COLORS')
   # Lower nested clasp: inner-left over outer-left; outer-right over inner-right.
   c3=2*c1-c0;c2=2*c3-c1;p=c0-c1;q=c1-c2
   need(q==2*p and c0-c1+c2-c3==0,'E_LOWER_CAP_COLORS')
  constant=mm(U,mp(U,2));slope=mm(U,mm(J,mp(U,2)))
  need(constant==[[1,0],[3,1]] and slope==[[0,0],[4*self.turns,0]],'E_CLOSURE_ALL_N')
  # Material permutation and closure component count, checked separately.
  order=list(range(4));bands=[0,1,1,0];direction=[-1,-1,1,1]
  def apply(word):
   signed_between_bands=0
   for g in word:
    z=abs(g)-1;l,r=order[z:z+2]
    if bands[l]!=bands[r]:signed_between_bands+=(1 if g>0 else -1)*direction[l]*direction[r]
    order[z:z+2]=[r,l]
   return signed_between_bands
  cable=apply([-2,-3,-1,-2]*2)
  need(order==list(range(4)) and cable==4,'E_CABLE_MATERIAL')
  pair1=apply([1,1]);pair3=apply([3,3])
  need(order==list(range(4)) and pair1==pair3==2,'E_INTERNAL_MATERIAL')
  need(self.periods*cable+(self.turns-self.periods)*(pair1+pair3)==4*self.turns,'E_BODY_BAND_COUNT')
  parent=list(range(4))
  def root(i):
   while parent[i]!=i:i=parent[i]
   return i
  for l,r in [(0,3),(1,2),(0,2),(1,3)]:parent[root(l)]=root(r)
  need(len({root(i) for i in range(4)})==1,'E_CLOSURE_COMPONENTS')
  need(4*self.turns+3>=3 and (4*self.turns)%2==0,'E_TORUS_DIAGRAM_RANGE')
  return {'body_matrix':body,'nilpotent_increment':J,'closure_constant_matrix':constant,'closure_n_coefficient':slope,'crossings':'4*P*n+3','knot':'T(2,4*P*n+3), up to mirror','components':1,'qualification':'expected body action and cap algebra; the actual physical word is checked by verify_projection.py, with the rational tangle argument in PROOF.md'}

def check_bundle(raw,documents):
 C=Checker(json.loads(raw));scalars=C.scalar();top=C.topology();seen=set();leaves=0
 for d in documents:
  row=C.cover(d,raw);need(row[:3] not in seen,'E_DUPLICATE_COVER');seen.add(row[:3]);leaves+=row[3]
 expected={('interface',j,k) for j in range(4) for k in range(4)}|{('lower_cap_pair',j,3) for j in [1,2]}|{(kind,0,0) for kind in ['body_outer','body_cross','curvature_outer','curvature_inner']}
 need(seen==expected,'E_MISSING_COVER')
 return {'verdict':'DIRECT_KNOT_GEOMETRY_CHECKS_PASS_CANDIDATE_UNREFEREED','verifier':'separately written (same agent)','precision_bits':ctx.prec,'covers':len(seen),'leaves':leaves,'scalars':scalars,'topology':top,'scope':'finite arithmetic plus analytic and topological proof in PROOF.md; not a formal proof assistant'}
def check_folder(folder):
 P=pathlib.Path(folder);return check_bundle((P/'CONSTRUCTION.json').read_bytes(),[json.loads(gzip.decompress(p.read_bytes())) for p in sorted((P/'covers').glob('*.json.gz'))])
if __name__=='__main__':
 try:print(json.dumps(check_folder(sys.argv[1]),indent=2))
 except Reject as e:print(str(e));sys.exit(1)

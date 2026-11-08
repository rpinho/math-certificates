"""Separately written (same agent), physical braid projection verifier.

Imports only the separate verification geometry, never any producer/search.
Inverse phases are verified by exact rational brackets plus Arb signs.
"""
import json,gzip,pathlib,sys,hashlib
from fractions import Fraction as F
from flint import arb
from verify import Checker,Reject,need,B,box,mm

def Q(s):
 need(type(s) is str,'E_PROJECTION_RATIONAL')
 try:return F(s)
 except Exception:raise Reject('E_PROJECTION_RATIONAL')
def opposite(a,b):return (a<0 and b>0) or (a>0 and b<0)
class Projection:
 def __init__(self,construction_bytes,certificate):
  self.raw=construction_bytes;self.d=certificate;self.C=Checker(json.loads(construction_bytes));self.C.scalar();self.C.topology()
  need(set(certificate)=={'kind','status','artifact_sha256','projection','inverse_brackets','covers','word'},'E_PROJECTION_SCHEMA')
  need(certificate['kind']=='physical_body_braid_projection_v1','E_PROJECTION_KIND')
  need(certificate['status']=='candidate and unrefereed','E_PROJECTION_STATUS')
  need(certificate['artifact_sha256']==hashlib.sha256(construction_bytes).hexdigest(),'E_PROJECTION_HASH')
  need(certificate['projection']==[7,1],'E_PROJECTION_VECTOR')
  C=self.C
  need(all(z>0 for z in C.zmin),'E_HEIGHT_MONOTONE')
  self.inverse={};self.used=set();self.memo={};self.events=[]
  inv=certificate['inverse_brackets'];need(isinstance(inv,dict) and len(inv)<=1000000,'E_INVERSE_SCHEMA')
  for key,value in inv.items():
   x=Q(key);need(str(x)==key and 0<=x<=1,'E_INVERSE_KEY')
   need(isinstance(value,list) and len(value)==2,'E_INVERSE_SCHEMA');rows=[]
   for j,row in enumerate(value):
    need(isinstance(row,list) and len(row)==2,'E_INVERSE_SCHEMA');lo,hi=map(Q,row);need(lo<hi,'E_INVERSE_BRACKET')
    loB=B(lo);hiB=B(hi);rhs=2*arb.pi()*C.turns*B(x)
    need(self.height_phase(j,loB)-rhs<0,'E_INVERSE_LOWER')
    need(self.height_phase(j,hiB)-rhs>0,'E_INVERSE_UPPER')
    rows.append((lo,hi))
   self.inverse[key]=rows
 def height_phase(self,j,u):
  C=self.C;r=C.radius(j+2,u)[0];v=C.phase(u)[0]
  return u-C.N*C.R/(C.s*C.h)*r*v.sin()
 def domain(self,j,lo,hi):
  for x in [lo,hi]:
   key=str(x);need(key in self.inverse,'E_MISSING_INVERSE');self.used.add(key)
  return box(self.inverse[str(lo)][j][0],self.inverse[str(hi)][j][1])
 def values(self,lo,hi):
  key=(lo,hi)
  if key in self.memo:return self.memo[key]
  C=self.C;result=[]
  for j in range(2):
   u=self.domain(j,lo,hi);p=C.point(j+2,u);tangent=C.point(j+2,u,True)
   f=7*p[0]+p[1];g=7*p[1]-p[0]
   denominator=tangent[2]*C.N/(C.lam*C.h);need(denominator>0,'E_PHASE_DERIVATIVE')
   df=(7*tangent[0]+tangent[1])*(2*arb.pi()*C.turns)/denominator
   result.append((f,df,g))
  self.memo[key]=result;return result
 def function(self,kind,lo,hi,index=0):
  values=self.values(lo,hi);a=values[0][index];i=values[1][index]
  return a-i if kind=='m' else a+i if kind=='p' else a if kind=='a' else i
 def cover(self,kind,leaves):
  need(isinstance(leaves,list) and 0<len(leaves)<=1000000,'E_PROJECTION_LEAVES');tree={}
  for row in leaves:
   need(isinstance(row,list) and len(row) in [2,3],'E_PROJECTION_LEAF_SCHEMA');path=row[0]
   need(type(path) is str and len(path)<=50 and all(c in '01' for c in path),'E_PROJECTION_PATH')
   need((row[1]=='empty' and len(row)==2) or (row[1]=='root' and len(row)==3),'E_PROJECTION_LEAF_KIND')
   node=tree
   for bit in path:
    need('leaf' not in node,'E_PROJECTION_PREFIX');node=node.setdefault(bit,{})
   need(not node,'E_PROJECTION_DUPLICATE');node['leaf']=row[1:]
  def visit(node,lo,hi,path):
   if 'leaf' in node:
    need(set(node)=={'leaf'},'E_PROJECTION_PREFIX');row=node['leaf']
    if row[0]=='empty':
     value=self.function(kind,lo,hi)
     if not (value>0 or value<0):print(json.dumps({'function':kind,'path':path,'bounds':[str(lo),str(hi)],'enclosure':value.str(20)}),file=sys.stderr)
     need(value>0 or value<0,'E_FALSE_EMPTY');return
    need(isinstance(row[1],list) and len(row[1])==2,'E_ROOT_SCHEMA');L,H=map(Q,row[1]);need(L<H,'E_ROOT_INTERVAL');need(lo<=L and H<=hi,'E_ROOT_OUTSIDE_LEAF')
    derivative=self.function(kind,lo,hi,1);need(derivative>0 or derivative<0,'E_ROOT_DERIVATIVE')
    need(opposite(self.function(kind,L,L),self.function(kind,H,H)),'E_ROOT_SIGNS')
    self.events.append((L,H,kind,path));return
   need(set(node)=={'0','1'},'E_PROJECTION_COVER_GAP');mid=(lo+hi)/2
   visit(node['0'],lo,mid,path+'0');visit(node['1'],mid,hi,path+'1')
  visit(tree,F(0),F(1),'')
 def check(self):
  covers=self.d['covers'];need(isinstance(covers,dict) and set(covers)=={'m','p','a','i'},'E_PROJECTION_COVER_SET')
  for kind in ['m','p','a','i']:self.cover(kind,covers[kind])
  events=sorted(self.events)
  for a,b in zip(events,events[1:]):need(a[1]<b[0],'E_ROOT_ORDER')
  order=list(range(4));word=[];matrix=[[1,0],[0,1]];root_counts={k:0 for k in covers}
  for lo,hi,kind,path in events:
   root_counts[kind]+=1;vals=self.values(lo,hi);Ga=vals[0][2];Gi=vals[1][2];depth=[-Gi,-Ga,Ga,Gi]
   pairs={'m':[(0,1),(2,3)],'p':[(0,2),(1,3)],'a':[(1,2)],'i':[(0,3)]}[kind]
   pairs=sorted(pairs,key=lambda p:min(order.index(p[0]),order.index(p[1])))
   for j,k in pairs:
    x=order.index(j);y=order.index(k);need(abs(x-y)==1,'E_PAIR_ADJACENCY');ix=min(x,y);left,right=order[ix:ix+2];gap=depth[left]-depth[right]
    need(gap>0 or gap<0,'E_DEPTH_SIGN');sign=1 if gap>0 else -1;g=sign*(ix+1);word.append(g)
    G=[[1,0],[sign,1]] if ix in [0,2] else [[1,-sign],[0,1]];matrix=mm(G,matrix);order[ix:ix+2]=[right,left]
  need(order==list(range(4)),'E_PROJECTION_FINAL_ORDER')
  claimed=self.d['word'];need(isinstance(claimed,list) and all(type(g) is int and 0<abs(g)<4 for g in claimed),'E_WORD_SCHEMA');need(word==claimed,'E_WORD_MISMATCH')
  need(matrix==[[1,0],[4*self.C.turns,1]],'E_PHYSICAL_BODY_ACTION')
  need(self.used==set(self.inverse),'E_UNUSED_INVERSE')
  return {'verdict':'PHYSICAL_BRAID_PROJECTION_PASS_CANDIDATE_UNREFEREED','verifier':'separately written (same agent)','projection':[7,1],'inverse_witnesses':len(self.inverse),'leaves':sum(map(len,covers.values())),'root_events':len(events),'roots_by_function':root_counts,'raw_crossings':len(word),'body_matrix':matrix,'permutation':order,'qualification':'complete physical body braid check; full bound also requires geometry/caps and PROOF.md'}
def check(folder,certificate=None):
 P=pathlib.Path(folder);raw=(P/'CONSTRUCTION.json').read_bytes();d=certificate if certificate is not None else json.loads(gzip.decompress((P/'projection.json.gz').read_bytes()));return Projection(raw,d).check()
if __name__=='__main__':
 try:print(json.dumps(check(sys.argv[1]),indent=2))
 except Reject as e:print(str(e));sys.exit(1)

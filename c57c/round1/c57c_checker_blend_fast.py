"""Checker-only convex interpolation of two independently prepared duals."""
from fractions import Fraction as Q
from flint import arb
from verify_c57c_center6 import require,rational
from c57c_checker_core_fast import Core as C
from c57c_checker_mean_fast import preconditioner,rotate
from c57c_checker_pd import certified_pd
import c57c_checker_laurent_fast as plain

def weight(cells,w,point,gradient):
 axis=w['axis'];n,d=cells[axis];a,b=w['window']
 require(Q(n,2**d)>=Q(a,2**b)and Q(n+1,2**d)<=Q(a+1,2**b),'blend used outside nonnegative weight window')
 mid=arb(2*n+1)/2**(d+1);x=mid if point else arb(mid,arb(1)/2**(d+1))
 return (C(x,partials=[int(gradient and j==axis)for j in range(4)])-rational(Q(a,2**b)))*2**b

def children(w,t,q):
 for side in ['left','right']:
  child=w[side];child['parabolic']=w.get('parabolic',False)
  if 'laurent'not in child:child['laurent']=plain.compile_witness(child,t,q)

def fixed(cells,w,R,kappa,E,point,gradient,mu):
 z=weight(cells,w,point,gradient)
 L=plain.fixed(cells,w['left']['laurent'],R,kappa,E,point,gradient,mu)
 H=plain.fixed(cells,w['right']['laurent'],R,kappa,E,point,gradient,mu)
 return [[(1-z)*C(a)+z*C(b)for a,b in zip(lo,hi)]for lo,hi in zip(L,H)]

def gram(cells,w,R,kappa,t,q,point=False,mu=0):
 weight(cells,w,point,False);children(w,t,q)
 _,a=plain.gram(cells,w['left'],R,kappa,t,q,point,mu);_,b=plain.gram(cells,w['right'],R,kappa,t,q,point,mu)
 E=a.union(b).upper();G=fixed(cells,w,R,kappa,E,point,False,mu)
 return [[v.value.real for v in row]for row in G],E

def positive_mean(cells,w,R,kappa,t,q,E,mu=0):
 children(w,t,q);middle=fixed(cells,w,R,kappa,E,True,False,mu);A=[[-v.value.real for v in row]for row in middle];P=preconditioner(A)
 if P is None:return False
 B=rotate(A,P);whole=fixed(cells,w,R,kappa,E,False,True,mu)
 for axis,(n,d)in enumerate(cells):
  term=rotate([[-v.partials[axis].real for v in row]for row in whole],P);delta=arb(0,arb(1)/2**(d+1))
  for i in range(9):
   for j in range(9):B[i][j]+=term[i][j]*delta
 return certified_pd(B)

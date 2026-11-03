"""Separate exact scaled-radius Bloch inequalities. No search imports.
The constant term uses factored real/imaginary unit-vector identities;
unknown terms use sparse real polynomial multiplication.
"""
from fractions import Fraction as Q
from flint import arb,acb
from verify_c57c_center6 import require,rational
from c57c_checker_core_fast import Core as C
from c57c_checker_nested_fast import poly_times,poly_conj

def validate(disks):
 require(isinstance(disks,list)and len(disks)<=200,'invalid scaled disk list')
 for d in disks:
  require(isinstance(d,dict)and set(d)=={'scale','slope','sign','weight'},'invalid scaled disk')
  require(0<Q(d['scale'])<=64 and abs(Q(d['slope']))<=8,'invalid scaled radius or slope')
  require(d['sign']in(-1,1)and type(d['sign'])is int and Q(d['weight'])>0,'invalid scaled sign or weight')

def augment(G,s,a,cells,disks,point=False,gradient=False):
 x=[]
 for axis in [0,2]:
  n,d=cells[axis];mid=arb(2*n+1)/2**(d+1);value=mid if point else arb(mid,arb(1)/2**(d+1))
  x.append(C(value,partials=[int(gradient and j==axis)for j in range(4)]))
 u,v=x
 for disk in disks:
  B=1/rational(disk['scale'])+4*u;r=u/B;eta=rational(disk['slope']);den=1+eta*eta*r*r
  A=2*eta/den;J=disk['sign']*(1-eta*eta*r*r)/den;xi=r*A+acb(0,1)*J
  p=-3*s*xi**2+4*a*r*xi**3;h=r*r*p
  K=rational(Q(25,9)*Q(5,4)**8);T=K/(1-5*r/4)
  constant=2*B**2+12*s*A**2-8*a.real*(r*r*A**3-3*A*J*J)+12*v*B*(3*r*r*A*A*J-J**3)
  constant+=(3-2*r*r)/(1-r*r)**2+2*T*r**4/(1-r*r)+T*T*r**12-(p*p.conjugate()).real
  # Q(Y)=sum n r^(n-5) xi^(n-1) a_n. The full derivative
  # polynomial equals 1+h+r^4 Q. Its square has this exact quotient.
  poly={}
  for j in range(4):
   z=(j+5)*r**j*xi**(j+4);poly[0,2*j+1]=z;poly[0,2*j+2]=acb(0,1)*z
  terms={key:-r**4*value for key,value in poly_times(poly,poly_conj(poly)).items()}
  for key,value in poly.items():terms[key]=terms.get(key,C())-2*((1+h)*value.conjugate()).real
  terms[0,0]=constant;weight=rational(disk['weight'])
  for (i,j),value in terms.items():
   value=C(value).real*weight
   if i==j:G[i][j]=C(G[i][j])+value
   else:G[i][j]=C(G[i][j])+value/2;G[j][i]=C(G[j][i])+value/2
 return G

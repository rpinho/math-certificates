"""Checker-only derivative disks, assembled through sparse polynomial products.
No search imports. Each disk is a necessary Bloch inequality, with an
independent Cauchy bound on coefficients beyond degree eight.
"""
from fractions import Fraction as Q
from flint import acb,arb
from verify_c57c_center6 import require,rational
from c57c_checker_core_fast import Core as C
from c57c_checker_nested_fast import poly_times,poly_conj

def validate(disks):
 require(isinstance(disks,list)and len(disks)<=200,'invalid Bloch disk list')
 for d in disks:
  require(isinstance(d,dict)and set(d)=={'r','z','weight'},'invalid Bloch disk')
  r=Q(d['r']);weight=Q(d['weight']);require(0<r<=Q(1,4)and weight>0,'invalid Bloch disk radius or weight')
  require(isinstance(d['z'],list)and len(d['z'])==2,'invalid Bloch evaluation point')
  x,y=map(Q,d['z']);require(x*x+y*y==r*r,'incorrect Bloch point modulus')
 return disks

def augment(gram,s,a,disks):
 for disk in disks:
  r=rational(disk['r']);z=acb(*map(rational,disk['z']));weight=rational(disk['weight'])
  # Derivative series through degree seven, in eight real unknowns.
  p={(0,0):1-3*s*z**2+4*a*z**3}
  for j in range(4):
   coefficient=(j+5)*z**(j+4);p[0,2*j+1]=C(coefficient);p[0,2*j+2]=C(acb(0,1)*coefficient)
  square=poly_times(p,poly_conj(p))
  # On |z|=4/5 the Bloch bound is |f'|<=25/9. Cauchy
  # then bounds the remaining derivative terms by a geometric sum.
  ratio=5*r/4;remainder=rational('25/9')*ratio**8/(1-ratio)
  bound=1/(1-r*r)+remainder
  polynomial={key:-value for key,value in square.items()};polynomial[0,0]+=bound*bound
  for (i,j),value in polynomial.items():
   v=value.real*weight/r**4
   if i==j:gram[i][j]=C(gram[i][j])+v
   else:
    gram[i][j]=C(gram[i][j])+v/2;gram[j][i]=C(gram[j][i])+v/2
 return gram

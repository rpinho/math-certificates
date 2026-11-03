"""Independent rational binomial/geometric templates and Laurent checker.
No discovery imports. Formal Grunsky logarithms come from the checker-only
literal -log series; core chain rule and sparse Gram multiplication are also
checker-only. Laurent alpha powers use generic multiplication, not the
builder's explicit binomial substitution formula.
"""
from collections import defaultdict
from fractions import Fraction as Q
from flint import arb,acb
from verify_c57c_center6 import GRUNSKY,rational,require
from c57c_checker_core_fast import Core as C
from c57c_checker_nested_fast import quadratic_gram
from c57c_checker_mean_fast import preconditioner,rotate
from c57c_checker_bloch_fast import augment
from c57c_checker_scaled_bloch_fast import augment as scaled_augment
from c57c_checker_caps import local_caps
from c57c_checker_pd import certified_pd
ZERO=(0,)*8

def sum_poly(a,b,factor=Q(1)):
 out=defaultdict(Q,a)
 for key,c in b.items():out[key]+=factor*c
 return {key:c for key,c in out.items()if c}
def times_poly(a,b):
 out=defaultdict(Q)
 for ka,ca in a.items():
  for kb,cb in b.items():out[tuple(ka[j]+kb[j]for j in range(8))]+=ca*cb
 return {key:c for key,c in out.items()if c}
def variable(j):
 key=list(ZERO);key[j]=1;return {tuple(key):Q(1)}
def product_series(a,b):
 out=[{}for _ in range(8)]
 for total in range(8):
  for degree in range(total+1):out[total]=sum_poly(out[total],times_poly(a[degree],b[total-degree]))
 return out

def independent_templates():
 one={ZERO:Q(1)};U=[{}, {},{next(iter(variable(0))):Q(-1)},variable(1),variable(2),variable(3),variable(4),variable(5)]
 P=[one]+U[1:];term=[one]+[{}for _ in range(7)];inv=[dict(p)for p in term]
 for exponent in range(1,8):
  term=product_series(term,U);inv=[sum_poly(a,b,(-1)**exponent)for a,b in zip(inv,term)]
 inv[1]=sum_poly(inv[1],variable(6),-1)
 for degree in range(2,8):inv[degree]=sum_poly(inv[degree],times_poly(variable(7),P[degree-2]))
 V=[{}]+inv[1:];term=[one]+[{}for _ in range(7)];root=[dict(p)for p in term];binomial=Q(1)
 for exponent in range(1,8):
  binomial*=Q(1,2)-(exponent-1);binomial/=exponent;term=product_series(term,V);root=[sum_poly(a,b,binomial)for a,b in zip(root,term)]
 powers={}
 for j in range(7):
  powers[j,0]=one
  for e in range(1,8//(j+1)+1):powers[j,e]=times_poly(powers[j,e-1],root[j+1])
 answer={}
 for ij,poly in GRUNSKY.items():
  out={}
  for exponent,c in poly.items():
   term=one
   for j,e in enumerate(exponent):
    if e:term=times_poly(term,powers[j,e])
   out=sum_poly(out,term,c)
  answer[ij]=out
 return answer
TEMPLATES=independent_templates()

def laurent_product(a,b):
 out={}
 for (m,n),c in a.items():
  for (p,q),d in b.items():
   key=m+p,n+q;out[key]=out.get(key,acb(0))+c*d
 return out

def derivative(columns,axis):
 out=[]
 for poly in columns:
  result={}
  for key,c in poly.items():
   exponent=key[axis]
   if exponent:
    target=list(key);target[axis]-=1;target[4]+=(-1 if axis==2 else 1);target=tuple(target);result[target]=result.get(target,acb(0))+exponent*c
  out.append(result)
 return out

def compile_phase_witness(w,t,q):
 raw=w['raw'];columns=[{}for _ in range(5)];norm=acb(0)
 for form in raw['forms']:
  factor=rational(form['weight']);z=[acb(*pair)for pair in form['z']];mode=form['mode'];norm+=factor*sum((j+1)*(re*re+im*im)for j,(re,im)in enumerate(form['z']))
  if mode==0:alpha={};gamma={}
  elif mode==1:alpha={(-1,0):acb(1)};gamma={}
  else:alpha={(-1,0):acb(t),(0,1):acb(q/t)};gamma={(-1,1):acb(q)}
  pa=[{(0,0):acb(1)}];pg=[{(0,0):acb(1)}]
  for j in range(7):pa.append(laurent_product(pa[-1],alpha));pg.append(laurent_product(pg[-1],gamma))
  for i in range(1,8):
   for j in range(i,8):
    multiplier=factor*i*j*z[i-1]*z[j-1]*(1 if i==j else 2)
    if multiplier==0:continue
    for exponents,c in TEMPLATES.get((i,j),{}).items():
     s_power,a_power=exponents[:2];unknown=exponents[2:6];require(sum(unknown)<=1,'template nonlinear in high coefficients')
     column=next((index+1 for index,exponent in enumerate(unknown)if exponent),0)
     scaling=2*s_power+3*a_power+sum((index+4)*exponent for index,exponent in enumerate(unknown))
     low_scale=t**scaling if mode==2 else arb(1)
     for (m,n),coefficient in laurent_product(pa[exponents[6]],pg[exponents[7]]).items():
      key=s_power,a_power,m,n,(i+j)//2+m-n;columns[column][key]=columns[column].get(key,acb(0))+multiplier*rational(c)*low_scale*coefficient
 columns[0][0,0,0,0,0]=columns[0].get((0,0,0,0,0),acb(0))+norm
 z=derivative(columns,2);bar=derivative(columns,3);u=[];v=[]
 for left,right in zip(z,bar):
  keys=set(left)|set(right);u.append({k:left.get(k,acb(0))+right.get(k,acb(0))for k in keys});v.append({k:acb(0,1)*(left.get(k,acb(0))-right.get(k,acb(0)))for k in keys})
 return {'value':columns,'u':u,'v':v,'zz':derivative(z,2),'zb':derivative(z,3),'bb':derivative(bar,3),'zeta':rational(raw['area_weight']),'bloch_disks':raw.get('bloch_disks',[]),'scaled_disks':raw.get('scaled_disks',[]),'parabolic':w.get('parabolic',False),'phase':True}

def evaluate(columns,s,a,w,theta):
 # One memo table for all powers in all columns.
 powers=[{0:C(1)}for _ in range(5)];bases=[s,a,w,w.conjugate(),theta.cos()+acb(0,1)*theta.sin()];result=[]
 for poly in columns:
  value=C()
  for key,coefficient in poly.items():
   term=C(coefficient)
   for axis,exponent in enumerate(key):
    if exponent not in powers[axis]:powers[axis][exponent]=((theta*exponent).cos()+acb(0,1)*(theta*exponent).sin())if axis==4 else bases[axis]**exponent
    term*=powers[axis][exponent]
   value+=term
  result.append(value)
 return result

def parameters(cells,R,kappa,point=False,gradient=False,mu=0,parabolic=False):
 x=[]
 for axis,(n,d)in enumerate(cells):
  midpoint=arb(2*n+1)/2**(d+1);value=midpoint if point else arb(midpoint,arb(1)/2**(d+1));x.append(C(value,partials=[int(gradient and j==axis)for j in range(4)]))
 s=(1-x[0]**2)/3 if parabolic else x[0]/3;b=C(arb(2)/3)-s*s/2;theta=x[3]*(2*arb.pi())
 if parabolic:a=b*x[1]+acb(0,1)*rational('3/2')*x[0]*x[2];m=(a*a.conjugate()).real
 else:
  phi=x[2]*(arb.pi()/2);a=b*x[1]*(phi.cos()+acb(0,1)*phi.sin());m=b*b*x[1]*x[1]
 center=s*((C(arb(2)/5)-m/3-s*s/5)*a.real-acb(0,1)*(C(arb(25)/24)-3*m/2-s*s/4)*a.imag)
 epsilon=kappa*(-2500*(C(arb(1)/3)-s)**2-100*m).exp();v=R+(center+epsilon*mu*s*a)*(theta.cos()-acb(0,1)*theta.sin())
 return s,a,m,v,epsilon,theta

def fixed(cells,c,R,kappa,E,point=False,gradient=False,mu=0):
 if not c.get('phase'):
  from c57c_checker_laurent_scaled_fast import fixed as legacy
  return legacy(cells,c,R,kappa,E,point,gradient,mu)
 s,a,m,w,epsilon,theta=parameters(cells,R,kappa,point,gradient,mu,c.get('parabolic',False));values=evaluate(c['value'],s,a,w,theta);du=evaluate(c['u'],s,a,w,theta);dv=evaluate(c['v'],s,a,w,theta)
 coefficients=[(v,u,im,C(),C(),C())for v,u,im in zip(values,du,dv)]
 G=augment(quadratic_gram(s,a,m,epsilon,E,coefficients,c['zeta']),s,a,c['bloch_disks'])
 if c.get('scaled_disks'):require(c.get('parabolic',False),'scaled forms require the proved parabolic representation')
 return scaled_augment(G,s,a,cells,c.get('scaled_disks',[]),point,gradient)

def gram(cells,witness,R,kappa,t,q,point=False,mu=0):
 if witness.get('raw',{}).get('phase_rule')!='j*theta/2':
  from c57c_checker_laurent_scaled_fast import gram as legacy
  return legacy(cells,witness,R,kappa,t,q,point,mu)
 if witness['kind']=='blend':
  from c57c_checker_blend_fast import gram as blended
  return blended(cells,witness,R,kappa,t,q,point,mu)
 require(witness.get('parabolic',False),'moving phase requires the parabolic representation')
 if 'laurent'not in witness:witness['laurent']=compile_phase_witness(witness,t,q)
 c=witness['laurent'];s,a,m,w,epsilon,theta=parameters(cells,R,kappa,point,False,mu,c.get('parabolic',False));caps=local_caps(cells,c.get('parabolic',False));radius=(epsilon.value.real*caps[2]).upper();whole=C(acb(arb(w.value.real,radius),arb(w.value.imag,radius)))
 derivatives=[evaluate(c[name],s,a,whole,theta)for name in ['zz','zb','bb']];L=arb(0)
 for cap,row in zip(caps,zip(*derivatives)):L+=cap*(abs(row[0].value)+2*abs(row[1].value)+abs(row[2].value))
 E=(epsilon.value.real**2*L/2).upper();G=fixed(cells,c,R,kappa,E,point,False,mu);return [[C(v).value.real for v in row]for row in G],E

def positive_mean(cells,witness,R,kappa,t,q,E,mu=0):
 if witness.get('raw',{}).get('phase_rule')!='j*theta/2':
  from c57c_checker_laurent_scaled_fast import positive_mean as legacy
  return legacy(cells,witness,R,kappa,t,q,E,mu)
 if witness['kind']=='blend':
  from c57c_checker_blend_fast import positive_mean as blended_mean
  return blended_mean(cells,witness,R,kappa,t,q,E,mu)
 require(witness.get('parabolic',False),'moving phase requires the parabolic representation')
 if 'laurent'not in witness:witness['laurent']=compile_phase_witness(witness,t,q)
 c=witness['laurent'];mid=fixed(cells,c,R,kappa,E,True,False,mu);A=[[-C(v).value.real for v in row]for row in mid];P=preconditioner(A)
 if P is None:return False
 B=rotate(A,P);whole=fixed(cells,c,R,kappa,E,False,True,mu)
 for axis,(n,d)in enumerate(cells):
  rotated=rotate([[-C(v).partials[axis].real for v in row]for row in whole],P);delta=arb(0,arb(1)/2**(d+1))
  for i in range(9):
   for j in range(9):B[i][j]+=rotated[i][j]*delta
 return certified_pd(B)

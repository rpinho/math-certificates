"""Checker B: standard-library rational log series and Robbins factorial bounds.
No Arb, mpmath, gamma implementation, or code from discovery/Checker A.
"""
from fractions import Fraction as F
import json,pathlib,sys,os,shutil
N=44

def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[1],-x[0]
def sub(x,y):return add(x,neg(y))
def scale(x,q):return (x[0]*q,x[1]*q) if q>=0 else (x[1]*q,x[0]*q)

def log_range(x):
 x=F(x)
 if x<=0:raise ValueError('log domain')
 if x<1:return neg(log_range(1/x))
 e=x.numerator.bit_length()-x.denominator.bit_length()
 u=x/F(1<<e)
 if u<1:e-=1;u*=2
 if not 1<=u<2:raise ValueError('range reduction')
 def small(u):
  z=(u-1)/(u+1);zz=z*z;p=z;s=F(0)
  for j in range(N):s+=2*p/(2*j+1);p*=zz
  return s,s+2*p/((2*N+1)*(1-zz))
 a=small(u);b=small(F(2))
 return add(a,scale(b,e))

def factorial_log(m):
 if type(m)!=int or m<1:raise ValueError('factorial domain')
 # Robbins: sqrt(2 pi) m^(m+1/2) exp(-m) exp(1/(12m+1)) < m!
 #          < same leading term times exp(1/(12m)).
 # 3<pi<7/2 gives a deliberately coarse, independent enclosure of log(2pi).
 base=add(scale(log_range(m),F(2*m+1,2)),(-F(m),-F(m)))
 return base[0]+log_range(6)[0]/2+F(1,12*m+1),base[1]+log_range(7)[1]/2+F(1,12*m)

def check(path):
 c=json.loads(pathlib.Path(path).read_text())
 if c.get('schema')!='c70-cube-ball-single-term-v1':raise ValueError('schema')
 n=c['n'];k=c['k']
 if type(n) is not int or type(k) is not int or n<=k or k<=0 or n%2 or k%2:raise ValueError('dimensions')
 if F(c['normalized_side'])!=F(n-k,k):raise ValueError('scale certificate')
 C=F(c['claim'])
 if not 1<C<2:raise ValueError('claim')
 t=F(k,n)
 # Even-dimensional ball volumes cancel all powers of pi exactly.
 L=add(sub(sub(factorial_log(n),factorial_log(k)),factorial_log(n-k)),neg(factorial_log(k//2)))
 L=add(L,scale(factorial_log(n//2),t));L=scale(L,F(1,n))
 L=add(L,add(scale(log_range(1-t),1-t),scale(log_range(t),t)))
 gap=L[0]-log_range(C)[1]
 if gap<=0:raise ValueError('rational lower comparison fails')
 lo=F('1.20194336');hi=F('1.20194337')
 enclosed=L[0]>log_range(lo)[1] and L[1]<log_range(hi)[0]
 ef=1;es=F(1)
 for j in range(1,61):ef*=j;es+=F(1,ef)
 eup=es+F(1,ef*61)/(1-F(1,62))
 if c.get('limit_formula')!='exp(1/(2*e))' or not F(1,2*eup)>log_range(F(c['limit_claim']))[1]:raise ValueError('limit claim fails')
 return {'status':'PASS','limit_claim':c['limit_claim'],'limit_log_comparison_positive':True,'checker':'exact rational log series + Robbins, coarse 3<pi<7/2','terms':N,'claim':str(C),'log_comparison_positive':True,'finite_witness_between_1.20194336_and_1.20194337':enclosed,'margin_log_lower_display':float(gap),'interval_width_log_display':float(L[1]-L[0])}

if __name__=='__main__':
 if shutil.disk_usage('.').free<30_000_000_000:raise SystemExit('PAUSED disk floor')
 print('PID',os.getpid(),flush=True);print(json.dumps(check(sys.argv[1]),indent=2),flush=True)

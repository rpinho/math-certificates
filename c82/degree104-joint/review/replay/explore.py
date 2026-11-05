import os,json,time
from fractions import Fraction
from flint import ctx,fmpz_poly,arb,acb
ctx.prec=256;ctx.threads=1
print('PID',os.getpid(),flush=True)
c=json.load(open('inputs/certificates/certificate.json'),parse_float=str)
T=fmpz_poly([0,1,-1]);D=sum(f['multiplicity']*(len(f['coeffs'])-1) for f in c['denominator'])
a=sum(Fraction(f['q_rational'])*(len(f['coeffs'])-1) for f in c['numerator'])
print('D',D,'a',a,'slack',D-a,flush=True)
for typ in ['denominator','numerator']:
 for f in c[typ]:
  p=fmpz_poly(list(reversed(f['coeffs'])))(T)
  start=time.monotonic_ns();roots=p.complex_roots()
  h=arb(abs(p.leading_coefficient())).log()
  near=[]
  for z,m in roots:
   h+=m*abs(z).max(1).log()
   if not abs(z)>1 and not abs(z)<1:near.append(str(z))
  print(typ,f['name'],p.degree(),sum(m for z,m in roots),'logM',h,'circle?',near,'ms',(time.monotonic_ns()-start)//10**6,flush=True)
print('dilog',acb('0.5','0.5').polylog(2))

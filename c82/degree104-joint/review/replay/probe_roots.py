import os,json,time
from fractions import Fraction
from flint import ctx,fmpz_poly,arb
ctx.prec=256; ctx.threads=1
print('PID',os.getpid(),flush=True)
c=json.load(open('inputs/certificates/certificate.json'))
T=fmpz_poly([0,1,-1])
D=sum(x['multiplicity']*(len(x['coeffs'])-1) for x in c['denominator'])
a=sum(Fraction(x['q_rational'])*(len(x['coeffs'])-1) for x in c['numerator'])
print('D',D,'a',a,'slack',D-a,flush=True)
count=0; H=arb(0)
for section in ['denominator','numerator']:
 for x in c[section]:
  p=fmpz_poly(list(reversed(x['coeffs']))); P=p(T); t=time.monotonic(); roots=P.complex_roots()
  count+=sum(m for r,m in roots)
  M=arb(abs(int(P.leading_coefficient()))).log()+sum((abs(r).max(1).log()*m for r,m in roots),arb(0))
  if section=='denominator': H+=x['multiplicity']*M/D
  print(section,x['name'],'degree',P.degree(),'roots',len(roots),'circle',[(str(r),m) for r,m in roots if abs(r).contains(1)],'logM',M,'sec',round(time.monotonic()-t,3),flush=True)
print('total',count,'H',H,flush=True)

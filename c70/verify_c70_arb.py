"""Checker A: Arb ball arithmetic, factorial/gamma evaluation. No discovery imports."""
import json,sys,pathlib,os,shutil
from fractions import Fraction
from flint import arb,ctx

def aq(s):
 q=Fraction(s);return arb(q.numerator)/q.denominator

def parse(p):
 c=json.loads(pathlib.Path(p).read_text())
 if c.get('schema')!='c70-cube-ball-single-term-v1':raise ValueError('schema')
 n,k=c['n'],c['k']
 if type(n)!=int or type(k)!=int or not 0<k<n or n%2 or k%2:raise ValueError('even integer dimensions required')
 if Fraction(c['normalized_side'])!=Fraction(n-k,k):raise ValueError('normalized side mismatch')
 if not 1<Fraction(c['claim'])<2:raise ValueError('claim range')
 return c

def check(p,bits=256):
 if bits<128:raise ValueError('precision too low')
 ctx.prec=bits;c=parse(p);n,k=c['n'],c['k'];t=arb(k)/n
 # k is the Euclidean-ball dimension of the retained Steiner term.
 # Formula here evaluates ball volumes directly, so pi cancellation is not assumed.
 logvol=lambda d:arb.pi().log()*(arb(d)/2)-arb(d//2+1).lgamma()
 logbin=arb(n+1).lgamma()-arb(k+1).lgamma()-arb(n-k+1).lgamma()
 L=logbin/n+(1-t)*(1-t).log()+t*t.log()+(logvol(k)-t*logvol(n))/n
 value=L.exp();margin=value-aq(c['claim'])
 if not margin>0:raise ValueError('claimed lower bound not certified')
 limit=(arb(-1).exp()/2).exp()
 if c.get('limit_formula')!='exp(1/(2*e))' or not limit>aq(c['limit_claim']):raise ValueError('limit claim not certified')
 return {'status':'PASS','limit_ball':str(limit),'limit_claim':c['limit_claim'],'checker':'Arb factorial/ball-volume formula','bits':bits,'value_ball':str(value),'claim':c['claim'],'margin_ball':str(margin),'log_value_ball':str(L)}

def baseline(n=300000,side='13/1000',bits=256):
 ctx.prec=bits;a=aq(side);pi=arb.pi()
 logk=lambda d:arb(d)*pi.log()/2-(arb(d)/2+1).lgamma()
 kn=logk(n).exp();km=logk(n-1).exp()
 total=arb(0)
 for parity,term in [(0,kn),(1,arb(n)*a*km)]:
  j=parity
  while True:
   total+=term
   if j+2>n:break
   term*=arb(n-j)**2*(n-j-1)*a*a/(2*pi*(j+1)*(j+2));j+=2
 value=(total.log()/n).exp()/(a+(kn.log()/n).exp())
 if not value>aq('1.201927') or not value<aq('1.201927142573'):raise ValueError('baseline comparison')
 return {'status':'PASS','checker':'Arb parity recurrences','n':n,'side':side,'value_ball':str(value),'comparison_upper':'1.201927142573'}

if __name__=='__main__':
 if shutil.disk_usage('.').free<30_000_000_000:raise SystemExit('PAUSED disk floor')
 print('PID',os.getpid(),flush=True)
 if len(sys.argv)>1 and sys.argv[1]=='--baseline':out=baseline()
 else:out=check(sys.argv[1])
 print(json.dumps(out,indent=2),flush=True)

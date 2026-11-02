"""Exact reproduction of Epi's released nodes/weights and Wellens's degree recurrence."""
import json,math,pathlib,sys,hashlib,shutil,os,time
from fractions import Fraction as Q
R=pathlib.Path(__file__).resolve().parent

def block_bound(d):
 b=math.isqrt(2*(d**4-d*d)//3)+1
 while 3*b*(b-1)>2*(d**4-d*d):b-=1
 while 3*(b+1)*b<=2*(d**4-d*d):b+=1
 return b

def recurrence(B,H):
 unit=1<<H
 prev=[0]*(H+1)
 for b in range(1,max(B)+1):
  prefix=0;row=[0]*(H+1)
  for d in range(1,H+1):
   prefix=max(prefix,prev[d])
   row[d]=prev[d] if b>B[d] else min(d*unit//2,d*(1<<(H-d))+prefix)
  prev=row
 return prev

def main():
 if shutil.disk_usage(R).free<30_000_000_000:raise SystemExit('PAUSED: disk floor')
 print('PID',os.getpid(),flush=True)
 a=json.loads((R/'sources/wellens-certificate.json').read_text());H=a['horizon'];N=a['degree']
 B=[0]+[block_bound(d) for d in range(1,H+1)]
 margins={}
 for d in range(1,N+1):
  c=a['certificates'][str(d)];xs=c['nodes'];w=list(map(Q,c['weights']))
  if len(xs)!=d+1 or len(w)!=d+1 or xs!=sorted(set(xs)) or xs[0]!=1:raise ValueError('nodes')
  for k in range(1,d+1):
   if sum((v*x**k for v,x in zip(w,xs)),Q(0))!=0:raise ValueError(('moment',d,k))
  gap=w[0]+sum((v for v in w[1:] if v<0),Q(0))
  if w[0]<=0 or gap<=0:raise ValueError(('infeasibility',d))
  B[d]=min(B[d],xs[-1]-1);margins[str(d)]=str(gap)
 U=recurrence(B,H)
 # Wellens Cor.3.10: cutoff H, use B_{H+1}<=(H+1)^2 and quadratic difference tail.
 # sum_{k=H+2}^infinity (2k^2-k)/2^k = (2H^2+11H+19)/2^(H+1).
 tail=Q((H+1)**3,2**(H+1))+Q(2*H*H+11*H+19,2**(H+1))
 bound=Q(U[H],1<<H)+tail
 out={'status':'PASS','kind':'exact rational reproduction of sufficient certificates and recurrence','degree':N,'horizon':H,'B':B,'D_H':str(Q(U[H],1<<H)),'tail':str(tail),'bound':str(bound),'bound_decimal_display':format(float(bound),'.16g'),'infeasibility_margins':margins,'epi_printed_bound':'4.3654674227','below_epi_printed':bound<Q('4.3654674227')}
 p=R/'logs/c44_baseline.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['B','infeasibility_margins']},indent=2),flush=True)
if __name__=='__main__':main()

"""Independent Arb quantitative checker for GEOMETRIC_LEMMA.md.
No discovery or other checking code is imported. Every decision is exact
rational or a certified Arb comparison; all infinitely many moments covered.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,hashlib,time
from flint import arb,ctx
if not __debug__:raise SystemExit('Refusing -O/-OO: assertions are part of the proof')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--out');a=ap.parse_args();start=time.monotonic();p=Path(a.certificate);d=json.loads(p.read_text());ctx.dps=75
 assert d['analytic_model']=='two_covering_zeros_hyperbolic_jung'
 c0,R0,l0=map(F,[d['c'],d['R'],d['linear_slope']]);ts=list(map(F,d['nodes']));ws=list(map(F,d['weights']))
 assert 0<c0<1 and c0*c0<R0<1 and l0>0;assert len(ts)==len(ws)>=2 and ts[0]==c0*c0 and ts[-1]==R0 and all(x<y for x,y in zip(ts,ts[1:]));assert all(v>0 for v in ws) and sum(ws)==R0
 def ar(x):return arb(str(x))
 c,R,l=map(ar,[c0,R0,l0]);w=-c.log();pi=arb.pi();X=(pi*pi/(2*w)).sinh()**2;U=-pi*R.log()/(2*w);assert U>0 and U*U<6
 aa=(pi/(2*w))**2*(1-U*U/6)**2/X;delta=1-R;z=aa*delta*delta
 slope=2*(6*aa).sqrt()/((3*z*(2+z)).sqrt()+(4+6*z+3*z*z).sqrt());assert slope>l,('linear envelope',slope,l)
 T=list(map(ar,ts));W=list(map(ar,ws));beta=[arb(1)]
 for t in T[1:]:
  y=(pi*t.log()/(2*w)).sin()**2/X;H=3*y*(2+y);g=2*H.sqrt()/(H.sqrt()+(H+4).sqrt());assert g>0 and g<1;beta.append((1-g).upper())
 K1=max(1,int(R0//ws[-1]));assert ws[-1]*(K1+1)>=R0;K2=int(d['second_tail_k']);assert K2>=1
 t0,t1=map(F,[d['second_tail_t0'],d['second_tail_t1']]);assert R0<t0<t1<1
 tail=ar(l0*(1-t1)*(t1-t0))*ar(t0)**K2;neg=sum(v*t**K2 for v,t in zip(W,T));assert tail>neg,('second infinite tail',tail-neg)
 powers=[arb(1)]*len(T);rp=R;minA=None;minB=None;ia=ib=0
 for k in range(1,max(K1,K2)):
  powers=[x*t for x,t in zip(powers,T)];rp*=R
  if k<K1:
   gap=(k+1)*sum(v*x for v,x in zip(W,powers))-rp;assert gap>0,('first moment',k,gap);rel=(gap/rp).lower()
   if minA is None or rel<minA:minA=rel;ia=k
  if k<K2:
   integral=l*((1-rp)/(k+1)-(1-rp*R)/(k+2));gap=(k+1)*integral+rp-(k+1)*sum(v*b*x for v,b,x in zip(W,beta,powers));assert gap>0,('second moment',k,gap);rel=(gap/rp).lower()
   if minB is None or rel<minB:minB=rel;ib=k
 out={'status':'PASS','checker':'Arb, two covering zeros + hyperbolic Jung','certificate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'c':str(c0),'atoms':len(T),'linear_envelope_slope_lower':str(slope.lower()),'first_finite_through':K1-1,'first_tail_from':K1,'second_finite_through':K2-1,'second_tail_from':K2,'first_min_relative_lower':str(minA),'first_min_k':ia,'second_min_relative_lower':str(minB),'second_min_k':ib,'second_tail_gap_lower':str((tail-neg).lower()),'seconds':time.monotonic()-start}
 if a.out:Path(a.out).write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':main()

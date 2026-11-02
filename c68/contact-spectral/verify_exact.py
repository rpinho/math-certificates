#!/usr/bin/env python3
"""Independent rigorous C68 certificate verifier. No search-code imports.
Exact rational structure; Arb outward ball arithmetic for elementary functions,
finite moments, analytic infinite tails. Analytic proof: ANGULAR_LEMMA.md plus
GREEN_FLUX_PROOF.md. Refuses unsupported models/constants and Python -O.
"""
import argparse,json,hashlib,time
from fractions import Fraction
from pathlib import Path
from flint import arb,fmpq,ctx
if not __debug__:raise SystemExit('Assertions are required; do not use -O')

def exact(x):
 v=Fraction(x);return arb(fmpq(v.numerator,v.denominator))
def positive(x,reason):
 if not x>0:raise AssertionError((reason,str(x)))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--output');args=ap.parse_args();start=time.monotonic();raw=Path(args.certificate).read_bytes();cert=json.loads(raw)
 ctx.prec=320
 assert cert['model'] in ('fourier_majorant_low_coefficient_v1','spectral_geometric_mean_v2','contact_spectral_v3')
 expected_zeta={'fourier_majorant_low_coefficient_v1':Fraction(9,320),'spectral_geometric_mean_v2':Fraction(3,50),'contact_spectral_v3':Fraction(7,100)}[cert['model']]
 assert Fraction(cert['kappa'])==Fraction(3,25) and Fraction(cert['zeta'])==expected_zeta
 c,R=map(Fraction,(cert['c'],cert['R']));tt=list(map(Fraction,cert['nodes']));ww=list(map(Fraction,cert['weights']));partition=list(map(Fraction,cert['tail_partition']))
 assert 0<c<1 and c*c<R<1 and R>=c
 assert len(tt)==len(ww)>=2 and tt[0]==c*c and tt[-1]==R
 assert all(v>0 for v in ww) and sum(ww)==R
 assert all(a<b for a,b in zip(tt,tt[1:]));assert partition[0]==R and partition[-1]==1 and all(a<b for a,b in zip(partition,partition[1:]))
 spectral=None
 if cert['model']=='spectral_geometric_mean_v2':
  from verify_spectral import verify_cover
  spectral=verify_cover(Path(args.certificate).parent/'spectral-cover.json')
 if cert['model']=='contact_spectral_v3':
  from verify_contact import verify_cover
  spectral=verify_cover(Path(args.certificate).parent/'contact-cover.json')
 ca=exact(c);ra=exact(R);width=-ca.log();pi=arb.pi();A=pi*pi/width;q=(-A).exp();psi=(1+q)**2/(8*q);kap=exact('3/25');zet=exact(expected_zeta)
 hypotheses={
  'Green_sech':arb(1)/3-1/(A/2).cosh()**2,
  'Fourier_small_arc':2*(1-8*kap)*psi-16*(A/4).sinh()**2,
  'Fourier_near_midpoint':(A/8).tanh()**2-(1+8*kap)*pi*pi/64,
  'Fourier_middle_arc':(1-4*kap)/2-1/(A/8).cosh()**2,
  'nonnegative_beta1':psi-6,
 }
 for k,v in hypotheses.items():positive(v,k)
 # Exact constants in the low-coefficient proof, independent of transcendental data.
 assert Fraction(17,100)**2>Fraction(9,320)
 assert 2*Fraction(3,25)*(1-Fraction(15,16)**2)>Fraction(9,320)
 assert 4*Fraction(3,25)*Fraction(15,16)==Fraction(9,20)
 assert Fraction(9,5)>Fraction(117,100)**2
 assert Fraction(17,100)*Fraction(117,100)<Fraction(9,20)
 assert Fraction(9,20)/16==Fraction(9,320)
 # Atomic beta values; k=1 is the sole moment whose coefficient changes.
 ordinary=[];corrected=[];atomic_g=[];atomic_e=[]
 for node in tt:
  if node==c*c:g=e=arb(0)
  else:
   t=exact(node);s=(pi*t.log()/(2*width)).sin()**2
   h=(1+psi/(2*s)).sqrt();g=2/(1+h);e=zet*(h*h-1)/(h*(1+h)**2)
   positive(g,'atomic g');positive(1-g-e,'beta1 nonnegative')
  atomic_g.append(g);atomic_e.append(e);ordinary.append(1-g);corrected.append(1-g-e)
 # Piecewise analytic lower bounds g(t)>=slope*(1-t) on the tail.
 pieces=[]
 for a,b in zip(partition,partition[1:]):
  aa,bb=exact(a),exact(b);U=-pi*aa.log()/(2*width)
  positive(U,'tail positive angle');positive(6-U*U,'tail sine remainder')
  B=pi/(2*width)*(1+(1-bb)/2)*(1-U*U/6);positive(B,'tail slope numerator')
  z=arb(2).sqrt()*B*(1-aa)
  slope=2*arb(2).sqrt()*B/(z+(z*z+psi).sqrt());positive(slope,'tail slope')
  pieces.append((a,b,arb(slope.lower())))
 K1=int(cert['first_tail_k']);K2=int(cert['second_tail_k']);assert 1<K1<1000000 and 1<K2<1000000
 assert ww[-1]*(K1+1)>=R
 ta,tb=map(Fraction,(cert['second_tail_a'],cert['second_tail_b']));assert R<=ta<tb<1
 # Derive a fresh slope on this interval rather than selecting a tail partition cell.
 aa,bb=exact(ta),exact(tb);U=-pi*aa.log()/(2*width);positive(6-U*U,'second-tail sine');B=pi/(2*width)*(1+(1-bb)/2)*(1-U*U/6);z=arb(2).sqrt()*B*(1-aa);slope=2*arb(2).sqrt()*B/(z+(z*z+psi).sqrt())
 positive(slope,'second-tail slope')
 W=list(map(exact,ww));T=list(map(exact,tt))
 tail_good=slope*(1-bb)*(bb-aa)*aa**K2;tail_bad=sum(w*t**K2 for w,t in zip(W,T));tail_gap=tail_good-tail_bad;positive(tail_gap,'infinite second tail')
 # Independent normalized moment recurrences avoid tiny R^k intermediates.
 ratios=[t/ra for t in T];power=[arb(1)]*len(T)
 points=sorted(set(partition));point_value={p:exact(p) for p in points};ratio_p={p:point_value[p]/ra for p in points};pows={p:ratio_p[p] for p in points}
 minA=minB=None;argA=argB=None
 for k in range(1,max(K1,K2)):
  power=[p*t for p,t in zip(power,ratios)]
  for p in points:pows[p]*=ratio_p[p]
  if k<K1:
   margin=(k+1)*sum(w*p for w,p in zip(W,power))/ra-1
   positive(margin,('A',k))
   if minA is None or margin<minA:minA=margin;argA=k
  if k<K2:
   # integral g(t)t^k/R^(k+1), with g lower bounded piecewise.
   integ=arb(0)
   for a,b,slope in pieces:
    Ja=pows[a]*(arb(1)/(k+1)-point_value[a]/(k+2));Jb=pows[b]*(arb(1)/(k+1)-point_value[b]/(k+2));integ+=slope*(Jb-Ja)
   betas=corrected if k==1 else ordinary
   margin=1+(k+1)*integ-(k+1)*sum(w*b*p for w,b,p in zip(W,betas,power))/ra
   positive(margin,('B',k))
   if minB is None or margin<minB:minB=margin;argB=k
 out=dict(status='PASS',c=str(c),decimal_c=str(float(c)),model=cert['model'],certificate_sha256=hashlib.sha256(raw).hexdigest(),precision_bits=ctx.prec,hypothesis_margins={k:str(v) for k,v in hypotheses.items()},first_finite_through=K1-1,first_tail_from=K1,second_finite_through=K2-1,second_tail_from=K2,first_min_relative=str(minA),first_min_k=argA,second_min_relative=str(minB),second_min_k=argB,second_infinite_tail_gap=str(tail_gap),atomic_g=list(map(str,atomic_g)),atomic_epsilon=list(map(str,atomic_e)),seconds=time.monotonic()-start)
 if spectral is not None:out['spectral_scalar_verification']=spectral
 print(json.dumps(out,indent=2))
 if args.output:Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()

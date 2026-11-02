"""Exact Bernstein polynomial proof + independent Arb moment verification.
Self-contained; imports no search or other verifier. No numerical quadrature.
"""
from fractions import Fraction as F
from pathlib import Path
from math import comb,gcd
import json,argparse,time,hashlib
from flint import arb,ctx,fmpq,fmpq_poly
if not __debug__:raise SystemExit('Refusing -O/-OO: proof assertions must be active')

def poly_digest(coeff):
 g=0
 for x in coeff:g=gcd(g,abs(x))
 coeff=[x//g for x in coeff];h=hashlib.sha256()
 for x in coeff:
  b=abs(x).to_bytes(max(1,(abs(x).bit_length()+7)//8),'big');h.update(bytes([x<0]));h.update(len(b).to_bytes(8,'big'));h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--out');args=ap.parse_args();start=time.monotonic();path=Path(args.certificate);d=json.loads(path.read_text());ctx.dps=65
 c0=F(d['c']);R0=F(d['R']);nodes0=list(map(F,d['nodes']));weights0=list(map(F,d['weights']));assert 0<c0<1 and c0*c0<R0<1;assert sum(weights0)==R0 and all(w>0 for w in weights0);assert len(nodes0)==len(weights0)>=2;assert nodes0[0]==c0*c0 and nodes0[-1]==R0 and all(l<u for l,u in zip(nodes0,nodes0[1:]))
 env=d['lower_envelope'];assert F(env['c'])==c0 and F(env['R'])==R0;end0=F(env['end']);assert R0<end0<1;aa=list(map(F,env['coefficients_delta']));N=int(env['product_terms']);assert N>=28
 Delta=1-R0;assert aa[0]>sum(abs(a)*Delta**k for k,a in enumerate(aa[1:],1));assert sum(abs(a)*Delta**k for k,a in enumerate(aa,1))<1
 # This proves -L'(t)>0 on the whole envelope interval, as required
 # when L(t1) is used as a lower bound on [t0,t1] in the tail proof.
 assert aa[0]>sum((k+1)*abs(a)*Delta**k for k,a in enumerate(aa[1:],1)), 'envelope decreasing'
 cc=fmpq(str(c0));delta=fmpq_poly([1,-1]);one=fmpq_poly([1]);L=fmpq_poly([])
 for k,a in enumerate(aa,1):L+=fmpq(str(a))*delta**k
 P=fmpq_poly([4*cc*cc,8*cc,4]);Q=fmpq_poly([0,1])
 for n in range(1,N+1):
  top=fmpq_poly([1,cc**(2*n-1)])*fmpq_poly([cc**(2*n+1),1])*(1+cc**(2*n))**2
  bot=fmpq_poly([1,cc**(2*n-2)])*fmpq_poly([cc**(2*n),1])*(1+cc**(2*n-1))**2
  P*=top**2;Q*=bot**2
 err=(1+3*c0+2*c0*c0+(c0**3+c0*c0)/R0)*c0**(2*N)/(1-c0*c0);assert 0<err<1
 proof=(one-L)*Q*fmpq(str((1-err)**2))-(one-L+L*L)*P
 primitive_sha=poly_digest([int(x) for x in proof.numer().coeffs()]);degree=proof.degree();parts=[(F(a),F(b)) for a,b in env['positive_partitions']];parts.sort();assert parts[0][0]==R0 and parts[-1][1]==end0 and all(a<b for a,b in parts);assert all(x[1]==y[0] for x,y in zip(parts,parts[1:]))
 # Exact affine composition, followed by the power-to-Bernstein identity.
 # B_j*binom(n,j)*common_den = sum_k q_k binom(n-k,j-k).
 for a,b in parts:
  aff=proof(fmpq_poly([fmpq(str(a)),fmpq(str(b-a))]));coef=[int(x) for x in aff.numer().coeffs()];n=aff.degree()
  for j in range(n+1):assert sum(coef[k]*comb(n-k,j-k) for k in range(j+1))>0,('Bernstein',str(a),str(b),j)
 print('exact Bernstein envelope PASS degree',degree,'partitions',len(parts),flush=True)
 def ar(x):return arb(str(x))
 c=ar(c0);R=ar(R0);end=ar(end0);nodes=[ar(x) for x in nodes0];weights=[ar(x) for x in weights0];cp=[c**k for k in range(2*N+3)]
 def invg(t):
  q=4*(t+c)**2/t
  for n in range(1,N+1):
   factor=(1+t*cp[2*n-1])*(t+cp[2*n+1])*(1+cp[2*n])**2/((1+t*cp[2*n-2])*(t+cp[2*n])*(1+cp[2*n-1])**2)
   q*=factor*factor
  e=(1+3*c+2*c*c+(c**3+c*c)/t.lower())*cp[2*N]/(1-c*c)
  q*=arb(0,(2*e).upper()).exp();assert q>0 and q.upper()<1
  return 2/(1+((1+3*q)/(1-q)).sqrt())
 beta=[arb(1)]+[(1-invg(t)).upper() for t in nodes[1:]]
 K1=max(1,R0//weights0[-1]);assert weights0[-1]*(K1+1)>=R0
 powers=[arb(1) for _ in nodes];rp=R;minA=None;argA=0
 for k in range(1,K1):
  powers=[x*t for x,t in zip(powers,nodes)];rp*=R;gap=(k+1)*sum(w*x for w,x in zip(weights,powers))-rp;assert gap>0,('A',k,gap)
  rel=gap/rp
  if minA is None or rel.lower()<minA:minA=rel.lower();argA=k
 print('first infinite family PASS tail from',K1,flush=True)
 t0=F(d['second_tail_t0']);t1=F(d['second_tail_t1']);K2=int(d['second_tail_k']);assert R0<t0<t1<=end0 and K2>=1
 cap=sum(a*(1-t1)**k for k,a in enumerate(aa,1));assert cap>0
 tail=ar(cap*(t1-t0))*ar(t0)**K2;negative=sum(w*t**K2 for w,t in zip(weights,nodes));assert tail>negative,('second tail',tail-negative)
 # All coefficients of the proven lower polynomial are exact rationals.
 lc=[ar(F(str(x))) for x in L.coeffs()];rr=[R**j for j in range(len(lc))];ee=[end**j for j in range(len(lc))];rp=R;ep=end;powers=[arb(1) for _ in nodes];minB=None;argB=0
 for k in range(1,K2):
  rp*=R;ep*=end;powers=[x*t for x,t in zip(powers,nodes)]
  integral=sum(a*(ep*e-rp*r)/(k+j+1) for j,(a,e,r) in enumerate(zip(lc,ee,rr)))
  gap=(k+1)*integral+rp-(k+1)*sum(w*b*x for w,b,x in zip(weights,beta,powers));assert gap>0,('B',k,gap,gap/rp)
  rel=gap/rp
  if minB is None or rel.lower()<minB:minB=rel.lower();argB=k
  if k%50000==0:print('finite second moments through',k,flush=True)
 out={'status':'PASS','checker':'exact Flint/Bernstein polynomial + Arb moments','certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'c':str(c0),'R':str(R0),'atoms':len(nodes),'mass_exact':'1','envelope_polynomial_degree':degree,'primitive_polynomial_sha256':primitive_sha,'envelope_partitions':len(parts),'first_finite_through':K1-1,'first_tail_from':K1,'first_min_relative_lower':str(minA),'first_min_k':argA,'second_finite_through':K2-1,'second_tail_from':K2,'second_min_relative_lower':str(minB),'second_min_k':argB,'second_tail_gap_lower':str((tail-negative).lower()),'seconds':time.monotonic()-start}
 if args.out:Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':main()

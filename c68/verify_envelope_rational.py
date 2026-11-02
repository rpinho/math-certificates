"""Independent integer polynomial and fixed-point moment proof (standard library).
No Flint/Arb, optimizer, numerical integration, or other checker is imported.
"""
from fractions import Fraction as F
from pathlib import Path
from math import comb,gcd,lcm,isqrt
import json,argparse,time,hashlib
if not __debug__:raise SystemExit('Refusing -O/-OO: proof assertions must be active')
S=1<<180

def ceildiv(n,d):
 assert d>0
 return -((-n)//d)
def enc(x):
 x=F(x);return x.numerator*S//x.denominator,ceildiv(x.numerator*S,x.denominator)
def interval_multiply(a,b):
 assert min(a)>=0 and min(b)>=0
 return a[0]*b[0]//S,ceildiv(a[1]*b[1],S)
def interval_power(a,k):
 result=(S,S)
 while k:
  if k&1:result=interval_multiply(result,a)
  a=interval_multiply(a,a);k>>=1
 return result

def pmul(a,b):
 result=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):result[i+j]+=x*y
 while len(result)>1 and not result[-1]:result.pop()
 return result
def padd(a,b):
 result=[0]*max(len(a),len(b))
 for i,x in enumerate(a):result[i]+=x
 for i,x in enumerate(b):result[i]+=x
 while len(result)>1 and not result[-1]:result.pop()
 return result
def scale(a,c):return [x*c for x in a]
def primitive_digest(a):
 content=0
 for x in a:content=gcd(content,abs(x))
 h=hashlib.sha256()
 for x in a:
  x//=content;b=abs(x).to_bytes(max(1,(abs(x).bit_length()+7)//8),'big');h.update(bytes([x<0]));h.update(len(b).to_bytes(8,'big'));h.update(b)
 return h.hexdigest()
def mobius_positive(p,left,right):
 n=len(p)-1;D=lcm(left.denominator,right.denominator);A=left.numerator*(D//left.denominator);B=right.numerator*(D//right.denominator)
 # (1+x)^n P((A+B*x)/(D*(1+x))) * D^n, by homogenized Horner.
 q=[p[-1]];dp=1
 for j in range(1,n+1):
  dp*=D;v=p[n-j]*dp;new=[v*comb(j,k) for k in range(j+1)]
  for k,x in enumerate(q):new[k]+=A*x;new[k+1]+=B*x
  q=new
 assert all(x>0 for x in q),('Mobius positivity',str(left),str(right))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--out');args=ap.parse_args();start=time.monotonic();path=Path(args.certificate);d=json.loads(path.read_text());c=F(d['c']);R=F(d['R']);nodes=list(map(F,d['nodes']));weights=list(map(F,d['weights']))
 assert 0<c<1 and c*c<R<1 and len(nodes)==len(weights)>=2;assert all(w>0 for w in weights) and sum(weights)==R;assert nodes[0]==c*c and nodes[-1]==R and all(a<b for a,b in zip(nodes,nodes[1:]))
 env=d['lower_envelope'];assert F(env['c'])==c and F(env['R'])==R;end=F(env['end']);assert R<end<1;aa=list(map(F,env['coefficients_delta']));N=int(env['product_terms']);assert N>=28
 Delta=1-R;assert aa[0]>sum(abs(a)*Delta**j for j,a in enumerate(aa[1:],1));assert sum(abs(a)*Delta**j for j,a in enumerate(aa,1))<1
 # Reconstruct K_N(sqrt(t))^2 as a ratio of INTEGER polynomials.
 C,D=c.numerator,c.denominator;Cn=[C**j for j in range(2*N+3)];Dn=[D**j for j in range(2*N+3)];num=[C*C,2*C*D,D*D];den=[0,1];top=4;bot=D**(2+8*N)
 for n in range(1,N+1):
  for factor in [[Dn[2*n-1],Cn[2*n-1]],[Cn[2*n+1],Dn[2*n+1]]]:num=pmul(pmul(num,factor),factor)
  for factor in [[Dn[2*n-2],Cn[2*n-2]],[Cn[2*n],Dn[2*n]]]:den=pmul(pmul(den,factor),factor)
  top*=(Dn[2*n]+Cn[2*n])**4;bot*=(Dn[2*n-1]+Cn[2*n-1])**4
 common=gcd(top,bot);num=scale(num,top//common);den=scale(den,bot//common)
 # Expand the small lower polynomial independently by the binomial theorem.
 lc=[sum(((-1)**j)*aa[k-1]*comb(k,j) for k in range(max(1,j),len(aa)+1)) for j in range(len(aa)+1)]
 ell=1
 for x in lc:ell=lcm(ell,x.denominator)
 LP=[int(x*ell) for x in lc]
 err=(1+3*c+2*c*c+(c**3+c*c)/R)*c**(2*N)/(1-c*c);assert 0<err<1;en,ed=err.numerator,err.denominator
 first=scale(padd([ell],scale(LP,-1)),ell*(ed-en)**2)
 second=scale(padd(padd([ell*ell],scale(LP,-ell)),pmul(LP,LP)),ed*ed)
 proof=padd(pmul(first,den),scale(pmul(second,num),-1));digest=primitive_digest(proof)
 parts=sorted((F(a),F(b)) for a,b in env['positive_partitions']);assert parts and parts[0][0]==R and parts[-1][1]==end and all(a<b for a,b in parts);assert all(x[1]==y[0] for x,y in zip(parts,parts[1:]))
 for a,b in parts:mobius_positive(proof,a,b)
 print('integer Mobius envelope PASS degree',len(proof)-1,'partitions',len(parts),flush=True)
 # All subsequent transcendental decisions use integer outward enclosures.
 T=list(map(enc,nodes));W=list(map(enc,weights));RR=enc(R);EE=enc(end);cp=[enc(c**j) for j in range(2*N+3)];cl,ch=enc(c)
 e=(1+3*c+2*c*c+(c**3+c*c)/(c*c))*c**(2*N)/(1-c*c);e_hi=enc(e)[1];assert 0<e_hi<S
 def invg_lower(t):
  l,u=enc(t);low=4*(l+cl)**2//u;high=ceildiv(4*(u+ch)**2,l)
  for n in range(1,N+1):
   pl,ph=cp[2*n-1];ql,qh=cp[2*n+1];ul,uh=cp[2*n-2];vl,vh=cp[2*n]
   a=(S+l*pl//S,S+ceildiv(u*ph,S));b=(S+ql*S//u,S+ceildiv(qh*S,l));v=(S+vl,S+vh);numer=interval_multiply(interval_multiply(a,b),interval_multiply(v,v))
   a=(S+l*ul//S,S+ceildiv(u*uh,S));b=(S+vl*S//u,S+ceildiv(vh*S,l));p=(S+pl,S+ph);denom=interval_multiply(interval_multiply(a,b),interval_multiply(p,p))
   ratio=(numer[0]*S//denom[1],ceildiv(numer[1]*S,denom[0]));low,high=interval_multiply((low,high),interval_multiply(ratio,ratio))
  high=ceildiv(high*S*S,(S-e_hi)**2);assert 0<=high<S
  rad=ceildiv((S+3*high)*S*S,S-high);root=isqrt(rad)
  if root*root<rad:root+=1
  return 2*S*S//(S+root)
 beta=[S]+[S-invg_lower(t) for t in nodes[1:]]
 K1=max(1,R//weights[-1]);assert weights[-1]*(K1+1)>=R;powers=[S]*len(T);rp=RR[1];minA=None;argA=0
 for k in range(1,K1):
  powers=[p*t[0]//S for p,t in zip(powers,T)];rp=ceildiv(rp*RR[1],S);gap=(k+1)*sum(w[0]*p//S for w,p in zip(W,powers))-rp;assert gap>0,('A',k,F(gap,S));rel=F(gap,rp)
  if minA is None or rel<minA:minA=rel;argA=k
 print('integer first infinite family PASS tail from',K1,flush=True)
 t0=F(d['second_tail_t0']);t1=F(d['second_tail_t1']);K2=int(d['second_tail_k']);assert R<t0<t1<=end and K2>=1
 # Independently bound the derivative with respect to delta=1-t on
 # the tail interval: every nonconstant derivative term is bounded
 # below by minus its absolute coefficient times (1-t0)^power.
 slope_lower=aa[0]
 for j in range(2,len(aa)+1):slope_lower-=j*abs(aa[j-1])*(1-t0)**(j-1)
 assert slope_lower>0, 'tail envelope decreasing'
 cap=sum(a*(1-t1)**j for j,a in enumerate(aa,1));assert cap>0
 tail=interval_multiply(enc(cap*(t1-t0)),interval_power(enc(t0),K2))[0];negative=sum(interval_multiply(w,interval_power(t,K2))[1] for w,t in zip(W,T));assert tail>negative,('second tail',F(tail-negative,S))
 rj=[interval_power(RR,j) for j in range(len(lc))];ej=[interval_power(EE,j) for j in range(len(lc))];rp=RR;ep=EE;powers=[S]*len(T);wb=[ceildiv(w[1]*b,S) for w,b in zip(W,beta)];minB=None;argB=0
 for k in range(1,K2):
  rp=interval_multiply(rp,RR);ep=interval_multiply(ep,EE);powers=[ceildiv(p*t[1],S) for p,t in zip(powers,T)];integ=0
  for j,coef in enumerate(lc):
   e=interval_multiply(ep,ej[j]);r=interval_multiply(rp,rj[j]);diff=(e[0]-r[1],e[1]-r[0]);assert diff[0]>0
   bound=diff[0] if coef>=0 else diff[1];integ+=(coef.numerator*bound)//(coef.denominator*(k+j+1))
  gap=(k+1)*integ+rp[0]-(k+1)*sum(ceildiv(w*p,S) for w,p in zip(wb,powers));assert gap>0,('B',k,F(gap,S));rel=F(gap,rp[0])
  if minB is None or rel<minB:minB=rel;argB=k
  if k%50000==0:print('integer finite second moments through',k,flush=True)
 out={'status':'PASS','checker':'independent standard-library integer Mobius polynomial + fixed-point moments','certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'c':str(c),'R':str(R),'atoms':len(nodes),'bits':180,'mass_exact':'1','envelope_polynomial_degree':len(proof)-1,'primitive_polynomial_sha256':digest,'envelope_partitions':len(parts),'first_finite_through':K1-1,'first_tail_from':K1,'first_min_relative_lower':str(minA),'first_min_k':argA,'second_finite_through':K2-1,'second_tail_from':K2,'second_min_relative_lower':str(minB),'second_min_k':argB,'second_tail_gap_lower':str(F(tail-negative,S)),'seconds':time.monotonic()-start}
 if args.out:Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':main()

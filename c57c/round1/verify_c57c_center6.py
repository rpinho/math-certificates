#!/usr/bin/env python3
"""Separate Arb checker of a six-parameter higher-Grunsky certificate.

Imports no search, builder, SDP, NumPy or discovery arithmetic. Parameters
have explicitly differentiated formulas. Exterior coefficients use binomial
series; Grunsky coefficients use the literal -log(1-Q) series, independently
of the builder's inversion/square-root/Grunsky recurrences. Scalar derivative
arrays propagate these different polynomial constructions.
"""
import argparse,gzip,hashlib,json,math,pathlib,time
from fractions import Fraction as Q
from flint import arb,acb,ctx

DEG=7;DIM=6;ALPHABET='0123456789ab'
class Rejected(Exception):pass
def require(ok,why):
    if not ok:raise Rejected(why)
def rational(x):
    q=Q(x);return arb(q.numerator)/q.denominator
def complex_rational(x):return acb(rational(x))

# A scalar is (complex ball, tuple of six partial derivatives), with an
# empty tuple for a constant or a point evaluation that needs no gradient.
def j(value=0,partials=()):return (value if isinstance(value,acb) else acb(value),partials)
ZERO=j();ONE=j(1)
def plus(a,b):
    if not a[1] and not b[1]:return (a[0]+b[0],())
    return (a[0]+b[0],tuple((a[1][i] if a[1] else acb(0))+(b[1][i] if b[1] else acb(0)) for i in range(DIM)))
def scale(a,c):return (a[0]*c,tuple(v*c for v in a[1]))
def minus(a,b):return plus(a,scale(b,-1))
def product(a,b):
    if not a[1] and not b[1]:return (a[0]*b[0],())
    return (a[0]*b[0],tuple((a[1][i]*b[0] if a[1] else acb(0))+(a[0]*b[1][i] if b[1] else acb(0)) for i in range(DIM)))
def reciprocal(a):
    inverse=1/a[0];return (inverse,tuple(-v*inverse*inverse for v in a[1]))
def divide(a,b):return product(a,reciprocal(b))
def power(a,n):
    if not n:return ONE
    return (a[0]**n,tuple(n*a[0]**(n-1)*v for v in a[1]))
def conjugate(a):return (a[0].conjugate(),tuple(v.conjugate() for v in a[1]))
def real(a):return (acb(a[0].real),tuple(acb(v.real) for v in a[1]))
def imag(a):return (acb(a[0].imag),tuple(acb(v.imag) for v in a[1]))
def norm2(a):return plus(power(real(a),2),power(imag(a),2))
def affine(value=ZERO,index=0):
    row=[ZERO]*4;row[index]=value;return row
def affine_add(a,b):return [plus(x,y) for x,y in zip(a,b)]
def affine_scale(a,c):return [scale(x,c) for x in a]
def affine_product(a,b):return [product(a[0],b[0])]+[plus(product(a[0],b[i]),product(a[i],b[0])) for i in range(1,4)]
def affine_times_scalar(a,b):return [product(x,b) for x in a]

def poly_plus(a,b,multiplier=Q(1)):
    out=dict(a)
    for e,v in b.items():
        out[e]=out.get(e,Q(0))+multiplier*v
        if not out[e]:del out[e]
    return out
def poly_times(a,b):
    out={}
    for e,v in a.items():
        for f,w in b.items():
            exponent=tuple(x+y for x,y in zip(e,f));out[exponent]=out.get(exponent,Q(0))+v*w
    return {e:v for e,v in out.items() if v}
def independent_grunsky_polynomials():
    # Q(u,v)=sum h_k sum_{i+j=2k} u^i v^j. Coefficients of
    # -log(1-Q)=Q+Q^2/2+...+Q^7/7 suffice for i,j<=7.
    q={}
    for i in range(1,DEG+1):
        for l in range(1,DEG+1):
            if (i+l)%2==0:
                e=[0]*DEG;e[(i+l)//2-1]=1;q[i,l]={tuple(e):Q(1)}
    current=q;answer={key:dict(value) for key,value in q.items()}
    for exponent in range(2,DEG+1):
        nxt={}
        for (i,l),a in current.items():
            for (r,s),b in q.items():
                key=(i+r,l+s)
                if key[0]<=DEG and key[1]<=DEG:nxt[key]=poly_plus(nxt.get(key,{}),poly_times(a,b))
        current=nxt
        for key,value in current.items():answer[key]=poly_plus(answer.get(key,{}),value,Q(1,exponent))
    return answer
GRUNSKY=independent_grunsky_polynomials()

def prepare(witness):
    require(isinstance(witness,dict),'bad witness object');kind=witness.get('kind')
    require(kind in ('area','simple','dual'),'unknown witness kind')
    if kind=='area':return {'kind':'area'}
    forms=witness.get('forms');require(isinstance(forms,list) and 0<len(forms)<=100,'bad form count')
    norm=acb(0);poly=[{}, {}, {}];literal=[]
    for form in forms:
        mode=form.get('mode');require(type(mode) is int and 0<=mode<=2,'invalid transform mode')
        coords=form.get('z');require(isinstance(coords,list) and len(coords)==7,'bad complex vector')
        require(all(isinstance(p,list) and len(p)==2 and all(type(n) is int and abs(n)<1<<62 for n in p) for p in coords),'bad integer vector coordinates')
        require(any(r or im for r,im in coords),'zero complex vector')
        weight=Q(form['weight']);require(weight>0,'nonpositive quadratic-form weight');ww=complex_rational(weight)
        zz=[acb(r,im) for r,im in coords]
        norm+=ww*sum((i+1)*(r*r+im*im) for i,(r,im) in enumerate(coords))
        if kind=='simple':
            require(all(coords[i]==[0,0] for i in [1,3,4,5,6]),'simple form uses an unknown coefficient')
            literal.append((mode,zz[0],zz[2],ww))
        else:
            for i in range(1,DEG+1):
                for l in range(i,DEG+1):
                    coefficient=ww*i*l*zz[i-1]*zz[l-1]*(2 if i!=l else 1)
                    if coefficient==0:continue
                    for e,v in GRUNSKY.get((i,l),{}).items():poly[mode][e]=poly[mode].get(e,acb(0))+coefficient*complex_rational(v)
    if kind=='simple':return {'kind':kind,'norm':j(norm),'literal':literal}
    zeta=Q(witness['area_weight']);require(zeta>0,'nonpositive area weight')
    return {'kind':kind,'norm':j(norm),'poly':poly,'zeta':j(complex_rational(zeta))}

class CheckerArithmetic:
    def __init__(self,header,precision=160):
        ctx.prec=precision
        require(header.get('format')=='c57c-center6-dual-v1','wrong format')
        require(header.get('center')=='Wikstrom-eq9-plus-localized-a6','wrong center')
        require(header.get('bump')=='exp(-2500*(1/3-s)^2-100*abs(a4)^2)','wrong localization')
        self.R=rational(header['radius']);self.t=rational(header['t']);self.kappa=rational(header['kappa'])
        require(self.R>arb(1)/2 and self.R<arb(2)/3,'radius outside proved domain')
        require(self.t>arb(99)/100 and self.t<1,'invalid bounded-transform parameter')
        require(self.kappa>=0 and self.kappa<=arb(1)/100,'center coefficient outside proved domain')
        L=arb(25)/108+4*self.kappa/3
        require(L<self.R,'circle may meet zero');require(self.R+L<self.t.atanh(),'bounded-transform radial domain')
        self.q=(self.t/self.t.atanh())**2;self.boxes=0;self.refinements=0

    def parameters(self,cells,point=False,derivatives=True):
        x=[]
        for n,d in cells:
            center=arb(2*n+1)/2**(d+1);x.append(center if point else arb(center,arb(1)/2**(d+1)))
        s=x[0]/3;b=arb(2)/3-s*s/2;r=x[1];phi=arb.pi()*x[2]/2;theta=2*arb.pi()*x[3]
        phase=acb(phi.cos(),phi.sin());a=b*r*phase;m=b*b*r*r
        c=-3*s*a/2+acb(arb(4)/3*(x[4]-arb(1)/2),arb(4)/3*(x[5]-arb(1)/2))
        wu=arb(2)/5-m/3-s*s/5;wv=arb(25)/24-3*m/2-s*s/4
        old=s*acb(wu*a.real,-wv*a.imag)
        bump=(-2500*(arb(1)/3-s)**2-100*m).exp();turn=acb(theta.cos(),theta.sin())
        w=old+self.kappa*bump*c+self.R*turn
        if not derivatives:return j(acb(s)),j(a),j(acb(m)),j(c),j(w)
        ds=[];da=[];dm=[];dc=[];dw=[]
        for axis in range(DIM):
            sj=arb(1)/3 if axis==0 else arb(0);rj=arb(int(axis==1));phj=arb.pi()/2 if axis==2 else arb(0);thj=2*arb.pi() if axis==3 else arb(0)
            bj=-s*sj;aj=(bj*r+b*rj)*phase+acb(0,1)*a*phj;mj=2*b*r*r*bj+2*b*b*r*rj
            cj=-3*(sj*a+s*aj)/2+acb(arb(4)/3*int(axis==4),arb(4)/3*int(axis==5))
            oldj=sj*acb(wu*a.real,-wv*a.imag)+s*acb((-mj/3-2*s*sj/5)*a.real+wu*aj.real,-((-3*mj/2-s*sj/2)*a.imag+wv*aj.imag))
            bumpj=bump*(5000*(arb(1)/3-s)*sj-100*mj)
            wj=oldj+self.kappa*(bumpj*c+bump*cj)+acb(0,1)*self.R*turn*thj
            ds.append(acb(sj));da.append(aj);dm.append(acb(mj));dc.append(cj);dw.append(wj)
        return j(acb(s),tuple(ds)),j(a,tuple(da)),j(acb(m),tuple(dm)),j(c,tuple(dc)),j(w,tuple(dw))

    @staticmethod
    def area(s,a,m,c):
        term=minus(scale(c,-rational('1/2')),scale(product(s,a),rational('3/4')))
        return minus(minus(minus(ONE,scale(power(s,2),rational('3/4'))),scale(m,rational('5/4'))),scale(norm2(term),9))

    def transform(self,s,a,w,mode):
        if mode==0:return j(1),ZERO,ZERO
        if mode==1:return j(1),ZERO,reciprocal(w)
        t=j(acb(self.t));gamma=scale(divide(conjugate(w),w),acb(self.q))
        A=plus(divide(t,w),scale(product(gamma,w),1/self.t))
        return t,gamma,A

    @staticmethod
    def series_product(a,b):
        result=[affine() for _ in range(DEG+1)]
        for degree in range(DEG+1):
            for left in range(degree+1):result[degree]=affine_add(result[degree],affine_product(a[left],b[degree-left]))
        return result

    def exterior_binomial(self,s,a,c,w,mode):
        t,gamma,A=self.transform(s,a,w,mode)
        f=[affine(ONE),affine(),affine(scale(product(s,power(t,2)),-1)),affine(product(a,power(t,3))),
           affine(power(t,4),1),affine(product(c,power(t,5))),affine(power(t,6),2),affine(power(t,7),3)]
        u=[row[:] for row in f];u[0]=affine();term=[affine(ONE)]+[affine() for _ in range(DEG)]
        inv=[affine(ONE)]+[affine() for _ in range(DEG)]
        for exponent in range(1,DEG+1):
            term=self.series_product(term,u)
            inv=[affine_add(x,affine_scale(y,(-1)**exponent)) for x,y in zip(inv,term)]
        square=inv;square[1]=affine_add(square[1],affine(scale(A,-1)))
        for degree in range(2,DEG+1):square[degree]=affine_add(square[degree],affine_times_scalar(f[degree-2],gamma))
        v=[row[:] for row in square];v[0]=affine();term=[affine(ONE)]+[affine() for _ in range(DEG)]
        root=[affine(ONE)]+[affine() for _ in range(DEG)];coefficient=Q(1)
        for exponent in range(1,DEG+1):
            coefficient*=Q(1,2)-(exponent-1);coefficient/=exponent;term=self.series_product(term,v)
            root=[affine_add(x,affine_scale(y,complex_rational(coefficient))) for x,y in zip(root,term)]
        return root

    @staticmethod
    def polynomial_contraction(h,poly):
        result=affine();powers={}
        for axis in range(3):
            for exponent in range(8//(axis+1)+1):powers[axis,exponent]=power(h[axis+1][0],exponent)
        for exponent,coefficient in poly.items():
            multiplier=j(coefficient)
            for axis in range(3):
                if exponent[axis]:multiplier=product(multiplier,powers[axis,exponent[axis]])
            high=[axis for axis in range(3,7) if exponent[axis]]
            require(not high or len(high)==1 and exponent[high[0]]==1,'nonaffine unknown unexpectedly present')
            term=affine_times_scalar(h[high[0]+1],multiplier) if high else affine(multiplier)
            result=affine_add(result,term)
        return result

    def evaluate(self,cells,witness,point=False,derivatives=True):
        s,a,m,c,w=self.parameters(cells,point,derivatives);K=self.area(s,a,m,c)
        if witness['kind']=='area':return K
        if witness['kind']=='simple':
            answer=witness['norm']
            for mode,z1,z3,weight in witness['literal']:
                t,gamma,A=self.transform(s,a,w,mode);qq=plus(gamma,product(power(t,2),s));jj=scale(product(power(t,3),a),-1)
                b11=scale(A,-rational('1/2'));b13=minus(scale(qq,rational('1/2')),scale(power(A,2),rational('1/8')))
                b33=minus(scale(jj,rational('1/2')),scale(power(A,3),rational('1/24')))
                ss=plus(plus(scale(b11,z1*z1),scale(b13,6*z1*z3)),scale(b33,9*z3*z3))
                answer=plus(answer,scale(real(ss),weight))
            return real(answer)
        total=[witness['norm'],ZERO,ZERO,ZERO]
        for mode,poly in enumerate(witness['poly']):
            if poly:total=affine_add(total,self.polynomial_contraction(self.exterior_binomial(s,a,c,w,mode),poly))
        cb,cd,ce=total[1:];ds=[minus(plus(scale(cb,-2),scale(product(s,cd),3)),scale(product(a,ce),3)),scale(cd,-2),scale(ce,-2)]
        h0=[scale(power(s,2),rational('3/8')),plus(scale(power(a,2),rational('3/8')),scale(power(s,3),rational('5/16'))),minus(scale(product(s,c),-rational('3/4')),scale(product(power(s,2),a),rational('15/16')))]
        answer=plus(real(total[0]),product(witness['zeta'],K))
        for d,hh,weight in zip(ds,h0,[7,11,13]):
            answer=minus(answer,real(product(d,hh)))
            answer=plus(answer,divide(norm2(d),scale(witness['zeta'],4*weight)))
        return real(answer)

    def leaf(self,cells,witness):
        pending=[(cells,0)]
        while pending:
            box,depth=pending.pop();self.boxes+=1;require(self.boxes<=20000000,'arithmetic resource cap')
            value=self.evaluate(box,witness)
            if value[0].is_finite() and value[0].real<0:continue
            midpoint=self.evaluate(box,witness,True,False)
            require(midpoint[0].is_finite(),'nonfinite midpoint')
            require(not midpoint[0].real>=0,'quadratic form fails at exact midpoint')
            bound=midpoint[0].real
            if value[1]:
                for partial,(n,d) in zip(value[1],box):bound+=partial.real*arb(0,arb(1)/2**(d+1))
                if bound<0:continue
            require(depth<24,'additional subdivision cap; inequality unverified')
            self.refinements+=1
            try:weights=[float(abs(partial.real).upper())/2**d for partial,(n,d) in zip(value[1],box)]
            except (ValueError,OverflowError):weights=[]
            if len(weights)!=6 or not all(math.isfinite(x) for x in weights):weights=[v/2**d for v,(n,d) in zip([1/3,2/3,1,4,4/3,4/3],box)]
            axis=max(range(6),key=lambda k:weights[k]);n,d=box[axis];lo=list(box);hi=list(box);lo[axis]=(2*n,d+1);hi[axis]=(2*n+1,d+1)
            pending.extend([(tuple(hi),depth+1),(tuple(lo),depth+1)])

def verify(artifact,precision=160,structure_only=False,quiet=False,receipt=None):
    started=time.monotonic();count=0;maxdepth=0;definitions=0
    with gzip.open(artifact,'rt') as stream:
        header=json.loads(next(stream));arithmetic=CheckerArithmetic(header,precision);library=[prepare({'kind':'area'})]
        def read():
            nonlocal definitions
            while True:
                line=stream.readline()
                if not line:return None
                obj=json.loads(line)
                if isinstance(obj,dict):
                    require(set(obj)=={'D'},'unknown definition record');index,witness=obj['D']
                    require(type(index) is int and index==len(library),'out-of-order witness definition')
                    require(index<500000,'witness definition cap');library.append(prepare(witness));definitions+=1
                else:
                    require(isinstance(obj,list) and len(obj)==2,'bad leaf encoding');path,index=obj
                    require(isinstance(path,str) and len(path)<=500 and all(c in ALPHABET for c in path),'bad subdivision path')
                    require(type(index) is int and 0<=index<len(library),'undefined witness');return path,index
        record=read()
        def cover(prefix,cells):
            nonlocal record,count,maxdepth
            require(record is not None,'missing subtree / incomplete artifact');path,index=record
            require(path.startswith(prefix),'wrong subtree, duplicate or out-of-order leaf')
            if path==prefix:
                if not structure_only:arithmetic.leaf(cells,library[index])
                count+=1;maxdepth=max(maxdepth,len(path));require(count<=5000000,'leaf resource cap')
                if not quiet and count%10000==0:print(json.dumps({'leaves':count,'boxes':arithmetic.boxes,'seconds':time.monotonic()-started}),flush=True)
                record=read();return
            digit=ALPHABET.index(path[len(prefix)]);require(digit%2==0,'missing lower child');axis=digit//2;n,d=cells[axis]
            lo=list(cells);hi=list(cells);lo[axis]=(2*n,d+1);hi[axis]=(2*n+1,d+1)
            cover(prefix+ALPHABET[2*axis],tuple(lo));cover(prefix+ALPHABET[2*axis+1],tuple(hi))
        cover('',((0,0),)*6);require(record is None,'extraneous leaf')
    result={'status':'STRUCTURE_ONLY_NOT_A_PROOF' if structure_only else 'VERIFIED_CANDIDATE_UNREFEREED',
            'radius':header['radius'],'kappa':header['kappa'],'t':header['t'],'leaves':count,'max_depth':maxdepth,
            'witness_definitions':definitions,'arithmetic_boxes':arithmetic.boxes,'extra_subdivisions':arithmetic.refinements,
            'precision':precision,'seconds':time.monotonic()-started,'artifact_sha256':hashlib.sha256(pathlib.Path(artifact).read_bytes()).hexdigest(),
            'checker_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
    if receipt:pathlib.Path(receipt).write_text(json.dumps(result,indent=2)+'\n')
    if not quiet:print(json.dumps(result,indent=2),flush=True)
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('--precision',type=int,default=160);p.add_argument('--structure-only',action='store_true');p.add_argument('--receipt');a=p.parse_args()
    try:verify(a.artifact,a.precision,a.structure_only,receipt=a.receipt)
    except (Rejected,ValueError,KeyError,TypeError,ZeroDivisionError,StopIteration) as e:
        print('REJECTED:',str(e),flush=True);raise SystemExit(1)

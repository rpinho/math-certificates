#!/usr/bin/env python3
"""Standalone, separately implemented Arb checker for the four-variable packet.

No search/SDP/builder imports. Higher coefficients use literal binomial and
logarithm series from checker-only modules. The quadratic is assembled by
sparse polynomial algebra, and positivity uses an exactly checked dyadic
congruence followed by strict Gershgorin inequalities, not builder LDL.
"""
import argparse,gzip,hashlib,json,math,pathlib,time
from fractions import Fraction as Q
from flint import arb,acb,ctx,arb_mat
from verify_c57c_center6 import (Rejected,require,rational,prepare as prepare_common,
    j,plus,minus,scale,product,power,divide,conjugate,real,reciprocal)
from c57c_checker_hessian import prepare as prepare_higher,scalar_coefficients,quadratic_gram
from c57c_checker_laurent_phase_trig_fast import gram as laurent_gram,positive_mean
from c57c_checker_bloch_fast import validate as validate_disks
from c57c_checker_scaled_bloch_fast import validate as validate_scaled_disks
from c57c_checker_pd import certified_pd
from c57c_checker_parabolic import lemma as parabolic_lemma,excluded as domain_excluded,ranges as parabolic_ranges

def prepare(w):
    require(isinstance(w,dict),'bad witness')
    if w.get('kind')=='blend':
        axis=w.get('axis');window=w.get('window');require(type(axis)is int and 0<=axis<4,'blend axis')
        require(isinstance(window,list)and len(window)==2 and all(type(v)is int for v in window),'blend window')
        n,d=window;require(0<=d<=200 and 0<=n<2**d,'blend window range')
        require(w.get('left',{}).get('kind')=='taylor4'and w.get('right',{}).get('kind')=='taylor4','blend children must be static Taylor forms')
        return {'kind':'blend','axis':axis,'window':window,'left':prepare(w['left']),'right':prepare(w['right'])}
    if w.get('kind')=='a4cap':
        require(set(w)=={'kind'},'invalid coefficient-domain cap');return {'kind':'a4cap'}
    if w.get('kind')=='blochcap':
        r=Q(w['r']);require(0<r<=Q(1,4),'Bloch-cap radius outside proved domain');return {'kind':'blochcap','r':rational(r)}
    if w.get('kind')=='simple':return prepare_common(w)
    require(w.get('kind')=='taylor4','unknown witness kind');p=prepare_higher(w);validate_disks(w.get('bloch_disks',[]));validate_scaled_disks(w.get('scaled_disks',[]));require(w.get('phase_rule')in(None,'j*theta/2'),'invalid phase rule');p['kind']='taylor4';p['raw']=w;return p

def positive_by_congruence(gram):
    # Floating Cholesky only proposes an invertible rational preconditioner.
    # Acceptance below is entirely Arb and does not trust that factorization.
    n=9;A=[[-v for v in row] for row in gram]
    try:
        mid=[[float(v.mid()) for v in row] for row in A];L=[[0.]*n for _ in range(n)]
        for i in range(n):
            for k in range(i+1):
                v=mid[i][k]-sum(L[i][r]*L[k][r] for r in range(k))
                if i==k:
                    if not math.isfinite(v) or v<=0:return False
                    L[i][k]=math.sqrt(v)
                else:L[i][k]=v/L[k][k]
        proposed=[[0.]*n for _ in range(n)]
        for column in range(n):
            for row in range(column,-1,-1):proposed[row][column]=((1. if row==column else 0.)-sum(L[k][row]*proposed[k][column] for k in range(row+1,column+1)))/L[row][row]
        R=[[rational(Q.from_float(v)) for v in row] for row in proposed]
        require(all(R[i][i]>0 for i in range(n)),'singular dyadic congruence proposal')
        require(all(R[i][k]==0 for i in range(n) for k in range(i)),'nontriangular congruence')
        rr=arb_mat(R);product=rr.transpose()*arb_mat(A)*rr
        B=[[product[i,j]for j in range(n)]for i in range(n)]
        return certified_pd(B)
    except (ValueError,OverflowError,ZeroDivisionError):return False

class Arithmetic:
    def __init__(self,head,precision=192):
        ctx.prec=precision
        self.parabolic=head.get('format')in('c57c-bloch-parabolic-v3','c57c-scaled-bloch-v4','c57c-moving-phase-v7')
        self.shifted=self.parabolic or head.get('format')=='c57c-shifted6-taylor4-v2'
        if self.parabolic:parabolic_lemma()
        if self.shifted:
            require(head.get('center')=='Wikstrom-eq9-plus-localized-shifted-a6','wrong center')
            self.mu=rational(head['mu']);require(self.mu>=0 and self.mu<=6,'unsupported shift')
        else:
            require(head.get('format')=='c57c-center6-taylor4-v1','wrong format')
            require(head.get('center')=='Wikstrom-eq9-plus-localized-a6','wrong center');self.mu=arb(0)
        require(head.get('bump')=='exp(-2500*(1/3-s)^2-100*abs(a4)^2)','wrong bump')
        require(head.get('coefficient_caps')==['1','1','2','3'],'wrong coefficient caps')
        self.R=rational(head['radius']);self.t=rational(head['t']);self.kappa=rational(head['kappa'])
        require(self.R>arb(1)/2 and self.R<arb(2)/3,'unsupported radius')
        require(self.t>arb(99)/100 and self.t<1,'invalid t')
        require(self.kappa>=0 and self.kappa<=arb(1)/100,'unsupported center coefficient')
        require(arb(1)/12+2/arb(7).sqrt()<1,'a5 cap')
        require(2/arb(11).sqrt()+arb(1)/2+arb(1)/3+arb(5)/216<2,'a7 cap')
        require(2/arb(13).sqrt()+arb(1)/2+1+arb(5)/36<3,'a8 cap')
        # This stronger bound covers even the fictitious square used by
        # the simple forms, as well as every actual |a6|<=1 circle.
        L=arb(25)/108+(3 if self.shifted else 2)*self.kappa
        require(L<self.R,'circle can meet zero');require(self.R+L<self.t.atanh(),'bounded-transform domain')
        self.q=(self.t/self.t.atanh())**2;self.boxes=0;self.extra=0

    def parameters(self,cells,point=False):
        x=[]
        for n,d in cells:
            center=arb(2*n+1)/2**(d+1);x.append(center if point else arb(center,arb(1)/2**(d+1)))
        s=(1-x[0]**2)/3 if self.parabolic else x[0]/3;b=arb(2)/3-s*s/2;r=x[1];phi=arb.pi()*x[2]/2;theta=2*arb.pi()*x[3]
        phase=acb(phi.cos(),phi.sin())
        if self.parabolic:a=acb(b*x[1],arb(3)/2*x[0]*x[2]);m=a.real**2+a.imag**2
        else:a=b*r*phase;m=b*b*r*r
        wu=arb(2)/5-m/3-s*s/5;wv=arb(25)/24-3*m/2-s*s/4;old=s*acb(wu*a.real,-wv*a.imag)
        turn=acb(theta.cos(),theta.sin());w0=old+self.R*turn
        epsilon=self.kappa*(-2500*(arb(1)/3-s)**2-100*m).exp()
        return x,s,b,r,phase,a,m,wu,wv,turn,w0+epsilon*self.mu*s*a,epsilon

    def simple(self,cells,witness,point=False,derivatives=True):
        x,s,b,r,phase,a,m,wu,wv,turn,w0,epsilon=self.parameters(cells,point)
        if self.shifted:
            xi=acb(arb(0,arb(2)/3),arb(0,arb(2)/3));unknown=-3*s*a/2+xi
        else:unknown=acb(arb(0,1),arb(0,1))
        w=w0+epsilon*unknown
        if derivatives:
            ds=[];da=[];dw=[]
            for axis in range(6):
                thj=2*arb.pi() if axis==3 else arb(0)
                if self.parabolic:
                    sj=-2*x[0]/3 if axis==0 else arb(0);bj=-s*sj
                    real_j=bj*x[1]+(b if axis==1 else 0);imag_j=arb(3)/2*((x[2] if axis==0 else 0)+(x[0] if axis==2 else 0));aj=acb(real_j,imag_j);mj=2*a.real*real_j+2*a.imag*imag_j
                else:
                    sj=arb(1)/3 if axis==0 else arb(0);rj=arb(int(axis==1));phj=arb.pi()/2 if axis==2 else arb(0)
                    bj=-s*sj;aj=(bj*r+b*rj)*phase+acb(0,1)*a*phj;mj=2*b*r*r*bj+2*b*b*r*rj
                oldj=sj*acb(wu*a.real,-wv*a.imag)+s*acb((-mj/3-2*s*sj/5)*a.real+wu*aj.real,-((-3*mj/2-s*sj/2)*a.imag+wv*aj.imag))
                epsj=epsilon*(5000*(arb(1)/3-s)*sj-100*mj)
                ds.append(acb(sj));da.append(aj);dw.append(oldj+acb(0,1)*self.R*turn*thj+epsj*(unknown+self.mu*s*a)+epsilon*((self.mu-arb(3)/2)*(sj*a+s*aj) if self.shifted else 0))
            ss=j(acb(s),tuple(ds));aa=j(a,tuple(da));ww=j(w,tuple(dw))
        else:ss=j(acb(s));aa=j(a);ww=j(w)
        # Clear denominators by the positive factor 8*|w|^6. The
        # independent checker assembles the scaled B11,B13,B33 literally.
        rr=real(product(ww,conjugate(ww)));rr2=power(rr,2);rr3=power(rr,3);cw=conjugate(ww)
        answer=scale(product(rr3,witness['norm']),8)
        for mode,z1,z3,weight in witness['literal']:
            if mode==0:tt=j(1);qq=j();hh=j()
            elif mode==1:tt=j(1);qq=j();hh=j(1)
            else:
                tt=j(acb(self.t));qq=j(acb(self.q));hh=plus(tt,scale(product(qq,rr),1/self.t))
            b11=scale(product(product(hh,cw),rr2),-4)
            b13=plus(scale(product(product(qq,power(cw,2)),rr2),4),scale(product(product(power(tt,2),ss),rr3),4))
            b13=minus(b13,product(product(power(hh,2),power(cw,2)),rr))
            b33=minus(scale(product(product(power(tt,3),aa),rr3),-4),scale(product(power(hh,3),power(cw,3)),rational('1/3')))
            value=plus(plus(scale(b11,z1*z1),scale(b13,6*z1*z3)),scale(b33,9*z3*z3))
            answer=plus(answer,scale(real(value),weight))
        return real(answer)

    def gram(self,cells,witness,point=False):
        witness['parabolic']=self.parabolic
        return laurent_gram(cells,witness,self.R,self.kappa,self.t,self.q,point,self.mu)

    def legacy_gram(self,cells,witness,point=False):
        _,s,b,r,phase,a,m,wu,wv,turn,w0,epsilon=self.parameters(cells,point)
        point_w=(w0,acb(1),acb(0,1),acb(0),acb(0),acb(0))
        coefficients=scalar_coefficients(s,a,point_w,self.t,self.q,witness)
        radius=epsilon.upper();whole=acb(arb(w0.real,radius),arb(w0.imag,radius))
        full_w=(whole,acb(1),acb(0,1),acb(0),acb(0),acb(0))
        bounds=scalar_coefficients(s,a,full_w,self.t,self.q,witness);second=[]
        for index in [3,4,5]:second.append((abs(bounds[0][index])+sum(cap*abs(row[index]) for cap,row in zip([1,1,2,3],bounds[1:]))).upper())
        cartesian=second[0].union(second[2]).upper()+second[1]
        complex_direction=arb(0)
        for cap,row in zip([1,1,1,2,3],bounds):
            pure=(row[3]-2*acb(0,1)*row[4]-row[5])/4
            cross=(row[3]+row[5])/4
            opposite=(row[3]+2*acb(0,1)*row[4]-row[5])/4
            complex_direction+=cap*(abs(pure)+2*abs(cross)+abs(opposite))
        E=(epsilon**2*min(cartesian,complex_direction.upper())/2).upper()
        return quadratic_gram(s,a,m,epsilon,E,coefficients,witness['zeta']),E

    def bloch_margin(self,cells,witness,point=False):
        # Independent direct derivative inequality, without dividing by r^2.
        values=[]
        for n,d in cells[:3]:
            center=arb(2*n+1)/2**(d+1);values.append(center if point else arb(center,arb(1)/2**(d+1)))
        if self.parabolic:s,v=parabolic_ranges(cells,point)
        else:s=values[0]/3;v=(arb(2)/3-s*s/2)*values[1]*(arb.pi()*values[2]/2).sin()
        r=witness['r'];ratio=5*r/4
        tail=5*r**4+6*r**5+14*r**6+24*r**7+(arb(25)/9)*ratio**8/(1-ratio)
        derivative_lower=1+3*s*r*r+4*v*r**3-tail
        return derivative_lower-1/(1-r*r)

    def leaf(self,cells,witness):
        todo=[(cells,0)]
        while todo:
            box,depth=todo.pop();self.boxes+=1;require(self.boxes<=20000000,'arithmetic resource cap')
            if witness['kind']=='a4cap':
                require(self.parabolic,'coefficient cap only defined for parabolic map')
                if domain_excluded(box)>0:continue
                require(not domain_excluded(box,True)<=0,'coefficient cap fails at midpoint');weights=[1/2**box[0][1],1/2**box[1][1],1/2**box[2][1],0.]
            elif witness['kind']=='blochcap':
                value=self.bloch_margin(box,witness)
                if value>0:continue
                middle=self.bloch_margin(box,witness,True);require(not middle<=0,'Bloch cap fails at midpoint')
                r=float(witness['r']);amax=(2/3)*(box[1][0]+1)/2**box[1][1]
                weights=[v/2**d for v,(n,d) in zip([2.,0.,6*r,0.] if self.parabolic else [1.,3*r,2*r*max(amax,1e-8),0.],box)]
            elif witness['kind']=='simple':
                value=self.simple(box,witness)
                if value[0].is_finite() and value[0].real<0:continue
                middle=self.simple(box,witness,True,False);bound=middle[0].real
                if value[1]:
                    for derivative,(n,d) in zip(value[1],box):bound+=derivative.real*arb(0,arb(1)/2**(d+1))
                    if bound<0:continue
                require(not middle[0].real>=0,'simple form fails at midpoint')
                try:weights=[float(abs(g.real).upper())/2**d for g,(n,d) in zip(value[1],box)]
                except (ValueError,OverflowError):weights=[]
            else:
                gram,E=self.gram(box,witness)
                if positive_by_congruence(gram):continue
                if positive_mean(box,witness,self.R,self.kappa,self.t,self.q,E,self.mu):continue
                # A failed congruence proposal is never proof of a false
                # matrix. Refine both children before resource exhaustion.
                weights=[]
            require(depth<20,'leaf refinement resource cap; unverified')
            self.extra+=1
            if len(weights)!=4 or not all(math.isfinite(v) for v in weights):
                amax=arb(2)/3*(box[1][0]+1)/2**box[1][1];weights=[v/2**d for v,(n,d) in zip([2.,2/3,1.5*(box[0][0]+1)/2**box[0][1],2*math.pi*float(self.R)] if self.parabolic else [1/3,2/3,max(float(amax),1e-8)*math.pi/2,2*math.pi*float(self.R)],box)]
            axis=max(range(4),key=lambda k:weights[k]);n,d=box[axis];lo=list(box);hi=list(box);lo[axis]=(2*n,d+1);hi[axis]=(2*n+1,d+1)
            todo.extend([(tuple(hi),depth+1),(tuple(lo),depth+1)])

def verify(path,precision=192,structure_only=False,quiet=False,receipt=None,leaf_start=0,leaf_stop=None,root_prefix=""):
    started=time.monotonic();count=0;selected=0;maxdepth=0;kinds={'simple':0,'taylor4':0,'blochcap':0,'a4cap':0,'blend':0};library=[]
    require(type(leaf_start) is int and leaf_start>=0 and (leaf_stop is None or type(leaf_stop) is int and leaf_stop>leaf_start),'invalid leaf range')
    with gzip.open(path,'rt') as stream:
        header=json.loads(next(stream));arithmetic=Arithmetic(header,precision)
        def read():
            while True:
                line=stream.readline()
                if not line:return None
                obj=json.loads(line)
                if isinstance(obj,dict):
                    require(set(obj)=={'D'},'bad definition record');index,w=obj['D'];require(type(index) is int and index==len(library),'definition order');require(index<1000000,'definition cap');library.append(prepare(w))
                else:
                    require(isinstance(obj,list) and len(obj)==2,'bad leaf record');prefix,index=obj
                    require(isinstance(prefix,str) and len(prefix)<=200 and all(c in '01234567' for c in prefix),'bad path');require(type(index) is int and 0<=index<len(library),'undefined witness');return prefix,index
        record=read()
        def cover(prefix,box):
            nonlocal record,count,maxdepth,selected
            require(record is not None,'missing subtree / incomplete cover');target,index=record;require(target.startswith(prefix),'duplicate, wrong or unordered subtree')
            if target==prefix:
                if not structure_only and count>=leaf_start and (leaf_stop is None or count<leaf_stop):
                    arithmetic.leaf(box,library[index]);selected+=1
                count+=1;kinds[library[index]['kind']]+=1;maxdepth=max(maxdepth,len(prefix));require(count<=5000000,'leaf cap')
                if not quiet and count%5000==0:print(json.dumps({'leaves':count,'boxes':arithmetic.boxes,'seconds':time.monotonic()-started}),flush=True)
                record=read();return
            digit=int(target[len(prefix)]);require(digit%2==0,'missing lower child');axis=digit//2;n,d=box[axis];lo=list(box);hi=list(box);lo[axis]=(2*n,d+1);hi[axis]=(2*n+1,d+1)
            cover(prefix+str(2*axis),tuple(lo));cover(prefix+str(2*axis+1),tuple(hi))
        require(isinstance(root_prefix,str)and len(root_prefix)<=200 and all(c in '01234567'for c in root_prefix),'invalid root prefix')
        root_box=[(0,0)]*4
        for digit in root_prefix:
            axis=int(digit)//2;n,d=root_box[axis];root_box[axis]=(2*n+int(digit)%2,d+1)
        cover(root_prefix,tuple(root_box));require(record is None,'extraneous final leaf')
        require(leaf_start<count and (leaf_stop is None or leaf_stop<=count),'range exceeds complete cover')
    result={'status':'STRUCTURE_ONLY_NOT_A_PROOF' if structure_only else ('VERIFIED_ARITHMETIC_RANGE_NOT_FULL_PROOF' if root_prefix or leaf_start or leaf_stop is not None else 'VERIFIED_CANDIDATE_UNREFEREED'),'root_prefix':root_prefix,'format':header['format'],'center':header['center'],'mu':header['mu'] if arithmetic.shifted else '0','radius':header['radius'],'kappa':header['kappa'],'t':header['t'],
            'leaves':count,'leaf_range':[leaf_start,count if leaf_stop is None else leaf_stop],'verified_leaves':selected,'max_depth':maxdepth,'kinds':kinds,'definitions':len(library),'arithmetic_boxes':arithmetic.boxes,'extra_splits':arithmetic.extra,
            'precision':precision,'seconds':time.monotonic()-started,'artifact_sha256':hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest(),
            'checker_files':{p:hashlib.sha256(pathlib.Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ['verify_c57c_fast.py','c57c_checker_laurent_phase_trig_fast.py','verify_c57c_scaled.py','c57c_checker_laurent_scaled_fast.py','c57c_checker_scaled_bloch_fast.py','c57c_checker_hessian.py','verify_c57c_center6.py','c57c_checker_core_fast.py','c57c_checker_nested_fast.py','c57c_checker_mean_fast.py','c57c_checker_laurent_fast.py','c57c_checker_bloch_fast.py','c57c_checker_caps.py','c57c_checker_parabolic.py','c57c_checker_pd.py','c57c_checker_blend_fast.py']}}
    if receipt:pathlib.Path(receipt).write_text(json.dumps(result,indent=2)+'\n')
    if not quiet:print(json.dumps(result,indent=2),flush=True)
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('--root-prefix',default='');p.add_argument('--precision',type=int,default=192);p.add_argument('--structure-only',action='store_true');p.add_argument('--receipt');p.add_argument('--leaf-start',type=int,default=0);p.add_argument('--leaf-stop',type=int);a=p.parse_args()
    try:verify(a.artifact,a.precision,a.structure_only,receipt=a.receipt,leaf_start=a.leaf_start,leaf_stop=a.leaf_stop,root_prefix=a.root_prefix)
    except (Rejected,ValueError,KeyError,TypeError,ZeroDivisionError,StopIteration) as e:
        print('REJECTED:',str(e),flush=True);raise SystemExit(1)

"""Arb verifier, separately written (same agent), importing no search code.

Reuses our #324 cap/piece-pair checker. New modulated-radius proof steps
remain prose, unverified by any third party. No claim of independent review.
"""
import copy, json, pathlib, sys, gzip, hashlib, time
from fractions import Fraction as F
from flint import arb, arb_series, ctx
from base_verify import B, box, need, Reject, dot, plus, minus, times, mm, mp
from base_verify import Checker as OriginalChecker
ctx.prec=180

class Checker(OriginalChecker):
    def __init__(self,d):
        need(d['kind']=='c22b_even_fourier_superhelix_v1','E_KIND')
        self.mod=d['modulation'];need(set(self.mod)=={'outer_cos','inner_cos','phase_sin'},'E_MODULATION_SCHEMA')
        need(len(self.mod['outer_cos'])==len(self.mod['inner_cos']) and 1<=len(self.mod['outer_cos'])<=9,'E_ORDER')
        for key in self.mod:
            need(isinstance(self.mod[key],list) and all(type(z) is str for z in self.mod[key]),'E_COEFFICIENT_SCHEMA')
        self.coeff=[[B(F(z)) for z in self.mod['outer_cos']],[-B(F(z)) for z in self.mod['inner_cos']]]
        self.phase_coeff=[B(F(z)) for z in self.mod['phase_sin']]
        proxy=copy.deepcopy(d);proxy.pop('modulation');proxy['kind']='c22b_rational_superhelix_knot_splitcaps_v1'
        proxy['parameters']['outer_radius']=str(sum(map(F,self.mod['outer_cos'])))
        proxy['parameters']['inner_radius']=str(sum(map(F,self.mod['inner_cos'])))
        OriginalChecker.__init__(self,proxy)
        need(F(d['parameters']['outer_radius'])==sum(map(F,self.mod['outer_cos'])) and F(d['parameters']['inner_radius'])==sum(map(F,self.mod['inner_cos'])),'E_ENDPOINT_RADII')
        self.d=d
        # Recompute actual endpoint tangents; dr/du=0 and phase=0 at endpoints.
        self.ends=[]
        for j in range(4):
            origin=self.point(j,B(0));v=self.point(j,B(0),True);norm=dot(v,v).sqrt();T=times(v,1/norm);c=self.cs[j]
            need(T[1]*c>0 or T[1]*c<0,'E_CAP_TANGENT_SIGN');e=1 if T[1]*c>0 else -1
            W=[B(0),-c*e*T[2],c*e*T[1]];self.ends.append((origin,T,W,e))
        # A rigorous speed upper bound and height-derivative lower bound over
        # complete phase cells. U is rational; 44/7 > 2*pi is rechecked below.
        self.speeds=[];self.rmax=[];self.rmin=[];self.zmin=[];self.signed_radius_bounds=[]
        for j in [1,0]:
            sv=[];rr=[];zz=[];signed=[]
            for ix in range(512):
                u=box(F(44*ix,7*512),F(44*(ix+1),7*512));v=self.point(j,u,True);r=self.radius(j,u)[0]
                sv.append(dot(v,v).sqrt());rr.append(abs(r));zz.append(v[2]);signed.append(r)
            self.speeds.append(max(z.upper() for z in sv));self.rmax.append(max(z.upper() for z in rr));self.zmin.append(min(z.lower() for z in zz))
            self.signed_radius_bounds.append((min(z.lower() for z in signed),max(z.upper() for z in signed)))
        self.speeds=[self.speeds[1],self.speeds[0],self.speeds[0],self.speeds[1]]
        self.amax=self.rmax[0]

    def radius(self,j,u):
        coefficients=self.coeff[0 if j in [1,2] else 1]
        r=u*0+coefficients[0];dr=u*0;ddr=u*0
        for k,c in enumerate(coefficients[1:],1):
            r+=c*(k*u).cos();dr-=k*c*(k*u).sin();ddr-=k*k*c*(k*u).cos()
        return r,dr,ddr

    def phase(self,u):
        v=u;dv=u*0+1;ddv=u*0
        for k,c in enumerate(self.phase_coeff,1):
            v+=c*(k*u).sin();dv+=k*c*(k*u).cos();ddv-=k*k*c*(k*u).sin()
        return v,dv,ddv

    def point(self,j,u,velocity=False,acceleration=False):
        # Frenet-vector product rule, independently of cylindrical search.
        r,dr,ddr=self.radius(j,u);v,dv,ddv=self.phase(u);C=v.cos();S=-v.sin();c=self.cs[j];t=u/self.N;co=t.cos();si=t.sin()
        core=[c*self.R*co,c*self.R*si,self.h*t]
        n=[-c*co,-c*si,u*0];bn=[c*self.h/self.s*si,-c*self.h/self.s*co,u*0+self.R/self.s]
        radial=plus(times(n,C),times(bn,S))
        if not velocity and not acceleration:return times(plus(core,times(radial,r)),self.lam)
        dc=[-c*self.R*si/self.N,c*self.R*co/self.N,u*0+self.h/self.N]
        dn=[c*si/self.N,-c*co/self.N,u*0];db=[c*self.h/self.s*co/self.N,c*self.h/self.s*si/self.N,u*0]
        dC=S*dv;dS=-C*dv
        dRad=plus(plus(times(n,dC),times(dn,C)),plus(times(bn,dS),times(db,S)))
        if not acceleration:return times(plus(dc,plus(times(radial,dr),times(dRad,r))),self.lam)
        ddc=[-c*self.R*co/self.N**2,-c*self.R*si/self.N**2,u*0]
        ddn=[c*co/self.N**2,c*si/self.N**2,u*0];ddb=[-c*self.h/self.s*si/self.N**2,c*self.h/self.s*co/self.N**2,u*0]
        ddC=-C*dv*dv+S*ddv;ddS=-S*dv*dv-C*ddv
        ddRad=plus(plus(plus(times(n,ddC),times(dn,2*dC)),times(ddn,C)),plus(plus(times(bn,ddS),times(db,2*dS)),times(ddb,S)))
        return times(plus(ddc,plus(plus(times(radial,ddr),times(dRad,2*dr)),times(ddRad,r))),self.lam)

    def length_bound(self,cells=256,degree=6):
        # Taylor's theorem applied to speed f. Coefficients from interval
        # automatic differentiation bound f^(degree)/degree! on each cell.
        total=B(0);error=B(0);delta=2*arb.pi()/cells
        for j in [1,0]:
            for ix in range(cells):
                midpoint=(B(ix)+B(F(1,2)))*delta;half=delta/2
                domain=midpoint+arb(0,half.upper())
                def speed(z):
                    velocity=self.point(j,z,True)
                    return dot(velocity,velocity).sqrt()
                central=speed(arb_series([midpoint,B(1)],prec=degree+1))
                enclosing=speed(arb_series([domain,B(1)],prec=degree+1))
                need(enclosing[0]>0,'E_LENGTH_SPEED')
                val=sum(central[k]*2*half**(k+1)/(k+1) for k in range(0,degree,2))
                err=abs(enclosing[degree])*2*half**(degree+1)/(degree+1)
                total+=val+err;error+=err
        # body length per crossing: (1/2)*sum integrals of the two speeds.
        return total/2,error/2

    def leaf(self,kind,j,k,bounds,reason):
        if kind.startswith('curvature'):
            need(reason=='curvature','E_LEAF_REASON');idx=1 if kind=='curvature_outer' else 0
            lo,hi=bounds;u=box(lo,hi);mid=(lo+hi)/2
            def curvature_margin(t):
                v=self.point(idx,t,True);a=self.point(idx,t,acceleration=True)
                cross=[v[1]*a[2]-v[2]*a[1],v[2]*a[0]-v[0]*a[2],v[0]*a[1]-v[1]*a[0]]
                return dot(v,v)**3-dot(cross,cross)
            # The derivative is propagated through the independently written
            # Frenet product rules using Arb Taylor series of order one.
            direct=curvature_margin(u)
            if direct>0:return
            derivative=curvature_margin(arb_series([u,B(1)],prec=2))[1]
            need(curvature_margin(B(mid))+derivative*box(lo-mid,hi-mid)>0,'E_CURVATURE_LEAF');return
        return OriginalChecker.leaf(self,kind,j,k,bounds,reason)

    def scalar(self):
        # The cap part of the original checker is unchanged, except it uses
        # actual endpoint tangents and the certified speed/height bounds.
        a,i,R=self.a,self.i,self.R;lam=self.lam;N=self.N;s=self.s;h=self.h
        need(B(F(44,7))>2*arb.pi(),'E_PHASE_COVER')
        need(self.signed_radius_bounds[0][0]>0 and self.signed_radius_bounds[1][1]<0 and self.rmax[1]<self.amax,'E_RADII_RANGE')
        need(self.h**2>R**2 and lam*(2*R-2*self.amax)>2,'E_CROSS_BUNDLE')
        need(all(z>0 for z in self.zmin),'E_Z_MONOTONE')
        need(B(F(3,2))*self.speeds[1]<arb.pi(),'E_OUTER_SHORT_ARC')
        need(9*self.speeds[0]<arb.pi(),'E_INNER_SHORT_ARC')
        need(lam*(9*h/N-2*self.amax*R/s)>2,'E_BODY_TAIL')
        need(lam*(8*h/N-self.amax*R/s)>2,'E_BODY_END_ZONE')
        need(lam*2*arb.pi()*h>2,'E_END_SEPARATION')
        length,err=self.length_bound();need(length<self.claim,'E_LENGTH_COEFFICIENT')
        caps=[]
        for j in [2,3]:
            origin,T,W,e=self.ends[j];c=T[2];p=T[1];Qj=self.qs[j]
            need(c>0 and c<1 and ((j==2 and p>0) or (j==3 and p<0)),'E_CAP_TANGENT_SIGN')
            L=Qj*c.acos();need(L>0,'E_CAP_CONNECTOR_LENGTH')
            if L>16:need(16*c>2 or abs(self.cap(j,B(16))[1])>lam*(R+self.amax)+2,'E_CAP_END_ZONE')
            else:need(L<=16,'E_CAP_CONNECTOR_LENGTH')
            X=origin[0];Y=e*Qj*(1-c);Z=Qj*abs(p);D=(X*X+Y*Y).sqrt();theta=c.acos()
            if j==2:need(X>1 and D>4 and abs(Y)*B(3).sqrt()/2>2,'E_CAP_SIZE')
            else:need(X>2 and D>1,'E_CAP_SIZE')
            need(Qj>1,'E_CAP_CURVATURE');caps.append((X,Y,Z,D,theta,c,abs(p)))
        po,mi=caps;Xp,Yp,Zp,Dp,tp,cp,sp=po;Xm,Ym,Zm,Dm,tm,cm,sm=mi
        need(Xm-Xp>2,'E_CONNECTOR_PLANES');need(Zp-Zm-Dm>2 and Zm>2,'E_CAP_VERTICAL_SEPARATION')
        clearance=B(F(self.d['closure']['vertical_clearance']));need(clearance>2,'E_UPPER_CLEARANCE')
        ym=abs(Ym);need(Yp>ym,'E_UPPER_CHORD_DIRECTION')
        norm=((Xm+Xp)**2+(Yp-ym)**2).sqrt();D=norm/2;Zstar=Zp+clearance
        plane_distance=2*(Xm*Yp+Xp*ym)/norm;need(D>4 and plane_distance>2,'E_UPPER_PARALLEL_PLANES')
        E=4*(self.Q*tp+self.Qinner*tm)+4*Zstar-2*(Zp+Zm)+arb.pi()*(norm+Dp+Dm)
        need(E<self.additive,'E_ADDITIVE_LENGTH')
        return {'length_coefficient_upper':length.str(40),'length_remainder_upper':err.str(20),'cap_total_length':E.str(30),'upper_plane_distance':plane_distance.str(30),'cross_bundle_clearance':(lam*(2*R-2*self.amax)).str(30),'speeds':[z.str(20) for z in self.speeds],'height_derivative_lower':[z.str(20) for z in self.zmin]}

def check_folder(folder):
    P=pathlib.Path(folder);raw=(P/'CONSTRUCTION.json').read_bytes();C=Checker(json.loads(raw));scalars=C.scalar();top=C.topology();seen=set();leaves=0
    for p in sorted((P/'covers').glob('*.json.gz')):
        d=json.loads(gzip.decompress(p.read_bytes()));row=C.cover(d,raw);need(row[:3] not in seen,'E_DUPLICATE_COVER');seen.add(row[:3]);leaves+=row[3]
    expected={('interface',j,k) for j in range(4) for k in range(4)}|{('lower_cap_pair',j,3) for j in [1,2]}|{(k,0,0) for k in ['body_outer','body_cross','curvature_outer','curvature_inner']}
    need(seen==expected,'E_MISSING_COVER')
    return {'verdict':'MODULATED_GEOMETRY_PASS_CANDIDATE_UNREFEREED','verifier':'separately written (same agent)','precision_bits':ctx.prec,'covers':len(seen),'leaves':leaves,'scalars':scalars,'topology':top}

if __name__=='__main__':
    try:print(json.dumps(check_folder(sys.argv[1]),indent=2))
    except Reject as e:print(str(e));sys.exit(1)

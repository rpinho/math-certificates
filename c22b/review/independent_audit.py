"""Exact differentiation, joins, cap diagram, and arithmetic cross-checks."""
from independent_geometry import *
import sympy as S

def symbolic_derivatives():
    u,d,N0,R0,r0,r1,H,E,L=S.symbols('u d N R r k h eta lam', real=True)
    def position(r,v):
        return S.Matrix([L*((R0-r*S.cos(v))*S.cos(v/N0)-r*H*E*S.sin(v)*S.sin(v/N0)),
                         L*((R0-r*S.cos(v))*S.sin(v/N0)+r*H*E*S.sin(v)*S.cos(v/N0)),
                         L*(H*v/N0-r*R0*E*S.sin(v))])
    def rotate(v,t):
        return S.Matrix([v[0]*S.cos(t)-v[1]*S.sin(t),v[0]*S.sin(t)+v[1]*S.cos(t),v[2]])
    W0=1-H*E/N0;B0=H*E-1/N0;C0=R0*E
    v=L*rotate([r0*W0*S.sin(u),R0/N0+r0*B0*S.cos(u),H/N0-r0*C0*S.cos(u)],u/N0)
    acc=L*rotate([r0*(W0-B0/N0)*S.cos(u)-R0/N0**2,
                  r0*(W0/N0-B0)*S.sin(u),r0*C0*S.sin(u)],u/N0)
    checks={}
    for j in range(3):
        checks['velocity_'+str(j)]=S.trigsimp(S.diff(position(r0,u)[j],u)-v[j])==0
        checks['acceleration_'+str(j)]=S.trigsimp(S.diff(v[j],u)-acc[j])==0
    p=S.Matrix([R0-r0*S.cos(u),r0*H*E*S.sin(u),-r0*C0*S.sin(u)])
    q=rotate([R0-r1*S.cos(u+d),r1*H*E*S.sin(u+d),H*d/N0-r1*C0*S.sin(u+d)],d/N0)
    pu=S.Matrix([r0*S.sin(u),r0*H*E*S.cos(u),-r0*C0*S.cos(u)])
    qu=rotate([r1*S.sin(u+d),r1*H*E*S.cos(u+d),-r1*C0*S.cos(u+d)],d/N0)
    qd=rotate([r1*W0*S.sin(u+d),R0/N0+r1*B0*S.cos(u+d),H/N0-r1*C0*S.cos(u+d)],d/N0)
    for j in range(3):
        checks['pair_u_'+str(j)]=S.trigsimp(S.diff((q-p)[j],u)-(qu-pu)[j])==0
        checks['pair_d_'+str(j)]=S.trigsimp(S.diff(q[j],d)-qd[j])==0
    # Squared speed, with sin^2=1-cos^2 and eta^2=1/(R^2+h^2).
    z=S.symbols('z', real=True)
    v2=r0**2*W0**2*(1-z*z)+(R0/N0+r0*B0*z)**2+(H/N0-r0*C0*z)**2
    claimed=(R0**2+H**2)/N0**2+r0**2*W0**2-2*R0*r0*z/N0**2+r0**2*R0**2*E**2*z*z/N0**2
    diff=S.Poly(S.expand(v2-claimed),E)
    rem=S.rem(diff,S.Poly(E**2-1/(R0**2+H**2),E)).as_expr()
    checks['speed_identity']=S.simplify(rem)==0
    assert all(checks.values()),checks
    return checks

def cap_crossings_and_joins():
    # The inner lower-template semicircle intersects the two outer
    # connector projection lines at cos(theta)=+/- Xplus/Xminus.
    x=cp['X']/cm['X'];si=(1-x*x).sqrt()
    z=cm['Z']+cm['D']*si
    assert z>0 and z<cp['Z']
    # Each outer connector height is strictly increasing, so its crossing
    # parameter is unique. Circle geometry gives sin(theta_r-l/Q)=(Z_r-z)/Q.
    delta=((cp['Z']-z)/cp['Q']).asin()
    ell=cp['Q']*(cp['theta']-delta)
    right,_=connector(0,1,ell);left,_=connector(0,-1,ell)
    inner_right_depth=cm['Y']*x;inner_left_depth=-cm['Y']*x
    assert right[1]>inner_right_depth and inner_left_depth>left[1]
    # X-rotation reverses those depths for the actual lower cap.
    Y1=-(cp['Y']-cm['Y'])/2-(cp['Y']+cm['Y'])*(cm['X']-cp['X'])/(2*(cm['X']+cp['X']))
    Y2=-Y1
    assert Y1<0 and Y2>0
    join_residuals=[]
    for k,r in enumerate(radii):
        for c in [-1,1]:
            p,v,_=body(r,c,A(0)); q,w=connector(k,c,A(0))
            unit=tuple(vj/norm2(v).sqrt() for vj in v)
            assert all(d.contains(0) for d in sub(p,q))
            assert all(d.contains(0) for d in sub(unit,w))
            end,tangent=connector(k,c,caps[k]['Q']*caps[k]['theta'])
            expected=(c*caps[k]['X'],c*caps[k]['Y'],caps[k]['Z'])
            assert all(d.contains(0) for d in sub(end,expected))
            assert all(d.contains(0) for d in sub(tangent,(A(0),A(0),A(1))))
            join_residuals.append(dict(k=k,c=c,max_position_error=str(max(abs(d).upper() for d in sub(p,q))),
                max_tangent_error=str(max(abs(d).upper() for d in sub(unit,w)))))
    # Above interval residuals diagnose implementation mistakes; exact endpoint
    # identities sin(theta)=|p|, cos(theta)=c, p^2+c^2=1 prove C^1 joins.
    return dict(lower_crossing_height=str(z),lower_connector_crossing_arclength=str(ell),
                lower_template_right_depth_gap=str(right[1]-inner_right_depth),
                lower_template_left_depth_gap=str(inner_left_depth-left[1]),
                upper_crossing_depths=[str(Y1),str(Y2)],join_diagnostics=join_residuals)

def exact_arithmetic():
    a0=F(3545553,500000);rr=F(499951,500000);B0=F(1772603,250000)
    assert a0*rr<B0
    assert a0*1104+135==F(248861907,31250)
    assert (a0*1104+135)*rr/1107==F(13824306585173,1921875000000)
    assert a0*rr+150*rr/(1104*146336+3)<B0
    assert a0*rr+150*rr/(1104*146335+3)>B0
    # False stronger thickness is ruled out independently by the contact upper.
    pp,v,_=body(a,-1,A('-6252895448239407/1000000000000000'))
    qq,_,_=body(-i,-1,A('-970222336641621/200000000000000'))
    d=sub(qq,pp);dd=norm2(d);vv=norm2(v);dv=dot(d,v)
    contact=(dd*dd*vv/(4*(dd*vv-dv*dv))).sqrt()
    assert contact*A('999901/1000000')<1
    return dict(limit_of_stated_bound=str(a0*rr),gap_to_claim=str(B0-a0*rr),
                cap_intercept_after_scaling=str(F(150)*rr),false_margin_rejected=True,
                first_n_meeting_decimal_bound_using_stated_coarse_bound=146336)

def main():
    out=dict(symbolic=symbolic_derivatives(),cap_diagram=cap_crossings_and_joins(),
             arithmetic=exact_arithmetic())
    with open('audit_results.json','w') as f:json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()

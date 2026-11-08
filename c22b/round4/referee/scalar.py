from geometry import *
import time
res={}
def save(key,val):
    res[key]=({'ball':str(val),'lower':str(val.lower()),'upper':str(val.upper())} if isinstance(val,arb) else val)
    print(key,res[key],flush=True)

def bound(fun,lo,hi,test,limit=35):
    stack=[(lo,hi,0)]; acc=None; count=0
    while stack:
        l,r,d=stack.pop(); mid=(l+r)/2; U=box(l,r)
        v=fun(U)
        if not test(v):
            M=fun(Q(mid)); z=fun(arb_series([U,1],2)); v=M+z[1]*(U-Q(mid))
        if test(v):
            acc=v if acc is None else acc.union(v); count+=1
        else:
            if d>=limit: raise RuntimeError((l,r,str(v)))
            stack.extend([(l,mid,d+1),(mid,r,d+1)])
    return acc,count

if __name__=='__main__':
    from fractions import Fraction as F
    for j in range(2):
        z,n=bound(lambda u: local(u,j)[1][2],F(0),F(44,7),lambda x:x>arb('0.00000195') if j==0 else x>arb('0.30'))
        save('height_'+str(j),z); save('height_leaves_'+str(j),n)
        # natural uniform coarse bounds suffice for speed and radius
        rr=None; vv=None
        for i in range(2048):
            U=box(F(44*i,7*2048),F(44*(i+1),7*2048))
            ri=abs(radius(U,j)[0]); vi=speed(U,j)
            rr=ri if rr is None else rr.union(ri); vv=vi if vv is None else vv.union(vi)
        save('radius_'+str(j),rr); save('speed_'+str(j),vv)
        res['V'+str(j)]=str(vv.upper())
    # a'(u)=-sin(u) [a1+sum k ak U_(k-1)(cos u)].
    # |U_(k-1)| <= k, so this dominance proves max a=a(0).
    dominance=coef[0][1]-sum(m*m*abs(c) for m,c in enumerate(coef[0][2:],2))
    assert dominance>0
    save('outer_radius_dominance',dominance)
    amax=radius(arb(0),0)[0]
    save('outer_radius_max',amax)
    save('cross_bundle',lam*(2*R-2*amax)); assert lam*(2*R-2*amax)>2
    save('axis_h2_minus_R2',h*h-R*R)
    save('same_tail',lam*(9*h/N-2*amax*k))
    save('interface_tail',lam*(8*h/N-amax*k))
    save('outer_short',arb('3/2')*arb(res['V0']))
    save('inner_short',9*arb(res['V1']))
    # Independent eighth-order Taylor integration with full-cell derivative remainders.
    integrals=[]; errors=[]
    for j in range(2):
        total=arb(0); error=arb(0)
        for cell in range(512):
            m=pi*(2*cell+1)/512; d=pi/512; U=arb(m.mid(),(m.rad()+d).upper())
            a=speed(arb_series([m,1],9),j); B=speed(arb_series([U,1],9),j)
            total+=sum(2*d**(i+1)*a[i]/(i+1) for i in range(0,8,2))
            error+=2*d**9*abs(B[8])/9
        value=total+arb(0,error.upper())
        save('integral_'+str(j),value); integrals.append(value); errors.append(error)
    save('length_coefficient',(integrals[0]+integrals[1])/2)
    save('integration_remainder',(errors[0]+errors[1])/2)
    assert (integrals[0]+integrals[1])/2<arb('7.087559024')
    a,i=ends; Zstar=a['Z']+arb('21/10'); y=-i['Y']
    D=((a['X']+i['X'])**2+(a['Y']-y)**2).sqrt()/2
    E=4*(a['Q']*a['theta']+i['Q']*i['theta'])+pi*(a['D']+i['D']+2*D)+4*Zstar-2*(a['Z']+i['Z'])
    save('caps',E); assert E<150
    save('block_height',lam*2*pi*6*h)
    for j,a in enumerate(ends):
        for name,v in a.items(): save('end_'+str(j)+'_'+name,v)
    a,i=ends
    save('upper_circle_radius',D)
    save('plane_distance',(i['X']*a['Y']+a['X']*y)/D)
    save('nested_vertical_gap',a['Z']-i['Z']-i['D'])
    save('outer_Y_gap',a['Y']*arb(3).sqrt()/2)
    save('X_spacing',i['X']-a['X'])
    for j in range(2):
        save('connector_16_z_'+str(j),connector(arb(16),j)[0][2])
        save('connector_16_y_clear_'+str(j),abs(connector(arb(16),j)[0][1])-lam*(R+amax))
    cp=json.load(open('../candidate_high/CONTACT_POINT.json'))
    save('contact_input',cp)
    json.dump(res,open('scalar.json','w'),indent=2)

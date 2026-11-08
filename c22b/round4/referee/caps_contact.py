from geometry import *
from scalar import bound
from fractions import Fraction as Fr
import json
res={}
def add(name,x):
    res[name]={'lower':str(x.lower()),'upper':str(x.upper()),'ball':str(x)}
    print(name,res[name],flush=True)
a,i=ends
Zstar=a['Z']+arb('21/10'); y=-i['Y']
D=((a['X']+i['X'])**2+(a['Y']-y)**2).sqrt()/2
checks={'Xouter':a['X']-1,'Xinner':i['X']-2,'spacing':i['X']-a['X']-2,'Douter':a['D']-4,'Dupper':D-4,'Dinner':i['D']-1,'Zinner':i['Z']-2,'nested':a['Z']-i['Z']-i['D']-2,'outerY':a['Y']*arb(3).sqrt()/2-2,'Yorder':a['Y']-y,'plane':(i['X']*a['Y']+a['X']*y)/D-2,'upper_extension':Zstar-i['Z'],'upper_extension_outer':Zstar-a['Z']}
for key,v in checks.items(): assert v>0; add(key,v)
for j,e in enumerate(ends):
    assert e['c']>0 and e['c']<1 and e['e']*e['p']>0
    assert e['Q']*e['theta']<16 # Thus both connector tails are empty.
    add('connector_length_'+str(j),e['Q']*e['theta'])
    P,V=connector(arb(0),j); B,T,_=body(arb(0),j); norm=dot(T,T).sqrt()
    assert all((x-y).contains(0) for x,y in zip(P,B))
    assert all((x-y/norm).contains(0) for x,y in zip(V,T))
    E,W=connector(e['Q']*e['theta'],j)
    assert all((x-y).contains(0) for x,y in zip(E,[e['X'],e['Y'],e['Z']]))
    assert W[0].contains(0) and W[1].contains(0) and (W[2]-1).contains(0)
# Lower nested-template crossings, at X=+Xouter and its reflection.
ct=a['X']/i['X']; st=(1-ct*ct).sqrt(); z=i['Z']+i['D']*st
# z=Q*(sin(theta)-sin(theta-l/Q)); solve sin(theta-l/Q)=sin(theta)-z/Q.
ell=a['Q']*(a['theta']-(a['p']-z/a['Q']).asin())
CP,_=connector(ell,0)
assert ell>0 and ell<a['Q']*a['theta']; assert (CP[2]-z).contains(0)
add('lower_crossing_connector_l',ell)
add('lower_right_connector_minus_circle_depth',CP[1]-i['Y']*ct)
assert CP[1]-i['Y']*ct>0
# Upper semicircles: S2 over S1.
ratio=(i['X']-a['X'])/(i['X']+a['X'])
gap=a['Y']+y+(a['Y']-y)*ratio
assert ratio>0 and ratio<1 and gap>0
add('upper_depth_gap',gap)
# Selected contact is outer phase u and inner phase w in the same bundle.
u,w=map(arb,json.load(open('../candidate_high/CONTACT_POINT.json'))['phases'])
P,V,_=body(u,0); W,T,_=body(w,1); chord=sub(W,P); dist2=dot(chord,chord)
perp2=dist2-dot(chord,V)**2/dot(V,V)
rad=dist2/(2*perp2.sqrt())
add('contact_distance',dist2.sqrt()); add('contact_tangent_radius',rad)
add('contact_chord_dot_outer_tangent',dot(chord,V)); add('contact_chord_dot_inner_tangent',dot(chord,T))
assert rad<arb('1.000001')
# Exact-phase evaluations give upper endpoints for the infimal curvature radii.
for j in range(2):
    def rho(u):
        _,v,acc=local(u,j); cr=cross(v,acc)
        return dot(v,v)**arb('3/2')/dot(cr,cr).sqrt()
    # Floating-point comparisons only choose a point; Arb encloses its radius.
    vals=[rho(pi*m/128) for m in range(257)]
    index=min(range(len(vals)),key=lambda m:float(vals[m].mid()))
    add('curvature_sample_upper_'+str(j),vals[index]); res['curvature_sample_phase_'+str(j)]=str(pi*index/128)
json.dump(res,open('caps_contact.json','w'),indent=2)

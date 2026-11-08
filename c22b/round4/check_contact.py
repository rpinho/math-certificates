"""Exact selected tangent-point radius, for diagnosing remaining slack."""
import json,pathlib,sys
from fractions import Fraction as F
from verify import Checker,B,dot,minus
P=pathlib.Path(sys.argv[1]);C=Checker(json.loads((P/'CONSTRUCTION.json').read_text()));u,v=map(F,json.loads((P/'CONTACT_POINT.json').read_text())['phases'])
p=C.point(1,B(u));q=C.point(0,B(v));t=C.point(1,B(u),True);d=minus(q,p)
# Radius of the circle through p,q tangent to X'(u): |q-p|^2 |t| /(2 |t cross(q-p)|).
cross=[t[1]*d[2]-t[2]*d[1],t[2]*d[0]-t[0]*d[2],t[0]*d[1]-t[1]*d[0]]
r=dot(d,d)*dot(t,t).sqrt()/(2*dot(cross,cross).sqrt())
print(json.dumps({'qualification':'selected exact point only; not a global minimum','phases':[str(u),str(v)],'distance':dot(d,d).sqrt().str(40),'tangent_point_radius':r.str(40)},indent=2))

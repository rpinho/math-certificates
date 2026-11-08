"""Arb point-pair reach upper bound, separately written (same agent).

Only verification geometry is imported. The lower reach bound still needs
the complete covers and margin check; this component supplies an upper bound.
"""
import pathlib,json,hashlib,sys
from fractions import Fraction as F
from flint import arb,ctx
from verify import Checker,Reject,need,frac,B,minus,dot
def check(folder,certificate=None):
 P=pathlib.Path(folder);raw=(P/'CONSTRUCTION.json').read_bytes();D=json.loads(raw);m=json.loads((P/'margin.json').read_text());d=certificate if certificate is not None else json.loads((P/'CONTACT.json').read_text())
 need(set(d)=={'kind','status','artifact_sha256','indices','phases','tangent_index','radius_lower','radius_upper','false_margin_scale'},'E_CONTACT_SCHEMA')
 need(d['kind']=='selected_body_contact_v1' and d['status']=='candidate and unrefereed','E_CONTACT_KIND');need(d['artifact_sha256']==hashlib.sha256(raw).hexdigest(),'E_CONTACT_HASH')
 ids=d['indices'];need(isinstance(ids,list) and len(ids)==2 and all(type(j) is int and 0<=j<4 for j in ids),'E_CONTACT_INDEX')
 phases=d['phases'];need(isinstance(phases,list) and len(phases)==2,'E_CONTACT_PHASE');phases=list(map(frac,phases));C=Checker(D);C.scalar();need(all(B(u)>-2*arb.pi()*C.turns and u<=0 for u in phases),'E_CONTACT_PHASE')
 direction=d['tangent_index'];need(type(direction) is int and direction in [0,1],'E_CONTACT_TANGENT')
 p=C.point(ids[0],B(phases[0]));q=C.point(ids[1],B(phases[1]));v=C.point(ids[direction],B(phases[direction]),True);delta=minus(q,p);DD=dot(delta,delta);VV=dot(v,v);projection=dot(delta,v);normal=DD*VV-projection*projection
 need(DD>0 and VV>0 and normal>0,'E_CONTACT_DEGENERATE');radius=(DD*DD*VV/(4*normal)).sqrt();lower=frac(d['radius_lower']);upper=frac(d['radius_upper'])
 need(lower==frac(m['original_thickness_lower']),'E_CONTACT_LOWER_BINDING');need(radius>B(lower),'E_CONTACT_LOWER');need(radius<B(upper),'E_CONTACT_UPPER')
 bad=frac(d['false_margin_scale']);need(0<bad<1,'E_CONTACT_SCALE');need(radius*B(bad)<1,'E_CONTACT_FALSE_MARGIN')
 return {'verdict':'SELECTED_BODY_CONTACT_UPPER_PASS_CANDIDATE_UNREFEREED','verifier':'separately written (same agent)','precision_bits':ctx.prec,'radius_interval':radius.str(45),'closed_family_thickness_upper_exact':str(upper),'false_margin_scaled_radius_interval':(radius*B(bad)).str(45),'false_margin_scale':str(bad),'qualification':'selected body pair occurs in every n>=1 closure by core translation; thickness<=this tangent-point radius; lower bound requires all22 geometry covers and margin'}
if __name__=='__main__':
 try:print(json.dumps(check(sys.argv[1]),indent=2))
 except Reject as e:print(str(e));sys.exit(1)

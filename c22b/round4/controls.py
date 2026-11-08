"""Corruption controls for the new mathematical inputs, same-agent.

Runs selected semantic mutations rather than treating a hash rejection as
geometric evidence. Reuses our original partition and projection controls.
"""
import copy,gzip,json,pathlib,sys,time
from fractions import Fraction as F
import verify,verify_projection
from verify import Checker,Reject,B,need

def main(folder):
    P=pathlib.Path(folder);raw=(P/'CONSTRUCTION.json').read_bytes();D=json.loads(raw);rows=[];start=time.time()
    def trial(name,expected,action):
        try:action()
        except Reject as e:
            need(str(e)==expected,'CONTROL_WRONG_REJECTION:'+name+':'+str(e));rows.append({'name':name,'rejection':str(e)});return
        raise RuntimeError('CONTROL_ACCEPTED:'+name)
    def artifact(name,expected,modify,scalar=True):
        d=copy.deepcopy(D);modify(d)
        def act():
            c=Checker(d)
            if scalar:c.scalar()
        trial(name,expected,act)
    artifact('wrong rational period','E_PERIODS',lambda d:d['parameters'].update(core_periods=d['parameters']['core_periods']-1),False)
    artifact('false length claim','E_LENGTH_COEFFICIENT',lambda d:d['claim'].update(coefficient='7'))
    artifact('different comparison bar','E_BAR',lambda d:d['claim'].update(bar='7'),False)
    artifact('wrong crossing slope','E_CROSSING_FORMULA',lambda d:d['claim'].update(crossings_slope=d['claim']['crossings_slope']+4),False)
    artifact('wrong crossing intercept','E_CROSSING_FORMULA',lambda d:d['claim'].update(crossings_intercept=4),False)
    artifact('wrong component count','E_COMPONENT_COUNT',lambda d:d['claim'].update(components=2),False)
    artifact('inconsistent endpoint radius','E_ENDPOINT_RADII',lambda d:d['parameters'].update(outer_radius='2'),False)
    artifact('scale below schema range','E_PARAMETER_RANGE',lambda d:d['parameters'].update(scale='999/1000'),False)
    artifact('too short cap allowance','E_ADDITIVE_LENGTH',lambda d:d['claim'].update(additive='100'))
    artifact('insufficient upper clearance','E_UPPER_CLEARANCE',lambda d:d['closure'].update(vertical_clearance='1'))
    C=Checker(D)
    cv=json.loads(gzip.decompress((P/'covers/body_cross_0_0.json.gz').read_bytes()))
    for name,expected,change in [
        ('wrong geometry binding','E_ARTIFACT_HASH',lambda d:d.update(artifact_sha256='0'*64)),
        ('cover gap','E_COVER_GAP',lambda d:d['leaves'].pop(0)),
        ('duplicate cover leaf','E_DUPLICATE_OR_PREFIX',lambda d:d['leaves'].append(d['leaves'][0])),
        ('invalid leaf path','E_PATH',lambda d:d['leaves'][0].__setitem__(0,'x')),
        ('wrong leaf rationale','E_LEAF_REASON',lambda d:d['leaves'][0].__setitem__(1,'short_arc'))]:
        d=copy.deepcopy(cv);change(d);trial(name,expected,lambda d=d:C.cover(d,raw))
    # Direct semantic false distance at a rational point obtained by rounding a
    # discovery contact; no global statement depends on this selected point.
    # Shrinking spatial coordinates strongly makes that exact point invalid.
    T=copy.deepcopy(D);T['parameters']['scale']='1'
    C0=Checker(T)
    contact=json.loads((P/'CONTACT_POINT.json').read_text())
    u,v=map(F,contact['phases'])
    trial('unexpanded false unit-thickness contact','E_DISTANCE_LEAF',lambda:C0.leaf('body_cross',0,0,(u,u,v-u,v-u),'natural'))
    # A derivative term that is required by the changed geometry: increase the
    # inner constant radius and bind its endpoint consistently. The original
    # complete curvature domain must detect the resulting excess curvature.
    T=copy.deepcopy(D);T['modulation']['inner_cos'][0]=str(F(T['modulation']['inner_cos'][0])+F(1,10));T['parameters']['inner_radius']=str(sum(map(F,T['modulation']['inner_cos'])))
    Ct=Checker(T)
    trial('inner curvature corruption','E_CURVATURE_LEAF',lambda:Ct.leaf('curvature_inner',0,0,(F(0),F(0)),'curvature'))
    packet=json.loads(gzip.decompress((P/'projection.json.gz').read_bytes()))
    for name,expected,change in [
        ('wrong projection binding','E_PROJECTION_HASH',lambda d:d.update(artifact_sha256='0'*64)),
        ('wrong projection direction','E_PROJECTION_VECTOR',lambda d:d.update(projection=[1,0])),
        ('inverse bracket corruption','E_INVERSE_BRACKET',lambda d:next(iter(d['inverse_brackets'].values()))[0].__setitem__(1,next(iter(d['inverse_brackets'].values()))[0][0]))]:
        d=copy.deepcopy(packet);change(d);trial(name,expected,lambda d=d:verify_projection.Projection(raw,d))
    # Full physical word reconstruction must reject an edited crossing sign.
    d=copy.deepcopy(packet);d['word'][0]=-d['word'][0]
    trial('physical braid crossing sign','E_WORD_MISMATCH',lambda:verify_projection.Projection(raw,d).check())
    print(json.dumps({'verdict':'NEW_MODULATION_CORRUPTIONS_REJECTED','verifier':'separately written (same agent)','controls':rows,'count':len(rows),'seconds':time.time()-start},indent=2))

if __name__=='__main__':main(sys.argv[1])

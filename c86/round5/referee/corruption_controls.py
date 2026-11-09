"""Three corruptions specified by the referee, using the referee checker's routines."""
import copy,json
from fractions import Fraction as F
from referee_check import Certificate,A
from flint import arb

def normalized_bound(d):
    x=list(map(F,d['edges']));y=list(map(F,d['node_densities']))
    m=sum((v-u)*(a+b)/2 for u,v,a,b in zip(x,x[1:],y,y[1:]))
    t=sum((v-u)*((2*u+v)*a+(u+2*v)*b)/6 for u,v,a,b in zip(x,x[1:],y,y[1:]))
    d['bound']=str(t/m)
    d['bound_float']=float(t/m)

base=json.load(open('../certificate.json'));results=[]
c=Certificate(base);c.integrals();c.check_point(F(3))
for kind in ['raised_bound','raised_weight','perturbed_density_node']:
    d=copy.deepcopy(base)
    if kind=='raised_bound':
        d['bound']=str(F(d['bound'])+F(1,10**6)); detail={'increment':'1/1000000'}
    elif kind=='raised_weight':
        d['b'][0]=str(F(d['b'][0])+F(1,1000));detail={'auxiliary':0,'increment':'1/1000'}
    else:
        # Choose independently: largest positive node height at a coordinate >2.
        i=max((i for i,x in enumerate(c.x) if x>2),key=lambda i:c.y[i])
        d['node_densities'][i]=str(F(d['node_densities'][i])*F(99,100))
        normalized_bound(d)
        detail={'node':i,'x':str(c.x[i]),'old_height':base['node_densities'][i],'new_height':d['node_densities'][i],'bound_recomputed':d['bound']}
    try:
        test=Certificate(d)
        if kind=='raised_weight':
            # Degree still passes; require a genuine negative potential witness.
            detail['degree_slack']=str(test.mass-test.degree)
            test.check_point(F(3))
        else: test.integrals()
    except AssertionError as e:
        results.append(dict(control=kind,result='REJECT',detail=detail,reason=str(e)))
    else: raise RuntimeError(f'control unexpectedly accepted: {kind}')
json.dump(results,open('corruptions.json','w'),indent=2)
for r in results: print(r['control'],r['result'],r['reason'])

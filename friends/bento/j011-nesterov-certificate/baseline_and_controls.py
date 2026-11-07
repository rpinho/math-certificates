"""Primary-paper baseline and adversarial controls, independently implemented."""
import json, hashlib, itertools, copy, os
from flint import fmpq as Q, fmpq_mat as Mat
from independent_check import ldlt,check

# Safavi et al. primary PDF equations (8),(9),(12)-(17),(25),(26).
def baseline(k,root):
    k=Q(k); s=1/k; w=1-Q(root)/k
    b=(2*k-root-1)/(2*(k+root))
    a=-(1/b+2)*w+2*(b+2)+b*(s-1)/w-2*(b+1)*s
    bb=((2*b+1)*(s-1)+w)/2
    c=b-w*(s+w-1)/(2*b*(s-1))-(b+1)*s-w+1
    d=(1-s)*b; e=w-(1-s)*b; f=w*w/(b-b*s)
    P=Mat([[a,bb,c],[bb,d,e],[c,e,f]])
    A=Mat([[1+b,-b,0],[1,0,0],[-1-b,b,0]])
    B=Mat([[-1],[0],[1]])
    AB=Mat([[A[i,j] if j<3 else B[i,0] for j in range(4)] for i in range(3)])
    C=Mat([[1+b,-b,w,-1],[-s*(1+b),s*b,0,1]])
    J=Mat([[0,1],[1,0]])
    H=-AB.transpose()*P*AB-C.transpose()*J*C
    for i in range(3):
        for j in range(3):H[i,j]+=w*P[i,j]
    minors=[]
    for size in range(1,5):
        for ii in itertools.combinations(range(4),size):
            minor=Mat([[H[i,j] for j in ii] for i in ii]).det()
            assert minor>=0,(k,ii,str(minor))
            minors.append(str(minor))
    assert -4*(-k+1)**2*b*b*(-2+w)+w*(k-1+k*w)**2-4*(-k+1)*b*w*(-3*k+1+k*w)==0
    return {'kappa':str(k),'beta':str(b),'q':str(w),'P_LDL':ldlt(P,'source P'),
            'all_15_negative_LMI_principal_minors':minors,'P':[[str(P[i,j]) for j in range(3)] for i in range(3)]}

result={'source_baselines':[baseline(k,r) for k,r in [(5,3),(13,5),(25,7),(41,9)]]}
original=json.load(open('certificate.json'))
controls=[]
for kind in ['negative_multiplier','broken_function_equality','noncoercive_storage']:
    d=copy.deepcopy(original)
    if kind=='negative_multiplier':d['lam'][0]='-1'
    if kind=='broken_function_equality':d['p'][0]=str(Q(d['p'][0])+1)
    if kind=='noncoercive_storage':d['P']=[['0']*35 for _ in range(35)]
    filename='temp_control_'+kind+'.json'
    json.dump(d,open(filename,'w'))
    try:
        check(filename)
        raise RuntimeError('INVALID CERTIFICATE ACCEPTED: '+kind)
    except AssertionError as err:
        controls.append({'mutation':kind,'rejected':True,'reason':str(err)[:200]})
    os.unlink(filename) # temporary data created in this run
result['corruption_controls']=controls
# Quadratic control over every curvature h in [1/25,1]. Set z=1-h.
# Complex roots have |r|^2=beta*z. Discriminant >=0 iff
# z>=4*beta/(1+beta)^2; the larger real root increases with z.
# Thus max of endpoint and the complex regime suffices (no grid).
b=Q(21,32); zmax=Q(24,25); transition=4*b/(1+b)**2
complex_upper=b*transition
real_endpoint=Q(21,25)**2
assert transition<zmax and complex_upper<real_endpoint
result['all_scalar_quadratics']={'complex_to_real_transition_z':str(transition),
    'complex_regime_squared_max':str(complex_upper),'real_regime_squared_max':str(real_endpoint),
    'global_worst_squared_factor':str(real_endpoint)}
json.dump(result,open('baseline_controls_result.json','w'),indent=2)
print(json.dumps(result,indent=2))

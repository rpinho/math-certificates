"""Evaluate existing analytic formulas at this kappa on the pod."""
import sympy as S,json
r=S.Symbol('r'); delta=S.Rational(1,5); b=S.Rational(55,32)
p=r*(b*b*delta**3-b*b*delta-2*r*b*delta**3+2*r*b*delta+3*r*delta**2-2*delta-r)/(2*delta*r-2)
D=2*b+delta+delta*p-3*r+2*delta*r*r-delta*delta*p*r+b*b*delta**3-2*b*delta*delta-b*b*delta
E=p+r*r-b*r-delta*r-delta*p*r+b*delta*delta*r
poly=S.factor(S.together(r*(1-p)*D-E*E))
num,den=S.fraction(poly)
roots=S.polys.polytools.intervals(num,eps=S.Rational(1,10**20))
result={'dobson_2024':{'beta':'21/32','delta':'1/5','b':'55/32',
    'determinant_numerator':str(num),'determinant_denominator':str(den),'roots':[]}}
for ((lo,hi),mult) in roots:
    rr=float((lo+hi)/2); pp=float(p.subs(r,(lo+hi)/2)); dd=float(D.subs(r,(lo+hi)/2))
    # tilde-P positivity from its two leading principal minors
    T11=pp*float(delta)**2-2*rr*float(delta)+1
    T12=rr-float(delta)*pp
    T22=pp+1
    det=T11*T22-T12*T12
    ok=rr>0 and 0<1-rr*float(delta)<1 and T11>0 and det>0 and dd>=-1e-12 and 1-pp>=-1e-12
    result['dobson_2024']['roots'].append({'r_interval':[str(lo),str(hi)],'squared_factor_approx':1-rr*float(delta),'p22':pp,'D':dd,'tildeP_det':det,'constraints_numerical':ok})
g=625*r**3+2800*r**2-5184*r+2048
result['gannot_standard_beta']={'beta':'2/3','polynomial':str(g),'roots':[str(v) for v in S.nroots(g,maxsteps=200)]}
json.dump(result,open('prior_comparisons_result.json','w'),indent=2)
print(json.dumps(result,indent=2))

"""Alexander coloring module of independently reconstructed four-plat.

In a Wirtinger relation o*u*o^-1=v the abelianized Fox relation is
(1-t)O+tU-V=0. Inverting the over-meridian replaces t by t^-1.
Thus for an upward geometric braid with left-over generator, top under
color = O + t^orientation(over)*(bottom under - O). The right-over
generator has the opposite exponent. This also handles downward strands.
"""
import json
from flint import fmpz_poly

def add(a,b,scale=1):
    d=a.copy()
    for k,v in b.items():
        d[k]=d.get(k,0)+scale*v
        if not d[k]:del d[k]
    return d
def shift(a,n):return {k+n:v for k,v in a.items()}
def normalize(a):
    lo=min(a);hi=max(a);sign=1 if a[hi]>0 else -1
    return [sign*a.get(k,0) for k in range(lo,hi+1)],lo,sign

def alexander(word):
    colors=[{0:1},{},{},{0:1}]
    orientations=[1,1,-1,-1]
    for g in word:
        j=abs(g)-1;L,R=colors[j],colors[j+1]
        if g>0:
            exponent=orientations[j]
            colors[j],colors[j+1]=add(L,shift(add(R,L,-1),exponent)),L
        else:
            exponent=-orientations[j+1]
            colors[j],colors[j+1]=R,add(R,shift(add(L,R,-1),exponent))
        orientations[j],orientations[j+1]=orientations[j+1],orientations[j]
    assert orientations[0]==-orientations[3] and orientations[1]==-orientations[2]
    relations=[add(colors[0],colors[3],-1),add(colors[1],colors[2],-1)]
    normalized=[normalize(r) for r in relations]
    assert normalized[0][0]==normalized[1][0], 'Relations must be associates'
    polynomial=normalized[0][0]
    return polynomial,[(off,sign) for _,off,sign in normalized]

def main():
    # Local sanity cases: nested closed sigma_1^q gives T(2,q).
    for q in [1,3,5,7]:
        p,_=alexander([1]*q)
        assert p==[(-1)**j for j in range(q)]
    body=json.load(open('independent_braid.json'))['word']
    # Bottom cap is sigma_1 sigma_3 of the nested cap. Straightening
    # the top cap adds sigma_1, as derived directly from its crossing.
    full=[1,3]+body+[1]
    polynomial,units=alexander(full)
    assert polynomial==[(-1)**j for j in range(1107)]
    out=dict(degree=len(polynomial)-1,coefficient_rule='coefficient of t^j is (-1)^j, 0<=j<=1106',
             determinant=abs(sum(c*(-1)**j for j,c in enumerate(polynomial))),
             delta_at_one=sum(polynomial),relation_units=units,
             number_of_body_crossings=len(body),number_of_cap_crossings=3,
             local_sanity_knots=[1,3,5,7])
    with open('alexander_results.json','w') as f:json.dump(out,f,indent=2)
    print(json.dumps(out))

if __name__=='__main__':main()

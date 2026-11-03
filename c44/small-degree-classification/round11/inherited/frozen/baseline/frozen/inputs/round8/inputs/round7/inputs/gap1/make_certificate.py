"""Primary calculation of control matrices, caps and an explicit CHS polynomial."""
import json,hashlib,itertools
from fractions import Fraction as Q
from pathlib import Path
R=Path(__file__).resolve().parent
analysis=json.loads((R/'catalogue_analysis.json').read_text())
assert analysis['classes']==761
def xi(d,start=0):
    if d==1:return {1<<start:1},start+1
    a,end=xi(d-1,start+2);b,end=xi(d-1,end)
    p={}
    for mask,c in a.items():p[mask|1<<start]=c;p[mask|1<<(start+1)]=c
    for mask,c in b.items():p[mask|1<<start]=c;p[mask|1<<(start+1)]=-c
    return p,end
p,n=xi(4)
witness={'schema':'sign-fourier-integer-v1','degree':4,'variables':n,
         'denominator':8,'terms':[[m,c] for m,c in sorted(p.items())]}
(R/'witness22.json').write_text(json.dumps(witness,indent=2)+'\n')
rows=[]
for d in range(4,13):
    if d==4:n=22;branch='quartic energy envelope and equality exclusions'
    else:
        minimum=2*d-1+(2**d-2)*caps[d-1]
        nonminimum=(d*2**d)//3
        n=max(int(minimum),nonminimum);branch='inherited two-case restriction'
    if d==4:caps={1:Q(1,2),2:Q(1),3:Q(5,4)}
    caps[d]=Q(n,2**d)
    rows.append({'degree':d,'R':n,'cap':str(caps[d]),'reason':branch})
cert={'schema':'quartic-envelope-cap-v1','proof':'PROOF.md',
      'catalogue_source':'sources/F10T6.txt','catalogue_sha256':analysis['source_sha256'],
      'catalogue_classes':761,'external_completeness':'Rasoolzadeh ToSC 2023(3), n=10',
      'external_R3':10,'envelope':'D<=1+E3/4',
      'equality_signatures':[[0,1,4,2],['1/2','9/8',9,3],[1,'5/4',10,3]],
      'types':[{'fixed':3,'blocks':[]},{'fixed':2,'blocks':[2]},
               {'fixed':1,'blocks':[3]},{'fixed':1,'blocks':[2,2]},
               {'fixed':0,'blocks':[4]},{'fixed':0,'blocks':[2,3]},
               {'fixed':0,'blocks':[2,2,2]}],
      'top_energy_caps':{'point_pair_pair':'1/2','pair_triple':'3/4','three_pairs':'1/2'},
      'quartic_R':22,'caps':{str(d):str(c) for d,c in caps.items()},'rows':rows,
      'lower_recursion':{'increment':2,'seed_degree':4,'seed_variables':22,'limit':'3/2'},
      'witness_source':'witness22.json'}
(R/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
print(json.dumps({'caps':cert['caps'],'witness_terms':len(p)},indent=2))

"""Construct exact feasible primal edge tables near the float candidates."""
from fractions import Fraction
import json
from pathlib import Path

import numpy as np
from float_search import A,scale


def point(profile):
    total=10**12
    a=[round(x*total) for x in profile]
    i=max((i for i in range(5) if a[i]<4001*10**8),key=a.__getitem__)
    a[i]+=total-sum(a)
    a=[Fraction(x,total) for x in a]
    t=scale(np.array([float(x) for x in a]),A)
    cross=[Fraction(int(t[i]*t[j]*10**18),10**18) for i,j in [(0,2),(0,3),(1,3),(1,4),(2,4)]]
    return dict(a=list(map(str,a)),cross=list(map(str,cross)),t=[round(x*10**15) for x in t])


points=[dict(d=row['d'],r=str(row['r']),name='candidate',**point(row['profile']))
        for row in json.loads(Path('float.json').read_text())]
for r in ('0','0.015'):
    points.append(dict(d=10,r=r,name='control',**point([.4,.0127,.18716,.4,.00014])))
Path('points.json').write_text(json.dumps(points,indent=2)+'\n')

"""Check exact primal margins, direct pairing counts and sensitivity of the checker."""
from fractions import Fraction as F
from functools import cache
import gzip
import json
from math import factorial as fac,prod
from pathlib import Path
import subprocess
import sys

from verify import arb,ball,xlog,need

EDGES=[(i,j) for i in range(5) for j in range(i+1,5) if j-i in (2,3)]


def check_points():
    rows=json.loads(Path('points.json').read_text())
    raw=json.loads(Path('float.json').read_text())
    need(len(rows)==6,'wrong point count')
    for k,row in enumerate(rows):
        d,r=row['d'],F(row['r'])
        a=list(map(F,row['a']))
        cap=F(4001,10000) if k<4 else F(2,5)
        need(sum(a)==1 and min(a)>=0 and max(a)<=cap,'profile')
        if k<4:
            need((d,r)==(raw[k]['d'],F(str(raw[k]['r']))),'candidate case')
            need(max(abs(x-F(str(y))) for x,y in zip(a,raw[k]['profile']))<F(2,10**12),'candidate moved')
        else:
            case=('0','015')[k-4]
            need(d==10 and r==(F(0),F(3,200))[k-4],'control case')
            region=json.loads(Path('control-'+case+'.json').read_text())
            need(region['status']=='FAIL_TO_CLOSE' and region['case']==case,'control label')
            den=region['denominator']
            need(all(l<=den*x<=h for x,l,h in zip(a,region['lower'],region['upper'])),'witness outside box')
        q=[[F(0) for j in a] for i in a]
        for (i,j),off in zip(EDGES,row['cross'],strict=True):
            q[i][j]=q[j][i]=F(off)
        for i in range(5):
            q[i][i]=a[i]-sum(q[i])
        need(all(x>=0 for line in q for x in line) and all(sum(line)==v for line,v in zip(q,a)),'infeasible Q')
        p=sum(a[i]*a[j] for i in range(5) for j in range(5) if (i-j)%5 in (0,2,3))
        common=(d-1)*sum(xlog(x) for x in a)+ball(r)*ball(p).log()
        primal=common-d*sum(xlog(x) for line in q for x in line)/2
        t=row['t']
        need(len(t)==5 and min(t)>0,'bad point multiplier')
        z=sum(x*x for x in t)+2*sum(t[i]*t[j] for i,j in EDGES)
        dual=common+d*(arb(z).log()/2-sum(ball(x)*arb(w).log() for x,w in zip(a,t)))
        gap=dual-primal
        need(gap<ball(F(1,10**10)),'primal-dual gap')
        if k>=2:
            need(primal>0,'missing positive witness')
        print(f"{row['name']} d={d} r={r} primal={primal.str(23)} gap={gap.str(5)}")


@cache
def actual(stubs):
    if not any(stubs):
        return 1
    i=next(k for k,s in enumerate(stubs) if s)
    rest=list(stubs)
    rest[i]-=1
    count=0
    for j,partners in enumerate(rest):
        if partners and (i-j)%5 in (0,2,3):
            rest[j]-=1
            count+=partners*actual(tuple(rest))
            rest[j]+=1
    return count


def formula(stubs):
    top=prod(map(fac,stubs))
    def visit(pos,rest,den):
        if pos==len(EDGES):
            if any(s%2 for s in rest):
                return 0
            divisor=den*prod(2**(s//2)*fac(s//2) for s in rest)
            need(top%divisor==0,'type count noninteger')
            return top//divisor
        i,j=EDGES[pos]
        ans=0
        for m in range(min(rest[i],rest[j])+1):
            left=rest.copy()
            left[i]-=m
            left[j]-=m
            ans+=visit(pos+1,left,den*fac(m))
        return ans
    return visit(0,list(stubs),1)


def small_counts():
    examples=[(2,(1,1,1,1,1),None),(3,(2,1,1,1,1),None),(3,(2,2,0,0,0),None),
              (3,(1,1,0,0,0),None),(3,(2,1,0,1,1),1),(4,(0,1,0,2,1),None)]
    for d,v,defect in examples:
        s=tuple(d*num-(i==defect) for i,num in enumerate(v))
        D=sum(s)
        count=actual(s)
        need(count==formula(s),'pairing count mismatch')
        t=[max(1,x) for x in s]
        z=sum(w*w for w in t)+2*sum(t[i]*t[j] for i,j in EDGES)
        upper=F(prod(map(fac,s))*z**(D//2),
                2**(D//2)*fac(D//2)*prod(w**x for x,w in zip(s,t)))
        need(count<=upper,'finite dual pairing bound')
        print(f'n={sum(v)} d={d} defect_class={defect} stubs={s} enumeration=formula={count} coefficient_upper_floor={upper.__floor__()}')


def check_corruption():
    with gzip.open('cert-503.json.gz','rt') as f:
        data=json.load(f)
    idx=next(i for i,r in enumerate(data['tree']) if r[0]=='L')
    node=data['tree'][idx]
    old=node[1]
    node[1]-=100*10**10
    target='cert-503-corrupt.json.gz'
    with gzip.open(target,'wt') as f:
        json.dump(data,f,separators=(',',':'))
    run=subprocess.run([sys.executable,'verify.py','503','--file',target],capture_output=True,text=True)
    need(run.returncode!=0 and 'claimed leaf bound fails' in run.stderr,'corruption went undetected')
    print(f'mutated node {idx} ticks {old} -> {node[1]}. exit={run.returncode} {run.stderr.strip()}')


if __name__=='__main__':
    check_points()
    small_counts()
    check_corruption()

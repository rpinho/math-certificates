"""Exact certificate audit. Intentionally imports no path-generation module."""
from fractions import Fraction as Q
from pathlib import Path
import copy, json


def nonnegative(c, d, lo, hi):
    assert c+lo*d >= 0, ('left inequality',c,d,lo)
    if hi is None:
        assert d >= 0, ('infinite-tail inequality',c,d)
    else:
        assert c+hi*d >= 0, ('right inequality',c,d,hi)


def check(case):
    y, w = list(map(Q,case['y'])), list(map(Q,case['alpha']))
    n = len(y)
    assert len(w)==n-1 and all(v>0 for v in w)
    prev = None
    for p in case['pieces']:
        lo, hi = Q(p['lo']), None if p['hi'] is None else Q(p['hi'])
        a,b = list(map(Q,p['a'])),list(map(Q,p['b']))
        assert len(a)==len(b)==n
        assert hi is None or hi>lo
        if prev is None:
            assert lo==0 and a==y
        else:
            oldhi,olda,oldb=prev
            assert oldhi==lo
            assert [v+lo*t for v,t in zip(a,b)] == [v+lo*t for v,t in zip(olda,oldb)]
            assert oldb != b
        assert sum(a)==sum(y) and sum(b)==0, 'stationarity at last coordinate'
        # U_i is forced by the first i stationarity equations.
        # Dual feasibility plus the sign graph is necessary and sufficient.
        ca,cb = Q(0),Q(0)
        mid=lo+1 if hi is None else (lo+hi)/2
        for i in range(n-1):
            ca+=a[i]-y[i]
            cb+=b[i]
            nonnegative(-ca,w[i]-cb,lo,hi)
            nonnegative(ca,w[i]+cb,lo,hi)
            ja,jb=a[i+1]-a[i],b[i+1]-b[i]
            if ja or jb:
                value=ja+mid*jb
                assert value!=0, 'interior sign crossing'
                s=1 if value>0 else -1
                nonnegative(s*ja,s*jb,lo,hi)
                assert ca==0 and cb==s*w[i], 'subgradient sign graph'
        prev=hi,a,b
    assert prev is not None and prev[0] is None, 'tail missing'
    assert all(v==0 for v in prev[2])
    assert all(v==sum(y)/n for v in prev[1])
    return True


def main():
    files=sorted(Path('results').glob('*.json'))
    checked=0
    for p in files:
        check(json.loads(p.read_text()))
        checked+=1
    baseline=json.loads(Path('results/fig1.json').read_text())
    assert [p['hi'] for p in baseline['pieces']] == ['25/27','25/23','100/73','25/4',None]
    assert len(json.loads(Path('results/equal_control.json').read_text())['pieces'])==3
    mutants={}
    bad=copy.deepcopy(baseline)
    bad['pieces'][0]['b'][0]=str(Q(bad['pieces'][0]['b'][0])+Q(1,100))
    mutants['slope']=bad
    bad=copy.deepcopy(baseline)
    bad['pieces'].pop(1)
    mutants['omitted_interval']=bad
    bad=copy.deepcopy(baseline)
    bad['pieces'][-1]['hi']='100'
    mutants['tail_removed']=bad
    bad=copy.deepcopy(baseline)
    bad['alpha'][0]='1/100'
    mutants['wrong_objective_weight']=bad
    mutants['zero_edge_component_control']=json.loads(Path('zero_edge_control.json').read_text())
    rejected=[]
    for name,case in mutants.items():
        try:
            check(case)
        except AssertionError as exc:
            rejected.append(dict(name=name,reason=str(exc)))
        else:
            raise AssertionError('accepted corruption '+name)
    # Independently reconstruct the paper's Theorem 4 input, not merely the
    # claimant's interpretation of it.
    source=[]
    for n in range(3,11):
        q=[Q(1),Q(2)]
        g=Q(1,3)
        while len(q)<n:
            q.append(2*q[-1]-q[-2]+2*g+1)
            g=2*g+1
        c=[(-1)**(i+1)*v for i,v in enumerate(q)]+[Q(0)]
        y=[c[i+1]-c[i] for i in range(n)]
        case=json.loads(Path(f'results/source_n{n}.json').read_text())
        assert list(map(Q,case['y']))==y
        assert list(map(Q,case['alpha']))==[Q(i*i) for i in range(1,n)]
        source.append(dict(n=n,T=len(case['pieces'])))
    out=dict(checked=checked,all_passed=True,rejected=rejected,
             source_theorem4=source,fig1_knots=[p['hi'] for p in baseline['pieces']])
    Path('second_check.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()

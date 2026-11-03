"""Separately written (same agent), integer-only frozen counterexample verifier."""
import copy
import itertools
import json
from pathlib import Path


def pattern(p):
    return tuple(sorted(p).index(x)+1 for x in p)


def word(cell, axis):
    assert len(cell)==4 and sorted(cell)==[1,2,3,4]
    assert all(pattern([cell[i] for i in inds])!=(1,3,2) for inds in itertools.combinations(range(4),3))
    free=[not any(x<cell[i] for x in cell[:i]) for i in range(4)]
    order=range(4) if axis=='position' else sorted(range(4),key=cell.__getitem__)
    return [not free[i] for i in order]


def count(restricted,sizes):
    # DP over ordered points, accumulating admissible weak slot assignments.
    boundaries=[0]
    for x in sizes:boundaries.append(boundaries[-1]+x)
    last=boundaries[-1]
    dp=[1]*(last+1)
    for j,is_restricted in enumerate(restricted):
        nxt=[]
        for slot in range(last+1):
            allowed=(not is_restricted or slot in boundaries)
            nxt.append((sum(dp[:slot+1]) if j else 1) if allowed else 0)
        dp=nxt
    return sum(dp)


def verify(c):
    assert c['connector_total_size']==3 and c['connector_components']==2
    words={}
    for name in ['a','b']:
        h=word(c['horizontal_132_cells'][name],'value')
        v=word(c['vertical_132_cells'][name],'position')
        assert h==v==c[name+'_restricted_word']
        words[name]=h
    for w in words.values():
        strips=[];n=0
        for restricted in w:
            if restricted:strips.append(n);n=0
            else:n+=1
        strips.append(n)
        assert sorted(strips)==c['common_unordered_strip_profile']
    aa=ab=0
    assert len(c['placements'])==2
    for row,sizes in zip(c['placements'],[[1,2],[2,1]]):
        assert row['component_sizes']==sizes
        vals={}
        for name,w in words.items():
            vals[name+'_forward']=count(w,sizes)
            vals[name+'_reversed']=count(w,list(reversed(sizes)))
        for name,value in vals.items():assert row[name]==value
        aa+=vals['a_forward']*vals['a_reversed']
        ab+=vals['a_forward']*vals['b_reversed']
    assert aa==c['joint_a_a'] and ab==c['joint_a_b']
    assert aa!=ab, 'no ordering discrepancy'
    return {'status':'PASS','joint_a_a':aa,'joint_a_b':ab,'same_profile_different_joint_count':True,'verifier':'separately written (same agent)'}


if __name__=='__main__':
    c=json.loads(Path('artifacts/ordering_counterexample.json').read_text())
    result=verify(c)
    controls=[]
    for key in ['joint_a_a','joint_a_b']:
        bad=copy.deepcopy(c);bad[key]+=1
        try:verify(bad)
        except AssertionError:controls.append({'field':key,'rejected':True})
        else:raise RuntimeError('corrupted counterexample accepted')
    result['rejection_controls']=controls
    Path('artifacts/ordering_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

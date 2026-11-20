"""Audit the pinned upper-bound verifier and compute true maxima by scalar ideals."""
import io,json,sys
from hashlib import sha256
from pathlib import Path
from planes import WORDS
# Check the rank-tree verifier against its digest at math-certificates 5c51a38.
two_block = Path(__file__).resolve().parents[2] / 'two-block'
verifier = two_block / 'src' / 'rank_tree_replay.py'
assert sha256(verifier.read_bytes()).hexdigest() == 'eb98702c31543eb73bdb0468c63d6bd15a9af9a2f22920a3f9b512d8aae4d93d'
sys.path.insert(0, str(verifier.parent))
from rank_tree_replay import tree, witness

def exact(word,c):
    # No threshold, component decomposition, or restriction on the number of ideals.
    n=len(word)-1
    maximum=0
    def visit(base,weights,order):
        nonlocal maximum
        ideals=[]
        for mask in range(1<<len(order)):
            if all(not (mask>>i&1) or mask&parents==parents for i,parents in enumerate(order)):
                ideals.append((mask,sum(w for i,w in enumerate(weights) if mask>>i&1)))
        maximum=max(maximum,len(ideals))
        for down,_ in ideals:
            above=[v for m,v in ideals if m&down==down]
            for delta in range(1,n-base-sum(weights)+1):
                if all(word[base+v+delta]==str(c) for v in above):
                    visit(base,weights+[delta],order+[down])
    for beta in range(n+1):
        if word[beta]==str(c):visit(beta,[],[])
    return maximum

def cube_control():
    allsets=set(range(8))
    def closed(q):return all(x|y in q and x&y in q for x in q for y in q)
    assert closed(allsets) and all(not closed(allsets-{x}) for x in allsets)
    assert exact('0000',0)==8
    # An attempted no-at-7 tree reaches the three-element antichain.
    lines=[dict(n=3,word='0000',colour=0,threshold=7,nodes=0)]
    def gen(base,ideals,weights,k):
        lines[0]['nodes']+=1
        edges=[[d,w,-1] for d in sorted(ideals) for w in range(1,4-base-weights)]
        lines.append(edges)
        for d,w,_ in edges:
            add={m|(1<<k) for m in ideals if m&d==d}
            gen(base,ideals|add,weights+w,k+1)
    for base in range(4):
        lines.append({'root':base})
        gen(base,{0},0,0)
    data=io.StringIO(''.join(json.dumps(t)+'\n' for t in lines))
    try:tree(data,'0000',0,7)
    except AssertionError as exc:
        assert 'threshold reached in no tree' in str(exc),str(exc)
    else:raise ValueError('false no-at-7 tree accepted')
    print('Boolean 3-cube: 8 closed; all eight 7-subfamilies fail closure; false no-at-7 tree rejected on ideal count')

if __name__=='__main__':
    cube_control()
    for w in WORDS:
        m=[exact(w,c) for c in (0,1)]
        assert m==[12,12]
        print('face',w,'exact maxima',*m)
    for n,folder in [(23,two_block / 'data/upper'),(22,Path('data/upper22'))]:
        record=json.loads((folder/f'upper_n{n}.json').read_text())
        word=record['word']
        for c,col in enumerate(record['colours']):
            h=col['maximum'];assert h==n-9
            witness(n,word,c,h,col['witness'])
            visited=tree(folder/Path(col['proof']).name,word,c,h+1)
            assert exact(word,c)==h
            print(n,word,'colour',c,'true maximum',h,'no-tree nodes',visited,flush=True)

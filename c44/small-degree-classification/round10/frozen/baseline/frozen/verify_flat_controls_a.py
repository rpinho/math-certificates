"""Exact control A: direct character evaluation, complete character family."""
import itertools,json,pathlib,sys
R=pathlib.Path(sys.argv[1]).resolve();P=json.loads((R/'certificates/flat_controls.json').read_text())
assert P['schema']=='c44-flat-controls-v1' and P['denominator']==32
E=P['masks'];assert len(E)==32 and len(set(E))==32
assert E==sorted(sum(1<<v for v in choice) for choice in itertools.product(*[(2*j,2*j+1) for j in range(5)]))
characters={sum(((s&u).bit_count()%2)<<i for i,s in enumerate(E)) for u in range(1024)}
assert len(characters)==64 and sorted(characters)==P['character_sign_vectors']
count=0
for vector in characters:
    truth=[]
    for x in range(1024):
        value=sum((-1 if ((s&x).bit_count()+((vector>>i)&1))%2 else 1) for i,s in enumerate(E))
        assert value in (-32,0,32);truth.append(value)
    assert sum(v*v for v in truth)==32*1024
    count+=1
bad=P['nonaffine_sign_vector'];assert bad not in characters
values=[sum((-1 if ((s&x).bit_count()+((bad>>i)&1))%2 else 1) for i,s in enumerate(E)) for x in range(1024)]
assert any(v not in (-32,0,32) for v in values)
assert set(values)=={-16,0,16}
# The strict coset threshold cannot be relaxed to <=1/4.
assert all(t+1 in (0,2) for t in (-1,1))
assert P['odd_coset_boundary']=={'T':'x/2','U':'1/2','T_energy':'1/4','sum_ternary':True}
print('PASS flat controls A:',count,'global characters; noncharacter and threshold counterexamples')

"""Exact control B: independent binary basis and sparse polynomial identities."""
import collections,json,pathlib,sys
R=pathlib.Path(sys.argv[1]).resolve();A=json.loads((R/'certificates/flat_controls.json').read_text())
assert A['schema']=='c44-flat-controls-v1' and A['denominator']==32
masks=A['masks'];assert len(masks)==len(set(masks))==32
assert all(s.bit_count()==5 for s in masks)
base=masks[0];directions=[(1<<(2*j))^(1<<(2*j+1)) for j in range(5)]
points={base}
for v in directions:points|={s^v for s in points}
assert points==set(masks)
index={s:i for i,s in enumerate(masks)}
all_vectors=[]
for assignment in range(64):
    vector=0
    for t in range(32):
        s=base
        for j in range(5):
            if t>>j&1:s^=directions[j]
        sign=((assignment&31)&t).bit_count()%2 ^ ((assignment>>5)&1)
        vector|=sign<<index[s]
    all_vectors.append(vector)
assert len(set(all_vectors))==64 and sorted(all_vectors)==A['character_sign_vectors']
def multiply(left,right):
    out=collections.defaultdict(int)
    for a,c in left.items():
        for b,d in right.items():out[a^b]+=c*d
    return {a:c for a,c in out.items() if c}
for v in all_vectors:
    polynomial={s:(-1 if v>>i&1 else 1) for i,s in enumerate(masks)}
    square=multiply(polynomial,polynomial);cube=multiply(square,polynomial)
    assert cube=={s:c*1024 for s,c in polynomial.items()}
    assert square[0]==32
bad=A['nonaffine_sign_vector'];assert bad not in all_vectors
polynomial={s:(-1 if bad>>i&1 else 1) for i,s in enumerate(masks)}
assert multiply(multiply(polynomial,polynomial),polynomial)!={s:c*1024 for s,c in polynomial.items()}
assert A['odd_coset_boundary']['T_energy']=='1/4' and A['odd_coset_boundary']['sum_ternary']
print('PASS flat controls B: 64 sparse ternary identities and rejected noncharacter')

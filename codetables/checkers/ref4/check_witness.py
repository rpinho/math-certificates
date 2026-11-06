import json
from pathlib import Path
from prepare import add,mul,eliminate,word
G=[[int(x) for x in line.split()] for line in Path('inputs/q9_n92_k13_d61.txt').read_text().splitlines()]
D=json.loads(Path('candidate.json').read_text()); R=json.loads(Path('candidate_result.json').read_text())
aug=[r+[int(i==j) for j in range(13)] for i,r in enumerate(G)]
trans=[]
for p,m in zip(D['information_sets_zero_based'],D['matrices']):
    a,p2=eliminate(aug,p)
    assert p2==p
    assert [r[:92] for r in a]==m
    u=[r[92:] for r in a]
    assert [word(G,r) for r in u]==m
    trans.append(u)
s=R['witness_set_zero_based']; coeff=R['witness_coefficients']
original=word(trans[s],coeff)
w=word(G,original)
assert w==R['witness_word'] and sum(x!=0 for x in w)==61
assert len(set(sum(D['information_sets_zero_based'],[])))==91
R['witness_original_generator_coefficients']=original
Path('witness.json').write_text(json.dumps(R,indent=2)+'\n')
print('original generator coefficients:',original)
print('scalar witness weight:',sum(x!=0 for x in w))
print('all seven transformed matrices equal exact row operations on original G')

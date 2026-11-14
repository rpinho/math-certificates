"""Seeded literal comparisons and explicit full-size negative controls."""
import json
import random
import subprocess
from pathlib import Path

rng=random.Random(491114)
Path('samples').mkdir(exist_ok=True)
results=[]
def run(label,masks,literal=False,expected=None):
    path=Path('samples')/(label+'.masks')
    path.write_text('\n'.join(map(str,masks))+'\n')
    p=subprocess.run(['./independent',str(path)]+(['literal'] if literal else []),capture_output=True,text=True)
    assert p.returncode in (0,1),(label,p.stderr)
    r=json.loads(p.stdout)
    if expected is not None: assert r['valid']==expected,(label,r)
    r.update(label=label,exit_code=p.returncode)
    results.append(r)
    Path('logs/cross_checks.json').write_text(json.dumps(results,indent=2)+'\n')
    print(label,json.dumps(r),flush=True)
    return r

base=list(map(int,Path('baseline.masks').read_text().split()))
cand=list(map(int,Path('candidate.masks').read_text().split()))
for label,v in [('baseline',base),('candidate',cand)]:
    for size in [2048,2500,3072]:
        run(label+'_'+str(size),rng.sample(v,size),True,True)

# Exercise non-Sperner families too: the 3(P-N) correction must agree literally.
for i in range(20):
    size=rng.randrange(8,48)
    run('random_small_'+str(i),rng.sample(range(1<<7),size),True)

# Independently find an added mask making a known sunflower while retaining Sperner.
# For any A,B the legal C has mandatory A&B, forbidden A^B, and free outside A|B.
cset=set(cand); full=(1<<28)-1
for attempt in range(10000):
    a,b=rng.sample(cand,2)
    c=(a&b)| (full^(a|b))
    if c in cset: continue
    if any((c&x)==c or (c&x)==x for x in cand): continue
    assert len({a,b,c})==3 and a&b==a&c==b&c
    r=run('sunflower_control',cand+[c],False,False)
    assert r['ordered_containment_pairs']==len(cand)+1
    assert r['distinct_sunflowers']>0
    sf={'added_mask':c,'witness':[a,b,c],'intersection':a&b,'search_attempt':attempt+1,
        'proper_containments':0,'distinct_sunflowers':r['distinct_sunflowers'],'exit_code':r['exit_code']}
    break
else: raise AssertionError('no Sperner-preserving sunflower control found')

assert 0 not in cset
r=run('sperner_control',cand+[0],False,False)
assert r['ordered_containment_pairs']>r['members']
controls={'sunflower':sf,'sperner':{'added_mask':0,'witness':[0,cand[0]],
    'proper_containments':r['ordered_containment_pairs']-r['members'],'exit_code':r['exit_code']},
    'random_seed':491114}
Path('logs/controls.json').write_text(json.dumps(controls,indent=2)+'\n')
print(json.dumps(controls,indent=2),flush=True)

"""Rejection controls on the actual certified family and small brute-force checks."""
import argparse,itertools,json,random,time
from pathlib import Path
import checker
start=time.monotonic()
ap=argparse.ArgumentParser();ap.add_argument('certificate',nargs='?',default='certificates/baseline.json');ap.add_argument('--output',default='logs/controls.json');args=ap.parse_args()
cert=json.loads(Path(args.certificate).read_text())
results={}
def reject(name,masks=None,claim=None,expect=''):
    c=dict(cert)
    if masks is not None:c['masks']=masks
    if claim is not None:c['claimed_rate_lower']=claim
    try:checker.verify(c)
    except checker.Invalid as e:
        reason=str(e)
        assert expect in reason,(name,reason)
        results[name]={'rejected':True,'reason':reason};return
    raise AssertionError(f'{name} accepted')
m=cert['masks']
reject('duplicate',m+[m[0]],expect='duplicate')
reject('Sperner',m+[0],expect='Sperner')
x=json.loads(Path('logs/sperner_candidate.json').read_text())
reject('added_sunflower',m+[x],expect='sunflower')
reject('raised_claimed_rate',claim=str(__import__('decimal').Decimal(cert['claimed_rate_lower'])+__import__('decimal').Decimal('0.00000000000000000001')),expect='raised claimed rate')
# Compare complete acceptance against the literal definition, including boxes
# with multiple members in either factor and triples repeating a box.
rng=random.Random(49);cases=0
for n in [5,9,12,20,28]:
    for _ in range(100):
        if n<10:
            fam=rng.sample(range(1<<n),rng.randrange(4,20))
        else:
            low=rng.sample(range(256),rng.randrange(1,4))
            uu=rng.sample(range(1<<min(n-8,10)),rng.randrange(2,5))
            vv=rng.sample(range(1<<max(0,n-18)),min(3,1<<max(0,n-18)))
            fam=sorted({a|(u<<8)|(v<<18) for a in low for u in uu for v in vv})
        # Force positive counts: match the checker's documented hypothesis.
        ports=[0,1]
        good=len({(x&1,(x>>1)&1) for x in fam})==4
        good=good and all((a&b)!=a and (a&b)!=b for a,b in itertools.combinations(fam,2))
        good=good and all(not(a&b==a&c==b&c) for a,b,c in itertools.combinations(fam,3))
        try:checker.check_family({'n':n,'ports':ports,'masks':fam});actual=True
        except checker.Invalid:actual=False
        assert actual==good,(n,fam,actual,good)
        cases+=1
# Positive nontrivial box and a triple involving two equal boxes.
fam=[(a<<8)|(b<<18)|3 for a in [3,5] for b in [3,5]]
boxes,_,_=checker.partition(fam,28)
assert len(boxes)==1 and len(boxes[0][1])==2 and len(boxes[0][2])==2
results['brute_force_definition_checks']={'cases':cases,'matched':True}
results['wall_seconds']=time.monotonic()-start
Path(args.output).write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))

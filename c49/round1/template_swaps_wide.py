"""Weighted two-template exchanges in both augmentations, keeping the 32 extras.
The 123 singleton core candidates are a preliminary filter only: the actual
search changes both 28-point lifted augmentations and certifies the full family.
"""
import argparse,collections,itertools,json,math,os,subprocess,sys,time,datetime
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--radius',type=int,default=3);args=ap.parse_args()
start=time.monotonic();data=json.loads(Path('sources/ingredients.json').read_text());cert=json.loads(Path('certificates/current.json').read_text());family=set(cert['masks']);F=data['F'];A=[data['A1'],data['A2']];kept=data['kept_edges'];glue=[2,3]
assert data['edges'][2]==[0,3] and data['edges'][3]==[0,4]
H=[[d>>1 for d in data['H'] if (d&1)==k] for k in [0,1]]
def sunflower(a,b,c):return a&b==a&c==b&c
def core(c):return sum(((c>>i)&1)<<j for j,i in enumerate(kept))
def klass(c):return 2*(c&1)+((c>>1)&1)
def lift(c,side):
    other=glue[1-side];shift=18 if side==0 else 8
    return {core(c)|(q<<shift) for q in H[1-((c>>other)&1)]}
def neighbors(side):
    g=glue[side];fp={c&~(1<<g) for c in F};aa=A[side]
    universe=[t for t in range(1024) if not(t>>g&1) and not any(t&c==t for c in fp)]
    assert len(universe)==123
    candidates=[t for t in universe if t not in aa]
    mandatory={};edges={}
    for t in candidates:
        mandatory[t]={u for u in aa if t&u in [t,u] or any(sunflower(t,u,v) for v in fp)}
        edges[t]=[(u,v) for u,v in itertools.combinations(aa,2) if sunflower(t,u,v)]
    out=[{'remove':[],'add':[],'delta':[0]*4}]
    cache={}
    for size in range(1,args.radius+1):
        for rs in itertools.combinations(aa,size):
            rr=set(rs);rest=[a for a in aa if a not in rr]
            eligible=[t for t in candidates if mandatory[t]<=rr and all(u in rr or v in rr for u,v in edges[t])]
            for k in range(1,min(size,len(eligible))+1):
                for new in itertools.combinations(eligible,k):
                    bad=False
                    for t,u in itertools.combinations(new,2):
                        key=tuple(sorted((t,u)))
                        if key not in cache:cache[key]=t&u in [t,u] or any(sunflower(t,u,v) for v in fp)
                        if cache[key] or any(sunflower(t,u,v) for v in rest):bad=True;break
                    if bad or any(sunflower(t,u,v) for t,u,v in itertools.combinations(new,3)):continue
                    delta=[0]*4
                    for r in rs:delta[klass(r)]-=len(lift(r,side))
                    for t in new:delta[klass(t)]+=len(lift(t,side))
                    out.append({'remove':list(rs),'add':list(new),'delta':delta})
    return out
nbs=[neighbors(0),neighbors(1)]
counts=[0]*4
for m in family:counts[klass(m)]+=1
def rho(v):a,b,c,d=v;return (b+c+math.sqrt((b-c)**2+4*a*d))/2
bar=rho(counts);ranked=[]
for a,b in itertools.product(*nbs):
    new=[x+y+z for x,y,z in zip(counts,a['delta'],b['delta'])]
    rr=rho(new)
    if rr>bar+1e-8:ranked.append((rr,a,b,new))
ranked.sort(key=lambda x:x[0],reverse=True)
print(json.dumps({'neighbors_per_pendant':list(map(len,nbs)),'joint_choices':len(nbs[0])*len(nbs[1]),'potential_improving':len(ranked)}),flush=True)
results=[]
for rank,(rr,a,b,new) in enumerate(ranked):
    fam=family.copy()
    for side,entry in enumerate([a,b]):
        for r in entry['remove']:fam-=lift(r,side)
        for t in entry['add']:fam|=lift(t,side)
    proposal=dict(cert);proposal['masks']=sorted(fam);proposal.pop('claimed_rate_lower',None);proposal['status']='candidate and unrefereed'
    pp=Path('certificates/template_proposal.json');pp.write_text(json.dumps(proposal,separators=(',',':'))+'\n')
    cp=Path('logs/template_proposal_check.json')
    run=subprocess.run([sys.executable,'checker.py',str(pp),'--output',str(cp)],capture_output=True,text=True)
    result=json.loads(cp.read_text());entry={'rank':rank,'left':a,'right':b,'counts':new,'verdict':result['verdict'],'reason':result.get('reason')};results.append(entry)
    if run.returncode==0:
        assert result['bar_comparison']=='above'
        rate=result['rate_interval_decimal'][0]
        if rate>json.loads(Path('certificates/current.json').read_text())['claimed_rate_lower']:
            proposal['claimed_rate_lower']=rate;name='best_'+rate[:24]+'.json'
            Path('certificates',name).write_text(json.dumps(proposal,separators=(',',':'))+'\n')
            Path('certificates/current.json').write_text(json.dumps(proposal,separators=(',',':'))+'\n');Path('certificates/current.masks').write_text(''.join(str(x)+'\n' for x in proposal['masks']))
            Path('logs/'+name+'.check.json').write_text(json.dumps(result,indent=2)+'\n')
            stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();Path('logs/last_improvement_utc.txt').write_text(stamp+'\n')
            with open('STATUS.md','a') as f:f.write('\n'+stamp+': CERTIFIED BEST '+name+' from simultaneous lifted augmentation template changes, holding the 32 exceptional sets fixed.\n')
            print('CERTIFIED_BEST '+name,flush=True)
            entry['certificate']='certificates/'+name
        break
out={'neighbors_per_pendant':list(map(len,nbs)),'joint_choices':len(nbs[0])*len(nbs[1]),'potential_improving':len(ranked),'checked':results,'wall_seconds':time.monotonic()-start}
Path(f'logs/template_swaps_radius{args.radius}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)

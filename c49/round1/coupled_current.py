"""Simultaneous weighted selection of core and two pendant template boxes.
Own implementation, exact combinatorial separation; no third-party source code.
"""
import argparse,collections,datetime,itertools,json,math,os,resource,subprocess,time
from pathlib import Path
from ortools.sat.python import cp_model
ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=10800);ap.add_argument('--threads',type=int,default=4);ap.add_argument('--seed',type=int,default=49);ap.add_argument('--resume',action='store_true');args=ap.parse_args()
start=time.monotonic();clock=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
data=json.loads(Path('sources/ingredients.json').read_text())
h0=tuple(sorted(d>>1 for d in data['H'] if not d&1));h1=tuple(sorted(d>>1 for d in data['H'] if d&1))
types=[(0,),h0,h1];type_id={a:i for i,a in enumerate(types)}
def typ(a):
    a=tuple(sorted(a))
    if a not in type_id:type_id[a]=len(types);types.append(a)
    return type_id[a]
# Complete core/pendant product/empty-part domain, plus the 21 current extras.
boxes=[(c,u,v) for c in range(256) for u in range(3) for v in range(3)]
boxes += [(0,typ((u,)),0) for u in data['W']]
kept=data['kept_edges'];edges=data['edges']
extra_core=sum(1<<kept.index(edges.index(e)) for e in [[1,2],[1,4],[2,3]])
boxes.append((extra_core,0,typ((1023,))))
existing_extra={c|(types[u][0]<<8)|(types[v][0]<<18) for c,u,v in boxes[2304:]}
for mask in map(int,Path('logs/free_extras.masks').read_text().split()):
    if mask not in existing_extra:boxes.append((mask&255,typ(((mask>>8&1023),)),typ(((mask>>18),))))
base=json.loads(Path('certificates/current.json').read_text());base_set=set(base['masks'])
baseline=[]
for i,(c,u,v) in enumerate(boxes):
    a=next(iter(types[u]));b=next(iter(types[v]));m=c|(a<<8)|(b<<18)
    if m in base_set:
        assert all((c|(a<<8)|(b<<18)) in base_set for a in types[u] for b in types[v]);baseline.append(i)
assert sum(len(types[boxes[i][1]])*len(types[boxes[i][2]]) for i in baseline)==len(base_set)
# Cache exact projected containments and sunflower existence (repetitions allowed).
sub={};flower={}
def subset(i,j):
    key=(i,j)
    if key not in sub:sub[key]=any(a&b==a for a in types[i] for b in types[j])
    return sub[key]
def sf(i,j,k):
    key=tuple(sorted((i,j,k)))
    if key not in flower:
        ans=False
        for a in types[key[0]]:
            if ans:break
            for b in types[key[1]]:
                ab=a&b;xx=a^b
                if any((c&ab)==ab and not c&xx for c in types[key[2]]):ans=True;break
        flower[key]=ans
    return flower[key]
model=cp_model.CpModel();z=[model.new_bool_var(f'b{i}') for i in range(len(boxes))]
pair_count=0
for i,(c,u,v) in enumerate(boxes):
    for j in range(i+1,len(boxes)):
        d,s,t=boxes[j]
        if ((c&d)==c and subset(u,s) and subset(v,t)) or ((c&d)==d and subset(s,u) and subset(t,v)):
            model.add(z[i]+z[j]<=1);pair_count+=1
for i in baseline:model.add_hint(z[i],1)
for i in set(range(len(boxes)))-set(baseline):model.add_hint(z[i],0)
# Initially keep most of the current core, while allowing all core/augmentation
# variables together to move. Wider neighborhoods follow automatically.
core_base=[i for i in baseline if boxes[i][1] in (1,2) and boxes[i][2] in (1,2)]
# Each slot is a real selected rectangle; no speculative science restriction.
weights=[math.sqrt(88867/33969)/2,.5,.5,math.sqrt(33969/88867)/2]
coeff=[round(1000000*weights[2*(c&1)+((c>>1)&1)]*len(types[u])*len(types[v])) for c,u,v in boxes]
model.maximize(sum(w*x for w,x in zip(coeff,z)))
known=set();iteration=0;best_rate=float(base['claimed_rate_lower']);best_ids=baseline[:];last_best=start
stats={'start_utc':clock(),'universe_boxes':len(boxes),'baseline_boxes':len(baseline),'variables':len(boxes),'containment_clauses':pair_count,'threads':args.threads,'improvements':[],'rounds':[]}
print(json.dumps({k:v for k,v in stats.items() if k not in ['improvements','rounds']}),flush=True)
# Exact separation adds only clauses witnessed in the actual selected boxes.
def separate(ids,limit=50000):
    added=0
    for ai,i in enumerate(ids):
        c,u,v=boxes[i]
        for aj in range(ai,len(ids)):
            j=ids[aj];d,s,t=boxes[j];inter=c&d
            for ak in range(aj,len(ids)):
                k=ids[ak]
                if i==k:continue
                e,w,y=boxes[k]
                if c&e!=inter or d&e!=inter:continue
                key=tuple(sorted({i,j,k}))
                if key in known:continue
                if sf(u,s,w) and sf(v,t,y):
                    known.add(key);model.add(sum(z[ii] for ii in key)<=len(key)-1);added+=1
                    if added>=limit:return added
    return added
# Check baseline science once; checker.py is separate and remains the certifier.
assert separate(baseline)==0
if args.resume and Path('logs/coupled_seed_clauses.json').exists():
    for old in json.loads(Path('logs/coupled_seed_clauses.json').read_text()):
        key=tuple(old);known.add(key);model.add(sum(z[ii] for ii in key)<=len(key)-1)
# Add all exact conflicts with two incumbent boxes at once.
bycore=collections.defaultdict(list)
for ii,(cc,uu,vv) in enumerate(boxes):bycore[cc].append(ii)
seeded=0
for ai,i in enumerate(baseline):
    c,u,v=boxes[i]
    for j in baseline[ai:]:
        d,ss,tt=boxes[j];inter=c&d;free=255^(c|d);submask=free
        while True:
            for k in bycore[inter|submask]:
                if i==j==k:continue
                key=tuple(sorted({i,j,k}))
                if key in known:continue
                e,w,y=boxes[k]
                if sf(u,ss,w) and sf(v,tt,y):
                    known.add(key);model.add(sum(z[ii] for ii in key)<=len(key)-1);seeded+=1
            submask=(submask-1)&free
            if submask==free:break
print(json.dumps({'seeded_exact_incumbent_pair_clauses':seeded,'total_clauses':len(known)}),flush=True)
Path('logs/coupled_universe.json').write_text(json.dumps({'boxes':boxes,'types':types,'baseline':baseline},separators=(',',':'))+'\n')
# Limits on core changes, enlarged in successive solves; assumptions ensure
# older neighborhood bounds are disabled as the exploration widens.
old_neighborhood=[]
while time.monotonic()-start<args.seconds:
    iteration+=1
    radius=[2,4,8,16,75][min((iteration-1)//12,4)]
    gate=model.new_bool_var(f'neighborhood_{iteration}')
    model.add(sum(1-z[i] for i in core_base)<=radius).only_enforce_if(gate)
    model.clear_assumptions();model.add_assumption(gate)
    for old in old_neighborhood:model.add_assumption(old.Not())
    old_neighborhood.append(gate)
    # Vary positive Perron-gradient pricing after each batch of exact separation.
    if iteration%12==0:
        a,d=[(33969,88867),(34000,88800),(33800,89000),(35000,90000)][(iteration//12)%4]
        ww=[math.sqrt(d/a)/2,.5,.5,math.sqrt(a/d)/2]
        coeff=[round(1000000*ww[2*(c&1)+((c>>1)&1)]*len(types[u])*len(types[v])) for c,u,v in boxes]
        model.maximize(sum(w*x for w,x in zip(coeff,z)))
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=args.threads
    solver.parameters.random_seed=args.seed+iteration
    solver.parameters.max_time_in_seconds=min(90,max(.1,args.seconds-(time.monotonic()-start)))
    solver.parameters.log_search_progress=False
    solver.parameters.max_memory_in_mb=2800
    t=time.monotonic();status=solver.solve(model)
    rec={'iteration':iteration,'radius_core_deletions':radius,'status':solver.status_name(status),'solve_seconds':time.monotonic()-t,'utc':clock()}
    if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        rec['new_clauses']=0;stats['rounds'].append(rec);print(json.dumps(rec),flush=True)
        Path('logs/coupled_progress.json').write_text(json.dumps(stats,indent=2)+'\n');continue
    ids=[i for i in range(len(z)) if solver.value(z[i])]
    counts=[0]*4
    for i in ids:
        c,u,v=boxes[i];counts[2*(c&1)+((c>>1)&1)]+=len(types[u])*len(types[v])
    a,b,c,d=counts;rho=(b+c+math.sqrt((b-c)**2+4*a*d))/2;rate=rho**(1/26)
    added=separate(ids)
    rec.update(selected_boxes=len(ids),port_counts=counts,uncertified_rate=rate,new_clauses=added,total_sunflower_clauses=len(known),objective=solver.objective_value,best_objective_bound=solver.best_objective_bound)
    if added==0:
        rec['valid_in_template_model']=True
        # A candidate may improve rho even if a linearized objective drops.
        global_best=float(json.loads(Path('certificates/current.json').read_text())['claimed_rate_lower'])
        best_rate=max(best_rate,global_best)
        if rate>best_rate+1e-14:
            masks=sorted(c|(a<<8)|(b<<18) for i in ids for c,u,v in [boxes[i]] for a in types[u] for b in types[v])
            cert={'n':28,'ports':[0,1],'masks':masks,'credit':base['credit'],'status':'candidate and unrefereed'}
            proposal=Path('certificates/proposal.json');proposal.write_text(json.dumps(cert,separators=(',',':'))+'\n')
            output=Path('logs/proposal_check.json')
            check=subprocess.run([os.sys.executable,'checker.py',str(proposal),'--output',str(output)],capture_output=True,text=True)
            result=json.loads(output.read_text())
            if check.returncode or result['bar_comparison']!='above':
                rec['certification_failure']=result;stats['rounds'].append(rec)
                Path('logs/coupled_progress.json').write_text(json.dumps(stats,indent=2)+'\n')
                raise RuntimeError('proposed improvement rejected; stop and revert search before investigation')
            cert['claimed_rate_lower']=result['rate_interval_decimal'][0]
            name='best_'+cert['claimed_rate_lower'][:24]+'.json'
            Path('certificates',name).write_text(json.dumps(cert,separators=(',',':'))+'\n')
            best_rate=rate;best_ids=ids[:];last_best=time.monotonic()
            Path('certificates/current.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
            Path('certificates/current.masks').write_text(''.join(str(x)+'\n' for x in masks))
            Path('logs/last_improvement_utc.txt').write_text(clock()+'\n')
            hit={'utc':clock(),'certificate':'certificates/'+name,'verification':result}
            stats['improvements'].append(hit);print(json.dumps({'CERTIFIED_BEST':hit}),flush=True)
        # Enumerate another near-optimal template configuration without repeating.
        model.add(sum(z[i] for i in ids)<=len(ids)-1)
    model.clear_hints()
    # Feasible baseline is retained as a hint until it is deliberately excluded.
    for i in range(len(z)):model.add_hint(z[i],int(i in set(best_ids)))
    stats['rounds'].append(rec);print(json.dumps(rec),flush=True)
    Path('logs/coupled_clauses.json').write_text(json.dumps(sorted(known),separators=(',',':'))+'\n')
    with open('STATUS.md','a') as f:f.write('\n'+clock()+': Coupled CP-SAT round '+str(iteration)+', core deletion radius '+str(radius)+', '+str(len(known))+' exact sunflower clauses; certified improvements '+str(len(stats['improvements']))+'.\n')
    Path('logs/coupled_progress.json').write_text(json.dumps(stats,indent=2)+'\n')
    # The job requires at least three hours without an improving move.
    if time.monotonic()-last_best>=10800:break
stats.update(end_utc=clock(),wall_seconds=time.monotonic()-start,cpu_seconds=time.process_time(),peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,stop_reason='allocated search time reached',sunflower_clauses=len(known))
Path('logs/coupled_progress.json').write_text(json.dumps(stats,indent=2)+'\n');print(json.dumps({'finished':True,'seconds':stats['wall_seconds'],'improvements':len(stats['improvements'])}),flush=True)

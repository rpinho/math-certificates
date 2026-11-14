"""Exact small-exchange pool SAT model, with literal sunflower separation."""
import argparse,collections,itertools,json,math,os,subprocess,time
from pathlib import Path
from ortools.sat.python import cp_model
ap=argparse.ArgumentParser();ap.add_argument('--radius',type=int,default=6);ap.add_argument('--seconds',type=float,default=300);ap.add_argument('--all-extras',action='store_true');ap.add_argument('--threads',type=int,default=1);ap.add_argument('--target',type=int,default=33);args=ap.parse_args()
start=time.monotonic();regions=json.loads(Path(f'logs/exchange_combined_r{args.radius}.json').read_text())['promising'];baseline=json.loads(Path('certificates/baseline.json').read_text());old=baseline['masks'];results=[]
if args.all_extras:
    fixed=set(map(int,Path('certificates/fixed_core.masks').read_text().split()))
    regions=[{'remove':sorted(set(old)-fixed),'candidate_pool':list(map(int,Path('logs/free_extras.masks').read_text().split()))}]
for ri,region in enumerate(regions):
    removed=set(region['remove']);pool=region['candidate_pool'];kept=[x for x in old if x not in removed]
    slices=collections.defaultdict(lambda:collections.defaultdict(list))
    for x in kept:slices[x&255][(x>>8)&1023].append(x>>18)
    boxes=[]
    for c,uv in slices.items():
        groups=collections.defaultdict(list)
        for u,v in uv.items():groups[tuple(sorted(v))].append(u)
        for v,u in groups.items():boxes.append((c,u,v))
    def partner(a,b):
        i=a&b;f=a^b
        ic=i&255;fc=f&255;iu=(i>>8)&1023;fu=(f>>8)&1023;iv=i>>18;fv=f>>18
        for c,us,vs in boxes:
            if c&ic!=ic or c&fc:continue
            u=next((u for u in us if u&iu==iu and not u&fu),None)
            if u is None:continue
            v=next((v for v in vs if v&iv==iv and not v&fv),None)
            if v is not None:return c|(u<<8)|(v<<18)
        return None
    model=cp_model.CpModel();z=[model.new_bool_var(str(i)) for i in range(len(pool))];pairs=0;triples=0
    for i,a in enumerate(pool):
        for j in range(i+1,len(pool)):
            b=pool[j]
            if a&b==a or a&b==b or partner(a,b) is not None:model.add(z[i]+z[j]<=1);pairs+=1
    for i,a in enumerate(pool):
        for j in range(i+1,len(pool)):
            b=pool[j];ab=a&b;xx=a^b
            for k in range(j+1,len(pool)):
                c=pool[k]
                if c&ab==ab and not c&xx:model.add(z[i]+z[j]+z[k]<=2);triples+=1
    incumbent=set(json.loads(Path('certificates/current.json').read_text())['masks'])
    for i,a in enumerate(pool):model.add_hint(z[i],int(a in incumbent))
    model.add(sum(z)>=max(args.target,len(incumbent)-len(kept)))
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=args.threads;solver.parameters.max_time_in_seconds=args.seconds
    solver.parameters.random_seed=49
    class SaveBest(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__();self.best=len(json.loads(Path('certificates/current.json').read_text())['masks'])
        def on_solution_callback(self):
            chosen=[pool[i] for i in range(len(pool)) if self.value(z[i])]
            if len(kept)+len(chosen)<=self.best:return
            cert=dict(baseline);cert['masks']=sorted(kept+chosen);cert.pop('claimed_rate_lower',None);cert['status']='candidate and unrefereed'
            proposal=Path('certificates/free_extras_proposal.json');proposal.write_text(json.dumps(cert,separators=(',',':'))+'\n')
            output=Path('logs/free_extras_proposal_check.json');check=subprocess.run([os.sys.executable,'checker.py',str(proposal),'--output',str(output)],capture_output=True,text=True)
            result=json.loads(output.read_text())
            if check.returncode or result['bar_comparison']!='above':
                self.stop_search();raise RuntimeError('rejected exact extra-pool proposal')
            cert['claimed_rate_lower']=result['rate_interval_decimal'][0];name='best_'+cert['claimed_rate_lower'][:24]+'.json'
            Path('certificates',name).write_text(json.dumps(cert,separators=(',',':'))+'\n')
            Path('certificates/current.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
            Path('certificates/current.masks').write_text(''.join(str(x)+'\n' for x in cert['masks']))
            Path('logs/'+name+'.check.json').write_text(json.dumps(result,indent=2)+'\n')
            self.best=len(cert['masks'])
            import datetime
            stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
            with open('STATUS.md','a') as f:f.write('\n'+stamp+': CERTIFIED BEST '+name+', '+str(self.best)+' members; count '+str(self.best-len(kept))+' in the free-extra pool.\n')
            Path('logs/last_improvement_utc.txt').write_text(stamp+'\n')
            print('CERTIFIED_BEST '+name+' members '+str(self.best),flush=True)
    callback=SaveBest()
    status=solver.solve(model,callback);chosen=[pool[i] for i in range(len(pool)) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) and solver.value(z[i])]
    rec={'target_at_least':args.target,'region':ri,'removed':sorted(removed),'pool_size':len(pool),'pair_conflicts':pairs,'triple_conflicts':triples,'status':solver.status_name(status),'max_count_found':len(chosen),'upper_bound':solver.best_objective_bound,'chosen':chosen,'solve_seconds':solver.wall_time}
    current=json.loads(Path('certificates/current.json').read_text()) if Path('certificates/current.json').exists() else baseline
    if len(kept)+len(chosen)>len(current['masks']):
        cert=dict(baseline);cert['masks']=sorted(kept+chosen);cert.pop('claimed_rate_lower',None);cert['status']='candidate and unrefereed'
        proposal=Path('certificates/pool_proposal.json');proposal.write_text(json.dumps(cert,separators=(',',':'))+'\n')
        output=Path('logs/pool_proposal_check.json');check=subprocess.run([os.sys.executable,'checker.py',str(proposal),'--output',str(output)],capture_output=True,text=True)
        result=json.loads(output.read_text());assert check.returncode==0 and result['bar_comparison']=='above',result
        cert['claimed_rate_lower']=result['rate_interval_decimal'][0]
        name='best_'+cert['claimed_rate_lower'][:24]+'.json';Path('certificates',name).write_text(json.dumps(cert,separators=(',',':'))+'\n');rec['certified_improvement']=str(Path('certificates',name));print('CERTIFIED_BEST',name,flush=True)
    results.append(rec);print(json.dumps(rec),flush=True)
Path('logs/free_extras_threshold'+str(args.target)+'_solution.json' if args.all_extras else f'logs/pool_search_r{args.radius}.json').write_text(json.dumps({'regions':results,'seconds':time.monotonic()-start},indent=2)+'\n')

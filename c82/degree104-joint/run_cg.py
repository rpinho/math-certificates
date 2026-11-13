"""Alternate new-dual LLL numerator and degree-104 CVP denominator columns."""
import argparse,hashlib,json,os,re,resource,subprocess,sys,time
from fractions import Fraction
from pathlib import Path
from numerics import register,write_json
from checkpoint import checkpoint
from supervise import run,snapshot,CAP

def verify(prefix):
    cert=prefix+'-certificate.json';sha=hashlib.sha256(Path(cert).read_bytes()).hexdigest()
    source=''.join("EXPECTED = '"+sha+"'\n" if l.startswith('EXPECTED = ') else l for l in Path('verify_public.py').read_text().splitlines(True))
    verifier=prefix+'-verifier.py';Path(verifier).write_text(source)
    run([verifier,'--certificate',cert,'--target','0.2519744488','--precision','256','--tol','1e-13','--out',prefix+'-replay.json'],prefix+'-verify.log')
    checkpoint(cert,verifier,prefix+'-replay.json')

def compact(state,out):
    s=json.loads(Path(state).read_text());keep=[i for i,w in enumerate(s['w']) if w>1e-13]
    s['numerator']=[s['numerator'][i] for i in keep];s['w']=[s['w'][i] for i in keep]
    write_json(out,s);return out

def batch(jobs):
    procs=[];started=time.monotonic();before=resource.getrusage(resource.RUSAGE_CHILDREN)
    for args,log in jobs:
        out=open(log,'w');timing=open(log+'.time','w')
        p=subprocess.Popen(['/usr/bin/time','-l',sys.executable,*args],stdout=out,stderr=timing)
        with open('evidence/pids.jsonl','a') as f:f.write(json.dumps({'pid':p.pid,'args':args,'kind':'batch_time'})+'\n')
        procs.append((p,out,timing))
    peak=0
    while any(p.poll() is None for p,_,_ in procs):
        rss=snapshot();total=sum(rss.values());peak=max(peak,total)
        if total>CAP-150_000_000:
            for pid in sorted(rss,reverse=True):
                if pid!=os.getpid():
                    try:os.kill(pid,15)
                    except ProcessLookupError:pass
            raise RuntimeError('batch memory stop: '+str(total))
        time.sleep(.2)
    codes=[]
    for p,out,timing in procs:codes.append(p.wait());out.close();timing.close()
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    rec={'kind':'batch','jobs':[args for args,log in jobs],'exit_codes':codes,'cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,'wall_seconds':time.monotonic()-started,'sampled_aggregate_peak_bytes':peak}
    with open('evidence/compute.jsonl','a') as f:f.write(json.dumps(rec)+'\n')
    print(json.dumps(rec),flush=True)
    if any(codes):raise RuntimeError('search failed: '+str(codes))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--state',default='rounds/warm.json');ap.add_argument('--dual',default='rounds/warm-dual.npz');ap.add_argument('--first',type=int,default=52);ap.add_argument('--empty',type=int,default=0);ap.add_argument('--seconds',type=int,default=240);ap.add_argument('--workers',type=int,default=4);ap.add_argument('--den-workers',type=int,default=2);ap.add_argument('--rounds',type=int,default=100);ap.add_argument('--measure-first',action='store_true');a=ap.parse_args();register('alternating_cg')
    state=a.state;dual=a.dual;empty=a.empty;history=json.loads(Path('rounds/progress.json').read_text())['history'] if Path('rounds/progress.json').exists() and a.first>53 else [];start=json.loads(Path('evidence/start.json').read_text())['start_epoch']
    if a.first==1:verify(state.removesuffix('.json'))
    state=compact(state,f'rounds/restricted-{a.first}.json')
    for k in range(a.first,a.first+a.rounds):
        if time.time()-start>9.5*3600:break
        old=json.loads(Path(state).read_text())['lp'];counts={}
        old_cert=Fraction(json.loads(Path('RESULT.json').read_text())['exact_upper'])
        for kind,program in [('num','lll_numerators.py'),('den','cvp_search.py')]:
            with open('STATUS.md','a') as f:f.write('\n'+time.strftime('%Y-%m-%d %H:%M:%S')+f' Round {k}: {kind} new-column search on {state}, dual {dual}.\n')
            jobs=[];paths=[];workers=1 if a.measure_first and k==a.first else (a.workers if kind=='num' else a.den_workers)
            for worker in range(workers):
                out=f'rounds/{kind}-search-{k}-{worker}.json';paths.append(out)
                args=[program,'--state',state,'--dual',dual,'--seconds',str(a.seconds),'--seed',str(811104+k*101+worker*7919+(30000 if kind=='den' else 0)),'--out',out]
                if kind=='den':args+=['--bank','prior_sources/union-factor-bank.json']
                jobs.append((args,f'logs/{kind}-search-{k}-{worker}.log'))
            batch(jobs)
            if workers==1:
                peak_rss=int(re.search(r'(\d+)\s+maximum resident set size',Path(jobs[0][1]+'.time').read_text()).group(1))
                planned=a.workers if kind=='num' else a.den_workers
                with open('STATUS.md','a') as f:f.write(f'\nMeasured solo {kind} worker: maximum resident set size {peak_rss} bytes; times planned {planned} workers = {peak_rss*planned} bytes. Aggregate RSS in evidence/compute.jsonl.\n')
            negative=sum(len(json.loads(Path(p).read_text())['negative_candidates']) for p in paths);counts[kind]=negative
            if negative:
                prefix=f'rounds/{kind}-{k}'
                run(['merge_numerators.py' if kind=='num' else 'add_columns.py','--state',state,'--prefix',prefix,*paths],f'logs/{kind}-merge-{k}.log')
                state=prefix+'.json';dual=prefix+'-dual.npz';verify(prefix)
                state=compact(state,f'rounds/restricted-{kind}-{k}.json')
            # Price every archive numerator on each changed dual, preserving union coverage.
            if negative:
                for j in range(6):
                    prefix=f'rounds/archive-{kind}-{k}-{j}'
                    run(['numerator_search.py','--state',state,'--dual',dual,'--prefix',prefix],f'logs/archive-{kind}-{k}-{j}.log')
                    if not json.loads(Path(prefix+'-screen.json').read_text())['added']:break
                    state=prefix+'.json';dual=prefix+'-dual.npz';verify(prefix)
                    state=compact(state,f'rounds/restricted-archive-{kind}-{k}-{j}.json')
        new=json.loads(Path(state).read_text())['lp'];gain=old-new
        new_cert=Fraction(json.loads(Path('RESULT.json').read_text())['exact_upper'])
        empty=empty+1 if new_cert>=old_cert else 0
        rec={'round':k,'old_lp':old,'new_lp':new,'gain':gain,'certified_gain':str(old_cert-new_cert),'negative_candidates':counts,'empty_rounds':empty,'state':state,'dual':dual}
        history.append(rec);write_json('rounds/progress.json',{'history':history,'state':state,'dual':dual})
        with open('STATUS.md','a') as f:f.write('\n'+json.dumps(rec)+'\n')
        print(json.dumps(rec),flush=True)
        if empty>=3:break
    write_json('rounds/finished.json',{'history':history,'state':state,'dual':dual,'stop':'three consecutive no-gain rounds' if empty>=3 else 'wall or batch limit'})

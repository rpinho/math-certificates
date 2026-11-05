"""Run the round-5 standard column-generation loop, checkpointing accepted bounds."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
from checkpoint import checkpoint
from numerics import register, write_json

def run(args,log):
    before=resource.getrusage(resource.RUSAGE_CHILDREN)
    begun=time.monotonic()
    with open(log,'w') as f:
        p=subprocess.Popen([sys.executable,*args],stdout=f,stderr=subprocess.STDOUT)
        with open('evidence/pids.jsonl','a') as out:out.write(json.dumps({'pid':p.pid,'kind':args[0],'log':log})+'\n')
        code=p.wait()
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    with open('evidence/compute.jsonl','a') as out:out.write(json.dumps({'args':args,'pid':p.pid,'exit_code':code,'wall_seconds':time.monotonic()-begun,'cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime})+'\n')
    if code:
        with open('STATUS.md','a') as f:f.write('\nFailure in '+str(args)+', exit '+str(code)+', log '+log+'. Retained previous certified certificate and previous master state; stopping for investigation.\n')
        raise RuntimeError(str(args)+' failed; previous state retained')

def verify(prefix):
    cert=prefix+'-certificate.json';source=Path('verify_public.py').read_text()
    sha=hashlib.sha256(Path(cert).read_bytes()).hexdigest()
    source=''.join("EXPECTED = '"+sha+"'\n" if line.startswith('EXPECTED = ') else line for line in source.splitlines(True))
    verifier=prefix+'-verifier.py';Path(verifier).write_text(source)
    run([verifier,'--certificate',cert,'--target','0.2520591386','--precision','256','--tol','1e-13','--out',prefix+'-replay.json'],prefix+'-verify.log')
    checkpoint(cert,verifier,prefix+'-replay.json')

def compact(state,prefix):
    # Standard restricted master: zero numerator columns remain available to pricing.
    s=json.loads(Path(state).read_text())
    keep=[i for i,v in enumerate(s['w']) if v>1e-13]
    s['numerator']=[s['numerator'][i] for i in keep];s['w']=[s['w'][i] for i in keep]
    write_json(prefix,s)
    return prefix

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--state',default='rounds/union.json');ap.add_argument('--dual',default='rounds/union-dual.npz')
    ap.add_argument('--first',type=int,default=0);ap.add_argument('--rounds',type=int,default=12);ap.add_argument('--seconds',type=int,default=240);ap.add_argument('--workers',type=int,default=2);ap.add_argument('--rotate-warm',action='store_true');ap.add_argument('--empty-start',type=int,default=0)
    a=ap.parse_args();register('column_generation_loop');begun=time.monotonic();state=a.state;dual=a.dual;empty=a.empty_start;history=[]
    if a.first==0:verify(state.removesuffix('.json'))
    state=compact(state,'rounds/restricted-'+str(a.first)+'.json')
    for k in range(a.first,a.first+a.rounds):
        if time.time()-json.loads(Path('evidence/start.json').read_text())['start_epoch']>7*3600:break
        searches=[];jobs=[]
        with open('STATUS.md','a') as f:f.write('\n'+time.strftime('%Y-%m-%d %H:%M:%S')+f' CVP round {k}, master {state}; {a.workers} workers, standard defaults, {a.seconds} seconds each.\n')
        before=resource.getrusage(resource.RUSAGE_CHILDREN)
        for worker in range(a.workers):
            out=f'rounds/search-{k}-{worker}.json';searches.append(out)
            log=open(f'logs/search-{k}-{worker}.log','w')
            warm_state=state
            if a.rotate_warm:
                warm=json.loads(Path(state).read_text())
                positive=sorted([i for i,v in enumerate(warm['mu']) if v>1e-13],key=lambda i:-warm['mu'][i])
                inactive=[i for i,v in enumerate(warm['mu']) if v<=1e-13]
                offset=(6*(k-a.first)+3*worker)%len(positive)
                order=positive[offset:]+positive[:offset]+inactive
                warm['denominator']=[warm['denominator'][i] for i in order]
                warm['mu']=[warm['mu'][i] for i in order]
                warm_state=f'rounds/warm-{k}-{worker}.json'
                write_json(warm_state,warm)
            args=[sys.executable,'cvp_search.py','--state',warm_state,'--dual',dual,'--bank','prior_sources/union-factor-bank.json','--seconds',str(a.seconds),'--seed',str(6104+k*101+worker*7919),'--out',out]
            p=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT)
            with open('evidence/pids.jsonl','a') as f:f.write(json.dumps({'pid':p.pid,'kind':'cvp','round':k,'worker':worker})+'\n')
            jobs.append((p,log))
        codes=[]
        for p,log in jobs:codes.append(p.wait());log.close()
        after=resource.getrusage(resource.RUSAGE_CHILDREN)
        with open('evidence/compute.jsonl','a') as f:f.write(json.dumps({'kind':'cvp_pair','round':k,'cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,'exit_codes':codes})+'\n')
        if any(codes):
            with open('STATUS.md','a') as f:f.write('\nCVP failure '+str(codes)+'. Previous master and certificate retained; stop for investigation.\n')
            raise RuntimeError(str(codes))
        negative=sum(len(json.loads(Path(path).read_text())['negative_candidates']) for path in searches)
        old=json.loads(Path(state).read_text())['lp']
        if negative:
            prefix=f'rounds/den-{k}'
            run(['add_columns.py','--state',state,'--prefix',prefix,*searches],f'logs/den-{k}.log')
            state=prefix+'.json';dual=prefix+'-dual.npz';verify(prefix)
        # All public bank numerators are screened against each current dual.
        for j in range(6):
            prefix=f'rounds/num-{k}-{j}'
            run(['numerator_search.py','--state',state,'--dual',dual,'--prefix',prefix],f'logs/num-{k}-{j}.log')
            screen=json.loads(Path(prefix+'-screen.json').read_text())
            if not screen['added']:break
            state=prefix+'.json';dual=prefix+'-dual.npz';verify(prefix)
        new=json.loads(Path(state).read_text())['lp'];empty=empty+1 if negative==0 and old-new<1e-10 else 0
        record={'round':k,'old_lp':old,'new_lp':new,'negative_candidates':negative,'gain':old-new,'empty_rounds':empty,'state':state,'dual':dual}
        history.append(record);write_json('rounds/progress.json',{'history':history,'state':state,'dual':dual,'elapsed':time.monotonic()-begun})
        with open('STATUS.md','a') as f:f.write('\n'+json.dumps(record)+'\n')
        print(json.dumps(record),flush=True)
        state=compact(state,f'rounds/restricted-{k+1}.json')
        if empty>=3:break
    write_json('rounds/finished.json',{'history':history,'state':state,'dual':dual,'elapsed':time.monotonic()-begun,'stop':'three no-gain rounds' if empty>=3 else 'batch or wall limit'})

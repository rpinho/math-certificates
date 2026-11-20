"""Stop on five successive certified gains under 1e-9 or the wall budget."""
import sys,time
from pathlib import Path
from fractions import Fraction
from result import read,put,save,sha,status,decimal
from worker import run,LIMIT
from search import extend
def current():return Fraction(read('RESULT.json')['exact_upper'])
def run_alternations():
    union=read('rounds/union-final.json')['state']
    progress=Path('rounds/alternations.json')
    history=read(progress) if progress.exists() else []
    state=history[-1]['state'] if history else union
    streak=history[-1]['small_gain_streak'] if history else 0
    rival=read('evidence/v6.json')['bound']['upper']
    upper=int(rival['mantissa'])*Fraction(2)**rival['exponent']
    den_arm=upper-current()>Fraction('1e-10') if not history else history[0]['den_arm']
    probe=True if not history else history[-1]['probe_next']
    above_seconds=sum(row['above_seconds'] for row in history)
    while streak<5 and time.time()<LIMIT-900:
        n=len(history)+1;before=current();counts={};extra_time=0
        status(f'Alternation {n} on {state}. Certified incumbent {decimal(before)}.')
        # Two main-band trials and a high-degree probe use separate deterministic streams.
        files=[];jobs=[]
        for j,(low,high) in enumerate([(24,48),(24,48),(48,64)]):
            label=f'lll-{n}-{j}';path=f'rounds/{label}.json';files.append(path)
            args=['lll_numerators.py','--state',state+'.json','--dual',state+'-dual.npz','--seed',120000+n*100+j,'--low',low,'--high',high,'--out',path]
            jobs.append((label,args))
        label=f'orbit-{n}';path=f'rounds/{label}.json';files.append(path)
        jobs.append((label,['orbit.py',state+'.json',state+'-dual.npz',path]))
        run(jobs)
        counts['numerator']=sum(len(read(f)['negative_candidates']) for f in files)
        state=extend(state,f'rounds/new-num-{n}','numerator',files)
        if den_arm:
            files=[];jobs=[]
            for deg in ([104,116] if probe and above_seconds<5100 else [104]):
                label=f'cvp-{n}-{deg}';path=f'rounds/{label}.json';files.append(path)
                args=['cvp_search.py','--state',state+'.json','--dual',state+'-dual.npz','--bank','inputs/full-bank.json','--seed',120000+n*100+deg,'--degree',deg,'--seconds',240,'--out',path]
                jobs.append((label,args))
            run(jobs)
            counts['denominator']=sum(len(read(f)['negative_candidates']) for f in files)
            if len(files)==2:
                probe_out=read(files[1]);extra_time=probe_out['elapsed'];above_seconds+=extra_time
                probe=bool(probe_out['negative_candidates']) and above_seconds<5100
            state=extend(state,f'rounds/new-den-{n}','denominator',files)
        after=current();gain=before-after;streak=streak+1 if gain<Fraction('1e-9') else 0
        history.append(dict(round=n,state=state,exact_gain=str(gain),gain=float(gain),upper=decimal(after),archive=read('RESULT.json')['archive'],small_gain_streak=streak,counts=counts,den_arm=den_arm,probe_next=probe,above_seconds=extra_time))
        put(progress,history);status(f'Alternation {n} certified gain {float(gain):.5g}, streak {streak}, archived endpoint {decimal(after)}.')
    put('rounds/stopped.json',dict(reason='five consecutive alternations gaining less than 1e-9' if streak>=5 else 'wall budget',state=state,streak=streak))
if __name__=='__main__':run_alternations()

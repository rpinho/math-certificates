"""Round 12 joint master and full-bank column generation, followed by alternations."""
from pathlib import Path
from fractions import Fraction
from result import read,put,sha,save,endpoint,status
from worker import run
import time
def certify(prefix):
    cert=prefix+'-certificate.json';replay=prefix+'-replay.json';label=Path(prefix).name
    run([(label+'-verify',['verify.py','--sha',sha(cert),'--certificate',cert,'--target','0.2519695579','--tol','1e-13','--out',replay])])
    hi=endpoint(read(replay)['bound']['upper'])
    if label.startswith('union'):
        r=read('evidence/v6.json')['bound'];high=endpoint(r['upper']);width=high-endpoint(r['lower'])
        if hi>high+width:raise RuntimeError('union above incumbent plus verifier width')
    save(cert,replay,label)
    return hi

def extend(state,prefix,kind,files):
    label=Path(prefix).name
    run([(label,['solve_added.py',state+'.json',prefix,kind,*files])])
    if not read(prefix+'-added.json'):return state
    certify(prefix)
    return prefix

def union():
    state='rounds/union-master';certify(state)
    for i in range(100):
        prefix=f'rounds/union-{i}'
        files=[f'{prefix}-screen-{p}.json' for p in range(4)]
        run([(Path(path).stem,['price_bank.py',state+'.json',state+'-dual.npz',path,p]) for p,path in enumerate(files)])
        new=extend(state,prefix,'numerator',files)
        if new==state:
            put('rounds/union-final.json',dict(state=state,all_columns_priced=True,screens=files))
            status('Full-bank union pricing complete. Best certified endpoint '+read('RESULT.json')['interval'][1])
            return state
        state=new
    raise RuntimeError('full-bank pricing did not converge')
if __name__=='__main__':union()

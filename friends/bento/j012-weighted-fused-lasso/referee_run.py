import json, os, random, time, traceback
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from fractions import Fraction as F
from referee_primal import solve, analyze, encode


def challenge_cases():
    rng = random.Random(7312026)
    cases = {}
    for n in range(2,9):
        for mode in range(6):
            for trial in range(6):
                # Include flat hulls, curved hulls, collinearities, deep defects,
                # arbitrary weights, and data with many simultaneous events.
                if mode in (0,1):
                    w = [F(1) for i in range(1,n)]
                elif mode in (2,3):
                    w = [F(i*(n-i)) for i in range(1,n)]
                elif mode == 4:
                    w = [F(rng.randint(1,50),rng.randint(1,10)) for i in range(1,n)]
                else:
                    w = [F(i*i) for i in range(1,n)]
                if mode in (1,2,3):
                    for i in rng.sample(range(n-1),min(n-1,1+trial%3)):
                        w[i] *= F(1,rng.choice((2,10,1000)))
                y = [rng.randint(-40,40) for _ in range(n)]
                if trial == 0:
                    y = [0]*n
                elif trial == 1:
                    y = [(-1)**i for i in range(n)]
                elif trial == 2:
                    y = [int(i>=n//2) for i in range(n)]
                cases[f'new_n{n}_mode{mode}_trial{trial}'] = dict(y=list(map(str,y)),alpha=list(map(str,w)))
    # Exhaustive small rational integer grid: tied data are intentional.
    from itertools import product
    for w in product((1,2,3),repeat=2):
        for y in product((-1,0,1),repeat=3):
            cases[f'exhaustive_n3_w{w}_y{y}'] = dict(y=list(map(str,y)),alpha=list(map(str,w)))
    return cases


def one(item):
    name, case = item
    start = time.time()
    try:
        path = solve(case['y'],case['alpha'])
        diag = analyze(case['y'],case['alpha'],path)
        path = encode(path)
        if 'pieces' in case:
            assert path == case['pieces'], 'independent path disagrees with claimant'
        out = dict(y=case['y'],alpha=case['alpha'],pieces=path,diagnostics=diag,
                   matched_claimant=('pieces' in case),seconds=time.time()-start)
        return name,out,None
    except Exception:
        return name,case,traceback.format_exc()


def main():
    cases = json.loads(Path('inputs.json').read_text())
    inputs = dict(cases)
    extra = challenge_cases()
    assert not (set(cases)&set(extra))
    cases.update(extra)
    Path('challenge_inputs.json').write_text(json.dumps(extra,indent=2))
    os.makedirs('results',exist_ok=True)
    summary = dict(total=len(cases),claimant=len(inputs),new=len(extra),passed=0,failed=0,records={})
    with ProcessPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(one,it) for it in cases.items()]
        for f in as_completed(futures):
            name,out,error = f.result()
            if error:
                summary['failed'] += 1
                out['error'] = error
                print('ERROR',name,error,flush=True)
            else:
                summary['passed'] += 1
            Path('results',name+'.json').write_text(json.dumps(out,indent=2))
            summary['records'][name] = out.get('diagnostics',dict(error=error))
            if (summary['passed']+summary['failed'])%20 == 0:
                print('PROGRESS',summary['passed'],summary['failed'],len(cases),flush=True)
                Path('summary.json').write_text(json.dumps(summary,indent=2))
    Path('summary.json').write_text(json.dumps(summary,indent=2))
    print('DONE',summary['passed'],summary['failed'],flush=True)


if __name__ == '__main__':
    main()

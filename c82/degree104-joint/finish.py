"""Build the report from the actual checkpoints and full coefficient matches."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import gzip,json,re,subprocess,tarfile,time
from result import read,put,sha,decimal,endpoint,status
from worker import START
BASE=Path('../c82r11')
def zipped(path):
    with gzip.open(path,'rt') as f:return json.load(f)
def provenance():
    sources=[]
    def add(label,data):
        sources.append((label,{k:{tuple(r['coeffs']):r['name'] for r in data[k]} for k in ('numerator','denominator')}))
    for i in (5,6,7):add('through round '+str(i),zipped(BASE/f'prior_sources/round{i}-certificate.json.gz'))
    add('pre-round-8 bank',zipped(BASE/'prior_sources/factor-bank.json.gz'))
    for i in (3,4,5):add('#280 v'+str(i),zipped(BASE/f'prior_sources/pr280-v{i}-certificate.json.gz'))
    with tarfile.open(BASE/'prior_sources/factor-banks.tar.xz') as t:
        for i in (8,9,10):
            records=json.load(t.extractfile(f'prior_sources/round{i}-bank.json'))
            for suffix in ('certificate','master'):
                more=zipped(BASE/f'prior_sources/round{i}-{suffix}.json.gz')
                for kind in ('denominator','numerator'):records[kind].extend(more[kind])
            add('round '+str(i)+' archive',records)
    add('round 11 bank',read('inputs/bank.json'))
    add('#280 v6',read('inputs/v6.json'))
    out={};summary={}
    for k,rows_in in ((k,read('certificate.json')[k]) for k in ('denominator','numerator')):
        rows=[];counts=Counter()
        for r in rows_in:
            c=tuple(r['coeffs']);matches={name:store[k][c] for name,store in sources if c in store[k]}
            ours=next((label for label in ['round 8 archive','round 9 archive','round 10 archive','round 11 bank'] if label in matches),None)
            if r['name'] in ['P1','P2','P3','P4','P6']:origin='Doche'
            elif any(k.startswith('#280 v') and k!='#280 v6' for k in matches):origin='earlier #280 / archive'
            elif any('through' in l or 'pre-round' in l for l in matches):origin='earlier archive'
            elif ours:origin=ours
            elif '#280 v6' in matches:origin='#280 v6'
            else:origin='round 12'
            counts[(origin, '#280 v6' in matches)]+=1
            rows.append(dict(**r,degree=len(c)-1,origin=origin,also_in_v6='#280 v6' in matches,exact_matches=matches))
        out[k]=rows;summary[k]=counts
    put('FACTOR_PROVENANCE.json',out)
    return summary
def inventory():
    tree=read('inputs/pinned-tree.json');assert not tree['truncated'] and tree['sha']=='e3bae2ea40c8b1f764a1ba08bcd21fe513b2c45d'
    blobs={r['sha'] for r in tree['tree'] if r['type']=='blob'}
    mine={str(p):subprocess.check_output(['git','hash-object','--no-filters',str(p)],text=True).strip() for p in sorted(Path('.').rglob('*.py'))}
    assert not blobs.intersection(mine.values())
    put('PYTHON_BLOBS.json',dict(pinned_commit=tree['sha'],remote_blobs=len(blobs),local_python=mine,matches=[]))
def encoding():
    lines=['# Equivalent encodings of numerator powers','']
    for path in sorted(Path('certificates').glob('best_*.json')):
        if path.name.endswith('-replay.json'):continue
        for r in read(path)['numerator']:
            q=Fraction(r['q_rational']);orig=r['q_rational'].split('/')
            if len(str(q.numerator)) in (15,16) or len(orig[0]) in (15,16):
                a=int(orig[0]);b=int(orig[1]) if len(orig)>1 else 1
                assert q==Fraction(2*a,2*b)
                lines.append(f"- {path.name}, {r['name']}, {a}/{b} = {2*a}/{2*b}.")
    Path('CERTIFICATE_ENCODING.md').write_text('\n'.join(lines)+'\n')
def compute():
    times={}
    for p in Path('logs').glob('*.log'):
        ms=re.findall(r'([\d.]+) real\s+([\d.]+) user\s+([\d.]+) sys',p.read_text())
        if ms:times[p.name]=sum(float(x) for x in ms[-1][1:])
    rss=max(r['peak_group_bytes'] for r in (json.loads(l) for l in Path('evidence/resources.jsonl').read_text().splitlines()))
    value=dict(timed_worker_core_hours=sum(times.values())/3600,worker_cpu_seconds=times,largest_sampled_worker_group_bytes=rss,elapsed_hours=(time.time()-START)/3600)
    put('COMPUTE.json',value);return value
def plot_curve(curve,elapsed):
    import csv,os
    os.environ['MPLCONFIGDIR']=str(Path('logs/mpl').resolve())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    times=[q['elapsed_hours']*60 for q in curve]
    gains=[float((Fraction('0.2519694883')-Fraction(q['exact_upper']))*10**9) for q in curve]
    with open('IMPROVEMENT_CURVE.csv','w',newline='') as f:
        w=csv.writer(f);w.writerow(['elapsed_minutes','checkpoint','certified_upper_outward','gain_to_printed_v6_times_1e9'])
        for t,q,g in zip(times,curve,gains):w.writerow([t,q['label'],q['interval'][1],g])
    fig,ax=plt.subplots(figsize=(7.3,3.5),layout='constrained')
    ax.step(times+[elapsed*60],gains+[gains[-1]],where='post',color='#245f81',linewidth=1.7)
    ax.scatter(times,gains,color='#245f81',s=18)
    ax.axhline(0,color='#888',linewidth=.7);ax.spines[['top','right']].set_visible(False)
    ax.set_xlabel('Elapsed minutes');ax.set_ylabel('(Printed v6 − upper endpoint) × 10⁹')
    ax.set_xlim(left=0);ax.grid(axis='y',alpha=.2)
    fig.savefig('IMPROVEMENT_CURVE.png',dpi=160);plt.close(fig)
def finish():
    best=read('RESULT.json');hi=Fraction(best['exact_upper']);r=read(best['replay'])
    assert r['certificate_sha256']==sha('certificate.json')==best['sha256']
    assert r['status']=='PASS' and hi==endpoint(r['bound']['upper'])<Fraction(best['stated'])<Fraction('0.2519694883')
    controls=read('evidence/rejection-controls.json');assert controls['certificate_sha256']==best['sha256'] and all(x['rejected'] for x in controls['cases'])
    counts=provenance();inventory();encoding();comp=compute()
    hist=read('rounds/alternations.json');stop=read('rounds/stopped.json');structure=read('evidence/structure.json')
    curve=[json.loads(l) for l in Path('IMPROVEMENT_CURVE.jsonl').read_text().splitlines()]
    plot_curve(curve,comp['elapsed_hours'])
    gaps={name:decimal(Fraction(x)-hi,22,False) for name,x in [('#280 v6 (0.2519694883)','0.2519694883'),('Round 11 (0.2519695579)','0.2519695579'),('#330 (0.2519696460)','0.2519696460')]}
    upper=best['interval'][1];union=read('rounds/union-final.json');ur=read(union['state']+'-replay.json');u=endpoint(ur['bound']['upper'])
    lines=[f"Shipped: candidate, unrefereed C82 < {best['stated']}.", '',
        f"Certified interval [{best['interval'][0]}, {upper}]. The exact upper endpoint is {hi}, strictly below {Fraction(best['stated'])}.",
        '', '| Printed comparator | Improvement, rounded down |','|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in gaps.items()]
    lines += ['',f"The full-bank union certified an upper endpoint of {decimal(u)}. Subsequent pricing gained {float(u-hi):.12g}. The final packet has {r['audit']['denominator_factors']} denominators and {r['audit']['numerator_factors']} numerators, with D = {r['audit']['D']}.",
        '', '## Replay and search', '',
        'Both exact inputs replayed with the separately written verifier (same agent, stdlib and python-flint). The rounded-up v6 endpoint was '+curve[0]['interval'][1]+', and the round-11 endpoint was '+decimal(endpoint(read('evidence/round11.json')['bound']['upper']))+'.',
        '', f"We copied and reused our round-11 joint LP, numerical helpers, LLL and CVP search, run wrapper, proof note and interval verifier. The pinned MIT v6 certificate supplied polynomial coefficients and exact initial weights. The common D represents both sets of normalized weights exactly. Exact modular coprimality checks covered {structure['nonzero_resultant_pairs']:,} imported numerator–denominator pairs. All denominators are coprime to X(1−X). The inherited numerator exceptions are P1=X and P2=X−1, present in both required exact packets. Doche’s reduction permits these zeros, and the interval verifier accounts for them.",
        '', 'The master used the inherited 524,288-point half-circle grid, HiGHS primal and dual tolerances of 1e-10, and full-bank reduced-cost pricing. Roots and logarithmic terms were recomputed from raw descending integer coefficients. The inherited round-11 dual was copied as reference. All search prices used freshly solved merged duals.',
        '', 'Our 22,212-factor bank contained 200 degrees below 24, 2,071 at 24–48, 15,019 at 49–64 and 4,922 above 64. The 16 v6 additions had degree counts 24×2, 26×2, 28×3, 30×1, 31×2, 33×2, 34×3, 42×1. Two already occurred in our bank by complete coefficient equality. [Degree histogram](evidence/degrees.json).',
        '', 'The LLL searches used degree bands 24–48 and 48–64 with active-factor and v6 seeds. Direct coefficient perturbations surrounded the v6 degree-42 factor. In the raw X variable, the six substitutions generated by X ↦ 1−X and X ↦ 1/X were priced as prospective columns. The certificate already enforces z ↦ 1−z through X=z(1−z). Each proposal still faced ordinary LP pricing and interval replay.',
        '', '## Alternations', '', '| Round | Negative numerator proposals | Negative denominator proposals | Certified gain | Small-gain streak |','|---:|---:|---:|---:|---:|']
    for row in hist:lines.append(f"| {row['round']} | {row['counts']['numerator']} | {row['counts'].get('denominator',0)} | {row['gain']:.5g} | {row['small_gain_streak']} |")
    lines += ['',f"Stopped after {len(hist)} alternations under the {stop['reason']} rule. The degree-116 CVP probe used {sum(row['above_seconds'] for row in hist)/60:.2f} minutes. Degree-104 CVP used the current merged dual in each denominator arm.",
        '',('Another round with the same settings is low priority. Five consecutive alternations fell below the specified marginal gain.' if stop['streak']>=5 else 'A continuation is worth considering if the final search gains justify the compute.'),'','## Column credit','','| Factor kind | Earliest matching bank or source | Also in v6 | Count |','|---|---|---|---:|']
    contribution=read('FACTOR_PROVENANCE.json')
    retained={tuple(q['coeffs']) for q in contribution['numerator'] if q['origin']=='round 12'}
    details=[]
    for path in sorted(Path('rounds').glob('lll-*-*.json')):
        search=read(path)
        for row in search['negative_candidates']:
            key=tuple(row['coeffs'])
            if key not in retained:continue
            ds=sorted({i['degree'] for i in search['iterations'] if i['trial']==row['trial']})
            details.append(f"{row['name']} (factor degree {len(key)-1}, lattice degree {ds}, run {path.stem}, trial {row['trial']})")
            retained.remove(key)
    if details:
        where=lines.index('## Alternations')
        lines[where:where]=['New LLL factors retained in the final packet include '+', '.join(details)+'.','']
    probe_rows=[read(p) for p in Path('rounds').glob('cvp-*-116.json')]
    if probe_rows:
        probe_min=min(q['best']['rc'] for q in probe_rows if q['best'] is not None)
        probe_count=sum(q['priced'] for q in probe_rows)
        where=lines.index('## Column credit')
        lines[where:where]=[f"The above-104 probe priced {probe_count} polynomial evaluations. Its best previously absent degree-116 denominator had reduced cost {probe_min:.9g}. "+('It produced no negative-reduced-cost denominator and was dropped after its first pass.' if not any(q['negative_candidates'] for q in probe_rows) else 'Negative proposals were passed to the joint solve.'),'']
    for k,c in counts.items():
        for (origin,match),n in sorted(c.items()):lines.append(f"| {k} | {origin} | {'yes' if match else 'no'} | {n} |")
    lines+=['','[Every column and its full coefficient matches](FACTOR_PROVENANCE.json). An earliest bank match establishes local presence. Shared factors retain both credits. Doche supplied the base factors, Patankar the v6 numerator work, and the six starting degree-104 denominators trace to our rounds 8–10.','', '## Certified improvement curve','','![Certified gain over time](IMPROVEMENT_CURVE.png)','','| Elapsed hours | Checkpoint | Certified upper endpoint (outward) |','|---:|---|---:|']
    for item in curve:lines.append(f"| {item['elapsed_hours']:.4f} | {item['label']} | {item['interval'][1]} |")
    lines+=['',f"Recorded compute was {comp['timed_worker_core_hours']:.4f} core-hours from user plus system CPU of timed workers over {comp['elapsed_hours']:.3f} wall hours. Peak sampled aggregate worker RSS was {comp['largest_sampled_worker_group_bytes']:,} bytes. Small controller and file-preparation costs are excluded from core-hours.",
        '', '## Reproduction','', 'From this directory, replay the final bytes and the three rejection controls with the shared python-flint environment.','', '~~~sh',f"./run_local.sh verify.py --certificate certificate.json --sha {best['sha256']} --precision 256 --tol 1e-13 --target {best['stated']} --out evidence/final-replay.json",'./run_local.sh controls.py','~~~','',
        'The source commit, URL, MIT license and SHA256 are retained in inputs. Only data and tree metadata were read. None of the rival code was executed. [Full search reproduction](REPRODUCE.md). Search entry points in order are worker.py (both replays), prepare.py, joint_lp.py --input inputs/union-master.json --prefix rounds/union-master, search.py and alternate.py. [Mathematical argument](PROOF.md) and [numerical enclosures](NUMERICS.md).',
        '', 'Changed bytes failed the pinned digest. After re-pinning, zero denominator multiplicity and a shared numerator–denominator factor failed their structural checks. Every local Python git blob was compared with the complete pinned tree. No match occurred. [Rejection results](evidence/rejection-controls.json) and [blob inventory](PYTHON_BLOBS.json).',
        '', 'The supplied [prior-art review](PRIOR_ART.md) records the official 82a table, #280 v6, #330, repository and paper searches on 20 November. This comparison uses the requested frozen numbers. [Pinned v6 source](https://github.com/vidigoat/optimization-records/tree/e3bae2ea40c8b1f764a1ba08bcd21fe513b2c45d/tao/certificates/c82/v6).']
    Path('REPORT.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':finish()

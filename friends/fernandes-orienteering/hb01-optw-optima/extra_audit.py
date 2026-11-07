from pathlib import Path
import json,subprocess,time,hashlib
import numpy as np
from math import isqrt
root=Path('/workspace/ref_hugo_HB01');cohort=json.load(open(root/'evidence/HB01/FROZEN_CLAIM_COHORT_RUN6.json'));cases=cohort['rows']
actual=[]
for f in (root/'public/data/benchmark').glob('t*.txt'):
    h=f.read_text().splitlines()[0].split()
    if len(h)==16 and h[0]=='20' and h[1]=='1':actual.append(f.stem)
assert sorted(actual)==sorted(r['instance'] for r in cohort['all33']) and len(actual)==33
res={};folder=root/'mutations';folder.mkdir(exist_ok=True)
for name,c in cases.items():
    raw=root/'public/data/benchmark'/(name+'.txt');lines=(root/'evidence/HB01'/c['ng_proof']).read_text().splitlines();n=int(lines[1].split()[0]);U=c['exact_optimum']
    text=[s.split() for s in raw.read_text().splitlines() if s.strip()]
    x=np.array([float(s[1]) for s in text[1:]]);y=np.array([float(s[2]) for s in text[1:]])
    # Match released nested scalar NumPy calculations, not a vectorized rewrite.
    dist=np.zeros((n,n));difference=[]
    from decimal import Decimal
    cents=[(int(Decimal(s[1])*100),int(Decimal(s[2])*100)) for s in text[1:]]
    for i in range(n):
        for j in range(i):
            dist[i,j]=np.floor(100*(np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)))/100
            dist[j,i]=dist[i,j]
            exact=isqrt((cents[i][0]-cents[j][0])**2+(cents[i][1]-cents[j][1])**2)
            if int(np.rint(dist[i,j]*100))!=exact:difference.append([i,j,exact,int(np.rint(dist[i,j]*100))])
    audit=json.load(open(root/'audit.json'))['cases'][name]
    assert difference==audit['float64_edge_differences'],(name,'NumPy scalar rounding differs from first audit')
    # NumPy float32 scalar replay gives an independent check of the struct simulation.
    day=int(text[0][2]);openings=np.array([float(s[5 if i==0 else 6+2*day]) for i,s in enumerate(text[1:])],dtype=np.float32)
    closings=np.array([float(s[6 if i==0 else 7+2*day]) for i,s in enumerate(text[1:])],dtype=np.float32)
    durations=np.array([float(s[3]) for s in text[1:]],dtype=np.float32);df=dist.astype(np.float32);t=openings[0]
    tour=c['primary_primal']['route'];slack=1e9
    for i,j in zip(tour,tour[1:]):
        a=t+df[i,j];wait=np.maximum(np.float32(0),openings[j]-a);st=a+wait;t=st+durations[j]
        assert st<=closings[j] and t+df[j,0]<=closings[0]
        slack=min(slack,float(closings[j]-st),float(closings[0]-(t+df[j,0])))
    assert float(t)==audit['operational_witness']['finish']
    # Valid zero-score primal + false upper, keeping all original labels.
    false=lines.copy();false[0]='NGBOUND2';false[1]=f'{n} 0 {U-1}';false[-1]='2 0 0'
    fp=folder/(name+'_false.proof');fp.write_text('\n'.join(false)+'\n')
    r=subprocess.run([str(root/'referee'),'cover',str(raw),str(fp)],capture_output=True,text=True)
    assert r.returncode!=0,(name,'false upper accepted')
    # Removing the entire cover must not let a trivial root bound prove U.
    blank=lines[:n+2]+['0','2 0 0'];blank[0]='NGBOUND2';blank[1]=f'{n} 0 {U}'
    bp=folder/(name+'_blank.proof');bp.write_text('\n'.join(blank)+'\n')
    b=subprocess.run([str(root/'referee'),'cover',str(raw),str(bp)],capture_output=True,text=True)
    assert b.returncode!=0,(name,'trivial root control closes')
    # Route-only greedy insertion, 24 fixed scoring variants, no proof data.
    g=subprocess.run([str(root/'greedy'),str(raw)],capture_output=True,text=True,check=True)
    res[name]=dict(false_upper_rejected=r.stderr.strip(),blank_cover_rejected=b.stderr.strip(),greedy=json.loads(g.stdout),exact=U,numpy_float64_edge_differences=difference,numpy_float32_finish=float(t),numpy_float32_slack=slack)
    print(name,res[name]['greedy']['score'],'/',U,flush=True)
(root/'extra_audit.json').write_text(json.dumps(dict(official_single_day_cases=actual,rows=res),indent=2))

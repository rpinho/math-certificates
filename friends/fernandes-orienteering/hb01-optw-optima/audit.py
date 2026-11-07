"""Independent raw-data, rational witness, and primary-paper audit; pod only."""
from pathlib import Path
from fractions import Fraction as Q
from math import isqrt, sqrt, floor
import hashlib,json,sys,struct,re
root=Path('/workspace/ref_hugo_HB01');sys.path.insert(0,str(root/'deps'))
def read(p):
    lines=[s.split() for s in p.read_text().splitlines() if s.strip()]
    h=lines[0]; assert len(h)==16 and h[0]=='20' and h[1]=='1'
    day=int(h[2]);n=int(h[3])+1;assert len(lines)==n+1
    v=[]
    for i,r in enumerate(lines[1:]):
        assert len(r)==(7 if i==0 else 21) and int(r[0])==i
        v.append(dict(x=Q(r[1]),y=Q(r[2]),s=Q(r[3]),p=int(r[4]),o=Q(r[5 if i==0 else 6+2*day]),c=Q(r[6 if i==0 else 7+2*day])))
    return v
def sq(v,i,j):return (v[i]['x']-v[j]['x'])**2+(v[i]['y']-v[j]['y'])**2
def floordist(v,i,j):
    q=sq(v,i,j)*10000
    return Q(isqrt(q.numerator//q.denominator),100)
def enclose(v,i,j):
    q=sq(v,i,j);D=10**14;lo=isqrt(q.numerator*D**2//q.denominator)
    return Q(lo,D),Q(lo if lo**2*q.denominator==q.numerator*D**2 else lo+1,D)
def route(v,r,kind='floor'):
    assert r[0]==r[-1]==0 and 0 not in r[1:-1] and len(set(r[1:-1]))==len(r)-2
    lo=hi=v[0]['o']; score=0;slack=v[0]['c']-hi;maskslack=slack;finishslack=slack
    for i,j in zip(r,r[1:]):
        dl,dh=(floordist(v,i,j),)*2 if kind=='floor' else enclose(v,i,j)
        lo=max(lo+dl,v[j]['o']);hi=max(hi+dh,v[j]['o'])
        assert hi<=v[j]['c'],(j,'window',hi,v[j]['c'])
        slack=min(slack,v[j]['c']-hi);finishslack=min(finishslack,v[j]['c']-hi-v[j]['s'])
        lo+=v[j]['s'];hi+=v[j]['s'];score+=v[j]['p']
        ret=floordist(v,j,0) if kind=='floor' else enclose(v,j,0)[1]
        maskslack=min(maskslack,v[0]['c']-hi-ret)
    assert hi<=v[0]['c'];assert maskslack>=0,('direct return',maskslack)
    return dict(score=score,finish_interval=[str(lo),str(hi)],min_window_slack=str(slack),min_direct_return_slack=str(maskslack),min_service_finish_slack=str(finishslack))
f32=lambda x:struct.unpack('f',struct.pack('f',x))[0]
def operational(v,r):
    t=f32(float(v[0]['o']));p=0;slack=1e9
    for i,j in zip(r,r[1:]):
        # Released matrix computes floor in float64, then converts to torch.float32.
        def d(a,b):
            dx=float(v[a]['x'])-float(v[b]['x']);dy=float(v[a]['y'])-float(v[b]['y'])
            return f32(floor(100*sqrt(dx**2+dy**2))/100)
        st=max(f32(t+d(i,j)),f32(float(v[j]['o'])))
        # match torch a+wait as an additional round when waiting.
        a=f32(t+d(i,j));wait=max(0.,f32(float(v[j]['o'])-a));st=f32(a+wait)
        t=f32(st+f32(float(v[j]['s'])));p+=v[j]['p']
        slack=min(slack,float(v[j]['c'])-st,float(v[0]['c'])-f32(t+d(j,0)))
    return dict(score=p,accepted=slack>=0,slack=slack,finish=t)
cohort=json.loads((root/'evidence/HB01/FROZEN_CLAIM_COHORT_RUN6.json').read_text())
aud=json.loads((root/'evidence/HB01/results/UNROUNDED_PRIMAL_AUDIT.json').read_text())
ar={r['instance']:r['witness']['route'] for r in aud['rows']}
rows={};pub=root/'public/data/benchmark'
for name,c in cohort['rows'].items():
    raw=pub/(name+'.txt');blob=raw.read_bytes();sha=hashlib.sha256(blob).hexdigest()
    assert sha==c['raw_sha256'] and blob==(root/'evidence/public/optw_rl/data/benchmark'/raw.name).read_bytes()
    proof=root/'evidence/HB01'/c['ng_proof'];assert hashlib.sha256(proof.read_bytes()).hexdigest()==c['ng_proof_sha256']
    v=read(raw);a=route(v,c['primary_primal']['route']);b=route(v,ar[name],'unrounded')
    assert a['score']==b['score']==c['exact_optimum']
    diff=[]
    for i in range(len(v)):
        for j in range(i):
            dx=float(v[i]['x'])-float(v[j]['x']);dy=float(v[i]['y'])-float(v[j]['y'])
            operational_cents=floor(100*sqrt(dx**2+dy**2))
            exact_cents=int(100*floordist(v,i,j))
            if operational_cents!=exact_cents:diff.append([i,j,exact_cents,operational_cents])
    rows[name]=dict(raw_sha256=sha,proof_sha256=c['ng_proof_sha256'],floor=a,unrounded=b,operational_witness=operational(v,c['primary_primal']['route']),float64_edge_differences=diff)
baseline=[0,68,29,8,76,3,62,7,61,16,69,17,15,33,39,44,97,46,92,74,78,0]
base=route(read(pub/'t101.txt'),baseline);assert base['score']==399
from pypdf import PdfReader
paper=PdfReader(root/'public/paper.pdf')
texts=[p.extract_text() for p in paper.pages]
(root/'public/paper.txt').write_text('\n\f\n'.join(texts))
(root/'paper_tables.txt').write_text(texts[21]+'\n\n'+texts[26])
# Each B.7 printed row holds two instances; compare BKS and global+ft,
# and take max with B.1 model/model+as only where that table contains it.
tables={}
for line in texts[26].splitlines():
    tok=line.split()
    for k,t in enumerate(tok):
        if re.fullmatch(r't\d{3}',t) and k+3<len(tok) and all(x.isdigit() for x in tok[k+1:k+4]):
            tables[t]=dict(bks=int(tok[k+1]),neural=int(tok[k+3]))
for line in texts[21].splitlines():
    tok=line.split()
    if tok and re.fullmatch(r't\d{3}',tok[0]) and tok[0] in tables:
        tables[tok[0]]['neural']=max(tables[tok[0]]['neural'],int(tok[3]),int(tok[6]))
for name,c in cohort['rows'].items():
    assert tables[name]==dict(bks=c['historical_BKS_B7'],neural=c['best_paper_neural_B1_B7']),(name,tables.get(name))
res=dict(status='ALL AUDITS PASS',cases=rows,baseline_t101=base,paper_tables=tables,paper_sha256=hashlib.sha256((root/'public/paper.pdf').read_bytes()).hexdigest())
(root/'audit.json').write_text(json.dumps(res,indent=2))
print(json.dumps(dict(status=res['status'],cases=len(rows),baseline_t101=base['score'],float_edges={k:len(v['float64_edge_differences']) for k,v in rows.items()},all_witnesses_float32_accepted=all(v['operational_witness']['accepted'] for v in rows.values()))))

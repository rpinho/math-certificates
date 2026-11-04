"""Integer arithmetic producer for the span-degree extension; no verifier import."""
import pathlib,json,hashlib,datetime,math,shutil
ROOT=pathlib.Path(__file__).resolve().parent
def pair(s):
 a,sep,b=s.partition('/');return int(a),int(b) if sep else 1
def add(a,b):
 n=a[0]*b[1]+b[0]*a[1];d=a[1]*b[1];g=math.gcd(n,d);return n//g,d//g
def fmt(a):return str(a[0]) if a[1]==1 else str(a[0])+'/'+str(a[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=ROOT/'frozen/c38_finite_strip';v=json.loads((base/'FULL_ACCEPTANCE.json').read_text())
L=(0,1);T=(0,1);rows=[]
for e in v['spans']:
 a=pair(e['finite_irreducible_lower']);N=e['l']*e['w'];L=add(L,a);T=add(T,(a[0]*N,a[1]))
 rows.append({'h':e['l'],'w':e['w'],'degree':N,'alpha':fmt(a)})
M=v['M'];k=(M*(L[0]-L[1])*T[1])//(L[1]*T[0]);new=M-k
S=add(L,(-k*T[0],M*T[1]));g=math.gcd(1<<27,new)
assert S[0]>=S[1] and all(M-k*r['degree']>=0 for r in rows)
root=ROOT/'frozen/c38_span_degree';fr=root/'input';fr.mkdir(parents=True,exist_ok=False)
seed={'schema':'c38-span-degree-seed-v1','candidate_unrefereed':True,'family':'same finite exact family; expanded integer coefficient vector unmaterialized','main_relative_path':'../c38_finite_strip','main_packet_sha256':sha(base/'packet.json'),'main_full_sha256':sha(base/'FULL_ACCEPTANCE.json'),'M':M,'k':k,'new_M':new,'spans':rows,'L':fmt(L),'T':fmt(T),'S':fmt(S),'mu':str((1<<27)//g)+'/'+str(new//g)}
(fr/'seed.json').write_text(json.dumps(seed,indent=2)+'\n')
names=['build_span_degree.py','verify_span_degree.py','test_span_degree_controls.py','PROOF_SPAN_DEGREE.md']
for n in names:shutil.copy2(ROOT/n,fr/n)
m={'schema':'c38-span-degree-input-v1','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':{p.name:sha(p) for p in fr.iterdir()}}
(fr/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
for p in fr.iterdir():p.chmod(0o444)
print(seed['mu'],sha(fr/'MANIFEST.json'))

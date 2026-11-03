import copy,hashlib,json,os,pathlib,subprocess,sys,time
F=pathlib.Path(__file__).resolve().parent;R=F.parent;O=R/'receipts/lower';O.mkdir(parents=True,exist_ok=True)
assert os.getpriority(os.PRIO_PROCESS,0)>=10
os.environ['PYTHONDONTWRITEBYTECODE']='1'
M=json.loads((F/'MANIFEST.json').read_text())
def guard():
 assert {str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}==set(M['sha256'])|{'MANIFEST.json'}
 for name,digest in M['sha256'].items():assert hashlib.sha256((F/name).read_bytes()).hexdigest()==digest
ledger=[]
def run(impl,directory,positive=True,label=None):
 log=O/((label or 'verify_'+impl)+'.log');start=time.time()
 with log.open('w') as out:
  child=subprocess.Popen([sys.executable,str(F/f'verify_{impl}.py'),str(directory)],stdout=out,stderr=subprocess.STDOUT);code=child.wait(timeout=180)
 ledger.append(dict(label=label or impl,pid=child.pid,code=code,seconds=time.time()-start))
 if positive:assert code==0,log.read_text()[-1000:]
 else:assert code!=0 and 'AssertionError' in log.read_text()
guard()
for impl in ('a','b'):run(impl,F)
original=json.loads((F/'artifact.json').read_text())
mutations=[(['seeds','xi5','terms',0,1],2),(['seeds','xi6','denominator'],64),(['seeds','xi5','count'],47),(['seeds','xi6','degree'],5),(['seeds','cofactor_split5','lift'],'49/32'),(['chain','steps',0,'before_count'],24),(['chain','steps',0,'image'],[0]*23),(['chain','steps',0,'flips'],1<<original['chain']['steps'][0]['coordinate']),(['improved'],True),(['universal_lower'],'4/3'),(['chain','initial','count'],24),(['chain','steps'],original['chain']['steps'][:-1])]
for j,(path,value) in enumerate(mutations):
 data=copy.deepcopy(original);target=data
 for field in path[:-1]:target=target[field]
 target[path[-1]]=value;assert data!=original
 directory=O/f'red_{j:02d}';directory.mkdir(exist_ok=True);(directory/'artifact.json').write_text(json.dumps(data)+'\n')
 for impl in ('a','b'):run(impl,directory,False,f'red_{j:02d}_{impl}')
guard();result=dict(status='PASS',qualification='candidate, unrefereed; no improved lower bound',seeds=3,verified_splittings=23,rejections=24,lower='3/2',improved=False,manifest_sha256=hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),ledger=ledger)
(O/'FINAL_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='ledger'}),flush=True)

import concurrent.futures,copy,gzip,hashlib,json,os,pathlib,subprocess,sys,time
F=pathlib.Path(__file__).resolve().parent;R=F.parent;O=R/'receipts/annihilator_certificate';O.mkdir(parents=True,exist_ok=True)
assert os.getpriority(os.PRIO_PROCESS,0)>=10
os.environ['PYTHONDONTWRITEBYTECODE']='1'
M=json.loads((F/'MANIFEST.json').read_text());ledger=[]
def guard():
 assert {str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}==set(M['sha256'])|{'MANIFEST.json'}
 for name,digest in M['sha256'].items():assert hashlib.sha256((F/name).read_bytes()).hexdigest()==digest

def run(impl,path,label,positive):
 start=time.time();log=O/(label+'_'+impl+'.log')
 with log.open('w') as output:
  child=subprocess.Popen([sys.executable,str(F/f'verify_{impl}.py'),str(path)],stdout=output,stderr=subprocess.STDOUT);code=child.wait(timeout=300)
 ledger.append(dict(label=label,verifier=impl,pid=child.pid,code=code,seconds=time.time()-start))
 text=log.read_text()
 if positive:assert code==0,text[-1000:];return json.loads(text)
 assert code!=0 and 'AssertionError' in text

guard()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:checks=list(pool.map(lambda impl:run(impl,F,'positive',True),('a','b')))
assert checks[0]['rows']==checks[1]['rows'] and checks[0]['cases']==checks[1]['cases']==14
with gzip.open(F/'certificates.json.gz','rt') as source:original=json.load(source)
with gzip.open(F/'source_seeds.json.gz','rt') as source:seeds=json.load(source)
pair=next(i for i,row in enumerate(original['cases'][0]['trace']) if row['kind']=='pair')
mutations=[(['schema'],'wrong'),(['cases',0,'expected_dimension'],0),(['cases',0,'degree'],6),(['cases',0,'bank',0],str(1<<original['cases'][0]['coordinate'])),(['cases',0,'trace',0,'row'],'0'),(['cases',0,'trace',pair,'sign'],-original['cases'][0]['trace'][pair]['sign']),(['cases',0,'trace'],[]),(['cases',0,'trace',0,'kind'],'unknown')]
for j,(path,value) in enumerate(mutations):
 data=copy.deepcopy(original);target=data
 for field in path[:-1]:target=target[field]
 target[path[-1]]=value;assert data!=original
 directory=O/f'red{j}';directory.mkdir(exist_ok=True)
 with gzip.open(directory/'certificates.json.gz','wt') as output:json.dump(data,output)
 with gzip.open(directory/'source_seeds.json.gz','wt') as output:json.dump(seeds,output)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda impl:run(impl,directory,f'red{j}',False),('a','b')))
guard();result=dict(status='PASS',qualification='candidate, unrefereed; finite submitted mask-bank obstruction only',cases=14,inferences=sum(r['inferences'] for r in checks[0]['rows']),rejections=16,scope=checks[0]['scope'],rows=checks[0]['rows'],manifest_sha256=hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),ledger=ledger)
(O/'FINAL_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('rows','ledger')}),flush=True)

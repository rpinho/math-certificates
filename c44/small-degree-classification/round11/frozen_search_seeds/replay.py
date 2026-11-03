import concurrent.futures,copy,hashlib,json,os,pathlib,subprocess,sys,time
F=pathlib.Path(__file__).resolve().parent;R=F.parent;O=R/'receipts/search_seeds';O.mkdir(parents=True,exist_ok=True)
assert os.getpriority(os.PRIO_PROCESS,0)>=10
os.environ['PYTHONDONTWRITEBYTECODE']='1'
M=json.loads((F/'MANIFEST.json').read_text());ledger=[]
def guard():
 assert {str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}==set(M['sha256'])|{'MANIFEST.json'}
 for name,digest in M['sha256'].items():assert hashlib.sha256((F/name).read_bytes()).hexdigest()==digest

def run(impl,path,label,positive):
 start=time.time();log=O/(label+'_'+impl+'.log')
 with log.open('w') as out:
  child=subprocess.Popen([sys.executable,str(F/f'verify_{impl}.py'),str(path)],stdout=out,stderr=subprocess.STDOUT);code=child.wait(timeout=180)
 row=dict(label=label,verifier=impl,pid=child.pid,code=code,seconds=time.time()-start);ledger.append(row)
 text=log.read_text()
 if positive:assert code==0,text[-1000:];return json.loads(text)
 assert code!=0 and 'AssertionError' in text
guard()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:checks=list(pool.map(lambda impl:run(impl,F,'positive',True),('a','b')))
assert checks[0]['rows']==checks[1]['rows'] and checks[0]['lower']==checks[1]['lower']=='3/2'
original=json.loads((F/'artifact.json').read_text());first=sorted(original['seeds'])[0]
mutations=[(['schema'],'bad'),(['status'],'refereed'),(['lower_claim'],'49/32'),(['source_errors'],['missing']),(['seeds',first,'terms',0,1],2),(['seeds',first,'denominator'],17),(['seeds',first,'count'],47),(['seeds',first,'degree'],4),(['seeds',first,'asymptotic_lift'],'49/32')]
for j,(path,value) in enumerate(mutations):
 data=copy.deepcopy(original);target=data
 for k in path[:-1]:target=target[k]
 target[path[-1]]=value;assert data!=original
 directory=O/f'red{j}';directory.mkdir(exist_ok=True);(directory/'artifact.json').write_text(json.dumps(data)+'\n')
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda impl:run(impl,directory,f'red{j}',False),('a','b')))
guard();receipt=dict(status='PASS',qualification='candidate, unrefereed; no lower improvement',seeds=8,rejections=18,lower='3/2',rows=checks[0]['rows'],manifest_sha256=hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),ledger=ledger)
(O/'FINAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ('ledger','rows')}),flush=True)

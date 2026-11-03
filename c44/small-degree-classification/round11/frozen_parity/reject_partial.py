"""Deliberate partial-artifact corruption, both newly written checkers."""
import concurrent.futures,copy,hashlib,json,pathlib,subprocess,sys,time
F=pathlib.Path(sys.argv[1]).resolve();O=pathlib.Path(sys.argv[2]).resolve();O.mkdir(parents=True,exist_ok=True)
original=json.loads((F/'partial.json').read_text())
mutations=[(['schema'],'wrong'),(['status'],'verified'),(['degree'],5),(['controls'],20),(['norms'],[120,125]),(['minimum_norm'],31),(['gap'],15),(['component_variance_numerator'],64),(['homogeneous_seed'],False),(['even_masks'],False),(['cases',0,'omitted'],0),(['conclusion','ceiling'],21)]
tasks=[]
for i,(path,value) in enumerate(mutations):
 d=copy.deepcopy(original);cur=d
 for part in path[:-1]:cur=cur[part]
 cur[path[-1]]=value;assert d!=original
 file=O/(str(i)+'.json');file.write_text(json.dumps(d,indent=2)+'\n')
 for v in ('a','b'):tasks.append((i,v,file,path,value))
def run(t):
 i,v,file,path,value=t;cmd=[sys.executable,str(F/f'verify_partial_{v}.py'),str(file),'--case','0']
 if v=='a':cmd+=['--binary',str(F.parent/'build/verify_partial_a')]
 start=time.time();log=O/f'{i}_{v}.log'
 with log.open('w') as out:
  child=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT)
  code=child.wait(timeout=120)
 assert code!=0 and 'AssertionError' in log.read_text(),(i,v,code)
 return dict(case=i,verifier=v,code=code,pid=child.pid,path=path,value=value,seconds=time.time()-start,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(run,tasks))
j=dict(status='PASS',mutations=12,rejections=24,rows=rows);(O/'REJECTIONS.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(dict(status='PASS',rejections=24)),flush=True)

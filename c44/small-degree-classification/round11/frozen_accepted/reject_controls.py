"""Reject corrupted frozen mathematical artifacts with both exact checkers."""
import argparse, concurrent.futures, copy, hashlib, json, pathlib, subprocess, sys, time
p=argparse.ArgumentParser();p.add_argument('frozen');p.add_argument('output');a=p.parse_args()
F=pathlib.Path(a.frozen).resolve();O=pathlib.Path(a.output).resolve();O.mkdir(parents=True,exist_ok=True)
original={name:json.loads((F/name).read_text()) for name in ('caps.json','lemma.json','direct_r7.json','allminimum.json')}
def setpath(data,path,value):
 for part in path[:-1]:data=data[part]
 data[path[-1]]=value
mutations=[
 ('caps.json',['schema'],'wrong'),('caps.json',['status'],'verified'),('caps.json',['horizon'],95),
 ('caps.json',['base_counts','4'],23),('caps.json',['previous_bound'],'2'),('caps.json',['improvement_bar'],'0'),
 ('caps.json',['rows',3,'R'],475),('caps.json',['rows',3,'R'],477),('caps.json',['rows',3,'b'],'1'),
 ('caps.json',['rows',1,'previous'],'3/2'),('caps.json',['caps','8'],'479/256'),
 ('caps.json',['bound'],'2'),('caps.json',['tail'],'0'),('caps.json',['strict_claim'],'1.99'),
 ('lemma.json',['schema'],'wrong'),('lemma.json',['status'],'verified'),('lemma.json',['strict'],False),
 ('lemma.json',['link_dimension_minimum'],1),('lemma.json',['thresholds','7'],'3/2'),
 ('lemma.json',['statement'],'unconditional'),('lemma.json',['tensor_rows',0,'loss'],0),
 ('lemma.json',['tensor_rows',0,'histogram'],[]),('lemma.json',['tensor_rows',0,'low_union'],999),
 ('lemma.json',['decisive',0,'delta'],33),('lemma.json',['decisive',1,'weight'],'2'),
 ('lemma.json',['lower_links','T_requires_k_at_least'],4),
 ('lemma.json',['lower_links','P_component_loss'],'2^k'),
 ('lemma.json',['dimension_one_control','vertices'],4),
 ('direct_r7.json',['deficit'],39),
 ('direct_r7.json',['one_bad','loss_at_most'],25),
 ('direct_r7.json',['two_bad','top_pair_divisor'],8),
 ('direct_r7.json',['conclusion','R7_upper'],229),
 ('direct_r7.json',['all_minimum','homogeneous_seed_required'],False),
 ('allminimum.json',['target','norm'],125),
 ('allminimum.json',['component_variance_numerator'],64),
 ('allminimum.json',['two_component_norm_threshold'],125),
 ('allminimum.json',['positive','controls'],11),
 ('allminimum.json',['seed','terms',0],0)]
tasks=[]
for index,(name,path,value) in enumerate(mutations):
 directory=O/f'case_{index:02d}';directory.mkdir(exist_ok=True);data=copy.deepcopy(original)
 setpath(data[name],path,value)
 assert data!=original,(index,name,path,value)
 for filename,payload in data.items():(directory/filename).write_text(json.dumps(payload,indent=2)+'\n')
 for impl in ('a','b'):tasks.append((index,impl,directory,name,path,value))
def run(task):
 index,impl,directory,name,path,value=task;start=time.time()
 log=O/f'case_{index:02d}_{impl}.log'
 with log.open('w') as output:
  child=subprocess.Popen([sys.executable,str(F/f'verify_{impl}.py'),str(directory)],stdout=output,stderr=subprocess.STDOUT)
  code=child.wait(timeout=900)
 text=log.read_text();assert code!=0 and 'AssertionError' in text,(index,impl,code,text[-1000:])
 return dict(case=index,verifier=impl,pid=child.pid,code=code,path=[name,*path],value=value,seconds=time.time()-start,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,tasks))
# A weaker true claim is a positive acceptance control after crossing two.
positive=O/'positive_weaker';positive.mkdir(exist_ok=True)
weaker=copy.deepcopy(original);weaker['caps.json']['strict_claim']='2'
for name,payload in weaker.items():(positive/name).write_text(json.dumps(payload,indent=2)+'\n')
positives=[]
for impl in ('a','b'):
 child=subprocess.run([sys.executable,str(F/f'verify_{impl}.py'),str(positive)],capture_output=True,text=True,timeout=900)
 assert child.returncode==0,(impl,child.stderr)
 positives.append(dict(verifier=impl,status='ACCEPTED_TRUE_WEAKER_CLAIM',claim='2'))
receipt=dict(status='PASS',mutations=len(mutations),rejections=len(results),positive_controls=len(positives),positive_outcomes=positives,outcomes=results)
(O/'REJECTIONS.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='outcomes'}),flush=True)

"""Finish the interrupted standard round 53 without repeating generation."""
import json,time
from fractions import Fraction
from pathlib import Path
from numerics import register,write_json
from run_cg import compact,verify,batch
from supervise import run
register('resume_interrupted_round53')
p=json.loads(Path('rounds/progress.json').read_text());previous=p['history'][-1]
state=compact('rounds/archive-num-53-0.json','rounds/restricted-archive-num-53-0.json');dual='rounds/archive-num-53-0-dual.npz'
old=json.loads(Path(previous['state']).read_text())['lp'];old_cert=Fraction(json.loads(Path('certificates/best_0.2519708741876694861411-replay.json').read_text())['bound']['upper']['mantissa'])*Fraction(2)**json.loads(Path('certificates/best_0.2519708741876694861411-replay.json').read_text())['bound']['upper']['exponent']
for j in range(1,6):
 prefix=f'rounds/archive-num-53-{j}'
 run(['numerator_search.py','--state',state,'--dual',dual,'--prefix',prefix],f'logs/archive-num-53-{j}.log')
 if not json.loads(Path(prefix+'-screen.json').read_text())['added']:break
 state=prefix+'.json';dual=prefix+'-dual.npz';verify(prefix);state=compact(state,f'rounds/restricted-archive-num-53-{j}.json')
with open('STATUS.md','a') as f:f.write('\n'+time.strftime('%Y-%m-%d %H:%M:%S')+f' Round 53: den new-column search on {state}, dual {dual}.\n')
jobs=[];paths=[]
for worker in range(2):
 out=f'rounds/den-search-53-{worker}.json';paths.append(out)
 args=['cvp_search.py','--state',state,'--dual',dual,'--seconds','240','--seed',str(811104+53*101+worker*7919+30000),'--out',out,'--bank','prior_sources/union-factor-bank.json']
 jobs.append((args,f'logs/den-search-53-{worker}.log'))
batch(jobs)
negative=sum(len(json.loads(Path(path).read_text())['negative_candidates']) for path in paths)
if negative:
 prefix='rounds/den-53';run(['add_columns.py','--state',state,'--prefix',prefix,*paths],'logs/den-merge-53.log');state=prefix+'.json';dual=prefix+'-dual.npz';verify(prefix);state=compact(state,'rounds/restricted-den-53.json')
 for j in range(6):
  prefix=f'rounds/archive-den-53-{j}'
  run(['numerator_search.py','--state',state,'--dual',dual,'--prefix',prefix],f'logs/archive-den-53-{j}.log')
  if not json.loads(Path(prefix+'-screen.json').read_text())['added']:break
  state=prefix+'.json';dual=prefix+'-dual.npz';verify(prefix);state=compact(state,f'rounds/restricted-archive-den-53-{j}.json')
new=json.loads(Path(state).read_text())['lp'];new_cert=Fraction(json.loads(Path('RESULT.json').read_text())['exact_upper'])
num_negative=sum(len(json.loads(Path(f'rounds/num-search-53-{w}.json').read_text())['negative_candidates']) for w in range(4))
rec={'round':53,'old_lp':old,'new_lp':new,'gain':old-new,'certified_gain':str(old_cert-new_cert),'negative_candidates':{'num':num_negative,'den':negative},'empty_rounds':0 if new_cert<old_cert else 1,'state':state,'dual':dual,'interruption':'storage-reader revert; resumed after archive-num-53-0'}
p['history'].append(rec);p['state']=state;p['dual']=dual;write_json('rounds/progress.json',p)
with open('STATUS.md','a') as f:f.write('\n'+json.dumps(rec)+'\n')
print(json.dumps(rec),flush=True)

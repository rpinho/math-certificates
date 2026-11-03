import copy,gzip,json,pathlib,tempfile
from verify_c57c_fast import Arithmetic,prepare,verify,Rejected
source=pathlib.Path('results/c57c_phase_control055_mixed.jsonl.gz')
with gzip.open(source,'rt')as f:head=json.loads(next(f));records=[json.loads(line)for line in f]
row=next(v['D'][1]for v in records if isinstance(v,dict)and v['D'][1]['kind']=='taylor4');bad=copy.deepcopy(row);bad['phase_rule']='j*theta'
try:prepare(bad)
except Rejected:print('INVALID_PHASE_RULE_REJECTED',flush=True)
else:raise AssertionError('unsupported phase accepted')
# For mode0 the first Grunsky entry is a2=0. This valid positive form is
# identically1 and cannot be used as a negative exclusion at any point.
false={'kind':'taylor4','phase_rule':'j*theta/2','forms':[{'mode':0,'z':[[1,0]]+[[0,0]for _ in range(6)],'weight':'1'}],'area_weight':'1'}
A=Arithmetic(head)
prepared_false=prepare(false) # Reach arithmetic rather than an area-weight validation failure.
try:A.leaf(((0,40),)*4,prepared_false)
except Rejected as error:print('IDENTICALLY_POSITIVE_FORM_FALSE_EXCLUSION_REJECTED: '+str(error),flush=True)
else:raise AssertionError('false exclusion accepted')
with tempfile.TemporaryDirectory(prefix='phase-rejections-',dir=pathlib.Path.cwd())as scratch:
 for name,rows in [('empty',[]),('missing',records[:-1]),('duplicate',records+[records[-1]])]:
  p=pathlib.Path(scratch)/(name+'.gz')
  with gzip.GzipFile(str(p),'wb',mtime=0)as f:
   for v in [head,*rows]:f.write((json.dumps(v,separators=(',',':'))+'\n').encode())
  try:verify(p,quiet=True,structure_only=True)
  except Rejected:print(name.upper()+'_COVER_REJECTED',flush=True)
  else:raise AssertionError('bad cover accepted '+name)
print('ALL_MOVING_PHASE_REJECTION_CONTROLS_PASS')

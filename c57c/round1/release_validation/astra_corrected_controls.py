import sys,pathlib,gzip,json,copy
root=pathlib.Path(__file__).resolve().parent.parent;sys.path.insert(0,str(root))
from verify_c57c_fast import Arithmetic,prepare,Rejected
with gzip.open(root/'cert_parts/prefix.jsonl.gz','rt') as f:head=json.loads(next(f))
false={'kind':'taylor4','phase_rule':'j*theta/2','forms':[{'mode':0,'z':[[1,0]]+[[0,0] for _ in range(6)],'weight':'1'}],'area_weight':'0'}
def check(label,f,expected):
 try:f()
 except Rejected as e:
  msg=str(e);print(label+': '+msg,flush=True);assert msg==expected,(label,msg,expected)
 else:raise AssertionError(label+' ACCEPTED')
check('original false exclusion rejected in prepare',lambda:prepare(false),'nonpositive area weight')
bad=copy.deepcopy(false);bad['phase_rule']='j*theta'
check('original unsupported phase rejected in prepare',lambda:prepare(bad),'nonpositive area weight')
bad['area_weight']='1'
check('corrected unsupported phase',lambda:prepare(bad),'invalid phase rule')
simple={'kind':'simple','forms':false['forms']}
w=prepare(simple);A=Arithmetic(head,192)
check('valid identically positive simple form reaches arithmetic',lambda:A.leaf(((0,40),)*4,w),'simple form fails at midpoint')
# Actual finite-tree coverage and receipt mutations, keeping all other inputs valid.
from verify_c57c_forest import aggregate
import tempfile
receipts=sorted((root/'cert_receipts').glob('*.json'))
with tempfile.TemporaryDirectory(dir=root,prefix='referee-control-') as td:
 td=pathlib.Path(td); saved=json.loads(receipts[0].read_text())
 for label,field,value,reason in [('stale checker hash','checker_files',{},'checker or precision mismatch'),('false precision','precision',80,'checker or precision mismatch'),('false radius','parameters',dict(saved['parameters'],radius='13/20'),'receipt parameter mismatch')]:
  bad=copy.deepcopy(saved);bad[field]=value;p=td/'bad.json';p.write_text(json.dumps(bad))
  check(label,lambda:aggregate(root/'C57_FOREST_V2.json',[p,*receipts[1:]]),reason)
print('CORRECTED_CONTROLS_PASS')

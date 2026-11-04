"""Corrupt frozen artifacts; require each exact expected rejection code.
This program never treats an arbitrary exception as a successful control.
"""
from pathlib import Path
from fractions import Fraction as Q
from flint import ctx
import copy,json,hashlib,time
from verify_measure import verify as verify_measure
from verify_row import verify as verify_row,Rejection
ctx.prec=256
ROOT=Path(__file__).resolve().parent
BASE=json.loads((ROOT/'certificates/certificate-0447.json').read_text())
COVER=json.loads((ROOT/'certificates/row-cover.json').read_text())

def mutate_field(field,value):
 def f(d):d[field]=value
 return f
def shift(i,j,amount):
 def f(d):
  ws=list(map(Q,d['weights']));ws[i]-=Q(amount);ws[j]+=Q(amount);d['weights']=list(map(str,ws))
 return f
def bad_tail(d):d['second_tail_b']=str(Q(d['second_tail_a'])+Q(1,10**12))
def numerical_cover_failure(d):
 # Merge a deliberately broad, positive-floor branch into one grid leaf.
 # Its floor is positive, so rejection must be the numerical scalar margin.
 path=['left','left','left','left','right','left','right']
 node=d['tree']
 for key in path[:-1]:node=node[key]
 node[path[-1]]={'kind':'grid','n':4096}

measure_cases=[
 ('model','MEASURE_MODEL',mutate_field('model','signed_contact_v4')),
 ('radius','TARGET_RADIUS',mutate_field('c','8937/20000')),
 ('zeta','MEASURE_ZETA',mutate_field('zeta','21/200')),
 ('kappa','MEASURE_KAPPA',mutate_field('kappa','1/8')),
 ('list-length','MEASURE_LENGTH',mutate_field('weights',BASE['weights'][:-1])),
 ('negative-weight','MEASURE_WEIGHT',mutate_field('weights',['-1']+BASE['weights'][1:])),
 ('mass','MEASURE_MASS',mutate_field('weights',[str(Q(BASE['weights'][0])+Q(1,10**8))]+BASE['weights'][1:])),
 ('endpoint','MEASURE_ENDPOINTS',mutate_field('nodes',['1/5']+BASE['nodes'][1:])),
 ('order','MEASURE_ORDER',mutate_field('nodes',[BASE['nodes'][0],BASE['nodes'][2],BASE['nodes'][1]]+BASE['nodes'][3:])),
 ('rational-type','MEASURE_NODE_RATIONAL',mutate_field('nodes',[0.199809]+BASE['nodes'][1:])),
 ('tail-envelope','TAIL_ENVELOPE',mutate_field('tail_envelope','sampled-quadrature')),
 ('tail-cutoff-type','TAIL_CUTOFF_TYPE',mutate_field('first_tail_k',True)),
 ('first-tail-start','TAIL1_START',mutate_field('first_tail_k',100)),
 ('second-tail-interval','TAIL2_INTERVAL',mutate_field('second_tail_b','1')),
 ('cover-filename','COVER_FILENAME',mutate_field('cover_file','../row-cover.json')),
 ('cover-hash','COVER_HASH',mutate_field('cover_sha256','0'*64)),
 ('ordinary-moment','ORDINARY_MOMENT_1',shift(1,0,'1/10')),
 ('weighted-moment','WEIGHTED_MOMENT_1',shift(0,1,'1/10')),
 ('second-tail-gap','TAIL2_GAP',bad_tail),
 ('second-tail-start','TAIL2_GAP',mutate_field('second_tail_k',2)),
]
cover_cases=[
 ('cover-model','COVER_MODEL',mutate_field('model','signed_contact_v4')),
 ('cover-zeta','COVER_ZETA',mutate_field('zeta','21/200')),
 ('cover-kappa','COVER_KAPPA',mutate_field('kappa','1/8')),
 ('cover-delta','COVER_DELTA',mutate_field('delta','1/10000')),
 ('cover-root','COVER_ROOT',mutate_field('root',['0','1/3']+COVER['root'][2:])),
 ('cover-missing-child','COVER_NODE',mutate_field('tree',{'axis':0,'mid':'1/10','left':{'kind':'small'}})),
 ('cover-axis','COVER_AXIS',mutate_field('tree',{'axis':3,'mid':'1/10','left':{'kind':'small'},'right':{'kind':'small'}})),
 ('cover-split','COVER_SPLIT',mutate_field('tree',{'axis':0,'mid':'0','left':{'kind':'small'},'right':{'kind':'small'}})),
 ('false-psd','PSD_NOT_EXCLUDED',mutate_field('tree',{'kind':'psd'})),
 ('false-constant','CONSTANT_FLOOR',mutate_field('tree',{'kind':'constant'})),
 ('false-small','SMALL_REGION',mutate_field('tree',{'kind':'small'})),
 ('grid-size','GRID_SIZE',mutate_field('tree',{'kind':'grid','n':16})),
 ('unknown-leaf','COVER_LEAF_KIND',mutate_field('tree',{'kind':'trust_previous_pass'})),
 ('leaf-extra-field','COVER_LEAF_FIELDS',mutate_field('tree',{'kind':'constant','proof':'PASS'})),
 ('scalar-numerical-margin','GRID_SCALAR_MARGIN',numerical_cover_failure),
]

def main():
 start=time.monotonic();receipts=[];dest=ROOT/'controls';dest.mkdir(exist_ok=True)
 for group,cases in [('measure',measure_cases),('cover',cover_cases)]:
  for name,expected,mutate in cases:
   data=copy.deepcopy(BASE if group=='measure' else COVER);mutate(data)
   folder=dest/name;folder.mkdir(exist_ok=True)
   frozen=folder/('certificate-0447.json' if group=='measure' else 'row-cover.json')
   frozen.write_text(json.dumps(data,indent=2)+'\n')
   if group=='measure':(folder/'row-cover.json').write_bytes((ROOT/'certificates/row-cover.json').read_bytes())
   try:
    (verify_measure if group=='measure' else verify_row)(frozen);actual='ACCEPTED'
   except Rejection as e:actual=str(e)
   if actual!=expected:raise RuntimeError({'name':name,'expected':expected,'actual':actual})
   receipts.append(dict(name=name,expected=expected,actual=actual,status='PASS',artifact_sha256=hashlib.sha256(frozen.read_bytes()).hexdigest()))
   print(name,expected,'PASS',flush=True)
 out=dict(status='PASS',verification='separately written (same agent)',controls=len(receipts),all_exact_rejections=True,results=receipts,seconds=time.monotonic()-start)
 (ROOT/'logs/controls-results.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()

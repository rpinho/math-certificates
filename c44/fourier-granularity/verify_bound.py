"""Exact row recurrence, independently written from search code.
All arithmetic is rational/integer. Universal proof dependencies: PROOF.md.
"""
import hashlib,json,math,os,pathlib,sys
from fractions import Fraction as Q
from verify_spectral import verify_one
R=pathlib.Path(__file__).resolve().parent
EPISHA='ce66f1097a7284e9845113fa1dc39267932cc934fd23d9019ff13d3dcb39cf49'
CAPS={'3':'5/4','4':'31/16','7':'447/128'}
def verify(spec):
 assert spec['schema']=='c44-fourier-granularity-bound-v1'
 assert spec['caps']==CAPS and spec['external_R3']==10
 assert spec['external_bs_theorem']=='3b(b-1)<=2(d^4-d^2)'
 assert spec['horizon']==96
 data=(R/spec['epi_source']).read_bytes()
 assert hashlib.sha256(data).hexdigest()==EPISHA
 H=96;S=2**H;B=[0]
 for d in range(1,H+1):
  b=math.isqrt(2*(d**4-d*d)//3)+1
  while 3*b*(b-1)>2*(d**4-d*d):b-=1
  assert 3*b*(b-1)<=2*(d**4-d*d)<3*(b+1)*b
  B.append(b)
 epi=json.loads(data)
 for d in range(1,49):
  a=epi['certificates'][str(d)];xs=a['nodes'];ws=list(map(Q,a['weights']))
  assert len(xs)==d+1==len(ws) and xs==sorted(set(xs)) and xs[0]==1
  assert all(type(x)==int and x>0 for x in xs)
  assert ws[0]>0 and ws[0]+sum(w for w in ws[1:] if w<0)>0
  for j in range(1,d+1):assert sum(w*x**j for w,x in zip(ws,xs))==0
  B[d]=min(B[d],xs[-1]-1)
 oldB=B.copy()
 raw=(R/spec['spectral_source']).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==spec['spectral_sha256']
 spectral=json.loads(raw);assert spectral['schema']=='c44-spectral-bounds-v1'
 checks=[verify_one(c) for c in spectral['certificates']]
 assert len({a['degree'] for a in checks})==len(checks)
 for a in checks:B[a['degree']]=min(B[a['degree']],a['B'])
 def run(block,caps):
  ceiling=[0]+[int(Q(caps.get(str(d),Q(d,2)))*S) for d in range(1,H+1)]
  charge=[0]+[d*2**(H-d) for d in range(1,H+1)]
  row=[0]*(H+1)
  for b in range(1,max(block)+1):
   new=[0]*(H+1);prefix=0
   for d in range(1,H+1):
    prefix=max(prefix,row[d])
    new[d]=row[d] if b>block[d] else min(ceiling[d],charge[d]+prefix)
   row=new
  assert max(row)==row[H]
  return Q(row[H],S),row
 finite,row=run(B,CAPS);base,_=run(oldB,CAPS)
 tail=Q(H**3+6*H*H+18*H+26,2**H)
 bound=finite+tail
 assert bound<Q(spec['claim'])<Q('4.3264049226')
 ablations={}
 for name,caps in [('influence_only',{}),('cubic_only',{'3':'5/4'}),('no_strict7',{'3':'5/4','4':'31/16'})]:
  z,_=run(B,caps);ablations[name]=str(z+tail)
 return {'status':'PASS exact duals, power moments, row recurrence and elementary tail',
         'horizon':H,'B':B,'caps':CAPS,'finite':str(finite),'elementary_tail':str(tail),
         'certified_bound':str(bound),'bound_decimal':format(float(bound),'.16g'),
         'claim':spec['claim'],'margin':str(Q(spec['claim'])-bound),
         'baseline_bound':str(base+tail),'exact_gain_same_tail':str(base-finite),
         'all_finite_degrees':{str(d):str(Q(row[d],S)) for d in range(1,H+1)},
         'ablations':ablations,'spectral_checks':checks}
def main():
 print('PID',os.getpid(),flush=True)
 p=R/(sys.argv[1] if len(sys.argv)>1 else 'candidate.json')
 result=verify(json.loads(p.read_text()))
 (R/'verification_bound_row.json').write_text(json.dumps(result,indent=2)+'\n')
 print({k:result[k] for k in ('status','certified_bound','bound_decimal','claim','exact_gain_same_tail')},flush=True)
if __name__=='__main__':main()

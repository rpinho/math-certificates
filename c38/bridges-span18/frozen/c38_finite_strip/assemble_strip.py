"""Search-side exact assembler. No acceptance without complete separate replay."""
import sys,json,pathlib
from fractions import Fraction as Q
sys.set_int_max_str_digits(200000)
def assemble(directory,L,M,separate=False):
 lo,hi,alpha,beta={},{},{},{}
 caps={};rows=[]
 for l in range(1,L+1):
  d=json.loads((pathlib.Path(directory)/('span_%d.json'%l)).read_text())
  if separate:
   assert d['M']==M and d['l']==l;e=d
  else:
   assert d['l']==l;e=next(e for e in d['x'] if e['Mnum']==M)
  D=1<<d['S'];lo[l]=Q(int(e['num_lo']),D);hi[l]=Q(int(e['num_hi'])+int(e['num_tail']),D);caps[l]=d['w']
  assert 0<=lo[l]<=hi[l]
  alpha[l]=max(Q(0),lo[l]-sum((beta[j]*hi[l-j] for j in range(1,l)),Q(0)))
  finite=d.get('mode')=='FINITE_LAST_SPAN_LOWER_ONLY'
  if finite:
   assert l==L and int(e['num_tail'])==0 and d.get('infinite_tail_certified') is False
   beta[l]=None;upper=None
  else:
   beta[l]=hi[l]-sum((alpha[j]*lo[l-j] for j in range(1,l)),Q(0));assert 0<=alpha[l]<=beta[l];upper=str(beta[l])
  rows.append({'l':l,'w':caps[l],'mode':'FINITE_LAST_SPAN_LOWER_ONLY' if finite else 'FULL_WIDTH_CERTIFIED','finite_irreducible_lo':str(alpha[l]),'full_irreducible_hi':upper,'lo_decimal_diagnostic':float(alpha[l]),'hi_decimal_diagnostic':float(beta[l]) if beta[l] is not None else None})
 P=sum(alpha.values(),Q(0));return {'status':'ARITHMETIC_ONLY_REPLAY_REQUIRED','L':L,'M':M,'x':str(Q(M,1<<27)),'mu':str(Q(1<<27,M)),'P_lower':str(P),'P_decimal_diagnostic':float(P),'margin_decimal_diagnostic':float(P-1),'P_ge_1':P>=1,'max_degree':max(l*caps[l] for l in caps),'rows':rows}
if __name__=='__main__':
 result=assemble(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),'--separate' in sys.argv)
 pathlib.Path(sys.argv[4]).write_text(json.dumps(result,indent=2)+'\n');print('P=',result['P_decimal_diagnostic'],'>=1',result['P_ge_1'])

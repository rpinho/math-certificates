"""Compare independently enumerated numbers to untrusted producer data."""
import csv
import json
import pathlib
import sys
from fractions import Fraction as Q
sys.set_int_max_str_digits(500000)
ROOT=pathlib.Path(__file__).resolve().parent
PRODUCER=ROOT.parent/'c38'
def read(p):return json.loads(p.read_text())
def finite(r):return Q(int(r['finite_numerator']),1<<r['finite_denominator_exponent'])
def tail(r):return Q(int(r['tail_numerator']),1<<r['tail_denominator_exponent'])
def irred_coeff(B,L,N):
    A=[[0]*(N+1) for _ in range(L+1)]
    for h in range(1,L+1):
        for n in range(1,N+1):
            A[h][n]=B[h][n]-sum(A[j][m]*B[h-j][n-m]
                                  for j in range(1,h) for m in range(1,n))
            assert A[h][n]>=0
    return A
def main():
    baseline=read(PRODUCER/'sources'/'numaro'/'bridge_table_record_L17.json')
    N=40;L=int(sys.argv[1]) if len(sys.argv)>1 else 10
    B=[[0]*(N+1)]+[list(map(int,read(ROOT/'results'/'pod'/f'count{h}.json')['bridge_counts'])) for h in range(1,L+1)]
    A=irred_coeff(B,L,N)
    baseB=[[int(baseline['b_nl'][n][h]) for n in range(N+1)] for h in range(L+1)]
    baseA=irred_coeff(baseB,L,N)
    assert B[1:]==baseB[1:] and A[1:]==baseA[1:]
    prefix={(int(r['n']),int(r['span'])):int(r['bridges']) for r in csv.DictReader((PRODUCER/'frozen/c38_prefix24/replay/bridges.csv').open())}
    prefixchecks=0
    for (n,h),v in prefix.items():
        if h<=L and n<=N:assert B[h][n]==v;prefixchecks+=1
    literal=read(ROOT/'results'/'LITERAL.json')
    for n,h,b,a in literal['rows']:
        if h<=L:assert (B[h][n],A[h][n])==(b,a)
    audited=read(ROOT/'results'/'EXACT_AUDIT.json')
    rows=[]
    for name,m in [('b',51081913),('c',51082227)]:
        bb=[Q(0)];UU=[Q(0)];aa=[Q(0)];bet=[Q(0)]
        for h in range(1,L+1):
            own=read(ROOT/'results'/'pod'/f'{name}{h}.json')
            folder='c38_finite_strip/replay' if name=='b' else 'span17_all_length_stop/replay_public'
            claimed=read(PRODUCER/'frozen'/folder/f'span_{h}.json')
            x=finite(own);t=tail(own)
            assert own['span']==h and own['M']==m and own['width']==claimed['w']
            assert Q(int(claimed['num_lo']),1<<96)<=x<=Q(int(claimed['num_hi']),1<<96)
            assert x+t<=Q(int(claimed['num_hi'])+int(claimed['num_tail']),1<<96)
            bb.append(x);UU.append(x+t)
            aa.append(max(Q(0),x-sum((bet[j]*UU[h-j] for j in range(1,h)),Q(0))))
            bet.append(UU[h]-sum((aa[j]*bb[h-j] for j in range(1,h)),Q(0)))
            if name=='b':
                assert aa[h]>=Q(audited['per_span'][h-1]['alpha'])
                assert bet[h]<=Q(audited['per_span'][h-1]['beta'])
            rows.append({'point':name,'h':h,'finite_exact_inside_claimed_interval':True,
                         'own_full_upper_no_larger_than_claimed':True,
                         'B_finite_diagnostic':float(x),'own_alpha_diagnostic':float(aa[h]),
                         'own_beta_diagnostic':float(bet[h]),
                         'claimed_bracket_width':str(Q(int(claimed['num_hi'])-int(claimed['num_lo']),1<<96))})
    output={'status':'PASS','spans':L,'coefficient_max_length':N,
            'bridge_entries_compared_to_numaro':L*(N+1),
            'irreducible_entries_compared_to_numaro':L*(N+1),
            'bridge_entries_compared_to_producer_prefix':prefixchecks,
            'literal_prefixes':literal['prefixes'],'literal_factorizations':literal['factorizations_checked'],
            'exact_point_checks':rows,
            'irreducible_counts':{str(h):[str(a) for a in A[h]] for h in range(1,L+1)}}
    (ROOT/'results'/'RECOUNT_COMPARISON.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ['exact_point_checks','irreducible_counts']},indent=2))
    for h in range(1,L+1):print(h,'a40=',A[h][40])
if __name__=='__main__':main()

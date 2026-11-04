"""Independent data-only arithmetic audit. Never imports producer programs."""
import hashlib
import json
import pathlib
import sys
from fractions import Fraction as Q

sys.set_int_max_str_digits(500000)
HERE=pathlib.Path(__file__).resolve().parent
BASE=HERE.parent/'c38'/'frozen'
D=1<<96
def read(p): return json.loads(p.read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def renewal(rows,terminal=False):
    b=[Q(0)]; u=[Q(0)]; alpha=[Q(0)]; beta=[Q(0)]
    for h,row in enumerate(rows,1):
        assert row['l']==h and row['S']==96
        assert int(row['num_lo'])<=int(row['num_hi'])
        b.append(Q(int(row['num_lo']),D))
        u.append(Q(int(row['num_hi'])+int(row['num_tail']),D))
        alpha.append(max(Q(0),b[h]-sum((beta[j]*u[h-j] for j in range(1,h)),Q(0))))
        beta.append(None if terminal and h==len(rows) else
                    u[h]-sum((alpha[j]*b[h-j] for j in range(1,h)),Q(0)))
        assert alpha[h]>=0
        if beta[h] is not None: assert alpha[h]<=beta[h]
    return b,u,alpha,beta

def main():
    mainroot=BASE/'c38_finite_strip'
    packet=read(mainroot/'packet.json')
    assert [x['l'] for x in packet['spans']]==list(range(1,19))
    rows=[];hashes={}
    for entry in packet['spans']:
        p=mainroot/entry['separate']['path'];row=read(p);rows.append(row)
        assert digest(p)==entry['separate']['sha256']
        assert row['w']==entry['w'] and row['M']==51081913
        production=read(mainroot/entry['production']['path'])
        assert digest(mainroot/entry['production']['path'])==entry['production']['sha256']
        point=next(x for x in production['x'] if x['Mnum']==51081913)
        assert all(point[k]==row[k] for k in ['num_lo','num_hi'])
        assert read(mainroot/'complete_union_replay'/f"span_{entry['l']}.json")==row
        hashes[str(p.relative_to(BASE))]=digest(p)
    assert rows[-1]['infinite_tail_certified'] is False
    assert int(rows[-1]['num_tail'])==0
    b,u,alpha,beta=renewal(rows,True)
    assert sum(alpha,Q(0))==Q(packet['P_lower'])
    other=[read(BASE/'span17_all_length_stop'/'replay_public'/f'span_{h}.json') for h in range(1,18)]
    assert all(r['M']==51082227 for r in other)
    for h,r in enumerate(other,1):
        assert r==read(BASE/'span17_all_length_stop'/'complete_union_replay'/f'public_{h}.json')
        p=BASE/'span17_all_length_stop'/'replay_public'/f'span_{h}.json'
        hashes[str(p.relative_to(BASE))]=digest(p)
    bc,uc,ac,betac=renewal(other)
    L17=sum(alpha[1:18],Q(0));L18=alpha[18];U=sum(betac[1:],Q(0))
    r22=read(BASE/'rectangle_point'/'w22_h18_30_c5'/'replay.json')
    r23=read(BASE/'rectangle_point'/'w23_h18_18_c5_parallel'/'replay.json')
    for folder in ['w22_h18_30_c5','w23_h18_18_c5_parallel']:
        p=BASE/'rectangle_point'/folder/'replay.json';hashes[str(p.relative_to(BASE))]=digest(p)
    assert [r22[k] for k in ['W','span_min','span_max','crossing_cap','M','S']]==[22,18,30,5,51081913,96]
    assert [r23[k] for k in ['W','span_min','span_max','crossing_cap','M','S']]==[23,18,18,5,51081913,96]
    e=max(Q(0),Q(int(r22['num_lo'])-int(r23['num_hi']),D))
    seed=read(BASE/'c38_power_secant'/'input'/'seed.json')
    for name,value in [('L17',L17),('L18',L18),('U',U),('e',e)]:assert Q(seed[name])==value
    assert min(L17,L18,e)>=0 and U>=L17
    assert max(x['l']*x['w'] for x in packet['spans'])==packet['max_degree']==6817
    N18=18*packet['spans'][-1]['w'];NE=30*(22+1)
    assert (N18,NE)==(1296,690)
    M=51081913
    def terms(k):
        r=Q(M-k,M);t=Q(k,314)
        return [(1+t)*L17,-t*U,r**N18*L18,r**NE*e]
    k=1353;parts=terms(k);S=sum(parts,Q(0));nextS=sum(terms(k+1),Q(0))
    assert S>1 and nextS<1
    slack_lo=Q(11437205719677,10**20);slack_hi=Q(11437205719678,10**20)
    assert slack_lo<S-1<slack_hi
    assert Q(seed['S'])==S==Q(read(BASE/'c38_power_secant'/'VERIFIED.json')['S'])
    mu=Q(1<<27,M-k)
    baseline=Q(1<<128,129513673858566230428673965530967449326)
    assert mu==Q(8388608,3192535) and mu>Q(1051,400)>baseline
    output={'status':'EXACT_ARITHMETIC_PASS_CONDITIONAL_ON_NATIVE_DATA',
            'source_sha256':digest(pathlib.Path(__file__)), 'native_input_sha256':hashes,
            'L17':str(L17),'L18':str(L18),'U':str(U),'e':str(e),
            'k':k,'a':str(Q(M-k,1<<27)),'r':str(Q(M-k,M)),
            'N18':N18,'NE':NE,'mu':str(mu),
            'terms_diagnostic':[float(t) for t in parts],
            'S':str(S),'S_minus_one':str(S-1),
            'simple_exact_slack_bracket':[str(slack_lo),str(slack_hi)],
            'S_minus_one_diagnostic':float(S-1),'next_minus_one_diagnostic':float(nextS-1),
            'per_span':[{'h':h,'b_lower':str(b[h]),'B_upper':str(u[h]) if h<18 else None,
                         'alpha':str(alpha[h]),'beta':str(beta[h]) if h<18 else None,
                         'alpha_decimal':float(alpha[h])} for h in range(1,19)]}
    (HERE/'results'/'EXACT_AUDIT.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ['status','mu','terms_diagnostic','S_minus_one_diagnostic','next_minus_one_diagnostic']},indent=2))

if __name__=='__main__':main()

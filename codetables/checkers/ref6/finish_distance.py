"""Assemble the complete distance argument from exact BCH and BZ calculations."""
from checker import *
from prepare import nullspace
import math

def main():
    start=time.perf_counter();field_check()
    assert NS not in {mul(x,x) for x in range(9)}
    assert epow(ALPHA,80)==1 and epow(ALPHA,40)!=1 and epow(ALPHA,16)!=1
    G=[list(map(int,r.split())) for r in Path('inputs/q9_n85_k15_d54.txt').read_text().splitlines()]
    assert len(rref(G)[1])==15
    base=set(roots(G[0][:80]));assert len(base)==65
    assert all(set(roots(row[:80]))==base for row in G)
    assert bch_bound(base)[0]>=51
    # Exhaust all tail supports of size <=2 other than the exceptional subcode.
    cases=[]
    for size in (1,2):
        for support in itertools.combinations(range(5),size):
            if support==(0,):continue
            H=[[row[80+j] for row in G] for j in range(5) if j not in support]
            B=nullspace(H);C=[codeword(G,b)[:80] for b in B];common=set(range(80))
            for row in C:common.intersection_update(roots(row))
            bound=bch_bound(common)
            assert bound[0]+size>=54
            cases.append({'tail_support':list(support),'dimension':len(B),'bch':bound,'additional_roots':sorted(common-base),'total_lower_bound':bound[0]+size})
    setup=json.loads(Path('bz_setup.json').read_text());C=setup['G'];k=len(C);assert k==12
    B=nullspace([[row[j] for row in G] for j in range(81,85)])
    assert C==[codeword(G,b)[:81] for b in B]
    records=[json.loads(l) for l in Path('bz_result.jsonl').read_text().splitlines()]
    assert len(records)==sum(s['depth'] for s in setup['sets'])
    total=0;lower=0;seen=set();best=86;witness=None
    for i,s in enumerate(setup['sets']):
        cols=s['columns'];S=s['G'];r=len(set(cols)-seen)
        assert r==s['relative_rank'];seen.update(cols)
        assert len(cols)==k and len(set(cols))==k and len(rref(C+S)[1])==k
        assert all(S[a][cols[b]]==int(a==b) for a in range(k) for b in range(k))
        for depth in range(1,s['depth']+1):
            rec=[x for x in records if x['set']==i and x['depth']==depth];assert len(rec)==1
            rec=rec[0];expected=math.comb(k,depth)*8**(depth-1)
            assert rec['count']==expected and rec['min']>=54
            word=rec['word'];assert sum(bool(x) for x in word)==rec['min']
            assert codeword(S,[word[j] for j in cols])==word
            total+=expected
            if rec['min']<best:best=rec['min'];witness=word+[0]*4
        lower+=max(0,s['depth']+1-(k-r))
    assert lower==54 and best==54
    # Recover message in the supplied generator, whose first 15 columns are triangular.
    m=[]
    for j in range(15):
        residual=witness[j]
        for i in range(j):residual=add(residual,neg(mul(m[i],G[i][j])))
        m.append(mul(residual,inv(G[j][j])))
    assert codeword(G,m)==witness and sum(bool(x) for x in witness)==54
    rs=json.loads(Path('rs_control.json').read_text())
    rsrows=[json.loads(l) for l in Path('rs_bz.jsonl').read_text().splitlines()]
    assert all(r['min']==7 for r in rsrows) and len(rsrows)==6
    assert rs['exhaustive_distance']==rs['theoretical_distance']==7
    out={'rank':15,'minimum_distance':54,'method':'BCH bounds by appended support plus complete Brouwer-Zimmermann on a shortened [81,12,54] subcode','base_bch_bound':51,'support_cases':cases,'bz_projective_visits':total,'bz_relative_ranks':[s['relative_rank'] for s in setup['sets']],'bz_depths':[s['depth'] for s in setup['sets']],'bz_unseen_lower_bound':lower,'witness_message':m,'witness_word':witness,'witness_weight':54,'rs_control_distance':7,'assembly_seconds':time.perf_counter()-start}
    Path('distance_result.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:val for key,val in out.items() if key not in ('support_cases','witness_word')},indent=2))
if __name__=='__main__':main()

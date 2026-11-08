from checker import *

def nullspace(H):
    R,p=rref(H); B=[]
    for j in range(len(H[0])):
        if j in p:continue
        row=[0]*len(H[0]);row[j]=1
        for i,c in enumerate(p):row[c]=neg(R[i][j])
        B.append(row)
    return B

def information_sets(G):
    n=len(G[0]);k=len(G);used=set();out=[]
    while len(used)<n:
        order=[j for j in range(n) if j not in used]+sorted(used)
        R,p=rref([[row[j] for j in order] for row in G]);assert len(p)==k
        cols=[order[j] for j in p];fresh=set(cols)-used
        if not fresh:break
        S=[[0]*n for _ in range(k)]
        for i in range(k):
            for j in range(n):S[i][order[j]]=R[i][j]
        assert all(S[i][cols[j]]==int(i==j) for i in range(k) for j in range(k))
        assert len(rref(G+S)[1])==k
        out.append({'columns':cols,'relative_rank':len(fresh),'G':S})
        used.update(cols)
    assert len(used)==n
    return out

def write_input(filename,sets,depths):
    n=len(sets[0]['G'][0]);k=len(sets[0]['G'])
    with open(filename,'w') as f:
        f.write(f'{len(sets)} {n} {k}\n')
        for i,(s,depth) in enumerate(zip(sets,depths)):
            f.write(f'{i} {depth} {s["relative_rank"]}\n')
            for row in s['G']:f.write(' '.join(map(str,row))+'\n')

def main():
    G=[list(map(int,r.split())) for r in Path('inputs/q9_n85_k15_d54.txt').read_text().splitlines()]
    B=nullspace([[row[j] for row in G] for j in range(81,85)])
    assert len(B)==12
    C=[codeword(G,b) for b in B];assert all(not any(row[81:]) for row in C)
    C=[row[:81] for row in C]
    sets=information_sets(C);ranks=[s['relative_rank'] for s in sets]
    depths=[7]*len(sets)
    while sum(max(0,d+1-(12-r)) for d,r in zip(depths,ranks))<54:
        depths[depths.index(min(depths))]+=1
    for s,d in zip(sets,depths):s['depth']=d
    result={'basis_messages':B,'G':C,'sets':sets,'unseen_lower_bound':sum(max(0,d+1-(12-r)) for d,r in zip(depths,ranks))}
    Path('bz_setup.json').write_text(json.dumps(result,indent=2)+'\n')
    write_input('bz_input.txt',sets,depths)
    print('relative ranks',ranks,'depths',depths,'unseen bound',result['unseen_lower_bound'])
    RS=[[power(x,i) for x in range(9)] for i in range(3)]
    rssets=information_sets(RS);write_input('rs_input.txt',rssets,[2]*len(rssets))
    # RS exhaustive independent scalar arithmetic, normalise first nonzero coefficient.
    hist={};count=0
    for m in itertools.product(range(9),repeat=3):
        if not any(m) or next(x for x in m if x)!=1:continue
        w=sum(x!=0 for x in codeword(RS,m));hist[w]=hist.get(w,0)+1;count+=1
    assert min(hist)==7 and count==91
    Path('rs_control.json').write_text(json.dumps({'n':9,'k':3,'theoretical_distance':7,'exhaustive_distance':min(hist),'projective_words':count,'histogram':hist,'sets':rssets},indent=2)+'\n')
if __name__=='__main__':main()

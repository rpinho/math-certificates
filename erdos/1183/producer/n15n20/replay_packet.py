"""Replay delivered n=15..20 trees and every explicit witness; standard library only.

Run with python3 -B from the packet root. Does not import the search code.
"""
import sys, pathlib, json, math
ROOT=pathlib.Path(__file__).resolve().parents[2]
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'src'))
from check import witness,tree,read_open

def run():
    rows=json.loads((HERE/'certificates/results.json').read_text())
    assert [r['n'] for r in rows]==list(range(15,21))
    for r in rows:
        n,w=r['n'],r['word']
        coloring=json.loads((ROOT/f'certificates/n{n}_coloring.json').read_text())
        assert coloring['n']==n and coloring['rank_word']==w
        assert len(coloring['colors'])==1<<n
        assert all(v==int(w[k.bit_count()]) for k,v in enumerate(coloring['colors']))
        for c in r['colours']:
            witness(n,w,c['colour'],c['maximum'],c['witness'])
            assert len(c['witness'])==c['maximum']
            nodes=tree(HERE/c['proof'],w,c['colour'],c['maximum']+1)
            assert nodes==c['nodes']
        assert max(c['maximum'] for c in r['colours'])==r['upper']
        print('HEADLINE',n,'upper',r['upper'],'both trees and witnesses PASS',flush=True)
    total=0
    for kind in ('screen','prefix'):
        for p in sorted((HERE/'certificates').glob('*_'+kind+'.jsonl.xz')):
            count=0
            with read_open(p) as inp:
                h=json.loads(next(inp))
                for line in inp:
                    word,c,f=json.loads(line)
                    if c=='survives':continue
                    assert len(word)-1<=h['n']
                    witness(len(word)-1,word,c,h['T']+1,f)
                    count+=1
            total+=count
            print('WITNESSES',p.name,count,'PASS',flush=True)
    for n in (15,17,19):
        p=HERE/f'certificates/n{n}_balanced.jsonl.xz'
        with read_open(p) as inp:
            h=json.loads(next(inp));seen=set()
            assert h['threshold']==(n+3)//2
            for line in inp:
                w,c,f=json.loads(line)
                assert len(w)==n+1 and w.count('1')==(n+1)//2 and w not in seen
                seen.add(w);witness(n,w,c,h['threshold'],f)
            assert len(seen)==math.comb(n+1,(n+1)//2)
        print('BALANCED producer',n,len(seen),'PASS',flush=True)
        seen=set();count=0
        for line in (ROOT/f'referee/n15n20/out/bal_n{n}.tsv').open():
            w,c,*f=line.split();assert c!='NONE'
            assert len(w)==n+1 and w.count('1')==(n+1)//2 and w not in seen
            seen.add(w);witness(n,w,int(c),(n+3)//2,list(map(int,f)));count+=1
        assert count==len(seen)==math.comb(n+1,(n+1)//2)
        print('BALANCED referee',n,count,'PASS',flush=True)
    print('PACKET REPLAY PASS;',total,'screen/prefix witnesses;',flush=True)

if __name__=='__main__':run()

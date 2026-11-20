import pickle, itertools, sys
res = pickle.load(open('out/final21.pkl','rb'))
W = ["0010011100101100011011","0011001011100010110011","1100110100011101001100","1101100011010011100100"]
print('dim-21 shapes:', len(res), ' (two-block:', sum(1 for s in res if s[2]==0), ')')
words_all = None; bad = 0
for (u,v,w), lst in sorted(res.items()):
    ws = set()
    for t, zm in lst:
        cells = [(x,y,z) for z in range(w+1) for y in range(v+1) for x in range(u+1)]
        r = {}
        for ch,(x,y,z) in zip(t, cells): r.setdefault(x+y+z, set()).add(ch)
        if any(len(s)!=1 for s in r.values()) or zm != 2: bad += 1; print('NONRANK/ctx', (u,v,w), zm)
        ws.add(''.join(r[k].pop() for k in range(22)))
    if words_all is None: words_all = ws
    if ws != words_all or len(lst)!=4: bad += 1; print('DIFF', (u,v,w), len(lst))
print('every shape has 4 rank tables at z=1 only, same words:', bad==0, sorted(words_all)==sorted(W))
# 16 ordered comparisons w[k+1] vs v[k], k=0..20
dists = [sum(a[k+1]!=b[k] for k in range(21)) for a in W for b in W]
print('shift distances', dists, 'min', min(dists), 'count10', dists.count(10), 'count11', dists.count(11))
# n=23 splits: fix two elements of largest block -> windows (a-2,b,c) at offsets 0,1; shared ranks 1..21
splits = [(a,b,23-a-b) for a in range(21,0,-1) for b in range(a,0,-1) if 1<=23-a-b<=b]
ok = 0
for a,b,c in splits:
    sh = tuple(sorted((a-2,b,c), reverse=True))
    rng = set(x+y+z for x in range(1,a-1) for y in range(b+1) for z in range(c+1))  # shared x in [1,a-2]
    ok += (sh in res and rng == set(range(1,22)))
print('splits', len(splits), 'covered by displaced-window argument', ok)

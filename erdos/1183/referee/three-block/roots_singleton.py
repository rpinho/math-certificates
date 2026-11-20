import collections, itertools
exec(open('roots.py').read().split('s23 = ')[0])
def single(a,b,ax):
    # singleton block C fixed absent (z=0); displace a window along axis ax (0: shorten A, 1: shorten B)
    c = 1; V = (a+1)*(b+1)*2; cl = []
    for o in (0,1):
        sels = [V+1+4*o+i for i in range(4)]; cl.append(tuple(sels))
        for i,s in enumerate(sels):
            rx = range(a) if ax==0 else range(a+1); ry = range(b+1) if ax==0 else range(b)
            for y in ry:
                for x in rx:
                    X, Y = (x+o, y) if ax==0 else (x, y+o)
                    v = var(a,b,X,Y,0); cl.append((-s, v if W[i][x+y]=='1' else -v))
    return collections.Counter(tuple(sorted(t)) for t in cl)
s23 = [(a,b,23-a-b) for a in range(21,0,-1) for b in range(a,0,-1) if 1<=23-a-b<=b]
for s in s23:
    sh = cnf(f'{D}/split23/%d-%d-%d.cnf' % s)
    if split23(*s) == sh: continue
    a,b,c = s
    print(s, 'singleton-window match axis0:', single(a,b,0)==sh, 'axis1:', single(a,b,1)==sh)

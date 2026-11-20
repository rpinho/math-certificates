# Regenerate split roots from the definition (own encoding guess), compare clause multisets with shipped files;
# check every split22 13-family from the definition and the n=22 adjoin-full-set argument directly.
import gzip, json, sys, os, collections
D = '../data'
W = ["0010011100101100011011","0011001011100010110011","1100110100011101001100","1101100011010011100100"]
def cnf(path):
    cl = []
    for ln in open(path):
        if ln[0] in 'pc': continue
        cl.append(tuple(sorted(map(int, ln.split()[:-1]))))
    return collections.Counter(cl)
def closed(f):
    s = set(f); return len(s) == len(f) and all((a|b) in s and (a&b) in s for a in f for b in f)
def var(a,b,x,y,z): return 1 + x + (a+1)*(y + (b+1)*z)
def split23(a,b,c):
    V = (a+1)*(b+1)*(c+1); cl = []
    for o in (0,1):
        sels = [V+1+4*o+i for i in range(4)]; cl.append(tuple(sels))
        for i,s in enumerate(sels):
            for z in range(c+1):
                for y in range(b+1):
                    for x in range(a-1):
                        v = var(a,b,x+o,y,z); cl.append((-s, v if W[i][x+y+z]=='1' else -v))
    return collections.Counter(tuple(sorted(t)) for t in cl)
def cellof(m,a,b,c):
    return (bin(m & ((1<<a)-1)).count('1'), bin((m>>a) & ((1<<b)-1)).count('1'), bin((m>>(a+b)) & ((1<<c)-1)).count('1'))
def split22(a,b,c, fams):
    V = (a+1)*(b+1)*(c+1); cl = []
    sels = [V+1+i for i in range(4)]; cl.append(tuple(sels))
    for i,s in enumerate(sels):
        for z in range(c+1):
            for y in range(b+1):
                for x in range(a):
                    v = var(a,b,x,y,z); cl.append((-s, v if W[i][x+y+z]=='1' else -v))
    for f in fams:
        vs = sorted(set(var(a,b,*cellof(m,a,b,c)) for m in f))
        cl.append(tuple(vs)); cl.append(tuple(-v for v in vs))
    return collections.Counter(tuple(sorted(t)) for t in cl)
s23 = [(a,b,23-a-b) for a in range(21,0,-1) for b in range(a,0,-1) if 1<=23-a-b<=b]
ok = sum(split23(*s) == cnf(f'{D}/split23/%d-%d-%d.cnf' % s) for s in s23)
print('split23 roots regenerated, clause multiset equal:', ok, '/', len(s23))
s22 = sorted(set(tuple(map(int, f.split('.')[0].split('-'))) for f in os.listdir(f'{D}/split22')))
okc = okf = okarg = 0; nf = 0
for (a,b,c) in s22:
    fams = json.load(gzip.open(f'{D}/split22/%d-%d-%d.families.gz' % (a,b,c)))
    full = (1<<22)-1; good = True; cover = set()
    for f in fams:
        nf += 1
        inner = [m for m in f if m != full]
        absent = full & ~ (lambda o: o)(0)
        orr = 0
        for m in inner: orr |= m
        fixed = [k for k in range(a) if not (orr>>k)&1]          # some A-coordinate absent from all 12
        cols = set()
        for m in f:
            x,y,z = cellof(m,a,b,c)
        if not (closed(f) and len(f)==13 and full in f and fixed): good = False; continue
        # which word/colour does the inner 12-family certify? ranks of inner sets (block counts sum = popcount)
        ranks = [bin(m).count('1') for m in inner]
        for i,w in enumerate(W):
            for col in '01':
                if all(w[r]==col for r in ranks): cover.add((i,col))
    okf += good; okarg += (len(cover)==8)
    okc += split22(a,b,c,fams) == cnf(f'{D}/split22/%d-%d-%d.cnf' % (a,b,c))
print('split22 splits', len(s22), 'families', nf, 'all valid(13 distinct, closed, full set, fixed A-coord absent):', okf,
      '| every word x colour has a 12-family:', okarg, '| CNF regenerated equal:', okc)

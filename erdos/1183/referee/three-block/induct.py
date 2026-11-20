# Clean-room referee induction for 21-dim faces of block colourings (Erdos #1183, n=23, h=13).
# Own window gluing, own slice test, own context bookkeeping. Producer witness families are read
# from data/{p,t}-*.gz only as certificates; each one used is checked here from the definition.
import gzip, json, sys, os, pickle, itertools
import numpy as np

N, H = 23, 13
DATA = sys.argv[1] if len(sys.argv) > 1 else '../data'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'out'
os.makedirs(OUT, exist_ok=True)
stats = {'fam_checked': 0, 'fam_bad': 0, 'fam_used': 0, 'cand_pairs': 0, 'surv_pairs': 0}

def zrange(d):
    lo, hi = max(0, 10 - d), min(H, N - d)       # need 13-z>=0 and d-10+z>=0
    return sum(1 << z for z in range(lo, hi + 1)) if lo <= hi else 0

def bound_ok_mask(c, k, d):
    # z-mask of contexts in which a colour-c local closed family of size k is allowed
    if c == 0:   # k <= 13 - z
        return sum(1 << z for z in range(0, N + 1) if k <= H - z)
    return sum(1 << z for z in range(0, N + 1) if k <= H - (N - d - z))

def closed(fam):
    s = set(fam)
    if len(s) != len(fam): return False
    for a in fam:
        for b in fam:
            if (a | b) not in s or (a & b) not in s: return False
    return True

def cells_of(fam, shape):
    u, v, w = shape
    mA, mB, mC = (1 << u) - 1, ((1 << v) - 1) << u, ((1 << w) - 1) << (u + v)
    return [(bin(m & mA).count('1'), bin(m & mB).count('1'), bin(m & mC).count('1')) for m in fam]

def load_families(shape):
    u, v, w = shape
    f = os.path.join(DATA, ('t-%d-%d-%d.gz' % shape) if w else ('p-%d-%d.gz' % (u, v)))
    raw = json.load(gzip.open(f))
    d = u + v + w
    fams = {}
    for z, lst in enumerate(raw):
        for fam in lst:
            loc = tuple(sorted(m for m in fam if m < (1 << d)))
            ext = [m for m in fam if m >= (1 << d)]
            # exterior members must be canonical prefixes above the face (comparable with all local sets)
            ok_ext = all(m & (m + 1) == 0 for m in ext)
            stats['fam_checked'] += 1
            if not loc: continue
            if not (ok_ext and closed(list(loc)) and closed(list(fam))):
                stats['fam_bad'] += 1; continue
            fams[loc] = 1
    out = []
    for loc in fams:
        cs = sorted(set(cells_of(loc, shape)))
        out.append((len(loc), cs, loc))
    return out

shapes2 = [(u, v, 0) for d in range(0, 22) for v in range(0, d // 2 + 1) for u in [d - v]]
def child3(s):
    u, v, w = s
    if (u, v, w) == (1, 1, 1): return 2
    for j in (2, 1, 0):
        if s[j] >= 2: return j
    return 0
def child2(s):
    u, v, _ = s
    return 1 if (v >= 2 or (u, v) == (1, 1)) else 0
need3 = set()
def add3(s):
    if s in need3: return
    need3.add(s)
    j = child3(s); c = list(s); c[j] -= 1; c = tuple(c)
    if c[2] > 0: add3(c)
for d21 in [(a, b, 21 - a - b) for a in range(21, 0, -1) for b in range(a, 0, -1) if 1 <= 21 - a - b <= b]:
    add3(d21)
shapes3 = sorted(need3, key=lambda s: (sum(s), s))

S = {}   # shape -> dict bytes -> zmask ; plus arrays
def key(a): return np.packbits(a.ravel()).tobytes() + bytes([a.size % 251])

def lookup2(arr2, zs):
    # arr2: 2-D table (p+1,q+1); return zmask from two-block catalogue
    p, q = arr2.shape[0] - 1, arr2.shape[1] - 1
    if p < q: arr2 = arr2.T; p, q = q, p
    return S[(p, q, 0)][0].get(key(np.ascontiguousarray(arr2)[:, :, None]), 0)

def build(shape, j):
    d = sum(shape)
    full = zrange(d)
    if d == 0:
        A = np.array([[[[0]]], [[[1]]]], dtype=np.uint8)
        Z = [full & bound_ok_mask(0, 1, 0) & bound_ok_mask(1, 0, 0), full & bound_ok_mask(1, 1, 0) & bound_ok_mask(0, 0, 0)]
        return A, Z
    c = list(shape); c[j] -= 1; c = tuple(c)
    cd, cA, cZ = S[c]
    m = shape[j]
    sl = lambda a, lo, hi: np.take(a, range(lo, hi), axis=j + 1)
    if m >= 2:
        kl = [key(x) for x in sl(cA, 1, m)]
        ku = [key(x) for x in sl(cA, 0, m - 1)]
        grp = {}
        for i, k in enumerate(ku): grp.setdefault(k, []).append(i)
        pairs = [(i, iu) for i, k in enumerate(kl) for iu in grp.get(k, ())]
    else:
        pairs = [(i, iu) for i in range(len(cA)) for iu in range(len(cA))]
    top = cA.reshape(len(cA), -1)[:, -1]; bot = cA.reshape(len(cA), -1)[:, 0]
    keepA, keepZ = [], []
    for i, iu in pairs:
        zm = (cZ[i] >> int(top[iu] == 0)) & (cZ[iu] >> int(bot[i] == 0)) & full
        if zm:
            keepA.append((i, iu)); keepZ.append(zm)
    if not keepA:
        return np.zeros((0,) + tuple(x + 1 for x in shape), np.uint8), []
    li = np.array([p[0] for p in keepA]); ui = np.array([p[1] for p in keepA])
    A = np.concatenate([cA[li], sl(cA[ui], m - 1, m)], axis=j + 1)
    return A, keepZ

def slice_filter(shape, A, Z):
    u, v, w = shape
    if w == 0: return Z
    Z = list(Z)
    for j in range(3):
        sj = shape[j]
        for k in range(sj + 1):
            sl = np.take(A, k, axis=j + 1)           # (n, p+1, q+1)
            Am = np.moveaxis(A, j + 1, 1)             # (n, sj+1, p+1, q+1)
            below = Am[:, :k, 0, 0]                   # counts below k, others zero
            above = Am[:, k + 1:, -1, -1]             # counts above k, others maximal
            extra = (below == 0).sum(1) + (above == 0).sum(1)
            for i in range(len(Z)):
                if not Z[i]: continue
                zm = lookup2(sl[i], 0)
                Z[i] &= (zm >> int(extra[i]))
    return Z

def witness_filter(shape, A, Z, fams):
    d = sum(shape)
    Z = np.array(Z, dtype=np.int64)
    flat = A.transpose(0, 3, 2, 1).reshape(len(A), -1) if len(A) else A.reshape(0, 1)
    u, v, w = shape
    used = set()
    for k, cs, loc in sorted(fams, key=lambda f: -f[0]):
        live = Z != 0
        if not live.any(): break
        idx = [x + (u + 1) * (y + (v + 1) * z) for x, y, z in cs]
        sub = flat[:, idx]
        for c in (0, 1):
            mono = (sub == c).all(1) & live
            if mono.any():
                okm = bound_ok_mask(c, k, d)
                newZ = np.where(mono, Z & okm, Z)
                if (newZ != Z).any(): used.add(loc)
                Z = newZ
    stats['fam_used'] += len(used)
    return [int(z) for z in Z]

def run():
    log = open(os.path.join(OUT, 'induct.log'), 'w')
    for shape in shapes2 + shapes3:
        d = sum(shape)
        j = child3(shape) if shape[2] else child2(shape)
        A, Z = build(shape, j)
        cand = sum(bin(z).count('1') for z in Z)
        Z = slice_filter(shape, A, Z)
        Z = witness_filter(shape, A, Z, load_families(shape) if d else [])
        keep = [i for i, z in enumerate(Z) if z]
        A = A[keep]; Z = [Z[i] for i in keep]
        surv = sum(bin(z).count('1') for z in Z)
        stats['cand_pairs'] += cand; stats['surv_pairs'] += surv
        S[shape] = ({key(a): z for a, z in zip(A, Z)}, A, Z)
        print(shape, 'axis', j, 'cand', cand, 'surv', surv, 'tables', len(A), file=log, flush=True)
    print(stats, file=log, flush=True)
    res = {}
    for s in list(S):
        if sum(s) == 21:
            A, Z = S[s][1], S[s][2]
            res[s] = [(''.join(map(str, a.transpose(2, 1, 0).ravel())), z) for a, z in zip(A, Z)]
    pickle.dump(res, open(os.path.join(OUT, 'final21.pkl'), 'wb'))
    print('DONE', stats)

if __name__ == '__main__':
    run()

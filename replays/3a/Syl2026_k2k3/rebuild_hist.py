#!/usr/bin/env python3
"""Own rebuild of the cost histogram m_k(c) = #{r in Z/q^k : c_k(r) = c} for k = 2, 3.
   kappa(d) = min{a+b : a,b in M, a-b = d}; c_k(r) = min over lifts (d_0..d_{k-1}) in D^k
   with sum d_i q^i = r (mod q^k) of sum kappa(d_i).
   The carry-automaton form of c_k (Lemma 0 of the claimant's note) is used for the full
   rebuild; Lemma 0 is itself tested here against the definition on random residues
   (check_lemma0) before the full rebuild is trusted.
Usage: rebuild_hist.py k out.tsv
"""
import sys, random, time
from collections import Counter

G = [1971, 2016, 2100, 2628, 2688, 2800]
B = 26972
q = 27022
INF = 10 ** 9


def mask():
    ok = [False] * (B + 1); ok[0] = True
    for n in range(1, B + 1):
        for g in G:
            if n >= g and ok[n - g]:
                ok[n] = True; break
    return [n for n in range(B + 1) if ok[n]]


def kappa_table(M):
    kap = [INF] * (2 * B + 1)          # index d + B
    for a in M:
        for b in M:
            d = a - b + B
            s = a + b
            if s < kap[d]:
                kap[d] = s
    return kap


def make_kap(tab):
    def kap(d):
        if d < -B or d > B:
            return INF
        return tab[d + B]
    return kap


def check_lemma0(kap, k, trials, seed=1):
    """c_k(r) by the definition (enumerate lifts for k=2 exactly) vs automaton."""
    rnd = random.Random(seed)
    Dlist = [d for d in range(-B, B + 1) if kap(d) < INF]
    Q = q ** k
    def c_auto(r):
        digs = []
        t = r
        for _ in range(k):
            digs.append(t % q); t //= q
        best = INF
        for gs in range(2 ** k):
            g = [0] + [-((gs >> i) & 1) for i in range(k)]  # g[0]=0, g[1..k]
            tot = 0
            for i in range(k):
                tot += kap(digs[i] - g[i] + q * g[i + 1])
                if tot >= INF: break
            best = min(best, tot)
        return best
    if k == 2:
        def c_def(r):
            best = INF
            for d1 in Dlist:
                # d0 = r - d1*q mod q^2, representative in [-B,B] (unique since q^2 > 2B)
                d0 = (r - d1 * q) % Q
                if d0 > Q // 2: d0 -= Q
                s = kap(d0) + kap(d1)
                if s < best: best = s
            return best
    else:
        def c_def(r):  # k=3: enumerate d2, d1 in D (2.7e9) is too large; fix d2 and use k=2 structure
            best = INF
            for d2 in Dlist:
                rem = (r - d2 * q * q) % Q
                # need d0 + d1 q = rem mod q^3 with |d0|,|d1| <= B: d1 range determined mod q^2
                # enumerate d1 over D, d0 unique
                for d1 in Dlist:
                    d0 = (rem - d1 * q) % Q
                    if d0 > Q // 2: d0 -= Q
                    if -B <= d0 <= B:
                        s = kap(d0) + kap(d1) + kap(d2)
                        if s < best: best = s
            return best
    bad = 0
    for _ in range(trials):
        r = rnd.randrange(Q)
        if c_auto(r) != c_def(r): bad += 1
    return bad


def rebuild(kap, k):
    k0 = [kap(r0) for r0 in range(q)]          # kappa(r0)
    k1 = [kap(r0 - q) for r0 in range(q)]      # kappa(r0 - q)
    # A_{g1}(tail) vectors
    if k == 2:
        # tail = r1 ; A_{g1}(r1) = min_{g2} kap(r1 - g1 + q g2)
        tails = Counter()
        for r1 in range(q):
            A0 = min(kap(r1), kap(r1 - q))
            A1 = min(kap(r1 + 1), kap(r1 + 1 - q))
            tails[(A0, A1)] += 1
        pairs = tails
    else:
        # tail = (r1, r2); A_{g1} = min_{g2}(kap(r1 - g1 + q g2) + T_{g2}(r2)); T_{g2}(r2)=min_{g3} kap(r2 - g2 + q g3)
        U = Counter()
        for r1 in range(q):
            U[(kap(r1), kap(r1 - q), kap(r1 + 1), kap(r1 + 1 - q))] += 1   # (g1=0,g2=0),(g1=0,g2=-1),(g1=-1,g2=0),(g1=-1,g2=-1)
        T = Counter()
        for r2 in range(q):
            T[(min(kap(r2), kap(r2 - q)), min(kap(r2 + 1), kap(r2 + 1 - q)))] += 1   # (g2=0),(g2=-1)
        print('distinct r1 tuples', len(U), 'distinct r2 tuples', len(T), file=sys.stderr, flush=True)
        pairs = Counter()
        for (u00, u0m, um0, umm), cu in U.items():
            for (t0, tm), ct in T.items():
                A0 = min(u00 + t0, u0m + tm)
                A1 = min(um0 + t0, umm + tm)
                pairs[(A0, A1)] += cu * ct
        print('distinct (A0,A1)', len(pairs), file=sys.stderr, flush=True)
    # r0 histogram for each (A0, A1): min(k0[r0] + A0, k1[r0] + A1) ; depends on delta = A1 - A0
    W = Counter()
    for (A0, A1), mult in pairs.items():
        if A0 >= INF and A1 >= INF:
            raise SystemExit('residue not covered')
        if A0 >= INF: key = (A1, 'only1')
        elif A1 >= INF: key = (A0, 'only0')
        else: key = (A0, A1 - A0)
        W[key] += mult
    deltas = {key[1] for key in W}
    print('distinct delta keys', len(deltas), file=sys.stderr, flush=True)
    Hcache = {}
    def H(delta):
        if delta in Hcache: return Hcache[delta]
        if delta == 'only1': cnt = Counter(v for v in k1 if v < INF)
        elif delta == 'only0': cnt = Counter(v for v in k0 if v < INF)
        else: cnt = Counter(min(a, b + delta) for a, b in zip(k0, k1) if min(a, b + delta) < INF)
        Hcache[delta] = cnt
        return cnt
    hist = Counter()
    for (A, delta), mult in W.items():
        for c, m in H(delta).items():
            hist[A + c] += mult * m
    return hist


if __name__ == '__main__':
    k = int(sys.argv[1]); out = sys.argv[2]
    t0 = time.time()
    M = mask(); tab = kappa_table(M); kap = make_kap(tab)
    print('M', len(M), 'D', sum(1 for d in range(-B, B + 1) if kap(d) < INF), 'kappa built', round(time.time() - t0, 1), file=sys.stderr, flush=True)
    if len(sys.argv) > 3:
        bad = check_lemma0(kap, 2, int(sys.argv[3]))
        print('lemma0 k=2 mismatches vs definition:', bad, file=sys.stderr)
        bad = check_lemma0(kap, 3, int(sys.argv[4]) if len(sys.argv) > 4 else 3)
        print('lemma0 k=3 mismatches vs definition:', bad, file=sys.stderr)
    hist = rebuild(kap, k)
    assert sum(hist.values()) == q ** k, (sum(hist.values()), q ** k)
    with open(out, 'w') as f:
        f.write('# cost\tmultiplicity\n')
        for c in sorted(hist): f.write('%d\t%d\n' % (c, hist[c]))
    print('done', len(hist), 'costs', round(time.time() - t0, 1), 's', file=sys.stderr)

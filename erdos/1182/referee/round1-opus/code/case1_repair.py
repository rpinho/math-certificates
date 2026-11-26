"""Referee's corrected Case I certificate (producer + checker), Region C.

Bound used (referee derivation, REFEREE.md section c/d):
  For every blue symmetric Q with rows a, any t>0, s>0:
    L(a,Q) = V_{t,s}(a) - 10 Q03 log s - 5 KL(Q || B_{t,s}),
    V_{t,s}(a) = 9 sum a log a - 10 sum a log t + 5 log Z_s,  Z_s = sum_ij A_ij t_i t_j with A_03=A_30=s.
  Case I: Pr(E_I | K) <= (D+1) n^19 20^19 exp(n a0 log f(Q03/a0)),  f(p) = 1-(1-p)^10.
  a0 log f(q/a0) is decreasing in a0 and increasing in q.
  Partition Q03 in [0, qmax], qmax = min(max a0, max a3) on the box, into M equal intervals [q_k, q_k+1]:
    rate <= max_vertices V + max_k [ -10 log s * (q_k if s>=1 else q_k+1) + a0min log f(min(1, q_k+1/a0min)) ].
Producer part uses floats only to pick (t, s); the checker recomputes all in Arb (160 bits).
Usage: python -I case1_repair.py produce OUT.json | check CERT.json
"""
import sys, json
from fractions import Fraction
sys.path.insert(0, __import__("os").path.dirname(__file__))
import arbverify as V
from flint import arb, ctx

ctx.prec = 160
GRID = 10485760000
TS = 10**12
CAP = 4195352576
DELTA = 1572864000
M_INT = 64
CLAIM = -Fraction(1, 1000)


def arb_bound(lo, hi, T, S, M):
    """Rigorous upper bound for Case I rate over region C ∩ box, given tilt ints T and s int S."""
    boxes = V.region_parts("case1", lo, hi, GRID, DELTA)
    if not boxes:
        return None
    vs = []
    for b in boxes:
        vs += V.vertices(b[0], b[1], GRID)
    if any(x <= 0 for x in T) or S <= 0:
        raise V.Reject("nonpositive parameter")
    t = [arb(x) / TS for x in T]
    s = arb(S) / TS
    Z = arb(0)
    for i, j in V.BLUE:
        w = t[i] * t[j] * (1 if i == j else 2)
        if (i, j) == (0, 3):
            w = w * s
        Z += w
    G = arb(GRID)
    Vmax = None
    for p in vs:
        val = arb(0)
        for i in range(5):
            ai = arb(p[i]) / G
            val += 9 * V.xlogx(ai)
            if p[i]:
                val -= 10 * ai * t[i].log()
        val = V.up(val + 5 * Z.log())
        Vmax = val if Vmax is None else V._amax(Vmax, val)
    a0min = min(p[0] for p in vs)
    if a0min <= 0:
        raise V.Reject("a0min<=0")
    qmax = min(max(p[0] for p in vs), max(p[3] for p in vs))
    c = 10 * s.log()
    cpos = S >= TS
    best = None
    for k in range(M):
        qk = Fraction(qmax * k, M * GRID)
        qk1 = Fraction(qmax * (k + 1), M * GRID)
        qlin = qk if cpos else qk1
        lin = -c * (arb(qlin.numerator) / qlin.denominator)
        x = min(Fraction(1), qk1 / Fraction(a0min, GRID))
        if x == 0:
            occ = None  # log f(0) = -inf: interval [0,0] contributes nothing
            continue
        occ = (arb(a0min) / G) * V.f_occ(arb(x.numerator) / x.denominator).log()
        term = V.up(lin + occ)
        best = term if best is None else V._amax(best, term)
    return V.up(Vmax + best)


def choose_params(lo, hi):
    import numpy as np
    import rates_numeric as R
    boxes = V.region_parts("case1", lo, hi, GRID, DELTA)
    vs = []
    for b in boxes:
        vs += V.vertices(b[0], b[1], GRID)
    a = np.mean(np.array(vs, float), axis=0) / GRID
    a = np.maximum(a, 1e-9); a /= a.sum()
    val, s, Q = R.case1_exact(a)
    t = R.scale_ts_t(a, s)
    T = [max(1, int(round(x * TS))) for x in t]
    return T, max(1, int(round(s * TS))), val


def produce(out):
    import rates_numeric as R
    recs = []
    claim_arb = arb(CLAIM.numerator) / CLAIM.denominator
    stats = {"K": 0, "X": 0, "S": 0}
    worst = [None]

    def rec(lo, hi, depth):
        boxes = V.region_parts("case1", lo, hi, GRID, DELTA)
        if not boxes:
            recs.append(["X"]); stats["X"] += 1; return
        T, S, val = choose_params(lo, hi)
        b = arb_bound(lo, hi, T, S, M_INT)
        if b <= arb(claim_arb.lower()) or depth > 60:
            recs.append(["K", T, S, M_INT, float(b)]); stats["K"] += 1
            if worst[0] is None or float(b) > worst[0]:
                worst[0] = float(b)
            return
        # split longest side of tightened hull
        tl = [min(bb[0][i] for bb in boxes) for i in range(5)]
        th = [max(bb[1][i] for bb in boxes) for i in range(5)]
        i = max(range(5), key=lambda k: th[k] - tl[k])
        m = (tl[i] + th[i]) // 2
        if not lo[i] < m < hi[i]:
            m = (lo[i] + hi[i]) // 2
        recs.append(["S", i, m]); stats["S"] += 1
        h1 = list(hi); h1[i] = m
        l2 = list(lo); l2[i] = m
        rec(lo, h1, depth + 1)
        rec(l2, hi, depth + 1)
        if stats["K"] % 100 == 0:
            print(stats, worst[0], flush=True)

    rec([0] * 5, [CAP] * 5, 0)
    cert = {"format": "referee-case1s-1", "case": "case1s", "grid": GRID, "tilt_scale": TS,
            "root": [[0] * 5, [CAP] * 5], "claim": "-1/1000", "M": M_INT, "records": recs}
    json.dump(cert, open(out, "w"))
    print("PRODUCED", stats, "worst", worst[0])


def check(path, corrupt=None):
    cert = json.load(open(path))
    assert cert["grid"] == GRID and cert["root"] == [[0] * 5, [CAP] * 5]
    assert Fraction(CAP, GRID) == Fraction(4001, 10000) and Fraction(DELTA, GRID) == Fraction(3, 20)
    recs = cert["records"]
    if corrupt:
        recs = corrupt(recs)
    claim = arb(CLAIM.numerator) / CLAIM.denominator
    pos = [0]; st = {"K": 0, "X": 0, "S": 0, "max": None}

    def rec(lo, hi):
        if pos[0] >= len(recs):
            raise V.Reject("truncated")
        r = recs[pos[0]]; pos[0] += 1
        if r[0] == "S":
            _, i, m = r
            if not lo[i] < m < hi[i]:
                raise V.Reject("bad split")
            st["S"] += 1
            h1 = list(hi); h1[i] = m; l2 = list(lo); l2[i] = m
            rec(lo, h1); rec(l2, hi); return
        if r[0] == "X":
            if V.region_parts("case1", lo, hi, GRID, DELTA):
                raise V.Reject("X leaf nonempty")
            st["X"] += 1; return
        if r[0] != "K":
            raise V.Reject("unknown record")
        b = arb_bound(lo, hi, r[1], r[2], r[3])
        if b is None:
            st["K"] += 1; return
        if not b <= arb(claim.lower()):
            raise V.Reject("leaf bound %.15g > -1/1000 at %s %s" % (float(b), lo, hi))
        st["K"] += 1
        if st["max"] is None or float(b) > st["max"]:
            st["max"] = float(b)

    rec([0] * 5, [CAP] * 5)
    if pos[0] != len(recs):
        raise V.Reject("trailing records")
    return st


if __name__ == "__main__":
    if sys.argv[1] == "produce":
        produce(sys.argv[2])
    else:
        try:
            print("ACCEPT", check(sys.argv[2]))
        except V.Reject as e:
            print("REJECT", e)

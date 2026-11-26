"""Referee controls for the Arb verifiers. Usage: python -I controls.py DATA_DIR OUT_DIR"""
import sys, os, json, copy
from fractions import Fraction
sys.path.insert(0, os.path.dirname(__file__))
import arbverify as V
import case1_repair as C1
from flint import arb, ctx
import numpy as np
import rates_numeric as R

ctx.prec = 160
data, out = sys.argv[1], sys.argv[2]
G = 10485760000
log = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); log.append(s)


# ---- 1. positive naive witness, rigorous lower bound on the naive rate ----
a_f = np.array([0.4, 0.000138839258, 0.4, 0.18711729, 0.0])
a_f[4] = 1 - a_f[:4].sum()
den = 10**9
a = [Fraction(round(x * den), den) for x in a_f[:4]]
a.append(1 - sum(a))
assert max(a) <= Fraction(2, 5) and min(a) > 0
t = R.scale_t(np.array([float(x) for x in a]))
Qf = R.A * np.outer(t, t) / (t @ R.A @ t)
off = {}
for i, j in R.PAIRS:
    off[(i, j)] = Fraction(round(Qf[i, j] * 10**15), 10**15)
Q = [[Fraction(0)] * 5 for _ in range(5)]
for (i, j), v in off.items():
    Q[i][j] = Q[j][i] = v
for i in range(5):
    Q[i][i] = a[i] - sum(Q[i][j] for j in range(5) if j != i)
    assert Q[i][i] > 0
# exact feasibility
assert all(sum(Q[i]) == a[i] for i in range(5)) and sum(map(sum, Q)) == 1
for i in range(5):
    for j in range(5):
        if (j - i) % 5 in (1, 4):
            assert Q[i][j] == 0
fr = lambda x: arb(x.numerator) / x.denominator
Lw = 9 * sum(V.xlogx(fr(x)) for x in a) - 5 * sum(V.xlogx(fr(Q[i][j])) for i in range(5) for j in range(5))
say("1. naive witness a=", [str(x) for x in a], " cap 2/5 profile; rigorous L(a,Q) in", Lw.str(15),
    "lower bound", float(arb(Lw.lower())), "positive:", bool(arb(Lw.lower()) > 0),
    "a in region C:", a[0] - a[3] >= Fraction(3, 20) and a[2] - a[3] >= Fraction(3, 20) and a[3] >= a[4])
# the naive leaf test must reject a box containing it, for any tilt: use optimal float tilt
k = [int(x * G) for x in a[:4]]
k.append(G - sum(k))
lo = [max(0, x - 2000) for x in k]; hi = [x + 2000 for x in k]
T = [int(round(x / t.sum() * 10**12)) for x in t]
cert = {"format": 1, "case": "case1", "root": [lo, hi], "grid": G, "tilt_scale": 10**12, "claim": -10**9,
        "records": [["N", T, 0, -10**9]]}
try:
    boxes = V.region_parts("case1", lo, hi, G, 1572864000)
    cx = V.Ctx(G, 10**12)
    V.check_leaf(["N", T, 0, -10**9], boxes, cx, "case1", arb(-1) / 1000)
    say("   naive-leaf control: ACCEPTED (BAD)")
except V.Reject as e:
    say("   naive-leaf control at witness box: REJECT (good):", str(e)[:80])

# ---- 2. corrupted certificates must be rejected ----
def load(c):
    return json.load(open(os.path.join(data, "cert_%s.json" % c)))


def first(recs, kind):
    return next(i for i, r in enumerate(recs) if r[0] == kind)


def tightest(recs, kind, idx):
    return max((i for i, r in enumerate(recs) if r[0] == kind), key=lambda i: recs[i][idx])


def mut_tilt(recs):
    r = copy.deepcopy(recs); i = tightest(r, "N", 2); r[i][1] = [10**12] * 5; return r


def mut_tilt_small(recs):
    r = copy.deepcopy(recs); i = tightest(r, "N", 2); r[i][1] = [x + (x // 50) * (k % 2) for k, x in enumerate(r[i][1])]; return r


def mut_trunc(recs):
    return recs[:-1]


def mut_trail(recs):
    return recs + [["X"]]


def mut_split(recs):
    r = copy.deepcopy(recs); i = first(r, "S"); r[i] = ["S", r[i][1], 0]; return r


def mut_X(recs):
    r = copy.deepcopy(recs); i = first(r, "N"); r[i] = ["X"]; return r


def mut_c2_h02(recs):
    r = copy.deepcopy(recs); i = first(r, "C"); r[i][3][0] = r[i][3][0] // 2; return r


def mut_c2_h24(recs):
    r = copy.deepcopy(recs); i = first(r, "C"); r[i][3][1] = r[i][3][1] * 3; return r


def mut_c2_u(recs):
    r = copy.deepcopy(recs); i = first(r, "C"); r[i][3][2] = 999999999999; return r


tests = [("naive_ab", "tilt->uniform", mut_tilt), ("naive_ab", "tilt perturbed 2%", mut_tilt_small),
         ("naive_ab", "truncated", mut_trunc), ("naive_ab", "trailing record", mut_trail),
         ("naive_ab", "split point 0", mut_split), ("naive_ab", "N leaf -> X", mut_X),
         ("case2", "tilt->uniform", mut_tilt), ("case2", "h02 halved", mut_c2_h02),
         ("case2", "h24 tripled", mut_c2_h24), ("case2", "u->1-1e-12", mut_c2_u),
         ("case2", "truncated", mut_trunc)]
say("2. corrupted producer certificates (expect REJECT):")
for c, name, fn in tests:
    try:
        V.run(load(c), corrupt=fn); say("   ", c, name, "ACCEPT  <-- control FAILED")
    except V.Reject as e:
        say("   ", c, name, "REJECT:", str(e)[:90])
    except Exception as e:
        say("   ", c, name, "REJECT (exception):", type(e).__name__, str(e)[:60])

say("3. referee Case I certificate corruptions (expect REJECT):")
def k_s(recs):
    r = copy.deepcopy(recs); i = tightest(r, "K", 4); r[i][2] = 10**12; return r
def k_t(recs):
    r = copy.deepcopy(recs); i = tightest(r, "K", 4); r[i][1] = [10**12] * 5; return r
def k_M(recs):
    r = copy.deepcopy(recs)
    for i, x in enumerate(r):
        if x[0] == "K": r[i][3] = 1
    return r
for name, fn in [("s->1", k_s), ("tilt->uniform", k_t), ("M->1 everywhere", k_M), ("truncated", mut_trunc), ("trailing", mut_trail)]:
    try:
        C1.check(os.path.join(out, "cert_case1_referee.json"), corrupt=fn); say("   case1s", name, "ACCEPT  <-- control FAILED?")
    except V.Reject as e:
        say("   case1s", name, "REJECT:", str(e)[:90])
    except Exception as e:
        say("   case1s", name, "REJECT (exception):", type(e).__name__, str(e)[:60])

# ---- 4. producer Case I direction counterexample ----
c1 = load("case1")
say("4. producer Case I occupancy leaves: cutoff vs B03, and a type violating the leaf's near-cell inequality")
cx = V.Ctx(G, 10**12)
recs = c1["records"]; pos = [0]; found = []
def walk(lo, hi):
    r = recs[pos[0]]; pos[0] += 1
    if r[0] == "S":
        h1 = list(hi); h1[r[1]] = r[2]; l2 = list(lo); l2[r[1]] = r[2]
        walk(lo, h1); walk(l2, hi); return
    if r[0] == "C":
        found.append((lo, hi, r))
walk([0] * 5, [4195352576] * 5)
nbelow = 0
viol = 0
worst_true = -1
for lo, hi, r in found:
    t_, Z, B = cx.tilt(r[1])
    q = r[3][0] / G
    if q < float(B[(0, 3)].mid()): nbelow += 1
    boxes = V.region_parts("case1", lo, hi, G, 1572864000)
    vs = []
    for b in boxes: vs += V.vertices(b[0], b[1], G)
    ac = np.mean(np.array(vs, float), axis=0) / G
    a0min = min(p[0] for p in vs) / G
    # producer near-cell claim on Q03 >= q: L + occ <= U + a0min log f(q/a0min)
    claimed_near = r[2] / 1e12 + a0min * np.log(R.f(min(1, q / a0min)))
    # actual: max-entropy type at centroid (Q03 = B03-like >= q) has L = naive rate, occ = a0 log f(Q03/a0)
    nv, tt, Qm = R.naive_exact(ac)
    actual = nv + ac[0] * np.log(R.f(Qm[0, 3] / ac[0]))
    if Qm[0, 3] >= q and actual > claimed_near + 1e-9:
        viol += 1
    worst_true = max(worst_true, R.case1_exact(ac)[0])
say("   C leaves:", len(found), " with q* < B03:", nbelow, " leaves where the max-entropy type at the centroid has Q03 >= q* and"
    " true L+occ exceeds the leaf's claimed near bound:", viol)
say("   max over C-leaf centroids of the TRUE Case I rate (numeric):", worst_true)
json.dump(log, open(os.path.join(out, "controls.json"), "w"), indent=1)

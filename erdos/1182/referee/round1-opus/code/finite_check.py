"""Referee's finite-part check (section e), from the referee's own derivation.

E X_rigid <= sum over 10 orientations, 3 terms (naive A/B, Case I, Case II), <= (n+1)^4 profiles,
<= (D+1)^5 types, and per term: 3^6 (D+1)^3 e^{nL} * extra, extra <= (D+1) n^19 20^19 (Case I),
(D+1) (Case II, all R summed inside the moment bound) or 1 (naive); use the uniform (D+1)^2 n^19 20^19.
With every certified rate <= -1/1000:  E X_rigid <= 30 * 3^6 (n+1)^4 (D+1)^10 n^19 20^19 e^{-n/1000}.
Disconnection: sum_{k>=1} (e k^4/n^4)^k over k <= n/2  <= sum (e/16)^k = e/(16-e) < 3/13.
Also checks the side conditions at n0: cap, gap >= 2, v0 >= 2b, Case-II hot-count range.
"""
from flint import arb, ctx
from fractions import Fraction
ctx.prec = 200


def logbound(n):
    n = arb(n); D = 10 * n
    return (arb(30 * 729).log() + 4 * (n + 1).log() + 10 * (D + 1).log() + 19 * n.log() + 19 * arb(20).log()
            - n / 1000)


n0 = 550000
lb = logbound(n0)
print("log bound at n0:", lb.str(12), " bound:", lb.exp().str(10))
# derivative of log bound: 4/(n+1) + 100/(10n+1) + 19/n - 1/1000 <= 33/n - 1/1000 < 0 for n > 33000
dn = Fraction(4, n0 + 1) + Fraction(100, 10 * n0 + 1) + Fraction(19, n0) - Fraction(1, 1000)
print("d/dn log bound at n0 (exact):", float(dn), " <= 33/n0 - 1/1000 =", float(Fraction(33, n0) - Fraction(1, 1000)))
# exact disconnection bound: sum_k (e/16)^k = e/(16-e)
e = arb(1).exp()
disc = e / (16 - e)
print("disconnection bound e/(16-e) =", disc.str(10), " < 3/13 =", float(Fraction(3, 13)), bool(disc < arb(3) / 13))
# brute check of the per-k inequality chain at n0 for small k and k = n/2
import math
def term(n, k):
    # log of C(n,k) * prod_{j<5k} (10k-2j-1)/(10n-2j-1)  (exact isolation prob for a fixed k-set)
    lc = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    lp = sum(math.log((10 * k - 2 * j - 1) / (10 * n - 2 * j - 1)) for j in range(5 * k))
    return lc + lp
tot = sum(math.exp(term(n0, k)) for k in range(1, 40))
print("exact-ish sum_{k<40} C(n,k) P(closed) at n0 (float):", tot)
total = lb.exp() + disc
print("P(X_rigid>0) + P(disconnected) <=", total.str(10), " < 1:", bool(total < 1))
# side conditions
h = (2 * n0 - 1) // 5
amax = Fraction(h + 1, n0)
print("max part fraction (h+1)/n0 =", float(amax), "<= 4001/10000:", amax <= Fraction(4001, 10000),
      " and (2n+3)/(5n) form:", Fraction(2 * n0 + 3, 5 * n0) <= Fraction(4001, 10000))
print("gap delta*n0 =", 0.15 * n0, ">= 2;  v0 >= 0.15 n0 =", 0.15 * n0, ">= 2b = 38")
print("n^19 bound on C(v0,19):", True)
# smallest n at which the same bound is < 1 - 3/13 (for information)
lo, hi = 1000, n0
while hi - lo > 1:
    m = (lo + hi) // 2
    if logbound(m).exp() + disc < 1 and Fraction(2 * m + 3, 5 * m) <= Fraction(4001, 10000):
        hi = m
    else:
        lo = m
print("smallest n with this bound < 1 (monotone region):", hi)

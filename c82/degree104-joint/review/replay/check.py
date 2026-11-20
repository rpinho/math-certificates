#!/usr/bin/env python3
"""Clean-room interval checker for a C82 (Zhang-Zagier essential minimum) certificate
in Doche's limit-point construction.

Written by the referee from the live 82a definition and Doche (2001) only.
Dependencies: Python standard library + python-flint (FLINT/Arb).  No floating point:
all real numbers are exact integers/Fractions or Arb balls; numbers are printed as strings.

Quantities (natural logs, T(z) = z(1-z), e(t) = exp(2 pi i t)):
  Q = prod R_j^m_j (R_j monic integer), D = sum m_j deg R_j,
  A^(1/b) = prod S_i^q_i (S_i nonzero integer, q_i >= 0 rational), a = sum q_i deg S_i < D,
  H = (1/D) sum_j m_j log M(R_j o T)
  g(t) = (1/D) [ sum_i q_i log|S_i(T(e(t)))| - sum_j m_j log|R_j(T(e(t)))| ]
  J = int_0^1 max(0, g(t)) dt = 2 int_0^(1/2) max(0, g(t)) dt   (g(t) = g(1-t): real coefficients)
  B = H + J.

H: every root of R_j o T is enclosed by FLINT's rigorous complex root isolation;
   log M = log|lc| + sum log max(1, |rho|) evaluated in ball arithmetic.
J: Arb's rigorous integrator (acb_calc_integrate) applied to f = max(0, g).  g is written in
   root form g(t) = c + sum_k w_k log|T(e(t)) - s_k| over the (isolated) roots s_k of the S_i
   and R_j.  For analytic=True (ellipse bounds) the integrand returns the analytic
   continuation G(t) = c + sum_k (w_k/2) log((T(z)-s_k)(T(1/z)-conj(s_k))), z = e(t), if
   Re G > 0 on the whole ball (then f = G on the real points), 0 if Re G < 0 on the whole ball
   (then f = 0 there), and a non-finite ball otherwise.  For analytic=False it returns a
   ball containing max(0, g) on the real points of the input ball, with log|.| -> -inf
   handled by one-sided bounds (numerator zeros on the circle, e.g. from S = X, X - 1).
"""
import sys
import json
import re
import hashlib
from fractions import Fraction
from flint import fmpz_poly, arb, acb, ctx

PREC = 192          # working precision of the integrator and of all ball arithmetic (bits)
ROOT_PREC = 256     # precision for root isolation
T_POLY = fmpz_poly([0, 1, -1])   # T(X) = X - X^2
DEFAULT_TARGET = "0.2519694759"


class Reject(Exception):
    pass


# ---------------------------------------------------------------- parsing / hypotheses
_RAT = re.compile(r"^(0|[1-9][0-9]*)(/[1-9][0-9]*)?$")


def parse_rational(v):
    if isinstance(v, bool):
        raise Reject("exponent is a bool")
    if isinstance(v, int):
        if v < 0:
            raise Reject("negative exponent")
        return Fraction(v)
    if not isinstance(v, str) or not _RAT.match(v):
        raise Reject("exponent %r is not a nonnegative integer or p/q string" % (v,))
    return Fraction(v)


def parse_coeffs(lst, what):
    if not isinstance(lst, list) or len(lst) == 0:
        raise Reject("%s: coefficient list missing" % what)
    for x in lst:
        if isinstance(x, bool) or not isinstance(x, int):
            raise Reject("%s: non-integer coefficient %r" % (what, x))
    return fmpz_poly(lst[::-1])      # JSON lists are highest degree first


def compose_T(P):
    r = fmpz_poly([0])
    for co in reversed(P.coeffs()):
        r = r * T_POLY + co
    return r


def load_certificate(cert):
    dens, nums = [], []
    for d in cert["denominator"]:
        R = parse_coeffs(d["coeffs"], d.get("name", "?"))
        m = d["multiplicity"]
        if isinstance(m, bool) or not isinstance(m, int) or m <= 0:
            raise Reject("denominator %s: multiplicity must be a positive integer" % d.get("name"))
        if R.degree() < 1:
            raise Reject("denominator %s is constant" % d.get("name"))
        if R.leading_coefficient() != 1:
            raise Reject("denominator %s is not monic" % d.get("name"))
        dens.append((d.get("name", "?"), R, m))
    for n in cert["numerator"]:
        S = parse_coeffs(n["coeffs"], n.get("name", "?"))
        q = parse_rational(n["q_rational"])
        if S.is_zero():
            raise Reject("numerator %s is zero" % n.get("name"))
        if q == 0:
            continue                      # inactive factor
        nums.append((n.get("name", "?"), S, q))
    if not dens:
        raise Reject("no denominator")
    D = sum(m * R.degree() for _, R, m in dens)
    a = sum(q * S.degree() for _, S, q in nums)
    if not a < D:
        raise Reject("degree condition fails: a = %s >= D = %s" % (a, D))
    pairs = 0
    for nn, S, q in nums:
        for dn, R, m in dens:
            if S.gcd(R).degree() != 0:
                raise Reject("gcd(%s, %s) is nonconstant" % (nn, dn))
            pairs += 1
    return dens, nums, D, a, pairs


# ---------------------------------------------------------------- ball helpers
def exact_fraction(x):
    """exact value of an exact (radius 0) arb as a Fraction"""
    man, exp = x.man_exp()
    man, exp = int(man), int(exp)
    return Fraction(man) * (Fraction(2) ** exp)


def upper_fraction(x):
    return exact_fraction(x.upper())


def lower_fraction(x):
    return exact_fraction(x.lower())


def dec_up(F, digits):
    s = 10 ** digits
    n = -((-F.numerator * s) // F.denominator)
    return _dec(n, digits)


def dec_down(F, digits):
    s = 10 ** digits
    n = (F.numerator * s) // F.denominator
    return _dec(n, digits)


def _dec(n, digits):
    sign = "-" if n < 0 else ""
    n = abs(n)
    ip, fp = divmod(n, 10 ** digits)
    return "%s%d.%s" % (sign, ip, str(fp).rjust(digits, "0"))


def rat_arb(F):
    return arb(F.numerator) / arb(F.denominator)


NAN = arb(0).log()      # Arb returns nan for log(0); used as the non-finite marker


# ---------------------------------------------------------------- H
def log_mahler_composed(R):
    """rigorous enclosure of log M(R o T)"""
    P = compose_T(R)
    roots = P.complex_roots()
    if sum(e for _, e in roots) != P.degree():
        raise Reject("root isolation incomplete")
    s = abs(arb(P.leading_coefficient())).log()
    undecided = 0
    for r, e in roots:
        m = abs(r)
        if m > 1:
            s += e * m.log()
        elif m < 1:
            pass
        else:                             # cannot decide: enclose log max(1,|r|) in [0, log upper]
            undecided += 1
            hi = m.upper()
            s += e * (arb(0).union(hi.log()) if hi > 1 else arb(0))
    rec = fmpz_poly(P.coeffs()[::-1])
    circle = P.gcd(rec).degree()          # >0 iff P has a root on |z|=1 (or a reciprocal pair)
    return s, undecided, circle


# ---------------------------------------------------------------- g in root form
class RootForm:
    def __init__(self, dens, nums, D):
        self.groups = []                  # (weight arb, [(root acb, mult)], is_numerator)
        c = arb(0)
        for _, S, q in nums:
            w = rat_arb(q / D)
            c += w * abs(arb(S.leading_coefficient())).log()
            rts = S.complex_roots() if S.degree() > 0 else []
            if sum(e for _, e in rts) != S.degree():
                raise Reject("root isolation incomplete")
            self.groups.append((w, rts, True))
        for _, R, m in dens:
            w = rat_arb(Fraction(m, D))
            rts = R.complex_roots()
            if sum(e for _, e in rts) != R.degree():
                raise Reject("root isolation incomplete")
            self.groups.append((-w, rts, False))
        self.c = c
        self.nroots = sum(len(r) for _, r, _ in self.groups)

    def analytic(self, t):
        """analytic continuation G(t); non-finite if a log touches its branch cut"""
        z = acb(2 * t).exp_pi_i()
        zi = acb(-2 * t).exp_pi_i()
        Tz = z - z * z
        Tzi = zi - zi * zi
        G = acb(self.c)
        for w, rts, _ in self.groups:
            s = acb(0)
            for r, e in rts:
                p = (Tz - r) * (Tzi - r.conjugate())
                L = p.log(analytic=True)
                s += e * L if e != 1 else L
            G += (w / 2) * s
        return G

    def real_bounds(self, t):
        """ball [lo, hi] for g on the real points of the ball t; lo may be None (= -inf)"""
        tr = acb(t.real)
        z = acb(2 * tr).exp_pi_i()
        Tz = z - z * z
        tot = arb(self.c)
        lo_unbounded = False
        for w, rts, is_num in self.groups:
            s = arb(0)
            for r, e in rts:
                d = abs(Tz - r)
                if d > 0:
                    L = d.log()
                elif is_num:                    # positive weight: only the upper side is needed
                    lo_unbounded = True
                    up = d.upper()
                    if not up > 0:
                        return None, None
                    L = up.log()
                else:                           # denominator root touched: g unbounded above
                    return None, None
                s += e * L if e != 1 else L
            tot += w * s
        if lo_unbounded:
            return None, tot.upper()
        return tot.lower(), tot.upper()


def integrand_factory(rf, stats):
    zero = acb(0)
    nan = acb(NAN)

    def f(t, analytic):
        stats[0] += 1
        if stats[0] % 50000 == 0:
            sys.stderr.write("evals %d\n" % stats[0])
            sys.stderr.flush()
        if analytic:
            G = rf.analytic(t)
            if not G.is_finite():
                return nan
            gr = G.real
            if gr < 0:
                return zero
            if gr > 0:
                return G
            return nan
        lo, hi = rf.real_bounds(t)
        if hi is None:
            return nan
        if hi <= 0:
            return zero
        if lo is None or not lo > 0:
            return acb(arb(0).union(hi))
        return acb(lo.union(hi))
    return f


TOL_BITS = [60]


def compute_B(dens, nums, D, verbose=True):
    ctx.prec = ROOT_PREC
    H = arb(0)
    undecided_total = 0
    circle_den = 0
    for name, R, m in dens:
        lm, und, circ = log_mahler_composed(R)
        undecided_total += und
        circle_den += circ
        H += rat_arb(Fraction(m, D)) * lm
    rf = RootForm(dens, nums, D)
    ctx.prec = PREC
    stats = [0]
    f = integrand_factory(rf, stats)
    I = acb.integral(f, acb(0), acb(1) / 2, abs_tol=arb(2) ** -TOL_BITS[0], rel_tol=arb(2) ** -(TOL_BITS[0] - 10),
                     eval_limit=4000000, depth_limit=400)
    if not I.imag.contains(0):
        raise Reject("imaginary part of the integral does not contain 0")
    J = 2 * I.real
    B = H + J
    info = {"H": H, "J": J, "B": B, "evals": stats[0], "undecided_roots": undecided_total,
            "denominator_circle_gcd_degree": circle_den, "w_roots": rf.nroots}
    return info


def circle_zeros_of_numerators(nums):
    out = []
    for name, S, q in nums:
        P = compose_T(S)
        g = P.gcd(fmpz_poly(P.coeffs()[::-1]))
        if g.degree() > 0:
            out.append((name, str(g)))
    return out


def run(cert, target_str, label):
    target = Fraction(target_str)
    dens, nums, D, a, pairs = load_certificate(cert)
    print("[%s] hypotheses: %d monic integer denominators, %d active integer numerators" % (label, len(dens), len(nums)))
    print("[%s] D = %d ; a = %s ; a/D < 1 exactly: %s ; active gcd pairs checked coprime: %d"
          % (label, D, a, a < D, pairs))
    print("[%s] numerators with zeros of S o T on |z|=1 (gcd with reciprocal): %s" % (label, circle_zeros_of_numerators(nums)))
    info = compute_B(dens, nums, D)
    B = info["B"]
    lo, hi = lower_fraction(B), upper_fraction(B)
    print("[%s] denominator R o T: undecided |root|=1 cases %d ; gcd(P,P*) degree sum %d"
          % (label, info["undecided_roots"], info["denominator_circle_gcd_degree"]))
    print("[%s] H in [%s, %s]" % (label, dec_down(lower_fraction(info["H"]), 25), dec_up(upper_fraction(info["H"]), 25)))
    print("[%s] J in [%s, %s]" % (label, dec_down(lower_fraction(info["J"]), 25), dec_up(upper_fraction(info["J"]), 25)))
    print("[%s] B in [%s, %s]   (integrand evaluations %d, roots in w-plane %d, prec %d)"
          % (label, dec_down(lo, 25), dec_up(hi, 25), info["evals"], info["w_roots"], PREC))
    ok = hi < target
    print("[%s] upper endpoint < %s : %s" % (label, target_str, ok))
    print("[%s] %s" % (label, "PASS" if ok else "FAIL"))
    return ok, lo, hi


# ---------------------------------------------------------------- controls
def analytic_controls():
    results = []
    ctx.prec = PREC
    cases = [
        ("A: R=X-3, no numerator, B = log 3", {"denominator": [{"name": "R", "coeffs": [1, -3], "multiplicity": 1}], "numerator": []},
         arb(3).log()),
        ("B: R=X-3, S=7 (q=1), g>0 everywhere, B = log 7", {"denominator": [{"name": "R", "coeffs": [1, -3], "multiplicity": 1}],
                                                             "numerator": [{"name": "S", "coeffs": [7], "q_rational": "1"}]},
         arb(7).log()),
    ]
    # C: R=X-3, S=2: g = log 2 - log|T(e)-3|, |T(e^{i th})-3|^2 = 12 cos^2 th - 8 cos th + 5,
    # g > 0 exactly for 1/6 < cos th < 1/2.  B = log 3 + (1/pi) int_{pi/3}^{acos(1/6)} (log 2 - log(12c^2-8c+5)/2) dth
    def hC(x, analytic):
        cth = x.cos()
        v = 12 * cth * cth - 8 * cth + 5
        return arb(2).log() - v.log(analytic=analytic) / 2
    ctx.prec = PREC
    IC = acb.integral(hC, acb(arb.pi() / 3), acb(arb(1) / 6).acos())
    BC = arb(3).log() + IC.real / arb.pi()
    cases.append(("C: R=X-3, S=2 (q=1), two sign changes, B = log3 + independent 1-D integral",
                  {"denominator": [{"name": "R", "coeffs": [1, -3], "multiplicity": 1}],
                   "numerator": [{"name": "S", "coeffs": [2], "q_rational": "1"}]}, BC))
    for name, cert, exact in cases:
        dens, nums, D, a, pairs = load_certificate(cert)
        info = compute_B(dens, nums, D)
        B = info["B"]
        ok = B.overlaps(exact) and upper_fraction(B) - lower_fraction(B) < Fraction(1, 10 ** 15)
        print("[control analytic %s] computed B in [%s, %s]; known %s; consistent and tight: %s"
              % (name, dec_down(lower_fraction(B), 20), dec_up(upper_fraction(B), 20), exact.str(20), ok))
        results.append(ok)
    return all(results)


def rejection_controls(cert):
    out = []
    def mutate(fn):
        c = json.loads(json.dumps(cert))
        fn(c)
        return c
    cases = [
        ("non-monic denominator", lambda c: c["denominator"][0]["coeffs"].__setitem__(0, 2)),
        ("numerator equal to a denominator (gcd)", lambda c: c["numerator"].append(
            {"name": "dup", "coeffs": list(c["denominator"][0]["coeffs"]), "q_rational": "1/1048576"})),
        ("P1 exponent doubled (a >= D)", lambda c: c["numerator"][0].__setitem__(
            "q_rational", str(2 * Fraction(c["numerator"][0]["q_rational"])))),
        ("decimal exponent string", lambda c: c["numerator"][1].__setitem__("q_rational", ".".join(["0", "5"]))),
        ("zero multiplicity", lambda c: c["denominator"][1].__setitem__("multiplicity", 0)),
        ("non-integer coefficient", lambda c: c["numerator"][5]["coeffs"].__setitem__(3, "3")),
    ]
    for name, fn in cases:
        c = mutate(fn)
        try:
            load_certificate(c)
            print("[control reject] %s: NOT rejected" % name)
            out.append(False)
        except Reject as e:
            print("[control reject] %s: rejected (%s)" % (name, e))
            out.append(True)
    return all(out)


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: check.py CERT.json [--target X] [--control analytic|reject|coeff|exponent]")
        sys.exit(2)
    path = args[0]
    target = DEFAULT_TARGET
    control = None
    if "--target" in args:
        target = args[args.index("--target") + 1]
    if "--tol" in args:
        TOL_BITS[0] = int(args[args.index("--tol") + 1])
    print("integrator abs_tol 2^-%d, rel_tol 2^-%d" % (TOL_BITS[0], TOL_BITS[0] - 10))
    if "--control" in args:
        control = args[args.index("--control") + 1]
    raw = open(path, "rb").read()
    print("certificate sha256 %s" % hashlib.sha256(raw).hexdigest())
    cert = json.loads(raw)
    if control is None:
        try:
            ok, lo, hi = run(cert, target, "main")
        except Reject as e:
            print("[main] REJECTED: %s" % e)
            print("[main] FAIL")
            sys.exit(1)
        sys.exit(0 if ok else 1)
    if control == "analytic":
        ok = analytic_controls()
    elif control == "reject":
        ok = rejection_controls(cert)
    elif control in ("coeff", "exponent"):
        c = json.loads(json.dumps(cert))
        if control == "coeff":
            c["denominator"][0]["coeffs"][-1] += 1          # constant term of the first denominator + 1
            desc = "constant coefficient of denominator 0 increased by 1"
        else:
            last = c["numerator"][-1]
            last["q_rational"] = str(2 * Fraction(last["q_rational"]))
            desc = "exponent of the last numerator (%s) doubled" % last["name"]
        print("[control %s] %s" % (control, desc))
        try:
            okp, lo, hi = run(c, target, "control " + control)
            ref_lo, ref_hi = Fraction(args[args.index("--ref-lo") + 1]), Fraction(args[args.index("--ref-hi") + 1])
            changed = hi < ref_lo or lo > ref_hi
            print("[control %s] enclosure disjoint from the unperturbed one: %s" % (control, changed))
            ok = changed
        except Reject as e:
            print("[control %s] rejected: %s" % (control, e))
            ok = True
    else:
        raise SystemExit("unknown control")
    print("[control %s] %s" % (control, "OK" if ok else "CONTROL FAILED"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

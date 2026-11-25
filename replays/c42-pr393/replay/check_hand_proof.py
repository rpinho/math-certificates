#!/usr/bin/env python3
"""Exact fractions.Fraction audit of Section 4.1 (one-box hand proof for q = 5001/10000)."""
from fractions import Fraction
import json

def F(*args):
    return Fraction(*args)

checks = []
def check(name, lhs, op, rhs, note=""):
    if op == "<":
        ok = lhs < rhs
    elif op == "<=":
        ok = lhs <= rhs
    elif op == ">":
        ok = lhs > rhs
    elif op == ">=":
        ok = lhs >= rhs
    elif op == "==":
        ok = lhs == rhs
    else:
        raise ValueError(op)
    checks.append({
        "name": name,
        "ok": ok,
        "op": op,
        "lhs_float": float(lhs),
        "rhs_float": float(rhs),
        "lhs_exact": str(lhs),
        "rhs_exact": str(rhs),
        "note": note,
    })
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {float(lhs):.12g} {op} {float(rhs):.12g}  ({note})")
    return ok

q = F("5001/10000")
c = F("9657/10000")
r_lo = F("7071/10000")
r_hi = F("7072/10000")

# 1. r bounds: r = 1/sqrt(2), so r^2 = 1/2
check("r_lo^2 < 1/2", r_lo**2, "<", F(1, 2), "0.7071 < r")
check("r_hi^2 > 1/2", r_hi**2, ">", F(1, 2), "r < 0.7072")

# 2. Preconditions for q = 0.5001, c = 0.9657
# Precondition 1: q < 2*c*sqrt(1-c^2) <=> q^2 < 4*c^2*(1-c^2)
check("c-precondition (q^2 < 4 c^2 (1-c^2))", q**2, "<", 4 * c**2 * (1 - c**2), "q < 2c sqrt(1-c^2)")
check("c > r_hi", c, ">", r_hi, "c > r")
# Precondition 2: r + sqrt(xi) + 1/4 <= 1 <=> sqrt(xi) <= 3/4 - r
# Sufficient: sqrt_xi_hi <= 3/4 - r_hi
xi = q**2 - F(1, 4)
check("xi == 0.00010001", xi, "==", F("10001/100000000"), "exact xi")
sqrt_xi_hi = F("1001/100000")  # 0.01001
check("xi < 0.01001^2", xi, "<", sqrt_xi_hi**2, "sqrt(xi) < 0.01001")
check("index precondition (r_hi + 0.01001 + 1/4 <= 1)", r_hi + sqrt_xi_hi + F(1, 4), "<=", F(1), "r+sqrt(xi)+1/4 <= 1")

# 3. t, s, I
# t <= (q - 1/2)/r < (q - 1/2)/r_lo
t_max_hi = (q - F(1, 2)) / r_lo
t_claim = F("142/1000000")  # 0.000142
check("t < 0.000142", t_max_hi, "<", t_claim, "(q-1/2)/r_lo < 0.000142")

s_hi = r_hi + t_claim
s_claim = F("708/1000")  # 0.708
check("s < 0.708", s_hi, "<", s_claim, "r_hi + 0.000142 < 0.708")

I_hi = t_claim / (1 - r_hi)
I_claim = F("49/100000")  # 0.00049
check("I < 0.00049", I_hi, "<", I_claim, "t_claim/(1-r_hi) < 0.00049")

# 4. b <= r*I + sqrt(2*xi*v^2 + 2*t*v) with v_+ = 0.708
v_init = s_claim  # 0.708
b_claim = F("18/1000")  # 0.018
# Check r_hi*I_claim + sqrt(2*xi*v_init^2 + 2*t_claim*v_init) < 0.018
# i.e. 2*xi*v_init^2 + 2*t_claim*v_init < (0.018 - r_hi*I_claim)^2
rem_b = b_claim - r_hi * I_claim
check("rem_b > 0", rem_b, ">", F(0))
check("b_* < 0.018", 2 * xi * v_init**2 + 2 * t_claim * v_init, "<", rem_b**2, "b = 0.018 suffices")

# 5. v bounds: (1-b)/(r+1/r) <= v <= (1+b+t/r)/(r+1/r)
# Note r + 1/r = 3*r (since 1/r = 2*r when r = 1/sqrt(2))!
# Also f(x) = x + 1/x is strictly decreasing on (0, 1), so r_hi + 1/r_hi < r + 1/r < r_lo + 1/r_lo.
# Using exact identity r + 1/r = 3*r gives tighter bounds: 3*r_lo < 3*r < 3*r_hi.
denom_lo = 3 * r_lo  # exact lower bound for r + 1/r = 3r
denom_hi = 3 * r_hi  # exact upper bound for r + 1/r = 3r
check("r_hi + 1/r_hi < 3*r_lo (decreasing f)", r_hi + 1/r_hi, "<", denom_lo, "3*r_lo is tighter lower bound than r_hi+1/r_hi")
check("r_lo + 1/r_lo < 3*r_hi (decreasing f)", r_lo + 1/r_lo, "<", denom_hi, "r_lo+1/r_lo is tighter upper bound than 3*r_hi")
# Check v bounds even with the weaker naive bounds (r_lo + 1/r_hi) and (r_hi + 1/r_lo)
check("v > 0.462 (naive r_hi+1/r_lo)", (1 - b_claim) / (r_hi + 1/r_lo), ">", F("462/1000"), "holds even with naive interval arithmetic")
check("v < 0.481 (naive r_lo+1/r_hi)", (1 + b_claim + t_claim / r_lo) / (r_lo + 1/r_hi), "<", F("481/1000"), "holds even with naive interval arithmetic")

v_lo_exact = (1 - b_claim) / denom_hi
v_hi_exact = (1 + b_claim + t_claim / r_lo) / denom_lo
v_lo_claim = F("462/1000")
v_hi_claim = F("481/1000")
check("v > 0.462", v_lo_exact, ">", v_lo_claim, "(1-b)/(3 r_hi) > 0.462")
check("v < 0.481", v_hi_exact, "<", v_hi_claim, "(1+b+t/r_lo)/(3 r_lo) < 0.481")

# 6. R = s/v: r_lo / v_hi_claim < R < s_claim / v_lo_claim
R_lo_exact = r_lo / v_hi_claim
R_hi_exact = s_claim / v_lo_claim
R_lo_claim = F("147/100")
R_hi_claim = F("1533/1000")
check("R > 1.47", R_lo_exact, ">", R_lo_claim, "r_lo / 0.481 > 1.47")
check("R < 1.533", R_hi_exact, "<", R_hi_claim, "0.708 / 0.462 < 1.533")
# Wait! Let's also check 0.7071 / 0.481 and 0.708 / 0.462!
# Wait: 0.708 / 0.462 = 708/462 = 1.532467... < 1.533!
# And 0.7071 / 0.481 = 1.47006237... > 1.47!

# 7. m1 = r*v_+ + b < 0.359
m1_hi = r_hi * v_hi_claim + b_claim
m1_claim = F("359/1000")
check("m1 < 0.359", m1_hi, "<", m1_claim, "r_hi*0.481 + 0.018 < 0.359")

# 8. L = (r*s + sqrt(xi))*I / v_- < 0.00055
# Note r*s <= q (since r*s = r^2 + r*t <= q)! Or use r_hi*s_claim.
L_hi_1 = (r_hi * s_claim + sqrt_xi_hi) * I_claim / v_lo_claim
L_hi_2 = (q + sqrt_xi_hi) * I_claim / v_lo_claim
L_claim = F("55/100000")
check("L < 0.00055 (using r_hi*s_claim)", L_hi_1, "<", L_claim)
check("L < 0.00055 (using r*s <= q)", L_hi_2, "<", L_claim)

# 9. |mu|^2 and Re(mu)
# |mu|^2 = (s^2/2 + z P)/r^2 = s^2 + 2 z P.
# Since s > r, s^2 > 1/2, and z P >= 0 => |mu|^2 > 1/2 (so >= 0.5).
# Upper bound: |mu|^2 <= q^2 / r^2 = 2 q^2.
a_lo_claim = F("1/2")
a_hi_claim = F("50021/100000")
check("|mu|^2 <= 2 q^2 < 0.50021", 2 * q**2, "<", a_hi_claim, "2*(0.5001)^2 = 0.50020002 < 0.50021")

# Re(mu) in [(s - sqrt(2 z P))/(2 r), (s + sqrt(2 z P))/(2 r)]
# Since s > r: s/(2r) > 1/2. And s <= q/r => s/(2r) <= q/(2 r^2) = q = 0.5001.
# Also P = q^2 - s^2/2 < q^2 - 1/4 = xi = 0.00010001.
# Wait: sqrt(2 z P)/(2 r) = sqrt(2 z P) / sqrt(2) = sqrt(z P) <= sqrt(P) < sqrt(xi) < 0.01001!
# Look how clean that is: 2 r = sqrt(2), so sqrt(2 z P)/(2 r) = sqrt(z P) < sqrt(xi) < 0.01001!
# Therefore:
# Re(mu) >= s/(2r) - sqrt(z P) > 1/2 - 0.01001 = 0.48999 > 0.489
# Re(mu) <= s/(2r) + sqrt(z P) < q + 0.01001 = 0.51011 < 0.511
x_lo_exact = F(1, 2) - sqrt_xi_hi
x_hi_exact = q + sqrt_xi_hi
x_lo_claim = F("489/1000")
x_hi_claim = F("511/1000")
check("Re(mu) > 0.489", x_lo_exact, ">", x_lo_claim, "0.5 - 0.01001 = 0.48999 > 0.489")
check("Re(mu) < 0.511", x_hi_exact, "<", x_hi_claim, "0.5001 + 0.01001 = 0.51011 < 0.511")
# Also check with cruder r_lo, r_hi, s_claim:
# s/(2r) > r/(2r) = 1/2 (exact), s/(2r) < s_claim/(2*r_lo) = 0.708 / 1.4142 = 0.500636...
# sqrt(2*xi)/(2*r_lo) < sqrt(2)*0.01001 / (2*0.7071) = 0.01001 * r_hi / r_lo < 0.010012
check("Re(mu) upper even with s_claim/(2*r_lo)", s_claim/(2*r_lo) + sqrt_xi_hi * r_hi / r_lo, "<", x_hi_claim)

# 10. E bound: E < (0.5001*0.018 + sqrt(0.000101*0.359)) / (0.7071*0.462) < 0.0461
check("sigma^2 <= P < xi < 0.000101", xi, "<", F("101/1000000"), "sigma^2 < 0.000101")
E_claim = F("461/10000")
rhs_E = E_claim * r_lo * v_lo_claim - q * b_claim
check("rhs_E > 0", rhs_E, ">", F(0))
check("E < 0.0461", F("101/1000000") * m1_claim, "<", rhs_E**2, "exact squared test for E < 0.0461")

# 11. Covariance contribution q*sqrt(1-c^2) < 0.130
cov_claim = F("130/1000")
check("q*sqrt(1-c^2) < 0.130", q**2 * (1 - c**2), "<", cov_claim**2)

# 12. U_* = L + h*E + cov < L_claim + 1*E_claim + cov_claim < 0.177
U_claim = F("177/1000")
check("U_* < 0.177", L_claim + E_claim + cov_claim, "<", U_claim, "0.00055 + 0.0461 + 0.130 = 0.17665 < 0.177")

# 13. Monotonicity conditions in Section 4.1:
# 1.533 * 0.50021 < 2 * 0.489  (R_+ * a_+ < 2 * x_-)
check("mono1: R_+ a_+ < 2 x_-", R_hi_claim * a_hi_claim, "<", 2 * x_lo_claim)
# 1.47 > 0.511 (R_- > 1^2 * x_+)
check("mono2: R_- > h_+^2 x_+", R_lo_claim, ">", F(1)**2 * x_hi_claim)
# 0.50021 < 1.47 * 0.489 (h_+^2 * a_+ < R_- * x_-)
check("mono3: h_+^2 a_+ < R_- x_-", F(1)**2 * a_hi_claim, "<", R_lo_claim * x_lo_claim)

# 14. A1 and A2 bounds with R0 = 1.533
R0 = R_hi_claim
A1_rad = 4 - 4 * R0 * x_hi_claim + a_lo_claim * R0**2
A1_claim = F("1379/1000")
check("A1_rad > 0", A1_rad, ">", F(0))
check("A1 > 1.379", c**2 * A1_rad, ">", A1_claim**2, "c^2*(4 - 4*R0*0.511 + 0.5*R0^2) > 1.379^2")

A2_rad = R0**2 - 2 * R0 * c**2 * x_lo_claim + a_hi_claim * c**4
A2_claim = F("1178/1000")
check("A2_rad > 0", A2_rad, ">", F(0))
check("A2 < 1.178", A2_rad, "<", A2_claim**2, "R0^2 - 2*R0*c^2*0.489 + 0.50021*c^4 < 1.178^2")

# 15. Final contradiction: A1 - A2 > 1.379 - 1.178 = 0.201 > 0.177 > U_*
check("A1 - A2 > 0.201", A1_claim - A2_claim, "==", F("201/1000"))
check("0.201 > 0.177", A1_claim - A2_claim, ">", U_claim)

all_ok = all(x["ok"] for x in checks)
print(f"\nALL HAND-PROOF CHECKS PASSED: {all_ok} ({sum(x['ok'] for x in checks)}/{len(checks)})")
with open("hand_proof_audit.json", "w") as f:
    json.dump({"all_ok": all_ok, "count": len(checks), "checks": checks}, f, indent=2)

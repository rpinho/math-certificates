"""Explicit finite-n prefactors for the degree-10 certificate."""

from flint import arb, ctx
from fractions import Fraction

ctx.prec = 160
DEGREE = 10
CAP = Fraction(4001, 10000)
GAP = Fraction(3, 20)
N0 = 550_000
MARGIN = Fraction(1, 1000)
EXEMPT = 2*DEGREE-1


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    require(Fraction(2,5)+Fraction(3,5*N0) <= CAP, "capacity rounding")
    require(GAP*N0 >= 2 and GAP*N0 >= 2*EXEMPT, "swap gaps and occupancy exemptions")
    require(Fraction(33,N0) < MARGIN, "union-bound derivative")

    n = arb(N0)
    d = DEGREE*n
    # n+1: four free part-size entries. d+1: five off-diagonal edge
    # counts, three pairing numerator powers, and two degree-count powers
    # (one occupancy conditioning power plus every R for Case II).
    # 30: three terms (naive, I, II) for each of the ten dihedral maps.
    log_union = (arb(30*3**6).log() + 4*(n+1).log() + 10*(d+1).log()
                 + EXEMPT*n.log() + EXEMPT*arb(2*DEGREE).log() - n/1000)
    require(log_union < -arb(2).log(), "first moment must be < 1/2")
    disconnect = Fraction(3,13)
    require(disconnect < Fraction(1,2), "disconnection bound")
    union = log_union.exp()
    total = union + arb(disconnect.numerator)/disconnect.denominator
    require(total < 1, "existence inequality")
    print("n0", N0, "(all integers, including odd n)")
    print("counts: profiles <= (n+1)^4; all K <= (10n+1)^5; all R <= (10n+1)")
    print("factors: pairing <= 3^6*(10n+1)^3; Case I <= (10n+1)*n^19*20^19; "
          "Case II <= (10n+1) per R")
    print("log first-moment upper bound", log_union.str(22))
    print("first-moment upper bound", union.str(22))
    print("disconnection probability <= 3/13 < 1/2")
    print("sum upper bound", total.str(22))
    print("monotone for n >= n0: 33/n - 1/1000 < 0")


if __name__ == "__main__":
    main()

# Full-coefficient moment criterion (draft, 2026-10-30)

This is an extension of the Wikström moment criterion using the geometric
coefficient argument in Pinho (2026), as sharpened in PR 274 by Niedbala Giraudin.
It is an unrefereed proof draft. No numerical claim is certified by this file.

Let beta(t)=1-1/G(t), with G from the flux / enclosing-disk geometry in
`sources/PROOF.md`. Suppose a finite positive measure nu on [c²,1], with no
atom at 1, satisfies, for EVERY integer k>=0,

    integral t^k dnu >= 1/(k+1),
    integral beta(t) t^k dnu <= 1/(k+1).

Then c is admissible. The mass need not equal one; its k=0 constraints are
nu([c²,1])>=1 and integral beta dnu<=1.

## Proof of the coefficient inequality including k=0

Let |f|<=|g| on c<|z|<1; the zero and constant boundary cases are immediate.
The quotient omega=f/g is holomorphic on the annulus after removing common
zeros and maps to the open unit disk. Fix c<r<1. The enclosing-disk result
provides alpha in the disk and a pseudohyperbolic radius rho with

    |f-alpha g| <= rho |g-conjugate(alpha)f| on |z|=r,
    1/(1-rho²)<=G(r²).

Put F=f-alpha g and H=g-conjugate(alpha)f; these are analytic on the WHOLE
unit disk, regardless of any poles of omega inside the inner circle.
For every coefficient index k INCLUDING ZERO,

    |H_k|²-|F_k|² = (1-|alpha|²)(|b_k|²-|a_k|²).

Write x_k=(|a_k|²-|b_k|²)_+ and y_k=(|b_k|²-|a_k|²)_+,
and X(t)=sum_{k>=0}x_k t^k, Y(t)=sum_{k>=0}y_k t^k.
Using the coefficient identity at all indices for which y_k>0,

    (1-|alpha|²)Y(r²)
      = sum_{y_k>0} (|H_k|²-|F_k|²)r^(2k)
      <= sum_{k>=0}|H_k|² r^(2k)
      = M_H(r)².

Parseval and the pointwise radius bound give

    M_H²-M_F² >= (1-rho²)M_H²,
    M_H²-M_F² = (1-|alpha|²)(M_g²-M_f²).

Thus Y<=G(Y-X), or X<=beta Y. This is the same coefficient argument as
Pinho's, with the constant coefficient retained in the negative part.
Both sides are continuous for t<1, so at t=c² we may use beta(c²)=1 by
letting r decrease to c.

## Integration

Since f,g are in Bergman A², sum y_k/(k+1) is finite. Tonelli and the upper
moment constraints give

    integral Y beta dnu = sum y_k integral beta t^k dnu
                         <= sum y_k/(k+1) < infinity.

Tonelli for X, the pointwise inequality, and the lower moment constraints give

    sum x_k/(k+1) <= integral X dnu
                  <= integral beta Y dnu
                  <= sum y_k/(k+1).

This is precisely ||f||²<=||g||². No probability normalization has been used.
The k=0 upper constraint is essential when y_0>0.

## Relation to the old criterion

The old argument isolates y_0 and imposes probability mass exactly one.
Any probability measure satisfying the old moments automatically satisfies
both new k=0 conditions (beta<=1). The new feasible family contains the old
one. Numerical improvement, if any, must pass a separate interval checker
for all indices and both infinite tails.

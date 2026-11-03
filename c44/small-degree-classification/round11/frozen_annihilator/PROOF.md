# Finite annihilator obstructions — candidate, unrefereed

This packet certifies a limited negative result for fourteen explicitly
listed Fourier-mask banks. It does not prove that3/2 is optimal and does
not classify companions outside these banks. The source polynomials are
the saved46-variable degree-five and94-variable degree-six search seeds.
Two separately written exact checkers verify their Booleanity again.

Fix a source f=P/D=x_b U/D+V/D, where U,V have integer Fourier
numerators and avoid b. The identity P^2=D^2 implies UV=0. The explicit
candidate bank consists of distinct masks S_1,...,S_m avoiding b, each of
cardinality at most d-1. A candidate numerator R=sum a_i x_(S_i) satisfies
RV=0 precisely when, for each Fourier mask T,

    sum_i Vhat_num(T xor S_i) a_i=0.                  (1)

These are exact integer linear equations over a field of characteristic
zero. The original U has all its masks in the bank and is a nonzero
solution, checked by exact multiplication. Thus the full kernel has
dimension at least one.

Each submitted trace uses only two kinds of inference from an actual row
of(1), after the previously established relations have been substituted:
(1) a nonzero multiple of one remaining parameter forces that parameter
to zero; (2) a nonzero multiple of a_i-epsilon a_j,epsilon=+/-1, identifies
two remaining parameters. Every row is reconstructed directly from the
bank and V by its submitted XOR mask; no row of the proposer's large
matrix is trusted or needed. Each valid operation removes exactly one
free parameter. There are m-1 operations and one nonzero parameter remains.
Both checkers also verify that the original nonzero U is consistent with
every resulting sign/zero relation. Therefore the full solution space of
RV=0 inside this bank is exactly the line spanned by U. Extra rows of(1)
cannot shrink it further, because U satisfies every row by UV=0.

Consequently any companion R in that bank satisfying R^2=U^2 must be U
or -U: write R=cU, then(c^2-1)U^2=0 and U^2 is nonzero. Such a companion
does not produce a nontrivial new selector in the splitting construction.
This proves the obstruction for the submitted banks only. They include
selected derivative/low-degree masks and were capped at3000 columns; they
are not the entire space of degree<=d-1 polynomials on these variables.
One coordinate per observed numerical signature was sampled, without a
claim that signatures classify all cofactor orbits.

Checker A uses signed weighted disjoint sets. Checker B, separately written (same agent),
stores an explicit signed free-parameter expression for every coefficient
and performs substitution by scanning all coefficients. They import
neither the proposer nor each other. Both reconstruct each original row,
check its proportionality by integer cross multiplication, check the
nonzero witness, and verify the fourteen final dimensions. Their frozen
receipt and corrupted-trace rejection tests are required for acceptance.
No universal lower-bound conclusion follows from this finite obstruction.

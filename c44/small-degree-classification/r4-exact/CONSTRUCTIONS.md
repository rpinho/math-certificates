# Construction and recursion audit

All statements below use real multilinear degree on a sign cube. Counts are
relevant coordinates, not Fourier sparsity. PR284 is a different constant.

The ordinary address function with m address bits and 2^m independent data
bits is sum_a 1_(address=a) y_a. It has degree exactly m+1 and uses 2^m+m
variables (m=0 gives a dictator). A selector joining two degree-d Boolean
functions on disjoint inputs has degree d+1 and 2n+1 variables. Its iterated
limit from a seed (d,n) is (n+1)/2^d.

The CHS/Shinkar--Tal two-control version is

    G(s,t,X,Y)=(s+t)f(X)/2+(s-t)f(Y)/2.

For s=t it is s f(X), and for s=-t it is s f(Y). Every seed variable remains
relevant and both controls are relevant for any nonconstant seed and
disjoint copies. Highest-degree monomials give degree exactly d+1. Its
count recursion is n'=2n+2; from any seed the count after k steps is
2^k(n+2)-2 and the limit is (n+2)/2^d. Starting with a dictator gives
3*2^(d-1)-2, including 22,46,94. This was reproduced exactly by Boolean
Fourier convolution on the authorized pod, before new work.

Thus 23 quartic variables or 47 quintic variables would indeed give a C44
lower bound above 3/2. The candidate proof R4=22 excludes the quartic
possibility. The quintic interval is only 46<=R5<=53 here.

The weighted CHS extremal identity max_(degree<=d)D=R_d/2^d is a separate
statement. Its corrected final proof duplicates *all* lower-local-degree
variables at once and shares the degree-d coordinates, then adds a selector.
Weights of duplicated variables sum to their old weights; the selector adds
positive weight. A single-variable AND substitution is used only to force
all local degrees d in an R_d maximizer, not to preserve D generally. The
corrected argument and original paper/thesis citations are retained in
baseline/c44r5/PROOF.md section 1.

PR284, https://github.com/teorth/optimizationproblems/pull/284 , is Koshta's
ternary Bohnenblust--Hille family on 3d inputs. The pinned repository commit
is 2557cdb23d08cd45414e4dc312b5a81d629e0b20. Its (2^d-1)2^d counts are
Fourier coefficients, not relevant variables. It has zero density 2^-d,
so its functions are not sign Boolean witnesses for R_d.

The elementary Boolean completion of any ternary f is

    F(x,z)=f(x)+z(1-f(x)^2).

It is Boolean, has degree at most 2d+1, and uses at most 3d+1 variables
for this family. This upper degree/count description supplies no improvement
over the CHS witnesses. It does not rule out a more sophisticated use of
Koshta's blocks. The family and its proof are credited, and no lower-bound
improvement for C44 is claimed.

Exact controls reproduced the committed PR284 instances at degrees 2,3,4:
they have 5,8,11 inputs, zero densities 1/4,1/8,1/16, and Boolean completions
with (degree, relevant count) respectively (5,6), (7,9), (9,12). The ordinary
address polynomials through degree six also passed exact Boolean convolution;
their counts are 1,3,6,11,20,37, versus CHS 1,4,10,22,46,94.

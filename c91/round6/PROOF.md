# Round 6 proof specification — Method 2

Candidate and unrefereed. The verified numerical instantiation is given below.
Credit Leandre Jack's #273 canonical-alignment first moment; Lueker;
Ganguly–Mossel–Rácz; Bilardi–Schimd; and inherited rounds 2–5. The inherited
round-5 proof is retained as sources/ROUND5_PROOF.md and is an explicit
premise for its unchanged frontier, base rules and bit-complement quotient.

## The selected intersection invariant

Fix a finite explicit bank F of column words of length at most 21. Verify
each word by exact dynamic programming against the minimum key (edit cost,
gap count, operation tuple), where diagonal < deletion < insertion. The
columns 0..7 are 00,11,01,10,D0,D1,I0,I1. A forbidden word must have strictly
larger key than the DP minimum on the two strings it consumes. This is a
finite exact test for every listed word, not an inference from the sampling
procedure used to select candidates.

Choose the minimum-key optimal alignment for any pair of finite strings.
Every contiguous segment is minimum-key for its own consumed substrings:
a smaller cost or gap count improves the full alignment, and at equal
cost/gaps the two segments have the same column count (the sum of consumed
lengths plus gap count, divided by two), so replacing a lexicographically
smaller operation tuple also improves the full operation tuple. Thus no
chosen canonical word has any factor in F.

At every processed column the combined state consists of (i) the inherited
five-rule run memory; (ii) the forbidden-bank suffix matcher state; (iii)
the round-5 genuine-witness frontier with W=3,B=2,S=0,T=2; (iv) the last four
valid input bits and their initial lengths. Its invariant is simultaneously:
all stored frontier records have the actual witnesses specified in the
round-5 proof, and the matcher coordinate is exactly the longest retained
suffix information of the processed label word. Update the two coordinates
on the same label and reject when either component rejects. Matcher failure
means a fully DP-verified forbidden factor occurred; frontier failure has a
strictly better real path witness. Both contradict canonical prefix/segment
optimality. The initial state satisfies both conditions, so induction proves
canonical survival at all lengths. Omitting any bank word is harmless.
Cold-start acceptance is used only for bank selection; it is not assumed to
characterize redundant exclusions in every reachable context.

The bank is closed under global bit complement; the frozen verifier must
verify this closure and the minimized matcher's root-fixing involution.
Every frontier update uses only bit equalities and is equivariant under the
same complement. Normalizing by the most recent X bit (otherwise Y bit)
therefore gives the inherited complement quotient. Keep all eight edges and
their multiplicities. Lifting a representative potential back to the full
graph makes its row inequality identical after permuting complemented
labels. The lifted state count is at most twice the representative count;
the artifact's counted value must be below 500 million.
Only the root has both input histories empty. Every other lifted state
contains a latest valid input bit, which complement flips, so it is not
fixed. Thus N representatives lift to exactly 2N-1 states.

## Higher-order input weights and almost-all-input guarantee

Use the eight nonempty even Walsh supports encoded by masks
[3,5,9,15,17,23,27,29], relative to the newest bit at offset zero. These
include lag-4 pair correlation and three span-four fourth-order correlations
in addition to the four inherited statistics. This feature family was
already explored in rounds 3/5. The round-6 structural change being tested
is its combination with longer DP-verified exclusions on the stronger
round-5 frontier; changing weights or frontier caps alone is ineligible.

For a support P, sum the spin product over every valid translate in each
input. Every summand has expectation zero. Distinct translates have
distinct nonempty supports; in the product of two different summands some
independent mean-zero spin appears once, so their covariance vanishes.
The two independent length-n strings therefore give Var(H_P)<=2n. For the
fixed eight supports, a union bound and Chebyshev imply probability at most
16/sqrt(n) that any |H_P| exceeds n^(3/4). No independence of overlapping
windows is assumed. Alternatively changing one bit affects at most |P|
terms with change at most 2 per term; bounded differences on 2n bits gives
P(|H_P|>u)<=2 exp(-u^2/(4n|P|^2)). Thus the typical set has probability
1-o(1), cardinality 4^n(1-o(1)), and zero entropy-rate penalty.

Emit each contribution exactly when its final input bit is consumed.
Initial histories suppress unavailable windows. Every alignment of a fixed
pair then has the same total H_P. Even support size makes each contribution
invariant under global bit complement, including along the explicit lifted
path. The brute-force audit compares emitted increments with products
computed directly from original complete strings.

## First moment and exact certificate obligation

For positive rational x>1,0<t<1 and z_P>0, weight a column consuming ell
input bits, with edit cost k and increments h_P, by
2^(-ell) x^ell t^k product z_P^h_P. A positive potential satisfying the
strict rational inequality A V < V at EVERY reachable complete row makes
the all-finite-path weight sum G finite. Indeed the finite maximum ratio
theta=max(AV)_i/V_i is <1, and a fixed multiple of V dominates 1.

For a typical pair with edit distance <=an, its surviving canonical word
has weight at least 4^(-n) x^(2n) t^(an) exp(-n^(3/4)sum |log z_P|).
Distinct input pairs have distinct labeled words. Thus their probability is
at most G exp(-n(2 log x+a log t)+O(n^(3/4))). If the displayed exponent
is strictly positive, adding the vanishing atypical probability proves
liminf E ed/n >=a. Subadditivity supplies the defining limit C91.

The frozen artifact must contain the full explicit forbidden bank, every
rational parameter, expected reconstruction counts and an exact positive
potential. A separately written (same agent) verifier reconstructs all
matcher/frontier/quotient states and partitions from these bytes and tests
every integer-cleared strict row inequality with multiplicity. The selected
potential encoding below uses exact integers throughout.
The inherited eight-feature clearing denominator is
D=4 q^2 s product u_P^2 v_P^2, for x=p/q,t=r/s,z_P=u_P/v_P.
The complete exact arithmetic capacity and overflow rejection are given in
the retained round-5 proof. Arb plus a separately written rational-series
logarithm check must prove 2 log x+a log t>0 and a>=529/2000.
Corrupted artifacts must fail. No numerical search result alone is a bound.

For the exact rational logarithm enclosure, put u=(q-1)/(q+1) for q>0.
Then |u|<1 and log(q)=2 sum_{j>=0} u^(2j+1)/(2j+1). After N terms the
absolute tail is at most
2 |u|^(2N+1) / ((2N+1)(1-u^2)), by replacing all remaining denominators
by 2N+1 and summing a geometric series. The rational checker uses N=120
for x and t and combines the resulting intervals using a>0. Its strictly
positive rational lower endpoint therefore proves the required exponent
sign without relying on its printed floating approximation.

## Compact integer-iteration potential encoding

The optional `integer-lazy-power-ceil-weights-v1` encoding defines a finite exact
integer vector without storing millions of entries. The artifact specifies
integer precision b, initial value M>0, and a finite iteration count k. For
every edge coefficient a_e=c_e/D (the exact rational formula above), set
u_e=ceil(2^b c_e/D), by exact integer ceiling, and B_e=u_e/2^b. Thus B>=A
entrywise, including edge multiplicity. This is a one-sided rational
majorant, with no floating arithmetic or error assumption in its construction.

After reconstructing weighted classes numbered by first appearance, take
the first complete row in each class to specify the quotient transitions.
Start V^(0)_i=M. Define k deterministic integer iterations

    V^(j+1)_i = 1 + floor((2^b V^(j)_i + sum_e u_e V^(j)_destination) / 2^(b+1)).

Every iterate is a fully specified exact integer. There is no theorem
asserting that this recipe converges or succeeds: the certificate is valid
only if the resulting positive vector passes every complete reachable row
inequality sum_e u_e V_destination < 2^b V_source. These inequalities imply
AV<=BV<V, so the preceding first-moment proof applies unchanged. The
partition only specifies how to reconstruct the proposed vector; the final
checks on every original row make no unverified representative-row premise.

The verifier rejects overflow and nonpositive values. It restricts b<=48,
M<=2^60, and u_e<2^48. Each vector entry is a positive uint64; products and
eight-edge row sums are below 2^115 and the identity-augmented iteration sums below 2^116, and 128-bit exact integers suffice for
the iteration and row tests. Exact rational coefficient ceilings use a bounded binary search with the
inherited 2560-bit products: u is the least positive integer with
D*u >= 2^b*c_e. The allowed coefficient range is checked first.
Each coefficient or denominator has at most 35 positive uint64 factors,
besides a factor at most 4. Multiplication by at most 2^48 therefore needs
at most 2290 bits, below the 2560-bit capacity; arithmetic also rejects
capacity overflow explicitly. This encoding is exact certificate data, not numerical search
instructions. A zero iteration count defines a constant vector and is a
useful positive-potential rejection control for this candidate's root row.

## Verified round-6 instantiation

Take a=265988/1000000, x=1126334981/10^9, t=408795349/10^9,
and z numerators in mask order [3,5,9,15,17,23,27,29]:
[1039958978,1022306830,1009100630,1002191349,
1002428586,999515806,1000849633,999490259], all over 10^9.
Use the explicit 59,550-word bank in candidate_c91r6.json.gz,
W=3,B=2,S=0,T=2, absolute caps, and recipe b=42,M=2^50,k=128.
The actual longest listed word has length 16, within the declared cap 21.

Complete reconstruction gives 121,332,798 representative rows,
499,034,690 edges with multiplicity, and 32,774,059
potential classes. Lifting gives 242,665,595 states,
below the frozen 500-million cap. Every row passes the exact strict
majorant inequality with minimum integer slack 4736028943110
at denominator 2^42. Arb and the separately written rational-series
enclosure prove 2 log x+a log t>0. Thus the preceding universal argument
gives the candidate, unrefereed conclusion C91>=0.265988.

Artifact SHA256: `e6bcacb08bb36ee21e93f90a05160b6240260692390630c03049ac0ccd39f767`.
Full replay, exponent and five actual-corruption rejection receipts are
logs/main_exact_summary.json, logs/main_exact.log,
logs/main_rational_exponent.json and logs/release_frozen_controls.json.
The verifier is separately written (same agent); see VERIFICATION_SCOPE.md.
The historical six-hour invariant-gate snapshot is retained in the producer archive;
it is not an input to this reproduction packet.

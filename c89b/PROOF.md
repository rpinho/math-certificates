# Candidate upper bound for the K5 Ramsey multiplicity constant

Status: exact finite arithmetic passed; candidate and unrefereed. Search and the separately written verifier were both authored in this Codex session. This is independent implementation, not an external referee report. Prior art and comparison audit: `../PRIOR_ART.md`.

## Construction and reduction

`candidate.json.gz` specifies a symmetric 192 by 192 integer matrix R, denominator D=7, and 192 equal block weights. Every entry is 0, 5, or 7. On blocks i,j put red-edge probability R_ij/D and blue probability 1-R_ij/D; diagonal entries describe distinct vertices within the same block. All diagonal red probabilities here are zero.

For any such step graphon its monochromatic K5 density is

    c(W) = 192^(-5) sum_(i1,...,i5) [prod_(a<b) W_ia,ib + prod_(a<b) (1-W_ia,ib)].

Indices in this sum may repeat. They represent different sampled graph vertices occupying the same graphon block, so those terms must be retained.

To see that C89b <= c(W), replace each block by t vertices and color each unordered pair independently with the stated probability. The expected monochromatic K5 density tends to the displayed expression as t tends to infinity: tuples with actual repeated vertices contribute only O(1/t). Some coloring has density at most its expectation for each t. The limit defining the Ramsey multiplicity constant therefore gives the inequality. This uses no optimality or symmetry assumption on R.

## Independent exact enumeration

The verifier reads the frozen matrix, checks symmetry, integer ranges, equal masses, and its single nontrivial probability p. It enumerates each set of k distinct occupied blocks, 1 <= k <= 5. For that set, it enumerates every positive occupancy vector (m1,...,mk) summing to 5.

The multiplicity of that occupancy is 5!/prod mi!. An edge between distinct occupied blocks i,j appears mi*mj times; a block loop appears mi*(mi-1)/2 times. An entry of probability zero kills the term. Otherwise the contribution is a multinomial integer times p^e for red, or (1-p)^e for blue, with 0 <= e <= 10. This partitions every ordered block tuple exactly once. The code shares no routines or term cache with the numerical search, which enumerates nondecreasing repeated block labels.

The full matrix, with no transitivity shortcut, yields:

| e | red coefficient r_e | blue coefficient b_e |
|---|---:|---:|
| 0 | 126282240 | 189161472 |
| 1 | 77414400 | 134615040 |
| 2 | 48384000 | 39029760 |
| 3 | 6451200 | 2956800 |
| 4 | 806400 | 893760 |
| 5 | 0 | 0 |
| 6 | 0 | 13440 |

All higher coefficients vanish. Hence

    c(p) = [sum_e r_e p^e + b_e (1-p)^e] / 192^5.

At p=5/7, exact rational arithmetic gives

    C89b <= 2405659597 / 1427496763392
          = 0.0016852294580925716...
          < 0.00168523.

`fine_candidate.json.gz` has the identical support pattern and p=714945/1000000. Its independently recounted density is

    14656959395069207318275707929513494927 /
    8697308774400000000000000000000000000000
    = 0.0016852292789938741...

The simple 5/7 certificate is the preferred concise statement; the fine value is only an optional refinement of the same construction.

The checker compares each fraction exactly to both 168523/100000000 and PR #277's complete public fraction. Decimal conversions are for display only. `verification.log`, `fine_verification.log`, and `SHA256SUMS` identify the artifacts. Twenty-five small cases, including fractional loops and repeated blocks, were checked against literal ordered 5-tuples with exact integer products (`controls.log`); asymmetric input was rejected.

## Structural search idea and limitations

The credited starting point is the PPSS Cayley construction and Jeetu SK's all-edge probability refinement in PR #277. The public result has a fractional perfect matching and a second class of 12 fractional neighbors per vertex. Its equal-weight first-order descent preserves these classes. After reproducing the exact baseline, the probability Hessian exposed a negative direction that divides the latter class into two sets of six neighbors at every vertex. One set saturates at red probability 1; the other joins the matching at approximately 0.714945. The remaining fractional graph consists of three 64-vertex folded seven-cubes. Choosing 5/7 gives the compact certificate above.

This is a structural change of the probability classes, not a more precise replay of the public minimum. Block weights did not improve in the tested directions. The Hessian and gradient diagnostics, the scalar optimization, and the signed-lift investigation are numerical exploration only; the bound relies solely on the frozen integer matrix and exact recount. No global or graphon-local optimality, uniqueness, external review, or priority is claimed.

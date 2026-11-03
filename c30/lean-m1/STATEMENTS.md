# Statement correspondence

Source: the unchanged `../c30r2/FIRST_MOMENT_PROOF.md` (SHA-256
`a1575a482c7bc92090013b2419e4f41fafe5cc344b5736511f2bac987dc08ee9`).
A byte-identical copy is retained in `sources/FIRST_MOMENT_PROOF.md`.
Line numbers below refer to that copy. Namespace throughout: `C30Lean`.

## Integer envelope: inputs and exact counts

| Informal text, quoted | Lean declaration/clause | Comparison |
|---|---|---|
| L182: “Let y be any r-vector of nonnegative integer strip sizes” | `strip_envelope`: `y : List ℤ`, `hy : ∀ a ∈ y, 0 ≤ a`; `r` is `(y.length : ℤ)` | Equivalent; lists retain the ordered vector and impose no bound on its entries. |
| L182: “with sum L” | `hL : y.sum = L` | Exact. |
| L182: “at least B zeroes” | `hn0 : B ≤ countStrip y 0`; `countStrip y j := (y.count j : ℤ)` | Exact. |
| L182: “and at most U entries equal to two” | `hn2 : countStrip y 2 ≤ U` | Exact. |
| L182: “Choose e2 from {U,U-1}” | `(e.e2 : ℤ) = U ∨ (e.e2 : ℤ) = U - 1` | Exact integer subtraction, including the odd case. |
| L182: “so that L-r+B-e2 is even” | `(L - y.length + B - e.e2) % 2 = 0` | Equivalent integer parity statement. |
| L184: “e0=B” | `(e.e0 : ℤ) = B` | Exact. |
| L185: “e1=[3(r-B)-L-e2]/2” | `(e.e1 : ℤ) = (3 * ((y.length : ℤ) - B) - L - e.e2) / 2` | Exact: parity makes this integer division exact; `parity_envelope` proves the doubled identity internally. |
| L186: “e3=[L-r+B-e2]/2” | `(e.e3 : ℤ) = (L - y.length + B - e.e2) / 2` | Exact; the displayed parity clause rules out truncation. |
| L188: “these are nonnegative integers” | `StripEnvelope.e0`, `.e1`, `.e2`, `.e3` all have type `ℕ` | Exact; casting them into `ℤ` preserves their values and nonnegativity. |
| L188: “Let x have e_j entries equal to j for j=0,1,2,3” | `StripEnvelope.vector` concatenates `List.replicate e.e0 0`, then the corresponding lists for 1, 2, 3 | This explicitly chooses one such x. The inequality depends on excess sums, which ignore the order of x; the input y is never sorted or replaced by a profile. |
| L188: “Then x is majorized by y.” | `ThresholdMajorized e.vector y` | Encoded in the standard threshold-excess formulation: equal lengths, equal sums and `∀ t : ℝ, ∑ max(xᵢ-t,0) ≤ ∑ max(yᵢ-t,0)`. No separate sorted-partial-sums or transfer-sequence API is asserted. |

The prose does not give arbitrary-parameter feasibility hypotheses; it asserts
nonnegativity only in the sufficiently-large-m application. The general Lean
theorems make sufficient hypotheses explicit:

* `hB : 0 ≤ B`, `hU : 0 ≤ U`;
* `h₁ : U ≤ 3 * (r - B) - L`;
* `h₃ : U ≤ L - r + B`;
* `hzero : U = 0 → (L - r + B) % 2 = 0`.

The two linear inequalities ensure nonnegative numerators for either parity
choice. They are sufficient, not claimed necessary. Relative to an unrestricted
reading of the informal lemma these are additional assumptions, needed to avoid
a false statement about negative counts. For instance `y=[1]`, `B=0`, `U=2`
has no feasible nonnegative envelope with the required choice. With `U=0` and
odd `L-r+B`, choosing `U-1` would force `e2=-1`; `y=[0,1]`, `B=0`, `U=0`
exhibits this obstruction. `strip_envelope_application` discharges all these
extra hypotheses for the exact application parameters and `m ≥ 100`.

`parity_envelope` proves the count construction independently of y and returns
both exact count identities. `integer_strip_envelope` proves the same count
conclusions together with equal vector lengths/sums and every integer threshold
inequality. `strip_envelope` strengthens the latter to every real threshold.

## Threshold identities and inequalities

| Informal text, quoted | Lean declaration | Comparison |
|---|---|---|
| L190: “their lengths and sums agree” | `StripEnvelope.vector_length`, `.vector_sum`; `parity_envelope` returns `e0+e1+e2+e3=r` and `e1+2e2+3e3=L`; `integer_strip_envelope` returns vector equalities | Exact. |
| L190: “At threshold one the excess sum for y is L-r+n0” | `strip_count_identities`, second conjunct | Exact, with `y.sum` in place of L. |
| L190: “at least L-r+B, the value for x” | `integer_strip_envelope`, case `k=1`, using `hn0`; `StripEnvelope.excess_values` gives `e2+2e3` | Exact, using the count identities to identify `e2+2e3=L-r+B`. |
| L190: “At threshold two it is L-2r+2n0+n1” | `strip_count_identities`, third conjunct | Exact. |
| L190–192: “With T=sum_{j>=4}(j-3)n_j>=0, the count identities give … 2(2n0+n1)=3r-L+n0-n2+T >= 3r-L+B-U.” | `strip_count_identities`, fourth conjunct, then `hn0`, `hn2` in `integer_strip_envelope` | Proves the required inequality directly by induction on the vector. It does not separately define T or claim a histogram identity with T. This is a shorter proof of the same needed bound. |
| L194: “The left half is an integer. Taking its ceiling if necessary gives at least (3r-L+B-e2)/2=2B+e1” | `integer_strip_envelope`, case `k=2`; exact parity/count identities and integer arithmetic | Exact parity rounding; no real or fractional multiplicity is used. |
| L194: “At threshold zero the excess sums agree” | `strip_count_identities`, first conjunct; equal sums in `integer_strip_envelope` | Exact. |
| L194: “at thresholds at least three x has no excess” | `StripEnvelope.excess_values`, final conjunct, plus `excess_nonneg` for y | Exact, for all integer thresholds ≥3. |
| L194: “Between integers the excess sums are linear” | `realExcess_interpolate`; `realExcess_int`; `integer_thresholds_suffice` | Exact identity on each closed interval `[k,k+1]`, then all real thresholds using the integer floor. |
| L194: “These inequalities characterize majorization” | `ThresholdMajorized` definition | Uses the threshold formulation as the definition. Equivalence with sorted partial sums and generation by transfers is outside this milestone. |

`excess` and `realExcess` are exactly the displayed excess sums over the entries.
`excess_nonneg` proves the universal nonnegative lower bound.
`StripEnvelope.vector_nonneg` verifies that the explicitly constructed vector
has nonnegative entries. These are auxiliary statements with no extra informal
assumptions.

## Exact sufficiently-large-m specialization

| Informal text, quoted | Lean declaration | Comparison |
|---|---|---|
| L173: “alpha=555555/10^6, beta=185185/10^6, c2=7/50” | Exact rational numerators/denominators in `freeLeaves`, `emptyBound`, `twoCap` | Exact rational arithmetic. |
| L175: “L=ceil(alpha m)” | `freeLeaves m := ⌈(555555 : ℚ) * m / 1000000⌉` | Exact. |
| L177: “r=m-L+1 strips” | `stripCount m := (m : ℤ) - freeLeaves m + 1`, and `hlen` in `strip_envelope_application` | Exact. |
| L177: “n0>=B=ceil(beta m)+1” | `emptyBound`, `hn0` | Exact. |
| L178: “n2<=U=floor(c2 m), total free points L” | `twoCap`, `hn2`, `hL` | Exact. |
| L188: “nonnegative integers for all sufficiently large m” | `application_feasibility`; `strip_envelope_application`, `hm : 100 ≤ m` | Stronger: gives an explicit sufficient cutoff for envelope arithmetic. It does not assert that actual domino families or their leaf restriction already exist at every m ≥100. |
| L188: “indeed the linear lower estimate e1>0.0411125*m-3.5 suffices” | Feasibility proved directly from rational ceiling/floor bounds | The displayed estimate is not a named Lean theorem; the needed nonnegativity is proved without assuming it. |

The specialization leaves the actual strip vector hypotheses explicit. Leaf
restriction, the growth of B_m, the H_j coefficientwise product, transfers,
limiting eta coordinates and the whole C30 bound are outside this milestone.

## Finite weighted Markov and family selection

Source L148:

> Take s2=1/10. If a domino has N2>s2 n, then n(n-1)<=n N2/s2.
> Therefore the total n(n-1)-weighted generating function of these bad
> dominoes is at most z M'(z)/s2.

`finite_weighted_markov s w f t ht hw hf` proves

```text
Σ_{i∈s, t<f(i)} w(i) ≤ (Σ_{i∈s} w(i) f(i))/t,
```

where `s : Finset ι`, `w f : ι → ℝ`, `0 < t`, and both w and f are
nonnegative on s. Weights need not sum to one. Empty sets, zero weights and
zero total mass are permitted. This is stronger than a probability-normalized
form and allows arbitrary finite object sets and real thresholds. It is finite;
it does not assert an infinite generating-function limit or convergence.

`finite_family_selection s w n N₂ t ht hw` states the precise finite version
of the quoted bound, allowing variable sizes `n : ι → ℕ`:

```text
Σ_{i∈s, t*n(i)<N₂(i)} w(i)*n(i)*(n(i)-1)
  ≤ (Σ_{i∈s} w(i)*n(i)*N₂(i))/t.
```

Every occurrence of `n(i)-1` in this formula is subtraction in ℝ after casting
the natural size; it is multiplied by n, so n=0 contributes zero. For a finite
collection of dominoes take `w(D)=z^|D|` with z≥0 and t=1/10. The right side
is the finite first-moment derivative weight appearing in zM'(z)/t. This is
stronger in its arbitrary positive t and arbitrary nonnegative finite weights;
weaker than the prose's infinite-GF conclusion, whose limit passage is explicitly
outside this finite milestone. No leaf/empty concentration or two-leaf
concentration is assumed.


# math_review_gap1_1101 — independent adversarial review

**PASS: the reviewed argument establishes R4 = 22 and R5 ≤ 53, accepting its explicitly cited published theorems.** I found no mathematical GAP or FALSE step in those claims. Independent searches found no 23-variable quartic. My subjective probability that R4 = 22 is correct is **99%**; likewise **99%** for R5 ≤ 53.

The review started 2026-11-01 at about 21:43 UTC and completed well within the three-hour allowance. The target was read as an adversarial reviewer; no target search/checker code was imported or executed. The written proof, public data and raw inherited rational certificates were inputs. All mathematical computation ran on a rented pod in `the job directory`, under tmux, nice 10, with one BLAS/OpenMP thread. Peak concurrent review computation was below the ten-core allowance.

## Verdict by proof step

Line numbers refer to the unchanged [reviewed snapshot](target_snapshot/PROOF.md), corresponding to `../gap1/PROOF.md`. Detailed reasoning, including the delicate equality cases, is in [REVIEW_NOTES.md](REVIEW_NOTES.md).

|Step|Exact target lines|Verdict|Reason|
|---|---|---|---|
|Published classification and coverage|15–23, 29–34|PASS|Primary paper and fresh public data agree on 761 classes. The actual equivalence is appropriate. Higher-dimensional completeness remains a cited published classification.|
|Parity translation and invariance|24–31|PASS|Directly, ghat(S) = 2^-10 W_b([10] xor S). Input flips add only a constant output sign after the translation. Padding is valid.|
|Cubic envelope and equality signatures|36–52|PASS|Two independently written exact calculations agree on every row, including precisely lines 700, 716 and 757.|
|Maximum and all local degrees four|56–60|PASS|The AND replacement preserves all old relevant coordinates and adds one, while respecting degree four.|
|Integer derivative and Reed–Muller gap|62–70|PASS|Integer-valued finite differences give integer bit coefficients; reduction mod two is the support indicator. Dummy padding satisfies the theorem's parameter range.|
|Complete minimum-support structure|72–79|PASS|The source theorem applies to the full spectral interval [0,3]. Its seven nonconstant factor types give exactly the stated budgets.|
|Active dictators and degree reduction|81–86|PASS|A quartic coefficient disjoint from H cannot change when H is fixed and therefore contradicts B=0 on an active assignment.|
|Weighted restriction and h≤4|88–104|PASS|Coordinatewise nonnegative restriction slack proves (C); the displayed bound is 45/32 and integer relevance is at most 22.|
|Affine cubic parts and energy inequality|108–120|PASS|The original degree leaves at most one control in each Y-triple coefficient. The active-branch saving gives R4 ≤ h+15+4e.|
|Fixed bit and two pairs|124–131|PASS|The mismatch-slice average and full-cube covariance give e≤1/2.|
|Pair and triple|135–150|PASS|Equality at 23 forces three sign functions whose pointwise sum is zero, which is impossible.|
|Three-pair preliminary bound and equality reduction|154–171|PASS|The eight mismatch norms force orthogonality, then the catalogue equality table permits only energy patterns (1,0,0) and (1/2,1/2,0), up to permutation.|
|One energy equals one; pair lemma|173–191|PASS|The constructed h has degree at most d−1; every relevant Z variable appears in g or h. The resulting count is at most 22.|
|Two energies equal one half|193–210|PASS|Two nine-coordinate cubic parts overlap within sixteen Y coordinates. The shared coordinate has expected restricted weight ≥5/64 > 1/16, contradicting equality in (C).|
|Attainment|214–221|PASS|Independent rational XOR convolution verifies the 22-variable, degree-four, 64-term polynomial squares to one.|
|Duplication and seed thresholds|223–232|PASS|The recurrence gives 2^k(n+2)−2 variables; the stated 25/16 and 49/32 thresholds follow. The weighted-maximum identity also has a valid independent argument in the inherited proof.|
|R5 consequence|233–240|PASS|The two cases give max(floor(160/3), floor(9+30·11/8)) = max(53,50) = 53.|
|Secondary C44 recurrence and endpoint|241–252|PASS|A fresh rational checker verifies all 37 spectral duals, 48 node certificates, block bounds, chosen caps, recurrence columns, tail and exact 9/512 gain.|

The corresponding mathematical claims in `REPORT.md:3–15`, `41–58`, `118–122` agree with these results. This review does not treat historical operational assertions in the target report as mathematical premises.

One wording clarification is advisable at `PROOF.md:240`: `c5=53/32` selects an upper cap. It does **not** establish R5=53 or the exact weighted maximum W5=53/32. In its inherited cap notation, the statement is valid.

## What was checked from the classification source

I read the [primary 2023 paper](https://d-nb.info/1307299091/34), especially Definition 1 on p.215, Definition 2 on pp.215–216, Theorem 1 on p.217 and Table 1/classification discussion on p.224. I freshly cloned the [author's public data](https://gitlab.science.ru.nl/shahramr/ResilientFunctions) at commit `eace0ce0edcb664cd5e4f84d7f5cb56dc7400925`. The F10T6 SHA256 is

```
d0ca4026c3bfa61f7c40945e4627feecd9264d7854114806c533d64e06836ba0
```

The parity bridge above is independently derived, rather than inferred from cryptographic ANF degree. Six-resilience includes higher resilience, so lower real degrees and constant sign functions are included. An exhaustive independent orbit computation over all 65,536 four-input truth tables confirms all 58 source classes at the classification's starting dimension. It does not rerun the author's entire higher-dimensional classification.

The secondary [Krotov–Valyuzhenich paper](https://arxiv.org/html/2311.05566v2) prints 961 in section 3.1, but its own Data availability section explicitly identifies 761 and F10T6.txt. The primary paper, actual file and independent checks agree on 761; I found no evidence of 200 missing classes.

The [2024 addendum](https://doi.org/10.46586/tosc.v2024.i3.298-301) concerns restricted ANF degree at (n−5)-resilience. It does not replace the 761-class (n−4)-resilient result. Its data supplied additional quartic search seeds. The target's reliance on a published classification is properly disclosed; a finite row checker alone cannot establish completeness.

Other checked primary premises were [Valyuzhenich, Theorem 2(2)](https://arxiv.org/html/2303.10995), the [binary second-weight statement](https://arxiv.org/pdf/0902.0058), and [Wellens, Theorem 4.1](https://arxiv.org/html/2005.00566). The live table, public repository search, relevant open PR, recent papers and community searches are recorded in [PRIOR_ART.md](PRIOR_ART.md). GitHub API rate limits prevented a clean full metadata refresh; that limitation is disclosed there. No novelty claim is made.

## Degree-three control

**The energy-refined argument gives R3=10 without assuming R3=10 or cubic catalogue completeness.** For a quadratic g,

```
D(g) ≤ I(g)/2 = (1−E0(g)+E2(g))/2 ≤ 1/2+E2(g)/2.
```

The first inequality follows from the elementary derivative support bound. All 222 quadratic four-input truth tables independently satisfy this envelope.

At degree three the no-minimum-influence branch gives R3≤8. Otherwise the minimum derivative has control types h=2,3,3,4 and active density 1/4. For h≤3,

```
R3/8 ≤ h/8 + (1/4)(1/2) + (3/4)(1) ≤10/8.
```

For h=4, the two-pair affine quadratic part has average energy e≤1/2. The quadratic envelope then gives

```
R3/8 ≤ 4/8 + 1/2 + e/2 ≤10/8.
```

The independently verified Xi3 witness attains ten. The **unrefined scalar recurrence at target line 238 gives 11**, not ten; the energy step is essential to this control.

## Independent attempts to obtain 23 variables

1. **Disjoint nonlinear substitutions into all 761 cubic classes.** An independently written ILP replaces input i by Xi_(k_i), with disjoint variables and k_i in {1,2,3,4}. Every original Fourier support S must obey sum_(i∈S) k_i≤4. It maximizes the actual relevant count. Best result: **22**. A separate solver-free enumeration checks all **59,166** possible degree assignments, of which **8,080** are feasible, and confirms every class optimum exactly.

2. **Additional public quartic seeds.** A separate C++ search transforms every supplied ANF-degree≤3, (n−5)-resilient nonextension representative for 5≤n≤14, then exhausts the permitted disjoint Xi substitutions. It checks **358,448** representatives and **476,565** assignments. Best result: **22**. Independently written direct character sums and rational polynomial squaring verify all improving witnesses, including the final 22-variable witness. This public data is a restricted quartic family.

3. **Parity-substitution ILPs.** Each new coordinate is a binary column c; a seed monomial m has transformed degree sum_c x_c parity(m·c). Distinct seed Fourier masks are required to remain distinct. All **761 cubic classes** were processed; the solver-reported optima have maximum **14**, and every nonconstant returned polynomial was independently squared exactly. The 22-variable seed was also tested with parity columns of input weight at most four: the fixed-identity extension model reports infeasible at 23; the free injective model hit its **600-second limit without a candidate** and is **inconclusive**. Neither is claimed as a universal exclusion.

An initial parity relaxation allowed Fourier-mask collisions and produced nominal counts whose exact relevant counts collapsed. Those counts were rejected; only the verified injective results are used. No unrestricted 23-input SAT exhaustion was performed. The universal exclusion comes from the reviewed proof, not from these bounded searches.

## Receipts and reproduction

Key files are [FINAL_REVIEW_RECEIPT.json](receipts/FINAL_REVIEW_RECEIPT.json), [audit.json](receipts/audit.json), [direct.json](receipts/direct.json), [exact_search_verification.json](receipts/exact_search_verification.json), [quartic_public_final.json](receipts/quartic_public_final.json), [public_witness_verification.json](receipts/public_witness_verification.json), [types.json](receipts/types.json), and [downstream.json](receipts/downstream.json). Search source and separate verifiers are retained in `scripts/`. No target implementation was executed.

Replay the main exact checks on the authorized pod, where the public checkout and isolated SciPy installation remain in this review's own directory:

```sh
ssh a rented pod 'cd the job directory && tmux new-session -d -s review_gap1_replay "bash scripts/run_audit.sh && bash scripts/run_direct.sh && bash scripts/run_composition.sh && bash scripts/run_quartic.sh && bash scripts/run_public_verify.sh && bash scripts/run_types.sh && bash scripts/run_exact.sh && bash scripts/run_downstream.sh"'
```

Each wrapper records worker PIDs, uses nice 10, and sets single-thread BLAS/OpenMP. The exact enumeration and direct catalogue verifier need only Python's standard library and g++; ILP searches additionally use the isolated SciPy installation. The optional parity replay is:

```sh
ssh a rented pod 'cd the job directory && tmux new-session -d -s review_gap1_parity_replay "bash scripts/run_injective.sh"'
```

Its final version handles constants and one-term spectra. It skips cubic classes already present in the results. Existing JSONL logs append on rerun; for a clean full replay, first move the existing receipts directory to a uniquely named backup and create an empty receipts directory, then run the main checks, parity replay and exact verification sequentially. Preserve the historical receipts used for this review.

The downstream H96 result independently reproduced is

```
124779448974759300361320478779 / 39614081257132168796771975168
```

and its exact gain over the preceding candidate is 9/512. Both H72 and H96 match the target.

## Next work and closeout

The useful next mathematical check is a human audit of the classification bridge and the two equality exclusions; the exact notes and small receipts are sufficient to focus that review. A universal SAT model is unnecessary to the present proof, but would give a different computational route if pursued later.

No target or other job was modified. No commits, pushes, PRs, posts or messages were made. Compute workers and recorded shells were checked after completion; no review worker remains. The pod was left running. Receipts were pulled into this directory, and STATUS.md was updated during the session.

**Overall verdict: PASS. Probability R4=22 is correct: 99%; probability R5≤53 is correct: 99%.**

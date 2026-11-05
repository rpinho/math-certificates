# Feasibility method and provenance

This local, unrefereed experiment uses the public certificate and denominator-coefficient bank of vidigoat PR280, commit 3a7a84fec9c64ae426f06a5f52597c84b3453ba0. The Schnorr–Euchner/weighted-evaluation/product-start method is credited to vidigoat. The reduced-cost formula, residue restriction, joint LP, root-based screening and verification approach are inherited from our PR301 work; Doche supplies the limit-point construction, with earlier factor-library contributions by Grinsztajn and Épi.

The search imports two MIT-licensed files from vidigoat/optimization-records@3a7a84f: core.py, byte-identical to vidigoat's, and wlp.py, vidigoat's file with one added thread setting. An earlier version of this note said no vidigoat module was imported and called both files copies of our earlier code; that was wrong. The other scripts (cvp_search.py, cvp_gram.py, cvp_fixed.py, cvp_profile.py, solve_lp.py, check_numerics.py, and merge_evaluate.py through solve_lp.py) were written in our lane and use core.py; their line-level similarity to vidigoat's search code is under 10%. Neither verify_interval.py nor the referee checker imports core.py or wlp.py. Licence and file list: [THIRD_PARTY_NOTICE.md](THIRD_PARTY_NOTICE.md). The interval verifier is a copy of our own arb301 code, sharing no search functions.

## LP and pricing

For normalised nonnegative denominator weights mu and numerator weights w, minimise

    sum_j mu_j log M(R_j composed with T)
      + mean_k max(0, sum_i w_i log|S_i(T(z_k))| - sum_j mu_j log|R_j(T(z_k))|),
    subject to sum_j deg(R_j) mu_j = 1, sum_i deg(S_i) w_i < 1.

T(z)=z(1-z); the uniform midpoint grid covers [0,1/2], exploiting real-coefficient symmetry. The baseline grid has 524288 half-circle points. HiGHS runs one thread, with primal/dual feasibility tolerance 1e-10. Positive-epigraph rows are added until no omitted positive row remains. The dual has 0<=nu_k<=1/N, degree-budget price eta>=0 and denominator normalisation price lambda. All active denominator reduced costs are near floating zero. Price a proposed monic R by

    rc(R) = log M(R composed with T) - sum_k nu_k log|R(T(z_k))| - lambda deg(R).

Prices use certified FLINT roots converted to doubles; they are heuristic, not interval certificates or continuous dual bounds. Jensen identifies the continuous complementary-measure logarithmic objective underlying IRLS. Sampling/LP quadrature errors do not pass into the bound certificate, which is re-integrated independently.

## Closest-vector step

Let H=X(X-1)P4, degree6. A degree-d monic start R_current is changed to R_current + H U with deg(U)<d-6; this preserves monicity, R(0), R(1), and the residue modulo P4. Starts are active degree104 denominators, public library degree104 polynomials, products44+60 (degree104), and products104+16 or60+60 (degree120). All public products are exact integer polynomials.

Stratified samples come from the normalised complementary discrete mass max(1/N-nu,0). There are 720 samples for degree104 and 1024 for degree120 in the initial pilots, exceeding the 540 mentioned in the public README. The real/imaginary H X^j evaluation rows are divided by |R_current| and scaled to high-precision integers, with a negligible coefficient-identity ridge. We retain all evaluation scales: a median-relative floor was found to suppress entire arcs in a discarded diagnostic implementation. First-step log-noise or power profiles diversify some starts; subsequent IRLS steps use unperturbed inverse-modulus weights.

LLL is applied to the lattice alone. The optimised version reduces its exact integer Gram matrix, checks the returned transformation by exact matrix multiplication, and applies that transformation to the evaluation basis. Floating QR projects the target -R_current onto the reduced span. A fresh iterative Schnorr–Euchner enumerator retains the best16 points within a stated node budget; it is heuristic and generally exhausts the budget. A small 3D case is checked against exhaustive enumeration. The current polynomial is included as a feasible fallback. Polynomial coefficients are reconstructed with exact integers. Proposals are scored on the full LP dual using root-based logs; only a decreasing full reduced cost is followed. Exact gcd checks reject any shared numerator factor, and negative candidates are factored exactly.

Reduced-cost size is not realised gain. Candidate columns are jointly added to the LP and weights re-solved. Integer multiplicities are rounded at scale10^12, numerator exponents in 2^-20 Z; strict degree inequality is checked exactly. The resulting certificate requires its own independently written interval replay.

## Verification

verify_interval.py is the final pinned interval verifier, archived byte-identically from the producer’s verify_final.py. verify_public.py retains the earlier public-certificate pin. NUMERICS.md gives the independent root-isolation and adaptive two-sided Gaussian/clipped-affine integration proof. Outputs retain exact dyadic ball endpoints; decimal enclosures in reports are rounded outwards. This verifies finite conditions and B within the inherited Doche construction; it is not a formal proof of the arithmetic backend or the construction theorem. All candidate bounds remain unrefereed, with no priority or optimality claim.

## Follow-up controls and implementation refinements

cvp_profile.py adds smooth random root perturbations as an initial weight profile, independently reconstructed from the public prose description. Exact candidate offsets and coefficients are unchanged by those floating root profiles. The post-re-optimisation pilot prices against runs/pilot-early-dual.npz; the degree120 pilot continues against runs/baseline-dual.npz. These are separate dual cohorts and their reduced costs must not be pooled without labels.

Later LP solves use a smaller initial active-row margin (threshold1e-5 rather than0.004), while adding omitted near-positive rows until no positive row is missing. solve_lp.py now records complete-grid primal/dual residuals and asserts no omitted positive constraint. Initial baseline/first/early LP receipts used the original threshold0.004. Independent interval replays are unaffected by this numerical LP implementation refinement.

## Enumeration audit correction

A 16-case brute-force audit found that the initial seed pool could contain the zero vector twice (as a Babai neighbour and as the explicit feasible fallback). This sometimes left 15 distinct candidates in16 slots and could tighten the retained-point radius prematurely. The search was heuristic in either case; all saved integer columns and independently verified bounds remain valid. The exact failing3D case is saved in evidence/enumeration_initial_failure.json. The initial cvp_gram.py and corrected cvp_fixed.py are both retained here for reproducibility.

cvp_fixed.py deduplicates the initial pool. It passes16 random3D cases (including signed diagonals), matching all16 nearest squared distances against an exhaustive [-8,8]^3 oracle. evidence/numerical_checks.json also verifies the complete-grid primal/dual objective gaps, reduced costs and dual-atom bounds for both the original and moved LPs. The final fine120 and fixed104 pilots use the corrected enumerator; earlier negative search outcomes must be read with this implementation limitation.

# C44 < 1.9916994577: R4 = 22 and classification at small degree

Candidate, unrefereed. This certifies an upper bound on C44, the constant in r(f) <= C 2^deg(f), Tao table [44a](https://teorth.github.io/optimizationproblems/constants/44a.html), and the exact value R4 = 22 for the maximum number of relevant variables at degree 4. No human referee has checked this chain. Please read it with suspicion. The asterisk stays.

    R4 = 22,  46 <= R5 <= 50,  94 <= R6 <= 107,
    R7 <= 227,  R8 <= 474
    3/2 <= C44 <= 39449672077327653986659243787 / 19807040628566084398385987584 < 1.9916994577

It updates the earlier 2.0417086280 candidate and rests on the 2.1974348818 argument in [c44-certificate/reed-muller-caps](https://github.com/rpinho/c44-certificate/tree/e44b9b0cc91c656a680854ce341927c5a7b337c4/reed-muller-caps), including its inequality (3). The lower bound stays at 3/2.

## What's here

- `r4-exact/`: proof of R4 = 22 and R5 <= 53, using the published cubic classification.
- `round7/`: R5 <= 51, R6 <= 110, C44 < 2.0808959614, by a 52-case classification. Its quintic ceiling h <= 12 at (d, lambda) = (6, 3/2) is load-bearing again in rounds 9–11.
- `round8/`: R5 <= 50, R6 <= 109, C44 < 2.0417086280, by Boolean completion compatibility. Its `INPUT_ERRATA.md` corrects round-seven's real budget to 201/4 = 50.25, whose floor is 50.
- `round9/`: R6 <= 107, C44 < 2.0209645587. The new ceiling h <= 13 at (6, 7/4) uses all 189 exact cases. Both this ceiling and round-seven's quintic ceiling are needed.
- `round10/`: R7 <= 229, C44 < 2.0111998311, using near-equality and sign completion. The final sign-completion packet is `frozen_final/`; the first-stage packet alone gives 2.0114439717.
- `round11/`: R7 <= 227, R8 <= 474, C44 < 1.9916994577. Start at `frozen_parity/PROOF.md`. Its predecessor `frozen_accepted/` supplies the full deficit gap and 22-control exclusion; the final packet adds the parity exclusion and 15 unsigned incidence cases (six plus nine), checked by both implementations.
- `review/`: earlier AI reviews. Each new round also carries its two AI review records in `roundN/review/`. Astra's markdown reports have publication summaries because their original links are workstation paths; the portable round-eleven full referee report is included.

The new round folders include the exact earlier inputs they consume, certificates, checkers, rejection controls, historical receipts and reproduction notes. Compiled binaries, caches, large search logs and public-source snapshots are left out. Exact catalogue and template inputs needed for replay are retained. Regenerated manifests cover the packaged frozen trees; `SHA256SUMS` in each round covers its distributed files. `INPUT_ERRATA.md` records the missing Q != 0 hypothesis in round-eight equation (13), without editing that proof. Every application is to a relevant coordinate. Copied round-seven checker descriptions say "separately written (same agent)".

## Reproduce

Use **Python >= 3.10**, its standard library, and a C++17 compiler. Each new round has `REPRODUCE.md`. From `round11/`, after checking `SHA256SUMS`, run:

```sh
nice -n 10 python3 -B frozen_parity/replay.py
```

The restored predecessor receipts are included. The replay verifies the packaged manifests, builds the required native sources, checks all 15 cases under both implementations, checks the exact recurrence through degree 96 and the 9508/2^96 tail, and runs 120 artifact rejection checks and the existing positive controls. It does not rerun the earlier 189-case search. Its original replay remains available in `round9/frozen/replay.py`; the full inherited wrapper has a documented macOS resource-limit problem in the supplied review. The release verification receipts distinguish fresh checks from historical replays.

For the preceding round-eight result, run its completion and composition verifiers as before.

## What this doesn't show

Every review here is AI. Two AI reviews of round 11, Claude Opus 5.5 via Claude Science and GPT-6 Astra, each found no false step affecting the candidate bound on its stated premises. The Claude Science review retained a procedural FLAG; Astra accepted on the published premises. Earlier reviews reproduced the round-seven classification and round-nine 189-case exclusion. These are AI reviews, with no human referee or proof-assistant formalization.

The exact checkers are **separately written (same agent)**. The two round-eleven incidence checkers share a search design; agreement does not exclude a shared design error. A positive control for the fresh-tensor and omitted-coordinate branch, suggested by the Claude Science review, is not yet frozen here.

The published premises remain load-bearing: Valyuzhenich's minimum-support classification, Theorem 2(2); the Barnes–Wall norm gap, using Barnes–Wall, Broué–Enguehard and Nebe; the Masuda–Panov cross-polytope link lemma; Rasoolzadeh's complete cubic catalogue; the Kasami–Tokura and Berlekamp–Sloane low-weight Reed–Muller spectrum; and the Chiarelli–Hatami–Saks identity and Wellens restriction recurrence and tail. R3 = 10 is cited via Tarannikov–Kirienko and Krotov–Valyuzhenich. The checkers do not prove those universal classification or lattice premises.

A fallback **C44 < 2.0365511973** (about 2.0366) uses neither the round-seven nor the round-nine search. It uses round-eight inputs, the norm gap and round-ten sign completion. The round-ten Claude Science review removes one input at a time: deleting either the entire round-seven quintic ceiling or the round-nine ceiling changes R6 from 107 to 109 and its round-ten bound from 2.0111998310 to 2.0365511973; keeping only round-seven's h = 14 exclusion gives R6 <= 108 and 2.0261066981. Removing round-seven's quartic ceiling costs nothing. These are round-ten ablations, not asserted round-eleven decimals. The round-eleven review also reports R6 <= 109 and R7 <= 231 when either load-bearing ceiling is dropped.

No priority or optimality is claimed. No improvement of the lower bound is certified.

## Credit

Nisan and Szegedy; Chiarelli, Hatami and Saks; Wellens; BakeLab/Épi; Shinkar and Tal; Tarannikov and Kirienko; Krotov and Valyuzhenich; Rasoolzadeh; Valyuzhenich; Kasami, Tokura and Azumi; Berlekamp and Sloane; Barnes and Wall; Broué and Enguehard; Nebe; and Masuda and Panov. Source links and normalizations are in the retained proofs and `PRIOR_ART.md` files.

## AI use

Written and checked by AI agents under Ricardo Pinho's direction. AI agents prepared the proofs, certificates, checkers, release package and submission draft. Ricardo Pinho reviewed the results at summary level. This does not claim line-by-line human verification. There is no human referee; the candidate remains unrefereed and the asterisk stays.

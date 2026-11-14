# C49 round-one candidate certificate

This packet establishes the candidate lower bound

\[
C_{49}\ge R=(64728+\sqrt{3019700660})^{1/26}
>\mathbf{1.5678643845}
\]
(rigorous, `referee/exact_rates_integer.py`).

The displayed ten-place decimal is **ROUNDED DOWN**. The exact expression is authoritative. Here C49 is the asymptotic capacity of families of subsets with no sunflower of three distinct members, as defined in the pinned table reference below.

Koshta's exact incumbent is
\(R_0=(64728+\sqrt{3018723123})^{1/26}=1.5678599024\ldots\).
The exact margin is \(R-R_0\), strictly between
`0.0000044821482170935091180159147830749067693242554392250907328019176417`
and
`0.0000044821482170935091180159147830749067693242554392250907328019176419`.
These bounds are certified by integer surd comparisons in `referee/exact_rates_integer.py` and its retained and fresh outputs; no floating-point comparison decides the claim.

| Block | Members | N00 | N01 | N10 | N11 |
|---|---:|---:|---:|---:|---:|
| Koshta baseline | 252292 | 33969 | 64728 | 64728 | 88867 |
| Candidate | 252303 | 33980 | 64728 | 64728 | 88867 |

The block has 28 points and distinct ports 0 and 1. Replace the incumbent's 21 exceptional members by 32 seven-element sets, sixteen wholly inside each pendant: N00 increases by 11. The 252271 common members include all 250659 product members and all 806 lifted augmentation members at each pendant. The augmentation is not merely fifteen unlifted sets per pendant. The exact subtraction is in `certificates/best_delta.json`.

For port counts N_ab (first index: port 0, second: port 1), the transfer matrix is
`[[64728,88867],[33980,64728]]`, with Perron root `64728+sqrt(3019700660)`.
The DEGKM1997 Lemma 4.4 gluing statement pairs opposite port memberships in two Sperner, sunflower-free families on disjoint ground sets, then removes both glued points. The glued family remains Sperner and sunflower-free, and the retained-pair map is injective. Iterating fresh relabelled copies adds 26 points per block, giving at least c rho^k members on 26k+2 points for some c>0. Thus C49 is at least rho^(1/26). `PROOF.md` checks the hypotheses and supplies the argument from the producer's source statements and the referee's proof.

Our `checker.py` is **separately written (same agent)** from the search code. Its Cartesian-box check exhausts the actual certificate. The referee is **a clean-room AI referee on a different model (GPT-6 Astra)**, using its own decision-diagram checker. Its verdict is **HOLDS WITH CAVEATS**: the only caveat concerns rounding the decimal upward; the exact expression and the rounded-down decimal here resolve it. The referee's `REFEREE.md` and `PRIOR_ART.md` are preserved byte-for-byte, including their original historical terminology. See `referee/README.md` for archival scope. The release also includes transparent exact-arithmetic adaptations of the referee sources for the publishing lint; the original sources and report remain unchanged, and this is no additional referee review. `REPRODUCE.md` describes the adaptations and their output comparison.

This is a **candidate**, with **no human review**; **optimality not claimed**. It is a numerical improvement within the existing construction and gluing method. Did this packaging job find something new? **No.** The supplied round-one candidate beats the printed exact incumbent under the same definition; this job packages that result and makes no new-method or unrestricted priority claim. A second round found no improvement.

`REPRODUCE.md` gives standard-library Python verification and C++17 referee replay commands. `CLAIMS.json` maps the numerical statements above to evidence. `MANIFEST.json` records byte sizes and digests; `SHA256SUMS` seals the packet. Fresh runs are in `release_validation/`. Search sources and historical logs are supplied for provenance; no third-party code is included. Koshta's MIT baseline data and mathematical text needed for reconstruction have the byte-for-byte `LICENSE_KOSHTA` beside them. Aspect5 is cited only.

## References

- D. Koshta with Claude, incumbent two-pendant block: [certificate and mathematical proof](https://github.com/DennisKoshta/sunflower3-49a-certificate/blob/c4ee81737f9f6a4ae9793586a27004553a12d5c0/PROOF.md), commit `c4ee81737f9f6a4ae9793586a27004553a12d5c0`. Its table contribution was merged as teorth PR #260 at [commit `2d8eba58ea108f8cf746dbab8712ad317202d6c5`](https://github.com/teorth/optimizationproblems/commit/2d8eba58ea108f8cf746dbab8712ad317202d6c5).
- Aspect5 / Institute for Recursive Self Improvement (IRSI), [exact transfer construction](https://github.com/Aspect5/sunflower-free-capacity/tree/e478c81d8b57eba956fdaf621643eb6f0781f820). Cited only; no content from that unlicensed repository is included.
- joshua17-create with Claude, [F/H families](https://github.com/joshua17-create/sunflower-lower-bound/tree/6e34d78ab482f4cfd5a5ece62a6d06141e3e8c8d).
- Sylla, [pendant augmentation](https://github.com/xSyllaa/sunflower-pendant-chain/tree/8e21d0287711b4f0bfc23e9443523e2aa472cca1).
- W. A. Deuber, P. Erdős, D. S. Gunderson, A. V. Kostochka and A. G. Meyer, *Intersection statements for systems of sets*, J. Combin. Theory Ser. A 79 (1997), 118–132, Lemma 4.4. [DOI](https://doi.org/10.1006/jcta.1997.2778).
- [Tao table, pinned C49 definition and incumbent](https://github.com/teorth/optimizationproblems/blob/2d8eba58ea108f8cf746dbab8712ad317202d6c5/constants/49a.md).

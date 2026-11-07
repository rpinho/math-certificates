# HB16 — exact TOPTW certificate, pr11 with three vehicles

**Verified optimum: 654.** This closes the published unstarred 654 entry with an exact certificate. The public solution score is unchanged. Submitted for independent mechanical verification and separate priority/taste review; no first-discovery or relevance verdict is asserted by this worker.

## Published comparison

The strongest accessible public executable is Jan Ševeček's 2026 best-frequency2 SISR variant. Its [thesis, Table C.5, printed pages 66–68 / PDF pages 74–76](https://is.muni.cz/th/uuuxx/thesis.pdf), reports pr11 with three vehicles at 654. Its [public source](https://is.muni.cz/th/uuuxx/source.zip) was compiled unmodified; only the fleet size was set to three. It reproduced **654**, independently replayed against original raw data. The trivial insertion control scored **598**.

[Amarouche et al. 2020 supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0305054820301568-mmc1.pdf), Tables 9 and 20 (PDF pages 10 and 17), lists 654 **without a star**. Page 5 explicitly reserves stars for proven optima. Its four-vehicle value 657 is starred. The old official ResultsTOPTW workbook reports 628 for three vehicles; that is stale algorithm output and is not the comparison baseline.

## Exact result

The independently implemented raw C++ checker establishes

`1000 × score ≤ sum(node penalties) + 3 × 11082 = 656962`.

It checks 46,749 states and 1,180,957 transitions. Thus integer score is at most 656. Original raw prizes total 657, with minimum positive prize 3: omitting any customer loses at least 3, so neither 655 nor 656 is attainable. A separately written raw subset-score verifier confirms this, and a separate Fraction route verifier checks the public three-route solution scoring 654, visiting 47 customers and omitting node 19. Therefore **lower = upper = 654**. No solver-native optimality status is accepted. Fresh compilation and complete raw replay passed on phys in 1.45 seconds; replay from the saved Mini copy also passed.

The data are the [official MontemanniTOPTW1](https://www.mech.kuleuven.be/en/mim/op/instances/MontemanniTOPTW1) long-window Cordeau pr11, with 48 customers. An independent official download matched the input. This is classical TOPTW with service-start windows and travel rounded down to two decimals, not short-window pr01 or a capacity/mandatory-visits variant.

- Raw SHA256: `9f66f32dbf1108bf38a18387d4040d74b570f2875db8034a956a4f16d1205075`
- Proof SHA256: `392e14cc0354d50763e642d45943d0de3fe84061eeee972df5a184509c8641bf`
- Dual SHA256: `15942e3d13b4605296777b8ad2dc4a5fc877f05c6492af4e7bbd8e20b831141f`

## Mini files and reproduction

Root: `friends_pf_hugo/HB16_worker/`.

- `evidence/portable_pr11/`: raw input, primal routes, proof/dual, standalone independent C++ and Python verifiers, `reproduce.sh`, hashes, and original/fresh receipts. Under 1 MB.
- `evidence/strong_baseline/pr11/`: public solution, configuration and result, including the 598 control. Public method source: `evidence/sources/sevecek_source.zip`.
- `evidence/EXACT_PR11.json`, `evidence/BATCH_CONTROLS.json`, `evidence/A2_controls_replay.log`, `evidence/PORTABLE_REBUILD.json`: independent verification and controls.
- `PLAN.md`, immutable `ATTEMPT1.md`/`ATTEMPT2.md` and configurations, `PRIOR_ART.md`, `SWEEP.md`, `REPORT.md`, `FROZEN_FILES.json`: protocol, methods, source audit and exact commands.
- `BACKUP_RECEIPT.json` and `LOCAL_EVIDENCE_RECEIPT.json`: verified checkpoint and every-member hashes. Protected pod copy: `/workspace/hugo/RESULTS/HB16/`.

From `friends_pf_hugo`, run `python3 HB16_worker/replay_from_mini.py`, then `python3 _codex/friends_podsh.py phys HB16_worker/reviewer_poll.sh 40`. The first command transports the public package and launches a fresh build/replay on phys; the second polls it. Verification needs only GCC/Clang with C++17 and Python's standard library. No scientific computation runs on the Mini.

## Controls and attempts

The accepted route checker passed 48 exhaustive tiny weighted-route and three-route fixtures. The final prize verifier passed 100 exhaustive fixtures covering 3,798 thresholds and rejected five forged inputs: score, repeated customer, fleet, false upper and changed raw prize. Each public baseline rejected six malformed solutions. A2 additionally passed 48 signed-cut fixtures, high-bit/high-population checks, a negative-prefix false-proof regression and 24 circuit-model fixtures checked against exhaustive enumeration.

A1 used standard DW/ng pricing and stopped without closure: pr11 654–656. Its immutable report records the other unsuccessful panel cases and a baseline superseded by public rc201 = 1699. After the mandatory sweep, A2 used subset-row parity-strengthened masters and an original multiple-circuit formulation. Circuit presolve exposed the prize-gap argument, then independently derived and checked from raw inputs. The three SRI arms retained upper 656 and were stopped after exact closure. Owned parents and descendants were tracked and stopped. At most eight cores, explicit thread limits and nice 10 on phys; no other queue row, sealed hold-out, biology data or contact was involved.

## Worries and review boundaries

Gedik et al. 2017 reports two newly proved optima in its abstract. Its public university record is readable, but manuscript PDF requests returned 403, so its per-instance proof table was not authenticated. The 2026 Springer chapter full text was also inaccessible. These are priority gaps. The specific status evidence is the 2020 unstarred entry, corroborated by the later 654 score; this worker does not infer exhaustive absence of an earlier proof.

Final sources 1–3 were reread on 2026-11-03 at 14:28–14:36 UTC: official sources, recently updated GitHub search, primary SISR README, and six AI-result repository README/contents sources. GitHub code search was login-limited; branch/issues/PR retries were rate-limited. X was login-limited and Reddit returned 403. Receipts and limitations are in `evidence/final_sources/` and `PRIOR_ART.md`.

Credit: Ševeček and Pajersky/Sobotka/Rudova SISR primal methods; Dantzig-Wolfe/ng routing and Peng 2025; controlled HB10 proof machinery. The mechanical referee should challenge model identity, dominance, knapsack bounds and prize-gap composition. Separate taste review owns novelty, priority and relevance. This worker wrote no VERDICT, TASTE or FRIEND_NOTE and sent nothing externally.

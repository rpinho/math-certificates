# Clean-room replays of three starred 3a rows

These are replays of other people's finite certificates for the sum-difference constant on
[Tao's table, page 3a](https://teorth.github.io/optimizationproblems/constants/3a.html). They are not our results.
Each replay was written from the row's definition and the claimant's prose notes. The claimants'
code was neither read nor run; their data files were used only for comparison. The replays were
prepared with AI assistance (Claude) and fact-checked by a second model (GPT-6 Astra). No human
has reviewed them.

| Row | Claim | Replay | Folder |
|---|---|---|---|
| M2026 ([PR #236](https://github.com/teorth/optimizationproblems/pull/236), mizopl) | > 1.19230254 | PASS: θ ≥ 1.192302540705685029…, with n0 = 17074745018 and L = 50031092045455301 rebuilt from the page text and equal to the page's | [M2026/](M2026/) |
| Syl2026, k = 2 ([PR #238](https://github.com/teorth/optimizationproblems/pull/238), xSyllaa) | > 1.19281555 | PASS: θ ≥ 1.192815557092986…, margin 7.1·10⁻⁹. The cost histogram was rebuilt in full and is byte-identical to the claimant's | [Syl2026_k2k3/](Syl2026_k2k3/) |
| Syl2026, k = 3 ([PR #238](https://github.com/teorth/optimizationproblems/pull/238)) | > 1.19359680 | PASS conditional on the high-cost part (cost > 17500) of the claimant's histogram. That part was checked only statistically, and the low-cost part exactly | [Syl2026_k2k3/](Syl2026_k2k3/) |

Our M2026 value differs from the claimant's in the 15th digit because we use the denominator bound
4Bq^N/(q−1) instead of 5q^N. Both bounds are valid and both clear the claim. The counting
inequalities come from the claimants' prose notes and were tested by brute force on small
instances (`Syl2026_k2k3/toy_test.py`, `toy_result.txt`); this is not a proof. Whether a row keeps
its asterisk is for the maintainers.

## Run

Everything uses the Python 3 standard library only.

- M2026: `cd M2026 && python3 -I m2026_check.py` (about 5 s) and `python3 -I controls_m2026.py`. This needs no claimant data.
- Syl2026 k = 2: `cd Syl2026_k2k3 && python3 -I ghr_check.py k2 <dir>`, where `<dir>/data/k2_cost_hist.tsv` is the claimant's file from xSyllaa/c3a-controlled-carry-k2 @ ad16a46c (SHA-256 `4d16010f…6c63`). `python3 -I rebuild_hist.py 2 out.tsv 400 0` rebuilds it from scratch (about 65 s), and `my_k2_hist.tsv` is our rebuild.
- Syl2026 k = 3: `python3 -I ghr_check.py k3 <dir>` with `k3/data/k3_cost_hist.tsv` @ 5ca7cb88 (SHA-256 `3186f6e2…5c63`), then `python3 -I k3_partial_check.py 17500 300000`.

Controls that must fail are in `controls.py` and `controls_m2026.py`, with their results in the JSON files: a raised claim, a perturbed x, a small depth, and tampered histograms.

## References

- The 3a page and the PRs above. Arhan Canli's earlier independent replays are on [#236](https://github.com/teorth/optimizationproblems/pull/236), [#238](https://github.com/teorth/optimizationproblems/pull/238) and [#340](https://github.com/teorth/optimizationproblems/pull/340).
- mizopl/ghr-c3a-odd-base-finite-bound @ 464ceda9 (data used for comparison only) and xSyllaa/c3a-controlled-carry-k2 (prose note `k3/proof/THEOREM_k.md`; data only).

# HB17 — c104 TOPTW, four vehicles: exact optimum1260

Submitted2026-11-03 for independent mechanical and priority/taste review. **Worker verification passes; no referee verdict or novelty judgment is asserted.**

Published number and location: Jan Ševeček2026, best-frequency2 SISRs, [thesis](https://is.muni.cz/th/uuuxx/thesis.pdf), TableC.6 printed68/PDF76: c104m4=1260 (c103m4=1210). The retained actual PDF is `HB17_worker/evidence/sources/sevecek2026_actual.pdf`; some direct fetches returned an HTML challenge, recorded explicitly. [Public source](https://is.muni.cz/th/uuuxx/source.zip) and [SISRs repository](https://github.com/hankarudova/open-source-sisr-routing/tree/toptw) supplied the reproduced baseline. This is the strongest accessible executable baseline identified, with equal score1260.

Published proof status: [Peng etal2025 EJOR](https://doi.org/10.1016/j.ejor.2025.04.014), [accepted manuscript](https://lirias.kuleuven.be/retrieve/ec847f07-8b23-4cf1-9c91-b459df258a7a), §5.4 printed27 and Table6 printed29/PDF29. Its convention is bold=verified optimum, regular=best found; c104m4=1260 is regular with7200s, TaeKim dash/7200. Stored font extraction confirms the regular font. [Amarouche2020 supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0305054820301568-mmc1.pdf) Tables6/17 likewise list1260 unstarred. These specific sources establish the tracked open proof status, subject to the priority gaps below.

Own number: **lower=upper=1260** for the same official short Solomon c104 and at most four disjoint vehicle routes. This moves proof status; the heuristic score itself is unchanged. Official [library](https://www.mech.kuleuven.be/en/mim/op), [format](https://www.mech.kuleuven.be/en/mim/op/instances/TOPTWformat) and [raw archive](https://www.mech.kuleuven.be/en/mim/op/instances/righiniTOPTW2) were freshly checked. Raw SHA256 `931c01e136e690c05aeb9a62f7c4fcc095fa693e22ef67695abb19b3a548cc53`. Travel is Euclidean truncated to one decimal, windows constrain service start, depot return must meet closing time, no capacity constraint. No rounding/model substitution, sealed hold-out or biology data.

Verification: a separately written C++17 checker parses the original decimal raw file and checks a complete integer upper-bound closure, using no optimizer status or floating LP acceptance. With saved nonnegative node penalties u_i, weighted reward q_i=1000*p_i-u_i is at most181976 on each elementary feasible route. Hence four disjoint routes satisfy `1000*score <= sum(u_i)+4*181976 =1269996`. Original prizes have gcd10, so score<=1260. A separate Python Fraction checker verifies four feasible, disjoint routes with47 customers and score1260. The selected root certificate checks44,166 states/3,130,101 transitions. A second minU certificate checks49,803/3,492,392 and gives the same bound with numerator1269998. The portable verifier was freshly compiled, then replayed successfully again from the actual saved Mini bytes (about0.269s verification excluding compilation). The checker is independent code written by this worker; the independent referee has not yet reviewed it.

Mini artifacts, rooted at `friends_pf_hugo/HB17_worker/`:

- `evidence/portable_c104/`: raw c104.txt, primal.json, BEST.dual, BEST.proof, big_weighted_verify64.cpp, verify_primal.py, reproduce.py/sh and MANIFEST.json. Proof SHA256 `5ed028520eab35c7709ff60d9a8a9b98916aca054170d8dc0c0658aee5c3615b`.
- `evidence/EXACT_C104.json`, `MINI_SAVED_REPLAY.json`, `FRESH_BASELINE_REBUILD.json`, `RAW_IDENTITY.json`, `PUBLIC_SOURCE_IDENTITY.json` and `A1/`: exact checks, source/raw identity, fresh public baseline and both certificates.
- `evidence/code/batch_ng64_search.cpp`, `cg_A1.py`, `controls_A1.py`, immutable `config_A1.json` and `ATTEMPT1.md`: search, controls and frozen attempt. Public source.zip and all small code/data are retained in the verified checkpoint archive. Full search uses NumPy/SciPy and SISRs; proof replay needs only C++17/Python standard library.
- `PLAN.md`, `METHOD.md`, `PRIOR_ART.md`, `REPORT.md`, checkpoint/transport manifests: frozen bar, exact argument, source audit, reproduction and backups. Protected pod mirror: `/workspace/hugo/RESULTS/HB17/`.

Reproduce from `friends_pf_hugo` on the Mini, transporting computation to phys:

```sh
python3 HB17_worker/replay_from_mini.py
python3 _codex/friends_podsh.py phys HB17_worker/reviewer_poll.sh 45
```

Poll until complete. The saved package is rehashed and freshly compiled on phys under nohup/nice10; no local scientific computation. Worker jobs are stopped at handoff.

Controls: public best-frequency2 scores1210/1260 were reproduced before search, with independent raw replay, and reproduced again after a fresh unmodified source build. Trivial greedy insertion gives1100/1180. Each baseline rejects six primal forgeries. Upper verifier passed48 exhaustive fixtures spanning both metric conventions and exact four-route disjoint-mask DP, with96 false-upper/negative-penalty forgeries; additional cutoff controls and a61-node high-bit fixture pass. Removing the real proof's states is rejected (`root uncovered`). The receipt's legacy `exact_two_routes` label actually records fleet4; the first high-bit fixture exercised no high bits and was replaced transparently. See METHOD.md for these limitations.

What worries us: the correctness of ng-memory dominance and the elementary-route leaf-bound argument merits independent scrutiny despite exhaustive controls. Current exact result does not by itself settle priority. Final checks refreshed the official library, SISRs branch/issues/pulls, recent50 GitHub TOPTW repositories, named AI result indexes and last12months arXiv queries. GitHub code/X were login-limited; some AI trees were capped/incomplete. Gedik2017's detailed per-case exact-method table was inaccessible; the full2026 Springer heuristic chapter was also unavailable. No claim of exhaustive literature coverage or first proof is made. The separate priority/taste review must resolve these gaps. The frozen c103 panel stopped1210–1220 after c104 succeeded and is outside this claim. No contact or publication occurred.

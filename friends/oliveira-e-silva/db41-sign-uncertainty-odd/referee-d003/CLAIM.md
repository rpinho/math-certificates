# D003 claim: exact adjacent local cyclic minus jump at q7320/7321

Submitted for independent mechanical referee and separate Opus/Fable taste review. This worker does not judge novelty, priority, or whether the author cares.

Published number and location: Felipe Gonçalves, Diogo Oliveira e Silva, João P. G. Ramos, *New Sign Uncertainty Principles*, Discrete Analysis 2023:9, arXiv2003.10771v4, Problem3.1 (printed p22), Figure3 and caption (printed p40). Figure3 uses minus k120,q7081 and a minimum-tail-energy -1 DFT eigenvector. Authors used Gurobi/PARI; Table1's k68,q2245 is an older, smaller endpoint. Primary source: https://arxiv.org/html/2003.10771v4 . Bibliography/primary-source and current-repository audit: friends_pf_diogo/D003_worker/PRIOR_ART.md .

Our numbers, in precisely the original full even unitary-DFT, origin-sign and endpoint-normalized feasibility problem:

| q | N | certified exact A_minus_disc(q) |
|---|---|---|
| 7320 | 14641=121² | 121 |
| 7321 | 14643 | 122 |
| 7440 | 14881 | 122 |

The first two certify an adjacent local jump121→122 beyond Figure3's k120,q7081. They do not establish that7321 is the *first* q requiring122. No monotonicity assumption is used. The square point is the ell121 instance of Conjecture3.7; the paper reports numerical square tests only through ell100. No general conjecture or continuous bound is claimed.

Baseline reproduction: q7081,k120 feasibility PASSED at256-bit precision using the public sine construction, exact modular zeros and an independent ball-DFT cross-check. pod_backup/baseline_7081.json records the proof. This reproduces the published feasibility number, not the minimum-energy selection or an unreported energy value.

Code and data on the Mini: friends_pf_diogo/D003_worker/ . Executed pod code, exact rational seed JSON, all independent verifier receipts, search logs, environment and process audit are in pod_backup/ there. The key files are dual_7320_b2.json, dual_7321_b2.json, dual_7440_b2.json; verified_dual_7320.json, verified_dual_7321.json, verified_dual_7440_b2.json; verified_upper_7320.json, verified_upper_7321.json, verified_upper_7440.json. Complete proof: PROOF.md; reproduction: REPRODUCE.sh; summary: REPORT.md; hashes: MANIFEST.json. No large external data set is required.

How verified: verify_dual.py imports no optimizer/search code. It interprets stored decimal seeds as exact rationals, uses P=(I+D)/2, and defines g=P[h-E(E^TPE)^(-1)E^TPh]. A rigorous Arb solve certifies the correction matrix nonsingular and makes g(1..K-1)=0 exactly, Dg=g exactly. It checks g(0)>=0, all g(K..q)>=0 and g(q)>0 with a ball FFT. Self-adjoint DFT orthogonality contradicts any minus-feasible vector at K; see PROOF.md. After exact correction, strict tail lower margins exceed3e-5 at q7320,K120;2e-7 at q7321,K121;3e-5 at q7440,K121. Upper verifier verify_sine.py independently checks the entire tail and normalization by exact finite-sum formula, modular zeros and direct ball DFT. All cited receipts passed.

Controls and comparison: the authors' public sine construction with D045/D051's corrected common-index choice already gives A_minus_disc(q)<=ceil(sqrt(2q+1)); therefore larger feasible rows alone are not this claim. Matching rigorous lower certificates establish exact values which that control does not establish. At q5 the same procedure certifies the known exact value4: k3 lower obstruction and k4 upper both pass. A zero-margin k4 dual trial is rejected by the independent checker (exit2, no conclusion), controlling the positive-endpoint requirement. No sealed hold-out applies to this deterministic problem.

Compute/provenance: public code/data only on sharedcpu /workspace/diogo/D003, max four one-core processes, nice10 and thread limits1. Mini editing/transport only. All small results backed up; final pod ps audit has no search/verifier/controller workers. Wider variants were stopped once band2 certificates passed. No GPU request, contact, publication or friend message.

Worries/limitations: these are individual finite exact instances, not all-q theorems, a continuous improvement, or a globally first jump index. The baseline does not reproduce the energy-minimized Figure3 curve. The upper control is credited prior art, and the lower checker reuses the separately written D002 correction/ball verifier. The bounded public source audit located no superseding same-object table, but is not exhaustive. External novelty/taste and independent referee remain required. Do not send this to the author based on this worker's claim alone.

Final source1–3 recheck: 2026-11-02 20:49:46–47 UTC, official journal/arXiv, current GitHub searches and relevant issues/PRs, Epi/openai and DeepMind result catalogs; snapshots and inspected matches are in sources/final/. No superseding same-object table found in that bounded inspection. Credits: paper's LP/sine methods, SciPy/HiGHS, D002 projection/correction verification, D045/D051 common-index sine bound.

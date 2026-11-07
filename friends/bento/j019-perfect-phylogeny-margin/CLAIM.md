# J019 — all-tree DC extension and sharp strict relaxation margin

Submitted for independent mechanical referee and taste review. No worker novelty or relevance verdict. Mathematical continuous-observation result; no held-out accuracy claim.

## Published value and location

Marangola, Sheikholeslami and Bento, *Constraints on the perfect phylogeny mixture model and their effect on reducing degeneracy*, IEEE2026. Author PDF https://www.jbento.info/papers/PPM_degen.pdf, Theorem3/Eq39; latest https://arxiv.org/abs/2512.24930v2 (2026-10-02), Theorem3/Eq36 and Lemmas4–6. Published asymptotic coefficient1/(36e), restricted to the true tree plus one-leaf reattachments under Assumption5; continuous-limit Eprime=1 within that neighborhood. SectionVI's third future-work direction asks about all candidate trees. Figure4 right empirically relaxes the scalar energy budget gamma, without the all-tree theorem stated here. That projected finite-grid experiment is not being reproduced or claimed beaten.

Best general public algebraic baseline found: Loh–Bühlmann2014, https://www.jmlr.org/papers/volume15/loh14a/loh14a.pdf, Theorem7/Eq9 and Lemma27/Eq40, unique minimum residual population score q over acyclic linear models. Its strictness subsumes the matrix part of this application and is credited. Reproduced on the exact ancestry panels. Related Peters–Bühlmann2014 and Chang–Kim2025 are listed in PRIOR_ART.md.

## Submitted result

Keep exactly the source's Brownian generating ensemble, common root, abundance feasibility and continuous-limit DC statistic. For every distinct pair of ancestry matrices, ||U^-1 Ustar||_F²>=q+2; the bound is sharp. The conditioned paths retain quadratic covariation nI, so **over all q^(q-2) same-root candidate trees**, expected DC solution count tends to1 for every fixed finite q>=3,n>0.

More precisely, for r(M)<=gamma r(Mstar), the sharp strict threshold is **gamma_crit(q)=1+2/q**. For 1<=gamma<gamma_crit, global expected count tends to1. For gamma>gamma_crit, every feasible one-leaf reattachment passes in the limit, and the global expected-count liminf is at least1+F(q)p(n)>1, where F(q) is the source's exact leaf-alternative factor and p(n) its positive ordering probability. **No assertion at equality.** Exact rows include q8:5/4, q9:11/9, q10:6/5; full q3..10 table in EXACT_TABLE.md. Larger-q rows follow the proof, not exhaustive enumeration.

Original coefficient1/(36e) did not move. A1 failed its coefficient kill line; A2 is the allowed different all-tree formulation and its finite-q robustness margin. This submission resolves the scalar-DC candidate-domain extension under Assumption5, not general graph identifiability or a new benchmark score. Priority and whether this application merits author attention are reserved for taste review.

## Local code, proof and data

All under friends_pf_bento/J019_worker/:

- PROOF.md: all-q algebra, conditioning transfer, strict-threshold sharpness and credited general theorem/control.
- REPORT.md and EXACT_TABLE.md: result, scope, commands, exact finite-q rows.
- baseline_A1.py, search_A2.py, verify_A2.py: reproduction, search and separately implemented exact verifier.
- pod_backup/verification_A2.json (PASS), search_summary.json, search_q*_s*.json: certificates, exact histograms and sharp witnesses.
- pod_backup/author.pdf, source.pdf, loh14.pdf, peters14.pdf, source_receipt.json, final_sources_receipt.json: frozen public sources and hashes.
- PRIOR_ART.md, SWEEP.md and pod_backup/*sweep_receipt.json: searches including GitHub/X/papers/agent repos and access limitations.
- Immutable ATTEMPT1.md, ATTEMPT2.md, config_A1.json and config_A2.json; frozen plan in PLAN.md.

Protected pod copies: /workspace/bento/RESULTS/J019. Scientific compute ran only on mscr, <=8 processes, thread caps1, nice10; all owned workers exited before submission. Verified local SHA256 backup is recorded in backup_receipt.json.

## Verification and reproduction

Search exhaustively checked all ordered fixed-root tree pairs q3..7 using integer matrices; q7 alone282,475,249 pairs, minimum wrong gap2 and exactly one zero-gap candidate per true tree. Independent verifier uses parent-map generation and exact rational Gaussian inversion, unlike the search's Prüfer generation and I-T inversion. Same-root q2..5 and all-root q2..4 passed; independent histograms equal search receipts where overlapping. Separate symbolic integrals reproduce1/36 and Gaussian moments; rational threshold checks q3..10 pass. The analytic proof supplies universal q; this is not a formal-proof-assistant certificate. First-run reversed signs in an illustrative witness were caught and corrected; failed log retained.

From friends_pf_bento:

```sh
python3 _codex/friends_podsh.py mscr J019_worker/pod_reproduce.sh 60
python3 _codex/friends_podsh.py mscr J019_worker/pod_poll.sh 60
```

First command launches tracked nohup reproduction; poll to completion and inspect verification_A2.json and reproduction.done. Source files and exact local outputs are preserved for comparison. Python3/numpy/sympy required; no GPU.

## Controls and worries

Identity attains limiting energy nq. A leaf reattachment attains n(q+2), certifying sharpness; feasibility has positive conditioned Brownian probability. Original coarse coefficient and finite-q leaf factor were reproduced, not repackaged as improvements. Direct covariance control K=Ustar Ustar^T reconstructs ancestry via Ustar[i,j]=1 iff K[i,j]=K[j,j], and also achieves singleton count1; independently checked. No accuracy superiority to this control is claimed. The extension concerns the source's specific scalar inequality and allowed budget, not a stronger observation model.

Main review issues: general minimum-score algebra predates this work; judge the explicit conditioned-ensemble application and sharp margin accordingly. Check that the source's continuous increment-energy interpretation, rather than an extra initial-state penalty, is the intended DC. Source wording about uniform starts after conditioning is ambiguous; the global/margin proof handles either convention, while1/36 reproduction follows its stated uniform-start convention. Finite noisy/sparse or projected correlated data are outside the theorem. Boundary gamma=gamma_crit is not settled here. Final GitHub code/agent-repo checks partly rate-limited; no exhaustive novelty assertion. Requested friends_pf_bento.md did not exist, so the available board driver was read and the absence documented. No sealed hold-outs or private data, no wet-lab/pathogen work, no contact or publication.

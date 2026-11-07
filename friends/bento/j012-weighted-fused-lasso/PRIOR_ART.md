# Independent referee source record

Started 2026-11-03 UTC, before writing referee code. This is a correctness audit, not a novelty assessment.

1. Primary result / live table: no competition leaderboard applies. Bento–Furmaniak–Ray, arXiv:1801.04987v3, Eq.(2), Theorems 2–4, gives unrestricted positive-weight path complexity Theta(n^2), equal-weight T <= n, counting maximal affine intervals of the scalar-parameter solution path. Read https://arxiv.org/html/1801.04987v3 directly. Fig.1 supplies a reproducible nonmonotone baseline. Independent exact reproduction is pending.
2. Public code: indexed searches `"weighted fused lasso" github` and `"weighted fused lasso" "2026"` found https://github.com/bips-hb/wFLSA-paper and https://github.com/bips-hb/wflsa (ADMM for fixed parameters). Updated GitHub repository search and author-code issues/PRs will be recorded separately from the pod. No solver code is imported in this audit.
3. AI-lab/agent results: indexed search combining the problem with BakeLab, alphaevolve_results, openai/math, EinsteinArena, erdos, kisonecat found no matching restricted-envelope theorem. This is an incomplete indexed search, not evidence of absence.
4. Papers: the stronger simple control is Tibshirani–Taylor (2011), The Solution Path of the Generalized Lasso, https://www.stat.berkeley.edu/~ryantibs/papers/genlasso.pdf : diagonal dominance of D D^T implies the boundary lemma. For D=diag(alpha) times chain differences it gives 2 alpha_i >= alpha_(i-1)+alpha_(i+1), with zero padding. Direct primary reading pending PDF retrieval. The 2025 wFLSA ADMM work solves a different computational question. A 2026 paper, https://proceedings.mlr.press/v306/le26f.html / arXiv:2602.02406, concerns multiple hyperparameter learnability; full relevant passage to inspect.
5. Community: indexed queries for the problem with Reddit / X / blog / concavity and for `"weighted fused lasso" "least concave majorant"` found no directly relevant new bound. No accounts, messages, or nonpublic sources used.

Author identity: https://jbento.info/ explicitly lists the paper with Furmaniak and Ray; its Boston College affiliation matches the primary arXiv paper. The author's public PDF is https://www.jbento.info/papers/1dwfl.pdf .

What would be added relative to the primary paper: an explicit O(n(k+1)) sufficient-family bound where k counts strict deficits below the zero-padded weight profile's least concave majorant. The already-known k=0 concavity case alone would not establish that addition. No priority or taste conclusion is made.

Final source reading and reproduction, 2026-11-03 02:26–02:31 UTC:

- Independently reproduced Fig.1 exactly (T=5; knots 25/27,25/23,100/73,25/4), its equal-weight control (T=3), and the printed Theorem 4 inputs for n=3,...,10. All computations ran on phys.
- Read the full relevant generalized-lasso passage: Section 6, Eq.(23), confirms the diagonal-dominance control. Read 2026 paper Section 8.2 and Appendix G.2: its 3^(d-1) signed-box-state count and O(d^2) pseudo-dimension result do not state an envelope-deficit path bound. These are prior results to credit, without making a priority assessment.
- Independent public GitHub search sorted by update returned bips-hb/wflsa (2025) and bentoayr/simple_fused_lasso_solver (2023); adding 2026 returned no repository. Subsequent repo/issues/PR/commit API requests were rate-limited (403). The public repository page read through web shows one commit and zero issues/PRs, but that indexed page is older; I do not treat it as a fresh API confirmation. The claimant's successful API check is data, not my independent result.
- Raw primary HTML, author page, generalized-lasso PDF, 2026 HTML, repository search JSON, and independent source receipts are copied into evidence/. GitHub code search and indexed AI-lab/community coverage remain incomplete. No claim of exhaustive novelty checking is made.

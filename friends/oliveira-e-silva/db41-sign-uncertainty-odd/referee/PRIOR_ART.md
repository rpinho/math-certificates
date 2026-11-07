# Prior-art and primary-source audit (2026-11-02)

Independent referee, not a novelty search or improvement project. No computational code has yet been written.

Primary target: Gonçalves, Oliveira e Silva, Ramos, *New Sign Uncertainty Principles*, arXiv:2003.10771v4, Section 3.1, Proposition 3.6 and Conjecture 3.7; https://arxiv.org/html/2003.10771v4 and https://discreteanalysisjournal.com/article/84266-new-sign-uncertainty-principles .

The submitted claim says the published sine construction proves the upper bound ell at odd-square group size ell^2; the submitted universal lower bound is the object of this audit. Primary definitions and numerical scope remain to be checked.

Before independent computation, check: official article and any corrections; recently updated public GitHub results and issues; BakeLab/Epi-results, DeepMind alphaevolve_results/repository_of_problems, openai/math, EinsteinArena, plasma-ai/erdos, kisonecat/openai-math; recent arXiv and primary references; public community searches. Record search limitations honestly. No contact or account creation.

Baseline reproduction will use an independent implementation of the paper's original operator and the published sine upper construction on the authorized stats pod only. Source and audit receipts will be added below.

## Initial read and search, before scientific implementation

- Read the live arXiv v4 HTML, latest abstract, and official journal. Equations (3.1),(3.3), Proposition 3.6 and Conjecture 3.7 match the target. No separate live scoreboard exists in the supplied source: the published baseline is the sine upper ell and numerical equality through ell <= 100, not a universal lower theorem. The journal identifies Diogo Oliveira e Silva among the three authors.
- Queried public web search for exact title, paper number, Conjecture 3.7, cyclic/square/discrete variants, GitHub and 2026. Tried GitHub repositories sorted by updated and paper-number issues sorted by updated; those web fetches failed (cache miss). This is incomplete anonymous coverage, not evidence of absence.
- Read public landing pages of https://github.com/BakeLab/Epi-results , https://github.com/google-deepmind/alphaevolve_results , https://github.com/google-deepmind/alphaevolve_repository_of_problems , https://github.com/openai/math , https://einsteinarena.com , https://github.com/plasma-ai/erdos , https://github.com/kisonecat/openai-math . Grouped exact-topic searches found no same-object result in these catalogs; landing-page coverage is bounded.
- Recent arXiv searches found Ismoilov, https://arxiv.org/html/2606.02299v1 , on fixed-degree trigonometric polynomials with a measure/integral constraint, and Lee, https://arxiv.org/abs/2608.15415 , on continuous plus-sign bounds in dimensions divisible by four. Neither abstract states the present cyclic minus-square theorem. Ismoilov's actual introduction was read; no priority inference is drawn.
- Searched public X/Reddit/Discord and blog-indexed results with the exact discrete topic. No settling same-object primary source appeared. No account creation or contact.
- Related public formalization seen: https://github.com/seewoo5/cohn-elkies-refactor (continuous sphere-packing/sign-uncertainty work). It is not the finite cyclic target.

The submitted proof and prose outputs were read, but its computational search/verifier sources were not read or imported. The independent baseline will reproduce the paper's analytic sine construction because no matching public executable was located. This referee makes no novelty, priority or record claim.

## Direct source receipts

Anonymous GitHub API requests succeeded after the web-fetch failures. Retained github_updated.json (13 repositories, sorted updated), github_issues.json (paper-number issue search, zero), github_paper.json (paper-number repository search, zero), github_discrete.json (one unrelated interval-DFT repository), and github_square_issues.json (noisy broad results, not evidence of absence). The most recently updated relevant-looking repository was Roni-Edwin/Fourier-numerical-computations (2026-11-01); its README actually concerns a continuous radial L2/L1 norm ratio, not the present finite sign threshold. README retained in public_code_README.md. Other results included the continuous plus-sign constant and Cohn-Elkies formalization.

Fetched the actual public raw arXiv source archive to primary_source.tar and extracted only oliveira2023.tex to primary.tex; also retained primary_v4.html. The raw source confirms the same origin and endpoint constraints, sine upper, numerical ell<=100 statement, and open lower question. The submitted proof SHA-256 matches the frozen claim manifest (91643ffe...42ee8).

## Final recheck, 2026-11-02

All 11 fresh direct public requests returned HTTP 200; URL, UTC, size and SHA-256 receipts are retained in final_public_receipts.json, with downloaded pages under final_public/. The latest abstract still reports v4 (2023-07-20). Rechecked updated GitHub repositories, paper-number issues, and the seven catalog entrypoints. No uncertainty match appears on the six GitHub landing pages; this is explicitly not a recursive code audit. EinsteinArena's similarly named problem uses Laguerre polynomials/double roots and a real sign-change objective, not this finite cyclic formula: https://einsteinarena.com/problems/uncertainty-principle . Its displayed leader is CLOADEX25-DevinWright at 0.313093; that unrelated value is not used as a baseline here.

Final exact-conjecture/cyclic-square and awesome-list searches produced no additional same-object primary result in the bounded returned set. Recent Ismoilov/Lee and continuous formalization work remain related sources only. No assertion of novelty or author interest is made. The actual paper's prior sine upper and conjectured equality, and the submitted driver's earlier finite D003 baseline, are distinguished from the proposed uniform lower proof.

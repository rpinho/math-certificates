# Independent referee audit: bento_J019

The mathematical result survives the audit for the source's explicit continuous
increment-energy interpretation. Its scope is fixed finite q and time horizon n>0,
with grid resolution N tending to infinity. There is no improvement of the source's
1/(36e) coefficient and no finite-grid accuracy claim.

I read RULES.md first and wrote PRIOR_ART.md before constructing the independent
checker. All scientific computation ran on mscr at nice 10, with one process and
one numerical-library thread per task. No claimant search or verifier was read or
imported. The claimant's output histograms were loaded only after independent
results existed, for comparison. Both complete histograms agree for q=3,...,7.

The code generates undirected edge subsets, tests connectivity, and orients each
tree from root 0. This differs from both claimant generators. It computes the
candidate abundance through the paper's descendant identity
M_i = F_i - sum_{j a direct child of i} F_j,
and computes its exact integer energy using descendant-intersection counts.
No floating point matrix inversion enters the exhaustive results.

Independent exact checks:

| q | Trees with root 0 | Ordered pairs | Minimum wrong gap |
|---|---:|---:|---:|
| 3 | 3 | 9 | 2 |
| 4 | 16 | 256 | 2 |
| 5 | 125 | 15,625 | 2 |
| 6 | 1,296 | 1,679,616 | 2 |
| 7 | 16,807 | 282,475,249 | 2 |

Each true tree has exactly one minimum-score candidate. Every gap is even.
Constructive rational witnesses check the sharp ratio (q+2)/q for q=3,...,40;
these larger rows are witnesses, not exhaustive enumerations.
The mean leaf-alternative counts equal the source's F(q) exactly on every panel.

The all-q proof also checks out. B=U^{-1}Ustar is an invertible integer matrix,
so its q nonzero columns have total squared norm at least q. Equality forces a
signed permutation. Since UB=Ustar has nonnegative entries, the signs are positive.
The diagonal of Ustar then makes each vertex an ancestor of its permuted vertex
in U; a nontrivial permutation cycle would violate antisymmetry of ancestry.
Equality therefore requires U=Ustar. With a common root each column of B sums
to 1, so its squared norm is odd. A nonzero gap must consequently be at least 2.
Every leaf move attains 2. This proves the all-q part without extrapolating from
finite enumeration.

Under the unconditioned Brownian law, G_N=sum Delta M Delta M^T converges to nI.
For fixed positive starting vector x, survival has positive probability
s(x)=product_i erf(x_i/sqrt(2n)). Thus P(A|survival,x)<=P(A|x)/s(x), which transfers
convergence to the conditioned law. Integrating over x uses bounded convergence;
no independence of conditioned increments is assumed. There are finitely many
candidate trees for fixed q. Hence all wrong energies exceed the true energy
simultaneously in the limit, even before applying nonnegative-abundance feasibility.
Below gamma=(q+2)/q the strict separation remains. Above it each feasible leaf
move passes; a tube around strictly ordered positive constant paths has positive
Brownian survival probability. Its expected count contribution is F(q)p(n)>0.
This establishes both strict sides and does not settle equality.

Independent symbolic integration of the killed half-line kernel determinant
reproduces the leading ordering coefficient 1/36, also under the alternative
annealed conditioning of the initial uniform mixture. The source's coarse
coefficient is therefore 1/(36e) in the appropriate large-q limit. Independent
Gaussian moments reproduce the source comparison's mean 1 and variance 6.

A diagnostic sampled 3,000 exact survival-conditioned Brownian grids at each
N=8,32,128,512,2048, using bridge-survival rejection to account for between-grid
crossings. At q=3, gamma=3/2 the candidate energy acceptance decreased from
0.3573 to 0; at gamma=11/6 it increased from 0.667 to 1. This is supporting
numerical evidence only; the proof establishes the limit. The diagnostic fixes
positive initial values, while the proof covers their distribution.

The trivial control ties the claimed identification: observed quadratic
covariation gives K=Ustar Ustar^T; ancestor(i,j) iff K_ij=K_jj. This recovered
every tree on every panel. The all-candidate score strictness is already a
special case of Loh–Bühlmann (2014), Theorem 7 and Lemma 27; that theorem was
read in its primary JMLR PDF. The contribution relative to the PPM paper is the
explicit application to every same-root candidate and the sharp strict scalar
relaxation margin. These are facts about the relationship of the statements,
not a priority or significance judgment.

The strongest scope objection is the energy convention. The paper's general
r(M) definition includes a first-sample term without fully specifying it, but
its explicit Brownian limit uses increments alone. I checked a counterexample
to adding ||M(0)||^2: true star, candidate 0->1->2, x=(1/10,9/10,1/5), n=1/50.
The increment gap is +1/25, the initial penalty gap is -6/25, and total gap -1/5.
An open set of strictly feasible paths has positive probability, so that altered
statistic would invalidate singleton recovery at gamma=1. This does not refute
the submitted claim, which expressly uses the source's increment-only limit.
An explicit finite-N bound would be the next substantive verification target.
The projected finite-grid generator in the source is outside this theorem.

Authorship and source version were independently checked against arXiv v2 and
Bento's publication page. Fresh author/arXiv PDFs have exactly the same hashes as
the frozen claimant PDFs. No held-out data are involved: this is an all-ensemble
proof and exhaustive diagnostic, not a trained prediction system. The submitted
plan likewise freezes a mathematical panel and disclaims a hold-out experiment;
there is no hold-out score or contamination advantage to audit.

Primary sources, accessed 2026-11-03:

- https://www.jbento.info/papers/PPM_degen.pdf — Section V-C, equations 30–39,
  Assumptions 4–5 and conclusion; note numbering differs from arXiv.
- https://arxiv.org/html/2512.24930v2 — equations 28–36; its explicit Brownian
  increment definition is equation 34 and source theorem is equation 36.
- https://arxiv.org/abs/2512.24930v2 — author list and version date.
- https://www.jbento.info/ — author publication listing linking the same paper.
- https://www.jmlr.org/papers/volume15/loh14a/loh14a.pdf — Theorem 7, Lemma 27.

Reproduction from this directory on the Mini (transport/launch only):

```sh
python3 _codex/friends_podsh.py mscr pod_run.sh 60
python3 _codex/friends_podsh.py mscr pod_poll.sh 60
python3 _codex/friends_podsh.py mscr pod_compare.sh 60
python3 _codex/friends_podsh.py mscr pod_boundary.sh 60
python3 _codex/friends_podsh.py mscr pod_boundary_poll.sh 60
```

The launch scripts embed the independent code and tracked nohup jobs. The pod
provides Python 3, numpy 2.1.2, sympy 1.13.3, scipy 1.18.1. Full source receipts,
executed code, logs, exact histograms and comparison are backed up in evidence/;
manifest.json records each SHA256. No certificates depend on continuing pod storage.

Completion receipt: both tracked workers exited; pod folder totals 3,217,904 bytes,
well below 1 GB. No large intermediates were created. All 13 archived evidence
files passed local SHA256 verification after copying. See evidence/finish_receipt.json.

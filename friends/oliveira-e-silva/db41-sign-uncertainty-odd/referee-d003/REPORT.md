# Independent referee evidence for diogo_D003

The three claimed exact values pass a verifier written here independently of the claimant's search and verifier code. Verdict: HOLDS in the stated finite feasibility problem. No novelty, priority or author-interest judgment is made.

| q | N=2q+1 | lower obstruction at k | upper feasibility at k | exact A_minus_disc(q) |
|---|---|---|---|---|
| 7320 | 14641 | 120 | 121 | 121 |
| 7321 | 14643 | 121 | 122 | 122 |
| 7440 | 14881 | 121 | 122 | 122 |

## Primary-source meaning

Read the official [paper](https://arxiv.org/html/2003.10771v4), its PDF and [journal record](https://discreteanalysisjournal.com/article/84266-new-sign-uncertainty-principles). All three authors, including Diogo Oliveira e Silva, are confirmed. The arXiv HTML visually loses two authors from its main heading, but its metadata, PDF and journal agree.

Equation (3.1) and Problem 3.1 define the even unitary DFT on N=2q+1 coordinates. For the minus case the requirements are f(0)>=0, Df(0)<=0, both f and -Df nonnegative on k<=|n|<=q, and both endpoints at least 1. The independent checks use exactly these requirements and the full-vector inner product, with weight 2 on positive half-vector coordinates.

Figure 3 explicitly reports k=120,q=7081, a minus DFT eigenvector, f(0)=0 and minimum tail energy. The reproduced baseline here proves feasibility at that index using sine sums. It neither reproduces the plotted vector nor establishes its energy minimum. This agrees with the submitted claim's explicit limitation. Table 1's older endpoint is not the comparison used here.

## Independent proof and computation

`independent_check.py` imports only standard libraries, python-flint, and (for the small diagnostic LP) NumPy/SciPy. No claimant Python file was opened, executed or imported. The four files in `inputs/` are copied JSON data. Stored decimals are interpreted as exact rational numbers. The verifier is SHA256-addressed in every receipt and in `pod_evidence/evidence_hashes.json`.

All mathematical computation ran on the designated shared pod inside `/workspace/ref_diogo_D003`, at nice 10 with one thread. Initial free disk: 31,729,053,696 bytes. Local operations were source reading, writing, transport, archive extraction and hashing only.

For each lower bound, form the exact DFT D from the paper and let E embed coordinates 1,...,k-1. The code constructs B=(I+D) restricted to these coordinates directly with Arb cosines at rational multiples of pi. A determinant interval excludes zero. A rigorous LU solve encloses the exact x satisfying Bx=(h+Dh)_inner. Define r=h-Ex and g=r+Dr. Thus g_inner=0 exactly by this equation and Dg=g exactly by D^2=I on even vectors; numerical near-zeros are not used as proof. Direct interval cosine sums check every remaining coordinate, including g(0)>=0 and g(q)>0. No FFT is used.

If any original feasible f existed, u=(f-Df)/2 would be a minus eigenvector with u(0)>=0, nonnegative k-tail and u(q)>=1. DFT self-adjointness makes the full inner product <u,g>=0. Exact inner zeros and all certified signs instead make it at least 2*u(q)*g(q)>0, a contradiction. This covers the original unrestricted feasible f, not just a constrained eigenvector search.

At 320 bits, all lower signs passed. Our g is twice the claimant's projected g. Its minimum tail lower bounds exceed 6.4803e-5, 4.6787e-7 and 6.0192e-5 at q=7320,7321,7440 respectively. The correction determinants are positive and well separated from zero. Receipts: `pod_evidence/receipts/lower_*.json`.

For upper bounds, independently define w(j)=sin(2*pi*|j|/L) for |j|<L and zero elsewhere, and v=w-Dw. Pairing j with L-j gives v(0)=0 exactly; Dv=-v. Direct Arb cosine sums check every tail coordinate. When N divides L*n, product-to-sum and complete sine-cycle cancellation prove an exact zero; no tolerance declares a zero. The endpoint is strictly positive, so exact scaling by 2/v(q) satisfies both endpoint constraints. All three upper witnesses and the baseline passed. The upper method is the authors' Proposition 3.6 sine construction with the common-index choice already credited in the claim; it is a trivial control, not an added upper-bound result.

At q=5, a separate direct LP on the original f,Df constraints rejected k=2,3 and accepted k=4,5; separate rigorous certificates prove the exact value 4. Five negative controls all exited 2 as required: zero seed, reversed-sign seed, exclusion at feasible k=4 for q=5, and exclusion at feasible k=121/122 for q=7320/7321. The zero seed has nonnegative tails but endpoint zero and is rejected. Floating LP status is only diagnostic.

There is no sampled data or held-out test set in this deterministic finite problem. Search-dependent choice of q does not invalidate a proof for those explicitly fixed q, and does not support generalization to other q.

## Reproduction

From this directory, using the provided transport helper:

```sh
python3 _codex/friends_podsh.py ref pod_setup.sh 90
python3 upload_and_start.py
python3 _codex/friends_podsh.py ref upload_and_start.sh 90
python3 _codex/friends_podsh.py ref poll_checks.sh 90
python3 _codex/friends_podsh.py ref run_controls_launch.sh 90
python3 _codex/friends_podsh.py ref poll_controls.sh 90
python3 copyback.py
python3 _codex/friends_podsh.py ref cleanup_pod.sh 90
```

Poll to completion before copyback. Exact executed pod commands are also retained in `pod_evidence/run_checks.sh` and `run_controls.sh`. Python 3.12.3; python-flint 0.9.0; NumPy 2.1.2; SciPy 1.18.1. Controller PIDs 945763 and 946026 finished; the retained audit found no referee workers. `pod_cleanup_receipt.txt` records removal of temporary dependencies and the pod's final retained size.

## Literature facts and limits

`PRIOR_ART.md` and `sources/` contain the bounded audit with dated fetch hashes. The official source reports square tests only through ell=100 and conjectures the general square equality. Relative to that paper, this submission supplies rigorous matching lower certificates at three specified larger q, including the ell=121 square and an adjacent local 121-to-122 change. Its upper construction is already explained by the sine control. No uniform lower bound, continuous improvement or energy optimum follows from these three certificates.

Recently updated public repositories and 2026 papers located in the audit concern continuous plus uncertainty, trigonometric degree constraints or Krawtchouk asymptotics. For example, tejasvi/sign-uncertainty-constant reports continuous 0.5502<A_plus(1)<=0.5509; Station arXiv:2608.23691 concerns the continuous plus product constant. These are not the finite cyclic minus quantity. No superseding same-object table was found in the bounded inspection; repository/catalog searches cannot prove absence. A final independent source 1-3 recheck is retained in `sources/final/`.

The strongest author objection is scope: three anticipated finite instances and a prior-art upper construction do not explain or prove the general lower-bound pattern. The next substantive bar is a uniform lower-bound proof for every admissible square N=ell^2 (odd ell>=3), resolving the lower-bound side of Conjecture 3.7.

Shipped: referee verdict HOLDS. PROOF.md correctly proves Selvaraja's Conjecture 5.9 (conj:skew, close-skew length ≤ 2^r, sharp) and Conjecture 3.6 (conj:theta, θ(VR(I_n;r)) = 2^r) for all n > r ≥ 1. No novelty check was possible: the job ran with no network access.
VERDICT: HOLDS
CONTROLS: no assumption overrode a control. All 12 mutation checks in `referee_verify.py` detect their targeted failure, and all positive controls pass (output below, `SUMMARY: 0 failures`). The mutants: char 3 breaks (1+u_h)^2=1 and u_h^2=0; forward doubling of the one-sided example v=[0,1], w=[6,2] (n=3, r=1) is not skew; appending (p,q) breaks the Lew list on graph nv=4 mask=13; dropping the diameter condition gives k=2^{r+1} with a non-isotropic span, for each r=1..4 and n=r+1,r+2.
CONTRADICTING: none found. The exhaustive and recurrence computations gave d'(VR(I_n;r)) = 2^r in every computed case: (2,1),(3,1),(3,2),(4,1),(4,2),(4,3),(5,2),(5,3). Reversed doubling is skew for all 871 close-skew lists, including the empty list for each parameter pair, on (2,1),(3,1),(3,2), and T(H) ≤ s(H) holds on all 164 test graphs. No output was dropped. The full log is reproduced by the command below.
LABELS: none trusted without a check. Every definition PROOF.md uses was compared verbatim with the v1 source (lines 501–510, 800–809, 1034–1036, 1892–1897, 1531–1536). PROOF's four source-line citations (982–992, 828–841, 938–949, 1514–1526) were opened and match what is claimed.

# Referee report: PROOF.md vs S. Selvaraja, arXiv:2611.20820v1

Model: claude-opus-5-5. Clean room: my only inputs were Selvaraja's v1 paper and the producer's proof. I used no producer code and no network.

## Did the producer find something new?

**Yes, subject to a novelty recheck.** The paper (v1) states both conjectures as open. It says they were known only for r ≤ 2 and for n = r+1 (tex l.1917–1918). PROOF.md settles both for every n > r ≥ 1. Per the paper's own implication (l.1039–1041, 1914–1916), this also proves Shukla's conjecture coll(VR(I_n;r)) = 2^r. With no network access I could not check whether a later version or another paper got there first. That must be checked before any public claim.

## Line-by-line audit

### §1 Reversed doubling: correct
The list is (v_1,w_1),…,(v_k,w_k),(w_k,v_k),…,(w_1,v_1). Index the positions 1..2k. For p < q, the pair (a_p, b_q) falls into one of three cases:
- Both in the first half: (v_p, w_q) with p<q. The witness condition d(w_q,v_p) ≤ r for p<q (tex l.1896) applies directly.
- p in the first half, q in the second: b_q = v_j for some j, so the required comparison is d(v_p, v_j) ≤ r. That is the diameter hypothesis, which covers j = p (distance 0).
- Both in the second half: a_p = w_i and b_q = v_j with i = 2k+1−p and j = 2k+1−q. Then p<q gives i>j, and d(w_i,v_j) ≤ r for j<i is again the witness condition.

The diagonals of both halves are d(v_i,w_i) ≥ r+1. So the list is skew in the sense of Hypothesis (S_r) (tex l.341–343), with the same index direction i<j, and 2k ≤ 2^{r+1} gives k ≤ 2^r. Reversing the second half is essential. Forward doubling fails on the one-sided example found by the verifier.

Sharpness: v=(x,0,0…) and w=(x̄,1,0…) give d(v,w)=r+1, d(v,v')=d(x,x') ≤ r, and d(w,v') = r+1−d(x,x') ≤ r for x≠x'. This works for every n ≥ r+1. It is the same construction as the paper's (l.1899–1904). Verified for r=1..4 and n up to 6.

### §2 Binary skew bound: correct
- In characteristic 2, u_h^2 = Σ t_{hj}^2 e_j^2 + 2·(cross terms) = 0, so (1+u_h)^2 = 1. A is commutative, so P_xP_y = ∏_{h∈x∩y}(1+u_h)^2 ∏_{h∈xΔy}(1+u_h) = ∏_{h∈D}(1+u_h).
- Threshold identity: L(∏_{h∈D}(1+u_h)) = Σ_{S⊆D,|S|=s} perm(t_{h,j})_{h∈S, j≤s}. Different pairs (S, bijection S→[s]) give different monomials, so no cancellation can occur, even when |D| > s. For |D| < s there is no degree-s part, so the value is 0. The producer's unique-monomial argument is a special case of this.
- Rank: M_{ij} = L(P_{a_i}P_{b_j}) is triangular with zeros above the diagonal (d ≤ r < s) and a nonzero diagonal, so rank M = m. Row i is the image of P_{a_i} under the linear map A → K^m given by z ↦ (L(zP_{b_j}))_j, so rank M ≤ dim A = 2^s. Hence m ≤ 2^{r+1}. This is an unconditional replacement for the Gao–Zhao preprint in the binary case.
- Isotropic route: B(e_S,e_T) = 1 exactly when T is the complement of S. The Gram matrix is a permutation matrix, so B is nondegenerate (and symmetric). The P_{v_i} are independent by the triangular pairing with the P_{w_j}. B(P_{v_i},P_{v_j}) = 0 because d(v_i,v_j) ≤ r < s. So U ⊆ U^⊥, and dim U + dim U^⊥ = 2^s gives k ≤ 2^r directly. Correct. (A ≅ exterior algebra Λ(K^s) in characteristic 2, so this is the Lovász–Frankl method.)

### §3 θ = 2^r: correct
- Recurrence: Ind(H) is a simplex iff H is edgeless. A vertex is a cone point of Ind(H) iff it is isolated in H. Deletion and link are as in tex eq. (ind-link), l.475–476. So T(H) matches eq. (theta-rec), l.503–509, exactly.
- T ≤ s: a list in an induced subgraph is a list in H. Prepending (p,q) to a list in H−N[p] is valid: v_i ∉ N[p] keeps {p, v_i} independent and distinct, and w_i ∉ N(p) satisfies (iii) with j = index of p. The new witness q comes first, so it carries no constraint. Induction is over the pivot-p bound, as in Lemma theta-basic. Appending would need q to be a nonneighbour of every v_j, and the verifier's mutant shows that can fail. I also derived the exact recurrence s(H) = max_p 1+s(H−N[p]), and it agrees with brute force on all 164 graphs.
- Lower bound: isolate invariance, monotonicity under induced subgraphs (the argument is sound, including the case where p is isolated in J; this is F2 / BC Prop. 2), T(M_m) = m, and the subcube inducing a perfect matching with 2^r edges (Thm VR-matching).
- The alternative route PROOF cites (θ ≤ d', Thm theta-dprime, l.828–841, via BC Cor. 29, plus d' = max close-skew, Lemma dprime-VR) is also valid. The direct argument removes any dependence on it.

No gaps found. In the audited draft, §2 said "its columns are the evaluations"; the precise statement is that the rows are images of the P_{a_i} under a linear map. The packet uses the row-map wording.

## Verification (referee_verify.py, pure integer Python: no math import, no floats, no single-slash division; self-audited)
```
gtimeout 120 python3 -I referee_verify.py   # 6.9 s, exit 0, "SUMMARY: 0 failures"
```
1. Exact symbolic F_2[t_hj] algebra for (r,n) = (1,3), all 64 word pairs, and (2,4), all 256 pairs. Checked: u_h^2 = 0, (1+u_h)^2 = 1, P_xP_y = ∏_D(1+u_h), the threshold identity including |D| > s, and coefficient 1 on t_{h1,1}…t_{hs,s}.
2. GF(2^16), with x^16+x^5+x^3+x^2+1 shown irreducible by a Rabin test. For r = 1..4 and n = r+1, r+2: the reversed-doubled subcube system gives a triangular M with nonzero diagonal, rank 2^{r+1} = dim A. B is nondegenerate, and U is isotropic with dim U = 2^r and dim U^⊥ = 2^r.
3. Exact minimax θ(VR(I_n;r)) = 2^r for (2,1),(3,1),(3,2),(4,1),(4,2),(4,3). Also d' = 2^r on those six cases plus (5,2) and (5,3); The case (5,2) reproduces the published close-skew result. The case (5,3) lies outside the published close-skew cases. Subcube matching tightness (θ = 2^r) for every r ≤ 4 and n ≤ 6.
4. T(H) ≤ s(H), with brute-force s, on all 64 labelled 4-vertex graphs and 100 deterministic sampled 5-vertex graphs. Also checked on these graphs: monotonicity on every induced subgraph and isolate invariance. Separately, T(M_m) = m for m ≤ 6.
5. Controls: the 12 mutation checks listed under CONTROLS, and the positives (subcube system; one-sided example v=[0,1], w=[6,2], n=3, r=1, whose reversed doubling is skew).

The finite checks confirm consequences of the argument. They do not prove it: the proof itself is the line-by-line audit above.

## Sources
- [S. Selvaraja, arXiv:2611.20820v1](https://arxiv.org/abs/2611.20820v1). Source line references above refer to the v1 TeX.
- [Producer's proof](../PROOF.md) (GPT-6.2 Astra).

## Limitations
- No novelty or literature check: the brief forbids network access. Gao–Zhao, Lew, Bıyıkoğlu–Civan and Adamaszek–Adams were not read; I relied only on the paper's statements of them, and the main proof needs none of them.
- Finite computations stop at n ≤ 6 (θ for the full cube only at n ≤ 4).

## Next steps
1. Check novelty online: arXiv listings after 2611.20820v1, later versions of the paper, and the Gao–Zhao preprint.
2. If the result is still new, write it up as a short note, but only with Ricardo's approval; no outreach from this job.

VERDICT: HOLDS

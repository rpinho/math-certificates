# Selvaraja’s Conjectures 5.9 and 3.6

## Main theorem

Let $n>r\ge1$ be integers, and let $d_H$ be Hamming distance on the binary cube $I_n=\{0,1\}^n$. A close-skew system consists of ordered pairs $(v_i,w_i)$ whose vertices $v_i$ are pairwise at distance at most $r$. Each witness $w_i$ is at distance greater than $r$ from $v_i$ and at distance at most $r$ from every earlier vertex $v_j$.

The maximum length of a close-skew system is $2^r$, and $\theta(\mathrm{VR}(I_n;r))=2^r$. These are Conjectures 5.9 and 3.6, respectively. Selvaraja’s subcube lower bound and $\operatorname{coll}\le\theta$ then give $\operatorname{coll}(\mathrm{VR}(I_n;r))=2^r$, Shukla’s collapsibility conjecture. [Proof](PROOF.md) · [Selvaraja’s paper](https://arxiv.org/abs/2611.20820v1)

## Proof outline

1. **Reversed doubling.** Append the swapped pairs in reverse order. Within each half, the original one-sided witness conditions give the required close comparisons. Across the halves, the comparisons are between original vertices, so pairwise closeness supplies them.
2. **Binary skew bound.** Encode cube vertices in the characteristic-two algebra of square-free monomials on $r+1$ generators with square zero. The top coefficient of a product is nonzero exactly when its two vertices are at distance greater than $r$. A skew list therefore gives a triangular matrix with nonzero diagonal whose rank is at most the dimension of the algebra, $2^{r+1}$. The doubled list has twice the original length. Selvaraja’s antipodal subcube construction attains $2^r$.
3. **Theta from deletion, link, and a subcube matching.** In the graph joining vertices at distance greater than $r$, the theta recurrence uses vertex deletion and closed-neighborhood deletion. The maximum close-skew length controls the deletion branch by monotonicity and the link branch by prepending the pivot and a neighbor. The antipodal matching on an $(r+1)$-subcube gives the opposite inequality.

## Verification

The clean-room audit returned **VERDICT: HOLDS**. It checks the order of the doubled sequence, the characteristic-two threshold and rank argument, and the theta recurrence. The finite runs check consequences of the proof using exact arithmetic. The producer verifier also checks a finite rank certificate in dimension ten at scale four. The producer’s bounded searches initially timed out at six targets. A forward search resolved one of them, and the rank certificate covers the other five. [Referee report](referee/REFEREE.md) · [Replay results](REPLAY.json)

A statistical holdout does not apply to this deductive proof. The finite controls include asymmetric witnesses, a broken doubling order, and changes to the algebra and graph arguments that trigger their intended failures.

**Edits after the referee.** `PROOF.md` differs from the text the referee read in two places: Section 2 now says "row $i$ is the image of $P_{a_i}$ under the linear map ..." where the refereed text said "its columns are the evaluations ..." (the referee flagged that loose phrase and judged it harmless), and one closing sentence now points to this README. The refereed text is [certificates/PROOF_as_refereed.md](certificates/PROOF_as_refereed.md). `referee/REFEREE.md` is a lightly edited copy of the referee report (wording, file names, and a mutation count of 12 recounted from the raw replay where the referee wrote 8); the verbatim report is [referee/REFEREE_original.md](referee/REFEREE_original.md).

**Lean status:** None

**AI disclosure:** Proof by GPT-6.2 Astra (Codex). Clean-room audit by Claude Opus 5.5, returning **VERDICT: HOLDS**. No human mathematician has reviewed this packet.

## Prior art

- Selvaraja proved the close-skew result for $r=1,2$ and $n=r+1$, and the theta result for those cases and $n=r+2$. The paper supplies the antipodal constructions, the relation to Lew’s invariant, and the symmetric doubling of induced matching edges. The rank proof uses the exterior-algebra method in characteristic two. [Selvaraja’s paper](https://arxiv.org/abs/2611.20820v1) · [Credits](CREDITS.md)
- The supplied priority check on 2026-11-27 UTC found only v1 in the arXiv API, dated 2026-11-16. Its literature searches found related work and no newer resolution of these statements. The solved-conjectures index and the GitHub issue/PR searches yielded no matching resolution. A GitHub API recheck during packaging found no matching issue or PR for the exact identifier. [arXiv record](https://arxiv.org/abs/2611.20820v1) · [Solved-conjectures index](https://github.com/1337isnot1337/solved-conjectures) · [GitHub issue and PR search](https://github.com/search?q=%222611.20820%22&type=issues)
- The relevant code hits were in rainwangphy/aftd-platform under its Lean TCS knowledge base. They define the close-skew predicate and formalize the published cases $r=1$, $r=2$, and $n=r+1$. The searches found no general proof as of 2026-11-27 UTC. [AFTD Platform](https://github.com/rainwangphy/aftd-platform) · [Lean code search](https://github.com/search?q=repo%3Arainwangphy%2Faftd-platform+2611.20820&type=code)

## Reproduction

Run from this directory with Python 3. The scripts use standard-library modules.

```sh
python3 -B certificates/verify.py controls
python3 -B certificates/verify.py five
python3 -B certificates/verify.py kernel
python3 -I -B referee/referee_verify.py
```

# Recheck of the two Section 4 repairs

Both required changes in REFEREE.md are resolved in v3. The revised passage is ready to send to an outside mathematician on the scope of this recheck. References below are to delta/paper_v3.tex; both repairs also appear on page 6 of delta/paper_v3.pdf.

**1. Ambient dimension before the minimum-distance assertion — RESOLVED.** Step 7 now begins (lines 403–406):

> “Regard $A_i$ as a function on $n$ bit coordinates, adjoining unused coordinates if necessary so that $n\ge k+2$. This leaves $p_i$, $\lambda$ and the degree bounds unchanged, because each value is repeated equally often.”

This puts the convention before the first assertion that RM(k,n) has minimum distance $2^{n-k}$. In particular, $k\le n$ now holds even when $d$ is a loose degree bound and the original cube has fewer than $k$ coordinates. If the derivative originally lives on $m$ coordinates, adjoining $n-m$ unused coordinates multiplies its support size and the size of the cube by the same factor $2^{n-m}$. Thus $p_i$ and $\lambda=2^kp_i$ stay fixed. The polynomial remains independent of the new coordinates, so its real degree and its degree after coefficient reduction modulo two are unchanged. Nonzeroness is preserved. Consequently the padded support word has weight $w=2^np_i$ and normalized weight $w/2^{n-k}=\lambda$, as claimed. Here $n$ is an ambient dimension, not a count of relevant variables.

The later sentence (line 434) now reads:

> “As in Step 7, we have $n\ge k+2$ (append unused coordinates if necessary);”

This is a consistent reference back to the already established convention. It introduces no extra assumption on the original function. The following lower-degree observation remains valid: a nonzero binary polynomial of degree $r<k$ has weight at least $2^{n-r}\ge2^{n-k+1}$, excluding normalized weight strictly below two. The standard minimum-distance statement and the order-at-least-two low-weight premise agree with [Carlet (2024), Sections 1–2, especially p. 10613](https://www.aimspress.com/aimspress-data/math/2024/5/PDF/math-09-05-518.pdf), reconsulted for this recheck.

**2. The $k=1$ case before combining (6) and (7) — RESOLVED.** The combination paragraph now starts (line 444):

> “When $k=1$, $M=2$, so (6) and relevance give $\lambda\in\mathbb Z_{>0}$; therefore $\lambda<2$ forces $\lambda=1$, again giving (8) below. For $k\ge2$, combine (6),(7).”

This argument is correct: (6) becomes $\lambda\in\mathbb Z$, relevance gives $p_i>0$ and hence $\lambda>0$, and the only positive integer below two is one. At $k=1$, list (8) has only $j=0$, giving exactly $\{1\}$. No application of (7) is made in this boundary case. For $k\ge2$, the existing intersection calculation remains correct: $M\lambda=2^{k+1}-2^{k-j}$ is even for $0\le j\le k-1$, odd at $j=k$, and nonintegral for $j>k$. The list remains a necessary list, without asserting that all entries are realized by derivatives. No new issue is introduced.

**Complete diff and PDF.** A fresh `diff inputs/paper_v2.tex delta/paper_v3.tex` matches delta/v2_to_v3.diff byte for byte. It contains exactly four hunks: the Step 7 repair, the matching later reference, the boundary-case repair/restricted invocation of (7), and the editorial note at lines 326–327 explaining the added arithmetic and $d=2$ case. The editorial note accurately describes the revision relative to the first version; the arithmetic itself was already present in v2. There are no other substantive changes. In particular, equations (6)–(8), the external theorem statement, the rest of the argument, and existing correction notices are unchanged. Extracted text from the supplied PDF confirms the revised editorial note on page 5 and both repairs and the cross-reference on page 6.

This acceptance concerns the two fixes and their effect on the rewritten opening; it does not certify the paper's numerical artifacts or settle its previously marked attribution caveats. No further change is required for these two referee objections. New result: no; this is a recheck of the supplied proof revision.

VERDICT: ACCEPT

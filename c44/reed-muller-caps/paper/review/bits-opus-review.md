# Review of paper_v3.tex (bit-convention revision)

Reviewer: Claude Opus 5.5, 2026-11-09. Inputs read: paper_v2.tex, paper_v3.tex,
v2_to_v3.diff, PROOF.md, CORRECTIONS.md, plus the text layer of paper_v3.pdf
(it matches the tex, and Section 4 renders cleanly). Nothing else was opened.

## 0. Global consistency check

Identify a sign coordinate with a bit by x = 1 - 2b, and a sign-valued Boolean
F with a bit-valued one by F = 1 - 2f. Under this map (which is the one v3's
Walsh characters chi_S = prod(1 - 2x_j) use):

- v2's A_i = (F(i=+1) - F(i=-1))/2 = f(b_i=1) - f(b_i=0), which is v3's A_i.
  It is the same function, so p_i, lambda, H, h_i and every quantity fed to
  the certificate are numerically identical. caps.json and both checkers
  need no rerun.
- v2's Delta_j equals minus v3's Delta_j. It only enters squared, so nothing
  changes.
- Walsh normalization: for S nonempty, f_hat_bit(S) = -F_hat(S)/2, and
  Var(f) = Var(F)/4. v3's factor 4 in I(f) = 4 sum |S| f_hat(S)^2 and the bound
  4 deg(f) Var(f) <= deg(f) are exactly v2's sum |S| F_hat(S)^2 <= deg(F).
- v2's lower family maps to v3's: sign selector +1 corresponds to bit 0, and
  the four selector cases match term by term (checked below).

So conclusions (1)-(13) carry over unchanged. Section 5, Section 7 and the
certificates use only (4), (5), (6), (8) and R_d >= 3M - 2, and v3 still
supplies all of them.

## 1. Mathematics, hunk by hunk

| # | Diff hunk | Content | Verdict |
|---|---|---|---|
| 1 | @@-27 | date line | Holds. |
| 2 | @@-52 | front-matter provenance | Accurate as far as it goes, but the unchanged sentence just before it is now stale. See R1. |
| 3 | @@-72 (P004) | {0,1} cube, monomial expansion, degree, relevance, local degree | Holds. Uniqueness of the monomial expansion is standard, and Section 4 proves the Moebius inversion anyway. Relevance via a nonzero c_S with S containing i is correct in this basis. |
| 4 | @@-94 (P006) | support lemma, branches B+A and B | Holds. With P = x_j A + B, the branches are B (x_j=0) and B+A (x_j=1), and both cannot vanish where A != 0. The averaging gives 2^-k. |
| 4 | @@-94 (P007-P009) | A_i = f(x^{i<-1}) - f(x^{i<-0}); values; p_i = Pr(A_i != 0) = E A_i^2 = Inf_i | Holds. The degree is d_i - 1, so the support lemma gives p_i >= 2^{1-d_i}. |
| 4 | @@-94 (P009) | Walsh characters, degree equality, bit difference of chi_S | Holds. chi_S(x^{i<-1}) - chi_S(x^{i<-0}) = (-1 - 1) chi_{S\i} = -2 chi_{S\i}, which is correct. Degree equality under y = 1-2x is correct. Local degree: in either basis it equals 1 + deg(A_i), because A_i = sum_{S containing i} c_S x^{S\i} = -2 sum f_hat(S) chi_{S\i}. Small gap: orthonormality also needs (1-2x_j)^2 = 1 (so that chi_S chi_T = chi_{S xor T}), and the text cites only independence and mean zero. See O3. |
| 4 | @@-94 (P010-P011) | I(f) = 4 sum \|S\| f_hat^2 <= 4 deg Var <= deg; Var = Ef(1-Ef) <= 1/4 | Holds. Factor 4 is right (see Section 0). The middle inequality uses the fact that S = empty carries weight 0 and Var = sum over nonempty S of f_hat^2. The downstream facts D <= d/2, influence >= 2^{1-d} and R_d <= d 2^{d-1} follow as before. |
| 5 | @@-127 (P012-P013) | h = z f(x_L,Y) + (1-z) f(x_{L'},Y) | Holds. h = f(x_{L'},Y) + z(f(x_L,Y) - f(x_{L'},Y)). The degree-d terms involve only Y, so they cancel in the z coefficient, and deg h <= d. |
| 6 | @@-140 (P014) | "largest multilinear term" | Holds. For l in L, the terms z c_S x^S are new and nothing cancels them. For the copy l', -z c_S x'^S has size \|S\|+1 and is also unique. Y coordinates keep local degree d through the f(x_{L'},Y) term. |
| 7 | @@-150 (P015) | dropped "In bit coordinates" | Holds. The AND substitution is now native. |
| 8 | @@-180 (P019) | Delta_j A as a half bit difference | Holds. Values lie in {0, +-1/2, +-1}, and the degree is <= k-1 in the monomial basis. |
| 9 | @@-196 (P022) | Delta_j chi_S = -chi_{S\j} | Holds. sum_j E(Delta_j A)^2 = sum \|S\| A_hat(S)^2 <= k p uses Walsh degree <= k, which P009 supplies. Equations (1) and (2) are unchanged and need k >= 1. |
| 10 | @@-249 (P032) | factor x_j or 1-x_j | Holds. A_i = x_j A_i\|_{x_j=1} + (1-x_j) A_i\|_{x_j=0}. If one branch derivative vanishes, the factor raises the degree by exactly one, so half the surviving branch weight equals the original weight. Correction 1 is unaffected and still applies to the unchanged sentence. |
| 11 | @@-267 (P033) | B = f(x^{i<-0}); A_i(alpha) = 1 forces B = 0, and -1 forces B = 1; f_alpha is x_i or 1-x_i | Holds. This is the one place where the convention changes the argument: B is constant rather than zero, and v3 handles it correctly. The active fraction is p_i because A_i depends only on x_H. |
| 11 | @@-267 (P034) | degree-d monomials meet H | Holds, and is slightly better than v2. v3 restricts to degree-d monomials disjoint from H, whose coefficient after restricting H is exactly c_T, and uses "nonconstant in Y" against "B constant in Y". v2's "a monomial in B" (any degree) was looser. The "d >= 2" in the first sentence is needed only for the second half (the monomial through i), so it is harmless. deg f_alpha <= d-1 follows. |
| 12 | @@-317 (Section 4 setup) | f bit-valued, d >= 2, k = d-1 >= 1, M = 2^{d-1}, lambda = M p_i | Holds. |
| 12 | @@-317 (Integer coefficients) | Moebius inversion, c_T in Z; A_i = sum_{T containing i} c_T x^{T\i} = sum a_T x^T with a_T in Z and a_T = 0 for \|T\| > k | Holds. The inversion check, inner sum (1-1)^{\|T\\V\|}, is correct. "Real degree <= d" is defined in Section 1 in this same basis, so c_T = 0 for \|T\| > d needs no conversion step. That is the saving over v2's Steps 2-4. |
| 12 | @@-317 (Energy grid, eq. (6)) | p_i = sum a_T^2 2^{-\|T\|} + 2 sum_{T<U} a_T a_U 2^{-\|T u U\|}; each term in 2^{1-2k} Z | Holds. Diagonal: 2k-1-\|T\| >= k-1 >= 0, which uses \|T\| <= k and k >= 1. Off-diagonal: the factor 2 absorbs the 1 in 2^{1-2k}, and \|T u U\| <= 2k. So p_i is in 2^{1-2k} Z and lambda = 2^k p_i is in 2^{1-k} Z = (2/M) Z. This is the same grid as v2's (sum z_S^2 even over M), proved more directly. The product rule x^T x^U = x^{T u U} silently uses x_j^2 = x_j (O4). |
| 13 | @@-407 (Support word) | reduce a_T mod 2, giving an RM(k,n) word; n >= k+2 padding; minimum distance 2^{n-k}; normalized weight lambda | Holds. Reduction commutes with evaluation because evaluation at a 0/1 point is an integer sum of coefficients. +-1 reduces to 1, so the word is the support indicator. It is nonzero because i is relevant. Padding repeats each value 2^{n'-n} times, so p_i and lambda are unchanged. The F2 support induction for the minimum distance is correct, and x_1...x_k attains it (n >= k holds). w/2^{n-k} = 2^k p_i = lambda. |
| 14 | @@-442 (P052) | "As in Step 7" becomes "As above" | Holds. The referent (padding to n >= k+2) is in the Support word paragraph. No other "Step" references remain (grep). |
| 15 | @@-580 (Section 6) | Xi_d = s + (1-s-t) Xi(x) + (t-s) Xi(y) | Holds. The cases (0,0), (0,1), (1,0), (1,1) give Xi(x), Xi(y), 1-Xi(y), 1-Xi(x), so it is Boolean. The degree is <= d. The term -s m (m of degree d-1 in Xi(x)) is the only s-times-x-monomial term, so the degree is exactly d (only deg <= d is used). Input copies are relevant through (0,0) and (0,1). Selectors: with Xi(x) = Xi(y) = 0 the output is s, and with Xi(x) = 0, Xi(y) = 1 the output is t. Both cases are realizable because Xi_{d-1} is nonconstant on disjoint variables. L_d = 2L_{d-1} + 2 and L_d = 3M - 2 are unchanged. v2's extra claim that all Fourier masks have size d is dropped. It is never used later (P074 and P093 need only the count and deg <= d). |
| 16 | @@-731 (P093) | "signed" becomes "ternary" | Holds, and is clearer. |
| 17 | @@-830 (Credit) | thanks to Valyuzhenich | Fine. |

Later sections: Section 5 uses (4), (5), (6), (8), (9); Section 6 uses (4), (5)
and the family; Section 7 uses (4), (5), (6), (8) and R_d >= 3M - 2. All are
present with unchanged statements. The hypotheses d >= 2 (k >= 1) for (2) and
(6), k >= 2 for (7), and M = 2^{d-1} are stated where they are used.

No mathematical errors found. The only gaps are two unstated one-line facts,
(1-2x_j)^2 = 1 and x_j^2 = x_j (O3, O4).

## 2. Reader-facing quality (for a Boolean-functions combinatorialist)

Section 4 now reads as a clear, complete, short argument: integer coefficients,
then the energy grid, then the support word, then Kasami-Tokura. The tex word
count drops from about 910 to about 510. The core is exactly his suggestion:
A_i has integer monomial coefficients of degree <= k, so E A_i^2 lands on a
2^{1-2k} grid, and A_i mod 2 is an RM(k,n) word.

Places that are still more elaborate than his suggestion needs:

- Moebius-inversion verification ("Indeed, substituting ..."). He knows this.
  One clause ("by Moebius inversion") suffices.
- Minimum distance of RM(k,n) ("For completeness ... attains it", 3 sentences).
  This is textbook for him, since he works on minimum supports of RM-type
  functions. Stating "RM(k,n) has minimum distance 2^{n-k}" is enough.
- "We reduce A_i itself, rather than A_i^2 ..." is a defensive leftover from
  the v2 history. In bits A_i^2 = |A_i| has the same support, so the remark
  now raises a question it doesn't need to.
- "Here and below the masks in the final sum omit i; the bound follows because
  c_T = 0 for |T| > d." is awkward. Defining a_T outright is clearer:
  a_T = c_{T u {i}} for T not containing i, otherwise 0.
- "where < is any fixed ordering of the masks, so each distinct pair is
  counted once" could just be "sum over unordered pairs T != U".
- His name appears three times (front matter, Section 4 editorial, Credit).
  Two would be enough.

Notation: x^S is defined as a monomial in P004, and two lines later x^{i<-a}
means "x with coordinate i set to a". The superscript is overloaded, and
Section 4 uses x^T heavily. His own phrasing, f(x_i=1) - f(x_i=0), avoids
this.

Leftover sign-convention phrases: none remain in the mathematics. A grep for
sign, signed, +-, Fourier and "Step" finds only:
- P028 "a direct real Fourier calculation" and P094 "Fourier energy". Both are
  acceptable as Walsh-Fourier, but "Walsh" would match Section 1.
- P089 "Fourier-lattice duals" is the name of an inherited certificate, so it
  should stay.
- The front matter (R1 below).

Section 1's new Walsh paragraph is dense but needed, since Sections 1 and 2 are
energy arguments. That fits his remark that Sections 2-3 stay largely
unchanged.

## Required changes

R1. Front matter, lines 53-55. This sentence is now false and contradicts the
next one: "The seven numbered sections below transcribe the frozen PROOF.md.
The exception is Section 4, which was expanded step by step and reworded for
clarity on 6 November 2026." In v3 the sections no longer transcribe PROOF.md,
which uses the +-1 convention, and Section 4 is no longer the step-by-step
expansion. This is the first page he reads. Suggested replacement:

"The seven numbered sections below follow the frozen PROOF.md, which uses the
+-1 convention. On 9 November 2026 the write-up was converted to the {0,1}
convention, and Section 4 was rewritten and shortened following Alexandr
Valyuzhenich's suggestion, with all conclusions unchanged."

Optionally add one sentence noting that the SOURCE line ranges and the
PROOF.md hash refer to the sign-convention original.

## Optional suggestions

O1. Replace x^{i<-a} with f(x_i=a) or f|_{x_i=a}, in P008-P009, P019 and P033.
    This avoids the clash with the monomial x^S. Recommended.
O2. Cut the Moebius-inversion verification, the minimum-distance proof and the
    "reduce A_i itself, rather than A_i^2" remark from Section 4. Define a_T
    explicitly and sum over unordered pairs.
O3. P009: add "and (1-2x_j)^2 = 1" to the orthogonality justification.
    Possibly move the "same holds for local degree" sentence after the
    bit-difference formula that justifies it.
O4. Energy grid: say "since x_j^2 = x_j" for x^T x^U = x^{T u U}.
O5. P028: "Walsh-Fourier calculation" instead of "real Fourier calculation",
    to match Section 1.
O6. Mention his name twice rather than three times.

VERDICT: FLAG
(The mathematics is accepted with no errors. The flag is only for R1, the
stale page-1 provenance sentence. After that one-sentence edit, no further
mathematical review is needed.)

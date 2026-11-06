# Independent referee: C44 paper, Section 4 (Steps 1-7), commit 87cadf7

Read: `paper/c44_reed_muller_caps.tex` (full) and Section 4 text extracted from the PDF.
PDF sha256 bb01283a... matches SHA256SUMS; extracted text matches the .tex.
Written before reading `paper/review/`; comparison at the end.

## Verdict: SEND AFTER SMALL FIXES

The mathematics in Steps 1-7 and the combination paragraph is correct. The main risk is not
Steps 1-7. It is the frame around them. Nothing says why Section 4 exists, and the section ends
with the old internal-notes paragraph (P055) followed by three boxes in a row. That is the part
most likely to get "not very well written" again.

## 1. Correctness, step by step

- **Setup.** f has real degree <= d, d >= 2, i relevant, M = 2^{d-1}, lambda = M p_i. This matches
  Section 3, where f is a count extremizer with all local degrees d. Section 4 needs only "at most d".
  Holds.
- **Step 1.** Moebius inversion is correct. The inner sum is (1-1)^{|T\V|}. Integer values give
  integer bit coefficients. Holds. (The triangular system also proves existence. The text asserts
  existence and uniqueness first, which is fine.)
- **Step 2.** The substitutions do not raise degree in either direction, and expansions are
  unique, so the two degrees are equal. Holds.
- **Step 3.** The coefficient of x^S in b^T is (-1)^{|S|} 2^{-|T|}. With f = 1 - 2g, the formula
  for f-hat(S) and the factor 2^{1-|T|} are right, and |T| <= d puts every term on (1/M)Z.
  Holds.
- **Step 4.** A_i-hat(S') = f-hat(S' + i). Holds.
- **Step 5.** Parseval in the uniform normalization of Section 1. Holds.
- **Step 6.** Sum z_S = M A_i(1,...,1), and M is even because d >= 2. Since z^2 = z mod 2, the
  sum of the z_S^2 is even, so lambda is in (2/M)Z. Holds. (In fact sum z_S = 0 mod M, but that
  is not needed.)
- **Step 7.** Padding to n >= k+2 is now done before the minimum distance 2^{n-k} is used. Reducing
  integer coefficients mod 2 commutes with evaluation at 0/1 points. The weight is 2^n p_i and the
  normalized weight is lambda. Holds.
- **(7) and the following paragraph.** The Kasami-Tokura form 2^{n-k+1} - 2^{n-k+1-mu},
  normalized, is 2 - 2^{-j}. Algebraic degree below k gives weight >= 2^{n-k+1}, which holds by
  RM minimum distance. Holds.
- **(6) with (7).** M lambda = 2^{k+1} - 2^{k-j} is even only for j <= k-1. The k = 1 case is
  correct. Holds.
- **Links to Section 5.** Section 5 needs only lambda >= 1, the grid (6) for lambda >= 2, and a
  list of values below 2 that contains every possible one, which (8) is. The formula
  lambda_h = (2/M) ceil(hM/4k) gives the first grid point of each cell, and it is correct.

**No gaps.** Two wording points matter for correctness:

- **C1.** "Hence the safe finite list below 2 is exactly" overstates the result. (8) is a
  necessary list. Nothing shows that every value in it is attained. Replace it with: "Hence every
  possible value of lambda below 2 lies in the finite set".
- **C2.** "Its real degree is d_i-1 <= k (Section 1)". Section 1 asserts this without proof, but
  Step 4 proves it. Replace with: "By Step 4, A_i-hat(S') is nonzero only when f-hat(S' + i) is,
  so the real degree of A_i is d_i - 1 <= k."

## 2. Readability for Valyuzhenich (top fixes, in priority order)

**R1. Missing motivation at the top of Section 4.** Add this sentence right after the editorial box:

> "Section 3 bounds N in terms of the real parameter lambda >= 1 of one chosen derivative. This
> section shows that lambda can take only special values. Equation (6) puts lambda on the grid
> (2/M)Z. The Reed-Muller weight theorem then limits the values below 2 to the finite list (8).
> Section 5 checks only these values."

**R2. P050: the theorem has a jargon name.** Current text: "The external below-twice-minimum
Reed-Muller theorem states:". Replace with:

> "We use the Kasami-Tokura theorem on Reed-Muller codewords of weight less than twice the minimum
> distance [refs]. For k >= 2, any nonzero word of RM(k,n) with weight strictly below 2*2^{n-k}
> has normalized weight". Also add, after (7): "Since w < 2*2^{n-k} is the same as lambda < 2,
> (7) applies exactly when lambda < 2."

**R3. P052 is compressed.** Current text: "Only necessity is used, so all parameter-dependent
restrictions on j may be dropped." Replace with:

> "The theorem also says which j occur for given n and k. We use only the fact that lambda has the
> form (7), so we allow every j >= 0."

Also replace "a weight below twice this minimum is already impossible by the support bound" with:

> "a word of algebraic degree at most k-1 lies in RM(k-1,n), whose minimum distance is
> 2^{n-k+1} = 2*2^{n-k}, so its weight is never below twice the minimum."

As written, "support bound" points the reader to Section 1's real-variable lemma, which is the
wrong lemma here.

**R4. Ordering and "again".** "When k=1, ... again giving (8) below. For k>=2, combine (6),(7)."
Put the k >= 2 case first. Then write: "When k = 1 (d = 2), (6) says lambda is a positive integer,
so lambda < 2 forces lambda = 1, which is (8) with k = 1. (The certificate in Section 5 starts at
d = 4, so this case is recorded only for completeness.)" Right now "again" refers to nothing
earlier.

**R5. P055 reads as internal notes.** It uses all caps, "silently", "false uniform gap", "KTA
table for 2..2.5" and a repo file name. Correction 2 and an editorial box then undercut it right
away. Rewrite it as:

> "For lambda >= 2 we use only the grid (6). No further information about Reed-Muller weights in
> [2, 2.5) (Kasami-Tokura-Azumi) is used."

Then collapse the correction box and the editorial box into one footnote. Correction 2 is printed
twice, at the ends of Sections 4 and 5. Keeping it once is enough.

**R6 (minor).** Step 7's last sentence, "We reduce A_i itself, not A_i^2, whose real degree could be
2k.", needs its reason. Replace with:

> "We reduce A_i itself. Reducing the 0/1 indicator A_i^2 directly would only place it in
> RM(2k,n), because A_i^2 can have real degree 2k."

**R7 (minor).** The letter n means the ambient dimension in Section 4 but the excluded count in
Section 5, and j means a coordinate in Sections 2-3 but an exponent in (7). These clashes are
harmless, but the reader may notice them.

No uses of "clearly" or "it follows". Notation is defined before use within Section 4: lambda,
p_i and d_i are recalled in the setup, and RM(k,n) is standard for this reader.

## 3. Comparison with Astra's referee and recheck (read afterwards)

I agree with both fixes: n >= k+2 imposed before the RM minimum distance is used, and the k = 1
case kept separate from (7). Both are correct and both are already in 87cadf7. I found nothing
that contradicts Astra. Astra calls "safe finite list" acceptable, with "Only necessity is used"
as the disambiguation. I would still change "exactly" (C1), because a reader stopping at (8)
sees "exactly". Astra also flags that "support bound" should not be read as Section 1's lemma. I
agree, and I propose explicit wording for it (R3). Astra did not assess readability. R1, R2 and
R5 are new.

# Claude Science reviews (Claude Opus 5.5)

## 1. Argument referee (round 6)

I found no false or unjustified step in the argument for the C91 ≥ 0.265988 candidate (problem 91a); it is still unrefereed. I checked 14 lemmas and all passed. I did not replay the certificate, which needs about 28 GB and belongs to the other reviewer.

**What carries over from round 5.** The retained round-5 proof is byte-identical to the one I refereed yesterday, and so is the competitor-tracking code that implements the gap-debt record. The only code change in that part is four added emitters for the new statistics. [MEASURED: shasum, cmp, diff]

**The three points you flagged:**
- **Gap-debt record (W=3, B=2, S=0, T=2):** PASS, by inheritance. I re-ran my round-5 test harness on the round-6 certificate:
  - none of the 16,129 canonical string pairs up to length 6 is rejected;
  - every rejection among all 37,449 words of length ≤ 5 happens at a noncanonical prefix;
  - all 59,550 forbidden words are noncanonical under my own DP, and the list is closed under bit complement;
  - it contains exactly 4,000 words of length 13–16 (the new ones).
- **Bit-complement quotient:** PASS. The tracking updates use only bit equalities and the eight statistics have even support, so complementing is a symmetry. The verifier checks the complement map on the minimized word matcher and on the run memory. The lifted potential makes every original row identical to a checked representative row. The state count checks out: 2 × 121,332,798 − 1 = 242,665,595.
- **First moment for all input lengths:** PASS. For every n, P(ed ≤ an) ≤ G·e^(−εn + c·n^(3/4)) + 16/√n, with G a fixed constant, ε = 8.94e-7 and c = 0.0768. This tends to 0, so liminf E[ed]/n ≥ a. It only becomes a nontrivial bound for n above about 5.4e19, which is fine for a limit statement.

**The new eight-statistic typicality bound:** PASS.
- **Variance:** each statistic sums ±1 terms whose pairwise covariances are 0, so Var ≤ 2n. Chebyshev with a union bound over the eight gives an exceptional probability of at most 16/√n for every n ≥ 1. That is vacuous below n = 256 and vanishes as n grows, with no entropy-rate cost.
- **Exact check at n = 12** (all strings enumerated): means are 0, each variance equals n minus the pattern's maximal offset, and cross-covariances are 0.
- **Alternative tail bound:** flipping one bit changes a statistic by at most 2|P|, so the bounded-differences bound in PROOF.md is also correct.
- **Emission:** in 20,000 random pairs and alignments, the totals emitted along each alignment always equal the sums computed directly from the strings, including through the quotient lift.

**Exact arithmetic and rounding.** On 3,000 random edges, the verifier's integer coefficients match the exact rational edge weights, with each statistic paired to its own weight. The threshold is a* = −2 log x / log t = 0.2659889995225821. So 0.265988 is rounded down (safe), and 0.265989 would fail. My own rational series check confirms the exponent is positive (lower endpoint 8.94e-7).

1. **First false or unjustified step:** none found.
2. **Step I trust least:** the inherited proof that every stored competitor entry is backed by a genuine path. I did not re-derive it this round; it rests on yesterday's pass, the identical code and the harness rerun. Two text items remain: the per-step update order is still not fixed in the text (soundness does not depend on it), and the "all input lengths" claim should be written as the explicit per-n inequality above.
3. **Worth filing:** yes, as a #306 update (0.263561 → 0.265988, +0.002427; +0.001725 over round 5), but only after four things:
   - the other reviewer's full replay passes, on a host with at least 40 GB, not the Mini;
   - a same-day live check of Tao's table page, the open pull requests (#273, #306) and arXiv. The packet's own check was at 23:16 UTC on 2026-11-03; I could not check live today;
   - "separately written (same agent)" wording for the verifier;
   - the AI-use disclosure, with the asterisk kept.

The reviewer pass was weaker than the rules intend. Delegation is off in this session, so it was a single call to a smaller model, which concurred. Its one checkable point was the statistic-to-weight pairing, which I then tested.

**VERDICT / PROBABILITIES / IDEAS / OUT_OF_BOUNDS**
- **VERDICT:** argument sound, no false step; filing waits on the replay, the live recheck and the disclosure.
- **PROBABILITIES:**
  - argument correct 0.93: the new parts were fully checked; the competitor tracking is inherited;
  - full replay passes 0.9: the receipts look complete and the inherited verifier code is identical;
  - no stronger public C91 claim exists at filing 0.8: not checked live today.
- **IDEAS:**
  1. Write the per-n inequality into PROOF.md; the bar is explicit constants G, c and ε.
  2. Run an ablation outside this project (floating-point estimate only) separating the 4,000 new words from the four new statistics; the bar is a reported gain for each.
  3. Fix the per-step update order in the text; the bar is that my harness reproduces the same tracking state.
- **OUT_OF_BOUNDS:** the 28 GB replay on the Mini; a live scoreboard fetch (no network); retuning x, t and z for extra digits (a precision-only gain).

Files are in the output tray:
- CS-2026-11-04-c91r6-referee.md — the lemma-by-lemma table
- c91r6_referee_tests.py — the typicality, emission and exponent tests

VERDICT: ACCEPT

## 2. Final-bytes check of the PR #306 update

Every sentence in the body and the diff checks out, including the L0 whole / L1 finite line, except one. The body says the Claude Science review accepted, but the reviews folder it links to still says that review is pending. So this is a FLAG.

**The change set is what you described.**
- Both files match the hashes you gave.
- Applying the COMMIT_SHA → 8de8c2d5… substitution to the prefill files reproduces both finals byte for byte. There were 3 placeholders in the body and 2 in the diff, and none are left.
- From v1 to the final body, the only other changes are the verifier wording and the review sentence.
- The patch applies cleanly to branch c91-1101 at 76cb132a, according to the release's recorded check.

**The rest is true and not overstated.**
- **Numbers:** the counts (121,332,798 rows, 499,034,690 edges, 32,774,059 classes, 242,665,595 lifted states) match the receipts. So do the bank details (59,550 words of length 8–16, cap 21, 4,000 new), the previous claim 0.263561, and "about 0.275" (91a.md gives 0.27496).
- **Finite component L1** holds under the definitions:
  - The checker was written by gpt-6-astra; the producer is gpt-6.1-sol.
  - In the published tree, the checker's output file hashes to 9f301257…. That equals the output hash recorded in its receipt and the l1chk_e original.
  - The certificate and checker-source hashes match the receipt.
  - The output covers all rows (AGREES, minimum slack 4,736,028,943,110), checks every forbidden word by DP, and gives a positive exact exponent enclosure of about 8.941e-7.
  - None of the producer's code identifiers appear in the checker.
  - All 69 SHA256SUMS entries pass.
- **Whole bound L0** is correct, because the universal steps are proved only in prose.
- The phrase "separately written by the same AI agent", the AI-use paragraph and the asterisk are all present.

**The problem.** The body says "Proof, certificate, verifiers and reviews: <tree at 8de8c2d5>" and that both AI reviews accepted. In the staged tree, `c91/round6/reviews/README.md` (sha256 ad3fb2a0…, listed in MANIFEST and SHA256SUMS) says "CS review: pending; placeholder only, no acceptance claimed". The tree has no CS review file. I could not open commit 8de8c2d5 (no network), but if it matches the staged tree, the evidence a reader clicks through to contradicts the body.

**Fix:**
1. Add `reviews/cs.md` with both reports, without their internal links. One is the argument referee (ACCEPT, scope limited to the argument); the other is this final-bytes check.
2. Change the README line to "CS review: ACCEPT within argument scope; see cs.md".
3. Regenerate MANIFEST and SHA256SUMS, commit, substitute the new SHA in all 5 places, and rehash.

If 8de8c2d5 already contains an updated reviews folder, send me the output of `git show 8de8c2d5:c91/round6/reviews/README.md` and this becomes ACCEPT.

**Smaller points (not blocking):**
- Paragraph 3 of the body lists the prose-only steps without "complement-lifting", which the level line includes. The two lists should match.
- The footer includes the Claude Code session URL, as in the accepted C47 and C57c bodies. Keeping it is your choice.
- The verification sidecar's receipt hash points to the body-level relocated receipt rather than the copy in the tree. That is consistent with the release's provenance note, so it is fine.

Files are in the output tray:
- CS-2026-11-04-c91r6-release-final-bytes.md

VERDICT: FLAG

Note added by the coordinating session: the final-bytes check flagged that this folder's reviews/README.md still said the CS review was pending. This file and the README update are the fix.

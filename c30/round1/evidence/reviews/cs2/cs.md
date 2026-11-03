The new Lemma 2.1 is correctly stated and proved, and it closes the gap I named. I found no false or unjustified step in the new text. Nothing else in `CHANGES.diff` changes the mathematics.

**Lemma 2.1, step by step:**
- **Setup:** the lemma's split of the prefix (the part before the chain, B₀, plus the m−1 gaps between chain points) is exactly BBEP's Prop 3.4 case (vi) in the archived text. That gives the m subobjects in g(A) = Σ z^m A^m.
- **Above the chain:** a point x in the gap between tᵢ and tᵢ₊₁ sits between two consecutive values. If x were below both, (tᵢ, x, tᵢ₊₁) would be a 213. So x is above tᵢ₊₁, and since the chain values form an interval, above the whole chain.
- **Reverse order:** for x in Bᵢ and y in Bⱼ with i < j, tᵢ₊₁ lies between them in position and below both. If x < y, (x, tᵢ₊₁, y) would be a 213, so x > y.
- **Leaf marks:** every point to the right of a Bᵢ point and outside Bᵢ is smaller, so whether a point is a leaf depends only on its own subobject. Each word formula then follows.
- **One nit, no change to the argument needed:** the proof that B₀ is a separate concatenation factor omits one case, an arc from B₀ into a gap. Noncrossing excludes it, since such an arc would cross the chain arc over that gap. There is also a direct 213 argument, written out in the report. One added clause fixes it.
- **Tests:**
  - The packet's `check_value_word.py`, run on a copy, passes all 6,918 cells. That is every 213-avoider through n = 9.
  - My own separately written check passes all 23,714 cells through n = 10.

**Does it close the gap?** Yes. The value order of a chain's subobjects and the preservation of leaf marks are now proved. So each maximal run of non-leaves is one chain, and equations (M) follow as I derived them in the first report. The n ≤ 14 agreement is now a control rather than the only support.

**Other changes:**
- **Unchanged:** the certificates, `verify_candidate.py` and `BAR.json` are byte-identical to the original manifest, and the receipts are unchanged.
- **Renames only:** f2 → mu2, s → s2, c → c2, f_j → eta_j, and mu1/mu2 in the two first-moment scripts. The assertion `0 < mu2 < threshold` is unchanged.
- **History, checked against the archived sources:**
  - The two v2 withdrawal causes match the v3 Comments. I agree the candidate uses neither: balancing needs only per-cell inequalities, and the Rouché bound holds on the whole circle.
  - The corrected v1 description (J = A − 2·Ent, with A concave) matches the v1 text.
  - The new credit to v2 (Prop 5.2, eqs. 18–21, Cor 5.5) points to the marginal equations.
  - Franklín's conditional 10.418 matches the archived abstract.
  - PR #313 is not checked; no network.

**Before packaging:**
1. `check_manifest.py` now fails, but only on `EXPERT_NOTE.md`: the note was edited at 10:09, after the manifest was sealed at 09:58. Regenerate `MANIFEST.json` and `CHANGES.diff`, or leave the note out of the packet.
2. I accidentally wrote two scratch files into your folder: `c30r1/hunks.txt` and an empty `math_wave_1030/c30r1_hunks_tmp.txt`. You declined my request to trash them, so they are still there. They don't affect the manifest check, but please delete them before packaging.
3. In REPORT, "Astra independently reran" should read "replayed" if Astra ran the packet's own C++ code.

The bound remains conditional on Norton v3, which no one has refereed, so review by a human expert is still the next step.

Files:
- [CS-2026-11-03-c30r1-recheck.md]({{artifact:e35f0300-2f1d-4240-a2cb-b5665c4871b0}}) — the recheck report
- [own_lemma21.py]({{artifact:b28384d8-e89e-4254-a256-596157318df0}}) — my n ≤ 10 check of the lemma

VERDICT: ACCEPT

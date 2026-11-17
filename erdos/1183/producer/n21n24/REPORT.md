Shipped: candidate, unrefereed f(21)=12, f(22)=13 conditional on BMB lem:window20, and f(24)=14; 13≤f(23)≤14. The exact rank-colouring minima are 12,13,14,14.

**Counts:** 4 dimensions tried and completed; 3 candidate values settled, including 1 conditional on an external computational lemma; 4 upper bounds proved by checked trees; 4 rank minima proved with complete rejection coverage. The unrestricted n=23 gap is one.

Here f(n) is the minimum, over all two-colourings of the Boolean cube, of the largest monochromatic family closed under both union and intersection. T′(n) restricts that minimum to size-only colourings. A word's kth letter colours every k-element set, with the first letter corresponding to rank zero. These are candidate mathematical claims, unrefereed. Our separately written checks belong to the same lane; they are same-lane checks. The preceding round's “refereed” results underwent an internal clean-room review, which reported HOLDS WITH CAVEATS.

## Results by dimension

| n | Lower bound and source | T′ | Exact maxima of displayed word, colours 0/1 | Unrestricted claim |
|---|---|---:|---|---|
| 21 | 12: our balanced witnesses + chain exchange; also BMB flower and f20 | 12 | 12/12 | f(21)=12; no window20 dependency |
| 22 | 13: BMB thm:f20 only, using lem:window20 | 13 | 13/13 | f(22)=13 conditional on that lemma; otherwise 12≤f(22)≤13 |
| 23 | 13: our balanced witnesses + chain exchange; also BMB flower and f20 | 14 | 14/14 | 13≤f(23)≤14; rank restriction does not settle f(23) |
| 24 | 14: BMB prop:flower; also thm:f20 | 14 | 14/14 | f(24)=14 using flower, without window20 |

| n | A best word | Explicit families and both No-tree references | No-tree nodes, colours 0/1 |
|---|---|---|---|
| 21 | `0010011100101100011011` | [upper_n21.json](certificates/upper_n21.json) | 7,116 / 7,116, threshold 13 |
| 22 | `00100111010011100110100` | [upper_n22.json](certificates/upper_n22.json) | 13,422 / 9,133, threshold 14 |
| 23 | `001001110010110001101101` | [upper_n23.json](certificates/upper_n23.json) | 19,170 / 19,757, threshold 15 |
| 24 | `0011010011101001101010010` | [upper_n24.json](certificates/upper_n24.json) | 39,621 / 21,625, threshold 15 |

Each linked JSON contains the complete integer-mask witness for each colour. Distinctness, coordinate bounds, rank colour, and every pair's union and intersection were checked directly. The exhaustive No tree excludes a family of size maximum+1 or greater. Together these establish each stated exact colour maximum. All eight headline trees are retained directly as gzip files at the paths in those JSONs.

At n=21 the other optimal representative is `0011001011100010110011`, also with exact maxima 12/12; both words' witnesses and checked trees are in [best_n21.json](certificates/best_n21.json). At n=22 all seven optimal orbit representatives have exact maxima 13/13: the fourteen witnesses and tree references are in [n22_all_maxima.json](certificates/n22_all_maxima.json). Additional retained trees are streamed from `certificates/no_trees.tar.xz` by the replay script.

## Lower bounds and dependencies

The revised BMB manuscript gives

* chain: ceil((n+1)/2);
* prop:flower: ceil((n+1+floor((n+1)/12))/2);
* thm:f20: write n+1=20q+r, 0≤r<20, and e=1 if r≥12, else 0; the bound is ceil((n+1+2q+e)/2).

| n | Chain | Flower | f20 | q,r,e |
|---|---:|---:|---:|---|
| 21 | 11 | 12 | 12 | 1,2,0 |
| 22 | 12 | 12 | 13 | 1,3,0 |
| 23 | 12 | 13 | 13 | 1,4,0 |
| 24 | 13 | 14 | 14 | 1,5,0 |

We read the actual manuscript dependency chain: flower uses the elementary closure/product/concatenation facts, adjacent-set lemma, eight gadgets, twelve-letter word lemma, and twelve-rank window. It does **not** use lem:window20. The gadgets and all 4,096 twelve-letter words were also checked locally. The twenty-rank theorem does use lem:window20, including its external mixed-level computer-assisted calculation. That calculation was not rerun here. Thus only the n=22 equality needs that external computational assumption. Details are in [PROOF.md](PROOF.md), including the source distinction between the revised GitHub manuscript and older arXiv v1.

For odd n, if every monochromatic closed family had size at most (n+1)/2, every maximal chain would split evenly. Exchanging adjacent sets in two otherwise identical chains forces the colouring to depend only on rank. Our second code path supplies an explicit closed monochromatic family of size at least (n+3)/2 for every balanced word: **705,432 words at n=21**, and **2,704,156 at n=23**. Direct replay of every family and complete word coverage gives our own lower bounds 12 and 13. This is also a cross-check: the rank-screen certificates already cover these words. The chain-exchange argument cannot raise the n=23 unrestricted lower bound to 14.

Monotonicity: **f(n)≤f(n+1)**, since restricting any colouring to sets avoiding the last coordinate gives a copy of the smaller cube, whose closed families remain closed in the larger cube.

## Complete rank screens and the n=23 obstruction

| n | Rejected threshold T′−1 | All full words covered | Colour-swap/reversal orbits | Optimal orbits at T′ | All optimal words |
|---|---:|---:|---:|---:|---:|
| 21 | 11 | 4,194,304 | 1,049,600 | 2 | 4 |
| 22 | 12 | 8,388,608 | 2,098,176 | 7 | 28 |
| 23 | 13 | 16,777,216 | 4,196,352 | 141 | 536 |
| 24 | 13 | 33,554,432 | 8,390,656 | 1 | 4 |

Every rejection is covered by a concrete family, including class-size chains and factor witnesses. Factor witnesses are lifted into the full cube with the explicit offset recorded in the certificate. The checker verifies that lift, enumerates **all** 2^(n+1) words itself, applies colour swap and reversal itself, and requires covering evidence for each word. It does not accept the producer's orbit list as exhaustive. The four below-minimum screens cover 62,914,560 full words in total; no conclusion uses a truncated run.

At n=23 the standard target 13 failed. The complete n=22 classification explains why: any rank word of value at most 13 has a length-23 prefix in one of the seven optimal n=22 orbits. Each prefix has a 13-member family in both colours. Appending the new full set in its colour makes a 14-member closed family. We documented this failure and changed the upper-bound target to 14, certified both colour trees, then completed the rejecting threshold-13 screen and the threshold-14 list. A redundant direct finder at 13 was stopped; it supplies no claim.

The same argument excludes value 13 in the one-pivot class: the layer avoiding the distinguished coordinate is a rank colouring of the n=22 cube, and the full n=23 set extends the appropriate 13-family. This is a restricted observation, not an unrestricted lower bound or a novelty claim. **No non-rank search was run.** Closing the n=23 gap needs a non-rank construction beyond this one-pivot class at 13, or an unrestricted lower bound of 14.

The rank minima 12,12,13,14,14 at n=20..24 are nondecreasing. Exact values of the displayed best words' length-n prefix/suffix restrictions are respectively 12/12, 13/13, 14/14, 14/14 for n=21..24, each at least the preceding rank minimum and at most the current one. Witnesses and trees are in [crosschecks.json](certificates/crosschecks.json).

All lists G_L(T) are saved at every length in the corresponding `certificates/nN_TT/` directory. They contain every good word beginning with zero; colour swaps supply the other half. Checker-side counts agree with twice the list sizes at every length. All entries' No trees were checked during production, and terminal survivors were replayed before packing. The small delivered packet retains the 42 trees needed for the reported headline, alternative, classification, baseline and restriction claims. Unused G-membership tree caches are regenerable and were moved reversibly to macOS Trash; they are not included in the final packet. See [REPRODUCE.md](REPRODUCE.md) for regenerating those checks.

## Method, checks and changes

The weighted-poset reduction uses Birkhoff's representation of finite distributive lattices, with positive coordinate-block weights. The round-4 `poset.cpp`, `check.py` and `run.py` are byte-identical copies. The separately written old referee's C enumerator is also reused unchanged for balanced witnesses. Changes here add the new dimensions, streamed resumable prefix checkpoints, explicit suffix-factor offsets, five-worker scheduling of disjoint ordinary DFS branches, checker-owned full-word coverage and symmetries, and saved G lists. No new mathematical pruning rule was introduced. The proof of completeness and coordinate lifts is in [PROOF.md](PROOF.md).

Validation reproduced brute closed-family counts 73, 731, 12,084 and 319,987 at n=3..6, with zero rank-set disagreements. Both colours of 6,000 random words at n=11..16 agree with the separately written referee implementation. There were 400 planted weighted-poset tests at n=21..24. A small parallel-search control agrees with brute force at every length and resumes completed checkpoints without work.

Required corruptions were all rejected: dropped coverage leaf, shifted nonzero lift offset, flipped balanced-witness set, truncated No tree, changed weight and changed externally expected word. The delivered packet passed those corruption checks. Final replay checked 42 retained No trees, 490,225 nodes, all reported families, all full-word rejection coverage, and both complete balanced-witness lists in 80.97 seconds. Logs: [final_replay.json](logs/final_replay.json), [corruptions_delivered.log](logs/corruptions_delivered.log).

## Existing controls, sources and novelty

The public BLLM computation already states exact values through n=20 and uses the same weighted-poset method. We reproduced its n=20 word `000101100111001011100` with exact maxima 12/12 and checked No trees. We also reproduced round 4's `110010110001101100110` at 12/12. The launch planning note's suggestion that public exact values stopped at ten was incorrect; [PRIOR_ART.md](PRIOR_ART.md) corrects it explicitly.

| n | BMB printed finite upper formula | Simple inherited-colouring upper, inferred here | This job's checked upper |
|---|---:|---:|---:|
| 21 | 463 | 24 | 12 |
| 22 | 496 | 48 | 13 |
| 23 | 518 | 96 | 14 |
| 24 | 540 | 192 | 14 |

The middle column is an inference, not a printed table: ignore the added coordinates in the public n=20 colouring. Its 2^(n−20) slices each have maximum 12, and product witnesses attain the resulting 12·2^(n−20). These are exact combinatorial bounds, not predictive scores; SBS has no split or metric to apply to. [BASELINES.json](BASELINES.json) records this and both reproduced controls.

**Did we find something new? Yes, as candidate finite numerical extensions in the checked sources:** the four upper bounds improve the printed finite bounds under the same definition, and three meet the stated lower bounds, with the n=22 caveat. The method is existing work; reproductions, rank classification, and the one-pivot observation are not counted as new results. No priority “first” claim is made.

Final full-source checks were on 17 November 2026 at 19:04–19:05 UTC, followed by unchanged immediate pre-report rereads at **19:27:21–19:27:23 UTC**. We reread the [official problem](https://www.erdosproblems.com/1183), [forum](https://www.erdosproblems.com/forum/thread/1183), proof-claims page, [BMB repository and issues including #20](https://github.com/anaxia-research/Erdos-1183/issues/20), revised manuscript, BLLM theorem, and [arXiv:2610.02833](https://arxiv.org/abs/2610.02833). No n=21..24 finite values were found in those returned sources or the checked result repositories. This is a bounded search; source coverage limits are stated in PRIOR_ART.md.

The lower-bound manuscript is pinned to [BMB commit 2842ef3a](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/paper/Erdos.tex), revised 14 October 2026; arXiv v1 is dated 2 October and lacks these revisions. The existing exact method/finite table is pinned to [BLLM commit 241326bb](https://github.com/creelie/eBLLM/blob/241326bbba4726afde74ae1858265878b2176c59/paper/bllm/paper/sections/sec10d_crossing.tex). Dated source URLs and hashes remain in `sources/*fetch.json`; fetched bodies are losslessly archived in `sources/captures.tar.xz`.

## Resources and reproduction

The job used five search workers at nice 10, with at most one additional CPU task, within six cores. Metered search, checking and packing consumed approximately **9.31 core-hours**, including unsuccessful searches, the n=20 timing control and repeated packing; minor compilation/source utilities are not included. Maximum measured process RSS was **311,689,216 bytes**; peak sampled aggregate job RSS was **1,685,274,624 bytes**. Packing remained below 1 GB. The working directory was 7.12 GB immediately before reversible cache cleanup, below the 20 GB limit. Start: 16:26:17 UTC; all scientific stages finished within about three hours, with final reporting at about 3.2 hours, under the eight-hour wall limit. No scientific workers remain; the final descendant-process inspection is recorded in logs/processes_final.txt.

The required n=24 cost decision used measured n=20→22 CPU growth: 1,406.60→5,629.77 seconds, ratio 4.0024. It forecast 2.23 hours against 5.20 hours remaining, so n=24 ran. Its actual incremental upper/prefix/coverage stages took about 29 seconds because complete same-threshold n=23 prefixes were already available. This is reuse of completed work, not a cold-run speed claim. Details: [n24_cost_decision.json](logs/n24_cost_decision.json), [compute.json](logs/compute.json).

The final certificates occupy **39,729,675 distinct bytes** and source captures/metadata **5,790,677 bytes**, together **45,520,352 bytes**, below the 50 MB retention limit. Recompression at low preset 3 used a 32 MiB dictionary and verified equality of decompressed SHA256 hashes. Replaced files and unused caches went to macOS Trash. The certificate payload uses hard links for identical immutable prefix chunks; preserve hard links when copying it. Explicit balanced witnesses are streamed and compressed with bounded-memory xz. Retained proof scope and regeneration commands are in REPRODUCE.md; all claims above replay from the retained packet without the unused working caches.

From this directory, the short replay is:

```sh
RESEARCH_PYTHON="$HOME/dev/open-science/.venv/bin/python"
nice -n 10 "$RESEARCH_PYTHON" src/final_replay.py
nice -n 10 "$RESEARCH_PYTHON" src/corruptions.py
```

[REPRODUCE.md](REPRODUCE.md) includes compiler commands and complete producer/resume commands. No claim uses an incomplete checkpoint. No submissions, commits, pushes, PRs, posts or external messages were made.

## Open items and credits

The unrestricted n=23 value remains open between 13 and 14. The n=22 equality retains the external mixed-level lemma dependency; removing it requires an unrestricted lower-bound proof/check. All new claims need a referee outside this lane; none is implied by our checks.

Credit Erdős and Ulam for the problem; Bhattacharjee–Mandal–Bhattacharya for the lower-bound manuscript; Bhattacharjee and Bhattacharya/BLLM for the existing public weighted-poset computation; Birkhoff for the representation theorem; the round-4 producer and internal clean-room referee jobs; and both pre-launch computer-science reviews for the proof and certificate requirements. Earlier odd-rank rigidity and asymptotic work is credited in PROOF.md and PRIOR_ART.md.

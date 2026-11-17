Shipped: candidate, unrefereed f(15)..f(20) = 9, 9, 10, 10, 11, 12, with exact rank maxima, witnesses and replayable upper-bound trees; f(20)=12 depends on the revised BMB manuscript’s twenty-level lower-bound theorem.

Counts: **6 n tried; 6 values settled as candidates (5 with lower bounds proved here; 1 conditional on BMB thm:f20); 6 exact minima over rank colourings; 12 headline upper-bound certificates; 55,893 retained exhaustive no-tree certificates.** No result has human refereeing.

Ranks are read from 0 to n. Every family below is nonempty and closed under binary union and intersection; it need not contain ∅ or [n]. The definition, the reduction and all pruning proofs are in [PROOF.md](PROOF.md). These are separately written implementations in the same lane, not external review.

| n | Lower bound and source | Best word | Exact max c0 / c1 | Claim 1: upper | Claim 2: f(n) | Claim 3: rank minimum |
|---:|---|---|---:|---:|---|---:|
| 15 | 9: ours (balanced words); also prop:flower | `1100101100011010` | 9 / 8 | ≤ 9 | = 9, candidate | 9 |
| 16 | 9: chain | `00100111010011001` | 9 / 9 | ≤ 9 | = 9, candidate | 9 |
| 17 | 10: ours (balanced words); also prop:flower | `110010110001101001` | 10 / 10 | ≤ 10 | = 10, candidate | 10 |
| 18 | 10: chain | `0010110011101001100` | 10 / 10 | ≤ 10 | = 10, candidate | 10 |
| 19 | 11: ours (balanced words); also prop:flower | `00110010111000101101` | 11 / 11 | ≤ 11 | = 11, candidate | 11 |
| 20 | 12: BMB thm:f20* | `110010110001101100110` | 12 / 12 | ≤ 12 | = 12*, candidate | 12 |

*For n=20, prop:flower and the chain give eleven. The revised public GitHub manuscript’s thm:f20 gives twelve: n+1=20·1+1, so ceil((21+2)/2)=12. Its nineteen-coordinate window lemma includes an external mixed-level computation that was **not rerun here**. If that theorem is withheld, the unrestricted statement from this job is **11≤f(20)≤12**. The rank minimum twelve and the upper bound twelve are certified here without that dependency. All other rows have unrestricted lower bounds proved in this job. There is no gap relative to the stated strongest manuscript lower bounds.

## Exact maximum witnesses and upper trees

The following decimal masks use bit i for coordinate i+1. Every list was checked for distinctness, colour, coordinate range and direct closure under every pairwise bitwise union and intersection. Each linked no-tree proves there is no family of at least maximum+1 in that colour. The stronger per-colour bound at n=15 is eight in colour 1.

**n=15, word `1100101100011010`.**

- Colour 0, maximum 9: `[3, 7, 31, 999, 1023, 31751, 31775, 32743, 32767]`. [No-tree at threshold 10](certificates/search_1100101100011010_c0_t10.tree.gz), 498 valid nodes.
- Colour 1, maximum 8: `[0, 1, 15, 113, 127, 2047, 4095, 16383]`. [No-tree at threshold 9](certificates/search_1100101100011010_c1_t9.tree.gz), 403 valid nodes.

**n=16, word `00100111010011001`.**

- Colour 0, maximum 9: `[0, 1, 14, 15, 2033, 2047, 16369, 16383, 32767]`. [No-tree at threshold 10](certificates/search_00100111010011001_c0_t10.tree.gz), 1,114 valid nodes.
- Colour 1, maximum 9: `[3, 31, 483, 511, 7711, 8191, 57827, 57855, 65535]`. [No-tree at threshold 10](certificates/search_00100111010011001_c1_t10.tree.gz), 552 valid nodes.

**n=17, word `110010110001101001`.**

- Colour 0, maximum 10: `[3, 7, 31, 999, 1023, 31751, 31775, 32743, 32767, 65535]`. [No-tree at threshold 11](certificates/search_110010110001101001_c0_t11.tree.gz), 1,255 valid nodes.
- Colour 1, maximum 10: `[0, 1, 126, 127, 3969, 4095, 126977, 127103, 130945, 131071]`. [No-tree at threshold 11](certificates/search_110010110001101001_c1_t11.tree.gz), 1,043 valid nodes.

**n=18, word `0010110011101001100`.**

- Colour 0, maximum 10: `[0, 1, 126, 127, 8065, 8191, 123007, 131071, 139263, 262143]`. [No-tree at threshold 11](certificates/search_0010110011101001100_c0_t11.tree.gz), 2,369 valid nodes.
- Colour 1, maximum 10: `[3, 15, 31, 495, 511, 3615, 4095, 29183, 32767, 65535]`. [No-tree at threshold 11](certificates/search_0010110011101001100_c1_t11.tree.gz), 1,330 valid nodes.

**n=19, word `00110010111000101101`.**

- Colour 0, maximum 11: `[0, 1, 30, 31, 2017, 2047, 6175, 8191, 26623, 32767, 262143]`. [No-tree at threshold 12](certificates/search_00110010111000101101_c0_t12.tree.gz), 2,709 valid nodes.
- Colour 1, maximum 11: `[3, 7, 63, 255, 511, 767, 1023, 16383, 65535, 475135, 524287]`. [No-tree at threshold 12](certificates/search_00110010111000101101_c1_t12.tree.gz), 2,606 valid nodes.

**n=20, word `110010110001101100110`.**

- Colour 0, maximum 12: `[3, 7, 31, 255, 511, 767, 1023, 8191, 58367, 65535, 991231, 1048575]`. [No-tree at threshold 13](certificates/search_110010110001101100110_c0_t13.tree.gz), 3,577 valid nodes.
- Colour 1, maximum 12: `[0, 1, 15, 113, 127, 16271, 16383, 245887, 262143, 278415, 278527, 524287]`. [No-tree at threshold 13](certificates/search_110010110001101100110_c1_t13.tree.gz), 7,471 valid nodes.

## Complete rank search and odd lower proofs

The first pass tested all 126 right extensions of the n=14 word, at depths one through six. It found words meeting the lower bound for n=15,17,20; the full screen found the missing n=16,18,19 words. [Extension results](logs/extensions.json).

Each full screen uses colour swap and reversal, with the larger-class chain filter. A catalogue entry is an actual closed family; a reused entry is accepted only when all its member ranks have the required colour, and every emitted rejection is directly checked. This witness reuse is proved sound by membership alone. No decision is inferred from a multiset of sums. The exhaustive screens one below the reported minima reject every orbit:

| n | Full-word orbits rejected below the minimum | Threshold witnessed |
|---:|---:|---:|
| 15 | 16,512 | ≥ 9 |
| 16 | 32,896 | ≥ 9 |
| 17 | 65,792 | ≥ 10 |
| 18 | 131,328 | ≥ 10 |
| 19 | 262,656 | ≥ 11 |
| 20 | 524,800 | ≥ 12 |

Full screens at the attained bound additionally give 8 / 76 / 3 surviving orbits at n=14 / 15 / 16, and 2 / 10 at n=18 / 19. The prefix branch-and-bound reproduces exactly all 8 / 76 / 3 survivors at n=14..16. Prefix searches below the minima at n=17..20 also reject every branch. Each pruned prefix carries a concrete family; factor monotonicity embeds it into every extension. [Full-screen logs](logs/screens.log), [larger prefix logs](logs/prefix_large.log). All rejection lists and prefix witnesses are in `certificates/*_screen.jsonl.xz` and `*_prefix.jsonl.xz`.

For the odd lower bounds, **every** balanced rank word was expanded and directly checked: 12,870 words at n=15 (family ≥9), 48,620 at n=17 (≥10), and 184,756 at n=19 (≥11). By the chain-exchange lemma this rules out all colourings at the chain bound, not just rank colourings. [Counts](logs/balanced.json); complete witness lists `certificates/n{15,17,19}_balanced.jsonl.xz`.

## Validation and replay

- Brute-force NextClosure enumeration of all nonempty sublattices gives **73, 731, 12,084, 319,987** at n=3,4,5,6. For every rank word at n≤6, both colour maxima agree with the poset search (zero mismatches). [Brute output](logs/brute.jsonl).
- All rank words at n=11..14 were screened below the published bounds; none beats them. The prior words reproduce colour maxima (7,7), (7,7), (8,7), (8,8), hence overall 7,7,8,8. [Baseline reproduction](logs/results.log).
- 1,000 random words per n=11..16, both colours, agree with the referee’s separately written poset_search.py; 600 planted weighted-poset tests at n=15..20 pass. The seed and threshold distribution are explicit in src/validate.py. [Validation summary](logs/validation.json).
- The separately written checker rejected deletion of a subtree, a changed weight and a flipped word letter. A self-consistent changed-word header was also rejected. It binds the expected word externally, reconstructs down-sets from the predecessor relation, checks every branch and invalidity witness, and enforces the chain-node floor 2^|R|−1.
- The final mathematical replay checked the twelve headline upper trees, all surviving screen words, **1,501,085** full-screen rejection records, all seven prefix screens, and every balanced-word witness. [Replay output](logs/replay.log). The initial replay paused while larger prefix files finished; the final replay also checks the delivered compressed tables. CPU time is reported below.
- One reporting assertion initially demanded both n=13 colours attain eight; it was reverted and corrected to the maximum over colours (8 and 7). A Python 3.12 packaging API error was also reverted before switching to its supported standard writer. Both are documented in STATUS.md; neither altered the search or a mathematical certificate.

Replay commands and full rebuild commands are in [REPRODUCE.md](REPRODUCE.md). Headline machine-readable data are in [results.json](certificates/results.json). Other exhaustive no-trees are losslessly packed into [no_trees.tar.xz](certificates/no_trees.tar.xz); directly referenced trees remain individually available. The checker can read either spelling. No SAT run was used. No predictive score was claimed, so the trivial/simple/method SBS rule is inapplicable.

## Public status, dependencies and credit

Source bodies are retained in sources/captures.tar.xz (extract with Python’s tarfile command); the dated fetch records remain directly readable. Initial and final public reads are recorded in [PRIOR_ART.md](PRIOR_ART.md), with source captures and dates. The eighteen-source recheck was 17 November 2026, 13:42:36 UTC; fourteen further mandatory-source and repository-root reads immediately before reporting, at 14:06:27 UTC, were also unchanged (sources/pre_report_fetch.json). Problem-page and forum mathematical visible text were unchanged; all other repeated source bodies were byte-identical. Issue #20 contains only the prior f(11)..f(14) candidates. No public exact f(15)..f(20) value was found in the checked problem/forum, repository/issues, omega note, arXiv or named AI-result repositories. This is a bounded priority search, not a claim to have searched all possible publications.

The arXiv v1 source (2 October 2026) has only the chain lower bound. The improved bounds are in the [revised GitHub manuscript](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/paper/Erdos.tex), dated 14 October. Its prop:flower gives 9,9,10,10,11,11; thm:f20 improves the last to 12. The unchanged [omega note](https://github.com/the-omega-institute/trureturing/blob/HEAD/Problems/bhattacharjee-mandal-bhattacharya-2026-sublattice-chain-bound-refutation.md) states (n+3)/2 for every odd n≥11 and claims Lean verification; it adds no stronger number here. Lean and the external mixed-level check were not rerun. The prop:flower dependency chain was read lemma by lemma; all eight gadget families and all 4,096 length-twelve words were additionally checked in src/lower_review.py. [Bound arithmetic](logs/lower_bounds.json).

**Did we find something new? Yes, candidate numerical values relative to the public sources checked:** the six equalities in the table, with the stated n=20 dependency. The search method is the existing referee method extended to these dimensions, not a new general method. No priority “first” is claimed.

Credit: Erdős and Ulam for the problem; Bhattacharjee–Mandal–Bhattacharya for the manuscript bounds; the omega institute for its odd-bound note; Birkhoff for the representation theorem; our n=13/14 referee job for the weighted-poset method; and the pre-launch review for the positivity lemma, completeness argument and proof-tree requirements. All checks here are separately written within the same lane. These are candidate, unrefereed claims.

## Compute and open items

Measured scientific-stage CPU: **0.3618 core-hours** (1302.38 CPU seconds). Largest `/usr/bin/time -l` process RSS: **2,915,647,488 bytes** (2915.6 MB). Largest sampled coordinator-plus-descendants RSS in a guarded run: **2,915,631,104 bytes** (2915.6 MB). These are run-level measurements; compiling, source retrieval and this report’s generation add small unmetered costs. Concurrent stages used fewer than six cores and remained far below the 4 GB target and 8 GB guard. Scientific commands ran at nice 10 or lower priority. No worker is left running (final process snapshot in logs/processes_final.txt).

| Stage | Wall seconds | CPU seconds | Peak process RSS (MB) |
|---|---:|---:|---:|
| baseline | 0.06 | 0.00 | 2.3 |
| brute | 0.95 | 0.81 | 2.2 |
| extensions | 2.24 | 2.22 | 22.4 |
| validation | 8.18 | 7.78 | 36.4 |
| screens | 180.44 | 179.65 | 118.6 |
| balanced | 6.10 | 5.35 | 46.9 |
| results | 0.68 | 0.66 | 21.4 |
| prefix_large | 416.68 | 416.52 | 105.5 |
| replay_before_pack | 378.50 | 34.30 | 47.7 |
| replay | 30.32 | 29.87 | 57.0 |
| packing_default | 195.84 | 187.95 | 184.5 |
| pack_probe | 10.98 | 10.96 | 773.4 |
| packing_preset9 | 195.90 | 195.04 | 793.3 |
| pack_probe256 | 10.78 | 10.76 | 1567.0 |
| packing | 195.85 | 195.92 | 2915.6 |
| witness_packing | 16.63 | 16.61 | 120.9 |
| source_packing | 4.58 | 4.55 | 160.2 |
| archive_check | 3.45 | 3.43 | 316.1 |

Tree archive: 42,546,176 bytes for 55,684 archived trees, plus 209 directly accessible trees (including the twelve headline certificates). Retained data size and exact process termination were checked after packing. The original packed gzip copies were moved reversibly to the macOS Trash.

Certificate/data payload: 49,184,899 bytes (under 50 MB); reference-source captures and metadata: 3,269,898 additional bytes. The whole job remains far below its 20 GB disk budget.

Open items: external human refereeing of the reduction, code and numerical claims; and, if a self-contained unrestricted f(20)=12 proof is desired, replay/referee the revised manuscript’s mixed-level twenty-window computation. Without that external theorem, retain the explicit gap 11..12 for f(20). No submissions, commits, pushes, PRs, posts or messages were made.

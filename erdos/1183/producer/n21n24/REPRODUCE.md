# Reproduce the candidate, unrefereed results

Run from this job directory. Use the shared research Python and nice 10. The mathematical search and tree checker use only the standard library; C/C++ builds use clang/clang++.

```sh
RESEARCH_PYTHON="$HOME/dev/open-science/.venv/bin/python"
clang++ -O3 -std=c++17 src/poset.cpp -o src/poset
clang++ -O3 -std=c++17 src/coverage.cpp -o src/coverage
clang -O3 -std=c11 src/balanced_referee.c -o src/balanced_referee
```

For a given n, first run `src/upper.py n`, which tries extensions of round-4 and this round's earlier words. If extensions fail, the standard full orbit search in `screen.full(n,T,runner,True,label)` searches for a word at the lower bound T. `src/finish_upper.py logs/<label>.json` reads the found word directly from that result and produces both exact maxima, concrete witnesses and exhaustive no-trees. The baseline n=20 row lives in certificates/upper_n20.json; the four requested headline rows are certificates/upper_n21.json through upper_n24.json when present.

Then run the prefix screens at one below the attained rank bound, and at the bound. For example:

```sh
nice -n 10 "$RESEARCH_PYTHON" src/guard.py "$RESEARCH_PYTHON" src/prefix_resume.py 21 11
nice -n 10 "$RESEARCH_PYTHON" src/guard.py "$RESEARCH_PYTHON" src/prefix_resume.py 21 12
nice -n 10 "$RESEARCH_PYTHON" src/coverage.py 21 11
nice -n 10 "$RESEARCH_PYTHON" src/coverage.py 21 12
```

Checkpoints in certificates/nN_TT/checkpoint.json hold the remaining DFS stack. Repeating a prefix command resumes it, and repeats nothing after a completed checkpoint. Each committed gzip segment contains concrete factor witnesses or good prefixes with two no-tree paths. No claim uses an incomplete checkpoint. The preceding dimension's complete records may be reused at the same threshold; only good terminal words can extend. The coverage checker uses its own full word enumeration at every length and verifies terminal survivor trees and all rejection families, not the producer's orbit list.

G_L(T) lists in those directories contain every good word whose first letter is zero. The colour swap of each supplies the other half. Words are written as strings in rank order, length L; the corresponding cube has dimension L-1. These are saved for a later one-pivot search; this job runs no non-rank search.

The odd-n second-code-path cross-check produces one explicit family per balanced word:

```sh
nice -n 10 src/balanced_referee bal 21 > certificates/n21_balanced.txt
nice -n 10 "$RESEARCH_PYTHON" src/check_balanced.py 21 certificates/n21_balanced.txt
```

Use 23 in place of 21 for the other odd dimension. Both output and checker are streamed; the checker's complete-word seen bitmap is at most 16 MiB. `src/corruptions.py` tests dropped coverage, altered factor offset, flipped balanced witness member, truncated tree, changed tree weight and changed externally bound word. Original certificates are preserved. This is separate implementation within the same lane, a same-lane replay.

One upper-bound tree can be checked directly, with the expected word, colour and threshold bound externally:

```sh
nice -n 10 "$RESEARCH_PYTHON" src/check.py certificates/search_0010011100101100011011_c0_t13.tree.gz 0010011100101100011011 0 13
```

PROOF.md gives the mathematical reduction, completeness, symmetry, factor-lift and chain-exchange proofs. PRIOR_ART.md distinguishes the revised GitHub manuscript from arXiv v1. The external mixed-level computation behind BMB lem:window20 is not rerun by these commands; n=22's lower bound 13 retains that dependency.

Every intermediate G-list entry had two no-trees checked by Runner at production. After regenerating unused caches, `src/coverage_all_prefix_trees.py N T` can replay all of those additionally. The default coverage replay checks all positive rejections and full-length survivor trees, as in round 4; attained-bound runs need the regenerated unused survivor caches or the `--coverage-only` option described below. Both enumerate every word using checker-side symmetries.


For the larger G-list searches use ordinary parallel scheduling of the same DFS:

```sh
nice -n 10 "$RESEARCH_PYTHON" src/guard.py "$RESEARCH_PYTHON" src/parallel_prefix.py 22 13 5
```

The first argument is n, the second is the allowed maximum T, and the last is the worker count. Five workers leave one of the six allowed cores for the isolated timing baseline. `part*/checkpoint.json` keeps each unprocessed stack; the parent `parallel.json` fixes the partition and the saved base records. Re-running the command resumes unfinished parts and then merges their unchanged records. It neither starts a non-rank search nor changes the weighted-poset algorithm. The n=4 parallel G lists were compared with brute force at all five lengths, and the merged large runs use the same full coverage checker.


The n=23 target differs from its manuscript lower bound. Target 13 fails because every one of the seven n=22 optimal orbits has maxima 13/13; adding the new full set in its colour forces 14. `certificates/n22_all_maxima.json` gives those fourteen witnesses and trees, and PROOF.md proves the implication. Thus this row uses `src/upper.py 23 14`, followed by prefix/coverage searches at T=13 and T=14. The earlier direct full finder at 13 was deliberately stopped; no claim uses that truncated run. The completed positive-witness screen at T=13 supplies the full rank lower certificate.

`src/final_replay.py` checks the delivered headline families, all required no-trees, full-word coverage and both balanced-word lists. It reads selected archived no-trees in a single streaming pass. Intermediate no-trees were already checked when the G lists were generated; the optional all-prefix replay can be rebuilt from the producer if those caches are not retained in the small final packet.


The delivered packet retains 42 No trees for the reported words, the seven n=22 classification representatives, baselines and restriction checks. All G-list membership trees were checked during production and the complete terminal replays recorded in logs/nN_TT_coverage.json; unused membership No files are regenerable working caches and are excluded from the small packet. To replay every retained claim use:

```sh
nice -n 10 "$RESEARCH_PYTHON" src/final_replay.py
nice -n 10 "$RESEARCH_PYTHON" src/corruptions.py
```

For an attained-bound G-list coverage/count replay without regenerating its unused No cache, use `src/coverage.py N T --coverage-only`. Below-minimum screens have no terminal good words, so their ordinary replay needs only the delivered positive witnesses. To recheck an individual G-list member's upper bound from scratch, run Runner.decide(word,c,T+1) for both colours; the unchanged search produces the No files and the original checker verifies them. Intermediate/all-entry No replay requires regenerating those caches first.

Identical immutable prefix chunks use hard links. Preserve hard links when copying the whole packet. The distinct certificate/data payload is under 50 MB; logical path sizes count inherited chunks more than once.

Final lossless compression uses xz preset 3 with a 32 MiB dictionary. Certificates plus source captures/metadata occupy 45,520,352 distinct bytes; see logs/retained_sizes.json. The fetched source bodies now live only in sources/captures.tar.xz; source paths recorded earlier in PRIOR_ART.md refer to archive members.

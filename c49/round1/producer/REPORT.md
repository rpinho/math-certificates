Shipped: a candidate, unrefereed C49 lower bound (64728+sqrt(3019700660))^(1/26) = 1.567864384572806979362033445047060687289228710864066381805835... , with a complete 252303-set block and separately written checker (same agent).

This exceeds the exact frozen Koshta bar by **0.000004482148217093509118015914783074906769324255439225090732...**. The ground set is still 28 points, the ports are still 0 and 1, and the gluing theorem and exponent 1/26 are unchanged.

| Block | Sets | N00 | N01 | N10 | N11 |
|---|---:|---:|---:|---:|---:|
| Koshta baseline | 252292 | 33969 | 64728 | 64728 | 88867 |
| This candidate | 252303 | 33980 | 64728 | 64728 | 88867 |

The transfer matrix is `[[64728,88867],[33980,64728]]`; its Perron root is `64728+sqrt(3019700660)`. Only N00 increases, by eleven. The certified rate lies between the adjacent 60-place decimals ending `...805835` and `...805836` printed in `logs/final_best_check.json`. Integer/rational root isolation compares it against the **exact** baseline surd root, rather than a truncated decimal.

The complete integer-mask certificate is `certificates/best_1.5678643845728069793620.json`. `certificates/best_delta.json` lists its exact difference from the baseline: retain all 252271 product and lifted pendant augmentation members; replace the original 21 exceptional members with 32 members, sixteen seven-element sets wholly inside each pendant. The 806 lifted members at each pendant are retained in full; this is not a fifteen-full-set simplification.

`checker.py` is **separately written (same agent), not independent**. It checks mask ranges, distinctness, Sperner, absence of a sunflower among three distinct members, port counts, matrix and rate. It derives 107 disjoint Cartesian boxes directly from the actual masks, then exhausts pair/triple existence on their coordinate factors. It assumes neither validity of F/H nor the source construction. SEARCH_NOTES.md gives the argument that this is an exhaustive check of the original definition. The finite-to-asymptotic mathematical input is DEGKM1997 Lemma 4.4 and the IRSI positive transfer-matrix chain argument. SOURCE_STATEMENTS.md quotes the requested definition and gluing statements verbatim, with source licenses retained.

All four rejection controls on this best block fail as required (`logs/best_controls.json`):

- A Sperner-compatible added mask creates the distinct sunflower `[61603840,199491584,61112067]`.
- A duplicated member is rejected.
- Adding the empty set is rejected for containment.
- A raised claimed rate is rejected by exact arithmetic.

The checker also matched literal pair/triple enumeration on 500 small families. These checks support the finite certificate; they do not constitute outside refereeing.

What paid was distributing exceptional members across both pendants. Normal-first exhaustive extension found no addable mask among all 2^28 masks of the original block. Exact deletion-cover search ruled out the requested one/two-deletion exchanges and all improving exchanges through five deletions. At six deletions, one removal choice unlocked 166 candidates; exact CP-SAT selected sixteen compatible additions, giving the first improvement, 252302 members. Releasing all 21 original exceptional members then gave a 344-candidate model and the 32-addition candidate above. The successful first pool solve took 10.15 seconds and 172179456 bytes peak RSS. Its sixteen-addition optimum is only for those six fixed removals.

The final block is maximal over all 2^28 masks. The subsequent local search excludes every improving exchange with at most seven old-member deletions: 1198 introducible masks, 147630 unions of minimal covers, and 108 residual pools. For the twelve residual unions of size six, an all-new sunflower prevents selecting all seven N00 candidates, even if a seventh old member is removed; this closes the proper-union issue that fixed-removal SAT alone would miss. See `logs/r7_superset_proof.json`. Holding the product core and 32 exceptions fixed, changes deleting up to four lifted templates per pendant give 85 legal options per side and 7225 joint choices; none raises the Perron root.

Broader coupled CP-SAT searched 2648 core/pendant/exception templates, including changes to both augmentations and the core. Its full core-deletion neighborhood was reached; the final stage used a weighted-objective improvement constraint. This heuristic template search is not an exhaustive global search. The separate three-hour 344-candidate exceptional-member optimization ended FEASIBLE with 32 additions and solver upper bound 50; a ten-minute target-33 feasibility run ended UNKNOWN. **Optimality is not established.** These domains differ from Sylla's one-pendant 123-candidate problem; no improvement from merely replaying that problem is claimed.

The numerical search stopped at **2026-11-14T06:24:23.811088+00:00**, after **10862.4 seconds** without a further improving move (last improvement 2026-11-14T03:23:21.368399+00:00). Timed computation used approximately **9.51 core-hours**, excluding small untimed setup/interactive overhead. The largest measured aggregate job RSS was **2435252224 bytes (2.435 GB)**, below 4 GB. Workers ran at nice 10; solver allocations were at most four coupled-search threads plus two exceptional-search threads, with short additional one-core searches. All workers are stopped.

Baseline reconstruction was exact: all 252292 masks equal the public data, decompressed SHA-256 `10ee18f93204468f3611d2c909a9eee443f3b4769cf7fddd964209edfebd4838`; counts and 1.567859902424589885852915429132277612382459386608627156715102... reproduce. Rebuilding took 0.60 seconds, peak RSS 134201344 bytes; the baseline validity/rate check took 0.18 seconds, peak RSS 61571072 bytes. The final candidate check took 0.18 seconds, peak RSS 61308928 bytes. These are separate sequential process measurements, not an estimate for a parallel job.

To reproduce the claimed bound, no solver or third-party construction code is needed:

```sh
python3 checker.py certificates/best_1.5678643845728069793620.json
python3 controls.py certificates/best_1.5678643845728069793620.json --output logs/replayed_best_controls.json
```

The checker uses the Python standard library. ENVIRONMENT.json records Python 3.12.13 and OR-Tools 9.15.6755 for the search. To rebuild and reproduce the successful search path from the supplied source data, set `PY` to the shared environment Python:

```sh
nice -n 10 $PY prepare.py
nice -n 10 $PY checker.py certificates/baseline.json
clang++ -O3 -std=c++17 extension.cpp -o extension
nice -n 10 ./extension certificates/baseline.masks logs/addable.masks
clang++ -O3 -std=c++17 exchange_wide.cpp -o exchange_wide
clang++ -O3 -std=c++17 exchange_exact_wide.cpp -o exchange_exact_wide
nice -n 10 ./exchange_wide certificates/baseline.masks 6 _r6
nice -n 10 ./exchange_exact_wide 6 _r6
nice -n 10 $PY combine_exchanges.py --radius 6
nice -n 10 $PY pool_search.py --radius 6 --seconds 300
nice -n 10 ./extension certificates/fixed_core.masks logs/free_extras.masks
nice -n 10 $PY free_extras.py --all-extras --seconds 300 --threads 2
```

Parallel CP-SAT may return a different equivalent family; the supplied full certificate fixes the actual claimed object. Large derived candidate streams and clause caches are compressed; originals were moved to macOS Trash. No requested best certificate was removed.

The final public-source check still lists Koshta's bar on the [live page](https://teorth.github.io/optimizationproblems/constants/49a.html). The required [#357](https://github.com/teorth/optimizationproblems/pull/357), [#326](https://github.com/teorth/optimizationproblems/pull/326), [#322](https://github.com/teorth/optimizationproblems/pull/322) and [#235](https://github.com/teorth/optimizationproblems/pull/235) remain open and contain no higher numerical bound. PRIOR_ART.md records the bounded GitHub, named AI-result-repository and arXiv searches and their limits. No novelty judgment is made.

CODE_BLOBS.json records `git hash-object` for **all 30 local code files**, including backups and compiled executables. None equals any of the 40 blobs in the recursive GitHub tree API responses for DennisKoshta at `c4ee81737f9f6a4ae9793586a27004553a12d5c0`, Aspect5 at `e478c81d8b57eba956fdaf621643eb6f0781f820`, joshua17-create at `6e34d78ab482f4cfd5a5ece62a6d06141e3e8c8d`, and xSyllaa at `8e21d0287711b4f0bfc23e9443523e2aa472cca1`. Their code was not downloaded, copied, imported or executed. We read mathematical descriptions and certificate data only.

Credit: **D. Koshta with Claude** for the incumbent two-pendant block; **IRSI/Aspect5** for exact transfer counting of DEGKM's gluing chain; **joshua17-create/Claude** for F and H; **Sylla** for pendant augmentation. This is an optimization of that construction. No submission, commit, push, PR, post or external message was made. A next numerical target is an exchange beyond seven members or a change to the pendant projection families; the current restricted searches do not settle either.

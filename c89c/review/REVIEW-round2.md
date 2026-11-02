# Fresh adversarial review of c89cr2

**Mathematical verdict: PASS for C89c >= 0.000025987181439 and C89b >= 0.001524159308866, in the definitions of PRs #279 and #277.** A fresh exact checker reproduces the frozen inequalities from the proof and integer factors. No gap in the proof of either lower bound was found. Search-history reproduction and exhaustive priority are outside this PASS.

There is one useful simplification: **the primary C89c bound already follows from eight-vertex inequalities with the frozen factors.** The nine-vertex work is valid but unnecessary for the stated number. There is also a wording correction about negative eight-vertex residuals, explained below.

The reviewer did not author the submitted proof or verifier. I read the machine rules, submitted proof and certificate format, wrote and hashed `scripts/reviewer_exact.cpp`, and ran it on the old baseline and both new C6 artifacts before opening any submitted verifier source. The C5 run was already running with that same source. The independently written checker was never changed after that freeze: SHA256 `205b24967f0ba8467922a2498e55798d29da479912e638eaaadb60de55e67b53`. See `INDEPENDENCE.md` and `receipts/reviewer_source_before_author_read.sha256`.


The previous review accepted `../sweep3/c6_8.cert`: n=8, k=6, unordered roots, D=10^9, 13 blocks, 793 square rows, bound 21083/10^9. Its proof describes the two families (2,3),(4,2) at `../sweep3/PROOF.md:22–45`. I independently reproduced that exact result, including exhaustive disjoint coverage of 268435456 labelled graphs and minimum slack 42383221189/35000000000000000000 at graph 198.

Freshly fetched `sources/pr277.diff:33–39` defines C89b by the number of monochromatic five-element vertex sets divided by binomial(N,5). `sources/pr279.diff:86–92` gives the analogous definition for six-element sets. This agrees with the new `../c89cr2/PROOF.md:15–17` and the direct counts in the checkers. Both colours count once. There is no missing factor 2, k!, 512 or 16384. The random-colouring reference densities are 1/512 and 1/16384; C89c's stated value is 0.425773980696576 times its random reference. The factor 2^-14 used to display upper bounds in #279 is not part of the definition.

In the tables below, `P`, `R` and `V` mean the frozen submitted `../c89cr2/PROOF.md`, `../c89cr2/REPORT.md`, and `../c89cr2/scripts/verify_frozen.cpp`. Line numbers refer to these exact files. The proof is fixed by the archive manifest. A new step means a change relative to the previous review's accepted primary artifact, not a claim that the mathematical idea is new.


| New or generalized step | Exact submitted lines | Verdict | Independent check / reason |
|---|---|---|---|
| Add the C5 target and its normalization | P:7–9,15–17; V:41–44 | PASS | Directly counts both all-red and all-blue five-sets, denominator 56. Fresh #277 definition agrees. |
| Change the C6 target value and integer factors | P:7–8,35; V:26–29,44–46 | PASS | Recomputed every Gram product and every coefficient from frozen integers; exact positive minima below. |
| Restore/use the empty-root (0,4) family | P:23,35; V:31–36 | PASS | Includes one type and 11 unrooted four-vertex flags. Fixed empty roots still give a probability vector and a nonnegative independent-sample square. |
| Enlarge C6 to 14 blocks and 1303 rows, D=10^12 | P:25–35; V:28–33 | PASS | Independently parsed counts, checked complete nonoverlapping flag orbits, and rebuilt L^T L. Arbitrary integer rows are valid square factors. |
| Introduce labelled/ordered roots for the final C5 theorem | P:23,37,46,90–92; V:30,32,36 | PASS | Labels stay fixed in flag isomorphisms. Enumerated all t! actual root orders, using the same order for both extensions. Wrong labelled types contribute zero. |
| Add ordered-root (6,1) blocks | P:37; V:28–36 | PASS | 156 six-vertex root types; 170 blocks and 13227 factor rows in total. Included-type flag coverage and duplicate-orbit rejection checked separately. |
| Ordered-root normalization by t! | P:44–46,52; V:30,36 | PASS | Explicit sampling counts give 70,1120,10080,40320. No extra automorphism factor is needed when averaging all root injections. Fresh ordered-root K3/K4 tests also pass. |
| Allow unused ambient vertices | P:41–44,100–102; V:28,36 | PASS | Explicitly chooses two disjoint m-subsets even when vertices remain unused. Each triple lies in the same binomial(N-t-2m,n-t-2m) ambient subsets. |
| Ambient-nine C6 denominators and target | P:35,52; V:30,36,41–45 | PASS | Denominators 630,5040,3780 and target denominator 84. Submitted direct enumeration agrees with independent deletion averaging. |
| Off-diagonal multiplicity after both changes | P:46; V:36,45 | PASS | Both (A,B) and (B,A) occur. Full matrix Gram entries are used for each ordered occurrence; no lost/doubled cross term. |
| Relabelling invariance with labelled roots | P:54 | PASS | A vertex bijection sends root injections and ordered disjoint extensions bijectively to their counterparts, preserving the fixed label positions. |
| Replace checked 128-bit arithmetic by GMP | P:67–69; V:15,29,35,44–46 | PASS | All Gram products and inequality decisions use arbitrary-precision integers. Native small integers only index/count bounded finite sampling spaces. |
| New direct frozen checker | P:67; V:26–49 | PASS | Source audited after independent checker was frozen. It reads the certificate and graph list, not solver/search coefficients. Fresh replay matches all three minima. |
| Adapt the legacy eight-vertex checker to GMP and ordered roots | P:69; `verify_legacy_gmp.cpp:27–42,46–65,90–109` | PASS | Integer parsing, Gram formation, root-order enumeration, target count and orbit cover implement the proof; both new eight-vertex certificates also pass fresh legacy replay. |
| Revalidate exhaustive eight-vertex input | P:60,63; V:38–43,48 | PASS | Reviewer orbit map independently assigns all 2^28 labelled graphs to exactly one of 12346 classes. Random normalization also passes in submitted replays. |
| Prove nine-vertex list completeness | P:61,65; `check_graph9.py:15–25` | PASS | Fresh implementation checks every one of 3160576 augmentations; exactly 274668 distinct nine-vertex classes, no missing or duplicate class. |
| New deletion identity and lifted exact replay | P:71–76; `verify_lift9.cpp:93–129` | PASS | Every product uses eight vertices and has one unused vertex. For p_k, every k-set survives 9-k deletions. Both averages therefore equal the nine-vertex quantity. Reviewer rebuilds its own labelled-eight index. |
| New coefficient minima and bounds | P:78–84 | PASS | Reviewer independently reproduces all fractions and minimizing indices exactly, including all ordered C5 coefficients. |
| Conditional positivity for ordered roots | P:90–92 | PASS | Condition on the actual root injection, then independent extensions produce x_R^T L^T L x_R / D^2 >=0. Type mismatch remains zero. |
| Extend finite-sampling error to ordered roots and unused vertices | P:94–106 | PASS | Overlap probability <=m^2/(N-t); conditioning changes a bounded expectation by <=2 M_Q times this probability. Uniform ambient sampling gives the same disjoint-triple law. |
| Conclude both limits uniformly | P:104–110 | PASS | Fixed finite matrices give a uniform O(1/N) error. Minimize over G, then take N to infinity. No Ramsey-number assumption is introduced. |
| Identify the exact frozen bytes | P:114–120; R:77–80 | PASS | Independent archive audit verifies all 107 manifest members and the reported 8800036-byte archive SHA256. |

The core square-positivity and overlap arguments were present in the previous round; the rows above check their new ordered-root, C5 and unused-vertex applications rather than accepting those extensions on analogy.


The factor body after the header is byte-identical between `c6_8.cert.gz` (decompressed) and `c6_9.cert`: SHA256 of the newline-joined body is `52beed0c11f1d936e54a8ee0c65764177dfe571811e6fd8f7bf94d6db210d89e`. Only ambient order and the stated bound change.

Using the **primary** bound b=25987181439/10^15, the reviewer finds at ambient order eight:

```
min_H [p6(H)-a8(H)-b]
= 7421426482829 / 420000000000000000000000000
= 1.767006305435476...e-14 > 0,
```

at graph 11661, with **zero negative residuals**. Changing only the primary header's n from 9 to 8 also passes the submitted direct checker (`receipts/author_primary_as8.log`). Thus the stated primary theorem needs no nine-vertex graph list or nauty dependency: the complete eight-vertex coefficient check suffices.

The actual minimum of p6-a8 for those factors is 0.000025987181456670063..., while the minimum of p6-a9 is 0.000025987182439626913.... Nine-vertex averaging really does increase the finite minimum by about 9.8295685e-13. However, the safety margins used in the reported bounds place the stated primary b below the eight-vertex minimum too. R:42 correctly distinguishes eight-vertex products from genuinely nine-vertex products; it should additionally state this simpler proof of its final number.

P:76's phrase “including negative individual residuals” is **FALSE if read as a factual claim that the final frozen primary certificate has any negative eight-vertex residuals**. It has none. As a statement of the lifting checker's ability to handle potentially negative residuals, it is valid. This wording issue does not create a theorem gap.


The independent checker uses bit-coded induced subgraphs, explicit root injections, separately generated disjoint extensions, GMP Gram products and integer cross-multiplication. It imports no submitted verifier, coefficient table or solver output. Source locations: `scripts/reviewer_exact.cpp:35–64` (Gram matrices and flag orbits), `:72–83` (sampling/targets), `:85–92` (complete labelled orbit index), `:96–105` (exact inequalities and deletion averages).

| Frozen artifact | Independent exact minimum slack | Zero-based graph index | Classes |
|---|---|---:|---:|
| c6_8.cert.gz | 420281426482829/420000000000000000000000000 | 11661 | 12346 |
| c6_9.cert | 7564739462625047/7560000000000000000000000000 | 30156 | 274668 |
| c5_8.cert.gz | 560022510134247/560000000000000000000000000 | 9736 | 12346 |

These match P:82–84 and the submitted direct checker's exact integers. See `receipts/reviewer_c6_8.log`, `reviewer_c6_9.log`, `reviewer_c5_8.log`, `reviewer_graph9.log`, `author_c6_8.log`, `author_c6_9.log`, `author_c5_8.log`, and the final `replay_comparison.json`.

All three minimizing graphs have zero monochromatic target cliques. For example the eight-vertex C6 minimizer is `GEznv{`, and a(H) is strictly negative there. Thus the checks do not assume a pointwise nonnegative a(H) or an unavoidable K6 at order eight; positivity is asymptotic after averaging. See `receipts/witnesses.json`.

Uncompressed frozen hashes independently match:

```
c6_9  0137db8ed8648496eddf8f007bcda642ffae9c2e7d93f9b224c4b5c4eec96665
c6_8  bbcc572b177c0f1a5bf5a36f3be7056441f0fe160ad8e7f59b840aaf0ff199ad
c5_8  cc7fa1eb973d9d350b4a0cc01163eb027578497c0d2f3aa12d7deb8e7ffb385a
```

`receipts/archive_check.json` verifies the archive SHA256 `6ec8aa40e3d6fe09155f8c6ffcc18cd8ceddcf8520dd684193e4adf0093e229d` and every manifested hash/byte count. The archive is retained as `sources/submitted_bundle.tar.gz`.

Seven independent certificate controls reject doubled C6 b, doubled square denominator D, duplicate flag classes, interpreting the C5 ordered certificate as unordered, a C5 target above the random-colouring upper bound, a missing eight-vertex class, and a duplicate eight-vertex class. See `receipts/negative_controls.json` and individual logs. Two additional independent completeness controls reject a missing or duplicate nine-vertex class (`receipts/negative_graph9.json`). These test certificate/completeness rejection, not the optimality of the factors or a proof that every rejected b is mathematically false.


I wrote a separate small model builder, `scripts/falsify_small.py`, using all labelled six-vertex graphs generated from scratch and reduced to 156 classes. It builds the conditional-square SDP from explicit sampling, solves with Clarabel, projects/rounds to integer factors, and computes exact rational residuals. The frozen C++ checker then independently verifies the exported certificates. The families are (1,1),(0,3),(2,2),(4,1), at ambient order six; these are smaller instances of the same method, not attempts to reproduce the main eight-vertex optimum. Both unordered and ordered modes are tested.

| Target | Root mode | Exactly certified value | Verdict |
|---|---|---:|---|
| K3 | unordered | 1249999999/5000000000 = 0.2499999998 | PASS |
| K3 | ordered | 499999999/2000000000 = 0.2499999995 | PASS |
| K4 | unordered | 142946827/5000000000 = 0.0285893654 | PASS |
| K4 | ordered | 287507317/10000000000 = 0.0287507317 | PASS |

A separate analytic triangle certificate gives **exactly c3>=1/4**, with zero slack on all four three-vertex classes. Its single (1,1) block has D=2 and three identical rows (1,-1), hence Q=(3/4)[[1,-1],[-1,1]]. Direct sampling gives a(H)=3/4 on a monochromatic triangle and -1/4 on a mixed triangle, so p3(H)-a(H)=1/4 identically. Random colouring supplies the matching upper bound. See `sanity/goodman.cert` and `receipts/falsification_goodman.log`.

The K4 values stay below the published 0.0296 lower benchmark and the simple random-colouring upper bound 1/32. Neither root mode produced an impossible bound. Solver status is not proof: the unordered numerical K3 solve reports `optimal_inaccurate`, while its integer-factor certificate passes exactly. Receipts and certificate files are in `receipts/falsification*.json`, `receipts/falsification*.log`, `sanity/` and `sanity_ordered/`.

One early model-builder prototype incorrectly minimized flags over root permutations that changed the chosen labelled type, causing a missing-flag KeyError. It was fixed before any certificate was accepted, and the failed log is retained. The main independent frozen-certificate checker was unaffected and remained unchanged.


[PPSS, Theorem 1.2](https://arxiv.org/html/2206.04036v3) proves c5>0.001524 using flag algebras, with its exact eight-vertex flagmatic certificate available in the [original Zenodo release](https://zenodo.org/records/6602512). I downloaded the original archive and independently imported its factors, retaining literal original root labels and original column ordering rather than the submitted importer's canonical relabelling. Every reduced Qdash is exactly the identity, so transposing the exact R matrices after multiplication by 2^60 gives integer square factors. Exact replay passes with zero minimum slack at graph 12051 (`receipts/published_baseline_check.log`).

The underlying exact published bound is

```
20421620024978222587630220763104861267
/ 13398618197511951998870375167625873326080
= 0.001524158665015949369131777412356944113054480851847579...
```

The new C89b value improves this by **6.438500506308682225876430558869...e-10**, or **0.00004224298069546%** relative. R:8–12,44,56–59 correctly treats this as microscopic. Comparing only against rounded 0.001524 would substantially exaggerate the gain. The original JSON SHA256 is `239e3aec252b5fe1a104c68a8491b78145dbe1344ff1f04d917b365af5fc7020`; original archive SHA256 is `bc8272b3fbd70b769026eebb0da352184fc9dadfadcb5573772ecfd56cea2cd9`. The independent translated baseline is retained compressed as `sources/ppss_baseline.cert.gz`.

[KPS, section 7](https://arxiv.org/html/2312.08049v1#S7) explicitly describes 0.001557 as suggested by floating-point CSDP output and says it was not converted to exact rational values. It is stronger numerically but is not an established certified lower bound. R:61 handles this correctly. No stronger applicable published exact K5 lower certificate was found in the bounded audit.

| Other new assertion | Exact submitted lines | Verdict | Scope |
|---|---|---|---|
| C6 gain over 0.000021083 is 23.2613074% | R:3–7,38–42 | PASS | Exact rational ratio independently recomputed: 23.26130739932647...%. |
| C5 gain over the full PPSS fraction | R:8–12,56–59 | PASS | Original public factors independently imported and exactly replayed; full difference above. |
| KPS 0.001557 remains uncertified | R:61 | PASS | Confirmed directly in the primary paper, section 7. |
| CSDP/reweighting/dual-pricing discovery history | R:38–46; P:37 | GAP for an independent reproduction of the entire numerical search | I audited relevant source/receipts but did not rerun the original large optimization searches. This history is not a premise of the frozen-square proof. |
| Any exhaustive priority or optimality assertion | P:11; R:3,54,61 | GAP if asserted | The report expressly disclaims it. Fresh bounded searches cannot prove absence of another result. |

`PRIOR_ART.md` records fresh official raw table/PR/issue reads, all 46 open PRs, recently updated public repository searches, all seven required AI/agent repository root inventories, primary papers, recent arXiv and bounded public community searches. The seven repository roots match the submitted closeout inventories. A second complete source fetch at approximately 12:19 UTC again found unchanged relevant raw sources, all 46 PR IDs/titles/head commits, repository searches and rival roots (`receipts/final_source_comparison.json`). #307 concerns a C5 upper bound; #308 is the preceding unrefereed C6 lower certificate. Neither changes the comparison above. No posts, PRs, commits, pushes or messages were made.


All heavy work ran on a rented pod under this own job directory. `REPRODUCE.md` gives the exact setup, tmux launches, dependencies and certificate commands. The independent mathematical check requires C++17 and GMP; the independent nine-vertex completeness replay additionally needs pynauty, and the falsification searches use NumPy/CVXPY/Clarabel. The primary C6 and C5 theorems can both be checked at order eight without nauty or an SDP solver.

All submitted direct, legacy-GMP and deletion-based replays finished successfully. `receipts/replay_comparison.json` confirms exact agreement of all three independent/replay routes for each final artifact. Heavy runs used nice 10, single-threaded BLAS and a 38000000-KiB virtual-memory limit; final runs shared a ten-CPU affinity, and final numerical falsification runs explicitly limited Clarabel to one thread. The recorded aggregate RSS peak was **943356 KiB**, below 1 GiB; the maximum recorded child RSS was 618496 KiB. See `receipts/resource_summary.json`, per-run resource records and `affinity_limits.json`.

Scientific checks and temporary cleanup finished at **2026-11-02 12:24:55 UTC**. The final process audit at **12:25:40 UTC** found no own scientific workers and no own tmux sessions. The lightweight monitor also exited. `receipts/worker_cleanup_final.json`, `pod_ps_final.txt` and `local_ps_final.txt` retain the audits. The pod remains running; no other job was modified. Only temporary files created by this review session were removed, after retaining hashes, the translated PPSS baseline, the frozen submitted archive and replay receipts. Retained pod artifacts total 28522740 bytes excluding the Python dependency environment; local retained files remain below 50 MB. This review completed in about 22 minutes, well within three hours and before the declared 18:05 UTC pod cutoff. No commits, pushes, PRs, posts or external messages were made.

Recommended correction: explicitly mention the eight-vertex proof of the final primary C6 number and change P:76 to “allowing potentially negative individual residuals.” Retain the full PPSS fraction in every C5 comparison. No change to the claimed numerical lower bounds is needed.

**Overall verdict: PASS for both frozen lower bounds. My subjective probability that C89c >= 0.000025987181439 is correct is 99.5%; likewise 99.5% for C89b >= 0.001524159308866.** These probabilities concern the normalized mathematical inequalities, not priority, optimality or full reproduction of the numerical search history.

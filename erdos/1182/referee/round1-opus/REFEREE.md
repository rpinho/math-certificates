# Referee report: F(n) ≤ 5n−1 for every n ≥ 550,000 (Erdős #1182)

This is a separate AI referee (Claude Opus 5.5) of a proof written by a different model (gpt-6.2-sol). Clean room: I read only `../e1182kempe/{PROOF,LEMMAS,REPORT,PRIOR_ART,STATUS}.md` and used the certificate `.json.gz` files as data. I did not read, run or copy any producer `*.py` or `*.log`, or anything in `../e1182replay`. All code under `code/` is mine.

**Summary.**
- **The written proof has a real error in Case I.** The occupancy inequality at LEMMAS.md:52 points the wrong way. All 311 occupancy leaves of `cert_case1.json.gz` depend on it, so that certificate does not prove Case I.
- **The error does not make the theorem false.** Numerically, the true Case I rate is about −0.015 at its maximum.
- **I repaired it.** I built a replacement Case I certificate myself and checked it in Arb: 1,223 leaves, maximum −0.0010209.
- **Everything else holds.** I checked the reduction, the Kempe dichotomy, the naive A/B and Case II certificates, the finite sum and the connectivity bound.
- **So the theorem holds, but only with my replacement for Case I.** That replacement has had no second check yet.

---

## (a) Definition and reduction — PASS

**Definition.** I fetched erdosproblems.com/1182 on 2026-11-25 (`web/ep1182.html`; the page says "last edited 11 April 2026"). It says: "Let F(n) be maximal such that every connected graph G with n vertices and ≤ F(n) edges has R(K_3,G) = 2n−1". Kataria's note at `Sovi11/erdos-1182@6d4f78c`, `preprint/main.tex` line 20, uses the same definition: "the largest q such that every connected graph with n vertices and at most q edges is good". So a connected n-vertex graph G with R(K_3,G) > 2n−1 gives F(n) ≤ e(G)−1. The definition is "at most q edges", so monotonicity is not an issue.

**Reduction** (PROOF.md:7-11). I re-derived each step.
- **The red graph.** H_n = C_5[k_0..k_4] with k_i ∈ {h, h+1}, where Σk_i = 2n−1. It is triangle-free. The blue graph is its complement: part-index differences {0, 2, 3}, with each part a blue clique.
- **Embeddings and maps.** An embedding of G into the blue graph is the same as a map f: V → Z_5 with |f⁻¹(i)| ≤ k_i and every edge on a blue part pair. One direction restricts the embedding; the other injects each class into its part.
- **Multigraph to simple graph.** M has a valid map exactly when its simplification G does. Loops sit at difference 0, which is blue, and parallel edges repeat the same constraint.
- **Connectivity and odd n.** Simplification preserves connectivity, and e(G) ≤ 5n. D = 10n is even for every n, so odd n needs no pendant-vertex trick (Kataria needed one at main.tex:145).
- **No simplicity step is needed.** The argument only needs one pairing M that is connected and has no valid map. Its simplification is then a simple connected graph with ≤ 5n edges and R(K_3,G) > 2n−1, so F(n) ≤ 5n−1.

**Cap.** max a_i ≤ (h+1)/n ≤ (2n+3)/(5n) = 2/5 + 3/(5n). At n_0 this is 0.4000 ≤ 4001/10000 (`out/finite_check.log`).

**Connectivity** (PROOF.md:36), re-derived.
- A disconnected M has a closed set of k ≤ n/2 vertices.
- Revealing that set's stubs one at a time, the next stub's mate lands inside the set with probability (10k−2j−1)/(10n−2j−1) ≤ k/n. This uses k ≤ n.
- So for a fixed set, P(closed) ≤ (k/n)^{5k}, and C(n,k)(k/n)^{5k} ≤ (e(k/n)^4)^k ≤ (e/16)^k.
- Summing over k gives at most e/(16−e) = 0.20466 < 3/13 (`out/finite_check.log`, Arb).

**Symmetry and regions** (PROOF.md:15).
- The ten dihedral maps preserve the blue graph and permute the capacities within {h, h+1}.
- Region A: the top pair is red-adjacent, normalized to a_0 ≥ a_1 ≥ max(a_2,a_3,a_4).
- Regions B and C: the top pair is blue-adjacent and moved to {0,2}. The reflection i ↦ 2−i = (0 2)(3 4) then makes a_3 ≥ a_4. So in B and C, a_0, a_2 ≥ a_1, a_3, a_4.
- The boundary at δ = 3/20 is closed on both sides.
- I use exactly these inequalities in my verifier (`code/arbverify.py` `region_parts`).

**Potential-minimal maps.** If any valid map exists, a Φ-minimizer exists, and it satisfies every necessary condition below in its normalized orientation. The capacities are only used through "v_j ≤ h−1 ⇒ a move into j fits", which holds under any capacity vector in {h, h+1}⁵. So the count E X_rigid may drop capacities except a_i ≤ 4001/10000, which the trees use.

## (b) Kempe-swap dichotomy — PASS

**Statement** (PROOF.md:21-25). Take n ≥ 14, a Φ-minimal valid map in Region C (v_0 − v_3 ≥ δn, v_2 − v_3 ≥ δn, a_3 ≥ a_4, so v_2 − v_4 ≥ δn ≥ 2), and d = 10. Then:
- every u ∈ V_0 has n_2(u) ≥ 1, and every v ∈ V_2 has n_0(v) ≥ 1; and
- with Z_0 = {u ∈ V_0 : n_3(u) = 0} and G_2 = {v ∈ V_2 : n_4(v) = 0}, either
  - **Case I:** |Z_0| ≤ 2d−1 = 19, or
  - **Case II:** every u ∈ V_0 has an M-neighbour in V_2 \ G_2.

**Step-by-step check.**
1. **One-vertex moves.** A vertex in V_0 has neighbours only in parts {0,2,3}. Part 3's blue parts are {3,0,1}, so the move 0→3 is valid iff n_2 = 0. Likewise a vertex in V_2 has neighbours in {0,2,4}, part 4's blue parts are {4,1,2}, so 2→4 is valid iff n_0 = 0. A move i→j changes Φ by 2(v_j − v_i + 1) ≤ −2 when v_i ≥ v_j + 2, and then v_j + 1 ≤ h ≤ k_j. Loops move with their vertex (3–3 and 4–4 are blue). **PASS.**
2. **Donor count.** u has ≥ r stubs into V_2, so it has at most d−r neighbours in Z_0 \ {u}. Then |Z_0 \ (N(u) ∪ {u})| ≥ 2d − (d−r) − 1 = d + r − 1 ≥ r − 1. **PASS.**
3. **Net transfer.** u: 0→3, r vertices 2→0, r−1 donors 0→2. Net change per part: (0, 0, −1, +1, 0), i.e. one vertex from 2 to 3. With v_2 ≥ v_3 + 2 this strictly decreases Φ and fits the capacities. **PASS.**
4. **Edge validity.**
   - u, now in 3: its V_2-neighbours have all moved to 0 (3–0 blue). Its V_0-neighbours stay in 0, since no donor is adjacent to u. Its V_3-neighbours stay in 3.
   - Each v_j, now in 0: it had n_4 = 0, so its neighbours were in {0,2}. They are now in {0 (stayed or moved v_j), 2 (donors or stayed), 3 (u)}, all blue from 0.
   - Each donor, now in 2: it had n_3 = 0, so its neighbours were in {0,2}, and it is not adjacent to u. They are now in {0, 2}, all blue from 2.
   - Edges inside moved classes and loops are covered by the same lists. **PASS.**
5. **Conclusion.** No u with all its V_2-neighbours in G_2 can exist when |Z_0| ≥ 20. The case r = 0 is excluded by step 1. **PASS.**

**Simulation** (`code/kempe_sim.py`, 4 seeds × 1,500; `out/kempe_total.json`).
- **Instances.** Random 10-regular configurations (loops allowed) with n = 40–160, all stub pairs blue for a planted Region-C-like map (v_0, v_2 ≥ v_3 + 2, v_2 ≥ v_4 + 2). I added a random per-vertex restriction on which parts each vertex may touch, so the swap hypothesis comes up often.
- **Results.** 5,996 instances, with 88,827 loops in total.
  - One-vertex moves: 100,673 (0→3) and 102,090 (2→4), 0 invalid.
  - Swaps: 83,966 performed, 0 invalid, 0 with a wrong profile change, 0 without a strict Φ decrease.
  - Donor count: 107,819 cases had |Z_0| ≥ 20 with r ≥ 1, and 0 of them were short of donors.
- **Mutants.**
  - Donor adjacent to u: 70,104 swaps, all invalid. Example: u = 0, donor 27, bad edge {27, 0} on parts (2, 3).
  - A v_j with a 4-neighbour: 57,224, all invalid.
  - A donor with a V_3-neighbour: 65,349, all invalid.

## (c) First-moment rates — Naive and Case II PASS; Case I FALSE as written (repairable)

**Re-derived** (each by hand, then used in my own code):
- **Pairing count and Stirling bound** (LEMMAS.md:7-22). I get Pr(K|f) = 2^{D/2}(D/2)!/D! · ΠS_i! / (Π2^{K_ii/2}(K_ii/2)! Π_{i<j}K_ij!) and the bound multinomial·p_K ≤ 3^6(D+1)^3 e^{nL}, with L(a,Q) = 9Σa log a − 5Σ_{ij}Q log Q. This matches Kataria's Ψ_d (main.tex:103-110) after substituting x_ii = dQ_ii/2 and x_ij = dQ_ij. My rigorous lower bound for the naive rate at a = (2/5, 138839/10⁹, 2/5, 18711729/10⁸, 12743871/10⁹) is +0.0033635269515, matching Kataria's +0.0033635 (`out/controls.log`).
- **Type count.** (D+1)^5 types per profile, (n+1)^4 profiles (LEMMAS.md:24).
- **Tilt identity and convexity.** L = U_t(a) − 5·KL(Q‖B) (LEMMAS.md:30-31), and U_t is convex in a.
- **Binary edge tail.** KL ≥ 𝒟(2Q_ij, 2B_ij), with 𝒟 monotone on each side of b (LEMMAS.md:35-39).
- **Convex-vertex argument.** A box cut by the mass hyperplane has its vertices among points with at least 4 coordinates at an endpoint (LEMMAS.md:93). My code enumerates that superset.
- **Case I occupancy bound** Pr(E_I|K) ≤ (D+1)n^19 20^19 exp(n a_0 log f(Q_03/a_0)), f(p) = 1−(1−p)^10 (LEMMAS.md:45-50). Each step checks out: the binomial-mode comparison P(mode) ≥ 1/(N+1), the union over C(v_0,19) ≤ n^19 sets, and p ≥ 1/20 ⇒ f^{−19} ≤ 20^19.
- **Monotonicity of a·log f(q/a).** It decreases in a: its derivative is log f(x) − x f′(x)/f(x) ≤ 0, which increases to 0 at x = 1.
- **Case II.**
  - Received hot slots form a uniform R-subset of the dv_0 row-0 slots (LEMMAS.md:64).
  - P(all of V_0 hit) ≤ (D+1) f(R/dv_0)^{v_0}.
  - Tangent bound: log f(x) ≤ γ + βx.
  - Moment bound: E w^R ≤ (1 + (K_20/S)(w−1))^m with m ≤ 9K_24 (LEMMAS.md:78).
  - Near-cell bound: a_min·γ + 90·h_24·log(1 + p_max(e^{β/10} − 1)) with upper cutoffs on Q_02 and Q_24 (LEMMAS.md:80-87).
  - The direction is correct: the moment factor increases in Q_02 and Q_24, and the far cells sit above B.
- **Normalization.** a_3 ≥ a_4; a_0, a_2 unordered; orientation toward part 3 (PROOF.md:15).

**Read only, not re-derived:** the exact Case II row-2 law P_{V_2} (LEMMAS.md:57-62), which the certified bound does not use; and the whole-row fixed-tilt discussion (LEMMAS.md:95), which is diagnostic.

**ERROR — LEMMAS.md:52.**
- **The text.** "If positive types have Q_03 ≥ q_*, the last rate is at most a_min log f(min(1, q_*/a_min))".
- **Why it's false.** f increases, so a_0 log f(Q_03/a_0) *increases* with Q_03. A lower bound Q_03 ≥ q_* gives a lower bound on the occupancy rate, not an upper bound. The valid statement needs Q_03 ≤ q_*, with the tail cell Q_03 > q_* ≥ B_03.
- **The certificate uses the wrong version.** In `cert_case1.json.gz`, all 311 occupancy ("C") leaves have q_* < B_03 (`out/controls.log` item 4). So each leaf covers Q_03 < q_* with the binary-KL tail and applies the false bound on Q_03 ≥ q_*.
- **Concrete violation** (`out/case1_direction_counterexample.txt`). In the first C leaf (DFS order), take the vertex a = (0.37815, 0.034175, 0.4001, 0.12505, 0.062525) and the max-entropy type with Q_03 = 0.07167 ≥ q_* = 0.05567. The true occupancy rate there is −0.04932. The claimed bound is −0.08601, which is exceeded by 0.0367.
- **The theorem itself is not contradicted.** The true Case I rate max_Q [L + a_0 log f(Q_03/a_0)] is about −0.0152 at its numerical maximum, near a = (0.4001, 0.0001, 0.4001, 0.19, 0.01). This is non-rigorous (`code/rates_numeric.py`, `code/rc_search.py`): 24 local searches, plus the 311 leaf centroids, whose maximum is −0.0255.

**Repair (mine).** For any t > 0 and s > 0, put weight s on the 03 cell: B_{t,s} ∝ A_ij t_i t_j s^{[ij∈{03,30}]}. Then for every feasible Q:

> L(a,Q) = V_{t,s}(a) − 10·Q_03·log s − 5·KL(Q‖B_{t,s}),  V_{t,s} = 9Σa log a − 10Σa log t + 5 log Z_s.

Split Q_03 ∈ [0, min(max a_0, max a_3)] into 64 intervals [q_k, q_{k+1}]. On each, the Case I rate is at most max_vertices V − 10·log s·(q_k if s ≥ 1, else q_{k+1}) + a_0min·log f(min(1, q_{k+1}/a_0min)). The 64 intervals cover all types, with the same Pr(E_I|K) prefactor as the producer's, so the finite sum in (e) is unchanged.

## (d) Certificates — naive A/B PASS, Case II PASS, Case I REJECTED (replaced)

**My verifier** (`code/arbverify.py`). It is python-flint 0.9.0 Arb at 160 bits, written from (c).
- **Coverage.** It rebuilds each tree from the exact root [0, 4001/10000]⁵ (grid 10485760000 = 2²⁰·10⁴; δ = 1572864000/grid exactly). It requires each split point to be strictly interior and rejects truncated or trailing records.
- **Region tightening.** Boxes are tightened by interval propagation of the region inequalities and the mass constraint. B is handled as the union of {a_0 ≤ a_3 + δ} and {a_2 ≤ a_3 + δ}. Every polytope vertex is enumerated exactly. U, 𝒟, γ, β and the occupancy terms are evaluated in Arb, and each leaf requires the upper endpoint ≤ the lower endpoint of −1/1000.
- **What it does not take from the producer.** Only split coordinates, tilts and cutoffs come from the certificate. Stored values are only compared.
- **Bug I fixed in my own verifier.** It first tested whether a Case II tail cell is empty using max over vertices of the concave min(a_0,a_2), which is unsound. I replaced it with min(max a_0, max a_2). Case II still passes.

| Tree | Result | Leaves | My max leaf bound | Reported (REPORT.md:10-12) |
|---|---|---:|---:|---:|
| naive A/B | ACCEPT (34 empty X leaves confirmed empty) | 805 | −0.00117883621834 | −0.0011788362183 |
| Case II | ACCEPT | 1,978 (1,504 naive + 474 occupancy) | −0.00100000102061 | −0.0010000010000 |
| Case I, producer | **REJECT**: tail on the wrong side of B_03 in all 311 C leaves; the 351 naive leaves pass (max −0.0013548) | 662 | — | −0.0010000010001 (not a valid bound) |
| Case I, referee repair (`out/cert_case1_referee.json`, sha256 `ed752ead3d9b…845d`) | ACCEPT | 1,223 | −0.00102091368896 | — |

My leaf U values match the stored ones to 2.1e−11 in the Case I and Case II trees. In the naive tree they differ by up to 0.49 on some leaves, because my B split is tighter than the producer's coordinate hull. Commands: `out/verify_*.txt` and `out/check_case1_referee.txt`. Runtime is under 1 s per tree, peak RSS 33 MB.

**Controls** (`code/controls.py`, `out/controls.log`).
- **Positive witness.** The naive witness is rigorously positive: L ≥ +0.0033635269515 at a point in Region C. A naive-leaf check on a box around it, with the optimal tilt, is REJECTED (leaf bound +0.0033648).
- **Producer certificate corruptions, all REJECTED (11):**
  - naive A/B: tightest leaf's tilt set to uniform; tightest leaf's tilt perturbed by 2% (bound +0.0031); truncated; trailing record; split point at the box edge; an N leaf replaced by X;
  - Case II: tilt set to uniform; h_02 halved (falls below 2B_02); h_24 tripled; u → 1−10⁻¹²; truncated.
- **Referee-certificate corruptions, all REJECTED (5):** s → 1 on the tightest leaf (bound +0.0139), uniform tilt, M = 1, truncated, trailing.
- **Producer's Case I tree:** REJECTED, as in the table.

The first version of my controls corrupted the first leaf rather than the tightest one, and two corruptions passed because those leaves have slack. I changed the controls to target the tightest leaf; the log above is from that rerun.

## (e) Finite part — PASS (with the Case I repair)

**Re-derivation.**
- E X_rigid ≤ Σ over 10 orientations × 3 terms × (n+1)^4 profiles × (D+1)^5 types of 3^6(D+1)^3 e^{nL} × extra.
- The extra factor is at most (D+1)n^19 20^19 for Case I, at most (D+1) for Case II (all R are summed inside the moment bound, LEMMAS.md:82-85), and 1 for the naive term. Using (D+1)^2 n^19 20^19 uniformly, as LEMMAS.md:99 does, is conservative.
- With every rate ≤ −1/1000, E X_rigid ≤ 30·3^6·(n+1)^4·(10n+1)^10·n^19·20^19·e^{−n/1000}. This matches PROOF.md:34.
- My Case I repair uses the same per-type prefactor and has no tail cells, so the formula is unchanged.

**Numbers** (`code/finite_check.py`, Arb).
- At n_0 = 550,000 the bound is 4.2602e−11 (< 4.261e−11).
- d/dn log bound = 4/(n+1) + 100/(10n+1) + 19/n − 1/1000 = −0.00094 at n_0, and it stays negative for n > 33,000.
- Side conditions at n_0: cap 0.4000 ≤ 0.4001; δn_0 = 82,500 ≥ 2; v_0 ≥ 0.15n ≥ 2b = 38.
- Total: P(X_rigid > 0) + P(disconnected) ≤ 4.3e−11 + 0.2047 < 1 for every n ≥ n_0.
- For information: the same bound is already below 1 from n = 524,803.

## (f) Prior art — no bound below 5.025n found before 2026-11-25

**What I searched,** all with curl, read-only (WebFetch was denied in this session; files are in `web/`):
- erdosproblems.com/1182: the page still lists 17n/15 ≤ F(n) ≤ 84n (Brandt).
- The forum thread /forum/thread/1182: 4 comments. The newest is pravarkataria's, 2026-09-28; the others are from March 2026.
- /forum/thread/1182/proof-claims: 2 claims.
  - Kataria, 2026-09-29: 11n/2 and 5.03n.
  - Qiyuan Gu, 2026-09-10: about f(n) = Θ(n^{3/2}√log n), not about the constant in F(n).
- GitHub API for Sovi11/erdos-1182: the latest commit is still 6d4f78cf (2026-11-13), and there are 0 issues or PRs (the `issues?state=all` call returned `[]`).
- BOUNDS.md@6d4f78c line 114: "10-regular plus 0.025n independent random edges … 5.025n" is the best stated there. main.tex:132 says bare d = 10 "fails: max Ψ_10 ≈ +0.003".
- arXiv API:
  - `all:"triangle-good"`: 0 hits.
  - `abs:"Ramsey goodness" AND abs:triangle`: 1 hit, a 2025 odd-cycles paper, not F(n).
  - `"K_3-good" OR "triangle goodness" OR (Erdos AND 1182)`: 0 hits.

**Not searched:** X/social media, a general GitHub code search, Brandt's paper, and Nikiforov–Rousseau Theorem 5.1 (I did not check the producer's "50n−1" reading of it).

**Novelty: yes.** Under the same definition, 5n−1 is below the best public bound I found (Kataria, 5.025n unrefereed; 84n on the official page), as of 2026-11-25. This is conditional on the Case I repair.

---

**CONTROLS:** Yes, but in the producer's work, not mine. The producer's controls (REPORT.md:22: "All 2,880 Case I joint Chernoff inequalities … held") did not test the inequality the leaves actually rely on. My own check found the direction error: `out/verify_case1.txt` REJECT, and 311/311 leaves with q_* < B_03 (`out/controls.log` item 4). In my own work, no assumption overrode a control. Every corruption I made was rejected, and the positive witness was found (`out/controls.log`).

**CONTRADICTING:** No. I kept the data that cut against my conclusion: the producer's Case I rejection, the two corruption controls that first passed (rerun on the tightest leaves), and my own verifier bug (concave min; fixed, Case II still accepts). The non-rigorous true Case I maximum (−0.0152) is reported, not used as proof.

**LABELS:** No. The certificate's record labels ("N", "C", cutoff meaning, scales) were inferred from the data and then checked against raw values. q_* is in grid units: q_*/grid = 0.0557 and B_03 = 0.0720 from the leaf's own tilt. The stored U agrees with my recomputation to 2.1e−11. h_02 and h_24 are in grid units and u in tilt units; with this reading, the Case II leaves pass my independent bound.

**Caveats and failures:**
1. **FAILURE in the written proof:** LEMMAS.md:52, the Case I occupancy bound with the wrong cutoff direction. Everything that rests on it fails too:
   - `cert_case1.json.gz`, all 311 "C" leaves;
   - PROOF.md:29 ("verify a rate upper bound of −1/1000 … for each case in C");
   - LEMMAS.md:93 (the "accepted occupancy leaf" check for Case I);
   - REPORT.md:1 and REPORT.md:11 (the Case I row, −0.0010000010001).
2. **The theorem holds only through the referee-built Case I certificate** (`out/cert_case1_referee.json`, `code/case1_repair.py`, derivation in (c)). I produced it and checked it myself, so it needs a second check before any public claim. The producer should replace LEMMAS.md §3 lines 51-52 and `cert_case1.json.gz`.
3. REPORT.md:22: the producer's Case I controls did not exercise the leaf inequality, so their "passed" says nothing about Case I.
4. Prior art: X and social media were not searched, and Nikiforov–Rousseau (PRIOR_ART.md "50n−1") was not checked by me.

VERDICT: HOLDS WITH CAVEATS

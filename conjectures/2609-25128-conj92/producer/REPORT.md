Shipped: Complete, elementary, unconditional proof of Ma, Sahbi & Zhang (`arXiv:2609.25128v4`) Conjecture 9.2 ($\psi_{sq}(G) + \psi_{sq}(\overline{G}) \le n + 2$ for every finite simple graph $G$ of order $n \ge 2$) in `PROOF.md`, computationally verified across all 288,265 unlabeled graphs of orders $2 \le n \le 9$ and 53,470 random/structured/adversarial graphs up to $n = 20$.

- **RESULT:** `yes` (Conjecture 9.2 settled affirmatively via Path B).
- **Did we find something new?** **Yes.** Conjecture 9.2 (`\label{conj:ng-upper}`) is explicitly stated as an open problem in Section 9 and the Conclusion of Ma, Sahbi & Zhang (`arXiv:2609.25128v4`, manuscript lines 862–867 and 882). We prove $\psi_{sq}(G) + \psi_{sq}(\overline{G}) \le n + 2$ unconditionally for every finite simple undirected graph $G$ of order $n \ge 2$ (and $n = 1$).
- **Why no statistical holdout / SBS baseline applies:** This task settles a universal deterministic inequality over all finite simple graphs rather than estimating a statistical or predictive score. Per the rules for exact certificate/theorem tasks, validation uses a separately written zero-dependency rational-arithmetic verifier ([verify_proof.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/verify_proof.py)) with 5 explicit negative/mutant controls, an independent C++ exact census and lemma auditor ([src/verify_all.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/src/verify_all.cpp)), and a line-by-line adversarial referee audit against the source manuscript.

---

## Proof Summary (Full Proof in [PROOF.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/PROOF.md))

Let $f_1 : V \dashrightarrow \{1, \dots, k_1\}$ and $f_2 : V \dashrightarrow \{1, \dots, k_2\}$ be optimal sub-quorum colorings of $G$ and $\overline{G}$ with colored supports $S_1, S_2 \subseteq V$, and put $I = S_1 \cap S_2$ with $m = |I|$.

1. **Exact reciprocal class-size weights (Lemma 1):** Assigning $w_{f}(v) = 1/|C_{f(v)}|$ for $v \in S$ and $0$ outside $S$ gives the exact identity $k_1 + k_2 = \sum_{v \in V} \bigl(w_{f_1}(v) + w_{f_2}(v)\bigr)$ without requiring connected color classes or discarding vertices beyond a matching edge.
2. **Outside $I$:** Every $v \in V \setminus I$ misses $S_1$ or $S_2$, so $w_{f_1}(v) + w_{f_2}(v) \le 1$, contributing at most $n - m$.
3. **Inside $I$ (Lemmas 1(2), 2, and 3):** For $v \in I$ with degree $d_I(v) = |N_G(v) \cap I|$ in $H = G[I]$ and $(m - 1) - d_I(v)$ in $\overline{G}[I]$, the sub-quorum majority rule forces $|C_{f_1(v)}| \ge 1 + \lfloor d_I(v)/2 \rfloor$ and $|C_{f_2(v)}| \ge 1 + \lfloor (m - 1 - d_I(v))/2 \rfloor$. Using $\frac{1}{a} + \frac{1}{b} \le 1 + \frac{1}{a + b - 1}$ (from $(a-1)(b-1) \ge 0$, Lemma 2):
   - If $m = 0$ or $m = 1$, $\Sigma(H) \le m + 1$.
   - If $m = 2r$ is even ($r \ge 1$), every vertex satisfies $a(v) + b(v) = r + 1$, so $\Sigma(H) \le 2r(1 + 1/r) = m + 2$.
   - If $m = 2r + 1$ is odd ($r \ge 1$), odd-degree vertices satisfy $a(v) + b(v) = r + 1$ while even-degree vertices satisfy $a(v) + b(v) = r + 2$. By the handshaking lemma in $H = G[I]$, at least one vertex of $I$ has even degree, giving
     $$\Sigma(H) \le 2r\left(1 + \frac{1}{r}\right) + \left(1 + \frac{1}{r + 1}\right) = m + 2 + \frac{1}{r + 1} \le m + \frac{5}{2}.$$
4. **Integrality (Theorem 1):** Combining both regions gives $k_1 + k_2 \le (n - m) + (m + \frac{5}{2}) = n + \frac{5}{2}$. Because $k_1 + k_2 \in \mathbb{Z}$, $\psi_{sq}(G) + \psi_{sq}(\overline{G}) \le \lfloor n + \frac{5}{2} \rfloor = n + 2$.

---

## Computational Census, Gap Analysis, and Verification Status

### 1. Exhaustive Unlabeled Census ($2 \le n \le 9$, [results/census_n2_to_9.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/results/census_n2_to_9.json))

All `288,265` canonical unlabeled graphs of orders $2 \le n \le 9$ (verified against exact OEIS A000088 counts) were evaluated, verifying Definition 2.2 on every witness coloring and checking Lemmas 1–3 and Theorem 1 in exact integer-scaled rational arithmetic (`QSCALE = lcm(1..20) = 232,792,560`):

| $n$ | Unlabeled graphs | $\max(\psi_{sq}(G)+\psi_{sq}(\overline{G}))$ | $n+2$ | $\min$ sum | Equality ($=n+2$) count | Equality with strict gap ($\psi_{sq}>\beta_2$) | Graphs with $\psi_{sq}(G)>\beta_2(G)$ | $\max(\psi_{sq}-\beta_2)$ | Counterexamples |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 2 | 4 | 4 | 4 | 2 | 0 | 0 | 0 | 0 |
| 3 | 4 | 5 | 5 | 5 | 4 | 0 | 0 | 0 | 0 |
| 4 | 11 | 6 | 6 | 6 | 11 | 0 | 0 | 0 | 0 |
| 5 | 34 | 7 | 7 | 6 | 32 | 0 | 0 | 0 | 0 |
| 6 | 156 | 8 | 8 | 7 | 122 | 2 | 1 | 1 | 0 |
| 7 | 1,044 | 9 | 9 | 7 | 538 | 26 | 13 | 1 | 0 |
| 8 | 12,346 | 10 | 10 | 7 | 3,036 | 264 | 263 | 1 | 0 |
| 9 | 274,668 | 11 | 11 | 8 | 21,354 | 2,450 | 7,160 | 1 | 0 |

- **$\psi_{sq}(G) - \beta_2(G)$ gap structure:** $\psi_{sq}(G) = \beta_2(G)$ for all graphs on $n \le 5$. At $n = 6$, the unique unlabeled graph with $\psi_{sq}(G) > \beta_2(G)$ is the double star $S_{2,2}$ ($\psi_{sq} = 5, \beta_2 = 4$), which together with $\overline{S_{2,2}}$ ($\psi_{sq} = \beta_2 = 3$) attains $5 + 3 = 8 = n + 2$ and hits Lemma 3's bound $\Sigma(P_3) = \frac{11}{2} = m + \frac{5}{2}$ with exact equality at $m = 3$. Larger gaps $\psi_{sq}(G) - \beta_2(G) = k$ occur on $k$ disjoint copies of $S_{2,2}$ ($n = 6k$, verified for $k = 2, 3$ in `multi_S22_high_gap` and `sa_tabu_adversarial`), where $\psi_{sq}(k S_{2,2}) = 5k$, $\beta_2(k S_{2,2}) = 4k$, and $\psi_{sq}(\overline{k S_{2,2}}) = 3$ ($k \ge 2$), giving sum $5k + 3 < 6k + 2$.
- **All 4 cases of Lemma 3 exercised on census optima:** Case A ($m=0$): `318`; Case B ($m=1$): `35,474`; Case C (even $m \ge 2$): `241,352`; Case D (odd $m \ge 3$): `11,121`.

### 2. Structured, Random, and Adversarial SA/Tabu Suite ($6 \le n \le 20$, [results/verification_60k.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/results/verification_60k.json))

Across `53,470` additional graphs (`341,735` total graphs combined with the census, completed in `53.79s` on 4 threads at `nice -n 10`), zero counterexamples and zero lemma violations occurred:
- `sa_tabu_adversarial` (`24,435` evaluated states across $10 \le n \le 20$, maximizing $1000(\psi_{sq}(G)+\psi_{sq}(\overline{G})-n-2) + 20(\psi_{sq}(G)-\beta_2(G)+\psi_{sq}(\overline{G})-\beta_2(\overline{G}))$): max excess `0` (`5,308` equality hits, max gap `3`).
- `erdos_renyi_random` (`12,540` graphs, $6 \le n \le 18$) + `erdos_renyi_n19_20` (`300` graphs, $n = 19, 20$): max excess `0`.
- `split_graphs` (`4,180`), `threshold_cographs` (`4,180` random threshold graphs — `4,180/4,180` hit equality $n + 2$), `trees_and_complements` (`4,180`), `blowups_C5_S22` (`2,090` $C_5$ blowups), `self_complementary` (`1,560` across $n \in \{8,9,12,13,16,17,20\}$), `paley_ramsey` (`3`: Paley-13, Paley-17, cubic-residue Ramsey-$(3,5)$ circulant on $n=13$), `multi_S22_high_gap` (`2`): max excess `0` across all families.
- **Lemma 3 cases exercised in random/adversarial suite:** Case A: `133`; Case B: `3,965`; Case C: `42,122`; Case D: `7,250`.

### 3. Failed Analytical Attempt & Runtime Deviation Documented
- **Failed analytical route (Lemma 2.4 / $\Omega$):** Trying to bound $\psi_{sq}(G) + \psi_{sq}(\overline{G})$ via the paper's representative-pair bound $\Omega(G)$ fails at $n = 6$: $\Omega(K_6) + \Omega(\overline{K_6}) = 3 + 6 = 9 = n + 3 > n + 2$ ([verify_proof.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/verify_proof.py#L265-L268)). Retaining exact class-size reciprocals $1/|C_{f(v)}|$ in Lemma 1 resolved this failure.
- **Solver runtime deviation:** Our first search binary ([src/run_searches.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/src/run_searches.cpp)) completed the $n \le 9$ census in `3.55s` ([results/archive/census_n2_to_9.attempt1.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/results/archive/census_n2_to_9.attempt1.json)) but exceeded `120s` on dense $n = 19, 20$ complements before adding exact integer `INV_TABLE` reciprocal-degree pruning in [src/verify_all.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/src/verify_all.cpp#L20-L28).

---

## Referee Verdict Checks (`CONTROLS`, `CONTRADICTING`, `LABELS`)

- **`CONTROLS:` No — no assumption overrode what the controls show.**
  - Checked 12 published benchmark controls in [PRIOR_ART.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/PRIOR_ART.md#L44-L59) ($K_4, K_5, \overline{K_5}, P_4, C_5, K_{1,4}, S_{2,2}, K_3 \circ K_1, Q_3, G_{3,3}$, Petersen, $G_{3,4}$): `12/12` exact matches.
  - Checked [src/subquorum_engine.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/src/subquorum_engine.cpp#L454-L484) (`./build/subquorum_engine --self-test`) and [src/verify_all.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/src/verify_all.cpp#L523-L526): `1,251/1,251` unlabeled graphs ($2 \le n \le 7$) and their complements match unpruned `brute_force_psi_sq` (which does not assume connected color classes or `w_ub` pruning), plus `252/252` subcubic graphs against Theorem 3.3.
  - Checked `python3 verify_proof.py` ([verify_proof.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/verify_proof.py#L253-L283)): `5/5` negative/mutant controls confirmed load-bearing hypotheses (`K_3` 3-singleton coloring rejected; tightened bound $n+1$ falsified on $K_4$ and $S_{2,2}$; $\Omega(K_6)+\Omega(\overline{K_6}) = 9 > 8$ falsified; non-graphical degree sequence `[1,1,1]` at $m=3$ gives $\Sigma = 6 > 11/2$ when handshaking is dropped; non-onto coloring `[1,3]` rejected).
- **`CONTRADICTING:` No — zero contradicting graphs or runs were dropped or ignored.**
  - Checked [results/census_n2_to_9.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/results/census_n2_to_9.json#L3-L15): all `288,265` OEIS-verified unlabeled graphs ($2 \le n \le 9$) accounted for (`318 + 35,474 + 241,352 + 11,121 = 288,265`), matching the pre-pruning run in [results/archive/census_n2_to_9.attempt1.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/results/archive/census_n2_to_9.attempt1.json#L3-L10) on every order (`0` counterexamples).
  - Checked [results/verification_60k.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/results/verification_60k.json#L2-L19): all `53,470` random/structured/SA-Tabu evaluations accounted for (`133 + 3,965 + 42,122 + 7,250 = 53,470`, `0` counterexamples).
- **`LABELS:` No — every manuscript citation, theorem number, and JSON bucket label was checked directly against raw bytes and generator code.**
  - Checked raw `inputs/2609.25128v4.tex.json.gz` (`64,804` TeX bytes): verified Definition 2.2 (lines 69–75), Lemma 2.4 (`\label{lem:omega}`, line 89), Theorem 7.4 (line 549), Remark 7.5 (line 602), Theorem 8.2 (line 648), and Conjecture 9.2 (`\label{conj:ng-upper}`, lines 862–867), correcting three off-by-one section citations in [PRIOR_ART.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/PRIOR_ART.md#L31-L56).
  - Checked [results/verification_60k.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/results/verification_60k.json#L2-L19) against [src/verify_all.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subquorum/src/verify_all.cpp#L689-L725): verified the exact count inside `verification_60k.json` is `53,470` (due to tabu skips in `sa_tabu_adversarial`, line 857), that `"threshold_cographs"` (lines 689–696) specifically generates random threshold graphs, and that `"blowups_C5_S22"` (lines 712–725) generates $C_5$ blowups while $S_{2,2}$ copies/seeds are in `"multi_S22_high_gap"` and `"sa_tabu_adversarial"`.

---

## Reproduction Commands

```bash
# 1. Zero-dependency pure-Python rational-arithmetic proof & mutant verifier (~2s)
nice -n 10 python3 verify_proof.py

# 2. Solver brute-force & subcubic cross-validation on all 1,251 graphs of orders n = 2..7 (~0.05s)
clang++ -O3 -std=c++17 -pthread src/subquorum_engine.cpp -o build/subquorum_engine
nice -n 10 ./build/subquorum_engine --self-test

# 3. Full exhaustive n = 2..9 census (288,265 graphs) + 53,470 random/structured/SA-Tabu audit (~54s, 4 threads)
clang++ -O3 -std=c++17 -pthread src/verify_all.cpp -o build/verify_all
nice -n 10 ./build/verify_all
```

---

## Sources, Limitations, and Next Steps

- **Sources:**
  - Haobo Ma, Rafik Sahbi, and Wenlin Zhang, *Sub-quorum colorings of graphs*, `arXiv:2609.25128v4` (`inputs/2609.25128v4.tex.json.gz`).
  - S.M. Hedetniemi, S.T. Hedetniemi, R. Laskar, and H.M. Mulder, *Quorum colorings of graphs*, *AKCE Int. J. Graphs Comb.* 10(1) (2013), 97–109.
  - R. Sahbi and M. Chellali, *On some open problems concerning quorum colorings of graphs*, *Discrete Appl. Math.* 247 (2018), 294–299.
  - B. Brešar, M. Jakovac, J. Katrenič, G. Semanišin, and A. Taranenko, *On the vertex $k$-path cover*, *Discrete Appl. Math.* 161 (2013), 1943–1949.
- **Limitations & Next Steps:**
  1. While Theorem 1 settles the upper bound $\psi_{sq}(G) + \psi_{sq}(\overline{G}) \le n + 2$ for all $n \ge 2$, a complete structural characterization of all extremal graphs achieving equality $\psi_{sq}(G) + \psi_{sq}(\overline{G}) = n + 2$ (`21,354` of `274,668` graphs at $n = 9$, including all tested threshold graphs and `2,450` graphs with strict dissociation gap) remains a rich follow-up problem; tracking equality in Lemma 1–3 shows every extremal pair has $|S_1 \cap S_2| \in \{2, 3, 4, \dots\}$ with tightly constrained cross-boundary color classes.
  2. Determining the asymptotic order of the complementary Nordhaus–Gaddum lower extremal function $\min_{|V(G)|=n}\{\psi_{sq}(G) + \psi_{sq}(\overline{G})\}$ (bounded below by $\log_2 n$ in Theorem 9.1 of `arXiv:2609.25128v4`, with census minima $4, 5, 6, 6, 7, 7, 7, 8$ for $n = 2..9$) remains open.

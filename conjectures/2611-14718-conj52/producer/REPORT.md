Shipped: Exact-rational-certified disproof of Conjecture 5.2 of Higuita-Diaz, López & Roldán-Correa (`arXiv:2611.14718v2`), establishing the sharp minimum counterexample order $n = 15$ (`witness.json` + `verify_counterexample.py`: a 15-vertex, 14-edge subcubic tree $F_3$ with $\Delta = 3$ and $\mathbb{P}[N_G^{\mathrm{seq}} \le 6] = 64/3375 > 1/55 = \mathbb{P}[N_G^{\mathrm{stat}} \le 6]$, plus two 15-vertex unicyclic $\Delta = 3$ graphs with strict global static dominance $N_G^{\mathrm{seq}} <_{\mathrm{st}} N_G^{\mathrm{stat}}$ and an infinite family $\{F_m\}_{m \ge 3}$ of subcubic tree counterexamples), because chaining three 5-vertex subcubic hubs preserves sequential independence $(4/15)^3$ at $k=6$ while boosting static MIS multiplicity to $55 > 3375/64$.

RESULT: yes

## 1. Summary & Novelty Answer

- **Did we find something new? Yes.** Conjecture 5.2 (`\label{conj:grado3}`) of Higuita-Diaz, López & Roldán-Correa (`arXiv:2611.14718v2`, v2 revised 2026-11-18) states that for every finite simple graph $G$ with maximum degree $\Delta(G) \le 3$, the sequential (RSA) model first-order stochastically dominates the static (uniform MIS) model ($N_G^{\mathrm{stat}} \le_{\mathrm{st}} N_G^{\mathrm{seq}}$). The authors verified Conjecture 5.2 on all $27,525$ connected $\Delta \le 3$ graphs with $n \le 12$, and `csweep1` verified trees up to $n \le 14$.
- **Complete settlement & sharp threshold ($n = 15$):**
  1. Exhaustive exact evaluation of all **`1,375,631`** non-isomorphic connected simple graphs with $\Delta(G) \le 3$ and $1 \le n \le 15$ (`358,891` for $n \le 14$; `1,016,740` at $n = 15$, matching OEIS `A005967`) proves that **zero** counterexamples exist for $n \le 14$ (connected or disconnected, by Corollary 6.3 of `arXiv:2611.14718v2`), and **exactly three** non-isomorphic connected counterexamples exist at $n = 15$.
  2. **Unique vertex- and edge-minimal witness (`CE#1` = $F_3$, stored in [witness.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/witness.json)):** a **15-vertex, 14-edge subcubic tree** with $\Delta(F_3) = 3$ (only three vertices of degree 3):
     $$\mathbb{P}[N_{F_3}^{\mathrm{seq}} \le 6] = \frac{64}{3375} \approx 0.01896296 > \frac{1}{55} \approx 0.01818182 = \mathbb{P}[N_{F_3}^{\mathrm{stat}} \le 6],$$
     with exact reduced integer cross-difference $64 \times 55 - 1 \times 3375 = \mathbf{145 > 0}$ and exact gap $J(F_3) = \mathbf{\frac{29}{37125}}$. Deleting any single vertex or any single edge of $F_3$ restores $N^{\mathrm{stat}} \le_{\mathrm{st}} N^{\mathrm{seq}}$.
  3. **Strict global dominance & expectation reversal at $n = 15$ (`CE#2` and `CE#3`):** On the other two 15-vertex counterexamples (`CE#2`, unicyclic triangle-free of girth 5, $|E|=15$; and `CE#3` = $C_3(T_5)$, 3-fold symmetric unicyclic of girth 3, $|E|=15$, also edge-minimal), $N_G$ is supported solely on $\{6, 7\}$ with $|M(G)| = 55$ (`{6: 1, 7: 54}`) and $\mathbb{P}[N_G^{\mathrm{seq}} = 6] = 64/3375 > 1/55 = \mathbb{P}[N_G^{\mathrm{stat}} = 6]$. Hence on both `CE#2` and `CE#3`, **the static model strictly first-order stochastically dominates the sequential model ($N_G^{\mathrm{seq}} <_{\mathrm{st}} N_G^{\mathrm{stat}}$)** and strictly exceeds its mean occupancy:
     $$\mathbb{E}[N_G^{\mathrm{seq}}] = \frac{23561}{3375} \approx 6.98103704 < \frac{384}{55} \approx 6.98181818 = \mathbb{E}[N_G^{\mathrm{stat}}].$$
  4. **Infinite family of subcubic trees $\{F_m\}_{m \ge 3}$:** Chaining $m \ge 3$ copies of the 5-vertex subcubic unit $T_5$ gives a $5m$-vertex subcubic tree $F_m$ ($\Delta(F_m) = 3$) satisfying $\mathbb{P}[N_{F_m}^{\mathrm{seq}} \le 2m] = (4/15)^m$ and $|M(F_m)| = 5|M(F_{m-1})| - 4|M(F_{m-2})| + 2|M(F_{m-3})|$ ($1, 3, 13, 55, 229, 951, 3949, \dots$), so $\mathbb{P}[N_{F_m}^{\mathrm{seq}} \le 2m] / \mathbb{P}[N_{F_m}^{\mathrm{stat}} \le 2m] \sim c (4\lambda_*/15)^m \approx c (1.10835)^m \to +\infty$.

- **Why no statistical holdout / SBS baseline applies:** This is an exact deterministic discrete-mathematics certificate task over finite simple graphs, not a statistical prediction task. Verification is performed in exact arbitrary-precision rational arithmetic (`fractions.Fraction`) with zero floating-point operations by the standalone verifier [verify_counterexample.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/verify_counterexample.py).

---

## 2. Human-Verifiable Combinatorial Proof (Zero Computer Needed)

Let $T_5$ be the 5-vertex subcubic tree with vertex set $\{h, \ell_1, \ell_2, a, b\}$ and edges $\{h, \ell_1\}, \{h, \ell_2\}, \{h, a\}, \{a, b\}$ ($\deg(h)=3$, $\deg(a)=2$, $\deg(\ell_1)=\deg(\ell_2)=\deg(b)=1$). For $m \ge 1$, construct the $5m$-vertex tree $F_m$ by taking $m$ disjoint copies $V_i = \{h_i, \ell_1^{(i)}, \ell_2^{(i)}, a_i, b_i\}$ ($i = 1, \dots, m$) of $T_5$ and adding the $m-1$ bridge edges $\{\ell_2^{(i)}, \ell_1^{(i+1)}\}$ for $1 \le i \le m-1$. Every vertex in $F_m$ has degree at most $3$ ($\deg(h_i) = 3$, bridged $\ell$-vertices have degree $2$, unbridged end-leaves and $b_i$ have degree $1$).

1. **Minimum MIS size and exact static count at $k = 2m$:**
   In any $I \in M(F_m)$, each pendant edge $\{a_i, b_i\}$ contributes $|I \cap \{a_i, b_i\}| = 1$ (since $b_i$ has sole neighbor $a_i$). If $h_i \in I$ for all $i$, then $a_i$ is blocked so $b_i \in I$, giving the unique set $I^* = \bigcup_{i=1}^m \{h_i, b_i\}$ of size $2m$. Suppose instead that $\{i : h_i \notin I\}$ is decomposed into $r \ge 1$ maximal contiguous intervals $[j_0, j_1]$ of length $t = j_1 - j_0 + 1 \ge 1$. On each such interval, neither $\ell_1^{(j_0)}$ nor $\ell_2^{(j_1)}$ has an occupied neighbor outside the interval, so $\ell_1^{(j_0)}, \ell_2^{(j_1)} \in I$ are both forced ($+2$), while each of the $t-1$ disjoint internal bridge edges $\{\ell_2^{(j)}, \ell_1^{(j+1)}\}$ has both outside hubs excluded and therefore contributes exactly $1$ vertex to $I$ ($+(t-1)$), and the $t$ pairs $\{a_j, b_j\}$ contribute $t$ vertices. Thus the interval contributes $2 + (t-1) + t = 2t + 1$ vertices, proving $|I| = 2m + r \ge 2m + 1$ whenever $I \neq I^*$.
   For $m = 3$ ($F_3$, $n = 15$): counting subsets of excluded hubs $\{1, 2, 3\}$ gives:
   - $\emptyset$ ($r=0$, size 6): $1$ MIS ($I^*$).
   - $\{1\}, \{2\}, \{3\}$ ($r=1, t=1$, size 7): each forces $\ell_1^{(i)}, \ell_2^{(i)} \in I$ and leaves $2$ choices on $\{a_i, b_i\}$ $\implies 3 \times 2 = 6$ MISs.
   - $\{1, 3\}$ ($r=2$, two $t=1$ blocks, size 8): $2 \times 2 = 4$ MISs.
   - $\{1, 2\}, \{2, 3\}$ ($r=1, t=2$, size 7): $2$ choices on the internal bridge edge $\times 2^2$ choices on the two $\{a, b\}$ pairs $\implies 2 \times 8 = 16$ MISs.
   - $\{1, 2, 3\}$ ($r=1, t=3$, size 7): of the $4$ choices $(x_1, x_2) \in \{L, R\}^2$ on the two internal bridge edges, $(L,L), (R,L), (R,R)$ leave $2^3 = 8$ choices each on $\{a_i, b_i\}_{i=1}^3$, while $(L,R)$ leaves both $\ell_1^{(2)}, \ell_2^{(2)} \notin I$, forcing $a_2 \in I$ to dominate $h_2$ ($2 \cdot 1 \cdot 2 = 4$ choices) $\implies 24 + 4 = 28$ MISs.
   Summing gives $|M(F_3)| = 1 + 6 + 4 + 16 + 28 = \mathbf{55}$, so $\mathbb{P}[N_{F_3}^{\mathrm{stat}} \le 6] = \mathbf{\frac{1}{55}}$.

2. **Exact sequential probability at $k = 2m$:**
   Couple the RSA process with i.i.d. arrival times $U_v \sim \mathrm{Uniform}(0,1)$ for $v \in V(F_m)$. On a single 5-vertex unit $V_i$, the greedy process restricted to $V_i$ outputs $\{h_i, b_i\}$ iff either $U_{h_i} = \min_{v \in V_i} U_v$ (prob. $1/5$) or $U_{b_i} = \min_{v \in V_i} U_v$ and $U_{h_i} = \min(U_{h_i}, U_{\ell_1^{(i)}}, U_{\ell_2^{(i)}})$ (prob. $\frac{1}{5} \cdot \frac{1}{3} = \frac{1}{15}$), totaling $\frac{4}{15}$. Whenever this event holds in every unit $i = 1, \dots, m$, every $h_i$ arrives strictly before both $\ell_1^{(i)}$ and $\ell_2^{(i)}$ (either first in $V_i$, or immediately after $b_i$ which only blocks $a_i$), so no bridge vertex $\ell_1^{(i)}, \ell_2^{(i)}$ can ever be occupied before its own hub $h_i$ blocks it; conversely, if $F_m$'s global greedy MIS is $I^*$, no $\ell$-vertex is occupied so the bridge edges never transmit any blocking between units, implying the internal arrival order of each $V_i$ must yield $\{h_i, b_i\}$. Since $V_1, \dots, V_m$ are disjoint,
   $$\mathbb{P}[N_{F_m}^{\mathrm{seq}} \le 2m] = \mathbb{P}[I_{\mathrm{seq}} = I^*] = \left(\frac{4}{15}\right)^m.$$
   At $m = 3$ ($n = 15$), $\mathbb{P}[N_{F_3}^{\mathrm{seq}} \le 6] = \frac{64}{3375} > \frac{1}{55} = \mathbb{P}[N_{F_3}^{\mathrm{stat}} \le 6]$ because $64 \times 55 = 3520 > 3375$. $\blacksquare$

---

## 3. Exact Evaluation Counts & Near-Miss Landscape

### 3.1 Exhaustive Connected Subcubic Census ($1 \le n \le 15$)
Computed via [src/validate_and_census.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/src/validate_and_census.cpp) (`1,375,631` non-isomorphic connected $\Delta \le 3$ graphs, logs in [census_n14.txt](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/logs/census_n14.txt) and [census_n15.txt](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/logs/census_n15.txt)):

| $n$ | Connected $\Delta \le 3$ graphs | Well-covered | Max $J^*(G)$ (exact rational) | Max $R^*(G) = F_{\mathrm{seq}}/F_{\mathrm{stat}}$ | Counterexamples |
|---:|---:|---:|---:|---:|---:|
| 1–2 | 2 | 2 | — | — | 0 |
| 3 | 2 | 1 | $-1/6 \approx -1.667 \times 10^{-1}$ (`1/3` vs `1/2`, $k=1$) | $0.666667$ | 0 |
| 4 | 6 | 3 | $-1/12 \approx -8.333 \times 10^{-2}$ (`1/4` vs `1/3`, $k=1$) | $0.750000$ | 0 |
| 5 | 10 | 5 | $-1/15 \approx -6.667 \times 10^{-2}$ (`4/15` vs `1/3`, $k=2$) | $0.800000$ | 0 |
| 6 | 29 | 9 | $-4/45 \approx -8.889 \times 10^{-2}$ (`1/9` vs `1/5`, $k=2$) | $0.833333$ | 0 |
| 7 | 64 | 9 | $-1/24 \approx -4.167 \times 10^{-2}$ (`1/12` vs `1/8`, $k=2$) | $0.830357$ | 0 |
| 8 | 194 | 22 | $-3/208 \approx -1.442 \times 10^{-2}$ (`1/16` vs `1/13`, $k=2$) | $0.862500$ | 0 |
| 9 | 531 | 23 | $-2/195 \approx -1.026 \times 10^{-2}$ (`1/15` vs `1/13`, $k=3$) | $0.877037$ | 0 |
| 10 | 1,733 | 46 | $-17/2925 \approx -5.812 \times 10^{-3}$ (`16/225` vs `1/13`, $k=4$) | $0.924444$ | 0 |
| 11 | 5,524 | 47 | $-7/816 \approx -8.578 \times 10^{-3}$ (`1/48` vs `1/34`, $k=3$) | $0.915791$ | 0 |
| 12 | 19,430 | 80 | $-9/3520 \approx -2.557 \times 10^{-3}$ (`1/64` vs `1/55`, $k=3$) | $0.931852$ | 0 |
| 13 | 69,322 | 115 | $-1/660 \approx -1.515 \times 10^{-3}$ (`1/60` vs `1/55`, $k=4$) | $0.953333$ | 0 |
| 14 | 262,044 | 172 | $-1/2475 \approx -4.040 \times 10^{-4}$ (`4/225` vs `1/55`, $k=5$) | $0.977778$ | 0 |
| **15** | **1,016,740** | **260** | **$+29/37125 \approx +7.811 \times 10^{-4}$ (`64/3375` vs `1/55`, $k=6$)** | **$1.042963$** | **3** |
| **Total** | **1,375,631** | **794** | — | — | **3** |

### 3.2 Multi-Strategy & Subclass Search ($n = 14..30$, [search_subcubic.txt](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/logs/search_subcubic.txt))
- **Mode 0 (Unrestricted connected $\Delta \le 3$, $n = 15..28$):** `35,273` SA evaluations, `5` counterexample hits (rediscovering $n=15, |E|=15, J=+29/37125$).
- **Mode 1 (Subcubic trees, $\Delta \le 3$, $n = 15..30$):** `55,831` SA evaluations, `144` counterexample hits, peaking on $F_4$ ($n=20, |E|=19, k=8$: `256/50625 > 1/229`, $R^* = 1.158005$, $J = 7999/11593125$) and extending analytically via $F_m$ ($n=25$: `1024/759375 > 1/951`, $R^* = 1.282402$).
- **Mode 2 (Triangle-free connected $\Delta \le 3$, $n = 14..26$):** `33,396` SA evaluations, `7` counterexample hits ($R^* = 1.158005$ at $n=20$).
- **Mode 3 (3-regular cubic connected graphs, $n = 14..22$):** `35,389` SA 2-switch evaluations, **`0` counterexamples** (closest near-miss: $n=22, |E|=33, k=8$, $R^* = 0.988013$, $J^* = -8.991 \times 10^{-3}$).
- **Failed constructions documented:** Naive cycle-gluing $C_m(T_5)$ succeeded at $m=3$ ($n=15$, `CE#3`) because all 3 leaves of $T_5$ remained free, whereas $C_4(T_5), C_5(T_5), C_6(T_5)$ ($n = 20, 25, 30$) failed ($R^* = 0.733, 0.851, 0.801$) because using only one leaf per unit along a higher cycle yields smaller MIS multiplicity growth ($\approx 3.65^m < 3.75^m$) than chaining $\ell_2^{(i)}$ to $\ell_1^{(i+1)}$ ($F_m$, growth $\approx 4.156^m > 3.75^m$). Similarly, attaching bare paths to `CE#3` at $n = 16..28$ diluted the single-point tail without amplifying static multiplicity.

---

## 4. Verification & Self-Audit Verdict

- **`CONTROLS:` No** — no assumption overrode what the controls show. Checked in [verify_counterexample.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/verify_counterexample.py#L204-L243) via `python3 verify_counterexample.py`: all 5 controls ran and passed before witness certification — Control 1 (paper's Section 5.2 $n=6, \Delta=4$ graph: $D_1$ fails with $5/24 > 1/5$, and `is_subcubic_counterexample` explicitly rejects $\Delta=4 > 3$), Control 2 ($P_4$, $\Delta=2$: $D_1$ passes), Control 3 ($K_3$, $\Delta=2$: $D_1$ passes), Control 4 ($P_3$, $\Delta=2$: $D_1$ passes strictly with $1/3 < 1/2$), and Control 5 (top $n=14$ subcubic near-miss: $4/225 < 1/55$, $p_1 q_2 - p_2 q_1 = -5 < 0$, $D_1$ passes). Cross-checked C++ engine against brute-force $2^n$ subsets and $n!$ permutations in [validate_and_census.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/src/validate_and_census.cpp#L63-L148) (`307` subcubic graphs $n \le 8$ + `200` random $n=8$ graphs, 0 mismatches).
- **`CONTRADICTING:` No** — no contradicting data was dropped or ignored. Checked across all `1,375,631` graphs in [census_n15.txt](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/logs/census_n15.txt) and `159,889` SA evaluations in [search_subcubic.txt](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/logs/search_subcubic.txt): we explicitly report that on primary tree witness `CE#1` ($F_3$), the CDFs cross in the opposite direction at $k=7$ ($8185211/10135125 < 51/55$), that $n \le 14$ has $0$ counterexamples (`358,891` graphs), that $C_m(T_5)$ fails for $m=4,5,6$, and that 3-regular cubic search (`35,389` evals up to $n=22$) found $0$ counterexamples. Note that Conjecture 5.2 requires $\mathbb{P}[N_G^{\mathrm{seq}} \le k] \le \mathbb{P}[N_G^{\mathrm{stat}} \le k]$ for *all* $k \ge 0$, so $k=6$ on `CE#1` already disproves Conjecture 5.2, and `CE#2`/`CE#3` have no reverse crossing at any $k$.
- **`LABELS:` No** — no label, graph degree, or MIS annotation was trusted without checking raw data. Checked in [verify_counterexample.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/verify_counterexample.py#L18-L120): `validate_simple_graph` verifies vertex range $0 \le u,v < 15$, absence of self-loops and parallel edges, BFS connectivity, and computes $\Delta(G) = \max_v \deg(v) = 3$ directly from raw edge endpoints in [witness.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/witness.json); `enumerate_exact_mis_sets` explicitly checks `(adj[v] & mask) == 0` (independence) and `dom == (1 << n) - 1` (maximality) on all `55` discovered MIS bitmasks; `compute_exact_rsa_pmf` asserts $\sum_k \mathbb{P}[N_G^{\mathrm{seq}} = k] == \mathrm{Fraction}(1, 1)$; and `verify_minimality` ([verify_counterexample.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/verify_counterexample.py#L246-L263)) directly re-evaluates all `15` subgraphs $G-v$ and all `14` subgraphs $G-e$.

---

## 5. Reproduction Commands

Run from `/Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic`:

```bash
# 1. Standalone zero-dependency exact rational verification (< 0.2s, Python stdlib only)
python3 verify_counterexample.py witness.json

# 2. Exact rational reproduction of paper baselines (Sec. 5.2, 5.3, 6.2)
python3 repro_prior_art.py

# 3. Compile and run C++ engine brute-force + OEIS A005967 (27,525) validation (~1.8s)
mkdir -p bin logs
clang++ -O3 -std=c++20 -pthread -Wall -Wextra src/validate_and_census.cpp -o bin/csweep_census
nice -n 10 ./bin/csweep_census --validate-only

# 4. Complete exhaustive n <= 15 connected subcubic census (~3 min on 4 threads)
nice -n 10 ./bin/csweep_census --max-n 15 --threads 4

# 5. Multi-strategy & subclass search (trees, triangle-free, cubic; ~77s on 4 threads)
clang++ -O3 -std=c++20 -pthread -Wall -Wextra src/search_subcubic.cpp -o bin/csweep_search
nice -n 10 ./bin/csweep_search
```

---

## 6. Sources, Limitations & Next Steps

- **Sources:**
  - Higuita-Diaz, López & Roldán-Correa, `arXiv:2611.14718v2` (2026-11-18) and MIT-licensed repository `https://github.com/lykoslopezrivera-blip/Stochastic_Dominance_DPP_Graphs` (see [PRIOR_ART.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_subcubic/PRIOR_ART.md)).
  - McKay, *J. Algorithms* **26** (1998), 306–324 (canonical deletion for isomorph-free graph generation).
  - OEIS `A005967` (number of connected simple graphs on $n$ vertices with $\Delta \le 3$).
- **Limitations & Open Next Steps:**
  1. **Cubic (3-regular) graphs ($\delta(G) = \Delta(G) = 3$):** Every counterexample we found uses vertices of degree $1$ and $2$ (pendant leaves and $P_2$ tails) to create forced occupations when degree-3 hubs are excluded. Across `35,389` simulated annealing evaluations on connected 3-regular graphs ($n = 14..22$) and all cubic graphs in our $n \le 15$ census, zero cubic counterexamples appeared (closest ratio $R^* = 0.98801$ at $n = 22$). Determining whether $N_G^{\mathrm{stat}} \le_{\mathrm{st}} N_G^{\mathrm{seq}}$ holds for all **cubic (3-regular)** graphs or all **claw-free** subcubic graphs (such as $2 \times n$ ladder graphs, which are claw-free) is the natural sharpened replacement for Conjecture 5.2.
  2. **Minimum degree $\delta(G) \ge 2$:** Testing whether eliminating degree-1 leaves ($\delta(G) \ge 2, \Delta(G) \le 3$) suffices to restore $N_G^{\mathrm{stat}} \le_{\mathrm{st}} N_G^{\mathrm{seq}}$ — e.g., by replacing pendant $P_2$ tails with diamond ($K_4 - e$) or $C_4$ gadgets at $n = 20..40$ — is an immediate follow-up computation.

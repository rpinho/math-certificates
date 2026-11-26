# Clean-Room Cross-Family Referee Audit (`REFEREE2.md`)
**Job:** `math_e1182kempefixref_1125`  
**Target Claim:** Repaired Case I proof and 160-bit Arb certificate for **Erdős #1182 ($F(n) \le 5n - 1$ for every integer $n \ge 550{,}000$, including odd $n$)**, produced by `gpt-6.2-sol`.  
**Referee Verdict:** **`VERDICT: HOLDS`**

---

## 1. Scope, Clean-Room Isolation, and SHA-256 Hash Locks

### 1.1 Clean-Room Protocol
- Audited **exclusively** the six staged files inside `/Users/ricardo/dev/open-science/math_wave_1030/e1182kempe_referee2/inputs/`:
  - `inputs/PROOF.md`, `inputs/LEMMAS.md`, `inputs/REPORT.md`
  - `inputs/cert_case1.json.gz`, `inputs/cert_naive_ab.json.gz`, `inputs/cert_case2.json.gz`
- Zero files outside `/Users/ricardo/dev/open-science/math_wave_1030/e1182kempe_referee2` were read, inspected, copied, or executed.
- All verification and control code (`arb_case1_referee.py`, `controls_referee.py`) was written from scratch using `/Users/ricardo/dev/open-science/.venv/bin/python` (`python-flint 0.9.0` + Python standard library ONLY).

### 1.2 SHA-256 Certificate Hash Lock Check (`verify.log` lines 2–6)
| Staged Archive | Expected SHA-256 (from sealed Round 1) | Measured SHA-256 | Status |
|---|---|---|---|
| `inputs/cert_naive_ab.json.gz` | `b4cbc312f5f1a042990c031df8b35542eb6f192639ea93edf024b61002ec5989` | `b4cbc312f5f1a042990c031df8b35542eb6f192639ea93edf024b61002ec5989` | **EXACT MATCH** |
| `inputs/cert_case2.json.gz` | `c68d3339047880b19de426b6bde3114630ce10ad853ecc409926f621d5c3bab8` | `c68d3339047880b19de426b6bde3114630ce10ad853ecc409926f621d5c3bab8` | **EXACT MATCH** |
| `inputs/cert_case1.json.gz` | *(Repaired `format: 2` Case I archive)* | `09fba47458edf71cf255b63bb3842e4360b7d275748543c61c9b6fe494bf0611` | **RECORDED & VERIFIED** |

Because `cert_naive_ab.json.gz` and `cert_case2.json.gz` are byte-identical to the archives accepted by the sealed Round 1 Claude Opus 5.5 referee (`math_e1182kemperef_1125`) alongside the reduction, disconnection bound ($\le e/(16-e) < 3/13$), odd-$n$ support, and Kempe-swap dichotomy (`83,966` swaps, `0` invalid, `3/3` mutants), closing Erdős #1182 for all $n \ge 550{,}000$ reduces to auditing the repaired Case I mathematics, `cert_case1.json.gz`, and the resulting finite-$n$ bound.

---

## 2. First-Principles Mathematical Audit of Repaired Case I

Let $d = 10$, $D = dn = 10n$ (always even for every integer $n \ge 1$, including odd $n$), $v_i = n a_i$, $S_i = d v_i = D a_i$, and blue adjacency $A_{ij} = \mathbf{1}_{(i-j) \bmod 5 \in \{0,2,3\}}$ on $\mathbb{Z}_5$.

### 2.1 Pairing Law and Stirling Prefactor (`inputs/LEMMAS.md` §1)
For a fixed map $f: V(M) \to \mathbb{Z}_5$ of profile $v = (v_0,\dots,v_4)$ and any admissible symmetric integer stub-matching matrix $K = (K_{ij})$ supported on $A_{ij} = 1$ with row sums $\sum_j K_{ij} = S_i$ and $K_{ii}$ even, counting destination partitions $\prod_i \bigl(S_i! / \prod_j K_{ij}!\bigr)$, internal matchings $\prod_i (K_{ii}-1)!!$, and inter-part bijections $\prod_{i<j} K_{ij}!$ divided by $(D-1)!! = D! / (2^{D/2}(D/2)!)$ yields:
$$p_K = \Pr(K \mid f) = \frac{2^{D/2}(D/2)!}{D!} \frac{\prod_{i=0}^4 S_i!}{\prod_{i=0}^4 2^{K_{ii}/2}(K_{ii}/2)! \prod_{i<j} K_{ij}!}.$$
For every integer $m \ge 0$ (with $0^0 = 1$), concavity of $\log x$ via the trapezoidal sum vs. right-endpoint integral on $[1, m]$ gives:
$$\left(\frac{m}{e}\right)^m \le m! \le e\sqrt{m+1}\left(\frac{m}{e}\right)^m.$$
Applying the upper bound to the $6$ numerator factorials ($(D/2)!$ and $S_0!,\dots,S_4!$, each $\le D$) and the lower bound to all denominator factorials:
- Prefactor: $e \sqrt{D/2 + 1} \cdot e^5 \prod_{i=0}^4 \sqrt{S_i + 1} \le e^6 (D+1)^3 < 3^6 (D+1)^3$.
- Powers of $e$: numerator $e^{-D/2 - \sum S_i} = e^{-3D/2}$; denominator $e^{-D - \sum K_{ii}/2 - \sum_{i<j} K_{ij}} = e^{-3D/2}$ (exact cancellation).
- Powers of $2$: $2^{D/2} \cdot 2^{-D/2} = 1$ in numerator; $2^{K_{ii}/2} \cdot 2^{-K_{ii}/2} = 1$ in denominator (exact cancellation).
- Powers of $D$: with $Q_{ij} = K_{ij}/D$, numerator $D^{D/2 + D} = D^{3D/2}$ and denominator $D^{D + \sum_{ij} K_{ij}/2} = D^{3D/2}$ (exact cancellation).
- Multinomial map count: $\binom{n}{v_0,\dots,v_4} \le \prod_{i=0}^4 a_i^{-n a_i} = \exp\bigl(-n \sum_{i=0}^4 a_i \log a_i\bigr)$.

Combining $10 \sum_i a_i \log a_i - \sum_i a_i \log a_i = 9 \sum_i a_i \log a_i$ proves:
$$\binom{n}{v_0,\dots,v_4} p_K \le 3^6 (D+1)^3 \exp\bigl(n L(a, Q)\bigr), \qquad L(a, Q) = 9 \sum_{i=0}^4 a_i \log a_i - 5 \sum_{i,j=0}^4 Q_{ij} \log Q_{ij}. \quad \checkmark$$

### 2.2 Tilt Decomposition and Binary-KL Upper Tail (`inputs/LEMMAS.md` §2)
For any tilt $t = (t_0,\dots,t_4) \in (0, \infty)^5$, put $Z = \sum_{i,j} A_{ij} t_i t_j > 0$ and $B_{ij} = A_{ij} t_i t_j / Z$. Since $\sum_j Q_{ij} = a_i$, $\sum_i Q_{ij} = a_j$, and $\sum_{i,j} Q_{ij} = 1$:
$$L(a, Q) = U_t(a) - 5 D_{\mathrm{KL}}(Q \Vert B), \qquad U_t(a) = 9 \sum_{i=0}^4 a_i \log a_i - 10 \sum_{i=0}^4 a_i \log t_i + 5 \log Z.$$
Coarse-graining the blue index set $E_{\mathrm{blue}} = \{(i,j) : A_{ij} = 1\}$ into $C_1 = \{(0,3), (3,0)\}$ (having $Q$-mass $2 Q_{03}$ and $B$-mass $2 B_{03} \in (0, 1)$, since $Z > t_0^2 + t_3^2 + 2 t_0 t_3 > 2 t_0 t_3$) and $C_2 = E_{\mathrm{blue}} \setminus C_1$ gives, by the log-sum inequality:
$$D_{\mathrm{KL}}(Q \Vert B) \ge \mathcal{D}(2 Q_{03}, 2 B_{03}), \qquad \mathcal{D}(x, b) = x \log \frac{x}{b} + (1 - x) \log \frac{1 - x}{1 - b}.$$
Differentiating with respect to $x \in (0, 1)$ at fixed $b \in (0, 1)$:
$$\frac{\partial}{\partial x}\mathcal{D}(x, b) = \log \frac{x(1 - b)}{b(1 - x)},$$
which is strictly negative on $(0, b)$, zero at $x = b$, and **strictly positive on $(b, 1)$** (continuous up to $x = 1$). Therefore:
- **Crucial cutoff requirement:** Whenever $q_* \ge B_{03}$ (with $2 q_* < 1$), every feasible $Q$ in the upper tail $Q_{03} > q_*$ satisfies $1 \ge 2 Q_{03} > 2 q_* \ge 2 B_{03}$, so $\mathcal{D}(2 Q_{03}, 2 B_{03}) > \mathcal{D}(2 q_*, 2 B_{03}) \ge 0$, whence:
  $$L(a, Q) \le U - 5 \mathcal{D}(2 q_*, 2 B_{03}) \qquad \text{for all } Q_{03} > q_* \text{ when } U_t(a) \le U \text{ and } q_* \ge B_{03}. \quad \checkmark$$
- Conversely, if $q_* < B_{03}$ were allowed, $Q_{03} = B_{03} > q_*$ would belong to the tail while $\mathcal{D}(2 B_{03}, 2 B_{03}) = 0 < \mathcal{D}(2 q_*, 2 B_{03})$, invalidating the tail inequality. Strict enforcement of $q_* \ge B_{03}$ on every occupancy leaf is therefore necessary and sufficient for tail soundness.

### 2.3 Case I Conditional Occupancy Law and Exempt-Set Prefactor (`inputs/LEMMAS.md` §3)
In Region C ($\min(a_0, a_2) - a_3 \ge 3/20$, $a_3 \ge a_4 \ge 0$), every profile satisfies $a_0 \ge 3/20$ (in fact $a_0 \ge 0.224975$), so for $n \ge 550{,}000$, $v_0 = n a_0 \ge 82{,}500 \ge 38 = 2b$ where $b = 2d - 1 = 19$.
- Case I requires $|Z_0| \le 19$, where $Z_0 = \{u \in V_0 : n_3(u) = 0\}$. Since $v_0 \ge 19$, $|Z_0| \le 19$ holds if and only if there exists a subset $W \subseteq V_0$ of **exact size $|W| = 19$** such that every $u \in V_0 \setminus W$ has $n_3(u) \ge 1$.
- Conditional on $K$, the $K_{03}$ destination-$3$ stubs in row $0$ form a uniform $K_{03}$-subset of the $N_0 = d v_0$ stubs of $V_0$.
- If $K_{03} < v_0 - 19$, disjointness of the $v_0 - 19$ vertex stub blocks forces $\Pr(\mathcal{E}_{\mathrm{I}} \mid K) = 0$.
- Assume $K_{03} \ge v_0 - 19$. Since $v_0 \ge 2b = 38$, $v_0 - b \ge v_0 / 2$, so $p = \frac{K_{03}}{d v_0} = \frac{Q_{03}}{a_0} \ge \frac{1}{2d} = \frac{1}{20}$.
- Under $\mathrm{Binomial}(N_0, p)$ with $p = k/N_0$ ($k = K_{03}$): for $0 < p < 1$, $\frac{b_{m+1}}{b_m} = \frac{(N_0 - m)k}{(m+1)(N_0 - k)}$ exceeds $1$ for $m \le k-1$ and is $< 1$ for $m \ge k$ (since $(N_0 - m)k - (m+1)(N_0 - k) = N_0(k - m - 1) + k$). Thus $k = K_{03}$ is the unique mode of $\mathrm{Binomial}(N_0, p)$ (and $\Pr = 1$ at $p = 1$), so $\Pr_p(S = K_{03}) \ge \frac{1}{N_0 + 1} \ge \frac{1}{D + 1}$.
- Conditioning i.i.d. $\mathrm{Bernoulli}(p)$ stubs on $S = K_{03}$ reproduces the uniform $K_{03}$-subset law; hence for fixed $W \in \binom{V_0}{19}$:
  $$\Pr(\forall u \in V_0 \setminus W,\ n_3(u) \ge 1 \mid K) \le (D + 1) f(p)^{v_0 - 19}, \qquad f(p) = 1 - (1 - p)^{10}.$$
- By Bernoulli's inequality on $[0, 1]$, $(1 - p)^{10} \le 1 - p$, so $f(p) \ge p \ge \frac{1}{20}$, giving $f(p)^{-19} \le 20^{19}$. Also $\binom{v_0}{19} \le v_0^{19} \le n^{19}$. Union-bounding over $\binom{v_0}{19}$ choices of $W$ yields:
  $$\Pr(\mathcal{E}_{\mathrm{I}} \mid K) \le (D + 1) n^{19} 20^{19} \exp\bigl(n a_0 \log f(Q_{03}/a_0)\bigr). \quad \checkmark$$

### 2.4 Rigorous Derivative Signs & Direction of the Upper Cutoff (`inputs/LEMMAS.md` §3)
Define $g(a, q) = a \log f(q/a) = a \log\bigl(1 - (1 - q/a)^{10}\bigr)$ for $a > 0$ and $0 \le q \le a$ (with $g(a, 0) = -\infty$, $g(a, a) = 0$). For $0 < q < a$, put $p = q/a \in (0, 1)$:
1. **Strict increase in $q$ ($Q_{03}$) at fixed $a > 0$:**
   $$\frac{\partial g}{\partial q}(a, q) = a \cdot \frac{10(1 - p)^9}{1 - (1 - p)^{10}} \cdot \frac{1}{a} = \frac{10(1 - p)^9}{1 - (1 - p)^{10}} > 0 \quad \forall p \in (0, 1),$$
   since $1 - p \in (0, 1) \implies (1-p)^9 > 0$ and $1 - (1-p)^{10} \in (0, 1)$. With $\lim_{q \downarrow 0^+} g(a, q) = -\infty$ and $\lim_{q \uparrow a^-} g(a, q) = 0$, $q \mapsto g(a, q)$ is **strictly increasing on $[0, a]$**. $\checkmark$
2. **Strict decrease in $a$ ($a_0$) at fixed $q > 0$ (for $a > q$), nonincreasing on $(0, \infty)$:**
   For $a > q > 0$, $\frac{\partial p}{\partial a} = -q/a^2 = -p/a$, so:
   $$\frac{\partial g}{\partial a}(a, q) = \log\bigl(1 - (1 - p)^{10}\bigr) - \frac{10 p (1 - p)^9}{1 - (1 - p)^{10}}.$$
   For every $p \in (0, 1)$:
   - $0 < 1 - (1 - p)^{10} < 1 \implies \log\bigl(1 - (1 - p)^{10}\bigr) < 0$ strictly;
   - $10 p (1 - p)^9 > 0$ and $1 - (1 - p)^{10} > 0 \implies -\frac{10 p (1 - p)^9}{1 - (1 - p)^{10}} < 0$ strictly.
   Hence $\frac{\partial g}{\partial a}(a, q) < 0$ strictly on $(q, \infty)$. Extending continuously by $\tilde{g}(a, q) = a \log f(\min(1, q/a)) = 0$ on $(0, q]$ gives a continuous **nonincreasing** function of $a \in (0, \infty)$. $\checkmark$
3. **Combined leaf inequality at upper cutoff $q_* > 0$:**
   On any leaf box with $U_t(a) \le U$ and tightened lower endpoint $a_{0,\min} > 0$:
   - **Near cell ($Q_{03} \le q_*$):** Since $Q_{03} \le \min(a_0, q_*)$, increase in $q$ and nonincrease in $a$ give:
     $$L(a, Q) + g(a_0, Q_{03}) \le U + \tilde{g}(a_0, q_*) \le U + a_{0,\min} \log f\bigl(\min(1, q_*/a_{0,\min})\bigr).$$
   - **Far tail ($Q_{03} > q_*$):** Using $\Pr(\mathcal{E}_{\mathrm{I}} \mid K) \le 1$ (and $g \le 0$), if $q_* \ge B_{03}$, §2.2 gives:
     $$L(a, Q) + g(a_0, Q_{03}) \le L(a, Q) \le U - 5 \mathcal{D}(2 q_*, 2 B_{03}).$$
   Every integer pairing matrix $K$ satisfies either $Q_{03} \le q_*$ or $Q_{03} > q_*$ (disjoint partition of types, so zero extra factor of $2$). $\checkmark$

### 2.5 Finite-$n$ Prefactor and 160-bit Arb Check at $n_0 = 550{,}000$ (`finite.log` lines 1–15)
- **Complete count over ALL admissible $K$ (no typical-$K$ truncation):**
  - Dihedral maps: $\le 10$.
  - Profiles $v = (v_0,\dots,v_4)$ summing to $n$: $\binom{n+4}{4} \le (n+1)^4$.
  - Symmetric integer blue matrices $K$ for fixed $v$: $\overline{C_5}$ has exactly $5$ off-diagonal unordered blue edges ($\{0,2\}, \{0,3\}, \{1,3\}, \{1,4\}, \{2,4\}$), each in $\{0,\dots,D\}$ ($\le (D+1)^5 = (10n+1)^5$ choices), uniquely fixing all $5$ diagonal entries $K_{ii} = S_i - \sum_{j \ne i} K_{ij}$. Every admissible symmetric blue $K$ is counted.
  - Per-term multipliers when certified leaf rates are $\le -1/1000$:
    - A $\cup$ B naive: $\le 3^6 (10n+1)^8 e^{-n/1000}$.
    - Region C, Case I: $\le 3^6 (10n+1)^9 n^{19} 20^{19} e^{-n/1000}$ (at $n_0 = 550{,}000$, $10 \times$ this term alone is $2.581917327502 \times 10^{-18}$).
    - Region C, Case II: $\le 3^6 (10n+1)^9 e^{-n/1000}$ (bounded conservatively by $3^6 (10n+1)^{10} e^{-n/1000}$).
  - Summing all $10$ orientations $\times$ $3$ terms yields `PROOF.md` eq. (35):
    $$\mathbb{E} X_{\mathrm{rigid}} \le B(n) := 30 \cdot 3^6 (n+1)^4 (10n+1)^{10}\, n^{19} 20^{19}\, e^{-n/1000}.$$
- **160-bit Arb values at $n_0 = 550{,}000$ (`finite.log` lines 8–14):**
  - $B(550{,}000) = [4.2601643649539548653672494951787149840843670154 \times 10^{-11} \pm 2.87 \times 10^{-58}] < 4.261 \times 10^{-11}$.
  - Disconnection bound: $\Pr(M\text{ disconnected}) \le \sum_{k=1}^{\lfloor n/2\rfloor} (e(k/n)^4)^k \le \frac{e}{16 - e} \approx 0.204663417289 < \frac{3}{13} \approx 0.230769230769$.
  - Total failure probability: $B(550{,}000) + \frac{3}{13} = [0.23076923081183241288... \pm 4.49 \times 10^{-49}] < 1$ (and $0.204663417332 < 1$ with $e/(16-e)$).
  - Monotonicity for all $n \ge 550{,}000$: $\frac{d}{dn}\log B(n) = \frac{4}{n+1} + \frac{100}{10n+1} + \frac{19}{n} - \frac{1}{1000} < \frac{33}{n} - \frac{1}{1000} \le -0.00094 < 0$.
  - Threshold persistence for all $n \ge 550{,}000$: cap $\frac{2}{5} + \frac{3}{5n} \le \frac{4001}{10000}$ ($n \ge 6{,}000$), Region C transfer gap $\frac{3}{20}n \ge 2$ ($n \ge 14$), and Case I mode/exemption condition $v_0 \ge \frac{3}{20}n \ge 38$ ($n \ge 254$) all hold.

### 2.6 Audit of Unverified External Claims in `inputs/PROOF.md` and `inputs/REPORT.md`
- **`inputs/PROOF.md` and `inputs/LEMMAS.md` (Theorem-critical content):** **Zero** unverified external mathematical claims remain. Every construction, algebraic identity, Stirling bound, Kempe-swap step, occupancy inequality, KL tail bound, polytope coverage step, and disconnection bound is proved from elementary first principles. (`reference_table.json` mentioned in `LEMMAS.md` line 111 is explicitly marked diagnostic and is unused in the proof.)
- **`inputs/REPORT.md` (Contextual / producer-log prose):** Contains bibliographic comparisons (`PRIOR_ART.md`, `erdosproblems.com/1182`, Kataria's unrefereed $5.025n$ at `Sovi11/erdos-1182`, Brandt's $84n$ and unproved $11.75n`) and operational metadata from the producer workspace (`produce.log` $< 90\text{ MiB}$ RSS, two-run deterministic `cmp`, producer `STATUS.md` historical 311-leaf count, and Round 1 `controls.log` counts). None of these unstaged references are used in the mathematical proof of $F(n) \le 5n - 1$; the novel theorem statement $F(n) \le 5n - 1$ ($\forall n \ge 550{,}000$) stands completely on the staged proof and hash-locked certificates.

---

## 3. Standalone 160-bit Arb Certificate Verification (`arb_case1_referee.py` -> `verify.log`)

`arb_case1_referee.py` (`python-flint 0.9.0`, `flint.ctx.prec = 160`, stdlib only) verified `inputs/cert_case1.json.gz` from scratch:
- **Header & Exact Root:** `format == 2`, `case == 'case1'`, `grid = 10485760000`, `tilt_scale = 1000000000000`, exact rational root $[0, 4195352576/10485760000]^5 = [0, 4001/10000]^5$, global claim $-1/1000$.
- **Inductive Partition Coverage:** Consumed `3,049 / 3,049` records (`1,524` strictly interior splits `'S'`, `766` naive leaves `'N'`, `759` occupancy leaves `'C'`, `0` `'X'` leaves, `0` truncated branches, `0` trailing records). Every split replaces $[\ell_d, u_d]$ by $[\ell_d, s] \cup [s, u_d]$ with $\ell_d < s < u_d$, inductively covering $100\%$ of $[0, 4001/10000]^5$ and hence $100\%$ of canonical Region C.
- **Dual Independent Vertex Enumeration (Zero Trust of Stored Bounds):**
  1. *Outer tightened sliced-box superset $H(B')$:* Exact `Fraction` propagation of $\sum_i a_i = 1$ and Region C differences yields $B' \supseteq P_C(B)$; enumerating all points with $\ge 4$ endpoint coordinates (`15,523` vertices across the `759` `'C'` leaves) captures all extreme points of $H(B')$ unconditionally (even on the 1 singleton `'N'` leaf). Worst-case recomputed leaf bound: **`-0.001000001020155670 <= -1/1000`**.
  2. *Exact Region C 4D polytope $P_C(B)$:* Sequential exact rational halfspace clipping (`15,446` verified extreme points across the `759` `'C'` leaves) independently gives the identical worst-case recomputed leaf bound **`-0.001000001020155670 <= -1/1000`**.
  3. *Stored-$U_t$ cross-check:* Every leaf satisfies $U_{\mathrm{recomp}} \le U_{\mathrm{stored}}$ (`U_stored - U_recomp` $\approx 2.0 \times 10^{-11}$), and evaluating leaf bounds with $U_{\mathrm{stored}}$ gives **`-0.001000001000007235 <= -1/1000`**, reproducing `-0.001000001000007` in `inputs/REPORT.md` line 11.
- **Strict Cutoff Check $q_* \ge B_{03}$:** Verified in 160-bit Arb on **all `759 / 759` occupancy leaves**, with $\min(q_* - B_{03}) \ge +7.814076246073 \times 10^{-4} > 0$ (`verify.log` line 10). All `759` occupancy leaves have $q_* < \min(a_{0,\max}, a_{3,\max})$ and pass both near (`max = -0.0010152779776830`) and binary-KL tail (`max = -0.0010000010201557`) checks.

---

## 4. Referee Controls (`controls_referee.py` -> `controls.log`)

1. **Direct Numeric Rate Verification on `1,518` Feasible $(a, Q)$ Pairs (`controls.log` lines 4–8):**
   - Generated `759` near pairs ($Q_{03} \le q_*$) and `759` tail pairs ($Q_{03} > q_*$) across all `759` accepted occupancy leaves using exact `Fraction` arithmetic (verified in `Region C`, inside leaf box, symmetric nonnegative $Q$ with zero red entries and exact row sums $a$).
   - Every pair satisfied `true_rate <= recomputed_leaf_bound <= -1/1000` in 160-bit Arb (`max_true_near = -0.088898994636`, `max_true_tail = -0.118960367157`, minimum slack $+8.7899 \times 10^{-2}$ near / $+9.8555 \times 10^{-2}$ tail-$L$).
2. **Positive Naive Witness at $d = 10$ & Reversed-Cutoff Regression (`controls.log` lines 10–17):**
   - Constructed exact rational $a_{\mathrm{wit}} = (2/5, 138841/10^9, 2/5, 187117283/10^9, 3185969/250000000) \in \text{Region C}$ and exact symmetric blue $Q_{\mathrm{wit}}$, certifying in 160-bit Arb:
     $$L(a_{\mathrm{wit}}, Q_{\mathrm{wit}}) = [+0.0033635269510218... \pm 5.74 \times 10^{-46}] > +0.0033635265 > +0.00336.$$
   - Located covering leaf `record[716]` (`kind='C'`); mutating `record[716]` to `'N'` was **REJECTED** (`exit=1`, recomputed $U = +0.010952254 > -0.001$), confirming Case I occupancy is indispensable. Meanwhile true Case I rate $L + g = -0.017165431 < -0.001$.
   - Confirmed the old reversed lower-cutoff formula $g(a_{0,\max}, 1/20) = -0.122189512$ underestimates true $g(a_0, Q_{03}) = -0.020528958$ by $+0.101660554$ (unsafe direction).
3. **10/10 Subprocess Corruption Controls Rejected (`controls.log` lines 19–29):**
   - Clean copy accepted (`exit=0`); **10/10** corrupted archives rejected (`exit=1`):
     - `mutant_1a_perturbed_tilt_raw` (`understates recomputed U` on `record[2699]`)
     - `mutant_1b_perturbed_tilt_adjusted_U` (`recomputed tail bound +0.0003589 exceeds -1/1000` on `record[2699]`, proving zero reliance on stored $U$)
     - `mutant_2_cutoff_below_B03` (surgical $q_* = 0.01800 < B_{03} = 0.07200$ on `record[22]` where both near and wrong-side KL expressions stay $< -0.001$, rejected specifically by `q_* >= B_03`)
     - `mutant_3_altered_root_boundary` (`Root box mismatch`)
     - `mutant_4_non_interior_split` (`Non-interior split at index 0`)
     - `mutant_5_deleted_leaf` (`Truncated record stream at index 3048`)
     - `mutant_6_trailing_record` (`Trailing records after tree completion: consumed 3049 of 3050`)
     - `mutant_7_inflated_global_claim` (`Top-level claim -999/1000000 exceeds required target -1/1000`)
     - `mutant_8_inflated_stored_U` (`C leaf 2699 tail bound ... exceeds leaf claim`)
     - `mutant_9_legacy_format_1` (`Invalid Case I format 1: expected exact int 2`)

---

## 5. Mandatory Referee Audit Answers & Verdict

- **CONTROLS:** No — no assumption overrode what the controls show. Checked in `controls.log` lines 4–29 and `verify.log` lines 8–18 via `OPENBLAS_NUM_THREADS=1 nice -n 10 /Users/ricardo/dev/open-science/.venv/bin/python -B controls_referee.py`: all `1,518` feasible $(a, Q)$ pairs (`759` near + `759` tail) satisfied `true_rate <= recomputed_leaf_bound <= -0.001`; the $d = 10$ bare positive witness (`L = +0.00336352695 > +0.00336` at `controls.log` line 12) was rejected under a naive leaf check (`record[716]`, $U = +0.01095225$, line 16); the old lower-cutoff formula failed by `+0.101660554` (line 17); and `10/10` corrupted certificates exited `1` (`controls.log` lines 19–29), including surgical `mutant_2_cutoff_below_B03` (line 22).
- **CONTRADICTING:** No — no contradicting region, tail, or counterexample was dropped or ignored. Checked in `controls.log` lines 5–17, `verify.log` lines 9–15, `finite.log` lines 6–15, and `inputs/LEMMAS.md` lines 24 & 115: the positive bare first-moment region in C (`+0.00336352695`) is covered by occupancy leaf `record[716]` (`L + g = -0.0171654 < -0.001`); all `759` upper-tail cells ($Q_{03} > q_*$) are certified alongside all `759` near cells ($Q_{03} \le q_*$); and the finite sum in `finite.log` counts all $(n+1)^4$ profiles, all $(10n+1)^5$ symmetric blue matrices $K$ (zero typical-$K$ truncation), and all $10n+1$ Case II hot counts $R$.
- **LABELS:** No — no stored certificate bound or pre-assigned label was trusted without checking raw data. Checked in `arb_case1_referee.py` lines 78–103 & 330–710, `controls_referee.py` lines 51–73 & 185–278, `verify.log` lines 2–16, and `controls.log` lines 4–29: SHA-256 hashes were computed over raw archive bytes; `arb_case1_referee.py` recomputed $U_t$, $B_{03}$, occupancy, and binary-KL bounds from scratch on both `15,523` outer sliced-box vertices and `15,446` exact Region C polytope vertices; and `controls_referee.py` checked symmetry, nonnegativity, red-pair zeros, and exact row sums on every $Q$ before classifying near vs. tail directly from $Q_{03} \le q_*$ vs. $Q_{03} > q_*$.

**VERDICT: HOLDS**

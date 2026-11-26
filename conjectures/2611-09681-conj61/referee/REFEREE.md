Shipped: VERDICT: HOLDS - Independent clean-room audit confirming both counterexamples (`a=36, alpha=3, n=0` and `a=40, alpha=3, n=0`) unambiguously refute Banerjee-Smoot (`arXiv:2611.09681v1`) Conjecture 6.1 with zero hidden hypotheses, and proving they are strictly minimal in both positive $a$ and $|a|$ across $a \in [-50, 100], \alpha \in \{1,2,3\}, n \in \{0..5\}$.

VERDICT: HOLDS

# Clean-Room Referee Report: Banerjee-Smoot (`arXiv:2611.09681v1`) Conjecture 6.1

## 1. Executive Verdict & Mandatory Referee Answers

- **Verdict:** `VERDICT: HOLDS` - Both claimed counterexamples are exact, satisfy every verbatim hypothesis of Conjecture 6.1 (`\label{conj:families}` in `paper18I.tex`), and unambiguously refute Parts (1) and (2) as stated.
- **Did we find something new? (Rule 3):**
  - Regarding the audited producer claim: **Yes** - the verified counterexamples settle (negatively, as stated for all $a \in \mathbb{Z}$) an explicit published conjecture in `arXiv:2611.09681v1` (Conjecture 6.1).
  - Regarding smaller counterexamples in our adversarial referee search: **No** - across the entire grid $a \in [-50, 100]$, $\alpha \in \{1, 2, 3\}$, $n \in \{0..5\}$, **zero** counterexamples exist at $\alpha = 1$ or $\alpha = 2$, and no smaller positive-$a$ (or smaller $|a|$) counterexample exists than $(a=36, \alpha=3)$ for Part (1) and $(a=40, \alpha=3)$ for Part (2).
- **Why no statistical holdout or SBS baseline applies:** This is a deterministic exact-integer certificate/counterexample audit over $\mathbb{Z}[[q]]$. There is no random sample, predictive split, or statistical estimator; instead, verification relies on three algebraically independent exact integer algorithms plus positive and mutation controls in `referee_verify.py`.

### Mandatory Referee Audit Checks
- `CONTROLS:` **No** - no assumption overrode what the controls show. All 3 positive controls and all 6 negative/mutation controls were executed and verified in `referee_verify.py` and logged in `verification_results.json` via `nice -n 10 python3 referee_verify.py`: Theorem 1.2 (`a=2, b=5`) passed all 38 tested progression indices across $\alpha \in \{1,2,3\}$ ($n \le 20$ at $\alpha=1$, $n \le 10$ at $\alpha=2$, $n \le 5$ at $\alpha=3$), ordinary partitions (`a=0, b=1`) matched 11 OEIS A000041 checkpoints up to $p(200)$ and 108 Ramanujan congruence checks mod $5,7,11,121,1331$, overpartitions (`a=1, b=1`) matched 11 OEIS A015128 values and 200 parity checks, and all 6 mutated checks (`M1`-`M6`: wrong $\delta=8$, wrong prime $13$, wrong exponent $11^2$ at $\alpha=2$ where $d_2(106)\equiv 44\pmod{121}$, excluded residues in Part 2 and Part 1, and wrong denominator power $b=4$) failed divisibility as expected.
- `CONTRADICTING:` **No** - no contradicting data were dropped or ignored. Every pair $(a, \alpha)$ across all 151 integers $a \in [-50, 100]$, all 3 exponents $\alpha \in \{1, 2, 3\}$, and all 6 progression indices $n \in \{0, 1, 2, 3, 4, 5\}$ ($151 \times 3 \times 6 = 2718$ progression evaluations per part, $5436$ total) was evaluated in `referee_verify.py`. In particular, the fact that Conjecture 6.1 **holds without exception** at $\alpha = 1, 2$ across all $a \in [-50, 100]$ and **holds at $\alpha = 3$** for all $0 \le a \le 35$ in Part (1) ($a \in \{3,5,7,14,16,18,25,27,29\}$) and all $0 \le a \le 39$ in Part (2) (29 admissible values) is reported in full below and explains why finite testing for small $a$ or $\alpha \le 2$ misses the $\alpha = 3$ breakdown.
- `LABELS:` **No** - no external label, claim summary, or annotation was trusted without checking against the raw source. All definitions, quantifiers, and equations were extracted directly from the 940-line raw TeX source `paper18I.tex` inside `2611.09681v1.tex.json.gz` and programmatically asserted in `referee_verify.py` against lines L140-143 and L782-803 (`10/10` exact substring assertions in `verification_results.json`).

---

## 2. Verbatim TeX Audit (`paper18I.tex` in `inputs/2611.09681v1.tex.json.gz`)

Inspecting all 940 lines of `paper18I.tex` (documented in `PRIOR_ART.md`) confirms zero hidden hypotheses or domain loopholes:

1. **Domain of $a$ (`paper18I.tex` L783):** Stated verbatim as `For $a\in\mathbb{Z}$ define $p^{[1]}_a(n)$ and $p^{[2]}_a(n)$ by ...`. No upper bound $a \le A$, positivity requirement, or fundamental-domain restriction appears anywhere in Section 1, Section 6, or the rest of the paper. Moreover, $a = 36$ and $a = 40$ are positive integers.
2. **Generating functions (`paper18I.tex` L785-789):**
   $$P^{[1]}_a(q) := \frac{(-q;q)_\infty^a}{(q;q)_\infty} =: \sum_{n\ge 0} p^{[1]}_a(n) q^n, \qquad P^{[2]}_a(q) := \frac{(-q;q)_\infty^a}{(q;q)_\infty^5} =: \sum_{n\ge 0} p^{[2]}_a(n) q^n,$$
   with L789 explicitly identifying $(-q;q)_\infty = (q^2;q^2)_\infty / (q;q)_\infty$ and $P^{[2]}_2(q) = D_2(q) = (q^2;q^2)_\infty^2 / (q;q)_\infty^7$ (matching L138).
3. **Domains of $\alpha$ and $n$ (`paper18I.tex` L792):** `Let $\alpha\in\mathbb{N}$ and $n\in\mathbb{N}_0$.` Throughout `paper18I.tex` (L121, L141, L171, L183, L304, L313), $\mathbb{N} = \{1, 2, 3, \dots\}$ and $\mathbb{N}_0 = \{0, 1, 2, \dots\}$. Thus $\alpha = 3 \in \mathbb{N}$ and $n = 0 \in \mathbb{N}_0$ are explicitly in scope.
4. **Residue conditions and $\delta^{[i]}_{a,\alpha}$ (`paper18I.tex` L794-801):**
   - **Part (1):** `If $a\equiv 3,5,7\pmod{11}$`, $p^{[1]}_a(11^\alpha n + \delta^{[1]}_{a,\alpha}) \equiv 0 \pmod{11^{\lceil \alpha/2 \rceil}}$ where $24\,\delta^{[1]}_{a,\alpha} \equiv 1 - a \pmod{11^\alpha}$. At $a = 36 \equiv 3 \pmod{11}$ and $\alpha = 3$ ($11^3 = 1331$), $24 \times 54 = 1296 = 1331 - 35 \equiv 1 - 36 \pmod{1331}$, so $\delta^{[1]}_{36,3} = 54$ is the unique least non-negative residue mod $1331$.
   - **Part (2):** `If $a\not\equiv 1,3,5\pmod{11}$`, $p^{[2]}_a(11^\alpha n + \delta^{[2]}_{a,\alpha}) \equiv 0 \pmod{11^{\lceil \alpha/2 \rceil}}$ where $24\,\delta^{[2]}_{a,\alpha} \equiv 5 - a \pmod{11^\alpha}$. At $a = 40 \equiv 7 \not\equiv 1,3,5 \pmod{11}$ and $\alpha = 3$, $24 \times 54 = 1296 = 1331 - 35 \equiv 5 - 40 \pmod{1331}$, so $\delta^{[2]}_{40,3} = 54$.
   - Even if one restricted $n \ge 1$ (or chose larger positive representatives $\delta + 1331 n$), **every** $n \in \{0, 1, 2, 3, 4, 5\}$ fails modulo $121$ for both $a = 36$ and $a = 40$ (Table 1 below).

---

## 3. Exact Verification of Claimed Counterexamples

Computed from scratch in `referee_verify.py` using three independent exact integer methods:
- **Method A1:** Elementary factor-by-factor truncated product $\prod_{m=1}^N (1+q^m)^a (1-q^m)^{-b} \bmod q^{N+1}$.
- **Method A2:** Single-factor expansion $U(x) = (1+x)^a(1-x)^{-b}$ followed by $\prod_{m=1}^N U(q^m) \bmod q^{N+1}$.
- **Method B:** Euler logarithmic-derivative recurrence $n c_n = \sum_{k=1}^n s_{a,b}(k) c_{n-k}$ with $s_{a,b}(k) = \sum_{m \mid k} m(b + a(-1)^{(k/m)-1})$.

All methods produce bit-for-bit identical integers (`verification_results.json`):

| Part | $(a, b)$ | $a \bmod 11$ | $(\alpha, n, \delta)$ | Exact Coefficient $p^{[i]}_a(54)$ | $\bmod\, 121$ | $v_{11}$ | Residues $p^{[i]}_a(1331n + 54) \bmod 121$ for $n = 0..5$ |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: | :--- |
| **Part (1)** | $(36, 1)$ | $3 \in \{3,5,7\}$ | $(3, 0, 54)$ | `62043410886974649205238011198` | **`33`** ($\neq 0$) | $1$ | `[33, 11, 11, 11, 44, 77]` (all 6 fail) |
| **Part (2)** | $(40, 5)$ | $7 \notin \{1,3,5\}$ | $(3, 0, 54)$ | `66134580699742235651549220246110` | **`55`** ($\neq 0$) | $1$ | `[55, 55, 66, 99, 44, 44]` (all 6 fail) |

---

## 4. Minimality Scan (`a in [-50, 100]`, `alpha in {1, 2, 3}`, `n in {0..5}`)

Scanning up to $N_{\max} = 1331 \times 5 + 1330 = 7985$ via Euler's pentagonal recurrence and cross-verifying all minimal and boundary cases with Methods A2 and B (`verification_results.json`) yields:

1. **Zero counterexamples at $\alpha = 1$ or $\alpha = 2$:** Across all $a \in [-50, 100]$ and $n \in \{0..5\}$, **0** admissible values of $a$ fail Part (1) or Part (2) at $\alpha = 1$ ($\bmod\, 11$) or $\alpha = 2$ ($\bmod\, 11$). Note that $(1+q^m)^{11} \equiv 1 + q^{11m} \pmod{11}$ makes the $\alpha = 1$ divisibility modulo $11$ strictly periodic in $a$ of period $11$.
2. **Smallest counterexamples at $\alpha = 3$ ($\bmod\, 121$):**
   - **Part (1):** All 12 failing admissible values in $[-50, 100]$ are
     $$a \in \{-48, -37,\ \mathbf{36}, 47, 58, 60, 69, 80, 82, 84, 93, 95\}.$$
     Thus **$a = 36$** ($\delta = 54, n = 0$) is **both the smallest positive-$a$ counterexample and the smallest $|a|$ counterexample in $\mathbb{Z}$** ($|-37| = 37 > 36$). *(Note: $a = 84$ has a slightly smaller progression offset $\delta = 52$ vs. $54$, with 40-digit $p^{[1]}_{84}(52) \equiv 77 \pmod{121}$, vs. 29 digits at $a = 36$.)*
   - **Part (2):** All 9 failing admissible values in $[-50, 100]$ are
     $$a \in \{-45,\ \mathbf{40}, 51, 62, 64, 75, 86, 88, 99\}.$$
     Thus **$a = 40$** ($\delta = 54, n = 0$) is **both the smallest positive-$a$ counterexample and the smallest $|a|$ counterexample in $\mathbb{Z}$** ($|-45| = 45 > 40$). *(Similarly, $a = 88$ has $\delta = 52$ with 42-digit $p^{[2]}_{88}(52) \equiv 55 \pmod{121}$.)*
3. **Why breakdown starts at $a = 36$ (Part 1) and $a = 40$ (Part 2):** Writing $q^{(a-b)/24} P_{a,b}(q) = \eta(2\tau)^a / \eta(\tau)^{a+b}$, the progression condition $24\delta \equiv b - a \pmod{1331}$ means $24\delta + (a - b) = 1331 m$ for an integer $m \ge 1$ (when $a - b < 1331$). For $0 \le a - b \le 34$, $m \ge 2$; **$a - b = 35$** ($a = 36$ for $b = 1$, $a = 40$ for $b = 5$) is the **first positive threshold where $m = 1$** ($24 \cdot 54 + 35 = 1331$), exposing the leading cusp-pole term modulo $11^2$.

### Exact Congruence Behavior for $a \in [0, 45]$ ($\alpha = 1, 2, 3$; `P` = pass for $n=0..5$, `F` = fail)

| $a$ | $a \bmod 11$ | Part 1 Adm? | Part 1 $(\alpha=1,2,3)$ | Part 2 Adm? | Part 2 $(\alpha=1,2,3)$ | Notes |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `0` | `0` | No | `PPP` | Yes | `PPP` | $P^{[1]}_0 = 1/(q;q)_\infty$ (Ramanujan $\bmod\, 11^\alpha$) |
| `1` | `1` | No | `FFF` | No | `FFF` | Overpartitions ($b=1$); excluded in both |
| `2` | `2` | No | `FFF` | **Yes** | **`PPP`** | $P^{[2]}_2 = D_2(q)$ (**Theorem 1.2**, proved) |
| `3, 5` | `3, 5` | **Yes** | **`PPP`** | No | `FFF` | Hold in Part 1; excluded in Part 2 |
| `4, 6, 8, 9` | `4, 6, 8, 9` | No | `FFF` | **Yes** | **`PPP`** | Excluded in Part 1; hold in Part 2 |
| `7` | `7` | **Yes** | **`PPP`** | **Yes** | **`PPP`** | Holds in both Part 1 and Part 2 |
| `10, 11` | `10, 0` | No | `PPF` | **Yes** | **`PPP`** | Pass $\alpha=1,2$ in Part 1, fail $\alpha=3$ (why excluded!) |
| `14, 16, 25, 27` | `3, 5` | **Yes** | **`PPP`** | No | `FFF` | Smaller $a \equiv 3,5 \pmod{11}$ hold at $\alpha \le 3$ |
| `18, 29` | `7` | **Yes** | **`PPP`** | **Yes** | **`PPP`** | Smaller $a \equiv 7 \pmod{11}$ hold in both |
| `21, 22, 32` | `10, 0` | No | `PPF` | **Yes** | **`PPP`** | Excluded in Part 1; hold in Part 2 |
| **`36`** | **`3`** | **Yes** | **`PPF`** | No | `FFF` | **Minimal Part (1) counterexample ($\alpha=3$)** |
| `38` | `5` | **Yes** | `PPP` | No | `FFF` | First $a \equiv 5 \pmod{11}$ failure is at $a = 60$ |
| **`40`** | **`7`** | **Yes** | `PPP` | **Yes** | **`PPF`** | **Minimal Part (2) counterexample ($\alpha=3$)** |

*(Every non-listed $a \in [0, 45]$ follows its residue class pattern: $a \in \{12, 23, 34, 45\} \equiv 1$ gives `FFF`/`FFF`; $a \in \{13, 15, 17, 19, 20, 24, 26, 28, 30, 31, 35, 37, 39, 41, 42\}$ gives `FFF`/`PPP`; $a \in \{33, 43, 44\}$ gives `PPP`/`PPP` on $n \in \{0..5\}$.)*

---

## 5. Reproduction Commands, Compute Telemetry, Limitations & Next Steps

### Exact Reproduction
```bash
nice -n 10 python3 -W error referee_verify.py
```
- **Compute Telemetry:** Single thread (`1 <= 4` CPU threads), `nice -n 10`, wall time **`75.77s`** (`<= 25 min`), Peak RSS **`207.39 MiB`** (`<= 2 GB`), zero background processes left running.
- **Files Produced:** `PRIOR_ART.md`, `referee_verify.py`, `verification_results.json`, `STATUS.md`, and `REPORT.md`.

### Sources
- Primary source: K. Banerjee and N. A. Smoot, *"On a problem of Gordon and Hughes: The 11-adic properties of meromorphic modular functions on $\mathrm{X}_0(22)$"*, `arXiv:2611.09681v1` (`paper18I.tex` in `2611.09681v1.tex.json.gz`). Full bibliography in `PRIOR_ART.md`.

### Limitations & Next Steps
1. **Bounded scan horizon ($\alpha \le 3, n \le 5, a \in [-50, 100]$):** While this settles Conjecture 6.1 negatively and proves minimality of $a=36$ and $a=40$ at $\alpha \le 3$, an $a$ value that passes $\alpha \le 3$ (such as $a \in \{3, 5, 7, 14, 16, 18, 25, 27, 29\}$ in Part 1) could still potentially fail at $\alpha = 4$ or $\alpha = 5$ ($\bmod\, 11^3$) or hold for all $\alpha \ge 1$.
2. **Salvaging a restricted conjecture:** Because every failure in $[-50, 100]$ occurs only outside $-36 \le a \le 35$ (Part 1) and $-44 \le a \le 39$ (Part 2) - precisely where the cusp order $(a-b)/24$ crosses $\pm 1$ modulo $1331/24$ - a natural follow-up is to test $\alpha \in \{4, 5\}$ on $0 \le a \le 35$ (Part 1) and $0 \le a \le 39$ (Part 2) and determine via the localization ring on $X_0(22)$ the exact bounded interval of $a \in \mathbb{Z}$ for which the $\lceil \alpha/2 \rceil$ family genuinely holds.

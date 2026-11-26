Shipped: VERDICT: HOLDS  --  independent clean-room mathematical audit confirms that `inputs/PROOF.md` proves all four Section 6 conjectures (`conj:A2adic`, `conj:B2adic`, `conj:A6`, `conj:deep`) of Yaqubi & Mirzavaziri (`arXiv:2611.05623v1`) with zero deductive, modular-form, or arithmetic gaps.

VERDICT: HOLDS

---

## 1. Executive Summary & Novelty Assessment

- **Overall Verdict:** `VERDICT: HOLDS` across all four Section 6 conjectures of `arXiv:2611.05623v1` (`2611.05623v1.tex.json.gz`, `designated_k_tuples_v4.tex`, lines 908-931), audited against `PROOF.md` (lines 1-73) in strict clean-room isolation.
- **Rule 3 ("Did you find something new? Yes or no."):** As an adversarial referee job, we make no new mathematical claim of our own beyond certifying (and supplying a self-contained $M_{12}(\Gamma_0(24))$ Sturm proof of the cited Hirschhorn $f_1 f_3$ identity for) the producer's proof. Regarding the producer's result: **yes**  --  `PROOF.md` settles all four stated open conjectures in Section 6 of `arXiv:2611.05623v1` under the exact definitions of the paper.
- **Rule 2 Note (Predictive Baselines):** No statistical or predictive model/score is claimed; this is an exact deductive proof and finite integer certificate audit, so no statistical holdout or `BASELINES.json` applies.

| Conjecture | TeX Location | Statement Summary | Proof Method in `PROOF.md` | Audit & Certificate Status |
|---|---|---|---|---|
| `conj:A2adic` | Lines 908-910 | Exact power of $2$ dividing all $A_k(4n+3)$ is $2^{v_2(A_k(3))}$ if $k\not\equiv 2\pmod{16}$, else $2^3$ | Double Frobenius mod $2^{s-1}$ on $F^{k+1}$ + exact dissection of $F^{-1}$; mod-$64$ periodicity of $A_k(7)\bmod{16}$ for $k\equiv 2\pmod{16}$ | **HOLDS** (gap-free for all $k\ge 1$) |
| `conj:B2adic` | Lines 912-914 | Exact power of $2$ dividing all $B_k(4n+3)$ is $2^{v_2(B_k(3))}$, except $2^2$ ($k\equiv 1\pmod 8$) and $2^3$ ($k\equiv 6\pmod 8$) | Frobenius + paper's Theorems `pdo2`, `pdo4`, `pdo4exact` + mod-$64$ periodicity of $B_k(7)\bmod 8$ for $k\equiv 9\pmod{16}$ | **HOLDS** (gap-free for all $k\ge 1$) |
| `conj:A6` | Lines 920-922 | $A_6(12n+10)\equiv 0\pmod{3^5}$ for all $n\ge 0$, and $3^5$ is exact | Clearing factor $\Delta(12z)^5 F^6 \in M_{54}(\Gamma_0(72))$, phase projection onto $\Gamma_0(144)$, Sturm bound $B=1296$ ($J=102$), sharp witness $A_6(22)$ | **HOLDS** (103/103 terms $\equiv 0\pmod{243}$, $v_3(A_6(22))=5$) |
| `conj:deep` | Lines 925-931 | $A_3(12n+7), A_3(12n+11)\equiv 0\pmod{3^4}$; $A_4(6n+5), A_7(12n+11)\equiv 0\pmod{3^3}$; $A_8(18n+15)\equiv 0\pmod{3^5}$ | Clearing factors $\Delta(mz)^H F^k$ at level $72$, sifting to $\Gamma\subseteq\Gamma_0(L)$, Sturm bounds up to $B=12096$ ($J=661$) | **HOLDS** (all 5 progressions + sharpness witnesses verified) |

---

## 2. Mandatory Referee Checks (`CONTROLS`, `CONTRADICTING`, `LABELS`)

- `CONTROLS:` **No**  --  no assumption overrode what the controls show. Checked in `referee_verify.py` via command `nice -n 10 python3 -B referee_verify.py`: all **4 of 4** positive controls (reproducing proved Theorems 3.3, 3.7, 3.9(d), and 4.3 of `designated_k_tuples_v4.tex`) passed, and all **8 of 8** negative/mutation controls were caught (`M1`: raising $e \mapsto e+1$ refuted on all 6 rows within $0\le n\le J$; `M2`: shifting $r=10\mapsto 11$ on $A_6(12n+r)\bmod 3^5$ refuted; `M3`: lowering $H \mapsto H-1$ produced strictly negative Ligozat cusp orders at $c=1$ on all 6 rows; `M4`: non-invariant residue $(k=8,m=18,r=1)$ rejected by $r(a^2-1)\equiv 0\pmod{18}$ at $a=5$; `M5`: flipping $-q \mapsto +q$ in $F^{-1}$ failed $F\cdot F^{-1}=1$; `M6` & `M7`: naive $v_2(A_2(3))=4$ and $v_2(B_9(3))=3$ refuted at $n=1$ where $v_2(A_2(7))=3$ and $v_2(B_9(7))=2$; `M8`: under-truncated $n=0$ check on $A_6(12n+10)\bmod 3^6$ falsely passes $A_6(10)=384183$ ($v_3=6$) and is caught at $n=1$ by $A_6(22)=6635911068$ ($v_3=5$)).
- `CONTRADICTING:` **No**  --  no contradicting cases, residue classes, cusps, or exceptional indices were dropped or ignored. Checked exhaustively across: (i) all **16 of 16** residue classes of $k\bmod 16$ for `conj:A2adic` and all **8 of 8** residue classes of $k\bmod 8$ (split to $1\bmod 16$ and $9\bmod 16$) for `conj:B2adic`, plus **41** explicit parameter values $k\in\{1,\dots,34,41,50,57,62,64,66,128\}$ across $0\le n\le 60$ ($2501$ progression terms per family) in `referee_verify.py`; (ii) all **12 of 12** cusp denominators $c\mid 72$ (and all $72$ residues $1\le c\le 72$) in `referee_verify.py`; and (iii) all $\sum (J+1) = 103+129+129+38+254+662 = 1315$ progression coefficients (up to degree $N_{\max}=11913$) in `referee_verify.py`, including the over-divisible initial term $v_3(A_6(10))=6>5$ resolved by $v_3(A_6(22))=5$.
- `LABELS:` **No**  --  no theorem label, definition, formula, or table entry in `PROOF.md` was trusted without checking it verbatim against the raw TeX source `designated_k_tuples_v4.tex` inside `2611.05623v1.tex.json.gz` (all 997 lines inspected; documented in `PRIOR_ART.md`): `Definition 2.1` (lines 137-143), `lem:frob` (lines 149-153), `thm:frob` (lines 214-219), `lem:odd` (lines 412-426), `thm:mod2` (lines 427-464), `prop:A3` (lines 465-471), `thm:pdo2` (lines 727-762), `thm:pdo4` and Hirschhorn's $f_1 f_3$ identity (lines 776-801), `thm:pdo4exact` (lines 802-829), and `conj:A2adic`, `conj:B2adic`, `conj:A6`, `conj:deep` (lines 908-931). Moreover, $A_k(n)$ and $B_k(n)$ were cross-checked across three independent clean-room implementations in `referee_verify.py` (sparse pentagonal recurrences, Euler logarithmic-derivative divisor recurrences up to degree 400, and combinatorial part-size products up to degree 25).

---

## 3. Line-by-Line Audit of `conj:A2adic` and `conj:B2adic` (`PROOF.md`)

### 3.1 Self-Contained Proof & Verification of the $f_1 f_3$ and $F^{-1}$ Dissections
- `PROOF.md` multiplies Hirschhorn's 2-dissection (`designated_k_tuples_v4.tex`, lines 795-797)
  $$f_1 f_3 = \frac{f_2 f_8^2 f_{12}^4}{f_4^2 f_6 f_{24}^2} - q \frac{f_4^4 f_6 f_{24}^2}{f_2 f_8^2 f_{12}^2}$$
  by $f_2 / f_6$ to obtain
  $$F^{-1} = \frac{f_1 f_2 f_3}{f_6} = \frac{f_2^2 f_8^2 f_{12}^4}{f_4^2 f_6^2 f_{24}^2} - q \frac{f_4^4 f_{24}^2}{f_8^2 f_{12}^2}.$$
- **Independent proof from scratch:** Substituting $\eta(dz)=q^{d/24}f_d$, all three terms of the $f_1 f_3$ identity carry exact $q$-shift $q^{1/6}$ ($1+3=4$, $2+16+48-8-6-48=4$, $16+6+48-2-16-24=28=24+4$). Clearing all denominators yields $A(z) = B(z) - C(z)$ where $A = \eta_1\eta_2\eta_3\eta_4^2\eta_6\eta_8^2\eta_{12}^2\eta_{24}^2$, $B = \eta_2^2\eta_8^4\eta_{12}^6$, $C = \eta_4^6\eta_6^2\eta_{24}^4$. Squaring gives four holomorphic eta-products $A^2, B^2, BC, C^2$ with nonnegative exponents, integer weight $w = 24/2 = 12$, $\sum \delta r_\delta \in \{216, 240, 264\} \equiv 0 \pmod{24}$, $\sum (24/\delta) r_\delta \in \{144, 96\} \equiv 0 \pmod{24}$, and even exponents (hence trivial character on $\Gamma_0(24)$). Since $[\mathrm{SL}_2(\mathbb{Z}):\Gamma_0(24)] = 48$, Sturm's bound on $M_{12}(\Gamma_0(24))$ is $B = 48$; equality of $A^2$ and $(B-C)^2$ through $q^{48}$ (verified through $O(q^{300})$ in `referee_verify.py`) proves $A = B - C$ in the integral domain $\mathbb{Z}[[q]]$ since both have leading coefficient $+1$.
- **Support check on $F^{-1}$:** In the second term of $F^{-1}$, both $f_2$ and $f_6$ cancel identically, leaving $-q f_4^4 f_{24}^2 / (f_8^2 f_{12}^2) \in q\mathbb{Z}[[q^4]]$ (supported strictly on $1\bmod 4$), while the first term lies in $\mathbb{Z}[[q^2]]$ (supported on $0,2\bmod 4$). Thus $[q^{4n+3}]F^{-1} = 0$ for all $n\ge 0$.

### 3.2 Audit of the Mod-$2^{s-1}$ Double-Frobenius Transfer (No Mod-2 Lift Bug)
- For odd $k \ge 1$, let $s = v_2(k+1) \ge 1$. Since $A_k(3) = k(k+1)(k+14)/6$ has $k$ and $k+14$ odd, $v_2(A_k(3)) = s - 1$, giving an immediate sharpness witness at $n = 0$ for every odd $k$.
- When $s = 1$ ($k \equiv 1 \pmod 4$), $s - 1 = 0$, so divisibility by $2^0 = 1$ is trivial.
- When $s \ge 2$ ($k \equiv 3 \pmod 4$), Lemma `lem:frob` ($H(q)^{2^j} \equiv H(q^2)^{2^{j-1}} \pmod{2^j}$, valid for all $j \ge 1$ because $2j \ge j+1$) gives:
  1. $j = s \ge 2$: $F(q)^{2^s} \equiv F(q^2)^{2^{s-1}} \pmod{2^s}$, hence a fortiori $\pmod{2^{s-1}}$.
  2. $j = s - 1 \ge 1$ (evaluated at $q \mapsto q^2$): $F(q^2)^{2^{s-1}} \equiv F(q^4)^{2^{s-2}} \pmod{2^{s-1}}$.
  Writing $k + 1 = 2^s t$ ($t \ge 1$ odd) and raising the congruence in $(\mathbb{Z}/2^{s-1}\mathbb{Z})[[q]]$ to the $t$-th power gives $F(q)^{k+1} \equiv F(q^4)^{2^{s-2} t} \in \mathbb{Z}[[q^4]] \pmod{2^{s-1}}$. Multiplying by $F^{-1}$ (supported on $\{0, 1, 2\} \bmod 4$) yields $[q^{4n+3}]F^k \equiv 0 \pmod{2^{s-1}}$ for all $n \ge 0$. Every modulus drop is exact.

### 3.3 Exhaustive Residue-Class Coverage & Edge-Case Verification (`conj:A2adic` & `conj:B2adic`)
- **`conj:A2adic` ($k \bmod 16$):**
  - Odd $k$ ($1,3,5,7,9,11,13,15 \bmod 16$): exact exponent $v_2(k+1) - 1 = v_2(A_k(3))$, attained at $n=0$.
  - $4 \mid k$ ($0,4,8,12 \bmod 16$): $v_2(A_k(3)) = v_2(k) + 0 + 1 - 1 = v_2(k)$; Theorem `thm:frob` gives $2^{v_2(k)} \mid A_k(2m+1)$, attained at $n=0$.
  - $k \equiv 6 \pmod 8$ ($6,14 \bmod 16$): Proposition `prop:A3` proves exact exponent $2 = v_2(A_k(3))$, attained at $n=0$.
  - $k \equiv 10 \pmod{16}$: Theorem `thm:mod2(c)` gives $2^3 \mid A_k(4n+3)$, and $v_2(k+14) = 3 \implies v_2(A_k(3)) = 1 + 0 + 3 - 1 = 3$, attained at $n=0$.
  - $k \equiv 2 \pmod{16}$: Theorem `thm:mod2(c)` gives $2^3 \mid A_k(4n+3)$. Since $F - 1 \in q\mathbb{Z}[[q]]$ and $v_2\binom{64}{j} = 6 - v_2(j) \ge 4$ for $1 \le j \le 7$, $F^{64} \equiv 1 \pmod{(16, q^8)}$. Checking $k \in \{2, 18, 34, 50\}$ gives $A_2(7)=328$, $A_{18}(7)=2748312$, $A_{34}(7)=79541096$, $A_{50}(7)=713942200$, all $\equiv 8 \pmod{16}$ ($v_2 = 3$), establishing sharpness at $n=1$ for every $k \equiv 2 \pmod{16}$.
- **`conj:B2adic` ($k \bmod 8$):**
  - $4 \mid k$ ($0,4 \bmod 8$): $v_2(B_k(3)) = v_2(k) + 1 + 0 - 1 = v_2(k)$; Theorem `thm:frob` gives lower bound, $n=0$ gives sharpness.
  - $k \equiv 3 \pmod 4$ ($3,7 \bmod 8$): $v_2(B_k(3)) = 0 + 0 + 1 - 1 = 0$ (odd at $n=0$).
  - $k \equiv 5 \pmod 8$: $v_2(B_k(3)) = 1$; Theorem `thm:pdo2(b)` gives $2^1 \mid B_k(4n+3)$, sharp at $n=0$.
  - $k \equiv 2 \pmod 8$: $v_2(B_k(3)) = 2$; Theorem `thm:pdo2(c)` gives $2^2 \mid B_k(4n+3)$, sharp at $n=0$.
  - $k \equiv 6 \pmod 8$: Theorem `thm:pdo4exact` gives exact exponent $3$ ($n=0$ for $k\equiv 6\pmod{16}$; $n=1$ via $B_k(7)\equiv 8\pmod{16}$ for $k\in\{14,30,46,62\}$).
  - $k \equiv 1 \pmod 8$: Theorem `thm:pdo4(a)` gives $2^2 \mid B_k(4n+3)$. For $k \equiv 1 \pmod{16}$, $v_2(B_k(3)) = 2$ ($n=0$). For $k \equiv 9 \pmod{16}$, $G^{64} \equiv 1 \pmod{(16, q^8)}$, and $B_9(7)=45972$, $B_{25}(7)=8109100$, $B_{41}(7)=138388612$, $B_{57}(7)=1014953628$ all satisfy $B_k(7) \equiv 4 \pmod 8$ ($v_2 = 2$, sharp at $n=1$).

| Edge $k$ | $k \bmod 16$ | Exact $\min_n v_2(A_k(4n+3))$ | Witness $4n+3$ ($A_k(3), A_k(7)$) | Exact $\min_n v_2(B_k(4n+3))$ | Witness $4n+3$ ($B_k(3), B_k(7)$) |
|---:|---:|---:|---|---:|---|
| 1 | 1 | 0 | $3$ ($5, 41$) | 2 | $3$ ($4, 16$) |
| 2 | 2 | 3 | $7$ ($16, 328$) | 2 | $3$ ($12, 128$) |
| 3 | 3 | 1 | $3$ ($34, 1296$) | 0 | $3$ ($25, 516$) |
| 4 | 4 | 2 | $3$ ($60, 3708$) | 2 | $3$ ($44, 1508$) |
| 5 | 5 | 0 | $3$ ($95, 8770$) | 1 | $3$ ($70, 3640$) |
| 6 | 6 | 2 | $3$ ($140, 18264$) | 3 | $3$ ($104, 7728$) |
| 7 | 7 | 2 | $3$ ($196, 34700$) | 0 | $3$ ($147, 14953$) |
| 8 | 8 | 3 | $3$ ($264, 61488$) | 3 | $3$ ($200, 26960$) |
| 16 | 0 | 4 | $3$ ($1360, 1528640$) | 4 | $3$ ($1104, 751552$) |
| 17 | 1 | 0 | $3$ ($1581, 2064429$) | 2 | $3$ ($1292, 1027208$) |
| 18 | 2 | 3 | $7$ ($1824, 2748312$) | 2 | $3$ ($1500, 1383408$) |
| 32 | 0 | 5 | $3$ ($8096, 56911360$) | 5 | $3$ ($7072, 32585728$) |
| 34 | 2 | 3 | $7$ ($9520, 79541096$) | 2 | $3$ ($8364, 46208992$) |
| 128 | 0 | 7 | $3$ ($390784, 226225540096$) | 7 | $3$ ($374400, 177124207616$) |

---

## 4. Modular-Form, Cusp-Order & Sturm Audit of `conj:A6` and `conj:deep` (`PROOF.md`)

### 4.1 Newman-Gordon-Hughes-Ligozat Conditions on $D(z) = \Delta(mz)^H F(z)^k$ at Level $N = 72$
For each row $(k, m, r, e)$, $m \in \{6, 12, 18\}$ divides $72$, and $D(z) = \eta(mz)^{24H} \eta(z)^{-k}\eta(2z)^{-k}\eta(3z)^{-k}\eta(6z)^k$:
1. **Integer Positive Weight (No Half-Integer Trap):** Because $F = \eta_6/(\eta_1\eta_2\eta_3)$ has sum of exponents $-2$ (even), $w = \frac{1}{2}(24H - 2k) = 12H - k \in \mathbb{Z}_{>0}$ for **all** integer $k$ (including odd $k=3, 7$, giving $w=33, 65$).
2. **First Congruence ($\infty$-shift):** $\sum_{\delta\mid 72} \delta r_\delta = 24mH + (-1-2-3+6)k = 24mH \equiv 0 \pmod{24}$ (leading $q$-power $q^{mH}$).
3. **Second Congruence ($0$-shift):** $\sum_{\delta\mid 72} (72/\delta) r_\delta = 24(72/m)H - 120k = 24((72/m)H - 5k) \equiv 0 \pmod{24}$.
4. **Nebentypus Character & Exact Clearing Factor:** Since $\prod_{\delta\mid 72} \delta^{r_\delta} = m^{24H} (6/(1\cdot 2\cdot 3))^k = (m^{12H})^2$ is a square coprime to every $d$ with $\gcd(d,72)=1$, Ono Theorem 1.64 gives $\chi(d) = \left(\frac{(-1)^{12H-k}(m^{12H})^2}{d}\right) = \left(\frac{(-1)^k}{d}\right)$. Crucially, for negative odd $d = -|d|$ and odd $k$, the Kronecker symbol satisfies $\left(\frac{-1}{d}\right) = (-1)\cdot(-1)^{(|d|-1)/2} = \chi_{-4}(d)$, which equals $+1$ iff $d \equiv 1 \pmod 4$ (matching $(-I)^w$: $\chi(-1) = -1 = (-1)^w$). Furthermore, `PROOF.md` does **not** use the false congruence $\Delta(mz) \equiv \Delta(z)^m \pmod{3^e}$; instead, $\Delta(mz)^H = q^{mH} U(q^m)$ with $U \in 1 + q\mathbb{Z}[[q]]$ is kept **exact over $\mathbb{Z}$**, commuting cleanly through the $r \bmod m$ projection as an invertible series in $q^m$.

### 4.2 Exact Ligozat Cusp Orders at All 12 Divisors $c \mid 72$
Evaluating $\mathrm{ord}_{a/c}(D) = \frac{72}{24\,c\,\gcd(c, 72/c)} \sum_{\delta\mid 72} r_\delta \frac{\gcd(c,\delta)^2}{\delta}$ across every divisor $c \mid 72$:

| Row $(k,m,r,e)$ | $H$ | $c=1$ | $2$ | $3$ | $4$ | $6$ | $8$ | $9$ | $12$ | $18$ | $24$ | $36$ | $72$ | $H-1$ at $c=1$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $(6,12,10,5)$ | 5 | **0** | 18 | 24 | 54 | 30 | 54 | 24 | 60 | 30 | 60 | 60 | 60 | $-6$ |
| $(3,12,7,4)$ | 3 | **3** | 12 | 15 | 33 | 18 | 33 | 15 | 36 | 18 | 36 | 36 | 36 | $-3$ |
| $(3,12,11,4)$ | 3 | **3** | 12 | 15 | 33 | 18 | 33 | 15 | 36 | 18 | 36 | 36 | 36 | $-3$ |
| $(4,6,5,3)$ | 2 | **4** | 16 | 20 | 8 | 24 | 8 | 20 | 12 | 24 | 12 | 12 | 12 | $-8$ |
| $(7,12,11,3)$ | 6 | **1** | 22 | 29 | 65 | 36 | 65 | 29 | 72 | 36 | 72 | 72 | 72 | $-5$ |
| $(8,18,15,5)$ | 10 | **0** | 24 | 32 | 12 | 40 | 12 | 352 | 20 | 360 | 20 | 180 | 180 | $-4$ |

Every cusp order is a nonnegative integer, confirming $D \in M_w(\Gamma_0(72), \chi)$, and $H$ is minimal in every row.

### 4.3 Sifting Projection $P(z)$, Level $L$, Cusp Holomorphicity, and Sturm Cutoff $J$
- **Matrix identity & level:** Setting $L = \mathrm{lcm}(72, m^2, 4m)$ and $\Gamma = \Gamma_0(L)$ (even $k$) or $\{\gamma \in \Gamma_0(L) : d \equiv 1 \pmod 4\}$ (odd $k$), for any $\gamma = \left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right) \in \Gamma$, $\gcd(a, m) = 1$ since $m \mid L \mid c$ and $ad - bc = 1$. Choosing $h' \equiv d a^{-1} h \equiv a^{-2} h \pmod m$, the matrix $\tilde{\gamma} = T_h \gamma T_{h'}^{-1}$ (all of determinant $1$, so $|_w$ is strictly associative with no scalar factors) has entries $a + hc/m \in \mathbb{Z}$, $b + (hd-ah')/m - hch'/m^2 \in \mathbb{Z}$ (since $m^2 \mid L \mid c$), $c \equiv 0 \pmod{72}$, and $d' = d - (c/m)h' \equiv d \pmod 4$ (since $4m \mid L \mid c \implies 4 \mid c/m$). Thus $D |_w T_h \gamma = \chi(d') D |_w T_{h'} = D |_w T_{h'}$ on $\Gamma$.
- **Unit-square phase invariance:** For $m \in \{6, 12\}$, $a^2 \equiv 1 \pmod m$ for all $\gcd(a,m)=1$. For $m = 18$, $a^2 \equiv 1 \pmod 6$ for all $\gcd(a,18)=1$; because $r = 15$ is divisible by $3$, $r(a^2 - 1) \equiv 0 \pmod{18}$ holds for all units $a \bmod 18$. Thus $P |_w \gamma = P$ for all $\gamma \in \Gamma$.
- **Cusp holomorphicity of $P(z)$:** For any $\sigma \in \mathrm{SL}_2(\mathbb{Z})$, $m T_h \sigma \in M_2(\mathbb{Z})$ has determinant $m^2 > 0$ and factors by Hermite normal form as $\sigma' \left(\begin{smallmatrix}g & v\\ 0 & m^2/g\end{smallmatrix}\right)$ with $\sigma' \in \mathrm{SL}_2(\mathbb{Z})$ and $g = \gcd((mT_h\sigma)_{11}, (mT_h\sigma)_{21}) > 0$. Hence $T_h \sigma = \sigma' \left(\begin{smallmatrix}g/m & v/m\\ 0 & m/g\end{smallmatrix}\right)$, which rescales $\tau \mapsto (g^2 z + gv)/m^2$ in $(D |_w \sigma')(\tau)$ and introduces no negative powers of $q^{1/\text{width}}$.
- **Subgroup index, Sturm bound & $3^e$ induction:** For even $k$, $[\mathrm{SL}_2(\mathbb{Z}):\Gamma_0(L)] = L\prod_{p\mid L}(1+1/p) = I$. For odd $k$, $[\Gamma_0(144):\Gamma] = 2$ gives matrix index $I = 576 = 2 \cdot 288$ (conservatively twice the projective index $[\mathrm{PSL}_2(\mathbb{Z}):\overline{\Gamma}] = 288$). Sturm's theorem (Sturm 1987, Theorem 1; valid for all primes including $p = 3 \mid L$) gives $B = \lfloor wI/12 \rfloor$. Since $P(z) = \sum_{n\equiv r(m)} d_n q^n \in M_w(\Gamma) \cap \mathbb{Z}[[q]]$ has strictly integer coefficients at $\infty$, vanishing mod $3^e$ up to $q^B$ (i.e., $0 \le n \le J = \lfloor(B - mH - r)/m\rfloor$) implies $P \equiv 0 \pmod 3$ everywhere, allowing exact scalar division $3^{-1}P \in M_w(\Gamma) \cap \mathbb{Z}[[q]]$ $e$ times, after which cancelling the unit $U(q^m) \in 1 + q^m\mathbb{Z}[[q^m]]$ yields $A_k(mn+r) \equiv 0 \pmod{3^e}$ for all $n \ge 0$.

| $k$ | $m$ | $r$ | $e$ | $H$ | $L$ | $w$ | $I$ | $B$ | $J$ | Verified $0\le n\le J$ | Sharpness Witness & $v_3$ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 6 | 12 | 10 | 5 | 5 | 144 | 54 | 288 | 1296 | 102 | 103/103 $\equiv 0\pmod{243}$ | $A_6(22)=6{,}635{,}911{,}068$ ($v_3=5$; $v_3(A_6(10))=6$) |
| 3 | 12 | 7 | 4 | 3 | 144 | 33 | 576 | 1584 | 128 | 129/129 $\equiv 0\pmod{81}$ | $A_3(7)=1{,}296$ ($v_3=4$) |
| 3 | 12 | 11 | 4 | 3 | 144 | 33 | 576 | 1584 | 128 | 129/129 $\equiv 0\pmod{81}$ | $A_3(11)=24{,}624$ ($v_3=4$) |
| 4 | 6 | 5 | 3 | 2 | 72 | 20 | 144 | 240 | 37 | 38/38 $\equiv 0\pmod{27}$ | $A_4(5)=540$ ($v_3=3$) |
| 7 | 12 | 11 | 3 | 6 | 144 | 65 | 576 | 3120 | 253 | 254/254 $\equiv 0\pmod{27}$ | $A_7(11)=2{,}427{,}516$ ($v_3=3$) |
| 8 | 18 | 15 | 5 | 10 | 648 | 112 | 1296 | 12096 | 661 | 662/662 $\equiv 0\pmod{243}$ | $A_8(15)=277{,}575{,}984$ ($v_3=5$) |

---

## 5. Reproduction Commands & Compute Footprint

Run from `/Users/ricardo/dev/open-science/math_wave_1030/csweep_2adic_ref`:
```sh
nice -n 10 /usr/bin/time -l python3 -B referee_verify.py
```
- **Measured runtime:** `4.58 s` wall (`4.54 s` user, `0.01 s` sys, single thread, vs 45 min budget).
- **Measured Peak RSS:** `36,585,472` bytes (`~34.9 MB`, vs 2 GB budget).
- **Pure-integer guarantee:** `referee_verify.py` parses its own AST at startup and enforces zero transcendental/trig imports, zero floating-point literals/casts, and zero true-division operators.

---

## 6. Sources, Limitations, and Next Steps

- **Sources Used:** Exclusively clean-room inputs `2611.05623v1.tex.json.gz` and `PROOF.md`, plus classical theorems of Hirschhorn (2017), Ligozat (1975), Sturm (1987), and Ono (2004) cited therein (documented in `PRIOR_ART.md`).
- **Limitations:**
  1. Problem 6.5 (`\label{prob:rank}`, lines 936-938 of `designated_k_tuples_v4.tex`: constructing an explicit Young-diagram statistic / bijection splitting $k$-tuples of designated partitions of size $3n+2$ into three equinumerous classes for $k \equiv 1 \pmod 3$, $k \ge 4$) is explicitly posed as an open combinatorial problem rather than one of the four Section 6 conjectures and is outside the scope of `PROOF.md`.
  2. The proofs of `conj:A6` and `conj:deep` rely on modular forms and Sturm's theorem rather than explicit $q$-series dissections or combinatorial cranks; while 100% rigorous over $\mathbb{Z}$, they do not supply closed-form generating-function congruences analogous to Theorem 3.9(d) for $k=2$.
- **Next Steps:**
  1. If preparing a short note or appendix on these four conjectures, include the 5-line $M_{12}(\Gamma_0(24))$ Sturm proof (or Jacobi triple-product proof) of Hirschhorn's $f_1 f_3$ dissection alongside `PROOF.md` so even the external citation to [Hir] is self-contained.
  2. Investigate elementary $q$-series dissections for $A_3(12n+7), A_3(12n+11) \pmod{81}$ and Problem 6.5 (`prob:rank`) for $k=4$.

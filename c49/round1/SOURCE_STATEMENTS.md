# Verbatim mathematical source statements

Definition and operative gluing/transfer statement below are quoted from the live C49 page (Apache-2.0; license in sources/TEORTH_LICENSE), fetched 2026-11-14 UTC:
https://teorth.github.io/optimizationproblems/constants/49a.html

A family of three distinct sets $A,B,C$ is a **$3$-sunflower** (or $\Delta$-system) if
$$
A\cap B \ =\ A\cap C \ =\ B\cap C.
$$
A family of sets is **sunflower-free** if it contains no $3$-sunflower (equivalently, no sunflower of any size $\ge 3$).

Let $[n]:=\\{1,2,\dots,n\\}$ and let $f(n)$ denote the maximum size of a sunflower-free family $\mathcal{F}\subseteq 2^{[n]}$.
Define
$$
C_{49}\ :=\ \mu^{\mathrm S}\_3\ :=\ \limsup\_{n\to\infty} f(n)^{1/n}.
$$
A standard tensor power argument shows that the limsup is in fact a limit:
$$
\mu^{\mathrm S}\_3\ =\ \lim\_{n\to\infty} f(n)^{1/n}
$$
(see e.g. [TZ2025, (1.2)]).

| $\ge 1.5678599$* | [Kos2026] | Same chain construction and exact transfer-matrix count as [IRSI2026], with a 28-point base family built from the two families $F$ (75 sets on the edges of $K\_5$) and $H$ (121 sets on $\mathbb{Z}\_{11}$) of [Cla2026], extending the augmentation proposed in [PR #237](https://github.com/teorth/optimizationproblems/pull/237) to two pendants. Glue a copy of $H$ (at $0$) to $F$ at the edge $(0,3)$ and another at the edge $(0,4)$ by [DEGKM1997], Lemma 4.4 (250659 sets on 28 points). Then, at each pendant, add 15 sets whose part in that pendant is empty, and add 20 sets lying inside the first copy of $H$ and one set made of three $K\_5$ edges and all of the second copy (all listed at [Kos2026]). The resulting family has 252292 sets and is Sperner and 3-sunflower-free by an exhaustive check. Chaining copies at the edges $(0,1)\to(0,2)$ gives port counts $N\_{00}=33969$, $N\_{01}=N\_{10}=64728$, $N\_{11}=88867$, i.e. the transfer matrix with rows $(64728,88867)$ and $(33969,64728)$, with Perron root $64728+\sqrt{3018723123}$, and each copy adds 26 points: the chain families have at least $c\rho^k$ members on $26k+2$ points, so $\mu^{\mathrm S}\_3\ge(64728+\sqrt{3018723123})^{1/26} = 1.5678599\ldots$. Certificate (SHA-256 10ee18f9...4838), a C checker for the exhaustive check, and a standard-library Python script that rebuilds the family from this description and recomputes $\rho$ are at [Kos2026]; the family was also checked exhaustively by an independent checker written from the certificate format alone. Found by an AI agent; see the disclosure there. |

The page invokes DEGKM Lemma 4.4 but does not print its general statement. The full general statement below is quoted from Koshta FORMAT.md at the required c4ee81737f9f6a4ae9793586a27004553a12d5c0 pin (MIT; copyright Dennis Koshta, license in sources/LICENSE_KOSHTA):

**Gluing lemma** (Deuber–Erdős–Gunderson–Kostochka–Meyer 1997, Lemma 4.4). Let 𝓐 and 𝓑 be Sperner, 3-sunflower-free
families on disjoint ground sets X and Y, and let a ∈ X and b ∈ Y. Then

  𝓖 = {(C∖a) ∪ D : a ∈ C ∈ 𝓐, b ∉ D ∈ 𝓑} ∪ {C ∪ (D∖b) : a ∉ C ∈ 𝓐, b ∈ D ∈ 𝓑}

is Sperner and 3-sunflower-free on (X ∪ Y) ∖ {a, b}, and has |𝓐_a||𝓑_{b̄}| + |𝓐_{ā}||𝓑_b| members.


These are the mathematical inputs, not outputs of the finite certificate checker. The stored verbatim source snapshots are unmodified.

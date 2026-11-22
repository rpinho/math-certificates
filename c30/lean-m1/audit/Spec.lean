import Mathlib

/-!
# Spec v1 (Lean transcription of SPEC.md, sha256 5b7fec9f476bbf6cf4546d96300ce9ac60425862d29a715b456843589f36635b)

Written by Claude Opus 5.5 from SPEC.md only (AI audit, unrefereed). Imports only Mathlib.
Vectors are `Multiset ℤ` (SPEC.md: "a function Fin r -> Int, or a multiset of integers");
r is `Multiset.card y`. All arithmetic on r, L, B, U, e_j is in ℤ (no Nat subtraction, no
division: E7 is written as `2 * e1 = ...`). Rational parameters of E-app are exact rationals in ℚ.
-/

namespace Spec

open scoped BigOperators

/-- `ex_t(v) = Σ_i max(v_i - t, 0)` for real `t` (SPEC.md notation). -/
noncomputable def ex (t : ℝ) (v : Multiset ℤ) : ℝ :=
  (v.map (fun a : ℤ => max ((a : ℝ) - t) 0)).sum

/-- Majorization `x ≺ y`: same length, (M-a) equal sums, (M-b) `ex_t x ≤ ex_t y` for every real t. -/
def Majorized (x y : Multiset ℤ) : Prop :=
  Multiset.card x = Multiset.card y ∧ x.sum = y.sum ∧ ∀ t : ℝ, ex t x ≤ ex t y

/-- The vector with `e_j` entries equal to `j` (j = 0..3). Under E8 (`e_j ≥ 0`) `toNat` is exact. -/
def envVec (e0 e1 e2 e3 : ℤ) : Multiset ℤ :=
  Multiset.replicate e0.toNat 0 + Multiset.replicate e1.toNat 1 +
    Multiset.replicate e2.toNat 2 + Multiset.replicate e3.toNat 3

/-- The hypotheses E1-E4 on (y, L, B, U). -/
def HypE1_4 (y : Multiset ℤ) (L B U : ℤ) : Prop :=
  (∀ a ∈ y, 0 ≤ a) ∧ y.sum = L ∧ B ≤ (y.count 0 : ℤ) ∧ (y.count 2 : ℤ) ≤ U

/-- The hypotheses E5-E8 on (e0..e3), with r = card y. -/
def HypE5_8 (r L B U e0 e1 e2 e3 : ℤ) : Prop :=
  (e2 = U ∨ e2 = U - 1) ∧
  Even (L - r + B - e2) ∧
  e0 = B ∧ 2 * e1 = 3 * (r - B) - L - e2 ∧ 2 * e3 = L - r + B - e2 ∧
  0 ≤ e0 ∧ 0 ≤ e1 ∧ 0 ≤ e2 ∧ 0 ≤ e3

/-- The conclusion of Lemma E. -/
def ConclE (y : Multiset ℤ) (L e0 e1 e2 e3 : ℤ) : Prop :=
  Majorized (envVec e0 e1 e2 e3) y ∧
  e0 + e1 + e2 + e3 = (Multiset.card y : ℤ) ∧ e1 + 2 * e2 + 3 * e3 = L

/-- **Lemma E** (SPEC.md): ∀ r L B U y, E1-E4 → ∀ e0 e1 e2 e3, E5-E8 → x ≺ y (+ length/sum identities). -/
def LemmaE : Prop :=
  ∀ (y : Multiset ℤ) (L B U : ℤ), HypE1_4 y L B U →
    ∀ (e0 e1 e2 e3 : ℤ), HypE5_8 (Multiset.card y : ℤ) L B U e0 e1 e2 e3 →
      ConclE y L e0 e1 e2 e3

/-! ## Lemma E-app parameters -/

def Lapp (m : ℕ) : ℤ := ⌈(555555 / 1000000 : ℚ) * (m : ℚ)⌉
def rapp (m : ℕ) : ℤ := (m : ℤ) - Lapp m + 1
def Bapp (m : ℕ) : ℤ := ⌈(185185 / 1000000 : ℚ) * (m : ℚ)⌉ + 1
def Uapp (m : ℕ) : ℤ := ⌊(7 / 50 : ℚ) * (m : ℚ)⌋
/-- "the element of {U, U-1} making L - r + B - e2 even" -/
def e2app (m : ℕ) : ℤ :=
  if Even (Lapp m - rapp m + Bapp m - Uapp m) then Uapp m else Uapp m - 1
def e0app (m : ℕ) : ℤ := Bapp m
def e1app (m : ℕ) : ℤ := (3 * (rapp m - Bapp m) - Lapp m - e2app m) / 2
def e3app (m : ℕ) : ℤ := (Lapp m - rapp m + Bapp m - e2app m) / 2

/-- **E-app (core)**: for all sufficiently large m, the numerators are even and e0..e3 ≥ 0. -/
def EappCore : Prop :=
  ∃ M0 : ℕ, ∀ m ≥ M0,
    Even (3 * (rapp m - Bapp m) - Lapp m - e2app m) ∧
    Even (Lapp m - rapp m + Bapp m - e2app m) ∧
    0 ≤ e0app m ∧ 0 ≤ e1app m ∧ 0 ≤ e2app m ∧ 0 ≤ e3app m

/-- **E-app (counting, supplementary)**, SPEC.md lines 179-180: with a₊ = 555556/10⁶,
    b₋ = 1851851/10⁷, s2 = 1/10, for all sufficiently large m: (i) s2 m + 2 + 2(a₊ m - L) ≤ U,
    (ii) b₋ m - 1 ≥ B, and r ≥ B. -/
def EappCounting : Prop :=
  ∃ M0 : ℕ, ∀ m ≥ M0,
    (1 / 10 : ℚ) * m + 2 + 2 * ((555556 / 1000000 : ℚ) * m - Lapp m) ≤ Uapp m ∧
    (Bapp m : ℚ) ≤ (1851851 / 10000000 : ℚ) * m - 1 ∧
    Bapp m ≤ rapp m

/-- Lemma E at the E-app parameters (the "present application"), with cutoff M0. -/
def EappInstance (M0 : ℕ) : Prop :=
  ∀ m ≥ M0, ∀ y : Multiset ℤ, (Multiset.card y : ℤ) = rapp m →
    HypE1_4 y (Lapp m) (Bapp m) (Uapp m) →
      HypE5_8 (rapp m) (Lapp m) (Bapp m) (Uapp m) (e0app m) (e1app m) (e2app m) (e3app m) ∧
      ConclE y (Lapp m) (e0app m) (e1app m) (e2app m) (e3app m)

/-! ## Lemma M (finite weighted Markov step) -/

/-- **Lemma M** (SPEC.md): pointwise and summed forms. `n_i(n_i - 1)` is computed in ℝ. -/
def LemmaM : Prop :=
  ∀ (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s : ℝ),
    0 < s → (∀ i, 0 ≤ X i) → (∀ i, 0 ≤ a i) →
    (∀ i, X i > s * (n i : ℝ) → (n i : ℝ) * ((n i : ℝ) - 1) ≤ (n i : ℝ) * X i / s) ∧
    (∑ i ∈ Finset.univ.filter (fun i => X i > s * (n i : ℝ)),
        (n i : ℝ) * ((n i : ℝ) - 1) * a i)
      ≤ (1 / s) * ∑ i, (n i : ℝ) * X i * a i

/-! ## Lemma S (finite family-selection step) -/

/-- **Lemma S** (SPEC.md), with `W_i = n_i(n_i - 1) a_i`. -/
def LemmaS : Prop :=
  ∀ (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s mu eta : ℝ) (E : I → Prop)
    [DecidablePred E],
    0 < s → (∀ i, 0 ≤ X i) → (∀ i, 0 ≤ a i) →
    (∑ i, (n i : ℝ) * X i * a i ≤ mu * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i) →
    (∑ i ∈ Finset.univ.filter (fun i => ¬ E i), (n i : ℝ) * ((n i : ℝ) - 1) * a i
        ≤ eta * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i) →
    (1 - mu / s - eta) * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i
      ≤ ∑ i ∈ Finset.univ.filter (fun i => X i ≤ s * (n i : ℝ) ∧ E i),
          (n i : ℝ) * ((n i : ℝ) - 1) * a i

end Spec

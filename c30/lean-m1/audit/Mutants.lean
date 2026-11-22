import Spec
import Bridge

/-!
# Mutation tests and satisfiability for Spec v1 (AI audit, Claude Opus 5.5, unrefereed)

Each mutant changes one thing in a Spec v1 lemma (mutants of round 1, mutants.py) and is proved
FALSE by an explicit counterexample, so the bridges cannot pass because Spec is vacuous or weak.
Satisfiability: the hypotheses of each Spec lemma hold at the C30 parameters.
-/

namespace Mutants

open Spec
open scoped BigOperators

/-! ## Lemma E mutants -/

/-- E-mA: E5 widened to e2 ∈ {U, U-1, U-2}. -/
def LemmaE_mA : Prop :=
  ∀ (y : Multiset ℤ) (L B U : ℤ), HypE1_4 y L B U →
    ∀ (e0 e1 e2 e3 : ℤ),
      let r := (Multiset.card y : ℤ)
      (e2 = U ∨ e2 = U - 1 ∨ e2 = U - 2) → Even (L - r + B - e2) →
      e0 = B → 2 * e1 = 3 * (r - B) - L - e2 → 2 * e3 = L - r + B - e2 →
      0 ≤ e0 → 0 ≤ e1 → 0 ≤ e2 → 0 ≤ e3 → ConclE y L e0 e1 e2 e3

/-- E-mB: E4 (cnt₂(y) ≤ U) dropped. -/
def LemmaE_mB : Prop :=
  ∀ (y : Multiset ℤ) (L B U : ℤ), (∀ a ∈ y, 0 ≤ a) → y.sum = L → B ≤ (y.count 0 : ℤ) →
    ∀ (e0 e1 e2 e3 : ℤ), HypE5_8 (Multiset.card y : ℤ) L B U e0 e1 e2 e3 →
      ConclE y L e0 e1 e2 e3

/-- E-mC: E3 weakened to cnt₀(y) ≥ B - 1. -/
def LemmaE_mC : Prop :=
  ∀ (y : Multiset ℤ) (L B U : ℤ), (∀ a ∈ y, 0 ≤ a) → y.sum = L → B - 1 ≤ (y.count 0 : ℤ) →
    (y.count 2 : ℤ) ≤ U →
    ∀ (e0 e1 e2 e3 : ℤ), HypE5_8 (Multiset.card y : ℤ) L B U e0 e1 e2 e3 →
      ConclE y L e0 e1 e2 e3

/-- E-mR: conclusion direction reversed (y ≺ x). -/
def LemmaE_mR : Prop :=
  ∀ (y : Multiset ℤ) (L B U : ℤ), HypE1_4 y L B U →
    ∀ (e0 e1 e2 e3 : ℤ), HypE5_8 (Multiset.card y : ℤ) L B U e0 e1 e2 e3 →
      Majorized y (envVec e0 e1 e2 e3)

theorem refute_E_mA : ¬ LemmaE_mA := by
  intro h
  have := h (([2, 2] : List ℤ) : Multiset ℤ) 4 0 2 (by simp [HypE1_4]) 0 1 0 1
    (by norm_num) (by norm_num) rfl (by norm_num) (by norm_num) le_rfl zero_le_one le_rfl
    zero_le_one
  have h2 := this.1.2.2 2
  norm_num [Spec.ex, envVec, max_def] at h2

theorem refute_E_mB : ¬ LemmaE_mB := by
  intro h
  have := h (([2, 2] : List ℤ) : Multiset ℤ) 4 0 0 (by simp) (by simp) (by simp) 0 1 0 1
    (by norm_num [HypE5_8])
  have h2 := this.1.2.2 2
  norm_num [Spec.ex, envVec, max_def] at h2

theorem refute_E_mC : ¬ LemmaE_mC := by
  intro h
  have := h (([1, 1] : List ℤ) : Multiset ℤ) 2 1 1 (by simp) (by simp) (by simp) (by simp)
    1 0 1 0 (by norm_num [HypE5_8])
  have h2 := this.1.2.2 1
  norm_num [Spec.ex, envVec, max_def] at h2

theorem refute_E_mR : ¬ LemmaE_mR := by
  intro h
  have := h (([0, 1, 1, 4] : List ℤ) : Multiset ℤ) 6 1 1 (by simp [HypE1_4]) 1 1 1 1
    (by norm_num [HypE5_8])
  have h2 := this.2.2 3
  norm_num [Spec.ex, envVec, max_def] at h2

/-! ## Lemma M mutants -/

/-- M-mA: s > 0 dropped. -/
def LemmaM_mA : Prop :=
  ∀ (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s : ℝ),
    (∀ i, 0 ≤ X i) → (∀ i, 0 ≤ a i) →
    (∑ i ∈ Finset.univ.filter (fun i => X i > s * (n i : ℝ)),
        (n i : ℝ) * ((n i : ℝ) - 1) * a i)
      ≤ (1 / s) * ∑ i, (n i : ℝ) * X i * a i

/-- M-mB: a ≥ 0 dropped. -/
def LemmaM_mB : Prop :=
  ∀ (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s : ℝ),
    0 < s → (∀ i, 0 ≤ X i) →
    (∑ i ∈ Finset.univ.filter (fun i => X i > s * (n i : ℝ)),
        (n i : ℝ) * ((n i : ℝ) - 1) * a i)
      ≤ (1 / s) * ∑ i, (n i : ℝ) * X i * a i

/-- M-mC: X ≥ 0 dropped. -/
def LemmaM_mC : Prop :=
  ∀ (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s : ℝ),
    0 < s → (∀ i, 0 ≤ a i) →
    (∑ i ∈ Finset.univ.filter (fun i => X i > s * (n i : ℝ)),
        (n i : ℝ) * ((n i : ℝ) - 1) * a i)
      ≤ (1 / s) * ∑ i, (n i : ℝ) * X i * a i

/-- M-mD: conclusion strengthened, n(n-1) → n(n+1). -/
def LemmaM_mD : Prop :=
  ∀ (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s : ℝ),
    0 < s → (∀ i, 0 ≤ X i) → (∀ i, 0 ≤ a i) →
    (∑ i ∈ Finset.univ.filter (fun i => X i > s * (n i : ℝ)),
        (n i : ℝ) * ((n i : ℝ) + 1) * a i)
      ≤ (1 / s) * ∑ i, (n i : ℝ) * X i * a i

/-- M-mQ: quantifier swap in the pointwise form: (∃ bad i) → ∀ i, bound. -/
def LemmaM_mQ : Prop :=
  ∀ (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s : ℝ),
    0 < s → (∀ i, 0 ≤ X i) → (∀ i, 0 ≤ a i) →
    ((∃ i, X i > s * (n i : ℝ)) → ∀ i, (n i : ℝ) * ((n i : ℝ) - 1) ≤ (n i : ℝ) * X i / s)

theorem refute_M_mA : ¬ LemmaM_mA := by
  intro h
  have := h Unit (fun _ => 2) (fun _ => 1) (fun _ => 1) (-1) (fun _ => zero_le_one)
    (fun _ => zero_le_one)
  norm_num [Finset.sum_filter] at this

theorem refute_M_mB : ¬ LemmaM_mB := by
  intro h
  have := h (Fin 2) (fun _ => 2) ![3, 1] ![1, -10] 1 one_pos
    (fun i => by fin_cases i <;> norm_num)
  norm_num [Finset.sum_filter, Fin.sum_univ_two] at this

theorem refute_M_mC : ¬ LemmaM_mC := by
  intro h
  have := h (Fin 2) (fun _ => 2) ![3, -10] (fun _ => 1) 1 one_pos (fun _ => zero_le_one)
  simp only [Finset.sum_filter, Fin.sum_univ_two] at this
  norm_num at this

theorem refute_M_mD : ¬ LemmaM_mD := by
  intro h
  have := h Unit (fun _ => 1) (fun _ => 3 / 2) (fun _ => 1) 1 one_pos (fun _ => by norm_num)
    (fun _ => zero_le_one)
  norm_num [Finset.sum_filter] at this

theorem refute_M_mQ : ¬ LemmaM_mQ := by
  intro h
  have := h (Fin 2) ![0, 2] ![1, 0] (fun _ => 1) 1 one_pos
    (fun i => by fin_cases i <;> norm_num) (fun _ => zero_le_one) ⟨0, by norm_num⟩ 1
  norm_num at this

/-! ## Lemma S mutants -/

/-- S-mA: Markov term dropped from the factor (1 - eta). -/
def LemmaS_mA : Prop :=
  ∀ (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s mu eta : ℝ) (E : I → Prop)
    [DecidablePred E],
    0 < s → (∀ i, 0 ≤ X i) → (∀ i, 0 ≤ a i) →
    (∑ i, (n i : ℝ) * X i * a i ≤ mu * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i) →
    (∑ i ∈ Finset.univ.filter (fun i => ¬ E i), (n i : ℝ) * ((n i : ℝ) - 1) * a i
        ≤ eta * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i) →
    (1 - eta) * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i
      ≤ ∑ i ∈ Finset.univ.filter (fun i => X i ≤ s * (n i : ℝ) ∧ E i),
          (n i : ℝ) * ((n i : ℝ) - 1) * a i

/-- S-mB: conclusion made strict. -/
def LemmaS_mB : Prop :=
  ∀ (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s mu eta : ℝ) (E : I → Prop)
    [DecidablePred E],
    0 < s → (∀ i, 0 ≤ X i) → (∀ i, 0 ≤ a i) →
    (∑ i, (n i : ℝ) * X i * a i ≤ mu * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i) →
    (∑ i ∈ Finset.univ.filter (fun i => ¬ E i), (n i : ℝ) * ((n i : ℝ) - 1) * a i
        ≤ eta * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i) →
    (1 - mu / s - eta) * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i
      < ∑ i ∈ Finset.univ.filter (fun i => X i ≤ s * (n i : ℝ) ∧ E i),
          (n i : ℝ) * ((n i : ℝ) - 1) * a i

/-- S-mC: hypothesis S5 dropped. -/
def LemmaS_mC : Prop :=
  ∀ (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s mu eta : ℝ) (E : I → Prop)
    [DecidablePred E],
    0 < s → (∀ i, 0 ≤ X i) → (∀ i, 0 ≤ a i) →
    (∑ i, (n i : ℝ) * X i * a i ≤ mu * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i) →
    (1 - mu / s - eta) * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i
      ≤ ∑ i ∈ Finset.univ.filter (fun i => X i ≤ s * (n i : ℝ) ∧ E i),
          (n i : ℝ) * ((n i : ℝ) - 1) * a i

theorem refute_S_mA : ¬ LemmaS_mA := by
  intro h
  have := h Unit (fun _ => 3) (fun _ => 3) (fun _ => 1) (1 / 2) (3 / 2) 0 (fun _ => True)
    (by norm_num) (fun _ => by norm_num) (fun _ => zero_le_one) (by norm_num)
    (by norm_num [Finset.sum_filter])
  norm_num [Finset.sum_filter] at this

theorem refute_S_mB : ¬ LemmaS_mB := by
  intro h
  have := h Empty (fun _ => 0) (fun _ => 0) (fun _ => 0) (1 / 10) 0 0 (fun _ => True)
    (by norm_num) (fun _ => le_rfl) (fun _ => le_rfl) (by simp) (by simp)
  simp at this

theorem refute_S_mC : ¬ LemmaS_mC := by
  intro h
  have := h Unit (fun _ => 3) (fun _ => 0) (fun _ => 1) (1 / 10) 0 0 (fun _ => False)
    (by norm_num) (fun _ => le_rfl) (fun _ => zero_le_one) (by norm_num)
  norm_num [Finset.sum_filter] at this

/-- Controls: the unmutated Spec lemmas are all Lean-proved (Bridge), so each mutant above
    differs in truth value from its Spec lemma. -/
example : LemmaE ∧ LemmaM ∧ LemmaS ∧ EappCore ∧ EappInstance 100 :=
  ⟨Bridge.specE_full, Bridge.bridge_M, Bridge.specS_proved, Bridge.bridge_EappCore,
    Bridge.bridge_Eapp⟩

/-! ## Satisfiability at the actual C30 parameters -/

/-- E at the E-app parameters, every m ≥ 100: the envelope vector itself satisfies E1-E4 with
    card = r, and the pinned e's satisfy E5-E8. So Spec E / E-app are non-vacuous at C30. -/
theorem sat_E (m : ℕ) (hm : 100 ≤ m) :
    let y := envVec (e0app m) (e1app m) (e2app m) (e3app m)
    (Multiset.card y : ℤ) = rapp m ∧ HypE1_4 y (Lapp m) (Bapp m) (Uapp m) ∧
    HypE5_8 (rapp m) (Lapp m) (Bapp m) (Uapp m) (e0app m) (e1app m) (e2app m) (e3app m) := by
  obtain ⟨ev1, ev3, p0, p1, p2, p3⟩ := Bridge.eappCore_at m hm
  have hU2 : e2app m = Uapp m ∨ e2app m = Uapp m - 1 := by unfold e2app; split_ifs <;> simp
  rw [Int.even_iff] at ev1 ev3
  have q1 : 2 * e1app m = 3 * (rapp m - Bapp m) - Lapp m - e2app m := by unfold e1app; omega
  have q3 : 2 * e3app m = Lapp m - rapp m + Bapp m - e2app m := by unfold e3app; omega
  have q0 : e0app m = Bapp m := rfl
  intro y
  refine ⟨?_, ⟨?_, ?_, ?_, ?_⟩, ⟨hU2, ?_, q0, q1, q3, p0, p1, p2, p3⟩⟩
  · simp only [y, envVec, Multiset.card_add, Multiset.card_replicate]
    push_cast
    rw [Int.toNat_of_nonneg p0, Int.toNat_of_nonneg p1, Int.toNat_of_nonneg p2,
      Int.toNat_of_nonneg p3]
    unfold rapp at q1 q3 ⊢; omega
  · intro a ha
    simp only [y, envVec, Multiset.mem_add, Multiset.mem_replicate] at ha
    omega
  · simp only [y, envVec, Multiset.sum_add, Multiset.sum_replicate, nsmul_eq_mul]
    push_cast
    rw [Int.toNat_of_nonneg p1, Int.toNat_of_nonneg p2, Int.toNat_of_nonneg p3]
    omega
  · simp [y, envVec, Multiset.count_replicate]
    omega
  · simp [y, envVec, Multiset.count_replicate]
    omega
  · rw [Int.even_iff]; exact ev3

/-- Concrete values at m = 100 (L, r, B, U, e) = (56, 45, 20, 14, (20, 3, 13, 9)). -/
example : Lapp 100 = 56 ∧ rapp 100 = 45 ∧ Bapp 100 = 20 ∧ Uapp 100 = 14 := by
  have hL : Lapp 100 = 56 := by unfold Lapp; rw [Int.ceil_eq_iff]; norm_num
  have hB : Bapp 100 = 20 := by
    have hc : ⌈(185185 / 1000000 : ℚ) * ((100 : ℕ) : ℚ)⌉ = 19 := by
      rw [Int.ceil_eq_iff]; norm_num
    unfold Bapp; rw [hc]; rfl
  have hU : Uapp 100 = 14 := by unfold Uapp; rw [Int.floor_eq_iff]; norm_num
  refine ⟨hL, ?_, hB, hU⟩
  unfold rapp; rw [hL]; rfl

/-- M at the C30 instance: s = s2 = 1/10, X = N2 (a count), a = z^n with 0 ≤ z (z = 50/521). -/
theorem sat_M (I : Type) [Fintype I] (n N₂ : I → ℕ) (z : ℝ) (hz : 0 ≤ z) :
    (0 : ℝ) < 1 / 10 ∧ (∀ i, 0 ≤ ((N₂ i : ℕ) : ℝ)) ∧ (∀ i, 0 ≤ z ^ n i) :=
  ⟨by norm_num, fun _ => Nat.cast_nonneg _, fun _ => pow_nonneg hz _⟩

example : (0 : ℝ) ≤ 50 / 521 := by norm_num

/-- S at the C30 instance: s = 1/10, mu = 663/10000 (≥ mu2 = 0.066279...), eta = 1/100, on a
    one-domino family with n = 20, N2 = 1 ≤ s n, positive total weight; the factor is positive. -/
example :
    let n : Unit → ℕ := fun _ => 20
    let X : Unit → ℝ := fun _ => 1
    let a : Unit → ℝ := fun _ => 1
    (0 : ℝ) < 1 / 10 ∧ (∀ i, 0 ≤ X i) ∧ (∀ i, 0 ≤ a i) ∧
    (∑ i, (n i : ℝ) * X i * a i ≤ (663 / 10000) * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i) ∧
    (∑ i ∈ Finset.univ.filter (fun _ => ¬ True), (n i : ℝ) * ((n i : ℝ) - 1) * a i
        ≤ (1 / 100) * ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i) ∧
    0 < ∑ i, (n i : ℝ) * ((n i : ℝ) - 1) * a i ∧
    (0 : ℝ) < 1 - (663 / 10000) / (1 / 10) - 1 / 100 := by
  intro n X a
  refine ⟨by norm_num, fun _ => by norm_num [X], fun _ => by norm_num [a], ?_, ?_, ?_, by norm_num⟩
  · norm_num [n, X, a]
  · simp [n, a]
  · norm_num [n, a]

end Mutants

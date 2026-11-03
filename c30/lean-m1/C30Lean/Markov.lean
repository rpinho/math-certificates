module

public import Mathlib.Algebra.Order.BigOperators.Group.Finset
public import Mathlib.Basic.Real.Basic
public import Mathlib.Tactic

@[expose] public section

namespace C30Lean

open scoped BigOperators

/-- Finite weighted Markov, without normalizing the total weight. -/
theorem finite_weighted_markov {ι : Type*} (s : Finset ι)
    (w f : ι → ℝ) (t : ℝ) (ht : 0 < t)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hf : ∀ i ∈ s, 0 ≤ f i) :
    (∑ i ∈ s with t < f i, w i) ≤ (∑ i ∈ s, w i * f i) / t := by
  classical
  apply (le_div_iff₀ ht).2
  rw [Finset.sum_mul]
  calc
    ∑ i ∈ s with t < f i, w i * t ≤
        ∑ i ∈ s with t < f i, w i * f i := by
      apply Finset.sum_le_sum
      intro i hi
      exact mul_le_mul_of_nonneg_left (le_of_lt (Finset.mem_filter.mp hi).2)
        (hw i (Finset.mem_filter.mp hi).1)
    _ ≤ ∑ i ∈ s, w i * f i := by
      exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
        (fun i hi _ => mul_nonneg (hw i hi) (hf i hi))

/-- The finite truncation of the n(n-1)-weighted bad-domino estimate in §4. -/
theorem finite_family_selection {ι : Type*} (s : Finset ι)
    (w : ι → ℝ) (n N₂ : ι → ℕ) (t : ℝ) (ht : 0 < t)
    (hw : ∀ i ∈ s, 0 ≤ w i) :
    (∑ i ∈ s with t * (n i : ℝ) < (N₂ i : ℝ),
      w i * (n i : ℝ) * ((n i : ℝ) - 1)) ≤
      (∑ i ∈ s, w i * (n i : ℝ) * (N₂ i : ℝ)) / t := by
  classical
  apply (le_div_iff₀ ht).2
  rw [Finset.sum_mul]
  calc
    _ ≤ ∑ i ∈ s with t * (n i : ℝ) < (N₂ i : ℝ),
        w i * (n i : ℝ) * (N₂ i : ℝ) := by
      apply Finset.sum_le_sum
      intro i hi
      have hn : (0 : ℝ) ≤ n i := Nat.cast_nonneg _
      have hwi := hw i (Finset.mem_filter.mp hi).1
      have hbad := (Finset.mem_filter.mp hi).2
      have hpoint : t * ((n i : ℝ) - 1) ≤ (N₂ i : ℝ) := by nlinarith
      have := mul_le_mul_of_nonneg_left hpoint (mul_nonneg hwi hn)
      nlinarith only [this]
    _ ≤ _ := Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
      (fun i hi _ => mul_nonneg (mul_nonneg (hw i hi) (Nat.cast_nonneg _))
        (Nat.cast_nonneg _))

end C30Lean

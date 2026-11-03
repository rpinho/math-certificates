module

public import C30Lean.Envelope
public import Mathlib.Algebra.Order.Archimedean.Real.Basic

@[expose] public section

namespace C30Lean

def realExcess (y : List ℤ) (t : ℝ) : ℝ :=
  (y.map (fun (a : ℤ) => max ((a : ℝ) - t) 0)).sum

/-- Majorization in the threshold-excess formulation, including equal totals. -/
def ThresholdMajorized (x y : List ℤ) : Prop :=
  x.length = y.length ∧ x.sum = y.sum ∧
    ∀ t : ℝ, realExcess x t ≤ realExcess y t

theorem realExcess_int (y : List ℤ) (k : ℤ) :
    realExcess y (k : ℝ) = (excess y k : ℝ) := by
  simp [realExcess, excess, List.map_map, Function.comp_def, Int.cast_max]

/-- There is no breakpoint strictly between successive integer thresholds. -/
theorem realExcess_interpolate (y : List ℤ) (k : ℤ) (t : ℝ)
    (ht₀ : (k : ℝ) ≤ t) (ht₁ : t ≤ (k : ℝ) + 1) :
    realExcess y t = ((k : ℝ) + 1 - t) * realExcess y k +
      (t - k) * realExcess y ((k : ℝ) + 1) := by
  have point (a : ℤ) : max ((a : ℝ) - t) 0 =
      ((k : ℝ) + 1 - t) * max ((a : ℝ) - k) 0 +
      (t - k) * max ((a : ℝ) - ((k : ℝ) + 1)) 0 := by
    by_cases ha : a ≤ k
    · have har : (a : ℝ) ≤ k := by exact_mod_cast ha
      rw [max_eq_right (by linarith : (a : ℝ) - t ≤ 0),
        max_eq_right (by linarith : (a : ℝ) - k ≤ 0),
        max_eq_right (by linarith : (a : ℝ) - ((k : ℝ) + 1) ≤ 0)]
      ring
    · have har : (k : ℝ) + 1 ≤ a := by exact_mod_cast (show k + 1 ≤ a by omega)
      rw [max_eq_left (by linarith : 0 ≤ (a : ℝ) - t),
        max_eq_left (by linarith : 0 ≤ (a : ℝ) - k),
        max_eq_left (by linarith : 0 ≤ (a : ℝ) - ((k : ℝ) + 1))]
      ring
  induction y with
  | nil => simp [realExcess]
  | cons a y ih =>
    simp only [realExcess, List.map_cons, List.sum_cons] at *
    rw [point, ih]
    ring

theorem integer_thresholds_suffice (x y : List ℤ)
    (h : ∀ k : ℤ, excess x k ≤ excess y k) :
    ∀ t : ℝ, realExcess x t ≤ realExcess y t := by
  intro t
  let k : ℤ := ⌊t⌋
  have ht₀ : (k : ℝ) ≤ t := Int.floor_le t
  have ht₁ : t ≤ (k : ℝ) + 1 := le_of_lt (Int.lt_floor_add_one t)
  rw [realExcess_interpolate x k t ht₀ ht₁, realExcess_interpolate y k t ht₀ ht₁]
  have h₀ : realExcess x (k : ℝ) ≤ realExcess y (k : ℝ) := by
    simpa only [realExcess_int] using (show (excess x k : ℝ) ≤ excess y k by
      exact_mod_cast h k)
  have h₁ : realExcess x ((k : ℝ) + 1) ≤ realExcess y ((k : ℝ) + 1) := by
    have := h (k + 1)
    have : realExcess x ((k + 1 : ℤ) : ℝ) ≤ realExcess y ((k + 1 : ℤ) : ℝ) := by
      simpa only [realExcess_int] using
        (show (excess x (k + 1) : ℝ) ≤ excess y (k + 1) by exact_mod_cast this)
    simpa using this
  exact add_le_add (mul_le_mul_of_nonneg_left h₀ (by linarith))
    (mul_le_mul_of_nonneg_left h₁ (by linarith))

/-- The full finite envelope, with the parity-correct integer counts and all
    real threshold inequalities. The two linear hypotheses make the displayed
    multiplicities nonnegative; the zero-cap hypothesis handles U=0 exactly. -/
theorem strip_envelope (y : List ℤ) (L B U : ℤ)
    (hy : ∀ a ∈ y, 0 ≤ a) (hL : y.sum = L)
    (hn0 : B ≤ countStrip y 0) (hn2 : countStrip y 2 ≤ U)
    (hB : 0 ≤ B) (hU : 0 ≤ U)
    (hzero : U = 0 → (L - y.length + B) % 2 = 0)
    (h₁ : U ≤ 3 * ((y.length : ℤ) - B) - L)
    (h₃ : U ≤ L - y.length + B) :
    ∃ e : StripEnvelope,
      (e.e0 : ℤ) = B ∧
      ((e.e2 : ℤ) = U ∨ (e.e2 : ℤ) = U - 1) ∧
      (L - y.length + B - e.e2) % 2 = 0 ∧
      (e.e1 : ℤ) = (3 * ((y.length : ℤ) - B) - L - e.e2) / 2 ∧
      (e.e3 : ℤ) = (L - y.length + B - e.e2) / 2 ∧
      ThresholdMajorized e.vector y := by
  obtain ⟨e, h0, h2, hp, h1, h3, hlen, hsum, hex⟩ :=
    integer_strip_envelope y L B U hy hL hn0 hn2 hB hU hzero h₁ h₃
  exact ⟨e, h0, h2, hp, h1, h3, hlen, hsum, integer_thresholds_suffice _ _ hex⟩

end C30Lean

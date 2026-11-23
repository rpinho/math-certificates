import Spec
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

open MeasureTheory Metric Set
open scoped RealInnerProductSpace ENNReal

namespace DoubleCapAudit

theorem probability {n : ℕ} (hn : 3 ≤ n) : IsProbabilityMeasure (μ n) := by
  let : NeZero n := ⟨by omega⟩
  have h : surface n univ ≠ 0 := by
    exact Measure.measure_univ_ne_zero.mpr (Measure.toSphere_ne_zero (volume : Measure (Ambient n)))
  exact ⟨ENNReal.inv_mul_cancel h (measure_ne_top (volume.toSphere : Measure (Sphere n)) _)⟩

theorem cap_open {n : ℕ} (a : Sphere n) (r : ℝ) : IsOpen (cap a r) :=
  isOpen_lt continuous_const (continuous_const.inner continuous_subtype_val).abs

theorem D_measurable {n : ℕ} (a : Sphere n) : MeasurableSet (D a) :=
  (cap_open a _).measurableSet

private theorem unit_inner {n : ℕ} (x : Sphere n) :
    ⟪(x : Ambient n), (x : Ambient n)⟫ = 1 := by
  simp [norm_eq_of_mem_sphere x]

theorem D_pos {n : ℕ} (a : Sphere n) : 0 < μ n (D a) := by
  have ha : a ∈ D a := by
    change Real.cos (Real.pi / 4) < |⟪(a : Ambient n), (a : Ambient n)⟫|
    rw [unit_inner, abs_one, Real.cos_pi_div_four]
    nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)]
  change 0 < (surface n univ)⁻¹ * surface n (D a)
  apply ENNReal.mul_pos (ENNReal.inv_ne_zero.mpr (measure_ne_top (volume.toSphere : Measure (Sphere n)) _))
  exact (cap_open a _).measure_ne_zero (volume.toSphere : Measure (Sphere n)) ⟨a, ha⟩

private theorem residual {n : ℕ} (a x : Sphere n) (hx : x ∈ D a) :
    ‖(x : Ambient n) - ⟪(a : Ambient n), (x : Ambient n)⟫ • (a : Ambient n)‖ <
      Real.sqrt 2 / 2 := by
  change Real.cos (Real.pi / 4) < _ at hx
  rw [Real.cos_pi_div_four] at hx
  have hsq := mul_self_lt_mul_self (by positivity : 0 ≤ Real.sqrt 2 / 2) hx
  rw [abs_mul_abs_self] at hsq
  have h := norm_sub_sq_real (x : Ambient n) (⟪(a : Ambient n), (x : Ambient n)⟫ • (a : Ambient n))
  rw [real_inner_smul_right, real_inner_comm (a : Ambient n) (x : Ambient n),
    norm_smul, norm_eq_of_mem_sphere a, norm_eq_of_mem_sphere x, mul_one,
    Real.norm_eq_abs, sq_abs] at h
  apply (sq_lt_sq₀ (norm_nonneg _) (by positivity : 0 ≤ Real.sqrt 2 / 2)).mp
  nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)]

theorem D_avoids {n : ℕ} (a : Sphere n) : AvoidsOrthogonality (D a) := by
  intro x hx y hy hxy
  have rx := residual a x hx
  have ry := residual a y hy
  change Real.cos (Real.pi / 4) < _ at hx hy
  rw [Real.cos_pi_div_four] at hx hy
  let s := ⟪(a : Ambient n), (x : Ambient n)⟫
  let t := ⟪(a : Ambient n), (y : Ambient n)⟫
  have hinner : ⟪(x : Ambient n) - s • (a : Ambient n),
      (y : Ambient n) - t • (a : Ambient n)⟫ = -(s*t) := by
    simp only [inner_sub_left, inner_sub_right, real_inner_smul_left, real_inner_smul_right,
      unit_inner, hxy, real_inner_comm (a : Ambient n) (x : Ambient n)]
    dsimp [s,t]
    ring
  have bound := abs_real_inner_le_norm ((x : Ambient n) - s • (a : Ambient n))
    ((y : Ambient n) - t • (a : Ambient n))
  rw [hinner, abs_neg, abs_mul] at bound
  have hr := mul_lt_mul_of_le_of_lt_of_nonneg_of_pos rx.le ry (norm_nonneg _) (by positivity)
  have hc := mul_lt_mul_of_le_of_lt_of_nonneg_of_pos hx.le hy (by positivity) ((by positivity : 0 < Real.sqrt 2 / 2).trans hx)
  exact (not_lt_of_ge bound) (hr.trans hc)

end DoubleCapAudit

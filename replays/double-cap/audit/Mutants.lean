import Bridge

open MeasureTheory Metric Set Real WithLp
open scoped ENNReal RealInnerProductSpace

namespace DoubleCapAudit.Controls

/-- Every numerical refutation uses an admissible input equal to the literal D. -/
def FailsAtD {n : ℕ} (a : Sphere n) (claim : Set (Sphere n) → Prop) : Prop :=
  MeasurableSet (D a) ∧ AvoidsOrthogonality (D a) ∧ ¬ claim (D a)

private theorem witness {n : ℕ} (a : Sphere n) {P : Set (Sphere n) → Prop}
    (h : ¬ P (D a)) : FailsAtD a P := ⟨D_measurable a, D_avoids a, h⟩

private theorem mass3 (a : Sphere 3) (r : ℝ) (hr : r ∈ Icc 0 (π / 2)) :
    (μ 3).real (cap a r) = 1 - cos r := by
  have h := (LeanShadow.Comparator.caps_attain (volume : Measure (Ambient 3))
    (by simp) a r hr).1
  change (μ 3).real (cap a r) = LeanShadow.Comparator.capMass 1 r at h
  simpa [LeanShadow.Comparator.capMass, LeanShadow.Comparator.normalizer,
    LeanShadow.Comparator.sinPrimitive] using h

private theorem D_mass3 (a : Sphere 3) : (μ 3).real (D a) = 1 - sqrt 2 / 2 := by
  simpa [D, cos_pi_div_four] using mass3 a (π / 4) ⟨by positivity, by linarith [pi_pos]⟩

/-- A concrete choice of axis, in particular for dimensions three and four. -/
noncomputable def axis (n : ℕ) [NeZero n] : Sphere n :=
  ⟨EuclideanSpace.single 0 (1 : ℝ), by simp⟩

theorem scaled_99 (a : Sphere 3) :
    FailsAtD a (fun A => (μ 3).real A ≤ (μ 3).real (D a) * (99/100 : ℝ)) := by
  apply witness
  rw [D_mass3]
  nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)]

theorem strict_bound (a : Sphere 3) :
    FailsAtD a (fun A => μ 3 A < μ 3 (D a)) := witness a (lt_irrefl _)

theorem minus_thousandth (a : Sphere 3) :
    FailsAtD a (fun A => (μ 3).real A ≤ (μ 3).real (D a) - 1/1000) := by
  apply witness
  linarith

theorem radius_fifth (a : Sphere 3) :
    FailsAtD a (fun A => (μ 3).real A ≤ (μ 3).real (cap a (π / 5))) := by
  apply witness
  change ¬ (μ 3).real (cap a (π/4)) ≤ _
  rw [mass3 a _ ⟨by positivity, by linarith [pi_pos]⟩,
    mass3 a _ ⟨by positivity, by linarith [pi_pos]⟩]
  have h := strictAntiOn_cos (show π/5 ∈ Icc 0 π from ⟨by positivity, by linarith [pi_pos]⟩)
    (show π/4 ∈ Icc 0 π from ⟨by positivity, by linarith [pi_pos]⟩) (by linarith [pi_pos])
  linarith

/-- At n=3, using S^n means measuring the cap on S³ in ambient dimension four. -/
theorem next_sphere (a : Sphere 3) :
    FailsAtD a (fun A => (μ 3).real A ≤ (μ 4).real (D (axis 4))) := by
  apply witness
  rw [D_mass3]
  have h := (LeanShadow.Comparator.caps_attain (volume : Measure (Ambient 4))
    (by simp) (axis 4) (π/4) ⟨by positivity, by linarith [pi_pos]⟩).1
  change (μ 4).real (D (axis 4)) = LeanShadow.Comparator.capMass 2 (π/4) at h
  rw [h]
  simp only [LeanShadow.Comparator.capMass, LeanShadow.Comparator.normalizer,
    LeanShadow.Comparator.sinPrimitive, integral_sin_sq, sin_zero, cos_zero, zero_mul,
    sin_pi_div_two, cos_pi_div_two, mul_zero, sub_zero, zero_add, sin_pi_div_four, cos_pi_div_four]
  have hs := Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)
  have hs' : sqrt 2 < 3/2 := by nlinarith
  have he : sqrt 2 / 2 * (sqrt 2 / 2) = 1/2 := by nlinarith
  rw [he]
  push Not
  field_simp [pi_ne_zero]
  nlinarith [pi_lt_four, pi_pos, mul_pos pi_pos (sub_pos.mpr hs')]

/-- Mixed units: unnormalized area of A against the original probability bound. -/
theorem raw_area (a : Sphere 3) :
    FailsAtD a (fun A => (surface 3).real A ≤ (μ 3).real (D a)) := by
  apply witness
  change ¬ (surface 3 (D a)).toReal ≤ ((surface 3 univ)⁻¹ * surface 3 (D a)).toReal
  rw [ENNReal.toReal_mul, ENNReal.toReal_inv]
  have ht : (surface 3 univ).toReal = 4 * π := by
    simp [surface, Ambient, ENNReal.toReal_ofReal (by positivity : 0 ≤ π * 4 / 3)] <;> ring
  have hm := D_pos a
  change 0 < (surface 3 univ)⁻¹ * surface 3 (D a) at hm
  have hp : 0 < (surface 3 (D a)).toReal := by
    apply ENNReal.toReal_pos _ (measure_ne_top (volume.toSphere : Measure (Sphere 3)) _)
    intro hz
    change surface 3 (D a) = 0 at hz
    rw [hz, mul_zero] at hm
    exact (lt_irrefl _ hm)
  rw [ht]
  have hi : (4 * π)⁻¹ < 1 := (inv_lt_one₀ (by positivity)).2 (by linarith [pi_gt_three])
  exact not_le.mpr (by simpa using mul_lt_mul_of_pos_right hi hp)

/-- Scaling both sides instead preserves the order, for every pair of sets. -/
theorem raw_both {n : ℕ} (hn : 3 ≤ n) (A B : Set (Sphere n)) :
    μ n A ≤ μ n B ↔ surface n A ≤ surface n B := by
  let : NeZero n := ⟨by omega⟩
  have hnz : surface n univ ≠ 0 :=
    Measure.measure_univ_ne_zero.mpr (Measure.toSphere_ne_zero (volume : Measure (Ambient n)))
  have hfin : surface n univ ≠ ⊤ := measure_ne_top (volume.toSphere : Measure (Sphere n)) _
  change (surface n univ)⁻¹ * surface n A ≤ (surface n univ)⁻¹ * surface n B ↔ _
  simpa [mul_comm] using (ENNReal.mul_le_mul_iff_left
    (a := surface n A) (b := surface n B) (ENNReal.inv_ne_zero.mpr hfin) (ENNReal.inv_ne_top.mpr hnz))

/-- Coordinate vectors (1,±1,0)/√2. -/
private noncomputable def diagonal (s : ℝ) : Ambient 3 :=
  toLp 2 ![sqrt 2 / 2, s * (sqrt 2 / 2), 0]

private theorem diag_inner (s t : ℝ) :
    ⟪diagonal s, diagonal t⟫ = (1 + s*t)/2 := by
  simp [diagonal, EuclideanSpace.inner_toLp_toLp, dotProduct, Fin.sum_univ_succ]
  nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num),
    congrArg (fun z : ℝ => s*t*z) (Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num))]

private theorem diag_unit (s : ℝ) (hs : s*s = 1) : diagonal s ∈ Metric.sphere 0 1 := by
  rw [mem_sphere_zero_iff_norm]
  have h := diag_inner s s
  rw [real_inner_self_eq_norm_sq, hs] at h
  nlinarith [norm_nonneg (diagonal s)]

theorem closed_boundary :
    ¬ AvoidsOrthogonality (LeanShadow.Comparator.closedCap (axis 3) (π/4)) := by
  let x : Sphere 3 := ⟨diagonal 1, diag_unit 1 (by norm_num)⟩
  let y : Sphere 3 := ⟨diagonal (-1), diag_unit (-1) (by norm_num)⟩
  have mem (s : ℝ) (hs : s*s = 1) :
      (⟨diagonal s, diag_unit s hs⟩ : Sphere 3) ∈ LeanShadow.Comparator.closedCap (axis 3) (π/4) := by
    change cos (π/4) ≤ |inner ℝ (EuclideanSpace.single 0 (1 : ℝ)) (diagonal s)|
    simp [cos_pi_div_four, EuclideanSpace.inner_single_left, diagonal, abs_of_nonneg (by positivity : 0 ≤ sqrt 2 / 2)]
  intro h
  apply h x (mem 1 (by norm_num)) y (mem (-1) (by norm_num))
  norm_num [x, y, diag_inner]

theorem radius_third {n : ℕ} (hn : 3 ≤ n) (a : Sphere n) (A : Set (Sphere n))
    (hA : MeasurableSet A) (hind : AvoidsOrthogonality A) : μ n A ≤ μ n (cap a (π/3)) := by
  apply (fromSolution n hn a A hA hind).trans
  apply measure_mono
  intro x hx
  change cos (π/4) < |inner ℝ (a : Ambient n) (x : Ambient n)| at hx
  change cos (π/3) < |inner ℝ (a : Ambient n) (x : Ambient n)|
  apply lt_trans _ hx
  exact strictAntiOn_cos ⟨by positivity, by linarith [pi_pos]⟩
    ⟨by positivity, by linarith [pi_pos]⟩ (by linarith [pi_pos])

theorem borel_only {n : ℕ} (hn : 3 ≤ n) (a : Sphere n) (A : Set (Sphere n))
    (hA : @MeasurableSet _ (borel (Sphere n)) A) (hind : AvoidsOrthogonality A) :
    μ n A ≤ μ n (D a) :=
  fromSolution n hn a A (by rwa [BorelSpace.measurable_eq (α := Sphere n)]) hind

theorem n_ge_four {n : ℕ} (hn : 4 ≤ n) (a : Sphere n) (A : Set (Sphere n))
    (hA : MeasurableSet A) (hind : AvoidsOrthogonality A) : μ n A ≤ μ n (D a) :=
  fromSolution n (by omega) a A hA hind

#print axioms scaled_99
#print axioms strict_bound
#print axioms minus_thousandth
#print axioms radius_fifth
#print axioms next_sphere
#print axioms raw_area
#print axioms closed_boundary
#print axioms radius_third
#print axioms borel_only
#print axioms n_ge_four
#print axioms raw_both

end DoubleCapAudit.Controls

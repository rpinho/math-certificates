import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

open MeasureTheory Metric Set
open scoped RealInnerProductSpace ENNReal

namespace DoubleCapAudit

abbrev Ambient (n : ℕ) := EuclideanSpace ℝ (Fin n)
abbrev Sphere (n : ℕ) := Metric.sphere (0 : Ambient n) 1

noncomputable def surface (n : ℕ) : Measure (Sphere n) :=
  (volume : Measure (Ambient n)).toSphere

noncomputable def μ (n : ℕ) : Measure (Sphere n) :=
  ((surface n) univ)⁻¹ • surface n

def cap {n : ℕ} (a : Sphere n) (r : ℝ) : Set (Sphere n) :=
  {x | Real.cos r < |⟪(a : Ambient n), (x : Ambient n)⟫|}

def D {n : ℕ} (a : Sphere n) : Set (Sphere n) := cap a (Real.pi / 4)

def AvoidsOrthogonality {n : ℕ} (A : Set (Sphere n)) : Prop :=
  ∀ x ∈ A, ∀ y ∈ A, ⟪(x : Ambient n), (y : Ambient n)⟫ ≠ 0

def Conjecture : Prop :=
  ∀ (n : ℕ), 3 ≤ n → ∀ (a : Sphere n) (A : Set (Sphere n)),
    MeasurableSet A → AvoidsOrthogonality A → μ n A ≤ μ n (D a)

end DoubleCapAudit

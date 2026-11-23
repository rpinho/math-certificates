import ComparatorChallenges.Shadow
import NonVacuity

open MeasureTheory Set
open scoped ENNReal

namespace DoubleCapAudit

/-- The authors supply both the extremal inequality and the area of a literal cap. -/
theorem fromChallenge : Conjecture := by
  intro n hn a A hA hind
  let : NeZero n := ⟨by omega⟩
  let : IsProbabilityMeasure (μ n) := probability hn
  have dim : 2 < Module.finrank ℝ (Ambient n) := by simpa [Ambient] using (show 2 < n by omega)
  have bound := LeanShadow.Comparator.double_cap_bound (volume : Measure (Ambient n))
    dim A hA.nullMeasurableSet hind
  have mass := (LeanShadow.Comparator.caps_attain (volume : Measure (Ambient n))
    dim a (Real.pi / 4) ⟨by positivity, by linarith [Real.pi_pos]⟩).1
  apply (ENNReal.toReal_le_toReal (measure_ne_top (μ n) A) (measure_ne_top (μ n) (D a))).mp
  exact bound.trans_eq mass.symm

#print axioms fromChallenge
end DoubleCapAudit

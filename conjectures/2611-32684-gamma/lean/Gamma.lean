import Gamma.Connectivity

namespace Gamma

/-- A counterexample to the nonnegativity conjecture in the Discussion of
Supkar and Yaddanapudi, arXiv:2611.32684v1. -/
theorem supkar_yaddanapudi_conjecture_false :
    ∃ g : SimpleGraph11, ThreeConnected g ∧ ¬Bipartite g ∧
      eval (chiPoly g) 2 = 0 ∧ (-1 : Int)^10 * eval (deriv (chiPoly g)) 2 = -2 := by
  refine ⟨G,three_connected,not_bipartite,?_,?_⟩
  · rw [witness_polynomial,chi_at_two]
  · rw [witness_polynomial,signed_derivative]

end Gamma

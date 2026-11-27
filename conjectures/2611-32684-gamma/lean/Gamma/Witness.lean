import Gamma.Graph

namespace Gamma

def G : SimpleGraph11 where
  edges := [(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),
            (1,3),(1,5),(1,6),(1,7),(2,4),(2,5),(2,6),(2,7),
            (3,8),(3,9),(3,10),(4,8),(4,9),(4,10)]
  ordered := by decide
  uniqueEdges := by decide

theorem simple_G : (∀ a, ¬Adj G a a) ∧ (∀ a b, Adj G a b → Adj G b a) :=
  ⟨adj_irreflexive G,adj_symmetric G⟩

theorem twenty_edges : G.edges.length = 20 := rfl

def Bipartite (g : SimpleGraph n) := ∃ c : Fin n → Fin 2, IsProperColoring g c

theorem five_cycle : Adj G 0 5 ∧ Adj G 5 1 ∧ Adj G 1 3 ∧ Adj G 3 8 ∧ Adj G 8 0 := by decide

theorem not_bipartite : ¬Bipartite G := by
  rintro ⟨c,h⟩
  obtain ⟨a,b,d,e,f⟩ := five_cycle
  have proper := (proper_iff_adj G c).mp h
  have noCycle : ∀ p q r s t : Fin 2,
      p ≠ q → q ≠ r → r ≠ s → s ≠ t → t ≠ p → False := by
    intro p q r s t hp hq hr hs ht
    omega
  exact noCycle _ _ _ _ _ (proper _ _ a) (proper _ _ b) (proper _ _ d)
    (proper _ _ e) (proper _ _ f)

def chiG : Poly :=
  [0,5018,-20253,36166,-38153,26647,-13007,4533,-1122,190,-20,1]

set_option maxRecDepth 8192 in
set_option maxHeartbeats 4000000 in
theorem witness_polynomial : chiPoly G = chiG := by decide +kernel

theorem chromatic_poly_matches_colorings (k : Nat) :
    (coloringCount G k : Int) = eval chiG k :=
  witness_polynomial ▸ chiPoly_counts G k

/-- The half signed derivative, with exact rational division for every graph. -/
def gamma (g : SimpleGraph n) : Rat :=
  (((-1 : Int) ^ (n-1) * eval (deriv (chiPoly g)) 2 : Int) : Rat) / 2

theorem chi_at_two : eval chiG 2 = 0 := by decide
theorem deriv_at_two : eval (deriv chiG) 2 = -2 := by decide
theorem signed_derivative : (-1 : Int)^10 * eval (deriv chiG) 2 = -2 := by decide

theorem gamma_eq_neg_one : gamma G = -1 := by
  rw [gamma,witness_polynomial]
  decide +kernel

theorem twice_gamma : 2 * gamma G = (((-1 : Int)^10 * eval (deriv chiG) 2 : Int) : Rat) := by
  rw [gamma_eq_neg_one,signed_derivative]
  decide +kernel

theorem gamma_negative : gamma G < 0 := by rw [gamma_eq_neg_one]; decide +kernel

theorem palette_controls : eval chiG 3 = 150 ∧ eval chiG 4 = 20760 := by decide

def K3 : SimpleGraph 3 where
  edges := [(0,1),(0,2),(1,2)]
  ordered := by decide
  uniqueEdges := by decide

def K4 : SimpleGraph 4 where
  edges := [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
  ordered := by decide
  uniqueEdges := by decide

theorem K3_complete : ∀ a b, Adj K3 a b ↔ a ≠ b := by decide
theorem K4_complete : ∀ a b, Adj K4 a b ↔ a ≠ b := by decide
theorem K3_gamma : gamma K3 = 1 := by decide +kernel
theorem K4_gamma : gamma K4 = 1 := by decide +kernel

end Gamma

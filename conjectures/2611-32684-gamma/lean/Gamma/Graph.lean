import Gamma.Eliminate

namespace Gamma

/-- One canonically oriented entry per undirected edge. -/
structure SimpleGraph (n : Nat) where
  edges : List (Fin n × Fin n)
  ordered : ∀ e ∈ edges, e.1 < e.2
  uniqueEdges : edges.Nodup

abbrev SimpleGraph11 := SimpleGraph 11

def Adj (g : SimpleGraph n) (a b : Fin n) : Prop :=
  (a,b) ∈ g.edges ∨ (b,a) ∈ g.edges

instance (g : SimpleGraph n) (a b : Fin n) : Decidable (Adj g a b) :=
  inferInstanceAs (Decidable (_ ∨ _))

theorem adj_symmetric (g : SimpleGraph n) (a b : Fin n) : Adj g a b → Adj g b a := Or.symm

theorem adj_irreflexive (g : SimpleGraph n) (a : Fin n) : ¬Adj g a a := by
  intro h
  have hh : (a,a) ∈ g.edges := h.elim id id
  exact Nat.lt_irrefl _ (g.ordered _ hh)

def IsProperColoring (g : SimpleGraph n) (c : Fin n → Fin k) : Prop :=
  ∀ e ∈ g.edges, c e.1 ≠ c e.2

instance (g : SimpleGraph n) (c : Fin n → Fin k) : Decidable (IsProperColoring g c) :=
  inferInstanceAs (Decidable (∀ e ∈ g.edges, _))

theorem proper_iff_adj (g : SimpleGraph n) (c : Fin n → Fin k) :
    IsProperColoring g c ↔ ∀ a b, Adj g a b → c a ≠ c b := by
  constructor
  · intro h a b hab
    exact hab.elim (h (a,b)) (fun e => Ne.symm (h (b,a) e))
  · intro h e he
    exact h _ _ (Or.inl he)

def coloringCount (g : SimpleGraph n) (k : Nat) : Nat :=
  ((assignments k n).filter (fun c => decide (IsProperColoring g c))).length

def edgeFactors (es : List (Fin n × Fin n)) : List Query :=
  es.map fun (a,b) => .apart a.val b.val

def chiPoly (g : SimpleGraph n) : Poly :=
  compile (eliminate n (edgeFactors g.edges)) (r := 0) (fun _ => none)

private theorem edgeWeight (es : List (Fin n × Fin n)) (c : Fin n → Fin k) :
    run k (product (edgeFactors es)) (envOf c) =
    if ∀ e ∈ es, c e.1 ≠ c e.2 then 1 else 0 := by
  induction es with
  | nil => simp [edgeFactors,product,run]
  | cons e es ih =>
    obtain ⟨a,b⟩ := e
    change run k (.apart a.val b.val) (envOf c) * run k (product (edgeFactors es)) (envOf c) = _
    rw [ih]
    simp [run,envOf]
    split <;> split <;> simp_all

private theorem sum_indicator (xs : List α) (p : α → Prop) [DecidablePred p] :
    (xs.map (fun a => if p a then (1 : Int) else 0)).sum = (xs.filter (fun x => decide (p x))).length := by
  induction xs with
  | nil => rfl
  | cons x xs ih => by_cases h : p x <;> simp [h,ih] <;> omega

/-- The graph polynomial counts proper functions on every finite palette. -/
theorem chiPoly_counts (g : SimpleGraph n) (k : Nat) :
    (coloringCount g k : Int) = eval (chiPoly g) k := by
  unfold chiPoly
  rw [← compile_correct _ _ (Fin.elim0 : Fin 0 → Fin k) (fun i => i.elim0)]
  change _ = run k _ (fun _ => none)
  rw [eliminate_correct]
  simp only [edgeWeight]
  exact (sum_indicator (assignments k n) (IsProperColoring g)).symm

end Gamma

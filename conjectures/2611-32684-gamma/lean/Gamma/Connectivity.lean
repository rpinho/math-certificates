import Gamma.Witness

namespace Gamma

/-- Follow the vertices of a path in order, starting at a. -/
def follows (g : SimpleGraph n) (a : Fin n) : List (Fin n) → Prop
  | [] => True
  | b :: rest => Adj g a b ∧ follows g b rest

instance decFollows (g : SimpleGraph n) (a : Fin n) : (l : List (Fin n)) → Decidable (follows g a l)
  | [] => isTrue trivial
  | b :: rest => @instDecidableAnd _ _ (inferInstanceAs (Decidable (Adj g a b))) (decFollows g b rest)

def PathAvoiding (g : SimpleGraph n) (deleted : List (Fin n)) (a b : Fin n) : Prop :=
  ∃ tail, (a :: tail).Nodup ∧ follows g a tail ∧ (a :: tail).getLast? = some b ∧
    ∀ x ∈ a :: tail, x ∉ deleted

def ThreeConnected (g : SimpleGraph11) : Prop :=
  ∀ u v a b, a ∉ [u,v] → b ∉ [u,v] → PathAvoiding g [u,v] a b

private abbrev V := Fin 11
private abbrev Routes := List V × List V × List V

/-- Three internally disjoint routes per nonedge, stored by their interior
vertices only. Adjacent pairs use the direct edge (empty interior). -/
private def forward : Nat → Nat → Routes
  | 0, 1 => ([5], [6], [7])
  | 0, 2 => ([5], [6], [7])
  | 0, 3 => ([8], [9], [10])
  | 0, 4 => ([8], [9], [10])
  | 1, 2 => ([5], [6], [7])
  | 1, 4 => ([3, 9], [6, 2], [5, 0, 8])
  | 1, 8 => ([3], [6, 0], [5, 2, 4])
  | 1, 9 => ([3], [6, 0], [5, 2, 4])
  | 1, 10 => ([3], [6, 0], [5, 2, 4])
  | 2, 3 => ([4, 9], [6, 1], [5, 0, 8])
  | 2, 8 => ([4], [6, 0], [5, 1, 3])
  | 2, 9 => ([4], [6, 0], [5, 1, 3])
  | 2, 10 => ([4], [6, 0], [5, 1, 3])
  | 3, 4 => ([8], [9], [10])
  | 3, 5 => ([1], [9, 0], [8, 4, 2])
  | 3, 6 => ([1], [9, 0], [8, 4, 2])
  | 3, 7 => ([1], [9, 0], [8, 4, 2])
  | 4, 5 => ([2], [9, 0], [8, 3, 1])
  | 4, 6 => ([2], [9, 0], [8, 3, 1])
  | 4, 7 => ([2], [9, 0], [8, 3, 1])
  | 5, 6 => ([0], [1], [2])
  | 5, 7 => ([0], [1], [2])
  | 5, 8 => ([0], [1, 3], [2, 4])
  | 5, 9 => ([0], [1, 3], [2, 4])
  | 5, 10 => ([0], [1, 3], [2, 4])
  | 6, 7 => ([0], [1], [2])
  | 6, 8 => ([0], [1, 3], [2, 4])
  | 6, 9 => ([0], [1, 3], [2, 4])
  | 6, 10 => ([0], [1, 3], [2, 4])
  | 7, 8 => ([0], [1, 3], [2, 4])
  | 7, 9 => ([0], [1, 3], [2, 4])
  | 7, 10 => ([0], [1, 3], [2, 4])
  | 8, 9 => ([0], [3], [4])
  | 8, 10 => ([0], [3], [4])
  | 9, 10 => ([0], [3], [4])
  | _, _ => ([], [], [])

private def routes (a b : V) : Routes :=
  if a < b then forward a.val b.val else
    let (p,q,r) := forward b.val a.val
    (p.reverse,q.reverse,r.reverse)

private abbrev good (a b : V) (p : List V) :=
  (a :: (p ++ [b])).Nodup ∧ follows G a (p ++ [b])

private abbrev disjoint (p q : List V) := ∀ x ∈ p, x ∉ q

set_option maxHeartbeats 1000000 in
set_option maxRecDepth 4096 in
set_option synthInstance.maxSize 512 in
private theorem routes_checked : ∀ a b : V, a ≠ b →
    let p := (routes a b).1
    let q := (routes a b).2.1
    let r := (routes a b).2.2
    good a b p ∧ good a b q ∧ good a b r ∧ disjoint p q ∧ disjoint p r ∧ disjoint q r := by
  decide +kernel

private theorem usable (u v : V) (p q r : List V)
    (hpq : disjoint p q) (hpr : disjoint p r) (hqr : disjoint q r) :
    (u ∉ p ∧ v ∉ p) ∨ (u ∉ q ∧ v ∉ q) ∨ (u ∉ r ∧ v ∉ r) := by
  by_cases up : u ∈ p <;> by_cases vp : v ∈ p <;>
    by_cases uq : u ∈ q <;> by_cases vq : v ∈ q <;> grind

private theorem make_path (a b u v : V) (p : List V)
    (ha : a ∉ [u,v]) (hb : b ∉ [u,v]) (h : good a b p) (hp : u ∉ p ∧ v ∉ p) :
    PathAvoiding G [u,v] a b := by
  refine ⟨p ++ [b],h.1,h.2,?_,?_⟩
  · change ((a :: p) ++ [b]).getLast? = some b
    exact List.getLast?_concat
  · grind

theorem three_connected : ThreeConnected G := by
  intro u v a b ha hb
  by_cases eq : a = b
  · subst b
    exact ⟨[],by simp, trivial,rfl,by simpa using ha⟩
  · obtain ⟨p,q,r,hpq, hpr,hqr⟩ := routes_checked a b eq
    rcases usable u v _ _ _ hpq hpr hqr with h | h | h
    · exact make_path a b u v _ ha hb p h
    · exact make_path a b u v _ ha hb q h
    · exact make_path a b u v _ ha hb r h

theorem three_vertex_cut : ¬PathAvoiding G [0,1,2] 5 8 := by
  rintro ⟨tail,_,walk,finish,avoid⟩
  cases tail with
  | nil => contradiction
  | cons c rest =>
    have onlyNeighbors : ∀ d : V, Adj G 5 d → d ∈ [0,1,2] := by decide
    exact avoid c (by simp) (onlyNeighbors c walk.1)

end Gamma

import Dichrom.Sign

namespace Dichrom
variable {α β : Type} [DecidableEq β]

/-- Explicit enumeration of maps, by independent choices at the vertices. -/
def maps (cs : List β) : (n : Nat) → List (Fin n → β)
  | 0 => [Fin.elim0]
  | n+1 => cs.flatMap (fun c => (maps cs n).map (fun f => Fin.cases c f))

def put (g : β → List α) (c : β) (s : List α) (d : β) := if d = c then s else g d

def push (v : α) (c : β) (g : β → List α) := put g c (v::g c)

/-- The list of vertices of each colour, in vertex order. -/
def fibres : (l : List α) → (Fin l.length → β) → β → List α
  | [], _ => fun _ => []
  | v::t, f => push v (f 0) (fibres t (fun i => f i.succ))

def mapSum (cs : List β) (l : List α) (F : (β → List α) → Int) :=
  total (maps cs l.length) (fun f => F (fibres l f))

theorem map_nil (cs : List β) (F : (β → List α) → Int) :
    mapSum cs [] F = F (fun _ => []) := by simp [mapSum, maps, fibres, total]

theorem map_cons (cs : List β) (v : α) (t : List α) (F : (β → List α) → Int) :
    mapSum cs (v::t) F = total cs (fun c => mapSum cs t (fun g => F (push v c g))) := by
  simp [mapSum, maps, fibres]

private theorem swap_total {δ ε : Type} (s : List δ) (t : List ε) (f : δ → ε → Int) :
    total s (fun a => total t (f a)) = total t (fun b => total s (fun a => f a b)) := by
  induction s with
  | nil => simp [total]
  | cons a s ih => simp only [total, total_add, ih]

private theorem push_other (g : β → List α) (s : List α) (c d : β) (v : α) (h : d ≠ c) :
    push v d (put g c s) = put (push v d g) c s := by
  funext e; by_cases hd : e = d <;> by_cases hc : e = c <;> simp_all [push, put]

theorem palette_split (cs : List β) (c : β) (hc : c ∉ cs) (l : List α)
    (F : (β → List α) → Int) :
    mapSum (c::cs) l F =
      splitSum l (fun s r => mapSum cs r (fun g => F (put g c s))) := by
  induction l generalizing F with
  | nil =>
    simp only [map_nil, split_nil]
    congr 1; funext; simp [put]
  | cons v t ih =>
    rw [map_cons, split_cons]
    simp only [total, ih]
    congr 1
    · apply split_congr; intro s r _
      unfold mapSum
      apply total_congr; intro g _
      apply congrArg F; funext d; by_cases h : d = c <;> simp_all [put, push]
    · unfold splitSum
      rw [swap_total]
      apply total_congr; intro ⟨s,r⟩ _
      dsimp only
      rw [map_cons]
      apply total_congr; intro d hd
      have h : d ≠ c := by grind
      simp only [push_other _ _ _ _ _ h]

private theorem mark_count (p : Blocks α) (z : Nat → Int) :
    mark p (fun _ u => z u.length) = (p.length:Int) * z (p.length-1) := by
  induction p generalizing z with
  | nil => simp [mark]
  | cons b p ih =>
    simp only [mark, List.length_cons]
    rw [ih (fun k => z (k+1))]
    cases p <;> simp <;> grind

theorem palette_polynomial (A : System α) (l : List α) (x : Int) :
    P A.ok l (x+1) = splitSum l (fun s r => keep (A.ok s) (P A.ok r x)) := by
  rw [eraseEmptyAux]
  unfold P partSum
  rw [← total_add]
  apply total_congr; intro p _
  rw [mark_count]
  cases p with
  | nil => simp [fall]
  | cons b p =>
    simp only [List.length_cons, Nat.add_sub_cancel, fall]
    have := fall_right x p.length
    simp only [Int.natCast_succ] at *
    rw [show x+1-1=x by omega]
    grind
  where
    eraseEmptyAux : splitSum l (fun s r => keep (A.ok s) (P A.ok r x)) =
        P A.ok l x + partSum A.ok l (fun p => mark p (fun _ u => fall x u.length)) := by
      rw [pointing, ← split_empty_left l (fun r => P A.ok r x), ← split_add]
      apply split_congr; intro s r _
      cases s <;> simp [good, keep, P, A.empty]

def proper (A : System α) (cs : List β) (g : β → List α) := cs.all (fun c => A.ok (g c))

private theorem proper_put (A : System α) (cs : List β) (c : β) (hc : c ∉ cs)
    (s : List α) (g : β → List α) :
    proper A (c::cs) (put g c s) = (A.ok s && proper A cs g) := by
  unfold proper
  simp only [List.all_cons, put, ite_true]
  congr 1
  apply Bool.eq_iff_iff.mpr
  simp only [List.all_eq_true]
  constructor <;> intro h d hd
  all_goals
    have hn : d ≠ c := by grind
    simpa [hn] using h d hd

theorem count_maps (A : System α) (cs : List β) (hcs : cs.Nodup) (l : List α) :
    mapSum cs l (fun g => keep (proper A cs g) 1) = P A.ok l (cs.length:Int) := by
  induction cs generalizing l with
  | nil =>
    cases l with
    | nil => simp [map_nil, P, part_nil, fall, keep, proper]
    | cons v t => simp [map_cons, total, identity1]
  | cons c cs ih =>
    obtain ⟨hc,ht⟩ := List.nodup_cons.mp hcs
    rw [palette_split cs c hc, List.length_cons, Int.natCast_succ, palette_polynomial]
    apply split_congr; intro s r _
    simp only [proper_put A cs c hc]
    cases A.ok s <;> simp [keep]
    · simp [mapSum]
    · exact ih ht r

theorem total_indicator {δ : Type} (l : List δ) (f : δ → Bool) :
    total l (fun d => keep (f d) (1:Int)) = ((l.filter f).length:Int) := by
  induction l with
  | nil => rfl
  | cons a l ih => cases h : f a <;> simp_all [total, keep] <;> omega

theorem eval_eq_coloring_count (A : System (Fin n)) (x : Nat) :
    (polynomial A.ok (List.finRange n)).eval (x:Int) =
      (((maps (List.finRange x) (List.finRange n).length).filter (fun f =>
        proper A (List.finRange x) (fibres (List.finRange n) f))).length : Int) := by
  rw [eval_P, ← total_indicator]
  have h := count_maps A (List.finRange x) (List.nodup_finRange x) (List.finRange n)
  simpa only [List.length_finRange, mapSum] using h.symm

omit [DecidableEq β] in
theorem maps_nodup (cs : List β) (hc : cs.Nodup) (n : Nat) : (maps cs n).Nodup := by
  induction n with
  | zero => simp [maps]
  | succ n ih =>
    apply List.pairwise_flatMap.mpr
    constructor
    · intro c _
      apply List.pairwise_map.mpr
      apply ih.imp
      intro a b hab e
      apply hab; funext i
      exact congrFun e i.succ
    · apply hc.imp
      intro c d hcd f hf g hg e
      obtain ⟨u,_,rfl⟩ := List.mem_map.mp hf
      obtain ⟨v,_,rfl⟩ := List.mem_map.mp hg
      exact hcd (congrFun e 0)

theorem maps_complete (f : Fin n → Fin x) : f ∈ maps (List.finRange x) n := by
  induction n with
  | zero =>
    have e : f = Fin.elim0 := funext (fun i => i.elim0)
    simp [maps,e]
  | succ n ih =>
    apply List.mem_flatMap.mpr
    refine ⟨f 0, List.mem_finRange _, List.mem_map.mpr ⟨fun i => f i.succ, ih _, ?_⟩⟩
    funext i; exact Fin.cases rfl (fun _ => rfl) i

theorem mem_fibres (l : List α) (f : Fin l.length → β) (c : β) (a : α) :
    a ∈ fibres l f c ↔ ∃ i : Fin l.length, l[i] = a ∧ f i = c := by
  induction l generalizing c with
  | nil => simp [fibres]
  | cons v t ih =>
    simp only [fibres,push,put]
    by_cases hc : c = f 0
    · simp only [hc,ite_true,List.mem_cons,ih]
      constructor
      · rintro (rfl | ⟨i,hi,h⟩)
        · exact ⟨0,rfl,rfl⟩
        · exact ⟨i.succ,hi,h⟩
      · rintro ⟨i,hi,h⟩
        cases i using Fin.cases with
        | zero => exact Or.inl hi.symm
        | succ j => exact Or.inr ⟨j,hi,h⟩
    · simp only [hc,ite_false,ih]
      constructor
      · rintro ⟨i,hi,h⟩; exact ⟨i.succ,hi,h⟩
      · rintro ⟨i,hi,h⟩
        cases i using Fin.cases with
        | zero => exact False.elim (hc h.symm)
        | succ j => exact ⟨j,hi,h⟩

end Dichrom

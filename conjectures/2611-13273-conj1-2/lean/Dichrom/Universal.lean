import Dichrom.Theorems
import Dichrom.Coefficients

namespace Dichrom

theorem System.ok_perm (A : System α) (p : l.Perm m) : A.ok l = A.ok m :=
  Bool.eq_iff_iff.mpr ⟨A.down (fun _ h => p.mem_iff.mpr h), A.down (fun _ h => p.mem_iff.mp h)⟩

private theorem split_perm {l m : List α} (p : l.Perm m) (f : List α → List α → Int)
    (hf : ∀ {a b c d}, a.Perm b → c.Perm d → f a c = f b d) :
    splitSum l f = splitSum m f := by
  induction p generalizing f with
  | nil => rfl
  | cons a p ih =>
    rw [split_cons,split_cons,ih (fun s r => f (a::s) r) (fun h k => hf (.cons _ h) k),
      ih (fun s r => f s (a::r)) (fun h k => hf h (.cons _ k))]
  | swap a b t =>
    simp only [split_cons]
    have fst : splitSum t (fun s r => f (b::a::s) r) = splitSum t (fun s r => f (a::b::s) r) :=
      split_congr (fun s r _ => hf (.swap ..) (.refl r))
    have snd : splitSum t (fun s r => f s (b::a::r)) = splitSum t (fun s r => f s (a::b::r)) :=
      split_congr (fun s r _ => hf (.refl s) (.swap ..))
    grind only
  | trans p q ih jh => exact (ih f hf).trans (jh f hf)

theorem polynomial_perm (A : System α) {l m : List α} (p : l.Perm m) :
    (polynomial A.ok l).coeffs = (polynomial A.ok m).coeffs := by
  apply coeffs_ext _ _ 0
  intro x hx
  clear hx
  simp only [eval_P]
  induction x generalizing l m with
  | zero =>
    cases l <;> cases m <;> first | rfl | (have := p.length_eq; simp at this; done) | (simp [identity1])
  | succ x ih =>
    rw [Int.natCast_succ,palette_polynomial,palette_polynomial]
    apply split_perm p
    intro a b c d hab hcd
    rw [A.ok_perm hab, ih hcd]

theorem defect_perm (A : System α) {l m : List α} (p : l.Perm m) :
    (defect A.ok l).formal = (defect A.ok m).formal := by
  apply Quotient.sound (s:=polynomialSetoid)
  intro K inst x
  rw [eval_H,eval_H]
  simp only [H,← eval_dP,← eval_P]
  rw [← deriv_coeffs,← deriv_coeffs,← eval_coeffs x (polynomial _ l),← eval_coeffs x (polynomial _ m),
    polynomial_perm A p,p.length_eq]

/-- The vertex list may always be reordered to put any requested pivot first. -/
theorem at_vertex [DecidableEq α] (A : System α) (l : List α) (v : α) (h : v ∈ l) :
    (polynomial A.ok l).formal = (polynomial A.ok (v::l.erase v)).formal ∧
    (defect A.ok l).formal = (defect A.ok (v::l.erase v)).formal := by
  have p := List.perm_cons_erase h
  exact ⟨(formal_iff_coeffs ..).mpr (polynomial_perm A p), defect_perm A p⟩

private theorem total_const {δ : Type} (l : List δ) (a : Int) :
    total l (fun _ => a) = (l.length:Int)*a := by
  induction l <;> simp_all [total] <;> grind

private theorem all_maps_count (cs : List β) [DecidableEq β] (l : List α) :
    mapSum cs l (fun _ => 1) = (cs.length:Int)^l.length := by
  induction l with
  | nil => simp [map_nil]
  | cons v t ih => simp [map_cons,ih,total_const,Int.pow_succ]; grind

theorem acyclic_polynomial (A : System α) (l : List α) (ha : A.ok l = true) :
    (polynomial A.ok l).formal = (xPower l.length).formal := by
  apply (formal_iff_coeffs ..).mpr
  apply coeffs_ext _ _ 0
  intro x _
  let cs := List.finRange x
  have cnt := count_maps A cs (List.nodup_finRange _) l
  have allgood (f : Fin l.length → Fin x) : proper A cs (fibres l f) = true := by
    apply List.all_eq_true.mpr
    intro c _
    apply A.down (t:=l) _ ha
    intro a h
    obtain ⟨i,hi,_⟩ := (mem_fibres ..).mp h
    exact hi ▸ List.getElem_mem ..
  have plain : mapSum cs l (fun g => keep (proper A cs g) 1) = mapSum cs l (fun _ => 1) := by
    apply total_congr; intro f _
    change keep (proper A cs (fibres l f)) 1 = 1
    rw [allgood]; rfl
  rw [plain,all_maps_count] at cnt
  simpa only [cs,List.length_finRange,eval_P,power_eval] using cnt.symm

theorem dag_normalized (A : System α) (l : List α) (ha : A.ok l = true) (q : Rat) (hq : 0 < q) :
    normalized A l q = 1 := by
  have e := Quotient.exact (s:=polynomialSetoid) (acyclic_polynomial A l ha)
  have eqn := e Rat q
  simp only [eval_P,power_eval] at eqn
  unfold normalized
  rw [eqn]
  have nz := Rat.ne_of_gt (Rat.pow_pos hq (n:=l.length))
  grind

theorem cleared_nonnegative (A : System (Fin n)) (_hn : 2 ≤ n) (a b : Int) (hb : 0 < b)
    (hq : (n:Rat)-1 ≤ (a:Rat)/(b:Rat)) : 0 ≤ (defect A.ok (vertices n)).cleared a b := by
  apply Rat.intCast_nonneg.mp
  rw [cleared_eval _ _ _ hb,eval_H]
  exact Rat.mul_nonneg (Rat.pow_nonneg (Rat.le_of_lt (Rat.intCast_pos.mpr hb)))
    (nonnegative A _ _ (by simpa [vertices] using hq))

theorem cleared_positive (A : System (Fin n)) (_hn : 2 ≤ n) (a b : Int) (hb : 0 < b)
    (hq : (n:Rat)-1 < (a:Rat)/(b:Rat)) (bad : A.ok (vertices n) = false) :
    0 < (defect A.ok (vertices n)).cleared a b := by
  apply Rat.intCast_pos.mp
  rw [cleared_eval _ _ _ hb,eval_H]
  exact Rat.mul_pos (Rat.pow_pos (Rat.intCast_pos.mpr hb))
    (positive A _ _ bad (by simpa [vertices] using hq))

end Dichrom

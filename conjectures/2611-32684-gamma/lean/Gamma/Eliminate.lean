import Gamma.Query

namespace Gamma

def free (v : Nat) : Query → Bool
  | .one => false
  | .apart i j => v == i || v == j
  | .mul a b => free v a || free v b
  | .bind i a => v != i && free v a

private theorem run_congr (q : Query) (s t : Env k)
    (h : ∀ i, free i q = true → s i = t i) : run k q s = run k q t := by
  induction q generalizing s t with
  | one => rfl
  | apart i j =>
    have hi := h i (by simp [free])
    have hj := h j (by simp [free])
    simp [run,hi,hj]
  | mul a b ha hb =>
    rw [run,run,ha s t (by intro i hi; apply h; simp [free,hi]),
      hb s t (by intro i hi; apply h; simp [free,hi])]
  | bind v a ih =>
    apply congrArg total
    funext c
    apply ih
    intro i hi
    by_cases eq : i = v
    · simp [put,eq]
    · simp [put,eq,h i (by simp [free,eq,hi])]

def product : List Query → Query
  | [] => .one
  | a :: as => .mul a (product as)

/-- Bind only factors depending on v. All other factors can be pulled out
of this color sum. In particular the six leaves of G are summed separately. -/
def sumOut (v : Nat) (fs : List Query) : List Query :=
  .bind v (product (fs.filter (free v))) :: fs.filter (fun f => !free v f)

private theorem split_factors (fs : List Query) (p : Query → Bool) (s : Env k) :
    run k (product fs) s =
      run k (product (fs.filter p)) s * run k (product (fs.filter (fun f => !p f))) s := by
  induction fs with
  | nil => rfl
  | cons f fs ih => cases h : p f <;> simp [product,run,h,ih] <;> grind

private theorem fixed_factors (fs : List Query) (v : Nat) (s : Env k) (c : Fin k) :
    run k (product (fs.filter (fun f => !free v f))) (put s v c) =
    run k (product (fs.filter (fun f => !free v f))) s := by
  induction fs with
  | nil => rfl
  | cons f fs ih =>
    cases h : free v f
    · have hf : run k f (put s v c) = run k f s := by
        apply run_congr
        intro i hi
        have hn : i ≠ v := by grind
        simp [put,hn]
      simp [h,product,run,hf,ih]
    · simpa [h] using ih

theorem sumOut_correct (fs : List Query) (v : Nat) (s : Env k) :
    run k (product (sumOut v fs)) s = total (fun c => run k (product fs) (put s v c)) := by
  change total _ * _ = _
  rw [← total_mul]
  apply congrArg total
  funext c
  rw [split_factors fs (free v),fixed_factors]

def eliminate : Nat → List Query → Query
  | 0, fs => product fs
  | n+1, fs => eliminate n (sumOut n fs)

def extendColor (f : Fin n → Fin k) (d : Fin k) : Fin (n+1) → Fin k :=
  Fin.lastCases d f

/-- Enumeration of actual functions; the inner loop chooses the last coordinate. -/
def assignments (k : Nat) : (n : Nat) → List (Fin n → Fin k)
  | 0 => [Fin.elim0]
  | n+1 => (assignments k n).flatMap fun f => (List.finRange k).map (extendColor f)

theorem mem_assignments (f : Fin n → Fin k) : f ∈ assignments k n := by
  induction n with
  | zero =>
    have h : f = Fin.elim0 := funext fun i => i.elim0
    simp [assignments,h]
  | succ n ih =>
    apply List.mem_flatMap.mpr
    refine ⟨_, ih (fun i => f i.castSucc), List.mem_map.mpr ⟨_,List.mem_finRange (f (Fin.last n)),?_⟩⟩
    funext i
    induction i using Fin.lastCases <;> simp [extendColor]

theorem nodup_assignments (k n : Nat) : (assignments k n).Nodup := by
  induction n with
  | zero => simp [assignments]
  | succ n ih =>
    apply List.pairwise_flatMap.mpr
    constructor
    · intro f _
      apply List.pairwise_map.mpr
      apply (List.nodup_finRange k).imp
      intro a b hab eq
      exact hab (by simpa [extendColor] using congrFun eq (Fin.last n))
    · apply ih.imp
      intro f g h x hx y hy eq
      obtain ⟨a,_,rfl⟩ := List.mem_map.mp hx
      obtain ⟨b,_,rfl⟩ := List.mem_map.mp hy
      apply h
      funext i
      simpa [extendColor] using congrFun eq i.castSucc

private def weight (xs : List α) (f : α → Int) := (xs.map f).sum

private theorem weight_flat (xs : List α) (ys : α → List β) (f : β → Int) :
    weight (xs.flatMap ys) f = weight xs (fun x => weight (ys x) f) := by
  induction xs <;> simp_all [weight]

private theorem weight_fin (f : Fin n → Int) : weight (List.finRange n) f = total f := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [List.finRange_succ,weight,List.map_cons,List.map_map,List.sum_cons,total,over]
    exact congrArg (f 0 + ·) (ih (fun i => f i.succ))

def envOf (f : Fin n → Fin k) : Env k :=
  fun i => if h : i < n then some (f ⟨i,h⟩) else none

private theorem env_extend (f : Fin n → Fin k) (d : Fin k) :
    envOf (extendColor f d) = put (envOf f) n d := by
  funext i
  by_cases hi : i < n
  · have h : i < n+1 := by omega
    have hn : i ≠ n := by omega
    simp only [envOf,put,hi,h,hn, dite_true,ite_false]
    exact congrArg some (Fin.lastCases_castSucc (i := (⟨i,hi⟩ : Fin n)) ..)
  · by_cases hn : i = n
    · subst i; simp [envOf,put,extendColor,show (⟨n, by omega⟩ : Fin (n+1)) = Fin.last n from rfl]
    · have h : ¬ i < n+1 := by omega
      simp [envOf,put,hi,h,hn]

theorem eliminate_correct (n k : Nat) (fs : List Query) :
    run k (eliminate n fs) (fun _ => none) =
      ((assignments k n).map (fun f => run k (product fs) (envOf f))).sum := by
  change _ = weight _ _
  induction n generalizing fs with
  | zero =>
    have h : envOf (Fin.elim0 : Fin 0 → Fin k) = fun _ => none := by funext i; simp [envOf]
    simp [eliminate,assignments,weight,h]
  | succ n ih =>
    rw [eliminate,ih,assignments,weight_flat]
    congr 1
    funext f
    rw [sumOut_correct,← weight_fin]
    simp [weight,List.map_map,Function.comp_def,env_extend]

end Gamma

import Gamma.Counting

namespace Gamma

/-- Expressions for finite color sums. A product of separate sums expresses
independent choices of colors after their common neighbors have been colored. -/
inductive Query where
  | one
  | apart (i j : Nat)
  | mul (a b : Query)
  | bind (v : Nat) (a : Query)
  deriving Repr

abbrev Env (r : Nat) := Nat → Option (Fin r)

def put (s : Env r) (v : Nat) (c : Fin r) : Env r :=
  fun i => if i = v then some c else s i

def run (k : Nat) : Query → Env k → Int
  | .one, _ => 1
  | .apart i j, s => if s i = s j then 0 else 1
  | .mul a b, s => run k a s * run k b s
  | .bind v a, s => total fun c => run k a (put s v c)

/-- Partition the next color into the r named possibilities and one fresh
equality pattern, with multiplicity X-r. -/
def compile : Query → {r : Nat} → Env r → Poly
  | .one, _, _ => [1]
  | .apart i j, _, s => if s i = s j then [] else [1]
  | .mul a b, _, s => times (compile a s) (compile b s)
  | .bind v a, r, s =>
    plus (over [] plus (fun c => compile a (put s v c)))
      (linear r (compile a (put (fun i => (s i).map Fin.succ) v 0)))

private theorem map_inj (e : Fin r → Fin k) (he : ∀ i j, e i = e j → i = j)
    (x y : Option (Fin r)) : x.map e = y.map e ↔ x = y := by
  cases x <;> cases y <;> simp_all <;> grind

private theorem map_put (e : Fin r → Fin k) (s : Env r) (v : Nat) (c : Fin r) :
    (fun i => ((put s v c) i).map e) = put (fun i => (s i).map e) v (e c) := by
  funext i; by_cases h : i = v <;> simp [put,h]

private def extend (e : Fin r → Fin k) (c : Fin k) : Fin (r+1) → Fin k :=
  Fin.cases c e

private theorem extend_inj (e : Fin r → Fin k) (he : ∀ i j, e i = e j → i = j)
    (c : Fin k) (hc : ∀ i, e i ≠ c) : ∀ i j, extend e c i = extend e c j → i = j := by
  intro i j
  induction i using Fin.cases <;> induction j using Fin.cases <;> simp_all [extend, Fin.cases_succ]
  all_goals grind

theorem compile_correct (q : Query) (s : Env r) (e : Fin r → Fin k)
    (he : ∀ i j, e i = e j → i = j) :
    run k q (fun i => (s i).map e) = eval (compile q s) k := by
  induction q generalizing r with
  | one => simp [run,compile,eval]
  | apart i j => simp [run,compile,map_inj e he]; split <;> simp [eval]
  | mul a b ha hb => simp [run,compile,eval_times,ha s e he,hb s e he]
  | bind v a ih =>
    simp only [run,compile,eval_plus,eval_over,linear,eval_scale,eval_shift]
    let fresh := put (fun i => (s i).map Fin.succ) v (0 : Fin (r+1))
    let f := fun c => run k a (put (fun i => (s i).map e) v c)
    have old (i : Fin r) : f (e i) = eval (compile a (put s v i)) k := by
      simpa [f,map_put] using ih (put s v i) e he
    have newColor (c : Fin k) (hc : ∀ i, e i ≠ c) : f c = eval (compile a fresh) k := by
      have h := ih fresh (extend e c) (extend_inj e he c hc)
      have eq : (fun i => (fresh i).map (extend e c)) = put (fun i => (s i).map e) v c := by
        funext i
        by_cases hi : i = v
        · simp [fresh,put,hi,extend]
        · cases h : s i <;> simp [fresh,put,hi,h,extend,Fin.cases_succ]
      simpa [eq,f] using h
    have h := palette_split e he f (eval (compile a fresh) k) newColor
    simp only [old] at h
    change total f = _ + (-(r : Int) * eval (compile a fresh) k + (k : Int)*eval (compile a fresh) k)
    grind

end Gamma

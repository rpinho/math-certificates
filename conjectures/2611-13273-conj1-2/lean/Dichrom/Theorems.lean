import Dichrom.Digraph
import Dichrom.Rational

namespace Dichrom

def xPower : Nat → Poly
  | 0 => .C 1
  | n+1 => .mul (xPower n) .X

theorem power_eval {K : Type} [Lean.Grind.CommRing K] (n : Nat) (x : K) :
    (xPower n).eval x = x^n := by
  induction n <;> simp_all only [xPower, Poly.eval, Lean.Grind.Semiring.pow_succ,
    Lean.Grind.Semiring.pow_zero] <;> grind

private theorem power_deriv (n : Nat) (x : Rat) :
    (xPower (n+1)).deriv.eval x = ((n+1:Nat):Rat)*x^n := by
  induction n with
  | zero => simp [xPower, Poly.deriv, Poly.eval]; grind
  | succ n ih =>
    change (xPower (n+1)).deriv.eval x*x+(xPower (n+1)).eval x*((1:Int):Rat) = _
    rw [ih,power_eval,Rat.pow_succ]
    simp only [Rat.natCast_add]; grind

private theorem power_ge_one (x : Rat) (hx : 1 ≤ x) (n : Nat) : 1 ≤ x^n := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Rat.pow_succ]
    have := Rat.mul_le_mul_of_nonneg_left hx (show 0 ≤ x^n by grind)
    grind

private theorem numerator (A : System α) (l : List α) (x : Rat) (n : Nat)
    (hn : l.length=n+1) :
    (polynomial A.ok l).deriv.eval x*(xPower (n+1)).eval x -
    (polynomial A.ok l).eval x*(xPower (n+1)).deriv.eval x = x^n*H A.ok l x := by
  simp only [power_eval,power_deriv,eval_P,eval_dP,H,hn,Rat.pow_succ]
  grind

def normalized (A : System α) (l : List α) (x : Rat) := P A.ok l x / x^l.length

theorem monotone (A : System α) (l : List α) (hn : 2 ≤ l.length)
    (r s : Rat) (hr : (l.length:Rat)-1 ≤ r) (hrs : r ≤ s) :
    normalized A l r ≤ normalized A l s := by
  obtain ⟨n,hlen⟩ : ∃ n, l.length = n+1 := ⟨l.length-1,by omega⟩
  have htwo := Rat.natCast_le_natCast.mpr hn
  have r1 : 1 ≤ r := by grind
  have h := quotient_monotone (polynomial A.ok l) (xPower (n+1)) r s (by grind) hrs
    (fun a ha _ => by rw [power_eval]; exact power_ge_one a (Rat.le_trans r1 ha) _)
    (fun a ha _ => by
      rw [numerator A l a n hlen]
      exact Rat.mul_nonneg (Rat.pow_nonneg (by grind)) (nonnegative A l a (Rat.le_trans hr ha)))
  simpa only [normalized,eval_P,power_eval,hlen] using h

theorem strict_mono (A : System α) (l : List α) (hn : 2 ≤ l.length) (bad : A.ok l = false)
    (r s : Rat) (hr : (l.length:Rat)-1 ≤ r) (hrs : r < s) :
    normalized A l r < normalized A l s := by
  obtain ⟨n,hlen⟩ : ∃ n, l.length = n+1 := ⟨l.length-1,by omega⟩
  let a := (r+s)/2
  have mid : r < a ∧ a < s := by dsimp [a]; grind
  have htwo := Rat.natCast_le_natCast.mpr hn
  have ha : 0 < a := by grind
  have left := monotone A l hn r a hr (Rat.le_of_lt mid.1)
  obtain ⟨b,hab,hbs,rise⟩ := quotient_rises (polynomial A.ok l) (xPower (n+1)) a s
    (Rat.le_of_lt ha) mid.2 (fun b hb _ => by rw [power_eval]; exact Rat.pow_pos (by grind))
    (by rw [numerator A l a n hlen]; exact Rat.mul_pos (Rat.pow_pos ha) (positive A l a bad (by grind)))
  have right := monotone A l hn b s (by grind) hbs
  have inside : normalized A l a < normalized A l b := by
    simpa only [normalized,eval_P,power_eval,hlen] using rise
  grind only

theorem eval_integer (p : Poly) (z : Int) : p.eval (z:Rat) = ((p.eval z:Int):Rat) := by
  induction p <;> simp_all [Poly.eval]

abbrev vertices (n : Nat) := List.finRange n

theorem theoremA (D : Digraph n) (_hn : 2 ≤ n) (q : Rat) (hq : (n:Rat)-1 ≤ q) :
    (defect D.acyclic (vertices n)).eval q ≥ 0 := by
  rw [eval_H]
  exact nonnegative D.system _ q (by simpa [vertices] using hq)

theorem theoremA_strict (D : Digraph n) (_hn : 2 ≤ n) (q : Rat) (hq : (n:Rat)-1 < q)
    (cycle : D.Cyclic (vertices n)) : 0 < (defect D.acyclic (vertices n)).eval q := by
  rw [eval_H]
  exact positive D.system _ q ((D.acyclic_false _).mpr cycle) (by simpa [vertices] using hq)

theorem theoremB (D : Digraph n) (hn : 2 ≤ n) (r s : Rat) (hr : (n:Rat)-1 ≤ r) (hrs : r ≤ s) :
    (polynomial D.acyclic (vertices n)).eval r / r^n ≤
      (polynomial D.acyclic (vertices n)).eval s / s^n := by
  simpa only [eval_P,normalized,vertices,List.length_finRange,Digraph.system] using
    monotone D.system (vertices n) (by simpa [vertices] using hn) r s
      (by simpa [vertices] using hr) hrs

theorem theoremB_strict (D : Digraph n) (hn : 2 ≤ n) (r s : Rat)
    (hr : (n:Rat)-1 ≤ r) (hrs : r < s) (cycle : D.Cyclic (vertices n)) :
    (polynomial D.acyclic (vertices n)).eval r / r^n <
      (polynomial D.acyclic (vertices n)).eval s / s^n := by
  simpa only [eval_P,normalized,vertices,List.length_finRange,Digraph.system] using
    strict_mono D.system (vertices n) (by simpa [vertices] using hn) ((D.acyclic_false _).mpr cycle)
      r s (by simpa [vertices] using hr) hrs

private theorem clear_le (u v a b : Rat) (ha : 0 < a) (hb : 0 < b) :
    u/a ≤ v/b ↔ u*b ≤ v*a := by
  have eqn : (u/a-v/b)*(a*b) = u*b-v*a := by
    rw [show (u/a-v/b)*(a*b)=(u/a*a)*b-(v/b*b)*a by grind only,
        Rat.div_mul_cancel (Rat.ne_of_gt ha), Rat.div_mul_cancel (Rat.ne_of_gt hb)]
  have pos := Rat.mul_pos ha hb
  constructor
  · intro h
    have le := Rat.mul_le_mul_of_nonneg_right (show u/a-v/b ≤ 0 by grind only) (Rat.le_of_lt pos)
    rw [eqn] at le
    grind only
  · intro h
    have le : (u/a-v/b)*(a*b) ≤ 0*(a*b) := by rw [eqn]; grind only
    have := Rat.le_of_mul_le_mul_right le pos
    grind only

theorem shameful (A : System (Fin n)) (hn : 2 ≤ n) :
    (polynomial A.ok (vertices n)).eval (n:Int) * ((n:Int)-1)^n ≥
      (polynomial A.ok (vertices n)).eval ((n:Int)-1) * (n:Int)^n := by
  let p := polynomial A.ok (vertices n)
  have two := Rat.natCast_le_natCast.mpr hn
  have lo : 0 < (n:Rat)-1 := by grind
  have hi : 0 < (n:Rat) := by grind
  have h := monotone A (vertices n) (by simp [vertices,hn]) ((n:Rat)-1) (n:Rat)
    (by simp [vertices]) (by grind)
  change P A.ok _ _ / _ ≤ P A.ok _ _ / _ at h
  simp only [vertices,List.length_finRange,← eval_P] at h
  have e := (clear_le _ _ _ _ (Rat.pow_pos lo) (Rat.pow_pos hi)).mp h
  apply Rat.intCast_le_intCast.mp
  simp only [Rat.intCast_mul,Rat.intCast_pow,Rat.intCast_sub,Rat.intCast_one, Rat.intCast_natCast]
  have ep : p.eval ((n:Rat)-1) = ((p.eval ((n:Int)-1):Int):Rat) := by
    simpa only [Rat.intCast_sub,Rat.intCast_one,Rat.intCast_natCast] using eval_integer p ((n:Int)-1)
  have en : p.eval (n:Rat) = ((p.eval (n:Int):Int):Rat) := eval_integer p (n:Int)
  change p.eval _ * _ ≤ p.eval _ * _ at e
  rwa [ep,en] at e

theorem shameful_strict (A : System (Fin n)) (hn : 2 ≤ n) (bad : A.ok (vertices n) = false) :
    (polynomial A.ok (vertices n)).eval ((n:Int)-1) * (n:Int)^n <
      (polynomial A.ok (vertices n)).eval (n:Int) * ((n:Int)-1)^n := by
  let p := polynomial A.ok (vertices n)
  have two := Rat.natCast_le_natCast.mpr hn
  have lo : 0 < (n:Rat)-1 := by grind
  have hi : 0 < (n:Rat) := by grind
  have h := strict_mono A (vertices n) (by simp [vertices,hn]) bad ((n:Rat)-1) (n:Rat)
    (by simp [vertices]) (by grind)
  simp only [normalized,vertices,List.length_finRange,← eval_P] at h
  have en (z : Int) : p.eval (z:Rat) = ((p.eval z:Int):Rat) := eval_integer p z
  change p.eval ((n:Int)-1)*(n:Int)^n < p.eval (n:Int)*((n:Int)-1)^n
  apply Rat.intCast_lt_intCast.mp
  simp only [Rat.intCast_mul,Rat.intCast_pow,← en,Rat.intCast_sub,Rat.intCast_one,Rat.intCast_natCast]
  apply Classical.byContradiction
  intro fail
  have backwards := (clear_le (p.eval (n:Rat)) (p.eval ((n:Rat)-1)) _ _
    (Rat.pow_pos hi (n:=n)) (Rat.pow_pos lo (n:=n))).mpr (Rat.not_lt.mp fail)
  exact (Rat.not_le.mpr h) backwards

end Dichrom

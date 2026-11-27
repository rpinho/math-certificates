import Dichrom.Partitions

namespace Dichrom
open Lean.Grind
attribute [local instance] Semiring.natCast Ring.intCast
variable {α K : Type} [CommRing K]

/-- Integer polynomial expressions. Polynomial identities below hold under
evaluation in every commutative ring at every element, including at X in ℤ[X]. -/
inductive Poly where
  | C (a : Int) | X | add (p q : Poly) | mul (p q : Poly)
deriving Repr

def Poly.eval (x : K) : Poly → K
  | .C a => (a : K)
  | .X => x
  | .add p q => p.eval x + q.eval x
  | .mul p q => p.eval x * q.eval x

def Poly.deriv : Poly → Poly
  | .C _ => .C 0
  | .X => .C 1
  | .add p q => .add p.deriv q.deriv
  | .mul p q => .add (.mul p.deriv q) (.mul p q.deriv)

def sumPoly (l : List α) (f : α → Poly) : Poly :=
  match l with
  | [] => .C 0
  | a::t => .add (f a) (sumPoly t f)

def falling (z : Poly) : Nat → Poly
  | 0 => .C 1
  | k+1 => .mul z (falling (.add z (.C (-1))) k)

def polynomial (ok : List α → Bool) (l : List α) :=
  sumPoly (parts ok l) (fun p => falling .X p.length)

def defect (ok : List α → Bool) (l : List α) : Poly :=
  let p := polynomial ok l
  .add (.mul .X p.deriv) (.mul (.C (-(l.length : Int))) p)

def fall (x : K) : Nat → K
  | 0 => 1
  | k+1 => x * fall (x-1) k

def dfall (x : K) : Nat → K
  | 0 => 0
  | k+1 => fall (x-1) k + x * dfall (x-1) k

def P (ok : List α → Bool) (l : List α) (x : K) :=
  partSum ok l (fun p => fall x p.length)

def dP (ok : List α → Bool) (l : List α) (x : K) :=
  partSum ok l (fun p => dfall x p.length)

def H (ok : List α → Bool) (l : List α) (x : K) := x * dP ok l x - (l.length : K) * P ok l x

theorem eval_sumPoly (x : K) (l : List α) (f : α → Poly) :
    (sumPoly l f).eval x = total l (fun a => (f a).eval x) := by
  induction l <;> simp_all [sumPoly, total, Poly.eval] <;> grind

theorem deriv_sumPoly (x : K) (l : List α) (f : α → Poly) :
    (sumPoly l f).deriv.eval x = total l (fun a => (f a).deriv.eval x) := by
  induction l <;> simp_all [sumPoly, total, Poly.eval, Poly.deriv] <;> grind

theorem eval_falling (x : K) (z : Poly) (k : Nat) :
    (falling z k).eval x = fall (z.eval x) k := by
  have e (a : K) : a + ((-1:Int):K) = a - 1 := by grind
  induction k generalizing z <;> simp_all [falling, Poly.eval, fall] <;> grind

theorem deriv_falling (x : K) (z : Poly) (k : Nat) :
    (falling z k).deriv.eval x = z.deriv.eval x * dfall (z.eval x) k := by
  induction k generalizing z <;>
    simp_all [falling, Poly.deriv, Poly.eval, dfall, eval_falling] <;> grind

theorem eval_P (ok : List α → Bool) (l : List α) (x : K) :
    (polynomial ok l).eval x = P ok l x := by
  simp [polynomial, eval_sumPoly, eval_falling, Poly.eval, P, partSum]

theorem eval_dP (ok : List α → Bool) (l : List α) (x : K) :
    (polynomial ok l).deriv.eval x = dP ok l x := by
  simp only [polynomial, deriv_sumPoly, deriv_falling, Poly.deriv, Poly.eval, dP, partSum]
  apply total_congr; intros; grind

theorem eval_H (ok : List α → Bool) (l : List α) (x : K) :
    (defect ok l).eval x = H ok l x := by
  simp only [defect, Poly.eval, eval_P, eval_dP, H]
  have e : ((l.length : Int) : K) = (l.length : K) := by
    exact (Ring.intCast_ofNat _).trans (Semiring.ofNat_eq_natCast _)
  grind

theorem fall_right (x : K) (k : Nat) : x * fall (x-1) k = (x-(k:K)) * fall x k := by
  induction k generalizing x with
  | zero => simp [fall]; grind
  | succ k ih =>
    simp only [fall]
    have e := ih (x-1)
    rw [Semiring.natCast_add, Semiring.natCast_one]
    grind

private theorem part_linear (l : List (Blocks α)) (x : K) (k : Blocks α → Nat) :
    total l (fun p => fall (x-1) (k p) + x * dfall (x-1) (k p)) =
    total l (fun p => fall (x-1) (k p)) + x * total l (fun p => dfall (x-1) (k p)) := by
  rw [total_add, total_mul]

theorem identity1 (ok : List α → Bool) (v : α) (l : List α) (x : K) :
    P ok (v::l) x = x * splitSum l (fun s r => keep (ok (v::s)) (P ok r (x-1))) := by
  unfold P
  rw [part_cons, ← split_mul]
  apply split_congr; intro s r _
  cases ok (v::s) <;> simp [keep, partSum, fall, total_mul, Semiring.mul_zero]

theorem derivative1 (ok : List α → Bool) (v : α) (l : List α) (x : K) :
    dP ok (v::l) x = splitSum l (fun s r => keep (ok (v::s))
      (P ok r (x-1) + x * dP ok r (x-1))) := by
  unfold dP
  rw [part_cons]; apply split_congr; intro s r _
  cases ok (v::s) <;> simp [keep, dfall, P, partSum, part_linear]

theorem identity2 (ok : List α → Bool) (v : α) (l : List α) (x : K) :
    (x-1) * H ok (v::l) x =
    x^2 * splitSum l (fun s r => keep (ok (v::s)) (H ok r (x-1))) +
    x * splitSum l (fun s r => keep (ok (v::s))
      (((l.length:K) - x*(s.length:K)) * P ok r (x-1))) := by
  simp only [H, identity1, derivative1, List.length_cons, Semiring.natCast_add, Semiring.natCast_one]
  have lin (a b : K) (f g : List α → List α → K) :
      a * splitSum l f - b * splitSum l g = splitSum l (fun s r => a * f s r - b * g s r) := by
    have sub (z w : K) : z - b*w = z + (-b)*w := by grind
    simp only [sub, split_add, split_mul]
  rw [show ∀ a b c : K, (x-1)*(x*a-(c+1)*(x*b)) =
      ((x-1)*x)*a - ((x-1)*(c+1)*x)*b by intros; grind]
  rw [lin, ← split_mul, ← split_mul, ← split_add]
  apply split_congr; intro s r hr
  have hn := congrArg (fun n : Nat => (n:K)) (split_size hr)
  simp only [Semiring.natCast_add] at hn
  cases ok (v::s) <;> simp only [keep, Bool.false_eq_true, ite_false, ite_true] <;> grind

end Dichrom

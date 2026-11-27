import Dichrom.Formal

namespace Dichrom
open Lean.Grind
attribute [local instance] Ring.intCast Semiring.natCast
variable {K : Type} [CommRing K]

def horner (x : K) : List Int → K
  | [] => 0
  | a::t => (a:K) + x*horner x t

private def addC : List Int → List Int → List Int
  | [], u => u
  | t, [] => t
  | a::t,b::u => (a+b)::addC t u

private def mulC : List Int → List Int → List Int
  | [], _ => []
  | a::t,u => addC (u.map (a*·)) (0::mulC t u)

private def rawCoeffs : Poly → List Int
  | .C z => [z]
  | .X => [0,1]
  | .add p q => addC (rawCoeffs p) (rawCoeffs q)
  | .mul p q => mulC (rawCoeffs p) (rawCoeffs q)

private def consC (a : Int) (l : List Int) :=
  if l.isEmpty && a == 0 then [] else a::l

private def trim : List Int → List Int
  | [] => []
  | a::t => consC a (trim t)

/-- Monomial coefficients, constant first, with all trailing zeros removed. -/
def Poly.coeffs (p : Poly) := trim (rawCoeffs p)

private theorem add_eval (x : K) (l m : List Int) :
    horner x (addC l m) = horner x l + horner x m := by
  induction l generalizing m with
  | nil => simp [addC,horner]; grind
  | cons a l ih => cases m <;> simp only [addC,horner,ih,Ring.intCast_add] <;> grind

private theorem mul_eval (x : K) (l m : List Int) :
    horner x (mulC l m) = horner x l * horner x m := by
  have scale (a : Int) : horner x (m.map (a*·)) = (a:K)*horner x m := by
    induction m <;> simp_all [horner,Ring.intCast_mul] <;> grind
  induction l <;> simp_all only [mulC,horner,add_eval] <;> grind

private theorem consC_eval (x : K) (a : Int) (t : List Int) :
    horner x (consC a t) = (a:K)+x*horner x t := by
  unfold consC
  split
  · rename_i h
    simp at h
    simp [h,horner]; grind
  · rfl

private theorem trim_eval (x : K) (l : List Int) : horner x (trim l) = horner x l := by
  induction l <;> simp_all only [trim,horner,consC_eval]

theorem eval_coeffs (x : K) (p : Poly) : horner x p.coeffs = p.eval x := by
  simp only [Poly.coeffs,trim_eval]
  induction p <;> simp_all only [Poly.eval,rawCoeffs,horner,add_eval,mul_eval] <;> grind

private theorem expand_head (x : Int) (l : List Int) :
    horner x l = l.headD 0 + x*horner x l.tail := by
  cases l <;> simp [horner]

private theorem tails_shorter (l m : List Int) (h : ¬ (l=[] ∧ m=[])) :
    l.tail.length + m.tail.length < l.length + m.length := by
  cases l <;> cases m <;> simp_all <;> omega

/-- Evaluations at all sufficiently large integers determine every coefficient.
The constant-term difference is divisible by arbitrarily large integers. -/
private theorem unique (l m : List Int) (T : Nat)
    (h : ∀ x : Nat, T < x → horner (x:Int) l = horner (x:Int) m) :
    trim l = trim m := by
  have front (x : Nat) (hx : T < x) : l.headD 0 - m.headD 0 =
      (x:Int)*(horner (x:Int) m.tail-horner (x:Int) l.tail) := by
    have hh := h x hx
    rw [expand_head _ l,expand_head _ m] at hh
    grind only
  let x := (l.headD 0 - m.headD 0).natAbs + T + 1
  have big := front x (by dsimp [x]; omega)
  have dvd : (x:Int) ∣ l.headD 0 - m.headD 0 := ⟨_,big⟩
  have zero := Int.eq_zero_of_dvd_of_natAbs_lt_natAbs dvd (by simp [x]; omega)
  have he : l.headD 0 = m.headD 0 := by omega
  have ht (y : Nat) (hy : T < y) : horner (y:Int) l.tail = horner (y:Int) m.tail := by
    have hh := front y hy
    have yz : (y:Int) ≠ 0 := by omega
    rw [zero] at hh
    have := (Int.mul_eq_zero.mp hh.symm).resolve_left yz
    omega
  by_cases empty : l=[] ∧ m=[]
  · rw [empty.1,empty.2]
  · have aux := unique l.tail m.tail T ht
    have eq (s : List Int) : trim s = consC (s.headD 0) (trim s.tail) := by cases s <;> rfl
    rw [eq l,eq m,he,aux]
termination_by l.length + m.length
decreasing_by exact tails_shorter _ _ empty

theorem coeffs_ext (p q : Poly) (T : Nat)
    (h : ∀ x : Nat, T < x → p.eval (x:Int) = q.eval (x:Int)) : p.coeffs = q.coeffs := by
  apply unique _ _ T
  intro x hx
  simpa only [← eval_coeffs,Poly.coeffs,trim_eval] using h x hx

theorem formal_iff_coeffs (p q : Poly) : p.formal = q.formal ↔ p.coeffs = q.coeffs := by
  constructor
  · intro h
    have e := Quotient.exact (s:=polynomialSetoid) h
    exact coeffs_ext p q 0 (fun x _ => e Int x)
  · intro h
    apply Quotient.sound (s:=polynomialSetoid)
    intro K inst x
    rw [← eval_coeffs x p,← eval_coeffs x q,h]

/-- Degree convention for the zero polynomial is zero. -/
def Poly.degree (p : Poly) := p.coeffs.length-1

private def homogeneous (a b : Int) : List Int → Int
  | [] => 0
  | [c] => c
  | c::d::t => c*b^(t.length+1)+a*homogeneous a b (d::t)

def Poly.cleared (p : Poly) (a b : Int) := homogeneous a b p.coeffs

private theorem homogeneous_eval (a b : Int) (hb : 0 < b) (l : List Int) :
    ((homogeneous a b l:Int):Rat) = (b:Rat)^(l.length-1)*horner ((a:Rat)/(b:Rat)) l := by
  match l with
  | [] => simp [homogeneous,horner]
  | [c] => simp [homogeneous,horner]; grind
  | c::d::t =>
    have ih := homogeneous_eval a b hb (d::t)
    have nz : (b:Rat) ≠ 0 := Rat.ne_of_gt (Rat.intCast_pos.mpr hb)
    have cancel := Rat.div_mul_cancel (a:=(a:Rat)) nz
    simp only [List.length_cons,Nat.add_sub_cancel] at *
    simp only [homogeneous,Rat.intCast_add,Rat.intCast_mul,Rat.intCast_pow,ih,
      Rat.pow_succ,horner]
    grind only

theorem cleared_eval (p : Poly) (a b : Int) (hb : 0 < b) :
    ((p.cleared a b:Int):Rat) = (b:Rat)^p.degree*p.eval ((a:Rat)/(b:Rat)) := by
  rw [Poly.cleared,homogeneous_eval a b hb,eval_coeffs,Poly.degree]

/-- Derivative of a polynomial written in Horner form. -/
def dHorner (x : K) : List Int → K
  | [] => 0
  | _::t => horner x t + x*dHorner x t

private theorem dadd (x : K) (l m : List Int) :
    dHorner x (addC l m) = dHorner x l + dHorner x m := by
  induction l generalizing m with
  | nil => simp [addC,dHorner]; grind
  | cons a l ih => cases m <;> simp only [addC,dHorner,add_eval,ih] <;> grind

private theorem dmul (x : K) (l m : List Int) :
    dHorner x (mulC l m) = dHorner x l*horner x m + horner x l*dHorner x m := by
  have scale (a : Int) (u : List Int) : horner x (u.map (a*·)) = (a:K)*horner x u := by
    induction u <;> simp_all [horner,Ring.intCast_mul] <;> grind
  have ds (a : Int) : dHorner x (m.map (a*·)) = (a:K)*dHorner x m := by
    induction m <;> simp_all [dHorner] <;> grind
  induction l <;> simp_all only [mulC,dHorner,horner,dadd,mul_eval] <;> grind

private theorem dtrim (x : K) (l : List Int) : dHorner x (trim l) = dHorner x l := by
  induction l with
  | nil => rfl
  | cons a t ih =>
    change dHorner x (consC a (trim t)) = _
    unfold consC
    split
    · rename_i h
      simp at h
      have val := trim_eval x t
      rw [h.1] at ih val
      simp only [dHorner,horner] at *
      grind
    · simp only [dHorner,trim_eval,ih]

theorem deriv_coeffs (x : K) (p : Poly) : dHorner x p.coeffs = p.deriv.eval x := by
  simp only [Poly.coeffs,dtrim]
  have raw (z : Poly) : horner x (rawCoeffs z) = z.eval x := by
    simpa only [Poly.coeffs,trim_eval] using eval_coeffs x z
  induction p <;> simp_all only [rawCoeffs,dHorner,horner,Poly.deriv,Poly.eval,dadd,dmul] <;> grind

end Dichrom

namespace Dichrom
/-- A subtraction-free expression in X with nonnegative integer constants. -/
inductive PositiveForm : Poly → Prop
  | const (a : Nat) : PositiveForm (.C a)
  | var : PositiveForm .X
  | add : PositiveForm p → PositiveForm q → PositiveForm (.add p q)
  | mul : PositiveForm p → PositiveForm q → PositiveForm (.mul p q)

private def nn (l : List Int) := ∀ z ∈ l, 0 ≤ z

private theorem nn_cons {a : Int} {l : List Int} : nn (a::l) ↔ 0 ≤ a ∧ nn l := by
  simp [nn]

private theorem nn_add (l m : List Int) (h : nn l) (g : nn m) : nn (addC l m) := by
  induction l generalizing m with
  | nil => exact g
  | cons a t ih =>
    cases m with
    | nil => exact h
    | cons b u =>
      obtain ⟨ha,ht⟩ := nn_cons.mp h
      obtain ⟨hb,hu⟩ := nn_cons.mp g
      exact nn_cons.mpr ⟨Int.add_nonneg ha hb,ih u ht hu⟩

private theorem nn_mul (l m : List Int) (h : nn l) (g : nn m) : nn (mulC l m) := by
  induction l with
  | nil => simp [mulC,nn]
  | cons a t ih =>
    obtain ⟨ha,ht⟩ := nn_cons.mp h
    apply nn_add
    · intro z hz
      obtain ⟨b,hb,rfl⟩ := List.mem_map.mp hz
      exact Int.mul_nonneg ha (g b hb)
    · exact nn_cons.mpr ⟨by decide,ih ht⟩

theorem PositiveForm.coefficients {p : Poly} (h : PositiveForm p) : ∀ c ∈ p.coeffs, 0 ≤ c := by
  have trim_nn (l : List Int) (hl : nn l) : nn (trim l) := by
    induction l with
    | nil => exact hl
    | cons a t ih =>
      obtain ⟨ha,ht⟩ := nn_cons.mp hl
      simp only [trim,consC]
      split
      · simp [nn]
      · exact nn_cons.mpr ⟨ha,ih ht⟩
  apply trim_nn
  induction h with
  | const a => simp [rawCoeffs,nn]
  | var => simp [rawCoeffs,nn]
  | add _ _ hp hq => exact nn_add _ _ hp hq
  | mul _ _ hp hq => exact nn_mul _ _ hp hq

end Dichrom

import Dichrom.Universal

/-! Why the shift works for H itself: remove X(X-1) from the correction in
identity (3). A partition with at least two blocks supplies both factors in its
falling factorial. For a one-block partition the forbidden-block weight is
(n-1)(X-1). The recursion uses the corresponding factor X-1 of the smaller H. -/
namespace Dichrom

private def affine (m : Nat) := Poly.add (.C m) .X
private theorem affine_good (m : Nat) : PositiveForm (affine m) := .add (.const _) .var
private theorem affine_eval (m u : Nat) : (affine m).eval (u:Int) = (m:Int)+(u:Int) := rfl

private def shiftedFall (m : Nat) : Nat → Poly
  | 0 => .C 1
  | k+1 => .mul (affine m) (shiftedFall (m-1) k)

private theorem shiftedFall_good (m k : Nat) : PositiveForm (shiftedFall m k) := by
  induction k generalizing m with
  | zero => exact .const 1
  | succ k ih => exact .mul (affine_good _) (ih _)

private theorem shiftedFall_eval (m k u : Nat) (hk : k ≤ m) :
    (shiftedFall m k).eval (u:Int) = fall ((m:Int)+(u:Int)) k := by
  induction k generalizing m with
  | zero => rfl
  | succ k ih =>
    simp only [shiftedFall,Poly.eval,affine_eval,fall]
    rw [ih (m-1) (by omega),show ((m-1:Nat):Int)+(u:Int)=(m:Int)+u-1 by omega]

private theorem positive_sum {δ : Type} (l : List δ) (f : δ → Poly)
    (h : ∀ a ∈ l, PositiveForm (f a)) : PositiveForm (sumPoly l f) := by
  induction l with
  | nil => exact .const 0
  | cons a t ih => exact .add (h a (by simp)) (ih (by grind))

/-- Represent f by a nonnegative-coefficient polynomial after extracting c. -/
private def factors (c f : Nat → Int) := ∃ p, PositiveForm p ∧
  ∀ u : Nat, 0 < u → c u*p.eval (u:Int) = f u

private theorem sum_factors {δ : Type} (l : List δ) (c : Nat → Int) (f : δ → Nat → Int)
    (h : ∀ a ∈ l, factors c (f a)) : factors c (fun u => total l (fun a => f a u)) := by
  induction l with
  | nil =>
    exact ⟨.C 0,.const 0,fun _ _ => by simp [Poly.eval,total]⟩
  | cons a t ih =>
    obtain ⟨p,hp,ep⟩ := h a (by simp)
    obtain ⟨q,hq,eq⟩ := ih (by grind)
    refine ⟨.add p q,.add hp hq,?_⟩
    intro u hu
    have := ep u hu; have := eq u hu
    simp only [Poly.eval,total]; grind only

private def blockWeight (A : System α) (v : α) (N m : Nat) (b : List α) : Poly :=
  if A.ok (v::b) then .C 0 else .add (.C (Int.ofNat (m*b.length-N))) (.mul .X (.C b.length))

private theorem weight_good (A : System α) (v : α) (N m : Nat) (b : List α) :
    PositiveForm (blockWeight A v N m b) := by
  unfold blockWeight; split
  · exact .const 0
  · exact .add (.const _) (.mul .var (.const _))

private theorem weight_eval (A : System α) (v : α) (N m u : Nat) (b : List α)
    (hn : N ≤ m) (hb : 0 < b.length) :
    (blockWeight A v N m b).eval (u:Int) =
      keep (!(A.ok (v::b))) (((m:Int)+u)*(b.length:Int)-(N:Int)) := by
  have le : N ≤ m*b.length := Nat.le_trans hn (by
    simpa using Nat.mul_le_mul_left m (show 1 ≤ b.length from hb))
  unfold blockWeight
  cases A.ok (v::b) <;> simp [keep, Poly.eval,Int.ofNat_eq_natCast,Int.natCast_sub le] <;> grind

private theorem bonus_factor (A : System α) (v : α) (t : List α) (m : Nat) (hm : t.length ≤ m)
    (p : Blocks α) (hp : p ∈ parts A.ok t) :
    factors (fun u => ((m:Int)+u)*((m:Int)+u-1)) (fun u =>
      fall ((m:Int)+u) p.length * total p (fun b =>
        keep (!(A.ok (v::b))) (((m:Int)+u)*(b.length:Int)-(t.length:Int)))) := by
  obtain ⟨massEq,kbound,nonempty⟩ := part_info _ _ _ hp
  match p with
  | [] => exact ⟨.C 0,.const 0,fun _ _ => by simp [Poly.eval,total,fall]⟩
  | [b] =>
    have size : b.length = t.length := by simpa [mass] using massEq
    cases hb : A.ok (v::b) with
    | true => exact ⟨.C 0,.const 0,fun _ _ => by simp [total,keep,hb,Poly.eval]⟩
    | false =>
      exact ⟨.C t.length,.const _,fun _ _ => by simp [total,keep,hb,Poly.eval,size,fall]; grind⟩
  | b::d::z =>
    let p := b::d::z
    let w := blockWeight A v t.length m
    refine ⟨.mul (shiftedFall (m-2) z.length) (sumPoly p w),
      .mul (shiftedFall_good ..) (positive_sum _ _ (fun e _ => weight_good ..)),?_⟩
    intro u _
    have room : z.length+2 ≤ m := Nat.le_trans kbound hm
    have sumEq : total p (fun b => (w b).eval (u:Int)) = total p (fun b =>
        keep (!(A.ok (v::b))) (((m:Int)+u)*(b.length:Int)-(t.length:Int))) :=
      total_congr (fun b h => weight_eval _ _ _ _ _ b hm (nonempty b h))
    simp only [Poly.eval,eval_sumPoly,sumEq,shiftedFall_eval _ _ _ (show z.length ≤ m-2 by omega),
      List.length_cons,fall]
    rw [show ((m-2:Nat):Int)+u=(m:Int)+u-1-1 by omega]
    dsimp only [p]
    grind only

private theorem shifted_factor (A : System α) (l : List α) (m : Nat) (hm : l.length ≤ m+1) :
    factors (fun u => (m:Int)+u) (fun u => H A.ok l ((m:Int)+u)) := by
  match l with
  | [] =>
    refine ⟨.C 0,.const 0,?_⟩
    intro u _; simp [H,dP,P,part_nil,fall,dfall,Poly.eval]
  | [v] =>
    refine ⟨.C 0,.const 0,?_⟩
    intro u _; simp [H,dP,P,part_cons,split_nil,part_nil,fall,dfall,A.single,Poly.eval]
  | v::w::t =>
    let tail := w::t
    have bound : tail.length ≤ m := by simp [tail] at *; omega
    have mpos : 1 ≤ m := by change t.length+1 ≤ m at bound; omega
    let y (u : Nat) := (m:Int)+u-1
    have small (a : List α × List α) (ha : a ∈ splits tail) :
        factors y (fun u => keep (A.ok (v::a.1)) (H A.ok a.2 (y u))) := by
      obtain ⟨s,r⟩ := a
      have sz := split_size ha
      dsimp only
      cases hs : A.ok (v::s) with
      | false => exact ⟨.C 0,.const 0,fun _ _ => by simp [Poly.eval,keep]⟩
      | true =>
        obtain ⟨p,hp,ep⟩ := shifted_factor A r (m-1) (by omega)
        refine ⟨p,hp,?_⟩; intro u hu
        have e : y u = ((m-1:Nat):Int)+u := by dsimp [y]; omega
        simpa only [e,keep,ite_true] using ep u hu
    obtain ⟨p,hp,ep⟩ := sum_factors _ y _ small
    obtain ⟨q,hq,eq⟩ := sum_factors _ _ _ (bonus_factor A v tail m bound)
    refine ⟨.add (.mul (affine m) p) q,.add (.mul (affine_good _) hp) hq,?_⟩
    intro u hu
    let x := (m:Int)+u
    have nonzero : x-1 ≠ 0 := by dsimp [x]; omega
    have smaller := ep u hu
    change (x-1)*p.eval (u:Int) = splitSum tail (fun s r => keep (A.ok (v::s)) (H A.ok r (x-1))) at smaller
    have bonus := eq u hu
    change (x*(x-1))*q.eval (u:Int) = correction A v tail x at bonus
    have main := identity3 A v tail x
    rw [← smaller, ← bonus] at main
    change x*(x*p.eval (u:Int)+q.eval (u:Int)) = H A.ok (v::tail) x
    apply Int.eq_of_mul_eq_mul_left nonzero
    grind only
termination_by l.length
decreasing_by dsimp [tail] at *; simp_all; omega

theorem shifted_coefficients (A : System α) (l : List α) (m : Nat) (hm : l.length ≤ m+1) :
    ∀ c ∈ ((defect A.ok l).subst (.add (.C m) .X)).coeffs, 0 ≤ c := by
  change ∀ c ∈ ((defect A.ok l).subst (affine m)).coeffs, 0 ≤ c
  obtain ⟨p,hp,ep⟩ := shifted_factor A l m hm
  have same := coeffs_ext ((defect A.ok l).subst (affine m)) (.mul (affine m) p) 0
    (fun u hu => by simpa only [eval_subst,Poly.eval,affine_eval,eval_H] using (ep u hu).symm)
  rw [same]
  exact (PositiveForm.mul (affine_good m) hp).coefficients

end Dichrom

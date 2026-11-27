import Dichrom.Marked

namespace Dichrom
variable {α : Type}

theorem sum_nonneg {l : List α} {f : α → Rat} (h : ∀ a ∈ l, 0 ≤ f a) : 0 ≤ total l f := by
  induction l with
  | nil => exact Rat.le_refl
  | cons a t ih => exact Rat.add_nonneg (h a (by simp)) (ih (by grind))

theorem term_le_sum {l : List α} {f : α → Rat} (h : ∀ a ∈ l, 0 ≤ f a) {a : α}
    (ha : a ∈ l) : f a ≤ total l f := by
  induction l with
  | nil => simp at ha
  | cons b t ih =>
    have hb := h b (by simp)
    have ht : ∀ c ∈ t, 0 ≤ f c := by grind
    have := sum_nonneg ht
    rcases List.mem_cons.mp ha with rfl | hr
    · simp only [total]; grind
    · have := ih ht hr; simp only [total]; grind

theorem fall_pos (k : Nat) (x : Rat) (hx : (k:Rat)-1 < x) : 0 < fall x k := by
  induction k generalizing x with
  | zero => exact (by decide : (0:Rat) < 1)
  | succ k ih =>
    simp only [fall]
    have hn := Rat.natCast_nonneg (a:=k)
    simp only [Rat.natCast_add] at hx
    exact Rat.mul_pos (by grind) (ih _ (by grind))

private theorem block_nonneg (A : System α) (v : α) (t : List α) (x : Rat)
    (hx : (t.length:Rat) ≤ x) (p : Blocks α) (hp : p ∈ parts A.ok t) :
    ∀ b ∈ p, 0 ≤ keep (!(A.ok (v::b))) (x*(b.length:Rat)-(t.length:Rat)) := by
  intro b hb
  have h := (part_info _ _ _ hp).2.2 b hb
  have h1 : (1:Rat) ≤ (b.length:Rat) := Rat.natCast_le_natCast.mpr h
  have hn := Rat.natCast_nonneg (a:=t.length)
  have := Rat.mul_le_mul_of_nonneg_left h1 (Rat.le_trans hn hx)
  cases A.ok (v::b) <;> simp [keep] <;> grind

private theorem correction_terms (A : System α) (v : α) (t : List α) (x : Rat)
    (hx : (t.length:Rat) ≤ x) (p : Blocks α) (hp : p ∈ parts A.ok t) :
    0 ≤ fall x p.length * total p (fun b => keep (!(A.ok (v::b)))
      (x*(b.length:Rat)-(t.length:Rat))) := by
  have hlen := Rat.natCast_le_natCast.mpr (part_info _ _ _ hp).2.1
  exact Rat.mul_nonneg (Rat.le_of_lt (fall_pos _ _ (by grind)))
    (sum_nonneg (block_nonneg A v t x hx p hp))

private theorem H_pair (A : System α) (v w : α) (x : Rat) :
    H A.ok [v,w] x = if A.ok [v,w] then 0 else x := by
  have hp := A.single v
  have hq := A.single w
  cases h : A.ok [v,w] <;> simp [H,dP,P,part_cons,part_nil,split_cons,split_nil,fall,dfall,h,hp,hq] <;> grind

theorem nonnegative (A : System α) (l : List α) (x : Rat)
    (hx : (l.length:Rat)-1 ≤ x) : 0 ≤ H A.ok l x := by
  match l with
  | [] => simp [H,dP,P,part_nil,dfall]; grind
  | [v] => simp [H,dP,P,part_cons,part_nil,split_nil,dfall,fall,A.single]; grind
  | [v,w] => change (2:Rat)-1 ≤ x at hx; rw [H_pair]; split <;> grind
  | v::w::z::t =>
    let tail := w::z::t
    have ht : (tail.length:Rat) ≤ x := by
      simp only [tail,List.length_cons,Rat.natCast_add] at *; grind
    have hx1 : 0 < x-1 := by
      have := Rat.natCast_nonneg (a:=t.length)
      simp only [tail,List.length_cons,Rat.natCast_add] at ht; grind
    have recurse (u : List α × List α) (hm : u ∈ splits tail) :
        0 ≤ keep (A.ok (v::u.1)) (H A.ok u.2 (x-1)) := by
      obtain ⟨s,r⟩ := u
      have sz := split_size hm
      have le : (r.length:Rat) ≤ (tail.length:Rat) := Rat.natCast_le_natCast.mpr (by omega)
      have ih := nonnegative A r (x-1) (by grind)
      cases A.ok (v::s) <;> simp_all [keep]
    have first := Rat.mul_nonneg (Rat.pow_nonneg (Rat.le_trans (Rat.natCast_nonneg) ht) (n:=2))
      (sum_nonneg recurse)
    have last := sum_nonneg (correction_terms A v tail x ht)
    have eqn := identity3 A v tail x
    change 0 ≤ x^2 * splitSum tail (fun s r => keep (A.ok (v::s)) (H A.ok r (x-1))) at first
    change 0 ≤ correction A v tail x at last
    have bound := Rat.add_nonneg first last
    rw [← eqn] at bound
    exact Rat.le_of_mul_le_mul_left (by simpa using bound) hx1
termination_by l.length
decreasing_by dsimp [tail] at *; simp_all; omega

theorem positive (A : System α) (l : List α) (x : Rat) (hbad : A.ok l = false)
    (hx : (l.length:Rat)-1 < x) : 0 < H A.ok l x := by
  match l with
  | [] => simp [A.empty] at hbad
  | [v] => simp [A.single] at hbad
  | v::w::t =>
    let tail := w::t
    have ht : (tail.length:Rat) < x := by
      simp only [tail,List.length_cons,Rat.natCast_add] at *; grind
    have hn := Rat.natCast_nonneg (a:=tail.length)
    have xpos : 0 < x := by grind
    have xone : 0 < x-1 := by
      have := Rat.natCast_nonneg (a:=t.length)
      simp only [tail,List.length_cons,Rat.natCast_add] at ht; grind
    let term (u : List α × List α) := keep (A.ok (v::u.1)) (H A.ok u.2 (x-1))
    have terms (u) (hu : u ∈ splits tail) : 0 ≤ term u := by
      obtain ⟨s,r⟩ := u
      have sz := split_size hu
      have le : (r.length:Rat) ≤ (tail.length:Rat) := Rat.natCast_le_natCast.mpr (by omega)
      have h := nonnegative A r (x-1) (by grind)
      simp only [term]; cases A.ok (v::s) <;> simp_all [keep]
    have rec0 := sum_nonneg terms
    let bonus (p : Blocks α) := fall x p.length * total p (fun b =>
      keep (!(A.ok (v::b))) (x*(b.length:Rat)-(tail.length:Rat)))
    have bonuses (p) (hp : p ∈ parts A.ok tail) : 0 ≤ bonus p :=
      correction_terms A v tail x (Rat.le_of_lt ht) p hp
    have corr0 := sum_nonneg bonuses
    have rhs : 0 < x^2 * total (splits tail) term + total (parts A.ok tail) bonus := by
      cases htail : A.ok tail with
      | false =>
        have ih := positive A tail (x-1) htail (by grind)
        have hb := term_le_sum terms (splits_right tail)
        change keep (A.ok [v]) (H A.ok tail (x-1)) ≤ _ at hb
        simp only [A.single, keep, ite_true] at hb
        have := Rat.mul_pos (Rat.pow_pos xpos (n:=2)) (show 0 < total (splits tail) term by grind)
        grind
      | true =>
        have hm : [tail] ∈ parts A.ok tail := part_one htail
        have hb := term_le_sum bonuses hm
        have size : (1:Rat) ≤ (tail.length:Rat) := Rat.natCast_le_natCast.mpr (by simp [tail])
        have := Rat.mul_le_mul_of_nonneg_left size (Rat.le_of_lt xpos)
        have val : 0 < x*(tail.length:Rat)-(tail.length:Rat) := by grind
        have hpos := Rat.mul_pos xpos val
        have hfull : A.ok (v::tail) = false := hbad
        have bpos : 0 < bonus [tail] := by simpa [bonus, total, keep, hfull, fall, Rat.add_zero] using hpos
        have bsum : 0 < total (parts A.ok tail) bonus := by grind only
        have := Rat.mul_nonneg (Rat.le_of_lt (Rat.pow_pos xpos (n:=2))) rec0
        grind
    change 0 < x^2 * splitSum tail (fun s r => keep (A.ok (v::s)) (H A.ok r (x-1))) + correction A v tail x at rhs
    rw [← identity3] at rhs
    exact (Rat.mul_pos_iff_of_pos_left xone).mp rhs
termination_by l.length
decreasing_by simp

end Dichrom

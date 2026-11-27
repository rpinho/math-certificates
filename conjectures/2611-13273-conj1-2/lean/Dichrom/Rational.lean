import Dichrom.Polynomial

/-! An algebraic substitute for the mean value theorem on a rational interval.
Use the two-point polynomial remainder, then add the error bounds over equally
spaced rational subintervals. All bounds and divisions take place in Rat. -/
namespace Dichrom

private inductive Bi where
  | C (z : Int) | L | R | add (p q : Bi) | mul (p q : Bi)

private def Bi.val (a b : Rat) : Bi → Rat
  | .C z => z
  | .L => a
  | .R => b
  | .add p q => p.val a b + q.val a b
  | .mul p q => p.val a b * q.val a b

private def liftAt (v : Bi) : Poly → Bi
  | .C z => .C z
  | .X => v
  | .add p q => .add (liftAt v p) (liftAt v q)
  | .mul p q => .mul (liftAt v p) (liftAt v q)

private theorem lift_val (v : Bi) (p : Poly) (a b : Rat) :
    (liftAt v p).val a b = p.eval (v.val a b) := by
  induction p <;> simp_all [liftAt,Bi.val,Poly.eval]

/-- Divided difference, with no division even on the diagonal. -/
private def sec : Poly → Bi
  | .C _ => .C 0
  | .X => .C 1
  | .add p q => .add (sec p) (sec q)
  | .mul p q => .add (.mul (sec p) (liftAt .R q)) (.mul (liftAt .L p) (sec q))

private theorem sec_eq (p : Poly) (a b : Rat) :
    p.eval b - p.eval a = (b-a)*(sec p).val a b := by
  induction p <;> simp_all only [sec,Poly.eval,Bi.val,lift_val] <;> grind

private def remainder : Poly → Bi
  | .C _ | .X => .C 0
  | .add p q => .add (remainder p) (remainder q)
  | .mul p q => .add (.mul (remainder p) (liftAt .R q))
      (.add (.mul (liftAt .L p.deriv) (sec q)) (.mul (liftAt .L p) (remainder q)))

private theorem remainder_eq (p : Poly) (a b : Rat) :
    (sec p).val a b - p.deriv.eval a = (b-a)*(remainder p).val a b := by
  induction p with
  | C z => simp [sec,Poly.deriv,Poly.eval,remainder,Bi.val]; grind
  | X => simp [sec,Poly.deriv,Poly.eval,remainder,Bi.val]; grind
  | add p q ih jh => simp only [sec,Poly.deriv,Poly.eval,remainder,Bi.val]; grind
  | mul p q ih jh =>
    have h := sec_eq q a b
    simp only [sec,Poly.deriv,Poly.eval,remainder,Bi.val,lift_val]
    grind

private theorem mul_bounds {a b m n : Rat} (ha : -m ≤ a ∧ a ≤ m) (hb : -n ≤ b ∧ b ≤ n) :
    -(m*n) ≤ a*b ∧ a*b ≤ m*n := by
  obtain ⟨al,au⟩ := ha; obtain ⟨bl,bu⟩ := hb
  have hm : 0 ≤ m := by grind
  have hn : 0 ≤ n := by grind
  by_cases h : 0 ≤ a
  · have h1 := Rat.mul_le_mul_of_nonneg_left bl h
    have h2 := Rat.mul_le_mul_of_nonneg_left bu h
    have h3 := Rat.mul_le_mul_of_nonneg_right au hn
    grind
  · have h1 := Rat.mul_le_mul_of_nonneg_left bl (show 0 ≤ -a by grind)
    have h2 := Rat.mul_le_mul_of_nonneg_left bu (show 0 ≤ -a by grind)
    have h3 := Rat.mul_le_mul_of_nonneg_right al hn
    grind

private def Bi.bound (M : Rat) : Bi → Rat
  | .L | .R => M
  | .C z => (z:Rat).abs
  | .add p q => p.bound M + q.bound M
  | .mul p q => p.bound M * q.bound M

private theorem bounds (p : Bi) (a b M : Rat) (ha : 0 ≤ a ∧ a ≤ M) (hb : 0 ≤ b ∧ b ≤ M) :
    -(p.bound M) ≤ p.val a b ∧ p.val a b ≤ p.bound M := by
  induction p with
  | L | R => simp only [Bi.val,Bi.bound]; grind
  | C z =>
    simp only [Bi.val,Bi.bound]
    by_cases h : 0 ≤ (z:Rat)
    · rw [Rat.abs_of_nonneg h]; grind
    · rw [Rat.abs_of_nonpos (by grind)]; grind
  | add p q ih jh => simp only [Bi.val,Bi.bound]; grind
  | mul p q ih jh => exact mul_bounds ih jh

/-- Cross-multiplied quadratic remainder for a polynomial quotient. -/
private def crossError (p q : Poly) := Bi.add
    (.mul (remainder p) (liftAt .L q))
    (.mul (.C (-1)) (.mul (liftAt .L p) (remainder q)))

private theorem cross_eq (p q : Poly) (a b : Rat) :
    p.eval b * q.eval a - p.eval a * q.eval b =
    (b-a)*(p.deriv.eval a*q.eval a-p.eval a*q.deriv.eval a) +
    (b-a)^2*(crossError p q).val a b := by
  have := sec_eq p a b
  have := sec_eq q a b
  have := remainder_eq p a b
  have := remainder_eq q a b
  simp only [crossError,Bi.val,lift_val]
  grind

private theorem exists_nat_gt (x : Rat) : ∃ n : Nat, x < (n:Rat) := by
  refine ⟨x.floor.toNat+1, ?_⟩
  have := Rat.lt_floor_add_one (a := x)
  have h : (x.floor : Rat) ≤ (x.floor.toNat:Rat) :=
    Rat.intCast_le_intCast.mpr (Int.self_le_toNat _)
  simp only [Rat.natCast_add]
  grind

/-- A uniform quadratic bound on loss forces weak increase. -/
private theorem mesh (f : Rat → Rat) (r s C : Rat) (hrs : r ≤ s)
    (h : ∀ a b, r ≤ a → a ≤ b → b ≤ s → f a - f b ≤ C*(b-a)^2) : f r ≤ f s := by
  apply Classical.byContradiction
  intro fail
  have gap : 0 < f r-f s := by grind
  obtain ⟨m,hm⟩ := exists_nat_gt (C*(s-r)^2/(f r-f s))
  let N := m+1
  have Npos : 0 < (N:Rat) := Rat.natCast_pos.mpr (by simp [N])
  have big : C*(s-r)^2 < (N:Rat)*(f r-f s) := by
    have := (Rat.div_lt_iff gap).mp hm
    have hm' : (m:Rat) ≤ (N:Rat) := Rat.natCast_le_natCast.mpr (by simp [N])
    have := Rat.mul_le_mul_of_nonneg_right hm' (Rat.le_of_lt gap)
    grind
  let d := (s-r)/(N:Rat)
  have hd : d*(N:Rat) = s-r := Rat.div_mul_cancel (Rat.ne_of_gt Npos)
  have d0 : 0 ≤ d := by
    apply Rat.le_of_mul_le_mul_right (c:=(N:Rat)) _ Npos
    grind
  have telescope (k : Nat) (hk : k ≤ N) :
      f r - f (r+(k:Rat)*d) ≤ (k:Rat)*(C*d^2) := by
    induction k with
    | zero => simp; grind
    | succ k ih =>
      have hk' : k ≤ N := by omega
      have prev := ih hk'
      have m0 := Rat.mul_nonneg (Rat.natCast_nonneg (a:=k)) d0
      have hi := Rat.mul_le_mul_of_nonneg_right (Rat.natCast_le_natCast.mpr hk) d0
      have next := h (r+(k:Rat)*d) (r+((k+1:Nat):Rat)*d) (by grind)
        (by simp only [Rat.natCast_add]; grind) (by grind)
      simp only [Rat.natCast_add,Rat.natCast_ofNat] at *
      have step : r+((k:Rat)+1)*d-(r+(k:Rat)*d) = d := by grind
      rw [step] at next
      grind
  have last := telescope N (Nat.le_refl _)
  rw [show r+(N:Rat)*d=s by grind] at last
  have mul := Rat.mul_le_mul_of_nonneg_left last (Rat.le_of_lt Npos)
  have iden : (N:Rat)*((N:Rat)*(C*d^2)) = C*(s-r)^2 := by rw [← hd]; grind
  grind

theorem quotient_monotone (p q : Poly) (r s : Rat) (hr : 0 ≤ r) (hrs : r ≤ s)
    (hq : ∀ a, r ≤ a → a ≤ s → 1 ≤ q.eval a)
    (hsign : ∀ a, r ≤ a → a ≤ s → 0 ≤ p.deriv.eval a*q.eval a-p.eval a*q.deriv.eval a) :
    p.eval r / q.eval r ≤ p.eval s / q.eval s := by
  let E := crossError p q
  apply mesh (fun a => p.eval a/q.eval a) r s (E.bound s) hrs
  intro a b hra hab hbs
  have has := Rat.le_trans hab hbs
  have hrb := Rat.le_trans hra hab
  have ha := hq a hra has
  have hb := hq b hrb hbs
  have d0 : 0 ≤ b-a := by grind
  have sq := Rat.pow_nonneg (n:=2) d0
  have ⟨lo,hi⟩ := bounds E a b s ⟨Rat.le_trans hr hra,has⟩ ⟨Rat.le_trans hr hrb,hbs⟩
  have C0 : 0 ≤ E.bound s := by grind
  have err := Rat.mul_le_mul_of_nonneg_left lo sq
  have sign := Rat.mul_nonneg d0 (hsign a hra has)
  have cross := cross_eq p q a b
  change _ = _ + _ * E.val a b at cross
  have denom := Rat.mul_le_mul_of_nonneg_left hb (show 0 ≤ q.eval a by grind)
  have ee := Rat.mul_nonneg C0 sq
  have scale := Rat.mul_le_mul_of_nonneg_left (show 1 ≤ q.eval a*q.eval b by grind) ee
  have qa := Rat.div_mul_cancel (a:=p.eval a) (b:=q.eval a) (by grind)
  have qb := Rat.div_mul_cancel (a:=p.eval b) (b:=q.eval b) (by grind)
  apply Rat.le_of_mul_le_mul_right (c:=q.eval a*q.eval b) _ (by grind)
  have cleared : (p.eval a/q.eval a - p.eval b/q.eval b) * (q.eval a*q.eval b) =
      p.eval a*q.eval b - p.eval b*q.eval a := by
    calc
      _ = (p.eval a/q.eval a*q.eval a)*q.eval b - (p.eval b/q.eval b*q.eval b)*q.eval a := by grind only
      _ = _ := by rw [qa,qb]
  rw [cleared]
  have lower : p.eval a*q.eval b - p.eval b*q.eval a ≤ E.bound s*(b-a)^2 := by
    have lower := Rat.add_nonneg sign (show 0 ≤ (b-a)^2*E.val a b + E.bound s*(b-a)^2 by grind only)
    grind only
  exact Rat.le_trans lower (by simpa [Rat.mul_one] using scale)

/-- A positive derivative at the left endpoint gives a strict increase
somewhere before any prescribed right endpoint. -/
theorem quotient_rises (p q : Poly) (a s : Rat) (ha : 0 ≤ a) (has : a < s)
    (hq : ∀ b, a ≤ b → b ≤ s → 0 < q.eval b)
    (hD : 0 < p.deriv.eval a*q.eval a-p.eval a*q.deriv.eval a) :
    ∃ b, a < b ∧ b ≤ s ∧ p.eval a/q.eval a < p.eval b/q.eval b := by
  let E := crossError p q
  let D := p.deriv.eval a*q.eval a-p.eval a*q.deriv.eval a
  obtain ⟨m,hm⟩ := exists_nat_gt ((s-a)*E.bound s/D)
  let N := m+1
  have one : (1:Rat) ≤ (N:Rat) := Rat.natCast_le_natCast.mpr (by simp [N])
  have np : 0 < (N:Rat) := by grind
  let h := (s-a)/(N:Rat)
  have eqn : h*(N:Rat) = s-a := Rat.div_mul_cancel (Rat.ne_of_gt np)
  have hp : 0 < h := (Rat.mul_pos_iff_of_pos_right np).mp (by rw [eqn]; grind)
  have le := Rat.mul_le_mul_of_nonneg_left one (Rat.le_of_lt hp)
  have abs : a+h ≤ s := by grind
  have d : 0 < D := hD
  have big := (Rat.div_lt_iff d).mp hm
  have lift := Rat.mul_le_mul_of_nonneg_right
    (Rat.natCast_le_natCast.mpr (show m ≤ N by simp [N])) (Rat.le_of_lt d)
  have small : h*E.bound s < D := by
    apply (Rat.mul_lt_mul_right np).mp
    rw [show h*E.bound s*(N:Rat) = (s-a)*E.bound s by rw [← eqn]; grind only]
    grind only
  have ⟨lo,_⟩ := bounds E a (a+h) s ⟨ha,Rat.le_of_lt has⟩ ⟨by grind,abs⟩
  have err := Rat.mul_le_mul_of_nonneg_left lo (Rat.le_of_lt hp)
  have pos := Rat.mul_pos hp (show 0 < D+h*E.val a (a+h) by grind only)
  have cross := cross_eq p q a (a+h)
  change _ = _*D + _ * E.val a (a+h) at cross
  rw [show a+h-a=h by grind] at cross
  have qa := hq a Rat.le_refl (Rat.le_of_lt has)
  have qb := hq (a+h) (by grind) abs
  refine ⟨a+h,by grind,abs,?_⟩
  apply (Rat.div_lt_iff qa).mpr
  apply (Rat.mul_lt_mul_right qb).mp
  have cancel := Rat.div_mul_cancel (a:=p.eval (a+h)) (Rat.ne_of_gt qb)
  rw [show p.eval (a+h)/q.eval (a+h)*q.eval a*q.eval (a+h) =
      (p.eval (a+h)/q.eval (a+h)*q.eval (a+h))*q.eval a by grind only, cancel]
  grind only

end Dichrom

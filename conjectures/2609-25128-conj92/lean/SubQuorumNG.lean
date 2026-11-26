/-
  Standalone Lean 4.36.0 formalization (no Mathlib) of the unconditional proof of
  Conjecture 9.2 of Haobo Ma, Rafik Sahbi, and Wenlin Zhang (arXiv:2609.25128v4):
    psi_sq(G) + psi_sq(G.compl) <= n + 2
  for every finite simple undirected graph G of order n >= 2 (and all n >= 0).
-/

/-! ## Section 1: Exact Nonnegative Rationals (`NNRat`) -/

/-- Unreduced nonnegative rational `num / den` with `0 < den`. -/
structure RawRat where
  num : Nat
  den : Nat
  den_pos : 0 < den

namespace RawRat

def Equiv (a b : RawRat) : Prop :=
  a.num * b.den = b.num * a.den

theorem equiv_refl (a : RawRat) : Equiv a a := rfl

theorem equiv_symm {a b : RawRat} (h : Equiv a b) : Equiv b a := h.symm

theorem equiv_trans {a b c : RawRat} (hab : Equiv a b) (hbc : Equiv b c) : Equiv a c := by
  unfold Equiv at *
  refine Nat.eq_of_mul_eq_mul_right b.den_pos ?_
  calc
    a.num * c.den * b.den = a.num * b.den * c.den := Nat.mul_right_comm a.num c.den b.den
    _ = b.num * a.den * c.den := by rw [hab]
    _ = b.num * c.den * a.den := Nat.mul_right_comm b.num a.den c.den
    _ = c.num * b.den * a.den := by rw [hbc]
    _ = c.num * a.den * b.den := Nat.mul_right_comm c.num b.den a.den

instance instSetoid : Setoid RawRat where
  r := Equiv
  iseqv := ⟨equiv_refl, equiv_symm, equiv_trans⟩

def add (a b : RawRat) : RawRat where
  num := a.num * b.den + b.num * a.den
  den := a.den * b.den
  den_pos := Nat.mul_pos a.den_pos b.den_pos

theorem add_congr {a1 a2 b1 b2 : RawRat} (ha : Equiv a1 a2) (hb : Equiv b1 b2) :
    Equiv (add a1 b1) (add a2 b2) := by
  unfold Equiv add at *
  simp only [Nat.add_mul]
  have h1 : a1.num * b1.den * (a2.den * b2.den) = a2.num * b2.den * (a1.den * b1.den) := by
    calc
      a1.num * b1.den * (a2.den * b2.den)
          = (a1.num * a2.den) * (b1.den * b2.den) := by ac_rfl
      _ = (a2.num * a1.den) * (b1.den * b2.den) := by rw [ha]
      _ = a2.num * b2.den * (a1.den * b1.den) := by ac_rfl
  have h2 : b1.num * a1.den * (a2.den * b2.den) = b2.num * a2.den * (a1.den * b1.den) := by
    calc
      b1.num * a1.den * (a2.den * b2.den)
          = (b1.num * b2.den) * (a1.den * a2.den) := by ac_rfl
      _ = (b2.num * b1.den) * (a1.den * a2.den) := by rw [hb]
      _ = b2.num * a2.den * (a1.den * b1.den) := by ac_rfl
  rw [h1, h2]

def le (a b : RawRat) : Prop :=
  a.num * b.den ≤ b.num * a.den

theorem le_imp {a1 a2 b1 b2 : RawRat} (ha : Equiv a1 a2) (hb : Equiv b1 b2)
    (h : le a1 b1) : le a2 b2 := by
  unfold Equiv le at *
  have hpos : 0 < a1.den * b1.den := Nat.mul_pos a1.den_pos b1.den_pos
  refine Nat.le_of_mul_le_mul_right ?_ hpos
  have lhs_eq : a2.num * b2.den * (a1.den * b1.den) = a1.num * b1.den * (a2.den * b2.den) := by
    calc
      a2.num * b2.den * (a1.den * b1.den)
          = (a2.num * a1.den) * (b1.den * b2.den) := by ac_rfl
      _ = (a1.num * a2.den) * (b1.den * b2.den) := by rw [← ha]
      _ = a1.num * b1.den * (a2.den * b2.den) := by ac_rfl
  have rhs_eq : b2.num * a2.den * (a1.den * b1.den) = b1.num * a1.den * (a2.den * b2.den) := by
    calc
      b2.num * a2.den * (a1.den * b1.den)
          = (b2.num * b1.den) * (a1.den * a2.den) := by ac_rfl
      _ = (b1.num * b2.den) * (a1.den * a2.den) := by rw [← hb]
      _ = b1.num * a1.den * (a2.den * b2.den) := by ac_rfl
  rw [lhs_eq, rhs_eq]
  exact Nat.mul_le_mul_right (a2.den * b2.den) h

theorem le_congr {a1 a2 b1 b2 : RawRat} (ha : Equiv a1 a2) (hb : Equiv b1 b2) :
    le a1 b1 = le a2 b2 :=
  propext ⟨le_imp ha hb, le_imp ha.symm hb.symm⟩

def nsmul (m : Nat) (a : RawRat) : RawRat where
  num := m * a.num
  den := a.den
  den_pos := a.den_pos

theorem nsmul_congr (m : Nat) {a b : RawRat} (h : Equiv a b) :
    Equiv (nsmul m a) (nsmul m b) := by
  unfold Equiv nsmul at *
  calc
    m * a.num * b.den = m * (a.num * b.den) := by ac_rfl
    _ = m * (b.num * a.den) := by rw [h]
    _ = m * b.num * a.den := by ac_rfl

end RawRat

/-- Exact nonnegative rational numbers built as the quotient of `RawRat`. -/
def NNRat : Type := Quotient RawRat.instSetoid

namespace NNRat

def mk (num den : Nat) (h : 0 < den := by omega) : NNRat :=
  Quotient.mk RawRat.instSetoid ⟨num, den, h⟩

def ofNat (k : Nat) : NNRat := mk k 1 (by omega)

def zero : NNRat := ofNat 0

def inv (d : Nat) (h : 0 < d := by omega) : NNRat := mk 1 d h

def add (x y : NNRat) : NNRat :=
  Quotient.lift₂ (fun a b => Quotient.mk RawRat.instSetoid (RawRat.add a b))
    (fun _ _ _ _ ha hb => Quotient.sound (RawRat.add_congr ha hb)) x y

instance : Add NNRat where add := add

def le (x y : NNRat) : Prop :=
  Quotient.lift₂ RawRat.le (fun _ _ _ _ ha hb => RawRat.le_congr ha hb) x y

instance : LE NNRat where le := le

def nsmul (m : Nat) (x : NNRat) : NNRat :=
  Quotient.lift (fun a => Quotient.mk RawRat.instSetoid (RawRat.nsmul m a))
    (fun _ _ h => Quotient.sound (RawRat.nsmul_congr m h)) x

theorem mk_eq_mk {n1 d1 n2 d2 : Nat} {h1 : 0 < d1} {h2 : 0 < d2}
    (h : n1 * d2 = n2 * d1) : mk n1 d1 h1 = mk n2 d2 h2 :=
  Quotient.sound h

theorem add_comm (x y : NNRat) : x + y = y + x := by
  refine Quotient.inductionOn₂ x y fun a b => Quotient.sound ?_
  show RawRat.Equiv (RawRat.add a b) (RawRat.add b a)
  unfold RawRat.Equiv RawRat.add
  simp only
  have h1 : a.num * b.den + b.num * a.den = b.num * a.den + a.num * b.den := Nat.add_comm _ _
  have h2 : b.den * a.den = a.den * b.den := Nat.mul_comm _ _
  rw [h1, h2]

theorem add_assoc (x y z : NNRat) : x + y + z = x + (y + z) := by
  refine Quotient.inductionOn₃ x y z fun a b c => Quotient.sound ?_
  show RawRat.Equiv (RawRat.add (RawRat.add a b) c) (RawRat.add a (RawRat.add b c))
  unfold RawRat.Equiv RawRat.add
  simp only [Nat.add_mul]
  ac_rfl

theorem zero_add (x : NNRat) : zero + x = x := by
  refine Quotient.inductionOn x fun a => Quotient.sound ?_
  show (0 * a.den + a.num * 1) * a.den = a.num * (1 * a.den)
  simp

theorem add_zero (x : NNRat) : x + zero = x := by
  rw [add_comm, zero_add]

theorem ofNat_add (a b : Nat) : ofNat a + ofNat b = ofNat (a + b) := by
  apply Quotient.sound
  show (a * 1 + b * 1) * 1 = (a + b) * (1 * 1)
  omega

theorem nsmul_zero_left (x : NNRat) : nsmul 0 x = zero := by
  refine Quotient.inductionOn x fun a => Quotient.sound ?_
  show (0 * a.num) * 1 = 0 * a.den
  omega

theorem nsmul_zero_right (m : Nat) : nsmul m zero = zero := by
  apply Quotient.sound
  show (m * 0) * 1 = 0 * 1
  omega

theorem nsmul_succ (m : Nat) (x : NNRat) : nsmul (m + 1) x = x + nsmul m x := by
  refine Quotient.inductionOn x fun a => Quotient.sound ?_
  show ((m + 1) * a.num) * (a.den * a.den) = (a.num * a.den + m * a.num * a.den) * a.den
  simp only [Nat.add_mul, Nat.one_mul]
  ac_rfl

theorem nsmul_inv_self (d : Nat) (hd : 0 < d) : nsmul d (inv d hd) = ofNat 1 := by
  apply Quotient.sound
  show (d * 1) * 1 = 1 * d
  omega

theorem nsmul_ofNat_one (m : Nat) : nsmul m (ofNat 1) = ofNat m := by
  apply Quotient.sound
  show (m * 1) * 1 = m * 1
  omega

theorem one_add_inv_pred (s : Nat) (hs : 2 ≤ s) :
    ofNat 1 + inv (s - 1) (by omega) = mk s (s - 1) (by omega) := by
  apply Quotient.sound
  show (1 * (s - 1) + 1 * 1) * (s - 1) = s * (1 * (s - 1))
  have hs1 : 1 * (s - 1) + 1 * 1 = s := by omega
  rw [hs1, Nat.one_mul]

theorem le_refl (x : NNRat) : x ≤ x := by
  refine Quotient.inductionOn x fun a => ?_
  exact Nat.le_refl _

theorem le_trans {x y z : NNRat} (hxy : x ≤ y) (hyz : y ≤ z) : x ≤ z := by
  revert hxy hyz
  refine Quotient.inductionOn₃ x y z fun a b c hxy hyz => ?_
  change a.num * b.den ≤ b.num * a.den at hxy
  change b.num * c.den ≤ c.num * b.den at hyz
  change a.num * c.den ≤ c.num * a.den
  refine Nat.le_of_mul_le_mul_right ?_ b.den_pos
  calc
    a.num * c.den * b.den = a.num * b.den * c.den := by ac_rfl
    _ ≤ b.num * a.den * c.den := Nat.mul_le_mul_right c.den hxy
    _ = b.num * c.den * a.den := by ac_rfl
    _ ≤ c.num * b.den * a.den := Nat.mul_le_mul_right a.den hyz
    _ = c.num * a.den * b.den := by ac_rfl

theorem add_le_add {x1 x2 y1 y2 : NNRat} (hx : x1 ≤ x2) (hy : y1 ≤ y2) :
    x1 + y1 ≤ x2 + y2 := by
  revert hx hy
  refine Quotient.inductionOn₂ x1 x2 fun a1 a2 =>
    Quotient.inductionOn₂ y1 y2 fun b1 b2 hx hy => ?_
  change a1.num * a2.den ≤ a2.num * a1.den at hx
  change b1.num * b2.den ≤ b2.num * b1.den at hy
  change (a1.num * b1.den + b1.num * a1.den) * (a2.den * b2.den) ≤
    (a2.num * b2.den + b2.num * a2.den) * (a1.den * b1.den)
  simp only [Nat.add_mul]
  have h1 : a1.num * b1.den * (a2.den * b2.den) ≤ a2.num * b2.den * (a1.den * b1.den) := by
    calc
      a1.num * b1.den * (a2.den * b2.den)
          = (a1.num * a2.den) * (b1.den * b2.den) := by ac_rfl
      _ ≤ (a2.num * a1.den) * (b1.den * b2.den) := Nat.mul_le_mul_right _ hx
      _ = a2.num * b2.den * (a1.den * b1.den) := by ac_rfl
  have h2 : b1.num * a1.den * (a2.den * b2.den) ≤ b2.num * a2.den * (a1.den * b1.den) := by
    calc
      b1.num * a1.den * (a2.den * b2.den)
          = (b1.num * b2.den) * (a1.den * a2.den) := by ac_rfl
      _ ≤ (b2.num * b1.den) * (a1.den * a2.den) := Nat.mul_le_mul_right _ hy
      _ = b2.num * a2.den * (a1.den * b1.den) := by ac_rfl
  exact Nat.add_le_add h1 h2

theorem zero_le (x : NNRat) : zero ≤ x := by
  refine Quotient.inductionOn x fun a => ?_
  change 0 * a.den ≤ a.num * 1
  omega

theorem inv_le_one (d : Nat) (hd : 0 < d) : inv d hd ≤ ofNat 1 := by
  change 1 * 1 ≤ 1 * d
  omega

theorem inv_anti {a b : Nat} (ha : 0 < a) (hb : 0 < b) (h : a ≤ b) :
    inv b hb ≤ inv a ha := by
  change 1 * a ≤ 1 * b
  omega

theorem le_add_five_halves_imp {k n : Nat} (h : ofNat k ≤ ofNat n + mk 5 2 (by omega)) :
    k ≤ n + 2 := by
  change k * (1 * 2) ≤ (n * 2 + 5 * 1) * 1 at h
  omega

/-- Lemma 2 of PROOF.md: for integers `a, b >= 1` and `s >= 2` with `a + b >= s`,
    `1 / a + 1 / b <= 1 + 1 / (s - 1)`. -/
theorem reciprocal_pair_bound {a b s : Nat} (ha : 1 ≤ a) (hb : 1 ≤ b)
    (hs : 2 ≤ s) (hab : s ≤ a + b) :
    inv a (by omega) + inv b (by omega) ≤ ofNat 1 + inv (s - 1) (by omega) := by
  change (1 * b + 1 * a) * (1 * (s - 1)) ≤ (1 * (s - 1) + 1 * 1) * (a * b)
  have ha' : a = (a - 1) + 1 := by omega
  have hb' : b = (b - 1) + 1 := by omega
  let a0 := a - 1
  let b0 := b - 1
  let s0 := s - 2
  let d := (a0 + b0) - s0
  have lhs_eq : (1 * b + 1 * a) * (1 * (s - 1)) = (s0 + d + 2) * (s0 + 1) := by
    have h1 : 1 * b + 1 * a = s0 + d + 2 := by omega
    have h2 : 1 * (s - 1) = s0 + 1 := by omega
    rw [h1, h2]
  have rhs_ge : (s0 + 2) * (s0 + d + 1) ≤ (1 * (s - 1) + 1 * 1) * (a * b) := by
    have h1 : 1 * (s - 1) + 1 * 1 = s0 + 2 := by omega
    have h2 : s0 + d + 1 ≤ a * b := by
      calc
        s0 + d + 1 = a0 + b0 + 1 := by omega
        _ ≤ a0 * b0 + a0 + b0 + 1 := by omega
        _ = (a0 + 1) * (b0 + 1) := by
          simp only [Nat.add_mul, Nat.mul_add]
          ac_rfl
        _ = a * b := by rw [← ha', ← hb']
    rw [h1]
    exact Nat.mul_le_mul_left (s0 + 2) h2
  have step : (s0 + d + 2) * (s0 + 1) ≤ (s0 + 2) * (s0 + d + 1) := by
    have hcomm : d * s0 = s0 * d := Nat.mul_comm d s0
    simp only [Nat.add_mul, Nat.mul_add, hcomm]
    omega
  omega

end NNRat

/-! ## Section 2: Finite List Counting and Summation Utilities -/

namespace SubQuorumAux

def qsum {α : Type} (l : List α) (f : α → NNRat) : NNRat :=
  match l with
  | [] => NNRat.zero
  | x :: xs => f x + qsum xs f

theorem qsum_congr {α : Type} {l : List α} {f g : α → NNRat}
    (h : ∀ x ∈ l, f x = g x) : qsum l f = qsum l g := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    simp only [qsum]
    rw [h a List.mem_cons_self, ih (fun x hx => h x (List.mem_cons_of_mem a hx))]

theorem qsum_le {α : Type} {l : List α} {f g : α → NNRat}
    (h : ∀ x ∈ l, f x ≤ g x) : qsum l f ≤ qsum l g := by
  induction l with
  | nil => exact NNRat.le_refl _
  | cons a tl ih =>
    simp only [qsum]
    exact NNRat.add_le_add (h a List.mem_cons_self)
      (ih (fun x hx => h x (List.mem_cons_of_mem a hx)))

theorem qsum_add {α : Type} (l : List α) (f g : α → NNRat) :
    qsum l (fun x => f x + g x) = qsum l f + qsum l g := by
  induction l with
  | nil =>
    simp only [qsum]
    rw [NNRat.add_zero]
  | cons a tl ih =>
    simp only [qsum, ih]
    calc
      (f a + g a) + (qsum tl f + qsum tl g)
          = f a + (g a + (qsum tl f + qsum tl g)) := NNRat.add_assoc _ _ _
      _ = f a + ((g a + qsum tl f) + qsum tl g) := by rw [← NNRat.add_assoc (g a)]
      _ = f a + ((qsum tl f + g a) + qsum tl g) := by rw [NNRat.add_comm (g a) (qsum tl f)]
      _ = f a + (qsum tl f + (g a + qsum tl g)) := by rw [NNRat.add_assoc (qsum tl f)]
      _ = (f a + qsum tl f) + (g a + qsum tl g) := (NNRat.add_assoc _ _ _).symm

theorem qsum_const {α : Type} (l : List α) (c : NNRat) :
    qsum l (fun _ => c) = NNRat.nsmul l.length c := by
  induction l with
  | nil =>
    simp only [qsum, List.length_nil, NNRat.nsmul_zero_left]
  | cons a tl ih =>
    simp only [qsum, List.length_cons, NNRat.nsmul_succ, ih]

theorem qsum_ite_zero {α : Type} (l : List α) (p : α → Bool) (c : NNRat) :
    qsum l (fun x => if p x then c else NNRat.zero) = NNRat.nsmul (l.countP p) c := by
  induction l with
  | nil =>
    simp [qsum, NNRat.nsmul_zero_left]
  | cons a tl ih =>
    simp only [qsum]
    cases hp : p a
    · simp [hp, ih, NNRat.zero_add]
    · simp [hp, ih, NNRat.nsmul_succ]

theorem qsum_ite {α : Type} (l : List α) (p : α → Bool) (c1 c2 : NNRat) :
    qsum l (fun x => if p x then c1 else c2) =
      NNRat.nsmul (l.countP p) c1 + NNRat.nsmul (l.countP (fun x => !p x)) c2 := by
  have hsplit : qsum l (fun x => if p x then c1 else c2) =
      qsum l (fun x => (if p x then c1 else NNRat.zero) + (if !p x then c2 else NNRat.zero)) := by
    apply qsum_congr
    intro x _
    cases p x <;> simp [NNRat.zero_add, NNRat.add_zero]
  rw [hsplit, qsum_add, qsum_ite_zero, qsum_ite_zero]

theorem qsum_split {α : Type} (l : List α) (b : α → Bool) (f : α → NNRat) :
    qsum l f =
      qsum l (fun x => if !b x then f x else NNRat.zero) +
      qsum l (fun x => if b x then f x else NNRat.zero) := by
  rw [← qsum_add]
  apply qsum_congr
  intro x _
  cases b x <;> simp [NNRat.zero_add, NNRat.add_zero]

theorem qsum_filter {α : Type} (l : List α) (b : α → Bool) (f : α → NNRat) :
    qsum (l.filter b) f = qsum l (fun x => if b x then f x else NNRat.zero) := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    cases hb : b a
    · simp only [List.filter, hb, Bool.false_eq_true, ↓reduceIte, qsum, NNRat.zero_add, ih]
    · simp only [List.filter, hb, ↓reduceIte, qsum, ih]

theorem qsum_map {α β : Type} (l : List α) (g : α → β) (f : β → NNRat) :
    qsum (l.map g) f = qsum l (fun x => f (g x)) := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    simp only [List.map, qsum, ih]

theorem qsum_comm {α β : Type} (l1 : List α) (l2 : List β) (h : α → β → NNRat) :
    qsum l1 (fun x => qsum l2 (fun y => h x y)) =
      qsum l2 (fun y => qsum l1 (fun x => h x y)) := by
  induction l1 with
  | nil =>
    simp only [qsum, qsum_const, NNRat.nsmul_zero_right]
  | cons a tl ih =>
    simp only [qsum, ih, ← qsum_add]

theorem countP_congr {α : Type} {l : List α} {p q : α → Bool}
    (h : ∀ x ∈ l, p x = q x) : l.countP p = l.countP q := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    simp only [List.countP_cons, h a List.mem_cons_self,
      ih (fun x hx => h x (List.mem_cons_of_mem a hx))]

theorem countP_split {α : Type} (l : List α) (p b : α → Bool) :
    l.countP p = l.countP (fun x => p x && b x) + l.countP (fun x => p x && !b x) := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    simp only [List.countP_cons, ih]
    cases p a <;> cases b a <;> simp <;> omega

theorem countP_filter {α : Type} (l : List α) (b p : α → Bool) :
    (l.filter b).countP p = l.countP (fun x => p x && b x) := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    cases hb : b a <;> cases hp : p a <;> simp [List.filter, hb, hp, ih]

theorem countP_map {α β : Type} (l : List α) (f : α → β) (p : β → Bool) :
    (l.map f).countP p = l.countP (fun x => p (f x)) := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    simp only [List.map, List.countP_cons, ih]

theorem length_filter_eq_countP {α : Type} (l : List α) (b : α → Bool) :
    (l.filter b).length = l.countP b := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    simp only [List.filter, List.countP_cons]
    cases b a <;> simp [ih] <;> omega

theorem nodup_countP_beq_eq_one {n : Nat} {l : List (Fin n)} (hnd : l.Nodup)
    {v : Fin n} (hv : v ∈ l) : l.countP (fun u => u == v) = 1 := by
  induction l with
  | nil => cases hv
  | cons a tl ih =>
    have hcons := List.nodup_cons.mp hnd
    rcases hcons with ⟨ha_not_mem, hnd_tl⟩
    simp only [List.countP_cons]
    by_cases hav : a = v
    · subst hav
      have hzero : tl.countP (fun u => u == a) = 0 := by
        rw [List.countP_eq_zero]
        intro u hu hbeq
        have heq : u = a := beq_iff_eq.mp hbeq
        subst heq
        exact ha_not_mem hu
      simp [hzero]
    · have hmem : v ∈ tl := by
        cases List.mem_cons.mp hv with
        | inl h => exact absurd h.symm hav
        | inr h => exact h
      have hbeq : (a == v) = false := beq_false_of_ne hav
      simp [hbeq, ih hnd_tl hmem]

def nsum {α : Type} (l : List α) (f : α → Nat) : Nat :=
  match l with
  | [] => 0
  | x :: xs => f x + nsum xs f

theorem nsum_congr {α : Type} {l : List α} {f g : α → Nat}
    (h : ∀ x ∈ l, f x = g x) : nsum l f = nsum l g := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    simp only [nsum, h a List.mem_cons_self,
      ih (fun x hx => h x (List.mem_cons_of_mem a hx))]

theorem nsum_add {α : Type} (l : List α) (f g : α → Nat) :
    nsum l (fun x => f x + g x) = nsum l f + nsum l g := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    simp only [nsum, ih]
    omega

theorem nsum_comm {α β : Type} (l1 : List α) (l2 : List β) (h : α → β → Nat) :
    nsum l1 (fun x => nsum l2 (fun y => h x y)) =
      nsum l2 (fun y => nsum l1 (fun x => h x y)) := by
  induction l1 with
  | nil =>
    simp only [nsum]
    induction l2 with
    | nil => rfl
    | cons b tl2 ih2 => simp [nsum, ← ih2]
  | cons a tl ih =>
    simp only [nsum, ih, ← nsum_add]

theorem countP_eq_nsum {α : Type} (l : List α) (p : α → Bool) :
    l.countP p = nsum l (fun x => if p x then 1 else 0) := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    simp only [List.countP_cons, nsum, ih]
    cases p a <;> omega

theorem nsum_mod_two_eq_odd_count {α : Type} (l : List α) (d : α → Nat) :
    (nsum l d) % 2 = (l.countP (fun x => d x % 2 == 1)) % 2 := by
  induction l with
  | nil => rfl
  | cons a tl ih =>
    simp only [nsum, List.countP_cons]
    by_cases hodd : d a % 2 = 1
    · have hb : (d a % 2 == 1) = true := beq_iff_eq.mpr hodd
      rw [hb]
      simp only [↓reduceIte]
      omega
    · have hb : (d a % 2 == 1) = false := beq_false_of_ne hodd
      rw [hb]
      simp only [Bool.false_eq_true, ↓reduceIte]
      omega

end SubQuorumAux

/-! ## Section 3: Exact Graph and Sub-Quorum Coloring Definitions -/

/-- Exact cardinality `|{u : Fin n | p u = true}|`. -/
def cardFin (n : Nat) (p : Fin n → Bool) : Nat :=
  (List.finRange n).countP p

theorem cardFin_mono {n : Nat} {p q : Fin n → Bool}
    (h : ∀ u : Fin n, p u = true → q u = true) : cardFin n p ≤ cardFin n q :=
  List.countP_mono_left (fun u _ hp => h u hp)

theorem cardFin_congr {n : Nat} {p q : Fin n → Bool}
    (h : ∀ u : Fin n, p u = q u) : cardFin n p = cardFin n q :=
  SubQuorumAux.countP_congr (fun u _ => h u)

theorem cardFin_beq_eq_one {n : Nat} (v : Fin n) :
    cardFin n (fun u => u == v) = 1 :=
  SubQuorumAux.nodup_countP_beq_eq_one (List.nodup_finRange n) (List.mem_finRange v)

theorem cardFin_split_all {n : Nat} (b : Fin n → Bool) :
    cardFin n b + cardFin n (fun u => !b u) = n := by
  have h := SubQuorumAux.countP_split (List.finRange n) (fun _ => true) b
  have hall : (List.finRange n).countP (fun _ => true) = n := by
    rw [List.countP_true, List.length_finRange]
  simp only [Bool.true_and] at h
  have h' : (List.finRange n).countP (fun _ => true) =
      cardFin n b + cardFin n (fun u => !b u) := h
  omega

/-- Finite simple undirected graph on `Fin n`. -/
structure SimpleGraph (n : Nat) where
  adj : Fin n → Fin n → Bool
  symm : ∀ u v, adj u v = adj v u
  loopless : ∀ v, adj v v = false

namespace SimpleGraph

/-- Graph complement on `Fin n`, with `adj u v = (u != v && !G.adj u v)`. -/
def compl {n : Nat} (G : SimpleGraph n) : SimpleGraph n where
  adj u v := (u != v && !G.adj u v)
  symm u v := by
    by_cases huv : u = v
    · subst huv; simp
    · have hvu : v ≠ u := Ne.symm huv
      have hb1 : (u != v) = true := bne_iff_ne.mpr huv
      have hb2 : (v != u) = true := bne_iff_ne.mpr hvu
      rw [hb1, hb2, G.symm u v]
  loopless v := by simp

/-- Closed neighborhood membership `N_G[v] = {u : Fin n | u = v ∨ G.adj v u = true}`. -/
def inClosedNbr {n : Nat} (G : SimpleGraph n) (v u : Fin n) : Bool :=
  (u == v) || G.adj v u

theorem inClosedNbr_iff {n : Nat} (G : SimpleGraph n) (v u : Fin n) :
    G.inClosedNbr v u = true ↔ (u = v ∨ G.adj v u = true) := by
  simp [inClosedNbr, beq_iff_eq]

/-- Degree `|N_G(v)|` of vertex `v` in `G`. -/
def deg {n : Nat} (G : SimpleGraph n) (v : Fin n) : Nat :=
  cardFin n (fun u => G.adj v u)

/-- Induced degree `d_I(v) = |N_G(v) ∩ I|` of vertex `v` in subset `I`. -/
def inducedDeg {n : Nat} (G : SimpleGraph n) (I : Fin n → Bool) (v : Fin n) : Nat :=
  cardFin n (fun u => G.adj v u && I u)

theorem adj_ne {n : Nat} (G : SimpleGraph n) {v u : Fin n} (h : G.adj v u = true) : u ≠ v := by
  intro heq
  subst heq
  rw [G.loopless] at h
  cases h

theorem deg_le_pred {n : Nat} (G : SimpleGraph n) (v : Fin n) : G.deg v ≤ n - 1 := by
  have hsplit := cardFin_split_all (n := n) (fun u => u == v)
  rw [cardFin_beq_eq_one v] at hsplit
  have hle : G.deg v ≤ cardFin n (fun u => !(u == v)) := by
    apply cardFin_mono
    intro u hadj
    have hne : u ≠ v := G.adj_ne hadj
    simp [beq_false_of_ne hne]
  omega

theorem closedNbr_inter_card {n : Nat} (G : SimpleGraph n) (I : Fin n → Bool)
    (v : Fin n) (hv : I v = true) :
    cardFin n (fun u => G.inClosedNbr v u && I u) = 1 + G.inducedDeg I v := by
  unfold inducedDeg cardFin
  rw [SubQuorumAux.countP_split (List.finRange n)
    (fun u => G.inClosedNbr v u && I u) (fun u => u == v)]
  have h1 : (List.finRange n).countP (fun u => (G.inClosedNbr v u && I u) && (u == v)) = 1 := by
    have heq : (List.finRange n).countP (fun u => (G.inClosedNbr v u && I u) && (u == v)) =
        cardFin n (fun u => u == v) := by
      apply SubQuorumAux.countP_congr
      intro u _
      by_cases huv : u = v
      · subst huv; simp [inClosedNbr, hv]
      · simp [beq_false_of_ne huv]
    rw [heq, cardFin_beq_eq_one v]
  have h2 : (List.finRange n).countP (fun u => (G.inClosedNbr v u && I u) && !(u == v)) =
      (List.finRange n).countP (fun u => G.adj v u && I u) := by
    apply SubQuorumAux.countP_congr
    intro u _
    by_cases huv : u = v
    · subst huv; simp [G.loopless]
    · simp [inClosedNbr, beq_false_of_ne huv]
  rw [h1, h2]

theorem compl_inducedDeg_eq {n : Nat} (G : SimpleGraph n) (I : Fin n → Bool)
    (v : Fin n) (hv : I v = true) :
    G.compl.inducedDeg I v = cardFin n I - 1 - G.inducedDeg I v := by
  have hsplit1 : cardFin n I =
      (List.finRange n).countP (fun u => I u && (u == v)) +
      (List.finRange n).countP (fun u => I u && !(u == v)) :=
    SubQuorumAux.countP_split (List.finRange n) I (fun u => u == v)
  have h1 : (List.finRange n).countP (fun u => I u && (u == v)) = 1 := by
    have heq : (List.finRange n).countP (fun u => I u && (u == v)) =
        cardFin n (fun u => u == v) := by
      apply SubQuorumAux.countP_congr
      intro u _
      by_cases huv : u = v
      · subst huv; simp [hv]
      · simp [beq_false_of_ne huv]
    rw [heq, cardFin_beq_eq_one v]
  have hsplit2 : (List.finRange n).countP (fun u => I u && !(u == v)) =
      (List.finRange n).countP (fun u => (I u && !(u == v)) && G.adj v u) +
      (List.finRange n).countP (fun u => (I u && !(u == v)) && !G.adj v u) :=
    SubQuorumAux.countP_split (List.finRange n) (fun u => I u && !(u == v)) (fun u => G.adj v u)
  have h2a : (List.finRange n).countP (fun u => (I u && !(u == v)) && G.adj v u) =
      G.inducedDeg I v := by
    apply SubQuorumAux.countP_congr
    intro u _
    by_cases huv : u = v
    · subst huv; simp [G.loopless]
    · simp [beq_false_of_ne huv, Bool.and_comm]
  have h2b : (List.finRange n).countP (fun u => (I u && !(u == v)) && !G.adj v u) =
      G.compl.inducedDeg I v := by
    apply SubQuorumAux.countP_congr
    intro u _
    by_cases huv : u = v
    · subst huv; simp [SimpleGraph.compl]
    · have hvu : v ≠ u := Ne.symm huv
      have hb1 : (u == v) = false := beq_false_of_ne huv
      have hb2 : (v != u) = true := bne_iff_ne.mpr hvu
      simp [SimpleGraph.compl, hb1, hb2, Bool.and_comm]
  omega

/-- Embedding of `Fin (cardFin n I)` into `Fin n` enumerating `{v | I v = true}`. -/
def induceEmb {n : Nat} (I : Fin n → Bool) (i : Fin (cardFin n I)) : Fin n :=
  ((List.finRange n).filter I)[i.val]'(by
    rw [SubQuorumAux.length_filter_eq_countP]
    exact i.isLt)

/-- Induced subgraph `G[I]` as a `SimpleGraph (cardFin n I)`. -/
def induce {n : Nat} (G : SimpleGraph n) (I : Fin n → Bool) : SimpleGraph (cardFin n I) where
  adj i j := G.adj (induceEmb I i) (induceEmb I j)
  symm i j := G.symm (induceEmb I i) (induceEmb I j)
  loopless i := G.loopless (induceEmb I i)

theorem map_induceEmb {n : Nat} (I : Fin n → Bool) :
    (List.finRange (cardFin n I)).map (induceEmb I) = (List.finRange n).filter I := by
  apply List.ext_getElem
  · simp only [List.length_map, List.length_finRange, SubQuorumAux.length_filter_eq_countP]
    rfl
  · intro k hk1 hk2
    simp [induceEmb]

theorem induce_deg_eq {n : Nat} (G : SimpleGraph n) (I : Fin n → Bool)
    (i : Fin (cardFin n I)) :
    (G.induce I).deg i = G.inducedDeg I (induceEmb I i) := by
  show (List.finRange (cardFin n I)).countP (fun j => G.adj (induceEmb I i) (induceEmb I j)) =
    (List.finRange n).countP (fun u => G.adj (induceEmb I i) u && I u)
  rw [← SubQuorumAux.countP_map (List.finRange (cardFin n I)) (induceEmb I)
    (fun u => G.adj (induceEmb I i) u)]
  rw [map_induceEmb, SubQuorumAux.countP_filter]

end SimpleGraph

/-- Complete graph `K_n` on `Fin n`. -/
def completeGraph (n : Nat) : SimpleGraph n where
  adj u v := u != v
  symm u v := by
    by_cases huv : u = v
    · subst huv; simp
    · simp [bne_iff_ne.mpr huv, bne_iff_ne.mpr (Ne.symm huv)]
  loopless v := by simp

/-- Sub-quorum coloring of `G` with `k` colors (Definition 2.2 of `arXiv:2609.25128v4`):
    a partial coloring `f : Fin n → Option (Fin k)` that is surjective onto `Fin k`
    and satisfies weak majority on the colored closed neighborhood of every colored vertex. -/
structure SubQuorumColoring {n : Nat} (G : SimpleGraph n) (k : Nat) where
  f : Fin n → Option (Fin k)
  surj : ∀ c : Fin k, ∃ v : Fin n, f v = some c
  quorum : ∀ (v : Fin n) (c : Fin k), f v = some c →
    2 * cardFin n (fun u => G.inClosedNbr v u && (f u == some c)) ≥
      cardFin n (fun u => G.inClosedNbr v u && (f u).isSome)

/-! ## Section 4: Lemma 1 (Vertex-Weight Identity and Induced-Degree Class-Size Bound) -/

namespace SubQuorumColoring

/-- Color class size `|C_c| = |{u : Fin n | f u = some c}|`. -/
def classSize {n k : Nat} {G : SimpleGraph n} (col : SubQuorumColoring G k) (c : Fin k) : Nat :=
  cardFin n (fun u => col.f u == some c)

theorem classSize_pos {n k : Nat} {G : SimpleGraph n} (col : SubQuorumColoring G k) (c : Fin k) :
    0 < col.classSize c := by
  unfold classSize cardFin
  rw [List.countP_pos_iff]
  rcases col.surj c with ⟨v, hv⟩
  exact ⟨v, List.mem_finRange v, by simp [hv]⟩

/-- Vertex reciprocal weight `w_f(v) = 1 / |C_{f(v)}|` if colored, and `0` if uncolored. -/
def weight {n k : Nat} {G : SimpleGraph n} (col : SubQuorumColoring G k) (v : Fin n) : NNRat :=
  match col.f v with
  | none => NNRat.zero
  | some c => NNRat.inv (col.classSize c) (col.classSize_pos c)

theorem weight_le_one {n k : Nat} {G : SimpleGraph n} (col : SubQuorumColoring G k) (v : Fin n) :
    col.weight v ≤ NNRat.ofNat 1 := by
  unfold weight
  cases col.f v with
  | none => exact NNRat.zero_le _
  | some c => exact NNRat.inv_le_one _ _

theorem weight_eq_zero_of_isSome_false {n k : Nat} {G : SimpleGraph n}
    (col : SubQuorumColoring G k) (v : Fin n) (h : (col.f v).isSome = false) :
    col.weight v = NNRat.zero := by
  unfold weight
  cases hf : col.f v with
  | none => rfl
  | some c => simp [hf] at h

/-- Lemma 1(1) of PROOF.md: the vertex weights sum to `k` across `Fin n`. -/
theorem weight_sum_eq {n k : Nat} {G : SimpleGraph n} (col : SubQuorumColoring G k) :
    SubQuorumAux.qsum (List.finRange n) col.weight = NNRat.ofNat k := by
  have hpoint : ∀ v ∈ List.finRange n, col.weight v =
      SubQuorumAux.qsum (List.finRange k) (fun c =>
        if col.f v == some c then NNRat.inv (col.classSize c) (col.classSize_pos c)
        else NNRat.zero) := by
    intro v _
    unfold weight
    cases hf : col.f v with
    | none =>
      have hz : SubQuorumAux.qsum (List.finRange k) (fun c : Fin k =>
          if (none : Option (Fin k)) == some c then
            NNRat.inv (col.classSize c) (col.classSize_pos c)
          else NNRat.zero) = SubQuorumAux.qsum (List.finRange k) (fun _ => NNRat.zero) := by
        apply SubQuorumAux.qsum_congr
        intro c _
        rfl
      rw [hz, SubQuorumAux.qsum_const, NNRat.nsmul_zero_right]
    | some c0 =>
      have heq : SubQuorumAux.qsum (List.finRange k) (fun c : Fin k =>
          if (some c0 == some c) then NNRat.inv (col.classSize c) (col.classSize_pos c)
          else NNRat.zero) =
          SubQuorumAux.qsum (List.finRange k) (fun c : Fin k =>
            if c == c0 then NNRat.inv (col.classSize c0) (col.classSize_pos c0)
            else NNRat.zero) := by
        apply SubQuorumAux.qsum_congr
        intro c _
        by_cases hcc : c = c0
        · subst hcc; simp
        · have hne : (some c0 == some c) = false := by
            cases hb : (some c0 == some c)
            · rfl
            · exfalso
              have : some c0 = some c := beq_iff_eq.mp hb
              injection this with h'; exact hcc h'.symm
          simp [hne, beq_false_of_ne hcc]
      rw [heq, SubQuorumAux.qsum_ite_zero]
      have hc1 : (List.finRange k).countP (fun c => c == c0) = 1 :=
        cardFin_beq_eq_one c0
      rw [hc1, NNRat.nsmul_succ, NNRat.nsmul_zero_left, NNRat.add_zero]
  rw [SubQuorumAux.qsum_congr hpoint, SubQuorumAux.qsum_comm]
  have hclass : ∀ c ∈ List.finRange k,
      SubQuorumAux.qsum (List.finRange n) (fun v =>
        if col.f v == some c then NNRat.inv (col.classSize c) (col.classSize_pos c)
        else NNRat.zero) = NNRat.ofNat 1 := by
    intro c _
    rw [SubQuorumAux.qsum_ite_zero]
    exact NNRat.nsmul_inv_self (col.classSize c) (col.classSize_pos c)
  rw [SubQuorumAux.qsum_congr hclass, SubQuorumAux.qsum_const,
    List.length_finRange, NNRat.nsmul_ofNat_one]

end SubQuorumColoring

/-- Lemma 1(2) of PROOF.md (`class_size_lower_bound`):
    for every subset `I` of the colored support and every vertex `v` in `I` with color `c`,
    `|C_c| >= 1 + d_I(v) / 2`. -/
theorem class_size_lower_bound {n k : Nat} {G : SimpleGraph n}
    (col : SubQuorumColoring G k) (I : Fin n → Bool)
    (hI : ∀ u : Fin n, I u = true → (col.f u).isSome = true)
    (v : Fin n) (hv : I v = true) (c : Fin k) (hc : col.f v = some c) :
    1 + G.inducedDeg I v / 2 ≤ col.classSize c := by
  have hsub1 : cardFin n (fun u => G.inClosedNbr v u && (col.f u == some c)) ≤ col.classSize c := by
    apply cardFin_mono
    intro u h
    simp only [Bool.and_eq_true] at h
    exact h.2
  have hquorum := col.quorum v c hc
  have hsub2 : cardFin n (fun u => G.inClosedNbr v u && I u) ≤
      cardFin n (fun u => G.inClosedNbr v u && (col.f u).isSome) := by
    apply cardFin_mono
    intro u h
    simp only [Bool.and_eq_true] at h ⊢
    exact ⟨h.1, hI u h.2⟩
  have hcard := G.closedNbr_inter_card I v hv
  omega

theorem weight_le_inv_inducedDeg {n k : Nat} {G : SimpleGraph n}
    (col : SubQuorumColoring G k) (I : Fin n → Bool)
    (hI : ∀ u : Fin n, I u = true → (col.f u).isSome = true)
    (v : Fin n) (hv : I v = true) :
    col.weight v ≤ NNRat.inv (1 + G.inducedDeg I v / 2) (by omega) := by
  unfold SubQuorumColoring.weight
  cases hc : col.f v with
  | none =>
    have hsome := hI v hv
    simp [hc] at hsome
  | some c =>
    have hcls := class_size_lower_bound col I hI v hv c hc
    exact NNRat.inv_anti (by omega) (col.classSize_pos c) hcls

/-! ## Section 5: Lemma 3 (Handshaking Weight Bound) -/

/-- Per-vertex summand of `Sigma(H)` from Lemma 3 of PROOF.md. -/
def sigmaTerm (m d : Nat) : NNRat :=
  NNRat.inv (1 + d / 2) (by omega) + NNRat.inv (1 + (m - 1 - d) / 2) (by omega)

/-- Complementary degree-weight sum `Sigma(H)` on a simple graph `H` of order `m`. -/
def sigma {m : Nat} (H : SimpleGraph m) : NNRat :=
  SubQuorumAux.qsum (List.finRange m) (fun v => sigmaTerm m (H.deg v))

/-- Handshaking parity: every finite simple graph has an even number of odd-degree vertices. -/
theorem odd_deg_count_even {m : Nat} (H : SimpleGraph m) :
    (cardFin m (fun v => H.deg v % 2 == 1)) % 2 = 0 := by
  let l := List.finRange m
  have hdeg : ∀ v ∈ l, H.deg v =
      SubQuorumAux.nsum l (fun u =>
        (if decide (v.val < u.val) && H.adj v u then 1 else 0) +
        (if decide (u.val < v.val) && H.adj v u then 1 else 0)) := by
    intro v _
    unfold SimpleGraph.deg cardFin
    rw [SubQuorumAux.countP_eq_nsum]
    apply SubQuorumAux.nsum_congr
    intro u _
    by_cases hlt : v.val < u.val
    · have hgt : ¬(u.val < v.val) := by omega
      simp [hlt, hgt]
    · by_cases hgt : u.val < v.val
      · simp [hlt, hgt]
      · have heq : v = u := Fin.ext (by omega)
        subst heq
        simp [H.loopless]
  have hsum_even : (SubQuorumAux.nsum l H.deg) % 2 = 0 := by
    rw [SubQuorumAux.nsum_congr hdeg]
    have hsplit : SubQuorumAux.nsum l (fun v =>
        SubQuorumAux.nsum l (fun u =>
          (if decide (v.val < u.val) && H.adj v u then 1 else 0) +
          (if decide (u.val < v.val) && H.adj v u then 1 else 0))) =
        SubQuorumAux.nsum l (fun v =>
          SubQuorumAux.nsum l (fun u => if decide (v.val < u.val) && H.adj v u then 1 else 0)) +
        SubQuorumAux.nsum l (fun v =>
          SubQuorumAux.nsum l (fun u => if decide (u.val < v.val) && H.adj v u then 1 else 0)) := by
      calc
        _ = SubQuorumAux.nsum l (fun v =>
              SubQuorumAux.nsum l (fun u => if decide (v.val < u.val) && H.adj v u then 1 else 0) +
              SubQuorumAux.nsum l (fun u => if decide (u.val < v.val) && H.adj v u then 1 else 0)) := by
            apply SubQuorumAux.nsum_congr
            intro v _
            exact SubQuorumAux.nsum_add l _ _
        _ = _ := SubQuorumAux.nsum_add l _ _
    have hsymm :
        SubQuorumAux.nsum l (fun v =>
          SubQuorumAux.nsum l (fun u => if decide (u.val < v.val) && H.adj v u then 1 else 0)) =
        SubQuorumAux.nsum l (fun u =>
          SubQuorumAux.nsum l (fun v => if decide (u.val < v.val) && H.adj u v then 1 else 0)) := by
      rw [SubQuorumAux.nsum_comm]
      apply SubQuorumAux.nsum_congr
      intro u _
      apply SubQuorumAux.nsum_congr
      intro v _
      rw [H.symm v u]
    rw [hsplit, hsymm]
    omega
  unfold cardFin
  rw [← SubQuorumAux.nsum_mod_two_eq_odd_count l H.deg]
  exact hsum_even

/-- Lemma 3 of PROOF.md (`handshaking_weight_bound`):
    for every finite simple graph `H` of order `m >= 0`, `Sigma(H) <= m + 5 / 2`. -/
theorem handshaking_weight_bound {m : Nat} (H : SimpleGraph m) :
    sigma H ≤ NNRat.ofNat m + NNRat.mk 5 2 (by omega) := by
  by_cases hm0 : m = 0
  · subst hm0
    unfold sigma
    simp only [List.finRange_zero, SubQuorumAux.qsum]
    exact NNRat.zero_le _
  · by_cases hm1 : m = 1
    · subst hm1
      unfold sigma
      have hfr1 : List.finRange 1 = [⟨0, by omega⟩] := rfl
      rw [hfr1]
      simp only [SubQuorumAux.qsum, NNRat.add_zero]
      have hd0 : H.deg ⟨0, by omega⟩ = 0 := by
        have hle := H.deg_le_pred ⟨0, by omega⟩
        omega
      rw [hd0]
      unfold sigmaTerm
      change (1 * 1 + 1 * 1) * (1 * 2) ≤ (1 * 2 + 5 * 1) * (1 * 1)
      omega
    · have hm2 : 2 ≤ m := by omega
      by_cases hpar : m % 2 = 0
      · -- Case C: m = 2 * r even, r >= 1
        let r := m / 2
        have hr : 1 ≤ r := by omega
        have hm_eq : m = 2 * r := by omega
        let c := NNRat.mk (r + 1) r (by omega)
        have hterm : ∀ v ∈ List.finRange m, sigmaTerm m (H.deg v) ≤ c := by
          intro v _
          have hd : H.deg v ≤ 2 * r - 1 := by
            have := H.deg_le_pred v
            omega
          unfold sigmaTerm
          have hpair := NNRat.reciprocal_pair_bound
            (a := 1 + H.deg v / 2) (b := 1 + (m - 1 - H.deg v) / 2) (s := r + 1)
            (by omega) (by omega) (by omega) (by omega)
          rw [NNRat.one_add_inv_pred (r + 1) (by omega)] at hpair
          exact hpair
        have hsum1 : sigma H ≤ SubQuorumAux.qsum (List.finRange m) (fun _ => c) :=
          SubQuorumAux.qsum_le hterm
        rw [SubQuorumAux.qsum_const, List.length_finRange] at hsum1
        apply NNRat.le_trans hsum1
        change (m * (r + 1)) * (1 * 2) ≤ (m * 2 + 5 * 1) * r
        rw [hm_eq]
        have lhs_eq : (2 * r * (r + 1)) * (1 * 2) = (2 * (r + 1) * (1 * 2)) * r := by ac_rfl
        rw [lhs_eq]
        exact Nat.mul_le_mul_right r (by omega)
      · -- Case D: m = 2 * r + 1 odd, r >= 1
        let r := m / 2
        have hr : 1 ≤ r := by omega
        have hm_eq : m = 2 * r + 1 := by omega
        let cOdd := NNRat.mk (r + 1) r (by omega)
        let cEven := NNRat.mk (r + 2) (r + 1) (by omega)
        let isOdd : Fin m → Bool := fun v => H.deg v % 2 == 1
        have hterm : ∀ v ∈ List.finRange m,
            sigmaTerm m (H.deg v) ≤ (if isOdd v then cOdd else cEven) := by
          intro v _
          have hd : H.deg v ≤ 2 * r := by
            have := H.deg_le_pred v
            omega
          by_cases hodd : H.deg v % 2 = 1
          · have hb : isOdd v = true := beq_iff_eq.mpr hodd
            rw [hb]
            simp only [↓reduceIte]
            unfold sigmaTerm
            have hpair := NNRat.reciprocal_pair_bound
              (a := 1 + H.deg v / 2) (b := 1 + (m - 1 - H.deg v) / 2) (s := r + 1)
              (by omega) (by omega) (by omega) (by omega)
            rw [NNRat.one_add_inv_pred (r + 1) (by omega)] at hpair
            exact hpair
          · have hb : isOdd v = false := beq_false_of_ne hodd
            rw [hb]
            simp only [Bool.false_eq_true, ↓reduceIte]
            unfold sigmaTerm
            have hpair := NNRat.reciprocal_pair_bound
              (a := 1 + H.deg v / 2) (b := 1 + (m - 1 - H.deg v) / 2) (s := r + 2)
              (by omega) (by omega) (by omega) (by omega)
            rw [NNRat.one_add_inv_pred (r + 2) (by omega)] at hpair
            exact hpair
        have hsum1 : sigma H ≤
            SubQuorumAux.qsum (List.finRange m) (fun v => if isOdd v then cOdd else cEven) :=
          SubQuorumAux.qsum_le hterm
        rw [SubQuorumAux.qsum_ite] at hsum1
        apply NNRat.le_trans hsum1
        let tOdd := cardFin m isOdd
        let tEven := cardFin m (fun v => !isOdd v)
        have ht_sum : tOdd + tEven = 2 * r + 1 := by
          have := cardFin_split_all isOdd
          omega
        have ht_even : tOdd % 2 = 0 := odd_deg_count_even H
        have ht_le : tOdd ≤ 2 * r := by omega
        change (tOdd * (r + 1) * (r + 1) + tEven * (r + 2) * r) * (1 * 2) ≤
          (m * 2 + 5 * 1) * (r * (r + 1))
        have hcomb : tOdd * (r + 1) * (r + 1) + tEven * (r + 2) * r =
            (2 * r + 1) * (r + 2) * r + tOdd := by
          have hsq : (r + 1) * (r + 1) = (r + 2) * r + 1 := by
            simp only [Nat.add_mul, Nat.mul_add]
            omega
          calc
            tOdd * (r + 1) * (r + 1) + tEven * (r + 2) * r
                = tOdd * ((r + 1) * (r + 1)) + tEven * ((r + 2) * r) := by ac_rfl
            _ = tOdd * ((r + 2) * r + 1) + tEven * ((r + 2) * r) := by rw [hsq]
            _ = (tOdd + tEven) * ((r + 2) * r) + tOdd := by
              simp only [Nat.add_mul, Nat.mul_add]
              ac_rfl
            _ = (2 * r + 1) * (r + 2) * r + tOdd := by
              rw [ht_sum]
              ac_rfl
        rw [hcomb, hm_eq]
        have hstep1 : ((2 * r + 1) * (r + 2) * r + tOdd) * (1 * 2) ≤
            (((2 * r + 1) * (r + 2) + 2) * 2) * r := by
          have hlin : ((2 * r + 1) * (r + 2) + 2) * r =
              (2 * r + 1) * (r + 2) * r + 2 * r := by
            simp only [Nat.add_mul]
          have hmul : (((2 * r + 1) * (r + 2) + 2) * 2) * r =
              ((2 * r + 1) * (r + 2) * r + 2 * r) * 2 := by
            calc
              (((2 * r + 1) * (r + 2) + 2) * 2) * r
                  = (((2 * r + 1) * (r + 2) + 2) * r) * 2 := by ac_rfl
              _ = ((2 * r + 1) * (r + 2) * r + 2 * r) * 2 := by rw [hlin]
          rw [hmul]
          omega
        have hstep2 : (((2 * r + 1) * (r + 2) + 2) * 2) * r ≤
            (((2 * r + 1) * 2 + 5 * 1) * (r + 1)) * r := by
          apply Nat.mul_le_mul_right r
          have hp1 : (2 * r + 1) * (r + 2) = 2 * (r * r) + 5 * r + 2 := by
            simp only [Nat.add_mul, Nat.mul_add, Nat.mul_assoc]
            omega
          have hp2 : ((2 * r + 1) * 2 + 5 * 1) * (r + 1) = 4 * (r * r) + 11 * r + 7 := by
            have h47 : (2 * r + 1) * 2 + 5 * 1 = 4 * r + 7 := by omega
            rw [h47]
            simp only [Nat.add_mul, Nat.mul_add, Nat.mul_assoc]
            omega
          rw [hp1, hp2]
          omega
        have hstep3 : (((2 * r + 1) * 2 + 5 * 1) * (r + 1)) * r =
            ((2 * r + 1) * 2 + 5 * 1) * (r * (r + 1)) := by ac_rfl
        omega

/-! ## Section 6: Theorem 1 and Conjecture 9.2 -/

/-- Theorem 1 of PROOF.md: for every finite simple graph `G` of order `n` and any
    sub-quorum colorings of `G` and `G.compl` with `k1` and `k2` colors, `k1 + k2 <= n + 2`. -/
theorem theorem_1 (n : Nat) (G : SimpleGraph n)
    (k1 k2 : Nat)
    (f1 : SubQuorumColoring G k1)
    (f2 : SubQuorumColoring G.compl k2) :
    k1 + k2 ≤ n + 2 := by
  let I : Fin n → Bool := fun v => (f1.f v).isSome && (f2.f v).isSome
  let m := cardFin n I
  have hm_def : m = (List.finRange n).countP I := rfl
  have hm_le_n : m ≤ n := by
    have := cardFin_split_all I
    omega
  have hk_sum : NNRat.ofNat (k1 + k2) =
      SubQuorumAux.qsum (List.finRange n) (fun v => f1.weight v + f2.weight v) := by
    rw [← NNRat.ofNat_add, ← f1.weight_sum_eq, ← f2.weight_sum_eq, ← SubQuorumAux.qsum_add]
  rw [SubQuorumAux.qsum_split (List.finRange n) I] at hk_sum
  -- Bound on V \ I
  have hext : SubQuorumAux.qsum (List.finRange n)
      (fun v => if !I v then f1.weight v + f2.weight v else NNRat.zero) ≤
      NNRat.ofNat (n - m) := by
    have hpt : ∀ v ∈ List.finRange n,
        (if !I v then f1.weight v + f2.weight v else NNRat.zero) ≤
        (if !I v then NNRat.ofNat 1 else NNRat.zero) := by
      intro v _
      cases hI_v : I v
      · simp only [Bool.not_false, ↓reduceIte]
        have hfalse : ((f1.f v).isSome && (f2.f v).isSome) = false := hI_v
        cases hs1 : (f1.f v).isSome
        · rw [f1.weight_eq_zero_of_isSome_false v hs1, NNRat.zero_add]
          exact f2.weight_le_one v
        · have hs2 : (f2.f v).isSome = false := by
            rw [hs1, Bool.true_and] at hfalse
            exact hfalse
          rw [f2.weight_eq_zero_of_isSome_false v hs2, NNRat.add_zero]
          exact f1.weight_le_one v
      · simp only [Bool.not_true, Bool.false_eq_true, ↓reduceIte]
        exact NNRat.le_refl _
    have hle1 := SubQuorumAux.qsum_le hpt
    rw [SubQuorumAux.qsum_ite_zero, NNRat.nsmul_ofNat_one] at hle1
    have hcnt : (List.finRange n).countP (fun v => !I v) = n - m := by
      have hsp := cardFin_split_all I
      have hc1 : cardFin n I = m := rfl
      have hc2 : cardFin n (fun u => !I u) = (List.finRange n).countP (fun v => !I v) := rfl
      omega
    rw [hcnt] at hle1
    exact hle1
  -- Bound on I
  have hI1 : ∀ u : Fin n, I u = true → (f1.f u).isSome = true := by
    intro u hu; simp only [I, Bool.and_eq_true] at hu; exact hu.1
  have hI2 : ∀ u : Fin n, I u = true → (f2.f u).isSome = true := by
    intro u hu; simp only [I, Bool.and_eq_true] at hu; exact hu.2
  have hint_pt : ∀ v ∈ List.finRange n,
      (if I v then f1.weight v + f2.weight v else NNRat.zero) ≤
      (if I v then sigmaTerm m (G.inducedDeg I v) else NNRat.zero) := by
    intro v _
    cases hIv : I v
    · simp only [Bool.false_eq_true, ↓reduceIte]
      exact NNRat.le_refl _
    · simp only [↓reduceIte]
      have hw1 := weight_le_inv_inducedDeg f1 I hI1 v hIv
      have hw2 := weight_le_inv_inducedDeg f2 I hI2 v hIv
      simp only [G.compl_inducedDeg_eq I v hIv] at hw2
      exact NNRat.add_le_add hw1 hw2
  have hint_eq : SubQuorumAux.qsum (List.finRange n)
      (fun v => if I v then sigmaTerm m (G.inducedDeg I v) else NNRat.zero) =
      sigma (G.induce I) := by
    rw [← SubQuorumAux.qsum_filter, ← SimpleGraph.map_induceEmb I, SubQuorumAux.qsum_map]
    unfold sigma
    apply SubQuorumAux.qsum_congr
    intro i _
    rw [G.induce_deg_eq I i]
  have hint : SubQuorumAux.qsum (List.finRange n)
      (fun v => if I v then f1.weight v + f2.weight v else NNRat.zero) ≤
      NNRat.ofNat m + NNRat.mk 5 2 (by omega) := by
    have h1 := SubQuorumAux.qsum_le hint_pt
    rw [hint_eq] at h1
    exact NNRat.le_trans h1 (handshaking_weight_bound (G.induce I))
  -- Combine V \ I and I bounds
  have htotal : NNRat.ofNat (k1 + k2) ≤ NNRat.ofNat n + NNRat.mk 5 2 (by omega) := by
    rw [hk_sum]
    have hadd := NNRat.add_le_add hext hint
    have hrhs : NNRat.ofNat (n - m) + (NNRat.ofNat m + NNRat.mk 5 2 (by omega)) =
        NNRat.ofNat n + NNRat.mk 5 2 (by omega) := by
      rw [← NNRat.add_assoc, NNRat.ofNat_add]
      have hnm : n - m + m = n := by omega
      rw [hnm]
    rw [hrhs] at hadd
    exact hadd
  exact NNRat.le_add_five_halves_imp htotal

/-- Main Theorem (`conjecture_9_2`): Ma, Sahbi & Zhang (`arXiv:2609.25128v4`) Conjecture 9.2.
    For every finite simple graph `G` on `n >= 2` vertices, any sub-quorum colorings
    of `G` and `G.compl` satisfy `k1 + k2 <= n + 2`. -/
theorem conjecture_9_2 (n : Nat) (hn : n ≥ 2) (G : SimpleGraph n)
    (k1 k2 : Nat)
    (f1 : SubQuorumColoring G k1)
    (f2 : SubQuorumColoring G.compl k2) :
    k1 + k2 ≤ n + 2 := by
  have _ := hn
  exact theorem_1 n G k1 k2 f1 f2

/-! ## Section 7: Sharpness on Complete Graphs (`sharpness_Kn`) -/

private def knMap (n : Nat) (v : Fin n) : Option (Fin 2) :=
  if v.val == 0 then some ⟨0, by omega⟩
  else if v.val == 1 then some ⟨1, by omega⟩
  else none

/-- Explicit 2-color sub-quorum coloring of `K_n` for `n >= 2` (coloring vertices `0` and `1`
    with distinct colors and leaving all remaining vertices uncolored). -/
def completeGraphColoring (n : Nat) (hn : n ≥ 2) :
    SubQuorumColoring (completeGraph n) 2 where
  f := knMap n
  surj c := by
    have _ := hn
    by_cases hc0 : c.val = 0
    · refine ⟨⟨0, by omega⟩, ?_⟩
      have hc_eq : c = ⟨0, by omega⟩ := Fin.ext hc0
      rw [hc_eq]
      rfl
    · have hc1 : c.val = 1 := by omega
      refine ⟨⟨1, by omega⟩, ?_⟩
      have hc_eq : c = ⟨1, by omega⟩ := Fin.ext hc1
      rw [hc_eq]
      rfl
  quorum v c hvc := by
    let v0 : Fin n := ⟨0, by omega⟩
    let v1 : Fin n := ⟨1, by omega⟩
    have hn_all : ∀ u : Fin n, (completeGraph n).inClosedNbr v u = true := by
      intro u
      unfold SimpleGraph.inClosedNbr completeGraph
      by_cases huv : u = v
      · subst huv; simp
      · simp [beq_false_of_ne huv, bne_iff_ne.mpr (Ne.symm huv)]
    have hsupp : cardFin n (fun u =>
        (completeGraph n).inClosedNbr v u && (knMap n u).isSome) = 2 := by
      have heq : cardFin n (fun u =>
          (completeGraph n).inClosedNbr v u && (knMap n u).isSome) =
          cardFin n (fun u => (u == v0) || (u == v1)) := by
        apply cardFin_congr
        intro u
        rw [hn_all u, Bool.true_and]
        unfold knMap
        by_cases hu0 : u.val = 0
        · have huv0 : u = v0 := Fin.ext hu0
          subst huv0; simp [v0]
        · by_cases hu1 : u.val = 1
          · have huv1 : u = v1 := Fin.ext hu1
            subst huv1; simp [v0, v1]
          · have hne0 : u ≠ v0 := fun h => hu0 (congrArg Fin.val h)
            have hne1 : u ≠ v1 := fun h => hu1 (congrArg Fin.val h)
            simp [hu0, hu1, beq_false_of_ne hne0, beq_false_of_ne hne1]
      rw [heq]
      unfold cardFin
      rw [SubQuorumAux.countP_split (List.finRange n)
        (fun u => (u == v0) || (u == v1)) (fun u => u == v0)]
      have hp0 : (List.finRange n).countP (fun u => ((u == v0) || (u == v1)) && (u == v0)) = 1 := by
        have h0 : (List.finRange n).countP (fun u => ((u == v0) || (u == v1)) && (u == v0)) =
            cardFin n (fun u => u == v0) := by
          apply SubQuorumAux.countP_congr
          intro u _
          cases u == v0 <;> simp
        rw [h0, cardFin_beq_eq_one v0]
      have hp1 : (List.finRange n).countP (fun u => ((u == v0) || (u == v1)) && !(u == v0)) = 1 := by
        have h1 : (List.finRange n).countP (fun u => ((u == v0) || (u == v1)) && !(u == v0)) =
            cardFin n (fun u => u == v1) := by
          apply SubQuorumAux.countP_congr
          intro u _
          by_cases hu0 : u = v0
          · subst hu0
            have hne : v0 ≠ v1 := by intro h; injection h with h'; omega
            simp [beq_false_of_ne hne]
          · simp [beq_false_of_ne hu0]
        rw [h1, cardFin_beq_eq_one v1]
      omega
    rw [hsupp]
    by_cases hv0 : v.val = 0
    · have hvc0 : knMap n v = some ⟨0, by omega⟩ := by
        unfold knMap; simp [hv0]
      rw [hvc0] at hvc
      injection hvc with hc_eq
      rw [← hc_eq]
      have hsame : cardFin n (fun u =>
          (completeGraph n).inClosedNbr v u && (knMap n u == some ⟨0, by omega⟩)) = 1 := by
        have heq : cardFin n (fun u =>
            (completeGraph n).inClosedNbr v u && (knMap n u == some ⟨0, by omega⟩)) =
            cardFin n (fun u => u == v0) := by
          apply cardFin_congr
          intro u
          rw [hn_all u, Bool.true_and]
          unfold knMap
          by_cases hu0 : u.val = 0
          · have huv0 : u = v0 := Fin.ext hu0
            subst huv0; simp [v0]
          · have hne0 : u ≠ v0 := fun h => hu0 (congrArg Fin.val h)
            by_cases hu1 : u.val = 1 <;> simp [hu0, hu1, beq_false_of_ne hne0]
        rw [heq, cardFin_beq_eq_one v0]
      rw [hsame]
      omega
    · by_cases hv1 : v.val = 1
      · have hvc1 : knMap n v = some ⟨1, by omega⟩ := by
          unfold knMap; simp [hv1]
        rw [hvc1] at hvc
        injection hvc with hc_eq
        rw [← hc_eq]
        have hsame : cardFin n (fun u =>
            (completeGraph n).inClosedNbr v u && (knMap n u == some ⟨1, by omega⟩)) = 1 := by
          have heq : cardFin n (fun u =>
              (completeGraph n).inClosedNbr v u && (knMap n u == some ⟨1, by omega⟩)) =
              cardFin n (fun u => u == v1) := by
            apply cardFin_congr
            intro u
            rw [hn_all u, Bool.true_and]
            unfold knMap
            by_cases hu0 : u.val = 0
            · have huv0 : u = v0 := Fin.ext hu0
              subst huv0
              have hne : v0 ≠ v1 := by intro h; injection h with h'; omega
              simp [v0, beq_false_of_ne hne]
            · by_cases hu1 : u.val = 1
              · have huv1 : u = v1 := Fin.ext hu1
                subst huv1; simp [v1]
              · have hne1 : u ≠ v1 := fun h => hu1 (congrArg Fin.val h)
                simp [hu0, hu1, beq_false_of_ne hne1]
          rw [heq, cardFin_beq_eq_one v1]
        rw [hsame]
        omega
      · have hv_none : knMap n v = none := by
          unfold knMap; simp [hv0, hv1]
        rw [hv_none] at hvc
        cases hvc

/-- Explicit `n`-color sub-quorum coloring of `K_n.compl` (the edgeless graph on `n` vertices),
    assigning every vertex its own singleton color class. -/
def completeGraphComplColoring (n : Nat) :
    SubQuorumColoring (completeGraph n).compl n where
  f v := some v
  surj c := ⟨c, rfl⟩
  quorum v c hvc := by
    injection hvc with hvc'
    subst hvc'
    have hnbr : ∀ u : Fin n, (completeGraph n).compl.inClosedNbr v u = (u == v) := by
      intro u
      unfold SimpleGraph.inClosedNbr SimpleGraph.compl completeGraph
      cases v != u <;> simp
    have hsame : cardFin n (fun u =>
        (completeGraph n).compl.inClosedNbr v u && (some u == some v)) = 1 := by
      have heq : cardFin n (fun u =>
          (completeGraph n).compl.inClosedNbr v u && (some u == some v)) =
          cardFin n (fun u => u == v) := by
        apply cardFin_congr
        intro u
        rw [hnbr u]
        by_cases huv : u = v
        · subst huv; simp
        · simp [beq_false_of_ne huv]
      rw [heq, cardFin_beq_eq_one v]
    have hsupp : cardFin n (fun u =>
        (completeGraph n).compl.inClosedNbr v u && (some u).isSome) = 1 := by
      have heq : cardFin n (fun u =>
          (completeGraph n).compl.inClosedNbr v u && (some u).isSome) =
          cardFin n (fun u => u == v) := by
        apply cardFin_congr
        intro u
        simp [hnbr u]
      rw [heq, cardFin_beq_eq_one v]
    omega

/-- Sharpness of Conjecture 9.2 on `K_n` for every `n >= 2`:
    there exist a 2-color sub-quorum coloring of `K_n` and an `n`-color sub-quorum coloring
    of `K_n.compl`, attaining `2 + n = n + 2`. -/
theorem sharpness_Kn (n : Nat) (hn : n ≥ 2) :
    ∃ (_ : SubQuorumColoring (completeGraph n) 2)
      (_ : SubQuorumColoring (completeGraph n).compl n),
      2 + n = n + 2 :=
  ⟨completeGraphColoring n hn, completeGraphComplColoring n, Nat.add_comm 2 n⟩

/-- Optimality of `2` on `K_n` for `n >= 2` (`psi_sq(K_n) <= 2`). -/
theorem completeGraph_subquorum_le_two (n : Nat) (hn : n ≥ 2) (k : Nat)
    (col : SubQuorumColoring (completeGraph n) k) : k ≤ 2 := by
  have h := conjecture_9_2 n hn (completeGraph n) k n col (completeGraphComplColoring n)
  omega

/-- Optimality of `n` on `K_n.compl` for `n >= 2` (`psi_sq(K_n.compl) <= n`). -/
theorem completeGraph_compl_subquorum_le_n (n : Nat) (hn : n ≥ 2) (k : Nat)
    (col : SubQuorumColoring (completeGraph n).compl k) : k ≤ n := by
  have h := conjecture_9_2 n hn (completeGraph n) 2 k (completeGraphColoring n hn) col
  omega

/-! ## Section 8: Additional Tightness Witnesses (`P_3` for Lemma 3 and `S_{2,2}` for Theorem 1) -/

/-- The 3-vertex path `P_3` (`0 - 1 - 2`, with center `0` adjacent to leaves `1` and `2`). -/
def path3 : SimpleGraph 3 where
  adj u v :=
    (u.val == 0 && (v.val == 1 || v.val == 2)) ||
    (v.val == 0 && (u.val == 1 || u.val == 2))
  symm := by decide
  loopless := by decide

/-- Exact tightness of the `m + 5 / 2` constant in Lemma 3 (`handshaking_weight_bound`):
    on `P_3` (`m = 3`), `Sigma(P_3) = 3 + 5 / 2 = 11 / 2`. -/
theorem handshaking_weight_bound_sharp_P3 :
    sigma path3 = NNRat.ofNat 3 + NNRat.mk 5 2 (by omega) := by
  have hfr : List.finRange 3 = [⟨0, by omega⟩, ⟨1, by omega⟩, ⟨2, by omega⟩] := rfl
  unfold sigma
  rw [hfr]
  simp only [SubQuorumAux.qsum, NNRat.add_zero]
  have hd0 : path3.deg ⟨0, by omega⟩ = 2 := by decide
  have hd1 : path3.deg ⟨1, by omega⟩ = 1 := by decide
  have hd2 : path3.deg ⟨2, by omega⟩ = 1 := by decide
  rw [hd0, hd1, hd2]
  unfold sigmaTerm
  exact Quotient.sound rfl

/-- The 6-vertex double star `S_{2,2}` from Remark 1 and Remark 2 of PROOF.md:
    adjacent centers `0, 1`, leaves `2, 3` at `0`, and leaves `4, 5` at `1`. -/
def doubleStar22 : SimpleGraph 6 where
  adj u v :=
    (u.val == 0 && (v.val == 1 || v.val == 2 || v.val == 3)) ||
    (v.val == 0 && (u.val == 1 || u.val == 2 || u.val == 3)) ||
    (u.val == 1 && (v.val == 4 || v.val == 5)) ||
    (v.val == 1 && (u.val == 4 || u.val == 5))
  symm := by decide
  loopless := by decide

/-- Total 5-color sub-quorum coloring of `S_{2,2}` (`{0, 1}, {2}, {3}, {4}, {5}`),
    witnessing `psi_sq(S_{2,2}) >= 5 > beta_2(S_{2,2}) = 4`. -/
def doubleStar22Coloring : SubQuorumColoring doubleStar22 5 where
  f v :=
    match v.val with
    | 0 => some ⟨0, by omega⟩
    | 1 => some ⟨0, by omega⟩
    | 2 => some ⟨1, by omega⟩
    | 3 => some ⟨2, by omega⟩
    | 4 => some ⟨3, by omega⟩
    | _ => some ⟨4, by omega⟩
  surj := by decide
  quorum := by decide

/-- Partial 3-color sub-quorum coloring of `S_{2,2}.compl` with support `{0, 2, 3}`
    and singleton classes `{0}, {2}, {3}`, leaving `{1, 4, 5}` uncolored. -/
def doubleStar22ComplColoring : SubQuorumColoring doubleStar22.compl 3 where
  f v :=
    match v.val with
    | 0 => some ⟨0, by omega⟩
    | 2 => some ⟨1, by omega⟩
    | 3 => some ⟨2, by omega⟩
    | _ => none
  surj := by decide
  quorum := by decide

/-- Non-clique sharpness witness on `S_{2,2}` (`n = 6`): `5 + 3 = 6 + 2`. -/
theorem sharpness_S22 :
    ∃ (_ : SubQuorumColoring doubleStar22 5)
      (_ : SubQuorumColoring doubleStar22.compl 3),
      5 + 3 = 6 + 2 :=
  ⟨doubleStar22Coloring, doubleStar22ComplColoring, rfl⟩

/-- Negative control (`not_upper_bound_n_plus_one`): tightening `n + 2` to `n + 1` is false for
    every `n >= 2`, confirming both tightness of `n + 2` and non-vacuity of `SubQuorumColoring`. -/
theorem not_upper_bound_n_plus_one (n : Nat) (hn : n ≥ 2) :
    ¬ (∀ (G : SimpleGraph n) (k1 k2 : Nat),
        SubQuorumColoring G k1 → SubQuorumColoring G.compl k2 → k1 + k2 ≤ n + 1) := by
  intro h
  have hbad := h (completeGraph n) 2 n (completeGraphColoring n hn) (completeGraphComplColoring n)
  omega

/-- Negative control (`no_three_color_K3`): `K_3` has no 3-color sub-quorum coloring,
    confirming `SubQuorumColoring` enforces closed-neighborhood majority rather than proper coloring. -/
theorem no_three_color_K3 : ¬ Nonempty (SubQuorumColoring (completeGraph 3) 3) := by
  intro ⟨col⟩
  have h := completeGraph_subquorum_le_two 3 (by omega) 3 col
  omega


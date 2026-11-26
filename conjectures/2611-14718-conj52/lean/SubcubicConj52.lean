import Init.Data.Rat.Lemmas

/-
Standalone Lean 4.36.0 formalization of the
disproof of Conjecture 5.2 (conj:grado3) of Higuita-Diaz, Lopez, and Roldan-Correa
(arXiv:2611.14718v2): Random Sequential Adsorption versus the Uniform Ensemble of Jammed
Configurations: Stochastic Dominance on Graphs.
-/

namespace SubcubicConj52

open scoped Rat

/-! ## Section 1: Exact Non-Negative Rational Probabilities (`QProb`) -/

structure QProb where
  num : Nat
  den : Nat
  den_pos : 0 < den
  deriving Repr

namespace QProb

def zero : QProb := ⟨0, 1, Nat.one_pos⟩

def one : QProb := ⟨1, 1, Nat.one_pos⟩

def add (p q : QProb) : QProb :=
  ⟨p.num * q.den + q.num * p.den, p.den * q.den, Nat.mul_pos p.den_pos q.den_pos⟩

def scaleNat (k : Nat) (p : QProb) : QProb :=
  ⟨k * p.num, p.den, p.den_pos⟩

def divNat (p : QProb) (k : Nat) (hk : 0 < k) : QProb :=
  ⟨p.num, k * p.den, Nat.mul_pos hk p.den_pos⟩

/-- Exact rational equality cleared to cross-multiplied `Nat` arithmetic. -/
def Eq (p q : QProb) : Prop :=
  p.num * q.den = q.num * p.den

/-- Exact rational `≤` cleared to cross-multiplied `Nat` arithmetic. -/
def Le (p q : QProb) : Prop :=
  p.num * q.den ≤ q.num * p.den

/-- Exact rational `<` cleared to cross-multiplied `Nat` arithmetic. -/
def Lt (p q : QProb) : Prop :=
  p.num * q.den < q.num * p.den

theorem eq_refl (p : QProb) : Eq p p := rfl

theorem eq_symm {p q : QProb} (h : Eq p q) : Eq q p := _root_.Eq.symm h

theorem eq_trans {p q r : QProb} (h1 : Eq p q) (h2 : Eq q r) : Eq p r := by
  unfold Eq at *
  have hmul : (p.num * r.den) * q.den = (r.num * p.den) * q.den := by
    calc
      (p.num * r.den) * q.den = (p.num * q.den) * r.den := by
        rw [Nat.mul_assoc, Nat.mul_comm r.den q.den, ← Nat.mul_assoc]
      _ = (q.num * p.den) * r.den := by rw [h1]
      _ = (q.num * r.den) * p.den := by
        rw [Nat.mul_assoc, Nat.mul_comm p.den r.den, ← Nat.mul_assoc]
      _ = (r.num * q.den) * p.den := by rw [h2]
      _ = (r.num * p.den) * q.den := by
        rw [Nat.mul_assoc, Nat.mul_comm q.den p.den, ← Nat.mul_assoc]
  exact Nat.eq_of_mul_eq_mul_right q.den_pos hmul

theorem Le_congr {p1 p2 q1 q2 : QProb} (hp : Eq p1 p2) (hq : Eq q1 q2) (h : Le p1 q1) :
    Le p2 q2 := by
  unfold Eq Le at *
  have h1 : (p2.num * q2.den) * (p1.den * q1.den) ≤ (q2.num * p2.den) * (p1.den * q1.den) := by
    have lhs_eq : (p2.num * q2.den) * (p1.den * q1.den) = (p1.num * q1.den) * (p2.den * q2.den) := by
      calc
        (p2.num * q2.den) * (p1.den * q1.den)
            = (p2.num * p1.den) * (q2.den * q1.den) := by
              simp [Nat.mul_left_comm, Nat.mul_comm]
        _ = (p1.num * p2.den) * (q2.den * q1.den) := by rw [hp.symm]
        _ = (p1.num * q1.den) * (p2.den * q2.den) := by
              simp [Nat.mul_left_comm, Nat.mul_comm]
    have rhs_eq : (q2.num * p2.den) * (p1.den * q1.den) = (q1.num * p1.den) * (p2.den * q2.den) := by
      calc
        (q2.num * p2.den) * (p1.den * q1.den)
            = (q2.num * q1.den) * (p2.den * p1.den) := by
              simp [Nat.mul_left_comm, Nat.mul_comm]
        _ = (q1.num * q2.den) * (p2.den * p1.den) := by rw [hq.symm]
        _ = (q1.num * p1.den) * (p2.den * q2.den) := by
              simp [Nat.mul_left_comm, Nat.mul_comm]
    rw [lhs_eq, rhs_eq]
    exact Nat.mul_le_mul_right (p2.den * q2.den) h
  exact Nat.le_of_mul_le_mul_right h1 (Nat.mul_pos p1.den_pos q1.den_pos)

theorem Lt_congr {p1 p2 q1 q2 : QProb} (hp : Eq p1 p2) (hq : Eq q1 q2) (h : Lt p1 q1) :
    Lt p2 q2 := by
  unfold Eq Lt at *
  have h1 : (p2.num * q2.den) * (p1.den * q1.den) < (q2.num * p2.den) * (p1.den * q1.den) := by
    have lhs_eq : (p2.num * q2.den) * (p1.den * q1.den) = (p1.num * q1.den) * (p2.den * q2.den) := by
      calc
        (p2.num * q2.den) * (p1.den * q1.den)
            = (p2.num * p1.den) * (q2.den * q1.den) := by
              simp [Nat.mul_left_comm, Nat.mul_comm]
        _ = (p1.num * p2.den) * (q2.den * q1.den) := by rw [hp.symm]
        _ = (p1.num * q1.den) * (p2.den * q2.den) := by
              simp [Nat.mul_left_comm, Nat.mul_comm]
    have rhs_eq : (q2.num * p2.den) * (p1.den * q1.den) = (q1.num * p1.den) * (p2.den * q2.den) := by
      calc
        (q2.num * p2.den) * (p1.den * q1.den)
            = (q2.num * q1.den) * (p2.den * p1.den) := by
              simp [Nat.mul_left_comm, Nat.mul_comm]
        _ = (q1.num * q2.den) * (p2.den * p1.den) := by rw [hq.symm]
        _ = (q1.num * p1.den) * (p2.den * q2.den) := by
              simp [Nat.mul_left_comm, Nat.mul_comm]
    rw [lhs_eq, rhs_eq]
    exact Nat.mul_lt_mul_of_pos_right h (Nat.mul_pos p2.den_pos q2.den_pos)
  exact Nat.lt_of_mul_lt_mul_right h1

theorem not_Le_of_Lt {p q : QProb} (h : Lt q p) : ¬ Le p q := by
  unfold Lt Le at *
  omega

theorem Eq_zero_iff {p : QProb} : Eq p zero ↔ p.num = 0 := by
  unfold Eq zero
  simp

theorem Eq_one_iff {p : QProb} : Eq p one ↔ p.num = p.den := by
  unfold Eq one
  simp

theorem add_congr {p1 p2 q1 q2 : QProb} (hp : Eq p1 p2) (hq : Eq q1 q2) :
    Eq (add p1 q1) (add p2 q2) := by
  unfold Eq add at *
  calc
    (p1.num * q1.den + q1.num * p1.den) * (p2.den * q2.den)
        = (p1.num * p2.den) * (q1.den * q2.den) + (q1.num * q2.den) * (p1.den * p2.den) := by
          rw [Nat.add_mul]
          simp [Nat.mul_left_comm, Nat.mul_comm]
    _ = (p2.num * p1.den) * (q1.den * q2.den) + (q2.num * q1.den) * (p1.den * p2.den) := by
          rw [hp, hq]
    _ = (p2.num * q2.den + q2.num * p2.den) * (p1.den * q1.den) := by
          rw [Nat.add_mul]
          simp [Nat.mul_left_comm, Nat.mul_comm]

theorem add_zero_right (p : QProb) : Eq (add p zero) p := by
  unfold Eq add zero
  simp

theorem add_zero_left (p : QProb) : Eq (add zero p) p := by
  unfold Eq add zero
  simp

theorem add_comm_eq (p q : QProb) : Eq (add p q) (add q p) := by
  unfold Eq add
  simp [Nat.add_comm, Nat.mul_comm]

theorem add_assoc_eq (p q r : QProb) : Eq (add (add p q) r) (add p (add q r)) := by
  unfold Eq add
  simp [Nat.mul_add, Nat.add_assoc, Nat.mul_left_comm, Nat.mul_comm]

theorem divNat_congr {p1 p2 : QProb} {k : Nat} (hk : 0 < k) (hp : Eq p1 p2) :
    Eq (divNat p1 k hk) (divNat p2 k hk) := by
  unfold Eq divNat at *
  calc
    p1.num * (k * p2.den) = k * (p1.num * p2.den) := by
      simp [Nat.mul_left_comm]
    _ = k * (p2.num * p1.den) := by rw [hp]
    _ = p2.num * (k * p1.den) := by
      simp [Nat.mul_left_comm]

theorem scaleNat_zero (p : QProb) : Eq (scaleNat 0 p) zero := by
  unfold Eq scaleNat zero
  simp

theorem scaleNat_one (p : QProb) : Eq (scaleNat 1 p) p := by
  unfold Eq scaleNat
  simp

theorem scaleNat_add (a b : Nat) (p : QProb) :
    Eq (add (scaleNat a p) (scaleNat b p)) (scaleNat (a + b) p) := by
  unfold Eq add scaleNat
  rw [Nat.add_mul, Nat.add_mul, Nat.add_mul]
  simp [Nat.mul_left_comm, Nat.mul_comm]

theorem divNat_scaleNat_self (k : Nat) (hk : 0 < k) (p : QProb) :
    Eq (divNat (scaleNat k p) k hk) p := by
  unfold Eq divNat scaleNat
  simp [Nat.mul_left_comm, Nat.mul_comm]

def listSum : List QProb → QProb
  | [] => zero
  | x :: xs => add x (listSum xs)

theorem listSum_append (l1 l2 : List QProb) :
    Eq (listSum (l1 ++ l2)) (add (listSum l1) (listSum l2)) := by
  induction l1 with
  | nil =>
    simpa [listSum] using eq_symm (add_zero_left (listSum l2))
  | cons x xs ih =>
    simp only [List.cons_append, listSum]
    exact eq_trans (add_congr (eq_refl x) ih) (eq_symm (add_assoc_eq x (listSum xs) (listSum l2)))

end QProb

/-! ## Section 2: Finite Index Lists, Nodup Counting, and Subsets (`Fin n → Bool`) -/

theorem nodup_map_of_injOn {α β : Type} {f : α → β} {l : List α}
    (hl : l.Nodup) (hinj : ∀ a ∈ l, ∀ b ∈ l, f a = f b → a = b) :
    (l.map f).Nodup := by
  induction l with
  | nil => exact List.Pairwise.nil
  | cons x xs ih =>
    cases hl with
    | cons hx_ne hxs =>
      simp only [List.map_cons]
      apply List.Pairwise.cons
      · intro y hy
        rw [List.mem_map] at hy
        rcases hy with ⟨z, hz, rfl⟩
        intro hfxz
        have hxz := hinj x List.mem_cons_self z (List.mem_cons_of_mem x hz) hfxz
        exact hx_ne z hz hxz
      · exact ih hxs (fun a ha b hb h =>
          hinj a (List.mem_cons_of_mem x ha) b (List.mem_cons_of_mem x hb) h)

theorem nodup_get_inj {α : Type} {l : List α} (hl : l.Nodup)
    {i j : Fin l.length} (h : l.get i = l.get j) : i = j := by
  induction l with
  | nil => exact Fin.elim0 i
  | cons x xs ih =>
    cases hl with
    | cons hx_ne hxs =>
      rcases i with ⟨iv, hi⟩
      rcases j with ⟨jv, hj⟩
      cases iv with
      | zero =>
        cases jv with
        | zero => rfl
        | succ jv' =>
          exfalso
          have hmem : xs.get ⟨jv', Nat.lt_of_succ_lt_succ hj⟩ ∈ xs :=
            List.get_mem xs ⟨jv', Nat.lt_of_succ_lt_succ hj⟩
          exact hx_ne _ hmem h
      | succ iv' =>
        cases jv with
        | zero =>
          exfalso
          have hmem : xs.get ⟨iv', Nat.lt_of_succ_lt_succ hi⟩ ∈ xs :=
            List.get_mem xs ⟨iv', Nat.lt_of_succ_lt_succ hi⟩
          exact hx_ne _ hmem h.symm
        | succ jv' =>
          have hij := ih hxs (i := ⟨iv', Nat.lt_of_succ_lt_succ hi⟩)
            (j := ⟨jv', Nat.lt_of_succ_lt_succ hj⟩) h
          exact Fin.ext (congrArg Nat.succ (congrArg Fin.val hij))

def idxOfMem {α : Type} [DecidableEq α] : (l : List α) → (x : α) → x ∈ l → Fin l.length
  | [], _, hx => nomatch hx
  | a :: as, x, hx =>
    if hax : x = a then
      ⟨0, Nat.succ_pos _⟩
    else
      have hx' : x ∈ as := by
        cases hx with
        | head => exact absurd rfl hax
        | tail _ hm => exact hm
      (idxOfMem as x hx').succ

theorem get_idxOfMem {α : Type} [DecidableEq α] (l : List α) (x : α) (hx : x ∈ l) :
    l.get (idxOfMem l x hx) = x := by
  induction l with
  | nil => cases hx
  | cons a as ih =>
    dsimp [idxOfMem]
    split
    · next hax => exact hax.symm
    · exact ih _

def finRange : (n : Nat) → List (Fin n)
  | 0 => []
  | n + 1 => ⟨0, Nat.succ_pos n⟩ :: (finRange n).map Fin.succ

theorem length_finRange (n : Nat) : (finRange n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [finRange, ih]

theorem mem_finRange {n : Nat} (i : Fin n) : i ∈ finRange n := by
  induction n with
  | zero => exact Fin.elim0 i
  | succ n ih =>
    rcases i with ⟨val, isLt⟩
    cases val with
    | zero =>
      simp [finRange]
    | succ k =>
      simp only [finRange, List.mem_cons, List.mem_map]
      right
      refine ⟨⟨k, Nat.lt_of_succ_lt_succ isLt⟩, ih _, rfl⟩

theorem nodup_finRange (n : Nat) : (finRange n).Nodup := by
  induction n with
  | zero => exact List.Pairwise.nil
  | succ n ih =>
    simp only [finRange]
    apply List.Pairwise.cons
    · intro x hx
      rw [List.mem_map] at hx
      rcases hx with ⟨y, _, rfl⟩
      intro h
      cases h
    · exact nodup_map_of_injOn ih (fun _ _ _ _ hab => Fin.succ_inj.mp hab)

theorem nodup_filter {α : Type} (p : α → Bool) {l : List α} (h : l.Nodup) :
    (l.filter p).Nodup :=
  List.Pairwise.filter p h

theorem length_erase_of_mem {α : Type} [DecidableEq α] {a : α} {l : List α} (h : a ∈ l) :
    (l.erase a).length + 1 = l.length := by
  induction l with
  | nil => cases h
  | cons b bs ih =>
    simp only [List.erase_cons]
    cases hba : (b == a) with
    | true => simp
    | false =>
      simp only [Bool.false_eq_true, ↓reduceIte]
      have ha : a ∈ bs := by
        cases h with
        | head =>
          rw [beq_self_eq_true] at hba
          cases hba
        | tail _ hmem => exact hmem
      simpa [List.length_cons] using congrArg Nat.succ (ih ha)

theorem mem_erase_of_ne_of_mem {α : Type} [DecidableEq α] {a b : α} {l : List α}
    (hab : a ≠ b) (ha : a ∈ l) : a ∈ l.erase b := by
  induction l with
  | nil => cases ha
  | cons c cs ih =>
    simp only [List.erase_cons]
    cases hcb : (c == b) with
    | true =>
      have hceq : c = b := beq_iff_eq.mp hcb
      simp only [↓reduceIte]
      cases ha with
      | head => exact absurd hceq hab
      | tail _ hmem => exact hmem
    | false =>
      simp only [Bool.false_eq_true, ↓reduceIte, List.mem_cons]
      cases ha with
      | head => exact Or.inl rfl
      | tail _ hmem => exact Or.inr (ih hmem)

/-- Fundamental finite bijection/subset cardinality lemma for duplicate-free lists. -/
theorem length_le_of_nodup_subset {α : Type} [DecidableEq α] {l1 l2 : List α}
    (h1 : l1.Nodup) (hsub : ∀ x, x ∈ l1 → x ∈ l2) : l1.length ≤ l2.length := by
  induction l1 generalizing l2 with
  | nil => exact Nat.zero_le _
  | cons a t ih =>
    cases h1 with
    | cons ha_ne ht_nodup =>
      have ha_l2 : a ∈ l2 := hsub a List.mem_cons_self
      have hlen_erase : (l2.erase a).length + 1 = l2.length := length_erase_of_mem ha_l2
      have ht_sub : ∀ x, x ∈ t → x ∈ l2.erase a := by
        intro x hx
        have hne : x ≠ a := (ha_ne x hx).symm
        exact mem_erase_of_ne_of_mem hne (hsub x (List.mem_cons_of_mem a hx))
      have hle : t.length ≤ (l2.erase a).length := ih ht_nodup ht_sub
      simp only [List.length_cons]
      omega

theorem length_eq_of_nodup_iff {α : Type} [DecidableEq α] {l1 l2 : List α}
    (h1 : l1.Nodup) (h2 : l2.Nodup) (hiff : ∀ x, x ∈ l1 ↔ x ∈ l2) :
    l1.length = l2.length :=
  Nat.le_antisymm
    (length_le_of_nodup_subset h1 (fun x hx => (hiff x).mp hx))
    (length_le_of_nodup_subset h2 (fun x hx => (hiff x).mpr hx))

theorem length_filter_lt_of_false {α : Type} (p : α → Bool) {l : List α} {x : α}
    (hx : x ∈ l) (hpx : p x = false) : (l.filter p).length < l.length := by
  induction l with
  | nil => cases hx
  | cons a as ih =>
    cases hx with
    | head =>
      simp only [List.filter_cons, hpx, Bool.false_eq_true, ↓reduceIte, List.length_cons]
      exact Nat.lt_succ_of_le (List.length_filter_le p as)
    | tail _ hmem =>
      have hlt : (as.filter p).length < as.length := ih hmem
      cases hpa : p a with
      | false =>
        simp only [List.filter_cons, hpa, Bool.false_eq_true, ↓reduceIte, List.length_cons]
        omega
      | true =>
        simp only [List.filter_cons, hpa, ↓reduceIte, List.length_cons]
        omega

def finSum (n : Nat) (f : Fin n → QProb) : QProb :=
  QProb.listSum ((finRange n).map f)

theorem listSum_map_congr {α : Type} (l : List α) {f g : α → QProb}
    (h : ∀ x ∈ l, QProb.Eq (f x) (g x)) :
    QProb.Eq (QProb.listSum (l.map f)) (QProb.listSum (l.map g)) := by
  induction l with
  | nil => exact QProb.eq_refl _
  | cons a as ih =>
    simp only [List.map_cons, QProb.listSum]
    exact QProb.add_congr (h a List.mem_cons_self)
      (ih (fun x hx => h x (List.mem_cons_of_mem a hx)))

theorem listSum_map_zero {α : Type} (l : List α) {f : α → QProb}
    (h : ∀ x ∈ l, QProb.Eq (f x) QProb.zero) :
    QProb.Eq (QProb.listSum (l.map f)) QProb.zero := by
  induction l with
  | nil => exact QProb.eq_refl _
  | cons a as ih =>
    simp only [List.map_cons, QProb.listSum]
    exact QProb.eq_trans
      (QProb.add_congr (h a List.mem_cons_self)
        (ih (fun x hx => h x (List.mem_cons_of_mem a hx))))
      (QProb.add_zero_left QProb.zero)

theorem listSum_map_const {α : Type} (l : List α) (c : QProb) :
    QProb.Eq (QProb.listSum (l.map (fun _ => c))) (QProb.scaleNat l.length c) := by
  induction l with
  | nil =>
    simpa [QProb.listSum] using QProb.eq_symm (QProb.scaleNat_zero c)
  | cons a as ih =>
    simp only [List.map_cons, QProb.listSum, List.length_cons]
    have h1 : QProb.Eq (QProb.add c (QProb.listSum (as.map (fun _ => c))))
        (QProb.add (QProb.scaleNat 1 c) (QProb.scaleNat as.length c)) :=
      QProb.add_congr (QProb.eq_symm (QProb.scaleNat_one c)) ih
    have h2 := QProb.scaleNat_add 1 as.length c
    rw [Nat.add_comm 1 as.length] at h2
    exact QProb.eq_trans h1 h2

/-- Reindexing a `QProb` sum along a bijection between duplicate-free lists. -/
theorem listSum_perm_bij {α β : Type} [DecidableEq β]
    (l1 : List α) (l2 : List β) (e : α → β) (f : α → QProb) (g : β → QProb)
    (h1 : l1.Nodup) (h2 : l2.Nodup)
    (he_inj : ∀ a1 ∈ l1, ∀ a2 ∈ l1, e a1 = e a2 → a1 = a2)
    (he_mem : ∀ b, b ∈ l2 ↔ ∃ a ∈ l1, e a = b)
    (hfg : ∀ a ∈ l1, QProb.Eq (f a) (g (e a))) :
    QProb.Eq (QProb.listSum (l1.map f)) (QProb.listSum (l2.map g)) := by
  have listSum_erase : ∀ (b : β) (l : List β), b ∈ l →
      QProb.Eq (QProb.listSum (l.map g)) (QProb.add (g b) (QProb.listSum ((l.erase b).map g))) := by
    intro b l hmem
    induction l with
    | nil => cases hmem
    | cons c cs ih_l =>
      simp only [List.erase_cons, List.map_cons, QProb.listSum]
      cases hcb : (c == b) with
      | true =>
        have hceq : c = b := beq_iff_eq.mp hcb
        subst hceq
        simp only [↓reduceIte]
        exact QProb.eq_refl _
      | false =>
        simp only [Bool.false_eq_true, ↓reduceIte, List.map_cons, QProb.listSum]
        have hb_cs : b ∈ cs := by
          cases hmem with
          | head =>
            rw [beq_self_eq_true] at hcb
            cases hcb
          | tail _ hm => exact hm
        have step1 := QProb.add_congr (QProb.eq_refl (g c)) (ih_l hb_cs)
        have step2 := QProb.eq_symm (QProb.add_assoc_eq (g c) (g b) (QProb.listSum ((cs.erase b).map g)))
        have step3 := QProb.add_congr (QProb.add_comm_eq (g c) (g b))
          (QProb.eq_refl (QProb.listSum ((cs.erase b).map g)))
        have step4 := QProb.add_assoc_eq (g b) (g c) (QProb.listSum ((cs.erase b).map g))
        exact QProb.eq_trans step1 (QProb.eq_trans step2 (QProb.eq_trans step3 step4))
  induction l1 generalizing l2 with
  | nil =>
    cases l2 with
    | nil => exact QProb.eq_refl _
    | cons b bs =>
      rcases (he_mem b).mp List.mem_cons_self with ⟨a, ha, _⟩
      cases ha
  | cons a as ih =>
    cases h1 with
    | cons ha_ne has_nodup =>
      have hea_mem : e a ∈ l2 := (he_mem (e a)).mpr ⟨a, List.mem_cons_self, rfl⟩
      have h2_erase_nodup : (l2.erase (e a)).Nodup := List.Pairwise.erase (e a) h2
      have he_mem_erase : ∀ b, b ∈ l2.erase (e a) ↔ ∃ x ∈ as, e x = b := by
        intro b
        constructor
        · intro hb
          have hb_l2 : b ∈ l2 := List.mem_of_mem_erase hb
          rcases (he_mem b).mp hb_l2 with ⟨x, hx_cons, rfl⟩
          cases hx_cons with
          | head =>
            exfalso
            exact (List.Nodup.not_mem_erase h2) hb
          | tail _ hx_as => exact ⟨x, hx_as, rfl⟩
        · rintro ⟨x, hx_as, rfl⟩
          have hne : e x ≠ e a := by
            intro heq
            have hxa := he_inj x (List.mem_cons_of_mem a hx_as) a List.mem_cons_self heq
            exact ha_ne x hx_as hxa.symm
          exact mem_erase_of_ne_of_mem hne ((he_mem (e x)).mpr ⟨x, List.mem_cons_of_mem a hx_as, rfl⟩)
      have ih_res := ih (l2.erase (e a)) has_nodup h2_erase_nodup
        (fun x1 hx1 x2 hx2 h => he_inj x1 (List.mem_cons_of_mem a hx1) x2 (List.mem_cons_of_mem a hx2) h)
        he_mem_erase
        (fun x hx => hfg x (List.mem_cons_of_mem a hx))
      simp only [List.map_cons, QProb.listSum]
      have stepA := QProb.add_congr (hfg a List.mem_cons_self) ih_res
      exact QProb.eq_trans stepA (QProb.eq_symm (listSum_erase (e a) l2 hea_mem))

/-- Decidable equality on vertex subsets `Fin n → Bool`. -/
def setEqB {n : Nat} (S1 S2 : Fin n → Bool) : Bool :=
  (finRange n).all (fun i => S1 i == S2 i)

theorem setEqB_eq_true_iff {n : Nat} {S1 S2 : Fin n → Bool} :
    setEqB S1 S2 = true ↔ S1 = S2 := by
  unfold setEqB
  rw [List.all_eq_true]
  constructor
  · intro h
    funext i
    exact beq_iff_eq.mp (h i (mem_finRange i))
  · intro h i _
    subst h
    exact beq_self_eq_true _

instance instDecidableEqFinSet (n : Nat) : DecidableEq (Fin n → Bool) :=
  fun S1 S2 =>
    if h : setEqB S1 S2 = true then
      isTrue (setEqB_eq_true_iff.mp h)
    else
      isFalse (fun heq => h (setEqB_eq_true_iff.mpr heq))

def setSize {n : Nat} (S : Fin n → Bool) : Nat :=
  ((finRange n).filter S).length

def extendSet {n : Nat} (b : Bool) (S : Fin n → Bool) (i : Fin (n + 1)) : Bool :=
  if h : i.val < n then S ⟨i.val, h⟩ else b

def restrictSet {n : Nat} (S : Fin (n + 1) → Bool) (i : Fin n) : Bool :=
  S ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩

theorem restrict_extendSet {n : Nat} (b : Bool) (S : Fin n → Bool) :
    restrictSet (extendSet b S) = S := by
  funext i
  simp [restrictSet, extendSet, i.isLt]

theorem extendSet_last {n : Nat} (b : Bool) (S : Fin n → Bool) :
    extendSet b S ⟨n, Nat.lt_succ_self n⟩ = b := by
  simp [extendSet]

theorem extendSet_restrict {n : Nat} (S : Fin (n + 1) → Bool) :
    extendSet (S ⟨n, Nat.lt_succ_self n⟩) (restrictSet S) = S := by
  funext i
  rcases i with ⟨v, hv⟩
  by_cases hlt : v < n
  · simp [extendSet, restrictSet, hlt]
  · have hveq : v = n := by omega
    subst hveq
    simp [extendSet]

def allSubsets : (n : Nat) → List (Fin n → Bool)
  | 0 => [fun i => Fin.elim0 i]
  | n + 1 => (allSubsets n).map (extendSet false) ++ (allSubsets n).map (extendSet true)

theorem mem_allSubsets {n : Nat} (S : Fin n → Bool) : S ∈ allSubsets n := by
  induction n with
  | zero =>
    simp only [allSubsets, List.mem_singleton]
    funext i
    exact Fin.elim0 i
  | succ n ih =>
    simp only [allSubsets, List.mem_append, List.mem_map]
    cases hb : S ⟨n, Nat.lt_succ_self n⟩ with
    | false =>
      left
      refine ⟨restrictSet S, ih _, ?_⟩
      simpa [hb] using extendSet_restrict S
    | true =>
      right
      refine ⟨restrictSet S, ih _, ?_⟩
      simpa [hb] using extendSet_restrict S

theorem nodup_allSubsets (n : Nat) : (allSubsets n).Nodup := by
  induction n with
  | zero =>
    simp [allSubsets]
  | succ n ih =>
    simp only [allSubsets]
    have hmap (b : Bool) : ((allSubsets n).map (extendSet b)).Nodup := by
      apply nodup_map_of_injOn ih
      intro S1 _ S2 _ heq
      have h := congrArg restrictSet heq
      simpa [restrict_extendSet] using h
    rw [List.nodup_append]
    refine ⟨hmap false, hmap true, ?_⟩
    intro x hx1 y hy2 hxy
    subst hxy
    rw [List.mem_map] at hx1 hy2
    rcases hx1 with ⟨S1, _, rfl⟩
    rcases hy2 with ⟨S2, _, heq⟩
    have hlast := congrFun heq ⟨n, Nat.lt_succ_self n⟩
    simp [extendSet_last] at hlast

/-! ## Section 3: Finite Simple Graphs, Degrees, Walks, and Trees -/

structure SimpleGraph (n : Nat) where
  adj : Fin n → Fin n → Bool
  symm : ∀ u v : Fin n, adj u v = adj v u
  loopless : ∀ v : Fin n, adj v v = false

def SimpleGraph.degree {n : Nat} (G : SimpleGraph n) (v : Fin n) : Nat :=
  ((finRange n).filter (fun u => G.adj v u)).length

def maxDegreeLe3 {n : Nat} (G : SimpleGraph n) : Prop :=
  ∀ v : Fin n, G.degree v ≤ 3

def numEdges {n : Nat} (G : SimpleGraph n) : Nat :=
  ((finRange n).foldl
    (fun acc u => acc + ((finRange n).filter (fun v => decide (u.val < v.val) && G.adj u v)).length)
    0)

inductive Walk {n : Nat} (G : SimpleGraph n) : Fin n → Fin n → Prop where
  | nil (u : Fin n) : Walk G u u
  | cons {u v w : Fin n} : G.adj u v = true → Walk G v w → Walk G u w

theorem Walk.trans {n : Nat} {G : SimpleGraph n} {u v w : Fin n}
    (h1 : Walk G u v) (h2 : Walk G v w) : Walk G u w := by
  induction h1 with
  | nil => exact h2
  | cons hadj _ ih => exact Walk.cons hadj (ih h2)

theorem Walk.symm {n : Nat} {G : SimpleGraph n} {u v : Fin n}
    (h : Walk G u v) : Walk G v u := by
  induction h with
  | nil u0 => exact Walk.nil u0
  | @cons a b c hadj _ ih =>
    have hadj' : G.adj b a = true := by rw [G.symm]; exact hadj
    exact Walk.trans ih (Walk.cons hadj' (Walk.nil a))

def Connected {n : Nat} (G : SimpleGraph n) : Prop :=
  0 < n ∧ ∀ u v : Fin n, Walk G u v

/-- A simple cycle in `G` is a duplicate-free vertex list `[v_0, ..., v_{k-1}]` of length `≥ 3`
where consecutive vertices and `(v_{k-1}, v_0)` are adjacent in `G`. -/
def IsSimpleCycle {n : Nat} (G : SimpleGraph n) (c : List (Fin n)) : Prop :=
  3 ≤ c.length ∧ c.Nodup ∧
  ∀ i : Fin c.length,
    G.adj (c.get i) (c.get ⟨(i.val + 1) % c.length, Nat.mod_lt _ (Nat.zero_lt_of_lt i.isLt)⟩) = true

def Acyclic {n : Nat} (G : SimpleGraph n) : Prop :=
  ∀ c : List (Fin n), ¬ IsSimpleCycle G c

/-- Standard graph-theoretic tree definition: non-empty connected acyclic simple graph. -/
def IsTree {n : Nat} (G : SimpleGraph n) : Prop :=
  Connected G ∧ Acyclic G

/-- General rooted-tree criterion: if `G` admits a root, parent map, and depth map such that
every edge connects a non-root vertex to its parent of depth one less, then `G` is a tree. -/
theorem isTree_of_rootedParent {n : Nat} (G : SimpleGraph n)
    (root : Fin n) (parent : Fin n → Fin n) (depth : Fin n → Nat)
    (_hroot : depth root = 0)
    (hstep : ∀ v : Fin n, v ≠ root → G.adj v (parent v) = true ∧ depth v = depth (parent v) + 1)
    (hedge : ∀ u v : Fin n, G.adj u v = true →
      (u ≠ root ∧ v = parent u ∧ depth u = depth v + 1) ∨
      (v ≠ root ∧ u = parent v ∧ depth v = depth u + 1)) :
    IsTree G := by
  have hn : 0 < n := Nat.zero_lt_of_lt root.isLt
  have walk_to_root : ∀ d : Nat, ∀ v : Fin n, depth v ≤ d → Walk G v root := by
    intro d
    induction d with
    | zero =>
      intro v hv
      by_cases hvr : v = root
      · subst hvr; exact Walk.nil _
      · have ⟨_, hd⟩ := hstep v hvr
        omega
    | succ d ih =>
      intro v hv
      by_cases hvr : v = root
      · subst hvr; exact Walk.nil _
      · have ⟨hadj, hd⟩ := hstep v hvr
        exact Walk.cons hadj (ih (parent v) (by omega))
  have hconn : Connected G := by
    refine ⟨hn, fun u v => ?_⟩
    exact Walk.trans (walk_to_root (depth u) u (Nat.le_refl _))
      (Walk.symm (walk_to_root (depth v) v (Nat.le_refl _)))
  have hacyc : Acyclic G := by
    intro c ⟨hlen, hnodup, hcyc⟩
    have hc_pos : 0 < c.length := by omega
    have hex_max : ∃ i : Fin c.length, ∀ j : Fin c.length, depth (c.get j) ≤ depth (c.get i) := by
      have aux : ∀ (l : List (Fin c.length)), l ≠ [] →
          ∃ i ∈ l, ∀ j ∈ l, depth (c.get j) ≤ depth (c.get i) := by
        intro l hl
        induction l with
        | nil => contradiction
        | cons x xs ih =>
          cases xs with
          | nil =>
            refine ⟨x, List.mem_singleton.mpr rfl, ?_⟩
            intro j hj
            rw [List.mem_singleton.mp hj]
            exact Nat.le_refl _
          | cons y ys =>
            rcases ih (List.cons_ne_nil y ys) with ⟨m, hm_mem, hm_max⟩
            by_cases hxm : depth (c.get m) ≤ depth (c.get x)
            · refine ⟨x, List.mem_cons_self, ?_⟩
              intro j hj
              cases hj with
              | head => exact Nat.le_refl _
              | tail _ hj' => exact Nat.le_trans (hm_max j hj') hxm
            · refine ⟨m, List.mem_cons_of_mem x hm_mem, ?_⟩
              intro j hj
              cases hj with
              | head => omega
              | tail _ hj' => exact hm_max j hj'
      have hne : finRange c.length ≠ [] := by
        intro hemp
        have hlen0 : (finRange c.length).length = 0 := by rw [hemp]; rfl
        rw [length_finRange] at hlen0
        omega
      rcases aux (finRange c.length) hne with ⟨i, _, hi⟩
      exact ⟨i, fun j => hi j (mem_finRange j)⟩
    rcases hex_max with ⟨i, hi_max⟩
    let nextIdx : Fin c.length := ⟨(i.val + 1) % c.length, Nat.mod_lt _ hc_pos⟩
    let prevIdx : Fin c.length := ⟨(i.val + c.length - 1) % c.length, Nat.mod_lt _ hc_pos⟩
    have hprev_next : (prevIdx.val + 1) % c.length = i.val := by
      dsimp [prevIdx]
      have hi_lt : i.val < c.length := i.isLt
      by_cases hi0 : i.val = 0
      · rw [hi0, Nat.zero_add, Nat.mod_eq_of_lt (by omega : c.length - 1 < c.length)]
        have hsum : c.length - 1 + 1 = c.length := by omega
        rw [hsum, Nat.mod_self]
      · have hrew : i.val + c.length - 1 = c.length + (i.val - 1) := by omega
        rw [hrew, Nat.add_comm c.length, Nat.add_mod_right,
            Nat.mod_eq_of_lt (by omega : i.val - 1 < c.length)]
        have hsum : i.val - 1 + 1 = i.val := by omega
        rw [hsum, Nat.mod_eq_of_lt hi_lt]
    have hadj_next : G.adj (c.get i) (c.get nextIdx) = true := hcyc i
    have hadj_prev' : G.adj (c.get prevIdx) (c.get i) = true := by
      have h := hcyc prevIdx
      have heqIdx : (⟨(prevIdx.val + 1) % c.length, Nat.mod_lt _ (Nat.zero_lt_of_lt prevIdx.isLt)⟩ : Fin c.length) = i :=
        Fin.ext hprev_next
      simpa [heqIdx] using h
    have hadj_prev : G.adj (c.get i) (c.get prevIdx) = true := by
      rw [G.symm]; exact hadj_prev'
    have hparent_next : c.get nextIdx = parent (c.get i) := by
      rcases hedge (c.get i) (c.get nextIdx) hadj_next with ⟨_, hp, _⟩ | ⟨_, _, hd⟩
      · exact hp
      · have hle := hi_max nextIdx
        omega
    have hparent_prev : c.get prevIdx = parent (c.get i) := by
      rcases hedge (c.get i) (c.get prevIdx) hadj_prev with ⟨_, hp, _⟩ | ⟨_, _, hd⟩
      · exact hp
      · have hle := hi_max prevIdx
        omega
    have hget_eq : c.get nextIdx = c.get prevIdx := hparent_next.trans hparent_prev.symm
    have hidx_eq : nextIdx = prevIdx := nodup_get_inj hnodup hget_eq
    have hval_eq : (i.val + 1) % c.length = (i.val + c.length - 1) % c.length :=
      congrArg Fin.val hidx_eq
    have hi_lt : i.val < c.length := i.isLt
    by_cases hi0 : i.val = 0
    · simp only [hi0, Nat.zero_add] at hval_eq
      rw [Nat.mod_eq_of_lt (by omega : 1 < c.length),
          Nat.mod_eq_of_lt (by omega : c.length - 1 < c.length)] at hval_eq
      omega
    · by_cases hitop : i.val + 1 = c.length
      · have h1 : (i.val + 1) % c.length = 0 := by rw [hitop, Nat.mod_self]
        have h2 : (i.val + c.length - 1) % c.length = i.val - 1 := by
          have hrew : i.val + c.length - 1 = c.length + (i.val - 1) := by omega
          rw [hrew, Nat.add_comm c.length, Nat.add_mod_right, Nat.mod_eq_of_lt (by omega)]
        rw [h1, h2] at hval_eq
        omega
      · have h1 : (i.val + 1) % c.length = i.val + 1 := Nat.mod_eq_of_lt (by omega)
        have h2 : (i.val + c.length - 1) % c.length = i.val - 1 := by
          have hrew : i.val + c.length - 1 = c.length + (i.val - 1) := by omega
          rw [hrew, Nat.add_comm c.length, Nat.add_mod_right, Nat.mod_eq_of_lt (by omega)]
        rw [h1, h2] at hval_eq
        omega
  exact ⟨hconn, hacyc⟩

/-! ## Section 4: Independent Sets, Maximal Independent Sets, and Static Model (`Nstat`) -/

def IsIndepSet {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) : Prop :=
  ∀ u v : Fin n, S u = true → S v = true → G.adj u v = false

/-- Standard inclusion-maximality definition of a maximal independent set (MIS). -/
def IsMaximalIndepSet {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) : Prop :=
  IsIndepSet G S ∧
  ∀ S' : Fin n → Bool, IsIndepSet G S' → (∀ u : Fin n, S u = true → S' u = true) → S' = S

/-- Domination characterization: `S` is independent and every vertex is in `S` or adjacent to `S`. -/
def IsDominatingIndepSet {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) : Prop :=
  IsIndepSet G S ∧
  ∀ v : Fin n, S v = true ∨ ∃ u : Fin n, S u = true ∧ G.adj v u = true

theorem isMaximalIndepSet_iff_dominating {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) :
    IsMaximalIndepSet G S ↔ IsDominatingIndepSet G S := by
  constructor
  · rintro ⟨hindep, hmax⟩
    refine ⟨hindep, fun v => ?_⟩
    cases hsv : S v with
    | true => exact Or.inl rfl
    | false =>
      right
      by_cases hex : ∃ u : Fin n, S u = true ∧ G.adj v u = true
      · exact hex
      · exfalso
        let S' : Fin n → Bool := fun w => if w = v then true else S w
        have hindep' : IsIndepSet G S' := by
          intro a b ha hb
          dsimp [S'] at ha hb
          split at ha
          · next hav =>
            split at hb
            · next hbv => simpa only [hav, hbv] using G.loopless v
            · rw [hav]
              cases hadj : G.adj v b with
              | false => rfl
              | true => exact absurd ⟨b, hb, hadj⟩ hex
          · split at hb
            · next hbv =>
              subst hbv
              cases hadj : G.adj a b with
              | false => rfl
              | true =>
                have hadj' : G.adj b a = true := by rw [G.symm]; exact hadj
                exact absurd ⟨a, ha, hadj'⟩ hex
            · exact hindep a b ha hb
        have hsub : ∀ u : Fin n, S u = true → S' u = true := by
          intro u hu
          dsimp [S']
          split
          · rfl
          · exact hu
        have heq := hmax S' hindep' hsub
        have hv_eq := congrFun heq v
        simp [S', hsv] at hv_eq
  · rintro ⟨hindep, hdom⟩
    refine ⟨hindep, fun S' hindep' hsub => ?_⟩
    funext v
    cases hsv : S v with
    | true => exact hsub v hsv
    | false =>
      cases hsv' : S' v with
      | false => rfl
      | true =>
        rcases hdom v with hv_true | ⟨u, huS, hadj⟩
        · rw [hsv] at hv_true; cases hv_true
        · have huS' : S' u = true := hsub u huS
          have hfalse := hindep' v u hsv' huS'
          rw [hadj] at hfalse
          cases hfalse

def isIndepSetB {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) : Bool :=
  (finRange n).all (fun u =>
    !S u || (finRange n).all (fun v => !S v || !G.adj u v))

def isMaximalIndepSetB {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) : Bool :=
  isIndepSetB G S &&
  (finRange n).all (fun v => S v || (finRange n).any (fun u => S u && G.adj v u))

theorem isIndepSetB_eq_true_iff {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) :
    isIndepSetB G S = true ↔ IsIndepSet G S := by
  unfold isIndepSetB IsIndepSet
  simp only [List.all_eq_true, Bool.or_eq_true, Bool.not_eq_true']
  constructor
  · intro h u v hu hv
    rcases h u (mem_finRange u) with hnu | hall
    · rw [hu] at hnu; cases hnu
    · rcases hall v (mem_finRange v) with hnv | hadj
      · rw [hv] at hnv; cases hnv
      · exact hadj
  · intro h u _
    cases hu : S u with
    | false => exact Or.inl rfl
    | true =>
      right
      intro v _
      cases hv : S v with
      | false => exact Or.inl rfl
      | true => exact Or.inr (h u v hu hv)

theorem isMaximalIndepSetB_eq_true_iff {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) :
    isMaximalIndepSetB G S = true ↔ IsMaximalIndepSet G S := by
  rw [isMaximalIndepSet_iff_dominating]
  unfold isMaximalIndepSetB IsDominatingIndepSet
  rw [Bool.and_eq_true, isIndepSetB_eq_true_iff]
  apply and_congr_right
  intro _
  simp only [List.all_eq_true, List.any_eq_true, Bool.or_eq_true, Bool.and_eq_true]
  constructor
  · intro h v
    rcases h v (mem_finRange v) with hv | ⟨u, _, hu, hadj⟩
    · exact Or.inl hv
    · exact Or.inr ⟨u, hu, hadj⟩
  · intro h v _
    rcases h v with hv | ⟨u, hu, hadj⟩
    · exact Or.inl hv
    · exact Or.inr ⟨u, mem_finRange u, hu, hadj⟩

def allMIS {n : Nat} (G : SimpleGraph n) : List (Fin n → Bool) :=
  (allSubsets n).filter (isMaximalIndepSetB G)

theorem nodup_allMIS {n : Nat} (G : SimpleGraph n) : (allMIS G).Nodup :=
  nodup_filter _ (nodup_allSubsets n)

theorem mem_allMIS_iff {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) :
    S ∈ allMIS G ↔ IsMaximalIndepSet G S := by
  unfold allMIS
  rw [List.mem_filter]
  exact ⟨fun ⟨_, h⟩ => (isMaximalIndepSetB_eq_true_iff G S).mp h,
         fun h => ⟨mem_allSubsets S, (isMaximalIndepSetB_eq_true_iff G S).mpr h⟩⟩

def NstatTotal {n : Nat} (G : SimpleGraph n) : Nat :=
  (allMIS G).length

def NstatCountEq {n : Nat} (G : SimpleGraph n) (t : Nat) : Nat :=
  ((allMIS G).filter (fun S => decide (setSize S = t))).length

def NstatCountLe {n : Nat} (G : SimpleGraph n) (t : Nat) : Nat :=
  ((allMIS G).filter (fun S => decide (setSize S ≤ t))).length

/-! ## Section 5: Induced Subgraphs, Closed-Neighborhood Deletion, and RSA (`Nseq`) -/

def inducedSubgraph {n : Nat} (G : SimpleGraph n) (keep : Fin n → Bool) :
    SimpleGraph ((finRange n).filter keep).length where
  adj i j := G.adj (((finRange n).filter keep).get i) (((finRange n).filter keep).get j)
  symm _ _ := G.symm _ _
  loopless _ := G.loopless _

def notInClosedNhd {n : Nat} (G : SimpleGraph n) (v u : Fin n) : Bool :=
  !(decide (u = v)) && !(G.adj v u)

def remVerts {n : Nat} (G : SimpleGraph n) (v : Fin n) : List (Fin n) :=
  (finRange n).filter (notInClosedNhd G v)

def remOrder {n : Nat} (G : SimpleGraph n) (v : Fin n) : Nat :=
  (remVerts G v).length

theorem remOrder_lt {n : Nat} (G : SimpleGraph n) (v : Fin n) :
    remOrder G v < n := by
  unfold remOrder remVerts
  have hlt : ((finRange n).filter (notInClosedNhd G v)).length < (finRange n).length :=
    length_filter_lt_of_false (notInClosedNhd G v) (mem_finRange v) (by simp [notInClosedNhd])
  rwa [length_finRange] at hlt

def deleteClosedNhd {n : Nat} (G : SimpleGraph n) (v : Fin n) : SimpleGraph (remOrder G v) :=
  inducedSubgraph G (notInClosedNhd G v)

/-- Lifting an MIS `J` of `G \ N_G[v]` to an MIS `{v} ∪ J` of `G` of size `1 + |J|`. -/
def liftMIS {n : Nat} (G : SimpleGraph n) (v : Fin n) (J : Fin (remOrder G v) → Bool)
    (w : Fin n) : Bool :=
  decide (w = v) || (finRange (remOrder G v)).any (fun i => J i && decide ((remVerts G v).get i = w))

theorem mem_rem_iff {n : Nat} (G : SimpleGraph n) (v w : Fin n) :
    notInClosedNhd G v w = true ↔ ∃ i : Fin (remOrder G v), (remVerts G v).get i = w := by
  have hmem : w ∈ remVerts G v ↔ notInClosedNhd G v w = true := by
    unfold remVerts
    rw [List.mem_filter]
    exact ⟨fun ⟨_, h⟩ => h, fun h => ⟨mem_finRange w, h⟩⟩
  rw [← hmem, List.mem_iff_get]
  rfl

theorem liftMIS_get {n : Nat} (G : SimpleGraph n) (v : Fin n)
    (J : Fin (remOrder G v) → Bool) (i : Fin (remOrder G v)) :
    liftMIS G v J ((remVerts G v).get i) = J i := by
  have hrem_nodup := nodup_filter (notInClosedNhd G v) (nodup_finRange n)
  unfold liftMIS
  have hmem_i : (remVerts G v).get i ∈ remVerts G v := List.get_mem _ i
  have hnot : notInClosedNhd G v ((remVerts G v).get i) = true :=
    (List.mem_filter.mp hmem_i).2
  have hne_v : (remVerts G v).get i ≠ v := by
    unfold notInClosedNhd at hnot
    rw [Bool.and_eq_true, Bool.not_eq_true', decide_eq_false_iff_not] at hnot
    exact hnot.1
  simp only [decide_eq_false hne_v, Bool.false_or]
  cases hJi : J i with
  | true =>
    rw [List.any_eq_true]
    exact ⟨i, mem_finRange i, by simp [hJi]⟩
  | false =>
    rw [Bool.eq_false_iff]
    intro hany
    rw [List.any_eq_true] at hany
    rcases hany with ⟨j, _, hj⟩
    rw [Bool.and_eq_true, decide_eq_true_eq] at hj
    have hij : j = i := nodup_get_inj hrem_nodup hj.2
    subst hij
    rw [hJi] at hj
    cases hj.1

theorem liftMIS_true_cases {n : Nat} (G : SimpleGraph n) (v : Fin n)
    (J : Fin (remOrder G v) → Bool) (w : Fin n) (hw : liftMIS G v J w = true) :
    w = v ∨ ∃ i : Fin (remOrder G v), J i = true ∧ (remVerts G v).get i = w := by
  unfold liftMIS at hw
  rw [Bool.or_eq_true] at hw
  rcases hw with hwv | hany
  · exact Or.inl (of_decide_eq_true hwv)
  · rw [List.any_eq_true] at hany
    rcases hany with ⟨i, _, hi⟩
    rw [Bool.and_eq_true, decide_eq_true_eq] at hi
    exact Or.inr ⟨i, hi.1, hi.2⟩

theorem isMaximalIndepSet_liftMIS {n : Nat} (G : SimpleGraph n) (v : Fin n)
    (J : Fin (remOrder G v) → Bool) (hJ : IsMaximalIndepSet (deleteClosedNhd G v) J) :
    IsMaximalIndepSet G (liftMIS G v J) ∧
    liftMIS G v J v = true ∧
    setSize (liftMIS G v J) = 1 + setSize J := by
  rw [isMaximalIndepSet_iff_dominating] at hJ ⊢
  rcases hJ with ⟨hJ_ind, hJ_dom⟩
  have hrem_nodup : (remVerts G v).Nodup := nodup_filter _ (nodup_finRange n)
  have lift_v : liftMIS G v J v = true := by simp [liftMIS]
  have hind : IsIndepSet G (liftMIS G v J) := by
    intro a b ha hb
    rcases liftMIS_true_cases G v J a ha with hav | ⟨ia, hJia, rfl⟩
    · subst a
      rcases liftMIS_true_cases G v J b hb with hbv | ⟨ib, _, rfl⟩
      · subst b
        exact G.loopless v
      · have hnot : notInClosedNhd G v ((remVerts G v).get ib) = true :=
          (List.mem_filter.mp (List.get_mem _ ib)).2
        unfold notInClosedNhd at hnot
        rw [Bool.and_eq_true, Bool.not_eq_true', Bool.not_eq_true'] at hnot
        exact hnot.2
    · rcases liftMIS_true_cases G v J b hb with hbv | ⟨ib, hJib, rfl⟩
      · subst b
        have hnot : notInClosedNhd G v ((remVerts G v).get ia) = true :=
          (List.mem_filter.mp (List.get_mem _ ia)).2
        unfold notInClosedNhd at hnot
        rw [Bool.and_eq_true, Bool.not_eq_true', Bool.not_eq_true'] at hnot
        rw [G.symm]
        exact hnot.2
      · exact hJ_ind ia ib hJia hJib
  have hdom : ∀ w : Fin n, liftMIS G v J w = true ∨
      ∃ u : Fin n, liftMIS G v J u = true ∧ G.adj w u = true := by
    intro w
    by_cases hwv : w = v
    · subst hwv; exact Or.inl lift_v
    · cases hadj_vw : G.adj v w with
      | true =>
        right
        refine ⟨v, lift_v, ?_⟩
        rw [G.symm]; exact hadj_vw
      | false =>
        have hnot : notInClosedNhd G v w = true := by
          unfold notInClosedNhd
          simp [hwv, hadj_vw]
        rcases (mem_rem_iff G v w).mp hnot with ⟨iw, rfl⟩
        rcases hJ_dom iw with hJiw | ⟨ju, hJju, hadj_ij⟩
        · left; rw [liftMIS_get]; exact hJiw
        · right
          refine ⟨(remVerts G v).get ju, ?_, hadj_ij⟩
          rw [liftMIS_get]; exact hJju
  have hsize : setSize (liftMIS G v J) = 1 + setSize J := by
    unfold setSize
    let L1 := (finRange n).filter (liftMIS G v J)
    let Lmap := ((finRange (remOrder G v)).filter J).map (fun i => (remVerts G v).get i)
    let L2 := v :: Lmap
    have hL1_nodup : L1.Nodup := nodup_filter _ (nodup_finRange n)
    have hL2_nodup : L2.Nodup := by
      apply List.Pairwise.cons
      · intro x hx
        change x ∈ ((finRange (remOrder G v)).filter J).map
          (fun i : Fin (remOrder G v) => (remVerts G v).get i) at hx
        rw [List.mem_map] at hx
        rcases hx with ⟨i, _, rfl⟩
        intro hvx
        have hnot : notInClosedNhd G v ((remVerts G v).get i) = true :=
          (List.mem_filter.mp (List.get_mem _ i)).2
        rw [← hvx] at hnot
        simp [notInClosedNhd] at hnot
      · exact nodup_map_of_injOn (nodup_filter J (nodup_finRange (remOrder G v)))
          (fun _ _ _ _ hab => nodup_get_inj hrem_nodup hab)
    have hiff : ∀ x : Fin n, x ∈ L1 ↔ x ∈ L2 := by
      intro x
      change x ∈ (finRange n).filter (liftMIS G v J) ↔
        x ∈ v :: (((finRange (remOrder G v)).filter J).map
          (fun i : Fin (remOrder G v) => (remVerts G v).get i))
      rw [List.mem_filter, List.mem_cons, List.mem_map]
      constructor
      · rintro ⟨_, hx⟩
        rcases liftMIS_true_cases G v J x hx with rfl | ⟨i, hJi, rfl⟩
        · exact Or.inl rfl
        · exact Or.inr ⟨i, List.mem_filter.mpr ⟨mem_finRange i, hJi⟩, rfl⟩
      · intro hx
        rcases hx with rfl | ⟨i, hi_filt, rfl⟩
        · exact ⟨mem_finRange x, lift_v⟩
        · have hJi : J i = true := (List.mem_filter.mp hi_filt).2
          refine ⟨mem_finRange _, ?_⟩
          rw [liftMIS_get]; exact hJi
    have hlen : L1.length = L2.length := length_eq_of_nodup_iff hL1_nodup hL2_nodup hiff
    have hL2_len : L2.length = 1 + ((finRange (remOrder G v)).filter J).length := by
      change (v :: (((finRange (remOrder G v)).filter J).map
        (fun i : Fin (remOrder G v) => (remVerts G v).get i))).length = _
      rw [List.length_cons, List.length_map, Nat.add_comm]
    exact hlen.trans hL2_len
  exact ⟨⟨hind, hdom⟩, lift_v, hsize⟩

/-- Every finite simple graph has at least one maximal independent set, so `0 < NstatTotal G`. -/
theorem exists_mis (n : Nat) (G : SimpleGraph n) :
    ∃ S : Fin n → Bool, IsMaximalIndepSet G S := by
  induction n using Nat.strongRecOn with
  | ind n ih =>
    cases n with
    | zero =>
      refine ⟨fun i => Fin.elim0 i, ?_⟩
      rw [isMaximalIndepSet_iff_dominating]
      exact ⟨fun u => Fin.elim0 u, fun v => Fin.elim0 v⟩
    | succ m =>
      let v0 : Fin (m + 1) := ⟨0, Nat.succ_pos m⟩
      rcases ih (remOrder G v0) (remOrder_lt G v0) (deleteClosedNhd G v0) with ⟨J, hJ⟩
      exact ⟨liftMIS G v0 J, (isMaximalIndepSet_liftMIS G v0 J hJ).1⟩

theorem NstatTotal_pos {n : Nat} (G : SimpleGraph n) : 0 < NstatTotal G := by
  rcases exists_mis n G with ⟨S, hS⟩
  have hmem : S ∈ allMIS G := (mem_allMIS_iff G S).mpr hS
  unfold NstatTotal
  cases hm : allMIS G with
  | nil => rw [hm] at hmem; cases hmem
  | cons _ _ => simp

/-- Exact rational static CDF `P(N^stat(G) ≤ t) = #{MIS of size ≤ t} / #{all MIS}`. -/
def Nstat {n : Nat} (G : SimpleGraph n) (t : Nat) : QProb :=
  ⟨NstatCountLe G t, NstatTotal G, NstatTotal_pos G⟩

/-- Exact rational sequential (RSA) CDF `P(N^seq(G) ≤ t)` via the paper's uniform vertex-deletion
Markov chain (arXiv:2611.14718v2, Section 2.1). -/
def Nseq {n : Nat} (G : SimpleGraph n) (t : Nat) : QProb :=
  match n with
  | 0 => QProb.one
  | m + 1 =>
    match t with
    | 0 => QProb.zero
    | t' + 1 =>
      QProb.divNat
        (finSum (m + 1) (fun v => Nseq (deleteClosedNhd G v) t'))
        (m + 1)
        (Nat.succ_pos m)
termination_by n
decreasing_by
  exact remOrder_lt G v

theorem Nseq_zero_verts (G : SimpleGraph 0) (t : Nat) :
    Nseq G t = QProb.one := by
  unfold Nseq
  rfl

theorem Nseq_succ_zero {m : Nat} (G : SimpleGraph (m + 1)) :
    Nseq G 0 = QProb.zero := by
  unfold Nseq
  rfl

theorem Nseq_succ_succ {m : Nat} (G : SimpleGraph (m + 1)) (t : Nat) :
    Nseq G (t + 1) =
      QProb.divNat
        (finSum (m + 1) (fun v => Nseq (deleteClosedNhd G v) t))
        (m + 1)
        (Nat.succ_pos m) := by
  conv => lhs; unfold Nseq

/-- Conjecture 5.2 order at threshold `t`: `P(N^seq(G) ≤ t) ≤ P(N^stat(G) ≤ t)`. -/
def SeqDominatesStatAt {n : Nat} (G : SimpleGraph n) (t : Nat) : Prop :=
  QProb.Le (Nseq G t) (Nstat G t)

/-- First-order stochastic dominance `N^stat(G) ≤_st N^seq(G)` across all thresholds `t`. -/
def SeqDominatesStat {n : Nat} (G : SimpleGraph n) : Prop :=
  ∀ t : Nat, SeqDominatesStatAt G t

/-- Conjecture 5.2 (`\label{conj:grado3}`) of Higuita-Diaz, Lopez, and Roldan-Correa
(`arXiv:2611.14718v2`). -/
def Conjecture52 : Prop :=
  ∀ (n : Nat) (G : SimpleGraph n), maxDegreeLe3 G → SeqDominatesStat G

/-- General RSA lower-support lemma: if every MIS of `G` has size `> t`, then `P(N^seq(G) ≤ t) = 0`. -/
theorem Nseq_eq_zero_of_all_mis_gt {n : Nat} (G : SimpleGraph n) (t : Nat)
    (hgt : ∀ S : Fin n → Bool, IsMaximalIndepSet G S → t < setSize S) :
    QProb.Eq (Nseq G t) QProb.zero := by
  induction n using Nat.strongRecOn generalizing t with
  | ind n ih =>
    cases n with
    | zero =>
      exfalso
      let S0 : Fin 0 → Bool := fun i => Fin.elim0 i
      have hS0 : IsMaximalIndepSet G S0 := by
        rw [isMaximalIndepSet_iff_dominating]
        exact ⟨fun u => Fin.elim0 u, fun v => Fin.elim0 v⟩
      have hlt := hgt S0 hS0
      have hsz : setSize S0 = 0 := rfl
      omega
    | succ m =>
      cases t with
      | zero =>
        rw [Nseq_succ_zero]
        exact QProb.eq_refl _
      | succ t' =>
        rw [Nseq_succ_succ]
        have hsum0 : QProb.Eq (finSum (m + 1) (fun v => Nseq (deleteClosedNhd G v) t')) QProb.zero := by
          unfold finSum
          apply listSum_map_zero
          intro v _
          apply ih (remOrder G v) (remOrder_lt G v) (deleteClosedNhd G v) t'
          intro J hJ
          have ⟨hM, _, hsz⟩ := isMaximalIndepSet_liftMIS G v J hJ
          have hlt := hgt (liftMIS G v J) hM
          omega
        exact QProb.eq_trans (QProb.divNat_congr (Nat.succ_pos m) hsum0)
          (by unfold QProb.Eq QProb.divNat QProb.zero; simp)

/-- General RSA upper-support lemma: if every MIS of `G` has size `≤ t`, then `P(N^seq(G) ≤ t) = 1`. -/
theorem Nseq_eq_one_of_all_mis_le {n : Nat} (G : SimpleGraph n) (t : Nat)
    (hle : ∀ S : Fin n → Bool, IsMaximalIndepSet G S → setSize S ≤ t) :
    QProb.Eq (Nseq G t) QProb.one := by
  induction n using Nat.strongRecOn generalizing t with
  | ind n ih =>
    cases n with
    | zero =>
      rw [Nseq_zero_verts]
      exact QProb.eq_refl _
    | succ m =>
      cases t with
      | zero =>
        exfalso
        let v0 : Fin (m + 1) := ⟨0, Nat.succ_pos m⟩
        rcases exists_mis (remOrder G v0) (deleteClosedNhd G v0) with ⟨J, hJ⟩
        have ⟨hM, _, hsz⟩ := isMaximalIndepSet_liftMIS G v0 J hJ
        have h0 := hle (liftMIS G v0 J) hM
        omega
      | succ t' =>
        rw [Nseq_succ_succ]
        have hcongr : QProb.Eq
            (finSum (m + 1) (fun v => Nseq (deleteClosedNhd G v) t'))
            (finSum (m + 1) (fun _ => QProb.one)) := by
          unfold finSum
          apply listSum_map_congr
          intro v _
          apply ih (remOrder G v) (remOrder_lt G v) (deleteClosedNhd G v) t'
          intro J hJ
          have ⟨hM, _, hsz⟩ := isMaximalIndepSet_liftMIS G v J hJ
          have h := hle (liftMIS G v J) hM
          omega
        have hconst : QProb.Eq (finSum (m + 1) (fun _ => QProb.one)) (QProb.scaleNat (m + 1) QProb.one) := by
          unfold finSum
          simpa [length_finRange] using listSum_map_const (finRange (m + 1)) QProb.one
        have htot := QProb.eq_trans hcongr hconst
        exact QProb.eq_trans
          (QProb.divNat_congr (Nat.succ_pos m) htot)
          (QProb.divNat_scaleNat_self (m + 1) (Nat.succ_pos m) QProb.one)

/-! ## RSA at a unique minimum maximal independent set -/

def pullMIS {n : Nat} (G : SimpleGraph n) (v : Fin n) (S : Fin n → Bool)
    (i : Fin (remOrder G v)) : Bool :=
  S ((remVerts G v).get i)

private theorem kept_of_selected_ne {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool)
    (hS : IsIndepSet G S) {v w : Fin n} (hv : S v = true) (hw : S w = true) (hne : w ≠ v) :
    notInClosedNhd G v w = true := by
  simp [notInClosedNhd, hne, hS v w hv hw]

theorem lift_pullMIS {n : Nat} (G : SimpleGraph n) (v : Fin n) (S : Fin n → Bool)
    (hS : IsIndepSet G S) (hv : S v = true) : liftMIS G v (pullMIS G v S) = S := by
  funext w
  apply Bool.eq_iff_iff.mpr
  constructor
  · intro h
    rcases liftMIS_true_cases G v (pullMIS G v S) w h with rfl | ⟨i, hi, rfl⟩
    · exact hv
    · exact hi
  · intro hw
    by_cases heq : w = v
    · subst w
      simp [liftMIS]
    · have hkeep := kept_of_selected_ne G S hS hv hw heq
      obtain ⟨i, rfl⟩ := (mem_rem_iff G v w).mp hkeep
      rw [liftMIS_get]
      exact hw

theorem pullMIS_isMIS {n : Nat} (G : SimpleGraph n) (v : Fin n) (S : Fin n → Bool)
    (hS : IsMaximalIndepSet G S) (hv : S v = true) :
    IsMaximalIndepSet (deleteClosedNhd G v) (pullMIS G v S) := by
  rw [isMaximalIndepSet_iff_dominating] at hS ⊢
  have hkept (i : Fin (remOrder G v)) :
      G.adj v ((remVerts G v).get i) = false := by
    have h := (mem_rem_iff G v _).mpr ⟨i, rfl⟩
    rw [notInClosedNhd, Bool.and_eq_true] at h
    simpa using h.2
  refine ⟨fun i j hi hj => hS.1 _ _ hi hj, ?_⟩
  intro i
  rcases hS.2 ((remVerts G v).get i) with hi | ⟨w, hw, ha⟩
  · exact Or.inl hi
  · have hne : w ≠ v := by
      intro h
      subst w
      rw [G.symm, hkept i] at ha
      contradiction
    obtain ⟨j, rfl⟩ := (mem_rem_iff G v w).mp (kept_of_selected_ne G S hS.1 hv hw hne)
    exact Or.inr ⟨j, hw, ha⟩

/-- Probability that every selected vertex lies in the proposed target. For a maximal
independent target this is the probability of obtaining that target. -/
def NseqTarget {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) : QProb :=
  match n with
  | 0 => QProb.one
  | m + 1 =>
    QProb.divNat (finSum (m + 1) (fun v =>
      if S v then NseqTarget (deleteClosedNhd G v) (pullMIS G v S) else QProb.zero))
      (m + 1) (Nat.succ_pos m)
termination_by n
decreasing_by exact remOrder_lt G v

theorem Nseq_of_unique_le {n : Nat} (G : SimpleGraph n) (t : Nat) (S : Fin n → Bool)
    (hS : IsMaximalIndepSet G S) (hs : setSize S ≤ t)
    (huniq : ∀ J : Fin n → Bool, IsMaximalIndepSet G J → setSize J ≤ t → J = S) :
    QProb.Eq (Nseq G t) (NseqTarget G S) := by
  induction n using Nat.strongRecOn generalizing t with
  | ind n ih =>
    cases n with
    | zero =>
      rw [Nseq_zero_verts]
      unfold NseqTarget
      exact QProb.eq_refl _
    | succ n =>
      cases t with
      | zero =>
        exfalso
        have ⟨v, hv⟩ : ∃ v : Fin (n + 1), S v = true := by
          rcases (isMaximalIndepSet_iff_dominating G S).mp hS |>.2 0 with h | ⟨w, hw, _⟩
          · exact ⟨0, h⟩
          · exact ⟨w, hw⟩
        have hmem := List.mem_filter.mpr ⟨mem_finRange v, hv⟩
        have hlen := List.length_pos_of_mem hmem
        exact Nat.not_lt_of_ge hs hlen
      | succ t =>
        rw [Nseq_succ_succ]
        conv => rhs; unfold NseqTarget
        apply QProb.divNat_congr
        unfold finSum
        apply listSum_map_congr
        intro v _
        cases hv : S v with
        | false =>
          simp only [Bool.false_eq_true, ↓reduceIte]
          apply Nseq_eq_zero_of_all_mis_gt
          intro J hJ
          obtain ⟨hJ', hv', hsz⟩ := isMaximalIndepSet_liftMIS G v J hJ
          by_cases h : setSize J ≤ t
          · have heq := huniq _ hJ' (by omega)
            rw [heq, hv] at hv'
            contradiction
          · omega
        | true =>
          simp only [↓reduceIte]
          have hP := pullMIS_isMIS G v S hS hv
          have hL := lift_pullMIS G v S hS.1 hv
          have hsize := (isMaximalIndepSet_liftMIS G v _ hP).2.2
          rw [hL] at hsize
          apply ih (remOrder G v) (remOrder_lt G v) _ t _ hP (by omega)
          intro J hJ hj
          obtain ⟨hJ', _, hsz⟩ := isMaximalIndepSet_liftMIS G v J hJ
          have heq := huniq _ hJ' (by omega)
          funext i
          have hi := congrFun heq ((remVerts G v).get i)
          rwa [liftMIS_get] at hi

/-! ## RSA on a list of active vertices -/

private def targetOn {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) :
    Nat → List (Fin n) → QProb
  | _, [] => QProb.one
  | 0, _ :: _ => QProb.zero
  | fuel + 1, x :: xs =>
    QProb.divNat
      (QProb.listSum ((x :: xs).map fun v => if S v then
        targetOn G S fuel ((x :: xs).filter (notInClosedNhd G v))
        else QProb.zero))
      (xs.length + 1) (Nat.succ_pos _)

private theorem NseqTarget_succ {n : Nat} (G : SimpleGraph (n + 1)) (S : Fin (n + 1) → Bool) :
    NseqTarget G S = QProb.divNat (finSum (n + 1) (fun v =>
      if S v then NseqTarget (deleteClosedNhd G v) (pullMIS G v S) else QProb.zero))
      (n + 1) (Nat.succ_pos n) := by
  conv => lhs; unfold NseqTarget

private theorem divNat_eq_of_same_order {a b : Nat} (ha : 0 < a) (hb : 0 < b)
    (h : a = b) {p q : QProb} (h' : QProb.Eq p q) :
    QProb.Eq (QProb.divNat p a ha) (QProb.divNat q b hb) := by
  subst b
  exact QProb.divNat_congr ha h'

private theorem NseqTarget_eq_active {n k : Nat} (G : SimpleGraph n) (H : SimpleGraph k)
    (S : Fin k → Bool) (live : List (Fin k)) (fuel : Nat)
    (emb : Fin n → Fin k) (hn : n ≤ fuel) (hnd : live.Nodup)
    (hinj : ∀ i j, emb i = emb j → i = j)
    (hmem : ∀ v, v ∈ live ↔ ∃ i, emb i = v)
    (hadj : ∀ i j, G.adj i j = H.adj (emb i) (emb j)) :
    QProb.Eq (NseqTarget G (S ∘ emb)) (targetOn H S fuel live) := by
  induction n using Nat.strongRecOn generalizing fuel live with
  | ind n ih =>
    cases n with
    | zero =>
      cases live with
      | nil =>
        unfold NseqTarget
        cases fuel <;> exact QProb.eq_refl _
      | cons x xs =>
        obtain ⟨i, _⟩ := (hmem x).mp List.mem_cons_self
        exact Fin.elim0 i
    | succ n =>
      have hlen : (n + 1) = live.length := by
        have hnd' := nodup_map_of_injOn (nodup_finRange (n + 1))
          (fun i _ j _ he => hinj i j he)
        have he := length_eq_of_nodup_iff hnd' hnd (by
          intro v
          rw [List.mem_map, hmem]
          exact ⟨fun ⟨i, _, hi⟩ => ⟨i, hi⟩, fun ⟨i, hi⟩ => ⟨i, mem_finRange i, hi⟩⟩)
        simpa only [List.length_map, length_finRange] using he
      cases live with
      | nil => simp at hlen
      | cons x xs =>
        cases fuel with
        | zero => omega
        | succ f =>
          rw [NseqTarget_succ, targetOn]
          apply divNat_eq_of_same_order _ _ hlen
          unfold finSum
          apply listSum_perm_bij (finRange (n + 1)) (x :: xs) emb
          · exact nodup_finRange _
          · exact hnd
          · exact fun i _ j _ he => hinj i j he
          · intro v
            exact (hmem v).trans
              ⟨fun ⟨i, hi⟩ => ⟨i, mem_finRange i, hi⟩, fun ⟨i, _, hi⟩ => ⟨i, hi⟩⟩
          · intro v _
            simp only [Function.comp_apply]
            by_cases hv : S (emb v) = true
            · simp only [ite_eq_left hv]
              let e' : Fin (remOrder G v) → Fin k := fun i => emb ((remVerts G v).get i)
              change QProb.Eq (NseqTarget (deleteClosedNhd G v) (S ∘ e'))
                (targetOn H S f ((x :: xs).filter (notInClosedNhd H (emb v))))
              apply ih (remOrder G v) (remOrder_lt G v) _ _ _ e' (by
                have hlt := remOrder_lt G v
                omega)
              · exact nodup_filter _ hnd
              · intro i j he
                exact nodup_get_inj (nodup_filter _ (nodup_finRange _)) (hinj _ _ he)
              · intro w
                rw [List.mem_filter]
                have hkeep (u : Fin (n + 1)) :
                    notInClosedNhd H (emb v) (emb u) = notInClosedNhd G v u := by
                  unfold notInClosedNhd
                  rw [hadj]
                  by_cases he : u = v
                  · simp [he]
                  · have he' : emb u ≠ emb v := fun heq => he (hinj _ _ heq)
                    simp [he, he']
                constructor
                · rintro ⟨hw, hkeepw⟩
                  obtain ⟨u, rfl⟩ := (hmem w).mp hw
                  rw [hkeep] at hkeepw
                  obtain ⟨i, hi⟩ := (mem_rem_iff G v u).mp hkeepw
                  exact ⟨i, congrArg emb hi⟩
                · rintro ⟨i, rfl⟩
                  refine ⟨(hmem _).mpr ⟨_, rfl⟩, ?_⟩
                  change notInClosedNhd H (emb v) (emb ((remVerts G v).get i)) = true
                  rw [hkeep]
                  exact (mem_rem_iff G v _).mpr ⟨i, rfl⟩
              · intro i j
                exact hadj ((remVerts G v).get i) ((remVerts G v).get j)
            · simp only [ite_eq_right hv]
              exact QProb.eq_refl _

private theorem NseqTarget_eq_full_active {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) :
    QProb.Eq (NseqTarget G S) (targetOn G S n (finRange n)) :=
  NseqTarget_eq_active G G S _ _ id (Nat.le_refl _) (nodup_finRange _)
    (fun _ _ h => h) (fun v => ⟨fun _ => ⟨v, rfl⟩, fun _ => mem_finRange v⟩)
    (fun _ _ => rfl)

private def QProb.asRat (p : QProb) : Rat :=
  (p.num : Int) /. (p.den : Int)

private theorem QProb.eq_iff_asRat (p q : QProb) :
    QProb.Eq p q ↔ p.asRat = q.asRat := by
  unfold QProb.Eq QProb.asRat
  rw [Rat.divInt_eq_divInt_iff (by have := p.den_pos; omega) (by have := q.den_pos; omega)]
  simp only [← Int.natCast_mul, Int.natCast_inj]

private theorem QProb.asRat_add (p q : QProb) :
    (QProb.add p q).asRat = p.asRat + q.asRat := by
  unfold QProb.asRat QProb.add
  rw [Rat.divInt_add_divInt _ _ (by have := p.den_pos; omega)
    (by have := q.den_pos; omega)]
  simp [Int.natCast_mul, Int.natCast_add]

private theorem QProb.asRat_listSum (l : List QProb) :
    (QProb.listSum l).asRat = (l.map QProb.asRat).sum := by
  induction l with
  | nil => decide
  | cons x xs ih =>
    simp only [QProb.listSum, QProb.asRat_add, List.map_cons, List.sum_cons, ih]

private theorem QProb.asRat_divNat (p : QProb) (k : Nat) (hk : 0 < k) :
    (QProb.divNat p k hk).asRat = p.asRat / (k : Rat) := by
  unfold QProb.asRat QProb.divNat
  change (p.num : Int) /. ((k * p.den : Nat) : Int) = ((p.num : Int) /. (p.den : Int)) / (k : Rat)
  have he : (1 : Int) /. (k : Int) = (k : Rat)⁻¹ := by
    calc
      (1 : Int) /. (k : Int) = (((k : Int) /. (1 : Int))⁻¹) :=
        (Rat.inv_divInt _ _).symm
      _ = (k : Rat)⁻¹ := by
        rw [Rat.divInt_eq_div, Rat.intCast_natCast]
        change ((k : Rat) / 1)⁻¹ = (k : Rat)⁻¹
        rw [Rat.div_def, show (1 : Rat)⁻¹ = 1 by decide +kernel, Rat.mul_one]
  rw [Rat.div_def, ← he, Rat.divInt_mul_divInt, Int.natCast_mul, Int.mul_one, Int.mul_comm]

private def activeProb {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool)
    (fuel : Nat) (live : List (Fin n)) : Rat := (targetOn G S fuel live).asRat

private theorem activeProb_nil {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool) (fuel : Nat) :
    activeProb G S fuel [] = 1 := by
  have h : QProb.one.asRat = 1 := by decide
  cases fuel <;> exact h

private def activeTerm {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool)
    (fuel : Nat) (live : List (Fin n)) (v : Fin n) : Rat :=
  if S v then activeProb G S fuel (live.filter (notInClosedNhd G v)) else 0

private theorem activeProb_step {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool)
    (fuel : Nat) (live : List (Fin n)) (hne : live ≠ []) :
    activeProb G S (fuel + 1) live =
      (live.map (activeTerm G S fuel live)).sum / (live.length : Rat) := by
  cases live with
  | nil => contradiction
  | cons x xs =>
    unfold activeProb targetOn
    rw [QProb.asRat_divNat, QProb.asRat_listSum, List.map_map]
    congr 1
    apply congrArg List.sum
    apply List.map_congr_left
    intro v _
    unfold activeTerm
    simp only [Function.comp_apply]
    by_cases hv : S v = true
    · simp only [ite_eq_left hv]
      rfl
    · simp only [ite_eq_right hv]
      decide

private theorem activeProb_fuel {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool)
    (l : List (Fin n)) (f g : Nat) (hf : l.length ≤ f) (hg : l.length ≤ g) :
    activeProb G S f l = activeProb G S g l := by
  induction f generalizing g l with
  | zero =>
    have hl : l = [] := List.length_eq_zero_iff.mp (by omega)
    simp [hl, activeProb_nil]
  | succ f ih =>
    cases l with
    | nil => simp only [activeProb_nil]
    | cons x xs =>
      cases g with
      | zero => simp at hg
      | succ g =>
        rw [activeProb_step G S f _ (by simp), activeProb_step G S g _ (by simp)]
        congr 1
        apply congrArg List.sum
        apply List.map_congr_left
        intro v hv
        unfold activeTerm
        by_cases hS : S v = true
        · simp only [ite_eq_left hS]
          have hlt := length_filter_lt_of_false (notInClosedNhd G v) hv (by simp [notInClosedNhd])
          exact ih _ _ (by omega) (by omega)
        · simp only [ite_eq_right hS]

private theorem weightedSum_mul {α : Type} (l : List α) (f : α → Rat) (c : Rat) :
    (l.map (fun x => f x * c)).sum = (l.map f).sum * c := by
  induction l with
  | nil => simp
  | cons x xs ih => simp only [List.map_cons, List.sum_cons, ih, Rat.add_mul]

private theorem separates_kept_right {n : Nat} {G : SimpleGraph n} {S : Fin n → Bool}
    {l r : List (Fin n)}
    (hab : ∀ u ∈ l, ∀ v ∈ r, u ≠ v ∧ (S u = true ∨ S v = true → G.adj u v = false))
    {u : Fin n} (hu : u ∈ l) (hs : S u = true) :
    r.filter (notInClosedNhd G u) = r := by
  apply List.filter_eq_self.mpr
  intro v hv
  obtain ⟨hne, ha⟩ := hab u hu v hv
  simp [notInClosedNhd, Ne.symm hne, ha (Or.inl hs)]

private theorem separates_symm {n : Nat} {G : SimpleGraph n} {S : Fin n → Bool}
    {l r : List (Fin n)}
    (hab : ∀ u ∈ l, ∀ v ∈ r, u ≠ v ∧ (S u = true ∨ S v = true → G.adj u v = false))
    (u) (hu : u ∈ r) (v) (hv : v ∈ l) :
    u ≠ v ∧ (S u = true ∨ S v = true → G.adj u v = false) := by
  obtain ⟨hne, ha⟩ := hab v hv u hu
  exact ⟨Ne.symm hne, fun h => (G.symm u v).trans (ha (Or.symm h))⟩

/-- Target selection probabilities multiply when no target vertex can delete a vertex
of the other list. Edges between two vertices outside the target are allowed. -/
private theorem activeProb_append {n : Nat} (G : SimpleGraph n) (S : Fin n → Bool)
    (f : Nat) (l r : List (Fin n)) (a b : Nat)
    (hf : l.length + r.length ≤ f) (ha : l.length ≤ a) (hb : r.length ≤ b)
    (hsep : ∀ u ∈ l, ∀ v ∈ r, u ≠ v ∧ (S u = true ∨ S v = true → G.adj u v = false)) :
    activeProb G S f (l ++ r) = activeProb G S a l * activeProb G S b r := by
  induction f generalizing l r a b with
  | zero =>
    have hl : l = [] := List.length_eq_zero_iff.mp (by omega)
    have hr : r = [] := List.length_eq_zero_iff.mp (by omega)
    simp [hl, hr, activeProb_nil]
  | succ f ih =>
    by_cases hl : l = []
    · subst l
      simp only [List.nil_append, activeProb_nil, Rat.one_mul]
      exact activeProb_fuel G S r _ _ (by simpa using hf) hb
    by_cases hr : r = []
    · subst r
      simp only [List.append_nil, activeProb_nil, Rat.mul_one]
      exact activeProb_fuel G S l _ _ (by simpa using hf) ha
    have hlpos := List.length_pos_iff.mpr hl
    have hrpos := List.length_pos_iff.mpr hr
    cases a with
    | zero => omega
    | succ a =>
      cases b with
      | zero => omega
      | succ b =>
        let L := activeProb G S (a + 1) l
        let R := activeProb G S (b + 1) r
        let leftSum := (l.map (activeTerm G S a l)).sum
        let rightSum := (r.map (activeTerm G S b r)).sum
        have hleft : (l.map (activeTerm G S f (l ++ r))).sum = leftSum * R := by
          rw [← weightedSum_mul l (activeTerm G S a l) R]
          apply congrArg List.sum
          apply List.map_congr_left
          intro v hv
          unfold activeTerm
          by_cases hs : S v = true
          · simp only [ite_eq_left hs, List.filter_append, separates_kept_right hsep hv hs]
            have hh := length_filter_lt_of_false (notInClosedNhd G v) hv (by simp [notInClosedNhd])
            exact ih _ _ _ _ (by omega) (by omega) hb
              (fun u hu w hw => hsep u (List.mem_filter.mp hu).1 w hw)
          · simp [hs]
        have hright : (r.map (activeTerm G S f (l ++ r))).sum = rightSum * L := by
          rw [← weightedSum_mul r (activeTerm G S b r) L]
          apply congrArg List.sum
          apply List.map_congr_left
          intro v hv
          unfold activeTerm
          by_cases hs : S v = true
          · simp only [ite_eq_left hs, List.filter_append,
              separates_kept_right (separates_symm hsep) hv hs]
            have hh := length_filter_lt_of_false (notInClosedNhd G v) hv (by simp [notInClosedNhd])
            rw [Rat.mul_comm]
            exact ih _ _ _ _ (by omega) ha (by omega)
              (fun u hu w hw => hsep u hu w (List.mem_filter.mp hw).1)
          · simp [hs]
        have hln : (l.length : Rat) ≠ 0 := by simp [Nat.ne_of_gt hlpos]
        have hrn : (r.length : Rat) ≠ 0 := by simp [Nat.ne_of_gt hrpos]
        have hden : ((l ++ r).length : Rat) ≠ 0 := by
          simp only [ne_eq, Rat.natCast_eq_zero_iff, List.length_append]
          omega
        have hx : L * (l.length : Rat) = leftSum :=
          (congrArg (· * (l.length : Rat)) (activeProb_step G S a l hl)).trans
            (Rat.div_mul_cancel hln)
        have hy : R * (r.length : Rat) = rightSum :=
          (congrArg (· * (r.length : Rat)) (activeProb_step G S b r hr)).trans
            (Rat.div_mul_cancel hrn)
        change activeProb G S (f + 1) (l ++ r) = L * R
        rw [activeProb_step G S f _ (fun h => hl (List.append_eq_nil_iff.mp h).1),
          List.map_append, List.sum_append, hleft, hright, ← hx, ← hy]
        have hsum : L * (l.length : Rat) * R + R * (r.length : Rat) * L =
            (L * R) * ((l ++ r).length : Rat) := by
          rw [List.length_append, Rat.natCast_add, Rat.mul_add]
          congr 1
          · rw [Rat.mul_assoc L, Rat.mul_comm (l.length : Rat) R, ← Rat.mul_assoc]
          · rw [Rat.mul_comm _ L, Rat.mul_assoc L, Rat.mul_comm R, ← Rat.mul_assoc]
        rw [hsum]
        exact Rat.mul_div_cancel hden

/-! ## Section 6: Graph Isomorphisms and Invariance of Graph/MIS/RSA Invariants -/

structure GraphIso {n1 n2 : Nat} (G : SimpleGraph n1) (H : SimpleGraph n2) where
  toFun : Fin n1 → Fin n2
  invFun : Fin n2 → Fin n1
  left_inv : ∀ u : Fin n1, invFun (toFun u) = u
  right_inv : ∀ v : Fin n2, toFun (invFun v) = v
  map_adj : ∀ u v : Fin n1, H.adj (toFun u) (toFun v) = G.adj u v

def GraphIso.symm {n1 n2 : Nat} {G : SimpleGraph n1} {H : SimpleGraph n2}
    (e : GraphIso G H) : GraphIso H G where
  toFun := e.invFun
  invFun := e.toFun
  left_inv := e.right_inv
  right_inv := e.left_inv
  map_adj u v := by
    have h := e.map_adj (e.invFun u) (e.invFun v)
    rw [e.right_inv u, e.right_inv v] at h
    exact h.symm

theorem GraphIso.order_eq {n1 n2 : Nat} {G : SimpleGraph n1} {H : SimpleGraph n2}
    (e : GraphIso G H) : n1 = n2 := by
  have h1 : ((finRange n1).map e.toFun).Nodup := by
    apply nodup_map_of_injOn (nodup_finRange n1)
    intro a _ b _ hab
    have := congrArg e.invFun hab
    rwa [e.left_inv, e.left_inv] at this
  have hiff : ∀ v : Fin n2, v ∈ (finRange n1).map e.toFun ↔ v ∈ finRange n2 := by
    intro v
    simp only [List.mem_map]
    exact ⟨fun _ => mem_finRange v, fun _ => ⟨e.invFun v, mem_finRange _, e.right_inv v⟩⟩
  have hlen := length_eq_of_nodup_iff h1 (nodup_finRange n2) hiff
  simpa [length_finRange] using hlen

theorem GraphIso.degree_eq {n1 n2 : Nat} {G : SimpleGraph n1} {H : SimpleGraph n2}
    (e : GraphIso G H) (u : Fin n1) : G.degree u = H.degree (e.toFun u) := by
  unfold SimpleGraph.degree
  let L1 := ((finRange n1).filter (fun w => G.adj u w)).map e.toFun
  let L2 := (finRange n2).filter (fun z => H.adj (e.toFun u) z)
  have hL1_nodup : L1.Nodup := by
    apply nodup_map_of_injOn (nodup_filter _ (nodup_finRange n1))
    intro a _ b _ hab
    have := congrArg e.invFun hab
    rwa [e.left_inv, e.left_inv] at this
  have hL2_nodup : L2.Nodup := nodup_filter _ (nodup_finRange n2)
  have hiff : ∀ z : Fin n2, z ∈ L1 ↔ z ∈ L2 := by
    intro z
    simp only [L1, L2, List.mem_map, List.mem_filter]
    constructor
    · rintro ⟨w, ⟨_, hadj⟩, rfl⟩
      exact ⟨mem_finRange _, by rw [e.map_adj]; exact hadj⟩
    · rintro ⟨_, hadj⟩
      refine ⟨e.invFun z, ⟨mem_finRange _, ?_⟩, e.right_inv z⟩
      have h := e.map_adj u (e.invFun z)
      rw [e.right_inv z] at h
      exact h.symm.trans hadj
  have hlen := length_eq_of_nodup_iff hL1_nodup hL2_nodup hiff
  simpa [L1] using hlen

theorem GraphIso.maxDegreeLe3_iff {n1 n2 : Nat} {G : SimpleGraph n1} {H : SimpleGraph n2}
    (e : GraphIso G H) : maxDegreeLe3 G ↔ maxDegreeLe3 H := by
  constructor
  · intro h v
    have hd := e.degree_eq (e.invFun v)
    rw [e.right_inv v] at hd
    rw [← hd]
    exact h (e.invFun v)
  · intro h u
    rw [e.degree_eq u]
    exact h (e.toFun u)

theorem GraphIso.isTree_iff {n1 n2 : Nat} {G : SimpleGraph n1} {H : SimpleGraph n2}
    (e : GraphIso G H) : IsTree G ↔ IsTree H := by
  have mapWalk : ∀ {a b : Nat} {G1 : SimpleGraph a} {G2 : SimpleGraph b}
      (f : GraphIso G1 G2) {u v : Fin a}, Walk G1 u v → Walk G2 (f.toFun u) (f.toFun v) := by
    intro a b G1 G2 f u v hw
    induction hw with
    | nil u => exact Walk.nil (f.toFun u)
    | cons hadj _ ih =>
      exact Walk.cons (by rw [f.map_adj]; exact hadj) ih
  have mapCycle : ∀ {a b : Nat} {G1 : SimpleGraph a} {G2 : SimpleGraph b}
      (f : GraphIso G1 G2) (c : List (Fin a)), IsSimpleCycle G1 c → IsSimpleCycle G2 (c.map f.toFun) := by
    intro a b G1 G2 f c ⟨hlen, hnodup, hcyc⟩
    refine ⟨by simpa using hlen, ?_, ?_⟩
    · apply nodup_map_of_injOn hnodup
      intro x _ y _ hxy
      have := congrArg f.invFun hxy
      rwa [f.left_inv, f.left_inv] at this
    · intro i
      let i0 : Fin c.length := ⟨i.val, by simpa using i.isLt⟩
      have h := hcyc i0
      have h1 : (c.map f.toFun).get i = f.toFun (c.get i0) := by simp [i0]
      have h2 : (c.map f.toFun).get
          ⟨(i.val + 1) % (c.map f.toFun).length, Nat.mod_lt _ (Nat.zero_lt_of_lt i.isLt)⟩ =
          f.toFun (c.get ⟨(i0.val + 1) % c.length, Nat.mod_lt _ (Nat.zero_lt_of_lt i0.isLt)⟩) := by
        simp [i0]
      rw [h1, h2, f.map_adj]
      exact h
  have dir : ∀ {a b : Nat} {G1 : SimpleGraph a} {G2 : SimpleGraph b}
      (f : GraphIso G1 G2), IsTree G1 → IsTree G2 := by
    intro a b G1 G2 f ⟨⟨ha, hconn⟩, hacyc⟩
    refine ⟨⟨f.order_eq ▸ ha, fun u v => ?_⟩, fun c hc => ?_⟩
    · have hw := mapWalk f (hconn (f.invFun u) (f.invFun v))
      rwa [f.right_inv u, f.right_inv v] at hw
    · exact hacyc (c.map f.symm.toFun) (mapCycle f.symm c hc)
  exact ⟨dir e, dir e.symm⟩

theorem GraphIso.Nstat_eq {n1 n2 : Nat} {G : SimpleGraph n1} {H : SimpleGraph n2}
    (e : GraphIso G H) (t : Nat) :
    NstatTotal G = NstatTotal H ∧
    NstatCountLe G t = NstatCountLe H t ∧
    QProb.Eq (Nstat G t) (Nstat H t) := by
  let tr : (Fin n1 → Bool) → (Fin n2 → Bool) := fun S v => S (e.invFun v)
  let trInv : (Fin n2 → Bool) → (Fin n1 → Bool) := fun T u => T (e.toFun u)
  have htr_left : ∀ S : Fin n1 → Bool, trInv (tr S) = S := by
    intro S; funext u; simp [tr, trInv, e.left_inv]
  have htr_right : ∀ T : Fin n2 → Bool, tr (trInv T) = T := by
    intro T; funext v; simp [tr, trInv, e.right_inv]
  have htr_size : ∀ S : Fin n1 → Bool, setSize (tr S) = setSize S := by
    intro S
    unfold setSize
    let L1 := ((finRange n1).filter S).map e.toFun
    let L2 := (finRange n2).filter (tr S)
    have h1 : L1.Nodup := by
      apply nodup_map_of_injOn (nodup_filter _ (nodup_finRange n1))
      intro a _ b _ hab
      have := congrArg e.invFun hab
      rwa [e.left_inv, e.left_inv] at this
    have h2 : L2.Nodup := nodup_filter _ (nodup_finRange n2)
    have hiff : ∀ v : Fin n2, v ∈ L1 ↔ v ∈ L2 := by
      intro v
      simp only [L1, L2, List.mem_map, List.mem_filter, tr]
      constructor
      · rintro ⟨u, ⟨_, hu⟩, rfl⟩
        exact ⟨mem_finRange _, by simpa [e.left_inv] using hu⟩
      · rintro ⟨_, hv⟩
        exact ⟨e.invFun v, ⟨mem_finRange _, hv⟩, e.right_inv v⟩
    have hlen := length_eq_of_nodup_iff h1 h2 hiff
    simpa [L1] using hlen.symm
  have htr_mis : ∀ S : Fin n1 → Bool, IsMaximalIndepSet G S → IsMaximalIndepSet H (tr S) := by
    intro S hS
    rw [isMaximalIndepSet_iff_dominating] at hS ⊢
    rcases hS with ⟨hind, hdom⟩
    refine ⟨fun u v hu hv => ?_, fun v => ?_⟩
    · have hadj := hind (e.invFun u) (e.invFun v) hu hv
      have hm := e.map_adj (e.invFun u) (e.invFun v)
      rw [e.right_inv u, e.right_inv v] at hm
      exact hm.trans hadj
    · rcases hdom (e.invFun v) with hv | ⟨u, hu, hadj⟩
      · exact Or.inl hv
      · right
        refine ⟨e.toFun u, ?_, ?_⟩
        · simp [tr, e.left_inv, hu]
        · have hm := e.map_adj (e.invFun v) u
          rw [e.right_inv v] at hm
          exact hm.trans hadj
  have htrInv_mis : ∀ T : Fin n2 → Bool, IsMaximalIndepSet H T → IsMaximalIndepSet G (trInv T) := by
    intro T hT
    rw [isMaximalIndepSet_iff_dominating] at hT ⊢
    rcases hT with ⟨hind, hdom⟩
    refine ⟨fun u v hu hv => ?_, fun v => ?_⟩
    · have hadj := hind (e.toFun u) (e.toFun v) hu hv
      rw [e.map_adj] at hadj
      exact hadj
    · rcases hdom (e.toFun v) with hv | ⟨w, hw, hadj⟩
      · exact Or.inl hv
      · right
        refine ⟨e.invFun w, ?_, ?_⟩
        · simp [trInv, e.right_inv, hw]
        · have hm := e.map_adj v (e.invFun w)
          rw [e.right_inv w] at hm
          exact hm.symm.trans hadj
  have htot : NstatTotal G = NstatTotal H := by
    unfold NstatTotal
    let L1 := (allMIS G).map tr
    have h1 : L1.Nodup := by
      apply nodup_map_of_injOn (nodup_allMIS G)
      intro a _ b _ hab
      have := congrArg trInv hab
      rwa [htr_left, htr_left] at this
    have hiff : ∀ T : Fin n2 → Bool, T ∈ L1 ↔ T ∈ allMIS H := by
      intro T
      simp only [L1, List.mem_map, mem_allMIS_iff]
      constructor
      · rintro ⟨S, hS, rfl⟩; exact htr_mis S hS
      · intro hT; exact ⟨trInv T, htrInv_mis T hT, htr_right T⟩
    have hlen := length_eq_of_nodup_iff h1 (nodup_allMIS H) hiff
    simpa [L1] using hlen
  have hle : NstatCountLe G t = NstatCountLe H t := by
    unfold NstatCountLe
    let L1 := ((allMIS G).filter (fun S => decide (setSize S ≤ t))).map tr
    let L2 := (allMIS H).filter (fun T => decide (setSize T ≤ t))
    have h1 : L1.Nodup := by
      apply nodup_map_of_injOn (nodup_filter _ (nodup_allMIS G))
      intro a _ b _ hab
      have := congrArg trInv hab
      rwa [htr_left, htr_left] at this
    have h2 : L2.Nodup := nodup_filter _ (nodup_allMIS H)
    have hiff : ∀ T : Fin n2 → Bool, T ∈ L1 ↔ T ∈ L2 := by
      intro T
      simp only [L1, L2, List.mem_map, List.mem_filter, mem_allMIS_iff, decide_eq_true_eq]
      constructor
      · rintro ⟨S, ⟨hS, hsz⟩, rfl⟩
        exact ⟨htr_mis S hS, by rwa [htr_size]⟩
      · rintro ⟨hT, hsz⟩
        refine ⟨trInv T, ⟨htrInv_mis T hT, ?_⟩, htr_right T⟩
        have h := htr_size (trInv T)
        rw [htr_right] at h
        omega
    have hlen := length_eq_of_nodup_iff h1 h2 hiff
    simpa [L1] using hlen
  refine ⟨htot, hle, ?_⟩
  unfold QProb.Eq Nstat
  simp [htot, hle]

/-- Induced subgraph isomorphism from duplicate-free vertex bijections. -/
def inducedSubgraphIso {n1 n2 : Nat} {G : SimpleGraph n1} {H : SimpleGraph n2}
    (keep1 : Fin n1 → Bool) (keep2 : Fin n2 → Bool)
    (e : GraphIso G H)
    (hkeep : ∀ u : Fin n1, keep2 (e.toFun u) = keep1 u) :
    GraphIso (inducedSubgraph G keep1) (inducedSubgraph H keep2) := by
  let L1 := (finRange n1).filter keep1
  let L2 := (finRange n2).filter keep2
  have hL1_nodup : L1.Nodup := nodup_filter _ (nodup_finRange n1)
  have hL2_nodup : L2.Nodup := nodup_filter _ (nodup_finRange n2)
  have mem2_of_1 : ∀ i : Fin L1.length, e.toFun (L1.get i) ∈ L2 := by
    intro i
    have hi : L1.get i ∈ L1 := List.get_mem L1 i
    rw [List.mem_filter] at hi ⊢
    exact ⟨mem_finRange _, by rw [hkeep]; exact hi.2⟩
  have mem1_of_2 : ∀ j : Fin L2.length, e.invFun (L2.get j) ∈ L1 := by
    intro j
    have hj : L2.get j ∈ L2 := List.get_mem L2 j
    rw [List.mem_filter] at hj ⊢
    refine ⟨mem_finRange _, ?_⟩
    have hk := hkeep (e.invFun (L2.get j))
    rw [e.right_inv] at hk
    exact hk.symm.trans hj.2
  refine
    { toFun := fun i => idxOfMem L2 (e.toFun (L1.get i)) (mem2_of_1 i)
      invFun := fun j => idxOfMem L1 (e.invFun (L2.get j)) (mem1_of_2 j)
      left_inv := fun i => ?_
      right_inv := fun j => ?_
      map_adj := fun i j => ?_ }
  · apply nodup_get_inj hL1_nodup
    rw [get_idxOfMem, get_idxOfMem, e.left_inv]
  · apply nodup_get_inj hL2_nodup
    rw [get_idxOfMem, get_idxOfMem, e.right_inv]
  · dsimp [inducedSubgraph]
    change H.adj (L2.get (idxOfMem L2 (e.toFun (L1.get i)) (mem2_of_1 i)))
        (L2.get (idxOfMem L2 (e.toFun (L1.get j)) (mem2_of_1 j))) =
      G.adj (L1.get i) (L1.get j)
    rw [get_idxOfMem, get_idxOfMem, e.map_adj]

theorem GraphIso.Nseq_eq {n1 n2 : Nat} {G : SimpleGraph n1} {H : SimpleGraph n2}
    (e : GraphIso G H) (t : Nat) :
    QProb.Eq (Nseq G t) (Nseq H t) := by
  induction n1 using Nat.strongRecOn generalizing n2 H t with
  | ind n1 ih =>
    have hord := e.order_eq
    subst hord
    cases n1 with
    | zero =>
      rw [Nseq_zero_verts, Nseq_zero_verts]
      exact QProb.eq_refl _
    | succ m =>
      cases t with
      | zero =>
        rw [Nseq_succ_zero, Nseq_succ_zero]
        exact QProb.eq_refl _
      | succ t' =>
        rw [Nseq_succ_succ, Nseq_succ_succ]
        apply QProb.divNat_congr (Nat.succ_pos m)
        unfold finSum
        apply listSum_perm_bij (finRange (m + 1)) (finRange (m + 1)) e.toFun
          (fun u => Nseq (deleteClosedNhd G u) t')
          (fun v => Nseq (deleteClosedNhd H v) t')
          (nodup_finRange (m + 1)) (nodup_finRange (m + 1))
        · intro a1 _ a2 _ hab
          have := congrArg e.invFun hab
          rwa [e.left_inv, e.left_inv] at this
        · intro b
          exact ⟨fun _ => ⟨e.invFun b, mem_finRange _, e.right_inv b⟩,
                 fun _ => mem_finRange b⟩
        · intro u _
          have hkeep : ∀ w : Fin (m + 1),
              notInClosedNhd H (e.toFun u) (e.toFun w) = notInClosedNhd G u w := by
            intro w
            unfold notInClosedNhd
            have heq_iff : (e.toFun w = e.toFun u) ↔ (w = u) :=
              ⟨fun h => by have := congrArg e.invFun h; rwa [e.left_inv, e.left_inv] at this,
               fun h => congrArg e.toFun h⟩
            have hdec : decide (e.toFun w = e.toFun u) = decide (w = u) := by
              by_cases hwu : w = u
              · simp [hwu]
              · have hne : e.toFun w ≠ e.toFun u := fun h => hwu (heq_iff.mp h)
                simp [hwu, hne]
            rw [hdec, e.map_adj]
          let subIso : GraphIso (deleteClosedNhd G u) (deleteClosedNhd H (e.toFun u)) :=
            inducedSubgraphIso (notInClosedNhd G u) (notInClosedNhd H (e.toFun u)) e hkeep
          exact ih (remOrder G u) (remOrder_lt G u) subIso t'

/-! ## The supplied 15-vertex witness -/

def graphOfEdges {n : Nat} (edges : List (Nat × Nat)) : SimpleGraph n where
  adj u v := decide (u ≠ v) && (edges.contains (u.val, v.val) || edges.contains (v.val, u.val))
  symm u v := by simp [ne_comm, Bool.or_comm]
  loopless v := by simp

def F3Edges : List (Nat × Nat) :=
  [(0, 1), (0, 2), (0, 3), (1, 4), (2, 8), (3, 12), (4, 5),
   (5, 6), (5, 7), (6, 13), (8, 9), (9, 10), (9, 11), (10, 14)]

def F3 : SimpleGraph 15 := graphOfEdges F3Edges

theorem F3_numEdges : numEdges F3 = 14 := by decide +kernel

theorem F3_maxDegreeLe3 : maxDegreeLe3 F3 := by
  unfold maxDegreeLe3
  decide +kernel

private def F3parent (v : Fin 15) : Fin 15 :=
  #[0, 0, 0, 0, 1, 4, 5, 5, 2, 8, 9, 9, 3, 6, 10][v.val]!

private def F3depth (v : Fin 15) : Nat :=
  #[0, 1, 1, 1, 2, 3, 4, 4, 2, 3, 4, 4, 2, 5, 5][v.val]!

theorem F3_isTree : IsTree F3 := by
  apply isTree_of_rootedParent F3 0 F3parent F3depth
  · rfl
  · decide +kernel
  · decide +kernel

theorem F3_connected : Connected F3 := F3_isTree.1

/-! ## Kernel evaluation of finite static counts -/

private def maskSubset (n k : Nat) (v : Fin n) : Bool := k.testBit v.val

private theorem allSubsets_masks (n : Nat) :
    allSubsets n = (List.range (2 ^ n)).map (maskSubset n) := by
  induction n with
  | zero =>
    simp only [allSubsets, Nat.pow_zero]
    change [fun i => Fin.elim0 i] = [maskSubset 0 0]
    congr
    funext i
    exact Fin.elim0 i
  | succ n ih =>
    rw [allSubsets, ih, Nat.pow_succ, Nat.mul_two, List.range_add, List.map_append]
    simp only [List.map_map]
    congr 1
    · apply List.map_congr_left
      intro k hk
      have hlt := List.mem_range.mp hk
      funext i
      by_cases hi : i.val < n
      · simp [extendSet, maskSubset, hi]
      · have heq : i.val = n := by have := i.isLt; omega
        simp [extendSet, maskSubset, heq, Nat.testBit_lt_two_pow hlt]
    · apply List.map_congr_left
      intro k hk
      have hlt := List.mem_range.mp hk
      funext i
      by_cases hi : i.val < n
      · simp [extendSet, maskSubset, hi, Nat.testBit_two_pow_add_gt hi]
      · have heq : i.val = n := by have := i.isLt; omega
        simp [extendSet, maskSubset, heq, Nat.testBit_two_pow_add_eq,
          Nat.testBit_lt_two_pow hlt]

private theorem mask_inter_empty {n k a : Nat} (ha : a < 2 ^ n) :
    k &&& a = 0 ↔ ∀ i : Fin n, k.testBit i.val = true → a.testBit i.val = false := by
  constructor
  · intro h i hi
    have hb := congrArg (fun b : Nat => b.testBit i.val) h
    simpa [Nat.testBit_and, hi] using hb
  · intro h
    apply Nat.eq_of_testBit_eq
    intro i
    rw [Nat.testBit_and, Nat.zero_testBit]
    by_cases hi : i < n
    · cases hki : k.testBit i
      · rfl
      · simp [h ⟨i, hi⟩ hki]
    · have hat : a < 2 ^ i := Nat.lt_of_lt_of_le ha (Nat.pow_le_pow_right (by decide) (by omega))
      simp [Nat.testBit_lt_two_pow hat]

private def maskMIS {n : Nat} (neighbors : Fin n → Nat) (k : Nat) : Bool :=
  (finRange n).all (fun v => k.testBit v.val == (k &&& neighbors v == 0))

private theorem maskMIS_spec {n : Nat} (G : SimpleGraph n) (neighbors : Fin n → Nat)
    (hb : ∀ v, neighbors v < 2 ^ n)
    (hn : ∀ v w : Fin n, (neighbors v).testBit w.val = G.adj v w)
    (k : Nat) : maskMIS neighbors k = true ↔ IsMaximalIndepSet G (maskSubset n k) := by
  rw [isMaximalIndepSet_iff_dominating]
  simp only [maskMIS, List.all_eq_true, beq_iff_eq]
  constructor
  · intro h
    refine ⟨?_, ?_⟩
    · intro v w hv hw
      have hv' := h v (mem_finRange v)
      change k.testBit v.val = true at hv
      rw [hv] at hv'
      rw [← hn]
      exact (mask_inter_empty (hb v)).mp (beq_iff_eq.mp hv'.symm) w hw
    · intro v
      by_cases hv : maskSubset n k v = true
      · exact Or.inl hv
      · right
        apply Classical.byContradiction
        intro hnbr
        have hint := (mask_inter_empty (k := k) (hb v)).mpr (by
          intro u hu
          rw [hn]
          cases he : G.adj v u
          · rfl
          · exact False.elim (hnbr ⟨u, hu, he⟩))
        exact hv ((h v (mem_finRange v)).trans (beq_iff_eq.mpr hint))
  · rintro ⟨hind, hdom⟩ v _
    cases hv : maskSubset n k v with
    | true =>
      change k.testBit v.val = true at hv
      rw [hv]
      symm
      apply beq_iff_eq.mpr
      apply (mask_inter_empty (hb v)).mpr
      intro w hw
      rw [hn]
      exact hind v w hv hw
    | false =>
      change k.testBit v.val = false at hv
      rw [hv]
      symm
      apply Bool.eq_false_iff.mpr
      intro he
      rcases hdom v with hv' | ⟨w, hw, hAdj⟩
      · simp [maskSubset, hv] at hv'
      · have h := (mask_inter_empty (hb v)).mp (beq_iff_eq.mp he) w hw
        rw [hn, hAdj] at h
        contradiction

private def F3neighbors (v : Fin 15) : Nat :=
  #[14, 17, 257, 4097, 34, 208, 8224, 32, 516, 3328, 16896, 512, 8, 64, 1024][v.val]!

private theorem F3neighbors_bound : ∀ v, F3neighbors v < 2 ^ 15 := by decide +kernel

private theorem F3neighbors_adj :
    ∀ v w : Fin 15, (F3neighbors v).testBit w.val = F3.adj v w := by decide +kernel

private theorem F3_allMIS_masks :
    allMIS F3 =
      ((List.range (2 ^ 15)).filter (maskMIS F3neighbors)).map (maskSubset 15) := by
  unfold allMIS
  rw [allSubsets_masks, List.filter_map]
  have heq : isMaximalIndepSetB F3 ∘ maskSubset 15 = maskMIS F3neighbors := by
    funext k
    exact Bool.eq_iff_iff.mpr ((isMaximalIndepSetB_eq_true_iff F3 (maskSubset 15 k)).trans
      (maskMIS_spec F3 F3neighbors F3neighbors_bound F3neighbors_adj k).symm)
  rw [heq]

private theorem mask_singleton_zero (k i : Nat) :
    (k &&& 2 ^ i == 0) = !(k.testBit i) := by
  apply Bool.eq_iff_iff.mpr
  rw [beq_iff_eq, Bool.not_eq_true']
  constructor
  · intro h
    have he := congrArg (fun x : Nat => x.testBit i) h
    simpa only [Nat.testBit_and, Nat.testBit_two_pow_self, Bool.and_true, Nat.zero_testBit]
      using he
  · intro h
    apply Nat.eq_of_testBit_eq
    intro j
    by_cases hij : i = j
    · subst j
      simp [Nat.testBit_and, h]
    · simp [Nat.testBit_and, hij]

private theorem beq_not_eq_bne (a b : Bool) : (a == !b) = (a != b) := by
  cases a <;> cases b <;> rfl

private def F3fastMIS (k : Nat) : Bool :=
  k.testBit 7 != k.testBit 5 && k.testBit 11 != k.testBit 9 &&
  k.testBit 12 != k.testBit 3 && k.testBit 13 != k.testBit 6 && k.testBit 14 != k.testBit 10 &&
  [(0, 14), (1, 17), (2, 257), (3, 4097), (4, 34), (5, 208),
   (6, 8224), (8, 516), (9, 3328), (10, 16896)].all
    (fun (i, mask) => k.testBit i == (k &&& mask == 0))

private theorem F3_maskMIS_fast : maskMIS F3neighbors = F3fastMIS := by
  funext k
  change [(0, 14), (1, 17), (2, 257), (3, 4097), (4, 34), (5, 208),
      (6, 8224), (7, 32), (8, 516), (9, 3328), (10, 16896), (11, 512),
      (12, 8), (13, 64), (14, 1024)].all
      (fun (i, mask) => k.testBit i == (k &&& mask == 0)) = F3fastMIS k
  simp only [F3fastMIS, List.all_cons, List.all_nil]
  rw [show (k &&& 32 == 0) = _ from mask_singleton_zero k 5,
      show (k &&& 512 == 0) = _ from mask_singleton_zero k 9,
      show (k &&& 8 == 0) = _ from mask_singleton_zero k 3,
      show (k &&& 64 == 0) = _ from mask_singleton_zero k 6,
      show (k &&& 1024 == 0) = _ from mask_singleton_zero k 10]
  simp only [beq_not_eq_bne, Bool.and_true]
  ac_rfl

section
set_option maxRecDepth 8192
set_option maxHeartbeats 0

private def F3_maskBlock (start : Nat) : List Nat :=
  (List.range' start 1024).filter F3fastMIS

private theorem F3_block_0 : F3_maskBlock 0 = [] := by decide +kernel
private theorem F3_block_1 : F3_maskBlock 1024 = [] := by decide +kernel
private theorem F3_block_2 : F3_maskBlock 2048 = [] := by decide +kernel
private theorem F3_block_3 : F3_maskBlock 3072 = [3278, 3292, 3530, 3544] := by decide +kernel
private theorem F3_block_4 : F3_maskBlock 4096 = [] := by decide +kernel
private theorem F3_block_5 : F3_maskBlock 5120 = [] := by decide +kernel
private theorem F3_block_6 : F3_maskBlock 6144 = [] := by decide +kernel
private theorem F3_block_7 : F3_maskBlock 7168 = [7366, 7380, 7618, 7633] := by decide +kernel
private theorem F3_block_8 : F3_maskBlock 8192 = [] := by decide +kernel
private theorem F3_block_9 : F3_maskBlock 9216 = [] := by decide +kernel
private theorem F3_block_10 : F3_maskBlock 10240 = [] := by decide +kernel
private theorem F3_block_11 : F3_maskBlock 11264 = [11310, 11406, 11420, 11562, 11658, 11672] := by decide +kernel
private theorem F3_block_12 : F3_maskBlock 12288 = [] := by decide +kernel
private theorem F3_block_13 : F3_maskBlock 13312 = [] := by decide +kernel
private theorem F3_block_14 : F3_maskBlock 14336 = [] := by decide +kernel
private theorem F3_block_15 : F3_maskBlock 15360 = [15398, 15494, 15508, 15649, 15650, 15746, 15761] := by decide +kernel
private theorem F3_block_16 : F3_maskBlock 16384 = [17102, 17116] := by decide +kernel
private theorem F3_block_17 : F3_maskBlock 17408 = [] := by decide +kernel
private theorem F3_block_18 : F3_maskBlock 18432 = [18638, 18652, 18890, 18904] := by decide +kernel
private theorem F3_block_19 : F3_maskBlock 19456 = [] := by decide +kernel
private theorem F3_block_20 : F3_maskBlock 20480 = [21190, 21201, 21204] := by decide +kernel
private theorem F3_block_21 : F3_maskBlock 21504 = [] := by decide +kernel
private theorem F3_block_22 : F3_maskBlock 22528 = [22726, 22740, 22978, 22993] := by decide +kernel
private theorem F3_block_23 : F3_maskBlock 23552 = [] := by decide +kernel
private theorem F3_block_24 : F3_maskBlock 24576 = [25134, 25230, 25244] := by decide +kernel
private theorem F3_block_25 : F3_maskBlock 25600 = [] := by decide +kernel
private theorem F3_block_26 : F3_maskBlock 26624 = [26670, 26766, 26780, 26922, 27018, 27032] := by decide +kernel
private theorem F3_block_27 : F3_maskBlock 27648 = [] := by decide +kernel
private theorem F3_block_28 : F3_maskBlock 28672 = [29217, 29222, 29318, 29329, 29332] := by decide +kernel
private theorem F3_block_29 : F3_maskBlock 29696 = [] := by decide +kernel
private theorem F3_block_30 : F3_maskBlock 30720 = [30758, 30854, 30868, 31009, 31010, 31106, 31121] := by decide +kernel
private theorem F3_block_31 : F3_maskBlock 31744 = [] := by decide +kernel

private def F3_maskBlocks (start : Nat) : Nat → List Nat
  | 0 => []
  | m + 1 => F3_maskBlock start ++ F3_maskBlocks (start + 1024) m

private theorem F3_maskBlocks_correct (start m : Nat) :
    F3_maskBlocks start m = (List.range' start (1024 * m)).filter F3fastMIS := by
  induction m generalizing start with
  | zero => rfl
  | succ m ih =>
    have hm : 1024 * (m + 1) = 1024 + 1024 * m := by omega
    rw [F3_maskBlocks, ih, hm, ← List.range'_append_1, List.filter_append]
    rfl

private def F3_MIS_masks : List Nat :=
  [3278, 3292, 3530, 3544, 7366, 7380, 7618, 7633, 11310, 11406, 11420, 11562,
   11658, 11672, 15398, 15494, 15508, 15649, 15650, 15746, 15761, 17102, 17116, 18638,
   18652, 18890, 18904, 21190, 21201, 21204, 22726, 22740, 22978, 22993, 25134, 25230,
   25244, 26670, 26766, 26780, 26922, 27018, 27032, 29217, 29222, 29318, 29329, 29332,
   30758, 30854, 30868, 31009, 31010, 31106, 31121]

private theorem F3_joinBlock {start count : Nat} {here rest : List Nat}
    (h : F3_maskBlock start = here) (hs : F3_maskBlocks (start + 1024) count = rest) :
    F3_maskBlocks start (count + 1) = here ++ rest :=
  (congrArg (fun xs => xs ++ F3_maskBlocks (start + 1024) count) h).trans
    (congrArg (List.append here) hs)

private theorem F3_MIS_list : allMIS F3 = F3_MIS_masks.map (maskSubset 15) := by
  have blocks : F3_maskBlocks 0 32 = F3_MIS_masks :=
    F3_joinBlock F3_block_0
    (F3_joinBlock F3_block_1
    (F3_joinBlock F3_block_2
    (F3_joinBlock F3_block_3
    (F3_joinBlock F3_block_4
    (F3_joinBlock F3_block_5
    (F3_joinBlock F3_block_6
    (F3_joinBlock F3_block_7
    (F3_joinBlock F3_block_8
    (F3_joinBlock F3_block_9
    (F3_joinBlock F3_block_10
    (F3_joinBlock F3_block_11
    (F3_joinBlock F3_block_12
    (F3_joinBlock F3_block_13
    (F3_joinBlock F3_block_14
    (F3_joinBlock F3_block_15
    (F3_joinBlock F3_block_16
    (F3_joinBlock F3_block_17
    (F3_joinBlock F3_block_18
    (F3_joinBlock F3_block_19
    (F3_joinBlock F3_block_20
    (F3_joinBlock F3_block_21
    (F3_joinBlock F3_block_22
    (F3_joinBlock F3_block_23
    (F3_joinBlock F3_block_24
    (F3_joinBlock F3_block_25
    (F3_joinBlock F3_block_26
    (F3_joinBlock F3_block_27
    (F3_joinBlock F3_block_28
    (F3_joinBlock F3_block_29
    (F3_joinBlock F3_block_30
    (F3_joinBlock F3_block_31
    (show F3_maskBlocks 32768 0 = [] from rfl))))))))))))))))))))))))))))))))
  have fast : (List.range (2 ^ 15)).filter (maskMIS F3neighbors) =
      (List.range (2 ^ 15)).filter F3fastMIS :=
    congrArg (fun f => (List.range (2 ^ 15)).filter f) F3_maskMIS_fast
  have range : (List.range (2 ^ 15)).filter F3fastMIS =
      (List.range' 0 (1024 * 32)).filter F3fastMIS :=
    congrArg (List.filter F3fastMIS) (List.range_eq_range' (n := 2 ^ 15))
  exact F3_allMIS_masks.trans (congrArg (List.map (maskSubset 15))
    (fast.trans (range.trans ((F3_maskBlocks_correct 0 32).symm.trans blocks))))

private def F3target : Fin 15 → Bool := maskSubset 15 29217

private theorem F3_smallMask_check :
    F3_MIS_masks.filter (fun k => decide (setSize (maskSubset 15 k) ≤ 6)) = [29217] := by
  decide +kernel

private theorem F3_min_MIS :
    ((allMIS F3).filter (fun S => decide (setSize S ≤ 6))) = [F3target] :=
  (congrArg (List.filter (fun S : Fin 15 → Bool => decide (setSize S ≤ 6))) F3_MIS_list).trans
    (List.filter_map.trans (congrArg (List.map (maskSubset 15)) F3_smallMask_check))

theorem F3_static_counts : NstatTotal F3 = 55 ∧ NstatCountLe F3 6 = 1 :=
  ⟨congrArg List.length F3_MIS_list, congrArg List.length F3_min_MIS⟩

private theorem Nstat_eq_counts {n : Nat} (G : SimpleGraph n) (t a b : Nat)
    (hn : NstatCountLe G t = a) (hd : NstatTotal G = b) (hb : 0 < b) :
    QProb.Eq (Nstat G t) ⟨a, b, hb⟩ := by
  cases hn
  cases hd
  exact QProb.eq_refl _

theorem F3_Nstat : QProb.Eq (Nstat F3 6) ⟨1, 55, by decide⟩ :=
  Nstat_eq_counts F3 6 1 55 F3_static_counts.2 F3_static_counts.1 (by decide)

end

private theorem Nseq_of_singleton_min {n : Nat} (G : SimpleGraph n) (t : Nat)
    (S : Fin n → Bool) (hmin : (allMIS G).filter (fun J => decide (setSize J ≤ t)) = [S]) :
    QProb.Eq (Nseq G t) (NseqTarget G S) := by
  have hmem : S ∈ (allMIS G).filter (fun J => decide (setSize J ≤ t)) :=
    (congrArg (fun xs => S ∈ xs) hmin).symm.mp (List.mem_singleton.mpr rfl)
  obtain ⟨hM, hsize⟩ := List.mem_filter.mp hmem
  refine Nseq_of_unique_le G t S ((mem_allMIS_iff G S).mp hM)
    (of_decide_eq_true hsize) ?_
  intro J hJ hj
  have h : J ∈ (allMIS G).filter (fun T => decide (setSize T ≤ t)) :=
    List.mem_filter.mpr ⟨(mem_allMIS_iff G J).mpr hJ, decide_eq_true hj⟩
  exact List.mem_singleton.mp ((congrArg (fun xs => J ∈ xs) hmin).mp h)

private theorem F3_target_eq :
    QProb.Eq (Nseq F3 6) (NseqTarget F3 F3target) :=
  Nseq_of_singleton_min F3 6 F3target F3_min_MIS

private def F3maskGraph : SimpleGraph 15 where
  adj v w := (F3neighbors v).testBit w.val
  symm v w := by rw [F3neighbors_adj, F3neighbors_adj, F3.symm]
  loopless v := (F3neighbors_adj v v).trans (F3.loopless v)

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
private theorem F3_activeChance :
    QProb.Eq (targetOn F3maskGraph F3target 15 (finRange 15)) ⟨64, 3375, by decide⟩ := by
  unfold QProb.Eq
  decide +kernel

theorem F3_Nseq : QProb.Eq (Nseq F3 6) ⟨64, 3375, by decide⟩ :=
  QProb.eq_trans F3_target_eq (QProb.eq_trans (NseqTarget_eq_active F3 F3maskGraph F3target (finRange 15) 15 id
    (Nat.le_refl 15) (nodup_finRange _) (fun _ _ h => h)
    (fun v => ⟨fun _ => ⟨v, rfl⟩, fun _ => mem_finRange v⟩)
    (fun v w => (F3neighbors_adj v w).symm)) F3_activeChance)

theorem F3_cross_product :
    64 * 55 = 3520 ∧ 3375 < 64 * 55 ∧ 64 * 55 - 3375 = 145 := by decide

theorem F3_strict_violation : QProb.Lt (Nstat F3 6) (Nseq F3 6) :=
  @QProb.Lt_congr ⟨1, 55, by decide⟩ (Nstat F3 6) ⟨64, 3375, by decide⟩ (Nseq F3 6)
    (QProb.eq_symm F3_Nstat) (QProb.eq_symm F3_Nseq) (by unfold QProb.Lt; decide)

theorem conj52_disproof_F3 : ¬ Conjecture52 :=
  fun h => QProb.not_Le_of_Lt F3_strict_violation (h 15 F3 F3_maxDegreeLe3 6)

/-! ## The five-vertex-unit chain -/

/-- The unit at index `i` is numbered `L,h,R,a,b` at positions `5*i` through `5*i+4`.
Rooting at the first left leaf gives the bridge parent of each later left leaf. -/
private def chainParent (v : Nat) : Nat :=
  if v % 5 = 0 then v - 3
  else if v % 5 = 3 then v - 2
  else v - 1

private theorem chainParent_le (v : Nat) : chainParent v ≤ v := by
  unfold chainParent
  split <;> first | omega | split <;> omega

private theorem chainParent_lt {v : Nat} (hv : v ≠ 0) : chainParent v < v := by
  unfold chainParent
  split <;> first | omega | split <;> omega

def Fm (m : Nat) : SimpleGraph (5 * m) where
  adj u v := decide ((u.val ≠ 0 ∧ v.val = chainParent u.val) ∨
    (v.val ≠ 0 ∧ u.val = chainParent v.val))
  symm u v := by simp [or_comm]
  loopless v := by
    simp only [or_self, decide_eq_false_iff_not]
    exact fun ⟨h0, heq⟩ => (Nat.ne_of_lt (chainParent_lt h0)) heq.symm

private def chainDepth (v : Nat) : Nat :=
  3 * (v / 5) + if v % 5 = 3 then 2 else if v % 5 = 4 then 3 else v % 5

private theorem chainDepth_parent {v : Nat} (hv : v ≠ 0) :
    chainDepth v = chainDepth (chainParent v) + 1 := by
  unfold chainDepth chainParent
  repeat' split
  all_goals omega

theorem Fm_isTree (m : Nat) (hm : 0 < m) : IsTree (Fm m) := by
  let root : Fin (5 * m) := ⟨0, by omega⟩
  let parent (v : Fin (5 * m)) : Fin (5 * m) :=
    ⟨chainParent v.val, Nat.lt_of_le_of_lt (chainParent_le _) v.isLt⟩
  apply isTree_of_rootedParent (Fm m) root parent (fun v => chainDepth v.val)
  · change chainDepth 0 = 0
    decide
  · intro v hv
    have hv' : v.val ≠ 0 := fun h => hv (Fin.ext h)
    exact ⟨decide_eq_true (Or.inl ⟨hv', rfl⟩), chainDepth_parent hv'⟩
  · intro u v huv
    change decide ((u.val ≠ 0 ∧ v.val = chainParent u.val) ∨
      (v.val ≠ 0 ∧ u.val = chainParent v.val)) = true at huv
    rcases of_decide_eq_true huv with ⟨h0, hp⟩ | ⟨h0, hp⟩
    · exact Or.inl ⟨fun he => h0 (congrArg Fin.val he), Fin.ext hp,
        (chainDepth_parent h0).trans (congrArg (fun x => chainDepth x + 1) hp.symm)⟩
    · exact Or.inr ⟨fun he => h0 (congrArg Fin.val he), Fin.ext hp,
        (chainDepth_parent h0).trans (congrArg (fun x => chainDepth x + 1) hp.symm)⟩

theorem Fm_connected (m : Nat) (hm : 0 < m) : Connected (Fm m) := (Fm_isTree m hm).1

private def chainNeighbors (v : Nat) : List Nat :=
  if v % 5 = 0 then [v - 3, v + 1]
  else if v % 5 = 1 then [v - 1, v + 1, v + 2]
  else if v % 5 = 2 then [v - 1, v + 3]
  else if v % 5 = 3 then [v - 2, v + 1]
  else [v - 1]

private theorem chainNeighbors_len (v : Nat) : (chainNeighbors v).length ≤ 3 := by
  unfold chainNeighbors
  repeat' split
  all_goals simp

private theorem mem_chainNeighbors {u v : Nat}
    (h : (v ≠ 0 ∧ u = chainParent v) ∨ (u ≠ 0 ∧ v = chainParent u)) :
    u ∈ chainNeighbors v := by
  unfold chainNeighbors
  repeat' split
  all_goals simp only [List.mem_cons, List.not_mem_nil, or_false]
  all_goals rcases h with ⟨h0, hp⟩ | ⟨h0, hp⟩
  all_goals unfold chainParent at hp
  all_goals repeat' split at hp
  all_goals omega

theorem Fm_maxDegreeLe3 (m : Nat) : maxDegreeLe3 (Fm m) := by
  intro v
  let ns := (finRange (5 * m)).filter (fun u => (Fm m).adj v u)
  have hnd : (ns.map Fin.val).Nodup :=
    nodup_map_of_injOn (nodup_filter _ (nodup_finRange _)) (fun _ _ _ _ h => Fin.ext h)
  have hle := length_le_of_nodup_subset hnd (l2 := chainNeighbors v.val) (by
    intro w hw
    obtain ⟨u, hu, rfl⟩ := List.mem_map.mp hw
    exact mem_chainNeighbors (of_decide_eq_true (List.mem_filter.mp hu).2))
  rw [List.length_map] at hle
  exact Nat.le_trans hle (chainNeighbors_len _)

/-- The chain labeling of the supplied certificate, read from its first end leaf. -/
def F3_chain_iso : GraphIso (Fm 3) F3 where
  toFun v := #[7, 5, 4, 6, 13, 1, 0, 2, 3, 12, 8, 9, 11, 10, 14][v.val]!
  invFun v := #[6, 5, 7, 8, 2, 1, 3, 0, 10, 11, 13, 12, 9, 4, 14][v.val]!
  left_inv := by decide +kernel
  right_inv := by decide +kernel
  map_adj := by decide +kernel

/-! ## Exact finite controls -/

private theorem Nstat_eq_one_of_all_mis_le {n : Nat} (G : SimpleGraph n) (t : Nat)
    (hall : ∀ S : Fin n → Bool, IsMaximalIndepSet G S → setSize S ≤ t) :
    QProb.Eq (Nstat G t) QProb.one := by
  have hf : (allMIS G).filter (fun S => decide (setSize S ≤ t)) = allMIS G := by
    apply List.filter_eq_self.mpr
    intro S hS
    exact decide_eq_true (hall S ((mem_allMIS_iff G S).mp hS))
  change ((allMIS G).filter (fun S => decide (setSize S ≤ t))).length * 1 =
    1 * (allMIS G).length
  rw [hf, Nat.mul_one, Nat.one_mul]

private theorem dominates_of_finite_check {n : Nat} (G : SimpleGraph n) (b : Nat)
    (hbound : (allMIS G).all (fun S => decide (setSize S ≤ b)) = true)
    (hsmall : ∀ t : Fin b, SeqDominatesStatAt G t.val) : SeqDominatesStat G := by
  intro t
  by_cases ht : t < b
  · exact hsmall ⟨t, ht⟩
  · have hlarge : ∀ S : Fin n → Bool, IsMaximalIndepSet G S → setSize S ≤ t := by
      intro S hS
      have hs := List.all_eq_true.mp hbound S ((mem_allMIS_iff G S).mpr hS)
      exact Nat.le_trans (of_decide_eq_true hs) (Nat.le_of_not_lt ht)
    exact QProb.Le_congr
      (QProb.eq_symm (Nseq_eq_one_of_all_mis_le G t hlarge))
      (QProb.eq_symm (Nstat_eq_one_of_all_mis_le G t hlarge))
      (Nat.le_refl _)

def P3Graph : SimpleGraph 3 := graphOfEdges [(0, 1), (1, 2)]
def P4Graph : SimpleGraph 4 := graphOfEdges [(0, 1), (1, 2), (2, 3)]
def P5Graph : SimpleGraph 5 := graphOfEdges [(0, 1), (1, 2), (2, 3), (3, 4)]
def ClawGraph : SimpleGraph 4 := graphOfEdges [(0, 1), (0, 2), (0, 3)]

/-- The six-vertex maximum-degree-four graph in Section 5.2 of the paper. -/
def Deg4Control : SimpleGraph 6 :=
  graphOfEdges [(0, 1), (0, 2), (0, 3), (0, 4), (4, 5), (1, 2)]

set_option maxRecDepth 4096 in
theorem small_control_CDFs :
    QProb.Eq (Nseq P3Graph 1) ⟨1, 3, by decide⟩ ∧
    QProb.Eq (Nstat P3Graph 1) ⟨1, 2, by decide⟩ ∧
    QProb.Eq (Nseq P4Graph 2) QProb.one ∧
    QProb.Eq (Nstat P4Graph 2) QProb.one ∧
    QProb.Eq (Nseq P5Graph 2) ⟨8, 15, by decide⟩ ∧
    QProb.Eq (Nstat P5Graph 2) ⟨3, 4, by decide⟩ ∧
    QProb.Eq (Nseq ClawGraph 1) ⟨1, 4, by decide⟩ ∧
    QProb.Eq (Nstat ClawGraph 1) ⟨1, 2, by decide⟩ ∧
    QProb.Eq (Nseq (Fm 1) 2) ⟨4, 15, by decide⟩ ∧
    QProb.Eq (Nstat (Fm 1) 2) ⟨1, 3, by decide⟩ := by
  unfold QProb.Eq
  decide +kernel

theorem P3_control : maxDegreeLe3 P3Graph ∧ SeqDominatesStat P3Graph := by
  refine ⟨by unfold maxDegreeLe3; decide +kernel, dominates_of_finite_check P3Graph 2 ?_ ?_⟩
  · decide +kernel
  · unfold SeqDominatesStatAt QProb.Le
    decide +kernel

theorem P4_control : maxDegreeLe3 P4Graph ∧ SeqDominatesStat P4Graph := by
  refine ⟨by unfold maxDegreeLe3; decide +kernel, dominates_of_finite_check P4Graph 2 ?_ ?_⟩
  · decide +kernel
  · unfold SeqDominatesStatAt QProb.Le
    decide +kernel

theorem P5_control : maxDegreeLe3 P5Graph ∧ SeqDominatesStat P5Graph := by
  refine ⟨by unfold maxDegreeLe3; decide +kernel, dominates_of_finite_check P5Graph 3 ?_ ?_⟩
  · decide +kernel
  · unfold SeqDominatesStatAt QProb.Le
    decide +kernel

theorem Claw_control : maxDegreeLe3 ClawGraph ∧ SeqDominatesStat ClawGraph := by
  refine ⟨by unfold maxDegreeLe3; decide +kernel, dominates_of_finite_check ClawGraph 3 ?_ ?_⟩
  · decide +kernel
  · unfold SeqDominatesStatAt QProb.Le
    decide +kernel

theorem F1_control : maxDegreeLe3 (Fm 1) ∧ SeqDominatesStat (Fm 1) := by
  refine ⟨Fm_maxDegreeLe3 1, dominates_of_finite_check (Fm 1) 3 ?_ ?_⟩
  · decide +kernel
  · unfold SeqDominatesStatAt QProb.Le
    decide +kernel

set_option maxRecDepth 4096 in
set_option maxHeartbeats 0 in
theorem degree4_control :
    Deg4Control.degree 0 = 4 ∧ (∀ v, Deg4Control.degree v ≤ 4) ∧ ¬maxDegreeLe3 Deg4Control ∧
    QProb.Eq (Nseq Deg4Control 2) ⟨5, 24, by decide⟩ ∧
    QProb.Eq (Nstat Deg4Control 2) ⟨1, 5, by decide⟩ ∧
    ¬SeqDominatesStat Deg4Control := by
  have hd : Deg4Control.degree 0 = 4 := by decide +kernel
  have hs : QProb.Eq (Nseq Deg4Control 2) ⟨5, 24, by decide⟩ := by
    unfold QProb.Eq
    decide +kernel
  have ht : QProb.Eq (Nstat Deg4Control 2) ⟨1, 5, by decide⟩ := by
    unfold QProb.Eq
    decide +kernel
  refine ⟨hd, by decide +kernel, (fun h => ?_), hs, ht, fun h => ?_⟩
  · have hb := h 0
    omega
  · apply QProb.not_Le_of_Lt _ (h 2)
    exact QProb.Lt_congr (QProb.eq_symm ht) (QProb.eq_symm hs) (by unfold QProb.Lt; decide)

/-! ## The unique minimum maximal independent set of each chain -/

private def chainForward (x y : Nat) : Prop :=
  (y = x + 1 ∧ (x % 5 = 0 ∨ x % 5 = 1 ∨ x % 5 = 3)) ∨
  (y = x + 2 ∧ x % 5 = 1) ∨ (y = x + 3 ∧ x % 5 = 2)

private theorem chainForward_iff (x y : Nat) :
    chainForward x y ↔ y ≠ 0 ∧ x = chainParent y := by
  unfold chainForward chainParent
  repeat' split
  all_goals omega

private theorem Fm_adj_iff {m : Nat} (u v : Fin (5 * m)) :
    (Fm m).adj u v = true ↔ chainForward u.val v.val ∨ chainForward v.val u.val := by
  simp only [Fm, decide_eq_true_eq, chainForward_iff]
  exact or_comm

private def unitVertex {m : Nat} (i : Fin m) (r : Fin 5) : Fin (5 * m) :=
  ⟨5 * i.val + r.val, by have := i.isLt; have := r.isLt; omega⟩

private def leftSpare {m : Nat} (i : Fin m) : Fin (5 * m) :=
  ⟨5 * i.val - 3, by have := i.isLt; omega⟩

private def chainLeftPick {m : Nat} (S : Fin (5 * m) → Bool) (i : Fin m) : Fin (5 * m) :=
  if S (unitVertex i 1) then unitVertex i 1
  else if S (unitVertex i 0) then unitVertex i 0
  else leftSpare i

private def chainPendantPick {m : Nat} (S : Fin (5 * m) → Bool) (i : Fin m) : Fin (5 * m) :=
  if S (unitVertex i 3) then unitVertex i 3 else unitVertex i 4

private theorem leftPick_spec {m : Nat} {S : Fin (5 * m) → Bool}
    (hS : IsDominatingIndepSet (Fm m) S) (i : Fin m) :
    S (chainLeftPick S i) = true ∧
    ((chainLeftPick S i).val = 5 * i.val + 1 ∨ (chainLeftPick S i).val = 5 * i.val ∨
      (0 < i.val ∧ (chainLeftPick S i).val = 5 * i.val - 3)) := by
  by_cases hh : S (unitVertex i 1) = true
  · rw [chainLeftPick, ite_eq_left hh]
    exact ⟨hh, Or.inl rfl⟩
  · by_cases hl : S (unitVertex i 0) = true
    · rw [chainLeftPick, ite_eq_right hh, ite_eq_left hl]
      exact ⟨hl, Or.inr (Or.inl rfl)⟩
    · rcases hS.2 (unitVertex i 0) with h | ⟨u, hu, ha⟩
      · exact False.elim (hl h)
      · have he := (Fm_adj_iff _ _).mp ha
        change chainForward (5*i.val) u.val ∨ chainForward u.val (5*i.val) at he
        unfold chainForward at he
        have hloc : u.val = 5 * i.val + 1 ∨
            (0 < i.val ∧ u.val = 5 * i.val - 3) := by
          omega
        rcases hloc with ht | ⟨hpos, ht⟩
        · have heq : u = unitVertex i 1 := Fin.ext ht
          exact False.elim (hh (heq ▸ hu))
        · have heq : u = leftSpare i := Fin.ext ht
          rw [chainLeftPick, ite_eq_right hh, ite_eq_right hl]
          exact ⟨heq ▸ hu, Or.inr (Or.inr ⟨hpos, rfl⟩)⟩

private theorem pendantPick_spec {m : Nat} {S : Fin (5 * m) → Bool}
    (hS : IsDominatingIndepSet (Fm m) S) (i : Fin m) :
    S (chainPendantPick S i) = true ∧
    ((chainPendantPick S i).val = 5 * i.val + 3 ∨
      (chainPendantPick S i).val = 5 * i.val + 4) := by
  by_cases ha : S (unitVertex i 3) = true
  · rw [chainPendantPick, ite_eq_left ha]
    exact ⟨ha, Or.inl rfl⟩
  · have hb : S (unitVertex i 4) = true := by
      rcases hS.2 (unitVertex i 4) with h | ⟨u, hu, huw⟩
      · exact h
      · have he := (Fm_adj_iff _ _).mp huw
        change chainForward (5*i.val+4) u.val ∨ chainForward u.val (5*i.val+4) at he
        unfold chainForward at he
        have heq : u = unitVertex i 3 := Fin.ext (by
          change u.val = 5 * i.val + 3
          omega)
        exact False.elim (ha (heq ▸ hu))
    rw [chainPendantPick, ite_eq_right ha]
    exact ⟨hb, Or.inr rfl⟩

private def chainPicks {m : Nat} (S : Fin (5 * m) → Bool) : List (Fin (5 * m)) :=
  (finRange m).map (chainLeftPick S) ++ (finRange m).map (chainPendantPick S)

private theorem chainPicks_length {m : Nat} (S : Fin (5 * m) → Bool) :
    (chainPicks S).length = 2 * m := by
  simp [chainPicks, length_finRange]
  omega

private theorem chainPicks_mem {m : Nat} {S : Fin (5 * m) → Bool}
    (hS : IsDominatingIndepSet (Fm m) S) {v : Fin (5 * m)} (hv : v ∈ chainPicks S) :
    S v = true := by
  rcases List.mem_append.mp hv with h | h
  · obtain ⟨i, _, rfl⟩ := List.mem_map.mp h
    exact (leftPick_spec hS i).1
  · obtain ⟨i, _, rfl⟩ := List.mem_map.mp h
    exact (pendantPick_spec hS i).1

private theorem chainPicks_nodup {m : Nat} {S : Fin (5 * m) → Bool}
    (hS : IsDominatingIndepSet (Fm m) S) : (chainPicks S).Nodup := by
  unfold chainPicks
  apply List.nodup_append.mpr
  refine ⟨?_, ?_, ?_⟩
  · apply nodup_map_of_injOn (nodup_finRange m)
    intro i _ j _ h
    have he := congrArg Fin.val h
    exact Fin.ext (by
      have hi := (leftPick_spec hS i).2
      have hj := (leftPick_spec hS j).2
      omega)
  · apply nodup_map_of_injOn (nodup_finRange m)
    intro i _ j _ h
    have he := congrArg Fin.val h
    exact Fin.ext (by
      have hi := (pendantPick_spec hS i).2
      have hj := (pendantPick_spec hS j).2
      omega)
  · intro u hu v hv heq
    obtain ⟨i, _, rfl⟩ := List.mem_map.mp hu
    obtain ⟨j, _, rfl⟩ := List.mem_map.mp hv
    have he := congrArg Fin.val heq
    have hi := (leftPick_spec hS i).2
    have hj := (pendantPick_spec hS j).2
    omega

private theorem chainPicks_cover {m : Nat} {S : Fin (5 * m) → Bool}
    (hS : IsDominatingIndepSet (Fm m) S) (hle : setSize S ≤ 2 * m) {v : Fin (5 * m)}
    (hv : S v = true) : v ∈ chainPicks S := by
  by_cases hm : v ∈ chainPicks S
  · exact hm
  · have hnd : (v :: chainPicks S).Nodup :=
      List.Pairwise.cons (fun x hx h => hm (h ▸ hx)) (chainPicks_nodup hS)
    have hh := length_le_of_nodup_subset hnd
      (l2 := (finRange (5*m)).filter S) (by
        intro u hu
        rcases List.mem_cons.mp hu with rfl | hu
        · exact List.mem_filter.mpr ⟨mem_finRange _, hv⟩
        · exact List.mem_filter.mpr ⟨mem_finRange u, chainPicks_mem hS hu⟩)
    have hlen := chainPicks_length S
    change (chainPicks S).length + 1 ≤ setSize S at hh
    omega

private theorem allHubs_of_min {m : Nat} {S : Fin (5 * m) → Bool}
    (hS : IsDominatingIndepSet (Fm m) S) (hle : setSize S ≤ 2 * m) (i : Fin m) :
    S (unitVertex i 1) = true := by
  suffices h : ∀ d, ∀ i : Fin m, m - i.val ≤ d → S (unitVertex i 1) = true from h _ i (Nat.le_refl _)
  intro d
  induction d with
  | zero =>
    intro i hi
    have := i.isLt
    omega
  | succ d ih =>
    intro i hi
    by_cases hh : S (unitVertex i 1) = true
    · exact hh
    · exfalso
      have hnext : ∀ j : Fin m, j.val = i.val + 1 → S (unitVertex j 1) = true := by
        intro j hj
        exact ih j (by have := i.isLt; have := j.isLt; omega)
      have hr : S (unitVertex i 2) = true := by
        rcases hS.2 (unitVertex i 2) with h | ⟨u, hu, hadj⟩
        · exact h
        · have he := (Fm_adj_iff _ _).mp hadj
          change chainForward (5*i.val+2) u.val ∨ chainForward u.val (5*i.val+2) at he
          unfold chainForward at he
          have hloc : u.val = 5 * i.val + 1 ∨ u.val = 5 * (i.val + 1) := by omega
          rcases hloc with h | h
          · have heq : u = unitVertex i 1 := Fin.ext h
            exact False.elim (hh (heq ▸ hu))
          · let j : Fin m := ⟨i.val + 1, by have := u.isLt; omega⟩
            have heq : u = unitVertex j 0 := Fin.ext (by simpa [unitVertex, j] using h)
            have adj : (Fm m).adj (unitVertex j 0) (unitVertex j 1) = true := by
              apply (Fm_adj_iff _ _).mpr
              left
              simp [chainForward, unitVertex]
            have hbad := hS.1 _ _ (heq ▸ hu) (hnext j rfl)
            rw [adj] at hbad
            cases hbad
      have hc := chainPicks_cover hS hle hr
      rcases List.mem_append.mp hc with hc | hc
      · obtain ⟨j, _, hj⟩ := List.mem_map.mp hc
        have he := congrArg Fin.val hj
        change (chainLeftPick S j).val = 5 * i.val + 2 at he
        have hj' := (leftPick_spec hS j).2
        have hsucc : j.val = i.val + 1 := by omega
        have hsel := hnext j hsucc
        rw [chainLeftPick, ite_eq_left hsel] at he
        change 5 * j.val + 1 = 5 * i.val + 2 at he
        omega
      · obtain ⟨j, _, hj⟩ := List.mem_map.mp hc
        have he := congrArg Fin.val hj
        change (chainPendantPick S j).val = 5 * i.val + 2 at he
        have hj' := (pendantPick_spec hS j).2
        omega

def chainTarget {m : Nat} (v : Fin (5 * m)) : Bool :=
  decide (v.val % 5 = 1 ∨ v.val % 5 = 4)

private theorem chainTarget_independent (m : Nat) : IsIndepSet (Fm m) chainTarget := by
  intro u v hu hv
  apply Bool.eq_false_iff.mpr
  intro h
  have hu' := of_decide_eq_true hu
  have hv' := of_decide_eq_true hv
  have he := (Fm_adj_iff _ _).mp h
  unfold chainForward at he
  omega

theorem chainTarget_isMIS (m : Nat) : IsMaximalIndepSet (Fm m) chainTarget := by
  rw [isMaximalIndepSet_iff_dominating]
  refine ⟨chainTarget_independent m, fun v => ?_⟩
  by_cases hv : v.val % 5 = 1 ∨ v.val % 5 = 4
  · exact Or.inl (decide_eq_true hv)
  · right
    have hb := v.isLt
    by_cases hr : v.val % 5 = 2
    · let w : Fin (5*m) := ⟨v.val - 1, by omega⟩
      refine ⟨w, decide_eq_true (Or.inl (by change (v.val - 1) % 5 = 1; omega)), ?_⟩
      apply (Fm_adj_iff _ _).mpr
      right
      change chainForward (v.val - 1) v.val
      unfold chainForward
      omega
    · let w : Fin (5*m) := ⟨v.val + 1, by omega⟩
      refine ⟨w, decide_eq_true (by change (v.val + 1) % 5 = 1 ∨ (v.val + 1) % 5 = 4; omega), ?_⟩
      apply (Fm_adj_iff _ _).mpr
      left
      change chainForward v.val (v.val + 1)
      unfold chainForward
      omega

private theorem chainTarget_unique_of_hubs {m : Nat} {S : Fin (5*m) → Bool}
    (hS : IsMaximalIndepSet (Fm m) S) (hubs : ∀ i : Fin m, S (unitVertex i 1) = true) :
    S = chainTarget := by
  have hinc : ∀ v, chainTarget v = true → S v = true := by
    intro v hv
    have hb := v.isLt
    let i : Fin m := ⟨v.val / 5, by omega⟩
    rcases of_decide_eq_true hv with hr | hr
    · have heq : v = unitVertex i 1 := Fin.ext (by change v.val = 5 * (v.val / 5) + 1; omega)
      rw [heq]
      exact hubs i
    · have heq : v = unitVertex i 4 := Fin.ext (by change v.val = 5 * (v.val / 5) + 4; omega)
      rw [heq]
      have hd := (isMaximalIndepSet_iff_dominating _ _).mp hS
      have ha : (Fm m).adj (unitVertex i 1) (unitVertex i 3) = true := by
        apply (Fm_adj_iff _ _).mpr
        left
        change chainForward (5*i.val+1) (5*i.val+3)
        unfold chainForward
        omega
      have hna : S (unitVertex i 3) ≠ true := by
        intro hs
        have hbad := hd.1 _ _ (hubs i) hs
        rw [ha] at hbad
        cases hbad
      have h := (pendantPick_spec hd i).1
      simpa [chainPendantPick, hna] using h
  exact (chainTarget_isMIS m).2 S hS.1 hinc

theorem chainTarget_size (m : Nat) : setSize (chainTarget (m := m)) = 2 * m := by
  have hd := (isMaximalIndepSet_iff_dominating _ _).mp (chainTarget_isMIS m)
  have hiff : ∀ v, v ∈ (finRange (5*m)).filter (chainTarget (m := m)) ↔
      v ∈ chainPicks (chainTarget (m := m)) := by
    intro v
    constructor
    · intro h
      have hv : chainTarget v = true := (List.mem_filter.mp h).2
      have hb := v.isLt
      let i : Fin m := ⟨v.val / 5, by omega⟩
      rcases of_decide_eq_true hv with hr | hr
      · apply List.mem_append_left
        apply List.mem_map.mpr
        refine ⟨i, mem_finRange i, Fin.ext ?_⟩
        simp [chainLeftPick, chainTarget, unitVertex]
        change 5 * (v.val / 5) + 1 = v.val
        omega
      · apply List.mem_append_right
        apply List.mem_map.mpr
        refine ⟨i, mem_finRange i, Fin.ext ?_⟩
        simp [chainPendantPick, chainTarget, unitVertex]
        change 5 * (v.val / 5) + 4 = v.val
        omega
    · intro h
      exact List.mem_filter.mpr ⟨mem_finRange v, chainPicks_mem hd h⟩
  exact (length_eq_of_nodup_iff (nodup_filter _ (nodup_finRange _))
    (chainPicks_nodup hd) hiff).trans (chainPicks_length _)

theorem Fm_unique_min (m : Nat) {S : Fin (5*m) → Bool}
    (hS : IsMaximalIndepSet (Fm m) S) (ht : setSize S ≤ 2 * m) : S = chainTarget :=
  chainTarget_unique_of_hubs hS
    (allHubs_of_min ((isMaximalIndepSet_iff_dominating _ _).mp hS) ht)

theorem Fm_static_min (m : Nat) : NstatCountLe (Fm m) (2*m) = 1 := by
  let l := (allMIS (Fm m)).filter (fun S => decide (setSize S ≤ 2*m))
  have hl : l.Nodup := nodup_filter _ (nodup_allMIS _)
  have hmem : ∀ S, S ∈ l ↔ S ∈ [chainTarget (m := m)] := by
    intro S
    rw [List.mem_singleton]
    constructor
    · intro h
      obtain ⟨hm, hs⟩ := List.mem_filter.mp h
      exact Fm_unique_min m ((mem_allMIS_iff _ S).mp hm) (of_decide_eq_true hs)
    · rintro rfl
      exact List.mem_filter.mpr
        ⟨(mem_allMIS_iff _ _).mpr (chainTarget_isMIS m), decide_eq_true (by rw [chainTarget_size]; exact Nat.le_refl _)⟩
  exact length_eq_of_nodup_iff hl (by simp) hmem

section

set_option maxRecDepth 4096

private theorem F2_count : NstatTotal (Fm 2) = 13 := by decide +kernel

private theorem F2_ceiling : (allMIS (Fm 2)).all (fun S => decide (setSize S ≤ 5)) = true := by
  decide +kernel

private theorem F2_activeChance :
    QProb.Eq (targetOn (Fm 2) chainTarget 10 (finRange 10)) ⟨16, 225, by decide⟩ := by
  unfold QProb.Eq
  decide +kernel

theorem F2_control_CDFs :
    QProb.Eq (Nseq (Fm 2) 4) ⟨16, 225, by decide⟩ ∧
    QProb.Eq (Nstat (Fm 2) 4) ⟨1, 13, by decide⟩ := by
  have hs := Nseq_of_unique_le (Fm 2) 4 chainTarget (chainTarget_isMIS 2)
    (show setSize (chainTarget (m := 2)) ≤ 4 from Nat.le_of_eq (chainTarget_size 2))
    (fun _ hM hsize => Fm_unique_min 2 hM hsize)
  have hcalc := NseqTarget_eq_full_active (Fm 2) chainTarget
  exact ⟨QProb.eq_trans hs (QProb.eq_trans hcalc F2_activeChance),
    Nstat_eq_counts (Fm 2) 4 1 13 (Fm_static_min 2) F2_count (by decide)⟩

theorem F2_control : maxDegreeLe3 (Fm 2) ∧ SeqDominatesStat (Fm 2) := by
  refine ⟨Fm_maxDegreeLe3 2, dominates_of_finite_check (Fm 2) 5 F2_ceiling ?_⟩
  intro t
  by_cases ht : t.val = 4
  · rw [ht]
    exact QProb.Le_congr (QProb.eq_symm F2_control_CDFs.1)
      (QProb.eq_symm F2_control_CDFs.2) (by unfold QProb.Le; decide)
  · have hlt : t.val < 4 := by have := t.isLt; omega
    have hzero : QProb.Eq (Nseq (Fm 2) t.val) QProb.zero := by
      apply Nseq_eq_zero_of_all_mis_gt
      intro S hS
      by_cases hsmall : setSize S ≤ 4
      · rw [Fm_unique_min 2 hS hsmall, chainTarget_size]
        exact hlt
      · omega
    exact QProb.Le_congr (QProb.eq_symm hzero) (QProb.eq_refl _)
      (Nat.zero_le _)

end

/-! ## The exact sequential probability for every chain -/

private def unitVertices {m : Nat} (i : Fin m) : List (Fin (5*m)) :=
  (finRange 5).map (unitVertex i)

private theorem unitVertices_mem {m : Nat} (i : Fin m) (v : Fin (5*m)) :
    v ∈ unitVertices i ↔ ∃ r : Fin 5, unitVertex i r = v := by
  rw [unitVertices, List.mem_map]
  exact ⟨fun ⟨r, _, h⟩ => ⟨r, h⟩, fun ⟨r, h⟩ => ⟨r, mem_finRange r, h⟩⟩

private theorem unitVertices_length {m : Nat} (i : Fin m) : (unitVertices i).length = 5 := rfl

private theorem unitVertices_nodup {m : Nat} (i : Fin m) : (unitVertices i).Nodup := by
  apply nodup_map_of_injOn (nodup_finRange 5)
  intro a _ b _ h
  have he := congrArg Fin.val h
  change 5*i.val+a.val = 5*i.val+b.val at he
  exact Fin.ext (by omega)

private def chainLive {m : Nat} (is : List (Fin m)) : List (Fin (5*m)) :=
  is.flatMap unitVertices

private theorem chainLive_length {m : Nat} (is : List (Fin m)) :
    (chainLive is).length = 5 * is.length := by
  induction is with
  | nil => rfl
  | cons i is ih =>
    change (unitVertices i ++ chainLive is).length = _
    rw [List.length_append, ih, unitVertices_length, List.length_cons]
    omega

private theorem units_separate {m : Nat} {i j : Fin m} (hij : i ≠ j)
    {v w : Fin (5*m)} (hv : v ∈ unitVertices i) (hw : w ∈ unitVertices j) :
    v ≠ w ∧ (chainTarget v = true ∨ chainTarget w = true → (Fm m).adj v w = false) := by
  obtain ⟨a, rfl⟩ := (unitVertices_mem i v).mp hv
  obtain ⟨b, rfl⟩ := (unitVertices_mem j w).mp hw
  have ha := a.isLt
  have hb := b.isLt
  have hn : i.val ≠ j.val := fun h => hij (Fin.ext h)
  constructor
  · intro h
    have he := congrArg Fin.val h
    change 5*i.val+a.val = 5*j.val+b.val at he
    omega
  · intro hS
    apply Bool.eq_false_iff.mpr
    intro hadj
    have h := (Fm_adj_iff _ _).mp hadj
    change chainForward (5*i.val+a.val) (5*j.val+b.val) ∨
      chainForward (5*j.val+b.val) (5*i.val+a.val) at h
    unfold chainForward at h
    rcases hS with hv | hw
    · have hs := of_decide_eq_true hv
      change (5*i.val+a.val)%5 = 1 ∨ (5*i.val+a.val)%5 = 4 at hs
      omega
    · have hs := of_decide_eq_true hw
      change (5*j.val+b.val)%5 = 1 ∨ (5*j.val+b.val)%5 = 4 at hs
      omega

private theorem chainLive_nodup {m : Nat} {is : List (Fin m)} (h : is.Nodup) :
    (chainLive is).Nodup := by
  induction is with
  | nil => exact List.Pairwise.nil
  | cons i is ih =>
    obtain ⟨hi, htail⟩ := List.nodup_cons.mp h
    change (unitVertices i ++ chainLive is).Nodup
    apply List.nodup_append.mpr
    refine ⟨unitVertices_nodup i, ih htail, ?_⟩
    intro v hv w hw
    obtain ⟨j, hj, hwj⟩ := List.mem_flatMap.mp hw
    exact (units_separate (i := i) (j := j) (fun he => hi (he.symm ▸ hj)) hv hwj).1

private theorem chainForward_shift (i : Nat) (a b : Fin 5) :
    chainForward a.val b.val ↔ chainForward (5*i+a.val) (5*i+b.val) := by
  have ha := a.isLt
  have hb := b.isLt
  unfold chainForward
  omega

private theorem unit_adj {m : Nat} (i : Fin m) (a b : Fin 5) :
    (Fm 1).adj a b = (Fm m).adj (unitVertex i a) (unitVertex i b) :=
  Bool.eq_iff_iff.mpr ((Fm_adj_iff (m := 1) a b).trans
    ((or_congr (chainForward_shift i.val a b) (chainForward_shift i.val b a)).trans
      (Fm_adj_iff (unitVertex i a) (unitVertex i b)).symm))

private theorem unit_target {m : Nat} (i : Fin m) :
    (chainTarget (m := m) ∘ unitVertex i) = chainTarget (m := 1) := by
  funext r
  apply Bool.eq_iff_iff.mpr
  simp only [Function.comp_apply, chainTarget, decide_eq_true_eq]
  change ((5*i.val+r.val)%5 = 1 ∨ (5*i.val+r.val)%5 = 4) ↔
    (r.val%5 = 1 ∨ r.val%5 = 4)
  omega

private theorem F1_targetChance :
    QProb.Eq (NseqTarget (Fm 1) chainTarget) ⟨4, 15, by decide⟩ := by
  apply QProb.eq_trans (NseqTarget_eq_full_active (Fm 1) chainTarget)
  unfold QProb.Eq
  decide +kernel

private theorem unit_prob {m : Nat} (i : Fin m) :
    activeProb (Fm m) chainTarget 5 (unitVertices i) = (4 : Int) /. (15 : Int) := by
  have h := NseqTarget_eq_active (Fm 1) (Fm m) chainTarget (unitVertices i) 5
    (unitVertex i) (Nat.le_refl 5) (unitVertices_nodup i)
    (fun a b h => Fin.ext (by
      have he := congrArg Fin.val h
      change 5*i.val+a.val = 5*i.val+b.val at he
      omega))
    (unitVertices_mem i) (unit_adj i)
  rw [unit_target i] at h
  exact (QProb.eq_iff_asRat _ _).mp (QProb.eq_trans (QProb.eq_symm h) F1_targetChance)

private theorem chainLive_prob {m : Nat} (is : List (Fin m)) (hnd : is.Nodup)
    (fuel : Nat) (hf : 5 * is.length ≤ fuel) :
    activeProb (Fm m) chainTarget fuel (chainLive is) = ((4 : Int) /. (15 : Int)) ^ is.length := by
  induction is generalizing fuel with
  | nil => simp [chainLive, activeProb_nil]
  | cons i is ih =>
    obtain ⟨hi, htail⟩ := List.nodup_cons.mp hnd
    change activeProb (Fm m) chainTarget fuel (unitVertices i ++ chainLive is) = _
    rw [activeProb_append (Fm m) chainTarget fuel (unitVertices i) (chainLive is)
        5 (5 * is.length)]
    · rw [unit_prob i, ih htail _ (Nat.le_refl _), List.length_cons, Rat.pow_succ]
      exact Rat.mul_comm _ _
    · rw [unitVertices_length, chainLive_length]
      simp only [List.length_cons] at hf
      omega
    · exact Nat.le_refl _
    · rw [chainLive_length]
      exact Nat.le_refl _
    · intro v hv w hw
      obtain ⟨j, hj, hwj⟩ := List.mem_flatMap.mp hw
      exact units_separate (i := i) (j := j) (fun he => hi (he.symm ▸ hj)) hv hwj

private theorem rat_chainPower (m : Nat) :
    ((4 : Int) /. (15 : Int)) ^ m = ((4 ^ m : Nat) : Int) /. ((15 ^ m : Nat) : Int) := by
  induction m with
  | zero => decide
  | succ m ih =>
    rw [Rat.pow_succ, ih, Rat.divInt_mul_divInt, Nat.pow_succ, Nat.pow_succ,
      Int.natCast_mul, Int.natCast_mul]
    rfl

theorem Fm_Nseq (m : Nat) :
    QProb.Eq (Nseq (Fm m) (2*m)) ⟨4 ^ m, 15 ^ m, Nat.pow_pos (by decide)⟩ := by
  have hsize : setSize (chainTarget (m := m)) ≤ 2*m := Nat.le_of_eq (chainTarget_size m)
  have ht := Nseq_of_unique_le (Fm m) (2*m) chainTarget (chainTarget_isMIS m) hsize
    (fun _ h hs => Fm_unique_min m h hs)
  have hlive : ∀ v : Fin (5*m), v ∈ chainLive (finRange m) ↔ ∃ i : Fin (5*m), id i = v := by
    intro v
    constructor
    · intro _
      exact ⟨v, rfl⟩
    · intro _
      have hv := v.isLt
      let i : Fin m := ⟨v.val / 5, by omega⟩
      apply List.mem_flatMap.mpr
      refine ⟨i, mem_finRange i, (unitVertices_mem i v).mpr ⟨⟨v.val % 5, by omega⟩, Fin.ext ?_⟩⟩
      change 5 * (v.val / 5) + v.val % 5 = v.val
      omega
  have hd := NseqTarget_eq_active (Fm m) (Fm m) chainTarget (chainLive (finRange m)) (5*m) id
    (Nat.le_refl _) (chainLive_nodup (nodup_finRange m)) (fun _ _ h => h) hlive (fun _ _ => rfl)
  apply QProb.eq_trans ht (QProb.eq_trans hd _)
  apply (QProb.eq_iff_asRat _ _).mpr
  change activeProb (Fm m) chainTarget (5*m) (chainLive (finRange m)) = _
  rw [chainLive_prob (finRange m) (nodup_finRange m) _ (by rw [length_finRange]; exact Nat.le_refl _),
    length_finRange, rat_chainPower]
  rfl

/-! ## Transfer counts and the exact integer comparison -/

/-- Counts of completions starting with bridge states `00`, `10`, and `01`.
The empty suffix accepts the first two states, in which its absent left leaf is unselected. -/
def chainTransfer : Nat → Nat × Nat × Nat
  | 0 => (1, 1, 0)
  | m + 1 =>
    let (x, y, z) := chainTransfer m
    (x + z, x + 2*y + 2*z, 2*y + 2*z)

/-- The two initial states have an unselected exterior vertex on the left. -/
def misCountFm (m : Nat) : Nat := (chainTransfer m).1 + (chainTransfer m).2.2

theorem misCountFm_recurrence (m : Nat) :
    misCountFm (m + 3) + 4 * misCountFm (m + 1) =
      5 * misCountFm (m + 2) + 2 * misCountFm m := by
  unfold misCountFm
  simp only [chainTransfer]
  cases h : chainTransfer m with
  | mk x yz =>
    obtain ⟨y, z⟩ := yz
    dsimp
    omega

theorem misCountFm_initial :
    misCountFm 0 = 1 ∧ misCountFm 1 = 3 ∧ misCountFm 2 = 13 ∧ misCountFm 3 = 55 :=
  by decide

theorem misCountFm_growth (m : Nat) :
    4 * misCountFm (m + 1) < misCountFm (m + 2) := by
  induction m with
  | zero => decide
  | succ m ih =>
    have h := misCountFm_recurrence m
    change 4 * misCountFm (m + 2) < misCountFm (m + 3)
    omega

theorem Fm_cross_product (m : Nat) (hm : 3 ≤ m) :
    15 ^ m < 4 ^ m * misCountFm m := by
  obtain ⟨j, rfl⟩ : ∃ j, m = j + 3 := ⟨m - 3, by omega⟩
  clear hm
  induction j with
  | zero => decide
  | succ j ih =>
    have hg := misCountFm_growth (j + 2)
    have ha : j + 1 + 3 = (j + 3) + 1 := by omega
    rw [ha, Nat.pow_succ, Nat.pow_succ]
    have hp : 0 < 4 ^ (j + 3) := Nat.pow_pos (by decide)
    calc
      15 ^ (j + 3) * 15 < (4 ^ (j + 3) * misCountFm (j + 3)) * 15 :=
        Nat.mul_lt_mul_of_pos_right ih (by decide)
      _ ≤ (4 ^ (j + 3) * misCountFm (j + 3)) * 16 :=
        Nat.mul_le_mul_left _ (by decide)
      _ = (4 ^ (j + 3) * 4) * (4 * misCountFm (j + 3)) := by
        rw [← show 4 * 4 = 16 by decide]
        ac_rfl
      _ < (4 ^ (j + 3) * 4) * misCountFm ((j + 3) + 1) :=
        Nat.mul_lt_mul_of_pos_left hg (Nat.mul_pos hp (by decide))

/-! ## Counting maximal independent sets by the two ends of a bridge -/

private abbrev UnitWord := Fin 5 → Bool

private def wordAt (ws : List UnitWord) (i : Nat) : UnitWord :=
  (ws[i]?).getD (fun _ => false)

private def wordFront (ws : List UnitWord) : Bool := wordAt ws 0 0

/-- Each vertex is selected exactly when none of its neighbors is selected.
The arguments `p` and `q` give the states of the exterior neighbors of the leaves. -/
private def unitOK (p : Bool) (w : UnitWord) (q : Bool) : Bool :=
  (w 0 == !(w 1 || p)) &&
  (w 1 == !(w 0 || w 2 || w 3)) &&
  (w 2 == !(w 1 || q)) &&
  (w 3 == !(w 1 || w 4)) &&
  (w 4 == !w 3)

private def wordsOK (p : Bool) : List UnitWord → Bool
  | [] => true
  | w :: ws => unitOK p w (wordFront ws) && wordsOK (w 2) ws

private theorem wordsOK_index (p : Bool) (ws : List UnitWord) :
    wordsOK p ws = true ↔ ∀ i : Nat, i < ws.length →
      unitOK (if i = 0 then p else wordAt ws (i-1) 2)
        (wordAt ws i) (wordAt ws (i+1) 0) = true := by
  induction ws generalizing p with
  | nil => simp [wordsOK]
  | cons w ws ih =>
    rw [wordsOK, Bool.and_eq_true, ih]
    constructor
    · rintro ⟨hhead, htail⟩ i hi
      cases i with
      | zero => simpa [wordAt, wordFront] using hhead
      | succ i =>
        have hi' : i < ws.length := Nat.lt_of_succ_lt_succ hi
        have h := htail i hi'
        cases i <;> simpa [wordAt] using h
    · intro h
      refine ⟨?_, ?_⟩
      · simpa [wordAt, wordFront] using h 0 (by simp)
      · intro i hi
        have hh := h (i+1) (Nat.succ_lt_succ hi)
        cases i <;> simpa [wordAt] using hh

private def unitChoices (p l : Bool) : List (UnitWord × Bool) :=
  ((allSubsets 5).flatMap fun w => [(w, false), (w, true)]).filter
    (fun (w, q) => (w 0 == l) && unitOK p w q)

private theorem unitChoices_mem (p l : Bool) (w : UnitWord) (q : Bool) :
    (w,q) ∈ unitChoices p l ↔ w 0 = l ∧ unitOK p w q = true := by
  unfold unitChoices
  have hw : (w,q) ∈ (allSubsets 5).flatMap (fun w => [(w,false),(w,true)]) := by
    apply List.mem_flatMap.mpr
    refine ⟨w, mem_allSubsets w, ?_⟩
    cases q <;> simp
  simp only [List.mem_filter, hw, true_and, Bool.and_eq_true, beq_iff_eq]

private theorem unitChoices_nodup (p l : Bool) : (unitChoices p l).Nodup := by
  apply nodup_filter
  apply List.pairwise_flatMap.mpr
  refine ⟨fun w _ => by simp, ?_⟩
  apply (nodup_allSubsets 5).imp
  intro w v h x hx y hy heq
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hx hy
  rcases hx with rfl | rfl <;> rcases hy with rfl | rfl <;> exact h (congrArg Prod.fst heq)

private def wordRows : Nat → Bool → Bool → List (List UnitWord)
  | 0, _, l => if l then [] else [[]]
  | m + 1, p, l =>
    (unitChoices p l).flatMap fun (w,q) =>
      (wordRows m (w 2) q).map (w :: ·)

private theorem wordRows_mem (m : Nat) (p l : Bool) (ws : List UnitWord) :
    ws ∈ wordRows m p l ↔ ws.length = m ∧ wordFront ws = l ∧ wordsOK p ws = true := by
  induction m generalizing p l ws with
  | zero =>
    cases ws <;> cases l <;> simp [wordRows, wordFront, wordAt, wordsOK]
  | succ m ih =>
    rw [wordRows, List.mem_flatMap]
    constructor
    · rintro ⟨⟨w,q⟩, hw, hm⟩
      obtain ⟨ys, hy, rfl⟩ := List.mem_map.mp hm
      obtain ⟨hlen, hfront, hok⟩ := (ih _ _ _).mp hy
      obtain ⟨hl, hcheck⟩ := (unitChoices_mem p l w q).mp hw
      exact ⟨congrArg Nat.succ hlen, hl, by
        simp only [wordsOK, hfront, hcheck, hok, Bool.and_self]⟩
    · rintro ⟨hlen, hfront, hok⟩
      cases ws with
      | nil => simp at hlen
      | cons w ys =>
        rw [wordsOK, Bool.and_eq_true] at hok
        obtain ⟨hh, ht⟩ := hok
        refine ⟨(w,wordFront ys), (unitChoices_mem _ _ _ _).mpr ⟨hfront,hh⟩, ?_⟩
        exact List.mem_map.mpr ⟨ys, (ih _ _ _).mpr ⟨Nat.succ.inj hlen, rfl, ht⟩, rfl⟩

private theorem wordRows_nodup (m : Nat) (p l : Bool) : (wordRows m p l).Nodup := by
  induction m generalizing p l with
  | zero => cases l <;> simp [wordRows]
  | succ m ih =>
    apply List.pairwise_flatMap.mpr
    constructor
    · rintro ⟨w,q⟩ _
      exact nodup_map_of_injOn (ih _ _) (fun _ _ _ _ he => (List.cons.inj he).2)
    · apply (unitChoices_nodup p l).imp
      rintro ⟨w,q⟩ ⟨v,r⟩ h xs hx ys hy he
      obtain ⟨xs', hx', rfl⟩ := List.mem_map.mp hx
      obtain ⟨ys', hy', rfl⟩ := List.mem_map.mp hy
      obtain ⟨rfl,rfl⟩ := List.cons.inj he
      have hq := ((wordRows_mem _ _ _ _).mp hx').2.1
      have hr := ((wordRows_mem _ _ _ _).mp hy').2.1
      exact h (congrArg (Prod.mk w) (hq.symm.trans hr))

private def allChainWords (m : Nat) : List (List UnitWord) :=
  wordRows m false false ++ wordRows m false true

private theorem allChainWords_mem (m : Nat) (ws : List UnitWord) :
    ws ∈ allChainWords m ↔ ws.length = m ∧ wordsOK false ws = true := by
  simp only [allChainWords, List.mem_append, wordRows_mem]
  constructor
  · rintro (⟨a,_,b⟩ | ⟨a,_,b⟩) <;> exact ⟨a,b⟩
  · rintro ⟨h1,h2⟩
    cases wordFront ws
    · exact Or.inl ⟨h1,rfl,h2⟩
    · exact Or.inr ⟨h1,rfl,h2⟩

private theorem allChainWords_nodup (m : Nat) : (allChainWords m).Nodup := by
  apply List.nodup_append.mpr
  refine ⟨wordRows_nodup _ _ _, wordRows_nodup _ _ _, ?_⟩
  intro x hx y hy he
  have h0 := ((wordRows_mem _ _ _ _).mp hx).2.1
  have h1 := ((wordRows_mem _ _ _ _).mp hy).2.1
  rw [he,h1] at h0
  contradiction

private def nextBridgeStates (p l : Bool) : List (Bool × Bool) :=
  (unitChoices p l).map (fun (w,q) => (w 2,q))

private theorem nextBridgeStates00 :
    nextBridgeStates false false = [(false,false),(false,true)] := by decide +kernel
private theorem nextBridgeStates10 :
    nextBridgeStates true false =
      [(false,true),(true,false),(false,false),(false,true),(true,false)] := by decide +kernel
private theorem nextBridgeStates01 :
    nextBridgeStates false true =
      [(false,true),(true,false),(false,true),(true,false)] := by decide +kernel

private theorem wordRows_length_succ (m : Nat) (p l : Bool) :
    (wordRows (m+1) p l).length =
      ((nextBridgeStates p l).map (fun (p',l') => (wordRows m p' l').length)).sum := by
  rw [wordRows, List.length_flatMap, nextBridgeStates, List.map_map]
  congr 1
  apply List.map_congr_left
  rintro ⟨w,q⟩ _
  exact List.length_map _

private theorem wordRows_length (m : Nat) :
    (wordRows m false false).length = (chainTransfer m).1 ∧
    (wordRows m true false).length = (chainTransfer m).2.1 ∧
    (wordRows m false true).length = (chainTransfer m).2.2 := by
  induction m with
  | zero => decide
  | succ m ih =>
    obtain ⟨hx,hy,hz⟩ := ih
    rw [wordRows_length_succ, wordRows_length_succ, wordRows_length_succ,
      nextBridgeStates00, nextBridgeStates10, nextBridgeStates01]
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, hx, hy, hz, chainTransfer]
    cases h : chainTransfer m with
    | mk a bc =>
      obtain ⟨b, c⟩ := bc
      dsimp
      omega

private theorem allChainWords_length (m : Nat) : (allChainWords m).length = misCountFm m := by
  simp only [allChainWords, List.length_append, (wordRows_length m).1, (wordRows_length m).2.2, misCountFm]

private def wordsOf {m : Nat} (S : Fin (5*m) → Bool) : List UnitWord :=
  List.ofFn (fun i : Fin m => S ∘ unitVertex i)

private theorem wordsOf_length {m : Nat} (S : Fin (5*m) → Bool) : (wordsOf S).length = m :=
  List.length_ofFn

private theorem wordAt_wordsOf {m : Nat} (S : Fin (5*m) → Bool) (i : Fin m) (r : Fin 5) :
    wordAt (wordsOf S) i.val r = S (unitVertex i r) := by
  simp [wordAt, wordsOf, i.isLt]

private theorem wordAt_outside {m : Nat} (S : Fin (5*m) → Bool) (i : Nat) (hi : ¬ i < m) (r : Fin 5) :
    wordAt (wordsOf S) i r = false := by
  simp [wordAt, wordsOf, hi]

private theorem wordsOf_inj {m : Nat} {S T : Fin (5*m) → Bool}
    (h : wordsOf S = wordsOf T) : S = T := by
  funext v
  have hb := v.isLt
  let i : Fin m := ⟨v.val / 5, by omega⟩
  let r : Fin 5 := ⟨v.val % 5, by omega⟩
  have heq : v = unitVertex i r := Fin.ext (by
    change v.val = 5*(v.val/5) + v.val%5
    omega)
  rw [heq, ← wordAt_wordsOf S, ← wordAt_wordsOf T, h]

private theorem wordsOf_surj {m : Nat} (ws : List UnitWord) (hlen : ws.length = m) :
    ∃ S : Fin (5*m) → Bool, wordsOf S = ws := by
  let S (v : Fin (5*m)) : Bool :=
    wordAt ws (v.val/5) ⟨v.val%5, by omega⟩
  refine ⟨S, ?_⟩
  apply List.ext_getElem
  · exact (wordsOf_length S).trans hlen.symm
  · intro i hi hw
    have him : i < m := by rwa [wordsOf_length] at hi
    have hget := List.getElem_ofFn (f := fun j : Fin m => S ∘ unitVertex j) (i := i)
      (by simpa only [List.length_ofFn] using him)
    refine hget.trans ?_
    funext r
    have hr := r.isLt
    change wordAt ws ((5*i + r.val)/5) ⟨(5*i+r.val)%5, _⟩ = ws[i] r
    have ha : (5*i+r.val)/5 = i := by omega
    have hb : (⟨(5*i+r.val)%5, by omega⟩ : Fin 5) = r := Fin.ext (by
      change (5*i+r.val)%5 = r.val
      omega)
    rw [ha, hb]
    simp [wordAt, List.getElem?_eq_getElem hw]

private def unitSideNeighbors {m : Nat} (i : Fin m) (r : Nat) : List (Fin (5*m)) :=
  match r with
  | 0 => unitVertex i 1 :: (if h : 0 < i.val then [unitVertex ⟨i.val-1, by omega⟩ 2] else [])
  | 1 => [unitVertex i 0, unitVertex i 2, unitVertex i 3]
  | 2 => unitVertex i 1 :: (if h : i.val+1 < m then [unitVertex ⟨i.val+1, h⟩ 0] else [])
  | 3 => [unitVertex i 1, unitVertex i 4]
  | _ => [unitVertex i 3]

private theorem unitSideNeighbors_spec {m : Nat} (i : Fin m) (r : Fin 5) (v : Fin (5*m)) :
    v ∈ unitSideNeighbors i r.val ↔ (Fm m).adj (unitVertex i r) v = true := by
  rw [Fm_adj_iff]
  change v ∈ unitSideNeighbors i r.val ↔
    chainForward (5*i.val+r.val) v.val ∨ chainForward v.val (5*i.val+r.val)
  have hl := i.isLt
  have hu := v.isLt
  have hr : r.val = 0 ∨ r.val = 1 ∨ r.val = 2 ∨ r.val = 3 ∨ r.val = 4 := by
    have := r.isLt
    omega
  rcases hr with (hr | hr | hr | hr | hr) <;>
    by_cases hp : 0 < i.val <;> by_cases hq : i.val + 1 < m <;>
    simp [hr, unitSideNeighbors, hp, hq, Fin.ext_iff, unitVertex, chainForward] <;> omega

private theorem unitNeighborRule {m : Nat} (S : Fin (5*m) → Bool) :
    IsMaximalIndepSet (Fm m) S ↔ ∀ i : Fin m, ∀ r : Fin 5,
        S (unitVertex i r) = !(List.any (unitSideNeighbors i r.val) S) := by
  rw [isMaximalIndepSet_iff_dominating]
  constructor
  · rintro ⟨hind,hdom⟩ i r
    cases h : S (unitVertex i r) with
    | false =>
      have hn : (unitSideNeighbors i r.val).any S = true := by
        rcases hdom (unitVertex i r) with hs | ⟨w,hw,ha⟩
        · rw [h] at hs
          contradiction
        · exact List.any_eq_true.mpr ⟨w, (unitSideNeighbors_spec i r w).mpr ha, hw⟩
      rw [hn]
      rfl
    | true =>
      have hn : (unitSideNeighbors i r.val).any S = false := by
        apply Bool.eq_false_iff.mpr
        rintro hn
        obtain ⟨w,hw,hs⟩ := List.any_eq_true.mp hn
        have he := hind _ w h hs
        rw [(unitSideNeighbors_spec i r w).mp hw] at he
        contradiction
      rw [hn]
      rfl
  · intro h
    have localRule (v : Fin (5*m)) :
        ∃ i : Fin m, ∃ r : Fin 5, v = unitVertex i r ∧
          S v = !(List.any (unitSideNeighbors i r.val) S) := by
      have hv := v.isLt
      let i : Fin m := ⟨v.val/5, by omega⟩
      let r : Fin 5 := ⟨v.val%5, by omega⟩
      have he : v = unitVertex i r := Fin.ext (by
        change v.val = 5*(v.val/5)+v.val%5
        omega)
      exact ⟨i,r,he,he.symm ▸ h i r⟩
    constructor
    · intro v w hv hw
      apply Bool.eq_false_iff.mpr
      intro hAdj
      obtain ⟨i,r,rfl,he⟩ := localRule v
      have hm := (unitSideNeighbors_spec i r w).mpr hAdj
      rw [List.any_eq_true.mpr ⟨w,hm,hw⟩, hv] at he
      contradiction
    · intro v
      obtain ⟨i,r,rfl,he⟩ := localRule v
      cases hv : S (unitVertex i r)
      · rw [hv] at he
        have ha : (unitSideNeighbors i r.val).any S = true := by
          cases h : (unitSideNeighbors i r.val).any S
          · rw [h] at he
            contradiction
          · rfl
        obtain ⟨w,hw,hs⟩ := List.any_eq_true.mp ha
        exact Or.inr ⟨w,hs,(unitSideNeighbors_spec i r w).mp hw⟩
      · exact Or.inl rfl

private theorem forall_fin_five (p : Fin 5 → Prop) :
    (∀ r, p r) ↔ p 0 ∧ p 1 ∧ p 2 ∧ p 3 ∧ p 4 := by
  refine ⟨fun h => ⟨h 0,h 1,h 2,h 3,h 4⟩, ?_⟩
  rintro ⟨h0,h1,h2,h3,h4⟩ r
  have hr : r.val = 0 ∨ r.val = 1 ∨ r.val = 2 ∨ r.val = 3 ∨ r.val = 4 := by
    have := r.isLt
    omega
  rcases hr with (hr | hr | hr | hr | hr)
  · exact (Fin.ext hr : r = 0).symm ▸ h0
  · exact (Fin.ext hr : r = 1).symm ▸ h1
  · exact (Fin.ext hr : r = 2).symm ▸ h2
  · exact (Fin.ext hr : r = 3).symm ▸ h3
  · exact (Fin.ext hr : r = 4).symm ▸ h4

private theorem wordsOf_mis {m : Nat} (S : Fin (5*m) → Bool) :
    wordsOK false (wordsOf S) = true ↔ IsMaximalIndepSet (Fm m) S := by
  rw [wordsOK_index, wordsOf_length, unitNeighborRule]
  have check (i : Fin m) :
      unitOK (if i.val = 0 then false else wordAt (wordsOf S) (i.val-1) 2)
        (wordAt (wordsOf S) i.val) (wordAt (wordsOf S) (i.val+1) 0) = true ↔
        ∀ r : Fin 5, S (unitVertex i r) = !(List.any (unitSideNeighbors i r.val) S) := by
    rw [forall_fin_five]
    have hp : (if i.val = 0 then false else wordAt (wordsOf S) (i.val-1) 2) =
        (if h : 0 < i.val then S (unitVertex ⟨i.val-1, by omega⟩ 2) else false) := by
      by_cases h : i.val = 0
      · simp [h]
      · have hp : 0 < i.val := by omega
        simp only [ite_eq_right h, dite_eq_left hp]
        exact wordAt_wordsOf S ⟨i.val-1, by omega⟩ 2
    have hq : wordAt (wordsOf S) (i.val+1) 0 =
        (if h : i.val+1 < m then S (unitVertex ⟨i.val+1,h⟩ 0) else false) := by
      by_cases h : i.val+1 < m
      · rw [dite_eq_left h]
        exact wordAt_wordsOf S ⟨i.val+1,h⟩ 0
      · rw [dite_eq_right h]
        exact wordAt_outside S _ h _
    rw [hp,hq]
    simp only [unitOK, Bool.and_eq_true, beq_iff_eq, wordAt_wordsOf, and_assoc]
    change _ ↔
      S (unitVertex i 0) = !(List.any (unitSideNeighbors i 0) S) ∧
      S (unitVertex i 1) = !(List.any (unitSideNeighbors i 1) S) ∧
      S (unitVertex i 2) = !(List.any (unitSideNeighbors i 2) S) ∧
      S (unitVertex i 3) = !(List.any (unitSideNeighbors i 3) S) ∧
      S (unitVertex i 4) = !(List.any (unitSideNeighbors i 4) S)
    by_cases hp : 0 < i.val <;> by_cases hq : i.val+1 < m <;>
      simp [unitSideNeighbors, hp, hq, Bool.or_assoc]
  exact ⟨fun h i => (check i).mp (h i.val i.isLt),
    fun h i hi => (check ⟨i, hi⟩).mpr (h ⟨i,hi⟩)⟩

theorem Fm_static_total (m : Nat) : NstatTotal (Fm m) = misCountFm m := by
  have hnd : ((allMIS (Fm m)).map wordsOf).Nodup :=
    nodup_map_of_injOn (nodup_allMIS _) (fun _ _ _ _ h => wordsOf_inj h)
  have hm : ∀ ws, ws ∈ (allMIS (Fm m)).map wordsOf ↔ ws ∈ allChainWords m := by
    intro ws
    rw [List.mem_map,allChainWords_mem]
    constructor
    · rintro ⟨S,hS,rfl⟩
      exact ⟨wordsOf_length _, (wordsOf_mis _).mpr ((mem_allMIS_iff _ _).mp hS)⟩
    · rintro ⟨hL,hS⟩
      obtain ⟨S,rfl⟩ := wordsOf_surj ws hL
      exact ⟨S,(mem_allMIS_iff _ _).mpr ((wordsOf_mis _).mp hS),rfl⟩
  have h := length_eq_of_nodup_iff hnd (allChainWords_nodup m) hm
  rw [List.length_map] at h
  exact h.trans (allChainWords_length m)

theorem Fm_Nstat (m : Nat) :
    QProb.Eq (Nstat (Fm m) (2*m)) ⟨1, misCountFm m, (Fm_static_total m) ▸ NstatTotal_pos (G := Fm m)⟩ :=
  Nstat_eq_counts _ _ _ _ (Fm_static_min m) (Fm_static_total m) _

theorem infinite_family_Fm_disproof (m : Nat) (hm : 3 ≤ m) :
    IsTree (Fm m) ∧ maxDegreeLe3 (Fm m) ∧
    QProb.Lt (Nstat (Fm m) (2*m)) (Nseq (Fm m) (2*m)) ∧ ¬SeqDominatesStat (Fm m) := by
  have hv : QProb.Lt (Nstat (Fm m) (2*m)) (Nseq (Fm m) (2*m)) :=
    QProb.Lt_congr (QProb.eq_symm (Fm_Nstat m)) (QProb.eq_symm (Fm_Nseq m))
      (show 1 * 15^m < 4^m * misCountFm m from
        (Nat.one_mul (15^m)).symm ▸ Fm_cross_product m hm)
  exact ⟨Fm_isTree m (by omega), Fm_maxDegreeLe3 m, hv, fun h => QProb.not_Le_of_Lt hv (h (2*m))⟩

end SubcubicConj52

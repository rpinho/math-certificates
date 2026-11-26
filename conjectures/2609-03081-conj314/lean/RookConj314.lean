import Lean.Elab.Tactic.Basic
import Lean.Elab.Tactic.Cbv
import Lean.Meta.LitValues
import Lean.ToExpr
import Std.Data.HashMap

set_option Elab.async false

/-
  RookConj314.lean
  Standalone Lean 4.36.0 (zero Mathlib) formalization of the disproof of
  Joel Brewster Lewis and Robert Won (arXiv:2609.03081v1), Conjecture 3.14
  (conj:maxlayered) at n = 17 and n = 18.
-/

namespace RookConj314

/-! ## Section 0: Conditional Helpers (Warning-Free in Lean 4.36.0) -/

theorem ite_pos {c : Prop} [inst : Decidable c] {α : Sort u} {t e : α} (h : c) :
    (if c then t else e) = t := by
  cases inst with
  | isTrue _ => rfl
  | isFalse hn => exact absurd h hn

theorem ite_neg {c : Prop} [inst : Decidable c] {α : Sort u} {t e : α} (h : ¬c) :
    (if c then t else e) = e := by
  cases inst with
  | isTrue hp => exact absurd hp h
  | isFalse _ => rfl

theorem dite_pos {c : Prop} [inst : Decidable c] {α : Sort u} {t : c → α} {e : ¬c → α} (h : c) :
    (if hc : c then t hc else e hc) = t h := by
  cases inst with
  | isTrue _ => rfl
  | isFalse hn => exact absurd h hn

theorem dite_neg {c : Prop} [inst : Decidable c] {α : Sort u} {t : c → α} {e : ¬c → α} (h : ¬c) :
    (if hc : c then t hc else e hc) = e h := by
  cases inst with
  | isTrue hp => exact absurd hp h
  | isFalse _ => rfl

/-! ## Section 1: Explicit Bijections and Exact Finite Cardinality -/

/-- Explicit two-sided bijection between two types. -/
structure Equiv (α : Type u) (β : Type v) where
  toFun : α → β
  invFun : β → α
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ y, toFun (invFun y) = y

infixl:25 " ≃ " => Equiv

namespace Equiv

def refl (α : Type u) : α ≃ α where
  toFun x := x
  invFun x := x
  left_inv _ := rfl
  right_inv _ := rfl

def symm (e : α ≃ β) : β ≃ α where
  toFun := e.invFun
  invFun := e.toFun
  left_inv := e.right_inv
  right_inv := e.left_inv

def trans (e₁ : α ≃ β) (e₂ : β ≃ γ) : α ≃ γ where
  toFun x := e₂.toFun (e₁.toFun x)
  invFun z := e₁.invFun (e₂.invFun z)
  left_inv x := by rw [e₂.left_inv, e₁.left_inv]
  right_inv z := by rw [e₁.right_inv, e₂.right_inv]

theorem injective (e : α ≃ β) {x y : α} (h : e.toFun x = e.toFun y) : x = y := by
  have h' := congrArg e.invFun h
  rw [e.left_inv, e.left_inv] at h'
  exact h'

def sumCongr (e₁ : α₁ ≃ β₁) (e₂ : α₂ ≃ β₂) : (α₁ ⊕ α₂) ≃ (β₁ ⊕ β₂) where
  toFun
    | .inl a => .inl (e₁.toFun a)
    | .inr b => .inr (e₂.toFun b)
  invFun
    | .inl a => .inl (e₁.invFun a)
    | .inr b => .inr (e₂.invFun b)
  left_inv
    | .inl a => congrArg Sum.inl (e₁.left_inv a)
    | .inr b => congrArg Sum.inr (e₂.left_inv b)
  right_inv
    | .inl a => congrArg Sum.inl (e₁.right_inv a)
    | .inr b => congrArg Sum.inr (e₂.right_inv b)

def prodCongr (e₁ : α₁ ≃ β₁) (e₂ : α₂ ≃ β₂) : (α₁ × α₂) ≃ (β₁ × β₂) where
  toFun p := (e₁.toFun p.1, e₂.toFun p.2)
  invFun p := (e₁.invFun p.1, e₂.invFun p.2)
  left_inv p := by cases p; simp [e₁.left_inv, e₂.left_inv]
  right_inv p := by cases p; simp [e₁.right_inv, e₂.right_inv]

def sigmaCongrRight {α : Type u} {β γ : α → Type v} (e : ∀ a, β a ≃ γ a) :
    ((a : α) × β a) ≃ ((a : α) × γ a) where
  toFun p := ⟨p.1, (e p.1).toFun p.2⟩
  invFun p := ⟨p.1, (e p.1).invFun p.2⟩
  left_inv p := by cases p; simp [(e _).left_inv]
  right_inv p := by cases p; simp [(e _).right_inv]

end Equiv

/-- Type `α` has exact finite cardinality `n` iff there is a bijection `α ≃ Fin n`. -/
def HasExactCard (α : Type) (n : Nat) : Prop := Nonempty (α ≃ Fin n)

/-- Swap two elements of `Fin n`. -/
def finSwap {n : Nat} (a b : Fin n) : Fin n ≃ Fin n where
  toFun x := if x = a then b else if x = b then a else x
  invFun x := if x = a then b else if x = b then a else x
  left_inv x := by
    by_cases hxa : x = a
    · rw [ite_pos hxa]
      by_cases hba : b = a
      · rw [ite_pos hba, hxa, hba]
      · rw [ite_neg hba, ite_pos rfl, hxa]
    · rw [ite_neg hxa]
      by_cases hxb : x = b
      · rw [ite_pos hxb, ite_pos rfl, hxb]
      · rw [ite_neg hxb, ite_neg hxa, ite_neg hxb]
  right_inv x := by
    by_cases hxa : x = a
    · rw [ite_pos hxa]
      by_cases hba : b = a
      · rw [ite_pos hba, hxa, hba]
      · rw [ite_neg hba, ite_pos rfl, hxa]
    · rw [ite_neg hxa]
      by_cases hxb : x = b
      · rw [ite_pos hxb, ite_pos rfl, hxb]
      · rw [ite_neg hxb, ite_neg hxa, ite_neg hxb]

/-- Pigeonhole / cardinality uniqueness: `Fin m ≃ Fin n` implies `m = n`. -/
theorem finEquivUnique : ∀ {m n : Nat}, (Fin m ≃ Fin n) → m = n
  | 0, 0, _ => rfl
  | 0, _ + 1, e => nomatch e.invFun ⟨0, by omega⟩
  | _ + 1, 0, e => nomatch e.toFun ⟨0, by omega⟩
  | m + 1, n + 1, e => by
    let lastM : Fin (m + 1) := ⟨m, by omega⟩
    let lastN : Fin (n + 1) := ⟨n, by omega⟩
    let e' : Fin (m + 1) ≃ Fin (n + 1) := e.trans (finSwap (e.toFun lastM) lastN)
    have hlast : e'.toFun lastM = lastN := by
      dsimp [e', Equiv.trans, finSwap]
      rw [ite_pos rfl]
    have hinvLast : e'.invFun lastN = lastM := by
      rw [← hlast, e'.left_inv]
    have hToLt : ∀ i : Fin m, (e'.toFun ⟨i.val, by omega⟩).val < n := by
      intro i
      have hne : e'.toFun ⟨i.val, by omega⟩ ≠ lastN := by
        intro heq
        rw [← hlast] at heq
        have hi := e'.injective heq
        have hval := congrArg Fin.val hi
        dsimp [lastM] at hval
        omega
      have hlt := (e'.toFun ⟨i.val, by omega⟩).isLt
      have hvalNe : (e'.toFun ⟨i.val, by omega⟩).val ≠ n := fun hv => hne (Fin.ext hv)
      omega
    have hInvLt : ∀ j : Fin n, (e'.invFun ⟨j.val, by omega⟩).val < m := by
      intro j
      have hne : e'.invFun ⟨j.val, by omega⟩ ≠ lastM := by
        intro heq
        rw [← hinvLast] at heq
        have hj := e'.symm.injective heq
        have hval := congrArg Fin.val hj
        dsimp [lastN] at hval
        omega
      have hlt := (e'.invFun ⟨j.val, by omega⟩).isLt
      have hvalNe : (e'.invFun ⟨j.val, by omega⟩).val ≠ m := fun hv => hne (Fin.ext hv)
      omega
    let res : Fin m ≃ Fin n := {
      toFun := fun i => ⟨(e'.toFun ⟨i.val, by omega⟩).val, hToLt i⟩
      invFun := fun j => ⟨(e'.invFun ⟨j.val, by omega⟩).val, hInvLt j⟩
      left_inv := fun i => by
        apply Fin.ext
        dsimp
        exact congrArg Fin.val (e'.left_inv ⟨i.val, by omega⟩)
      right_inv := fun j => by
        apply Fin.ext
        dsimp
        exact congrArg Fin.val (e'.right_inv ⟨j.val, by omega⟩)
    }
    exact congrArg (· + 1) (finEquivUnique res)

theorem hasExactCard_unique {α : Type} {m n : Nat}
    (hm : HasExactCard α m) (hn : HasExactCard α n) : m = n := by
  rcases hm with ⟨em⟩
  rcases hn with ⟨en⟩
  exact finEquivUnique (em.symm.trans en)

/-- Canonical bijection `Fin m ⊕ Fin n ≃ Fin (m + n)`. -/
def finSumEquiv (m n : Nat) : (Fin m ⊕ Fin n) ≃ Fin (m + n) where
  toFun
    | .inl i => ⟨i.val, by omega⟩
    | .inr j => ⟨m + j.val, by omega⟩
  invFun k :=
    if h : k.val < m then .inl ⟨k.val, h⟩
    else .inr ⟨k.val - m, by omega⟩
  left_inv
    | .inl i => by
      dsimp
      rw [dite_pos i.isLt]
    | .inr j => by
      dsimp
      have hnot : ¬ (m + j.val < m) := by omega
      rw [dite_neg hnot]
      congr 1
      apply Fin.ext
      dsimp
      omega
  right_inv k := by
    by_cases h : k.val < m
    · rw [dite_pos h]
    · rw [dite_neg h]
      apply Fin.ext
      dsimp
      omega

theorem mul_add_lt {m n a b : Nat} (ha : a < m) (hb : b < n) : a * n + b < m * n := by
  have h1 : a + 1 ≤ m := by omega
  have h2 : (a + 1) * n ≤ m * n := Nat.mul_le_mul_right n h1
  have h3 : (a + 1) * n = a * n + n := Nat.succ_mul a n
  omega

theorem mul_add_div_right (a b : Nat) {n : Nat} (hb : b < n) : (a * n + b) / n = a := by
  have hn : 0 < n := by omega
  rw [Nat.add_comm (a * n) b, Nat.mul_comm a n, Nat.add_mul_div_left b a hn]
  have hdiv : b / n = 0 := Nat.div_eq_of_lt hb
  omega

theorem mul_add_mod_right (a b : Nat) {n : Nat} (hb : b < n) : (a * n + b) % n = b := by
  rw [Nat.add_comm (a * n) b, Nat.mul_comm a n, Nat.add_mul_mod_self_left]
  exact Nat.mod_eq_of_lt hb

/-- Canonical bijection `Fin m × Fin n ≃ Fin (m * n)`. -/
def finProdEquiv (m : Nat) : (n : Nat) → (Fin m × Fin n) ≃ Fin (m * n)
  | 0 => {
      toFun := fun p => nomatch p.2
      invFun := fun k => nomatch k
      left_inv := fun p => nomatch p.2
      right_inv := fun k => nomatch k
    }
  | n + 1 => {
      toFun := fun p => ⟨p.1.val * (n + 1) + p.2.val, mul_add_lt p.1.isLt p.2.isLt⟩
      invFun := fun k =>
        have hdiv : k.val / (n + 1) < m := by
          by_cases hlt : k.val / (n + 1) < m
          · exact hlt
          · exfalso
            have hge : m ≤ k.val / (n + 1) := by omega
            have hmul : m * (n + 1) ≤ (k.val / (n + 1)) * (n + 1) := Nat.mul_le_mul_right (n + 1) hge
            have hdm := Nat.div_add_mod k.val (n + 1)
            rw [Nat.mul_comm (n + 1) (k.val / (n + 1))] at hdm
            have hk := k.isLt
            omega
        (⟨k.val / (n + 1), hdiv⟩, ⟨k.val % (n + 1), Nat.mod_lt k.val (by omega)⟩)
      left_inv := fun ⟨a, b⟩ => by
        apply Prod.ext
        · apply Fin.ext; exact mul_add_div_right a.val b.val b.isLt
        · apply Fin.ext; exact mul_add_mod_right a.val b.val b.isLt
      right_inv := fun k => by
        apply Fin.ext
        dsimp
        have hdm := Nat.div_add_mod k.val (n + 1)
        rw [Nat.mul_comm (k.val / (n + 1)) (n + 1)]
        exact hdm
    }

/-- Sum of `f i` for `i : Fin k`. -/
def finSum : (k : Nat) → (Fin k → Nat) → Nat
  | 0, _ => 0
  | k + 1, f => f ⟨0, Nat.zero_lt_succ k⟩ + finSum k (fun i => f ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)

/-- Split sigma over `Fin (k + 1)` by pattern-matching `0` vs `j + 1`. -/
def sigmaFinSuccSplit (k : Nat) (β : Fin (k + 1) → Type) :
    ((i : Fin (k + 1)) × β i) ≃ (β ⟨0, Nat.zero_lt_succ k⟩ ⊕ ((j : Fin k) × β ⟨j.val + 1, Nat.succ_lt_succ j.isLt⟩)) where
  toFun
    | ⟨⟨0, _⟩, x⟩ => .inl x
    | ⟨⟨v + 1, hv⟩, x⟩ => .inr ⟨⟨v, Nat.lt_of_succ_lt_succ hv⟩, x⟩
  invFun
    | .inl x => ⟨⟨0, Nat.zero_lt_succ k⟩, x⟩
    | .inr ⟨⟨v, hv⟩, y⟩ => ⟨⟨v + 1, Nat.succ_lt_succ hv⟩, y⟩
  left_inv
    | ⟨⟨0, _⟩, _⟩ => rfl
    | ⟨⟨_ + 1, _⟩, _⟩ => rfl
  right_inv
    | .inl _ => rfl
    | .inr ⟨⟨_, _⟩, _⟩ => rfl

/-- Canonical bijection `((i : Fin k) × Fin (f i)) ≃ Fin (finSum k f)`. -/
def finSigmaEquiv : (k : Nat) → (f : Fin k → Nat) → (((i : Fin k) × Fin (f i)) ≃ Fin (finSum k f))
  | 0, _ => {
      toFun := fun p => nomatch p.1
      invFun := fun z => nomatch z
      left_inv := fun p => nomatch p.1
      right_inv := fun z => nomatch z
    }
  | k + 1, f =>
    let f' : Fin k → Nat := fun j => f ⟨j.val + 1, Nat.succ_lt_succ j.isLt⟩
    (sigmaFinSuccSplit k (fun i => Fin (f i))).trans
      ((Equiv.sumCongr (Equiv.refl _) (finSigmaEquiv k f')).trans (finSumEquiv _ _))

/-! ## Duplicate-Free Exhaustive Lists (`FinList`) and Boolean Subtypes -/

/-- Duplicate-free predicate on a `List`. -/
inductive NoDup {α : Type u} : List α → Prop where
  | nil : NoDup []
  | cons {x : α} {xs : List α} : x ∉ xs → NoDup xs → NoDup (x :: xs)

/-- An exhaustive duplicate-free list enumerating all elements of `α`. -/
structure FinList (α : Type) where
  elems : List α
  nodup : NoDup elems
  complete : ∀ x : α, x ∈ elems

def listGetFin : (xs : List α) → Fin xs.length → α
  | x :: _, ⟨0, _⟩ => x
  | _ :: xs, ⟨i + 1, h⟩ => listGetFin xs ⟨i, Nat.lt_of_succ_lt_succ h⟩

def listIdxOf [DecidableEq α] : (xs : List α) → (x : α) → (x ∈ xs) → Fin xs.length
  | y :: ys, x, h =>
    if hxy : x = y then ⟨0, Nat.zero_lt_succ ys.length⟩
    else
      have hmem : x ∈ ys := by
        cases h with
        | head => exact absurd rfl hxy
        | tail _ hm => exact hm
      let idx := listIdxOf ys x hmem
      ⟨idx.val + 1, Nat.succ_lt_succ idx.isLt⟩

theorem listGetFin_idxOf [DecidableEq α] :
    ∀ (xs : List α) (x : α) (h : x ∈ xs), listGetFin xs (listIdxOf xs x h) = x
  | y :: ys, x, h => by
    unfold listIdxOf
    by_cases hxy : x = y
    · rw [dite_pos hxy]; exact hxy.symm
    · rw [dite_neg hxy]
      exact listGetFin_idxOf ys x _

theorem listGetFin_mem : ∀ (xs : List α) (i : Fin xs.length), listGetFin xs i ∈ xs
  | _ :: _, ⟨0, _⟩ => List.Mem.head _
  | _ :: xs, ⟨i + 1, h⟩ => List.Mem.tail _ (listGetFin_mem xs ⟨i, Nat.lt_of_succ_lt_succ h⟩)

theorem listIdxOf_getFin [DecidableEq α] :
    ∀ (xs : List α) (_hnd : NoDup xs) (i : Fin xs.length),
      listIdxOf xs (listGetFin xs i) (listGetFin_mem xs i) = i
  | y :: ys, .cons _ _, ⟨0, _⟩ => by
    unfold listGetFin listIdxOf
    rw [dite_pos rfl]
  | y :: ys, .cons hy hnd, ⟨i + 1, hi⟩ => by
    unfold listGetFin listIdxOf
    have hmem : listGetFin ys ⟨i, Nat.lt_of_succ_lt_succ hi⟩ ∈ ys :=
      listGetFin_mem ys ⟨i, Nat.lt_of_succ_lt_succ hi⟩
    have hne : listGetFin ys ⟨i, Nat.lt_of_succ_lt_succ hi⟩ ≠ y := by
      intro heq
      rw [heq] at hmem
      exact hy hmem
    rw [dite_neg hne]
    apply Fin.ext
    dsimp
    have ih := listIdxOf_getFin ys hnd ⟨i, Nat.lt_of_succ_lt_succ hi⟩
    exact congrArg (· + 1) (congrArg Fin.val ih)

/-- Any `FinList α` with `[DecidableEq α]` induces a canonical bijection `α ≃ Fin L.elems.length`. -/
def FinList.equivFin [DecidableEq α] (L : FinList α) : α ≃ Fin L.elems.length where
  toFun x := listIdxOf L.elems x (L.complete x)
  invFun i := listGetFin L.elems i
  left_inv x := listGetFin_idxOf L.elems x (L.complete x)
  right_inv i := listIdxOf_getFin L.elems L.nodup i

/-- Canonical list `[0, 1, ..., n - 1]` of `Fin n`. -/
def finRangeList : (n : Nat) → List (Fin n)
  | 0 => []
  | n + 1 => ⟨0, Nat.zero_lt_succ n⟩ :: (finRangeList n).map (fun i => ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)

theorem mem_map_succ_iff {n : Nat} {xs : List (Fin n)} {k : Fin (n + 1)} :
    k ∈ xs.map (fun i : Fin n => (⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩ : Fin (n + 1))) ↔
      ∃ i : Fin n, i ∈ xs ∧ i.val + 1 = k.val := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    simp only [List.map, List.mem_cons]
    constructor
    · rintro (h | h)
      · subst h
        exact ⟨x, Or.inl rfl, rfl⟩
      · rcases ih.mp h with ⟨i, hi, hiv⟩
        exact ⟨i, Or.inr hi, hiv⟩
    · rintro ⟨i, rfl | hi, hiv⟩
      · left; apply Fin.ext; exact hiv.symm
      · right; exact ih.mpr ⟨i, hi, hiv⟩

theorem nodup_map_succ {n : Nat} {xs : List (Fin n)} (h : NoDup xs) :
    NoDup (xs.map (fun i : Fin n => (⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩ : Fin (n + 1)))) := by
  induction h with
  | nil => exact .nil
  | @cons x xs hx _ ih =>
    refine .cons ?_ ih
    intro hmem
    rcases mem_map_succ_iff.mp hmem with ⟨i, hi, hiv⟩
    change i.val + 1 = x.val + 1 at hiv
    have hxi : i = x := Fin.ext (by omega)
    subst hxi
    exact hx hi

theorem finRangeList_nodup : (n : Nat) → NoDup (finRangeList n)
  | 0 => .nil
  | n + 1 => by
    refine .cons ?_ (nodup_map_succ (finRangeList_nodup n))
    intro hmem
    rcases mem_map_succ_iff.mp hmem with ⟨i, _, hiv⟩
    dsimp at hiv
    omega

theorem finRangeList_complete : (n : Nat) → ∀ x : Fin n, x ∈ finRangeList n
  | 0, x => nomatch x
  | _ + 1, ⟨0, _⟩ => List.Mem.head _
  | n + 1, ⟨k + 1, hk⟩ => by
    dsimp [finRangeList]
    refine List.Mem.tail _ ?_
    exact mem_map_succ_iff.mpr ⟨⟨k, Nat.lt_of_succ_lt_succ hk⟩, finRangeList_complete n _, rfl⟩

theorem finRangeList_length : (n : Nat) → (finRangeList n).length = n
  | 0 => rfl
  | n + 1 => by simp [finRangeList, finRangeList_length n]

def finListFin (n : Nat) : FinList (Fin n) where
  elems := finRangeList n
  nodup := finRangeList_nodup n
  complete := finRangeList_complete n

/-- Filter a list into a list of subtypes `{ x : α // P x = true }`. -/
def filterSubtype {α : Type} (P : α → Bool) : List α → List { x : α // P x = true }
  | [] => []
  | x :: xs =>
    if h : P x = true then ⟨x, h⟩ :: filterSubtype P xs
    else filterSubtype P xs

theorem mem_filterSubtype_iff {α : Type} (P : α → Bool) :
    ∀ (xs : List α) (u : { x : α // P x = true }), u ∈ filterSubtype P xs ↔ u.val ∈ xs
  | [], _ => by simp [filterSubtype]
  | x :: xs, ⟨v, hv⟩ => by
    dsimp [filterSubtype]
    by_cases hx : P x = true
    · rw [dite_pos hx]
      simp only [List.mem_cons]
      rw [mem_filterSubtype_iff P xs]
      constructor
      · rintro (h | h)
        · left; exact congrArg Subtype.val h
        · right; exact h
      · rintro (rfl | h)
        · left; rfl
        · right; exact h
    · rw [dite_neg hx]
      rw [mem_filterSubtype_iff P xs]
      simp only [List.mem_cons]
      constructor
      · intro h; exact Or.inr h
      · rintro (rfl | h)
        · exact absurd hv hx
        · exact h

theorem nodup_filterSubtype {α : Type} (P : α → Bool) :
    ∀ {xs : List α}, NoDup xs → NoDup (filterSubtype P xs)
  | [], .nil => .nil
  | x :: xs, .cons hx hnd => by
    dsimp [filterSubtype]
    by_cases hpx : P x = true
    · rw [dite_pos hpx]
      refine .cons ?_ (nodup_filterSubtype P hnd)
      intro hmem
      exact hx ((mem_filterSubtype_iff P xs _).mp hmem)
    · rw [dite_neg hpx]
      exact nodup_filterSubtype P hnd

theorem filterSubtype_length_eq_filter {α : Type} (P : α → Bool) :
    ∀ (xs : List α), (filterSubtype P xs).length = (xs.filter P).length
  | [] => rfl
  | x :: xs => by
    dsimp [filterSubtype, List.filter]
    by_cases h : P x = true
    · rw [dite_pos h, h]; simp [filterSubtype_length_eq_filter P xs]
    · rw [dite_neg h]
      cases hpx : P x
      · exact filterSubtype_length_eq_filter P xs
      · exact absurd hpx h

def FinList.subtype {α : Type} (L : FinList α) (P : α → Bool) :
    FinList { x : α // P x = true } where
  elems := filterSubtype P L.elems
  nodup := nodup_filterSubtype P L.nodup
  complete u := (mem_filterSubtype_iff P L.elems u).mpr (L.complete u.val)

/-- Number of elements of `Fin n` satisfying Boolean predicate `P`. -/
def countFinTrue (n : Nat) (P : Fin n → Bool) : Nat :=
  ((finRangeList n).filter P).length

/-- Canonical bijection `{ x : Fin n // P x = true } ≃ Fin (countFinTrue n P)`. -/
def subtypeTrueEquivFin (n : Nat) (P : Fin n → Bool) :
    { x : Fin n // P x = true } ≃ Fin (countFinTrue n P) := by
  let L := (finListFin n).subtype P
  have hlen : L.elems.length = countFinTrue n P :=
    filterSubtype_length_eq_filter P (finRangeList n)
  exact L.equivFin.trans (hlen ▸ Equiv.refl _)

/-- Product of two `FinList`s. -/
def listProd {α β : Type} : List α → List β → List (α × β)
  | [], _ => []
  | x :: xs, ys => ys.map (fun y => (x, y)) ++ listProd xs ys

theorem mem_listProd_iff {α β : Type} :
    ∀ (xs : List α) (ys : List β) (p : α × β), p ∈ listProd xs ys ↔ p.1 ∈ xs ∧ p.2 ∈ ys
  | [], _, _ => by simp [listProd]
  | x :: xs, ys, (a, b) => by
    simp only [listProd, List.mem_append, List.mem_map, List.mem_cons]
    rw [mem_listProd_iff xs ys (a, b)]
    constructor
    · rintro (⟨y, hy, hxy⟩ | ⟨ha, hb⟩)
      · injection hxy with hxa hyb
        subst hxa hyb
        exact ⟨Or.inl rfl, hy⟩
      · exact ⟨Or.inr ha, hb⟩
    · rintro ⟨rfl | ha, hb⟩
      · left; exact ⟨b, hb, rfl⟩
      · right; exact ⟨ha, hb⟩

theorem nodup_append {α : Type} {xs ys : List α}
    (hx : NoDup xs) (hy : NoDup ys) (hdisj : ∀ z, z ∈ xs → z ∉ ys) : NoDup (xs ++ ys) := by
  induction hx with
  | nil => exact hy
  | @cons x xs hnx _ ih =>
    refine .cons ?_ (ih (fun z hz => hdisj z (List.Mem.tail _ hz)))
    intro hm
    rcases List.mem_append.mp hm with hm | hm
    · exact hnx hm
    · exact hdisj x (List.Mem.head _) hm

theorem nodup_map_inj {α β : Type} (f : α → β) (hinj : ∀ x y, f x = f y → x = y)
    {xs : List α} (hx : NoDup xs) : NoDup (xs.map f) := by
  induction hx with
  | nil => exact .nil
  | @cons x xs hnx _ ih =>
    refine .cons ?_ ih
    intro hm
    rcases List.mem_map.mp hm with ⟨x', hx', heq⟩
    have hxx := hinj x' x heq
    subst hxx
    exact hnx hx'

theorem nodup_listProd {α β : Type} {xs : List α} {ys : List β}
    (hx : NoDup xs) (hy : NoDup ys) : NoDup (listProd xs ys) := by
  induction hx with
  | nil => exact .nil
  | @cons x xs hnx _ ih =>
    dsimp [listProd]
    have hpair : NoDup (ys.map (fun y => (x, y))) :=
      nodup_map_inj (fun y => (x, y)) (fun _ _ h => by injection h) hy
    refine nodup_append hpair ih ?_
    intro z hzx hzy
    rcases List.mem_map.mp hzx with ⟨y, _, rfl⟩
    exact hnx ((mem_listProd_iff xs ys (x, y)).mp hzy).1

def FinList.prod {α β : Type} (L₁ : FinList α) (L₂ : FinList β) : FinList (α × β) where
  elems := listProd L₁.elems L₂.elems
  nodup := nodup_listProd L₁.nodup L₂.nodup
  complete p := (mem_listProd_iff L₁.elems L₂.elems p).mpr ⟨L₁.complete p.1, L₂.complete p.2⟩

/-! ## Section 2: Permutations, Crossword Grids, Words, and Rook Placements -/

/-- A permutation of `Fin n`, matching `S_n` in Lewis and Won (arXiv:2609.03081v1). -/
structure Perm (n : Nat) where
  toFun : Fin n → Fin n
  invFun : Fin n → Fin n
  left_inv : ∀ i, invFun (toFun i) = i
  right_inv : ∀ j, toFun (invFun j) = j

namespace Perm

theorem ext {n : Nat} {u v : Perm n} (h : ∀ i, u.toFun i = v.toFun i) : u = v := by
  have hfun : u.toFun = v.toFun := funext h
  have hinv : u.invFun = v.invFun := by
    funext j
    have hj := u.left_inv (v.invFun j)
    rw [h (v.invFun j), v.right_inv j] at hj
    exact hj
  cases u; cases v
  simp only [mk.injEq]
  exact ⟨hfun, hinv⟩

def equiv (w : Perm n) : Fin n ≃ Fin n where
  toFun := w.toFun
  invFun := w.invFun
  left_inv := w.left_inv
  right_inv := w.right_inv

end Perm

/-- Construct a `Perm n` from a 1-based list `[w(1), ..., w(n)]` verified by decidable check. -/
def listGetDNat : List Nat → Nat → Nat
  | [], _ => 0
  | x :: _, 0 => x
  | _ :: xs, i + 1 => listGetDNat xs i

def listFindIdx1Based : List Nat → Nat → Nat
  | [], _ => 0
  | x :: xs, v => if x == v then 0 else listFindIdx1Based xs v + 1

def isValidPerm1Based (n : Nat) (xs : List Nat) : Bool :=
  (xs.length == n) &&
  (finRangeList n).all (fun i =>
    let v := listGetDNat xs i.val
    (1 ≤ v && v ≤ n) &&
    (listFindIdx1Based xs v == i.val)) &&
  (finRangeList n).all (fun j =>
    let idx := listFindIdx1Based xs (j.val + 1)
    (idx < n) && (listGetDNat xs idx == j.val + 1))

def permOfList1Based (n : Nat) (xs : List Nat) (h : isValidPerm1Based n xs = true) : Perm n :=
  have h12 : ((xs.length == n) &&
      (finRangeList n).all (fun i =>
        let v := listGetDNat xs i.val
        (1 ≤ v && v ≤ n) && (listFindIdx1Based xs v == i.val))) = true ∧
      (finRangeList n).all (fun j =>
        let idx := listFindIdx1Based xs (j.val + 1)
        (idx < n) && (listGetDNat xs idx == j.val + 1)) = true := by
    unfold isValidPerm1Based at h
    exact Bool.and_eq_true _ _ ▸ h
  have hallI := (Bool.and_eq_true _ _ ▸ h12.1).2
  have hallJ := h12.2
  { toFun := fun i =>
      have hi := (list_all_iff _ _).mp hallI i (finRangeList_complete n i)
      have hb := (Bool.and_eq_true _ _ ▸ hi).1
      have hbounds := Bool.and_eq_true _ _ ▸ hb
      have hlo : 1 ≤ listGetDNat xs i.val := of_decide_eq_true hbounds.1
      have hhi : listGetDNat xs i.val ≤ n := of_decide_eq_true hbounds.2
      ⟨listGetDNat xs i.val - 1, by omega⟩
    invFun := fun j =>
      have hj := (list_all_iff _ _).mp hallJ j (finRangeList_complete n j)
      have hlt : listFindIdx1Based xs (j.val + 1) < n :=
        of_decide_eq_true (Bool.and_eq_true _ _ ▸ hj).1
      ⟨listFindIdx1Based xs (j.val + 1), hlt⟩
    left_inv := fun i => by
      have hi := (list_all_iff _ _).mp hallI i (finRangeList_complete n i)
      have hb := Bool.and_eq_true _ _ ▸ hi
      have hbounds := Bool.and_eq_true _ _ ▸ hb.1
      have hlo : 1 ≤ listGetDNat xs i.val := of_decide_eq_true hbounds.1
      have hidx : listFindIdx1Based xs (listGetDNat xs i.val) = i.val := by
        have := hb.2; simp at this; exact this
      apply Fin.ext
      dsimp
      have hsub : listGetDNat xs i.val - 1 + 1 = listGetDNat xs i.val := by omega
      rw [hsub, hidx]
    right_inv := fun j => by
      have hj := (list_all_iff _ _).mp hallJ j (finRangeList_complete n j)
      have hb := Bool.and_eq_true _ _ ▸ hj
      have hval : listGetDNat xs (listFindIdx1Based xs (j.val + 1)) = j.val + 1 := by
        have := hb.2; simp at this; exact this
      apply Fin.ext
      dsimp
      rw [hval]
      omega }
where
  list_all_iff {α : Type} (p : α → Bool) :
      ∀ (ys : List α), ys.all p = true ↔ ∀ x ∈ ys, p x = true
    | [] => by simp
    | x :: ys => by
      simp only [List.all_cons, Bool.and_eq_true, List.mem_cons]
      rw [list_all_iff p ys]
      constructor
      · rintro ⟨hx, hys⟩ y (rfl | hy)
        · exact hx
        · exact hys y hy
      · intro h
        exact ⟨h x (Or.inl rfl), fun y hy => h y (Or.inr hy)⟩

/-- An `m × n` crossword grid: `isBlack r c = true` iff square `(r, c)` is black. -/
structure Grid (m n : Nat) where
  isBlack : Fin m → Fin n → Bool

/-- Transpose of an `m × n` crossword grid. -/
def Grid.transpose (G : Grid m n) : Grid n m where
  isBlack c r := G.isBlack r c

/-- The `n × n` permutation grid `Grid(w)` with black squares at `(i, w(i))`. -/
def gridOfPerm {n : Nat} (w : Perm n) : Grid n n where
  isBlack i j := decide (j = w.toFun i)

/-- A maximal contiguous horizontal white run (across word) in `G`. -/
structure AcrossWord {m n : Nat} (G : Grid m n) where
  row : Fin m
  lo : Fin n
  hi : Fin n
  le : lo.val ≤ hi.val
  allWhite : ∀ c : Fin n, lo.val ≤ c.val → c.val ≤ hi.val → G.isBlack row c = false
  leftMax : ∀ h : 0 < lo.val, G.isBlack row ⟨lo.val - 1, by omega⟩ = true
  rightMax : ∀ h : hi.val + 1 < n, G.isBlack row ⟨hi.val + 1, h⟩ = true
  deriving DecidableEq

/-- A maximal contiguous vertical white run (down word) in `G`. -/
structure DownWord {m n : Nat} (G : Grid m n) where
  col : Fin n
  lo : Fin m
  hi : Fin m
  le : lo.val ≤ hi.val
  allWhite : ∀ r : Fin m, lo.val ≤ r.val → r.val ≤ hi.val → G.isBlack r col = false
  topMax : ∀ h : 0 < lo.val, G.isBlack ⟨lo.val - 1, by omega⟩ col = true
  botMax : ∀ h : hi.val + 1 < m, G.isBlack ⟨hi.val + 1, h⟩ col = true
  deriving DecidableEq

theorem AcrossWord.ext {m n : Nat} {G : Grid m n} {w₁ w₂ : AcrossWord G}
    (hr : w₁.row = w₂.row) (hlo : w₁.lo = w₂.lo) (hhi : w₁.hi = w₂.hi) : w₁ = w₂ := by
  cases w₁; cases w₂; subst hr hlo hhi; rfl

theorem DownWord.ext {m n : Nat} {G : Grid m n} {w₁ w₂ : DownWord G}
    (hc : w₁.col = w₂.col) (hlo : w₁.lo = w₂.lo) (hhi : w₁.hi = w₂.hi) : w₁ = w₂ := by
  cases w₁; cases w₂; subst hc hlo hhi; rfl

def AcrossWord.containsBool {m n : Nat} {G : Grid m n} (aw : AcrossWord G) (r : Fin m) (c : Fin n) : Bool :=
  decide (r = aw.row ∧ aw.lo.val ≤ c.val ∧ c.val ≤ aw.hi.val)

def DownWord.containsBool {m n : Nat} {G : Grid m n} (dw : DownWord G) (r : Fin m) (c : Fin n) : Bool :=
  decide (c = dw.col ∧ dw.lo.val ≤ r.val ∧ r.val ≤ dw.hi.val)

def AcrossWord.Contains {m n : Nat} {G : Grid m n} (aw : AcrossWord G) (r : Fin m) (c : Fin n) : Prop :=
  r = aw.row ∧ aw.lo.val ≤ c.val ∧ c.val ≤ aw.hi.val

def DownWord.Contains {m n : Nat} {G : Grid m n} (dw : DownWord G) (r : Fin m) (c : Fin n) : Prop :=
  c = dw.col ∧ dw.lo.val ≤ r.val ∧ r.val ≤ dw.hi.val

/-- Down words of `G` correspond bijectively to across words of `G.transpose`. -/
def downWordEquivTransposeAcross {m n : Nat} (G : Grid m n) :
    DownWord G ≃ AcrossWord G.transpose where
  toFun dw := ⟨dw.col, dw.lo, dw.hi, dw.le, dw.allWhite, dw.topMax, dw.botMax⟩
  invFun aw := ⟨aw.row, aw.lo, aw.hi, aw.le, aw.allWhite, aw.leftMax, aw.rightMax⟩
  left_inv dw := by cases dw; rfl
  right_inv aw := by cases aw; rfl

/-- Scan right from `cur` in row `r` to find the end of a maximal white run. -/
def findRunEnd {m n : Nat} (G : Grid m n) (r : Fin m) (cur : Nat) (h : cur < n) : Fin n :=
  if hnext : cur + 1 < n then
    if G.isBlack r ⟨cur + 1, hnext⟩ then ⟨cur, h⟩
    else findRunEnd G r (cur + 1) hnext
  else ⟨cur, h⟩
termination_by n - cur

theorem findRunEnd_ge {m n : Nat} (G : Grid m n) (r : Fin m) (cur : Nat) (h : cur < n) :
    cur ≤ (findRunEnd G r cur h).val := by
  unfold findRunEnd
  by_cases hnext : cur + 1 < n
  · rw [dite_pos hnext]
    by_cases hb : G.isBlack r ⟨cur + 1, hnext⟩ = true
    · rw [ite_pos hb]; exact Nat.le_refl _
    · rw [ite_neg hb]
      have ih := findRunEnd_ge G r (cur + 1) hnext
      omega
  · rw [dite_neg hnext]; exact Nat.le_refl _
termination_by n - cur

theorem findRunEnd_white {m n : Nat} (G : Grid m n) (r : Fin m) (cur : Nat) (h : cur < n)
    (hw : G.isBlack r ⟨cur, h⟩ = false) :
    ∀ c : Fin n, cur ≤ c.val → c.val ≤ (findRunEnd G r cur h).val → G.isBlack r c = false := by
  unfold findRunEnd
  by_cases hnext : cur + 1 < n
  · rw [dite_pos hnext]
    by_cases hb : G.isBlack r ⟨cur + 1, hnext⟩ = true
    · rw [ite_pos hb]
      intro c hlo hhi
      change c.val ≤ cur at hhi
      have hc : c = ⟨cur, h⟩ := Fin.ext (show c.val = cur by omega)
      subst hc; exact hw
    · rw [ite_neg hb]
      have hw' : G.isBlack r ⟨cur + 1, hnext⟩ = false := by
        cases hval : G.isBlack r ⟨cur + 1, hnext⟩
        · rfl
        · exact absurd hval hb
      intro c hlo hhi
      by_cases hce : c.val = cur
      · have hc : c = ⟨cur, h⟩ := Fin.ext hce
        subst hc; exact hw
      · exact findRunEnd_white G r (cur + 1) hnext hw' c (by omega) hhi
  · rw [dite_neg hnext]
    intro c hlo hhi
    change c.val ≤ cur at hhi
    have hc : c = ⟨cur, h⟩ := Fin.ext (show c.val = cur by omega)
    subst hc; exact hw
termination_by n - cur

theorem findRunEnd_rightMax {m n : Nat} (G : Grid m n) (r : Fin m) (cur : Nat) (h : cur < n) :
    ∀ hlt : (findRunEnd G r cur h).val + 1 < n,
      G.isBlack r ⟨(findRunEnd G r cur h).val + 1, hlt⟩ = true := by
  intro hlt
  have heq : findRunEnd G r cur h =
      (if hnext : cur + 1 < n then
        if G.isBlack r ⟨cur + 1, hnext⟩ then ⟨cur, h⟩
        else findRunEnd G r (cur + 1) hnext
      else ⟨cur, h⟩) := by
    conv => lhs; unfold findRunEnd
  by_cases hnext : cur + 1 < n
  · rw [dite_pos hnext] at heq
    by_cases hb : G.isBlack r ⟨cur + 1, hnext⟩ = true
    · rw [ite_pos hb] at heq
      have hv : (findRunEnd G r cur h).val = cur := congrArg Fin.val heq
      have hfin : (⟨(findRunEnd G r cur h).val + 1, hlt⟩ : Fin n) = ⟨cur + 1, hnext⟩ :=
        Fin.ext (by dsimp; omega)
      rw [hfin]
      exact hb
    · rw [ite_neg hb] at heq
      have hv : (findRunEnd G r cur h).val = (findRunEnd G r (cur + 1) hnext).val :=
        congrArg Fin.val heq
      have hlt' : (findRunEnd G r (cur + 1) hnext).val + 1 < n := by omega
      have ih := findRunEnd_rightMax G r (cur + 1) hnext hlt'
      have hfin : (⟨(findRunEnd G r cur h).val + 1, hlt⟩ : Fin n) =
          ⟨(findRunEnd G r (cur + 1) hnext).val + 1, hlt'⟩ :=
        Fin.ext (by dsimp; omega)
      rw [hfin]
      exact ih
  · rw [dite_neg hnext] at heq
    have hv : (findRunEnd G r cur h).val = cur := congrArg Fin.val heq
    omega
termination_by n - cur

/-- Scan left from `cur` in row `r` to find the start of a maximal white run. -/
def findRunStart {m n : Nat} (G : Grid m n) (r : Fin m) : (cur : Nat) → (h : cur < n) → Fin n
  | 0, h => ⟨0, h⟩
  | k + 1, h =>
    if G.isBlack r ⟨k, by omega⟩ then ⟨k + 1, h⟩
    else findRunStart G r k (by omega)

theorem findRunStart_le {m n : Nat} (G : Grid m n) (r : Fin m) :
    ∀ (cur : Nat) (h : cur < n), (findRunStart G r cur h).val ≤ cur
  | 0, _ => Nat.le_refl _
  | k + 1, h => by
    unfold findRunStart
    by_cases hb : G.isBlack r ⟨k, by omega⟩ = true
    · rw [ite_pos hb]; exact Nat.le_refl _
    · rw [ite_neg hb]
      have ih := findRunStart_le G r k (by omega)
      omega

theorem findRunStart_white {m n : Nat} (G : Grid m n) (r : Fin m) :
    ∀ (cur : Nat) (h : cur < n), G.isBlack r ⟨cur, h⟩ = false →
      ∀ c : Fin n, (findRunStart G r cur h).val ≤ c.val → c.val ≤ cur → G.isBlack r c = false
  | 0, h, hw => by
    intro c _ hhi
    have hc : c = ⟨0, h⟩ := Fin.ext (by dsimp; omega)
    subst hc; exact hw
  | k + 1, h, hw => by
    unfold findRunStart
    by_cases hb : G.isBlack r ⟨k, by omega⟩ = true
    · rw [ite_pos hb]
      intro c hlo hhi
      dsimp at hlo
      have hc : c = ⟨k + 1, h⟩ := Fin.ext (by dsimp; omega)
      subst hc; exact hw
    · rw [ite_neg hb]
      have hw' : G.isBlack r ⟨k, by omega⟩ = false := by
        cases hval : G.isBlack r ⟨k, by omega⟩
        · rfl
        · exact absurd hval hb
      intro c hlo hhi
      by_cases hce : c.val = k + 1
      · have hc : c = ⟨k + 1, h⟩ := Fin.ext hce
        subst hc; exact hw
      · exact findRunStart_white G r k (by omega) hw' c hlo (by omega)

theorem findRunStart_leftMax {m n : Nat} (G : Grid m n) (r : Fin m) :
    ∀ (cur : Nat) (h : cur < n) (hlt : 0 < (findRunStart G r cur h).val),
      G.isBlack r ⟨(findRunStart G r cur h).val - 1, by omega⟩ = true
  | 0, _, hlt => by dsimp [findRunStart] at hlt; omega
  | k + 1, h, hlt => by
    have heq : findRunStart G r (k + 1) h =
        (if G.isBlack r ⟨k, by omega⟩ then ⟨k + 1, h⟩ else findRunStart G r k (by omega)) := rfl
    by_cases hb : G.isBlack r ⟨k, by omega⟩ = true
    · rw [ite_pos hb] at heq
      have hv : (findRunStart G r (k + 1) h).val = k + 1 := congrArg Fin.val heq
      have hfin : (⟨(findRunStart G r (k + 1) h).val - 1, by omega⟩ : Fin n) = ⟨k, by omega⟩ :=
        Fin.ext (by dsimp; omega)
      rw [hfin]
      exact hb
    · rw [ite_neg hb] at heq
      have hv : (findRunStart G r (k + 1) h).val = (findRunStart G r k (by omega)).val :=
        congrArg Fin.val heq
      have hlt' : 0 < (findRunStart G r k (by omega)).val := by omega
      have ih := findRunStart_leftMax G r k (by omega) hlt'
      have hfin : (⟨(findRunStart G r (k + 1) h).val - 1, by omega⟩ : Fin n) =
          ⟨(findRunStart G r k (by omega)).val - 1, by omega⟩ :=
        Fin.ext (by dsimp; omega)
      rw [hfin]
      exact ih

/-- Every white square `(r, c)` lies in a unique across word of `G`. -/
def acrossWordOfWhite {m n : Nat} (G : Grid m n) (r : Fin m) (c : Fin n)
    (hw : G.isBlack r c = false) : AcrossWord G where
  row := r
  lo := findRunStart G r c.val c.isLt
  hi := findRunEnd G r c.val c.isLt
  le := Nat.le_trans (findRunStart_le G r c.val c.isLt) (findRunEnd_ge G r c.val c.isLt)
  allWhite := fun c' hlo hhi => by
    by_cases hle : c'.val ≤ c.val
    · exact findRunStart_white G r c.val c.isLt hw c' hlo hle
    · exact findRunEnd_white G r c.val c.isLt hw c' (by omega) hhi
  leftMax := findRunStart_leftMax G r c.val c.isLt
  rightMax := findRunEnd_rightMax G r c.val c.isLt

theorem acrossWordOfWhite_contains {m n : Nat} (G : Grid m n) (r : Fin m) (c : Fin n)
    (hw : G.isBlack r c = false) : (acrossWordOfWhite G r c hw).Contains r c :=
  ⟨rfl, findRunStart_le G r c.val c.isLt, findRunEnd_ge G r c.val c.isLt⟩

theorem acrossWord_unique_of_contains {m n : Nat} {G : Grid m n}
    (w₁ w₂ : AcrossWord G) (r : Fin m) (c : Fin n)
    (h₁ : w₁.Contains r c) (h₂ : w₂.Contains r c) : w₁ = w₂ := by
  rcases h₁ with ⟨hr₁, hlo₁, hhi₁⟩
  rcases h₂ with ⟨hr₂, hlo₂, hhi₂⟩
  have hrow : w₁.row = w₂.row := hr₁.symm.trans hr₂
  have hlo : w₁.lo = w₂.lo := by
    apply Fin.ext
    by_cases hlt : w₁.lo.val < w₂.lo.val
    · have hp : 0 < w₂.lo.val := by omega
      have hb := w₂.leftMax hp
      rw [← hrow] at hb
      have hw := w₁.allWhite ⟨w₂.lo.val - 1, by omega⟩ (by dsimp; omega) (by dsimp; omega)
      rw [hw] at hb; contradiction
    · by_cases hgt : w₂.lo.val < w₁.lo.val
      · have hp : 0 < w₁.lo.val := by omega
        have hb := w₁.leftMax hp
        rw [hrow] at hb
        have hw := w₂.allWhite ⟨w₁.lo.val - 1, by omega⟩ (by dsimp; omega) (by dsimp; omega)
        rw [hw] at hb; contradiction
      · omega
  have hhi : w₁.hi = w₂.hi := by
    apply Fin.ext
    by_cases hlt : w₁.hi.val < w₂.hi.val
    · have hp : w₁.hi.val + 1 < n := by omega
      have hb := w₁.rightMax hp
      rw [hrow] at hb
      have hw := w₂.allWhite ⟨w₁.hi.val + 1, hp⟩ (by dsimp; omega) (by dsimp; omega)
      rw [hw] at hb; contradiction
    · by_cases hgt : w₂.hi.val < w₁.hi.val
      · have hp : w₂.hi.val + 1 < n := by omega
        have hb := w₂.rightMax hp
        rw [← hrow] at hb
        have hw := w₁.allWhite ⟨w₂.hi.val + 1, hp⟩ (by dsimp; omega) (by dsimp; omega)
        rw [hw] at hb; contradiction
      · omega
  exact AcrossWord.ext hrow hlo hhi

/-- Every white square `(r, c)` lies in a unique down word of `G`. -/
def downWordOfWhite {m n : Nat} (G : Grid m n) (r : Fin m) (c : Fin n)
    (hw : G.isBlack r c = false) : DownWord G :=
  (downWordEquivTransposeAcross G).invFun (acrossWordOfWhite G.transpose c r hw)

theorem downWordOfWhite_contains {m n : Nat} (G : Grid m n) (r : Fin m) (c : Fin n)
    (hw : G.isBlack r c = false) : (downWordOfWhite G r c hw).Contains r c :=
  acrossWordOfWhite_contains G.transpose c r hw

theorem downWord_unique_of_contains {m n : Nat} {G : Grid m n}
    (w₁ w₂ : DownWord G) (r : Fin m) (c : Fin n)
    (h₁ : w₁.Contains r c) (h₂ : w₂.Contains r c) : w₁ = w₂ := by
  have heq := acrossWord_unique_of_contains
    ((downWordEquivTransposeAcross G).toFun w₁)
    ((downWordEquivTransposeAcross G).toFun w₂) c r h₁ h₂
  exact (downWordEquivTransposeAcross G).injective heq

/-- Fast duplicate-free enumeration of all across words via word starts `(r, lo)`. -/
def isAcrossStartBool {m n : Nat} (G : Grid m n) (r : Fin m) (lo : Fin n) : Bool :=
  !G.isBlack r lo && (if h : 0 < lo.val then G.isBlack r ⟨lo.val - 1, by omega⟩ else true)

def acrossWordOfStart {m n : Nat} (G : Grid m n)
    (s : { p : Fin m × Fin n // isAcrossStartBool G p.1 p.2 = true }) : AcrossWord G :=
  have hs : !G.isBlack s.val.1 s.val.2 = true ∧
      (if h : 0 < s.val.2.val then G.isBlack s.val.1 ⟨s.val.2.val - 1, by omega⟩ else true) = true := by
    have hp := s.property
    unfold isAcrossStartBool at hp
    exact Bool.and_eq_true _ _ ▸ hp
  have hw : G.isBlack s.val.1 s.val.2 = false := by
    cases hb : G.isBlack s.val.1 s.val.2
    · rfl
    · rw [hb] at hs; exact absurd hs.1 (by decide)
  { row := s.val.1
    lo := s.val.2
    hi := findRunEnd G s.val.1 s.val.2.val s.val.2.isLt
    le := findRunEnd_ge G s.val.1 s.val.2.val s.val.2.isLt
    allWhite := findRunEnd_white G s.val.1 s.val.2.val s.val.2.isLt hw
    leftMax := fun h => by
      have hl := hs.2
      rw [dite_pos h] at hl
      exact hl
    rightMax := findRunEnd_rightMax G s.val.1 s.val.2.val s.val.2.isLt }

def acrossWordEquivStarts {m n : Nat} (G : Grid m n) :
    AcrossWord G ≃ { p : Fin m × Fin n // isAcrossStartBool G p.1 p.2 = true } where
  toFun aw := ⟨(aw.row, aw.lo), by
    unfold isAcrossStartBool
    have hw := aw.allWhite aw.lo (Nat.le_refl _) aw.le
    rw [hw]
    simp only [Bool.not_false, Bool.true_and]
    by_cases h : 0 < aw.lo.val
    · rw [dite_pos h]; exact aw.leftMax h
    · rw [dite_neg h]⟩
  invFun := acrossWordOfStart G
  left_inv aw := by
    apply acrossWord_unique_of_contains _ _ aw.row aw.lo
    · exact ⟨rfl, Nat.le_refl _, findRunEnd_ge G aw.row aw.lo.val aw.lo.isLt⟩
    · exact ⟨rfl, Nat.le_refl _, aw.le⟩
  right_inv _ := Subtype.ext rfl

def finListAcrossWords {m n : Nat} (G : Grid m n) : FinList (AcrossWord G) :=
  let starts := ((finListFin m).prod (finListFin n)).subtype (fun p => isAcrossStartBool G p.1 p.2)
  { elems := starts.elems.map (acrossWordOfStart G)
    nodup := nodup_map_inj (acrossWordOfStart G)
      (fun _ _ h => (acrossWordEquivStarts G).symm.injective h) starts.nodup
    complete := fun aw => by
      refine List.mem_map.mpr ⟨(acrossWordEquivStarts G).toFun aw, starts.complete _, ?_⟩
      exact (acrossWordEquivStarts G).left_inv aw }

def finListDownWords {m n : Nat} (G : Grid m n) : FinList (DownWord G) :=
  let tr := finListAcrossWords G.transpose
  { elems := tr.elems.map (downWordEquivTransposeAcross G).invFun
    nodup := nodup_map_inj (downWordEquivTransposeAcross G).invFun
      (fun _ _ h => (downWordEquivTransposeAcross G).symm.injective h) tr.nodup
    complete := fun dw => by
      refine List.mem_map.mpr ⟨(downWordEquivTransposeAcross G).toFun dw, tr.complete _, ?_⟩
      exact (downWordEquivTransposeAcross G).left_inv dw }

/-! ## Complete Non-Attacking Rook Placements (`RP(G)`) and Word-Graph Bijection -/

/-- Exact uniqueness of a `Fin k` witness. -/
def UniqueFin {k : Nat} (P : Fin k → Prop) : Prop :=
  ∃ x : Fin k, P x ∧ ∀ y : Fin k, P y → y = x

/-- A complete non-attacking rook placement on `G` (Lewis and Won, Section 2):
    a subset of white squares containing exactly one rook in every across word
    and every down word. -/
structure RookPlacement {m n : Nat} (G : Grid m n) where
  hasRook : Fin m → Fin n → Bool
  onlyWhite : ∀ r c, hasRook r c = true → G.isBlack r c = false
  acrossUnique : ∀ aw : AcrossWord G, UniqueFin (fun c : Fin n => aw.Contains aw.row c ∧ hasRook aw.row c = true)
  downUnique : ∀ dw : DownWord G, UniqueFin (fun r : Fin m => dw.Contains r dw.col ∧ hasRook r dw.col = true)

theorem RookPlacement.ext {m n : Nat} {G : Grid m n} {p₁ p₂ : RookPlacement G}
    (h : ∀ r c, p₁.hasRook r c = p₂.hasRook r c) : p₁ = p₂ := by
  have hf : p₁.hasRook = p₂.hasRook := by funext r c; exact h r c
  cases p₁; cases p₂; subst hf; rfl

/-- Constructive search for the first `Fin k` satisfying Boolean predicate `P`. -/
def findUniqueFin : {k : Nat} → (P : Fin k → Bool) →
    (∃ x : Fin k, P x = true) → { x : Fin k // P x = true }
  | 0, _, h => by exfalso; rcases h with ⟨x, _⟩; exact nomatch x
  | k + 1, P, h =>
    if h0 : P ⟨0, Nat.zero_lt_succ k⟩ = true then ⟨⟨0, Nat.zero_lt_succ k⟩, h0⟩
    else
      have hex : ∃ j : Fin k, P ⟨j.val + 1, Nat.succ_lt_succ j.isLt⟩ = true := by
        rcases h with ⟨⟨v, hv⟩, hx⟩
        cases v with
        | zero => exact absurd hx h0
        | succ v' => exact ⟨⟨v', Nat.lt_of_succ_lt_succ hv⟩, hx⟩
      let sub := findUniqueFin (fun j : Fin k => P ⟨j.val + 1, Nat.succ_lt_succ j.isLt⟩) hex
      ⟨⟨sub.val.val + 1, Nat.succ_lt_succ sub.val.isLt⟩, sub.property⟩

/-- Word-incidence edge check: an across word and down word intersect iff `(aw.row, dw.col)` lies in both. -/
def wordsIntersect {m n : Nat} {G : Grid m n} (aw : AcrossWord G) (dw : DownWord G) : Bool :=
  decide (aw.lo.val ≤ dw.col.val ∧ dw.col.val ≤ aw.hi.val ∧
          dw.lo.val ≤ aw.row.val ∧ aw.row.val ≤ dw.hi.val)

theorem wordsIntersect_iff {m n : Nat} {G : Grid m n} (aw : AcrossWord G) (dw : DownWord G) :
    wordsIntersect aw dw = true ↔ aw.Contains aw.row dw.col ∧ dw.Contains aw.row dw.col := by
  unfold wordsIntersect AcrossWord.Contains DownWord.Contains
  simp only [decide_eq_true_eq, true_and]
  constructor
  · rintro ⟨h1, h2, h3, h4⟩; exact ⟨⟨h1, h2⟩, ⟨h3, h4⟩⟩
  · rintro ⟨⟨h1, h2⟩, ⟨h3, h4⟩⟩; exact ⟨h1, h2, h3, h4⟩

/-- A perfect matching in the word-incidence bipartite graph `Graph(G)`. -/
structure WordPerfectMatching {m n : Nat} (G : Grid m n) where
  matchFun : AcrossWord G → DownWord G
  invMatch : DownWord G → AcrossWord G
  left_inv : ∀ aw, invMatch (matchFun aw) = aw
  right_inv : ∀ dw, matchFun (invMatch dw) = dw
  incident : ∀ aw, wordsIntersect aw (matchFun aw) = true

theorem WordPerfectMatching.ext {m n : Nat} {G : Grid m n} {M₁ M₂ : WordPerfectMatching G}
    (h : ∀ aw, M₁.matchFun aw = M₂.matchFun aw) : M₁ = M₂ := by
  have hf : M₁.matchFun = M₂.matchFun := funext h
  have hi : M₁.invMatch = M₂.invMatch := by
    funext dw
    have h1 := M₁.left_inv (M₂.invMatch dw)
    rw [h (M₂.invMatch dw), M₂.right_inv dw] at h1
    exact h1
  cases M₁; cases M₂; subst hf hi; rfl

theorem containsBool_across_iff {m n : Nat} {G : Grid m n} (aw : AcrossWord G) (r : Fin m) (c : Fin n) :
    aw.containsBool r c = true ↔ aw.Contains r c := by
  unfold AcrossWord.containsBool AcrossWord.Contains
  exact decide_eq_true_iff

theorem containsBool_down_iff {m n : Nat} {G : Grid m n} (dw : DownWord G) (r : Fin m) (c : Fin n) :
    dw.containsBool r c = true ↔ dw.Contains r c := by
  unfold DownWord.containsBool DownWord.Contains
  exact decide_eq_true_iff

/-- First-principles bijection `RP(G) ≃ PerfectMatchings(Graph(G))` (Lewis and Won, Section 2). -/
def rookPlacementEquivWordMatching {m n : Nat} (G : Grid m n) :
    RookPlacement G ≃ WordPerfectMatching G where
  toFun R :=
    let acrossCol (aw : AcrossWord G) : { c : Fin n // (aw.containsBool aw.row c && R.hasRook aw.row c) = true } :=
      findUniqueFin (fun c => aw.containsBool aw.row c && R.hasRook aw.row c) (by
        rcases R.acrossUnique aw with ⟨c, ⟨hc1, hc2⟩, _⟩
        exact ⟨c, Bool.and_eq_true _ _ |>.mpr ⟨(containsBool_across_iff aw aw.row c).mpr hc1, hc2⟩⟩)
    let downRow (dw : DownWord G) : { r : Fin m // (dw.containsBool r dw.col && R.hasRook r dw.col) = true } :=
      findUniqueFin (fun r => dw.containsBool r dw.col && R.hasRook r dw.col) (by
        rcases R.downUnique dw with ⟨r, ⟨hr1, hr2⟩, _⟩
        exact ⟨r, Bool.and_eq_true _ _ |>.mpr ⟨(containsBool_down_iff dw r dw.col).mpr hr1, hr2⟩⟩)
    { matchFun := fun aw =>
        let c := (acrossCol aw).val
        have hp := (Bool.and_eq_true _ _).mp (acrossCol aw).property
        downWordOfWhite G aw.row c (R.onlyWhite aw.row c hp.2)
      invMatch := fun dw =>
        let r := (downRow dw).val
        have hp := (Bool.and_eq_true _ _).mp (downRow dw).property
        acrossWordOfWhite G r dw.col (R.onlyWhite r dw.col hp.2)
      left_inv := fun aw => by
        dsimp
        let c := (acrossCol aw).val
        have hp := (Bool.and_eq_true _ _).mp (acrossCol aw).property
        have hcont : aw.Contains aw.row c := (containsBool_across_iff aw aw.row c).mp hp.1
        have hrook : R.hasRook aw.row c = true := hp.2
        let dw := downWordOfWhite G aw.row c (R.onlyWhite aw.row c hrook)
        have hdwCont : dw.Contains aw.row c := downWordOfWhite_contains G aw.row c _
        have hdc : dw.col = c := hdwCont.1.symm
        let r := (downRow dw).val
        have hdp := (Bool.and_eq_true _ _).mp (downRow dw).property
        have hrCont : dw.Contains r dw.col := (containsBool_down_iff dw r dw.col).mp hdp.1
        have hrRook : R.hasRook r dw.col = true := hdp.2
        have hreq : r = aw.row := by
          rcases R.downUnique dw with ⟨_, _, huniq⟩
          have h1 := huniq r ⟨hrCont, hrRook⟩
          have h2 := huniq aw.row ⟨hdc ▸ hdwCont, hdc ▸ hrook⟩
          exact h1.trans h2.symm
        apply acrossWord_unique_of_contains _ _ r dw.col
        · exact acrossWordOfWhite_contains G r dw.col _
        · rw [hreq, hdc]; exact hcont
      right_inv := fun dw => by
        dsimp
        let r := (downRow dw).val
        have hp := (Bool.and_eq_true _ _).mp (downRow dw).property
        have hcont : dw.Contains r dw.col := (containsBool_down_iff dw r dw.col).mp hp.1
        have hrook : R.hasRook r dw.col = true := hp.2
        let aw := acrossWordOfWhite G r dw.col (R.onlyWhite r dw.col hrook)
        have hawCont : aw.Contains r dw.col := acrossWordOfWhite_contains G r dw.col _
        have har : aw.row = r := hawCont.1.symm
        let c := (acrossCol aw).val
        have hap := (Bool.and_eq_true _ _).mp (acrossCol aw).property
        have hcCont : aw.Contains aw.row c := (containsBool_across_iff aw aw.row c).mp hap.1
        have hcRook : R.hasRook aw.row c = true := hap.2
        have hceq : c = dw.col := by
          rcases R.acrossUnique aw with ⟨_, _, huniq⟩
          have h1 := huniq c ⟨hcCont, hcRook⟩
          have h2 := huniq dw.col ⟨har ▸ hawCont, har ▸ hrook⟩
          exact h1.trans h2.symm
        apply downWord_unique_of_contains _ _ aw.row c
        · exact downWordOfWhite_contains G aw.row c _
        · rw [har, hceq]; exact hcont
      incident := fun aw => by
        dsimp
        let c := (acrossCol aw).val
        have hp := (Bool.and_eq_true _ _).mp (acrossCol aw).property
        have hcont : aw.Contains aw.row c := (containsBool_across_iff aw aw.row c).mp hp.1
        have hrook : R.hasRook aw.row c = true := hp.2
        let dw := downWordOfWhite G aw.row c (R.onlyWhite aw.row c hrook)
        have hdwCont : dw.Contains aw.row c := downWordOfWhite_contains G aw.row c _
        have hdc : dw.col = c := hdwCont.1.symm
        rw [wordsIntersect_iff, hdc]
        exact ⟨hcont, hdwCont⟩ }
  invFun M :=
    let hasRook (r : Fin m) (c : Fin n) : Bool :=
      if hw : G.isBlack r c = false then
        decide (M.matchFun (acrossWordOfWhite G r c hw) = downWordOfWhite G r c hw)
      else false
    { hasRook := hasRook
      onlyWhite := fun r c hr => by
        dsimp [hasRook] at hr
        by_cases hw : G.isBlack r c = false
        · exact hw
        · rw [dite_neg hw] at hr; contradiction
      acrossUnique := fun aw => by
        let dw := M.matchFun aw
        have hinc := (wordsIntersect_iff aw dw).mp (M.incident aw)
        have hw : G.isBlack aw.row dw.col = false := aw.allWhite dw.col hinc.1.2.1 hinc.1.2.2
        refine ⟨dw.col, ⟨hinc.1, ?_⟩, ?_⟩
        · dsimp [hasRook]
          rw [dite_pos hw, decide_eq_true_iff]
          have haw : acrossWordOfWhite G aw.row dw.col hw = aw :=
            acrossWord_unique_of_contains _ _ aw.row dw.col (acrossWordOfWhite_contains G _ _ hw) hinc.1
          have hdw : downWordOfWhite G aw.row dw.col hw = dw :=
            downWord_unique_of_contains _ _ aw.row dw.col (downWordOfWhite_contains G _ _ hw) hinc.2
          rw [haw, hdw]
        · intro c ⟨hcCont, hcRook⟩
          dsimp [hasRook] at hcRook
          have hwc : G.isBlack aw.row c = false := aw.allWhite c hcCont.2.1 hcCont.2.2
          rw [dite_pos hwc, decide_eq_true_iff] at hcRook
          have haw : acrossWordOfWhite G aw.row c hwc = aw :=
            acrossWord_unique_of_contains _ _ aw.row c (acrossWordOfWhite_contains G _ _ hwc) hcCont
          rw [haw] at hcRook
          have hdwCont := downWordOfWhite_contains G aw.row c hwc
          rw [← hcRook] at hdwCont
          exact hdwCont.1
      downUnique := fun dw => by
        let aw := M.invMatch dw
        have hmaw : M.matchFun aw = dw := M.right_inv dw
        have hinc := (wordsIntersect_iff aw dw).mp (hmaw ▸ M.incident aw)
        have hw : G.isBlack aw.row dw.col = false := aw.allWhite dw.col hinc.1.2.1 hinc.1.2.2
        refine ⟨aw.row, ⟨hinc.2, ?_⟩, ?_⟩
        · dsimp [hasRook]
          rw [dite_pos hw, decide_eq_true_iff]
          have haw : acrossWordOfWhite G aw.row dw.col hw = aw :=
            acrossWord_unique_of_contains _ _ aw.row dw.col (acrossWordOfWhite_contains G _ _ hw) hinc.1
          have hdw : downWordOfWhite G aw.row dw.col hw = dw :=
            downWord_unique_of_contains _ _ aw.row dw.col (downWordOfWhite_contains G _ _ hw) hinc.2
          rw [haw, hdw, hmaw]
        · intro r ⟨hrCont, hrRook⟩
          dsimp [hasRook] at hrRook
          have hwr : G.isBlack r dw.col = false := dw.allWhite r hrCont.2.1 hrCont.2.2
          rw [dite_pos hwr, decide_eq_true_iff] at hrRook
          have hdw : downWordOfWhite G r dw.col hwr = dw :=
            downWord_unique_of_contains _ _ r dw.col (downWordOfWhite_contains G _ _ hwr) hrCont
          rw [hdw] at hrRook
          have hawEq : acrossWordOfWhite G r dw.col hwr = aw := by
            have := congrArg M.invMatch hrRook
            rw [M.left_inv] at this
            exact this
          have hawCont := acrossWordOfWhite_contains G r dw.col hwr
          rw [hawEq] at hawCont
          exact hawCont.1 }
  left_inv R := by
    apply RookPlacement.ext
    intro r c
    dsimp
    by_cases hw : G.isBlack r c = false
    · rw [dite_pos hw]
      let aw := acrossWordOfWhite G r c hw
      let dw := downWordOfWhite G r c hw
      have hawCont := acrossWordOfWhite_contains G r c hw
      have hdwCont := downWordOfWhite_contains G r c hw
      by_cases hr : R.hasRook r c = true
      · rw [hr, decide_eq_true_iff]
        let found := findUniqueFin (fun c' => aw.containsBool aw.row c' && R.hasRook aw.row c') (by
          rcases R.acrossUnique aw with ⟨c₀, ⟨hc1, hc2⟩, _⟩
          exact ⟨c₀, Bool.and_eq_true _ _ |>.mpr ⟨(containsBool_across_iff aw aw.row c₀).mpr hc1, hc2⟩⟩)
        have hfp := (Bool.and_eq_true _ _).mp found.property
        have hceq : found.val = c := by
          rcases R.acrossUnique aw with ⟨_, _, huniq⟩
          have h1 := huniq found.val ⟨(containsBool_across_iff aw aw.row found.val).mp hfp.1, hfp.2⟩
          have h2 := huniq c ⟨hawCont, hr⟩
          exact h1.trans h2.symm
        apply downWord_unique_of_contains _ _ aw.row found.val
        · exact downWordOfWhite_contains G aw.row found.val _
        · rw [hceq]; exact hdwCont
      · have hrf : R.hasRook r c = false := by
          cases hval : R.hasRook r c
          · rfl
          · exact absurd hval hr
        rw [hrf, decide_eq_false_iff_not]
        intro heq
        let found := findUniqueFin (fun c' => aw.containsBool aw.row c' && R.hasRook aw.row c') (by
          rcases R.acrossUnique aw with ⟨c₀, ⟨hc1, hc2⟩, _⟩
          exact ⟨c₀, Bool.and_eq_true _ _ |>.mpr ⟨(containsBool_across_iff aw aw.row c₀).mpr hc1, hc2⟩⟩)
        have hfp := (Bool.and_eq_true _ _).mp found.property
        have hfc : found.val = c := congrArg DownWord.col heq
        have hrTrue : R.hasRook aw.row found.val = true := hfp.2
        change R.hasRook r found.val = true at hrTrue
        rw [hfc, hrf] at hrTrue
        contradiction
    · rw [dite_neg hw]
      cases hval : R.hasRook r c
      · rfl
      · exact absurd (R.onlyWhite r c hval) hw
  right_inv M := by
    apply WordPerfectMatching.ext
    intro aw
    dsimp
    let dw := M.matchFun aw
    have hinc := (wordsIntersect_iff aw dw).mp (M.incident aw)
    have hw : G.isBlack aw.row dw.col = false := aw.allWhite dw.col hinc.1.2.1 hinc.1.2.2
    let R_inv_col := findUniqueFin
      (fun c => aw.containsBool aw.row c &&
        if hw' : G.isBlack aw.row c = false then
          decide (M.matchFun (acrossWordOfWhite G aw.row c hw') = downWordOfWhite G aw.row c hw')
        else false)
      (by
        refine ⟨dw.col, Bool.and_eq_true _ _ |>.mpr ⟨(containsBool_across_iff aw aw.row dw.col).mpr hinc.1, ?_⟩⟩
        rw [dite_pos hw, decide_eq_true_iff]
        have haw : acrossWordOfWhite G aw.row dw.col hw = aw :=
          acrossWord_unique_of_contains _ _ aw.row dw.col (acrossWordOfWhite_contains G _ _ hw) hinc.1
        have hdw : downWordOfWhite G aw.row dw.col hw = dw :=
          downWord_unique_of_contains _ _ aw.row dw.col (downWordOfWhite_contains G _ _ hw) hinc.2
        rw [haw, hdw])
    have hp := (Bool.and_eq_true _ _).mp R_inv_col.property
    have hcCont : aw.Contains aw.row R_inv_col.val :=
      (containsBool_across_iff aw aw.row R_inv_col.val).mp hp.1
    have hwc : G.isBlack aw.row R_inv_col.val = false := aw.allWhite R_inv_col.val hcCont.2.1 hcCont.2.2
    have hmatch := hp.2
    rw [dite_pos hwc, decide_eq_true_iff] at hmatch
    have haw : acrossWordOfWhite G aw.row R_inv_col.val hwc = aw :=
      acrossWord_unique_of_contains _ _ aw.row R_inv_col.val (acrossWordOfWhite_contains G _ _ hwc) hcCont
    rw [haw] at hmatch
    exact hmatch.symm

/-! ## Exact Matching Recurrence for `|RP(G)|` (`rpCount`) -/

/-- Remove first occurrence of `y` from a list. -/
def listErase [DecidableEq α] : List α → α → List α
  | [], _ => []
  | x :: xs, y => if x = y then xs else x :: listErase xs y

theorem listErase_length_of_mem [DecidableEq α] :
    ∀ {xs : List α} {y : α}, y ∈ xs → (listErase xs y).length + 1 = xs.length
  | x :: xs, y, hm => by
    dsimp [listErase]
    by_cases hxy : x = y
    · rw [ite_pos hxy]
    · rw [ite_neg hxy]
      cases hm with
      | head => exact absurd rfl hxy
      | tail _ hm' => simp [listErase_length_of_mem hm']

theorem mem_listErase_iff_of_nodup [DecidableEq α] :
    ∀ {xs : List α} {y z : α}, NoDup xs → (z ∈ listErase xs y ↔ z ∈ xs ∧ z ≠ y)
  | [], _, _, _ => by simp [listErase]
  | x :: xs, y, z, .cons hnx hnd => by
    dsimp [listErase]
    by_cases hxy : x = y
    · subst hxy
      rw [ite_pos rfl]
      simp only [List.mem_cons]
      constructor
      · intro hz; exact ⟨Or.inr hz, fun hzx => by subst hzx; exact hnx hz⟩
      · rintro ⟨rfl | hz, hne⟩
        · exact absurd rfl hne
        · exact hz
    · rw [ite_neg hxy]
      simp only [List.mem_cons]
      rw [mem_listErase_iff_of_nodup hnd]
      constructor
      · rintro (rfl | ⟨hz, hzy⟩)
        · exact ⟨Or.inl rfl, hxy⟩
        · exact ⟨Or.inr hz, hzy⟩
      · rintro ⟨rfl | hz, hzy⟩
        · exact Or.inl rfl
        · exact Or.inr ⟨hz, hzy⟩

theorem nodup_listErase [DecidableEq α] :
    ∀ {xs : List α} (y : α), NoDup xs → NoDup (listErase xs y)
  | [], _, .nil => .nil
  | x :: xs, y, .cons hnx hnd => by
    dsimp [listErase]
    by_cases hxy : x = y
    · rw [ite_pos hxy]; exact hnd
    · rw [ite_neg hxy]
      refine .cons ?_ (nodup_listErase y hnd)
      intro hm
      exact hnx ((mem_listErase_iff_of_nodup hnd).mp hm).1

/-- Exact matching recurrence along left vertices `0 .. k-1` against available right vertices `avail`. -/
def countMatchingsAux : (k D : Nat) → (Fin k → Fin D → Bool) → List (Fin D) → Nat
  | 0, _, _, _ => 1
  | k + 1, D, adj, avail =>
    let choices := filterSubtype (adj ⟨0, Nat.zero_lt_succ k⟩) avail
    finSum choices.length (fun idx =>
      countMatchingsAux k D (fun i => adj ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)
        (listErase avail (listGetFin choices idx).val))

/-- Exact rook placement count `|RP(G)|` computed from the word-incidence bipartite graph. -/
def rpCount {m n : Nat} (G : Grid m n) : Nat :=
  let awList := finListAcrossWords G
  let dwList := finListDownWords G
  let A := awList.elems.length
  let D := dwList.elems.length
  if A = D then
    let adj (i : Fin A) (j : Fin D) : Bool :=
      wordsIntersect (listGetFin awList.elems i) (listGetFin dwList.elems j)
    countMatchingsAux A D adj (finRangeList D)
  else 0

/-- An injective matching of `Fin k` into `avail : List (Fin D)` respecting `adj`. -/
structure PartialMatching (k D : Nat) (adj : Fin k → Fin D → Bool) (avail : List (Fin D)) where
  toFun : Fin k → Fin D
  mem_avail : ∀ i, toFun i ∈ avail
  inj : ∀ i₁ i₂, toFun i₁ = toFun i₂ → i₁ = i₂
  valid : ∀ i, adj i (toFun i) = true

theorem PartialMatching.ext {k D : Nat} {adj : Fin k → Fin D → Bool} {avail : List (Fin D)}
    {p₁ p₂ : PartialMatching k D adj avail} (h : ∀ i, p₁.toFun i = p₂.toFun i) : p₁ = p₂ := by
  have hf : p₁.toFun = p₂.toFun := funext h
  cases p₁; cases p₂; subst hf; rfl

/-- Helper shifting a function along `Fin (k + 1)` by pattern-matching `0` vs `v + 1`. -/
def consFinFun {k : Nat} {β : Type} (y0 : β) (f : Fin k → β) : Fin (k + 1) → β
  | ⟨0, _⟩ => y0
  | ⟨v + 1, hv⟩ => f ⟨v, Nat.lt_of_succ_lt_succ hv⟩

theorem PartialMatching.heq_ext {k D : Nat} {adj : Fin k → Fin D → Bool}
    {av₁ av₂ : List (Fin D)} {P : PartialMatching k D adj av₁}
    {Q : PartialMatching k D adj av₂} (h : av₁ = av₂)
    (hfun : ∀ i, P.toFun i = Q.toFun i) : HEq P Q := by
  cases h
  exact heq_of_eq (PartialMatching.ext hfun)

/-- Bijection between `PartialMatching k D adj avail` and `Fin (countMatchingsAux k D adj avail)`. -/
def partialMatchingEquivFin :
    (k D : Nat) → (adj : Fin k → Fin D → Bool) → (avail : List (Fin D)) → NoDup avail →
      PartialMatching k D adj avail ≃ Fin (countMatchingsAux k D adj avail)
  | 0, _, _, _, _ => {
      toFun := fun _ => ⟨0, Nat.zero_lt_one⟩
      invFun := fun _ => {
        toFun := fun i => nomatch i
        mem_avail := fun i => nomatch i
        inj := fun i => nomatch i
        valid := fun i => nomatch i
      }
      left_inv := fun _ => by apply PartialMatching.ext; intro i; exact nomatch i
      right_inv := fun ⟨v, hv⟩ => by
        apply Fin.ext
        change v < 1 at hv
        change 0 = v
        omega
    }
  | k + 1, D, adj, avail, hnd =>
    let zeroIdx : Fin (k + 1) := ⟨0, Nat.zero_lt_succ k⟩
    let choices := filterSubtype (adj zeroIdx) avail
    let hndChoices : NoDup choices := nodup_filterSubtype (adj zeroIdx) hnd
    let adj' : Fin k → Fin D → Bool := fun i => adj ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩
    let splitEquiv : PartialMatching (k + 1) D adj avail ≃
        ((idx : Fin choices.length) × PartialMatching k D adj' (listErase avail (listGetFin choices idx).val)) := {
      toFun := fun P =>
        let y0 : { y : Fin D // adj zeroIdx y = true } := ⟨P.toFun zeroIdx, P.valid zeroIdx⟩
        have hy0Mem : y0 ∈ choices := (mem_filterSubtype_iff _ avail y0).mpr (P.mem_avail zeroIdx)
        let idx := listIdxOf choices y0 hy0Mem
        have hgetEq : listGetFin choices idx = y0 := listGetFin_idxOf choices y0 hy0Mem
        ⟨idx, {
          toFun := fun i => P.toFun ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩
          mem_avail := fun i => by
            rw [hgetEq, mem_listErase_iff_of_nodup hnd]
            refine ⟨P.mem_avail _, ?_⟩
            intro heq
            have hi := P.inj _ _ heq
            have hv := congrArg Fin.val hi
            dsimp [zeroIdx] at hv; omega
          inj := fun i₁ i₂ heq => by
            have hi := P.inj _ _ heq
            have hv := congrArg Fin.val hi
            dsimp at hv
            exact Fin.ext (Nat.add_right_cancel hv)
          valid := fun i => P.valid ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩
        }⟩
      invFun := fun ⟨idx, P'⟩ =>
        let y0 := listGetFin choices idx
        have hy0Avail : y0.val ∈ avail :=
          (mem_filterSubtype_iff _ avail y0).mp (listGetFin_mem choices idx)
        { toFun := consFinFun y0.val P'.toFun
          mem_avail := fun
            | ⟨0, _⟩ => hy0Avail
            | ⟨v + 1, hv⟩ =>
              ((mem_listErase_iff_of_nodup hnd).mp (P'.mem_avail ⟨v, Nat.lt_of_succ_lt_succ hv⟩)).1
          inj := fun i₁ i₂ heq => by
            rcases i₁ with ⟨v₁, h1⟩
            rcases i₂ with ⟨v₂, h2⟩
            cases v₁ with
            | zero =>
              cases v₂ with
              | zero => rfl
              | succ v₂' =>
                dsimp [consFinFun] at heq
                have hm := ((mem_listErase_iff_of_nodup hnd).mp (P'.mem_avail ⟨v₂', Nat.lt_of_succ_lt_succ h2⟩)).2
                exact absurd heq.symm hm
            | succ v₁' =>
              cases v₂ with
              | zero =>
                dsimp [consFinFun] at heq
                have hm := ((mem_listErase_iff_of_nodup hnd).mp (P'.mem_avail ⟨v₁', Nat.lt_of_succ_lt_succ h1⟩)).2
                exact absurd heq hm
              | succ v₂' =>
                dsimp [consFinFun] at heq
                have hi := P'.inj _ _ heq
                have hv := congrArg Fin.val hi
                dsimp at hv
                exact Fin.ext (congrArg (· + 1) hv)
          valid := fun
            | ⟨0, _⟩ => y0.property
            | ⟨v + 1, hv⟩ => P'.valid ⟨v, Nat.lt_of_succ_lt_succ hv⟩ }
      left_inv := fun P => by
        apply PartialMatching.ext
        intro i
        rcases i with ⟨v, hv⟩
        cases v with
        | zero =>
          dsimp [consFinFun]
          have hget := listGetFin_idxOf choices ⟨P.toFun zeroIdx, P.valid zeroIdx⟩
            ((mem_filterSubtype_iff _ avail _).mpr (P.mem_avail zeroIdx))
          exact congrArg Subtype.val hget
        | succ _ => rfl
      right_inv := fun ⟨idx, P'⟩ => by
        dsimp
        let y0 := listGetFin choices idx
        have hidx : listIdxOf choices y0 (listGetFin_mem choices idx) = idx :=
          listIdxOf_getFin choices hndChoices idx
        refine Sigma.ext hidx ?_
        apply PartialMatching.heq_ext (congrArg (fun i => listErase avail (listGetFin choices i).val) hidx)
        intro _
        rfl
    }
    let recEquiv (idx : Fin choices.length) :=
      partialMatchingEquivFin k D adj' (listErase avail (listGetFin choices idx).val)
        (nodup_listErase _ hnd)
    splitEquiv.trans ((Equiv.sigmaCongrRight recEquiv).trans (finSigmaEquiv choices.length _))

/-- Surjectivity from injectivity on `Fin A`: every injective `f : Fin A → Fin A` is surjective. -/
theorem injective_surjective_fin :
    ∀ {A : Nat} (f : Fin A → Fin A), (∀ i₁ i₂, f i₁ = f i₂ → i₁ = i₂) → ∀ y : Fin A, ∃ x : Fin A, f x = y := by
  intro A f hinj y
  suffices hgen : ∀ (k : Nat) (xs : List (Fin A)), NoDup xs → xs.length ≤ k →
      ∀ (g : Fin k → Fin A), (∀ i, g i ∈ xs) → (∀ i₁ i₂, g i₁ = g i₂ → i₁ = i₂) →
      ∀ z ∈ xs, ∃ i : Fin k, g i = z by
    exact hgen A (finRangeList A) (finRangeList_nodup A)
      (by rw [finRangeList_length]; exact Nat.le_refl A) f
      (fun i => finRangeList_complete A (f i)) hinj y (finRangeList_complete A y)
  intro k
  induction k with
  | zero =>
    intro xs _ hlen _ _ _ z hz
    cases xs with
    | nil => nomatch hz
    | cons _ _ => simp at hlen
  | succ k ih =>
    intro xs hnd hlen g hmem hginj z hz
    let y0 := g ⟨0, Nat.zero_lt_succ k⟩
    by_cases hzy : z = y0
    · exact ⟨⟨0, Nat.zero_lt_succ k⟩, hzy.symm⟩
    · have hy0 : y0 ∈ xs := hmem ⟨0, Nat.zero_lt_succ k⟩
      have hlen' : (listErase xs y0).length ≤ k := by
        have he := listErase_length_of_mem hy0
        omega
      let g' (i : Fin k) : Fin A := g ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩
      have hmem' : ∀ i : Fin k, g' i ∈ listErase xs y0 := by
        intro i
        rw [mem_listErase_iff_of_nodup hnd]
        refine ⟨hmem _, ?_⟩
        intro heq
        have hi := hginj _ _ heq
        have hv := congrArg Fin.val hi
        dsimp at hv; omega
      have hginj' : ∀ i₁ i₂ : Fin k, g' i₁ = g' i₂ → i₁ = i₂ := by
        intro i₁ i₂ heq
        have hi := hginj _ _ heq
        have hv := congrArg Fin.val hi
        dsimp at hv
        exact Fin.ext (by omega)
      have hz' : z ∈ listErase xs y0 :=
        (mem_listErase_iff_of_nodup hnd).mpr ⟨hz, hzy⟩
      rcases ih (listErase xs y0) (nodup_listErase y0 hnd) hlen' g' hmem' hginj' z hz' with ⟨i, hi⟩
      exact ⟨⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩, hi⟩

/-- Helper connecting `WordPerfectMatching G` to `countMatchingsAux` with free `A, D` parameters. -/
def wordMatchingEquivCount {m n : Nat} (G : Grid m n)
    (awElems : List (AcrossWord G)) (dwElems : List (DownWord G))
    (eA : AcrossWord G ≃ Fin awElems.length) (eD : DownWord G ≃ Fin dwElems.length)
    (heA : ∀ i, eA.invFun i = listGetFin awElems i)
    (heD : ∀ j, eD.invFun j = listGetFin dwElems j) :
    WordPerfectMatching G ≃
      Fin (if awElems.length = dwElems.length then
        countMatchingsAux awElems.length dwElems.length
          (fun i j => wordsIntersect (listGetFin awElems i) (listGetFin dwElems j))
          (finRangeList dwElems.length)
      else 0) :=
  go awElems.length dwElems.length eA eD
    (fun i j => wordsIntersect (eA.invFun i) (eD.invFun j))
    (fun i j => wordsIntersect (listGetFin awElems i) (listGetFin dwElems j))
    (fun _ _ => rfl)
    (by
      funext i j
      rw [heA i, heD j])
where
  go (A D : Nat) (eA : AcrossWord G ≃ Fin A) (eD : DownWord G ≃ Fin D)
      (adj adj' : Fin A → Fin D → Bool)
      (hInc : ∀ i j, adj i j = wordsIntersect (eA.invFun i) (eD.invFun j))
      (hadj : adj = adj') :
      WordPerfectMatching G ≃
        Fin (if A = D then countMatchingsAux A D adj' (finRangeList D) else 0) := by
    cases hadj
    by_cases hAD : A = D
    · subst hAD
      rw [ite_pos rfl]
      let wmToPm : WordPerfectMatching G ≃ PartialMatching A A adj (finRangeList A) := {
        toFun := fun M => {
          toFun := fun i => eD.toFun (M.matchFun (eA.invFun i))
          mem_avail := fun _ => finRangeList_complete A _
          inj := fun i₁ i₂ heq => by
            have h1 := eD.injective heq
            have h2 := congrArg M.invMatch h1
            rw [M.left_inv, M.left_inv] at h2
            exact eA.symm.injective h2
          valid := fun i => by
            rw [hInc, eD.left_inv]
            exact M.incident (eA.invFun i)
        }
        invFun := fun P =>
          let ginv (j : Fin A) : Fin A :=
            (findUniqueFin (fun i : Fin A => decide (P.toFun i = j)) (by
              rcases injective_surjective_fin P.toFun P.inj j with ⟨x, hx⟩
              exact ⟨x, decide_eq_true hx⟩)).val
          have g_right : ∀ j : Fin A, P.toFun (ginv j) = j := fun j =>
            of_decide_eq_true (findUniqueFin (fun i : Fin A => decide (P.toFun i = j)) _).property
          have g_left : ∀ i : Fin A, ginv (P.toFun i) = i := fun i =>
            P.inj _ _ (g_right (P.toFun i))
          { matchFun := fun aw => eD.invFun (P.toFun (eA.toFun aw))
            invMatch := fun dw => eA.invFun (ginv (eD.toFun dw))
            left_inv := fun aw => by rw [eD.right_inv, g_left, eA.left_inv]
            right_inv := fun dw => by rw [eA.right_inv, g_right, eD.left_inv]
            incident := fun aw => by
              have hv := P.valid (eA.toFun aw)
              rw [hInc, eA.left_inv] at hv
              exact hv }
        left_inv := fun M => by
          apply WordPerfectMatching.ext
          intro aw
          dsimp
          rw [eA.left_inv, eD.left_inv]
        right_inv := fun P => by
          apply PartialMatching.ext
          intro i
          dsimp
          rw [eA.right_inv, eD.right_inv]
      }
      exact wmToPm.trans (partialMatchingEquivFin A A adj (finRangeList A) (finRangeList_nodup A))
    · rw [ite_neg hAD]
      exact {
        toFun := fun M => by
          exfalso
          let bij : AcrossWord G ≃ DownWord G := ⟨M.matchFun, M.invMatch, M.left_inv, M.right_inv⟩
          exact hAD (finEquivUnique (eA.symm.trans (bij.trans eD)))
        invFun := fun z => nomatch z
        left_inv := fun M => by
          exfalso
          let bij : AcrossWord G ≃ DownWord G := ⟨M.matchFun, M.invMatch, M.left_inv, M.right_inv⟩
          exact hAD (finEquivUnique (eA.symm.trans (bij.trans eD)))
        right_inv := fun z => nomatch z
      }

/-- First-principles theorem: for EVERY crossword grid `G`, `RookPlacement G ≃ Fin (rpCount G)`. -/
def rookPlacementEquivFinRpCount {m n : Nat} (G : Grid m n) :
    RookPlacement G ≃ Fin (rpCount G) :=
  let awList := finListAcrossWords G
  let dwList := finListDownWords G
  (rookPlacementEquivWordMatching G).trans
    (wordMatchingEquivCount G awList.elems dwList.elems awList.equivFin dwList.equivFin
      (fun _ => rfl) (fun _ => rfl))

theorem rookPlacement_hasExactCard {m n : Nat} (G : Grid m n) :
    HasExactCard (RookPlacement G) (rpCount G) :=
  ⟨rookPlacementEquivFinRpCount G⟩

/-! ## Permanent by deletion of one column at a time -/

/-- Sum over positions. The callback receives the chosen entry and the residual list.
Equal entries still contribute once per position. -/
def pickSum {α : Type} (xs : List α) (f : α → List α → Nat) : Nat :=
  match xs with
  | [] => 0
  | x :: tail => f x tail + pickSum tail (fun y ys => f y (x :: ys))

theorem pickSum_congr {α : Type} (xs : List α) {f g : α → List α → Nat}
    (h : ∀ x ys, ys.length + 1 = xs.length → f x ys = g x ys) :
    pickSum xs f = pickSum xs g := by
  induction xs generalizing f g with
  | nil => rfl
  | cons a as ih =>
    simp only [pickSum]
    rw [h a as rfl, ih]
    intro x ys hy
    exact h x (a :: ys) (congrArg (· + 1) hy)

theorem pickSum_perm {α : Type} {xs ys : List α} (h : xs.Perm ys)
    (f : α → List α → Nat)
    (hf : ∀ x {ls rs}, ls.Perm rs → f x ls = f x rs) :
    pickSum xs f = pickSum ys f := by
  induction h generalizing f with
  | nil => rfl
  | cons a h ih =>
    simp only [pickSum]
    rw [hf a h, ih]
    intro x ls rs hp
    exact hf x (.cons a hp)
  | swap a b ts =>
    simp only [pickSum]
    have htail := pickSum_congr ts
      (f := fun x ls => f x (b :: a :: ls))
      (g := fun x ls => f x (a :: b :: ls))
      (fun x ls _ => hf x (.swap a b ls))
    rw [htail, Nat.add_left_comm]
  | trans _ _ ih₁ ih₂ =>
    exact (ih₁ f hf).trans (ih₂ f hf)

theorem pickSum_map {α β : Type} (xs : List α) (g : α → β) (f : β → List β → Nat) :
    pickSum (xs.map g) f = pickSum xs (fun x ys => f (g x) (ys.map g)) := by
  induction xs generalizing f with
  | nil => rfl
  | cons a as ih =>
    simp only [List.map_cons, pickSum, ih]

theorem pickSum_erase {α : Type} [DecidableEq α] (xs pre : List α)
    (h : NoDup (pre ++ xs)) (f : α → List α → Nat) :
    pickSum xs (fun x ys => f x (pre ++ ys)) =
      (xs.map fun x => f x (listErase (pre ++ xs) x)).sum := by
  induction xs generalizing pre with
  | nil => rfl
  | cons a as ih =>
    have hhead : listErase (pre ++ a :: as) a = pre ++ as := by
      induction pre with
      | nil => simp [listErase]
      | cons b bs step =>
        cases h with
        | cons hb ht =>
          have hab : b ≠ a := by
            intro e
            subst b
            exact hb (List.mem_append_right _ (List.Mem.head _))
          simp [listErase, hab, step ht]
    simp only [pickSum, List.map_cons, List.sum_cons, hhead]
    congr 1
    have hh : NoDup ((pre ++ [a]) ++ as) := by simpa using h
    simpa only [List.append_assoc, List.singleton_append] using ih (pre ++ [a]) hh

theorem finSum_listGetFin {α : Type} (xs : List α) (f : α → Nat) :
    finSum xs.length (fun i => f (listGetFin xs i)) = (xs.map f).sum := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    change f x + finSum xs.length (fun i => f (listGetFin xs i)) = f x + (xs.map f).sum
    rw [ih]

theorem sum_filterSubtype {α : Type} (xs : List α) (p : α → Bool) (f : α → Nat) :
    ((filterSubtype p xs).map (fun x => f x.val)).sum =
      (xs.map (fun x => if p x then f x else 0)).sum := by
  induction xs with
  | nil => rfl
  | cons a as ih =>
    cases h : p a <;> simp only [filterSubtype, h, Bool.false_eq_true,
      dite_false, dite_true, List.map_cons, List.sum_cons, ite_false, ite_true, Nat.zero_add, ih]

/-- The row bits of a column, with the first row at the low bit. -/
def columnBits : (k : Nat) → (Fin k → Bool) → Nat
  | 0, _ => 0
  | k + 1, f => (if f ⟨0, Nat.zero_lt_succ k⟩ then 1 else 0) +
      2 * columnBits k (fun i => f i.succ)

theorem columnBits_head (k : Nat) (f : Fin (k + 1) → Bool) :
    (columnBits (k + 1) f % 2 == 1) = f ⟨0, Nat.zero_lt_succ k⟩ := by
  rw [columnBits]
  cases f ⟨0, Nat.zero_lt_succ k⟩
  · apply beq_eq_false_iff_ne.mpr
    simp only [Bool.false_eq_true, ite_false, Nat.zero_add]
    omega
  · apply beq_iff_eq.mpr
    simp only [ite_true]
    omega

theorem columnBits_tail (k : Nat) (f : Fin (k + 1) → Bool) :
    columnBits (k + 1) f / 2 = columnBits k (fun i => f i.succ) := by
  rw [columnBits]
  cases f ⟨0, Nat.zero_lt_succ k⟩ <;> simp only [Bool.false_eq_true, ite_false, ite_true, Nat.zero_add] <;> omega

/-- The column-signature recurrence before dropping states with an expired column. -/
def signatureCount : Nat → List Nat → Nat
  | 0, _ => 1
  | k + 1, cs => pickSum cs fun c rest =>
      if c % 2 == 1 then signatureCount k (rest.map (· / 2)) else 0

theorem signatureCount_perm (k : Nat) {cs ds : List Nat} (h : cs.Perm ds) :
    signatureCount k cs = signatureCount k ds := by
  induction k generalizing cs ds with
  | zero => rfl
  | succ k ih =>
    simp only [signatureCount]
    apply pickSum_perm h
    intro x ls rs hp
    rw [ih (hp.map (· / 2))]

theorem signatureCount_eq_countMatchingsAux :
    ∀ (k D : Nat) (adj : Fin k → Fin D → Bool) (avail : List (Fin D)),
      NoDup avail →
      signatureCount k (avail.map fun j => columnBits k (fun i => adj i j)) =
        countMatchingsAux k D adj avail := by
  intro k
  induction k with
  | zero => intros; rfl
  | succ k ih =>
    intro D adj avail h
    rw [signatureCount, pickSum_map]
    simp only [columnBits_head, List.map_map, Function.comp_def, columnBits_tail]
    have hpick := pickSum_erase avail [] (show NoDup ([] ++ avail) from h)
      (fun j rest => if adj ⟨0, Nat.zero_lt_succ k⟩ j
        then signatureCount k (rest.map fun q => columnBits k (fun i => adj i.succ q)) else 0)
    simp only [List.nil_append] at hpick
    rw [hpick]
    rw [countMatchingsAux]
    let p := adj ⟨0, Nat.zero_lt_succ k⟩
    let F := fun j => countMatchingsAux k D (fun i => adj i.succ) (listErase avail j)
    change _ = finSum (filterSubtype p avail).length
      (fun i => F (listGetFin (filterSubtype p avail) i).val)
    rw [finSum_listGetFin (filterSubtype p avail) (fun j => F j.val), sum_filterSubtype]
    congr 1
    apply List.map_congr_left
    intro j _
    have hh := ih D (fun (i : Fin k) q => adj i.succ q) (listErase avail j) (nodup_listErase j h)
    simp only [p, F, hh]

/-! ## Executable recurrence with aggregation at each row -/

def picks {α : Type} : List α → List (α × List α)
  | [] => []
  | x :: xs => (x, xs) :: (picks xs).map (fun (y, ys) => (y, x :: ys))

theorem picks_sum {α : Type} (xs : List α) (f : α → List α → Nat) :
    ((picks xs).map (fun (x, ys) => f x ys)).sum = pickSum xs f := by
  induction xs generalizing f with
  | nil => rfl
  | cons a as ih =>
    simp only [picks, List.map_cons, List.sum_cons, List.map_map, Function.comp_def, pickSum]
    rw [← ih]

theorem picks_length {α : Type} {xs : List α} {p : α × List α}
    (hp : p ∈ picks xs) : p.2.length + 1 = xs.length := by
  induction xs generalizing p with
  | nil => cases hp
  | cons a as ih =>
    simp only [picks, List.mem_cons, List.mem_map] at hp
    rcases hp with rfl | ⟨q, hq, rfl⟩
    · rfl
    · exact congrArg (· + 1) (ih hq)

theorem mem_picks_of_mem_other {α : Type} [DecidableEq α] (x : α) {cs : List α}
    (hx : x ∈ cs) : ∀ (p : α × List α), p ∈ picks cs → p.1 ≠ x → x ∈ p.2 := by
  induction cs with
  | nil => cases hx
  | cons a as ih =>
    intro p hp hn
    simp only [picks, List.mem_cons, List.mem_map] at hp
    rcases hp with rfl | ⟨q, hq, rfl⟩
    · rcases List.mem_cons.mp hx with e | e
      · exact (hn e.symm).elim
      · exact e
    · rcases List.mem_cons.mp hx with e | e
      · simp [e]
      · exact List.Mem.tail _ (ih e q hq hn)

theorem signatureCount_expired (k : Nat) (cs : List Nat)
    (hlen : cs.length = k) (hz : 0 ∈ cs) : signatureCount k cs = 0 := by
  induction k generalizing cs with
  | zero => simp [List.eq_nil_of_length_eq_zero hlen] at hz
  | succ k ih =>
    rw [signatureCount, ← picks_sum]
    apply List.sum_eq_zero_iff_forall_eq_nat.mpr
    intro v hv
    rcases List.mem_map.mp hv with ⟨⟨c, rest⟩, hp, rfl⟩
    change (if c % 2 == 1 then signatureCount k (rest.map (· / 2)) else 0) = 0
    split
    · rename_i hc
      have hc0 : c ≠ 0 := by intro e; subst c; contradiction
      have hm := mem_picks_of_mem_other 0 hz (c, rest) hp hc0
      have hh := picks_length hp
      change rest.length + 1 = cs.length at hh
      exact ih _ (by simp; omega) (List.mem_map.mpr ⟨0, hm, rfl⟩)
    · rfl

abbrev State := List Nat × Nat

def shiftColumn (cs : List Nat) : List Nat := cs.map (· / 2)

def expandState (s : State) : List State :=
  (picks s.1).filterMap fun (c, rest) =>
    if c % 2 == 1 then
      let cs := shiftColumn rest
      if cs.head? == some 0 then none else some (cs, s.2)
    else none

def insertRun {α : Type} (le : α → α → Bool) (x : α) (mergeTail : List α → List α) :
    List α → List α
  | [] => x :: mergeTail []
  | y :: ys => if le x y then x :: mergeTail (y :: ys) else y :: insertRun le x mergeTail ys

/-- Merge two runs by nested structural recursion, so concrete merges reduce in the kernel. -/
def mergeRuns {α : Type} (le : α → α → Bool) : List α → List α → List α
  | [], ys => ys
  | x :: xs, ys => insertRun le x (mergeRuns le xs) ys

theorem mergeRuns_perm {α : Type} (le : α → α → Bool) (xs ys : List α) :
    (mergeRuns le xs ys).Perm (xs ++ ys) := by
  induction xs generalizing ys with
  | nil => simp [mergeRuns]
  | cons x xs ih =>
    induction ys with
    | nil => simpa only [mergeRuns, insertRun, List.cons_append] using (ih []).cons x
    | cons y ys ihy =>
      rw [mergeRuns, insertRun]
      split
      · exact (ih _).cons x
      · exact (ihy.cons y).trans (List.perm_middle.symm)

def mergePairs {α : Type} (le : α → α → Bool) : List (List α) → List (List α)
  | x :: y :: xs => mergeRuns le x y :: mergePairs le xs
  | xs => xs

theorem mergePairs_perm {α : Type} (le : α → α → Bool) :
    ∀ xs : List (List α), (mergePairs le xs).flatten.Perm xs.flatten
  | [] => .nil
  | [_] => .refl _
  | x :: y :: xs => by
    simp only [mergePairs, List.flatten_cons]
    rw [← List.append_assoc]
    exact (mergeRuns_perm le x y).append (mergePairs_perm le xs)

def combineRuns {α : Type} (le : α → α → Bool) : Nat → List (List α) → List α
  | 0, xs => xs.flatten
  | _ + 1, [] => []
  | _ + 1, [xs] => xs
  | fuel + 1, x :: y :: xs => combineRuns le fuel (mergePairs le (x :: y :: xs))

theorem combineRuns_perm {α : Type} (le : α → α → Bool) (fuel : Nat) (xs : List (List α)) :
    (combineRuns le fuel xs).Perm xs.flatten := by
  induction fuel generalizing xs with
  | zero => rfl
  | succ fuel ih =>
    rcases xs with _ | ⟨a, _ | ⟨b, cs⟩⟩
    · rfl
    · simp [combineRuns]
    · exact (ih _).trans (mergePairs_perm le (a :: b :: cs))

def sortRuns {α : Type} (xs : List α) (le : α → α → Bool) : List α :=
  combineRuns le 24 (xs.map fun x => [x])

theorem sortRuns_perm {α : Type} (xs : List α) (le : α → α → Bool) :
    (sortRuns xs le).Perm xs := by
  have hf : (xs.map fun x => [x]).flatten = xs := by
    induction xs with
    | nil => rfl
    | cons x xs ih => simp [ih]
  have h := combineRuns_perm le 24 (xs.map fun x => [x])
  rw [hf] at h
  exact h

/-- Sort states, then add multiplicities of identical residual column lists. -/
def gather (cs : List Nat) (w : Nat) : List State → List State
  | [] => [(cs, w)]
  | (ds, v) :: ss =>
      if cs == ds then gather cs (w + v) ss else (cs, w) :: gather ds v ss

def coalesce (ss : List State) : List State :=
  match sortRuns ss (fun s t => compare s.1 t.1 != .gt) with
  | [] => []
  | (cs, w) :: rest => gather cs w rest

def sweepStep (ss : List State) : List State := coalesce (ss.flatMap expandState)

def sweepRows : Nat → List State → List State
  | 0, ss => ss
  | k + 1, ss => sweepRows k (sweepStep ss)

def sweepCount (blocks : List Nat) (cs : List Nat) : Nat :=
  let initial := [(sortRuns cs (· ≤ ·), 1)]
  let final := blocks.foldl (fun states rows => sweepRows rows states) initial
  (final.map Prod.snd).sum

def stateTotal (k : Nat) (ss : List State) : Nat :=
  (ss.map fun (cs, w) => w * signatureCount k cs).sum

theorem stateTotal_append (k : Nat) (ss ts : List State) :
    stateTotal k (ss ++ ts) = stateTotal k ss + stateTotal k ts := by
  simp [stateTotal]

theorem stateTotal_cons (k : Nat) (s : State) (ss : List State) :
    stateTotal k (s :: ss) = s.2 * signatureCount k s.1 + stateTotal k ss := rfl

theorem gather_total (k : Nat) (ss : List State) (cs : List Nat) (w : Nat) :
    stateTotal k (gather cs w ss) = stateTotal k ((cs, w) :: ss) := by
  induction ss generalizing cs w with
  | nil => rfl
  | cons s ss ih =>
    rcases s with ⟨ds, v⟩
    simp only [gather]
    split
    · rename_i he
      obtain rfl : cs = ds := beq_iff_eq.mp he
      rw [ih]
      simp only [stateTotal_cons, Nat.add_mul, Nat.add_assoc]
    · rw [stateTotal_cons, ih]
      rfl

theorem perm_sum {xs ys : List Nat} (h : xs.Perm ys) : xs.sum = ys.sum := by
  induction h with
  | nil => rfl
  | cons _ _ ih => simp [ih]
  | swap a b xs => simp [Nat.add_left_comm]
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂

theorem coalesce_total (k : Nat) (ss : List State) :
    stateTotal k (coalesce ss) = stateTotal k ss := by
  have hp := sortRuns_perm ss (fun s t => compare s.1 t.1 != .gt)
  have he : stateTotal k _ = stateTotal k ss :=
    perm_sum (hp.map (fun s => s.2 * signatureCount k s.1))
  simp only [coalesce]
  split
  · rename_i h
    exact h ▸ he
  · rename_i hd w ts h
    rw [gather_total]
    exact h ▸ he

def uniformLength (k : Nat) (ss : List State) : Prop :=
  ∀ s ∈ ss, s.1.length = k

theorem gather_length {k : Nat} (ss : List State) (cs : List Nat) (w : Nat)
    (hcs : cs.length = k) (h : uniformLength k ss) :
    uniformLength k (gather cs w ss) := by
  induction ss generalizing cs w with
  | nil =>
    intro a ha
    rcases List.mem_singleton.mp ha with rfl
    exact hcs
  | cons s ss ih =>
    rcases s with ⟨ds, v⟩
    have hd := h _ (List.Mem.head _)
    have ht : uniformLength k ss := fun a ha => h a (List.Mem.tail _ ha)
    simp only [gather]
    split
    · exact ih cs (w + v) hcs ht
    · intro a ha
      rcases List.mem_cons.mp ha with rfl | ha
      · exact hcs
      · exact ih ds v hd ht a ha

theorem coalesce_length {k : Nat} (ss : List State) (h : uniformLength k ss) :
    uniformLength k (coalesce ss) := by
  have hp := sortRuns_perm ss (fun s t => compare s.1 t.1 != .gt)
  have hs : uniformLength k _ := fun a ha => h a (hp.mem_iff.mp ha)
  unfold coalesce
  split
  · intro a ha
    cases ha
  · rename_i cs w rest hsort
    rw [hsort] at hs
    exact gather_length _ _ _ (hs _ (List.Mem.head _)) (fun a ha => hs a (List.Mem.tail _ ha))

theorem expand_length {k : Nat} (s : State) (h : s.1.length = k + 1) :
    uniformLength k (expandState s) := by
  intro out ho
  rcases List.mem_filterMap.mp ho with ⟨⟨c, cs⟩, hp, hout⟩
  have hcs := picks_length hp
  change cs.length + 1 = s.1.length at hcs
  dsimp only at hout
  split at hout
  · split at hout
    · contradiction
    · cases hout
      simp [shiftColumn]
      omega
  · contradiction

theorem filterMap_sum {α β : Type} (xs : List α) (f : α → Option β) (v : β → Nat) :
    ((xs.filterMap f).map v).sum = (xs.map fun x => (f x).elim 0 v).sum := by
  induction xs with
  | nil => rfl
  | cons a as ih =>
    cases h : f a <;> simp [h, ih]

theorem mul_sum (a : Nat) (xs : List Nat) :
    a * xs.sum = (xs.map (a * ·)).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [Nat.mul_add, ih]

theorem expand_total (k : Nat) (s : State) (h : s.1.length = k + 1) :
    stateTotal k (expandState s) = s.2 * signatureCount (k + 1) s.1 := by
  unfold stateTotal expandState
  rw [filterMap_sum, signatureCount, ← picks_sum, mul_sum]
  simp only [List.map_map]
  congr 1
  apply List.map_congr_left
  rintro ⟨c, cs⟩ hp
  dsimp only [Function.comp_def]
  split
  · split
    · rename_i hz
      have hhead : (shiftColumn cs).head? = some 0 := beq_iff_eq.mp hz
      have hlen := picks_length hp
      change cs.length + 1 = s.1.length at hlen
      have hzero : 0 ∈ shiftColumn cs := List.mem_of_head? hhead
      rw [← show shiftColumn cs = cs.map (· / 2) from rfl,
        signatureCount_expired _ _ (by simp [shiftColumn]; omega) hzero, Nat.mul_zero]
      rfl
    · rfl
  · simp

theorem sweepStep_length {k : Nat} {ss : List State} (h : uniformLength (k + 1) ss) :
    uniformLength k (sweepStep ss) := by
  apply coalesce_length
  intro s hs
  rcases List.mem_flatMap.mp hs with ⟨t, ht, hs⟩
  exact expand_length t (h t ht) s hs

theorem sweepStep_total (k : Nat) (ss : List State) (h : uniformLength (k + 1) ss) :
    stateTotal k (sweepStep ss) = stateTotal (k + 1) ss := by
  unfold sweepStep
  rw [coalesce_total]
  induction ss with
  | nil => rfl
  | cons s ss ih =>
    rw [List.flatMap_cons, stateTotal_append, stateTotal_cons, expand_total k s (h _ (.head _))]
    rw [ih (fun t ht => h t (.tail _ ht))]

theorem sweepRows_spec (rows k : Nat) (ss : List State) (h : uniformLength (k + rows) ss) :
    uniformLength k (sweepRows rows ss) ∧
      stateTotal k (sweepRows rows ss) = stateTotal (k + rows) ss := by
  induction rows generalizing ss with
  | zero => exact ⟨h, rfl⟩
  | succ rows ih =>
    have hh := ih (sweepStep ss) (sweepStep_length h)
    exact ⟨hh.1, hh.2.trans (sweepStep_total (k + rows) ss h)⟩

theorem sweepBlocks_spec (blocks : List Nat) (ss : List State)
    (h : uniformLength blocks.sum ss) :
    stateTotal 0 (blocks.foldl (fun states rows => sweepRows rows states) ss) =
      stateTotal blocks.sum ss := by
  induction blocks generalizing ss with
  | nil => rfl
  | cons b bs ih =>
    have hh : uniformLength (bs.sum + b) ss := by
      simpa [List.sum_cons, Nat.add_comm] using h
    have hs := sweepRows_spec b bs.sum ss hh
    rw [List.foldl_cons, ih _ hs.1, hs.2, List.sum_cons, Nat.add_comm]

theorem stateTotal_zero (ss : List State) : stateTotal 0 ss = (ss.map Prod.snd).sum := by
  simp [stateTotal, signatureCount]

theorem sweepCount_eq_signatureCount (blocks cs : List Nat) (h : cs.length = blocks.sum) :
    sweepCount blocks cs = signatureCount blocks.sum cs := by
  unfold sweepCount
  rw [← stateTotal_zero, sweepBlocks_spec]
  · simp only [stateTotal, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
      Nat.one_mul, Nat.add_zero]
    exact signatureCount_perm _ (sortRuns_perm _ _)
  · intro s hs
    rcases List.mem_singleton.mp hs with rfl
    exact (sortRuns_perm _ _).length_eq.trans h

/-! ## Layered geometry and its block permanent

A block on the diagonal contributes its two staircase triangles. For a
block above the diagonal the rectangle is east-to-north. Below the
diagonal it is west-to-south. The word lists omit empty boundary words.
-/

def layeredValue : List Nat → Nat → Nat
  | [], i => i
  | d :: ds, i => if i < d then d - 1 - i else d + layeredValue ds (i - d)

theorem layeredValue_lt (ds : List Nat) (i : Nat) (hi : i < ds.sum) :
    layeredValue ds i < ds.sum := by
  induction ds generalizing i with
  | nil => cases hi
  | cons d ds ih =>
    simp only [List.sum_cons] at hi ⊢
    rw [layeredValue]
    split
    · omega
    · have h := ih (i - d) (by omega)
      omega

theorem layeredValue_involutive (ds : List Nat) (i : Nat) :
    layeredValue ds (layeredValue ds i) = i := by
  induction ds generalizing i with
  | nil => rfl
  | cons d ds ih =>
    by_cases hi : i < d
    · rw [show layeredValue (d :: ds) i = d - 1 - i by rw [layeredValue, ite_pos hi],
        layeredValue, ite_pos (show d - 1 - i < d by omega)]
      omega
    · rw [show layeredValue (d :: ds) i = d + layeredValue ds (i - d) by rw [layeredValue, ite_neg hi],
        layeredValue, ite_neg (show ¬ d + layeredValue ds (i - d) < d by omega)]
      rw [Nat.add_sub_cancel_left, ih]
      omega

/-- Direct sum of the reversals of consecutive intervals of the indicated lengths. -/
def layered (ds : List Nat) : Perm ds.sum where
  toFun i := ⟨layeredValue ds i.val, layeredValue_lt ds _ i.isLt⟩
  invFun i := ⟨layeredValue ds i.val, layeredValue_lt ds _ i.isLt⟩
  left_inv i := Fin.ext (layeredValue_involutive ds i.val)
  right_inv i := Fin.ext (layeredValue_involutive ds i.val)

def Perm.cast {m n : Nat} (h : m = n) (p : Perm m) : Perm n := h ▸ p

theorem layered_grid_symmetric (ds : List Nat) :
    (gridOfPerm (layered ds)).transpose = gridOfPerm (layered ds) := by
  apply congrArg Grid.mk
  funext i j
  apply Bool.eq_iff_iff.mpr
  simp only [gridOfPerm, decide_eq_true_eq]
  constructor
  · intro h
    rw [h]
    exact ((layered ds).left_inv j).symm
  · intro h
    rw [h]
    exact ((layered ds).left_inv i).symm

theorem across_contains_perm {n : Nat} (p : Perm n)
    (a : AcrossWord (gridOfPerm p)) (c : Fin n) :
    a.Contains a.row c ↔
      if a.lo.val = 0 then c.val < (p.toFun a.row).val else (p.toFun a.row).val < c.val := by
  let b := p.toFun a.row
  have hnot : ¬ (a.lo.val ≤ b.val ∧ b.val ≤ a.hi.val) := by
    intro h
    have hw := a.allWhite b h.1 h.2
    have hb : (gridOfPerm p).isBlack a.row b = true := by
      change decide (b = b) = true
      exact decide_eq_true rfl
    exact Bool.noConfusion (hw.symm.trans hb)
  have hb₁ : ∀ h : 0 < a.lo.val, a.lo.val - 1 = b.val := by
    intro h
    have ht := a.leftMax h
    change decide ((⟨a.lo.val - 1, by omega⟩ : Fin n) = b) = true at ht
    exact congrArg Fin.val (of_decide_eq_true ht)
  have hb₂ : ∀ h : a.hi.val + 1 < n, a.hi.val + 1 = b.val := by
    intro h
    have ht := a.rightMax h
    change decide ((⟨a.hi.val + 1, h⟩ : Fin n) = b) = true at ht
    exact congrArg Fin.val (of_decide_eq_true ht)
  change (a.row = a.row ∧ _) ↔ if a.lo.val = 0 then c.val < b.val else b.val < c.val
  simp only [true_and]
  by_cases ha : a.lo.val = 0
  · rw [ite_pos ha]
    have hh : a.hi.val < b.val := by omega
    have hb := hb₂ (Nat.lt_of_le_of_lt (by omega : a.hi.val + 1 ≤ b.val) b.isLt)
    omega
  · rw [ite_neg ha]
    have hl := hb₁ (by omega)
    have hmax : ¬ a.hi.val + 1 < n := by
      intro ht
      have hb := hb₂ ht
      have hle := a.le
      omega
    have hc := c.isLt
    omega

def sideTest (after : Bool) (cell black : Nat) : Bool :=
  if after then decide (black < cell) else decide (cell < black)

/-- An entry of the block matrix. The two flags select the east and south words. -/
def blockEdge : List Nat → Nat → Nat → Bool → Bool → Bool
  | [], _, _, _, _ => false
  | d :: ds, i, j, east, south =>
    if i < d then
      if j < d then
        (!east && !south && decide (i + j + 1 < d)) ||
          (east && south && decide (d < i + j + 1))
      else east && !south
    else if j < d then !east && south
    else blockEdge ds (i - d) (j - d) east south

theorem blockEdge_eq_sides (ds : List Nat) (i j : Nat) (east south : Bool)
    (hi : i < ds.sum) (hj : j < ds.sum) :
    blockEdge ds i j east south =
      (sideTest east j (layeredValue ds i) && sideTest south i (layeredValue ds j)) := by
  induction ds generalizing i j with
  | nil => cases hi
  | cons d ds ih =>
    simp only [List.sum_cons] at hi hj
    by_cases hr : i < d <;> by_cases hc : j < d
    · rw [blockEdge, ite_pos hr, ite_pos hc, layeredValue, ite_pos hr, layeredValue, ite_pos hc]
      cases east <;> cases south <;> apply Bool.eq_iff_iff.mpr <;>
        simp [sideTest] <;> omega
    · rw [blockEdge, ite_pos hr, ite_neg hc, layeredValue, ite_pos hr, layeredValue, ite_neg hc]
      cases east <;> cases south <;> apply Bool.eq_iff_iff.mpr <;>
        simp [sideTest] <;> omega
    · rw [blockEdge, ite_neg hr, ite_pos hc, layeredValue, ite_neg hr, layeredValue, ite_pos hc]
      cases east <;> cases south <;> apply Bool.eq_iff_iff.mpr <;>
        simp [sideTest] <;> omega
    · rw [blockEdge, ite_neg hr, ite_neg hc, layeredValue, ite_neg hr, layeredValue, ite_neg hc]
      rw [ih (i - d) (j - d) (by omega) (by omega)]
      cases east <;> cases south <;> apply Bool.eq_iff_iff.mpr <;>
        simp [sideTest] <;> omega

theorem across_contains_side {n : Nat} (p : Perm n)
    (a : AcrossWord (gridOfPerm p)) (c : Fin n) :
    a.Contains a.row c ↔ sideTest (a.lo.val != 0) c.val (p.toFun a.row).val = true := by
  rw [across_contains_perm]
  by_cases h : a.lo.val = 0 <;> simp [h, sideTest]

theorem layered_words_blockEdge (ds : List Nat)
    (a : AcrossWord (gridOfPerm (layered ds))) (b : DownWord (gridOfPerm (layered ds))) :
    wordsIntersect a b = blockEdge ds a.row.val b.col.val (a.lo.val != 0) (b.lo.val != 0) := by
  have hb : b.Contains a.row b.col ↔
      sideTest (b.lo.val != 0) a.row.val (layeredValue ds b.col.val) = true := by
    let c := (downWordEquivTransposeAcross (gridOfPerm (layered ds))).toFun b
    have h (G : Grid ds.sum ds.sum) (he : G = gridOfPerm (layered ds))
        (w : AcrossWord G) (r : Fin ds.sum) :
        w.Contains w.row r ↔
          sideTest (w.lo.val != 0) r.val (layeredValue ds w.row.val) = true := by
      subst G
      exact across_contains_side (layered ds) w r
    exact h _ (layered_grid_symmetric ds) c a.row
  apply Bool.eq_iff_iff.mpr
  rw [wordsIntersect_iff, blockEdge_eq_sides ds _ _ _ _ a.row.isLt b.col.isLt,
    Bool.and_eq_true, across_contains_side, hb]
  rfl

def blockNumber : List Nat → Nat → Nat
  | [], _ => 0
  | d :: ds, i => if i < d then 0 else blockNumber ds (i - d) + 1

def runLengthsFrom (a len : Nat) : List Nat → List Nat
  | [] => [len]
  | b :: bs => if a == b then runLengthsFrom a (len + 1) bs
    else len :: runLengthsFrom b 1 bs

def runLengths : List Nat → List Nat
  | [] => []
  | a :: as => runLengthsFrom a 1 as

theorem runLengthsFrom_sum (bs : List Nat) (a len : Nat) :
    (runLengthsFrom a len bs).sum = len + bs.length := by
  induction bs generalizing a len with
  | nil => simp [runLengthsFrom]
  | cons b bs ih =>
    rw [runLengthsFrom]
    split
    · rw [ih]
      simp only [List.length_cons]
      omega
    · simp [ih, Nat.add_comm]

theorem runLengths_sum (bs : List Nat) : (runLengths bs).sum = bs.length := by
  cases bs with
  | nil => rfl
  | cons a as => simp [runLengths, runLengthsFrom_sum, Nat.add_comm]

def shapeRowBlocks (ds : List Nat) (aw : List (AcrossWord (gridOfPerm (layered ds)))) : List Nat :=
  runLengths (aw.map fun a => blockNumber ds a.row.val)

theorem shapeRowBlocks_sum (ds : List Nat) (aw : List (AcrossWord (gridOfPerm (layered ds)))) :
    (shapeRowBlocks ds aw).sum = aw.length := by
  simp [shapeRowBlocks, runLengths_sum]

theorem layered_word_lengths (ds : List Nat) :
    (finListAcrossWords (gridOfPerm (layered ds))).elems.length =
      (finListDownWords (gridOfPerm (layered ds))).elems.length := by
  unfold finListDownWords
  rw [List.length_map, layered_grid_symmetric]

/-- Block recurrence on the staircase/rectangle matrix of a layered permutation. -/
def layeredBlockData (ds : List Nat) : List Nat × List Nat :=
  let G := gridOfPerm (layered ds)
  let rows := (finListAcrossWords G).elems
  let cols := (finListDownWords G).elems
  let masks := cols.map fun b => columnBits rows.length fun i =>
    let a := listGetFin rows i
    blockEdge ds a.row.val b.col.val (a.lo.val != 0) (b.lo.val != 0)
  (shapeRowBlocks ds rows, masks)

/-- Exact recurrence applied to the diagonal row blocks and their column signatures. -/
def layeredBlockCount (ds : List Nat) : Nat :=
  let (blocks, masks) := layeredBlockData ds
  sweepCount blocks masks

theorem map_listGetFin {α : Type} (xs : List α) :
    (finRangeList xs.length).map (listGetFin xs) = xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    simp only [List.length_cons, finRangeList, List.map_cons, List.map_map]
    exact congrArg (x :: ·) ih

theorem rpCount_layered (ds : List Nat) :
    rpCount (gridOfPerm (layered ds)) = layeredBlockCount ds := by
  let G := gridOfPerm (layered ds)
  let rows := (finListAcrossWords G).elems
  let cols := (finListDownWords G).elems
  have h : rows.length = cols.length := layered_word_lengths ds
  have hlen := shapeRowBlocks_sum ds rows
  let adj (i : Fin rows.length) (j : Fin cols.length) :=
    wordsIntersect (listGetFin rows i) (listGetFin cols j)
  let mask (b : DownWord G) := columnBits rows.length fun i =>
    let a := listGetFin rows i
    blockEdge ds a.row.val b.col.val (a.lo.val != 0) (b.lo.val != 0)
  change (if rows.length = cols.length then countMatchingsAux rows.length cols.length adj
    (finRangeList cols.length) else 0) = sweepCount (shapeRowBlocks ds rows) (cols.map mask)
  have hmask : (cols.map mask).length = (shapeRowBlocks ds rows).sum :=
    (List.length_map mask).trans (h.symm.trans hlen.symm)
  rw [ite_pos h, sweepCount_eq_signatureCount _ _ hmask, hlen]
  have he := signatureCount_eq_countMatchingsAux rows.length cols.length adj
    (finRangeList cols.length) (finRangeList_nodup _)
  rw [← he]
  change signatureCount rows.length ((finRangeList cols.length).map (fun j =>
    columnBits rows.length (fun i => wordsIntersect (listGetFin rows i) (listGetFin cols j)))) = _
  congr 1
  rw [show ((finRangeList cols.length).map (fun j =>
      columnBits rows.length (fun i => wordsIntersect (listGetFin rows i) (listGetFin cols j)))) =
      (((finRangeList cols.length).map (listGetFin cols)).map (fun b =>
        columnBits rows.length (fun i => wordsIntersect (listGetFin rows i) b))) by
      rw [List.map_map]; rfl, map_listGetFin]
  apply List.map_congr_left
  intro b _
  congr 1
  funext i
  exact layered_words_blockEdge ds _ _


/-! ## Kernel checking of shared arithmetic subproblems

The tactic only proposes intermediate equations. Each equation is a theorem
whose value is checked from one recurrence step and previously proved equations.
-/

private theorem signatureCount_zero (cs : List Nat) : signatureCount 0 cs = 1 := rfl

private theorem stateTotal_nil (k : Nat) : stateTotal k [] = 0 := rfl

private theorem stateTotal_certificate (k : Nat) (cs : List Nat) (w a b : Nat)
    (states : List State) (ha : signatureCount k cs = a) (hb : stateTotal k states = b) :
    stateTotal k ((cs, w) :: states) = w * a + b := by
  rw [stateTotal_cons, ha, hb]

/-- Within one ordered residual list, equal deletions already occur in runs. -/
private def certificateStep (cs : List Nat) : List State :=
  match expandState (cs, 1) with
  | [] => []
  | (ds, w) :: ss => gather ds w ss

private theorem certificateStep_total (k : Nat) (cs : List Nat) :
    stateTotal k (certificateStep cs) = stateTotal k (expandState (cs, 1)) := by
  unfold certificateStep
  generalize expandState (cs, 1) = states
  cases states with
  | nil => rfl
  | cons head tail =>
    rcases head with ⟨ds, w⟩
    exact gather_total k tail ds w

private theorem signatureCount_certificate (k : Nat) (cs : List Nat) (states : List State)
    (result : Nat) (hlen : cs.length = k + 1) (hstep : certificateStep cs = states)
    (hc : stateTotal k states = result) : signatureCount (k + 1) cs = result := by
  have ht := (certificateStep_total k cs).trans (expand_total k (cs, 1) hlen)
  rw [hstep, Nat.one_mul] at ht
  exact ht.symm.trans hc

private theorem layeredBlockCount_certificate (ds blocks masks : List Nat) (result : Nat)
    (hdata : layeredBlockData ds = (blocks, masks)) (hlen : masks.length = blocks.sum)
    (hc : signatureCount blocks.sum (sortRuns masks (· ≤ ·)) = result) :
    layeredBlockCount ds = result := by
  unfold layeredBlockCount
  rw [hdata]
  change sweepCount blocks masks = result
  rw [sweepCount_eq_signatureCount _ _ hlen]
  exact (signatureCount_perm _ (sortRuns_perm _ _)).symm.trans hc

open Lean in
private structure CertificateCache where
  proofs : Std.HashMap (List Nat) (Nat × Expr) := {}
  lists : Std.HashMap (List Nat) Expr := {}

open Lean Elab Tactic in
private def columnsExpr : (cs : List Nat) → StateT CertificateCache TacticM Expr
  | [] => pure (toExpr ([] : List Nat))
  | c :: cs => do
    if let some term := (← get).lists.get? (c :: cs) then
      return term
    let tail ← columnsExpr cs
    let term := mkApp3 (mkConst ``List.cons [0]) (mkConst ``Nat) (mkRawNatLit c) tail
    modify fun cache => { cache with lists := cache.lists.insert (c :: cs) term }
    return term

open Lean in
private def signatureDeclName (k : Nat) (cs : List Nat) : Name :=
  .num (.num `RookConj314.signatureCertificates k)
    (cs.foldl (fun v c => (v <<< k) + c) 0)

open Lean Elab Tactic Meta in
/-- Propose one recurrence equation per residual column multiset. The kernel
checks each equation before any parent equation can use it. -/
private def certifySignatureCount :
    Nat → (cs : List Nat) → StateT CertificateCache TacticM (Nat × Expr)
  | 0, cs => do
    let cols ← columnsExpr cs
    pure (1, mkApp (mkConst ``signatureCount_zero) cols)
  | k + 1, cs => do
    if let some known := (← get).proofs.get? cs then
      return known
    let name := signatureDeclName (k + 1) cs
    if let some existing := (← getEnv).find? name then
      if let some value ← getNatValue? existing.type.appArg! then
        return (value, mkConst name)
      throwError "invalid cached recurrence equation"
    let states := certificateStep cs
    let kExpr := mkRawNatLit k
    let natType := mkConst ``Nat
    let natRefl := mkApp (mkConst ``Eq.refl [1]) natType
    let mut total := 0
    let mut totalProof := mkApp (mkConst ``stateTotal_nil) kExpr
    let mut tailExpr := toExpr ([] : List State)
    for (remaining, w) in states.reverse do
      let (value, childProof) ← certifySignatureCount k remaining
      let cols ← columnsExpr remaining
      let wExpr := mkRawNatLit w
      let newTotal := w * value + total
      totalProof := mkAppN (mkConst ``stateTotal_certificate)
        #[kExpr, cols, wExpr, mkRawNatLit value, mkRawNatLit total, tailExpr,
          childProof, totalProof]
      let pair := mkAppN (mkConst ``Prod.mk [0, 0])
        #[mkApp (mkConst ``List [0]) natType, natType, cols, wExpr]
      tailExpr := mkApp3 (mkConst ``List.cons [0]) (mkConst ``State) pair tailExpr
      total := newTotal
    let cols ← columnsExpr cs
    let sizeExpr := mkRawNatLit (k + 1)
    let hstep ← mkEqRefl tailExpr
    let ty ← mkEq (mkApp2 (mkConst ``signatureCount) sizeExpr cols) (mkRawNatLit total)
    let proof := mkAppN (mkConst ``signatureCount_certificate)
      #[kExpr, cols, tailExpr, mkRawNatLit total, mkApp natRefl sizeExpr, hstep, totalProof]
    let decl : Declaration := .thmDecl { name, type := ty, value := proof, levelParams := [] }
    let checked ← ofExceptKernelException
      ((← getEnv).addDeclCore 0 10000 decl none (doCheck := true))
    setEnv checked
    let result := (total, mkConst name)
    modify fun cache => { cache with proofs := cache.proofs.insert cs result }
    return result

open Lean Elab Tactic Meta in
elab "certify_layered_count " "[" ds:num,* "]" : tactic => withMainContext do
  let ds := ds.getElems.toList.map (·.getNat)
  let (blocks, masks) := layeredBlockData ds
  let k := blocks.sum
  let ((result, proof), _) ← (certifySignatureCount k (sortRuns masks (· ≤ ·))).run {}
  let hlen := mkApp2 (mkConst ``Eq.refl [1]) (mkConst ``Nat) (toExpr k)
  let hdata ← mkEqRefl (toExpr (blocks, masks))
  closeMainGoal `certify_layered_count (mkAppN (mkConst ``layeredBlockCount_certificate)
    #[toExpr ds, toExpr blocks, toExpr masks, toExpr result, hdata, hlen, proof])


/-! ## Counterexamples to Conjecture 3.14 -/

def w17 : Perm 17 := layered [5, 3, 1, 3, 5]

def w18 : Perm 18 := layered [5, 3, 1, 1, 3, 5]

def oneLine {n : Nat} (p : Perm n) : List Nat :=
  (finRangeList n).map fun i => (p.toFun i).val + 1

theorem w17_oneLine :
    oneLine w17 = [5, 4, 3, 2, 1, 8, 7, 6, 9, 12, 11, 10, 17, 16, 15, 14, 13] := rfl

theorem w18_oneLine :
    oneLine w18 = [5, 4, 3, 2, 1, 8, 7, 6, 9, 10, 13, 12, 11, 18, 17, 16, 15, 14] := rfl

/-- Zero-length end blocks leave the identity when m = 0. -/
def singleShellShape (n m : Nat) : List Nat :=
  m :: List.replicate (n - 2 * m) 1 ++ [m]

theorem singleShellShape_sum (n m : Nat) (hm : 2 * m ≤ n) :
    (singleShellShape n m).sum = n := by
  simp [singleShellShape, List.sum_replicate_nat]
  omega

def singleShell (n m : Nat) (hm : 2 * m ≤ n) : Perm n :=
  (layered (singleShellShape n m)).cast (singleShellShape_sum n m hm)

theorem rpCount_cast {m n : Nat} (h : m = n) (p : Perm m) :
    rpCount (gridOfPerm (p.cast h)) = rpCount (gridOfPerm p) := by
  cases h
  rfl

theorem singleShell_rpCount (n m : Nat) (hm : 2 * m ≤ n) :
    rpCount (gridOfPerm (singleShell n m hm)) = layeredBlockCount (singleShellShape n m) := by
  rw [singleShell, rpCount_cast, rpCount_layered]

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
private theorem shape17_count : layeredBlockCount [5, 3, 1, 3, 5] = 104476798194769 := by
  certify_layered_count [5, 3, 1, 3, 5]

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
private theorem shape18_count : layeredBlockCount [5, 3, 1, 1, 3, 5] = 2949333362474113 := by
  certify_layered_count [5, 3, 1, 1, 3, 5]

theorem w17_rpCount : rpCount (gridOfPerm w17) = 104476798194769 :=
  (rpCount_layered [5, 3, 1, 3, 5]).trans shape17_count

theorem w18_rpCount : rpCount (gridOfPerm w18) = 2949333362474113 :=
  (rpCount_layered [5, 3, 1, 1, 3, 5]).trans shape18_count

section

set_option maxRecDepth 10000
set_option maxHeartbeats 0

private theorem shell17_0 : layeredBlockCount (singleShellShape 17 0) = 1 := by
  certify_layered_count [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

private theorem shell17_1 : layeredBlockCount (singleShellShape 17 1) = 1 := by
  certify_layered_count [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

private theorem shell17_2 : layeredBlockCount (singleShellShape 17 2) = 268435457 := by
  certify_layered_count [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]

private theorem shell17_3 : layeredBlockCount (singleShellShape 17 3) = 1129869140869 := by
  certify_layered_count [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]

private theorem shell17_4 : layeredBlockCount (singleShellShape 17 4) = 40084566933905 := by
  certify_layered_count [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4]

private theorem shell17_5 : layeredBlockCount (singleShellShape 17 5) = 103460138813701 := by
  certify_layered_count [5, 1, 1, 1, 1, 1, 1, 1, 5]

private theorem shell17_6 : layeredBlockCount (singleShellShape 17 6) = 65555327816657 := by
  certify_layered_count [6, 1, 1, 1, 1, 1, 6]

private theorem shell17_7 : layeredBlockCount (singleShellShape 17 7) = 18356098793509 := by
  certify_layered_count [7, 1, 1, 1, 7]

private theorem shell17_8 : layeredBlockCount (singleShellShape 17 8) = 2824217777825 := by
  certify_layered_count [8, 1, 8]

end

theorem singleShell_bound_n17 (m : Nat) (hm : 2 * m ≤ 17) :
    rpCount (gridOfPerm (singleShell 17 m hm)) ≤ 103460138813701 := by
  rw [singleShell_rpCount]
  have cases_m : m = 0 ∨ m = 1 ∨ m = 2 ∨ m = 3 ∨ m = 4 ∨ m = 5 ∨ m = 6 ∨ m = 7 ∨ m = 8 := by omega
  rcases cases_m with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    first
    | rw [shell17_0]; decide
    | rw [shell17_1]; decide
    | rw [shell17_2]; decide
    | rw [shell17_3]; decide
    | rw [shell17_4]; decide
    | rw [shell17_5]; decide
    | rw [shell17_6]; decide
    | rw [shell17_7]; decide
    | rw [shell17_8]; decide

theorem singleShell_max_n17 : rpCount (gridOfPerm (singleShell 17 5 (by decide))) = 103460138813701 :=
  (singleShell_rpCount 17 5 _).trans shell17_5

/-- The witness exceeds the attained maximum over every allowed endpoint size. -/
theorem conj314_disproof_n17 :
    rpCount (gridOfPerm w17) = 104476798194769 ∧
    (∀ (m : Nat) (hm : 2 * m ≤ 17),
      rpCount (gridOfPerm (singleShell 17 m hm)) ≤ 103460138813701) ∧
    rpCount (gridOfPerm (singleShell 17 5 (by decide))) = 103460138813701 ∧
    103460138813701 < rpCount (gridOfPerm w17) ∧
    rpCount (gridOfPerm w17) - 103460138813701 = 1016659381068 := by
  refine ⟨w17_rpCount, singleShell_bound_n17, singleShell_max_n17, ?_, ?_⟩ <;>
    rw [w17_rpCount] <;> decide

section

set_option maxRecDepth 10000
set_option maxHeartbeats 0

private theorem shell18_0 : layeredBlockCount (singleShellShape 18 0) = 1 := by
  certify_layered_count [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

private theorem shell18_1 : layeredBlockCount (singleShellShape 18 1) = 1 := by
  certify_layered_count [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

private theorem shell18_2 : layeredBlockCount (singleShellShape 18 2) = 1073741825 := by
  certify_layered_count [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]

private theorem shell18_3 : layeredBlockCount (singleShellShape 18 3) = 10168067293093 := by
  certify_layered_count [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]

private theorem shell18_4 : layeredBlockCount (singleShellShape 18 4) = 637837775703569 := by
  certify_layered_count [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4]

private theorem shell18_5 : layeredBlockCount (singleShellShape 18 5) = 2445624351454501 := by
  certify_layered_count [5, 1, 1, 1, 1, 1, 1, 1, 1, 5]

private theorem shell18_6 : layeredBlockCount (singleShellShape 18 6) = 1960443604780625 := by
  certify_layered_count [6, 1, 1, 1, 1, 1, 1, 6]

private theorem shell18_7 : layeredBlockCount (singleShellShape 18 7) = 645315196970053 := by
  certify_layered_count [7, 1, 1, 1, 1, 7]

private theorem shell18_8 : layeredBlockCount (singleShellShape 18 8) = 112363477776209 := by
  certify_layered_count [8, 1, 1, 8]

private theorem shell18_9 : layeredBlockCount (singleShellShape 18 9) = 12020754177001 := by
  certify_layered_count [9, 9]

end

theorem singleShell_bound_n18 (m : Nat) (hm : 2 * m ≤ 18) :
    rpCount (gridOfPerm (singleShell 18 m hm)) ≤ 2445624351454501 := by
  rw [singleShell_rpCount]
  have cases_m : m = 0 ∨ m = 1 ∨ m = 2 ∨ m = 3 ∨ m = 4 ∨ m = 5 ∨ m = 6 ∨ m = 7 ∨ m = 8 ∨ m = 9 := by omega
  rcases cases_m with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    first
    | rw [shell18_0]; decide
    | rw [shell18_1]; decide
    | rw [shell18_2]; decide
    | rw [shell18_3]; decide
    | rw [shell18_4]; decide
    | rw [shell18_5]; decide
    | rw [shell18_6]; decide
    | rw [shell18_7]; decide
    | rw [shell18_8]; decide
    | rw [shell18_9]; decide

theorem singleShell_max_n18 : rpCount (gridOfPerm (singleShell 18 5 (by decide))) = 2445624351454501 :=
  (singleShell_rpCount 18 5 _).trans shell18_5

/-- The witness exceeds the attained maximum over every allowed endpoint size. -/
theorem conj314_disproof_n18 :
    rpCount (gridOfPerm w18) = 2949333362474113 ∧
    (∀ (m : Nat) (hm : 2 * m ≤ 18),
      rpCount (gridOfPerm (singleShell 18 m hm)) ≤ 2445624351454501) ∧
    rpCount (gridOfPerm (singleShell 18 5 (by decide))) = 2445624351454501 ∧
    2445624351454501 < rpCount (gridOfPerm w18) ∧
    rpCount (gridOfPerm w18) - 2445624351454501 = 503709011019612 := by
  refine ⟨w18_rpCount, singleShell_bound_n18, singleShell_max_n18, ?_, ?_⟩ <;>
    rw [w18_rpCount] <;> decide

/-- The conjecture as a universal claim that a symmetric single shell attains a maximum. -/
def Conjecture314 : Prop :=
  ∀ n : Nat, ∃ (m : Nat) (hm : 2 * m ≤ n), ∀ u : Perm n,
    rpCount (gridOfPerm u) ≤ rpCount (gridOfPerm (singleShell n m hm))

theorem not_conjecture314 : ¬ Conjecture314 := by
  intro claim
  obtain ⟨m, hm, maximal⟩ := claim 17
  exact (Nat.not_le_of_lt conj314_disproof_n17.2.2.2.1)
    (Nat.le_trans (maximal w17) (singleShell_bound_n17 m hm))

/-! ## Arithmetic replay of the referee's seven-square certificate -/

def stirlingNumber : Nat → Nat → Nat
  | 0, k => if k = 0 then 1 else 0
  | _ + 1, 0 => 0
  | n + 1, k + 1 => (k + 1) * stirlingNumber n (k + 1) + stirlingNumber n k

def fallingFactorial (n : Nat) : Nat → Nat
  | 0 => 1
  | k + 1 => (n - k) * fallingFactorial n k

def witnessCutCoefficient (h : Nat) : Nat :=
  ((List.range' 1 5).map fun p =>
    ((List.range' 1 3).map fun a =>
      ((List.range' 1 3).map fun b =>
        if a ≤ p ∧ p - a + b = h then
          stirlingNumber 5 p * stirlingNumber 3 a * stirlingNumber 3 b *
            fallingFactorial p a ^ 2
        else 0).sum).sum).sum

def witnessSevenSquares (t : Nat) : Nat :=
  ((List.range' 1 7).map fun h =>
    (witnessCutCoefficient h * h ^ t * fallingFactorial h h) ^ 2).sum

theorem witnessCoefficients :
    (List.range' 1 7).map witnessCutCoefficient = [1081, 11763, 34786, 34315, 12250, 1435, 25] := by
  decide

theorem witnessSevenSquares_n17 : rpCount (gridOfPerm w17) = witnessSevenSquares 1 := by
  rw [w17_rpCount]
  decide

theorem witnessSevenSquares_n18 : rpCount (gridOfPerm w18) = witnessSevenSquares 2 := by
  rw [w18_rpCount]
  decide

/-! ## Direct small-grid controls -/

private theorem rawControl1 : rpCount (gridOfPerm (layered [1])) = 1 := by cbv

private theorem rawControl2 : rpCount (gridOfPerm (layered [2])) = 1 := by cbv

private theorem rawControl3 : rpCount (gridOfPerm (layered [1, 1, 1])) = 1 := by cbv

private theorem rawControl4Identity : rpCount (gridOfPerm (layered [1, 1, 1, 1])) = 1 := by cbv

private theorem rawControl4Layered : rpCount (gridOfPerm (layered [2, 2])) = 5 := by cbv

set_option maxHeartbeats 0 in
private theorem rawControl5 : rpCount (gridOfPerm (layered [2, 1, 2])) = 17 := by cbv

def smallLayeredShapes : List (List Nat) :=
  [[1], [2], [1, 1, 1], [1, 1, 1, 1], [2, 2], [2, 1, 2]]

def smallLayeredCounts : List Nat := [1, 1, 1, 1, 5, 17]

theorem controls_layered_direct :
    (smallLayeredShapes.map fun ds => rpCount (gridOfPerm (layered ds))) = smallLayeredCounts := by
  simp only [smallLayeredShapes, smallLayeredCounts, List.map_cons, List.map_nil,
    rawControl1, rawControl2, rawControl3, rawControl4Identity, rawControl4Layered, rawControl5]

theorem controls_layered_block :
    smallLayeredShapes.map layeredBlockCount = smallLayeredCounts := by
  have h : (fun ds => rpCount (gridOfPerm (layered ds))) = layeredBlockCount :=
    funext rpCount_layered
  rw [← h]
  exact controls_layered_direct

theorem control_2143 : rpCount (gridOfPerm (permOfList1Based 4 [2, 1, 4, 3] (by decide))) = 5 := by
  cbv

theorem control_2413 : rpCount (gridOfPerm (permOfList1Based 4 [2, 4, 1, 3] (by decide))) = 2 := by
  cbv

theorem control_1234 : rpCount (gridOfPerm (permOfList1Based 4 [1, 2, 3, 4] (by decide))) = 1 := by
  cbv

end RookConj314

open RookConj314

#print axioms rookPlacementEquivWordMatching
#print axioms rookPlacement_hasExactCard
#print axioms signatureCount_eq_countMatchingsAux
#print axioms blockEdge_eq_sides
#print axioms sweepCount_eq_signatureCount
#print axioms rpCount_layered
#print axioms w17_oneLine
#print axioms w18_oneLine
#print axioms w17_rpCount
#print axioms w18_rpCount
#print axioms singleShell_bound_n17
#print axioms singleShell_bound_n18
#print axioms singleShell_max_n17
#print axioms singleShell_max_n18
#print axioms conj314_disproof_n17
#print axioms conj314_disproof_n18
#print axioms not_conjecture314
#print axioms witnessCoefficients
#print axioms witnessSevenSquares_n17
#print axioms witnessSevenSquares_n18
#print axioms controls_layered_direct
#print axioms controls_layered_block
#print axioms control_2143
#print axioms control_2413
#print axioms control_1234

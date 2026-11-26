/-
Standalone Lean 4 (v4.36.0, zero Mathlib) formalization of the disproof and
complete d >= 3 resolution of van Berkel & Bosma (arXiv:2609.16843v2) Conjecture 4.
-/

/-- `IsStrict3Sum S x` holds iff `x` is the sum of three strictly increasing members of `S`. -/
def IsStrict3Sum (S : Nat → Prop) (x : Nat) : Prop :=
  ∃ a b c, S a ∧ S b ∧ S c ∧ a < b ∧ b < c ∧ a + b + c = x

/-- Characteristic predicate `InSeq d x` of the greedy strict 3-sumfree sequence `S_{1, d-1, 2d-1}`.
    For `d >= 3`, the seed on `[1, 2d - 1]` is `{1, d - 1, 2d - 1}`, `0` is excluded, and every
    `x > 2d - 1` belongs to the sequence iff it is not a strict 3-sum of smaller members. -/
def InSeq (d : Nat) : Nat → Prop
  | 0 => False
  | x + 1 =>
    if x + 1 ≤ 2 * d - 1 then
      x + 1 = 1 ∨ x + 1 = d - 1 ∨ x + 1 = 2 * d - 1
    else
      ¬ ∃ (a b c : Nat) (_ha : a < x + 1) (_hb : b < x + 1) (_hc : c < x + 1),
          InSeq d a ∧ InSeq d b ∧ InSeq d c ∧ a < b ∧ b < c ∧ a + b + c = x + 1
termination_by x => x

theorem inSeq_zero (d : Nat) : ¬ InSeq d 0 := by
  simp [InSeq]

theorem inSeq_pos {d x : Nat} (h : InSeq d x) : 0 < x := by
  cases x with
  | zero => exact False.elim (inSeq_zero d h)
  | succ _ => omega

theorem inSeq_seed (d x : Nat) (hd : d ≥ 3) (hx : x ≤ 2 * d - 1) :
    InSeq d x ↔ (x = 1 ∨ x = d - 1 ∨ x = 2 * d - 1) := by
  cases x with
  | zero =>
    simp [InSeq]
    omega
  | succ _ =>
    simp [InSeq, hx]

theorem inSeq_gt (d x : Nat) (hx : x > 2 * d - 1) :
    InSeq d x ↔ ¬ IsStrict3Sum (fun y => y < x ∧ InSeq d y) x := by
  cases x with
  | zero => omega
  | succ n =>
    have hnotle : ¬ (n + 1 ≤ 2 * d - 1) := by omega
    simp only [InSeq, hnotle, ↓reduceIte, IsStrict3Sum]
    constructor
    · intro h ⟨a, b, c, ⟨ha, hIa⟩, ⟨hb, hIb⟩, ⟨hc, hIc⟩, hab, hbc, hsum⟩
      exact h ⟨a, b, c, ha, hb, hc, hIa, hIb, hIc, hab, hbc, hsum⟩
    · intro h ⟨a, b, c, ha, hb, hc, hIa, hIb, hIc, hab, hbc, hsum⟩
      exact h ⟨a, b, c, ⟨ha, hIa⟩, ⟨hb, hIb⟩, ⟨hc, hIc⟩, hab, hbc, hsum⟩

namespace Internal

def decExistsLt : (n : Nat) → (P : (y : Nat) → y < n → Prop) →
    ((y : Nat) → (hy : y < n) → Decidable (P y hy)) → Decidable (∃ y, ∃ hy : y < n, P y hy)
  | 0, _, _ => isFalse (by rintro ⟨y, hy, _⟩; omega)
  | n + 1, P, hP =>
    match hP n (Nat.lt_succ_self n) with
    | isTrue hn => isTrue ⟨n, Nat.lt_succ_self n, hn⟩
    | isFalse hn =>
      match decExistsLt n (fun y hy => P y (Nat.lt_succ_of_lt hy))
          (fun y hy => hP y (Nat.lt_succ_of_lt hy)) with
      | isTrue hlt =>
        isTrue (by
          obtain ⟨y, hy, py⟩ := hlt
          exact ⟨y, Nat.lt_succ_of_lt hy, py⟩)
      | isFalse hlt =>
        isFalse (by
          rintro ⟨y, hy, py⟩
          by_cases hyn : y = n
          · subst hyn; exact hn py
          · have hylt : y < n := by omega
            exact hlt ⟨y, hylt, py⟩)

def decInSeq (d : Nat) : (x : Nat) → Decidable (InSeq d x)
  | 0 => isFalse (inSeq_zero d)
  | x + 1 =>
    if hle : x + 1 ≤ 2 * d - 1 then
      have hiff : InSeq d (x + 1) ↔ (x + 1 = 1 ∨ x + 1 = d - 1 ∨ x + 1 = 2 * d - 1) := by
        simp [InSeq, hle]
      decidable_of_iff (x + 1 = 1 ∨ x + 1 = d - 1 ∨ x + 1 = 2 * d - 1) hiff.symm
    else
      let P3 (a b c : Nat) (_ha : a < x + 1) (_hb : b < x + 1) (_hc : c < x + 1) : Prop :=
        InSeq d a ∧ InSeq d b ∧ InSeq d c ∧ a < b ∧ b < c ∧ a + b + c = x + 1
      have dec3 : Decidable (∃ a, ∃ ha : a < x + 1, ∃ b, ∃ hb : b < x + 1,
          ∃ c, ∃ hc : c < x + 1, P3 a b c ha hb hc) :=
        decExistsLt (x + 1) _ fun a _ =>
          decExistsLt (x + 1) _ fun b _ =>
            decExistsLt (x + 1) _ fun c _ =>
              haveI := decInSeq d a
              haveI := decInSeq d b
              haveI := decInSeq d c
              inferInstance
      have hiff : InSeq d (x + 1) ↔ ¬ (∃ a, ∃ ha : a < x + 1, ∃ b, ∃ hb : b < x + 1,
          ∃ c, ∃ hc : c < x + 1, P3 a b c ha hb hc) := by
        simp only [InSeq, hle, ↓reduceIte, P3]
        constructor
        · intro h ⟨a, ha, b, hb, c, hc, hrest⟩
          exact h ⟨a, b, c, ha, hb, hc, hrest⟩
        · intro h ⟨a, b, c, ha, hb, hc, hrest⟩
          exact h ⟨a, ha, b, hb, c, hc, hrest⟩
      @decidable_of_iff _ _ hiff.symm (@instDecidableNot _ dec3)
termination_by x => x

attribute [local instance] decInSeq

/-- Every interval `(m, max (2*d) (3*m + 1)]` contains a member of `InSeq d`. -/
theorem exists_inSeq_above (d m : Nat) :
    ∃ x, m < x ∧ x ≤ max (2 * d) (3 * m + 1) ∧ InSeq d x := by
  let B := max (2 * d) (3 * m + 1)
  have hdec : Decidable (∃ y, ∃ _ : y < B, m < y ∧ InSeq d y) :=
    decExistsLt B _ fun _ _ => inferInstance
  cases hdec with
  | isTrue hex =>
    obtain ⟨y, _, hmy, hIy⟩ := hex
    exact ⟨y, hmy, by omega, hIy⟩
  | isFalse hno =>
    refine ⟨B, by omega, Nat.le_refl B, ?_⟩
    rw [inSeq_gt d B (by omega)]
    rintro ⟨a, b, c, ⟨_, _⟩, ⟨_, _⟩, ⟨hcB, hIc⟩, _, _, _⟩
    by_cases hmc : m < c
    · exact hno ⟨c, hcB, hmc, hIc⟩
    · omega

def scanLeast (d cur bound : Nat) : Nat :=
  if cur ≥ bound then
    bound
  else if InSeq d cur then
    cur
  else
    scanLeast d (cur + 1) bound
termination_by bound - cur

theorem scanLeast_spec (d cur bound : Nat)
    (hex : ∃ x, cur ≤ x ∧ x ≤ bound ∧ InSeq d x) :
    cur ≤ scanLeast d cur bound ∧
    scanLeast d cur bound ≤ bound ∧
    InSeq d (scanLeast d cur bound) ∧
    (∀ z, cur ≤ z → z < scanLeast d cur bound → ¬ InSeq d z) := by
  unfold scanLeast
  split
  · obtain ⟨x, _, _, hIx⟩ := hex
    have hxb' : x = bound := by omega
    subst hxb'
    refine ⟨by omega, Nat.le_refl _, hIx, ?_⟩
    intro z _ _; omega
  · split
    · next hcur =>
      refine ⟨Nat.le_refl _, by omega, hcur, ?_⟩
      intro z _ _; omega
    · next hncur =>
      have hex' : ∃ x, cur + 1 ≤ x ∧ x ≤ bound ∧ InSeq d x := by
        obtain ⟨x, _, hxb, hIx⟩ := hex
        have hne : x ≠ cur := by intro heq; subst heq; exact hncur hIx
        exact ⟨x, by omega, hxb, hIx⟩
      obtain ⟨_, h2, h3, h4⟩ := scanLeast_spec d (cur + 1) bound hex'
      refine ⟨by omega, h2, h3, ?_⟩
      intro z _ hzs
      by_cases hzc : z = cur
      · subst hzc; exact hncur
      · exact h4 z (by omega) hzs
termination_by bound - cur

def nextInSeq (d m : Nat) : Nat :=
  scanLeast d (m + 1) (max (2 * d) (3 * m + 1))

theorem nextInSeq_spec (d m : Nat) :
    m < nextInSeq d m ∧
    InSeq d (nextInSeq d m) ∧
    (∀ z, m < z → z < nextInSeq d m → ¬ InSeq d z) := by
  unfold nextInSeq
  obtain ⟨x, hmx, hxb, hIx⟩ := exists_inSeq_above d m
  obtain ⟨h1, _, h3, h4⟩ := scanLeast_spec d (m + 1) (max (2 * d) (3 * m + 1))
    ⟨x, by omega, hxb, hIx⟩
  exact ⟨by omega, h3, fun z hmz hzn => h4 z (by omega) hzn⟩

end Internal

/-- Exact 0-indexed strictly increasing enumeration of `S_{1, d-1, 2d-1}`. -/
def seq (d : Nat) : Nat → Nat
  | 0 => Internal.nextInSeq d 0
  | i + 1 => Internal.nextInSeq d (seq d i)

/-- Alias matching the specification's `Greedy3Sumfree` identifier. -/
abbrev Greedy3Sumfree (d : Nat) (i : Nat) : Nat := seq d i

theorem seq_step_lt (d i : Nat) : seq d i < seq d (i + 1) :=
  (Internal.nextInSeq_spec d (seq d i)).1

theorem seq_strictMono (d : Nat) {i j : Nat} (hij : i < j) : seq d i < seq d j := by
  induction j with
  | zero => omega
  | succ n ih =>
    by_cases hin : i = n
    · subst hin; exact seq_step_lt d i
    · exact Nat.lt_trans (ih (by omega)) (seq_step_lt d n)

theorem seq_injective (d : Nat) {i j : Nat} (h : seq d i = seq d j) : i = j := by
  by_cases hlt : i < j
  · have := seq_strictMono d hlt; omega
  · by_cases hgt : j < i
    · have := seq_strictMono d hgt; omega
    · omega

theorem seq_inSeq (d i : Nat) : InSeq d (seq d i) := by
  cases i with
  | zero => exact (Internal.nextInSeq_spec d 0).2.1
  | succ n => exact (Internal.nextInSeq_spec d (seq d n)).2.1

theorem seq_below_zero (d z : Nat) (hz : z < seq d 0) : ¬ InSeq d z := by
  cases z with
  | zero => exact inSeq_zero d
  | succ n => exact (Internal.nextInSeq_spec d 0).2.2 (n + 1) (by omega) hz

theorem seq_gap (d i z : Nat) (h1 : seq d i < z) (h2 : z < seq d (i + 1)) : ¬ InSeq d z :=
  (Internal.nextInSeq_spec d (seq d i)).2.2 z h1 h2

theorem seq_ge_succ (d i : Nat) : i + 1 ≤ seq d i := by
  induction i with
  | zero =>
    have h0 := (Internal.nextInSeq_spec d 0).1
    dsimp only [seq]
    omega
  | succ n ih =>
    have := seq_step_lt d n
    omega

namespace Internal

theorem exists_index_of_lt_step {f : Nat → Nat} {A : Nat → Prop}
    (hbelow0 : ∀ x, x < f 0 → ¬ A x)
    (hgap : ∀ i x, f i < x → x < f (i + 1) → ¬ A x) :
    ∀ n x, x < f n → A x → ∃ i, i < n ∧ f i = x
  | 0, x, hx, hAx => False.elim (hbelow0 x hx hAx)
  | n + 1, x, hx, hAx => by
    by_cases hlt : x < f n
    · obtain ⟨i, hin, hfi⟩ := exists_index_of_lt_step hbelow0 hgap n x hlt hAx
      exact ⟨i, by omega, hfi⟩
    · by_cases heq : x = f n
      · exact ⟨n, by omega, heq.symm⟩
      · exact False.elim (hgap n x (by omega) hx hAx)

theorem strictMono_ge_id {f : Nat → Nat} (hf : ∀ i, f i < f (i + 1)) : ∀ n, n ≤ f n
  | 0 => Nat.zero_le _
  | n + 1 => by
    have := strictMono_ge_id hf n
    have := hf n
    omega

theorem range_iff_of_step_gaps {f : Nat → Nat} {A : Nat → Prop}
    (hf : ∀ i, f i < f (i + 1))
    (hmem : ∀ i, A (f i))
    (hbelow0 : ∀ x, x < f 0 → ¬ A x)
    (hgap : ∀ i x, f i < x → x < f (i + 1) → ¬ A x) (x : Nat) :
    (∃ i, f i = x) ↔ A x := by
  constructor
  · rintro ⟨i, rfl⟩; exact hmem i
  · intro hAx
    have hlt : x < f (x + 1) := by
      have := strictMono_ge_id hf (x + 1)
      omega
    obtain ⟨i, _, hfi⟩ := exists_index_of_lt_step hbelow0 hgap (x + 1) x hlt hAx
    exact ⟨i, hfi⟩

theorem strictMono_of_step {f : Nat → Nat} (hf : ∀ i, f i < f (i + 1)) {i j : Nat} (hij : i < j) :
    f i < f j := by
  induction j with
  | zero => omega
  | succ n ih =>
    by_cases hin : i = n
    · subst hin; exact hf i
    · exact Nat.lt_trans (ih (by omega)) (hf n)

theorem eq_of_strictMono_same_range {f g : Nat → Nat}
    (hf : ∀ i, f i < f (i + 1))
    (hg : ∀ i, g i < g (i + 1))
    (hrange : ∀ x, (∃ i, f i = x) ↔ (∃ i, g i = x)) :
    ∀ i, f i = g i := by
  intro i
  induction i using Nat.strongRecOn with
  | ind i ih =>
    obtain ⟨r, hgr⟩ := (hrange (f i)).mp ⟨i, rfl⟩
    have hir : i ≤ r := by
      by_cases hri : r < i
      · have hfr : f r = g r := ih r hri
        have hflt : f r < f i := strictMono_of_step hf hri
        omega
      · omega
    have hgle : g i ≤ f i := by
      by_cases heq : i = r
      · subst heq; omega
      · have := strictMono_of_step hg (by omega : i < r); omega
    obtain ⟨s, hfs⟩ := (hrange (g i)).mpr ⟨i, rfl⟩
    have his : i ≤ s := by
      by_cases hsi : s < i
      · have hgs : f s = g s := ih s hsi
        have hglt : g s < g i := strictMono_of_step hg hsi
        omega
      · omega
    have hfle : f i ≤ g i := by
      by_cases heq : i = s
      · subst heq; omega
      · have := strictMono_of_step hf (by omega : i < s); omega
    omega

end Internal

/-- The range of `seq d` equals `InSeq d`. -/
theorem seq_range_eq_inSeq (d x : Nat) : (∃ i, seq d i = x) ↔ InSeq d x :=
  Internal.range_iff_of_step_gaps (seq_step_lt d) (seq_inSeq d)
    (seq_below_zero d) (seq_gap d) x

/-- Initial seed terms of `seq d` for `d >= 3`: `(seq d 0, seq d 1, seq d 2) = (1, d - 1, 2*d - 1)`. -/
theorem seq_seed (d : Nat) (hd : d ≥ 3) :
    seq d 0 = 1 ∧ seq d 1 = d - 1 ∧ seq d 2 = 2 * d - 1 := by
  have h1 : InSeq d 1 := (inSeq_seed d 1 hd (by omega)).mpr (Or.inl rfl)
  have hd1 : InSeq d (d - 1) := (inSeq_seed d (d - 1) hd (by omega)).mpr (Or.inr (Or.inl rfl))
  have h2d1 : InSeq d (2 * d - 1) :=
    (inSeq_seed d (2 * d - 1) hd (by omega)).mpr (Or.inr (Or.inr rfl))
  have hs0 : seq d 0 = 1 := by
    have hge : 1 ≤ seq d 0 := seq_ge_succ d 0
    by_cases hgt : 1 < seq d 0
    · exact False.elim (seq_below_zero d 1 hgt h1)
    · omega
  have hs1 : seq d 1 = d - 1 := by
    have hstep0 : seq d 0 < seq d 1 := seq_step_lt d 0
    have hgt0 : 1 < seq d 1 := by omega
    by_cases hlt : seq d 1 < d - 1
    · have hI := (inSeq_seed d (seq d 1) hd (by omega)).mp (seq_inSeq d 1)
      omega
    · by_cases hgt : d - 1 < seq d 1
      · exact False.elim (seq_gap d 0 (d - 1) (by omega) hgt hd1)
      · omega
  have hs2 : seq d 2 = 2 * d - 1 := by
    have hstep1 : seq d 1 < seq d 2 := seq_step_lt d 1
    have hgt1 : d - 1 < seq d 2 := by omega
    by_cases hlt : seq d 2 < 2 * d - 1
    · have hI := (inSeq_seed d (seq d 2) hd (by omega)).mp (seq_inSeq d 2)
      omega
    · by_cases hgt : 2 * d - 1 < seq d 2
      · exact False.elim (seq_gap d 1 (2 * d - 1) (by omega) hgt h2d1)
      · omega
  exact ⟨hs0, hs1, hs2⟩

/-- Direct greedy recurrence characterization of `seq d`: for every `d >= 3` and `n >= 2`,
    `seq d (n + 1)` is the least integer strictly greater than `seq d n` that is not a
    3-sum `seq d i + seq d j + seq d l` with `i < j < l <= n`. -/
theorem seq_greedy_step (d : Nat) (hd : d ≥ 3) (n : Nat) (hn : n ≥ 2) :
    seq d n < seq d (n + 1) ∧
    (¬ ∃ i j l, i < j ∧ j < l ∧ l ≤ n ∧ seq d i + seq d j + seq d l = seq d (n + 1)) ∧
    (∀ z, seq d n < z → z < seq d (n + 1) →
      ∃ i j l, i < j ∧ j < l ∧ l ≤ n ∧ seq d i + seq d j + seq d l = z) := by
  have hseed := seq_seed d hd
  have hge2 : 2 * d - 1 ≤ seq d n := by
    by_cases h2 : n = 2
    · subst h2; omega
    · have := seq_strictMono d (by omega : 2 < n); omega
  refine ⟨seq_step_lt d n, ?_, ?_⟩
  · rintro ⟨i, j, l, hij, hjl, hln, hsum⟩
    have hIn : InSeq d (seq d (n + 1)) := seq_inSeq d (n + 1)
    have hgt : seq d (n + 1) > 2 * d - 1 := by have := seq_step_lt d n; omega
    have hnot := (inSeq_gt d (seq d (n + 1)) hgt).mp hIn
    have hll : seq d l < seq d (n + 1) := seq_strictMono d (by omega)
    have hjl' : seq d j < seq d l := seq_strictMono d hjl
    have hij' : seq d i < seq d j := seq_strictMono d hij
    exact hnot ⟨seq d i, seq d j, seq d l,
      ⟨by omega, seq_inSeq d i⟩, ⟨by omega, seq_inSeq d j⟩, ⟨hll, seq_inSeq d l⟩,
      hij', hjl', hsum⟩
  · intro z hzn hzs
    have hnotIn : ¬ InSeq d z := seq_gap d n z hzn hzs
    have hgt : z > 2 * d - 1 := by omega
    have h3 : IsStrict3Sum (fun y => y < z ∧ InSeq d y) z := by
      by_cases h : IsStrict3Sum (fun y => y < z ∧ InSeq d y) z
      · exact h
      · exact False.elim (hnotIn ((inSeq_gt d z hgt).mpr h))
    obtain ⟨a, b, c, ⟨_, hIa⟩, ⟨_, hIb⟩, ⟨hcz, hIc⟩, hab, hbc, hsum⟩ := h3
    obtain ⟨i, rfl⟩ := (seq_range_eq_inSeq d a).mpr hIa
    obtain ⟨j, rfl⟩ := (seq_range_eq_inSeq d b).mpr hIb
    obtain ⟨l, rfl⟩ := (seq_range_eq_inSeq d c).mpr hIc
    have hij : i < j := by
      by_cases h : i < j
      · exact h
      · by_cases heq : i = j
        · subst heq; omega
        · have := seq_strictMono d (by omega : j < i); omega
    have hjl : j < l := by
      by_cases h : j < l
      · exact h
      · by_cases heq : j = l
        · subst heq; omega
        · have := seq_strictMono d (by omega : l < j); omega
    have hln : l ≤ n := by
      by_cases h : l ≤ n
      · exact h
      · by_cases heq : n + 1 = l
        · subst heq; omega
        · have := seq_strictMono d (by omega : n + 1 < l); omega
    exact ⟨i, j, l, hij, hjl, hln, hsum⟩

/-- Ultimate periodicity with preperiod `k`, positive period `p`, and step/modulus `m`. -/
def HasPeriodMod (seq : Nat → Nat) (k p m : Nat) : Prop :=
  p > 0 ∧ ∀ i ≥ k, seq (i + p) = seq i + m

/-- Exact minimal periodicity predicate for `(k, p, m)` on `seq`. -/
def IsMinimalPeriodicity (seq : Nat → Nat) (k p m : Nat) : Prop :=
  HasPeriodMod seq k p m ∧
  (∀ p', p' > 0 → (∃ k' m', HasPeriodMod seq k' p' m') → p ≤ p') ∧
  (∀ k', HasPeriodMod seq k' p m → k ≤ k')

/-- Minimal periodicity parameters `(k, p, m)` are unique whenever they exist. -/
theorem unique_minimal_periodicity {f : Nat → Nat} {k p m k' p' m' : Nat}
    (h1 : IsMinimalPeriodicity f k p m) (h2 : IsMinimalPeriodicity f k' p' m') :
    k = k' ∧ p = p' ∧ m = m' := by
  have hp1 : p ≤ p' := h1.2.1 p' h2.1.1 ⟨k', m', h2.1⟩
  have hp2 : p' ≤ p := h2.2.1 p h1.1.1 ⟨k, m, h1.1⟩
  have hpeq : p = p' := by omega
  subst hpeq
  let idx := max k k'
  have hm1 : f (idx + p) = f idx + m := h1.1.2 idx (by omega)
  have hm2 : f (idx + p) = f idx + m' := h2.1.2 idx (by omega)
  have hmeq : m = m' := by omega
  subst hmeq
  have hk1 : k ≤ k' := h1.2.2 k' h2.1
  have hk2 : k' ≤ k := h2.2.2 k h1.1
  exact ⟨by omega, rfl, rfl⟩

namespace Internal

/-- General strong-induction bridge: if `A` agrees with the seed on `[0, 2d - 1]`, is strictly
    3-sumfree, and covers every gap above `2d - 1` by a strict 3-sum in `A`, then
    `InSeq d x ↔ A x` for all `x`. -/
theorem inSeq_iff_of_characterization (d : Nat) (hd : d ≥ 3) (A : Nat → Prop)
    (hseed : ∀ x ≤ 2 * d - 1, A x ↔ (x = 1 ∨ x = d - 1 ∨ x = 2 * d - 1))
    (hexcl : ∀ a b c, A a → A b → A c → a < b → b < c → ¬ A (a + b + c))
    (hincl : ∀ x > 2 * d - 1, ¬ A x → ∃ a b c, A a ∧ A b ∧ A c ∧ a < b ∧ b < c ∧ a + b + c = x) :
    ∀ x, InSeq d x ↔ A x := by
  have hA0 : ¬ A 0 := by
    intro h0
    have := (hseed 0 (by omega)).mp h0
    omega
  intro x
  induction x using Nat.strongRecOn with
  | ind x ih =>
    by_cases hx : x ≤ 2 * d - 1
    · rw [inSeq_seed d x hd hx, hseed x hx]
    · have hxgt : x > 2 * d - 1 := by omega
      rw [inSeq_gt d x hxgt]
      constructor
      · intro hnot
        by_cases hAx : A x
        · exact hAx
        · obtain ⟨a, b, c, hAa, hAb, hAc, hab, hbc, hsum⟩ := hincl x hxgt hAx
          have ha0 : a ≥ 1 := by
            cases a with
            | zero => exact False.elim (hA0 hAa)
            | succ _ => omega
          have hax : a < x := by omega
          have hbx : b < x := by omega
          have hcx : c < x := by omega
          exact False.elim (hnot ⟨a, b, c,
            ⟨hax, (ih a hax).mpr hAa⟩,
            ⟨hbx, (ih b hbx).mpr hAb⟩,
            ⟨hcx, (ih c hcx).mpr hAc⟩,
            hab, hbc, hsum⟩)
      · intro hAx ⟨a, b, c, ⟨hax, hIa⟩, ⟨hbx, hIb⟩, ⟨hcx, hIc⟩, hab, hbc, hsum⟩
        have hAa := (ih a hax).mp hIa
        have hAb := (ih b hbx).mp hIb
        have hAc := (ih c hcx).mp hIc
        rw [← hsum] at hAx
        exact hexcl a b c hAa hAb hAc hab hbc hAx

theorem hasPeriodMod_iter {f : Nat → Nat} {k p m : Nat}
    (hper : ∀ i ≥ k, f (i + p) = f i + m) {n : Nat} (hn : n ≥ k) :
    ∀ q, f (n + p * q) = f n + m * q
  | 0 => by simp
  | q + 1 => by
    have h1 : n + p * (q + 1) = (n + p * q) + p := by rw [Nat.mul_succ]; omega
    rw [h1, hper (n + p * q) (by omega), hasPeriodMod_iter hper hn q, Nat.mul_succ]
    omega

/-- General minimality criterion via a unique cyclic gap `r0 < p` and preperiod break at `k - 1`. -/
theorem minimal_periodicity_of_unique_gap {f : Nat → Nat} {k p m : Nat}
    (hf : ∀ i, f i < f (i + 1))
    (hp : p > 0)
    (hper : ∀ i ≥ k, f (i + p) = f i + m)
    (huniq : ∃ r0, r0 < p ∧ ∀ s, 0 < s → s < p →
      f (k + r0 + s + 1) - f (k + r0 + s) ≠ f (k + r0 + 1) - f (k + r0))
    (hpre : k > 0 ∧ f ((k - 1) + p) ≠ f (k - 1) + m) :
    IsMinimalPeriodicity f k p m := by
  refine ⟨⟨hp, hper⟩, ?_, ?_⟩
  · intro p' hp' ⟨k', m', _, hper'⟩
    by_cases hle : p ≤ p'
    · exact hle
    · obtain ⟨r0, _, hgapne⟩ := huniq
      have hp'lt : p' < p := by omega
      have hpk : k' ≤ p * k' := by
        have : 1 * k' ≤ p * k' := Nat.mul_le_mul_right k' hp
        omega
      let j := (k + r0) + p * k'
      have hj1 : f (j + p') = f j + m' := hper' j (by omega)
      have hj2 : f ((j + 1) + p') = f (j + 1) + m' := hper' (j + 1) (by omega)
      have hfj_lt : f j < f (j + 1) := hf j
      have hit0 : f j = f (k + r0) + m * k' := hasPeriodMod_iter hper (by omega) k'
      have hit1 : f (j + 1) = f (k + r0 + 1) + m * k' := by
        have heq : j + 1 = (k + r0 + 1) + p * k' := by omega
        rw [heq]; exact hasPeriodMod_iter hper (by omega) k'
      have hit2 : f (j + p') = f (k + r0 + p') + m * k' := by
        have heq : j + p' = (k + r0 + p') + p * k' := by omega
        rw [heq]; exact hasPeriodMod_iter hper (by omega) k'
      have hit3 : f ((j + 1) + p') = f (k + r0 + p' + 1) + m * k' := by
        have heq : (j + 1) + p' = (k + r0 + p' + 1) + p * k' := by omega
        rw [heq]; exact hasPeriodMod_iter hper (by omega) k'
      have hkr0_lt : f (k + r0) < f (k + r0 + 1) := hf (k + r0)
      have hkrp_lt : f (k + r0 + p') < f (k + r0 + p' + 1) := hf (k + r0 + p')
      have heq_gap : f (k + r0 + p' + 1) - f (k + r0 + p') = f (k + r0 + 1) - f (k + r0) := by
        omega
      exact False.elim (hgapne p' hp' hp'lt heq_gap)
  · intro k' ⟨_, hper'⟩
    by_cases hle : k ≤ k'
    · exact hle
    · have := hper' (k - 1) (by omega)
      exact False.elim (hpre.2 this)

/-! ### Reusable Small-Case Certificate Engine (`d = 3, 4, 5`) -/

theorem bool_beq_iff (a b : Bool) : Bool.beq a b = true ↔ a = b := by
  cases a <;> cases b <;> decide

theorem nat_beq_false_iff (a b : Nat) : Nat.beq a b = false ↔ a ≠ b := by
  cases h : Nat.beq a b
  · simp only [true_iff]
    intro heq
    subst heq
    have ht : Nat.beq a a = true := by rw [Nat.beq_eq]
    rw [h] at ht
    cases ht
  · simp only [Bool.true_eq_false, false_iff]
    intro hne
    rw [Nat.beq_eq] at h
    exact hne h

theorem add_mul_div_mod (r q m : Nat) (hr : r < m) :
    (r + m * q) % m = r ∧ (r + m * q) / m = q := by
  induction q with
  | zero =>
    simp [Nat.mod_eq_of_lt hr, Nat.div_eq_of_lt hr]
  | succ q ih =>
    have h1 : r + m * (q + 1) = (r + m * q) + m := by rw [Nat.mul_succ]; omega
    rw [h1, Nat.add_mod_right, Nat.add_div_right _ (by omega)]
    exact ⟨ih.1, by rw [ih.2]⟩

theorem mod_sub_of_add_mod_eq {u c0 x m : Nat} (hm : m > 0)
    (hle : u + c0 ≤ x) (hmod : (u + c0) % m = x % m) :
    (x - u) % m = c0 % m := by
  have hsum : (x - u) + u = x := by omega
  have hmod2 : ((x - u) + u) % m = (c0 + u) % m := by
    rw [hsum, Nat.add_comm c0 u, hmod]
  have h1 : ((x - u) % m + u % m) % m = (c0 % m + u % m) % m := by
    rw [← Nat.add_mod, ← Nat.add_mod, hmod2]
  have _hlt1 : (x - u) % m < m := Nat.mod_lt _ hm
  have _hlt2 : c0 % m < m := Nat.mod_lt _ hm
  have _hlt3 : u % m < m := Nat.mod_lt _ hm
  by_cases hsum1 : (x - u) % m + u % m < m <;> by_cases hsum2 : c0 % m + u % m < m
  · rw [Nat.mod_eq_of_lt hsum1, Nat.mod_eq_of_lt hsum2] at h1
    omega
  · have h2 : c0 % m + u % m = (c0 % m + u % m - m) + m * 1 := by omega
    have hm2 := (add_mul_div_mod (c0 % m + u % m - m) 1 m (by omega)).1
    rw [← h2] at hm2
    rw [Nat.mod_eq_of_lt hsum1, hm2] at h1
    omega
  · have h2 : (x - u) % m + u % m = ((x - u) % m + u % m - m) + m * 1 := by omega
    have hm1 := (add_mul_div_mod ((x - u) % m + u % m - m) 1 m (by omega)).1
    rw [← h2] at hm1
    rw [hm1, Nat.mod_eq_of_lt hsum2] at h1
    omega
  · have h2 : (x - u) % m + u % m = ((x - u) % m + u % m - m) + m * 1 := by omega
    have hm1 := (add_mul_div_mod ((x - u) % m + u % m - m) 1 m (by omega)).1
    rw [← h2] at hm1
    have h3 : c0 % m + u % m = (c0 % m + u % m - m) + m * 1 := by omega
    have hm2 := (add_mul_div_mod (c0 % m + u % m - m) 1 m (by omega)).1
    rw [← h3] at hm2
    rw [hm1, hm2] at h1
    omega

theorem step_ge_of_mod_eq {a b m : Nat} (_hm : m > 0) (hlt : a < b) (hmod : a % m = b % m) :
    a + m ≤ b := by
  have ha : a = a % m + m * (a / m) := (Nat.mod_add_div a m).symm
  have hb : b = b % m + m * (b / m) := (Nat.mod_add_div b m).symm
  have hqlt : a / m < b / m := by
    by_cases h : a / m < b / m
    · exact h
    · have hle : m * (b / m) ≤ m * (a / m) := Nat.mul_le_mul_left m (by omega)
      omega
  have hqle : m * (a / m + 1) ≤ m * (b / m) := Nat.mul_le_mul_left m hqlt
  rw [Nat.mul_succ] at hqle
  omega

def inABoolAux (m : Nat) (iso : List Nat) (progs : List (Nat × Nat)) (x : Nat) : Bool :=
  iso.any (fun v => Nat.beq v x) || progs.any (fun rs => Nat.ble rs.2 x && Nat.beq (x % m) rs.1)

def makeTags (m : Nat) (iso : List Nat) (progs : List (Nat × Nat)) : List (Bool × Nat × Nat) :=
  iso.map (fun v => (true, v, v % m)) ++ progs.map (fun rs => (false, rs.2, rs.1))

def tagEq (t1 t2 : Bool × Nat × Nat) : Bool :=
  Bool.beq t1.1 t2.1 && Nat.beq t1.2.1 t2.2.1 && Nat.beq t1.2.2 t2.2.2

theorem tagEq_iff (t1 t2 : Bool × Nat × Nat) : tagEq t1 t2 = true ↔ t1 = t2 := by
  rcases t1 with ⟨b1, v1, r1⟩
  rcases t2 with ⟨b2, v2, r2⟩
  unfold tagEq
  simp only [Bool.and_eq_true, bool_beq_iff, Nat.beq_eq]
  constructor
  · rintro ⟨⟨rfl, rfl⟩, rfl⟩; rfl
  · rintro ⟨rfl, rfl, rfl⟩; exact ⟨⟨rfl, rfl⟩, rfl⟩

theorem tagEq_false_iff (t1 t2 : Bool × Nat × Nat) : tagEq t1 t2 = false ↔ t1 ≠ t2 := by
  cases h : tagEq t1 t2
  · simp only [true_iff]
    intro heq
    have := (tagEq_iff t1 t2).mpr heq
    rw [h] at this; cases this
  · simp only [Bool.true_eq_false, false_iff]
    intro hne
    exact hne ((tagEq_iff t1 t2).mp h)

def matchesTag (m : Nat) (t : Bool × Nat × Nat) (x : Nat) : Prop :=
  match t.1 with
  | true => x = t.2.1 ∧ t.2.1 % m = t.2.2
  | false => t.2.1 ≤ x ∧ x % m = t.2.2 ∧ t.2.1 % m = t.2.2

theorem matchesTag_mod {m : Nat} {t : Bool × Nat × Nat} {x : Nat}
    (h : matchesTag m t x) : x % m = t.2.2 := by
  rcases t with ⟨b, v, r⟩
  cases b <;> simp only [matchesTag] at h
  · exact h.2.1
  · rw [h.1]; exact h.2

theorem matchesTag_ge {m : Nat} {t : Bool × Nat × Nat} {x : Nat}
    (h : matchesTag m t x) : t.2.1 ≤ x := by
  rcases t with ⟨b, v, r⟩
  cases b <;> simp only [matchesTag] at h
  · exact h.1
  · dsimp only; omega

theorem matchesTag_iso_eq {m : Nat} {t : Bool × Nat × Nat} {x : Nat}
    (hb : t.1 = true) (h : matchesTag m t x) : x = t.2.1 := by
  rcases t with ⟨b, v, r⟩
  cases b
  · cases hb
  · simp only [matchesTag] at h; exact h.1

def tagSumLb (m : Nat) (t1 t2 t3 : Bool × Nat × Nat) : Nat :=
  t1.2.1 +
  (t2.2.1 + (if tagEq t1 t2 then m else 0)) +
  (t3.2.1 + (if tagEq t1 t2 && tagEq t2 t3 then 2 * m
             else if tagEq t1 t3 || tagEq t2 t3 then m else 0))

theorem tagSumLb_le {m a b c : Nat} {t1 t2 t3 : Bool × Nat × Nat}
    (hm : m > 0) (hab : a < b) (hbc : b < c)
    (ht1 : matchesTag m t1 a) (ht2 : matchesTag m t2 b) (ht3 : matchesTag m t3 c) :
    tagSumLb m t1 t2 t3 ≤ a + b + c := by
  unfold tagSumLb
  have ha_ge := matchesTag_ge ht1
  have hb_ge := matchesTag_ge ht2
  have hc_ge := matchesTag_ge ht3
  have ha_mod := matchesTag_mod ht1
  have hb_mod := matchesTag_mod ht2
  have hc_mod := matchesTag_mod ht3
  have hlb2 : t2.2.1 + (if tagEq t1 t2 then m else 0) ≤ b := by
    by_cases h12 : t1 = t2
    · rw [(tagEq_iff t1 t2).mpr h12]
      subst h12
      simp only [↓reduceIte]
      have hs := step_ge_of_mod_eq hm hab (by rw [ha_mod, hb_mod])
      omega
    · rw [(tagEq_false_iff t1 t2).mpr h12]
      simp only [Bool.false_eq_true, ↓reduceIte, Nat.add_zero]
      exact hb_ge
  have hlb3 : t3.2.1 + (if tagEq t1 t2 && tagEq t2 t3 then 2 * m
      else if tagEq t1 t3 || tagEq t2 t3 then m else 0) ≤ c := by
    by_cases h12 : t1 = t2
    · rw [(tagEq_iff t1 t2).mpr h12]
      by_cases h23 : t2 = t3
      · rw [(tagEq_iff t2 t3).mpr h23]
        subst h12; subst h23
        simp only [Bool.and_self, ↓reduceIte]
        have hs1 := step_ge_of_mod_eq hm hab (by rw [ha_mod, hb_mod])
        have hs2 := step_ge_of_mod_eq hm hbc (by rw [hb_mod, hc_mod])
        omega
      · rw [(tagEq_false_iff t2 t3).mpr h23]
        subst h12
        rw [(tagEq_false_iff t1 t3).mpr h23]
        simp only [Bool.and_false, Bool.or_self, Bool.false_eq_true, ↓reduceIte, Nat.add_zero]
        exact hc_ge
    · rw [(tagEq_false_iff t1 t2).mpr h12]
      simp only [Bool.false_and, Bool.false_eq_true, ↓reduceIte]
      by_cases h13 : t1 = t3
      · rw [(tagEq_iff t1 t3).mpr h13]
        subst h13
        simp only [Bool.true_or, ↓reduceIte]
        have hs := step_ge_of_mod_eq hm (Nat.lt_trans hab hbc) (by rw [ha_mod, hc_mod])
        omega
      · rw [(tagEq_false_iff t1 t3).mpr h13]
        by_cases h23 : t2 = t3
        · rw [(tagEq_iff t2 t3).mpr h23]
          subst h23
          simp only [Bool.or_true, ↓reduceIte]
          have hs := step_ge_of_mod_eq hm hbc (by rw [hb_mod, hc_mod])
          omega
        · rw [(tagEq_false_iff t2 t3).mpr h23]
          simp only [Bool.or_self, Bool.false_eq_true, ↓reduceIte, Nat.add_zero]
          exact hc_ge
  omega

theorem tagSumLb_eq_of_iso {m a b c : Nat} {t1 t2 t3 : Bool × Nat × Nat}
    (hab : a < b) (hbc : b < c)
    (hi1 : t1.1 = true) (hi2 : t2.1 = true) (hi3 : t3.1 = true)
    (ht1 : matchesTag m t1 a) (ht2 : matchesTag m t2 b) (ht3 : matchesTag m t3 c) :
    a + b + c = tagSumLb m t1 t2 t3 := by
  have ha := matchesTag_iso_eq hi1 ht1
  have hb := matchesTag_iso_eq hi2 ht2
  have hc := matchesTag_iso_eq hi3 ht3
  have hne12 : t1 ≠ t2 := by intro h; subst h; omega
  have hne23 : t2 ≠ t3 := by intro h; subst h; omega
  have hne13 : t1 ≠ t3 := by intro h; subst h; omega
  unfold tagSumLb
  rw [(tagEq_false_iff t1 t2).mpr hne12, (tagEq_false_iff t2 t3).mpr hne23,
      (tagEq_false_iff t1 t3).mpr hne13]
  simp only [Bool.false_and, Bool.or_self, Bool.false_eq_true, ↓reduceIte, Nat.add_zero]
  omega

theorem add3_mod_eq {m a b c r1 r2 r3 : Nat}
    (ha : a % m = r1) (hb : b % m = r2) (hc : c % m = r3) :
    (a + b + c) % m = (r1 + r2 + r3) % m := by
  calc (a + b + c) % m
      = ((a + b) % m + c % m) % m := Nat.add_mod (a + b) c m
    _ = (((a % m + b % m) % m) + c % m) % m := by rw [Nat.add_mod a b m]
    _ = ((r1 + r2) % m + r3) % m := by rw [ha, hb, hc]
    _ = (r1 + r2 + r3) % m := Nat.mod_add_mod (r1 + r2) m r3

theorem list_any_iff {α : Type} (l : List α) (p : α → Bool) :
    l.any p = true ↔ ∃ a ∈ l, p a = true := by
  induction l with
  | nil => simp [List.any]
  | cons hd tl ih =>
    simp only [List.any, Bool.or_eq_true, List.mem_cons]
    constructor
    · rintro (h | h)
      · exact ⟨hd, Or.inl rfl, h⟩
      · obtain ⟨a, ha, pa⟩ := ih.mp h
        exact ⟨a, Or.inr ha, pa⟩
    · rintro ⟨a, rfl | ha, pa⟩
      · exact Or.inl pa
      · exact Or.inr (ih.mpr ⟨a, ha, pa⟩)

theorem list_all_iff {α : Type} (l : List α) (p : α → Bool) :
    l.all p = true ↔ ∀ a ∈ l, p a = true := by
  induction l with
  | nil => simp [List.all]
  | cons hd tl ih =>
    simp only [List.all, Bool.and_eq_true, List.mem_cons]
    constructor
    · rintro ⟨h1, h2⟩ a (rfl | ha)
      · exact h1
      · exact ih.mp h2 a ha
    · intro h
      exact ⟨h hd (Or.inl rfl), ih.mpr (fun a ha => h a (Or.inr ha))⟩

def allRange (start count : Nat) (p : Nat → Bool) : Bool :=
  match count with
  | 0 => true
  | count' + 1 => p start && allRange (start + 1) count' p

theorem allRange_iff (start count : Nat) (p : Nat → Bool) :
    allRange start count p = true ↔ ∀ x, start ≤ x → x < start + count → p x = true := by
  induction count generalizing start with
  | zero =>
    simp [allRange]
    intro x h1 h2; omega
  | succ _ ih =>
    simp only [allRange, Bool.and_eq_true, ih]
    constructor
    · rintro ⟨h0, hrest⟩ x h1 h2
      by_cases hx : x = start
      · subst hx; exact h0
      · exact hrest x (by omega) (by omega)
    · intro h
      exact ⟨h start (by omega) (by omega), fun x h1 h2 => h x (by omega) (by omega)⟩

def allWithIdx {α : Type} (l : List α) (idx : Nat) (p : Nat → α → Bool) : Bool :=
  match l with
  | [] => true
  | hd :: tl => p idx hd && allWithIdx tl (idx + 1) p

theorem allWithIdx_getD {α : Type} (l : List α) (idx : Nat) (dflt : α) (p : Nat → α → Bool)
    (h : allWithIdx l idx p = true) :
    ∀ k < l.length, p (idx + k) (l.getD k dflt) = true := by
  induction l generalizing idx with
  | nil => intro k hk; simp at hk
  | cons _ tl ih =>
    simp only [allWithIdx, Bool.and_eq_true] at h
    intro k hk
    cases k with
    | zero =>
      simpa [List.getD] using h.1
    | succ k' =>
      simp only [List.length_cons] at hk
      have := ih (idx + 1) h.2 k' (by omega)
      have heq : idx + 1 + k' = idx + (k' + 1) := by omega
      rw [heq] at this
      simpa [List.getD] using this

def checkTagOut (res slb : Nat) (allIso : Bool) (tout : Bool × Nat × Nat) : Bool :=
  match tout.1 with
  | true => !Nat.beq res tout.2.2 || Nat.ble (tout.2.1 + 1) slb
  | false => !Nat.beq res tout.2.2 || (allIso && Nat.ble (slb + 1) tout.2.1)

def checkTagTriple (m : Nat) (tags : List (Bool × Nat × Nat))
    (t1 t2 t3 : Bool × Nat × Nat) : Bool :=
  if (tagEq t1 t2 && t1.1) || (tagEq t2 t3 && t2.1) || (tagEq t1 t3 && t1.1) then
    true
  else
    let slb := tagSumLb m t1 t2 t3
    let res := (t1.2.2 + t2.2.2 + t3.2.2) % m
    let allIso := t1.1 && t2.1 && t3.1
    tags.all (checkTagOut res slb allIso)

def checkAllTags (m : Nat) (ts : List (Bool × Nat × Nat)) : Bool :=
  ts.all (fun t1 => ts.all (fun t2 => ts.all (fun t3 => checkTagTriple m ts t1 t2 t3)))

theorem checkTagTriple_sound {m a b c : Nat} {tags : List (Bool × Nat × Nat)}
    {t1 t2 t3 tout : Bool × Nat × Nat}
    (hm : m > 0) (hab : a < b) (hbc : b < c)
    (ht1 : matchesTag m t1 a) (ht2 : matchesTag m t2 b) (ht3 : matchesTag m t3 c)
    (htout_mem : tout ∈ tags) (htout : matchesTag m tout (a + b + c))
    (hok : checkTagTriple m tags t1 t2 t3 = true) : False := by
  unfold checkTagTriple at hok
  have hdup : ((tagEq t1 t2 && t1.1) || (tagEq t2 t3 && t2.1) || (tagEq t1 t3 && t1.1)) = false := by
    rw [Bool.or_eq_false_iff, Bool.or_eq_false_iff]
    refine ⟨⟨?_, ?_⟩, ?_⟩
    · by_cases h12 : t1 = t2
      · subst h12
        cases hb1 : t1.1
        · simp
        · have e1 := matchesTag_iso_eq hb1 ht1
          have e2 := matchesTag_iso_eq hb1 ht2
          omega
      · rw [(tagEq_false_iff t1 t2).mpr h12]; simp
    · by_cases h23 : t2 = t3
      · subst h23
        cases hb2 : t2.1
        · simp
        · have e2 := matchesTag_iso_eq hb2 ht2
          have e3 := matchesTag_iso_eq hb2 ht3
          omega
      · rw [(tagEq_false_iff t2 t3).mpr h23]; simp
    · by_cases h13 : t1 = t3
      · subst h13
        cases hb1 : t1.1
        · simp
        · have e1 := matchesTag_iso_eq hb1 ht1
          have e3 := matchesTag_iso_eq hb1 ht3
          omega
      · rw [(tagEq_false_iff t1 t3).mpr h13]; simp
  rw [hdup] at hok
  simp only [Bool.false_eq_true, ↓reduceIte] at hok
  have hout := (list_all_iff _ _).mp hok tout htout_mem
  have hslb := tagSumLb_le hm hab hbc ht1 ht2 ht3
  have hres := add3_mod_eq (matchesTag_mod ht1) (matchesTag_mod ht2) (matchesTag_mod ht3)
  have htout_mod := matchesTag_mod htout
  rcases tout with ⟨bout, vout, rout⟩
  cases bout
  · simp only [checkTagOut, Bool.or_eq_true, Bool.not_eq_true', nat_beq_false_iff,
      Bool.and_eq_true, Nat.ble_eq] at hout
    simp only [matchesTag] at htout
    rcases hout with hne | ⟨⟨⟨hi1, hi2⟩, hi3⟩, hlt⟩
    · exact hne (by rw [← hres, htout_mod])
    · have heq := tagSumLb_eq_of_iso hab hbc hi1 hi2 hi3 ht1 ht2 ht3
      have hvle : vout ≤ a + b + c := htout.1
      omega
  · simp only [checkTagOut, Bool.or_eq_true, Bool.not_eq_true', nat_beq_false_iff,
      Nat.ble_eq] at hout
    simp only [matchesTag] at htout
    rcases hout with hne | hlt
    · exact hne (by rw [← hres, htout_mod])
    · have hveq : a + b + c = vout := htout.1
      omega

def evalSeqAux (k p m : Nat) (pre blk : List Nat) (i : Nat) : Nat :=
  if Nat.ble (i + 1) k then
    pre.getD i 0
  else
    blk.getD ((i - k) % p) 0 + m * ((i - k) / p)

def checkParams (d k p m thresh : Nat) (pre blk : List Nat)
    (fgList rcList : List (Nat × Nat × Nat)) : Bool :=
  Nat.ble 3 d && Nat.ble 1 k && Nat.ble 1 p && Nat.ble 1 m &&
  Nat.beq pre.length k && Nat.beq blk.length p &&
  Nat.beq fgList.length thresh && Nat.beq rcList.length m

def checkProgsWf (m thresh : Nat) (progs : List (Nat × Nat)) : Bool :=
  progs.all (fun rs =>
    Nat.ble (rs.1 + 1) m && Nat.beq (rs.2 % m) rs.1 && Nat.ble rs.2 thresh)

def checkSeed (d m : Nat) (iso : List Nat) (progs : List (Nat × Nat)) : Bool :=
  allRange 0 (2 * d) (fun x =>
    Bool.beq (inABoolAux m iso progs x)
      (Nat.beq x 1 || Nat.beq x (d - 1) || Nat.beq x (2 * d - 1)))

def checkFg (d m : Nat) (iso : List Nat) (progs : List (Nat × Nat))
    (fgList : List (Nat × Nat × Nat)) : Bool :=
  allWithIdx fgList 0 (fun x abc =>
    if Nat.ble (x + 1) (2 * d) || inABoolAux m iso progs x then
      true
    else
      let (a, b, c) := abc
      inABoolAux m iso progs a &&
      inABoolAux m iso progs b &&
      inABoolAux m iso progs c &&
      Nat.ble (a + 1) b && Nat.ble (b + 1) c && Nat.beq (a + b + c) x)

def checkRc (m thresh : Nat) (iso : List Nat) (progs : List (Nat × Nat))
    (rcList : List (Nat × Nat × Nat)) : Bool :=
  allWithIdx rcList 0 (fun r abc =>
    if progs.any (fun rs => Nat.beq rs.1 r) then
      true
    else
      let (a, b, c0) := abc
      inABoolAux m iso progs a &&
      inABoolAux m iso progs b &&
      Nat.ble (a + 1) b && Nat.ble (b + 1) c0 &&
      Nat.ble (a + b + c0) thresh && Nat.beq ((a + b + c0) % m) r &&
      progs.any (fun rs => Nat.beq (c0 % m) rs.1 && Nat.ble rs.2 c0))

def checkTail (m B : Nat) (iso : List Nat) (progs : List (Nat × Nat)) : Bool :=
  iso.all (fun v => Nat.ble (v + 1) B) &&
  progs.all (fun rs =>
    Nat.ble rs.2 B ||
    (Nat.ble (rs.2 + 1) (B + m) &&
      allRange B (rs.2 - B) (fun x => !Nat.beq (x % m) rs.1)))

def checkEnum (k p m : Nat) (pre blk iso : List Nat) (progs : List (Nat × Nat)) : Bool :=
  let f := evalSeqAux k p m pre blk
  Nat.beq (f 0) 1 && (!inABoolAux m iso progs 0) &&
  allRange 0 (k + p) (fun i =>
    let u := f i
    let v := f (i + 1)
    Nat.ble (u + 1) v && inABoolAux m iso progs u &&
      allRange (u + 1) (v - u - 1) (fun z => !inABoolAux m iso progs z)) &&
  (!Nat.beq (f ((k - 1) + p)) (f (k - 1) + m)) &&
  allRange 0 1 (fun _ =>
    (List.range p).any fun r0 =>
      allRange 1 (p - 1) fun s =>
        !Nat.beq (f (k + r0 + s + 1) - f (k + r0 + s))
          (f (k + r0 + 1) - f (k + r0)))

theorem smallCert_sound
    (d k p m thresh : Nat)
    (iso : List Nat) (progs : List (Nat × Nat))
    (tags : List (Bool × Nat × Nat))
    (pre blk : List Nat)
    (fgList rcList : List (Nat × Nat × Nat))
    (htags : tags = makeTags m iso progs)
    (hparams : checkParams d k p m thresh pre blk fgList rcList = true)
    (hprogs_wf : checkProgsWf m thresh progs = true)
    (hseed_ok : checkSeed d m iso progs = true)
    (hexcl_ok : checkAllTags m tags = true)
    (hfg_ok : checkFg d m iso progs fgList = true)
    (hrc_ok : checkRc m thresh iso progs rcList = true)
    (htail_ok : checkTail m (blk.getD 0 0) iso progs = true)
    (henum_all : checkEnum k p m pre blk iso progs = true) :
    IsMinimalPeriodicity (seq d) k p m := by
  unfold checkParams at hparams
  simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq] at hparams
  rcases hparams with ⟨⟨⟨⟨⟨⟨⟨hd, hk⟩, hp⟩, hm⟩, _hpre_len⟩, _hblk_len⟩, hfg_len⟩, hrc_len⟩

  unfold checkTail at htail_ok
  simp only [Bool.and_eq_true] at htail_ok
  rcases htail_ok with ⟨hiso_B, hprogs_B⟩

  unfold checkEnum at henum_all
  simp only [Bool.and_eq_true, Nat.beq_eq, Bool.not_eq_true', nat_beq_false_iff] at henum_all
  rcases henum_all with ⟨⟨⟨⟨hf0, hnA0⟩, henum_ok⟩, hpre_break⟩, huniq_ok⟩

  let A (x : Nat) : Prop := inABoolAux m iso progs x = true
  let f := evalSeqAux k p m pre blk

  have hprog_mem : ∀ r s, (r, s) ∈ progs → r < m ∧ s % m = r ∧ s ≤ thresh := by
    intro r s hrs
    unfold checkProgsWf at hprogs_wf
    have h := (list_all_iff _ _).mp hprogs_wf (r, s) hrs
    simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq] at h
    exact ⟨by omega, h.1.2, h.2⟩

  have hA_to_tag : ∀ x, A x → ∃ t ∈ tags, matchesTag m t x := by
    intro x hx
    unfold A inABoolAux at hx
    rw [Bool.or_eq_true] at hx
    rcases hx with hiso | hprog
    · obtain ⟨v, hv_mem, hvx⟩ := (list_any_iff _ _).mp hiso
      rw [Nat.beq_eq] at hvx
      refine ⟨(true, v, v % m), ?_, ?_⟩
      · rw [htags]
        simp only [makeTags, List.mem_append, List.mem_map]
        exact Or.inl ⟨v, hv_mem, rfl⟩
      · simp [matchesTag, hvx]
    · obtain ⟨⟨r, s⟩, hrs_mem, hrs_ok⟩ := (list_any_iff _ _).mp hprog
      simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq] at hrs_ok
      have hwf := hprog_mem r s hrs_mem
      refine ⟨(false, s, r), ?_, ?_⟩
      · rw [htags]
        simp only [makeTags, List.mem_append, List.mem_map]
        exact Or.inr ⟨(r, s), hrs_mem, rfl⟩
      · simp [matchesTag, hrs_ok.1, hrs_ok.2, hwf.2.1]

  have hseed : ∀ x ≤ 2 * d - 1, A x ↔ (x = 1 ∨ x = d - 1 ∨ x = 2 * d - 1) := by
    intro x hx
    unfold checkSeed at hseed_ok
    have h := (allRange_iff 0 (2 * d) _).mp hseed_ok x (by omega) (by omega)
    rw [bool_beq_iff] at h
    unfold A
    rw [h]
    simp only [Bool.or_eq_true, Nat.beq_eq, or_assoc]

  have hexcl : ∀ a b c, A a → A b → A c → a < b → b < c → ¬ A (a + b + c) := by
    intro a b c hAa hAb hAc hab hbc hAsum
    obtain ⟨t1, ht1_mem, ht1⟩ := hA_to_tag a hAa
    obtain ⟨t2, ht2_mem, ht2⟩ := hA_to_tag b hAb
    obtain ⟨t3, ht3_mem, ht3⟩ := hA_to_tag c hAc
    obtain ⟨tout, htout_mem, htout⟩ := hA_to_tag (a + b + c) hAsum
    unfold checkAllTags at hexcl_ok
    have h1 := (list_all_iff _ _).mp hexcl_ok t1 ht1_mem
    have h2 := (list_all_iff _ _).mp h1 t2 ht2_mem
    have h3 := (list_all_iff _ _).mp h2 t3 ht3_mem
    exact checkTagTriple_sound hm hab hbc ht1 ht2 ht3 htout_mem htout h3

  have hincl : ∀ x > 2 * d - 1, ¬ A x →
      ∃ a b c, A a ∧ A b ∧ A c ∧ a < b ∧ b < c ∧ a + b + c = x := by
    intro x hxgt hnAx
    by_cases hxth : x < thresh
    · unfold checkFg at hfg_ok
      have hfg := allWithIdx_getD fgList 0 (0, 0, 0) _ hfg_ok x (by omega)
      simp only [Nat.zero_add] at hfg
      have hble_f : Nat.ble (x + 1) (2 * d) = false := by
        cases h : Nat.ble (x + 1) (2 * d)
        · rfl
        · rw [Nat.ble_eq] at h; omega
      have hcond : (Nat.ble (x + 1) (2 * d) || inABoolAux m iso progs x) = false := by
        rw [hble_f, Bool.false_or]
        cases h : inABoolAux m iso progs x
        · rfl
        · exact False.elim (hnAx h)
      rw [hcond] at hfg
      simp only [Bool.false_eq_true, ↓reduceIte] at hfg
      rcases htr : fgList.getD x (0, 0, 0) with ⟨a, b, c⟩
      rw [htr] at hfg
      simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq] at hfg
      exact ⟨a, b, c, hfg.1.1.1.1.1, hfg.1.1.1.1.2, hfg.1.1.1.2,
        by omega, by omega, hfg.2⟩
    · let r := x % m
      have hrm : r < m := Nat.mod_lt x hm
      unfold checkRc at hrc_ok
      have hrc := allWithIdx_getD rcList 0 (0, 0, 0) _ hrc_ok r (by omega)
      simp only [Nat.zero_add] at hrc
      have hnprog : progs.any (fun rs => Nat.beq rs.1 r) = false := by
        cases hp_any : progs.any (fun rs => Nat.beq rs.1 r)
        · rfl
        · obtain ⟨⟨rp, sp⟩, hrp_mem, hrp_eq⟩ := (list_any_iff _ _).mp hp_any
          rw [Nat.beq_eq] at hrp_eq
          have hwf := hprog_mem rp sp hrp_mem
          have hA_true : inABoolAux m iso progs x = true := by
            unfold inABoolAux
            rw [Bool.or_eq_true]
            refine Or.inr ((list_any_iff _ _).mpr ⟨(rp, sp), hrp_mem, ?_⟩)
            simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq]
            exact ⟨by omega, by omega⟩
          exact False.elim (hnAx hA_true)
      rw [hnprog] at hrc
      simp only [Bool.false_eq_true, ↓reduceIte] at hrc
      rcases htr : rcList.getD r (0, 0, 0) with ⟨a, b, c0⟩
      rw [htr] at hrc
      simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq] at hrc
      rcases hrc with ⟨⟨⟨⟨⟨⟨hAa, hAb⟩, hab⟩, hbc0⟩, hle_th⟩, hmod_r⟩, hc0_prog⟩
      obtain ⟨⟨rp, sp⟩, hrp_mem, hc0_ok⟩ := (list_any_iff _ _).mp hc0_prog
      simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq] at hc0_ok
      let c := x - (a + b)
      have hcm : c % m = c0 % m :=
        mod_sub_of_add_mod_eq hm (by omega : a + b + c0 ≤ x) hmod_r
      have hAc : A c := by
        unfold A inABoolAux
        rw [Bool.or_eq_true]
        refine Or.inr ((list_any_iff _ _).mpr ⟨(rp, sp), hrp_mem, ?_⟩)
        simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq]
        exact ⟨by omega, by omega⟩
      exact ⟨a, b, c, hAa, hAb, hAc, by omega, by omega, by omega⟩

  have hInSeq_iff : ∀ x, InSeq d x ↔ A x :=
    inSeq_iff_of_characterization d hd A hseed hexcl hincl

  let B := blk.getD 0 0
  have hshift1 : ∀ z ≥ B, inABoolAux m iso progs (z + m) = inABoolAux m iso progs z := by
    intro z hzB
    unfold inABoolAux
    have hiso_z : iso.any (fun v => Nat.beq v z) = false := by
      cases h : iso.any (fun v => Nat.beq v z)
      · rfl
      · obtain ⟨v, hv_mem, hvz⟩ := (list_any_iff _ _).mp h
        rw [Nat.beq_eq] at hvz
        have hvlt := (list_all_iff _ _).mp hiso_B v hv_mem
        rw [Nat.ble_eq] at hvlt
        omega
    have hiso_zm : iso.any (fun v => Nat.beq v (z + m)) = false := by
      cases h : iso.any (fun v => Nat.beq v (z + m))
      · rfl
      · obtain ⟨v, hv_mem, hvz⟩ := (list_any_iff _ _).mp h
        rw [Nat.beq_eq] at hvz
        have hvlt := (list_all_iff _ _).mp hiso_B v hv_mem
        rw [Nat.ble_eq] at hvlt
        omega
    rw [hiso_z, hiso_zm, Bool.false_or, Bool.false_or]
    cases hpz : progs.any (fun rs => Nat.ble rs.2 z && Nat.beq (z % m) rs.1)
    · cases hpzm : progs.any (fun rs => Nat.ble rs.2 (z + m) && Nat.beq ((z + m) % m) rs.1)
      · rfl
      · obtain ⟨⟨r, s⟩, hrs_mem, hrs_zm⟩ := (list_any_iff _ _).mp hpzm
        simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq, Nat.add_mod_right] at hrs_zm
        have hpB := (list_all_iff _ _).mp hprogs_B (r, s) hrs_mem
        simp only [Bool.or_eq_true, Bool.and_eq_true, Nat.ble_eq] at hpB
        have hsz : s ≤ z := by
          rcases hpB with hsB | ⟨_, hrange⟩
          · omega
          · by_cases hlt : z < s
            · have hne := (allRange_iff B (s - B) _).mp hrange z hzB (by omega)
              rw [Bool.not_eq_true', nat_beq_false_iff] at hne
              exact False.elim (hne hrs_zm.2)
            · omega
        have hpz_true : progs.any (fun rs => Nat.ble rs.2 z && Nat.beq (z % m) rs.1) = true := by
          refine (list_any_iff _ _).mpr ⟨(r, s), hrs_mem, ?_⟩
          simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq]
          exact ⟨hsz, hrs_zm.2⟩
        rw [hpz] at hpz_true
        cases hpz_true
    · obtain ⟨⟨r, s⟩, hrs_mem, hrs_z⟩ := (list_any_iff _ _).mp hpz
      simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq] at hrs_z
      refine (list_any_iff _ _).mpr ⟨(r, s), hrs_mem, ?_⟩
      simp only [Bool.and_eq_true, Nat.ble_eq, Nat.beq_eq, Nat.add_mod_right]
      exact ⟨by omega, hrs_z.2⟩

  have hshift_iter : ∀ z ≥ B, ∀ q, inABoolAux m iso progs (z + m * q) = inABoolAux m iso progs z := by
    intro z hzB q
    induction q with
    | zero => simp
    | succ q ih =>
      have heq : z + m * (q + 1) = (z + m * q) + m := by rw [Nat.mul_succ]; omega
      rw [heq, hshift1 (z + m * q) (by omega), ih]

  have heval_per : ∀ i ≥ k, f (i + p) = f i + m := by
    intro i hik
    dsimp only [f]
    unfold evalSeqAux
    have h1 : Nat.ble (i + 1) k = false := by
      cases h : Nat.ble (i + 1) k
      · rfl
      · rw [Nat.ble_eq] at h; omega
    have h2 : Nat.ble (i + p + 1) k = false := by
      cases h : Nat.ble (i + p + 1) k
      · rfl
      · rw [Nat.ble_eq] at h; omega
    have hu : (i + p) - k = (i - k) + p := by omega
    simp only [h1, h2, Bool.false_eq_true, ↓reduceIte, hu, Nat.add_mod_right,
      Nat.add_div_right _ hp, Nat.mul_succ]
    omega

  have heval_k : f k = B := by
    dsimp only [f]
    unfold evalSeqAux
    have h1 : Nat.ble (k + 1) k = false := by
      cases h : Nat.ble (k + 1) k
      · rfl
      · rw [Nat.ble_eq] at h; omega
    simp only [h1, Bool.false_eq_true, ↓reduceIte, Nat.sub_self, Nat.zero_mod,
      Nat.zero_div, Nat.mul_zero, Nat.add_zero]
    rfl

  have henum_base : ∀ i < k + p,
      f i < f (i + 1) ∧
      A (f i) ∧
      (∀ z, f i < z → z < f (i + 1) → ¬ A z) := by
    intro i hi
    have h := (allRange_iff 0 (k + p) _).mp henum_ok i (by omega) (by omega)
    simp only [Bool.and_eq_true, Nat.ble_eq] at h
    refine ⟨by dsimp only [f]; omega, h.1.2, ?_⟩
    intro z hz1 hz2 hAz
    have hz := (allRange_iff (f i + 1) (f (i + 1) - f i - 1) _).mp
      h.2 z (by omega) (by omega)
    rw [Bool.not_eq_true'] at hz
    unfold A at hAz
    rw [hz] at hAz
    cases hAz

  have heval_ge_B : ∀ r < p, B ≤ f (k + r) := by
    intro r hr
    induction r with
    | zero => simp [heval_k]
    | succ r' ih =>
      have hstep := (henum_base (k + r') (by omega)).1
      have hprev := ih (by omega)
      have heq : k + (r' + 1) = k + r' + 1 := by omega
      rw [heq]
      omega

  have hf_step : ∀ i, f i < f (i + 1) := by
    intro i
    by_cases hik : i < k + p
    · exact (henum_base i hik).1
    · have hr : (i - k) % p < p := Nat.mod_lt _ hp
      have hdivmod := Nat.mod_add_div (i - k) p
      have hi_eq : i = (k + (i - k) % p) + p * ((i - k) / p) := by omega
      have hi1 : i + 1 = (k + (i - k) % p + 1) + p * ((i - k) / p) := by omega
      have h0 := hasPeriodMod_iter heval_per
        (by omega : k + (i - k) % p ≥ k) ((i - k) / p)
      have h1 := hasPeriodMod_iter heval_per
        (by omega : k + (i - k) % p + 1 ≥ k) ((i - k) / p)
      rw [← hi_eq] at h0
      rw [← hi1] at h1
      have hbase := (henum_base (k + (i - k) % p) (by omega)).1
      omega

  have hf_mem : ∀ i, A (f i) := by
    intro i
    by_cases hik : i < k + p
    · exact (henum_base i hik).2.1
    · have hr : (i - k) % p < p := Nat.mod_lt _ hp
      have hdivmod := Nat.mod_add_div (i - k) p
      have hi_eq : i = (k + (i - k) % p) + p * ((i - k) / p) := by omega
      have h0 := hasPeriodMod_iter heval_per
        (by omega : k + (i - k) % p ≥ k) ((i - k) / p)
      rw [← hi_eq] at h0
      have hB := heval_ge_B ((i - k) % p) hr
      unfold A
      rw [h0, hshift_iter (f (k + (i - k) % p)) hB ((i - k) / p)]
      exact (henum_base (k + (i - k) % p) (by omega)).2.1

  have hf_below0 : ∀ x, x < f 0 → ¬ A x := by
    intro x hx
    change x < evalSeqAux k p m pre blk 0 at hx
    rw [hf0] at hx
    have hx0 : x = 0 := by omega
    subst hx0
    unfold A
    rw [hnA0]
    decide

  have hf_gap : ∀ i x, f i < x → x < f (i + 1) → ¬ A x := by
    intro i x hx1 hx2
    by_cases hik : i < k + p
    · exact (henum_base i hik).2.2 x hx1 hx2
    · have hr : (i - k) % p < p := Nat.mod_lt _ hp
      have hdivmod := Nat.mod_add_div (i - k) p
      have hi_eq : i = (k + (i - k) % p) + p * ((i - k) / p) := by omega
      have hi1 : i + 1 = (k + (i - k) % p + 1) + p * ((i - k) / p) := by omega
      have h0 := hasPeriodMod_iter heval_per
        (by omega : k + (i - k) % p ≥ k) ((i - k) / p)
      have h1 := hasPeriodMod_iter heval_per
        (by omega : k + (i - k) % p + 1 ≥ k) ((i - k) / p)
      rw [← hi_eq] at h0
      rw [← hi1] at h1
      let x0 := x - m * ((i - k) / p)
      have hx_eq : x = x0 + m * ((i - k) / p) := by omega
      have hB := heval_ge_B ((i - k) % p) hr
      have hx0_B : x0 ≥ B := by omega
      intro hAx
      unfold A at hAx
      rw [hx_eq, hshift_iter x0 hx0_B ((i - k) / p)] at hAx
      exact (henum_base (k + (i - k) % p) (by omega)).2.2 x0 (by omega) (by omega) hAx

  have hrange_eval : ∀ x, (∃ i, f i = x) ↔ (∃ i, seq d i = x) := by
    intro x
    rw [range_iff_of_step_gaps hf_step hf_mem hf_below0 hf_gap x,
        seq_range_eq_inSeq d x, hInSeq_iff x]

  have hseq_eq : ∀ i, f i = seq d i :=
    eq_of_strictMono_same_range hf_step (seq_step_lt d) hrange_eval

  have hfun_eq : f = seq d := funext hseq_eq
  rw [← hfun_eq]

  have huniq_any := (allRange_iff 0 1 _).mp huniq_ok 0 (by omega) (by omega)
  obtain ⟨r0, hr0_mem, hr0_ok⟩ := (list_any_iff _ _).mp huniq_any
  rw [List.mem_range] at hr0_mem
  have huniq : ∃ r0, r0 < p ∧ ∀ s, 0 < s → s < p →
      f (k + r0 + s + 1) - f (k + r0 + s) ≠
        f (k + r0 + 1) - f (k + r0) := by
    refine ⟨r0, hr0_mem, ?_⟩
    intro s hs1 hs2
    have hs := (allRange_iff 1 (p - 1) _).mp hr0_ok s (by omega) (by omega)
    rwa [Bool.not_eq_true', nat_beq_false_iff] at hs

  exact minimal_periodicity_of_unique_gap hf_step hp heval_per huniq ⟨hk, hpre_break⟩

/-! ### Concrete Certificates for `d = 3`, `d = 4`, and `d = 5` -/

def iso3 : List Nat := [2, 5, 7]
def progs3 : List (Nat × Nat) := [(1, 1)]
def tags3 : List (Bool × Nat × Nat) := [(true, 2, 2), (true, 5, 0), (true, 7, 2), (false, 1, 1)]
def pre3 : List Nat := [1, 2, 5, 6, 7]
def blk3 : List Nat := [11]
def fg3 : List (Nat × Nat × Nat) := [
  (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
  (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 2, 5), (1, 2, 6),
  (1, 2, 7), (0, 0, 0), (1, 5, 6), (1, 5, 7), (1, 2, 11),
  (2, 6, 7), (0, 0, 0), (1, 5, 11), (1, 6, 11), (1, 2, 16)
]
def rc3 : List (Nat × Nat × Nat) := [(2, 7, 11), (0, 0, 0), (1, 5, 6), (2, 5, 6), (1, 2, 6)]

def iso4 : List Nat := [1, 3, 7, 10, 15]
def progs4 : List (Nat × Nat) := [(2, 29), (8, 8), (9, 9)]
def tags4 : List (Bool × Nat × Nat) := [
  (true, 1, 1), (true, 3, 3), (true, 7, 7), (true, 10, 10), (true, 15, 15),
  (false, 29, 2), (false, 8, 8), (false, 9, 9)
]
def pre4 : List Nat := [1, 3, 7, 8, 9, 10, 15]
def blk4 : List Nat := [29, 35, 36]
def fg4 : List (Nat × Nat × Nat) := [
  (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
  (0, 0, 0), (1, 3, 7), (1, 3, 8), (1, 3, 9), (1, 3, 10), (0, 0, 0), (1, 7, 8), (1, 7, 9), (1, 7, 10), (1, 3, 15),
  (1, 9, 10), (3, 8, 10), (3, 9, 10), (1, 7, 15), (1, 8, 15), (1, 9, 15), (1, 10, 15), (3, 9, 15), (3, 10, 15), (0, 0, 0),
  (7, 8, 15), (7, 9, 15), (7, 10, 15), (1, 3, 29), (9, 10, 15), (0, 0, 0), (0, 0, 0), (1, 7, 29), (1, 8, 29), (1, 3, 35),
  (1, 3, 36), (3, 9, 29), (3, 10, 29), (1, 7, 35), (1, 7, 36), (1, 8, 36), (1, 9, 36), (1, 10, 36), (3, 9, 36), (3, 10, 36),
  (7, 8, 35), (1, 15, 35), (1, 15, 36), (3, 15, 35), (3, 15, 36), (9, 10, 36), (0, 0, 0), (7, 15, 35), (7, 15, 36), (8, 15, 36),
  (1, 3, 56)
]
def rc4 : List (Nat × Nat × Nat) := [
  (3, 15, 36), (9, 10, 36), (0, 0, 0), (7, 15, 35), (7, 15, 36), (8, 15, 36), (1, 3, 29), (10, 15, 36), (0, 0, 0),
  (0, 0, 0), (1, 7, 29), (1, 8, 29), (1, 3, 8), (1, 3, 9), (3, 9, 29), (3, 10, 29), (1, 7, 8), (1, 7, 9),
  (1, 8, 9), (3, 7, 9), (3, 8, 9), (3, 9, 36), (3, 10, 36), (7, 8, 35), (7, 8, 9), (1, 15, 36), (3, 15, 35)
]

def iso5 : List Nat := [1, 4, 9, 13, 37, 79]
def progs5 : List (Nat × Nat) := [
  (10, 10), (11, 11), (12, 12), (19, 19), (45, 45),
  (46, 46), (54, 158), (72, 72), (80, 80), (81, 81)
]
def tags5 : List (Bool × Nat × Nat) := [
  (true, 1, 1), (true, 4, 4), (true, 9, 9), (true, 13, 13), (true, 37, 37), (true, 79, 79),
  (false, 10, 10), (false, 11, 11), (false, 12, 12), (false, 19, 19), (false, 45, 45),
  (false, 46, 46), (false, 158, 54), (false, 72, 72), (false, 80, 80), (false, 81, 81)
]
def pre5 : List Nat := [1, 4, 9, 10, 11, 12, 13, 19, 37, 45, 46, 72, 79]
def blk5 : List Nat := [80, 81, 114, 115, 116, 123, 149, 150, 158, 176]
def fg5 : List (Nat × Nat × Nat) := [
  (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
  (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 4, 9), (1, 4, 10), (1, 4, 11), (1, 4, 12), (1, 4, 13), (0, 0, 0),
  (1, 9, 10), (1, 9, 11), (1, 9, 12), (1, 9, 13), (1, 4, 19), (1, 11, 13), (1, 12, 13), (4, 10, 13), (4, 11, 13), (1, 9, 19),
  (1, 10, 19), (1, 11, 19), (1, 12, 19), (1, 13, 19), (4, 11, 19), (4, 12, 19), (4, 13, 19), (0, 0, 0), (9, 10, 19), (9, 11, 19),
  (9, 12, 19), (9, 13, 19), (1, 4, 37), (11, 13, 19), (12, 13, 19), (0, 0, 0), (0, 0, 0), (1, 9, 37), (1, 10, 37), (1, 11, 37),
  (1, 4, 45), (1, 4, 46), (4, 11, 37), (4, 12, 37), (4, 13, 37), (1, 9, 45), (1, 9, 46), (1, 10, 46), (1, 11, 46), (1, 12, 46),
  (1, 13, 46), (4, 11, 46), (4, 12, 46), (4, 13, 46), (9, 10, 45), (1, 19, 45), (1, 19, 46), (9, 12, 46), (4, 19, 45), (4, 19, 46),
  (11, 13, 46), (12, 13, 46), (0, 0, 0), (9, 19, 45), (9, 19, 46), (10, 19, 46), (11, 19, 46), (1, 4, 72), (13, 19, 46), (0, 0, 0),
  (0, 0, 0), (0, 0, 0), (1, 9, 72), (1, 10, 72), (1, 4, 79), (1, 4, 80), (1, 4, 81), (4, 11, 72), (4, 12, 72), (1, 9, 79),
  (1, 9, 80), (1, 9, 81), (1, 10, 81), (1, 11, 81), (1, 12, 81), (1, 13, 81), (4, 11, 81), (4, 12, 81), (4, 13, 81), (1, 19, 79),
  (1, 19, 80), (1, 19, 81), (4, 19, 79), (4, 19, 80), (4, 19, 81), (11, 13, 81), (12, 13, 81), (9, 19, 79), (9, 19, 80), (9, 19, 81),
  (1, 37, 72), (11, 19, 81), (12, 19, 81), (4, 37, 72), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 37, 79), (1, 37, 80), (1, 4, 114),
  (1, 4, 115), (1, 4, 116), (4, 37, 81), (0, 0, 0), (1, 9, 114), (1, 9, 115), (1, 9, 116), (1, 10, 116), (1, 4, 123), (1, 12, 116),
  (1, 13, 116), (4, 11, 116), (4, 12, 116), (1, 9, 123), (1, 10, 123), (1, 11, 123), (1, 12, 123), (1, 13, 123), (4, 11, 123), (4, 12, 123),
  (4, 13, 123), (12, 13, 116), (9, 10, 123), (1, 19, 123), (9, 12, 123), (9, 13, 123), (4, 19, 123), (11, 13, 123), (12, 13, 123), (0, 0, 0),
  (0, 0, 0), (9, 19, 123), (1, 37, 114), (1, 37, 115), (1, 4, 149), (1, 4, 150), (4, 37, 115), (4, 37, 116), (0, 0, 0), (1, 9, 149),
  (1, 9, 150), (1, 10, 150), (1, 11, 150), (1, 4, 158), (1, 13, 150), (4, 11, 150), (4, 12, 150), (4, 13, 150), (1, 9, 158), (1, 10, 158),
  (1, 11, 158), (1, 12, 158), (1, 13, 158), (4, 11, 158), (4, 12, 158), (4, 13, 158), (0, 0, 0), (9, 10, 158), (1, 19, 158), (9, 12, 158),
  (9, 13, 158), (1, 4, 176), (11, 13, 158), (12, 13, 158), (0, 0, 0), (0, 0, 0), (1, 9, 176), (1, 10, 176), (1, 11, 176), (1, 4, 184),
  (1, 4, 185), (4, 11, 176), (4, 12, 176), (4, 13, 176), (1, 9, 184), (1, 9, 185), (1, 10, 185), (1, 11, 185), (1, 12, 185), (1, 13, 185),
  (4, 11, 185), (4, 12, 185), (4, 13, 185), (1, 79, 123), (1, 19, 184), (1, 19, 185), (4, 79, 123), (4, 19, 184), (4, 19, 185), (11, 13, 185),
  (12, 13, 185), (9, 79, 123), (9, 19, 184), (9, 19, 185), (1, 37, 176), (11, 19, 185), (12, 19, 185), (4, 37, 176), (0, 0, 0), (0, 0, 0),
  (0, 0, 0)
]
def rc5 : List (Nat × Nat × Nat) := [
  (4, 19, 81), (11, 13, 81), (12, 13, 81), (9, 79, 123), (9, 19, 80), (9, 19, 81), (1, 37, 72), (11, 19, 81),
  (12, 19, 81), (4, 37, 72), (0, 0, 0), (0, 0, 0), (0, 0, 0), (19, 79, 123), (1, 37, 80), (1, 4, 10),
  (1, 4, 11), (1, 4, 12), (4, 37, 81), (0, 0, 0), (1, 9, 10), (1, 9, 11), (1, 9, 12), (1, 10, 12),
  (1, 4, 19), (4, 9, 12), (4, 10, 12), (4, 11, 12), (4, 12, 116), (1, 9, 19), (1, 10, 19), (1, 11, 19),
  (1, 12, 19), (1, 13, 19), (4, 11, 19), (4, 12, 19), (4, 13, 19), (12, 13, 116), (9, 10, 19), (9, 11, 19),
  (9, 12, 19), (9, 13, 19), (10, 13, 19), (11, 13, 19), (12, 13, 19), (0, 0, 0), (0, 0, 0), (9, 19, 123),
  (1, 37, 114), (1, 37, 115), (1, 4, 45), (1, 4, 46), (4, 37, 115), (4, 37, 116), (0, 0, 0), (1, 9, 45),
  (1, 9, 46), (1, 10, 46), (1, 11, 46), (1, 12, 46), (1, 13, 46), (4, 11, 46), (4, 12, 46), (4, 13, 46),
  (9, 10, 45), (1, 19, 45), (1, 19, 46), (9, 12, 46), (4, 19, 45), (4, 19, 46), (11, 13, 46), (12, 13, 46),
  (0, 0, 0), (9, 19, 45), (9, 19, 46), (10, 19, 46), (11, 19, 46), (1, 4, 72), (13, 19, 46), (12, 13, 158),
  (0, 0, 0), (0, 0, 0), (1, 9, 72), (1, 10, 72), (1, 11, 72), (1, 4, 80), (1, 4, 81), (4, 11, 72),
  (4, 12, 72), (4, 13, 72), (1, 9, 80), (1, 9, 81), (1, 10, 81), (1, 11, 81), (1, 12, 81), (1, 13, 81),
  (4, 11, 81), (4, 12, 81), (4, 13, 81), (9, 10, 80), (1, 19, 80), (1, 19, 81), (9, 12, 81), (4, 19, 80)
]

/-! ### General Algebraic Proof for All `d >= 6` -/

/-- Closed-form periodic membership predicate `Ad d x` for `S_{1, d-1, 2d-1}` (`d >= 6`),
    with preperiod `{1, d - 1} U [2d - 1, 3d - 2] U {4d - 1}` and periodic blocks
    `[10d - 5 + j*(8d - 3), 11d - 6 + j*(8d - 3)]` (`j >= 0`). -/
def Ad (d x : Nat) : Prop :=
  x = 1 ∨ x = d - 1 ∨ (2 * d - 1 ≤ x ∧ x ≤ 3 * d - 2) ∨ x = 4 * d - 1 ∨
    (10 * d - 5 ≤ x ∧ 2 * d - 2 ≤ x % (8 * d - 3) ∧ x % (8 * d - 3) ≤ 3 * d - 3)

/-- Canonical quotient-residue characterization of `Ad d x` modulo `8d - 3`. -/
def AdQR (d r q : Nat) : Prop :=
  (r = 1 ∧ q = 0) ∨
  (r = d - 1 ∧ q = 0) ∨
  (2 * d - 2 ≤ r ∧ r ≤ 3 * d - 2 ∧ (r = 2 * d - 2 → q ≥ 1) ∧ (r = 3 * d - 2 → q = 0)) ∨
  (r = 4 * d - 1 ∧ q = 0)

theorem ad_iff_qr (d x : Nat) (hd : d ≥ 6) :
    Ad d x ↔ AdQR d (x % (8 * d - 3)) (x / (8 * d - 3)) := by
  have hm : 8 * d - 3 > 0 := by omega
  have hrlt : x % (8 * d - 3) < 8 * d - 3 := Nat.mod_lt x hm
  have hxeq : x = x % (8 * d - 3) + (8 * d - 3) * (x / (8 * d - 3)) :=
    (Nat.mod_add_div x (8 * d - 3)).symm
  unfold Ad AdQR
  cases hq : x / (8 * d - 3) with
  | zero =>
    rw [hq, Nat.mul_zero, Nat.add_zero] at hxeq
    omega
  | succ q' =>
    cases q' with
    | zero =>
      rw [hq, Nat.mul_one] at hxeq
      omega
    | succ q'' =>
      have hge2 : (8 * d - 3) * 2 ≤ (8 * d - 3) * (q'' + 1 + 1) :=
        Nat.mul_le_mul_left (8 * d - 3) (by omega)
      rw [hq] at hxeq
      omega

theorem ad_iff_of_div_mod {d x r q : Nat} (hd : d ≥ 6)
    (hmod : x % (8 * d - 3) = r) (hdiv : x / (8 * d - 3) = q) :
    Ad d x ↔ AdQR d r q := by
  rw [ad_iff_qr d x hd, hmod, hdiv]

theorem ad_seed (d x : Nat) (hd : d ≥ 6) (hx : x ≤ 2 * d - 1) :
    Ad d x ↔ (x = 1 ∨ x = d - 1 ∨ x = 2 * d - 1) := by
  unfold Ad
  omega

/-- Pure linear arithmetic exclusion core on canonical quotient-residue pairs. -/
theorem adQR_sum_excl (d ra qa rb qb rc qc rs qs : Nat) (hd : d ≥ 6)
    (hab : ¬ (ra = rb ∧ qa = qb))
    (hbc : ¬ (rb = rc ∧ qb = qc))
    (hac : ¬ (ra = rc ∧ qa = qc))
    (ha : AdQR d ra qa) (hb : AdQR d rb qb) (hc : AdQR d rc qc)
    (hcarry : (ra + rb + rc < 8 * d - 3 ∧ rs = ra + rb + rc ∧ qs = qa + qb + qc) ∨
              (8 * d - 3 ≤ ra + rb + rc ∧ rs = ra + rb + rc - (8 * d - 3) ∧
                qs = qa + qb + qc + 1)) :
    ¬ AdQR d rs qs := by
  unfold AdQR at ha hb hc
  intro hs
  unfold AdQR at hs
  rcases ha with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | haJ | ⟨rfl, rfl⟩
  · omega
  · omega
  · rcases hb with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | hbJ | ⟨rfl, rfl⟩ <;> omega
  · omega

theorem adQR_r_upper {d r q : Nat} (hd : d ≥ 6) (h : AdQR d r q) : r ≤ 4 * d - 1 := by
  unfold AdQR at h
  omega

theorem sum3_div_mod (a b c m : Nat) :
    a + b + c = (a % m + b % m + c % m) + m * (a / m + b / m + c / m) := by
  have ha := Nat.mod_add_div a m
  have hb := Nat.mod_add_div b m
  have hc := Nat.mod_add_div c m
  rw [Nat.left_distrib, Nat.left_distrib]
  omega

/-- Part A (Exclusion): `Ad d` is strictly 3-sumfree for every `d >= 6`. -/
theorem ad_excl (d : Nat) (hd : d ≥ 6) (a b c : Nat)
    (hAa : Ad d a) (hAb : Ad d b) (hAc : Ad d c) (hab : a < b) (hbc : b < c) :
    ¬ Ad d (a + b + c) := by
  intro hAsum
  have ha_eq : a = a % (8 * d - 3) + (8 * d - 3) * (a / (8 * d - 3)) :=
    (Nat.mod_add_div a (8 * d - 3)).symm
  have hb_eq : b = b % (8 * d - 3) + (8 * d - 3) * (b / (8 * d - 3)) :=
    (Nat.mod_add_div b (8 * d - 3)).symm
  have hc_eq : c = c % (8 * d - 3) + (8 * d - 3) * (c / (8 * d - 3)) :=
    (Nat.mod_add_div c (8 * d - 3)).symm
  have hab_ne : ¬ (a % (8 * d - 3) = b % (8 * d - 3) ∧ a / (8 * d - 3) = b / (8 * d - 3)) := by
    rintro ⟨h1, h2⟩; rw [ha_eq, hb_eq, h1, h2] at hab; omega
  have hbc_ne : ¬ (b % (8 * d - 3) = c % (8 * d - 3) ∧ b / (8 * d - 3) = c / (8 * d - 3)) := by
    rintro ⟨h1, h2⟩; rw [hb_eq, hc_eq, h1, h2] at hbc; omega
  have hac_ne : ¬ (a % (8 * d - 3) = c % (8 * d - 3) ∧ a / (8 * d - 3) = c / (8 * d - 3)) := by
    rintro ⟨h1, h2⟩
    have hac := Nat.lt_trans hab hbc
    rw [ha_eq, hc_eq, h1, h2] at hac
    omega
  have qra := (ad_iff_qr d a hd).mp hAa
  have qrb := (ad_iff_qr d b hd).mp hAb
  have qrc := (ad_iff_qr d c hd).mp hAc
  have hra_le := adQR_r_upper hd qra
  have hrb_le := adQR_r_upper hd qrb
  have hrc_le := adQR_r_upper hd qrc
  have hsum_eq := sum3_div_mod a b c (8 * d - 3)
  by_cases hcarry : a % (8 * d - 3) + b % (8 * d - 3) + c % (8 * d - 3) < 8 * d - 3
  · obtain ⟨hmod, hdiv⟩ := add_mul_div_mod
      (a % (8 * d - 3) + b % (8 * d - 3) + c % (8 * d - 3))
      (a / (8 * d - 3) + b / (8 * d - 3) + c / (8 * d - 3))
      (8 * d - 3) hcarry
    rw [← hsum_eq] at hmod hdiv
    have qrsum := (ad_iff_of_div_mod hd hmod hdiv).mp hAsum
    exact adQR_sum_excl d
      (a % (8 * d - 3)) (a / (8 * d - 3))
      (b % (8 * d - 3)) (b / (8 * d - 3))
      (c % (8 * d - 3)) (c / (8 * d - 3))
      (a % (8 * d - 3) + b % (8 * d - 3) + c % (8 * d - 3))
      (a / (8 * d - 3) + b / (8 * d - 3) + c / (8 * d - 3))
      hd hab_ne hbc_ne hac_ne qra qrb qrc (Or.inl ⟨hcarry, rfl, rfl⟩) qrsum
  · have hrew :
        (a % (8 * d - 3) + b % (8 * d - 3) + c % (8 * d - 3)) +
          (8 * d - 3) * (a / (8 * d - 3) + b / (8 * d - 3) + c / (8 * d - 3)) =
        (a % (8 * d - 3) + b % (8 * d - 3) + c % (8 * d - 3) - (8 * d - 3)) +
          (8 * d - 3) * (a / (8 * d - 3) + b / (8 * d - 3) + c / (8 * d - 3) + 1) := by
      rw [Nat.mul_succ]; omega
    obtain ⟨hmod, hdiv⟩ := add_mul_div_mod
      (a % (8 * d - 3) + b % (8 * d - 3) + c % (8 * d - 3) - (8 * d - 3))
      (a / (8 * d - 3) + b / (8 * d - 3) + c / (8 * d - 3) + 1)
      (8 * d - 3) (by omega)
    rw [← hrew, ← hsum_eq] at hmod hdiv
    have qrsum := (ad_iff_of_div_mod hd hmod hdiv).mp hAsum
    exact adQR_sum_excl d
      (a % (8 * d - 3)) (a / (8 * d - 3))
      (b % (8 * d - 3)) (b / (8 * d - 3))
      (c % (8 * d - 3)) (c / (8 * d - 3))
      (a % (8 * d - 3) + b % (8 * d - 3) + c % (8 * d - 3) - (8 * d - 3))
      (a / (8 * d - 3) + b / (8 * d - 3) + c / (8 * d - 3) + 1)
      hd hab_ne hbc_ne hac_ne qra qrb qrc (Or.inr ⟨by omega, rfl, rfl⟩) qrsum

/-- Elementary Interval-Sum Lemma (1): pairwise distinct sums in `[alpha, beta]`. -/
theorem pair_sum_interval (α β s : Nat) (_hL : α + 1 ≤ β)
    (hs1 : 2 * α + 1 ≤ s) (hs2 : s ≤ 2 * β - 1) :
    ∃ u v, α ≤ u ∧ u < v ∧ v ≤ β ∧ u + v = s := by
  by_cases h : s ≤ α + β
  · exact ⟨α, s - α, by omega, by omega, by omega, by omega⟩
  · exact ⟨s - β, β, by omega, by omega, by omega, by omega⟩

/-- Elementary Interval-Sum Lemma (2): triple distinct sums in `[alpha, beta]`. -/
theorem triple_sum_interval (α β s : Nat) (_hL : α + 2 ≤ β)
    (hs1 : 3 * α + 3 ≤ s) (hs2 : s ≤ 3 * β - 3) :
    ∃ u v w, α ≤ u ∧ u < v ∧ v < w ∧ w ≤ β ∧ u + v + w = s := by
  by_cases h : s ≤ α + 2 * β - 1
  · obtain ⟨v, w, _, hvw, hw2, _⟩ :=
      pair_sum_interval (α + 1) β (s - α) (by omega) (by omega) (by omega)
    exact ⟨α, v, w, by omega, by omega, hvw, hw2, by omega⟩
  · obtain ⟨u, v, hu1, huv, _, _⟩ :=
      pair_sum_interval α (β - 1) (s - β) (by omega) (by omega) (by omega)
    exact ⟨u, v, β, hu1, huv, by omega, by omega, by omega⟩

theorem ad_of_Istar {d x : Nat} (h1 : 2 * d - 1 ≤ x) (h2 : x ≤ 3 * d - 2) : Ad d x :=
  Or.inr (Or.inr (Or.inl ⟨h1, h2⟩))

theorem ad_1 (d : Nat) : Ad d 1 := Or.inl rfl
theorem ad_dm1 (d : Nat) : Ad d (d - 1) := Or.inr (Or.inl rfl)
theorem ad_4dm1 (d : Nat) : Ad d (4 * d - 1) := Or.inr (Or.inr (Or.inr (Or.inl rfl)))

theorem ad_of_Tj (d c0 j : Nat) (hd : d ≥ 6)
    (hc1 : 10 * d - 5 ≤ c0) (hc2 : c0 ≤ 11 * d - 6) :
    Ad d (c0 + (8 * d - 3) * j) := by
  have hrew : c0 + (8 * d - 3) * j = (c0 - (8 * d - 3)) + (8 * d - 3) * (j + 1) := by
    rw [Nat.mul_succ]; omega
  obtain ⟨hmod, hdiv⟩ := add_mul_div_mod (c0 - (8 * d - 3)) (j + 1) (8 * d - 3) (by omega)
  rw [← hrew] at hmod hdiv
  rw [ad_iff_of_div_mod hd hmod hdiv]
  unfold AdQR
  refine Or.inr (Or.inr (Or.inl ?_))
  omega

/-- Covering preperiod gaps `G_{pre,1}` and `G_{pre,2}` (`2d <= n <= 10d - 6`). -/
theorem ad_cover_pre (d n : Nat) (hd : d ≥ 6)
    (hn1 : 2 * d ≤ n) (hn2 : n ≤ 10 * d - 6) (hnA : ¬ Ad d n) :
    ∃ a b c, Ad d a ∧ Ad d b ∧ Ad d c ∧ a < b ∧ b < c ∧ a + b + c = n := by
  have _hnot_pre : ¬ (2 * d - 1 ≤ n ∧ n ≤ 3 * d - 2) ∧ n ≠ 4 * d - 1 := by
    unfold Ad at hnA; omega
  by_cases hg1 : n ≤ 4 * d - 2
  · exact ⟨1, d - 1, n - d, ad_1 d, ad_dm1 d,
      ad_of_Istar (by omega) (by omega), by omega, by omega, by omega⟩
  · by_cases hb1 : n ≤ 6 * d - 4
    · obtain ⟨u, v, hu, huv, hv, _⟩ :=
        pair_sum_interval (2 * d - 1) (3 * d - 2) (n - 1) (by omega) (by omega) (by omega)
      exact ⟨1, u, v, ad_1 d, ad_of_Istar hu (by omega), ad_of_Istar (by omega) hv,
        by omega, huv, by omega⟩
    · by_cases hb2 : n ≤ 7 * d - 6
      · obtain ⟨u, v, hu, huv, hv, _⟩ :=
          pair_sum_interval (2 * d - 1) (3 * d - 2) (n - (d - 1))
            (by omega) (by omega) (by omega)
        exact ⟨d - 1, u, v, ad_dm1 d, ad_of_Istar hu (by omega), ad_of_Istar (by omega) hv,
          by omega, huv, by omega⟩
      · by_cases hb3 : n ≤ 7 * d - 2
        · exact ⟨1, n - 4 * d, 4 * d - 1, ad_1 d, ad_of_Istar (by omega) (by omega),
            ad_4dm1 d, by omega, by omega, by omega⟩
        · by_cases hb4 : n ≤ 9 * d - 9
          · obtain ⟨u, v, w, hu, huv, hvw, hw, hsum⟩ :=
              triple_sum_interval (2 * d - 1) (3 * d - 2) n (by omega) (by omega) (by omega)
            exact ⟨u, v, w, ad_of_Istar hu (by omega), ad_of_Istar (by omega) (by omega),
              ad_of_Istar (by omega) hw, huv, hvw, hsum⟩
          · obtain ⟨u, v, hu, huv, hv, _⟩ :=
              pair_sum_interval (2 * d - 1) (3 * d - 2) (n - (4 * d - 1))
                (by omega) (by omega) (by omega)
            exact ⟨u, v, 4 * d - 1, ad_of_Istar hu (by omega), ad_of_Istar (by omega) hv,
              ad_4dm1 d, huv, by omega, by omega⟩

theorem split_with_T0 (d u0 u1 s : Nat) (_hd : d ≥ 6) (hu : u0 ≤ u1)
    (hs1 : u0 + (10 * d - 5) ≤ s) (hs2 : s ≤ u1 + (11 * d - 6)) :
    ∃ uv c0, u0 ≤ uv ∧ uv ≤ u1 ∧ 10 * d - 5 ≤ c0 ∧ c0 ≤ 11 * d - 6 ∧ uv + c0 = s := by
  by_cases h : s - u0 ≤ 11 * d - 6
  · exact ⟨u0, s - u0, Nat.le_refl _, hu, by omega, h, by omega⟩
  · exact ⟨s - (11 * d - 6), 11 * d - 6, by omega, by omega, by omega, Nat.le_refl _, by omega⟩

/-- Base periodic gap cover `G_0 = [11d - 5, 18d - 9]` via `C_{1,0} .. C_{5,0}`. -/
theorem ad_cover_per0 (d s : Nat) (hd : d ≥ 6)
    (hs1 : 11 * d - 5 ≤ s) (hs2 : s ≤ 18 * d - 9) :
    ∃ a b c0, Ad d a ∧ Ad d b ∧ a < b ∧ b ≤ 4 * d - 1 ∧
      10 * d - 5 ≤ c0 ∧ c0 ≤ 11 * d - 6 ∧ a + b + c0 = s := by
  by_cases hc1 : s ≤ 12 * d - 6
  · exact ⟨1, d - 1, s - d, ad_1 d, ad_dm1 d, by omega, by omega, by omega, by omega, by omega⟩
  · by_cases hc2 : s ≤ 14 * d - 7
    · obtain ⟨uv, c0, _, _, hc01, hc02, _⟩ :=
        split_with_T0 d (2 * d) (3 * d - 1) s hd (by omega) (by omega) (by omega)
      exact ⟨1, uv - 1, c0, ad_1 d, ad_of_Istar (by omega) (by omega),
        by omega, by omega, hc01, hc02, by omega⟩
    · by_cases hc3 : s ≤ 15 * d - 9
      · obtain ⟨uv, c0, _, _, hc01, hc02, _⟩ :=
          split_with_T0 d (3 * d - 2) (4 * d - 3) s hd (by omega) (by omega) (by omega)
        exact ⟨d - 1, uv - (d - 1), c0, ad_dm1 d, ad_of_Istar (by omega) (by omega),
          by omega, by omega, hc01, hc02, by omega⟩
      · by_cases hc4 : s ≤ 17 * d - 11
        · obtain ⟨uv, c0, _, _, hc01, hc02, _⟩ :=
            split_with_T0 d (4 * d - 1) (6 * d - 5) s hd (by omega) (by omega) (by omega)
          obtain ⟨a, b, ha, hab, hb, _⟩ :=
            pair_sum_interval (2 * d - 1) (3 * d - 2) uv (by omega) (by omega) (by omega)
          exact ⟨a, b, c0, ad_of_Istar ha (by omega), ad_of_Istar (by omega) hb,
            hab, by omega, hc01, hc02, by omega⟩
        · obtain ⟨uv, c0, _, _, hc01, hc02, _⟩ :=
            split_with_T0 d (6 * d - 2) (7 * d - 3) s hd (by omega) (by omega) (by omega)
          exact ⟨uv - (4 * d - 1), 4 * d - 1, c0, ad_of_Istar (by omega) (by omega),
            ad_4dm1 d, by omega, Nat.le_refl _, hc01, hc02, by omega⟩

/-- Part B (Inclusion): every gap `n > 2d - 1` outside `Ad d` is a strict 3-sum in `Ad d`. -/
theorem ad_incl (d : Nat) (hd : d ≥ 6) (n : Nat) (hn : n > 2 * d - 1) (hnA : ¬ Ad d n) :
    ∃ a b c, Ad d a ∧ Ad d b ∧ Ad d c ∧ a < b ∧ b < c ∧ a + b + c = n := by
  have hm : 8 * d - 3 > 0 := by omega
  have hrlt : n % (8 * d - 3) < 8 * d - 3 := Nat.mod_lt n hm
  have hneq : n = n % (8 * d - 3) + (8 * d - 3) * (n / (8 * d - 3)) :=
    (Nat.mod_add_div n (8 * d - 3)).symm
  have hnot_qr :
      ¬ (2 * d - 2 ≤ n % (8 * d - 3) ∧ n % (8 * d - 3) ≤ 3 * d - 3 ∧ n / (8 * d - 3) ≥ 1) := by
    rintro ⟨h1, h2, h3⟩
    apply hnA
    rw [ad_iff_qr d n hd]
    exact Or.inr (Or.inr (Or.inl ⟨h1, by omega, fun _ => h3, fun _ => by omega⟩))
  cases hq : n / (8 * d - 3) with
  | zero =>
    rw [hq, Nat.mul_zero, Nat.add_zero] at hneq
    exact ad_cover_pre d n hd (by omega) (by omega) hnA
  | succ q1 =>
    cases q1 with
    | zero =>
      rw [hq, Nat.mul_one] at hneq
      by_cases hr_low : n % (8 * d - 3) < 2 * d - 2
      · exact ad_cover_pre d n hd (by omega) (by omega) hnA
      · have hr_high : n % (8 * d - 3) > 3 * d - 3 := by omega
        obtain ⟨a, b, c0, hAa, hAb, hab, _, hc01, hc02, hsum⟩ :=
          ad_cover_per0 d n hd (by omega) (by omega)
        have hAc0 : Ad d c0 := by simpa using ad_of_Tj d c0 0 hd hc01 hc02
        exact ⟨a, b, c0, hAa, hAb, hAc0, hab, by omega, hsum⟩
    | succ j =>
      rw [hq] at hneq
      by_cases hr_low : n % (8 * d - 3) < 2 * d - 2
      · let s := n % (8 * d - 3) + 2 * (8 * d - 3)
        have hs_eq : n = s + (8 * d - 3) * j := by
          have hmul : (8 * d - 3) * (j + 1 + 1) = (8 * d - 3) * j + 2 * (8 * d - 3) := by
            rw [Nat.mul_succ (8 * d - 3) (j + 1), Nat.mul_succ (8 * d - 3) j]
            omega
          omega
        obtain ⟨a, b, c0, hAa, hAb, hab, _, hc01, hc02, hsum⟩ :=
          ad_cover_per0 d s hd (by omega) (by omega)
        exact ⟨a, b, c0 + (8 * d - 3) * j, hAa, hAb, ad_of_Tj d c0 j hd hc01 hc02,
          hab, by omega, by omega⟩
      · have hr_high : n % (8 * d - 3) > 3 * d - 3 := by omega
        let s := n % (8 * d - 3) + (8 * d - 3)
        have hs_eq : n = s + (8 * d - 3) * (j + 1) := by
          have hmul : (8 * d - 3) * (j + 1 + 1) = (8 * d - 3) * (j + 1) + (8 * d - 3) :=
            Nat.mul_succ (8 * d - 3) (j + 1)
          omega
        obtain ⟨a, b, c0, hAa, hAb, hab, _, hc01, hc02, hsum⟩ :=
          ad_cover_per0 d s hd (by omega) (by omega)
        exact ⟨a, b, c0 + (8 * d - 3) * (j + 1), hAa, hAb, ad_of_Tj d c0 (j + 1) hd hc01 hc02,
          hab, by omega, by omega⟩

theorem inSeq_iff_ad (d : Nat) (hd : d ≥ 6) (x : Nat) : InSeq d x ↔ Ad d x :=
  inSeq_iff_of_characterization d (by omega) (Ad d)
    (fun z hz => ad_seed d z hd hz)
    (ad_excl d hd)
    (ad_incl d hd)
    x

/-- Explicit 0-indexed enumeration `fd d` of `Ad d` for `d >= 6`. -/
def fd (d i : Nat) : Nat :=
  if i = 0 then 1
  else if i = 1 then d - 1
  else if i ≤ d + 1 then (2 * d - 1) + (i - 2)
  else if i = d + 2 then 4 * d - 1
  else
    (10 * d - 5) + ((i - (d + 3)) % d) + (8 * d - 3) * ((i - (d + 3)) / d)

theorem fd_zero (d : Nat) : fd d 0 = 1 := by
  unfold fd; rfl

theorem fd_one (d : Nat) : fd d 1 = d - 1 := by
  unfold fd; rfl

theorem fd_mid (d i : Nat) (h1 : 2 ≤ i) (h2 : i ≤ d + 1) :
    fd d i = (2 * d - 1) + (i - 2) := by
  unfold fd
  split; · omega
  split
  · omega
  · rfl

theorem fd_d2 (d : Nat) (_hd : d ≥ 6) : fd d (d + 2) = 4 * d - 1 := by
  unfold fd
  split; · omega
  split; · omega
  split; · omega
  split
  · rfl
  · omega

theorem fd_tail (d i : Nat) (_hd : d ≥ 6) (hi : d + 3 ≤ i) :
    fd d i = (10 * d - 5) + ((i - (d + 3)) % d) + (8 * d - 3) * ((i - (d + 3)) / d) := by
  unfold fd
  split; · omega
  split; · omega
  split; · omega
  split
  · omega
  · rfl

theorem succ_div_mod (u d : Nat) (hd : d > 0) :
    ((u % d + 1 < d ∧ (u + 1) % d = u % d + 1 ∧ (u + 1) / d = u / d) ∨
     (u % d + 1 = d ∧ (u + 1) % d = 0 ∧ (u + 1) / d = u / d + 1)) := by
  have hrlt : u % d < d := Nat.mod_lt u hd
  have hueq : u = u % d + d * (u / d) := (Nat.mod_add_div u d).symm
  by_cases h : u % d + 1 < d
  · left
    have hrew : u + 1 = (u % d + 1) + d * (u / d) := by omega
    obtain ⟨hmod, hdiv⟩ := add_mul_div_mod (u % d + 1) (u / d) d h
    rw [← hrew] at hmod hdiv
    exact ⟨h, hmod, hdiv⟩
  · right
    have heq : u % d + 1 = d := by omega
    have hrew : u + 1 = 0 + d * (u / d + 1) := by rw [Nat.mul_succ]; omega
    obtain ⟨hmod, hdiv⟩ := add_mul_div_mod 0 (u / d + 1) d hd
    rw [← hrew] at hmod hdiv
    exact ⟨heq, hmod, hdiv⟩

theorem fd_step_lt (d : Nat) (hd : d ≥ 6) (i : Nat) : fd d i < fd d (i + 1) := by
  by_cases h0 : i = 0
  · subst h0; rw [fd_zero, fd_one]; omega
  · by_cases h1 : i = 1
    · subst h1; rw [fd_one, fd_mid d 2 (by omega) (by omega)]; omega
    · by_cases h2 : i ≤ d
      · rw [fd_mid d i (by omega) (by omega), fd_mid d (i + 1) (by omega) (by omega)]; omega
      · by_cases h3 : i = d + 1
        · subst h3
          have heq : d + 1 + 1 = d + 2 := by omega
          rw [fd_mid d (d + 1) (by omega) (by omega), heq, fd_d2 d hd]; omega
        · by_cases h4 : i = d + 2
          · subst h4
            have heq : d + 2 + 1 = d + 3 := by omega
            rw [fd_d2 d hd, heq, fd_tail d (d + 3) hd (by omega)]
            simp only [Nat.sub_self, Nat.zero_mod, Nat.zero_div, Nat.mul_zero, Nat.add_zero]
            omega
          · rw [fd_tail d i hd (by omega), fd_tail d (i + 1) hd (by omega)]
            have hu1 : (i + 1) - (d + 3) = (i - (d + 3)) + 1 := by omega
            rw [hu1]
            rcases succ_div_mod (i - (d + 3)) d (by omega) with ⟨_, hm1, hd1⟩ | ⟨_, hm1, hd1⟩
            · rw [hm1, hd1]; omega
            · rw [hm1, hd1, Nat.mul_succ]; omega

theorem fd_mem_ad (d : Nat) (hd : d ≥ 6) (i : Nat) : Ad d (fd d i) := by
  by_cases h0 : i = 0
  · subst h0; rw [fd_zero]; exact ad_1 d
  · by_cases h1 : i = 1
    · subst h1; rw [fd_one]; exact ad_dm1 d
    · by_cases h2 : i ≤ d + 1
      · rw [fd_mid d i (by omega) h2]
        exact ad_of_Istar (by omega) (by omega)
      · by_cases h3 : i = d + 2
        · subst h3; rw [fd_d2 d hd]; exact ad_4dm1 d
        · rw [fd_tail d i hd (by omega)]
          have hult : (i - (d + 3)) % d < d := Nat.mod_lt _ (by omega)
          exact ad_of_Tj d ((10 * d - 5) + ((i - (d + 3)) % d)) ((i - (d + 3)) / d) hd
            (by omega) (by omega)

theorem fd_below0 (d : Nat) (_hd : d ≥ 6) (x : Nat) (hx : x < fd d 0) : ¬ Ad d x := by
  rw [fd_zero] at hx
  have hx0 : x = 0 := by omega
  subst hx0
  unfold Ad
  omega

theorem not_adQR_of_gt {d r q : Nat} (_hd : d ≥ 6) (hq : q ≥ 1) (hr : r > 3 * d - 3) :
    ¬ AdQR d r q := by
  unfold AdQR
  omega

theorem not_adQR_of_lt {d r q : Nat} (_hd : d ≥ 6) (hq : q ≥ 2) (hr : r < 2 * d - 2) :
    ¬ AdQR d r q := by
  unfold AdQR
  omega

theorem fd_gap (d : Nat) (hd : d ≥ 6) (i x : Nat)
    (hx1 : fd d i < x) (hx2 : x < fd d (i + 1)) : ¬ Ad d x := by
  by_cases h0 : i = 0
  · subst h0
    rw [fd_zero] at hx1; rw [fd_one] at hx2
    unfold Ad; omega
  · by_cases h1 : i = 1
    · subst h1
      rw [fd_one] at hx1; rw [fd_mid d 2 (by omega) (by omega)] at hx2
      unfold Ad; omega
    · by_cases h2 : i ≤ d
      · rw [fd_mid d i (by omega) (by omega)] at hx1
        rw [fd_mid d (i + 1) (by omega) (by omega)] at hx2
        omega
      · by_cases h3 : i = d + 1
        · subst h3
          have heq : d + 1 + 1 = d + 2 := by omega
          rw [fd_mid d (d + 1) (by omega) (by omega)] at hx1
          rw [heq, fd_d2 d hd] at hx2
          unfold Ad; omega
        · by_cases h4 : i = d + 2
          · subst h4
            have heq : d + 2 + 1 = d + 3 := by omega
            rw [fd_d2 d hd] at hx1
            rw [heq, fd_tail d (d + 3) hd (by omega)] at hx2
            simp only [Nat.sub_self, Nat.zero_mod, Nat.zero_div, Nat.mul_zero,
              Nat.add_zero] at hx2
            unfold Ad; omega
          · rw [fd_tail d i hd (by omega)] at hx1
            rw [fd_tail d (i + 1) hd (by omega)] at hx2
            have hu1 : (i + 1) - (d + 3) = (i - (d + 3)) + 1 := by omega
            rw [hu1] at hx2
            rcases succ_div_mod (i - (d + 3)) d (by omega) with ⟨_, hm1, hd1⟩ | ⟨heq, hm1, hd1⟩
            · rw [hm1, hd1] at hx2; omega
            · rw [hm1, hd1, Nat.mul_succ] at hx2
              intro hAx
              by_cases hcarry : x < 2 * (8 * d - 3) + (8 * d - 3) * ((i - (d + 3)) / d)
              · let r := x - (8 * d - 3) * ((i - (d + 3)) / d) - (8 * d - 3)
                have hr_gt : r > 3 * d - 3 := by omega
                have hr_lt : r < 8 * d - 3 := by omega
                have hx_rew : x = r + (8 * d - 3) * ((i - (d + 3)) / d + 1) := by
                  rw [Nat.mul_succ]; omega
                obtain ⟨hmod, hdiv⟩ := add_mul_div_mod r
                  ((i - (d + 3)) / d + 1) (8 * d - 3) hr_lt
                rw [← hx_rew] at hmod hdiv
                have hqr := (ad_iff_of_div_mod hd hmod hdiv).mp hAx
                exact not_adQR_of_gt hd (Nat.le_add_left 1 _) hr_gt hqr
              · let r := x - (8 * d - 3) * ((i - (d + 3)) / d) - 2 * (8 * d - 3)
                have hr_lt2 : r < 2 * d - 2 := by omega
                have hr_ltm : r < 8 * d - 3 := by omega
                have hx_rew : x = r + (8 * d - 3) * ((i - (d + 3)) / d + 2) := by
                  have hmul : (8 * d - 3) * ((i - (d + 3)) / d + 2) =
                      (8 * d - 3) * ((i - (d + 3)) / d) + 2 * (8 * d - 3) := by
                    rw [Nat.mul_succ, Nat.mul_succ]; omega
                  omega
                obtain ⟨hmod, hdiv⟩ := add_mul_div_mod r
                  ((i - (d + 3)) / d + 2) (8 * d - 3) hr_ltm
                rw [← hx_rew] at hmod hdiv
                have hqr := (ad_iff_of_div_mod hd hmod hdiv).mp hAx
                exact not_adQR_of_lt hd (Nat.le_add_left 2 _) hr_lt2 hqr

theorem fd_eq_seq (d : Nat) (hd : d ≥ 6) : fd d = seq d := by
  funext i
  refine eq_of_strictMono_same_range (fd_step_lt d hd) (seq_step_lt d) ?_ i
  intro x
  rw [range_iff_of_step_gaps (fd_step_lt d hd) (fd_mem_ad d hd) (fd_below0 d hd) (fd_gap d hd) x,
      seq_range_eq_inSeq d x, inSeq_iff_ad d hd x]

theorem fd_periodic (d : Nat) (hd : d ≥ 6) (i : Nat) (hi : i ≥ d + 3) :
    fd d (i + d) = fd d i + (8 * d - 3) := by
  rw [fd_tail d i hd hi, fd_tail d (i + d) hd (by omega)]
  have hud : (i + d) - (d + 3) = (i - (d + 3)) + d := by omega
  rw [hud, Nat.add_mod_right, Nat.add_div_right _ (by omega), Nat.mul_succ]
  omega

theorem fd_tail_eval (d : Nat) (hd : d ≥ 6) (q r : Nat) (hr : r < d) :
    fd d ((d + 3) + (r + d * q)) = (10 * d - 5) + r + (8 * d - 3) * q := by
  rw [fd_tail d ((d + 3) + (r + d * q)) hd (by omega)]
  have hu : ((d + 3) + (r + d * q)) - (d + 3) = r + d * q := by omega
  obtain ⟨hmod, hdiv⟩ := add_mul_div_mod r q d hr
  rw [hu, hmod, hdiv]

end Internal

/-! ## Main Theorems: Complete Resolution and Disproof of Conjecture 4 -/

/-- Case `d = 3`: `S_{1,2,5}` has minimal periodicity `(k, p, m) = (5, 1, 5)`. -/
theorem d3_minimal : IsMinimalPeriodicity (seq 3) 5 1 5 :=
  Internal.smallCert_sound 3 5 1 5 20
    Internal.iso3 Internal.progs3 Internal.tags3 Internal.pre3 Internal.blk3
    Internal.fg3 Internal.rc3
    rfl rfl rfl rfl rfl rfl rfl rfl rfl

set_option maxRecDepth 100000 in
/-- Case `d = 4`: `S_{1,3,7}` has minimal periodicity `(k, p, m) = (7, 3, 27)`,
    refuting Conjecture 4 (`p = 3 != 4` and `m = 27 != 31`). -/
theorem d4_minimal : IsMinimalPeriodicity (seq 4) 7 3 27 :=
  Internal.smallCert_sound 4 7 3 27 61
    Internal.iso4 Internal.progs4 Internal.tags4 Internal.pre4 Internal.blk4
    Internal.fg4 Internal.rc4
    rfl rfl rfl rfl rfl rfl rfl rfl rfl

private theorem d5_c1 : Internal.tags5 = Internal.makeTags 104 Internal.iso5 Internal.progs5 := rfl

set_option maxRecDepth 100000 in
private theorem d5_c2 :
    Internal.checkParams 5 13 10 104 221 Internal.pre5 Internal.blk5 Internal.fg5 Internal.rc5 = true := rfl
private theorem d5_c3 : Internal.checkProgsWf 104 221 Internal.progs5 = true := rfl
private theorem d5_c4 : Internal.checkSeed 5 104 Internal.iso5 Internal.progs5 = true := rfl

set_option maxRecDepth 200000 in
private theorem d5_c5a :
    (Internal.tags5.take 8).all (fun t1 =>
      Internal.tags5.all (fun t2 =>
        Internal.tags5.all (fun t3 =>
          Internal.checkTagTriple 104 Internal.tags5 t1 t2 t3))) = true := rfl

set_option maxRecDepth 200000 in
private theorem d5_c5b :
    (Internal.tags5.drop 8).all (fun t1 =>
      Internal.tags5.all (fun t2 =>
        Internal.tags5.all (fun t3 =>
          Internal.checkTagTriple 104 Internal.tags5 t1 t2 t3))) = true := rfl

private theorem d5_c5 : Internal.checkAllTags 104 Internal.tags5 = true := by
  unfold Internal.checkAllTags
  rw [← List.take_append_drop 8 Internal.tags5, List.all_append, Bool.and_eq_true]
  exact ⟨d5_c5a, d5_c5b⟩

set_option maxRecDepth 200000 in
private theorem d5_c6 :
    Internal.checkFg 5 104 Internal.iso5 Internal.progs5 Internal.fg5 = true := rfl

set_option maxRecDepth 200000 in
private theorem d5_c7 :
    Internal.checkRc 104 221 Internal.iso5 Internal.progs5 Internal.rc5 = true := rfl

private theorem d5_c8 :
    Internal.checkTail 104 (Internal.blk5.getD 0 0) Internal.iso5 Internal.progs5 = true := rfl

set_option maxRecDepth 200000 in
private theorem d5_c9 :
    Internal.checkEnum 13 10 104 Internal.pre5 Internal.blk5 Internal.iso5 Internal.progs5 = true := rfl

/-- Case `d = 5`: `S_{1,4,9}` has minimal periodicity `(k, p, m) = (13, 10, 104)`. -/
theorem d5_minimal : IsMinimalPeriodicity (seq 5) 13 10 104 :=
  Internal.smallCert_sound 5 13 10 104 221
    Internal.iso5 Internal.progs5 Internal.tags5 Internal.pre5 Internal.blk5
    Internal.fg5 Internal.rc5
    d5_c1 d5_c2 d5_c3 d5_c4 d5_c5 d5_c6 d5_c7 d5_c8 d5_c9

/-- General Theorem (`d >= 6`): For every integer `d >= 6`, `S_{1, d-1, 2d-1}` has minimal
    preperiod `k = d + 3`, minimal period `p = d`, and minimal modulus `m = 8d - 3`
    (refuting Conjecture 4's modulus `8d - 1` for every `d >= 6`). -/
theorem all_d_ge_6_minimal (d : Nat) (hd : d ≥ 6) :
    IsMinimalPeriodicity (seq d) (d + 3) d (8 * d - 3) := by
  rw [← Internal.fd_eq_seq d hd]
  refine Internal.minimal_periodicity_of_unique_gap
    (Internal.fd_step_lt d hd) (by omega) (Internal.fd_periodic d hd) ?_ ?_
  · refine ⟨d - 1, by omega, ?_⟩
    intro s hs1 hs2
    have h0 : Internal.fd d ((d + 3) + (d - 1)) = 11 * d - 6 := by
      have h := Internal.fd_tail_eval d hd 0 (d - 1) (by omega)
      simp only [Nat.mul_zero, Nat.add_zero] at h
      omega
    have h1 : Internal.fd d ((d + 3) + (d - 1) + 1) = 18 * d - 8 := by
      have heq : (d + 3) + (d - 1) + 1 = (d + 3) + (0 + d * 1) := by omega
      rw [heq, Internal.fd_tail_eval d hd 1 0 (by omega)]
      omega
    have hs_lo :
        Internal.fd d ((d + 3) + (d - 1) + s) = (10 * d - 5) + (s - 1) + (8 * d - 3) := by
      have heq : (d + 3) + (d - 1) + s = (d + 3) + ((s - 1) + d * 1) := by omega
      rw [heq, Internal.fd_tail_eval d hd 1 (s - 1) (by omega)]
      omega
    have hs_hi :
        Internal.fd d ((d + 3) + (d - 1) + s + 1) = (10 * d - 5) + s + (8 * d - 3) := by
      have heq : (d + 3) + (d - 1) + s + 1 = (d + 3) + (s + d * 1) := by omega
      rw [heq, Internal.fd_tail_eval d hd 1 s (by omega)]
      omega
    omega
  · refine ⟨by omega, ?_⟩
    have hpre1 : Internal.fd d (((d + 3) - 1) + d) = 11 * d - 6 := by
      have heq : ((d + 3) - 1) + d = (d + 3) + ((d - 1) + d * 0) := by omega
      rw [heq, Internal.fd_tail_eval d hd 0 (d - 1) (by omega)]
      omega
    have hpre2 : Internal.fd d ((d + 3) - 1) = 4 * d - 1 := by
      have heq : (d + 3) - 1 = d + 2 := by omega
      rw [heq, Internal.fd_d2 d hd]
    omega

/-! ## Mission-Section Aliases and Explicit Disproof Corollaries -/

theorem d3_minimal_periodicity : IsMinimalPeriodicity (seq 3) 5 1 5 := d3_minimal
theorem d4_minimal_periodicity : IsMinimalPeriodicity (seq 4) 7 3 27 := d4_minimal
theorem d5_minimal_periodicity : IsMinimalPeriodicity (seq 5) 13 10 104 := d5_minimal

theorem all_d_ge_6_minimal_periodicity (d : Nat) (hd : d ≥ 6) :
    IsMinimalPeriodicity (seq d) (d + 3) d (8 * d - 3) :=
  all_d_ge_6_minimal d hd

/-- Explicit disproof of Conjecture 4 at `d = 4`: minimal `(k, p, m) = (7, 3, 27)` has
    `3 != 4` and `27 != 31`, so `(7, 4, 31)` is not minimal and not a valid period/modulus. -/
theorem d4_refutes_conj4 :
    (3 ≠ 4 ∧ 27 ≠ 31) ∧
    (∀ k' m', ¬ IsMinimalPeriodicity (seq 4) k' 4 m') ∧
    (∀ k' p', ¬ IsMinimalPeriodicity (seq 4) k' p' 31) ∧
    (∀ k', ¬ HasPeriodMod (seq 4) k' 4 31) := by
  refine ⟨⟨by omega, by omega⟩, ?_, ?_, ?_⟩
  · intro k' m' h
    have := unique_minimal_periodicity d4_minimal h
    omega
  · intro k' p' h
    have := unique_minimal_periodicity d4_minimal h
    omega
  · intro k' ⟨_, hper⟩
    let i := 7 + 3 * k'
    have hp3 := d4_minimal.1.2
    have a1 := hp3 i (by omega)
    have a2 := hp3 (i + 3) (by omega)
    have a3 := hp3 (i + 6) (by omega)
    have a4 := hp3 (i + 9) (by omega)
    have b1 := hper i (by omega)
    have b2 := hper (i + 4) (by omega)
    have b3 := hper (i + 8) (by omega)
    have heq1 : i + 3 + 3 = i + 6 := by omega
    have heq2 : i + 6 + 3 = i + 9 := by omega
    have heq3 : i + 9 + 3 = i + 12 := by omega
    have heq4 : i + 4 + 4 = i + 8 := by omega
    have heq5 : i + 8 + 4 = i + 12 := by omega
    rw [heq1] at a2; rw [heq2] at a3; rw [heq3] at a4
    rw [heq4] at b2; rw [heq5] at b3
    omega

/-- Explicit disproof of Conjecture 4 for every `d >= 6`: `8d - 3 != 8d - 1`, and no preperiod
    can give period `d` with modulus `8d - 1`. -/
theorem all_d_ge_6_refutes_conj4 (d : Nat) (hd : d ≥ 6) :
    8 * d - 3 ≠ 8 * d - 1 ∧
    (∀ k' p', ¬ IsMinimalPeriodicity (seq d) k' p' (8 * d - 1)) ∧
    (∀ k', ¬ HasPeriodMod (seq d) k' d (8 * d - 1)) := by
  have hmin := all_d_ge_6_minimal d hd
  refine ⟨by omega, ?_, ?_⟩
  · intro k' p' h
    have := unique_minimal_periodicity hmin h
    omega
  · intro k' ⟨_, hper⟩
    let i := max (d + 3) k'
    have h1 := hmin.1.2 i (by omega)
    have h2 := hper i (by omega)
    omega

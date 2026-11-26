/-
  Sumfree2Conj59.lean
  Standalone Lean 4 (v4.36.0, zero Mathlib) formalization of the disproofs of
  Conjectures 5 and 9 of Daan van Berkel and Wieb Bosma,
  "Periodicity conjectures for all 2-sumfree sequences" (arXiv:2609.18522v1).

  All proofs are verified in Lean's kernel using standard axioms only
  (propext, Classical.choice, Quot.sound; zero sorry, zero axiom, zero native_decide, zero ofReduceBool).
-/

private theorem ite_pos {α : Sort u} {c : Prop} [inst : Decidable c] {t e : α} (hc : c) :
    (if c then t else e) = t :=
  match inst with
  | isTrue _ => rfl
  | isFalse h => absurd hc h

private theorem ite_neg {α : Sort u} {c : Prop} [inst : Decidable c] {t e : α} (hnc : ¬ c) :
    (if c then t else e) = e :=
  match inst with
  | isTrue h => absurd h hnc
  | isFalse _ => rfl

/-! ## 1. First-Principles Definitions of Strict Greedy 2-Sum Sequences -/

/-- `IsStrict2Sum P x` holds when `x` is the sum of two distinct elements `a < b` satisfying `P`. -/
def IsStrict2Sum (P : Nat → Prop) (x : Nat) : Prop :=
  ∃ a b, P a ∧ P b ∧ a < b ∧ a + b = x

/-- Membership predicate `InSeq f g` for the strict greedy 2-sum sequence `S_{f,g}`:
    - For `x ≤ g`, the members are the seed elements `f` and `g`.
    - For `x > g`, `x` belongs to `InSeq f g` iff `x` cannot be written as `a + b`
      with `a < b < x` already in `InSeq f g`. -/
def InSeq (f g x : Nat) : Prop :=
  if x ≤ g then
    x = f ∨ x = g
  else
    ¬ IsStrict2Sum (fun y => ∃ (_ : y < x), InSeq f g y) x
termination_by x

theorem inSeq_le {f g x : Nat} (hx : x ≤ g) :
    InSeq f g x ↔ x = f ∨ x = g := by
  conv => lhs; unfold InSeq
  rw [ite_pos hx]

theorem inSeq_f {f g : Nat} (hfg : f < g) : InSeq f g f := by
  have hle : f ≤ g := Nat.le_of_lt hfg
  exact (inSeq_le hle).2 (Or.inl rfl)

theorem inSeq_g (f g : Nat) : InSeq f g g :=
  (inSeq_le (Nat.le_refl g)).2 (Or.inr rfl)

theorem inSeq_gt {f g x : Nat} (hx : g < x) :
    InSeq f g x ↔ ¬ IsStrict2Sum (fun y => y < x ∧ InSeq f g y) x := by
  conv => lhs; unfold InSeq
  have hnot : ¬ x ≤ g := by omega
  rw [ite_neg hnot]
  constructor
  · intro h ⟨a, b, ⟨ha1, ha2⟩, ⟨hb1, hb2⟩, hab, hsum⟩
    exact h ⟨a, b, ⟨ha1, ha2⟩, ⟨hb1, hb2⟩, hab, hsum⟩
  · intro h ⟨a, b, ⟨ha1, ha2⟩, ⟨hb1, hb2⟩, hab, hsum⟩
    exact h ⟨a, b, ⟨ha1, ha2⟩, ⟨hb1, hb2⟩, hab, hsum⟩

/-! ## 2. Constructive Strictly Increasing Sequence `seq f g` and Equivalence with `InSeq` -/

def listAnyB (p : Nat → Bool) : List Nat → Bool
  | [] => false
  | y :: ys => if p y = true then true else listAnyB p ys

theorem listAnyB_iff {p : Nat → Bool} {L : List Nat} :
    listAnyB p L = true ↔ ∃ y ∈ L, p y = true := by
  induction L with
  | nil =>
    simp [listAnyB]
  | cons y ys ih =>
    simp only [listAnyB, List.mem_cons]
    split
    · next hy =>
      exact ⟨fun _ => ⟨y, Or.inl rfl, hy⟩, fun _ => rfl⟩
    · next hy =>
      constructor
      · intro h
        obtain ⟨z, hz, hpz⟩ := ih.1 h
        exact ⟨z, Or.inr hz, hpz⟩
      · intro ⟨z, hz, hpz⟩
        cases hz with
        | inl heq =>
          rw [heq] at hpz
          exact False.elim (hy hpz)
        | inr hmem =>
          exact ih.2 ⟨z, hmem, hpz⟩

def hasList2Sum (L : List Nat) (x : Nat) : Bool :=
  listAnyB (fun a => listAnyB (fun b => if a < b ∧ a + b = x then true else false) L) L

theorem hasList2Sum_iff {L : List Nat} {x : Nat} :
    hasList2Sum L x = true ↔ ∃ a ∈ L, ∃ b ∈ L, a < b ∧ a + b = x := by
  unfold hasList2Sum
  rw [listAnyB_iff]
  constructor
  · intro ⟨a, ha, hb_any⟩
    rw [listAnyB_iff] at hb_any
    obtain ⟨b, hb, hcond⟩ := hb_any
    split at hcond
    · next h => exact ⟨a, ha, b, hb, h⟩
    · contradiction
  · intro ⟨a, ha, b, hb, h⟩
    refine ⟨a, ha, ?_⟩
    rw [listAnyB_iff]
    refine ⟨b, hb, ?_⟩
    rw [ite_pos h]

def findNext (L : List Nat) (start fuel : Nat) : Nat :=
  match fuel with
  | 0 => start
  | fuel' + 1 =>
    if hasList2Sum L start = true then
      findNext L (start + 1) fuel'
    else
      start

theorem findNext_ge (L : List Nat) (start fuel : Nat) :
    start ≤ findNext L start fuel := by
  induction fuel generalizing start with
  | zero => exact Nat.le_refl start
  | succ fuel' ih =>
    unfold findNext
    split
    · exact Nat.le_trans (Nat.le_succ start) (ih (start + 1))
    · exact Nat.le_refl start

theorem findNext_spec {L : List Nat} {start fuel : Nat}
    (h_end : ¬ hasList2Sum L (start + fuel) = true) :
    ¬ hasList2Sum L (findNext L start fuel) = true ∧
      ∀ z, start ≤ z → z < findNext L start fuel → hasList2Sum L z = true := by
  induction fuel generalizing start with
  | zero =>
    have h0 : start + 0 = start := Nat.add_zero start
    rw [h0] at h_end
    refine ⟨h_end, ?_⟩
    intro z _ hz2
    unfold findNext at hz2
    omega
  | succ fuel' ih =>
    unfold findNext
    split
    · next hstart =>
      have h_end' : ¬ hasList2Sum L ((start + 1) + fuel') = true := by
        have heq : (start + 1) + fuel' = start + (fuel' + 1) := by omega
        rw [heq]
        exact h_end
      obtain ⟨h1, h2⟩ := ih h_end'
      refine ⟨h1, ?_⟩
      intro z hz1 hz2
      by_cases heq : z = start
      · rw [heq]; exact hstart
      · exact h2 z (by omega) hz2
    · next hstart =>
      refine ⟨hstart, ?_⟩
      intro z hz1 hz2
      omega

/-- Prefix state `(terms_so_far, last_term)` of the constructive greedy 2-sum sequence. -/
def seqState (f g : Nat) : Nat → List Nat × Nat
  | 0 => ([f], f)
  | 1 => ([f, g], g)
  | m + 2 =>
    ( (seqState f g (m + 1)).1 ++
        [findNext (seqState f g (m + 1)).1 ((seqState f g (m + 1)).2 + 1) ((seqState f g (m + 1)).2 + 1)],
      findNext (seqState f g (m + 1)).1 ((seqState f g (m + 1)).2 + 1) ((seqState f g (m + 1)).2 + 1) )

/-- Constructive 0-based strict greedy 2-sum sequence `seq f g`:
    `seq f g 0 = f`, `seq f g 1 = g`, and each subsequent term is the least integer
    exceeding the previous term that is not a strict 2-sum of earlier terms. -/
def seq (f g n : Nat) : Nat :=
  (seqState f g n).2

theorem seq_zero (f g : Nat) : seq f g 0 = f := rfl
theorem seq_one (f g : Nat) : seq f g 1 = g := rfl

theorem seqState_inv {f g : Nat} (hfg : f < g) :
    ∀ m : Nat,
      g ≤ (seqState f g (m + 1)).2 ∧
      InSeq f g (seqState f g (m + 1)).2 ∧
      (∀ y, y ∈ (seqState f g (m + 1)).1 ↔ y ≤ (seqState f g (m + 1)).2 ∧ InSeq f g y) := by
  intro m
  induction m with
  | zero =>
    refine ⟨Nat.le_refl g, inSeq_g f g, ?_⟩
    intro y
    simp only [seqState, List.mem_cons, List.not_mem_nil, or_false]
    constructor
    · intro hy
      cases hy with
      | inl h => rw [h]; exact ⟨Nat.le_of_lt hfg, inSeq_f hfg⟩
      | inr h => rw [h]; exact ⟨Nat.le_refl g, inSeq_g f g⟩
    · intro ⟨hle, hin⟩
      exact (inSeq_le hle).1 hin
  | succ m' ih =>
    obtain ⟨hg_le, _, hmem⟩ := ih
    have h_no_end : ¬ hasList2Sum (seqState f g (m' + 1)).1
        (((seqState f g (m' + 1)).2 + 1) + ((seqState f g (m' + 1)).2 + 1)) = true := by
      intro hsum
      obtain ⟨a, ha, b, hb, hab, heq⟩ := hasList2Sum_iff.1 hsum
      have ha_le : a ≤ (seqState f g (m' + 1)).2 := (hmem a).1 ha |>.1
      have hb_le : b ≤ (seqState f g (m' + 1)).2 := (hmem b).1 hb |>.1
      omega
    have h_ge : (seqState f g (m' + 1)).2 + 1 ≤
        findNext (seqState f g (m' + 1)).1 ((seqState f g (m' + 1)).2 + 1) ((seqState f g (m' + 1)).2 + 1) :=
      findNext_ge _ _ _
    obtain ⟨h_next_nosum, h_between_sum⟩ := findNext_spec h_no_end
    have h_not_in_between : ∀ z, (seqState f g (m' + 1)).2 < z →
        z < findNext (seqState f g (m' + 1)).1 ((seqState f g (m' + 1)).2 + 1) ((seqState f g (m' + 1)).2 + 1) →
        ¬ InSeq f g z := by
      intro z hz1 hz2 hinz
      have hsumz : hasList2Sum (seqState f g (m' + 1)).1 z = true := h_between_sum z (by omega) hz2
      obtain ⟨a, ha, b, hb, hab, heq⟩ := hasList2Sum_iff.1 hsumz
      obtain ⟨ha_le, ha_in⟩ := (hmem a).1 ha
      obtain ⟨hb_le, hb_in⟩ := (hmem b).1 hb
      have hgz : g < z := by omega
      have hnot := (inSeq_gt hgz).1 hinz
      exact hnot ⟨a, b, ⟨by omega, ha_in⟩, ⟨by omega, hb_in⟩, hab, heq⟩
    have h_in_next : InSeq f g
        (findNext (seqState f g (m' + 1)).1 ((seqState f g (m' + 1)).2 + 1) ((seqState f g (m' + 1)).2 + 1)) := by
      have hg_next : g <
          findNext (seqState f g (m' + 1)).1 ((seqState f g (m' + 1)).2 + 1) ((seqState f g (m' + 1)).2 + 1) := by
        omega
      rw [inSeq_gt hg_next]
      intro ⟨a, b, ⟨ha_lt, ha_in⟩, ⟨hb_lt, hb_in⟩, hab, heq⟩
      have ha_le : a ≤ (seqState f g (m' + 1)).2 := by
        by_cases hle_a : a ≤ (seqState f g (m' + 1)).2
        · exact hle_a
        · exact False.elim (h_not_in_between a (by omega) ha_lt ha_in)
      have hb_le : b ≤ (seqState f g (m' + 1)).2 := by
        by_cases hle_b : b ≤ (seqState f g (m' + 1)).2
        · exact hle_b
        · exact False.elim (h_not_in_between b (by omega) hb_lt hb_in)
      have ha_mem : a ∈ (seqState f g (m' + 1)).1 := (hmem a).2 ⟨ha_le, ha_in⟩
      have hb_mem : b ∈ (seqState f g (m' + 1)).1 := (hmem b).2 ⟨hb_le, hb_in⟩
      exact h_next_nosum (hasList2Sum_iff.2 ⟨a, ha_mem, b, hb_mem, hab, heq⟩)
    simp only [seqState]
    refine ⟨by omega, h_in_next, ?_⟩
    intro y
    rw [List.mem_append, List.mem_singleton]
    constructor
    · intro hy
      cases hy with
      | inl h_in_s =>
        obtain ⟨hy_le, hy_in⟩ := (hmem y).1 h_in_s
        exact ⟨by omega, hy_in⟩
      | inr h_eq =>
        rw [h_eq]
        exact ⟨Nat.le_refl _, h_in_next⟩
    · intro ⟨hy_le, hy_in⟩
      by_cases heq : y =
          findNext (seqState f g (m' + 1)).1 ((seqState f g (m' + 1)).2 + 1) ((seqState f g (m' + 1)).2 + 1)
      · exact Or.inr heq
      · have hy_lt : y <
            findNext (seqState f g (m' + 1)).1 ((seqState f g (m' + 1)).2 + 1) ((seqState f g (m' + 1)).2 + 1) := by
          omega
        have hy_le_s : y ≤ (seqState f g (m' + 1)).2 := by
          by_cases hle_y : y ≤ (seqState f g (m' + 1)).2
          · exact hle_y
          · exact False.elim (h_not_in_between y (by omega) hy_lt hy_in)
        exact Or.inl ((hmem y).2 ⟨hy_le_s, hy_in⟩)

theorem seq_lt_succ {f g : Nat} (hfg : f < g) (n : Nat) :
    seq f g n < seq f g (n + 1) := by
  cases n with
  | zero => exact hfg
  | succ m =>
    unfold seq
    simp only [seqState]
    have h := findNext_ge (seqState f g (m + 1)).1 ((seqState f g (m + 1)).2 + 1) ((seqState f g (m + 1)).2 + 1)
    omega

theorem seq_strictMono {f g : Nat} (hfg : f < g) {i j : Nat} (hij : i < j) :
    seq f g i < seq f g j := by
  induction j with
  | zero => omega
  | succ j' ih =>
    by_cases heq : i = j'
    · rw [heq]; exact seq_lt_succ hfg j'
    · exact Nat.lt_trans (ih (by omega)) (seq_lt_succ hfg j')

theorem seq_mono {f g : Nat} (hfg : f < g) {i j : Nat} (hij : i ≤ j) :
    seq f g i ≤ seq f g j := by
  by_cases heq : i = j
  · rw [heq]; exact Nat.le_refl _
  · exact Nat.le_of_lt (seq_strictMono hfg (by omega))

theorem inSeq_seq {f g : Nat} (hfg : f < g) (n : Nat) :
    InSeq f g (seq f g n) := by
  cases n with
  | zero => exact inSeq_f hfg
  | succ m => exact (seqState_inv hfg m).2.1

theorem not_inSeq_between {f g : Nat} (hfg : f < g) (n z : Nat)
    (h1 : seq f g n < z) (h2 : z < seq f g (n + 1)) :
    ¬ InSeq f g z := by
  cases n with
  | zero =>
    intro hin
    change f < z at h1
    change z < g at h2
    have hle : z ≤ g := by omega
    have hor := (inSeq_le hle).1 hin
    omega
  | succ m =>
    intro hin
    have inv := (seqState_inv hfg (m + 1)).2.2 z
    change (seqState f g (m + 1)).2 < z at h1
    change z < (seqState f g (m + 2)).2 at h2
    have hmem : z ∈ (seqState f g (m + 2)).1 := inv.2 ⟨Nat.le_of_lt h2, hin⟩
    have hmem' : z ∈ (seqState f g (m + 1)).1 ++ [(seqState f g (m + 2)).2] := hmem
    rw [List.mem_append, List.mem_singleton] at hmem'
    cases hmem' with
    | inl hprev =>
      have hle_prev := ((seqState_inv hfg m).2.2 z).1 hprev |>.1
      omega
    | inr heq =>
      omega

theorem not_inSeq_lt_f {f g z : Nat} (hfg : f < g) (hz : z < f) :
    ¬ InSeq f g z := by
  intro hin
  have hle : z ≤ g := by omega
  have hor := (inSeq_le hle).1 hin
  omega

theorem id_le_seq {f g : Nat} (hfg : f < g) (n : Nat) :
    n ≤ seq f g n := by
  induction n with
  | zero => exact Nat.zero_le _
  | succ n' ih =>
    have hlt := seq_lt_succ hfg n'
    omega

theorem exists_seq_of_inSeq_le {f g : Nat} (hfg : f < g) :
    ∀ k x : Nat, InSeq f g x → x ≤ seq f g k → ∃ n, n ≤ k ∧ seq f g n = x := by
  intro k
  induction k with
  | zero =>
    intro x hin hx
    change x ≤ f at hx
    have hge : f ≤ x := by
      by_cases hle : f ≤ x
      · exact hle
      · exact False.elim (not_inSeq_lt_f hfg (by omega) hin)
    exact ⟨0, Nat.le_refl 0, by change f = x; omega⟩
  | succ k' ih =>
    intro x hin hx
    by_cases heq : x = seq f g (k' + 1)
    · exact ⟨k' + 1, Nat.le_refl _, heq.symm⟩
    · have hlt : x < seq f g (k' + 1) := by omega
      have hle : x ≤ seq f g k' := by
        by_cases hle_k : x ≤ seq f g k'
        · exact hle_k
        · exact False.elim (not_inSeq_between hfg k' x (by omega) hlt hin)
      obtain ⟨n, hn, hseq⟩ := ih x hin hle
      exact ⟨n, by omega, hseq⟩

/-- Exact equivalence between `InSeq f g` and the range of `seq f g` for `f < g`. -/
theorem inSeq_iff_exists_seq {f g : Nat} (hfg : f < g) (x : Nat) :
    InSeq f g x ↔ ∃ n, seq f g n = x := by
  constructor
  · intro hin
    have hle : x ≤ seq f g x := id_le_seq hfg x
    obtain ⟨n, _, hn⟩ := exists_seq_of_inSeq_le hfg x x hin hle
    exact ⟨n, hn⟩
  · intro ⟨n, hn⟩
    rw [← hn]
    exact inSeq_seq hfg n

/-- Operational greedy step characterization of `seq f g`: for every `n ≥ 1`,
    `seq f g (n + 1)` is the least integer `> seq f g n` not expressible as a
    strict 2-sum of `{seq f g 0, ..., seq f g n}`. -/
theorem seq_greedy_step {f g : Nat} (hfg : f < g) {n : Nat} (hn : 1 ≤ n) :
    seq f g n < seq f g (n + 1) ∧
    ¬ IsStrict2Sum (fun y => ∃ i, i ≤ n ∧ seq f g i = y) (seq f g (n + 1)) ∧
    ∀ z, seq f g n < z → z < seq f g (n + 1) →
      IsStrict2Sum (fun y => ∃ i, i ≤ n ∧ seq f g i = y) z := by
  have hlt := seq_lt_succ hfg n
  have hg_le : g ≤ seq f g n := by
    have h1 := seq_mono hfg hn
    simpa [seq_one] using h1
  refine ⟨hlt, ?_, ?_⟩
  · intro ⟨a, b, ⟨i, hi, hai⟩, ⟨j, hj, hbj⟩, hab, hsum⟩
    rw [← hai] at hab hsum
    rw [← hbj] at hab hsum
    have hin_next := inSeq_seq hfg (n + 1)
    have hnot := (inSeq_gt (by omega)).1 hin_next
    have ha_le : seq f g i ≤ seq f g n := seq_mono hfg hi
    have hb_le : seq f g j ≤ seq f g n := seq_mono hfg hj
    exact hnot ⟨seq f g i, seq f g j,
      ⟨by omega, inSeq_seq hfg i⟩, ⟨by omega, inSeq_seq hfg j⟩, hab, hsum⟩
  · intro z hz1 hz2
    cases n with
    | zero => omega
    | succ m =>
      have inv_m := seqState_inv hfg m
      have h_no_end : ¬ hasList2Sum (seqState f g (m + 1)).1
          (((seqState f g (m + 1)).2 + 1) + ((seqState f g (m + 1)).2 + 1)) = true := by
        intro hsum
        obtain ⟨a, ha, b, hb, hab, heq⟩ := hasList2Sum_iff.1 hsum
        have ha_le : a ≤ (seqState f g (m + 1)).2 := (inv_m.2.2 a).1 ha |>.1
        have hb_le : b ≤ (seqState f g (m + 1)).2 := (inv_m.2.2 b).1 hb |>.1
        omega
      obtain ⟨_, h_between⟩ := findNext_spec h_no_end
      change (seqState f g (m + 1)).2 < z at hz1
      change z < findNext (seqState f g (m + 1)).1 ((seqState f g (m + 1)).2 + 1) ((seqState f g (m + 1)).2 + 1) at hz2
      have hsumz := h_between z (by omega) hz2
      obtain ⟨a, ha, b, hb, hab, heq⟩ := hasList2Sum_iff.1 hsumz
      obtain ⟨ha_le, ha_in⟩ := (inv_m.2.2 a).1 ha
      obtain ⟨hb_le, hb_in⟩ := (inv_m.2.2 b).1 hb
      obtain ⟨i, hi, hai⟩ := exists_seq_of_inSeq_le hfg (m + 1) a ha_in ha_le
      obtain ⟨j, hj, hbj⟩ := exists_seq_of_inSeq_le hfg (m + 1) b hb_in hb_le
      exact ⟨a, b, ⟨i, hi, hai⟩, ⟨j, hj, hbj⟩, hab, heq⟩

/-! ## 3. Uniqueness of Strictly Increasing Enumerations -/

theorem strictMono_eq_of_range_eq {s₁ s₂ : Nat → Nat}
    (h₁ : ∀ i j, i < j → s₁ i < s₁ j)
    (h₂ : ∀ i j, i < j → s₂ i < s₂ j)
    (hr : ∀ x, (∃ n, s₁ n = x) ↔ (∃ n, s₂ n = x)) :
    ∀ n, s₁ n = s₂ n := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    by_cases heq : s₁ n = s₂ n
    · exact heq
    · by_cases hlt : s₁ n < s₂ n
      · obtain ⟨j, hj⟩ := (hr (s₁ n)).1 ⟨n, rfl⟩
        by_cases hjn : j < n
        · have heqj := ih j hjn
          have hlt1 := h₁ j n hjn
          omega
        · by_cases hjeq : j = n
          · rw [hjeq] at hj; omega
          · have hlt2 := h₂ n j (by omega)
            omega
      · have hgt : s₂ n < s₁ n := by omega
        obtain ⟨j, hj⟩ := (hr (s₂ n)).2 ⟨n, rfl⟩
        by_cases hjn : j < n
        · have heqj := ih j hjn
          have hlt2 := h₂ j n hjn
          omega
        · by_cases hjeq : j = n
          · rw [hjeq] at hj; omega
          · have hlt1 := h₁ n j (by omega)
            omega

/-! ## 4. Exact Ultimate Periodicity and Minimality Definitions -/

/-- Exact ultimate periodicity of a 0-indexed sequence `s`:
    `0 < p`, `0 < m`, and `s (n + p) = s n + m` for every `n ≥ k`. -/
def HasPeriodMod (s : Nat → Nat) (k p m : Nat) : Prop :=
  0 < p ∧ 0 < m ∧ ∀ n, k ≤ n → s (n + p) = s n + m

/-- Exact minimal ultimate periodicity of `s` with parameters `(k, p, m)`:
    1. `HasPeriodMod s k p m` holds,
    2. `p` is the minimum period across all valid triples `(k', p', m')`,
    3. `k` is the minimum preperiod for period `p` across all `(k', m')`. -/
def IsMinimalPeriodicity (s : Nat → Nat) (k p m : Nat) : Prop :=
  HasPeriodMod s k p m ∧
  (∀ k' p' m', HasPeriodMod s k' p' m' → p ≤ p') ∧
  (∀ k' m', HasPeriodMod s k' p m' → k ≤ k')

/-- Minimal periodicity parameters `(k, p, m)` are uniquely determined by `s`. -/
theorem IsMinimalPeriodicity.unique {s : Nat → Nat} {k₁ p₁ m₁ k₂ p₂ m₂ : Nat}
    (h₁ : IsMinimalPeriodicity s k₁ p₁ m₁)
    (h₂ : IsMinimalPeriodicity s k₂ p₂ m₂) :
    k₁ = k₂ ∧ p₁ = p₂ ∧ m₁ = m₂ := by
  have hp12 : p₁ ≤ p₂ := h₁.2.1 k₂ p₂ m₂ h₂.1
  have hp21 : p₂ ≤ p₁ := h₂.2.1 k₁ p₁ m₁ h₁.1
  have hp : p₁ = p₂ := by omega
  subst hp
  have hk12 : k₁ ≤ k₂ := h₁.2.2 k₂ m₂ h₂.1
  have hk21 : k₂ ≤ k₁ := h₂.2.2 k₁ m₁ h₁.1
  have hk : k₁ = k₂ := by omega
  subst hk
  have eq1 := h₁.1.2.2 k₁ (Nat.le_refl k₁)
  have eq2 := h₂.1.2.2 k₁ (Nat.le_refl k₁)
  exact ⟨rfl, rfl, by omega⟩

theorem HasPeriodMod.add_mul {s : Nat → Nat} {k p m : Nat}
    (h : HasPeriodMod s k p m) {n : Nat} (hn : k ≤ n) (q : Nat) :
    s (n + p * q) = s n + m * q := by
  induction q with
  | zero => simp
  | succ q' ih =>
    have heq1 : n + p * (q' + 1) = (n + p * q') + p := by
      rw [Nat.mul_succ, Nat.add_assoc]
    rw [heq1, h.2.2 (n + p * q') (by omega), ih, Nat.mul_succ, Nat.add_assoc]

theorem HasPeriodMod.diff_add_mul {s : Nat → Nat} {k p m : Nat}
    (h : HasPeriodMod s k p m) {n : Nat} (hn : k ≤ n) (q : Nat) :
    s (n + 1 + p * q) - s (n + p * q) = s (n + 1) - s n := by
  have h1 := h.add_mul (by omega : k ≤ n + 1) q
  have h2 := h.add_mul hn q
  rw [h1, h2]
  exact Nat.add_sub_add_right (s (n + 1)) (m * q) (s n)

/-! ## 5. Periodic Mask Cutoff Lemma (Strong Induction on `x`) -/

def anyRange (p : Nat → Bool) (lo : Nat) : Nat → Bool
  | 0 => false
  | k + 1 => if p lo = true then true else anyRange p (lo + 1) k

def allRange (p : Nat → Bool) (lo : Nat) : Nat → Bool
  | 0 => true
  | k + 1 => if p lo = true then allRange p (lo + 1) k else false

theorem anyRange_iff {p : Nat → Bool} {lo k : Nat} :
    anyRange p lo k = true ↔ ∃ x, lo ≤ x ∧ x < lo + k ∧ p x = true := by
  induction k generalizing lo with
  | zero =>
    simp only [anyRange, Nat.add_zero]
    exact ⟨fun h => by contradiction, fun ⟨_, h1, h2, _⟩ => by omega⟩
  | succ k' ih =>
    unfold anyRange
    split
    · next hlo =>
      exact ⟨fun _ => ⟨lo, Nat.le_refl lo, by omega, hlo⟩, fun _ => rfl⟩
    · next hlo =>
      rw [ih]
      constructor
      · intro ⟨x, hx1, hx2, hpx⟩
        exact ⟨x, by omega, by omega, hpx⟩
      · intro ⟨x, hx1, hx2, hpx⟩
        by_cases heq : x = lo
        · rw [heq] at hpx; exact False.elim (hlo hpx)
        · exact ⟨x, by omega, by omega, hpx⟩

theorem allRange_iff {p : Nat → Bool} {lo k : Nat} :
    allRange p lo k = true ↔ ∀ x, lo ≤ x → x < lo + k → p x = true := by
  induction k generalizing lo with
  | zero =>
    simp only [allRange, Nat.add_zero]
    exact ⟨fun _ _ h1 h2 => by omega, fun _ => trivial⟩
  | succ k' ih =>
    unfold allRange
    split
    · next hlo =>
      rw [ih]
      constructor
      · intro hall x hx1 hx2
        by_cases heq : x = lo
        · rw [heq]; exact hlo
        · exact hall x (by omega) (by omega)
      · intro hall x hx1 hx2
        exact hall x (by omega) (by omega)
    · next hlo =>
      constructor
      · intro h; contradiction
      · intro hall
        exact False.elim (hlo (hall lo (Nat.le_refl lo) (by omega)))

def has2SumB (M : Nat → Bool) (x : Nat) : Bool :=
  anyRange (fun a => Nat.ble (a + 1) (x - a) && M a && M (x - a)) 1 (x / 2)

theorem has2SumB_iff {M : Nat → Bool} (hM0 : M 0 = false) (x : Nat) :
    has2SumB M x = true ↔ IsStrict2Sum (fun y => y < x ∧ M y = true) x := by
  unfold has2SumB
  rw [anyRange_iff]
  constructor
  · intro ⟨a, ha1, ha2, hcond⟩
    simp only [Bool.and_eq_true, Nat.ble_eq] at hcond
    obtain ⟨⟨hab, hMa⟩, hMb⟩ := hcond
    refine ⟨a, x - a, ⟨by omega, hMa⟩, ⟨by omega, hMb⟩, by omega, by omega⟩
  · intro ⟨a, b, ⟨_, hMa⟩, ⟨_, hMb⟩, hab, hsum⟩
    have ha_pos : 1 ≤ a := by
      by_cases ha0 : a = 0
      · rw [ha0, hM0] at hMa; contradiction
      · omega
    refine ⟨a, ha_pos, by omega, ?_⟩
    simp only [Bool.and_eq_true, Nat.ble_eq]
    have hb_eq : x - a = b := by omega
    rw [hb_eq]
    exact ⟨⟨by omega, hMa⟩, hMb⟩

def stepOk (f g : Nat) (M : Nat → Bool) (x : Nat) : Bool :=
  if Nat.ble x g then
    Bool.beq (M x) (Nat.beq x f || Nat.beq x g)
  else
    Bool.beq (M x) (!has2SumB M x)

/-- Core shift invariance lemma for strict 2-sums:
    Once a candidate mask `M` (with `M 0 = false`) is periodic with modulus `m ≥ 1`
    starting at `T ≥ 1`, strict 2-sum representability is invariant under `+ m`
    for every `x₀ ≥ 2 * T + 2 * m`. -/
theorem strict2Sum_shift_iff {M : Nat → Bool} {T m x₀ : Nat}
    (hM0 : M 0 = false)
    (hT : 1 ≤ T)
    (hm : 1 ≤ m)
    (hper : ∀ z, T ≤ z → M (z + m) = M z)
    (hx : 2 * T + 2 * m ≤ x₀) :
    IsStrict2Sum (fun y => y < x₀ + m ∧ M y = true) (x₀ + m) ↔
      IsStrict2Sum (fun y => y < x₀ ∧ M y = true) x₀ := by
  constructor
  · intro ⟨a', b', ⟨_, hMa'⟩, ⟨_, hMb'⟩, hab', hsum'⟩
    have ha'_pos : 1 ≤ a' := by
      by_cases h0 : a' = 0
      · rw [h0, hM0] at hMa'; contradiction
      · omega
    have hb'_gt : T + m < b' := by omega
    have hb_add : (b' - m) + m = b' := by omega
    have hb_ge_T : T ≤ b' - m := by omega
    have hMb : M (b' - m) = true := by
      have hp := hper (b' - m) hb_ge_T
      rw [hb_add] at hp
      rw [← hp]
      exact hMb'
    have hsum : a' + (b' - m) = x₀ := by omega
    by_cases hlt : a' < b' - m
    · exact ⟨a', b' - m, ⟨by omega, hMa'⟩, ⟨by omega, hMb⟩, hlt, hsum⟩
    · by_cases hgt : b' - m < a'
      · exact ⟨b' - m, a', ⟨by omega, hMb⟩, ⟨by omega, hMa'⟩, hgt, by omega⟩
      · have heq : a' = b' - m := by omega
        have ha'_ge : T + m ≤ a' := by omega
        have hu_add : (a' - m) + m = a' := by omega
        have hu_ge_T : T ≤ a' - m := by omega
        have hMu : M (a' - m) = true := by
          have hp := hper (a' - m) hu_ge_T
          rw [hu_add] at hp
          rw [← hp]
          exact hMa'
        have hMv : M (a' + m) = true := by
          have hp := hper a' (by omega)
          rw [hp]
          exact hMa'
        exact ⟨a' - m, a' + m, ⟨by omega, hMu⟩, ⟨by omega, hMv⟩, by omega, by omega⟩
  · intro ⟨a, b, ⟨_, hMa⟩, ⟨_, hMb⟩, hab, hsum⟩
    have ha_pos : 1 ≤ a := by
      by_cases h0 : a = 0
      · rw [h0, hM0] at hMa; contradiction
      · omega
    have hb_ge_T : T ≤ b := by omega
    have hMbm : M (b + m) = true := by
      rw [hper b hb_ge_T]
      exact hMb
    exact ⟨a, b + m, ⟨by omega, hMa⟩, ⟨by omega, hMbm⟩, by omega, by omega⟩

/-- Exact characterization theorem via finite cutoff and strong induction on `x`:
    if `M` is periodic mod `m` from `T` and passes `stepOk f g M x` for all
    `x < 2 * T + 3 * m`, then `InSeq f g x ↔ M x = true` holds for ALL `x : Nat`. -/
theorem periodic_mask_characterization {f g T m : Nat} {M : Nat → Bool}
    (hf : 1 ≤ f)
    (hfg : f < g)
    (hT : 1 ≤ T)
    (hm : 1 ≤ m)
    (hg_bound : g < 2 * T + 2 * m)
    (hper : ∀ z, T ≤ z → M (z + m) = M z)
    (hwin : ∀ x, x < 2 * T + 3 * m → stepOk f g M x = true) :
    ∀ x, InSeq f g x ↔ M x = true := by
  have hM0 : M 0 = false := by
    have h0 := hwin 0 (by omega)
    unfold stepOk at h0
    have hble0 : Nat.ble 0 g = true := Eq.mpr Nat.ble_eq (Nat.zero_le g)
    rw [hble0] at h0
    have hbeq_f : Nat.beq 0 f = false := by
      cases h : Nat.beq 0 f
      · rfl
      · have heq := Eq.mp Nat.beq_eq h; omega
    have hbeq_g : Nat.beq 0 g = false := by
      cases h : Nat.beq 0 g
      · rfl
      · have heq := Eq.mp Nat.beq_eq h; omega
    rw [hbeq_f, hbeq_g] at h0
    cases hM : M 0 <;> rw [hM] at h0 <;> simp [Bool.beq] at h0 ⊢
  have hstep_all : ∀ x, g < x →
      (M x = true ↔ ¬ IsStrict2Sum (fun y => y < x ∧ M y = true) x) := by
    intro x
    induction x using Nat.strongRecOn with
    | ind x ih =>
      intro hgx
      by_cases hlt : x < 2 * T + 3 * m
      · have hok := hwin x hlt
        unfold stepOk at hok
        have hble : Nat.ble x g = false := by
          cases h : Nat.ble x g
          · rfl
          · have hle := Eq.mp Nat.ble_eq h; omega
        rw [hble] at hok
        rw [← has2SumB_iff hM0 x]
        cases hMx : M x <;> cases h2 : has2SumB M x <;>
          rw [hMx, h2] at hok <;> simp [Bool.beq] at hok ⊢
      · have hx_eq : x = (x - m) + m := by omega
        have hx0_bound : 2 * T + 2 * m ≤ x - m := by omega
        have hx0_lt : x - m < x := by omega
        have hgx0 : g < x - m := by omega
        have hMx : M x = M (x - m) := by
          conv => lhs; rw [hx_eq]
          exact hper (x - m) (by omega)
        rw [hMx, ih (x - m) hx0_lt hgx0]
        conv => rhs; rw [hx_eq]
        have hshift := strict2Sum_shift_iff hM0 hT hm hper hx0_bound
        exact ⟨fun h h1 => h (hshift.1 h1), fun h h2 => h (hshift.2 h2)⟩
  intro x
  induction x using Nat.strongRecOn with
  | ind x ih =>
    by_cases hle : x ≤ g
    · rw [inSeq_le hle]
      have hok := hwin x (by omega)
      unfold stepOk at hok
      have hble : Nat.ble x g = true := Eq.mpr Nat.ble_eq hle
      rw [hble] at hok
      have hor_iff : (Nat.beq x f || Nat.beq x g) = true ↔ (x = f ∨ x = g) := by
        rw [Bool.or_eq_true, Nat.beq_eq, Nat.beq_eq]
      cases hMx : M x <;> cases hor : (Nat.beq x f || Nat.beq x g) <;>
        rw [hMx, hor] at hok <;> simp [Bool.beq] at hok
      · exact ⟨fun h => False.elim (hor_iff.2 h |>.symm.trans hor |> Bool.noConfusion), fun h => by contradiction⟩
      · exact ⟨fun _ => rfl, fun _ => hor_iff.1 hor⟩
    · have hgx : g < x := by omega
      rw [inSeq_gt hgx, hstep_all x hgx]
      constructor
      · intro h ⟨a, b, ⟨ha1, ha2⟩, ⟨hb1, hb2⟩, hab, hsum⟩
        exact h ⟨a, b, ⟨ha1, (ih a ha1).2 ha2⟩, ⟨hb1, (ih b hb1).2 hb2⟩, hab, hsum⟩
      · intro h ⟨a, b, ⟨ha1, ha2⟩, ⟨hb1, hb2⟩, hab, hsum⟩
        exact h ⟨a, b, ⟨ha1, (ih a ha1).1 ha2⟩, ⟨hb1, (ih b hb1).1 hb2⟩, hab, hsum⟩

/-! ## 6. Reusable Candidate Sequence, Periodic Mask, and Minimality Engine -/

def listGetD : List Nat → Nat → Nat
  | [], _ => 0
  | x :: _, 0 => x
  | _ :: xs, i + 1 => listGetD xs i

def memB (x : Nat) : List Nat → Bool
  | [] => false
  | y :: ys => Nat.beq x y || memB x ys

def listAllB (p : Nat → Bool) : List Nat → Bool
  | [] => true
  | y :: ys => if p y = true then listAllB p ys else false

def isStrictChain : List Nat → Bool
  | [] => true
  | [_] => true
  | a :: b :: rest => if a < b then isStrictChain (b :: rest) else false

theorem memB_iff_exists_get {x : Nat} {L : List Nat} :
    memB x L = true ↔ ∃ i, i < L.length ∧ listGetD L i = x := by
  induction L with
  | nil =>
    simp [memB]
  | cons y ys ih =>
    simp only [memB, Bool.or_eq_true, Nat.beq_eq, List.length_cons]
    constructor
    · intro h
      cases h with
      | inl hxy => exact ⟨0, by omega, hxy.symm⟩
      | inr hmem =>
        obtain ⟨i, hi, hget⟩ := ih.1 hmem
        exact ⟨i + 1, by omega, hget⟩
    · intro ⟨i, hi, hget⟩
      cases i with
      | zero => exact Or.inl hget.symm
      | succ j => exact Or.inr (ih.2 ⟨j, by omega, hget⟩)

theorem listAllB_get {p : Nat → Bool} {L : List Nat} (hall : listAllB p L = true) :
    ∀ i, i < L.length → p (listGetD L i) = true := by
  induction L with
  | nil => intro _ hi; simp at hi
  | cons y ys ih =>
    unfold listAllB at hall
    split at hall
    · next hpy =>
      intro i hi
      cases i with
      | zero => exact hpy
      | succ j =>
        simp only [List.length_cons] at hi
        exact ih hall j (by omega)
    · contradiction

theorem isStrictChain_adj {L : List Nat} (hc : isStrictChain L = true) :
    ∀ i, i + 1 < L.length → listGetD L i < listGetD L (i + 1) := by
  induction L with
  | nil => intro _ hi; simp at hi
  | cons a rest ih =>
    cases rest with
    | nil => intro _ hi; simp at hi
    | cons b tail =>
      unfold isStrictChain at hc
      split at hc
      · next hab =>
        intro i hi
        cases i with
        | zero => exact hab
        | succ j =>
          simp only [List.length_cons] at hi
          exact ih hc j (by simp only [List.length_cons]; omega)
      · contradiction

/-- Closed-form candidate sequence determined by preperiod `pre`, first period block `per`,
    and modulus `m`. -/
def candSeq (pre per : List Nat) (m n : Nat) : Nat :=
  if n < pre.length then
    listGetD pre n
  else
    listGetD per ((n - pre.length) % per.length) + m * ((n - pre.length) / per.length)

/-- Closed-form boolean membership mask corresponding to `candSeq pre per m`. -/
def candMask (pre per : List Nat) (m x : Nat) : Bool :=
  if Nat.ble (x + 1) (listGetD per 0) then
    memB x pre
  else
    memB (listGetD per 0 + (x - listGetD per 0) % m) per

def validCandParams (f g : Nat) (pre per : List Nat) (m : Nat) : Bool :=
  if 1 ≤ f ∧ f < g ∧ 0 < per.length ∧ 0 < m ∧ 1 ≤ listGetD per 0 ∧
     g < 2 * listGetD per 0 + 2 * m then
    isStrictChain pre &&
    listAllB (fun y => if y < listGetD per 0 then true else false) pre &&
    isStrictChain per &&
    listAllB (fun y => if listGetD per 0 ≤ y ∧ y < listGetD per 0 + m then true else false) per
  else
    false

theorem candMask_periodic (pre per : List Nat) {m : Nat} (hm : 0 < m) :
    ∀ z, listGetD per 0 ≤ z → candMask pre per m (z + m) = candMask pre per m z := by
  intro z hz
  unfold candMask
  have hb1 : Nat.ble (z + m + 1) (listGetD per 0) = false := by
    cases h : Nat.ble (z + m + 1) (listGetD per 0)
    · rfl
    · have hle := Eq.mp Nat.ble_eq h; omega
  have hb2 : Nat.ble (z + 1) (listGetD per 0) = false := by
    cases h : Nat.ble (z + 1) (listGetD per 0)
    · rfl
    · have hle := Eq.mp Nat.ble_eq h; omega
  rw [hb1, hb2]
  simp only [Bool.false_eq_true, ↓reduceIte]
  have hsub : z + m - listGetD per 0 = (z - listGetD per 0) + m := by omega
  rw [hsub, Nat.add_mod_right]

theorem candSeq_lt_succ {pre per : List Nat} {m : Nat}
    (hp : 0 < per.length)
    (hc_pre : isStrictChain pre = true)
    (hb_pre : listAllB (fun y => if y < listGetD per 0 then true else false) pre = true)
    (hc_per : isStrictChain per = true)
    (hb_per : listAllB (fun y => if listGetD per 0 ≤ y ∧ y < listGetD per 0 + m then true else false) per = true) :
    ∀ n, candSeq pre per m n < candSeq pre per m (n + 1) := by
  intro n
  unfold candSeq
  by_cases hn1 : n + 1 < pre.length
  · have hn0 : n < pre.length := by omega
    rw [ite_pos hn0, ite_pos hn1]
    exact isStrictChain_adj hc_pre n hn1
  · by_cases hn0 : n < pre.length
    · rw [ite_pos hn0, ite_neg hn1]
      have h_eq : n + 1 - pre.length = 0 := by omega
      rw [h_eq, Nat.zero_mod, Nat.zero_div, Nat.mul_zero, Nat.add_zero]
      have hget := listAllB_get hb_pre n hn0
      split at hget
      · assumption
      · contradiction
    · rw [ite_neg hn0, ite_neg hn1]
      have hidx1 : n + 1 - pre.length = (n - pre.length) + 1 := by omega
      rw [hidx1]
      have hrem_lt : (n - pre.length) % per.length < per.length := Nat.mod_lt _ hp
      have hdiv_eq : per.length * ((n - pre.length) / per.length) + (n - pre.length) % per.length =
          n - pre.length := Nat.div_add_mod _ _
      by_cases hwrap : (n - pre.length) % per.length + 1 < per.length
      · have heq_idx : (n - pre.length) + 1 =
            ((n - pre.length) % per.length + 1) + per.length * ((n - pre.length) / per.length) := by
          omega
        have hmod_next : ((n - pre.length) + 1) % per.length = (n - pre.length) % per.length + 1 := by
          rw [heq_idx, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hwrap]
        have hdiv_next : ((n - pre.length) + 1) / per.length = (n - pre.length) / per.length := by
          rw [heq_idx, Nat.add_mul_div_left _ _ hp, Nat.div_eq_of_lt hwrap, Nat.zero_add]
        rw [hmod_next, hdiv_next]
        have hlt_per := isStrictChain_adj hc_per ((n - pre.length) % per.length) hwrap
        omega
      · have heq_idx : (n - pre.length) + 1 =
            0 + per.length * ((n - pre.length) / per.length + 1) := by
          rw [Nat.mul_succ]
          omega
        have hmod_next : ((n - pre.length) + 1) % per.length = 0 := by
          rw [heq_idx, Nat.add_mul_mod_self_left, Nat.zero_mod]
        have hdiv_next : ((n - pre.length) + 1) / per.length = (n - pre.length) / per.length + 1 := by
          rw [heq_idx, Nat.add_mul_div_left _ _ hp, Nat.zero_div, Nat.zero_add]
        rw [hmod_next, hdiv_next, Nat.mul_succ]
        have hget := listAllB_get hb_per ((n - pre.length) % per.length) hrem_lt
        split at hget
        · next hb => omega
        · contradiction

theorem candSeq_strictMono {pre per : List Nat} {m : Nat}
    (hstep : ∀ n, candSeq pre per m n < candSeq pre per m (n + 1)) :
    ∀ i j, i < j → candSeq pre per m i < candSeq pre per m j := by
  intro i j hij
  induction j with
  | zero => omega
  | succ j' ih =>
    by_cases heq : i = j'
    · rw [heq]; exact hstep j'
    · exact Nat.lt_trans (ih (by omega)) (hstep j')

theorem candMask_iff_exists_candSeq {pre per : List Nat} {m : Nat}
    (hp : 0 < per.length)
    (hb_pre : listAllB (fun y => if y < listGetD per 0 then true else false) pre = true)
    (hb_per : listAllB (fun y => if listGetD per 0 ≤ y ∧ y < listGetD per 0 + m then true else false) per = true) :
    ∀ x, candMask pre per m x = true ↔ ∃ n, candSeq pre per m n = x := by
  intro x
  unfold candMask
  by_cases hxT : x < listGetD per 0
  · have hble : Nat.ble (x + 1) (listGetD per 0) = true := Eq.mpr Nat.ble_eq (by omega)
    rw [hble]
    simp only [↓reduceIte, memB_iff_exists_get]
    constructor
    · intro ⟨i, hi, hget⟩
      refine ⟨i, ?_⟩
      unfold candSeq
      rw [ite_pos hi]
      exact hget
    · intro ⟨n, hn⟩
      by_cases hnk : n < pre.length
      · unfold candSeq at hn
        rw [ite_pos hnk] at hn
        exact ⟨n, hnk, hn⟩
      · unfold candSeq at hn
        rw [ite_neg hnk] at hn
        have hrem : (n - pre.length) % per.length < per.length := Nat.mod_lt _ hp
        have hget := listAllB_get hb_per ((n - pre.length) % per.length) hrem
        split at hget
        · next hb => omega
        · contradiction
  · have hble : Nat.ble (x + 1) (listGetD per 0) = false := by
      cases h : Nat.ble (x + 1) (listGetD per 0)
      · rfl
      · have hle := Eq.mp Nat.ble_eq h; omega
    rw [hble]
    simp only [Bool.false_eq_true, ↓reduceIte, memB_iff_exists_get]
    constructor
    · intro ⟨i, hi, hget⟩
      have hdiv_x : m * ((x - listGetD per 0) / m) + (x - listGetD per 0) % m =
          x - listGetD per 0 := Nat.div_add_mod _ _
      refine ⟨pre.length + (i + per.length * ((x - listGetD per 0) / m)), ?_⟩
      unfold candSeq
      have hnot_lt : ¬ pre.length + (i + per.length * ((x - listGetD per 0) / m)) < pre.length := by
        omega
      rw [ite_neg hnot_lt]
      have hsub : pre.length + (i + per.length * ((x - listGetD per 0) / m)) - pre.length =
          i + per.length * ((x - listGetD per 0) / m) := by
        omega
      rw [hsub]
      have hmod : (i + per.length * ((x - listGetD per 0) / m)) % per.length = i := by
        rw [Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hi]
      have hdiv : (i + per.length * ((x - listGetD per 0) / m)) / per.length =
          (x - listGetD per 0) / m := by
        rw [Nat.add_mul_div_left _ _ hp, Nat.div_eq_of_lt hi, Nat.zero_add]
      rw [hmod, hdiv, hget]
      omega
    · intro ⟨n, hn⟩
      by_cases hnk : n < pre.length
      · unfold candSeq at hn
        rw [ite_pos hnk] at hn
        have hget := listAllB_get hb_pre n hnk
        split at hget
        · next hb => omega
        · contradiction
      · unfold candSeq at hn
        rw [ite_neg hnk] at hn
        have hi : (n - pre.length) % per.length < per.length := Nat.mod_lt _ hp
        have hget := listAllB_get hb_per ((n - pre.length) % per.length) hi
        split at hget
        · next hb =>
          have hr'_lt : listGetD per ((n - pre.length) % per.length) - listGetD per 0 < m := by
            omega
          have hx_sub : x - listGetD per 0 =
              (listGetD per ((n - pre.length) % per.length) - listGetD per 0) +
                m * ((n - pre.length) / per.length) := by
            omega
          have hmod_r : (x - listGetD per 0) % m =
              listGetD per ((n - pre.length) % per.length) - listGetD per 0 := by
            rw [hx_sub, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hr'_lt]
          refine ⟨(n - pre.length) % per.length, hi, ?_⟩
          rw [hmod_r]
          omega
        · contradiction

theorem candSeq_hasPeriodMod {pre per : List Nat} {m : Nat}
    (hp : 0 < per.length) (hm : 0 < m) :
    HasPeriodMod (candSeq pre per m) pre.length per.length m := by
  refine ⟨hp, hm, ?_⟩
  intro n hn
  unfold candSeq
  have hnot1 : ¬ n + per.length < pre.length := by omega
  have hnot2 : ¬ n < pre.length := by omega
  rw [ite_neg hnot1, ite_neg hnot2]
  have hsub : n + per.length - pre.length = (n - pre.length) + per.length := by omega
  rw [hsub, Nat.add_mod_right, Nat.add_div_right _ hp, Nat.mul_succ]
  omega

/-- Decidable check that the repeating gap word of length `p` starting at `k` is primitive. -/
def checkPrimitiveGaps (s : Nat → Nat) (k p : Nat) : Bool :=
  allRange (fun d =>
    anyRange (fun r =>
      if s (k + r + d + 1) - s (k + r + d) ≠ s (k + r + 1) - s (k + r) then true else false) 0 p) 1 (p - 1)

/-- Decidable check that `k` is sharp (either `k = 0` or periodicity fails at `k - 1`). -/
def checkSharpPreperiod (s : Nat → Nat) (k p m : Nat) : Bool :=
  if k = 0 then
    true
  else
    if s (k - 1 + p) ≠ s (k - 1) + m ∧
       s (k + p) - s (k - 1 + p) ≠ s k - s (k - 1) then
      true
    else
      false

/-- General global minimality theorem: any sequence satisfying `HasPeriodMod s k p m`
    with primitive gap word and sharp preperiod satisfies `IsMinimalPeriodicity s k p m`,
    and moreover every valid `(k', p', m')` satisfies `p ∣ p'` and `k ≤ k'`. -/
theorem minimal_of_primitive_and_sharp {s : Nat → Nat} {k p m : Nat}
    (hper : HasPeriodMod s k p m)
    (hprim : checkPrimitiveGaps s k p = true)
    (hsharp : checkSharpPreperiod s k p m = true) :
    IsMinimalPeriodicity s k p m ∧
      ∀ k' p' m', HasPeriodMod s k' p' m' → (∃ q, 0 < q ∧ p' = p * q) ∧ k ≤ k' := by
  have hp_pos : 0 < p := hper.1
  have h_all : ∀ k' p' m', HasPeriodMod s k' p' m' → (∃ q, 0 < q ∧ p' = p * q) ∧ k ≤ k' := by
    intro k' p' m' hper'
    have hp'_pos : 0 < p' := hper'.1
    have h_diff_shift : ∀ r, s (k + r + p' + 1) - s (k + r + p') = s (k + r + 1) - s (k + r) := by
      intro r
      have hn_ge_k' : k' ≤ k + r + p * k' := by
        have h1 : 1 * k' ≤ p * k' := Nat.mul_le_mul_right k' hp_pos
        omega
      have heq1 : s ((k + r + p * k') + p' + 1) - s ((k + r + p * k') + p') =
          s ((k + r + p * k') + 1) - s (k + r + p * k') := by
        have ha := hper'.2.2 ((k + r + p * k') + 1) (by omega)
        have hb := hper'.2.2 (k + r + p * k') hn_ge_k'
        have hn1 : (k + r + p * k') + p' + 1 = (k + r + p * k') + 1 + p' := by omega
        rw [hn1, ha, hb]
        exact Nat.add_sub_add_right _ m' _
      have heq2 : s ((k + r + p * k') + 1) - s (k + r + p * k') = s (k + r + 1) - s (k + r) := by
        have h := hper.diff_add_mul (by omega : k ≤ k + r) k'
        have ha : k + r + 1 + p * k' = (k + r + p * k') + 1 := by omega
        rw [ha] at h
        exact h
      have heq3 : s ((k + r + p * k') + p' + 1) - s ((k + r + p * k') + p') =
          s (k + r + p' + 1) - s (k + r + p') := by
        have h := hper.diff_add_mul (by omega : k ≤ k + r + p') k'
        have ha : k + r + p' + 1 + p * k' = (k + r + p * k') + p' + 1 := by omega
        have hb : k + r + p' + p * k' = (k + r + p * k') + p' := by omega
        rw [ha, hb] at h
        exact h
      omega
    have hp'_decomp : p * (p' / p) + p' % p = p' := Nat.div_add_mod p' p
    have hrem_lt : p' % p < p := Nat.mod_lt p' hp_pos
    have hrem_zero : p' % p = 0 := by
      by_cases hrem0 : p' % p = 0
      · exact hrem0
      · unfold checkPrimitiveGaps at hprim
        have hd := (allRange_iff.1 hprim) (p' % p) (by omega) (by omega)
        obtain ⟨r, _, _, hr_ne⟩ := anyRange_iff.1 hd
        split at hr_ne
        · next hne =>
          have h1 := h_diff_shift r
          have h2 := hper.diff_add_mul (by omega : k ≤ k + r + p' % p) (p' / p)
          have ha : k + r + p' % p + 1 + p * (p' / p) = k + r + p' + 1 := by omega
          have hb : k + r + p' % p + p * (p' / p) = k + r + p' := by omega
          rw [ha, hb] at h2
          omega
        · contradiction
    have hp'_eq : p' = p * (p' / p) := by omega
    have hq_pos : 0 < p' / p := by
      by_cases hq0 : p' / p = 0
      · rw [hq0, Nat.mul_zero] at hp'_eq; omega
      · exact Nat.pos_of_ne_zero hq0
    have hk_le : k ≤ k' := by
      by_cases hk0 : k = 0
      · omega
      · unfold checkSharpPreperiod at hsharp
        rw [ite_neg hk0] at hsharp
        split at hsharp
        · next hsharp_pair =>
          by_cases hk_le_chk : k ≤ k'
          · exact hk_le_chk
          · exfalso
            have hk'_le : k' ≤ k - 1 := by omega
            have ha := hper'.2.2 (k - 1 + 1) (by omega)
            have hb := hper'.2.2 (k - 1) hk'_le
            have hdiff_k' : s (k - 1 + 1 + p') - s (k - 1 + p') = s (k - 1 + 1) - s (k - 1) := by
              rw [ha, hb]
              exact Nat.add_sub_add_right _ m' _
            have hq1 : p' = p + p * (p' / p - 1) := by
              have hq_eq : p' / p = 1 + (p' / p - 1) := by omega
              conv => lhs; rw [hp'_eq, hq_eq, Nat.mul_add, Nat.mul_one]
            have hdiff_mul := hper.diff_add_mul (by omega : k ≤ k - 1 + p) (p' / p - 1)
            have ha2 : k - 1 + p + 1 + p * (p' / p - 1) = k - 1 + 1 + p' := by omega
            have hb2 : k - 1 + p + p * (p' / p - 1) = k - 1 + p' := by omega
            rw [ha2, hb2] at hdiff_mul
            have hk1 : k - 1 + 1 = k := by omega
            have hkp1 : k - 1 + p + 1 = k + p := by omega
            rw [hk1] at hdiff_k' hdiff_mul
            rw [hkp1] at hdiff_mul
            exact hsharp_pair.2 (hdiff_mul.symm.trans hdiff_k')
        · contradiction
    exact ⟨⟨p' / p, hq_pos, hp'_eq⟩, hk_le⟩
  refine ⟨⟨hper, ?_, ?_⟩, h_all⟩
  · intro k' p' m' hper'
    obtain ⟨⟨q, hq, hp'_eq⟩, _⟩ := h_all k' p' m' hper'
    have h1 : p * 1 ≤ p * q := Nat.mul_le_mul_left p hq
    omega
  · intro k' m' hper'
    exact (h_all k' p m' hper').2

/-- Master certification theorem packaging the entire proof pipeline for any `(f, g, pre, per, m)`. -/
theorem certify_sequence {f g : Nat} {pre per : List Nat} {m : Nat}
    (hvalid : validCandParams f g pre per m = true)
    (hwin : ∀ x, x < 2 * listGetD per 0 + 3 * m → stepOk f g (candMask pre per m) x = true)
    (hprim : checkPrimitiveGaps (candSeq pre per m) pre.length per.length = true)
    (hsharp : checkSharpPreperiod (candSeq pre per m) pre.length per.length m = true) :
    (∀ x, InSeq f g x ↔ candMask pre per m x = true) ∧
    (∀ n, seq f g n = candSeq pre per m n) ∧
    IsMinimalPeriodicity (seq f g) pre.length per.length m ∧
    (∀ k' p' m', HasPeriodMod (seq f g) k' p' m' →
      (∃ q, 0 < q ∧ p' = per.length * q) ∧ pre.length ≤ k') := by
  unfold validCandParams at hvalid
  split at hvalid
  · next hbounds =>
    obtain ⟨hf, hfg, hp, hm, hT, hg_bound⟩ := hbounds
    simp only [Bool.and_eq_true] at hvalid
    obtain ⟨⟨⟨hc_pre, hb_pre⟩, hc_per⟩, hb_per⟩ := hvalid
    have hmask_per := candMask_periodic pre per hm
    have hin_iff := periodic_mask_characterization hf hfg hT hm hg_bound hmask_per hwin
    have hcand_step := candSeq_lt_succ hp hc_pre hb_pre hc_per hb_per
    have hcand_mono := candSeq_strictMono hcand_step
    have hcand_range := candMask_iff_exists_candSeq hp hb_pre hb_per
    have hseq_mono : ∀ i j, i < j → seq f g i < seq f g j := fun _ _ hij => seq_strictMono hfg hij
    have hrange_eq : ∀ x, (∃ n, seq f g n = x) ↔ (∃ n, candSeq pre per m n = x) := by
      intro x
      rw [← inSeq_iff_exists_seq hfg x, hin_iff x, hcand_range x]
    have hseq_eq : ∀ n, seq f g n = candSeq pre per m n :=
      strictMono_eq_of_range_eq hseq_mono hcand_mono hrange_eq
    have hfun_eq : seq f g = candSeq pre per m := funext hseq_eq
    have hcand_per := candSeq_hasPeriodMod (pre := pre) hp hm
    have hmin_cand := minimal_of_primitive_and_sharp hcand_per hprim hsharp
    rw [← hfun_eq] at hmin_cand
    exact ⟨hin_iff, hseq_eq, hmin_cand.1, hmin_cand.2⟩
  · contradiction

/-! ## 7. Disproof of Conjecture 5: `S_{4, 11}` Has Minimal `(k, p, m) = (11, 10, 33)` (`p = 10 ≠ 9`) -/

def pre4_11 : List Nat := [4, 11, 12, 13, 14, 19, 20, 21, 22, 28, 29]
def per4_11 : List Nat := [37, 38, 44, 45, 46, 53, 54, 61, 62, 69]
abbrev mask4_11 : Nat → Bool := candMask pre4_11 per4_11 33

private theorem w4_11_0 : allRange (stepOk 4 11 mask4_11) 0 30 = true := rfl
private theorem w4_11_1 : allRange (stepOk 4 11 mask4_11) 30 30 = true := rfl
private theorem w4_11_2 : allRange (stepOk 4 11 mask4_11) 60 30 = true := rfl
private theorem w4_11_3 : allRange (stepOk 4 11 mask4_11) 90 30 = true := rfl
private theorem w4_11_4 : allRange (stepOk 4 11 mask4_11) 120 30 = true := rfl
private theorem w4_11_5 : allRange (stepOk 4 11 mask4_11) 150 23 = true := rfl

private theorem win4_11 : ∀ x, x < 2 * listGetD per4_11 0 + 3 * 33 → stepOk 4 11 mask4_11 x = true := by
  intro x hx
  change x < 173 at hx
  by_cases h1 : x < 30
  · exact (allRange_iff.1 w4_11_0) x (Nat.zero_le x) h1
  · by_cases h2 : x < 60
    · exact (allRange_iff.1 w4_11_1) x (by omega) h2
    · by_cases h3 : x < 90
      · exact (allRange_iff.1 w4_11_2) x (by omega) h3
      · by_cases h4 : x < 120
        · exact (allRange_iff.1 w4_11_3) x (by omega) h4
        · by_cases h5 : x < 150
          · exact (allRange_iff.1 w4_11_4) x (by omega) h5
          · exact (allRange_iff.1 w4_11_5) x (by omega) hx

private theorem cert4_11 :
    (∀ x, InSeq 4 11 x ↔ mask4_11 x = true) ∧
    (∀ n, seq 4 11 n = candSeq pre4_11 per4_11 33 n) ∧
    IsMinimalPeriodicity (seq 4 11) 11 10 33 ∧
    (∀ k' p' m', HasPeriodMod (seq 4 11) k' p' m' →
      (∃ q, 0 < q ∧ p' = 10 * q) ∧ 11 ≤ k') :=
  certify_sequence (f := 4) (g := 11) (pre := pre4_11) (per := per4_11) (m := 33)
    rfl win4_11 rfl rfl

/-- Exact membership characterization of `S_{4,11}` for all `x : Nat`. -/
theorem S4_11_inSeq_iff (x : Nat) : InSeq 4 11 x ↔ mask4_11 x = true :=
  cert4_11.1 x

/-- Exact closed-form evaluation of `seq 4 11 n` for all `n : Nat`. -/
theorem S4_11_seq_eq (n : Nat) : seq 4 11 n = candSeq pre4_11 per4_11 33 n :=
  cert4_11.2.1 n

/-- `S_{4,11}` is ultimately periodic with exact minimal parameters `(k, p, m) = (11, 10, 33)`. -/
theorem S4_11_minimal : IsMinimalPeriodicity (seq 4 11) 11 10 33 :=
  cert4_11.2.2.1

/-- Global divisibility and onset minimality of `S_{4,11}` across all valid `(k', p', m')`. -/
theorem S4_11_global_minimality (k' p' m' : Nat) (h : HasPeriodMod (seq 4 11) k' p' m') :
    (∃ q, 0 < q ∧ p' = 10 * q) ∧ 11 ≤ k' :=
  cert4_11.2.2.2 k' p' m' h

/-- Exact 22-term prefix verification of `seq 4 11` matching `inputs/certificates/witness.json`. -/
theorem S4_11_witness_prefix :
    List.map (seq 4 11) [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] =
      [4, 11, 12, 13, 14, 19, 20, 21, 22, 28, 29, 37, 38, 44, 45, 46, 53, 54, 61, 62, 69, 70] := by
  have hfun : seq 4 11 = candSeq pre4_11 per4_11 33 := funext S4_11_seq_eq
  rw [hfun]
  rfl

/-- Negative control / refutation of period 9: no `(k, m)` gives `S_{4,11}` period `9`. -/
theorem S4_11_no_period_9 (k m : Nat) : ¬ HasPeriodMod (seq 4 11) k 9 m := by
  intro h9
  obtain ⟨⟨q, _, heq⟩, _⟩ := cert4_11.2.2.2 k 9 m h9
  omega

/-- Negative control on `S_{4,11}`: preperiod `k = 10` fails (`seq 4 11 20 = 69 ≠ 62 = 29 + 33`). -/
theorem S4_11_preperiod_10_fails : ¬ HasPeriodMod (seq 4 11) 10 10 33 := by
  intro h
  have h10 := h.2.2 10 (Nat.le_refl 10)
  rw [S4_11_seq_eq 20, S4_11_seq_eq 10] at h10
  have hv20 : candSeq pre4_11 per4_11 33 20 = 69 := rfl
  have hv10 : candSeq pre4_11 per4_11 33 10 = 29 := rfl
  omega

/-- Definition 3 Clause (4) formula `\mathcal{L}_f(d)` from `arXiv:2609.18522v1` (lines 286-302, 338-341)
    for the block `b = 1` range `f + q^+ + 1 ≤ d ≤ 2*f + 2`, including the `d = 2*b*f - 1`
    subtraction for `f ≤ 4` (with `f = 4` exceptions at `d = 5, 36` and `d ≡ 4 mod 8, d ≥ 44`). -/
def conj5Clause4Block1Formula (f d : Nat) : Nat :=
  let qMinus := f / 2
  let qPlus := (f + 1) / 2
  let j := d - (f + qPlus + 1)
  let base := 1 * (f + 1 + qMinus) + qPlus + 1 - j * 0
  let corr := if f ≤ 4 ∧ d = 2 * f - 1 then base - 1 else base
  if f = 4 ∧ d = 5 then 2
  else if f = 4 ∧ d = 36 then 5
  else if f = 4 ∧ d % 8 = 4 ∧ 44 ≤ d then corr + (d + 44) / 8
  else corr

theorem conj5_formula_4_7 : conj5Clause4Block1Formula 4 7 = 9 := rfl

/-- Complete disproof of van Berkel & Bosma Conjecture 5 at `(f, g) = (4, 11)` (`d = 7`):
    `S_{4,11}` has unique minimal periodicity `(11, 10, 33)`, `10 ≠ 9`, and Conjecture 5's
    predicted period `9` fails for every `(k, m)`. -/
theorem conj5_disproof_S4_11 :
    IsMinimalPeriodicity (seq 4 11) 11 10 33 ∧
    conj5Clause4Block1Formula 4 (11 - 4) = 9 ∧
    10 ≠ 9 ∧
    (∀ k m, ¬ HasPeriodMod (seq 4 11) k 9 m) ∧
    (∀ k m, ¬ IsMinimalPeriodicity (seq 4 11) k (conj5Clause4Block1Formula 4 (11 - 4)) m) := by
  refine ⟨S4_11_minimal, rfl, by decide, S4_11_no_period_9, ?_⟩
  intro k m hmin
  exact S4_11_no_period_9 k m hmin.1

/-! ## 8. Disproof of Conjecture 9: `S_{5, 10}` Has Minimal `(k, p, m) = (6, 6, 24)` (`k = 6 ≠ 7`) -/

def pre5_10 : List Nat := [5, 10, 11, 12, 13, 14]
def per5_10 : List Nat := [20, 28, 29, 35, 36, 37]
abbrev mask5_10 : Nat → Bool := candMask pre5_10 per5_10 24

private theorem w5_10_0 : allRange (stepOk 5 10 mask5_10) 0 30 = true := rfl
private theorem w5_10_1 : allRange (stepOk 5 10 mask5_10) 30 30 = true := rfl
private theorem w5_10_2 : allRange (stepOk 5 10 mask5_10) 60 30 = true := rfl
private theorem w5_10_3 : allRange (stepOk 5 10 mask5_10) 90 22 = true := rfl

private theorem win5_10 : ∀ x, x < 2 * listGetD per5_10 0 + 3 * 24 → stepOk 5 10 mask5_10 x = true := by
  intro x hx
  change x < 112 at hx
  by_cases h1 : x < 30
  · exact (allRange_iff.1 w5_10_0) x (Nat.zero_le x) h1
  · by_cases h2 : x < 60
    · exact (allRange_iff.1 w5_10_1) x (by omega) h2
    · by_cases h3 : x < 90
      · exact (allRange_iff.1 w5_10_2) x (by omega) h3
      · exact (allRange_iff.1 w5_10_3) x (by omega) hx

private theorem cert5_10 :
    (∀ x, InSeq 5 10 x ↔ mask5_10 x = true) ∧
    (∀ n, seq 5 10 n = candSeq pre5_10 per5_10 24 n) ∧
    IsMinimalPeriodicity (seq 5 10) 6 6 24 ∧
    (∀ k' p' m', HasPeriodMod (seq 5 10) k' p' m' →
      (∃ q, 0 < q ∧ p' = 6 * q) ∧ 6 ≤ k') :=
  certify_sequence (f := 5) (g := 10) (pre := pre5_10) (per := per5_10) (m := 24)
    rfl win5_10 rfl rfl

/-- Exact membership characterization of `S_{5,10}` for all `x : Nat`. -/
theorem S5_10_inSeq_iff (x : Nat) : InSeq 5 10 x ↔ mask5_10 x = true :=
  cert5_10.1 x

/-- Exact closed-form evaluation of `seq 5 10 n` for all `n : Nat`. -/
theorem S5_10_seq_eq (n : Nat) : seq 5 10 n = candSeq pre5_10 per5_10 24 n :=
  cert5_10.2.1 n

/-- `S_{5,10}` is ultimately periodic with exact minimal parameters `(k, p, m) = (6, 6, 24)`. -/
theorem S5_10_minimal : IsMinimalPeriodicity (seq 5 10) 6 6 24 :=
  cert5_10.2.2.1

/-- Global divisibility and onset minimality of `S_{5,10}` across all valid `(k', p', m')`. -/
theorem S5_10_global_minimality (k' p' m' : Nat) (h : HasPeriodMod (seq 5 10) k' p' m') :
    (∃ q, 0 < q ∧ p' = 6 * q) ∧ 6 ≤ k' :=
  cert5_10.2.2.2 k' p' m' h

/-- Exact 13-term prefix verification of `seq 5 10` matching `inputs/certificates/witness.json`. -/
theorem S5_10_witness_prefix :
    List.map (seq 5 10) [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] =
      [5, 10, 11, 12, 13, 14, 20, 28, 29, 35, 36, 37, 44] := by
  have hfun : seq 5 10 = candSeq pre5_10 per5_10 24 := funext S5_10_seq_eq
  rw [hfun]
  rfl

/-- Negative control on `S_{5,10}`: `k = 7` gives a valid periodic tail with `(p, m) = (6, 24)`,
    yet is NOT minimal for any `(p, m)` because `k = 6` already suffices. -/
theorem S5_10_preperiod_7_not_minimal :
    HasPeriodMod (seq 5 10) 7 6 24 ∧ ∀ p m, ¬ IsMinimalPeriodicity (seq 5 10) 7 p m := by
  refine ⟨⟨by decide, by decide, ?_⟩, ?_⟩
  · intro n hn
    exact S5_10_minimal.1.2.2 n (by omega)
  · intro p m h7
    have hun := IsMinimalPeriodicity.unique S5_10_minimal h7
    omega

/-- Negative control on `S_{5,10}`: preperiod `k = 5` fails (`seq 5 10 11 = 37 ≠ 38 = 14 + 24`). -/
theorem S5_10_preperiod_5_fails : ¬ HasPeriodMod (seq 5 10) 5 6 24 := by
  intro h
  have h5 := h.2.2 5 (Nat.le_refl 5)
  rw [S5_10_seq_eq 11, S5_10_seq_eq 5] at h5
  have hv11 : candSeq pre5_10 per5_10 24 11 = 37 := rfl
  have hv5 : candSeq pre5_10 per5_10 24 5 = 14 := rfl
  omega

/-- Negative control on `S_{5,10}`: doubled period `(p, m) = (12, 48)` satisfies `HasPeriodMod`
    yet is rejected by `IsMinimalPeriodicity`. -/
theorem S5_10_doubled_period_not_minimal :
    HasPeriodMod (seq 5 10) 6 12 48 ∧ ¬ IsMinimalPeriodicity (seq 5 10) 6 12 48 := by
  refine ⟨⟨by decide, by decide, ?_⟩, ?_⟩
  · intro n hn
    have h2 := S5_10_minimal.1.add_mul hn 2
    simpa using h2
  · intro hmin
    have hun := IsMinimalPeriodicity.unique S5_10_minimal hmin
    omega

/-- Definition 8 Clause (d) + Clause (k_0) formula `\mathcal{K}_f(d, f)` from `arXiv:2609.18522v1`
    (lines 511-526, 561-565) for `f ≥ 5` and `r = f` (`d = f + h * (2 * f)`). -/
def conj9ClauseDFormula (f d : Nat) : Nat :=
  let twoF := 2 * f
  let r := (d - 1) % twoF + 1
  let h := (d - 1) / twoF
  let base := (4 * f + 1) * h + (5 * f - 3)
  if h = 0 then base - (2 * f + r) else base

theorem conj9_formula_5_5 : conj9ClauseDFormula 5 5 = 7 := rfl

/-- Complete disproof of van Berkel & Bosma Conjecture 9 at `(f, g) = (5, 10)` (`d = 5`):
    `S_{5,10}` has unique minimal periodicity `(6, 6, 24)`, `6 ≠ 7`, and Conjecture 9's
    predicted minimal preperiod `7` fails `IsMinimalPeriodicity` for every `(p, m)`. -/
theorem conj9_disproof_S5_10 :
    IsMinimalPeriodicity (seq 5 10) 6 6 24 ∧
    conj9ClauseDFormula 5 (10 - 5) = 7 ∧
    6 ≠ 7 ∧
    (∀ p m, ¬ IsMinimalPeriodicity (seq 5 10) 7 p m) ∧
    (∀ p m, ¬ IsMinimalPeriodicity (seq 5 10) (conj9ClauseDFormula 5 (10 - 5)) p m) := by
  refine ⟨S5_10_minimal, rfl, by decide, S5_10_preperiod_7_not_minimal.2, ?_⟩
  intro p m hmin
  exact S5_10_preperiod_7_not_minimal.2 p m hmin

/-! ## 9. Kernel-Checked Positive Controls (`S_{1,3}`, `S_{1,2}`, `S_{2,3}`) -/

-- Positive Control 1: `S_{1,3} = 1, 3, 5, 7, ...` (odd numbers, `k = 0, p = 1, m = 2`).
def pre1_3 : List Nat := []
def per1_3 : List Nat := [1]

private theorem w1_3 : allRange (stepOk 1 3 (candMask pre1_3 per1_3 2)) 0 8 = true := rfl

private theorem win1_3 : ∀ x, x < 2 * listGetD per1_3 0 + 3 * 2 →
    stepOk 1 3 (candMask pre1_3 per1_3 2) x = true :=
  fun x hx => (allRange_iff.1 w1_3) x (Nat.zero_le x) hx

/-- Positive control 1: `S_{1,3}` is purely periodic with minimal `(k, p, m) = (0, 1, 2)`. -/
theorem S1_3_minimal : IsMinimalPeriodicity (seq 1 3) 0 1 2 :=
  (certify_sequence (f := 1) (g := 3) (pre := pre1_3) (per := per1_3) (m := 2)
    rfl win1_3 rfl rfl).2.2.1

-- Positive Control 2: `S_{1,2} = 1, 2, 4, 7, 10, 13, ...` (`k = 2, p = 1, m = 3`).
def pre1_2 : List Nat := [1, 2]
def per1_2 : List Nat := [4]

private theorem w1_2 : allRange (stepOk 1 2 (candMask pre1_2 per1_2 3)) 0 17 = true := rfl

private theorem win1_2 : ∀ x, x < 2 * listGetD per1_2 0 + 3 * 3 →
    stepOk 1 2 (candMask pre1_2 per1_2 3) x = true :=
  fun x hx => (allRange_iff.1 w1_2) x (Nat.zero_le x) hx

/-- Positive control 2: `S_{1,2}` has exact minimal parameters `(k, p, m) = (2, 1, 3)`. -/
theorem S1_2_minimal : IsMinimalPeriodicity (seq 1 2) 2 1 3 :=
  (certify_sequence (f := 1) (g := 2) (pre := pre1_2) (per := per1_2) (m := 3)
    rfl win1_2 rfl rfl).2.2.1

-- Positive Control 3: `S_{2,3} = 2, 3, 4, 8, 9, 14, 15, ...` (`k = 3, p = 2, m = 6`).
def pre2_3 : List Nat := [2, 3, 4]
def per2_3 : List Nat := [8, 9]

private theorem w2_3_0 : allRange (stepOk 2 3 (candMask pre2_3 per2_3 6)) 0 20 = true := rfl
private theorem w2_3_1 : allRange (stepOk 2 3 (candMask pre2_3 per2_3 6)) 20 14 = true := rfl

private theorem win2_3 : ∀ x, x < 2 * listGetD per2_3 0 + 3 * 6 →
    stepOk 2 3 (candMask pre2_3 per2_3 6) x = true := by
  intro x hx
  change x < 34 at hx
  by_cases h1 : x < 20
  · exact (allRange_iff.1 w2_3_0) x (Nat.zero_le x) h1
  · exact (allRange_iff.1 w2_3_1) x (by omega) hx

/-- Positive control 3: `S_{2,3}` has exact minimal parameters `(k, p, m) = (3, 2, 6)`. -/
theorem S2_3_minimal : IsMinimalPeriodicity (seq 2 3) 3 2 6 :=
  (certify_sequence (f := 2) (g := 3) (pre := pre2_3) (per := per2_3) (m := 6)
    rfl win2_3 rfl rfl).2.2.1

-- Positive Control 4: Immediate neighbor `S_{4,12}` (`f = 4, d = 8`) in the same Clause 4 block,
-- where `conj5Clause4Block1Formula 4 8 = 10` agrees with the true minimal period `p = 10`.
def pre4_12 : List Nat := [4, 12, 13, 14, 15, 20]
def per4_12 : List Nat := [21, 22, 23, 30, 31, 39, 40, 47, 48, 49]
abbrev mask4_12 : Nat → Bool := candMask pre4_12 per4_12 35

private theorem w4_12_0 : allRange (stepOk 4 12 mask4_12) 0 30 = true := rfl
private theorem w4_12_1 : allRange (stepOk 4 12 mask4_12) 30 30 = true := rfl
private theorem w4_12_2 : allRange (stepOk 4 12 mask4_12) 60 30 = true := rfl
private theorem w4_12_3 : allRange (stepOk 4 12 mask4_12) 90 30 = true := rfl
private theorem w4_12_4 : allRange (stepOk 4 12 mask4_12) 120 27 = true := rfl

private theorem win4_12 : ∀ x, x < 2 * listGetD per4_12 0 + 3 * 35 → stepOk 4 12 mask4_12 x = true := by
  intro x hx
  change x < 147 at hx
  by_cases h1 : x < 30
  · exact (allRange_iff.1 w4_12_0) x (Nat.zero_le x) h1
  · by_cases h2 : x < 60
    · exact (allRange_iff.1 w4_12_1) x (by omega) h2
    · by_cases h3 : x < 90
      · exact (allRange_iff.1 w4_12_2) x (by omega) h3
      · by_cases h4 : x < 120
        · exact (allRange_iff.1 w4_12_3) x (by omega) h4
        · exact (allRange_iff.1 w4_12_4) x (by omega) hx

/-- Positive control 4 (same-clause neighbor of `S_{4,11}`): `S_{4,12}` (`d = 8`) has minimal
    parameters `(6, 10, 35)`, agreeing with `conj5Clause4Block1Formula 4 8 = 10`. -/
theorem S4_12_minimal_and_conj5_agrees :
    IsMinimalPeriodicity (seq 4 12) 6 10 35 ∧ conj5Clause4Block1Formula 4 (12 - 4) = 10 :=
  ⟨(certify_sequence (f := 4) (g := 12) (pre := pre4_12) (per := per4_12) (m := 35)
    rfl win4_12 rfl rfl).2.2.1, rfl⟩

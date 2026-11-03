module

public import Mathlib.Data.List.Count
public import Mathlib.Algebra.Order.BigOperators.Group.List
public import Mathlib.Basic.Real.Basic
public import Mathlib.Tactic

@[expose] public section

namespace C30Lean

/-- Integer excess above a threshold; the order of the list is retained. -/
def excess (y : List ℤ) (k : ℤ) : ℤ := (y.map (fun a => max (a - k) 0)).sum

def countStrip (y : List ℤ) (j : ℤ) : ℤ := y.count j

theorem excess_nonneg (y : List ℤ) (k : ℤ) : 0 ≤ excess y k := by
  apply List.sum_nonneg
  intro a ha
  obtain ⟨b, _, rfl⟩ := List.mem_map.mp ha
  exact le_max_right _ _

theorem strip_count_identities (y : List ℤ) (hy : ∀ a ∈ y, 0 ≤ a) :
    excess y 0 = y.sum ∧
    excess y 1 = y.sum - y.length + countStrip y 0 ∧
    excess y 2 = y.sum - 2 * y.length + 2 * countStrip y 0 + countStrip y 1 ∧
    3 * (y.length : ℤ) - y.sum + countStrip y 0 - countStrip y 2 ≤
      2 * (2 * countStrip y 0 + countStrip y 1) := by
  induction y with
  | nil => simp [excess, countStrip]
  | cons a y ih =>
    have ha := hy a (by simp)
    have ih := ih (by intro b hb; exact hy b (by simp [hb]))
    simp only [excess, List.map_cons, List.sum_cons, List.length_cons,
      countStrip, List.count_cons, beq_iff_eq, Nat.cast_add, Nat.cast_one] at *
    split_ifs <;> omega

/-- Natural multiplicities ensure that the envelope vector is integral and nonnegative. -/
structure StripEnvelope where
  e0 : ℕ
  e1 : ℕ
  e2 : ℕ
  e3 : ℕ

def StripEnvelope.vector (e : StripEnvelope) : List ℤ :=
  List.replicate e.e0 0 ++ List.replicate e.e1 1 ++
    List.replicate e.e2 2 ++ List.replicate e.e3 3

theorem StripEnvelope.vector_nonneg (e : StripEnvelope) :
    ∀ a ∈ e.vector, 0 ≤ a := by
  intro a ha
  simp only [StripEnvelope.vector, List.mem_append, List.mem_replicate] at ha
  rcases ha with ((⟨_, rfl⟩ | ⟨_, rfl⟩) | ⟨_, rfl⟩) | ⟨_, rfl⟩ <;> norm_num

theorem StripEnvelope.vector_length (e : StripEnvelope) :
    e.vector.length = e.e0 + e.e1 + e.e2 + e.e3 := by
  simp [StripEnvelope.vector, add_assoc]

theorem StripEnvelope.vector_sum (e : StripEnvelope) :
    e.vector.sum = (e.e1 : ℤ) + 2 * e.e2 + 3 * e.e3 := by
  simp [StripEnvelope.vector, List.sum_replicate]
  ring

theorem StripEnvelope.excess_values (e : StripEnvelope) :
    excess e.vector 1 = (e.e2 : ℤ) + 2 * e.e3 ∧
    excess e.vector 2 = e.e3 ∧
    (∀ k : ℤ, 3 ≤ k → excess e.vector k = 0) := by
  constructor
  · simp [excess, StripEnvelope.vector, List.sum_replicate]
    ring
  constructor
  · simp [excess, StripEnvelope.vector, List.sum_replicate]
  · intro k hk
    have h1 : max (1 - k) 0 = (0 : ℤ) := max_eq_right (by omega)
    have h2 : max (2 - k) 0 = (0 : ℤ) := max_eq_right (by omega)
    have h3 : max (3 - k) 0 = (0 : ℤ) := max_eq_right (by omega)
    simp [excess, StripEnvelope.vector, h1, h2, h3, show 0 ≤ k by omega]

/-- Choose U or U-1, keeping the numerator of e3 even. The U=0 guard is
    necessary: an odd numerator would force the negative multiplicity -1. -/
theorem parity_envelope (r L B U : ℤ)
    (hB : 0 ≤ B) (hU : 0 ≤ U)
    (hzero : U = 0 → (L - r + B) % 2 = 0)
    (h₁ : U ≤ 3 * (r - B) - L) (h₃ : U ≤ L - r + B) :
    ∃ e : StripEnvelope,
      (e.e0 : ℤ) = B ∧
      ((e.e2 : ℤ) = U ∨ (e.e2 : ℤ) = U - 1) ∧
      (L - r + B - e.e2) % 2 = 0 ∧
      (e.e1 : ℤ) = (3 * (r - B) - L - e.e2) / 2 ∧
      (e.e3 : ℤ) = (L - r + B - e.e2) / 2 ∧
      (e.e0 : ℤ) + e.e1 + e.e2 + e.e3 = r ∧
      (e.e1 : ℤ) + 2 * e.e2 + 3 * e.e3 = L := by
  let c := if (L - r + B - U) % 2 = 0 then U else U - 1
  have hc : c = U ∨ c = U - 1 := by simp only [c]; split_ifs <;> simp
  have hp : (L - r + B - c) % 2 = 0 := by
    dsimp [c]
    split_ifs <;> omega
  have hc0 : 0 ≤ c := by
    dsimp [c]
    split_ifs with h
    · exact hU
    · by_cases hz : U = 0
      · have hpz := hzero hz
        omega
      · omega
  let a := (3 * (r - B) - L - c) / 2
  let d := (L - r + B - c) / 2
  have ha : 0 ≤ a := by dsimp [a]; omega
  have hd : 0 ≤ d := by dsimp [d]; omega
  have ha2 : 2 * a = 3 * (r - B) - L - c := by dsimp [a]; omega
  have hd2 : 2 * d = L - r + B - c := by dsimp [d]; omega
  refine ⟨⟨B.toNat, a.toNat, c.toNat, d.toNat⟩, ?_⟩
  change B.toNat = B ∧ ((c.toNat : ℤ) = U ∨ (c.toNat : ℤ) = U - 1) ∧
    (L - r + B - c.toNat) % 2 = 0 ∧
    (a.toNat : ℤ) = (3 * (r - B) - L - c.toNat) / 2 ∧
    (d.toNat : ℤ) = (L - r + B - c.toNat) / 2 ∧
    (B.toNat : ℤ) + a.toNat + c.toNat + d.toNat = r ∧
    (a.toNat : ℤ) + 2 * c.toNat + 3 * d.toNat = L
  simp only [Int.toNat_of_nonneg hB, Int.toNat_of_nonneg ha,
    Int.toNat_of_nonneg hc0, Int.toNat_of_nonneg hd]
  exact ⟨trivial, hc, hp, rfl, rfl, by linarith only [ha2, hd2],
    by linarith only [ha2, hd2]⟩

/-- The integer threshold-excess form of the strip envelope. -/
theorem integer_strip_envelope (y : List ℤ) (L B U : ℤ)
    (hy : ∀ a ∈ y, 0 ≤ a) (hL : y.sum = L)
    (hn0 : B ≤ countStrip y 0) (hn2 : countStrip y 2 ≤ U)
    (hB : 0 ≤ B) (hU : 0 ≤ U)
    (hzero : U = 0 → (L - y.length + B) % 2 = 0)
    (h₁ : U ≤ 3 * ((y.length : ℤ) - B) - L)
    (h₃ : U ≤ L - y.length + B) :
    ∃ e : StripEnvelope,
      (e.e0 : ℤ) = B ∧
      ((e.e2 : ℤ) = U ∨ (e.e2 : ℤ) = U - 1) ∧
      (L - y.length + B - e.e2) % 2 = 0 ∧
      (e.e1 : ℤ) = (3 * ((y.length : ℤ) - B) - L - e.e2) / 2 ∧
      (e.e3 : ℤ) = (L - y.length + B - e.e2) / 2 ∧
      e.vector.length = y.length ∧ e.vector.sum = y.sum ∧
      (∀ k : ℤ, excess e.vector k ≤ excess y k) := by
  obtain ⟨e, he0, he2, hp, he1, he3, hlen, hsum⟩ :=
    parity_envelope y.length L B U hB hU hzero h₁ h₃
  have hlen' : e.vector.length = y.length := by
    rw [e.vector_length]
    omega
  have hsum' : e.vector.sum = y.sum := by rw [e.vector_sum, hsum, hL]
  refine ⟨e, he0, he2, hp, he1, he3, hlen', hsum', ?_⟩
  have hid := strip_count_identities y hy
  have hxid := strip_count_identities e.vector e.vector_nonneg
  have hx := e.excess_values
  intro k
  by_cases hk : k ≤ 0
  · have neg_excess : ∀ (z : List ℤ), (∀ a ∈ z, 0 ≤ a) →
        excess z k = z.sum - k * z.length := by
      intro z hz
      induction z with
      | nil => simp [excess]
      | cons a z ih =>
        have ha := hz a (by simp)
        have hi := ih (by intro b hb; exact hz b (by simp [hb]))
        have hm : max (a - k) 0 = a - k := max_eq_left (by omega)
        simp only [excess, List.map_cons, List.sum_cons, List.length_cons,
          Nat.cast_add, Nat.cast_one] at *
        rw [hm, hi]
        ring
    rw [neg_excess _ e.vector_nonneg, neg_excess _ hy, hlen', hsum']
  · by_cases hk1 : k = 1
    · subst k; omega
    · by_cases hk2 : k = 2
      · subst k; omega
      · rw [hx.2.2 k (by omega)]
        exact excess_nonneg y k

end C30Lean

import C30Lean
import Spec

/-!
# Bridge: producer theorems (C30Lean, math-certificates cfaa054) ⇒ Spec v1

AI audit (Claude Opus 5.5), unrefereed.
-/

namespace Bridge

open Spec C30Lean
open scoped BigOperators

/-! ## Translation lemmas between `List ℤ` (producer) and `Multiset ℤ` (Spec) -/

lemma ex_coe (l : List ℤ) (t : ℝ) : Spec.ex t (l : Multiset ℤ) = realExcess l t := by
  simp [Spec.ex, realExcess]

lemma envVec_eq (e : StripEnvelope) :
    envVec (e.e0 : ℤ) (e.e1 : ℤ) (e.e2 : ℤ) (e.e3 : ℤ) = (e.vector : Multiset ℤ) := by
  simp only [envVec, StripEnvelope.vector, Int.toNat_natCast, ← Multiset.coe_add,
    Multiset.coe_replicate, add_assoc]

lemma majorized_of_threshold (x y : List ℤ) (h : ThresholdMajorized x y) :
    Majorized (x : Multiset ℤ) (y : Multiset ℤ) := by
  obtain ⟨hl, hs, ht⟩ := h
  refine ⟨by simpa using hl, by simpa using hs, fun t => ?_⟩
  rw [ex_coe, ex_coe]
  exact ht t

/-- Pinning: the parity clause makes the producer's e₂ equal to the Spec's e₂. -/
lemma pin (r L B U a b : ℤ) (ha : a = U ∨ a = U - 1) (hb : b = U ∨ b = U - 1)
    (hpa : (L - r + B - a) % 2 = 0) (hpb : Even (L - r + B - b)) : a = b := by
  rw [Int.even_iff] at hpb
  omega

/-! ## Lemma E: conditional bridge from the headline theorem `strip_envelope` -/

/-- `strip_envelope` ⇒ Spec E, under the producer's two extra hypotheses h₁, h₃. -/
theorem bridge_E_conditional (y : Multiset ℤ) (L B U : ℤ) (hE : HypE1_4 y L B U)
    (e0 e1 e2 e3 : ℤ) (he : HypE5_8 (Multiset.card y : ℤ) L B U e0 e1 e2 e3)
    (h₁ : U ≤ 3 * ((Multiset.card y : ℤ) - B) - L)
    (h₃ : U ≤ L - (Multiset.card y : ℤ) + B) :
    ConclE y L e0 e1 e2 e3 := by
  obtain ⟨l, rfl⟩ : ∃ l : List ℤ, (l : Multiset ℤ) = y := Quotient.exists_rep y
  obtain ⟨hy, hL, hn0, hn2⟩ := hE
  obtain ⟨h25, hpar, he0, he1, he3, p0, p1, p2, p3⟩ := he
  have hcard : (Multiset.card (l : Multiset ℤ) : ℤ) = (l.length : ℤ) := by simp
  simp only [Multiset.sum_coe, Multiset.coe_count,
    Multiset.mem_coe] at hy hL hn0 hn2
  unfold ConclE; simp only [hcard] at *
  have hB : 0 ≤ B := he0 ▸ p0
  have hU : 0 ≤ U := by omega
  have hzero : U = 0 → (L - l.length + B) % 2 = 0 := by
    intro hU0
    have : e2 = 0 := by omega
    rw [Int.even_iff] at hpar
    omega
  obtain ⟨e, f0, f2, fp, f1, f3, hmaj⟩ :=
    strip_envelope l L B U hy hL hn0 hn2 hB hU hzero h₁ h₃
  have q2 : (e.e2 : ℤ) = e2 := pin _ _ _ _ _ _ f2 h25 fp hpar
  have q0 : (e.e0 : ℤ) = e0 := by omega
  have q1 : (e.e1 : ℤ) = e1 := by rw [f1, q2]; omega
  have q3 : (e.e3 : ℤ) = e3 := by rw [f3, q2]; omega
  refine ⟨?_, by omega, by omega⟩
  rw [← q0, ← q1, ← q2, ← q3, envVec_eq]
  exact majorized_of_threshold _ _ hmaj

/-- The round-1 boundary example, in Lean: at y = [0,0], B = 2, U = 1 (L = 0), Spec E's
    hypotheses hold with e = (2,0,0,0), but `strip_envelope`'s h₁ and h₃ both fail. -/
example :
    HypE1_4 (([0, 0] : List ℤ) : Multiset ℤ) 0 2 1 ∧
    HypE5_8 (Multiset.card (([0, 0] : List ℤ) : Multiset ℤ) : ℤ) 0 2 1 2 0 0 0 ∧
    ¬ ((1 : ℤ) ≤ 3 * ((Multiset.card (([0, 0] : List ℤ) : Multiset ℤ) : ℤ) - 2) - 0) ∧
    ¬ ((1 : ℤ) ≤ 0 - (Multiset.card (([0, 0] : List ℤ) : Multiset ℤ) : ℤ) + 2) := by
  refine ⟨⟨?_, ?_, ?_, ?_⟩, ⟨?_, ?_, ?_⟩, ?_, ?_⟩ <;> simp

/-! ## Lemma E: the strongest implication — Spec E in full, from the producer's auxiliary lemmas
    (`strip_count_identities`, `StripEnvelope.excess_values`, `excess_nonneg`,
    `integer_thresholds_suffice`). This shows h₁, h₃ are an artifact of `parity_envelope`,
    not needed for truth. -/

lemma excess_nonpos_threshold (z : List ℤ) (k : ℤ) (hk : k ≤ 0) (hz : ∀ a ∈ z, 0 ≤ a) :
    excess z k = z.sum - k * z.length := by
  induction z with
  | nil => simp [excess]
  | cons a z ih =>
    have ha := hz a (by simp)
    have hi := ih (fun b hb => hz b (by simp [hb]))
    have hm : max (a - k) 0 = a - k := max_eq_left (by omega)
    simp only [excess, List.map_cons, List.sum_cons, List.length_cons, Nat.cast_add,
      Nat.cast_one] at *
    rw [hm, hi]
    ring

theorem specE_full : LemmaE := by
  intro y L B U hE e0 e1 e2 e3 he
  obtain ⟨l, rfl⟩ : ∃ l : List ℤ, (l : Multiset ℤ) = y := Quotient.exists_rep y
  obtain ⟨hy, hL, hn0, hn2⟩ := hE
  obtain ⟨h25, hpar, he0, he1, he3, p0, p1, p2, p3⟩ := he
  have hcard : (Multiset.card (l : Multiset ℤ) : ℤ) = (l.length : ℤ) := by simp
  simp only [Multiset.sum_coe, Multiset.coe_count,
    Multiset.mem_coe] at hy hL hn0 hn2
  unfold ConclE; simp only [hcard] at *
  rw [Int.even_iff] at hpar
  let e : StripEnvelope := ⟨e0.toNat, e1.toNat, e2.toNat, e3.toNat⟩
  have c0 : (e.e0 : ℤ) = e0 := Int.toNat_of_nonneg p0
  have c1 : (e.e1 : ℤ) = e1 := Int.toNat_of_nonneg p1
  have c2 : (e.e2 : ℤ) = e2 := Int.toNat_of_nonneg p2
  have c3 : (e.e3 : ℤ) = e3 := Int.toNat_of_nonneg p3
  have hlen : e.vector.length = l.length := by
    have := e.vector_length
    have h : ((e.vector.length : ℕ) : ℤ) = l.length := by
      rw [this]; push_cast; rw [c0, c1, c2, c3]; omega
    exact_mod_cast h
  have hsum : e.vector.sum = l.sum := by rw [e.vector_sum, c1, c2, c3, hL]; omega
  have hid := strip_count_identities l hy
  have hxid := strip_count_identities e.vector e.vector_nonneg
  have hx := e.excess_values
  unfold countStrip at hid hxid
  have hexc : ∀ k : ℤ, excess e.vector k ≤ excess l k := by
    intro k
    by_cases hk : k ≤ 0
    · rw [excess_nonpos_threshold _ k hk e.vector_nonneg,
        excess_nonpos_threshold _ k hk hy, hlen, hsum]
    · by_cases hk1 : k = 1
      · subst hk1; rw [hx.1, hid.2.1, c2, c3]; omega
      · by_cases hk2 : k = 2
        · subst hk2; rw [hx.2.1, hid.2.2.1, c3]; omega
        · rw [hx.2.2 k (by omega)]
          exact excess_nonneg l k
  have hmaj : ThresholdMajorized e.vector l :=
    ⟨hlen, hsum, integer_thresholds_suffice _ _ hexc⟩
  refine ⟨?_, by omega, by omega⟩
  rw [← c0, ← c1, ← c2, ← c3, envVec_eq]
  exact majorized_of_threshold _ _ hmaj

/-! ## Lemma E-app: `strip_envelope_application` ⇒ Spec E at the application parameters, m ≥ 100 -/

lemma Lapp_eq (m : ℕ) : Lapp m = freeLeaves m := by
  unfold Lapp freeLeaves; congr 1; ring
lemma Bapp_eq (m : ℕ) : Bapp m = emptyBound m := by
  unfold Bapp emptyBound; congr 2; ring
lemma Uapp_eq (m : ℕ) : Uapp m = twoCap m := by
  unfold Uapp twoCap; congr 1; ring
lemma rapp_eq (m : ℕ) : rapp m = stripCount m := by
  unfold rapp stripCount; rw [Lapp_eq]

theorem bridge_Eapp : EappInstance 100 := by
  intro m hm y hcardy hE
  obtain ⟨l, rfl⟩ : ∃ l : List ℤ, (l : Multiset ℤ) = y := Quotient.exists_rep y
  obtain ⟨hy, hL, hn0, hn2⟩ := hE
  have hcard : (Multiset.card (l : Multiset ℤ) : ℤ) = (l.length : ℤ) := by simp
  simp only [Multiset.sum_coe, Multiset.coe_count,
    Multiset.mem_coe] at hy hL hn0 hn2
  rw [hcard] at hcardy
  rw [Lapp_eq] at hL
  rw [Bapp_eq] at hn0
  rw [Uapp_eq] at hn2
  obtain ⟨e, f0, f2, fp, f1, f3, hmaj⟩ :=
    strip_envelope_application l m hm hy (by rw [hcardy, rapp_eq]) hL hn0 hn2
  rw [hcardy, rapp_eq] at fp f1 f3
  have g2 : e2app m = (e.e2 : ℤ) := by
    unfold e2app
    rw [Lapp_eq, Bapp_eq, Uapp_eq, rapp_eq]
    split_ifs with h
    · rw [Int.even_iff] at h; omega
    · rw [Int.even_iff] at h; omega
  have g0 : e0app m = (e.e0 : ℤ) := by unfold e0app; rw [Bapp_eq, f0]
  have g1 : e1app m = (e.e1 : ℤ) := by
    unfold e1app; rw [g2, Lapp_eq, Bapp_eq, rapp_eq, f1]
  have g3 : e3app m = (e.e3 : ℤ) := by
    unfold e3app; rw [g2, Lapp_eq, Bapp_eq, rapp_eq, f3]
  have hU2 : e2app m = Uapp m ∨ e2app m = Uapp m - 1 := by
    unfold e2app; split_ifs <;> simp
  refine ⟨⟨hU2, ?_, rfl, ?_, ?_, ?_, ?_, ?_, ?_⟩, ?_⟩
  · rw [Int.even_iff, g2, Lapp_eq, Bapp_eq, rapp_eq]; exact fp
  · rw [g1, g2, Lapp_eq, Bapp_eq, rapp_eq]; omega
  · rw [g3, g2, Lapp_eq, Bapp_eq, rapp_eq]; omega
  · rw [g0]; positivity
  · rw [g1]; positivity
  · rw [g2]; positivity
  · rw [g3]; positivity
  · have hc : (Multiset.card (l : Multiset ℤ) : ℤ) = rapp m := by simpa using hcardy
    refine ⟨?_, ?_, ?_⟩
    · rw [g0, g1, g2, g3, envVec_eq]
      exact majorized_of_threshold _ _ hmaj
    · rw [hc, g0, g1, g2, g3, rapp_eq]; omega
    · rw [g1, g2, g3, Lapp_eq]; omega

/-- E-app (core) with the explicit cutoff M0 = 100, from `application_feasibility`. -/
theorem eappCore_at (m : ℕ) (hm : 100 ≤ m) :
    Even (3 * (rapp m - Bapp m) - Lapp m - e2app m) ∧
    Even (Lapp m - rapp m + Bapp m - e2app m) ∧
    0 ≤ e0app m ∧ 0 ≤ e1app m ∧ 0 ≤ e2app m ∧ 0 ≤ e3app m := by
  obtain ⟨hb, hu, h1, h3⟩ := application_feasibility m hm
  rw [← Lapp_eq, ← Bapp_eq, ← Uapp_eq, ← rapp_eq] at h1 h3
  rw [← Bapp_eq] at hb
  rw [← Uapp_eq] at hu
  have hU2 : (e2app m = Uapp m ∨ e2app m = Uapp m - 1) ∧
      (Lapp m - rapp m + Bapp m - e2app m) % 2 = 0 := by
    unfold e2app; split_ifs with h
    · rw [Int.even_iff] at h; exact ⟨Or.inl rfl, h⟩
    · rw [Int.even_iff] at h; exact ⟨Or.inr rfl, by omega⟩
  unfold e0app e1app e3app
  simp only [Int.even_iff]
  omega

theorem bridge_EappCore : EappCore := ⟨100, fun m hm => eappCore_at m hm⟩

/-- E-app (counting): no producer theorem states it (the producer keeps hn0, hn2 as hypotheses).
    Proved here (our proof) with M0 = 3·10⁷; round 1 found the last failure of (ii) at
    m = 29,799,973, so the cutoff is near-tight. -/
theorem eappCounting_proved : EappCounting := by
  refine ⟨30000000, fun m hm => ?_⟩
  have hm' : (30000000 : ℚ) ≤ m := by exact_mod_cast hm
  have hL₀ := Int.le_ceil ((555555 / 1000000 : ℚ) * m)
  have hL₁ := Int.ceil_lt_add_one ((555555 / 1000000 : ℚ) * m)
  have hB₁ := Int.ceil_lt_add_one ((185185 / 1000000 : ℚ) * m)
  have hU₁ := Int.lt_floor_add_one ((7 / 50 : ℚ) * m)
  refine ⟨?_, ?_, ?_⟩
  · unfold Uapp Lapp; linarith
  · unfold Bapp; push_cast; linarith
  · have : ((Bapp m : ℤ) : ℚ) ≤ (rapp m : ℚ) := by
      unfold Bapp rapp Lapp; push_cast; linarith
    exact_mod_cast this

/-! ## Lemma M -/

/-- Spec M restricted to ℕ-valued X, from the headline theorem `finite_family_selection`. -/
theorem bridge_M_nat (I : Type) [Fintype I] (n N₂ : I → ℕ) (a : I → ℝ) (s : ℝ)
    (hs : 0 < s) (ha : ∀ i, 0 ≤ a i) :
    (∑ i ∈ Finset.univ.filter (fun i => (N₂ i : ℝ) > s * (n i : ℝ)),
        (n i : ℝ) * ((n i : ℝ) - 1) * a i)
      ≤ (1 / s) * ∑ i, (n i : ℝ) * (N₂ i : ℝ) * a i := by
  have h := finite_family_selection Finset.univ a n N₂ s hs (fun i _ => ha i)
  have e1 : (∑ i ∈ Finset.univ.filter (fun i => (N₂ i : ℝ) > s * (n i : ℝ)),
        (n i : ℝ) * ((n i : ℝ) - 1) * a i) =
      ∑ i ∈ Finset.univ with s * (n i : ℝ) < (N₂ i : ℝ),
        a i * (n i : ℝ) * ((n i : ℝ) - 1) := by
    apply Finset.sum_congr rfl; intro i _; ring
  have e2 : (1 / s) * ∑ i, (n i : ℝ) * (N₂ i : ℝ) * a i =
      (∑ i, a i * (n i : ℝ) * (N₂ i : ℝ)) / s := by
    rw [one_div_mul_eq_div]; congr 1; apply Finset.sum_congr rfl; intro i _; ring
  rw [e1, e2]; exact h

/-- Spec M summed form over real X, from the headline theorem `finite_weighted_markov`
    (with w = n(n-1)a, f = X/n). -/
theorem bridge_M_summed (I : Type) [Fintype I] (n : I → ℕ) (X a : I → ℝ) (s : ℝ)
    (hs : 0 < s) (hX : ∀ i, 0 ≤ X i) (ha : ∀ i, 0 ≤ a i) :
    (∑ i ∈ Finset.univ.filter (fun i => X i > s * (n i : ℝ)),
        (n i : ℝ) * ((n i : ℝ) - 1) * a i)
      ≤ (1 / s) * ∑ i, (n i : ℝ) * X i * a i := by
  classical
  set w : I → ℝ := fun i => (n i : ℝ) * ((n i : ℝ) - 1) * a i with hw
  set f : I → ℝ := fun i => X i / (n i : ℝ) with hf
  have wnn : ∀ i, 0 ≤ w i := by
    intro i
    have : 0 ≤ (n i : ℝ) * ((n i : ℝ) - 1) := by
      rcases Nat.eq_zero_or_pos (n i) with h0 | hpos
      · simp [h0]
      · have : (1 : ℝ) ≤ n i := by exact_mod_cast hpos
        nlinarith
    exact mul_nonneg this (ha i)
  have fnn : ∀ i, 0 ≤ f i := fun i => div_nonneg (hX i) (Nat.cast_nonneg _)
  have hm := finite_weighted_markov Finset.univ w f s hs (fun i _ => wnn i) (fun i _ => fnn i)
  -- left side: {X > s n} ≤ {s < X/n} on weights w (items with n = 0 have w = 0)
  have hl : (∑ i ∈ Finset.univ.filter (fun i => X i > s * (n i : ℝ)), w i) ≤
      ∑ i ∈ Finset.univ with s < f i, w i := by
    rw [Finset.sum_filter, Finset.sum_filter]
    apply Finset.sum_le_sum
    intro i _
    split_ifs with h1 h2 h2
    · exact le_rfl
    · rcases Nat.eq_zero_or_pos (n i) with h0 | hpos
      · simp [hw, h0]
      · exfalso; apply h2
        have hn : (0 : ℝ) < n i := by exact_mod_cast hpos
        simp only [hf]; rw [lt_div_iff₀ hn]; linarith
    · exact wnn i
    · exact le_rfl
  -- right side: w f = (n-1) X a ≤ n X a
  have hr : (∑ i, w i * f i) ≤ ∑ i, (n i : ℝ) * X i * a i := by
    apply Finset.sum_le_sum
    intro i _
    rcases Nat.eq_zero_or_pos (n i) with h0 | hpos
    · simp [hw, h0]
    · have hn : (n i : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
      have : w i * f i = ((n i : ℝ) - 1) * X i * a i := by
        simp only [hw, hf]; field_simp
      rw [this]
      have := mul_nonneg (hX i) (ha i)
      nlinarith
  calc (∑ i ∈ Finset.univ.filter (fun i => X i > s * (n i : ℝ)),
        (n i : ℝ) * ((n i : ℝ) - 1) * a i)
      = ∑ i ∈ Finset.univ.filter (fun i => X i > s * (n i : ℝ)), w i := rfl
    _ ≤ ∑ i ∈ Finset.univ with s < f i, w i := hl
    _ ≤ (∑ i, w i * f i) / s := hm
    _ ≤ (∑ i, (n i : ℝ) * X i * a i) / s := div_le_div_of_nonneg_right hr hs.le
    _ = (1 / s) * ∑ i, (n i : ℝ) * X i * a i := by rw [one_div_mul_eq_div]

/-- Spec M in full (pointwise form = summed form on the one-point family). -/
theorem bridge_M : LemmaM := by
  intro I _ n X a s hs hX ha
  refine ⟨fun i hi => ?_, bridge_M_summed I n X a s hs hX ha⟩
  have h := bridge_M_summed Unit (fun _ => n i) (fun _ => X i) (fun _ => 1) s hs
    (fun _ => hX i) (fun _ => zero_le_one)
  simp only [Finset.sum_filter, Finset.univ_unique, Finset.sum_singleton, hi, ite_true,
    mul_one] at h
  rw [one_div_mul_eq_div] at h
  exact h

/-! ## Lemma S: no producer theorem. Spec S follows from Spec M (our proof, not the producer's). -/

theorem specS_of_specM (hM : LemmaM) : LemmaS := by
  intro I _ n X a s mu eta E _ hs hX ha hS4 hS5
  classical
  set W : I → ℝ := fun i => (n i : ℝ) * ((n i : ℝ) - 1) * a i with hW
  have Wnn : ∀ i, 0 ≤ W i := by
    intro i
    have : 0 ≤ (n i : ℝ) * ((n i : ℝ) - 1) := by
      rcases Nat.eq_zero_or_pos (n i) with h0 | hpos
      · simp [h0]
      · have : (1 : ℝ) ≤ n i := by exact_mod_cast hpos
        nlinarith
    exact mul_nonneg this (ha i)
  have hMk := (hM I n X a s hs hX ha).2
  have split : (∑ i, W i) ≤
      (∑ i ∈ Finset.univ.filter (fun i => X i ≤ s * (n i : ℝ) ∧ E i), W i) +
      (∑ i ∈ Finset.univ.filter (fun i => X i > s * (n i : ℝ)), W i) +
      (∑ i ∈ Finset.univ.filter (fun i => ¬ E i), W i) := by
    rw [Finset.sum_filter, Finset.sum_filter, Finset.sum_filter, ← Finset.sum_add_distrib,
      ← Finset.sum_add_distrib]
    apply Finset.sum_le_sum
    intro i _
    have := Wnn i
    split_ifs <;> first | linarith |
      (exfalso; rename_i h1 h2 h3; exact h1 ⟨not_lt.mp h2, h3⟩)
  have hmu : (1 / s) * ∑ i, (n i : ℝ) * X i * a i ≤ mu / s * ∑ i, W i := by
    rw [one_div_mul_eq_div, div_mul_eq_mul_div]
    exact div_le_div_of_nonneg_right hS4 hs.le
  have : (1 - mu / s - eta) * ∑ i, W i =
      (∑ i, W i) - mu / s * (∑ i, W i) - eta * ∑ i, W i := by ring
  rw [this]
  linarith

theorem specS_proved : LemmaS := specS_of_specM bridge_M

end Bridge

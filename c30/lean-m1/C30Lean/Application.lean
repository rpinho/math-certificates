module

public import C30Lean.Majorization
public import Mathlib.Data.Rat.Floor

@[expose] public section

namespace C30Lean

def freeLeaves (m : ℕ) : ℤ := ⌈(555555 : ℚ) * m / 1000000⌉
def emptyBound (m : ℕ) : ℤ := ⌈(185185 : ℚ) * m / 1000000⌉ + 1
def twoCap (m : ℕ) : ℤ := ⌊(7 : ℚ) * m / 50⌋
def stripCount (m : ℕ) : ℤ := (m : ℤ) - freeLeaves m + 1

/-- An explicit sufficient meaning of 'all sufficiently large m' for the
    nonnegative envelope multiplicities in the application: m ≥ 100. -/
theorem application_feasibility (m : ℕ) (hm : 100 ≤ m) :
    0 ≤ emptyBound m ∧ 0 < twoCap m ∧
    twoCap m ≤ 3 * (stripCount m - emptyBound m) - freeLeaves m ∧
    twoCap m ≤ freeLeaves m - stripCount m + emptyBound m := by
  have hm' : (100 : ℚ) ≤ m := by exact_mod_cast hm
  have hL₀ := Int.le_ceil ((555555 : ℚ) * m / 1000000)
  have hL₁ := Int.ceil_lt_add_one ((555555 : ℚ) * m / 1000000)
  have hB₀ := Int.le_ceil ((185185 : ℚ) * m / 1000000)
  have hB₁ := Int.ceil_lt_add_one ((185185 : ℚ) * m / 1000000)
  have hU₀ := Int.floor_le ((7 : ℚ) * m / 50)
  have hU₁ := Int.lt_floor_add_one ((7 : ℚ) * m / 50)
  have hb : (0 : ℚ) ≤ emptyBound m := by
    dsimp [emptyBound]; push_cast; linarith
  have hu : (0 : ℚ) < twoCap m := by dsimp [twoCap]; linarith
  have h1 : (twoCap m : ℚ) ≤ 3 * ((stripCount m : ℚ) - emptyBound m) - freeLeaves m := by
    dsimp [twoCap, stripCount, emptyBound, freeLeaves]; push_cast; linarith
  have h3 : (twoCap m : ℚ) ≤ freeLeaves m - (stripCount m : ℚ) + emptyBound m := by
    dsimp [twoCap, stripCount, emptyBound, freeLeaves]; push_cast; linarith
  exact ⟨by exact_mod_cast hb, by exact_mod_cast hu,
    by exact_mod_cast h1, by exact_mod_cast h3⟩

/-- The precise rational parameters of §5, with no asymptotic feasibility
    assumption left over. The hypotheses on y are still actual strip data. -/
theorem strip_envelope_application (y : List ℤ) (m : ℕ) (hm : 100 ≤ m)
    (hy : ∀ a ∈ y, 0 ≤ a) (hlen : (y.length : ℤ) = stripCount m)
    (hL : y.sum = freeLeaves m)
    (hn0 : emptyBound m ≤ countStrip y 0) (hn2 : countStrip y 2 ≤ twoCap m) :
    ∃ e : StripEnvelope,
      (e.e0 : ℤ) = emptyBound m ∧
      ((e.e2 : ℤ) = twoCap m ∨ (e.e2 : ℤ) = twoCap m - 1) ∧
      (freeLeaves m - y.length + emptyBound m - e.e2) % 2 = 0 ∧
      (e.e1 : ℤ) = (3 * ((y.length : ℤ) - emptyBound m) - freeLeaves m - e.e2) / 2 ∧
      (e.e3 : ℤ) = (freeLeaves m - y.length + emptyBound m - e.e2) / 2 ∧
      ThresholdMajorized e.vector y := by
  obtain ⟨hb, hu, h1, h3⟩ := application_feasibility m hm
  apply strip_envelope y (freeLeaves m) (emptyBound m) (twoCap m)
    hy hL hn0 hn2 hb (le_of_lt hu)
  · intro h; omega
  · simpa only [hlen] using h1
  · simpa only [hlen] using h3

end C30Lean

import Lean.Elab.Term
import Lean.Meta.Closure

/-!
# Banerjee–Smoot, arXiv:2611.09681v1, Conjecture 6.1

A series is its sequence of integer coefficients. Every coefficient operation
below reads only indices at most the output degree. An infinite Euler product
is interpreted by coefficientwise stabilization of its finite partial products.
-/

namespace BanerjeeSmoot

abbrev Series := Nat → Int
abbrev Poly (N : Nat := 54) := Fin (N + 1) → Int

def truncate (N : Nat) (f : Series) : Poly N := fun i => f i.val

/-- Sum over j = 0, ..., last. -/
def sumThrough (term : Nat → Int) : Nat → Int
  | 0 => term 0
  | j + 1 => sumThrough term j + term (j + 1)

/-- Cauchy multiplication modulo q^(N+1). -/
def polyMul {N : Nat} (f g : Poly N) : Poly N := fun k =>
  sumThrough (fun j => f ⟨min j k.val, by omega⟩ *
                        g ⟨k.val - j, by omega⟩) k.val

/-- The multiplicative recurrence for the binomial coefficient n choose j.
Beyond n the falling numerator reaches zero. -/
def binom (n : Nat) : Nat → Nat
  | 0 => 1
  | j + 1 => binom n j * (n - j) / (j + 1)

/-- Coefficients of (1-x)^(-b), including the identity when b=0. -/
def multichoose (b j : Nat) : Nat :=
  match b with
  | 0 => if j = 0 then 1 else 0
  | t + 1 => binom (t + j) j

/-- Row a of Pascal's triangle is obtained from row a-1 by multiplication
by 1+x. These coefficients use addition alone, independently of binom. -/
def pascal : Nat → Nat → Nat
  | 0, 0 => 1
  | 0, _+1 => 0
  | _+1, 0 => 1
  | n+1, j+1 => pascal n j + pascal n (j+1)

private theorem pascal_zero (n : Nat) : pascal n 0 = 1 := by cases n <;> rfl

private theorem pascal_above (n j : Nat) (h : n < j) : pascal n j = 0 := by
  induction n generalizing j with
  | zero => cases j <;> simp_all [pascal]
  | succ n ih =>
    cases j with
    | zero => omega
    | succ j => rw [pascal, ih j (by omega), ih (j+1) (by omega)]

private theorem pascal_adjacent (n j : Nat) :
    pascal n (j+1) * (j+1) = pascal n j * (n-j) := by
  induction n generalizing j with
  | zero => simp [pascal]
  | succ n ih =>
    cases j with
    | zero =>
      have h : pascal n 1 = n := by simpa [pascal_zero] using ih 0
      simp [pascal, pascal_zero, h, Nat.add_comm]
    | succ j =>
      by_cases h : j < n
      · simp only [pascal, Nat.add_mul, Nat.succ_sub_succ_eq_sub]
        rw [ih (j+1), ← ih j, ← Nat.mul_add, ← Nat.mul_add]
        congr 1
        omega
      · have hj : n < j+1 := by omega
        simp [pascal, pascal_above n (j+1) hj, pascal_above n (j+1+1) (by omega),
          Nat.sub_eq_zero_of_le (Nat.le_of_not_gt h)]

/-- The division-based evaluator agrees with repeated multiplication by 1+x. -/
theorem binom_is_pascal (n j : Nat) : binom n j = pascal n j := by
  induction j with
  | zero => simp [binom, pascal_zero]
  | succ j ih =>
    rw [binom, ih, ← pascal_adjacent, Nat.mul_div_cancel _ (by omega)]

/-- Multiplication by 1+x+x²+… takes prefix sums. This is exactly the
recursion from the bth geometric power to the (b+1)st. -/
theorem geometric_power_step (b j : Nat) :
    (multichoose (b+1) j : Int) = sumThrough (fun i => (multichoose b i : Int)) j := by
  induction j with
  | zero => cases b <;> rfl
  | succ j ih =>
    rw [sumThrough, ← ih]
    cases b with
    | zero => simp [multichoose, binom_is_pascal, pascal_above, pascal]
    | succ b =>
      simp only [multichoose, binom_is_pascal]
      rw [show b+1+(j+1) = (b+(j+1))+1 by omega, pascal, show b + 1 + j = b + (j+1) by omega]
      exact Int.natCast_add _ _

/-- Cauchy multiplication by a factor supported at multiples of positive m.
Term j multiplies [q^(k-j*m)] f by [q^(j*m)] of the factor. -/
def strideMul (m : Nat) (weight : Nat → Int) (f : Series) : Series := fun k =>
  sumThrough (fun j => weight j * f (k - j*m)) (k / m)

def mulOnePlusPow (m a : Nat) (f : Series) : Series :=
  strideMul m (fun j => (binom a j : Int)) f

def mulInvOneMinusPow (m b : Nat) (f : Series) : Series :=
  strideMul m (fun j => (multichoose b j : Int)) f

/-- For a negative exponent -s use (1+x)^(-s) = Σ (-1)^j C(s+j-1,j) x^j. -/
def mulSignedPlusPow (m : Nat) (a : Int) (f : Series) : Series :=
  match a with
  | .ofNat s => mulOnePlusPow m s f
  | .negSucc t => strideMul m (fun j => (-1 : Int)^j * multichoose (t+1) j) f

private theorem stride_above (w : Nat → Int) (hw : w 0 = 1) (f : Series)
    {k m : Nat} (h : k < m) : strideMul m w f k = f k := by
  simp [strideMul, Nat.div_eq_of_lt h, sumThrough, hw]

theorem truncation_invariance (f : Series) (a b : Nat) {N m : Nat} (hm : N < m) :
    truncate N (mulOnePlusPow m a f) = truncate N f ∧
    truncate N (mulInvOneMinusPow m b f) = truncate N f := by
  constructor
  · funext k
    exact stride_above _ rfl f (by omega : k.val < m)
  · funext k
    apply stride_above _ _ f (by omega : k.val < m)
    cases b <;> rfl

private theorem signed_above (a : Int) (f : Series) {k m : Nat} (h : k < m) :
    mulSignedPlusPow m a f k = f k := by
  cases a <;> exact stride_above _ rfl f h

def one : Series := fun k => if k = 0 then 1 else 0

/-- Multiply the first M numerator and denominator factors, in ascending order of m. -/
def partialProduct (a : Int) (b : Nat) : Nat → Series
  | 0 => one
  | m + 1 => mulInvOneMinusPow (m+1) b (mulSignedPlusPow (m+1) a (partialProduct a b m))

/-- All partial products from the kth onwards have the same kth coefficient. -/
theorem product_stabilizes (a : Int) (b k M : Nat) (h : k ≤ M) :
    partialProduct a b M k = partialProduct a b k k := by
  induction h with
  | refl => rfl
  | @step M h ih =>
    have hlt : k < M+1 := Nat.lt_succ_of_le h
    let prev := partialProduct a b M
    let num := mulSignedPlusPow (M+1) a prev
    calc
      mulInvOneMinusPow (M+1) b num k = num k :=
        stride_above _ (by cases b <;> rfl) _ hlt
      _ = prev k := signed_above a prev hlt
      _ = _ := ih

/-- The eventual coefficient of the infinite product. -/
def coefficient (a : Int) (b k : Nat) : Int := partialProduct a b k k

theorem finite_product_exact (a : Int) (b N M : Nat) (h : N ≤ M) :
    truncate N (partialProduct a b M) = truncate N (coefficient a b) := by
  funext k
  exact product_stabilizes a b k.val M (by omega)

/-- A row lists the coefficients in order from degree 0 through N. -/
def sample (N : Nat) (f : Series) := (List.range (N+1)).map f

private theorem sumThrough_congr {f g : Nat → Int} (s : Nat)
    (h : ∀ j, j ≤ s → f j = g j) : sumThrough f s = sumThrough g s := by
  induction s with
  | zero => exact h 0 (by omega)
  | succ s ih =>
    simp only [sumThrough]
    rw [ih (fun j hj => h j (by omega)), h (s+1) (by omega)]

/-- Insert the zeros between the coefficients of w(x) when x = q^m. -/
def dilate (m : Nat) (w : Nat → Int) : Series := fun i =>
  if m ∣ i then w (i / m) else 0

private theorem sum_multiples (m : Nat) (v : Nat → Int) (s : Nat) :
    sumThrough (fun i => if m ∣ i then v i else 0) s =
    sumThrough (fun j => v (j*m)) (s/m) := by
  induction s with
  | zero => simp [sumThrough]
  | succ s ih =>
    by_cases h : m ∣ s+1
    · rw [sumThrough, ih, Nat.succ_div_of_dvd h, sumThrough, ite_eq_left h,
          ← Nat.succ_div_of_dvd h, Nat.div_mul_cancel h]
    · rw [sumThrough, ih, ite_eq_right h, Nat.succ_div_of_not_dvd h, Int.add_zero]

/-- The sparse step used in every certificate is exactly the ordinary
truncated Cauchy product, for every input series and every positive stride. -/
theorem stride_is_cauchy (N m : Nat) (hm : 0 < m) (w : Nat → Int) (f : Series) :
    polyMul (truncate N (dilate m w)) (truncate N f) = truncate N (strideMul m w f) := by
  funext k
  let v (i : Nat) := w (i / m) * f (k.val - i)
  calc
    _ = sumThrough (fun i => if m ∣ i then v i else 0) k.val := by
      apply sumThrough_congr
      intro j hj
      simp only [truncate, dilate, Nat.min_eq_left hj, v]
      split <;> simp_all
    _ = sumThrough (fun j => v (j*m)) (k.val/m) := sum_multiples m v k.val
    _ = _ := by
      apply sumThrough_congr
      intro j _
      simp [v, Nat.mul_div_cancel _ hm]

private theorem stride_congr (m : Nat) (w : Nat → Int) {N k : Nat}
    {f g : Series} (h : ∀ i, i ≤ N → f i = g i) (hk : k ≤ N) :
    strideMul m w f k = strideMul m w g k := by
  apply sumThrough_congr
  intro j _
  rw [h (k-j*m) (by omega)]

/-- A certificate row stores its nonnegative coefficients as base-2^128 digits.
Every digit is checked individually, so an oversized proposed coefficient cannot
make a false certificate pass. This encoding is only used for finite witnesses. -/
def digit (row k : Nat) : Int := Int.ofNat ((row >>> (128*k)) % (2^128))

private def pack (row : List Int) := row.foldr (fun x t => x.toNat + (t <<< 128)) 0

def agrees (row : Nat) (f : Series) : Nat → Bool
  | 0 => digit row 0 == f 0
  | k+1 => agrees row f k && digit row (k+1) == f (k+1)

theorem agrees_sound {v : Nat} {f : Series} {N : Nat} (h : agrees v f N = true) :
    ∀ k, k ≤ N → digit v k = f k := by
  induction N with
  | zero =>
    intro k hk
    have : k = 0 := by omega
    subst k
    exact eq_of_beq h
  | succ N ih =>
    obtain ⟨h₀,h₁⟩ := Bool.and_eq_true_iff.mp h
    intro k hk
    by_cases hlt : k ≤ N
    · exact ih h₀ k hlt
    · have : k = N+1 := by omega
      subst k
      exact eq_of_beq h₁

theorem packed_step {a : Int} {b N t prev num den : Nat}
    (hp : ∀ k, k ≤ N → digit prev k = partialProduct a b t k)
    (hn : agrees num (mulSignedPlusPow (t+1) a (digit prev)) N = true)
    (hd : agrees den (mulInvOneMinusPow (t+1) b (digit num)) N = true) :
    ∀ k, k ≤ N → digit den k = partialProduct a b (t+1) k := by
  have hnum (k : Nat) (hk : k ≤ N) :
      digit num k = mulSignedPlusPow (t+1) a (partialProduct a b t) k := by
    rw [agrees_sound hn k hk]
    cases a <;> exact stride_congr _ _ hp hk
  intro k hk
  rw [agrees_sound hd k hk]
  exact stride_congr _ _ hnum hk

private def RowAt (a : Int) (b N t row : Nat) : Prop :=
  ∀ k, k ≤ N → digit row k = partialProduct a b t k

private theorem row_start (a : Int) (b N : Nat) (h : agrees 1 one N = true) :
    ∀ k, k ≤ N → digit 1 k = partialProduct a b 0 k := agrees_sound h

private structure Certificate (a : Int) (b N : Nat) where
  packed : Nat
  correct : ∀ k, k ≤ N → coefficient a b k = digit packed k

private def finish {a : Int} {b N row : Nat}
    (h : ∀ k, k ≤ N → digit row k = partialProduct a b N k) : Certificate a b N :=
  ⟨row, fun k hk => (product_stabilizes _ _ _ _ hk).symm.trans (h k hk).symm⟩

open Lean Elab Term in
/-- Propose the digits and assemble the row proofs.
Each proposed equality has proof term Eq.refl true. The kernel must reduce
both coefficient comparisons itself to accept the enclosing declaration. -/
elab "certified_row% " a:num b:num N:num : term => do
  let degree := N.getNat
  let numerator := a.getNat
  let denominator := b.getNat
  let A := mkApp (mkConst ``Int.ofNat) (mkNatLit numerator)
  let B := mkNatLit denominator
  let N := mkNatLit degree
  let reflTrue := mkApp2 (mkConst ``Eq.refl [.succ .zero]) (mkConst ``Bool) (mkConst ``true)
  let mut prev := 1
  let mut proof := mkAppN (mkConst ``row_start) #[A, B, N, reflTrue]
  for t in [:degree] do
    let m := t+1
    let mid := pack (sample degree (mulOnePlusPow m numerator (digit prev)))
    let den := pack (sample degree (mulInvOneMinusPow m denominator (digit mid)))
    proof := mkAppN (mkConst ``packed_step)
      #[A, B, N, mkNatLit t, mkNatLit prev, mkNatLit mid, mkNatLit den, proof, reflTrue, reflTrue]
    let rowType := mkAppN (mkConst ``RowAt) #[A, B, N, mkNatLit m, mkNatLit den]
    proof ← Meta.mkAuxTheorem rowType proof (cache := false)
    prev := den
  return mkAppN (mkConst ``finish) #[A, B, N, mkNatLit prev, proof]

set_option maxRecDepth 4096 in
private def familyOne : Certificate 36 1 54 := certified_row% 36 1 54
set_option maxRecDepth 4096 in
private def familyTwo : Certificate 40 5 54 := certified_row% 40 5 54
private def ordinary : Certificate 0 1 14 := certified_row% 0 1 14
private def overpartition : Certificate 1 1 6 := certified_row% 1 1 6
private def secondControl : Certificate 2 5 7 := certified_row% 2 5 7

/-- The two coefficient families in §6 of the paper. -/
def p₁ (a : Int) := coefficient a 1
def p₂ (a : Int) := coefficient a 5

/-- The least nonnegative representative of the shift satisfies
24δ ≡ b-a (mod 11^α). Integer arithmetic permits negative right sides. -/
def IsShift (a : Int) (b α δ : Nat) : Prop :=
  δ < 11^α ∧ (24 * (δ : Int) + a - b) % (11 : Int)^α = 0

def ConjecturePartOne : Prop :=
  ∀ (a : Int) (α n δ : Nat), 0 < α →
    (a % 11 = 3 ∨ a % 11 = 5 ∨ a % 11 = 7) → IsShift a 1 α δ →
    p₁ a (11^α * n + δ) % (11 : Int)^((α+1)/2) = 0

def ConjecturePartTwo : Prop :=
  ∀ (a : Int) (α n δ : Nat), 0 < α →
    (a % 11 ≠ 1 ∧ a % 11 ≠ 3 ∧ a % 11 ≠ 5) → IsShift a 5 α δ →
    p₂ a (11^α * n + δ) % (11 : Int)^((α+1)/2) = 0

theorem part1_coefficient : p₁ 36 54 = 62043410886974649205238011198 := by
  exact (familyOne.correct 54 (by decide)).trans (by rfl)

theorem part2_coefficient : p₂ 40 54 = 66134580699742235651549220246110 := by
  exact (familyTwo.correct 54 (by decide)).trans (by rfl)

theorem part1_residue : p₁ 36 54 % 121 = 33 := by rw [part1_coefficient]; decide
theorem part2_residue : p₂ 40 54 % 121 = 55 := by rw [part2_coefficient]; decide

theorem witness_arithmetic :
    (36 : Int) % 11 = 3 ∧ (40 : Int) % 11 = 7 ∧
    (24 * 54 + 35 : Nat) % 1331 = 0 ∧ 11^(3 : Nat) = (1331 : Nat) ∧
    (11 : Nat)^((3+1)/2) = 121 ∧ IsShift 36 1 3 54 ∧ IsShift 40 5 3 54 := by
  unfold IsShift
  decide

theorem negative_controls : p₁ 36 54 % 121 ≠ 0 ∧ p₂ 40 54 % 121 ≠ 0 := by
  rw [part1_residue, part2_residue]
  decide

theorem _root_.banerjee_smoot_conj61_part1_false : ¬ ConjecturePartOne := by
  intro h
  exact negative_controls.1 (h 36 3 0 54 (by decide) (by decide) (by unfold IsShift; decide))

theorem _root_.banerjee_smoot_conj61_part2_false : ¬ ConjecturePartTwo := by
  intro h
  exact negative_controls.2 (h 40 3 0 54 (by decide) (by decide) (by unfold IsShift; decide))

theorem ordinary_partitions :
    sample 10 (coefficient 0 1) = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42] := by
  unfold sample
  calc
    _ = _ := List.map_congr_left (fun k hk => ordinary.correct k (by
      have := List.mem_range.mp hk; omega))
    _ = _ := by rfl

theorem ramanujan_three :
    coefficient 0 1 4 = 5 ∧ coefficient 0 1 9 = 30 ∧ coefficient 0 1 14 = 135 ∧
    coefficient 0 1 (5*0+4) % 5 = 0 ∧ coefficient 0 1 (5*1+4) % 5 = 0 ∧
    coefficient 0 1 (5*2+4) % 5 = 0 := by
  change coefficient 0 1 4 = 5 ∧ coefficient 0 1 9 = 30 ∧ coefficient 0 1 14 = 135 ∧
    coefficient 0 1 4 % 5 = 0 ∧ coefficient 0 1 9 % 5 = 0 ∧ coefficient 0 1 14 % 5 = 0
  rw [ordinary.correct 4 (by decide), ordinary.correct 9 (by decide), ordinary.correct 14 (by decide)]
  decide

theorem overpartitions :
    sample 6 (coefficient 1 1) = [1, 2, 4, 8, 14, 24, 40] := by
  unfold sample
  calc
    _ = _ := List.map_congr_left (fun k hk => overpartition.correct k (by
      have := List.mem_range.mp hk; omega))
    _ = _ := by rfl

/-- The degree-seven congruence for D₂ (Theorem 1.1, derived in the
paper from Theorem 1.2). The shift and exact value are checked as well. -/
theorem theorem12_control : IsShift 2 5 1 7 ∧ p₂ 2 7 = 9185 ∧ p₂ 2 7 % 11 = 0 := by
  unfold p₂ IsShift
  rw [secondControl.correct 7 (by decide)]
  decide

#print axioms binom_is_pascal
#print axioms geometric_power_step
#print axioms stride_is_cauchy
#print axioms truncation_invariance
#print axioms product_stabilizes
#print axioms finite_product_exact
#print axioms agrees_sound
#print axioms packed_step
#print axioms part1_coefficient
#print axioms part2_coefficient
#print axioms part1_residue
#print axioms part2_residue
#print axioms witness_arithmetic
#print axioms negative_controls
#print axioms ordinary_partitions
#print axioms ramanujan_three
#print axioms overpartitions
#print axioms theorem12_control
#print axioms banerjee_smoot_conj61_part1_false
#print axioms banerjee_smoot_conj61_part2_false

end BanerjeeSmoot

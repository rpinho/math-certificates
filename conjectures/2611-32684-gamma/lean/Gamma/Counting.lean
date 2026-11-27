import Std

namespace Gamma

/-- Coefficients in increasing degree order. -/
abbrev Poly := List Int

def eval : Poly → Int → Int
  | [], _ => 0
  | a :: p, x => a + x * eval p x

def plus : Poly → Poly → Poly
  | [], q => q
  | p, [] => p
  | a :: p, b :: q => (a+b) :: plus p q

def scale (a : Int) (p : Poly) : Poly := p.map (a * ·)

def shift : Poly → Poly
  | [] => []
  | a :: p => 0 :: a :: p

theorem eval_shift (p : Poly) (x : Int) : eval (shift p) x = x * eval p x := by
  cases p <;> simp [shift, eval]

def times : Poly → Poly → Poly
  | [], _ => []
  | a :: p, q => plus (scale a q) (shift (times p q))

-- Multiply by the fresh-color factor (X - r).
def linear (r : Nat) (p : Poly) : Poly := plus (scale (-(r : Int)) p) (shift p)

theorem eval_plus (p q : Poly) (x : Int) :
    eval (plus p q) x = eval p x + eval q x := by
  induction p generalizing q with
  | nil => simp [plus, eval]
  | cons a p ih =>
    cases q <;> simp [plus, eval, ih] <;> grind

theorem eval_scale (a : Int) (p : Poly) (x : Int) :
    eval (scale a p) x = a * eval p x := by
  induction p with
  | nil => simp [scale, eval]
  | cons b p ih => simp [scale, eval] at *; grind

theorem eval_times (p q : Poly) (x : Int) :
    eval (times p q) x = eval p x * eval q x := by
  induction p with
  | nil => simp [times, eval]
  | cons a p ih => simp [times, eval_plus, eval_scale, eval_shift, eval, ih]; grind

def deriv (p : Poly) : Poly :=
  p.tail.zipIdx.map fun (a,i) => a * ((i : Int) + 1)

/-- Sum, once per element of Fin n, in any specified additive operation. -/
def over (z : α) (add : α → α → α) : {n : Nat} → (Fin n → α) → α
  | 0, _ => z
  | _+1, f => add (f 0) (over z add (fun i => f i.succ))

abbrev total {n : Nat} (f : Fin n → Int) := over 0 (·+·) f

theorem total_const (a : Int) (n : Nat) : total (n := n) (fun _ => a) = n*a := by
  induction n with
  | zero => simp [total, over]
  | succ n ih => change a + total (n := n) _ = _; rw [ih]; grind

theorem total_mul (f : Fin n → Int) (a : Int) :
    total (fun i => f i * a) = total f * a := by
  induction n with
  | zero => simp [total, over]
  | succ n ih => change f 0 * a + total (fun i => f i.succ * a) = (f 0 + _) * a
                 rw [ih]; grind

private theorem total_replace (f : Fin n → Int) (i : Fin n) (b : Int) :
    total f = total (fun j => if j = i then b else f j) + (f i - b) := by
  induction n with
  | zero => exact i.elim0
  | succ n ih =>
    induction i using Fin.cases with
    | zero => simp [total, over, Fin.succ_ne_zero]; omega
    | succ i =>
      simp only [total, over, Ne.symm (Fin.succ_ne_zero i), Fin.succ_inj]
      have h := ih (fun j => f j.succ) i
      unfold total at h
      simpa [Fin.succ_ne_zero, Ne.symm (Fin.succ_ne_zero i)] using
        (show f 0 + over 0 (·+·) (fun j => f j.succ) =
           f 0 + over 0 (·+·) (fun j => if j = i then b else f j.succ) + (f i.succ-b) by omega)

/-- A sum over named colors plus one common value for all unnamed colors.
The formula also covers an exhausted palette. -/
theorem palette_split (e : Fin r → Fin k) (he : ∀ i j, e i = e j → i = j)
    (f : Fin k → Int) (b : Int) (hb : ∀ x, (∀ i, e i ≠ x) → f x = b) :
    total f = total (fun i => f (e i)) + ((k : Int)-r)*b := by
  induction r generalizing f with
  | zero =>
    have h : f = fun _ => b := funext fun x => hb x (fun i => i.elim0)
    simp [h, total_const, total, over]
  | succ r ih =>
    let g := fun x => if x = e 0 then b else f x
    have hne (i : Fin r) : e i.succ ≠ e 0 := fun h => Fin.succ_ne_zero i (he _ _ h)
    have h := ih (fun i => e i.succ) (fun _ _ h => Fin.succ_inj.mp (he _ _ h)) g (by
      intro x hx
      by_cases h : x = e 0
      · simp [g,h]
      · rw [show g x = f x by simp [g,h]]
        exact hb x (fun i => Fin.cases (Ne.symm h) (fun j => hx j) i))
    have heq : (fun i : Fin r => g (e i.succ)) = fun i => f (e i.succ) :=
      funext fun i => by simp [g, hne]
    rw [heq] at h
    have hh := total_replace f (e 0) b
    change total f = total g + _ at hh
    change total f = (f (e 0) + total (fun i => f (e i.succ))) + _
    grind

theorem eval_over (f : Fin n → Poly) (x : Int) :
    eval (over [] plus f) x = total (fun i => eval (f i) x) := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [over, eval_plus, total]; rw [ih]

end Gamma

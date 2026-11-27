import Dichrom.Polynomial

namespace Dichrom
open Lean.Grind
attribute [local instance] Semiring.natCast
variable {α K : Type} [CommRing K]

structure System (α : Type) where
  ok : List α → Bool
  empty : ok [] = true
  single : ∀ v, ok [v] = true
  down : ∀ {s t}, (∀ a ∈ s, a ∈ t) → ok t = true → ok s = true

theorem splits_left (l : List α) : (l, []) ∈ splits l := by
  induction l <;> simp_all [splits] <;> grind

theorem splits_right (l : List α) : ([], l) ∈ splits l := by
  induction l <;> simp_all [splits] <;> grind

theorem part_one {ok : List α → Bool} {v : α} {t : List α} (h : ok (v::t) = true) :
    [v::t] ∈ parts ok (v::t) := by
  rw [parts]
  apply List.mem_flatMap.mpr
  refine ⟨⟨(t,[]), splits_left t⟩, by simp, ?_⟩
  simp [h, parts]

def mass (p : Blocks α) := (p.map List.length).sum

theorem part_info (ok : List α → Bool) (l : List α) (p : Blocks α) (h : p ∈ parts ok l) :
    mass p = l.length ∧ p.length ≤ l.length ∧ ∀ b ∈ p, 0 < b.length := by
  match l with
  | [] => simp [parts] at h; simp [h, mass]
  | v::t =>
    rw [parts] at h
    obtain ⟨⟨⟨s,r⟩,hs⟩,_,hm⟩ := List.mem_flatMap.mp h
    dsimp at hm
    split at hm
    · obtain ⟨u, hu, rfl⟩ := List.mem_map.mp hm
      obtain ⟨hmass,hlen,hpos⟩ := part_info ok r u hu
      have := split_size hs
      simp_all [mass] <;> omega
    · simp at hm
termination_by l.length
decreasing_by have := split_size hs; simp; omega

theorem split_empty_left (l : List α) (f : List α → K) :
    splitSum l (fun s r => if s.isEmpty then f r else 0) = f l := by
  induction l generalizing f with
  | nil => simp [split_nil]
  | cons a l ih =>
    rw [split_cons]
    simp only [List.isEmpty_cons, Bool.false_eq_true, ite_false, split_zero]
    rw [ih (fun r => f (a::r))]; grind

private theorem erase_empty (l : List α) (f : List α → List α → K) :
    splitSum l f = f [] l + splitSum l (fun s r => keep (!s.isEmpty) (f s r)) := by
  rw [← split_empty_left l (f []), ← split_add]
  apply split_congr; intro s r _
  cases s <;> simp [keep, Semiring.add_zero] <;> grind

private theorem mark_weight (p : Blocks α) (w : List α → K) (z : Nat → K) (j : Nat) :
    mark p (fun b u => z (u.length+1+j) * w b) =
      z (p.length+j) * total p w := by
  induction p generalizing j with
  | nil => simp [total, mark, Semiring.mul_zero]
  | cons a p ih =>
    simp only [mark, total, List.length_cons]
    have e (u : Blocks α) : u.length + 1 + 1 + j = u.length + 1 + (j+1) := by omega
    simp only [e, ih]
    rw [show p.length+1+j = p.length+(j+1) by omega]
    grind

private theorem blocks_balance (p : Blocks α) (ok : List α → Bool) (v : α) (N x : K) :
    total p (fun b => keep (ok (v::b)) (N-x*(b.length:K))) -
      total p (fun b => keep (!(ok (v::b))) (x*(b.length:K)-N)) =
      (p.length:K)*N - x*(mass p:K) := by
  induction p with
  | nil => simp [total, mass]; grind
  | cons b p ih =>
    have e : mass (b::p) = b.length + mass p := by simp [mass]
    simp only [e, total, List.length_cons, Semiring.natCast_add, Semiring.natCast_one]
    have k0 (a : K) : keep false a = 0 := rfl
    have k1 (a : K) : keep true a = a := rfl
    cases ok (v::b) <;> simp only [Bool.not_true, Bool.not_false, k0, k1] <;> grind

/-- Contribution of all forbidden placements of the marked vertex. -/
def correction (A : System α) (v : α) (l : List α) (x : K) :=
  partSum A.ok l fun p => fall x p.length * total p (fun b =>
    keep (!(A.ok (v::b))) (x*(b.length:K)-(l.length:K)))

theorem reindex (A : System α) (v : α) (l : List α) (x : K) :
    x * splitSum l (fun s r => keep (A.ok (v::s))
      (((l.length:K) - x*(s.length:K)) * P A.ok r (x-1))) = correction A v l x := by
  let w (s : List α) := keep (A.ok (v::s)) ((l.length:K)-x*(s.length:K))
  let f (s r : List α) := w s * x * P A.ok r (x-1)
  have start : x * splitSum l (fun s r => keep (A.ok (v::s))
      (((l.length:K) - x*(s.length:K)) * P A.ok r (x-1))) = splitSum l f := by
    rw [← split_mul]; apply split_congr; intro s r _
    dsimp [f,w]; cases A.ok (v::s) <;> simp [keep] <;> grind
  rw [start, erase_empty]
  have marked : splitSum l (fun s r => keep (!s.isEmpty) (f s r)) =
      partSum A.ok l (fun p => mark p (fun b u => fall x (u.length+1) * w b)) := by
    rw [pointing]; apply split_congr; intro s r _
    unfold f P partSum
    rw [← total_mul]
    cases he : s.isEmpty <;> cases ho : A.ok s <;> cases hv : A.ok (v::s) <;>
      simp [he, ho, hv, keep, good, w, fall, total_zero, Semiring.mul_zero, Semiring.zero_mul] <;>
      first | (exfalso; have hh := A.down (s:=s) (t:=v::s) (by intro a ha; simp [ha]) hv; simp_all; done)
            | (apply total_congr; intros; grind)
  rw [marked]
  have e (p : Blocks α) : mark p (fun b u => fall x (u.length+1) * w b) =
      fall x p.length * total p w := mark_weight p w (fall x) 0
  simp only [e]
  unfold correction f P partSum
  rw [← total_mul, ← total_add]
  apply total_congr; intro p hp
  have hmass := (part_info A.ok l p hp).1
  have balance := blocks_balance p A.ok v (l.length:K) x
  rw [hmass] at balance
  have right := fall_right x p.length
  simp only [w, List.length_nil, Semiring.natCast_zero, Semiring.mul_zero, keep, A.single,
    ite_true, Ring.sub_eq_add_neg] at *
  grind

theorem identity3 (A : System α) (v : α) (l : List α) (x : K) :
    (x-1) * H A.ok (v::l) x =
    x^2 * splitSum l (fun s r => keep (A.ok (v::s)) (H A.ok r (x-1))) +
    correction A v l x := by rw [identity2, reindex]

end Dichrom

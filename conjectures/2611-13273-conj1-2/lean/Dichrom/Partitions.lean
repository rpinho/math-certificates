import Std

namespace Dichrom
open Lean.Grind
attribute [local instance] Semiring.natCast

variable {α β γ K : Type} [CommRing K]

def total (l : List α) (f : α → K) : K :=
  match l with
  | [] => 0
  | a :: as => f a + total as f

theorem total_congr {l : List α} {f g : α → K} (h : ∀ a ∈ l, f a = g a) :
    total l f = total l g := by
  induction l with
  | nil => rfl
  | cons a l ih => simp only [total]; rw [h a (by simp), ih (by grind)]

@[simp] theorem total_zero (l : List α) : total l (fun _ => (0 : K)) = 0 := by
  induction l <;> simp_all [total, Semiring.add_zero]

theorem total_add (l : List α) (f g : α → K) :
    total l (fun a => f a + g a) = total l f + total l g := by
  induction l <;> simp_all [total] <;> grind

theorem total_mul (c : K) (l : List α) (f : α → K) :
    total l (fun a => c * f a) = c * total l f := by
  induction l <;> simp_all [total] <;> grind

theorem total_append (l m : List α) (f : α → K) :
    total (l ++ m) f = total l f + total m f := by
  induction l <;> simp_all [total] <;> grind

@[simp] theorem total_map (g : α → β) (l : List α) (f : β → K) :
    total (l.map g) f = total l (fun a => f (g a)) := by
  induction l <;> simp_all [total]

@[simp] theorem total_flatMap (l : List α) (g : α → List β) (f : β → K) :
    total (l.flatMap g) f = total l (fun a => total (g a) f) := by
  induction l <;> simp_all [total, total_append]

/-- Ordered sublist and its complementary sublist, each selection exactly once. -/
def splits : List α → List (List α × List α)
  | [] => [([], [])]
  | a :: l => (splits l).map (fun (s,r) => (a::s,r)) ++
                (splits l).map (fun (s,r) => (s,a::r))

def splitSum (l : List α) (f : List α → List α → K) :=
  total (splits l) fun p => f p.1 p.2

theorem split_nil (f : List α → List α → K) : splitSum [] f = f [] [] := by
  simp [splitSum, splits, total, Semiring.add_zero]

theorem split_cons (a : α) (l : List α) (f : List α → List α → K) :
    splitSum (a::l) f = splitSum l (fun s r => f (a::s) r) +
                        splitSum l (fun s r => f s (a::r)) := by
  simp [splitSum, splits, total_append]

theorem split_congr {l : List α} {f g : List α → List α → K}
    (h : ∀ s r, (s,r) ∈ splits l → f s r = g s r) : splitSum l f = splitSum l g :=
  total_congr fun ⟨s,r⟩ => h s r

theorem split_size {l s r : List α} (h : (s,r) ∈ splits l) :
    s.length + r.length = l.length := by
  induction l generalizing s r with
  | nil => simp [splits] at h; simp [h]
  | cons a l ih =>
    simp [splits] at h
    rcases h with ⟨b,hm,rfl⟩ | ⟨b,c,hm,rfl,rfl⟩ <;> specialize ih hm <;> simp_all <;> omega

@[simp] theorem split_zero (l : List α) : splitSum l (fun _ _ => (0:K)) = 0 := total_zero _

theorem split_add (l : List α) (f g : List α → List α → K) :
    splitSum l (fun s r => f s r + g s r) = splitSum l f + splitSum l g :=
  total_add _ _ _

theorem split_mul (c : K) (l : List α) (f : List α → List α → K) :
    splitSum l (fun s r => c * f s r) = c * splitSum l f := total_mul ..

/-- Interchange the names of two disjoint selected sublists. -/
theorem split_swap (l : List α) (f : List α → List α → List α → K) :
    splitSum l (fun s u => splitSum u (fun b r => f s b r)) =
    splitSum l (fun b u => splitSum u (fun s r => f s b r)) := by
  induction l generalizing f with
  | nil => simp [split_nil]
  | cons a l ih =>
    simp only [split_cons, split_add]
    rw [ih (fun s b r => f (a::s) b r), ih (fun s b r => f s (a::b) r),
        ih (fun s b r => f s b (a::r))]
    grind

abbrev Blocks (α : Type) := List (List α)

/-- The first vertex fixes the first block. Recurse on the complement. -/
def parts (ok : List α → Bool) (l : List α) : List (Blocks α) :=
  match l with
  | [] => [[]]
  | a :: t => (splits t).attach.flatMap fun ⟨(s,r),_hs⟩ =>
      if ok (a::s) then (parts ok r).map ((a::s) :: ·) else []
termination_by l.length
decreasing_by have := split_size _hs; simp; omega

abbrev partSum (ok : List α → Bool) (l : List α) (f : Blocks α → K) := total (parts ok l) f

theorem part_nil (ok : List α → Bool) (f : Blocks α → K) : partSum ok [] f = f [] := by
  simp [partSum, parts, total, Semiring.add_zero]

theorem part_cons (ok : List α → Bool) (a : α) (l : List α) (f : Blocks α → K) :
    partSum ok (a::l) f = splitSum l (fun s r =>
      if ok (a::s) then partSum ok r (fun p => f ((a::s)::p)) else 0) := by
  unfold partSum
  rw [parts]
  simp only [total_flatMap]
  unfold splitSum
  generalize splits l = ps
  induction ps with
  | nil => rfl
  | cons p ps ih =>
    simp only [List.attach_cons, total, total_map] at *
    rcases p with ⟨s,r⟩
    cases h : ok (a::s) <;> simp_all [total, total_map]

end Dichrom

namespace Dichrom
open Lean.Grind
variable {α K : Type} [CommRing K]

def keep (b : Bool) (z : K) : K := if b then z else 0
private theorem keep_add (b : Bool) (z w : K) : keep b (z+w) = keep b z + keep b w := by
  cases b <;> simp [keep, Semiring.add_zero]

theorem keep_swap (a b : Bool) (z : K) : keep a (keep b z) = keep b (keep a z) := by
  cases a <;> cases b <;> rfl

theorem keep_split (b : Bool) (l : List α) (f : List α → List α → K) :
    keep b (splitSum l f) = splitSum l (fun s r => keep b (f s r)) := by
  cases b <;> simp [keep]

def good (ok : List α → Bool) (b : List α) := !b.isEmpty && ok b

/-- Sum over a choice of one block, passing the remaining partition to f. -/
def mark (p : Blocks α) (f : List α → Blocks α → K) : K :=
  match p with
  | [] => 0
  | a::t => f a t + mark t (fun b u => f b (a::u))

theorem pointing (ok : List α → Bool) (l : List α) (f : List α → Blocks α → K) :
    partSum ok l (fun p => mark p f) =
    splitSum l (fun b r => keep (good ok b) (partSum ok r (f b))) := by
  match l with
  | [] => simp [part_nil, split_nil, mark, good, keep]
  | v::t =>
    rw [part_cons, split_cons]
    change splitSum t (fun a r => keep (ok (v::a)) (partSum ok r (fun p =>
        f (v::a) p + mark p (fun b u => f b ((v::a)::u))))) = _
    have addP (r : List α) (g h : Blocks α → K) : partSum ok r (fun p => g p + h p) = partSum ok r g + partSum ok r h := total_add ..
    simp only [addP, keep_add, split_add]
    congr 1
    calc
        _ = splitSum t (fun a r => splitSum r (fun b u =>
              keep (good ok b) (keep (ok (v::a)) (partSum ok u (fun p => f b ((v::a)::p)))))) := by
                apply split_congr; intro a r hr
                rw [pointing ok r, keep_split]
                apply split_congr; intros; apply keep_swap
        _ = _ := by
                rw [split_swap]
                apply split_congr; intro b r _
                rw [part_cons, keep_split]
                rfl
termination_by l.length
decreasing_by have := split_size hr; simp; omega

end Dichrom

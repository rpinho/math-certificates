import Dichrom.Counting

namespace Dichrom

structure Digraph (n : Nat) where
  arc : Fin n → Fin n → Bool
  loopless : ∀ v, arc v v = false

/-- Successor along a cyclically ordered (nonempty) tuple. -/
def around (i : Fin (k+1)) : Fin (k+1) :=
  if h : i.val+1 < k+1 then ⟨i.val+1,h⟩ else 0

/-- A simple directed cycle of arbitrary positive length inside s. -/
def Digraph.Cyclic (D : Digraph n) (s : List (Fin n)) : Prop :=
  ∃ k, ∃ f : Fin (k+1) → Fin n, (List.ofFn f).Nodup ∧
    ∀ i, f i ∈ s ∧ D.arc (f i) (f (around i)) = true

private def isCycle (D : Digraph n) (s : List (Fin n)) (k : Nat) (f : Fin (k+1) → Fin n) :=
  decide (List.ofFn f).Nodup && (List.finRange (k+1)).all (fun i =>
    s.contains (f i) && D.arc (f i) (f (around i)))

def Digraph.acyclic (D : Digraph n) (s : List (Fin n)) : Bool :=
  !(List.finRange n).any (fun k => (maps (List.finRange n) (k.val+1)).any (isCycle D s k.val))

theorem Digraph.acyclic_false (D : Digraph n) (s : List (Fin n)) :
    D.acyclic s = false ↔ D.Cyclic s := by
  simp only [Digraph.acyclic,Bool.not_eq_false',List.any_eq_true,isCycle,
    Bool.and_eq_true,decide_eq_true_eq,List.all_eq_true,List.contains_iff_mem]
  constructor
  · rintro ⟨k,_,f,_,hf,h⟩
    exact ⟨k.val,f,hf,fun i => h i (List.mem_finRange i)⟩
  · rintro ⟨k,f,hf,h⟩
    have bound := hf.length_le_of_subset (l₂:=List.finRange n) (fun a _ => List.mem_finRange a)
    simp only [List.length_ofFn,List.length_finRange] at bound
    exact ⟨⟨k,by omega⟩,List.mem_finRange _,f,maps_complete f,hf,fun i _ => h i⟩

theorem Digraph.acyclic_iff (D : Digraph n) (s : List (Fin n)) :
    D.acyclic s = true ↔ ¬ D.Cyclic s := by
  rw [← D.acyclic_false]; cases D.acyclic s <;> decide

def Digraph.system (D : Digraph n) : System (Fin n) where
  ok := D.acyclic
  empty := (D.acyclic_iff _).mpr (by
    rintro ⟨k,f,_,h⟩; have := (h 0).1; simp at this)
  single v := (D.acyclic_iff _).mpr (by
    rintro ⟨k,f,_,h⟩
    have hv (i) : f i = v := by simpa using (h i).1
    have := (h 0).2
    rw [hv,hv,D.loopless] at this
    contradiction)
  down := by
    intro s t h ha
    apply (D.acyclic_iff _).mpr
    rintro ⟨k,f,hf,he⟩
    exact ((D.acyclic_iff _).mp ha) ⟨k,f,hf,fun i => ⟨h _ (he i).1,(he i).2⟩⟩

/-- A colour map stated directly on vertex labels. -/
def properColoring (A : System (Fin n)) (x : Nat) (f : Fin n → Fin x) :=
  (List.finRange x).all (fun c => A.ok ((List.finRange n).filter (fun v => f v == c)))

private theorem fibres_on_vertices (A : System (Fin n)) (x : Nat)
    (f : Fin (List.finRange n).length → Fin x) :
    proper A (List.finRange x) (fibres (List.finRange n) f) =
      properColoring A x (fun v => f (Fin.cast (List.length_finRange).symm v)) := by
  unfold proper properColoring
  apply Bool.eq_iff_iff.mpr
  simp only [List.all_eq_true]
  have mem (v : Fin n) (c : Fin x) :
      v ∈ fibres (List.finRange n) f c ↔
      v ∈ (List.finRange n).filter (fun w => f (Fin.cast List.length_finRange.symm w) == c) := by
    rw [mem_fibres]
    simp only [List.mem_filter,List.mem_finRange,true_and,beq_iff_eq]
    constructor
    · rintro ⟨i,hi,h⟩
      have e : Fin.cast List.length_finRange.symm v = i := by
        apply Fin.ext; simp [← hi]
      rwa [e]
    · intro h
      exact ⟨Fin.cast List.length_finRange.symm v,by simp,h⟩
  constructor <;> intro h c hc
  · exact A.down (fun w hw => (mem w c).mpr hw) (h c hc)
  · exact A.down (fun w hw => (mem w c).mp hw) (h c hc)

theorem direct_count (A : System (Fin n)) (x : Nat) :
    (polynomial A.ok (List.finRange n)).eval (x:Int) =
      (((maps (List.finRange x) n).filter (properColoring A x)).length : Int) := by
  rw [eval_eq_coloring_count]
  simp only [fibres_on_vertices]
  have transport (m : Nat) (hm : m = n) :
      ((maps (List.finRange x) m).filter (fun f =>
        properColoring A x (fun v => f (Fin.cast hm.symm v)))).length =
      ((maps (List.finRange x) n).filter (properColoring A x)).length := by
    subst m; rfl
  exact congrArg (fun k : Nat => (k:Int)) (transport _ List.length_finRange)

end Dichrom

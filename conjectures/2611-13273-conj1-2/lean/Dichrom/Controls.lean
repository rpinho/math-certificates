import Dichrom.Theorems

namespace Dichrom.Controls
open Dichrom

def cycle3 : Digraph 3 where
  arc i j := j.val == (i.val+1)%3
  loopless := by decide +kernel

def complete (n : Nat) : Digraph n where
  arc i j := i != j
  loopless v := by simp

def empty (n : Nat) : Digraph n where
  arc _ _ := false
  loopless _ := rfl

private def sizes (D : Digraph n) := (parts D.acyclic (vertices n)).map List.length

private theorem cycle3_sizes : sizes cycle3 = [2,2,2,3] := by decide +kernel
private theorem complete3_sizes : sizes (complete 3) = [3] := by decide +kernel
private theorem complete4_sizes : sizes (complete 4) = [4] := by decide +kernel

private theorem by_sizes (D : Digraph n) (x : Rat) :
    P D.acyclic (vertices n) x = total (sizes D) (fall x) ∧
    dP D.acyclic (vertices n) x = total (sizes D) (dfall x) := by
  simp [P,dP,partSum,sizes]

theorem oriented_triangle (x : Rat) :
    P cycle3.acyclic (vertices 3) x = x^3-x ∧ H cycle3.acyclic (vertices 3) x = 2*x := by
  have ⟨p,d⟩ := by_sizes cycle3 x
  simp only [cycle3_sizes,total,fall,dfall] at p d
  simp only [H,vertices,List.length_finRange] at *
  grind

theorem bidirected_triangle (x : Rat) :
    P (complete 3).acyclic (vertices 3) x = x*(x-1)*(x-2) ∧
    H (complete 3).acyclic (vertices 3) x = 3*x^2-4*x := by
  have ⟨p,d⟩ := by_sizes (complete 3) x
  simp only [complete3_sizes,total,fall,dfall] at p d
  simp only [H,vertices,List.length_finRange] at *
  grind

theorem bidirected_four (x : Rat) :
    P (complete 4).acyclic (vertices 4) x = x*(x-1)*(x-2)*(x-3) ∧
    H (complete 4).acyclic (vertices 4) x = 6*x^3-22*x^2+18*x := by
  have ⟨p,d⟩ := by_sizes (complete 4) x
  simp only [complete4_sizes,total,fall,dfall] at p d
  simp only [H,vertices,List.length_finRange] at *
  grind

theorem triangle_sharpness : H (complete 3).acyclic (vertices 3) (1:Rat) = -1 := by
  rw [(bidirected_triangle 1).2]; grind

end Dichrom.Controls

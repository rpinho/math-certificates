import Std.Tactic.BVDecide.LRAT.Checker
import Std.Tactic.BVDecide.LRAT.Parser

open Std.Sat Std.Tactic.BVDecide

def dimacs (file : System.FilePath) : IO (CNF Nat) := do
  let h ← IO.FS.Handle.mk file .read
  let header := ((← h.getLine).trimAscii.toString.splitOn " ")
  let ["p", "cnf", vars, count] := header | throw (IO.userError "invalid DIMACS header")
  let some nv := vars.toNat? | throw (IO.userError "variable count")
  let some nc := count.toNat? | throw (IO.userError "clause count")
  let mut clauses := Array.emptyWithCapacity nc
  for _ in [:nc] do
    let tokens := (← h.getLine).trimAscii.toString.splitOn " "
    let "0" :: rev := tokens.reverse | throw (IO.userError "unterminated clause")
    let mut lits := []
    for tok in rev do
      let some z := tok.toInt? | throw (IO.userError "literal")
      if z == 0 || z.natAbs > nv then throw (IO.userError "literal out of bounds")
      lits := (z.natAbs - 1, decide (z > 0)) :: lits
    clauses := clauses.push (.ofLiterals lits)
  if !(← h.getLine).isEmpty then throw (IO.userError "data after clauses")
  return ⟨clauses⟩

def main (args : List String) : IO Unit := do
  let [formula, certificate] := args | throw (IO.userError "expected DIMACS and LRAT")
  let cnf ← dimacs formula
  let proof ← LRAT.loadLRATProof certificate
  if LRAT.check proof cnf then
    IO.println s!"VERIFIED {cnf.clauses.size} clauses, {proof.size} actions (Std LRAT.check_sound)"
  else throw (IO.userError "LRAT rejected")

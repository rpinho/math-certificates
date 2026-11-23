import Comparator
import Export.Parse
import Lean

/-- Run the pinned comparator's own comparison and axiom functions on two local exports. -/
def main (args : List String) : IO Unit := do
  let [cfgFile, refFile, solFile] := args | throw (IO.userError "expected config, challenge, solution")
  let cfg ← IO.ofExcept <| Lean.Json.parse (← IO.FS.readFile cfgFile)
  let targets ← IO.ofExcept <| cfg.getObjValAs? (Array String) "theorem_names"
  let axioms ← IO.ofExcept <| cfg.getObjValAs? (Array String) "permitted_axioms"
  let readExport (path : System.FilePath) := do
    Export.parseStream <| IO.FS.Stream.ofHandle (← IO.FS.Handle.mk path .read)
  let ref ← readExport refFile
  let sol ← readExport solFile
  let names := targets.map String.toName
  let allowed := axioms.map String.toName
  IO.println s!"read {ref.constMap.size} challenge and {sol.constMap.size} solution declarations"
  let primitives := #[``Nat.zero, ``Nat.succ, ``Nat.add, ``Nat.sub, ``Nat.mul, ``Nat.div,
    ``Nat.mod, ``Nat.pow, ``Nat.gcd, ``Nat.beq, ``Nat.ble, ``Nat.land, ``Nat.lor,
    ``Nat.xor, ``Nat.shiftLeft, ``Nat.shiftRight, ``String.ofList, ``Char.ofNat, ``List, ``eagerReduce]
  IO.ofExcept <| Comparator.compareAt ref sol (names ++ allowed) #[] primitives
  IO.println s!"Comparator.compareAt passed for {names.size} theorems"
  IO.ofExcept <| Comparator.checkAxioms sol names #[] allowed
  IO.println "Comparator.checkAxioms passed"
  -- The pinned driver's runKernel removes these three constants before replay.
  let decls := sol.constMap.erase `Quot.mk |>.erase `Quot.lift |>.erase `Quot.ind
  discard <| (← Lean.mkEmptyEnvironment).replay decls
  IO.println "Lean kernel replayed the exported proof closure from an empty environment"

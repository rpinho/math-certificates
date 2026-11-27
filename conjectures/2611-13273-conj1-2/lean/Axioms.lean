import Dichrom
import Lean.Elab.Print

open Lean Elab Command

-- Inspect the compiled environment so new public theorems are included automatically.
run_cmd do
  let env ← getEnv
  let mut names := #[]
  for mod in env.header.moduleNames, data in env.header.moduleData do
    if `Dichrom |>.isPrefixOf mod then
      for name in data.constNames, info in data.constants do
        if (`Dichrom |>.isPrefixOf name) && info.isTheorem then names := names.push name
  names := names.qsort Name.lt
  for name in names do
    let used ← collectAxioms name
    for dep in used do
      unless #[`propext, `Classical.choice, `Quot.sound].contains dep do
        throwError "{name} depends on unexpected constant {dep}"
    elabCommand (← `(#print axioms $(mkIdent name)))
  logInfo m!"Checked {names.size} public theorem declarations in Dichrom."

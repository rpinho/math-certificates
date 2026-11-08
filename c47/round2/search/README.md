# Selected producer search sources

These are our own numerical source files, not Tomar or Doldrums code. The final snapshot is retained to document the selected rational measure. The exact frozen certificate in ../certificates/final.json, rather than a numerical search replay, is the asserted artifact. Numerical search uses periodic atom moves, mass rebalancing, insertions and removals, then reflection and joint polishing. This extends the published measure and method rather than proposing a distinct construction principle.

objective.py compiles and calls evaluator.cpp; NumPy/SciPy are required for search and the utility modules. certify.py and final_one.py make rectangle witnesses at dyadic radius precision. Some original orchestration scripts are omitted because they encode machine-specific search schedules; this selection documents the method and does not promise reproduction of the original stochastic trajectory. Exact verification from the release root is self-contained and uses only the standard library.

To regenerate witnesses from the final snapshot, compile the library in this folder, then run from the release root. The output path below is created by this optional command:

```sh
python3 search/final_one.py search/final-snapshot.json release_validation/rebuilt.json --bits 48
```

The script calls the release-root exact verifier. This numerical regeneration is optional; witness selection and ordering may change tiny final digits. The archived certificate remains authoritative. Search-chain launchers also expect their historical starting certificates and diagnostic logs; these are not required for this final-snapshot regeneration or the bound replay.

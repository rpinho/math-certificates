# SAT coverage

Each main certificate covers one entire CNF. There was no cube split, so a separate proof for a cube cover does not apply.

| Order | Threshold \(K\) | Families | Piece |
| --- | ---: | --- | --- |
| 8 | 3 | Original | runs/n8/formula.cnf.gz |
| 10 | 4 | Original + FAN | runs/n10-fan/formula.cnf.gz |
| 12 | 5 | Original + FAN | runs/n12-fan/formula.cnf.gz |

The only reduction is the minimum-side normalization proved in [PROOFS.md](PROOFS.md). For every model of the unbroken formula, its restriction to boundary-edge lengths is one of the total preorders traversed by `verify_inputs.py`, regardless of \(K\). The script tests the actual SYM literals under dihedral images. The enumeration visits 13, 75, 541, 4,683, 47,293 and 545,835 projected preorders for orders 3 through 8. [Enumeration log](runs/fan_verify_inputs.log).

BISECTOR and CROSS supply identical clauses. Their individual omission at n=12 was checked by rebuilding both canonical encodings and comparing each against the certified input SHA-256. Each ablation reuses that input's exact proof and core, with its own core provenance.

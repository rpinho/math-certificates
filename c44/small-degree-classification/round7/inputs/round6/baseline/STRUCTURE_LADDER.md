# What the stronger minimum-support theorem changes

All count budgets in this note concern the all-local-degrees-d extremal
reduction in PROOF.md. They are not asserted for an arbitrary mixed-local-
degree function with the same derivative shape.

Valyuzhenich's classification gives more than the old 2(d-1) control bound.
Write r for the number of fixed input coordinates in the point indicator,
and let each nontrivial block of size m consume degree m-1. Its type is phi_m
for even m, psi_m for odd m. Thus all types at derivative degree k=d-1 are
exactly the integer partitions of k-r into these positive degree costs.

At degree four the complete list is:

|fixed r|nontrivial factors|controls|minimum-case count ceiling|
|--:|--|--:|--:|
|3|none|3|21|
|2|phi_2|4|22|
|1|psi_3|4|22|
|1|phi_2 phi_2|5|23|
|0|phi_4|4|22|
|0|phi_2 psi_3|5|23|
|0|phi_2 phi_2 phi_2|6|24|

These integers follow from floor(h+1+14*(5/4)). The no-minimum branch has
ceiling 21. Since the known construction has 22 variables, every extremal
quartic has a minimum derivative. If R4=24, every minimum derivative in an
extremizer must have the last type, up to the symmetries in the theorem.
This isolates the precise remaining case for reducing c4 from 3/2 to 23/16.

Likewise, at degree five the worst minimum-case ceiling is 54; every type
except phi_2^4 has ceiling at most 53, as does the no-minimum branch. Thus
R5=54 could occur only with that exceptional minimum-derivative type.
This is a necessary condition, not an existence assertion or an exclusion.

The frozen structure_cases.json enumerates all 113 types at degrees four
through eight. verify_structure_cases.py independently enumerates block
multiplicities, verifies completeness and checks every exact rational budget.
The worst minimum-case ceilings are 24,54,115,265,606; every nonexceptional
type saves at least one count. The full phi_2 product witnesses show why the
classification cannot lower the worst control count by itself. The global
improvement here combines its safe restriction budget with the stronger
Reed–Muller gap and sequentially improved lower-degree caps.

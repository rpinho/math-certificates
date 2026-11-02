# C44 < 2.1974348818: control sets and Reed-Muller weights

Unrefereed. This certifies an upper bound on C44, the constant in the relevant-variable bound r(f) <= C 2^deg(f), Tao table [44a](https://teorth.github.io/optimizationproblems/constants/44a.html). No human expert has reviewed it line by line. Please read it with suspicion: it's a very large move for an elementary argument.

    C44 < 174098727923678791596986402933 / 79228162514264337593543950336 < 2.1974348818

It improves the 3.9819073803 in [`../local-degree-caps/`](../local-degree-caps/). The lower bound is 1.5.

## The idea

For a ternary polynomial A of real degree at most k, with support density p and h relevant coordinates, the support lemma and Fourier energy give h <= floor(k p 2^(k+1)). Applied to a Boolean derivative, fixing those controls lowers the degree on every branch and leaves a signed dictator on the active ones. The Kasami-Tokura spectrum of Reed-Muller weights below twice the minimum then cuts the case analysis to finitely many exact cases. That gives count ceilings R4 <= 24, R5 <= 54, R6 <= 119, R7 <= 254, R8 <= 528, and the caps feed the Chiarelli-Hatami-Saks identity and Wellens's recurrence. The block-sensitivity inputs are no longer active.

## What's here

- `PROOF.md`: the written proof. The verifiers check the arithmetic, not these lemmas.
- `caps.json`, `candidate.json`: the exact inputs. `generate.py` and `analyze.py` produce them.
- `check_a.log`, `check_b.log`, `verification_a.json`, `verification_b.json`, `FINAL_RECEIPT.json`: both exact implementations and their receipts.
- `control_boolean.cpp`, `control_ternary.cpp`, `control_corruption.py`: finite controls and corruption tests.
- `KTA_AUDIT.md`: how the Kasami-Tokura-Azumi tables were used.
- `CORRECTIONS.md`: two wording defects a referee found in `PROOF.md`. Read this with the proof.
- `review/`: separate AI reviews and a hostile AI referee.

## What this doesn't show

Separate AI reviews passed every step, recomputed the bound with their own code, and ran the argument at d = 2 and 3, getting R2 <= 4 and R3 <= 11, consistent with the exact values. A separate proof gives R4 = 22, and its caps are compatible. The hostile referee found no false step and put the chance that a human referee finds a fatal error at 10%. All of that is AI, so none of it is a second party. The recursion is a short proof of the O(2^d) theorem without block sensitivity, so it may already exist.

The cited theorems are used, not reproved: Kasami-Tokura, R3 <= 10 and the published recurrence. Parts of the 1970s sources were not available in full, as `KTA_AUDIT.md` says. This relaxation ends near 2.1974, and no priority or optimality is claimed.

## Credit

Chiarelli, Hatami and Saks for the weighted framework, including the corrected duplication in Chiarelli's thesis. Wellens for the recurrence, Kasami, Tokura and Azumi for the weight spectra, and Valyuzhenich for the structure of minimum-influence functions.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificate, verifiers and this text. This does not claim a line-by-line human verification.

# C31b: h=9 lower bound with fixed-point unit 2^-30

Candidate, unrefereed:

    gamma_4 >= 3835447842/6212691217 > 0.617356908308.

This refines Leandre Jack's construction in [PR #272](https://github.com/teorth/optimizationproblems/pull/272).
The gain comes from the finer fixed-point unit, 2^-30 instead of 2^-27.
The operator, h=9 and set of 1,431,743,147 classes are the same as in #272.
This is a precision refinement of Jack's construction, not a new method.

The exact gain over Jack's stated 14982218/24268325 is
570425344/150771609578801525, about 3.7834e-9. His exact witness may
support a higher value, so the gain over that witness may be smaller.
Both values have the same six-place floor, 0.617356.

## What's here

- `PROOF_C31_LOWER.md`, `CONCENTRATION_DETAILS.md`: the analytic reduction and concentration details.
- `VALUE_PROOF.md`, `comparison.json`: exact fractions, rounding and comparison scope.
- `c31_lower_table.c`, `decode_c31_lower.py`, `packet.json`: the procedural certificate and pinned vector hashes.
- `verify_c31_lower.c`, `verify_c31_lower.py`: the separately written (same agent) literal-operator checker and wrapper.
- `check_value.py`, `check_controls.py`: value arithmetic and small-state positive/negative controls.
- `verification.json`, `decoder_replay.json`, `decoder_byte_cmp.json`: historical full h=9 receipts from the frozen packet.
- `controls.json`, `controls.log`: original small-state controls; `receipts/`: fresh release checks and source evidence.
- `REPRODUCE.md`, `MANIFEST.json`, `SHA256SUMS`: commands, resource needs and release integrity hashes.

## Reproduce

Needs Python 3 (standard library), a C11 compiler with pthreads and a
little-endian host. Run from this folder:

```sh
nice -n 10 python3 check_controls.py
nice -n 10 python3 check_value.py --receipt verification.json
```

These take seconds locally. Full h=9 reconstruction and checking need
about 80 GB RAM, at least 13 GB temporary disk and roughly two hours on
the original shared CPU pod. The decoded potential is 11,453,945,176 bytes;
it is rebuilt from the recipe, rather than stored here. See REPRODUCE.md.

## Verification status

The frozen receipt reports all 1,431,743,147 h=9 classes checked, with
minimum numerator 7,670,895,684 over 17,179,869,184. It is historical
evidence supplied by the producing agent. This release reran only h=5,
controls and value arithmetic. No h=9 vector was rebuilt or checked here.
Source edits are comments only. Original hash-referenced files survive
under `.orig` names; the h=9 receipt was not rewritten. REPRODUCE.md maps
its hashes to those originals and explains the new package hashes.

Two AI reviews found no false mathematical step in their stated scope.
One accepted the candidate; the other flagged filing a PR because the gain
is a precision refinement. Neither replayed the full h=9 check. Their
small-h checks and code review do not replace that replay. Not refereed;
no priority or optimality claim is made.

## Credit

Jack's source is credited at exactly the commit linked by #272:
[bb3b815](https://github.com/leandrejack-afk/chvatal-sankoff-bound/tree/bb3b815/lower),
full SHA `bb3b815c72c4f4cf84fe15be9a7ab06141c70f44`.
The frozen packet instead cited later HEAD `574220ee90b332181ba8f8eccf500c380c0f78bb`.
The lower source, README and h=9 logs are byte-identical at both commits.

The reduction is [Lueker (2009), Lemma 2.3](https://mathematicaster.org/teaching/lcs22/lueker_lcs.pdf).
The k-letter method, including the four-letter setting here, is due to
[Kiwi and Soto (2009)](https://doi.org/10.1017/S0963548309009900), and was
also used by [Rosenfeld (2024)](https://arxiv.org/abs/2407.18113).
The proof rederives the implication for general k. See also
[Heineman et al. (2024)](https://arxiv.org/abs/2407.10925) for earlier four-letter bounds.

## AI use

Written and checked by AI agents under Ricardo Pinho's direction.
The checker was separately written (same agent); two AI reviews were
supplied. This does not claim human line-by-line verification. Not refereed.

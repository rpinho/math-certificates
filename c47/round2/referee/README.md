# Clean-room AI referee

GPT-6 Astra via Codex wrote its own checks after reading the supplied mathematical prose, certificate and finite-instance data, plus earlier referee reports. It did not read or run the producer’s code. The checker uses Python integers and fractions.Fraction; Decimal is used only for display.

It checked the definition against Tao page 47a, Tomar’s Lemma 6.2 and Lin’s truncation-and-smearing argument; all atom locations, positivity and distinctness; every periodic box mass, strict radius and rectangle containment; exact rectangle-union area and ratio; finite block retention and all smearing inequalities; decimal truncation; and the half-open atomic cell correction. Its verdict is **HOLDS**, with no mathematical caveats among the requested checks. It does not establish optimality, search completeness, exact superlevel-set area, an upper bound, or exhaustive priority.

This is a commissioned clean-room AI referee on a different model using its own checks, **an AI referee and not a human review**. It supplies no basis by itself to remove Tao’s asterisk. The underlying clean-room attestations are historical statements from the supplied referee report, not facts authenticated by file hashes.

Run `python3 independent_check.py` from this folder without disabling assertions. The checker and its certificate and finite-receipt inputs are byte-identical to those supplied by the referee. Release editing only made report citations portable and changed review wording. The original producer proof read by the referee is preserved in [sources/producer-proof.md](sources/producer-proof.md); the release [proof](../PROOF.md) adds corrections and updated review attribution without changing the argument. Fresh JSON output is copied into [../release_validation/](../release_validation/).

## Release edits and generated output

The Tomar link in REFEREE.md was changed only as a citation: it now cites the [Zenodo record](https://doi.org/10.5281/zenodo.23716077), v5, Lemma 6.2, Section 6. Its mathematical text and conclusions are unchanged. Source redistribution decisions, attribution, removed manuscript extracts and their original SHA-256 hashes are listed in [sources/SOURCES.md](sources/SOURCES.md).

Running the checker from this folder regenerates the per-witness TSV with all 1500 witness rows:

```sh
python3 independent_check.py  # regenerates witness_results.tsv
```

That regenerable TSV and its duplicate under the release validation folder are deliberately omitted from the public packet because rational-number digit runs trigger the publication scanner. The original SHA-256 of **both** copies is `9314c749c0e73db083b290f8b0b986ed3d0179ac395af914cd00de9df729f54d`. Existing TSV references in REFEREE.md refer to this regenerated output. After a local replay, inspect the output locally and remove it before publishing:

```sh
/usr/bin/trash witness_results.tsv
```

The checker, certificate, finite receipt and saved producer proof remain unchanged.

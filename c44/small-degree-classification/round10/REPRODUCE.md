# Round ten reproduction — candidate, unrefereed

Use `frozen_final/PROOF.md` for R7 <= 229 and C44 < 2.0111998311.
The first-stage `frozen/` packet alone gives 2.0114439717.
The release's fresh exact check was:

```sh
nice -n 10 python3 -B frozen_final/verify_a.py frozen_final
```

It checks the sign-completion inputs and all rational propagation rows.
Historical first-stage/final receipts and both reviews are included.
The following original commands run the full checks on Linux:

```sh
nice -n 10 python3 -B frozen/replay.py --workers 4 --replay
nice -n 10 python3 -B frozen_final/replay.py
```

The first command also replays the copied round-nine baseline and its
inherited inputs. The second checks the baseline receipt, sign controls,
both final verifiers and 40 rejection combinations. `frozen_lower/` and
`frozen_controls/` retain the separate lower/known-count seed controls.

Use Python >= 3.10 (the acceptance programs use `int.bit_count()`), the
standard library and a C++17 compiler. Python 3.12.13 was used for this
release. Run at nice 10; keep native numerical libraries single threaded.
No search logs or compiled binaries are required as inputs.

Check the distributed hashes **before** replay:

```sh
shasum -a 256 -c SHA256SUMS
```

Replay writes mutable receipts and build outputs next to the frozen
packets. Those outputs will differ from the distributed receipt hashes
after a new run; the frozen inputs must continue to match their manifests.
The historical REPORT.md describes the original research job. Commands
in that report for unshipped exploratory `jobs/` scripts are historical;
the acceptance commands below apply to this release.

The release omits compiled binaries, caches, large search logs, downloaded
papers and public-source snapshots. It keeps the exact cubic catalogue,
compressed template bank, certificate files and construction controls
consumed by replay. Source URLs and named premises remain in the proofs.
Full-wrapper replay on macOS has an inherited R4 `RLIMIT_AS` problem,
documented by the supplied Astra review; running the underlying checks
or using Linux avoids that wrapper issue. No numerical algorithm was
changed to address it in this packaging job.

All own checkers are separately written (same agent). Their finite
agreement does not establish the external universal mathematical premises.
See INPUT_ERRATA.md for Q != 0 and the existing round-eight 201/4 erratum.

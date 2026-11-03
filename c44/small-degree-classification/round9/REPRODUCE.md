# Round nine reproduction — candidate, unrefereed

The frozen packet proves R6 <= 107 and C44 < 2.0209645587. The release's
fresh exact check was:

```sh
nice -n 10 python3 -B frozen/verify_packet_a.py frozen
```

This checks canonical coverage of all 189 case files and the rational
propagation; it does **not** rerun the 189 native exclusion searches.
Their historical PASS receipt and compressed receipts are included.
Both supplied reviews describe earlier exact replays, including all
378 native checker/case combinations in Astra's review.

Full original acceptance replay on Linux (including inherited checks,
compilation, both 189-case searches and all rejection controls):

```sh
nice -n 10 python3 -B frozen/replay.py --workers 4 --replay
```

The 189-case ceiling h <= 13 at (6, 7/4) and the inherited round-seven
quintic ceiling h <= 12 at (6, 3/2) are both load-bearing. Copied inputs
are retained under `frozen/inputs/round8/`.

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

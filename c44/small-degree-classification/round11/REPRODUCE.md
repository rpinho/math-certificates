# Round eleven reproduction — candidate, unrefereed

Final packet: `frozen_parity/PROOF.md`; predecessor: `frozen_accepted/`.
The candidate is R7 <= 227, R8 <= 474 and C44 < 1.9916994577, with lower
bound 3/2. The exact rational is
39449672077327653986659243787/19807040628566084398385987584.

The release's fresh full final replay was:

```sh
nice -n 10 python3 -B frozen_parity/replay.py
```

It compiles two C++17 sources, runs A and B on the 15 parity cases,
retains both minimum-product positive controls, checks both scalar
implementations and their weaker-claim controls, and requires 120
artifact rejections (96 scalar/dependency plus 24 partial-artifact).
At most four workers run concurrently. The release does not rerun the
round-seven classification or the round-nine native exclusion searches.

The original round-ten and accepted-predecessor receipts were restored
from the supplied archives; their manifest references were updated for
the packaged copies, after wording-only fixes and allowed omissions.
This changes packaging identities, not mathematical certificate bytes
or historical verification scope. Original receipt bytes are preserved
in the compressed archives; the job's private provenance folder retains
verbatim final receipts as well. The final parity receipt is fresh.

To rerun the accepted predecessor on its own:

```sh
nice -n 10 python3 -B frozen_accepted/replay.py
```

The final replay checks the accepted predecessor's manifest and receipt;
it does not execute that predecessor or the inherited round-ten replays.
The dependency tree is retained in `inherited/` for those longer checks.

The Claude Science review reports a 42-node positive control exercising
fresh tensors and omitted coordinates. The actual
`positive_fresh_omitted.py` script was absent from the supplied local
review folder. It is recommended for freezing when retrieved; this
release does not claim to have run or included it. The supplied frozen
minimum-product positive controls are retained and replayed.

The additional lower/search-seed/annihilator frozen families are retained
as finite checks of known counts and obstructions. None improves 3/2.

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

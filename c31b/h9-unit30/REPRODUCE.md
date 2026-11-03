# Reproducing the C31b h=9, unit 2^-30 packet

Run commands from this folder. Use Python 3 with the standard library,
a C11 compiler with pthreads, and a little-endian host. The original
release checks used one worker at nice 10. No extra Python packages are needed.
Use fresh scratch and output paths for each replay.

## Small checks

```sh
shasum -a 256 -c SHA256SUMS
nice -n 10 python3 check_controls.py
nice -n 10 python3 check_value.py --receipt verification.json
nice -n 10 python3 verify_c31_lower.py receipts/h5_packet.json --generate \
  --work scratch_h5 --threads 1 --receipt h5_replay.json
```

The first Python command rebuilds the h=5 positive fixture and rejects
all six invalid controls. It rewrites controls.json with its results;
on this release it remained byte-identical. The second command checks
exact fractions, the decimal floor, orbit count and selected receipt fields.
It does not replay h=9 or authenticate the receipt's historical execution.
The last command separately rebuilds and checks the h=5 recipe with the
same producer, decoder and literal checker used for h=9. It must match
SHA256 e6c43fa1b002bc1457dee394e0d0823dea64244995c4d9fe31e11d8c56742375,
check all 22,187 classes and report minimum numerator 7,349,629,664 over
17,179,869,184. Small checks take seconds and well below 1 GB RAM locally.
Release outputs are in receipts/controls_release.log, value_release.log,
h5_release.log and h5_release.json. Job-directory prefixes in published
logs are normalized to <job>; numerical output is unchanged.

## Full h=9 check: substantial memory and time

The whole recipe and check need about 80 GB RAM at peak, at least 13 GB
temporary disk, and roughly two hours on the original shared CPU pod.
The 11,453,945,176-byte decoded vector is absent from this small package.
The historical literal-check receipt alone records 1,923.86 seconds;
that excludes reconstruction. Times depend on hardware and contention.
This command was NOT run in the release job. Run it only on a machine
with the required resources, with no inherited KLOW_* overrides:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
nice -n 10 python3 verify_c31_lower.py packet.json --generate \
  --work scratch_h9 --threads 1 --receipt h9_replay.json
```

The decoder runs the fixed h=5,6,7,8,9 warm-start recipe. Every intermediate
and final vector hash must match packet.json. Then the separate literal
checker checks all 1,431,743,147 classes. The result must say
VERIFIED_CANDIDATE_UNREFEREED, with minimum numerator 7,670,895,684,
denominator 17,179,869,184, and gamma_exact 3835447842/6212691217.
A decoder hash match or iteration log alone is not the full-check verdict.

## Historical receipts and release edits

verification.json, decoder_replay.json and controls.log are unchanged
historical receipts from the frozen packet. Do not interpret them as
checks run during packaging. decoder_byte_cmp.json and comparison.json
have wording corrections only. Their numerical fields are unchanged.
source_comparison.json is the unchanged dated source snapshot; fresh
source facts are in receipts/source_release.json.

The current packet corrects credit/resource prose and source hashes after
comment-only edits to the two C sources. No mathematical parameter,
recipe step, vector hash or executable C statement changed. The decoded
h=5 hash matched again. Current MANIFEST.json and SHA256SUMS cover this
release. CHANGES.diff in the enclosing job records all changes from the
frozen packet, including new files.

The old hashes in the retained receipts resolve as follows:

| Receipt field | Preserved file |
| --- | --- |
| verification.json: metadata_sha256 | packet.json.orig |
| verification.json: checker_sha256; controls.log: checker_sha256 | verify_c31_lower.c.orig |
| decoder_replay.json: generator_sha256 | c31_lower_table.c.orig |
| decoder_replay.json: decoder_sha256 | decode_c31_lower.py (unchanged) |
| verification.json and controls.log: wrapper_sha256 | verify_c31_lower.py (unchanged) |

packet.json.orig references the original generator and checker hashes;
those resolve to the corresponding `.c.orig` files above. The originals
are provenance evidence, not the current reproduction inputs. No new
h=9 receipt was created after the wording edits. receipts/provenance.json
records these links and source-comment equivalence checks.

The original controls.log also contains a hash of its transient h=5
metadata; that temporary file was not retained in the frozen packet.
decoder_replay.json's full_log_sha256 refers to a historical log absent
from the frozen packet. These hashes are retained as historical claims,
not as locally authenticated files.

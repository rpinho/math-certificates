# Reproduce C89c round 3

Candidate and unrefereed. Run from this folder. Requirements: C++17, GMP headers
and runtime, and Python >=3.10 with its standard library. No numerical solver or
pynauty is needed. The graph list and compressed certificate are included.
`artifacts/` and compiled binaries are excluded from the manifest. The SHA list
includes the manifest and excludes itself.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p artifacts
python3 scripts/check_manifest.py
shasum -a 256 -c SHA256SUMS
python3 - <<'PYCODE'
from pathlib import Path
import lzma,hashlib
raw=lzma.decompress(Path('certificates/c6_ordered_type8.cert.xz').read_bytes())
assert hashlib.sha256(raw).hexdigest()=='888552bb82994a387f152d8a7816c011c2bad19f5ed98059152b6dd417ee3c94'
Path('artifacts/c6_ordered_type8.cert').write_bytes(raw)
PYCODE
nice -n 10 c++ -O3 -std=c++17 scripts/check_coloured_predecessor.cpp -lgmp -o check_coloured_predecessor
nice -n 10 ./check_coloured_predecessor artifacts/c6_ordered_type8.cert sources/graph8.g6
```

Expected: all 12,346 coefficient inequalities pass, exhaustive labelled coverage
is 268,435,456, random normalization passes, and the exact bound is
8280981029/250000000000000. The worst graph is 905; reduced slack is
112016854832021/56000000000000000000000000.

For the second separately written coefficient implementation and selected
negative controls:

```sh
nice -n 10 c++ -O3 -std=c++17 scripts/check_certificate.cpp -lgmp -o check_certificate_v3
nice -n 10 ./check_certificate_v3 artifacts/c6_ordered_type8.cert sources/graph8.g6
python3 - <<'PYCODE'
from pathlib import Path
import lzma
Path('certificates/c6_ordered_type8.cert').write_bytes(lzma.decompress(Path('certificates/c6_ordered_type8.cert.xz').read_bytes()))
PYCODE
nice -n 10 python3 scripts/rejection_ordered.py
```

The controls check false bound, zero denominator, duplicate flag, invalid colour,
truncation, and incomplete/duplicate graph lists. They create temporary mutations
under artifacts/ and rewrite the rejection receipt. Run frozen integrity checks
first. The decompressed certificate created for these controls is a replay
intermediate and is not part of the distributed package.

On Apple Silicon with Homebrew GMP, add `-I/opt/homebrew/include
-L/opt/homebrew/lib` to each C++ command. Other platforms should use their own GMP
paths. The cheaper complete release replay took about 96 seconds locally.
The `release_*` receipts distinguish release replays from frozen receipts.

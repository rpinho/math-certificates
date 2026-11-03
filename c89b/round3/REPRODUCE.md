# Reproduce C89b round 3

Candidate and unrefereed. Run from this folder. Requirements: C++17, GMP headers
and runtime, and Python >=3.10 (the controls use int.bit_count). Python's standard
library suffices; no numerical solver or pynauty is required. Keep replay artifacts
outside the manifested files, as below. The manifest excludes `artifacts/` and
compiled checker binaries. The SHA list includes the manifest and excludes itself.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p artifacts
python3 scripts/check_manifest.py
shasum -a 256 -c SHA256SUMS
nice -n 10 c++ -O3 -std=c++17 scripts/check_radial_exact.cpp -lgmp -o check_radial_exact
printf '6 4 36 24 35\n' | nice -n 10 ./check_radial_exact > artifacts/selected.txt
printf '6 3 7 5 7\n' | nice -n 10 ./check_radial_exact > artifacts/baseline.txt
nice -n 10 python3 scripts/freeze_radial.py 6 4 36 24 35 artifacts/reconstructed.json.gz
python3 - <<'PYCODE'
from pathlib import Path
from fractions import Fraction
import gzip
assert gzip.decompress(Path('artifacts/reconstructed.json.gz').read_bytes()) == gzip.decompress(Path('certificates/c5_upper_radial4.json.gz').read_bytes())
a,b,red,blue=map(int,Path('artifacts/selected.txt').read_text().split())
v=Fraction(a,b)
assert v==Fraction(10014541091180996983,6058287395472553279488)
assert red==13559225531043975390720 and blue==12398464977297168789216
assert v<Fraction('0.001653032') and v<Fraction(2405659597,1427496763392)
a,b,*_=map(int,Path('artifacts/baseline.txt').read_text().split())
assert Fraction(a,b)==Fraction(2405659597,1427496763392)
print('PASS exact selected bound, safe rounding, matrix identity and public baseline')
PYCODE
```

For the separate full-matrix recount and all small controls:

```sh
nice -n 10 c++ -O3 -std=c++17 scripts/check_uniform.cpp -lgmp -o check_uniform
nice -n 10 c++ -O3 -std=c++17 scripts/check_graphon.cpp -lgmp -o check_graphon
nice -n 10 python3 scripts/check_uniform.py certificates/c5_upper_radial4.json.gz 0.001653032
nice -n 10 python3 scripts/check_uniform.py sources/upper/candidate.json.gz 0.00168523
nice -n 10 python3 scripts/control_uniform.py
nice -n 10 python3 scripts/graphon_controls.py
nice -n 10 python3 scripts/control_radial.py
```

Control programs rewrite their JSON receipts; the frozen integrity checks should
be run before replay. The selected fast check takes about three seconds locally;
the matrix recount takes longer. The exact expected fraction, colour sums and
compressed/uncompressed hashes are in CERTIFICATES.json and accepted receipts.
The structured checker has parameters as input, so the reconstruction comparison
above is required to tie it to the frozen full matrix.

On Apple Silicon with Homebrew GMP, add `-I/opt/homebrew/include
-L/opt/homebrew/lib` to each C++ command. Other platforms should use their own GMP
paths. The `release_*` receipts distinguish these release replays from the copied
frozen receipts; neither is a human referee report.

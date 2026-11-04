# Reproducing the C38 candidate

Run commands from this directory. Python 3.11 or later is sufficient for the fast check; it uses only the standard library. Native reconstruction requires Linux, GCC with OpenMP, substantial RAM and hours of wall time. Use fresh output directories and preserve the original frozen/ tree. No compilation or full native enumeration is needed for the lightweight release check.

## Fast exact replay and all 22 controls

```sh
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 OMP_NUM_THREADS=1 OMP_DYNAMIC=FALSE
mkdir -p replay_new
nice -n 10 python3 frozen/c38_power_secant/input/verify_power_secant.py frozen/c38_power_secant replay_new/VERIFIED.json
nice -n 10 python3 frozen/c38_power_secant/input/test_power_controls.py frozen/c38_power_secant replay_new/REJECTION_CONTROLS.json
nice -n 10 python3 audit_exact_extension.py frozen/c38_power_secant replay_new/AUDIT.json
```

The final audit compares fresh results with the frozen certificate, reruns the actual corruption code, and requires the entire new control receipt to match the historical receipt. The 22 cases include rebound seed hashes before semantic mutations, wrong values/degrees/reciprocal/family description, future freeze, and malformed JSON. See [release_validation/summary.json](release_validation/summary.json) for this release's measured Mini replay and the exact command log.

This verifies hash bindings, saved native outputs, full-output matches, historical replay chronology, exact rational enclosures and the final power/secant inequality. It does not regenerate transfer states or prove the mathematical interpretation of the programs. Prose establishes state sufficiency, counting, range inclusion, renewal and passage to the connective constant. There is no expanded full integer coefficient vector.

## Full native reconstruction

This optional step was not rerun for the release. Run sequentially, with at most four OpenMP workers on a suitable local machine or eight on the authorized math-cpu-15 pod. The Mini was kept light; the original span-18 native verifier sampled about 49 GB RAM. The original packet's PACKET_README.md contains historical 14-thread examples; use the limits below for this release.

```sh
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 OMP_DYNAMIC=FALSE OMP_NUM_THREADS=4
mkdir -p native_new/bin
nice -n 10 g++ -O3 -march=native -std=c++17 -fopenmp frozen/c38_finite_strip/verify_strip.cpp -o native_new/bin/verify_strip
nice -n 10 g++ -O3 -march=native -std=c++17 -fopenmp frozen/c38_finite_strip/verify_finite_strip.cpp -o native_new/bin/verify_finite_strip
nice -n 10 python3 frozen/c38_finite_strip/verify_packet.py frozen/c38_finite_strip/packet.json --full --binary native_new/bin/verify_strip --finite-binary native_new/bin/verify_finite_strip --work native_new/main --receipt native_new/MAIN_FULL.json
nice -n 10 python3 frozen/span17_all_length_stop/verify_span17_stop.py frozen/span17_all_length_stop native_new/TWO_POINT_FULL.json --full --binary native_new/bin/verify_strip --work native_new/two_point
nice -n 10 g++ -O3 -std=c++17 frozen/rectangle_point/w22_h18_30_c5/input/verify_rectangle_point.cpp -o native_new/bin/verify_rectangle_point
nice -n 10 native_new/bin/verify_rectangle_point 22 18 30 5 native_new/point22.json
nice -n 10 native_new/bin/verify_rectangle_point 23 18 18 5 native_new/point23.json
nice -n 10 python3 - <<'PY'
import json, pathlib
for name, folder in [('point22','w22_h18_30_c5'),('point23','w23_h18_18_c5_parallel')]:
    new=json.loads(pathlib.Path('native_new',name+'.json').read_text())
    old=json.loads(pathlib.Path('frozen/rectangle_point',folder,'replay.json').read_text())
    assert new==old, name
print('Both complete rectangle outputs match')
PY
nice -n 10 python3 frozen/c38_power_secant/input/verify_power_secant.py frozen/c38_power_secant native_new/FINAL_EXACT.json
```

Both rectangles pin the same scalar verifier source, so one binary serves both. It is single-threaded. Main and two-point full modes compare every regenerated output field to the frozen native result, including graph counts and exact numerators. A failure rejects. The last exact call rechecks the immutable packet; the preceding full-mode receipts and rectangle comparisons provide evidence of the new native reconstruction separately.

For the main packet's 35 native/semantic controls, run after compilation:

```sh
nice -n 10 python3 frozen/c38_finite_strip/test_point_packet_controls.py frozen/c38_finite_strip/packet.json native_new/MAIN_CONTROLS.json --binary native_new/bin/verify_strip --finite-binary native_new/bin/verify_finite_strip --scratch native_new/main_controls_scratch
nice -n 10 python3 frozen/span17_all_length_stop/test_span17_stop_controls.py frozen/span17_all_length_stop native_new/TWO_POINT_CONTROLS.json --binary native_new/bin/verify_strip --scratch native_new/stop_controls_scratch
```

## Producer sources and measured original runtimes

The adapted main enumerator is frozen/c38_finite_strip/input/tmx_parallel.c. The span-18 finite enumerator is input/finite/tmx_finite.c there. The supplement producer is frozen/rectangle_point/w22_h18_30_c5/input/rectangle_point_pilot.cpp. Their separate native checkers are included beside them. These programs evaluate generating values by directed exact integer arithmetic, rather than writing the full integer coefficient vector.

The optional producer rerun can use GCC with -O3 -fopenmp -lm for the C sources. tmx_parallel accepts `h 51081913 51082227 --scale 96 --relstop 56 --out NEW.json`; compare exact finite numerators and geometry against each frozen producer output, allowing diagnostic times and valid tail enclosures to differ. The finite enumerator accepts `18 51081913 72 NEW.json` for the frozen 72-column sweep. The rectangle producer accepts `22 18 30 5 NEW.json` or `23 18 18 5 NEW.json`; its SEARCH_ONLY status never substitutes for the separate verifier.

Historical measurements on math-cpu-12 (Linux, GCC 13.3, original aggregate budget up to 18 workers/threads) were: span-18 production 3930.53 seconds; its first separate native replay 1663.42 seconds; complete main frozen-union replay 4455.79 seconds; complete two-point replay 4825.79 seconds. The two scalar rectangle replays took 11242.0719 and 9406.4383 seconds (3.123 and 2.613 hours). These are separate run measurements, not an additive end-to-end runtime or forecasts at four/eight workers. Rectangle timing receipts are in each REPLAY_RECEIPT.json; main span logs and historical runtime provenance are retained. No new large native computation ran during packaging.

Check MANIFEST.json and SHA256SUMS before replay. SHA256SUMS covers all package files except itself; MANIFEST.json covers all payload files except these two seal files. Frozen nested manifests retain their original byte hashes. Two unpinned historical receipt command paths were made relative; their numerical contents, timestamps and all verifier checks are unchanged.

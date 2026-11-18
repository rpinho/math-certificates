# Reproduce the round-9 certificate

Use Python 3.9 or later, with assertions enabled. Only the standard library is required. Replay a copy of this package: output timings change file hashes. The following four checks run serially, with one numerical thread; stop any process exceeding 2 GB RSS. No producer, full-family enumeration or search is required.

```sh
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
/usr/bin/time -l nice -n 10 python3 verify_exact.py certificates/final.json --claim 22878843460258009274861600625288681562329176839147945011303/13414024367090776613897918866165655414442557440000000000000 --out release_validation/exact.json
/usr/bin/time -l nice -n 10 python3 rejection_controls.py certificates/final.json 22878843460258009274861600625288681562329176839147945011303/13414024367090776613897918866165655414442557440000000000000
/usr/bin/time -l nice -n 10 python3 finite_instance.py certificates/final.json release_validation/exact.json release_validation/finite.json --claim 341118263/200000000
(cd referee && /usr/bin/time -l nice -n 10 python3 referee_check.py)
nice -n 10 python3 comparison.py
nice -n 10 python3 sources/claim_facts.py
shasum -a 256 -c SHA256SUMS
```

The seven rejection controls deliberately corrupt data and require rejection. Their generated input files are omitted after hashing; release_validation/omitted-generated.json records hashes and the command above regenerates them. The referee checker emits only aggregate results, with no regenerable per-witness table. producer_logs/ retains the supplied numerical receipts; their “candidate, unrefereed” status is historical producer metadata. The later AI referee verdict HOLDS is recorded separately.

Scheduling: the release session inherited nice 15, lower CPU priority than requested nice 10. The commands above request nice 10 from a normal-priority shell.

## Omitted search history

Only final.json is shipped under certificates/. Superseded certificates and producer archives are not needed for replay and are not shipped. No full-family producer, enumeration or search should run for reproduction. Original file hashes follow:

- archives/all-improvements.tar.xz: SHA-256 `f826eeb4903937011d1f3bae7595ed7325ca72ff8d42a49ad5bb3d568277a9b6`.
- archives/corruption-controls.tar.xz: SHA-256 `0ac1f6cda5b9892dde0a2548d49b27ac58e185ef0e4b7cbb1e02cd44cd142bff`.
- archives/legacy-insertion-targets.tar.xz: SHA-256 `6854299956048ef1b1f83b2bf8ad0c7b77c3cc7f585983f766a061c3bd32626e`.
- archives/public-sources.tar.xz: SHA-256 `82e9e98210e41a228523f1f11b31c47c4f36bc03064f944565504ce9e9cdb248`.
- archives/refreshed-families.tar.xz: SHA-256 `3913c61c176a6de5b08e2257f38b728d08c11b2f6f43c4acbf44df283d944608`.
- archives/search-history.tar.xz: SHA-256 `00af6d6f203e6c07b62ac73de3a61c5101ccce64fd65f8dd72e9454eb426481e`.
- certificates/best_1.7055913150409727.json: SHA-256 `ead3bb2464b4ea93a2f0643ddfc0d68ed77a41309e0347034b53b019a1d32a41`.
- certificates/start444.json: SHA-256 <code>b2200226&#49;180442d2b903988d6381e90dc41129cb09376a3fa8e9146752db394</code>.

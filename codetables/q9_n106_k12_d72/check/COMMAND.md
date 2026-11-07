Run from the codetables/ root after building the checker as described in [its README](../../checkers/ref5/README.md).

```sh
nice -n 10 checkers/ref5/checker q9_n106_k12_d72/generator.txt > q9_n106_k12_d72/check/rerun_result.txt 2> q9_n106_k12_d72/check/rerun.log
```

`result.txt` and `run.log` are the original referee outputs (standard output and progress on standard error), copied byte for byte. `rerun_result.txt` and `rerun.log` are the package reproduction outputs. The referee ran the same checker on a byte-identical copy of `generator.txt` (SHA-256 231b48c60fde5195a4c155a01f64cfce238dfc739c8ba0bd0d095aa05a984445).

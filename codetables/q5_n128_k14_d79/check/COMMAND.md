Run from the codetables/ root after building and preparing the checker as described in [its README](../../checkers/ref2/README.md).

```sh
nice -n 10 checkers/ref2/checker q5_n128_k14_d79/generator.txt 4 > q5_n128_k14_d79/check/rerun_result.json 2> q5_n128_k14_d79/check/rerun.log
```

`result.json` and `run.log` are the original referee outputs, copied byte for byte. `rerun_result.json` and `rerun.log` are the package reproduction outputs. Only file locations change in the command.

The original referee invocation, expressed with the relocated package paths, is the same command with the saved output names:

```sh
nice -n 10 checkers/ref2/checker q5_n128_k14_d79/generator.txt 4 > q5_n128_k14_d79/check/result.json 2> q5_n128_k14_d79/check/run.log
```

The archived outputs are retained unchanged; use the rerun names above when reproducing.

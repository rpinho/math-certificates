Run from the codetables/ root after building and preparing the checker as described in [its README](../../checkers/ref3/README.md).

```sh
nice -n 10 checkers/ref3/checker checkers/ref3/results/q9_n99_k12_d67.dat q9_n99_k12_d67/check/rerun_result.json 8 > q9_n99_k12_d67/check/rerun.log 2>&1
```

`result.json` and `run.log` are the original referee outputs, copied byte for byte. `rerun_result.json` and `rerun.log` are the package reproduction outputs. Only file locations change in the command.

The original referee invocation, expressed with the relocated package paths, is the same command with the saved output names:

```sh
nice -n 10 checkers/ref3/checker checkers/ref3/results/q9_n99_k12_d67.dat q9_n99_k12_d67/check/result.json 8 > q9_n99_k12_d67/check/run.log 2>&1
```

The archived outputs are retained unchanged; use the rerun names above when reproducing.

The referee's scripts write into their working directory, so run them in a fresh one. From the codetables/ root:

```sh
W=$(mktemp -d) && cp checkers/ref6/*.py checkers/ref6/enumerate.cpp "$W"/ && mkdir "$W/inputs" \
  && cp q9_n85_k15_d54/generator.txt "$W/inputs/q9_n85_k15_d54.txt" \
  && (cd "$W/inputs" && shasum -a 256 q9_n85_k15_d54.txt > SHA256SUMS) \
  && (cd "$W" && nice -n 10 python3 -I run_check.py) && cat "$W/distance_result.json"
```

The files without a `rerun_` prefix are the original referee outputs, copied byte for byte: `distance_result.json`, `bz_result.jsonl`, `rs_bz.jsonl`, `rs_control.json`, `initial_check.json`, `bz_setup.json`, `run_metadata.json` and `bound_comparison.json`. The referee ran on a byte-identical copy of `generator.txt` (SHA-256 26e048b359ec2381558530ed88cc2df5ca8220c7a1626177a9043844575e761c). The `rerun_` files come from the package replay; see [RERUN.md](RERUN.md).

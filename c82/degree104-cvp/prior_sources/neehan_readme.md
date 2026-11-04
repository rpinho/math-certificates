# zhang-zagier-82a

Companion code and source files for:

**First variations and block selection for Doche's Zhang--Zagier upper bounds**

This repository contains the reproducibility artifacts for the paper's certified and
diagnostic computations.

## Layout

- `certificate/` — Python certificate and diagnostic scripts.
- `certificate/README.md` — detailed commands and expected outputs.

## Main certified bound

From `certificate/`:

```sh
python3 bound_07_block_j9.py certify \
  14.011500 13.443930 2.643590 2.299880 0.252420 0 0 \
  0.575080 0.568800 0.891590 0.066860 200000 14 1e-10
```

The expected certified result is:

```text
CERTIFIED  log h <= 0.2538893183
```

This improves Doche's `0.25443677` bound.

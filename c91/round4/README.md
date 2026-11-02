# Candidate and unrefereed C91 >= 0.263561

The independently written checker reconstructs all 65,623,319 product states,
268,855,220 edges and 9,409,061 potential classes. It checks every complete
reachable row in exact integers and the final exponent with 256-bit Arb.

Run on the authorized compute host, with python-flint and a C++17 compiler:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
nice -n 10 python3 -u verify_factored_infinite.py candidate.json.gz
```

Run from this directory. No search graph, optimizer, state map, NumPy or SciPy
is needed. The checker compiles its adjacent C++ file into a private temporary
directory and removes its own temporary files afterward. Keep assertions enabled.
The main replay took 1098.60 seconds on math-cpu-7.

Decisive artifact SHA-256:
`2b408738acf654f6a0763d56a7a3283259310eff4c5e4f6cc72afc9993432302`.
The artifact is 30,801,887 bytes. Its binary32 potential is decoded as exact
dyadic integers after an invertible byte-plane transpose. No floating row
inequality is trusted. The proof and authorship scope are in the parent
PROOF.md and INDEPENDENCE.md. This is not external human refereeing.

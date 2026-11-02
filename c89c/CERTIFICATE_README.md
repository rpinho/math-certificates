# C89c lower-bound candidate — unrefereed

The primary statement is **C89c >= 21083/1000000000 = 0.000021083**. This uses the unscaled monochromatic six-set density, with denominator binomial(N,6). No Ramsey-number assumption is used.

Read PROOF.md for the complete finite-to-asymptotic proof. Read ELEMENTARY.md and PRIOR_ART.md for the classical baselines and bounded source audit. The certificate contains integer sum-of-squares factors; the solvers are outside the trusted verification path.

The self-contained exact replay requires a C++17 compiler supporting checked __int128 arithmetic:

```sh
g++ -O3 -std=c++17 verify_exact.cpp -o verify_exact
nice -n 10 ./verify_exact c6_8.cert sources/graph8.g6
```

The additional Python replay requires pynauty 2.8.8.1 and uses arbitrary-precision integers:

```sh
nice -n 10 python verify_python.py c6_8.cert sources/graph8.g6
```

Both should report bound 21083/1000000000 and the same exact smallest slack, at graph index 198. C++ must report coverage of all 268435456 labelled graphs and random-colouring density 1/16384. Verification logs are included.

The auxiliary seven-vertex artifact gives 0.000019448 and is explained in PROOF_7.md. The weaker c6_7.cert is retained for rejection controls; its intentionally invalid derivatives must fail:

```sh
nice -n 10 python check_verifier_controls.py
```

`verify_baselines.py` replays exact classical arithmetic without external Python packages. `requirements_search.txt` records the numerical search environment, which is unnecessary for the C++ verification. REPORT.md in the enclosing job directory gives the full search commands and remaining work. All results are candidate and unrefereed; there is no independent human referee or priority claim.

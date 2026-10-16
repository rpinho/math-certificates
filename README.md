# Math certificates

Explicit, machine-checkable bounds on open optimization constants. Each result comes with an exact certificate
and at least one independently written checker. Each result lives in its own repository, linked below, so the
links already in pull requests, issues and emails keep working. New results will be added here as folders.

| Problem | Bound | Previous best | Status | Repository |
| --- | --- | --- | --- | --- |
| **C<sub>86</sub>**: Schur–Siegel–Smyth trace constant ([Tao table 86a](https://teorth.github.io/optimizationproblems/constants/86a.html)) | C<sub>86</sub> ≤ **1.8117251** | 1.8216 (Talebizadeh Sardari–Orloski 2024) | Table update proposed in [teorth/optimizationproblems#227](https://github.com/teorth/optimizationproblems/pull/227) | [c86-trace-certificate](https://github.com/rpinho/c86-trace-certificate) |
| **C<sub>82</sub>**: essential minimum of the Zhang–Zagier height ([Tao table 82a](https://teorth.github.io/optimizationproblems/constants/82a.html)) | C<sub>82</sub> < **0.2534449** | 0.2536331 on the table (Grinsztajn 2026); 0.2535745 reported by Épi (BakeLab, Sep 2026) | Builds on Épi's construction; table update proposed in [teorth/optimizationproblems#229](https://github.com/teorth/optimizationproblems/pull/229) | [c82-height-certificate](https://github.com/rpinho/c82-height-certificate) |
| **Tetrahedron cylinder cover**: [openai/math problem 100](https://github.com/openai/math/blob/main/lean/docs/100.md) | C < **0.499613830783714149** (saving 3.86 × 10⁻⁴ below 1/2) | ≈ 5.4 × 10⁻¹⁰ saving (the problem's explicit example) | Reported at [plasma-ai/erdos#55](https://github.com/plasma-ai/erdos/issues/55) and [kisonecat/openai-math#1](https://github.com/kisonecat/openai-math/issues/1) | [tetrahedron-cylinder-cover](https://github.com/rpinho/tetrahedron-cylinder-cover) |

## How to check a result

Every repository's README gives the exact run commands. The certificates use exact rational arithmetic or
rigorous interval arithmetic (Arb/FLINT), and the checkers are written independently of the code that found
the construction. None of these results claims optimality. Credits for the methods each construction builds on
are in the individual READMEs.

## Layout for new results

```
<problem-name>/
  README.md        statement, bound, prior art and credit, how to run
  certificate.*    exact data (rationals as strings)
  check_*.py       independent checker(s)
```

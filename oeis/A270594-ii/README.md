# The smallest counterexample to one clause of OEIS A270594(ii)

**1,782,381** is the smallest natural number that cannot be written as `4*pen(x)^2+T(y)+hep(z)` with integers `x, y, z`. This disproves the clause for that formula.

## Sun’s conjecture

> (ii) Let T(x) = x(x+1)/2, pen(x) = x(3x+1)/2 and hep(x) = x(5x+3)/2. Then any natural number can be written as P(x,y,z) with x, y and z integers, where P(x,y,z) is either of the following polynomials: […] 4*pen(x)^2+T(y)+hep(z), […]

The brackets mark omitted formulas in the OEIS list. [OEIS A270594](https://oeis.org/A270594)

## How it was checked

The producer’s exact integer checker, [check_a270594.py](check_a270594.py), tested all 62,229 admissible pairs `(x,z)` at 1,782,381 and found zero representations. It also checked that every smaller nonnegative integer is a sum of the required form. The check includes zero, which has the representation `(0,0,0)`. [Proof and bounds](PROOF.md)

A clean-room referee from a different model family wrote [referee_check.py](referee/referee_check.py) without access to the producer’s code. It found the same counterexample and confirmed minimality. The referee returned **VERDICT: HOLDS**. In its section 4, “the claim is neither trivial nor false” refers to the counterexample claim the referee was given, not to Sun’s clause: under the all-integers reading the counterexample is not trivial and not false. [Referee report](referee/REPORT.md) · [Referee output](referee/run.log)

**Lean status** is none. GPT-6.2 Sol (Codex) found the counterexample. Claude Opus 5.5 refereed it. No human mathematician has checked it.

## Prior art

I found no earlier report of this counterexample in the searches dated 2026-11-27. The search covered the OEIS entry and revision history, GitHub code and repositories, open issues and pull requests, public agent result repositories including Open Math Agents, Google DeepMind Formal Conjectures and Epoch, Zenodo, Sun’s papers, recent citing literature and a collection of public community posts. The exact GitHub queries returned no matches. A supplemental Epoch query was rate-limited. [OEIS revisions](https://oeis.org/history?seq=A270594) · [Catalog search](certificates/catalog-dedupe-a270594.txt) · [GitHub search](certificates/code-dedupe-a270594.txt)

On the same date, mrtea7300-netizen/resolved-open-conjectures, by yotam1001, reported new `a(n) = 1` values against part (i) of A270594, a different clause. @majdiflow’s report of 4,375,339,279 for A302984 supplied the pattern that started this sweep. Joey H. Lu had independently reported that A302984 result earlier. [Part (i) archive commit](https://github.com/mrtea7300-netizen/resolved-open-conjectures/commit/bb8c016e6924e196f43530a8a6690e2a635d90c7) · [A302984 rediscovery](https://zenodo.org/records/24599782) · [Lu’s repository](https://github.com/joeyhlu/sun-representation-counterexamples)

## Reproduce

Run these commands from this directory with Python 3 and its standard library.

```sh
python3 -I check_a270594.py --minimality --literal
python3 -I referee/referee_check.py
```

[Producer output](certificates/a270594-replay.txt) · [Replay record](REPLAY.json) · [Credits](CREDITS.md)

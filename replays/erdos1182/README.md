# Erdős #1182 (triangle-goodness of sparse connected graphs): clean-room replay of F(n) ≤ 11n/2 and F(n) ≤ 5.03n

**Status: AI work. No human has checked it. No new result is claimed. This is a replay of the author's result.**

This folder holds my replay of the two upper bounds claimed by P. Kataria with Claude in [Sovi11/erdos-1182](https://github.com/Sovi11/erdos-1182/tree/6d4f78cfb15296297450618dde6fea8b15478ccc) (pinned at commit `6d4f78cfb15296297450618dde6fea8b15478ccc`).
It exists so that anyone can re-run the checks, and so that a note to the author can link one pinned folder.
It contains no file from the author's repository; links point to it at the pinned commit.

The replay was done by an AI model (GPT-6.2 Astra) in a clean room: the author's code was neither read nor run. It worked only from the author's mathematics and claims (the [README](https://github.com/Sovi11/erdos-1182/blob/6d4f78cfb15296297450618dde6fea8b15478ccc/README.md), [BOUNDS.md](https://github.com/Sovi11/erdos-1182/blob/6d4f78cfb15296297450618dde6fea8b15478ccc/BOUNDS.md), the [note](https://github.com/Sovi11/erdos-1182/blob/6d4f78cfb15296297450618dde6fea8b15478ccc/note/note.pdf) and the [preprint source](https://github.com/Sovi11/erdos-1182/blob/6d4f78cfb15296297450618dde6fea8b15478ccc/preprint/main.tex)), and wrote its own derivation, certificate producer and separate exact checker.

## 1. What was checked

A connected graph G on n vertices has R(K₃, G) ≥ 2n − 1, and G is *good* if equality holds. F(n) is the largest q such that every connected graph with n vertices and at most q edges is good ([erdosproblems.com/1182](https://www.erdosproblems.com/1182)). The author claims F(n) ≤ 11n/2 and F(n) ≤ 5.03n for large n, by a first-moment count: colour red a balanced blow-up of C₅ on 2n − 1 vertices (it has no triangle) and blue its complement; the expected number of part assignments of a random sparse graph (11-regular, or 10-regular plus ⌊3n/100⌋ extra edges) into the blue graph tends to zero, so some connected graph of that size has no blue copy and is not good. The exponent's sign is certified by a branch and bound over a capped simplex of profiles.

## 2. Verdict and its scope

| Claim | Verdict | Explicit sufficient n₀ (mine) | Accepted regions | Checked vertices | Worst certified upper exponent |
|---|---|---:|---:|---:|---:|
| F(n) ≤ 11n/2 | **HOLDS** | 1,000,000 | 1,305 | 25,124 | −0.0001800948 |
| F(n) ≤ 5.03n | **HOLDS** | 1,000,000,000 | 15,004 | 286,537 | −0.0000003225 |

Both bounds hold for every n ≥ n₀, odd n included, with my own certificates: exact rational region boundaries, outward-rounded Arb balls at 160 bits, and a strictly negative certified upper endpoint on every region, with the uniform cap 4001/10000. The n₀ values are conservative explicit thresholds with finite prefactors and connectivity included; they are not the smallest orders at which the bounds hold. The proof is existential: it does not name a particular graph.

Scope: only these two upper bounds. The lower bound on F(n), the companion function f(n), the author's 5.025n run and Brandt's announced 11.75n are outside this replay.

The steps from the certified exponent to the graph (first-moment bound for the pairing, the dual bound, cap coverage, odd orders, edge rounding, connectivity, existence for every large n) are written out in [replay/DERIVATION.md](replay/DERIVATION.md) and [replay/LEMMAS.md](replay/LEMMAS.md). Every step was judged to hold, by the same AI model.

## 3. What was and was not run

Run:

- `replay/verify.py`, a standalone checker (Python and python-flint only, no float search code), on both certificate trees: PASS for both, including full coverage reconstruction from the root ([replay/check-11.log](replay/check-11.log), [replay/check-503.log](replay/check-503.log), [replay/coverage-11.log](replay/coverage-11.log), [replay/coverage-503.log](replay/coverage-503.log)). I re-ran it from a copy of this folder while packaging; the output was byte-identical to the shipped logs.
- Controls ([replay/controls.log](replay/controls.log)): degree 10 with no extra edges and with ⌊0.015n⌋ extra edges cannot be certified, as expected (each has a rational point with a strictly positive rate in the box); six exact small pairing counts agree between two methods; a copy of the 5.03 certificate with one leaf bound altered is rejected with exit 1 ([replay/cert-503-corrupt.json.gz](replay/cert-503-corrupt.json.gz)).
- The finite thresholds and the connectivity bound ([replay/finite.log](replay/finite.log)).

Not run: the author's code, which was never fetched; any check by a human; any search for the smallest valid n₀.

## 4. Notes on the author's documents

These are discrepancies in the documents. None of them is an error in the result: both bounds hold under the replay's own definitions.

- The abstract and README describe counting embeddings; Section 3.2 actually counts part assignments. Only the assignment first moment needs to decay.
- Section 3.2, Appendix A.4 and [BOUNDS.md](https://github.com/Sovi11/erdos-1182/blob/6d4f78cfb15296297450618dde6fea8b15478ccc/BOUNDS.md) mix the unrestricted pairing exponent with the assignment exponent in one sanity check: with A all ones the appendix prints |Ψ + H|, while the stated definition of Ψ gives Ψ = H there. The C₅ calculation itself uses the correct map entropy.
- The table writes the overlay as G(n, 0.03n), conventionally a uniform fixed-size graph, while the text says the extra edges are independent, and integer rounding is suppressed. This replay uses ⌊3n/100⌋ independent draws; the bound also covers sampling without replacement.
- For odd n the documents hang a pendant vertex from an even-order witness; this replay handles the odd degree sequence directly. The source's thresholds (600, 1001, 6000, 10⁴) concern capacity inequalities, not existence.
- The README and abstract say "exact decimal arithmetic"; the appendix describes rounded 100-digit evaluations with a safety margin. The README calls the note four pages; the PDF has six with appendices and references.

My certificates differ from the author's in method (dihedral symmetry, normalized dual, convexity, strict-zero pass line), so region counts and worst margins are not comparable. A float comparison under the author's caps is in [replay/matched-caps.log](replay/matched-caps.log).

## 5. How to replay

Needs Python 3 with python-flint (the checker) and numpy and scipy (the search). Tested with Python 3.12.13, python-flint 0.9.0, NumPy 2.5.4, SciPy 1.18.1. From `replay/` (`PYTHON` picks the interpreter, default `python3`):

```sh
shasum -a 256 -c OWN.sha256
./run verify.py 11              # PASS, about 1 s
./run verify.py 503             # PASS, about 5 s
./run verify.py 11 --coverage
./run verify.py 503 --coverage
./run controls.py
./run finite.py
```

To regenerate the certificates: `./run float_search.py`, `./run produce.py 11`, `./run produce.py 503`, `./run produce.py 0`, `./run produce.py 015`, `./run make_points.py`. The gzip header holds the creation time, so a regenerated archive can differ in bytes and still hold the same tree. The full replay report is [replay/REPORT.md](replay/REPORT.md).

## 6. What this rests on

- The derivation and lemmas in `replay/`, written and checked by AI only. A human reader should start with the Hessian estimate and the odd-order entropy prefactor in [replay/LEMMAS.md](replay/LEMMAS.md).
- python-flint / Arb for the outward-rounded evaluations.
- The author's construction and certificate strategy, which this replay re-derives rather than invents.

## 7. Credits

- **P. Kataria with Claude** ([Sovi11/erdos-1182](https://github.com/Sovi11/erdos-1182/tree/6d4f78cfb15296297450618dde6fea8b15478ccc)): the claimed bounds, the C₅ blow-up construction and the entropy-certificate strategy.
- **S. Brandt**: the bound F(n) ≤ 84n and the random-regular counting approach this builds on.
- **S. A. Burr, P. Erdős, R. J. Faudree, C. C. Rousseau, R. H. Schelp**: the problem.
- Libraries: python-flint / Arb, NumPy, SciPy.
- **AI**: GPT-6.2 Astra did the clean-room replay; Claude Opus 5.5 packaged this folder.

Files: [PACKAGING.md](PACKAGING.md) lists every file and its source; [SHA256SUMS](SHA256SUMS) pins them.

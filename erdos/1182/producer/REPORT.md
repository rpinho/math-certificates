Shipped: A repaired computer-assisted proof that \(F(n)\le5n-1\) for every integer \(n\ge550{,}000\) in Erdős #1182, including odd \(n\).
RESULT: yes

Case I now uses an upper cutoff for \(Q_{03}\). The occupancy rate increases with \(Q_{03}\) and decreases with \(a_0\) at fixed \(Q_{03}\). Below the cutoff the proof uses the occupancy bound at that cutoff and the smallest \(a_0\) in the box. Above it the proof uses a binary relative-entropy tail. The finite first-moment bound at \(n_0=550{,}000\) is below \(4.261\times10^{-11}\). With the disconnection bound of \(3/13\), the total is below \(0.231\), and the first-moment bound decreases thereafter. [Proof](PROOF.md), [Case I and finite-count lemmas](LEMMAS.md), [finite verification](finite.log)

Yes, the bound improves on the closest public upper bound located under the same definition of \(F\), Kataria's unrefereed \(5.025n\). The project uses the balanced \(C_5\) and random-regular framework of Brandt and Kataria. The official page credits Brandt's \(84n\), and Brandt announced \(11.75n\) without a proof. The prior-art note gives the deduction of the intermediate published bound from the authors' Theorem 5.1 and definition of 3-goodness. The repaired result passed the standalone replay. Cross-family review of the repair is pending. [Prior art and recheck](PRIOR_ART.md), [official problem](https://www.erdosproblems.com/1182), [Kataria's pinned bounds](https://raw.githubusercontent.com/Sovi11/erdos-1182/6d4f78c/BOUNDS.md)

| Region and rate | Certified upper bound | Leaves |
|---|---:|---:|
| A and B, naive | \(-0.0011788362183\) | 805 |
| C, Case I | \(-0.001000001000007\) | 1,525 |
| C, Case II | \(-0.001000001000009\) | 1,978 |

The displayed bounds are rounded upward. All 4,308 leaves replayed in 160-bit Arb from the exact cap-\(4001/10000\) roots. Case I has 766 naive and 759 occupancy leaves. Two runs produced byte-identical Case I archives. Both other archives compare byte-for-byte with the source package. The repaired Case I build and full controls peaked below 90 MiB RSS in timed runs. [Producer log](produce.log), [verifier log](verify.log), [SHA-256 manifest](OWN.sha256)

The inherited lower-cutoff certificate had 311 occupancy leaves relying on the reversed inequality. The earlier whole-row fixed-tilt approach also failed because pure-vertex maxima introduced more than four units of entropy slack at the reference profiles. The new proof checks a deterministic inequality for every feasible profile and type, so no statistical holdout applies. The threshold is sufficient and its optimality is open. [Run history](STATUS.md), [certificate lemmas](LEMMAS.md)

## Controls and verdict

- The repaired bound held for all 1,518 randomized feasible pairs, 759 on each side of the cutoff. At all 15,523 occupancy-leaf vertex checks, the control evaluated the direct rate at a feasible approximation of the maximum-entropy \(Q\) and bounded the rate at the exact optimizer using its primal–dual gap. [Control transcript](controls.log)
- The old Case I bound predicted \(-0.0860062574530\) for the occupancy term at the regression fixture. The direct rate was \(-0.0493225162024\), an excess of \(+0.0366837412506\). The verifier rejected all eight Case I mutations, covering the tilt, cutoff, grid, missing leaf, inflated claim, inflated profile bound, legacy format and trailing null. [Control transcript](controls.log)
- The inherited controls passed on 15,000 integer profiles and 6,000 eligible swap configurations. The latter yielded 70,059 valid decreasing swaps and 7,570 forbidden-edge failures with the donor check removed. Across degrees two through four, the direct enumerations matched all 2,093 Case II joint cells, all 2,880 Case I Chernoff inequalities and all 1,824 Case II moment inequalities. All six Case II certificate mutations were rejected. [Control transcript](controls.log)

**CONTROLS:** No. The old bound fails by \(+0.0366837412506\) in control 7. The bare first-moment witness in the verifier log exceeds \(+0.0033635265\), so the proof retains the Case I occupancy argument. [Control transcript](controls.log), [verifier log](verify.log)

**CONTRADICTING:** No. The rejected 311-leaf occupancy argument and its counterexample are recorded. The new control evaluated 759 tail samples alongside 759 near samples, and the finite check counted all \(K,R\). The bare positive witness and the near-zero Case II mirror remain in the replay. [Run history](STATUS.md), [control transcript](controls.log), [verifier log](verify.log)

**LABELS:** No. The Case I controls built symmetric, nonnegative matrices from exact rational edge masses and row complements. Near and tail counts came from comparing the resulting \(Q_{03}\) with the cutoff. The reference replay also reconstructed the mirror from the raw profiles and checked the attached rates. [Controls source](controls.py), [verifier log](verify.log)

## Reproduce

Run from the proof directory with \(PYTHON\) set to the supplied virtual environment's interpreter. Production and controls use NumPy, SciPy and python-flint. The standalone verifier and finite check use python-flint 0.9.0 and the standard library.

~~~sh
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
shasum -a 256 -c OWN.sha256
nice -n 10 "$PYTHON" -B verify.py --coverage --finite --reference reference_table.json --red-witness
nice -n 10 "$PYTHON" -B finite.py
nice -n 10 "$PYTHON" -B controls.py
cmp cert_naive_ab.json.gz ../e1182kempe/cert_naive_ab.json.gz
cmp cert_case2.json.gz ../e1182kempe/cert_case2.json.gz
proof_dir=$PWD
replay_dir=$(mktemp -d .case1-replay.XXXXXX)
(
  cd "$replay_dir" &&
  nice -n 10 "$PYTHON" -B "$proof_dir/produce.py" case1 --seconds 60 &&
  cmp cert_case1.json.gz "$proof_dir/cert_case1.json.gz"
)
~~~

The next step is cross-family replay of the corrected Case I argument and certificate.

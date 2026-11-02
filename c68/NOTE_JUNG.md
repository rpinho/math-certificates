# A certificate for Korenblum's constant c2 >= 0.432

The supplied certificate proves **c2 >= 54/125 = 0.432**. Both independent exact
checkers pass every moment index, including analytic infinite tails. The full
analytic argument is in [GEOMETRIC_LEMMA.md](GEOMETRIC_LEMMA.md) and the
[LaTeX note](paper/korenblum.tex). It uses an elementary covering-strip bound,
classical hyperbolic Jung, and Wikström's unchanged moment-duality criterion.
The proof is an unrefereed mathematical draft; no proof-assistant formalization
is claimed. The checkers certify its quantitative hypotheses.

The best public certified lower bound located in the dated priority audit is
Wikström's 0.4263, so the gain is exactly 57/10000 = 0.0057. The live source recheck and its limits are recorded in FINAL_LIVE_CHECK.md.

## What changes

Wikström's public construction uses eight atoms and a Lebesgue tail beginning
at 0.99. We first widened that construction, keeping Wang's annular estimate,
and certified 0.42638465 using sixteen atoms and a tail beginning at 0.9999.
That result remains separately reproducible from certificate-tight.json.

For the stronger certificate, take the quotient f/g on the annulus, lift it to
the covering strip, normalize its value at one point, and use the two zeros at
neighboring lifts. Concavity of the logarithm of the strip Schwarz distance
bounds the image diameter. Classical hyperbolic Jung chooses a potentially
complex enclosing-disk center. A coefficientwise identity gives the required
annular estimate, to which the same moment criterion applies. The complete
proof is supplied; it does not assume that Wang's product is an angular maximum.

The final measure has twelve rational atoms and Lebesgue measure on [0.999,1].
Its weights sum to 0.999 exactly. The first node is (54/125)^2 and the last is
0.999. Every input is an exact rational in certificate-jung.json. A single
rational linear lower bound for 1/G makes all Lebesgue integrals elementary.
The classical geometry and Schwarz factorization are credited, not claimed
as new theorems. No optimality is asserted.

## Exact checks

- `verify_jung_arb.py`: Arb at 75 decimal digits, exact rational support/mass,
  certified elementary functions, finite moment recurrences and infinite tails.
- `verify_jung_rational.py`: standard library only, outward 200-bit integer
  intervals, Machin's identity for pi, explicit series/remainder enclosures for
  log/sin/exp, integer square roots, separately arranged moment calculations.

Neither imports the optimizer or the other checker. Both prove the linear
slope 2563746486913/10^14 lies below the derived analytic bound. Both check
first moments 1..31278 and second moments 1..23999. The last atom covers the
remaining first moments. A positive interval contribution on [0.9998,0.9999]
covers all second moments from 24000 onward. The finite relative margins exceed
2.0961e-6 and 2.2847e-7; the infinite second-tail gap exceeds 2.1063e-12.

Seventeen independent arithmetic enclosure controls against Arb at 100 digits
pass. Both checkers reject mass-preserving bad moments, an unsafe envelope,
a false infinite-tail cutoff, a wrong analytic-model label and Python -O.
The original 0.4263 measure was reproduced before optimization, including
Wikström's unmodified official checker and both of our original-model checkers.

Certificate SHA-256:

```
80a056f2cec4cfd933944fa51100bc5a1a9657f1a1de509e3a51401ff282002b
```

Run `./reproduce-jung.sh`. The rational checker needs only Python 3; the Arb
checker additionally needs python-flint (tested with 0.9.0). Floating searches
are not needed to reproduce the certificate. Larger failed numerical trials
are exploratory negatives, not proofs of a limiting radius.

Credit: Wang and Schuster for annular-pseudodistance methods; classical Schwarz
factorization and hyperbolic Jung; Wikström, arXiv:2607.17748 and official
Zenodo software doi:10.5281/zenodo.21446369, for moment duality, the measure form
and the LP/refinement strategy. The note and checking software were prepared
with AI assistance for human mathematical review.

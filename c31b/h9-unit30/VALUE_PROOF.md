# Exact value comparison

Candidate and unrefereed; no novelty judgment. Let N=7,670,895,684 and
D=17,179,869,184=16*2^30. The complete separate literal-operator check must
report minimum drift numerator N with denominator D. It then proves
T(w)>=w+r for r=N/D=1,917,723,921/4,294,967,296. The stopping-time proof
in PROOF_C31_LOWER.md gives

    gamma_4 >= 2r/(1+r)=3,835,447,842/6,212,691,217.

Jack's stated exact r0=59,928,872/134,217,728=7,491,109/16,777,216 gives

    gamma0=14,982,218/24,268,325.

Cross multiplication yields

    3,835,447,842*24,268,325
      -14,982,218*6,212,691,217 = 570,425,344 > 0.

The product of the denominators is 150,771,609,578,801,525. Therefore the
exact positive difference is 570,425,344/150,771,609,578,801,525.

For the twelve-decimal floor, cross multiplication gives

    3,835,447,842*10^12
      > 617,356,908,308*6,212,691,217,
    3,835,447,842*10^12
      < 617,356,908,309*6,212,691,217.

These integer identities are checked by the separate wrapper's Fraction
arithmetic and the accompanying value-control script. The finite drift
check, rather than the producer's rounded stopping value, is the input to
this comparison. A complete receipt is required before the headline claim.

The comparison is with Jack's stated value, not a fresh evaluation of his
exact witness. His exact witness may support a higher bound, so the
gain over that witness may be smaller. The source cited in PR #272 is
[bb3b815](https://github.com/leandrejack-afk/chvatal-sankoff-bound/tree/bb3b815/lower).

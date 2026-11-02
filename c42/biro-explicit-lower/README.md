# C42: an explicit value for Biró's strict lower bound

Candidate, unrefereed.

**Claim.** For every n >= 1, R_n > 1/2 + 2^(-4096); hence C42 = limsup R_n >= 1/2 + 2^(-4096).

This makes explicit the strict bound of A. Biró, "An improved estimate in a power sum problem of Turán", Indag. Math. 11 (2000), 343-358 ([author copy](https://users.renyi.hu/~biroand/pdfs/Turan1.pdf)). Biró proved R_n > q for an effectively computable q > 1/2 but did not evaluate q. The method here is his: the first-escape geometry, the summed Newton identities and the attractive fixed point. What this note adds is explicit estimates and one concrete constant. The gain over 1/2 is about 10^(-1233), so it says nothing about where C42 lies.

## Files

| File | What it is |
|---|---|
| [LOWER_PROOF.md](LOWER_PROOF.md) | The written proof, section by section |
| [inputs/lower_certificate.json](inputs/lower_certificate.json) | All parameters (delta = 2^-4096 and the auxiliary constants) |
| [inputs/lower_manifest.json](inputs/lower_manifest.json) | SHA-256 of the proof and certificate |
| [verify_lower_exact.py](verify_lower_exact.py) | Exact-rational checker of every numerical comparison the proof uses |
| [results/lower_exact.json](results/lower_exact.json) | Checker output: 59 checks pass, 6 damaged certificates rejected |
| [PRIOR_ART.md](PRIOR_ART.md) | Sources read and what was checked for priority |
| [reviews/](reviews/) | Two blind AI referee reports on these exact files |

Reproduce (Python 3, standard library only, under a second):

    python3 verify_lower_exact.py

## How it was made and checked

- An AI agent (OpenAI GPT-6.1 Sol, under Ricardo Pinho's direction) wrote both the proof and the checker. The checker was written separately from the proof but by the same agent.
- The checker verifies the arithmetic only: every numerical inequality and the two telescoping polynomial identities. It does not check the analytic steps.
- Two blind AI reviews re-derived the proof step by step and found no false step: GPT-6 Astra and Claude Opus 5.5 (via Claude Science). A fresh GPT-6.1 Sol run did a mechanical correctness check; it is the same model family as the author, so it is not independent. The reports are in reviews/. These are AI reviews, not human refereeing.
- No human has refereed this argument.

Model: gpt-6.1-sol (proof, checker, mechanical review); gpt-6-astra, claude-opus-5-5 (review); claude-opus-5-5 (decision)

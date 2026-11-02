# Prior art for the explicit lower bound

Checked 2026-11-02, 13:16-13:43 UTC.

## The live table

The C42 page of Tao's optimization-constants table ([rendered](https://teorth.github.io/optimizationproblems/constants/42a.html)) lists the lower bounds 1/6, 1/3, π/8, 1/2 and Biró's strict >1/2, described as a computable constant that was not computed. No explicit value above 1/2 appears there. The best upper bound on the page is Koshta's 0.6873358063 (unrefereed). Open PRs #302 (Bakeas, 0.68637) and #305 (Pinho, 0.6863607950) concern the upper bound only.

All 46 open PRs on teorth/optimizationproblems were fetched in full at 13:18 and again at 13:43 UTC. None proposes an explicit lower value for C42.

## The source

A. Biró, "An improved estimate in a power sum problem of Turán", Indagationes Mathematicae 11 (2000), 343-358, [doi:10.1016/S0019-3577(00)80003-8](https://doi.org/10.1016/S0019-3577(00)80003-8), [author copy](https://users.renyi.hu/~biroand/pdfs/Turan1.pdf). It proves R_n > q for every n with an effective q > 1/2 and does not evaluate q. The plasma-ai library card ([link](https://erdosproblems.ai/wiki/library/analysis/biro_2000_improved_estimate_power_sum_problem_turan)) describes the same scope.

This note's argument follows Biró's first-escape geometry, summed Newton identities and attractive fixed point. It is an explicit instance of his theorem, not a new proof that C42 > 1/2 and not a new method.

## Other sources checked

- arXiv: an exact-phrase search returns Andersson's 2006/2007 paper, which concerns a different long-exponent regime. A broader date-sorted search showed no explicit lower constant.
- GitHub: recent repositories on C42 (Bakeas, Koshta, Plata, Griego, rpinho), plus BakeLab/Epi-results, google-deepmind/alphaevolve_results, openai/math, EinsteinArena, plasma-ai/erdos, kisonecat/openai-math and vidigoat/optimization-records. These were README and organization-level checks, not full code searches.

These searches were bounded. Not finding an explicit constant is not proof that none exists.

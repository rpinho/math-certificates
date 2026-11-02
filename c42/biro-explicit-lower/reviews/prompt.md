Referee LOWER_PROOF.md in this directory. It claims an explicit lower bound for Turán's power-sum constant: for every n >= 1 and every complex z_1=1, z_2, ..., z_n, some power sum |S_l| with 1 <= l <= n exceeds 1/2 + 2^(-4096), so C42 = limsup R_n >= 1/2 + 2^(-4096). It says it makes Biró's 2000 strict bound (Indag. Math. 11, 343-358) explicit. inputs/lower_certificate.json holds the parameters, inputs/lower_manifest.json the hashes, verify_lower_exact.py is an exact-rational checker of the numerical hypotheses (run it from this directory), and PRIOR_ART.md lists the sources checked. You have no other information. Don't look at any other local directory. You may open public sources (Biró's paper at https://users.renyi.hu/~biroand/pdfs/Turan1.pdf, the C42 page of Tao's optimization-constants table at https://teorth.github.io/optimizationproblems/constants/42a.html, arXiv).

Your job is adversarial: find the false step. Go lemma by lemma: state the quantifiers, check every inequality direction, check every constant against the certificate, and test steps numerically on explicit small examples where you can. Check the normalization (z_1 = 1 versus max|z_j| = 1) and that the conclusion about R_n and limsup R_n follows. Check whether the checker actually tests the hypotheses the proof uses. Running the checker is fine if it finishes in a few minutes; keep compute light.

Report:
(1) the first false or unjustified step, with its exact location and a counterexample if there is one, or "none found";
(2) every use of Biró's paper: is it stated correctly and do its hypotheses hold where it is applied;
(3) the single step you trust least and why;
(4) novelty and worth: is an explicit q = 1/2 + 2^(-4096) new relative to Biró and the live table, and is it worth recording on Tao's table, or too small to matter. Be blunt;
(5) your probability that the bound is correct, with its basis.

End with one line exactly of the form
VERDICT: PASS | FLAG | FAIL
PASS = no false or unjustified step found; FLAG = an unjustified, unclear or misstated step that is fixable; FAIL = a false step that breaks the claimed bound. Don't claim anything you didn't check.

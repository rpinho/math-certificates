# Credits

Doldrums / SCiEL / CPIL lab MBZUAI's even-radius modulation in
[PR #342](https://github.com/teorth/optimizationproblems/pull/342) is the
starting idea for rounds 3 and 4. Their PR names authors Arina Kharlamova,
Jikun Kang, Yusheng Zhao, Xue Liu and Bowei He (CPIL lab, MBZUAI),
and states the candidate
7.087662112* (underlying certified value 7.08766211189). Their exact
construction could not be retrieved by the producer, so their certificate
was not locally reproduced. Our cosine-radius coefficients are separately searched.

The underlying four-strand superhelix, rational closure, caps and knot
argument are our #324, building on Huh–Kim–Oh's four-strand superhelix
and Youhua Li / Claude Opus 5.5's unequal-double-helix parameters and method.
The preceding constructions and classical theorem credits are retained in
[round 1 credits](../round1/CREDITS.md) and [prior art](PRIOR_ART.md).
They include Olsen–Bohr, Klotz–Maldonado, Kim–Oh–Huh, Diao;
Cantarella–Kusner–Sullivan and Litherland–Simon–Durumeric–Rawdon for
thickness/reach; Conway, Kauffman–Lambropoulou for rational tangles; and
Murasugi, Kauffman and Thistlethwaite for alternating crossing minimality.

Models: GPT-6.1 Sol via Codex (search, construction, proof drafting,
certificates, checkers, packaging); GPT-6 Astra via Codex (round 1 adversarial referee; round 4 clean-room referee);
Claude Opus 5.5 via Claude Science (round 1 review); Claude Code with Claude Opus 5.5 (coordination and PR-text revisions).
The producer's interval verifiers were separately written by the same AI
agent as the search. The clean-room AI referee used a different model and
its own checks; this is an AI referee, not a human review.

NumPy/SciPy support discovery and referee bracket proposals; python-flint /
FLINT / Arb supply interval arithmetic. Python integers, Fraction and SymPy
supply exact algebra where used. See the proof and referee report for scope.

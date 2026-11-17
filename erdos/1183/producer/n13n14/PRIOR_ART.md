# Public status recheck

Started 2026-11-16 America/New_York. Sources and exact read times will be recorded below before search code is written. Locally supplied round 2 is the method baseline; n=11 and n=12 will not be rerun, as instructed.

## Initial reads: 2026-11-17 04:50:08–04:50:10 UTC (November 16 local)

Raw responses, exact URLs, times and HTTP outcomes are in sources/FETCH.json. The problem page and all eleven forum comments were reachable with urllib (browser returned 403). Issue #20, opened today, announces only our f(11)=7 and f(12)=7 candidate certificates; it has no comments. No public exact f(13) or f(14) was found in these sources. Repository HEAD is 2842ef3a58604a8f4b35271d5753c2bf9bdecd0b, unchanged since October 14.

**Critical correction to the spec:** the omega note, lines under “Evidence” and “Triage”, proves f(n) >= (n+3)/2 for odd n >= 11. Thus f(13) >= 8, not merely 7. The current BMB paper, Proposition labelled prop:flower, gives f(n) >= ceil((n+1+floor((n+1)/12))/2), also yielding f(13) >= 8 and f(14) >= 8. Searching for an upper bound 7 at n=13 cannot succeed. This is existing public knowledge, not a new result here. We will screen the requested balanced rank words as a concrete finite check, then seek the mathematically possible upper bound 8; if successful it settles the original exact-value ask.

Best public baseline: BMB membership-closure SAT and counterexample-guided colouring search; our previous rounds supply working encoders/tools and certificates. Reproduction of n=11/n=12 is explicitly prohibited, so those supplied results are reused rather than rerun. No external research code is executed. The current anaxia paper and ipezygj README were read only as text. No predictive metric or SBS applies.

ArXiv search sorted newest and the cited arXiv:2610.02833 page were read. GitHub repository searches sorted by recent update found anaxia-research/Erdos-1183 and QuanyuTang/erdos-problem-1183; no 2026-name match. Named AI result trees: Epi 97fa6a4, AlphaEvolve 4226acb, kisonecat 77bce8d have no 1183 or relevant Ulam path. plasma 6ca84ee contains BMB and Chojecki exposition and will be read below. OpenAI 4eaee87 recursive tree was truncated, so a narrower read is needed. EinsteinArena and repository_of_problems API endpoints return 404. X, Reddit, Discord and other sites are outside the network allowlist; the problem forum and GitHub issues provide the permitted community check. Coverage is bounded.

Follow-up reads at 04:51 UTC: plasma's E1183 page and its BMB transcription describe asymptotic bounds and no exact n=13/14 value; Tang's README is only the repository title. The first OpenAI overview URL returned 404; the correct root overview.tex was then retrieved successfully and has no 1183, union-closed or sublattice match. GitHub issue search for f(13) plus Erdos returned many unrelated numeric matches; the only relevant issue found was #20, about n=11/12. The attempted proof-claims sub-URL returned 404; the main page/forum provide the readable claim discussion. See FETCH_MORE.json and FETCH_OVERVIEW.json.

## Source recheck during final certification: 2026-11-17 05:17:01–05:17:03 UTC

All sixteen reads in sources/FETCH_FINAL.json returned HTTP 200. Anaxia README, paper, all issues, issue #20 and its empty comment list, omega note, recent GitHub repository search, and OpenAI overview are byte-for-byte unchanged. The anaxia first commit remains 2842ef3a58604a8f4b35271d5753c2bf9bdecd0b; the commit-list response differs only because this read requests one commit rather than three. Epi, AlphaEvolve, OpenAI/math, kisonecat and plasma HEADs match the initial tree SHAs. Problem/forum raw HTML contains changing request script tokens; normalized visible text is compared in sources/FINAL_COMPARE.json. No exact f(13) or f(14) was found. This remains a bounded priority search.

## Final source recheck after both theorem checks

2026-11-17T05:22:24.907507+00:00 through 2026-11-17T05:22:25.918815+00:00: repeated all sixteen reads after both dimensions had checked proofs. All returned HTTP 200. Mathematical visible text of the problem page/forum is unchanged; paper, README, issue list, issue #20 and empty comments, omega note, repository search, OpenAI overview, and all five named AI-repository HEADs are unchanged. No public exact f(13) or f(14) value was found. Candidate novelty is these two exact values, 8 and 8; the stronger lower bound f(13)>=8 is existing public knowledge. No new general method is claimed.

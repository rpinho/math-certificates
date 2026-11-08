# Prior art and scope — C22b

This release packages the existing candidate 7.087559024. The packaging
itself adds no search. The source construction extends an earlier
unpublished 7.087580303 construction. That starting point was fully replayed
before the producer searched; [its saved result](producer_logs/baseline_replay.json)
is included. The release's live source scope is [SOURCE_REFRESH.md](SOURCE_REFRESH.md).

The public comparison is Doldrums / SCiEL / CPIL lab MBZUAI's
[7.087662112* proposal, PR #342](https://github.com/teorth/optimizationproblems/pull/342),
underlying advertised value 7.08766211189. Its even-radius modulation of
our [#324 four-strand superhelix](https://github.com/teorth/optimizationproblems/pull/324)
is the starting idea for the unpublished intermediate and this extension.
Authors: Arina Kharlamova, Jikun Kang, Yusheng Zhao, Xue Liu and Bowei He.
Its exact construction was unavailable to the producer at retrieval from
[Zenodo](https://zenodo.org/records/24038188), before any geometry check.
This is a retrieval limit, not evidence of a mathematical failure.

The underlying four-strand superhelix idea is Huh–Kim–Oh's; the unequal
radii and preceding optimization method are Youhua Li / Claude Opus 5.5's
[paper and code](https://github.com/YouhuaLi/tight-alternating-knot-constant/tree/debf7c92f93bae64486e6302e565a2d3b1290f9c).
The original release reproduced that public checker subject to its stated
libm qualification. The all-n cap and rational-tangle argument and inherited
source-access qualifications are in [round 1](../round1/PROOF.md) and
[its credits](../round1/CREDITS.md). The full 2018/2021 Huh–Kim–Oh and
2024 Kim–Oh–Huh papers were unavailable in the original source review;
primary abstracts/metadata were read, and the present argument states its
geometry explicitly. This release does not expand that access claim.

Recent primary references refreshed here are Klotz's
[T(Q,Q) torus links](https://arxiv.org/abs/2603.02416) and
[concentric helices and non-alternating torus knots](https://arxiv.org/abs/2504.00861).
They are different families and normalizations of crossing growth, not
new C22b comparison values. Classical thickness, rational-tangle and
alternating-crossing theorems are credited in [CREDITS.md](CREDITS.md).

The live page still lists 7.2012719* and 7.31; all 78 open PR changed-file
lists identify only #324 and #342 as changing constants/22b.md. Fresh
public-code/agent searches, primary abstract reads and bounded community
queries supplied no stronger candidate within their recorded scope.
Earlier producer source checks on 7–8 November reached the same scoped
conclusion; some late list/README reads were unavailable then. The release
now supplies a complete current open-PR changed-file scan. It does not
claim an exhaustive code, paper or priority review.

The exact comparison
7.087662112 - 7.087559024 = 0.000103088 concerns the supplied construction,
not a discovery made by packaging. Overall verification is L0: finite
interval/exact checks pass; the prose reductions still need mathematical
review, despite a clean-room AI referee's HOLDS conclusion.

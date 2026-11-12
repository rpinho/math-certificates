You asked: push the certified C82 upper bound further below round 8's 0.2519758217, continuing its warm search. I will: reuse round 8's scripts and full union bank, continue LLL numerator pricing and closest-vector denominator generation, and ship a candidate, unrefereed certificate below 0.2519758216 or the best certified value and why it stopped.

Started 2026-11-12. Read the machine-wide RULES.md. Limits: 10 hours, 6 cores, 3 GB total RSS; nice 10 and single-threaded BLAS. No external writes or messages. No novelty judgment.

Copied and reused our round-8 numerical helpers, joint LP, LLL numerator search, CVP search, mergers, controller, separately written verifier, rejection controls and source-inventory method, plus full union bank and final LP state/dual. Inherited public data only; no third-party Python. Four numerator workers and two denominator workers, alternating, with sequential LP/verification.

Setup failure: ./run_local.sh public_reads.py initial exited 126 (permission denied). Restored the inherited wrapper before investigating: copyfile had preserved contents but not its executable bit. Apply chmod +x, as round 8's setup did; numerical scripts and method unchanged.

The no-gain stop counts actual certified endpoint improvements over a complete alternating round. Round 8's inherited LP cutoff of 1e-10 is larger than the new frozen-bar margin (3.77e-11), so it is not used to discard certified gains here. The search, LP tolerances and verifier are unchanged. Solo first-round measurements precede scaling to 4 numerator / 2 denominator workers; at most 4 numerical workers run at once.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519758216376568674750; frozen target not yet met. Source certificate.json

Warm baseline replay passed: B in [0.2519758216376568634394, 0.2519758216376568674750], unchanged from round 8. Solo verifier /usr/bin/time -l peak RSS: 38,764,544 bytes; 73.09 seconds wall. The baseline does not meet 0.2519758216. Begin round 22 with inherited full LP state and dual.

2026-11-12 00:13:46 Round 22: num new-column search on rounds/restricted-22.json, dual rounds/warm-dual.npz.

Measured solo num worker: see logs/num-search-22-0.log.time and aggregate RSS in evidence/compute.jsonl; planned subsequent worker count 4.

Solo round-22 numerator worker measured 108,412,928 bytes maximum resident set size; four times this is 433,651,712 bytes, below 3 GB. Continue planned four-worker numerator batches after solo denominator measurement.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519758125556973843153; frozen target met. Source rounds/num-22-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519758117536014522265; frozen target met. Source rounds/archive-num-22-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519758115766568544853; frozen target met. Source rounds/archive-num-22-1-certificate.json

2026-11-12 00:40:41 Round 22: den new-column search on rounds/restricted-archive-num-22-1.json, dual rounds/archive-num-22-1-dual.npz.

Measured solo den worker: see logs/den-search-22-0.log.time and aggregate RSS in evidence/compute.jsonl; planned subsequent worker count 4.

{"round": 22, "old_lp": 0.25197582156501663, "new_lp": 0.25197581143918496, "gain": 1.0125831673146735e-08, "certified_gain": "1164984211320734737822805931259126172632385987925406019125361389845747/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 4, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-22-1.json", "dual": "rounds/archive-num-22-1-dual.npz"}

2026-11-12 00:44:47 Round 23: num new-column search on rounds/restricted-archive-num-22-1.json, dual rounds/archive-num-22-1-dual.npz.

Solo round-22 CVP worker measured 451,559,424 bytes maximum resident set size; two planned CVP workers total 903,118,848 bytes before controller overhead, below 3 GB. The inherited controller's preceding generic “planned worker count 4” line refers to numerator workers; denominator batches use --den-workers 2. Round 23 starts the planned 4 numerator / 2 denominator allocation, in alternating batches.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519757068257903981497; frozen target met. Source rounds/num-23-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519757008027238753495; frozen target met. Source rounds/archive-num-23-0-certificate.json

Execution allocation: serial complete-bank numerator pricing ran normally and exposed additional gains, but now takes 6–7 minutes per moved dual (logs/archive-num-23-1.log). Assign four single-threaded workers to the independent per-factor gcd/root-log/reduced-cost calculations, retaining the full bank, original order, original formulas and sequential LP. This changes CPU allocation, not the mathematical search method. Original serial code is saved as evidence/numerator_search_serial.py for immediate reversion. The first complete parallel pass remains supervised under /usr/bin/time -l and the 3 GB aggregate guard.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519757007788551890048; frozen target met. Source rounds/archive-num-23-1-certificate.json

2026-11-12 01:09:04 Round 23: den new-column search on rounds/restricted-archive-num-23-1.json, dual rounds/archive-num-23-1-dual.npz.

First four-worker full-bank pass completed normally (rounds/archive-num-23-2-screen.json): 104.89 wall seconds, 425.58 recorded CPU seconds including supervision, sampled aggregate RSS 559,382,528 bytes. No additional negative column. This preserves complete bank coverage and ordered reduced-cost evaluation; degree-104 CVP now runs with two workers on the latest dual.

{"round": 23, "old_lp": 0.25197581143918496, "new_lp": 0.25197570069133535, "gain": 1.1074784961317974e-07, "certified_gain": "12829508937747782055522031601955452378340708261929537844172703704238847/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 22, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-23-1.json", "dual": "rounds/archive-num-23-1-dual.npz"}

2026-11-12 01:13:09 Round 24: num new-column search on rounds/restricted-archive-num-23-1.json, dual rounds/archive-num-23-1-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756801294185915884; frozen target met. Source rounds/num-24-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756748558874032218; frozen target met. Source rounds/archive-num-24-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756747468334639667; frozen target met. Source rounds/archive-num-24-1-certificate.json

2026-11-12 01:26:38 Round 24: den new-column search on rounds/restricted-archive-num-24-1.json, dual rounds/archive-num-24-1-dual.npz.

{"round": 24, "old_lp": 0.25197570069133535, "new_lp": 0.25197567461195775, "gain": 2.6079377601906373e-08, "certified_gain": "3014302182613366749195661859954173923133843898624189351063620418470759/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 7, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-24-1.json", "dual": "rounds/archive-num-24-1-dual.npz"}

2026-11-12 01:30:41 Round 25: num new-column search on rounds/restricted-archive-num-24-1.json, dual rounds/archive-num-24-1-dual.npz.

Retained <50 MB: gzip-compressed 93 completed historical JSON/log files and moved 8 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756557935080371234; frozen target met. Source rounds/num-25-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756556946732165262; frozen target met. Source rounds/archive-num-25-0-certificate.json

2026-11-12 01:41:32 Round 25: den new-column search on rounds/restricted-archive-num-25-0.json, dual rounds/archive-num-25-0-dual.npz.

{"round": 25, "old_lp": 0.25197567461195775, "new_lp": 0.2519756556039317, "gain": 1.9008026042044435e-08, "certified_gain": "2206089439535282563649229215574798523935749778077551966459829129160043/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 11, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-25-0.json", "dual": "rounds/archive-num-25-0-dual.npz"}

2026-11-12 01:45:35 Round 26: num new-column search on rounds/restricted-archive-num-25-0.json, dual rounds/archive-num-25-0-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756481745235770197; frozen target met. Source rounds/num-26-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756479080223813978; frozen target met. Source rounds/archive-num-26-0-certificate.json

2026-11-12 01:56:34 Round 26: den new-column search on rounds/restricted-archive-num-26-0.json, dual rounds/archive-num-26-0-dual.npz.

{"round": 26, "old_lp": 0.2519756556039317, "new_lp": 0.2519756478067755, "gain": 7.797156198474653e-09, "certified_gain": "1803265136722018620489578778459057159179531351995365967537677819452135/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 3, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-26-0.json", "dual": "rounds/archive-num-26-0-dual.npz"}

2026-11-12 02:00:35 Round 27: num new-column search on rounds/restricted-archive-num-26-0.json, dual rounds/archive-num-26-0-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756193606640932567; frozen target met. Source rounds/num-27-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756190595209022274; frozen target met. Source rounds/archive-num-27-0-certificate.json

2026-11-12 02:11:23 Round 27: den new-column search on rounds/restricted-archive-num-27-0.json, dual rounds/archive-num-27-0-dual.npz.

{"round": 27, "old_lp": 0.2519756478067755, "new_lp": 0.2519756189774596, "gain": 2.882931587899762e-08, "certified_gain": "6680856515277883349326762433723971386232995143738582310997949018627071/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 13, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-27-0.json", "dual": "rounds/archive-num-27-0-dual.npz"}

2026-11-12 02:15:25 Round 28: num new-column search on rounds/restricted-archive-num-27-0.json, dual rounds/archive-num-27-0-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756069540503236489; frozen target met. Source rounds/num-28-certificate.json

Retained <50 MB: gzip-compressed 83 completed historical JSON/log files and moved 6 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519756068984098885200; frozen target met. Source rounds/archive-num-28-0-certificate.json

2026-11-12 02:26:38 Round 28: den new-column search on rounds/restricted-archive-num-28-0.json, dual rounds/archive-num-28-0-dual.npz.

{"round": 28, "old_lp": 0.2519756189774596, "new_lp": 0.2519756068447218, "gain": 1.2132737814418704e-08, "certified_gain": "2816320903448242953649903584575089821480488825271045636991276719245717/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 9, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-28-0.json", "dual": "rounds/archive-num-28-0-dual.npz"}

2026-11-12 02:30:43 Round 29: num new-column search on rounds/restricted-archive-num-28-0.json, dual rounds/archive-num-28-0-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519755916525379614194; frozen target met. Source rounds/num-29-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519755916328177380492; frozen target met. Source rounds/archive-num-29-0-certificate.json

2026-11-12 02:41:39 Round 29: den new-column search on rounds/restricted-archive-num-29-0.json, dual rounds/archive-num-29-0-dual.npz.

{"round": 29, "old_lp": 0.2519756068447218, "new_lp": 0.25197559153889837, "gain": 1.5305823442002264e-08, "certified_gain": "3535269617095576824360129711709749402656392641438494984901669666342421/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 7, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-29-0.json", "dual": "rounds/archive-num-29-0-dual.npz"}

2026-11-12 02:45:39 Round 30: num new-column search on rounds/restricted-archive-num-29-0.json, dual rounds/archive-num-29-0-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519755583505470508310; frozen target met. Source rounds/num-30-certificate.json

Retained <50 MB: gzip-compressed 54 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519755517636076710567; frozen target met. Source rounds/archive-num-30-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519755516419089843136; frozen target met. Source rounds/archive-num-30-1-certificate.json

2026-11-12 03:00:07 Round 30: den new-column search on rounds/restricted-archive-num-30-1.json, dual rounds/archive-num-30-1-dual.npz.

{"round": 30, "old_lp": 0.25197559153889837, "new_lp": 0.25197555154923856, "gain": 3.998965980578362e-08, "certified_gain": "2315315437546960633622930533339669924623366382152374293609973620814731/57896044618658097711785492504343953926634992332820282019728792003956564819968", "negative_candidates": {"num": 10, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-30-1.json", "dual": "rounds/archive-num-30-1-dual.npz"}

2026-11-12 03:04:10 Round 31: num new-column search on rounds/restricted-archive-num-30-1.json, dual rounds/archive-num-30-1-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519755447751923149066; frozen target met. Source rounds/num-31-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519755445399234998198; frozen target met. Source rounds/archive-num-31-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519755445300598721447; frozen target met. Source rounds/archive-num-31-1-certificate.json

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

2026-11-12 03:22:37 Round 31: den new-column search on rounds/restricted-archive-num-31-2.json, dual rounds/archive-num-31-2-dual.npz.

{"round": 31, "old_lp": 0.25197555154923856, "new_lp": 0.2519755444221206, "gain": 7.127117951366557e-09, "certified_gain": "411747933519291981821807169957943513303900148865390378542698746475779/57896044618658097711785492504343953926634992332820282019728792003956564819968", "negative_candidates": {"num": 8, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-31-2.json", "dual": "rounds/archive-num-31-2-dual.npz"}

2026-11-12 03:26:42 Round 32: num new-column search on rounds/restricted-archive-num-31-2.json, dual rounds/archive-num-31-2-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519754894616937182643; frozen target met. Source rounds/num-32-certificate.json

Retained <50 MB: gzip-compressed 41 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519754858009415858806; frozen target met. Source rounds/archive-num-32-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519754855975299582795; frozen target met. Source rounds/archive-num-32-1-certificate.json

2026-11-12 03:41:29 Round 32: den new-column search on rounds/restricted-archive-num-32-1.json, dual rounds/archive-num-32-1-dual.npz.

{"round": 32, "old_lp": 0.2519755444221206, "new_lp": 0.2519754854829777, "gain": 5.893914289956115e-08, "certified_gain": "13647841525534178458124736893083625972644930852887240928330872510545965/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 15, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-32-1.json", "dual": "rounds/archive-num-32-1-dual.npz"}

2026-11-12 03:45:33 Round 33: num new-column search on rounds/restricted-archive-num-32-1.json, dual rounds/archive-num-32-1-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519754848329520052216; frozen target met. Source rounds/num-33-certificate.json

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

2026-11-12 03:53:21 Round 33: den new-column search on rounds/restricted-num-33.json, dual rounds/num-33-dual.npz.

{"round": 33, "old_lp": 0.2519754854829777, "new_lp": 0.2519754847094788, "gain": 7.734989315721919e-10, "certified_gain": "88532078569368843140325072393342881435964794193609218468900270719463/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 1, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-num-33.json", "dual": "rounds/num-33-dual.npz"}

2026-11-12 03:57:25 Round 34: num new-column search on rounds/restricted-num-33.json, dual rounds/num-33-dual.npz.

2026-11-12 04:01:26 Round 34: den new-column search on rounds/restricted-num-33.json, dual rounds/num-33-dual.npz.

{"round": 34, "old_lp": 0.2519754847094788, "new_lp": 0.2519754847094788, "gain": 0.0, "certified_gain": "0", "negative_candidates": {"num": 0, "den": 0}, "empty_rounds": 1, "state": "rounds/restricted-num-33.json", "dual": "rounds/num-33-dual.npz"}

2026-11-12 04:05:29 Round 35: num new-column search on rounds/restricted-num-33.json, dual rounds/num-33-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519754806606503392866; frozen target met. Source rounds/num-35-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519754806246492688047; frozen target met. Source rounds/archive-num-35-0-certificate.json

Retained <50 MB: gzip-compressed 32 completed historical JSON/log files and moved 1 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

2026-11-12 04:16:51 Round 35: den new-column search on rounds/restricted-archive-num-35-0.json, dual rounds/archive-num-35-0-dual.npz.

{"round": 35, "old_lp": 0.2519754847094788, "new_lp": 0.2519754805318069, "gain": 4.1776718751052044e-09, "certified_gain": "974576331985650344669172850711816015152575786995701831843231149268735/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 3, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-35-0.json", "dual": "rounds/archive-num-35-0-dual.npz"}

2026-11-12 04:20:55 Round 36: num new-column search on rounds/restricted-archive-num-35-0.json, dual rounds/archive-num-35-0-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519754778395081456327; frozen target met. Source rounds/num-36-certificate.json

Retained <50 MB: gzip-compressed 27 completed historical JSON/log files and moved 2 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519754773256954499739; frozen target met. Source rounds/archive-num-36-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519754773207200846022; frozen target met. Source rounds/archive-num-36-1-certificate.json

2026-11-12 04:35:04 Round 36: den new-column search on rounds/restricted-archive-num-36-1.json, dual rounds/archive-num-36-1-dual.npz.

{"round": 36, "old_lp": 0.2519754805318069, "new_lp": 0.25197547718400504, "gain": 3.3478018690580313e-09, "certified_gain": "765137725861885409742126011842499144913078980801323439669409579813163/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 3, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-36-1.json", "dual": "rounds/archive-num-36-1-dual.npz"}

2026-11-12 04:39:10 Round 37: num new-column search on rounds/restricted-archive-num-36-1.json, dual rounds/archive-num-36-1-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519754249846646812583; frozen target met. Source rounds/num-37-certificate.json

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519753943998049659379; frozen target met. Source rounds/archive-num-37-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519753941452102234653; frozen target met. Source rounds/archive-num-37-1-certificate.json

2026-11-12 04:52:49 Round 37: den new-column search on rounds/restricted-archive-num-37-1.json, dual rounds/archive-num-37-1-dual.npz.

{"round": 37, "old_lp": 0.25197547718400504, "new_lp": 0.25197539406116887, "gain": 8.312283616973559e-08, "certified_gain": "19262132120400089497985166353451997961583435530470442131807817475049901/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 2, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-37-1.json", "dual": "rounds/archive-num-37-1-dual.npz"}

2026-11-12 04:56:54 Round 38: num new-column search on rounds/restricted-archive-num-37-1.json, dual rounds/archive-num-37-1-dual.npz.

Retained <50 MB: gzip-compressed 32 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519753794609831952451; frozen target met. Source rounds/num-38-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519753777227970820186; frozen target met. Source rounds/archive-num-38-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519753776928587379400; frozen target met. Source rounds/archive-num-38-1-certificate.json

2026-11-12 05:13:57 Round 38: den new-column search on rounds/restricted-archive-num-38-2.json, dual rounds/archive-num-38-2-dual.npz.

{"round": 38, "old_lp": 0.25197539406116887, "new_lp": 0.2519753776494466, "gain": 1.6411722258968808e-08, "certified_gain": "3810104302751265882821235744025859196114567557797668774724976181017599/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 13, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-38-2.json", "dual": "rounds/archive-num-38-2-dual.npz"}

2026-11-12 05:18:04 Round 39: num new-column search on rounds/restricted-archive-num-38-2.json, dual rounds/archive-num-38-2-dual.npz.

Retained <50 MB: gzip-compressed 41 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519752868352606523623; frozen target met. Source rounds/num-39-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519752765150925342784; frozen target met. Source rounds/archive-num-39-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519752764462934577264; frozen target met. Source rounds/archive-num-39-1-certificate.json

Retained packet reached 45 MB. Moved 84 old compressed floating LP caches (6,791,339 bytes) to macOS Trash; their old dual caches had already been retired. Warm state, current state/dual, complete factor bank, every best certificate, all certificate/replay records and all Python remain. Bound reproduction uses the standalone exact certificates and verifier.

2026-11-12 05:36:40 Round 39: den new-column search on rounds/restricted-archive-num-39-2.json, dual rounds/archive-num-39-2-dual.npz.

{"round": 39, "old_lp": 0.2519753776494466, "new_lp": 0.25197527635329914, "gain": 1.0129614747000915e-07, "certified_gain": "23447102643796512100451400302297601451599517816504497709171460446868223/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 14, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-39-2.json", "dual": "rounds/archive-num-39-2-dual.npz"}

2026-11-12 05:40:45 Round 40: num new-column search on rounds/restricted-archive-num-39-2.json, dual rounds/archive-num-39-2-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519752409309729003823; frozen target met. Source rounds/num-40-certificate.json

Retained <50 MB: gzip-compressed 43 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519752387003503386237; frozen target met. Source rounds/archive-num-40-0-certificate.json

2026-11-12 05:51:48 Round 40: den new-column search on rounds/restricted-archive-num-40-0.json, dual rounds/archive-num-40-0-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519749220891971145117; frozen target met. Source rounds/den-40-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519747921404401885183; frozen target met. Source rounds/archive-den-40-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519747817061537509278; frozen target met. Source rounds/archive-den-40-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519747806254432357571; frozen target met. Source rounds/archive-den-40-2-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519747806105809080127; frozen target met. Source rounds/archive-den-40-3-certificate.json

{"round": 40, "old_lp": 0.25197527635329914, "new_lp": 0.2519747805338462, "gain": 4.958194529391946e-07, "certified_gain": "114827706149209409913751315286964116685120687545761884958799343151785105/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 25, "den": 1}, "empty_rounds": 0, "state": "rounds/restricted-archive-den-40-3.json", "dual": "rounds/archive-den-40-3-dual.npz"}

2026-11-12 06:11:59 Round 41: num new-column search on rounds/restricted-archive-den-40-3.json, dual rounds/archive-den-40-3-dual.npz.

Retained <50 MB: gzip-compressed 61 completed historical JSON/log files and moved 7 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519747169284980306825; frozen target met. Source rounds/num-41-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519746944962311012419; frozen target met. Source rounds/archive-num-41-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519746920810862792909; frozen target met. Source rounds/archive-num-41-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519746916473669833747; frozen target met. Source rounds/archive-num-41-2-certificate.json

2026-11-12 06:30:17 Round 41: den new-column search on rounds/restricted-archive-num-41-2.json, dual rounds/archive-num-41-2-dual.npz.

{"round": 41, "old_lp": 0.2519747805338462, "new_lp": 0.25197469152880103, "gain": 8.900504516740071e-08, "certified_gain": "20602472811200269395762693527689989656300480403628114230138426958557785/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 221, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-41-2.json", "dual": "rounds/archive-num-41-2-dual.npz"}

2026-11-12 06:34:22 Round 42: num new-column search on rounds/restricted-archive-num-41-2.json, dual rounds/archive-num-41-2-dual.npz.

Retained <50 MB: gzip-compressed 41 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519746255527689625549; frozen target met. Source rounds/num-42-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745906924629447561; frozen target met. Source rounds/archive-num-42-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745904262694651072; frozen target met. Source rounds/archive-num-42-1-certificate.json

2026-11-12 06:48:27 Round 42: den new-column search on rounds/restricted-archive-num-42-1.json, dual rounds/archive-num-42-1-dual.npz.

{"round": 42, "old_lp": 0.25197469152880103, "new_lp": 0.25197459034703096, "gain": 1.0118177007356621e-07, "certified_gain": "23441204713068642302693408493267263680596537841411900952989930006233463/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 399, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-42-1.json", "dual": "rounds/archive-num-42-1-dual.npz"}

2026-11-12 06:52:32 Round 43: num new-column search on rounds/restricted-archive-num-42-1.json, dual rounds/archive-num-42-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745440628156078764; frozen target met. Source rounds/num-43-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745426343467702732; frozen target met. Source rounds/archive-num-43-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745424908702794659; frozen target met. Source rounds/archive-num-43-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745424797357957986; frozen target met. Source rounds/archive-num-43-2-certificate.json

2026-11-12 07:10:45 Round 43: den new-column search on rounds/restricted-archive-num-43-2.json, dual rounds/archive-num-43-2-dual.npz.

{"round": 43, "old_lp": 0.25197459034703096, "new_lp": 0.2519745423580893, "gain": 4.798894165380929e-08, "certified_gain": "5551829305256563326240899312104601739032351529414571252096976752707033/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 39, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-43-2.json", "dual": "rounds/archive-num-43-2-dual.npz"}

2026-11-12 07:14:48 Round 44: num new-column search on rounds/restricted-archive-num-43-2.json, dual rounds/archive-num-43-2-dual.npz.

Retained <50 MB: gzip-compressed 41 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745289258011211607; frozen target met. Source rounds/num-44-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745284920620517042; frozen target met. Source rounds/archive-num-44-0-certificate.json

2026-11-12 07:29:18 Round 44: den new-column search on rounds/restricted-archive-num-44-1.json, dual rounds/archive-num-44-1-dual.npz.

{"round": 44, "old_lp": 0.2519745423580893, "new_lp": 0.25197452830338707, "gain": 1.4054702235366534e-08, "certified_gain": "1619661966398647491282771695287946704975817302752375610265274140088125/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 21, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-44-1.json", "dual": "rounds/archive-num-44-1-dual.npz"}

2026-11-12 07:33:25 Round 45: num new-column search on rounds/restricted-archive-num-44-1.json, dual rounds/archive-num-44-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745077480290575307; frozen target met. Source rounds/num-45-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745075307625806976; frozen target met. Source rounds/archive-num-45-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519745075302016513671; frozen target met. Source rounds/archive-num-45-1-certificate.json

2026-11-12 07:48:33 Round 45: den new-column search on rounds/restricted-archive-num-45-1.json, dual rounds/archive-num-45-1-dual.npz.

{"round": 45, "old_lp": 0.25197452830338707, "new_lp": 0.25197450742539096, "gain": 2.087799610972496e-08, "certified_gain": "4854435220111988841814114118427301481611656907298723469506302614721251/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 15, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-45-1.json", "dual": "rounds/archive-num-45-1-dual.npz"}

2026-11-12 07:52:39 Round 46: num new-column search on rounds/restricted-archive-num-45-1.json, dual rounds/archive-num-45-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744957651570195342; frozen target met. Source rounds/num-46-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744952515796401594; frozen target met. Source rounds/archive-num-46-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744952289922818985; frozen target met. Source rounds/archive-num-46-1-certificate.json

2026-11-12 08:07:46 Round 46: den new-column search on rounds/restricted-archive-num-46-1.json, dual rounds/archive-num-46-1-dual.npz.

{"round": 46, "old_lp": 0.25197450742539096, "new_lp": 0.25197449514856657, "gain": 1.2276824390422547e-08, "certified_gain": "1424382733036411948211741836263237072719402677069734189030441789012145/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 7, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-46-1.json", "dual": "rounds/archive-num-46-1-dual.npz"}

2026-11-12 08:11:50 Round 47: num new-column search on rounds/restricted-archive-num-46-1.json, dual rounds/archive-num-46-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744829177648826996; frozen target met. Source rounds/num-47-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744826182606977012; frozen target met. Source rounds/archive-num-47-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744826165565187986; frozen target met. Source rounds/archive-num-47-1-certificate.json

2026-11-12 08:26:35 Round 47: den new-column search on rounds/restricted-archive-num-47-1.json, dual rounds/archive-num-47-1-dual.npz.

Retained packet reached 47 MB. Moved 62 old compressed floating LP caches (5,095,789 bytes) to macOS Trash. Warm/current states, current dual, full bank, all certificates/replays and all Python remain; exact bound reproduction is unchanged.

{"round": 47, "old_lp": 0.25197449514856657, "new_lp": 0.25197448248324855, "gain": 1.266531801658033e-08, "certified_gain": "1460420287380783935869223370118028127156882114184762108620027119529169/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 11, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-47-1.json", "dual": "rounds/archive-num-47-1-dual.npz"}

2026-11-12 08:30:39 Round 48: num new-column search on rounds/restricted-archive-num-47-1.json, dual rounds/archive-num-47-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744755581594321244; frozen target met. Source rounds/num-48-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744744370187468537; frozen target met. Source rounds/archive-num-48-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744742005745220853; frozen target met. Source rounds/archive-num-48-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744741541115553934; frozen target met. Source rounds/archive-num-48-2-certificate.json

2026-11-12 08:51:56 Round 48: den new-column search on rounds/restricted-archive-num-48-3.json, dual rounds/archive-num-48-3-dual.npz.

{"round": 48, "old_lp": 0.25197448248324855, "new_lp": 0.2519744740695891, "gain": 8.413659435824172e-09, "certified_gain": "979884182368491537228387475960145645411659268244316916861469634099109/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 5, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-48-3.json", "dual": "rounds/archive-num-48-3-dual.npz"}

2026-11-12 08:56:02 Round 49: num new-column search on rounds/restricted-archive-num-48-3.json, dual rounds/archive-num-48-3-dual.npz.

Retained <50 MB: gzip-compressed 48 completed historical JSON/log files and moved 5 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744679410232353184; frozen target met. Source rounds/num-49-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744660885903951223; frozen target met. Source rounds/archive-num-49-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744660515703600599; frozen target met. Source rounds/archive-num-49-1-certificate.json

2026-11-12 09:10:22 Round 49: den new-column search on rounds/restricted-archive-num-49-1.json, dual rounds/archive-num-49-1-dual.npz.

{"round": 49, "old_lp": 0.2519744740695891, "new_lp": 0.2519744660556423, "gain": 8.0139468394691e-09, "certified_gain": "938210173139094368489776154545723574853182854329006367752625390570587/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 10, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-49-1.json", "dual": "rounds/archive-num-49-1-dual.npz"}

2026-11-12 09:14:23 Round 50: num new-column search on rounds/restricted-archive-num-49-1.json, dual rounds/archive-num-49-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744557953114964140; frozen target met. Source rounds/num-50-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744542309988299119; frozen target met. Source rounds/archive-num-50-0-certificate.json

2026-11-12 09:25:31 Round 50: den new-column search on rounds/restricted-archive-num-50-0.json, dual rounds/archive-num-50-0-dual.npz.

{"round": 50, "old_lp": 0.2519744660556423, "new_lp": 0.251974454185727, "gain": 1.1869915272910703e-08, "certified_gain": "2737457346909939618236501943523743304162716147734530692314956552336175/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 10, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-50-0.json", "dual": "rounds/archive-num-50-0-dual.npz"}

2026-11-12 09:29:35 Round 51: num new-column search on rounds/restricted-archive-num-50-0.json, dual rounds/archive-num-50-0-dual.npz.

Retained <50 MB: gzip-compressed 27 completed historical JSON/log files and moved 2 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744490533681078501; frozen target met. Source rounds/num-51-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744487551640730707; frozen target met. Source rounds/archive-num-51-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744487408958502183; frozen target met. Source rounds/archive-num-51-1-certificate.json

2026-11-12 09:45:14 Round 51: den new-column search on rounds/restricted-archive-num-51-1.json, dual rounds/archive-num-51-1-dual.npz.

{"round": 51, "old_lp": 0.251974454185727, "new_lp": 0.25197444859878654, "gain": 5.586940465818202e-09, "certified_gain": "635710494146740344290018102519235965091760815292142563394715244092835/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 7, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-51-1.json", "dual": "rounds/archive-num-51-1-dual.npz"}

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

2026-11-12 09:52:41 Shipped: candidate, unrefereed C82 < 0.2519744488; the exact certified upper endpoint is below the frozen 0.2519758216 bar. Stop: wall time budget: no new round started after 9.5 hours; the last complete round finished before 10 hours; 25.3227 recorded core-hours.

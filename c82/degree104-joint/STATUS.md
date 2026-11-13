You asked: push the certified C82 upper bound below round 9's 0.2519744488, warm from its final LP state, with frozen bar B < 0.2519744487. I will: reuse our round 9 scripts and full rounds 8–9 bank, alternate LLL numerator pricing and CVP denominator generation, certify each new best, and ship REPORT.md with the best certified value and why search stopped.

2026-11-12: Read machine rules first. Preparing inherited state and prior-art context; no search started. Job limit: 10 hours, at most 6 cores, aggregate RSS 3 GB. No novelty judgment, external writes, or third-party Python reuse.

Copied and reused our round-9 joint LP, numerical helpers, LLL numerator pricing, CVP denominator search, full-bank pricing, mergers, controller, checkpoint code, separately written verifier, controls and source inventory. Warm final LP/dual and full rounds 8–9 coefficient bank retained. Four numerator workers and two CVP workers alternate; sequential solve/verification.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744487408958502183; frozen target not yet met. Source certificate.json

2026-11-12 09:58:07 Round 52: num new-column search on rounds/restricted-52.json, dual rounds/warm-dual.npz.

Baseline replay passed: B upper endpoint 0.2519744487408958502183. Baseline worker peak RSS from logs/baseline-replay.log.time is retained, sampled aggregate 62,930,944 bytes. Search starts at round 52 using the unchanged inherited alternation and 240-second generation budgets. The effective niceness inherits the launcher; run_local.sh adds nice -n 10.

Measured solo num worker: maximum resident set size 108478464 bytes; times planned 4 workers = 433913856 bytes. Aggregate RSS in evidence/compute.jsonl.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519744483636100482926; frozen target met. Source rounds/num-52-certificate.json

2026-11-12 10:06:26 Round 52: den new-column search on rounds/restricted-num-52.json, dual rounds/num-52-dual.npz.

Measured solo den worker: maximum resident set size 458342400 bytes; times planned 2 workers = 916684800 bytes. Aggregate RSS in evidence/compute.jsonl.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519721993911815707394; frozen target met. Source rounds/den-52-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519715086773613875439; frozen target met. Source rounds/archive-den-52-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519708914329409044822; frozen target met. Source rounds/archive-den-52-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519708758817242415556; frozen target met. Source rounds/archive-den-52-2-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519708745781637779896; frozen target met. Source rounds/archive-den-52-3-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519708741876694861411; frozen target met. Source rounds/archive-den-52-4-certificate.json

{"round": 52, "old_lp": 0.25197444859878654, "new_lp": 0.25197087410122315, "gain": 3.5744975633855702e-06, "certified_gain": "827809972341371498426864208412224353272550894573244380655366559136585025/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 1, "den": 1}, "empty_rounds": 0, "state": "rounds/restricted-archive-den-52-4.json", "dual": "rounds/archive-den-52-4-dual.npz"}

2026-11-12 10:27:14 Round 53: num new-column search on rounds/restricted-archive-den-52-4.json, dual rounds/archive-den-52-4-dual.npz.

Retained <50 MB: gzip-compressed 54 completed historical JSON/log files and moved 6 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519706569734291206548; frozen target met. Source rounds/num-53-certificate.json

Storage maintenance: completed-history compression alone left 54,640 KiB after round 53 generated thousands of factors. Compressing the immutable round-8/9 provenance bank copies; checkpoint reader will accept gzip. Exact coefficients and live search bank/state remain unchanged.

Controller exited with error after compressed-provenance reader change. Reverted that reader change and restored the exact original bank bytes before investigating. Latest interval-certified packet remains saved.

Failure identified: logs/cg.log, checkpoint() after rounds/archive-num-53-0 interval replay, FileNotFoundError prior_sources/round9-bank.json. The running controller had imported the original checkpoint module before the gzip-reader edit, so it still required the uncompressed bank. Revert restored the original reader and exact bank bytes. Continuing with uncompressed immutable banks until search ends; storage compression will occur only after the last checkpoint reader exits. No numerical method or certificate arithmetic changes. Resume round 53 after its already-certified archive numerator pass 0, then complete its CVP phase and continue round 54. One reverted storage change, no chain of forward fixes.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519705568922036187138; frozen target met. Source rounds/archive-num-53-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519705331588041200670; frozen target met. Source rounds/archive-num-53-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519705208689315963103; frozen target met. Source rounds/archive-num-53-2-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519705206196310184723; frozen target met. Source rounds/archive-num-53-3-certificate.json

2026-11-12 10:52:20 Round 53: den new-column search on rounds/restricted-archive-num-53-3.json, dual rounds/archive-num-53-3-dual.npz.

{"round": 53, "old_lp": 0.25197087410122315, "new_lp": 0.2519705205687971, "gain": 3.5353242605618007e-07, "certified_gain": "81880763723422287920083306711205364411574754464859422039831545598996325/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 6381, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-53-3.json", "dual": "rounds/archive-num-53-3-dual.npz", "interruption": "storage-reader revert; resumed after archive-num-53-0"}

2026-11-12 10:56:58 Round 54: num new-column search on rounds/restricted-54.json, dual rounds/archive-num-53-3-dual.npz.

Retained <50 MB: gzip-compressed 48 completed historical JSON/log files and moved 5 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519704432678604366337; frozen target met. Source rounds/num-54-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519704111419974982724; frozen target met. Source rounds/archive-num-54-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519704092542053585435; frozen target met. Source rounds/archive-num-54-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519704092525472903622; frozen target met. Source rounds/archive-num-54-2-certificate.json

2026-11-12 11:16:33 Round 54: den new-column search on rounds/restricted-archive-num-54-2.json, dual rounds/archive-num-54-2-dual.npz.

{"round": 54, "old_lp": 0.2519705205687971, "new_lp": 0.25197040912346774, "gain": 1.114453293538098e-07, "certified_gain": "25790854594289984352912522786154211200263386395143202570882063236470077/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 173, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-54-2.json", "dual": "rounds/archive-num-54-2-dual.npz"}

2026-11-12 11:20:34 Round 55: num new-column search on rounds/restricted-archive-num-54-2.json, dual rounds/archive-num-54-2-dual.npz.

Retained <50 MB: gzip-compressed 43 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519703266576892167280; frozen target met. Source rounds/num-55-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519703134699978231328; frozen target met. Source rounds/archive-num-55-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519703134638784807905; frozen target met. Source rounds/archive-num-55-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519703134635521491442; frozen target met. Source rounds/archive-num-55-2-certificate.json

2026-11-12 11:38:28 Round 55: den new-column search on rounds/restricted-archive-num-55-2.json, dual rounds/archive-num-55-2-dual.npz.

{"round": 55, "old_lp": 0.25197040912346774, "new_lp": 0.25197031339704146, "gain": 9.572642628574712e-08, "certified_gain": "22183215746689514033394724998905969195461804250362738711343070392677027/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 140, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-55-2.json", "dual": "rounds/archive-num-55-2-dual.npz"}

2026-11-12 11:42:33 Round 56: num new-column search on rounds/restricted-archive-num-55-2.json, dual rounds/archive-num-55-2-dual.npz.

Retained <50 MB: gzip-compressed 41 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519702549356610143481; frozen target met. Source rounds/num-56-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519702418294985013197; frozen target met. Source rounds/archive-num-56-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519702406448529829683; frozen target met. Source rounds/archive-num-56-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519702402431479415521; frozen target met. Source rounds/archive-num-56-2-certificate.json

2026-11-12 12:00:31 Round 56: den new-column search on rounds/restricted-archive-num-56-2.json, dual rounds/archive-num-56-2-dual.npz.

{"round": 56, "old_lp": 0.25197031339704146, "new_lp": 0.2519702402056662, "gain": 7.319137523831287e-08, "certified_gain": "16956687155995733166207459378020753370544631488660590052676219606754317/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 60, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-56-2.json", "dual": "rounds/archive-num-56-2-dual.npz"}

2026-11-12 12:04:35 Round 57: num new-column search on rounds/restricted-archive-num-56-2.json, dual rounds/archive-num-56-2-dual.npz.

Retained <50 MB: gzip-compressed 41 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701810491955385478; frozen target met. Source rounds/num-57-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701671089259256032; frozen target met. Source rounds/archive-num-57-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701646401094087763; frozen target met. Source rounds/archive-num-57-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701646225972651800; frozen target met. Source rounds/archive-num-57-2-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701646163025007679; frozen target met. Source rounds/archive-num-57-3-certificate.json

2026-11-12 12:26:40 Round 57: den new-column search on rounds/restricted-archive-num-57-3.json, dual rounds/archive-num-57-3-dual.npz.

{"round": 57, "old_lp": 0.2519702402056662, "new_lp": 0.25197016455080873, "gain": 7.565485748983747e-08, "certified_gain": "8756990436016006923718703044239895973729778206851682982657867601082099/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 45, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-57-3.json", "dual": "rounds/archive-num-57-3-dual.npz"}

2026-11-12 12:30:45 Round 58: num new-column search on rounds/restricted-archive-num-57-3.json, dual rounds/archive-num-57-3-dual.npz.

Retained <50 MB: gzip-compressed 48 completed historical JSON/log files and moved 5 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701409711713477963; frozen target met. Source rounds/num-58-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701378249042539103; frozen target met. Source rounds/archive-num-58-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701376820479644017; frozen target met. Source rounds/archive-num-58-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701376742646491579; frozen target met. Source rounds/archive-num-58-2-certificate.json

2026-11-12 12:52:19 Round 58: den new-column search on rounds/restricted-archive-num-58-3.json, dual rounds/archive-num-58-3-dual.npz.

{"round": 58, "old_lp": 0.25197016455080873, "new_lp": 0.2519701376078788, "gain": 2.6942929942652682e-08, "certified_gain": "779918712787194052151740918783426976050694581750414654013137189714191/28948022309329048855892746252171976963317496166410141009864396001978282409984", "negative_candidates": {"num": 15, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-58-3.json", "dual": "rounds/archive-num-58-3-dual.npz"}

2026-11-12 12:56:25 Round 59: num new-column search on rounds/restricted-archive-num-58-3.json, dual rounds/archive-num-58-3-dual.npz.

Retained <50 MB: gzip-compressed 48 completed historical JSON/log files and moved 5 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701198684158519709; frozen target met. Source rounds/num-59-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701082100713963646; frozen target met. Source rounds/archive-num-59-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701080949901588044; frozen target met. Source rounds/archive-num-59-1-certificate.json

2026-11-12 13:11:03 Round 59: den new-column search on rounds/restricted-archive-num-59-1.json, dual rounds/archive-num-59-1-dual.npz.

{"round": 59, "old_lp": 0.2519701376078788, "new_lp": 0.2519701080495717, "gain": 2.9558307079735613e-08, "certified_gain": "3425045991362081292290007853134211291664973520854583108143789076075055/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 5, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-59-1.json", "dual": "rounds/archive-num-59-1-dual.npz"}

2026-11-12 13:15:09 Round 60: num new-column search on rounds/restricted-archive-num-59-1.json, dual rounds/archive-num-59-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701033860790817734; frozen target met. Source rounds/num-60-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701019879526459950; frozen target met. Source rounds/archive-num-60-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701019146864158811; frozen target met. Source rounds/archive-num-60-1-certificate.json

2026-11-12 13:30:55 Round 60: den new-column search on rounds/restricted-archive-num-60-1.json, dual rounds/archive-num-60-1-dual.npz.

{"round": 60, "old_lp": 0.2519701080495717, "new_lp": 0.2519701018881778, "gain": 6.161393895087741e-09, "certified_gain": "1431260565028597218700948588027386163747603430988381808530514250111891/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 25, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-60-1.json", "dual": "rounds/archive-num-60-1-dual.npz"}

2026-11-12 13:34:59 Round 61: num new-column search on rounds/restricted-archive-num-60-1.json, dual rounds/archive-num-60-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519701003089294512529; frozen target met. Source rounds/num-61-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519700995590095248089; frozen target met. Source rounds/archive-num-61-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519700995255770827495; frozen target met. Source rounds/archive-num-61-1-certificate.json

2026-11-12 13:51:18 Round 61: den new-column search on rounds/restricted-archive-num-61-1.json, dual rounds/archive-num-61-1-dual.npz.

{"round": 61, "old_lp": 0.2519701018881778, "new_lp": 0.2519700993758037, "gain": 2.5123740865495847e-09, "certified_gain": "553279922199343971980314974040625052476185439320889504974996905262995/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 8, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-61-1.json", "dual": "rounds/archive-num-61-1-dual.npz"}

2026-11-12 13:55:28 Round 62: num new-column search on rounds/restricted-archive-num-61-1.json, dual rounds/archive-num-61-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519700771508652344623; frozen target met. Source rounds/num-62-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519700697445381351414; frozen target met. Source rounds/archive-num-62-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519700693676131732153; frozen target met. Source rounds/archive-num-62-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519700693297235469357; frozen target met. Source rounds/archive-num-62-2-certificate.json

2026-11-12 14:21:30 Round 62: den new-column search on rounds/restricted-archive-num-62-2.json, dual rounds/archive-num-62-2-dual.npz.

{"round": 62, "old_lp": 0.2519700993758037, "new_lp": 0.2519700692323277, "gain": 3.0143476048571927e-08, "certified_gain": "6992881934431769068368049454836431161791818556667696835397719429503723/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 8, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-62-2.json", "dual": "rounds/archive-num-62-2-dual.npz"}

2026-11-12 14:25:33 Round 63: num new-column search on rounds/restricted-archive-num-62-2.json, dual rounds/archive-num-62-2-dual.npz.

Retained <50 MB: gzip-compressed 41 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519700478466489598357; frozen target met. Source rounds/num-63-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519700466524985479611; frozen target met. Source rounds/archive-num-63-0-certificate.json

2026-11-12 14:40:46 Round 63: den new-column search on rounds/restricted-archive-num-63-1.json, dual rounds/archive-num-63-1-dual.npz.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519699550370236792876; frozen target met. Source rounds/den-63-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519699306108476293157; frozen target met. Source rounds/archive-den-63-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519699209755793776153; frozen target met. Source rounds/archive-den-63-1-certificate.json

{"round": 63, "old_lp": 0.2519700692323277, "new_lp": 0.2519699209239473, "gain": 1.4830838035440053e-07, "certified_gain": "8589118150189814042506963127195075329877017552175626797475839750756309/57896044618658097711785492504343953926634992332820282019728792003956564819968", "negative_candidates": {"num": 6, "den": 1}, "empty_rounds": 0, "state": "rounds/restricted-archive-den-63-1.json", "dual": "rounds/archive-den-63-1-dual.npz"}

2026-11-12 14:55:03 Round 64: num new-column search on rounds/restricted-archive-den-63-1.json, dual rounds/archive-den-63-1-dual.npz.

Retained <50 MB: gzip-compressed 56 completed historical JSON/log files and moved 6 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519699039526871287723; frozen target met. Source rounds/num-64-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519698975649027384446; frozen target met. Source rounds/archive-num-64-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519698972319870586830; frozen target met. Source rounds/archive-num-64-1-certificate.json

2026-11-12 15:11:10 Round 64: den new-column search on rounds/restricted-archive-num-64-1.json, dual rounds/archive-num-64-1-dual.npz.

{"round": 64, "old_lp": 0.2519699209239473, "new_lp": 0.25196989714812645, "gain": 2.3775820867655284e-08, "certified_gain": "5498640321216515634706430043712457980485649472372973600239997657730803/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 62, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-64-1.json", "dual": "rounds/archive-num-64-1-dual.npz"}

2026-11-12 15:15:17 Round 65: num new-column search on rounds/restricted-archive-num-64-1.json, dual rounds/archive-num-64-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519698801657834857450; frozen target met. Source rounds/num-65-certificate.json

Restored active logs/cg54.log from Trash before investigating a retention failure: inherited compact_history.py excluded only cg.log, whereas the resumed controller writes cg54.log. Restoring the moved open file preserves ongoing writes. Excluding all cg-prefixed controller logs from history compression; numerical search is unaffected.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519698756064185768273; frozen target met. Source rounds/archive-num-65-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519698744301589656438; frozen target met. Source rounds/archive-num-65-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519698744039141917153; frozen target met. Source rounds/archive-num-65-2-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519698743853822661150; frozen target met. Source rounds/archive-num-65-3-certificate.json

2026-11-12 15:39:42 Round 65: den new-column search on rounds/restricted-archive-num-65-3.json, dual rounds/archive-num-65-3-dual.npz.

{"round": 65, "old_lp": 0.25196989714812645, "new_lp": 0.2519698742611721, "gain": 2.2886954331724496e-08, "certified_gain": "5290912201821472020771774575790035726221231707378272900263319069995889/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 28, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-65-3.json", "dual": "rounds/archive-num-65-3-dual.npz"}

2026-11-12 15:43:48 Round 66: num new-column search on rounds/restricted-archive-num-65-3.json, dual rounds/archive-num-65-3-dual.npz.

Retained <50 MB: gzip-compressed 48 completed historical JSON/log files and moved 5 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519698376397044015599; frozen target met. Source rounds/num-66-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519698362884997030401; frozen target met. Source rounds/archive-num-66-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519698362382866261034; frozen target met. Source rounds/archive-num-66-1-certificate.json

2026-11-12 16:00:56 Round 66: den new-column search on rounds/restricted-archive-num-66-1.json, dual rounds/archive-num-66-1-dual.npz.

{"round": 66, "old_lp": 0.2519698742611721, "new_lp": 0.2519698361030846, "gain": 3.815808752305472e-08, "certified_gain": "8834263804985307382004911780873250885783670806739332735667400255457239/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 18, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-66-1.json", "dual": "rounds/archive-num-66-1-dual.npz"}

2026-11-12 16:04:58 Round 67: num new-column search on rounds/restricted-archive-num-66-1.json, dual rounds/archive-num-66-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697802682457170610; frozen target met. Source rounds/num-67-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697795470309756543; frozen target met. Source rounds/archive-num-67-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697795448715583932; frozen target met. Source rounds/archive-num-67-1-certificate.json

2026-11-12 16:20:01 Round 67: den new-column search on rounds/restricted-archive-num-67-1.json, dual rounds/archive-num-67-1-dual.npz.

{"round": 67, "old_lp": 0.2519698361030846, "new_lp": 0.2519697794268419, "gain": 5.6676242699005286e-08, "certified_gain": "6564648976688502897420574313123657356629854420633243360586496576540563/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 28, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-67-1.json", "dual": "rounds/archive-num-67-1-dual.npz"}

2026-11-12 16:24:04 Round 68: num new-column search on rounds/restricted-archive-num-67-1.json, dual rounds/archive-num-67-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697700435811365310; frozen target met. Source rounds/num-68-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697688862358922029; frozen target met. Source rounds/archive-num-68-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697687058445278919; frozen target met. Source rounds/archive-num-68-1-certificate.json

2026-11-12 16:39:30 Round 68: den new-column search on rounds/restricted-archive-num-68-1.json, dual rounds/archive-num-68-1-dual.npz.

{"round": 68, "old_lp": 0.2519697794268419, "new_lp": 0.251969768636683, "gain": 1.0790158877505007e-08, "certified_gain": "2510147170322977106583402314096070531344971945267386497402762061256023/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 14, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-68-1.json", "dual": "rounds/archive-num-68-1-dual.npz"}

2026-11-12 16:43:36 Round 69: num new-column search on rounds/restricted-archive-num-68-1.json, dual rounds/archive-num-68-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697566295345487509; frozen target met. Source rounds/num-69-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697447849513001516; frozen target met. Source rounds/archive-num-69-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697444787321183747; frozen target met. Source rounds/archive-num-69-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697444309899492717; frozen target met. Source rounds/archive-num-69-2-certificate.json

2026-11-12 17:02:48 Round 69: den new-column search on rounds/restricted-archive-num-69-2.json, dual rounds/archive-num-69-2-dual.npz.

{"round": 69, "old_lp": 0.251969768636683, "new_lp": 0.25196974434941527, "gain": 2.4287267752498565e-08, "certified_gain": "2810836127590467697887750219031159372465575816297520510033346308201217/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 13, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-69-2.json", "dual": "rounds/archive-num-69-2-dual.npz"}

2026-11-12 17:06:51 Round 70: num new-column search on rounds/restricted-archive-num-69-2.json, dual rounds/archive-num-69-2-dual.npz.

Retained <50 MB: gzip-compressed 41 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697399423353042115; frozen target met. Source rounds/num-70-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697397710727986431; frozen target met. Source rounds/archive-num-70-0-certificate.json

2026-11-12 17:22:28 Round 70: den new-column search on rounds/restricted-archive-num-70-1.json, dual rounds/archive-num-70-1-dual.npz.

{"round": 70, "old_lp": 0.25196974434941527, "new_lp": 0.25196973972722847, "gain": 4.6221867999740596e-09, "certified_gain": "539581542544080730547711322736237095454043188963974027219359034591829/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 3, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-70-1.json", "dual": "rounds/archive-num-70-1-dual.npz"}

2026-11-12 17:26:34 Round 71: num new-column search on rounds/restricted-archive-num-70-1.json, dual rounds/archive-num-70-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697074934228303978; frozen target met. Source rounds/num-71-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519697074695009521597; frozen target met. Source rounds/archive-num-71-0-certificate.json

2026-11-12 17:38:16 Round 71: den new-column search on rounds/restricted-archive-num-71-0.json, dual rounds/archive-num-71-0-dual.npz.

{"round": 71, "old_lp": 0.25196973972722847, "new_lp": 0.25196970742035274, "gain": 3.230687573019253e-08, "certified_gain": "7480532979507190840047455486393595704035669021891273854803915439293877/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 12, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-71-0.json", "dual": "rounds/archive-num-71-0-dual.npz"}

2026-11-12 17:42:22 Round 72: num new-column search on rounds/restricted-archive-num-71-0.json, dual rounds/archive-num-71-0-dual.npz.

Retained <50 MB: gzip-compressed 27 completed historical JSON/log files and moved 2 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696923919829443641; frozen target met. Source rounds/num-72-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696919492684037895; frozen target met. Source rounds/archive-num-72-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696918668373583289; frozen target met. Source rounds/archive-num-72-1-certificate.json

2026-11-12 17:59:22 Round 72: den new-column search on rounds/restricted-archive-num-72-1.json, dual rounds/archive-num-72-1-dual.npz.

{"round": 72, "old_lp": 0.25196970742035274, "new_lp": 0.25196969178617656, "gain": 1.56341761758938e-08, "certified_gain": "451666253799167873491544909899142028854271551194903068466519874958591/28948022309329048855892746252171976963317496166410141009864396001978282409984", "negative_candidates": {"num": 7, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-72-1.json", "dual": "rounds/archive-num-72-1-dual.npz"}

2026-11-12 18:03:28 Round 73: num new-column search on rounds/restricted-archive-num-72-1.json, dual rounds/archive-num-72-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696855073195027914; frozen target met. Source rounds/num-73-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696838485545427829; frozen target met. Source rounds/archive-num-73-0-certificate.json

2026-11-12 18:19:01 Round 73: den new-column search on rounds/restricted-archive-num-73-1.json, dual rounds/archive-num-73-1-dual.npz.

{"round": 73, "old_lp": 0.25196969178617656, "new_lp": 0.2519696837272746, "gain": 8.058901990182221e-09, "certified_gain": "232113429826936272032332890778909098365565670781326254155560713511135/28948022309329048855892746252171976963317496166410141009864396001978282409984", "negative_candidates": {"num": 2, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-73-1.json", "dual": "rounds/archive-num-73-1-dual.npz"}

2026-11-12 18:23:08 Round 74: num new-column search on rounds/restricted-archive-num-73-1.json, dual rounds/archive-num-73-1-dual.npz.

Retained <50 MB: gzip-compressed 34 completed historical JSON/log files and moved 3 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696838407989711246; frozen target met. Source rounds/num-74-certificate.json

2026-11-12 18:30:53 Round 74: den new-column search on rounds/restricted-num-74.json, dual rounds/num-74-dual.npz.

{"round": 74, "old_lp": 0.2519696837272746, "new_lp": 0.25196968372239653, "gain": 4.8780424144467815e-12, "certified_gain": "1796067691084601814277724045360370090649845212884564538651627674657/231584178474632390847141970017375815706539969331281128078915168015826259279872", "negative_candidates": {"num": 1, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-num-74.json", "dual": "rounds/num-74-dual.npz"}

2026-11-12 18:34:59 Round 75: num new-column search on rounds/restricted-num-74.json, dual rounds/num-74-dual.npz.

Retained <50 MB: gzip-compressed 20 completed historical JSON/log files and moved 1 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696713893781389883; frozen target met. Source rounds/num-75-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696641205468018945; frozen target met. Source rounds/archive-num-75-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696634558014924161; frozen target met. Source rounds/archive-num-75-1-certificate.json

2026-11-12 18:54:13 Round 75: den new-column search on rounds/restricted-archive-num-75-2.json, dual rounds/archive-num-75-2-dual.npz.

{"round": 75, "old_lp": 0.25196968372239653, "new_lp": 0.2519696633733395, "gain": 2.0349057050506048e-08, "certified_gain": "18440792555914682022020759081994996585723828267772608793423151711915/904625697166532776746648320380374280103671755200316906558262375061821325312", "negative_candidates": {"num": 4, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-75-2.json", "dual": "rounds/archive-num-75-2-dual.npz"}

2026-11-12 18:58:19 Round 76: num new-column search on rounds/restricted-archive-num-75-2.json, dual rounds/archive-num-75-2-dual.npz.

Retained <50 MB: gzip-compressed 41 completed historical JSON/log files and moved 4 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696622782126203691; frozen target met. Source rounds/num-76-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696621614668879326; frozen target met. Source rounds/archive-num-76-0-certificate.json

2026-11-12 19:10:19 Round 76: den new-column search on rounds/restricted-archive-num-76-0.json, dual rounds/archive-num-76-0-dual.npz.

{"round": 76, "old_lp": 0.2519696633733395, "new_lp": 0.2519696621037062, "gain": 1.269633287392935e-09, "certified_gain": "149873708025303220426357517532140300419691567873988954028544617958395/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 4, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-76-0.json", "dual": "rounds/archive-num-76-0-dual.npz"}

2026-11-12 19:14:25 Round 77: num new-column search on rounds/restricted-archive-num-76-0.json, dual rounds/archive-num-76-0-dual.npz.

Retained <50 MB: gzip-compressed 27 completed historical JSON/log files and moved 2 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

Retention wording correction: the inherited compactor message “Retained <50 MB” described its intended limit, not a measured current packet size. Final logical size will be measured after compressing the immutable banks with search stopped. All certified best packets and replays remain retained.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696461145342816245; frozen target met. Source rounds/num-77-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519696459872491000812; frozen target met. Source rounds/archive-num-77-0-certificate.json

2026-11-12 19:26:17 Round 77: den new-column search on rounds/restricted-archive-num-77-0.json, dual rounds/archive-num-77-0-dual.npz.

{"round": 77, "old_lp": 0.2519696621037062, "new_lp": 0.2519696459222134, "gain": 1.6181492812350484e-08, "certified_gain": "1872846469434676362936651226130133419081644534543144337540822752449509/115792089237316195423570985008687907853269984665640564039457584007913129639936", "negative_candidates": {"num": 6, "den": 0}, "empty_rounds": 0, "state": "rounds/restricted-archive-num-77-0.json", "dual": "rounds/archive-num-77-0-dual.npz"}

Compressed completed history: gzip-compressed 27 completed historical JSON/log files and moved 2 old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.

2026-11-12 19:32:32 Shipped: candidate, unrefereed C82 < 0.2519696460; the exact certified upper endpoint is below the frozen 0.2519744487 bar. Stop: wall time budget: no new round started after 9.5 hours; final packet time reserved; 27.7740 recorded core-hours.

Search and finalizer have exited. Compressing the immutable provenance banks and final mutable union bank only now, after every checkpoint reader has stopped. Restore commands for warm/resumed search are in REPRODUCE.md.

Final retained packet size measured: 53,828,989 bytes; wall time 9.642 hours.

Final retention: ordinary history and bank compression left 53,828,989 bytes, above the 50,000,000-byte packet limit. Reusing round 9’s final cleanup method: retire redundant compressed floating LP master caches to reversible Trash, preserving warm and final LP states/duals, the complete coefficient banks, every best certificate/replay and all Python sources. Exact bounds and certificates are unaffected.

Retired 189 redundant floating state archives to reversible macOS Trash. Measured retained packet: 38,483,326 bytes (38.5 MB); warm/final states and every certified best retained.

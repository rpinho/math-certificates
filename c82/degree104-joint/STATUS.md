You asked: get a certified C82 upper bound below #280 v6's 0.2519694883 by combining our round-11 bank with their v6 columns and then searching higher-degree numerators. I will: replay both certificates, run the merged search, and ship the best certified value and what stopped the search.

2026-11-20 04:35:29 EST Certified #280 v6 exact incumbent upper endpoint 0.2519694882727008797941. Saved certificates/best_0.2519694882727008797941.json.

2026-11-20 04:37:09 EST Certified union-master upper endpoint 0.2519694780462110150323. Saved certificates/best_0.2519694780462110150323.json.

2026-11-20 04:40:24 EST Certified union-0 upper endpoint 0.2519694777811065577145. Saved certificates/best_0.2519694777811065577145.json.

2026-11-20 04:40:27 EST Full-bank union pricing complete. Best certified endpoint 0.2519694777811065577145

2026-11-20 04:40:37 EST Step 0a passed both pinned replays. Step 0b checked 2,622,668 nonzero pair resultants and exact weight representability at D=740384615402384615382720. P1=X and P2=X−1 are endpoint-root exceptions in both inputs. All 118 denominators are endpoint-free. Retained the required incumbent and these inherited numerators. The 16 v6 additions have degrees 24×2, 26×2, 28×3, 30×1, 31×2, 33×2, 34×3 and 42×1. Our 22,212-factor bank has 2,071 factors at 24–48. Full counts are in evidence/degrees.json.

2026-11-20 04:40:37 EST Initial joint master measured 301,924,352 bytes sampled group RSS. Four bank workers together peaked at 574,636,032 bytes. Round 11 solo maximum RSS on these LLL/CVP kernels was 119,554,048 / 535,003,136 bytes. All round-12 compute batches are timed and the group guard uses a 2.8 GB stop threshold.

2026-11-20 04:40:53 EST Alternation 1 on rounds/union-0. Certified incumbent 0.2519694777811065577145.

2026-11-20 04:41:45 EST Closed full-bank union at 0.2519694777811065577145 (outward endpoint). Pricing added one archived round-10 numerator and a second scan found no omitted negative column at tolerance 1e-10. The union gained over 1e-10 versus exact v6, so both search arms continue.

2026-11-20 04:46:19 EST Certified new-num-1 upper endpoint 0.2519694777669961914660. Saved certificates/best_0.2519694777669961914660.json.

2026-11-20 04:50:29 EST Alternation 1 certified gain 1.411e-11, streak 1, archived endpoint 0.2519694777669961914660.

2026-11-20 04:50:29 EST Alternation 2 on rounds/new-num-1. Certified incumbent 0.2519694777669961914660.

2026-11-20 04:53:46 EST Degree-116 CVP stopped after 248.16 seconds. Nine trials, 354 priced evaluations, minimum reduced cost +0.0210055321 among previously absent candidates. No negative column. First 104/116 CVP workers measured 511,279,104 and 495,435,776 bytes maximum RSS; the main-band LLL worker measured 114,098,176 bytes.

2026-11-20 04:55:56 EST Certified new-num-2 upper endpoint 0.2519694758381300658953. Saved certificates/best_0.2519694758381300658953.json.

2026-11-20 05:00:05 EST Alternation 2 certified gain 1.9289e-09, streak 0, archived endpoint 0.2519694758381300658953.

2026-11-20 05:00:05 EST Alternation 3 on rounds/new-num-2. Certified incumbent 0.2519694758381300658953.

2026-11-20 05:08:09 EST Alternation 3 certified gain 0, streak 1, archived endpoint 0.2519694758381300658953.

2026-11-20 05:08:09 EST Alternation 4 on rounds/new-num-2. Certified incumbent 0.2519694758381300658953.

2026-11-20 05:16:19 EST Alternation 4 certified gain 0, streak 2, archived endpoint 0.2519694758381300658953.

2026-11-20 05:16:19 EST Alternation 5 on rounds/new-num-2. Certified incumbent 0.2519694758381300658953.

2026-11-20 05:24:24 EST Alternation 5 certified gain 0, streak 3, archived endpoint 0.2519694758381300658953.

2026-11-20 05:24:24 EST Alternation 6 on rounds/new-num-2. Certified incumbent 0.2519694758381300658953.

2026-11-20 05:32:32 EST Alternation 6 certified gain 0, streak 4, archived endpoint 0.2519694758381300658953.

2026-11-20 05:32:32 EST Alternation 7 on rounds/new-num-2. Certified incumbent 0.2519694758381300658953.

2026-11-20 05:40:38 EST Alternation 7 certified gain 0, streak 5, archived endpoint 0.2519694758381300658953.

2026-11-20 05:41:40 EST Closed at C82 < 0.2519694759, candidate and unrefereed, after five consecutive zero-gain alternations. Final replay at the stated rational passed. REPORT.md contains the endpoint, comparator gaps, full credit and compute. All worker sessions exited and the final ps check found no remaining job workers.

# Referee attempts and exclusions

- The independent transfer graph and exact finite evaluator were written
  before reading the producer's native verifier source. Neither producer
  executable was run. Boost headers were missing on the pod; a public
  Debian Boost development package was extracted inside this job directory.
  The package SHA256 is
  `ba14fe04d7f138f874bd3ab3a20c4fd1e9f654e271449b8f3e48d20f942dbb93`.
- The first exact span-1 result matched its closed form. Literal span-2
  coefficients matched the public table, after which the main independent
  batch was launched. Completed spans 1–10 found no mismatch.
- A memory-only change discards consumed stage numerators in exact mode.
  It changes neither transitions nor arithmetic values. Larger-span state
  keys were then widened from 64 to 128 bits with exact key comparison;
  terminal and connectivity rules were unchanged.
- The recorded large-span session used a fixed 14:25 UTC cutoff. After
  launch, the local scheduling helper's future default was made relative
  (10,000 seconds, configurable by `REFEREE_LARGE_TIMEOUT_SECONDS`) so that
  later reproduction does not silently skip jobs after the historical date.
  This scheduling change does not alter the already running session or any
  enumeration/arithmetic code. Final-source controls reproduce the original
  span-10 coefficients and span-1 exact value/tail.
- The final reproduction helpers accept `REFEREE_WORKERS` to reduce their
  six-worker pod default to four on the Mini. This changes scheduling only;
  the recorded runs preceded this convenience option.
- The first draft of the *baseline arithmetic* script mistakenly divided
  its homogeneous Horner value by an extra factor q. The resulting assertion
  failure was a referee-script error, not an enumeration mismatch. Removing
  that spurious division gives the polynomial's correct homogeneous value;
  the final source and saved baseline result use that formula. No producer
  checker was used to obtain the result.
- A direct minimum-row-contact rectangle implementation passed the complete
  small literal control. Full range-22 and range-23 runs use its 160-bit
  directed arithmetic.
- A native 128-bit arithmetic variant at scale 2^112 also passed that
  literal control. Two large pilots were stopped voluntarily after about
  496 seconds: measured column timings did not predict an earlier finish
  than the already running 160-bit computations. Their return code −15
  means deliberate termination, not a detected mismatch. No partial pilot
  value is used as evidence; see `results/pod/FAST_RECT_STOP.json`.
- One attempted shell invocation of the optional-pilot stop command failed
  at quoting/parsing before any process was stopped. A standalone Python
  script was then copied to the job directory and stopped the two recorded
  pilot PIDs. No other job's processes were targeted.
- Three local SSH clients remained open after their remote controllers had
  exited. After confirming the remote jobs' receipts and absence of those
  controllers, the exact three client PIDs were terminated. SSH multiplexing
  was disabled. This closes idle transport processes, not enumeration jobs;
  the resulting SSH exit 255 is not a mathematical or native-run failure.
  See `results/SSH_CLEANUP.json`.
- The long heavy-batch SSH transport reported a connection reset. The remote
  controller and its workers continued, and the subsequently fetched
  `HEAVY_BATCH.json` records return code zero for all eight native tasks.
  Final independent comparisons and process checks passed. Transport exit
  status is not being substituted for a native completion receipt.

All comparison outcomes used by the report come from the final named
comparison scripts and completed output files. A resource stop, dependency
failure or corrected referee implementation error is not presented as a
counterexample to the candidate.

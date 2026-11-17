# BMB window20: pinned inputs and recorded replay

The authors' code and lists are not bundled. Obtain them at revised-manuscript commit `2842ef3a58604a8f4b35271d5753c2bf9bdecd0b`:

| File | SHA-256 |
|---|---|
| [check_window.c](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/checks/window20/check_window.c) | `a287d48122c50e5de80a49d7d7416687d45936c47fa8ab09e891d2979bbf784d` |
| [certs_11.txt](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/checks/window20/certs_11.txt) | `f1a6dc2832c3257c6df1e962b34e4d272a24a62d2824716786281e37e47de29d` |
| [certs_19_22.txt](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/checks/window20/certs_19_22.txt) | `f13c6afa9a72fa530eac18d09f7da7741b6d5375308cbad0a2056980f9e2e7f5` |
| [run_checks.sh](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/checks/window20/run_checks.sh) | `260dd1b4b3d67e3386924da78f12a02ed36cbca1cee5fe5db20c3fc350d99115` |

The byte-preserved raw [out/window20_replay.txt](out/window20_replay.txt), supplied by the clean-room referee, records PASS for the 288 eleven-coordinate certificates and for the 63,272 nineteen-coordinate certificates (5,308,416 patterns, 242 settled by pivots, 708,872 word choices, least pair 22). All three supplied corruptions were rejected. This is the referee's recorded output, not a new packaging run.

The referee wrote its own size-only check, whose output is in out/splitsum_n19.log and out/splitsum_n19_p*.txt. It did not reimplement the authors' mixed-level case analysis. Thus f(22)=13 uses thm:f20 through lem:window20; without it, 12≤f(22)≤13. The existing f(20) dependency is the same. The f(24) flower bound does not use this computation. Candidate, no human review.

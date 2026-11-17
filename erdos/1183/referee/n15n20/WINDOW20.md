# BMB window20 dependency and recorded referee replay

Source: Bhattacharjee–Mandal–Bhattacharya, revised manuscript commit `2842ef3a58604a8f4b35271d5753c2bf9bdecd0b`. Authors’ files are obtained separately from pinned URLs; none is bundled in this packet.

| Authors’ file | SHA-256 |
|---|---|
| [check_window.c](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/checks/window20/check_window.c) | `a287d48122c50e5de80a49d7d7416687d45936c47fa8ab09e891d2979bbf784d` |
| [certs_19_22.txt](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/checks/window20/certs_19_22.txt) | `f13c6afa9a72fa530eac18d09f7da7741b6d5375308cbad0a2056980f9e2e7f5` |
| [certs_11.txt](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/checks/window20/certs_11.txt) | `f1a6dc2832c3257c6df1e962b34e4d272a24a62d2824716786281e37e47de29d` |

The byte-preserved REFEREE.md records this output (transcribed from that report; a separate raw stdout file was not supplied):

```text
63272 certificates, 5308416 patterns, 242 settled by pivots, 708872 word choices, least pair 22 / PASS
```

It also records least pair 13 for certs_11.txt, and rejection of three corrupted lists: target 23, pivot families removed, and one member deleted. The referee read the reduction and replayed the authors’ C checker; it did not reimplement the mixed-level computation. Its own rank-only check is preserved in `out/split_n19_K22.txt` and does not replace that computation. This packaging job did not rerun or bundle third-party code. The equality f(20)=12 retains this dependency; otherwise 11≤f(20)≤12.

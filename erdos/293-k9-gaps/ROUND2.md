# Round 2 of the D₉ gap search

I resumed the ordered search at 16,762,189 on 2026-11-24 at 20:00 UTC with eight workers, the same driver, and the existing C/GMP solver binary. The run ended at 01:55:35 UTC on 2026-11-25. The driver reported the first-omission regression at 13,856,993 with all 1,412 shards and zero skips. It also reported six verified nearby composite witnesses before the resumed search. [Round-2 driver log](logs/gap-driver-round2.log).

I added twelve exhaustive zeros (`16,767,637`, `16,796,999`, `16,932,329`, `17,012,789`, `17,222,137`, `17,256,539`, `17,284,343`, `17,434,961`, `17,850,913`, `17,854,283`, `17,859,497` and `17,867,767`) and 113 exact witnesses. The combined table contains **20 exhaustive zeros** including the candidate second missing integer **13,878,989**, and **165 exact witnesses**. The last settled gap is **17,938,507**. The round-2 log and table give the exact witness for 16,762,189. The summary in its original directory records the round-1 pilot. [Gap table](gaps.tsv), [round-1 pilot](logs/k9-16762189/summary.json).

I stopped at **17,945,717**, the first of **438 unsettled gaps** below 20,000,000. The pilot checked 14 of 1,398 shards, with zero witnesses and 1,384 shards still unsearched. Its estimated 318.9 seconds exceeded the 273.5 seconds remaining before the driver's search cutoff. [Pilot estimate](logs/k9-17945717/pilot.tsv), [pilot summary](logs/k9-17945717/summary.json).

I checked that the following SHA-256 digests match between the round-2 run and the published round-1 copies.

| File | Shared SHA-256 |
|---|---|
| `solver.c` | `43be51de4ad7c3239871d379bccb1036a27e0ee31fa5e3caf11444b656fca1aa` |
| `run_gaps.py` | `7e4f6f6b6bf3dc3bce9a17c87a91eeb3d0f7ea3f3fcd84d33d358b02ee41dacd` |
| `geometry.py` | `d703914e6ae74873d745ace3728a1ff8f283d1601054a4c1455ea8a8a887494f` |
| `controls.py` | `b0996cbfbf64101f21290d68e2b77ceecbfbc4f5b1f44c2560d9b654c2e2c067` |
| `prepare_gaps.py` | `f9ab00810e945dce00d8a12e203ee49440f5ceec1b6e6de5e8e7577df177d385` |
| `check_certificates.c` | `bfd2d04b620589bd076ae2cfc782d29bd9de96642dd7f171cb048260da9978c8` |
| `enumerator.c` | `f5ca5ed7fbfb05f40793f32e8fc85bbc19ccf8225ef082c46be7d7a4eb47b949` |
| `Makefile` | `bee4e230ef41b19f71fda946fc05a50d2216c26a482c5c49eadcda9ca69d21c2` |

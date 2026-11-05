# Third-party code and data

This folder redistributes files from [vidigoat/optimization-records](https://github.com/vidigoat/optimization-records) by V. Patankar (@vidigoat), at commit [3a7a84f](https://github.com/vidigoat/optimization-records/tree/3a7a84fec9c64ae426f06a5f52597c84b3453ba0). That repository is under the MIT License, copyright (c) 2026 Vidit Patankar. The full licence text is in [LICENSE-vidigoat-optimization-records.txt](LICENSE-vidigoat-optimization-records.txt) and applies to the files below.

| File here | Origin in vidigoat/optimization-records@3a7a84f | Changes |
|---|---|---|
| `core.py` | `tao/certificates/c82/v2/search/core.py` | none (byte-identical, git blob 395522d6) |
| `wlp.py` | `tao/certificates/c82/v2/search/wlp.py` | one added option, `setOptionValue('threads', 1)` |
| `prior_sources/certificate.json`, `prior_sources/final_state_lp.json`, `prior_sources/VIDIGOAT_README.original.txt`, `prior_sources/vidigoat_*.json`, `prior_sources/final/vidigoat_*.json` | the #280 certificate, LP state, README and listings | JSON transport metadata only, as recorded in MANIFEST.json |

The search scripts `cvp_search.py`, `cvp_gram.py`, `cvp_fixed.py`, `cvp_profile.py`, `solve_lp.py` and `check_numerics.py` import `core.py`, and `solve_lp.py` imports `wlp.py`. The certificate check does not: `verify_interval.py` and the referee checker `review/replay/check.py` use only the Python standard library and python-flint.

An earlier version of METHOD.md, REPRODUCE.md and prior_sources/README.md said that no vidigoat module was imported, and called `core.py` and `wlp.py` copies of our own code. Both statements were wrong and are corrected here.

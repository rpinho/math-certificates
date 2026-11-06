# Third-party data

This packet redistributes data, not code, from [vidigoat/optimization-records](https://github.com/vidigoat/optimization-records/tree/79ce0dfb211a67ff7e387b58b0d19ff1d6accfba), by V. Patankar (@vidigoat), at commits [79ce0df](https://github.com/vidigoat/optimization-records/tree/79ce0dfb211a67ff7e387b58b0d19ff1d6accfba), [197962c](https://github.com/vidigoat/optimization-records/tree/197962c9610f583e9bc56efe37bfb994c1eeb834) and [3a7a84f](https://github.com/vidigoat/optimization-records/tree/3a7a84fec9c64ae426f06a5f52597c84b3453ba0). The MIT License, copyright (c) 2026 Vidit Patankar, is preserved in LICENSE-vidigoat-optimization-records.txt.

| Data here | Origin and changes |
|---|---|
| prior_sources/pr280-v3-certificate.json; D11_5_0 and matching numerator coefficients in certificate.json, FACTOR_PROVENANCE.json and rounds/ | #280 v3 certificate at 197962c, tao/certificates/c82/v3; release weights re-optimized here |
| prior_sources/pr280-v4-certificate.json | #280 v4 coefficient JSON at 79ce0df; byte-for-byte copy, release weights re-optimized here |
| prior_sources/factor-bank.json | Earlier public coefficient archive at 3a7a84f; coefficient data unchanged |
| prior_sources/union-factor-bank.json, union-input.json, prior_sources/round5-certificate.json and historical evidence/control certificate JSON | Derived coefficient collections including #280 v3 and earlier public-bank data; exact comparisons in FACTOR_PROVENANCE.json; weights and selection changed |
| prior_sources/vidigoat-tree-79ce0df.json, prior_sources/vidigoat-tree-197962c.json and prior_sources/vidigoat-tree-3a7a84f.json | Complete GitHub tree metadata only; no source blobs downloaded, used for PYTHON_BLOBS.json |

Doche's P-factors and #301 MS360 retain their original mathematical credit in README.md even though they also occur in Patankar's public coefficient collections. Grinsztajn and Épi are credited for earlier factor libraries. A first local coefficient match is not an authorship attribution.

Public PR bodies/diffs and the constants page in sources/ are provenance citations to teorth/optimizationproblems (Apache-2.0 repository), not third-party search code. prior_sources/ retains relevant mathematical data and public source snapshots; Retained third-party snapshots are copied byte-for-byte without JSON reserialization. The open-prs.json/open-prs-final.json metadata collections and the old sources/pr330.json snapshot are omitted whole, because they contain obsolete unfinished-status text. Failure-log paths were made relative. Finished producer records are retained with publication-safe paths and the producer equal-fraction encodings described in README.md and CERTIFICATE_ENCODING.md.

No Python from vidigoat/optimization-records is redistributed, imported or executed. PYTHON_BLOBS.json checks every included .py against every blob in the retained full trees, and checks for imports of core or wlp. Any match is a blocker.

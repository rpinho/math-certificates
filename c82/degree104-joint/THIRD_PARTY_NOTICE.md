# Third-party data

This packet redistributes data, not code, from [vidigoat/optimization-records](https://github.com/vidigoat/optimization-records/tree/79ce0dfb211a67ff7e387b58b0d19ff1d6accfba), by V. Patankar (@vidigoat), at commits [79ce0df](https://github.com/vidigoat/optimization-records/tree/79ce0dfb211a67ff7e387b58b0d19ff1d6accfba), [197962c](https://github.com/vidigoat/optimization-records/tree/197962c9610f583e9bc56efe37bfb994c1eeb834) and [3a7a84f](https://github.com/vidigoat/optimization-records/tree/3a7a84fec9c64ae426f06a5f52597c84b3453ba0). The MIT License, copyright (c) 2026 Vidit Patankar, is preserved in LICENSE-vidigoat-optimization-records.txt.

| Data here | Origin and changes |
|---|---|
| prior_sources/pr280-v3-certificate.json; matching numerator coefficients in certificate.json, FACTOR_PROVENANCE.json and the retained final round | #280 v3 certificate at 197962c, tao/certificates/c82/v3; release weights re-optimized here |
| prior_sources/pr280-v4-certificate.json | #280 v4 coefficient JSON at 79ce0df; byte-for-byte copy, release weights re-optimized here |
| prior_sources/factor-bank.json | Earlier public coefficient archive at 3a7a84f; coefficient data unchanged |
| prior_sources/union-factor-bank.json.gz, prior_sources/round5-certificate.json and historical evidence/control certificate JSON | Derived coefficient collections including #280 v3 and earlier public-bank data; exact comparisons in FACTOR_PROVENANCE.json; weights and selection changed |
| prior_sources/vidigoat-tree-79ce0df.json, prior_sources/vidigoat-tree-197962c.json and prior_sources/vidigoat-tree-3a7a84f.json | Complete GitHub tree metadata only; no source blobs downloaded, used for PYTHON_BLOBS.json |

Doche's P-factors retain their original mathematical credit in README.md even though they also occur in Patankar's public coefficient collections. Grinsztajn and Épi are credited for earlier factor libraries. A first local coefficient match is not an authorship attribution.

Public PR bodies/diffs in sources/ and the constants page source cited in README.md are provenance citations to teorth/optimizationproblems (Apache-2.0 repository), not third-party search code. prior_sources/ retains relevant mathematical data and public source snapshots; Retained third-party snapshots are copied byte-for-byte without JSON reserialization. Whole-file omissions from this round-10 packet are listed in NOTE.md. Failure-log paths were made relative. Finished producer records are retained with publication-safe paths and the producer equal-fraction encodings described in README.md and CERTIFICATE_ENCODING.md.

No Python from vidigoat/optimization-records is redistributed, imported or executed. PYTHON_BLOBS.json checks every included .py against every blob in the retained full trees, and checks for imports of core or wlp. Any match is a blocker.

Round 10 inherited V. Patankar's #280 v5 certificate at [191064e7ccd88718853fe239dfd3890a8dc0fa37](https://github.com/vidigoat/optimization-records/tree/191064e7ccd88718853fe239dfd3890a8dc0fa37/tao/certificates/c82/v5), SHA256 8a5f363c29f02fca71e99dcedfdae0bd8969cd02bbed560484d1da726175a909, byte-for-byte from round 8's prior_sources/. Its complete tree metadata is prior_sources/vidigoat-tree-191064e.json. README.md and FACTOR_PROVENANCE.json credit every retained factor by full coefficient matches to v3/v4/v5. V5 itself reused four #330 denominators: C82r6_8c76cd0c4e53, C82r6_935548ec48fe, C82r6_083ca9b3950a and C82r7_dd0a7c419abf (with prefix Pin330c_). The current certificate retains none of those four denominators; its five numerator overlaps with each of v3/v4/v5 are P1, P2, P3, P4 and P6. Public-data reuse does not transfer original mathematical authorship.

Method credit also includes V. Patankar's iterated LLL numerator search and Ricardo Pinho's earlier dual-weighted LLL numerator work [Pin26] (PR #229); see the pinned source in README.md.

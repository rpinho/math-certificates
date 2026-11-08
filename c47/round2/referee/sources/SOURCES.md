# Referee source inventory and redistribution attribution

Hashes below identify the exact bytes supplied to/read by the referee, including files removed from the release. No third-party code was executed for this repair. Retained third-party files are unchanged except for the explicitly marked upstream planning-folder citation in lin-PROOF.md.

Tomar: **Tejasvi Singh Tomar**, *Bounds for the weak type (1,1) constant of the centred maximal operator over squares*, **v5, Lemma 6.2, Section 6**, [Zenodo record](https://doi.org/10.5281/zenodo.23716077). The original v5 repository license is reproduced as [tomar-LICENSE](tomar-LICENSE), consistent with the published round1 distribution.

Lin: **Yongxi Lin** and CoolRmal/centered-maximal-constant contributors. The copied repository files match Git blob IDs at the pinned commit below. The original copyright notice in Challenge.lean is preserved; [LICENSE](LICENSE) is the repository Apache-2.0 text. The inspected tree has no separate NOTICE. docs/ also contains the license and attribution.

Table: **teorth/optimizationproblems contributors**, with [table-LICENSE](table-LICENSE). Both the table and license match the pinned source bytes.

The two manuscript extracts came from separate PDF publications on Lin’s website. The inspected website tree has no license or NOTICE file; no permission is inferred from the Apache license of the formalization repository. Their copies are omitted. The .mathlib-quality tool cache is omitted regardless of its repository license.

## tomar-main.tex

- url: https://doi.org/10.5281/zenodo.23716077
- version: v5; origin commit 3af09fc359ce262f4a7f63d34b0d97e6d4d95d1a, paper/main.tex
- sha256: `be6cca23f1770215717e791aacaaa81f8fa5d786ffc6944bec4a62cc56fb9ed2`
- license: Apache-2.0
- decision: KEEP unchanged; Tejasvi Singh Tomar; adjacent tomar-LICENSE

## lin-PROOF.md

- url: https://github.com/CoolRmal/centered-maximal-constant/blob/72c022ba09032b522c878cca2f9b6c68217d77ea/docs/PROOF.md
- version: 72c022ba09032b522c878cca2f9b6c68217d77ea
- sha256: `f192aa030fca3dbbf64ac71ef5115632ccd233d3795458e57b346a90fba4f38e`
- license: Apache-2.0
- decision: KEEP; Yongxi Lin and repository contributors; adjacent LICENSE. Release citation edit on line 4 replaces the omitted cache path with its pinned upstream link and explicitly marks the edit; mathematics unchanged.

## lin-README.md

- url: https://github.com/CoolRmal/centered-maximal-constant/blob/72c022ba09032b522c878cca2f9b6c68217d77ea/README.md
- version: 72c022ba09032b522c878cca2f9b6c68217d77ea
- sha256: `387c56f90e42e7d6ffd31367f8daad770d973b2281b3bd8e2e013390d7f1f64a`
- license: Apache-2.0
- decision: KEEP unchanged; Yongxi Lin and repository contributors; adjacent LICENSE (also docs/LICENSE for HISTORY.md)

## Challenge.lean

- url: https://github.com/CoolRmal/centered-maximal-constant/blob/72c022ba09032b522c878cca2f9b6c68217d77ea/Challenge.lean
- version: 72c022ba09032b522c878cca2f9b6c68217d77ea
- sha256: `f3ad2119b5026b16b9c4345c6e37f84e02e95facc949343531f00bb1da3f27c1`
- license: Apache-2.0
- decision: KEEP unchanged; Yongxi Lin and repository contributors; adjacent LICENSE (also docs/LICENSE for HISTORY.md)

## docs/HISTORY.md

- url: https://github.com/CoolRmal/centered-maximal-constant/blob/72c022ba09032b522c878cca2f9b6c68217d77ea/docs/HISTORY.md
- version: 72c022ba09032b522c878cca2f9b6c68217d77ea
- sha256: `cadab3ea48b5ad76eaec368ce7839f52cac333a867da296a4abd215f477cfc25`
- license: Apache-2.0
- decision: KEEP unchanged; Yongxi Lin and repository contributors; adjacent LICENSE (also docs/LICENSE for HISTORY.md)

## LICENSE

- url: https://github.com/CoolRmal/centered-maximal-constant/blob/72c022ba09032b522c878cca2f9b6c68217d77ea/LICENSE
- version: 72c022ba09032b522c878cca2f9b6c68217d77ea
- sha256: `b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1`
- license: Apache-2.0
- decision: KEEP unchanged; Yongxi Lin and repository contributors; adjacent LICENSE (also docs/LICENSE for HISTORY.md)

## .mathlib-quality/plan.md

- url: https://github.com/CoolRmal/centered-maximal-constant/blob/72c022ba09032b522c878cca2f9b6c68217d77ea/.mathlib-quality/plan.md
- version: 72c022ba09032b522c878cca2f9b6c68217d77ea
- sha256: `e6f30ec84e02c1fe244d3063b61a56df54404fc70e782c081d911c8e61c0ee77`
- license: Apache-2.0
- decision: TRASH tool cache, even though licensed

## lin-balayage.txt

- url: https://coolrmal.github.io/assets/papers/two-partial-balayage-principles.pdf
- version: fe49fc2b2e25e8953a3ffb0b9fd776a8eec3bced (website tree inspected; PDF text extraction read by referee)
- sha256: `17269aaa4a77d7f91859db672db970878b787cdd723e8fcf807b707e8e91cdc9`
- license: No redistribution grant found
- decision: TRASH; Yongxi Lin; no redistribution license identified for the separate manuscript/PDF; Apache license of a different repository is not assumed to cover it

## lin-c2.txt

- url: https://coolrmal.github.io/assets/papers/c2-less-than-4.pdf
- version: fe49fc2b2e25e8953a3ffb0b9fd776a8eec3bced (website tree inspected; PDF text extraction read by referee)
- sha256: `7e3e1db53b3773894eae1a71090d7e41b1d5cb30e7f7060e1123fe128c3e2122`
- license: No redistribution grant found
- decision: TRASH; Yongxi Lin; no redistribution license identified for the separate manuscript/PDF; Apache license of a different repository is not assumed to cover it

## 47a.md

- url: https://github.com/teorth/optimizationproblems/blob/d793db4c680bedeb85c838cb17756b3a7f6ac38d/constants/47a.md
- version: d793db4c680bedeb85c838cb17756b3a7f6ac38d
- sha256: `b989ff415dde87b78195824eeb6343cc3d2c6528b9fa6e0c9fafeffb9f4e1bb0`
- license: Apache-2.0
- decision: KEEP unchanged; teorth/optimizationproblems contributors; adjacent table-LICENSE

## table-LICENSE

- url: https://github.com/teorth/optimizationproblems/blob/d793db4c680bedeb85c838cb17756b3a7f6ac38d/LICENSE
- version: d793db4c680bedeb85c838cb17756b3a7f6ac38d
- sha256: `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`
- license: Apache-2.0
- decision: KEEP unchanged; license accompanying 47a.md

## final.json

- url: Local producer input supplied to the clean-room referee
- version: Original supplied bytes
- sha256: `bc342d18f9fe219828856bcaa9531669a1051c2685394e41dfbeb3e794e818eb`
- license: First-party input
- decision: KEEP unchanged; our producer input, not a third-party copy

## final-finite.json

- url: Local producer input supplied to the clean-room referee
- version: Original supplied bytes
- sha256: `c1444264d096d87ae7863b7de9fa77dca8c1c51b8f89f616c531b40c469fd3ed`
- license: First-party input
- decision: KEEP unchanged; our producer input, not a third-party copy

## producer-proof.md

- url: Local producer input supplied to the clean-room referee
- version: Original supplied bytes
- sha256: `72226760991855177614278160c85b7938876be5e33b7ea79c5dfd88a9691752`
- license: First-party input
- decision: KEEP unchanged; our producer input, not a third-party copy

## Release citation substitutions

The two saved first-party PR #321 API snapshots in ../../sources/ have only their Tomar v5 GitHub citation replaced with the Zenodo DOI and the words “v5, Lemma 6.2, Section 6”. They are release-edited snapshots, not byte-for-byte API responses. Mathematical data and credit fields are unchanged.

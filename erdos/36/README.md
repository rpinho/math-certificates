# Erdős #36 (minimum overlap): certificates for the means 0 ≤ |m| ≤ 1/160

**Status: candidate, unrefereed. AI work. No human has checked it. No new bound is claimed.**

This packet holds exact certificates, two separately written checkers (a Claude producer verifier and a GPT-6.2 Astra referee checker; AI checking AI, not independent review) and a replay for one step in someone else's claimed lower bound
on the Erdős minimum-overlap constant: the claim by Unktok, plasma-ai/erdos#67 (repository [unktok/erdos-36-lower-bound](https://github.com/unktok/erdos-36-lower-bound/tree/cb2f01237c2867a704739f6864075e0ce4e67f07)).
It exists so that anyone can re-run the checks, and so that a follow-up on #67 can link to one pinned folder.
It does not contain, and the scripts never ship, the claimant's code or data files or Wetch's certificates;
you fetch those yourself from the pinned commits (section 4).

## 1. What is claimed

Notation. h : [0,2] → [0,1] is measurable with ∫h = 1; g = 1 − h on [0,2] (0 outside); h is extended by 0.
p(t) = ∫ h(x) g(x+t) dx. Then p ≥ 0, ∫p = 1, M = ‖p‖∞ and m = ∫ t p(t) dt ∈ [−1, 1] is the mean of p.

**Claim (type K, this packet).** For every such h with m(h) ∈ [−1/160, 1/160]: ‖p‖∞ > L, where L is the claimant's
exact rational

    L = 295115424188729399759259170770153384401616054763504786695772146837923638817310985375107967151349
        / 775338951052420904588737482312221487781542035285383462905883789062500000000000000000000000000000
      = 0.380627625876591043727074…

The claim is **conditional** on the premises in section 3: the claimant's core inequality S12 and the two-scale convention.
The smallest margin over L is +3.05e-10 in the first bin [0, 7e-5], which is slack the claimant left below their own
N0/D_up, not a better bound. On the 77 bins that meet [1.46e-4, 1/160] the smallest margin is +1.866e-9 (bin 17, [1.459e-4, 1.532e-4]).

The certificate is `certificates/certK_r105.json` (7.6 MB, sha256 df14a592c74b6b5dd3b791d178372433a89dabd125582659c9884efb589d371b): 94 closed bins tiling [0, 1/160] with exactly equal consecutive
endpoints. Each bin has an exact multiplier λ and a piecewise-linear u on the 1/65536 grid with exact rational slopes.
Reflection h(x) ↦ h(2−x) sends p(t) ↦ p(−t), m ↦ −m and keeps M, so m ≥ 0 covers m ≤ 0.
For |m| ≥ 1/160 the claim rests on a different, earlier piece (87 "type O" outer bins of Wetch's kind, round 1); that piece is **not** in this packet (section 3).

## 2. The type-K lemma in six steps

Let Φ be the claimant's core kernel as rebuilt from their data files (even, bounded, piecewise smooth), let N0 and C be the
constants in [target.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/target.json), and suppose **S12**: ∫ p Φ ≥ N0 + C m² for every admissible h. Put D = ∫ Φ₊ and
g(t) = |Φ(t)| + |Φ(2−t)| on (0,1) (not the g = 1 − h above).

1. **Odd profile.** For t ∈ [0,2], p(t) = H(2−t) − R(t) and p(−t) = 1 − H(t) − R(t), where H(u) = ∫₀ᵘ h and R(t) = ∫ h(x)h(x+t)dx is even. So d(t) := p(t) − p(−t) = H(t) + H(2−t) − 1. Hence d(0) = 0, d(2−t) = d(t), d is absolutely continuous with d′ = h(t) − h(2−t) ∈ [−1,1] a.e., and m = ∫₀² t d(t) dt = 2∫₀¹ d.
2. **Even/odd split.** Let e = (p(t)+p(−t))/2. Φ is even, so ∫pΦ = ∫eΦ. Since 0 ≤ p ≤ M, |d|/2 ≤ e ≤ M − |d|/2. Hence ∫eΦ ≤ M·D − ½∫_{−2}^{2} |d||Φ|.
3. **Fold.** Using |d(−t)| = |d(t)| and d(2−t) = d(t): ½∫_{−2}^{2}|d||Φ| = ∫₀¹ |d(t)| g(t) dt.
4. Steps 2–3 with S12 give **M·D ≥ N0 + C m² + ∫₀¹ |d| g.** (This is the claimant's "quartet maximization" inequality.)
5. **Lipschitz dual for the d-term (this packet's).** Take any real λ and any Lipschitz u on [0,1] with u(1) = 0 and |λ − u′| ≤ g a.e. Then |d| g ≥ d(λ − u′) pointwise, so ∫₀¹|d|g ≥ λm/2 − ∫₀¹ d u′. Integrating by parts (d(0) = 0, u(1) = 0) gives −∫₀¹ d u′ = ∫₀¹ d′ u ≥ −∫₀¹ |u|, because |d′| ≤ 1.
6. **Bin bound.** For every admissible h with mean m: M ≥ [N0 + C m² + λm/2 − ∫₀¹|u|] / D_up, whenever the numerator is positive and D ≤ D_up. On a bin [lo, hi] the numerator is concave in m (C < 0), so its minimum over the bin is at lo or hi. The verifier checks that this minimum over D_up exceeds L, in exact rationals.

Every step holds for measurable h; the only regularity used is absolute continuity of d. A step-function reduction is not used.

Credits inside the lemma: the quartet inequality (steps 2–4) and the facts about d (step 1) are documented in the claimant's
documents, which credit Wetch's EVEN_ODD_CAPACITY_RETURN for the odd-part capacity idea. The Lipschitz dual (step 5) and its
exact check are this packet's. A human should read steps 2 and 5.

What the verifier checks for each bin (`producer/verify_K.py`): (1) |λ − s_k| ≤ g_lb(k) on all 65 536 cells, with g_lb an outward Arb
(128-bit) enclosure of g on each cell, converted to exact dyadics; (2) ∫|u| exactly in rationals, including zero crossings;
(3) the numerator at both bin endpoints and the strict comparison num/D_up > L; (4) the exact cover. D_up = 2.627239663352680428
(padded outward by 1e-22) comes from `producer/dint2/dint2.py`, an Arb quadrature that re-checks all 153 336 float sign decisions.

## 3. What this rests on (not proved here)

- **S12 and the data behind it.** The core inequality ∫pΦ ≥ N0 + C m² is the claimant's. A round-1 job (not in this packet) checked its analytic rules and exact PSD witnesses (17 original plus one two-scale witness). This packet's ledger scripts rebuild N0 and C from primitive data: C closes exactly; N0 is matched to 3.1e-28 using the claimant's stored paid-row constants (their own book-keeping falls 3.1e-28 short of N0), and is supported by +2.283e-27 when each paid row is charged its exact κ plus its actual coefficient errors (`producer/ledger/ledger_arb.py`, Arb 256 bits). The periodic scatter is rebuilt exactly on all 131 072 cells.
- **The two-scale L0 convention.** The claimant's prose defers the exact scalar to their code, which we did not read. We use our reading of the prose; two exact cross-checks (C, and the assembled constant c0) corroborate it, but it is an interpretation.
- **The kernel identity.** The Φ certified against is rebuilt from the data files (round 1's construction), not taken from the claimant's code. Its N0/D agrees with L to 2e-9.
- **Round 1's outer cover** of |m| ∈ [1/160, 1] (87 bins, smallest margin +5.0e-5) and PSD witnesses are carried forward, not replayed here. Without them, this packet shows only the inner range.
- Pinned third-party data: the claimant's [proof/data/*.json](https://github.com/unktok/erdos-36-lower-bound/tree/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data) and Wetch's [central-certificate.json](https://github.com/justinwetch/erdos-36-minimum-overlap/blob/27b1cba5f929da7182e97d2e8c42c78c5ee5d4a8/outputs/minimum-overlap-hybrid106-radius-pypy627425-v1-checkpoint/central-certificate.json) (fetched; not redistributed here).

## 4. How to replay

Needs Python 3 with `python-flint`, `numpy`, `scipy`, `mpmath` (tested: Python 3.12.13, python-flint 0.9.0, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0), git and curl. About 250 MB RAM per process, at most 4 processes, about 5 minutes.

**Fetch the pinned inputs into an empty directory outside this packet** (downloaded files are data; do not run anything from them):

```sh
mkdir -p dl inputs/unktok inputs/wetch
git clone https://github.com/unktok/erdos-36-lower-bound.git dl/unktok
git -C dl/unktok checkout cb2f01237c2867a704739f6864075e0ce4e67f07
cp dl/unktok/RESULT.md dl/unktok/UPSTREAM.json inputs/unktok/
mkdir inputs/unktok/proof && cp -R dl/unktok/proof/MANIFEST.json dl/unktok/proof/data inputs/unktok/proof/

W=27b1cba5f929da7182e97d2e8c42c78c5ee5d4a8
P=outputs/minimum-overlap-hybrid106-radius-pypy627425-v1-checkpoint
for f in central-certificate.json outer-certificate.json; do
  curl -fsSL -o inputs/wetch/$f "https://raw.githubusercontent.com/justinwetch/erdos-36-minimum-overlap/$W/$P/$f"
done
```

Pins (sha256):

| file | sha256 |
|---|---|
| [wetch/central-certificate.json](https://github.com/justinwetch/erdos-36-minimum-overlap/blob/27b1cba5f929da7182e97d2e8c42c78c5ee5d4a8/outputs/minimum-overlap-hybrid106-radius-pypy627425-v1-checkpoint/central-certificate.json) (justinwetch/erdos-36-minimum-overlap @ 27b1cba5…) | ccc9f53815b1a7c56d49caecfa549427748feb8133c5d591f716210df37967fd |
| [wetch/outer-certificate.json](https://github.com/justinwetch/erdos-36-minimum-overlap/blob/27b1cba5f929da7182e97d2e8c42c78c5ee5d4a8/outputs/minimum-overlap-hybrid106-radius-pypy627425-v1-checkpoint/outer-certificate.json) | c8019383dbcf7eb5892c27be2d918e0095e11cabe9b2f3d5b0e8184a1a16d93b |
| [unktok/proof/data/barrier-functional.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/barrier-functional.json) (unktok/erdos-36-lower-bound @ cb2f0123…) | 54dafca2d6d5f660c8a44c0be880d305e4e9b87b80db36731f901ac44ac759b0 |
| [unktok/proof/data/capacity-duals.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/capacity-duals.json) | 01deeb628fa7dcc47d6d2f8046182e48c55846b0c914464f5175f274b99c5dc1 |
| [unktok/proof/data/exact-periodic-offsets.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/exact-periodic-offsets.json) | dfc488f7629104f349e531be13f8e7102a6884d638b6f1f5b464126d0cf91a3a |
| [unktok/proof/data/fine-boundary-reference.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/fine-boundary-reference.json) | 542510472527297cf3d3785f8fbd812edad7550eea4159e0e051433a71668fc7 |
| [unktok/proof/data/original-preconditioners.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/original-preconditioners.json) | 90cf1311bc760a88c4f6fe4c0296504c30830bc6300731ce2ae0b01145f7c84b |
| [unktok/proof/data/rational-preconditioner.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/rational-preconditioner.json) | 66e49462e3d2cae32e8231f462e37b042a70b75daa701abde5572a7d5b1fda36 |
| [unktok/proof/data/selected-exact-kernel.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/selected-exact-kernel.json) | 64316807b1ad463836ad3609315fea8586e86061d05328f017c8be280d4af11e |
| [unktok/proof/data/selected-flow-duals.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/selected-flow-duals.json) | a001bab5c58c288c239643388c305330114dcf2b141726ea3dfae202cf6e6b8b |
| [unktok/proof/data/selected-paid-rows.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/selected-paid-rows.json) | 63c27d0073a6dff137b273487d4dde10251af7b000ce68ef736453df5bf4e64e |
| [unktok/proof/data/target.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/data/target.json) | d091159238f9040242cb6ca699027623aab7f6e0aa1147694f8b0bd43b777beb |

The claimant's [proof/MANIFEST.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/MANIFEST.json) also lists [data/central-sparse.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/MANIFEST.json) and [data/outer-certificate.json](https://github.com/unktok/erdos-36-lower-bound/blob/cb2f01237c2867a704739f6864075e0ce4e67f07/proof/MANIFEST.json); these are derived from Wetch's files by the claimant's own fetch script, which we neither need nor run. The scripts here read Wetch's files directly.

**Run everything** from the packet directory (`E36_INPUTS` is set by the script from its first argument):

```sh
python3 -I check_inputs.py ../inputs          # sha256 check of the fetched files
sh replay_all.sh ../inputs python3 replay_out  # ~5 min; ends with compare_replay: PASS
```

`replay_all.sh` does not modify the packet. It runs, in order: `producer/dint2/dint2.py` (D_up); `producer/verify_K.py` on the certificate, then its controls
(`--raiseL 1e-6`, `--flip 17`, `--nocap 17`, `--drop 17`, `--N0shift=-1e-27`); `referee/referee_check.py` and `referee/referee_fixtures.py`;
the seven `producer/ledger/*.py` scripts; the search-side float caches, 16 step-function fixtures and `make_K.py`; then `compare_replay.py`, which compares with the shipped results.
Shipped results are in `results/` (producer) and `referee/` (referee); the replay recorded for this packet is in `replay/`. `replay/` omits the 7.6 MB [certK_search.json](replay/certK_search.cmp.txt) (search output, not shipped) and the float caches (`certK_search.cmp.txt` records that the search output was byte-identical), so `compare_replay.py` is meant for your own `replay_out`, not for `replay/`.

Individual commands (from the packet directory, `E36_INPUTS=../inputs`):

```sh
python -I producer/dint2/dint2.py --out replay                       # writes producer/dint2/res_replay.json
python -I producer/verify_K.py certificates/certK_r105.json --out vK.json   # 18 s; add --dint2 FILE to use your own D_up
python -I referee/referee_check.py certificates/certK_r105.json OUTDIR     # 7 s; OUTDIR must exist; then referee_fixtures.py OUTDIR
```

**Expected results** (from the replay in `replay/`, fresh copy of this packet, pinned inputs):

| check | result |
|---|---|
| producer verifier | 94 of 94 bins pass; 0 slope violations; cover exact [0, 1/160]; min margin +3.0518e-10; min over the 77 target bins +1.8665e-9 |
| referee checker | 94 of 94 pass; 6 160 384 cell inequalities, 0 violations; min slack of any cell +1.3177e-7; margins +3.0518e-10 and +1.8665e-9 |
| D_up | 2.627239663352680427900351, width of its Arb enclosure 1.8e-15 (the referee's own quadrature: 1.65e-19) |
| controls (producer) | L raised by 1e-6: 79 of 94 bins fail. λ sign flipped (bin 17): 549 slope violations. Capacity deleted (bin 17): margin −4.78e-9. Bin 17 removed: gap [1.459e-4, 1.532e-4], target not covered |
| controls (referee) | L raised by 1e-9: bin 0 fails (−6.9e-10); by 1e-6: 79 fail; flipped λ; one altered slope (1 cell violation although the margin still reads positive); removed bin leaves a gap |
| fixtures | producer: 16 lawful step functions (15 inside the bins get all four links; `three_block`, m = 0.5, only the first two), smallest final slack +3.1e-4; referee: 7 exact step-function densities, smallest slack +6.2e-4. None falls below its bin's bound |
| ledger | C exact; periodic scatter 0 of 131 072 cells differ; N0 supported by +2.283e-27 (exact κ) |

The packet's `make_K.py` search is not needed to check the certificate; re-running it with `1.05` reproduces `certK_r105.json` byte for byte.

## 5. The two checkers

- **Producer: Claude Opus 5.5.** Wrote the lemma, the search `producer/make_K.py` (float grid) and a separate exact verifier `producer/verify_K.py`. The verifier shares no code with the search and rebuilds Φ from primitive data. The N0/C ledger, the D_up quadrature, controls and fixtures are in `producer/`.
- **Referee: GPT-6.2 Astra (cross-family).** Rederived the lemma, rebuilt the kernel and ledger, wrote its own Arb quadrature and certificate checker, and ran its own mutations and exact fixtures (`referee/`, verdict in `referee/REFEREE.md`, which calls it a "Codex" review). It did not see the producer's code. It had the supplied documents, Wetch's data, the certificate and the producer's report, and its verdict is conditional on the same two-scale convention.
- Both are AI. No human has read the lemma (steps 2 and 5 especially), the two-scale reading, or the certificates.
- There is no statistical holdout: the certificate is an exact finite inequality system and the claim is universal over densities, so the fixtures are consistency checks, not evidence.

## 6. Limitations and next steps

- Conditional on S12 and on the two-scale L0 reading (section 3). The claimant has not confirmed either.
- Round 1's outer cover and PSD checks are cited, not included.
- The kernel is our rebuild from data files, not the claimant's code.
- The smallest margins are about 3e-10 and 1.9e-9; the bound is not improved, it is checked.
- `producer/ledger/n0_ledger.py` prints the sum with the claimant's stored paid-row constants, which falls 3.1e-28 short of N0; `ledger_arb.py` gives the rigorous comparison (+2.283e-27).
- Next: a human reading of lemma steps 2 and 5 and of the two-scale reading; ask the claimant on #67 whether their capacity step reduces to inequality 4 and for the two-scale L0 convention in prose.

## 7. Credits

- **Unktok** (plasma-ai/erdos#67, [unktok/erdos-36-lower-bound](https://github.com/unktok/erdos-36-lower-bound/tree/cb2f01237c2867a704739f6864075e0ce4e67f07)): the claimed bound, the kernel data, N0, C, L, and the analytic documents this packet builds on, including the quartet inequality.
- **Justin Wetch** ([justinwetch/erdos-36-minimum-overlap](https://github.com/justinwetch/erdos-36-minimum-overlap/tree/27b1cba5f929da7182e97d2e8c42c78c5ee5d4a8)): the phase-Gram method, the periodic families, the central and outer certificates, and EVEN_ODD_CAPACITY_RETURN (the odd-part capacity idea).
- **E. P. White**, the density formulation and the refereed lower bound 0.379005; **J. Haugland**, background on the upper side. Price (mean conditioning) and Kim–Pilanci are credited in the claim.
- Libraries: python-flint / Arb, mpmath, numpy, scipy.

Layout: see `PACKAGING.md` (every file, its source, and each portability edit) and `SHA256SUMS`.

# Different-model provenance and receipt normalization

Producer author: **gpt-6.1-sol**. The source log `_codex/math_c91r6_1103.log`
begins with a MODEL_SELECTION record naming `openai/gpt-6.1-sol`, selection
`81027c3f2c544f1eab4a85ecd2e40e63`. Its first two lines are preserved in
producer_log_excerpt.txt; the parsed record is producer_model_selection.json.
Full source-log SHA256 at release: `f24a9c13b695e2907d2735d75c58c752ea1b6eeb5892add28a3a58eb1997a41c`.
The full log contains private operational paths and is not published.

Checker author: **gpt-6-astra**. The execution selection sidecar
`_codex/math_l1chk_e_1103.log.selection.json` names `openai/gpt-6-astra`, with
override `different-model-independent-checker`; checker_model_selection.json
preserves those exact bytes, SHA256 `08483e622b4d75bdcc264760266ae3a813a869e9dbcfb731426864c55fdd0b22`.
This is a different model from the producer. The checker extends the earlier
authorized independently written round-5 implementation, with round-6 changes
derived from proof, scope and certificate, without producer implementation.

The original checker report, README and receipt self-label the model `gpt-6`.
The supplied executor-selection sidecar resolves that generic session label
to `gpt-6-astra`. `original/check.json` and `original/levels_update.json`
preserve the original metadata byte for byte. The active `check.json` and
`levels_update.json` explicitly normalize the checker author and relocate
argv, output and both implementation-source paths to the round-6 root.
The body-level packet similarly relocates paths relative to pr_body.md.
These are packaging adaptations of an existing successful execution, not
new executions. No certificate, checker implementation or stdout bytes changed.
normalization.json records original and normalized hashes.

The original receipt hash is `64dc32b1b17046dfb111b71ca81c89e9cdbd8c8c78171a8d4171eb14ba8da8d1`.
The exact stdout hash is `9f3012574de4287fa9b51f8993a2c7bca08883d16c45a914ba558a3050638d67`.
Both implementation files are hashed, not merely a launcher. The recorded
successful full run took **2141.69722533226 seconds**, exit 0; see execution.json.
The timeout is 18,000 seconds, above both the actual run and the 120-second
automatic-replay threshold. Packet validation uses hashed evidence without
rerunning the full graph. The receipt is a local record, not remote attestation.

The producer checker is separately written by the same producer model; that
alone does not establish strict finite L1. The different-model checker packet
does. Universal bridges remain prose, so the whole-bound level stays L0.

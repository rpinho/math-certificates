# Rejection-order regression fixtures

Round-6 captures from `logs/mini_controls_control_*.log`, with their actual
exit codes and positive stop condition in `captures.json`. Two probes move
the sole C++ diagnostic immediately before C++ START, preserving all other
lines, following Astra2's original probes. Tests independently derive the
checkpoint order from captures, permute/remove checkpoints, move diagnostics
before every checkpoint, and insert extra rejection lines at every boundary.
`astra_round5/` retains the original reviewer probes and receipt with local compiler-path prefixes redacted.

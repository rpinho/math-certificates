# Review probe: fresh-tensor and omitted-coordinate positive control

Written by the Claude Science (Claude Opus 5.5) round-11 review and recorded here unchanged. It is not part of the frozen replay.
It subclasses checker B (`frozen_parity/verify_partial_b.py`) and runs two positive configurations with omitted coordinates; the one with coordinates 11 and 23 omitted must reach an unsigned leaf, and does after 42 nodes, exercising the fresh-tensor branch.

Run from `round11/frozen_parity/` with Python >= 3.10:

    python3 ../review/probes/positive_fresh_omitted.py

Recorded output: `positive_fresh_omitted.out.txt`.

Shipped: REFEREE.md, verdict HOLDS WITH CAVEATS. The submitted Case I argument (LEMMAS.md:52) and certificate are wrong (cutoff direction). The theorem F(n) <= 5n-1 for n >= 550,000 holds once that tree is replaced by my own Arb-checked Case I tree (out/cert_case1_referee.json, 1,223 leaves, max -0.0010209), which still needs a second check.

Did I find something new? No, not of my own. This is a referee report. The producer's result is new relative to the public sources I searched on 2026-11-25 (Kataria 5.025n unrefereed, 84n on the official page), provided the Case I repair stands.

## Verification status
- (a) reduction, connectivity (<= e/(16-e) = 0.2047 < 3/13), odd n, simplification: PASS, re-derived.
- (b) Kempe dichotomy: PASS by hand. Simulation: 5,996 random 10-regular configurations, 83,966 swaps, 0 invalid. The three mutants (adjacent donor, v_j with a 4-neighbour, donor with a 3-neighbour) were invalid every time.
- (c) rates: naive and Case II re-derived and correct. Case I: the occupancy inequality at LEMMAS.md:52 is false (wrong cutoff direction); counterexample in out/case1_direction_counterexample.txt.
- (d) own Arb verifier (code/arbverify.py): naive A/B ACCEPT (max -0.00117883621834), Case II ACCEPT (max -0.00100000102061), producer Case I REJECT. Referee Case I tree ACCEPT (max -0.00102091368896). All 16 corruption controls REJECT. The positive naive witness is certified at +0.0033635269515.
- (e) finite sum: 4.2602e-11 at n0, decreasing; the total with the disconnection bound is < 1.
- (f) prior art: no bound below 5.025n found (see REFEREE.md (f) for what was and was not searched).

## Reproduce (from this directory; PY=~/dev/open-science/.venv/bin/python)
    mkdir -p data out; for f in cert_case1 cert_case2 cert_naive_ab; do gunzip -c ../e1182kempe/$f.json.gz > data/$f.json; done
    for c in naive_ab case1 case2; do nice -n 10 $PY -I code/arbverify.py data/cert_$c.json --json out/verify_$c.json; done
    nice -n 10 $PY -I code/case1_repair.py produce out/cert_case1_referee.json   # ~1 min, deterministic
    nice -n 10 $PY -I code/case1_repair.py check out/cert_case1_referee.json
    nice -n 10 $PY -I code/controls.py data out
    nice -n 10 $PY -I code/finite_check.py
    for s in 1 2 3 4; do nice -n 10 $PY -I code/kempe_sim.py $s 1500 out/kempe_$s.json; done
    nice -n 10 $PY -I code/rc_search.py 1 6    # non-rigorous true Case I rate search

## Limitations
- I built the Case I repair and checked it myself. It needs a second check, ideally by a different model, before any public claim.
- The verifier format for the producer certificates was inferred from the data (grid and tilt scales checked against raw values).
- X/social media, GitHub code search, Brandt (1996) and Nikiforov–Rousseau Thm 5.1 were not checked.

## Next steps
1. The producer replaces LEMMAS.md lines 51-52 (upper cutoff Q03 <= q*, tail above B03, or the s-tilt form in REFEREE.md (c)) and regenerates cert_case1.
2. A second referee replays out/cert_case1_referee.json with their own code.

"""Referee: extra control of exact_rank_max against brute-force sublattice enumeration at n=6."""
import sys, time
sys.path.insert(0, ".")
from upper_check import brute, exact_rank_max
words = ["0010011", "0100110", "0110100", "0011001", "1011010", "0101101", "0001110", "1100101"]
mism = 0
for w in words:
    for c in "01":
        t = time.time(); b = brute(w, c); e, _ = exact_rank_max(w, c, cap=10**6)
        print(w, c, "brute", b, "solver", e, f"{time.time()-t:.1f}s", flush=True)
        mism += b != e
print("n=6 mismatches:", mism)

# consistency scan: for each n, min over all rank words of the largest monochromatic sublattice (capped at 8)
import sys; sys.path.insert(0, sys.argv[1]); import ref
for n in range(1, 13):
    vals = {}
    for wi in range(1 << (n + 1)):
        word = "".join(str(wi >> r & 1) for r in range(n + 1))
        b = ref.cmd_dfs(None, word, n, quiet=True)
        vals[word] = min(max(b.values()), 8)
    m = min(vals.values()); arg = [w for w, v in vals.items() if v == m]
    print(f"n={n}: min over rank words = {m}; chain bound {(n+2)//2}; attained by {len(arg)} words, e.g. {arg[:4]}")
# paper Table (BMB): word RRBRBBRRBR (n=9), red letters give an 8-member family
w = "RRBRBBRRBR".replace("R", "1").replace("B", "0")
print("RRBRBBRRBR red:", ref.cmd_dfs(None, w, 9, quiet=True)[1])

#!/bin/sh
# Referee corruption controls. Each corrupted input must be rejected by the referee's checker.
set -u
P="$HOME/dev/open-science/.venv/bin/python"
D=../data
T=out/corrupt
mkdir -p $T

echo "== 1. flip one literal in a clause used by the proof =="
# all-splits: clause 2 is '-1 37 38 39 40' (split 1 -> window-0 selectors); flip 37 -> -37
awk 'NR==3{sub(/^-1 37 /,"-1 -37 ")}1' $D/all-splits.cnf > $T/all-flip.cnf
cmp -s $T/all-flip.cnf out/all-splits.regen.cnf && echo "  all-splits flip: NOT detected by regeneration" || echo "  all-splits flip: differs from regenerated DIMACS (rejected)"
python3 lrat_check.py $T/all-flip.cnf $D/all-splits.lrat | sed 's/^/  all-splits flip LRAT: /'
# exclusion: flip the first literal of clause 1 ('1 2 3 4 5' -> '-1 2 3 4 5')
awk 'NR==2{sub(/^1 /,"-1 ")}1' $D/exclusion.cnf > $T/excl-flip.cnf
cmp -s $T/excl-flip.cnf out/exclusion.regen.cnf && echo "  exclusion flip: NOT detected" || echo "  exclusion flip: differs from regenerated DIMACS (rejected)"
python3 lrat_check.py $T/excl-flip.cnf $D/exclusion.lrat | sed 's/^/  exclusion flip LRAT: /'
# a used selector-implication clause in exclusion: last clause '-122 63 0'? flip '-122 -62' -> '-122 62'
awk '$0=="-122 -62 0"{$0="-122 62 0"}1' $D/exclusion.cnf > $T/excl-flip2.cnf
python3 lrat_check.py $T/excl-flip2.cnf $D/exclusion.lrat | sed 's/^/  exclusion flip (-122 -62 -> -122 62) LRAT: /'

# a clause the exclusion proof uses: hint 293306 of the final step -> flip its first literal
awk 'NR==293307{ if ($1 ~ /^-/) sub(/^-/,""); else $1="-"$1 }1' $D/exclusion.cnf > $T/excl-flip3.cnf
python3 lrat_check.py $T/excl-flip3.cnf $D/exclusion.lrat | sed 's/^/  exclusion flip in used clause 293306 LRAT: /'

echo "== 2. alter one LRAT hint (replace by another in-range id) =="
awk 'NR==1{$5=$5+1}1' $D/all-splits.lrat > $T/all-hint.lrat
python3 lrat_check.py $D/all-splits.cnf $T/all-hint.lrat | sed 's/^/  all-splits hint: /'
awk 'NR==1{$6=$6+1}1' $D/exclusion.lrat > $T/excl-hint.lrat
python3 lrat_check.py $D/exclusion.cnf $T/excl-hint.lrat | sed 's/^/  exclusion hint: /'
# drop the final empty-clause step
sed '$d' $D/all-splits.lrat > $T/all-trunc.lrat
python3 lrat_check.py $D/all-splits.cnf $T/all-trunc.lrat | sed 's/^/  all-splits truncated: /'

echo "== 3. drop one set from a witness family =="
$P - <<'EOF'
import gzip, json, sys
sys.path.insert(0, ".")
from faces_check import check_family
from excl_check import check_closed
from upper_check import check_family as up_check
# faces: family #1 of the first nonempty (u,v,z) case with d>0, and a sample of 200 more
n = rej = 0
with gzip.open("../data/faces.jsonl.gz", "rt") as f:
    for line in f:
        u, v, z, fams = json.loads(line)
        for fam in fams:
            for k in range(len(fam)):          # drop each member in turn
                g = fam[:k] + fam[k+1:]
                n += 1
                try:
                    check_family(g, u, v, z)
                except ValueError:
                    rej += 1
            if n > 20000:
                break
        if n > 20000:
            break
print(f"  faces families: {n} single-member drops, {rej} rejected; the {n-rej} accepted remainders are themselves closed families of size >= 14 (still valid witnesses)")
n = rej = 0
with gzip.open("../data/sets.jsonl.gz", "rt") as f:
    for i, line in enumerate(f):
        if i % 997:
            continue
        fam = json.loads(line)[2]
        for k in range(len(fam)):
            n += 1
            try:
                check_closed(fam[:k] + fam[k+1:], 23)
            except ValueError:
                rej += 1
print(f"  sets.jsonl.gz families (every 997th): {n} single-member drops, {rej} rejected; the {n-rej} accepted remainders are closed families of size >= 14 (still valid)")
up = json.load(open("../data/upper/upper_n23.json"))
n = rej = 0
for col in up["colours"]:
    fam = col["witness"]
    for k in range(len(fam)):
        n += 1
        g = fam[:k] + fam[k+1:]
        try:
            size, cols = up_check(g, up["word"])
            if size < 14:
                rej += 1
        except AssertionError:
            rej += 1
print(f"  upper families: {n} single-member drops, {rej} fall below 14")
# flip one coordinate in a member
fam = up["colours"][0]["witness"][:]
fam[5] ^= 1 << 22
try:
    size, cols = up_check(fam, up["word"]); print("  upper coordinate flip: accepted?!", size, cols)
except AssertionError:
    print("  upper coordinate flip: rejected (not closed)")
EOF

echo "== 4. induction sensitivity: remove every witness for shape (20,0), context 1 =="
$P - <<'EOF2'
import sys; sys.path.insert(0, ".")
import faces_check as fc
orig = fc.load_witnesses
def patched(path, drop=None):
    W, n, b = orig(path, drop)
    k = len(W.pop((20, 0, 1), []))
    print(f"  removed {k} checked witnesses of case (20,0,1)")
    return W, n, b
fc.load_witnesses = patched
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    fc.main("../data/faces.jsonl.gz")
for l in buf.getvalue().splitlines():
    if l.startswith("  removed") or l.startswith("FACE CLAIM") or l.startswith("shape (21,0)"):
        print(" ", l[:200])
EOF2

"""Referee every row of inputs/WITNESSES.tsv with referee_solver (and the naive cross-check solver)."""
import sys, csv, re, json
sys.path.insert(0, '.')
from referee_solver import Game, parse_pos
from naive_solver import naive
exec(open('controls_rows.py').read().split("allrows = {}")[0])  # printed p.28 rows: rows, codes
printed = {c: seq for name, seq, per in rows for c in codes[name]}
# p.27 table, transcribed from inputs/sources/page27.png (p1, t1, p2, t2)
T27 = {'0.157': (22,6,1,3), '0.175': (19,4,1,2), '0.2˙6¯0': (19,4,1,2), '0.32˙6': (17,4,1,2), '0.337': (22,4,0,2),
       '0.355': (20,2,1,1), '0.357': (28,2,1,3), '0.51˙2': (16,6,3,6), '0.51˙6': (20,6,1,3), '0.53˙4': (19,4,1,2),
       '0.55˙2': (16,6,1,3), '0.55˙6': (20,6,1,3), '0.57˙0': (20,4,1,2), '0.57˙4': (19,4,1,2), '0.71˙6': (22,2,2,1),
       '0.72¯4': (19,4,1,2), '0.73˙2': (20,4,0,2), '0.73˙4': (4,4,0,2), '0.73˙6': (19,4,0,2), '0.75˙4': (17,2,1,1),
       '0.75˙6': (24,2,1,3), '4.¨0˙6': (16,4,1,2), '4.1˙6': (16,4,1,2), '4.5˙2': (17,4,1,2), '4.7˙0': (16,2,1,1)}
tup = {}
for name, t in T27.items():
    n2 = re.sub('([˙¨¯])(\\d)', lambda m: m.group(2) + m.group(1), name)
    for c in expand(n2): tup[c] = t
def msort(p): return tuple(sorted(p, reverse=True))
def inP734(u):  # p.27 explicit formula for 0.73˙4
    u = [x for x in u if x > 0]
    if u and all(x == 1 for x in u) and len(u) % 2 == 1: return True
    if not u or max(u) <= 2: return False
    S, Om = sum(u), sum(x % 2 for x in u); D = max(u) - (S - max(u))
    if D <= 1: return S % 2 == 0 and (S + Om) % 4 == 0
    return D % 2 == 0 and (D + Om) % 4 == 0
games = {}; out = []
for r in csv.DictReader(open('inputs/WITNESSES.tsv'), delimiter='\t'):
    c = r['game']
    g = games.setdefault(c, (Game(c), naive(c)))
    P, N, O = parse_pos(r['p_position']), parse_pos(r['n_position']), parse_pos(r['original_or_mismatching_position'])
    oP, oN = g[0].outcome(P), g[0].outcome(N)
    big = sum(P) + sum(N) > 70
    if True:
        assert g[1](P) == oP and g[1](N) == oN, ('naive disagrees', r)
    outcomes_ok = (oP == 'P' and oN == 'N')
    comp = r['comparison']; note = ''; rule_ok = None
    if comp.startswith('Def. 3.4'):
        p1, t1, p2, t2 = tup[c]; u = msort(O)
        a1, a2 = u[0], (u[1] if len(u) > 1 else 0)
        if a1 < p1 + t1: rule_ok = False; note = 'a1 below p1+t1'
        else:
            br = 1 if a2 < p2 + t2 else 2
            red = (a1 - t1,) + u[1:] if br == 1 else (a1 - t2, a2 - t2) + u[2:]
            rule_ok = (('branch %d' % br) in comp) and {msort(red), u} == {msort(P), msort(N)}
            note = f'tuple {tup[c]} branch {br}: {u} -> {msort(red)}'
    elif comp == 'outcome template' and 'explicit P formula' in r['source']:
        fp, fn = inP734(P), inP734(N)
        rule_ok = (fp == fn); note = f'formula says P? {P}:{fp} {N}:{fn}'
    elif comp == 'outcome template':
        seq = printed[c]
        mm = O  # the position the row says is printed wrongly
        pr1 = seq[mm[0]-1]; pr0 = seq[mm[0]] if mm[0] < len(seq) else None
        tru = g[0].outcome(mm)
        rule_ok = (pr1 != tru)
        row0 = [g[0].outcome((n,)) for n in range(0, len(seq))]
        if rule_ok and row0 == seq:  # whole printed row is exact if read from size 0
            rule_ok = 'offset'  # wrong only under the caption's "starting from size 1"; right if row starts at 0
        pr = [seq[x[0]-1] for x in (P, N)]
        note = f'mismatching {mm}: printed(from 1) {pr1}, true {tru}; printed if row starts at 0: {pr0}; printed P,N rows: {pr}'
    elif comp == 'Definition 4.2 branch 2':
        m = re.search(r'Fixed prefix \((\d+), (\d+)\), tuple \((\d+), (\d+), (\d+), (\d+)\)', r['detail'])
        a, b, p1, t1, p2, t2 = map(int, m.groups())
        rest = list(O); rest.remove(a); rest.remove(b); x1, x2 = max(rest), min(rest)
        ok = x1 >= p1 + t1 and x2 >= p2 + t2
        red = (a, b, x1 - t2, x2 - t2)
        rule_ok = ok and {msort(red), msort(O)} == {msort(P), msort(N)}
        note = f'prefix ({a},{b}) tuple {(p1,t1,p2,t2)}: {O} -> {red}; x1>=p1+t1 {x1>=p1+t1}, x2>=p2+t2 {x2>=p2+t2}'
    elif comp in ('residue key', 'published residue counterexample'):
        def key(u):
            u = list(u) + [0] * (4 - len(u)); u = sorted(u, reverse=True)
            # slice o(2,2,x,y): remove the two fixed 2s
            w = list(u); w.remove(2); w.remove(2); x, y = w
            return (x % 7, y % 7, abs(x - y) <= 4), (x, y)
        kP, kN = key(P), key(N)
        # key is symmetric in x,y only up to ordering; compare as unordered residue pair
        kk = lambda k: (tuple(sorted(k[0][:2])), k[0][2])
        rule_ok = kk(kP) == kk(kN); note = f'(x,y)={kP[1]} key {kP[0]} vs (x,y)={kN[1]} key {kN[0]}'
    elif comp == 'fixed heap folding':
        rule_ok = None; note = 'Conjecture 4.4 asserts folding FAILS; an inequality agrees with it'
    status = ('UNCLEAR-OFFSET' if outcomes_ok and rule_ok == 'offset' else 'CONFIRMED' if outcomes_ok and rule_ok
              else 'NOT-A-REFUTATION' if rule_ok is None and outcomes_ok else 'REJECTED')
    out.append(dict(game=c, comparison=comp, source=r['source'], P=P, N=N, oP=oP, oN=oN, rule_ok=rule_ok, status=status, note=note))
    print(f"{status:16s} {c:7s} {comp:28s} {str(P):26s}{oP} {str(N):26s}{oN} | {note}")
json.dump(out, open('witness_results.json', 'w'), indent=1, default=str)

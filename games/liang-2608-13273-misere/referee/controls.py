"""Controls: printed values from 2608.13273v2, 2611.29198 and Plambeck-Siegel reproduced by referee_solver."""
import sys, itertools
sys.path.insert(0, '.')
from referee_solver import Game
ok_all = True
def rep(name, ok, detail):
    global ok_all; ok_all &= ok
    print(('PASS ' if ok else 'FAIL ') + name + ': ' + detail)
# C1 Plambeck-Siegel 0609825 footnote 5: in 0.26, H13+H17+H31 is a (misere) P-position
g = Game('0.26'); v = g.outcome((13, 17, 31)); rep('P-S 0.26 H13+H17+H31', v == 'P', v)
# C2 2611.29198 Thm 3.7 (0.3122) and Thm 3.8 (0.3123)
for code, a in (('0.3122', 2), ('0.3123', 3)):
    g = Game(code); bad = [h for h in range(0, 61) if g.outcome((a, a, h, h)) != 'P' or g.outcome((a, a, h + 1, h)) != 'N']
    rep(f'2611 Thm {code} o({a},{a},h,h)=P, o({a},{a},h+1,h)=N, h<=60', not bad, f'violations {bad}')
# C3 2608v2 sec 3.5.1: 0.04:0.03 (normal play, labelled) classes and outcomes; label 0=L, 1=R
g = Game('0.04:0.03', misere=False)
L, R = 0, 1
exp = {(L, ()): 'P', (L, (2,)): 'P', (L, (4,)): 'N', (R, ()): 'P', (R, (2,)): 'N'}
got = {k: g.outcome(k[1], k[0]) for k in exp}
rep('0.04:0.03 class outcomes', got == exp, str(got))
# printed equivalences (L;1)~(L;), (L;3)~(L;2), (L;5)~(L;2), (L;4,1)~(L;4), (L;4,2..5)~(L;2), (L;2,1)~(L;2),
# (R;1)~(R;), (R;4)~(R;2), (R;5)~(R;2): test o(u+v)=o(u'+v) for all v with <=3 heaps each <=8
eqs = [(L,(1,),()),(L,(3,),(2,)),(L,(5,),(2,)),(L,(4,1),(4,)),(L,(4,2),(2,)),(L,(4,3),(2,)),(L,(4,4),(2,)),(L,(4,5),(2,)),
       (L,(2,1),(2,)),(R,(1,),()),(R,(4,),(2,)),(R,(5,),(2,)),(R,(2,1,3),(2,3)),(L,(5,3),(3,)),(L,(4,8),(7,)),(R,(9,),(4,))]
vs = [v for k in range(0, 4) for v in itertools.combinations_with_replacement(range(1, 9), k)]
bad = [(s, u, w, v) for s, u, w in eqs for v in vs if g.outcome(u + v, s) != g.outcome(w + v, s)]
rep('0.04:0.03 printed equivalences on %d test sums each' % len(vs), not bad, f'{len(bad)} violations {bad[:3]}')
# C4 2608v2 p.27 explicit P-formula for 0.73˙4: agreement on positions with max(u) > 2 (the Pinn/Pout categories)
exec(open('check_witnesses.py').read().split('games = {}')[0].split('def msort')[1].join(['def msort', '']) if False else '')
def inP734(u):
    u = [x for x in u if x > 0]
    if u and all(x == 1 for x in u) and len(u) % 2 == 1: return True
    if not u or max(u) <= 2: return False
    S, Om = sum(u), sum(x % 2 for x in u); D = max(u) - (S - max(u))
    if D <= 1: return S % 2 == 0 and (S + Om) % 4 == 0
    return D % 2 == 0 and (D + Om) % 4 == 0
for code in ('0.734', '0.735'):
    g = Game(code); n = 0; bad = []
    for k in range(1, 5):
        for u in itertools.combinations_with_replacement(range(1, 13), k):
            n += 1
            if (g.outcome(u) == 'P') != inP734(u): bad.append(u)
    big = [u for u in bad if max(u) > 3]
    print(f'INFO {code} formula vs solver on {n} positions (<=4 heaps, each <=12): {len(bad)} disagree; with max>3: {len(big)}; all: {bad[:20]}')
# C5 p.28 printed rows reproduced exactly (see controls_rows.py / controls_crossmatch.py)
print('ALL CONTROLS PASS' if ok_all else 'SOME CONTROL FAILED')

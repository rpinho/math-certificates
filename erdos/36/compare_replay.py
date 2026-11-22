"""Compare a replay_all.sh output directory with the shipped results. Stdlib only.
usage: python -I compare_replay.py REPLAY_OUT_DIR      Prints PASS/FAIL per check; exit 1 on any FAIL."""
import json, os, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); R = sys.argv[1]
J = lambda *p: json.load(open(os.path.join(*p)))
T = lambda *p: open(os.path.join(*p)).read()
fails = 0
def chk(name, ok, extra=''):
    global fails; fails += not ok
    print(('PASS ' if ok else 'FAIL ') + name + (('  ' + extra) if extra else ''))
S = J(HERE, 'results', 'vK_main.json'); P = J(R, 'vK_main.json')
chk('producer: 94 bins, all pass, 0 slope violations, cover [0,1/160] exact',
    P['n_bins'] == 94 and P['all_pass'] and P['n_fail'] == 0 and P['cover']['covers_target'] and not P['cover']['gaps']
    and sum(b['slope_violations'] for b in P['bins']) == 0)
tg = [b['margin'] for b in P['bins'] if F(b['hi']) > F('0.000146')]
chk('producer: min margin overall = +3.05e-10', abs(P['min_margin'] - 3.0518327e-10) < 1e-15, '%.6e' % P['min_margin'])
chk('producer: min margin on bins meeting [1.46e-4,1/160] (%d bins) = +1.866e-9' % len(tg), len(tg) == 77 and abs(min(tg) - 1.8664913e-9) < 1e-14, '%.6e' % min(tg))
chk('producer: every bin identical to shipped vK_main.json', P['bins'] == S['bins'])
chk('D_up identical to shipped', J(R, 'dint2_res.json')['D_up'] == J(HERE, 'producer', 'dint2', 'res_main.json')['D_up'] and J(R, 'dint2_res.json')['n_arb_fail'] == 0)
for n, f in [('raiseL', lambda c: c['n_fail'] == 79), ('flip', lambda c: sum(b['slope_violations'] for b in c['bins']) == 549 and c['n_fail'] == 1),
             ('nocap', lambda c: c['n_fail'] == 1 and c['min_margin'] < 0), ('drop', lambda c: not c['cover']['covers_target'] and len(c['cover']['gaps']) == 1)]:
    c = J(R, 'ctrl_%s.json' % n); chk('producer control %s rejects' % n, f(c), 'n_fail=%d covers_target=%s' % (c['n_fail'], c['cover']['covers_target']))
c = J(R, 'vK_N0shift.json'); chk('producer: N0 lowered by 1e-27, all 94 bins still pass', c['all_pass'] and c['n_bins'] == 94)
Rr = J(R, 'referee', 'replay.json'); s = Rr['summary']; Rs = J(HERE, 'referee', 'replay.json')
chk('referee: 94 bins, 6160384 cell checks, 0 violations, 0 gaps', s['bins'] == 94 and s['cell_checks'] == 6160384 and s['violations'] == 0 and not s['gaps'])
chk('referee: margins +3.0518e-10 (all) and +1.8665e-9 (target bin 17)', abs(s['minimum_margin'] - 3.0518347e-10) < 1e-15 and abs(s['target_margin'] - 1.8664915e-9) < 1e-14 and s['target_bin'] == 17)
chk('referee: every bin and ledger identical to shipped', Rr['bins'] == Rs['bins'] and Rr['ledger'] == Rs['ledger'])
cc = Rr['controls']
chk('referee controls reject (raise 1e-9, raise 1e-6, flip, slope, drop)', bool(cc['raise_1e-9']['failed']) and bool(cc['raise_1e-6']['failed']) and bool(cc['flip']['violations']) and bool(cc['slope']['violations']) and bool(cc['drop']['gaps']))
chk('referee fixtures: all 7 pass, identical to shipped', J(R, 'referee', 'fixtures.json') == J(HERE, 'referee', 'fixtures.json') and all(x['pass_exact'] for x in J(R, 'referee', 'fixtures.json')['fixtures']))
chk('producer fixtures_K (16 step functions) identical to shipped', J(R, 'fixtures_K.json') == J(HERE, 'results', 'fixtures_K.json'))
chk('make_K.py search output byte-identical to shipped certificate', open(os.path.join(R, 'certK_search.json'), 'rb').read() == open(os.path.join(HERE, 'certificates', 'certK_r105.json'), 'rb').read())
chk('ledger_arb: provable lower expectation exceeds N0 (+2.283e-27)', 'exact kappa + actual errors      LB - N0 in [2.2830e-27, 2.2830e-27]   LB >= N0 proved: True' in T(R, 'ledger', 'ledger_arb.log'))
chk('scatter_exact: periodic offsets match on all 131072 cells', '0 of 131072' in T(R, 'ledger', 'scatter_exact.log'))
chk('c_check: C ledger residual = 2^-20 x two-scale C', '9.5367431640625e-07' in T(R, 'ledger', 'c_check.log'))
print('compare_replay:', 'PASS' if fails == 0 else 'FAIL (%d)' % fails); sys.exit(1 if fails else 0)

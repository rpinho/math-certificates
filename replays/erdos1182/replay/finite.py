"""Replay the numeric inequalities in the finite-n and connectivity lemmas."""
import json
from fractions import Fraction as F
from pathlib import Path

from flint import arb,ctx,fmpq

ctx.prec=160
for case,n0 in [('11',10**6),('503',10**9)]:
    line=Path('check-'+case+'.log').read_text()
    label,raw=line.split(' ',1)
    proof=json.loads(raw)
    assert label=='PASS' and proof['case']==case and proof['mode']=='arb_and_coverage'
    slope=F(proof['worst_ticks'],proof['tick_scale'])
    assert F(11,n0)+slope<0
    log_ex=(arb(125).log()+2+6*arb(11*n0+1).log()+5*arb(n0+1).log()
            +arb(fmpq(slope.numerator,slope.denominator))*n0)
    assert log_ex < -arb(2).log()
    print(f'case={case} n0={n0} uniform log E X upper at threshold {log_ex.str(18)}, derivative negative thereafter')
rho=arb(1).exp()*arb(fmpq(11,10))**5/16
assert rho/(1-rho)<arb(fmpq(1,2))
print(f'cut union bound { (rho/(1-rho)).str(18) } < 1/2')

"""Arb quadrature and absolute-value enclosures for the documented kernel."""
from collections import defaultdict
from fractions import Fraction as F
from math import factorial

from flint import arb, arb_poly

from referee_data import GRID, ball, bounds

BLOCKS_PER_UNIT = 512
DEG = 36
SCALE = 2**80


def affine_pieces(grids, constant):
    # Keep each original hat breakpoint. Accumulate slope changes exactly.
    changes = defaultdict(F)
    initial = constant
    for heights in grids:
        n = len(heights)-1
        initial += heights[0]
        last = F(0)
        for i in range(n):
            slope = (heights[i+1]-heights[i])*n/2
            changes[F(2*i,n)] += slope-last
            last = slope
    knots = sorted(set(changes) | {F(i,GRID) for i in range(2*GRID+1)})
    slope, value = F(0), initial
    for left,right in zip(knots,knots[1:]):
        slope += changes.get(left,0)
        yield left,right,value,slope
        value += slope*(right-left)


class Fourier:
    """Taylor coefficients and uniform remainder on each 1/512 block."""
    def __init__(self, cosines):
        half = F(1,2*BLOCKS_PER_UNIT)
        self.tables = []
        for freq,z in cosines.items():
            xi = ball(freq)
            powers = [ball(z)]
            for j in range(1,DEG+1):
                powers.append(powers[-1]*xi/j)
            self.tables.append((xi,powers))
        self.errors = []
        for d in range(3):
            degree = DEG+1-d
            rem = sum(abs(ball(z))*ball(xi)**(DEG+1) for xi,z in cosines.items())
            self.errors.append(rem*ball(half)**degree/factorial(degree))
        self.third = sum(abs(ball(z))*ball(xi)**3 for xi,z in cosines.items())

    def at_block(self, center, y2):
        coeff = [arb(0) for _ in range(DEG+1)]
        for xi,powers in self.tables:
            sn,cs = (xi*center).sin_cos()
            phases = (cs,-sn,-cs,sn)
            for j,a in enumerate(powers):
                coeff[j] += a*phases[j%4]
        coeff[0] += y2*center**2
        coeff[1] += 2*y2*center
        coeff[2] += y2
        return arb_poly(coeff)


class PieceIntegrator:
    def __init__(self, series):
        self.series = series
        self.positive = arb(0)
        self.unresolved = arb(0)
        self.count = dict(smooth=0,positive=0,negative=0,brackets=0,splits=0)
        self.piece_budget = ball(F(1,10**22))
        self.flat = ball(F(1,10**18))

    def start_block(self, center, y2):
        self.center = center
        self.poly = self.series.at_block(center,y2)
        self.prim = self.poly.integral()
        self.prime = self.poly.derivative()
        self.second = self.prime.derivative()

    def interval(self, left, right, v, slope, depth=0):
        # The affine part has value v at left. The polynomial variable
        # is displacement from the block center, never an absolute time.
        half = (right-left)/2
        mid = left+half
        x = mid-self.center
        val = self.poly(x)+v+slope*half
        first = self.prime(x)+slope
        e0,e1,e2 = self.series.errors
        radius = e0 + (abs(first)+e1)*half + (abs(self.second(x))+e2)*half**2/2
        radius += self.series.third*half**3/6
        ran = val+arb(0,radius.upper())
        if ran > 0:
            # Exact primitive for the polynomial, paid uniform Taylor error.
            area = self.prim(right-self.center)-self.prim(left-self.center)
            area += (right-left)*(v+slope*half+arb(0,e0.upper()))
            self.positive += area
            self.count['positive'] += 1
        elif ran < 0:
            self.count['negative'] += 1
        else:
            cap = (right-left)*ran.upper()
            if cap < self.piece_budget or ran.upper() < self.flat:
                self.unresolved += cap
                self.count['brackets'] += 1
            else:
                assert depth < 70
                self.count['splits'] += 1
                self.interval(left,mid,v,slope,depth+1)
                self.interval(mid,right,v+slope*half,slope,depth+1)
        return ran


def enclose(c0, y2, cosines, grids, offsets):
    state = PieceIntegrator(Fourier(cosines))
    cell_lo = [None]*(2*GRID)
    cell_hi = [0]*(2*GRID)
    block = -1
    for a,b,value,slope in affine_pieces(grids,c0):
        cell = int(a*GRID)
        new_block = int(a*BLOCKS_PER_UNIT)
        if block != new_block:
            block = new_block
            state.start_block(ball(F(2*block+1,2*BLOCKS_PER_UNIT)), ball(y2))
        ran = state.interval(ball(a),ball(b),ball(value+offsets.get(cell,0)),ball(slope))
        # Convert endpoints to fixed point integers, always rounding out.
        lo = int((ran.abs_lower()*SCALE).lower().floor().unique_fmpz())
        hi = int((ran.abs_upper()*SCALE).upper().ceil().unique_fmpz())
        cell_lo[cell] = lo if cell_lo[cell] is None else min(cell_lo[cell],lo)
        cell_hi[cell] = max(cell_hi[cell],hi)
        state.count['smooth'] += 1
    folded_lower = [cell_lo[i]+cell_lo[-1-i] for i in range(GRID)]
    folded_upper = [cell_hi[i]+cell_hi[-1-i] for i in range(GRID)]
    dlo = bounds(2*state.positive)[0]
    dup = bounds(2*(state.positive+state.unresolved))[1]
    assert 0 < dlo <= dup
    return folded_lower, folded_upper, dlo, dup, state.count

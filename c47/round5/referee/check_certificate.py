#!/usr/bin/env python3
"""C47 referee using its own checks, written from the definition and periodic smearing proof.

Only Python's standard library is used. All mathematical comparisons and area
computations are exact. Decimal conversions are display-only. No producer code
is imported, read or run. Certificate endpoints mean closed boxes/rectangles.
"""
import argparse
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from hashlib import sha256
# Exact integer helpers are defined below; no floating arithmetic is needed.
from pathlib import Path
import json
import os
import time

TARGET = F('1.7048221231')
CLAIMED_Q = F('57160787529186565434927719505838181711244340833364808847853/33528886534937259000645393217902994011665203200000000000000')
CLAIMED_AREA = F('57160787529186565434927719505838181711244340833364808847853/6338253001141147007483516026880000000000000000000000000000')
CLAIMED_MASS = F('16531017364377/3125000000000')
CLAIMED_SLACK = F('34802060175181125102274071/129807421463370690713262408230502400000000000000')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decimal(q):
    with localcontext() as ctx:
        ctx.prec = 75
        return str(ctx.divide(Decimal(q.numerator), Decimal(q.denominator)))


def rational(s):
    require(isinstance(s, (str, int)) and not isinstance(s, bool),
            'Mathematical data must be rational strings or integers, never floats')
    return F(s)


def union_area(rectangles):
    """Sweep exact open slabs; boundary segments have zero Lebesgue area.

    Scaling each axis by the LCM of its denominators maps all endpoints to
    integers. At each slab, merge the active y intervals, sum their lengths,
    then multiply by slab width. Divide by the two scales only at the end.
    """
    sx = lcm(*(v.denominator for r in rectangles for v in r[:2]))
    sy = lcm(*(v.denominator for r in rectangles for v in r[2:]))
    events = defaultdict(list)
    ys = []
    for i, (u, v, s, t) in enumerate(rectangles):
        a, b, c, d = u*sx, v*sx, s*sy, t*sy
        require(all(z.denominator == 1 for z in (a,b,c,d)), 'Integer scaling')
        a, b, c, d = map(int, (a,b,c,d))
        events[a].append((i, 1))
        events[b].append((i, -1))
        ys.append((c,d))
    active = set()
    previous = None
    total = 0
    slabs = 0
    max_active = 0
    for x in sorted(events):
        if previous is not None and x > previous:
            intervals = sorted(ys[i] for i in active)
            length = 0
            if intervals:
                lo, hi = intervals[0]
                for c, d in intervals[1:]:
                    if c > hi:
                        length += hi-lo
                        lo, hi = c,d
                    else:
                        hi = max(hi,d)
                length += hi-lo
            total += (x-previous)*length
            slabs += 1
        # Ending rectangles are removed, starting rectangles added for next slab.
        for i, direction in events[x]:
            if direction == 1:
                active.add(i)
            else:
                active.remove(i)
        max_active = max(max_active, len(active))
        previous = x
    require(not active, 'All rectangles must end')
    return F(total, sx*sy), {'x_slabs':slabs, 'maximum_active_rectangles':max_active,
                           'x_integer_scale':str(sx), 'y_integer_scale':str(sy)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', default='../certificates/final.json')
    parser.add_argument('--finite', default='../producer_logs/final-finite.json')
    parser.add_argument('--out', default='CHECK_RESULTS.json')
    args = parser.parse_args()
    started = time.monotonic()
    print(f'pid={os.getpid()} nice={os.getpriority(os.PRIO_PROCESS,0)}', flush=True)
    raw = Path(args.certificate).read_bytes()
    cert = json.loads(raw)
    finite = json.loads(Path(args.finite).read_text())
    m = cert['measure']
    px, py, level = map(rational, (m['Px'],m['Py'],m['lam']))
    require(px > 0 and py > 0 and level == 1, 'Positive periods and level one')
    atoms = [tuple(map(rational, p)) for p in m['pts']]
    require(len(atoms) == 392, '392 base atoms')
    require(all(len(p)==3 for p in atoms), 'Atom triples')
    require(all(0 <= x < px and 0 <= y < py and mass > 0
                for x,y,mass in atoms), 'Positive atoms in half-open cell')
    require(len(set((x,y) for x,y,_ in atoms)) == len(atoms), 'No duplicate positions')
    mass = sum((p[2] for p in atoms), F(0))
    require(mass == CLAIMED_MASS, 'Cell mass matches PROOF.md:36')
    boxes, radii, rectangles, masses, counts = [], [], [], [], []
    kmin = lmin = 0
    kmax = lmax = 0
    boundary_incidents = 0
    require(len(cert['witnesses']) == 4735, '4735 witnesses')
    for i, witness in enumerate(cert['witnesses']):
        box = tuple(map(rational, witness['box']))
        rect = tuple(map(rational, witness['rectangle']))
        r = rational(witness['radius'])
        require(len(box)==4 and len(rect)==4, f'Witness {i}: endpoint counts')
        a,b,c,d = box
        u,v,s,t = rect
        require(a <= b and c <= d, f'Witness {i}: ordered box')
        require(0 <= u < v <= px and 0 <= s < t <= py, f'Witness {i}: clipped positive rectangle')
        require(r > 0, f'Witness {i}: positive radius')
        require(u >= b-r and v <= a+r and s >= d-r and t <= c+r,
                f'Witness {i}: every center contains its full box')
        # For each base atom, exactly these integer translations lie in the
        # closed box. No heuristic reach or preselected image window is used.
        bm = F(0)
        count = 0
        on_boundary = 0
        for x,y,w in atoms:
            kl, kh = ceil(F(a-x)/F(px)), floor(F(b-x)/F(px))
            ll, lh = ceil(F(c-y)/F(py)), floor(F(d-y)/F(py))
            if kl <= kh and ll <= lh:
                nx, ny = kh-kl+1, lh-ll+1
                bm += nx*ny*w
                count += nx*ny
                kmin,kmax = min(kmin,kl),max(kmax,kh)
                lmin,lmax = min(lmin,ll),max(lmax,lh)
                # Count images on any of the four closed-box edges once.
                for k in range(kl,kh+1):
                    for l in range(ll,lh+1):
                        if x+k*px in (a,b) or y+l*py in (c,d):
                            on_boundary += 1
        require(bm > 4*level*r*r, f'Witness {i}: strict mass inequality')
        boxes.append(box)
        rectangles.append(rect)
        radii.append(r)
        masses.append(bm)
        counts.append(count)
        boundary_incidents += on_boundary
        if (i+1)%1000==0:
            print(f'Checked {i+1} witnesses', flush=True)
    slack = min(bm-4*level*r*r for bm,r in zip(masses,radii))
    slack_index = next(i for i,(bm,r) in enumerate(zip(masses,radii)) if bm-4*level*r*r==slack)
    rmax = max(radii)
    require(slack == CLAIMED_SLACK, 'Minimum slack matches PROOF.md:38')
    area, sweep = union_area(rectangles)
    ratio = F(level*area)/F(mass)
    require(0 < area <= px*py, 'Area between zero and full cell')
    require(area == CLAIMED_AREA, 'Area matches PROOF.md:37')
    require(ratio == CLAIMED_Q, 'Ratio matches PROOF.md:37')
    require(ratio > TARGET, 'Periodic ratio exceeds requested decimal')
    # Check every number that is part of the supplied finite construction.
    h, n = finite['boundary_cells'], finite['block_side_cells']
    require(type(h) is int and type(n) is int and h >= 0 and n > 2*h,
            'Finite-block integer parameters')
    eps = rational(finite['smear_radius'])
    require(h*min(px,py) > rmax, 'Strict block boundary clearance')
    require(-h <= kmin <= kmax <= h and -h <= lmin <= lmax <= h,
            'Every counted image retained for every inner cell')
    require(0 < eps <= F(1,2), 'Smearing radius positive and at most one half')
    require(4*level*(2*rmax+1)*eps < slack, 'Uniform smearing margin')
    expanded_slacks = [bm-4*level*(r+eps)**2 for bm,r in zip(masses,radii)]
    require(min(expanded_slacks) > 0, 'All expanded witness squares have average >1')
    finite_ratio = ratio * F(n-2*h,n)**2
    norm = n*n*mass
    atom_count = n*n*len(atoms)
    require(finite_ratio > TARGET, 'Finite ratio exceeds requested decimal')
    require(rational(finite['claim']) == TARGET, 'Finite log target')
    require(rational(finite['maximum_witness_radius']) == rmax, 'Finite log radius')
    require(rational(finite['finite_function_L1_norm']) == norm, 'Finite log L1 norm')
    require(finite['finite_atom_count'] == atom_count, 'Finite log atom count')
    require(rational(finite['finite_ratio_lower_bound']) == finite_ratio, 'Finite log ratio')
    require(finite['artifact_sha256'] == sha256(raw).hexdigest(), 'Finite log references these certificate bytes')
    require(floor(ratio*10**10) == 17048221231, 'Ten-decimal downward truncation')
    details = {
        'result':'PASS', 'certificate_sha256':sha256(raw).hexdigest(),
        'period_x':px, 'period_y':py, 'level':level,
        'base_atoms':len(atoms), 'witnesses_checked':len(rectangles),
        'outside_cell_atoms':0, 'duplicate_positions':0,
        'atoms_on_left_edge':sum(x==0 for x,y,w in atoms),
        'atoms_on_bottom_edge':sum(y==0 for x,y,w in atoms),
        'atoms_on_right_or_top_edge':sum(x==px or y==py for x,y,w in atoms),
        'cell_mass':mass, 'union_area':area, 'cell_uncovered_area':px*py-area,
        'periodic_ratio':ratio, 'claimed_periodic_ratio':CLAIMED_Q,
        'periodic_decimal':decimal(ratio), 'target':TARGET,
        'periodic_minus_target':ratio-TARGET,
        'minimum_mass_slack':slack, 'minimum_slack_witness_zero_based':slack_index,
        'maximum_radius':rmax, 'minimum_radius':min(radii),
        'atom_image_counts_min_max':[min(counts),max(counts)],
        'atom_image_incidents':sum(counts), 'box_boundary_atom_incidents':boundary_incidents,
        'image_index_ranges':{'k':[kmin,kmax],'l':[lmin,lmax]},
        'union_sweep':sweep,
        'h':h, 'N':n, 'epsilon':eps,
        'smearing_uniform_margin':slack-4*level*(2*rmax+1)*eps,
        'minimum_expanded_square_mass_slack':min(expanded_slacks),
        'finite_atom_count':atom_count, 'finite_L1_norm':norm,
        'finite_ratio':finite_ratio, 'finite_decimal':decimal(finite_ratio),
        'finite_minus_target':finite_ratio-TARGET,
        'finite_minus_target_decimal':decimal(finite_ratio-TARGET),
        'elapsed_seconds':time.monotonic()-started,
    }
    Path(args.out).write_text(json.dumps(details,default=str,indent=2)+'\n')
    print('PASS: all witnesses, union area, and finite parameters match',flush=True)
    print('Periodic ratio:',decimal(ratio),flush=True)
    print('Finite ratio:',decimal(finite_ratio),flush=True)


# Exact integer helpers; equivalent to math.ceil/floor/lcm on these inputs.
def floor(q):
    return q.numerator // q.denominator


def ceil(q):
    return -((-q.numerator) // q.denominator)


def lcm(*values):
    result = 1
    for value in values:
        a, b = result, value
        while b:
            a, b = b, a % b
        result = result // a * value
    return result

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Clean-room C47 check: standard library only; never imports producer code.

For each base atom p and closed box [a,b] x [c,d], the admissible
horizontal shifts are ceil((a-px)/Px) through floor((b-px)/Px), inclusive.
The vertical shifts are counted independently. Their product counts exactly
all periodic copies, with no finite search-window assumption.

The rectangle union is integrated in vertical slabs. Endpoints are scaled
to a common integer denominator; a coverage-count segment tree maintains
exact covered y-length. Thus all mathematical decisions use integers or
Fraction, never float. Decimal is used only for human-readable output.
"""
import argparse
import csv
from decimal import Decimal, localcontext
from fractions import Fraction as F
from hashlib import sha256
import json
# Exact integer helpers are defined below.
import os
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decimal(q):
    with localcontext() as ctx:
        ctx.prec = 85
        return str(ctx.divide(Decimal(q.numerator), Decimal(q.denominator)))


def union_area(rectangles):
    # Compress exact coordinates; the scale is derived from data, not D.
    scale = lcm(*(z.denominator for r in rectangles for z in r))
    integer_rectangles = [tuple(z.numerator * (scale // z.denominator)
                                for z in r) for r in rectangles]
    ys = sorted({z for r in integer_rectangles for z in r[2:]})
    pos = {v: i for i, v in enumerate(ys)}
    intervals = len(ys) - 1
    cover = [0] * (4 * intervals + 8)
    length = [0] * len(cover)

    def update(node, left, right, start, stop, change):
        if start <= left and right <= stop:
            cover[node] += change
            require(cover[node] >= 0, 'negative sweep coverage')
        else:
            mid = (left + right) // 2
            if start < mid:
                update(2 * node, left, mid, start, stop, change)
            if stop > mid:
                update(2 * node + 1, mid, right, start, stop, change)
        if cover[node]:
            length[node] = ys[right] - ys[left]
        elif right - left == 1:
            length[node] = 0
        else:
            length[node] = length[2 * node] + length[2 * node + 1]

    events = []
    for u, v, s, t in integer_rectangles:
        events.append((u, 1, pos[s], pos[t]))
        events.append((v, -1, pos[s], pos[t]))
    events.sort()
    area = 0
    previous = events[0][0]
    slab_count = 0
    for x, change, lower, upper in events:
        if x != previous:
            area += (x - previous) * length[1]
            slab_count += 1
        update(1, 0, intervals, lower, upper, change)
        previous = x
    require(length[1] == 0 and all(c == 0 for c in cover), 'unfinished sweep')
    return F(area, scale * scale), {
        'coordinate_scale': str(scale),
        'x_slabs': slab_count,
        'y_intervals': intervals,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', default='../certificates/final.json')
    ap.add_argument('--finite', default='../producer_logs/final-finite.json')
    ap.add_argument('--output', default='CHECK_RESULTS.json')
    ap.add_argument('--witness-output', default='witness_checks.csv')
    args = ap.parse_args()
    started = time.monotonic()
    try:
        os.setpriority(os.PRIO_PROCESS, 0, 10)
        priority_note = 'absolute nice 10'
    except PermissionError:
        priority_note = 'OS denied nice 10; retained lower inherited priority'
    actual_nice = os.getpriority(os.PRIO_PROCESS, 0)
    require(actual_nice >= 10, 'priority higher than authorized')
    print(f'pid={os.getpid()} nice={actual_nice}; {priority_note}', flush=True)
    raw = Path(args.certificate).read_bytes()
    data = json.loads(raw)
    m = data['measure']
    px, py, level = (F(m[k]) for k in ('Px', 'Py', 'lam'))
    require(px > 0 and py > 0 and level == 1, 'periods or level invalid')
    atoms = [tuple(F(v) for v in p) for p in m['pts']]
    require(len(atoms) == 474, 'wrong atom count')
    require(all(len(a) == 3 for a in atoms), 'malformed atom')
    require(all(0 <= x < px and 0 <= y < py and w > 0 for x, y, w in atoms),
            'atom outside half-open cell or nonpositive mass')
    require(len({(x, y) for x, y, w in atoms}) == len(atoms),
            'duplicate location (including modulo period)')
    mass = sum((w for x, y, w in atoms), F(0))
    require(mass == F('529047036568853/100000000000000'), 'claimed cell mass differs')
    witnesses = data['witnesses']
    require(len(witnesses) == 6292, 'wrong witness count')
    radii, masses, slacks, rectangles, rows = [], [], [], [], []
    shift_x_min = shift_y_min = 0
    shift_x_max = shift_y_max = 0
    minimum_containment = None
    for index, witness in enumerate(witnesses):
        a, b, c, d = map(F, witness['box'])
        r = F(witness['radius'])
        u, v, s, t = rect = tuple(map(F, witness['rectangle']))
        require(a <= b and c <= d and r > 0, f'witness {index}: box/radius invalid')
        require(0 <= u < v <= px and 0 <= s < t <= py,
                f'witness {index}: rectangle not positive and inside closed cell')
        contain = min(u - (b-r), (a+r) - v, s - (d-r), (c+r) - t)
        require(contain >= 0, f'witness {index}: box containment fails')
        minimum_containment = contain if minimum_containment is None else min(minimum_containment, contain)
        box_mass = F(0)
        number = 0
        boundary_number = 0
        for x, y, w in atoms:
            k0, k1 = ceil(F(a-x)/F(px)), floor(F(b-x)/F(px))
            l0, l1 = ceil(F(c-y)/F(py)), floor(F(d-y)/F(py))
            nx, ny = max(0, k1-k0+1), max(0, l1-l0+1)
            count = nx * ny
            if not count:
                continue
            box_mass += count * w
            number += count
            shift_x_min, shift_x_max = min(shift_x_min, k0), max(shift_x_max, k1)
            shift_y_min, shift_y_max = min(shift_y_min, l0), max(shift_y_max, l1)
            # Count the copies lying on any closed box boundary, without
            # counting corner copies twice. This is diagnostic, not a mass shortcut.
            interior_x = max(0, ceil(F(b-x)/F(px)) - floor(F(a-x)/F(px)) - 1)
            interior_y = max(0, ceil(F(d-y)/F(py)) - floor(F(c-y)/F(py)) - 1)
            boundary_number += count - interior_x * interior_y
        slack = box_mass - 4 * level * r * r
        require(slack > 0, f'witness {index}: strict mass slack fails: {slack}')
        radii.append(r)
        masses.append(box_mass)
        slacks.append(slack)
        rectangles.append(rect)
        rows.append((index, number, boundary_number, str(box_mass), str(slack), str(contain)))
        if (index+1) % 500 == 0:
            print(f'checked {index+1}/{len(witnesses)} witnesses in {time.monotonic()-started:.1f}s', flush=True)
    area, sweep = union_area(rectangles)
    claimed_area = F('28587164107974856086021451670774323985081039148875463526401/3169126500570573503741758013440000000000000000000000000000')
    claimed_ratio = F('28587164107974856086021451670774323985081039148875463526401/16766169836386813382037844357636904350593843200000000000000')
    ratio = F(level * area) / F(mass)
    require(area == claimed_area, 'claimed union area differs')
    require(ratio == claimed_ratio, 'claimed ratio differs')
    require(0 < area <= px*py, 'union area outside cell area')
    delta = min(slacks)
    claimed_delta = F('121866966319552490346558479/519229685853482762853049632922009600000000000000')
    require(delta == claimed_delta, 'claimed minimum slack differs')
    rmax = max(radii)
    finite = json.loads(Path(args.finite).read_bytes())
    require(finite['artifact_sha256'] == sha256(raw).hexdigest(), 'finite artifact hash mismatch')
    h, n = finite['boundary_cells'], finite['block_side_cells']
    require(type(h) is int and type(n) is int and h >= 0 and n > 2*h, 'invalid h,N')
    require(h * min(px,py) > rmax, 'insufficient retained cell margin')
    eps = F(finite['smear_radius'])
    require(0 < eps <= F(1,2), 'invalid smear radius')
    smear_cost_bound = 4 * level * (2*rmax+1)*eps
    require(smear_cost_bound < delta, 'uniform smear inequality fails')
    smeared_slacks = [m0 - 4*level*(r+eps)**2 for m0,r in zip(masses,radii)]
    require(min(smeared_slacks) > 0, 'a smeared witness has nonpositive slack')
    # Check retained atom cell indices directly as well as the radius bound.
    require(h + min(shift_x_min,shift_y_min) >= 0, 'left/bottom copy missing')
    require(n-h-1 + max(shift_x_max,shift_y_max) < n, 'right/top copy missing')
    finite_ratio = ratio * F(n-2*h,n)**2
    target = F('1.7050503714')
    require(F(finite['claim']) == target, 'wrong finite target')
    require(rmax == F(finite['maximum_witness_radius']), 'finite Rmax differs')
    require(mass*n*n == F(finite['finite_function_L1_norm']), 'finite norm differs')
    require(len(atoms)*n*n == finite['finite_atom_count'], 'finite atom count differs')
    require(finite_ratio == F(finite['finite_ratio_lower_bound']), 'finite ratio differs')
    require(finite_ratio > target, 'finite ratio does not exceed target')
    require(target <= ratio < target+F(1,10**10), 'decimal truncation incorrect')
    with open(args.witness_output, 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(['witness_index_0based','periodic_atom_count','closed_boundary_atom_count',
                         'box_mass','strict_mass_slack','minimum_containment_slack'])
        writer.writerows(rows)
    result = {
        'status':'all requested exact certificate and finite arithmetic checks pass',
        'certificate_sha256':sha256(raw).hexdigest(),
        'atoms':len(atoms),'witnesses':len(witnesses),
        'period_x':str(px),'period_y':str(py),'level':str(level),
        'atoms_outside_half_open_cell':0,'duplicate_locations_mod_period':0,
        'atoms_on_left_edge':sum(x==0 for x,y,w in atoms),
        'atoms_on_bottom_edge':sum(y==0 for x,y,w in atoms),
        'cell_mass':str(mass),'cell_area':str(px*py),
        'claimed_union_area':str(claimed_area),'recomputed_union_area':str(area),
        'union_area_decimal':decimal(area),'uncovered_cell_area':str(px*py-area),
        'claimed_ratio':str(claimed_ratio),'recomputed_ratio':str(ratio),
        'ratio_decimal':decimal(ratio),'ratio_minus_claim':str(ratio-target),
        'minimum_mass_slack':str(delta),'minimum_mass_slack_decimal':decimal(delta),
        'minimum_slack_witness_0based':slacks.index(delta),
        'minimum_radius':str(min(radii)),'maximum_radius':str(rmax),
        'maximum_radius_decimal':decimal(rmax),
        'minimum_containment_slack':str(minimum_containment),
        'periodic_copy_x_indices':[shift_x_min,shift_x_max],
        'periodic_copy_y_indices':[shift_y_min,shift_y_max],
        'witnesses_with_boundary_atoms':sum(row[2]>0 for row in rows),
        'rectangle_count_touching_cell_edge':sum(u==0 or v==px or s==0 or t==py for u,v,s,t in rectangles),
        'sweep':sweep,
        'finite':{
            'h':h,'N':n,'smear_radius':str(eps),'smear_radius_decimal':decimal(eps),
            'cell_margin_minus_Rmax':str(h*min(px,py)-rmax),
            'smear_cost_bound_over_delta':str(F(smear_cost_bound)/F(delta)),
            'minimum_smeared_mass_slack':str(min(smeared_slacks)),
            'norm':str(mass*n*n),'atom_count':len(atoms)*n*n,
            'inner_cells':(n-2*h)**2,'ratio':str(finite_ratio),
            'ratio_decimal':decimal(finite_ratio),
            'ratio_minus_claim':str(finite_ratio-target),
            'ratio_minus_claim_decimal':decimal(finite_ratio-target),
        },
        'runtime_seconds':time.monotonic()-started,
        'pid':os.getpid(),'nice':actual_nice,'priority_note':priority_note,
    }
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


# Exact integer helpers, equivalent on the rational/integer inputs here.
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

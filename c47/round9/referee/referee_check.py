"""Exact referee using its own checks of the supplied C47 data; standard library only.

No producer code is used. Box masses use integer ceil/floor bounds for every
base atom; the rectangle union uses the standard x sweep with a y segment tree.
All coordinates/masses are Fractions or integers on an exact common grid.
"""
import argparse
import hashlib
import json
import os
import resource
import time
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def common_grid(values):
    result = 1
    for value in values:
        denominator = value.denominator
        a, b = result, denominator
        while b:
            a, b = b, a % b
        result = result // a * denominator
    return result


def scaled(value, denominator):
    require(denominator % value.denominator == 0, 'inexact scaling')
    return value.numerator * (denominator // value.denominator)


def ceildiv(a, b):
    return -((-a) // b)


def decimal(value):
    with localcontext() as ctx:
        ctx.prec = 65
        return str(ctx.divide(Decimal(value.numerator), Decimal(value.denominator)))


def union_area(rectangles):
    """Integrate the covered y length between consecutive x endpoints."""
    scale = common_grid(v for rect in rectangles for v in rect)
    rects = [tuple(scaled(v, scale) for v in rect) for rect in rectangles]
    ys = sorted({v for u, v, s, t in rects for v in (s, t)})
    ranks = {v: i for i, v in enumerate(ys)}
    events = []
    for u, v, s, t in rects:
        events.append((u, 1, ranks[s], ranks[t]))
        events.append((v, -1, ranks[s], ranks[t]))
    events.sort()
    n = len(ys) - 1
    cover = [0] * (4 * n + 8)
    length = [0] * (4 * n + 8)

    def change(node, lo, hi, qlo, qhi, delta):
        if qlo <= lo and hi <= qhi:
            cover[node] += delta
            require(cover[node] >= 0, 'negative segment coverage')
        else:
            mid = (lo + hi) // 2
            if qlo < mid:
                change(2 * node, lo, mid, qlo, qhi, delta)
            if mid < qhi:
                change(2 * node + 1, mid, hi, qlo, qhi, delta)
        if cover[node]:
            length[node] = ys[hi] - ys[lo]
        elif hi - lo == 1:
            length[node] = 0
        else:
            length[node] = length[2 * node] + length[2 * node + 1]

    area = 0
    previous = events[0][0]
    for x, delta, lo, hi in events:
        area += (x - previous) * length[1]
        change(1, 0, n, lo, hi, delta)
        previous = x
    require(length[1] == 0 and all(c == 0 for c in cover), 'unclosed sweep')
    return F(area, scale * scale), {'grid_denominator': scale,
                                   'x_endpoints': len({e[0] for e in events}),
                                   'y_endpoints': len(ys)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', nargs='?', default='../certificates/final.json')
    parser.add_argument('finite_parameters', nargs='?', default='../producer_logs/final-finite.json')
    parser.add_argument('--out', default='../release_validation/referee-results.json')
    args = parser.parse_args()
    started = time.monotonic()
    print(f'PID {os.getpid()}: the referee’s own exact check starting', flush=True)
    raw = Path(args.certificate).read_bytes()
    data = json.loads(raw)
    finite = json.loads(Path(args.finite_parameters).read_text())
    digest = hashlib.sha256(raw).hexdigest()
    measure = data['measure']
    px, py, level = (F(measure[k]) for k in ('Px', 'Py', 'lam'))
    require(px > 0 and py > 0 and level == 1, 'periods or level')
    atoms = [tuple(map(F, p)) for p in measure['pts']]
    witnesses = [(tuple(map(F, w['box'])), F(w['radius']),
                  tuple(map(F, w['rectangle']))) for w in data['witnesses']]
    require(len(atoms) == 452 and len(witnesses) == 8443, 'artifact counts')
    for j, (x, y, m) in enumerate(atoms):
        require(0 <= x < px and 0 <= y < py and m > 0, f'atom {j}')
    require(len({(x, y) for x, y, m in atoms}) == len(atoms), 'duplicate atom')
    mass = sum((m for x, y, m in atoms), F(0))
    # These grids are inferred from the data, not a claimed producer grid.
    coord_grid = common_grid([px, py] + [v for x, y, m in atoms for v in (x, y)]
                             + [v for box, r, rect in witnesses for v in box])
    mass_grid = common_grid(m for x, y, m in atoms)
    ix, iy = scaled(px, coord_grid), scaled(py, coord_grid)
    int_atoms = [(scaled(x, coord_grid), scaled(y, coord_grid), scaled(m, mass_grid))
                 for x, y, m in atoms]
    eps = F(finite['smear_radius'])
    require(0 < eps <= F(1, 2), 'smear radius')
    slacks, smeared_slacks, masses = [], [], []
    radii = []
    shift_min = [0, 0]
    shift_max = [0, 0]
    support_min = [None, None]
    support_max = [None, None]
    containment_min = None
    copy_counts = []
    for index, (box, r, rect) in enumerate(witnesses):
        a, b, c, d = box
        u, v, s, t = rect
        require(a <= b and c <= d and r > 0, f'witness {index}: box/radius')
        require(0 <= u < v <= px and 0 <= s < t <= py,
                f'witness {index}: rectangle/cell')
        margins = [u - (b - r), a + r - v, s - (d - r), c + r - t]
        require(min(margins) >= 0, f'witness {index}: containment')
        containment_min = min(margins) if containment_min is None else min(containment_min, *margins)
        ai, bi, ci, di = (scaled(z, coord_grid) for z in box)
        mass_units = 0
        copies = 0
        for x, y, m in int_atoms:
            # Closed boxes: equality at either boundary is included.
            k0, k1 = ceildiv(ai - x, ix), (bi - x) // ix
            l0, l1 = ceildiv(ci - y, iy), (di - y) // iy
            if k0 <= k1 and l0 <= l1:
                count = (k1 - k0 + 1) * (l1 - l0 + 1)
                copies += count
                mass_units += m * count
                for axis, low, high, p, period in ((0, k0, k1, x, ix), (1, l0, l1, y, iy)):
                    shift_min[axis] = min(shift_min[axis], low)
                    shift_max[axis] = max(shift_max[axis], high)
                    lowpos, highpos = p + low * period, p + high * period
                    support_min[axis] = lowpos if support_min[axis] is None else min(support_min[axis], lowpos)
                    support_max[axis] = highpos if support_max[axis] is None else max(support_max[axis], highpos)
        enclosed = F(mass_units, mass_grid)
        slack = enclosed - 4 * level * r * r
        smeared = enclosed - 4 * level * (r + eps) ** 2
        require(slack > 0, f'witness {index}: insufficient mass')
        require(smeared > 0, f'witness {index}: smearing fails')
        slacks.append(slack)
        smeared_slacks.append(smeared)
        masses.append(enclosed)
        radii.append(r)
        copy_counts.append(copies)
        if (index + 1) % 2000 == 0:
            print(f'{index + 1}/{len(witnesses)} witnesses checked', flush=True)
    rmax = max(radii)
    delta = min(slacks)
    h, n = finite['boundary_cells'], finite['block_side_cells']
    require(type(h) is int and type(n) is int and h >= 0 and n > 2 * h, 'block integers')
    require(h * min(px, py) > rmax, 'insufficient boundary layers')
    require(4 * (2 * rmax + 1) * eps < delta, 'uniform smearing condition')
    # Also directly bound every participating periodic copy's cell index.
    require(all(h + a >= 0 for a in shift_min), 'lower truncation loses atom')
    require(all((n - h - 1) + b < n for b in shift_max), 'upper truncation loses atom')
    print('All witnesses passed; computing exact rectangle union', flush=True)
    area, sweep = union_area([rect for box, r, rect in witnesses])
    require(0 < area <= px * py, 'union area outside cell range')
    ratio = F(level * area) / F(mass)
    claimed = F('22878843460258009274861600625288681562329176839147945011303/13414024367090776613897918866165655414442557440000000000000')
    require(ratio == claimed, 'periodic ratio differs from claimed fraction')
    finite_ratio = ratio * F(n - 2 * h, n) ** 2
    target = F('1.7055913150')
    require(finite_ratio > target, 'finite ratio below decimal claim')
    require(F(finite['claim']) == target, 'finite claim mismatch')
    require(digest == finite['artifact_sha256'], 'finite parameters for different certificate')
    require(F(finite['maximum_witness_radius']) == rmax, 'maximum radius mismatch')
    require(F(finite['finite_function_L1_norm']) == n * n * mass, 'L1 norm mismatch')
    require(finite['finite_atom_count'] == n * n * len(atoms), 'finite count mismatch')
    require(F(finite['finite_ratio_lower_bound']) == finite_ratio, 'finite ratio mismatch')
    result = {
        'status': 'all exact checks passed', 'certificate_sha256': digest,
        'atoms_checked': len(atoms), 'witnesses_checked': len(witnesses),
        'Px': str(px), 'Py': str(py), 'level': str(level), 'cell_mass': str(mass),
        'cell_area': str(px * py), 'union_area': str(area), 'uncovered_area': str(px * py - area),
        'claimed_periodic_ratio': str(claimed), 'recomputed_periodic_ratio': str(ratio),
        'periodic_ratio_decimal': decimal(ratio), 'difference_from_claimed_ratio': str(ratio - claimed),
        'minimum_mass_slack': str(delta), 'minimum_slack_witness_zero_based': slacks.index(delta),
        'maximum_radius': str(rmax), 'maximum_radius_witness_zero_based': radii.index(rmax),
        'minimum_radius': str(min(radii)), 'minimum_containment_margin': str(containment_min),
        'minimum_smeared_mass_slack': str(min(smeared_slacks)),
        'periodic_copy_index_min': shift_min, 'periodic_copy_index_max': shift_max,
        'participating_support_min': [str(F(v, coord_grid)) for v in support_min],
        'participating_support_max': [str(F(v, coord_grid)) for v in support_max],
        'min_box_atom_copies': min(copy_counts), 'max_box_atom_copies': max(copy_counts),
        'outside_cell_atoms': 0, 'duplicate_atoms': 0,
        'atoms_on_left_or_bottom': sum(x == 0 or y == 0 for x, y, m in atoms),
        'radius_denominators_divide_D': all(data['D'] % r.denominator == 0 for r in radii),
        'coordinate_grid_denominator': coord_grid, 'mass_grid_denominator': mass_grid,
        'sweep': sweep, 'boundary_cells': h, 'block_side_cells': n, 'smear_radius': str(eps),
        'uniform_smearing_margin': str(delta - 4 * (2 * rmax + 1) * eps),
        'boundary_radius_margin': str(h * min(px, py) - rmax),
        'finite_function_L1_norm': str(n * n * mass), 'finite_atom_count': n * n * len(atoms),
        'finite_ratio_lower_bound': str(finite_ratio), 'finite_ratio_decimal': decimal(finite_ratio),
        'finite_margin_above_target': str(finite_ratio - target),
        'finite_margin_decimal': decimal(finite_ratio - target),
        'periodic_margin_above_target': str(ratio - target),
        'periodic_ten_decimal_floor': (ratio * 10 ** 10).__floor__(),
        'finite_ten_decimal_floor': (finite_ratio * 10 ** 10).__floor__(),
        'elapsed_seconds': time.monotonic() - started,
        'peak_rss_bytes_macos': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'pid': os.getpid(),
    }
    Path(args.out).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()

"""Clean-room C47 check, using only stdlib exact rational/integer arithmetic.

No producer or prior-referee code is imported. All noninteger input numbers
are parsed as Fraction. Integer scaling is an exact change of units.
"""
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
# Exact integer lcm, equivalent to math.lcm on the positive denominators here.
def lcm(*values):
    result = 1
    for value in values:
        a, b = result, value
        while b:
            a, b = b, a % b
        result = result // a * value
    return result

from pathlib import Path
import hashlib
import json
import os
import time


def denominator(values):
    return lcm(*(v.denominator for v in values))


def integer(v, scale):
    w = v * scale
    assert w.denominator == 1
    return w.numerator


def ceil_div(a, b):
    assert b > 0
    return -((-a) // b)


def decimal(q):
    with localcontext() as c:
        c.prec = 85
        return str(c.divide(Decimal(q.numerator), Decimal(q.denominator)))


def union_area(rectangles):
    """Sweep x slabs, independently merge the active y intervals each time."""
    scale = denominator(v for rect in rectangles for v in rect)
    events = defaultdict(list)
    for index, rect in enumerate(rectangles):
        left, right, bottom, top = [integer(v, scale) for v in rect]
        events[left].append((index, (bottom, top)))
        events[right].append((index, None))
    active = {}
    area = 0
    previous_x = min(events)
    slab_count = 0
    for x in sorted(events):
        intervals = sorted(active.values())
        height = 0
        if intervals:
            low, high = intervals[0]
            for bottom, top in intervals[1:]:
                if bottom > high:
                    height += high - low
                    low, high = bottom, top
                else:
                    high = max(high, top)
            height += high - low
        area += (x - previous_x) * height
        slab_count += x > previous_x
        for index, interval in events[x]:
            if interval is None:
                del active[index]
            else:
                active[index] = interval
        previous_x = x
    assert not active
    return F(area, scale * scale), slab_count, scale


def main():
    started = time.monotonic()
    source = Path('../certificates/final.json')
    finite_source = Path('../producer_logs/final-finite.json')
    raw = source.read_bytes()
    data = json.loads(raw, parse_float=F)
    finite = json.loads(finite_source.read_text(), parse_float=F)
    measure = data['measure']
    px, py, level = (F(measure[k]) for k in ('Px', 'Py', 'lam'))
    assert px > 0 and py > 0 and level == 1
    atoms = [tuple(map(F, p)) for p in measure['pts']]
    assert len(atoms) == 454
    assert all(0 <= x < px and 0 <= y < py and m > 0 for x, y, m in atoms)
    assert len({(x, y) for x, y, m in atoms}) == len(atoms)
    witnesses = [(tuple(map(F, w['box'])), F(w['radius']),
                  tuple(map(F, w['rectangle']))) for w in data['witnesses']]
    assert len(witnesses) == 6920
    box_lines = [i for i, line in enumerate(raw.decode().splitlines(), 1)
                 if '"box":' in line]
    assert len(box_lines) == len(witnesses)
    coordinate_scale = denominator([px, py] +
        [v for x, y, m in atoms for v in (x, y)] +
        [v for box, r, rect in witnesses for v in box])
    mass_scale = denominator(m for x, y, m in atoms)
    ipx, ipy = integer(px, coordinate_scale), integer(py, coordinate_scale)
    integer_atoms = [(integer(x, coordinate_scale), integer(y, coordinate_scale),
                      integer(m, mass_scale)) for x, y, m in atoms]
    epsilon = F(finite['smear_radius'])
    assert 0 < epsilon <= F(1, 2)
    h, n = finite['boundary_cells'], finite['block_side_cells']
    assert type(h) is int and type(n) is int and n > 2 * h >= 0
    details = []
    rectangles = []
    min_slack = None
    min_smeared_slack = None
    radius_max = F(0)
    shift_min_x = shift_min_y = 0
    shift_max_x = shift_max_y = 0
    boundary_incidences = 0
    print('pid', os.getpid(), 'nice', os.getpriority(os.PRIO_PROCESS, 0), flush=True)
    for index, (box, radius, rect) in enumerate(witnesses):
        a, b, c, d = box
        u, v, s, t = rect
        assert a <= b and c <= d and radius > 0, index
        assert 0 <= u < v <= px and 0 <= s < t <= py, index
        # All four extrema of B are within radius of every centre in R.
        assert max(v - a, b - u, t - c, d - s) <= radius, index
        ia, ib, ic, id_ = [integer(z, coordinate_scale) for z in box]
        mass_int = 0
        copies = 0
        for x, y, weight in integer_atoms:
            k0, k1 = ceil_div(ia - x, ipx), (ib - x) // ipx
            l0, l1 = ceil_div(ic - y, ipy), (id_ - y) // ipy
            nx, ny = max(0, k1 - k0 + 1), max(0, l1 - l0 + 1)
            mass_int += weight * nx * ny
            copies += nx * ny
            if nx and ny:
                shift_min_x, shift_max_x = min(shift_min_x, k0), max(shift_max_x, k1)
                shift_min_y, shift_max_y = min(shift_min_y, l0), max(shift_max_y, l1)
                assert -h <= k0 <= k1 <= h and -h <= l0 <= l1 <= h, index
                boundary_incidences += int((ia-x) % ipx == 0 or (ib-x) % ipx == 0
                                            or (ic-y) % ipy == 0 or (id_-y) % ipy == 0)
        mass = F(mass_int, mass_scale)
        slack = mass - 4 * level * radius**2
        smeared_slack = mass - 4 * level * (radius + epsilon)**2
        assert slack > 0 and smeared_slack > 0, index
        if min_slack is None or slack < min_slack:
            min_slack, min_slack_index = slack, index
        if min_smeared_slack is None or smeared_slack < min_smeared_slack:
            min_smeared_slack = smeared_slack
        radius_max = max(radius_max, radius)
        rectangles.append(rect)
        details.append({'index_zero_based': index, 'source_box_line': box_lines[index],
                        'periodic_atom_copies': copies, 'mass': str(mass),
                        'slack': str(slack), 'smeared_slack': str(smeared_slack)})
        if (index + 1) % 1000 == 0:
            print('witnesses', index + 1, 'seconds', time.monotonic() - started, flush=True)
    area, slabs, area_scale = union_area(rectangles)
    cell_mass = sum(m for x, y, m in atoms)
    ratio = F(level * area) / F(cell_mass)
    claimed = F('11436840446775366245825984602005252649658962678483718696299/6706834195253218266545949032739264680888893440000000000000')
    claimed_area = F('11436840446775366245825984602005252649658962678483718696299/1267650600228229401496703205376000000000000000000000000000')
    assert ratio == claimed and area == claimed_area and 0 < area <= px * py
    assert cell_mass == F('529075929443469/100000000000000')
    assert min_slack == F('1851161072028377713189111/32451855365842672678315602057625600000000000000')
    assert h * min(px, py) > radius_max
    smear_cost_bound = 4 * level * (2 * radius_max + 1) * epsilon
    assert smear_cost_bound < min_slack
    finite_ratio = ratio * F(n - 2 * h, n)**2
    finite_norm = n**2 * cell_mass
    target = F('1.7052517050')
    assert finite_ratio > target and ratio > target
    assert F(finite['claim']) == target
    assert F(finite['maximum_witness_radius']) == radius_max
    assert F(finite['finite_function_L1_norm']) == finite_norm
    assert F(finite['finite_ratio_lower_bound']) == finite_ratio
    assert finite['finite_atom_count'] == n**2 * len(atoms)
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == finite['artifact_sha256']
    assert target == F((ratio * 10**10).__floor__(), 10**10)
    result = {
        'status': 'all exact checks passed', 'certificate_sha256': digest,
        'atoms': len(atoms), 'witnesses': len(witnesses),
        'Px': str(px), 'Py': str(py), 'level': str(level),
        'outside_cell_atoms': 0, 'duplicate_support_points_mod_period': 0,
        'atoms_on_left_boundary': sum(x == 0 for x, y, m in atoms),
        'atoms_on_bottom_boundary': sum(y == 0 for x, y, m in atoms),
        'rectangles_touching_cell_boundary': sum(u == 0 or v == px or s == 0 or t == py for u, v, s, t in rectangles),
        'box_boundary_atom_incidences': boundary_incidences,
        'cell_mass': str(cell_mass), 'cell_area': str(px * py),
        'union_area': str(area), 'claimed_union_area': str(claimed_area),
        'area_difference': str(area - claimed_area), 'uncovered_area': str(px * py - area),
        'ratio': str(ratio), 'claimed_ratio': str(claimed),
        'ratio_difference': str(ratio - claimed), 'ratio_decimal': decimal(ratio),
        'margin_over_target': str(ratio - target), 'margin_over_target_decimal': decimal(ratio - target),
        'minimum_slack': str(min_slack), 'minimum_slack_witness_index': min_slack_index,
        'minimum_slack_source_box_line': box_lines[min_slack_index],
        'maximum_radius': str(radius_max), 'h': h, 'N': n,
        'periodic_shift_ranges': {'x': [shift_min_x, shift_max_x], 'y': [shift_min_y, shift_max_y]},
        'smear_radius': str(epsilon), 'smear_cost_bound': str(smear_cost_bound),
        'minimum_smeared_slack': str(min_smeared_slack),
        'finite_atom_count': n**2 * len(atoms), 'finite_norm': str(finite_norm),
        'finite_ratio': str(finite_ratio), 'finite_ratio_decimal': decimal(finite_ratio),
        'finite_margin': str(finite_ratio - target), 'finite_margin_decimal': decimal(finite_ratio - target),
        'coordinate_scale': coordinate_scale, 'mass_scale': mass_scale,
        'union_coordinate_scale': area_scale, 'union_slabs': slabs,
        'elapsed_seconds': time.monotonic() - started, 'pid': os.getpid(),
        'nice': os.getpriority(os.PRIO_PROCESS, 0)
    }
    Path('../release_validation/witness_checks.json').write_text(json.dumps(details, indent=2) + '\n')
    Path('../release_validation/referee-results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

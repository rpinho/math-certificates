#!/usr/bin/env python3
"""C47 certificate check using the referee’s own checks; standard library, exact rational arithmetic.
Written in this job from the operator definition and elementary box geometry.
No imported producer or prior-referee code. Run from this directory.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
# Integer ceiling and floor of rational values; equivalent to math.ceil/floor.
def ceil(value):
    return -((-value.numerator) // value.denominator)

def floor(value):
    return value.numerator // value.denominator

# Exact integer lcm, equivalent to math.lcm on these positive denominators.
def lcm(*values):
    result = 1
    for value in values:
        a, b = result, value
        while b:
            a, b = b, a % b
        result = result // a * value
    return result

import hashlib
import json
import os
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decimal(q):
    with localcontext() as ctx:
        ctx.prec = 85
        return str(ctx.divide(Decimal(q.numerator), Decimal(q.denominator)))


def union_area(rectangles):
    """Sweep x; a segment tree stores covered y-length with multiplicities.
    Scaling rationals to integers is lossless. Between adjacent event x values
    the active y union is constant. Shared edges have zero two-dimensional area.
    """
    scale = lcm(*(z.denominator for rect in rectangles for z in rect))
    rects = [tuple(int(z * scale) for z in rect) for rect in rectangles]
    ys = sorted({z for _, _, s, t in rects for z in (s, t)})
    index = {y: i for i, y in enumerate(ys)}
    segments = len(ys) - 1
    cover = [0] * (4 * segments)
    length = [0] * (4 * segments)

    def update(node, lo, hi, a, b, increment):
        if a <= lo and hi <= b:
            cover[node] += increment
            require(cover[node] >= 0, 'negative segment multiplicity')
        else:
            mid = (lo + hi) // 2
            if a < mid:
                update(2 * node, lo, mid, a, b, increment)
            if b > mid:
                update(2 * node + 1, mid, hi, a, b, increment)
        if cover[node]:
            length[node] = ys[hi] - ys[lo]
        elif hi - lo == 1:
            length[node] = 0
        else:
            length[node] = length[2 * node] + length[2 * node + 1]

    events = []
    for u, v, s, t in rects:
        events.extend([(u, 1, index[s], index[t]), (v, -1, index[s], index[t])])
    events.sort()
    area = 0
    previous = events[0][0]
    for x, increment, a, b in events:
        area += (x - previous) * length[1]
        update(1, 0, segments, a, b, increment)
        previous = x
    require(length[1] == 0 and not any(cover), 'sweep did not close')
    return F(area, scale * scale), scale, len({e[0] for e in events}) - 1


def main():
    started = time.monotonic()
    print(f'PID={os.getpid()} nice={os.getpriority(os.PRIO_PROCESS, 0)}', flush=True)
    source = Path('../certificates/final.json')
    raw = source.read_bytes()
    data = json.loads(raw)
    finite = json.loads(Path('../producer_logs/final-finite.json').read_text())
    m = data['measure']
    px, py, level = (F(m[k]) for k in ('Px', 'Py', 'lam'))
    require(px > 0 and py > 0 and level == 1, 'periods or level')
    atoms = [tuple(F(v) for v in point) for point in m['pts']]
    require(len(atoms) == 440, 'atom count')
    require(all(0 <= x < px and 0 <= y < py and w > 0 for x, y, w in atoms),
            'atom outside half-open cell or nonpositive mass')
    require(len({(x, y) for x, y, _ in atoms}) == len(atoms), 'duplicate support')
    mass = sum((w for _, _, w in atoms), F(0))
    witnesses = data['witnesses']
    require(len(witnesses) == 7806, 'witness count')
    source_lines = [i for i, line in enumerate(raw.decode().splitlines(), 1) if '"box":' in line]
    require(len(source_lines) == len(witnesses), 'witness source-line mapping')
    epsilon = F(finite['smear_radius'])
    h, n = finite['boundary_cells'], finite['block_side_cells']
    require(isinstance(h, int) and isinstance(n, int) and h > 0 and n > 2 * h,
            'finite block parameters')
    require(0 < epsilon <= F(1, 2), 'smear radius')
    all_rectangles, records = [], []
    min_slack = None
    max_radius = F(0)
    xmin = ymin = 0
    xmax = ymax = 0
    boundary_incidences = 0
    edge_rectangles = 0
    total_copies = 0
    for i, witness in enumerate(witnesses):
        a, b, c, d = map(F, witness['box'])
        r = F(witness['radius'])
        u, v, s, t = map(F, witness['rectangle'])
        where = f'witness {i}, certificate line {source_lines[i]}'
        require(a <= b and c <= d and r > 0, where + ': box/radius')
        require(0 <= u < v <= px and 0 <= s < t <= py, where + ': rectangle/cell')
        # Extreme coordinates suffice for B subset Q(z,r), for every z in R.
        require(v - a <= r and b - u <= r and t - c <= r and d - s <= r,
                where + ': containment')
        box_mass = F(0)
        copies = 0
        for x, y, weight in atoms:
            left, right = F(a - x) / F(px), F(b - x) / F(px)
            bottom, top = F(c - y) / F(py), F(d - y) / F(py)
            kl, kh, ll, lh = ceil(left), floor(right), ceil(bottom), floor(top)
            if kl > kh or ll > lh:
                continue
            multiplicity = (kh - kl + 1) * (lh - ll + 1)
            box_mass += weight * multiplicity
            copies += multiplicity
            xmin, xmax = min(xmin, kl), max(xmax, kh)
            ymin, ymax = min(ymin, ll), max(ymax, lh)
            # For any inner-cell offset h<=k,l<N-h all atom copies stay retained.
            require(-h <= kl <= kh <= h and -h <= ll <= lh <= h,
                    where + ': atom outside retained finite block')
            boundary_incidences += any(q.denominator == 1 for q in (left, right, bottom, top))
        slack = box_mass - 4 * level * r * r
        smeared_slack = box_mass - 4 * level * (r + epsilon) ** 2
        require(slack > 0, where + ': strict mass inequality')
        require(smeared_slack > 0, where + ': strict smeared inequality')
        if min_slack is None or slack < min_slack:
            min_slack, min_index = slack, i
        max_radius = max(max_radius, r)
        total_copies += copies
        edge_rectangles += u == 0 or v == px or s == 0 or t == py
        all_rectangles.append((u, v, s, t))
        records.append({'index': i, 'certificate_line': source_lines[i],
                        'box_mass': str(box_mass), 'atom_copies': copies,
                        'mass_slack': str(slack), 'smeared_slack': str(smeared_slack)})
        if (i + 1) % 1000 == 0:
            print(f'checked {i+1}/{len(witnesses)} witnesses', flush=True)
    area, scale, slabs = union_area(all_rectangles)
    require(0 < area <= px * py, 'union area range')
    ratio = F(level * area) / F(mass)
    claimed_ratio = F('114388018195906255044427129545533845966664904690010061034899/67069990589546886330812144279013633721316147200000000000000')
    claimed_area = F('114388018195906255044427129545533845966664904690010061034899/12676506002282294014967032053760000000000000000000000000000')
    require(ratio == claimed_ratio and area == claimed_area, 'claimed ratio or area mismatch')
    require(mass == F('529088934896347/100000000000000'), 'claimed cell mass')
    require(min_slack == F('648464387435490448162039/519229685853482762853049632922009600000000000000'), 'claimed minimum slack')
    require(h * min(px, py) > max_radius, 'geometric finite boundary condition')
    smear_cost_bound = 4 * level * (2 * max_radius + 1) * epsilon
    require(smear_cost_bound < min_slack, 'uniform smearing inequality')
    finite_ratio = ratio * F(n - 2 * h, n) ** 2
    target = F('1.7055022252')
    finite_norm = n * n * mass
    atom_count = n * n * len(atoms)
    require(F(finite['claim']) == target and finite_ratio > target, 'finite target')
    require(F(finite['finite_ratio_lower_bound']) == finite_ratio, 'finite ratio mismatch')
    require(F(finite['finite_function_L1_norm']) == finite_norm, 'finite norm mismatch')
    require(finite['finite_atom_count'] == atom_count, 'finite count mismatch')
    require(F(finite['maximum_witness_radius']) == max_radius, 'maximum radius mismatch')
    digest = hashlib.sha256(raw).hexdigest()
    require(finite['artifact_sha256'] == digest, 'finite certificate identity')
    require(floor(ratio * 10**10) == target * 10**10, 'decimal is not downward truncation')
    result = {
        'certificate': str(source), 'sha256': digest, 'atoms': len(atoms), 'witnesses': len(witnesses),
        'Px': str(px), 'Py': str(py), 'level': str(level), 'cell_mass': str(mass),
        'union_area': str(area), 'claimed_union_area': str(claimed_area), 'area_difference': str(area-claimed_area),
        'ratio': str(ratio), 'claimed_ratio': str(claimed_ratio), 'ratio_difference': str(ratio-claimed_ratio),
        'ratio_decimal': decimal(ratio), 'uncovered_cell_area': str(px*py-area),
        'minimum_mass_slack': str(min_slack), 'minimum_slack_witness': min_index,
        'minimum_slack_source_line': source_lines[min_index], 'maximum_radius': str(max_radius),
        'rectangle_coordinate_scale': scale, 'sweep_slabs': slabs,
        'atom_cell_offsets': [[xmin,xmax],[ymin,ymax]], 'atom_copy_incidences': total_copies,
        'box_boundary_atom_witness_incidences': boundary_incidences,
        'cell_edge_rectangles': edge_rectangles,
        'base_atoms_on_included_cell_boundary': sum(x == 0 or y == 0 for x,y,_ in atoms),
        'outside_cell_atoms': 0, 'duplicate_supports': 0,
        'h': h, 'N': n, 'epsilon': str(epsilon),
        'uniform_smear_cost_bound': str(smear_cost_bound), 'smear_cost_over_slack': str(F(smear_cost_bound)/F(min_slack)),
        'finite_norm': str(finite_norm), 'finite_atom_count': atom_count,
        'finite_ratio': str(finite_ratio), 'finite_ratio_decimal': decimal(finite_ratio),
        'target': str(target), 'finite_margin': str(finite_ratio-target),
        'finite_margin_decimal': decimal(finite_ratio-target),
        'periodic_margin': str(ratio-target), 'periodic_margin_decimal': decimal(ratio-target),
        'all_exact_checks': 'PASS', 'elapsed_seconds': time.monotonic()-started
    }
    Path('../release_validation/witness_results.json').write_text(json.dumps(records, indent=2)+'\n')
    Path('../release_validation/referee-results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()

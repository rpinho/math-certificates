"""Direct rational verification of the supplied C47 data; standard library only.

No producer/checker module is imported. Geometry is for closed l_infinity balls.
All mathematical decisions use integers and Fraction. Decimal is display only.
"""
import csv
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def decimal(x):
    with localcontext() as ctx:
        ctx.prec = 75
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def union_area(rectangles):
    """Partition into vertical slabs; merge all active y intervals in each."""
    xs = sorted({x for u, v, s, t in rectangles for x in (u, v)})
    area = F(0)
    for left, right in zip(xs, xs[1:]):
        intervals = sorted((s, t) for u, v, s, t in rectangles
                           if u <= left and right <= v)
        length = F(0)
        end = None
        for low, high in intervals:
            if end is None or low > end:
                length += high - low
                end = high
            elif high > end:
                length += high - end
                end = high
        area += (right - left) * length
    return area, len(xs) - 1


def main():
    raw = (ROOT / 'sources/final.json').read_bytes()
    certificate = json.loads(raw)
    finite = json.loads((ROOT / 'sources/final-finite.json').read_text())
    m = certificate['measure']
    px, py, level = map(F, (m['Px'], m['Py'], m['lam']))
    assert px > 0 and py > 0 and level == 1
    atoms = [tuple(map(F, p)) for p in m['pts']]
    assert len(atoms) == 98
    assert all(0 <= x < px and 0 <= y < py and mass > 0
               for x, y, mass in atoms)
    assert len({(x, y) for x, y, mass in atoms}) == len(atoms)
    cell_mass = sum((mass for x, y, mass in atoms), F(0))
    closed_mass = sum((mass * (2 if x == 0 else 1) * (2 if y == 0 else 1)
                       for x, y, mass in atoms), F(0))
    eps = F(finite['smear_radius'])
    h, n = finite['boundary_cells'], finite['block_side_cells']
    assert isinstance(h, int) and isinstance(n, int) and n > 2*h >= 0
    assert 0 < eps <= F(1, 2)
    rectangles, radii, slacks, smear_slacks, rows = [], [], [], [], []
    offsets = set()
    lines = [i for i, line in enumerate(raw.decode().splitlines(), 1)
             if '"box":' in line]
    assert len(certificate['witnesses']) == len(lines) == 1500
    for index, witness in enumerate(certificate['witnesses']):
        a, b, c, d = map(F, witness['box'])
        u, v, s, t = map(F, witness['rectangle'])
        r = F(witness['radius'])
        assert a <= b and c <= d and r > 0, index
        assert 0 <= u < v <= px and 0 <= s < t <= py, index
        # Maximum coordinate distance over the Cartesian product B x R.
        gap = max(abs(xx-cc) for ends, centers in
                  (((a, b), (u, v)), ((c, d), (s, t)))
                  for xx in ends for cc in centers)
        assert gap <= r, index
        mass = F(0)
        selected = []
        for j, (x, y, weight) in enumerate(atoms):
            k0, k1 = ceil((a-x)/px), floor((b-x)/px)
            l0, l1 = ceil((c-y)/py), floor((d-y)/py)
            for k in range(k0, k1+1):
                for l in range(l0, l1+1):
                    xx, yy = x+k*px, y+l*py
                    assert a <= xx <= b and c <= yy <= d
                    assert max(abs(xx-u), abs(xx-v), abs(yy-s), abs(yy-t)) <= r
                    # For every inner cell i in [h, n-h-1], i+k is retained.
                    assert h+k >= 0 and n-h-1+k < n
                    assert h+l >= 0 and n-h-1+l < n
                    selected.append((j, k, l))
                    offsets.add((k, l))
                    mass += weight
        assert len(selected) == len(set(selected)) and selected, index
        slack = mass - 4*level*r*r
        smeared = mass - 4*level*(r+eps)**2
        assert slack > 0 and smeared > 0, index
        assert (r*certificate['D']).denominator == 1
        rectangles.append((u, v, s, t))
        radii.append(r)
        slacks.append(slack)
        smear_slacks.append(smeared)
        rows.append((index, lines[index], len(selected), str(mass), str(r),
                     str(slack), str(smeared), min(k for j,k,l in selected),
                     max(k for j,k,l in selected), min(l for j,k,l in selected),
                     max(l for j,k,l in selected)))
    print('All 1500 witness masses, radii, containments and smearing inequalities hold.', flush=True)
    area, slabs = union_area(rectangles)
    assert 0 < area <= px*py
    claimed = F('1771220457083239070854869084751983500209800598673/1039431510074799032049552767561236480000000000000')
    ratio = level * area / cell_mass
    assert ratio == claimed
    rmax, delta = max(radii), min(slacks)
    assert h*min(px, py) > rmax
    common_slack = delta - 4*level*(2*rmax+1)*eps
    assert common_slack > 0
    target = F('1.7040280575')
    finite_ratio = ratio * F(n-2*h, n)**2
    digest = hashlib.sha256(raw).hexdigest()
    assert finite['artifact_sha256'] == digest
    assert F(finite['claim']) == target
    assert F(finite['maximum_witness_radius']) == rmax
    assert F(finite['finite_function_L1_norm']) == n*n*cell_mass
    assert finite['finite_atom_count'] == len(atoms)*n*n
    assert F(finite['finite_ratio_lower_bound']) == finite_ratio
    assert finite_ratio > target
    assert target == F(floor(ratio*10**10), 10**10)
    result = dict(
        certificate_sha256=digest, atoms=len(atoms), witnesses=len(rows),
        periods=[str(px),str(py)], level=str(level),
        min_atom_mass=str(min(mass for x,y,mass in atoms)),
        atoms_on_left_or_bottom=[j for j,(x,y,mass) in enumerate(atoms) if x==0 or y==0],
        cell_mass=str(cell_mass), closed_cell_mass=str(closed_mass),
        distinct_atom_locations=len(atoms), atom_incidences=sum(row[2] for row in rows),
        offsets=sorted(offsets), vertical_slabs=slabs, area=str(area), area_decimal=decimal(area),
        uncovered_area=str(px*py-area),
        radius_min=str(min(radii)), radius_max=str(rmax),
        minimum_slack=str(delta), minimum_slack_index=slacks.index(delta),
        minimum_slack_source_line=lines[slacks.index(delta)],
        minimum_smeared_slack=str(min(smear_slacks)), common_smear_margin=str(common_slack),
        radius_boundary_margin=str(h*min(px,py)-rmax),
        claimed_ratio=str(claimed), recomputed_ratio=str(ratio), difference=str(ratio-claimed),
        ratio_decimal=decimal(ratio), decimal_claim=str(target),
        periodic_excess=str(ratio-target), periodic_excess_decimal=decimal(ratio-target),
        h=h, N=n, smear_radius=str(eps), smear_radius_decimal=decimal(eps),
        finite_atom_count=n*n*len(atoms), finite_L1=str(n*n*cell_mass),
        finite_ratio=str(finite_ratio), finite_ratio_decimal=decimal(finite_ratio),
        finite_excess=str(finite_ratio-target), finite_excess_decimal=decimal(finite_ratio-target),
        public_printed_bar='1.7032090736', excess_over_public_bar=str(ratio-F('1.7032090736')),
        all_exact_checks_passed=True)
    (ROOT/'exact_results.json').write_text(json.dumps(result, indent=2)+'\n')
    with (ROOT/'witness_results.tsv').open('w') as out:
        writer = csv.writer(out, delimiter='\t', lineterminator='\n')
        writer.writerow(('index','source_box_line','atom_count','mass','radius','slack',
                         'smeared_slack','k_min','k_max','l_min','l_max'))
        writer.writerows(rows)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

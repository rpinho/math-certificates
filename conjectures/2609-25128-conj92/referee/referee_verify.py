"""Exact independent replay of the sub-quorum referee checks. Python 3.10+."""
import os
import signal
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations


def require(condition, *evidence):
    if not condition:
        raise AssertionError(evidence)


def subsets(mask):
    """All submasks, including the whole mask and the empty mask."""
    part = mask
    while True:
        yield part
        if part == 0:
            return
        part = (part - 1) & mask


@lru_cache(maxsize=8192)
def vertices(mask):
    return tuple(i for i in range(mask.bit_length()) if mask & (1 << i))


@lru_cache(None)
def edges(n):
    return tuple(combinations(range(n), 2))


def graph(n, pairs):
    rows = [0] * n
    for i, j in pairs:
        require(0 <= i < n and 0 <= j < n and i != j, n, i, j)
        rows[i] |= 1 << j
        rows[j] |= 1 << i
    return tuple(rows)


def complement(rows):
    full = (1 << len(rows)) - 1
    return tuple(full ^ (1 << v) ^ row for v, row in enumerate(rows))


def graph_id(rows):
    return sum(1 << i for i, (u, v) in enumerate(edges(len(rows))) if rows[u] & (1 << v))


def decode(n, code):
    return graph(n, (edge for j, edge in enumerate(edges(n)) if code & (1 << j)))


def grid(h, w):
    return graph(h * w, ((a, b) for a, b in edges(h * w)
                         if abs(a // w - b // w) + abs(a % w - b % w) == 1))


def double_star():
    # x, y, a1, a2, b1, b2 in that order
    return graph(6, [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)])


def class_passes(closed, support, block):
    """TeX line 72, multiplied by two. The graph rows here already include self."""
    for v in vertices(block):
        neighborhood = closed[v] & support
        if 2 * (neighborhood & block).bit_count() < neighborhood.bit_count():
            return False
    return True


def closed_rows(rows):
    return tuple(row | (1 << v) for v, row in enumerate(rows))


def is_coloring(rows, labels, k):
    """Explicit partial map, None for an uncolored vertex, with an explicit codomain."""
    if len(labels) != len(rows) or k < 0:
        return False
    present = {c for c in labels if c is not None}
    if present != set(range(1, k + 1)):
        return False
    for v, c in enumerate(labels):
        if c is None:
            continue
        neighborhood = [labels[u] for u in range(len(rows))
                        if labels[u] is not None and (u == v or rows[v] & (1 << u))]
        if 2 * neighborhood.count(c) < len(neighborhood):
            return False
    return True


def partitions(mask):
    """Partition a support into nonempty classes, once up to renaming."""
    if not mask:
        yield ()
        return
    first = mask & -mask
    others = mask ^ first
    for extra in subsets(others):
        block = first | extra
        for rest in partitions(mask ^ block):
            yield (block,) + rest


def optimal_by_cover(rows):
    """For each support, maximize the number of blocks in a valid exact cover."""
    closed = closed_rows(rows)
    best = ()
    n = len(rows)
    for support in subsets((1 << n) - 1):
        if support.bit_count() <= len(best):
            continue
        choices = [[] for _ in rows]
        for block in subsets(support):
            if block and class_passes(closed, support, block):
                choices[vertices(block)[0]].append(block)

        @lru_cache(None)
        def visit(remaining):
            if not remaining:
                return ()
            answer = None
            for block in choices[vertices(remaining)[0]]:
                if block & remaining == block:
                    tail = visit(remaining ^ block)
                    if tail is not None and (answer is None or 1 + len(tail) > len(answer)):
                        answer = (block,) + tail
            return answer

        candidate = visit(support)
        visit.cache_clear()
        if candidate is not None and len(candidate) > len(best):
            best = candidate
    labels = [None] * n
    for c, block in enumerate(best, 1):
        for v in vertices(block):
            labels[v] = c
    require(is_coloring(rows, labels, len(best)), rows, labels)
    return len(best)


def beta(rows):
    return max(s.bit_count() for s in subsets((1 << len(rows)) - 1)
               if all((rows[v] & s).bit_count() <= 1 for v in vertices(s)))


def omega(rows):
    """TeX line 88. Enumerate all matchings; for each one enumerate all disjoint T."""
    n = len(rows)
    full = (1 << n) - 1

    def best(remaining, occupied, matches):
        if remaining:
            v = vertices(remaining)[0]
            unused = remaining ^ (1 << v)
            values = [best(unused, occupied, matches)]
            for u in vertices(rows[v] & unused):
                values.append(best(unused ^ (1 << u), occupied | (1 << v) | (1 << u),
                                   matches + 1))
            return max(values)
        return max(matches + t.bit_count() for t in subsets(full ^ occupied)
                   if all((rows[v] & (t | occupied)).bit_count() <= 1 for v in vertices(t)))

    return best(full, 0, 0)


def weight_vector(n, parts):
    weights = [Fraction(0)] * n
    for part in parts:
        for v in vertices(part):
            weights[v] = Fraction(1, part.bit_count())
    return weights


@lru_cache(None)
def reciprocal(d):
    return Fraction(1, 1 + d // 2)


def check_optimal(rows, support, parts):
    """Test both parts of Lemma 1 on every I in this optimal support."""
    w = weight_vector(len(rows), parts)
    require(all(0 <= x <= 1 for x in w) and sum(w) == len(parts), rows, parts)
    sizes = {v: part.bit_count() for part in parts for v in vertices(part)}
    checks = 0
    for intersection in subsets(support):
        for v in vertices(intersection):
            d = (rows[v] & intersection).bit_count()
            require(sizes[v] >= 1 + d // 2 and w[v] <= reciprocal(d),
                    rows, parts, intersection, v)
            checks += 1
    return checks


def isomorphism_rows(n, vals, betas):
    """Group labeled results by explicit relabeling to compare the producer's counts."""
    edge_list = edges(n)
    index = {e: j for j, e in enumerate(edge_list)}
    maps = [tuple(1 << index[tuple(sorted((p[a], p[b])))] for a, b in edge_list)
            for p in permutations(range(n))]
    seen = set()
    count = Counter()
    gaps = []
    full = (1 << len(edge_list)) - 1
    for code, k in enumerate(vals):
        if code in seen:
            continue
        on = vertices(code)
        orbit = {sum(p[j] for j in on) for p in maps}
        require(not orbit.intersection(seen), n, code)
        seen.update(orbit)
        other = full ^ code
        total = k + vals[other]
        gap = k > betas[code]
        if gap:
            gaps.append(code)
        for member in orbit:
            require((vals[member], betas[member]) == (k, betas[code]), n, code, member)
        count['graphs'] += 1
        count['equality'] += int(total == n + 2)
        count['gap_G'] += int(gap)
        count['equality_gap_G'] += int(total == n + 2 and gap)
        count['equality_gap_either'] += int(total == n + 2 and (gap or vals[other] > betas[other]))
    require(len(seen) == len(vals), n)
    return dict(count), gaps


def coloring_census(n):
    full = (1 << n) - 1
    patterns = [(s, p) for s in subsets(full) for p in partitions(s)]
    graphs = 1 << len(edges(n))
    vals, betas = [], []
    optimum_count = vertex_checks = 0
    valid_count = 0
    for code in range(graphs):
        rows = decode(n, code)
        closed = closed_rows(rows)
        k = -1
        optimal = []
        for s, parts in patterns:
            if all(class_passes(closed, s, block) for block in parts):
                valid_count += 1
                if len(parts) > k:
                    k = len(parts)
                    optimal = []
                if len(parts) == k:
                    optimal.append((s, parts))
        vals.append(k)
        betas.append(beta(rows))
        for s, parts in optimal:
            optimum_count += 1
            vertex_checks += check_optimal(rows, s, parts)
    totals = [k + vals[graphs - 1 - code] for code, k in enumerate(vals)]
    require(max(totals) <= n + 2, n, max(totals))
    grouped, gaps = isomorphism_rows(n, vals, betas)
    print('COLOR', n, 'labeled', graphs, 'partitions_tested', graphs * len(patterns),
          'valid', valid_count, 'optimal', optimum_count, 'subset_vertex_checks', vertex_checks,
          'sum_range', (min(totals), max(totals)), 'unlabeled', grouped, 'gap_reps', gaps,
          flush=True)
    if n == 6:
        require(vals[graph_id(double_star())] == 5 and betas[graph_id(double_star())] == 4,
                'double star')
    return grouped


def parity_bound(m):
    if m < 2:
        return Fraction(2 * m)
    if m % 2 == 0:
        return Fraction(m + 2)
    return m + 2 + Fraction(1, 1 + m // 2)


@lru_cache(maxsize=8192)
def checked_score(degrees):
    m = len(degrees)
    require(all(0 <= d < m for d in degrees), degrees)
    odd = sum(d % 2 for d in degrees)
    require(odd % 2 == 0, 'handshake', degrees)
    total = sum((reciprocal(d) + reciprocal(m - 1 - d) for d in degrees), Fraction(0))
    if m >= 2:
        r = m // 2
        if m % 2:
            require(odd <= 2 * r, degrees)
            intermediate = m + Fraction(odd, r) + Fraction(m - odd, r + 1)
        else:
            intermediate = Fraction(m + 2)
        require(total <= intermediate <= parity_bound(m), degrees, total, intermediate)
    require(total <= parity_bound(m) <= m + Fraction(5, 2), degrees, total)
    return total


def lemma_two():
    count = equal = 0
    for a in range(1, 32):
        for b in range(1, 32):
            for s in range(2, a + b + 1):
                left = Fraction(1, a) + Fraction(1, b)
                middle = 1 + Fraction(1, a + b - 1)
                right = 1 + Fraction(1, s - 1)
                require(left <= middle <= right, a, b, s)
                require((left == right) == (min(a, b) == 1 and a + b == s), a, b, s)
                count += 1
                equal += int(left == right)
    for m in range(2, 31):
        for d in range(m):
            a = 1 + d // 2
            b = 1 + (m - 1 - d) // 2
            target = m // 2 + 1 + int(m % 2 == 1 and d % 2 == 0)
            require(a + b == target, m, d)
            require(reciprocal(d) + reciprocal(m - 1 - d) <= 1 + Fraction(1, target - 1),
                    m, d)
    print('LEMMA2 triples', count, 'equalities', equal, flush=True)


def sigma_census(m):
    e = edges(m)
    count = 1 << len(e)
    full = (1 << m) - 1
    rows = [0] * m
    best = None
    maximizers = 0
    edge_layers = Counter()
    for i in range(count):
        if i:
            # Successive reflected Gray codes toggle exactly this edge.
            a, b = e[(i & -i).bit_length() - 1]
            rows[a] ^= 1 << b
            rows[b] ^= 1 << a
        degrees = tuple(row.bit_count() for row in rows)
        for v, row in enumerate(rows):
            require((full ^ (1 << v) ^ row).bit_count() + degrees[v] == m - 1, m, i, v)
        code = i ^ (i >> 1)
        require(sum(degrees) == 2 * code.bit_count(), m, code, degrees)
        edge_layers[code.bit_count()] += 1
        score = checked_score(tuple(sorted(degrees)))
        if best is None or score > best:
            best, maximizers, witness = score, 0, code
        maximizers += int(score == best)
    for j, multiplicity in edge_layers.items():
        binomial = 1
        for k in range(j):
            binomial = binomial * (len(e) - k) // (k + 1)
        require(multiplicity == binomial, m, j, multiplicity, binomial)
    require(len(edge_layers) == len(e) + 1 and sum(edge_layers.values()) == count,
            m, edge_layers)
    require(best == parity_bound(m), m, best)
    print('SIGMA', m, 'graphs', count, 'max', best, 'maximizers', maximizers,
          'first_edge_mask', witness, 'edge_counts_tested', len(edge_layers), flush=True)


class IntegerStream:
    def __init__(self, seed):
        self.state = seed

    def take(self, modulus):
        # xorshift64. All sampling, including decisions at prescribed densities, is integer.
        word = self.state
        mask = (1 << 64) - 1
        word ^= (word << 13) & mask
        word ^= word >> 7
        word ^= (word << 17) & mask
        self.state = word
        return word % modulus


def medium(m, stream):
    pairs = edges(m)
    empty = graph(m, [])
    counts = Counter()
    best = None
    hits = 0

    def test(rows, family):
        nonlocal best, hits
        ds = tuple(row.bit_count() for row in rows)
        score = checked_score(tuple(sorted(ds)))
        counts[family] += 1
        if best is None or score > best:
            best = score
            hits = 0
        hits += int(score == best)
        return score

    for k in range(m // 2 + 1):
        h = graph(m, [(2 * i, 2 * i + 1) for i in range(k)])
        for g in (h, complement(h)):
            score = test(g, 'matching')
            if k == m // 2:
                require(score == parity_bound(m), m, k, score)
    for k in range(m + 1):
        h = graph(m, [(i, j) for i in range(k) for j in range(k, m)])
        for g in (h, complement(h)):
            test(g, 'cut')
    for edge_order in (pairs, sorted(pairs, key=lambda e: (e[1], e[0]))):
        rows = list(empty)
        test(rows, 'prefix')
        for a, b in edge_order:
            rows[a] |= 1 << b
            rows[b] |= 1 << a
            test(rows, 'prefix')
    starts = [empty]
    for numerator in (1, 2, 4, 6, 7):
        for i in range(24):
            rows = graph(m, (e for e in pairs if stream.take(8) < numerator))
            test(rows, 'random')
            if i == 0:
                starts.append(rows)

    # Score every one-edge neighbor. Use endpoint deltas to pick a steepest
    # improvement, then reconstruct the moved graph and check its score afresh.
    term = [reciprocal(d) + reciprocal(m - 1 - d) for d in range(m)]
    limit = parity_bound(m)
    for start in starts:
        rows = list(start)
        for _ in range(64):
            old = test(rows, 'ascent_state')
            high = old
            move = None
            for a, b in pairs:
                step = -1 if rows[a] & (1 << b) else 1
                da = rows[a].bit_count()
                db = rows[b].bit_count()
                neighbor = old - term[da] - term[db] + term[da + step] + term[db + step]
                if neighbor > limit:
                    raise AssertionError((m, graph_id(rows), a, b, neighbor))
                counts['ascent_neighbor'] += 1
                if neighbor > high:
                    high, move = neighbor, (a, b)
            if move is None:
                break
            a, b = move
            rows[a] ^= 1 << b
            rows[b] ^= 1 << a
            require(test(rows, 'ascent_move') == high, m, move)
    print('MEDIUM', m, 'max', best, 'max_hits_scored_states', hits, 'evaluations', dict(counts),
          flush=True)


def benchmarks():
    for n in range(1, 9):
        empty = graph(n, [])
        values = optimal_by_cover(complement(empty)), optimal_by_cover(empty)
        require(values == (min(2, n), n), n, values)
        print('EXAMPLE K and empty', n, values)
    p4 = graph(4, [(0, 1), (1, 2), (2, 3)])
    c5 = graph(5, [(i, (i + 1) % 5) for i in range(5)])
    star = graph(5, [(0, i) for i in range(1, 5)])
    cube = graph(8, ((i, j) for i, j in edges(8) if (i ^ j).bit_count() == 1))
    for name, g, expected in [('P4', p4, (3, 3)), ('C5', c5, (3, 3)),
                              ('S22', double_star(), (5, 4)),
                              ('complement S22', complement(double_star()), (3, 3)),
                              ('K1,4', star, (4, 4)), ('Q3', cube, (4, 4)),
                              ('G3,3', grid(3, 3), (5, 5)), ('G3,4', grid(3, 4), (7, 7))]:
        actual = optimal_by_cover(g), beta(g)
        require(actual == expected, name, actual)
        print('EXAMPLE', name, 'vertices', len(g), 'edges', graph_id(g).bit_count(),
              'psi,beta', actual)
    require(is_coloring(cube, [1, None, None, 2, None, 3, 4, None], 4), 'Q3 figure')
    print('EXAMPLE Q3 figure even-weight support 0,3,5,6 accepted', flush=True)


def controls():
    p3 = graph(3, [(0, 1), (0, 2)])
    score = checked_score(tuple(sorted(row.bit_count() for row in p3)))
    require(score == Fraction(11, 2) > len(p3) + 2, 'tightened Sigma', score)
    empty = graph(6, [])
    om = omega(empty), omega(complement(empty))
    require(om == (6, 3) and sum(om) > 8, 'Omega', om)
    triangle = graph(3, edges(3))
    require(not is_coloring(triangle, [1, 2, 3], 3), 'invalid colored triangle')
    require(is_coloring(triangle, [1, 2, None], 2), 'uncolored neighbor, closed tie')
    require(is_coloring(p3, [1, None, None], 1), 'isolated in support')
    require(not is_coloring(graph(2, []), [1, 3], 3), 'not onto')
    require(is_coloring(graph(2, []), [None, None], 0), 'empty map')
    impossible = sum((reciprocal(1) + reciprocal(1) for _ in range(3)), Fraction(0))
    require(impossible == 6 > parity_bound(3), 'nongraphical all-odd sequence')
    p4 = graph(4, [(0, 1), (1, 2), (2, 3)])
    good, bad = (1, 1, 2, 2), (1, 2, 1, 2)
    require(is_coloring(p4, good, 2) and not is_coloring(p4, bad, 2), 'P4 pair')
    for labels in (good, bad):
        for v, c in enumerate(labels):
            for sub in subsets(15):
                if sub & (1 << v):
                    require(labels.count(c) >= 1 + (p4[v] & sub).bit_count() // 2, labels, sub)
    paths = graph(6, [(0, 1), (0, 2), (3, 4), (3, 5)])
    relaxed = (1, 2, 3, 1, 4, 5)
    require(all(relaxed.count(c) >= 1 + paths[v].bit_count() // 2
                for v, c in enumerate(relaxed)), 'two paths relaxed coloring')
    require(not is_coloring(paths, relaxed, 5) and optimal_by_cover(paths) == 4,
            'two paths true optimum')
    print('CONTROLS two disjoint P3s: size-only constraints allow 5, true optimum 4')
    h = double_star()
    labels1 = [1, 1, 2, 3, 4, 5]
    labels2 = [1, None, 2, 3, None, None]
    require(is_coloring(h, labels1, 5) and is_coloring(complement(h), labels2, 3), 'S22 maps')
    inside = [v for v in range(6) if labels1[v] is not None and labels2[v] is not None]
    local_d = tuple(sum(int(bool(h[v] & (1 << u))) for u in inside) for v in inside)
    weights = [Fraction(1, labels1.count(c)) +
               (Fraction(0) if d is None else Fraction(1, labels2.count(d)))
               for c, d in zip(labels1, labels2)]
    inside_sum = sum(weights[v] for v in inside)
    outside_sum = sum(weights[v] for v in range(6) if v not in inside)
    require(local_d == (2, 1, 1) and checked_score(tuple(sorted(local_d))) == inside_sum == score,
            'S22 induced sum', local_d, weights)
    require(outside_sum == Fraction(5, 2) and inside_sum + outside_sum == 8, weights)
    print('CONTROLS P3 Sigma', score, '> 5; Omega(empty6),Omega(K6)', om, 'sum 9 > 8')
    print('CONTROLS triangle 3 private rejected, 2 private + uncolored accepted; '
          'isolated in support accepted; non-onto rejected; empty onto accepted')
    print('CONTROLS degree sequence (1,1,1) gives', impossible, 'with odd degree sum')
    print('CONTROLS P4 same class sizes, weights and subset bounds: 1122 accepted, 1212 rejected')
    print('WITNESS S22 overlap', inside, 'degrees', local_d, 'weights', tuple(map(str, weights)),
          'inside', inside_sum, 'outside', outside_sum, flush=True)


def canonical(rows):
    """Canonical edge mask by equitable refinement and individualization."""
    n = len(rows)
    full = (1 << n) - 1

    def search(cells):
        while True:
            refined = []
            for cell in cells:
                if cell & (cell - 1) == 0:
                    refined.append(cell)
                    continue
                groups = {}
                for v in vertices(cell):
                    signature = tuple((rows[v] & block).bit_count() for block in cells)
                    groups[signature] = groups.get(signature, 0) | (1 << v)
                refined.extend(groups[k] for k in sorted(groups))
            if len(refined) == len(cells):
                break
            cells = refined
        if len(cells) == n:
            order = [x.bit_length() - 1 for x in cells]
            return sum(1 << j for j, (u, v) in enumerate(edges(n))
                       if rows[order[u]] & (1 << order[v]))
        _, i = min((c.bit_count(), i) for i, c in enumerate(cells) if c & (c - 1))
        cell = cells[i]
        representatives = []
        for v in vertices(cell):
            # Vertices interchangeable by the transposition (u v) give isomorphic branches.
            if all((rows[v] ^ rows[u]) & ~(1 << u | 1 << v) for u in representatives):
                representatives.append(v)
        if len(representatives) == 1:
            singletons = [1 << v for v in vertices(cell)]
            return search(cells[:i] + singletons + cells[i + 1:])
        return min(search(cells[:i] + [1 << v, cell ^ (1 << v)] + cells[i + 1:])
                   for v in representatives)

    return search([full]) if n else 0


def total_colors(rows):
    full = (1 << len(rows)) - 1
    closed = closed_rows(rows)
    choices = [[] for _ in rows]
    for block in range(1, full + 1):
        if class_passes(closed, full, block):
            choices[vertices(block)[0]].append(block)

    @lru_cache(None)
    def visit(rest):
        if not rest:
            return 0
        best = -len(rows) - 1
        for block in choices[vertices(rest)[0]]:
            if rest & block == block:
                best = max(best, 1 + visit(rest ^ block))
        return best

    k = visit(full)
    visit.cache_clear()
    return k


def producer_table(max_order):
    """A partial coloring is total on the graph or omits some vertex."""
    previous = {0: ((), 0, 0)}
    for n in range(1, max_order + 1):
        children = {}
        for rows, k, b in previous.values():
            for neighbors in range(1 << (n - 1)):
                larger = tuple(row | (((neighbors >> v) & 1) << (n - 1))
                               for v, row in enumerate(rows)) + (neighbors,)
                key = canonical(larger)
                inherited = children.get(key)
                if inherited is None:
                    children[key] = (larger, k, b)
                elif k > inherited[1] or b > inherited[2]:
                    children[key] = (inherited[0], max(k, inherited[1]), max(b, inherited[2]))
        previous = {}
        for key, (rows, k, b) in children.items():
            previous[key] = (rows, max(k, total_colors(rows)),
                             n if all(row.bit_count() <= 1 for row in rows) else b)
        del children
        oriented = either = equal = gaps = biggest_gap = 0
        totals = []
        for key, (rows, k, b) in previous.items():
            opposite = canonical(complement(rows))
            _, ck, cb = previous[opposite]
            value = k + ck
            totals.append(value)
            biggest_gap = max(biggest_gap, k - b)
            gaps += int(k > b)
            if value == n + 2:
                equal += 1
                oriented += int(k > b)
                either += int(k > b or ck > cb)
        require(max(totals) <= n + 2, n, max(totals))
        print('TABLE', n, 'unlabeled', len(previous), 'sum_range', (min(totals), max(totals)),
              'equality', equal, 'gap_G', gaps, 'max_gap', biggest_gap,
              'equality_gap_G', oriented, 'equality_gap_either', either, flush=True)


def edge_count_attack():
    # Optimize over all length-m degree lists with fixed sum. This deliberately
    # relaxes graphicality; every simple graph still lies in its own sum layer.
    for m in range(8, 31):
        term = [Fraction(1, (d + 2) // 2) + Fraction(1, (m + 1 - d) // 2)
                for d in range(m)]
        prev = [Fraction(0)]
        for _ in range(m):
            next_layer = [None] * (len(prev) + m - 1)
            for partial, value in enumerate(prev):
                for d, increment in enumerate(term):
                    candidate = value + increment
                    j = partial + d
                    if next_layer[j] is None or candidate > next_layer[j]:
                        next_layer[j] = candidate
            prev = next_layer
        graph_layers = prev[::2]
        high = max(graph_layers)
        require(high == parity_bound(m), m, high)
        print('EDGE_LAYERS', m, 'even_sums', len(graph_layers), 'max', high,
              'odd_sum_max', max(prev[1::2]), flush=True)


def feasible_maps(rows):
    n = len(rows)
    for s in subsets((1 << n) - 1):
        for blocks in partitions(s):
            labels = [None] * n
            for color, block in enumerate(blocks, 1):
                for v in vertices(block):
                    labels[v] = color
            if is_coloring(rows, labels, len(blocks)):
                yield s, len(blocks), weight_vector(n, blocks)


def support_pair_attack():
    """Check the inside/outside argument on both arbitrary colorings, including all ties."""
    for n in range(7):
        codes = {canonical(decode(n, i)) for i in range(1 << len(edges(n)))}
        pair_count = 0
        by_overlap = Counter()
        max_inside_excess = None
        for code in sorted(codes):
            rows = decode(n, code)
            comp = complement(rows)
            left = list(feasible_maps(rows))
            right = list(feasible_maps(comp))
            full = (1 << n) - 1
            sigma = {}
            for s in subsets(full):
                ds = []
                for v in vertices(s):
                    d = (rows[v] & s).bit_count()
                    c = (comp[v] & s).bit_count()
                    require(d + c + 1 == s.bit_count(), n, code, s, v)
                    ds.append(d)
                sigma[s] = checked_score(tuple(sorted(ds)))
            for s1, k1, w1 in left:
                for s2, k2, w2 in right:
                    overlap = s1 & s2
                    m = overlap.bit_count()
                    inside = Fraction(0)
                    outside = Fraction(0)
                    for v in range(n):
                        local = w1[v] + w2[v]
                        if overlap & (1 << v):
                            inside += local
                        else:
                            require(local <= 1, code, s1, s2, v, local)
                            outside += local
                    require(inside <= sigma[overlap] and outside <= n - m
                            and inside + outside == k1 + k2 <= n + 2,
                            n, code, s1, s2, inside, outside)
                    excess = inside - m
                    if max_inside_excess is None or excess > max_inside_excess:
                        max_inside_excess = excess
                    by_overlap[m] += 1
                    pair_count += 1
        print('SUPPORT_PAIRS', n, 'isomorphism_classes', len(codes), 'coloring_pairs', pair_count,
              'max_actual_inside_minus_m', max_inside_excess, 'by_overlap',
              [by_overlap[m] for m in range(n + 1)], flush=True)


@lru_cache(maxsize=32768)
def graphical(degrees):
    """Havel-Hakimi reduction of an ascending degree list."""
    if not degrees or degrees[-1] == 0:
        return True
    d = degrees[-1]
    keep = len(degrees) - 1 - d
    if keep < 0 or degrees[keep] == 0:
        return False
    remaining = degrees[:keep] + tuple(x - 1 for x in degrees[keep:-1])
    return graphical(tuple(sorted(remaining)))


def degree_list_attack():
    for m in range(8, 16):
        cap = parity_bound(m)
        terms = [reciprocal(d) + reciprocal(m - 1 - d) for d in range(m)]
        layers = [None] * (len(edges(m)) + 1)
        visited = even_sum = realized = 0
        for degrees in combinations_with_replacement(range(m), m):
            visited += 1
            total = sum(degrees)
            if total % 2:
                continue
            even_sum += 1
            if not graphical(degrees):
                continue
            realized += 1
            e = total // 2
            score = sum((terms[d] for d in degrees), Fraction(0))
            require(score <= cap, m, e, degrees, score)
            if layers[e] is None or layers[e] < score:
                layers[e] = score
        require(all(x is not None for x in layers) and layers == layers[::-1], m, layers)
        require(max(layers) == cap, m, cap, layers)
        print('GRAPHICAL', m, 'sorted_lists', visited, 'even_sum', even_sum, 'realized', realized,
              'max', cap, 'edge_counts_at_max', [e for e, x in enumerate(layers) if x == cap],
              flush=True)
        graphical.cache_clear()


def main():
    signal.alarm(int(os.environ.get('REFEREE_SECONDS', '2700')))
    if sys.argv[1:] == ['--degree-lists']:
        degree_list_attack()
        return
    if sys.argv[1:] == ['--pairs']:
        support_pair_attack()
        return
    if sys.argv[1:] == ['--table']:
        producer_table(9)
        return
    if sys.argv[1:] == ['--order-eight']:
        sigma_census(8)
        return
    require(not sys.argv[1:], 'unrecognized arguments', sys.argv[1:])
    benchmarks()
    controls()
    lemma_two()
    for n in range(7):
        coloring_census(n)
    for m in range(8):
        sigma_census(m)
    stream = IntegerStream(260925128)
    for m in range(8, 31):
        medium(m, stream)
    edge_count_attack()
    sigma_census(8)
    producer_table(9)
    support_pair_attack()
    degree_list_attack()
    print('PASS all requested checks completed', flush=True)


if __name__ == '__main__':
    main()

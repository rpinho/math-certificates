#!/usr/bin/env python3
"""Independently verify the exact comparisons from white-square runs."""

from itertools import permutations


def layered(shape):
    """Return the one-based direct sum of the indicated reversals."""
    result = []
    for width in shape:
        start = len(result)
        result.extend(range(start + width, start, -1))
    return tuple(result)


def runs(board):
    """Label each maximal contiguous white run along the first axis."""
    labels = {}
    count = 0
    for i, row in enumerate(board):
        at_start = True
        for j, white in enumerate(row):
            if white:
                if at_start:
                    count += 1
                labels[i, j] = count - 1
            at_start = not white
    return labels, count


def direct_count(permutation):
    """Sweep across words with a bit set for each used, live down word."""
    n = len(permutation)
    if sorted(permutation) != list(range(1, n + 1)):
        raise ValueError("expected a one-based permutation")
    board = [[j != black for j in range(1, n + 1)] for black in permutation]
    across, row_count = runs(board)
    down, column_count = runs(zip(*board))
    if row_count != column_count:
        return 0

    rows = [0] * row_count
    last = [0] * column_count
    for (i, j), row in across.items():
        column = down[j, i]
        rows[row] |= 1 << column
        last[column] = row

    expiry = [0] * row_count
    for column, row in enumerate(last):
        expiry[row] |= 1 << column

    counts = {0: 1}
    for adjacent, closing in zip(rows, expiry):
        following = {}
        for used, count in counts.items():
            remaining = adjacent & ~used
            while remaining:
                selected = remaining & -remaining
                remaining ^= selected
                occupied = used | selected
                if occupied & closing == closing:
                    live = occupied & ~closing
                    following[live] = following.get(live, 0) + count
        counts = following
    return counts.get(0, 0)


def compositions(n):
    if n == 0:
        yield ()
    else:
        for width in range(1, n + 1):
            for rest in compositions(n - width):
                yield (width,) + rest


def falling(n, k):
    result = 1
    for offset in range(k):
        result *= n - offset
    return result


def triangular(width):
    """Stirling counts for each number of unfilled words in a triangle."""
    counts = [1]
    for length in range(1, width + 1):
        counts = [
            (k * counts[k] if k < length else 0) + (counts[k - 1] if k else 0)
            for k in range(length + 1)
        ]
    return counts


def block_count(shape):
    """Sweep diagonal blocks, recording the number of open words of each kind."""
    opened = {0: 1}
    for width in shape:
        triangle = triangular(width)
        following = {}
        for pool, weight in opened.items():
            for west in range(min(width, pool) + 1):
                if pool == 0:
                    # With no previous open words, all existing west and north
                    # words must be matched at this boundary.
                    west_weight = 1 if west == 0 else 0
                else:
                    west_weight = triangle[west] * falling(pool, west) ** 2
                for east in range(width + 1):
                    east_weight = triangle[east]
                    unfilled = pool - west + east
                    following[unfilled] = (
                        following.get(unfilled, 0) + weight * west_weight * east_weight
                    )
        opened = following
    return opened


def shell_count(n, m):
    if m == 0:
        return 1
    return sum(
        (weight * k ** (n - 2 * m) * falling(k, k)) ** 2
        for k, weight in enumerate(triangular(m))
        if k
    )


def seven_square(t):
    coefficients = block_count((5, 3))
    if tuple(coefficients[k] for k in range(1, 8)) != (
        1081, 11763, 34786, 34315, 12250, 1435, 25
    ):
        raise AssertionError("incorrect seven-square coefficients")
    return sum((weight * h ** t * falling(h, h)) ** 2 for h, weight in coefficients.items())


def require_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: got {actual}, expected {expected}")


def verify():
    witnesses = (
        (17, (5, 3, 1, 3, 5), 104476798194769, 103460138813701, 1016659381068),
        (18, (5, 3, 1, 1, 3, 5), 2949333362474113, 2445624351454501, 503709011019612),
    )
    for n, shape, count, maximum, excess in witnesses:
        word = layered(shape)
        if n == 17:
            require_equal(word, (5, 4, 3, 2, 1, 8, 7, 6, 9, 12, 11, 10, 17, 16, 15, 14, 13), "w17")
        require_equal(direct_count(word), count, f"n={n} grid")
        require_equal(seven_square(n - 16), count, f"n={n} seven-square")
        shells = []
        for m in range(n // 2 + 1):
            single = (m,) + (1,) * (n - 2 * m) + (m,)
            observed = direct_count(layered(single))
            require_equal(observed, shell_count(n, m), f"n={n}, m={m}")
            shells.append(observed)
        require_equal(max(shells), maximum, f"n={n} maximum")
        require_equal(shells[5], maximum, f"n={n}, m=5 attainment")
        require_equal(count - maximum, excess, f"n={n} excess")
        print(f"n={n} witness={count}, shells={shells}, excess={excess}")

    for w, count in [((2, 1, 4, 3), 5), ((2, 4, 1, 3), 2), ((1, 2, 3, 4), 1)]:
        require_equal(direct_count(w), count, f"control {w}")
    checked = 0
    for n, maximum in enumerate([1, 1, 1, 5, 17], 1):
        observed = max(direct_count(w) for w in permutations(range(1, n + 1)))
        require_equal(observed, maximum, f"n={n} exhaustive maximum")
        for shape in compositions(n):
            word = layered(shape)
            if shape == (n,):
                expected = 1
            else:
                # Last block closes the pools. Its south and east boundary
                # words are already covered by its forced outer triangle.
                prefix = block_count(shape[:-1])
                triangle = triangular(shape[-1])
                expected = sum(
                    value * triangle[pool] * falling(pool, pool) ** 2
                    for pool, value in prefix.items()
                    if pool < len(triangle)
                )
            require_equal(direct_count(word), expected, f"layered control {shape}")
            checked += 1
    require_equal(checked, 31, "small layered case count")
    print("Small controls passed for all 31 layered compositions and 153 permutations at n=1..5.")


if __name__ == "__main__":
    verify()

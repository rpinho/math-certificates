"""Big-integer reference for the binary32 table and README equations."""

from array import array
from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
from pathlib import Path
from struct import iter_unpack
import sys

SCALE = 1 << 20
ROUNDINGS = ("away", "even", "up")


@dataclass(frozen=True)
class Chain:
    pairs: tuple[tuple[int, int], ...]
    h: int
    v: int


def chain_family(s, H, window, positive_gamma=False):
    """Enumerate pairs of equally sized subsets, lifting values modulo P^3."""
    P = 2**s
    modulus = P**3
    by_residue = [[] for _ in range(P)]
    gamma_power = [pow(7, g if positive_gamma else -g, modulus) for g in range(H)]
    for size in range(min(s, H) + 1):
        for aa in combinations(range(s), size):
            for gg in combinations(range(H), size):
                pairs = tuple(zip(aa, gg))
                v = sum(2**a * gamma_power[g] for a, g in pairs) % modulus
                by_residue[v % P].append(Chain(pairs, gg[-1] + 1 if gg else 0, v))
    if any(not group for group in by_residue):
        raise ValueError("uncovered residue")
    result = []
    for group in by_residue:
        limit = H if window is None else min(chain.h for chain in group) + window
        result.append(tuple(sorted((chain for chain in group if chain.h <= limit),
                                   key=lambda chain: chain.pairs)))
    return tuple(result)


def canonical_rows(family):
    for residue, chains in enumerate(family):
        for chain in chains:
            fields = [residue, len(chain.pairs)]
            for pair in chain.pairs:
                fields.extend(pair)
            yield " ".join(map(str, fields)) + "\n"


def read_roundings(path, s):
    """Decode the source bytes as signed dyadic rationals without float operations."""
    raw = Path(path).read_bytes()
    P = 2**s
    if len(raw) != 4 * P * P:
        raise ValueError("binary32 byte count differs from P^2")
    away, even, up = (array("q") for _ in ROUNDINGS)
    append_away, append_even, append_up = away.append, even.append, up.append
    positive_ties = negative_ties = 0
    for (bits,) in iter_unpack("<I", raw):
        negative = bits >> 31
        exponent = (bits >> 23) & 255
        if exponent == 255:
            raise ValueError("non-finite binary32 entry")
        significand = bits & ((1 << 23) - 1)
        if exponent:
            significand += 1 << 23
        shift = max(exponent, 1) - 130
        if shift >= 0:
            integral, remainder, denominator = significand << shift, 0, 1
        else:
            denominator = 1 << -shift
            integral, remainder = divmod(significand, denominator)
        doubled = remainder * 2
        if doubled == denominator:
            negative_ties += negative
            positive_ties += 1 - negative
            sign = -1 if negative else 1
            append_away(sign * (integral + 1))
            append_even(sign * (integral + (integral % 2)))
            append_up(-integral if negative else integral + 1)
        else:
            rounded = integral + (doubled > denominator)
            rounded = -rounded if negative else rounded
            append_away(rounded)
            append_even(rounded)
            append_up(rounded)
    return dict(zip(ROUNDINGS, (away, even, up))), {
        "finite": P * P, "ties": positive_ties + negative_ties,
        "negative_ties": negative_ties, "positive_ties": positive_ties,
        "raw_sha256": sha256(raw).hexdigest(),
    }


def little_endian_digest(table):
    if sys.byteorder == "big":
        table = array("q", table)
        table.byteswap()
    return sha256(memoryview(table)).hexdigest()


def exact_next(P, c, b, u, chain):
    z = c + P*b + P**2*u
    q, remainder = divmod(z - chain.v, P)
    if remainder:
        raise ValueError("transition lost its low-digit match")
    b_next, c_next = divmod((pow(7, chain.h) * q) % P**2, P)
    return c_next, b_next


def drift(table, family, c, b, layout, rule="standard", target_delta=None):
    """Direct look-ahead enumeration. Optionally derive the exact target-edit response."""
    P = len(family)
    modulus = P * P
    cb = layout == "cb"
    target = c*P + b if cb else b*P + c
    options = []
    for chain in family[c]:
        value = chain.v % P if rule == "low-value" else chain.v
        exponent = chain.h - 1 if rule == "last-gamma" and chain.h else chain.h
        options.append((value, 7**exponent, SCALE * chain.h))
    total = expected_delta = choices_hitting_target = 0
    for u in range(P):
        z = c + P*b + modulus*u
        best = best_hit = best_miss = None
        for value, factor, cost in options:
            quotient, remainder = divmod(z - value, P)
            if remainder:
                raise ValueError("transition lost its low-digit match")
            next_b, next_c = divmod((factor * quotient) % modulus, P)
            index = next_c*P + next_b if cb else next_b*P + next_c
            score = cost + table[index]
            if best is None or score < best:
                best = score
            if target_delta is not None:
                if index == target:
                    best_hit = score if best_hit is None else min(score, best_hit)
                else:
                    best_miss = score if best_miss is None else min(score, best_miss)
        total += best
        if target_delta is not None and best_hit is not None:
            choices_hitting_target += 1
            edited = best_hit + target_delta
            if best_miss is not None:
                edited = min(edited, best_miss)
            expected_delta += edited - best
    base = total - P * table[target]
    if target_delta is None:
        return base
    return base, expected_delta - P * target_delta, choices_hitting_target

"""Exact replay of the Section 3 encoder and the fresh-digit test."""

import argparse
from array import array
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import random
import signal
import sys
import time

from reference import SCALE, chain_family, exact_next

SEED = 1110
LARGE_SAMPLE = 256


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ceil(x):
    return -(-x.numerator // x.denominator)


def simplest_between(low, high):
    denominator = 1
    while True:
        numerator = (denominator * low).numerator // (denominator * low).denominator + 1
        candidate = Fraction(numerator, denominator)
        if candidate < high:
            return candidate
        denominator += 1


def check_size(P, N, c_star, numerator, denominator, exponent):
    """Check n < P^(N+1)*7^(c_star+1)/(P*7^(-exponent) - 1) by integer powers."""
    a, b = exponent.numerator, exponent.denominator
    require(7**a < P**b, "denominator in K must be positive")
    lhs = (numerator * P)**b
    rhs = 7**a * (numerator + denominator * P**(N+1) * 7**(c_star+1))**b
    require(lhs < rhs, "strict Lemma 1(c) bound failed")


@lru_cache(maxsize=16384)
def lifted_value(pairs, modulus):
    return sum((1 << a) * pow(7, -g, modulus) for a, g in pairs) % modulus


class Encoder:
    def __init__(self, s, H, N, c_star, lam, family, policy):
        self.s, self.H, self.N, self.c_star = s, H, N, c_star
        self.lam, self.family, self.policy = lam, family, policy
        self.P = 2**s
        self.powers = [self.P**t for t in range(N + 1)]
        self.ceilings = [ceil(t * lam) for t in range(N + 1)]
        self.A = self.ceilings[N] + c_star

    def encode(self, y, upper_exponent=None):
        P, N, A = self.P, self.N, self.A
        modulus = self.powers[N]
        require(0 <= y < modulus, "y outside input residues")
        z, G, prefix = y, 0, 0
        exponents, history, heights, fresh = [], [], [G], []
        padded = 0
        for t in range(N):
            c = z % P
            early = t <= N - 3
            if early:
                b, u = (z // P) % P, (z // P**2) % P
                fresh.append((t, u, (tuple(history), tuple(heights), (c, b))))
                chain = self.policy(c, b, u)
            else:
                chain = self.family[c][0]
            precise_modulus = self.powers[N-t]
            value = lifted_value(chain.pairs, precise_modulus)
            next_G = max(G + chain.h, self.ceilings[t+1])
            quotient, leftover = divmod(z - value, P)
            require(leftover == 0, "encoder chain residue mismatch")
            next_modulus = self.powers[N-t-1]
            next_z = (pow(7, next_G - G, next_modulus) * quotient) % next_modulus

            excess = G - t*self.lam
            next_excess = next_G - (t+1)*self.lam
            require(0 <= next_excess <= excess + self.H, "Fact 1 failed")
            if next_G > G + chain.h:
                padded += 1
                require(next_excess < 1, "padded excess is at least one")
            elif early:
                require(next_excess == excess + chain.h - self.lam, "Fact 2 excess failed")
                next_state = next_z % P, (next_z // P) % P
                require(next_state == exact_next(P, c, b, u, chain), "Fact 2 state failed")
            prefix = (prefix + self.powers[t] * pow(7, -G, modulus) * value) % modulus
            remainder = self.powers[t+1] * pow(7, -next_G, modulus) * next_z
            require((prefix + remainder) % modulus == y, "Lemma 1(b) invariant failed")
            exponents.extend((self.s*t + a, A-G-g) for a, g in chain.pairs)
            history.append(chain.pairs)
            heights.append(next_G)
            G, z = next_G, next_z

        admissible = G <= A
        antichain = all(a0 < a1 and g0 > g1 for (a0, g0), (a1, g1) in zip(exponents, exponents[1:]))
        require(antichain, "Lemma 1(a) went non-strict")
        shift = max(0, -min((g for _, g in exponents), default=0))
        require(not admissible or shift == 0, "negative exponent on admitted y")
        numerator = sum((1 << a) * 7**(g + shift) for a, g in exponents)
        denominator = 7**shift
        require((numerator == 0) == (y == 0), "zero sum did not identify y=0")
        require(y != 0 or admissible, "y=0 is inadmissible")
        modular_n = (numerator * pow(denominator, -1, modulus)) % modulus
        require(modular_n == (pow(7, A, modulus) * y) % modulus,
                "Lemma 1(b) reconstructed sum failed")
        check_size(P, N, self.c_star, numerator, denominator, self.lam)
        if upper_exponent is not None:
            check_size(P, N, self.c_star, numerator, denominator, upper_exponent)
        return admissible, numerator, fresh, padded


def choose_small_policies(family):
    P = len(family)
    yield "first", lambda c, b, u: family[c][0]
    yield "tallest", lambda c, b, u: max(family[c], key=lambda chain: chain.h)
    for seed in (SEED, SEED + 1):
        rng = random.Random(seed)
        lookups = {(c, b, u): rng.choice(family[c])
                   for c in range(P) for b in range(P) for u in range(P)}
        yield f"random_{seed}", lambda c, b, u, lookups=lookups: lookups[c, b, u]


def test_small():
    s, H, N, c_star, lam = 3, 4, 4, 0, Fraction(1)
    P = 2**s
    family = chain_family(s, H, window=None)
    cases = {}
    for name, policy in choose_small_policies(family):
        encoder = Encoder(s, H, N, c_star, lam, family, policy)
        frequencies, signatures = {}, {}
        admitted_outputs = set()
        padded_steps = 0
        for y in range(P**N):
            admissible, numerator, fresh, padded = encoder.encode(y)
            if admissible:
                require(numerator not in admitted_outputs, "Lemma 1(b) injection collision")
                admitted_outputs.add(numerator)
            padded_steps += padded
            for t, u, signature in fresh:
                key = (t, y % P**(t+2))
                counts = frequencies.setdefault(key, Counter())
                counts[u] += 1
                require(signatures.setdefault(key, signature) == signature,
                        "Fact 3 measurability failed")
        conditioning = {}
        for t in range(N-2):
            classes = [counter for key, counter in frequencies.items() if key[0] == t]
            expected = P**(N-t-3)
            require(len(classes) == P**(t+2), "missing conditioning classes")
            require(all([counts[u] for u in range(P)] == [expected] * P for counts in classes),
                    "fresh look-ahead not exactly uniform")
            conditioning[t] = {"classes": len(classes), "values_per_class": P,
                               "count_per_value": expected}
        cases[name] = {
            "inputs": P**N, "admissible": len(admitted_outputs),
            "inadmissible": P**N - len(admitted_outputs), "distinct_admitted_n": len(admitted_outputs),
            "strict_antichain_checks": P**N, "congruence_checks": P**N, "strict_K_checks": P**N,
            "zero_admitted": 0 in admitted_outputs, "padded_steps": padded_steps,
            "conditioned_uniformity": conditioning,
        }
    return {"s": s, "H": H, "N": N, "c_star": c_star, "lambda": str(lam),
            "chain_count": sum(map(len, family)), "policies": cases}


def test_large():
    s, H = 11, 10
    P = 2**s
    logs = Path("logs")
    record = json.loads((logs / "reference.json").read_text())
    claim = json.loads((logs / "claim.json").read_text())
    require(claim["passes"], "certificate replay did not pass")
    raw = Path("V_hat.i64le").read_bytes()
    digest = sha256(raw).hexdigest()
    require(digest == record["rounding"]["away"]["sha256_i64le"], "V_hat digest mismatch")
    table = array("q")
    table.frombytes(raw)
    if sys.byteorder == "big":
        table.byteswap()
    family = chain_family(s, H, window=3)
    upper = Fraction(286, 73)
    lower = Fraction(claim["readme_expectation"]["maximum"], P*SCALE)
    lam = simplest_between(lower, upper)
    require(lower < lam < upper, "lambda outside proven interval")

    def minimize(c, b, u):
        def objective(chain):
            c_next, b_next = exact_next(P, c, b, u, chain)
            return SCALE * chain.h + table[c_next*P + b_next]
        return min(family[c], key=objective)

    rng = random.Random(SEED)
    outcomes = {}
    for N in (10, 20):
        encoder = Encoder(s, H, N, 2*H, lam, family, minimize)
        samples = [0]
        seen = {0}
        while len(samples) <= LARGE_SAMPLE:
            y = rng.randrange(1, P**N)
            if y not in seen:
                seen.add(y)
                samples.append(y)
        admitted = set()
        zero, padded_steps = False, 0
        for y in samples:
            admissible, numerator, _, padded = encoder.encode(y, upper_exponent=upper)
            padded_steps += padded
            if admissible:
                require(numerator not in admitted, "large encoder admission collision")
                admitted.add(numerator)
            if y == 0:
                zero = admissible and numerator == 0
        outcomes[N] = {
            "random_inputs": LARGE_SAMPLE, "zero_checks": 1, "zero_admitted": zero,
            "empirical_admissible_random": {"numerator": len(admitted) - int(zero),
                                           "denominator": LARGE_SAMPLE},
            "strict_antichain_checks": len(samples), "congruence_checks": len(samples),
            "strict_K_checks": len(samples), "strict_upper_surrogate_checks": len(samples),
            "distinct_admitted_n": len(admitted), "padded_steps": padded_steps,
        }
    return {"s": s, "H": H, "c_star": 2*H, "lambda": str(lam),
            "upper_exponent": str(upper), "V_hat_sha256_i64le": digest, "runs": outcomes}


def expired(signum, frame):
    raise TimeoutError("encoder deadline reached")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deadline", type=int, required=True)
    args = parser.parse_args()
    remaining = args.deadline - time.time()
    require(remaining > 0, "deadline already reached")
    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, remaining)
    result = {"small_exhaustive": test_small(), "large_samples": test_large()}
    Path("logs/encoder.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Encoder passed the exhaustive small cases and both large sample runs.")


if __name__ == "__main__":
    main()

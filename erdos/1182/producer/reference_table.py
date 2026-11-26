"""Floating-point reference rates for the degree-10 pairing model."""

import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import root
from scipy.special import logsumexp, xlogy

D = 10
EDGES = [(i, (i + 2) % 5) for i in range(5)]
ALLOWED = np.array([[(j-i) % 5 in (0, 2, 3) for j in range(5)] for i in range(5)])


def naive(a):
    support = a > 0
    positive = a[support]
    matrix = ALLOWED[np.ix_(support, support)]
    fit = root(lambda l: l + np.log(matrix @ np.exp(l)) - np.log(positive),
               np.log(positive) / 2, tol=1e-11)
    t = np.zeros(5)
    t[support] = np.exp(fit.x)
    q = ALLOWED * t[:, None] * t
    if np.max(np.abs(q.sum(axis=1) - a)) > 1e-11:
        raise ArithmeticError("row scaling failed")
    rate = (D-1)*np.sum(xlogy(a, a)) - D/2*np.sum(xlogy(q, q))
    upper = (D-1)*np.sum(xlogy(a, a)) - D*np.dot(positive, fit.x) + D/2*np.log(q.sum())
    if abs(rate-upper) > 1e-10:
        raise ArithmeticError("naive primal-dual mismatch")
    return float(rate), q


def row_types(i, case, a):
    """Local count vectors, row-symmetry features, and log multiplicities."""
    destinations = [j for j in range(5) if ALLOWED[i, j] and a[j] > 0]
    hot_dest = case == 2 and i == 0
    local_size = len(destinations) + hot_dest
    rows, hot_counts, multiplicities = [], [], []
    for partial in itertools.product(range(D+1), repeat=local_size-1):
        counts = (*partial, D-sum(partial))
        if counts[-1] < 0:
            continue
        row = np.zeros(5)
        row[destinations] = counts[:len(destinations)]
        hot = 0
        if case == 1 and (i == 0 and min(row[2], row[3]) == 0 or i == 2 and row[0] == 0):
            continue
        if case == 2:
            if i == 0:
                hot = counts[-1]
                if not hot:
                    continue
                row[2] += hot
            if i == 2:
                if not row[0]:
                    continue
                hot = row[0] if row[4] else 0
        rows.append(row / D)
        hot_counts.append(hot / D)
        multiplicities.append(math.log(math.factorial(D) // math.prod(math.factorial(x) for x in counts)))
    rows = np.array(rows)
    hot_counts = np.array(hot_counts)
    features = np.zeros((len(rows), 5 + (case == 2)))
    for col, (u, v) in enumerate(EDGES):
        if i == u:
            features[:, col] = rows[:, v]
        if i == v:
            features[:, col] = -rows[:, u]
    if case == 2:
        features[:, 5] = hot_counts if i == 0 else -hot_counts
    return rows, hot_counts, np.array(multiplicities), features


def constrained(a, case):
    """Maximize from the naive starting point using entropy minorization.

    Report a stationary candidate only after checking row balance and the
    entropy primal against the dual of the linearized subproblem.
    """
    rate, q = naive(a)
    if (case == 1 and (a[3] < a[0]/D or min(a[0], a[2]) < max(a[0], a[2])/D)
            or case == 2 and a[4] < a[0]/(D*(D-1))):
        return {"infeasible": True}
    rows = [(i, a[i], *row_types(i, case, a)) for i in range(5) if a[i]]
    dim = 5 + (case == 2)
    lam = np.zeros(dim)
    r = q[0, 2] / 2
    previous = -np.inf
    for iteration in range(1, 1001):
        gradient = (D/2)*(1+np.log(np.maximum(q, 1e-300)))
        hot_slope = 0.
        if case == 2:
            hot_slope = D*np.log(r/(q[0, 2]-r))
            gradient[0, 2] += D*np.log((q[0, 2]-r)/q[0, 2])
        base = [
            mult + counts @ gradient[i] + (hot * hot_slope if i == 0 else 0)
            for i, _, counts, hot, mult, _ in rows
        ]

        def dual(l, details=False):
            value = 0.
            residual = np.zeros(dim)
            hessian = np.zeros((dim, dim))
            laws = []
            for (_, size, _, _, _, features), b in zip(rows, base):
                logs = b + features @ l
                z = logsumexp(logs)
                p = np.exp(logs-z)
                expectation = p @ features
                centered = features-expectation
                value += size*z
                residual += size*expectation
                hessian += size*((centered.T*p) @ centered)
                laws.append(p)
            if details:
                return laws
            return value, residual, hessian

        for _ in range(100):
            value, balance, hessian = dual(lam)
            if np.max(np.abs(balance)) < 5e-13:
                break
            direction = np.linalg.lstsq(hessian, balance, rcond=1e-14)[0]
            directional = balance @ direction
            step = 1.
            while step > 2**-35:
                trial = lam-step*direction
                new_value, new_balance, _ = dual(trial)
                if (new_value <= value-1e-4*step*directional or
                        abs(new_value-value) < 4e-14 and np.max(np.abs(new_balance)) < np.max(np.abs(balance))):
                    lam = trial
                    break
                step /= 2
            else:
                raise ArithmeticError("balance dual stalled")
        else:
            raise ArithmeticError("balance dual failed to converge")

        entropy = 0.
        new_q = np.zeros_like(q)
        new_r = 0.
        for (i, size, counts, hot, mult, _), p in zip(rows, dual(lam, True)):
            entropy += size*(p @ mult - np.sum(xlogy(p, p)))
            new_q[i] = size*(p @ counts)
            if i == 0:
                new_r = size*(p @ hot)
        if np.max(np.abs(new_q-new_q.T)) > 1e-11:
            raise ArithmeticError("primal row balance")
        penalty = 0.
        if case == 2:
            split = np.array([new_r, new_q[0, 2]-new_r])
            if np.min(split) <= 0:
                raise ArithmeticError("infeasible hot split")
            penalty = D*np.sum(xlogy(split, split/new_q[0, 2]))
        new_rate = float((D/2)*np.sum(xlogy(new_q, new_q)) - np.sum(xlogy(a, a)) + entropy + penalty)
        linear_primal = entropy + np.sum(gradient*new_q) + hot_slope*new_r
        if abs(linear_primal-value) > 1e-9 or new_rate < previous-1e-10:
            raise ArithmeticError("linearized primal-dual or monotonicity check")
        if max(np.max(np.abs(q-new_q)), abs(r-new_r)) < 2e-11:
            log_weights = gradient.copy()/D
            for k,(i,j) in enumerate(EDGES):
                log_weights[i,j] += lam[k]/D
                log_weights[j,i] -= lam[k]/D
            log_hot = [0.]*5
            if case == 2:
                log_hot[0], log_hot[2] = (hot_slope+lam[5])/D, -lam[5]/D
            return dict(rate=new_rate, q=new_q.tolist(), r=new_r, iterations=iteration,
                        balance_error=float(np.max(np.abs(balance))), log_hot=log_hot,
                        log_weights=log_weights.tolist(), linearized_gap=float(value-linear_primal))
        q, r, previous = new_q, new_r, new_rate
    raise ArithmeticError("outer iteration limit")


def main():
    profiles = {
        "naive_cap_0.4": [.4, .00013884009573850511, .4, .1871172864884783, .012743873415783051],
        "naive_cap_0.4001": [.4001, .00013798522823667877, .4001, .18688742801391883, .012774586757843947],
        "original_peak": [.4001, .00001, .4001, .18789, .01190],
        "symmetric_normalized": [.4001, .00001, .4001, .1049, .09489],
        "symmetric_unnormalized": [.4001, .00001, .4001, .09489, .1049],
        "mirrored_unnormalized": [.4001, .00011, .4001, .0119, .18779],
        "mirrored_normalized": [.4001, .00011, .4001, .18779, .0119],
        "a2_larger": [.397, .0002, .4001, .1877, .015],
    }
    out = {}
    for name, profile in profiles.items():
        a = np.array(profile)
        if abs(sum(a)-1) > 1e-12:
            raise ValueError((name, sum(a)))
        naive_rate, naive_q = naive(a)
        result = {"profile": profile, "naive": naive_rate, "naive_q": naive_q.tolist()}
        for case in (1, 2):
            result[f"case_{case}"] = constrained(a, case)
        for case in (1, 2):
            entry = result[f"case_{case}"]
            if entry.get("infeasible"):
                continue
            q = np.array(entry["q"])
            slack = (D/2)*(np.sum(xlogy(a,a))-np.sum(xlogy(q,q)))
            if case == 2:
                split = np.array([entry["r"],q[0,2]-entry["r"]])
                slack -= D*np.sum(xlogy(split,split/q[0,2]))
            entry["whole_row_fixed_tilt_lower"] = float(entry["rate"]+slack)
        out[name] = result
        print(name, result["naive"], *(result[f"case_{i}"].get("rate") for i in (1, 2)), flush=True)
    Path("reference_table.json").write_text(json.dumps(out, indent=2)+"\n")


if __name__ == "__main__":
    main()

"""Adversarial checks of statistic conventions; execute on compute pod only."""
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import sympy as s


def main():
    # A source-valid leaf reattachment, true star 0->{1,2}, candidate 0->1->2.
    b = s.Matrix([[1, 0, 1], [0, 1, -1], [0, 0, 1]])
    x = s.Matrix([s.Rational(1, 10), s.Rational(9, 10), s.Rational(1, 5)])
    n = s.Rational(1, 50)
    inferred = b*x
    assert min(inferred) > 0
    initial_gap = (inferred.dot(inferred) - x.dot(x))
    increment_gap = n*(sum(v*v for v in b)-3)
    assert initial_gap == -s.Rational(6, 25)
    assert increment_gap == s.Rational(1, 25)
    assert initial_gap + increment_gap == -s.Rational(1, 5)
    # This has positive probability on an open set of initial vectors and paths
    # in a sufficiently narrow tube, so adding ||M(0)||^2 really changes the claim.
    convention = {'true_parent': [-1, 0, 0], 'candidate_parent': [-1, 0, 1],
                  'x': [str(v) for v in x], 'candidate_initial': [str(v) for v in inferred],
                  'horizon': str(n), 'increment_gap': str(increment_gap),
                  'initial_penalty_gap': str(initial_gap),
                  'total_gap_with_initial_penalty': str(initial_gap+increment_gap),
                  'conclusion': 'Extra initial-state penalty admits a wrong feasible tree at gamma=1; not the explicit source increment limit.'}
    # Check the exact Gaussian quadratic form moment on the same leaf witness.
    z = s.symbols('z0:3')
    c = b.T*b-s.eye(3)
    polynomial = (s.Matrix(z).T*c*s.Matrix(z))[0]
    def gaussian_expectation(poly):
        total = 0
        for powers, coefficient in s.Poly(s.expand(poly), *z).terms():
            moment = 1
            for power in powers:
                if power % 2:
                    moment = 0
                    break
                if power:
                    moment *= s.factorial2(power-1)
            total += coefficient*moment
        return s.simplify(total)
    mean = gaussian_expectation(polynomial)
    variance = gaussian_expectation(polynomial**2)-mean**2
    assert mean == s.trace(c) == 2
    assert variance == 2*s.trace(c*c) == 16
    # Source Lemma 6 studies a different comparison, with moments 1 and 6.
    zz1, zz2 = z[1:]
    half_gap = zz2*(zz2-2*zz1)
    assert gaussian_expectation(half_gap) == 1
    assert gaussian_expectation(half_gap**2)-1 == 6
    moments = {'leaf_gap_mean': str(mean), 'leaf_gap_variance': str(variance),
               'source_half_gap_mean': '1', 'source_half_gap_variance': '6'}
    # Small numerical diagnostic under exact continuous survival conditioning.
    # Bridge survival weights correct for crossings missed between grid points.
    # This is a diagnostic of the proof, not an empirical universal certificate.
    rng = np.random.default_rng(19019)
    start = np.array([.1, .9, .2])
    horizon = .02
    target = 3000
    rows = []
    bn = np.array(b).astype(float)
    for count in [8, 32, 128, 512, 2048]:
        dt = horizon/count
        accepted = proposed = failed_dc = penalty_pass = below_pass = above_pass = 0
        diag = np.zeros(3)
        offdiag = 0.
        while accepted < target:
            batch = min(192, target-accepted)
            inc = rng.normal(0, dt**.5, size=(batch, 3, count))
            paths = np.concatenate((np.broadcast_to(start[None,:,None],(batch,3,1)),
                                    start[None,:,None]+np.cumsum(inc, axis=2)), axis=2)
            left, right = paths[:,:,:-1], paths[:,:,1:]
            positive = np.all(paths > 0, axis=(1,2))
            weights = np.zeros(batch)
            weights[positive] = np.exp(np.sum(np.log(-np.expm1(-2*left[positive]*right[positive]/dt)),axis=(1,2)))
            selected = rng.uniform(size=batch) < weights
            inc = inc[selected]
            accepted += len(inc)
            proposed += batch
            g = inc @ inc.transpose(0,2,1)
            true_energy = np.trace(g,axis1=1,axis2=2)
            candidate_energy = np.einsum('ij,bjk,ik->b',bn,g,bn)
            failed_dc += int(np.count_nonzero(candidate_energy <= true_energy))
            penalty_pass += int(np.count_nonzero(candidate_energy-true_energy <= .24))
            below_pass += int(np.count_nonzero(candidate_energy <= 1.5*true_energy))
            above_pass += int(np.count_nonzero(candidate_energy <= (11/6)*true_energy))
            diag += np.sum(np.diagonal(g,axis1=1,axis2=2)/horizon,axis=0)
            offdiag += np.sum(g[:,1,2]/horizon)
        rows.append({'N': count,'accepted':accepted,'proposed':proposed,
                     'candidate_energy_pass_rate_increment_only':failed_dc/accepted,
                     'candidate_energy_pass_rate_with_initial_penalty':penalty_pass/accepted,
                     'candidate_energy_pass_rate_gamma_3_2':below_pass/accepted,
                     'candidate_energy_pass_rate_gamma_11_6':above_pass/accepted,
                     'mean_normalized_diagonal':(diag/accepted).tolist(),
                     'mean_normalized_cross_12':offdiag/accepted})
        print(json.dumps(rows[-1]),flush=True)
    result = {'status':'PASS','convention_counterexample':convention,
              'exact_moments':moments,'conditioned_brownian_diagnostic':rows,
              'seed':19019,'note':'fixed positive start tests conditional step; all-start result uses dominated convergence'}
    Path('boundary_results.json').write_text(json.dumps(result,indent=2))
    print('PASS',flush=True)


if __name__ == '__main__':
    main()

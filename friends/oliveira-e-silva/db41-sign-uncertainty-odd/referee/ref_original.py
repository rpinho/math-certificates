"""Independent referee. Original full-coordinate unitary DFT, Arb balls.

No claimant code read/imported. Definitions transcribed from paper (3.1),
Problem 3.1; submitted formulas are treated as candidate data to attack.
Run only on the authorized pod.
"""
import json, time
from flint import arb, acb, ctx

ctx.prec = 256
TINY = arb(2) ** -200


def transform(v, ell, roots):
    N = ell * ell
    nz = [(n, x) for n, x in enumerate(v) if not x.is_zero()]
    return [sum((roots[(-k*n) % N] * x for n, x in nz), acb(0))/ell
            for k in range(N)]


def zero(x):
    assert x.contains(0), str(x)
    assert abs(x).abs_upper() < TINY, str(x)


def signed(x, kind):
    if kind == 0:
        zero(x)
    else:
        assert x > 0 if kind > 0 else x < 0, (str(x), kind)


def one(ell):
    N = ell*ell
    q = (N-1)//2
    rep = [n if n <= q else n-N for n in range(N)]
    roots = [acb((arb(2*n)/N).cos_pi(), (arb(2*n)/N).sin_pi())
             for n in range(N)]
    c = [z.real for z in roots]
    s = [z.imag for z in roots]
    t = (arb(1)/N).sin_pi() / (arb(1)/N).cos_pi()
    G, H, badphase, badH, sine = [], [], [], [], []
    for n in range(N):
        r, m = n % ell, n // ell
        a = int(r == 0)
        p = int(r in (1, ell-1))
        b = int(r == 1) - int(r == ell-1)
        G.append((2+2*c[n])*a + (1-c[n])*p - t*s[n]*b)
        badphase.append((2+2*c[n])*a + (1-c[n])*p)
        H.append((arb(1)/ell).cos_pi() - (arb(2*m+1)/ell).cos_pi()
                 if r else arb(0))
        badH.append((arb(1)/ell).cos_pi() - (arb(2*m)/ell).cos_pi()
                    if r else arb(0))
        j = abs(rep[n])
        sine.append((arb(2*j)/ell).sin_pi() if j <= ell else arb(0))
        gz = r not in (0, 1, ell-1) or rep[n] in (-1, 1)
        hz = r == 0 or m in (0, ell-1)
        signed(G[-1], 0 if gz else 1)
        signed(H[-1], 0 if hz else 1)
        if 1 <= abs(rep[n]) <= ell-2:
            zero(G[-1])
        if abs(rep[n]) <= ell-1:
            zero(H[-1])
    DG, DH = transform(G, ell, roots), transform(H, ell, roots)
    for k in range(N):
        zero(DG[k]-G[k])
        zero(DH[k].imag)
        if k % ell not in (0, 1, ell-1):
            zero(DH[k])
    zero(H[q] - (1+(arb(1)/ell).cos_pi()))
    assert H[q] > 0
    # Reproduce the paper's upper from its seed via the original transform.
    Dsine = transform(sine, ell, roots)
    f = [sine[n]-Dsine[n].real for n in range(N)]
    Df = transform(f, ell, roots)
    zero(f[0])
    for n in range(N):
        zero(Df[n]+f[n])
        j = abs(rep[n])
        if j >= ell:
            signed(f[n], 0 if j % ell == 0 else 1)
        if j == ell-1:
            assert f[n] < 0
        # Independently compare the closed formula, treating removable zeros.
        if j == ell:
            zero(Dsine[n])
        else:
            closed = 2*(arb(j)/ell).sin_pi()**2*(arb(2)/ell).sin_pi()
            closed /= ell*((arb(2*j)/N).cos_pi()-(arb(2)/ell).cos_pi())
            zero(Dsine[n]-closed)
    assert f[q] > 0
    scaled = [2*x/f[q] for x in f]  # margin 2 at both paper endpoints
    Dscaled = transform(scaled, ell, roots)
    assert scaled[q] > 1 and -Dscaled[q].real > 1
    zero(scaled[0])
    zero(Dscaled[0])
    # Negative controls: suppressing the small G phase breaks an inner zero;
    # suppressing the H half-grid phase breaks nonnegativity outright.
    assert badphase[1] > 0
    assert badH[1] < 0
    assert G[ell-1] > 0  # invalid at next (known feasible) cutoff ell
    # Poisson/coset-sum-only relaxation has a simple feasible vector.
    # Its DFT equation fails, so subgroup sums alone are not the theorem.
    h = (ell-1)//2
    v = [arb(0) for _ in range(N)]
    for j in (q, N-q):
        v[j] = arb(1)
    for j in (h, N-h):
        v[j] = arb(-1)
    assert all(sum((v[n] for n in range(r,N,ell)),arb(0)).is_zero()
               for r in range(ell))
    assert all(v[n] >= 0 for n in range(N) if abs(rep[n]) >= ell-1)
    Dv = transform(v, ell, roots)
    assert any(not (Dv[n]+v[n]).contains(0) for n in range(N))
    return dict(ell=ell, N=N, signs='certified', DFT_residuals='contain zero and <2^-200',
                H_endpoint=str(H[q]), sine_endpoint=str(f[q]),
                negative_controls='all rejected', subgroup_only_control='feasible but not eigen')


if __name__ == '__main__':
    start=time.monotonic()
    out=[]
    for ell in (3,5,7,9,11,13,17,25,33,41,51):
        row=one(ell)
        out.append(row)
        print(json.dumps(row),flush=True)
        json.dump(dict(rows=out, seconds=time.monotonic()-start),open('original_balls.json','w'),indent=2)
    print('ALL PASS',time.monotonic()-start,flush=True)

"""Independent exact checks for note.tex; Python standard library only.

Arithmetic in Q[z]/Phi_N(z), z=exp(2*pi*i/N), for N=9,25,49,81.
Sines are stored multiplied by i; no floating-point equality tests.
The final decimal column is illustrative, not a proof of positivity.
"""
from fractions import Fraction as Q
from math import cos, pi
from time import process_time


def check(ell, prime):
    N = ell * ell
    q = (N - 1) // 2
    step = N // prime
    degree = N - step

    def reduce(a):
        a = list(a) + [Q(0)] * (N - len(a))
        for j in range(N - 1, degree - 1, -1):
            v = a[j]
            for k in range(prime - 1):
                a[j - degree + k * step] -= v
        return tuple(a[:degree])

    zero = reduce([])
    one = reduce([Q(1)])

    def add(a, b):
        return tuple(x + y for x, y in zip(a, b))

    def scale(a, x):
        return tuple(v * x for v in a)

    def sub(a, b):
        return add(a, scale(b, -1))

    def shift(a, e):
        out = [Q(0)] * N
        for j, v in enumerate(a):
            if v:
                out[(j + e) % N] += v
        return reduce(out)

    def mul(a, b):
        out = [Q(0)] * N
        for j, v in enumerate(a):
            if v:
                for k, w in enumerate(b):
                    if w:
                        out[(j + k) % N] += v * w
        return reduce(out)

    powers = [shift(one, j) for j in range(N)]

    def c(j):
        return scale(add(powers[j % N], powers[-j % N]), Q(1, 2))

    def si(j):
        return scale(sub(powers[j % N], powers[-j % N]), Q(1, 2))

    def D(f):
        # Direct unitary Fourier sums, not the identities in the note.
        result = []
        for k in range(N):
            out = [Q(0)] * N
            for n, a in enumerate(f):
                for j, v in enumerate(a):
                    if v:
                        out[(j - n * k) % N] += v / ell
            result.append(reduce(out))
        return result

    def support(f):
        return {n for n, a in enumerate(f) if a != zero}

    def centered(n):
        return n if n <= q else n - N

    C = [[one if n % ell == b else zero for n in range(N)]
         for b in range(ell)]
    for b in range(ell):
        assert D(C[b]) == [powers[-b*k % N] if k % ell == 0 else zero
                           for k in range(N)]
    P = [add(a, b) for a, b in zip(C[1], C[-1])]
    R = [sub(a, b) for a, b in zip(C[1], C[-1])]
    cP = [mul(c(n), P[n]) for n in range(N)]
    isR = [mul(si(n), R[n]) for n in range(N)]
    assert D(P) == [scale(mul(c(n), C[0][n]), 2) for n in range(N)]
    assert D([mul(c(n), C[0][n]) for n in range(N)]) == [scale(a, Q(1,2)) for a in P]
    assert D(cP) == [sub(mul(c(1), cP[n]), mul(si(1), isR[n])) for n in range(N)]
    assert D(isR) == [sub(mul(si(1), cP[n]), mul(c(1), isR[n])) for n in range(N)]

    # i*tan(pi/N)=(z-1)/(z+1), with exact inverse of (1+z).
    inv = reduce([Q((-1)**j, 2) for j in range(N)])
    assert mul(add(one, powers[1]), inv) == one
    it = mul(sub(powers[1], one), inv)
    assert sub(c(1), mul(it, si(1))) == one
    assert sub(si(1), mul(it, c(1))) == it
    G = [add(add(mul(add(scale(one, 2), scale(c(n), 2)), C[0][n]),
                 mul(sub(one, c(n)), P[n])), mul(it, isR[n])) for n in range(N)]
    assert D(G) == G
    assert all(G[n] == G[-n % N] for n in range(N))
    expected_G = {n for n in range(N) if n % ell in (0, 1, ell-1)} - {1, N-1}
    assert support(G) == expected_G
    assert all(G[n % N] == zero for n in range(-ell+2, ell-1) if n)
    half_N = (N + 1) // 2
    cos_half_N = scale(c(half_N), -1)
    for n in range(N):
        if n % ell == 0:
            assert G[n] == scale(add(one, c(n)), 2)
        elif n % ell == 1:
            # Product-to-sum form of the sine factorization in line 90.
            assert mul(G[n], cos_half_N) == add(cos_half_N, c(n-half_N))

    # Check the coset-sum identity on every coordinate basis vector,
    # and orthogonality of the length-ell Fourier matrix.
    for n in range(N):
        for j in range(ell):
            assert powers[-n*j*ell % N] == powers[-(n % ell)*j*ell % N]
    for r in range(ell):
        total = zero
        for j in range(ell):
            total = add(total, powers[j*r*ell % N])
        assert total == (scale(one, ell) if r == 0 else zero)

    # exp(pi*i/ell) = -z**(ell*(ell+1)/2), since ell is odd.
    half = ell * (ell + 1) // 2
    a = scale(c(half), -1)
    H = [zero if n % ell == 0 else add(a, c(half + (n//ell)*ell)) for n in range(N)]
    for n in range(N):
        r, m = n % ell, n // ell
        if r:
            beta = scale(powers[(half-r) % N], -1)
            beta_bar = scale(powers[-(half-r) % N], -1)
            expanded = sub(a, scale(add(shift(beta, n), shift(beta_bar, -n)), Q(1,2)))
            assert H[n] == expanded
    assert all(H[n] == H[-n % N] for n in range(N))
    assert support(H) == {n for n in range(N) if n % ell != 0 and n//ell not in (0,ell-1)}
    DH = D(H)
    assert support(DH) == {n for n in range(N) if n % ell in (0,1,ell-1)}
    assert H[q] == add(one, a)

    # iw and i*Dw remain in Q(z); check the quotient by cross multiplication.
    iw = [si(ell*abs(centered(n))) if abs(centered(n)) < ell else zero for n in range(N)]
    iDw = D(iw)
    assert D(iDw) == iw
    for n in range(N):
        if abs(centered(n)) != ell:
            denominator = scale(sub(c(n), c(ell)), ell)
            numerator = mul(si(ell), sub(one, c(n*ell)))
            assert mul(iDw[n], denominator) == numerator
            assert denominator != zero
    assert iDw[0] == iDw[ell] == iDw[-ell] == zero
    assert iDw[q] != zero
    iv = [sub(x, y) for x, y in zip(iw, iDw)]
    assert D(iv) == [scale(x, -1) for x in iv]
    assert iv[0] == zero and iv[q] == scale(iDw[q], -1)

    # Independent floating evaluations only for signs/illustration.
    def ev(a):
        return sum(float(v) * complex(cos(2*pi*j/N), __import__('math').sin(2*pi*j/N))
                   for j, v in enumerate(a))
    assert min(ev(G[n]).real for n in support(G)) > 0
    assert min(ev(H[n]).real for n in support(H)) > 0
    f = [(ev(x)/(-ev(iDw[q]))).real for x in iv]
    assert min(f[n] for n in range(N) if abs(centered(n)) >= ell) > -1e-10
    assert f[ell-1] < 0 and abs(f[q]-1) < 1e-10
    print(f'ell={ell}, N={N}, degree={degree}: exact assertions PASS; '
          f'|supp G|={len(support(G))}, |supp H|={len(support(H))}, '
          f'|supp DH|={len(support(DH))}, H(q)~{ev(H[q]).real:.12f}, '
          f'f*(ell-1)~{f[ell-1]:.12f}', flush=True)


if __name__ == '__main__':
    start = process_time()
    for ell, prime in [(3,3), (5,5), (7,7), (9,3)]:
        check(ell, prime)
    print(f'Single-process CPU time: {process_time()-start:.2f}s')

"""Independent exact full-path solver from Eq.(2), using primal fused blocks.

No claimant module is imported. For each {-1,0,1} jump pattern, each zero
run is a constant block with level mean(y)+lambda*(q_right-q_left)/length.
The cumulative stationarity residual U_i=sum_{j<=i}(x_j-y_j) must equal
lambda*alpha_i*sign(jump) at a jump, and lie in that interval at a fusion.
All conditions are affine rational inequalities; intersect them exactly.
"""
from fractions import Fraction as F
from itertools import product


def solve(y, alpha):
    y, alpha = list(map(F, y)), list(map(F, alpha))
    n = len(y)
    assert len(alpha) == n - 1 and all(v > 0 for v in alpha)
    sy = [F(0)]
    for v in y:
        sy.append(sy[-1] + v)
    aw = [F(0)] + alpha + [F(0)]
    cache = {}
    for l in range(n):
        for r in range(l+1, n+1):
            for sl, sr in product((-1, 0, 1), repeat=2):
                cache[l, r, sl, sr] = ((sy[r]-sy[l])/(r-l),
                                      (aw[r]*sr-aw[l]*sl)/(r-l))
    answers = []
    for s in product((-1, 0, 1), repeat=n-1):
        cuts = [0] + [i+1 for i, v in enumerate(s) if v] + [n]
        a, b = [F(0)]*n, [F(0)]*n
        for l, r in zip(cuts, cuts[1:]):
            av, bv = cache[l, r, s[l-1] if l else 0,
                           s[r-1] if r<n else 0]
            a[l:r], b[l:r] = [av]*(r-l), [bv]*(r-l)
        lo, hi = F(0), None
        valid = True
        # c + lambda*d >= 0, strictly inside the interval for a jump.
        cond = []
        for i, si in enumerate(s):
            if si:
                c, d = si*(a[i+1]-a[i]), si*(b[i+1]-b[i])
                if not c and not d:
                    valid = False
                    break
                cond.append((c, d))
        if not valid:
            continue
        ua, ub = F(0), F(0)
        for i in range(n-1):
            ua += a[i]-y[i]
            ub += b[i]
            if s[i]:
                assert ua == 0 and ub == alpha[i]*s[i]
            else:
                cond.extend(((-ua, alpha[i]-ub), (ua, alpha[i]+ub)))
        for c, d in cond:
            if d > 0:
                lo = max(lo, -c/d)
            elif d < 0:
                t = -c/d
                hi = t if hi is None else min(hi, t)
            elif c < 0:
                valid = False
                break
            if hi is not None and hi <= lo:
                valid = False
                break
        if valid:
            answers.append(dict(lo=lo, hi=hi, a=a, b=b))
    answers.sort(key=lambda p: p['lo'])
    assert answers and answers[0]['lo'] == 0
    assert answers[-1]['hi'] is None
    for p, q in zip(answers, answers[1:]):
        assert p['hi'] == q['lo'], ('coverage/overlap', p, q)
        t = q['lo']
        assert [a+t*b for a,b in zip(p['a'], p['b'])] == [a+t*b for a,b in zip(q['a'], q['b'])]
        assert p['b'] != q['b'], 'non-maximal affine pieces'
    assert all(v == 0 for v in answers[-1]['b'])
    assert all(v == sy[-1]/n for v in answers[-1]['a'])
    return answers


def good_indices(alpha):
    a = [F(0)] + list(map(F, alpha)) + [F(0)]
    n = len(a)-1
    # Direct all-chord definition, no hull algorithm.
    return {i for i in range(n+1) if all(
        (r-l)*a[i] >= (r-i)*a[l] + (i-l)*a[r]
        for l in range(i) for r in range(i+1,n+1))}


def analyze(y, alpha, pieces):
    y, alpha = list(map(F,y)), list(map(F,alpha))
    n = len(y)
    good = good_indices(alpha)
    k, g = n+1-len(good), len(good)
    active = []
    for p in pieces:
        ua, ub = F(0), F(0)
        act = {0:0, n:0}
        for i in range(n-1):
            ua += p['a'][i]-y[i]
            ub += p['b'][i]
            if ua == 0 and abs(ub) == alpha[i]:
                act[i+1] = 1 if ub > 0 else -1
        active.append(act)
    freed = set()
    good_return = []
    charges = {}
    unfusions = 0
    for idx, act in enumerate(active):
        good_return.extend(sorted(freed & set(act)))
        freed.update(good-set(act))
        if idx == 0:
            prev_piece = pieces[idx]
            continue
        prev = active[idx-1]
        for j in set(prev)^set(act):
            free_side = act if j in prev else prev
            l = max(i for i in free_side if i<j)
            r = min(i for i in free_side if i>j)
            charges.setdefault((l,r),set()).add(pieces[idx]['lo'])
        # A primal jump is a saturated dual contact with nonzero multiplier.
        for i in range(n-1):
            waszero = prev_piece['a'][i+1] == prev_piece['a'][i] and prev_piece['b'][i+1] == prev_piece['b'][i]
            iszero = pieces[idx]['a'][i+1] == pieces[idx]['a'][i] and pieces[idx]['b'][i+1] == pieces[idx]['b'][i]
            unfusions += int(waszero and not iszero)
        prev_piece = pieces[idx]
    P = 2*g-3+g*k+k*(k-1)//2
    bound1, bound2 = 3**k*(g-1), 1+8*P
    assert not good_return, ('good contact returned', good_return)
    assert len(pieces) <= min(bound1,bound2), ('bound violation',n,k,len(pieces))
    assert len(charges) <= P
    assert all(len(v)<=8 for v in charges.values())
    return dict(n=n,k=k,g=g,T=len(pieces),bound1=bound1,bound2=bound2,
                good=sorted(good),unfusions=unfusions,
                charged_pairs=len(charges),max_charges=max(map(len,charges.values()),default=0))


def encode(pieces):
    return [dict(lo=str(p['lo']),hi=None if p['hi'] is None else str(p['hi']),
                 a=list(map(str,p['a'])),b=list(map(str,p['b']))) for p in pieces]

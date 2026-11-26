"""Independent exact referee for the 312 formula. Run with ordinary Python 3."""
import gzip
import json
import os
import re
import signal
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product

cache = lru_cache(maxsize=None)


def equal(label, actual, expected):
    if actual != expected:
        raise AssertionError((label, actual, expected))


def paper():
    path = os.path.join(os.path.dirname(__file__), 'inputs', '2610.07442v1.tex.json.gz')
    with gzip.open(path, 'rt', encoding='utf8') as file:
        source, = [body for name, body in json.load(file) if name == 'Extended_avoidance.tex']
    lines = source.splitlines()
    exact = {
        69: r'\newcommand{\Sch}[1]{\mathrm{Sch}_{#1}}',
        70: r'\newcommand{\s}[4]{S^{#1}_{{#2},{#3},{#4}}}',
        86: r'\title[Extended avoidance]{Pattern avoidance in alternating sign rectangles~I: Extended avoidance}',
        88: r'\author[H. H\"ongesberg]{Hans H\"ongesberg}',
        93: r'\author[M. Konvalinka]{Matja\v{z} Konvalinka}',
        97: r'\author[S. Linusson]{Svante Linusson}',
        204: r'\item the nonzero entries alternate in each row and column;',
        205: r'\item if a row contains a nonzero entry, then its leftmost and rightmost nonzero entries are $1$;',
        206: r'\item if a column contains a nonzero entry, then its topmost nonzero entry is $1$.',
        447: r'\begin{prop}\label{lem:r=d}',
        448: r'For $1\le r\le k$, we have',
        450: r'\s{312}{r}{k}{r}=\s{312}{r}{k-1}{r}+\s{312}{r-1}{k-1}{r-1}+\sum_{i=2}^{r} \Sch{i-2}\cdot \s{312}{r+1-i}{k+1-i}{r+1-i}.',
        520: r'\begin{prop}\label{lem:k=d}',
        521: r'For $1\le k<r$, we have',
        523: r'\s{312}{r}{k}{k}=\sum_{j=0}^k \s{312}{j}{k}{j}\binom{r-j-1}{k-j}.',
        555: r'\begin{thm}\label{lem:general}',
        556: r'For $d< r, k$ we have',
        558: r'\s{312}{r}{k}{d}=\s{312}{r}{k-1}{d}+\s{312}{r-1}{k-1}{d-1}+\sum_{i=2}^d \Sch{i-2}\cdot \left (\s{312}{r+1-i}{k+1-i}{d+1-i}-\binom{r-i}{d+1-i} \right ).',
        568: r'\begin{conj}\label{conj:312-formula}',
        569: r'For integers $d \leq r,k$, we have',
        570: r'\begin{multline}\label{eq:conj312}',
        571: r'\s{312}{r}{k}{d} = \sum_{i=1}^{d} 2^{i-1} \binom{k}{i} \left( \binom{r-2}{d-i} - 2\binom{r-2}{d-i-2} \right) + \binom{r}{d}\\',
        572: r'+ \sum_{i \geq 0 }^{} C_{2i} \binom{r-1+2i}{d-1-2i} + 2 \sum_{i=1}^{d} (-1)^i \binom{r}{d-i},',
        574: r'where $C_n = \frac{1}{n+1} \binom{2n}{n}$ denotes the $n$th Catalan number.',
    }
    for n, value in exact.items():
        equal(('source', n), lines[n-1].strip(), value)
    for n, tokens in {
        202: [r'\{-1,0,1\}'], 213: ['rows and columns each sum to $1$'],
        219: ['downwards and to the right'], 268: [r'M_{i_1,j_{\pi(1)}}', r'j_1 < \dots < j_n'],
        272: ['there exists an extension'], 279: [r'\asm{n}{312}', r'\Sch{n-1}'],
        281: [r'\Sch{0}=1', r'\Sch{1}=2', r'\frac{1-x-\sqrt{1-6x+x^2}}{2x}'],
        282: [r'\Sch{-1}=1'], 407: [r'r < d', r'k < d', r'r,k\ge d\ge 0', r'\s{\pi}{r}{k}{0} = 1'],
        412: [r'\s{\pi}{0}{k}{0} = 1 = \s{\pi}{r}{0}{0}', r'\s{\pi}{n}{n}{n} = \Sch{n-1}'],
        507: [r'\sum_{i=1}^k', r'\Sch{-1}=1'], 578: ['F(1,k,1)=k', 'F(r,1,1)=r'],
    }.items():
        for token in tokens:
            equal(('source', n, token), token in lines[n-1], True)
    # Reconstruct the printed numbering from declarations and the actual section.
    equal('counter', lines[32], r'\newtheorem{thm}{Theorem}[section]')
    envs = re.findall(r'\\newtheorem\{(\w+)\}\[thm\]', source) + ['thm']
    numbering = []
    section = ordinal = 0
    for n, line in enumerate(lines[:575], 1):
        if line.startswith(r'\section{'):
            section += 1
            ordinal = 0
        begin = re.match(r'\s*\\begin\{(\w+)\}', line)
        if begin and begin[1] in envs:
            ordinal += 1
            if n >= 416:
                numbering.append((n, section, ordinal))
    equal('section numbering', numbering, [(416,4,1),(447,4,2),(520,4,3),(555,4,4),(568,4,5)])
    table = {}
    for line in lines[1099:1105]:
        row, *cells = line.strip().rstrip('\\').split('&')
        for k, cell in enumerate(cells):
            if cell.strip():
                table[int(row), k] = int(cell)
    print('Raw source lines', len(lines), 'Table 2 populated cells', len(table))
    return table


@cache
def choose(n, m):
    if m < 0:
        return 0
    value = 1
    for i in range(1, m+1):
        value = value * (n+1-i) // i
    return value


@cache
def catalan(n):
    return choose(2*n, n) // (n+1)


def pieces(r, k, d, mutant=''):
    a = b = c = e = 0
    for i in range(1, d+1):
        p = choose(r-2, d-i)
        if mutant == 'negative top zero' and r < 2:
            p = 0
        q = choose(r-2, d-i-2)
        a += (3 if mutant == 'power base 3' else 2)**(i-1) * choose(k, i) * (
            p - (1 if mutant == 'single subtraction' else 2)*q)
        e += (-1)**(i + (mutant == 'reversed parity')) * choose(r, d-i)
    b = choose(r, d) * (2 if mutant == 'double free binomial' else 1)
    for i in range((d+1)//2):
        c += catalan(i if mutant == 'ordinary Catalan index' else 2*i) * choose(r-1+2*i, d-1-2*i)
    return a, b, c, (1 if mutant == 'single alternating sum' else 2)*e


def formula(r, k, d, mutant=''):
    return sum(pieces(r,k,d,mutant))


@cache
def paths(x,y):
    """Large Schroeder walks from the origin, never above the diagonal."""
    if y < 0 or y > x:
        return 0
    if x == y == 0:
        return 1
    return paths(x-1,y) + paths(x,y-1) + paths(x-1,y-1)


def sch(n):
    if n < 0:
        raise ValueError(n)
    return paths(n,n)


@cache
def pascal(n,m):
    if n < 0:
        raise ValueError(n)
    if m < 0 or m > n:
        return 0
    if m == 0 or m == n:
        return 1
    return pascal(n-1,m) + pascal(n-1,m-1)


def recurrence(get,r,k,d):
    if d == k < r:
        return sum(get(j,k,j)*pascal(r-j-1,k-j) for j in range(k+1))
    total = get(r,k-1,d) + get(r-1,k-1,d-1)
    for i in range(2,d+1):
        tail = get(r+1-i,k+1-i,d+1-i)
        if d < r:
            tail -= pascal(r-i,d+1-i)
        total += sch(i-2)*tail
    return total


@cache
def count(r,k,d):
    if d == 0:
        return 1
    if d > min(r,k):
        return 0
    return recurrence(count,r,k,d)  # includes R1 on diagonal, with off-cone zero


def alternating(line, ends_plus):
    nonzero = [x for x in line if x]
    return not nonzero or (nonzero[0] == 1 and
                           (not ends_plus or nonzero[-1] == 1) and
                           all(a == -b for a,b in zip(nonzero, nonzero[1:])))


def rectangles(r,k):
    rows = [row for row in product((-1,0,1), repeat=k) if alternating(row, True)]

    def grow(matrix, sums):
        if len(matrix) == r:
            yield matrix
            return
        for row in rows:
            after = tuple(a+b for a,b in zip(sums,row))
            if all(x in (0,1) for x in after):
                yield from grow(matrix+(row,),after)

    yield from grow((),(0,)*k)


def completion(matrix,k):
    empty = [i for i,row in enumerate(matrix) if not any(row)]
    deficient = [j for j in reversed(range(k)) if sum(row[j] for row in matrix) == 0]
    n = k+len(empty)
    square = [list(row)+[0]*len(empty) for row in matrix]
    for t,i in enumerate(empty):
        square[i][k+t] = 1
    for j in deficient:
        row = [0]*n
        row[j] = 1
        square.append(row)
    equal('square shape',len(square),n)
    for row in list(square)+list(zip(*square)):
        equal('square ASM axis', (sum(row),alternating(row,True)), (1,True))
    return square


def pattern(square):
    positive = [[j for j,entry in enumerate(row) if entry == 1] for row in square]
    for a,b,c in combinations(range(len(square)),3):
        for high in positive[a]:
            for low in positive[b]:
                for mid in positive[c]:
                    if low < mid < high:
                        return ((a,high),(b,low),(c,mid))
    return None


def objects():
    # Project actual order-five ASMs without using the canonical construction.
    projected = set()
    asm_total = asm_avoiding = 0
    for square in rectangles(5,5):
        if not all(sum(axis) == 1 for axis in (*square,*zip(*square))):
            continue
        asm_total += 1
        if pattern(square) is None:
            asm_avoiding += 1
            for r,k in product(range(6),repeat=2):
                corner = tuple(row[:k] for row in square[:r])
                projected.add((r,k,corner))
    print('Order-five ASMs',asm_total,'avoiding',asm_avoiding)
    totals = {}
    projection_checks = 0
    raw = accepted = internally_avoiding_rejects = forced = 0
    for r,k in product(range(6),repeat=2):
        counts = [0]*(min(r,k)+1)
        for mat in rectangles(r,k):
            sq = completion(mat,k)
            witness = pattern(sq)
            d = sum(any(row) for row in mat)
            if len(sq) <= 5:
                equal(('order-five ASM projection',r,k,mat),
                      (r,k,mat) in projected,witness is None)
                projection_checks += 1
            if r*k:
                raw += 1
            if witness is None:
                counts[d] += 1
                accepted += int(bool(r*k))
            else:
                # The same internal entries and the forced exterior ones
                # in these rows or columns witness 312 in ANY completion.
                for pos,(i,j) in enumerate(witness):
                    if j >= k:
                        equal('forced right', (pos,any(mat[i])), (0,False))
                    if i >= r:
                        equal('forced bottom',(pos,sum(row[j] for row in mat)), (2,0))
                forced += 1
                if pattern(mat) is None:
                    internally_avoiding_rejects += 1  # naive corner-only test would accept
        for d,n in enumerate(counts):
            totals[r,k,d] = n
            equal(('ASR vs F',r,k,d),n,formula(r,k,d))
    for (r,k,d), n in totals.items():
        if d:
            def lookup(a,b,c):
                return 0 if c > min(a,b) else totals[a,b,c]
            equal(('ASR vs printed recurrence',r,k,d),n,recurrence(lookup,r,k,d))
    print('Positive dimensions: ASRs',raw,'extendably avoiding',accepted,'rejected',forced,
          'of which avoid internally',internally_avoiding_rejects)
    print('Candidates cross-checked against actual order-five corners', projection_checks)
    print('Small triples',len(totals),'5x5 by d',[totals[5,5,d] for d in range(6)])
    return totals


def numbers(table, small):
    tested = 0
    for r,k in product(range(51),repeat=2):
        for d in range(min(r,k)+1):
            equal(('grid',r,k,d),count(r,k,d),formula(r,k,d))
            tested += 1
    for n in range(1,51):
        equal(('diagonal',n),count(n,n,n),sch(n-1))
        equal(('outside by one',n),formula(n,n-1,n),0)
    for (r,k),value in table.items():
        equal(('Table 2',r,k),count(r,k,r),value)
    print('Grid through 50',tested,'mismatches 0')
    for triple in ((51,52,50),(67,58,19),(60,91,60),(77,53,53),(64,64,64),(99,1,1)):
        value = count(*triple)
        equal(('larger',triple),value,formula(*triple))
        print('Larger',triple,value)
    for mutation in ('negative top zero','power base 3','single subtraction','reversed parity',
                     'double free binomial','ordinary Catalan index','single alternating sum'):
        for point,expected in sorted(small.items()):
            actual = formula(*point, mutation)
            if actual != expected:
                print('Mutation', mutation, point, 'observed',actual,'expected',expected)
                break
        else:
            raise AssertionError(('surviving mutation',mutation))


# Truncated series in Q[[z]], with extra coefficients for shifts and derivatives.
ORDER = 36
SIZE = 41


class Series:
    def __init__(self, coefficients):
        values = tuple(Q(c) for c in coefficients)
        self.c = (values + (Q(0),)*SIZE)[:SIZE]

    def __add__(self, other):
        other = series(other)
        return Series(a+b for a,b in zip(self.c,other.c))

    __radd__ = __add__

    def __neg__(self):
        return Series(-a for a in self.c)

    def __sub__(self, other):
        return self + (-series(other))

    def __rsub__(self, other):
        return series(other) + (-self)

    def __mul__(self, other):
        if isinstance(other,(int,Q)):
            return Series(a*other for a in self.c)
        out = [Q(0)]*SIZE
        for i,a in enumerate(self.c):
            if a:
                for j,b in enumerate(other.c[:SIZE-i]):
                    if b:
                        out[i+j] += a*b
        return Series(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            return self.inverse()**(-n)
        if n == 0:
            return series(1)
        if n == 1:
            return self
        half = self**(n//2)
        square = half*half
        return square*self if n%2 else square

    def inverse(self):
        out = [1/self.c[0]]
        for n in range(1,SIZE):
            out.append(-sum(self.c[i]*out[n-i] for i in range(1,n+1))/self.c[0])
        return Series(out)

    def sqrt(self):
        equal('principal square root input',self.c[0],1)
        out = [Q(1)]
        for n in range(1,SIZE):
            out.append((self.c[n]-sum(out[i]*out[n-i] for i in range(1,n)))/2)
        return Series(out)

    def at(self, inner):
        equal('composition valuation', inner.c[0], 0)
        value = series(0)
        for c in reversed(self.c):
            value = value*inner+c
        return value

    def derivative(self):
        return Series(i*self.c[i] for i in range(1,SIZE))

    def shift(self, n):
        if n >= 0:
            return Series((0,)*n + self.c)
        equal('division by monomial',any(self.c[:-n]),False)
        return Series(self.c[-n:])


def series(x):
    return x if isinstance(x,Series) else Series((x,))


def same(label, left, right):
    for n,(a,b) in enumerate(zip(series(left).c[:ORDER+1], series(right).c)):
        equal((label,'degree',n), a,b)


z = Series((0,1))
one = series(1)
A = 1+z
B = 1+2*z
D = (1-4*z-4*z*z).sqrt()
E = (1-6*z+z*z).sqrt()
H = (3+2*z-D)*Q(1,4)
P = (1-2*z*z)*Q(1,2)


@cache
def linear_power(scale, exponent):
    return (1+scale*z)**exponent


@cache
def phi(r,k):
    return linear_power(1,r-2)*(P*linear_power(2,k)+H)


def series_checks():
    C = Series(catalan(n) for n in range(SIZE))
    S = Series(sch(n) for n in range(SIZE))
    u = z*A
    even = Series(catalan(n) if n%2 == 0 else 0 for n in range(SIZE))
    same('Catalan recurrence', C,1+z*C*C)
    same('Catalan radical', C,(1-(1-4*z).sqrt()).shift(-1)*Q(1,2))
    same('even part', even,(C+C.at(-z))*Q(1,2))
    same('even radical',even,((1+4*z).sqrt()-(1-4*z).sqrt()).shift(-1)*Q(1,4))
    same('positive square', (1+4*u).sqrt(), B)
    same('D branch', D*D,1-4*u)
    half_binom = [Q(1)]
    for n in range(1,SIZE):
        half_binom.append(half_binom[-1]*(Q(1,2)-n+1)/n)
    same('half-binomial root branch',Series(half_binom).at(-4*u),D)
    same('1.1', z*even.at(u),(B-D)*A.inverse()*Q(1,4))
    for r,k in ((0,0),(0,9),(1,0),(1,21),(2,0),(2,13),(18,40),(42,37)):
        direct = [pieces(r,k,d) for d in range(SIZE)]
        terms = (linear_power(1,r-2)*P*(linear_power(2,k)-1),
                 A**r, A**(r-1)*z*even.at(u), -2*z*A**(r-1))
        for i,term in enumerate(terms):
            same(('four pieces',r,k,i),term,Series(row[i] for row in direct))
        same(('Lemma 1',r,k),sum(terms),phi(r,k))

    a = z*(A*B).inverse()
    b = z*A.inverse()
    Sa,Sb = S.at(a),S.at(b)
    same('Schroeder radical, divided',S,(1-z-E).shift(-1)*Q(1,2))
    same('Schroeder quadratic',z*S*S-(1-z)*S+1,0)
    same('a discriminant',1-6*a+a*a,((1-2*z*z)*(A*B).inverse())**2)
    same('a principal branch',(1-6*a+a*a).sqrt(),(1-2*z*z)*(A*B).inverse())
    same('2.1',Sa,B)
    same('b discriminant',1-6*b+b*b,(1-4*z-4*z*z)*A**(-2))
    same('b principal branch',(1-6*b+b*b).sqrt(),D*A.inverse())
    same('2.2',Sb,(1-D).shift(-1)*Q(1,2))
    same('2.3',(H-A)*Sb,-H)
    for r,k in ((-4,-3),(0,0),(1,1),(2,5),(5,2),(39,39),(40,44)):
        tail = series(0)
        for m in range(SIZE-1):
            bracket = phi(r-1-m,k-1-m)-linear_power(1,r-2-m)
            equal(('3.1 endpoint',r,k,m),bracket.c[0],0)
            tail += bracket.shift(m+1)*sch(m)
        same(('regroup tail',r,k),tail,
             z*A**(r-3)*(P*B**(k-1)*Sa+(H-A)*Sb))
        diff = phi(r,k)-phi(r,k-1)
        same(('3.3',r,k),diff,2*z*P*A**(r-2)*B**(k-1))
        same(('3.1',r,k),diff,z*phi(r-1,k-1)+tail)

    w = z*(1-z).inverse()
    inv_a = (S-1)*Q(1,2)
    same('inverse b', b.at(w),z)
    same('second residue discriminant',1-4*w-4*w*w,(1-6*z+z*z)*(1-z)**(-2))
    same('second residue Jacobian',w.derivative(),(1-z)**(-2))
    same('second residue transformed unit',(1-z)*H.at(w),(1+z*S)*Q(1,2))
    same('4.3',a.at(inv_a),z)
    same('inverse a, opposite composition',inv_a.at(a),z)
    AU,BU = 1+inv_a,1+2*inv_a
    same('first residue Jacobian',(1-2*inv_a**2)*inv_a.derivative(),(AU*BU)**2)
    same('conjugate product',(1+z-E)*(1+z+E),8*z)
    same('first transformed unit k=r-1',(2*AU).inverse(),(1-z*S)*Q(1,2))
    same('first transformed unit k=r',BU*(2*AU).inverse(),(1+z*S)*Q(1,2))

    # A Laurent monomial t^m under t=z*g has valuation m. Store its
    # regular factor after pulling z^m out, and read degree -1-m.
    for subst in (w,inv_a,-2*z+3*z*z-z**3):
        g = subst.shift(-1)
        dg = subst.derivative()
        for m in range(-ORDER-1,4):
            pullback = g**m*dg
            residue = pullback.c[-1-m] if m < 0 else Q(0)
            equal(('4.1 monomial',m),residue,int(m == -1))
            if m == -1:
                same('log derivative regular factor',pullback,1+z*g.derivative()*g.inverse())
            else:
                power = g**(m+1)
                same(('Laurent derivative',m),pullback,power+z*power.derivative()*Q(1,m+1))

    # Compare the full regular factors after pulling out the pole z^(-r-1).
    for r in (1,2,17,36):
        left = (1+w)**(r-2)*H.at(w)*w.shift(-1)**(-r-1)*w.derivative()
        same(('second residue integrand',r),left,(1-z)*H.at(w))
        for k in (r-1,r):
            left = (P.at(inv_a)*AU**(r-2)*BU**k *
                    inv_a.shift(-1)**(-r-1)*inv_a.derivative())
            same(('first residue integrand',r,k),left,BU**(k-r+1)*(2*AU).inverse())

    for r in range(1,ORDER+1):
        expected = Q(sch(r-1),2)
        equal(('second diagonal half',r),(A**(r-2)*H).c[r], expected)
        for k in (r-1,r):
            sign = 1 if k == r else -1
            equal(('first diagonal half',r,k),(A**(r-2)*P*B**k).c[r], sign*expected)
            equal(('diagonal recombination',r,k),phi(r,k).c[r], (1+sign)*expected)

    # Universal linear map tested on an entire truncated monomial basis.
    for k in range(1,ORDER+1):
        for r in (k+1, k+11):
            for n in range(k+1):
                M = k-n
                before = after = Q(0)
                for m in range(M+1):
                    factor1 = linear_power(1,n-2+m).c[m]
                    factor2 = linear_power(1,r-n-1-m).c[M-m]
                    neg1 = (-1)**m*linear_power(1,1-n).c[m]
                    neg2 = (-1)**(M-m)*linear_power(1,M-r+n).c[M-m]
                    equal(('5.2',r,k,n,m),(factor1,factor2),(neg1,neg2))
                    before += factor1*factor2
                    after += neg1*neg2
                equal(('5.3',r,k,n),after,(-1)**M*linear_power(1,M-r+1).c[M])
                equal(('5.1',r,k,n),before,linear_power(1,r-2).c[M])
    print('Formal series and Laurent checks through degree',ORDER,'mismatches 0')


if __name__ == '__main__':
    # No children or worker threads. Limit a replay to ten wall-clock minutes.
    signal.alarm(600)
    printed = paper()
    small_counts = objects()
    numbers(printed,small_counts)
    series_checks()
    print('All exact comparisons passed.')

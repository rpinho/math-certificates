"""Separate implementation, same agent. Implements the clauses in PROOFS.md."""
import argparse
import itertools


def formula(n, k, omitted, fan=False):
    vertices = tuple(range(n))
    edges = tuple(itertools.combinations(vertices, 2))
    less = {pair: index for index, pair in enumerate(itertools.permutations(edges, 2), 1)}
    representatives = {
        pair: index
        for index, pair in enumerate(itertools.permutations(vertices, 2), len(less) + 1)
    }
    clauses = set()

    def put(name, *clause):
        if name not in omitted:
            clauses.add(tuple(sorted(clause)))

    def distance(x, y):
        return tuple(sorted((x, y)))

    def comparison(x, y, z, w):
        return less[distance(x, y), distance(z, w)]

    for u, v in itertools.combinations(edges, 2):
        put("ASYM", -less[u, v], -less[v, u])
    for a, b, c in itertools.combinations(edges, 3):
        for x, y, z in ((a, b, c), (a, c, b), (b, a, c),
                        (b, c, a), (c, a, b), (c, b, a)):
            put("TRANS", -less[z, x], less[y, x], less[z, y])

    for vertex in vertices:
        others = [w for w in vertices if w != vertex]
        for rank, w in enumerate(others):
            mark = representatives[vertex, w]
            directions = [(comparison(vertex, w, vertex, p),
                           comparison(vertex, p, vertex, w)) for p in others[:rank]]
            for inferior, superior in directions:
                put("FIRST", inferior, superior, -mark)
            for selector in range(1 << rank):
                put("FIRST", mark, *(-pair[(selector >> j) & 1]
                                     for j, pair in enumerate(directions)))
        for group in itertools.combinations(others, k + 1):
            put("BOUND", *(-representatives[vertex, w] for w in group))

    for a, b, c, d in itertools.combinations(vertices, 4):
        for u, v, w, x in ((a, b, c, d), (c, d, a, b), (a, d, b, c), (b, c, a, d)):
            put("CROSS", comparison(u, v, a, c), comparison(w, x, b, d))
        for v, x, y, z in ((a, b, c, d), (b, c, d, a), (c, d, a, b), (d, a, b, c)):
            put("BISECTOR", comparison(y, z, v, y), comparison(v, x, x, z))
            for p, q in ((x, y), (y, z)):
                put("CAP", comparison(v, x, v, y), comparison(v, z, v, x),
                    comparison(v, x, v, z), comparison(p, q, x, z))
    for index in range(1, n):
        put("SYM", -comparison(index, (index + 1) % n, 0, 1))
    if fan:
        for vertex in vertices:
            chain = tuple((vertex+offset) % n for offset in range(1,n))
            for a,b,c,d in itertools.combinations(chain,4):
                put("FAN", comparison(a,b,vertex,a), comparison(a,b,vertex,b),
                    comparison(b,c,vertex,b), comparison(b,c,vertex,c),
                    comparison(c,d,vertex,c), comparison(c,d,vertex,d))
    return len(less) + len(representatives), sorted(clauses)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("k", type=int)
    parser.add_argument("target")
    parser.add_argument("--omit", action="append", default=[])
    parser.add_argument("--fan", action="store_true")
    args = parser.parse_args()
    variables, clauses = formula(args.n, args.k, args.omit, args.fan)
    with open(args.target, "w") as output:
        print("p", "cnf", variables, len(clauses), file=output)
        for literals in clauses:
            print(*literals, 0, file=output)

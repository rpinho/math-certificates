"""Independent finite-graph referee. Run from the referee directory with Python 3."""
import argparse
import copy
import hashlib
import itertools
import json
import re
from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
def factorial(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r
from pathlib import Path

DIGEST = "716b2577a500e1bf0bff8622f4902c6070885ab6f443ccb6658b670ef92b7805"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def vertices(bits):
    while bits:
        bit = bits & -bits
        yield bit.bit_length() - 1
        bits -= bit


def adjacency(n, edges):
    require(type(n) is int and n >= 0, "invalid order")
    rows = [0] * n
    for pair in edges:
        require(len(pair) == 2, "invalid pair")
        u, v = pair
        require(all(type(i) is int and 0 <= i < n for i in pair), "invalid vertex")
        require(u != v, "loop")
        require(not rows[u] & (1 << v), "parallel edge")
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return tuple(rows)


def edges_of(g):
    return [(u, v) for u, row in enumerate(g) for v in vertices(row) if u < v]


def component(g, mask):
    wave = mask & -mask
    seen = wave
    while wave:
        neighbors = 0
        for v in vertices(wave):
            neighbors |= g[v]
        wave = neighbors & mask & ~seen
        seen |= wave
    return seen


def topology(g):
    edges = edges_of(g)
    girth = None
    # For each edge find the shortest alternate path between its ends.
    for u, v in edges:
        queue = deque([(u, 0)])
        seen = {u}
        while queue:
            w, dist = queue.popleft()
            if w == v:
                girth = min(girth or len(g) + 1, dist + 1)
                break
            for x in vertices(g[w]):
                if (w, x) == (u, v) or x in seen:
                    continue
                seen.add(x)
                queue.append((x, dist + 1))
    full = (1 << len(g)) - 1
    connected = bool(g) and component(g, full) == full
    degrees = Counter(row.bit_count() for row in g)
    return dict(n=len(g), num_edges=len(edges), connected=connected,
                max_degree=max(degrees, default=0), is_tree=connected and girth is None,
                girth=girth, degree_counts=dict(sorted(degrees.items())))


def static_hist(g):
    # Visit each independent set once in increasing label order. An
    # independent set is maximal exactly when its closed neighborhoods cover V.
    full = (1 << len(g)) - 1
    counts = Counter()

    def visit(eligible, dominated, k):
        if dominated == full:
            counts[k] += 1
            return
        while eligible:
            bit = eligible & -eligible
            eligible -= bit
            v = bit.bit_length() - 1
            visit(eligible & ~g[v], dominated | bit | g[v], k + 1)
    visit(full, 0, 0)
    return dict(sorted(counts.items()))


def sequential(g):
    @lru_cache(None)
    def solve(mask):
        if not mask:
            return {0: F(1)}
        part = component(g, mask)
        sums = Counter()
        if part != mask:
            for a, p in solve(part).items():
                for b, q in solve(mask ^ part).items():
                    sums[a+b] += p*q
        else:
            for v in vertices(mask):
                child = mask & ~(g[v] | (1 << v))
                for k, p in solve(child).items():
                    sums[k+1] += p
            sums = {k: p / mask.bit_count() for k, p in sums.items()}
        return sums

    pmf = dict(sorted(solve((1 << len(g))-1).items()))
    solve.cache_clear()
    return pmf


def cdf(pmf, n):
    return tuple(itertools.accumulate(pmf.get(k, F(0)) for k in range(n+1)))


@dataclass
class Law:
    hist: dict
    seq: dict
    stat: dict
    fs: tuple  # sequential CDF, k=0,...,n
    ft: tuple  # static CDF
    positive: tuple
    negative: tuple

    @classmethod
    def compute(cls, g):
        hist, seq = static_hist(g), sequential(g)
        total = sum(hist.values())
        stat = {k: F(v,total) for k,v in hist.items()}
        require(set(stat) == set(seq), "support mismatch")
        require(sum(stat.values()) == sum(seq.values()) == 1, "invalid mass")
        fs, ft = cdf(seq, len(g)), cdf(stat, len(g))
        return cls(hist, seq, stat, fs, ft,
                   tuple(k for k in range(len(fs)) if fs[k] > ft[k]),
                   tuple(k for k in range(len(fs)) if fs[k] < ft[k]))

    def summary(self):
        return dict(total_mis=sum(self.hist.values()), hist=self.hist,
                    seq=self.seq, stat=self.stat, seq_cdf=self.fs, stat_cdf=self.ft,
                    mean_seq=sum(k*p for k,p in self.seq.items()),
                    mean_stat=sum(k*p for k,p in self.stat.items()),
                    k_seq_cdf_greater=self.positive, k_seq_cdf_less=self.negative)


def brute(g):
    # Deliberately use edges and Python sets, distinct from bit-mask recursion.
    adj = [set(vertices(a)) for a in g]
    hits = Counter()
    outcomes = set()
    for order in itertools.permutations(range(len(g))):
        occupied = set()
        for v in order:
            if not (occupied & adj[v]):
                occupied.add(v)
        hits[len(occupied)] += 1
        outcomes.add(frozenset(occupied))
    return ({k: F(x, factorial(len(g))) for k,x in hits.items()},
            Counter(map(len, outcomes)))


def paper_sum_over_orders(g):
    """TeX eqs. 82, 88 evaluated per final MIS, independently of residual graph DP."""
    n = len(g)
    full = (1 << n) - 1
    contributions = {}
    for target in range(1 << n):
        selected = tuple(vertices(target))
        if any(g[v] & target for v in selected):
            continue
        covered = target
        for v in selected:
            covered |= g[v]
        if covered != full:
            continue
        # Prefix probabilities with the same accepted subset can be added.
        prefix = {0: F(1)}
        for _ in selected:
            next_prefix = Counter()
            for used, prob in prefix.items():
                blocked = used
                for v in vertices(used):
                    blocked |= g[v]
                prob_per_vertex = prob / (n - blocked.bit_count())
                for v in vertices(target ^ used):
                    next_prefix[used | (1<<v)] += prob_per_vertex
            prefix = next_prefix
        contributions[target] = prefix[target]
    return contributions


def subcubic_violation(g, law):
    return max((a.bit_count() for a in g), default=0) <= 3 and bool(law.positive)


def controls():
    inputs = [
        ("P3", 3, [(0,1),(1,2)]),
        ("P4", 4, [(0,1),(1,2),(2,3)]),
        ("K3", 3, [(0,1),(1,2),(0,2)]),
        ("7-vertex tree", 7, [(0,1),(0,2),(0,3),(1,4),(2,5),(5,6)]),
        ("paper degree four", 6, [(0,1),(0,2),(0,3),(0,4),(4,5),(1,2)]),
    ]
    result = {}
    for name, n, edges in inputs:
        g = adjacency(n, edges)
        law = Law.compute(g)
        pmf, hist = brute(g)
        require(pmf == law.seq and hist == law.hist, f"{name} brute disagreement")
        require(not subcubic_violation(g, law), f"{name} witness guard")
        if name == "paper degree four":
            require(topology(g)["max_degree"] == 4 and law.fs[2] == F(5,24)
                    and law.ft[2] == F(1,5) and law.positive == (2,), "degree-four control")
        result[name] = dict(permutations=factorial(n), seq=pmf, hist=hist,
                            subcubic_witness=False)
    return result


def delete_vertex(g, v):
    def new(x):
        return x - (x > v)
    return adjacency(len(g)-1, [(new(a),new(b)) for a,b in edges_of(g) if v not in (a,b)])


def deletions(g):
    checked = {}
    for kind, items in (("vertex", range(len(g))), ("edge", edges_of(g))):
        rows = []
        for item in items:
            if kind == "vertex":
                h = delete_vertex(g, item)
            else:
                h = adjacency(len(g), [e for e in edges_of(g) if e != item])
            law = Law.compute(h)
            rows.append(dict(deleted=item, connected=topology(h)["connected"],
                             violating_k=law.positive))
        checked[kind] = rows
    return checked


def isomorphism(g, h):
    # Search bijections matching degrees and adjacency for every mapped pair.
    if len(g) != len(h):
        return None
    mapping = {}
    def search(free):
        if not free:
            return tuple(mapping[v] for v in range(len(g)))
        best = None
        for v in range(len(g)):
            if v in mapping:
                continue
            choices = [u for u in vertices(free) if g[v].bit_count()==h[u].bit_count()
                       and all(bool(g[v] & (1<<a)) == bool(h[u] & (1<<b))
                               for a,b in mapping.items())]
            if not choices:
                return None
            if best is None or len(choices) < len(best[1]):
                best = v, choices
        v, choices = best
        for u in choices:
            mapping[v] = u
            found = search(free ^ (1<<u))
            if found is not None:
                return found
            del mapping[v]
        return None
    perm = search((1<<len(g))-1)
    if perm is not None:
        require(sorted(perm)==list(range(len(g))) and
                adjacency(len(g),[(perm[u],perm[v]) for u,v in edges_of(g)])==h, "bad bijection")
    return perm


def family(m, ring=False):
    edges = []
    for i in range(m):
        h = 5*i
        edges += [(h,h+1),(h,h+2),(h,h+3),(h+3,h+4)]
        if ring:
            edges.append((h+1,5*((i+1)%m)+1))
        elif i:
            edges.append((h-3,h+1))
    return adjacency(5*m, edges)


def check_certificate(record, *, annotation_errors=None):
    g = adjacency(record["n"], record["edges"])
    law = Law.compute(g)
    require(subcubic_violation(g, law), "no subcubic violation")
    k = record["violating_k"]
    require(k in law.positive, "declared threshold")
    x, y = law.fs[k], law.ft[k]
    require(x == F(record["P_seq_le_k"]), "wrong sequential CDF")
    require(y == F(record["P_stat_le_k"]), "wrong static CDF")
    require(x-y == F(record["J_exact"]) and
            x.numerator*y.denominator - y.numerator*x.denominator ==
            record["cross_product_diff"], "gap")
    t = topology(g)
    for key in ("n","num_edges","connected","is_tree","max_degree"):
        require(record[key] == t[key], key)
    require(law.hist == {int(k):v for k,v in record["mis_size_counts"].items()}
            and sum(law.hist.values()) == record["total_mis"], "static histogram")
    annotated = {int(k):F(v) for k,v in record["rsa_pmf"].items()}
    if law.seq != annotated:
        differences = [dict(field=f"rsa_pmf[{k}]", stored=annotated.get(k),
                            computed=law.seq.get(k)) for k in sorted(law.seq.keys() | annotated.keys())
                       if law.seq.get(k) != annotated.get(k)]
        if annotation_errors is None:
            detail = ", ".join(f"{d['field']} supplied {d['stored']}, computed {d['computed']}"
                               for d in differences)
            raise ValueError(f"RSA PMF mismatch: {detail}")
        annotation_errors.extend(differences)
        annotation_errors.append(dict(field="sum of stored rsa_pmf", stored=sum(annotated.values()),
                                      computed=sum(law.seq.values())))
    return g, law


def corruptions(original):
    results = {}
    # Isolate each mutation. Keep the supplied bytes untouched.
    original = copy.deepcopy(original)
    g = adjacency(original["n"], original["edges"])
    original["rsa_pmf"] = {str(k):str(v) for k,v in sequential(g).items()}
    check_certificate(original)
    for kind, expected in [
            ("edge drop","no subcubic violation"), ("degree four","no subcubic violation"),
            ("probability","wrong sequential CDF"), ("loop","loop"),
            ("duplicate reversed","parallel edge"), ("out of range","invalid vertex"),
            ("mass at seven",f"RSA PMF mismatch: rsa_pmf[7] supplied 0, computed {original['rsa_pmf']['7']}")]:
        r = copy.deepcopy(original)
        if kind == "edge drop":
            del r["edges"][0]
        elif kind == "degree four":
            r["edges"].append([0,4])
            h = adjacency(r["n"], r["edges"])
            require(topology(h)["max_degree"] == 4, "mutant degree")
            mutant = Law.compute(h)
            require(mutant.fs[6] == F(6229,108000) > F(3,59) == mutant.ft[6],
                    "degree mutant must retain a genuine CDF violation")
        elif kind == "probability":
            r["P_seq_le_k"] = "63/3375"
        elif kind == "loop":
            r["edges"].append([0,0])
        elif kind == "duplicate reversed":
            r["edges"].append([1,0])
        elif kind == "mass at seven":
            r["rsa_pmf"]["7"] = "0"
        else:
            r["edges"].append([0,15])
        try:
            check_certificate(r)
        except ValueError as exc:
            require(str(exc)==expected, f"unexpected rejection of {kind}: {exc}")
            results[kind] = str(exc)
        else:
            raise ValueError(f"accepted {kind}")
    return results


def checked_witnesses(doc, annotation_errors):
    g0, _ = check_certificate(doc, annotation_errors=annotation_errors)
    items = doc["all_minimal_n15_counterexamples"]
    require([r["id"] for r in items] == ["CE#1","CE#2","CE#3"], "witness list")
    graphs, results = [], {}
    for i, r in enumerate(items):
        g = adjacency(r["n"], r["edges"])
        t = topology(g)
        require(t["n"]==15 and t["connected"] and t["max_degree"]==3
                and t["num_edges"]==r["num_edges"]==(14,15,15)[i]
                and t["girth"]==r["girth"]==(None,5,3)[i], "topology")
        if i==0:
            require(g==g0 and t["is_tree"], "tree edge list")
        law = Law.compute(g)
        per_set = paper_sum_over_orders(g)
        regroup = Counter()
        for s, p in per_set.items():
            regroup[s.bit_count()] += p
        require(regroup == law.seq and Counter(s.bit_count() for s in per_set)==law.hist,
                "direct paper sum disagrees")
        x, y = law.fs[6], law.ft[6]
        require(x==F(64,3375) and y==F(1,55) and law.positive==(6,), "tail")
        require((not law.negative)==r["global_static_dominance"], "dominance flag")
        if i:
            require(law.hist=={6:1,7:54} and not law.negative, "reversed order")
            require(law.summary()["mean_seq"]==F(23561,3375)<F(384,55)
                    ==law.summary()["mean_stat"], "mean reversal")
        else:
            require(law.hist=={6:1,7:50,8:4} and law.negative==(7,)
                    and law.fs[7]==F(8185211,10135125), "tree crossing")
        d = deletions(g)
        minimal = not any(row["violating_k"] for rows in d.values() for row in rows)
        require(minimal == r["vertex_and_edge_minimal"], "minimality flag")
        types = {}
        if i in (0,2):
            model = family(3,ring=(i==2))
            types["construction_to_witness"] = isomorphism(model,g)
            require(types["construction_to_witness"] is not None, "wrong construction")
        for row in d["edge"]:
            if row["violating_k"]:
                sub = adjacency(15,[e for e in edges_of(g) if e!=row["deleted"]])
                row["isomorphism_to_tree"] = isomorphism(sub,g0)
                require(row["isomorphism_to_tree"] is not None, "unexpected deletion witness")
        graphs.append(g)
        results[r["id"]] = dict(**t, **law.summary(), **types, deletions=d,
                                independently_summed_sets=len(per_set))
    return graphs, results


def family_checks():
    rows = {}
    counts = [1,3,13]
    for m in range(1,7):
        if m >= 3:
            counts.append(5*counts[-1]-4*counts[-2]+2*counts[-3])
        g = family(m)
        law = Law.compute(g)
        require(topology(g)["is_tree"] and topology(g)["max_degree"]==3, "family shape")
        require(sum(law.hist.values())==counts[m] and min(law.hist)==2*m and
                law.hist[2*m]==1 and law.fs[2*m]==F(4,15)**m, "family identity")
        rows[m] = dict(hist=law.hist, seq_at_min=law.fs[2*m], stat_at_min=law.ft[2*m],
                       gap_at_min=law.fs[2*m]-law.ft[2*m],
                       ratio_at_min=law.fs[2*m]/law.ft[2*m],
                       max_ratio=max(s/t for s,t in zip(law.fs,law.ft) if 0<t<1))
    return rows


def extrema(g):
    law = Law.compute(g)
    points = [(s,t) for s,t in zip(law.fs,law.ft) if 0<t<1]
    return dict(max_gap=max(s-t for s,t in points), max_ratio=max(s/t for s,t in points),
                violating_k=law.positive, hist=law.hist)


def path_attachments(g):
    # Every subcubic attachment site, including vertices of degree two.
    rows = {}
    best = (F(0), None, None)
    attaining_hist = {}
    for v, adj in enumerate(g):
        if adj.bit_count() >= 3:
            continue
        ratios = []
        for n in range(16,29):
            edges = edges_of(g) + [(v,15)] + [(w-1,w) for w in range(16,n)]
            h = adjacency(n,edges)
            point = extrema(h)
            ratios.append(point["max_ratio"])
            if point["max_ratio"] > best[0]:
                best = (point["max_ratio"],v,n)
                attaining_hist = point["hist"]
        rows[v] = ratios
    return dict(site_ratios_n16_to_28=rows, count=sum(map(len,rows.values())),
                reversed=sum(r>1 for row in rows.values() for r in row),
                max_ratio=best[0], attaining_site=best[1], attaining_order=best[2],
                attaining_hist=attaining_hist)


def tree_size_eight_integral():
    # Integral in REFEREE.md. Index j denotes the even power s^(2*j).
    end = [95,75,5,1]
    return sum(F(a*b, 2*240**2*(2*(j+k+i)+1))
               for j,a in enumerate(end) for k,b in enumerate(end) for i in (0,1))


def compare_printed_table(rows):
    section = Path("inputs/REPORT.md").read_text().split("### 3.1",1)[1].split("### 3.2",1)[0]
    checked, differences = [], []
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [s.strip().replace("**","").replace(",","") for s in line.strip("|").split("|")]
        if cells[0] in ("1–2","Total"):
            ns = (1,2) if cells[0]=="1–2" else tuple(range(1,16))
            actual = tuple(sum(rows[n][i] for n in ns) for i in range(3))
            printed = tuple(int(cells[i]) for i in (1,2,5))
            if actual != printed:
                differences.append([cells[0],"totals",actual,printed])
            checked.append(cells[0])
            continue
        if not cells[0].isdigit():
            continue
        n = int(cells[0])
        count,well,bad,gap,ratio,k,seq,stat = rows[n]
        printed = [int(cells[i]) for i in (1,2,5)]
        actual = [count,well,bad]
        if printed != actual:
            differences.append([n,"counts",actual,printed])
        exacts = [F(t) for t in re.findall(r"[+-]?\d+/\d+",cells[3])]
        target_k = int(re.search(r"k=(\d+)",cells[3])[1])
        if exacts != list(map(F,(gap,seq,stat))) or target_k!=int(k):
            differences.append([n,"exact gap or attaining threshold"])
        decimal, exponent = re.search(r"\\approx\s+([+-]?\d+\.\d+)\s+\\times 10\^\{(-?\d+)\}",cells[3]).groups()
        scale = F(10)**int(exponent)
        unit = F(1,10**len(decimal.split(".")[1]))
        if abs(scale*F(decimal)-F(gap)) > scale*unit/2:
            differences.append([n,"printed gap approximation"])
        printed_ratio = cells[4].strip("$")
        unit = F(1,10**len(printed_ratio.split(".")[1]))
        if abs(F(printed_ratio)-F(ratio)) > unit/2:
            differences.append([n,"printed ratio approximation"])
        checked.append(n)
    require(checked==["1–2",*range(3,16),"Total"], "incomplete printed table comparison")
    return dict(rows_checked=checked, discrepancies=differences)


def census_checks(file, graphs):
    rows, matches = {}, {}
    for line in file.read_text().splitlines()[1:]:
        f = line.split()
        if f[0] == "hit":
            n, *masks = map(int,f[1:])
            require(len(masks)==n and adjacency(n,edges_of(masks))==tuple(masks), "hit masks")
            found = [(j, p) for j,g in enumerate(graphs,1)
                     if (p:=isomorphism(masks,g)) is not None]
            require(len(found)==1, "unmatched or ambiguous census hit")
            j, p = found[0]
            require(j not in matches, "duplicated census hit")
            matches[j] = p
        else:
            n, count, well, violations = map(int,f[:4])
            require(n not in rows, "duplicate census row")
            rows[n] = (count,well,violations,*f[4:])
    require(set(rows)==set(range(1,16)) and set(matches)=={1,2,3}, "incomplete census")
    totals = {k:sum(rows[i][0] for i in range(1,k+1)) for k in (12,14,15)}
    require(totals=={12:27525,14:358891,15:1375631} and rows[15][:3]==(1016740,260,3)
            and all(rows[i][2]==0 for i in range(1,15)), "census tally")
    return dict(cumulative_counts=totals, total_well_covered=sum(r[1] for r in rows.values()),
                by_order=rows, census_to_witness_bijections=matches,
                printed_table=compare_printed_table(rows))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", type=Path, help="also match output of referee_census")
    parser.add_argument("--strict-certificate", action="store_true",
                        help="fail if any submitted probability differs")
    args = parser.parse_args()
    result = {"controls":controls()}
    witness = Path("inputs/witness.json").read_bytes()
    result["sha256"] = hashlib.sha256(witness).hexdigest()
    require(result["sha256"]==DIGEST, "witness hash")
    doc = json.loads(witness)
    if args.strict_certificate:
        check_certificate(doc)
    result["annotation_errors"] = []
    graphs, result["witnesses"] = checked_witnesses(doc, result["annotation_errors"])
    result["tree_size_eight_integral"] = tree_size_eight_integral()
    require(result["tree_size_eight_integral"] == result["witnesses"]["CE#1"]["seq"][8],
            "tree probability integral")
    result["rejected_mutants"] = corruptions(doc)
    result["family"] = family_checks()
    result["one_leaf_cycles"] = {m:extrema(family(m,ring=True)) for m in range(3,7)}
    result["pendant_paths_CE3"] = path_attachments(graphs[2])
    if args.census:
        result["census"] = census_checks(args.census,graphs)
    print(json.dumps(result, default=str, indent=2))


if __name__ == "__main__":
    main()

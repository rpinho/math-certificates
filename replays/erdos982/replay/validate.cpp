#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

constexpr int MAX_ORDER = 30;
constexpr int FAMILIES = 9;
constexpr int MUTANTS = 11;
const array<string, FAMILIES> names = {
    "ASYM", "TRANS", "FIRST", "BOUND", "BISECTOR", "CROSS", "CAP", "SYM", "FAN"
};
const array<string, MUTANTS> mutant_names = {
    "ASYM_allow_tie_in_strict_premise", "FIRST_count_repeat", "BISECTOR_drop_premise",
    "BISECTOR_reverse_consequent", "CROSS_require_first_diagonal",
    "CROSS_use_adjacent_side", "CAP_drop_equal_radius", "CAP_reverse_radial_test",
    "CAP_shift_center_by_one", "CROSS_longest_diagonal_beats_all_sides",
    "FAN_drop_last_sector_premise"
};

struct Count {
    uint64_t samples = 0, any = 0, full = 0, violations = 0;
};
struct Summary {
    array<Count, FAMILIES> families{};
    array<uint64_t, MUTANTS> mutants{};
    uint64_t samples = 0;
};
struct Flags {
    bool any[FAMILIES]{}, full[FAMILIES]{}, bad[FAMILIES]{},
         killed[MUTANTS]{};
};
void harvest(Summary &summary, const Flags &flags) {
    ++summary.samples;
    for (int i = 0; i < FAMILIES; ++i) {
        auto &count = summary.families[i];
        ++count.samples;
        count.any += flags.any[i];
        count.full += flags.full[i];
        count.violations += flags.bad[i];
    }
    for (int i = 0; i < MUTANTS; ++i)
        summary.mutants[i] += flags.killed[i];
}

struct Polygon {
    int n;
    int d[MAX_ORDER][MAX_ORDER]{};

    explicit Polygon(int order) : n(order) {}

    int max_classes() const {
        int best = 0;
        for (int i = 0; i < n; ++i) {
            array<bool, 435> present{};
            int distinct = 0;
            for (int j = 0; j < n; ++j) {
                if (i != j && !present[d[i][j]]) {
                    present[d[i][j]] = true;
                    ++distinct;
                }
            }
            best = max(best, distinct);
        }
        return best;
    }

    int rotation() const {
        int best = 0;
        for (int i = 1; i < n; ++i)
            if (d[i][(i+1)%n] < d[best][(best+1)%n])
                best = i;
        return best;
    }

    Polygon normalized() const {
        Polygon result(n);
        int r = rotation();
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                result.d[i][j] = d[(i+r)%n][(j+r)%n];
        return result;
    }

    Flags base() const {
        Flags flags;
        int shortest = 1000, longest = -1, edges = 0;
        for (int a = 0; a < n; ++a)
            for (int b = a + 1; b < n; ++b) {
                shortest = min(shortest, d[a][b]);
                longest = max(longest, d[a][b]);
                ++edges;
            }
        flags.any[0] = flags.full[0] = shortest < longest;
        flags.any[1] = flags.full[1] = edges >= 3;
        flags.any[2] = flags.full[2] = n >= 3;
        // A BOUND clause has K+1 entries. At K=max_classes(), an
        // extremal row gives a true prefix of K markers if such a clause exists.
        int k = max_classes();
        flags.any[3] = flags.full[3] = k < n-1;
        flags.any[7] = flags.full[7] = true;
        for (int a = 1; a < n; ++a)
            flags.bad[7] |= d[a][(a+1)%n] < d[0][1];

        array<bool, 435> seen{};
        for (int a = 0; a < n; ++a) {
            array<bool, 435> row_seen{};
            for (int b = 0; b < n; ++b) {
                if (a != b) {
                    flags.killed[1] |= row_seen[d[a][b]];
                    row_seen[d[a][b]] = true;
                }
                if (a < b) {
                    flags.killed[0] |= seen[d[a][b]];
                    seen[d[a][b]] = true;
                }
            }
        }
        return flags;
    }

    Flags quad(int a, int b, int c, int d0) const {
        Flags flags;
        const array<int,4> v = {a,b,c,d0};
        const int ac = d[a][c], bd = d[b][d0];
        const int ab = d[a][b], bc = d[b][c], cd = d[c][d0], ad = d[a][d0];

        for (auto [x,y] : {pair{ab,cd}, pair{cd,ab}, pair{ad,bc}, pair{bc,ad}}) {
            bool premise = ac <= x;
            flags.any[5] |= premise;
            flags.full[5] |= premise;
            flags.bad[5] |= premise && bd <= y;
            flags.killed[4] |= ac <= x;
            flags.killed[5] |= premise && bd <= bc;
        }
        flags.killed[9] = max(ac,bd) <= max({ab,bc,cd,ad});

        for (int shift = 0; shift < 4; ++shift) {
            int w = v[shift], x = v[(shift+1)%4], y = v[(shift+2)%4],
                z = v[(shift+3)%4];
            int wx = d[w][x], wy = d[w][y], wz = d[w][z],
                xy = d[x][y], xz = d[x][z], yz = d[y][z];

            bool bisector = wx >= xz;
            bool closer = yz < wy;
            flags.any[4] |= bisector;
            flags.full[4] |= bisector;
            flags.bad[4] |= bisector && !closer;
            flags.killed[2] |= !closer;
            flags.killed[3] |= bisector && closer;

            bool cap = wx == wz && wy <= wx;
            bool short_chords = xy < xz && yz < xz;
            flags.any[6] |= wx <= wz || wz <= wx || wy <= wx;
            flags.full[6] |= cap;
            flags.bad[6] |= cap && !short_chords;
            flags.killed[6] |= wy <= wx && !short_chords;
            flags.killed[7] |= wx == wz && wx <= wy && !short_chords;
            flags.killed[8] |= xy == wx && xz <= xy && !short_chords;
        }
        return flags;
    }

    Flags fan(const array<int,5> &v) const {
        Flags flags;
        for (int shift = 0; shift < 5; ++shift) {
            int center = v[shift];
            bool largest[3];
            for (int i = 0; i < 3; ++i) {
                int a = v[(shift+1+i)%5], b = v[(shift+2+i)%5];
                bool left = d[a][b] >= d[center][a];
                bool right = d[a][b] >= d[center][b];
                largest[i] = left && right;
                if (i != 1)
                    flags.any[8] |= left || right;
            }
            flags.full[8] |= largest[0] && largest[2];
            flags.bad[8] |= largest[0] && largest[1] && largest[2];
            flags.killed[10] |= largest[0] && largest[1];
        }
        return flags;
    }
};

void combine(Flags &first, const Flags &other) {
    for (int i = 0; i < FAMILIES; ++i) {
        first.any[i] |= other.any[i];
        first.full[i] |= other.full[i];
        first.bad[i] |= other.bad[i];
    }
    for (int i = 0; i < MUTANTS; ++i)
        first.killed[i] |= other.killed[i];
}

void check_flags(const Flags &flags) {
    for (int i = 0; i < FAMILIES; ++i)
        if (flags.bad[i])
            throw runtime_error("Geometric test violation in " + names[i]);
}

uint32_t pack_quad(const Flags &flags) {
    uint32_t result = 0;
    for (int i = 4; i <= 6; ++i) {
        result |= uint32_t(flags.any[i]) << (i - 4);
        result |= uint32_t(flags.full[i]) << (i - 1);
    }
    for (int i = 2; i < 10; ++i)
        result |= uint32_t(flags.killed[i]) << (i + 4);
    return result;
}

void unpack_quad(Flags &flags, uint32_t bits) {
    for (int i = 4; i <= 6; ++i) {
        flags.any[i] = (bits >> (i-4)) & 1;
        flags.full[i] = (bits >> (i-1)) & 1;
    }
    for (int i = 2; i < 10; ++i)
        flags.killed[i] = (bits >> (i+4)) & 1;
}

struct Dimacs {
    int variables = 0;
    vector<int> literals;
    explicit Dimacs(int n) {
        ifstream input("runs/check_fan_" + to_string(n) + ".cnf");
        string p, cnf;
        int count;
        if (!(input >> p >> cnf >> variables >> count) || p != "p" || cnf != "cnf")
            throw runtime_error("missing or invalid control CNF");
        int literal, clauses = 0;
        while (input >> literal) {
            literals.push_back(literal);
            clauses += literal == 0;
        }
        if (clauses != count)
            throw runtime_error("incorrect control DIMACS count");
    }

    void check(const Polygon &p) const {
        vector<int> edges;
        for (int a = 0; a < p.n; ++a)
            for (int b = a+1; b < p.n; ++b)
                edges.push_back(p.d[a][b]);
        vector<unsigned char> value(2*variables+1);
        int id = variables;
        auto assign = [&](bool truth) {
            ++id;
            value[id] = truth;
            value[2*variables-id] = !truth;
        };
        for (size_t i = 0; i < edges.size(); ++i)
            for (size_t j = 0; j < edges.size(); ++j)
                if (i != j)
                    assign(edges[i] < edges[j]);
        for (int a = 0; a < p.n; ++a) {
            array<bool,435> seen{};
            for (int b = 0; b < p.n; ++b) {
                if (a == b)
                    continue;
                assign(!seen[p.d[a][b]]);
                seen[p.d[a][b]] = true;
            }
        }
        if (id != 2*variables)
            throw runtime_error("incorrect control variable count");
        bool clause = false;
        for (int literal : literals) {
            if (literal)
                clause |= value[variables+literal];
            else {
                if (!clause)
                    throw runtime_error("CNF rejected a realized pattern");
                clause = false;
            }
        }
    }
};

array<array<Summary,14>,3> results;
array<array<uint64_t,MAX_ORDER+1>,14> necklaces{};

void fixed_generators(const string &witnesses) {
    vector<Dimacs> formulas;
    for (int n = 3; n <= 13; ++n)
        formulas.emplace_back(n);
    ifstream stream(witnesses, ios::binary);
    if (!stream)
        throw runtime_error("missing witness file");
    char order, kind, rank;
    while (stream.get(order)) {
        if (!stream.get(kind) || order < 3 || order > 13 || kind < 0 || kind > 5)
            throw runtime_error("invalid witness file");
        Polygon p(order);
        for (int a = 0; a < order; ++a)
            for (int b = a+1; b < order; ++b) {
                if (!stream.get(rank))
                    throw runtime_error("truncated witness file");
                p.d[a][b] = p.d[b][a] = static_cast<unsigned char>(rank);
            }
        p = p.normalized();
        formulas[order-3].check(p);
        // The checked CNF contains all families except BOUND, which has no
        // clauses at K=n-1. Its additional clauses at the sample's K follow
        // from the explicit representative count in base().
        Flags flags = p.base();
        for (int a = 0; a < order; ++a)
            for (int b = a+1; b < order; ++b)
                for (int c = b+1; c < order; ++c)
                    for (int d = c+1; d < order; ++d) {
                        combine(flags, p.quad(a,b,c,d));
                        for (int e = d+1; e < order; ++e)
                            combine(flags, p.fan({a,b,c,d,e}));
                    }
        check_flags(flags);
        harvest(results[kind ? 2 : 0][order], flags);
    }
}

class Regular {
    int n, m;
    Polygon carrier;
    vector<uint32_t> quads;
    vector<uint8_t> fans;
    uint32_t possible = 0;
    uint8_t fan_possible = 0;
    array<int,MAX_ORDER+1> word{};
    array<int,MAX_ORDER> selected{};

    size_t index(int a,int b,int c,int d) const {
        return ((a*m + b)*m + c)*m + d;
    }

    void sample() {
        int j = 0;
        for (int i = 0; i < m; ++i)
            if (word[i+1])
                selected[j++] = i;
        if (j != n)
            throw runtime_error("necklace weight");
        Flags flags;
        int k = 0, shortest = m, longest = 0;
        uint32_t used = 0;
        for (int a = 0; a < n; ++a) {
            uint32_t row = 0;
            for (int b = 0; b < n; ++b) {
                if (a == b)
                    continue;
                int step = carrier.d[selected[a]][selected[b]];
                uint32_t bit = uint32_t(1) << step;
                flags.killed[1] |= bool(row & bit);
                row |= bit;
                if (a < b) {
                    flags.killed[0] |= bool(used & bit);
                    used |= bit;
                    shortest = min(shortest, step);
                    longest = max(longest, step);
                }
            }
            k = max(k, __builtin_popcount(row));
        }
        flags.any[0] = flags.full[0] = shortest < longest;
        flags.any[1] = flags.full[1] = true;
        flags.any[2] = flags.full[2] = true;
        flags.any[3] = flags.full[3] = k < n-1;
        flags.any[7] = flags.full[7] = true;

        // All local clauses were checked on the carrier. Restriction and
        // rotation preserve their cyclic quadruple instances, so none needs
        // rechecking per subset. Here inspect them for test/mutant coverage.
        uint32_t bits = 0;
        for (int a = 0; a < n && bits != possible; ++a)
            for (int b = a+1; b < n && bits != possible; ++b)
                for (int c = b+1; c < n && bits != possible; ++c) {
                    size_t offset = index(selected[a],selected[b],selected[c],0);
                    for (int d = c+1; d < n; ++d)
                        bits |= quads[offset+selected[d]];
                }
        unpack_quad(flags, bits);
        uint8_t fan_bits = 0;
        for (int a = 0; a < n && fan_bits != fan_possible; ++a)
            for (int b = a+1; b < n && fan_bits != fan_possible; ++b)
                for (int c = b+1; c < n && fan_bits != fan_possible; ++c)
                    for (int d = c+1; d < n && fan_bits != fan_possible; ++d) {
                        size_t offset = index(selected[a],selected[b],selected[c],selected[d])*m;
                        for (int e = d+1; e < n; ++e)
                            fan_bits |= fans[offset+selected[e]];
                    }
        flags.any[8] = fan_bits & 1;
        flags.full[8] = fan_bits & 2;
        flags.killed[10] = fan_bits & 4;
        // CROSS_use_adjacent_side uses a chosen first diagonal and side;
        // its count is for the printed canonical necklace orientation.
        check_flags(flags);
        harvest(results[1][n], flags);
        ++necklaces[n][m];
    }

    // Binary necklace recursion. p is the period of the copied prefix.
    void visit(int t, int p, int ones) {
        if (ones > n || ones + m - t + 1 < n)
            return;
        if (t > m) {
            if (m % p == 0)
                sample();
            return;
        }
        word[t] = word[t-p];
        visit(t+1, p, ones+word[t]);
        if (!word[t-p]) {
            word[t] = 1;
            visit(t+1, t, ones+1);
        }
    }

public:
    Regular(int order, int size)
        : n(order), m(size), carrier(m), quads(m*m*m*m), fans(m*m*m*m*m) {
        for (int a = 0; a < m; ++a)
            for (int b = a+1; b < m; ++b)
                carrier.d[a][b] = carrier.d[b][a] = min(b-a,m-b+a);
        for (int a = 0; a < m; ++a)
            for (int b = a+1; b < m; ++b)
                for (int c = b+1; c < m; ++c)
                    for (int d = c+1; d < m; ++d) {
                        auto flags = carrier.quad(a,b,c,d);
                        check_flags(flags);
                        uint32_t packed = pack_quad(flags);
                        quads[index(a,b,c,d)] = packed;
                        possible |= packed;
                        for (int e = d+1; e < m; ++e) {
                            auto fan = carrier.fan({a,b,c,d,e});
                            check_flags(fan);
                            uint8_t packed_fan = fan.any[8] | (fan.full[8] << 1)
                                                           | (fan.killed[10] << 2);
                            fans[index(a,b,c,d)*m+e] = packed_fan;
                            fan_possible |= packed_fan;
                        }
                    }
    }

    void run() { visit(1,1,0); }
};

int main(int argc, char **argv) {
    bool run_regular = argc == 1 || string(argv[1]) == "regular";
    bool run_other = argc == 1 || string(argv[1]) == "other";
    bool run_targeted = argc > 1 && string(argv[1]) == "targeted";
    if (run_other || run_targeted)
        fixed_generators(run_targeted ? "runs/witnesses_targeted.bin" : "runs/witnesses.bin");
    if (run_regular)
        for (int n = 3; n <= 13; ++n) {
            for (int m = n; m <= 2*n+4; ++m)
                Regular(n,m).run();
            cerr << "finished G2 order " << n << '\n';
        }

    cout << "generator\tn\tfamily\tsamples\tany\tfull\tviolations\tcoverage\n";
    for (int g = 0; g < 3; ++g)
        for (int n = 3; n <= 13; ++n)
            for (int i = 0; i < FAMILIES; ++i) {
                auto c = results[g][n].families[i];
                if (!c.samples)
                    continue;
                cout << g+1 << '\t' << n << '\t' << names[i] << '\t'
                     << c.samples << '\t' << c.any << '\t' << c.full << '\t'
                     << c.violations << '\t' << (c.full ? "TESTED" : "UNTESTED") << '\n';
            }
    string suffix = argc == 1 ? "" : "_" + string(argv[1]);
    ofstream mutant("runs/mutants" + suffix + ".tsv");
    mutant << "mutant\tG1\tG2\tG3\n";
    for (int i = 0; i < MUTANTS; ++i) {
        mutant << mutant_names[i];
        for (auto &generator : results) {
            uint64_t total = 0;
            for (auto &order : generator)
                total += order.mutants[i];
            mutant << '\t' << total;
        }
        mutant << '\n';
    }
    if (run_regular) {
        ofstream counts("runs/necklaces.tsv");
        counts << "n\tm\tsamples\n";
        for (int n = 3; n <= 13; ++n)
            for (int m = n; m <= 2*n+4; ++m)
                counts << n << '\t' << m << '\t' << necklaces[n][m] << '\n';
    }
}

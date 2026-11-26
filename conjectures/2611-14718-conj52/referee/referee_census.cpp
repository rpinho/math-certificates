// Complete connected subcubic census, order at most 15. Standalone C++20.
#include <algorithm>
#include <array>
#include <atomic>
#include <bit>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using Mask = unsigned;
using Count = long long;
constexpr int limit = 15;
using Graph = std::array<uint16_t, limit>;
using Colors = std::array<int, limit>;
using Key = std::array<uint64_t, 2>;

int size(Mask s) { return std::popcount(s); }
int first(Mask s) { return std::countr_zero(s); }
void edge(Graph &g, int u, int v) { g[u] ^= 1u << v; g[v] ^= 1u << u; }

struct KeyHash {
    size_t operator()(const Key &k) const {
        return k[0] ^ (k[1] * 0x9e3779b97f4a7c15ULL);
    }
};

// Refine an ordered partition by the multiset of neighbor colors. Compare
// full adjacency encodings at discrete leaves, never hashes as identities.
Key canonical(const Graph &g, int n, Colors color, int classes) {
    std::array<std::pair<unsigned,int>, limit> order{};
    while (true) {
        for (int v = 0; v < n; ++v) {
            std::array<unsigned,3> nbr{};
            int j = 0;
            for (Mask s = g[v]; s; s &= s-1) nbr[j++] = color[first(s)];
            std::sort(nbr.begin(), nbr.end());
            unsigned sig = (((color[v]*16u + nbr[0])*16 + nbr[1])*16 + nbr[2]);
            order[v] = {sig,v};
        }
        std::sort(order.begin(), order.begin()+n);
        int distinct = 0;
        for (int i = 0; i < n; ++i) {
            if (!i || order[i].first != order[i-1].first) ++distinct;
            color[order[i].second] = distinct;
        }
        if (distinct == classes) break;
        classes = distinct;
    }
    if (classes == n) {
        int bit = 0;
        Key key{};
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < i; ++j, ++bit)
                if (g[order[i].second] & (1u << order[j].second))
                    key[bit/64] |= uint64_t(1) << (bit%64);
        return key;
    }
    std::array<Mask,limit+1> cells{};
    for (int i = 0; i < n; ++i) cells[color[i]] |= 1u << i;
    Mask branch = 0;
    for (int i = 1; i <= classes; ++i)
        if (size(cells[i]) > 1 && (!branch || size(cells[i]) < size(branch))) branch = cells[i];
    Key best{UINT64_MAX,UINT64_MAX};
    Mask tried = 0;
    for (Mask s = branch; s; s &= s-1) {
        int v = first(s);
        bool twin = false;
        for (Mask t = tried; t; t &= t-1) {
            int w = first(t);
            if (((g[v]^g[w]) & ~((1u<<v)|(1u<<w))) == 0) twin = true;
        }
        if (twin) continue; // swapping the two vertices preserves this partition and graph
        tried |= 1u << v;
        Colors next = color;
        next[v] = classes + 1;
        best = std::min(best, canonical(g, n, next, classes+1));
    }
    return best;
}

std::vector<Graph> extend(const std::vector<Graph> &parents, int n) {
    std::unordered_set<Key,KeyHash> seen;
    std::vector<Graph> out;
    auto save = [&](const Graph &g) {
        Colors c;
        c.fill(1);
        if (seen.insert(canonical(g,n,c,1)).second) out.push_back(g);
    };
    int v = n-1;
    for (const Graph &p : parents) {
        int leaves = 0;
        for (int u = 0; u < v; ++u) leaves += size(p[u]) == 1;
        for (int u = 0; u < v; ++u) {
            if (size(p[u]) < 3) {
                Graph g = p;
                edge(g,u,v);
                save(g);
            }
            for (Mask s = p[u] >> (u+1); s; s &= s-1) {
                int w = u+1+first(s);
                if (!leaves) { // subdividing an edge preserves old degrees
                    Graph g = p;
                    edge(g,u,w); edge(g,u,v); edge(g,w,v);
                    save(g);
                }
                if (size(p[u]) < 3 && size(p[w]) < 3 &&
                    leaves == (size(p[u]) == 1) + (size(p[w]) == 1)) {
                    Graph g = p;
                    edge(g,u,v); edge(g,w,v);
                    save(g);
                }
            }
        }
    }
    // A cubic graph has a cycle edge. Removing it leaves a connected graph
    // of the same order with two degree-two vertices and all others cubic.
    if (n % 2 == 0) {
        auto before = out.size();
        for (size_t i = 0; i < before; ++i) {
            Graph g = out[i];
            Mask deficiency = 0;
            for (int v = 0; v < n; ++v)
                if (size(g[v]) != 3) deficiency |= 1u << v;
            if (size(deficiency) != 2) continue;
            int u = first(deficiency), w = first(deficiency & (deficiency-1));
            if (size(g[u]) == 2 && size(g[w]) == 2 && !(g[u] & (1u<<w))) {
                edge(g,u,w);
                save(g);
            }
        }
    }
    return out;
}

using Poly = std::array<Count, limit+1>;
struct Law {
    Poly ways{};
    int lo{}, hi{};
    int stamp{};
};
std::array<Count,limit+1> factorial{};
struct Evaluator {
    std::vector<Law> cache;
    Graph g{};
    Mask full{};
    int stamp = 0;
    Evaluator(int n): cache(1u<<n) { cache[0].ways[0]=1; }

    // Count random full permutations classified by final greedy size.
    const Law &seq(Mask available) {
        auto &p = cache[available];
        if (!available || p.stamp == stamp) return p;
        p.stamp = stamp;
        p.lo = limit; p.hi = 0;
        p.ways.fill(0);
        int n = size(available);
        for (Mask t = available; t; t &= t-1) {
            int v = first(t);
            Mask child = available & ~(g[v] | (1u<<v));
            Count lifts = factorial[n-1]/factorial[size(child)];
            const auto &q = seq(child);
            for (int k = q.lo; k <= q.hi; ++k) p.ways[k+1] += lifts*q.ways[k];
            p.lo = std::min(p.lo,q.lo+1);
            p.hi = std::max(p.hi,q.hi+1);
        }
        return p;
    }

    // Bron--Kerbosch on the complement, where cliques are independent sets.
    void mis(Mask possible, Mask excluded, int k, Poly &count) {
        if (!possible) {
            if (!excluded) ++count[k];
            return;
        }
        int pivot = first(possible | excluded);
        Mask branch = possible & (g[pivot] | (1u << pivot));
        for (; branch; branch &= branch-1) {
            int v = first(branch);
            Mask bit=1u<<v, compatible=full & ~(g[v]|bit);
            mis(possible & compatible, excluded & compatible,k+1,count);
            possible ^= bit;
            excluded |= bit;
        }
    }
};
struct Fraction {
    Count a=0,b=1;
    bool operator<(const Fraction &y) const {
        return (__int128)a*y.b < (__int128)y.a*b;
    }
    std::string str() const {
        auto d=std::gcd(a,b);
        return std::to_string(a/d)+"/"+std::to_string(b/d);
    }
};
struct Stats {
    int graphs=0, well=0, violations=0;
    Fraction maxGap{-2,1}, maxRatio{-1,1};
    Fraction bestSeq{}, bestStat{};
    int bestK=-1;
    std::vector<std::string> hits;
    void gapPoint(Fraction gap, int k, Fraction sq, Fraction st) {
        if (maxGap<gap || (!(gap<maxGap) && k<bestK)) {
            maxGap=gap; bestK=k; bestSeq=sq; bestStat=st;
        }
    }
    void add(const Stats &s) {
        graphs+=s.graphs; well+=s.well; violations+=s.violations;
        gapPoint(s.maxGap,s.bestK,s.bestSeq,s.bestStat);
        maxRatio=std::max(maxRatio,s.maxRatio);
        hits.insert(hits.end(),s.hits.begin(),s.hits.end());
    }
};

Stats evaluate(const std::vector<Graph> &graphs, int n, int workers) {
    std::atomic<size_t> start{0};
    std::vector<Stats> partial(workers);
    auto worker = [&](int id) {
        Stats &s = partial[id];
        Evaluator e(n);
        e.full=(1u<<n)-1;
        while (true) {
            size_t pos=start.fetch_add(64);
            if (pos>=graphs.size()) break;
            for (size_t i=pos; i<std::min(graphs.size(),pos+64); ++i) {
                e.g=graphs[i]; ++e.stamp; ++s.graphs;
                Poly hist{};
                e.mis(e.full,0,0,hist);
                Count total=std::accumulate(hist.begin(),hist.end(),Count(0));
                const auto &p=e.seq(e.full);
                Count st=0, sq=0;
                bool bad=false;
                for (int k=0; k<=n; ++k) {
                    st+=hist[k]; sq+=p.ways[k];
                    if (!st || st==total) continue;
                    Fraction gap{sq*total-st*factorial[n],factorial[n]*total};
                    Fraction ratio{sq*total,st*factorial[n]};
                    s.gapPoint(gap,k,{sq,factorial[n]},{st,total});
                    s.maxRatio=std::max(s.maxRatio,ratio);
                    bad |= gap.a>0;
                }
                assert(total>0 && sq==factorial[n] && st==total);
                s.well += p.lo==p.hi;
                if (bad) {
                    ++s.violations;
                    std::string line="hit "+std::to_string(n);
                    for (int v=0;v<n;++v) line+=" "+std::to_string(e.g[v]);
                    s.hits.push_back(line);
                }
            }
        }
    };
    std::vector<std::thread> ts;
    for (int i=1;i<workers;++i) ts.emplace_back(worker,i);
    worker(0);
    for (auto &t:ts) t.join();
    Stats all;
    for (auto &s:partial) all.add(s);
    return all;
}

void bruteCheck(const Graph &g, int n) {
    Mask full=(1u<<n)-1;
    Evaluator eval(n);
    eval.g=g; eval.full=full; ++eval.stamp;
    Poly hist{}, subsets{}, perms{};
    eval.mis(full,0,0,hist);
    for (Mask subset=0; subset<=full; ++subset) {
        Mask neighbors=0;
        for (int v=0;v<n;++v)
            if (subset & (1u<<v)) neighbors|=g[v];
        if (!(subset & neighbors) && (subset | neighbors)==full) ++subsets[size(subset)];
    }
    std::array<int,limit> order{};
    std::iota(order.begin(),order.begin()+n,0);
    do {
        Mask occupied=0;
        for (int i=0;i<n;++i) {
            int v=order[i];
            if (!(occupied & g[v])) occupied |= 1u<<v;
        }
        ++perms[size(occupied)];
    } while (std::next_permutation(order.begin(),order.begin()+n));
    if (hist!=subsets || eval.seq(full).ways!=perms) {
        std::cerr<<"census controls disagree at order "<<n<<std::endl;
        std::exit(1);
    }
}

int runControls() {
    std::vector<Graph> level(1);
    int checked=0;
    Count orders=0;
    for (int n=1;n<=8;++n) {
        if (n>1) level=extend(level,n);
        for (auto &g:level) bruteCheck(g,n);
        checked+=level.size(); orders+=factorial[n]*level.size();
    }
    std::mt19937 rng(20261125);
    for (int i=0;i<200;++i) {
        Graph g{};
        for (int v=1;v<8;++v)
            for (int u=0;u<v;++u)
                if (rng()%8 < static_cast<unsigned>(1+i%7)) edge(g,u,v);
        bruteCheck(g,8);
    }
    std::cout<<checked<<" connected subcubic graphs through order 8, "<<orders
             <<" permutations. 200 additional order-8 draws, "<<factorial[8]*200
             <<" permutations. All subset histograms and full permutation counts agree.\n";
    return 0;
}

// Supply full laws to the stand-alone Fraction replay. Each row is n,
// n adjacency masks, followed by (size, MIS count, permutation count) triples.
using Index = std::array<std::unordered_map<Key,int,KeyHash>,limit+1>;

std::vector<int> componentIds(const Graph &g, Mask rest, const Index &index) {
    std::vector<int> ids;
    while (rest) {
        Mask part=rest & -rest, wave=part;
        while (wave) {
            Mask neighbors=0;
            for (Mask t=wave;t;t&=t-1) neighbors|=g[first(t)];
            wave=neighbors & rest & ~part;
            part|=wave;
        }
        rest^=part;
        Graph compact{};
        int k=0;
        for (Mask t=part;t;t&=t-1,++k) {
            for (Mask a=g[first(t)] & part;a;a&=a-1) {
                Mask lower=(a & -a)-1;
                compact[k] |= 1u<<size(part & lower);
            }
        }
        Colors colors; colors.fill(1);
        ids.push_back(index[k].at(canonical(compact,k,colors,1)));
    }
    std::sort(ids.begin(),ids.end());
    return ids;
}

int streamLaws(int maxn) {
    if (maxn<1 || maxn>limit) return 2;
    std::vector<Graph> level(1);
    Index index;
    int serial=0;
    for (int n=1;n<=maxn;++n) {
        if (n>1) level=extend(level,n);
        Evaluator eval(n);
        eval.full=(1u<<n)-1;
        for (const Graph &g:level) {
            ++serial;
            if (n<=maxn-2) {
                Colors colors; colors.fill(1);
                index[n].emplace(canonical(g,n,colors,1),serial);
            }
            ++eval.stamp;
            eval.g=g;
            Poly hist{};
            eval.mis(eval.full,0,0,hist);
            const auto &law=eval.seq(eval.full);
            std::cout<<n;
            for (int v=0;v<n;++v) std::cout<<" "<<g[v];
            for (int k=0;k<=n;++k)
                if (hist[k] || law.ways[k]) std::cout<<" "<<k<<" "<<hist[k]<<" "<<law.ways[k];
            std::cout<<" |";
            for (int v=0;v<n;++v) {
                auto ids=componentIds(g,eval.full & ~(g[v]|(1u<<v)),index);
                std::cout<<" ";
                if (ids.empty()) std::cout<<"0";
                for (size_t i=0;i<ids.size();++i) {
                    if (i) std::cout<<".";
                    std::cout<<ids[i];
                }
            }
            std::cout<<"\n";
        }
    }
    return 0;
}

int main(int argc,char **argv) {
    std::ios::sync_with_stdio(false);
    factorial[0]=1;
    for (int n=1;n<=limit;++n) factorial[n]=n*factorial[n-1];
    if (argc==2 && std::string(argv[1])=="--controls") return runControls();
    if (argc==3 && std::string(argv[1])=="--stream") return streamLaws(std::atoi(argv[2]));
    int maxn=argc>1?std::atoi(argv[1]):15;
    int workers=argc>2?std::atoi(argv[2]):3;
    if (maxn<1 || maxn>15 || workers<1 || workers>4) return 2;
    std::vector<Graph> level(1);
    std::cout<<"n graphs well_covered violations max_gap max_ratio gap_k gap_seq_cdf gap_stat_cdf\n";
    for (int n=1;n<=maxn;++n) {
        if (n>1) level=extend(level,n);
        Stats s=evaluate(level,n,workers);
        std::cout<<n<<" "<<s.graphs<<" "<<s.well<<" "<<s.violations<<" ";
        if (s.graphs==s.well) std::cout<<"- - - - -";
        else std::cout<<s.maxGap.str()<<" "<<s.maxRatio.str()<<" "<<s.bestK
                      <<" "<<s.bestSeq.str()<<" "<<s.bestStat.str();
        std::cout<<std::endl;
        std::sort(s.hits.begin(),s.hits.end());
        for (auto &h:s.hits) std::cout<<h<<std::endl;
    }
}

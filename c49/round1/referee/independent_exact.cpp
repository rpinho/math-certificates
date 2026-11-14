// Independent exact checker: merged binary trie, tuple-counting dynamic programs.
// Algorithm by the original clean-room referee; independent.cpp is unchanged.
// Mechanical release adaptation: GMP counts replace fixed-width tuple counts;
// elapsed time uses integer nanoseconds. No recurrence or acceptance rule changes.
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using U = uint64_t;
struct Node { uint32_t lo, hi; };
struct Tri {
    uint32_t a,b,c;
    bool operator==(const Tri& t) const { return a==t.a && b==t.b && c==t.c; }
};
struct Hash {
    size_t operator()(const Tri& t) const {
        U h=t.a; h=(h*1000003)^t.b; return (h*1000003)^t.c;
    }
};
struct Diagram {
    std::vector<Node> nodes{{0,0},{0,0}}; // 0: empty family; 1: singleton empty suffix
    std::unordered_map<U,uint32_t> unique;
    std::unordered_map<U,mpz_class> pairs;
    std::unordered_map<Tri,mpz_class,Hash> triples;
    std::vector<uint32_t> masks;
    uint32_t root;
    uint32_t build(size_t l, size_t r, int bit) {
        if(l==r) return 0;
        if(bit<0) return 1;
        size_t s=l;
        // Integer sorting makes this bit's zero branch precede its one branch.
        while(s<r && !(masks[s] & (1u<<bit))) ++s;
        auto lo=build(l,s,bit-1), hi=build(s,r,bit-1);
        U key=(U(lo)<<32)|hi;
        auto it=unique.find(key);
        if(it!=unique.end()) return it->second;
        uint32_t id=nodes.size(); nodes.push_back({lo,hi}); unique[key]=id;
        return id;
    }
    Diagram(std::vector<uint32_t> f):masks(std::move(f)) {
        std::sort(masks.begin(),masks.end()); root=build(0,masks.size(),27);
    }
    // Number of ordered (A,B) with A subseteq B, including equality.
    mpz_class contain(uint32_t a,uint32_t b) {
        if(!a || !b) return 0;
        if(a==1 && b==1) return 1;
        U key=(U(a)<<32)|b;
        auto it=pairs.find(key); if(it!=pairs.end()) return it->second;
        auto x=nodes[a], y=nodes[b];
        mpz_class count=contain(x.lo,y.lo)+contain(x.lo,y.hi)+contain(x.hi,y.hi);
        pairs.emplace(key,count); return count;
    }
    // Number of ordered triples (A,B,C), with repetitions permitted,
    // having equal pairwise intersections. Allowed per-bit patterns:
    // 000, 100, 010, 001, 111.
    mpz_class sunflower(uint32_t a,uint32_t b,uint32_t c) {
        if(!a || !b || !c) return 0;
        if(a==1 && b==1 && c==1) return 1;
        if(a>b) std::swap(a,b); if(b>c) std::swap(b,c); if(a>b) std::swap(a,b);
        Tri key{a,b,c};
        auto it=triples.find(key); if(it!=triples.end()) return it->second;
        if(triples.size()>15000000) throw std::runtime_error("tuple cache safety limit");
        auto x=nodes[a],y=nodes[b],z=nodes[c];
        mpz_class count=sunflower(x.lo,y.lo,z.lo)+sunflower(x.hi,y.lo,z.lo)
            +sunflower(x.lo,y.hi,z.lo)+sunflower(x.lo,y.lo,z.hi)
            +sunflower(x.hi,y.hi,z.hi);
        triples.emplace(key,count); return count;
    }
};
int main(int argc,char**argv) {
    try {
        if(argc<2) throw std::runtime_error("usage: independent MASKS [literal]");
        auto start=std::chrono::steady_clock::now();
        std::ifstream f(argv[1]); if(!f) throw std::runtime_error("cannot open masks");
        std::vector<uint32_t> v; std::string token;
        while(f>>token) {
            if(token.empty() || token.find_first_not_of("0123456789")!=std::string::npos)
                throw std::runtime_error("noninteger mask");
            U x=std::stoull(token); if(x>=(1u<<28)) throw std::runtime_error("out-of-range mask");
            v.push_back(x);
        }
        if(v.empty() || v.size()>300000) throw std::runtime_error("unsupported family size");
        std::sort(v.begin(),v.end());
        if(std::adjacent_find(v.begin(),v.end())!=v.end()) throw std::runtime_error("duplicate mask");
        size_t N=v.size(); std::array<U,4> ports{};
        for(auto x:v) ++ports[((x&1)<<1)|((x>>1)&1)];
        Diagram d(v);
        mpz_class P=d.contain(d.root,d.root), T=d.sunflower(d.root,d.root,d.root);
        // T = N (all equal) + 3(P-N) (exactly two equal) + D (all distinct).
        mpz_class D=T-3*P+2*N;
        bool valid=P==N && D==0;
        std::cout << "{\"members\":"<<N<<",\"nodes\":"<<d.nodes.size()
          <<",\"containment_states\":"<<d.pairs.size()<<",\"sunflower_states\":"<<d.triples.size()
          <<",\"ordered_containment_pairs\":"<<P<<",\"ordered_sunflower_tuples\":"<<T
          <<",\"distinct_sunflowers\":"<<D/6<<",\"ports\":["<<ports[0]<<","<<ports[1]<<","<<ports[2]<<","<<ports[3]<<"]"
          <<",\"valid\":"<<(valid?"true":"false");
        if(argc>2 && std::string(argv[2])=="literal") {
            mpz_class lp=0,lt=0;
            for(size_t i=0;i<N;++i) for(size_t j=i+1;j<N;++j) {
                uint32_t ab=v[i]&v[j];
                if(ab==v[i] || ab==v[j]) ++lp;
                for(size_t k=j+1;k<N;++k)
                    if(ab==(v[i]&v[k]) && ab==(v[j]&v[k])) ++lt;
            }
            std::cout << ",\"literal_proper_containments\":"<<lp<<",\"literal_distinct_sunflowers\":"<<lt;
            if(lp!=P-N || lt!=D/6) throw std::runtime_error("literal cross-check mismatch");
        }
        auto elapsed_ns=std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now()-start).count();
        std::cout << ",\"elapsed_nanoseconds\":"<<elapsed_ns<<"}\n";
        return valid?0:1;
    } catch(const std::exception& e) { std::cerr<<e.what()<<"\n"; return 2; }
}

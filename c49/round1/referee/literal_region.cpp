// Literal triple enumeration: each listed pivot and every pair of other members.
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
#include <unistd.h>
std::vector<uint32_t> read(const char* path) {
    std::ifstream f(path); std::vector<uint32_t> v; uint32_t x;
    while(f>>x) v.push_back(x); return v;
}
int main(int argc,char**argv) {
    if(argc!=3) return 2;
    auto v=read(argv[1]), pivots=read(argv[2]);
    uint64_t total=0, found=0, contained=0;
    std::cerr<<"pid "<<getpid()<<"\n";
    for(auto a:pivots) {
        uint64_t count=0, tests=0;
        for(size_t j=0;j<v.size();++j) {
            auto b=v[j]; if(b==a) continue;
            auto ab=a&b;
            contained+=(ab==a || ab==b);
            for(size_t k=j+1;k<v.size();++k) {
                auto c=v[k];
                if(c==a) continue;
                count+=((a&c)==ab && (b&c)==ab);
                ++tests;
            }
        }
        total+=tests; found+=count;
        std::cerr<<"pivot "<<a<<": "<<tests<<" literal triples, "<<count<<" sunflowers\n";
    }
    std::cout<<"{\"pivots\":"<<pivots.size()<<",\"members\":"<<v.size()
      <<",\"pivot_triple_tests\":"<<total<<",\"sunflowers\":"<<found
      <<",\"proper_containment_incidences\":"<<contained<<"}\n";
    return (found || contained)?1:0;
}

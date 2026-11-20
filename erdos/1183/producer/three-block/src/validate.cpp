// Enumerate closed physical set systems by closing one-generator extensions.
#include <iostream>
#include <unordered_set>
#include "finder.hpp"
namespace old {
#define main prior_main
#include "two_block_grid.cpp"
#undef main
}
using Bits=uint64_t;
static int pc(Bits x) {return __builtin_popcountll(x);}
Bits close(Bits f) {
    std::vector<int> v;
    for(Bits b=f;b;b&=b-1) v.push_back(__builtin_ctzll(b));
    for(size_t j=0;j<v.size();++j) for(size_t k=0;k<j;++k)
        for(int s:{v[k]|v[j],v[k]&v[j]}) if(!(f&(Bits(1)<<s))) {
            f|=Bits(1)<<s;
            v.push_back(s);
        }
    return f;
}
int main(){
    uint64_t total=0,paired=0;
    for(int n=0;n<=5;++n){
        int cube=1<<n;
        std::vector<Bits> families{0};
        std::unordered_set<Bits> seen{0};
        for(size_t j=0;j<families.size();++j)
            for(int x=0;x<cube;++x) if(!(families[j]&(Bits(1)<<x))){
                Bits f=close(families[j]|(Bits(1)<<x));
                if(seen.insert(f).second) families.push_back(f);
            }
        for(int a=0;a<=n;++a) for(int b=0;b<=n-a;++b) {
            int d=n-a-b,k=(a+1)*(b+1)*(d+1),m=1<<k;
            int cell[32];
            for(int s=0;s<cube;++s) cell[s]=pc(s&ones(a))+(a+1)*(pc((s>>a)&ones(b))+(b+1)*pc(s>>(a+b)));
            std::vector<int> h(m);
            for(Bits f:families){
                int image=0;
                for(Bits g=f;g;g&=g-1) image|=1<<cell[__builtin_ctzll(g)];
                h[image]=std::max(h[image],pc(f));
            }
            for(int j=0;j<k;++j) for(int w=0;w<m;++w)
                if(w>>j&1) h[w]=std::max(h[w],h[w^(1<<j)]);
            for(int w=0;w<m;++w) {
                std::string t(k,'0');
                for(int j=0;j<k;++j) t[j]+=(w>>j)&1;
                for(int c=0;c<2;++c){
                    auto f=Finder({a,b,d},t,c,cube+1).run();
                    int expect=h[c?w:m-1-w];
                    if(int(f.size())!=expect) return 1;
                    Bits physical=0;
                    for(auto s:f) {
                        if(s>=unsigned(cube) || t[cell[s]]!='0'+c) return 2;
                        physical|=Bits(1)<<s;
                    }
                    if(pc(physical)!=expect || close(physical)!=physical) return 3;
                    if(!a || !b || !d) {
                        int u=a?a:b;
                        if(int(old::Finder{u,n-u,c,cube+1,t}.run().size())!=expect) return 4;
                        ++paired;
                    }
                    ++total;
                }
            }
        }
        std::cout<<"n "<<n<<" physical families "<<families.size()-1
                 <<" cumulative colour maxima "<<total<<" empty-axis comparisons "<<paired<<std::endl;
    }
    // Each facet of the 4-cube is a monochromatic Boolean 3-cube.
    if(Finder({1,1,1},std::string(8,'0'),0,7).run().size()<7) return 5;
    if(Finder({1,1,1},std::string(8,'0'),0,9).run().size()!=8) return 6;
    for(int c=0;c<2;++c)
        if(Finder({2,1,1},"000000111111",c,17).run().size()!=8) return 7;
    std::cout<<"monochrome Boolean 3-cube: maximum 8 in each facet, threshold 7 accepted; zero mismatches\n";
}

// Exhaustive GF(5) row-space checker.
#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <thread>
#include <vector>
#include <unistd.h>
#ifdef __aarch64__
#include <arm_neon.h>
#endif
using Row = std::array<uint8_t,128>;
using Matrix = std::vector<Row>;
uint64_t pow5(int j) { uint64_t x=1; while(j--) x*=5; return x; }
void add(Row& x, const Row& y, int padded) {
#ifdef __aarch64__
    auto five=vdupq_n_u8(5);
    for(int c=0;c<padded;c+=16) {
        auto a=vaddq_u8(vld1q_u8(x.data()+c),vld1q_u8(y.data()+c));
        a=vsubq_u8(a,vandq_u8(vcgeq_u8(a,five),five));
        vst1q_u8(x.data()+c,a);
    }
#else
    for(int c=0;c<padded;++c) { int v=x[c]+y[c]; x[c]=v>=5?v-5:v; }
#endif
}
int weight(const Row& x, int padded) {
#ifdef __aarch64__
    auto s=vdupq_n_u8(0), one=vdupq_n_u8(1), zero=vdupq_n_u8(0);
    for(int c=0;c<padded;c+=16)
        s=vaddq_u8(s,vandq_u8(vcgtq_u8(vld1q_u8(x.data()+c),zero),one));
    return vaddvq_u8(s);
#else
    int w=0; for(int c=0;c<padded;++c) w+=x[c]!=0; return w;
#endif
}
int rank(Matrix a,int n) {
    int r=0; const int inv[5]={0,1,3,2,4};
    for(int c=0;c<n && r<(int)a.size();++c) {
        int p=r; while(p<(int)a.size() && !a[p][c]) ++p;
        if(p==(int)a.size()) continue;
        std::swap(a[p],a[r]); int t=inv[a[r][c]];
        for(int z=0;z<n;++z) a[r][z]=(a[r][z]*t)%5;
        for(int i=r+1;i<(int)a.size();++i) {
            t=a[i][c];
            for(int z=0;z<n;++z) a[i][z]=(a[i][z]+5-t*a[r][z]%5)%5;
        }
        ++r;
    }
    return r;
}
struct Task { int j,low; uint64_t high; };
struct Result {
    std::array<uint64_t,129> hist{};
    int best=129;
    std::vector<int> msg;
    Row word{};
};
int main(int argc,char** argv) {
    try {
        auto start=std::chrono::steady_clock::now();
        if(argc!=3) throw std::runtime_error("usage: checker MATRIX THREADS");
        int nt=std::stoi(argv[2]);
        if(nt<1 || nt>4) throw std::runtime_error("threads must be 1..4");
        std::ifstream f(argv[1]); if(!f) throw std::runtime_error("cannot open matrix");
        Matrix g; int n=-1; std::string line;
        while(std::getline(f,line)) {
            std::istringstream s(line); Row a{}; int v,c=0;
            while(s>>v) { if(c>=128 || v<0 || v>4) throw std::runtime_error("invalid entry/width"); a[c++]=v; }
            if(!s.eof()) throw std::runtime_error("invalid matrix token");
            if(!c) continue;
            if(n<0) n=c;
            if(c!=n) throw std::runtime_error("unequal row lengths");
            g.push_back(a);
        }
        int k=g.size(); if(k<1 || k>14) throw std::runtime_error("supported rows: 1..14");
        int r=rank(g,n);
        std::cerr<<"pid="<<getpid()<<" n="<<n<<" rows="<<k<<" rank="<<r<<" threads="<<nt<<std::endl;
        if(r!=k) throw std::runtime_error("dependent rows: reduce to independent basis before enumeration");
        int padded=((n+15)/16)*16;
        std::vector<Task> tasks;
        for(int j=0;j<k;++j) {
            int low=std::min(j,8);
            for(uint64_t h=0;h<pow5(j-low);++h) tasks.push_back({j,low,h});
        }
        std::atomic<size_t> next{0};
        std::vector<Result> out(nt);
        std::vector<std::thread> workers;
        for(int id=0;id<nt;++id) workers.emplace_back([&,id] {
            auto& o=out[id]; size_t ti;
            while((ti=next.fetch_add(1))<tasks.size()) {
                auto t=tasks[ti]; Row x=g[t.j]; std::vector<int> msg(k,0); msg[t.j]=1;
                uint64_t h=t.high;
                for(int c=t.low;c<t.j;++c) {
                    msg[c]=h%5; h/=5;
                    for(int a=0;a<msg[c];++a) add(x,g[c],padded);
                }
                uint64_t count=pow5(t.low);
                for(uint64_t a=0;a<count;++a) {
                    int w=weight(x,padded); ++o.hist[w];
                    if(w<o.best) { o.best=w; o.msg=msg; o.word=x; }
                    if(a+1==count) break;
                    // Base-five odometer: even 4 -> 0 is +1 in GF(5).
                    for(int c=0;c<t.low;++c) {
                        add(x,g[c],padded);
                        if(++msg[c]<5) break;
                        msg[c]=0;
                    }
                }
            }
        });
        for(auto& w:workers) w.join();
        Result total;
        for(auto& o:out) {
            for(int w=0;w<=n;++w) total.hist[w]+=o.hist[w];
            if(o.best<total.best) { total.best=o.best; total.msg=o.msg; total.word=o.word; }
        }
        uint64_t visited=std::accumulate(total.hist.begin(),total.hist.end(),uint64_t(0));
        uint64_t expected=(pow5(k)-1)/4;
        if(visited!=expected || total.hist[0]) throw std::runtime_error("enumeration count/zero failure");
        double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cout<<"{\n  \"n\": "<<n<<", \"rank\": "<<r<<", \"threads\": "<<nt
          <<",\n  \"projective_messages\": "<<visited<<", \"expected\": "<<expected
          <<",\n  \"minimum_distance\": "<<total.best<<", \"minimum_codewords\": "<<4*total.hist[total.best]
          <<",\n  \"elapsed_seconds\": "<<sec<<",\n  \"witness_message\": [";
        for(int c=0;c<k;++c) std::cout<<(c?",":"")<<total.msg[c];
        std::cout<<"],\n  \"witness_codeword\": [";
        for(int c=0;c<n;++c) std::cout<<(c?",":"")<<int(total.word[c]);
        std::cout<<"],\n  \"weight_enumerator\": {\"0\": 1";
        for(int w=1;w<=n;++w) if(total.hist[w]) std::cout<<", \""<<w<<"\": "<<4*total.hist[w];
        std::cout<<"}\n}\n";
    } catch(const std::exception& e) { std::cerr<<e.what()<<"\n"; return 1; }
}

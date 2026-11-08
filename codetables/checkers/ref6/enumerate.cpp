// Clean-room projective information-vector enumeration over GF(9).
// Polynomial encoding a+3b with t^2=2; packed arithmetic is componentwise GF(3).
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <mutex>
#include <stdexcept>
#include <thread>
#include <vector>
using U=uint64_t;
struct Word { U a[2]{},b[2]{},c[2]{},d[2]{}; };
inline Word plus(const Word& x,const Word& y){
    Word z;
    for(int i=0;i<2;i++){
        U t=(x.a[i]|x.b[i])&(y.a[i]|y.b[i]);
        z.a[i]=((x.a[i]^y.a[i])&~t)|(x.b[i]&y.b[i]);
        z.b[i]=((x.b[i]^y.b[i])&~t)|(x.a[i]&y.a[i]);
        t=(x.c[i]|x.d[i])&(y.c[i]|y.d[i]);
        z.c[i]=((x.c[i]^y.c[i])&~t)|(x.d[i]&y.d[i]);
        z.d[i]=((x.d[i]^y.d[i])&~t)|(x.c[i]&y.c[i]);
    }
    return z;
}
inline int weight(const Word& x){return __builtin_popcountll(x.a[0]|x.b[0]|x.c[0]|x.d[0])+__builtin_popcountll(x.a[1]|x.b[1]|x.c[1]|x.d[1]);}
void put(Word& w,int j,int v){U bit=U(1)<<(j%64);int i=j/64;if(v%3==1)w.a[i]|=bit;if(v%3==2)w.b[i]|=bit;if(v/3==1)w.c[i]|=bit;if(v/3==2)w.d[i]|=bit;}
int get(const Word&w,int j){int i=j/64,b=j%64;return ((w.a[i]>>b)&1)+2*((w.b[i]>>b)&1)+3*((w.c[i]>>b)&1)+6*((w.d[i]>>b)&1);}
int add9(int x,int y){return (x%3+y%3)%3+3*((x/3+y/3)%3);}
int mul9(int x,int y){return ((x%3)*(y%3)-(x/3)*(y/3)+9)%3+3*(((x%3)*(y/3)+(x/3)*(y%3))%3);}
U choose(int n,int r){U v=1;for(int i=1;i<=r;i++)v=v*(n-r+i)/i;return v;}
std::mutex output_mutex;
struct Job{
    int id,n,k,depth,rank,best;U count=0;Word witness;
    std::vector<std::array<Word,9>> rows;
    void visit(const Word&w){++count;int v=weight(w);if(v<best){best=v;witness=w;}}
    void extend(int start,int left,const Word&w){
        if(left==1){
            for(int j=start;j<k;j++)for(int a=1;a<9;a++)visit(plus(w,rows[j][a]));
            return;
        }
        for(int j=start;j<=k-left;j++)for(int a=1;a<9;a++)extend(j+1,left-1,plus(w,rows[j][a]));
    }
    void run(){
        const auto begin=std::chrono::steady_clock::now();best=n+1;
        for(int r=1;r<=depth;r++){
            count=0;
            for(int j=0;j<=k-r;j++){
                if(r==1)visit(rows[j][1]);
                else extend(j+1,r-1,rows[j][1]);
            }
            U expect=choose(k,r);for(int a=1;a<r;a++)expect*=8;
            if(count!=expect)throw std::runtime_error("enumeration count mismatch");
            double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
            std::lock_guard<std::mutex> lock(output_mutex);
            std::cout<<"{\"set\":"<<id<<",\"depth\":"<<r<<",\"count\":"<<count<<",\"min\":"<<best<<",\"seconds\":"<<sec<<",\"word\":[";
            for(int j=0;j<n;j++){if(j)std::cout<<',';std::cout<<get(witness,j);}std::cout<<"]}"<<std::endl;
        }
    }
};
int main(int argc,char**argv){
    if(argc!=3){std::cerr<<"usage: enumerate INPUT THREADS\n";return 2;}
    for(int a=0;a<9;a++)for(int b=0;b<9;b++){
        Word x,y;for(int j=0;j<128;j++){put(x,j,a);put(y,j,b);}Word z=plus(x,y);
        for(int j=0;j<128;j++)if(get(z,j)!=add9(a,b))throw std::runtime_error("packed arithmetic");
        if(weight(z)!=(add9(a,b)?128:0))throw std::runtime_error("packed weight");
    }
    std::ifstream f(argv[1]);int nj,n,k;f>>nj>>n>>k;
    if(!f||n>128||k<1)throw std::runtime_error("input");
    std::vector<Job>jobs(nj);
    for(auto&j:jobs){f>>j.id>>j.depth>>j.rank;j.n=n;j.k=k;j.rows.resize(k);
        for(int i=0;i<k;i++)for(int c=0;c<n;c++){
            int x;f>>x;if(x<0||x>8)throw std::runtime_error("entry");
            for(int a=1;a<9;a++)put(j.rows[i][a],c,mul9(a,x));
        }
    }
    if(!f)throw std::runtime_error("truncated input");
    int nt=std::stoi(argv[2]);if(nt<1||nt>4)throw std::runtime_error("threads");
    std::atomic<int>next{0};std::vector<std::thread>threads;
    for(int i=0;i<nt;i++)threads.emplace_back([&]{for(;;){int x=next.fetch_add(1);if(x>=nj)break;jobs[x].run();}});
    for(auto&t:threads)t.join();
}

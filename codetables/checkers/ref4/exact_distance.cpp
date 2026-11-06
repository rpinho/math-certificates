// Clean-room Brouwer-Zimmermann enumeration. No external code/library.
#include <arm_neon.h>
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <mutex>
#include <numeric>
#include <random>
#include <sstream>
#include <thread>
#include <vector>
using namespace std;
using Clock=chrono::steady_clock;
int add9(int x,int y){return (x%3+y%3)%3+3*((x/3+y/3)%3);}
int mul9(int x,int y){return ((x%3)*(y%3)+6-(x/3)*(y/3))%3+3*(((x%3)*(y/3)+(x/3)*(y%3))%3);}
// One-hot planes for the two nonzero digits of each GF(3) component.
struct Packed { uint64x2_t a,b,c,d; };
Packed zero(){auto z=vdupq_n_u64(0);return {z,z,z,z};}
inline void add3(uint64x2_t a,uint64x2_t b,uint64x2_t c,uint64x2_t d,uint64x2_t &r,uint64x2_t &s){
    auto za=vmvnq_u32(vreinterpretq_u32_u64(vorrq_u64(a,b)));
    auto zb=vmvnq_u32(vreinterpretq_u32_u64(vorrq_u64(c,d)));
    r=vorrq_u64(vorrq_u64(vandq_u64(vreinterpretq_u64_u32(za),c),vandq_u64(a,vreinterpretq_u64_u32(zb))),vandq_u64(b,d));
    s=vorrq_u64(vorrq_u64(vandq_u64(vreinterpretq_u64_u32(za),d),vandq_u64(b,vreinterpretq_u64_u32(zb))),vandq_u64(a,c));
}
inline Packed plus9(const Packed &x,const Packed &y){Packed z;add3(x.a,x.b,y.a,y.b,z.a,z.b);add3(x.c,x.d,y.c,y.d,z.c,z.d);return z;}
inline int weight(const Packed &x){return vaddvq_u8(vcntq_u8(vreinterpretq_u8_u64(vorrq_u64(vorrq_u64(x.a,x.b),vorrq_u64(x.c,x.d)))));}
Packed pack(const vector<int> &v){
    uint64_t p[4][2]{};
    for(int j=0;j<(int)v.size();j++){
        int a=v[j]%3,b=v[j]/3;
        if(a)p[a-1][j/64]|=uint64_t(1)<<(j%64);
        if(b)p[b+1][j/64]|=uint64_t(1)<<(j%64);
    }
    return {vld1q_u64(p[0]),vld1q_u64(p[1]),vld1q_u64(p[2]),vld1q_u64(p[3])};
}
vector<int> unpack(const Packed &v,int n){
    uint64_t p[4][2];vst1q_u64(p[0],v.a);vst1q_u64(p[1],v.b);vst1q_u64(p[2],v.c);vst1q_u64(p[3],v.d);
    vector<int> r(n);for(int j=0;j<n;j++)for(int i=0;i<4;i++)if((p[i][j/64]>>(j%64))&1)r[j]+=(i==0?1:i==1?2:i==2?3:6);return r;
}
void selftest(){
    for(int x=0;x<9;x++)for(int y=0;y<9;y++){
        vector<int>a(128,x),b(128,y),c(128,add9(x,y));
        assert(unpack(plus9(pack(a),pack(b)),128)==c);
    }
    mt19937 rng(731);
    for(int trial=0;trial<1000;trial++){
        vector<int>a(92),b(92),c(92);
        for(int j=0;j<92;j++){a[j]=rng()%9;b[j]=rng()%9;c[j]=add9(a[j],b[j]);}
        auto z=plus9(pack(a),pack(b));assert(unpack(z,92)==c);
        assert(weight(z)==count_if(c.begin(),c.end(),[](int x){return x!=0;}));
    }
}
struct Task{int set;vector<int> support;};
struct Result{uint64_t count=0;int best=1000,set=-1;vector<int> coeff;Packed witness=zero();};
struct Enumerator{
    const vector<array<Packed,9>> &rows; const Task &task; Result &out; vector<int> coeff;
    Enumerator(const vector<array<Packed,9>>&r,const Task&t,Result&o,int k):rows(r),task(t),out(o),coeff(k){}
    inline void record(const Packed &v){
        ++out.count;int w=weight(v);
        if(w<out.best){out.best=w;out.set=task.set;out.coeff=coeff;out.witness=v;}
    }
    void recurse(int pos,const Packed &sum){
        int row=task.support[pos];
        if(pos+1==(int)task.support.size()){
            for(int a=1;a<9;a++){coeff[row]=a;record(plus9(sum,rows[row][a]));}
        }else{
            for(int a=1;a<9;a++){coeff[row]=a;recurse(pos+1,plus9(sum,rows[row][a]));}
        }
    }
    void run(){int r=task.support[0];coeff[r]=1;if(task.support.size()==1)record(rows[r][1]);else recurse(1,rows[r][1]);}
};
void supports(int k,int w,int first,vector<int>&s,int set,vector<Task>&tasks){
    if(w==0){tasks.push_back({set,s});return;}
    for(int j=first;j<=k-w;j++){s.push_back(j);supports(k,w-1,j+1,s,set,tasks);s.pop_back();}
}
uint64_t choose(int n,int k){uint64_t x=1;for(int i=1;i<=k;i++)x=x*(n-i+1)/i;return x;}
int main(int argc,char**argv){
    if(argc!=4){cerr<<"usage: exact_distance data threads result.json\n";return 1;}
    selftest();auto begin=Clock::now();int n,k,m;ifstream in(argv[1]);in>>n>>k>>m;
    assert(in&&n<=128&&n>0&&k>0&&m>0);int threads=stoi(argv[2]);assert(threads>=1&&threads<=4);
    vector<vector<array<Packed,9>>> matrices(m,vector<array<Packed,9>>(k));
    for(int s=0;s<m;s++)for(int i=0;i<k;i++){
        vector<int> row(n);for(auto &x:row){in>>x;assert(in&&x>=0&&x<9);}
        for(int a=0;a<9;a++){vector<int> v(n);for(int j=0;j<n;j++)v[j]=mul9(a,row[j]);matrices[s][i][a]=pack(v);}
    }
    Result overall;int completed=0,lower=1;uint64_t total=0;
    cout<<"{\"event\":\"start\",\"n\":"<<n<<",\"k\":"<<k<<",\"sets\":"<<m<<",\"threads\":"<<threads<<",\"packed_tests\":\"passed\"}"<<endl;
    for(int w=1;w<=k;w++){
        vector<Task>tasks;vector<int>s;for(int j=0;j<m;j++)supports(k,w,0,s,j,tasks);
        atomic<size_t>next{0};vector<Result> results(threads);vector<thread> pool;
        for(int t=0;t<threads;t++)pool.emplace_back([&,t]{
            while(true){size_t j=next.fetch_add(1);if(j>=tasks.size())break;
                Enumerator e(matrices[tasks[j].set],tasks[j],results[t],k);e.run();}
        });
        for(auto &t:pool)t.join();
        uint64_t count=0;for(auto &r:results){count+=r.count;if(r.best<overall.best)overall=r;}
        uint64_t expected=m*choose(k,w);for(int i=1;i<w;i++)expected*=8;
        assert(count==expected);total+=count;completed=w;lower=m*(w+1);
        double seconds=chrono::duration<double>(Clock::now()-begin).count();
        cout<<"{\"weight_layer\":"<<w<<",\"enumerated\":"<<count<<",\"total\":"<<total<<",\"upper\":"<<overall.best<<",\"unseen_lower\":"<<lower<<",\"seconds\":"<<seconds<<"}"<<endl;
        if(lower>=overall.best||w==k)break;
    }
    auto witness=unpack(overall.witness,n);double sec=chrono::duration<double>(Clock::now()-begin).count();
    ofstream out(argv[3]);out<<"{\n\"n\":"<<n<<",\"k\":"<<k<<",\"minimum_distance\":"<<overall.best<<",\"completed_weight_layer\":"<<completed<<",\"unseen_lower_bound\":"<<lower<<",\"normalized_words_evaluated\":"<<total<<",\"runtime_seconds\":"<<sec<<",\"witness_set_zero_based\":"<<overall.set<<",\n\"witness_coefficients\":[";
    for(int i=0;i<k;i++)out<<(i?",":"")<<overall.coeff[i];out<<"],\n\"witness_word\":[";
    for(int j=0;j<n;j++)out<<(j?",":"")<<witness[j];out<<"]\n}\n";
    cout<<"{\"event\":\"complete\",\"minimum_distance\":"<<overall.best<<",\"seconds\":"<<sec<<"}"<<endl;
}

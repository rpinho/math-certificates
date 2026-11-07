// Exhaustive GF(9) checker.
#include <array>
#include <atomic>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <thread>
#include <vector>
#include <unistd.h>
using namespace std;
using Row=vector<int>; using Matrix=vector<Row>;
int add9(int x,int y){return (x%3+y%3)%3+3*((x/3+y/3)%3);}
int mul9(int x,int y){return ((x%3)*(y%3)+2*(x/3)*(y/3))%3+3*(((x%3)*(y/3)+(x/3)*(y%3))%3);}
int neg9(int x){return (3-x%3)%3+3*((3-x/3)%3);}
int inv9(int x){for(int y=1;y<9;y++)if(mul9(x,y)==1)return y;assert(false);return 0;}
uint64_t pow9(int k){uint64_t v=1;while(k--)v*=9;return v;}
void field_check(){
 assert(mul9(3,3)==2);assert(add9(1,1)==2);assert(add9(2,1)==0);
 for(int a=0;a<9;a++){
  assert(add9(a,0)==a&&mul9(a,1)==a&&mul9(a,0)==0&&add9(a,neg9(a))==0);
  if(a)assert(mul9(a,inv9(a))==1);
  for(int b=0;b<9;b++){
   assert(add9(a,b)>=0&&add9(a,b)<9&&mul9(a,b)>=0&&mul9(a,b)<9);
   assert(add9(a,b)==add9(b,a)&&mul9(a,b)==mul9(b,a));
   if(a&&b)assert(mul9(a,b)!=0);
   for(int c=0;c<9;c++){
    assert(add9(add9(a,b),c)==add9(a,add9(b,c)));
    assert(mul9(mul9(a,b),c)==mul9(a,mul9(b,c)));
    assert(mul9(a,add9(b,c))==add9(mul9(a,b),mul9(a,c)));
   }
  }
 }
 cout<<"field_axioms: PASS (all elements, pairs, triples; t^2=2)\n";
}
int rank9(Matrix a){int k=a.size(),n=a[0].size(),r=0;for(int j=0;j<n&&r<k;j++){
 int p=r;while(p<k&&a[p][j]==0)p++;if(p==k)continue;swap(a[p],a[r]);
 int v=inv9(a[r][j]);for(int c=0;c<n;c++)a[r][c]=mul9(a[r][c],v);
 for(int i=0;i<k;i++)if(i!=r){int f=neg9(a[i][j]);for(int c=0;c<n;c++)a[i][c]=add9(a[i][c],mul9(f,a[r][c]));}r++;
 }return r;}
Row digits(uint64_t x,int k){Row m(k);for(int i=0;i<k;i++){m[i]=x%9;x/=9;}return m;}
bool normalized(uint64_t x){if(!x)return false;while(x%9==0)x/=9;return x%9==1;}
Row word(const Matrix& g,uint64_t x,int start,int k){Row c(g[0].size());for(int i=0;i<k;i++){int a=x%9;x/=9;for(size_t j=0;j<c.size();j++)c[j]=add9(c[j],mul9(a,g[start+i][j]));}return c;}
struct Packed{uint64_t b[8]={};};
Packed pack(const Row& c,bool negative=false){Packed p;for(size_t j=0;j<c.size();j++){int x=negative?neg9(c[j]):c[j];for(int b=0;b<4;b++)if((x>>b)&1)p.b[4*(j/64)+b]|=uint64_t(1)<<(j%64);}return p;}
inline int weight_sum(const Packed& a,const Packed& minus_b){
 uint64_t x=(a.b[0]^minus_b.b[0])|(a.b[1]^minus_b.b[1])|(a.b[2]^minus_b.b[2])|(a.b[3]^minus_b.b[3]);
 uint64_t y=(a.b[4]^minus_b.b[4])|(a.b[5]^minus_b.b[5])|(a.b[6]^minus_b.b[6])|(a.b[7]^minus_b.b[7]);
 return __builtin_popcountll(x)+__builtin_popcountll(y);
}
struct Result{array<uint64_t,129> hist{};int d=129;uint64_t witness=0,count=0;double seconds=0;};
Result enumerate(const Matrix& g,int nt,bool progress){
 auto begin=chrono::steady_clock::now();int k=g.size(),n=g[0].size(),s=k/2,t=k-s;assert(n<=128&&k<=12);
 uint64_t p=pow9(s),q=pow9(t);vector<Packed> left,right;vector<uint64_t> ids;
 for(uint64_t x=1;x<p;x++)if(normalized(x)){left.push_back(pack(word(g,x,0,s)));ids.push_back(x);}
 right.reserve(q);for(uint64_t y=0;y<q;y++)right.push_back(pack(word(g,y,s,t),true));
 Result res;Packed zero;
 for(uint64_t y=1;y<q;y++)if(normalized(y)){int w=weight_sum(zero,right[y]);res.hist[w]++;res.count++;if(w<res.d){res.d=w;res.witness=p*y;}}
 vector<Result> local(nt);atomic<size_t> next{0},done{0};vector<thread> threads;
 for(int h=0;h<nt;h++)threads.emplace_back([&,h]{auto &r=local[h];for(;;){size_t st=next.fetch_add(16);if(st>=left.size())break;size_t en=min(st+16,left.size());for(size_t i=st;i<en;i++){
  const Packed a=left[i];for(uint64_t y=0;y<q;y++){int w=weight_sum(a,right[y]);r.hist[w]++;if(w<r.d){r.d=w;r.witness=ids[i]+p*y;}}
  r.count+=q;
 }size_t now=done.fetch_add(en-st)+(en-st);if(progress&&now/2048!=(now-(en-st))/2048){double sec=chrono::duration<double>(chrono::steady_clock::now()-begin).count();cerr<<"completed_left="<<now<<"/"<<left.size()<<" seconds="<<sec<<"\n";}
 }});
 for(auto &th:threads)th.join();for(auto &r:local){res.count+=r.count;for(int w=0;w<=n;w++)res.hist[w]+=r.hist[w];if(r.d<res.d){res.d=r.d;res.witness=r.witness;}}
 assert(res.count==(pow9(k)-1)/8);assert(res.hist[0]==0);
 Row c=word(g,res.witness,0,k);int w=0;for(int x:c)w+=x!=0;assert(w==res.d);
 res.seconds=chrono::duration<double>(chrono::steady_clock::now()-begin).count();return res;
}
void control(){
 Matrix rs(4,Row(9));for(int j=0;j<9;j++){int v=1;for(int i=0;i<4;i++){rs[i][j]=v;v=mul9(v,j);}}
 for(int reps: {1,9}){Matrix g(4);for(int i=0;i<4;i++)for(int r=0;r<reps;r++)g[i].insert(g[i].end(),rs[i].begin(),rs[i].end());
 assert(rank9(g)==4);Result e=enumerate(g,1,false);array<uint64_t,129> hist{};
 for(uint64_t x=1;x<pow9(4);x++)if(normalized(x)){auto c=word(g,x,0,4);int w=0;for(int a:c)w+=a!=0;hist[w]++;}
 assert(hist==e.hist);assert(e.d==6*reps);cout<<"RS control ["<<9*reps<<",4,"<<e.d<<"] PASS; representatives="<<e.count<<" seconds="<<e.seconds<<"\n";
 }
}
void show(const Matrix& g,const Result&r){
 cout<<"distance="<<r.d<<"\nrepresentatives="<<r.count<<"\nseconds="<<r.seconds<<"\nwitness_message:";
 for(int x:digits(r.witness,g.size()))cout<<" "<<x;cout<<"\nwitness_word:";for(int x:word(g,r.witness,0,g.size()))cout<<" "<<x;
 cout<<"\nprojective_weight_distribution:\n";for(size_t w=0;w<r.hist.size();w++)if(r.hist[w])cout<<w<<" "<<r.hist[w]<<"\n";cout.flush();
}
int main(int argc,char**argv){
 cout<<"pid="<<getpid()<<"\n";field_check();control();cout.flush();if(argc==1)return 0;
 ifstream in(argv[1]);assert(in);Matrix g;string line;while(getline(in,line)){istringstream ss(line);Row r;int x;while(ss>>x){assert(x>=0&&x<9);r.push_back(x);}if(!r.empty())g.push_back(r);}
 assert(g.size()==12);for(auto&r:g)assert(r.size()==106);int rk=rank9(g);cout<<"n=106 k=12 rank="<<rk<<"\n";assert(rk==12);
 // Compare packed field-sum weight against scalar arithmetic for 10,000 deterministic message pairs.
 uint64_t seed=7;for(int z=0;z<10000;z++){seed=seed*6364136223846793005ULL+1;uint64_t x=seed%pow9(6);seed=seed*6364136223846793005ULL+1;uint64_t y=seed%pow9(6);auto a=word(g,x,0,6),b=word(g,y,6,6);int w=0;for(int j=0;j<106;j++)w+=add9(a[j],b[j])!=0;assert(w==weight_sum(pack(a),pack(b,true)));}
 cout<<"packed/scalar crosscheck: PASS\n";cout.flush();show(g,enumerate(g,4,true));
}

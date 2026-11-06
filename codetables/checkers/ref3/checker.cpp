// Brouwer--Zimmermann information-set enumeration.
#include <arm_neon.h>
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <sstream>
#include <chrono>
#include <algorithm>
#include <cassert>
using namespace std;
static int addfield(int q,int a,int b){return q==5?(a+b)%5:(a%3+b%3)%3+3*((a/3+b/3)%3);}
static int mulfield(int q,int a,int b){return q==5?a*b%5:((a%3*(b%3)-a/3*(b/3)+9)%3)+3*((a%3*(b/3)+a/3*(b%3))%3);}
template<int Q,int L> struct Word {array<uint8x16_t,L> x;};
template<int Q,int L> static inline Word<Q,L> sumword(const Word<Q,L>&a,const Word<Q,L>&b){
 Word<Q,L> c;
 for(int i=0;i<L;i++){
  auto s=vaddq_u8(a.x[i],b.x[i]);
  if constexpr(Q==5) c.x[i]=vsubq_u8(s,vandq_u8(vcgeq_u8(s,vdupq_n_u8(5)),vdupq_n_u8(5)));
  else {
   auto lo=vandq_u8(s,vdupq_n_u8(7)); auto hi=vshrq_n_u8(s,4);
   auto t=vandq_u8(vcgeq_u8(lo,vdupq_n_u8(3)),vdupq_n_u8(3));
   auto u=vandq_u8(vcgeq_u8(hi,vdupq_n_u8(3)),vdupq_n_u8(48));
   c.x[i]=vsubq_u8(vsubq_u8(s,t),u);
  }
 } return c;
}
template<int Q,int L> static inline int weight(const Word<Q,L>&a){
 auto count=vdupq_n_u8(0);
 for(int i=0;i<L;i++) count=vsubq_u8(count,vceqq_u8(a.x[i],vdupq_n_u8(0)));
 return 16*L-vaddvq_u8(count);
}
template<int Q,int L> struct Search{
 using W=Word<Q,L>; int n,k,best,active=0; uint64_t tested=0; vector<int> ranks,depth; vector<vector<array<W,Q>>> bases; vector<int> witness; chrono::steady_clock::time_point start;
 W pack(const vector<int>&v){W w; uint8_t a[16*L]={};for(int j=0;j<n;j++)a[j]=Q==5?v[j]:v[j]%3+16*(v[j]/3);for(int j=0;j<L;j++)w.x[j]=vld1q_u8(a+16*j);return w;}
 vector<int> unpack(const W&w){uint8_t a[16*L]; for(int j=0;j<L;j++)vst1q_u8(a+16*j,w.x[j]);vector<int>v(n);for(int j=0;j<n;j++)v[j]=Q==5?a[j]:(a[j]&15)+3*(a[j]>>4);return v;}
 void visit(const W&w){tested++;int d=weight<Q,L>(w);if(d<best){best=d;witness=unpack(w);cout<<"witness weight="<<best<<" tested="<<tested<<" seconds="<<seconds()<<"\n";cout.flush();}}
 double seconds(){return chrono::duration<double>(chrono::steady_clock::now()-start).count();}
 void walk(int next,int remaining,bool first,const W&current){
  if(remaining==1){for(int i=next;i<k;i++)for(int a=1;a<(first?2:Q);a++)visit(sumword<Q,L>(current,bases[active][i][a]));return;}
  for(int i=next;i<=k-remaining;i++)for(int a=1;a<(first?2:Q);a++)walk(i+1,remaining-1,false,sumword<Q,L>(current,bases[active][i][a]));
 }
 int lower(){int t=0;for(size_t i=0;i<ranks.size();i++)t+=max(0,depth[i]+1-(k-ranks[i]));return t;}
 void run(const string&file,const string&out,int limit){
  start=chrono::steady_clock::now();ifstream in(file);int q,m;in>>q>>n>>k>>m;assert(q==Q&&n<=16*L);best=n+1;
  for(int b=0;b<m;b++){int rank;in>>rank;ranks.push_back(rank);depth.push_back(0);vector<array<W,Q>> rows(k);for(int i=0;i<k;i++){vector<int>v(n);for(int&x:v)in>>x;for(int a=0;a<Q;a++){vector<int>u(n);for(int j=0;j<n;j++)u[j]=mulfield(Q,a,v[j]);rows[i][a]=pack(u);}}bases.push_back(rows);}
  // Check the packed arithmetic against scalar field arithmetic for all pairs.
  for(int a=0;a<Q;a++)for(int b=0;b<Q;b++){vector<int>x(n,a),y(n,b),z(n,addfield(Q,a,b));auto s=sumword<Q,L>(pack(x),pack(y));assert(unpack(s)==z);assert((weight<Q,L>(s)==(addfield(Q,a,b)?n:0)));}
  W zero=pack(vector<int>(n,0)); bool done=false;
  // Every chosen information set enumerates all messages with the given support size,
  // fixing the first nonzero coefficient to one, hence one per scalar orbit.
  for(int r=1;r<=min(k,limit)&&!done;r++){
   for(size_t b=0;b<ranks.size();b++){
    // A block with defect so large that it cannot help before limit is unnecessary.
    if(ranks[b]+limit<k)continue;
    active=b; walk(0,r,true,zero);depth[b]=r;
    cout<<"stage support="<<r<<" block="<<b<<" lower="<<lower()<<" best="<<best<<" tested="<<tested<<" seconds="<<seconds()<<"\n";cout.flush();
    if(lower()>=best){done=true;break;}
   }
  }
  ofstream f(out);f<<"{\n\"q\":"<<Q<<",\"n\":"<<n<<",\"k\":"<<k<<",\"distance\":"<<best<<",\"lower_bound\":"<<lower()<<",\"complete\":"<<(done?"true":"false")<<",\"tested_projective_messages_with_repeats\":"<<tested<<",\"seconds\":"<<seconds()<<",\"depths\":[";
  for(size_t i=0;i<depth.size();i++){if(i)f<<',';f<<depth[i];}f<<"],\"witness\":[";for(size_t j=0;j<witness.size();j++){if(j)f<<',';f<<witness[j];}f<<"]}\n";
 }
};
int main(int argc,char**argv){if(argc<3)return 2;ifstream f(argv[1]);int q;f>>q;int limit=argc>3?stoi(argv[3]):16;if(q==5){Search<5,9>s;s.run(argv[1],argv[2],limit);}else if(q==9){Search<9,7>s;s.run(argv[1],argv[2],limit);}else return 3;}

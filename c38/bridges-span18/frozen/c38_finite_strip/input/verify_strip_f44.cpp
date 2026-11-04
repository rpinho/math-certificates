// Separately written (same agent) verifier for finite strip bridge sums.
// Mathematics: Kesten/Jensen; point evaluation and boundary convention: Vit Planocka.
// This implementation uses explicit component identities and vertex degree constraints,
// rather than the production kernel's case table. It imports no production source.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <limits>
#include <string>
#include <vector>
#include <omp.h>
using U=unsigned __int128;
static int L, M, COLS, S=96, F=44;
static double seconds(){return std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count();}
[[noreturn]] static void fail(const char*s){std::cerr<<"REJECT:"<<s<<"\n";std::exit(2);}
static std::string dec(U n){if(!n)return "0";std::string s;while(n){s+=char('0'+n%10);n/=10;}std::reverse(s.begin(),s.end());return s;}
struct Move{uint64_t key;unsigned k;};
struct Moves{Move a[3];int n=0,c=0;};
// Decode labels to explicit connected-component identities. Each component has
// two live stubs (no terminal), or one live stub (one terminal). A bracket label
// is only serialization; the transition logic below is graph incidence logic.
static Moves vertex(uint64_t key,int r){
 int c[24]={},occ[24]={},term[24]={},stack[24],top=0,nc=0;
 int sf=(key>>(2*(L+2)))&1,ef=(key>>(2*(L+2)+1))&1;
 int E[24]={};for(int j=0;j<=L;j++)E[j]=(key>>(2*j))&3;
 int v=(key>>(2*(L+1)))&3;
 for(int i=0;i<L+2;i++){
  int a=i<r?E[i]:(i==r?v:E[i-1]);
  if(a==0)c[i]=0;
  else if(a==1){c[i]=++nc;stack[top++]=nc;}
  else if(a==2){if(!top)fail("BAD_BRACKET");c[i]=stack[--top];}
  else {c[i]=++nc;term[nc]=1;}
  if(c[i])occ[c[i]]++;
 }
 if(top)fail("BAD_BRACKET");
 int left=c[r+1],down=c[r];
 if(r==0&&(left||down))fail("BOTTOM_INCOMING");
 Moves ans;
 // Local degree: bottom row is empty or start of degree one, top row may
 // create/end the unique endpoint, every other occupied vertex has degree two.
 for(int right=0;right<=1;right++)for(int up=0;up<=1;up++){
  int in=(left!=0)+(down!=0),out=right+up,deg=in+out;
  int nsf=sf,nef=ef;
  bool terminal=false;
  if(r==0){if(right||deg>1)continue;if(deg==1){if(sf)continue;nsf=1;terminal=true;}}
  else {
   if(r==L&&up)continue;
   if(deg==0){}
   else if(deg==2){}
   else if(deg==1&&r==L&&!ef){nef=1;terminal=true;}
   else continue;
  }
  if(in==2&&left==down)continue; // a completed cycle is never a walk
  int labels[24];std::copy(c,c+L+2,labels);
  labels[r]=labels[r+1]=0;
  int representative=0,number_of_terminals=terminal?1:0;
  if(left){representative=left;number_of_terminals+=term[left];}
  if(down){if(!representative)representative=down;number_of_terminals+=term[down];}
  if(deg&&!representative)representative=nc+1;
  if(left&&down)for(int i=0;i<L+2;i++)if(labels[i]==down)labels[i]=representative;
  if(right)labels[r]=representative;
  if(up)labels[r+1]=representative;
  int all=0,ends=0;for(int i=0;i<L+2;i++){all+=labels[i]!=0;ends+=labels[i]==representative&&representative;}
  if(deg&&ends==0){
   if(number_of_terminals==2&&all==0&&nsf&&nef){ans.c++;}
   continue; // never retain a closed component
  }
  if(deg&&number_of_terminals>1)continue;
  int counts[24]={},first[24];std::fill(first,first+24,-1);
  for(int i=0;i<L+2;i++)if(labels[i])counts[labels[i]]++;
  uint64_t outkey=0;int checkstack[24],sp=0;
  for(int i=0;i<L+2;i++){
   int a=labels[i],lab=0;
   if(a){
    if(counts[a]==1)lab=3;
    else if(counts[a]==2){if(first[a]<0){first[a]=i;lab=1;checkstack[sp++]=a;}else {lab=2;if(!sp||checkstack[--sp]!=a)fail("CROSSING_COMPONENTS");}}
    else fail("COMPONENT_DEGREE");
   }
   int slot=i<=r?i:(i==r+1?L+1:i-1);
   outkey|=uint64_t(lab)<<(2*slot);
  }
  if(sp)fail("OUTPUT_BRACKET");
  outkey|=uint64_t(nsf)<<(2*(L+2));outkey|=uint64_t(nef)<<(2*(L+2)+1);
  if(ans.n>=3)fail("TOO_MANY_LOCAL_MOVES");
  ans.a[ans.n++]={outkey,unsigned(out)};
 }
 return ans;
}
static void radix(std::vector<uint64_t>&a){
 std::vector<uint64_t>b(a.size());
 for(int byte=0;byte<8;byte++){
  size_t count[256]={};for(auto k:a)count[(k>>(8*byte))&255]++;
  size_t pos[256],z=0;for(int j=0;j<256;j++){pos[j]=z;z+=count[j];}
  for(auto k:a)b[pos[(k>>(8*byte))&255]++]=k;
  a.swap(b);
 }
 a.erase(std::unique(a.begin(),a.end()),a.end());
}
struct Lookup{
 std::vector<uint64_t>keys;std::vector<uint32_t>values;size_t mask;
 static uint64_t hash(uint64_t k){k^=k>>30;k*=0xbf58476d1ce4e5b9ULL;k^=k>>27;k*=0x94d049bb133111ebULL;return k^(k>>31);}
 Lookup(const std::vector<uint64_t>&a){size_t n=16;while(n<a.size()*2)n*=2;keys.assign(n,UINT64_MAX);values.resize(n);mask=n-1;
  for(size_t i=0;i<a.size();i++){size_t p=hash(a[i])&mask;while(keys[p]!=UINT64_MAX)p=(p+1)&mask;keys[p]=a[i];values[p]=uint32_t(i);}}
 uint32_t find(uint64_t k)const{size_t p=hash(k)&mask;while(keys[p]!=UINT64_MAX){if(keys[p]==k)return values[p];p=(p+1)&mask;}fail("GRAPH_NOT_CLOSED");}
};
// Transposed sparse edges make both directed forward planes parallel over
// destination vertices, with no atomics and no order-dependent sum.
struct Stage{
 std::vector<uint32_t>outstart,outedge,instart,inedge;
 std::vector<uint8_t>complete;
};
static std::vector<std::vector<uint64_t>>keys;
static std::vector<Stage>G;
static std::vector<size_t>sz;
static size_t maxsize;
static void graph(){
 double t=seconds();keys.resize(L+1);keys[0]={0};
 for(int turn=0;turn<64;turn++){
  bool changed=false;
  for(int r=0;r<=L;r++){
   int nr=(r+1)%(L+1);size_t n=keys[r].size();
   std::vector<uint64_t> next(3*n,UINT64_MAX);
   #pragma omp parallel for schedule(static)
   for(size_t i=0;i<n;i++){Moves m=vertex(keys[r][i],r);for(int j=0;j<m.n;j++)next[3*i+j]=m.a[j].key;}
   radix(next);if(!next.empty()&&next.back()==UINT64_MAX)next.pop_back();
   std::vector<uint64_t> merged;merged.reserve(next.size()+keys[nr].size());
   std::set_union(next.begin(),next.end(),keys[nr].begin(),keys[nr].end(),std::back_inserter(merged));
   if(merged.size()!=keys[nr].size()){changed=true;keys[nr].swap(merged);}
  }
  std::cerr<<"closure turn="<<turn<<" stage0="<<keys[0].size()<<" elapsed="<<seconds()-t<<"\n";
  if(!changed)break;if(turn==63)fail("CLOSURE_LIMIT");
 }
 sz.resize(L+1);G.resize(L+1);maxsize=0;
 uint64_t states=0,edges=0;
 for(int r=0;r<=L;r++){sz[r]=keys[r].size();maxsize=std::max(maxsize,sz[r]);states+=sz[r];}
 for(int r=0;r<=L;r++){
  int nr=(r+1)%(L+1);Stage &g=G[r];Lookup target(keys[nr]);
  if(sz[nr]>=(1ULL<<30)||sz[r]*3>=(1ULL<<32))fail("INDEX_CAPACITY");
  g.outstart.resize(sz[r]+1);g.complete.resize(sz[r]);std::vector<uint8_t>num(sz[r]);
  #pragma omp parallel for schedule(static)
  for(size_t i=0;i<sz[r];i++){Moves m=vertex(keys[r][i],r);num[i]=m.n;g.complete[i]=m.c;}
  uint64_t ne=0;for(size_t i=0;i<sz[r];i++){g.outstart[i]=uint32_t(ne);ne+=num[i];}g.outstart[sz[r]]=uint32_t(ne);g.outedge.resize(ne);
  #pragma omp parallel for schedule(static)
  for(size_t i=0;i<sz[r];i++){Moves m=vertex(keys[r][i],r);for(int j=0;j<m.n;j++){
   auto d=target.find(m.a[j].key);if(d==0&&i!=0)fail("NONEMPTY_TO_EMPTY");g.outedge[g.outstart[i]+j]=d|(m.a[j].k<<30);
  }}
  if(g.complete[0])fail("EMPTY_COMPLETES");
  g.instart.assign(sz[nr]+1,0);for(auto e:g.outedge)g.instart[(e&0x3fffffff)+1]++;
  for(size_t i=0;i<sz[nr];i++)g.instart[i+1]+=g.instart[i];
  g.inedge.resize(ne);auto cursor=g.instart;
  for(size_t i=0;i<sz[r];i++)for(auto e=g.outstart[i];e<g.outstart[i+1];e++){
   uint32_t a=g.outedge[e];g.inedge[cursor[a&0x3fffffff]++]=uint32_t(i)|(a&0xc0000000);
  }
  edges+=ne;std::cerr<<"graph stage="<<r<<" states="<<sz[r]<<" edges="<<ne<<" elapsed="<<seconds()-t<<"\n";
 }
 keys.clear();keys.shrink_to_fit();
 std::cerr<<"GRAPH_COMPLETE states="<<states<<" edges="<<edges<<" elapsed="<<seconds()-t<<"\n";
}
// Upper potential is constructed with integer ceilings from zero. A full
// stabilized cycle is then checked again; all components and edges are covered.
static std::vector<uint64_t> potential(){
 std::vector<uint64_t>u0(sz[0]),a(maxsize),b(maxsize);
 const uint64_t wt[3]={1ULL<<54,uint64_t(M)<<27,uint64_t(M)*M};
 for(int it=0;it<2000;it++){
  std::copy(u0.begin(),u0.end(),b.begin());
  auto *src=&b,*dst=&a;
  for(int r=L;r>=0;r--){auto &g=G[r];
   #pragma omp parallel for schedule(static)
   for(size_t i=0;i<sz[r];i++){
    U rhs=U(g.complete[i])<<(F+54);
    for(uint32_t k=g.outstart[i];k<g.outstart[i+1];k++){uint32_t e=g.outedge[k];rhs+=U((*src)[e&0x3fffffff])*wt[e>>30];}
    U n=(rhs+((U(1)<<54)-1))>>54;
    if(n>=(U(1)<<60))fail("POTENTIAL_OVERFLOW");(*dst)[i]=uint64_t(n);
   }
   (*dst)[0]=0;std::swap(src,dst);
  }
  bool equal=std::equal(u0.begin(),u0.end(),src->begin());
  if(it%10==0||equal)std::cerr<<"potential cycle="<<it+1<<" fixed="<<equal<<"\n";
  if(equal){return u0;}
  std::copy(src->begin(),src->begin()+sz[0],u0.begin());
 }
 fail("POTENTIAL_NO_FIXED_POINT");
}
static U weighted(U n,uint64_t mult,unsigned sh,bool ceiling){
 // n<2^107 and mult<2^54. Two 64-bit limbs form exact 192-bit product.
 U low=U(uint64_t(n))*mult,high=U(uint64_t(n>>64))*mult;
 uint64_t p0=uint64_t(low);U middle=(low>>64)+uint64_t(high);
 uint64_t p1=uint64_t(middle),p2=uint64_t(high>>64)+uint64_t(middle>>64);
 if(p2>>sh)fail("PRODUCT_OVERFLOW");
 U out=(U((p1>>sh)|(p2<<(64-sh)))<<64)|((p0>>sh)|(p1<<(64-sh)));
 if(ceiling&&(p0&((1ULL<<sh)-1))){if(out==~U(0))fail("CEILING_OVERFLOW");out++;}return out;
}
static void sweep(const std::vector<uint64_t>&u,const std::string&out){
 std::vector<U>a(2*maxsize),b(2*maxsize);a[0]=a[maxsize]=U(1)<<S;
 U sums[2]={0,0},tail=0;uint64_t weights[3]={1,uint64_t(M),uint64_t(M)*M};
 for(int col=1;col<=COLS;col++){
  for(int r=0;r<=L;r++){auto&g=G[r];int nr=(r+1)%(L+1);
   for(int p=0;p<2;p++)for(size_t i=0;i<sz[r];i++)if(g.complete[i]){
    if(a[p*maxsize+i]>=(U(1)<<107))fail("COMPLETION_OVERFLOW_GUARD");
    U q=a[p*maxsize+i]*g.complete[i];if(sums[p]>~U(0)-q)fail("SUM_OVERFLOW");sums[p]+=q;
   }
   #pragma omp parallel for schedule(static)
   for(size_t k=0;k<2*sz[nr];k++){
    int p=int(k/sz[nr]);size_t i=k%sz[nr];U z=0;
    for(uint32_t j=g.instart[i];j<g.instart[i+1];j++){
     uint32_t e=g.inedge[j];unsigned power=e>>30;U v=a[p*maxsize+(e&0x3fffffff)];
     if(v>=(U(1)<<107))fail("FORWARD_OVERFLOW_GUARD");
     U q=power?weighted(v,weights[power],27*power,p):v;
     if(z>~U(0)-q)fail("ACCUMULATION_OVERFLOW");z+=q;
    }b[p*maxsize+i]=z;
   }a.swap(b);
  }
  if(col==1)a[0]=a[maxsize]=0;
  if(col%25==0||col==COLS)std::cerr<<"column="<<col<<" lo="<<dec(sums[0])<<" hi="<<dec(sums[1])<<"\n";
 }
 for(size_t i=0;i<sz[0];i++){
  U q=weighted(a[maxsize+i],u[i],F,true);if(tail>~U(0)-q)fail("TAIL_OVERFLOW");tail+=q;
 }
 uint64_t nstates=0,nedges=0;for(int r=0;r<=L;r++){nstates+=sz[r];nedges+=G[r].outedge.size();}
 std::ofstream f(out);if(!f)fail("OUTPUT_OPEN");
 f<<"{\"l\":"<<L<<",\"M\":"<<M<<",\"S\":"<<S<<",\"F\":"<<F<<",\"w\":"<<COLS<<",\"total_states\":"<<nstates<<",\"edges\":"<<nedges<<",\"num_lo\":\""<<dec(sums[0])<<"\",\"num_hi\":\""<<dec(sums[1])<<"\",\"num_tail\":\""<<dec(tail)<<"\",\"stage_sizes\":[";
 for(int r=0;r<=L;r++){if(r)f<<",";f<<sz[r];}f<<"],\"status\":\"COMPLETE_SEPARATE_SAME_AGENT_RECOMPUTATION\"}\n";
}
static void polynomial(int N,const std::string&out){
 if(N<1||N>24)fail("POLYNOMIAL_CONTROL_LIMIT");
 std::vector<uint64_t>a(maxsize*(N+1)),b(maxsize*(N+1)),result(N+1);a[0]=1;
 for(int col=0;col<=N;col++){
  for(int r=0;r<=L;r++){auto&g=G[r];int nr=(r+1)%(L+1);
   for(size_t i=0;i<sz[r];i++)if(g.complete[i])for(int n=0;n<=N;n++)result[n]+=a[i*(N+1)+n]*g.complete[i];
   std::fill(b.begin(),b.begin()+sz[nr]*(N+1),0);
   for(size_t i=0;i<sz[r];i++)for(uint32_t j=g.outstart[i];j<g.outstart[i+1];j++){
    uint32_t e=g.outedge[j];unsigned k=e>>30;size_t dst=e&0x3fffffff;
    for(int n=0;n+int(k)<=N;n++){auto v=a[i*(N+1)+n];auto &d=b[dst*(N+1)+n+k];if(d>UINT64_MAX-v)fail("CONTROL_COEFFICIENT_OVERFLOW");d+=v;}
   }a.swap(b);
  }
  if(col==0)a[0]=0;
 }
 std::ofstream f(out);f<<"{\"span\":"<<L<<",\"N\":"<<N<<",\"b\":[";for(int n=0;n<=N;n++){if(n)f<<",";f<<result[n];}f<<"]}\n";
}
int main(int argc,char**argv){
 if(argc==5&&std::string(argv[1])=="--poly"){
 L=std::stoi(argv[2]);if(L<1||L>10)fail("CONTROL_SPAN_LIMIT");graph();polynomial(std::stoi(argv[3]),argv[4]);return 0;
 }
 if(argc!=5){std::cerr<<"usage: verify_strip span M columns out.json\n";return 1;}
 L=std::stoi(argv[1]);M=std::stoi(argv[2]);COLS=std::stoi(argv[3]);
 if(L<1||L>20||M<1||M>=(1<<26)||COLS<1||COLS>10000)fail("PARAMETERS");
 double t=seconds();graph();auto u=potential();sweep(u,argv[4]);std::cerr<<"VERIFIED complete recomputation elapsed="<<seconds()-t<<"\n";
}

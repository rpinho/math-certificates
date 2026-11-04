// Independent referee implementation, written from vertex/path definitions.
// No producer headers, code, state keys, transition tables, or executables used.
#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <deque>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using boost::multiprecision::cpp_int;
using U=uint64_t;
using StateKey=unsigned __int128;
struct StateHash { size_t operator()(StateKey key)const {
 U a=key,b=key>>64;a^=b*0x9e3779b97f4a7c15ULL;
 a^=a>>30;a*=0xbf58476d1ce4e5b9ULL;a^=a>>27;a*=0x94d049bb133111ebULL;
 return a^(a>>31);
}};
struct Edge { int to, power; };
struct Node { StateKey key; int row; std::vector<Edge> out; int finish=0; };
struct Graph {
 int h, slots, flagshift;
 std::vector<Node> nodes;
 std::vector<std::unordered_map<StateKey,int,StateHash>> ids;
 std::vector<std::vector<int>> stages;
 Graph(int span):h(span),slots(span+2),flagshift(4*slots),ids(span+1),stages(span+1) {
  if(span>15) throw std::runtime_error("key capacity");
  get(0,0);
  for(size_t i=0;i<nodes.size();++i) expand(i);
 }
 int get(int row,StateKey key) {
  auto it=ids[row].find(key); if(it!=ids[row].end())return it->second;
  int id=nodes.size(); ids[row][key]=id; stages[row].push_back(id);
  nodes.push_back({key,row,{ },0}); return id;
 }
 StateKey pack(std::array<int,24> a,int flags) {
  int map[16]={},next=1; StateKey k=StateKey(flags)<<flagshift;
  for(int i=0;i<slots;++i) {
   if(a[i] && a[i]<14) {if(!map[a[i]])map[a[i]]=next++; a[i]=map[a[i]];}
   k|=StateKey(a[i])<<(4*i);
  }
  return k;
 }
 void expand(int id) {
  StateKey key=nodes[id].key; int row=nodes[id].row, flags=int(key>>flagshift);
  std::array<int,24>a{};
  for(int i=0;i<slots;++i)a[i]=(key>>(4*i))&15;
  int l=a[row],d=a[h+1],nin=(l!=0)+(d!=0);
  // Enumerate all four outgoing choices and each permitted terminal status.
  for(int right=0;right<=1;++right)for(int up=0;up<=1;++up) {
   if(row==h && up)continue;
   if(row==0 && (l||d||right))continue;
   int nout=right+up, degree=nin+nout;
   for(int terminal=0;terminal<=2;++terminal) {
    if(terminal==1 && (row!=0 || (flags&1)))continue;
    if(terminal==2 && (row!=h || (flags&2)))continue;
    if(terminal ? degree!=1 : (degree!=0 && degree!=2))continue;
    if(row==0 && degree && terminal!=1)continue;
    auto z=a;z[row]=z[h+1]=0;
    int nf=flags|(terminal?1<<(terminal-1):0),lab=0;
    bool completed=false,valid=true;
    if(!degree) { }
    else if(terminal) {
     int t=terminal==1?14:15;
     if(nout)lab=t;
     else {
      int q=l?l:d;
      if(q>=14)completed=true;
      else {bool seen=false;for(int i=0;i<slots;++i)if(z[i]==q){z[i]=t;seen=true;}
       if(!seen)throw std::runtime_error("lost mate");}
     }
    } else if(nin==0) {
     lab=1;for(int i=0;i<slots;++i)if(z[i]<14)lab=std::max(lab,z[i]+1);
     if(lab>=14)throw std::runtime_error("component capacity");
    } else if(nin==1) lab=l?l:d;
    else {
     if(l==d)valid=false; // closes a cycle, never a walk
     else if(l>=14 && d>=14)completed=true;
     else {
      int keep=(l>=14?l:(d>=14?d:l));int drop=(keep==l?d:l);
      for(int i=0;i<slots;++i)if(z[i]==drop)z[i]=keep;
     }
    }
    if(!valid)continue;
    if(completed) {
     bool empty=true;for(int i=0;i<slots;++i)if(z[i])empty=false;
     if(empty && nf==3)nodes[id].finish++;
     continue;
    }
    if(right)z[row]=lab;if(up)z[h+1]=lab;
    StateKey dest=pack(z,nf);
    if(key && !dest)throw std::runtime_error("lost nonempty history");
    int target=get((row+1)%(h+1),dest);
    nodes[id].out.push_back({target,nout});
   }
  }
 }
};
std::string str(const cpp_int&x){return x.convert_to<std::string>();}
// Exact rational finite generating value: a common denominator 2^(54*t)
// after t visited vertices. There is no floating point or directed rounding.
void exact_value(Graph&g,int width,U m,const std::string&path) {
 std::vector<cpp_int>v(g.nodes.size()),next(g.nodes.size());v[0]=1;
 cpp_int total=0; unsigned exponent=0;
 cpp_int mult[3]={cpp_int(1)<<54,cpp_int(m)<<27,cpp_int(m)*m};
 auto begin=std::chrono::steady_clock::now();
 for(int col=0;col<width;++col) {
  for(int row=0;row<=g.h;++row) {
   for(int id:g.stages[(row+1)%(g.h+1)])next[id]=0;
   total<<=54;
   for(int id:g.stages[row])if(v[id]!=0) {
    if(g.nodes[id].finish)total+=(v[id]*g.nodes[id].finish)<<54;
    for(auto e:g.nodes[id].out)next[e.to]+=v[id]*mult[e.power];
    v[id]=cpp_int(); // discard the consumed stage's large denominator storage
   }
   v.swap(next);exponent+=54;
  }
  if(col==0)v[0]=0; // unique translate with first occupied column zero
  if(col%25==0)std::cerr<<"exact h="<<g.h<<" M="<<m<<" column="<<col+1<<"\n";
 }
 // Independently construct an all-width upper potential in units 2^-32.
 // A stabilized backward cycle proves every finite future sum is bounded.
 const int f=32;std::vector<cpp_int>pot(g.nodes.size());
 cpp_int q=cpp_int(1)<<54, wt[3]={q,cpp_int(m)<<27,cpp_int(m)*m};
 int cycles=0;bool changed=true;
 while(changed) {
  changed=false;if(++cycles>100000)throw std::runtime_error("potential cap");
  for(int row=g.h;row>=0;--row)for(int id:g.stages[row]) {
   if(g.nodes[id].key==0)continue;
   cpp_int rhs=cpp_int(g.nodes[id].finish)<<(f+54);
   for(auto e:g.nodes[id].out)rhs+=wt[e.power]*pot[e.to];
   cpp_int u=(rhs+q-1)>>54;
   if(u<pot[id])throw std::runtime_error("potential decreased");
   if(u!=pot[id]){changed=true;pot[id]=u;}
  }
 }
 // Directly check inequalities again with no iterative assumptions.
 for(size_t id=0;id<g.nodes.size();++id)if(g.nodes[id].key!=0) {
  cpp_int rhs=cpp_int(g.nodes[id].finish)<<(f+54);
  for(auto e:g.nodes[id].out)rhs+=wt[e.power]*pot[e.to];
  if((pot[id]<<54)<rhs)throw std::runtime_error("bad potential");
 }
 cpp_int tail=0;for(int id:g.stages[0])tail+=v[id]*pot[id];
 unsigned tz=total==0?0:boost::multiprecision::lsb(total);
 unsigned tt=tail==0?0:boost::multiprecision::lsb(tail);
 std::ofstream out(path);
 out<<"{\n\"span\":"<<g.h<<",\"width\":"<<width<<",\"M\":"<<m
    <<",\"nodes\":"<<g.nodes.size()<<",\"potential_cycles\":"<<cycles
    <<",\"finite_numerator\":\""<<str(total>>tz)<<"\",\"finite_denominator_exponent\":"<<exponent-tz
    <<",\"tail_numerator\":\""<<str(tail>>tt)<<"\",\"tail_denominator_exponent\":"<<exponent+f-tt
    <<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()<<"\n}\n";
}
// Full length-truncated bridge coefficients. Range <= n for an n-edge walk,
// so N+1 columns contain every translated walk of length at most N.
void coefficients(Graph&g,int N,const std::string&path) {
 using Poly=std::vector<cpp_int>;
 std::vector<Poly>v(g.nodes.size(),Poly(N+1)),next(v);v[0][0]=1;
 Poly total(N+1);
 for(int col=0;col<=N;++col) {
  for(int row=0;row<=g.h;++row) {
   for(int id:g.stages[(row+1)%(g.h+1)])for(auto&x:next[id])x=0;
   for(int id:g.stages[row])for(int n=0;n<=N;++n)if(v[id][n]!=0) {
    if(g.nodes[id].finish)total[n]+=v[id][n]*g.nodes[id].finish;
    for(auto e:g.nodes[id].out)if(n+e.power<=N)next[e.to][n+e.power]+=v[id][n];
   }
   v.swap(next);
  }
  if(col==0)for(auto&x:v[0])x=0;
 }
 std::ofstream out(path);out<<"{\"span\":"<<g.h<<",\"N\":"<<N<<",\"bridge_counts\":[";
 for(int n=0;n<=N;++n){if(n)out<<",";out<<"\""<<total[n]<<"\"";}out<<"]}\n";
}
int main(int argc,char**argv) {
 try {
  if(argc!=6)throw std::runtime_error("usage: tm span width-or-N M exact|coeff output.json");
  int h=std::stoi(argv[1]),w=std::stoi(argv[2]);U m=std::stoull(argv[3]);
  Graph g(h);std::cerr<<"graph h="<<h<<" nodes="<<g.nodes.size()<<"\n";
  if(std::string(argv[4])=="exact")exact_value(g,w,m,argv[5]);
  else if(std::string(argv[4])=="coeff")coefficients(g,w,argv[5]);
  else throw std::runtime_error("bad mode");
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}
}

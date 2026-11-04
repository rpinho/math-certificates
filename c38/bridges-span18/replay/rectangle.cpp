#include "transfer.hpp"
#include <unordered_map>
#include <chrono>
struct Pair{U lo=0,hi=0;};
struct Hash{size_t operator()(K k)const{k^=k>>30;k*=0xbf58476d1ce4e5b9ULL;k^=k>>27;k*=0x94d049bb133111ebULL;return k^(k>>31);}};
using Map=std::unordered_map<K,Pair,Hash>;
static int W,C;static uint64_t M=51081913;
Map advance(const Map&cur,int row,bool final,Pair&sum){
 Map next;next.reserve(cur.size()+cur.size()/2);int slots=W+2;
 K bits=(K(1)<<(2*slots))-1;K rightmask=(K(1)<<(2*(row+1)))-1;
 for(auto &it:cur){Moves moves=vertex(it.first,slots,row,!final,row<W,final,1);
  for(unsigned i=0;i<moves.n;i++){
   auto m=moves.a[i];if(m.done){need(final&&m.k==0,"rectangle completion");sum.lo=plus(sum.lo,it.second.lo);sum.hi=plus(sum.hi,it.second.hi);continue;}
   K key=m.key;
   if(!final){
    unsigned occupied=__builtin_popcountll((key|(key>>1))&0x5555555555555555ULL&rightmask);
    if(occupied>unsigned(C))continue;
    if(row==W&&(occupied<3||occupied%2==0))continue;
   }
   if(row==W){need(((key>>(2*(W+1)))&3)==0,"rectangle top");key=(key&~bits)|((key<<2)&bits);}
   auto &v=next[key];v.lo=plus(v.lo,weight(it.second.lo,m.k,M,false));v.hi=plus(v.hi,weight(it.second.hi,m.k,M,true));
  }
 }
 return next;
}
int main(int argc,char**argv){try{
 need(argc==5,"usage rectangle frame_range span_min span_max crossing_cap");W=atoi(argv[1]);int mn=atoi(argv[2]),mx=atoi(argv[3]);C=atoi(argv[4]);need(W>=0&&W<=23&&mn>=1&&mx>=mn&&C>=3,"rectangle parameters");
 auto start=std::chrono::steady_clock::now();Map cur;U z=U(M)<<69;
 for(int y=0;y<=W;y++)cur[(K(1)<<(2*(W+2)))|(K(3)<<(2*(y+1)))]={z,z};Pair total;
 for(int h=1;h<=mx;h++){
  if(h>=mn){Map ending=cur;Pair one;for(int r=0;r<=W;r++)ending=advance(ending,r,true,one);need(ending.empty(),"unfinished final graph");total.lo=plus(total.lo,one.lo);total.hi=plus(total.hi,one.hi);std::cerr<<"terminal frame "<<W<<" span "<<h<<" lo "<<dec(one.lo)<<" hi "<<dec(one.hi)<<std::endl;}
  if(h==mx)break;
  Pair unused;for(int r=0;r<=W;r++){cur=advance(cur,r,false,unused);if(r==W/2)std::cerr<<"middle frame "<<W<<" span "<<h<<" states "<<cur.size()<<std::endl;}
  need(unused.lo==0&&unused.hi==0,"interior completion");std::cerr<<"prefix frame "<<W<<" span "<<h<<" states "<<cur.size()<<std::endl;
 }
 double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"{\"frame_range\":"<<W<<",\"span_min\":"<<mn<<",\"span_max\":"<<mx<<",\"crossing_cap\":"<<C<<",\"M\":"<<M<<",\"scale\":96,\"num_lo\":\""<<dec(total.lo)<<"\",\"num_hi\":\""<<dec(total.hi)<<"\",\"seconds\":"<<elapsed<<"}"<<std::endl;
}catch(std::exception&e){std::cerr<<"REJECT "<<e.what()<<std::endl;return 1;}}

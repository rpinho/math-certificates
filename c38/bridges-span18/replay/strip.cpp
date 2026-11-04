#include "transfer.hpp"
#include <chrono>
#include <fstream>
#include <numeric>
#include <omp.h>
// Collision-resolving table compares entire keys; indices follow discovery order.
struct Index{
 std::vector<K> table;std::vector<uint32_t> value;size_t used=0;
 static uint64_t hash(K a){a^=a>>30;a*=0xbf58476d1ce4e5b9ULL;a^=a>>27;a*=0x94d049bb133111ebULL;return a^(a>>31);}
 void grow(){size_t sz=table.empty()?16:table.size()*2;std::vector<K> old;std::vector<uint32_t> ov;old.swap(table);ov.swap(value);table.assign(sz,~K(0));value.resize(sz);for(size_t i=0;i<old.size();i++)if(old[i]!=~K(0)){size_t j=hash(old[i])&(sz-1);while(table[j]!=~K(0))j=(j+1)&(sz-1);table[j]=old[i];value[j]=ov[i];}}
 uint32_t get(K k,bool& fresh){if(table.empty()||(used+1)*10>table.size()*7)grow();size_t j=hash(k)&(table.size()-1);while(table[j]!=~K(0)&&table[j]!=k)j=(j+1)&(table.size()-1);fresh=table[j]==~K(0);if(fresh){need(used<(1u<<30),"index capacity");table[j]=k;value[j]=used++;}return value[j];}
 void release(){std::vector<K>().swap(table);std::vector<uint32_t>().swap(value);}
};
struct Edge{uint32_t d[3]={};uint8_t n=0,done=0;};
struct Stage{Index idx;std::vector<K> keys;std::vector<Edge> edges;std::vector<uint32_t> offsets,ins;uint32_t empty=0;};
int main(int argc,char**argv){try{
 need(argc>=5,"usage: strip span width tail_bits points(1|2) [threads]");int h=atoi(argv[1]),w=atoi(argv[2]),F=atoi(argv[3]),points=atoi(argv[4]);int threads=argc>5?atoi(argv[5]):1;omp_set_num_threads(threads);need(h>=1&&h<=18&&w>=1,"parameters");
 auto start=std::chrono::steady_clock::now();std::vector<Stage> st(h+1);bool fresh;st[0].idx.get(0,fresh);st[0].keys.push_back(0);
 for(int turn=0;;turn++){
  uint64_t added=0;
  for(int r=0;r<=h;r++){
   Stage &s=st[r],&d=st[(r+1)%(h+1)];size_t end=s.keys.size();
   if(s.edges.size()==end)continue;
   s.edges.reserve(end);
   if(d.idx.table.empty())for(size_t j=0;j<d.keys.size();j++){uint32_t got=d.idx.get(d.keys[j],fresh);need(fresh&&got==j,"index rebuild");}
   for(size_t i=s.edges.size();i<end;i++){
    Moves moves=strip_moves(s.keys[i],h,r);Edge e;
    for(unsigned t=0;t<moves.n;t++){
     Move m=moves.a[t];if(m.done){need(m.k==0,"weighted completion");e.done++;continue;}
     uint32_t j=d.idx.get(m.key,fresh);if(fresh){d.keys.push_back(m.key);added++;}
     need(e.n<3,"edge capacity");e.d[e.n++]=j|(uint32_t(m.k)<<30);
     need(s.keys[i]==0||m.key!=0,"nonempty to empty");
    }
    s.edges.push_back(e);
   }
   d.idx.release();d.idx.used=0;d.keys.shrink_to_fit();
  }
  uint64_t total=0;for(auto&s:st)total+=s.keys.size();std::cerr<<"closure "<<h<<" turn "<<turn<<" states "<<total<<" new "<<added<<std::endl;
  if(!added)break;need(turn<100,"closure convergence");
 }
 uint64_t total=0,edges=0,maxsize=0;
 for(auto&s:st){total+=s.keys.size();maxsize=std::max<uint64_t>(maxsize,s.keys.size());for(auto e:s.edges)edges+=e.n; auto pos=std::find(s.keys.begin(),s.keys.end(),K(0));need(pos!=s.keys.end(),"missing empty");s.empty=pos-s.keys.begin();s.idx.release();std::vector<K>().swap(s.keys);}
 // Destination-owned forward reductions; each edge retains its own rounding.
 for(int r=0;r<=h;r++){
  auto&s=st[r];auto&d=st[(r+1)%(h+1)];s.offsets.assign(d.edges.size()+1,0);
  for(auto e:s.edges)for(unsigned k=0;k<e.n;k++)s.offsets[(e.d[k]&0x3fffffff)+1]++;
  for(size_t i=1;i<s.offsets.size();i++)s.offsets[i]+=s.offsets[i-1];s.ins.resize(s.offsets.back());auto cur=s.offsets;
  for(size_t i=0;i<s.edges.size();i++)for(unsigned k=0;k<s.edges[i].n;k++){uint32_t v=s.edges[i].d[k];s.ins[cur[v&0x3fffffff]++]=uint32_t(i)|(v&0xc0000000);}
 }
 std::cerr<<"GRAPH READY span "<<h<<" states "<<total<<" edges "<<edges<<std::endl;
 for(int point=0;point<points;point++){
  uint64_t M=51081913+314*point;std::vector<std::vector<uint64_t>> pot;
  int cycles=0;
  if(F){
   pot.resize(h+1);for(int r=0;r<=h;r++)pot[r].assign(st[r].edges.size(),0);
   for(;;){uint64_t changed=0;
    for(int r=h;r>=0;r--){auto&s=st[r];auto&cur=pot[r];auto&next=pot[(r+1)%(h+1)];uint64_t local=0;
     #pragma omp parallel for reduction(+:local) schedule(static)
     for(size_t i=0;i<s.edges.size();i++){
      if(i==s.empty)continue;const Edge&e=s.edges[i];U rhs=U(e.done)<<(F+54);
      for(unsigned j=0;j<e.n;j++){uint32_t v=e.d[j];unsigned k=v>>30;uint64_t q=k==0?(1ULL<<54):k==1?(M<<27):M*M;rhs+=U(q)*next[v&0x3fffffff];}
      uint64_t val=(rhs+((U(1)<<54)-1))>>54;need(val<(1ULL<<60),"potential capacity");need(val>=cur[i],"potential monotonicity");local+=val!=cur[i];cur[i]=val;
     } changed+=local;
    }
    cycles++;if(cycles%50==0)std::cerr<<"potential span "<<h<<" M "<<M<<" cycle "<<cycles<<" changed "<<changed<<std::endl;
    if(!changed)break;need(cycles<20000,"potential did not stabilize");
   }
  }
  std::vector<U> lo(maxsize),hi(maxsize),nl(maxsize),nh(maxsize);lo[st[0].empty]=hi[st[0].empty]=U(1)<<96;U blo=0,bhi=0;
  for(int col=0;col<w;col++){
   for(int r=0;r<=h;r++){
    auto&s=st[r];auto&d=st[(r+1)%(h+1)];U cl=0,ch=0;
    // OpenMP reduction on uint128 uses exact integer addition. Capacity bounded below.
    #pragma omp parallel for reduction(+:cl,ch) schedule(static)
    for(size_t i=0;i<s.edges.size();i++)if(s.edges[i].done){need(s.edges[i].done==1&&hi[i]<(U(1)<<98),"completion capacity");cl+=lo[i];ch+=hi[i];}
    blo=plus(blo,cl);bhi=plus(bhi,ch);
    #pragma omp parallel for schedule(static)
    for(size_t j=0;j<d.edges.size();j++){
     U l=0,u=0;for(uint32_t t=s.offsets[j];t<s.offsets[j+1];t++){uint32_t v=s.ins[t];l=plus(l,weight(lo[v&0x3fffffff],v>>30,M,false));u=plus(u,weight(hi[v&0x3fffffff],v>>30,M,true));}nl[j]=l;nh[j]=u;
    }
    lo.swap(nl);hi.swap(nh);
   }
   if(col==0)lo[st[0].empty]=hi[st[0].empty]=0;
   if((col+1)%10==0||col+1==w)std::cerr<<"forward span "<<h<<" M "<<M<<" column "<<col+1<<" lo "<<dec(blo)<<" hi "<<dec(bhi)<<std::endl;
  }
  U tail=0;if(F)for(size_t i=0;i<st[0].edges.size();i++){
   // Exact 192-bit product reduced using quotient and remainder; hi<2^107, potential<2^60.
   U a=hi[i],mask=(U(1)<<F)-1,q=pot[0][i];need((a>>F)==0||q<=~U(0)/(a>>F),"tail overflow");U t=plus((a>>F)*q,((a&mask)*q+mask)>>F);tail=plus(tail,t);
  }
  double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout<<"{\"span\":"<<h<<",\"width\":"<<w<<",\"M\":"<<M<<",\"scale\":96,\"tail_bits\":"<<F<<",\"states\":"<<total<<",\"edges\":"<<edges<<",\"cycles\":"<<cycles<<",\"num_lo\":\""<<dec(blo)<<"\",\"num_hi\":\""<<dec(bhi)<<"\",\"num_tail\":\""<<dec(tail)<<"\",\"seconds\":"<<elapsed<<"}"<<std::endl;
 }
}catch(std::exception&e){std::cerr<<"REJECT "<<e.what()<<std::endl;return 1;}}

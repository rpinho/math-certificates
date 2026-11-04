// Shares only the referee's own graph, not any producer implementation.
// Fixed 160-bit denominator makes an additional span-13 audit affordable.
#define main unused_exact_main
#include "independent_tm.cpp"
#undef main
using Fixed=boost::multiprecision::uint256_t;
Fixed mul(Fixed x,uint64_t m,int k,bool ceiling) {
 if(x>=(Fixed(1)<<192))throw std::runtime_error("input capacity");
 if(!k)return x;
 int s=27*k;uint64_t q=k==1?m:m*m;Fixed p=x*q;
 return (p>>s)+Fixed(ceiling && ((p&((Fixed(1)<<s)-1))!=0));
}
void plus(Fixed&x,Fixed y){if(x>~Fixed(0)-y)throw std::runtime_error("overflow");x+=y;}
int main(int argc,char**argv){try{
 if(argc!=5)throw std::runtime_error("usage: interval h width M output");
 int h=std::stoi(argv[1]),w=std::stoi(argv[2]);uint64_t m=std::stoull(argv[3]);
 Graph g(h);std::cerr<<"graph nodes="<<g.nodes.size()<<"\n";
 std::vector<std::array<Fixed,2>>a(g.nodes.size()),b(g.nodes.size());
 a[0][0]=a[0][1]=Fixed(1)<<160;Fixed sum[2]={0,0};
 for(int col=0;col<w;++col){
  for(int row=0;row<=h;++row){
   for(int id:g.stages[(row+1)%(h+1)])b[id]={0,0};
   for(int id:g.stages[row])for(int p=0;p<2;++p)if(a[id][p]!=0){
    for(int j=0;j<g.nodes[id].finish;++j)plus(sum[p],a[id][p]);
    for(auto e:g.nodes[id].out)plus(b[e.to][p],mul(a[id][p],m,e.power,p));
   }
   a.swap(b);
  }
  if(!col)a[0]={0,0};
  if(col%25==0)std::cerr<<"column="<<col+1<<"\n";
 }
 const unsigned f=32;std::vector<uint64_t>potential(g.nodes.size());
 const uint64_t q=1ULL<<54,wt[3]={q,m<<27,m*m};
 int cycles=0;bool changed=true;
 while(changed){changed=false;if(++cycles>10000)throw std::runtime_error("potential timeout");
  for(int row=h;row>=0;--row)for(int id:g.stages[row])if(g.nodes[id].key){
   unsigned __int128 rhs=(unsigned __int128)(g.nodes[id].finish)<<(f+54);
   for(auto e:g.nodes[id].out)rhs+=(unsigned __int128)(wt[e.power])*potential[e.to];
   auto u=(rhs+q-1)>>54;if(u>=((unsigned __int128)1<<60))throw std::runtime_error("potential capacity");
   if(u<potential[id])throw std::runtime_error("potential decreased");
   if(u!=potential[id]){changed=true;potential[id]=uint64_t(u);}
  }
 }
 for(size_t id=0;id<g.nodes.size();++id)if(g.nodes[id].key){
  unsigned __int128 rhs=(unsigned __int128)(g.nodes[id].finish)<<(f+54);
  for(auto e:g.nodes[id].out)rhs+=(unsigned __int128)(wt[e.power])*potential[e.to];
  if(((unsigned __int128)potential[id]<<54)<rhs)throw std::runtime_error("invalid upper potential");
 }
 Fixed tail=0;
 for(int id:g.stages[0]){
  if(a[id][1]>=(Fixed(1)<<192))throw std::runtime_error("tail capacity");
  Fixed product=a[id][1]*potential[id];plus(tail,(product+((Fixed(1)<<f)-1))>>f);
 }
 std::ofstream out(argv[4]);out<<"{\"span\":"<<h<<",\"width\":"<<w<<",\"M\":"<<m<<",\"scale\":160,\"nodes\":"<<g.nodes.size()
 <<",\"potential_cycles\":"<<cycles<<",\"num_lo\":\""<<sum[0]<<"\",\"num_hi\":\""<<sum[1]<<"\",\"num_tail\":\""<<tail<<"\"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}

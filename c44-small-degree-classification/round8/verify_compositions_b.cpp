// Independent B: bit Mobius interpolation, direct Fourier conversion,
// then exhaustive mixed-radix allocations (no recursive search).
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
int main(int argc,char**argv){
 assert(argc==2);std::ifstream in(argv[1]);assert(in.good());
 std::string s;int lines=0;std::array<int,7> best{};std::array<uint64_t,7> totals{};
 while(std::getline(in,s)){
  if(!s.empty()&&s.back()=='\r')s.pop_back();if(s.empty())continue;
  assert(s.size()==1024);lines++;std::array<int,1024> bit{},fourier{};
  for(int x=0;x<1024;x++)bit[x]=((s[x]-'0')^__builtin_parity((unsigned)x))?-1:1;
  // Integer coefficients in 0/1 input variables.
  for(int j=0;j<10;j++)for(int x=0;x<1024;x++)if(x>>j&1)bit[x]-=bit[x^(1<<j)];
  for(int x=0;x<1024;x++)if(bit[x]){
   int deg=__builtin_popcount((unsigned)x);assert(deg<=3);
   for(int sub=x;;sub=(sub-1)&x){
    fourier[sub]+=bit[x]*(8>>deg)*(__builtin_parity((unsigned)sub)?-1:1);
    if(!sub)break;
   }
  }
  int used=0,degree=0;std::vector<int>masks,vars;std::array<int,10>local{};
  for(int m=1;m<1024;m++)if(fourier[m]){
   masks.push_back(m);used|=m;int r=__builtin_popcount((unsigned)m);degree=std::max(degree,r);
   for(int j=0;j<10;j++)if(m>>j&1)local[j]=std::max(local[j],r);
  }
  for(int j=0;j<10;j++)if(used>>j&1)vars.push_back(j);
  for(int d=2;d<=6;d++){
   if(degree>d)continue;std::array<int,10>w{};for(int j:vars)w[j]=1;
   bool done=false;uint64_t accepted=0;int optimum=-1;
   while(!done){
    bool valid=true;
    for(int m:masks){int sum=0;for(int j:vars)if(m>>j&1)sum+=w[j];if(sum>d){valid=false;break;}}
    if(valid){int value=0;for(int j:vars)value+=3*(1<<(w[j]-1))-2;optimum=std::max(optimum,value);accepted++;}
    int pos=0;
    for(;pos<(int)vars.size();pos++){
     int j=vars[pos];if(++w[j]<=d-local[j]+1)break;w[j]=1;
    }
    if(pos==(int)vars.size())done=true;
   }
   totals[d]+=accepted;best[d]=std::max(best[d],optimum);
  }
 }
 assert(lines==761);
 std::cout<<"{\"status\":\"PASS\",\"classes\":761,\"method\":\"bit interpolation and complete mixed-radix enumeration\",\"degrees\":[";
 const uint64_t expected[7]={0,0,8,796,8080,49761,221198};
 for(int d=2;d<=6;d++){
  assert(best[d]==3*(1<<(d-1))-2&&totals[d]==expected[d]);if(d>2)std::cout<<',';
  std::cout<<"{\"degree\":"<<d<<",\"maximum\":"<<best[d]<<",\"allocations\":"<<totals[d]<<'}';
 }
 std::cout<<"]}\n";
}

// Exploratory exact lower-side search over the complete cubic catalogue.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <string>
#include <vector>
struct Row {int line;std::vector<int> masks;std::vector<int> vars;};
int main(int argc,char**argv){
 assert(argc==3);std::ifstream in(argv[1]);assert(in.good());
 std::vector<Row> rows;std::string s;int line=0;
 while(std::getline(in,s)){
  if(!s.empty()&&s.back()=='\r')s.pop_back();if(s.empty())continue;
  ++line;assert(s.size()==1024);std::array<int,1024>a{};
  for(int x=0;x<1024;x++)a[x]=((s[x]-'0')^__builtin_parity((unsigned)x))?-1:1;
  for(int w=1;w<1024;w*=2)for(int b=0;b<1024;b+=2*w)for(int j=0;j<w;j++){
   int u=a[b+j],v=a[b+j+w];a[b+j]=u+v;a[b+j+w]=u-v;}
  Row r;r.line=line;int used=0;
  for(int m=1;m<1024;m++)if(a[m]){assert(__builtin_popcount((unsigned)m)<=3);r.masks.push_back(m);used|=m;}
  for(int j=0;j<10;j++)if(used>>j&1)r.vars.push_back(j);
  rows.push_back(r);
 }
 assert(line==761);std::ofstream out(argv[2]);assert(out.good());
 std::array<int,7>L{0,1,4,10,22,46,94};
 out<<"{\"status\":\"EXPLORATORY\",\"model\":\"disjoint cubic-catalogue compositions\",\"degrees\":[";
 for(int d=2;d<=6;d++){
  if(d>2)out<<',';int global=0;uint64_t count=0;
  out<<"{\"degree\":"<<d<<",\"rows\":[";
  for(int ri=0;ri<(int)rows.size();ri++){
   const auto&r=rows[ri];std::array<int,10>w{},local{};std::vector<int> loads(r.masks.size());
   int start=0;for(int m:r.masks){int z=__builtin_popcount((unsigned)m);start=std::max(start,z);for(int j:r.vars)if(m>>j&1)local[j]=std::max(local[j],z);}
   int best=-1;uint64_t feasible=0;std::array<int,10>witness{};
   if(start<=d){
    for(size_t t=0;t<loads.size();t++)loads[t]=__builtin_popcount((unsigned)r.masks[t]);
    for(int j:r.vars)w[j]=1;
    std::function<void(int,int)> dfs=[&](int at,int val){
     if(at==(int)r.vars.size()){feasible++;if(val>best){best=val;witness=w;}return;}
     int j=r.vars[at];
     for(int v=1;v<=d-local[j]+1;v++){
      bool ok=true;
      for(size_t t=0;t<loads.size();t++)if(r.masks[t]>>j&1)if(loads[t]+v-1>d){ok=false;break;}
      if(!ok)continue;w[j]=v;
      for(size_t t=0;t<loads.size();t++)if(r.masks[t]>>j&1)loads[t]+=v-1;
      dfs(at+1,val+L[v]);
      for(size_t t=0;t<loads.size();t++)if(r.masks[t]>>j&1)loads[t]-=v-1;
     }
    };dfs(0,0);
   }
   count+=feasible;global=std::max(global,best);
   if(ri)out<<',';out<<"{\"line\":"<<r.line<<",\"max\":"<<best<<",\"feasible\":"<<feasible<<",\"weights\":[";
   for(int j=0;j<10;j++){if(j)out<<',';out<<witness[j];}out<<"]}";
  }
  out<<"],\"maximum\":"<<global<<",\"feasible\":"<<count<<"}";
  std::cout<<"degree "<<d<<" maximum "<<global<<" feasible "<<count<<std::endl;
 }
 out<<"]}\n";
}

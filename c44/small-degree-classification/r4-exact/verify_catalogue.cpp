// Independent direct character-sum checker. No Walsh transform or search imports.
// Completeness is the explicitly named published classification premise.
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>
int main(int argc,char**argv){
  assert(argc==2); std::ifstream in(argv[1]); assert(in.good());
  constexpr int N=1024; constexpr int64_t Z=int64_t(N)*N;
  std::string line; int count=0,tight=0;std::map<int,int> hist;
  std::vector<int> eq;
  while(std::getline(in,line)){
    if(!line.empty()&&line.back()=='\r')line.pop_back();
    if(line.empty())continue;
    ++count;assert(line.size()==N);
    std::array<int,N> val{},coef{};std::array<int,10> local{};
    for(int x=0;x<N;++x){assert(line[x]=='0'||line[x]=='1');
      val[x]=((line[x]-'0')^__builtin_parity(unsigned(x)))?-1:1;}
    int64_t energy=0,third=0;
    for(int s=0;s<N;++s){
      int c=0;for(int x=0;x<N;++x)c+=(__builtin_parity(unsigned(s&x))?-val[x]:val[x]);
      coef[s]=c;if(!c)continue;
      int d=__builtin_popcount(unsigned(s));assert(d<=3);assert(c%256==0);
      energy+=int64_t(c)*c;if(d==3)third+=int64_t(c)*c;
      for(int j=0;j<10;++j)if(s&(1<<j))local[j]=std::max(local[j],d);
    }
    assert(energy==Z);
    int ds=0,relevant=0;for(int d:local)if(d){ds+=1<<(3-d);++relevant;}
    // Independent relevance check directly from the truth table.
    for(int j=0;j<10;++j){bool differs=false;
      for(int x=0;x<N;++x)if(val[x]!=val[x^(1<<j)]){differs=true;break;}
      assert(differs==(local[j]!=0));}
    ++hist[relevant];assert(int64_t(ds-8)*Z<=2*third);
    if(int64_t(ds-8)*Z==2*third){
      ++tight;eq.push_back(count);
      if(third==0){assert(ds==8&&relevant==4);for(int d:local)assert(d==0||d==2);}
      else if(2*third==Z){assert(ds==9&&relevant==9);for(int d:local)assert(d==0||d==3);}
      else {assert(third==Z&&ds==10&&relevant==10);for(int d:local)assert(d==3);}
    }
  }
  assert(count==761&&tight==3);assert((eq==std::vector<int>{700,716,757}));
  assert(hist[10]==1&&hist[9]==6);
  std::cout<<"{\"status\":\"PASS\",\"classes\":"<<count
    <<",\"equality_lines\":[700,716,757],\"method\":\"direct integer character sums\",\"R_histogram\":{";
  bool first=true;for(auto [r,n]:hist){if(!first)std::cout<<',';first=false;std::cout<<'"'<<r<<"\":"<<n;}
  std::cout<<"}}\n";
}

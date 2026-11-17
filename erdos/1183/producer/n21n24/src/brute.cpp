// Enumerate ALL closed families by NextClosure on the 2^n cube elements.
#include <cstdint>
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
uint64_t closure(uint64_t seed){
 vector<int> a;for(uint64_t b=seed;b;b&=b-1)a.push_back(__builtin_ctzll(b));
 for(size_t i=0;i<a.size();++i)for(size_t j=0;j<=i;++j){
  for(int x:{a[i]&a[j],a[i]|a[j]})if(!(seed>>x&1)){seed|=1ULL<<x;a.push_back(x);}
 }
 return seed;
}
int main(){
 for(int n=0;n<=6;++n){int U=1<<n;uint64_t F=0,count=0;vector<int> best(1<<(n+1));
  for(;;){
   if(F){++count;int mask=0;for(uint64_t b=F;b;b&=b-1)mask|=1<<__builtin_popcount(__builtin_ctzll(b));best[mask]=max(best[mask],__builtin_popcountll(F));}
   bool next=false;
   for(int i=U-1;i>=0;--i)if(!(F>>i&1)){
    uint64_t low=i?((1ULL<<i)-1):0;uint64_t G=closure((F&low)|(1ULL<<i));
    if((G&low)==(F&low)){F=G;next=true;break;}
   }
   if(!next)break;
  }
  for(int i=0;i<=n;++i)for(int R=0;R<(1<<(n+1));++R)if(R>>i&1)best[R]=max(best[R],best[R^(1<<i)]);
  cout<<"{\"n\":"<<n<<",\"count\":"<<count<<",\"maxima\":[";for(int R=0;R<(int)best.size();++R){if(R)cout<<",";cout<<best[R];}cout<<"]}\n"<<flush;
 }
}

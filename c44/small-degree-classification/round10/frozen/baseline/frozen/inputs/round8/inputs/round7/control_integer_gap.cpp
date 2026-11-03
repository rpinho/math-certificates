// Exhaustive finite corroboration of the new integer-valued norm gap.
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
int main(){
 uint64_t total=0,checks=0;
 for(int n=1;n<=3;n++){
  int N=1<<n;uint64_t count=1;for(int i=0;i<N;i++)count*=5;
  vector<int> v(N,-2),b;
  for(uint64_t code=0;code<count;code++){
   b=v;
   for(int bit=1;bit<N;bit*=2)for(int s=0;s<N;s++)if(s&bit)b[s]-=b[s^bit];
   int deg=0,sq=0;for(int s=0;s<N;s++){if(b[s])deg=max(deg,__builtin_popcount((unsigned)s));sq+=v[s]*v[s];}
   if(sq){int D=1<<deg;assert(int64_t(sq)*D>=N);assert(int64_t(sq)*D==N || int64_t(sq)*D*2>=3*N);checks++;}
   total++;
   for(int x=0;x<N;x++){if(v[x]<2){v[x]++;break;}v[x]=-2;}
  }
 }
 cout<<"{\"status\":\"PASS\",\"integer_tables\":"<<total<<",\"nonzero_checks\":"<<checks<<",\"values\":\"-2,-1,0,1,2\",\"max_inputs\":3}"<<endl;
}

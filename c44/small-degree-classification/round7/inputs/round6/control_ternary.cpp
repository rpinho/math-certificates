// Independent finite corroboration of the new universal lemma.
// Enumerates ternary tables, uses a real Mobius transform for degree,
// and edge differences for energy and relevant-coordinate count.
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main(){
 cout<<"{\"status\":\"PASS\",\"tables\":[";
 for(int n=1;n<=4;n++){
  int N=1<<n;uint32_t count=1;for(int i=0;i<N;i++)count*=3;
  vector<int> v(N,-1),a(N);a[0]=-1;
  vector<int> nonzero(n+1);nonzero[0]=1;
  vector<vector<pair<int,int>>> update(N);
  for(int x=0;x<N;x++)for(int s=0;s<N;s++)if((s&x)==x)
    update[x].push_back({s,__builtin_popcount(unsigned(s^x))%2?-1:1});
  vector<uint64_t> by_degree(n+1);uint64_t strict=0,equalities=0;
  for(uint32_t t=0;t<count;t++){
   int k=n;while(k>0&&!nonzero[k])k--;
   int w=0;for(int z:v)w+=(z!=0);
   if(w){
    by_degree[k]++;
    int h=0,edge_energy=0;
    for(int j=0;j<n;j++){
     int diffs=0;
     for(int x=0;x<N;x++)if(!(x>>j&1)){
       int dif=v[x]-v[x|(1<<j)];diffs+=dif*dif;
     }
     if(diffs){
       h++;
       // E (Delta_j A)^2 = diffs/(2N).
       // Nonzero degree <=k-1 forces >=2^(-(k+1)).
       assert(k>0 && int64_t(diffs)*(1<<(k+1))>=2*N);
     }
     edge_energy+=diffs;
    }
    assert(edge_energy<=2*k*w); // sum derivative energies <= k E A^2.
    assert(int64_t(h)*N<=int64_t(k)*w*(1<<(k+1)));
    if(int64_t(h)*N==int64_t(k)*w*(1<<(k+1)))equalities++;else strict++;
   }
   if(t+1==count)break;
   for(int x=0;x<N;x++){
    int old=v[x],z=old==1?-1:old+1;v[x]=z;
    for(auto [s,sign]:update[x]){
     int level=__builtin_popcount(unsigned(s));
     if(a[s])nonzero[level]--;
     a[s]+=(z-old)*sign;
     if(a[s])nonzero[level]++;
    }
    if(old!=1)break;
   }
  }
  if(n>1)cout<<",";
  cout<<"{\"n\":"<<n<<",\"all_tables\":"<<count<<",\"nonzero_by_degree\":[";
  for(int i=0;i<=n;i++){if(i)cout<<",";cout<<by_degree[i];}
  cout<<"],\"equalities\":"<<equalities<<",\"strict\":"<<strict<<"}"<<flush;
 }
 // Independent exact counterexample to a universal 2-to-2.125 RM gap:
 // complement of five pairwise products on 10 bits, algebraic order 2.
 int weight=0;
 for(int x=0;x<(1<<10);x++){
   int v=1;for(int j=0;j<5;j++)v^=((x>>(2*j))&1)&((x>>(2*j+1))&1);
   weight+=v;
 }
 assert(weight==528 && 528*16==33*256 && 528*8<17*256);
 int lifted=0;for(int x=0;x<(1<<12);x++){
  int v=1;for(int j=0;j<5;j++)v^=((x>>(2*j))&1)&((x>>(2*j+1))&1);
  lifted+=v*((x>>10)&1)*((x>>11)&1);
 }
 assert(lifted==528);
 cout<<"],\"kta_table_counterexample\":{\"n\":10,\"order\":2,\"weight\":"<<weight
     <<",\"minimum_weight\":256,\"normalized_weight\":\"33/16\",\"lifted_n\":12,\"lifted_order\":4,\"lifted_weight\":"<<lifted<<"}}\n";
}

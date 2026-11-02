// Exhaustive exact corroboration. It does not replace published universal theorems.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <unordered_map>
#include <vector>
using namespace std;
int main(){
  array<unordered_map<uint32_t,int>,5> templates;
  ifstream in("structure_templates.txt");assert(in.good());
  unsigned code;int n,k;
  while(in>>n>>code>>k)templates[n][code]=k;
  cout<<"{\"status\":\"PASS\",\"ternary\":[";
  for(n=1;n<=4;n++){
    int N=1<<n,top=0;
    uint32_t total=1;for(int j=0;j<N;j++)total*=3;
    vector<int> binary_degree(1<<N);
    for(int mask=0;mask<(1<<N);mask++){
      vector<int>a(N);for(int j=0;j<N;j++)a[j]=(mask>>j)&1;
      for(int b=1;b<N;b*=2)for(int j=0;j<N;j++)if(j&b)a[j]^=a[j^b];
      int deg=0;for(int j=0;j<N;j++)if(a[j])deg=max(deg,__builtin_popcount((unsigned)j));
      binary_degree[mask]=deg;
    }
    vector<int>vals(N,-1),coeff(N);coeff[0]=-1;
    vector<int>nz(n+1);nz[0]=1;
    vector<vector<pair<int,int>>> update(N);
    for(int j=0;j<N;j++)for(int s=0;s<N;s++)if((s&j)==j)
      update[j].push_back({s,(__builtin_popcount((unsigned)(s^j))%2)?-1:1});
    int weight=N;uint32_t support=(1u<<N)-1;
    uint64_t nonzero=0,minimum=0,strict=0,classification=0;
    vector<int> smallest(5,1000);
    for(uint32_t table=0;table<total;table++){
      if(weight){
        int deg=n;while(deg>0&&nz[deg]==0)deg--;
        assert(binary_degree[support]<=deg);
        int lower=1<<(n-deg);assert(weight>=lower);
        if(weight==lower){
          minimum++;
          auto it=templates[n].find(table);assert(it!=templates[n].end()&&it->second==deg);
          classification++;
        }else{
          assert(2*weight>=3*lower);strict++;
          smallest[deg]=min(smallest[deg],weight);
        }
        nonzero++;
      }
      if(table+1==total)break;
      for(int j=0;j<N;j++){
        int old=vals[j];int next=(old==1)?-1:old+1;vals[j]=next;
        if((old!=0)!=(next!=0)){support^=1u<<j;weight+=(next!=0)?1:-1;}
        for(auto [s,sign]:update[j]){
          int deg=__builtin_popcount((unsigned)s);
          if(coeff[s])nz[deg]--;
          coeff[s]+=(next-old)*sign;
          if(coeff[s])nz[deg]++;
        }
        if(old!=1)break;
      }
    }
    assert(minimum==templates[n].size());
    if(n>1)cout<<",";
    cout<<"{\"n\":"<<n<<",\"all_tables\":"<<total<<",\"nonzero\":"<<nonzero
        <<",\"minimum\":"<<minimum<<",\"classification_checks\":"<<classification
        <<",\"nonminimum\":"<<strict<<",\"smallest_nonminimum_weights\":[";
    for(int j=0;j<=n;j++){if(j)cout<<",";cout<<(smallest[j]==1000?-1:smallest[j]);}
    cout<<"]}"<<flush;
  }
  cout<<"],\"binary_codes\":[";
  bool comma=false;
  // Enumerate every RM(k,n) word for n<=5,k<=n-2; also all affine orders.
  for(n=2;n<=5;n++)for(k=1;k<=max(1,n-2);k++){
    int N=1<<n;vector<uint32_t>monomials;
    for(int mask=0;mask<N;mask++)if(__builtin_popcount((unsigned)mask)<=k){
      uint32_t truth=0;for(int x=0;x<N;x++)if((x&mask)==mask)truth|=1u<<x;
      monomials.push_back(truth);
    }
    assert(monomials.size()<32);
    uint32_t num=1u<<monomials.size(),word=0;
    int first=N+1,second=N+1;
    for(uint32_t j=1;j<num;j++){
      word^=monomials[__builtin_ctz(j)];
      int w=__builtin_popcount(word);assert(w>0);
      if(w<first){second=first;first=w;}else if(w>first&&w<second)second=w;
    }
    assert(first==1<<(n-k));assert(2*second>=3*first);
    if(k>=2)assert(second*2==3*first);
    if(comma)cout<<",";comma=true;
    cout<<"{\"n\":"<<n<<",\"k\":"<<k<<",\"words\":"<<num
        <<",\"minimum\":"<<first<<",\"second\":"<<second<<"}"<<flush;
  }
  cout<<"]}\n";
}

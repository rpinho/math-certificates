// Exact finite controls for the general deficit lemma. These do not
// establish the external minimum-support or lattice completeness premises.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
int pc(uint64_t x){return __builtin_popcountll(x);}
bool forbidden(int k,int norm,int h){
 long long m=1ll<<(k-1),gap=m/2,slack=1ll*k*norm-h*m;
 return k>=3&&slack<gap&&h%(2*k)!=0;
}
void test(const map<uint64_t,int>& p,int k,int denominator){
 int norm=0,h=0;uint64_t used=0;map<int,int> energies;
 for(auto [s,c]:p){assert(pc(s)<=k);norm+=c*c;used|=s;for(int j=0;j<63;++j)if(s>>j&1)energies[j]+=c*c;}
 h=pc(used);assert(!forbidden(k,norm,h));
 int minimum=1<<(k-1);for(auto [j,e]:energies)assert(e==minimum||2*e>=3*minimum);
 // Exact sparse convolution verifies these explicit constructions ternary:
 // P^3=P. Products can be checked without enumerating all 2^16 inputs.
 map<uint64_t,long long> square,cube;
 for(auto [s,c]:p)for(auto [t,d]:p)square[s^t]+=1ll*c*d;
 for(auto [s,c]:square)for(auto [t,d]:p)cube[s^t]+=c*d;
 for(auto [s,c]:cube)assert(c==1ll*denominator*denominator*(p.count(s)?p.at(s):0));
}
int main(){
 int products=0;
 for(int k=3;k<=8;++k){
  map<uint64_t,int> p{{0,1}};
  for(int j=0;j<k;++j){map<uint64_t,int> next;for(auto [s,c]:p){next[s|(1ull<<(2*j))]=c;next[s|(1ull<<(2*j+1))]=(j%2)?-c:c;}p=move(next);}
  test(p,k,1<<k);++products;
  map<uint64_t,int> point{{0,1}};
  for(int j=0;j<k;++j){map<uint64_t,int> next;for(auto [s,c]:point){next[s]=c;next[s|(1ull<<j)]=(j%2)?-c:c;}point=move(next);}
  test(point,k,1<<k);++products;
 }
 int checked=0;
 for(int table=0;table<6561;++table){
  int code=table;vector<int> v(8);for(int& x:v){x=code%3-1;code/=3;}
  for(int step=1;step<8;step*=2)for(int s=0;s<8;s+=step*2)for(int j=0;j<step;++j){int a=v[s+j],b=v[s+j+step];v[s+j]=a+b;v[s+j+step]=a-b;}
  map<uint64_t,int> p;int k=0;for(int s=0;s<8;++s)if(v[s]){p[s]=v[s];k=max(k,pc(s));}
  if(k!=3)continue;
  // For k=3 the Fourier denominator is exactly the one used in the lemma.
  int norm=0;uint64_t used=0;for(auto [s,c]:p){norm+=c*c;used|=s;}
  assert(!forbidden(3,norm,pc(used)));++checked;
 }
 assert(forbidden(6,124,23));
 assert(!forbidden(6,64,12)); // Divisibility exception is essential.
 assert(!forbidden(6,120,22)); // Strict threshold: slack=16 is allowed.
 cout<<"PASS "<<products<<" exact ternary constructions, "<<checked<<" complete degree-three ternary tables, strict and divisibility controls\n";
}

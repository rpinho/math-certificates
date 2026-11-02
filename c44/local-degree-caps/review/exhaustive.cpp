// Independent exact reviewer checks. Standard C++17, no target code.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
int pc(unsigned x){return __builtin_popcount(x);}
int rank2(vector<int> a){int r=0;for(int bit=0;bit<12;bit++){int j=r;while(j<(int)a.size()&&!(a[j]>>bit&1))j++;if(j==(int)a.size())continue;swap(a[r],a[j]);for(int q=0;q<(int)a.size();q++)if(q!=r&&(a[q]>>bit&1))a[q]^=a[r];r++;}return r;}
long long tested=0,minima=0,restrictions=0,duplicates=0;
void fwht(vector<int>&a){for(int h=1;h<(int)a.size();h*=2)for(int t=0;t<(int)a.size();t+=2*h)for(int j=0;j<h;j++){int x=a[t+j],y=a[t+j+h];a[t+j]=x+y;a[t+j+h]=x-y;}}
void check(uint64_t table,int n,bool deep){
 int N=1<<n;vector<int>a(N);for(int x=0;x<N;x++)a[x]=(table>>x&1)?1:-1;fwht(a);
 int d=0;for(int s=0;s<N;s++)if(a[s])d=max(d,pc(s));
 if(!d)return;tested++;
 vector<int> local(n),infc(n);int Du=0; // D measured in units of 2^-d.
 for(int i=0;i<n;i++){
  for(int s=0;s<N;s++)if(a[s]&&(s>>i&1))local[i]=max(local[i],pc(s));
  if(local[i])Du+=1<<(d-local[i]);
  for(int x=0;x<N;x++)if(!(x>>i&1)&&((table>>x&1)!=(table>>(x^(1<<i))&1)))infc[i]++;
 }
 assert(Du<=d*(1<<(d-1)));
 for(int s=0;s<N;s++)assert((a[s]*(1<<(d-1)))%N==0);
 if(d>=2)for(int i=0;i<n;i++)if(local[i]){
  int M=1<<(d-1);long long sum=0;int signed_sum=0;
  for(int s=0;s<N;s++)if(s>>i&1){int z=a[s]*M/N;sum+=z*z;signed_sum+=z;}
  assert(sum*(N/2)==1LL*M*M*infc[i]);assert(sum%2==0&&signed_sum%2==0);
  assert(sum>=M);assert(sum==M||sum>=M+2);
  if(sum==M){
   minima++;vector<int>T;int H=0;
   for(int s=0;s<N;s++)if((s>>i&1)&&a[s]){assert(abs(a[s]*M)==N);T.push_back(s^(1<<i));H|=s^(1<<i);}
   assert((int)T.size()==M);vector<int>dif;for(int s:T)dif.push_back(s^T[0]);
   assert(rank2(dif)==d-1);assert(pc(H)<=2*(d-1));assert(!(H>>i&1));
   for(int s=0;s<N;s++)if(a[s]&&pc(s)==d)assert(s&H);
   if(deep){
    int h=pc(H),active=0;vector<int>hv;for(int j=0;j<n;j++)if(H>>j&1)hv.push_back(j);
    for(int alpha=0;alpha<(1<<h);alpha++){
     int fixed=0;for(int j=0;j<h;j++)if(alpha>>j&1)fixed|=1<<hv[j];
     int x0=fixed,x1=fixed|(1<<i);int A=((table>>x0&1)?1:-1)-((table>>x1&1)?1:-1);
     if(A){active++;for(int x=0;x<N;x++)if((x&H)==fixed)assert(((table>>x&1)!=(table>>(x^(1<<i))&1))&&((table>>x&1)==(table>>(fixed|(x&(1<<i)))&1)));}
    }
    assert(active*M==(1<<h));
   }
  }
 }
 if(!deep)return;
 // Direct single-coordinate expected restricted-weight inequality.
 for(int j=0;j<n;j++)for(int i=0;i<n;i++)if(i!=j&&local[i]){
  int branch[2]={0,0};
  for(int s=0;s<N;s++)if(!(s>>j&1)&&(s>>i&1))for(int b=0;b<2;b++){
   if(a[s]+(b?-1:1)*a[s|(1<<j)])branch[b]=max(branch[b],pc(s));
  }
  int rhs=0;for(int b=0;b<2;b++)if(branch[b])rhs+=1<<(d-branch[b]);
  assert(2*(1<<(d-local[i]))<=rhs);restrictions++;
 }
}
int main(){
 for(int n=1;n<=4;n++)for(uint64_t t=0;t<(1ULL<<(1<<n));t++)check(t,n,true);
 cerr<<"all truth tables through n=4 passed: "<<tested<<"\n";
 // Exhaustive n=5 degree<=3: split on fifth bit. Both four-bit
 // restrictions have degree<=3, and their degree-3 spectra agree.
 map<array<int,4>,vector<unsigned>> groups;
 for(unsigned t=0;t<65536;t++){
  vector<int>a(16);for(int x=0;x<16;x++)a[x]=(t>>x&1)?1:-1;fwht(a);
  if(a[15])continue;
  groups[{a[7],a[11],a[13],a[14]}].push_back(t);
 }
 map<array<int,10>,vector<uint32_t>> groups6;
 long long n5=0;for(auto &kv:groups)for(unsigned a:kv.second)for(unsigned b:kv.second){
  uint32_t t=uint32_t(a)|(uint32_t(b)<<16);
  check(t,5,true);n5++;
  vector<int>spec(32);for(int x=0;x<32;x++)spec[x]=(t>>x&1)?1:-1;fwht(spec);
  array<int,10>key;int j=0;for(int s=0;s<32;s++)if(pc(s)==3)key[j++]=spec[s];
  groups6[key].push_back(t);
 }
 cerr<<"all n=5 degree<=3 passed: "<<n5<<"\n";
 long long n6=0;for(auto &kv:groups6)for(uint32_t a:kv.second)for(uint32_t b:kv.second){
  check(uint64_t(a)|(uint64_t(b)<<32),6,true);n6++;
 }
 assert(n5==807980&&n6==16750860); // independent published counts, KV2024 Remark1.
 cout<<"{\"status\":\"PASS\",\"boolean_nonconstant_checked\":"<<tested
     <<",\"n5_degree_le3_including_constants\":"<<n5<<",\"n6_degree_le3_including_constants\":"<<n6<<",\"minimum_derivatives_checked\":"<<minima
     <<",\"coordinate_restriction_checks\":"<<restrictions<<"}\n";
}

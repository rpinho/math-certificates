// All 3^16 ternary tables on four coordinates, exact Walsh arithmetic.
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
int pc(unsigned s){return __builtin_popcount(s);}
int rank2(vector<int>v){int r=0;for(int b=0;b<4;b++){int j=r;while(j<(int)v.size()&&!(v[j]>>b&1))j++;if(j==(int)v.size())continue;swap(v[j],v[r]);for(int q=0;q<(int)v.size();q++)if(q!=r&&(v[q]>>b&1))v[q]^=v[r];r++;}return r;}
int main(){
 array<int,16>val,walsh;val.fill(-1);walsh.fill(0);walsh[0]=-16;
 int character[16][16];for(int x=0;x<16;x++)for(int s=0;s<16;s++)character[x][s]=(pc(x&s)%2)?-1:1;
 long long count=0,hist[5]={0},mins[5]={0};int gap[5]={0,9999,9999,9999,9999};
 do {
  count++;int support=0,k=0;for(int x:val)support+=(x!=0);if(!support)goto advance;
  for(int s=0;s<16;s++)if(walsh[s])k=max(k,pc(s));hist[k]++;
  if(k){
   int M=1<<k,E=0,sum=0;vector<int>T;
   for(int s=0;s<16;s++){assert(walsh[s]*M%16==0);int z=walsh[s]*M/16;E+=z*z;sum+=z;if(z)T.push_back(s);}
   assert(E*16==M*M*support&&E%2==0&&sum%2==0);assert(E>=M);
   if(E==M){
    mins[k]++;assert((int)T.size()==M);int H=0;vector<int>dif;
    for(int s:T){assert(abs(walsh[s]*M)==16);H|=s;dif.push_back(s^T[0]);}
    assert(rank2(dif)==k&&pc(H)<=2*k);
   }else {assert(E>=M+2);gap[k]=min(gap[k],E-M);}
  }
 advance:
  int x=0;while(x<16&&val[x]==1){val[x]=-1;for(int s=0;s<16;s++)walsh[s]-=2*character[x][s];x++;}
  if(x==16)break;
  val[x]++;for(int s=0;s<16;s++)walsh[s]+=character[x][s];
 }while(true);
 assert(count==43046721);
 cout<<"{\"status\":\"PASS\",\"tables_including_zero\":"<<count<<",\"by_degree\":[";
 for(int k=0;k<=4;k++)cout<<(k?",":"")<<hist[k];cout<<"],\"minima_by_degree\":[";
 for(int k=0;k<=4;k++)cout<<(k?",":"")<<mins[k];cout<<"],\"smallest_nonminimum_energy_gap\":[";
 for(int k=1;k<=4;k++)cout<<(k>1?",":"")<<gap[k];cout<<"]}\n";
}

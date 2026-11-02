// Full truth-table tests, independent of cap generation and verification code.
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int degree(const vector<int>& p){int d=0;for(unsigned s=0;s<p.size();s++)if(p[s])d=max(d,__builtin_popcount(s));return d;}
int potential(const vector<int>& p,int n){
 vector<int> local(n,0);for(unsigned s=1;s<p.size();s++)if(p[s])for(int i=0;i<n;i++)if(s>>i&1)local[i]=max(local[i],__builtin_popcount(s));
 int value=0;for(int d:local)if(d)value+=1<<(n-d);return value;
}
int main(){
 uint64_t derivatives=0,restrictions=0,weighted=0;
 for(int n=1;n<=4;n++){
  int N=1<<n;uint32_t total=1u<<N;
  for(uint32_t word=0;word<total;word++){
   vector<int> vals(N),p(N);for(int x=0;x<N;x++)vals[x]=p[x]=(word>>x&1)?1:-1;
   for(int b=1;b<N;b*=2)for(int x=0;x<N;x+=2*b)for(int j=0;j<b;j++){
     int a=p[x+j],c=p[x+j+b];p[x+j]=a+c;p[x+j+b]=a-c;
   }
   int d=degree(p),orig=potential(p,n);
   for(int i=0;i<n;i++){
    unsigned H=0;int di=0;
    for(unsigned s=0;s<unsigned(N);s++)if(p[s]&&(s>>i&1)){H|=s^(1u<<i);di=max(di,__builtin_popcount(s));}
    if(!di)continue;
    derivatives++;
    int h=__builtin_popcount(H),k=di-1,M=1<<k,e=0;
    for(int x=0;x<N;x++)if(!(x>>i&1))e+=(vals[x]!=vals[x|(1<<i)]);
    assert(int64_t(h)*N<=int64_t(2*k)*2*e*M);
    assert((int64_t(2*e)*M*M)%N==0);
    int64_t energy=int64_t(2*e)*M*M/N;
    if(k)assert(energy%2==0);
    if(k>=2&&int64_t(2*e)*M<2*N){
     bool found=false;for(int j=0;j<k;j++)if(int64_t(2*e)*M*(1<<j)==int64_t(N)*(2*(1<<j)-1))found=true;
     assert(found);
    }
    vector<int> controls;for(int j=0;j<n;j++)if(H>>j&1)controls.push_back(j);
    int cost=0;
    for(int j:controls){int dj=0;for(unsigned s=0;s<unsigned(N);s++)if(p[s]&&(s>>j&1))dj=max(dj,__builtin_popcount(s));cost+=1<<(n-dj);}
    int sum=0;
    for(int assignment=0;assignment<(1<<h);assignment++){
     unsigned full=0;for(int j=0;j<h;j++)if(assignment>>j&1)full|=1u<<controls[j];
     vector<int> branch(N);
     for(unsigned s=0;s<unsigned(N);s++)if(p[s])branch[s&~H]+=(__builtin_popcount(s&full)%2?-p[s]:p[s]);
     if(d>=2){assert(degree(branch)<=d-1);restrictions++;}
     // An active branch must be a signed dictator on i.
     int low=full&~(1u<<i),hi=low|(1u<<i);
     if(vals[low]!=vals[hi]){
       int count=0;for(unsigned s=0;s<unsigned(N);s++)if(branch[s]){count++;assert(s==(1u<<i)&&abs(branch[s])==N);}
       assert(count==1);
     }
     sum+=potential(branch,n);
    }
    assert(orig*(1<<h)<=cost*(1<<h)+sum);weighted++;
   }
  }
 }
 cout<<"{\"status\":\"PASS\",\"all_boolean_tables\":65812,\"derivatives\":"<<derivatives
 <<",\"degree_drop_branches\":"<<restrictions<<",\"weighted_restriction_checks\":"<<weighted<<"}\n";
}

// Exact finite controls for the universal written completion argument.
// These finite tests do not substitute for its proof or lattice premises.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
static int c8[]={0,4,8,10,11};
static uint64_t functions=0,eligible=0,retained=0,ternaries=0,edges=0;
void check(const std::vector<int>&f,int n){
 int N=1<<n;assert((int)f.size()==N);functions++;
 std::vector<int>a=f;for(int w=1;w<N;w*=2)for(int b=0;b<N;b+=2*w)for(int j=0;j<w;j++){
  int u=a[b+j],v=a[b+j+w];a[b+j]=u+v;a[b+j+w]=u-v;}
 int d=0,used=0;std::vector<int>local(n);
 for(int s=1;s<N;s++)if(a[s]){int z=__builtin_popcount((unsigned)s);d=std::max(d,z);used|=s;for(int j=0;j<n;j++)if(s>>j&1)local[j]=std::max(local[j],z);}
 if(d<3||d>4)return;
 for(int j=0;j<n;j++)if(local[j]&&local[j]!=d)return;
 eligible++;int rel=__builtin_popcount((unsigned)used),M=1<<(d-1),b16=8;
 for(int t=1;t<=d-2;t++)b16=std::max(b16,4+(16>>(t+1))+c8[t]);
 for(int i=0;i<n;i++)if(used>>i&1){
  int H=0;for(int s=1;s<N;s++)if(a[s]&&(s>>i&1))H|=s^(1<<i);
  int h=__builtin_popcount((unsigned)H);std::vector<int>A(N);int active=0;
  for(int x=0;x<N;x++){A[x]=(f[x&~(1<<i)]-f[x|(1<<i)])/2;active+=A[x]!=0;}
  int64_t ordinary=int64_t(1<<d)*c8[d-1]*N+int64_t(h+1)*8*N-int64_t(2*c8[d-1])*M*active;
  assert(int64_t(rel)*8*N<=ordinary);
  for(int j=0;j<n;j++)if(H>>j&1){
   int sum=0;for(int x=0;x<N;x++){int z=A[x]-A[x^(1<<j)];sum+=z*z;}
   if(int64_t(sum)*(1<<d)!=4*N||M*active<=N)continue;
   retained++;int q=0,r=0;
   for(int x=0;x<N;x++){
    int u=A[x],v=A[x^(1<<j)];assert(std::abs(u-v)<=1);
    q+=bool(u)!=bool(v);r+=bool(u)&&bool(v);
   }
   assert(q*(1<<d)==4*N&&r>0&&2*active==q+2*r);
   int K=H^(1<<j);
   for(int s=1;s<N;s++)if(a[s]&&__builtin_popcount((unsigned)s)==d)assert(s&K);
   int64_t value=int64_t(1<<d)*c8[d-1]*N+int64_t(h)*8*N-int64_t(2*c8[d-1])*M*active;
   value+=int64_t(2*b16-2*c8[d-1]-8)*N;
   assert(int64_t(rel)*8*N<=value);
  }
 }
}
int main(){
 for(int n=0;n<=4;n++){
  int N=1<<n;uint64_t total=uint64_t(1)<<N;
  for(uint64_t bits=0;bits<total;bits++){
   std::vector<int>f(N);for(int x=0;x<N;x++)f[x]=(bits>>x&1)?-1:1;check(f,n);
  }
 }
 // A separately given homogeneous Boolean completion of the six-cycle A2.
 std::vector<int>core(256);
 for(int x=0;x<256;x++){
  auto X=[&](int j){return (x>>j&1)?-1:1;};
  int g=(X(0)*X(2)+X(1)*X(2)+X(0)*X(3)-X(1)*X(3))/2;
  int h=(X(0)*X(2)+X(4)*X(2)+X(0)*X(5)-X(4)*X(5))/2;
  assert(std::abs(g)==1&&std::abs(h)==1);
  core[x]=(X(6)*(g-h)+X(7)*(g+h))/2;assert(std::abs(core[x])==1);
 }
 check(core,8);
 for(int n=0;n<=3;n++){
  int N=1<<n;uint64_t total=1;for(int x=0;x<N;x++)total*=3;
  for(uint64_t code=0;code<total;code++){
   std::vector<int>A(N);uint64_t v=code;int active=0;
   for(int x=0;x<N;x++){A[x]=int(v%3)-1;v/=3;active+=A[x]!=0;}
   ternaries++;std::vector<int>a=A;
   for(int w=1;w<N;w*=2)for(int b=0;b<N;b+=2*w)for(int j=0;j<w;j++){
    int u=a[b+j],z=a[b+j+w];a[b+j]=u+z;a[b+j+w]=u-z;}
   int k=0;for(int s=1;s<N;s++)if(a[s])k=std::max(k,__builtin_popcount((unsigned)s));
   if(k<1||active*(1<<k)<=N)continue;
   for(int j=0;j<n;j++){
    int sum=0;for(int x=0;x<N;x++){int z=A[x]-A[x^(1<<j)];sum+=z*z;}
    if(sum*(1<<(k+1))!=4*N)continue;
    bool edge=false;for(int x=0;x<N;x++)if(A[x]&&A[x^(1<<j)]){assert(A[x]==A[x^(1<<j)]);edge=true;}
    assert(edge);edges++;
   }
  }
 }
 assert(retained>0&&edges>0);
 std::cout<<"{\"status\":\"PASS\",\"Boolean_tables\":"<<functions<<",\"full_local_degree_tables\":"<<eligible<<",\"retained_cases\":"<<retained<<",\"ternary_tables\":"<<ternaries<<",\"active_edge_cases\":"<<edges<<"}\n";
}

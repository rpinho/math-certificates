// Independent semantic check of numerical state data; no producer code used.
// State meaning: end vertex, service-start ticks, accumulated reduced reward,
// and remembered visited vertices (translated to global bit positions).
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;
struct L{int v,t,w;U m;};
int main(int argc,char**argv){
 ifstream in("model.txt");int n;in>>n;assert(n>0&&n<63);
 vector<int>s(n),a(n),b(n),w(n);vector<vector<int>>d(n,vector<int>(n));
 for(int i=0;i<n;i++)in>>s[i]>>a[i]>>b[i]>>w[i];
 for(auto&r:d)for(int&x:r)in>>x;
 // All-pairs shortest paths: flooring can break the triangle inequality.
 auto sp=d;for(int k=0;k<n;k++)for(int i=0;i<n;i++)for(int j=0;j<n;j++)sp[i][j]=min(sp[i][j],sp[i][k]+sp[k][j]);
 ifstream p(argc>1?argv[1]:"input/upper.proof");string magic;p>>magic;assert(magic=="NGBOUND2");
 int nn,B,unused;p>>nn>>B>>unused;assert(nn==n&&B>=0);
 vector<vector<int>>ng(n);vector<U>mask(n);
 for(int i=0;i<n;i++){int k;p>>k;assert(k>0&&k<=n);while(k--){int j;p>>j;assert(j>=0&&j<n);ng[i].push_back(j);mask[i]|=U(1)<<j;}assert(mask[i]&(U(1)<<i));}
 int count;p>>count;assert(count>0&&count<10000000);
 vector<vector<L>>labels(n);vector<L>all;
 for(int k=0;k<count;k++){
  int v,t,z;U local;p>>v>>t>>z>>local;assert(v>=0&&v<n&&local<(U(1)<<ng[v].size()));
  t-=s[v]; // serialized time is departure; internally use service start
  U m=0;for(int h=0;h<(int)ng[v].size();h++)if(local&(U(1)<<h))m|=U(1)<<ng[v][h];
  if(!((m&(U(1)<<v))&&t>=a[v]&&t<=b[v]&&z>=0&&z<=B)){
    cerr<<"bad label "<<k<<" v "<<v<<" t "<<t<<" w "<<z<<" mask "<<local<<" global "<<m<<" window "<<a[v]<<' '<<b[v]<<endl;return 3;
  }
  L l{v,t,z,m};labels[v].push_back(l);all.push_back(l);
 }
 auto covered=[&](L x){for(auto y:labels[x.v])if(y.t<=x.t&&y.w>=x.w&&(y.m&x.m)==y.m)return true;return false;};
 assert(covered({0,a[0],0,1}));
 long long edges=0,missing=0,invalid=0;
 ofstream miss("missing.txt");
 for(auto x:all){
  if(x.t+s[x.v]+d[x.v][0]<=b[0])assert(x.w<=B);
  for(int j=1;j<n;j++){
   if(x.m&(U(1)<<j))continue;
   int t=max(a[j],x.t+s[x.v]+d[x.v][j]);
   if(t>b[j]||t+s[j]+sp[j][0]>b[0]){invalid++;continue;}
   L y{j,t,x.w+w[j],(x.m&mask[j])|(U(1)<<j)};edges++;
   if(!covered(y)){missing++;miss<<y.v<<' '<<y.t<<' '<<y.w<<' '<<y.m<<'\n';}
  }
 }
 cout<<"states "<<count<<" transitions "<<edges<<" missing "<<missing<<" infeasible "<<invalid<<endl;
 return missing?2:0;
}

// Literal vertex-list DFS, independent of all transfer-state implementations.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
int N;
int range_limit=99,span_limit=40,min_span=1,crossing_cap=99;
bool seen[50][100];
int cuts[50],px[50],py[50];
uint64_t bridges[50][50],irreducible[50][50],prefixes=0,checked=0;
void factor_check(int n,int h) {
 int previous=0,span=0;
 for(int j=1;j<=h;++j)if(j==h || cuts[j]==1) {
  int end=n;
  if(j<h){for(int i=1;i<=n;++i)if(px[i-1]==j && px[i]==j+1){end=i-1;break;}}
  if(end<=previous)throw std::runtime_error("empty factor");
  for(int i=previous+1;i<=end;++i)
   if(px[i]<=span || px[i]>j)throw std::runtime_error("bad strict factor");
  if(px[end]!=j)throw std::runtime_error("factor endpoint");
  for(int t=span+1;t<j;++t)if(cuts[t]<3)throw std::runtime_error("reducible factor");
  previous=end;span=j;
 }
 if(previous!=n)throw std::runtime_error("incomplete factorization");
 ++checked;
}
void visit(int n,int x,int y,int maximum,int ymin,int ymax) {
 ++prefixes;px[n]=x;py[n]=y;
 if(x==maximum && x>=min_span) {
  ++bridges[n][x];bool irr=true;
  for(int j=1;j<x;++j)if(cuts[j]<3)irr=false;
  if(irr)++irreducible[n][x];
  if(n<=16)factor_check(n,x);
 }
 if(n==N)return;
 const int dx[]={1,-1,0,0},dy[]={0,0,1,-1};
 for(int d=0;d<4;++d) {
  int X=x+dx[d],Y=y+dy[d];
  if(X<=0||X>span_limit||seen[X][Y+45])continue;
  int lo=std::min(ymin,Y),hi=std::max(ymax,Y);if(hi-lo>range_limit)continue;
  int c=std::min(x,X);if(dx[d])++cuts[c];
  if(!dx[d] || cuts[c]<=crossing_cap){
   seen[X][Y+45]=true;visit(n+1,X,Y,std::max(maximum,X),lo,hi);seen[X][Y+45]=false;
  }
  if(dx[d])--cuts[c];
 }
}
int main(int argc,char**argv) {
 if(argc!=3 && argc!=7)return 1;N=std::stoi(argv[1]);if(N<1||N>30)return 2;
 if(argc==7){range_limit=std::stoi(argv[3]);span_limit=std::stoi(argv[4]);min_span=std::stoi(argv[5]);crossing_cap=std::stoi(argv[6]);}
 seen[0][45]=seen[1][45]=true;cuts[0]=1;visit(1,1,0,1,0,0);
 std::ofstream o(argv[2]);o<<"{\"N\":"<<N<<",\"prefixes\":"<<prefixes<<",\"factorizations_checked\":"<<checked<<",\"rows\":[";
 for(int n=1;n<=N;++n)for(int h=1;h<=n;++h){if(n!=1||h!=1)o<<",";o<<"["<<n<<","<<h<<","<<bridges[n][h]<<","<<irreducible[n][h]<<"]";}o<<"]}\n";
 std::cerr<<"prefixes="<<prefixes<<" factorizations="<<checked<<"\n";
}

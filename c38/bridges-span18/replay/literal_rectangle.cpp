#include "transfer.hpp"
static int h,W;static uint64_t seen;static int cross[32];static std::vector<U> coeff;
void dfs(int x,int y,int n){
 if(x==h){bool good=true;for(int j=1;j<h;j++)good&=cross[j]>=3&&cross[j]<=5&&cross[j]%2==1;if(good)coeff[n]++;}
 int dx[4]={1,-1,0,0},dy[4]={0,0,1,-1};
 for(int i=0;i<4;i++){
  int xx=x+dx[i],yy=y+dy[i];if(xx<1||xx>h||yy<0||yy>W)continue;
  uint64_t bit=1ULL<<((xx-1)*(W+1)+yy);if(seen&bit)continue;
  int cut=std::min(x,xx);if(xx!=x)cross[cut]++;
  seen|=bit;dfs(xx,yy,n+1);seen^=bit;if(xx!=x)cross[cut]--;
 }
}
int main(){for(W=0;W<=4;W++){
 std::vector<U> total(5*(W+1)+1);
 for(h=2;h<=5;h++){
  coeff.assign(h*(W+1)+1,0);for(int s=0;s<=W;s++){seen=1ULL<<s;dfs(1,s,1);}
  for(size_t n=0;n<coeff.size();n++)total[n]+=coeff[n];
 }
 std::cout<<"{\"frame_range\":"<<W<<",\"span_min\":2,\"span_max\":5,\"coefficients\":[";for(size_t n=0;n<total.size();n++)std::cout<<(n?",":"")<<'"'<<dec(total[n])<<'"';std::cout<<"]}"<<std::endl;
}}

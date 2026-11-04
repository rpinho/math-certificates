#include "transfer.hpp"
#include <unordered_map>
using Poly=std::vector<U>;
static int h,w,N;static uint64_t visited;static std::vector<U> brute;
// Literal oriented vertex-sequence DFS, separately from the edge-subset transfer.
void walk(int x,int y,int n,bool bottom){
 if(x==h&&bottom)brute[n]++;
 if(n==N)return;
 const int dx[4]={1,-1,0,0},dy[4]={0,0,1,-1};
 for(int k=0;k<4;k++){
  int a=x+dx[k],b=y+dy[k];if(a<1||a>h||b<0||b>=w)continue;
  uint64_t bit=1ULL<<((a-1)*w+b);if(visited&bit)continue;
  visited|=bit;walk(a,b,n+1,bottom||b==0);visited^=bit;
 }
}
int main(){try{
 for(h=1;h<=12;h++)for(w=1;w<=3;w++){
  N=w<=2?h*w:std::min(18,h*w);brute.assign(N+1,0);
  for(int s=0;s<w;s++){visited=1ULL<<s;walk(1,s,1,s==0);}
  std::unordered_map<K,Poly> cur,next;cur[0]=Poly(N+1);cur[0][0]=1;Poly counted(N+1);
  for(int col=0;col<w;col++){
   for(int r=0;r<=h;r++){
    next.clear();for(auto &it:cur){Moves m=strip_moves(it.first,h,r);
     for(unsigned j=0;j<m.n;j++){
      auto v=m.a[j];if(v.done){for(int n=0;n+v.k<=N;n++)counted[n+v.k]+=it.second[n];}
      else{auto&dest=next[v.key];if(dest.empty())dest.resize(N+1);for(int n=0;n+v.k<=N;n++)dest[n+v.k]+=it.second[n];}
     }
    }
    for(auto it=next.begin();it!=next.end();){bool nz=false;for(U a:it->second)nz|=a!=0;if(!nz)it=next.erase(it);else ++it;}
    cur.swap(next);
   }
   if(col==0)cur.erase(0);
  }
  need(counted==brute,"literal coefficient mismatch");std::cout<<"{\"span\":"<<h<<",\"width\":"<<w<<",\"max_length\":"<<N<<",\"coefficients\":[";for(int n=0;n<=N;n++)std::cout<<(n?",":"")<<'"'<<dec(brute[n])<<'"';std::cout<<"],\"match\":true}"<<std::endl;
 }
}catch(std::exception&e){std::cerr<<e.what()<<std::endl;return 1;}}

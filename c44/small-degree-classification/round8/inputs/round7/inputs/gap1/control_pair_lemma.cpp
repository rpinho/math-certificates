// Exhaustive small controls for the new universal pair lemma, not its proof.
#include <cassert>
#include <iostream>
#include <vector>
int degree(std::vector<int> a){
  for(unsigned step=1;step<a.size();step*=2)
    for(unsigned b=0;b<a.size();b+=2*step)
      for(unsigned j=b;j<b+step;++j){int u=a[j],v=a[j+step];a[j]=u+v;a[j+step]=u-v;}
  int d=0;for(unsigned s=0;s<a.size();++s)if(a[s])d=std::max(d,__builtin_popcount(s));return d;
}
int relevance(const std::vector<int>& a){
  int n=0;for(unsigned bit=1;bit<a.size();bit*=2){bool yes=false;
    for(unsigned x=0;x<a.size();++x)if(a[x]!=a[x^bit])yes=true;
    n+=yes;}return n;
}
int main(){
  int counts[5]={};
  for(unsigned table=0;table<65536;++table){
    std::vector<int> f(16),g(4),h(8);
    for(unsigned x=0;x<16;++x)f[x]=(table>>x&1)?-1:1;
    bool property=true;
    for(unsigned z=0;z<4;++z){g[z]=f[(z<<2)|2];if(f[(z<<2)|1]!=-g[z])property=false;}
    if(!property)continue;
    for(unsigned z=0;z<4;++z)for(unsigned s=0;s<2;++s)h[(z<<1)|s]=(s?-1:1)*f[(z<<2)|s|(s<<1)];
    int df=degree(f),dg=degree(g),dh=degree(h);
    for(int d=2;d<=4;++d)if(df<=d&&dg<=d-1){
      assert(dh<=d-1);assert(relevance(f)<=2+relevance(g)+relevance(h));++counts[d];
    }
  }
  assert(counts[2]>0&&counts[3]>counts[2]&&counts[4]==4096);
  std::cout<<"{\"status\":\"PASS\",\"tables\":65536,\"eligible_degree2\":"<<counts[2]
           <<",\"eligible_degree3\":"<<counts[3]<<",\"eligible_degree4\":"<<counts[4]<<"}\n";
}

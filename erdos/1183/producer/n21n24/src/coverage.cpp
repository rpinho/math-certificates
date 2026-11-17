// Separate coverage checker. Reads only prefix labels already checked against
// concrete families / exhaustive trees by coverage.py. No search code imported.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
struct Node {int child[2]={-1,-1}; int type=0;};
int main(int argc,char**argv){
 if(argc!=3)return 2;
 int N=stoi(argv[1]);ifstream in(argv[2]);vector<Node> nodes(1);string w;char kind;
 while(in>>kind>>w){
  int at=0;
  for(char b:w){int c=b-'0';if(c<0||c>1)return 3;
   int next=nodes[at].child[c];
   if(next<0){next=nodes.size();nodes[at].child[c]=next;nodes.emplace_back();}at=next;
  }
  if(nodes[at].type){cerr<<"duplicate label\n";return 4;}
  nodes[at].type=kind=='R'?1:kind=='G'?2:0;if(!nodes[at].type)return 5;
 }
 for(int L=1;L<=N+1;++L){
  uint32_t top=(1u<<L)-1;uint64_t good=0,orbits=0,goodorbits=0;
  for(uint32_t x=0;x<=top;++x){
   uint32_t rev=0;for(int i=0;i<L;++i)rev=(rev<<1)|((x>>i)&1);
   uint32_t v=min(min(x,top^x),min(rev,top^rev));
   if(v==x)++orbits;
   int at=0;bool rejected=false;
   for(int i=L-1;i>=0;--i){
    at=nodes[at].child[(v>>i)&1];
    if(at<0){cerr<<"missing coverage L="<<L<<" word="<<v<<"\n";return 6;}
    if(nodes[at].type==1){rejected=true;break;}
   }
   if(!rejected){if(nodes[at].type!=2){cerr<<"unproved leaf\n";return 7;}++good;if(v==x)++goodorbits;}
  }
  cout<<"{\"length\":"<<L<<",\"words\":"<<(uint64_t(1)<<L)<<",\"orbits\":"<<orbits
      <<",\"good_words\":"<<good<<",\"good_orbits\":"<<goodorbits<<"}\n";
 }
 return 0;
}

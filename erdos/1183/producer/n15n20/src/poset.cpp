// Exact weighted-poset search, written for this job from PROOF.md.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
struct Elem {uint32_t p; int w;};
struct Down {uint32_t m; int s;};
struct Edge {uint32_t p;int w;int bad;int child;};
struct Node {vector<Edge> edges;};
struct Search {
 int n,t,a; uint32_t R; uint64_t nodes=0; vector<Elem> path,answer;
 vector<Node> tree; vector<pair<int,int>> roots; int answer_a=-1;
 bool dfs(const vector<Down>& ds,int used,int id){
  ++nodes;
  if((int)ds.size()>=t){answer=path;answer_a=a;return true;}
  int k=path.size();
  for(auto I:ds){
   vector<Down> supers; for(auto d:ds)if((d.m&I.m)==I.m)supers.push_back(d);
   for(int w=1;w<=n-a-used;++w){
    int bad=-1;
    for(auto d:supers)if(!((R>>(a+d.s+w))&1)){bad=d.m;break;}
    if(bad>=0){tree[id].edges.push_back({I.m,w,bad,-1});continue;}
    vector<Down> next=ds;for(auto d:supers)next.push_back({d.m|(1u<<k),d.s+w});
    int ch=tree.size(); tree.emplace_back();tree[id].edges.push_back({I.m,w,-1,ch});
    path.push_back({I.m,w});bool found=dfs(next,used+w,ch);path.pop_back();
    if(found)return true;
   }
  }
  return false;
 }
 bool run(){
  for(a=0;a<=n;++a)if((R>>a)&1){int id=tree.size();tree.emplace_back();roots.push_back({a,id});if(dfs({{0,0}},0,id))return true;}
  return false;
 }
 void dump_node(ostream&out,int id){
  out<<"[";bool first=true;for(auto e:tree[id].edges){if(!first)out<<",";first=false;out<<"["<<e.p<<","<<e.w<<","<<e.bad<<"]";}out<<"]\n";
  for(auto e:tree[id].edges)if(e.child>=0)dump_node(out,e.child);
 }
 void proof(const string&file,const string&word,int c){
  ofstream out(file);out<<"{\"n\":"<<n<<",\"word\":\""<<word<<"\",\"colour\":"<<c<<",\"threshold\":"<<t<<",\"nodes\":"<<nodes<<"}\n";
  for(auto root:roots){out<<"{\"root\":"<<root.first<<"}\n";dump_node(out,root.second);}
 }
 vector<uint32_t> family(){
  vector<Down> ds={{0,0}};vector<uint32_t> blocks;int shift=answer_a;
  for(int k=0;k<(int)answer.size();++k){auto e=answer[k];blocks.push_back(((1u<<e.w)-1)<<shift);shift+=e.w;vector<Down> nd=ds;for(auto d:ds)if((d.m&e.p)==e.p)nd.push_back({d.m|(1u<<k),0});ds=nd;}
  vector<uint32_t> out;for(auto d:ds){uint32_t S=(1u<<answer_a)-1;for(int k=0;k<(int)blocks.size();++k)if((d.m>>k)&1)S|=blocks[k];out.push_back(S);}sort(out.begin(),out.end());return out;
 }
};
void result(const string& word,int c,int t,const string&prefix){
 Search s;s.n=word.size()-1;s.t=t;s.R=0;for(int i=0;i<=s.n;++i)if(word[i]-'0'==c)s.R|=1u<<i;
 bool yes=s.run();
 cout<<"{\"word\":\""<<word<<"\",\"colour\":"<<c<<",\"threshold\":"<<t<<",\"nodes\":"<<s.nodes<<",\"found\":"<<(yes?"true":"false");
 if(yes){cout<<",\"family\":[";auto f=s.family();for(int i=0;i<(int)f.size();++i){if(i)cout<<",";cout<<f[i];}cout<<"]";}
 else {string fn=prefix+"_"+word+"_c"+to_string(c)+"_t"+to_string(t)+".tree";s.proof(fn,word,c);cout<<",\"proof\":\""<<fn<<"\"";}
 cout<<"}\n"<<flush;
}
int main(int argc,char**argv){
 if(argc==5){result(argv[1],stoi(argv[2]),stoi(argv[3]),argv[4]);return 0;}
 string word,prefix;int c,t;while(cin>>word>>c>>t>>prefix)result(word,c,t,prefix);
}

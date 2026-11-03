// Exploratory exact overlap-graph proposer; not an acceptance verifier.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <utility>
#include <vector>
using namespace std;
using Mask=uint64_t;
struct Gate{int id,degree,norm,payload,residual,payload_count;array<int,32> local{};Mask used;bool nonminimum;vector<pair<Mask,int>> square;};
vector<Gate> gates;vector<vector<uint64_t>> compatible;vector<int> chosen,found;
uint64_t nodes=0,complete=0;int h,d,best=-1,bar;double seconds_limit;string output;
chrono::steady_clock::time_point started;bool expired=false;
int pc(Mask x){return __builtin_popcountll(x);}
void save(const string& status){
 ofstream out(output);out<<"{\"status\":\""<<status<<"\",\"qualification\":\"exploratory finite bank, at least one nonminimum gate\",\"controls\":"<<h<<",\"degree\":"<<d<<",\"nodes\":"<<nodes<<",\"complete_partitions\":"<<complete<<",\"best_potential_units\":"<<best<<",\"selected\":[";
 for(int j=0;j<(int)found.size();++j)out<<(j?",":"")<<gates[found[j]].id;
 out<<"],\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-started).count()<<"}\n";
}
void search(const vector<int>& candidates,int energy,int payload,Mask used,array<int,32> local){
 if(!found.empty()||expired)return;
 ++nodes;
 if((nodes&65535)==0){
  if(chrono::duration<double>(chrono::steady_clock::now()-started).count()>seconds_limit){expired=true;save("BUDGET");return;}
  if((nodes&1048575)==0){cerr<<"nodes "<<nodes<<" complete "<<complete<<" best "<<best<<endl;save("RUNNING");}
 }
 if(energy==256){
  ++complete;int count=payload;for(int value:local)if(value)count+=1<<(d-value);best=max(best,count);
  if(count>=bar){found=chosen;save("PARTITION_FOUND");}
  return;
 }
 int remaining=256-energy,total_norm=0,ratio_gate=-1;Mask possible=used;
 for(int v:candidates){
  if(gates[v].norm>remaining)continue;
  total_norm+=gates[v].norm;possible|=gates[v].used;
  if(ratio_gate<0||gates[v].payload*gates[ratio_gate].norm>gates[ratio_gate].payload*gates[v].norm)ratio_gate=v;
 }
 if(total_norm<remaining||ratio_gate<0)return;
 int control_upper=0;
 for(int v=0;v<h;++v){
  if(local[v])control_upper+=1<<(d-local[v]);
  else{int most=0;for(int g:candidates)if(gates[g].local[v])most=max(most,1<<(d-gates[g].local[v]));control_upper+=most;}
 }
 int upper=payload+control_upper+remaining*gates[ratio_gate].payload/gates[ratio_gate].norm;
 if(upper<bar)return;
 for(int at=0;at<(int)candidates.size();++at){
  int v=candidates[at];if(gates[v].norm>remaining)continue;
  vector<int> next;
  for(int j=at+1;j<(int)candidates.size();++j){int w=candidates[j];if(compatible[v][w>>6]>>(w&63)&1)next.push_back(w);}
  array<int,32> next_local=local;for(int j=0;j<h;++j)next_local[j]=max(next_local[j],gates[v].local[j]);
  chosen.push_back(v);search(next,energy+gates[v].norm,payload+gates[v].payload,used|gates[v].used,next_local);chosen.pop_back();
  if(!found.empty()||expired)return;
 }
}
int main(int argc,char** argv){
 assert(argc==4||argc==5);output=argv[2];seconds_limit=stod(argv[3]);started=chrono::steady_clock::now();
 ifstream input(argv[1]);assert(input.good());int count;input>>count>>h>>d;assert(h<=32&&d>=2&&d<=8);bar=argc==5?stoi(argv[4]):3*(1<<(d-1))-1;
 for(int id=0;id<count;++id){
  Gate gate;gate.id=id;int terms,coefficient;Mask mask;
  input>>gate.degree>>gate.norm>>gate.used>>gate.residual>>terms;
  for(int j=0;j<terms;++j){input>>mask>>coefficient;for(int v=0;v<h;++v)if(mask>>v&1)gate.local[v]=max(gate.local[v],pc(mask)+gate.residual);}
  input>>terms;for(int j=0;j<terms;++j){input>>mask>>coefficient;gate.square.emplace_back(mask,coefficient);}
  assert(is_sorted(gate.square.begin(),gate.square.end()));
  gate.payload_count=3*(1<<(gate.residual-1))-2;gate.payload=gate.payload_count*(1<<(d-gate.degree-gate.residual));gate.nonminimum=gate.norm*(1<<gate.degree)>256;gates.push_back(move(gate));
 }
 string extra;assert(!(input>>extra));
 compatible.assign(count,vector<uint64_t>((count+63)/64));uint64_t edges=0;
 for(int i=0;i<count;++i)for(int j=0;j<i;++j){
  const auto& a=gates[i].square;const auto& b=gates[j].square;size_t u=0,v=0;long long product=0;
  while(u<a.size()&&v<b.size()){
   if(a[u].first<b[v].first)++u;else if(b[v].first<a[u].first)++v;else{product+=1ll*a[u].second*b[v].second;++u;++v;}
  }
  assert(product>=0);
  if(product==0){compatible[i][j>>6]|=1ull<<(j&63);compatible[j][i>>6]|=1ull<<(i&63);++edges;}
 }
 cerr<<"graph gates "<<count<<" compatible edges "<<edges<<endl;save("GRAPH_READY");
 vector<int> order(count);iota(order.begin(),order.end(),0);
 stable_sort(order.begin(),order.end(),[](int a,int b){return gates[a].payload*gates[b].norm>gates[b].payload*gates[a].norm;});
 // Anchor at the smallest selected nonminimum index. All minimum gates
 // remain eligible. This covers every partition in this restricted family.
 for(int anchor=0;anchor<count&&!expired&&found.empty();++anchor)if(gates[anchor].nonminimum){
  vector<int> candidates;for(int v:order)if((!gates[v].nonminimum||v>anchor)&&(compatible[anchor][v>>6]>>(v&63)&1))candidates.push_back(v);
  chosen={anchor};search(candidates,gates[anchor].norm,gates[anchor].payload,gates[anchor].used,gates[anchor].local);
 }
 save(!found.empty()?"PARTITION_FOUND":expired?"BUDGET":"FINITE_BANK_NO_MATCH");
 cout<<"nodes "<<nodes<<" complete "<<complete<<" best "<<best<<" found "<<found.size()<<endl;
}

// Exploratory exact unsigned completion with no homogeneous minimum partial.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <vector>
#include <functional>
using namespace std;
struct Pattern {array<uint16_t,16> t;uint16_t vars;bool homogeneous;};
const int n=13, ALL=(1<<13)-1;
vector<array<uint16_t,16>> base;
int pc(int x){return __builtin_popcount((unsigned)x);}
vector<int> tensor(vector<int> blocks,int coordinate){
 vector<int> s={1<<coordinate};
 for(int block:blocks){vector<int> factor;
  if(pc(block)==1)factor={0,block};
  else for(int t=block;;t=(t-1)&block){if((pc(t)&1)==(pc(block)%2==0))factor.push_back(t);if(!t)break;}
  vector<int> next;for(int a:s)for(int b:factor)next.push_back(a|b);s=next;
 }
 sort(s.begin(),s.end());assert(s.size()==16);return s;
}
void build(vector<int> blocks,int avail,int cost,pair<int,int> lower){
 if(cost==4){auto s=tensor(blocks,0);bool homogeneous=true;for(int t:s)homogeneous&=pc(t)==5;
  {array<uint16_t,16> p;copy(s.begin(),s.end(),p.begin());base.push_back(p);}return;}
 for(int size=1;size<=5;size++){int c=max(1,size-1);if(cost+c>4)continue;
  for(int b=avail;b;b=(b-1)&avail)if(pc(b)==size && make_pair(size,b)>=lower){auto v=blocks;v.push_back(b);build(v,avail^b,cost+c,{size,b});}
 }
}
vector<Pattern> pats[n];vector<int> by[n][1<<n];
bool contains[1<<n];vector<int> E;int energy[n],loss=0,bad;long long nodes,models;vector<int> good;
void add(int t){contains[t]=true;E.push_back(t);loss+=5-pc(t);for(int j=0;j<n;j++)if(t>>j&1)energy[j]++;}
void popto(int size){while((int)E.size()>size){int t=E.back();E.pop_back();contains[t]=false;loss-=5-pc(t);for(int j=0;j<n;j++)if(t>>j&1)energy[j]--;}}
vector<int> options(int j,int done){
 vector<int>*pool=nullptr;vector<int> req;
 for(int t:E)if(t>>j&1){req.push_back(t);auto &v=by[j][t];if(!pool || v.size()<pool->size())pool=&v;}
 vector<int> out;
 auto check=[&](int z){auto &p=pats[j][z];if(p.homogeneous)return;int added=0,extra_loss=0;
  for(int t:req)if(!binary_search(p.t.begin(),p.t.end(),t))return;
  for(int t:p.t)if(!contains[t]){if(t&done)return;added++;extra_loss+=5-pc(t);}
  if(E.size()+added>48 || loss+extra_loss>32)return;
  out.push_back(z);
 };
 if(pool){for(int z:*pool)check(z);}else for(int z=0;z<(int)pats[j].size();z++)check(z);
 return out;
}
string dfs(int done){
 nodes++;int rem=48-E.size();if(rem<0)return "[0]";if(loss>32)return "[1]";
 if(energy[bad]+rem<16)return "[2]";
 int unseen=0;for(int j:good)if(!energy[j])unseen++;
 if((unseen>=2 && rem<24)||(unseen && rem<16))return "[3]";
 if(pc(done)==12){bool feasible=false;
  for(int a=0;a*a<=rem;a++)for(int b=0;a*a+b*b<=rem;b++)if(a*a+b*b==rem){
   int be=energy[bad]+b*b;if(be!=16 && be<24)continue;
   if(loss+5*a*a+4*b*b>32)continue;
   if(be==16){if(b>1)continue;vector<int> req;for(int t:E)if(t>>bad&1)req.push_back(t);if(b)req.push_back(1<<bad);sort(req.begin(),req.end());bool found=false;
    if(req.size()==16)for(int z:by[bad][req[0]])if(!pats[bad][z].homogeneous && equal(req.begin(),req.end(),pats[bad][z].t.begin())){found=true;break;}
    if(!found)continue;
   }
   feasible=true;
  }
  if(feasible){models++;return "[6]";}return "[7]";
 }
 int chosen=-1;vector<int> choice;
 for(int j:good)if(!(done>>j&1)){
  if(energy[j]>16)return "[8,"+to_string(j)+"]";
  auto out=options(j,done);if(out.empty())return "[4,"+to_string(j)+"]";
  if(chosen<0 || out.size()<choice.size()){chosen=j;choice=move(out);}
 }
 string tree="[5,"+to_string(chosen)+",[";bool first=true;
 int old=E.size();for(int z:choice){for(int t:pats[chosen][z].t)if(!contains[t])add(t);auto child=dfs(done|(1<<chosen));popto(old);
  if(!first)tree+=",";first=false;tree+="["+to_string(z)+","+child+"]";
 }return tree+"]]";
}
int main(){
 cout<<"BUILD"<<endl;build({},ALL^1,0,{0,0});sort(base.begin(),base.end());base.erase(unique(base.begin(),base.end()),base.end());cout<<"BASE "<<base.size()<<endl;
 ofstream binary("quintic_minimum_templates.bin",ios::binary);for(auto row:base)binary.write((char*)row.data(),32);binary.close();
 ofstream proof("quintic13_nonhomogeneous_certificate.json");proof<<"{\"schema\":\"quintic13-nonhomogeneous-v1\",\"status\":\"candidate, unrefereed\",\"template_count\":"<<base.size()<<",\"cases\":[";bool firstcase=true;
 for(int j=0;j<n;j++){
  for(auto a:base){Pattern p;int v=0;
   for(int i=0;i<16;i++){int t=a[i];if(bool(t&1)!=bool(t&(1<<j)))t^=1|(1<<j);p.t[i]=t;v|=t;}
   sort(p.t.begin(),p.t.end());p.vars=v;p.homogeneous=true;for(int t:p.t)p.homogeneous&=pc(t)==5;pats[j].push_back(p);
  }
  for(int z=0;z<(int)pats[j].size();z++)for(int t:pats[j][z].t)by[j][t].push_back(z);
 }
 int caseid=0;long long allmodels=0;
 for(int r=0;r<=4;r++)for(int b2=0;b2<=4;b2++)for(int b3=0;b3<=2;b3++)for(int b4=0;b4<=1;b4++)for(int b5=0;b5<=1;b5++){
  if(r+b2+2*b3+3*b4+4*b5!=4 || b2==4)continue;
  vector<int> blocks,orbits;int at=1;
  for(auto item:vector<pair<int,int>>{{1,r},{2,b2},{3,b3},{4,b4},{5,b5}})if(item.second){orbits.push_back(at);for(int z=0;z<item.second;z++){int block=0;for(int t=0;t<item.first;t++)block|=1<<at++;blocks.push_back(block);}}
  orbits.push_back(at);auto seed=tensor(blocks,0);
  for(int bd:orbits){bad=bd;good.clear();for(int j=0;j<n;j++)if(j!=bad)good.push_back(j);E.clear();fill(begin(contains),end(contains),false);fill(begin(energy),end(energy),0);loss=0;for(int t:seed)add(t);nodes=models=0;
   string tree=dfs(1);if(!firstcase)proof<<",";firstcase=false;proof<<"{\"type\":["<<r<<","<<b2<<","<<b3<<","<<b4<<","<<b5<<"],\"bad\":"<<bad<<",\"nodes\":"<<nodes<<",\"models\":"<<models<<",\"tree\":"<<tree<<"}";cout<<"CASE "<<caseid++<<" type "<<r<<","<<b2<<","<<b3<<","<<b4<<","<<b5<<" bad "<<bad<<" nodes "<<nodes<<" models "<<models<<endl;allmodels+=models;
  }
 }
 proof<<"]}\n";proof.close();cout<<"DONE cases "<<caseid<<" models "<<allmodels<<endl;
}

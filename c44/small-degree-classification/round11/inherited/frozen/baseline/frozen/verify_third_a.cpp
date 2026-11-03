// Exact verifier A, written separately from search_third.cpp.
// Elementary supports are computed from truth tables; forced coefficients
// are held in a mutable incidence array rather than copied set unions.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
using Pattern=array<int,16>;
int dimensions, target=56, maxloss, mask_count;
vector<Pattern> catalog;
vector<vector<int>> inverted;
vector<bool> is_nonhom;
vector<uint32_t> template_union;
vector<int> template_loss;
map<tuple<int,uint32_t,vector<int>>,vector<int>> compatibility_cache;
size_t cached_ids=0;
array<vector<int>,6> factor_spectrum;
vector<int> type, group_sizes, groups;
vector<unsigned char> present;
vector<int> forced;
array<int,32> energy{};
int loss=0;
uint64_t visits=0, closures=0, scans=0, unresolved=0, odd_rejections=0, flat_rejections=0;
bool nonhomogeneous_case;
uint32_t selected;
inline int weight(int x){return __builtin_popcount((unsigned)x);}
int relabel(int x,int position){
 bool first=x%2,other=(x>>position)%2;
 return first==other?x:x^(1+(1<<position));
}
Pattern product_spectrum(int v,const vector<int>& bs){
 vector<int> result{1<<v};
 for(int block:bs){
  vector<int> coords;for(int i=0;i<dimensions;++i)if((block>>i)&1)coords.push_back(i);
  vector<int> mapped;for(int local:factor_spectrum[coords.size()]){
   int x=0;for(int j=0;j<(int)coords.size();++j)if((local>>j)&1)x|=1<<coords[j];mapped.push_back(x);
  }
  vector<int> next;for(int a:result)for(int b:mapped)next.push_back(a+b);result.swap(next);
 }
 assert(result.size()==16);sort(result.begin(),result.end());Pattern p;copy(result.begin(),result.end(),p.begin());return p;
}
void assign_groups(int at,int used){
 if(at==(int)group_sizes.size()){
  catalog.push_back(product_spectrum(0,groups));return;
 }
 int size=group_sizes[at];vector<int> available;
 for(int x=1;x<dimensions;++x)if(!((used>>x)&1))available.push_back(x);
 vector<int> positions(size);iota(positions.begin(),positions.end(),0);
 if((int)available.size()<size)return;
 while(true){
  int block=0;for(int i:positions)block|=1<<available[i];
  if(at==0||group_sizes[at-1]!=size||block>groups.back()){
   groups.push_back(block);assign_groups(at+1,used|block);groups.pop_back();
  }
  int t=size-1;while(t>=0&&positions[t]==(int)available.size()-size+t)--t;
  if(t<0)break;
  ++positions[t];for(int k=t+1;k<size;++k)positions[k]=positions[k-1]+1;
 }
}
void choose_types(int size,int cost){
 if(size==6){
  if(cost!=4)return;
  group_sizes.clear();for(int m=1;m<=5;++m)for(int c=0;c<type[m-1];++c)group_sizes.push_back(m);
  assign_groups(0,1);return;
 }
 int unit=max(1,size-1);
 for(int count=0;cost+count*unit<=4;++count){type[size-1]=count;choose_types(size+1,cost+count*unit);}
}
void initialize(){
 for(int m=1;m<=5;++m){
  vector<int> values(1<<m);values[0]=1;
  if(m>1)values.back()=(m%2)?1:-1;
  for(int mask=0;mask<(1<<m);++mask){
   int coefficient=0;for(int x=0;x<(1<<m);++x)coefficient+=(weight(mask&x)%2?-values[x]:values[x]);
   if(coefficient)factor_spectrum[m].push_back(mask);
  }
  assert(factor_spectrum[m].size()==size_t(1<<max(1,m-1)));
 }
 type.resize(5);choose_types(1,0);
 sort(catalog.begin(),catalog.end());catalog.erase(unique(catalog.begin(),catalog.end()),catalog.end());
 inverted.resize(mask_count);is_nonhom.resize(catalog.size());template_union.resize(catalog.size());template_loss.resize(catalog.size());
 for(int id=0;id<(int)catalog.size();++id){
  int intersection=mask_count-1;
  for(int s:catalog[id]){assert(s%2&&weight(s)<=5);intersection&=s;template_union[id]|=s;template_loss[id]+=5-weight(s);inverted[s].push_back(id);if(weight(s)!=5)is_nonhom[id]=true;}
  assert(intersection==1);
 }
 present.assign(mask_count,0);
}
vector<int> install(const Pattern& p){
 vector<int> added;
 for(int s:p)if(!present[s]){
  present[s]=1;forced.push_back(s);added.push_back(s);loss+=5-weight(s);
  for(int i=0;i<dimensions;++i)if((s>>i)&1)++energy[i];
 }
 return added;
}
void undo(const vector<int>& added){
 for(auto i=added.rbegin();i!=added.rend();++i){
  int s=*i;assert(forced.back()==s);forced.pop_back();present[s]=0;loss-=5-weight(s);
  for(int v=0;v<dimensions;++v)if((s>>v)&1)--energy[v];
 }
}
vector<int> admissible(int v,uint32_t done){
 if(int(forced.size())+16-energy[v]>target)return {};
 const vector<int>* candidates=nullptr;
 uint32_t required_union=0;int required_loss=0;vector<int> required;
 for(int s:forced)if((s>>v)&1){required.push_back(s);required_loss+=5-weight(s);required_union|=s;auto& pool=inverted[relabel(s,v)];if(!candidates||pool.size()<candidates->size())candidates=&pool;}
 sort(required.begin(),required.end());
 auto key=make_tuple(v,done,required);
 if(cached_ids>5000000){compatibility_cache.clear();cached_ids=0;}
 auto hit=compatibility_cache.find(key);
 if(hit!=compatibility_cache.end()){
  vector<int> answer;for(int id:hit->second)if(loss+template_loss[id]-required_loss<=maxloss)answer.push_back(id);return answer;
 }
 uint32_t forbidden=done&~required_union;
 vector<int> everything;
 if(!candidates){everything.resize(catalog.size());iota(everything.begin(),everything.end(),0);candidates=&everything;}
 vector<int> ids,compatible;
 for(int id:*candidates){
  ++scans;if(nonhomogeneous_case&&!is_nonhom[id])continue;
  // A completed coordinate absent from every required v-mask cannot
  // occur anywhere in a compatible v-template: every such mask would
  // be new and would touch that completed coordinate. This is a fast
  // prefilter for the exact no-new-mask check below, not a new prune.
  if(uint32_t(relabel(template_union[id],v))&forbidden)continue;
  int matching=0,newcount=0,newloss=0;bool ok=true;
  for(int old:catalog[id]){
   int s=relabel(old,v);
   if(present[s])++matching;
   else{
    if(s&done){ok=false;break;}
    ++newcount;newloss+=5-weight(s);
   }
  }
  if(ok&&matching==energy[v]){
   compatible.push_back(id);
   if(loss+newloss<=maxloss)ids.push_back(id);
  }
 }
 cached_ids+=compatible.size();compatibility_cache.emplace(move(key),move(compatible));
 return ids;
}
Pattern at_vertex(int id,int v){Pattern p;for(int i=0;i<16;++i)p[i]=relabel(catalog[id][i],v);return p;}
bool independent_odd_obstruction(uint32_t done){
 int used=0;for(int s:forced){if(weight(s)%2==0)return false;used|=s;}
 return (used&~done)==0 && (int)forced.size()<target && forced.size()<256;
}
int rank_low(vector<uint32_t> rows){
 array<uint32_t,32> basis{};int answer=0;
 for(uint32_t row:rows)for(int bit=0;bit<32&&row;++bit)if(row&(1u<<bit)){
  if(basis[bit])row^=basis[bit];else{basis[bit]=row;++answer;break;}
 }
 return answer;
}
bool forced_flat_is_ternary(uint32_t done){
 // Separately written (same agent) sign-equation construction: label each local affine
 // four-flat by a chosen basis and impose its eleven non-affine entries.
 if(forced.size()!=32||target<=32||target>=64)return false;
 vector<int> sorted=forced;sort(sorted.begin(),sorted.end());
 vector<uint32_t> differences;for(int s:sorted)differences.push_back(s^sorted[0]);
 if(rank_low(differences)!=5)return false;
 vector<uint32_t> equations;
 for(int v=0;v<dimensions;++v)if(done&(1u<<v)){
  vector<int> local;for(int i=0;i<32;++i)if((sorted[i]>>v)&1)local.push_back(i);
  assert(local.size()==16);
  int origin=sorted[local[0]];vector<uint32_t> independent;
  for(int index:local){
   uint32_t delta=sorted[index]^origin;auto trial=independent;trial.push_back(delta);
   if(rank_low(trial)>(int)independent.size())independent.push_back(delta);
  }
  assert(independent.size()==4);
  array<int,16> labels{};
  for(int t=0;t<16;++t){
   int term=origin;for(int j=0;j<4;++j)if((t>>j)&1)term^=independent[j];
   auto found=lower_bound(sorted.begin(),sorted.end(),term);
   assert(found!=sorted.end()&&*found==term);labels[t]=found-sorted.begin();
  }
  for(int t=1;t<16;++t)if(weight(t)>=2){
   uint32_t relation=1u<<labels[t];
   if(weight(t)%2==0)relation^=1u<<labels[0];
   for(int j=0;j<4;++j)if((t>>j)&1)relation^=1u<<labels[1<<j];
   equations.push_back(relation);
  }
 }
 int rank=rank_low(equations);assert(rank<=26);return rank==26;
}
void finish(uint32_t done){
 ++closures;
 int remaining=target-forced.size();if(remaining<0||loss>maxloss)return;
 int next=-1;
 for(int v=0;v<dimensions;++v){
  if(energy[v]+remaining<16)return;
  if(done&(1<<v)){if(energy[v]!=16)return;continue;}
  if(energy[v]+remaining<24){
   if(energy[v]>16)return;
   // Pick the last forced-minimum coordinate, unlike the search order.
   next=v;
  }
 }
 if(next<0){
  if(forced_flat_is_ternary(done)){++flat_rejections;return;}
  if(independent_odd_obstruction(done)){++odd_rejections;return;}
  ++unresolved;return;
 }
 for(int id:admissible(next,done)){
  auto added=install(at_vertex(id,next));finish(done|(1<<next));undo(added);
 }
}
void complete(uint32_t done){
 ++visits;
 int remaining=target-forced.size();if(remaining<0||loss>maxloss)return;
 int unseen=0,deficit=0;
 for(int v=0;v<dimensions;++v){
  if(selected&(1<<v)){
   if(energy[v]>16)return;
   if(!energy[v])++unseen;
  }else deficit+=max(0,16-energy[v]);
 }
 if(deficit>weight((mask_count-1)^selected)*remaining)return;
 if((unseen>1&&remaining<24)||(unseen&&remaining<16))return;
 if(done==selected){finish(done);return;}
 int next=-1;size_t smallest=SIZE_MAX;
 for(int v=dimensions-1;v>=0;--v)if((selected&(1<<v))&&!(done&(1<<v))){
  size_t estimate=catalog.size();for(int s:forced)if((s>>v)&1)estimate=min(estimate,inverted[relabel(s,v)].size());
  if(estimate<smallest||(estimate==smallest&&(next<0||energy[v]>energy[next]))){smallest=estimate;next=v;}
 }
 assert(next>=0);
 for(int id:admissible(next,done)){
  auto added=install(at_vertex(id,next));complete(done|(1<<next));undo(added);
 }
}
struct Case{string name;vector<int> seed;uint32_t good;};
int main(int argc,char** argv){
 if(argc==4&&string(argv[1])=="--flat-control"){
  ifstream file(argv[2]);assert(file.good());uint32_t done;int count;
  file>>dimensions>>target>>done>>count;
  for(int i=0;i<count;++i){int term;file>>term;forced.push_back(term);}
  string extra;assert(!(file>>extra));bool actual=forced_flat_is_ternary(done);
  cout<<"A flat control "<<actual<<endl;return actual==bool(stoi(argv[3]))?0:2;
 }
 bool file_mode=argc==4&&string(argv[1])=="--case-file";
 assert(file_mode||argc==5||argc==6);
 string kind,output;int case_index=-1;Case file_case;
 if(file_mode){
  ifstream file(argv[2]);assert(file.good());int nh,count;uint32_t bits;
  file>>dimensions>>target>>bits>>nh>>count;assert(nh==0||nh==1);
  vector<int> bs;int used=1,cost=0;
  for(int i=0;i<count;++i){int b;file>>b;assert(b&&!(used&b));used|=b;cost+=max(1,weight(b)-1);bs.push_back(b);}
  string extra;assert(!(file>>extra));assert(cost==4&&used<(1<<dimensions));
  assert((bits&1)&&bits<(1u<<dimensions));kind=nh?"nonhom":"hom";output=argv[3];file_case={"file",bs,bits};
 }else{
  dimensions=stoi(argv[1]);kind=argv[2];case_index=stoi(argv[3]);output=argv[4];
  if(argc==6)target=stoi(argv[5]);
 }
 assert((dimensions>=14&&dimensions<=17&&target==56)||(dimensions==13&&target==48));
 mask_count=1<<dimensions;maxloss=5*target-16*dimensions;
 vector<Case> cases;
 nonhomogeneous_case=kind=="nonhom";
 if(!file_mode&&kind=="hom"){
  int required=(24*dimensions-5*target+7)/8;
  for(int a=0;a<3;++a)for(int b=a;b<3;++b)for(int c=b;c<3;++c)for(int d=c;d<3;++d){
   int outside=required-1-a-b-c-d;if(outside<0||outside>dimensions-9)continue;
   uint32_t good=1;vector<int> counts{a,b,c,d};
   for(int j=0;j<4;++j)for(int x=0;x<counts[j];++x)good|=1<<(2*j+1+x);
   for(int x=0;x<outside;++x)good|=1<<(x+9);
   cases.push_back({to_string(a)+to_string(b)+to_string(c)+to_string(d)+"_"+to_string(outside),{6,24,96,384},good});
  }
 }else if(!file_mode){
  assert(kind=="nonhom"&&dimensions==15&&target==56);
  for(int a=0;a<=4;++a)for(int b=0;b<=4;++b)for(int c=0;c<=2;++c)for(int d=0;d<=1;++d)for(int e=0;e<=1;++e){
   if(a+b+2*c+3*d+4*e!=4||b==4)continue;
   vector<int> blocks,orbits;int position=1;array<int,5> counts{a,b,c,d,e};
   for(int m=1;m<=5;++m){
    if(counts[m-1])orbits.push_back(position);
    for(int z=0;z<counts[m-1];++z){int block=0;for(int q=0;q<m;++q)block|=1<<position++;blocks.push_back(block);}
   }
   if(position<dimensions)orbits.push_back(position);
   for(int bad:orbits)cases.push_back({to_string(a)+to_string(b)+to_string(c)+to_string(d)+to_string(e)+"_bad"+to_string(bad),blocks,(uint32_t)((mask_count-1)^(1<<bad))});
  }
 }
 if(!file_mode)assert(case_index>=0&&case_index<(int)cases.size());
 Case c=file_mode?file_case:cases[case_index];selected=c.good;
 auto started=chrono::steady_clock::now();initialize();
 if(dimensions==13)assert(catalog.size()==359502);
 if(dimensions==15)assert(catalog.size()==1479478);
 auto added=install(product_spectrum(0,c.seed));complete(1);undo(added);
 ofstream file(output);
 file<<"{\"implementation\":\"A truth-spectrum incidence completion\",\"n\":"<<dimensions<<",\"norm\":"<<target<<",\"case_index\":"<<case_index<<",\"kind\":\""<<kind<<"\",\"case\":\""<<c.name<<"\",\"goodbits\":"<<selected<<",\"templates\":"<<catalog.size()<<",\"nodes\":"<<visits<<",\"closure_nodes\":"<<closures<<",\"domain_tests\":"<<scans<<",\"unresolved\":"<<unresolved<<",\"odd_residual_rejections\":"<<odd_rejections<<",\"flat_residual_rejections\":"<<flat_rejections<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-started).count()<<"}\n";
 cout<<"A "<<dimensions<<" "<<kind<<" "<<case_index<<" nodes "<<visits<<" unresolved "<<unresolved<<endl;
 return unresolved?2:0;
}

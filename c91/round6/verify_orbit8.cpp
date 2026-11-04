// Separately written (same agent) exact checker; inherited arithmetic/base code.
// Round-5 normalized frontier is in gap_tracker8.inc; no search import.
// The frontier update enumerates eligible short edit paths by source position.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <sstream>
#include <omp.h>
using namespace std;
// Unsigned base-2^32 integers. 2560 bits cover every allowed 64-bit parameter.
struct Z{
 array<uint32_t,80>a{};int n=0;
 Z(uint64_t x=0){if(x){a[0]=uint32_t(x);a[1]=uint32_t(x>>32);n=a[1]?2:1;}}
 void trim(){while(n&&a[n-1]==0)n--;}
 Z& operator*=(uint64_t x){__uint128_t carry=0;for(int i=0;i<n;i++){__uint128_t z=__uint128_t(a[i])*x+carry;a[i]=uint32_t(z);carry=z>>32;}while(carry){if(n==80)throw runtime_error("integer capacity");a[n++]=uint32_t(carry);carry>>=32;}trim();return *this;}
 Z& operator+=(const Z&b){int end=max(n,b.n);uint64_t carry=0;for(int i=0;i<end;i++){uint64_t z=uint64_t(a[i])+b.a[i]+carry;a[i]=uint32_t(z);carry=z>>32;}n=end;if(carry){if(n==80)throw runtime_error("integer capacity");a[n++]=carry;}return *this;}
 friend bool operator<(const Z&a,const Z&b){if(a.n!=b.n)return a.n<b.n;for(int i=a.n-1;i>=0;i--)if(a.a[i]!=b.a[i])return a.a[i]<b.a[i];return false;}
 friend bool operator>(const Z&a,const Z&b){return b<a;}
 friend Z operator*(Z a,uint64_t b){a*=b;return a;}
 friend Z operator-(Z a,const Z&b){if(a<b)throw runtime_error("negative unsigned subtraction");uint64_t borrow=0;for(int i=0;i<a.n;i++){uint64_t sub=uint64_t(b.a[i])+borrow,old=a.a[i];a.a[i]=uint32_t(old-sub);borrow=old<sub;}if(borrow)throw runtime_error("subtraction borrow");a.trim();return a;}
 friend ostream& operator<<(ostream&o,Z z){if(!z.n)return o<<0;vector<uint32_t>parts;while(z.n){uint64_t rem=0;for(int i=z.n-1;i>=0;i--){uint64_t t=(rem<<32)|z.a[i];z.a[i]=t/1000000000;rem=t%1000000000;}z.trim();parts.push_back(rem);}o<<parts.back();for(int i=int(parts.size())-2;i>=0;i--){string t=to_string(parts[i]);o<<string(9-t.size(),'0')<<t;}return o;}
};
void need(bool b,const string&s){if(!b)throw runtime_error(s);}
uint32_t get32(istream&f){uint32_t x=0;for(int k=0;k<4;k++){int c=f.get();need(c>=0,"short input");x|=uint32_t(c)<<(8*k);}return x;}
uint64_t get64(istream&f){uint64_t x=0;for(int k=0;k<8;k++){int c=f.get();need(c>=0,"short input");x|=uint64_t(c)<<(8*k);}return x;}
const int xb[8]={0,1,0,1,0,1,-1,-1},yb[8]={0,1,1,0,-1,-1,0,1};
uint64_t suffix_mask(int n){return n?((uint64_t(1)<<(3*n))-1):0;}
struct Word{uint64_t bits;uint32_t length;bool operator==(const Word&o)const{return bits==o.bits&&length==o.length;}};
struct WordHash{size_t operator()(Word p)const{return p.bits*0xbf58476d1ce4e5b9ULL+p.length*0x94d049bb133111ebULL;}};
// Whole forward canonical keys, rather than the search's backwards scalar DP.
struct CanonKey{int cost=999,gaps=999;string ops;};
bool lesskey(const CanonKey&a,const CanonKey&b){return tie(a.cost,a.gaps,a.ops)<tie(b.cost,b.gaps,b.ops);}
bool iscanonical(Word w){
 vector<int>a,b,columns(w.length);for(int k=int(w.length)-1;k>=0;k--){columns[k]=w.bits&7;w.bits>>=3;}
 CanonKey actual{0,0,""};for(int c:columns){if(xb[c]>=0)a.push_back(xb[c]);if(yb[c]>=0)b.push_back(yb[c]);actual.cost+=c>=2;actual.gaps+=c>=4;actual.ops.push_back(c<4?'0':c<6?'1':'2');}
 int n=a.size(),m=b.size();vector<CanonKey>dp((n+1)*(m+1));dp[0]={0,0,""};
 auto offer=[&](int at,const CanonKey&from,int cost,int gap,char op){CanonKey t=from;t.cost+=cost;t.gaps+=gap;t.ops.push_back(op);if(lesskey(t,dp[at]))dp[at]=move(t);};
 for(int i=0;i<=n;i++)for(int j=0;j<=m;j++){const auto from=dp[i*(m+1)+j];if(i<n&&j<m)offer((i+1)*(m+1)+j+1,from,a[i]!=b[j],0,'0');if(i<n)offer((i+1)*(m+1)+j,from,1,1,'1');if(j<m)offer(i*(m+1)+j+1,from,1,1,'2');}
 const auto&best=dp.back();return tie(actual.cost,actual.gaps,actual.ops)==tie(best.cost,best.gaps,best.ops);
}
// Literal run memory; its private encoding differs from the search encoding.
struct Run{int last=8,mask=0,ban=-1,after=0;};
uint16_t tag(Run r){return r.last|(r.mask<<4)|((r.ban+1)<<6)|(r.after<<8);}
Run untag(uint16_t k){return {k&15,(k>>4)&3,((k>>6)&3)-1,(k>>8)&3};}
int runedge(uint16_t k,int c){Run r=untag(k);int prev=r.last==4?1:r.last==6?2:0;
 if(c<4){if(prev&&(c>=2||(r.mask&(1<<xb[c]))))return -1;return tag({c,0,-1,prev});}
 int dir=c<6?1:2,bit=dir==1?xb[c]:yb[c],mask=1<<bit,ban=-1;
 if(prev){if(prev!=dir)return -1;mask|=r.mask;ban=r.ban;}
 else {if(r.after&&r.after!=dir)return -1;if(r.last==2||r.last==3)ban=dir==1?yb[r.last]:xb[r.last];}
 if(bit==ban)return -1;return tag({dir==1?4:6,mask,ban,0});
}
struct BaseNode{uint16_t run;array<int32_t,8>out;};
struct BaseKey{uint32_t prefix;uint16_t run;bool operator==(const BaseKey&o)const{return prefix==o.prefix&&run==o.run;}};
struct BaseHash{size_t operator()(BaseKey k)const{return uint64_t(k.prefix)*65537+k.run;}};
vector<BaseNode> base_graph(const vector<Word>&bad,uint32_t expected){
 unordered_set<Word,WordHash>forbidden;forbidden.reserve(bad.size()*2);unordered_map<Word,uint32_t,WordHash>prefix;prefix.reserve(bad.size()*2);vector<Word>prefixes={{0,0}};prefix[prefixes[0]]=0;int maxlen=0;
 for(Word p:bad){need(forbidden.insert(p).second,"duplicate forbidden word");maxlen=max(maxlen,int(p.length));while(p.length){p.bits>>=3;p.length--;auto q=prefix.emplace(p,prefixes.size());if(q.second)prefixes.push_back(p);}}
 vector<BaseKey>states={{0,tag(Run{})}};unordered_map<BaseKey,uint32_t,BaseHash>ids;ids[states[0]]=0;vector<BaseNode>result;
 for(size_t i=0;i<states.size();i++){
  const auto state=states[i];BaseNode node{state.run,{}};node.out.fill(-1);Word p=prefixes[state.prefix];
  for(int c=0;c<8;c++){int nr=runedge(state.run,c);if(nr<0)continue;Word t{(p.bits<<3)|uint64_t(c),p.length+1};bool reject=false;
   for(int l=min(int(t.length),maxlen);l>=1;l--)if(forbidden.count({t.bits&suffix_mask(l),uint32_t(l)})){reject=true;break;}
   if(reject)continue;uint32_t at=0;for(int l=min(int(t.length),maxlen-1);l>=0;l--){auto q=prefix.find({t.bits&suffix_mask(l),uint32_t(l)});if(q!=prefix.end()){at=q->second;break;}}
   BaseKey next{at,uint16_t(nr)};auto q=ids.emplace(next,states.size());if(q.second)states.push_back(next);node.out[c]=q.first->second;
  }
  result.push_back(node);need(states.size()<=expected,"too many base states");
 }
 need(result.size()==expected,"wrong base state count");cout<<"base_full "<<result.size()<<endl;return result;
}
// Sort signatures, then canonically renumber by first appearance in the BFS list.
template<size_t M>vector<uint32_t> sorted_colors(const vector<array<uint64_t,M>>&sig,uint32_t&count){
 vector<uint32_t>order(sig.size()),group(sig.size());iota(order.begin(),order.end(),0);sort(order.begin(),order.end(),[&](uint32_t a,uint32_t b){return sig[a]<sig[b];});
 uint32_t c=0;for(size_t i=0;i<order.size();i++){if(i&&sig[order[i]]!=sig[order[i-1]])c++;group[order[i]]=c;}
 vector<uint32_t>renumber(c+1,UINT32_MAX);count=0;for(auto &g:group){if(renumber[g]==UINT32_MAX)renumber[g]=count++;g=renumber[g];}return group;
}
vector<BaseNode> minimize_base(const vector<BaseNode>&a,uint32_t expected){
 vector<uint32_t>g(a.size(),0);uint32_t count=1;
 for(int iteration=0;iteration<100;iteration++){
  vector<array<uint64_t,9>>signature(a.size());for(size_t i=0;i<a.size();i++){signature[i][0]=a[i].run;for(int c=0;c<8;c++)signature[i][c+1]=a[i].out[c]<0?0:g[a[i].out[c]]+1;}
  uint32_t nc;auto next=sorted_colors(signature,nc);g.swap(next);cout<<"base_refine "<<iteration<<" "<<nc<<endl;if(nc==count){count=nc;break;}count=nc;need(iteration<99,"base refinement failed");
 }
 need(count==expected,"wrong minimal base count");vector<BaseNode>result(count);vector<bool>seen(count,false);for(size_t i=0;i<a.size();i++)if(!seen[g[i]]){seen[g[i]]=true;result[g[i]]=a[i];for(int32_t &v:result[g[i]].out)if(v>=0)v=g[v];}return result;
}
struct State{uint32_t base;uint8_t nx=0,ny=0,x=0,y=0,run=0;array<int16_t,12>score{};bool operator==(const State&o)const{return base==o.base&&nx==o.nx&&ny==o.ny&&x==o.x&&y==o.y&&run==o.run&&score==o.score;}};
struct StateHash{size_t operator()(const State&s)const{uint64_t h=s.base+0x243f6a8885a308d3ULL;for(int v:{int(s.nx),int(s.ny),int(s.x),int(s.y),int(s.run)})h=(h^(v+1))*0x100000001b3ULL;for(int v:s.score)h=(h^(v+128))*0x100000001b3ULL;return h;}};
struct Row{array<int32_t,8>to;array<array<int8_t,8>,8>feature;};
int parity(unsigned x){int p=0;for(;x;x>>=1)p^=x&1;return p;}
struct Candidate{
 int cost=1000000,gaps=1000000,order=1;
 bool operator<(const Candidate&o)const{return tie(cost,gaps,order)<tie(o.cost,o.gaps,o.order);}
};
#include "base_complement.inc"
#include "orbit_tracker8.inc"
vector<BaseNode> run_graph(){
 vector<uint16_t>states={tag(Run{})};unordered_map<uint16_t,uint32_t>ids;ids[states[0]]=0;vector<BaseNode>result;
 for(size_t i=0;i<states.size();i++){
  BaseNode row{states[i],{}};row.out.fill(-1);
  for(int c=0;c<8;c++){int next=runedge(states[i],c);if(next<0)continue;auto p=ids.emplace(uint16_t(next),states.size());if(p.second)states.push_back(next);row.out[c]=p.first->second;}
  result.push_back(row);need(states.size()<1000,"run graph unexpectedly large");
 }
 cout<<"run_memory_states "<<result.size()<<endl;return result;
}
vector<Row> labeled_minimum(const vector<Row>&a,uint32_t expected){
 vector<uint32_t>color(a.size(),0);uint32_t count=1;
 for(int iteration=0;iteration<150;iteration++){
  vector<array<uint64_t,8>>signature(a.size());
  for(size_t i=0;i<a.size();i++)for(int column=0;column<8;column++)if(a[i].to[column]>=0){
   uint64_t label=column<2?0:column<4?1:2;
   for(int j=0;j<8;j++)label=5*label+a[i].feature[column][j]+2;
   signature[i][column]=(label<<32)|(uint64_t(color[a[i].to[column]])+1);
  }
  uint32_t next_count;auto next=sorted_colors(signature,next_count);color.swap(next);
  cout<<"labeled_refine "<<iteration<<" "<<next_count<<endl;
  if(next_count==count){count=next_count;break;}count=next_count;need(iteration<149,"labeled refinement failed");
 }
 need(count==expected,"wrong labeled class count");
 vector<Row>result(count);vector<uint32_t>representative(count,UINT32_MAX);
 for(size_t i=0;i<a.size();i++)if(representative[color[i]]==UINT32_MAX){representative[color[i]]=i;result[color[i]]=a[i];for(int &d:result[color[i]].to)if(d>=0)d=color[d];}
 for(size_t i=0;i<a.size();i++)for(int c=0;c<8;c++){
  const auto&r=result[color[i]];need((a[i].to[c]<0)==(r.to[c]<0),"labeled missing edge mismatch");
  if(a[i].to[c]>=0)need(color[a[i].to[c]]==uint32_t(r.to[c])&&a[i].feature[c]==r.feature[c],"labeled member mismatch");
 }
 cout<<"labeled_minimum "<<a.size()<<" "<<count<<endl;return result;
}
vector<Row> intersect_graph(const vector<BaseNode>&base,const vector<Row>&tracker,uint32_t expected){
 vector<pair<uint32_t,uint32_t>>states={{0,0}};unordered_map<uint64_t,uint32_t>ids;ids[0]=0;vector<Row>result;result.reserve(expected);
 for(size_t index=0;index<states.size();index++){
  auto [a,b]=states[index];Row row{};row.to.fill(-1);row.feature=tracker[b].feature;
  for(int column=0;column<8;column++)if(base[a].out[column]>=0&&tracker[b].to[column]>=0){
   uint32_t na=base[a].out[column],nb=tracker[b].to[column];uint64_t key=(uint64_t(na)<<32)|nb;
   auto position=ids.emplace(key,states.size());if(position.second)states.push_back({na,nb});row.to[column]=position.first->second;
   need(states.size()<=expected,"too many intersection states");
  }
  result.push_back(row);if(index%1000000==0)cout<<"intersection_rows "<<index<<" reachable "<<states.size()<<endl;
 }
 need(result.size()==expected,"wrong intersection count");cout<<"intersection_full "<<result.size()<<endl;return result;
}
vector<uint32_t> weighted_colors(const vector<Row>&rows,uint32_t expected){
 vector<uint32_t>g(rows.size(),0);uint32_t count=1;
 for(int it=0;it<100;it++){
  vector<array<uint64_t,8>>sig(rows.size());for(size_t i=0;i<rows.size();i++){
   for(int c=0;c<8;c++)if(rows[i].to[c]>=0){uint64_t label=c<2?0:c<4?1:2;for(int j=0;j<8;j++)label=5*label+rows[i].feature[c][j]+2;sig[i][c]=(label<<32)|(uint64_t(g[rows[i].to[c]])+1);}sort(sig[i].begin(),sig[i].end());
  }
  uint32_t nc;auto next=sorted_colors(sig,nc);g.swap(next);cout<<"weighted_refine "<<it<<" "<<nc<<endl;if(nc==count){count=nc;break;}count=nc;need(it<99,"weighted refinement failed");
 }
 need(count==expected,"wrong weighted class count");return g;
}


// Compact exact potential reconstruction. No numerical graph is an input.
int edge_kind(const Row&r,int c){
 int value=c<2?0:c<4?1:2;
 for(int j=0;j<8;j++){need(r.feature[c][j]>=-2&&r.feature[c][j]<=2,"feature range");value=5*value+r.feature[c][j]+2;}
 return value;
}
uint64_t upper_coefficient(int index,int precision,const vector<Z>&coefficient,
                          const Z&denominator,vector<uint64_t>&cache){
 if(cache[index]!=UINT64_MAX)return cache[index];
 Z numerator=coefficient[index];numerator*=uint64_t(1)<<precision;
 need(numerator.n>0&&denominator.n>0,"nonpositive coefficient");
 uint64_t low=1,high=(uint64_t(1)<<48)-1;
 need(!(denominator*high<numerator),"dyadic coefficient range");
 while(low<high){uint64_t middle=low+(high-low)/2;
  if(denominator*middle<numerator)low=middle+1;else high=middle;
 }
 // The least integer u with D*u>=2^precision*c is the exact ceiling.
 cache[index]=low;return low;
}
vector<uint64_t> reconstruct_power(const vector<Row>&rows,const vector<uint32_t>&group,
 uint32_t classes,uint32_t precision,uint32_t steps,uint64_t initial,
 const vector<Z>&coefficient,const Z&denominator,vector<uint64_t>&cache){
 struct IntegerRow{array<int32_t,8>destination;array<uint64_t,8>weight;};
 vector<IntegerRow>quotient(classes);vector<bool>present(classes,false);
 for(size_t i=0;i<rows.size();++i){auto g=group[i];if(present[g])continue;present[g]=true;
  for(int c=0;c<8;c++){int target=rows[i].to[c];quotient[g].destination[c]=target<0?-1:int32_t(group[target]);
   quotient[g].weight[c]=target<0?0:upper_coefficient(edge_kind(rows[i],c),precision,coefficient,denominator,cache);
  }
 }
 need(all_of(present.begin(),present.end(),[](bool b){return b;}),"unrepresented potential class");
 vector<uint64_t>current(classes,initial),following(classes);
 for(uint32_t round=0;round<steps;++round){int invalid=0;
  #pragma omp parallel for num_threads(12) reduction(|:invalid) schedule(static)
  for(uint32_t g=0;g<classes;++g){__uint128_t sum=__uint128_t(current[g])<<precision;const auto&r=quotient[g];
   for(int c=0;c<8;c++)if(r.destination[c]>=0)sum+=__uint128_t(r.weight[c])*current[r.destination[c]];
   // Nine terms (including the identity) sum to less than 2^116.
   __uint128_t value=sum>>(precision+1);if(value>=UINT64_MAX)invalid=1;
   following[g]=uint64_t(value)+1;
  }
  need(!invalid,"integer power overflow");current.swap(following);
  if((round+1)%32==0)cout<<"exact_potential_iteration "<<round+1<<endl;
 }
 uint64_t fingerprint=1469598103934665603ULL;for(uint64_t value:current){need(value>0,"zero reconstructed potential");fingerprint=(fingerprint^value)*1099511628211ULL;}
 cout<<"EXACT_POTENTIAL_RECONSTRUCTED steps="<<steps<<" minimum="<<*min_element(current.begin(),current.end())<<" maximum="<<*max_element(current.begin(),current.end())<<" fnv64="<<fingerprint<<endl;
 return current;
}

int main(int argc,char**argv){try{
 cout<<"VERIFY_CHECKPOINT cpp START"<<endl;
 need(argc==2,"usage: verifier binary-input");auto start=chrono::steady_clock::now();ifstream in(argv[1],ios::binary);string magic(8,' ');in.read(magic.data(),8);bool power_encoded=magic==string("C91PO008");need(power_encoded||magic==string("C91OR008"),"wrong input version");
 uint32_t L=get32(in),W=get32(in),B=get32(in),K=get32(in),norig=get32(in),nbase=get32(in),nfull=get32(in),nclass=get32(in),S=get32(in),T=get32(in),completion=get32(in),npat=get32(in);need(L>=2&&L<=21&&W>=1&&W<=6&&B<=10&&K==8,"invalid schema parameters");need(S<=3&&T>=1&&T<=3&&completion<=2,"invalid gap record");need(nfull<=250000000,"state cap");
 vector<int>lagcaps;if(completion==2){for(uint32_t lag=1;lag<=W;++lag){int value=int32_t(get32(in));need(value>=-int(lag)&&value<=10,"invalid per-lag cap");lagcaps.push_back(value);}}
 array<pair<uint64_t,uint64_t>,10>param;for(auto &p:param){p.first=get64(in);p.second=get64(in);need(p.first&&p.second,"zero parameter");}
 vector<Word>bad(npat);for(auto &p:bad){p.length=get32(in);p.bits=get64(in);need(p.length>=1&&p.length<=L&&(p.bits&suffix_mask(p.length))==p.bits,"malformed word");}
 uint32_t precision=0,steps=0;uint64_t initial=0;vector<uint64_t>v;
 if(power_encoded){precision=get32(in);steps=get32(in);initial=get64(in);need(precision>=16&&precision<=48&&steps<=4096&&initial>0&&initial<=(uint64_t(1)<<60),"invalid integer power recipe");}
 else{v.resize(nclass);for(auto&x:v){x=get64(in);need(x>0,"nonpositive vector");}}
 need(in.peek()==EOF,"extra data");
 for(size_t j=0;j<bad.size();j++){need(!iscanonical(bad[j]),"listed word is canonical");if(j%200000==0)cout<<"forbidden_checked "<<j<<endl;}
 cout<<"VERIFY_CHECKPOINT canonical word PASS"<<endl;
 // All one-column words are canonical. After exact bank checks above,
 // the complete root row has all labels and zero feature increments.
 {
  if(!power_encoded||steps==0){
  uint64_t rp=param[0].first,rq=param[0].second,rr=param[1].first,rs=param[1].second;
  Z rd=4;rd*=rq;rd*=rq;rd*=rs;
  Z lower=2;lower*=rp;lower*=rp;lower*=rs;
  Z substitutions=2;substitutions*=rp;substitutions*=rp;substitutions*=rr;lower+=substitutions;
  Z gaps=8;gaps*=rp;gaps*=rq;gaps*=rr;lower+=gaps;
  lower*=power_encoded?initial:*min_element(v.begin(),v.end());
  need(rd*(power_encoded?initial:v[0])>lower,"exact row inequality failed at 0 (positive-minimum lower bound)");
  cout<<"ROOT_NECESSARY_EXACT_PASS"<<endl;
  }
 }
 auto fullbase=base_graph(bad,norig);auto base=minimize_base(fullbase,nbase);fullbase.clear();fullbase.shrink_to_fit();bad.clear();bad.shrink_to_fit();auto rows=gap_record_graph(base,W,B,S,T,completion==1,nfull,lagcaps);base.clear();base.shrink_to_fit();auto group=weighted_colors(rows,nclass);
 uint64_t p=param[0].first,q=param[0].second,r=param[1].first,s=param[1].second;Z D=4;D*=q;D*=q;D*=s;for(int j=0;j<8;j++)for(int k=0;k<2;k++){D*=param[j+2].first;D*=param[j+2].second;}
 vector<Z>coefficient(1171875);for(int kind=0;kind<3;kind++)for(int f=0;f<390625;f++){int z=f;Z a=kind==2?2:1;a*=p;a*=kind==2?q:p;a*=kind==0?s:r;for(int j=7;j>=0;j--){int h=z%5-2;z/=5;for(int k=0;k<2+h;k++)a*=param[j+2].first;for(int k=0;k<2-h;k++)a*=param[j+2].second;}coefficient[kind*390625+f]=a;}
 if(power_encoded){
  vector<uint64_t>rounded(coefficient.size(),UINT64_MAX);
  v=reconstruct_power(rows,group,nclass,precision,steps,initial,coefficient,D,rounded);
  __uint128_t min_slack=~__uint128_t(0);uint64_t edges=0;
  for(size_t i=0;i<rows.size();++i){__uint128_t sum=0;
   for(int c=0;c<8;c++)if(rows[i].to[c]>=0){auto weight=upper_coefficient(edge_kind(rows[i],c),precision,coefficient,D,rounded);sum+=__uint128_t(weight)*v[group[rows[i].to[c]]];++edges;}
   __uint128_t limit=__uint128_t(v[group[i]])<<precision;need(sum<limit,"exact row inequality failed at "+to_string(i));min_slack=min(min_slack,limit-sum);
   if(i%1000000==0)cout<<"exact_rows "<<i<<endl;
  }
  Z slack(uint64_t(min_slack>>64));for(int j=0;j<2;j++)slack*=uint64_t(1)<<32;slack+=Z(uint64_t(min_slack));
  cout<<"EXACT_PASS states="<<rows.size()<<" edges="<<edges<<" classes="<<nclass<<" min_slack="<<slack<<"\ndenominator="<<(uint64_t(1)<<precision)<<"\nseconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
  return 0;
 }
 Z minslack=0;uint64_t edges=0;for(size_t i=0;i<rows.size();i++){
  Z sum=0;for(int c=0;c<8;c++)if(rows[i].to[c]>=0){int f=0;for(int j=0;j<8;j++){need(rows[i].feature[c][j]>=-2&&rows[i].feature[c][j]<=2,"feature range");f=5*f+rows[i].feature[c][j]+2;}sum+=coefficient[(c<2?0:c<4?1:2)*390625+f]*v[group[rows[i].to[c]]];edges++;}
  Z lhs=D*v[group[i]];need(lhs>sum,"exact row inequality failed at "+to_string(i));Z slack=lhs-sum;if(i==0||slack<minslack)minslack=slack;if(i%1000000==0)cout<<"exact_rows "<<i<<endl;
 }
 cout<<"EXACT_PASS states="<<rows.size()<<" edges="<<edges<<" classes="<<nclass<<" min_slack="<<minslack<<"\ndenominator="<<D<<"\nseconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
 }catch(const exception&e){cerr<<"REJECT: "<<e.what()<<endl;return 1;}}

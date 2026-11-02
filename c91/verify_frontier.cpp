// Independently written certificate checker. Imports no search implementation.
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
using namespace std;
// Unsigned base-2^32 integers. 1536 bits cover every allowed 64-bit parameter.
struct Z{
 array<uint32_t,48>a{};int n=0;
 Z(uint64_t x=0){if(x){a[0]=uint32_t(x);a[1]=uint32_t(x>>32);n=a[1]?2:1;}}
 void trim(){while(n&&a[n-1]==0)n--;}
 Z& operator*=(uint64_t x){__uint128_t carry=0;for(int i=0;i<n;i++){__uint128_t z=__uint128_t(a[i])*x+carry;a[i]=uint32_t(z);carry=z>>32;}while(carry){if(n==48)throw runtime_error("integer capacity");a[n++]=uint32_t(carry);carry>>=32;}trim();return *this;}
 Z& operator+=(const Z&b){int end=max(n,b.n);uint64_t carry=0;for(int i=0;i<end;i++){uint64_t z=uint64_t(a[i])+b.a[i]+carry;a[i]=uint32_t(z);carry=z>>32;}n=end;if(carry){if(n==48)throw runtime_error("integer capacity");a[n++]=carry;}return *this;}
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
struct State{uint32_t base;uint8_t nx=0,ny=0,x=0,y=0,run=0;array<int8_t,12>score{};bool operator==(const State&o)const{return base==o.base&&nx==o.nx&&ny==o.ny&&x==o.x&&y==o.y&&run==o.run&&score==o.score;}};
struct StateHash{size_t operator()(const State&s)const{uint64_t h=s.base+0x243f6a8885a308d3ULL;for(int v:{int(s.nx),int(s.ny),int(s.x),int(s.y),int(s.run)})h=(h^(v+1))*0x100000001b3ULL;for(int v:s.score)h=(h^(v+128))*0x100000001b3ULL;return h;}};
struct Row{array<int32_t,8>to;array<array<int8_t,4>,8>feature;};
int parity(unsigned x){int p=0;for(;x;x>>=1)p^=x&1;return p;}
vector<Row> product_graph(const vector<BaseNode>&base,int W,int B,uint32_t expected){
 const int missing=1000000,H=max(4,W);State initial{};initial.base=0;vector<State>states={initial};unordered_map<State,uint32_t,StateHash>ids;ids.reserve(min<uint32_t>(expected,20000000));ids[initial]=0;vector<Row>rows;rows.reserve(expected);
 for(size_t it=0;it<states.size();it++){
  State s=states[it];Run memory=untag(base[s.base].run);array<array<int,7>,2>old;
  for(auto &a:old)a.fill(missing);for(int r=1;r<=W;r++)for(int side=0;side<2;side++)if(s.score[2*r-2+side])old[side][r]=s.score[2*r-2+side]-W;
  Row row{};row.to.fill(-1);
  for(int c=0;c<8;c++)if(base[s.base].out[c]>=0){
   array<array<int,7>,2>fresh;for(auto &a:fresh)a.fill(missing);int edit=c>=2;
   if(c<4){
    // Enumerate one-diagonal edit paths from every eligible source boundary.
    unsigned extended[2]={(unsigned(s.x)<<1)|unsigned(xb[c]),(unsigned(s.y)<<1)|unsigned(yb[c])};
    for(int side=0;side<2;side++)for(int r=0;r<=W;r++)for(int q=r;q<=W;q++){
     int newbit=side==0?yb[c]:xb[c];
     if(old[side][q]!=missing)for(int before=0;before<=q-r;before++){
      int bit=(extended[side]>>(q-before))&1;
      fresh[side][r]=min(fresh[side][r],old[side][q]+q-r+(newbit!=bit)-edit);
     }
     if(q>=1&&q<=s.run&&((side==0&&memory.last==4)||(side==1&&memory.last==6))){int bit=(extended[side]>>q)&1;fresh[side][r]=min(fresh[side][r],-r+(newbit!=bit)-edit);}
    }
    fresh[0][0]=fresh[1][0]=min(fresh[0][0],fresh[1][0]);
   }else{
    int same=c<6?0:1,other=1-same;unsigned buffer=same==0?s.y:s.x;int bit=same==0?xb[c]:yb[c];
    for(int r=1;r<=W;r++)if(old[same][r-1]!=missing)fresh[same][r]=old[same][r-1]-1;
    // Alternative gap first, or diagonal first, then residual opposite gaps.
    for(int r=0;r<=W;r++)for(int q=r;q<=W;q++)if(old[other][q]!=missing){
     fresh[other][r]=min(fresh[other][r],old[other][q]+q-r);
     if(q>r)fresh[other][r]=min(fresh[other][r],old[other][q]+q-r-2+(bit!=int((buffer>>(q-1))&1)));
    }
    fresh[same][0]=fresh[other][0];
   }
   bool reject=false;for(int side=0;side<2;side++)for(int r=0;r<=W;r++)if(fresh[side][r]+r<=0)reject=true;if(reject)continue;
   State t=s;t.base=base[s.base].out[c];t.score.fill(0);
   for(int side=0;side<2;side++)for(int r=1;r<=W;r++)if(fresh[side][r]<=B){need(fresh[side][r]>-W,"invalid score range");t.score[2*r-2+side]=fresh[side][r]+W;}
   int dir=c<4?0:c<6?1:2,previous=memory.last==4?1:memory.last==6?2:0;t.run=dir?min(W,previous==dir?int(s.run)+1:1):0;
   for(int side=0;side<2;side++){
    int bit=side?yb[c]:xb[c],n=side?s.ny:s.nx;unsigned h=side?s.y:s.x;if(bit<0)continue;
    for(int lag=1;lag<=3;lag++)if(n>=lag)row.feature[c][lag-1]+=(((h>>(lag-1))&1)==unsigned(bit)?1:-1);
    if(n>=3)row.feature[c][3]+=parity(((h&7)<<1)|unsigned(bit))?-1:1;
    uint8_t nn=min(H,n+1),hh=((h<<1)|unsigned(bit))&((1<<H)-1);if(side){t.ny=nn;t.y=hh;}else{t.nx=nn;t.x=hh;}
   }
   auto q=ids.emplace(t,states.size());if(q.second)states.push_back(t);row.to[c]=q.first->second;need(states.size()<=expected,"too many frontier states");
  }
  rows.push_back(row);if(it%1000000==0)cout<<"frontier_rows "<<it<<" reachable "<<states.size()<<endl;
 }
 need(rows.size()==expected,"wrong frontier state count");cout<<"frontier_full "<<rows.size()<<endl;return rows;
}
vector<uint32_t> weighted_colors(const vector<Row>&rows,uint32_t expected){
 vector<uint32_t>g(rows.size(),0);uint32_t count=1;
 for(int it=0;it<100;it++){
  vector<array<uint64_t,8>>sig(rows.size());for(size_t i=0;i<rows.size();i++){
   for(int c=0;c<8;c++)if(rows[i].to[c]>=0){uint64_t label=c<2?0:c<4?1:2;for(int j=0;j<4;j++)label=5*label+rows[i].feature[c][j]+2;sig[i][c]=(label<<32)|(uint64_t(g[rows[i].to[c]])+1);}sort(sig[i].begin(),sig[i].end());
  }
  uint32_t nc;auto next=sorted_colors(sig,nc);g.swap(next);cout<<"weighted_refine "<<it<<" "<<nc<<endl;if(nc==count){count=nc;break;}count=nc;need(it<99,"weighted refinement failed");
 }
 need(count==expected,"wrong weighted class count");return g;
}

int main(int argc,char**argv){try{
 need(argc==2,"usage: verifier binary-input");auto start=chrono::steady_clock::now();ifstream in(argv[1],ios::binary);string magic(8,' ');in.read(magic.data(),8);need(magic==string("C91FR001"),"wrong input version");
 uint32_t L=get32(in),W=get32(in),B=get32(in),K=get32(in),norig=get32(in),nbase=get32(in),nfull=get32(in),nclass=get32(in),npat=get32(in);need(L>=2&&L<=21&&W>=1&&W<=6&&B<=10&&K==4,"invalid schema parameters");
 array<pair<uint64_t,uint64_t>,6>param;for(auto &p:param){p.first=get64(in);p.second=get64(in);need(p.first&&p.second,"zero parameter");}
 vector<Word>bad(npat);for(auto &p:bad){p.length=get32(in);p.bits=get64(in);need(p.length>=1&&p.length<=L&&(p.bits&suffix_mask(p.length))==p.bits,"malformed word");}
 vector<uint64_t>v(nclass);for(auto &x:v){x=get64(in);need(x>0,"nonpositive vector");}need(in.peek()==EOF,"extra data");
 for(size_t j=0;j<bad.size();j++){need(!iscanonical(bad[j]),"listed word is canonical");if(j%200000==0)cout<<"forbidden_checked "<<j<<endl;}
 auto fullbase=base_graph(bad,norig);auto base=minimize_base(fullbase,nbase);fullbase.clear();fullbase.shrink_to_fit();bad.clear();bad.shrink_to_fit();auto rows=product_graph(base,W,B,nfull);base.clear();base.shrink_to_fit();auto group=weighted_colors(rows,nclass);
 uint64_t p=param[0].first,q=param[0].second,r=param[1].first,s=param[1].second;Z D=4;D*=q;D*=q;D*=s;for(int j=0;j<4;j++)for(int k=0;k<2;k++){D*=param[j+2].first;D*=param[j+2].second;}
 vector<Z>coefficient(1875);for(int kind=0;kind<3;kind++)for(int f=0;f<625;f++){int z=f;Z a=kind==2?2:1;a*=p;a*=kind==2?q:p;a*=kind==0?s:r;for(int j=3;j>=0;j--){int h=z%5-2;z/=5;for(int k=0;k<2+h;k++)a*=param[j+2].first;for(int k=0;k<2-h;k++)a*=param[j+2].second;}coefficient[kind*625+f]=a;}
 Z minslack=0;uint64_t edges=0;for(size_t i=0;i<rows.size();i++){
  Z sum=0;for(int c=0;c<8;c++)if(rows[i].to[c]>=0){int f=0;for(int j=0;j<4;j++){need(rows[i].feature[c][j]>=-2&&rows[i].feature[c][j]<=2,"feature range");f=5*f+rows[i].feature[c][j]+2;}sum+=coefficient[(c<2?0:c<4?1:2)*625+f]*v[group[rows[i].to[c]]];edges++;}
  Z lhs=D*v[group[i]];need(lhs>sum,"exact row inequality failed at "+to_string(i));Z slack=lhs-sum;if(i==0||slack<minslack)minslack=slack;if(i%1000000==0)cout<<"exact_rows "<<i<<endl;
 }
 cout<<"EXACT_PASS states="<<rows.size()<<" edges="<<edges<<" classes="<<nclass<<" min_slack="<<minslack<<"\ndenominator="<<D<<"\nseconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
 }catch(const exception&e){cerr<<"REJECT: "<<e.what()<<endl;return 1;}}

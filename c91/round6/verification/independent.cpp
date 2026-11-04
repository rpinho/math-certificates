// Independently extended from the permitted round-5 checker and round-6 PROOF.md.
// No producer implementation consulted. All arithmetic is exact; overflow is fatal.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>
#include <set>
#include <omp.h>
using namespace std;
void require(bool b,string s){if(!b)throw runtime_error(s);}
constexpr uint32_t NONE=UINT32_MAX;
int W,B,S,T; uint64_t edgecount;
struct Row {array<uint32_t,8> to; array<uint32_t,8> wt; Row(){to.fill(NONE);wt.fill(0);}};
struct Run {int kind,detail,aux; bool operator==(Run const&o)const{return tie(kind,detail,aux)==tie(o.kind,o.detail,o.aux);}};
vector<Run> runs{{0,4,0}}; vector<array<int,8>> rt;
int symbolX(int a){return a<4?(a==1||a==3):(a<6?a-4:-1);}
int symbolY(int a){return a<4?(a==1||a==2):(a>=6?a-6:-1);}
int op(int a){return a<4?0:(a<6?1:2);}
int cost(int a){return a<2?0:1;}
int runnext(int id,int col){Run s=runs[id],n; int d=op(col),x=symbolX(col),y=symbolY(col);
 if(d==0){
  if(s.kind && (col>=2 || (s.detail&(1<<x))))return -1;
  n={0,col,s.kind};
 }else{
  int bit=d==1?x:y;
  if(s.kind){if(s.kind!=d)return -1;n={d,s.detail|(1<<bit),s.aux};}
  else {if(s.aux && s.aux!=d)return -1;int forbid=-1;
   if(s.detail==2||s.detail==3)forbid=d==1?symbolY(s.detail):symbolX(s.detail);
   n={d,1<<bit,forbid};}
  if(n.aux>=0 && (n.detail&(1<<n.aux)))return -1;
 }
 auto it=find(runs.begin(),runs.end(),n);if(it!=runs.end())return it-runs.begin();runs.push_back(n);return runs.size()-1;
}
void initruns(){for(size_t i=0;i<runs.size();i++){array<int,8>a;for(int c=0;c<8;c++)a[c]=runnext(i,c);rt.push_back(a);}cout<<"run states "<<runs.size()<<endl;}
struct Hash64{size_t operator()(uint64_t a)const {a^=a>>30;a*=0xbf58476d1ce4e5b9ULL;a^=a>>27;a*=0x94d049bb133111ebULL;return a^(a>>31);}};
struct Sig{array<uint64_t,9>a;bool operator==(Sig const&o)const{return a==o.a;}};
struct HS{size_t operator()(Sig const&s)const{uint64_t h=0;for(auto v:s.a)h=Hash64{}(h^v);return h;}};
vector<uint32_t> refine(vector<Row> const&g, bool unordered,vector<uint32_t> const*extra=nullptr){
 vector<uint32_t> colors(g.size(),0),next(g.size());size_t prev=1;
 for(int pass=0;;pass++){
  unordered_map<Sig,uint32_t,HS> m;m.reserve(g.size());
  for(size_t i=0;i<g.size();i++){
   Sig s; s.a[8]=extra?(*extra)[i]:0;
   for(int c=0;c<8;c++)s.a[c]=g[i].to[c]==NONE?UINT64_MAX:(uint64_t(g[i].wt[c])<<32)|colors[g[i].to[c]];
   if(unordered)sort(s.a.begin(),s.a.begin()+8);
   auto [it,ok]=m.emplace(s,m.size());next[i]=it->second;
  }
  size_t n=m.size();cout<<"refine "<<g.size()<<" pass "<<pass<<" classes "<<n<<endl;
  colors.swap(next);if(n==prev)return colors;require(n>prev,"nonrefining partition");prev=n;
 }
}
vector<Row> quotient(vector<Row>const&g,vector<uint32_t>const&c){
 auto n=1+*max_element(c.begin(),c.end());vector<Row> q(n);vector<bool> seen(n,false);
 for(size_t i=0;i<g.size();i++){Row r=g[i];for(auto &t:r.to)if(t!=NONE)t=c[t];
 if(seen[c[i]])require(q[c[i]].to==r.to&&q[c[i]].wt==r.wt,"quotient inconsistency");else{q[c[i]]=r;seen[c[i]]=true;}}
 return q;
}
// Trie/failure automaton; all forbidden words first proved noncanonical by DP.
struct Node{array<int,8>go;int fail=0;bool bad=false;Node(){go.fill(-1);}};
using Key=tuple<int,int,string>;
void wordcheck(vector<int>const&w){string x,y,ops;int cc=0,gg=0;for(int c:w){int a=symbolX(c),b=symbolY(c);if(a>=0)x+=char('0'+a);if(b>=0)y+=char('0'+b);cc+=cost(c);gg+=op(c)>0;ops+=char('0'+op(c));}
 vector<vector<Key>> dp(x.size()+1,vector<Key>(y.size()+1,{10000,10000,""}));dp[0][0]={0,0,""};
 for(size_t i=0;i<=x.size();i++)for(size_t j=0;j<=y.size();j++){
 auto put=[&](size_t a,size_t b,int co,int ga,char o){auto [c,g,s]=dp[i][j];dp[a][b]=min(dp[a][b],Key(c+co,g+ga,s+o));};
 if(i<x.size()&&j<y.size())put(i+1,j+1,x[i]!=y[j],0,'0');if(i<x.size())put(i+1,j,1,1,'1');if(j<y.size())put(i,j+1,1,1,'2');}
 require(dp.back().back()<Key(cc,gg,ops),"bank contains canonical word");
}
vector<uint32_t> base_run, flip_base;
vector<Row> base(istream&in,uint64_t expected,uint64_t minimized){
 size_t nw;in>>nw;vector<Node>tr(1);set<pair<int,uint64_t>> bank;
 for(size_t z=0;z<nw;z++){int len;uint64_t v;in>>len>>v;require(bank.emplace(len,v).second,"duplicate bank word");require(len>0&&len<=21,"bad length");vector<int>w(len);for(int j=len-1;j>=0;j--){w[j]=v%8;v/=8;}require(!v,"bad word");wordcheck(w);int s=0;for(int a:w){if(tr[s].go[a]<0){tr[s].go[a]=tr.size();tr.emplace_back();}s=tr[s].go[a];}tr[s].bad=true;}
 for(auto [len,v]:bank){uint64_t mask=0;for(int k=0;k<len;k++)mask=(mask<<3)|1;require(bank.count({len,v^mask}),"bank not complement closed");}
 vector<int> queue;for(int a=0;a<8;a++)if(tr[0].go[a]<0)tr[0].go[a]=0;else queue.push_back(tr[0].go[a]);
 for(size_t i=0;i<queue.size();i++){int s=queue[i];tr[s].bad=tr[s].bad||tr[tr[s].fail].bad;for(int a=0;a<8;a++){int d=tr[s].go[a];if(d<0)tr[s].go[a]=tr[tr[s].fail].go[a];else{tr[d].fail=tr[tr[s].fail].go[a];queue.push_back(d);}}}
 unordered_map<uint64_t,uint32_t,Hash64> ids;vector<pair<uint32_t,uint32_t>> st{{0,0}};vector<Row>g;vector<uint32_t>rmem;ids.emplace(0,0);
 for(size_t i=0;i<st.size();i++){auto [r,s]=st[i];Row row;rmem.push_back(r);for(int a=0;a<8;a++){int nr=rt[r][a],ns=tr[s].go[a];if(nr<0||tr[ns].bad)continue;uint64_t key=(uint64_t(nr)<<32)|ns;auto [it,ok]=ids.emplace(key,st.size());if(ok)st.emplace_back(nr,ns);row.to[a]=it->second;}g.push_back(row);}
 cout<<"base states "<<g.size()<<" bank "<<nw<<endl;require(g.size()==expected,"original base count");auto c=refine(g,false,&rmem);auto q=quotient(g,c);require(q.size()==minimized,"base quotient count");
 base_run.resize(q.size());for(size_t i=0;i<g.size();i++)base_run[c[i]]=rmem[i];
 flip_base.assign(q.size(),NONE);flip_base[0]=0;vector<uint32_t> todo{0};
 for(size_t i=0;i<todo.size();i++){uint32_t u=todo[i],v=flip_base[u];
  for(int a=0;a<8;a++){auto x=q[u].to[a],y=q[v].to[a^1];require((x==NONE)==(y==NONE),"complement missing edge");if(x==NONE)continue;
   if(flip_base[x]==NONE){flip_base[x]=y;todo.push_back(x);}else require(flip_base[x]==y,"complement inconsistent");}}
 require(todo.size()==q.size(),"unreachable matcher class");
 for(size_t i=0;i<q.size();i++){
  require(flip_base[flip_base[i]]==i,"matcher not involution");Run r=runs[base_run[i]],t=runs[base_run[flip_base[i]]];
  if(r.kind){r.detail=((r.detail&1)<<1)|((r.detail&2)>>1);if(r.aux>=0)r.aux^=1;}
  else if(r.detail<4)r.detail^=1;
  require(r==t,"literal run complement mismatch");
  for(int a=0;a<8;a++){auto x=q[i].to[a],y=q[flip_base[i]].to[a^1];require(x==NONE?y==NONE:flip_base[x]==y,"matcher conjugacy");}
 }
 cout<<"matcher complement involution checked "<<q.size()<<endl;return q;
}
struct Triple{int c,g,t;};constexpr int INF=1000;
struct State{array<uint16_t,6> f{};uint8_t hx=1,hy=1,run=0,length=0;bool operator==(State const&o)const{return f==o.f&&hx==o.hx&&hy==o.hy&&run==o.run&&length==o.length;}};
struct HState{size_t operator()(State const&s)const{uint64_t h=s.hx+32*s.hy+1024*s.run+32768*s.length;for(auto x:s.f)h=Hash64{}(h^x);return h;}};
int histlen(int h){int n=-1;while(h){n++;h>>=1;}return n;}
int append(int h,int b){return histlen(h)<4?2*h+b:16|((2*h+b)&15);}
Triple decode(int v,int r){v--;int t=(v&1)?1:-1;v>>=1;int g=v%(S+T+2);int c=v/(S+T+2)-W;return {c,g==S+T+1?INF:-r+2*(g-S),t};}
int encode(Triple v,int r){return 1+((v.c+W)*(S+T+2)+(v.g==INF?S+T+1:(v.g+r)/2+S))*2+(v.t==1);}
bool transition(State const&s,int col,State &n){
 int nr=rt[s.run][col];if(nr<0)return false;n=State{};n.run=nr;
 int a=symbolX(col),b=symbolY(col),o=op(col),e=cost(col);
 n.hx=a<0?s.hx:append(s.hx,a);n.hy=b<0?s.hy:append(s.hy,b);
 n.length=o?min(W,(runs[s.run].kind==o?s.length:0)+1):0;
 bool valid=true;
 auto put=[&](int side,int r,int c,int g,int t){if(!valid)return;
  if(c+r<0 || (c+r==0&&(g+r<0||(g+r==0&&t==-1)))){valid=false;return;}
  if(r==0||c>B)return;
  if(g==INF||g+r>2*T){g=INF;t=1;}else if(g<-r-2*S){g=-r-2*S;t=-1;}
  require(c>=-r && (g==INF||(g>=-r-2*S&&g<=-r+2*T&&(g+r)%2==0)),"frontier invariant");
 int ix=side*W+r-1;Triple v{c,g,t};int old=n.f[ix];
  if(!old||make_tuple(c,g,t)<make_tuple(decode(old,r).c,decode(old,r).g,decode(old,r).t))n.f[ix]=encode(v,r);
 };
 auto addg=[](int g,int d){return g==INF?INF:g+d;};
 for(int side=0;side<2;side++)for(int q=1;q<=W;q++)if(s.f[side*W+q-1]){
  auto v=decode(s.f[side*W+q-1],q);
  if(o==0){int h=side==0?n.hx:n.hy,bit=side==0?b:a;
   for(int r=0;r<=q;r++)for(int k=r;k<=q;k++)put(side,r,v.c+q-r+(((h>>k)&1)!=bit)-e,addg(v.g,q-r),v.t);
   put(1-side,1,v.c+q+1-e,addg(v.g,q+1),v.t);
   if(q<W)put(side,q+1,v.c+1-e,addg(v.g,1),v.t);
  }else if(side==o-1){for(int r=0;r<=min(W,q+1);r++)put(side,r,v.c+q-r,addg(v.g,q-r),v.t);}
  else {int h=side==0?s.hx:s.hy,bit=o==1?a:b;
   for(int r=0;r<=q;r++){put(side,r,v.c+q-r,addg(v.g,q-r),v.t);
    for(int k=r;k<q;k++)put(side,r,v.c+q-r-2+(((h>>k)&1)!=bit),addg(v.g,q-r-2),v.t);}
  }
 }
 if(o==0){put(0,1,1-e,1,1);put(1,1,1-e,1,1);
  if(runs[s.run].kind){int side=runs[s.run].kind-1,h=side==0?n.hx:n.hy,bit=side==0?b:a;
   for(int q=1;q<=s.length;q++){
    for(int r=0;r<=q;r++)put(side,r,-r+(((h>>q)&1)!=bit)-e,-r,-1);
    if(q<W)put(side,q+1,1-q-e,1-q,side==0?1:-1);
   }
  }
 }
 for(int side=0;side<2;side++)for(int q=W;q>=1;q--)if(n.f[side*W+q-1]){
  auto v=decode(n.f[side*W+q-1],q);for(int r=0;r<q;r++)put(side,r,v.c+q-r,addg(v.g,q-r),v.t);
 }
 return valid;
}
constexpr int NMON=390625;
constexpr array<int,8> MASKS{3,5,9,15,17,23,27,29};
array<int,8> increments(State const&s,int col){array<int,8> z{};
 for(int side=0;side<2;side++){
  int bit=side==0?symbolX(col):symbolY(col),h=side==0?s.hx:s.hy;if(bit<0)continue;
  int len=histlen(h),window=((h&15)<<1)|bit;
  for(int j=0;j<8;j++)if((MASKS[j]>>(len+1))==0)
   z[j]+=(__builtin_popcount(unsigned(window&MASKS[j]))&1)?-1:1;
 }return z;
}
uint32_t monomial(State const&s,int col){auto z=increments(s,col);int v=0;
 for(int j=7;j>=0;j--)v=5*v+z[j]+2;
 return (col<2?0:col<4?1:2)*NMON+v;
}
// The direct product avoids a standalone tracker partition. BFS labels are 0..7.
struct Full {State s;uint32_t b=0;bool operator==(Full const&o)const{return b==o.b&&s==o.s;}};
struct HFull {size_t operator()(Full const&v)const{return Hash64{}(HState{}(v.s)^uint64_t(v.b)*0x9e3779b97f4a7c15ULL);}};
int flip_hist(int h){return h^((1<<histlen(h))-1);}
void complement(Full &f){f.b=flip_base[f.b];f.s.hx=flip_hist(f.s.hx);f.s.hy=flip_hist(f.s.hy);f.s.run=base_run[f.b];}
void normalize(Full &f){if(f.s.hx>1?(f.s.hx&1):(f.s.hy>1&&(f.s.hy&1)))complement(f);}
// Independent small-pair canonical DP audit of acceptance and the path lift.
void audit(vector<Row>const&bg){uint64_t pairs=0;
 for(int nx=0;nx<=6;nx++)for(int ny=0;ny<=6;ny++)for(int xx=0;xx<(1<<nx);xx++)for(int yy=0;yy<(1<<ny);yy++){
  vector<int>x(nx),y(ny);for(int i=0;i<nx;i++)x[i]=(xx>>i)&1;for(int j=0;j<ny;j++)y[j]=(yy>>j)&1;
  vector<vector<Key>> dp(nx+1,vector<Key>(ny+1,{10000,10000,""}));dp[0][0]={0,0,""};
  for(int i=0;i<=nx;i++)for(int j=0;j<=ny;j++){
   auto put=[&](int a,int b,int co,int ga,char o){auto[c,g,w]=dp[i][j];dp[a][b]=min(dp[a][b],Key(c+co,g+ga,w+o));};
   if(i<nx&&j<ny)put(i+1,j+1,x[i]!=y[j],0,'0');if(i<nx)put(i+1,j,1,1,'1');if(j<ny)put(i,j+1,1,1,'2');
  }
  Full original,representative;int i=0,j=0;array<int,8> emitted{};
  for(char oper:get<2>(dp[nx][ny])){
   int c=oper=='0'?(x[i]==y[j]?x[i]:(x[i]?3:2)):(oper=='1'?4+x[i]:6+y[j]);
   bool flipped=original.s.hx>1?(original.s.hx&1):(original.s.hy>1&&(original.s.hy&1));int label=c^int(flipped);
   Full on,rn;on.b=bg[original.b].to[c];rn.b=bg[representative.b].to[label];
   require(on.b!=NONE&&rn.b!=NONE,"canonical bank/run path rejected");
   require(transition(original.s,c,on.s)&&transition(representative.s,label,rn.s),"canonical frontier path rejected");
   require(monomial(original.s,c)==monomial(representative.s,label),"lift feature mismatch");
   auto delta=increments(original.s,c);for(int k=0;k<8;k++)emitted[k]+=delta[k];
   Full normalized=on;normalize(normalized);normalize(rn);require(normalized==rn,"path lift mismatch");
   original=on;representative=rn;if(oper!='2')i++;if(oper!='1')j++;
  }
  array<int,8> explicit_sum{};
  for(auto const&bits: {x,y})for(int end=0;end<int(bits.size());end++)for(int k=0;k<8;k++){
   int product=1;bool available=true;
   for(int offset=0;offset<=4;offset++)if(MASKS[k]&(1<<offset)){
    if(end<offset){available=false;break;} product*=bits[end-offset]?-1:1;
   }
   if(available)explicit_sum[k]+=product;
  }
  require(emitted==explicit_sum,"emitted Walsh sums differ from complete input products");pairs++;
 }
 cout<<"canonical acceptance and lifted features audited "<<pairs<<" pairs (lengths 0..6)"<<endl;
}
vector<Row> direct(vector<Row>const&bg,uint64_t expected){
 unordered_map<Full,uint32_t,HFull> ids;ids.reserve(expected);vector<Full>st(1);st.reserve(expected);ids.emplace(st[0],0);vector<Row>g;g.reserve(expected);
 for(size_t i=0;i<st.size();i++){Full f=st[i];require(f.s.run==base_run[f.b],"run coordinate disagreement");Row row;
  for(int a=0;a<8;a++){auto bn=bg[f.b].to[a];if(bn==NONE)continue;Full n;n.b=bn;if(!transition(f.s,a,n.s))continue;
   require(n.s.run==base_run[n.b],"target run coordinate disagreement");normalize(n);
   auto[it,ok]=ids.emplace(n,st.size());if(ok){require(st.size()<expected,"excess product states");st.push_back(n);}row.to[a]=it->second;row.wt[a]=monomial(f.s,a);edgecount++;
  }g.push_back(row);if(i%1000000==0)cout<<"product "<<i<<" discovered "<<st.size()<<endl;
 }
 require(g.size()==expected,"product count");cout<<"product total "<<g.size()<<" edges "<<edgecount<<endl;return g;
}
// Exact 128-bit integer recipe and strict full-row tests. Coefficient ceilings
// were computed with unbounded Python integers from the certificate rationals.
using U128=__uint128_t;
string decimal(U128 v){string s;do{s+=char('0'+v%10);v/=10;}while(v);reverse(s.begin(),s.end());return s;}
int main(int argc,char**argv){try{
 require(argc==3,"usage independent input.txt graph_result.json");ifstream in(argv[1]);uint64_t bo,bm,ps,pc;
 in>>W>>B>>S>>T>>bo>>bm>>ps>>pc;require(bool(in),"input header");
 require(W==3&&B==2&&S==0&&T==2,"unsupported frontier parameters");
 initruns();auto bg=base(in,bo,bm);audit(bg);
 int precision,steps;uint64_t initial;in>>precision>>initial>>steps;
 require(precision>=0&&precision<=48&&initial>0&&initial<=(1ULL<<60)&&steps>=0,"recipe range");
 uint64_t unit=1ULL<<precision;vector<uint64_t> weights(3*NMON);
 for(auto &w:weights){in>>w;require(w>0&&w<(1ULL<<48),"weight range");}
 require(bool(in),"input truncated");string surplus;require(!(in>>surplus),"input trailing data");
 if(steps==0){State root;U128 row=0;
  for(int a=0;a<8;a++){State next;if(bg[0].to[a]!=NONE&&transition(root,a,next))row+=U128(weights[monomial(root,a)])*initial;}
  require(row<U128(unit)*initial,"constant recipe fails exact root row");
 }
 auto g=direct(bg,ps);require(edgecount==499034690ULL,"edge multiplicity count");
 auto colors=refine(g,true);require(1+*max_element(colors.begin(),colors.end())==pc,"potential palette count");
 // Quotient rows are exactly the first complete rows in first-appearance classes.
 vector<Row> q(pc);vector<bool> seen(pc,false);
 for(size_t i=0;i<g.size();i++)if(!seen[colors[i]]){
  Row r=g[i];for(auto &d:r.to)if(d!=NONE)d=colors[d];q[colors[i]]=r;seen[colors[i]]=true;
 }
 vector<uint64_t> pot(pc,initial),next(pc);
 for(int step=0;step<steps;step++){
  uint64_t bad=UINT64_MAX;
  #pragma omp parallel for num_threads(16) schedule(static) reduction(min:bad)
  for(size_t i=0;i<q.size();i++){
   U128 total=U128(unit)*pot[i];
   for(int a=0;a<8;a++)if(q[i].to[a]!=NONE)total+=U128(weights[q[i].wt[a]])*pot[q[i].to[a]];
   U128 value=1+(total>>(precision+1));
   if(value>numeric_limits<uint64_t>::max()||value==0)bad=min(bad,uint64_t(i));else next[i]=uint64_t(value);
  }
  require(bad==UINT64_MAX,"potential uint64 overflow at class "+to_string(bad));pot.swap(next);
  if((step+1)%8==0||step+1==steps)cout<<"integer recipe iteration "<<step+1<<" of "<<steps<<endl;
 }
 U128 minmargin=~U128(0);uint64_t minrow=UINT64_MAX,badrow=UINT64_MAX;
 #pragma omp parallel num_threads(16)
 {
 U128 localmin=~U128(0);uint64_t localrow=UINT64_MAX,localbad=UINT64_MAX;
 #pragma omp for schedule(static)
 for(size_t i=0;i<g.size();i++){
  U128 sum=0;for(int a=0;a<8;a++)if(g[i].to[a]!=NONE)sum+=U128(weights[g[i].wt[a]])*pot[colors[g[i].to[a]]];
  U128 rhs=U128(unit)*pot[colors[i]];
  if(!(sum<rhs)){localbad=min(localbad,uint64_t(i));continue;}
  U128 margin=rhs-sum;if(margin<localmin||(margin==localmin&&i<localrow)){localmin=margin;localrow=i;}
 }
 #pragma omp critical
 {badrow=min(badrow,localbad);if(localmin<minmargin||(localmin==minmargin&&localrow<minrow)){minmargin=localmin;minrow=localrow;}}
 }
 if(badrow!=UINT64_MAX){cout<<"DISAGREES first row failure "<<badrow<<endl;return 2;}
 cout<<"AGREES all exact rows; minimum integer slack "<<decimal(minmargin)<<" at row "<<minrow<<endl;
 ofstream out(argv[2]);out<<"{\"states\":"<<g.size()<<",\"edges\":"<<edgecount<<",\"classes\":"<<pc
 <<",\"lifted_states\":"<<(2*g.size()-1)<<",\"minimum_integer_slack\":\""<<decimal(minmargin)
 <<"\",\"majorant_denominator\":"<<unit<<",\"minimum_slack_row\":"<<minrow<<"}\n";
 require(bool(out),"result write failed");
 }catch(exception const&e){cout<<"DISAGREES "<<e.what()<<endl;return 2;} }

// Exact checker written for round 3, separately from generation and SDP/search.
// Rebuilds flag orbits and all disjoint extension samples from certificate data.
#include <gmpxx.h>
#include <array>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <tuple>
#include <vector>
using namespace std;using Z=mpz_class;using G=array<array<int,9>,9>;
static void demand(bool v,string msg){if(!v)throw runtime_error(msg);}
static long binom(int n,int k){if(k<0||k>n)return 0;long r=1;for(int j=1;j<=k;j++)r=r*(n-j+1)/j;return r;}
static vector<vector<int>> orderings(int n){vector<vector<int>>o;vector<int>v(n);iota(v.begin(),v.end(),0);do{o.push_back(v);}while(next_permutation(v.begin(),v.end()));return o;}
static int induced(const G&a,const vector<int>&v){int mask=0,bit=0;for(size_t j=1;j<v.size();j++)for(size_t i=0;i<j;i++)mask|=a[v[i]][v[j]]<<(bit++);return mask;}
static G unpack(int m,int s){G a{};int p=0;for(int j=1;j<s;j++)for(int i=0;i<j;i++)a[i][j]=a[j][i]=(m>>(p++))&1;return a;}
struct Block{int t,m,typ,d,r,mode,color;long den;vector<int>flags;vector<vector<Z>>Q;bool zero=true;};
struct Family{int t,m,mode,color;map<int,int>allowed;vector<pair<int,int>>which;};
struct Partition{int family;vector<int>left,right;};
int main(int argc,char**argv){try{
 demand(argc==3||argc==5,"usage: checker certificate graph6 [shard shards]");int shard=argc==5?stoi(argv[3]):0,shards=argc==5?stoi(argv[4]):1;demand(shard>=0&&shard<shards,"shard range");
 ifstream in(argv[1]);int n,k,B,mode;long D;string bnstr,bdstr,line;getline(in,line);istringstream h(line);demand(bool(h>>n>>k>>D>>B>>bnstr>>bdstr>>mode),"header parse");h>>ws;demand(h.eof(),"header extra");Z bn(bnstr),bd(bdstr);demand(n>=k&&n<=9&&k>=2&&D>0&&B>0&&B<=1000&&bd>0&&bn>=0&&(mode==-2||mode==-1||mode==0||mode==1),"header ranges");
 bool export8=getenv("EIGHT_RESIDUALS")!=nullptr;if(export8){demand(n==9,"lift requires ambient nine");n=8;}
 vector<Block>blocks;vector<Family>families;map<tuple<int,int,int,int>,int>fids;set<tuple<int,int,int,int,int>>unique;long common=binom(n,k);
 for(int z=0;z<B;z++){
  Block b;demand(bool(in>>b.t>>b.m>>b.typ>>b.d>>b.r),"block parse");b.mode=mode;b.color=0;if(mode<0)demand(bool(in>>b.mode),"block mode");if(mode==-2)demand(bool(in>>b.color),"block colour");demand(b.color==0||b.color==1,"colour range");
  demand(b.t>=0&&b.m>=1&&b.t+2*b.m<=n&&b.t+b.m<=7&&b.d>=1&&b.d<=4096&&b.r>=1&&b.r<=10000&&(b.mode==0||b.mode==1),"block ranges");demand(unique.insert({b.t,b.m,b.typ,b.mode,b.color}).second,"duplicate block");
  b.flags.resize(b.d);for(int&f:b.flags)demand(bool(in>>f),"missing flag");vector<vector<Z>>L(b.r,vector<Z>(b.d));
  for(auto&r:L)for(Z&v:r){string s;demand(bool(in>>s)&&mpz_set_str(v.get_mpz_t(),s.c_str(),10)==0,"invalid square factor");if(v!=0)b.zero=false;}
  b.Q.assign(b.d,vector<Z>(b.d));if(!b.zero)for(int i=0;i<b.d;i++)for(int j=0;j<=i;j++){Z v=0;for(int r=0;r<b.r;r++)v+=L[r][i]*L[r][j];b.Q[i][j]=b.Q[j][i]=v;}
  b.den=binom(n,b.t)*binom(n-b.t,b.m)*binom(n-b.t-b.m,b.m);if(b.mode)for(int j=2;j<=b.t;j++)b.den*=j;common=lcm(common,b.den);
  auto key=make_tuple(b.t,b.m,b.mode,b.color);if(!fids.count(key)){Family f;f.t=b.t;f.m=b.m;f.mode=b.mode;f.color=b.color;f.which.assign(1<<((b.t+b.m)*(b.t+b.m-1)/2),{-1,-1});fids[key]=families.size();families.push_back(move(f));}Family&f=families[fids[key]];demand(!f.allowed.count(b.typ),"type collision");f.allowed[b.typ]=z;
  auto rp=orderings(b.t),ep=orderings(b.m);
  for(int col=0;col<b.d;col++){
   demand(b.flags[col]>=0&&b.flags[col]<int(f.which.size()),"flag out of range");G a=unpack(b.flags[col],b.t+b.m);bool righttype=false;for(auto&r:rp){if(b.mode&&r!=rp.front())continue;if(induced(a,r)==b.typ)righttype=true;}demand(righttype,"wrong type in flag");
   for(auto&r:rp){if(b.mode&&r!=rp.front())continue;for(auto&e:ep){vector<int>v=r;for(int u:e)v.push_back(b.t+u);int m=induced(a,v);demand(f.which[m].first<0||f.which[m]==make_pair(z,col),"duplicate flag orbit");f.which[m]={z,col};}}
  }
  blocks.push_back(move(b));
 }
 demand(!(in>>line),"trailing certificate data");
 for(auto&f:families){int rootbits=f.t*(f.t-1)/2;auto rp=orderings(f.t);for(int mask=0;mask<int(f.which.size());mask++){int root=mask&((1<<rootbits)-1);bool needs=f.allowed.count(root);if(!f.mode&&!needs){G a=unpack(root,f.t);for(auto&r:rp)if(f.allowed.count(induced(a,r))){needs=true;break;}}demand(!needs||f.which[mask].first>=0,"incomplete flags for selected type");}}
 for(auto&b:blocks)if(!b.zero)for(auto&r:b.Q)for(auto&v:r)v*=common/b.den;
 vector<Partition>parts;
 for(int fidx=0;fidx<int(families.size());fidx++){
  auto&f=families[fidx];bool any=false;for(auto&kv:f.allowed)any|=!blocks[kv.second].zero;if(!any)continue;
  for(int R=0;R<(1<<n);R++)if(__builtin_popcount(unsigned(R))==f.t){vector<int>root,remaining;for(int v=0;v<n;v++)((R>>v&1)?root:remaining).push_back(v);
   do{for(int A=0;A<(1<<remaining.size());A++)if(__builtin_popcount(unsigned(A))==f.m){int rem=((1<<remaining.size())-1)^A;for(int B=rem;;B=(B-1)&rem){if(__builtin_popcount(unsigned(B))==f.m){Partition p;p.family=fidx;p.left=p.right=root;for(int v=0;v<int(remaining.size());v++){if(A>>v&1)p.left.push_back(remaining[v]);if(B>>v&1)p.right.push_back(remaining[v]);}parts.push_back(move(p));}if(B==0)break;}}}while(f.mode&&next_permutation(root.begin(),root.end()));
  }
 }
 ofstream exported;if(export8){exported.open(getenv("EIGHT_RESIDUALS"));Z den=Z(common)*D*D;exported<<den.get_str()<<" "<<bn.get_str()<<" "<<bd.get_str()<<"\n";}
 ifstream graphs(argv[2]);long row=0,count=0,worst=-1;Z mincore;vector<vector<int>>subsets;for(int S=0;S<(1<<n);S++)if(__builtin_popcount(unsigned(S))==k){vector<int>v;for(int j=0;j<n;j++)if(S>>j&1)v.push_back(j);subsets.push_back(v);}Z rhs=bn*common*D*D;
 while(getline(graphs,line)){
  demand(line.size()==size_t(1+(n*(n-1)/2+5)/6)&&int((unsigned char)line[0])-63==n,"graph6 format/order");for(size_t c=1;c<line.size();c++)demand(line[c]>=63&&line[c]<=126,"graph6 alphabet");long index=row++;if(index%shards!=shard)continue;
  G a{};int bit=0;for(int j=1;j<n;j++)for(int i=0;i<j;i++){int v=int((unsigned char)line[1+bit/6])-63;a[i][j]=a[j][i]=(v>>(5-bit%6))&1;bit++;}
  G opposite=a;for(int i=0;i<n;i++)for(int j=0;j<i;j++)opposite[i][j]=opposite[j][i]=1-a[i][j];
  int mono=0;for(auto&v:subsets){int code=induced(a,v);mono+=(code==0||code==(1<<(k*(k-1)/2))-1);}
  Z core=Z(mono)*(common/binom(n,k))*D*D;
  // Aggregate ordinary integer occurrence counts before any big-integer products.
  map<tuple<int,int,int>,int>counts;
  for(auto&p:parts){auto&f=families[p.family];const G&graph=f.color?opposite:a;auto[b,i]=f.which[induced(graph,p.left)];auto[c,j]=f.which[induced(graph,p.right)];if(b<0||c<0){demand(b==c,"inconsistent root membership");continue;}demand(b==c,"inconsistent type");if(!blocks[b].zero){if(i>j)swap(i,j);counts[{b,i,j}]++;}}
  for(auto&kv:counts){auto[b,i,j]=kv.first;core-=blocks[b].Q[i][j]*kv.second;}
  Z slack=core*bd-rhs;if(export8)exported<<core.get_str()<<"\n";else demand(slack>=0,"negative inequality at graph "+to_string(index));if(worst<0||core<mincore){mincore=core;worst=index;}count++;if(count%10000==0)cerr<<"checked "<<count<<" shard "<<shard<<"\n";
 }
 demand(row>0&&count>0,"empty input/shard");cout<<(export8?"EXPORTED exact eight-vertex coefficients; no eight-vertex bound asserted; ":"PASS exact inequalities ")<<count<<" / "<<row<<" graphs; shard "<<shard<<" of "<<shards<<"; integer-square PSD\n";cout<<"BOUND "<<bn.get_str()<<"/"<<bd.get_str()<<"\n";Z den=Z(common)*D*D;cout<<"MINIMUM "<<mincore.get_str()<<"/"<<den.get_str()<<" graph "<<worst<<"\n";cout<<"REQUIRES separate exhaustive graph-list completeness replay\n";
 return 0;
 }catch(exception&e){cerr<<"REJECT "<<e.what()<<"\n";return 1;}}

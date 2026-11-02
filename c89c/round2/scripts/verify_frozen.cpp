// Independently written exact certificate replay. Does not read any search table.
// Uses arbitrary precision integers and directly reconstructs every coefficient.
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <vector>
using namespace std;using Z=mpz_class;using Mask=uint64_t;
long C(int n,int k){if(k<0||k>n)return 0;long r=1;for(int i=1;i<=k;i++)r=r*(n+1-i)/i;return r;}
vector<vector<int>> allorders(int n){vector<vector<int>> r;vector<int>p(n);iota(p.begin(),p.end(),0);do{r.push_back(p);}while(next_permutation(p.begin(),p.end()));return r;}
using Adj=array<array<unsigned char,9>,9>;
Mask encode(const Adj&a,const vector<int>&v){Mask r=0;int k=0;for(int j=1;j<(int)v.size();j++)for(int i=0;i<j;i++,k++)r|=Mask(a[v[i]][v[j]])<<k;return r;}
Adj decode(Mask r,int n){Adj a{};int k=0;for(int j=1;j<n;j++)for(int i=0;i<j;i++,k++)a[i][j]=a[j][i]=(r>>k)&1;return a;}
struct Block{int t,m,typ,d,h;long den;vector<int>flags;vector<vector<Z>>q;};
struct Family{int t,m;vector<pair<int,int>>lut;};
struct Term{int f;vector<int>a,b;};
void require(bool b,string s){if(!b)throw runtime_error(s);}
int main(int argc,char**argv){try{
 require(argc==3,"usage: verify_frozen certificate graph6");ifstream f(argv[1]);int n,k,mode,B;long D;string sbn,sbd,line;getline(f,line);istringstream h(line);require(bool(h>>n>>k>>D>>B>>sbn>>sbd>>mode),"header fields");Z bn(sbn),bd(sbd);h>>ws;require(h.eof()&&n>=k&&n<=9&&k>=2&&D>0&&bd>0&&B>0&&(mode==0||mode==1),"header");
 vector<Block>blocks;vector<Family>families;map<pair<int,int>,int>famid;set<tuple<int,int,int>>seen;long common=C(n,k);
 for(int z=0;z<B;z++){Block b;f>>b.t>>b.m>>b.typ>>b.d>>b.h;require(f.good()&&b.t>=0&&b.m>0&&b.t+2*b.m<=n&&b.t+b.m<=7&&b.d>0&&b.d<2049&&b.h>0&&b.h<4097,"block parameters");require(seen.insert({b.t,b.m,b.typ}).second,"duplicate block");
 b.flags.resize(b.d);for(int&i:b.flags)f>>i;vector<vector<Z>>L(b.h,vector<Z>(b.d));for(auto&r:L)for(auto&v:r){string s;f>>s;require(mpz_set_str(v.get_mpz_t(),s.c_str(),10)==0,"integer factor syntax");}require(f.good(),"truncated factors");b.q.assign(b.d,vector<Z>(b.d));for(int i=0;i<b.d;i++)for(int j=i;j<b.d;j++){Z v=0;for(int r=0;r<b.h;r++)v+=L[r][i]*L[r][j];b.q[i][j]=b.q[j][i]=v;}
 b.den=C(n,b.t)*C(n-b.t,b.m)*C(n-b.t-b.m,b.m);if(mode)for(int j=2;j<=b.t;j++)b.den*=j;common=lcm(common,b.den);
 auto key=make_pair(b.t,b.m);if(!famid.count(key)){famid[key]=families.size();Family F;F.t=b.t;F.m=b.m;F.lut.assign(1<<((b.t+b.m)*(b.t+b.m-1)/2),{-1,-1});families.push_back(move(F));}auto&F=families[famid[key]];
 auto rp=allorders(b.t),up=allorders(b.m);for(int i=0;i<b.d;i++){require(b.flags[i]>=0&&b.flags[i]<(int)F.lut.size(),"flag range");auto a=decode(b.flags[i],b.t+b.m);bool typeok=false;for(auto&r:rp){if(mode&&r!=rp[0])continue;if(encode(a,r)==(Mask)b.typ)typeok=true;}require(typeok,"wrong root type");for(auto&r:rp){if(mode&&r!=rp[0])continue;for(auto&u:up){auto p=r;for(int v:u)p.push_back(v+b.t);auto im=encode(a,p);auto&slot=F.lut[im];require(slot.first<0||slot==make_pair(z,i),"duplicate flag orbit");slot={z,i};}}}
 blocks.push_back(move(b));}
 string excess;require(!(f>>excess),"extra data");for(auto&F:families){set<int>allowed;for(auto&b:blocks)if(b.t==F.t&&b.m==F.m)allowed.insert(b.typ);int rootmask=(1<<(F.t*(F.t-1)/2))-1;for(int x=0;x<(int)F.lut.size();x++)require((mode&&!allowed.count(x&rootmask))||F.lut[x].first>=0,"incomplete flag family");}
 for(auto&b:blocks)for(auto&r:b.q)for(auto&v:r)v*=Z(common/b.den)*bd;
 vector<Term>terms;for(int z=0;z<(int)families.size();z++){auto&F=families[z];for(int rootmask=0;rootmask<(1<<n);rootmask++)if(__builtin_popcount((unsigned)rootmask)==F.t){vector<int>r,v;for(int i=0;i<n;i++)((rootmask>>i&1)?r:v).push_back(i);do{for(int am=0;am<(1<<v.size());am++)if(__builtin_popcount((unsigned)am)==F.m){int avail=((1<<v.size())-1)^am;for(int bm=avail;;bm=(bm-1)&avail){if(__builtin_popcount((unsigned)bm)==F.m){Term T;T.f=z;T.a=T.b=r;for(int j=0;j<(int)v.size();j++){if(am>>j&1)T.a.push_back(v[j]);if(bm>>j&1)T.b.push_back(v[j]);}terms.push_back(move(T));}if(!bm)break;}}}while(mode&&next_permutation(r.begin(),r.end()));}}
 // Independent complete orbit cover at order <=8, accelerated with nibble tables.
 vector<unsigned char>cover;if(n<=8)cover.assign((size_t(1)<<(n*(n-1)/2))/8+1,0);long covered=0,randomsum=0;vector<vector<array<Mask,16>>>maps;
 if(n<=8){int bits=n*(n-1)/2,nibbles=(bits+3)/4;for(auto&p:allorders(n)){vector<int>inv(n);for(int i=0;i<n;i++)inv[p[i]]=i;vector<int>dest(bits);int b=0;for(int j=1;j<n;j++)for(int i=0;i<j;i++,b++){int x=inv[i],y=inv[j];if(x>y)swap(x,y);dest[b]=y*(y-1)/2+x;}vector<array<Mask,16>>table(nibbles);for(int q=0;q<nibbles;q++)for(int val=0;val<16;val++){Mask v=0;for(int j=0;j<4;j++)if((val>>j&1)&&q*4+j<bits)v|=Mask(1)<<dest[q*4+j];table[q][val]=v;}maps.push_back(move(table));}}
 ifstream graphs(argv[2]);int rows=0,worst=-1;Z best=0,scale=Z(common)*D*D*bd;
 vector<vector<int>>subsets;for(int S=0;S<(1<<n);S++)if(__builtin_popcount((unsigned)S)==k){vector<int>v;for(int i=0;i<n;i++)if(S>>i&1)v.push_back(i);subsets.push_back(v);}
 while(getline(graphs,line)){require(!line.empty()&&(unsigned char)line[0]-63==n,"graph order");require(line.size()==size_t(1+(n*(n-1)/2+5)/6),"graph6 length");Mask g=0;for(int b=0;b<n*(n-1)/2;b++){int v=(unsigned char)line[1+b/6]-63;require(v>=0&&v<64,"graph6 character");g|=Mask((v>>(5-b%6))&1)<<b;}auto a=decode(g,n);int mono=0;for(auto&v:subsets){Mask s=encode(a,v);mono+=(s==0||s==((Mask(1)<<(k*(k-1)/2))-1));}
 if(n<=8){require(!(cover[g/8]>>(g%8)&1),"duplicate graph class");long before=covered;for(auto&table:maps){Mask im=0,tmp=g;for(auto&T:table){im|=T[tmp&15];tmp>>=4;}unsigned char bit=1<<(im%8);if(!(cover[im/8]&bit)){cover[im/8]|=bit;covered++;}}randomsum+=(covered-before)*mono;}
 Z slack=Z(mono)*(common/C(n,k))*D*D*bd-bn*common*D*D;
 for(auto&T:terms){auto&F=families[T.f];auto [b,i]=F.lut[encode(a,T.a)];auto [bb,j]=F.lut[encode(a,T.b)];if(b<0||bb<0){require(b==bb,"type lookup mismatch");continue;}require(b==bb,"type mismatch");slack-=blocks[b].q[i][j];}
 require(slack>=0,"negative exact slack at graph "+to_string(rows));if(worst<0||slack<best){best=slack;worst=rows;}rows++;if(rows%10000==0)cerr<<"checked "<<rows<<"\n";
 }
 require(rows>0,"empty graph list");if(n<=8){require(covered==(1LL<<(n*(n-1)/2)),"incomplete graph list");require(randomsum*(1LL<<(k*(k-1)/2-1))==covered*C(n,k),"random normalization");cout<<"PASS exhaustive labelled cover "<<covered<<" and random normalization\n";}else cout<<"NOTE order-nine list completeness requires separate augmentation check\n";
 cout<<"PASS exact coefficient inequalities: "<<rows<<" classes, "<<B<<" PSD square-factor blocks; c"<<k<<" >= "<<bn.get_str()<<"/"<<bd.get_str()<<"\n";cout<<"MIN_SLACK "<<best.get_str()<<" / "<<scale.get_str()<<" at "<<worst<<"\n";return 0;
 }catch(exception&e){cerr<<"FAIL "<<e.what()<<"\n";return 1;}}

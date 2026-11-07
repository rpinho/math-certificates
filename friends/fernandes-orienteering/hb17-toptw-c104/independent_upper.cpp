// Independent HB17 referee. No claimant implementation used.
// Time and coordinates are exact hundredths; rewards are scaled integers.
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using I=long long;
I dec(string s){bool neg=s[0]=='-';if(neg)s=s.substr(1);auto p=s.find('.');string a=p==string::npos?s:s.substr(0,p),b=p==string::npos?"":s.substr(p+1);if(b.size()>2)throw runtime_error("precision");while(b.size()<2)b+='0';return (neg?-1:1)*(stoll(a)*100+stoll(b));}
I isqrt(I x){I v=sqrt((long double)x);while((v+1)*(v+1)<=x)++v;while(v*v>x)--v;return v;}
struct V{I x,y,s,p,o,c;};struct L{int i;I t,q;uint64_t m;};
struct Pareto{vector<pair<I,I>> v;void finish(){sort(v.begin(),v.end());I b=-(1LL<<60);for(auto &x:v){b=max(b,x.second);x.second=b;}}bool has(I t,I q)const{auto p=upper_bound(v.begin(),v.end(),make_pair(t,(I)(1LL<<60)));return p!=v.begin()&&prev(p)->second>=q;}};
int main(int argc,char**argv){try{
 if(argc<4)throw runtime_error("usage raw dual proof [unresolved_output]");
 vector<V>a;ifstream f(argv[1]);string line;getline(f,line);getline(f,line);
 while(getline(f,line)){istringstream s(line);vector<string>z;string w;while(s>>w)z.push_back(w);if(z.empty())continue;int i=stoi(z[0]);if(i!=(int)a.size()||z.size()<9)throw runtime_error("raw row");a.push_back({dec(z[1]),dec(z[2]),dec(z[3]),dec(z[4]),dec(z[z.size()-2]),dec(z.back())});}
 int n=a.size();vector<vector<I>>d(n,vector<I>(n)),sp;for(int i=0;i<n;i++)for(int j=0;j<n;j++){I dx=a[i].x-a[j].x,dy=a[i].y-a[j].y;d[i][j]=10*(isqrt(dx*dx+dy*dy)/10);}sp=d;for(int k=0;k<n;k++)for(int i=0;i<n;i++)for(int j=0;j<n;j++)sp[i][j]=min(sp[i][j],sp[i][k]+sp[k][j]);
 ifstream du(argv[2]);string magic;int nn,D,K;du>>magic>>nn>>D>>K;if(magic!="DUAL1"||nn!=n||D!=1000||K!=4)throw runtime_error("dual header");vector<I>u(n),q(n);I sumu=0,g=0;for(int i=0;i<n;i++){du>>u[i];if(!du||a[i].p%100||u[i]<0||u[i]>D*a[i].p/100)throw runtime_error("dual penalty");q[i]=D*a[i].p/100-u[i];sumu+=u[i];g=gcd(g,a[i].p/100);}if(u[0]||q[0])throw runtime_error("depot");
 ifstream pr(argv[3]);I ignore,U;pr>>magic>>nn>>ignore>>U;if(magic!="NGBOUND2"||nn!=n||U<0)throw runtime_error("proof header");
 vector<vector<int>>N(n);vector<vector<int>>pos(n,vector<int>(n,-1));for(int i=0;i<n;i++){int z;pr>>z;if(z<1||z>63)throw runtime_error("memory width");for(int k=0;k<z;k++){int j;pr>>j;if(j<0||j>=n||pos[i][j]>=0)throw runtime_error("memory node");pos[i][j]=k;N[i].push_back(j);}if(pos[i][i]<0)throw runtime_error("self memory");}
 int count;pr>>count;if(count<0||count>10000000)throw runtime_error("state count");vector<L>ls;vector<map<uint64_t,Pareto>>index(n);
 for(int z=0;z<count;z++){L l;pr>>l.i>>l.t>>l.q>>l.m;if(!pr||l.i<0||l.i>=n||l.t<0||l.q<0||l.m>>N[l.i].size()||!(l.m&(1ULL<<pos[l.i][l.i])))throw runtime_error("state invalid");if(l.i && (l.t<a[l.i].o+a[l.i].s||l.t>a[l.i].c+a[l.i].s))throw runtime_error("state window");ls.push_back(l);index[l.i][l.m].v.push_back({l.t,l.q});}for(auto &r:index)for(auto &p:r)p.second.finish();
 auto covered=[&](const L&l){uint64_t s=l.m;for(;;){auto p=index[l.i].find(s);if(p!=index[l.i].end()&&p->second.has(l.t,l.q))return true;if(s==0)break;s=(s-1)&l.m;}return false;};
 auto forbidden=[&](const L&l,int j){return pos[l.i][j]>=0&&(l.m&(1ULL<<pos[l.i][j]));};
 long long leaves=0,frac=0,knap=0,unresolved=0,trans=0,dom=0;ofstream bad(argc>4?argv[4]:"unresolved.tsv");
 auto leaf=[&](const L&l){++leaves;vector<int>C;for(int j=1;j<n;j++){if(forbidden(l,j))continue;I arr=max(l.t+sp[l.i][j],a[j].o);if(arr<=a[j].c&&arr+a[j].s+sp[j][0]<=a[0].c)C.push_back(j);}if(C.empty())return l.q<=U;
  I first=1LL<<60,last=first;for(int j:C){first=min(first,d[l.i][j]);last=min(last,d[j][0]);}I B=2*(a[0].c-l.t)-first-last;if(B<0)return l.q<=U;
  vector<pair<I,I>>items;I all=0;for(int j:C){I in=d[l.i][j],out=d[j][0];for(int h:C)if(h!=j){in=min(in,d[h][j]);out=min(out,d[j][h]);}I cost=2*a[j].s+in+out;if(cost<=0)throw runtime_error("nonpositive cost");items.push_back({cost,q[j]});all+=q[j];}if(l.q+all<=U)return true;
  sort(items.begin(),items.end(),[](auto x,auto y){return (__int128)x.second*y.first>(__int128)y.second*x.first;});I rem=B,bound=l.q;for(auto [cost,profit]:items){if(cost<=rem){bound+=profit;rem-=cost;}else{bound+=(I)((__int128)profit*rem/cost);break;}}if(bound<=U){++frac;return true;}
  // Exact 0/1 resource knapsack, after dividing costs by their gcd.
  I cg=0;for(auto x:items)cg=gcd(cg,x.first);int cap=B/cg;vector<I>dp(cap+1,0);for(auto [cost,profit]:items){int c=cost/cg;for(int b=cap;b>=c;b--)dp[b]=max(dp[b],dp[b-c]+profit);}if(l.q+dp[cap]<=U){++knap;return true;}
  ++unresolved;bad<<l.i<<' '<<l.t<<' '<<l.q<<' '<<l.m<<' '<<bound<<' '<<l.q+dp[cap]<<'\n';return false;
 };
 L root{0,a[0].o+a[0].s,0,1ULL<<pos[0][0]};if(!covered(root)&&!leaf(root))throw runtime_error("root uncovered");
 for(auto l:ls){if(l.t+d[l.i][0]<=a[0].c&&l.q>U)throw runtime_error("terminal exceeds bound");for(int j=1;j<n;j++){if(forbidden(l,j))continue;I start=max(l.t+d[l.i][j],a[j].o),t=start+a[j].s;if(start>a[j].c||t+sp[j][0]>a[0].c)continue;uint64_t m=1ULL<<pos[j][j];for(int k=0;k<(int)N[l.i].size();k++)if((l.m&(1ULL<<k))&&pos[j][N[l.i][k]]>=0)m|=1ULL<<pos[j][N[l.i][k]];L next{j,t,l.q+q[j],m};++trans;if(covered(next)){++dom;continue;}leaf(next);}}
 I num=sumu+K*U;cout<<"{\"states\":"<<ls.size()<<",\"transitions\":"<<trans<<",\"dominated\":"<<dom<<",\"leaf_calls\":"<<leaves<<",\"fractional\":"<<frac<<",\"knapsack\":"<<knap<<",\"unresolved\":"<<unresolved<<",\"sum_penalty\":"<<sumu<<",\"route_upper\":"<<U<<",\"fleet_numerator\":"<<num<<",\"gcd\":"<<g<<",\"score_upper\":"<<(num/(D*g))*g<<"}\n";
 return unresolved?2:0;
 }catch(exception&e){cerr<<"REJECT: "<<e.what()<<'\n';return 1;}}

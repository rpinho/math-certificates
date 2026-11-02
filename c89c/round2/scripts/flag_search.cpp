// Exploratory exact integer flag-product coefficient generation.
// Roots are unordered; extension flags are invariant under all root automorphisms.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <vector>
using namespace std;
bool labelled_roots=false;
int bitno[9][9];
int induced(int g,const vector<int>& v){
 int z=0,b=0;
 for(int j=1;j<(int)v.size();j++)for(int i=0;i<j;i++,b++)
  if(g&(1<<bitno[v[i]][v[j]]))z|=1<<b;
 return z;
}
struct BlockFamily{
 int t,m,s;vector<int> typ,flag;map<int,int> type_ids;vector<vector<int>> keys;
 vector<vector<vector<int>>> perms;
 BlockFamily(int T,int M):t(T),m(M),s(T+M){
  vector<int> r(t),u(m);iota(r.begin(),r.end(),0);iota(u.begin(),u.end(),t);
  vector<vector<int>> pp;
  do{do{vector<int> p=r;p.insert(p.end(),u.begin(),u.end());pp.push_back(p);}while(next_permutation(u.begin(),u.end()));}while(!labelled_roots && next_permutation(r.begin(),r.end()));
  vector<int> rootcan(1<<(t*(t-1)/2));
  vector<int> rp(t);iota(rp.begin(),rp.end(),0);
  for(int g=0;g<(int)rootcan.size();g++){rootcan[g]=g;do{rootcan[g]=min(rootcan[g],induced(g,rp));}while(next_permutation(rp.begin(),rp.end()));}
  int lim=1<<(s*(s-1)/2);typ.resize(lim);flag.resize(lim);vector<int> canonical(lim);
  vector<map<int,int>> ids;
  for(int g=0;g<lim;g++){
   int can=g,rootmask=(1<<(t*(t-1)/2))-1;
   if(labelled_roots && rootcan[g&rootmask]!=(g&rootmask)){typ[g]=flag[g]=-1;continue;}
   for(auto &p:pp){int h=induced(g,p);if(make_pair(h&rootmask,h)<make_pair(can&rootmask,can))can=h;}
   canonical[g]=can;
   int tc=can&((1<<(t*(t-1)/2))-1);
   if(!type_ids.count(tc)){int id=type_ids.size();type_ids[tc]=id;keys.emplace_back();ids.emplace_back();}
   int id=type_ids[tc];typ[g]=id;
   if(!ids[id].count(can)){int fid=ids[id].size();ids[id][can]=fid;keys[id].push_back(can);}
   flag[g]=ids[id][can];
  }
 }
};
int main(int argc,char**argv){
 if(argc<5){cerr<<"usage: N graphfile prefix t,m ...\n";return 1;}
 int n=stoi(argv[1]);string prefix=argv[3];
 labelled_roots=getenv("LABELLED_ROOTS")!=nullptr;
 int bb=0;for(int j=1;j<9;j++)for(int i=0;i<j;i++)bitno[i][j]=bitno[j][i]=bb++;
 // Global bit numbers must use the same initial segment convention for all orders.
 vector<BlockFamily> fam;
 for(int a=4;a<argc;a+=2){fam.emplace_back(stoi(argv[a]),stoi(argv[a+1]));cerr<<"family "<<fam.back().t<<","<<fam.back().m<<" blocks "<<fam.back().keys.size()<<"\n";}
 vector<int> offset;int cols=0;
 ofstream meta(prefix+".meta");
 meta<<n<<" "<<labelled_roots<<"\n";
 for(auto &f:fam){
  for(auto &[type,id]:f.type_ids){int d=f.keys[id].size();offset.push_back(cols);cols+=d*(d+1)/2;meta<<f.t<<" "<<f.m<<" "<<type<<" "<<d;for(int k:f.keys[id])meta<<" "<<k;meta<<"\n";}
 }
 // type_ids iteration need not agree with insertion IDs: explicit lookup offsets.
 vector<vector<int>> starts;int total=0;
 for(auto &f:fam){vector<int> v(f.keys.size());for(auto &[type,id]:f.type_ids){v[id]=total;int d=f.keys[id].size();total+=d*(d+1)/2;}starts.push_back(v);}
 vector<string> gs;ifstream in(argv[2]);string line;while(getline(in,line)){if(line.rfind(">>",0)==0)continue;if(!line.empty())gs.push_back(line);}
 ofstream out(prefix+".coo"),obj(prefix+".objective"),obj5(prefix+".objective5"),obj56(prefix+".objective56");
 out<<gs.size()<<" "<<cols<<"\n";
 for(int row=0;row<(int)gs.size();row++){
  string g6=gs[row];int g=0,nb=n*(n-1)/2;
  for(int b=0;b<nb;b++){int c=(unsigned char)g6[1+b/6]-63;if(c&(1<<(5-b%6)))g|=1<<b;}
  vector<int> six;int mono=0,all=0,blue6=0;
  for(int mask=0;mask<(1<<n);mask++)if(__builtin_popcount((unsigned)mask)==6){six.clear();for(int a=0;a<n;a++)if(mask>>a&1)six.push_back(a);int h=induced(g,six);mono+=(h==0 || h==32767);blue6+=(h==0);all++;}
  obj<<mono<<" "<<all<<"\n";
  int mono5=0,all5=0,red5=0;
  for(int mask=0;mask<(1<<n);mask++)if(__builtin_popcount((unsigned)mask)==5){six.clear();for(int a=0;a<n;a++)if(mask>>a&1)six.push_back(a);int h=induced(g,six);mono5+=(h==0 || h==1023);red5+=(h==1023);all5++;}
  obj5<<mono5<<" "<<all5<<"\n";
  obj56<<red5<<" "<<all5<<" "<<blue6<<" "<<all<<"\n";
  map<int,int> cnt;
  for(int z=0;z<(int)fam.size();z++){
   auto &f=fam[z];int t=f.t,m=f.m,den=0;
   for(int rm=0;rm<(1<<n);rm++)if(__builtin_popcount((unsigned)rm)==t){
    vector<int> roots,rest;for(int a=0;a<n;a++)((rm>>a&1)?roots:rest).push_back(a);
    do{for(int am=0;am<(1<<(n-t));am++)if(__builtin_popcount((unsigned)am)==m){
     vector<int> a=roots,b=roots;
     for(int j=0;j<n-t;j++)((am>>j&1)?a:b).push_back(rest[j]);
     if((int)b.size()!=t+m){cerr<<"bad family\n";return 2;}
     int ga=induced(g,a),gb=induced(g,b),id=f.typ[ga];
     if(id<0)continue;
     if(id!=f.typ[gb])return 3;
     int i=f.flag[ga],j=f.flag[gb];if(i>j)swap(i,j);
     int d=f.keys[id].size();int col=starts[z][id]+i*d-i*(i-1)/2+(j-i);
     cnt[col]++;den++;
    }}while(labelled_roots && next_permutation(roots.begin(),roots.end()));
   }
   // Each family's coefficients are scaled by its total root/partition count.
   // A common denominator for every graph in this family preserves positivity.
   if(row==0)cerr<<"den "<<t<<" "<<m<<" "<<den<<"\n";
  }
  for(auto &[c,v]:cnt)out<<row<<" "<<c<<" "<<v<<"\n";
  if(row%1000==0)cerr<<"row "<<row<<"/"<<gs.size()<<"\n";
 }
}

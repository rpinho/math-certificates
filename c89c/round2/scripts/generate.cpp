// Search coefficient generator, with orbit expansion and 64-bit graph masks.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <vector>
using namespace std;
using U=uint64_t;
int bitno[10][10];bool ordered;
int induced(U g,const vector<int>& p){int h=0,b=0;for(int j=1;j<(int)p.size();j++)for(int i=0;i<j;i++,b++)h|=((g>>bitno[p[i]][p[j]])&1)<<b;return h;}
vector<vector<int>> perms(int t,int m,bool fixed=false){vector<vector<int>> ans;vector<int> r(t),u(m);iota(r.begin(),r.end(),0);iota(u.begin(),u.end(),t);do{do{auto v=r;v.insert(v.end(),u.begin(),u.end());ans.push_back(v);}while(next_permutation(u.begin(),u.end()));}while(!fixed&&next_permutation(r.begin(),r.end()));return ans;}
struct Fam{int t,m,s;vector<int> type,flag,rootcan;map<int,vector<int>> keys;map<int,int> start;
 Fam(int T,int M):t(T),m(M),s(T+M){
  int rlim=1<<(t*(t-1)/2),lim=1<<(s*(s-1)/2);rootcan.assign(rlim,-1);auto rp=perms(t,0);
  for(int g=0;g<rlim;g++)if(rootcan[g]<0)for(auto&p:rp)rootcan[induced(g,p)]=g;
  type.assign(lim,-1);flag.assign(lim,-1);auto pp=perms(t,m,ordered);
  for(int g=0;g<lim;g++)if(type[g]<0 && rootcan[g&(rlim-1)]==(g&(rlim-1))){int typ=g&(rlim-1);int f=keys[typ].size();keys[typ].push_back(g);for(auto&p:pp){int h=induced(g,p);type[h]=typ;flag[h]=f;}}
  cerr<<"family "<<t<<","<<m<<" types "<<keys.size()<<" flags ";int total=0;for(auto &[a,k]:keys)total+=k.size();cerr<<total<<"\n";
 }
};
int main(int argc,char**argv){if(argc<6)return 1;int n=stoi(argv[1]);ordered=getenv("LABELLED_ROOTS");string prefix=argv[3];int b=0;for(int j=1;j<10;j++)for(int i=0;i<j;i++)bitno[i][j]=bitno[j][i]=b++;
 vector<Fam> fam;for(int a=4;a<argc;a+=2)fam.emplace_back(stoi(argv[a]),stoi(argv[a+1]));
 ofstream meta(prefix+".meta");meta<<n<<" "<<ordered<<"\n";int nc=0;for(auto&f:fam)for(auto &[typ,keys]:f.keys){f.start[typ]=nc;int d=keys.size();nc+=d*(d+1)/2;meta<<f.t<<" "<<f.m<<" "<<typ<<" "<<d;for(int k:keys)meta<<" "<<k;meta<<"\n";}
 vector<string> gs;ifstream input(argv[2]);string line;while(getline(input,line))if(!line.empty()&&line[0]!='>')gs.push_back(line);
 ofstream out(prefix+".coo"),obj(prefix+".objective"),ob5(prefix+".objective5"),ob4(prefix+".objective4");out<<gs.size()<<" "<<nc<<"\n";
 struct Sampling{int z;vector<int>a,b;};vector<Sampling> samples;
 for(int z=0;z<(int)fam.size();z++){auto&f=fam[z];for(int R=0;R<(1<<n);R++)if(__builtin_popcount((unsigned)R)==f.t){vector<int>r,rest;for(int v=0;v<n;v++)((R>>v&1)?r:rest).push_back(v);do{for(int A=0;A<(1<<rest.size());A++)if(__builtin_popcount((unsigned)A)==f.m)for(int B=0;B<(1<<rest.size());B++)if(!(A&B)&&__builtin_popcount((unsigned)B)==f.m){auto a=r,b=r;for(int j=0;j<(int)rest.size();j++){if(A>>j&1)a.push_back(rest[j]);if(B>>j&1)b.push_back(rest[j]);}samples.push_back({z,a,b});}}while(ordered&&next_permutation(r.begin(),r.end()));}}
 cerr<<"samples "<<samples.size()<<" rows "<<gs.size()<<" cols "<<nc<<"\n";
 int shard=getenv("SHARD")?stoi(getenv("SHARD")):0,shards=getenv("SHARDS")?stoi(getenv("SHARDS")):1;
 for(int row=shard;row<(int)gs.size();row+=shards){auto g6=gs[row];U g=0;for(int i=0;i<n*(n-1)/2;i++)if(((unsigned char)g6[1+i/6]-63)>>(5-i%6)&1)g|=U(1)<<i;
  for(int k=4;k<=6;k++){int mono=0,total=0;for(int S=0;S<(1<<n);S++)if(__builtin_popcount((unsigned)S)==k){vector<int>v;for(int i=0;i<n;i++)if(S>>i&1)v.push_back(i);int h=induced(g,v);mono+=h==0||h==(1<<(k*(k-1)/2))-1;total++;}auto &o=k==4?ob4:k==5?ob5:obj;o<<mono<<" "<<total<<"\n";}
  map<int,int> counts;
  for(auto&s:samples){auto&f=fam[s.z];int ga=induced(g,s.a),gb=induced(g,s.b),typ=f.type[ga];if(typ<0)continue;if(ordered && ((ga&((1<<(f.t*(f.t-1)/2))-1))!=typ))continue;int i=f.flag[ga],j=f.flag[gb];if(i>j)swap(i,j);int d=f.keys[typ].size();counts[f.start[typ]+i*d-i*(i-1)/2+j-i]++;}
  for(auto&[c,v]:counts)out<<row<<" "<<c<<" "<<v<<"\n";
  if(row%1000<shards)cerr<<"row "<<row<<"\n";
 }
}

// Independent lifted-coefficient route: sum eight-vertex residuals indexed by complete labelled orbit cover.
// Adaptation of the preceding exact verifier: only arithmetic backend and integer I/O changed.
// Independent exact verifier. No search coefficient files or canonicalization
// code are used. Flags are recognized by expanding permutation orbits.
// All coefficient arithmetic uses arbitrary-precision GMP integers.
#include <algorithm>
#include <gmpxx.h>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <sstream>
#include <vector>
#include <cstdint>
using namespace std;
using cpp_int=mpz_class;
struct Block{int t,m,type,d,rank,den;vector<int> masks;vector<vector<cpp_int>> gram;};
struct Family{int t,m,s;vector<pair<int,int>> lookup;};
long choose(int a,int b){long v=1;for(int i=1;i<=b;i++)v=v*(a-i+1)/i;return v;}
vector<vector<int>> permutations(int a,int b){
 vector<vector<int>> ans;vector<int> p(a);iota(p.begin(),p.end(),0);
 do{vector<int> q(b);iota(q.begin(),q.end(),a);do{auto r=p;r.insert(r.end(),q.begin(),q.end());ans.push_back(r);}while(next_permutation(q.begin(),q.end()));}while(next_permutation(p.begin(),p.end()));return ans;
}
vector<vector<int>> matrix_from_mask(int mask,int s){vector<vector<int>> a(s,vector<int>(s));int bit=0;for(int j=1;j<s;j++)for(int i=0;i<j;i++,bit++)a[i][j]=a[j][i]=(mask>>bit)&1;return a;}
int mapped_mask(const vector<vector<int>>& a,const vector<int>& p){int val=0,pos=0;for(int j=1;j<(int)p.size();j++)for(int i=0;i<j;i++,pos++)if(a[p[i]][p[j]])val+=1<<pos;return val;}
int main(int argc,char**argv){try{
 if(argc!=4)throw runtime_error("usage: verify_lift9 certificate graph8 graph9");
 ifstream c(argv[1]);int n,k,B,mode=0;long D;cpp_int bn,bd;
 string header;getline(c,header);istringstream hdr(header);string sbn,sbd;hdr>>n>>k>>D>>B>>sbn>>sbd;if(!hdr)throw runtime_error("invalid header fields");bn=cpp_int(sbn);bd=cpp_int(sbd);
 if(!hdr)throw runtime_error("invalid header");
 hdr>>ws;
 if(!hdr.eof()){if(!(hdr>>mode) || (mode!=0 && mode!=1))throw runtime_error("invalid root mode");hdr>>ws;if(!hdr.eof())throw runtime_error("extra header data");}
 if(n!=9)throw runtime_error("requires ambient order nine"); n=8;
 if(!c || n>8 || n<k || k<2 || D<=0 || bd<=0 || B<1)throw runtime_error("invalid header");
 vector<Block> blocks;map<pair<int,int>,int> family_ids;vector<Family> families;long common=1;
 for(int z=0;z<B;z++){
  Block b;c>>b.t>>b.m>>b.type>>b.d>>b.rank;
  if(b.t+2*b.m!=n || b.t<0 || b.m<1 || b.d<1 || b.d>1024 || b.rank<1 || b.rank>1024)throw runtime_error("invalid block");
  b.masks.resize(b.d);for(int &a:b.masks)c>>a;
  vector<vector<cpp_int>> rows(b.rank,vector<cpp_int>(b.d));
  for(auto &r:rows)for(auto &x:r){string v;c>>v;if(mpz_set_str(x.get_mpz_t(),v.c_str(),10)!=0)throw runtime_error("invalid integer factor");}
  b.gram.assign(b.d,vector<cpp_int>(b.d));
  for(int i=0;i<b.d;i++)for(int j=0;j<b.d;j++)for(int r=0;r<b.rank;r++)b.gram[i][j]+=rows[r][i]*rows[r][j];
  b.den=choose(n,b.t)*choose(n-b.t,b.m);if(mode)for(int i=2;i<=b.t;i++)b.den*=i;
  common=lcm(common,(long)b.den);
  pair<int,int> key={b.t,b.m};
  if(!family_ids.count(key)){family_ids[key]=families.size();Family f;f.t=b.t;f.m=b.m;f.s=b.t+b.m;f.lookup.assign(1<<(f.s*(f.s-1)/2),{-1,-1});families.push_back(f);}
  auto &f=families[family_ids[key]];auto pp=permutations(b.t,b.m);
  for(int i=0;i<b.d;i++){
   if(b.masks[i]<0 || b.masks[i]>=(int)f.lookup.size())throw runtime_error("bad flag mask");
   auto a=matrix_from_mask(b.masks[i],f.s);
   // Root type is checked as an isomorphism class, independently of labels.
   bool same=false;auto rootperm=permutations(b.t,0);
   for(auto &p:rootperm){bool fixed=true;for(int j=0;j<b.t;j++)fixed&=p[j]==j;if((!mode || fixed) && mapped_mask(a,p)==b.type)same=true;}
   if(!same)throw runtime_error("flag has wrong root type");
   for(auto &p:pp){bool fixed=true;for(int j=0;j<b.t;j++)fixed&=p[j]==j;if(mode && !fixed)continue;int image=mapped_mask(a,p);auto &slot=f.lookup[image];if(slot.first!=-1 && slot!=make_pair(z,i))throw runtime_error("duplicate flag orbit");slot={z,i};}
  }
  blocks.push_back(b);
 }
 string extra;if(!c || (c>>extra))throw runtime_error("truncated or extra certificate data");
 for(auto &f:families){
  vector<int> allowed(1<<(f.t*(f.t-1)/2),0);
  for(auto &b:blocks)if(b.t==f.t && b.m==f.m)allowed.at(b.type)=1;
  for(int mask=0;mask<(int)f.lookup.size();mask++){
   bool required=!mode || allowed[mask&((1<<(f.t*(f.t-1)/2))-1)];
   if(required && f.lookup[mask].first<0)throw runtime_error("incomplete rooted flag family");
  }
 }
 cpp_int scale=cpp_int(common)*D*D*choose(n,k)*bd;
 cpp_int best;int worst=-1,graphs=0;
 vector<uint16_t> covered(1<<(n*(n-1)/2),65535);vector<cpp_int> residuals8;long labeled_covered=0;
 auto allperm=permutations(n,0);long random_mono_sum=0;
 ifstream file(argv[2]);string line;
 while(getline(file,line)){
  if(line.empty())continue;
  if((int)(unsigned char)line[0]-63!=n)throw runtime_error("unexpected graph6 order/header");
  vector<vector<int>> a(n,vector<int>(n));int pos=0;
  for(int col=1;col<n;col++)for(int row=0;row<col;row++,pos++){
   int ch=(unsigned char)line.at(1+pos/6)-63;if(ch<0 || ch>=64)throw runtime_error("bad graph6 character");
   a[row][col]=a[col][row]=(ch>>(5-pos%6))&1;
  }
  int mask=mapped_mask(a,vector<int>(allperm[0]));
  if(covered[mask]!=65535)throw runtime_error("duplicate isomorphism class in graph file");
  long before=labeled_covered;
  for(auto &p:allperm){int h=mapped_mask(a,p);if(covered[h]==65535){covered[h]=graphs;labeled_covered++;}else if(covered[h]!=graphs)throw runtime_error("overlapping graph orbits");}
  int mono=0;
  for(int subset=0;subset<(1<<n);subset++)if(__builtin_popcount((unsigned)subset)==k){
   int ones=0;for(int i=0;i<n;i++)for(int j=0;j<i;j++)if((subset>>i&1)&&(subset>>j&1))ones+=a[i][j];
   if(ones==0 || ones==k*(k-1)/2)mono++;
  }
  random_mono_sum+=(labeled_covered-before)*mono;
  cpp_int lhs=cpp_int(mono)*common*D*D*bd - bn*common*D*D*choose(n,k);
  for(auto &f:families){
   for(int rootset=0;rootset<(1<<n);rootset++)if(__builtin_popcount((unsigned)rootset)==f.t){
    vector<int> root,other;for(int i=0;i<n;i++)((rootset>>i&1)?root:other).push_back(i);
    do{for(int part=0;part<(1<<(n-f.t));part++)if(__builtin_popcount((unsigned)part)==f.m){
     auto u=root,v=root;for(int j=0;j<(int)other.size();j++)((part>>j&1)?u:v).push_back(other[j]);
     auto [b1,f1]=f.lookup[mapped_mask(a,u)];auto [b2,f2]=f.lookup[mapped_mask(a,v)];
     if(b1<0 && b2<0)continue;
     if(b1!=b2)throw runtime_error("root types disagree");
     lhs-=blocks[b1].gram[f1][f2]*(common/blocks[b1].den)*choose(n,k)*bd;
    }}while(mode && next_permutation(root.begin(),root.end()));
   }
  }
  if(graphs==0 || lhs<best){best=lhs;worst=graphs;}
  residuals8.push_back(lhs);
  graphs++;
 }
 if(labeled_covered!=(long)covered.size())throw runtime_error("graph file is not exhaustive");
 long random_den=labeled_covered*choose(n,k);
 if(random_mono_sum*(1LL<<(k*(k-1)/2-1))!=random_den)throw runtime_error("random-color normalization failed");
 cout<<"PASS: eight-vertex orbit index covers all "<<labeled_covered<<" labelled graphs; random normalization.\n";
 ifstream nine(argv[3]);int count9=0,worst9=-1;cpp_int best9;
 while(getline(nine,line)){
  if(line.empty() || (unsigned char)line[0]-63!=9)throw runtime_error("order-nine graph format");
  vector<vector<int>> a9(9,vector<int>(9));int pos9=0;
  for(int j=1;j<9;j++)for(int i=0;i<j;i++,pos9++){int ch=(unsigned char)line.at(1+pos9/6)-63;if(ch<0||ch>63)throw runtime_error("graph9 character");a9[i][j]=a9[j][i]=(ch>>(5-pos9%6))&1;}
  cpp_int sum=0;
  for(int drop=0;drop<9;drop++){vector<int> vs;for(int j=0;j<9;j++)if(j!=drop)vs.push_back(j);int h=mapped_mask(a9,vs);auto id=covered[h];if(id==65535 || id>=residuals8.size())throw runtime_error("missing eight-vertex class");sum+=residuals8[id];}
  if(sum<0)throw runtime_error("negative lifted slack at graph "+to_string(count9));
  if(worst9<0||sum<best9){best9=sum;worst9=count9;}
  count9++;if(count9%50000==0)cerr<<"lift checked "<<count9<<"\n";
 }
 cpp_int den9=scale*9;
 cout<<"PASS: "<<count9<<" exact nine-vertex inequalities by summing nine independently indexed eight-vertex residuals.\n";
 cout<<"NOTE: graph9 completeness requires the separate exhaustive augmentation check.\n";
 cout<<"PASS: c"<<k<<" >= "<<bn.get_str()<<"/"<<bd.get_str()<<"; PSD by stored integer square factors.\n";
 cout<<"MIN_SLACK "<<best9.get_str()<<" / "<<den9.get_str()<<" at "<<worst9<<"\n";
 return 0;
 }catch(const exception &e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}

// Exact acceptance implementation A. Separately written (same agent); no search imports.
// Lowest-pivot elimination, integer subset domains, incremental term unions.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <vector>
using Word=uint32_t;using namespace std;
struct Check {
 int h,N;bool positive;uint64_t calls=0,solutions=0,domains=0;
 explicit Check(int n,int norm,bool p):h(n),N(norm),positive(p){assert(h>=11&&h<=22&&N<126&&6*N>=32*h);}
 void extend(const vector<Word>& known,Word finished) {
  if(positive&&solutions)return;
  ++calls;array<int,22> multiplicity{};int deficit=0;Word used=0;
  for(auto s:known){assert(s);used|=s;deficit+=6-__builtin_popcount(s);for(int j=0;j<h;++j)multiplicity[j]+=(s>>j)&1;}
  if(deficit>6*N-32*h||int(known.size())>N)return;
  int lack=0;
  for(int j=0;j<h;++j){if(multiplicity[j]>32)return;lack+=32-multiplicity[j];if(finished>>j&1)assert(multiplicity[j]==32);}
  if(lack>6*(N-int(known.size())))return;
  for(int u=0;u<h;++u)for(int v=u+1;v<h;++v){int both=0;for(Word s:known)both+=((s>>u)&(s>>v)&1);if(both>16)return;}
  if(__builtin_popcount(finished)==h){int r=N-known.size();for(int c=0;c*c<=r;++c)if(c*c==r){++solutions;break;}return;}
  // Each nonconstant integer degree-six component has numerator variance>=63.
  if((used&~finished)==0){assert(N<126);return;}
  int chosen=-1;
  for(int j=h-1;j>=0;--j)if((used>>j&1)&&!(finished>>j&1))if(chosen<0||multiplicity[j]>multiplicity[chosen])chosen=j;
  assert(chosen>=0&&multiplicity[chosen]>=16);
  vector<Word> required;for(Word s:known)if(s>>chosen&1)required.push_back(s);
  Word origin=required.back();array<Word,22> pivots{};int rank=0;
  for(Word s:required){Word delta=s^origin;while(delta){int j=__builtin_ctz(delta);if(pivots[j])delta^=pivots[j];else{pivots[j]=delta;++rank;break;}}}
  if(rank>5)return;assert(rank>=4);++domains;
  vector<Word> direction{0};for(Word s:pivots)if(s){int old=direction.size();for(int j=0;j<old;++j)direction.push_back(direction[j]^s);}
  vector<Word> base;for(Word s:direction)base.push_back(s^origin);sort(base.begin(),base.end());
  auto insert=[&](vector<Word> flat){
   sort(flat.begin(),flat.end());flat.erase(unique(flat.begin(),flat.end()),flat.end());assert(flat.size()==32);
   for(Word s:flat){if(__builtin_popcount(s)>6)return;if((s&finished)&&!binary_search(known.begin(),known.end(),s))return;}
   vector<Word> next;set_union(known.begin(),known.end(),flat.begin(),flat.end(),back_inserter(next));
   if(int(next.size())<=N)extend(next,finished|(1u<<chosen));
  };
  if(rank==5){insert(base);return;}
  vector<int> active,unseen;for(int j=0;j<h;++j)if(j!=chosen){if(used>>j&1)active.push_back(j);else unseen.push_back(j);}
  set<vector<Word>> unique_domains;
  for(uint64_t subset=0;subset<(1ull<<active.size());++subset){
   int count=__builtin_popcountll(subset);if(count>5)continue;
   Word oldmask=1u<<chosen;for(int j=0;j<int(active.size());++j)if(subset>>j&1)oldmask|=1u<<active[j];
   for(int fresh=0;fresh<=min(5-count,int(unseen.size()));++fresh){
    Word extra=oldmask;for(int j=0;j<fresh;++j)extra|=1u<<unseen[j];
    if(binary_search(base.begin(),base.end(),extra))continue;
    vector<Word> flat=base;for(Word s:direction)flat.push_back(extra^s);sort(flat.begin(),flat.end());
    if(unique_domains.insert(flat).second)insert(flat);
   }
  }
 }
 void run(){vector<Word> seed;for(int x=0;x<32;++x){Word s=1;for(int t=0;t<5;++t)s|=1u<<(1+2*t+((x>>t)&1));seed.push_back(s);}sort(seed.begin(),seed.end());extend(seed,1);}
};
int main(int argc,char**argv){assert(argc==4);int h=atoi(argv[1]),N=atoi(argv[2]);bool positive=atoi(argv[3]);assert((h==22&&N==124&&!positive)||(h==12&&N==64&&positive));
 auto start=chrono::steady_clock::now();Check check(h,N,positive);check.run();
 cout<<"{\"implementation\":\"A lowest-pivot integer subset domains\",\"controls\":"<<h<<",\"norm\":"<<N<<",\"nodes\":"<<check.calls<<",\"domains\":"<<check.domains<<",\"unsigned_leaves\":"<<check.solutions<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}"<<endl;
 if(positive)return check.solutions?0:2;return check.solutions?2:0;
}

// Acceptance A, newly written: sorted supports, low-pivot closure and profile blocks.
// No proposer, B or previous verifier imports.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <tuple>
#include <vector>
using namespace std;using M=uint32_t;
struct Audit {
 int n,total;M selected,all;bool control;uint64_t visits=0,leaves=0;
 Audit(int v,int norm,M s,bool p):n(v),total(norm),selected(s),all((1u<<v)-1),control(p){assert(total<126);}
 static int pc(M a){return __builtin_popcount(a);}
 void join(const vector<M>& old,vector<M> extra,M completed,int c){
  sort(extra.begin(),extra.end());extra.erase(unique(extra.begin(),extra.end()),extra.end());assert(extra.size()==32);
  for(M t:extra)if(pc(t)>6||pc(t)%2||((t&completed)&&!binary_search(old.begin(),old.end(),t)))return;
  vector<M> result;set_union(old.begin(),old.end(),extra.begin(),extra.end(),back_inserter(result));
  if(result.size()<=total)walk(result,completed|(1u<<c));
 }
 void empty_partial(const vector<M>& terms,M completed,M used,int c){
  M old=used&~completed&~(1u<<c),fresh=all&~used&~(1u<<c);
  vector<int> sizes;vector<M> blocks;
  auto realize=[&](){
   vector<M> out{1u<<c};
   for(M b:blocks){vector<M> next;for(M sub=b;;sub=(sub-1)&b){if(pc(sub)%2!=pc(b)%2)for(M t:out)next.push_back(t|sub);if(!sub)break;}out.swap(next);}
   join(terms,move(out),completed,c);
  };
  auto profile=[&](auto&& self,int index,M oldleft,M yes,M no,tuple<int,M,int,int> prior)->void{
   if(index==sizes.size()){realize();return;}
   int size=sizes[index];
   for(M fixed=oldleft;;fixed=(fixed-1)&oldleft){
    int k=pc(fixed);
    if(k<=size)for(int a=0;a<=min(size-k,pc(yes));++a){int b=size-k-a;if(b>pc(no))continue;
     auto role=make_tuple(size,fixed,a,b);if(index&&sizes[index-1]==size&&role<prior)continue;
     M block=fixed,y=yes,z=no;
     for(int j=0;j<a;++j){M bit=y&-y;y^=bit;block|=bit;}
     for(int j=0;j<b;++j){M bit=z&-z;z^=bit;block|=bit;}
     blocks.push_back(block);self(self,index+1,oldleft^fixed,y,z,role);blocks.pop_back();
    }
    if(!fixed)break;
   }
  };
  auto costs=[&](auto&& self,int remaining,int lower)->void{
   if(!remaining){int needed=0;for(int s:sizes)needed+=s;if(needed<=pc(all&~completed&~(1u<<c)))profile(profile,0,old,fresh&selected,fresh&~selected,{});return;}
   for(int size=lower;size<=remaining+1;++size){sizes.push_back(size);self(self,remaining-(size-1),size);sizes.pop_back();}
  };
  costs(costs,5,2);
 }
 void walk(const vector<M>& terms,M completed){
  if(control&&leaves)return;++visits;array<int,22> count{};M used=0;int loss=0;
  if(terms.size()>total)return;
  for(M t:terms){assert(t);if(pc(t)>6||pc(t)%2)return;used|=t;loss+=6-pc(t);for(int j=0;j<n;++j)count[j]+=(t>>j)&1;}
  if(loss>6*total-32*n)return;
  int need=0;
  for(int j=0;j<n;++j){int e=count[j];if(selected>>j&1){if(e>32)return;}
   if(completed>>j&1){assert(e==32);continue;}
   int target=e<=32||((selected>>j)&1)?32:max(48,((e+1)/2)*2);need+=target-e;
  }
  if(need>6*(total-int(terms.size())))return;
  array<int,22> parent;for(int j=0;j<n;++j)parent[j]=j;
  auto root=[&](int j){while(parent[j]!=j)j=parent[j];return j;};
  for(M t:terms){int first=__builtin_ctz(t);for(int j=0;j<n;++j)if(t>>j&1)parent[root(j)]=root(first);}
  array<M,22> comps{};for(int j=0;j<n;++j)if(used>>j&1)comps[root(j)]|=1u<<j;
  for(M c:comps)if(c&&!(c&~completed)&&c!=all)return;
  if((completed&selected)==selected){++leaves;return;}
  int c=-1;
  for(int j=0;j<n;++j)if((selected>>j&1)&&!(completed>>j&1)&&(used>>j&1))if(c<0||count[j]>=count[c])c=j;
  if(c<0){for(int j=0;j<n;++j)if((selected>>j&1)&&!(completed>>j&1)){c=j;break;}assert(c>=0);empty_partial(terms,completed,used,c);return;}
  vector<M> required;for(M t:terms)if(t>>c&1)required.push_back(t);assert(required.size()>=16);
  M origin=required.back();array<M,22> pivots{};int rank=0;
  for(M t:required){M d=t^origin;while(d){int j=__builtin_ctz(d);if(pivots[j])d^=pivots[j];else{pivots[j]=d;++rank;break;}}}
  if(rank>5)return;assert(rank>=4);
  vector<M> direction{0};for(M d:pivots)if(d){int before=direction.size();for(int j=0;j<before;++j)direction.push_back(direction[j]^d);}
  vector<M> base;for(M d:direction)base.push_back(d^origin);sort(base.begin(),base.end());
  if(rank==5){join(terms,base,completed,c);return;}
  vector<int> old,yes,no;for(int j=0;j<n;++j)if(j!=c){if(used>>j&1)old.push_back(j);else if(selected>>j&1)yes.push_back(j);else no.push_back(j);}
  set<vector<M>> tried;
  auto pick=[&](auto&& self,int index,int degree,M bits)->void{
   for(int a=0;a<=min(5-degree,int(yes.size()));++a)for(int b=0;b<=min(5-degree-a,int(no.size()));++b){
    M extra=bits|(1u<<c);for(int j=0;j<a;++j)extra|=1u<<yes[j];for(int j=0;j<b;++j)extra|=1u<<no[j];
    if(pc(extra)%2||binary_search(base.begin(),base.end(),extra))continue;
    vector<M> coset;for(M d:direction)coset.push_back(d^extra);sort(coset.begin(),coset.end());if(!tried.insert(coset).second)continue;
    vector<M> flat=base;flat.insert(flat.end(),coset.begin(),coset.end());join(terms,move(flat),completed,c);
   }
   if(degree==5)return;
   for(int at=index;at<old.size();++at)self(self,at+1,degree+1,bits|(1u<<old[at]));
  };
  pick(pick,0,0,0);
 }
 void run(){vector<M> seed;for(int j=0;j<32;++j){M t=1;for(int r=0;r<5;++r)t|=1u<<(1+2*r+((j>>r)&1));seed.push_back(t);}sort(seed.begin(),seed.end());walk(seed,1);}
};
int main(int argc,char**argv){assert(argc==5);int n=atoi(argv[1]),N=atoi(argv[2]);M good=strtoul(argv[3],nullptr,10);bool positive=atoi(argv[4]);assert((n==21&&(N==120||N==124)&&!positive)||(n==12&&N==64&&positive));assert(good&1);Audit q(n,N,good,positive);q.run();cout<<"{\"nodes\":"<<q.visits<<",\"unsigned_leaves\":"<<q.leaves<<"}"<<endl;return positive?(q.leaves?0:2):(q.leaves?2:0);}

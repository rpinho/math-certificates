// Exact verifier B: conditional parity-block enumeration. No search/A
// imports, no global minimum-template table, no numerical arithmetic.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
using namespace std;
using Block=uint32_t;
using Tensor=array<Block,16>;
int n, norm, max_deficit;
Block required_good, universe;
bool forbid_homogeneous;
bool first_unresolved_only=false;
vector<Block> first_unresolved_terms;
Block first_unresolved_done=0;
uint64_t nodes=0, final_nodes=0, dead_ends=0, independent_residuals=0, conditional_domains=0, flat_residuals=0;
map<pair<int,vector<Block>>,vector<Tensor>> memo;
inline int card(Block x){return __builtin_popcount(x);}
vector<Block> local_masks(Block b){
 if(card(b)==1)return {0,b};
 vector<Block> answer;
 // Enumerate all subsets of the actual block, in binary order. Even
 // blocks select odd subsets; odd blocks select even subsets.
 for(Block q=b;;q=(q-1)&b){if(card(q)%2!=(card(b)%2))answer.push_back(q);if(q==0)break;}
 return answer;
}
Tensor multiply_blocks(int distinguished,const vector<Block>& blocks){
 vector<Block> terms{Block(1)<<distinguished};
 for(Block block:blocks){
  vector<Block> next;for(Block a:terms)for(Block b:local_masks(block))next.push_back(a|b);terms.swap(next);
 }
 assert(terms.size()==16);sort(terms.begin(),terms.end());Tensor t;copy(terms.begin(),terms.end(),t.begin());return t;
}
vector<Tensor> construct(int distinguished,const vector<Block>& demanded){
 ++conditional_domains;
 if(demanded.size()>16)return {};
 Block must=0;for(Block term:demanded)must|=term&~(Block(1)<<distinguished);
 array<vector<Block>,6> allowed;
 vector<int> coords;for(int j=0;j<n;++j)if(j!=distinguished)coords.push_back(j);
 for(int size=1;size<=5;++size){
  vector<int> picks(size);for(int i=0;i<size;++i)picks[i]=i;
  if(size>(int)coords.size())continue;
  do{
   Block block=0;for(int i:picks)block|=Block(1)<<coords[i];
   bool valid=true;
   if(size>1)for(Block term:demanded)if(card(term&block)%2==size%2){valid=false;break;}
   if(valid)allowed[size].push_back(block);
   int at=size-1;while(at>=0&&picks[at]==(int)coords.size()-size+at)--at;
   if(at<0)break;
   ++picks[at];for(int j=at+1;j<size;++j)picks[j]=picks[j-1]+1;
  }while(true);
 }
 vector<Tensor> patterns;
 vector<int> sizes;vector<Block> chosen;
 // Enumerate degree-cost partitions recursively, distinguishing point
 // factors (size one, cost one) from size-two blocks (also cost one).
 auto partition=[&](auto&& self,int remaining,int smallest_size)->void{
  if(!remaining){
   if(forbid_homogeneous&&sizes==vector<int>({2,2,2,2}))return;
   int capacity=0;for(int size:sizes)capacity+=size;
   if(card(must)>capacity)return;
   auto put=[&](auto&& recurse,int at,Block used)->void{
    int left=0;for(int k=at;k<(int)sizes.size();++k)left+=sizes[k];
    if(card(must&~used)>left)return;
    if(at==(int)sizes.size()){
     if(must&~used)return;
     Tensor tensor=multiply_blocks(distinguished,chosen);
     for(Block s:demanded)if(!binary_search(tensor.begin(),tensor.end(),s))return;
     patterns.push_back(tensor);return;
    }
    int size=sizes[at];
    for(Block block:allowed[size]){
     if(used&block)continue;
     if(at&&size==sizes[at-1]&&block<=chosen.back())continue;
     chosen.push_back(block);recurse(recurse,at+1,used|block);chosen.pop_back();
    }
   };
   put(put,0,0);return;
  }
  for(int size=smallest_size;size<=5;++size){
   int cost=max(1,size-1);if(cost>remaining)continue;
   sizes.push_back(size);self(self,remaining-cost,size);sizes.pop_back();
  }
 };
 partition(partition,4,1);
 sort(patterns.begin(),patterns.end());patterns.erase(unique(patterns.begin(),patterns.end()),patterns.end());
 return patterns;
}
const vector<Tensor>& domain(int distinguished,const vector<Block>& demanded){
 auto key=make_pair(distinguished,demanded);auto found=memo.find(key);
 if(found!=memo.end())return found->second;
 // Map references remain stable on insertion; no eviction occurs while a
 // recursive caller could be iterating a domain.
 return memo.emplace(move(key),construct(distinguished,demanded)).first->second;
}
struct State{
 vector<Block> terms;
 array<int,32> energies{};
 int deficit=0;
 explicit State(vector<Block> t):terms(move(t)){
  for(Block s:terms){deficit+=5-card(s);for(int j=0;j<n;++j)if(s&(Block(1)<<j))++energies[j];}
 }
};
int binary_rank(vector<uint64_t> rows){
 array<uint64_t,64> pivots{};int rank=0;
 for(uint64_t row:rows){
  while(row){int bit=63-__builtin_clzll(row);if(pivots[bit])row^=pivots[bit];else{pivots[bit]=row;++rank;break;}}
 }
 return rank;
}
bool minimum_flat(const State& state,Block done){
 if(state.terms.size()!=32||norm<=32||norm>=64)return false;
 vector<uint64_t> differences;for(Block s:state.terms)differences.push_back(s^state.terms[0]);
 if(binary_rank(differences)!=5)return false;
 vector<uint64_t> constraints;
 for(int j=0;j<n;++j)if(done&(Block(1)<<j)){
  array<uint64_t,32> pivots{},combinations{};
  for(int i=0;i<32;++i)if(state.terms[i]&(Block(1)<<j)){
   uint64_t v=(uint64_t(state.terms[i])<<1)|1,relation=1ull<<i;
   while(v){int bit=63-__builtin_clzll(v);if(pivots[bit]){v^=pivots[bit];relation^=combinations[bit];}else{pivots[bit]=v;combinations[bit]=relation;break;}}
   if(!v)constraints.push_back(relation);
  }
 }
 int rank=binary_rank(constraints);assert(rank<=26);return rank==26;
}
void fill(const State&,Block,bool);
void extend_at(const State& state,Block done,int coordinate,bool residual){
 vector<Block> demanded;for(Block term:state.terms)if(term&(Block(1)<<coordinate))demanded.push_back(term);
 const auto& candidates=domain(coordinate,demanded);
 for(const Tensor& tensor:candidates){
  bool permitted=true;
  for(Block term:tensor)if((term&done)&&!binary_search(state.terms.begin(),state.terms.end(),term)){permitted=false;break;}
  if(!permitted)continue;
  vector<Block> combined;set_union(state.terms.begin(),state.terms.end(),tensor.begin(),tensor.end(),back_inserter(combined));
  if((int)combined.size()>norm)continue;
  State next(move(combined));
  if(next.deficit<=max_deficit)fill(next,done|(Block(1)<<coordinate),residual);
 }
}
void fill(const State& s,Block done,bool residual){
 if(first_unresolved_only&&dead_ends)return;
 ++nodes;if(residual)++final_nodes;
 int remainder=norm-s.terms.size();if(remainder<0||s.deficit>max_deficit)return;
 if(residual){
  // Check every still-unfinished coordinate against both possible
  // partial-energy ranges. A range below 24 forces minimum energy 16.
  int coordinate=-1;
  for(int j=0;j<n;++j){
   int current=s.energies[j];if(current+remainder<16)return;
   if(done&(Block(1)<<j)){if(current!=16)return;continue;}
   if(current+remainder<24){
    if(current>16)return;
    if(coordinate<0||current>s.energies[coordinate])coordinate=j;
   }
  }
  if(coordinate>=0){extend_at(s,done,coordinate,true);return;}
  if(minimum_flat(s,done)){++flat_residuals;return;}
  Block variables=0;bool odd=true;
  for(Block term:s.terms){variables|=term;if(card(term)%2==0)odd=false;}
  if(remainder>0&&(variables&~done)==0&&odd&&s.terms.size()<256){++independent_residuals;return;}
  if(!dead_ends){first_unresolved_terms=s.terms;first_unresolved_done=done;}
  ++dead_ends;return;
 }
 int missing=0,needed=0;
 for(int j=0;j<n;++j){
  if(required_good&(Block(1)<<j)){
   if(s.energies[j]>16)return;
   if(s.energies[j]==0)++missing;
  }else needed+=max(0,16-s.energies[j]);
 }
 if(needed>card(universe^required_good)*remainder)return;
 if((missing>=2&&remainder<24)||(missing>=1&&remainder<16))return;
 if(done==required_good){fill(s,done,true);return;}
 int coordinate=-1;
 for(int j=n-1;j>=0;--j)if((required_good&(Block(1)<<j))&&!(done&(Block(1)<<j)))
  if(coordinate<0||s.energies[j]>s.energies[coordinate])coordinate=j;
 assert(coordinate>=0);extend_at(s,done,coordinate,false);
}
int main(int argc,char** argv){
 if(argc==4&&string(argv[1])=="--flat-control"){
  ifstream file(argv[2]);assert(file.good());Block done;int count;
  file>>n>>norm>>done>>count;vector<Block> terms;
  for(int i=0;i<count;++i){Block term;file>>term;terms.push_back(term);}
  string extra;assert(!(file>>extra));State state(move(terms));
  bool actual=minimum_flat(state,done);cout<<"B flat control "<<actual<<endl;
  return actual==bool(stoi(argv[3]))?0:2;
 }
 assert(argc==3||argc==4);ifstream input(argv[1]);assert(input.good());
 int nh,number_of_blocks;input>>n>>norm>>required_good>>nh>>number_of_blocks;
 assert(n>=13&&n<=17&&(norm==56||norm==48));assert(n==13||norm==56);assert(nh==0||nh==1);
 universe=(Block(1)<<n)-1;assert((required_good&1)&&!(required_good&~universe));forbid_homogeneous=nh;
 vector<Block> seed_blocks;Block used=1;int cost=0;
 for(int i=0;i<number_of_blocks;++i){Block b;input>>b;assert(b&&!(b&used)&&!(b&~universe));used|=b;cost+=max(1,card(b)-1);seed_blocks.push_back(b);}
 assert(cost==4);string extra;assert(!(input>>extra));
 max_deficit=5*norm-16*n;
 auto started=chrono::steady_clock::now();
 if(argc==4&&string(argv[3])=="--catalogue"){
  const auto& all=domain(0,{});cout<<"B templates "<<all.size()<<endl;return 0;
 }
 first_unresolved_only=argc==4&&string(argv[3])=="--first-unresolved";
 Tensor seed=multiply_blocks(0,seed_blocks);State initial(vector<Block>(seed.begin(),seed.end()));fill(initial,1,false);
 ofstream output(argv[2]);output<<"{\"implementation\":\"B conditional parity partitions\",\"n\":"<<n<<",\"norm\":"<<norm<<",\"goodbits\":"<<required_good<<",\"nonhomogeneous_only\":"<<(forbid_homogeneous?"true":"false")<<",\"nodes\":"<<nodes<<",\"closure_nodes\":"<<final_nodes<<",\"conditional_domains\":"<<conditional_domains<<",\"unresolved\":"<<dead_ends<<",\"odd_residual_rejections\":"<<independent_residuals<<",\"flat_residual_rejections\":"<<flat_residuals<<",\"first_unresolved_done\":"<<first_unresolved_done<<",\"first_unresolved_terms\":[";
 for(int j=0;j<(int)first_unresolved_terms.size();++j)output<<(j?",":"")<<first_unresolved_terms[j];
 output<<"],\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-started).count()<<"}\n";
 cout<<"B "<<n<<" good "<<required_good<<" nodes "<<nodes<<" unresolved "<<dead_ends<<endl;
 return dead_ends?2:0;
}

// Separately written (same agent), directed scalar rectangle verifier.
// Component transitions derived from this job's coefficient verifier; credited Kesten, Jensen, Enting, Vit Planocka.
// No production transition source or coefficient arithmetic imported. Each local step is
// determined by vertex degrees and explicit connected-component identities.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <unordered_map>
#include <vector>
static int H,N,SPAN,MINSPAN;static bool lastcol;static std::vector<uint32_t> primes;
[[noreturn]]static void reject(const char*s){std::cerr<<"REJECT:"<<s<<"\n";std::exit(2);}
struct Edge{uint64_t key;int degree;};struct Update{Edge edge[3];int num=0,done=0;};
static int get(uint64_t code,int i){return int((code>>(2*i))&3);}
static Update advance(uint64_t key,int row){
 int tags[32]={},open[32],top=0,nextid=0,terminal[32]={},labels[32]={};
 int end=(key>>(2*(H+2)))&1;
 for(int i=0;i<H+2;i++){
  int pos=i<row?i:(i==row?H+1:i-1),v=get(key,pos);
  if(v==1){tags[i]=++nextid;open[top++]=nextid;}
  else if(v==2){if(!top)reject("BRACKET");tags[i]=open[--top];}
  else if(v==3){tags[i]=++nextid;terminal[nextid]=1;}
 }
 if(top)reject("BRACKET");if(row==0&&tags[0])reject("BOTTOM_UP_EDGE");
 int left=tags[row+1],down=tags[row];Update out;
 for(int right=0;right<2;right++)for(int up=0;up<2;up++){
  if((row==H&&up)||(lastcol&&right))continue;
  int deg=(left!=0)+(down!=0)+right+up,newend=end;
  bool add_end=deg==1;
  if(deg==1){if(!lastcol||end)continue;newend=1;}
  else if(deg!=0&&deg!=2)continue;
  if(left&&down&&left==down)continue;
  std::copy(tags,tags+H+2,labels);labels[row]=labels[row+1]=0;
  int id=left?left:down;int terms=add_end+(left?terminal[left]:0)+(down?terminal[down]:0);
  if(deg&&!id)id=nextid+1;
  if(left&&down)for(int j=0;j<H+2;j++)if(labels[j]==down)labels[j]=id;
  if(right)labels[row]=id;if(up)labels[row+1]=id;
  int remaining=0,component_stubs=0,count[32]={},first[32]={};
  for(int j=0;j<H+2;j++){remaining+=labels[j]!=0;component_stubs+=id&&labels[j]==id;if(labels[j])count[labels[j]]++;}
  if(deg&&!component_stubs){if(terms==2&&remaining==0&&newend)out.done++;continue;}
  if(deg&&terms>1)continue;
  uint64_t encoded=uint64_t(newend)<<(2*(H+2));int bracket[32],depth=0;
  for(int j=0;j<H+2;j++){
   int id2=labels[j],v=0;
   if(id2){if(count[id2]==1)v=3;else if(count[id2]==2){if(!first[id2]){first[id2]=1;v=1;bracket[depth++]=id2;}else{v=2;if(!depth||bracket[--depth]!=id2)reject("NONPLANAR_COMPONENT");}}else reject("COMPONENT_CARDINALITY");}
   int pos=j<=row?j:(j==row+1?H+1:j-1);encoded|=uint64_t(v)<<(2*pos);
  }
  if(depth)reject("OUTPUT_BRACKET");if(out.num>=3)reject("LOCAL_CAPACITY");out.edge[out.num++]={encoded,right+up};
 }
 return out;
}

using U=unsigned __int128;
struct Bounds{U lower=0,upper=0;};
struct KeyHash{size_t operator()(uint64_t n)const{n^=n>>33;n*=0xff51afd7ed558ccdULL;n^=n>>33;return n;}};
using StateValues=std::unordered_map<uint64_t,Bounds,KeyHash>;
static constexpr uint64_t point=51081913;
static int crossing_cap;
static std::string decimal(U x){if(!x)return "0";std::string s;while(x){s+=char('0'+x%10);x/=10;}std::reverse(s.begin(),s.end());return s;}
static U directed_product(U x,int edges,bool ceiling){
 if(!edges)return x;
 if(edges<0||edges>2||x>=(U(1)<<107))reject("VALUE_CAPACITY");
 int s=27*edges;uint64_t q=edges==1?point:point*point;
 U mask=(U(1)<<s)-1, low=(x&mask)*q;
 // Both products fit128 bits: the high product is below2^107,
 // and the low product is below2^108. This is a different quotient
 // decomposition from the search producer's three-limb product.
 U result=(x>>s)*q+(low>>s);
 if(ceiling&&(low&mask)){if(result==~U(0))reject("CEILING_CAPACITY");++result;}
 return result;
}
static void accumulate(Bounds&to,const Bounds&from,int edges){
 U l=directed_product(from.lower,edges,false),u=directed_product(from.upper,edges,true);
 if(to.lower>~U(0)-l||to.upper>~U(0)-u)reject("SUM_CAPACITY");to.lower+=l;to.upper+=u;
}
static StateValues propagate(const StateValues&input,bool closing,Bounds&answer){
 lastcol=closing;const StateValues*current=&input;StateValues owned;
 for(int row=0;row<=H;++row){
  StateValues next;next.reserve(current->size()*2+16);
  for(const auto&entry:*current){auto u=advance(entry.first,row);
   for(int k=0;k<u.done;++k)accumulate(answer,entry.second,0);
   for(int k=0;k<u.num;++k){
    if(!closing&&crossing_cap<H+1){int c=0;for(int j=0;j<=row;++j)c+=get(u.edge[k].key,j)!=0;if(c>crossing_cap)continue;}
    accumulate(next[u.edge[k].key],entry.second,u.edge[k].degree);
   }
  }owned.swap(next);current=&owned;
 }
 if(!closing)for(auto it=owned.begin();it!=owned.end();){int c=0;for(int j=0;j<=H;++j)c+=get(it->first,j)!=0;if(c<3||c>crossing_cap||!(c&1))it=owned.erase(it);else ++it;}
 return owned;
}
static Bounds evaluate(int height){
 H=height;StateValues states;
 for(int y=0;y<=H;++y)states[uint64_t(3)<<(2*y)]={U(point)<<69,U(point)<<69};
 Bounds total;
 for(int col=1;col<=SPAN;++col){
  if(col>=MINSPAN){auto rest=propagate(states,true,total);if(!rest.empty())reject("UNFINISHED_TERMINAL");}
  if(col<SPAN)states=propagate(states,false,total);
  std::cerr<<"point-verifier height="<<H<<" column="<<col<<" states="<<states.size()<<"\n";
 }
 return total;
}
int main(int argc,char**argv){
 if(argc!=6)return 1;int W=std::stoi(argv[1]);MINSPAN=std::stoi(argv[2]);SPAN=std::stoi(argv[3]);crossing_cap=std::stoi(argv[4]);
 if(W<1||W>28||MINSPAN<2||SPAN<MINSPAN||SPAN>133||crossing_cap<3||crossing_cap>99)reject("PARAMETERS");
 Bounds a=evaluate(W),b=evaluate(W-1);if(a.upper<b.lower)reject("NORMALIZED_INTERVAL");
 U l=a.lower>b.upper?a.lower-b.upper:0,u=a.upper-b.lower;
 std::ofstream f(argv[5]);if(!f)reject("OUTPUT_OPEN");
 f<<"{\"status\":\"COMPLETE_SEPARATE_SAME_AGENT_POINT_REPLAY\",\"W\":"<<W<<",\"span_min\":"<<MINSPAN<<",\"span_max\":"<<SPAN<<",\"crossing_cap\":"<<crossing_cap<<",\"M\":"<<point<<",\"S\":96,\"num_lo\":\""<<decimal(l)<<"\",\"num_hi\":\""<<decimal(u)<<"\"}\n";
}

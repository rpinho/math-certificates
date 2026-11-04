// Referee's direct normalized irreducible enumeration. It records a bottom-
// contact bit instead of subtracting two frames, and retains terminal identity.
#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <unordered_map>
#include <vector>
#ifdef FAST_RECT
using I=unsigned __int128;
const int SCALE=112;
#else
using I=boost::multiprecision::uint256_t;
const int SCALE=160;
#endif
using Key=unsigned __int128;
struct Hash {size_t operator()(Key k)const {
 uint64_t a=k,b=k>>64;a^=b*0x9e3779b97f4a7c15ULL;
 a^=a>>30;a*=0xbf58476d1ce4e5b9ULL;a^=a>>27;a*=0x94d049bb133111ebULL;return a^(a>>31);
}};
struct Value {I lo=0,hi=0;};
struct Move {Key dest;int power;};
struct Moves {std::array<Move,4>edges;int count=0,done=0;};
int W,lowspan,highspan,cap,shift;
const uint64_t M=51081913;
using Table=std::unordered_map<Key,Value,Hash>;
int label(Key k,int i){return (k>>(4*i))&15;}
Key encode(std::array<int,32> a,int flags) {
 int ren[16]={},next=1;Key k=Key(flags)<<shift;
 for(int i=0;i<W+2;++i){
  if(a[i] && a[i]<14){if(!ren[a[i]])ren[a[i]]=next++;a[i]=ren[a[i]];}
  k|=Key(a[i])<<(4*i);
 }return k;
}
Moves transitions(Key key,int row,bool closing) {
 std::array<int,32>a{};for(int i=0;i<W+2;++i)a[i]=label(key,i);
 int flags=key>>shift,l=a[row],d=a[W+1],in=(l!=0)+(d!=0);Moves ans;
 for(int right=0;right<=1;++right)for(int up=0;up<=1;++up){
  if((closing && right)||(row==W && up))continue;
  int out=right+up,degree=in+out;
  bool terminal=degree==1;
  if(terminal){if(!closing || (flags&1))continue;}
  else if(degree!=0 && degree!=2)continue;
  auto z=a;z[row]=z[W+1]=0;int nf=flags;
  if(terminal)nf|=1;if(row==0 && degree)nf|=2;
  int lab=0;bool done=false;
  if(!degree){}
  else if(terminal){
   if(out)lab=15;
   else {
    int q=l?l:d;
    if(q>=14)done=true;
    else {bool mate=false;for(int i=0;i<W+2;++i)if(z[i]==q){z[i]=15;mate=true;}
     if(!mate)throw std::runtime_error("missing mate");}
   }
  } else if(in==0){
   lab=1;for(int i=0;i<W+2;++i)if(z[i]<14)lab=std::max(lab,z[i]+1);
   if(lab>=14)throw std::runtime_error("component capacity");
  } else if(in==1)lab=l?l:d;
  else {
   if(l==d)continue;
   if(l>=14 && d>=14)done=true;
   else {int keep=l>=14?l:(d>=14?d:l),drop=keep==l?d:l;
    for(int i=0;i<W+2;++i)if(z[i]==drop)z[i]=keep;}
  }
  if(done){
   bool empty=true;for(int i=0;i<W+2;++i)if(z[i])empty=false;
   if(empty && nf==3)ans.done++;
   continue;
  }
  if(right)z[row]=lab;if(up)z[W+1]=lab;
  if(!closing){int crossing=0;for(int j=0;j<=row;++j)crossing+=z[j]!=0;
   if(crossing>cap)continue;}
  if(ans.count>=4)throw std::runtime_error("moves capacity");
  ans.edges[ans.count++]={encode(z,nf),out};
 }
 return ans;
}
I weight(I x,int power,bool upper){
#ifdef FAST_RECT
 if(x>=(I(1)<<124))throw std::runtime_error("input capacity");
 if(!power)return x;
 int bits=27*power;uint64_t m=power==1?M:M*M;I mask=(I(1)<<bits)-1;
 I low=(x&mask)*m,high=(x>>bits)*m;
 return high+(low>>bits)+I(upper && ((low&mask)!=0));
#else
 if(x>=(I(1)<<192))throw std::runtime_error("input capacity");
 if(!power)return x;
 int bits=27*power;uint64_t m=power==1?M:M*M;
 I p=x*m,mask=(I(1)<<bits)-1;
 return (p>>bits)+I(upper && ((p&mask)!=0));
#endif
}
std::string decimal(I x){
#ifdef FAST_RECT
 if(!x)return "0";std::string s;while(x){s+=char('0'+x%10);x/=10;}
 std::reverse(s.begin(),s.end());return s;
#else
 return x.convert_to<std::string>();
#endif
}
void add(Value&to,const Value&from,int power){
 I lo=weight(from.lo,power,false),hi=weight(from.hi,power,true);
 if(to.hi>~I(0)-hi || to.lo>~I(0)-lo)throw std::runtime_error("sum overflow");
 to.lo+=lo;to.hi+=hi;
}
Table column(const Table&input,bool closing,Value&sum){
 const Table*current=&input;Table owned;
 for(int row=0;row<=W;++row){
  Table next;next.reserve(current->size()*2+10);
  for(auto&entry:*current){
   auto moves=transitions(entry.first,row,closing);
   for(int i=0;i<moves.done;++i)add(sum,entry.second,0);
   for(int i=0;i<moves.count;++i)add(next[moves.edges[i].dest],entry.second,moves.edges[i].power);
  }
  owned.swap(next);current=&owned;
 }
 if(!closing)for(auto it=owned.begin();it!=owned.end();){
  int crossings=0;for(int i=0;i<=W;++i)crossings+=label(it->first,i)!=0;
  if(crossings<3 || crossings>cap || crossings%2==0)it=owned.erase(it);else ++it;
 }
 return owned;
}
int main(int argc,char**argv){try{
 if(argc!=6)throw std::runtime_error("usage: rectangle range minspan maxspan cap output");
 W=std::stoi(argv[1]);lowspan=std::stoi(argv[2]);highspan=std::stoi(argv[3]);cap=std::stoi(argv[4]);shift=4*(W+2);
 if(W<1||W>28||lowspan<2||highspan<lowspan||cap<3||cap>5)throw std::runtime_error("parameters");
 Table states;
 for(int y=0;y<=W;++y){Key k=Key(14)<<(4*y);if(y==0)k|=Key(2)<<shift;
  states[k]={I(M)<<(SCALE-27),I(M)<<(SCALE-27)};
 }
 Value total;std::vector<Value>byspan(highspan+1);auto start=std::chrono::steady_clock::now();
 for(int col=1;col<=highspan;++col){
  if(col>=lowspan){Value term;auto rest=column(states,true,term);
   if(!rest.empty())throw std::runtime_error("terminal leaves frontier");
   byspan[col]=term;add(total,term,0);
  }
  if(col<highspan){Value impossible;states=column(states,false,impossible);
   if(impossible.hi!=0)throw std::runtime_error("early completion");}
  std::cerr<<"column="<<col<<" states="<<states.size()<<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"\n";
 }
 std::ofstream out(argv[5]);out<<"{\"W\":"<<W<<",\"minspan\":"<<lowspan<<",\"maxspan\":"<<highspan<<",\"cap\":"<<cap<<",\"scale\":"<<SCALE
   <<",\"num_lo\":\""<<decimal(total.lo)<<"\",\"num_hi\":\""<<decimal(total.hi)<<"\",\"per_span\":[";
 for(int h=lowspan;h<=highspan;++h){if(h!=lowspan)out<<",";out<<"{\"h\":"<<h<<",\"lo\":\""<<decimal(byspan[h].lo)<<"\",\"hi\":\""<<decimal(byspan[h].hi)<<"\"}";}out<<"]}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}

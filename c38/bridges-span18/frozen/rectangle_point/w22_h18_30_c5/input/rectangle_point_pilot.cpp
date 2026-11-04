// Multiple disjoint spans, direct restricted finite grammar.
// Exact restricted irreducible-bridge polynomial search.
// Boundary cases adapted from Vit Planocka's MIT transfer kernel; Kesten/Jensen.
// Geometry differs: sweep along bridge span, cap transverse height, forbid
// singly crossed interior cuts. The source baseline generator remains credited.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <unordered_map>
#include <vector>

struct Hash{size_t operator()(uint64_t x)const{x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;return x;}};
using U=unsigned __int128;struct Value{U lo=0,hi=0;};using Bank=std::unordered_map<uint64_t,Value,Hash>;static int CAP;static const uint64_t M=51081913;
static int H,SPAN,N,MINSPAN;static bool final_column;
struct Move{uint64_t code;int length;};struct Choices{Move move[3];int count=0,completed=0;};
static int lab(uint64_t x,int i){return int((x>>(2*i))&3);}
static uint64_t pack(const int*e,int v,int end){uint64_t x=uint64_t(end)<<(2*(H+2));for(int j=0;j<=H;j++)x|=uint64_t(e[j])<<(2*j);return x|(uint64_t(v)<<(2*(H+1)));}
static void die(const char*s){std::cerr<<"REJECT:"<<s<<"\n";std::exit(2);}
static Choices step(uint64_t code,int row){
 int e[32],v=lab(code,H+1),end=int(code>>(2*(H+2)))&1;
 for(int j=0;j<=H;j++)e[j]=lab(code,j);int a=e[row],b=v;
 if(row==0&&v)die("ROW_ZERO_VERTICAL");
 int seq[32],mate[32],st[32],top=0;
 for(int i=0;i<H+2;i++){seq[i]=i<row?e[i]:(i==row?v:e[i-1]);mate[i]=-1;if(seq[i]==1)st[top++]=i;else if(seq[i]==2){if(!top)die("BRACKET");int j=st[--top];mate[i]=j;mate[j]=i;}}
 if(top)die("BRACKET");Choices out;
 auto emit=[&](int*ee,int vv,int en,int len){if(out.count>=3)die("LOCAL_MOVE_COUNT");out.move[out.count++]={pack(ee,vv,en),len};};
 auto put=[&](int*ee,int pos,int value){if(pos<0||pos>H+1||pos==row)die("MATE");if(pos<row)ee[pos]=value;else ee[pos-1]=value;};
 auto sole=[&](int p,int q){for(int i=0;i<H+2;i++)if(i!=p&&i!=q&&seq[i])return false;return true;};
 int z[32];
 if(!a&&!b){
  emit(e,0,end,0);
  if(!final_column&&row<H){std::copy(e,e+H+1,z);z[row]=1;emit(z,2,end,2);}
  if(final_column&&!end&&row<H){emit(e,3,1,1);}
 }else if(bool(a)!=bool(b)){
  int t=a?a:b,pos=a?row+1:row;
  if(!final_column){std::copy(e,e+H+1,z);z[row]=t;emit(z,0,end,1);}
  if(row<H){std::copy(e,e+H+1,z);z[row]=0;emit(z,t,end,1);}
  if(final_column&&!end){
   if(t==3){if(sole(pos,-1))out.completed++;}
   else{std::copy(e,e+H+1,z);z[row]=0;put(z,mate[pos],3);emit(z,0,1,0);}
  }
 }else{
  bool pa=a==1||a==2,pb=b==1||b==2;
  if(pa&&pb){
   if(mate[row+1]!=row){int p=mate[row+1],q=mate[row];std::copy(e,e+H+1,z);z[row]=0;put(z,std::min(p,q),1);put(z,std::max(p,q),2);emit(z,0,end,0);}
  }else if(a==3&&b==3){if(final_column&&end&&sole(row,row+1))out.completed++;}
  else{std::copy(e,e+H+1,z);z[row]=0;put(z,mate[pa?row+1:row],3);emit(z,0,end,0);}
 }
 return out;
}
static std::string dec(U x){if(!x)return "0";std::string s;while(x){s+=char('0'+x%10);x/=10;}std::reverse(s.begin(),s.end());return s;}
static U weight(U n,int k,bool up){
 if(!k)return n;if(n>=(U(1)<<107))die("POINT_VALUE_OVERFLOW");
 uint64_t mult=k==1?M:M*M;unsigned shift=27*k;
 U a=U(uint64_t(n))*mult,b=U(uint64_t(n>>64))*mult,c=(a>>64)+uint64_t(b);
 uint64_t p0=uint64_t(a),p1=uint64_t(c),p2=uint64_t(b>>64)+uint64_t(c>>64);
 if(p2>>shift)die("POINT_PRODUCT_OVERFLOW");U z=(U((p1>>shift)|(p2<<(64-shift)))<<64)|((p0>>shift)|(p1<<(64-shift)));
 if(up&&(p0&((1ULL<<shift)-1))){if(z==~U(0))die("POINT_CEILING_OVERFLOW");++z;}return z;
}
static void add(Value&d,Value v,int k){U a=weight(v.lo,k,false),b=weight(v.hi,k,true);if(d.lo>~U(0)-a||d.hi>~U(0)-b)die("POINT_SUM_OVERFLOW");d.lo+=a;d.hi+=b;}
static Bank column(const Bank&bank,bool closing,Value&result){
 final_column=closing;const Bank*current=&bank;Bank owned;
 for(int row=0;row<=H;row++){
  Bank next;next.reserve(current->size()*2+16);
  for(auto&item:*current){auto moves=step(item.first,row);
   for(int j=0;j<moves.completed;j++)add(result,item.second,0);
   for(int j=0;j<moves.count;j++){
    auto key=moves.move[j].code;
    if(!closing&&CAP<H+1){int count=0;for(int y=0;y<=row;y++)count+=lab(key,y)!=0;if(count>CAP)continue;}
    add(next[key],item.second,moves.move[j].length);
   }
  }owned.swap(next);current=&owned;
 }
 if(!closing)for(auto it=owned.begin();it!=owned.end();){int c=0;for(int y=0;y<=H;y++)c+=lab(it->first,y)!=0;if(c<3||c>CAP||!(c&1))it=owned.erase(it);else ++it;}
 return owned;
}
static Value count(){
 Bank bank;for(int y=0;y<=H;y++){int e[32]={};e[y]=3;auto&p=bank[pack(e,0,0)];p.lo=p.hi=U(M)<<69;}
 Value result;
 for(int col=1;col<=SPAN;col++){
  if(col>=MINSPAN){auto done=column(bank,true,result);if(!done.empty())die("TERMINAL_UNFINISHED");}
  if(col<SPAN)bank=column(bank,false,result);
  std::cerr<<"point height="<<H<<" column="<<col<<" states="<<bank.size()<<"\n";
 }
 return result;
}
int main(int argc,char**argv){if(argc!=6)return 1;int W=std::stoi(argv[1]);MINSPAN=std::stoi(argv[2]);SPAN=std::stoi(argv[3]);CAP=std::stoi(argv[4]);if(W<1||W>28||MINSPAN<2||SPAN<MINSPAN||SPAN>133||CAP<3||CAP>99)die("PARAMETERS");
 H=W;auto a=count();H=W-1;auto b=count();std::ofstream f(argv[5]);if(!f)die("OUTPUT_OPEN");
 U lo=a.lo>b.hi?a.lo-b.hi:0;U hi=a.hi>b.lo?a.hi-b.lo:0;
 f<<"{\"status\":\"SEARCH_ONLY_UNVERIFIED_POINT_PILOT\",\"W\":"<<W<<",\"span_min\":"<<MINSPAN<<",\"span_max\":"<<SPAN<<",\"crossing_cap\":"<<CAP<<",\"M\":"<<M<<",\"S\":96,\"num_lo\":\""<<dec(lo)<<"\",\"num_hi\":\""<<dec(hi)<<"\"}\n";
}

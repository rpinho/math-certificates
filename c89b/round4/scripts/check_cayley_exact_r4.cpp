// Separately written (same agent) exact binary Cayley counter, with arbitrary precision
// throughout. Fix the first part to zero using translation transitivity and
// enumerate all weakly ordered remaining four parts with their multiplicities.
#include <gmpxx.h>
#include <vector>
#include <iostream>
#include <stdexcept>
using namespace std;using Z=mpz_class;
static int n;static long D;static int color,v[4];static vector<long>q;static Z total[2];
long probability(int x){return color?D-q[x]:q[x];}
void extend(int count,int first,const Z&product){
 if(count==4){int div=1,run=1;for(int i=1;i<4;i++){if(v[i]==v[i-1])run++;else{for(int t=2;t<=run;t++)div*=t;run=1;}}for(int t=2;t<=run;t++)div*=t;total[color]+=product*(24/div);return;}
 for(int x=first;x<n;x++){long p=probability(x);if(!p)continue;Z next=product*p;bool possible=true;for(int i=0;i<count;i++){long a=probability(x^v[i]);if(!a){possible=false;break;}next*=a;}if(possible){v[count]=x;extend(count+1,x,next);}}
}
int main(){try{
 if(!(cin>>n>>D)||n<2||n>1024||(n&(n-1))||D<1||D>1000000000L)throw runtime_error("kernel header");q.resize(n);for(long&x:q)if(!(cin>>x)||x<0||x>D)throw runtime_error("kernel probability");string extra;if(cin>>extra)throw runtime_error("extra kernel input");for(color=0;color<2;color++)extend(0,0,Z(1));Z a,b;mpz_ui_pow_ui(a.get_mpz_t(),D,10);mpz_ui_pow_ui(b.get_mpz_t(),n,4);mpq_class result(total[0]+total[1],a*b);result.canonicalize();cout<<result.get_num().get_str()<<"\n"<<result.get_den().get_str()<<"\n"<<total[0].get_str()<<"\n"<<total[1].get_str()<<"\n";return 0;
 }catch(exception&e){cerr<<"REJECT "<<e.what()<<"\n";return 1;}}

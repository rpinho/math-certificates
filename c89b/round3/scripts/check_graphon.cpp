// Exact step-graphon count, separately written from the search.
// Partitions ordered samples by distinct support and positive occupancy vector.
#include <gmpxx.h>
#include <vector>
#include <iostream>
#include <stdexcept>
#include <algorithm>
using namespace std;using Z=mpz_class;
int n,col,chosen[5],occ[5];long D;vector<long>R,mass;Z total[2];long fact[6]={1,1,2,6,24,120};
long edge(int u,int v){long a=R[u*n+v];return col?D-a:a;}
Z power(long v,int e){Z r;mpz_ui_pow_ui(r.get_mpz_t(),v,e);return r;}
void value(int k){
 Z term=1;long divisor=1;for(int i=0;i<k;i++){int v=chosen[i],m=occ[i];divisor*=fact[m];term*=power(mass[v],m);if(m>1)term*=power(edge(v,v),m*(m-1)/2);for(int j=0;j<i;j++)term*=power(edge(v,chosen[j]),m*occ[j]);if(term==0)return;}
 total[col]+=term*(120/divisor);
}
void composition(int k,int pos,int remaining){if(pos==k-1){occ[pos]=remaining;value(k);return;}for(int x=1;x<=remaining-(k-pos-1);x++){occ[pos]=x;composition(k,pos+1,remaining-x);}}
void supports(int k,int first){if(k>0)composition(k,0,5);if(k==5)return;for(int v=first;v<n;v++){bool ok=true;for(int j=0;j<k;j++)if(edge(v,chosen[j])==0){ok=false;break;}if(ok){chosen[k]=v;supports(k+1,v+1);}}}
int main(){try{
 if(!(cin>>n>>D)||n<1||n>1024||D<1||D>1000000000000L)throw runtime_error("header");mass.resize(n);long M=0;for(long&w:mass){if(!(cin>>w)||w<=0||w>1000000000000L)throw runtime_error("mass");M+=w;}R.resize(n*n);for(long&r:R)if(!(cin>>r)||r<0||r>D)throw runtime_error("probability");for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(R[i*n+j]!=R[j*n+i])throw runtime_error("asymmetry");string extra;if(cin>>extra)throw runtime_error("trailing input");
 for(col=0;col<2;col++)supports(0,0);Z denom=power(D,10)*power(M,5);mpq_class density(total[0]+total[1],denom);density.canonicalize();cout<<density.get_num().get_str()<<"\n"<<density.get_den().get_str()<<"\n";cout<<total[0].get_str()<<"\n"<<total[1].get_str()<<"\n";return 0;
 }catch(exception&e){cerr<<"REJECT "<<e.what()<<"\n";return 1;}}

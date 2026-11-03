// Exact generic equal-mass graphon counter. No Cayley assumption is used.
// D<=4096 implies every ten-edge product is <=2^120, fitting unsigned 128 bits.
// Accumulation and final reduction use arbitrary-precision GMP integers.
#include <gmpxx.h>
#include <array>
#include <cstdint>
#include <vector>
#include <iostream>
#include <stdexcept>
using namespace std;using U=unsigned __int128;using Z=mpz_class;
int n,D,color,chosen[5],occupancy[5];vector<int>matrix;vector<array<U,11>>powers;Z total[2];int factorials[6]={1,1,2,6,24,120};
void accumulate(U v,int mult){v*=mult;uint64_t words[2]={uint64_t(v),uint64_t(v>>64)};Z z;mpz_import(z.get_mpz_t(),2,-1,sizeof(uint64_t),0,0,words);total[color]+=z;}
void value(int size){U product=1;int divisor=1;for(int i=0;i<size;i++){int a=chosen[i],c=occupancy[i];divisor*=factorials[c];product*=powers[a*n+a][c*(c-1)/2];for(int j=0;j<i;j++)product*=powers[a*n+chosen[j]][c*occupancy[j]];if(!product)return;}accumulate(product,120/divisor);}
void compositions(int size,int pos,int remaining){if(pos+1==size){occupancy[pos]=remaining;value(size);return;}for(int c=1;c<=remaining-(size-pos-1);c++){occupancy[pos]=c;compositions(size,pos+1,remaining-c);}}
void supports(int size,int first,U product){if(size==5){accumulate(product,120);return;}if(size)compositions(size,0,5);for(int v=first;v<n;v++){U factor=1;for(int i=0;i<size;i++){factor*=powers[v*n+chosen[i]][1];if(!factor)break;}if(factor){chosen[size]=v;supports(size+1,v+1,product*factor);}}}
int main(){try{
 if(!(cin>>n>>D)||n<1||n>1024||D<1||D>4096)throw runtime_error("uniform checker ranges");for(int i=0;i<n;i++){int m;if(!(cin>>m)||m!=1)throw runtime_error("requires unit masses");}matrix.resize(n*n);for(int&x:matrix)if(!(cin>>x)||x<0||x>D)throw runtime_error("probability range");for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(matrix[i*n+j]!=matrix[j*n+i])throw runtime_error("asymmetry");string extra;if(cin>>extra)throw runtime_error("trailing data");powers.resize(n*n);
 for(color=0;color<2;color++){for(int i=0;i<n*n;i++){powers[i][0]=1;int q=color?D-matrix[i]:matrix[i];for(int e=1;e<=10;e++)powers[i][e]=powers[i][e-1]*q;}supports(0,0,1);}
 Z a,b;mpz_ui_pow_ui(a.get_mpz_t(),D,10);mpz_ui_pow_ui(b.get_mpz_t(),n,5);mpq_class density(total[0]+total[1],a*b);density.canonicalize();cout<<density.get_num().get_str()<<"\n"<<density.get_den().get_str()<<"\n"<<total[0].get_str()<<"\n"<<total[1].get_str()<<"\n";return 0;
 }catch(exception&e){cerr<<"REJECT "<<e.what()<<"\n";return 1;}}

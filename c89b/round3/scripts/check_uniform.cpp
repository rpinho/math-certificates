// Exact generic uniform-mass matrix checker; no symmetry or search data used.
// For D<=64,n<=1024 each product <=2^60 and each full sum <=2^110.
#include <gmpxx.h>
#include <array>
#include <cstdint>
#include <vector>
#include <iostream>
#include <stdexcept>
using namespace std;using U=unsigned __int128;
int n,D,color,chosen[5],occupancy[5];vector<int>matrix;vector<array<uint64_t,11>>powers;U total[2];int factorials[6]={1,1,2,6,24,120};
string decimal(U v){if(!v)return "0";string s;while(v){s.push_back('0'+v%10);v/=10;}return string(s.rbegin(),s.rend());}
void value(int size){uint64_t product=1;int divisor=1;for(int i=0;i<size;i++){int a=chosen[i],c=occupancy[i];divisor*=factorials[c];product*=powers[a*n+a][c*(c-1)/2];for(int j=0;j<i;j++)product*=powers[a*n+chosen[j]][c*occupancy[j]];if(!product)return;}total[color]+=U(product)*(120/divisor);}
void compositions(int size,int pos,int remaining){if(pos+1==size){occupancy[pos]=remaining;value(size);return;}for(int c=1;c<=remaining-(size-pos-1);c++){occupancy[pos]=c;compositions(size,pos+1,remaining-c);}}
void supports(int size,int first,uint64_t distinct_product){
 if(size==5){total[color]+=U(distinct_product)*120;return;}
 if(size)compositions(size,0,5);
 for(int v=first;v<n;v++){uint64_t factor=1;for(int i=0;i<size;i++){factor*=powers[v*n+chosen[i]][1];if(!factor)break;}if(factor){chosen[size]=v;supports(size+1,v+1,distinct_product*factor);}}
}
int main(){try{
 if(!(cin>>n>>D)||n<1||n>1024||D<1||D>64)throw runtime_error("uniform checker ranges");
 for(int i=0;i<n;i++){int m;if(!(cin>>m)||m!=1)throw runtime_error("requires uniform unit masses");}
 matrix.resize(n*n);for(int&x:matrix)if(!(cin>>x)||x<0||x>D)throw runtime_error("probability range");
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(matrix[i*n+j]!=matrix[j*n+i])throw runtime_error("asymmetry");
 string extra;if(cin>>extra)throw runtime_error("trailing input");powers.resize(n*n);
 for(color=0;color<2;color++){for(int i=0;i<n*n;i++){powers[i][0]=1;int q=color?D-matrix[i]:matrix[i];for(int e=1;e<=10;e++)powers[i][e]=powers[i][e-1]*q;}supports(0,0,1);}
 U denominator=1;for(int i=0;i<10;i++)denominator*=D;for(int i=0;i<5;i++)denominator*=n;
 mpq_class density(mpz_class(decimal(total[0]+total[1])),mpz_class(decimal(denominator)));density.canonicalize();
 cout<<density.get_num().get_str()<<"\n"<<density.get_den().get_str()<<"\n"<<decimal(total[0])<<"\n"<<decimal(total[1])<<"\n";
 return 0;
 }catch(exception&e){cerr<<"REJECT "<<e.what()<<"\n";return 1;}}

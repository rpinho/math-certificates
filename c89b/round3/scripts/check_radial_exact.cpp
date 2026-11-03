// Exact structured checker, written separately from all search histograms.
// Enumerates every 16-column count vector of four binary vertices, then every
// ordered assignment of their layers. The fifth vertex is fixed by transitivity.
#include <gmpxx.h>
#include <array>
#include <algorithm>
#include <iostream>
#include <stdexcept>
using namespace std;
int d,L;long D,P,Q;int countcol[16];unsigned long column_factorial[13];mpz_class red,blue;
void leaf(){
 unsigned long den=1;for(int c:countcol)den*=column_factorial[c];unsigned long mult=column_factorial[d]/den;
 int dist[5][5]{};
 for(int j=1;j<5;j++)for(int i=0;i<j;i++){
  int w=0;for(int b=0;b<16;b++)w+=countcol[b]*(((b>>(j-1))&1)^(i?((b>>(i-1))&1):0));
  dist[i][j]=min(w,d+1-w);
 }
 unsigned long layers=1;for(int i=0;i<4;i++)layers*=L;
 for(unsigned long code=0;code<layers;code++){
  int layer[5]{},r=code;for(int i=1;i<5;i++){layer[i]=r%L;r/=L;}
  mpz_class a=mult,b=mult;
  for(int j=1;j<5;j++)for(int i=0;i<j;i++){
   int w=dist[i][j];long p=layer[i]==layer[j]?(w==1?P:(w==2?D:0)):(w==0?D:(w==3?Q:0));
   a*=p;b*=D-p;
  }
  red+=a;blue+=b;
 }
}
void enumerate(int column,int left){if(column==15){countcol[column]=left;leaf();return;}for(int n=0;n<=left;n++){countcol[column]=n;enumerate(column+1,left-n);}}
int main(){try{
 if(!(cin>>d>>L>>D>>P>>Q)||d<2||d>6||d%2||L<2||L>8||D<1||D>1000000000L||P<0||P>D||Q<0||Q>D)throw runtime_error("parameter range");
 string extra;if(cin>>extra)throw runtime_error("trailing input");
 column_factorial[0]=1;for(int i=1;i<=d;i++)column_factorial[i]=column_factorial[i-1]*i;
 enumerate(0,d);mpz_class den=1;for(int i=0;i<10;i++)den*=D;for(int i=0;i<4;i++)den*=L;mpz_mul_2exp(den.get_mpz_t(),den.get_mpz_t(),4*d);
 mpq_class value(red+blue,den);value.canonicalize();cout<<value.get_num().get_str()<<"\n"<<value.get_den().get_str()<<"\n"<<red.get_str()<<"\n"<<blue.get_str()<<"\n";
 return 0;
 }catch(exception&e){cerr<<"REJECT "<<e.what()<<"\n";return 1;}}

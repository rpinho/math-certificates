// Independent B: every coefficient is computed by a direct character sum.
#include <algorithm>
#include <array>
#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main(int argc,char** argv){
 assert(argc==3);ifstream input(argv[1]);assert(input.good());string text;
 array<int,11> limits{};vector<int> nine,ten;int classes=0;
 while(getline(input,text)){
  if(!text.empty()&&text.back()=='\r')text.pop_back();
  assert(text.size()==1024);++classes;array<int,1024> values{},coefficients{};array<int,10> degrees{};
  for(int point=0;point<1024;++point){assert(text[point]=='0'||text[point]=='1');values[point]=((text[point]-'0')^__builtin_parity(unsigned(point)))?-1:1;}
  long long norm=0;bool homogeneous=true;
  for(int mask=0;mask<1024;++mask){
   int value=0;for(int point=0;point<1024;++point)value+=(__builtin_parity(unsigned(mask&point))?-values[point]:values[point]);
   coefficients[mask]=value;norm+=1ll*value*value;if(!value)continue;
   int degree=__builtin_popcount(unsigned(mask));assert(degree<=3);homogeneous&=degree==3;
   for(int j=0;j<10;++j)if(mask>>j&1)degrees[j]=max(degrees[j],degree);
  }
  assert(norm==1024ll*1024);int used=0,score=0;
  for(int d:degrees)if(d){++used;score+=8/(1<<d);}
  for(int budget=used;budget<=10;++budget)limits[budget]=max(limits[budget],score);
  if(used==9){assert(coefficients[0]==0);for(int d:degrees)assert(d==0||d==3);nine.push_back(classes);}
  if(used==10){assert(homogeneous);ten.push_back(classes);}
 }
 assert(classes==761);assert((limits==array<int,11>{0,4,4,6,8,8,8,8,8,9,10}));
 assert((nine==vector<int>{485,571,633,689,701,716}));assert((ten==vector<int>{700}));
 ofstream out(argv[2]);out<<"{\"status\":\"PASS\",\"classes\":761,\"potential_units_eighths\":[";
 for(int j=0;j<11;++j)out<<(j?",":"")<<limits[j];out<<"],\"nine_balanced\":[485,571,633,689,701,716],\"ten_homogeneous\":[700]}\n";
 cout<<"PASS B cubic count/potential envelope and balance"<<endl;
}

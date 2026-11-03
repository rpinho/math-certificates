// Exact B sub-check: complete truth table of the small outer function,
// followed by separately written (same agent) weighted degree and relevance arithmetic.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
int main(int argc,char** argv){
 assert(argc==2);ifstream file(argv[1]);assert(file.good());
 int n,den,count,claimed;file>>n>>den>>count>>claimed;assert(n>=1&&n<=22&&den==8);
 vector<int> weights(n);for(int& w:weights){file>>w;assert(w>=1&&w<=5);}
 vector<int64_t> values(1<<n);int used=0,degree=0;
 for(int t=0;t<count;++t){int s,c;file>>s>>c;assert(s>=0&&s<(1<<n)&&c);assert(values[s]==0);values[s]=c;used|=s;int d=0;for(int j=0;j<n;++j)if(s>>j&1)d+=weights[j];degree=max(degree,d);}
 assert(used==(1<<n)-1&&degree<=5);string extra;assert(!(file>>extra));
 for(int width=1;width<(1<<n);width*=2)for(int start=0;start<(1<<n);start+=2*width)for(int j=start;j<start+width;++j){int64_t a=values[j],b=values[j+width];values[j]=a+b;values[j+width]=a-b;}
 for(int64_t value:values)assert(value==den||value==-den);
 int relevant=0;for(int w:weights)relevant+=3*(1<<(w-1))-2;
 assert(relevant==claimed);cout<<relevant<<" "<<degree<<endl;
}

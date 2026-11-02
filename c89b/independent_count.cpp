// Independent exact recount: distinct supports and positive occupancy compositions.
// This does not use the search enumerator, derivatives, or its monomial cache.
// Input: n D p followed by n*n integer red probabilities; equal block masses.
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
#include <stdexcept>
using namespace std;
static int n, color, k, vertices[5], occupancy[5];
static int64_t D,p;
static vector<int64_t> red;
static uint64_t hist[2][11];
static const int fact[]={1,1,2,6,24,120};
static int64_t edge(int i,int j) {int64_t a=red[i*n+j];return color?D-a:a;}
static int degree(int64_t a) {
    if(a==D) return 0;
    if(a==(color?D-p:p)) return 1;
    if(a==0) return -100;
    throw runtime_error("unsupported probability");
}
static void contribute() {
    int power=0,den=1;
    for(int i=0;i<k;i++) {
        int m=occupancy[i];den*=fact[m];
        if(m>1) {int e=degree(edge(vertices[i],vertices[i]));if(e<0)return;power+=e*m*(m-1)/2;}
        for(int j=0;j<i;j++) {int e=degree(edge(vertices[i],vertices[j]));if(e<0)return;power+=e*m*occupancy[j];}
    }
    if(power<0||power>10||120%den) throw runtime_error("bad exponent or multiplicity");
    hist[color][power]+=120/den;
}
static void compositions(int pos,int remaining) {
    if(pos==k-1) {occupancy[pos]=remaining;contribute();return;}
    for(int m=1;m<=remaining-(k-1-pos);m++) {occupancy[pos]=m;compositions(pos+1,remaining-m);}
}
static void supports(int used,int first) {
    if(used) {k=used;compositions(0,5);}
    if(used==5)return;
    for(int v=first;v<n;v++) {
        bool possible=true;
        for(int j=0;j<used;j++) if(edge(v,vertices[j])==0) {possible=false;break;}
        if(possible) {vertices[used]=v;supports(used+1,v+1);}
    }
}
int main() {
    if(!(cin>>n>>D>>p)||n<1||n>1024||!(0<p&&p<D)) throw runtime_error("invalid header");
    red.resize(n*n);
    for(auto &a:red) if(!(cin>>a)||!(a==0||a==p||a==D)) throw runtime_error("invalid edge");
    for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(red[i*n+j]!=red[j*n+i])throw runtime_error("asymmetric");
    for(color=0;color<2;color++)supports(0,0);
    for(int c=0;c<2;c++) {for(int e=0;e<=10;e++)cout<<hist[c][e]<<(e==10?'\n':' ');}
}

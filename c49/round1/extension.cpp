// Original exhaustive 28-point maximal-extension search, using mask boxes.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>
using namespace std;
using Bits=array<uint64_t,16>;
struct Box{int c;vector<int>u,v;};
vector<int> domain(const vector<int>& a,bool up){vector<int>d;for(int x=0;x<1024;x++)for(int y:a)if(up?((x&y)==y):((x&y)==x)){d.push_back(x);break;}return d;}
vector<int> third(const vector<int>&a,const vector<int>&b){array<bool,1024> ok{};for(int x:a)for(int y:b){int free=1023^(x|y),s=free;do{ok[(x&y)|s]=true;s=(s-1)&free;}while(s!=free);}vector<int>d;for(int x=0;x<1024;x++)if(ok[x])d.push_back(x);return d;}
Bits bitset_of(const vector<int>&v){Bits r{};for(int x:v)r[x>>6]|=1ULL<<(x&63);return r;}
int main(int argc,char**argv){
    auto start=chrono::steady_clock::now();
    if(argc!=3){cerr<<"usage: extension masks output\n";return 2;}
    ifstream f(argv[1]);uint32_t x;vector<uint32_t> family;
    map<int,map<int,vector<int>>> slices;
    while(f>>x){family.push_back(x);slices[x&255][(x>>8)&1023].push_back(x>>18);}
    vector<Box>boxes;
    for(auto &[c,uv]:slices){map<vector<int>,vector<int>> groups;for(auto &[u,v]:uv){sort(v.begin(),v.end());groups[v].push_back(u);}for(auto &[v,u]:groups)boxes.push_back({c,u,v});}
    vector<uint64_t> alive(1<<22,~0ULL);
    auto remove_box=[&](const vector<int>&cs,const vector<int>&us,const vector<int>&vs){Bits bits=bitset_of(vs);for(int c:cs)for(int u:us){uint64_t*p=&alive[(c*1024+u)*16];for(int k=0;k<16;k++)p[k]&=~bits[k];}};
    auto count=[&](){uint64_t n=0;for(auto a:alive)n+=__builtin_popcountll(a);return n;};
    for(auto &b:boxes){vector<int>csup,csub;for(int c=0;c<256;c++){if((c&b.c)==b.c)csup.push_back(c);if((c&b.c)==c)csub.push_back(c);}remove_box(csup,domain(b.u,true),domain(b.v,true));remove_box(csub,domain(b.u,false),domain(b.v,false));}
    cout<<"Sperner-compatible candidates "<<count()<<" boxes "<<boxes.size()<<endl;
    // One rejection control candidate compatible with Sperner, before removing flowers.
    uint32_t control=0;bool got=false;for(int c=0;c<256&&!got;c++)for(int u=0;u<1024&&!got;u++)for(int w=0;w<16&&!got;w++){auto a=alive[(c*1024+u)*16+w];if(a){control=c|(u<<8)|((w*64+__builtin_ctzll(a))<<18);got=true;}}
    if(got){ofstream cf("logs/sperner_candidate.json");cf<<control<<"\n";}
    map<pair<vector<int>,vector<int>>,vector<int>> cache;
    auto thirds=[&](const vector<int>&u,const vector<int>&v)->const vector<int>&{auto key=make_pair(min(u,v),max(u,v));auto it=cache.find(key);if(it==cache.end())it=cache.emplace(key,third(u,v)).first;return it->second;};
    size_t pairs=0;
    for(size_t i=0;i<boxes.size();i++)for(size_t j=i;j<boxes.size();j++){
        auto&a=boxes[i];auto&b=boxes[j];vector<int>cs;int inter=a.c&b.c,free=255^(a.c|b.c),s=free;do{cs.push_back(inter|s);s=(s-1)&free;}while(s!=free);
        remove_box(cs,thirds(a.u,b.u),thirds(a.v,b.v));pairs++;
    }
    auto total=count();cout<<"Addable candidates "<<total<<" box_pairs "<<pairs<<" elapsed "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
    ofstream out(argv[2]);uint64_t written=0;
    for(int c=0;c<256;c++)for(int u=0;u<1024;u++)for(int w=0;w<16;w++)for(uint64_t a=alive[(c*1024+u)*16+w];a;a&=a-1){uint32_t v=w*64+__builtin_ctzll(a);if(written++<1000000)out<<(c|(u<<8)|(v<<18))<<'\n';}
    ofstream stats("logs/extension.json");stats<<"{\"universe\":268435456,\"family_size\":"<<family.size()<<",\"addable\":"<<total<<",\"written\":"<<min(total,1000000ULL)<<",\"boxes\":"<<boxes.size()<<",\"wall_seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}\n";
}

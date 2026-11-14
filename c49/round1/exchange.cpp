// Original exact screening for all additions reachable after <=2 deletions.
// Sufficient obstruction counts discard candidates; remaining ones need exact covers.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <tuple>
#include <vector>
using namespace std;
struct Profile{array<int,1024>count{},row{},col{};};
struct Box{int c,u,v;};
using Bits=array<uint64_t,16>;
int main(int argc,char**argv){
    if(argc!=2)return 2;auto start=chrono::steady_clock::now();
    ifstream f(argv[1]);uint32_t x;vector<uint32_t>family;map<int,map<int,vector<int>>>slices;
    while(f>>x){family.push_back(x);slices[x&255][(x>>8)&1023].push_back(x>>18);}
    vector<vector<int>>types;map<vector<int>,int>ids;
    auto ident=[&](vector<int>a){sort(a.begin(),a.end());auto it=ids.find(a);if(it!=ids.end())return it->second;int k=types.size();types.push_back(a);ids[a]=k;return k;};
    vector<Box>boxes;for(auto &[c,uv]:slices){map<vector<int>,vector<int>>groups;for(auto &[u,v]:uv){sort(v.begin(),v.end());groups[v].push_back(u);}for(auto &[v,u]:groups)boxes.push_back({c,ident(u),ident(v)});}
    map<pair<int,int>,Profile>profiles;
    auto prof=[&](int i,int j)->Profile&{
        auto key=make_pair(i,j);auto it=profiles.find(key);if(it!=profiles.end())return it->second;
        Profile p;vector<array<int,1024>>rows(types[i].size()),cols(types[j].size());
        for(size_t a=0;a<types[i].size();a++)for(size_t b=0;b<types[j].size();b++){
            int aa=types[i][a],bb=types[j][b],free=1023^(aa|bb),s=free;do{int q=(aa&bb)|s;p.count[q]++;rows[a][q]++;cols[b][q]++;s=(s-1)&free;}while(s!=free);
        }
        for(int q=0;q<1024;q++){for(auto&r:rows)p.row[q]=max(p.row[q],r[q]);for(auto&r:cols)p.col[q]=max(p.col[q],r[q]);}
        return profiles.emplace(key,p).first->second;
    };
    vector<uint64_t>alive(1<<22,~0ULL);
    auto left=[&](){uint64_t n=0;for(auto y:alive)n+=__builtin_popcountll(y);return n;};
    // >=3 comparable members in a single box already require >2 deletions.
    for(auto&b:boxes)for(bool up:{false,true}){
        array<int,1024>us{},vs{};for(int q=0;q<1024;q++){for(int y:types[b.u])if(up?((q&y)==y):((q&y)==q))us[q]++;for(int y:types[b.v])if(up?((q&y)==y):((q&y)==q))vs[q]++;}
        for(int c=0;c<256;c++)if(up?((c&b.c)==b.c):((c&b.c)==c))for(int u=0;u<1024;u++)if(us[u])for(int w=0;w<16;w++){uint64_t bits=0;for(int k=0;k<64;k++)if(us[u]*vs[w*64+k]>=3)bits|=1ULL<<k;alive[(c*1024+u)*16+w]&=~bits;}
    }
    cout<<"After comparable obstruction "<<left()<<endl;
    map<tuple<int,int,int,int,int>,vector<Bits>>cache;
    size_t bi=0;
    for(size_t i=0;i<boxes.size();i++)for(size_t j=i;j<boxes.size();j++){
        auto&a=boxes[i];auto&b=boxes[j];int factor=(i==j?4:2);
        auto key=make_tuple(a.u,b.u,a.v,b.v,factor);auto it=cache.find(key);
        if(it==cache.end()){
            auto&pu=prof(a.u,b.u);auto&pv=prof(a.v,b.v);vector<Bits>mask(1024);
            for(int u=0;u<1024;u++)if(pu.count[u])for(int v=0;v<1024;v++){
                int pairs=pu.count[u]*pv.count[v];int deg=max(pu.row[u]*pv.row[v],pu.col[u]*pv.col[v]);
                if(pairs>factor*deg)mask[u][v>>6]|=1ULL<<(v&63);
            }
            it=cache.emplace(key,move(mask)).first;
        }
        int free=255^(a.c|b.c),s=free;
        do{int c=(a.c&b.c)|s;for(int u=0;u<1024;u++){auto p=&alive[(c*1024+u)*16];for(int k=0;k<16;k++)p[k]&=~it->second[u][k];}s=(s-1)&free;}while(s!=free);
        bi++;
    }
    for(uint32_t m:family){int c=m&255,u=(m>>8)&1023,v=m>>18;alive[(c*1024+u)*16+(v>>6)]&=~(1ULL<<(v&63));}
    auto total=left();cout<<"Candidates after <=2 deletion sufficient-obstruction screen "<<total<<" cache "<<cache.size()<<" types "<<types.size()<<" seconds "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
    ofstream out("logs/exchange_candidates.masks");for(int c=0;c<256;c++)for(int u=0;u<1024;u++)for(int w=0;w<16;w++)for(uint64_t a=alive[(c*1024+u)*16+w];a;a&=a-1)out<<(c|(u<<8)|((w*64+__builtin_ctzll(a))<<18))<<'\n';
    ofstream stats("logs/exchange_screen.json");stats<<"{\"universe\":268435456,\"remaining_nonmembers\":"<<total<<",\"types\":"<<types.size()<<",\"box_pair_profiles\":"<<cache.size()<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}\n";
}

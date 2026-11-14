// Original exact sunflower/containment separation and depth-two deletion covers.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <set>
#include <vector>
using namespace std;
struct Box{int c,u,v;};
using VP=vector<pair<int,int>>;
int main(){
    auto start=chrono::steady_clock::now();ifstream f("certificates/baseline.masks");uint32_t x;vector<uint32_t>family;map<int,map<int,vector<int>>>slices;
    while(f>>x){family.push_back(x);slices[x&255][(x>>8)&1023].push_back(x>>18);}
    vector<vector<int>>types;map<vector<int>,int>ids;
    auto ident=[&](vector<int>a){sort(a.begin(),a.end());auto it=ids.find(a);if(it!=ids.end())return it->second;int k=types.size();types.push_back(a);ids[a]=k;return k;};
    vector<Box>boxes;for(auto &[c,uv]:slices){map<vector<int>,vector<int>>groups;for(auto &[u,v]:uv){sort(v.begin(),v.end());groups[v].push_back(u);}for(auto &[v,u]:groups)boxes.push_back({c,ident(u),ident(v)});}
    map<pair<int,int>,vector<VP>>tables;
    auto table=[&](int i,int j)->vector<VP>&{
        auto key=make_pair(i,j);auto it=tables.find(key);if(it!=tables.end())return it->second;
        vector<VP>t(1024);for(int a:types[i])for(int b:types[j]){int free=1023^(a|b),s=free;do{t[(a&b)|s].emplace_back(a,b);s=(s-1)&free;}while(s!=free);}
        return tables.emplace(key,std::move(t)).first->second;
    };
    array<VP,256>pairs;
    for(int i=0;i<(int)boxes.size();i++)for(int j=i;j<(int)boxes.size();j++){
        auto&a=boxes[i];auto&b=boxes[j];int free=255^(a.c|b.c),s=free;do{pairs[(a.c&b.c)|s].emplace_back(i,j);s=(s-1)&free;}while(s!=free);
    }
    auto constraint=[&](uint32_t m,const vector<uint32_t>&removed)->vector<uint32_t>{
        auto gone=[&](uint32_t a){return find(removed.begin(),removed.end(),a)!=removed.end();};
        int c=m&255,u=(m>>8)&1023,v=m>>18;
        for(auto&b:boxes)for(bool up:{false,true}){
            if(up?((c&b.c)!=b.c):((c&b.c)!=c))continue;
            for(int a:types[b.u])if(up?((u&a)==a):((u&a)==u))for(int d:types[b.v])if(up?((v&d)==d):((v&d)==v)){
                uint32_t y=b.c|(a<<8)|(d<<18);if(!gone(y))return {y};
            }
        }
        for(auto [i,j]:pairs[c]){
            auto&a=boxes[i];auto&b=boxes[j];auto&ut=table(a.u,b.u)[u];if(ut.empty())continue;auto&vt=table(a.v,b.v)[v];if(vt.empty())continue;
            for(auto[ua,ub]:ut)for(auto[va,vb]:vt){uint32_t aa=a.c|(ua<<8)|(va<<18),bb=b.c|(ub<<8)|(vb<<18);if(aa!=bb&&!gone(aa)&&!gone(bb))return {aa,bb};}
        }
        return {};
    };
    ifstream cand("logs/exchange_candidates.masks");map<uint32_t,set<vector<uint32_t>>>covers;size_t total=0;
    while(cand>>x){
        uint32_t m=x;set<vector<uint32_t>>solutions;
        function<void(vector<uint32_t>)>visit=[&](vector<uint32_t>r){
            sort(r.begin(),r.end());for(auto&s:solutions)if(includes(r.begin(),r.end(),s.begin(),s.end()))return;
            auto con=constraint(m,r);if(con.empty()){
                for(auto it=solutions.begin();it!=solutions.end();)if(includes(it->begin(),it->end(),r.begin(),r.end()))it=solutions.erase(it);else ++it;
                solutions.insert(r);return;
            }
            if(r.size()==2)return;
            for(uint32_t a:con){auto rr=r;rr.push_back(a);visit(rr);}
        };
        visit({});if(!solutions.empty())covers[m]=solutions;total++;
    }
    ofstream out("logs/deletion_covers.json");out<<"[";bool first=true;size_t one=0,two=0;
    for(auto &[m,ss]:covers){if(!first)out<<",";first=false;out<<"{\"candidate\":"<<m<<",\"minimal_removals\":[";bool ff=true;for(auto&r:ss){if(!ff)out<<",";ff=false;out<<"[";for(size_t i=0;i<r.size();i++){if(i)out<<",";out<<r[i];}out<<"]";if(r.size()==1)one++;if(r.size()==2)two++;}out<<"]}";}out<<"]\n";
    cout<<"screened "<<total<<" feasible candidates "<<covers.size()<<" singleton covers "<<one<<" pair covers "<<two<<" seconds "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
}

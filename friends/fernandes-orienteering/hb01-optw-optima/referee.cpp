// Independent referee implementation. No claimant code is linked or imported.
// Inputs: released raw Gavalas file; untrusted finite-cover certificate.
#include <algorithm>
#include <array>
#include <bitset>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using i64=long long; using u64=unsigned long long;
void demand(bool b,string s){if(!b)throw runtime_error(s);}
i64 decimal100(string s){
    bool neg=!s.empty()&&s[0]=='-'; if(neg)s=s.substr(1);
    auto p=s.find('.'); string a=s.substr(0,p),b=p==string::npos?"":s.substr(p+1);
    demand(b.size()<=2,"too many decimal places"); while(b.size()<2)b+='0';
    return (neg?-1:1)*(stoll(a)*100+stoll(b));
}
i64 square_root(i64 x){i64 l=0,h=x+1; while(l+1<h){i64 m=l+(h-l)/2;if((__int128)m*m<=x)l=m;else h=m;}return l;}
vector<string> words(string l){istringstream in(l); vector<string> r;string s;while(in>>s)r.push_back(s);return r;}
struct Model{
    int n; vector<i64>x,y; vector<int>svc,profit,op,cl,mn,w,order,kp;
    vector<vector<int>> d,sp;
    explicit Model(string file){
        ifstream f(file); demand(bool(f),"missing raw file");string l;getline(f,l);auto h=words(l);
        demand(h.size()==16&&stoi(h[0])==20&&stoi(h[1])==1,"not single-day TTDP");
        int day=stoi(h[2]);n=stoi(h[3])+1; demand(day>=0&&day<7&&n>1&&n<=256,"bad dimensions");
        x.resize(n);y.resize(n);svc.resize(n);profit.resize(n);op.resize(n);cl.resize(n);
        for(int i=0;i<n;i++){
            demand(bool(getline(f,l)),"short raw input");auto r=words(l);
            demand(r.size()==(i?21:7)&&stoi(r[0])==i,"raw format/id mismatch");
            x[i]=decimal100(r[1]);y[i]=decimal100(r[2]);svc[i]=decimal100(r[3]);
            i64 p=decimal100(r[4]);demand(p%100==0&&p>=0,"reward not nonnegative integer");profit[i]=p/100;
            op[i]=decimal100(r[i?6+2*day:5]);cl[i]=decimal100(r[i?7+2*day:6]);
            demand(svc[i]>=0&&op[i]>=0&&cl[i]>=op[i],"invalid times");
        }
        while(getline(f,l))demand(words(l).empty(),"trailing raw rows");
        demand(svc[0]==0&&profit[0]==0&&cl[0]>=op[0]&&cl[0]<1000000,"depot convention");
        d.assign(n,vector<int>(n));
        for(int i=0;i<n;i++)for(int j=0;j<n;j++){
            i64 dx=x[i]-x[j],dy=y[i]-y[j]; d[i][j]=square_root(dx*dx+dy*dy);
        }
        prepare();
    }
    void prepare(){
        sp=d;for(int k=0;k<n;k++)for(int i=0;i<n;i++)for(int j=0;j<n;j++)sp[i][j]=min(sp[i][j],sp[i][k]+sp[k][j]);
        mn.assign(n,100000000); w.resize(n);
        for(int i=0;i<n;i++){for(int j=0;j<n;j++)if(i!=j)mn[i]=min(mn[i],d[i][j]);w[i]=2*(svc[i]+mn[i]);}
        // For every simple suffix, each traveled edge pays the endpoint minima.
        // Thus sum_j w[j] <= 2*(deadline-departure)-minout(i)-minin(0).
        int cap=2*(cl[0]-op[0]); kp.assign(cap+1,0);
        for(int j=1;j<n;j++)for(int c=cap;c>=w[j];--c)kp[c]=max(kp[c],kp[c-w[j]]+profit[j]);
        order.resize(n-1);iota(order.begin(),order.end(),1);
        sort(order.begin(),order.end(),[&](int a,int b){
            if(w[a]==0||w[b]==0)return w[a]==0&&w[b]!=0;
            i64 lhs=(i64)profit[a]*w[b],rhs=(i64)profit[b]*w[a]; return lhs==rhs?a<b:lhs>rhs;
        });
    }
    int upper(int i,int t,int p,const bitset<256>&forbidden)const{
        if(t+sp[i][0]>cl[0])return -1;
        int cap=2*(cl[0]-t)-mn[i]-mn[0]; if(cap<0)return p;
        int a=p+kp[min(cap,(int)kp.size()-1)],val=p,remaining=cap;
        for(int j:order){
            if(forbidden[j])continue;
            int start=max(t+sp[i][j],op[j]);
            if(start>cl[j]||start+svc[j]+sp[j][0]>cl[0])continue;
            if(w[j]<=remaining){remaining-=w[j];val+=profit[j];}
            else {val+=(i64)profit[j]*remaining/w[j];break;}
        }
        return min(a,val);
    }
    int route(const vector<int>&r,bool mask=true)const{
        demand(r.size()>=2&&r.front()==0&&r.back()==0,"route endpoints");
        bitset<256> seen;int t=op[0],p=0;
        for(size_t a=1;a<r.size();a++){
            int i=r[a-1],j=r[a];demand(j>=0&&j<n,"route vertex");
            demand(j!=0||a==r.size()-1,"internal depot");
            demand(!seen[j],"repeat");seen[j]=true;
            int start=max(t+d[i][j],op[j]);demand(start<=cl[j],"start window");
            t=start+svc[j];p+=profit[j];if(mask)demand(t+d[j][0]<=cl[0],"direct return mask");
        }
        demand(t<=cl[0],"late depot");return p;
    }
};
struct State{int v,t,p;u64 mask;};
struct Cover{
    const Model&m;int U,P;vector<vector<int>> ng,pos;vector<State> states;vector<vector<State>> at;vector<int>primal;
    Cover(const Model&model,string file):m(model){
        ifstream f(file);demand(bool(f),"missing proof");string magic;int n;f>>magic>>n>>P;
        if(magic=="NGBOUND2")f>>U;else{demand(magic=="NGCERT1","proof format");U=P;}
        demand(n==m.n&&0<=P&&P<=U,"proof dimensions/bound");ng.resize(n);pos.assign(n,vector<int>(n,-1));at.resize(n);
        for(int i=0;i<n;i++){
            int k;f>>k;demand(k>0&&k<63,"neighborhood size");ng[i].resize(k);
            for(int a=0;a<k;a++){int j;f>>j;demand(j>=0&&j<n&&pos[i][j]<0,"neighborhood vertex");ng[i][a]=j;pos[i][j]=a;}
            demand(pos[i][i]>=0,"neighborhood omits self");
        }
        int count;f>>count;demand(count>=0&&count<10000000,"proof size");
        for(int a=0;a<count;a++){
            State s;f>>s.v>>s.t>>s.p>>s.mask;
            demand(s.v>=0&&s.v<n&&s.t>=m.op[0]&&s.t<=m.cl[0]&&s.p>=0,"bad label");
            demand(s.mask<(1ULL<<ng[s.v].size())&&(s.mask&(1ULL<<pos[s.v][s.v])),"bad memory");
            states.push_back(s);at[s.v].push_back(s);
        }
        int k;f>>k;demand(k>=2&&k<=n+1,"primal size");primal.resize(k);for(int&i:primal)f>>i;
        demand(bool(f),"truncated proof");string tail;demand(!(f>>tail),"extra proof data");
        demand(m.route(primal)==P,"proof primal score");
        for(auto&v:at)sort(v.begin(),v.end(),[](State a,State b){return a.t<b.t;});
    }
    bitset<256> memory(State s)const{bitset<256>b;for(int a=0;a<(int)ng[s.v].size();a++)if(s.mask&(1ULL<<a))b[ng[s.v][a]]=true;return b;}
    u64 encode(int v,const bitset<256>&b)const{u64 z=0;for(int a=0;a<(int)ng[v].size();a++)if(b[ng[v][a]])z|=1ULL<<a;return z;}
    bool covered(State s)const{
        auto b=memory(s);
        if(m.upper(s.v,s.t,s.p,b)<=U)return true;
        for(auto c:at[s.v]){
            if(c.t>s.t)break;
            if(c.p>=s.p&&(c.mask&s.mask)==c.mask)return true;
        }return false;
    }
    void verify()const{
        State root{0,m.op[0],0,1ULL<<pos[0][0]};demand(covered(root),"uncovered root");
        u64 arcs=0;
        for(State s:states){
            if(s.t+m.d[s.v][0]<=m.cl[0])demand(s.p<=U,"terminal reward exceeds upper");
            auto b=memory(s);
            for(int j=1;j<m.n;j++){
                if(b[j])continue;
                int start=max(s.t+m.d[s.v][j],m.op[j]);
                if(start>m.cl[j])continue;
                int t=start+m.svc[j];if(t+m.sp[j][0]>m.cl[0])continue;
                auto nb=b;nb[j]=true;State q{j,t,s.p+m.profit[j],encode(j,nb)};
                if(!covered(q)){
                    cerr<<"uncovered "<<s.v<<" "<<s.t<<" "<<s.p<<" -> "<<j<<" "<<t<<" "<<q.p<<" mask "<<q.mask<<"\n";
                    throw runtime_error("uncovered transition");
                }arcs++;
            }
        }
        cout<<"{\"status\":\"CERTIFIED\",\"upper\":"<<U<<",\"primal\":"<<P<<",\"labels\":"<<states.size()<<",\"arcs\":"<<arcs<<"}"<<endl;
    }
};
u64 nodes=0;int best=0;vector<int>path,bestpath;
void dfs(const Model&m,int i,int t,int p,bitset<256>&seen,bool prune){
    nodes++;
    if(t+m.d[i][0]<=m.cl[0]&&p>best){best=p;bestpath=path;bestpath.push_back(0);}
    if(prune&&m.upper(i,t,p,seen)<=best)return;
    for(int j=1;j<m.n;j++){
        if(seen[j])continue;
        int st=max(t+m.d[i][j],m.op[j]);
        if(st>m.cl[j]||st+m.svc[j]+m.sp[j][0]>m.cl[0])continue;
        seen[j]=true;path.push_back(j);dfs(m,j,st+m.svc[j],p+m.profit[j],seen,prune);path.pop_back();seen[j]=false;
    }
}
int main(int argc,char**argv){try{
    demand(argc>=3,"usage: referee cover|dfs|plain raw [proof]");Model m(argv[2]);string mode=argv[1];
    if(mode=="cover"){demand(argc==4,"cover needs proof");Cover c(m,argv[3]);c.verify();}
    else if(mode=="dfs"||mode=="plain"){
        best=argc>3?stoi(argv[3]):0;bitset<256>seen;seen[0]=true;path={0};dfs(m,0,m.op[0],0,seen,mode=="dfs");
        cout<<"{\"status\":\"COMPLETE\",\"optimum\":"<<best<<",\"prefixes\":"<<nodes<<",\"route\":[";
        for(size_t a=0;a<bestpath.size();a++){if(a)cout<<",";cout<<bestpath[a];}cout<<"]}"<<endl;
    }else throw runtime_error("mode");
    return 0;
}catch(exception&e){cerr<<"REJECT: "<<e.what()<<endl;return 1;}}

// Simple insertion control. Uses only the referee's raw parser and definitions.
#define main referee_entry
#include "referee.cpp"
#undef main
#include <random>
#include <cmath>
int main(int argc,char**argv){try{
    demand(argc==2,"greedy raw");Model m(argv[1]);mt19937 rng(924872);uniform_real_distribution<double>u(.8,1.2);
    int top=0;vector<int>tour,finishroute;auto begin=chrono::steady_clock::now();
    auto finish=[&](const vector<int>&r){
        int t=m.op[0];for(size_t k=1;k<r.size();k++){
            int j=r[k];int st=max(t+m.d[r[k-1]][j],m.op[j]);
            if(st>m.cl[j])return -1;t=st+m.svc[j];if(t+m.d[j][0]>m.cl[0])return -1;
        }return t;
    };
    for(int run=0;run<24;run++){
        tour={0,0};bitset<256>used;used[0]=true;vector<double>noise(m.n,1.);
        if(run>=4)for(auto&x:noise)x=u(rng);
        double alpha=run%4==0?0:run%4==1?.5:run%4==2?1.:2.;int score=0;
        while(true){
            int base=finish(tour),chosen=-1,pos=-1;double value=-1;
            for(int j=1;j<m.n;j++)if(!used[j]){
                for(int k=1;k<(int)tour.size();k++){
                    auto candidate=tour;candidate.insert(candidate.begin()+k,j);int end=finish(candidate);if(end<0)continue;
                    double ratio=m.profit[j]*noise[j]/pow(max(1,end-base),alpha);
                    if(ratio>value){value=ratio;chosen=j;pos=k;}
                }
            }
            if(chosen<0)break;tour.insert(tour.begin()+pos,chosen);used[chosen]=true;score+=m.profit[chosen];
        }
        if(score>top){top=score;finishroute=tour;}
    }
    demand(m.route(finishroute)==top,"control witness");
    cout<<"{\"score\":"<<top<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-begin).count()<<",\"route\":[";
    for(size_t i=0;i<finishroute.size();i++){if(i)cout<<",";cout<<finishroute[i];}cout<<"]}"<<endl;
}catch(exception&e){cerr<<e.what()<<endl;return 1;}}

// Exhaustive gate: generate every Av_n(1324) once by inserting its maximum.
// Compare exact marginal strip encoding against the formal tower separately.
// No transfer-root search, ensemble tilt, or pairing of independent neighbours.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unistd.h>
using namespace std;
using U = uint64_t;
static constexpr int M=16;
array<int,M> perm{};
array<array<U,M>,5> counts{};
U avoiders=0, dominoes=0, roundtrips=0;
int goal;

int first132end(int n) {
    // First k at which prefix through k contains a 132.
    int minimum=M, first=n;
    for(int j=0;j<n;j++) {
        for(int k=j+1;k<first;k++)
            if(minimum<perm[k] && perm[k]<perm[j])first=k;
        minimum=min(minimum,perm[j]);
    }
    return first;
}

bool contains1324(int n) {
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)
        if(perm[i]<perm[k] && perm[k]<perm[j])for(int l=k+1;l<n;l++)
            if(perm[j]<perm[l])return true;
    return false;
}

void visit(int n) {
    ++avoiders;
    if(n<=8 && contains1324(n))throw runtime_error("generator produced 1324");
    int lower=0,upper=n;
    // A value cut c is a valid domino iff c >= every 213 minimum,
    // and c < every 132 maximum. This exact test avoids repeated triples.
    int prefmin=M;
    for(int j=0;j<n;j++) {
        for(int k=j+1;k<n;k++)
            if(prefmin<perm[k] && perm[k]<perm[j])upper=min(upper,perm[j]-1);
        int first_above=M;
        for(int i=0;i<j;i++)if(perm[i]>perm[j])first_above=min(first_above,perm[i]);
        bool extension=false;
        for(int k=j+1;k<n;k++)if(perm[k]>first_above)extension=true;
        if(extension)lower=max(lower,perm[j]);
        prefmin=min(prefmin,perm[j]);
    }
    for(int cut=lower;cut<=upper;cut++) {
        ++dominoes;
        array<int,M> top{},bottom{},word{},isleaf{};
        int nt=0,nb=0;
        unsigned binary=0;
        for(int i=0;i<n;i++) {
            if(perm[i]>cut){top[nt++]=perm[i]-cut;binary|=1u<<i;}
            else bottom[nb++]=perm[i];
        }
        // Decode the frozen exact marginal representation: cut, binary shuffle,
        // standardized top and bottom permutations. Compare every point.
        int it=0,ib=0;
        for(int i=0;i<n;i++) {
            int value=(binary&(1u<<i))?top[it++]+cut:bottom[ib++];
            if(value!=perm[i])throw runtime_error("encoding roundtrip failed");
        }
        ++roundtrips;
        int maximum=0;
        for(int i=nt-1;i>=0;i--) {
            if(top[i]>maximum)isleaf[top[i]]=1;
            maximum=max(maximum,top[i]);
        }
        for(int v=1;v<=nt;v++)word[v-1]=isleaf[v]?0:1;
        ++counts[0][0];
        int first=0;while(first<nt && !word[first])++first;
        if(first==nt){++counts[1][nt];continue;}
        ++counts[2][first];
        array<int,M> runs{};int nr=0,i=first;
        while(i<nt) {
            while(i<nt && word[i])++i;
            int zeroes=0;while(i<nt && !word[i]){++i;++zeroes;}
            if(zeroes==0)throw runtime_error("invalid top value word");
            runs[nr++]=zeroes-1;
        }
        ++counts[3][runs[nr-1]];
        for(int r=0;r+1<nr;r++)++counts[4][runs[r]];
    }
}

void generate(int n) {
    if(n==goal){visit(n);return;}
    int last=first132end(n);
    for(int slot=0;slot<=last;slot++) {
        for(int j=n;j>slot;j--)perm[j]=perm[j-1];
        perm[slot]=n+1;
        generate(n+1);
        for(int j=slot;j<n;j++)perm[j]=perm[j+1];
    }
}

int main(int argc,char**argv) {
    int limit=argc>1?atoi(argv[1]):10;
    if(limit<0||limit>14)return 64;
    cerr<<"pid="<<getpid()<<" max_n="<<limit<<"\n";
    const U expected[]={1,1,2,6,23,103,513,2762,15793,94776,591950,3824112,25431452,173453058,1209639642};
    for(goal=0;goal<=limit;goal++) {
        counts={};avoiders=dominoes=roundtrips=0;
        auto start=chrono::steady_clock::now();
        generate(0);
        if(avoiders!=expected[goal])throw runtime_error("A061552 mismatch");
        double secs=chrono::duration<double>(chrono::steady_clock::now()-start).count();
        cout<<"{\"n\":"<<goal<<",\"avoiders\":"<<avoiders<<",\"dominoes\":"<<dominoes<<",\"roundtrips\":"<<roundtrips<<",\"seconds\":"<<secs<<",\"series\":{";
        const char* names[]={"A","F","S","T","P"};
        for(int j=0;j<5;j++) {
            if(j)cout<<",";
            cout<<"\""<<names[j]<<"\":{";bool comma=false;
            for(int u=0;u<M;u++)if(counts[j][u]) {
                if(comma)cout<<",";comma=true;
                cout<<"\""<<u<<"\":"<<counts[j][u];
            }
            cout<<"}";
        }
        cout<<"}}"<<endl;
    }
}

// Component DP on a two-block Boolean cube. See PROOF.md for the search order.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Mask = uint32_t;
using Family = std::vector<Mask>;
static int count(Mask x) { return __builtin_popcount(x); }
static Mask low(int n) { return (Mask(1) << n) - 1; }

struct Member { Mask set; int x, y; };
struct Finder {
    int a, b, colour, limit;
    std::string grid;
    std::vector<Family> best;
    Family answer;
    int index(int x, int y) const { return y * (a + 1) + x; }
    bool matches(int x, int y) const { return grid[index(x,y)] == '0' + colour; }
    bool extend(int start, int x, int y, const std::vector<Member>& ideals) {
        // New element has a predecessor ideal. If this is a nonempty component,
        // its old top is excluded, ensuring an incomparability edge to the prefix.
        int choices = ideals.size() == 1 ? 1 : int(ideals.size()) - 1;
        for (int p = 0; p < choices; ++p) {
            std::vector<Member> supersets;
            for (auto d : ideals)
                if ((d.set & ideals[p].set) == ideals[p].set) supersets.push_back(d);
            for (int dy=0; dy<=b-y; ++dy) for (int dx=(dy==0); dx<=a-x; ++dx) {
                if (!matches(x+dx,y+dy)) continue;
                bool good = true;
                for (auto d : supersets)
                    if (!matches(d.x+dx,d.y+dy)) { good=false; break; }
                if (!good) continue;
                Mask block = (low(dx)<<x) | ((low(dy)<<y)<<a);
                auto next = ideals;
                for (auto d : supersets) next.push_back({d.set|block,d.x+dx,d.y+dy});
                auto& target = best[index(x+dx,y+dy)];
                if (best[start].size() + next.size() - 1 > target.size()) {
                    target = best[start];
                    for (size_t i=1; i<next.size(); ++i) target.push_back(next[i].set);
                    if (target.size() > answer.size()) answer = target;
                    if (int(answer.size()) >= limit) return true;
                }
                if (extend(start,x+dx,y+dy,next)) return true;
            }
        }
        return false;
    }
    Family run() {
        best.resize(grid.size());
        for (int y=0; y<=b; ++y) for (int x=0; x<=a; ++x) {
            if (!matches(x,y)) continue;
            int s=index(x,y);
            Mask base=low(x)|(low(y)<<a);
            if (best[s].empty()) best[s]={base};
            if (best[s].size()>answer.size()) answer=best[s];
            if (int(answer.size())>=limit || extend(s,x,y,{{base,x,y}})) return answer;
        }
        return answer;
    }
};
int main() {
    int a,b,c,t; std::string grid;
    while (std::cin>>a>>b>>c>>t>>grid) {
        if (a<0 || b<0 || a+b>25 || (c!=0 && c!=1) || t<1 ||
            grid.size()!=size_t((a+1)*(b+1)) || grid.find_first_not_of("01")!=grid.npos) return 2;
        Finder solver{a,b,c,t,grid};
        auto f=solver.run();
        std::cout<<f.size(); for (Mask s : f) std::cout<<' '<<s;
        std::cout<<std::endl;
    }
}

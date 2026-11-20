// Three vector weights in the ordinal-component recurrence of e1183b2.
#pragma once
#include <array>
#include <algorithm>
#include <cstdint>
#include <vector>
#include <string>
#include <stdexcept>

using Point = std::array<int,3>;
using Mask = uint32_t;
using Family = std::vector<Mask>;
inline Mask ones(int k) { return (Mask(1)<<k)-1; }
struct Ideal {
    Mask member;
    int cell;
};

class Finder {
    Point shape, stride;
    const std::string &table;
    char colour;
    int threshold;
    std::vector<Family> best;
    Family maximum;

    int cell(Point p) const { return p[0] + p[1]*stride[1] + p[2]*stride[2]; }
    Mask prefix(Point p) const {
        return ones(p[0]) | (ones(p[1])<<shape[0]) | (ones(p[2])<<(shape[0]+shape[1]));
    }
    bool extend(int start, Point top, const std::vector<Ideal>& ideals) {
        int count = ideals.size() == 1 ? 1 : int(ideals.size())-1;
        for (int i=0; i<count; ++i) {
            std::vector<Ideal> supersets;
            for (auto q: ideals)
                if ((q.member & ideals[i].member)==ideals[i].member) supersets.push_back(q);
            for (int z=top[2]; z<=shape[2]; ++z)
            for (int y=top[1]; y<=shape[1]; ++y)
            for (int x=top[0]+(z==top[2] && y==top[1]); x<=shape[0]; ++x) {
                Point end{x,y,z};
                int dest=cell(end), shift=dest-cell(top);
                if (table[dest]!=colour) continue;
                if (std::any_of(supersets.begin(),supersets.end(),
                    [&](Ideal q){return table[q.cell+shift]!=colour;})) continue;
                Mask weight=prefix(end)^prefix(top);
                auto next=ideals;
                for (auto q: supersets) next.push_back({q.member|weight,q.cell+shift});
                if (best[start].size()+next.size()-1 > best[dest].size()) {
                    best[dest]=best[start];
                    for (size_t k=1;k<next.size();++k) best[dest].push_back(next[k].member);
                    if (best[dest].size()>maximum.size()) maximum=best[dest];
                    if (int(maximum.size())>=threshold) return true;
                }
                if (extend(start,end,next)) return true;
            }
        }
        return false;
    }
public:
    Finder(Point p, const std::string &word, int c, int h):
        shape(p),stride{1,p[0]+1,(p[0]+1)*(p[1]+1)},table(word),colour('0'+c),
        threshold(h),best(word.size()) {}
    Family run() {
        for(int z=0;z<=shape[2];++z) for(int y=0;y<=shape[1];++y)
        for(int x=0;x<=shape[0];++x) {
            Point p{x,y,z};
            int s=cell(p);
            if(table[s]!=colour) continue;
            if(best[s].empty()) best[s]={prefix(p)};
            if(best[s].size()>maximum.size()) maximum=best[s];
            if(int(maximum.size())>=threshold || extend(s,p,{{prefix(p),s}})) return maximum;
        }
        return maximum;
    }
};

#include <iostream>
#include "finder.hpp"
int main() {
    Point p;
    int c,h;
    std::string word;
    while(std::cin>>p[0]>>p[1]>>p[2]>>c>>h>>word) {
        if (*std::min_element(p.begin(),p.end())<0 || p[0]+p[1]+p[2]>23 ||
            c<0 || c>1 || h<1 || word.size()!=size_t((p[0]+1)*(p[1]+1)*(p[2]+1)) ||
            word.find_first_not_of("01")!=word.npos) return 2;
        auto f=Finder(p,word,c,h).run();
        std::cout<<f.size();
        for(auto s:f) std::cout<<' '<<s;
        std::cout<<std::endl;
    }
}

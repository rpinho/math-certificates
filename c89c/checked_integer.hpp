// Signed 128-bit integer arithmetic with mandatory overflow rejection.
// Successful checks are exact; an oversized certificate fails explicitly.
#pragma once
#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <string>
class CheckedInteger {
    __int128 v;
    explicit CheckedInteger(__int128 x, bool): v(x) {}
public:
    CheckedInteger(long long x=0): v(x) {}
    friend CheckedInteger operator+(CheckedInteger a,CheckedInteger b){__int128 z;if(__builtin_add_overflow(a.v,b.v,&z))throw std::overflow_error("integer addition overflow");return CheckedInteger(z,true);}
    friend CheckedInteger operator-(CheckedInteger a,CheckedInteger b){__int128 z;if(__builtin_sub_overflow(a.v,b.v,&z))throw std::overflow_error("integer subtraction overflow");return CheckedInteger(z,true);}
    friend CheckedInteger operator*(CheckedInteger a,CheckedInteger b){__int128 z;if(__builtin_mul_overflow(a.v,b.v,&z))throw std::overflow_error("integer multiplication overflow");return CheckedInteger(z,true);}
    CheckedInteger& operator+=(CheckedInteger b){*this=*this+b;return *this;}
    CheckedInteger& operator-=(CheckedInteger b){*this=*this-b;return *this;}
    friend bool operator<(CheckedInteger a,CheckedInteger b){return a.v<b.v;}
    friend bool operator<=(CheckedInteger a,CheckedInteger b){return a.v<=b.v;}
    friend std::istream& operator>>(std::istream& in,CheckedInteger& a){
        std::string s;if(!(in>>s))return in;
        bool neg=s[0]=='-';size_t pos=(s[0]=='-'||s[0]=='+');CheckedInteger z;
        if(pos==s.size())throw std::runtime_error("invalid integer");
        for(;pos<s.size();pos++){if(s[pos]<'0'||s[pos]>'9')throw std::runtime_error("invalid integer");z=z*10+CheckedInteger(s[pos]-'0');}
        a=neg?CheckedInteger(0)-z:z;return in;
    }
    friend std::ostream& operator<<(std::ostream& out,CheckedInteger a){
        if(a.v==0)return out<<'0';
        bool neg=a.v<0;unsigned __int128 u=neg?-(a.v+1):a.v;if(neg)u++;
        std::string s;while(u){s.push_back('0'+u%10);u/=10;}if(neg)s.push_back('-');std::reverse(s.begin(),s.end());return out<<s;
    }
};

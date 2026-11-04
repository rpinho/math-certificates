// Clean-room component rules, derived solely from the supplied proof prose.
#pragma once
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using U=__uint128_t; using K=uint64_t;
inline void need(bool b,const char* m){if(!b)throw std::runtime_error(m);}
inline std::string dec(U a){if(!a)return "0";std::string s;while(a){s.push_back('0'+a%10);a/=10;}std::reverse(s.begin(),s.end());return s;}
inline U plus(U a,U b){need(~U(0)-a>=b,"sum overflow");return a+b;}
inline U weight(U a,unsigned k,uint64_t M,bool upper){
 if(!k)return a; unsigned s=27*k; uint64_t q=k==1?M:M*M;
 need(a<(U(1)<<107),"weight capacity"); U mask=(U(1)<<s)-1,v=(a&mask)*q;
 return ((a>>s)*q+(v>>s))+(upper&&bool(v&mask));
}
struct Move{K key; uint8_t k; bool done;};
struct Moves{std::array<Move,5> a;unsigned n=0;void add(K key,int k,bool done=false){need(n<5,"move count");a[n++]={key,uint8_t(k),done};}};
// Slots are in geometric boundary order, with adjacent incoming ports p,p+1.
// 0=empty,1=open pair,2=close pair,3=singleton; flags above the slots.
inline Moves vertex(K key,int slots,int p,bool right,bool up,bool terminal,int flagbit){
 int lab[32]={},stack[32],ns=0,nc=0,cnt[32]={};
 for(int i=0;i<slots;i++){
  int t=(key>>(2*i))&3;
  if(t==1){lab[i]=++nc;stack[ns++]=nc;cnt[nc]=2;}
  if(t==2){need(ns>0,"bracket underflow");lab[i]=stack[--ns];}
  if(t==3){lab[i]=++nc;cnt[nc]=1;}
 }
 need(ns==0,"unclosed pair");
 int a=lab[p],b=lab[p+1],incoming=bool(a)+bool(b);
 K flags=key>>(2*slots); Moves ans;
 for(int t=0;t<=int(terminal);t++){
  if(t&&(flags&(1u<<flagbit)))continue;
  for(int out=0;out<4;out++){
   if((out&1)&&!right)continue;if((out&2)&&!up)continue;
   int k=bool(out&1)+bool(out&2), degree=incoming+k;
   if(t?degree!=1:(degree!=0&&degree!=2))continue;
   int v[32];std::copy(lab,lab+slots,v);v[p]=v[p+1]=0;
   bool complete=false;int id=0;
   if(incoming==2){
    if(a==b)continue;
    complete=cnt[a]==1&&cnt[b]==1;
    for(int i=0;i<slots;i++)if(v[i]==b)v[i]=a;
   }else if(incoming==1){id=a?a:b;complete=t&&cnt[id]==1;}
   else if(k)id=nc+1;
   if(out&1)v[p]=id;if(out&2)v[p+1]=id;
   K nf=flags|(t?(1u<<flagbit):0);
   if(complete){bool empty=true;for(int i=0;i<slots;i++)empty&=v[i]==0;if(empty&&nf==3)ans.add(0,k,true);continue;}
   int counts[34]={},seen[34]={};for(int i=0;i<slots;i++)counts[v[i]]++;
   K dest=nf<<(2*slots);int ckstack[32],sp=0;
   for(int i=0;i<slots;i++)if(v[i]){
    int c=counts[v[i]],code;need(c==1||c==2,"component size");
    if(c==1)code=3;
    else if(!seen[v[i]]){code=1;ckstack[sp++]=v[i];}
    else{code=2;need(sp&&ckstack[--sp]==v[i],"crossed pairs");}
    seen[v[i]]=1;dest|=K(code)<<(2*i);
   }
   ans.add(dest,k);
  }
 }
 return ans;
}
inline Moves strip_moves(K key,int h,int r){
 int slots=h+1;K mask=(K(1)<<(2*slots))-1;
 if(r==0){need((key&3)==0,"row zero incoming");Moves m;m.add(key,0);if(!(key&(K(1)<<(2*slots))))m.add(key|3|(K(1)<<(2*slots)),1);return m;}
 Moves m=vertex(key,slots,r-1,true,r<h,r==h,1);
 if(r==h)for(unsigned i=0;i<m.n;i++)if(!m.a[i].done){K k=m.a[i].key;need(((k>>(2*h))&3)==0,"top outgoing");m.a[i].key=(k&~mask)|((k<<2)&mask);}
 return m;
}

// Fresh C47 floating search implementation, 2026-11-08.
// Standard coordinate-box formula (Tomar Lemma 6.2, following Lin).
// No third-party source included. Not an exact verifier.
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <vector>
using namespace std;
struct Point {double x,y,m;};
struct Rectangle {double l,r,b,t,a,z,c,d;};
struct Event {double x;int lo,hi,delta;};
struct Sweep {
 vector<int> count; vector<double> length,ys;
 Sweep(vector<double> v):ys(v),count(v.size()*4+8),length(v.size()*4+8){}
 void add(int k,int l,int r,int a,int b,int d){
  if(a>=r||b<=l)return;
  if(a<=l&&r<=b)count[k]+=d;
  else {int mid=(l+r)/2;add(k*2,l,mid,a,b,d);add(k*2+1,mid,r,a,b,d);}
  length[k]=count[k]?ys[r]-ys[l]:(r-l==1?0:length[k*2]+length[k*2+1]);
 }
};
static void unique_sort(vector<double>& a){sort(a.begin(),a.end());a.erase(unique(a.begin(),a.end()),a.end());}
static vector<Rectangle> enumerate(int n,const double* p,double px,double py,double reach){
 double mass=0;for(int i=0;i<n;i++)mass+=p[3*i+2];
 double R=sqrt((floor(reach/px)+1)*(floor(reach/py)+1)*mass/4)+1e-8;
 vector<Point> points; vector<double> xs,ys;
 int nx=(int)ceil(R/px)+1,ny=(int)ceil(R/py)+1;
 for(int i=0;i<n;i++)for(int a=-nx;a<=nx;a++)for(int b=-ny;b<=ny;b++){
  double x=p[3*i]+a*px,y=p[3*i+1]+b*py;
  if(x>=-R&&x<=px+R&&y>=-R&&y<=py+R){points.push_back({x,y,p[3*i+2]});xs.push_back(x);ys.push_back(y);}
 }
 unique_sort(xs);unique_sort(ys);int X=xs.size(),Y=ys.size();
 vector<double> grid(X*Y,0),pref((X+1)*(Y+1),0);
 for(auto p:points){int a=lower_bound(xs.begin(),xs.end(),p.x)-xs.begin();int b=lower_bound(ys.begin(),ys.end(),p.y)-ys.begin();grid[a*Y+b]+=p.m;}
 for(int a=0;a<X;a++){double acc=0;for(int b=0;b<Y;b++){acc+=grid[a*Y+b];pref[(a+1)*(Y+1)+b+1]=pref[a*(Y+1)+b+1]+acc;}}
 vector<Rectangle> rects;rects.reserve(50000);vector<double> strip(Y+1);
 for(int a=0;a<X;a++)for(int b=a;b<X&&xs[b]-xs[a]<=reach;b++){
  double dx=xs[b]-xs[a];
  for(int j=0;j<=Y;j++)strip[j]=pref[(b+1)*(Y+1)+j]-pref[a*(Y+1)+j];
  for(int c=0;c<Y;c++)for(int d=c;d<Y&&ys[d]-ys[c]<=reach;d++){
   double m=strip[d+1]-strip[c],dy=ys[d]-ys[c];
   if(m<=max(dx*dx,dy*dy))continue;
   double rho=.5*sqrt(m),l=max(0.,xs[b]-rho),r=min(px,xs[a]+rho),bot=max(0.,ys[d]-rho),top=min(py,ys[c]+rho);
   if(l<r&&bot<top)rects.push_back({l,r,bot,top,xs[a],xs[b],ys[c],ys[d]});
  }
 }
 return rects;
}
static double area(const vector<Rectangle>& rs){
 if(rs.empty())return 0;vector<double> ys;ys.reserve(rs.size()*2);
 for(auto r:rs){ys.push_back(r.b);ys.push_back(r.t);}unique_sort(ys);vector<Event> ev;ev.reserve(rs.size()*2);
 for(auto r:rs){int a=lower_bound(ys.begin(),ys.end(),r.b)-ys.begin(),b=lower_bound(ys.begin(),ys.end(),r.t)-ys.begin();ev.push_back({r.l,a,b,1});ev.push_back({r.r,a,b,-1});}
 sort(ev.begin(),ev.end(),[](const Event&a,const Event&b){return a.x<b.x;});Sweep tree(ys);double result=0,prev=ev[0].x;
 for(auto e:ev){result+=(e.x-prev)*tree.length[1];tree.add(1,0,ys.size()-1,e.lo,e.hi,e.delta);prev=e.x;}return result;
}
extern "C" double evaluate(int n,const double* p,double px,double py,double reach,int* nr,const char* output){
 auto rs=enumerate(n,p,px,py,reach);if(nr)*nr=rs.size();
 if(output){FILE* f=fopen(output,"w");if(!f)return -1;for(auto r:rs)fprintf(f,"%.17g %.17g %.17g %.17g\n",r.a,r.z,r.c,r.d);fclose(f);}
 return area(rs);
}
extern "C" void holes(int n,const double* p,double px,double py,double reach,int k,unsigned char* out){
 auto rs=enumerate(n,p,px,py,reach);vector<int> delta((k+1)*(k+1));
 for(auto r:rs){int a=max(0,(int)ceil(r.l/px*k-.5)),b=min(k,(int)floor(r.r/px*k-.5)+1),c=max(0,(int)ceil(r.b/py*k-.5)),d=min(k,(int)floor(r.t/py*k-.5)+1);
 if(a<b&&c<d){delta[a*(k+1)+c]++;delta[b*(k+1)+c]--;delta[a*(k+1)+d]--;delta[b*(k+1)+d]++;}}
 for(int a=0;a<k;a++)for(int b=0;b<k;b++){int &v=delta[a*(k+1)+b];if(a)v+=delta[(a-1)*(k+1)+b];if(b)v+=delta[a*(k+1)+b-1];if(a&&b)v-=delta[(a-1)*(k+1)+b-1];out[a*k+b]=v>0;}
}

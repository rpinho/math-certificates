// Separately written (same agent): reconstruct and check the matcher involution.
vector<uint32_t> checked_complement(const vector<BaseNode>&base){
 const int phi[8]={1,0,3,2,5,4,7,6};
 vector<uint32_t>flip(base.size(),UINT32_MAX),queue={0};flip[0]=0;
 for(size_t head=0;head<queue.size();++head){
  uint32_t q=queue[head],f=flip[q];
  for(int a=0;a<8;++a){
   int u=base[q].out[a],v=base[f].out[phi[a]];
   need((u<0)==(v<0),"complement missing-edge mismatch");if(u<0)continue;
   if(flip[u]==UINT32_MAX){flip[u]=v;queue.push_back(u);}
   else need(flip[u]==uint32_t(v),"inconsistent complement map");
  }
 }
 need(queue.size()==base.size(),"complement map does not cover matcher");
 for(size_t q=0;q<base.size();++q){
  need(flip[flip[q]]==q,"complement is not an involution");
  Run r=untag(base[q].run);if(r.last<4)r.last^=1;
  r.mask=((r.mask&1)<<1)|((r.mask&2)>>1);if(r.ban>=0)r.ban^=1;
  need(base[flip[q]].run==tag(r),"complement run-memory mismatch");
 }
 cout<<"MATCHER_COMPLEMENT_PASS states="<<base.size()<<endl;return flip;
}

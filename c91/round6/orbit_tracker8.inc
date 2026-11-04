// Separately written (same agent) frontier engine, using COMPLETED scores.
// A=cost(Q)-cost(actual)+lag; G=gap(Q)-gap(actual)+lag.
// Search stores uncompleted scores and uses a different variable-stride code.
vector<Row> gap_record_graph(const vector<BaseNode>&run,int W,int B,int S,int T,
                             bool completion,uint32_t expected,const vector<int>&lagcaps={}){
 const int inf=1000000,H=max(4,W),unknown_kind=2*(S+T+1);
 const auto completed_cap=[&](int lag){return lagcaps.empty()?(completion?B:B+lag):lagcaps.at(lag-1)+lag;};
 const auto flip=checked_complement(run);
 need(S>=0&&S<=3&&T>=1&&T<=3&&unknown_kind<16,"gap record parameters");
 State initial{};initial.base=0;
 vector<State>states={initial};states.reserve(expected);vector<Row>rows;rows.reserve(expected);
 unordered_map<State,uint32_t,StateHash>seen;seen.reserve(expected);seen[initial]=0;
 for(size_t index=0;index<states.size();++index){
  const State before=states[index];const Run memory=untag(run[before.base].run);
  Candidate old[2][7];
  for(int side=0;side<2;++side)for(int r=1;r<=W;++r){
   const int code=before.score[2*(r-1)+side];if(!code)continue;
   const int z=code-1,kind=z&15;need(kind<=unknown_kind,"internal score kind");
   old[side][r]={z>>4,kind==unknown_kind?inf:2*(kind/2-S),
                kind==unknown_kind?1:((kind&1)?1:-1)};
  }
  Row row{};row.to.fill(-1);
  for(int a=0;a<8;++a){
   int next_run=run[before.base].out[a];if(next_run<0)continue;
   Candidate fresh[2][7];bool reject=false;
   auto offer=[&](int side,int r,Candidate k,int dA,int dG){
    if(k.cost==inf)return;
    k.cost+=dA;if(k.gaps!=inf)k.gaps+=dG;
    need(k.gaps==inf||k.gaps%2==0,"completed gap parity");
    if(k.cost<0||(k.cost==0&&k.gaps!=inf&&
       (k.gaps<0||(k.gaps==0&&k.order<0))))reject=true;
    if(r==0||k.cost>completed_cap(r))return;
    if(k.gaps==inf||k.gaps>2*T){k.gaps=inf;k.order=1;}
    if(k.gaps< -2*S){k.gaps=-2*S;k.order=-1;}
    if(k<fresh[side][r])fresh[side][r]=k;
   };
   if(a<4){
    int e=a>=2;
    unsigned extended[2]={(unsigned(before.x)<<1)|unsigned(xb[a]),
                          (unsigned(before.y)<<1)|unsigned(yb[a])};
    for(int side=0;side<2;++side){
     int opposite=side?xb[a]:yb[a];
     for(int q=1;q<=W;++q){
      bool pending=q<=before.run&&memory.last==(side?6:4);
      for(int r=0;r<=q;++r){
       for(int position=r;position<=q;++position){
        int mismatch=int((extended[side]>>position)&1)!=opposite;
        offer(side,r,old[side][q],mismatch-e,0);
       }
       if(pending){
        int mismatch=int((extended[side]>>q)&1)!=opposite;
        offer(side,r,Candidate{0,0,-1},mismatch-e,0);
       }
      }
      if(q<W)offer(side,q+1,old[side][q],2-e,2);
      offer(1-side,1,old[side][q],2-e,2);
     }
     offer(side,1,Candidate{0,0,1},2-e,2);
    }
    for(int q=1;q<W&&q<=before.run;++q){
     if(memory.last==4)offer(0,q+1,Candidate{0,0,1},2-e,2);
     if(memory.last==6)offer(1,q+1,Candidate{0,0,-1},2-e,2);
    }
   }else{
    int emitted=a<6?0:1,other=1-emitted;
    int bit=emitted?yb[a]:xb[a];unsigned buffer=emitted?before.x:before.y;
    for(int q=1;q<=W;++q){
     for(int r=0;r<=min(W,q+1);++r)offer(emitted,r,old[emitted][q],0,0);
     for(int r=0;r<=q;++r){
      offer(other,r,old[other][q],0,0);
      for(int position=r;position<q;++position){
       int mismatch=int((buffer>>position)&1)!=bit;
       offer(other,r,old[other][q],mismatch-2,-2);
      }
     }
    }
   }
   for(int side=0;side<2;++side)for(int q=W;q>=1;--q){
    Candidate from=fresh[side][q];
    for(int r=q-1;r>=0;--r)offer(side,r,from,0,0);
   }
   if(reject)continue;
   State after=before;after.base=next_run;after.score.fill(0);
   for(int side=0;side<2;++side)for(int r=1;r<=W;++r){
    Candidate k=fresh[side][r];if(k.cost==inf)continue;
    need(k.cost>=0&&k.cost<=completed_cap(r),"completed cost range");
    need(k.gaps==inf||(k.gaps>=-2*S&&k.gaps<=2*T),"completed gap range");
    int kind=k.gaps==inf?unknown_kind:2*(k.gaps/2+S)+(k.order>0);
    int code=1+16*k.cost+kind;need(code>0&&code<32768,"score encoding");
    after.score[2*(r-1)+side]=code;
   }
   int direction=a<4?0:(a<6?1:2),previous=memory.last==4?1:(memory.last==6?2:0);
   after.run=direction?min(W,previous==direction?int(before.run)+1:1):0;
   for(int side=0;side<2;++side){
    int bit=side?yb[a]:xb[a];if(bit<0)continue;
    int length=side?before.ny:before.nx;unsigned history=side?before.y:before.x;
    for(int lag=1;lag<=3;++lag)if(length>=lag)
     row.feature[a][lag-1]+=int((history>>(lag-1))&1)==bit?1:-1;
    if(length>=3)row.feature[a][3]+=parity(((history&7)<<1)|unsigned(bit))?-1:1;
    if(length>=4){
     int spin=bit?-1:1,b1=(history&1)?-1:1,b2=(history&2)?-1:1,
         b3=(history&4)?-1:1,b4=(history&8)?-1:1;
     row.feature[a][4]+=spin*b4;
     row.feature[a][5]+=spin*b1*b2*b4;
     row.feature[a][6]+=spin*b1*b3*b4;
     row.feature[a][7]+=spin*b2*b3*b4;
    }
    int next_length=min(H,length+1),next_bits=((history<<1)|unsigned(bit))&((1<<H)-1);
    if(side){after.ny=next_length;after.y=next_bits;}
    else{after.nx=next_length;after.x=next_bits;}
   }
   bool complemented=after.nx?(after.x&1):(after.ny?(after.y&1):false);
   if(complemented){after.base=flip[after.base];after.x^=(1U<<after.nx)-1;after.y^=(1U<<after.ny)-1;}
   auto p=seen.emplace(after,states.size());if(p.second)states.push_back(after);
   row.to[a]=p.first->second;need(states.size()<=expected,"too many gap-record states");
  }
  rows.push_back(row);
  if(index%1000000==0)cout<<"gap_record_rows "<<index<<" reachable "<<states.size()<<endl;
 }
 need(rows.size()==expected,"wrong gap-record state count");
 cout<<"gap_record_full "<<rows.size()<<endl;return rows;
}

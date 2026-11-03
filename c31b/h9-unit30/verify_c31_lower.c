/* Separately written (same agent) exact lower-potential checker, direct k^2 sums.
 * No code imported from Jack's producer or this job's precision variant.
 * The class map uses a full rank->orbit array, rather than the producer's
 * intermediate F-space. Every first-letter case is evaluated literally. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

static int alphabet,history,length,nthreads,shift;
static uint64_t completions[21][5],ranks,classes,words,*flags,*potential,unit;
static uint32_t *prefix,*orbit;
static int64_t required;
static void fail(const char *why){fprintf(stderr,"REJECTED: %s\n",why);exit(1);}
static double wall(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}

static void counts(void){
    for(int used=0;used<=alphabet;used++)completions[0][used]=1;
    for(int remaining=1;remaining<=length;remaining++)for(int used=0;used<=alphabet;used++){
        uint64_t a,b=used<alphabet?completions[remaining-1][used+1]:0;
        if(__builtin_mul_overflow((uint64_t)used,completions[remaining-1][used],&a)||__builtin_add_overflow(a,b,&completions[remaining][used]))fail("rank count overflow");
    }
    ranks=completions[length][0];
}
static uint64_t rank_pair(const unsigned char *a,const unsigned char *b){
    signed char renamed[4]={-1,-1,-1,-1};int used=0;uint64_t rank=0;
    /* Each smaller existing label leaves "used" letters available in the
     * remaining suffix; a new label is exactly the next unused label. */
    for(int pos=0;pos<length;pos++){
        int raw=pos<history?a[pos]:b[pos-history];int label=renamed[raw];
        if(label<0){label=used;renamed[raw]=label;}
        rank+=(uint64_t)label*completions[length-pos-1][used];
        if(label==used)used++;
    }
    return rank;
}
static void unrank_word(uint64_t rank,unsigned char *s,unsigned char *used_after){
    int used=0;
    for(int pos=0;pos<length;pos++){
        int selected=-1;
        for(int label=0;label<=used&&label<alphabet;label++){
            int after=used+(label==used);uint64_t block=completions[length-pos-1][after];
            if(rank<block){selected=label;used=after;break;}rank-=block;
        }
        if(selected<0)fail("unrank outside range");s[pos]=selected;used_after[pos]=used;
    }
}
static void next_word(unsigned char *s,unsigned char *used_after){
    for(int pos=length-1;pos>=1;pos--){
        int used=used_after[pos-1];int top=used<alphabet?used:alphabet-1;
        if(s[pos]<top){s[pos]++;used=s[pos]==used?used+1:used;used_after[pos]=used;
            for(int j=pos+1;j<length;j++){s[j]=0;used_after[j]=used;}return;
        }
    }
    fail("next_word past end");
}
static uint32_t dense(uint64_t rank){
    uint64_t word=rank/64;unsigned bit=rank%64;uint64_t mask=bit?((1ULL<<bit)-1):0;
    return prefix[word]+__builtin_popcountll(flags[word]&mask);
}
static inline uint64_t value(const unsigned char *a,const unsigned char *b){return potential[orbit[rank_pair(a,b)]];}

typedef struct{uint64_t lo,hi,visited;int phase;int64_t minimum,maximum;} Work;
static void *worker(void *ptr){
    Work *work=ptr;if(work->lo==work->hi)return NULL;
    unsigned char s[20],used[20],a[10],b[10];unrank_word(work->lo,s,used);
    work->visited=0;work->minimum=INT64_MAX;work->maximum=INT64_MIN;double last=wall();
    for(uint64_t rank=work->lo;rank<work->hi;rank++){
        if(work->phase==0){
            uint64_t swapped=rank_pair(s+history,s);
            if(rank<=swapped)flags[rank/64]|=1ULL<<(rank%64);
        }else if(work->phase==1){
            uint64_t swapped=rank_pair(s+history,s),representative=rank<swapped?rank:swapped;
            orbit[rank]=dense(representative);
        }else if((flags[rank/64]>>(rank%64))&1){
            uint32_t index=dense(rank);uint64_t cur=potential[index],sum=0;int64_t drift;
            if(s[0]==s[history]){
                memcpy(a,s+1,history-1);memcpy(b,s+history+1,history-1);
                for(int c=0;c<alphabet;c++){a[history-1]=c;for(int d=0;d<alphabet;d++){b[history-1]=d;sum+=value(a,b);}}
                drift=(int64_t)(alphabet*alphabet*unit+sum)-(int64_t)(alphabet*alphabet*cur);
            }else{
                uint64_t left=0,right=0;memcpy(a,s+1,history-1);memcpy(b,s+history+1,history-1);
                for(int c=0;c<alphabet;c++){a[history-1]=c;b[history-1]=c;left+=value(a,s+history);right+=value(s,b);}
                drift=(int64_t)(alphabet*(left>right?left:right))-(int64_t)(alphabet*alphabet*cur);
            }
            if(drift<required){fprintf(stderr,"orbit %u drift=%" PRId64 " required=%" PRId64 "\n",index,drift,required);fail("lower potential inequality");}
            if(drift<work->minimum)work->minimum=drift;if(drift>work->maximum)work->maximum=drift;work->visited++;
        }
        if(work->phase<2)work->visited++;
        if(rank+1<work->hi)next_word(s,used);
        if(wall()-last>60){fprintf(stderr,"LOWER phase=%d ranks=%" PRIu64 "/%" PRIu64 " visited=%" PRIu64 "\n",work->phase,rank-work->lo+1,work->hi-work->lo,work->visited);last=wall();}
    }
    return NULL;
}
static void phase(int mode,Work *jobs){
    pthread_t threads[3];uint64_t chunks=(ranks+63)/64;
    for(int t=0;t<nthreads;t++){
        jobs[t]=(Work){.lo=(chunks*t/nthreads)*64,.hi=(chunks*(t+1)/nthreads)*64,.phase=mode};
        if(jobs[t].hi>ranks)jobs[t].hi=ranks;
        if(pthread_create(threads+t,NULL,worker,jobs+t))fail("worker creation failed");
    }
    for(int t=0;t<nthreads;t++)if(pthread_join(threads[t],NULL))fail("worker join failed");
    if(mode<2){uint64_t total=0;for(int t=0;t<nthreads;t++)total+=jobs[t].visited;if(total!=ranks)fail("incomplete index construction");}
}
int main(int argc,char **argv){
    if(argc!=8){fprintf(stderr,"usage: verify_c31_lower k h shift required_numerator witness threads expected_classes\n");return 1;}
    alphabet=atoi(argv[1]);history=atoi(argv[2]);shift=atoi(argv[3]);required=strtoll(argv[4],NULL,10);nthreads=atoi(argv[6]);uint64_t expected=strtoull(argv[7],NULL,10);
    if(alphabet<2||alphabet>4||history<2||history>9||shift<1||shift>35||nthreads<1||nthreads>3)fail("parameters");
    length=2*history;unit=1ULL<<shift;counts();if(ranks>4000000000ULL)fail("rank resource cap");words=(ranks+63)/64;
    flags=calloc(words,8);prefix=malloc((words+1)*4);orbit=malloc(ranks*4);if(!flags||!prefix||!orbit)fail("index allocation");
    double start=wall();Work jobs[3];phase(0,jobs);classes=0;
    for(uint64_t i=0;i<words;i++){prefix[i]=classes;classes+=__builtin_popcountll(flags[i]);}prefix[words]=classes;
    if(classes!=expected||classes>=UINT32_MAX)fail("class count / Burnside mismatch");phase(1,jobs);
    potential=malloc(classes*8);if(!potential)fail("potential allocation");FILE *f=fopen(argv[5],"rb");
    if(!f||fread(potential,8,classes,f)!=classes||fgetc(f)!=EOF)fail("witness length");fclose(f);
    for(uint64_t i=0;i<classes;i++)if(potential[i]>(1ULL<<50))fail("potential outside overflow guard");
    fprintf(stderr,"LOWER_INDEX_READY ranks=%" PRIu64 " classes=%" PRIu64 " seconds=%.3f\n",ranks,classes,wall()-start);
    phase(2,jobs);uint64_t visited=0;int64_t minimum=INT64_MAX,maximum=INT64_MIN;
    for(int t=0;t<nthreads;t++){visited+=jobs[t].visited;if(jobs[t].minimum<minimum)minimum=jobs[t].minimum;if(jobs[t].maximum>maximum)maximum=jobs[t].maximum;}
    if(visited!=classes)fail("incomplete class check");
    printf("EXACT_LOWER_PASS k=%d h=%d classes=%" PRIu64 " min_numerator=%" PRId64 " max_numerator=%" PRId64 " denominator=%" PRIu64 " seconds=%.3f\n",alphabet,history,classes,minimum,maximum,(uint64_t)(alphabet*alphabet)*unit,wall()-start);return 0;
}

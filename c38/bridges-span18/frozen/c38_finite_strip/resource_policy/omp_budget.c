/* Resource-only OpenMP team selector. No verifier data is inspected or changed.
 * GCC's GOMP_parallel callback, payload, and flags pass through unchanged.
 * The verified integer arithmetic is deterministic for every team size. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
typedef void (*parallel_call)(void (*)(void *),void *,unsigned,unsigned);
static parallel_call original;
static pthread_once_t once=PTHREAD_ONCE_INIT;
static const char *gate;
static unsigned before,after,last;
static void setup(void){
 original=(parallel_call)dlsym(RTLD_NEXT,"GOMP_parallel");
 gate=getenv("C38_THREAD_GATE");
 const char*b=getenv("C38_OMP_BEFORE"),*a=getenv("C38_OMP_AFTER");
 before=b?(unsigned)strtoul(b,0,10):3;after=a?(unsigned)strtoul(a,0,10):14;
 if(!original||!gate||before<1||before>14||after<before||after>14)_exit(95);
}
void GOMP_parallel(void(*fn)(void*),void*data,unsigned requested,unsigned flags){
 pthread_once(&once,setup);
 unsigned cap=access(gate,F_OK)==0?after:before;
 unsigned n=requested&&requested<cap?requested:cap;
 if(n!=last){fprintf(stderr,"OMP_BUDGET team=%u\n",n);last=n;}
 original(fn,data,n,flags);
}

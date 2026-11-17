/* CNF: "at least K members, closed under union and intersection, all of colour C" for a size-only
   colouring of 2^[n] given by a rank word.  x_S (S of colour C, mask order) are variables 1..N.
   Closure: for incomparable S<T of colour C: (-xS -xT x_{S|T}) or (-xS -xT) if S|T has the other colour;
   same for S&T (binary clause emitted once if both results have the other colour).
   Cardinality: sequential counter s(i,j) = "at least j among first i", only the direction
   s(i,j) -> s(i-1,j) v x_i ; s(i,j) -> s(i-1,j) v s(i-1,j-1); unit s(N,K).
   Optional lex-leader for every transposition (i j), i<j, variable order = mask order:
   over pairs (S, S^bi^bj) with bit i in S, bit j not, ascending S: e0=true,
   e_{p-1} -> (-xS v xS'),  e_{p-1} & xS & xS' -> e_p,  e_{p-1} & -xS & -xS' -> e_p.
   Usage: enc n word C K lex drop out.cnf   (drop = 1-based index of a closure clause to omit, 0 none) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n,C,K,LEX; static long DROP; static char *word; static int *var; static int N;
static long nclauses; static int nvars; static FILE *out; static int pass;
static char buf[256];
static void clause(int k, const int *l){ nclauses++; if(!pass) return; char *p=buf; for(int i=0;i<k;i++) p+=sprintf(p,"%d ",l[i]); strcpy(p,"0\n"); fputs(buf,out);}
static int col(int S){ return word[__builtin_popcount(S)]-'0'; }
static void build(void){
  nclauses=0; long ci=0; int U=1<<n;
  for(int S=0;S<U;S++) if(var[S]) for(int T=S+1;T<U;T++) if(var[T]){
    if((S&T)==S||(S&T)==T) continue;
    int u=S|T, m=S&T, a=-var[S], b=-var[T];
    int cu=var[u]!=0, cm=var[m]!=0;
    if(cu){ ci++; if(ci!=DROP){int l[3]={a,b,var[u]}; clause(3,l);} else if(pass) fprintf(stderr,"dropped closure clause %ld: %d %d %d 0 (S=%d T=%d union=%d)\n",ci,a,b,var[u],S,T,u);}
    if(cm){ ci++; if(ci!=DROP){int l[3]={a,b,var[m]}; clause(3,l);} else if(pass) fprintf(stderr,"dropped closure clause %ld: %d %d %d 0 (S=%d T=%d inter=%d)\n",ci,a,b,var[m],S,T,m);}
    if(!cu||!cm){ ci++; if(ci!=DROP){int l[2]={a,b}; clause(2,l);} else if(pass) fprintf(stderr,"dropped closure clause %ld: %d %d 0 (S=%d T=%d)\n",ci,a,b,S,T);}
  }
  if(pass) fprintf(stderr,"closure clauses %ld\n",ci);
  /* counter: s(i,j) var = N + (i-1)*K + j, i=1..N, j=1..K */
  int nv=N+N*K; int *xs=malloc(sizeof(int)*N); int t=0; for(int S=0;S<U;S++) if(var[S]) xs[t++]=var[S];
  #define SV(i,j) (N+((i)-1)*K+(j))
  for(int i=1;i<=N;i++) for(int j=1;j<=K;j++){
    if(i==1){ if(j==1){int l[2]={-SV(1,1),xs[0]}; clause(2,l);} else {int l[1]={-SV(1,j)}; clause(1,l);} continue; }
    {int l[3]={-SV(i,j),SV(i-1,j),xs[i-1]}; clause(3,l);}
    if(j>=2){int l[3]={-SV(i,j),SV(i-1,j),SV(i-1,j-1)}; clause(3,l);}
  }
  {int l[1]={SV(N,K)}; clause(1,l);}
  if(LEX) for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){
    int e=0; /* 0 = true (start) */
    for(int S=0;S<U;S++){ if(!((S>>i)&1)||((S>>j)&1)||!var[S]) continue;
      int S2=S^(1<<i)^(1<<j); int a=var[S], b=var[S2];
      if(e==0){ int l[2]={-a,b}; clause(2,l); nv++; int f=nv; {int l2[3]={-a,-b,f}; clause(3,l2);} {int l3[3]={a,b,f}; clause(3,l3);} e=f; }
      else { int l[3]={-e,-a,b}; clause(3,l); nv++; int f=nv; {int l2[4]={-e,-a,-b,f}; clause(4,l2);} {int l3[4]={-e,a,b,f}; clause(4,l3);} e=f; }
    }
  }
  nvars=nv; free(xs);
}
int main(int argc,char**argv){
  if(argc!=8){fprintf(stderr,"usage\n");return 2;}
  n=atoi(argv[1]); word=argv[2]; C=atoi(argv[3]); K=atoi(argv[4]); LEX=atoi(argv[5]); DROP=atol(argv[6]);
  if((int)strlen(word)!=n+1){fprintf(stderr,"word length\n");return 2;}
  var=calloc(1<<n,sizeof(int)); N=0; for(int S=0;S<(1<<n);S++) if(col(S)==C) var[S]=++N;
  pass=0; build();
  out=fopen(argv[7],"w"); setvbuf(out,NULL,_IOFBF,1<<24);
  fprintf(out,"p cnf %d %ld\n",nvars,nclauses); pass=1; build(); fclose(out);
  fprintf(stderr,"n=%d word=%s colour=%d K=%d lex=%d N=%d vars=%d clauses=%ld\n",n,word,C,K,LEX,N,nvars,nclauses);
  return 0;
}

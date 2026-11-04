/* ADAPTATION by this job from Vit Planocka's MIT tmx.c.
 * Only the forward sparse-matrix storage/traversal is changed. Exact addition
 * is associative and there is no per-add rounding; per-edge directed products
 * are unchanged. State generation, local case table, backward potential,
 * stopping rule and integer outputs retain the public construction. */
/* tmx.c  --  DUAL EXACT-INTEGER span-resolved SAW bridge transfer matrix.
 *
 * Derived from tmc.c (fp64 point evaluation).  State construction, transition rules,
 * the backward fixed point and the exact-integer tail certificate are byte-identical to
 * tmc.c.  What is NEW is the forward sweep: it is run TWICE in scaled-integer arithmetic
 * with DIRECTED ROUNDING,
 *
 *      value v_i  is represented by an integer numerator n_i  with  v_i = n_i * 2^-S,
 *      lower sweep : every inexact operation rounds DOWN (floor)   -> n_i <= v_i * 2^S
 *      upper sweep : every inexact operation rounds UP   (ceil)    -> n_i >= v_i * 2^S
 *
 * so the sweep output is a RIGOROUS two-sided bracket with NO round-off envelope and no
 * operation-count exponent D.  Everything is exact integer arithmetic in unsigned __int128.
 *
 * WHY EVERY OPERATION IS MONOTONE.  Per column the sweep performs exactly two kinds of
 * arithmetic on the state vector:
 *   (1) edge relaxation   dst[d] += x0^k * src[i]      k in {0,1,2}, x0 > 0, src >= 0
 *   (2) completion accrual res    += ncomp * src[i]    ncomp in {1,2}, src >= 0
 * plus, once per column, the tail functional  <src_stage0 , u>  with u >= 0.
 * There is NO subtraction and NO division anywhere in the sweep (the renewal subtraction
 * lives downstream, in exact Fractions).  Hence x -> (all of the above) is monotone
 * nondecreasing in every state value, and componentwise floor/ceil rounding propagates:
 *     n^lo <= v * 2^S <= n^hi   at every stage of every column, by induction.
 *
 * EXACTNESS OF THE SCALED PRODUCTS.  x0 = M * 2^-27 with M < 2^26, so
 *      k=0:  weight 1        -> exact, no rounding at all
 *      k=1:  n * M  >> 27    -> one directed rounding
 *      k=2:  n * M^2 >> 54   -> one directed rounding
 * The 192-bit product n*M^2 is formed exactly from two 128-bit half-products and then
 * shifted; the remainder bits decide the ceil correction.  The accumulation dst[d] += t
 * is an EXACT integer add - unlike fp64, where every add also rounds.
 *
 * OVERFLOW IS FAIL-CLOSED.  Every state value that is ever used is checked to satisfy
 * n < 2^107 (by OR-reducing the high 64-bit limbs and testing < 2^43), and max in-degree
 * is asserted < 2^20, so no accumulation can wrap 2^128 and every half-product stays in
 * range (proof in the report).  Any violation aborts with a nonzero exit status.
 *
 * Build:  gcc -O2 -march=native -fopenmp -o tmx tmx.c -lm
 * Usage:  ./tmx <l> <Mnum...> [--scale S] [--relstop K] [--fp64] [--out FILE]
 *         ./tmx <l> --states
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#ifdef _OPENMP
#include <omp.h>
#endif

typedef unsigned __int128 u128;

#define MAXL   24
#define MAXNX   4
#define NRHS    2          /* rhs0 = completion vector c, rhs1 = all ones */

/* value guard: every used state numerator must be < 2^GUARD_BITS */
#define GUARD_BITS 107
#define GUARD_HI   (1ULL << (GUARD_BITS - 64))   /* 2^43 */

static int L, NST, NX, NP;
#define SFBIT (2*(L+2))
#define EFBIT (2*(L+2)+1)

static inline int getlab(uint64_t c, int i) { return (int)((c >> (2 * i)) & 3ULL); }
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
                          return t.tv_sec + 1e-9 * t.tv_nsec; }

/* ---------------------------------------------------------------- transitions
 * (identical to tmc.c) */

/* ------------------------------------------------------------ BRACKET INVARIANT
 * matchpos() recovers the arc pairing of a boundary state by bracket matching.
 * It is CORRECT ONLY IF the 1/2 subword of s[0..n-1] is a BALANCED bracket word:
 *
 *   (B1) every prefix has  #{i<p : s[i]==1} >= #{i<p : s[i]==2};
 *   (B2) the totals are equal.
 *
 * This is a theorem about the reachable state set, not an accident of the code:
 * every FREE component occupies exactly two frontier slots, labelled 1 at the
 * lower and 2 at the upper (Invariant I6/I7), and the chord pairing is
 * NON-CROSSING (UNDERCOUNT_PROOF.md Lemma 6.1, an inductive invariant of the 16
 * transition rules).  Chords + non-crossing + lower=1/upper=2 is exactly a
 * balanced bracket word.  See KERNEL_AUDIT.md sec 2 for the full proof.
 *
 * CONSEQUENCE (the bound this array is sized by).  Under (B1)+(B2) every '1'
 * pushed is popped, so the stack never holds more than half the slots:
 *      max depth <= floor(n/2) = floor((l+2)/2) <= (MAXL+2)/2 = MPSTACK.
 *
 * WHAT WENT WRONG BEFORE.  The stack was sized MAXL+4 and NOTHING was checked.
 * If (B1) failed, `st[--sp]` with sp == 0 read st[-1] -- an out-of-bounds read of
 * whatever integer preceded the array in the frame -- and the very next statement
 * `m[j] = i` wrote to m[] at that arbitrary index: an UNBOUNDED out-of-bounds
 * write into trans()'s stack frame.  The bound is now stated and CHECKED, so a
 * violation aborts instead of corrupting.  The check costs one comparison per
 * bracket symbol on a code path dominated by hashing.                          */
#define MPSTACK  ((MAXL + 2) / 2)     /* proved bound on bracket nesting depth */

/* dynamic write counters (diagnostic only; they affect no output) */
static unsigned long long mp_calls = 0, mp_push = 0, mp_mwrite = 0,
                          mp_setpos = 0; static int mp_maxdepth = 0;

static void mp_fail(const char *what, int i, int n, int sp) {
    fprintf(stderr, "FATAL bracket invariant violated in matchpos: %s "
                    "(i=%d n=%d sp=%d MPSTACK=%d L=%d)\n",
            what, i, n, sp, MPSTACK, L);
    exit(12);
}

static void matchpos(const int *s, int n, int *m) {
    int st[MPSTACK], sp = 0;
    mp_calls++;
    if (n < 0 || n > MAXL + 3) mp_fail("slot count out of range", -1, n, sp);
    for (int i = 0; i < n; i++) m[i] = -1;
    for (int i = 0; i < n; i++) {
        if (s[i] == 1) {
            if (sp >= MPSTACK) mp_fail("nesting depth exceeds (MAXL+2)/2", i, n, sp);
            st[sp++] = i; mp_push++;
            if (sp > mp_maxdepth) mp_maxdepth = sp;
        }
        else if (s[i] == 2) {
            if (sp <= 0) mp_fail("unmatched '2' (bracket stack underflow)", i, n, sp);
            int j = st[--sp];
            if (j < 0 || j >= n) mp_fail("matched position out of range", i, n, sp);
            m[i] = j; m[j] = i; mp_mwrite += 2;
        }
    }
    if (sp != 0) mp_fail("unmatched '1' left on the stack", n, n, sp);
}
static inline uint64_t mkcode(const int *E, int V, int sf, int ef) {
    uint64_t c = 0;
    for (int i = 0; i <= L; i++) c |= (uint64_t)E[i] << (2 * i);
    c |= (uint64_t)V << (2 * (L + 1));
    if (sf) c |= 1ULL << SFBIT;
    if (ef) c |= 1ULL << EFBIT;
    return c;
}

static int trans(uint64_t code, int r, uint64_t *out, int *kk, int *ncomp)
{
    int l = L, E[MAXL + 2], E2[MAXL + 2], V, sf, ef;
    for (int i = 0; i <= l; i++) E[i] = getlab(code, i);
    V = getlab(code, l + 1);
    sf = (int)((code >> SFBIT) & 1ULL);
    ef = (int)((code >> EFBIT) & 1ULL);
    int ns = 0; *ncomp = 0;
    int a = E[r], b = V, n = l + 2;
    int s[MAXL + 3], m[MAXL + 3];
    for (int i = 0; i < r; i++) s[i] = E[i];
    s[r] = V;
    for (int i = r; i <= l; i++) s[i + 1] = E[i];

/* Index bound now STATED and CHECKED.  Writes land at arr[_p] (_p < r) or
 * arr[_p-1] (_p > r), so 0 <= _p <= l+1 puts every write inside [0,l] of a
 * MAXL+2 array.  _p == -1 (m[] entry for an UNMATCHED slot -- exactly what the
 * bracket invariant forbids) used to write arr[-1]; it now aborts. */
#define SETPOS(arr,p,val) do { int _p=(p); \
    if (_p < 0 || _p > l + 1) { fprintf(stderr, \
        "FATAL SETPOS index %d outside [0,%d] (l=%d r=%d)\n", _p, l+1, l, r); exit(12); } \
    mp_setpos++; \
    if(_p<r) arr[_p]=(val); \
    else if(_p>r) arr[_p-1]=(val); else { fprintf(stderr,"relabel@kink\n"); exit(3);} } while(0)

    if (r == 0) {
        if (a || b) { fprintf(stderr, "row0 invariant violated\n"); exit(3); }
        out[ns] = mkcode(E, 0, sf, ef); kk[ns++] = 0;
        if (!sf) { out[ns] = mkcode(E, 3, 1, ef); kk[ns++] = 1; }
        return ns;
    }
    if (a == 0 && b == 0) {
        out[ns] = mkcode(E, 0, sf, ef); kk[ns++] = 0;
        if (r < l) { memcpy(E2, E, sizeof(int) * (l + 1)); E2[r] = 1;
                     out[ns] = mkcode(E2, 2, sf, ef); kk[ns++] = 2; }
        else if (!ef) { memcpy(E2, E, sizeof(int) * (l + 1)); E2[r] = 3;
                        out[ns] = mkcode(E2, 0, sf, 1); kk[ns++] = 1; }
        return ns;
    }
    if ((a != 0) != (b != 0)) {
        int x = a ? a : b;
        memcpy(E2, E, sizeof(int) * (l + 1)); E2[r] = x;
        out[ns] = mkcode(E2, 0, sf, ef); kk[ns++] = 1;              /* continue right */
        if (r < l) { memcpy(E2, E, sizeof(int) * (l + 1)); E2[r] = 0;
                     out[ns] = mkcode(E2, x, sf, ef); kk[ns++] = 1; } /* continue up */
        else if (!ef) {
            int xpos = a ? (r + 1) : r;
            if (x == 3) {
                int ok = 1;
                for (int i = 0; i < n; i++) if (i != xpos && s[i]) { ok = 0; break; }
                if (ok) (*ncomp)++;
            } else {
                matchpos(s, n, m);
                memcpy(E2, E, sizeof(int) * (l + 1)); E2[r] = 0;
                SETPOS(E2, m[xpos], 3);
                out[ns] = mkcode(E2, 0, sf, 1); kk[ns++] = 0;
            }
        }
        return ns;
    }
    {   /* both incoming occupied; pb = r (V), pa = r+1 (E[r]) */
        int pb = r, pa = r + 1;
        int arca = (a == 1 || a == 2), arcb = (b == 1 || b == 2);
        if (arca || arcb) matchpos(s, n, m);
        if (arca && arcb) {
            if (m[pa] == pb) return ns;                              /* cycle: forbidden */
            int ma = m[pa], mb = m[pb];
            memcpy(E2, E, sizeof(int) * (l + 1)); E2[r] = 0;
            int lo = ma < mb ? ma : mb, hi = ma < mb ? mb : ma;
            SETPOS(E2, lo, 1); SETPOS(E2, hi, 2);
            out[ns] = mkcode(E2, 0, sf, ef); kk[ns++] = 0;
        } else if (a == 3 && b == 3) {
            int ok = 1;
            for (int i = 0; i < n; i++) if (i != pa && i != pb && s[i]) { ok = 0; break; }
            if (ok) (*ncomp)++;
        } else {
            int arcpos = arca ? pa : pb;
            memcpy(E2, E, sizeof(int) * (l + 1)); E2[r] = 0;
            SETPOS(E2, m[arcpos], 3);
            out[ns] = mkcode(E2, 0, sf, ef); kk[ns++] = 0;
        }
    }
    return ns;
}

/* ---------------------------------------------------------------- sort / hash */

static void radix_u64(uint64_t *a, size_t n, uint64_t *tmp) {
    if (n < 2) return;
    size_t cnt[256]; uint64_t *src = a, *dst = tmp;
    for (int pass = 0; pass < 7; pass++) {
        int sh = pass * 8;
        memset(cnt, 0, sizeof cnt);
        for (size_t i = 0; i < n; i++) cnt[(src[i] >> sh) & 255]++;
        if (cnt[(src[0] >> sh) & 255] == n) continue;
        size_t sum = 0;
        for (int j = 0; j < 256; j++) { size_t c = cnt[j]; cnt[j] = sum; sum += c; }
        for (size_t i = 0; i < n; i++) dst[cnt[(src[i] >> sh) & 255]++] = src[i];
        uint64_t *t = src; src = dst; dst = t;
    }
    if (src != a) memcpy(a, src, n * sizeof(uint64_t));
}
static size_t uniq(uint64_t *a, size_t n) {
    if (!n) return 0; size_t w = 1;
    for (size_t i = 1; i < n; i++) if (a[i] != a[w - 1]) a[w++] = a[i];
    return w;
}
typedef struct { uint64_t *key; uint32_t *val; uint64_t mask; } HMap;
static inline uint64_t hmix(uint64_t x) {
    x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33;
    x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x;
}
static void hm_build(HMap *h, const uint64_t *codes, size_t n) {
    uint64_t cap = 16; while (cap < n * 2 + 8) cap <<= 1;
    h->mask = cap - 1;
    h->key = (uint64_t *)calloc(cap, 8);
    h->val = (uint32_t *)malloc(cap * 4);
    if (!h->key || !h->val) { fprintf(stderr, "hash OOM\n"); exit(2); }
    for (size_t i = 0; i < n; i++) {
        uint64_t k = codes[i] + 1, j = hmix(k) & h->mask;
        while (h->key[j]) j = (j + 1) & h->mask;
        h->key[j] = k; h->val[j] = (uint32_t)i;
    }
}
static inline uint32_t hm_get(const HMap *h, uint64_t code) {
    uint64_t k = code + 1, j = hmix(k) & h->mask;
    while (h->key[j]) { if (h->key[j] == k) return h->val[j]; j = (j + 1) & h->mask; }
    fprintf(stderr, "hash miss\n"); exit(4);
}

/* ---------------------------------------------------------------- state */

static uint64_t *codes[MAXL + 2];
static size_t    nstate[MAXL + 2], nedge[MAXL + 2], ncomp_r[MAXL + 2];
static size_t    nedge_k[MAXL + 2][3];
static uint32_t *eptr[MAXL + 2], *eidx[MAXL + 2], *cidx[MAXL + 2];
static uint8_t  *cval[MAXL + 2];
static int       maxindeg[MAXL + 2];
static double    W[MAXNX][3];
static uint64_t  MNUM[MAXNX];

/* Adaptation: transpose graph for parallel destination accumulation. */
static uint32_t *incoming_ptr[MAXL+2], *incoming_edge[MAXL+2];
static void transpose_graph(void) {
 for(int r=0;r<NST;r++) {
  size_t nn=nstate[(r+1)%NST];
  incoming_ptr[r]=calloc(nn+1,4); incoming_edge[r]=malloc(nedge[r]*4);
  if(!incoming_ptr[r]||!incoming_edge[r]) { fprintf(stderr,"transpose OOM\n");exit(2); }
  for(size_t j=0;j<nedge[r];j++)incoming_ptr[r][(eidx[r][j]&0x3fffffffu)+1]++;
  for(size_t j=0;j<nn;j++)incoming_ptr[r][j+1]+=incoming_ptr[r][j];
  uint32_t *cursor=malloc(nn*4);if(!cursor)exit(2);memcpy(cursor,incoming_ptr[r],nn*4);
  for(size_t i=0;i<nstate[r];i++)for(uint32_t j=eptr[r][i];j<eptr[r][i+1];j++) {
   uint32_t v=eidx[r][j];incoming_edge[r][cursor[v&0x3fffffffu]++]=(uint32_t)i|(v&0xc0000000u);
  }free(cursor);
 }
}

static void build_states(void) {
    for (int r = 0; r < NST; r++) { codes[r] = NULL; nstate[r] = 0; }
    codes[0] = (uint64_t *)malloc(8); codes[0][0] = 0; nstate[0] = 1;
    size_t bcap = 1 << 16;
    uint64_t *buf = (uint64_t *)malloc(bcap * 8), *tmp = (uint64_t *)malloc(bcap * 8);
    for (int cyc = 0; cyc < 64; cyc++) {
        int changed = 0;
        for (int r = 0; r < NST; r++) {
            int r2 = (r + 1) % NST;
            size_t need = nstate[r] * 3 + 8;
            if (need > bcap) { while (bcap < need) bcap <<= 1;
                buf = (uint64_t *)realloc(buf, bcap * 8); tmp = (uint64_t *)realloc(tmp, bcap * 8);
                if (!buf || !tmp) { fprintf(stderr, "buf OOM\n"); exit(2); } }
            size_t nb = 0; uint64_t o[4]; int kk[4], nc;
            for (size_t i = 0; i < nstate[r]; i++) {
                int ns = trans(codes[r][i], r, o, kk, &nc);
                for (int j = 0; j < ns; j++) buf[nb++] = o[j];
            }
            radix_u64(buf, nb, tmp); nb = uniq(buf, nb);
            size_t na = nstate[r2], i = 0, j = 0, w = 0;
            uint64_t *mg = (uint64_t *)malloc((na + nb) * 8);
            if (!mg) { fprintf(stderr, "merge OOM\n"); exit(2); }
            while (i < na && j < nb) {
                if (codes[r2][i] < buf[j]) mg[w++] = codes[r2][i++];
                else if (codes[r2][i] > buf[j]) mg[w++] = buf[j++];
                else { mg[w++] = buf[j++]; i++; }
            }
            while (i < na) mg[w++] = codes[r2][i++];
            while (j < nb) mg[w++] = buf[j++];
            if (w > na) { changed = 1; free(codes[r2]); codes[r2] = mg; nstate[r2] = w; }
            else free(mg);
        }
        if (!changed) break;
    }
    free(buf); free(tmp);
}

static void build_edges(void) {
    uint64_t o[4]; int kk[4], nc;
    for (int r = 0; r < NST; r++) {
        int r2 = (r + 1) % NST;
        /* AUDIT: eidx packs (state index | k<<30), so the destination index must
         * fit in 30 bits; eptr is uint32_t, so the edge count must fit in 32.
         * Both were unstated couplings.  Fail closed. */
        if (nstate[r2] >= (1u << 30)) {
            fprintf(stderr, "FATAL nstate[%d]=%zu >= 2^30: eidx packing would corrupt\n",
                    r2, nstate[r2]); exit(13); }
        if ((unsigned long long)nstate[r] * 3ull + 8ull >= 4294967296ull) {
            fprintf(stderr, "FATAL edge count for stage %d exceeds uint32 eptr\n", r); exit(13); }
        HMap h; hm_build(&h, codes[r2], nstate[r2]);
        eptr[r] = (uint32_t *)malloc((nstate[r] + 1) * 4);
        eidx[r] = (uint32_t *)malloc((nstate[r] * 3 + 8) * 4);
        uint32_t *indeg = (uint32_t *)calloc(nstate[r2], 4);
        size_t ccap = 1024, cn = 0;
        cidx[r] = (uint32_t *)malloc(ccap * 4); cval[r] = (uint8_t *)malloc(ccap);
        if (!eptr[r] || !eidx[r] || !indeg || !cidx[r] || !cval[r]) { fprintf(stderr, "edge OOM\n"); exit(2); }
        size_t e = 0;
        nedge_k[r][0] = nedge_k[r][1] = nedge_k[r][2] = 0;
        for (size_t i = 0; i < nstate[r]; i++) {
            eptr[r][i] = (uint32_t)e;
            int ns = trans(codes[r][i], r, o, kk, &nc);
            if (nc) {
                if (cn == ccap) { ccap *= 2; cidx[r] = (uint32_t *)realloc(cidx[r], ccap * 4);
                                  cval[r] = (uint8_t *)realloc(cval[r], ccap); }
                cidx[r][cn] = (uint32_t)i; cval[r][cn] = (uint8_t)nc; cn++;
            }
            for (int j = 0; j < ns; j++) {
                uint32_t d = hm_get(&h, o[j]);
                if (d == 0 && i != 0) { fprintf(stderr, "FATAL nonempty->empty l=%d r=%d\n", L, r); exit(5); }
                indeg[d]++;
                nedge_k[r][kk[j]]++;
                eidx[r][e++] = d | ((uint32_t)kk[j] << 30);
            }
        }
        eptr[r][nstate[r]] = (uint32_t)e;
        nedge[r] = e; ncomp_r[r] = cn;
        int mi = 0; for (size_t i = 0; i < nstate[r2]; i++) if ((int)indeg[i] > mi) mi = indeg[i];
        maxindeg[r] = mi;
        if (mi >= (1 << 20)) { fprintf(stderr, "FATAL maxindeg %d >= 2^20\n", mi); exit(6); }
        free(indeg); free(h.key); free(h.val);
        if (r > 0) { free(codes[r]); codes[r] = NULL; }        /* keep stage 0 for the wrap */
    }
    free(codes[0]); codes[0] = NULL;
}

/* ---------------------------------------------------------------- numerics */

typedef struct { double s, c; } Ksum;
static inline void kadd(Ksum *k, double v) {
    double t = k->s + v;
    if (fabs(k->s) >= fabs(v)) k->c += (k->s - t) + v; else k->c += (v - t) + k->s;
    k->s = t;
}
static inline double kval(const Ksum *k) { return k->s + k->c; }

static double **pc, **pn;      /* NP planes each, length ms */
static size_t ms;

/* One backward cycle:  g_r = c_r + M_r^T g_{r+1}, cyclic; g0 in/out (stage-0 planes).
 * check != 0: additionally VERIFY, in exact __int128 integer arithmetic,
 *     uhat_r[i] >= c_r[i] + sum_{i->j} x0^k uhat_{r+1}[j]   for every nonempty i, every r.
 * (identical to tmc.c)                                                                  */
static long long backward_cycle(double *g0, int check, double eps, int F,
                                double *umaxout, uint64_t **Ubuf, uint64_t *U0fix)
{
    long long bad = 0;
    for (int p = 0; p < NP; p++) memcpy(pn[p], g0 + (size_t)p * nstate[0], nstate[0] * 8);
    double umax = 0.0;
    uint64_t *Ucur = Ubuf ? Ubuf[0] : NULL, *Unxt = Ubuf ? Ubuf[1] : NULL;
    if (check) memcpy(Unxt, U0fix, (size_t)NX * ms * 8);   /* wrap: uhat_0 */
    for (int r = NST - 1; r >= 0; r--) {
        size_t sz = nstate[r];
        #pragma omp parallel for schedule(static)
        for (long long i = 0; i < (long long)sz; i++) {
            double acc[MAXNX * NRHS];
            for (int p = 0; p < NP; p++) acc[p] = 0.0;
            uint32_t b = eptr[r][i], e2 = eptr[r][i + 1];
            for (uint32_t e = b; e < e2; e++) {
                uint32_t v = eidx[r][e]; uint32_t d = v & 0x3FFFFFFFu; int k = (int)(v >> 30);
                for (int x = 0; x < NX; x++) {
                    double w = W[x][k];
                    for (int q = 0; q < NRHS; q++) acc[x * NRHS + q] += w * pn[x * NRHS + q][d];
                }
            }
            for (int p = 0; p < NP; p++) pc[p][i] = acc[p];
        }
        for (int x = 0; x < NX; x++) {
            double *v1 = pc[x * NRHS + 1];
            for (size_t i = 0; i < sz; i++) v1[i] += 1.0;
            double *v0 = pc[x * NRHS];
            for (size_t j = 0; j < ncomp_r[r]; j++) v0[cidx[r][j]] += (double)cval[r][j];
        }
        for (int p = 0; p < NP; p++) pc[p][0] = 0.0;
        if (umaxout) for (int x = 0; x < NX; x++) {
            const double *G = pc[x * NRHS], *Pp = pc[x * NRHS + 1];
            for (size_t i = 0; i < sz; i++) { double u = G[i] + eps * Pp[i]; if (u > umax) umax = u; }
        }
        if (check) {
            if (r == 0) memcpy(Ucur, U0fix, (size_t)NX * ms * 8);
            else for (int x = 0; x < NX; x++) {
                const double *G = pc[x * NRHS], *Pp = pc[x * NRHS + 1];
                uint64_t *U = Ucur + (size_t)x * ms;
                for (size_t i = 0; i < sz; i++) U[i] = (uint64_t)ceil((G[i] + eps * Pp[i]) * ldexp(1.0, F));
                U[0] = 0;
            }
            long long badr = 0;
            for (int x = 0; x < NX; x++) {
                unsigned __int128 w0 = (unsigned __int128)1 << 54;
                unsigned __int128 w1 = (unsigned __int128)MNUM[x] << 27;
                unsigned __int128 w2 = (unsigned __int128)MNUM[x] * (unsigned __int128)MNUM[x];
                const uint64_t *Uc = Ucur + (size_t)x * ms, *Un = Unxt + (size_t)x * ms;
                long long bx = 0;
                #pragma omp parallel for schedule(static) reduction(+:bx)
                for (long long i = 1; i < (long long)sz; i++) {
                    unsigned __int128 rhs = 0;
                    uint32_t b = eptr[r][i], e2 = eptr[r][i + 1];
                    for (uint32_t e = b; e < e2; e++) {
                        uint32_t v = eidx[r][e]; uint32_t d = v & 0x3FFFFFFFu; int k = (int)(v >> 30);
                        rhs += (unsigned __int128)Un[d] * (k == 0 ? w0 : (k == 1 ? w1 : w2));
                    }
                    if (rhs > ((unsigned __int128)Uc[i] << 54)) bx++;
                }
                for (size_t j = 0; j < ncomp_r[r]; j++) {
                    uint32_t i = cidx[r][j]; if (i == 0) continue;
                    unsigned __int128 rhs = ((unsigned __int128)cval[r][j] << 54) << F;
                    uint32_t b = eptr[r][i], e2 = eptr[r][i + 1];
                    for (uint32_t e = b; e < e2; e++) {
                        uint32_t v = eidx[r][e]; uint32_t d = v & 0x3FFFFFFFu; int k = (int)(v >> 30);
                        rhs += (unsigned __int128)Un[d] * (k == 0 ? w0 : (k == 1 ? w1 : w2));
                    }
                    if (rhs > ((unsigned __int128)Uc[i] << 54)) bx++;
                }
                badr += bx;
            }
            bad += badr;
            uint64_t *t = Ucur; Ucur = Unxt; Unxt = t;
        }
        for (int p = 0; p < NP; p++) { double *t = pc[p]; pc[p] = pn[p]; pn[p] = t; }
    }
    for (int p = 0; p < NP; p++) memcpy(g0 + (size_t)p * nstate[0], pn[p], nstate[0] * 8);
    if (umaxout) *umaxout = umax;
    return bad;
}

/* ---------------------------------------------------------------- u128 helpers */

static void u128str(u128 v, char *buf) {
    char t[48]; int n = 0;
    if (v == 0) { buf[0] = '0'; buf[1] = 0; return; }
    while (v) { t[n++] = (char)('0' + (int)(v % 10)); v /= 10; }
    for (int i = 0; i < n; i++) buf[i] = t[n - 1 - i];
    buf[n] = 0;
}

/* floor( n * m / 2^sh ) for n < 2^GUARD_BITS, m < 2^53, 0 < sh < 64, using the exact
 * 192-bit product.  *ovf set if the true quotient does not fit in 128 bits.
 * remainder-nonzero flag returned in *rem (for the ceil variant).                      */
static inline u128 mulshr192(u128 n, uint64_t m, int sh, int *rem, int *ovf) {
    uint64_t lo = (uint64_t)n, hi = (uint64_t)(n >> 64);
    u128 a = (u128)lo * (u128)m;
    u128 b = (u128)hi * (u128)m;
    uint64_t p0 = (uint64_t)a;
    u128 mid = (a >> 64) + (u128)(uint64_t)b;
    uint64_t p1 = (uint64_t)mid;
    uint64_t p2 = (uint64_t)(b >> 64) + (uint64_t)(mid >> 64);
    if (sh <= 0 || sh >= 64) {   /* AUDIT: p1 << (64-sh) is UB at sh == 0 */
        fprintf(stderr, "FATAL mulshr192 shift %d outside (0,64)\n", sh); exit(14); }
    *rem = (p0 & ((1ULL << sh) - 1)) != 0;
    if ((p2 >> sh) != 0) *ovf = 1;
    uint64_t r0 = (p0 >> sh) | (p1 << (64 - sh));
    uint64_t r1 = (p1 >> sh) | (p2 << (64 - sh));
    return ((u128)r1 << 64) | r0;
}

int main(int argc, char **argv)
{
    if (argc < 3) { fprintf(stderr, "usage: %s <l> <Mnum...>|--states [--scale S] [--relstop K] [--fp64] [--out FILE]\n", argv[0]); return 1; }
    L = atoi(argv[1]); NST = L + 1;
    if (L < 1 || L > MAXL) { fprintf(stderr, "bad l\n"); return 1; }
    /* AUDIT: radix_u64 sorts only the low 56 bits; the packed code uses bits up
     * to EFBIT = 2L+5.  Silent state-dedup corruption if this is ever violated. */
    if (EFBIT >= 56) { fprintf(stderr, "FATAL EFBIT=%d >= 56: radix_u64 sorts 56 bits only\n",
                               EFBIT); return 1; }
    int states_only = !strcmp(argv[2], "--states");

    int S = 96, RELSTOP = 56, do_fp64 = 0;
    const char *outfn = NULL;
    int nm = 0; uint64_t marg[MAXNX];
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "--states")) continue;
        else if (!strcmp(argv[i], "--scale")) { S = atoi(argv[++i]); }
        else if (!strcmp(argv[i], "--relstop")) { RELSTOP = atoi(argv[++i]); }
        else if (!strcmp(argv[i], "--fp64")) { do_fp64 = 1; }
        else if (!strcmp(argv[i], "--out")) { outfn = argv[++i]; }
        else { if (nm >= MAXNX) { fprintf(stderr, "too many x values\n"); return 1; }
               marg[nm++] = strtoull(argv[i], NULL, 10); }
    }
    if (S < 8 || S > 100) { fprintf(stderr, "scale S out of range [8,100]\n"); return 1; }
    NX = states_only ? 1 : nm;
    if (NX < 1) { fprintf(stderr, "no Mnum given\n"); return 1; }
    NP = NX * NRHS;

    double t0 = now();
    build_states();
    size_t tot = 0; for (int r = 0; r < NST; r++) tot += nstate[r];
    fprintf(stderr, "l=%d stages:", L);
    for (int r = 0; r < NST; r++) fprintf(stderr, " %zu", nstate[r]);
    fprintf(stderr, "  total=%zu [%.1fs]\n", tot, now() - t0);
    build_edges();
    fprintf(stderr, "matchpos audit: calls=%llu pushes=%llu m-writes=%llu "
                    "setpos-writes=%llu max-depth=%d bound=%d\n",
            mp_calls, mp_push, mp_mwrite, mp_setpos, mp_maxdepth, MPSTACK);
    size_t tote = 0, totk[3] = {0,0,0}; int Dcol = 0;
    for (int r = 0; r < NST; r++) { tote += nedge[r]; Dcol += maxindeg[r];
        for (int k = 0; k < 3; k++) totk[k] += nedge_k[r][k]; }
    double t2 = now();
    fprintf(stderr, "l=%d edges=%zu (k0=%zu k1=%zu k2=%zu) Dcol=%d [%.1fs]\n",
            L, tote, totk[0], totk[1], totk[2], Dcol, t2 - t0);
    if (states_only) {
        printf("{\"l\":%d,\"total_states\":%zu,\"edges\":%zu,\"edges_k0\":%zu,"
               "\"edges_k1\":%zu,\"edges_k2\":%zu,\"Dcol\":%d,\"build_s\":%.1f}\n",
               L, tot, tote, totk[0], totk[1], totk[2], Dcol, t2 - t0);
        return 0;
    }
    transpose_graph();
    for (int x = 0; x < NX; x++) {
        MNUM[x] = marg[x];
        if (MNUM[x] >= (1ULL << 26)) { fprintf(stderr, "Mnum must be < 2^26\n"); return 1; }
        double x0 = (double)MNUM[x] / 134217728.0;
        W[x][0] = 1.0; W[x][1] = x0; W[x][2] = x0 * x0;
        if (W[x][1] * 134217728.0 != (double)MNUM[x]) { fprintf(stderr, "x0 inexact\n"); return 1; }
        if (W[x][2] * 18014398509481984.0 != (double)(MNUM[x] * MNUM[x])) { fprintf(stderr, "x0^2 inexact\n"); return 1; }
    }

    ms = 0; for (int r = 0; r < NST; r++) if (nstate[r] > ms) ms = nstate[r];
    pc = (double **)malloc(NP * sizeof(double *)); pn = (double **)malloc(NP * sizeof(double *));
    for (int p = 0; p < NP; p++) {
        pc[p] = (double *)malloc(ms * 8); pn[p] = (double *)malloc(ms * 8);
        if (!pc[p] || !pn[p]) { fprintf(stderr, "plane OOM\n"); return 2; }
    }
    double *g0 = (double *)calloc((size_t)NP * nstate[0], 8);

    /* backward fixed point (fp64: produces only a CANDIDATE u, verified exactly below) */
    double prev = 0.0; int iters;
    for (iters = 1; iters <= 3000; iters++) {
        backward_cycle(g0, 0, 0.0, 0, NULL, NULL, NULL);
        double mx = 0.0;
        for (size_t i = 0; i < (size_t)NP * nstate[0]; i++) if (g0[i] > mx) mx = g0[i];
        if (!(mx < 1e250)) { fprintf(stderr, "backward diverged (lambda>=1)\n"); return 7; }
        if (iters > 20 && fabs(mx - prev) <= 1e-15 * mx) break;
        prev = mx;
    }
    double t3 = now();
    fprintf(stderr, "backward: %d cycles [%.1fs]\n", iters, t3 - t2);

    /* certificate: exact integer verification of  u >= c + M(x0)^T u */
    uint64_t *Ubuf[2], *U0fix;
    Ubuf[0] = (uint64_t *)malloc((size_t)NX * ms * 8);
    Ubuf[1] = (uint64_t *)malloc((size_t)NX * ms * 8);
    U0fix   = (uint64_t *)calloc((size_t)NX * ms, 8);
    if (!Ubuf[0] || !Ubuf[1] || !U0fix) { fprintf(stderr, "U OOM\n"); return 2; }
    double eps = 0, umax = 0; int F = 0, cert_ok = 0;
    for (double e = 1e-11; e <= 1e-3; e *= 100.0) {
        backward_cycle(g0, 0, e, 0, &umax, NULL, NULL);
        F = 50; while (F > 4 && umax * ldexp(1.0, F) >= ldexp(1.0, 52)) F--;
        for (int x = 0; x < NX; x++) {
            const double *G = g0 + (size_t)(x * NRHS) * nstate[0];
            const double *Pp = g0 + (size_t)(x * NRHS + 1) * nstate[0];
            uint64_t *U = U0fix + (size_t)x * ms;
            for (size_t i = 0; i < nstate[0]; i++) U[i] = (uint64_t)ceil((G[i] + e * Pp[i]) * ldexp(1.0, F));
            U[0] = 0;
        }
        long long bad = backward_cycle(g0, 1, e, F, NULL, Ubuf, U0fix);
        fprintf(stderr, "cert eps=%.0e F=%d umax=%.4g -> %lld violations\n", e, F, umax, bad);
        if (bad == 0) { cert_ok = 1; eps = e; break; }
    }
    if (!cert_ok) { fprintf(stderr, "CERTIFICATE FAILED\n"); return 8; }
    free(Ubuf[0]); free(Ubuf[1]);
    double t4 = now();
    fprintf(stderr, "certificate proved (eps=%.0e F=%d) [%.1fs]\n", eps, F, t4 - t3);

    /* keep the certified dyadic stage-0 functional as EXACT integers U0i[x][i] * 2^-F */
    uint64_t **U0i = (uint64_t **)malloc(NX * sizeof(uint64_t *));
    double **U0 = (double **)malloc(NX * sizeof(double *));
    double sF = ldexp(1.0, -F);
    for (int x = 0; x < NX; x++) {
        U0i[x] = (uint64_t *)malloc(nstate[0] * 8);
        U0[x]  = (double *)malloc(nstate[0] * 8);
        const uint64_t *U = U0fix + (size_t)x * ms;
        for (size_t i = 0; i < nstate[0]; i++) { U0i[x][i] = U[i]; U0[x][i] = (double)U[i] * sF; }
    }
    free(U0fix);
    for (int p = 0; p < NP; p++) { free(pc[p]); free(pn[p]); }
    free(pc); free(pn); free(g0);

    int wmax = 90 * (L + 1) + 400;
    double fres[MAXNX], ftail[MAXNX]; int wf = 0; long long Dfp = 0;
    double t5 = t4;

    /* ---------------- optional fp64 reference sweep (unchanged from tmc.c) ------- */
    if (do_fp64) {
        double *cur = (double *)calloc((size_t)NX * ms, 8);
        double *nxt = (double *)calloc((size_t)NX * ms, 8);
        if (!cur || !nxt) { fprintf(stderr, "sweep OOM\n"); return 2; }
        Ksum res[MAXNX]; double tail[MAXNX];
        for (int x = 0; x < NX; x++) { res[x].s = res[x].c = 0.0; tail[x] = 1e300;
                                       cur[(size_t)x * ms] = 1.0; }
        int w = 0, done = 0;
        while (w < wmax && !done) {
            for (int r = 0; r < NST; r++) {
                size_t sz = nstate[r], sz2 = nstate[(r + 1) % NST];
                for (int x = 0; x < NX; x++) {
                    Ksum k = {0.0, 0.0}; const double *v = cur + (size_t)x * ms;
                    for (size_t j = 0; j < ncomp_r[r]; j++) kadd(&k, (double)cval[r][j] * v[cidx[r][j]]);
                    kadd(&res[x], kval(&k));
                }
                #pragma omp parallel for num_threads(NX) schedule(static,1)
                for (int x = 0; x < NX; x++) {
                    double *dst = nxt + (size_t)x * ms; const double *src = cur + (size_t)x * ms;
                    memset(dst, 0, sz2 * 8);
                    const double *wx = W[x];
                    for (size_t i = 0; i < sz; i++) {
                        double vi = src[i];
                        if (vi == 0.0) continue;
                        uint32_t b = eptr[r][i], e2 = eptr[r][i + 1];
                        for (uint32_t e = b; e < e2; e++) {
                            uint32_t v = eidx[r][e];
                            dst[v & 0x3FFFFFFFu] += wx[v >> 30] * vi;
                        }
                    }
                }
                double *t = cur; cur = nxt; nxt = t;
            }
            w++;
            if (w == 1) for (int x = 0; x < NX; x++) cur[(size_t)x * ms] = 0.0;
            done = 1;
            for (int x = 0; x < NX; x++) {
                Ksum k = {0.0, 0.0}; const double *v = cur + (size_t)x * ms;
                for (size_t i = 0; i < nstate[0]; i++) if (v[i] != 0.0) kadd(&k, v[i] * U0[x][i]);
                tail[x] = kval(&k);
                if (!(tail[x] <= 1e-15 * kval(&res[x]))) done = 0;
            }
        }
        for (int x = 0; x < NX; x++) { fres[x] = kval(&res[x]); ftail[x] = tail[x]; }
        wf = w; Dfp = (long long)w * (long long)Dcol + 8LL * w * NST + 256;
        free(cur); free(nxt);
        t5 = now();
        fprintf(stderr, "fp64 sweep w=%d [%.1fs]\n", w, t5 - t4);
    }

    /* ---------------- DUAL EXACT-INTEGER SWEEP ---------------------------------- */
    int NP2 = NX * 2;                       /* plane p: x = p>>1, dir = p&1 (0=floor,1=ceil) */
    u128 *icur = (u128 *)calloc((size_t)NP2 * ms, 16);
    u128 *inxt = (u128 *)calloc((size_t)NP2 * ms, 16);
    if (!icur || !inxt) { fprintf(stderr, "int plane OOM\n"); return 2; }
    uint64_t M1[MAXNX], M2[MAXNX];
    for (int x = 0; x < NX; x++) { M1[x] = MNUM[x]; M2[x] = MNUM[x] * MNUM[x]; }
    u128 ires[2 * MAXNX], itail[MAXNX];
    uint64_t orh[2 * MAXNX];
    for (int p = 0; p < NP2; p++) { ires[p] = 0; icur[(size_t)p * ms] = (u128)1 << S; }
    for (int x = 0; x < NX; x++) itail[x] = (u128)-1;
    int wI = 0, doneI = 0, ovf = 0;
    uint64_t orall = 0;

    while (wI < wmax && !doneI) {
        for (int r = 0; r < NST; r++) {
            size_t sz = nstate[r], sz2 = nstate[(r + 1) % NST];
            for (int p = 0; p < NP2; p++) {
                const u128 *v = icur + (size_t)p * ms;
                u128 acc = 0;
                for (size_t j = 0; j < ncomp_r[r]; j++) {
                    if ((v[cidx[r][j]] >> 64) >= GUARD_HI) { fprintf(stderr, "FATAL completion guard\n"); return 9; }
                    u128 term = (u128)cval[r][j] * v[cidx[r][j]];
                    u128 t2 = acc + term; if (t2 < acc) { ovf = 1; } acc = t2;
                }
                u128 t3 = ires[p] + acc; if (t3 < ires[p]) { ovf = 1; } ires[p] = t3;
            }
            uint64_t parallel_oh=0;int parallel_ovf=0;
            #pragma omp parallel for schedule(static) reduction(|:parallel_oh,parallel_ovf)
            for(size_t task=0;task<(size_t)NP2*sz2;task++) {
                int p=(int)(task/sz2),x=p>>1,dir=p&1;size_t d=task%sz2;
                const u128 *src=icur+(size_t)p*ms;u128 acc=0;
                uint64_t m1=M1[x],m2=M2[x];
                for(uint32_t j=incoming_ptr[r][d];j<incoming_ptr[r][d+1];j++) {
                    uint32_t e=incoming_edge[r][j];unsigned k=e>>30;
                    u128 vi=src[e&0x3fffffffu];if(!vi)continue;
                    uint64_t vlo=(uint64_t)vi,vhi=(uint64_t)(vi>>64);parallel_oh|=vhi;
                    u128 t;
                    if(k==0)t=vi;
                    else if(k==1) {
                        u128 plo=(u128)vlo*m1,phi=(u128)vhi*m1;
                        t=(phi<<37)+(plo>>27);
                        if(dir&&((uint64_t)plo&0x7ffffffULL))t++;
                    }else {
                        u128 plo=(u128)vlo*m2,phi=(u128)vhi*m2;
                        t=(phi<<10)+(plo>>54);
                        if(dir&&((uint64_t)plo&((1ULL<<54)-1)))t++;
                    }
                    u128 n=acc+t;if(n<acc)parallel_ovf=1;acc=n;
                }
                inxt[(size_t)p*ms+d]=acc;
            }
            orall|=parallel_oh;if(parallel_ovf)ovf=1;
            if (orall >= GUARD_HI) { fprintf(stderr, "FATAL value guard: orall=%llu >= 2^%d\n",
                                             (unsigned long long)orall, GUARD_BITS - 64); return 9; }
            u128 *t = icur; icur = inxt; inxt = t;
        }
        wI++;
        if (wI == 1) for (int p = 0; p < NP2; p++) icur[(size_t)p * ms] = 0;
        doneI = 1;
        for (int x = 0; x < NX; x++) {
            const u128 *v = icur + (size_t)(2 * x + 1) * ms;    /* CEIL plane, stage 0 */
            u128 acc = 0;
            for (size_t i = 0; i < nstate[0]; i++) {
                if (v[i] == 0 || U0i[x][i] == 0) continue;
                orall |= (uint64_t)(v[i] >> 64);
                int rem = 0;
                u128 q = mulshr192(v[i], U0i[x][i], F, &rem, &ovf);
                q += (rem ? 1 : 0);                              /* ceil */
                u128 t2 = acc + q; if (t2 < acc) ovf = 1; acc = t2;
            }
            itail[x] = acc;
            if (!(itail[x] <= (ires[2 * x] >> RELSTOP))) doneI = 0;
        }
        if (orall >= GUARD_HI) { fprintf(stderr, "FATAL value guard (tail)\n"); return 9; }
        if (ovf) { fprintf(stderr, "FATAL u128 overflow detected\n"); return 9; }
    }
    double t6 = now();
    fprintf(stderr, "exact dual sweep w=%d S=%d guard_hi_or=%llu [%.1fs]\n",
            wI, S, (unsigned long long)orall, t6 - t5);
    if (ovf) { fprintf(stderr, "FATAL u128 overflow detected\n"); return 9; }
    if (wI >= wmax) { fprintf(stderr, "FATAL sweep did not converge within wmax=%d\n", wmax); return 10; }

    char fn[256];
    if (outfn) snprintf(fn, sizeof fn, "%s", outfn);
    else snprintf(fn, sizeof fn, "span_%d.json", L);
    FILE *f = fopen(fn, "w");
    fprintf(f, "{\"l\":%d,\"total_states\":%zu,\"edges\":%zu,\"edges_k0\":%zu,\"edges_k1\":%zu,"
               "\"edges_k2\":%zu,\"Dcol\":%d,\"S\":%d,\"w\":%d,\"relstop\":%d,"
               "\"backward_cycles\":%d,\"cert_eps\":%.1e,\"cert_F\":%d,\"cert_ok\":1,"
               "\"fp64\":%d,\"w_fp64\":%d,\"D_fp64\":%lld,"
               "\"build_s\":%.1f,\"backward_s\":%.1f,\"cert_s\":%.1f,\"fp64_sweep_s\":%.1f,"
               "\"exact_sweep_s\":%.1f,\"x\":[",
            L, tot, tote, totk[0], totk[1], totk[2], Dcol, S, wI, RELSTOP,
            iters, eps, F, do_fp64, wf, Dfp,
            t2 - t0, t3 - t2, t4 - t3, t5 - t4, t6 - t5);
    for (int x = 0; x < NX; x++) {
        char blo[48], bhi[48], bta[48];
        u128str(ires[2 * x], blo); u128str(ires[2 * x + 1], bhi); u128str(itail[x], bta);
        fprintf(f, "%s{\"Mnum\":%llu,\"num_lo\":\"%s\",\"num_hi\":\"%s\",\"num_tail\":\"%s\"",
                x ? "," : "", (unsigned long long)MNUM[x], blo, bhi, bta);
        if (do_fp64) fprintf(f, ",\"res\":%.17g,\"tail\":%.17g", fres[x], ftail[x]);
        fprintf(f, "}");
        double sc = ldexp(1.0, -S);
        printf("l=%2d M=%llu  B_lo=%.17g  B_hi=%.17g  width=%.4g  tail=%.4g%s\n", L,
               (unsigned long long)MNUM[x],
               (double)ires[2 * x] * sc,
               ((double)ires[2 * x + 1] + (double)itail[x]) * sc,
               ((double)ires[2 * x + 1] + (double)itail[x] - (double)ires[2 * x]) * sc,
               (double)itail[x] * sc,
               do_fp64 ? "" : "");
        if (do_fp64) printf("        fp64 res=%.17g tail=%.4g\n", fres[x], ftail[x]);
    }
    fprintf(f, "]}\n"); fclose(f);
    fprintf(stderr, "wrote %s total %.1fs\n", fn, t6 - t0);
    return 0;
}

/* Clean-room weighted-poset search for Erdos #1183 (referee e1183n2124_referee).
   A closed (union+intersection) nonempty family of 2^[n] <-> (a, finite poset P, positive weights)
   with a + sum w <= n; members <-> down-sets, size = a + w(D).  We grow P by naturally labelled
   elements: new element with strict-predecessor down-set I and weight w; new down-sets are D+{new}
   for every old down-set D containing I.  Every positive witness is converted to explicit coordinate
   masks and checked by direct pairwise closure (check_family), independent of the poset logic.

   Modes:
     wp max   n word c            exact max closed family in colour c (word[k] colours k-sets)
     wp find  n word c T          is there a family >= T in colour c
     wp allmax n                  exact maxima of both colours for all 2^(n+1) words
     wp balanced n part mod       every balanced word: a colour with family >= (n+3)/2
     wp screen Lmax T part mod    prefix DFS over words (first letter 0) keeping words whose both
                                  colours have max <= T; prints survivors at length Lmax-1 and Lmax
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned long long u64;
#define MAXE 32
#define MAXD 256

static int N;          /* cube dimension */
static u64 RM;         /* allowed rank mask */
static int TH;         /* threshold */
static long long nodes;
static int ne;
static int wt[MAXE];
static uint32_t dsm[MAXE + 1][MAXD];
static int dss[MAXE + 1][MAXD];
static int dc[MAXE + 1];
static int rootA;
static u64 wit[MAXD];
static int witn;
static long long witfail;

static int check_family(int n, u64 rm, const u64 *f, int m) {
    /* distinct, inside [n], all ranks allowed, closed under | and & */
    u64 full = (n == 64) ? ~0ULL : ((1ULL << n) - 1);
    for (int i = 0; i < m; i++) {
        if (f[i] & ~full) return 0;
        if (!((rm >> __builtin_popcountll(f[i])) & 1)) return 0;
        for (int j = 0; j < i; j++) if (f[i] == f[j]) return 0;
    }
    for (int i = 0; i < m; i++)
        for (int j = 0; j < m; j++) {
            u64 u = f[i] | f[j], x = f[i] & f[j];
            int hu = 0, hx = 0;
            for (int k = 0; k < m; k++) { if (f[k] == u) hu = 1; if (f[k] == x) hx = 1; }
            if (!hu || !hx) return 0;
        }
    return 1;
}

static void build_witness(void) {
    int L = ne;
    u64 blk[MAXE];
    int pos = rootA;
    u64 amask = (rootA == 0) ? 0 : ((1ULL << rootA) - 1);
    for (int j = 0; j < ne; j++) {
        blk[j] = ((1ULL << wt[j]) - 1) << pos;
        pos += wt[j];
    }
    witn = dc[L];
    for (int i = 0; i < witn; i++) {
        u64 m = amask;
        for (int j = 0; j < ne; j++) if ((dsm[L][i] >> j) & 1) m |= blk[j];
        wit[i] = m;
    }
    if (!check_family(N, RM, wit, witn)) { witfail++; fprintf(stderr, "WITNESS CHECK FAILED\n"); exit(3); }
}

static int dfs(int used) {
    nodes++;
    int L = ne, cnt = dc[L];
    if (cnt >= TH) { build_witness(); return 1; }
    int rem = N - used;
    int idx[MAXD];
    for (int i = 0; i < cnt; i++) {
        uint32_t I = dsm[L][i];
        int k = 0;
        for (int j = 0; j < cnt; j++) if ((dsm[L][j] & I) == I) idx[k++] = j;
        for (int w = 1; w <= rem; w++) {
            int ok = 1;
            for (int t = 0; t < k; t++) if (!((RM >> (dss[L][idx[t]] + w)) & 1)) { ok = 0; break; }
            if (!ok) continue;
            memcpy(dsm[L + 1], dsm[L], sizeof(uint32_t) * cnt);
            memcpy(dss[L + 1], dss[L], sizeof(int) * cnt);
            for (int t = 0; t < k; t++) {
                dsm[L + 1][cnt + t] = dsm[L][idx[t]] | (1u << ne);
                dss[L + 1][cnt + t] = dss[L][idx[t]] + w;
            }
            dc[L + 1] = cnt + k;
            wt[ne] = w;
            ne++;
            int r = dfs(used + w);
            ne--;
            if (r) return 1;
        }
    }
    return 0;
}

/* is there a closed family of >= T members, all ranks in rm, in 2^[n]? */
static int find(int n, u64 rm, int T) {
    N = n; RM = rm; TH = T;
    if (T <= 0) return 1;
    for (int a = 0; a <= n; a++) {
        if (!((rm >> a) & 1)) continue;
        ne = 0; dc[0] = 1; dsm[0][0] = 0; dss[0][0] = a; rootA = a;
        if (dfs(a)) return 1;
    }
    return 0;
}

static int exact_max(int n, u64 rm) {
    int best = 0;
    for (;;) {
        if (find(n, rm, best + 1)) best = witn; else break;
    }
    return best;
}

static int exact_max_cap(int n, u64 rm, int cap) { /* min(max, cap) */
    int best = 0;
    while (best < cap) { if (find(n, rm, best + 1)) best = witn; else break; }
    return best < cap ? best : cap;
}

static u64 word_mask(const char *w, int c) {
    u64 m = 0;
    for (int k = 0; w[k]; k++) if (w[k] - '0' == c) m |= 1ULL << k;
    return m;
}

static void print_wit(void) {
    printf("[");
    for (int i = 0; i < witn; i++) printf("%s%llu", i ? "," : "", wit[i]);
    printf("]");
}

/* ---------- screen ---------- */
static int SL, ST;
static long long cnt_good[64];
static char sw[64];
static u64 wmask_len(const char *w, int L, int c) {
    u64 m = 0;
    for (int k = 0; k < L; k++) if (w[k] - '0' == c) m |= 1ULL << k;
    return m;
}
static int good_word(int L) { /* word sw[0..L-1], cube n=L-1, both colours max <= ST */
    for (int c = 0; c < 2; c++) {
        u64 rm = wmask_len(sw, L, c);
        if (__builtin_popcountll(rm) > ST) return 0;     /* chain witness */
    }
    for (int c = 0; c < 2; c++) if (find(L - 1, wmask_len(sw, L, c), ST + 1)) return 0;
    return 1;
}
static void screen_rec(int L) { /* sw[0..L-1] good */
    cnt_good[L]++;
    if (L >= SL - 1) { printf("GOOD L=%d %.*s\n", L, L, sw); fflush(stdout); }
    if (L == SL) return;
    for (int b = 0; b < 2; b++) {
        sw[L] = '0' + b;
        if (good_word(L + 1)) screen_rec(L + 1);
    }
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    if (!strcmp(argv[1], "max")) {
        int n = atoi(argv[2]); const char *w = argv[3]; int c = atoi(argv[4]);
        if ((int)strlen(w) != n + 1) { fprintf(stderr, "bad length\n"); return 1; }
        u64 rm = word_mask(w, c);
        int b = exact_max(n, rm);
        printf("n=%d word=%s colour=%d max=%d last_fail_nodes=%lld witness=", n, w, c, b, nodes);
        /* re-find witness at b */
        find(n, rm, b); print_wit(); printf("\n");
    } else if (!strcmp(argv[1], "find")) {
        int n = atoi(argv[2]); const char *w = argv[3]; int c = atoi(argv[4]); int T = atoi(argv[5]);
        int r = find(n, word_mask(w, c), T);
        printf("n=%d word=%s colour=%d T=%d found=%d nodes=%lld", n, w, c, T, r, nodes);
        if (r) { printf(" witness="); print_wit(); }
        printf("\n");
    } else if (!strcmp(argv[1], "allmax")) {
        int n = atoi(argv[2]);
        char w[64];
        for (u64 x = 0; x < (1ULL << (n + 1)); x++) {
            for (int k = 0; k <= n; k++) w[k] = '0' + ((x >> k) & 1);
            w[n + 1] = 0;
            int m0 = exact_max(n, word_mask(w, 0)), m1 = exact_max(n, word_mask(w, 1));
            printf("%s %d %d\n", w, m0, m1);
        }
    } else if (!strcmp(argv[1], "balanced")) {
        int n = atoi(argv[2]); int part = atoi(argv[3]), mod = atoi(argv[4]);
        int L = n + 1, h = L / 2, T = (n + 3) / 2;
        long long cnt = 0, ok = 0, bad = 0, idx = 0; long long fc[2] = {0, 0};
        /* enumerate L-bit masks with popcount h (Gosper) */
        u64 x = (1ULL << h) - 1, lim = 1ULL << L;
        char w[64];
        while (x < lim) {
            if (idx++ % mod == part) {
                cnt++;
                for (int k = 0; k < L; k++) w[k] = '0' + ((x >> k) & 1);
                w[L] = 0;
                int got = 0;
                for (int c = 0; c < 2 && !got; c++) {
                    nodes = 0;
                    if (find(n, word_mask(w, c), T)) { got = 1; fc[c]++; }
                }
                if (got) ok++; else { bad++; printf("NOFAMILY %s\n", w); fflush(stdout); }
            }
            u64 c = x & -x, r = x + c; x = (((r ^ x) >> 2) / c) | r;
        }
        printf("balanced n=%d part=%d/%d words=%lld ok=%lld bad=%lld found_in_colour0=%lld colour1=%lld T=%d witnesses_closure_checked=%lld\n",
               n, part, mod, cnt, ok, bad, fc[0], fc[1], T, ok);
    } else if (!strcmp(argv[1], "splitsum")) {
        /* min over rank words (first letter 0; colour swap covers the rest) of max0+max1 */
        int n = atoi(argv[2]); int part = atoi(argv[3]), mod = atoi(argv[4]); int K = atoi(argv[5]);
        int least = 1000; long long cnt = 0; char w[64]; char lw[64] = "";
        for (u64 x = 0; x < (1ULL << n); x++) {
            if ((long long)(x % mod) != part) continue;
            w[0] = '0'; for (int k = 1; k <= n; k++) w[k] = '0' + ((x >> (k - 1)) & 1); w[n + 1] = 0;
            int s = exact_max_cap(n, word_mask(w, 0), K) + exact_max_cap(n, word_mask(w, 1), K);
            cnt++; if (s < least) { least = s; strcpy(lw, w); }
        }
        printf("splitsum n=%d K=%d part=%d/%d words=%lld least_capped_sum=%d at %s\n", n, K, part, mod, cnt, least, lw);
    } else if (!strcmp(argv[1], "screen")) {
        SL = atoi(argv[2]); ST = atoi(argv[3]); int part = atoi(argv[4]), mod = atoi(argv[5]);
        /* split: enumerate prefixes of length P=12 starting with 0, take those with index%mod==part */
        int P = 12;
        long long idx = 0;
        for (u64 x = 0; x < (1ULL << (P - 1)); x++) {
            sw[0] = '0';
            for (int k = 1; k < P; k++) sw[k] = '0' + ((x >> (k - 1)) & 1);
            /* prefixes of length <= P: all must be good (checked) */
            int ok = 1;
            for (int L = 1; L <= P && ok; L++) if (!good_word(L)) ok = 0;
            if (!ok) continue;
            if (idx++ % mod != part) continue;
            screen_rec(P);
        }
        printf("DONE part=%d/%d T=%d Lmax=%d counts:", part, mod, ST, SL);
        for (int L = P; L <= SL; L++) printf(" L%d=%lld", L, cnt_good[L]);
        printf("\n");
    }
    return 0;
}

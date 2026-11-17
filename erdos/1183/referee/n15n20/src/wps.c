/* Referee's own weighted-poset search for Erdos #1183 (written from the mathematics; no producer code).
 * A closed (union+intersection) nonempty family in 2^[n] == down-set lattice of a finite poset P with
 * positive integer weights w and a base a >= 0, a + sum w <= n; member size = a + w(D).
 * Search: grow P by adding a new maximal element whose strict down-set I is any down-set of the current P
 * (natural labelling), with every weight 1..remaining. Prune when a new down-set size is not in the colour.
 * Modes:
 *   max  N WORD          exact maximum per colour (full enumeration), with witness masks
 *   dec  N WORD C T      is there a colour-C family with >= T members? (witness or exhaustive no)
 *   all  N               exact maxima of both colours for every word of length N+1 (for brute-force comparison)
 *   bal  N               every word with (N+1)/2 ones: find a family >= (N+3)/2 in some colour; print witnesses
 * WORD[r] is the colour of rank r, r = 0..N.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64;
#define MAXD 4096
#define MAXP 32
static int N, T, found, best, bestA, bestP;
static u64 RM;
static long long nodes;
static int pw[MAXP], ppm[MAXP], bw[MAXP], bpm[MAXP];

static void rec(int a, int W, int p, int nd, const uint32_t *ds, const int *s) {
    nodes++;
    if (nd > best) { best = nd; bestA = a; bestP = p; memcpy(bw, pw, sizeof pw); memcpy(bpm, ppm, sizeof ppm); }
    if (T && nd >= T) { found = 1; return; }
    int rem = N - a - W;
    if (rem <= 0) return;
    uint32_t *nds = malloc(sizeof(uint32_t) * MAXD);
    int *ns = malloc(sizeof(int) * MAXD), *sums = malloc(sizeof(int) * MAXD), *idx = malloc(sizeof(int) * MAXD);
    for (int i = 0; i < nd && !found; i++) {
        uint32_t I = ds[i];
        int cnt = 0;
        for (int j = 0; j < nd; j++) if ((ds[j] & I) == I) { sums[cnt] = s[j]; idx[cnt] = j; cnt++; }
        if (nd + cnt > MAXD) { fprintf(stderr, "MAXD overflow\n"); exit(2); }
        for (int w = 1; w <= rem && !found; w++) {
            int ok = 1;
            for (int k = 0; k < cnt; k++) if (!((RM >> (a + sums[k] + w)) & 1)) { ok = 0; break; }
            if (!ok) continue;
            memcpy(nds, ds, sizeof(uint32_t) * nd); memcpy(ns, s, sizeof(int) * nd);
            for (int k = 0; k < cnt; k++) { nds[nd + k] = ds[idx[k]] | (1u << p); ns[nd + k] = sums[k] + w; }
            pw[p] = w; ppm[p] = (int)I;
            rec(a, W + w, p + 1, nd + cnt, nds, ns);
        }
    }
    free(nds); free(ns); free(sums); free(idx);
}

static void run(u64 rm, int thr) {
    RM = rm; T = thr; found = 0; best = 0; nodes = 0;
    uint32_t ds[1] = {0}; int s[1] = {0};
    for (int a = 0; a <= N && !found; a++) if ((RM >> a) & 1) { memset(pw, 0, sizeof pw); rec(a, 0, 0, 1, ds, s); }
}

/* witness masks: recompute down-sets of the best poset from predecessor masks; returns count */
static int witness(u64 *out) {
    int off[MAXP], o = bestA, m = 0;
    for (int k = 0; k < bestP; k++) { off[k] = o; o += bw[k]; }
    if (o > N) { fprintf(stderr, "budget\n"); exit(3); }
    for (u64 D = 0; D < (1ull << bestP); D++) {
        int ok = 1;
        for (int k = 0; k < bestP; k++) if (((D >> k) & 1) && ((D & (u64)bpm[k]) != (u64)bpm[k])) { ok = 0; break; }
        if (!ok) continue;
        u64 x = (1ull << bestA) - 1;
        for (int k = 0; k < bestP; k++) if ((D >> k) & 1) x |= ((1ull << bw[k]) - 1) << off[k];
        out[m++] = x;
    }
    return m;
}

/* direct check: distinct, colour, closure under pairwise | and & */
static int verify(const u64 *f, int m, u64 rm) {
    for (int i = 0; i < m; i++) {
        if (f[i] >> N) return 0;
        if (!((rm >> __builtin_popcountll(f[i])) & 1)) return 0;
        for (int j = 0; j < m; j++) {
            if (j != i && f[j] == f[i]) return 0;
            u64 u = f[i] | f[j], v = f[i] & f[j]; int iu = 0, iv = 0;
            for (int k = 0; k < m; k++) { iu |= f[k] == u; iv |= f[k] == v; }
            if (!iu || !iv) return 0;
        }
    }
    return 1;
}

static u64 colmask(const char *w, int c) { u64 r = 0; for (int i = 0; i <= N; i++) if (w[i] - '0' == c) r |= 1ull << i; return r; }

int main(int argc, char **argv) {
    if (argc < 3) return 1;
    N = atoi(argv[2]);
    u64 out[MAXD];
    if (!strcmp(argv[1], "max") || !strcmp(argv[1], "dec")) {
        const char *w = argv[3];
        if ((int)strlen(w) != N + 1) { fprintf(stderr, "word length\n"); return 1; }
        int c0 = 0, c1 = 1, thr = 0;
        if (!strcmp(argv[1], "dec")) { c0 = c1 = atoi(argv[4]); thr = atoi(argv[5]); }
        for (int c = c0; c <= c1; c++) {
            run(colmask(w, c), thr);
            int m = witness(out), ok = verify(out, m, colmask(w, c));
            printf("%s n=%d word=%s colour=%d %s=%d nodes=%lld witness_ok=%d members=%d masks=[", argv[1], N, w, c,
                   thr ? (found ? "FOUND_at_least" : "NONE_at_least") : "max", thr ? thr : best, nodes, ok, m);
            for (int i = 0; i < m; i++) printf("%s%llu", i ? "," : "", out[i]);
            printf("] best=%d\n", best);
        }
    } else if (!strcmp(argv[1], "all")) {
        char w[64];
        for (u64 x = 0; x < (1ull << (N + 1)); x++) {
            for (int i = 0; i <= N; i++) w[i] = '0' + ((x >> i) & 1);
            w[N + 1] = 0;
            int mx[2];
            for (int c = 0; c < 2; c++) {
                run(colmask(w, c), 0);
                int m = witness(out);
                if (best && (m != best || !verify(out, m, colmask(w, c)))) { fprintf(stderr, "witness fail %s\n", w); return 4; }
                mx[c] = best;
            }
            printf("%s %d %d\n", w, mx[0], mx[1]);
        }
    } else if (!strcmp(argv[1], "split")) {
        /* split N K: every rank colouring of 2^[N] has max(colour0)+max(colour1) >= K ? (bit 0 fixed by colour swap) */
        int K = atoi(argv[3]); long long cnt = 0, fail = 0; int least = 1 << 30; char w[64];
        for (u64 x = 0; x < (1ull << (N + 1)); x += 2) {
            for (int i = 0; i <= N; i++) w[i] = '0' + ((x >> i) & 1);
            w[N + 1] = 0; cnt++;
            run(colmask(w, 0), K); int b0 = best;
            if (found) { if (b0 < least) least = b0; continue; }
            run(colmask(w, 1), K - b0);
            int tot = b0 + best;
            if (!found) { fail++; printf("FAIL %s %d %d\n", w, b0, best); }
            if (tot < least) least = tot;
        }
        printf("split n=%d K=%d words(bit0=0)=%lld failures=%lld least_capped_sum=%d\n", N, K, cnt, fail, least);
    } else if (!strcmp(argv[1], "bal")) {
        int m1 = (N + 1) / 2, thr = (N + 3) / 2; long long cnt = 0, fail = 0, tn = 0; char w[64];
        for (u64 x = 0; x < (1ull << (N + 1)); x++) {
            if (__builtin_popcountll(x) != m1) continue;
            for (int i = 0; i <= N; i++) w[i] = '0' + ((x >> i) & 1);
            w[N + 1] = 0; cnt++;
            int got = -1;
            for (int c = 1; c >= 0 && got < 0; c--) {
                run(colmask(w, c), thr); tn += nodes;
                if (found) {
                    int m = witness(out);
                    if (m < thr || !verify(out, m, colmask(w, c))) { fprintf(stderr, "bad witness %s\n", w); return 5; }
                    got = c;
                    printf("%s %d", w, c);
                    for (int i = 0; i < m; i++) printf(" %llu", out[i]);
                    printf("\n");
                }
            }
            if (got < 0) { fail++; printf("%s NONE\n", w); }
        }
        fprintf(stderr, "bal n=%d words=%lld failures=%lld threshold=%d total_nodes=%lld\n", N, cnt, fail, thr, tn);
    }
    return 0;
}

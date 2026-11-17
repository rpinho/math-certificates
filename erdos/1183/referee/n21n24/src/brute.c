/* Brute force: enumerate ALL nonempty sublattices (closed under | and &) of 2^[n], n<=6,
   as 64-bit sets of sets; then for every rank word and colour print the max family size.
   Output format matches `wp allmax n`: "<word> <max0> <max1>". Count goes to stderr. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static int n, M;
#define HS (1 << 22)
static u64 *tab; static u64 *list; static long long nl;
static int ins(u64 f) {
    u64 h = (f * 0x9E3779B97F4A7C15ULL) >> 42;
    while (tab[h]) { if (tab[h] == f) return 0; h = (h + 1) & (HS - 1); }
    tab[h] = f; list[nl++] = f; return 1;
}
static u64 closure(u64 f) {
    for (;;) {
        u64 g = f;
        for (int a = 0; a < M; a++) if ((f >> a) & 1)
            for (int b = 0; b < M; b++) if ((f >> b) & 1) g |= (1ULL << (a | b)) | (1ULL << (a & b));
        if (g == f) return f;
        f = g;
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); M = 1 << n;
    tab = calloc(HS, 8); list = malloc(8ULL * HS);
    for (int s = 0; s < M; s++) ins(1ULL << s);
    for (long long i = 0; i < nl; i++) {
        u64 f = list[i];
        for (int s = 0; s < M; s++) if (!((f >> s) & 1)) ins(closure(f | (1ULL << s)));
    }
    fprintf(stderr, "n=%d nonempty sublattices=%lld\n", n, nl);
    int R = 1 << (n + 1);
    int *best = calloc(R, sizeof(int));
    for (long long i = 0; i < nl; i++) {
        u64 f = list[i]; int rm = 0, sz = 0;
        for (int s = 0; s < M; s++) if ((f >> s) & 1) { rm |= 1 << __builtin_popcount(s); sz++; }
        if (sz > best[rm]) best[rm] = sz;
    }
    /* best over submasks */
    int *sub = calloc(R, sizeof(int));
    for (int r = 0; r < R; r++) { int m = 0; for (int q = r;; q = (q - 1) & r) { if (best[q] > m) m = best[q]; if (!q) break; } sub[r] = m; }
    for (int x = 0; x < R; x++) {
        char w[16]; for (int k = 0; k <= n; k++) w[k] = '0' + ((x >> k) & 1); w[n + 1] = 0;
        int r0 = (~x) & (R - 1), r1 = x;
        printf("%s %d %d\n", w, sub[r0], sub[r1]);
    }
    return 0;
}

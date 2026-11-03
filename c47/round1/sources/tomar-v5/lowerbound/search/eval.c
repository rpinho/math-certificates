// Area of the superlevel set {M mu >= lam} inside a rectangle ("cell") for a finite point-mass measure mu given on a
// window, M = centred maximal operator over closed axis-parallel squares. Uses the identity
//   {M mu >= lam} = union over boxes B (bounds at point coordinates) of
//                   [xb - rho, xa + rho] x [yb - rho, ya + rho],  rho = sqrt(mu(B) / (4 lam)),
// where B = [xa, xb] x [ya, yb]. Float version for the search (the certificate is checked exactly elsewhere).
// Build: gcc -O3 -march=native -shared -fPIC -o libeval.so eval.c -lm
#include <math.h>
#include <stdlib.h>
#include <string.h>

typedef struct { double x0, x1, y0, y1; } Rect;

static int cmp_d(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

static int uniq(double *v, int n) {
    qsort(v, n, sizeof(double), cmp_d);
    int k = 0;
    for (int i = 0; i < n; i++)
        if (k == 0 || v[i] != v[k - 1]) v[k++] = v[i];
    return k;
}

static int find(const double *v, int n, double x) {   // index of x in sorted unique v (exact match)
    int lo = 0, hi = n - 1;
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (v[mid] < x) lo = mid + 1; else hi = mid;
    }
    return lo;
}

// ---- union area of rectangles: sweep in x, segment tree on compressed y
typedef struct { double x; int y0, y1, d; } Ev;
static int cmp_ev(const void *a, const void *b) {
    const Ev *p = a, *q = b;
    return (p->x > q->x) - (p->x < q->x);
}
static int *cnt; static double *len, *ys_g;
static void upd(int node, int l, int r, int a, int b, int d) {   // segment [l, r) of elementary intervals
    if (b <= l || r <= a) return;
    if (a <= l && r <= b) cnt[node] += d;
    else {
        int m = (l + r) / 2;
        upd(2 * node, l, m, a, b, d); upd(2 * node + 1, m, r, a, b, d);
    }
    if (cnt[node] > 0) len[node] = ys_g[r] - ys_g[l];
    else if (r - l == 1) len[node] = 0;
    else len[node] = len[2 * node] + len[2 * node + 1];
}

static double union_area(Rect *R, int nr) {
    if (nr == 0) return 0.0;
    double *ys = malloc(sizeof(double) * 2 * nr);
    for (int i = 0; i < nr; i++) { ys[2 * i] = R[i].y0; ys[2 * i + 1] = R[i].y1; }
    int ny = uniq(ys, 2 * nr);
    Ev *ev = malloc(sizeof(Ev) * 2 * nr);
    for (int i = 0; i < nr; i++) {
        int a = find(ys, ny, R[i].y0), b = find(ys, ny, R[i].y1);
        ev[2 * i] = (Ev){R[i].x0, a, b, 1};
        ev[2 * i + 1] = (Ev){R[i].x1, a, b, -1};
    }
    qsort(ev, 2 * nr, sizeof(Ev), cmp_ev);
    int sz = 4 * ny + 8;
    cnt = calloc(sz, sizeof(int)); len = calloc(sz, sizeof(double)); ys_g = ys;
    double area = 0.0, px = ev[0].x;
    for (int i = 0; i < 2 * nr; i++) {
        area += len[1] * (ev[i].x - px);
        px = ev[i].x;
        if (ny > 1) upd(1, 0, ny - 1, ev[i].y0, ev[i].y1, ev[i].d);
    }
    free(cnt); free(len); free(ys); free(ev);
    return area;
}

double superlevel_area2(int n, const double *px, const double *py, const double *pm, double lam,
                        double cx0, double cx1, double cy0, double cy1, double reach, double rho_max, int *nrect_out);

// px, py, pm: n window points; cell = [cx0, cx1] x [cy0, cy1]; reach: max box side considered.
// Returns the area of {M mu >= lam} inside the cell; *nrect_out = number of rectangles used.
double superlevel_area(int n, const double *px, const double *py, const double *pm, double lam,
                       double cx0, double cx1, double cy0, double cy1, double reach, int *nrect_out) {
    return superlevel_area2(n, px, py, pm, lam, cx0, cx1, cy0, cy1, reach, 1e300, nrect_out);
}

// as superlevel_area, but box bounds are restricted to [c0 - rho_max, c1 + rho_max] (rho_max >= every rho that occurs)
double superlevel_area2(int n, const double *px, const double *py, const double *pm, double lam,
                        double cx0, double cx1, double cy0, double cy1, double reach, double rho_max, int *nrect_out) {
    double *X = malloc(sizeof(double) * n), *Y = malloc(sizeof(double) * n);
    memcpy(X, px, sizeof(double) * n); memcpy(Y, py, sizeof(double) * n);
    int nx = uniq(X, n), ny = uniq(Y, n);
    double *P = calloc((size_t)(nx + 1) * (ny + 1), sizeof(double));   // 2D prefix sums of masses
    for (int t = 0; t < n; t++) {
        int i = find(X, nx, px[t]), j = find(Y, ny, py[t]);
        P[(size_t)(i + 1) * (ny + 1) + (j + 1)] += pm[t];
    }
    for (int i = 1; i <= nx; i++)
        for (int j = 1; j <= ny; j++)
            P[(size_t)i * (ny + 1) + j] += P[(size_t)(i - 1) * (ny + 1) + j] + P[(size_t)i * (ny + 1) + j - 1]
                                         - P[(size_t)(i - 1) * (ny + 1) + j - 1];
    int cap = 1 << 16, nr = 0;
    Rect *R = malloc(sizeof(Rect) * cap);
    double inv4l = 1.0 / (4.0 * lam);
    for (int ia = 0; ia < nx; ia++) {
        if (X[ia] < cx0 - rho_max) continue;
        for (int ib = ia; ib < nx && X[ib] - X[ia] <= reach && X[ib] <= cx1 + rho_max; ib++) {
            for (int ja = 0; ja < ny; ja++) {
                if (Y[ja] < cy0 - rho_max) continue;
                for (int jb = ja; jb < ny && Y[jb] - Y[ja] <= reach && Y[jb] <= cy1 + rho_max; jb++) {
                    double m = P[(size_t)(ib + 1) * (ny + 1) + (jb + 1)] - P[(size_t)ia * (ny + 1) + (jb + 1)]
                             - P[(size_t)(ib + 1) * (ny + 1) + ja] + P[(size_t)ia * (ny + 1) + ja];
                    if (m <= 0) continue;
                    double rho = sqrt(m * inv4l);
                    double x0 = X[ib] - rho, x1 = X[ia] + rho, y0 = Y[jb] - rho, y1 = Y[ja] + rho;
                    if (x1 <= x0 || y1 <= y0) continue;
                    if (x0 < cx0) x0 = cx0;
                    if (x1 > cx1) x1 = cx1;
                    if (y0 < cy0) y0 = cy0;
                    if (y1 > cy1) y1 = cy1;
                    if (x1 <= x0 || y1 <= y0) continue;
                    if (nr == cap) { cap *= 2; R = realloc(R, sizeof(Rect) * cap); }
                    R[nr++] = (Rect){x0, x1, y0, y1};
                }
            }
        }
    }
    double area = union_area(R, nr);
    if (nrect_out) *nrect_out = nr;
    free(R); free(P); free(X); free(Y);
    return area;
}

// Coverage test on a grid: out[i*ny + j] = 1 if the grid point (gx[i], gy[j]) lies in some rectangle of the union
// (same enumeration as superlevel_area). Used to locate the uncovered holes of a configuration.
void coverage_grid(int n, const double *px, const double *py, const double *pm, double lam,
                   double cx0, double cx1, double cy0, double cy1, double reach,
                   int ngx, const double *gx, int ngy, const double *gy, unsigned char *out) {
    double *X = malloc(sizeof(double) * n), *Y = malloc(sizeof(double) * n);
    memcpy(X, px, sizeof(double) * n); memcpy(Y, py, sizeof(double) * n);
    int nx = uniq(X, n), ny = uniq(Y, n);
    double *P = calloc((size_t)(nx + 1) * (ny + 1), sizeof(double));
    for (int t = 0; t < n; t++) {
        int i = find(X, nx, px[t]), j = find(Y, ny, py[t]);
        P[(size_t)(i + 1) * (ny + 1) + (j + 1)] += pm[t];
    }
    for (int i = 1; i <= nx; i++)
        for (int j = 1; j <= ny; j++)
            P[(size_t)i * (ny + 1) + j] += P[(size_t)(i - 1) * (ny + 1) + j] + P[(size_t)i * (ny + 1) + j - 1]
                                         - P[(size_t)(i - 1) * (ny + 1) + j - 1];
    memset(out, 0, (size_t)ngx * ngy);
    double inv4l = 1.0 / (4.0 * lam);
    for (int ia = 0; ia < nx; ia++)
        for (int ib = ia; ib < nx && X[ib] - X[ia] <= reach; ib++)
            for (int ja = 0; ja < ny; ja++)
                for (int jb = ja; jb < ny && Y[jb] - Y[ja] <= reach; jb++) {
                    double m = P[(size_t)(ib + 1) * (ny + 1) + (jb + 1)] - P[(size_t)ia * (ny + 1) + (jb + 1)]
                             - P[(size_t)(ib + 1) * (ny + 1) + ja] + P[(size_t)ia * (ny + 1) + ja];
                    if (m <= 0) continue;
                    double rho = sqrt(m * inv4l);
                    double x0 = X[ib] - rho, x1 = X[ia] + rho, y0 = Y[jb] - rho, y1 = Y[ja] + rho;
                    if (x1 <= x0 || y1 <= y0 || x1 < cx0 || x0 > cx1 || y1 < cy0 || y0 > cy1) continue;
                    for (int a = 0; a < ngx; a++) {
                        if (gx[a] < x0 || gx[a] > x1) continue;
                        for (int b = 0; b < ngy; b++)
                            if (gy[b] >= y0 && gy[b] <= y1) out[(size_t)a * ngy + b] = 1;
                    }
                }
    free(P); free(X); free(Y);
}
